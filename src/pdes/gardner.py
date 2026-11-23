"""Gardner equation specification for the generic solver."""

from __future__ import annotations

import sympy as sp

from nnsca.models import T, X

from .models import PDESpec


def gardner_residual(u: sp.Expr, alpha=1, beta=1, gamma=1) -> sp.Expr:
    """Return the raw Gardner residual ``u_t + a*u*u_x + b*u^2*u_x + c*u_xxx``."""
    return (
        sp.diff(u, T)
        + alpha * u * sp.diff(u, X)
        + beta * u**2 * sp.diff(u, X)
        + gamma * sp.diff(u, X, 3)
    )


GARDNER = PDESpec(
    name="Gardner",
    independent_vars=(X, T),
    residual=gardner_residual,
    equation="u_t + u*u_x + u**2*u_x + u_xxx = 0",
    required_derivatives=((X, 3), (T, 1)),
)
