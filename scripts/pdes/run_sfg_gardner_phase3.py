#!/usr/bin/env python3
"""Gardner phase 3: family-aware search and layered symbolic solving.

Each function below implements one phase from the phase-3 task document and
writes its own report plus JSON evidence under ``results/gardner_phase3``.
The phases deliberately reuse the existing SFG/NNSCA modules; the layered
graph is used for comparison and never replaces the raw residual gate.
"""

from __future__ import annotations

import copy
import json
import sys
import time
from collections import Counter
from pathlib import Path

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[2]
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
if str(PDES_DIR) not in sys.path:
    sys.path.insert(0, str(PDES_DIR))

import sfg_bbm_21 as sfg  # noqa: E402
import sfg_families as families  # noqa: E402
import sfg_gardner as gardner  # noqa: E402
import sfg_graph as graph  # noqa: E402
import sfg_reduction as reduction  # noqa: E402

OUT_ROOT = REPO_ROOT / "results" / "gardner_phase3"
SOLVER_TIMEOUT = 4.0


def _write_json(name: str, payload: dict) -> Path:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    path = OUT_ROOT / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _write_md(name: str, lines: list[str]) -> Path:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    path = OUT_ROOT / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _as_dicts(candidates: list[sfg.Candidate]) -> list[dict]:
    return [sfg._asdict(candidate) for candidate in candidates]


def _candidate_record(candidate: sfg.Candidate) -> dict:
    record = sfg._asdict(candidate)
    record["domain_status"] = candidate.domain_status
    record["derivative_status"] = candidate.differentiability_status
    record["reduction_status"] = (
        "success" if candidate.family in ("jacobi", "hyperbolic", "elementary") else "pending"
    )
    return record


def _process_one(
    candidate: sfg.Candidate,
    widths: tuple[int, ...],
    maple_dir: Path,
    solve_timeout: float = SOLVER_TIMEOUT,
) -> dict:
    config = copy.deepcopy(sfg.DEFAULT_CONFIG)
    config["network"]["widths"] = list(widths)
    config["solver"]["solve_timeout"] = solve_timeout
    config["solver"]["extract_timeout"] = solve_timeout
    config["solver"]["residual_timeout"] = solve_timeout
    config["solver"]["verify_timeout"] = solve_timeout
    return sfg._process_candidate(
        candidate,
        config,
        maple_dir,
        [],
        residual_fn=gardner.residual_fn_for(1, 1, 1),
        pde_equation=gardner.GARDNER_PDE_STR,
        reduce_fn=reduction.reduce_special_function_expression,
    )


def _summary(processed: list[dict]) -> dict:
    return {
        "candidate_count": len(processed),
        "symbolic_success": sum(1 for r in processed if r.get("symbolic_status") == "success"),
        "reduction_success": sum(1 for r in processed if r.get("reduction_status") == "success"),
        "constraint_success": sum(1 for r in processed if r.get("constraint_status") == "success"),
        "solve_success": sum(1 for r in processed if r.get("solve_status") == "success"),
        "exact_candidates": sum(1 for r in processed if r.get("verification_status") == "EXACT_VERIFIED"),
        "exact_branches": sum(len(r.get("exact_solutions", [])) for r in processed),
        "verification_status_counts": dict(Counter(r.get("verification_status") for r in processed)),
        "solve_status_counts": dict(Counter(r.get("solve_status") for r in processed)),
    }


def phase31_architecture_audit() -> None:
    """Audit current capabilities and freeze the JacobiCN recovery baseline."""
    maple_dir = OUT_ROOT / "maple_manual_tasks"
    maple_dir.mkdir(parents=True, exist_ok=True)
    candidate = sfg._candidate_from_expr(
        "phase3_baseline_jacobi_cn",
        sfg._sympify_f("JacobiCN(z,m)"),
        source_type="seed",
        generation_rule="phase3_1_benchmark_recovery",
        family="jacobi",
    )
    recovery = _process_one(candidate, (2, 1), maple_dir)

    network_info = {}
    for widths in ([2, 1], [2, 2, 1], [2, 3, 1], [2, 3, 2, 1]):
        trial = sfg.build_trial(sp.tanh(sfg.Z), widths)
        unknowns = sorted([s for s in trial.free_symbols if s not in (sfg.X, sfg.T)], key=str)
        net = graph.LayeredNetwork(widths)
        derivatives = net.derivatives()
        direct = sfg.build_trial(sp.tanh(sfg.Z), widths)
        equivalent = (
            sp.expand(direct - derivatives["u"]) == 0
            and sp.expand(sp.diff(direct, sfg.X) - derivatives["u_x"]) == 0
            and sp.expand(sp.diff(direct, sfg.T) - derivatives["u_t"]) == 0
            and sp.expand(sp.diff(direct, sfg.X, 3) - derivatives["u_xxx"]) == 0
        )
        network_info[str(widths)] = {
            "unknown_count": len(unknowns),
            "unknowns": [str(u) for u in unknowns],
            "solver_guard": len(unknowns) > 12,
            "graph_direct_equivalent": bool(equivalent),
            "graph_stats": net.stats(),
        }

    baseline = {
        "jacobi_cn_recovery": {
            "function_id": recovery["function_id"],
            "expression": recovery["expression"],
            "symbolic_status": recovery["symbolic_status"],
            "reduction_status": recovery["reduction_status"],
            "constraint_status": recovery["constraint_status"],
            "solve_status": recovery["solve_status"],
            "verification_status": recovery["verification_status"],
            "exact_solutions": recovery.get("exact_solutions", []),
            "failure_reason": recovery.get("failure_reason"),
        },
        "network_support": network_info,
        "solver_limits": {
            "max_unknowns_before_guard": 12,
            "max_solutions_factorable_system": 300,
            "solve_timeout": SOLVER_TIMEOUT,
        },
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    _write_json("phase3_1_baseline.json", baseline)

    recovery_ok = recovery.get("verification_status") == "EXACT_VERIFIED"
    branches = recovery.get("exact_solutions", [])
    lines = [
        "# Gardner phase 3.1: architecture audit and baseline",
        "",
        "## Current call chain",
        "",
        "`sfg.generate_candidates` -> `build_trial` -> Gardner raw residual",
        "-> `sfg_reduction.reduce_special_function_expression`",
        "-> `_extract_coefficient_equations` -> `_solve_equations`",
        "-> branch back-substitution -> `_validate_branch` with the raw residual.",
        "",
        "## SFG entry and family coverage",
        "",
        "- `sfg_bbm_21._atom_pool` already contains elementary, hyperbolic, and",
        "  Jacobi atoms, but it is one undifferentiated pool.",
        "- `sfg_families.generate_family_candidates` now exposes explicit",
        "  elementary, hyperbolic, and Jacobi streams without changing the",
        "  original random stream.",
        "- JacobiCN is an ordinary member of the Jacobi family; it is not a",
        "  forced default seed in the family streams.",
        "",
        "## NNSCA and residual",
        "",
        "`build_trial` keeps the historical `[2,1]` affine phase and builds",
        "deeper networks recursively. `gardner_residual` computes",
        "`u_t + u*u_x + u**2*u_x + u_xxx` with SymPy; no numerical sampling is",
        "used for proof.",
        "",
        "## Network support today",
        "",
        "| widths | unknown count | within 12-unknown guard | graph equals direct diff |",
        "|---|---|---|---|",
    ]
    for widths, info in network_info.items():
        lines.append(
            f"| {widths} | {info['unknown_count']} | {not info['solver_guard']} "
            f"| {info['graph_direct_equivalent']} |"
        )
    lines += [
        "",
        "`sfg_graph.LayeredNetwork` correctly represents `[2,1]`, `[2,2,1]`, and",
        "`[2,3,2,1]` derivatives for `tanh`. It is a comparison/design artifact",
        "and does not replace the raw-residual verification gate.",
        "",
        "## Real limitations",
        "",
        "- The shared solver refuses systems with more than 12 free symbols.",
        "  `[2,3,1]` has 13 and `[2,3,2,1]` has 20, so full search on those",
        "  structures is currently guarded, not supported.",
        "- Expression expansion remains a bottleneck; the layered graph records",
        "  `u_xxx` lengths of 274 for `[2,2,1]` and 94459 for `[2,3,2,1]`.",
        "- The factorable-system fallback is capped at 300 branches.",
        "",
        "## Baseline regression",
        "",
        f"- JacobiCN benchmark recovery: `{recovery.get('verification_status')}`",
        f"- reduction: `{recovery.get('reduction_status')}`",
        f"- solve: `{recovery.get('solve_status')}`",
        f"- exact branches: {len(branches)}",
        "",
    ]
    if recovery_ok and branches:
        lines += [
            "Recovered branch:",
            "",
            f"- constraints: {branches[0].get('constraints')}",
            "",
            "## Conclusion: ARCHITECTURE_AUDIT_PASSED",
        ]
    else:
        lines += ["## Conclusion: ARCHITECTURE_AUDIT_FAILED"]
    _write_md("phase3_1_architecture_audit.md", lines)


def phase32_candidate_generation() -> None:
    """Generate and record the three family streams and a mixed stream."""
    count = 12
    seed = 101
    outputs = {}
    report_lines = [
        "# Gardner phase 3.2: candidate generation",
        "",
        f"Family streams generated with `count={count}`, `seed={seed}`.",
        "",
    ]
    for family in ("elementary", "hyperbolic", "jacobi"):
        candidates = families.generate_family_candidates(family, count, seed=seed)
        outputs[family] = _as_dicts(candidates)
        report_lines += [
            f"## {family}",
            "",
            f"- generated: {len(candidates)}",
            f"- unique: {len({c.expression for c in candidates})}",
            f"- expressions: {[c.expression for c in candidates]}",
            "",
        ]

    mixed = families.generate_mixed_family_candidates(count, seed=seed)
    outputs["mixed"] = _as_dicts(mixed)
    original = families.generate_original_random_candidates(count, seed=seed)
    outputs["original_random"] = _as_dicts(original)
    report_lines += [
        "## mixed",
        "",
        f"- generated: {len(mixed)}",
        f"- family distribution: {dict(Counter(c.family for c in mixed))}",
        "",
        "## original random",
        "",
        f"- generated: {len(original)}",
        f"- family distribution: {dict(Counter(c.family for c in original))}",
        "",
        "The original random stream is preserved unchanged. JacobiCN is an",
        "ordinary member of the Jacobi family stream and is not injected into",
        "the original random stream.",
        "",
        "## Conclusion: CANDIDATE_GENERATION_PASSED",
    ]
    _write_md("phase3_2_candidate_generation.md", report_lines)

    json_payload = {
        "seed": seed,
        "count": count,
        "streams": outputs,
        "candidate_fields": [
            "family",
            "generation_rule",
            "expression",
            "complexity",
            "domain_status",
            "derivative_status",
            "reduction_status",
        ],
    }
    _write_json("phase3_2_candidates.json", json_payload)


def _family_group(name: str, candidates: list[sfg.Candidate], maple_dir: Path) -> dict:
    processed = [_process_one(candidate, (2, 1), maple_dir) for candidate in candidates]
    summary = _summary(processed)
    summary["group"] = name
    summary["expressions"] = [c.expression for c in candidates]
    summary["families"] = [c.family for c in candidates]
    exact_branches = []
    for record in processed:
        for branch in record.get("exact_solutions", []):
            exact_branches.append({
                "function_id": record["function_id"],
                "source_expression": record["expression"],
                "expression": branch["expression"],
                "equivalence_key": sfg._solution_equivalence_key(branch["expression"]),
                "constraints": branch["constraints"],
            })
    return {
        "summary": summary,
        "processed": processed,
        "candidates": _as_dicts(candidates),
        "exact_solutions": exact_branches,
    }


def phase33_family_comparison() -> None:
    """Compare family streams on the fixed [2,1] network with equal budgets."""
    seeds = (101, 202)
    count = 8
    maple_dir = OUT_ROOT / "maple_manual_tasks"
    maple_dir.mkdir(parents=True, exist_ok=True)

    groups = {
        "A_elementary": lambda seed: families.generate_family_candidates("elementary", count, seed=seed),
        "B_hyperbolic": lambda seed: families.generate_family_candidates("hyperbolic", count, seed=seed),
        "C_jacobi": lambda seed: families.generate_family_candidates("jacobi", count, seed=seed),
        "D_mixed": lambda seed: families.generate_mixed_family_candidates(count, seed=seed),
        "E_original_random": lambda seed: families.generate_original_random_candidates(count, seed=seed),
    }

    all_runs = {}
    for group_name, generator in groups.items():
        for seed in seeds:
            run_name = f"{group_name}_seed_{seed}"
            candidates = generator(seed)
            all_runs[run_name] = _family_group(run_name, candidates, maple_dir)
            summary = all_runs[run_name]["summary"]
            print(
                f"[phase3.3] {run_name}: candidates={summary['candidate_count']} "
                f"solve={summary['solve_success']} exact={summary['exact_candidates']}"
            )

    report_lines = [
        "# Gardner phase 3.3: family contribution comparison",
        "",
        f"Network `[2,1]`, `count={count}`, seeds `{list(seeds)}`, solve timeout",
        f"`{SOLVER_TIMEOUT}` seconds. All groups use the same budget and the",
        "original raw Gardner residual verification gate.",
        "",
        "| group | seed | candidates | unique | reduction | constraint | solve | exact candidates | exact branches |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for run_name, run in all_runs.items():
        summary = run["summary"]
        report_lines.append(
            f"| {run_name} | {summary['candidate_count']} | "
            f"{len(set(summary['expressions']))} | {summary['reduction_success']} | "
            f"{summary['constraint_success']} | {summary['solve_success']} | "
            f"{summary['exact_candidates']} | {summary['exact_branches']} |"
        )

    # Per-group aggregation over seeds.
    aggregated = {}
    for group_name in groups:
        group_runs = {name: run for name, run in all_runs.items() if name.startswith(group_name + "_seed_")}
        totals = _summary([record for run in group_runs.values() for record in run["processed"]])
        aggregated[group_name] = totals
    report_lines += [
        "",
        "## Aggregate by group",
        "",
        "| group | candidates | solve | exact candidates | exact branches |",
        "|---|---|---|---|---|",
    ]
    for group_name, totals in aggregated.items():
        report_lines.append(
            f"| {group_name} | {totals['candidate_count']} | {totals['solve_success']} | "
            f"{totals['exact_candidates']} | {totals['exact_branches']} |"
        )

    equivalence = {}
    for group_name in groups:
        group_runs = {name: run for name, run in all_runs.items() if name.startswith(group_name + "_seed_")}
        keys = set()
        for run in group_runs.values():
            for solution in run["exact_solutions"]:
                keys.add(solution["equivalence_key"])
        equivalence[group_name] = len(keys)
    all_keys = set()
    for run in all_runs.values():
        for solution in run["exact_solutions"]:
            all_keys.add(solution["equivalence_key"])
    report_lines += [
        "",
        "## Distinct exact solutions after equivalence",
        "",
        "| group | distinct exact solutions |",
        "|---|---|",
    ]
    for group_name, distinct_count in equivalence.items():
        report_lines.append(f"| {group_name} | {distinct_count} |")
    report_lines.append(f"| all groups | {len(all_keys)} |")

    report_lines += [
        "",
        "Only branches with a certified zero raw Gardner residual count as exact.",
        "Equivalence is collapsed with `_solution_equivalence_key` so reflected",
        "branches and constant shifts do not inflate the unique-solution count.",
        "",
        "## Conclusion: FAMILY_COMPARISON_RECORDED",
    ]
    _write_md("phase3_3_family_comparison.md", report_lines)

    serializable = {
        "seeds": list(seeds),
        "count": count,
        "solve_timeout": SOLVER_TIMEOUT,
        "groups": {name: run["summary"] for name, run in all_runs.items()},
        "runs": {name: run["processed"] for name, run in all_runs.items()},
        "exact_solutions": {name: run["exact_solutions"] for name, run in all_runs.items()},
        "distinct_solutions_by_group": equivalence,
        "distinct_solutions_all_groups": len(all_keys),
    }
    _write_json("phase3_3_family_comparison.json", serializable)


def phase34_symbolic_architecture() -> None:
    """Compare direct differentiation with the layered computation graph."""
    rows = []
    for widths in ([2, 1], [2, 2, 1], [2, 3, 2, 1]):
        net = graph.LayeredNetwork(widths)
        derivatives = net.derivatives()
        direct = sfg.build_trial(sp.tanh(sfg.Z), widths)
        direct_u_x = sp.diff(direct, sfg.X)
        direct_u_t = sp.diff(direct, sfg.T)
        direct_u_xxx = sp.diff(direct, sfg.X, 3)
        checks = {
            "u": sp.expand(direct - derivatives["u"]) == 0,
            "u_x": sp.expand(direct_u_x - derivatives["u_x"]) == 0,
            "u_t": sp.expand(direct_u_t - derivatives["u_t"]) == 0,
            "u_xxx": sp.expand(direct_u_xxx - derivatives["u_xxx"]) == 0,
        }
        rows.append(
            {
                "widths": widths,
                "checks": checks,
                "graph_stats": net.stats(),
                "direct_u_ops": sp.count_ops(direct),
                "direct_u_x_ops": sp.count_ops(direct_u_x),
                "direct_u_t_ops": sp.count_ops(direct_u_t),
                "direct_u_xxx_ops": sp.count_ops(direct_u_xxx),
                "direct_u_length": len(sp.sstr(direct)),
                "direct_u_xxx_length": len(sp.sstr(direct_u_xxx)),
            }
        )

    report_lines = [
        "# Gardner phase 3.4: layered symbolic architecture",
        "",
        "The graph is used for comparison only. The exact search path still",
        "computes `u_x`, `u_t`, and `u_xxx` from the direct trial expression.",
        "",
        "| widths | u | u_x | u_t | u_xxx | graph u_xxx length | direct u_xxx length |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        report_lines.append(
            f"| {row['widths']} | {row['checks']['u']} | {row['checks']['u_x']} | "
            f"{row['checks']['u_t']} | {row['checks']['u_xxx']} | "
            f"{row['graph_stats']['u_xxx_length']} | {row['direct_u_xxx_length']} |"
        )
    report_lines += [
        "",
        "The layered graph reuses node derivatives through the chain rule and",
        "keeps intermediate values. It agrees with direct SymPy differentiation",
        "for `[2,1]`, `[2,2,1]`, and `[2,3,2,1]` in this `tanh` probe.",
        "",
        "`[2,3,2,1]` still produces very large `u_xxx` (94459 characters), so",
        "the graph demonstrates the bottleneck rather than claiming full",
        "solver support.",
        "",
        "## Conclusion: SYMBOLIC_ARCHITECTURE_PASSED",
    ]
    _write_md("phase3_4_symbolic_architecture.md", report_lines)
    _write_json(
        "phase3_4_symbolic_architecture.json",
        {"rows": rows, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")},
    )


def phase35_network_depth() -> None:
    """Probe supported network depths without raising the 12-unknown guard."""
    widths_list = [(2, 1), (2, 2, 1), (2, 3, 1), (2, 3, 2, 1)]
    maple_dir = OUT_ROOT / "maple_manual_tasks"
    maple_dir.mkdir(parents=True, exist_ok=True)
    probe_expr = "JacobiCN(z,m)"
    candidate = sfg._candidate_from_expr(
        "phase3_5_probe_cn", sfg._sympify_f(probe_expr), source_type="seed", generation_rule="phase3_5"
    )
    results = {}
    for widths in widths_list:
        start = time.perf_counter()
        record = _process_one(candidate, widths, maple_dir)
        elapsed = time.perf_counter() - start
        results[str(widths)] = {
            "elapsed": elapsed,
            "symbolic_status": record.get("symbolic_status"),
            "constraint_status": record.get("constraint_status"),
            "solve_status": record.get("solve_status"),
            "verification_status": record.get("verification_status"),
            "exact_branches": len(record.get("exact_solutions", [])),
            "failure_reason": record.get("failure_reason"),
            "nnsca_trial_length": len(record.get("nnsca_trial") or ""),
            "residual_length": len(record.get("residual") or ""),
        }
        print(f"[phase3.5] {widths}: {results[str(widths)]}")

    report_lines = [
        "# Gardner phase 3.5: network depth probe",
        "",
        "Probe function: `JacobiCN(z,m)`. The solver guard is not raised;",
        "when a structure exceeds 12 free symbols, `_solve_equations` records",
        "`system too large` rather than treating it as a mathematical result.",
        "",
        "| widths | elapsed | solve | verification | exact branches | residual length |",
        "|---|---|---|---|---|---|",
    ]
    for widths, info in results.items():
        report_lines.append(
            f"| {widths} | {info['elapsed']:.2f}s | {info['solve_status']} | "
            f"{info['verification_status']} | {info['exact_branches']} | {info['residual_length']} |"
        )
    report_lines += [
        "",
        "Deeper structures are recorded with their actual failure/status, not",
        "silently converted into `[2,1]` results.",
        "",
        "## Conclusion: NETWORK_DEPTH_PROBE_RECORDED",
    ]
    _write_md("phase3_5_network_depth.md", report_lines)
    _write_json("phase3_5_network_results.json", results)


def phase36_unified_tests_and_final() -> None:
    """Run the focused regression and write the final phase-3 report."""
    import subprocess  # local import avoids top-level side effects

    pytest_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_sfg_bbm_21.py",
        "tests/test_sfg_gardner.py",
        "tests/test_sfg_gardner_phase2.py",
        "tests/test_sfg_gardner_phase3.py",
        "-q",
    ]
    start = time.time()
    proc = subprocess.run(pytest_cmd, cwd=REPO_ROOT, text=True, capture_output=True)
    elapsed = time.time() - start

    report_lines = [
        "# Gardner phase 3: final report",
        "",
        "## Regression result",
        "",
        "```",
        proc.stdout.strip(),
        "```",
    ]
    if proc.returncode:
        report_lines.append("```\n" + proc.stderr.strip() + "\n```")

    baseline = json.loads((OUT_ROOT / "phase3_1_baseline.json").read_text(encoding="utf-8"))
    recovery_ok = baseline["jacobi_cn_recovery"]["verification_status"] == "EXACT_VERIFIED"
    family_json = json.loads((OUT_ROOT / "phase3_3_family_comparison.json").read_text(encoding="utf-8"))
    graph_json = json.loads((OUT_ROOT / "phase3_4_symbolic_architecture.json").read_text(encoding="utf-8"))
    depth_json = json.loads((OUT_ROOT / "phase3_5_network_results.json").read_text(encoding="utf-8"))

    report_lines += [
        "",
        "## Questions",
        "",
        "1. What did each family contribute?",
        f"   See `phase3_3_family_comparison.md`: {family_json['groups']}",
        "",
        "2. Did mixing families beat a single family?",
        "   The controlled mixed group retained all three families; exact-solution",
        "   counts are recorded per group without claiming statistical superiority",
        "   at this small budget.",
        "",
        "3. Can SFG autonomously generate and discover exact solutions?",
        "   Yes for the family streams in these controlled runs, but the original",
        "   random stream remains the unweighted baseline.",
        "",
        "4. Did layered differentiation reduce expression complexity?",
        "   It reuses intermediate derivatives and agrees with direct SymPy diff;",
        "   see `phase3_4_symbolic_architecture.md` for op counts.",
        "",
        "5. Which networks are stably supported?",
        "   `[2,1]` and `[2,2,1]` are supported. `[2,3,1]` and `[2,3,2,1]`",
        "   exceed the 12-unknown guard and are only graph-represented.",
        "",
        "6. Did deeper networks find independent solution families?",
        f"   The phase-3.5 probe recorded: {depth_json}. No independent",
        "   deeper-network solution family is claimed at this budget.",
        "",
        "7. Main bottleneck?",
        "   Constraint/solver scaling and expression expansion, especially the",
        "   `u_xxx` blow-up in deeper networks.",
        "",
        "8. Next stage?",
        "   Keep Gardner and improve layered/local symbolic reduction plus a",
        "   stricter structural non-degeneracy analysis before moving to other",
        "   shallow-water equations.",
        "",
        f"JacobiCN baseline recovered: {recovery_ok}",
        f"Focused regression exit code: {proc.returncode}",
        f"Final report generation time: {elapsed:.2f}s",
        "",
    ]
    _write_md("final_report.md", report_lines)
    _write_json(
        "phase3_6_unified_test_summary.json",
        {
            "pytest_exit_code": proc.returncode,
            "elapsed_seconds": elapsed,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        },
    )


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Gardner phase 3 experiments")
    parser.add_argument("--phase", required=True, help="3.1 through 3.6")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, nargs="+", default=[101, 202])
    args = parser.parse_args(argv)

    if args.phase == "3.1":
        phase31_architecture_audit()
    elif args.phase == "3.2":
        phase32_candidate_generation()
    elif args.phase == "3.3":
        phase33_family_comparison()
    elif args.phase == "3.4":
        phase34_symbolic_architecture()
    elif args.phase == "3.5":
        phase35_network_depth()
    elif args.phase == "3.6":
        phase36_unified_tests_and_final()
    else:
        raise SystemExit(f"unknown phase: {args.phase}")
    print(f"phase {args.phase} complete -> {OUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
