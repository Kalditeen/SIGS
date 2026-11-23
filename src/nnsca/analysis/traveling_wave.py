"""Basic symbolic travelling-wave classification for exact solutions."""

from __future__ import annotations

import sympy as sp

X = sp.symbols("x", real=True)
T = sp.symbols("t", real=True)


def classify_traveling_wave(
    expression: sp.Expr,
    x: sp.Symbol = X,
    t: sp.Symbol = T,
) -> dict:
    """Check whether ``u_t + c*u_x = 0`` holds for some constant ``c``.

    This is only the standard linear travelling-wave test.  It deliberately
    does not claim equivalence under more general variable transformations.
    """
    try:
        expr = sp.expand(sp.together(expression))
        u_x = sp.expand(sp.diff(expr, x))
        u_t = sp.expand(sp.diff(expr, t))
    except Exception as exc:
        return {
            "classification": "UNKNOWN",
            "wave_speed": None,
            "reason": f"derivative computation failed: {type(exc).__name__}: {exc}",
        }

    if u_x == 0 and u_t == 0:
        return {
            "classification": "CONSTANT_OR_DEGENERATE",
            "wave_speed": sp.Integer(0),
            "reason": "expression is independent of x and t",
        }

    if u_x == 0:
        return {
            "classification": "NON_TRAVELING_WAVE_CANDIDATE",
            "wave_speed": None,
            "reason": "u_x == 0 but u_t != 0",
        }

    ratio = sp.together(sp.expand(-u_t / u_x))
    ratio_x_t = {x, t} & ratio.free_symbols
    if not ratio_x_t:
        return {
            "classification": "TRAVELING_WAVE_CONFIRMED",
            "wave_speed": ratio,
            "reason": "u_t + c*u_x == 0 with c independent of x,t",
        }

    # Fallback: ask SymPy to solve u_t + c*u_x == 0 for c.
    c = sp.Symbol("__wave_speed", real=True)
    relation = sp.expand(u_t + c * u_x)
    try:
        solutions = sp.solve(relation, c)
    except Exception:
        solutions = None
    if isinstance(solutions, list):
        for value in solutions:
            if not ({x, t} & value.free_symbols):
                return {
                    "classification": "TRAVELING_WAVE_CONFIRMED",
                    "wave_speed": value,
                    "reason": "SymPy solved u_t + c*u_x == 0 with c independent of x,t",
                }

    return {
        "classification": "NON_TRAVELING_WAVE_CANDIDATE",
        "wave_speed": None,
        "reason": "standard travelling-wave relation was symbolically excluded",
    }


__all__ = ["classify_traveling_wave"]
