"""Tests for the IR-aware Phase 3-A automatic solver."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nnsca.search.automatic_solver import AutomaticSolver, AutomaticSolverConfig  # noqa: E402
from sfg.candidate_manager import CandidateManager  # noqa: E402
from sfg.network_ir import NetworkIR  # noqa: E402


def _single_ir(name: str = "single") -> NetworkIR:
    ir = NetworkIR(name)
    ir.add_phase("p1")
    ir.add_compute("h1", "sin", ["p1"])
    ir.set_linear_output(["h1"])
    return ir


def _two_node_ir(name: str = "two_node") -> NetworkIR:
    ir = NetworkIR(name)
    ir.add_phase("p1")
    ir.add_phase("p2")
    ir.add_compute("h1", "tanh", ["p1"])
    ir.add_compute("h2", "sin", ["p2"])
    ir.set_linear_output(["h1", "h2"])
    return ir


def _manager(*irs: NetworkIR) -> CandidateManager:
    manager = CandidateManager()
    for ir in irs:
        manager.register(ir, generation_method="test")
    return manager


class FakeStage2:
    """Queue-backed Stage2 replacement for deterministic unit tests."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def process(self, expression, residual_fn, config, pde_equation=""):
        self.calls += 1
        if not self.responses:
            raise AssertionError("no fake Stage2 response left")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def _exact_response() -> dict:
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


def _raw(statuses: dict) -> dict:
    base = {
        "symbolic_status": "success",
        "constraint_status": "skipped",
        "extraction_status": "skipped",
        "solve_status": "skipped",
        "verification_status": "skipped",
        "exact_solutions": [],
        "solutions": [],
        "branch_attempts": [],
        "nontrivial_status": "skipped",
        "substitution_status": "skipped",
        "identity_verification_status": "skipped",
        "failure_reason": None,
        "timing": {},
    }
    base.update(statuses)
    return base


def test_single_candidate_exact_verified() -> None:
    solver = AutomaticSolver(stage2=FakeStage2([_exact_response()]))
    result = solver.solve_candidate(
        _manager(_single_ir()).records[0],
        AutomaticSolverConfig(),
    )
    assert result["status"] == "EXACT_VERIFIED"
    assert result["parameter_consistency"]["consistent"] is True
    assert result["exact_solutions"]
    assert result["effective_analysis"][0]["classification"] == "EXACT_SINGLE_NODE"


def test_batch_continues_after_one_failure() -> None:
    solver = AutomaticSolver(stage2=FakeStage2([RuntimeError("boom"), _exact_response()]))
    manager = _manager(_single_ir("a"), _two_node_ir("b"))
    run_data = solver.run(manager, AutomaticSolverConfig())
    assert run_data["results"][0]["status"] == "RESIDUAL_FAILED"
    assert run_data["results"][1]["status"] == "EXACT_VERIFIED"
    assert run_data["statistics"]["candidate_total"] == 2


def test_multi_candidate_batch_all_success() -> None:
    solver = AutomaticSolver(stage2=FakeStage2([_exact_response(), _exact_response()]))
    manager = _manager(_single_ir("a"), _two_node_ir("b"))
    run_data = solver.run(manager, AutomaticSolverConfig())
    assert [record["status"] for record in run_data["results"]] == [
        "EXACT_VERIFIED",
        "EXACT_VERIFIED",
    ]


def test_compile_failure_is_isolated() -> None:
    manager = _manager(_single_ir())
    record = manager.records[0]
    record.network_ir.nodes["h1"] = None
    result = AutomaticSolver().solve_candidate(record, AutomaticSolverConfig())
    assert result["status"] == "COMPILE_FAILED"


def test_constraint_failure_maps_correctly() -> None:
    raw = _raw(
        {
            "constraint_status": "unsupported",
            "extraction_status": "unsupported",
            "solve_status": "skipped",
            "verification_status": "SYMBOLIC_UNRESOLVED",
        }
    )
    result = AutomaticSolver(stage2=FakeStage2([raw])).solve_candidate(
        _manager(_single_ir()).records[0],
        AutomaticSolverConfig(),
    )
    assert result["status"] == "CONSTRAINT_FAILED"


def test_solver_timeout_maps_correctly() -> None:
    raw = _raw({"solve_status": "timeout", "verification_status": "SYMBOLIC_UNRESOLVED"})
    result = AutomaticSolver(stage2=FakeStage2([raw])).solve_candidate(
        _manager(_single_ir()).records[0],
        AutomaticSolverConfig(),
    )
    assert result["status"] == "SOLVER_TIMEOUT"


def test_no_solution_maps_correctly() -> None:
    raw = _raw({"solve_status": "success", "verification_status": "NO_SOLUTION"})
    result = AutomaticSolver(stage2=FakeStage2([raw])).solve_candidate(
        _manager(_single_ir()).records[0],
        AutomaticSolverConfig(),
    )
    assert result["status"] == "NO_SOLUTION"


def test_solution_found_but_verification_failed() -> None:
    raw = _raw(
        {
            "solve_status": "success",
            "verification_status": "FAILED",
            "extraction_status": "success",
            "constraint_status": "success",
        }
    )
    result = AutomaticSolver(stage2=FakeStage2([raw])).solve_candidate(
        _manager(_single_ir()).records[0],
        AutomaticSolverConfig(),
    )
    assert result["status"] == "VERIFICATION_FAILED"


def test_parameter_roles_are_preserved_without_stage2() -> None:
    config = AutomaticSolverConfig(full_verification=False)
    result = AutomaticSolver().solve_candidate(_manager(_two_node_ir()).records[0], config)
    assert result["status"] == "COMPILED"
    consistency = result["parameter_consistency"]
    assert consistency["consistent"] is True
    assert consistency["missing_from_ir"] == []
    assert result["parameter_roles"]


def test_effective_network_analysis_is_attached() -> None:
    solver = AutomaticSolver(stage2=FakeStage2([_exact_response()]))
    result = solver.solve_candidate(
        _manager(_two_node_ir()).records[0],
        AutomaticSolverConfig(),
    )
    assert result["status"] == "EXACT_VERIFIED"
    assert result["effective_analysis"][0]["classification"] in {
        "EXACT_SINGLE_NODE",
        "EXACT_DEGENERATE_MULTI_NODE",
        "EXACT_NONDEGENERATE_MULTI_NODE",
        "EXACT_TRIVIAL",
    }


def test_save_run_writes_expected_files(tmp_path: Path) -> None:
    solver = AutomaticSolver(stage2=FakeStage2([_exact_response()]))
    run_data = solver.run(_manager(_single_ir()), AutomaticSolverConfig())
    run_dir = AutomaticSolver.save_run(run_data, AutomaticSolverConfig(), tmp_path)
    for filename in (
        "run_config.json",
        "candidate_results.json",
        "exact_solutions.json",
        "statistics.json",
        "run_report.md",
    ):
        assert (run_dir / filename).exists()
