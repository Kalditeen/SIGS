"""Focused tests for the minimal SFG + NNSCA [2,1] BBM workflow."""

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


def test_fixed_functions_generate() -> None:
    config = dict(sfg.DEFAULT_CONFIG["generator"])
    config["max_candidates"] = 4
    candidates = sfg.generate_candidates(config)
    expressions = {c.expression for c in candidates}
    assert "tanh(z)" in expressions
    assert "sech(z)**2" in expressions
    assert "exp(-z**2)" in expressions
    assert "sin(z)" in expressions


def test_jacobi_function_representation() -> None:
    expr = sfg._sympify_f("JacobiSN(z, m)")
    assert expr.func is sfg.JacobiSN
    assert expr.args[1] == sfg.M


def test_sech_derivative() -> None:
    z = sfg.Z
    derivative = sp.simplify(sp.diff(sp.sech(z), z))
    assert sp.expand(derivative + sp.tanh(z) * sp.sech(z)) == 0


def test_jacobi_third_derivative() -> None:
    z, m = sfg.Z, sfg.M
    expr = sfg.JacobiCN(z, m)
    third = sp.diff(expr, z, 3)
    # Deriving through fdiff keeps the expression symbolic and nontrivial.
    assert third.has(sfg.JacobiSN, sfg.JacobiCN, sfg.JacobiDN)


def test_expression_serialization_roundtrip() -> None:
    original = sfg._candidate_from_expr("roundtrip", sp.sech(sfg.Z) ** 2)
    restored = sfg._sympify_f(original.expression)
    assert sp.srepr(restored) == sp.srepr(sp.sech(sfg.Z) ** 2)


def test_deduplicate_marks_duplicates() -> None:
    config = dict(sfg.DEFAULT_CONFIG["generator"])
    config["max_candidates"] = 5
    candidates = sfg.generate_candidates(config)
    statuses = [c.duplicate_status for c in candidates]
    assert "unique" in statuses


def test_nnsca_assembly_uses_affine_phase() -> None:
    f = sp.sech(sfg.Z) ** 2
    trial = sfg.C0 + sfg.C1 * f.subs(sfg.Z, sfg.A * sfg.X + sfg.B * sfg.T + sfg.D)
    assert trial.has(sfg.C0, sfg.C1, sfg.A, sfg.B, sfg.D)


def test_bbm_residual_matches_formula() -> None:
    z = sfg.Z
    f = sp.Function("f")
    u = sfg.C0 + sfg.C1 * f(sfg.A * sfg.X + sfg.B * sfg.T + sfg.D)
    residual = sp.expand(sfg._bbm_residual(u))
    phase = sfg.A * sfg.X + sfg.B * sfg.T + sfg.D
    zeta = sp.Symbol("zeta")
    g = f(zeta)
    gp = sp.diff(g, zeta)
    gppp = sp.diff(g, zeta, 3)
    expected = sfg.C1 * (
        (sfg.A + sfg.B + sfg.A * sfg.C0) * gp
        + sfg.A * sfg.C1 * g * gp
        - sfg.A ** 2 * sfg.B * gppp
    ).subs(zeta, phase)
    assert sp.expand(residual - expected) == 0


def test_residual_certification_distinguishes_zero() -> None:
    assert sfg._residual_is_zero(sp.Integer(0)) is True
    assert sfg._residual_is_zero(sfg.X) is False


def test_constraint_extraction_for_polynomial_phase() -> None:
    z = sfg.Z
    u = sfg.C0 + sfg.C1 * (sfg.A * sfg.X + sfg.B * sfg.T + sfg.D)
    residual = sp.expand(sfg._bbm_residual(u))
    equations, basis, error = sfg._extract_coefficient_equations(residual, sfg.X, sfg.T)
    assert error is None
    assert isinstance(equations, list)


def test_end_to_end_quick(tmp_path: Path) -> None:
    result_dir = tmp_path / "results"
    exit_code = sfg.main(["--quick", "--results-dir", str(result_dir)])
    assert exit_code == 0
    exact_path = result_dir / "exact_solutions.json"
    assert exact_path.exists()
    exact = json.loads(exact_path.read_text(encoding="utf-8"))
    assert any(item["source_expression"] == "sech(z)**2" for item in exact)


def test_sech2_constraints_reverified() -> None:
    audit = sfg.audit_exact_solution(
        "sech(z)**2",
        {"b": "-c1/(12*a)", "c0": "-c1/3 - 1 + c1/(12*a**2)"},
    )
    assert audit["status"] == "EXACT_VERIFIED"


def test_tan2_constraints_reverified() -> None:
    audit = sfg.audit_exact_solution(
        "tan(z)**2",
        {"b": "c1/(12*a)", "c0": "2*c1/3 - 1 - c1/(12*a**2)"},
    )
    assert audit["status"] == "EXACT_VERIFIED"


def test_jacobi_cn2_branches_reverified() -> None:
    root = "sqrt(c1*(3*c0*m + 2*c1*m - c1 + 3*m))"
    den = "2*(3*c0*m + 2*c1*m - c1 + 3*m)"
    branches = [
        {"a": f"-{root}/({den})", "b": f"{root}/(6*m)"},
        {"a": f"{root}/({den})", "b": f"-{root}/(6*m)"},
    ]
    for constraints in branches:
        audit = sfg.audit_exact_solution("JacobiCN(z, m)**2", constraints)
        assert audit["status"] == "EXACT_VERIFIED"


def test_jacobi_cn2_branches_equivalent() -> None:
    root = "sqrt(c1*(3*c0*m + 2*c1*m - c1 + 3*m))"
    den = "2*(3*c0*m + 2*c1*m - c1 + 3*m)"
    expr1 = f"c0 + c1*JacobiCN(d - x*{root}/({den}) + t*{root}/(6*m), m)**2"
    expr2 = f"c0 + c1*JacobiCN(d + x*{root}/({den}) - t*{root}/(6*m), m)**2"
    assert sfg._solution_equivalence_key(expr1) == sfg._solution_equivalence_key(expr2)


def test_nonexact_parameter_set_rejected() -> None:
    audit = sfg.audit_exact_solution("sech(z)**2", {"b": "0", "c0": "0"})
    assert audit["status"] != "EXACT_VERIFIED"


def test_constant_trivial_solution_marked() -> None:
    assert sfg._is_trivial_network_solution({sfg.C1: sp.Integer(0)}) is True
    assert sfg._is_trivial_network_solution({sfg.A: sp.Integer(0), sfg.B: sp.Integer(0)}) is True


def test_tan2_domain_restriction_recorded() -> None:
    _conditions, notes = sfg._solution_notes("tan(z)**2", {})
    assert any("pole" in note for note in notes)


def test_exact_statistics_count(tmp_path: Path) -> None:
    result_dir = tmp_path / "results"
    exit_code = sfg.main(["--max-candidates", "30", "--results-dir", str(result_dir)])
    assert exit_code == 0
    exact = json.loads((result_dir / "exact_solutions.json").read_text(encoding="utf-8"))
    failed = json.loads((result_dir / "failed_candidates.json").read_text(encoding="utf-8"))
    generated = json.loads((result_dir / "generated_functions.json").read_text(encoding="utf-8"))
    assert len(generated) == 30
    assert len(exact) == 4
    assert len(failed) == 27
    report = (result_dir / "audit_report.md").read_text(encoding="utf-8")
    assert "distinct exact solutions after equivalence: 3" in report


def test_seed_and_generated_source_counts() -> None:
    config = dict(sfg.DEFAULT_CONFIG["generator"])
    config["max_candidates"] = 6
    candidates = sfg.generate_candidates(config)
    assert sum(1 for c in candidates if c.source_type == "seed") == 4
    assert sum(1 for c in candidates if c.source_type == "generated") == 2


def test_generated_only_mode_excludes_seeds() -> None:
    config = dict(sfg.DEFAULT_CONFIG["generator"])
    config["max_candidates"] = 6
    config["include_seeds"] = False
    candidates = sfg.generate_candidates(config)
    assert all(c.source_type == "generated" for c in candidates)
    assert len(candidates) == 6


def test_generated_only_seed_reproducible() -> None:
    config = dict(sfg.DEFAULT_CONFIG["generator"])
    config["max_candidates"] = 12
    config["include_seeds"] = False
    config["random_seed"] = 101
    first = [c.expression for c in sfg.generate_candidates(dict(config))]
    second = [c.expression for c in sfg.generate_candidates(dict(config))]
    assert first == second


def test_build_trial_2321_hierarchical_shape() -> None:
    trial = sfg.build_trial(sp.tanh(sfg.Z), [2, 3, 2, 1])
    assert trial.has(sfg.X, sfg.T)
    assert trial.has(sp.Symbol("w1_0_0"), sp.Symbol("b1_0"))
    assert trial.has(sp.Symbol("w2_0_0"), sp.Symbol("w_out_0"), sp.Symbol("b_out"))


def test_default_widths_remain_21() -> None:
    assert sfg.DEFAULT_CONFIG["network"]["widths"] == [2, 1]
    trial = sfg.build_trial(sp.tanh(sfg.Z), sfg.DEFAULT_CONFIG["network"]["widths"])
    assert trial.has(sfg.A, sfg.B, sfg.C0, sfg.C1, sfg.D)


def test_build_trial_221_same_function() -> None:
    trial = sfg.build_trial(sp.tanh(sfg.Z), [2, 2, 1])
    assert trial.has(sp.Symbol("w1_0_0"), sp.Symbol("w1_1_0"))
    assert trial.has(sp.Symbol("w_out_0"), sp.Symbol("w_out_1"), sp.Symbol("b_out"))


def test_build_trial_221_different_functions() -> None:
    trial = sfg.build_trial(sp.tanh(sfg.Z), [2, 2, 1], f_exprs=[sp.sech(sfg.Z) ** 2, sp.tan(sfg.Z) ** 2])
    assert trial.has(sp.sech(sp.Symbol("w1_0_0") * sfg.X + sp.Symbol("w1_0_1") * sfg.T + sp.Symbol("b1_0")) ** 2)
    assert trial.has(sp.tan(sp.Symbol("w1_1_0") * sfg.X + sp.Symbol("w1_1_1") * sfg.T + sp.Symbol("b1_1")) ** 2)


def test_function_identity_status() -> None:
    assert sfg._function_identity_status(sp.tanh(sfg.Z)) == "known"
    assert sfg._function_identity_status(sp.exp(sfg.Z)) == "unknown"


def test_two_node_determinant_arithmetic() -> None:
    solution = {
        sp.Symbol("w1_0_0"): 2,
        sp.Symbol("w1_0_1"): 3,
        sp.Symbol("w1_1_0"): 5,
        sp.Symbol("w1_1_1"): 7,
    }
    assert sfg._two_node_determinant(solution) == 2 * 7 - 5 * 3


def test_classify_two_node_branch_nondegenerate() -> None:
    branch = {
        "constraints": {
            "w_out_0": "1",
            "w_out_1": "1",
            "w1_0_0": "1",
            "w1_0_1": "2",
            "w1_1_0": "3",
            "w1_1_1": "4",
        }
    }
    assert sfg._classify_two_node_branch(branch) == "EXACT_TWO_NODE_NONDEGENERATE"


def test_classify_two_node_branch_equivalent() -> None:
    branch = {
        "constraints": {
            "w_out_0": "1",
            "w_out_1": "1",
            "w1_0_0": "1",
            "w1_0_1": "2",
            "w1_1_0": "2",
            "w1_1_1": "4",
        }
    }
    assert sfg._classify_two_node_branch(branch) == "EXACT_TWO_NODE_EQUIVALENT"


def test_classify_two_node_branch_single_node() -> None:
    branch = {
        "constraints": {
            "w_out_0": "1",
            "w_out_1": "0",
            "w1_0_0": "1",
            "w1_0_1": "2",
            "w1_1_0": "3",
            "w1_1_1": "4",
        }
    }
    assert sfg._classify_two_node_branch(branch) == "EXACT_SINGLE_NODE_DEGENERATE"


def test_cross_term_analysis_separates_node_products() -> None:
    trial = sfg.build_trial(sp.tanh(sfg.Z), [2, 2, 1])
    analysis = sfg._cross_term_analysis(trial)
    assert analysis["node_count"] >= 0
    assert "cross_term" in analysis
    assert "single_node_term" in analysis


def test_active_nondegenerate_augmentation_polynomial() -> None:
    w0 = sp.Symbol("w_out_0")
    w1 = sp.Symbol("w_out_1")
    a1 = sp.Symbol("w1_0_0")
    b1 = sp.Symbol("w1_0_1")
    a2 = sp.Symbol("w1_1_0")
    b2 = sp.Symbol("w1_1_1")
    equations = [w0 - 1, w1 - 2, a1 - 1, b1 - 1, a2 - 2, b2 - 1]
    unknowns = [w0, w1, a1, b1, a2, b2]
    augmented, augmented_unknowns, auxiliary, q = sfg._augment_nondegenerate_constraints(
        equations, unknowns
    )
    assert len(augmented) == len(equations) + 1
    assert q in augmented_unknowns
    ok, reason = sfg._is_polynomial_equation_system(augmented, augmented_unknowns)
    assert ok is True
    assert reason is None
