#!/usr/bin/env python3
"""Equation specifications for the generic PDE validation engine."""

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


def _vckdv_residual(u, x, t):
    return sp.diff(u, t) + 6.0 * (1.0 + t) * u * sp.diff(u, x) + (1.0 + t) * sp.diff(u, x, 3)


def _kawahara_residual(u, x, t):
    return (
        sp.diff(u, t)
        + u * sp.diff(u, x)
        + sp.diff(u, x, 3)
        - sp.diff(u, x, 5)
    )


def _boussinesq_residual(u, x, t):
    return (
        sp.diff(u, t, 2)
        - sp.diff(u, x, 2)
        - 3 * sp.diff(u**2, x, 2)
        - sp.diff(u, x, 4)
    )


def _sk_residual(u, x, t):
    return (
        sp.diff(u, t)
        + 45 * u**2 * sp.diff(u, x)
        + 15 * sp.diff(u, x) * sp.diff(u, x, 2)
        + 15 * u * sp.diff(u, x, 3)
        + sp.diff(u, x, 5)
    )


def _vcboussinesq_residual(u, x, t):
    return (
        sp.diff(u, t, 2)
        - sp.diff(u, x, 2)
        - 3 * t * sp.diff(u**2, x, 2)
        - sp.diff(u, x, 4)
    )


VCKDV = PDESpec(
    name="vc-KdV",
    problem_type="VcKdV-1Soliton-1D",
    operators="ut + 6*(1+t)*u*ux + (1+t)*uxxx",
    residual=_vckdv_residual,
    true_solution=2 * sp.sech(X_SYM - 4 * T_SYM - 2 * T_SYM ** 2) ** 2,
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + [
        "x - 4*t - 2*t**2", "x + 4*t + 2*t**2",
    ],
    baseline=["b + a*sech(k*x - w*t - m*t**2)**2"],
    baseline_defaults={"a": "2.0", "b": "0.0", "k": "1.0", "w": "4.0", "m": "2.0"},
    variable_coefficient=True,
)


KAWAHARA = PDESpec(
    name="Kawahara",
    problem_type="Kawahara-1Soliton-1D",
    operators="ut + u*ux + uxxx - uxxxxx",
    residual=_kawahara_residual,
    true_solution=(
        sp.Rational(105, 169)
        * sp.sech((X_SYM - sp.Rational(36, 169) * T_SYM) / (2 * sp.sqrt(13))) ** 4
    ),
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x - 36*t/169"],
    baseline=["a*sech(k*x - w*t)**4"],
    baseline_defaults={
        "a": "0.621301775147929",
        "k": "0.1386750490563073",
        "w": "0.02954212861424585",
    },
)


BOUSSINESQ = PDESpec(
    name="Boussinesq",
    problem_type="Boussinesq-1Soliton-1D",
    operators="utt - uxx - 3*(u**2)_xx - uxxxx",
    residual=_boussinesq_residual,
    true_solution=sp.Rational(3, 2) * sp.sech(sp.sqrt(3) / 2 * (X_SYM - 2 * T_SYM)) ** 2,
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x - 2*t", "x + 2*t"],
    baseline=["a*sech(k*x - w*t)**2"],
    baseline_defaults={
        "a": "1.5",
        "k": "0.8660254037844386",
        "w": "1.7320508075688772",
    },
    second_order_time=True,
)


SAWADA_KOTERA = PDESpec(
    name="Sawada-Kotera",
    problem_type="SawadaKotera-1Soliton-1D",
    operators="ut + 45*u**2*ux + 15*ux*uxx + 15*u*uxxx + uxxxxx",
    residual=_sk_residual,
    true_solution=2 * sp.sech(X_SYM - 16 * T_SYM) ** 2,
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x - 16*t", "x + 16*t"],
    baseline=["a*sech(k*x - w*t)**2"],
    baseline_defaults={"a": "2.0", "k": "1.0", "w": "16.0"},
)


VCBOUSSINESQ = PDESpec(
    name="vc-Boussinesq",
    problem_type="VcBoussinesq-Polynomial-1D",
    operators="utt - uxx - 3*t*(u**2)_xx - uxxxx",
    residual=_vcboussinesq_residual,
    true_solution=X_SYM + T_SYM ** 3,
    seed_functions=COMMON_SEED_FUNCS,
    search_atoms=COMMON_ATOMS + ["x + t**3", "x", "t**3"],
    baseline=["a*x + b*t**3 + c"],
    baseline_defaults={"a": "1.0", "b": "1.0", "c": "0.0"},
    variable_coefficient=True,
    second_order_time=True,
)


ALL_SPECS = [VCKDV, KAWAHARA, BOUSSINESQ, SAWADA_KOTERA, VCBOUSSINESQ]
