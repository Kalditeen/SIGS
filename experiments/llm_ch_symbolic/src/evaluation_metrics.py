"""Evaluation metrics for the three-way Phase 1.5 comparison."""

from __future__ import annotations

from .network_ir_adapter import NetworkIR, reference_structure


def _safe_ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def evaluate_structure_recognition(ir: NetworkIR, analysis_result: dict) -> dict:
    reference = reference_structure(ir)
    normalized = analysis_result.get("normalized") or {}
    inventory = normalized.get("activation_inventory") or {}
    network_type = normalized.get("network_type")
    network_type_accuracy = 1 if network_type == reference["network_type"] else 0

    expected_activations = {
        node["id"]: node["activation"]
        for node in ir.nodes
        if node.get("op") == "activation"
    }
    true_positive = sum(
        1
        for node_id, activation in expected_activations.items()
        if inventory.get(node_id) == activation
    )
    false_positive = sum(
        1
        for node_id in inventory
        if node_id not in expected_activations
    )
    false_negative = sum(
        1
        for node_id in expected_activations
        if node_id not in inventory
    )

    claimed_shared = set(normalized.get("shared_subexpressions") or [])
    reference_shared = set(reference["shared_subexpressions"])
    shared_tp = len(claimed_shared & reference_shared)
    shared_fp = len(claimed_shared - reference_shared)
    shared_fn = len(reference_shared - claimed_shared)

    node_ids = {node["id"] for node in ir.nodes}
    claimed_nodes = set(inventory) | claimed_shared
    node_accuracy = len(claimed_nodes & node_ids) / max(1, len(claimed_nodes))

    return {
        "activation_precision": _safe_ratio(true_positive, true_positive + false_positive),
        "activation_recall": _safe_ratio(true_positive, true_positive + false_negative),
        "activation_accuracy": _safe_ratio(true_positive, len(expected_activations)),
        "shared_precision": _safe_ratio(shared_tp, shared_tp + shared_fp),
        "shared_recall": _safe_ratio(shared_tp, shared_tp + shared_fn),
        "node_id_accuracy": node_accuracy,
        "network_type_accuracy": network_type_accuracy,
        "reference_network_type": reference["network_type"],
        "raw_counts": {
            "activation_tp": true_positive,
            "activation_fp": false_positive,
            "activation_fn": false_negative,
            "shared_tp": shared_tp,
            "shared_fp": shared_fp,
            "shared_fn": shared_fn,
        },
    }


def strategy_validation_summary(strategy_validation: dict) -> dict:
    return {
        "ok": strategy_validation.get("ok", False),
        "error_count": len(strategy_validation.get("errors", [])),
        "derivative_rule_count": len(
            (strategy_validation.get("normalized") or {}).get(
                "selected_derivative_rules", []
            )
        ),
        "identity_rule_count": len(
            (strategy_validation.get("normalized") or {}).get(
                "selected_identity_rules", []
            )
        ),
    }
