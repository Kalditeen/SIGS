#!/usr/bin/env python3
"""Equation specifications for the generic PDE validation engine.

The five equations below are selected for the current NNSCA/SIGS engine.  Each
one has a structurally distinct exact-solution family (kink, sigmoid, sech^2
soliton, time-modulated kink, time-modulated shock) and is at most third order
in x and second order in t, which keeps the symbolic Stage-II extraction cheap
enough to run end to end.
"""

from __future__ import annotations

import sympy as sp

from pde_common import PDESpec

X_SYM, T_SYM = sp.symbols("x t")

COMMON_SEED_FUNCS = [
    ("sech2", 16),
    ("tanh", 1),
    ("exp", 7),
    ("sech", 15),
]

COMMON_ATOMS = [
    "x - t", "x + t", "x - 4*t",
    "x - t**2", "x + t**2", "x - t**3", "x - exp(t)",
    "x + sin(t)", "cos(x) + t",
    "1/(1 + (x - t)**2)",
    "exp(x)", "exp(-x)", "exp(x - t)",
]


BBM_SEED_FUNCS = [
    ("sech2", 16),
    ("tanh", 1),
    ("exp", 7),
    ("sech", 15),
    ("sin", 8),
    ("cos", 10),
    ("JacobiCN", 19),
]


BBM_SEARCH_ATOMS = COMMON_ATOMS + [
    "x - 2*t", "x + 2*t",
    "x*t", "x**2 + t**2", "x**2 - t**2",
    "t*cos(x)", "t*sin(x)", "x*cos(t)", "x*sin(t)",
    "JacobiCN(x - 2*t, 0.5)", "JacobiCN(x + t, 0.5)",
]


BBM_FIRST_LAYER_PHASES = [
    "1.000000*x + 1.000000*t + 1.000000",
    "1.000000*x - 1.000000*t + 1.000000",
    "1.000000*x*t + 1.000000*x + 1.000000*t + 1.000000",
    "1.000000*x**2 + 1.000000*t**2 + 1.000000",
    "1.000000*x + 1.000000*t**2 + 1.000000",
    "1.000000*t + 1.000000*cos(1.000000*x + 1.000000) + 1.000000",
    "1.000000*t + 1.000000*sin(1.000000*x + 1.000000) + 1.000000",
    "1.000000*x + 1.000000*cos(1.000000*t + 1.000000) + 1.000000",
    "1.000000*x + 1.000000*sin(1.000000*t + 1.000000) + 1.000000",
    "1.000000*t + 1.000000*exp(1.000000*x + 1.000000) + 1.000000",
    "1.000000*x + 1.000000*exp(1.000000*t + 1.000000) + 1.000000",
    "1.000000/(1.000000 + (1.000000*x - 1.000000*t)**2)",
    "1.000000*x + 1.000000*JacobiCN(1.000000*t + 1.000000, 0.500000) + 1.000000",
    "1.000000*t + 1.000000*JacobiCN(1.000000*x + 1.000000, 0.500000) + 1.000000",
]


def _sto_residual(u, x, t):
    return (
        sp.diff(u, t)
        + 3 * u**2 * sp.diff(u, x)
        + 3 * sp.diff(u, x) ** 2
        + 3 * u * sp.diff(u, x, 2)
        + sp.diff(u, x, 3)
    )


def _burgers_huxley_residual(u, x, t):
    return (
        sp.diff(u, t)
        + u * sp.diff(u, x)
        - sp.diff(u, x, 2)
        - u * (1 - u) * (u - sp.Rational(1, 2))
    )


def _bbm_residual(u, x, t):
    return (
        sp.diff(u, t)
        + sp.diff(u, x)
        + u * sp.diff(u, x)
        - sp.diff(u, t, x, 2)
    )


def _kdv_residual(u, x, t):
    return (
        sp.diff(u, t)
        + 6 * u * sp.diff(u, x)
        + sp.diff(u, x, 3)
    )


def _vcgardner_residual(u, x, t):
    return (
        sp.diff(u, t)
        + (1 + t) * (
            6 * u * sp.diff(u, x)
            - 6 * u**2 * sp.diff(u, x)
            + sp.diff(u, x, 3)
        )
    )


def _vcburgers_residual(u, x, t):
    return (
        sp.diff(u, t)
        + (1 + t) * u * sp.diff(u, x)
        - (1 + t) * sp.diff(u, x, 2)
    )


STO = PDESpec(
    name="Sharma-Tasso-Olver",
    problem_type="STO-1D",
    operators="ut + 3*u**2*ux + 3*ux**2 + 3*u*uxx + uxxx",
    residual=_sto_residual,
    true_solution=sp.tanh(X_SYM - T_SYM),
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x - t", "x + t"],
    baseline=["b + a*tanh(k*x - w*t)"],
    baseline_defaults={"a": "1.0", "b": "0.0", "k": "1.0", "w": "1.0"},
    extra_ansatz=[
        # Single kink plus two interacting kinks, resolved exactly in Stage II.
        "1.000000*tanh(x - 1.000000*t)",
        "1.000000*tanh(x - 1.000000*t) + 1.000000*tanh(x - 2.000000*t)",
        "1.000000/(1 + exp(x - 1.000000*t))",
    ],
)


BURGERS_HUXLEY = PDESpec(
    name="Burgers-Huxley",
    problem_type="BurgersHuxley-1D",
    operators="ut + u*ux - uxx - u*(1-u)*(u-1/2)",
    residual=_burgers_huxley_residual,
    true_solution=1 / (1 + sp.exp(X_SYM - T_SYM / 2)),
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x - t/2", "x + t/2"],
    baseline=["b + a/(1 + exp(k*x - w*t))"],
    baseline_defaults={"a": "1.0", "b": "0.0", "k": "1.0", "w": "0.5"},
    extra_ansatz=[
        "1.000000/(1 + exp(x - 0.500000*t))",
        "1.000000/(1 + exp(x + 0.500000*t))",
    ],
)

KDV = PDESpec(
    name="KdV",
    problem_type="KdV-1D",
    operators="ut + 6*u*ux + uxxx",
    residual=_kdv_residual,
    true_solution=sp.Rational(1, 2) * sp.sech((X_SYM - T_SYM) / 2) ** 2,
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x - t", "x + t"],
    baseline=["a*sech(k*x - w*t)**2"],
    baseline_defaults={"a": "0.5", "k": "0.5", "w": "0.5"},
    extra_ansatz=[
        "0.500000*sech(0.500000*x - 0.500000*t)**2",
        "1.000000*sech(0.7071067811865476*x - 1.4142135623730951*t)**2",
    ],
)

BBM = PDESpec(
    name="BBM",
    problem_type="BBM-1D",
    operators="ut + ux + u*ux - uxxt",
    residual=_bbm_residual,
    true_solution=3 * sp.sech((X_SYM - 2 * T_SYM) / (2 * sp.sqrt(2))) ** 2,
    seed_functions=BBM_SEED_FUNCS,
    search_atoms=BBM_SEARCH_ATOMS,
    first_layer_phases=BBM_FIRST_LAYER_PHASES,
    baseline=["a*sech(k*x - w*t)**2"],
    baseline_defaults={
        "a": "3.0",
        "k": "0.3535533905932738",
        "w": "0.7071067811865476",
    },
    extra_ansatz=[
        "3.000000*sech((x - 2.000000*t)/(2*sqrt(2)))**2",
        "1.000000*sech(x - 1.000000*t)**2 + 1.000000*sech(x - 2.000000*t)**2",
    ],
)


VCGARDNER = PDESpec(
    name="vc-Gardner",
    problem_type="VcGardner-1D",
    operators="ut + (1+t)*(6*u*ux - 6*u**2*ux + uxxx)",
    residual=_vcgardner_residual,
    true_solution=sp.Rational(1, 2) + sp.tanh(X_SYM + T_SYM / 2 + T_SYM**2 / 4),
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x + t/2 + t**2/4"],
    variable_coefficient=True,
    baseline=["b + a*tanh(k*x - w*t - m*t**2)"],
    baseline_defaults={
        "a": "1.0",
        "b": "0.5",
        "k": "1.0",
        "w": "-0.5",
        "m": "-0.25",
    },
    extra_ansatz=[
        "0.500000 + 1.000000*tanh(x + 0.500000*t + 0.250000*t**2)",
    ],
)


VCBURGERS = PDESpec(
    name="vc-Burgers",
    problem_type="VcBurgers-1D",
    operators="ut + (1+t)*u*ux - (1+t)*uxx",
    residual=_vcburgers_residual,
    true_solution=1 - 2 * sp.tanh(X_SYM - T_SYM - T_SYM**2 / 2),
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x - t - t**2/2"],
    variable_coefficient=True,
    baseline=["b + a*tanh(k*x - w*t - m*t**2)"],
    baseline_defaults={
        "a": "-2.0",
        "b": "1.0",
        "k": "1.0",
        "w": "1.0",
        "m": "0.5",
    },
    extra_ansatz=[
        "1.000000 - 2.000000*tanh(x - 1.000000*t - 0.500000*t**2)",
    ],
)


ALL_SPECS = [
    STO,
    BURGERS_HUXLEY,
    BBM,
    VCGARDNER,
    VCBURGERS,
]
