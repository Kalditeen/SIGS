"""Minimal PDE input contract for the refactored solver."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import sympy as sp


@dataclass(frozen=True)
class PDESpec:
    """PDE-independent input to residual construction and verification."""

    name: str
    independent_vars: tuple[sp.Symbol, ...]
    residual: Callable[[sp.Expr], sp.Expr]
    equation: str
    required_derivatives: tuple[tuple[sp.Symbol, int], ...] = ()
    pde_parameters: dict[str, sp.Symbol] = None

    def __post_init__(self) -> None:
        if not self.independent_vars:
            raise ValueError("PDESpec requires independent variables")
        if self.pde_parameters is None:
            object.__setattr__(self, "pde_parameters", {})
