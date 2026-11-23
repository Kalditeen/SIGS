"""Adapter from compiled NNSCA candidates to the existing Stage2 engine.

Stage2 keeps ownership of symbolic constraint extraction, solving, and raw PDE
residual verification.  This module only adapts the new expression/parameter
interface to those existing helpers; it does not reimplement them.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from dataclasses import dataclass

import sympy as sp

REPO_ROOT = Path(__file__).resolve().parents[2]
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
SRC_DIR = REPO_ROOT / "src"
for path in (PDES_DIR, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import sfg_bbm_21 as sfg  # noqa: E402

X, T = sfg.X, sfg.T

@dataclass
class Stage2Input:
    pde: object
    expression: sp.Expr
    unknown_parameters: list[sp.Symbol]
    parameter_roles: dict
    candidate_id: str
    network_structure: dict | None = None

def _has_imaginary_value(value: sp.Expr) -> bool:
    try:
        if value.is_number and sp.im(value) != 0:
            return True
    except Exception:
        pass
    return value.has(sp.I)


def _clean_solution(solution) -> dict[sp.Symbol, sp.Expr]:
    return {
        symbol: value
        for symbol, value in solution.items()
        if symbol.is_Symbol
    }


def _is_x_t_dependent(expression: sp.Expr) -> bool:
    if not ({X, T} & expression.free_symbols):
        return False
    try:
        if sp.expand(sp.diff(expression, X)) == 0 and sp.expand(sp.diff(expression, T)) == 0:
            return False
    except Exception:
        pass
    return True


class Stage2Adapter:
    """Run one compiled ansatz through the existing symbolic Stage2 pipeline."""

    def process(
        self,
        expression: sp.Expr,
        residual_fn,
        config: dict,
        pde_equation: str = "pde=residual(u)=0",
        reduce_fn=None,
    ) -> dict:
        record: dict = {
            "symbolic_status": "success",
            "constraint_status": "skipped",
            "extraction_status": "skipped",
            "solve_status": "skipped",
            "verification_status": "skipped",
            "exact_solutions": [],
            "solutions": [],
            "branch_attempts": [],
            "nontrivial_status": "skipped",
            "substitution_status": "skipped",
            "identity_verification_status": "skipped",
            "failure_reason": None,
            "timing": {},
        }

        residual_start = time.perf_counter()
        residual, residual_error = sfg._call_with_timeout(
            lambda: residual_fn(expression),
            float(config["solver"].get("residual_timeout", config["solver"]["verify_timeout"])),
        )
        record["timing"]["residual"] = time.perf_counter() - residual_start
        if residual_error is not None:
            status = "timeout" if residual_error == "timeout" else "unsupported"
            record["constraint_status"] = status
            record["extraction_status"] = status
            record["verification_status"] = "SYMBOLIC_UNRESOLVED"
            record["failure_reason"] = f"PDE residual computation {residual_error}"
            return record

        extraction_residual = residual
        record["residual"] = sp.sstr(residual)
        record["reduction_status"] = "skipped"
        if reduce_fn is not None:
            try:
                extraction_residual, reduction_meta = reduce_fn(residual)
                record["reduction_status"] = reduction_meta.get("status", "unknown")
            except Exception:
                pass

        if residual == 0:
            record["constraint_status"] = "success"
            record["extraction_status"] = "success"
            record["solve_status"] = "success"
            if _is_x_t_dependent(expression):
                record["verification_status"] = "EXACT_VERIFIED"
                record["exact_solutions"] = [{
                    "expression": sp.sstr(expression),
                    "constraints": {},
                    "residual": "0",
                }]
            else:
                record["verification_status"] = "FAILED"
                record["failure_reason"] = "residual is zero but trial is x,t-independent"
            return record

        extraction_start = time.perf_counter()
        extraction, extract_error = sfg._call_with_timeout(
            lambda: sfg._extract_coefficient_equations(extraction_residual, X, T),
            float(config["solver"]["extract_timeout"]),
        )
        equations, _basis, inner_error = ([], [], None) if extraction is None else extraction
        record["timing"]["extraction"] = time.perf_counter() - extraction_start
        if extract_error is None:
            extract_error = inner_error
        if extract_error is not None:
            status = "timeout" if extract_error == "timeout" else "unsupported"
            record["constraint_status"] = status
            record["extraction_status"] = status
            record["verification_status"] = "SYMBOLIC_UNRESOLVED"
            record["failure_reason"] = f"coefficient extraction {extract_error}"
            return record

        record["constraint_status"] = "success"
        record["extraction_status"] = "success"
        record["coefficient_equations"] = [sp.sstr(eq) for eq in equations]

        unknowns = sorted(
            [symbol for symbol in expression.free_symbols if symbol not in (X, T)],
            key=lambda symbol: str(symbol),
        )
        solve_start = time.perf_counter()
        raw_solutions, solve_error = sfg._solve_equations(
            equations, unknowns, float(config["solver"]["solve_timeout"])
        )
        record["timing"]["solve"] = time.perf_counter() - solve_start
        if solve_error is not None:
            status = "timeout" if solve_error == "timeout" else "unsupported"
            record["solve_status"] = status
            record["verification_status"] = "SYMBOLIC_UNRESOLVED"
            record["failure_reason"] = f"coefficient solve {solve_error}"
            return record

        record["solve_status"] = "success"
        solutions = sfg._sympy_solution_dicts(raw_solutions)
        record["sympy_solutions"] = [sfg._serialize_solution(sol) for sol in solutions]
        if not solutions:
            record["nontrivial_status"] = "NO_SOLUTION"
            record["substitution_status"] = "skipped"
            record["identity_verification_status"] = "skipped"
            record["verification_status"] = "NO_SOLUTION"
            record["failure_reason"] = "coefficient system has no nontrivial solution"
            return record

        verified = []
        seen = set()
        for solution in solutions[:600]:
            clean = _clean_solution(solution)
            if any(_has_imaginary_value(value) for value in clean.values()):
                record["branch_attempts"].append({
                    "solution": sfg._serialize_solution(solution),
                    "substitution_status": "skipped",
                    "nontrivial_status": "DOMAIN_INVALID",
                    "identity_verification_status": "skipped",
                })
                continue
            try:
                substituted = sp.expand(expression.subs(clean))
                substitution_status = "success"
            except Exception as exc:
                record["branch_attempts"].append({
                    "solution": sfg._serialize_solution(solution),
                    "substitution_status": f"failed: {type(exc).__name__}: {exc}",
                    "nontrivial_status": "UNRESOLVED",
                    "identity_verification_status": "skipped",
                })
                continue

            identity_status = "skipped"
            if _is_x_t_dependent(substituted):
                try:
                    residual_sub = sp.expand(residual_fn(substituted))
                    identity_status = (
                        "verified"
                        if sfg._residual_is_zero(residual_sub)
                        else "not_verified"
                    )
                except Exception as exc:
                    identity_status = f"error: {type(exc).__name__}: {exc}"
            else:
                identity_status = "trivial_or_constant"

            record["branch_attempts"].append({
                "solution": sfg._serialize_solution(solution),
                "substitution_status": substitution_status,
                "nontrivial_status": (
                    "NONTRIVIAL"
                    if _is_x_t_dependent(substituted)
                    else "CONSTANT_TRIVIAL"
                ),
                "identity_verification_status": identity_status,
            })

            if identity_status != "verified":
                continue
            key = sp.srepr(sp.expand(substituted))
            if key in seen:
                continue
            seen.add(key)
            verified.append({
                "expression": sp.sstr(substituted),
                "constraints": sfg._serialize_solution(clean),
                "residual": "0",
            })

        if verified:
            record["verification_status"] = "EXACT_VERIFIED"
            record["exact_solutions"] = verified
            record["solutions"] = verified
            record["nontrivial_status"] = "NONTRIVIAL"
            record["substitution_status"] = "success"
            record["identity_verification_status"] = "verified"
        else:
            record["verification_status"] = "FAILED"
            record["nontrivial_status"] = "NONE"
            record["substitution_status"] = "success"
            record["identity_verification_status"] = "not_verified"
            record["failure_reason"] = (
                "solver produced branches but none passed independent "
                "back-substitution verification"
            )
        return record
