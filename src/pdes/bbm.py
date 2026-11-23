"""BBM equation specification for the generic solver."""

from __future__ import annotations

import sympy as sp

from nnsca.models import T, X

from .models import PDESpec


def bbm_residual(u: sp.Expr) -> sp.Expr:
    """Return the raw BBM residual ``u_t + u_x + u*u_x - u_{xxt}``."""
    return sp.diff(u, T) + sp.diff(u, X) + u * sp.diff(u, X) - sp.diff(u, T, X, 2)


BBM = PDESpec(
    name="BBM",
    independent_vars=(X, T),
    residual=bbm_residual,
    equation="u_t + u_x + u*u_x - u_{xxt} = 0",
    required_derivatives=((X, 2), (T, 1)),
)
