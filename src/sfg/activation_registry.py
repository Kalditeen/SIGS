"""Activation-function registry for heterogeneous SFG networks.

The registry is intentionally independent of PDE and network code.  Every
entry exposes its name, family, SymPy expression, internal parameters, and
domain notes so a compiler or analysis module never has to guess function
metadata from a string.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from sfg.atoms import ActivationAtom, available_atoms, parse_activation

Z = sp.symbols("z", real=True)
M = sp.symbols("m")

_ACTIVATION_NAMES = {atom.name: atom for atom in available_atoms()}


@dataclass(frozen=True)
class ActivationSpec:
    """Public metadata wrapper around one activation atom."""

    name: str
    family: str
    expression: sp.Expr
    parameter_names: tuple[str, ...]
    parameter_roles: dict[str, str]
    domain: str
    differentiable: bool = True

    def instantiate(self, preactivation: sp.Expr) -> sp.Expr:
        atom = _ACTIVATION_NAMES[self.name]
        return atom.instantiate(preactivation)

    def derivative(self, order: int = 1) -> sp.Expr:
        atom = _ACTIVATION_NAMES[self.name]
        return atom.derivative(order)

    def to_atom(self) -> ActivationAtom:
        return _ACTIVATION_NAMES[self.name]


def _spec_from_atom(atom: ActivationAtom) -> ActivationSpec:
    return ActivationSpec(
        name=atom.name,
        family=atom.family,
        expression=atom.expression,
        parameter_names=tuple(str(param) for param in atom.parameter_symbols),
        parameter_roles={
            str(param): "special_function_parameter"
            for param in atom.parameter_symbols
        },
        domain=atom.domain,
        differentiable=True,
    )


_SPECS = {name: _spec_from_atom(atom) for name, atom in _ACTIVATION_NAMES.items()}


def activation_by_name(name: str) -> ActivationSpec:
    try:
        return _SPECS[name]
    except KeyError as exc:
        raise KeyError(f"unknown activation {name!r}") from exc


def available_activations() -> tuple[ActivationSpec, ...]:
    return tuple(_SPECS.values())


def parse_activation_spec(activation) -> ActivationSpec:
    atom = parse_activation(activation)
    return _SPECS.get(atom.name, _spec_from_atom(atom))
