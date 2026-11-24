"""Grouping validator fault-injection tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import sympy as sp  # noqa: E402

from src.ch_equation import Q1, Q2, Q3, A1, A2, A3  # noqa: E402
from src.grouping_validator import validate_grouping  # noqa: E402
from src.term_serializer import serialize_terms  # noqa: E402


def _fixture():
    residual = A1 * Q1 + A2 * Q1 + A3 * Q2
    payload = serialize_terms(residual)
    valid = {
        "groups": [
            {"monomial": {"x": 0, "t": 0, "q1": 1, "q2": 0, "q3": 0}, "term_ids": [0, 1]},
            {"monomial": {"x": 0, "t": 0, "q1": 0, "q2": 1, "q3": 0}, "term_ids": [2]},
        ],
        "unassigned_term_ids": [],
        "notes": [],
    }
    return residual, payload, valid


def test_valid_grouping_passes() -> None:
    residual, payload, valid = _fixture()
    result = validate_grouping(valid, payload, residual)
    assert result["ok"] is True
    assert len(result["groups"]) == 2


def test_missing_term_rejected() -> None:
    residual, payload, valid = _fixture()
    valid["groups"][0]["term_ids"] = [0]
    result = validate_grouping(valid, payload, residual)
    assert result["ok"] is False
    assert any("do not match" in error for error in result["errors"])


def test_duplicate_term_rejected() -> None:
    residual, payload, valid = _fixture()
    valid["groups"][0]["term_ids"] = [0, 1]
    valid["groups"][1]["term_ids"] = [2, 2]
    result = validate_grouping(valid, payload, residual)
    assert result["ok"] is False
    assert any("duplicate" in error for error in result["errors"])


def test_unknown_term_rejected() -> None:
    residual, payload, valid = _fixture()
    valid["groups"][0]["term_ids"] = [0, 99]
    result = validate_grouping(valid, payload, residual)
    assert result["ok"] is False
    assert any("unknown term id" in error for error in result["errors"])


def test_wrong_monomial_rejected() -> None:
    residual, payload, valid = _fixture()
    valid["groups"][1]["monomial"]["q1"] = 1
    valid["groups"][1]["monomial"]["q2"] = 0
    result = validate_grouping(valid, payload, residual)
    assert result["ok"] is False
    assert any("actual monomial" in error for error in result["errors"])
