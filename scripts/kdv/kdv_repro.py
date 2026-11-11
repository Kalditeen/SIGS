#!/usr/bin/env python3
"""Reproduce the KdV 1-soliton result with the original SIGS hyperparameters.

This is a refactor-aware adaptation of the KdV walkthrough in
``notebooks/demo_pdes.ipynb``. The notebook's original flow used:

    Stage I  - sample 5000 SPATIOTEMPORAL_2D atoms from the cluster database,
               keep atoms whose first coefficient is >= 0.5, lift each atom to
               the series ``1 + a*phi + b*phi^2``, and rank the structures by
               the symbolic KdV residual plus the initial condition.
    Stage II - promote every numeric literal to a free parameter and refine it
               with JAX autodiff, AdaBelief, IC weight 5, and early stopping on
               either the weighted RMSE or the relative L2 error.

The manufactured solution is the 1-soliton u(x,t) = 2 / cosh^2(x - 4t).

Usage:
    python scripts/kdv_repro.py                 # original-scale run
    python scripts/kdv_repro.py --n-samples 200 --iters 500   # quick smoke
"""

from __future__ import annotations

import argparse
import re
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

jax.config.update("jax_enable_x64", True)

REPO_ROOT = Path(__file__).resolve().parents[2]

FUNCS = ["sin", "cos", "exp", "log", "sqrt", "tanh", "sinh", "cosh", "abs"]


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


def ic_rhs(problem: dict) -> str:
    cond = problem["initial_condition"][0]
    return cond.rsplit("=", 1)[1].strip()


def setup_symbols_meshes(problem: dict, points: dict | None = None):
    x, t = sp.symbols("x t")
    px = (points or problem["mesh"])["x"]["points"]
    pt = (points or problem["mesh"])["t"]["points"]
    xs = np.linspace(
        problem["mesh"]["x"]["start"], problem["mesh"]["x"]["end"], px
    )
    ts = np.linspace(
        problem["mesh"]["t"]["start"], problem["mesh"]["t"]["end"], pt
    )
    X, T = np.meshgrid(xs, ts, indexing="ij")
    return {"x": x, "t": t}, [X, T]


def make_u_fn(expr_str: str):
    """Compile an expression string in (x, t) into a JAX callable."""
    expr = ExpressionUtils.standardize_expression(expr_str)

    def fn(x, t):
        ctx = {"x": x, "t": t}
        for f in FUNCS:
            ctx[f] = getattr(jnp, f)
        ctx["pi"] = jnp.pi
        ctx["e"] = jnp.e
        return eval(expr, {"__builtins__": {}}, ctx)

    return fn


def make_x_fn(expr_str: str):
    """Compile an expression string in x only into a JAX callable."""
    expr = ExpressionUtils.standardize_expression(expr_str)

    def fn(x):
        ctx = {"x": x}
        for f in FUNCS:
            ctx[f] = getattr(jnp, f)
        ctx["pi"] = jnp.pi
        ctx["e"] = jnp.e
        return eval(expr, {"__builtins__": {}}, ctx)

    return fn


def make_numpy_x_fn(expr_str: str):
    x = sp.symbols("x")
    expr = sp.sympify(ExpressionUtils.standardize_expression(expr_str))
    return sp.lambdify((x,), expr, modules="numpy")


def score_candidate(expr_str: str, symbols, meshes, u0_fn, ic_weight: float = 1.0):
    """Rank one series ansatz with the exact symbolic KdV residual."""
    x, t = symbols["x"], symbols["t"]
    X, T = meshes
    try:
        u = sp.sympify(ExpressionUtils.standardize_expression(expr_str))
        residual = sp.diff(u, t) + 6.0 * u * sp.diff(u, x) + sp.diff(u, x, 3)

        residual_fn = sp.lambdify((x, t), residual, modules="numpy")
        rv = np.asarray(residual_fn(X, T))
        if np.iscomplexobj(rv):
            rv = np.real(rv)
        rv = np.nan_to_num(
            np.asarray(rv, dtype=np.float64), nan=1e3, posinf=1e3, neginf=-1e3
        )
        pde_mse = float(np.mean(rv**2))

        ic_fn = sp.lambdify((x,), u.subs(t, 0.0), modules="numpy")
        ic_pred = np.asarray(ic_fn(X[:, 0]))
        ic_true = np.asarray(u0_fn(X[:, 0]))
        ic_mse = float(np.mean((ic_pred - ic_true) ** 2))
        return pde_mse + ic_weight * ic_mse
    except Exception:
        return float("inf")


def lift_to_series(expr: str, max_k: int = 2) -> str:
    phi = f"({expr})"
    terms = ["1"]
    for k in range(1, max_k + 1):
        terms.append(f"1*({phi})^{k}")
    return " + ".join(terms)


def stage_one(
    problem: dict,
    n_samples: int,
    seed: int,
    screen_points: tuple[int, int],
    rmse_threshold: float = 3e-2,
):
    print("=" * 70)
    print("STAGE I: MathClass cluster sampling + symbolic KdV screening")
    print("=" * 70)

    sampler = FlexibleVectorSampler(
        cluster_file=str(REPO_ROOT / "data" / "clusters.pkl"), device="cpu"
    )
    sample_id = sampler.sample_from_subclusters(
        categories={MathClass.SPATIOTEMPORAL_2D: 5},
        n_samples=n_samples,
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
    candidates = [lift_to_series(e, max_k=2) for e in base_exprs]
    print(f"scoring {len(candidates)} series ansatze")

    symbols, meshes = setup_symbols_meshes(
        problem,
        points={
            "x": {"start": -10.0, "end": 10.0, "points": screen_points[0]},
            "t": {"start": 0.0, "end": 1.0, "points": screen_points[1]},
        },
    )
    u0_fn = make_numpy_x_fn(ic_rhs(problem))

    best_expr = None
    best_loss = float("inf")
    start = time.time()
    for idx, expr in enumerate(candidates):
        loss = score_candidate(expr, symbols, meshes, u0_fn)
        if loss < best_loss:
            best_loss = loss
            best_expr = expr
        if (idx + 1) % 100 == 0 or idx == 0:
            print(f"  [{idx + 1}/{len(candidates)}] best RMSE ~ {float(np.sqrt(best_loss)):.3e}")
        if np.isfinite(best_loss) and float(np.sqrt(best_loss)) < rmse_threshold:
            print(f"  early stop at candidate {idx + 1}: structural RMSE below {rmse_threshold:.1e}")
            break

    print(f"screening took {time.time() - start:.1f}s")
    print(f"best structural KdV series expr:\n  {best_expr}")
    return best_expr


def parse_params(expr: str):
    result_expr = expr.replace("^", "**")
    pattern = r"(?<![a-zA-Z0-9_.])([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)(?![a-zA-Z0-9_.])"
    matches = []
    for match in re.finditer(pattern, result_expr):
        val = float(match.group(1))
        start, end = match.span()
        if abs(val - 3.14159265359) < 1e-10 or abs(val - 2.71828182846) < 1e-10:
            continue
        if start >= 2 and result_expr[start - 2 : start] == "**":
            continue
        if val in [2.0, 3.0, 4.0, 5.0, 6.0, 0.5] and start > 0:
            context = result_expr[max(0, start - 3) : end + 3]
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
    def fn(x, t, params):
        ctx = {"x": x, "t": t}
        for f in FUNCS:
            ctx[f] = getattr(jnp, f)
        ctx["pi"] = jnp.pi
        ctx["e"] = jnp.e
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
):
    print("=" * 70)
    print("STAGE II: JAX autodiff parameter refinement")
    print("=" * 70)

    param_expr, init_params, names = parse_params(expr)
    print(f"learnable parameters: {names}")
    if len(names) == 0:
        print("no numeric literals found; skipping parameter optimization")
        return expr

    u = make_param_u(param_expr, names)
    u_t = grad(u, argnums=1)
    u_x = grad(u, argnums=0)
    u_xx = grad(u_x, argnums=0)
    u_xxx = grad(u_xx, argnums=0)

    def res(x, t, params):
        return u_t(x, t, params) + 6.0 * u(x, t, params) * u_x(x, t, params) + u_xxx(x, t, params)

    _, meshes = setup_symbols_meshes(problem)
    X, T = meshes
    xflat = X.ravel()
    tflat = T.ravel()
    u0_fn = make_x_fn(ic_rhs(problem))
    true_fn = make_u_fn(problem["true_solution"])

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
    print(f"final optimized KdV expression:\n  {final_expr}")

    u_opt = make_param_u(param_expr, names)
    U_true = true_fn(xflat, tflat)
    U_opt = u_opt(xflat, tflat, best_params)
    rel_l2 = float(jnp.sqrt(jnp.mean((U_opt - U_true) ** 2)) / (jnp.sqrt(jnp.mean(U_true**2)) + 1e-30))
    residual_mse = float(jnp.mean(vmap(lambda x, t: res(x, t, best_params), (0, 0))(xflat, tflat) ** 2))
    print(f"relative L2 error (optimized vs true soliton): {rel_l2:.6e}")
    print(f"final KdV residual MSE: {residual_mse:.3e}")
    return final_expr


def main():
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
    parser.add_argument(
        "--expr",
        default=None,
        help="initial ansatz when --stage2-only is set",
    )
    args = parser.parse_args()

    problem = create_kdv_problem()
    print(f"operator: {problem['operators']}")
    print(f"true solution: {problem['true_solution']}")

    if args.stage2_only:
        expr = args.expr or "2.0*cosh(1.1*(x - 3.5*t))**(-2)"
    else:
        expr = stage_one(
            problem,
            args.n_samples,
            args.seed,
            (args.screen_x, args.screen_t),
        )

    stage_two(
        problem,
        expr,
        args.lr,
        args.iters,
        args.w_ic,
        args.rmse_threshold,
        args.rel_l2_threshold,
    )


if __name__ == "__main__":
    main()
