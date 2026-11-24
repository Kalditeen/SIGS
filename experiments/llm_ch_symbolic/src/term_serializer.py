"""Serialize an expanded formal residual into reviewable additive terms."""

from __future__ import annotations

import json

import sympy as sp

from . import ch_equation as ce

GENERATORS = ["x", "t", "q1", "q2", "q3"]


def _term_exprs(residual: sp.Expr) -> list[sp.Expr]:
    expanded = sp.expand(residual)
    if expanded == 0:
        return []
    terms = [term for term in sp.Add.make_args(expanded)]
    terms.sort(key=lambda term: sp.srepr(term))
    return terms


def serialize_terms(residual: sp.Expr) -> dict:
    """Return the LLM input payload without performing any grouping."""
    terms = _term_exprs(residual)
    return {
        "generators": GENERATORS,
        "terms": [
            {
                "id": index,
                "expression": sp.sstr(term),
            }
            for index, term in enumerate(terms)
        ],
    }


def serialize_terms_json(residual: sp.Expr, indent: int = 2) -> str:
    return json.dumps(serialize_terms(residual), indent=indent, ensure_ascii=False)


def parse_serialized_terms(payload: dict) -> list[sp.Expr]:
    """Convert serialized term strings back to exact SymPy expressions."""
    terms = payload.get("terms", [])
    return [sp.sympify(item["expression"]) for item in terms]


def term_by_id(payload: dict) -> dict[int, sp.Expr]:
    """Return an id -> exact expression map for validation and extraction."""
    return {
        int(item["id"]): sp.sympify(item["expression"])
        for item in payload.get("terms", [])
    }
