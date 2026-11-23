"""Focused tests for Phase 3-B representative complex networks."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nnsca.search.automatic_solver import AutomaticSolver, AutomaticSolverConfig  # noqa: E402
from nnsca.search.representative_selector import (  # noqa: E402
    CATEGORY_NAMES,
    select_representative_candidates,
    structure_profile,
)
from sfg.candidate_manager import CandidateManager  # noqa: E402
from sfg.network_ir import NetworkIR  # noqa: E402


def _single_node_ir() -> NetworkIR:
    ir = NetworkIR("single_node")
    ir.add_phase("p1")
    ir.add_compute("h1", "tanh", ["p1"])
    ir.set_linear_output(["h1"])
    return ir


def _two_node_heterogeneous_ir() -> NetworkIR:
    ir = NetworkIR("two_node_heterogeneous")
    ir.add_phase("p1")
    ir.add_phase("p2")
    ir.add_compute("h1", "tanh", ["p1"])
    ir.add_compute("h2", "sin", ["p2"])
    ir.set_linear_output(["h1", "h2"])
    return ir


def _two_layer_ir() -> NetworkIR:
    ir = NetworkIR("two_layer")
    ir.add_phase("p1")
    ir.add_phase("p2")
    ir.add_compute("h1", "tanh", ["p1"])
    ir.add_compute("h2", "cos", ["p2"])
    ir.add_compute("h3", "sin", ["h1", "h2"])
    ir.set_linear_output(["h3"])
    return ir


def _chained_two_layer_ir() -> NetworkIR:
    ir = NetworkIR("chained_two_layer")
    ir.add_phase("p1")
    ir.add_phase("p2")
    ir.add_compute("h1", "tanh", ["p1"])
    ir.add_compute("h2", "cos", ["h1"])
    ir.set_linear_output(["h2"])
    return ir


def _manager(*irs: NetworkIR) -> CandidateManager:
    manager = CandidateManager()
    for ir in irs:
        manager.register(ir, generation_method="test")
    return manager


def test_structure_profile_detects_merge_and_depth() -> None:
    profile = structure_profile(_manager(_two_layer_ir()).records[0])
    assert "C" in profile.categories
    assert "D" in profile.categories
    assert profile.has_merge_node is True
    assert profile.depth == 2


def test_structure_profile_detects_heterogeneous_two_node() -> None:
    profile = structure_profile(_manager(_two_node_heterogeneous_ir()).records[0])
    assert "B" in profile.categories
    assert profile.heterogeneous is True


def test_representative_selection_uses_distinct_candidates_when_requested() -> None:
    manager = _manager(
        _single_node_ir(),
        _two_node_heterogeneous_ir(),
        _two_layer_ir(),
        _chained_two_layer_ir(),
    )
    selected = select_representative_candidates(manager, per_category=1, allow_overlap=False)
    filled_ids = {
        record.candidate_id
        for records in selected.values()
        for record in records
        if records
    }
    assert len(filled_ids) >= 2
    assert selected["D"]
    assert selected["D"][0].candidate_id != selected["C"][0].candidate_id


def test_missing_categories_are_reported_as_empty_lists() -> None:
    selected = select_representative_candidates(_manager(_single_node_ir()))
    assert selected["A"]
    assert selected["B"] == []
    assert selected["E"] == []


def test_complex_batch_continues_after_failure() -> None:
    class FakeStage2:
        def __init__(self):
            self.calls = 0

        def process(self, expression, residual_fn, config, pde_equation=""):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("boom")
            return {
                "symbolic_status": "success",
                "constraint_status": "success",
                "extraction_status": "success",
                "solve_status": "success",
                "verification_status": "EXACT_VERIFIED",
                "exact_solutions": [
                    {
                        "expression": "c0 + c_h1*sin(a_p1*x + b_p1*t + d_p1)",
                        "constraints": {},
                        "residual": "0",
                    }
                ],
                "solutions": [],
                "branch_attempts": [],
                "nontrivial_status": "NONTRIVIAL",
                "substitution_status": "success",
                "identity_verification_status": "verified",
                "failure_reason": None,
                "timing": {},
            }

    manager = _manager(_single_node_ir(), _two_node_heterogeneous_ir())
    selected = select_representative_candidates(manager, allow_overlap=False)
    unique_records = {
        records[0].candidate_id: records[0]
        for records in selected.values()
        if records
    }
    config = AutomaticSolverConfig(candidate_ids=tuple(unique_records))
    run_data = AutomaticSolver(stage2=FakeStage2()).run(manager, config)
    statuses = [result["status"] for result in run_data["results"]]
    assert "RESIDUAL_FAILED" in statuses
    assert "EXACT_VERIFIED" in statuses
    assert len(run_data["results"]) == len(unique_records)


def test_exact_complex_branch_gets_traveling_wave_classification() -> None:
    class FakeStage2:
        def process(self, expression, residual_fn, config, pde_equation=""):
            return {
                "symbolic_status": "success",
                "constraint_status": "success",
                "extraction_status": "success",
                "solve_status": "success",
                "verification_status": "EXACT_VERIFIED",
                "exact_solutions": [
                    {
                        "expression": "c0 + c_h1*tanh(a_p1*x + b_p1*t + d_p1)",
                        "constraints": {},
                        "residual": "0",
                    }
                ],
                "solutions": [],
                "branch_attempts": [],
                "nontrivial_status": "NONTRIVIAL",
                "substitution_status": "success",
                "identity_verification_status": "verified",
                "failure_reason": None,
                "timing": {},
            }

    manager = _manager(_single_node_ir())
    run_data = AutomaticSolver(stage2=FakeStage2()).run(manager, AutomaticSolverConfig())
    wave = run_data["exact_solutions"][0]["traveling_wave"]
    assert wave["classification"] == "TRAVELING_WAVE_CONFIRMED"
    assert wave["wave_speed"] is not None
