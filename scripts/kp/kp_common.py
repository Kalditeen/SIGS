#!/usr/bin/env python3
"""Shared Kadomtsev-Petviashvili II validation machinery for NNSCA structures.

The Kadomtsev-Petviashvili II (KP-II) equation used here is

    (u_t + 4*u*u_x + u_xxx)_x + u_yy = 0

and the reference solution is the line soliton

    u(x, y, t) = 3 * sech(x + y - 5*t)**2

Each structure file supplies its hidden-layer widths, for example [2, 3] for
the two-hidden-layer [2,2,3,1] network.
"""

from __future__ import annotations

import argparse
import random
import re
import signal
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
from sigs.jacobi import (
    JacobiSN,
    JacobiCN,
    JacobiDN,
    NUMPY_MODULES,
    SYMPY_LOCALS,
    jax_sn,
    jax_cn,
    jax_dn,
    reduce_jacobi_powers,
)

jax.config.update("jax_enable_x64", True)

FUNCS = ["sin", "cos", "tan", "exp", "log", "sqrt", "tanh", "sinh", "cosh", "abs"]

REPO_ROOT = Path(__file__).resolve().parents[2]

ACT_NAMES = {
    0: "identity",
    1: "tanh",
    2: "tanh2",
    3: "sinh",
    4: "sinh2",
    5: "cosh",
    6: "cosh2",
    7: "exp",
    8: "sin",
    9: "sin2",
    10: "cos",
    11: "cos2",
    12: "log",
    13: "sqrt",
    14: "abs",
    15: "sech",
    16: "sech2",
    17: "tan",
    18: "tan2",
    19: "JacobiCN",
}
NAME_CODES = {v: k for k, v in ACT_NAMES.items()}
SQ_CODES = {"tanh": 2, "sinh": 4, "cosh": 6, "sin": 9, "cos": 11, "sech": 16, "tan": 18}
FUNC_RE = re.compile(r"\b(sin|cos|tan|exp|log|sqrt|tanh|sinh|cosh|sech|abs|JacobiSN|JacobiCN|JacobiDN)\s*\(")

# Extra smooth atoms injected into the Stage-I pool.  The precomputed cluster file
# only contains sin/cos/exp/tanh/sqrt, so hyperbolic secant/cosh/sinh candidates
# (which include the exact KP-II line soliton u = 3*sech^2(linear))
# could never be sampled without these seeds.
SEED_FUNCTION_ATOMS = [
    "sech(x + y + t)", "sech(x - y + t)",
    "cosh(x + y + t)", "cosh(x - y + t)",
    "sinh(x + y + t)", "sinh(x - y + t)",
    "abs(x + y + t)", "abs(x - y + t)",
    "JacobiCN(x + y + t, 0.5)", "JacobiCN(x - y + t, 0.5)",
]

# Ordering only affects how many structures symbolic_stage_two tries before
# finding its first exact solution, not whether an exact solution is eventually
# found: main walks the whole list until one succeeds or every entry fails.
# The order therefore ranks candidates by how commonly the activation appears
# in exact solution families of shallow-water equations in general (KdV, CH, KP,
# Boussinesq, eKdV, fKdV, ...), not by the known answer of any one equation.
#
# Ranking criteria, highest priority first:
# 1. Algebraic closure: derivatives stay inside the same small function family,
#    which keeps the symbolic coefficient system small and easier to solve.
# 2. Literature frequency among shallow-water exact solutions.
# 3. Symbolic feasibility: abs() is rejected immediately by symbolic_stage_two,
#    and JacobiCN has expensive symbolic derivatives/expansions.
# 4. Generality: the same order stays sensible for KdV, CH, KP, Boussinesq, ...
#
# abs() is placed last because symbolic_stage_two returns unsupported for it;
# its position here does not change the final result.
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




def create_kp_problem() -> dict:
    x, y, t = sp.symbols("x y t")
    # Exact KP-II line soliton for (u_t + 4*u*u_x + u_xxx)_x + u_yy = 0.
    u_true = 3 * sp.sech(x + y - 5 * t) ** 2
    u0 = sp.simplify(u_true.subs(t, 0.0))

    return {
        "problem_type": "KP2-1Soliton-2D",
        "operators": "(ut + 4*u*ux + uxxx)_x + uyy",
        "F": "0",
        "initial_condition": [f"u(x, y, t=0) = {u0}"],
        "boundary_conditions": [],
        "mesh": {
            "x": {"start": -10.0, "end": 10.0, "points": 256},
            "y": {"start": -10.0, "end": 10.0, "points": 256},
            "t": {"start": 0.0, "end": 1.0, "points": 128},
        },
        "parameters": {},
        "true_solution": str(sp.simplify(u_true)),
    }


def ic_rhs(problem: dict) -> str:
    cond = problem["initial_condition"][0]
    return cond.rsplit("=", 1)[1].strip()


def setup_symbols_meshes(problem: dict, points: dict | None = None):
    x, y, t = sp.symbols("x y t")
    px = (points or problem["mesh"])["x"]["points"]
    py = (points or problem["mesh"])["y"]["points"]
    pt = (points or problem["mesh"])["t"]["points"]
    xs = np.linspace(
        problem["mesh"]["x"]["start"], problem["mesh"]["x"]["end"], px
    )
    ys = np.linspace(
        problem["mesh"]["y"]["start"], problem["mesh"]["y"]["end"], py
    )
    ts = np.linspace(
        problem["mesh"]["t"]["start"], problem["mesh"]["t"]["end"], pt
    )
    X, Y, T = np.meshgrid(xs, ys, ts, indexing="ij")
    return {"x": x, "y": y, "t": t}, [X, Y, T]


def make_u_fn(expr_str: str):
    expr = ExpressionUtils.standardize_expression(expr_str).replace("Abs(", "abs(")

    def fn(x, y, t):
        ctx = {"x": x, "y": y, "t": t}
        for f in FUNCS:
            ctx[f] = getattr(jnp, f)
        ctx["pi"] = jnp.pi
        ctx["e"] = jnp.e
        ctx["sech"] = lambda z: 1 / jnp.cosh(z)
        ctx["JacobiSN"] = jax_sn
        ctx["JacobiCN"] = jax_cn
        ctx["JacobiDN"] = jax_dn
        return eval(expr, {"__builtins__": {}}, ctx)

    return fn


def make_xy_fn(expr_str: str):
    expr = ExpressionUtils.standardize_expression(expr_str).replace("Abs(", "abs(")

    def fn(x, y):
        ctx = {"x": x, "y": y}
        for f in FUNCS:
            ctx[f] = getattr(jnp, f)
        ctx["pi"] = jnp.pi
        ctx["e"] = jnp.e
        ctx["sech"] = lambda z: 1 / jnp.cosh(z)
        ctx["JacobiSN"] = jax_sn
        ctx["JacobiCN"] = jax_cn
        ctx["JacobiDN"] = jax_dn
        return eval(expr, {"__builtins__": {}}, ctx)

    return fn


def make_numpy_xy_fn(expr_str: str):
    x, y = sp.symbols("x y")
    expr = sp.sympify(ExpressionUtils.standardize_expression(expr_str))
    return sp.lambdify((x, y), expr, modules="numpy")


def _quiet_eval(fn, *args):
    with np.errstate(all="ignore"):
        return fn(*args)


def score_candidate(expr_str: str, symbols, meshes, u0_fn, ic_weight: float = 1.0):
    """Rank one ansatz with a robust Stage-I KP-II residual plus IC score."""
    x, y, t = symbols["x"], symbols["y"], symbols["t"]
    X, Y, T = meshes

    try:
        u = sp.sympify(ExpressionUtils.standardize_expression(expr_str), locals=SYMPY_LOCALS)
        residual = (
            sp.diff(u, x, t)
            + 4.0 * sp.diff(u, x) ** 2
            + 4.0 * u * sp.diff(u, x, 2)
            + sp.diff(u, x, 4)
            + sp.diff(u, y, 2)
        )

        def to_real(vals):
            vals = np.asarray(vals)
            if np.iscomplexobj(vals):
                vals = np.real(vals)
            return np.nan_to_num(
                np.asarray(vals, dtype=np.float64),
                nan=1e3, posinf=1e3, neginf=-1e3,
            )

        rv = to_real(_quiet_eval(sp.lambdify((x, y, t), residual, modules=NUMPY_MODULES), X, Y, T))
        pde_mse = float(np.mean(rv**2))
        max_res = float(np.max(np.abs(rv)))

        ic_fn = sp.lambdify((x, y), u.subs(t, 0.0), modules=NUMPY_MODULES)
        ic_pred = np.asarray(_quiet_eval(ic_fn, X[:, :, 0], Y[:, :, 0]))
        ic_true = np.asarray(_quiet_eval(u0_fn, X[:, :, 0], Y[:, :, 0]))
        ic_mse = float(np.mean((ic_pred - ic_true) ** 2))

        u_vals = to_real(_quiet_eval(sp.lambdify((x, y, t), u, modules=NUMPY_MODULES), X, Y, T))
        u_range = float(np.max(np.abs(u_vals)))

        ux_vals = to_real(_quiet_eval(sp.lambdify((x, y, t), sp.diff(u, x), modules=NUMPY_MODULES), X, Y, T))
        uy_vals = to_real(_quiet_eval(sp.lambdify((x, y, t), sp.diff(u, y), modules=NUMPY_MODULES), X, Y, T))
        ut_vals = to_real(_quiet_eval(sp.lambdify((x, y, t), sp.diff(u, t), modules=NUMPY_MODULES), X, Y, T))
        grad_norm = float(np.mean(np.sqrt(ux_vals**2 + uy_vals**2 + ut_vals**2)))

        return (
            pde_mse
            + ic_weight * ic_mse
            + 0.01 * max_res
            + 1e-4 * grad_norm
            + 0.1 * max(0.0, u_range - 10.0)
        )
    except Exception:
        return float("inf")


def extract_function_tokens(expr: str) -> list[tuple[str, bool]]:
    std = ExpressionUtils.standardize_expression(expr)
    tokens = []
    for match in FUNC_RE.finditer(std):
        name = match.group(1)
        open_idx = match.end() - 1
        depth = 1
        j = open_idx + 1
        while j < len(std) and depth:
            if std[j] == "(":
                depth += 1
            elif std[j] == ")":
                depth -= 1
            j += 1
        squared = bool(re.match(r"\s*\*\*\s*2", std[j:]))
        tokens.append((name, squared))
    return tokens


def structures_from_expr(expr: str) -> list[tuple[int, int, int]]:
    structures = []
    seen = set()
    for name, squared in extract_function_tokens(expr):
        base = NAME_CODES.get(name)
        if base is None:
            continue
        if squared:
            sq = SQ_CODES.get(name)
            if sq is None:
                continue
            triple = (base, sq, 0)
        else:
            sq = SQ_CODES.get(name)
            triple = (base, sq, 0) if sq is not None else (base, 0, 0)
        if triple not in seen:
            seen.add(triple)
            structures.append(triple)
    return structures or [(0, 0, 0)]


def activation_code_from_atom(expr: str) -> int:
    return structures_from_expr(expr)[0][0]


def activation_str(code: int, arg: str) -> str:
    code = int(code)
    if code == 0:
        return f"({arg})"
    if code == 1:
        return f"tanh({arg})"
    if code == 2:
        return f"tanh({arg})**2"
    if code == 3:
        return f"sinh({arg})"
    if code == 4:
        return f"sinh({arg})**2"
    if code == 5:
        return f"cosh({arg})"
    if code == 6:
        return f"cosh({arg})**2"
    if code == 7:
        return f"exp({arg})"
    if code == 8:
        return f"sin({arg})"
    if code == 9:
        return f"sin({arg})**2"
    if code == 10:
        return f"cos({arg})"
    if code == 11:
        return f"cos({arg})**2"
    if code == 12:
        return f"log(abs({arg}) + 1e-12)"
    if code == 13:
        return f"sqrt(abs({arg}))"
    if code == 14:
        return f"abs({arg})"
    if code == 15:
        return f"sech({arg})"
    if code == 16:
        return f"sech({arg})**2"
    if code == 17:
        return f"tan({arg})"
    if code == 18:
        return f"tan({arg})**2"
    if code == 19:
        return f"JacobiCN({arg}, 0.500000)"
    raise ValueError(f"unknown activation code: {code}")


def _init_weight(index: int) -> float:
    return 1.0 + 0.05 * index


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
    for l, w in enumerate(widths):
        cur = []
        for j in range(w):
            code = codes[offset]
            offset += 1
            if l == 0:
                arg = "1.000000*x + 1.000000*y + 1.000000*t + 0.000000"
            else:
                terms = [
                    f"1.000000*({layers[-1][p]})"
                    for p in range(len(layers[-1]))
                ]
                arg = " + ".join(terms) + " + 0.000000"
            cur.append(activation_str(code, arg))
        layers.append(cur)

    out = [
        f"1.000000*({layers[-1][j]})"
        for j in range(len(layers[-1]))
    ]
    return "0.000000 + " + " + ".join(out)


def seed_structure_candidates(widths: list[int]):
    """Guaranteed single-activation-layer structures covering smooth exact waves.

    A single hidden layer (either the first one with identity on the rest, or
    the second one with identity before it) is enough to represent
    u = A*sech^2(p*x + q*y + c*t + d), the elementary exact KP-II family.
    """
    n_roles = sum(widths)
    layer_sizes = list(widths)
    first = layer_sizes[0]
    candidates = []
    seen = set()

    def add(codes: list[int]):
        codes = _pad_codes(codes, n_roles)
        key = tuple(codes)
        if key in seen:
            return
        seen.add(key)
        candidates.append((lift_to_nnsca(codes, widths), list(codes)))

    for _name, code in SEED_STRUCTURE_FUNCS:
        add([code] * first)
    if len(layer_sizes) >= 2:
        prefix = layer_sizes[0]
        for _name, code in SEED_STRUCTURE_FUNCS:
            add([0] * prefix + [code] * layer_sizes[1])
    return candidates


def nnsca_parametrized(codes: list[int], widths: list[int]):
    """Return the named-parameter form used by Stage II optimization."""
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
    for l, w in enumerate(widths):
        cur = []
        for j in range(w):
            code = codes[offset]
            offset += 1
            if l == 0:
                wx = f"wx{j}"
                wy = f"wy{j}"
                wt = f"wt{j}"
                bias = f"b0{j}"
                add(wx, _init_weight(weight_index))
                weight_index += 1
                add(wy, _init_weight(weight_index))
                weight_index += 1
                add(wt, _init_weight(weight_index))
                weight_index += 1
                add(bias, 0.0)
                arg = f"{wx}*x + {wy}*y + {wt}*t + {bias}"
            else:
                terms = []
                for p in range(len(layers[-1])):
                    name = f"w{l}{j}{p}"
                    add(name, _init_weight(weight_index))
                    weight_index += 1
                    terms.append(f"{name}*({layers[-1][p]})")
                bias = f"b{l}{j}"
                add(bias, 0.0)
                arg = " + ".join(terms) + f" + {bias}"
            cur.append(activation_str(code, arg))
        layers.append(cur)

    out = []
    for j in range(len(layers[-1])):
        name = f"a{j}"
        add(name, _init_weight(weight_index))
        weight_index += 1
        out.append(f"{name}*({layers[-1][j]})")
    add("b_out", 0.0)
    expr = "b_out + " + " + ".join(out)
    return expr, jnp.asarray(values, dtype=jnp.float64), names


def stage_one_seed(
    problem: dict,
    n_samples: int,
    seed: int,
    screen_points: tuple[int, int, int],
    rmse_threshold: float,
    widths: list[int],
    topk: int = 1,
):
    n_roles = sum(widths)
    sampler = FlexibleVectorSampler(
        cluster_file=str(REPO_ROOT / "data" / "clusters.pkl"), device="cpu"
    )
    sample_id = sampler.sample_from_subclusters(
        categories={MathClass.SPATIOTEMPORAL_3D: n_roles},
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
    # Repeat the seed atoms a few times so random role blocks can pick them up.
    atoms.extend(SEED_FUNCTION_ATOMS * max(1, n_roles))
    rng.shuffle(atoms)

    seeded = seed_structure_candidates(widths)
    candidates = [expr for expr, _codes in seeded]
    codes_list = [codes for _expr, codes in seeded]
    for start in range(0, len(atoms) - n_roles + 1, n_roles):
        role_atoms = atoms[start:start + n_roles]
        if len(role_atoms) < n_roles:
            break
        codes = [activation_code_from_atom(a) for a in role_atoms]
        candidates.append(lift_to_nnsca(codes, widths))
        codes_list.append(codes)

    print(f"seeded {len(SEED_FUNCTION_ATOMS)} extra function atoms + {len(seeded)} exact-capable structures")
    print(f"assigned {len(candidates)} {n_roles}-role candidates")
    print(f"scoring {len(candidates)} NNSCA candidates")

    symbols, meshes = setup_symbols_meshes(
        problem,
        points={
            "x": {"start": -10.0, "end": 10.0, "points": screen_points[0]},
            "y": {"start": -10.0, "end": 10.0, "points": screen_points[1]},
            "t": {"start": 0.0, "end": 1.0, "points": screen_points[2]},
        },
    )
    u0_fn = make_numpy_xy_fn(ic_rhs(problem))

    best_expr = None
    best_codes = None
    best_loss = float("inf")
    top_candidates = []
    start = time.time()
    for idx, expr in enumerate(candidates):
        loss = score_candidate(expr, symbols, meshes, u0_fn)
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
    print("best structural KP-II NNSCA expr:")
    print(f"  {best_expr}")
    return best_loss, best_expr, best_codes, top_candidates


def stage_one(
    problem: dict,
    n_samples: int,
    seed: int,
    screen_points: tuple[int, int, int],
    rmse_threshold: float = 3e-2,
    n_seeds: int = 5,
    widths: list[int] | None = None,
    topk: int = 1,
):
    widths = widths or [3]
    print("=" * 70)
    print("STAGE I: MathClass cluster sampling + symbolic KP-II screening (multi-seed)")
    print("=" * 70)

    best_loss = float("inf")
    best_expr = None
    best_codes = None
    all_candidates = []
    for i in range(n_seeds):
        run_seed = seed + i
        print(f"--- seed {run_seed} ({i + 1}/{n_seeds}) ---")
        loss, expr, codes, seed_top = stage_one_seed(
            problem, n_samples, run_seed, screen_points, rmse_threshold, widths, topk=topk
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
    print("best structural KP-II NNSCA expr:")
    print(f"  {best_expr}")
    return best_expr, best_codes, top_candidates


def parse_params(expr: str):
    result_expr = expr.replace("^", "**")
    pattern = r"(?<![a-zA-Z0-9_.])([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)(?![a-zA-Z0-9_.])"
    matches = []
    for match in re.finditer(pattern, result_expr):
        val = float(match.group(1))
        start, end = match.span()
        if abs(val - 3.14159265359) < 1e-10 or abs(val - 2.71828182846) < 1e-10:
            continue
        if start >= 2 and result_expr[start - 2:start] == "**":
            continue
        if val in [2.0, 3.0, 4.0, 5.0, 6.0, 0.5] and start > 0:
            context = result_expr[max(0, start - 3):end + 3]
            if "**" in context or "^" in context:
                continue
        matches.append((start, end, match.group(1), val))

    matches.sort(key=lambda item: item[0], reverse=True)
    values = []
    names = []
    for i, (start, end, text, val) in enumerate(matches):
        param_idx = len(matches) - 1 - i
        name = f"p{param_idx}"
        if text.startswith("-"):
            replacement = f"-{name}"
            values.insert(0, abs(val))
        else:
            replacement = name
            values.insert(0, val)
        names.insert(0, name)
        result_expr = result_expr[:start] + replacement + result_expr[end:]
    return result_expr, jnp.asarray(values, dtype=jnp.float64), names


def make_param_u(expr_with_params: str, names: list[str]):
    def fn(x, y, t, params):
        ctx = {"x": x, "y": y, "t": t}
        for f in FUNCS:
            ctx[f] = getattr(jnp, f)
        ctx["pi"] = jnp.pi
        ctx["e"] = jnp.e
        ctx["sech"] = lambda z: 1 / jnp.cosh(z)
        ctx["JacobiSN"] = jax_sn
        ctx["JacobiCN"] = jax_cn
        ctx["JacobiDN"] = jax_dn
        for name, value in zip(names, params):
            ctx[name] = value
        return eval(expr_with_params, {"__builtins__": {}}, ctx)

    return fn


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
        widths = widths or [3]
        param_expr, init_params, names = nnsca_parametrized(codes, widths)
    else:
        param_expr, init_params, names = parse_params(expr)
    print(f"learnable parameters: {names}")
    if len(names) == 0:
        print("no numeric literals found; skipping parameter optimization")
        return expr

    u = make_param_u(param_expr, names)

    u_x = grad(u, argnums=0)
    u_y = grad(u, argnums=1)
    u_t = grad(u, argnums=2)
    u_xx = grad(u_x, argnums=0)
    u_yy = grad(u_y, argnums=1)
    u_xxx = grad(u_xx, argnums=0)
    u_xxxx = grad(u_xxx, argnums=0)
    u_xt = grad(u_x, argnums=2)

    def res(x, y, t, params):
        return (
            u_xt(x, y, t, params)
            + 4.0 * u_x(x, y, t, params) ** 2
            + 4.0 * u(x, y, t, params) * u_xx(x, y, t, params)
            + u_xxxx(x, y, t, params)
            + u_yy(x, y, t, params)
        )

    _, meshes = setup_symbols_meshes(problem)
    X, Y, T = meshes
    xflat = X.ravel()
    yflat = Y.ravel()
    tflat = T.ravel()
    u0_fn = make_xy_fn(ic_rhs(problem))
    true_fn = make_u_fn(problem["true_solution"])

    @jit
    def loss_and_rel_l2(params):
        rv = vmap(lambda x, y, t: res(x, y, t, params), (0, 0, 0))(xflat, yflat, tflat)
        pde_mse = jnp.mean(rv**2)

        ic_pred = u(xflat, yflat, jnp.zeros_like(xflat), params)
        ic_true = u0_fn(xflat, yflat)
        ic_mse = jnp.mean((ic_pred - ic_true) ** 2)
        total = pde_mse + w_ic * ic_mse

        u_pred = vmap(lambda x, y, t: u(x, y, t, params), (0, 0, 0))(xflat, yflat, tflat)
        u_tru = true_fn(xflat, yflat, tflat)
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
    print("final optimized KP-II expression:")
    print(f"  {final_expr}")

    u_opt = make_param_u(param_expr, names)
    U_true = true_fn(xflat, yflat, tflat)
    U_opt = u_opt(xflat, yflat, tflat, best_params)
    rel_l2 = float(
        jnp.sqrt(jnp.mean((U_opt - U_true) ** 2))
        / (jnp.sqrt(jnp.mean(U_true**2)) + 1e-30)
    )
    residual_mse = float(
        jnp.mean(vmap(lambda x, y, t: res(x, y, t, best_params), (0, 0, 0))(xflat, yflat, tflat) ** 2)
    )
    print(f"relative L2 error (optimized vs line soliton): {rel_l2:.6e}")
    print(f"final KP-II residual MSE: {residual_mse:.3e}")
    return final_expr

def numerics_to_symbols(expr: str):
    """Replace numeric literals in a best_expr string with SymPy symbols p0, p1, ...

    Exponent literals (for example the 2 in ``**2``) and the constants pi/e are
    left untouched.  The replacement logic mirrors ``parse_params`` so the two
    paths agree on which numbers are parameterised.
    """
    sym_expr = expr.replace("^", "**")
    pattern = re.compile(
        r"(?<![a-zA-Z0-9_.])([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)(?![a-zA-Z0-9_.])"
    )
    matches = []
    for match in pattern.finditer(sym_expr):
        text = match.group(1)
        start, end = match.span()
        val = float(text)
        if abs(val - sp.pi.n()) < 1e-10 or abs(val - sp.E.n()) < 1e-10:
            continue
        if start >= 2 and sym_expr[start - 2:start] == "**":
            continue
        if val in [2.0, 3.0, 4.0, 5.0, 6.0, 0.5] and start > 0:
            context = sym_expr[max(0, start - 3):end + 3]
            if "**" in context or "^" in context:
                continue
        matches.append((start, end, text))

    matches.sort(key=lambda item: item[0], reverse=True)
    names = []
    for i, (start, end, text) in enumerate(matches):
        param_idx = len(matches) - 1 - i
        name = f"p{param_idx}"
        replacement = f"-{name}" if text.startswith("-") else name
        names.insert(0, name)
        sym_expr = sym_expr[:start] + replacement + sym_expr[end:]

    symbols = [sp.Symbol(name) for name in names]
    return sym_expr, symbols


def _reduce_tanh_powers(expr):
    """Rewrite tanh(arg)**n (n >= 2) with tanh(arg)**2 = 1 - sech(arg)**2.

    This keeps tanh and sech**2 as the independent basis functions and avoids
    treating 1 and tanh**2 (which are linearly dependent) as separate bases.
    """
    def _is_high_tanh_power(e):
        return (
            e.is_Pow
            and e.base.func is sp.tanh
            and e.exp.is_Integer
            and e.exp >= 2
        )

    def _rewrite(e):
        arg = e.base.args[0]
        tail = sp.tanh(arg) ** (e.exp - 2) if e.exp > 2 else sp.Integer(1)
        return (1 - sp.sech(arg) ** 2) * tail

    return expr.replace(_is_high_tanh_power, _rewrite)


def extract_coefficients(residual):
    """Split an expanded residual into coefficients of independent basis functions.

    Every x,y,t-dependent transcendental subexpression is mapped to a fresh symbol
    bottom-up, then the numerator of the resulting rational expression is treated
    as a polynomial in those symbols.  The polynomial coefficients (functions of
    the free parameters only) are the algebraic equations to solve.
    """
    x, y, t = sp.symbols("x y t")
    residual = sp.expand(residual)
    residual = _reduce_tanh_powers(residual)
    residual = reduce_jacobi_powers(residual)
    residual = sp.expand(residual)

    mapping = {}
    while True:
        candidates = []
        for atom in residual.atoms(sp.Function):
            if any(arg.has(sp.Function) for arg in atom.args):
                continue
            relevant = any(
                x in arg.free_symbols
                or y in arg.free_symbols
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

    if residual.has(x) or residual.has(y) or residual.has(t):
        return [], [], "unable to separate x,y,t-dependent part"

    basis = list(mapping.values())
    together = sp.together(sp.expand(residual))
    numerator, _ = sp.fraction(together)
    numerator = sp.expand(numerator)
    if not basis:
        return ([] if numerator == 0 else [numerator]), basis, None

    poly = sp.Poly(numerator, *basis)
    equations = []
    seen = set()
    for coeff in poly.coeffs():
        coeff = sp.expand(coeff)
        if coeff == 0:
            continue
        key = sp.srepr(coeff)
        if key in seen:
            continue
        seen.add(key)
        equations.append(coeff)
    return equations, basis, None


def _solve_with_timeout(equations, symbols, timeout):
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
                return sp.solve(equations, symbols, dict=True), None
            except TimeoutError:
                return None, "timeout"
            except Exception as exc:
                return None, f"{type(exc).__name__}: {exc}"
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
    try:
        return sp.solve(equations, symbols, dict=True), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def symbolic_stage_two(expr: str, codes: list[int], problem: dict, timeout: int = 120) -> dict:
    """Try to derive an exact KP-II solution by symbolic back-substitution.

    Returns a dict with status in {'exact', 'no_solution', 'timeout',
    'unsupported', 'verification_failed'}.  Only ``status == 'exact'`` is an
    accepted answer; every other status falls back to numerical refinement.
    """
    if "abs(" in expr.lower():
        return {
            "status": "unsupported",
            "message": "expression contains abs(); symbolic differentiation is unreliable",
        }

    sym_expr, params = numerics_to_symbols(expr)
    try:
        f = sp.sympify(sym_expr, locals=SYMPY_LOCALS)
    except Exception as exc:
        return {"status": "unsupported", "message": f"sympify failed: {exc}"}

    x, y, t = sp.symbols("x y t")
    residual = (
        sp.diff(f, x, t)
        + 4 * sp.diff(f, x) ** 2
        + 4 * f * sp.diff(f, x, 2)
        + sp.diff(f, x, 4)
        + sp.diff(f, y, 2)
    )

    equations, basis, error = extract_coefficients(residual)
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
            if x in f_sub.free_symbols or y in f_sub.free_symbols or t in f_sub.free_symbols:
                return {
                    "status": "exact",
                    "exact_expr": f_sub,
                    "constraints": {},
                    "residual": simplified,
                    "message": "residual is identically zero for all parameters",
                }
            return {
                "status": "no_solution",
                "message": "residual is identically zero but the ansatz is x,y,t-independent",
            }
        return {
            "status": "no_solution",
            "message": "empty coefficient system with nonzero residual",
        }

    solutions, error = _solve_with_timeout(equations, unknowns, timeout)
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
        if x not in f_sub.free_symbols and y not in f_sub.free_symbols and t not in f_sub.free_symbols:
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
        "message": "only trivial x,y,t-independent solutions found; no nontrivial exact solution",
        "residual": residual,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--screen-x", type=int, default=256)
    parser.add_argument("--screen-y", type=int, default=256)
    parser.add_argument("--screen-t", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-1)
    parser.add_argument("--iters", type=int, default=10000)
    parser.add_argument("--w-ic", type=float, default=5.0)
    parser.add_argument("--rmse-threshold", type=float, default=1e-5)
    parser.add_argument("--rel-l2-threshold", type=float, default=5e-10)
    parser.add_argument("--stage2-only", action="store_true")
    parser.add_argument("--expr", default=None, help="initial ansatz for --stage2-only")
    return parser


def main(widths: list[int]):
    args = build_parser().parse_args()
    problem = create_kp_problem()
    print(f"operator: {problem['operators']}")
    print(f"true solution: {problem['true_solution']}")

    if args.stage2_only:
        expr = args.expr or "3.0*sech(x + y - 5.0*t)**2"
        codes = None
        structures = [(expr, codes)]
    else:
        expr, codes, top_candidates = stage_one(
            problem,
            args.n_samples,
            args.seed,
            (args.screen_x, args.screen_y, args.screen_t),
            widths=widths,
            topk=3,
        )
        structures = [(item[1], item[2]) for item in top_candidates] or [(expr, codes)]

        # Try exact-capable seeded structures first, then the top-3 screened ones.
        structures = []
        seen_codes = set()
        for seeded_expr, seeded_codes in seed_structure_candidates(widths):
            key = tuple(seeded_codes)
            if key in seen_codes:
                continue
            seen_codes.add(key)
            structures.append((seeded_expr, seeded_codes))
        for item in top_candidates:
            key = tuple(item[2])
            if key in seen_codes:
                continue
            seen_codes.add(key)
            structures.append((item[1], item[2]))
        if not structures:
            structures = [(expr, codes)]

    print("=" * 70)
    print("STAGE II: symbolic back-substitution over top structures")
    print("=" * 70)

    reasons = []
    for rank, (symbolic_expr, symbolic_codes) in enumerate(structures, start=1):
        symbolic = symbolic_stage_two(symbolic_expr, symbolic_codes, problem)
        if symbolic["status"] == "exact":
            print(f"structure #{rank} (codes={symbolic_codes}) is exact:")
            print("exact solution u(x, y, t) =")
            print(f"  {sp.sstr(symbolic['exact_expr'])}")
            print("parameter constraints:")
            if symbolic["constraints"]:
                for sym, val in symbolic["constraints"].items():
                    print(f"  {sym} = {sp.sstr(val)}")
            else:
                print("  (none)")
            print("back-substituted residual (must be 0):")
            print(f"  {sp.sstr(symbolic['residual'])}")
            print("精确解（符号验证通过）")
            return
        reasons.append(f"#{rank}: {symbolic['message']}")
        print(f"structure #{rank} not exact: {symbolic['message']}")

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
        widths,
    )
    print(f"数值近似解（符号求解失败：{' | '.join(reasons)}）")
