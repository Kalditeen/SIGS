"""Execute a validated strategy with SymPy and record every transformation."""

from __future__ import annotations

import time

import sympy as sp

from . import activation_registry, symbolic_rule_registry
from .network_ir_adapter import NetworkIR, compile_expression
from .residual_analyzer import (
    camassa_holm_residual,
    common_term_groups,
    expression_size,
    residual_summary,
)


def _safe_expand(expr: sp.Expr) -> sp.Expr:
    try:
        return sp.expand(expr)
    except Exception:  # noqa: BLE001
        return expr


def _safe_sstr(expr: sp.Expr) -> str:
    try:
        return sp.sstr(expr)
    except Exception as exc:  # noqa: BLE001
        return f"<sstr failed: {type(exc).__name__}: {exc}>"


IDENTITY_TERM_LIMIT = 250


def execute_strategy(ir: NetworkIR, strategy: dict) -> dict:
    started = time.perf_counter()
    errors: list[str] = []
    try:
        u = compile_expression(ir, activation_registry)
    except Exception as exc:  # noqa: BLE001
        return {
            "network_id": ir.network_id,
            "compile_status": "failed",
            "compile_error": f"{type(exc).__name__}: {exc}",
            "duration_seconds": time.perf_counter() - started,
        }

    compiled = u
    residual = _safe_expand(camassa_holm_residual(compiled))
    summary = residual_summary(compiled)

    identity_rewrites = []
    current = residual
    identity_complexity_skipped = summary["additive_terms"] > IDENTITY_TERM_LIMIT
    for rule_id in strategy.get("selected_identity_rules", []):
        rule = symbolic_rule_registry.IDENTITY_RULES.get(rule_id)
        if rule is None:
            continue
        if identity_complexity_skipped:
            identity_rewrites.append({
                "rule_id": rule_id,
                "status": "skipped_complexity",
                "reason": (
                    f"residual additive terms {summary['additive_terms']} "
                    f"exceed IDENTITY_TERM_LIMIT {IDENTITY_TERM_LIMIT}"
                ),
            })
            continue
        before = current
        try:
            after = rule.executor(current)
        except Exception as exc:  # noqa: BLE001
            identity_rewrites.append({
                "rule_id": rule_id,
                "status": "executor_failed",
                "error": f"{type(exc).__name__}: {exc}",
            })
            continue
        try:
            equivalent = symbolic_rule_registry.identity_is_equivalent(
                rule, before, after
            )
        except Exception as exc:  # noqa: BLE001
            identity_rewrites.append({
                "rule_id": rule_id,
                "status": "equivalence_unresolved",
                "error": f"{type(exc).__name__}: {exc}",
            })
            continue
        identity_rewrites.append({
            "rule_id": rule_id,
            "status": "applied" if equivalent else "equivalence_failed",
            "equivalent": equivalent,
            "before_ops": sp.count_ops(before, visual=False),
            "after_ops": sp.count_ops(after, visual=False),
        })
        if equivalent:
            current = after
        else:
            errors.append(f"identity rule {rule_id} produced a non-equivalent expression")

    grouping = common_term_groups(current)

    return {
        "network_id": ir.network_id,
        "compile_status": "success",
        "compiled_expression": _safe_sstr(compiled),
        "compiled_size": expression_size(compiled),
        "residual_ops": sp.count_ops(current, visual=False),
        "residual_terms": summary["additive_terms"],
        "residual_is_zero": summary["residual_is_zero"],
        "identity_rewrites": identity_rewrites,
        "common_term_grouping": {
            "term_count": grouping["term_count"],
            "group_count": grouping["group_count"],
        },
        "errors": errors,
        "duration_seconds": time.perf_counter() - started,
    }




def _applicable_rule_ids(ir: NetworkIR) -> dict:
    """Rule subset a human planner would select for the activations in this IR."""
    supported = {
        node["activation"]
        for node in ir.nodes
        if node.get("op") == "activation"
        and activation_registry.get_activation(node["activation"]).supported
    }
    derivative_rules = [
        activation_registry.get_activation(act).derivative_rule_id
        for act in sorted(supported)
    ]
    derivative_rules = [rule for rule in derivative_rules if rule is not None]

    identity_rules = []
    if {"sinh", "cosh"}.issubset(supported):
        identity_rules.append("id_cosh_sinh")
    if {"sin", "cos"}.issubset(supported):
        identity_rules.append("id_sin_cos")

    return {
        "selected_derivative_rules": sorted(set(derivative_rules)),
        "selected_identity_rules": sorted(identity_rules),
    }


def execute_traditional(ir: NetworkIR) -> dict:
    """Deterministic fixed-rule baseline using only applicable rules."""
    return execute_strategy(ir, _applicable_rule_ids(ir))


def execute_manual(ir: NetworkIR) -> dict:
    """Human-planned baseline.

    For the current small rule catalog the curated subset coincides with the
    applicable-rule selection above; the design cost (choosing one derivative
    rule per activation and one identity rule per present function pair) is
    recorded in the Phase 1.5 report rather than encoded per network.
    """
    return execute_strategy(ir, _applicable_rule_ids(ir))
