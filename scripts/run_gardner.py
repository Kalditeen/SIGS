#!/usr/bin/env python3
"""End-to-end Gardner run for the refactored SFG-NNSCA architecture."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from nnsca.adapter import Stage2Adapter  # noqa: E402
from nnsca.compiler import AnsatzCompiler  # noqa: E402
from pdes.gardner import gardner_residual  # noqa: E402
from sfg.search import SearchConfig, SFGNetworkSearch  # noqa: E402

DEFAULT_RESULTS_DIR = REPO_ROOT / "results" / "refactor" / "gardner"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Refactored SFG-NNSCA Gardner search")
    parser.add_argument("--num-structures", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-hidden-layers", type=int, default=1)
    parser.add_argument("--max-width-per-layer", type=int, default=2)
    parser.add_argument("--max-total-hidden-nodes", type=int, default=4)
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    args = parser.parse_args(argv)

    results_dir = Path(args.results_dir).expanduser()
    results_dir.mkdir(parents=True, exist_ok=True)

    config = SearchConfig(
        num_candidates=args.num_structures,
        seed=args.seed,
        max_hidden_layers=args.max_hidden_layers,
        max_width_per_layer=args.max_width_per_layer,
        max_total_hidden_nodes=args.max_total_hidden_nodes,
        include_single_node_baseline=True,
    )
    search = SFGNetworkSearch(config)
    candidates = search.generate()
    compiler = AnsatzCompiler()
    stage2 = Stage2Adapter()

    solve_config = {
        "solver": {
            "extract_timeout": 8.0,
            "solve_timeout": 8.0,
            "residual_timeout": 8.0,
            "verify_timeout": 8.0,
        }
    }

    records = []
    started = time.time()
    for candidate in candidates:
        compiled = compiler.compile(candidate)
        record = stage2.process(
            compiled.expression,
            gardner_residual,
            solve_config,
            pde_equation="u_t + u*u_x + u**2*u_x + u_xxx = 0",
        )
        record["candidate_id"] = candidate.candidate_id
        record["structure"] = candidate.structure.to_dict()
        record["activation_functions"] = compiled.candidate.activation_functions
        records.append(record)

    summary = {
        "generated_structures": len(candidates),
        "unique_structures": len({candidate.structure.signature() for candidate in candidates}),
        "compile_success": len(records),
        "constraint_success": sum(1 for r in records if r.get("constraint_status") == "success"),
        "solve_success": sum(1 for r in records if r.get("solve_status") == "success"),
        "exact_candidates": sum(
            1 for r in records if r.get("verification_status") == "EXACT_VERIFIED"
        ),
        "exact_branches": sum(len(r.get("exact_solutions", [])) for r in records),
        "elapsed_seconds": round(time.time() - started, 3),
        "seed": args.seed,
    }

    run_config = {
        "search": config.__dict__,
        "solver": solve_config,
        "python_version": sys.version.split()[0],
        "sympy_version": __import__("sympy").__version__,
        "pde": "Gardner u_t + u*u_x + u**2*u_x + u_xxx = 0",
    }

    (results_dir / "run_config.json").write_text(
        json.dumps(run_config, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (results_dir / "candidates.json").write_text(
        json.dumps(
            [candidate.to_dict() for candidate in candidates],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (results_dir / "processed.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (results_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    exact = [
        {
            "candidate_id": record["candidate_id"],
            "solutions": record["exact_solutions"],
        }
        for record in records
        if record.get("exact_solutions")
    ]
    (results_dir / "exact_solutions.json").write_text(
        json.dumps(exact, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    lines = [
        "# Refactored SFG-NNSCA Gardner end-to-end run",
        "",
        f"- generated structures: {summary['generated_structures']}",
        f"- unique structures: {summary['unique_structures']}",
        f"- compile success: {summary['compile_success']}",
        f"- constraint extraction success: {summary['constraint_success']}",
        f"- solve success: {summary['solve_success']}",
        f"- exact candidates: {summary['exact_candidates']}",
        f"- exact branches: {summary['exact_branches']}",
        f"- elapsed seconds: {summary['elapsed_seconds']}",
        "",
        "Every reported exact branch was back-substituted into the raw Gardner",
        "residual and certified symbolically zero.  Known benchmark parameters",
        "were not written into the search or solver.",
    ]
    (results_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
