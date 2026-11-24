"""Deterministic validation of LLM network analysis and strategy output."""

from __future__ import annotations

import sympy as sp

from . import activation_registry, symbolic_rule_registry
from .network_ir_adapter import (
    NetworkIR,
    activation_inventory,
    node_by_id,
    topology_summary,
)


def _as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def validate_analysis(ir: NetworkIR, analysis: dict | None) -> dict:
    """Check that LLM network analysis only describes the real IR."""
    if not isinstance(analysis, dict):
        return {"ok": False, "errors": ["analysis is not a JSON object"], "normalized": None}

    errors: list[str] = []
    summary = topology_summary(ir)
    known_node_ids = {node["id"] for node in ir.nodes}
    reference_activations = set(activation_inventory(ir))
    reference_shared = set(summary["shared_subexpressions"])

    inventory = _as_list(analysis.get("activation_inventory"))
    inventory_by_node: dict[str, str] = {}
    for item in inventory:
        if not isinstance(item, dict) or "node_id" not in item:
            errors.append("activation_inventory entries must include node_id")
            continue
        node_id = item.get("node_id")
        if node_id not in known_node_ids:
            errors.append(f"unknown node_id {node_id!r} in activation_inventory")
            continue
        node = node_by_id(ir)[node_id]
        actual = node.get("activation")
        if node.get("op") != "activation" or item.get("activation") != actual:
            errors.append(
                f"activation mismatch for {node_id}: LLM={item.get('activation')!r} IR={actual!r}"
            )
        inventory_by_node[node_id] = item.get("activation")

    for node in ir.nodes:
        if node.get("op") == "activation" and node["id"] not in inventory_by_node:
            errors.append(f"missing activation node {node['id']} in LLM inventory")
        if node.get("op") != "activation" and node["id"] in inventory_by_node:
            errors.append(f"non-activation node {node['id']} listed as activation")

    claimed_shared = _as_list(analysis.get("shared_subexpressions"))
    unknown_shared = sorted(set(claimed_shared) - known_node_ids)
    if unknown_shared:
        errors.append(f"unknown shared_subexpression node ids: {unknown_shared}")
    if reference_shared and not claimed_shared:
        errors.append("LLM omitted all shared subexpressions")

    composite = _as_list(analysis.get("composite_relations"))
    for item in composite:
        if isinstance(item, dict):
            for key in ("node_id", "parent_node_id"):
                value = item.get(key)
                if value is not None and value not in known_node_ids:
                    errors.append(f"unknown {key} {value!r} in composite_relations")

    normalized = {
        "network_type": analysis.get("network_type", "unknown"),
        "activation_inventory": inventory_by_node,
        "composite_relations": composite,
        "shared_subexpressions": claimed_shared,
        "symbolic_difficulty": _as_list(analysis.get("symbolic_difficulty")),
        "unsupported_components": _as_list(analysis.get("unsupported_components")),
    }
    return {"ok": not errors, "errors": errors, "normalized": normalized}


def validate_strategy(ir: NetworkIR, analysis: dict, strategy: dict | None) -> dict:
    if not isinstance(strategy, dict):
        return {"ok": False, "errors": ["strategy is not a JSON object"], "normalized": None}

    errors: list[str] = []
    valid_der = set(symbolic_rule_registry.derivative_rule_ids())
    valid_id = set(symbolic_rule_registry.identity_rule_ids())

    selected_der = _as_list(strategy.get("selected_derivative_rules"))
    selected_id = _as_list(strategy.get("selected_identity_rules"))

    unknown_der = sorted(set(selected_der) - valid_der)
    unknown_id = sorted(set(selected_id) - valid_id)
    if unknown_der:
        errors.append(f"unknown derivative rule IDs: {unknown_der}")
    if unknown_id:
        errors.append(f"unknown identity rule IDs: {unknown_id}")

    supported_activations = {
        node["activation"]
        for node in ir.nodes
        if node.get("op") == "activation"
        and activation_registry.get_activation(node["activation"]).supported
    }
    covered = set()
    for rule_id in selected_der:
        rule = symbolic_rule_registry.DERIVATIVE_RULES.get(rule_id)
        if rule is not None:
            covered.add(rule.function_type)
    missing = sorted(
        act
        for act in supported_activations
        if activation_registry.get_activation(act).derivative_rule_id not in selected_der
    )
    if missing:
        errors.append(f"missing derivative rule for activation(s): {missing}")

    allowed_der_ids = {
        activation_registry.get_activation(act).derivative_rule_id
        for act in supported_activations
    }
    inapplicable_der = sorted(set(selected_der) - allowed_der_ids)
    if inapplicable_der:
        errors.append(f"inapplicable derivative rule(s) for this network: {inapplicable_der}")

    allowed_identity_ids = set()
    if {"sinh", "cosh"}.issubset(supported_activations):
        allowed_identity_ids.add("id_cosh_sinh")
    if {"sin", "cos"}.issubset(supported_activations):
        allowed_identity_ids.add("id_sin_cos")
    inapplicable_identity = sorted(set(selected_id) - allowed_identity_ids)
    if inapplicable_identity:
        errors.append(f"inapplicable identity rule(s) for this network: {inapplicable_identity}")

    normalized = {
        "generators": _as_list(strategy.get("generators")),
        "selected_derivative_rules": selected_der,
        "selected_identity_rules": selected_id,
        "intermediate_variables": _as_list(strategy.get("intermediate_variables")),
        "rewrite_strategy": _as_list(strategy.get("rewrite_strategy")),
        "collection_strategy": _as_list(strategy.get("collection_strategy")),
        "expected_structure": _as_list(strategy.get("expected_structure")),
        "unsupported_rules": _as_list(strategy.get("unsupported_rules")),
        "confidence_notes": _as_list(strategy.get("confidence_notes")),
    }
    return {"ok": not errors, "errors": errors, "normalized": normalized}
