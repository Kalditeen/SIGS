#!/usr/bin/env python3
"""Shared PDE validation engine for NNSCA new-solution discovery.

This is the parameterised full-expression Stage-I / symbolic Stage-II pipeline
used by the shallow-water and higher-order shallow-water validation programs.
Each equation is described by a :class:`PDESpec`; the thin ``*_nnsca.py`` entry
points in this directory only fill in the equation-specific pieces.

Stage-I is a prior-free structural prefilter: it builds candidates with the
NNSCA layer-wise constructor ``lift_to_nnsca(codes, widths)`` from a
parameterised phase vocabulary, keeps every syntactically valid, x/t-dependent,
derivative-closed candidate under the complexity budget, and sends them all to
Stage-II.  Stage-II then parameterises every numeric literal, symbolically
extracts coefficient equations, and verifies exact solutions by
back-substitution.
"""

from __future__ import annotations

import argparse
import itertools
import random
import re
import sys
import time
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Callable

import jax
import numpy as np
import sympy as sp

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
    extra_ansatz: list[str] = field(default_factory=list)
    pde_parameters: dict[str, sp.Symbol] = field(default_factory=dict)
    pde_parameter_defaults: dict[str, str] = field(default_factory=dict)
    momentum: Callable[[sp.Expr, sp.Symbol, sp.Symbol], sp.Expr] | None = None
    first_layer_phases: list[str] | None = None


DEFAULT_MESH = {
    "x": {"start": -10.0, "end": 10.0, "points": 256},
    "t": {"start": 0.0, "end": 1.0, "points": 128},
}

# Stage-II symbolic budgets.  These bound individual expensive SymPy calls, not the
# structural depth of a candidate.
STAGE2_EXTRACT_TIMEOUT = 30
STAGE2_SOLVE_TIMEOUT = 30
STAGE2_VERIFY_TIMEOUT = 8
STAGE2_MAX_SOLUTIONS = 600
MAX_DERIVATIVE_EXPANSION_RATIO = 300.0
MAX_COEFF_EQUATIONS = 200

# Stage-I is now a pure structural prefilter.  There is no numeric residual
# ranking and no top-k selection: a candidate only needs to be syntactically
# valid, x/t-dependent, closed under the required derivatives, and below the
# complexity budget.  Every survivor goes to the exact symbolic Stage-II.
STAGE1_MAX_CANDIDATES = 2000
STAGE1_EXHAUSTIVE_COMBOS = 2000
STAGE1_MAX_COMPLEXITY = 250.0
STAGE1_DERIVATIVE_TIMEOUT = 1

# Parameterised first-layer phase skeletons for the NNSCA role constructor.
# Stage-II turns every numeric literal into an independent symbol, so these
# strings only fix the functional skeleton, not coefficient values.  Linear,
# quadratic and trig/exp phases are mixed so non-travelling-wave structures
# such as exp(t + cos(x)) are reachable without any physics prior.
GENERAL_FIRST_LAYER_PHASES = [
    "1.000000*x + 1.000000*t + 1.000000",
    "1.000000*t + 1.000000*cos(1.000000*x + 1.000000) + 1.000000",
    "1.000000*t + 1.000000*sin(1.000000*x + 1.000000) + 1.000000",
    "1.000000*x**2 + 1.000000*x*t + 1.000000*t**2 + 1.000000",
    "1.000000*x + 1.000000*cos(1.000000*t + 1.000000) + 1.000000",
    "1.000000*x + 1.000000*sin(1.000000*t + 1.000000) + 1.000000",
    "1.000000*t + 1.000000*exp(1.000000*x + 1.000000) + 1.000000",
    "1.000000*x + 1.000000*exp(1.000000*t + 1.000000) + 1.000000",
]


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


def _sympify_expr(expr_str: str):
    """Sympify one string once and return None on failure."""
    try:
        return sp.sympify(
            ExpressionUtils.standardize_expression(expr_str), locals=_ch.SYMPY_LOCALS
        )
    except Exception:
        return None


def _pde_default_substitutions(spec: PDESpec) -> dict:
    """Map PDE-level symbols (for example k in CH) to their numeric defaults."""
    subs = {}
    for name, sym in spec.pde_parameters.items():
        default = spec.pde_parameter_defaults.get(name, "1.0")
        try:
            subs[sym] = sp.sympify(default)
        except Exception:
            subs[sym] = sp.Integer(1)
    return subs




def _is_valid_phase_argument(expr: sp.Expr) -> bool:
    """Keep structural exploration open; safety is enforced by soft penalties."""
    if expr.has(sp.Abs):
        return False
    for atom in expr.atoms(sp.Function):
        if len(atom.args) not in (1, 2):
            return False
    return True


def _inspect_candidate(expr_str: str, x: sp.Symbol | None = None) -> dict:
    """Parse and analyse a candidate once.

    Returns allowed/complexity/depth/closure flags so the later scoring
    functions do not have to sympify the same string repeatedly.
    """
    std = ExpressionUtils.standardize_expression(expr_str)
    result = {
        "u": None,
        "allowed": False,
        "complexity": float("inf"),
        "depth": 999,
        "closure_ok": True,
        "expansion_ratio": 1.0,
    }
    if "abs(" in std:
        return result
    u = _sympify_expr(expr_str)
    if u is None:
        return result

    allowed = True
    allowed = _is_valid_phase_argument(u)

    depth = 0

    def walk(node, current_depth):
        nonlocal depth
        if node.func in (sp.tanh, sp.sech):
            current_depth += 1
            depth = max(depth, current_depth)
        for arg in node.args:
            walk(arg, current_depth)

    walk(u, 0)

    expansion_ratio = 1.0
    if x is not None:
        base_ops = float(sp.count_ops(u))
        if base_ops > STAGE1_MAX_COMPLEXITY:
            expansion_ratio = 999.0
        else:
            u_xxx, diff_error = _ch._call_with_timeout(
                lambda: sp.diff(u, x, 3), STAGE1_DERIVATIVE_TIMEOUT
            )
            if diff_error is not None or u_xxx is None:
                expansion_ratio = 999.0
            else:
                expansion_ratio = float(sp.count_ops(u_xxx)) / max(base_ops, 1.0)
    closure_ok = expansion_ratio <= MAX_DERIVATIVE_EXPANSION_RATIO

    result.update({
        "u": u,
        "allowed": allowed,
        "complexity": float(sp.count_ops(u)),
        "depth": depth,
        "closure_ok": closure_ok,
        "expansion_ratio": expansion_ratio,
    }
    )
    return result


def _pde_activation_code_from_atom(expr: str) -> int:
    """Return the NNSCA activation code of an atom, preserving squared forms.

    The generic ch_common helper returns only the unsquared base code, so
    ``tanh(x)**2`` would collapse to code 1 instead of code 2.  This is the
    same preservation rule used by the KdV NNSCA implementation.
    """
    std = ExpressionUtils.standardize_expression(expr)
    for name, squared in _ch.extract_function_tokens(std):
        base = _ch.NAME_CODES.get(name)
        if base is None:
            continue
        if squared and name in _ch.SQ_CODES:
            return _ch.SQ_CODES[name]
        return base
    return 0

def _nnsca_role_candidates(
        spec: PDESpec,
        n_samples: int,
        seed: int,
        widths: list[int],
        n_seeds: int = 1,
        max_candidates: int = STAGE1_MAX_CANDIDATES,
        exhaustive_combos: int = STAGE1_EXHAUSTIVE_COMBOS,
):
    """Generate candidates with the NNSCA layer-wise neural constructor.

    ``widths`` are the hidden-layer sizes.  Each role is an activation code; the
    full trial function is built by :func:`ch_common.lift_to_nnsca` exactly like
    the original NNSCA scripts, while SIGS supplies the role atoms.
    """
    widths = [max(1, int(w)) for w in widths]
    n_roles = sum(widths)
    sampler = FlexibleVectorSampler(
        cluster_file=str(REPO_ROOT / "data" / "clusters.pkl"), device="cpu"
    )
    per_run_samples = max(1, n_samples // max(1, n_seeds))
    alphabet = {0}
    for _name, code in spec.seed_functions:
        alphabet.add(int(code))
    for atom in spec.search_atoms:
        alphabet.add(_pde_activation_code_from_atom(atom))

    total_raw = 0
    for run_i in range(max(1, n_seeds)):
        run_seed = seed + run_i
        sample_id = sampler.sample_from_subclusters(
            categories={MathClass.SPATIOTEMPORAL_2D: n_roles},
            n_samples=max(per_run_samples * n_roles, n_roles),
            operator="",
            seed=run_seed,
            model=None,
        )
        exprs, _, _, _ = sampler.get_sampling_results(sample_id)
        total_raw += len(exprs)
        filtered = ExpressionUtils.filter_by_first_const(exprs, min_val=0.5)
        if not filtered:
            filtered = [(i, e) for i, e in enumerate(exprs)]
        _, base_exprs = zip(*filtered)
        for atom in base_exprs:
            alphabet.add(_pde_activation_code_from_atom(atom))

    alphabet = sorted(alphabet)
    print(
        f"nnsca-roles: SIGS supplied {total_raw} raw atoms -> activation alphabet {alphabet}"
    )

    candidates = []
    seen = set()

    def add(codes: list[int]):
        codes = list(_ch._pad_codes(codes, n_roles))
        key = tuple(codes)
        if key in seen:
            return
        seen.add(key)
        phase_templates = spec.first_layer_phases or GENERAL_FIRST_LAYER_PHASES
        shift = sum(codes) % max(1, len(phase_templates))
        phases = phase_templates[shift:] + phase_templates[:shift]
        candidates.append((_ch.lift_to_nnsca(codes, widths, first_layer_args=phases), codes))

    # Exact-capable single-layer seeds first, then the full NNSCA code space.
    for _name, code in spec.seed_functions:
        add([code] * widths[0])
    if len(widths) >= 2:
        prefix = widths[0]
        for _name, code in spec.seed_functions:
            add([0] * prefix + [code] * widths[1])

    total_combos = len(alphabet) ** n_roles
    if total_combos <= exhaustive_combos:
        for combo in itertools.product(alphabet, repeat=n_roles):
            add(list(combo))
    else:
        rng = random.Random(seed + 20261120)
        attempts = 0
        while len(candidates) < max_candidates and attempts < max_candidates * 50:
            attempts += 1
            combo = tuple(rng.choice(alphabet) for _ in range(n_roles))
            add(list(combo))

    print(f"nnsca-roles: built {len(candidates)} layer-wise NNSCA structures")
    return candidates


def _prefilter_candidates(spec: PDESpec, plain_candidates, x, t):
    """Keep structurally admissible candidates without any numeric scoring.

    Validity, x/t-dependence, derivative closure and the complexity budget are
    the only gates.  Survivors are sorted by ascending complexity so Stage-II
    tries the cheapest symbolic back-substitutions first.
    """
    survivors = []
    for candidate, block in plain_candidates:
        info = _inspect_candidate(candidate, x)
        u = info.get("u")
        if u is None or not info["allowed"]:
            continue
        if not (x in u.free_symbols or t in u.free_symbols):
            continue
        if not info["closure_ok"]:
            continue
        if info["complexity"] > STAGE1_MAX_COMPLEXITY:
            continue
        survivors.append((candidate, block, info))
    survivors.sort(key=lambda item: item[2]["complexity"])
    return survivors


def stage_one(
        spec: PDESpec,
        n_samples: int,
        seed: int,
        n_seeds: int = 5,
        widths: list[int] | None = None,
        max_candidates: int = STAGE1_MAX_CANDIDATES,
):
    """Build and prefilter the prior-free NNSCA candidate pool for Stage-II.

    No numeric residual ranking and no top-k truncation are applied: every
    structurally admissible candidate goes to the exact symbolic Stage-II, where
    the existing complexity and timeout budgets decide its fate.
    """
    widths = list(widths or [1])
    print("=" * 70)
    print(f"STAGE I: NNSCA layer-wise construction for {spec.name} (structural prefilter)")
    print("=" * 70)

    x, t = sp.symbols("x t")
    plain = _nnsca_role_candidates(
        spec, n_samples, seed, widths, n_seeds=n_seeds, max_candidates=max_candidates
    )
    survivors = _prefilter_candidates(spec, plain, x, t)
    print(
        f"nnsca-general: {len(plain)} built -> {len(survivors)} passed structural prefilter"
    )

    groups = [{
        "name": "nnsca-general",
        "seed_code": None,
        "members": [(candidate, block) for candidate, block, _info in survivors],
    }]
    best_expr = survivors[0][0] if survivors else None
    if best_expr is not None:
        print("first Stage-II candidate (cheapest):")
        print(f"  {best_expr}")
    return best_expr, None, groups


def _dedupe_coeffs(coeffs):
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
    return equations


def _maple_coeff_equations(residual, variable_coefficient: bool = False):
    """Return coefficient equations from a PDE residual in Maple's style.

    Pure rational residuals are cleared and treated as polynomials in x,t.  For
    transcendental residuals the independent functions are replaced bottom-up
    by fresh symbols.  Any surviving x,t are also kept as polynomial generators,
    so non-travelling-wave phases and time-dependent coefficients survive into
    the coefficient system.
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
                # Replace every bottom-level function, including functions of
                # unresolved parameters.  The previous x,t-only relevance test
                # left exp(p9) inside tanh(...), which made sp.Poly treat a
                # generator as part of a transcendental argument.
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
            poly_symbols.extend([x, t])

        if not poly_symbols:
            coeffs = [] if sp.expand(residual) == 0 else [residual]
        else:
            poly = sp.Poly(sp.expand(residual), *poly_symbols)
            coeffs = []
            for coeff in poly.coeffs():
                num, _den = sp.fraction(sp.together(coeff))
                coeffs.append(sp.expand(num))

    equations = _dedupe_coeffs(coeffs)
    return equations, basis


def _sech_tanh_coeff_equations(residual, variable_coefficient: bool = False):
    """Extract coefficient equations for one or more sech/tanh phases.

    Even powers of ``sech`` are rewritten through ``sech^2 = 1 - tanh^2``
    before ``tanh(theta_i)`` becomes an independent generator ``T_i``.  This
    keeps distinct travelling-wave phases independent instead of treating
    sech and tanh as one basis, which produced spurious constraints.
    """
    x, t = sp.symbols("x t")
    residual = sp.together(residual)
    numerator, _denominator = sp.fraction(residual)
    expr = sp.expand(numerator)

    phases = []
    for atom in expr.atoms(sp.Function):
        if atom.func not in (sp.tanh, sp.sech):
            continue
        if any(arg.has(sp.Function) for arg in atom.args):
            continue
        theta = atom.args[0]
        if theta not in phases:
            phases.append(theta)
    if not phases:
        return None

    generators = [sp.Symbol(f"__T{i}") for i in range(len(phases))]
    for theta, tt in zip(phases, generators):
        expr = expr.replace(
            lambda e: (
                e.is_Pow
                and e.base == sp.sech(theta)
                and e.exp.is_Integer
                and e.exp >= 2
                and e.exp % 2 == 0
            ),
            lambda e: (1 - tt ** 2) ** (e.exp // 2),
        )
        if expr.has(sp.sech(theta)):
            return None
        expr = sp.expand(expr.replace(sp.tanh(theta), tt))

    if expr.has(sp.tanh, sp.sech):
        return None

    poly_symbols = list(generators)
    if expr.has(x) or expr.has(t):
        poly_symbols.extend([x, t])
    try:
        poly = sp.Poly(sp.expand(expr), *poly_symbols)
    except sp.PolynomialError:
        return None

    equations = _dedupe_coeffs(poly.coeffs())
    return equations, generators



def _extract_coeff_equations(residual, variable_coefficient: bool = False):
    """Try multi-phase sech/tanh extraction, then fall back to Maple-style."""
    sech_tanh = _sech_tanh_coeff_equations(
        residual, variable_coefficient=variable_coefficient
    )
    if sech_tanh is not None:
        if len(sech_tanh[0]) > MAX_COEFF_EQUATIONS:
            raise ValueError("too many coefficient equations to solve safely")
        return sech_tanh
    extracted = _maple_coeff_equations(
        residual, variable_coefficient=variable_coefficient
    )
    if len(extracted[0]) > MAX_COEFF_EQUATIONS:
        raise ValueError("too many coefficient equations to solve safely")
    return extracted


def _residual_is_zero(expr: sp.Expr) -> bool:
    """Certificate check for a fully substituted residual."""
    if expr == 0:
        return True

    # Rational cancellation catches polynomial/rational and most exponential cases.
    try:
        expr = sp.expand(sp.together(expr))
        if expr == 0:
            return True
    except Exception:
        pass

    # Even powers of sech are rewritten through sech^2 = 1 - tanh^2.  This is an
    # identity-preserving rewrite and is what proves classical sech solitons zero
    # without invoking SymPy's expensive trigsimp.
    expr = expr.replace(
        lambda e: (
            e.is_Pow
            and e.base.func is sp.sech
            and e.exp.is_Integer
            and e.exp >= 2
            and e.exp % 2 == 0
        ),
        lambda e: (1 - sp.tanh(e.base.args[0]) ** 2) ** (e.exp // 2),
    )
    try:
        if sp.expand(sp.together(expr)) == 0:
            return True
    except Exception:
        pass

    # A final, deliberately small general simplification handles trig/exponential
    # identities that the two targeted passes above cannot reach.  The caller wraps
    # this function in a short timeout, so pathological expressions are bounded.
    if sp.count_ops(expr) <= 300 and not expr.has(sp.tanh, sp.sech):
        try:
            if sp.simplify(expr) == 0:
                return True
        except Exception:
            pass
    return False


def _residual_numeric_zero(expr: sp.Expr, x: sp.Symbol, t: sp.Symbol, tol: float = 1e-8) -> bool:
    """Cheap numerical prefilter for a candidate residual."""
    free = [sym for sym in expr.free_symbols if sym not in (x, t)]
    if free:
        # Numeric probing is unreliable when unresolved parameters remain;
        # the bounded symbolic check in the caller is the real certificate.
        return True
    rng = random.Random(20261119)
    points = [(-1.1, 0.3), (0.4, -0.7), (0.9, 1.2), (-0.2, 0.8)]
    for _ in range(4):
        subs = {sym: rng.uniform(-2.0, 2.0) for sym in free}
        for xv, tv in points:
            try:
                value = complex(expr.subs({x: xv, t: tv, **subs}).evalf())
                if not np.isfinite(value.real) or not np.isfinite(value.imag):
                    return True
                if abs(value) > tol:
                    return False
            except Exception:
                return True
    return True


def _classify_momentum(spec: PDESpec, expr: sp.Expr, constraints: dict):
    """Classify a verified exact branch by the PDE momentum in ``spec.momentum``.

    Returns ``(category, reduced_momentum)``.  The category is
    ``zero_momentum`` only when the reduced momentum is identically zero after
    substituting the branch constraints; otherwise it is ``nonzero_momentum``.
    """
    if spec.momentum is None:
        return "unclassified", None

    x, t = sp.symbols("x t")
    try:
        momentum = spec.momentum(expr, x, t)
        reduced = sp.expand(momentum.subs(constraints))
    except Exception:
        return "unknown", None

    simplified, simplify_error = _ch._call_with_timeout(
        lambda: sp.simplify(reduced), STAGE2_VERIFY_TIMEOUT
    )
    if simplify_error is not None:
        # If the bounded simplify timed out, fall back to exact rational zero.
        try:
            is_zero = sp.expand(sp.together(reduced)) == 0
        except Exception:
            is_zero = False
        if is_zero:
            return "zero_momentum", reduced
        return "unknown", reduced

    category = "zero_momentum" if simplified == 0 else "nonzero_momentum"
    return category, simplified


_TRANSCENDENTAL_FUNCS = (
    sp.tanh, sp.sech, sp.exp, sp.sin, sp.cos, sp.sinh, sp.cosh, sp.tan
)


def _phase_variable_part(theta: sp.Expr, x: sp.Symbol, t: sp.Symbol) -> sp.Expr:
    """Return the x,t-dependent part of a phase argument.

    A pure constant shift is a symmetry of every autonomous travelling-wave
    phase, so branches differing only by ``cos(p13)``, ``sin(p5)`` or an
    explicit ``p9`` offset collapse to the same structural family.
    """
    theta = sp.expand(theta)
    terms = sp.Add.make_args(theta)
    keep = [term for term in terms if term.free_symbols & {x, t}]
    return sp.Add(*keep) if keep else sp.Integer(0)


def _canonical_branch_expr(expr: sp.Expr, x: sp.Symbol, t: sp.Symbol) -> sp.Expr:
    """Canonical form used only for deduplicating parameter-equivalent branches.

    The returned expression is not meant for display: constant phase offsets are
    removed and free parameters are alpha-renamed by first appearance so that
    ``p6*p7*tanh(p6*p7*x + ...)`` and ``p10*p11*tanh(p10*p11*x + ...)`` share
    one key.
    """
    e = sp.expand(expr)
    for _ in range(12):
        changed = False
        atoms = sorted(
            e.atoms(sp.Function), key=lambda a: (sp.count_ops(a), sp.srepr(a))
        )
        for atom in atoms:
            if (
                atom.func in _TRANSCENDENTAL_FUNCS
                and len(atom.args) == 1
                and not atom.args[0].has(sp.Function)
            ):
                phase = _phase_variable_part(atom.args[0], x, t)
                new = atom.func(phase)
                if new != atom:
                    e = e.subs(atom, new)
                    changed = True
        if not changed:
            break
    e = sp.expand(sp.together(e))
    free = []
    for node in sp.preorder_traversal(e):
        if node.is_Symbol and node not in (x, t) and node not in free:
            free.append(node)
    mapping = {sym: sp.Symbol(f"__q{i}") for i, sym in enumerate(free)}
    return e.subs(mapping)


def _dedupe_exact_solutions(exact_solutions):
    """Collapse parameter-equivalent branches across different candidates.

    Exact branches are already sorted by the caller, so the first kept item is
    the preferred representative of each canonical family.
    """
    x, t = sp.symbols("x t")
    seen = set()
    unique = []
    for item in exact_solutions:
        try:
            key = sp.srepr(_canonical_branch_expr(item[3]["exact_expr"], x, t))
        except Exception:
            key = sp.srepr(item[3]["exact_expr"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def _is_affine_polynomial(expr: sp.Expr, x: sp.Symbol, t: sp.Symbol) -> bool:
    """True when an exact branch is only an affine function of x and t."""
    try:
        if expr.atoms(sp.Function):
            return False
        poly = sp.Poly(sp.expand(sp.together(expr)), x, t)
        return poly.total_degree() <= 1
    except Exception:
        return False


def _solution_signature(expr: sp.Expr, x: sp.Symbol, t: sp.Symbol) -> dict:
    """Describe how structurally distinct an exact branch is."""
    funcs = expr.atoms(sp.Function)
    types = {atom.func for atom in funcs if atom.func is not sp.Function}
    phases = set()
    for atom in funcs:
        if atom.func in _TRANSCENDENTAL_FUNCS and len(atom.args) == 1:
            try:
                phases.add(sp.srepr(sp.together(_phase_variable_part(atom.args[0], x, t))))
            except Exception:
                phases.add(sp.srepr(atom.args[0]))
    try:
        terms = len(sp.Add.make_args(expr))
    except Exception:
        terms = 1
    return {
        "types": len(types),
        "phases": len(phases),
        "terms": terms,
        "ops": int(sp.count_ops(expr)),
    }


def _factor_list(eq):
    eq = sp.expand(sp.together(eq))
    try:
        factored = sp.factor(eq)
    except Exception:
        factored = eq
    factors = []
    for atom in sp.Mul.make_args(factored):
        if atom.is_number:
            continue
        factors.append(sp.expand(atom))
    seen = set()
    unique = []
    for atom in factors:
        key = sp.srepr(atom)
        if key not in seen:
            seen.add(key)
            unique.append(atom)
    return unique


def _solve_factored_cases(equations, unknowns, timeout):
    """Solve product-form coefficient systems by branching on univariate factors.

    PDE coefficient systems often factor as ``p1*p2*(1-p2**2)``.  SymPy's
    default Groebner path is very slow on these, while ``manual=True`` often
    returns only the zero-weight branches.  This fallback enumerates the
    single-variable factors (``p2=0,1,-1``) so the mixed-sign nonlinear
    branches are not lost.
    """
    deadline = time.time() + timeout
    solutions = []

    def _remaining(assignment):
        remaining = []
        for eq in equations:
            value = sp.simplify(sp.expand(eq.subs(assignment)))
            if value == 0:
                continue
            if value.is_number:
                return None
            remaining.append(value)
        return remaining

    def _walk(assignment, depth):
        if len(solutions) >= 600 or time.time() > deadline or depth > 40:
            return
        remaining = _remaining(assignment)
        if remaining is None:
            return
        if not remaining:
            solutions.append(dict(assignment))
            return

        best = None
        for eq in remaining:
            facs = _factor_list(eq)
            univariate = sum(
                1 for fac in facs if sum(1 for u in unknowns if fac.has(u)) == 1
            )
            key = (-univariate, len(facs), sp.count_ops(eq))
            if best is None or key < best[0]:
                best = (key, eq, facs)
        _key, eq, facs = best

        branched = False
        for fac in facs:
            vars_in = [u for u in unknowns if fac.has(u)]
            if len(vars_in) != 1:
                continue
            variable = vars_in[0]
            try:
                roots = sp.solve(fac, variable)
            except Exception:
                roots = []
            for root in roots:
                next_assignment = dict(assignment)
                next_assignment[variable] = sp.simplify(root)
                _walk(next_assignment, depth + 1)
                branched = True
                if len(solutions) >= 600 or time.time() > deadline:
                    return

        if not branched:
            try:
                solved = sp.solve(
                    eq, [u for u in unknowns if u not in assignment],
                    dict=True, simplify=False, manual=True,
                )
            except Exception:
                solved = []
            for partial in solved:
                next_assignment = dict(assignment)
                next_assignment.update({k: v for k, v in partial.items() if isinstance(k, sp.Symbol)})
                _walk(next_assignment, depth + 1)
                if len(solutions) >= 600 or time.time() > deadline:
                    break

    _walk({}, 0)

    valid = []
    for solution in solutions:
        if all(sp.simplify(eq.subs(solution)) == 0 for eq in equations):
            valid.append(solution)

    unique = []
    seen = set()
    for solution in valid:
        key = tuple(sorted((sp.srepr(k), sp.srepr(v)) for k, v in solution.items()))
        if key not in seen:
            seen.add(key)
            unique.append(solution)
    return unique


def _solve_coefficient_system(equations, unknowns, timeout):
    """Solve a PDE coefficient system with the fastest reliable solver first."""
    solved = []
    last_error = None

    factored = _solve_factored_cases(equations, unknowns, timeout)
    if factored:
        solved.extend(factored)

    manual_result, manual_error = _ch._call_with_timeout(
        lambda: sp.solve(equations, unknowns, dict=True, simplify=False, manual=True),
        timeout,
    )
    if manual_error is None and manual_result:
        solved.extend(manual_result)
    elif manual_error:
        last_error = f"manual sp.solve {manual_error}"

    full_result, full_error = _ch._call_with_timeout(
        lambda: sp.solve(equations, unknowns, dict=True, simplify=False),
        timeout,
    )
    if full_error is None and full_result:
        solved.extend(full_result)
    elif full_error:
        last_error = last_error or f"full sp.solve {full_error}"

    def _run_nonlinear():
        result = sp.nonlinsolve(equations, unknowns)
        if not isinstance(result, sp.FiniteSet):
            return None
        solutions = []
        for item in result:
            if isinstance(item, dict):
                solutions.append(item)
            elif isinstance(item, (tuple, list)) and len(item) == len(unknowns):
                solutions.append(dict(zip(unknowns, item)))
        return solutions or None

    nonlinear_result, nonlinear_error = _ch._call_with_timeout(
        _run_nonlinear, timeout
    )
    if nonlinear_error is None and nonlinear_result:
        solved.extend(nonlinear_result)
    elif nonlinear_error:
        last_error = last_error or f"nonlinsolve {nonlinear_error}"

    if solved:
        unique = []
        seen = set()
        for solution in solved:
            try:
                key = tuple(sorted(
                    (sp.srepr(k), sp.srepr(v)) for k, v in solution.items()
                ))
            except Exception:
                key = sp.srepr(solution)
            if key not in seen:
                seen.add(key)
                unique.append(solution)
        # Verify structurally richer branches first: fewer amplitudes forced to
        # zero means more of the ansatz survives, which is where new solutions
        # live.  This also keeps trivial zero-weight families from starving the
        # Stage-II solution budget.
        unique.sort(key=lambda s: (
            sum(1 for v in s.values() if v == 0),
            -len(s),
        ))
        return unique, None

    return None, last_error


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
            direct_residual = spec.residual(direct_f, x, t).subs(_pde_default_substitutions(spec))
            if _residual_numeric_zero(direct_residual, x, t):
                direct_ok, direct_error = _ch._call_with_timeout(
                    lambda: _residual_is_zero(direct_residual),
                    STAGE2_VERIFY_TIMEOUT,
                )
            else:
                direct_ok, direct_error = False, None
            if direct_error is None and direct_ok:
                sig = _solution_signature(direct_f, x, t)
                branch = {
                    "exact_expr": direct_f,
                    "constraints": {},
                    "residual": sp.Integer(0),
                    "affine_trivial": _is_affine_polynomial(direct_f, x, t),
                    **sig,
                }
                momentum_category, momentum_expr = _classify_momentum(
                    spec, direct_f, _pde_default_substitutions(spec)
                )
                branch["momentum_category"] = momentum_category
                branch["momentum_expr"] = momentum_expr
                momentum_raw_category, momentum_raw_expr = _classify_momentum(
                    spec, direct_f, {}
                )
                branch["momentum_category_raw"] = momentum_raw_category
                branch["momentum_expr_raw"] = momentum_raw_expr
                return {"status": "exact", "branches": [branch], "message": "expression is an exact solution"}
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
        extraction, extract_error = _ch._call_with_timeout(
            lambda: _extract_coeff_equations(
                residual, variable_coefficient=spec.variable_coefficient
            ),
            STAGE2_EXTRACT_TIMEOUT,
        )
        if extract_error:
            return {
                "status": "timeout" if extract_error == "timeout" else "unsupported",
                "message": f"coefficient extraction {extract_error}",
                "parameterized_expr": sym_expr,
                "residual": residual,
            }
        equations, basis = extraction

        unknowns = list(params) + list(spec.pde_parameters.values())
        if not equations:
            certified, verify_error = _ch._call_with_timeout(
                lambda: _residual_is_zero(residual), STAGE2_VERIFY_TIMEOUT
            )
            if verify_error is None and certified:
                if x in f.free_symbols or t in f.free_symbols:
                    sig = _solution_signature(f, x, t)
                    branch = {
                        "exact_expr": f,
                        "constraints": {},
                        "residual": sp.Integer(0),
                        "affine_trivial": _is_affine_polynomial(f, x, t),
                        **sig,
                    }
                    momentum_category, momentum_expr = _classify_momentum(
                        spec, f, _pde_default_substitutions(spec)
                    )
                    branch["momentum_category"] = momentum_category
                    branch["momentum_expr"] = momentum_expr
                    momentum_raw_category, momentum_raw_expr = _classify_momentum(
                        spec, f, {}
                    )
                    branch["momentum_category_raw"] = momentum_raw_category
                    branch["momentum_expr_raw"] = momentum_raw_expr
                    return {"status": "exact", "branches": [branch], "message": "residual is identically zero for all parameters"}
                return {
                    "status": "no_solution",
                    "message": "residual is identically zero but the ansatz is x,t-independent",
                }
            if verify_error:
                return {
                    "status": "timeout" if verify_error == "timeout" else "unsupported",
                    "message": f"residual certification {verify_error}",
                    "parameterized_expr": sym_expr,
                    "residual": residual,
                }
            return {
                "status": "no_solution",
                "message": "empty coefficient system with nonzero residual",
            }

        solutions, solve_error = _solve_coefficient_system(
            equations, unknowns, STAGE2_SOLVE_TIMEOUT
        )
        if solve_error:
            return {
                "status": "unsolved",
                "message": f"coefficient solve {solve_error}",
                "parameterized_expr": sym_expr,
                "residual": residual,
                "coefficient_equations": equations,
                "basis": basis,
            }

        if not solutions:
            return {
                "status": "no_solution",
                "message": "sp.solve returned no solutions",
                "residual": residual,
            }

        branches = []
        branch_keys = set()
        pending = []

        found_nontrivial = False
        found_complex = False
        verification_limited = False
        for solution in solutions[:STAGE2_MAX_SOLUTIONS]:
            clean = {sym: val for sym, val in solution.items() if isinstance(sym, sp.Symbol)}
            if any(val.is_number and sp.im(val) != 0 or val.has(sp.I) for val in clean.values()):
                found_complex = True
                continue
            f_sub = f.subs(clean)
            if x not in f_sub.free_symbols and t not in f_sub.free_symbols:
                continue
            if not _ch._probe_nonconstant_solution(f_sub, x, t):
                continue
            found_nontrivial = True
            # Back-substitute the concrete branch expression itself; this is the
            # certificate that must be zero before a branch is reported exact.
            candidate_residual = spec.residual(f_sub, x, t)
            # PDE-level symbols (for example k in CH) live in the residual but
            # not in the ansatz f_sub; apply any solved relations for them.
            pde_sub = {
                sym: val
                for sym, val in clean.items()
                if sym in spec.pde_parameters.values()
            }
            if pde_sub:
                candidate_residual = candidate_residual.subs(pde_sub)
            if not _residual_numeric_zero(candidate_residual, x, t):
                continue
            verdict, verify_error = _ch._call_with_timeout(
                lambda: _residual_is_zero(candidate_residual),
                STAGE2_VERIFY_TIMEOUT,
            )
            if verify_error:
                verification_limited = True
                continue
            if not verdict:
                continue
            pending.append((f_sub, clean))

        # Keep the cleanest representative of each parameter-equivalent family.
        pending.sort(key=lambda item: (sp.count_ops(item[0]), sp.srepr(item[0])))
        for f_sub, clean in pending:
            key = sp.srepr(_canonical_branch_expr(f_sub, x, t))
            if key in branch_keys:
                continue
            branch_keys.add(key)
            sig = _solution_signature(f_sub, x, t)
            branches.append({
                "exact_expr": f_sub,
                "constraints": clean,
                "residual": sp.Integer(0),
                "affine_trivial": _is_affine_polynomial(f_sub, x, t),
                **sig,
            })
            momentum_category, momentum_expr = _classify_momentum(spec, f_sub, clean)
            branches[-1]["momentum_category"] = momentum_category
            branches[-1]["momentum_expr"] = momentum_expr
            momentum_raw_category, momentum_raw_expr = _classify_momentum(spec, f_sub, {})
            branches[-1]["momentum_category_raw"] = momentum_raw_category
            branches[-1]["momentum_expr_raw"] = momentum_raw_expr

        if branches:
            return {
                "status": "exact",
                "branches": branches,
                "message": "exact solutions verified by back-substitution",
            }


        if not found_nontrivial and found_complex:
            return {
                "status": "complex_only",
                "message": "nontrivial solutions found only with complex-valued parameters; skipped",
                "residual": residual,
            }
        if found_nontrivial:
            if verification_limited:
                return {
                    "status": "unverified",
                    "message": "nontrivial parameter branches found but some residuals were too expensive to certify within the verification budget",
                    "parameterized_expr": sym_expr,
                    "residual": residual,
                }
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

    return _solve_candidate()


def _print_candidate_structures(spec: PDESpec, groups):
    print("=" * 70)
    print("STAGE II SKIPPED: candidate structures for manual verification")
    print("=" * 70)
    ranked = []
    for group in groups:
        name = group["name"]
        seed_code = group["seed_code"]
        header = name if seed_code is None else f"seed {name} (first-layer code {seed_code})"
        print(f"--- {header} ---")
        scores = group.get("scores")
        members = list(group["members"])
        for rank, member in enumerate(members, start=1):
            expr, codes = member
            try:
                parameterized, _params = _ch.numerics_to_symbols(expr)
            except Exception as exc:
                parameterized = f"<numerics_to_symbols failed: {exc}>"
            score_note = "" if scores is None else f" score={scores[rank - 1]:.6e}"
            print(f"candidate #{rank} codes={codes}{score_note}")
            print(f"  numeric: {expr}")
            print(f"  parameterized: {parameterized}")
            ranked.append((rank, header, rank, expr))

    top_n = min(3, len(ranked))
    if top_n:
        print("=" * 70)
        print(f"FIRST {top_n} CANDIDATES (CHEAPEST FIRST)")
        print("=" * 70)
        for idx, (_order, header, rank, expr) in enumerate(ranked[:top_n], start=1):
            print(f"[{idx}] {header} / candidate #{rank}")
            print(f"  maple: {expr}")

def _export_maple_candidates(spec: PDESpec, groups, path: str):
    """Write parameterized ansatz skeletons for Maple's coeffs/collect/solve.

    The file intentionally contains symbolic expressions, not Stage-I numeric
    optima: Maple should solve the free parameters p0, p1, ... exactly.
    """
    out_path = Path(path).expanduser()
    total = 0
    with out_path.open("w", encoding="utf-8") as handle:
        handle.write(f"# {spec.name} candidate ansatz for Maple (coeffs + collect + solve)\n")
        for group in groups:
            name = group["name"]
            seed_code = group["seed_code"]
            header = name if seed_code is None else f"seed {name} (first-layer code {seed_code})"
            handle.write(f"\n# --- {header} ---\n")
            for rank, (expr, codes) in enumerate(group["members"], start=1):
                try:
                    parameterized, _params = _ch.numerics_to_symbols(expr)
                except Exception:
                    continue
                code_note = f"  # codes={codes}" if isinstance(codes, list) else ""
                handle.write(f"u[{rank}] := {parameterized};{code_note}\n")
                total += 1
    print("=" * 70)
    print(f"MAPLE EXPORT: {total} parameterized candidates -> {out_path}")
    print("=" * 70)


def _write_unsolved_maple(spec: PDESpec, unsolved):
    """Persist candidates whose coefficient system SymPy could not solve.

    These are not discarded: they are written alongside their extracted
    coefficient equations so Maple's ``coeffs``/``solve`` can finish the exact
    branch derivation without redoing the symbolic differentiation.
    """
    if not unsolved:
        return
    safe_name = re.sub(r"[^0-9A-Za-z_.-]+", "_", spec.name).strip("_") or "pde"
    out_path = Path.cwd() / f"{safe_name}_unsolved_maple.txt"
    written = 0
    with out_path.open("w", encoding="utf-8") as handle:
        handle.write(f"# {spec.name}: candidates whose coefficient system SymPy could not solve\n")
        handle.write("# Solve the parameters p0, p1, ... from these equations, then back-substitute.\n")
        for header, rank, codes, symbolic in unsolved:
            expr = symbolic.get("parameterized_expr")
            if not expr:
                continue
            handle.write(f"\n# --- {header} / candidate #{rank} (codes={codes}) ---\n")
            handle.write(f"u := {expr.replace('**', '^')};\n")
            equations = symbolic.get("coefficient_equations") or []
            if equations:
                handle.write("# coefficient equations (each must be zero)\n")
                for idx, eq in enumerate(equations, start=1):
                    handle.write(f"eq[{idx}] := {sp.sstr(eq).replace('**', '^')};\n")
            handle.write(f"# reason: {symbolic.get('message', 'unknown')}\n")
            written += 1
    print("=" * 70)
    print(f"UNSOLVED MAPLE EXPORT: {written} candidate(s) -> {out_path}")
    print("=" * 70)


def _write_exact_solutions(spec: PDESpec, exact_solutions, path: Path, label: str = "verified"):
    """Persist exact branches with momentum classification to a caller-chosen path.

    The caller passes distinct pre-filter and post-filter paths so no existing
    result is overwritten.  Returns a category count dict.
    """
    out_path = Path(path).expanduser()
    if not exact_solutions:
        with out_path.open("w", encoding="utf-8") as handle:
            handle.write(f"# {spec.name}: {label} exact solutions with momentum classification\n")
            handle.write("# (no branches matched this filter)\n")
        print(f"EXACT SOLUTIONS EXPORT ({label}): 0 branches -> {out_path}")
        return {}
    counts = {}
    with out_path.open("w", encoding="utf-8") as handle:
        handle.write(f"# {spec.name}: {label} exact solutions with momentum classification\n")
        for header, rank, codes, solution in exact_solutions:
            category = solution.get("momentum_category", "unclassified")
            counts[category] = counts.get(category, 0) + 1
            handle.write(f"\n# [{category}] {header} / candidate #{rank} (codes={codes})\n")
            parameterized = solution.get("candidate_expr")
            if parameterized is not None:
                handle.write(f"# parameterized trial: {parameterized}\n")
            handle.write(f"u := {sp.sstr(solution['exact_expr']).replace('**', '^')};\n")
            if solution["constraints"]:
                handle.write("# constraints:\n")
                for sym, val in solution["constraints"].items():
                    handle.write(f"#   {sp.sstr(sym)} = {sp.sstr(val)}\n")
            else:
                handle.write("# constraints: (none)\n")
            momentum = solution.get("momentum_expr")
            if momentum is not None:
                handle.write(f"# m = {sp.sstr(momentum).replace('**', '^')}\n")
            raw_momentum = solution.get("momentum_expr_raw")
            if raw_momentum is not None:
                handle.write(f"# m_raw = {sp.sstr(raw_momentum).replace('**', '^')}\n")
    print("=" * 70)
    print(f"EXACT SOLUTIONS EXPORT ({label}): {len(exact_solutions)} -> {out_path}")
    print("  momentum classification: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print("=" * 70)
    return counts


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
    parser.add_argument("--max-candidates", type=int, default=None, help="Stage I candidate cap (default is engine-wide)")
    parser.add_argument(
        "--momentum-filter",
        choices=["all", "zero", "nonzero"],
        default="all",
        help="keep only exact branches whose momentum category matches",
    )
    parser.add_argument("--maple-export", default=None, help="write parameterized candidates to this file and skip Stage II")
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
        _expr, _codes, groups = stage_one(
            spec,
            args.n_samples,
            args.seed,
            n_seeds=args.n_seeds,
            widths=widths,
            max_candidates=args.max_candidates or STAGE1_MAX_CANDIDATES,
        )

    if args.maple_export:
        _export_maple_candidates(spec, groups, args.maple_export)
        return

    if not args.stage2:
        _print_candidate_structures(spec, groups)
        return

    print("=" * 70)
    print(f"STAGE II: symbolic back-substitution for {spec.name}")
    print("=" * 70)

    reasons = []
    exact_solutions = []
    unsolved = []
    for group in groups:
        group_name = group["name"]
        seed_code = group["seed_code"]
        header = group_name if seed_code is None else f"seed {group_name} (first-layer code {seed_code})"
        print(f"--- {header} ---")
        for rank, (symbolic_expr, symbolic_codes) in enumerate(group["members"], start=1):
            print(f"  candidate #{rank} (codes={symbolic_codes}) solving symbolically...", flush=True)
            symbolic = symbolic_stage_two(spec, symbolic_expr, symbolic_codes, problem)
            if symbolic["status"] == "exact":
                branches = symbolic.get("branches", [])
                for branch in branches:
                    branch.setdefault("candidate_expr", symbolic_expr)
                    exact_solutions.append((header, rank, symbolic_codes, branch))
                print(f"  candidate #{rank} (codes={symbolic_codes}) exact; collected {len(branches)} branch(es)")
            else:
                message = f"{header} #{rank}: {symbolic['message']}"
                reasons.append(message)
                print(f"  candidate #{rank} not exact: {symbolic['message']}")
                if symbolic["status"] in {"unsolved", "timeout", "unverified"}:
                    unsolved.append((header, rank, symbolic_codes, symbolic))

    _write_unsolved_maple(spec, unsolved)
    if exact_solutions:
        total_candidates = sum(len(group["members"]) for group in groups)
        verified_candidates = len({(item[0], item[1]) for item in exact_solutions})
        verified_branches_raw = len(exact_solutions)

        if spec.momentum is not None:
            exact_solutions.sort(
                key=lambda item: (
                    item[3].get("momentum_category") != "nonzero_momentum",
                    item[3]["affine_trivial"],
                    -item[3]["types"],
                    -item[3]["phases"],
                    -item[3]["terms"],
                    item[3]["ops"],
                )
            )
        else:
            exact_solutions.sort(
                key=lambda item: (
                    item[3]["affine_trivial"],
                    -item[3]["types"],
                    -item[3]["phases"],
                    -item[3]["terms"],
                    item[3]["ops"],
                )
            )

        exact_solutions = _dedupe_exact_solutions(exact_solutions)
        verified_branches = len(exact_solutions)
        momentum_counts = {}
        if spec.momentum is not None:
            for _header, _rank, _codes, solution in exact_solutions:
                category = solution.get("momentum_category", "unclassified")
                momentum_counts[category] = momentum_counts.get(category, 0) + 1

        stamp = time.strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r"[^0-9A-Za-z_.-]+", "_", spec.name).strip("_") or "pde"
        pre_path = Path.cwd() / f"{safe_name}_exact_pre_{stamp}.txt"
        post_path = Path.cwd() / f"{safe_name}_exact_post_{stamp}.txt"
        _write_exact_solutions(spec, exact_solutions, pre_path, label="pre-filter")

        if spec.momentum is not None and args.momentum_filter != "all":
            retained = [item for item in exact_solutions
                        if item[3].get("momentum_category") == args.momentum_filter]
        else:
            retained = list(exact_solutions)
        _write_exact_solutions(spec, retained, post_path, label=f"post-filter({args.momentum_filter})")

        changed = []
        if spec.momentum is not None:
            for item in exact_solutions:
                raw = item[3].get("momentum_category_raw")
                after = item[3].get("momentum_category")
                if raw is not None and after is not None and raw != after:
                    changed.append(item)

        print("=" * 70)
        print("CH momentum search statistics" if spec.momentum is not None else "Search statistics")
        print(f"  total candidates: {total_candidates}")
        print(f"  residual-verified candidates: {verified_candidates}")
        print(f"  residual-verified branches: {verified_branches}")
        print(f"  residual-verified branches (raw): {verified_branches_raw}")
        print(f"  unique solution families after dedup: {verified_branches}")
        if spec.momentum is not None:
            print(f"  zero_momentum: {momentum_counts.get('zero_momentum', 0)}")
            print(f"  nonzero_momentum: {momentum_counts.get('nonzero_momentum', 0)}")
            print(f"  unknown: {momentum_counts.get('unknown', 0)}")
            print(f"  classification changed after constraint substitution: {len(changed)}")
        print(f"  final retained solutions: {len(retained)}")
        print("=" * 70)

        if changed:
            print("分类在约束代入前后发生变化的解（最多展示 10 个）:")
            for item in changed[:10]:
                _header, rank, codes, solution = item
                print(f"  candidate #{rank} codes={codes}: {solution.get('momentum_category_raw')} -> {solution.get('momentum_category')}")
            print("=" * 70)

        if retained:
            print(f"最终保留的精确解：{len(retained)} 个")
            for idx, (header, rank, solution_codes, solution) in enumerate(retained, start=1):
                tag = "  [affine-trivial]" if solution["affine_trivial"] else ""
                if spec.momentum is not None:
                    tag += f"  [{solution.get('momentum_category', 'unclassified')}]"
                print(f"[{idx}/{len(retained)}] 来源：{header} / 候选 #{rank}，codes={solution_codes}{tag}")
                print(f"  u(x, t) = {sp.sstr(solution['exact_expr'])}")
                if spec.momentum is not None and solution.get("momentum_expr") is not None:
                    print(f"  m(x, t) = {sp.sstr(solution['momentum_expr'])}")
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

        if args.momentum_filter != "all" and exact_solutions:
            filtered_out = [item for item in exact_solutions
                            if item[3].get("momentum_category") != args.momentum_filter]
            show_n = min(10, len(filtered_out))
            print("=" * 70)
            print(f"没有找到 {args.momentum_filter} 解。以下展示 {show_n} 个被筛除的代表性候选解:")
            print("=" * 70)
            for item in filtered_out[:show_n]:
                header, rank, codes, solution = item
                print(f"[候选 #{rank}] 来源={header} codes={codes} category={solution.get('momentum_category')}")
                print(f"  原始试探函数(parameterized): {solution.get('candidate_expr')}")
                print(f"  u(x, t) = {sp.sstr(solution['exact_expr'])}")
                if solution.get("momentum_expr") is not None:
                    print(f"  m(x, t) = {sp.sstr(solution['momentum_expr'])}")
                print("  参数约束:")
                if solution["constraints"]:
                    for sym, val in solution["constraints"].items():
                        print(f"    {sym} = {sp.sstr(val)}")
                else:
                    print("    (无)")
            return

    print("=" * 70)
    print("STAGE II: no exact symbolic solution found")
    print("=" * 70)
    for message in reasons:
        print(f"  - {message}")
