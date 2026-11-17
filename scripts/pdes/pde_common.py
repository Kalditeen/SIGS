#!/usr/bin/env python3
"""Shared PDE validation engine for NNSCA new-solution discovery.

This is the parameterised full-expression Stage-I / symbolic Stage-II pipeline
used by the shallow-water and higher-order shallow-water validation programs.
Each equation is described by a :class:`PDESpec`; the thin ``*_nnsca.py`` entry
points in this directory only fill in the equation-specific pieces.

The Stage-I score is reference-free: it ranks candidates by PDE residual,
anti-triviality, derivative-closure, and a small complexity term.  Stage-II
symbolically extracts coefficient equations and verifies exact solutions by
back-substitution.
"""

from __future__ import annotations

import argparse
import random
import re
import signal
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

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


@dataclass
class PDESpec:
    name: str
    problem_type: str
    operators: str
    residual: Callable[[sp.Expr, sp.Symbol, sp.Symbol], sp.Expr]
    true_solution: sp.Expr
    seed_functions: list[tuple[str, int]]
    search_atoms: list[str]
    baseline: list[str]
    baseline_defaults: dict[str, str]
    variable_coefficient: bool = False
    second_order_time: bool = False
    mesh: dict | None = None


DEFAULT_MESH = {
    "x": {"start": -10.0, "end": 10.0, "points": 256},
    "t": {"start": 0.0, "end": 1.0, "points": 128},
}


def create_problem(spec: PDESpec) -> dict:
    x, t = sp.symbols("x t")
    u_true = sp.simplify(spec.true_solution)
    u0 = sp.simplify(u_true.subs(t, 0.0))
    ut0 = sp.simplify(sp.diff(u_true, t).subs(t, 0.0))
    initial_condition = [f"u(x, t=0) = {u0}"]
    if spec.second_order_time:
        initial_condition.append(f"u_t(x, t=0) = {ut0}")

    return {
        "problem_type": spec.problem_type,
        "operators": spec.operators,
        "F": "0",
        "initial_condition": initial_condition,
        "boundary_conditions": [],
        "mesh": spec.mesh or DEFAULT_MESH,
        "parameters": {},
        "true_solution": str(u_true),
    }


def _is_derivative_closure_valid(expr_str: str, x: sp.Symbol) -> bool:
    """Reject candidates whose third x-derivative explodes algebraically."""
    try:
        u = sp.sympify(
            ExpressionUtils.standardize_expression(expr_str), locals=_ch.SYMPY_LOCALS
        )
        u_xxx = sp.diff(u, x, 3)
        if sp.count_ops(u_xxx) > 15 * max(sp.count_ops(u), 1):
            return False
    except Exception:
        return False
    return True


def _is_allowed_inner_expr(expr: str) -> bool:
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
    try:
        u = sp.sympify(ExpressionUtils.standardize_expression(expr), locals=_ch.SYMPY_LOCALS)
        return float(sp.count_ops(u))
    except Exception:
        return float("inf")


def _max_tanh_sech_depth(expr: str) -> int:
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


def _sample_full_expressions(spec: PDESpec, n_samples: int, seed: int):
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
    atoms = [
        expr
        for expr in list(base_exprs) + spec.search_atoms
        if _is_allowed_inner_expr(expr)
    ]
    if not atoms:
        atoms = [expr for expr in spec.search_atoms if _is_allowed_inner_expr(expr)]
    rng = random.Random(seed)
    rng.shuffle(atoms)
    return atoms


def _collect_full_expression_blocks(
    spec: PDESpec, widths: list[int], n_samples: int, seed: int, n_seeds: int
):
    n_terms = widths[0]
    blocks = []
    seen = set()
    for i in range(n_seeds):
        atoms = _sample_full_expressions(spec, n_samples, seed + i)
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
    terms = [f"{leading}*({_ch.activation_str(seed_code, arg)})" for arg in args]
    return "0.000000 + " + " + ".join(terms)


def _hardcoded_baseline_candidates(spec: PDESpec):
    candidates = []
    for expr in spec.baseline:
        numeric = expr
        for symbol, value in spec.baseline_defaults.items():
            numeric = re.sub(rf"\b{symbol}\b", value, numeric)
        candidates.append((numeric, None))
    return candidates


def _score_candidate_unbiased(
    spec: PDESpec,
    expr_str: str,
    symbols: dict,
    meshes: list[np.ndarray],
    act_floor: float = 1e-3,
    w_act: float = 1.0,
    u_max: float = 1e8,
):
    x, t = symbols["x"], symbols["t"]
    X, T = meshes
    try:
        if not _is_derivative_closure_valid(expr_str, x):
            return float("inf")
        u = sp.sympify(
            ExpressionUtils.standardize_expression(expr_str), locals=_ch.SYMPY_LOCALS
        )
        residual = spec.residual(u, x, t)

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


def _refine_candidate_params(
    spec: PDESpec,
    expr_str: str,
    symbols: dict,
    meshes: list[np.ndarray],
    opt_points: tuple[int, int] = (48, 24),
    maxiter: int = 50,
    act_floor: float = 1e-3,
    w_act: float = 1.0,
    u_max: float = 1e8,
):
    try:
        param_expr, init_params, names = _ch.parse_params(expr_str)
    except Exception:
        return float("inf"), expr_str
    if not names:
        return float("inf"), expr_str

    try:
        x, t = symbols["x"], symbols["t"]
        u = sp.sympify(param_expr, locals=_ch.SYMPY_LOCALS)
        residual = spec.residual(u, x, t)
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
            nan=1e3,
            posinf=1e3,
            neginf=-1e3,
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
    spec: PDESpec,
    refined_expr: str,
    symbols: dict,
    meshes: list[np.ndarray],
    n_perturbations: int = 5,
    perturb_scale: float = 0.01,
):
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
        residual = spec.residual(u, x, t)
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
        rv = np.nan_to_num(rv, nan=1e3, posinf=1e3, neginf=-1e3)
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
    spec: PDESpec,
    seed_name: str,
    seed_code: int,
    problem: dict,
    screen_points: tuple[int, int],
    blocks: list[tuple[str, ...]],
    topk: int,
    act_floor: float = 1e-3,
    refine_maxiter: int = 50,
    w_complexity: float = 1e-4,
    plain_candidates: list[tuple[str, object]] | None = None,
):
    print(f"seed {seed_name}: scoring {len(blocks)} full SIGS expression blocks")
    symbols, meshes = _ch.setup_symbols_meshes(
        problem,
        points={
            "x": {"start": -10.0, "end": 10.0, "points": screen_points[0]},
            "t": {"start": 0.0, "end": 1.0, "points": screen_points[1]},
        },
    )

    candidates = []
    for candidate, block in plain_candidates or []:
        if _max_tanh_sech_depth(candidate) > 1:
            continue
        if not _is_derivative_closure_valid(candidate, symbols["x"]):
            continue
        candidates.append((candidate, block))
    for block in blocks:
        candidate = _seed_wrapped_candidate(seed_code, block)
        if _max_tanh_sech_depth(candidate) > 1:
            continue
        if not _is_derivative_closure_valid(candidate, symbols["x"]):
            continue
        candidates.append((candidate, block))

    raw_scores = []
    start = time.time()
    for idx, (candidate, block) in enumerate(candidates, start=1):
        loss = _score_candidate_unbiased(
            spec, candidate, symbols, meshes, act_floor=act_floor
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
        loss, refined_expr = _refine_candidate_params(
            spec,
            candidate,
            symbols,
            meshes,
            maxiter=refine_maxiter,
            act_floor=act_floor,
        )
        gen_loss = _score_multi_point_generalization(spec, refined_expr, symbols, meshes)

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
    spec: PDESpec,
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
    widths = list(widths or [1])
    print("=" * 70)
    print(f"STAGE I: full SIGS expressions wrapped by {spec.name} seed functions (reference-free)")
    print("=" * 70)

    best_loss = float("inf")
    best_expr = None
    groups = []
    print("--- hardcoded-baseline (physics-prior skeletons) ---")
    baseline_top = _score_seed_wrapped(
        spec,
        "hardcoded-baseline",
        0,
        problem,
        screen_points,
        [],
        topk,
        act_floor=act_floor,
        refine_maxiter=refine_maxiter,
        w_complexity=w_complexity,
        plain_candidates=_hardcoded_baseline_candidates(spec),
    )
    groups.append(_make_group("hardcoded-baseline", 0, baseline_top))
    for loss, item_expr, _block, _refined in baseline_top:
        if loss < best_loss:
            best_loss = loss
            best_expr = item_expr

    blocks = _collect_full_expression_blocks(spec, widths, n_samples, seed, n_seeds)
    print(f"sampled {len(blocks)} unique full-expression blocks over {n_seeds} seeds")

    for name, seed_code in spec.seed_functions:
        print(f"--- seed {name} (code {seed_code}) ---")
        top_candidates = _score_seed_wrapped(
            spec,
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
        groups.append(_make_group(name, seed_code, top_candidates))
        for loss, item_expr, _block, _refined in top_candidates:
            if loss < best_loss:
                best_loss = loss
                best_expr = item_expr

    print(f"full-expression best loss={best_loss:.6e}")
    if best_expr is not None:
        print(f"best full-expression {spec.name} candidate:")
        print(f"  {best_expr}")
    return best_expr, None, groups


def _make_group(name: str, seed_code: int, top_candidates):
    members = [(item_expr, None) for _loss, item_expr, _block, _refined in top_candidates]
    refined_exprs = [refined for _loss, _item_expr, _block, refined in top_candidates]
    return {
        "name": name,
        "seed_code": seed_code,
        "members": members,
        "refined": refined_exprs,
    }


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


def _maple_coeff_equations(residual, variable_coefficient: bool = False):
    """Return coefficient equations from a PDE residual in Maple's style.

    Pure rational residuals are cleared and treated as polynomials in x,t.  For
    transcendental residuals the independent functions are replaced bottom-up
    by fresh symbols.  Variable-coefficient equations additionally keep x,t as
    polynomial generators so time-dependent coefficients survive into the
    coefficient system.
    """
    x, t = sp.symbols("x t")
    residual = sp.together(residual)
    numerator, _denominator = sp.fraction(residual)
    residual = sp.expand(numerator)
    try:
        poly = sp.Poly(sp.expand(residual), x, t)
        coeffs = poly.coeffs()
        basis = []
    except sp.PolynomialError:
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

        residual = sp.together(residual)
        numerator, _denominator = sp.fraction(residual)
        residual = sp.expand(numerator)

        basis = list(mapping.values())
        poly_symbols = list(basis)
        if residual.has(x) or residual.has(t):
            if not variable_coefficient:
                return [], []
            poly_symbols.extend([x, t])

        if not poly_symbols:
            coeffs = [] if sp.expand(residual) == 0 else [residual]
        else:
            poly = sp.Poly(sp.expand(residual), *poly_symbols)
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


def _single_phase_coeff_equations(residual, variable_coefficient: bool = False):
    """Coefficient extraction for one-phase tanh/sech solitons.

    Rewrites even powers of sech as polynomials in tanh.  This avoids treating
    sech and tanh as independent generators, which fails for sech^4 forms.
    """
    x, t = sp.symbols("x t")
    funcs = [atom for atom in residual.atoms(sp.Function) if atom.func in (sp.tanh, sp.sech)]
    args = {atom.args[0] for atom in funcs}
    if len(args) != 1:
        return None
    theta = args.pop()
    tt = sp.Symbol("__T")
    expr = sp.expand(residual)
    expr = expr.replace(
        lambda e: (
            e.is_Pow
            and e.base == sp.sech(theta)
            and e.exp.is_Integer
            and e.exp >= 2
            and e.exp % 2 == 0
        ),
        lambda e: (1 - tt**2) ** (e.exp // 2),
    )
    if expr.has(sp.sech(theta)):
        return None
    expr = sp.expand(expr.replace(sp.tanh(theta), tt))
    generators = [tt]
    if variable_coefficient or expr.has(x) or expr.has(t):
        generators.extend([x, t])
    try:
        poly = sp.Poly(sp.expand(expr), *generators)
    except sp.PolynomialError:
        return None

    equations = []
    seen = set()
    for coeff in poly.coeffs():
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
    return equations, []


def _probe_nonconstant_solution(expr, x, t, tol: float = 1e-6) -> bool:
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


def symbolic_stage_two(
    spec: PDESpec, expr: str, codes: list[int], problem: dict, timeout: int = 120
) -> dict:
    if "abs(" in expr.lower():
        return {
            "status": "unsupported",
            "message": "expression contains abs(); symbolic differentiation is unreliable",
        }

    # A literal expression (for example the default --stage2-only true solution)
    # should be checked as-is before numeric literals are parameterised.
    try:
        x, t = sp.symbols("x t")
        direct_f = sp.sympify(expr, locals=_ch.SYMPY_LOCALS)
        if codes is None and direct_f.free_symbols <= {x, t}:
            direct_residual = spec.residual(direct_f, x, t)
            try:
                if sp.expand(sp.together(direct_residual)) == 0:
                    return {
                        "status": "exact",
                        "exact_expr": direct_f,
                        "constraints": {},
                        "residual": sp.Integer(0),
                        "message": "expression is an exact solution",
                    }
            except Exception:
                pass
            simplified, timeout_error = _call_with_timeout(
                lambda: sp.simplify(direct_residual) == 0, timeout=10
            )
            if timeout_error is None and simplified:
                return {
                    "status": "exact",
                    "exact_expr": direct_f,
                    "constraints": {},
                    "residual": sp.Integer(0),
                    "message": "expression is an exact solution",
                }
    except Exception:
        pass
    sym_expr, params = _ch.numerics_to_symbols(expr)
    try:
        f = sp.sympify(sym_expr, locals=_ch.SYMPY_LOCALS)
    except Exception as exc:
        return {"status": "unsupported", "message": f"sympify failed: {exc}"}

    x, t = sp.symbols("x t")
    residual = spec.residual(f, x, t)

    def _solve_candidate():
        try:
            single_result = _single_phase_coeff_equations(
                residual, variable_coefficient=spec.variable_coefficient
            )
            if single_result is None:
                equations, basis = _maple_coeff_equations(
                    residual, variable_coefficient=spec.variable_coefficient
                )
            else:
                equations, basis = single_result
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


def _print_candidate_structures(spec: PDESpec, groups):
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
    parser.add_argument("--stage2", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--expr", default=None, help="initial ansatz for --stage2-only")
    parser.add_argument("--n-seeds", type=int, default=5)
    parser.add_argument("--stage1-topk", type=int, default=3)
    parser.add_argument("--stage1-act-floor", type=float, default=1e-3)
    parser.add_argument("--stage1-refine-maxiter", type=int, default=50)
    parser.add_argument("--stage1-complexity-weight", type=float, default=1e-4)
    return parser


def main(spec: PDESpec, widths: list[int]):
    args = build_parser().parse_args()
    widths = list(widths or [1])
    problem = create_problem(spec)
    print(f"operator: {problem['operators']}")
    print(f"true solution: {problem['true_solution']}")

    if args.stage2_only:
        expr = args.expr or str(sp.sstr(spec.true_solution))
        groups = [{
            "name": "stage2-only",
            "seed_code": None,
            "members": [(expr, None)],
        }]
    else:
        expr, codes, groups = stage_one(
            spec,
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
        _print_candidate_structures(spec, groups)
        return

    print("=" * 70)
    print(f"STAGE II: symbolic back-substitution for {spec.name}")
    print("=" * 70)

    reasons = []
    exact_solutions = []
    for group in groups:
        group_name = group["name"]
        seed_code = group["seed_code"]
        header = group_name if seed_code is None else f"seed {group_name} (first-layer code {seed_code})"
        print(f"--- {header} ---")
        for rank, (symbolic_expr, symbolic_codes) in enumerate(group["members"], start=1):
            print(f"  candidate #{rank} (codes={symbolic_codes}) solving symbolically...", flush=True)
            symbolic = symbolic_stage_two(spec, symbolic_expr, symbolic_codes, problem)
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
    print("STAGE II: no exact symbolic solution found")
    print("=" * 70)
    for message in reasons:
        print(f"  - {message}")
