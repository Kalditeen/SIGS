"""IR-aware automatic solver for Gardner candidates produced by Phase 2.

This module does not reimplement Stage2.  It loads NetworkIR candidates,
recompiles them, runs the existing Stage2 adapter, and then performs effective
network analysis on verified branches.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[3]
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
SRC_DIR = REPO_ROOT / "src"
for path in (PDES_DIR, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import sfg_bbm_21 as sfg  # noqa: E402

from nnsca.adapter import Stage2Adapter  # noqa: E402
from nnsca.analysis.traveling_wave import classify_traveling_wave  # noqa: E402
from nnsca.analysis.effective_network import analyze_effective_network  # noqa: E402
from nnsca.compiler.ansatz_compiler import AnsatzCompiler  # noqa: E402
from pdes.gardner import gardner_residual  # noqa: E402
from sfg.architecture_utils import hidden_depth  # noqa: E402
from sfg.candidate_manager import CandidateManager, CandidateRecord  # noqa: E402

X, T = sfg.X, sfg.T


@dataclass
class AutomaticSolverConfig:
    """Selection and solver bounds for one automatic run."""

    max_candidates: int | None = None
    candidate_ids: tuple[str, ...] = ()
    seed: int | None = None
    min_depth: int | None = None
    max_depth: int | None = None
    min_nodes: int | None = None
    max_nodes: int | None = None
    max_expression_nodes: int | None = 4000
    full_verification: bool = True
    extract_timeout: float = 8.0
    solve_timeout: float = 8.0
    residual_timeout: float = 8.0
    verify_timeout: float = 8.0


class AutomaticSolver:
    """Orchestrate CandidateRecord -> compiler -> Stage2 -> verification."""

    def __init__(
        self,
        stage2: Stage2Adapter | None = None,
        compiler: AnsatzCompiler | None = None,
    ) -> None:
        self.stage2 = stage2 or Stage2Adapter()
        self.compiler = compiler or AnsatzCompiler()

    def select_records(
        self,
        manager: CandidateManager,
        config: AutomaticSolverConfig,
    ) -> list[CandidateRecord]:
        records = manager.unique_records()
        if config.candidate_ids:
            wanted = set(config.candidate_ids)
            records = [record for record in records if record.candidate_id in wanted]
        if config.min_depth is not None or config.max_depth is not None:
            filtered = []
            for record in records:
                depth = hidden_depth(record.network_ir)
                if config.min_depth is not None and depth < config.min_depth:
                    continue
                if config.max_depth is not None and depth > config.max_depth:
                    continue
                filtered.append(record)
            records = filtered
        if config.min_nodes is not None or config.max_nodes is not None:
            filtered = []
            for record in records:
                node_count = len(record.network_ir.nodes)
                if config.min_nodes is not None and node_count < config.min_nodes:
                    continue
                if config.max_nodes is not None and node_count > config.max_nodes:
                    continue
                filtered.append(record)
            records = filtered
        if config.max_candidates is not None:
            records = records[: config.max_candidates]
        return records

    def run(
        self,
        manager: CandidateManager,
        config: AutomaticSolverConfig | None = None,
    ) -> dict:
        config = config or AutomaticSolverConfig()
        records = self.select_records(manager, config)
        results = [self.solve_candidate(record, config) for record in records]
        exact_solutions = []
        for result in results:
            for branch in result.get("exact_solutions", []):
                exact_solutions.append({
                    "candidate_id": result["candidate_id"],
                    "structure_signature": result["structure_signature"],
                    "expression": branch["expression"],
                    "constraints": branch["constraints"],
                    "residual": branch.get("residual", "0"),
                    "effective_analysis": branch.get("effective_analysis"),
                    "traveling_wave": self._classify_exact_expression(branch["expression"]),
                })
        statistics = self._statistics(results, exact_solutions)
        return {
            "results": results,
            "exact_solutions": exact_solutions,
            "statistics": statistics,
        }

    def solve_candidate(
        self,
        record: CandidateRecord,
        config: AutomaticSolverConfig,
    ) -> dict:
        started = time.perf_counter()
        try:
            network_ir_dict = record.network_ir.to_dict()
        except Exception as exc:
            network_ir_dict = {"serialization_error": f"{type(exc).__name__}: {exc}"}
        result = {
            "candidate_id": record.candidate_id,
            "parent_candidate_id": record.parent_candidate_id,
            "structure_signature": record.structure_signature,
            "random_seed": record.random_seed,
            "network_ir": network_ir_dict,
            "expression": None,
            "unknown_parameters": [],
            "parameter_roles": {},
            "parameter_consistency": {},
            "status": "GENERATED",
            "stage2_record": None,
            "exact_solutions": [],
            "effective_analysis": [],
            "degeneracy_status": "UNKNOWN",
            "failure_reason": None,
            "timing": {},
        }

        # Compile from IR, not from the persisted expression string.
        try:
            compiled = self.compiler.compile_ir(record.network_ir)
            expression = compiled.expression
            result["expression"] = sp.sstr(expression)
            result["unknown_parameters"] = [
                str(symbol) for symbol in compiled.candidate.unknown_parameters
            ]
            result["parameter_roles"] = compiled.candidate.parameter_roles
        except Exception as exc:
            result["status"] = "COMPILE_FAILED"
            result["failure_reason"] = f"{type(exc).__name__}: {exc}"
            result["timing"]["total"] = time.perf_counter() - started
            return result

        result["status"] = "COMPILED"
        result["parameter_consistency"] = self._parameter_consistency(record, expression)

        node_count = sp.count_ops(expression)
        result["expression_node_count"] = int(node_count)
        if config.max_expression_nodes is not None and node_count > config.max_expression_nodes:
            result["status"] = "COMPILED"
            result["failure_reason"] = (
                f"expression has {node_count} operations; "
                f"max_expression_nodes={config.max_expression_nodes}"
            )
            result["timing"]["total"] = time.perf_counter() - started
            return result

        if not config.full_verification:
            result["status"] = "COMPILED"
            result["failure_reason"] = "full verification disabled"
            result["timing"]["total"] = time.perf_counter() - started
            return result

        solver_config = {
            "solver": {
                "extract_timeout": config.extract_timeout,
                "solve_timeout": config.solve_timeout,
                "residual_timeout": config.residual_timeout,
                "verify_timeout": config.verify_timeout,
            }
        }

        try:
            stage2_record = self.stage2.process(
                expression,
                gardner_residual,
                solver_config,
                pde_equation="u_t + u*u_x + u**2*u_x + u_xxx = 0",
            )
        except Exception as exc:
            result["status"] = "RESIDUAL_FAILED"
            result["failure_reason"] = f"Stage2 adapter raised {type(exc).__name__}: {exc}"
            result["timing"]["total"] = time.perf_counter() - started
            return result

        result["stage2_record"] = stage2_record
        result["status"] = self._map_status(stage2_record)
        if stage2_record.get("verification_status") != "EXACT_VERIFIED" and result.get("failure_reason") is None:
            result["failure_reason"] = stage2_record.get("failure_reason")

        if stage2_record.get("verification_status") == "EXACT_VERIFIED":
            for branch in stage2_record.get("exact_solutions", []):
                effective = self._effective_analysis(record, branch)
                branch_with_analysis = dict(branch)
                branch_with_analysis["effective_analysis"] = effective
                result["exact_solutions"].append(branch_with_analysis)
                result["effective_analysis"].append(effective)
            result["degeneracy_status"] = self._degeneracy_status(result["effective_analysis"])

        result["timing"] = dict(stage2_record.get("timing", {}))
        result["timing"]["total"] = time.perf_counter() - started
        return result

    def _parameter_consistency(self, record: CandidateRecord, expression: sp.Expr) -> dict:
        ir_parameters = {str(symbol) for symbol in record.network_ir.parameter_symbols()}
        expression_unknowns = sorted(
            str(symbol)
            for symbol in expression.free_symbols
            if symbol not in (X, T)
        )
        roles = record.network_ir.parameter_roles()
        special = set(roles.get("special_function_parameter", []))
        unused = sorted(ir_parameters - set(expression_unknowns))
        missing = sorted(set(expression_unknowns) - ir_parameters)
        return {
            "ir_parameters": sorted(ir_parameters),
            "expression_unknowns": expression_unknowns,
            "unused_ir_parameters": unused,
            "missing_from_ir": missing,
            "special_parameters": sorted(special),
            "consistent": not missing,
        }

    def _effective_analysis(self, record: CandidateRecord, branch: dict) -> dict:
        constraints: dict[sp.Symbol, sp.Expr] = {}
        parse_errors = []
        for key, value in branch.get("constraints", {}).items():
            try:
                constraints[sp.Symbol(key)] = sp.sympify(value)
            except Exception as exc:
                parse_errors.append(f"{key}: {type(exc).__name__}: {exc}")
        try:
            effective = analyze_effective_network(
                record.network_ir,
                constraints,
                compiler=self.compiler,
            )
            return {
                "classification": effective.classification,
                "active_nodes": effective.active_nodes,
                "unreachable_nodes": effective.unreachable_nodes,
                "inactive_edges": effective.inactive_edges,
                "inactive_outputs": effective.inactive_outputs,
                "reduced_expression": effective.reduced_expression,
                "reasons": effective.reasons,
                "parse_errors": parse_errors,
            }
        except Exception as exc:
            return {
                "classification": "UNKNOWN",
                "parse_errors": parse_errors,
                "error": f"{type(exc).__name__}: {exc}",
            }

    @staticmethod

    @staticmethod
    def _classify_exact_expression(expression_str: str) -> dict:
        try:
            expression = sfg._sympify_xt(expression_str)
            result = classify_traveling_wave(expression, X, T)
            if result.get("wave_speed") is not None:
                result = dict(result)
                result["wave_speed"] = sp.sstr(result["wave_speed"])
            return result
        except Exception as exc:
            return {
                "classification": "UNKNOWN",
                "wave_speed": None,
                "reason": f"classification failed: {type(exc).__name__}: {exc}",
            }

    @staticmethod
    def _map_status(stage2_record: dict) -> str:
        verification = stage2_record.get("verification_status")
        solve = stage2_record.get("solve_status")
        extraction = stage2_record.get("extraction_status")
        constraint = stage2_record.get("constraint_status")

        if verification == "EXACT_VERIFIED":
            return "EXACT_VERIFIED"
        if solve == "timeout":
            return "SOLVER_TIMEOUT"
        if verification == "NO_SOLUTION":
            return "NO_SOLUTION"
        if solve == "success":
            return "SOLUTION_FOUND" if verification not in ("FAILED", "SYMBOLIC_UNRESOLVED") else "VERIFICATION_FAILED"
        if extraction in ("timeout", "unsupported") or constraint in ("timeout", "unsupported"):
            return "CONSTRAINT_FAILED" if solve not in ("timeout",) else "SOLVER_TIMEOUT"
        if verification in ("SYMBOLIC_UNRESOLVED",):
            return "CONSTRAINT_FAILED"
        return "CONSTRAINT_FAILED"

    @staticmethod
    def _degeneracy_status(effective_analyses: list[dict]) -> str:
        if not effective_analyses:
            return "UNKNOWN"
        classifications = {item.get("classification") for item in effective_analyses}
        if classifications == {"EXACT_NONDEGENERATE_MULTI_NODE"}:
            return "NONDEGENERATE"
        if "UNKNOWN" in classifications or any(item.get("error") for item in effective_analyses):
            return "UNKNOWN"
        return "DEGENERATE"

    @staticmethod
    def _statistics(results: list[dict], exact_solutions: list[dict]) -> dict:
        status_counts: dict[str, int] = {}
        degeneracy_counts: dict[str, int] = {}
        for result in results:
            status = result.get("status", "UNKNOWN")
            status_counts[status] = status_counts.get(status, 0) + 1
            degeneracy = result.get("degeneracy_status", "UNKNOWN")
            degeneracy_counts[degeneracy] = degeneracy_counts.get(degeneracy, 0) + 1
        total_wall = sum(float(result.get("timing", {}).get("total", 0.0)) for result in results)
        return {
            "candidate_total": len(results),
            "status_counts": status_counts,
            "exact_candidates": sum(1 for result in results if result.get("status") == "EXACT_VERIFIED"),
            "exact_branches": len(exact_solutions),
            "degeneracy_counts": degeneracy_counts,
            "total_wall_seconds": total_wall,
        }

    @staticmethod
    def save_run(
        run_data: dict,
        config: AutomaticSolverConfig,
        output_dir: str | Path,
        run_id: str | None = None,
    ) -> Path:
        output_dir = Path(output_dir)
        run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = output_dir / f"run_{run_id}"
        run_dir.mkdir(parents=True, exist_ok=True)

        (run_dir / "run_config.json").write_text(
            json.dumps(
                {
                    "max_candidates": config.max_candidates,
                    "candidate_ids": list(config.candidate_ids),
                    "seed": config.seed,
                    "min_depth": config.min_depth,
                    "max_depth": config.max_depth,
                    "min_nodes": config.min_nodes,
                    "max_nodes": config.max_nodes,
                    "max_expression_nodes": config.max_expression_nodes,
                    "full_verification": config.full_verification,
                    "timeouts": {
                        "extract": config.extract_timeout,
                        "solve": config.solve_timeout,
                        "residual": config.residual_timeout,
                        "verify": config.verify_timeout,
                    },
                    "python_version": sys.version.split()[0],
                    "sympy_version": sp.__version__,
                    "pde": "Gardner u_t + u*u_x + u**2*u_x + u_xxx = 0",
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (run_dir / "candidate_results.json").write_text(
            json.dumps(run_data["results"], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (run_dir / "exact_solutions.json").write_text(
            json.dumps(run_data["exact_solutions"], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (run_dir / "statistics.json").write_text(
            json.dumps(run_data["statistics"], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        lines = [
            "# Phase 3-A Automatic Solving Report",
            "",
            "Raw Stage2 records are retained in `candidate_results.json`.",
            "Only branches whose raw Gardner residual was symbolically certified",
            "zero are listed as exact.",
            "",
            "## Summary",
            "",
        ]
        for key, value in run_data["statistics"].items():
            lines.append(f"- {key}: {value}")
        lines.append("")
        lines.append("## Candidate Results")
        lines.append("")
        lines.append("| candidate | status | degeneracy | failure |")
        lines.append("|---|---|---|---|")
        for result in run_data["results"]:
            lines.append(
                f"| {result['candidate_id']} | {result['status']} "
                f"| {result.get('degeneracy_status', 'UNKNOWN')} "
                f"| {result.get('failure_reason') or ''} |"
            )
        (run_dir / "run_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return run_dir


__all__ = ["AutomaticSolver", "AutomaticSolverConfig"]
