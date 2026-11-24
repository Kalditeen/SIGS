"""Coefficient extraction tests using SymPy-derived coefficients only."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import sympy as sp  # noqa: E402

from src.ch_equation import A1, A2, Q1, Q2  # noqa: E402
from src.coefficient_extractor import extract_coefficient_equations  # noqa: E402
from src.term_serializer import serialize_terms  # noqa: E402


def test_extract_summed_coefficient_equations() -> None:
    residual = A1 * Q1 + A2 * Q1 + sp.Symbol("A3") * Q2
    payload = serialize_terms(residual)
    groups = [
        {"monomial": {"x": 0, "t": 0, "q1": 1, "q2": 0, "q3": 0}, "term_ids": [0, 1]},
        {"monomial": {"x": 0, "t": 0, "q1": 0, "q2": 1, "q3": 0}, "term_ids": [2]},
    ]
    equations = extract_coefficient_equations(groups, payload)
    parsed = {item["equation"] for item in equations}
    assert "A1 + A2 = 0" in parsed or "-A1 - A2 = 0" in parsed
    assert "A3 = 0" in parsed or "-A3 = 0" in parsed


def test_extracted_coefficients_have_no_generators() -> None:
    residual = (sp.Symbol("A1") + sp.Symbol("A2")) * Q1
    payload = serialize_terms(residual)
    groups = [
        {"monomial": {"x": 0, "t": 0, "q1": 1, "q2": 0, "q3": 0}, "term_ids": [0, 1]},
    ]
    equations = extract_coefficient_equations(groups, payload)
    coefficient = sp.sympify(equations[0]["coefficient"])
    assert not ({Q1, Q2} & coefficient.free_symbols)
