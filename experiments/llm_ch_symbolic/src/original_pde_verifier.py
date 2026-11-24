"""Independent raw-CH verification of the Maple-known parameter branch."""

from __future__ import annotations

import sympy as sp

from . import ch_equation as ce


def maple_branch_substitution() -> dict[sp.Symbol, sp.Expr]:
    """Target branch used only in the verification stage."""
    return {
        ce.K: -ce.B4,
        ce.WX1: sp.Integer(-1),
        ce.WX2: sp.Integer(1),
        ce.WX3: sp.Integer(-1),
    }


def verify_maple_branch() -> dict:
    """Substitute the target branch after the residual is already built."""
    trial = ce.trial_function()

    wx_branch = {
        ce.WX1: sp.Integer(-1),
        ce.WX2: sp.Integer(1),
        ce.WX3: sp.Integer(-1),
    }
    residual_wx_only = sp.expand(ce.camassa_holm_residual(trial).subs(wx_branch))
    try:
        residual_wx_factored = sp.factor(residual_wx_only)
    except Exception:  # noqa: BLE001
        residual_wx_factored = sp.factor_terms(residual_wx_only)

    full_branch = maple_branch_substitution()
    trial_full = sp.expand(trial.subs(full_branch))
    residual_full = sp.expand(ce.camassa_holm_residual(trial).subs(full_branch))
    try:
        residual_full_simplified = sp.factor(residual_full)
    except Exception:  # noqa: BLE001
        residual_full_simplified = sp.factor_terms(residual_full)

    return {
        "branch": {str(key): sp.sstr(value) for key, value in full_branch.items()},
        "trial_after_branch": sp.sstr(trial_full),
        "residual_with_wx_branch_only": sp.sstr(residual_wx_only),
        "residual_with_wx_branch_factor": sp.sstr(residual_wx_factored),
        "final_residual": sp.sstr(residual_full),
        "final_residual_simplified": sp.sstr(residual_full_simplified),
        "is_zero": sp.expand(residual_full) == 0,
    }
