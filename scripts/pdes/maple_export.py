#!/usr/bin/env python3
"""Maple export/import helpers for the BBM semi-automatic NNSCA search.

This module intentionally contains no Maple process invocation.  It only
generates human-runnable ``.mpl`` files, standardises the result files that the
Maple files are expected to write, and parses those result files back into
SymPy for exact verification.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

import sympy as sp

import pde_common
import ch_common as _ch
from sigs.utils import ExpressionUtils

X, T = sp.symbols("x t")

_JACOBI_FUNCS = {"JacobiSN", "JacobiCN", "JacobiDN"}


@dataclass
class CandidateFeatures:
    candidate_id: int
    codes: list[int] = field(default_factory=list)
    widths: list[int] = field(default_factory=list)
    activation_names: tuple[str, ...] = field(default_factory=tuple)
    phase_types: tuple[str, ...] = field(default_factory=tuple)
    phase_max_degree: int | None = None
    has_xt_coupling: bool = False
    nesting_depth: int = 0
    jacobi_count: int = 0
    tree_nodes: int = 0
    count_ops: int = 0
    derivative_ops: int = 0
    derivative_timeout: bool = False
    structure_class: str = "unknown"
    complexity_grade: str = "simple"


def _safe_sympify(expr_str: str):
    """Parse one candidate string once; return None instead of raising."""
    try:
        std = ExpressionUtils.standardize_expression(expr_str)
        return sp.sympify(std, locals=_ch.SYMPY_LOCALS)
    except Exception:
        return None


def _activation_names(codes: Iterable[int]) -> tuple[str, ...]:
    return tuple(_ch.ACT_NAMES.get(int(c), f"code{c}") for c in codes)


def _has_xt_product(expr: sp.Expr) -> bool:
    """True when x and t multiply inside at least one term of the expression."""
    for node in sp.preorder_traversal(expr):
        if node.func is sp.Mul:
            syms = node.free_symbols
            if X in syms and T in syms:
                return True
    return False


def _nesting_depth(expr: sp.Expr) -> int:
    depth = 0

    def walk(node, current):
        nonlocal depth
        if isinstance(node, sp.Function) and node.func is not sp.Function:
            current += 1
            depth = max(depth, current)
        for arg in node.args:
            walk(arg, current)

    walk(expr, 0)
    return depth


def _phase_type(arg: sp.Expr) -> str:
    if any(atom.func.__name__ in _JACOBI_FUNCS for atom in arg.atoms(sp.Function)):
        return "jacobi"
    if arg.has(sp.sin, sp.cos, sp.tan, sp.sinh, sp.cosh, sp.exp, sp.tanh, sp.sech):
        return "mixed_transcendental"
    if arg.has(sp.Function):
        return "nested"
    try:
        numerator, denominator = sp.fraction(sp.together(arg))
        if denominator != 1 and (denominator.has(X) or denominator.has(T)):
            return "rational"
    except Exception:
        pass
    try:
        degree = sp.Poly(sp.expand(arg), X, T).total_degree()
        return f"polynomial_{degree}"
    except sp.PolynomialError:
        return "other"


def _phase_degree(arg: sp.Expr) -> int | None:
    try:
        return int(sp.Poly(sp.expand(arg), X, T).total_degree())
    except (sp.PolynomialError, TypeError, ValueError):
        return None


def analyze_candidate_structure(
    candidate_id: int,
    expr_str: str,
    codes: list[int] | None,
    widths: list[int],
    derivative_timeout: float = 2.0,
) -> CandidateFeatures:
    expr = _safe_sympify(expr_str)
    codes = list(codes or [])
    widths = list(widths or [1])
    if expr is None:
        return CandidateFeatures(candidate_id=candidate_id, codes=codes, widths=widths)

    phase_types: list[str] = []
    max_degree: int | None = None
    for atom in expr.atoms(sp.Function):
        if atom.func is sp.Function or len(atom.args) != 1:
            continue
        arg = atom.args[0]
        phase_types.append(_phase_type(arg))
        degree = _phase_degree(arg)
        if degree is not None and (max_degree is None or degree > max_degree):
            max_degree = degree

    def _derivative_measure():
        return int(sp.count_ops(sp.diff(expr, T, X, 2)))

    derivative_ops = 0
    derivative_timed_out = False
    measured, error = _ch._call_with_timeout(_derivative_measure, derivative_timeout)
    if error is not None:
        derivative_timed_out = True
    elif measured is not None:
        derivative_ops = int(measured)

    features = CandidateFeatures(
        candidate_id=candidate_id,
        codes=codes,
        widths=widths,
        activation_names=_activation_names(codes),
        phase_types=tuple(sorted(set(phase_types))) if phase_types else ("constant",),
        phase_max_degree=max_degree,
        has_xt_coupling=_has_xt_product(expr),
        nesting_depth=_nesting_depth(expr),
        jacobi_count=sum(
            1
            for atom in expr.atoms(sp.Function)
            if atom.func.__name__ in _JACOBI_FUNCS
        ),
        tree_nodes=len(list(sp.preorder_traversal(expr))),
        count_ops=int(sp.count_ops(expr)),
        derivative_ops=derivative_ops,
        derivative_timeout=derivative_timed_out,
    )
    features.structure_class = _structure_class(features)
    features.complexity_grade = grade_candidate(features)
    return features


def _structure_class(features: CandidateFeatures) -> str:
    phases = features.phase_types
    if any(p == "jacobi" for p in phases):
        return "jacobi"
    if any(p == "mixed_transcendental" for p in phases):
        return "mixed_transcendental"
    if any(p == "rational" for p in phases):
        return "rational"
    if any(p == "nested" for p in phases):
        return "nested"
    if any(p.startswith("polynomial_") for p in phases):
        degree = features.phase_max_degree or 0
        if features.has_xt_coupling:
            return f"coupled_poly_{degree}"
        return f"poly_{degree}"
    return "constant"


def grade_candidate(features: CandidateFeatures) -> str:
    """Grade a candidate for scheduling; no candidate is silently discarded."""
    if features.derivative_timeout:
        return "complex"
    if features.nesting_depth >= 4 or features.jacobi_count >= 2:
        return "complex"
    if features.derivative_ops >= 2000 or features.count_ops >= 180:
        return "complex"
    if features.nesting_depth >= 3 or features.derivative_ops >= 700:
        return "medium"
    if features.count_ops >= 90 or features.derivative_ops >= 350:
        return "medium"
    return "simple"


def candidate_structure_key(expr: sp.Expr, features: CandidateFeatures) -> str:
    """A coefficient-free structural key for duplicate filtering."""
    try:
        return sp.srepr(pde_common._canonical_branch_expr(expr, X, T))
    except Exception:
        return sp.srepr(expr)


def quick_check_bbm(expr_str: str, timeout: float = 3.0) -> dict:
    """Low-cost BBM derivative inspection before full Stage II.

    ``status`` is ok/timeout/unsupported/error.  A timeout is not treated as a
    no-solution verdict.
    """
    expr = _safe_sympify(expr_str)
    if expr is None:
        return {"status": "unsupported", "parts": {}, "message": "sympify failed"}

    parts = {}
    names = [
        ("u_t", lambda: sp.diff(expr, T)),
        ("u_x", lambda: sp.diff(expr, X)),
        ("u_u_x", lambda: expr * sp.diff(expr, X)),
        ("u_xxt", lambda: sp.diff(expr, T, X, 2)),
    ]
    aggregate = "ok"
    for name, call in names:
        started = time.time()
        value, error = _ch._call_with_timeout(
            lambda c=call: sp.count_ops(c()), timeout
        )
        elapsed = time.time() - started
        if error is not None:
            status = "timeout" if error == "timeout" else "error"
            parts[name] = {"status": status, "elapsed": elapsed, "message": str(error)}
            if aggregate == "ok":
                aggregate = status
        else:
            parts[name] = {"status": "ok", "elapsed": elapsed, "ops": int(value)}

    return {
        "status": aggregate,
        "parts": parts,
        "message": "derivatives constructed" if aggregate == "ok" else "derivative check limited",
    }


def sympy_to_maple(expr: sp.Expr) -> str:
    """Convert a SymPy expression to a conservative Maple expression string."""
    text = sp.sstr(expr)
    text = text.replace("**", "^")
    text = re.sub(r"\bpi\b", "Pi", text)
    text = re.sub(r"\bE\b", "exp(1)", text)
    return text


def maple_to_sympy(text: str):
    """Parse a Maple-written expression into SymPy."""
    text = text.strip()
    text = text.replace("^", "**")
    text = re.sub(r"\bPi\b", "pi", text)
    text = re.sub(r"\bexp\(1\)", "E", text)
    text = text.replace("ln(", "log(")
    return sp.sympify(text, locals=_ch.SYMPY_LOCALS)


def _maple_string(path: Path) -> str:
    return f'"{str(path)}"'


def _result_block(
    candidate_id: int,
    run_id: str,
    result_path: Path,
    status: str,
    *,
    notes: str = "",
    residual: sp.Expr | None = None,
    solutions: list[dict] | None = None,
) -> str:
    """Emit Maple code that writes a standard result file."""
    lines = [
        f"fd := fopen({_maple_string(result_path)}, WRITE, TEXT):",
        f"fprintf(fd, \"candidate_id=%d\\n\", {candidate_id}):",
        f"fprintf(fd, \"run_id=%s\\n\", \"{run_id}\"):",
        f"fprintf(fd, \"status=%s\\n\", \"{status}\"):",
    ]
    if notes:
        lines.append(f"fprintf(fd, \"notes=%s\\n\", \"{notes}\"):")
    if residual is not None:
        lines.append(f"fprintf(fd, \"residual=%a\\n\", {sympy_to_maple(residual)}):")
    if solutions:
        for index, solution in enumerate(solutions, start=1):
            lines.append(f"fprintf(fd, \"solution_index=%d\\n\", {index}):")
            if solution.get("expr") is not None:
                lines.append(
                    f"fprintf(fd, \"solution_expression=%a\\n\", {sympy_to_maple(solution['expr'])}):"
                )
            for equation in solution.get("constraints", []):
                lines.append(
                    f"fprintf(fd, \"constraint=%a\\n\", {sympy_to_maple(equation)}):"
                )
    lines.append("fclose(fd):")
    return "\n".join(lines)


def _activation_definitions(parameterized_expr: sp.Expr) -> list[str]:
    definitions = []
    funcs = {atom.func.__name__ for atom in parameterized_expr.atoms(sp.Function)}
    if "sech" in funcs:
        definitions.append("sech := z -> 1/cosh(z):")
    if _JACOBI_FUNCS & funcs:
        definitions.append("with(Jacobi):")
    return definitions


def write_maple_file(
    record: dict,
    result_path: Path,
    path_kind: str,
    sympy_result: dict | None,
    quick_result: dict,
    run_id: str,
) -> Path:
    """Write one standalone Maple file for a candidate."""
    candidate_id = record["candidate_id"]
    parameterized = record.get("parameterized_expr") or record["expr"]
    params = record.get("params", [])
    codes = record.get("codes", [])
    features = record.get("features")
    parameterized_sym = _safe_sympify(parameterized) or sp.sympify(parameterized)

    lines: list[str] = []
    lines.append(f"# BBM NNSCA candidate {candidate_id} (run {run_id})")
    lines.append(f"# export path: {path_kind}")
    lines.append(f"# codes: {codes}")
    if features is not None:
        lines.append(f"# structure_class: {features.structure_class}")
        lines.append(f"# complexity_grade: {features.complexity_grade}")
    lines.append("restart;")
    lines.extend(_activation_definitions(parameterized_sym))
    if params:
        param_names = ", ".join("'" + str(p) + "'" for p in params)
        lines.append(f"unassign({param_names}):")
    lines.append(f"u := {sympy_to_maple(parameterized_sym)};")
    lines.append("eq := diff(u, t) + diff(u, x) + u*diff(u, x) - diff(u, t, x, x) = 0;")
    lines.append("res := diff(u, t) + diff(u, x) + u*diff(u, x) - diff(u, t, x, x);")

    if path_kind == "A":
        equations = (sympy_result or {}).get("coefficient_equations") or []
        known = (sympy_result or {}).get("known_constraints") or {}
        if known:
            lines.append("# known constraints:")
            for sym, value in known.items():
                lines.append(f"#   {sp.sstr(sym)} = {sp.sstr(value)}")
        if equations:
            lines.append("# coefficient equations extracted by Python/SymPy:")
            eq_names = []
            for index, equation in enumerate(equations, start=1):
                name = f"eq{index}"
                lines.append(f"{name} := {sympy_to_maple(equation)} = 0;")
                eq_names.append(name)
            eq_set = ", ".join(eq_names)
            param_set = ", ".join(str(p) for p in params)
            if param_set:
                lines.append(f"sol := solve({{{eq_set}}}, {{{param_set}}});")
            else:
                lines.append(f"sol := solve({{{eq_set}}});")
            lines.append("sols := [sol]:")
            lines.append("if sol = NULL then")
            lines.append("  status := \"no_solution\":")
            lines.append("else")
            lines.append("  if nops(sol) > 0 and type(op(1, sol), set) then")
            lines.append("    sols := [op(sol)]:")
            lines.append("  end if:")
            lines.append("  status := \"solved\":")
            lines.append("end if:")
            lines.append("fd := fopen(" + _maple_string(result_path) + ", WRITE, TEXT):")
            lines.append(f"fprintf(fd, \"candidate_id=%d\\n\", {candidate_id}):")
            lines.append(f"fprintf(fd, \"run_id=%s\\n\", \"{run_id}\"):")
            lines.append("fprintf(fd, \"status=%s\\n\", status):")
            lines.append("if status = \"solved\" then")
            lines.append("  for i from 1 to nops(sols) do")
            lines.append("    s := sols[i]:")
            lines.append("    fprintf(fd, \"solution_index=%d\\n\", i):")
            lines.append("    fprintf(fd, \"solution_expression=%a\\n\", subs(s, u)):")
            lines.append("    for eqx in [op(s)] do")
            lines.append("      if type(eqx, equation) then")
            lines.append("        fprintf(fd, \"constraint=%a\\n\", eqx):")
            lines.append("      end if:")
            lines.append("    end do:")
            lines.append("  end do:")
            lines.append("end if:")
            lines.append("fclose(fd):")
        else:
            lines.append("# No coefficient equations were available.")
            lines.append(_result_block(
                candidate_id, run_id, result_path, "unsolved",
                notes="path A no equations",
            ))
    elif path_kind == "B":
        residual = (sympy_result or {}).get("residual")
        lines.append("# SymPy constructed a residual but coefficient extraction was limited.")
        if residual is not None:
            lines.append(f"res := {sympy_to_maple(residual)};")
        lines.append("res_simp := simplify(res);")
        lines.append(_result_block(
            candidate_id, run_id, result_path, "unsolved",
            notes="path B manual coefficient extraction",
            residual=residual,
        ))
    else:
        lines.append("# SymPy could not construct the residual; Maple must differentiate u.")
        lines.append("res := simplify(diff(u, t) + diff(u, x) + u*diff(u, x) - diff(u, t, x, x));")
        lines.append(_result_block(
            candidate_id, run_id, result_path, "unsolved",
            notes="path C independent derivative task",
        ))

    out_path = record["maple_pending_path"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def write_manifest(records: Iterable[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = []
    for record in records:
        item = {
            "candidate_id": record["candidate_id"],
            "expr": record["expr"],
            "parameterized_expr": record.get("parameterized_expr"),
            "codes": record.get("codes"),
            "widths": record.get("widths"),
            "group": record.get("group"),
            "rank": record.get("rank"),
            "path_kind": record.get("path_kind"),
        }
        features = record.get("features")
        if features is not None:
            item["features"] = asdict(features)
        payload.append(item)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_manifest(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_result_text(path: Path) -> dict:
    """Parse a result file written by a generated Maple script."""
    result: dict = {}
    constraints: list[str] = []
    solutions: list[dict] = []
    current_index = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key == "constraint" and current_index is not None:
            solutions[-1]["constraints"].append(value)
        elif key == "constraint":
            constraints.append(value)
        elif key == "solution_index":
            current_index = int(value)
            solutions.append({"index": int(value), "constraints": [], "expr": None})
        elif key == "solution_expression" and current_index is not None:
            solutions[-1]["expr"] = value
        else:
            result[key] = value
    if constraints:
        result["constraints"] = constraints
    if solutions:
        result["solutions"] = solutions
    if "candidate_id" in result:
        try:
            result["candidate_id"] = int(result["candidate_id"])
        except ValueError:
            pass
    return result
