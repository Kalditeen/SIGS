"""Focused tests for the Gardner adaptation of SFG + NNSCA."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts" / "pdes"))

import sfg_bbm_21 as sfg  # noqa: E402
import sfg_gardner as gardner  # noqa: E402


def test_gardner_residual_constant_is_zero() -> None:
    u = sp.Integer(3)
    assert sp.expand(gardner.gardner_residual(u)) == 0


def test_gardner_residual_general_function_formula() -> None:
    f = sp.Function("f")
    phase = sfg.A * sfg.X + sfg.B * sfg.T + sfg.D
    u = sfg.C0 + sfg.C1 * f(phase)
    residual = sp.expand(gardner.gardner_residual(u))

    zeta = sp.Symbol("zeta")
    g = f(zeta)
    gp = sp.diff(g, zeta)
    gppp = sp.diff(g, zeta, 3)
    expected = sfg.C1 * (
        (sfg.B + sfg.A * sfg.C0 + sfg.A * sfg.C0**2) * gp
        + sfg.A * sfg.C1 * (1 + 2 * sfg.C0) * g * gp
        + sfg.A * sfg.C1**2 * g**2 * gp
        + sfg.A**3 * gppp
    ).subs(zeta, phase)
    assert sp.expand(residual - expected) == 0


def test_gardner_cubic_term_is_u_squared_times_ux() -> None:
    u = sp.Function("u")(sfg.X, sfg.T)
    residual = gardner.gardner_residual(u, alpha=0, beta=1, gamma=0)
    assert sp.expand(residual - sp.diff(u, sfg.T)) == u**2 * sp.diff(u, sfg.X)
    assert residual != u * sp.diff(u, sfg.X) ** 2


def test_gardner_third_derivative_computed() -> None:
    u = sp.sin(sfg.X) ** 3
    residual = gardner.gardner_residual(u, alpha=0, beta=0, gamma=1)
    assert sp.expand(residual - sp.diff(u, sfg.X, 3)) == 0


def test_travelling_wave_reduces_to_ode_form() -> None:
    # R = d/dz(-cU + U^2/2 + U^3/3 + U'') for z=x-c*t.
    z = sp.Symbol("z", real=True)
    U = sp.Function("U")(z)
    c = sp.Symbol("c", real=True)
    u = U.subs(z, sfg.X - c * sfg.T)
    residual = sp.expand(gardner.gardner_residual(u))
    expected = sp.diff(-c * U + U**2 / 2 + U**3 / 3 + sp.diff(U, z, 2), z)
    assert sp.expand(residual - expected.subs(z, sfg.X - c * sfg.T)) == 0


def test_build_trial_21() -> None:
    trial = sfg.build_trial(sp.sech(sfg.Z) ** 2, [2, 1])
    assert trial.has(sfg.A, sfg.B, sfg.C0, sfg.C1, sfg.D)


def test_build_trial_221() -> None:
    trial = sfg.build_trial(sp.tanh(sfg.Z), [2, 2, 1])
    assert trial.has(sp.Symbol("w_out_0"), sp.Symbol("w_out_1"))
    assert trial.has(sp.Symbol("w1_0_0"), sp.Symbol("w1_1_0"))


def test_build_trial_2321() -> None:
    trial = sfg.build_trial(sp.tanh(sfg.Z), [2, 3, 2, 1])
    assert trial.has(sfg.X, sfg.T)
    assert trial.has(sp.Symbol("w2_0_0"), sp.Symbol("w_out_0"))


def test_known_jacobi_cn_solution_raw_residual() -> None:
    # u = -1/2 + c1*cn(k*(x-c*t) | m),
    # m = c1^2/(6*k^2), c = (4*c1^2 - 12*k^2 - 3)/12.
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
    assert audit["certified_zero"] is True
    assert audit["status"] == "EXACT_VERIFIED"


def test_known_jacobi_cn_solution_wrong_branch_rejected() -> None:
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


def test_tan2_domain_note_recorded() -> None:
    _conditions, notes = gardner._solution_notes("tan(z)**2", {})
    assert any("pole" in note for note in notes)


def test_seed_and_generated_counts_preserved() -> None:
    config = dict(sfg.DEFAULT_CONFIG["generator"])
    config["max_candidates"] = 6
    candidates = sfg.generate_candidates(config)
    assert sum(1 for c in candidates if c.source_type == "seed") == 4
    assert sum(1 for c in candidates if c.source_type == "generated") == 2


def test_gardner_cli_quick_writes_records(tmp_path: Path) -> None:
    result_dir = tmp_path / "gardner"
    exit_code = gardner.main([
        "--quick",
        "--num-candidates", "4",
        "--results-dir", str(result_dir),
    ])
    assert exit_code == 0
    assert (result_dir / "processed_candidates.json").exists()
    records = json.loads((result_dir / "processed_candidates.json").read_text(encoding="utf-8"))
    assert len(records) == 4
    assert (result_dir / "residual_verification.md").exists()
    assert (result_dir / "phase1_report.md").exists()
