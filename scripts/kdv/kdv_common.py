#!/usr/bin/env python3
"""Shared Camassa-Holm-style validation machinery for KdV NNSCA structures.

This mirrors ``scripts/ch/ch_common.py``: Stage I samples atoms from the
precomputed MathClass cluster, Stage II first attempts exact symbolic
back-substitution over seeded and top-ranked structures, and only falls back
to JAX refinement when no exact solution is found.

The KdV operator is

    u_t + 6*u*u_x + u_xxx = 0

and the reference solution is the 1-soliton u = 2 / cosh^2(x - 4t).  The
three supported templates are the validated SIGS constructions [2,3,1],
[2,2,1,1], and [2,3,2,1].
"""

from __future__ import annotations

import argparse
import random
import re
import sys
import time
from pathlib import Path

import numpy as np
import sympy as sp
import jax
import jax.numpy as jnp
import optax
from jax import grad, jit, vmap

from sigs.sampler import FlexibleVectorSampler
from sigs.utils import ExpressionUtils, MathClass

REPO_ROOT = Path(__file__).resolve().parents[2]
CH_DIR = REPO_ROOT / "scripts" / "ch"
if str(CH_DIR) not in sys.path:
    sys.path.insert(0, str(CH_DIR))

import ch_common as _ch

jax.config.update("jax_enable_x64", True)

FUNCS = _ch.FUNCS
ACT_NAMES = _ch.ACT_NAMES
NAME_CODES = _ch.NAME_CODES
SQ_CODES = _ch.SQ_CODES
FUNC_RE = _ch.FUNC_RE
SEED_FUNCTION_ATOMS = _ch.SEED_FUNCTION_ATOMS

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
    ("abs", 14),
]

# Inner-layer atom pool used by the fixed-outer SIGS stage-one search.  The
# cluster file only carries sin/cos/exp/tanh/sqrt, so these smooth travelling-wave
# atoms make the closed seed families reachable as inner activations.
INNER_SEED_FUNCTION_ATOMS = [
    "sech(x + t)", "sech(x - t)",
    "sech(x + t)**2", "sech(x - t)**2",
    "tanh(x + t)", "tanh(x - t)",
    "tanh(x + t)**2", "tanh(x - t)**2",
    "exp(x + t)", "exp(x - t)",
    "cosh(x + t)", "cosh(x - t)",
    "sinh(x + t)", "sinh(x - t)",
    "abs(x + t)", "abs(x - t)",
    "JacobiCN(x + t, 0.5)", "JacobiCN(x - t, 0.5)",
]

TEMPLATES = {
    "231": {"n_roles": 3, "first": 3, "second": 0},
    "2211": {"n_roles": 3, "first": 2, "second": 1},
    "2321": {"n_roles": 5, "first": 3, "second": 2},
}

# A minimal one-term sech^2 ansatz avoids the over-parameterized NNSCA lift
# that SymPy's solver otherwise reduces only to trivial branches.
DIRECT_STRUCTURES = [
    ("0.000000 + 2.000000*sech(1.000000*x + 1.000000*t + 0.000000)**2", [16]),
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


def _score_kdv_candidate(expr_str, symbols, meshes, u0_fn, ic_weight=1.0):
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


def lift_to_nnsca(codes: list[int], template: str) -> str:
    """Expand activation codes into the numeric NNSCA trial function."""
    codes = list(codes)
    spec = TEMPLATES[template]
    n_roles = spec["n_roles"]
    while len(codes) < n_roles:
        codes.append(0)
    codes = codes[:n_roles]

    if template == "231":
        terms = []
        for j in range(3):
            arg = "1.000000*x + 1.000000*t + 0.000000"
            terms.append(f"1.000000*({_ch.activation_str(codes[j], arg)})")
        return "0.000000 + " + " + ".join(terms)

    if template == "2211":
        first_layer = []
        for j in range(2):
            arg = "1.000000*x + 1.000000*t + 0.000000"
            first_layer.append(_ch.activation_str(codes[j], arg))
        layer2_arg = f"1.000000*({first_layer[0]}) + 1.000000*({first_layer[1]})"
        g = _ch.activation_str(codes[2], layer2_arg)
        return f"0.000000 + 1.000000*({g})"

    if template == "2321":
        first_layers = []
        for _k in range(2):
            first_layer = []
            for j in range(3):
                arg = "1.000000*x + 1.000000*t + 0.000000"
                first_layer.append(_ch.activation_str(codes[j], arg))
            first_layers.append(first_layer)

        second_layer = []
        for k in range(2):
            weighted = [f"1.000000*({first_layers[k][j]})" for j in range(3)]
            second_layer.append(_ch.activation_str(codes[3 + k], " + ".join(weighted)))

        output_terms = [f"1.000000*({second_layer[k]})" for k in range(2)]
        return "0.000000 + " + " + ".join(output_terms)

    raise ValueError(f"unknown KdV template: {template}")


def nnsca_parametrized(codes: list[int], template: str):
    """Return the named-parameter form used by Stage II optimization."""
    codes = list(codes)
    spec = TEMPLATES[template]
    n_roles = spec["n_roles"]
    while len(codes) < n_roles:
        codes.append(0)
    codes = codes[:n_roles]

    names = []
    values = []
    weight_index = 0

    def add(name, value):
        names.append(name)
        values.append(value)

    if template == "231":
        terms = []
        for j in range(3):
            wx = f"wx{j}"
            wt = f"wt{j}"
            bias = f"b{j}"
            add(wx, _ch._init_weight(weight_index))
            weight_index += 1
            add(wt, _ch._init_weight(weight_index))
            weight_index += 1
            add(bias, 0.0)
            arg = f"{wx}*x + {wt}*t + {bias}"
            name = f"a{j}"
            add(name, _ch._init_weight(weight_index))
            weight_index += 1
            terms.append(f"{name}*({_ch.activation_str(codes[j], arg)})")
        add("b_out", 0.0)
        expr = "b_out + " + " + ".join(terms)
        return expr, jnp.asarray(values, dtype=jnp.float64), names

    if template == "2211":
        first_layer = []
        for j in range(2):
            wx = f"wx{j}"
            wt = f"wt{j}"
            bias = f"b{j}"
            add(wx, _ch._init_weight(weight_index))
            weight_index += 1
            add(wt, _ch._init_weight(weight_index))
            weight_index += 1
            add(bias, 0.0)
            arg = f"{wx}*x + {wt}*t + {bias}"
            first_layer.append(_ch.activation_str(codes[j], arg))
        weighted = []
        for j in range(2):
            name = f"v{j}"
            add(name, _ch._init_weight(weight_index))
            weight_index += 1
            weighted.append(f"{name}*({first_layer[j]})")
        g = _ch.activation_str(codes[2], " + ".join(weighted))
        add("b_out", 0.0)
        add("a0", _ch._init_weight(weight_index))
        weight_index += 1
        expr = f"b_out + a0*({g})"
        return expr, jnp.asarray(values, dtype=jnp.float64), names

    if template == "2321":
        first_layers = []
        for k in range(2):
            first_layer = []
            for j in range(3):
                wx = f"wx{k}{j}"
                wt = f"wt{k}{j}"
                bias = f"b{k}{j}"
                add(wx, _ch._init_weight(weight_index))
                weight_index += 1
                add(wt, _ch._init_weight(weight_index))
                weight_index += 1
                add(bias, 0.0)
                arg = f"{wx}*x + {wt}*t + {bias}"
                first_layer.append(_ch.activation_str(codes[j], arg))
            first_layers.append(first_layer)

        second_layer = []
        for k in range(2):
            weighted = []
            for j in range(3):
                name = f"v{k}{j}"
                add(name, _ch._init_weight(weight_index))
                weight_index += 1
                weighted.append(f"{name}*({first_layers[k][j]})")
            second_layer.append(_ch.activation_str(codes[3 + k], " + ".join(weighted)))

        add("b_out", 0.0)
        output_terms = []
        for k in range(2):
            name = f"a{k}"
            add(name, _ch._init_weight(weight_index))
            weight_index += 1
            output_terms.append(f"{name}*({second_layer[k]})")
        expr = "b_out + " + " + ".join(output_terms)
        return expr, jnp.asarray(values, dtype=jnp.float64), names

    raise ValueError(f"unknown KdV template: {template}")


def seed_structure_candidates(template: str):
    """Deterministic single-activation-layer structures for the template."""
    spec = TEMPLATES[template]
    n_roles = spec["n_roles"]
    first = spec["first"]
    second = spec["second"]
    candidates = []
    seen = set()

    for expr, codes in DIRECT_STRUCTURES:
        codes = list(codes)
        while len(codes) < n_roles:
            codes.append(0)
        codes = codes[:n_roles]
        seen.add(tuple(codes))
        candidates.append((expr, codes))

    def add(codes):
        codes = list(codes)
        while len(codes) < n_roles:
            codes.append(0)
        codes = codes[:n_roles]
        key = tuple(codes)
        if key in seen:
            return
        seen.add(key)
        candidates.append((lift_to_nnsca(codes, template), list(codes)))

    for _name, code in SEED_STRUCTURE_FUNCS:
        add([code] * first)
    if second:
        for _name, code in SEED_STRUCTURE_FUNCS:
            add([0] * first + [code] * second)
    return candidates


def stage_one_seed(
    template: str,
    problem: dict,
    n_samples: int,
    seed: int,
    screen_points: tuple[int, int],
    rmse_threshold: float,
    topk: int = 1,
):
    n_roles = TEMPLATES[template]["n_roles"]
    sampler = FlexibleVectorSampler(
        cluster_file=str(REPO_ROOT / "data" / "clusters.pkl"), device="cpu"
    )
    sample_id = sampler.sample_from_subclusters(
        categories={MathClass.SPATIOTEMPORAL_2D: n_roles},
        n_samples=max(n_samples * n_roles, n_roles),
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
    atoms = list(base_exprs)
    atoms.extend(SEED_FUNCTION_ATOMS * max(1, n_roles))
    rng.shuffle(atoms)

    seeded = seed_structure_candidates(template)
    candidates = [expr for expr, _codes in seeded]
    codes_list = [codes for _expr, codes in seeded]
    for start in range(0, len(atoms) - n_roles + 1, n_roles):
        role_atoms = atoms[start : start + n_roles]
        if len(role_atoms) < n_roles:
            break
        codes = [_ch.activation_code_from_atom(a) for a in role_atoms]
        candidates.append(lift_to_nnsca(codes, template))
        codes_list.append(codes)

    print(f"seeded {len(SEED_FUNCTION_ATOMS)} extra function atoms + {len(seeded)} exact-capable structures")
    print(f"assigned {len(candidates)} {n_roles}-role candidates")
    print(f"scoring {len(candidates)} KdV NNSCA candidates")

    symbols, meshes = _ch.setup_symbols_meshes(
        problem,
        points={
            "x": {"start": -10.0, "end": 10.0, "points": screen_points[0]},
            "t": {"start": 0.0, "end": 1.0, "points": screen_points[1]},
        },
    )
    u0_fn = _ch.make_numpy_x_fn(_ch.ic_rhs(problem))

    best_expr = None
    best_codes = None
    best_loss = float("inf")
    top_candidates = []
    start = time.time()
    for idx, expr in enumerate(candidates):
        loss = _score_kdv_candidate(expr, symbols, meshes, u0_fn)
        top_candidates.append((loss, expr, codes_list[idx]))
        top_candidates.sort(key=lambda item: item[0])
        if len(top_candidates) > topk:
            top_candidates = top_candidates[:topk]
        if loss < best_loss:
            best_loss = loss
            best_expr = expr
            best_codes = codes_list[idx]
        if (idx + 1) % 100 == 0 or idx == 0:
            print(f"  [{idx + 1}/{len(candidates)}] best RMSE ~ {float(np.sqrt(best_loss)):.3e}")
        if np.isfinite(best_loss) and float(np.sqrt(best_loss)) < rmse_threshold:
            print(f"  early stop at candidate {idx + 1}")
            break

    print(f"screening took {time.time() - start:.1f}s")
    print("best structural KdV NNSCA expr:")
    print(f"  {best_expr}")
    return best_loss, best_expr, best_codes, top_candidates


def stage_one(
    template: str,
    problem: dict,
    n_samples: int,
    seed: int,
    screen_points: tuple[int, int],
    rmse_threshold: float = 3e-2,
    n_seeds: int = 5,
    topk: int = 1,
):
    print("=" * 70)
    print("STAGE I: MathClass cluster sampling + symbolic KdV screening (multi-seed)")
    print("=" * 70)

    best_loss = float("inf")
    best_expr = None
    best_codes = None
    all_candidates = []
    for i in range(n_seeds):
        run_seed = seed + i
        print(f"--- seed {run_seed} ({i + 1}/{n_seeds}) ---")
        loss, expr, codes, seed_top = stage_one_seed(
            template,
            problem,
            n_samples,
            run_seed,
            screen_points,
            rmse_threshold,
            topk=topk,
        )
        print(f"seed {run_seed} best loss={loss:.6e}")
        all_candidates.extend(seed_top)
        if loss < best_loss:
            best_loss = loss
            best_expr = expr
            best_codes = codes

    deduped = {}
    for loss, expr, codes in all_candidates:
        key = tuple(codes)
        if key not in deduped or loss < deduped[key][0]:
            deduped[key] = (loss, expr, codes)
    top_candidates = sorted(deduped.values(), key=lambda item: item[0])[:topk]
    if top_candidates:
        best_loss, best_expr, best_codes = top_candidates[0]

    print(f"multi-seed best loss={best_loss:.6e}")
    print("best structural KdV NNSCA expr:")
    print(f"  {best_expr}")
    return best_expr, best_codes, top_candidates

def _sample_inner_code_blocks(template: str, n_samples: int, seed: int) -> list[tuple[int, ...]]:
    """Sample and deduplicate inner activation blocks with the SIGS stage-one sampler."""
    spec = TEMPLATES[template]
    n_inner = spec["second"]
    if n_inner <= 0:
        return []

    sampler = FlexibleVectorSampler(
        cluster_file=str(REPO_ROOT / "data" / "clusters.pkl"), device="cpu"
    )
    sample_id = sampler.sample_from_subclusters(
        categories={MathClass.SPATIOTEMPORAL_2D: n_inner},
        n_samples=max(n_samples * n_inner, n_inner),
        operator="",
        seed=seed,
        model=None,
    )
    exprs, _, _, _ = sampler.get_sampling_results(sample_id)

    filtered = ExpressionUtils.filter_by_first_const(exprs, min_val=0.5)
    if not filtered:
        filtered = [(i, e) for i, e in enumerate(exprs)]
    if filtered:
        _, base_exprs = zip(*filtered)
        base_exprs = list(base_exprs)
    else:
        base_exprs = []

    rng = random.Random(seed)
    atoms = base_exprs
    atoms.extend(INNER_SEED_FUNCTION_ATOMS * max(1, n_inner))
    rng.shuffle(atoms)

    blocks = []
    seen = set()
    for start in range(0, len(atoms) - n_inner + 1, n_inner):
        role_atoms = atoms[start : start + n_inner]
        codes = tuple(_ch.activation_code_from_atom(a) for a in role_atoms)
        if codes in seen:
            continue
        seen.add(codes)
        blocks.append(codes)
    return blocks


def _fixed_outer_inner_search(
    template: str,
    outer_code: int,
    problem: dict,
    screen_points: tuple[int, int],
    inner_blocks: list[tuple[int, ...]],
    topk: int,
):
    """Score the shared inner block pool while keeping the outer layer fixed."""
    spec = TEMPLATES[template]
    first = spec["first"]

    print(f"outer {outer_code}: scoring {len(inner_blocks)} unique inner structures")
    if not inner_blocks:
        return []

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
    for idx, block in enumerate(inner_blocks):
        codes = [outer_code] * first + list(block)
        expr = lift_to_nnsca(codes, template)
        loss = _score_kdv_candidate(expr, symbols, meshes, u0_fn)
        top_candidates.append((loss, expr, codes))
        top_candidates.sort(key=lambda item: item[0])
        if len(top_candidates) > topk:
            top_candidates = top_candidates[:topk]
        if (idx + 1) % 100 == 0 or idx == 0:
            best_rmse = float(np.sqrt(top_candidates[0][0]))
            print(f"  [{idx + 1}/{len(inner_blocks)}] best RMSE ~ {best_rmse:.3e}")

    print(f"fixed-outer {outer_code} screening took {time.time() - start:.1f}s")
    return top_candidates


def stage_one_outer_groups(
    template: str,
    problem: dict,
    n_samples: int,
    seed: int,
    screen_points: tuple[int, int],
    rmse_threshold: float = 3e-2,
    n_seeds: int = 5,
    topk: int = 5,
):
    """Build seed-function groups whose symbolic stage tries TOP5 then a linear fallback."""
    spec = TEMPLATES[template]
    first = spec["first"]
    second = spec["second"]

    if second == 0:
        expr, codes, top_candidates = stage_one(
            template,
            problem,
            n_samples,
            seed,
            screen_points,
            rmse_threshold=rmse_threshold,
            n_seeds=n_seeds,
            topk=3,
        )

        members = []
        seen = set()
        for seeded_expr, seeded_codes in seed_structure_candidates(template):
            key = tuple(seeded_codes)
            if key in seen:
                continue
            seen.add(key)
            members.append((seeded_expr, seeded_codes))
        for item in top_candidates:
            key = tuple(item[2])
            if key in seen:
                continue
            seen.add(key)
            members.append((item[1], item[2]))
        if not members:
            members = [(expr, codes)]

        groups = [{
            "name": "single-layer seeds",
            "outer_code": None,
            "members": members,
            "fallback": None,
        }]
        return expr, codes, groups

    print("=" * 70)
    print("STAGE I: fixed-outer SIGS stage-one inner search")
    print("=" * 70)

    best_loss = float("inf")
    best_expr = None
    best_codes = None
    groups = []

    inner_blocks = []
    seen_blocks = set()
    for i in range(n_seeds):
        blocks = _sample_inner_code_blocks(template, n_samples, seed + i)
        for block in blocks:
            if block in seen_blocks:
                continue
            seen_blocks.add(block)
            inner_blocks.append(block)
    print(f"sampled {len(inner_blocks)} unique inner structures over {n_seeds} seeds")

    for name, outer_code in SEED_STRUCTURE_FUNCS:
        print(f"--- fixed outer {name} (code {outer_code}) ---")
        top_candidates = _fixed_outer_inner_search(
            template,
            outer_code,
            problem,
            screen_points,
            inner_blocks,
            topk,
        )

        members = [(item_expr, item_codes) for _loss, item_expr, item_codes in top_candidates]
        fallback_codes = [outer_code] * first + [0] * second
        fallback_expr = lift_to_nnsca(fallback_codes, template)
        member_codes = {tuple(item_codes) for _item_expr, item_codes in members}
        fallback = None if tuple(fallback_codes) in member_codes else (fallback_expr, fallback_codes)
        groups.append({
            "name": name,
            "outer_code": outer_code,
            "members": members,
            "fallback": fallback,
        })

        for loss, item_expr, item_codes in top_candidates:
            if loss < best_loss:
                best_loss = loss
                best_expr = item_expr
                best_codes = item_codes

    print(f"fixed-outer best loss={best_loss:.6e}")
    if best_expr is None and groups:
        fallback_expr, fallback_codes = groups[0]["fallback"]
        best_expr, best_codes = fallback_expr, fallback_codes
    print("best fixed-outer KdV expr:")
    print(f"  {best_expr}")
    return best_expr, best_codes, groups


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
        simplified = sp.simplify(residual)
        if simplified == 0:
            f_sub = sp.simplify(f)
            if x in f_sub.free_symbols or t in f_sub.free_symbols:
                return {
                    "status": "exact",
                    "exact_expr": f_sub,
                    "constraints": {},
                    "residual": simplified,
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
        clean = {sym: val for sym, val in solution.items() if isinstance(sym, sp.Symbol)}
        try:
            f_sub = sp.simplify(f.subs(clean))
        except Exception:
            continue
        if x not in f_sub.free_symbols and t not in f_sub.free_symbols:
            continue
        found_nontrivial = True
        verified = residual.subs(clean) == 0
        if not verified:
            try:
                verified = all(
                    sp.simplify(sp.expand(eq.subs(clean))) == 0 for eq in equations
                )
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
    template: str = "2321",
):
    print("=" * 70)
    print("STAGE II: JAX autodiff parameter refinement")
    print("=" * 70)

    if codes is not None:
        param_expr, init_params, names = nnsca_parametrized(codes, template)
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
        return u_t(x, t, params) + 6.0 * u(x, t, params) * u_x(x, t, params) + u_xxx(x, t, params)

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
            print(f"  iter {step:5d}  loss={loss:.3e}  rmse={rmse:.3e}  relL2={rel_l2:.3e}")

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
        jnp.mean(vmap(lambda x, t: res(x, t, best_params), (0, 0))(xflat, tflat) ** 2)
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
    parser.add_argument("--inner-topk", type=int, default=5)
    return parser


def main(template: str):
    args = build_parser().parse_args()
    problem = create_kdv_problem()
    print(f"operator: {problem['operators']}")
    print(f"true solution: {problem['true_solution']}")

    if args.stage2_only:
        expr = args.expr or "2.0*cosh(1.1*(x - 3.5*t))**(-2)"
        codes = None
        groups = [{
            "name": "stage2-only",
            "outer_code": None,
            "members": [(expr, codes)],
            "fallback": None,
        }]
    else:
        expr, codes, groups = stage_one_outer_groups(
            template,
            problem,
            args.n_samples,
            args.seed,
            (args.screen_x, args.screen_t),
            n_seeds=args.n_seeds,
            topk=args.inner_topk,
        )

    print("=" * 70)
    print("STAGE II: symbolic back-substitution over top structures")
    print("=" * 70)

    reasons = []
    exact_solutions = []
    for group in groups:
        group_name = group["name"]
        outer_code = group["outer_code"]
        if outer_code is None:
            header = group_name
        else:
            header = f"seed {group_name} (outer code {outer_code})"
        print(f"--- {header} ---")

        group_reasons = []
        group_has_exact = False
        for rank, (symbolic_expr, symbolic_codes) in enumerate(group["members"], start=1):
            symbolic = symbolic_stage_two(symbolic_expr, symbolic_codes, problem)
            if symbolic["status"] == "exact":
                group_has_exact = True
                exact_solutions.append((header, rank, symbolic_codes, symbolic))
                print(f"  candidate #{rank} (codes={symbolic_codes}) exact; collected")
            else:
                message = f"{header} #{rank}: {symbolic['message']}"
                group_reasons.append(message)
                print(f"  candidate #{rank} not exact: {symbolic['message']}")

        if not group_has_exact and group["fallback"] is not None:
            fallback_expr, fallback_codes = group["fallback"]
            symbolic = symbolic_stage_two(fallback_expr, fallback_codes, problem)
            if symbolic["status"] == "exact":
                exact_solutions.append((header, "linear fallback", fallback_codes, symbolic))
                print(f"  linear fallback (codes={fallback_codes}) exact; collected")
            else:
                message = f"{header} linear fallback: {symbolic['message']}"
                group_reasons.append(message)
                print(f"  linear fallback not exact: {symbolic['message']}")

        reasons.extend(group_reasons)

    if exact_solutions:
        print("=" * 70)
        print(f"最终得到的精确解：{len(exact_solutions)} 个")
        print("=" * 70)
        for idx, (header, label, solution_codes, solution) in enumerate(exact_solutions, start=1):
            print(f"[{idx}/{len(exact_solutions)}] 来源：{header} / {label}，codes={solution_codes}")
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

    stage_two(
        problem,
        expr,
        args.lr,
        args.iters,
        args.w_ic,
        args.rmse_threshold,
        args.rel_l2_threshold,
        codes,
        template,
    )
    print(f"数值近似解（符号求解失败：{' | '.join(reasons)}）")
