#!/usr/bin/env python3
"""Camassa-Holm validation with the generic NNSCA PDE engine.

The dispersionless Camassa-Holm equation used here is

    u_t - u_xxt + 3*u*u_x - 2*u_x*u_xx - u*u_xxx = 0

which is the k = 0 case of the standard CH equation

    u_t + 2*k*u_x - u_xxt + 3*u*u_x - 2*u_x*u_xx - u*u_xxx = 0.

For k = 0 the smooth exponential family

    u(x, t) = a*exp(+-x + w*t),  a and w arbitrary,

is an exact solution family.  The engine no longer injects baseline or
extra-ansatz priors into Stage-I; it explores the prior-free NNSCA phase/role
space and verifies every structurally admissible candidate symbolically.
Each verified exact branch is classified by the CH momentum
m = u - u_xx + k as either zero_momentum or nonzero_momentum.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

import sympy as sp

import pde_common

X_SYM, T_SYM = sp.symbols("x t")
K_SYM = sp.Symbol("k")

CH_COMMON_SEED_FUNCS = [
    ("exp", 7),
    ("tanh", 1),
    ("sech", 15),
    ("sech2", 16),
    ("sin", 8),
    ("cos", 10),
    ("sinh", 3),
    ("cosh", 5),
    ("tan", 17),
    ("JacobiCN", 19),
]

CH_SEARCH_ATOMS = [
    "x - t", "x + t", "x - 4*t",
    "x - t**2", "x + t**2", "x - t**3", "x - exp(t)",
    "x + sin(t)", "cos(x) + t",
    "1/(1 + (x - t)**2)",
    "exp(x)", "exp(-x)", "exp(x - t)", "exp(x + t)",
]

# Broader first-layer phase pool for CH.  The width-3 NNSCA constructor still
# cycles through these templates, so no network-structure change is involved.
CH_FIRST_LAYER_PHASES = [
    "1.000000*x + 1.000000*t + 1.000000",
    "2.000000*x + 1.000000*t + 1.000000",
    "0.500000*x + 1.000000*t + 1.000000",
    "-2.000000*x + 1.000000*t + 1.000000",
    "1.000000*t + 1.000000*cos(2.000000*x + 1.000000) + 1.000000",
    "1.000000*t + 1.000000*sin(2.000000*x + 1.000000) + 1.000000",
    "1.000000*t + 1.000000*cosh(3.000000*x + 1.000000) + 1.000000",
    "1.000000*t + 1.000000*sinh(3.000000*x + 1.000000) + 1.000000",
    "1.000000/(1.000000 + (1.000000*x - 1.000000*t)**2)",
    "1.000000*x + 1.000000*cos(1.000000*t + 1.000000) + 1.000000",
    "1.000000*x + 1.000000*sin(1.000000*t + 1.000000) + 1.000000",
    "1.000000*x**2 + 1.000000*x*t + 1.000000*t**2 + 1.000000",
]


def _ch_residual(u, x, t):
    return (
        sp.diff(u, t)
        + 2 * K_SYM * sp.diff(u, x)
        - sp.diff(u, x, 2, t)
        + 3 * u * sp.diff(u, x)
        - 2 * sp.diff(u, x) * sp.diff(u, x, 2)
        - u * sp.diff(u, x, 3)
    )


def _ch_momentum(u, x, t):
    return u - sp.diff(u, x, 2) + K_SYM




CH = pde_common.PDESpec(
    name="Camassa-Holm",
    problem_type="CH-1D",
    operators="ut + 2*k*u_x - uxxt + 3*u*ux - 2*ux*uxx - u*uxxx = 0",
    residual=_ch_residual,
    momentum=_ch_momentum,
    true_solution=1 + 2 * sp.exp(-X_SYM - T_SYM) + 3 * sp.exp(X_SYM + T_SYM),
    seed_functions=CH_COMMON_SEED_FUNCS,
    search_atoms=CH_SEARCH_ATOMS,
    first_layer_phases=CH_FIRST_LAYER_PHASES,
    baseline=["c + a*exp(m*t - x) + b*exp(n*t + x)"],
    baseline_defaults={"c": "1.0", "a": "2.0", "m": "-1.0", "b": "3.0", "n": "1.0"},
    pde_parameters={"k": K_SYM},
    pde_parameter_defaults={"k": "-1.0"},
    extra_ansatz=[
        "1.000000 + 2.000000*exp(-1.000000*x - 1.000000*t)",
        "1.000000 + 2.000000*exp(-1.000000*x - 1.000000*t) + 3.000000*exp(1.000000*x + 1.000000*t)",
        "1.000000 + 5.000000*exp(1.000000*x - 2.000000*t)",
    ],
)

if __name__ == "__main__":
    pde_common.main(CH, widths=[3])
