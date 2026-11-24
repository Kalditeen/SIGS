"""Generic CH residual construction and lightweight complexity metrics."""

from __future__ import annotations

import sympy as sp

from . import ch_equation as ce


def camassa_holm_residual(u: sp.Expr) -> sp.Expr:
    """Raw CH residual for an arbitrary network trial ``u(x, t)``."""
    u_t = sp.diff(u, ce.T)
    u_x = sp.diff(u, ce.X)
    u_xx = sp.diff(u, ce.X, 2)
    u_xxx = sp.diff(u, ce.X, 3)
    u_xxt = sp.diff(u, ce.X, 2, ce.T)
    return sp.expand(
        u_t + 2 * ce.K * u_x - u_xxt
        + 3 * u * u_x
        - 2 * u_x * u_xx
        - u * u_xxx
    )


def residual_summary(u: sp.Expr) -> dict:
    residual = camassa_holm_residual(u)
    return {
        "residual": residual,
        "residual_is_zero": sp.expand(residual) == 0,
        "additive_terms": len(sp.Add.make_args(sp.expand(residual)))
        if sp.expand(residual) != 0
        else 0,
        "sympy_operations": sp.count_ops(residual, visual=False),
        "free_symbols": sorted(str(symbol) for symbol in residual.free_symbols),
    }


def expression_size(expr: sp.Expr) -> dict:
    expanded = sp.expand(expr)
    return {
        "srepr_chars": len(sp.srepr(expanded)),
        "str_chars": len(sp.sstr(expanded)),
        "sympy_operations": sp.count_ops(expanded, visual=False),
        "additive_terms": len(sp.Add.make_args(expanded)) if expanded != 0 else 0,
    }


def common_term_groups(expr: sp.Expr) -> dict:
    """Deterministic additive-term grouping by symbolic factors.

    This is a lightweight structure-recognition metric, not a formal PDE
    coefficient extraction. It ignores only the numeric coefficient.
    """
    expanded = sp.expand(expr)
    if expanded == 0:
        return {"term_count": 0, "group_count": 0, "groups": []}
    terms = [term for term in sp.Add.make_args(expanded)]
    groups: dict[str, list[str]] = {}
    for term in terms:
        _coeff, factors = term.as_coeff_mul()
        key = sp.srepr(sp.Mul(*sorted(factors, key=lambda item: sp.srepr(item))))
        groups.setdefault(key, []).append(sp.sstr(term))
    return {
        "term_count": len(terms),
        "group_count": len(groups),
        "groups": list(groups.values()),
    }
