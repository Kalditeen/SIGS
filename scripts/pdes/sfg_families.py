#!/usr/bin/env python3
"""Family-aware SFG candidate generation for Gardner phase 3.

The original random generator remains unchanged in ``sfg_bbm_21.py``.  This
module adds explicit elementary, hyperbolic, and Jacobi family streams plus a
quota-preserving mixed stream.  The JacobiCN benchmark function is an ordinary
member of the Jacobi family stream; it is not injected into the default or
mixed random streams.
"""

from __future__ import annotations

import random
import sympy as sp
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PDES_DIR = REPO_ROOT / "scripts" / "pdes"
if str(PDES_DIR) not in sys.path:
    sys.path.insert(0, str(PDES_DIR))

import sfg_bbm_21 as sfg  # noqa: E402

FAMILY_DEFS = {
    "elementary": {
        "label": "elementary",
        "atoms": [
            "z",
            "z**2",
            "z**3",
            "z**4",
            "exp(z)",
            "sin(z)",
            "cos(z)",
            "log(z)",
            "z + 1",
            "z - 1",
        ],
    },
    "hyperbolic": {
        "label": "hyperbolic",
        "atoms": [
            "sinh(z)",
            "cosh(z)",
            "tanh(z)",
            "sech(z)",
            "csch(z)",
            "coth(z)",
            "tanh(z)**2",
            "sech(z)**2",
        ],
    },
    "jacobi": {
        "label": "jacobi",
        "atoms": [
            "JacobiSN(z,m)",
            "JacobiCN(z,m)",
            "JacobiDN(z,m)",
            "JacobiSN(z,m)**2",
            "JacobiCN(z,m)**2",
            "JacobiDN(z,m)**2",
        ],
    },
}


def _slug(expr: str) -> str:
    return (
        expr.replace("**", "pow")
        .replace("(", "_")
        .replace(")", "_")
        .replace(",", "_")
        .replace("*", "_")
        .replace(" ", "")
    )[:40]


def _make_candidate(expr_str: str, family: str, rule: str) -> sfg.Candidate:
    parsed = sfg._sympify_f(expr_str)
    return sfg._candidate_from_expr(
        _slug(expr_str),
        parsed,
        source_type="generated",
        generation_rule=f"family:{family}:{rule}",
        family=family,
    )


def _family_entries(family: str, count: int, seed: int) -> list[tuple[str, str]]:
    atoms = FAMILY_DEFS[family]["atoms"]
    entries: list[tuple[str, str]] = []
    for expr in atoms[: max(0, count)]:
        entries.append((expr, "atom"))

    rng = random.Random(seed)
    attempts = 0
    while len(entries) < count and attempts < count * 40:
        attempts += 1
        left = rng.choice(atoms)
        right = rng.choice(atoms)
        op = rng.choice(("add", "mul", "pow2", "compose"))
        try:
            if op == "add":
                expr = f"{left} + {right}"
            elif op == "mul":
                expr = f"{left} * {right}"
            elif op == "pow2":
                expr = f"({left})**2"
            else:
                if family == "hyperbolic":
                    expr = f"tanh({left})"
                elif family == "jacobi":
                    expr = f"JacobiSN({left}, m)"
                else:
                    expr = f"sin({left})"
            parsed = sfg._sympify_f(expr)
        except Exception:
            continue
        if sfg._function_depth(parsed) > 3 or sfg._node_count(parsed) > 12:
            continue
        if len(sfg._free_parameters(parsed)) > 2:
            continue
        entries.append((expr, op))
    return entries[:count]


def generate_family_candidates(family: str, count: int, seed: int = 101) -> list[sfg.Candidate]:
    if family not in FAMILY_DEFS:
        raise ValueError(f"unknown family: {family}")
    candidates = []
    seen = set()
    for expr, rule in _family_entries(family, count, seed):
        candidate = _make_candidate(expr, family, rule)
        key = sp.srepr(sfg._sympify_f(candidate.expression))
        if key in seen:
            candidate.duplicate_status = "duplicate"
        else:
            seen.add(key)
        candidates.append(candidate)
    return candidates


def generate_mixed_family_candidates(
    count: int,
    seed: int = 101,
    quotas: dict[str, int] | None = None,
) -> list[sfg.Candidate]:
    families = list(FAMILY_DEFS)
    if quotas is None:
        base, remainder = divmod(count, len(families))
        quotas = {family: base + (1 if index < remainder else 0) for index, family in enumerate(families)}
    candidates: list[sfg.Candidate] = []
    for family, family_count in quotas.items():
        if family_count <= 0:
            continue
        candidates.extend(generate_family_candidates(family, family_count, seed=seed + len(families)))
    # Rotate by a deterministic shuffle so the output is mixed rather than grouped.
    rng = random.Random(seed)
    rng.shuffle(candidates)
    return candidates


def generate_original_random_candidates(count: int, seed: int = 101) -> list[sfg.Candidate]:
    config = dict(sfg.DEFAULT_CONFIG["generator"])
    config["mode"] = "random"
    config["include_seeds"] = False
    config["random_seed"] = seed
    config["max_candidates"] = count
    return sfg.generate_candidates(config)


def family_signature(expr) -> set[str]:
    """Return the set of function families actually present in an expression."""
    text = sp.sstr(expr) if not isinstance(expr, str) else expr
    families = set()
    for marker in ("JacobiSN", "JacobiCN", "JacobiDN"):
        if marker in text:
            families.add("jacobi")
    for marker in ("sinh", "cosh", "tanh", "sech", "csch", "coth"):
        if marker in text:
            families.add("hyperbolic")
    for marker in ("exp", "log", "sin(", "cos(", "tan("):
        if marker in text:
            families.add("elementary")
    if "z" in text and not families:
        families.add("elementary")
    return families


def is_true_mixed_candidate(candidate: sfg.Candidate) -> bool:
    """True only when a single candidate combines at least two families."""
    return len(family_signature(candidate.expression)) >= 2
