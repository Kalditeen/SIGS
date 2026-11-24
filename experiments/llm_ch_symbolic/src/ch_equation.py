"""Symbols and the Camassa-Holm trial function for the independent experiment."""

from __future__ import annotations

import sympy as sp

X, T = sp.symbols("x t", real=True)
K = sp.Symbol("k")
B4 = sp.Symbol("b4")

A1, A2, A3 = sp.symbols("A1 A2 A3")
WT1, WT2, WT3 = sp.symbols("wt1 wt2 wt3")
WX1, WX2, WX3 = sp.symbols("wx1 wx2 wx3")

Q1, Q2, Q3 = sp.symbols("q1 q2 q3")

AMP = (A1, A2, A3)
WT = (WT1, WT2, WT3)
WX = (WX1, WX2, WX3)
Q = (Q1, Q2, Q3)

SYMBOLS = {
    "x": X,
    "t": T,
    "k": K,
    "b4": B4,
    "A1": A1,
    "A2": A2,
    "A3": A3,
    "wt1": WT1,
    "wt2": WT2,
    "wt3": WT3,
    "wx1": WX1,
    "wx2": WX2,
    "wx3": WX3,
    "q1": Q1,
    "q2": Q2,
    "q3": Q3,
}


def trial_function() -> sp.Expr:
    """Return the three-exponential CH trial used by the Maple benchmark."""
    return B4 + sum(
        amplitude * sp.exp(wt * T + wx * X)
        for amplitude, wt, wx in zip(AMP, WT, WX)
    )


def formal_trial_function() -> sp.Expr:
    """Return the same trial with q_i treated as formal generators."""
    return B4 + A1 * Q1 + A2 * Q2 + A3 * Q3


def camassa_holm_residual(u: sp.Expr) -> sp.Expr:
    """Raw CH residual: u_t + 2k u_x - u_xxt + 3u u_x - 2u_x u_xx - u u_xxx."""
    u_t = sp.diff(u, T)
    u_x = sp.diff(u, X)
    u_xx = sp.diff(u, X, 2)
    u_xxx = sp.diff(u, X, 3)
    u_xxt = sp.diff(u, X, 2, T)
    return sp.expand(
        u_t + 2 * K * u_x - u_xxt + 3 * u * u_x - 2 * u_x * u_xx - u * u_xxx
    )


def substitution_to_formal() -> dict[sp.Expr, sp.Expr]:
    """Map every original exponential to its formal generator."""
    return {
        sp.exp(wt * T + wx * X): q
        for wt, wx, q in zip(WT, WX, Q)
    }
