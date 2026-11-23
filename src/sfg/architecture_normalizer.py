"""Canonicalisation and structural deduplication for SFG NetworkIR."""

from __future__ import annotations

from dataclasses import dataclass, field

from sfg.architecture_utils import infer_layers, reachable_nodes
from sfg.network_ir import NetworkIR, OutputTerm


@dataclass
class NormalizedNetwork:
    network: NetworkIR
    signature: str
    duplicate_edges_removed: list[str] = field(default_factory=list)
    unreachable_nodes: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "signature": self.signature,
            "duplicate_edges_removed": self.duplicate_edges_removed,
            "unreachable_nodes": self.unreachable_nodes,
            "notes": self.notes,
            "network_ir": self.network.to_dict(),
        }


class ArchitectureNormalizer:
    """Canonicalise IDs without changing the underlying computation graph."""

    def normalize(self, ir: NetworkIR) -> NormalizedNetwork:
        ir.validate()
        canonical = canonical_network_ir(ir)
        unreachable = sorted(set(ir.nodes) - reachable_nodes(ir))
        notes: list[str] = []
        if unreachable:
            notes.append(f"{len(unreachable)} nodes do not reach the output; kept for traceability")
        return NormalizedNetwork(
            network=canonical,
            signature=canonical.signature(),
            duplicate_edges_removed=[],
            unreachable_nodes=unreachable,
            notes=notes,
        )

    def structurally_equivalent(self, left: NetworkIR, right: NetworkIR) -> bool:
        return self.normalize(left).signature == self.normalize(right).signature

    def equivalence_kind(self, left: NetworkIR, right: NetworkIR) -> str:
        if not self.structurally_equivalent(left, right):
            return "STRUCTURALLY_DIFFERENT"
        return "STRUCTURAL_EQUIVALENT"


def canonical_network_ir(ir: NetworkIR) -> NetworkIR:
    """Return an isomorphic IR whose IDs are derived from DAG depth and order.

    This is structural canonicalisation only.  It deliberately does not claim
    mathematical or parameter-solution equivalence.
    """
    layers = infer_layers(ir)
    phase_map = {
        node_id: f"p{idx}"
        for idx, node_id in enumerate(sorted(ir.phases), start=1)
    }
    node_map: dict[str, str] = {}

    for layer in sorted({value for key, value in layers.items() if key in ir.nodes}):
        node_ids = sorted(
            [node_id for node_id, value in layers.items() if node_id in ir.nodes and value == layer],
            key=lambda node_id: (
                ir.nodes[node_id].activation.name,
                tuple(
                    sorted(
                        phase_map.get(source, node_map.get(source, source))
                        for source in ir.nodes[node_id].sources
                    )
                ),
            ),
        )
        for idx, node_id in enumerate(node_ids):
            node_map[node_id] = f"h{layer}_{idx}"

    canonical = NetworkIR(ir_id=ir.ir_id)
    for original_id, canonical_id in sorted(phase_map.items(), key=lambda item: item[1]):
        phase = ir.phases[original_id]
        canonical.add_phase(canonical_id)
    for original_id in ir.topological_order():
        node = ir.nodes[original_id]
        sources = [node_map[source] if source in node_map else phase_map.get(source, source) for source in node.sources]
        canonical.add_compute(node_map[original_id], node.activation.name, sources)

    output_terms = [
        OutputTerm(
            source=node_map.get(term.source, phase_map.get(term.source, term.source)),
            weight=term.weight,
        )
        for term in ir.output_terms
    ]
    canonical.set_linear_output([term.source for term in output_terms], output_bias=ir.output_bias)
    canonical.metadata = dict(ir.metadata)
    canonical.metadata["canonicalized_from"] = ir.ir_id
    canonical.metadata["canonical_ids"] = {**phase_map, **node_map}
    return canonical


__all__ = ["ArchitectureNormalizer", "NormalizedNetwork", "canonical_network_ir"]
