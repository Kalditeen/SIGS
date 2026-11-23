"""Focused regression tests for Gardner phase 4."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts" / "pdes"))

import sfg_bbm_21 as sfg  # noqa: E402
import sfg_dag as dag  # noqa: E402
import sfg_families as families  # noqa: E402
import sfg_gardner as gardner  # noqa: E402
import sfg_reduction as reduction  # noqa: E402


def test_family_signature_detects_mixed_expression() -> None:
    signature = families.family_signature("tanh(z) + JacobiCN(z, m)")
    assert signature == {"hyperbolic", "jacobi"}


def test_true_mixed_candidate_requires_two_families() -> None:
    true_mixed = sfg._candidate_from_expr(
        "mixed", sfg._sympify_f("tanh(z) + JacobiCN(z,m)"), generation_rule="explicit"
    )
    jacobi_only = sfg._candidate_from_expr(
        "single", sfg._sympify_f("JacobiCN(z,m)"), generation_rule="explicit"
    )
    assert families.is_true_mixed_candidate(true_mixed) is True
    assert families.is_true_mixed_candidate(jacobi_only) is False


def test_dag_derivatives_equal_direct_for_all_supported_widths() -> None:
    for widths in ([2, 1], [2, 2, 1], [2, 3, 1], [2, 3, 2, 1]):
        for activation in ("tanh(z)", "sech(z)", "JacobiCN(z,m)"):
            network = dag.NetworkDAG(widths, activation)
            derivatives = network.derivatives(expand=True)
            direct = sfg.build_trial(network.activation, widths)
            assert sp.expand(direct - derivatives["u"]) == 0
            assert sp.expand(sp.diff(direct, sfg.X) - derivatives["u_x"]) == 0
            assert sp.expand(sp.diff(direct, sfg.T) - derivatives["u_t"]) == 0
            assert sp.expand(sp.diff(direct, sfg.X, 3) - derivatives["u_xxx"]) == 0


def test_lazy_expansion_is_smaller_for_deep_network() -> None:
    network = dag.NetworkDAG([2, 3, 2, 1], "tanh(z)")
    lazy_length = len(sp.sstr(network.derivatives(expand=False)["u_xxx"]))
    expanded_length = len(sp.sstr(network.derivatives(expand=True)["u_xxx"]))
    assert lazy_length < expanded_length


def test_dag_shares_intermediate_nodes() -> None:
    network = dag.NetworkDAG([2, 3, 2, 1], "tanh(z)")
    # The two second-layer nodes both reference the first hidden layer nodes.
    assert all(node.children for node in network.layers[0])


def test_dag_gardner_residual_matches_direct() -> None:
    network = dag.NetworkDAG([2, 1], "JacobiCN(z,m)")
    direct = sfg.build_trial(network.activation, [2, 1])
    assert sp.expand(network.residual(expand=True) - gardner.gardner_residual(direct)) == 0


def test_dag_residual_constraint_interface_returns_equations() -> None:
    network = dag.NetworkDAG([2, 1], "JacobiCN(z,m)")
    residual = network.residual(expand=True)
    equations, basis, error = sfg._extract_coefficient_equations(residual, sfg.X, sfg.T)
    assert error is None
    assert isinstance(equations, list)
    assert basis


def test_jacobi_derivative_rules_remain_correct() -> None:
    z, m = sp.symbols("z m")
    assert sp.diff(reduction.JacobiSN(z, m), z) == reduction.sn_derivative(z, m)
    assert sp.diff(reduction.JacobiCN(z, m), z) == reduction.cn_derivative(z, m)
    assert sp.diff(reduction.JacobiDN(z, m), z) == reduction.dn_derivative(z, m)


def test_gardner_raw_residual_certifies_known_cn_solution() -> None:
    audit = gardner.audit_exact_solution(
        "JacobiCN(z,m)",
        {
            "c0": "-1/2",
            "a": "k",
            "b": "-k*(4*c1**2 - 12*k**2 - 3)/12",
            "d": "0",
            "m": "c1**2/(6*k**2)",
        },
    )
    assert audit["status"] == "EXACT_VERIFIED"


def test_failure_classification_distinguishes_trivial_branch() -> None:
    assert sfg._classify_branch({sfg.C1: sp.Integer(0)}, sp.sin(sfg.X))[0] == "CONSTANT_TRIVIAL"
