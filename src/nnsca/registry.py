"""Parameter registry for the NNSCA data model.

A symbol is registered once per (role, name).  This is what keeps the same
mathematical parameter from being re-created as two different SymPy symbols
when several modules construct the same network.
"""

from __future__ import annotations

from collections import defaultdict

import sympy as sp

ROLE_INPUT_COEFFICIENT = "input_coefficient"
ROLE_NODE_WEIGHT = "node_weight"
ROLE_NODE_BIAS = "node_bias"
ROLE_OUTPUT_WEIGHT = "output_weight"
ROLE_OUTPUT_BIAS = "output_bias"
ROLE_SPECIAL_FUNCTION_PARAMETER = "special_function_parameter"
ROLE_PDE_PARAMETER = "pde_parameter"


class ParameterRegistry:
    """Symbol allocator with role tracking and deterministic naming."""

    def __init__(self) -> None:
        self._symbols: dict[tuple[str, str], sp.Symbol] = {}
        self._roles: dict[sp.Symbol, str] = {}
        self._names: dict[sp.Symbol, str] = {}

    def register(self, role: str, name: str, **assumptions) -> sp.Symbol:
        key = (role, name)
        symbol = self._symbols.get(key)
        if symbol is None:
            symbol = sp.Symbol(name, **assumptions)
            self._symbols[key] = symbol
            self._roles[symbol] = role
            self._names[symbol] = name
        return symbol

    def register_many(self, role: str, names: list[str]) -> list[sp.Symbol]:
        return [self.register(role, name) for name in names]

    def role_of(self, symbol: sp.Symbol) -> str | None:
        return self._roles.get(symbol)

    def name_of(self, symbol: sp.Symbol) -> str | None:
        return self._names.get(symbol)

    def all_symbols(self) -> list[sp.Symbol]:
        return list(self._names)

    def by_role(self) -> dict[str, list[sp.Symbol]]:
        grouped: dict[str, list[sp.Symbol]] = defaultdict(list)
        for symbol, role in self._roles.items():
            grouped[role].append(symbol)
        return {role: sorted(grouped[role], key=lambda s: str(s)) for role in grouped}

    def to_dict(self) -> dict:
        return {
            "roles": {
                role: [str(symbol) for symbol in symbols]
                for role, symbols in self.by_role().items()
            },
            "symbol_names": {str(symbol): name for symbol, name in self._names.items()},
        }
