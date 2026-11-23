#!/usr/bin/env python3
"""BBM-specific hierarchical search pipeline.

The generic engine in ``pde_common`` keeps CH and KdV unchanged.  This module
adds the BBM-only layers requested for the Python-Maple workflow:

* structural feature analysis and hierarchical scheduling,
* a quick SymPy derivative check,
* three Maple export paths (A: coefficients, B: residual, C: raw task),
* result-file import and exact back-substitution verification,
* a per-run Markdown report.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from pathlib import Path

import sympy as sp

import pde_common
import ch_common as _ch
import equations
import maple_export as me

X, T = sp.symbols("x t")
SPEC = equations.BBM
WIDTHS = [2, 2, 1]
MAPLE_ROOT = Path("/Users/kang/SIGS/maple")
GRADE_ORDER = {"simple": 0, "medium": 1, "complex": 2}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BBM NNSCA hierarchical search")
    parser.add_argument("--n-samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-seeds", type=int, default=5)
    parser.add_argument("--max-candidates", type=int, default=2000)
    parser.add_argument("--stage2-only", action="store_true")
    parser.add_argument("--expr", default=None, help="initial ansatz for --stage2-only")
    parser.add_argument("--no-stage2", action="store_true", help="stop after candidate generation")
    parser.add_argument("--hierarchical", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--prefilter-max-depth", type=int, default=3)
    parser.add_argument("--prefilter-max-complexity", type=float, default=180.0)
    parser.add_argument("--category-budget-file", default=None)
    parser.add_argument("--quick-check-timeout", type=float, default=3.0)
    parser.add_argument("--quick-check-all", action="store_true",
                        help="run the quick SymPy check on maple-only candidates too")
    parser.add_argument("--maple-root", default=str(MAPLE_ROOT))
    parser.add_argument("--import-maple-results", action="store_true")
    parser.add_argument("--maple-results-dir", default=None)
    return parser


def _parameterize(expr: str):
    sym_expr, params = _ch.numerics_to_symbols(expr)
    return sym_expr, params


def flatten_candidates(groups: list[dict], widths: list[int]) -> list[dict]:
    records = []
    candidate_id = 0
    for group in groups:
        group_name = group["name"]
        seed_code = group["seed_code"]
        header = group_name if seed_code is None else f"seed {group_name} (first-layer code {seed_code})"
        for rank, (expr, codes) in enumerate(group["members"], start=1):
            candidate_id += 1
            sym_expr, params = _parameterize(expr)
            records.append({
                "candidate_id": candidate_id,
                "expr": expr,
                "parameterized_expr": sym_expr,
                "params": params,
                "codes": codes,
                "widths": widths,
                "group": header,
                "rank": rank,
                "features": None,
                "path_kind": None,
                "try_sympy": True,
                "duplicate": False,
                "maple_pending_path": None,
                "maple_result_path": None,
                "quick_result": None,
                "sympy_result": None,
            })
    return records


def _load_category_budget(path: str | None) -> dict[str, int]:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {str(k): int(v) for k, v in data.items()}


def prepare_records(records: list[dict], args) -> list[dict]:
    """Analyse, deduplicate and schedule candidates without deleting any."""
    budget = _load_category_budget(args.category_budget_file)
    used = Counter()
    seen = set()
    active = []
    for record in records:
        record["features"] = me.analyze_candidate_structure(
            record["candidate_id"], record["expr"], record["codes"], record["widths"]
        )
        try:
            sym = me._safe_sympify(record["parameterized_expr"])
            key = me.candidate_structure_key(sym, record["features"]) if sym is not None else str(record["expr"])
        except Exception:
            key = str(record["expr"])
        if key in seen:
            record["duplicate"] = True
            continue
        seen.add(key)

        features = record["features"]
        if not args.hierarchical:
            record["try_sympy"] = True
            active.append(record)
            continue

        grade = features.complexity_grade
        category = features.structure_class
        hard_reasons = []
        if features.nesting_depth > args.prefilter_max_depth:
            hard_reasons.append(f"depth>{args.prefilter_max_depth}")
        if features.count_ops > args.prefilter_max_complexity:
            hard_reasons.append(f"complexity>{args.prefilter_max_complexity}")
        if features.derivative_timeout:
            hard_reasons.append("derivative_timeout")

        if hard_reasons or grade == "complex":
            record["try_sympy"] = False
            record["maple_reason"] = ", ".join(hard_reasons or [f"grade={grade}"])
            active.append(record)
            continue

        if category in budget and used[category] >= budget[category]:
            record["try_sympy"] = False
            record["maple_reason"] = f"category budget exhausted for {category}"
            active.append(record)
            continue

        used[category] += 1
        record["try_sympy"] = True
        active.append(record)

    active.sort(key=lambda r: (
        0 if r["try_sympy"] else 1,
        GRADE_ORDER.get(r["features"].complexity_grade, 9),
        r["features"].count_ops,
        r["candidate_id"],
    ))
    return active


def _classify_sympy_result(result: dict) -> str:
    if result.get("coefficient_equations"):
        return "A"
    if "residual" in result:
        return "B"
    return "C"


def _run_search(args) -> int:
    run_id = time.strftime("%Y%m%d_%H%M%S")
    run_root = Path(args.maple_root) / "pending" / f"run_{run_id}"
    pending_dir = run_root
    results_dir = Path(args.maple_root) / "results" / f"run_{run_id}"
    run_root.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    problem = pde_common.create_problem(SPEC)
    print(f"operator: {problem['operators']}")
    print(f"true solution: {problem['true_solution']}")

    if args.stage2_only:
        expr = args.expr or sp.sstr(SPEC.true_solution)
        groups = [{"name": "stage2-only", "seed_code": None, "members": [(expr, None)]}]
    else:
        _expr, _codes, groups = pde_common.stage_one(
            SPEC,
            args.n_samples,
            args.seed,
            n_seeds=args.n_seeds,
            widths=WIDTHS,
            max_candidates=args.max_candidates,
        )

    raw_records = flatten_candidates(groups, WIDTHS)
    total_raw = len(raw_records)
    records = prepare_records(raw_records, args)
    deduped = len(records)
    duplicate_count = total_raw - deduped

    if args.no_stage2:
        for record in records:
            print(f"candidate {record['candidate_id']}: {record['expr']}")
        return 0

    stats = Counter(
        quick_ok=0,
        quick_timeout=0,
        quick_unsupported=0,
        quick_error=0,
        sympy_exact=0,
        sympy_success=0,
        sympy_extract_fail=0,
        sympy_solve_fail=0,
        sympy_timeout=0,
        maple_only=0,
        maple_a=0,
        maple_b=0,
        maple_c=0,
        no_solution=0,
    )
    exact_solutions = []
    exported_records = []

    for record in records:
        cid = record["candidate_id"]
        features = record["features"]
        if not record["try_sympy"]:
            stats["maple_only"] += 1
            record["quick_result"] = {"status": "skipped_complexity", "parts": {}, "message": "maple-only by hierarchical filter"}
            record["path_kind"] = "C"
            record["sympy_result"] = {"status": "unsupported", "message": "deferred to Maple by hierarchical filter"}
            _export_record(record, pending_dir, results_dir, run_id, stats, exported_records)
            continue

        quick = me.quick_check_bbm(record["expr"], args.quick_check_timeout)
        record["quick_result"] = quick
        stats[f"quick_{quick['status']}"] += 1
        if quick["status"] == "unsupported":
            record["path_kind"] = "C"
            record["sympy_result"] = {"status": "unsupported", "message": "quick SymPy check could not parse the candidate"}
            _export_record(record, pending_dir, results_dir, run_id, stats, exported_records)
            continue

        print(f"  candidate #{cid} (codes={record['codes']}) solving symbolically...", flush=True)
        result = pde_common.symbolic_stage_two(SPEC, record["expr"], record["codes"], problem)
        record["sympy_result"] = result
        if result["status"] == "exact":
            stats["sympy_exact"] += 1
            branches = result.get("branches", [])
            for branch in branches:
                branch.setdefault("candidate_expr", record["parameterized_expr"])
                exact_solutions.append((record["group"], record["rank"], record["codes"], branch))
            continue
        if result["status"] == "no_solution":
            stats["no_solution"] += 1
            continue
        path_kind = _classify_sympy_result(result)
        record["path_kind"] = path_kind
        stats[f"maple_{path_kind.lower()}"] += 1
        if path_kind == "A":
            stats["sympy_solve_fail"] += 1
        elif path_kind == "B":
            stats["sympy_extract_fail"] += 1
        else:
            stats["sympy_timeout"] += 1
        _export_record(record, pending_dir, results_dir, run_id, stats, exported_records)

    manifest_path = me.write_manifest(records, pending_dir / "run_manifest.json")
    exact_pre = run_root / "BBM_exact_pre.txt"
    exact_post = run_root / "BBM_exact_post.txt"
    if exact_solutions:
        exact_solutions = pde_common._dedupe_exact_solutions(exact_solutions)
        pde_common._write_exact_solutions(SPEC, exact_solutions, exact_pre, label="pre-filter")
        pde_common._write_exact_solutions(SPEC, exact_solutions, exact_post, label="post-filter(all)")
    else:
        pde_common._write_exact_solutions(SPEC, [], exact_pre, label="pre-filter")
        pde_common._write_exact_solutions(SPEC, [], exact_post, label="post-filter(all)")

    report_path = _write_report(
        run_root, results_dir, run_id, stats, total_raw, deduped, duplicate_count,
        records, exact_solutions, exported_records, manifest_path,
    )
    print("=" * 70)
    print("BBM hierarchical search summary")
    print(f"  run id: {run_id}")
    print(f"  total raw candidates: {total_raw}")
    print(f"  after structural dedup: {deduped} ({duplicate_count} duplicates removed)")
    print(f"  quick SymPy ok/timeout/unsupported/error: "
          f"{stats['quick_ok']}/{stats['quick_timeout']}/{stats['quick_unsupported']}/{stats['quick_error']}")
    print(f"  exact verified branches (deduped): {len(exact_solutions)}")
    print(f"  maple-only candidates: {stats['maple_only']}")
    print(f"  maple exports A/B/C: {stats['maple_a']}/{stats['maple_b']}/{stats['maple_c']}")
    print(f"  Maple files: {pending_dir}")
    print(f"  results directory: {results_dir}")
    print(f"  report: {report_path}")
    print("=" * 70)
    return 0


def _export_record(record, pending_dir: Path, results_dir: Path, run_id: str, stats, exported_records):
    candidate_id = record["candidate_id"]
    path_kind = record["path_kind"]
    stem = f"candidate_{candidate_id:04d}_run_{run_id}"
    record["maple_pending_path"] = pending_dir / f"{stem}.mpl"
    # The generated Maple script writes this result file.
    record["maple_result_path"] = results_dir / f"{stem}.txt"
    me.write_maple_file(
        record,
        record["maple_result_path"],
        path_kind,
        record.get("sympy_result"),
        record.get("quick_result") or {},
        run_id,
    )
    exported_records.append(record)


def _write_report(
    run_root: Path,
    results_dir: Path,
    run_id: str,
    stats: Counter,
    total_raw: int,
    deduped: int,
    duplicate_count: int,
    records: list[dict],
    exact_solutions: list,
    exported_records: list[dict],
    manifest_path: Path,
) -> Path:
    lines = [
        "# BBM hierarchical search report",
        "",
        f"- run id: `{run_id}`",
        f"- total candidates generated: {total_raw}",
        f"- after structural dedup: {deduped}",
        f"- duplicates removed: {duplicate_count}",
        "",
        "## Structure classes",
    ]
    class_counts = Counter(r["features"].structure_class for r in records)
    for name, count in sorted(class_counts.items()):
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Complexity grades")
    grade_counts = Counter(r["features"].complexity_grade for r in records)
    for name, count in sorted(grade_counts.items()):
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## SymPy quick check")
    lines.append(f"- ok: {stats['quick_ok']}")
    lines.append(f"- timeout: {stats['quick_timeout']}")
    lines.append(f"- unsupported: {stats['quick_unsupported']}")
    lines.append(f"- error: {stats['quick_error']}")
    lines.append("")
    lines.append("## SymPy full stage")
    lines.append(f"- exact candidates: {stats['sympy_exact']}")
    lines.append(f"- coefficient extraction failed (path B): {stats['sympy_extract_fail']}")
    lines.append(f"- coefficient solve failed (path A): {stats['sympy_solve_fail']}")
    lines.append(f"- timeouts (path C): {stats['sympy_timeout']}")
    lines.append(f"- no_solution: {stats['no_solution']}")
    lines.append("")
    lines.append("## Maple exports")
    lines.append(f"- path A: {stats['maple_a']}")
    lines.append(f"- path B: {stats['maple_b']}")
    lines.append(f"- path C: {stats['maple_c']}")
    lines.append(f"- maple-only deferred: {stats['maple_only']}")
    lines.append("")
    lines.append("## Exact solutions after dedup")
    lines.append(f"- independent solution families: {len(exact_solutions)}")
    for idx, (_header, rank, codes, solution) in enumerate(exact_solutions[:20], start=1):
        lines.append(f"{idx}. candidate #{rank} codes={codes}")
        lines.append(f"   u = {sp.sstr(solution['exact_expr'])}")
    lines.append("")
    lines.append("## Locations")
    lines.append(f"- Maple pending directory: `{run_root}`")
    lines.append(f"- Maple result directory: `{results_dir}`")
    lines.append(f"- candidate manifest: `{manifest_path}`")
    lines.append("")
    lines.append("## Generated Maple files")
    if exported_records:
        for record in exported_records:
            lines.append(f"- `{record['maple_pending_path']}`  (path {record['path_kind']})")
    else:
        lines.append("- none")
    path = run_root / "report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _parse_constraint_text(text: str) -> tuple[sp.Symbol, sp.Expr] | None:
    try:
        if "=" not in text:
            return None
        left_text, right_text = text.split("=", 1)
        left = sp.Symbol(left_text.strip())
        right = me.maple_to_sympy(right_text)
    except Exception:
        return None
    if not left.is_Symbol:
        return None
    return left, sp.expand(right)


def _parse_constraints(texts: list[str]) -> dict[sp.Symbol, sp.Expr]:
    constraints = {}
    for text in texts:
        parsed = _parse_constraint_text(text)
        if parsed is None:
            continue
        sym, value = parsed
        constraints[sym] = value
    return constraints


def _run_import(args) -> int:
    results_root = Path(args.maple_results_dir or Path(args.maple_root) / "results")
    if not results_root.exists():
        print(f"no Maple results directory: {results_root}")
        return 1

    manifests = {}
    pending_root = Path(args.maple_root) / "pending"
    for manifest_path in list(pending_root.glob("*/run_manifest.json")) + list(results_root.glob("*/run_manifest.json")):
        try:
            for item in me.load_manifest(manifest_path):
                manifests[int(item["candidate_id"])] = item
        except Exception as exc:
            print(f"could not load manifest {manifest_path}: {exc}")

    result_files = sorted(results_root.glob("candidate_*.txt")) + sorted(results_root.glob("*/candidate_*.txt"))
    print(f"found {len(result_files)} Maple result file(s)")
    exact_verified = []
    unverified = []
    unsolved = []
    statuses = Counter()
    for path in result_files:
        try:
            result = me.parse_result_text(path)
        except Exception as exc:
            statuses["error"] += 1
            unverified.append({"path": path, "error": f"parse failed: {exc}"})
            continue
        status = result.get("status", "unknown")
        statuses[status] += 1
        if status != "solved":
            unsolved.append({"candidate_id": result.get("candidate_id"), "status": status, "path": path})
            continue
        candidate_id = result.get("candidate_id")
        record = manifests.get(candidate_id)
        if record is None:
            unverified.append({"path": path, "error": f"candidate {candidate_id} missing from manifests"})
            continue

        solution_blocks = result.get("solutions") or [{"constraints": result.get("constraints", []), "expr": result.get("solution_expression")}]
        for block in solution_blocks:
            constraints = _parse_constraints(block.get("constraints", []))
            if not constraints:
                # Try a top-level constraint fallback.
                constraints = _parse_constraints(result.get("constraints", []))
            if not constraints:
                unverified.append({"candidate_id": candidate_id, "path": path, "error": "no parseable constraints"})
                continue
            try:
                parameterized = record.get("parameterized_expr") or record["expr"]
                f = sp.sympify(parameterized, locals=_ch.SYMPY_LOCALS).subs(constraints)
                residual = SPEC.residual(f, X, T)
                if not pde_common._residual_numeric_zero(residual, X, T):
                    verdict = False
                else:
                    verdict, error = _ch._call_with_timeout(
                        lambda: pde_common._residual_is_zero(residual),
                        pde_common.STAGE2_VERIFY_TIMEOUT,
                    )
                    verdict = error is None and verdict
            except Exception as exc:
                unverified.append({"candidate_id": candidate_id, "path": path, "error": f"verification failed: {exc}"})
                continue
            entry = {
                "candidate_id": candidate_id,
                "path": str(path),
                "exact_expr": f,
                "constraints": {sp.sstr(k): sp.sstr(v) for k, v in constraints.items()},
                "residual": residual,
                "verdict": "exact_verified" if verdict else "unverified",
            }
            if verdict:
                exact_verified.append(entry)
            else:
                unverified.append(entry)

    # Deduplicate verified branches.
    x, t = sp.symbols("x t")
    unique_verified = []
    seen = set()
    for entry in exact_verified:
        key = sp.srepr(pde_common._canonical_branch_expr(entry["exact_expr"], x, t))
        if key not in seen:
            seen.add(key)
            unique_verified.append(entry)

    report_lines = [
        "# BBM Maple result import report",
        "",
        f"- result files read: {len(result_files)}",
        f"- statuses: {dict(statuses)}",
        f"- exact_verified before dedup: {len(exact_verified)}",
        f"- independent verified families: {len(unique_verified)}",
        f"- unverified: {len(unverified)}",
        f"- unsolved/timeout/other: {len(unsolved)}",
        "",
        "## Verified solutions",
    ]
    for idx, entry in enumerate(unique_verified, start=1):
        report_lines.append(f"{idx}. candidate {entry['candidate_id']}")
        report_lines.append(f"   u = {sp.sstr(entry['exact_expr'])}")
        report_lines.append(f"   constraints = {entry['constraints']}")
        report_lines.append(f"   residual = {sp.sstr(entry['residual'])}")
    report_path = results_root / "import_report.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("=" * 70)
    print("BBM Maple result import")
    print(f"  results root: {results_root}")
    print(f"  statuses: {dict(statuses)}")
    print(f"  exact_verified: {len(exact_verified)}")
    print(f"  independent verified families: {len(unique_verified)}")
    print(f"  unverified: {len(unverified)}")
    print(f"  unsolved/timeout/other: {len(unsolved)}")
    print(f"  report: {report_path}")
    print("=" * 70)
    for entry in unique_verified:
        print(f"VERIFIED candidate {entry['candidate_id']}: u = {sp.sstr(entry['exact_expr'])}")
    return 0


def main():
    args = build_parser().parse_args()
    if args.import_maple_results:
        raise SystemExit(_run_import(args))
    raise SystemExit(_run_search(args))


if __name__ == "__main__":
    main()
