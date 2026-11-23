#!/usr/bin/env python3
"""PDE-independent special-function reduction helpers.

This module is deliberately small.  It does not know about Gardner or BBM.
It provides derivative identities for the Jacobi elliptic functions and a
generic reducer that rewrites known algebraic powers so coefficient
extraction sees a smaller, mathematically honest basis.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sigs.jacobi import JacobiCN, JacobiDN, JacobiSN, reduce_jacobi_powers  # noqa: E402

JACOBI_FUNCS = (JacobiSN, JacobiCN, JacobiDN)


def has_jacobi(expr: sp.Expr) -> bool:
    return any(atom.func in JACOBI_FUNCS for atom in expr.atoms(sp.Function))


def sn_derivative(z, m):
    return JacobiCN(z, m) * JacobiDN(z, m)


def cn_derivative(z, m):
    return -JacobiSN(z, m) * JacobiDN(z, m)


def dn_derivative(z, m):
    return -m * JacobiSN(z, m) * JacobiCN(z, m)


def cn_second_derivative(z, m):
    """Return ``cn''`` as a polynomial in ``cn``."""
    cn = JacobiCN(z, m)
    return (2 * m - 1) * cn - 2 * m * cn**3


def cn_third_derivative(z, m):
    """Return ``cn'''`` as ``(2m - 1 - 6m*cn**2)*cn'``."""
    cn = JacobiCN(z, m)
    return (2 * m - 1 - 6 * m * cn**2) * cn_derivative(z, m)


def _reduce_sech_powers(expr: sp.Expr) -> sp.Expr:
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


def reduce_special_function_expression(
    expr: sp.Expr,
    function_family: str | None = None,
):
    """Reduce known special-function powers in one expression.

    Returns ``(reduced, metadata)``.  The metadata records the identities
    used and whether a supported reducer was found.  Unknown families are
    returned unchanged with an explicit ``unsupported`` status so callers
    never silently pretend a reduction happened.
    """
    before = sp.sstr(expr)

    if function_family is None:
        if has_jacobi(expr):
            function_family = "Jacobi"
        elif expr.has(sp.sech):
            function_family = "sech"
        elif expr.has(sp.tanh):
            function_family = "tanh"
        else:
            function_family = "unknown"

    if function_family in ("Jacobi", "JacobiCN", "JacobiSN", "JacobiDN"):
        try:
            reduced = sp.expand(reduce_jacobi_powers(expr))
            metadata = {
                "status": "success",
                "family": function_family,
                "identities": [
                    "sn**2 + cn**2 = 1",
                    "dn**2 + m*sn**2 = 1",
                ],
                "before": before,
                "after": sp.sstr(reduced),
                "failure_reason": None,
            }
            return reduced, metadata
        except Exception as exc:
            return expr, {
                "status": "failed",
                "family": function_family,
                "identities": [],
                "before": before,
                "after": before,
                "failure_reason": f"{type(exc).__name__}: {exc}",
            }

    if function_family == "sech":
        try:
            reduced = sp.expand(_reduce_sech_powers(expr))
            return reduced, {
                "status": "success",
                "family": "sech",
                "identities": ["sech**2 = 1 - tanh**2"],
                "before": before,
                "after": sp.sstr(reduced),
                "failure_reason": None,
            }
        except Exception as exc:
            return expr, {
                "status": "failed",
                "family": "sech",
                "identities": [],
                "before": before,
                "after": before,
                "failure_reason": f"{type(exc).__name__}: {exc}",
            }

    return expr, {
        "status": "unsupported",
        "family": function_family,
        "identities": [],
        "before": before,
        "after": before,
        "failure_reason": f"no reducer registered for family {function_family!r}",
    }
