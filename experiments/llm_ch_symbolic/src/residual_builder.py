"""Construct and compare original and formal CH residuals."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from . import ch_equation as ce


@dataclass
class ResidualSet:
    original: sp.Expr
    formal: sp.Expr
    formal_consistency: bool
    formal_consistency_error: str | None = None


def _formal_derivative(expr: sp.Expr, weights: tuple[sp.Expr, ...]) -> sp.Expr:
    """Differentiate a polynomial in q1,q2,q3 with D q_i = weight_i q_i.

    This operator is intentionally independent of SymPy's ``diff`` for q_i, so
    the formal residual is built by a different route from the exponential
    residual.  Non-polynomial input raises ``PolynomialError`` rather than
    returning a silent wrong answer.
    """
    expr = sp.expand(expr)
    poly = sp.Poly(expr, ce.Q1, ce.Q2, ce.Q3)
    terms: list[sp.Expr] = []
    for monomial, coefficient in poly.terms():
        exponents = tuple(int(value) for value in monomial)
        derivative_factor = sum(
            sp.expand(weights[index] * exponents[index])
            for index in range(3)
        )
        if derivative_factor == 0:
            continue
        monomial_expr = sp.expand(coefficient * derivative_factor)
        for q, exponent in zip(ce.Q, exponents):
            if exponent:
                monomial_expr *= q**exponent
        terms.append(sp.expand(monomial_expr))
    return sp.Add(*terms) if terms else sp.Integer(0)


def formal_residual_from_trial(trial_formal: sp.Expr) -> sp.Expr:
    """Compute the CH residual for ``b4 + A1*q1 + A2*q2 + A3*q3``."""
    u = trial_formal
    u_x = _formal_derivative(u, ce.WX)
    u_xx = _formal_derivative(u_x, ce.WX)
    u_xxx = _formal_derivative(u_xx, ce.WX)
    u_t = _formal_derivative(u, ce.WT)
    u_xxt = _formal_derivative(u_xx, ce.WT)
    return sp.expand(
        u_t + 2 * ce.K * u_x - u_xxt
        + 3 * u * u_x
        - 2 * u_x * u_xx
        - u * u_xxx
    )


def _term_to_formal(term: sp.Expr) -> sp.Expr:
    """Rewrite one expanded additive term into coefficient * q-monomial."""
    term = sp.expand(term)
    coefficient = term
    time_exponents = [0, 0, 0]
    space_exponents = [0, 0, 0]

    for atom in term.atoms(sp.exp):
        argument = sp.expand(atom.args[0])
        time_coeff = sp.expand(argument.coeff(ce.T))
        space_coeff = sp.expand(argument.coeff(ce.X))

        atom_time_parts = [0, 0, 0]
        atom_space_parts = [0, 0, 0]
        for index, (wt, wx) in enumerate(zip(ce.WT, ce.WX)):
            time_part = sp.expand(time_coeff.coeff(wt))
            space_part = sp.expand(space_coeff.coeff(wx))
            if not time_part.is_Integer or not space_part.is_Integer:
                raise ValueError(
                    f"non-integer exponential exponent for {sp.sstr(atom)}: "
                    f"t={sp.sstr(time_part)}, x={sp.sstr(space_part)}"
                )
            atom_time_parts[index] = int(time_part)
            atom_space_parts[index] = int(space_part)

        residual_time = sp.expand(
            time_coeff
            - sum(part * wt for part, wt in zip(atom_time_parts, ce.WT))
        )
        residual_space = sp.expand(
            space_coeff
            - sum(part * wx for part, wx in zip(atom_space_parts, ce.WX))
        )
        if residual_time != 0 or residual_space != 0:
            raise ValueError(
                f"exponential argument {sp.sstr(argument)} cannot be represented "
                f"by q1,q2,q3: residual t={sp.sstr(residual_time)}, x={sp.sstr(residual_space)}"
            )
        for index in range(3):
            time_exponents[index] += atom_time_parts[index]
            space_exponents[index] += atom_space_parts[index]
        coefficient = sp.expand(coefficient / atom)

    for index in range(3):
        if time_exponents[index] != space_exponents[index]:
            raise ValueError(
                f"inconsistent q{index + 1} exponents: "
                f"t={time_exponents[index]}, x={space_exponents[index]}"
            )
        if time_exponents[index] < 0 or space_exponents[index] < 0:
            raise ValueError(f"negative q{index + 1} exponent")

    q_product = sp.Integer(1)
    for q, exponent in zip(ce.Q, time_exponents):
        if exponent:
            q_product *= q**exponent
    return sp.expand(coefficient * q_product)


def _exponential_to_formal(expr: sp.Expr) -> sp.Expr:
    """Rewrite original exponential residual into the formal q-residual."""
    expanded = sp.expand(expr)
    if expanded == 0:
        return sp.Integer(0)
    terms = [term for term in sp.Add.make_args(expanded)]
    return sp.expand(sp.Add(*[_term_to_formal(term) for term in terms]))


def build_residuals() -> ResidualSet:
    """Return the exponential residual and the independently built formal one."""
    original = sp.expand(ce.camassa_holm_residual(ce.trial_function()))
    formal = sp.expand(formal_residual_from_trial(ce.formal_trial_function()))

    try:
        original_as_formal = _exponential_to_formal(original)
    except Exception as exc:  # noqa: BLE001 - report conversion failure exactly
        return ResidualSet(
            original=original,
            formal=formal,
            formal_consistency=False,
            formal_consistency_error=(
                f"could not convert original residual to formal generators: "
                f"{type(exc).__name__}: {exc}"
            ),
        )
    difference = sp.expand(original_as_formal - formal)
    if difference == 0:
        return ResidualSet(
            original=original,
            formal=formal,
            formal_consistency=True,
        )
    return ResidualSet(
        original=original,
        formal=formal,
        formal_consistency=False,
        formal_consistency_error=(
            f"formal and original residuals disagree: {sp.sstr(difference)}"
        ),
    )
