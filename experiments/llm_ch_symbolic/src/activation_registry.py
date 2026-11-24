"""Verified activation-function registry for the Phase 1.5 benchmarks."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class Activation:
    name: str
    apply: object
    derivative_rule_id: str | None
    identity_rule_ids: tuple[str, ...] = ()
    supported: bool = True


def _weierstrass_p(z: sp.Expr) -> sp.Expr:
    """Placeholder for the Maple-inspired Weierstrass node.

    SymPy can differentiate an undefined function, but we do not register a
    closed derivative rule, so this activation is deliberately unsupported.
    """
    return sp.Function("WeierstrassP")(z)


ACTIVATIONS: dict[str, Activation] = {
    "exp": Activation("exp", sp.exp, "der_exp", ()),
    "poly2": Activation("poly2", lambda z: z**2, "der_poly2", ()),
    "sinh": Activation("sinh", sp.sinh, "der_sinh", ("id_cosh_sinh",)),
    "cosh": Activation("cosh", sp.cosh, "der_cosh", ("id_cosh_sinh",)),
    "sin": Activation("sin", sp.sin, "der_sin", ("id_sin_cos",)),
    "cos": Activation("cos", sp.cos, "der_cos", ("id_sin_cos",)),
    "tanh": Activation("tanh", sp.tanh, "der_tanh", ()),
    "weierstrass": Activation(
        "weierstrass", _weierstrass_p, None, (), supported=False
    ),
}


def get_activation(name: str) -> Activation:
    if name not in ACTIVATIONS:
        raise KeyError(f"unknown activation {name!r}")
    return ACTIVATIONS[name]


def apply(name: str, expr: sp.Expr) -> sp.Expr:
    return get_activation(name).apply(expr)


def supported_activation_names() -> list[str]:
    return sorted(name for name, rule in ACTIVATIONS.items() if rule.supported)


def unsupported_activation_names() -> list[str]:
    return sorted(name for name, rule in ACTIVATIONS.items() if not rule.supported)
