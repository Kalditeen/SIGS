"""Deterministic validation of an LLM grouping before any solving happens."""

from __future__ import annotations

import sympy as sp

from . import ch_equation as ce
from .term_serializer import term_by_id

EXPECTED_KEYS = {"x", "t", "q1", "q2", "q3"}


def _term_monomial(expr: sp.Expr) -> dict[str, int]:
    """Return integer generator exponents for one expanded additive term."""
    expr = sp.expand(expr)
    try:
        poly = sp.Poly(expr, ce.X, ce.T, ce.Q1, ce.Q2, ce.Q3)
    except sp.PolynomialError as exc:
        raise ValueError(
            f"term is not polynomial in the formal generators: {sp.sstr(expr)}: {exc}"
        ) from exc
    if not poly.terms():
        return {key: 0 for key in EXPECTED_KEYS}
    if len(poly.terms()) != 1:
        raise ValueError(
            f"term is not a single formal monomial: {sp.sstr(expr)}"
        )
    exponents = poly.terms()[0][0]
    return {
        "x": int(exponents[0]),
        "t": int(exponents[1]),
        "q1": int(exponents[2]),
        "q2": int(exponents[3]),
        "q3": int(exponents[4]),
    }


def _all_term_ids(grouping: dict) -> list[int]:
    term_ids: list[int] = []
    for group in grouping.get("groups", []):
        for value in group.get("term_ids", []):
            if isinstance(value, int) and not isinstance(value, bool):
                term_ids.append(value)
    for value in grouping.get("unassigned_term_ids", []):
        if isinstance(value, int) and not isinstance(value, bool):
            term_ids.append(value)
    return term_ids


def validate_grouping(grouping: dict, payload: dict, residual_formal: sp.Expr) -> dict:
    """Validate an LLM grouping and return normalized groups if valid."""
    errors: list[str] = []
    if not isinstance(grouping, dict):
        return {"ok": False, "errors": ["grouping is not a JSON object"], "groups": []}

    groups = grouping.get("groups")
    if not isinstance(groups, list):
        return {"ok": False, "errors": ["missing or invalid 'groups' list"], "groups": []}
    if not isinstance(grouping.get("unassigned_term_ids"), list):
        errors.append("missing or invalid 'unassigned_term_ids' list")
    if not isinstance(grouping.get("notes"), list):
        errors.append("missing or invalid 'notes' list")

    known_ids = set(term_by_id(payload).keys())
    assigned_ids: list[int] = []
    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            errors.append(f"group {index} is not an object")
            continue
        monomial = group.get("monomial")
        if not isinstance(monomial, dict):
            errors.append(f"group {index} has missing 'monomial' object")
            continue
        if set(monomial) != EXPECTED_KEYS:
            errors.append(f"group {index} monomial keys must be exactly {sorted(EXPECTED_KEYS)}")
        for key, value in monomial.items():
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                errors.append(f"group {index} monomial[{key!r}] is not a non-negative integer")
        term_ids = group.get("term_ids")
        if not isinstance(term_ids, list):
            errors.append(f"group {index} has missing 'term_ids' list")
            continue
        for term_id in term_ids:
            if isinstance(term_id, bool) or not isinstance(term_id, int):
                errors.append(f"group {index} contains non-integer term id {term_id!r}")
                continue
            if term_id not in known_ids:
                errors.append(f"group {index} references unknown term id {term_id}")
                continue
            assigned_ids.append(term_id)
            try:
                actual = _term_monomial(term_by_id(payload)[term_id])
            except Exception as exc:  # noqa: BLE001
                errors.append(f"term {term_id} monomial extraction failed: {exc}")
                continue
            expected = {key: int(value) for key, value in monomial.items()} if isinstance(monomial, dict) else {}
            if actual != expected:
                errors.append(
                    f"term {term_id} actual monomial {actual} != group monomial {expected}"
                )

    all_ids = _all_term_ids(grouping)
    if sorted(all_ids) != sorted(known_ids):
        errors.append("assigned/unassigned term ids do not match the serialized terms exactly")
    if len(all_ids) != len(set(all_ids)):
        errors.append("duplicate term ids found")

    normalized_groups = []
    if not errors:
        terms_by_id = term_by_id(payload)
        for group in groups:
            monomial = {
                key: int(value) for key, value in group["monomial"].items()
            }
            normalized_groups.append({
                "monomial": monomial,
                "term_ids": [int(value) for value in group["term_ids"]],
            })
        reconstructed = sp.expand(
            sum(terms_by_id[term_id] for term_id in assigned_ids)
        )
        if sp.expand(reconstructed - sp.expand(residual_formal)) != 0:
            errors.append("grouped terms do not reconstruct the original residual")

    return {
        "ok": not errors,
        "errors": errors,
        "groups": normalized_groups if not errors else [],
    }
