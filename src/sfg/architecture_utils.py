"""Small shared helpers for SFG architecture generation.

This module intentionally contains only structural utilities used by the
generator, mutator, normalizer, and candidate manager.  It does not encode
search policy or PDE knowledge.
"""

from __future__ import annotations

import sympy as sp

from sfg.network_ir import ComputeNode, NetworkIR, PhaseNode


def infer_layers(ir: NetworkIR) -> dict[str, int]:
    """Assign each node a zero-based DAG depth from the phase inputs."""
    layers: dict[str, int] = {phase_id: 0 for phase_id in ir.phases}
    for node_id in ir.topological_order():
        node = ir.nodes[node_id]
        source_layers = [layers[source] for source in node.sources]
        layers[node_id] = 1 + max(source_layers, default=0)
    return layers


def hidden_depth(ir: NetworkIR) -> int:
    """Return the number of hidden layers in the DAG."""
    layers = infer_layers(ir)
    return max(layers.values(), default=0)


def layer_nodes(ir: NetworkIR) -> dict[int, list[str]]:
    """Group compute-node IDs by layer while preserving layer order."""
    layers = infer_layers(ir)
    grouped: dict[int, list[str]] = {}
    for node_id, layer in layers.items():
        if node_id in ir.nodes:
            grouped.setdefault(layer, []).append(node_id)
    for node_ids in grouped.values():
        node_ids.sort()
    return dict(sorted(grouped.items()))


def reachable_nodes(ir: NetworkIR) -> set[str]:
    """Return node IDs that can actually influence at least one output term."""
    active: set[str] = {term.source for term in ir.output_terms}
    active = {node_id for node_id in active if node_id in ir.nodes}
    changed = True
    while changed:
        changed = False
        for node_id, node in ir.nodes.items():
            if node_id in active:
                for source in node.sources:
                    if source not in active:
                        active.add(source)
                        changed = True
    return active


def clone_ir(ir: NetworkIR, ir_id: str | None = None) -> NetworkIR:
    """Return an independent deep copy of an IR."""
    clone = NetworkIR.from_dict(ir.to_dict())
    if ir_id is not None:
        clone.ir_id = ir_id
    clone.metadata = dict(ir.metadata)
    return clone


def activation_sources_key(
    ir: NetworkIR,
    node_id: str,
    phase_map: dict[str, str],
    node_map: dict[str, str],
) -> tuple[str, tuple[str, ...]]:
    """Return a canonical sorting key for a node in canonicalisation."""
    node = ir.nodes[node_id]
    canonical_sources = tuple(
        sorted(
            phase_map.get(source, node_map.get(source, source))
            for source in node.sources
        )
    )
    return (node.activation.name, canonical_sources)


def ensure_metadata_layers(ir: NetworkIR) -> dict[str, int]:
    """Attach and return the inferred layer map in IR metadata."""
    layers = infer_layers(ir)
    ir.metadata["layer_of_node"] = layers
    ir.metadata["depth"] = hidden_depth(ir)
    return layers
