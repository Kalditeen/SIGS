#!/usr/bin/env python3
"""Run the Phase 3-A IR-aware automatic solving experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nnsca.search.automatic_solver import AutomaticSolver, AutomaticSolverConfig
from sfg.architecture_utils import hidden_depth
from sfg.candidate_manager import CandidateManager

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = (
    REPO_ROOT / "results" / "phase2_architecture_generation" / "candidates.json"
)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "results" / "phase3_automatic_solving"


def _representative_candidates(manager: CandidateManager) -> tuple[list[str], list[str]]:
    unique = manager.unique_records()
    categories: dict[str, str | None] = {
        "jacobi_single_node": None,
        "jacobi_containing": None,
        "two_node": None,
        "two_node_heterogeneous": None,
        "two_layer": None,
    }
    for record in unique:
        ir = record.network_ir
        activations = sorted(ir.activation_functions().values())
        node_count = len(ir.nodes)
        depth = hidden_depth(ir)
        has_jacobi = any(name.startswith("Jacobi") for name in activations)
        if categories["jacobi_containing"] is None and has_jacobi:
            categories["jacobi_containing"] = record.candidate_id
        if categories["jacobi_single_node"] is None and node_count == 1 and has_jacobi:
            categories["jacobi_single_node"] = record.candidate_id
        if categories["two_node"] is None and node_count == 2:
            categories["two_node"] = record.candidate_id
        if (
            categories["two_node_heterogeneous"] is None
            and node_count == 2
            and len(set(activations)) >= 2
        ):
            categories["two_node_heterogeneous"] = record.candidate_id
        if categories["two_layer"] is None and depth >= 2:
            categories["two_layer"] = record.candidate_id

    selected: list[str] = []
    missing: list[str] = []
    for label, candidate_id in categories.items():
        if candidate_id is None:
            missing.append(label)
        else:
            selected.append(candidate_id)
    return sorted(set(selected)), missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 3-A automatic Gardner solving")
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--candidate-ids", default="")
    parser.add_argument("--num-candidates", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-expression-nodes", type=int, default=4000)
    parser.add_argument("--extract-timeout", type=float, default=6.0)
    parser.add_argument("--solve-timeout", type=float, default=8.0)
    parser.add_argument("--residual-timeout", type=float, default=6.0)
    parser.add_argument("--verify-timeout", type=float, default=8.0)
    args = parser.parse_args(argv)

    manager = CandidateManager.load(args.candidates)
    selected_ids = [
        item.strip()
        for item in args.candidate_ids.split(",")
        if item.strip()
    ]
    if selected_ids:
        selected = selected_ids
        missing_categories: list[str] = []
    else:
        selected, missing_categories = _representative_candidates(manager)
        if args.num_candidates is not None:
            selected = selected[: args.num_candidates]

    if not selected:
        selected = [record.candidate_id for record in manager.unique_records()[:1]]

    config = AutomaticSolverConfig(
        max_candidates=args.num_candidates,
        candidate_ids=tuple(selected),
        seed=args.seed,
        max_expression_nodes=args.max_expression_nodes,
        full_verification=True,
        extract_timeout=args.extract_timeout,
        solve_timeout=args.solve_timeout,
        residual_timeout=args.residual_timeout,
        verify_timeout=args.verify_timeout,
    )

    solver = AutomaticSolver()
    run_data = solver.run(manager, config)
    run_data["statistics"]["selected_candidate_ids"] = selected
    run_data["statistics"]["missing_categories"] = missing_categories
    run_dir = AutomaticSolver.save_run(run_data, config, args.output_dir)

    print(json.dumps(run_data["statistics"], indent=2, ensure_ascii=False))
    print(f"run_dir={run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
