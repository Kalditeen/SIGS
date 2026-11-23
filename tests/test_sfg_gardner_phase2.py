"""Phase-2 tests for Gardner JacobiCN automatic recovery."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts" / "pdes"))

import sfg_bbm_21 as sfg  # noqa: E402
import sfg_gardner as gardner  # noqa: E402
import sfg_reduction as reduction  # noqa: E402


def test_cn_first_derivative_identity() -> None:
    z, m = sp.symbols("z m")
    assert sp.diff(reduction.JacobiCN(z, m), z) == reduction.cn_derivative(z, m)


def test_sn_dn_derivative_identities() -> None:
    z, m = sp.symbols("z m")
    assert sp.diff(reduction.JacobiSN(z, m), z) == reduction.sn_derivative(z, m)
    assert sp.diff(reduction.JacobiDN(z, m), z) == reduction.dn_derivative(z, m)


def test_cn_second_derivative_formula() -> None:
    z, m = sp.symbols("z m")
    expected = reduction.cn_second_derivative(z, m)
    actual = sp.diff(reduction.JacobiCN(z, m), z, 2)
    actual_reduced = sp.expand(reduction.reduce_jacobi_powers(actual))
    expected_reduced = sp.expand(reduction.reduce_jacobi_powers(expected))
    assert sp.expand(actual_reduced - expected_reduced) == 0


def test_cn_third_derivative_formula() -> None:
    z, m = sp.symbols("z m")
    expected = reduction.cn_third_derivative(z, m)
    actual = sp.diff(reduction.JacobiCN(z, m), z, 3)
    actual_reduced = sp.expand(reduction.reduce_jacobi_powers(actual))
    expected_reduced = sp.expand(reduction.reduce_jacobi_powers(expected))
    assert sp.expand(actual_reduced - expected_reduced) == 0


def test_affine_chain_rule() -> None:
    x, t, a, b, d, m = sp.symbols("x t a b d m")
    phase = a * x + b * t + d
    left = sp.diff(reduction.JacobiCN(phase, m), x)
    right = a * reduction.cn_derivative(phase, m)
    assert sp.expand(left - right) == 0


def test_reduction_returns_equivalent_jacobi_expression() -> None:
    z, m = sp.symbols("z m")
    expr = reduction.JacobiCN(z, m) ** 2 + reduction.JacobiDN(z, m) ** 2
    reduced, meta = reduction.reduce_special_function_expression(expr, "JacobiCN")
    assert meta["status"] == "success"
    assert sp.expand(reduced - reduction.reduce_jacobi_powers(expr)) == 0


def test_unsupported_family_is_explicit() -> None:
    expr = sp.exp(sp.Symbol("z"))
    _reduced, meta = reduction.reduce_special_function_expression(expr, "no_such_family")
    assert meta["status"] == "unsupported"
    assert meta["failure_reason"] is not None


def test_factorable_solver_recovers_nontrivial_branch() -> None:
    c0, c1, a, b, d, m = sfg.C0, sfg.C1, sfg.A, sfg.B, sfg.D, sfg.M
    equations = [
        sp.expand(-a * c1**2 * (2 * c0 + 1)),
        sp.expand(a * c1 * (-6 * a**2 * m + c1**2)),
        sp.expand(c1 * (4 * a**3 * m + a**3 - a * c0**2 - a * c0 - a * c1**2 - b)),
    ]
    unknowns = sorted([c0, c1, a, b, d, m], key=lambda sym: str(sym))
    solutions = sfg._solve_factorable_system(equations, unknowns)

    target = None
    for solution in solutions:
        if solution.get(c1) == 0 or solution.get(a) == 0:
            continue
        if solution.get(c0) == sp.Rational(-1, 2):
            target = solution
            break
    assert target is not None
    assert sp.expand(target[m] - c1**2 / (6 * a**2)) == 0
    assert sp.expand(target[b] - (a**3 + a / 4 - a * c1**2 / 3)) == 0


def test_automatic_jacobi_cn_recovery(tmp_path: Path) -> None:
    config = copy.deepcopy(sfg.DEFAULT_CONFIG)
    config["network"]["widths"] = [2, 1]
    candidate = sfg._candidate_from_expr(
        "recover_cn", sfg._sympify_f("JacobiCN(z,m)"), source_type="seed", generation_rule="test"
    )
    record = sfg._process_candidate(
        candidate,
        config,
        tmp_path,
        [],
        residual_fn=gardner.residual_fn_for(1, 1, 1),
        pde_equation=gardner.GARDNER_PDE_STR,
        reduce_fn=reduction.reduce_special_function_expression,
    )
    assert record["solve_status"] == "success"
    assert record["reduction_status"] == "success"
    assert record["verification_status"] == "EXACT_VERIFIED"
    assert record["exact_solutions"]

    constraints = record["exact_solutions"][0]["constraints"]
    assert sp.sympify(constraints["c0"]) == sp.Rational(-1, 2)
    assert "c1**2/(6*a**2)" in constraints["m"].replace(" ", "")
    assert "a**3" in constraints["b"].replace(" ", "")


def test_trivial_jacobi_cn_branch_is_classified() -> None:
    branch = sfg._classify_branch({sfg.C1: sp.Integer(0)}, sp.sin(sfg.X))
    assert branch[0] == "CONSTANT_TRIVIAL"
