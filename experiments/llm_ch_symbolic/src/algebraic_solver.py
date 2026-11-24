"""Solve the SymPy-derived coefficient equations without injecting Maple data."""

from __future__ import annotations

import sympy as sp

from . import ch_equation as ce

UNKNOWNS = [
    ce.K,
    ce.B4,
    ce.A1,
    ce.A2,
    ce.A3,
    ce.WT1,
    ce.WT2,
    ce.WT3,
    ce.WX1,
    ce.WX2,
    ce.WX3,
]

def _as_zero_expr(equation_string: str) -> sp.Expr:
    if " = " in equation_string:
        lhs, rhs = equation_string.rsplit(" = ", 1)
        return sp.expand(sp.sympify(lhs) - sp.sympify(rhs))
    return sp.expand(sp.sympify(equation_string))

as_zero_expr = _as_zero_expr

def _classification(solution: dict[sp.Symbol, sp.Expr]) -> str:
    def value(symbol):
        return sp.expand(solution.get(symbol, sp.Symbol(str(symbol))))

    amplitudes = [value(ce.A1), value(ce.A2), value(ce.A3)]
    if all(item == 0 for item in amplitudes):
        return "ZERO"
    if any(item == 0 for item in amplitudes):
        return "DEGENERATE"
    return "NONDEGENERATE"


def _solution_dicts(raw) -> list[dict[sp.Symbol, sp.Expr]]:
    if raw is None:
        return []
    if isinstance(raw, dict):
        return [{key: value for key, value in raw.items() if key in UNKNOWNS}]
    if isinstance(raw, (list, tuple)):
        return [item for item in raw if isinstance(item, dict)]
    if isinstance(raw, sp.FiniteSet):
        result = []
        for item in raw:
            if isinstance(item, dict):
                result.append(item)
            elif isinstance(item, tuple) and len(item) == len(UNKNOWNS):
                result.append(dict(zip(UNKNOWNS, item)))
        return result
    return []


def _serialize(raw) -> str:
    try:
        if raw is None:
            return "None"
        if isinstance(raw, dict):
            return {str(key): sp.sstr(value) for key, value in raw.items()}
        if isinstance(raw, sp.FiniteSet):
            return sp.sstr(raw)
        return sp.sstr(sp.Tuple(*raw)) if isinstance(raw, (list, tuple)) else sp.sstr(raw)
    except Exception as exc:  # noqa: BLE001
        return f"serialization failed: {type(exc).__name__}: {exc}"


def solve_system(equation_strings: list[str]) -> dict:
    equations = [_as_zero_expr(equation) for equation in equation_strings]

    result: dict = {
        "equations": equation_strings,
        "unknowns": [str(symbol) for symbol in UNKNOWNS],
        "solve_status": "attempted",
        "raw_result": None,
        "branches": [],
        "error": None,
    }

    try:
        raw = sp.solve(equations, UNKNOWNS, dict=True, simplify=False)
        result["raw_result"] = raw
        branches = _solution_dicts(raw)
        if not branches:
            raise ValueError("sp.solve returned no dictionary branches")
    except Exception as solve_exc:  # noqa: BLE001
        result["solve_status"] = "solve_failed_then_nonlinsolve"
        result["error"] = f"sp.solve: {type(solve_exc).__name__}: {solve_exc}"
        try:
            raw_set = sp.nonlinsolve(equations, UNKNOWNS)
            result["raw_result"] = raw_set
            branches = _solution_dicts(raw_set)
        except Exception as nonlin_exc:  # noqa: BLE001
            result["solve_status"] = "failed"
            result["error"] += f"; nonlinsolve: {type(nonlin_exc).__name__}: {nonlin_exc}"
            result["raw_result"] = None
            return result

    if not branches:
        result["solve_status"] = "no_dictionary_branch"
        result["raw_result"] = _serialize(result.get("raw_result"))
        return result

    serialized_branches = []
    for index, branch in enumerate(branches):
        clean = {key: value for key, value in branch.items() if key in UNKNOWNS}
        serialized_branches.append({
            "index": index,
            "classification": _classification(clean),
            "values": {str(key): sp.sstr(sp.expand(value)) for key, value in clean.items()},
        })
    result["solve_status"] = "success"
    result["branches"] = serialized_branches
    result["raw_result"] = _serialize(result.get("raw_result"))
    return result
