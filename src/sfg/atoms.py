"""Activation-atom layer for SFG.

This module intentionally knows nothing about PDEs, networks, or Stage2.  It
only provides a small, traceable library of univariate activation functions
with family, domain, and parameter metadata.  Jacobi functions are first-class
members because they are not interchangeable with elementary or hyperbolic
functions in PDE exact-solution search.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from sigs.jacobi import JacobiCN, JacobiDN, JacobiSN, SYMPY_LOCALS

Z = sp.symbols("z", real=True)
M = sp.symbols("m")

_LOCALS = dict(SYMPY_LOCALS)
_LOCALS["z"] = Z
_LOCALS["m"] = M


@dataclass(frozen=True)
class ActivationAtom:
    """A candidate activation function expressed in the dummy variable ``z``."""

    name: str
    family: str
    expression: sp.Expr
    parameter_symbols: tuple[sp.Symbol, ...]
    domain: str
    nargs: int = 1

    def instantiate(self, preactivation: sp.Expr) -> sp.Expr:
        """Return ``F(preactivation)`` with special-function parameters preserved."""
        return self.expression.subs(Z, preactivation)

    def derivative(self, order: int = 1) -> sp.Expr:
        if order <= 0:
            return self.expression
        return sp.diff(self.expression, Z, order)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "family": self.family,
            "expression": sp.sstr(self.expression),
            "parameters": [str(s) for s in self.parameter_symbols],
            "domain": self.domain,
            "nargs": self.nargs,
        }


def _atom(name: str, family: str, expression: str, domain: str, parameters=()) -> ActivationAtom:
    expr = sp.sympify(expression, locals=_LOCALS)
    parameter_symbols = tuple(
        M if str(param) == "m" else sp.Symbol(str(param)) for param in parameters
    )
    return ActivationAtom(
        name=name,
        family=family,
        expression=expr,
        parameter_symbols=parameter_symbols,
        domain=domain,
        nargs=2 if parameter_symbols else 1,
    )


_ATOM_DEFS: dict[str, ActivationAtom] = {
    "tanh": _atom("tanh", "hyperbolic", "tanh(z)", "real_axis"),
    "sech": _atom("sech", "hyperbolic", "sech(z)", "real_axis"),
    "sech_pow2": _atom("sech_pow2", "hyperbolic", "sech(z)**2", "real_axis"),
    "sinh": _atom("sinh", "hyperbolic", "sinh(z)", "real_axis"),
    "cosh": _atom("cosh", "hyperbolic", "cosh(z)", "real_axis"),
    "tan": _atom("tan", "trigonometric", "tan(z)", "partial_domain"),
    "tan_pow2": _atom("tan_pow2", "trigonometric", "tan(z)**2", "partial_domain"),
    "sin": _atom("sin", "trigonometric", "sin(z)", "real_axis"),
    "cos": _atom("cos", "trigonometric", "cos(z)", "real_axis"),
    "exp": _atom("exp", "elementary", "exp(z)", "real_axis"),
    "log": _atom("log", "elementary", "log(z)", "partial_domain"),
    "JacobiSN": _atom("JacobiSN", "jacobi", "JacobiSN(z, m)", "real_axis", parameters=("m",)),
    "JacobiCN": _atom("JacobiCN", "jacobi", "JacobiCN(z, m)", "real_axis", parameters=("m",)),
    "JacobiDN": _atom("JacobiDN", "jacobi", "JacobiDN(z, m)", "real_axis", parameters=("m",)),
    "JacobiCN_pow2": _atom(
        "JacobiCN_pow2", "jacobi", "JacobiCN(z, m)**2", "real_axis", parameters=("m",)
    ),
}


def available_atoms() -> tuple[ActivationAtom, ...]:
    """Return the immutable activation-atom registry in insertion order."""
    return tuple(_ATOM_DEFS.values())


def atom_by_name(name: str) -> ActivationAtom:
    try:
        return _ATOM_DEFS[name]
    except KeyError as exc:
        raise KeyError(f"unknown activation atom {name!r}") from exc


def parse_activation(activation) -> ActivationAtom:
    """Normalise an atom name, ActivationAtom, or SymPy expression.

    Expressions are matched structurally against the registry so generated
    candidates can round-trip without depending on string formatting.
    """
    if isinstance(activation, ActivationAtom):
        return activation
    if isinstance(activation, str):
        if activation in _ATOM_DEFS:
            return _ATOM_DEFS[activation]
        try:
            expression = sp.sympify(activation, locals=_LOCALS)
        except Exception:
            raise ValueError(f"cannot parse activation expression {activation!r}")
    elif isinstance(activation, sp.Basic):
        expression = activation
    else:
        raise TypeError(f"unsupported activation type: {type(activation)!r}")

    for atom in _ATOM_DEFS.values():
        try:
            if sp.srepr(sp.expand(expression)) == sp.srepr(sp.expand(atom.expression)):
                return atom
        except Exception:
            continue
    return ActivationAtom(
        name="custom",
        family="custom",
        expression=expression,
        parameter_symbols=tuple(
            sorted([s for s in expression.free_symbols if s != Z], key=lambda s: str(s))
        ),
        domain="unknown",
        nargs=2 if expression.free_symbols - {Z} else 1,
    )


JACOBI_FUNCS = (JacobiSN, JacobiCN, JacobiDN)
