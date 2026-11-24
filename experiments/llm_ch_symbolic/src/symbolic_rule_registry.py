"""Curated derivative and identity rule registry for Phase 1.5.

Every rule has a stable ID.  LLM strategies may only reference IDs that exist
here; unknown IDs are rejected by ``strategy_validator``.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class DerivativeRule:
    rule_id: str
    function_type: str
    expression: str
    condition: str
    executor: object


@dataclass(frozen=True)
class IdentityRule:
    rule_id: str
    function_type: str
    expression: str
    condition: str
    executor: object
    pattern: sp.Expr
    replacement: sp.Expr
    preverified: bool = True


def _der_exp(z: sp.Expr) -> sp.Expr:
    return sp.exp(z)


def _der_poly2(z: sp.Expr) -> sp.Expr:
    return 2 * z


def _der_sinh(z: sp.Expr) -> sp.Expr:
    return sp.cosh(z)


def _der_cosh(z: sp.Expr) -> sp.Expr:
    return sp.sinh(z)


def _der_sin(z: sp.Expr) -> sp.Expr:
    return sp.cos(z)


def _der_cos(z: sp.Expr) -> sp.Expr:
    return -sp.sin(z)


def _der_tanh(z: sp.Expr) -> sp.Expr:
    return sp.sech(z) ** 2


DERIVATIVE_RULES: dict[str, DerivativeRule] = {
    "der_exp": DerivativeRule("der_exp", "exp", "D_x exp(ax)=a exp(ax)", "none", _der_exp),
    "der_poly2": DerivativeRule("der_poly2", "poly2", "D_x x^2=2x", "none", _der_poly2),
    "der_sinh": DerivativeRule("der_sinh", "sinh", "D_x sinh(ax)=a cosh(ax)", "none", _der_sinh),
    "der_cosh": DerivativeRule("der_cosh", "cosh", "D_x cosh(ax)=a sinh(ax)", "none", _der_cosh),
    "der_sin": DerivativeRule("der_sin", "sin", "D_x sin(ax)=a cos(ax)", "none", _der_sin),
    "der_cos": DerivativeRule("der_cos", "cos", "D_x cos(ax)=-a sin(ax)", "none", _der_cos),
    "der_tanh": DerivativeRule("der_tanh", "tanh", "D_x tanh(ax)=a sech(ax)^2", "none", _der_tanh),
}


_IDENTITY_WILD = sp.Wild("z")
_COSH_SINH_PATTERN = sp.cosh(_IDENTITY_WILD) ** 2
_COSH_SINH_REPLACEMENT = 1 + sp.sinh(_IDENTITY_WILD) ** 2
_SIN_COS_PATTERN = sp.sin(_IDENTITY_WILD) ** 2
_SIN_COS_REPLACEMENT = 1 - sp.cos(_IDENTITY_WILD) ** 2


def _preverify() -> tuple[bool, bool]:
    z = sp.Symbol("z")
    cosh_sinh = sp.trigsimp(sp.cosh(z) ** 2 - (1 + sp.sinh(z) ** 2)) == 0
    sin_cos = sp.trigsimp(sp.sin(z) ** 2 + sp.cos(z) ** 2 - 1) == 0
    return bool(cosh_sinh), bool(sin_cos)


_PREVERIFIED_COSH_SINH, _PREVERIFIED_SIN_COS = _preverify()


def _id_cosh_sinh(expr: sp.Expr) -> sp.Expr:
    return expr.replace(_COSH_SINH_PATTERN, _COSH_SINH_REPLACEMENT)


def _id_sin_cos(expr: sp.Expr) -> sp.Expr:
    return expr.replace(_SIN_COS_PATTERN, _SIN_COS_REPLACEMENT)


IDENTITY_RULES: dict[str, IdentityRule] = {
    "id_cosh_sinh": IdentityRule(
        "id_cosh_sinh",
        "cosh/sinh",
        "cosh(z)^2 - sinh(z)^2 = 1",
        "z arbitrary symbolic expression",
        _id_cosh_sinh,
        _COSH_SINH_PATTERN,
        _COSH_SINH_REPLACEMENT,
        _PREVERIFIED_COSH_SINH,
    ),
    "id_sin_cos": IdentityRule(
        "id_sin_cos",
        "sin/cos",
        "sin(z)^2 + cos(z)^2 = 1",
        "z arbitrary symbolic expression",
        _id_sin_cos,
        _SIN_COS_PATTERN,
        _SIN_COS_REPLACEMENT,
        _PREVERIFIED_SIN_COS,
    ),
}


def derivative_rule_ids() -> list[str]:
    return sorted(DERIVATIVE_RULES)


def identity_rule_ids() -> list[str]:
    return sorted(IDENTITY_RULES)


def identity_is_equivalent(rule: IdentityRule, before: sp.Expr, after: sp.Expr) -> bool:
    """Verify an identity rewrite without expensive full-expression trigsimp.

    ``after`` is produced by ``before.replace(rule.pattern, rule.replacement)``,
    so ``before - after`` is a sum of ``coeff * (pattern - replacement)`` terms.
    Applying the same rewrite once more annihilates those terms exactly; this
    fixed-point check only uses structural replacement and ``expand``.
    """
    if not rule.preverified:
        return False
    difference = sp.expand(before - after)
    annihilated = sp.expand(difference.replace(rule.pattern, rule.replacement))
    return annihilated == 0


def rule_catalog() -> dict:
    """JSON-ready catalog shown to the strategy-planning LLM."""
    return {
        "derivative_rules": [
            {
                "rule_id": rule.rule_id,
                "function_type": rule.function_type,
                "expression": rule.expression,
                "condition": rule.condition,
            }
            for rule in DERIVATIVE_RULES.values()
        ],
        "identity_rules": [
            {
                "rule_id": rule.rule_id,
                "function_type": rule.function_type,
                "expression": rule.expression,
                "condition": rule.condition,
                "preverified": rule.preverified,
            }
            for rule in IDENTITY_RULES.values()
        ],
    }
