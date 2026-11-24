"""Extract exact coefficient equations from validated LLM groups.

All coefficients come from SymPy, never from the LLM output.
"""

from __future__ import annotations

import sympy as sp

from . import ch_equation as ce
from .term_serializer import term_by_id


def extract_coefficient_equations(
    validated_groups: list[dict],
    payload: dict,
) -> list[dict]:
    terms_by_id = term_by_id(payload)
    equations: list[dict] = []
    for index, group in enumerate(validated_groups):
        monomial = group["monomial"]
        exponents = (
            int(monomial["x"]),
            int(monomial["t"]),
            int(monomial["q1"]),
            int(monomial["q2"]),
            int(monomial["q3"]),
        )
        grouped_sum = sp.expand(
            sum(terms_by_id[term_id] for term_id in group["term_ids"])
        )
        try:
            poly = sp.Poly(
                grouped_sum, ce.X, ce.T, ce.Q1, ce.Q2, ce.Q3
            )
            coefficient = sp.expand(poly.coeff_monomial(exponents))
        except sp.PolynomialError as exc:
            coefficient = sp.sympify(0)
            equations.append({
                "group": index,
                "monomial": monomial,
                "coefficient": None,
                "equation": None,
                "error": f"coefficient extraction failed: {exc}",
            })
            continue

        # The formal-generator independence condition gives the sufficient
        # constraint coefficient == 0; it is not claimed to be necessary.
        equation = sp.expand(coefficient)
        if any(symbol in equation.free_symbols for symbol in (ce.X, ce.T, ce.Q1, ce.Q2, ce.Q3)):
            equations.append({
                "group": index,
                "monomial": monomial,
                "coefficient": sp.sstr(coefficient),
                "equation": None,
                "error": "extracted coefficient still contains formal generators",
            })
            continue

        equations.append({
            "group": index,
            "monomial": monomial,
            "coefficient": sp.sstr(coefficient),
            "equation": f"{sp.sstr(equation)} = 0",
        })
    return equations
