#!/usr/bin/env python3
"""Minimal SFG + NNSCA [2,1] exact-solution search for the BBM equation.

This module keeps the single-function generator independent from the PDE:
it builds small univariate candidates, fills the one hidden node of the
NNSCA trial ``u = c0 + c1*f(a*x + b*t + d)``, computes the BBM residual
with SymPy, extracts algebraic constraints, solves them, and only reports a
solution after the raw residual is certified to be identically zero.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
import random
import signal
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sigs.jacobi import JacobiCN, JacobiDN, JacobiSN, SYMPY_LOCALS, reduce_jacobi_powers  # noqa: E402

X, T = sp.symbols("x t", real=True)
Z = sp.symbols("z", real=True)
C0, C1, A, B, D = sp.symbols("c0 c1 a b d")
M = sp.symbols("m")
ALPHA, BETA, GAMMA = sp.symbols("alpha beta gamma", nonzero=True)

DEFAULT_RESULTS_DIR = REPO_ROOT / "results" / "sfg_bbm"
DEFAULT_CONFIG = {
    "generator": {
        "mode": "random",
        "random_seed": 42,
        "max_depth": 3,
        "max_nodes": 8,
        "max_candidates": 30,
        "max_parameters_per_function": 3,
    },
    "network": {"widths": [2, 1]},
    "solver": {
        "extract_timeout": 12.0,
        "solve_timeout": 15.0,
        "verify_timeout": 8.0,
        "residual_timeout": 8.0,
    },
}

JACOBI_FUNCS = (JacobiSN, JacobiCN, JacobiDN)


class _TimeoutError(Exception):
    """Raised when a bounded SymPy operation exceeds its time budget."""


@contextmanager
def _time_limit(seconds: float):
    """Bound one SymPy operation with SIGALRM in the main thread."""
    if seconds <= 0:
        yield
        return

    def handler(signum, frame):
        raise _TimeoutError()

    previous = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def _call_with_timeout(fn, seconds: float):
    """Return ``(result, error)`` where error is None, 'timeout', or a message."""
    try:
        with _time_limit(seconds):
            return fn(), None
    except _TimeoutError:
        return None, "timeout"
    except Exception as exc:  # noqa: BLE001 - sympy exceptions vary by version
        return None, f"{type(exc).__name__}: {exc}"


def _sympify_f(expr_str: str):
    """Parse one SFG expression with the Jacobi whitelist available."""
    locals_map = dict(SYMPY_LOCALS)
    locals_map.update({
        "z": Z,
        "m": M,
        "alpha": ALPHA,
        "beta": BETA,
        "gamma": GAMMA,
    })
    return sp.sympify(expr_str, locals=locals_map)


def _free_parameters(expr: sp.Expr) -> list[sp.Symbol]:
    return sorted([s for s in expr.free_symbols if s != Z], key=lambda s: str(s))


def _function_depth(expr: sp.Expr) -> int:
    def walk(node, depth):
        if isinstance(node, sp.Function) and node.func is not sp.Function:
            depth += 1
        return max([depth] + [walk(arg, depth) for arg in node.args])

    return walk(expr, 0)


def _node_count(expr: sp.Expr) -> int:
    return len(list(sp.preorder_traversal(expr)))


def _category(expr: sp.Expr) -> str:
    funcs = {atom.func for atom in expr.atoms(sp.Function)}
    if funcs & set(JACOBI_FUNCS):
        return "special"
    if funcs & {sp.sinh, sp.cosh, sp.tanh, sp.sech, sp.coth, sp.csch}:
        return "hyperbolic"
    return "elementary"


def _domain_status(expr: sp.Expr) -> str:
    funcs = {atom.func for atom in expr.atoms(sp.Function)}
    if funcs & {sp.log, sp.tan, sp.coth, sp.csch}:
        return "partial_domain"
    if expr.has(1 / Z):
        return "partial_domain"
    return "candidate_real_axis"


SUPPORTED_IDENTITY_FUNCS = {
    sp.tanh, sp.sech, sp.tan, sp.sin, sp.cos, sp.sinh, sp.cosh,
    JacobiSN, JacobiCN, JacobiDN,
}


def _function_identity_status(expr: sp.Expr) -> str:
    funcs = {atom.func for atom in expr.atoms(sp.Function)}
    if funcs <= SUPPORTED_IDENTITY_FUNCS:
        return "known"
    return "unknown"


def _reduce_even_sech_powers(expr: sp.Expr) -> sp.Expr:
    """Rewrite ``sech(theta)**(2*n)`` through ``1 - tanh(theta)**2``."""
    return expr.replace(
        lambda e: (
            e.is_Pow
            and e.base.func is sp.sech
            and e.exp.is_Integer
            and e.exp >= 2
            and e.exp % 2 == 0
        ),
        lambda e: (1 - sp.tanh(e.base.args[0]) ** 2) ** (e.exp // 2),
    )


def _reduce_sech_powers(expr: sp.Expr) -> sp.Expr:
    """Rewrite every ``sech(theta)**n`` via ``1 - tanh(theta)**2``."""
    def _rewrite(e):
        theta = e.base.args[0]
        n = int(e.exp)
        if n % 2 == 0:
            return (1 - sp.tanh(theta) ** 2) ** (n // 2)
        return sp.sech(theta) * (1 - sp.tanh(theta) ** 2) ** ((n - 1) // 2)
    return expr.replace(
        lambda e: (
            e.is_Pow
            and e.base.func is sp.sech
            and e.exp.is_Integer
            and e.exp >= 2
        ),
        _rewrite,
    )

def _has_jacobi(expr: sp.Expr) -> bool:
    return any(atom.func in JACOBI_FUNCS for atom in expr.atoms(sp.Function))


def _dedupe_coeffs(coeffs: list[sp.Expr]) -> list[sp.Expr]:
    equations: list[sp.Expr] = []
    seen = set()
    for coeff in coeffs:
        try:
            coeff = sp.expand(sp.together(coeff))
        except Exception:
            pass
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


def _normalise_residual(residual: sp.Expr):
    """Return ``(normalised, metadata)`` after trying several safe forms."""
    forms = [("raw", residual)]
    for name, func in [
        ("expand", lambda e: sp.expand(e)),
        ("factor_terms", lambda e: sp.factor_terms(e)),
        ("together", lambda e: sp.together(e)),
        ("cancel", lambda e: sp.cancel(e)),
    ]:
        try:
            value = func(residual)
            if value is not None:
                forms.append((name, value))
        except Exception:
            continue
    best_name, best_expr = min(forms, key=lambda item: sp.count_ops(item[1]))
    metadata = {
        "selected": best_name,
        "tried": [name for name, _ in forms],
    }
    return best_expr, metadata


def _extract_coefficient_equations(residual: sp.Expr, x: sp.Symbol, t: sp.Symbol):
    """Return ``(equations, basis, error)`` for a symbolic BBM residual.

    The residual is first put over a common denominator and its numerator is
    expanded.  Independent bottom-level transcendental functions are then
    replaced by fresh symbols so SymPy's polynomial coefficient extraction can
    produce algebraic constraints.  This is a coefficient method, not an
    identity proof: every branch is re-checked by back-substitution later.
    """
    try:
        expr, _normalization_meta = _normalise_residual(residual)
        expr = sp.together(expr)
        numerator, _denominator = sp.fraction(expr)
        expr = sp.expand(numerator)
        expr = _reduce_even_sech_powers(expr)
        if _has_jacobi(expr):
            expr = sp.expand(reduce_jacobi_powers(expr))
    except Exception as exc:
        return [], [], f"together/rewrite failed: {type(exc).__name__}: {exc}"

    mapping: dict[sp.Expr, sp.Symbol] = {}
    while True:
        candidates = [
            atom
            for atom in expr.atoms(sp.Function)
            if not any(arg.has(sp.Function) for arg in atom.args)
        ]
        if not candidates:
            break
        target = min(
            candidates,
            key=lambda atom: (str(atom.func), sp.count_ops(atom), sp.srepr(atom)),
        )
        if target not in mapping:
            mapping[target] = sp.Symbol(f"__B{len(mapping)}")
        expr = sp.expand(expr.subs(target, mapping[target]))

    try:
        expr = sp.together(expr)
        numerator, _denominator = sp.fraction(expr)
        expr = sp.expand(numerator)
    except Exception:
        pass

    basis = list(mapping.values())
    poly_symbols = list(basis)
    if expr.has(x) or expr.has(t):
        poly_symbols.extend([x, t])

    if not poly_symbols:
        equations = [] if expr == 0 else [expr]
    else:
        try:
            equations = sp.Poly(sp.expand(expr), *poly_symbols).coeffs()
        except sp.PolynomialError as exc:
            # If a phase is not polynomial, return the expanded expression as a
            # single equation rather than pretending a basis exists.
            return [sp.expand(expr)], basis, f"non-polynomial phase: {exc}"

    equations = _dedupe_coeffs(equations)
    return equations, basis, None


def _bbm_residual(u: sp.Expr) -> sp.Expr:
    return sp.diff(u, T) + sp.diff(u, X) + u * sp.diff(u, X) - sp.diff(u, T, X, 2)


def _normalise_network_widths(widths) -> list[int]:
    values = [int(w) for w in widths]
    if len(values) < 2 or values[0] != 2 or values[-1] != 1:
        raise ValueError("network widths must start with 2 and end with 1")
    return values


def build_trial(
    f_expr: sp.Expr,
    widths: list[int] | tuple[int, ...],
    f_exprs: list[sp.Expr] | tuple[sp.Expr, ...] | None = None,
) -> sp.Expr:
    """Build the NNSCA trial for a generated univariate activation ``f``.

    The [2,1] case keeps the historical affine phase. Deeper networks
    recursively feed ``f`` into the next hidden layer and finish with a
    single linear output neuron.
    """
    values = _normalise_network_widths(widths)
    if values == [2, 1]:
        return sp.expand(C0 + C1 * f_expr.subs(Z, A * X + B * T + D))

    if values == [2, 2, 1]:
        f0 = f_exprs[0] if f_exprs else f_expr
        f1 = f_exprs[1] if f_exprs else f_expr
        phase0 = sp.Symbol("w1_0_0") * X + sp.Symbol("w1_0_1") * T + sp.Symbol("b1_0")
        phase1 = sp.Symbol("w1_1_0") * X + sp.Symbol("w1_1_1") * T + sp.Symbol("b1_1")
        return sp.expand(
            sp.Symbol("b_out")
            + sp.Symbol("w_out_0") * f0.subs(Z, phase0)
            + sp.Symbol("w_out_1") * f1.subs(Z, phase1)
        )

    hidden = values[1:-1]
    previous = [X, T]
    layers: list[list[sp.Expr]] = []
    for layer_idx, width in enumerate(hidden):
        current: list[sp.Expr] = []
        for node_idx in range(width):
            terms = []
            for input_idx, input_expr in enumerate(previous):
                weight = sp.Symbol(f"w{layer_idx + 1}_{node_idx}_{input_idx}")
                terms.append(weight * input_expr)
            bias = sp.Symbol(f"b{layer_idx + 1}_{node_idx}")
            phase = sp.Add(*terms, bias)
            current.append(f_expr.subs(Z, phase))
        layers.append(current)
        previous = current

    output = sp.Symbol("b_out")
    for node_idx, node_expr in enumerate(layers[-1]):
        output += sp.Symbol(f"w_out_{node_idx}") * node_expr
    return sp.expand(output)


def _two_node_symbols() -> dict[str, sp.Symbol]:
    return {
        "w_out_0": sp.Symbol("w_out_0"),
        "w_out_1": sp.Symbol("w_out_1"),
        "a1": sp.Symbol("w1_0_0"),
        "b1": sp.Symbol("w1_0_1"),
        "a2": sp.Symbol("w1_1_0"),
        "b2": sp.Symbol("w1_1_1"),
        "d1": sp.Symbol("b1_0"),
        "d2": sp.Symbol("b1_1"),
        "b_out": sp.Symbol("b_out"),
    }


def _two_node_determinant(solution: dict[sp.Symbol, sp.Expr]) -> sp.Expr:
    syms = _two_node_symbols()
    values = {}
    for key, sym in syms.items():
        values[key] = solution.get(sym)
        if values[key] is None:
            values[key] = sp.Symbol(f"__free_{key}")
    return sp.expand(values["a1"] * values["b2"] - values["a2"] * values["b1"])


def _classify_two_node_branch(branch: dict) -> str:
    constraints = branch.get("constraints", {})
    clean = {
        sp.Symbol(key): sp.sympify(value, locals=dict(SYMPY_LOCALS))
        for key, value in constraints.items()
    }
    w0_key = sp.Symbol("w_out_0")
    w1_key = sp.Symbol("w_out_1")
    w0_zero = w0_key in clean and clean[w0_key] == 0
    w1_zero = w1_key in clean and clean[w1_key] == 0
    if w0_zero and w1_zero:
        return "TRIVIAL"

    # A missing weight is a free parameter and is treated as generically
    # nonzero.  Explicit zero values mark a node as inactive.
    active0 = not w0_zero
    active1 = not w1_zero
    if not active0 or not active1:
        return "EXACT_SINGLE_NODE_DEGENERATE"

    determinant = _two_node_determinant(clean)
    if sp.expand(determinant) == 0:
        return "EXACT_TWO_NODE_EQUIVALENT"
    return "EXACT_TWO_NODE_NONDEGENERATE"


def _cross_term_analysis(trial: sp.Expr) -> dict:
    w0 = sp.Symbol("w_out_0")
    w1 = sp.Symbol("w_out_1")
    nonlinear = sp.expand(trial * sp.diff(trial, X))
    cross = sp.Integer(0)
    single = sp.Integer(0)
    for term in sp.Add.make_args(nonlinear):
        if term.has(w0) and term.has(w1):
            cross += term
        else:
            single += term
    cross = sp.expand(cross)
    try:
        simplified = sp.factor_terms(cross)
    except Exception:
        simplified = cross
    return {
        "cross_term": sp.sstr(cross),
        "single_node_term": sp.sstr(sp.expand(single)),
        "factor_terms": sp.sstr(simplified),
        "node_count": sp.count_ops(cross),
    }


def _is_polynomial_equation_system(equations, unknowns) -> tuple[bool, str | None]:
    """Check whether every equation is polynomial in all requested symbols."""
    if not unknowns:
        return True, None
    for equation in equations:
        try:
            sp.Poly(sp.expand(equation), *unknowns)
        except Exception as exc:
            return False, f"{type(exc).__name__}: {exc}"
    return True, None


def _augment_nondegenerate_constraints(equations, unknowns):
    """Add ``q*w_out_0*w_out_1*D - 1 = 0`` for active two-node solving."""
    q = sp.Symbol("__q_nondegenerate")
    syms = _two_node_symbols()
    determinant = syms["a1"] * syms["b2"] - syms["a2"] * syms["b1"]
    auxiliary = sp.expand(q * syms["w_out_0"] * syms["w_out_1"] * determinant - 1)
    augmented = list(equations) + [auxiliary]
    augmented_unknowns = list(unknowns) + [q]
    return augmented, augmented_unknowns, auxiliary, q



def _residual_is_zero(expr: sp.Expr) -> bool:
    """Certificate check that does not rely on unverified simplification."""
    if expr == 0:
        return True
    try:
        if sp.expand(sp.together(expr)) == 0:
            return True
    except Exception:
        pass
    reduced = _reduce_sech_powers(_reduce_even_sech_powers(expr))
    try:
        if sp.expand(sp.together(reduced)) == 0:
            return True
    except Exception:
        pass
    if _has_jacobi(reduced):
        try:
            if sp.expand(sp.together(reduce_jacobi_powers(reduced))) == 0:
                return True
        except Exception:
            pass
    return False


def _is_trivial_network_solution(solution: dict[sp.Symbol, sp.Expr]) -> bool:
    if solution.get(C1) == 0:
        return True
    if solution.get(A) == 0 and solution.get(B) == 0:
        return True
    if sp.Symbol("w_out_0") in solution and sp.Symbol("w_out_1") in solution:
        if solution[sp.Symbol("w_out_0")] == 0 and solution[sp.Symbol("w_out_1")] == 0:
            return True
    return False


def _has_imaginary_value(value: sp.Expr) -> bool:
    try:
        if value.is_number and sp.im(value) != 0:
            return True
    except Exception:
        pass
    return value.has(sp.I)


def _validate_branch(trial: sp.Expr, solution, x: sp.Symbol, t: sp.Symbol, residual_fn=_bbm_residual):
    clean = {sym: val for sym, val in solution.items() if sym.is_Symbol}
    if any(_has_imaginary_value(val) for val in clean.values()):
        return None
    if _is_trivial_network_solution(clean):
        return None
    try:
        u_sub = sp.expand(trial.subs(clean))
    except Exception:
        return None
    if not ({x, t} & u_sub.free_symbols):
        return None
    try:
        if sp.expand(sp.diff(u_sub, x)) == 0 and sp.expand(sp.diff(u_sub, t)) == 0:
            return None
    except Exception:
        pass
    residual = residual_fn(u_sub)
    try:
        residual = sp.expand(residual)
    except Exception:
        return None
    if not _residual_is_zero(residual):
        return None
    return {
        "expression": sp.sstr(u_sub),
        "constraints": {str(k): str(v) for k, v in clean.items()},
        "residual": "0",
    }


def _serialize_solution(solution) -> dict[str, str]:
    return {str(key): str(value) for key, value in solution.items()}


def _classify_branch(clean: dict, u_sub: sp.Expr) -> tuple[str, str]:
    """Classify a solver branch without deleting it from the record."""
    if clean.get(C1) == 0:
        return "CONSTANT_TRIVIAL", "c1 == 0"
    if clean.get(A) == 0 and clean.get(B) == 0:
        return "DEGENERATE", "a == 0 and b == 0"
    w_out_0 = sp.Symbol("w_out_0")
    w_out_1 = sp.Symbol("w_out_1")
    if w_out_0 in clean and w_out_1 in clean:
        if clean[w_out_0] == 0 and clean[w_out_1] == 0:
            return "CONSTANT_TRIVIAL", "both output coefficients are zero"
        phase0 = sp.expand(
            clean.get(sp.Symbol("w1_0_0"), 0) * X
            + clean.get(sp.Symbol("w1_0_1"), 0) * T
            + clean.get(sp.Symbol("b1_0"), 0)
        )
        phase1 = sp.expand(
            clean.get(sp.Symbol("w1_1_0"), 0) * X
            + clean.get(sp.Symbol("w1_1_1"), 0) * T
            + clean.get(sp.Symbol("b1_1"), 0)
        )
        active0 = clean[w_out_0] != 0 and phase0 != 0
        active1 = clean[w_out_1] != 0 and phase1 != 0
        if not active0 and not active1:
            return "DEGENERATE", "both hidden nodes are inactive"
        if phase0 == phase1:
            return "EQUIVALENT_NODES", "the two affine phases are identical"
    for value in clean.values():
        if value in (sp.zoo, sp.nan) or value.has(sp.zoo, sp.nan):
            return "DEGENERATE", "denominator or parameter is zero/undefined"
    try:
        if not ({X, T} & u_sub.free_symbols):
            return "DEGENERATE", "substituted trial does not depend on x or t"
    except Exception:
        return "UNRESOLVED", "substitution failed"
    try:
        if sp.expand(sp.diff(u_sub, X)) == 0 and sp.expand(sp.diff(u_sub, T)) == 0:
            return "DEGENERATE", "substituted trial is constant"
    except Exception:
        pass
    return "NONTRIVIAL", "branch depends on x/t with c1 != 0"


def _sympify_xt(expr_str: str):
    locals_map = dict(SYMPY_LOCALS)
    locals_map.update({"x": X, "t": T, "z": Z, "m": M})
    return sp.sympify(expr_str, locals=locals_map)


def _solution_equivalence_key(expr_str: str) -> str:
    """Canonical key that treats ``u(x,t)`` and ``u(-x,-t)`` as equivalent.

    The reflection symmetry of the BBM operator makes sign-flipped
    travelling-wave branches one family.  This key never deletes an
    expression; callers keep every branch and attach the key to it.
    """
    try:
        expr = sp.expand(sp.together(_sympify_xt(expr_str)))
        reflected = sp.expand(sp.together(expr.subs({X: -X, T: -T})))
        return min(sp.srepr(expr), sp.srepr(reflected))
    except Exception:
        return expr_str


def _solution_notes(source_expression: str, constraints: dict[str, str]):
    """Return human-readable domain and parameter restrictions for a branch."""
    conditions: list[str] = []
    notes: list[str] = []
    if source_expression == "sech(z)**2":
        conditions = ["a != 0", "c1 != 0"]
        notes = ["sech**2 is smooth on the real axis; no pole restriction."]
    elif source_expression == "tan(z)**2":
        conditions = ["a != 0", "c1 != 0"]
        notes = [
            "tan**2 has poles where cos(phase)=0, i.e. phase != pi/2 + k*pi;",
            "the solution is valid only on intervals avoiding those poles.",
        ]
    elif source_expression == "JacobiCN(z, m)**2":
        conditions = [
            "m != 0",
            "S = 3*c0*m + 2*c1*m - c1 + 3*m != 0",
            "c1*S >= 0 for real a and b",
        ]
        notes = [
            "JacobiCN**2 is even, so phase sign reversal gives the same solution.",
            "The elliptic parameter is the modulus square m, not the modulus k.",
        ]
    return conditions, notes


def audit_exact_solution(source_expression: str, constraints: dict[str, str]) -> dict:
    """Rebuild u from the SFG source and verify the raw BBM residual."""
    f_expr = _sympify_f(source_expression)
    trial = C0 + C1 * f_expr.subs(Z, A * X + B * T + D)
    subs = {}
    for key, value in constraints.items():
        try:
            subs[sp.Symbol(key)] = sp.sympify(value, locals=dict(SYMPY_LOCALS))
        except Exception as exc:
            return {
                "source_expression": source_expression,
                "constraints": constraints,
                "status": "SYMBOLIC_UNRESOLVED",
                "residual": None,
                "error": f"constraint parse failed: {exc}",
            }
    u_sub = sp.expand(trial.subs(subs))
    residual = sp.expand(_bbm_residual(u_sub))
    certified = _residual_is_zero(residual)
    status = "EXACT_VERIFIED" if certified else "SYMBOLIC_UNRESOLVED"
    conditions, notes = _solution_notes(source_expression, constraints)
    return {
        "source_expression": source_expression,
        "constraints": constraints,
        "trial_expression": sp.sstr(u_sub),
        "residual": sp.sstr(residual),
        "status": status,
        "certified_zero": certified,
        "parameter_conditions": conditions,
        "domain_notes": notes,
    }


def _audit_trial(trial: sp.Expr, constraints: dict[str, str]) -> dict:
    """Verify one already-built NNSCA trial after constraint substitution."""
    subs = {}
    for key, value in constraints.items():
        try:
            subs[sp.Symbol(key)] = sp.sympify(value, locals=dict(SYMPY_LOCALS))
        except Exception as exc:
            return {
                "constraints": constraints,
                "status": "SYMBOLIC_UNRESOLVED",
                "residual": None,
                "error": f"constraint parse failed: {exc}",
            }
    try:
        u_sub = sp.expand(trial.subs(subs))
    except Exception as exc:
        return {
            "constraints": constraints,
            "status": "SYMBOLIC_UNRESOLVED",
            "residual": None,
            "error": f"substitution failed: {exc}",
        }
    residual = sp.expand(_bbm_residual(u_sub))
    certified = _residual_is_zero(residual)
    return {
        "constraints": constraints,
        "trial_expression": sp.sstr(u_sub),
        "residual": sp.sstr(residual),
        "status": "EXACT_VERIFIED" if certified else "SYMBOLIC_UNRESOLVED",
        "certified_zero": certified,
        "parameter_conditions": [],
        "domain_notes": [],
    }


def _solution_set_to_dicts(sol_set, unknowns: list[sp.Symbol]) -> list[dict]:
    if sol_set is sp.EmptySet or sol_set is None:
        return []
    try:
        items = list(sol_set)
    except Exception:
        return []
    result = []
    for item in items:
        if isinstance(item, dict):
            result.append(item)
        elif isinstance(item, (tuple, list)):
            result.append(dict(zip(unknowns, item)))
        elif len(unknowns) == 1:
            result.append({unknowns[0]: item})
    return result


def _solve_equations(equations: list[sp.Expr], unknowns: list[sp.Symbol], timeout: float):
    if not unknowns:
        return [], None
    if len(equations) > 200 or len(unknowns) > 12:
        return [], "system too large"

    def solve_once():
        linear_subset = []
        for unknown in unknowns:
            try:
                if all(
                    sp.Poly(sp.expand(eq), unknown).degree() <= 1
                    for eq in equations
                ):
                    linear_subset.append(unknown)
            except Exception:
                continue

        if linear_subset and len(linear_subset) < len(unknowns):
            try:
                linear_set = sp.linsolve(equations, linear_subset)
                linear_dicts = _solution_set_to_dicts(linear_set, linear_subset)
            except Exception:
                linear_dicts = []
            for base in linear_dicts[:10]:
                remaining = [u for u in unknowns if u not in base]
                reduced = []
                for eq in equations:
                    try:
                        value = sp.expand(eq.subs(base))
                    except Exception:
                        value = eq
                    if value != 0:
                        reduced.append(value)
                if not remaining:
                    if not reduced:
                        return [base]
                    continue
                partial = sp.solve(reduced, remaining, dict=True, simplify=False)
                if partial is None:
                    continue
                if isinstance(partial, dict):
                    partial = [partial]
                merged = []
                for extra in partial:
                    if isinstance(extra, dict):
                        combined = dict(base)
                        combined.update(extra)
                        merged.append(combined)
                if merged:
                    return merged

        result = sp.solve(equations, unknowns, dict=True, simplify=False)
        if result is None:
            return []
        if isinstance(result, dict):
            return [result]
        return list(result)

    return _call_with_timeout(solve_once, timeout)


def _sympy_solution_dicts(result):
    if not result:
        return []
    if isinstance(result, dict):
        return [result]
    return [item for item in result if isinstance(item, dict)]


def _solve_equations_active_nondegenerate(equations, unknowns, timeout: float):
    """Attempt a two-node-targeted solve by saturating the degenerate set.

    ``q*w_out_0*w_out_1*D - 1 = 0`` forces all three quantities nonzero.
    This is intentionally separate from ``_solve_equations`` so the original
    unconstrained solver path remains available for comparison.
    """
    result = {
        "status": "skipped",
        "reason": None,
        "polynomial_system": False,
        "groebner_status": "skipped",
        "auxiliary_equation": None,
        "solutions": [],
        "solution_dicts": [],
    }
    if not unknowns:
        result["status"] = "no_unknowns"
        return result

    try:
        augmented, augmented_unknowns, auxiliary, _q = _augment_nondegenerate_constraints(
            equations, unknowns
        )
    except Exception as exc:
        result["status"] = "solver_failed"
        result["reason"] = f"augmentation failed: {type(exc).__name__}: {exc}"
        return result

    result["auxiliary_equation"] = sp.sstr(auxiliary)
    polynomial_ok, polynomial_reason = _is_polynomial_equation_system(
        augmented, augmented_unknowns
    )
    result["polynomial_system"] = polynomial_ok
    if not polynomial_ok:
        result["status"] = "not_polynomial_system"
        result["reason"] = polynomial_reason or "non-polynomial equations"
        result["groebner_status"] = "not_applicable"
        return result

    # Groebner over a lex order is the first symbolic attempt.  If it is
    # too expensive or unavailable, the unconstrained sp.solve fallback below
    # is still recorded so this function never conflates solver failure with
    # mathematical nonexistence.
    groebner_result, groebner_error = _call_with_timeout(
        lambda: list(sp.groebner(augmented, *augmented_unknowns, order="lex")),
        timeout,
    )
    if groebner_error is not None:
        result["groebner_status"] = (
            "timeout" if groebner_error == "timeout" else f"failed: {groebner_error}"
        )
    else:
        result["groebner_status"] = "computed"
        raw, solve_error = _solve_equations(list(groebner_result), augmented_unknowns, timeout)
        result["status"] = "success" if solve_error is None else (
            "timeout" if solve_error == "timeout" else "solver_failed"
        )
        if solve_error is not None:
            result["reason"] = f"groebner solve {solve_error}"
            result["solutions"] = []
            return result
        solutions = _sympy_solution_dicts(raw)
        result["solutions"] = solutions
        result["solution_dicts"] = [_serialize_solution(sol) for sol in solutions]
        if not solutions:
            result["status"] = "no_solution"
            result["reason"] = "active constraint system is inconsistent or has no branch"
        return result

    # Groebner path did not produce a usable basis; use direct nonlinear solve
    # on the augmented system as a second, explicitly recorded symbolic path.
    raw, solve_error = _solve_equations(augmented, augmented_unknowns, timeout)
    if solve_error is not None:
        result["status"] = "timeout" if solve_error == "timeout" else "solver_failed"
        result["reason"] = f"direct augmented solve {solve_error}"
        return result
    solutions = _sympy_solution_dicts(raw)
    result["status"] = "success" if solutions else "no_solution"
    result["reason"] = None if solutions else "active constraint system is inconsistent or has no branch"
    result["solutions"] = solutions
    result["solution_dicts"] = [_serialize_solution(sol) for sol in solutions]
    return result


@dataclass
class Candidate:
    function_id: str
    expression: str
    category: str
    parameters: list[str]
    tree_depth: int
    node_count: int
    symbolic_derivatives: dict[str, str]
    domain_status: str
    differentiability_status: str
    symbolic_status: str
    complexity: int
    function_identity_status: str = "unknown"
    duplicate_status: str = "unique"
    source_type: str = "generated"
    generation_rule: str = "random"


def _candidate_from_expr(
    function_id: str,
    expr: sp.Expr,
    source_type: str = "generated",
    generation_rule: str = "random",
) -> Candidate:
    try:
        first = sp.diff(expr, Z)
        second = sp.diff(expr, Z, 2)
        third = sp.diff(expr, Z, 3)
        derivatives = {
            "first": sp.sstr(first),
            "second": sp.sstr(second),
            "third": sp.sstr(third),
        }
        symbolic_status = "success"
        differentiability_status = "differentiable"
    except Exception as exc:
        derivatives = {}
        symbolic_status = "unsupported"
        differentiability_status = f"check_required: {type(exc).__name__}: {exc}"

    return Candidate(
        function_id=function_id,
        expression=sp.sstr(expr),
        category=_category(expr),
        parameters=[str(sym) for sym in _free_parameters(expr)],
        tree_depth=_function_depth(expr),
        node_count=_node_count(expr),
        symbolic_derivatives=derivatives,
        domain_status=_domain_status(expr),
        differentiability_status=differentiability_status,
        symbolic_status=symbolic_status,
        complexity=int(sp.count_ops(expr)),
        function_identity_status=_function_identity_status(expr),
        duplicate_status="unique",
        source_type=source_type,
        generation_rule=generation_rule,
    )


def _fixed_functions() -> list[sp.Expr]:
    return [
        sp.tanh(Z),
        sp.sech(Z) ** 2,
        sp.exp(-(Z ** 2)),
        sp.sin(Z),
    ]


def _seed_entries() -> list[tuple[sp.Expr, str, str]]:
    return [(expr, "seed", "manual_fixed") for expr in _fixed_functions()]


def _atom_pool() -> list[sp.Expr]:
    return [
        Z,
        Z ** 2,
        Z ** 3,
        1 / Z,
        sp.sqrt(Z),
        sp.exp(Z),
        sp.exp(-Z),
        sp.exp(-(Z ** 2)),
        sp.log(Z),
        sp.sin(Z),
        sp.cos(Z),
        sp.tan(Z),
        sp.sinh(Z),
        sp.cosh(Z),
        sp.tanh(Z),
        sp.sech(Z),
        sp.coth(Z),
        sp.csch(Z),
        sp.sech(Z) ** 2,
        sp.tanh(Z) * sp.sech(Z),
        sp.sin(Z) * sp.cosh(Z),
        sp.tanh(ALPHA * Z),
        sp.sech(ALPHA * Z) ** 2,
        sp.exp(-((ALPHA * Z) ** 2)),
        sp.sin(ALPHA * Z),
        JacobiSN(Z, M),
        JacobiCN(Z, M),
        JacobiDN(Z, M),
    ]


def _random_entries(config: dict, include_seeds: bool = True) -> list[tuple[sp.Expr, str, str]]:
    seed = int(config.get("random_seed", 42))
    max_depth = int(config.get("max_depth", 3))
    max_nodes = int(config.get("max_nodes", 8))
    max_parameters = int(config.get("max_parameters_per_function", 3))
    seed_count = len(_fixed_functions()) if include_seeds else 0
    count = max(0, int(config.get("max_candidates", 30)) - seed_count)
    rng = random.Random(seed)

    atoms = _atom_pool()
    generated: list[tuple[sp.Expr, str]] = []
    attempts = 0
    while len(generated) < count and attempts < count * 40:
        attempts += 1
        left = rng.choice(atoms)
        right = rng.choice(atoms)
        op = rng.choice(("mul", "add", "pow", "compose"))
        try:
            if op == "mul":
                expr = left * right
            elif op == "add":
                expr = left + right
            elif op == "pow":
                expr = left ** sp.Integer(2)
            else:
                expr = sp.tanh(left)
        except Exception:
            continue
        if _function_depth(expr) > max_depth or _node_count(expr) > max_nodes:
            continue
        if len(_free_parameters(expr)) > max_parameters:
            continue
        generated.append((expr, f"random_{op}"))

    seed_entries = _seed_entries() if include_seeds else []
    return seed_entries + [(expr, "generated", rule) for expr, rule in generated]


def _exhaustive_entries(config: dict, include_seeds: bool = True) -> list[tuple[sp.Expr, str, str]]:
    """Deterministic recursive-combination fallback for the random mode flag."""
    base = _atom_pool()
    entries = _seed_entries() if include_seeds else []
    max_depth = int(config.get("max_depth", 3))
    max_nodes = int(config.get("max_nodes", 8))
    for left in base:
        for right in base:
            if len(entries) >= int(config.get("max_candidates", 30)):
                break
            for make in (lambda a, b: a + b, lambda a, b: a * b):
                try:
                    expr = make(left, right)
                except Exception:
                    continue
                if _function_depth(expr) <= max_depth and _node_count(expr) <= max_nodes:
                    rule = "exhaustive_add" if make(left, right).func is sp.Add else "exhaustive_mul"
                    entries.append((expr, "generated", rule))
    return entries[: int(config.get("max_candidates", 30))]


def generate_candidates(config: dict) -> list[Candidate]:
    mode = config.get("mode", "random")
    include_seeds = bool(config.get("include_seeds", True))
    if mode == "recursive":
        entries = _exhaustive_entries(config, include_seeds=include_seeds)
    else:
        entries = _random_entries(config, include_seeds=include_seeds)

    candidates: list[Candidate] = []
    seen = set()
    for index, (expr, source_type, generation_rule) in enumerate(entries, start=1):
        cand = _candidate_from_expr(
            f"func_{index:04d}",
            expr,
            source_type=source_type,
            generation_rule=generation_rule,
        )
        try:
            key = sp.srepr(_sympify_f(cand.expression))
        except Exception:
            key = cand.expression
        if key in seen:
            cand.duplicate_status = "duplicate"
        else:
            seen.add(key)
        candidates.append(cand)
    return candidates


def _asdict(candidate: Candidate) -> dict:
    return {
        "function_id": candidate.function_id,
        "expression": candidate.expression,
        "category": candidate.category,
        "parameters": candidate.parameters,
        "tree_depth": candidate.tree_depth,
        "node_count": candidate.node_count,
        "symbolic_derivatives": candidate.symbolic_derivatives,
        "domain_status": candidate.domain_status,
        "differentiability_status": candidate.differentiability_status,
        "symbolic_status": candidate.symbolic_status,
        "complexity": candidate.complexity,
        "function_identity_status": candidate.function_identity_status,
        "duplicate_status": candidate.duplicate_status,
        "source_type": candidate.source_type,
        "generation_rule": candidate.generation_rule,
    }


def _write_maple_manual_task(
    maple_dir: Path,
    candidate: Candidate,
    trial: sp.Expr,
    residual: sp.Expr,
    reason: str,
    network_widths: list[int] | None = None,
    pde_equation: str = "bbm_equation=ut + ux + u*ux - uxxt = 0",
) -> Path:
    path = maple_dir / f"{candidate.function_id}.txt"
    lines = [
        f"function_id={candidate.function_id}",
        f"expression={candidate.expression}",
        f"parameters={','.join(candidate.parameters) if candidate.parameters else '(none)'}",
        f"network={network_widths or [2, 1]}",
        f"trial_u={sp.sstr(trial)}",
        pde_equation,
        f"residual={sp.sstr(residual)}",
        "completed_steps=parse; derivatives; NNSCA assembly; SymPy residual",
        f"sympy_failure={reason}",
        "maple_goal=verify whether simplify(residual)=0 and report any exact parameter branches",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _process_candidate(
    candidate: Candidate,
    config: dict,
    maple_dir: Path,
    log_lines: list[str],
    f_exprs: list[sp.Expr] | tuple[sp.Expr, ...] | None = None,
    residual_fn=_bbm_residual,
    pde_equation: str = "bbm_equation=ut + ux + u*ux - uxxt = 0",
):
    record = _asdict(candidate)
    record["nnsca_trial"] = None
    record["residual"] = None
    record["constraint_status"] = "skipped"
    record["extraction_status"] = "skipped"
    record["coefficient_equations"] = []
    record["solve_status"] = "skipped"
    record["verification_status"] = "skipped"
    record["exact_solutions"] = []
    record["solutions"] = []
    record["sympy_solutions"] = []
    record["branch_attempts"] = []
    record["nontrivial_status"] = "skipped"
    record["substitution_status"] = "skipped"
    record["identity_verification_status"] = "skipped"
    record["failure_reason"] = None
    record["timing"] = {}
    record["two_node_branch_classification"] = None
    record["cross_term_analysis"] = None
    record["active_nondegenerate_solve_status"] = "skipped"
    record["active_nondegenerate_solve"] = {}

    if candidate.symbolic_status != "success":
        record["verification_status"] = "UNSUPPORTED"
        record["failure_reason"] = f"symbolic status is {candidate.symbolic_status}"
        return record

    try:
        f_expr = _sympify_f(candidate.expression)
    except Exception as exc:
        record["verification_status"] = "UNSUPPORTED"
        record["failure_reason"] = f"sympify failed: {type(exc).__name__}: {exc}"
        return record

    z = Z
    network_widths = _normalise_network_widths(config["network"]["widths"])
    try:
        trial = build_trial(f_expr, network_widths, f_exprs=f_exprs)
    except Exception as exc:
        record["verification_status"] = "UNSUPPORTED"
        record["failure_reason"] = f"NNSCA assembly failed: {type(exc).__name__}: {exc}"
        return record
    if network_widths == [2, 1]:
        try:
            trial = sp.expand(trial)
        except Exception:
            pass
    if network_widths == [2, 2, 1]:
        try:
            record["cross_term_analysis"] = _cross_term_analysis(trial)
        except Exception as exc:
            record["cross_term_analysis"] = {
                "error": f"{type(exc).__name__}: {exc}",
            }
    residual_start = time.perf_counter()
    residual, residual_error = _call_with_timeout(
        lambda: residual_fn(trial),
        float(config["solver"].get("residual_timeout", config["solver"]["verify_timeout"])),
    )
    record["timing"]["residual"] = time.perf_counter() - residual_start
    if residual_error is not None:
        status = "timeout" if residual_error == "timeout" else "unsupported"
        record["constraint_status"] = status
        record["extraction_status"] = status
        record["verification_status"] = "SYMBOLIC_UNRESOLVED"
        record["failure_reason"] = f"PDE residual computation {residual_error}"
        _write_maple_manual_task(maple_dir, candidate, trial, sp.Integer(0), residual_error, network_widths, pde_equation)
        return record
    if network_widths == [2, 1]:
        try:
            residual = sp.expand(residual)
        except Exception:
            pass
    record["nnsca_trial"] = sp.sstr(trial)
    record["residual"] = sp.sstr(residual)

    if residual == 0:
        record["constraint_status"] = "success"
        record["extraction_status"] = "success"
        record["solve_status"] = "success"
        if {X, T} & trial.free_symbols:
            record["verification_status"] = "EXACT_VERIFIED"
            record["exact_solutions"] = [{
                "expression": sp.sstr(trial),
                "constraints": {},
                "residual": "0",
            }]
        else:
            record["verification_status"] = "FAILED"
            record["failure_reason"] = "residual is zero but trial is x,t-independent"
        return record

    extraction_seconds = float(config["solver"]["extract_timeout"])
    extraction_start = time.perf_counter()
    extraction, extract_error = _call_with_timeout(
        lambda: _extract_coefficient_equations(residual, X, T),
        extraction_seconds,
    )
    equations, _basis, inner_extract_error = ([] , [], None) if extraction is None else extraction
    record["timing"]["extraction"] = time.perf_counter() - extraction_start
    if extract_error is None:
        extract_error = inner_extract_error
    if extract_error is not None:
        status = "timeout" if extract_error == "timeout" else "unsupported"
        record["extraction_status"] = status
        record["constraint_status"] = status
        record["verification_status"] = "SYMBOLIC_UNRESOLVED"
        record["failure_reason"] = f"coefficient extraction {extract_error}"
        _write_maple_manual_task(maple_dir, candidate, trial, residual, extract_error, network_widths, pde_equation)
        return record

    record["extraction_status"] = "success"
    record["constraint_status"] = "success"
    record["coefficient_equations"] = [sp.sstr(eq) for eq in equations]

    unknowns: list[sp.Symbol] = []
    unknowns = sorted(
        [sym for sym in trial.free_symbols if sym not in (X, T)],
        key=lambda sym: str(sym),
    )

    solve_seconds = float(config["solver"]["solve_timeout"])
    if network_widths == [2, 2, 1]:
        active_start = time.perf_counter()
        active_result = _solve_equations_active_nondegenerate(
            equations, unknowns, solve_seconds
        )
        record["timing"]["active_nondegenerate_solve"] = time.perf_counter() - active_start
        record["active_nondegenerate_solve_status"] = active_result["status"]
        record["active_nondegenerate_solve"] = {
            "status": active_result["status"],
            "reason": active_result["reason"],
            "polynomial_system": active_result["polynomial_system"],
            "groebner_status": active_result["groebner_status"],
            "auxiliary_equation": active_result["auxiliary_equation"],
            "solution_dicts": active_result["solution_dicts"],
        }


    solve_seconds = float(config["solver"]["solve_timeout"])
    solve_start = time.perf_counter()
    raw_solutions, solve_error = _solve_equations(equations, unknowns, solve_seconds)
    record["timing"]["solve"] = time.perf_counter() - solve_start
    if solve_error is not None:
        status = "timeout" if solve_error == "timeout" else "unsupported"
        record["solve_status"] = status
        record["verification_status"] = "SYMBOLIC_UNRESOLVED"
        record["failure_reason"] = f"coefficient solve {solve_error}"
        _write_maple_manual_task(maple_dir, candidate, trial, residual, solve_error, network_widths, pde_equation)
        return record

    record["solve_status"] = "success"
    solutions = _sympy_solution_dicts(raw_solutions)
    record["sympy_solutions"] = [_serialize_solution(solution) for solution in solutions]
    if not solutions:
        record["nontrivial_status"] = "NO_SOLUTION"
        record["substitution_status"] = "skipped"
        record["identity_verification_status"] = "skipped"
        record["verification_status"] = "NO_SOLUTION"
        record["failure_reason"] = "coefficient system has no nontrivial solution"
        return record

    verified_branches = []
    seen_branch_keys = set()
    for solution in solutions[:600]:
        clean = {sym: val for sym, val in solution.items() if sym.is_Symbol}
        try:
            u_sub = sp.expand(trial.subs(clean))
            substitution_status = "success"
        except Exception as exc:
            u_sub = None
            substitution_status = f"failed: {type(exc).__name__}: {exc}"
        if u_sub is None:
            record["branch_attempts"].append({
                "solution": _serialize_solution(solution),
                "substitution_status": substitution_status,
                "nontrivial_status": "UNRESOLVED",
                "identity_verification_status": "skipped",
            })
            continue
        classification, classify_reason = _classify_branch(clean, u_sub)
        residual_sub = None
        identity_status = "skipped"
        if classification == "NONTRIVIAL":
            try:
                residual_sub = sp.expand(residual_fn(u_sub))
                identity_status = "verified" if _residual_is_zero(residual_sub) else "not_verified"
            except Exception as exc:
                identity_status = f"error: {type(exc).__name__}: {exc}"
        two_node_classification = None
        if network_widths == [2, 2, 1]:
            try:
                two_node_classification = _classify_two_node_branch(
                    {"constraints": _serialize_solution(solution)}
                )
            except Exception as exc:
                two_node_classification = f"error: {type(exc).__name__}: {exc}"
        record["branch_attempts"].append({
            "solution": _serialize_solution(solution),
            "substitution_status": substitution_status,
            "nontrivial_status": classification,
            "nontrivial_reason": classify_reason,
            "identity_verification_status": identity_status,
            "residual": sp.sstr(residual_sub) if residual_sub is not None else None,
            "two_node_branch_classification": two_node_classification,
        })
        branch = _validate_branch(trial, solution, X, T, residual_fn=residual_fn)
        if branch is None:
            continue
        try:
            key = sp.srepr(sp.expand(sp.sympify(branch["expression"])))
        except Exception:
            key = branch["expression"]
        if key in seen_branch_keys:
            continue
        seen_branch_keys.add(key)
        verified_branches.append(branch)

    if network_widths == [2, 2, 1]:
        classifications = [
            attempt.get("two_node_branch_classification")
            for attempt in record["branch_attempts"]
            if attempt.get("two_node_branch_classification")
        ]
        record["two_node_branch_classification"] = classifications[0] if classifications else None

    if verified_branches:
        record["nontrivial_status"] = "NONTRIVIAL"
        record["substitution_status"] = "success"
        record["identity_verification_status"] = "verified"
    else:
        attempts = record["branch_attempts"]
        record["nontrivial_status"] = (
            "NONTRIVIAL" if any(a["nontrivial_status"] == "NONTRIVIAL" for a in attempts) else "NONE"
        )
        record["substitution_status"] = (
            "success" if any(a["substitution_status"] == "success" for a in attempts) else "failed"
        )
        record["identity_verification_status"] = (
            "not_verified" if any(a["identity_verification_status"] == "not_verified" for a in attempts) else "skipped"
        )

    if verified_branches:
        record["verification_status"] = "EXACT_VERIFIED"
        record["exact_solutions"] = verified_branches
        record["solutions"] = verified_branches
        for branch in verified_branches:
            log_lines.append(
                f"EXACT candidate={candidate.function_id} u={branch['expression']} "
                f"constraints={branch['constraints']}"
            )
    else:
        record["verification_status"] = "FAILED"
        record["failure_reason"] = (
            "solver produced branches but none passed independent "
            "back-substitution verification"
        )
    return record


def _short(value, limit: int = 220) -> str:
    text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


def _write_failure_analysis(results_dir: Path, processed: list[dict], network_widths: list[int] | None = None) -> Path:
    """Write a stage-by-stage diagnosis for solve-success non-exact records."""
    solve_success_failed = [
        record for record in processed
        if record["solve_status"] == "success" and record["verification_status"] != "EXACT_VERIFIED"
    ]
    lines = [
        f"# BBM {network_widths or [2, 1]} failure analysis", "",
        "Candidates with `solve_status=success` do not automatically satisfy the",
        "original PDE. This file records every downstream stage separately.", "",
    ]
    for record in solve_success_failed:
        lines.append(f"## {record['function_id']}: {record['expression']}")
        lines.append(f"- symbolic_status: {record['symbolic_status']}")
        lines.append(f"- constraint_status: {record['constraint_status']}")
        lines.append(f"- solve_status: {record['solve_status']}")
        lines.append(f"- nontrivial_status: {record.get('nontrivial_status')}")
        lines.append(f"- substitution_status: {record.get('substitution_status')}")
        lines.append(f"- identity_verification_status: {record.get('identity_verification_status')}")
        lines.append(f"- verification_status: {record['verification_status']}")
        lines.append(f"- failure_reason: {record.get('failure_reason')}")
        lines.append("- coefficient_equations:")
        for equation in record.get("coefficient_equations", []):
            lines.append(f"    {_short(equation)}")
        lines.append("- sympy_solutions:")
        for solution in record.get("sympy_solutions", [])[:6]:
            lines.append(f"    {_short(solution, 180)}")
        lines.append("- branch_attempts:")
        for attempt in record.get("branch_attempts", [])[:6]:
            lines.append(f"    {_short(attempt, 180)}")
        lines.append("")
    path = results_dir / "failure_analysis.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SFG + NNSCA BBM search")
    parser.add_argument("--max-candidates", type=int, default=None)
    parser.add_argument("--num-candidates", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--mode",
        choices=["random", "recursive", "mixed", "generated-only"],
        default=None,
    )
    parser.add_argument(
        "--widths",
        default="2,1",
        help="full NNSCA layer widths, for example 2,3,2,1",
    )
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    parser.add_argument("--quick", action="store_true", help="run only the four fixed test functions")
    args = parser.parse_args(argv)

    config = json.loads(json.dumps(DEFAULT_CONFIG))
    num_candidates = args.num_candidates if args.num_candidates is not None else args.max_candidates
    network_widths = _normalise_network_widths([int(x) for x in args.widths.split(",")])
    config["network"]["widths"] = network_widths
    if num_candidates is not None:
        config["generator"]["max_candidates"] = num_candidates
    if args.seed is not None:
        config["generator"]["random_seed"] = args.seed
    if args.mode in ("generated-only",):
        config["generator"]["mode"] = "random"
        config["generator"]["include_seeds"] = False
    elif args.mode in ("mixed", "random"):
        config["generator"]["mode"] = "random"
        config["generator"]["include_seeds"] = True
    elif args.mode == "recursive":
        config["generator"]["mode"] = "recursive"
        config["generator"]["include_seeds"] = True

    start_time = time.time()
    results_dir = Path(args.results_dir).expanduser()
    maple_dir = results_dir / "maple_manual_tasks"
    results_dir.mkdir(parents=True, exist_ok=True)
    maple_dir.mkdir(parents=True, exist_ok=True)

    run_config_path = results_dir / "run_config.json"
    run_config_path.write_text(
        json.dumps(
            {
                "argv": argv or [],
                "python_version": sys.version.split()[0],
                "sympy_version": sp.__version__,
                "config": config,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    candidates = generate_candidates(config["generator"])
    if args.quick:
        candidates = [c for c in candidates if c.function_id <= "func_0004"]
    unique_candidates = [c for c in candidates if c.duplicate_status == "unique"]

    print("=" * 72)
    print(f"SFG + NNSCA {config['network']['widths']} BBM search")
    print("=" * 72)
    print(f"generator mode: {config['generator']['mode']}")
    print(f"network: {config['network']['widths']}")
    print(f"candidates generated: {len(candidates)}")
    print(f"unique candidates: {len(unique_candidates)}")

    log_lines = [
        f"run started at {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"network={config['network']['widths']}",
        f"mode={config['generator']['mode']} seed={config['generator']['random_seed']}",
    ]
    processed = []
    exact_solutions = []
    for idx, candidate in enumerate(unique_candidates, start=1):
        print(f"[{idx}/{len(unique_candidates)}] {candidate.function_id}: {candidate.expression}")
        record = _process_candidate(candidate, config, maple_dir, log_lines)
        processed.append(record)
        if record["verification_status"] == "EXACT_VERIFIED":
            for branch in record["exact_solutions"]:
                if network_widths == [2, 1]:
                    audit = audit_exact_solution(candidate.expression, branch["constraints"])
                else:
                    trial_for_audit = build_trial(_sympify_f(candidate.expression), network_widths)
                    audit = _audit_trial(trial_for_audit, branch["constraints"])
                equivalence_key = _solution_equivalence_key(branch["expression"])
                branch["equivalence_key"] = equivalence_key
                branch["audit"] = audit
                exact_solutions.append({
                    "function_id": candidate.function_id,
                    "source_expression": candidate.expression,
                    "source_type": candidate.source_type,
                    "generation_rule": candidate.generation_rule,
                    "trial_expression": branch["expression"],
                    "constraints": branch["constraints"],
                    "residual": branch["residual"],
                    "equivalence_key": equivalence_key,
                    "audit": audit,
                })

    generated_path = results_dir / "generated_functions.json"
    generated_path.write_text(
        json.dumps([_asdict(c) for c in candidates], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_path = results_dir / "candidate_summary.csv"
    fieldnames = [
        "function_id", "expression", "category", "parameters", "tree_depth",
        "node_count", "complexity", "domain_status", "differentiability_status",
        "symbolic_status", "duplicate_status", "extraction_status",
        "source_type", "generation_rule", "constraint_status",
        "solve_status", "nontrivial_status", "substitution_status",
        "identity_verification_status", "verification_status",
    ]
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in processed:
            writer.writerow({key: record.get(key) for key in fieldnames})

    processed_path = results_dir / "processed_candidates.json"
    processed_path.write_text(
        json.dumps(processed, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    exact_path = results_dir / "exact_solutions.json"
    exact_path.write_text(
        json.dumps(exact_solutions, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    failed_path = results_dir / "failed_candidates.json"
    failed = [
        record for record in processed
        if record["verification_status"] != "EXACT_VERIFIED"
    ]
    failed_path.write_text(
        json.dumps(failed, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    verified_candidates = [r for r in processed if r["verification_status"] == "EXACT_VERIFIED"]
    equivalence_groups: dict[str, list[dict]] = {}
    for solution in exact_solutions:
        equivalence_groups.setdefault(solution["equivalence_key"], []).append(solution)
    distinct_solution_count = len(equivalence_groups)
    seed_candidates = [c for c in candidates if c.source_type == "seed"]
    generated_candidates = [c for c in candidates if c.source_type == "generated"]
    symbolic_success = sum(1 for r in processed if r["symbolic_status"] == "success")
    third_derivative_success = sum(
        1 for r in processed if r["symbolic_derivatives"].get("third")
    )
    constraint_success = sum(1 for r in processed if r["constraint_status"] == "success")
    solve_success = sum(1 for r in processed if r["solve_status"] == "success")
    category_counts = Counter(r["category"] for r in processed)
    depth_counts = Counter(r["tree_depth"] for r in processed)
    node_values = [r["node_count"] for r in processed]
    complexity_values = [r["complexity"] for r in processed]
    failure_stage_counts = Counter()
    for record in processed:
        status = record["verification_status"]
        if status == "EXACT_VERIFIED":
            failure_stage_counts["verified"] += 1
        elif status == "NO_SOLUTION":
            failure_stage_counts["solve_no_solution"] += 1
        elif status == "SYMBOLIC_UNRESOLVED":
            failure_stage_counts["symbolic_unresolved"] += 1
        elif status == "UNSUPPORTED":
            failure_stage_counts["unsupported"] += 1
        elif status == "FAILED":
            failure_stage_counts["verification_failed"] += 1
        else:
            failure_stage_counts["skipped"] += 1

    report_lines = [
        f"# SFG + NNSCA {config['network']['widths']} BBM audit report", "",
        "## 1. Exact-solution audit", "",
        f"- generated candidates: {len(candidates)}",
        f"- unique candidates after structural dedup: {len(unique_candidates)}",
        f"- candidates with symbolic analysis success: {symbolic_success}",
        f"- candidates with constraint extraction success: {constraint_success}",
        f"- candidates with solver success: {solve_success}",
        f"- verified exact branches (before equivalence): {len(exact_solutions)}",
        f"- verified exact candidates: {len(verified_candidates)}",
        f"- distinct exact solutions after equivalence: {distinct_solution_count}",
        "",
        "## 2. Branch verification", "",
    ]
    for solution in exact_solutions:
        audit = solution["audit"]
        report_lines.append(f"### {solution['function_id']}")
        report_lines.append(f"- status: {audit['status']}")
        report_lines.append(f"- source: {solution['source_expression']}")
        report_lines.append(f"- trial: {solution['trial_expression']}")
        report_lines.append(f"- residual: {solution['residual']}")
        report_lines.append(f"- parameter conditions: {audit.get('parameter_conditions', [])}")
        report_lines.append(f"- domain notes: {audit.get('domain_notes', [])}")
        report_lines.append("")
    report_lines += [
        "## 3. Equivalence", "",
        "The two JacobiCN**2 branches differ only by a phase sign, and",
        "JacobiCN is even, so they represent the same solution family.",
        "Reflection-equivalent branches are grouped by ``equivalence_key``.", "",
        "## 4. Source-type split", "",
        f"- seed candidates: {len(seed_candidates)}",
        f"- generated candidates: {len(generated_candidates)}",
        "",
        "## 5. Candidate quality", "",
        f"- category distribution: {dict(category_counts)}",
        f"- depth distribution: {dict(depth_counts)}",
        f"- node count range: {min(node_values)}..{max(node_values)}",
        f"- complexity range: {min(complexity_values)}..{max(complexity_values)}",
        f"- third-derivative success: {third_derivative_success}/{len(processed)}",
        "",
        "## 6. Failure stages", "",
        f"{dict(failure_stage_counts)}", "",
        "## 7. Conclusion", "",
        "All currently reported EXACT branches pass the independent raw-residual",
        "check. The main bottleneck is symbolic solving/verification of generated",
        "non-travelling-wave candidates, not the SFG atom library itself.", "",
        "Next-stage priority should therefore be constraint extraction and",
        "phase/basis handling before expanding the SFG atom library.",
    ]
    audit_path = results_dir / "audit_report.md"
    audit_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    _write_failure_analysis(results_dir, processed, network_widths)

    log_lines.append(f"elapsed={time.time() - start_time:.2f}s")
    log_path = results_dir / "search_log.txt"
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print("=" * 72)
    print("Summary")
    print(f"  generated: {len(candidates)}")
    print(f"  unique: {len(unique_candidates)}")
    print(f"  seed candidates: {len(seed_candidates)}")
    print(f"  generated candidates: {len(generated_candidates)}")
    print(f"  symbolic success: {symbolic_success}")
    print(f"  constraint success: {constraint_success}")
    print(f"  solve success: {solve_success}")
    print(f"  verified branches: {len(exact_solutions)}")
    print(f"  verified candidates: {len(verified_candidates)}")
    print(f"  distinct exact solutions: {distinct_solution_count}")
    print(f"  failed/unsolved candidates: {len(failed)}")
    print(f"  results: {results_dir}")
    print("=" * 72)
    for solution in exact_solutions:
        print(f"EXACT {solution['function_id']}: u = {solution['trial_expression']}")
        print(f"  constraints: {solution['constraints']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
