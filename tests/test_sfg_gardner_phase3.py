"""Unified regression tests for Gardner phase 3 modules."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts" / "pdes"))

import sfg_bbm_21 as sfg  # noqa: E402
import sfg_families as families  # noqa: E402
import sfg_gardner as gardner  # noqa: E402
import sfg_graph as graph  # noqa: E402
import sfg_reduction as reduction  # noqa: E402


def test_family_streams_cover_required_atoms() -> None:
    elementary = families.generate_family_candidates("elementary", 12, seed=101)
    hyperbolic = families.generate_family_candidates("hyperbolic", 12, seed=101)
    jacobi = families.generate_family_candidates("jacobi", 12, seed=101)
    assert {"z", "z**2", "z**3", "exp(z)", "sin(z)", "cos(z)", "log(z)"} <= {c.expression for c in elementary}
    assert {"sinh(z)", "cosh(z)", "tanh(z)", "sech(z)", "csch(z)", "coth(z)"} <= {c.expression for c in hyperbolic}
    assert {"JacobiSN(z, m)", "JacobiCN(z, m)", "JacobiDN(z, m)"} <= {c.expression for c in jacobi}


def test_family_candidates_include_family_field() -> None:
    candidates = families.generate_family_candidates("jacobi", 4, seed=101)
    assert candidates
    assert all(candidate.family == "jacobi" for candidate in candidates)


def test_family_stream_is_seed_reproducible() -> None:
    first = [c.expression for c in families.generate_family_candidates("hyperbolic", 8, seed=303)]
    second = [c.expression for c in families.generate_family_candidates("hyperbolic", 8, seed=303)]
    assert first == second


def test_original_random_stream_has_no_forced_jacobi_seed() -> None:
    candidates = families.generate_original_random_candidates(12, seed=101)
    assert all(candidate.source_type == "generated" for candidate in candidates)
    assert not any(candidate.expression == "JacobiCN(z,m)" for candidate in candidates)


def test_mixed_stream_keeps_all_families() -> None:
    candidates = families.generate_mixed_family_candidates(12, seed=101)
    assert {candidate.family for candidate in candidates} == {"elementary", "hyperbolic", "jacobi"}


def test_hyperbolic_identity_tanh_squared_plus_sech_squared() -> None:
    z = sfg.Z
    assert sp.simplify(sp.tanh(z) ** 2 + sp.sech(z) ** 2 - 1) == 0


def test_jacobi_derivative_identities() -> None:
    z, m = sp.symbols("z m")
    assert sp.diff(reduction.JacobiSN(z, m), z) == reduction.sn_derivative(z, m)
    assert sp.diff(reduction.JacobiCN(z, m), z) == reduction.cn_derivative(z, m)
    assert sp.diff(reduction.JacobiDN(z, m), z) == reduction.dn_derivative(z, m)


def test_jacobi_square_identities() -> None:
    z, m = sp.symbols("z m")
    sn, cn, dn = reduction.JacobiSN(z, m), reduction.JacobiCN(z, m), reduction.JacobiDN(z, m)
    assert sp.expand(reduction.reduce_jacobi_powers(sn**2 + cn**2 - 1)) == 0
    assert sp.expand(reduction.reduce_jacobi_powers(dn**2 + m * sn**2 - 1)) == 0


def test_graph_rejects_invalid_widths() -> None:
    try:
        graph.LayeredNetwork([1, 1])
    except ValueError:
        pass
    else:
        raise AssertionError("invalid widths were accepted")


def test_graph_21_derivatives_equal_direct() -> None:
    net = graph.LayeredNetwork([2, 1])
    derivatives = net.derivatives()
    direct = sfg.build_trial(sp.tanh(sfg.Z), [2, 1])
    assert sp.expand(direct - derivatives["u"]) == 0
    assert sp.expand(sp.diff(direct, sfg.X) - derivatives["u_x"]) == 0
    assert sp.expand(sp.diff(direct, sfg.T) - derivatives["u_t"]) == 0
    assert sp.expand(sp.diff(direct, sfg.X, 3) - derivatives["u_xxx"]) == 0


def test_graph_deep_derivatives_equal_direct() -> None:
    for widths in ([2, 2, 1], [2, 3, 2, 1]):
        net = graph.LayeredNetwork(widths)
        derivatives = net.derivatives()
        direct = sfg.build_trial(sp.tanh(sfg.Z), widths)
        assert sp.expand(direct - derivatives["u"]) == 0
        assert sp.expand(sp.diff(direct, sfg.X) - derivatives["u_x"]) == 0
        assert sp.expand(sp.diff(direct, sfg.T) - derivatives["u_t"]) == 0
        assert sp.expand(sp.diff(direct, sfg.X, 3) - derivatives["u_xxx"]) == 0


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
    assert audit["certified_zero"] is True


def test_gardner_raw_residual_rejects_wrong_cn_branch() -> None:
    audit = gardner.audit_exact_solution(
        "JacobiCN(z,m)",
        {
            "c0": "-1/2",
            "a": "k",
            "b": "0",
            "d": "0",
            "m": "c1**2/(6*k**2)",
        },
    )
    assert audit["status"] != "EXACT_VERIFIED"
