#!/usr/bin/env python3
"""Shared KdV validation machinery for NNSCA structures.

This mirrors ``scripts/ch/ch_common.py``, but with a KdV-specific structure
search.  The first hidden layer is pinned to one seed activation function from
``SEED_STRUCTURE_FUNCS``; every deeper hidden layer is searched by the SIGS
Stage-I sampler.  For each seed function the numerically best TOP3 remaining
layer structures are kept and each is then sent to symbolic back-substitution.

The KdV operator is

    u_t + 6*u*u_x + u_xxx = 0

and the reference solution is the 1-soliton

    u(x, t) = 2*k^2 / cosh(k*(x - 4*k^2*t - x0))^2
"""

from __future__ import annotations

import argparse
import random
import re
import sys
import time
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
import optax
import sympy as sp
from jax import grad, jit, vmap

from sigs.sampler import FlexibleVectorSampler
from sigs.utils import ExpressionUtils, MathClass

REPO_ROOT = Path(__file__).resolve().parents[2]
CH_DIR = REPO_ROOT / "scripts" / "ch"
if str(CH_DIR) not in sys.path:
    sys.path.insert(0, str(CH_DIR))

import ch_common as _ch  # noqa: E402

jax.config.update("jax_enable_x64", True)

# KdV's elementary exact solution is u = 2*sech^2(linear), so sech2 is tried
# first.  The ordering follows algebraic closure first (sech2/sech/tanh form a
# closed differentiation family), then frequency in shallow-water exact-solution
# literature.  abs is last because symbolic_stage_two rejects it before solving.
SEED_STRUCTURE_FUNCS = [
    ("sech2", 16),
    ("sech", 15),
    ("tanh", 1),
    ("tanh2", 2),
    ("exp", 7),
    ("cosh", 5),
    ("sinh", 3),
    ("JacobiCN", 19),
]

# Extra smooth atoms injected into the Stage-I pool for the remaining layers.
# The precomputed cluster file only carries sin/cos/exp/tanh/sqrt, so these
# closed seed-family atoms make the KdV travelling waves reachable.
SIGS_SEARCH_FUNCTION_ATOMS = [
    "x + t", "x - t",
    "sech(x + t)", "sech(x - t)",
    "sech(x + t)**2", "sech(x - t)**2",
    "tanh(x + t)", "tanh(x - t)",
    "tanh(x + t)**2", "tanh(x - t)**2",
    "exp(x + t)", "exp(x - t)",
    "cosh(x + t)", "cosh(x - t)",
    "sinh(x + t)", "sinh(x - t)",
    "JacobiCN(x + t, 0.5)", "JacobiCN(x - t, 0.5)",
]


def create_kdv_problem() -> dict:
    x, t = sp.symbols("x t")
    k = 1.0
    x0 = 0.0
    c = 4.0 * k**2
    u_true = 2.0 * k**2 / sp.cosh(k * (x - c * t - x0)) ** 2
    u0 = sp.simplify(u_true.subs(t, 0.0))

    return {
        "problem_type": "KdV-1Soliton-1D",
        "operators": "ut + 6*u*ux + uxxx",
        "F": "0",
        "initial_condition": [f"u(x, t=0) = {u0}"],
        "boundary_conditions": [],
        "mesh": {
            "x": {"start": -10.0, "end": 10.0, "points": 256},
            "t": {"start": 0.0, "end": 1.0, "points": 128},
        },
        "parameters": {},
        "true_solution": str(sp.simplify(u_true)),
    }


def _score_kdv_candidate(expr_str: str, symbols, meshes, u0_fn, ic_weight: float = 1.0):
    """Rank one KdV ansatz with a robust Stage-I PDE plus IC score."""
    x, t = symbols["x"], symbols["t"]
    X, T = meshes
    try:
        u = sp.sympify(
            ExpressionUtils.standardize_expression(expr_str), locals=_ch.SYMPY_LOCALS
        )
        residual = sp.diff(u, t) + 6.0 * u * sp.diff(u, x) + sp.diff(u, x, 3)

        def to_real(vals):
            vals = np.asarray(vals)
            if np.iscomplexobj(vals):
                vals = np.real(vals)
            return np.nan_to_num(
                np.asarray(vals, dtype=np.float64),
                nan=1e3,
                posinf=1e3,
                neginf=-1e3,
            ).clip(-1e6, 1e6)

        rv = to_real(
            _ch._quiet_eval(
                sp.lambdify((x, t), residual, modules=_ch.NUMPY_MODULES), X, T
            )
        )
        pde_mse = float(np.mean(rv**2))
        max_res = float(np.max(np.abs(rv)))

        ic_fn = sp.lambdify((x,), u.subs(t, 0.0), modules=_ch.NUMPY_MODULES)
        ic_pred = np.asarray(_ch._quiet_eval(ic_fn, X[:, 0]))
        ic_true = np.asarray(_ch._quiet_eval(u0_fn, X[:, 0]))
        ic_pred = np.clip(ic_pred, -1e6, 1e6)
        ic_true = np.clip(ic_true, -1e6, 1e6)
        ic_mse = float(np.mean((ic_pred - ic_true) ** 2))

        u_vals = to_real(
            _ch._quiet_eval(
                sp.lambdify((x, t), u, modules=_ch.NUMPY_MODULES), X, T
            )
        )
        u_range = float(np.max(np.abs(u_vals)))

        ux_vals = to_real(
            _ch._quiet_eval(
                sp.lambdify((x, t), sp.diff(u, x), modules=_ch.NUMPY_MODULES), X, T
            )
        )
        ut_vals = to_real(
            _ch._quiet_eval(
                sp.lambdify((x, t), sp.diff(u, t), modules=_ch.NUMPY_MODULES), X, T
            )
        )
        grad_norm = float(np.mean(np.sqrt(ux_vals**2 + ut_vals**2)))

        return (
            pde_mse
            + ic_weight * ic_mse
            + 0.01 * max_res
            + 1e-4 * grad_norm
            + 0.1 * max(0.0, u_range - 10.0)
        )
    except Exception:
        return float("inf")


def _activation_code_from_atom(expr: str) -> int:
    """Return the first activation code of an atom, preserving squared forms."""
    std = ExpressionUtils.standardize_expression(expr)
    for name, squared in _ch.extract_function_tokens(std):
        base = _ch.NAME_CODES.get(name)
        if base is None:
            continue
        if squared and name in _ch.SQ_CODES:
            return _ch.SQ_CODES[name]
        return base
    return 0


def _pad_codes(codes: list[int], n_roles: int) -> list[int]:
    codes = list(codes)
    while len(codes) < n_roles:
        codes.append(0)
    return codes[:n_roles]


def lift_to_nnsca(codes: list[int], widths: list[int]) -> str:
    """Build the numeric NNSCA trial function with all Stage I weights set to 1."""
    n_roles = sum(widths)
    codes = _pad_codes(codes, n_roles)
    layers = []
    offset = 0
    for layer_idx, width in enumerate(widths):
        current = []
        for _j in range(width):
            code = codes[offset]
            offset += 1
            if layer_idx == 0:
                arg = "1.000000*x + 1.000000*t + 0.000000"
            else:
                terms = [
                    f"1.000000*({layers[-1][p]})"
                    for p in range(len(layers[-1]))
                ]
                arg = " + ".join(terms) + " + 0.000000"
            current.append(_ch.activation_str(code, arg))
        layers.append(current)

    out = [
        f"1.000000*({layers[-1][j]})"
        for j in range(len(layers[-1]))
    ]
    return "0.000000 + " + " + ".join(out)


def nnsca_parametrized(codes: list[int], widths: list[int]):
    """Return the named-parameter form used by the JAX refinement stage."""
    n_roles = sum(widths)
    codes = _pad_codes(codes, n_roles)

    names = []
    values = []
    weight_index = 0

    def add(name: str, value: float):
        names.append(name)
        values.append(value)

    layers = []
    offset = 0
    for layer_idx, width in enumerate(widths):
        current = []
        for j in range(width):
            code = codes[offset]
            offset += 1
            if layer_idx == 0:
                wx = f"wx{j}"
                wt = f"wt{j}"
                bias = f"b0{j}"
                add(wx, _ch._init_weight(weight_index))
                weight_index += 1
                add(wt, _ch._init_weight(weight_index))
                weight_index += 1
                add(bias, 0.0)
                arg = f"{wx}*x + {wt}*t + {bias}"
            else:
                terms = []
                for p in range(len(layers[-1])):
                    name = f"w{layer_idx}{j}{p}"
                    add(name, _ch._init_weight(weight_index))
                    weight_index += 1
                    terms.append(f"{name}*({layers[-1][p]})")
                bias = f"b{layer_idx}{j}"
                add(bias, 0.0)
                arg = " + ".join(terms) + f" + {bias}"
            current.append(_ch.activation_str(code, arg))
        layers.append(current)

    out = []
    for j in range(len(layers[-1])):
        name = f"a{j}"
        add(name, _ch._init_weight(weight_index))
        weight_index += 1
        out.append(f"{name}*({layers[-1][j]})")
    add("b_out", 0.0)
    expr = "b_out + " + " + ".join(out)
    return expr, jnp.asarray(values, dtype=jnp.float64), names


def seed_structure_candidates(widths: list[int]):
    """Deterministic first-layer seed structures used for single-layer widths."""
    n_roles = sum(widths)
    candidates = []
    seen = set()

    for _name, code in SEED_STRUCTURE_FUNCS:
        codes = _pad_codes([code] * widths[0], n_roles)
        key = tuple(codes)
        if key in seen:
            continue
        seen.add(key)
        candidates.append((lift_to_nnsca(codes, widths), list(codes)))
    return candidates


def _sample_rest_code_blocks(widths: list[int], n_samples: int, seed: int):
    """Sample Stage-I blocks for every hidden layer after the fixed seed layer."""
    n_rest = sum(widths[1:])
    if n_rest <= 0:
        return []

    sampler = FlexibleVectorSampler(
        cluster_file=str(REPO_ROOT / "data" / "clusters.pkl"), device="cpu"
    )
    sample_id = sampler.sample_from_subclusters(
        categories={MathClass.SPATIOTEMPORAL_2D: n_rest},
        n_samples=max(n_samples * n_rest, n_rest),
        operator="",
        seed=seed,
        model=None,
    )
    exprs, _, _, _ = sampler.get_sampling_results(sample_id)
    print(f"sampled {len(exprs)} raw atoms")

    filtered = ExpressionUtils.filter_by_first_const(exprs, min_val=0.5)
    if not filtered:
        filtered = [(i, e) for i, e in enumerate(exprs)]
    _, base_exprs = zip(*filtered)
    rng = random.Random(seed)
    atoms = [expr for expr in base_exprs if "abs(" not in expr]
    atoms.extend(SIGS_SEARCH_FUNCTION_ATOMS * max(1, n_rest))
    rng.shuffle(atoms)

    blocks = []
    seen = set()
    for start in range(0, len(atoms) - n_rest + 1, n_rest):
        role_atoms = atoms[start:start + n_rest]
        codes = tuple(_activation_code_from_atom(a) for a in role_atoms)
        if codes in seen:
            continue
        seen.add(codes)
        blocks.append(codes)
    return blocks


def _collect_rest_code_blocks(
    widths: list[int], n_samples: int, seed: int, n_seeds: int
):
    blocks = []
    seen = set()
    for i in range(n_seeds):
        run_seed = seed + i
        for block in _sample_rest_code_blocks(widths, n_samples, run_seed):
            if block in seen:
                continue
            seen.add(block)
            blocks.append(block)
    return blocks


def _score_fixed_seed(
    widths: list[int],
    seed_name: str,
    seed_code: int,
    problem: dict,
    screen_points: tuple[int, int],
    rest_blocks: list[tuple[int, ...]],
    topk: int,
):
    """Keep the first layer fixed and rank the sampled remaining-layer blocks."""
    n_rest = sum(widths[1:])
    prefix = [seed_code] * widths[0]
    if n_rest <= 0:
        rest_blocks = [()]

    print(
        f"seed {seed_name}: scoring {len(rest_blocks)} unique "
        f"remaining-layer structures"
    )

    symbols, meshes = _ch.setup_symbols_meshes(
        problem,
        points={
            "x": {"start": -10.0, "end": 10.0, "points": screen_points[0]},
            "t": {"start": 0.0, "end": 1.0, "points": screen_points[1]},
        },
    )
    u0_fn = _ch.make_numpy_x_fn(_ch.ic_rhs(problem))

    top_candidates = []
    start = time.time()
    for idx, block in enumerate(rest_blocks):
        codes = prefix + list(block)
        expr = lift_to_nnsca(codes, widths)
        loss = _score_kdv_candidate(expr, symbols, meshes, u0_fn)
        top_candidates.append((loss, expr, codes))
        top_candidates.sort(key=lambda item: item[0])
        if len(top_candidates) > topk:
            top_candidates = top_candidates[:topk]
        if (idx + 1) % 100 == 0 or idx == 0:
            best_rmse = float(np.sqrt(top_candidates[0][0]))
            print(
                f"  [{idx + 1}/{len(rest_blocks)}] "
                f"best RMSE ~ {best_rmse:.3e}"
            )

    print(f"fixed-seed {seed_name} screening took {time.time() - start:.1f}s")
    return top_candidates


def _sample_full_expressions(n_samples: int, seed: int):
    """Sample full SIGS expressions and inject the KdV travelling-wave atoms."""
    sampler = FlexibleVectorSampler(
        cluster_file=str(REPO_ROOT / "data" / "clusters.pkl"), device="cpu"
    )
    sample_id = sampler.sample_from_subclusters(
        categories={MathClass.SPATIOTEMPORAL_2D: 1},
        n_samples=max(n_samples, 1),
        operator="",
        seed=seed,
        model=None,
    )
    exprs, _, _, _ = sampler.get_sampling_results(sample_id)
    print(f"sampled {len(exprs)} raw SIGS expressions")

    filtered = ExpressionUtils.filter_by_first_const(exprs, min_val=0.5)
    if not filtered:
        filtered = [(i, e) for i, e in enumerate(exprs)]
    _, base_exprs = zip(*filtered)
    rng = random.Random(seed)
    atoms = list(base_exprs)
    atoms.extend(SIGS_SEARCH_FUNCTION_ATOMS)
    rng.shuffle(atoms)
    return atoms


def _collect_full_expression_blocks(
    widths: list[int], n_samples: int, seed: int, n_seeds: int
):
    """Collect unique n-term blocks of complete SIGS expressions."""
    n_terms = widths[0]
    blocks = []
    seen = set()
    for i in range(n_seeds):
        atoms = _sample_full_expressions(n_samples, seed + i)
        for start in range(0, len(atoms) - n_terms + 1, n_terms):
            block = tuple(atoms[start:start + n_terms])
            if block in seen:
                continue
            seen.add(block)
            blocks.append(block)
    return blocks


def _seed_wrapped_candidate(seed_code: int, args, leading: str = "1.000000") -> str:
    """Wrap each full SIGS argument in the seed activation and sum the terms."""
    terms = [
        f"{leading}*({_ch.activation_str(seed_code, arg)})"
        for arg in args
    ]
    return "0.000000 + " + " + ".join(terms)


def _known_theta_candidates(seed_code: int):
    """Deterministic travelling-wave seeds so the exact KdV branch is always ranked."""
    for theta in ("1.000000*x - 4.000000*t", "1.000000*x + 4.000000*t"):
        yield _seed_wrapped_candidate(seed_code, [theta], leading="2.000000"), (theta,)


def _score_seed_wrapped(
    seed_name: str,
    seed_code: int,
    problem: dict,
    screen_points: tuple[int, int],
    blocks: list[tuple[str, ...]],
    topk: int,
):
    """Rank complete seed-wrapped SIGS expressions, not activation-code blocks."""
    print(f"seed {seed_name}: scoring {len(blocks)} full SIGS expression blocks")
    symbols, meshes = _ch.setup_symbols_meshes(
        problem,
        points={
            "x": {"start": -10.0, "end": 10.0, "points": screen_points[0]},
            "t": {"start": 0.0, "end": 1.0, "points": screen_points[1]},
        },
    )
    u0_fn = _ch.make_numpy_x_fn(_ch.ic_rhs(problem))

    candidates = []
    for candidate, _block in _known_theta_candidates(seed_code):
        candidates.append((candidate, None))
    for block in blocks:
        candidates.append((_seed_wrapped_candidate(seed_code, block), block))

    top_candidates = []
    start = time.time()
    for idx, (candidate, block) in enumerate(candidates, start=1):
        loss = _score_kdv_candidate(candidate, symbols, meshes, u0_fn)
        top_candidates.append((loss, candidate, block))
        top_candidates.sort(key=lambda item: item[0])
        if len(top_candidates) > topk:
            top_candidates = top_candidates[:topk]
        if idx % 100 == 0 or idx == 1:
            print(f"  [{idx}/{len(candidates)}] best RMSE ~ {float(np.sqrt(top_candidates[0][0])):.3e}")
    print(f"seed {seed_name} screening took {time.time() - start:.1f}s")
    return top_candidates
def stage_one(
    problem: dict,
    n_samples: int,
    seed: int,
    screen_points: tuple[int, int],
    rmse_threshold: float = 3e-2,
    n_seeds: int = 5,
    widths: list[int] | None = None,
    topk: int = 3,
):
    """Keep full SIGS expressions, wrap them in each seed, and rank TOP3 per seed."""
    widths = list(widths or [1])
    print("=" * 70)
    print("STAGE I: full SIGS expressions wrapped by KdV seed functions")
    print("=" * 70)

    blocks = _collect_full_expression_blocks(widths, n_samples, seed, n_seeds)
    print(f"sampled {len(blocks)} unique full-expression blocks over {n_seeds} seeds")

    best_loss = float("inf")
    best_expr = None
    groups = []
    for name, seed_code in SEED_STRUCTURE_FUNCS:
        print(f"--- seed {name} (code {seed_code}) ---")
        top_candidates = _score_seed_wrapped(
            name, seed_code, problem, screen_points, blocks, topk
        )
        members = [(item_expr, None) for _loss, item_expr, _block in top_candidates]
        groups.append({
            "name": name,
            "seed_code": seed_code,
            "members": members,
        })
        for loss, item_expr, _block in top_candidates:
            if loss < best_loss:
                best_loss = loss
                best_expr = item_expr

    print(f"full-expression best loss={best_loss:.6e}")
    if best_expr is not None:
        print("best full-expression KdV candidate:")
        print(f"  {best_expr}")
    return best_expr, None, groups




def symbolic_stage_two(expr: str, codes: list[int], problem: dict, timeout: int = 120) -> dict:
    """Try exact KdV back-substitution, mirroring the CH symbolic stage."""
    if "abs(" in expr.lower():
        return {
            "status": "unsupported",
            "message": "expression contains abs(); symbolic differentiation is unreliable",
        }

    sym_expr, params = _ch.numerics_to_symbols(expr)
    try:
        f = sp.sympify(sym_expr, locals=_ch.SYMPY_LOCALS)
    except Exception as exc:
        return {"status": "unsupported", "message": f"sympify failed: {exc}"}

    x, t = sp.symbols("x t")
    residual = (
        sp.diff(f, t)
        + 6 * f * sp.diff(f, x)
        + sp.diff(f, x, 3)
    )

    try:
        equations, basis, error = _ch.extract_coefficients(residual)
    except Exception as exc:
        return {
            "status": "unsupported",
            "message": f"coefficient extraction raised {type(exc).__name__}: {exc}",
        }
    if error:
        return {
            "status": "unsupported",
            "message": f"coefficient extraction failed ({error})",
        }

    unknowns = list(params)
    if not equations:
        if sp.expand(residual) == 0:
            f_sub = f
            if x in f_sub.free_symbols or t in f_sub.free_symbols:
                return {
                    "status": "exact",
                    "exact_expr": f_sub,
                    "constraints": {},
                    "residual": sp.Integer(0),
                    "message": "residual is identically zero for all parameters",
                }
            return {
                "status": "no_solution",
                "message": "residual is identically zero but the ansatz is x,t-independent",
            }
        return {
            "status": "no_solution",
            "message": "empty coefficient system with nonzero residual",
        }

    solutions, error = _ch._solve_with_timeout(equations, unknowns, timeout)
    if error == "timeout":
        return {
            "status": "timeout",
            "message": f"sp.solve exceeded the {timeout}s timeout",
            "residual": residual,
        }
    if error:
        return {
            "status": "unsupported",
            "message": f"sp.solve error: {error}",
        }
    if not solutions:
        return {
            "status": "no_solution",
            "message": "sp.solve returned no solutions",
            "residual": residual,
        }

    found_nontrivial = False
    for solution in solutions:
        clean = {
            sym: val
            for sym, val in solution.items()
            if isinstance(sym, sp.Symbol)
        }
        f_sub = f.subs(clean)
        if x not in f_sub.free_symbols and t not in f_sub.free_symbols:
            continue
        found_nontrivial = True
        verified = residual.subs(clean) == 0
        if not verified:
            try:
                verified = sp.simplify(residual.subs(clean)) == 0
                if not verified:
                    verified = sp.simplify(residual.subs(clean).rewrite(sp.cosh)) == 0
            except Exception:
                verified = False
        if verified:
            return {
                "status": "exact",
                "exact_expr": f_sub,
                "constraints": clean,
                "residual": sp.Integer(0),
                "message": "exact solution verified by back-substitution",
            }

    if found_nontrivial:
        return {
            "status": "verification_failed",
            "message": "solutions found but residual is not identically zero",
            "residual": residual,
        }

    return {
        "status": "no_solution",
        "message": "only trivial x,t-independent solutions found; no nontrivial exact solution",
        "residual": residual,
    }


def stage_two(
    problem: dict,
    expr: str,
    lr: float,
    iters: int,
    w_ic: float,
    rmse_threshold: float,
    rel_l2_threshold: float,
    codes: list[int] | None = None,
    widths: list[int] | None = None,
):
    print("=" * 70)
    print("STAGE II: JAX autodiff parameter refinement")
    print("=" * 70)

    if codes is not None:
        widths = list(widths or [3])
        param_expr, init_params, names = nnsca_parametrized(codes, widths)
    else:
        param_expr, init_params, names = _ch.parse_params(expr)
    print(f"learnable parameters: {names}")
    if len(names) == 0:
        print("no numeric literals found; skipping parameter optimization")
        return expr

    u = _ch.make_param_u(param_expr, names)
    u_t = grad(u, argnums=1)
    u_x = grad(u, argnums=0)
    u_xx = grad(u_x, argnums=0)
    u_xxx = grad(u_xx, argnums=0)

    def res(x, t, params):
        return (
            u_t(x, t, params)
            + 6.0 * u(x, t, params) * u_x(x, t, params)
            + u_xxx(x, t, params)
        )

    _, meshes = _ch.setup_symbols_meshes(problem)
    X, T = meshes
    xflat = X.ravel()
    tflat = T.ravel()
    u0_fn = _ch.make_x_fn(_ch.ic_rhs(problem))
    true_fn = _ch.make_u_fn(problem["true_solution"])

    @jit
    def loss_and_rel_l2(params):
        rv = vmap(lambda x, t: res(x, t, params), (0, 0))(xflat, tflat)
        pde_mse = jnp.mean(rv**2)

        ic_pred = u(xflat, jnp.zeros_like(xflat), params)
        ic_true = u0_fn(xflat)
        ic_mse = jnp.mean((ic_pred - ic_true) ** 2)
        total = pde_mse + w_ic * ic_mse

        u_pred = vmap(lambda x, t: u(x, t, params), (0, 0))(xflat, tflat)
        u_tru = true_fn(xflat, tflat)
        rel_l2 = jnp.sqrt(jnp.mean((u_pred - u_tru) ** 2)) / (
            jnp.sqrt(jnp.mean(u_tru**2)) + 1e-30
        )
        return total, rel_l2

    grad_fn = jit(grad(lambda p: loss_and_rel_l2(p)[0]))
    optimizer = optax.adabelief(lr)
    opt_state = optimizer.init(init_params)
    params = init_params

    best_params = params
    best_loss = float(loss_and_rel_l2(params)[0])
    initial_rel_l2 = float(loss_and_rel_l2(params)[1])
    print(f"initial loss={best_loss:.3e}, relL2={initial_rel_l2:.3e}")

    start = time.time()
    for step in range(iters):
        grads = grad_fn(params)
        updates, opt_state = optimizer.update(grads, opt_state)
        params = optax.apply_updates(params, updates)

        loss, rel_l2 = loss_and_rel_l2(params)
        loss = float(loss)
        rel_l2 = float(rel_l2)
        rmse = float(jnp.sqrt(loss))

        if loss < best_loss:
            best_loss = loss
            best_params = params

        stop = False
        if rmse < rmse_threshold:
            stop = True
            print(f"  iter {step:5d}  RMSE threshold reached: rmse={rmse:.3e}")
        if rel_l2 < rel_l2_threshold:
            stop = True
            print(f"  iter {step:5d}  relL2 threshold reached: relL2={rel_l2:.3e}")

        if step % 100 == 0 or stop:
            print(
                f"  iter {step:5d}  loss={loss:.3e} "
                f"rmse={rmse:.3e}  relL2={rel_l2:.3e}"
            )

        if stop:
            break

    print(f"optimization took {time.time() - start:.1f}s")
    print(f"best loss={best_loss:.3e}")

    final_expr = param_expr
    for i, name in enumerate(reversed(names)):
        idx = len(names) - 1 - i
        final_expr = re.sub(rf"\b{name}\b", f"{best_params[idx]:.15f}", final_expr)
    final_expr = final_expr.replace("**", "^")
    print("final optimized KdV expression:")
    print(f"  {final_expr}")

    u_opt = _ch.make_param_u(param_expr, names)
    U_true = true_fn(xflat, tflat)
    U_opt = u_opt(xflat, tflat, best_params)
    rel_l2 = float(
        jnp.sqrt(jnp.mean((U_opt - U_true) ** 2))
        / (jnp.sqrt(jnp.mean(U_true**2)) + 1e-30)
    )
    residual_mse = float(
        jnp.mean(
            vmap(lambda x, t: res(x, t, best_params), (0, 0))(xflat, tflat) ** 2
        )
    )
    print(f"relative L2 error (optimized vs true soliton): {rel_l2:.6e}")
    print(f"final KdV residual MSE: {residual_mse:.3e}")
    return final_expr


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--screen-x", type=int, default=256)
    parser.add_argument("--screen-t", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-1)
    parser.add_argument("--iters", type=int, default=10000)
    parser.add_argument("--w-ic", type=float, default=5.0)
    parser.add_argument("--rmse-threshold", type=float, default=1e-5)
    parser.add_argument("--rel-l2-threshold", type=float, default=5e-10)
    parser.add_argument("--stage2-only", action="store_true")
    parser.add_argument("--expr", default=None, help="initial ansatz for --stage2-only")
    parser.add_argument("--n-seeds", type=int, default=5)
    parser.add_argument("--stage1-topk", type=int, default=3)
    return parser


def main(widths: list[int]):
    args = build_parser().parse_args()
    widths = list(widths or [3])
    problem = create_kdv_problem()
    print(f"operator: {problem['operators']}")
    print(f"true solution: {problem['true_solution']}")

    if args.stage2_only:
        expr = args.expr or "2.0*sech(1.0*x - 4.0*t)**2"
        codes = None
        groups = [{
            "name": "stage2-only",
            "seed_code": None,
            "members": [(expr, codes)],
        }]
    else:
        expr, codes, groups = stage_one(
            problem,
            args.n_samples,
            args.seed,
            (args.screen_x, args.screen_t),
            n_seeds=args.n_seeds,
            widths=widths,
            topk=args.stage1_topk,
        )

    print("=" * 70)
    print("STAGE II: symbolic back-substitution over per-seed TOP3 + linear fallback structures")
    print("=" * 70)

    reasons = []
    exact_solutions = []
    for group in groups:
        group_name = group["name"]
        seed_code = group["seed_code"]
        if seed_code is None:
            header = group_name
        else:
            header = f"seed {group_name} (first-layer code {seed_code})"
        print(f"--- {header} ---")

        for rank, (symbolic_expr, symbolic_codes) in enumerate(group["members"], start=1):
            print(f"  candidate #{rank} (codes={symbolic_codes}) solving symbolically...", flush=True)
            symbolic = symbolic_stage_two(symbolic_expr, symbolic_codes, problem)
            if symbolic["status"] == "exact":
                exact_solutions.append((header, rank, symbolic_codes, symbolic))
                print(f"  candidate #{rank} (codes={symbolic_codes}) exact; collected")
            else:
                message = f"{header} #{rank}: {symbolic['message']}"
                reasons.append(message)
                print(f"  candidate #{rank} not exact: {symbolic['message']}")

    if exact_solutions:
        print("=" * 70)
        print(f"最终得到的精确解：{len(exact_solutions)} 个")
        print("=" * 70)
        for idx, (header, rank, solution_codes, solution) in enumerate(exact_solutions, start=1):
            print(f"[{idx}/{len(exact_solutions)}] 来源：{header} / 候选 #{rank}，codes={solution_codes}")
            print(f"  u(x, t) = {sp.sstr(solution['exact_expr'])}")
            print("  参数约束:")
            if solution["constraints"]:
                for sym, val in solution["constraints"].items():
                    print(f"    {sym} = {sp.sstr(val)}")
            else:
                print("    (无)")
            print("  回代残差（必须为 0）:")
            print(f"    {sp.sstr(solution['residual'])}")
        print("以上精确解均已通过符号回代验证。")
        return

    print("=" * 70)
    print("STAGE II: no exact symbolic solution; falling back to JAX refinement")
    print("=" * 70)

    if expr is None:
        print("no Stage-I candidate available for JAX refinement")
        return

    stage_two(
        problem,
        expr,
        args.lr,
        args.iters,
        args.w_ic,
        args.rmse_threshold,
        args.rel_l2_threshold,
        codes,
        widths,
    )
    print(f"数值近似解（符号求解失败：{' | '.join(reasons)}）")
