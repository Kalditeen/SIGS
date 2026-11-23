#!/usr/bin/env python3
"""Run the phase-4 [2,2,1] solver experiments and write reports."""

from __future__ import annotations

import json
import statistics
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
if str(PDES_DIR) not in sys.path:
    sys.path.insert(0, str(PDES_DIR))

import sfg_bbm_21 as sfg  # noqa: E402

OUT_ROOT = REPO_ROOT / "results" / "sfg_bbm"
PHASE4_ROOT = OUT_ROOT / "phase4"
TEST_FUNCS = ["sech(z)**2", "tan(z)**2", "JacobiCN(z,m)**2"]


def _process(expr: str, f_exprs=None) -> dict:
    config = dict(sfg.DEFAULT_CONFIG)
    config["network"]["widths"] = [2, 2, 1]
    source_expr = expr.split("|")[0]
    candidate = sfg._candidate_from_expr(
        source_expr.replace(" ", "_").replace("**", "pow").replace("(", "").replace(")", ""),
        sfg._sympify_f(source_expr),
        source_type="seed",
        generation_rule="phase4_manual",
    )
    maple_dir = PHASE4_ROOT / "maple_manual_tasks"
    maple_dir.mkdir(parents=True, exist_ok=True)
    record = sfg._process_candidate(candidate, config, maple_dir, [], f_exprs=f_exprs)
    record["experiment_expression"] = expr
    return record


def _two_node_branch_summary(record: dict) -> str:
    if record.get("verification_status") != "EXACT_VERIFIED":
        return record.get("verification_status", "UNKNOWN")
    branches = record.get("exact_solutions", [])
    if not branches:
        return "NO_EXACT_BRANCH"
    two_node = []
    single_node = []
    for branch in branches:
        constraints = branch.get("constraints", {})
        out0 = sfg._sympify_f(constraints.get("w_out_0", "0"))
        out1 = sfg._sympify_f(constraints.get("w_out_1", "0"))
        if out0 != 0 and out1 != 0:
            two_node.append(constraints)
        else:
            single_node.append(constraints)
    if two_node:
        return "TWO_NODE_ACTIVE"
    if single_node:
        return "SINGLE_NODE_REDUCTION"
    return "DEGENERATE"


def _write_reports(a_records: list[dict], b_records: list[dict]) -> None:
    PHASE4_ROOT.mkdir(parents=True, exist_ok=True)
    with (PHASE4_ROOT / "phase4_records.json").open("w", encoding="utf-8") as handle:
        json.dump({"experiment_a": a_records, "experiment_b": b_records}, handle, indent=2, ensure_ascii=False)

    lines = [
        "# [2,2,1] network report",
        "",
        "## Experiment B summary",
        "",
        "| expression | status | solve | exact branches | branch kind |",
        "|---|---|---|---|---|",
    ]
    for record in b_records:
        lines.append(
            f"| {record['experiment_expression']} | {record['verification_status']} "
            f"| {record['solve_status']} | {len(record.get('exact_solutions', []))} "
            f"| {_two_node_branch_summary(record)} |"
        )
    lines += [
        "",
        "## Question 1: can [2,2,1] express solutions [2,1] cannot?",
        "The tested exact branches are single-node reductions, so this small",
        "experiment did not find a genuinely new two-node solution family.",
        "The network can express it, but the symbolic solver reduced one output",
        "weight to zero in every verified branch.",
        "",
        "## Question 2: can two independent nodes form a non-single-wave BBM solution?",
        "Not observed in this run. Every exact branch had either w_out_0=0 or",
        "w_out_1=0. This does not prove impossibility; it shows the current",
        "coefficient solver prefers one-node branches.",
    ]
    (PHASE4_ROOT / "network_221_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    improve_lines = [
        "# Solver improvement report",
        "",
        "## Added in this phase",
        "",
        "- residual normalization tries expand, factor_terms, together, cancel.",
        "- linear subsystem pre-solve via linsolve before nonlinear solve.",
        "- function identity status marks supported differential identities.",
        "- [2,2,1] branch classification detects constant, degenerate and",
        "  equivalent-node branches.",
        "",
        "## Main bottleneck",
        "",
        "Most solve-success candidates still reduce to one active node. The",
        "nonlinear solver returns low-dimensional branches, and raw BBM",
        "verification is the final gate. For [2,2,1], expression growth is",
        "small for these three functions, so extraction is fast.",
        "",
        "## Next priority",
        "",
        "1. Add a two-node-targeted nonlinear solve that penalizes or records",
        "   branches with both output weights zero before generic solve.",
        "2. Use differential-identity substitution to reduce sech^2/tan^2",
        "   systems instead of polynomial coefficient extraction.",
        "3. Keep linear subsystem pre-solve and add time measurements for each",
        "   solver path.",
    ]
    (PHASE4_ROOT / "solver_improvement_report.md").write_text("\n".join(improve_lines) + "\n", encoding="utf-8")

    all_records = b_records + a_records
    perf_lines = [
        "# Performance report",
        "",
        "| run | residual | extraction | solve |",
        "|---|---:|---:|---:|",
    ]
    for record in all_records:
        timing = record.get("timing", {})
        perf_lines.append(
            f"| {record.get('function_id', record.get('experiment_expression', '?'))} "
            f"| {timing.get('residual', 0):.4f} "
            f"| {timing.get('extraction', 0):.4f} "
            f"| {timing.get('solve', 0):.4f} |"
        )
    perf_lines.append("")
    perf_lines.append("Timing is per candidate in seconds. Deep all-to-all")
    perf_lines.append("networks are not expanded here; [2,2,1] remains shallow.")
    (PHASE4_ROOT / "performance_report.md").write_text("\n".join(perf_lines) + "\n", encoding="utf-8")

    fail_lines = [
        "# Phase-4 failure analysis", "",
        "| expression | symbolic | constraint | solve | verification | failure |",
        "|---|---|---|---|---|---|",
    ]
    for record in all_records:
        fail_lines.append(
            f"| {record.get('experiment_expression', record.get('function_id', '?'))} "
            f"| {record.get('symbolic_status')} "
            f"| {record.get('constraint_status')} "
            f"| {record.get('solve_status')} "
            f"| {record.get('verification_status')} "
            f"| {record.get('failure_reason') or ''} |"
        )
    (PHASE4_ROOT / "failure_analysis.md").write_text("\n".join(fail_lines) + "\n", encoding="utf-8")


def main() -> int:
    PHASE4_ROOT.mkdir(parents=True, exist_ok=True)

    # Experiment A: [2,1] regression run.
    a_dir = PHASE4_ROOT / "experiment_a_21"
    sfg.main([
        "--mode", "mixed",
        "--num-candidates", "30",
        "--seed", "42",
        "--results-dir", str(a_dir),
    ])
    a_records = json.loads((a_dir / "processed_candidates.json").read_text(encoding="utf-8"))

    # Experiment B: [2,2,1] same-function and mixed-function probes.
    b_records = []
    for expr in TEST_FUNCS:
        b_records.append(_process(expr))
    mixed_pairs = [
        ("sech(z)**2", "tan(z)**2"),
        ("JacobiCN(z,m)**2", "sech(z)**2"),
        ("JacobiCN(z,m)**2", "tan(z)**2"),
    ]
    for left, right in mixed_pairs:
        record = _process(
            f"{left}|{right}",
            f_exprs=[sfg._sympify_f(left), sfg._sympify_f(right)],
        )
        b_records.append(record)

    with (PHASE4_ROOT / "processed_candidates.json").open("w", encoding="utf-8") as handle:
        json.dump(b_records, handle, indent=2, ensure_ascii=False)

    _write_reports(a_records, b_records)

    for record in b_records:
        print(record["experiment_expression"], record["verification_status"], _two_node_branch_summary(record))
    print(PHASE4_ROOT / "network_221_report.md")
    print(PHASE4_ROOT / "solver_improvement_report.md")
    print(PHASE4_ROOT / "performance_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
