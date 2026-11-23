"""Camassa-Holm equation specification for cross-equation preparation."""

from __future__ import annotations

import sympy as sp

from nnsca.models import T, X

from .models import PDESpec


def ch_residual(u: sp.Expr, kappa=1) -> sp.Expr:
    """Return a standard Camassa-Holm residual.

    ``u_t + 2*kappa*u_x - u_{xxt} + 3*u*u_x = 2*u_x*u_{xx} + u*u_{xxx}``
    """
    return (
        sp.diff(u, T)
        + 2 * kappa * sp.diff(u, X)
        - sp.diff(u, T, X, 2)
        + 3 * u * sp.diff(u, X)
        - 2 * sp.diff(u, X) * sp.diff(u, X, 2)
        - u * sp.diff(u, X, 3)
    )


CH = PDESpec(
    name="Camassa-Holm",
    independent_vars=(X, T),
    residual=ch_residual,
    equation="u_t + 2*kappa*u_x - u_{xxt} + 3*u*u_x = 2*u_x*u_{xx} + u*u_{xxx}",
    required_derivatives=((X, 3), (X, 2), (X, 1), (T, 1)),
)
