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
import signal
import sys
import time
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
import sympy as sp
from scipy.optimize import minimize

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
    "1/(x - t)", "1/(x + t)",
    "(x - t)/(x + t)", "(x + t)/(x - t)",
    "1/(1 + (x - t)**2)", "1/(1 + (x + t)**2)",
    "(x - t)/(1 + (x - t)**2)", "(x + t)/(1 + (x + t)**2)",
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
    atoms = [expr for expr in list(base_exprs) + SIGS_SEARCH_FUNCTION_ATOMS if _is_allowed_inner_expr(expr)]
    if not atoms:
        atoms = [expr for expr in SIGS_SEARCH_FUNCTION_ATOMS if _is_allowed_inner_expr(expr)]
    rng.shuffle(atoms)
    return atoms


def _is_allowed_inner_expr(expr: str) -> bool:
    """Reject Stage-I atoms with deeply nested tanh/sech or abs."""
    std = ExpressionUtils.standardize_expression(expr)
    if "abs(" in std:
        return False
    try:
        u = sp.sympify(std, locals=_ch.SYMPY_LOCALS)
    except Exception:
        return False
    for atom in u.atoms(sp.Function):
        if atom.func in (sp.tanh, sp.sech):
            if any(arg.has(sp.tanh, sp.sech) for arg in atom.args):
                return False
    return True


def _expression_complexity(expr: str) -> float:
    """Count SymPy operations as a cheap structural-complexity measure."""
    try:
        u = sp.sympify(ExpressionUtils.standardize_expression(expr), locals=_ch.SYMPY_LOCALS)
        return float(sp.count_ops(u))
    except Exception:
        return float("inf")


def _max_tanh_sech_depth(expr: str) -> int:
    """Return the deepest nesting level of tanh/sech in an expression."""
    try:
        u = sp.sympify(ExpressionUtils.standardize_expression(expr), locals=_ch.SYMPY_LOCALS)
    except Exception:
        return 999
    best = 0

    def walk(node, depth):
        nonlocal best
        if node.func in (sp.tanh, sp.sech):
            depth += 1
            best = max(best, depth)
        for arg in node.args:
            walk(arg, depth)

    walk(u, 0)
    return best


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
            if not all(_is_allowed_inner_expr(atom) for atom in block):
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


def _score_kdv_candidate_unbiased(
    expr_str: str,
    symbols: dict,
    meshes: list[np.ndarray],
    act_floor: float = 1e-3,
    w_act: float = 1.0,
    u_max: float = 10.0,
):
    """Rank one KdV ansatz without any reference-solution term.

    The original score contains ``ic_weight * ic_mse``, where ``ic_mse`` is the
    t=0 mismatch against the known soliton.  That single term forces Stage I to
    rediscover the reference branch.  This score keeps only equation residual
    and domain safety, plus an anti-triviality barrier that pushes the search
    away from constant (exact but useless) solutions.
    """
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
        activity = float(np.mean(np.sqrt(ux_vals**2 + ut_vals**2)))

        u_vals = to_real(
            _ch._quiet_eval(
                sp.lambdify((x, t), u, modules=_ch.NUMPY_MODULES), X, T
            )
        )
        u_range = float(np.max(np.abs(u_vals)))
        bounded = float(max(0.0, u_range - u_max) ** 2)
        trivial = float(max(0.0, act_floor - activity) ** 2)
        return pde_mse + 0.01 * max_res + w_act * trivial + bounded
    except Exception:
        return float("inf")


def _refine_kdv_candidate_params(
    expr_str: str,
    symbols: dict,
    meshes: list[np.ndarray],
    opt_points: tuple[int, int] = (48, 24),
    maxiter: int = 50,
    act_floor: float = 1e-3,
    w_act: float = 1.0,
    u_max: float = 10.0,
):
    """Optimize the numeric parameters of one seed-wrapped SIGS expression.

    The candidate is the agreed Stage-I form: a seed activation on the outside
    and complete SIGS-generated expressions inside.  The inner and outer numeric
    literals are promoted to free parameters and refined against the KdV
    residual only, with an anti-triviality barrier.  Ranking uses the optimized
    residual rather than the unit-weight residual used by the cheap prefilter.
    """
    try:
        param_expr, init_params, names = _ch.parse_params(expr_str)
    except Exception:
        return float("inf"), expr_str
    if not names:
        return float("inf"), expr_str

    try:
        x, t = symbols["x"], symbols["t"]
        u = sp.sympify(param_expr, locals=_ch.SYMPY_LOCALS)
        residual = sp.diff(u, t) + 6.0 * u * sp.diff(u, x) + sp.diff(u, x, 3)
        param_syms = [sp.Symbol(name) for name in names]
        args = [x, t] + param_syms
        res_fn = sp.lambdify(args, residual, modules=_ch.NUMPY_MODULES)
        ux_fn = sp.lambdify(args, sp.diff(u, x), modules=_ch.NUMPY_MODULES)
        ut_fn = sp.lambdify(args, sp.diff(u, t), modules=_ch.NUMPY_MODULES)
        u_fn = sp.lambdify(args, u, modules=_ch.NUMPY_MODULES)
    except Exception:
        return float("inf"), expr_str

    X, T = meshes
    xs = np.linspace(float(X[:, 0].min()), float(X[:, 0].max()), opt_points[0])
    ts = np.linspace(float(T[0, :].min()), float(T[0, :].max()), opt_points[1])
    XX, TT = np.meshgrid(xs, ts, indexing="ij")
    xflat = XX.ravel()
    tflat = TT.ravel()

    def _safe(vals):
        vals = np.asarray(vals)
        if np.iscomplexobj(vals):
            vals = np.real(vals)
        return np.nan_to_num(
            np.asarray(vals, dtype=np.float64),
            nan=1e3, posinf=1e3, neginf=-1e3,
        ).clip(-1e6, 1e6)

    def loss(params):
        rv = _safe(res_fn(xflat, tflat, *params))
        pde_mse = float(np.mean(rv**2))
        uxv = _safe(ux_fn(xflat, tflat, *params))
        utv = _safe(ut_fn(xflat, tflat, *params))
        activity = float(np.mean(np.sqrt(uxv**2 + utv**2)))
        uv = _safe(u_fn(xflat, tflat, *params))
        bounded = float(max(0.0, np.max(np.abs(uv)) - u_max) ** 2)
        trivial = float(max(0.0, act_floor - activity) ** 2)
        return pde_mse + w_act * trivial + bounded

    try:
        result = minimize(
            loss,
            init_params,
            method="L-BFGS-B",
            options={"maxiter": maxiter, "ftol": 1e-12, "gtol": 1e-8},
        )
    except Exception:
        return float("inf"), expr_str

    if not np.isfinite(result.fun) or not np.all(np.isfinite(result.x)):
        return float("inf"), expr_str

    refined = param_expr
    for name, value in zip(names, result.x):
        refined = re.sub(rf"\b{name}\b", f"{float(value):.15g}", refined)
    return float(result.fun), refined


def _score_multi_point_generalization(
    refined_expr: str,
    symbols: dict,
    meshes: list[np.ndarray],
    n_perturbations: int = 5,
    perturb_scale: float = 0.3,
):
    """Penalize parameter-space overfitting for a refined candidate.

    A single optimized parameter vector can exploit the mesh.  This score
    evaluates the PDE residual at the optimized point and at nearby perturbed
    points, returning a weighted combination that rewards flat residual basins.
    """
    try:
        param_expr, init_params, names = _ch.parse_params(refined_expr)
        base = np.asarray(init_params, dtype=np.float64)
    except Exception:
        return float("inf")
    if base.size == 0:
        return float("inf")

    try:
        x, t = symbols["x"], symbols["t"]
        u = sp.sympify(param_expr, locals=_ch.SYMPY_LOCALS)
        residual = sp.diff(u, t) + 6.0 * u * sp.diff(u, x) + sp.diff(u, x, 3)
        res_fn = sp.lambdify(
            [x, t] + [sp.Symbol(name) for name in names],
            residual,
            modules=_ch.NUMPY_MODULES,
        )
    except Exception:
        return float("inf")

    X, T = meshes
    xflat = np.asarray(X, dtype=np.float64).ravel()
    tflat = np.asarray(T, dtype=np.float64).ravel()

    def _mse(params):
        params = np.asarray(params, dtype=np.float64)
        if not np.all(np.isfinite(params)):
            return float("inf")
        try:
            rv = np.asarray(res_fn(xflat, tflat, *params), dtype=np.float64)
        except Exception:
            return float("inf")
        if np.iscomplexobj(rv):
            rv = np.real(rv)
        rv = np.nan_to_num(
            rv, nan=1e3, posinf=1e3, neginf=-1e3
        )
        return float(np.mean(rv**2))

    base_mse = _mse(base)
    perturbed_mses = []
    rng = np.random.default_rng()
    for _ in range(n_perturbations):
        scales = np.maximum(np.abs(base), 0.1)
        noise = rng.normal(0.0, perturb_scale, size=base.shape)
        perturbed_mses.append(_mse(base + noise * scales))

    return base_mse + 0.5 * float(np.mean(perturbed_mses)) + 0.5 * float(np.max(perturbed_mses))


def _score_seed_wrapped(
    seed_name: str,
    seed_code: int,
    problem: dict,
    screen_points: tuple[int, int],
    blocks: list[tuple[str, ...]],
    topk: int,
    act_floor: float = 1e-3,
    refine_maxiter: int = 50,
    w_complexity: float = 1e-4,
):
    """Screen seed-wrapped SIGS expressions, then refine the shortlist."""
    print(f"seed {seed_name}: scoring {len(blocks)} full SIGS expression blocks")
    symbols, meshes = _ch.setup_symbols_meshes(
        problem,
        points={
            "x": {"start": -10.0, "end": 10.0, "points": screen_points[0]},
            "t": {"start": 0.0, "end": 1.0, "points": screen_points[1]},
        },
    )

    candidates = []
    for block in blocks:
        candidate = _seed_wrapped_candidate(seed_code, block)
        if _max_tanh_sech_depth(candidate) > 1:
            continue
        candidates.append((candidate, block))

    raw_scores = []
    start = time.time()
    for idx, (candidate, block) in enumerate(candidates, start=1):
        loss = _score_kdv_candidate_unbiased(
            candidate, symbols, meshes, act_floor=act_floor
        )
        loss += w_complexity * _expression_complexity(candidate)
        raw_scores.append((loss, candidate, block))
        if idx % 100 == 0 or idx == 1:
            raw_scores.sort(key=lambda item: item[0])
            print(f"  [{idx}/{len(candidates)}] cheap best RMSE ~ {float(np.sqrt(raw_scores[0][0])):.3e}")
    print(f"seed {seed_name} cheap screening took {time.time() - start:.1f}s")

    raw_scores.sort(key=lambda item: item[0])
    prefilter_topk = max(3 * topk, 5)
    shortlist = raw_scores[:prefilter_topk]
    print(f"seed {seed_name}: refining top {len(shortlist)} structures")

    refined = []
    start = time.time()
    for rank, (_cheap, candidate, block) in enumerate(shortlist, start=1):
        loss, refined_expr = _refine_kdv_candidate_params(
            candidate,
            symbols,
            meshes,
            maxiter=refine_maxiter,
            act_floor=act_floor,
        )
        gen_loss = _score_multi_point_generalization(refined_expr, symbols, meshes)

        # 惩罚项：参数越少、嵌套括号越浅，惩罚越小。
        # candidate 是数值表达式，不含参数名 p，因此用 _expression_complexity 统计算子数。
        complexity = _expression_complexity(candidate)
        depth = candidate.count("(")
        penalty = w_complexity * complexity + 1e-2 * max(0, depth - 4)

        final_loss = gen_loss + penalty
        refined.append((final_loss, candidate, block, refined_expr))
        min_rmse = float(np.sqrt(max(loss, 0.0)))
        gen_rmse = float(np.sqrt(max(gen_loss, 0.0)))
        print(f"  refined [{rank}/{len(shortlist)}] min-RMSE ~ {min_rmse:.3e} gen-RMSE ~ {gen_rmse:.3e} (penalty: {penalty:.3e})")
    refined.sort(key=lambda item: item[0])
    print(f"seed {seed_name} parameter refinement & penalty took {time.time() - start:.1f}s")
    return refined[:topk]
def stage_one(
    problem: dict,
    n_samples: int,
    seed: int,
    screen_points: tuple[int, int],
    rmse_threshold: float = 3e-2,
    n_seeds: int = 5,
    widths: list[int] | None = None,
    topk: int = 3,
    act_floor: float = 1e-3,
    refine_maxiter: int = 50,
    w_complexity: float = 1e-4,
):
    """Wrap full SIGS expressions in each seed and rank TOP3 by PDE feasibility."""
    widths = list(widths or [1])
    print("=" * 70)
    print("STAGE I: full SIGS expressions wrapped by KdV seed functions (reference-free)")
    print("=" * 70)

    blocks = _collect_full_expression_blocks(widths, n_samples, seed, n_seeds)
    print(f"sampled {len(blocks)} unique full-expression blocks over {n_seeds} seeds")

    best_loss = float("inf")
    best_expr = None
    groups = []
    for name, seed_code in SEED_STRUCTURE_FUNCS:
        print(f"--- seed {name} (code {seed_code}) ---")
        top_candidates = _score_seed_wrapped(
            name,
            seed_code,
            problem,
            screen_points,
            blocks,
            topk,
            act_floor=act_floor,
            refine_maxiter=refine_maxiter,
            w_complexity=w_complexity,
        )
        members = [(item_expr, None) for _loss, item_expr, _block, _refined in top_candidates]
        refined_exprs = [refined for _loss, _item_expr, _block, refined in top_candidates]
        groups.append({
            "name": name,
            "seed_code": seed_code,
            "members": members,
            "refined": refined_exprs,
        })
        for loss, item_expr, _block, _refined in top_candidates:
            if loss < best_loss:
                best_loss = loss
                best_expr = item_expr

    print(f"full-expression best loss={best_loss:.6e}")
    if best_expr is not None:
        print("best full-expression KdV candidate:")
        print(f"  {best_expr}")
    return best_expr, None, groups




def _call_with_timeout(func, timeout):
    if hasattr(signal, "SIGALRM"):
        try:
            old_handler = signal.signal(
                signal.SIGALRM,
                lambda *_args: (_ for _ in ()).throw(TimeoutError()),
            )
        except (ValueError, OSError):
            old_handler = None
        if old_handler is not None:
            signal.alarm(int(timeout) if timeout > 0 else 1)
            try:
                return func(), None
            except TimeoutError:
                return None, "timeout"
            except Exception as exc:
                return None, f"{type(exc).__name__}: {exc}"
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
    try:
        return func(), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def _maple_coeff_equations(residual):
    """Return coefficient equations from a KdV residual in Maple's style.

    Maple uses ``coeffs(collect(KdV_equation, {t, x}, 'distributed'),
    {t, x})``.  SymPy's direct analogue is ``sp.Poly`` over ``(x, t)``.  When
    the residual is transcendental (the usual sech/tanh/Jacobi Stage-I case),
    ``sp.Poly`` cannot represent it; we then fall back to the existing
    bottom-up independent-function basis extraction and post-process the
    resulting coefficients by factoring and de-duplicating them.
    """
    x, t = sp.symbols("x t")
    try:
        poly = sp.Poly(sp.expand(residual), x, t)
        coeffs = poly.coeffs()
        basis = []
    except sp.PolynomialError:
        # Fall back to independent-function basis extraction.  Unlike
        # ``ch_common.extract_coefficients``, do not ``sp.together`` the whole
        # expression first: a global denominator can couple unrelated
        # monomials and introduce spurious zero factors.
        residual = sp.expand(residual)
        residual = _ch._reduce_tanh_powers(residual)
        residual = _ch.reduce_jacobi_powers(residual)
        residual = sp.expand(residual)
        mapping = {}
        while True:
            candidates = []
            for atom in residual.atoms(sp.Function):
                if any(arg.has(sp.Function) for arg in atom.args):
                    continue
                relevant = any(
                    x in arg.free_symbols
                    or t in arg.free_symbols
                    or any(sym in arg.free_symbols for sym in mapping.values())
                    for arg in atom.args
                )
                if relevant:
                    candidates.append(atom)
            if not candidates:
                break
            target = min(
                candidates,
                key=lambda a: (str(a.func), sp.count_ops(a), sp.srepr(a)),
            )
            if target not in mapping:
                mapping[target] = sp.Symbol(f"__B{len(mapping)}")
            residual = sp.expand(residual.subs(target, mapping[target]))

        if residual.has(x) or residual.has(t):
            raise ValueError("unable to separate x,t-dependent part")

        basis = list(mapping.values())
        if not basis:
            coeffs = [] if sp.expand(residual) == 0 else [residual]
        else:
            poly = sp.Poly(sp.expand(residual), *basis)
            coeffs = []
            for coeff in poly.coeffs():
                num, _den = sp.fraction(sp.together(coeff))
                coeffs.append(sp.expand(num))

    equations = []
    seen = set()
    for coeff in coeffs:
        coeff = sp.expand(sp.together(coeff))
        if coeff == 0:
            continue
        try:
            coeff = sp.factor_terms(coeff)
        except Exception:
            pass
        key = sp.srepr(coeff)
        if key in seen:
            continue
        seen.add(key)
        equations.append(coeff)

    equations.sort(key=lambda eq: (sp.count_ops(eq), sp.srepr(eq)))
    return equations, basis




def _probe_nonconstant_solution(expr, x, t, tol: float = 1e-6) -> bool:
    """Numerically probe whether an exact candidate actually depends on x,t."""
    free = [sym for sym in expr.free_symbols if sym not in (x, t)]
    rng = random.Random(20261116)
    points = [(0.3, 0.1), (-0.8, 1.2), (1.1, -0.4)]
    for _ in range(4):
        param_sub = {sym: rng.uniform(-1.0, 1.0) for sym in free}
        values = []
        for xv, tv in points:
            try:
                val = complex(expr.subs({x: xv, t: tv, **param_sub}).evalf())
                if np.isfinite(val.real) and np.isfinite(val.imag):
                    values.append(val)
            except Exception:
                continue
        if len(values) >= 2 and any(abs(v - values[0]) > tol for v in values[1:]):
            return True
    return False


def symbolic_stage_two(expr: str, codes: list[int], problem: dict, timeout: int = 120) -> dict:
    """Try exact KdV back-substitution with a hard per-candidate timeout."""
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
    residual = sp.diff(f, t) + 6 * f * sp.diff(f, x) + sp.diff(f, x, 3)

    def _solve_candidate():
        try:
            equations, basis = _maple_coeff_equations(residual)
        except Exception as exc:
            return {
                "status": "unsupported",
                "message": f"coefficient extraction failed ({type(exc).__name__}: {exc})",
            }

        unknowns = list(params)
        if not equations:
            if sp.expand(residual) == 0:
                if x in f.free_symbols or t in f.free_symbols:
                    return {
                        "status": "exact",
                        "exact_expr": f,
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

        try:
            solutions = sp.solve(equations, unknowns, dict=True, simplify=False)
        except Exception as exc:
            return {
                "status": "unsupported",
                "message": f"sp.solve error: {type(exc).__name__}: {exc}",
            }

        if not solutions:
            return {
                "status": "no_solution",
                "message": "sp.solve returned no solutions",
                "residual": residual,
            }

        found_nontrivial = False
        for solution in solutions:
            clean = {sym: val for sym, val in solution.items() if isinstance(sym, sp.Symbol)}
            f_sub = f.subs(clean)
            try:
                f_sub = sp.simplify(f_sub)
            except Exception:
                pass
            if x not in f_sub.free_symbols and t not in f_sub.free_symbols:
                continue
            if not _probe_nonconstant_solution(f_sub, x, t):
                continue
            found_nontrivial = True
            try:
                satisfied = all(
                    sp.expand(sp.together(eq.subs(clean))) == 0 for eq in equations
                )
            except Exception:
                satisfied = False
            if not satisfied:
                continue
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

    result, timeout_error = _call_with_timeout(_solve_candidate, timeout)
    if timeout_error == "timeout":
        return {
            "status": "timeout",
            "message": f"symbolic solve exceeded the {timeout}s timeout",
            "parameterized_expr": sym_expr,
            "residual": residual,
        }
    if timeout_error:
        return {
            "status": "unsupported",
            "message": f"symbolic solve raised {timeout_error}",
            "residual": residual,
        }
    return result




def _print_candidate_structures(groups):
    """Print Stage I candidate structures for manual verification."""
    print("=" * 70)
    print("STAGE II SKIPPED: candidate structures for manual verification")
    print("=" * 70)
    for group in groups:
        name = group["name"]
        seed_code = group["seed_code"]
        header = name if seed_code is None else f"seed {name} (first-layer code {seed_code})"
        print(f"--- {header} ---")
        refined_exprs = group.get("refined", [None] * len(group["members"]))
        for rank, (member, refined_expr) in enumerate(zip(group["members"], refined_exprs), start=1):
            expr, codes = member
            try:
                parameterized, _params = _ch.numerics_to_symbols(expr)
            except Exception as exc:
                parameterized = f"<numerics_to_symbols failed: {exc}>"
            print(f"candidate #{rank} codes={codes}")
            print(f"  numeric: {expr}")
            print(f"  parameterized: {parameterized}")
            if refined_expr:
                print(f"  refined-numeric: {refined_expr}")
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--screen-x", type=int, default=256)
    parser.add_argument("--screen-t", type=int, default=128)
    parser.add_argument("--stage2-only", action="store_true")
    parser.add_argument("--stage2", action=argparse.BooleanOptionalAction, default=True, help="run symbolic back-substitution (default on; use --no-stage2 to print candidate structures only)")
    parser.add_argument("--expr", default=None, help="initial ansatz for --stage2-only")
    parser.add_argument("--n-seeds", type=int, default=5)
    parser.add_argument("--stage1-topk", type=int, default=3)
    parser.add_argument("--stage1-act-floor", type=float, default=1e-3)
    parser.add_argument("--stage1-refine-maxiter", type=int, default=50)
    parser.add_argument("--stage1-complexity-weight", type=float, default=1e-4)
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
            act_floor=args.stage1_act_floor,
            refine_maxiter=args.stage1_refine_maxiter,
            w_complexity=args.stage1_complexity_weight,
        )

    if not args.stage2:
        _print_candidate_structures(groups)
        return

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
                if symbolic["status"] == "timeout":
                    print("    参数化候选结构:")
                    print(f"    {symbolic.get('parameterized_expr', symbolic_expr)}")

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
    print("STAGE II: no exact symbolic solution found")
    print("=" * 70)
    for message in reasons:
        print(f"  - {message}")
