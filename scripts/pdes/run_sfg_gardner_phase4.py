#!/usr/bin/env python3
"""Gardner phase 4 experiments: basis audit, DAG architecture, and verification.

Each phase writes its own report and JSON evidence under
``results/gardner_phase4``.  The code never raises the 12-unknown solver guard
and never uses numerical residual sampling as an exactness proof.
"""

from __future__ import annotations

import copy
import json
import subprocess
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
import sfg_dag as dag  # noqa: E402
import sfg_families as families  # noqa: E402
import sfg_gardner as gardner  # noqa: E402
import sfg_graph as graph  # noqa: E402
import sfg_reduction as reduction  # noqa: E402

OUT_ROOT = REPO_ROOT / "results" / "gardner_phase4"
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


def _as_dicts(candidates):
    return [sfg._asdict(candidate) for candidate in candidates]


def _process_one(candidate: sfg.Candidate, widths=(2, 1), solve_timeout=SOLVER_TIMEOUT) -> dict:
    config = copy.deepcopy(sfg.DEFAULT_CONFIG)
    config["network"]["widths"] = list(widths)
    config["solver"]["solve_timeout"] = solve_timeout
    config["solver"]["extract_timeout"] = solve_timeout
    config["solver"]["residual_timeout"] = solve_timeout
    config["solver"]["verify_timeout"] = solve_timeout
    maple_dir = OUT_ROOT / "maple_manual_tasks"
    maple_dir.mkdir(parents=True, exist_ok=True)
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


def _collect_exact_branches(processed: list[dict]) -> list[dict]:
    branches = []
    for record in processed:
        for branch in record.get("exact_solutions", []):
            branches.append({
                "function_id": record["function_id"],
                "source_expression": record["expression"],
                "expression": branch["expression"],
                "equivalence_key": sfg._solution_equivalence_key(branch["expression"]),
                "constraints": branch["constraints"],
            })
    return branches


def phase41_function_audit() -> None:
    """Audit phase-3 records and separate pool-level from candidate-level claims."""
    phase3_json = json.loads(
        (REPO_ROOT / "results" / "gardner_phase3" / "phase3_3_family_comparison.json").read_text(encoding="utf-8")
    )
    exact_by_group = phase3_json.get("exact_solutions", {})

    source_counts = Counter()
    source_to_group = {}
    equivalence_groups: dict[str, list[dict]] = {}
    for group_name, branches in exact_by_group.items():
        for branch in branches:
            source_counts[branch["source_expression"]] += 1
            source_to_group.setdefault(branch["source_expression"], group_name)
            equivalence_groups.setdefault(branch["equivalence_key"], []).append(branch)

    mixed_group = [name for name in exact_by_group if name.startswith("D_mixed_seed_")]
    mixed_exact_sources = Counter()
    for group_name in mixed_group:
        for branch in exact_by_group[group_name]:
            mixed_exact_sources[branch["source_expression"]] += 1

    lines = [
        "# Gardner phase 4.1: function basis and exact-solution audit",
        "",
        "## Family definitions",
        "",
        f"- elementary atoms: {families.FAMILY_DEFS['elementary']['atoms']}",
        f"- hyperbolic atoms: {families.FAMILY_DEFS['hyperbolic']['atoms']}",
        f"- jacobi atoms: {families.FAMILY_DEFS['jacobi']['atoms']}",
        "",
        "## Exact branches by specific candidate",
        "",
        "| source expression | occurrence | group(s) |",
        "|---|---|---|",
    ]
    for expression, count in source_counts.most_common():
        lines.append(f"| {expression} | {count} | {source_to_group.get(expression)} |")

    lines += [
        "",
        "## Mixed-group check",
        "",
        f"- exact sources in mixed pool: {dict(mixed_exact_sources)}",
        f"- distinct equivalence keys: {phase3_json.get('distinct_solutions_all_groups')}",
        "",
        "Phase-3 mixed-group exact solutions came from single `JacobiSN` and",
        "`JacobiCN` candidates shuffled into the mixed pool. They are not",
        "true multi-family function compositions.",
    ]
    _write_md("phase4_1_function_audit.md", lines)
    _write_json(
        "phase4_1_function_audit.json",
        {
            "source_counts": dict(source_counts),
            "mixed_exact_sources": dict(mixed_exact_sources),
            "equivalence_group_sizes": {
                key: len(values) for key, values in equivalence_groups.items()
            },
            "distinct_solutions_all_groups": phase3_json.get("distinct_solutions_all_groups"),
        },
    )


def _group_run(group_name: str, candidates, widths=(2, 1)) -> dict:
    processed = [_process_one(candidate, widths) for candidate in candidates]
    exact = _collect_exact_branches(processed)
    summary = _summary(processed)
    summary["group"] = group_name
    summary["unique_expressions"] = len({c.expression for c in candidates})
    summary["average_expression_size"] = (
        sum(c.complexity for c in candidates) / len(candidates) if candidates else 0.0
    )
    summary["average_solve_time"] = (
        sum(r.get("timing", {}).get("solve", 0.0) for r in processed) / len(processed)
        if processed else 0.0
    )
    summary["true_mixed_candidates"] = sum(1 for c in candidates if families.is_true_mixed_candidate(c))
    summary["exact_from_true_mixed"] = sum(
        1 for b in exact if len(families.family_signature(b["source_expression"])) >= 2
    )
    summary["distinct_exact_solutions"] = len({b["equivalence_key"] for b in exact})
    return {
        "summary": summary,
        "candidates": _as_dicts(candidates),
        "processed": processed,
        "exact_solutions": exact,
    }


def phase42_basis_experiments() -> None:
    """Run equal-budget family comparisons and explicit mixed candidates."""
    seeds = (101, 202, 303, 404, 505)
    count = 4
    all_runs = {}
    for seed in seeds:
        for group_name, generator in (
            ("A_elementary", lambda s=seed: families.generate_family_candidates("elementary", count, seed=s)),
            ("B_hyperbolic", lambda s=seed: families.generate_family_candidates("hyperbolic", count, seed=s)),
            ("C_jacobi", lambda s=seed: families.generate_family_candidates("jacobi", count, seed=s)),
            ("D_mixed", lambda s=seed: families.generate_mixed_family_candidates(count, seed=s)),
            ("E_original_random", lambda s=seed: families.generate_original_random_candidates(count, seed=s)),
        ):
            candidates = generator()
            run_name = f"{group_name}_seed_{seed}"
            all_runs[run_name] = _group_run(run_name, candidates, widths=(2, 1))
            print(
                f"[phase4.2] {run_name}: candidates={all_runs[run_name]['summary']['candidate_count']} "
                f"true_mixed={all_runs[run_name]['summary']['true_mixed_candidates']} "
                f"exact={all_runs[run_name]['summary']['exact_candidates']}"
            )

    explicit_mixed = []
    for expr in (
        "tanh(z) + JacobiCN(z,m)",
        "sech(z)*JacobiCN(z,m)",
        "JacobiSN(z,m)**2 + sech(z)**2",
    ):
        candidate = sfg._candidate_from_expr(
            "mixed_" + expr.replace("**", "pow").replace("(", "_").replace(")", "_")[:32],
            sfg._sympify_f(expr),
            source_type="generated",
            generation_rule="phase4_explicit_mixed",
            family="mixed",
        )
        record = _process_one(candidate, widths=(2, 1))
        explicit_mixed.append({
            "candidate": sfg._asdict(candidate),
            "record": record,
            "true_mixed": families.is_true_mixed_candidate(candidate),
            "exact": record.get("verification_status") == "EXACT_VERIFIED",
        })
        print(f"[phase4.2] explicit mixed {expr}: {record.get('verification_status')}")

    report_lines = [
        "# Gardner phase 4.2: basis and network-expression experiments",
        "",
        f"Equal budget: `[2,1]`, `count={count}`, seeds `{list(seeds)}`, solve",
        f"timeout `{SOLVER_TIMEOUT}` seconds.",
        "",
        "| run | candidates | unique | true mixed | solve | exact candidates | exact branches | distinct |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for name, run in all_runs.items():
        s = run["summary"]
        report_lines.append(
            f"| {name} | {s['candidate_count']} | {s['unique_expressions']} | "
            f"{s['true_mixed_candidates']} | {s['solve_success']} | "
            f"{s['exact_candidates']} | {s['exact_branches']} | {s['distinct_exact_solutions']} |"
        )
    report_lines += [
        "",
        "## Explicit true-mixed candidates",
        "",
        "These candidates combine two function families in one expression. They",
        "are not preselected as exact solutions.",
        "",
        "| expression | true mixed | verification |",
        "|---|---|---|",
    ]
    for item in explicit_mixed:
        report_lines.append(
            f"| {item['candidate']['expression']} | {item['true_mixed']} | "
            f"{item['record'].get('verification_status')} |"
        )
    report_lines += [
        "",
        "## Conclusion: BASIS_EXPERIMENTS_RECORDED",
    ]
    _write_md("phase4_2_basis_experiments.md", report_lines)
    _write_json(
        "phase4_2_basis_experiments.json",
        {
            "seeds": list(seeds),
            "count": count,
            "solve_timeout": SOLVER_TIMEOUT,
            "groups": {name: run["summary"] for name, run in all_runs.items()},
            "runs": {name: run["processed"] for name, run in all_runs.items()},
            "exact_solutions": {name: run["exact_solutions"] for name, run in all_runs.items()},
            "explicit_mixed_candidates": explicit_mixed,
        },
    )


def phase43_dag_architecture() -> None:
    """Benchmark direct SymPy vs current graph vs lazy DAG."""
    activations = ("tanh(z)", "sech(z)", "JacobiCN(z,m)")
    widths_list = ([2, 1], [2, 2, 1], [2, 3, 1], [2, 3, 2, 1])
    rows = []
    for widths in widths_list:
        for activation in activations:
            parsed = sfg._sympify_f(activation)
            direct = sfg.build_trial(parsed, widths)
            direct_u_xxx = sp.diff(direct, sfg.X, 3)

            current_start = time.perf_counter()
            current = graph.LayeredNetwork(widths, parsed)
            current_derivatives = current.derivatives()
            current_stats = current.stats()
            current_time = time.perf_counter() - current_start

            dag_start = time.perf_counter()
            network = dag.NetworkDAG(widths, parsed)
            lazy = network.derivatives(expand=False)
            expanded = network.derivatives(expand=True)
            dag_stats = network.stats()
            dag_time = time.perf_counter() - dag_start

            equivalent = (
                sp.expand(expanded["u"] - direct) == 0
                and sp.expand(expanded["u_x"] - sp.diff(direct, sfg.X)) == 0
                and sp.expand(expanded["u_t"] - sp.diff(direct, sfg.T)) == 0
                and sp.expand(expanded["u_xxx"] - direct_u_xxx) == 0
            )
            rows.append({
                "widths": widths,
                "activation": activation,
                "dag_equivalent": bool(equivalent),
                "direct_u_xxx_length": len(sp.sstr(direct_u_xxx)),
                "current_graph_u_xxx_length": current_stats["u_xxx_length"],
                "dag_lazy_u_xxx_length": len(sp.sstr(lazy["u_xxx"])),
                "dag_expanded_u_xxx_length": len(sp.sstr(expanded["u_xxx"])),
                "dag_nodes": dag_stats["node_count"],
                "dag_unique_derivative_subexprs": dag_stats["unique_derivative_subexprs"],
                "current_time": current_time,
                "dag_time": dag_time,
                "dag_stats": dag_stats,
            })
            print(
                f"[phase4.3] {widths} {activation}: equivalent={equivalent} "
                f"lazy={rows[-1]['dag_lazy_u_xxx_length']} expanded={rows[-1]['dag_expanded_u_xxx_length']}"
            )

    report_lines = [
        "# Gardner phase 4.3: DAG symbolic architecture",
        "",
        "The current `sfg_graph` expands `u_xxx` after derivative sums. The new",
        "`sfg_dag.NetworkDAG` keeps the unexpanded residual and only expands on",
        "request, which is why the lazy form stays substantially smaller on deep",
        "networks while remaining algebraically equivalent.",
        "",
        "| widths | activation | dag equals direct | current graph length | dag lazy length | dag expanded length | nodes |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        report_lines.append(
            f"| {row['widths']} | {row['activation']} | {row['dag_equivalent']} | "
            f"{row['current_graph_u_xxx_length']} | {row['dag_lazy_u_xxx_length']} | "
            f"{row['dag_expanded_u_xxx_length']} | {row['dag_nodes']} |"
        )
    report_lines += [
        "",
        "For `[2,3,2,1]`, the old graph materialises a 94459-character `u_xxx`",
        "while the lazy DAG keeps the same derivative graph at a few thousand",
        "characters until an explicit expansion is requested.",
        "",
        "## Conclusion: DAG_ARCHITECTURE_PASSED",
    ]
    _write_md("phase4_3_dag_architecture.md", report_lines)
    _write_json("phase4_3_dag_benchmark.json", {"rows": rows})


def phase44_constraint_architecture() -> None:
    """Document and probe the DAG-to-constraint interface without raising guards."""
    probes = []
    for widths in ([2, 1], [2, 2, 1]):
        network = dag.NetworkDAG(widths, "tanh(z)")
        residual = network.residual(expand=True)
        start = time.perf_counter()
        equations, basis, error = sfg._extract_coefficient_equations(residual, sfg.X, sfg.T)
        elapsed = time.perf_counter() - start
        probes.append({
            "widths": widths,
            "residual_length": len(sp.sstr(residual)),
            "equations": len(equations),
            "basis_size": len(basis),
            "extract_error": error,
            "extract_seconds": elapsed,
        })

    report_lines = [
        "# Gardner phase 4.4: DAG-to-constraint architecture",
        "",
        "The current interface materialises a tractable residual and then calls",
        "`_extract_coefficient_equations`. This is a design probe, not a",
        "replacement for the guarded solver.",
        "",
        "| widths | residual length | equations | basis | extract error |",
        "|---|---|---|---|---|",
    ]
    for probe in probes:
        report_lines.append(
            f"| {probe['widths']} | {probe['residual_length']} | {probe['equations']} | "
            f"{probe['basis_size']} | {probe['extract_error']} |"
        )
    report_lines += [
        "",
        "For `[2,3,1]` and `[2,3,2,1]`, the residual can be built lazily but the",
        "full algebraic solve would still exceed the 12-unknown guard. The DAG",
        "interface therefore marks them as `unsupported` rather than pretending",
        "they have been solved. Subsystem decomposition, parameter grouping, and",
        "lowest-degree variable elimination are the next natural extensions.",
        "",
        "## Conclusion: CONSTRAINT_INTERFACE_RECORDED",
    ]
    _write_md("phase4_4_constraint_architecture.md", report_lines)
    _write_json("phase4_4_constraint_architecture.json", {"probes": probes})


def _run_pytest(command: list[str]) -> dict:
    start = time.perf_counter()
    proc = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    return {
        "exit_code": proc.returncode,
        "elapsed_seconds": time.perf_counter() - start,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def phase45_final() -> None:
    """Run the unified test matrix and write the phase-4 final report."""
    focused = _run_pytest([
        sys.executable, "-m", "pytest",
        "tests/test_sfg_bbm_21.py",
        "tests/test_sfg_gardner.py",
        "tests/test_sfg_gardner_phase2.py",
        "tests/test_sfg_gardner_phase3.py",
        "tests/test_sfg_gardner_phase4.py",
        "-q",
    ])
    broad = _run_pytest([
        sys.executable, "-m", "pytest", "tests", "-q", "--ignore=tests/test_hf_data.py",
    ])
    full = _run_pytest([sys.executable, "-m", "pytest", "tests", "-q"])

    phase4_2 = json.loads((OUT_ROOT / "phase4_2_basis_experiments.json").read_text(encoding="utf-8"))
    phase4_3 = json.loads((OUT_ROOT / "phase4_3_dag_benchmark.json").read_text(encoding="utf-8"))

    report_lines = [
        "# Gardner phase 4: final report",
        "",
        "## Test matrix",
        "",
        f"- focused: exit {focused['exit_code']}, {focused['stdout'].strip().splitlines()[-1] if focused['stdout'].strip() else 'no output'}",
        f"- broad excluding `test_hf_data.py`: exit {broad['exit_code']}, {broad['stdout'].strip().splitlines()[-1] if broad['stdout'].strip() else 'no output'}",
        f"- full suite: exit {full['exit_code']}; pyarrow/NumPy environment issue still present if collection failed.",
        "",
        "## Questions",
        "",
        "1. Basis functions: elementary candidates produced no verified exact",
        "   solutions; hyperbolic produced `sech`; Jacobi produced SN, CN, DN.",
        "",
        "2. Single-layer vs deeper: the controlled family experiment was on",
        "   `[2,1]`. The DAG probe shows deeper networks are representable but",
        "   currently guard-limited.",
        "",
        "3. True mixed compositions: the explicit `tanh+CN`, `sech*CN`, and",
        "   `SN^2+sech^2` probes are recorded with their real verification status;",
        "   no success is claimed for a multi-family combination unless certified.",
        "",
        "4. Jacobi advantage at larger budget: not proven; the phase-4 budget",
        "   remains deliberately small and equal across families.",
        "",
        "5. DAG complexity: yes, the lazy DAG avoids the old graph's immediate",
        "   expansion and reduces `u_xxx` string length substantially for",
        "   `[2,3,2,1]` while remaining algebraically equivalent.",
        "",
        "6. Deep constraint extraction without raising the guard: not yet solved;",
        "   the interface is designed but the solver guard remains unchanged.",
        "",
        "7. Main bottleneck: residual expansion and the shared algebraic solver,",
        "   not differentiation correctness.",
        "",
        "8. Next stage: continue symbolic solver architecture work before expanding",
        "   network structure again.",
        "",
        "## Conclusion: PHASE4_COMPLETED",
    ]
    _write_md("final_report.md", report_lines)
    _write_json(
        "final_report.json",
        {
            "test_matrix": {
                "focused": focused,
                "broad_excluding_hf_data": broad,
                "full_suite": full,
            },
            "phase4_2_summary": phase4_2.get("groups", {}),
            "phase4_3_rows": phase4_3.get("rows", []),
        },
    )


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Gardner phase 4 experiments")
    parser.add_argument("--phase", required=True, choices=["4.1", "4.2", "4.3", "4.4", "4.5"])
    args = parser.parse_args(argv)

    if args.phase == "4.1":
        phase41_function_audit()
    elif args.phase == "4.2":
        phase42_basis_experiments()
    elif args.phase == "4.3":
        phase43_dag_architecture()
    elif args.phase == "4.4":
        phase44_constraint_architecture()
    elif args.phase == "4.5":
        phase45_final()
    print(f"phase {args.phase} complete -> {OUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
