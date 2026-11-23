#!/usr/bin/env python3
"""Write a stage-by-stage solver diagnosis from processed_candidates.json."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def _summarise(data: list[dict]) -> dict:
    counters = {
        "symbolic": Counter(r.get("symbolic_status") for r in data),
        "constraint": Counter(r.get("constraint_status") for r in data),
        "extraction": Counter(r.get("extraction_status") for r in data),
        "solve": Counter(r.get("solve_status") for r in data),
        "nontrivial": Counter(r.get("nontrivial_status") for r in data),
        "substitution": Counter(r.get("substitution_status") for r in data),
        "identity": Counter(r.get("identity_verification_status") for r in data),
        "verification": Counter(r.get("verification_status") for r in data),
    }

    solve_success = [r for r in data if r.get("solve_status") == "success"]
    exact_from_solve = [
        r for r in solve_success if r.get("verification_status") == "EXACT_VERIFIED"
    ]
    branch_statuses = Counter()
    for record in data:
        for attempt in record.get("branch_attempts", []):
            branch_statuses[attempt.get("nontrivial_status")] += 1

    failure_patterns = Counter()
    for record in data:
        if record.get("verification_status") in ("EXACT_VERIFIED", "NO_SOLUTION"):
            continue
        reason = record.get("failure_reason") or record.get("verification_status")
        if "residual computation" in reason:
            key = "residual_timeout_or_error"
        elif "extraction" in reason:
            key = "extraction_timeout_or_error"
        elif "solver produced branches" in reason:
            key = "solver_branches_not_exact"
        elif "coefficient system has no" in reason:
            key = "no_nontrivial_solution"
        elif "solve" in reason:
            key = "solve_timeout_or_error"
        elif "system too large" in reason:
            key = "system_too_large"
        elif "no nontrivial" in reason:
            key = "no_nontrivial_solution"
        else:
            key = reason.split(":")[0]
        failure_patterns[key] += 1

    return {
        "total": len(data),
        "counters": counters,
        "solve_success": len(solve_success),
        "exact_from_solve": len(exact_from_solve),
        "branch_statuses": branch_statuses,
        "failure_patterns": failure_patterns,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("processed_json", nargs="?", default="results/sfg_bbm/processed_candidates.json")
    args = parser.parse_args(argv)

    processed_path = Path(args.processed_json)
    data = json.loads(processed_path.read_text(encoding="utf-8"))
    summary = _summarise(data)

    lines = [
        "# SFG solver diagnosis",
        "",
        f"- processed candidates: {summary['total']}",
        "",
        "## Stage counts",
        "",
        "| stage | counts |",
        "|---|---|",
    ]
    for name, key in [
        ("symbolic", "symbolic"),
        ("constraint", "constraint"),
        ("extraction", "extraction"),
        ("solve", "solve"),
        ("nontrivial", "nontrivial"),
        ("substitution", "substitution"),
        ("identity", "identity"),
        ("verification", "verification"),
    ]:
        counts = dict(summary["counters"][key])
        lines.append(f"| {name} | {counts} |")
    lines += [
        "",
        f"- solve success: {summary['solve_success']}",
        f"- solve success that are EXACT_VERIFIED: {summary['exact_from_solve']}",
        "",
        "## Branch nontrivial statuses",
        "",
    ]
    for status, count in summary["branch_statuses"].most_common():
        lines.append(f"- {status}: {count}")
    lines += ["", "## Failure patterns", ""]
    for pattern, count in summary["failure_patterns"].most_common():
        lines.append(f"- {pattern}: {count}")

    output_path = processed_path.with_name("solver_diagnosis.md")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
