#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit SIGS expression-generation capability and test whether the current BBM
Stage I depends on the reference solution.

Run from the repository root:
    python scripts/pdes/test_sigs_stage1_audit.py

Optional:
    python scripts/pdes/test_sigs_stage1_audit.py \
        --n-prior 200 --n-cluster 200 --stage1-candidates 40 --seed 42

The script is diagnostic only. It does NOT modify project source files.
It writes CSV/JSON/TXT reports under results/sigs_stage1_audit_<timestamp>/.

Part A distinguishes:
  A1. Expressions already stored in data/clusters.pkl and sampled by
      sample_from_subclusters().
  A2. Expressions actually decoded by the pretrained Grammar-VAE from random
      latent vectors using sample_from_prior().

Part B distinguishes:
  B1. Does changing PDESpec.true_solution alone change current Stage I?
  B2. Can Stage I still generate candidates after removing the explicitly
      target-shaped sech/sech^2 seeds and x-2*t atom from the BBM config?

Important interpretation:
  - Current pde_common.stage_one() is a structural prefilter, not a PDE-residual
    scorer. This script audits reference-solution dependence; it does not claim
    that current Stage I performs blind residual-based discovery.
  - The current BBM configuration still contains manually specified PDE/search
    priors. Those are reported separately from true_solution leakage.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
import time
import traceback
from collections import Counter
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
PDE_DIR = ROOT / "scripts" / "pdes"
CH_DIR = ROOT / "scripts" / "ch"

for p in (str(ROOT), str(SRC), str(PDE_DIR), str(CH_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)


def parse_args():
    p = argparse.ArgumentParser(description="SIGS + Stage-I diagnostic audit")
    p.add_argument("--n-prior", type=int, default=120,
                   help="number of unconditional Grammar-VAE prior samples per decoding mode")
    p.add_argument("--n-cluster", type=int, default=120,
                   help="number of expressions sampled from each available MathClass cluster")
    p.add_argument("--n-subclusters", type=int, default=4,
                   help="KMeans subclusters per MathClass (automatically capped by data size)")
    p.add_argument("--stage1-candidates", type=int, default=40,
                   help="maximum NNSCA structures generated in each Stage-I run")
    p.add_argument("--stage1-n-samples", type=int, default=80,
                   help="SIGS cluster samples requested by each Stage-I run")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--skip-stage1", action="store_true")
    p.add_argument("--skip-model-prior", action="store_true",
                   help="skip Grammar-VAE prior decoding; still audit stored cluster expressions")
    p.add_argument("--output-dir", default=None)
    return p.parse_args()


def timestamp():
    return time.strftime("%Y%m%d_%H%M%S")


def safe_mkdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def json_default(obj):
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, sp.Basic):
        return sp.sstr(obj)
    if hasattr(obj, "name"):
        return obj.name
    return str(obj)


def write_json(path: Path, payload: Any):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2,
                               default=json_default), encoding="utf-8")


def sympy_locals():
    x, y, t, z = sp.symbols("x y t z")
    return {
        "x": x, "y": y, "t": t, "z": z,
        "pi": sp.pi, "E": sp.E,
        "JacobiSN": sp.Function("JacobiSN"),
        "JacobiCN": sp.Function("JacobiCN"),
        "JacobiDN": sp.Function("JacobiDN"),
    }


def parse_expression(text: str):
    if not isinstance(text, str) or not text.strip():
        return None
    s = text.strip().replace("^", "**")
    try:
        return sp.sympify(s, locals=sympy_locals(), evaluate=True)
    except Exception:
        return None


def expression_stats(expressions: list[str], label: str):
    """Count valid expressions, function primitives and univariate subexpressions."""
    locals_ = sympy_locals()
    z = locals_["z"]
    parsed = []
    unique_full = {}
    function_counts = Counter()
    univariate = {}

    for raw in expressions:
        expr = parse_expression(raw)
        if expr is None:
            continue
        parsed.append((raw, expr))
        unique_full.setdefault(sp.srepr(expr), raw)

        for fn in expr.atoms(sp.Function):
            function_counts[fn.func.__name__] += 1

        # Extract function-bearing subtrees that depend on exactly one of x,y,t.
        # This is a practical proxy for possible one-input activation functions,
        # not a claim that the complete SIGS output is already an NNSCA activation.
        for node in sp.preorder_traversal(expr):
            if not isinstance(node, sp.Basic) or not node.has(sp.Function):
                continue
            free = list(node.free_symbols)
            if len(free) != 1:
                continue
            var = free[0]
            if str(var) not in {"x", "y", "t"}:
                continue
            try:
                candidate = sp.simplify(node.subs(var, z))
                if candidate == z or not candidate.has(sp.Function):
                    continue
                univariate.setdefault(sp.srepr(candidate), candidate)
            except Exception:
                continue

    def real_finite_fraction(candidate):
        vals = []
        points = [-1.2, -0.6, -0.15, 0.2, 0.65, 1.1]
        try:
            f = sp.lambdify(z, candidate, modules=["numpy"])
            df = sp.lambdify(z, sp.diff(candidate, z), modules=["numpy"])
            for q in points:
                try:
                    v = complex(np.asarray(f(q)).item())
                    d = complex(np.asarray(df(q)).item())
                    vals.append(
                        math.isfinite(v.real) and math.isfinite(v.imag)
                        and math.isfinite(d.real) and math.isfinite(d.imag)
                        and abs(v.imag) < 1e-8 and abs(d.imag) < 1e-8
                    )
                except Exception:
                    vals.append(False)
        except Exception:
            return 0.0
        return sum(vals) / max(1, len(vals))

    univariate_rows = []
    for key, candidate in univariate.items():
        univariate_rows.append({
            "canonical": sp.sstr(candidate),
            "real_finite_differentiable_fraction": real_finite_fraction(candidate),
            "ops": int(sp.count_ops(candidate)),
        })
    univariate_rows.sort(key=lambda r: (-r["real_finite_differentiable_fraction"], r["ops"], r["canonical"]))

    return {
        "label": label,
        "raw_count": len(expressions),
        "parseable_count": len(parsed),
        "parse_success_rate": len(parsed) / max(1, len(expressions)),
        "unique_full_expression_count": len(unique_full),
        "unique_function_bearing_univariate_subexpressions": len(univariate),
        "function_occurrences": dict(function_counts.most_common()),
        "univariate_candidates": univariate_rows,
        "sample_expressions": expressions[:20],
    }


def write_expression_csv(path: Path, groups: dict[str, list[str]]):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["source", "index", "expression", "parseable", "function_heads",
                    "free_symbols", "count_ops"])
        for source, expressions in groups.items():
            for i, raw in enumerate(expressions):
                expr = parse_expression(raw)
                if expr is None:
                    w.writerow([source, i, raw, False, "", "", ""])
                    continue
                heads = sorted({fn.func.__name__ for fn in expr.atoms(sp.Function)})
                syms = sorted(str(s) for s in expr.free_symbols)
                w.writerow([source, i, raw, True, ",".join(heads),
                            ",".join(syms), int(sp.count_ops(expr))])


def load_cluster_data(cluster_path: Path):
    from sigs.utils import FileUtils
    data = FileUtils.load_pickle(str(cluster_path))
    if data is None:
        raise RuntimeError(f"Cannot load cluster file: {cluster_path}")
    return data


def run_cluster_corpus_audit(cluster_path: Path, n_samples: int, n_subclusters: int,
                             seed: int):
    """Sample existing expressions from stored cluster pools by MathClass."""
    from sigs.sampler import FlexibleVectorSampler
    from sigs.utils import MathClass

    cluster_data = load_cluster_data(cluster_path)
    sampler = FlexibleVectorSampler(cluster_file=str(cluster_path), device="cpu")
    result = {}
    errors = {}

    preferred = [
        MathClass.SPATIOTEMPORAL_2D,
        MathClass.SPATIOTEMPORAL_3D,
        MathClass.SPATIAL_1D,
        MathClass.TEMPORAL_1D,
        MathClass.CONSTANT,
    ]

    for offset, category in enumerate(preferred):
        key = category.name
        if key not in cluster_data:
            errors[key] = "category not present in clusters.pkl"
            continue
        count = len(cluster_data[key].get("expressions", []))
        vectors = cluster_data[key].get("vectors", [])
        if count == 0:
            errors[key] = "empty category"
            continue
        k = max(1, min(n_subclusters, count, len(vectors)))
        try:
            sample_id = sampler.sample_from_subclusters(
                categories={category: k},
                n_samples=n_samples,
                operator="",
                seed=seed + offset,
                model=None,
            )
            expressions, _, _, _ = sampler.get_sampling_results(sample_id)
            result[key] = list(expressions)
        except Exception as exc:
            errors[key] = f"{type(exc).__name__}: {exc}"

    return result, errors, {
        "cluster_categories": {
            k: {
                "stored_expression_count": len(v.get("expressions", [])),
                "stored_vector_count": len(v.get("vectors", [])),
            }
            for k, v in cluster_data.items()
        }
    }


def run_model_prior_audit(cluster_path: Path, config_path: Path, checkpoint_path: Path,
                          n_prior: int, seed: int):
    """Decode fresh expressions from random latent vectors using the pretrained GVAE."""
    import torch
    from sigs.sampler import FlexibleVectorSampler
    from sigs.utils import ModelUtils

    config = ModelUtils.load_config(str(config_path))
    model = ModelUtils.load_checkpoint(str(checkpoint_path), config)
    model.eval()
    sampler = FlexibleVectorSampler(
        cluster_file=str(cluster_path),
        model=model,
        device="cpu",
    )

    generated = {}
    errors = {}

    # sample=True: native GrammarVAE.generate() sampling path.
    try:
        sid = sampler.sample_from_prior(
            n_samples=n_prior, scale=1.0, sample=True, seed=seed
        )
        exprs, _, _, _ = sampler.get_sampling_results(sid)
        generated["gvae_prior_native_sample"] = list(exprs)
    except Exception as exc:
        errors["gvae_prior_native_sample"] = f"{type(exc).__name__}: {exc}"

    # sample=False: decoder-logit -> grammar-constrained argmax decoding path.
    try:
        sid = sampler.sample_from_prior(
            n_samples=n_prior, scale=1.0, sample=False, seed=seed + 1
        )
        exprs, _, _, _ = sampler.get_sampling_results(sid)
        generated["gvae_prior_argmax_decode"] = list(exprs)
    except Exception as exc:
        errors["gvae_prior_argmax_decode"] = f"{type(exc).__name__}: {exc}"

    return generated, errors


def stage1_records(groups):
    rows = []
    for group in groups:
        for expr, codes in group.get("members", []):
            rows.append({
                "group": group.get("name"),
                "expr": str(expr),
                "codes": list(codes) if codes is not None else None,
            })
    return rows


def run_stage1_once(spec, args, seed: int):
    import pde_common
    _, _, groups = pde_common.stage_one(
        spec,
        n_samples=args.stage1_n_samples,
        seed=seed,
        n_seeds=1,
        widths=[2, 2, 1],
        max_candidates=args.stage1_candidates,
    )
    return stage1_records(groups)


def audit_stage1_reference_independence(args):
    import equations
    import sympy as sp

    base = equations.BBM
    x, t = sp.symbols("x t")

    # B1: Same PDE/search configuration, only the reference solution is changed.
    # If Stage I is truly independent of true_solution, deterministic outputs
    # should be identical.
    alt_reference = sp.sin(3 * x) + sp.cos(2 * t) + x / 7
    spec_alt_reference = replace(base, true_solution=alt_reference)

    print("\n[B1] Stage-I reference-solution mutation test")
    print("  Run 1: original BBM PDESpec")
    rows_original = run_stage1_once(base, args, args.seed)
    print("  Run 2: same BBM config, unrelated true_solution")
    rows_altered = run_stage1_once(spec_alt_reference, args, args.seed)

    keys_original = [(r["expr"], tuple(r["codes"] or [])) for r in rows_original]
    keys_altered = [(r["expr"], tuple(r["codes"] or [])) for r in rows_altered]
    invariant = keys_original == keys_altered

    # B2: Remove explicit target-family priors from the BBM config.
    # Keep the PDE residual and general search setup unchanged.
    blind_seeds = [
        (name, code) for name, code in base.seed_functions
        if name.lower() not in {"sech", "sech2"}
    ]
    blind_atoms = [
        atom for atom in base.search_atoms
        if "sech" not in atom.lower()
        and "x - 2*t" not in atom.replace(" ", "")
        and "x-2*t" not in atom.replace(" ", "")
    ]
    blind_phases = [
        phase for phase in (base.first_layer_phases or [])
        if "sech" not in phase.lower()
        and "x - 2*t" not in phase.replace(" ", "")
        and "x-2*t" not in phase.replace(" ", "")
    ]
    blind_spec = replace(
        base,
        true_solution=alt_reference,
        seed_functions=blind_seeds,
        search_atoms=blind_atoms,
        first_layer_phases=blind_phases or None,
        extra_ansatz=[],
    )

    print("\n[B2] Target-shaped prior ablation test")
    print("  Removed seed functions:", sorted(
        {name for name, _ in base.seed_functions}
        - {name for name, _ in blind_seeds}
    ))
    print("  Removed search atoms:", sorted(set(base.search_atoms) - set(blind_atoms)))
    print("  Run 3: ablated config, unrelated true_solution")
    rows_blind = run_stage1_once(blind_spec, args, args.seed)

    def summarize(rows):
        exprs = [r["expr"] for r in rows]
        return {
            "candidate_count": len(rows),
            "unique_expression_count": len(set(exprs)),
            "contains_sech_text_count": sum("sech" in e.lower() for e in exprs),
            "contains_jacobicn_count": sum("jacobicn" in e.lower() for e in exprs),
            "sample_candidates": exprs[:20],
        }

    config_audit = {
        "reference_solution_original": sp.sstr(base.true_solution),
        "reference_solution_alternative": sp.sstr(alt_reference),
        "original_seed_functions": base.seed_functions,
        "original_search_atoms": base.search_atoms,
        "original_first_layer_phases": base.first_layer_phases,
        "blind_seed_functions": blind_seeds,
        "blind_search_atoms": blind_atoms,
        "blind_first_layer_phases": blind_phases,
    }

    return {
        "reference_mutation_invariant": invariant,
        "original_vs_altered_exactly_equal": invariant,
        "original_stage1": summarize(rows_original),
        "altered_reference_stage1": summarize(rows_altered),
        "target_prior_ablated_stage1": summarize(rows_blind),
        "target_prior_ablation_candidate_overlap": (
            len(set(r["expr"] for r in rows_original) &
                set(r["expr"] for r in rows_blind))
            / max(1, len(set(r["expr"] for r in rows_original)))
        ),
        "config_audit": config_audit,
        "candidate_rows": {
            "original": rows_original,
            "altered_reference": rows_altered,
            "target_prior_ablated": rows_blind,
        },
        "interpretation": {
            "reference_independence": (
                "PASS: changing PDESpec.true_solution did not change Stage-I candidates."
                if invariant else
                "FAIL/UNEXPECTED: changing true_solution changed Stage-I candidates."
            ),
            "important_caveat": (
                "This only tests direct dependence on true_solution. It does not mean "
                "the search is free of hand-designed priors: seed_functions, search_atoms "
                "and first_layer_phases remain manually specified."
            ),
        },
    }


def main():
    args = parse_args()
    out = Path(args.output_dir) if args.output_dir else (
        ROOT / "results" / f"sigs_stage1_audit_{timestamp()}"
    )
    safe_mkdir(out)

    cluster_path = ROOT / "data" / "clusters.pkl"
    config_path = ROOT / "configs" / "config.yaml"
    checkpoint_path = ROOT / "data" / "model.ckpt"

    report = {
        "repo_root": str(ROOT),
        "created_at": timestamp(),
        "arguments": vars(args),
        "paths": {
            "cluster_file": str(cluster_path),
            "config_file": str(config_path),
            "checkpoint_file": str(checkpoint_path),
        },
        "part_A": {},
        "part_B": {},
        "warnings": [],
    }

    print("=" * 78)
    print("SIGS GENERATION CAPABILITY + BBM STAGE-I REFERENCE-INDEPENDENCE AUDIT")
    print("=" * 78)
    print("Repository:", ROOT)
    print("Output:", out)

    # ----------------------------- Part A ---------------------------------
    print("\n" + "=" * 78)
    print("PART A — What expression structures can SIGS provide?")
    print("=" * 78)

    all_expression_groups = {}

    if not cluster_path.exists():
        report["warnings"].append(
            f"Missing cluster file: {cluster_path}. Part A cluster sampling and "
            "current Stage I cannot run until SIGS data are downloaded."
        )
        print("[WARN] Missing:", cluster_path)
    else:
        try:
            cluster_samples, cluster_errors, cluster_meta = run_cluster_corpus_audit(
                cluster_path, args.n_cluster, args.n_subclusters, args.seed
            )
            report["part_A"]["stored_cluster_sampling"] = {
                "summary_by_mathclass": {
                    key: expression_stats(value, key)
                    for key, value in cluster_samples.items()
                },
                "errors": cluster_errors,
                "cluster_metadata": cluster_meta,
            }
            all_expression_groups.update({
                f"cluster_{k}": v for k, v in cluster_samples.items()
            })
            print("\nStored cluster expression sampling:")
            for key, value in report["part_A"]["stored_cluster_sampling"]["summary_by_mathclass"].items():
                print(
                    f"  {key}: raw={value['raw_count']}, "
                    f"parseable={value['parseable_count']}, "
                    f"unique_expr={value['unique_full_expression_count']}, "
                    f"univariate_function_structures="
                    f"{value['unique_function_bearing_univariate_subexpressions']}"
                )
            for key, err in cluster_errors.items():
                print(f"  [WARN] {key}: {err}")
        except Exception as exc:
            report["part_A"]["stored_cluster_sampling_error"] = (
                f"{type(exc).__name__}: {exc}"
            )
            report["warnings"].append("Cluster sampling failed: " + str(exc))
            traceback.print_exc()

    if not args.skip_model_prior:
        if not (cluster_path.exists() and config_path.exists() and checkpoint_path.exists()):
            missing = [str(p) for p in (cluster_path, config_path, checkpoint_path) if not p.exists()]
            report["part_A"]["gvae_prior_decode"] = {
                "skipped": True,
                "reason": "Missing required model/data files: " + "; ".join(missing),
            }
            print("\n[SKIP] Actual Grammar-VAE prior decoding; missing:", missing)
        else:
            try:
                prior_groups, prior_errors = run_model_prior_audit(
                    cluster_path, config_path, checkpoint_path,
                    args.n_prior, args.seed + 1000
                )
                report["part_A"]["gvae_prior_decode"] = {
                    "summary_by_decode_mode": {
                        key: expression_stats(value, key)
                        for key, value in prior_groups.items()
                    },
                    "errors": prior_errors,
                }
                all_expression_groups.update(prior_groups)
                print("\nActual Grammar-VAE prior decoding:")
                for key, value in report["part_A"]["gvae_prior_decode"]["summary_by_decode_mode"].items():
                    print(
                        f"  {key}: raw={value['raw_count']}, "
                        f"parseable={value['parseable_count']}, "
                        f"unique_expr={value['unique_full_expression_count']}, "
                        f"univariate_function_structures="
                        f"{value['unique_function_bearing_univariate_subexpressions']}"
                    )
                for key, err in prior_errors.items():
                    print(f"  [WARN] {key}: {err}")
            except Exception as exc:
                report["part_A"]["gvae_prior_decode_error"] = (
                    f"{type(exc).__name__}: {exc}"
                )
                report["warnings"].append("Grammar-VAE prior decoding failed: " + str(exc))
                traceback.print_exc()
    else:
        report["part_A"]["gvae_prior_decode"] = {"skipped": True, "reason": "--skip-model-prior"}

    if all_expression_groups:
        write_expression_csv(out / "part_A_all_expressions.csv", all_expression_groups)

    # Write a concise function-candidate CSV from all univariate candidates.
    activation_rows = []
    for source, expressions in all_expression_groups.items():
        stats = expression_stats(expressions, source)
        for row in stats["univariate_candidates"]:
            activation_rows.append([
                source, row["canonical"],
                row["real_finite_differentiable_fraction"], row["ops"]
            ])
    with (out / "part_A_univariate_function_candidates.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as f:
        w = csv.writer(f)
        w.writerow(["source", "candidate_phi_z", "real_finite_differentiable_fraction", "count_ops"])
        w.writerows(activation_rows)

    # ----------------------------- Part B ---------------------------------
    if not args.skip_stage1:
        print("\n" + "=" * 78)
        print("PART B — Can current BBM Stage I run without using the reference solution?")
        print("=" * 78)
        try:
            b = audit_stage1_reference_independence(args)
            report["part_B"] = {k: v for k, v in b.items() if k != "candidate_rows"}
            for run_name, rows in b["candidate_rows"].items():
                with (out / f"part_B_candidates_{run_name}.csv").open(
                    "w", newline="", encoding="utf-8-sig"
                ) as f:
                    w = csv.writer(f)
                    w.writerow(["candidate_id", "group", "expression", "activation_codes"])
                    for i, row in enumerate(rows, start=1):
                        w.writerow([i, row["group"], row["expr"], row["codes"]])
            print("\nB1 result:", report["part_B"]["interpretation"]["reference_independence"])
            print("  Original candidates:", b["original_stage1"]["candidate_count"])
            print("  Altered-reference candidates:", b["altered_reference_stage1"]["candidate_count"])
            print("  Exact candidate equality:", b["reference_mutation_invariant"])
            print("\nB2 target-prior ablation:")
            print("  Original candidates:", b["original_stage1"]["candidate_count"])
            print("  Ablated candidates:", b["target_prior_ablated_stage1"]["candidate_count"])
            print("  Original candidates containing 'sech':",
                  b["original_stage1"]["contains_sech_text_count"])
            print("  Ablated candidates containing 'sech':",
                  b["target_prior_ablated_stage1"]["contains_sech_text_count"])
            print("  Candidate overlap ratio:",
                  f"{b['target_prior_ablation_candidate_overlap']:.3f}")
            print("\nCaveat:", b["interpretation"]["important_caveat"])
        except Exception as exc:
            report["part_B"]["error"] = f"{type(exc).__name__}: {exc}"
            report["warnings"].append("Stage-I reference-independence test failed: " + str(exc))
            traceback.print_exc()
    else:
        report["part_B"] = {"skipped": True}

    # ----------------------------- Summary --------------------------------
    write_json(out / "report.json", report)

    lines = [
        "SIGS + Stage-I audit report",
        f"Repository: {ROOT}",
        f"Output: {out}",
        "",
        "PART A: SIGS expression capability",
        "  See report.json and part_A_all_expressions.csv.",
        "  part_A_univariate_function_candidates.csv contains extracted one-variable",
        "  function-bearing subexpressions that may be considered as activation candidates.",
        "",
        "PART B: Stage-I reference independence",
        "  See report.json and part_B_candidates_*.csv.",
        "  B1 changes only PDESpec.true_solution while keeping the PDE/search config fixed.",
        "  B2 additionally removes explicit sech/sech2 target-family seeds and x-2*t atoms.",
        "",
        "Interpretation warning:",
        "  The current Stage I is a structural prefilter. It does not currently rank",
        "  candidates by PDE residual. Passing B1 only proves that true_solution is not",
        "  directly read by stage_one(); it does not prove that Stage I is free from",
        "  manually designed function/phase priors or that it discovers exact solutions.",
        "",
        "No source files were modified.",
    ]
    (out / "README_report.txt").write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 78)
    print("AUDIT FINISHED")
    print("Reports saved to:", out)
    print("  report.json")
    print("  part_A_all_expressions.csv")
    print("  part_A_univariate_function_candidates.csv")
    print("  part_B_candidates_*.csv")
    print("  README_report.txt")
    print("=" * 78)


if __name__ == "__main__":
    main()
