"""Selection and structural profiling for Phase 3-B complex networks."""

from __future__ import annotations

from dataclasses import dataclass

from sfg.architecture_utils import hidden_depth, infer_layers, reachable_nodes
from sfg.candidate_manager import CandidateManager, CandidateRecord
from sfg.network_ir import NetworkIR


CATEGORY_NAMES = ("A", "B", "C", "D", "E", "F")


@dataclass
class StructureProfile:
    candidate_id: str
    node_count: int
    depth: int
    phase_count: int
    activation_names: list[str]
    heterogeneous: bool
    has_merge_node: bool
    has_skip_connection: bool
    multi_phase: bool
    unreachable_nodes: list[str]
    categories: list[str]

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "node_count": self.node_count,
            "depth": self.depth,
            "phase_count": self.phase_count,
            "activation_names": self.activation_names,
            "heterogeneous": self.heterogeneous,
            "has_merge_node": self.has_merge_node,
            "has_skip_connection": self.has_skip_connection,
            "multi_phase": self.multi_phase,
            "unreachable_nodes": self.unreachable_nodes,
            "categories": self.categories,
        }


def _has_skip_connection(ir: NetworkIR) -> bool:
    layers = infer_layers(ir)
    for edge in ir.edges.values():
        if edge.source in ir.nodes and edge.target in ir.nodes:
            if layers[edge.source] < layers[edge.target] - 1:
                return True
    return False


def _has_merge_node(ir: NetworkIR) -> bool:
    return any(len(node.sources) >= 2 for node in ir.nodes.values())


def structure_profile(record: CandidateRecord) -> StructureProfile:
    ir = record.network_ir
    activation_names = sorted(ir.activation_functions().values())
    node_count = len(ir.nodes)
    depth = hidden_depth(ir)
    phase_count = len(ir.phases)
    heterogeneous = len(set(activation_names)) >= 2
    merge = _has_merge_node(ir)
    skip = _has_skip_connection(ir)
    multi_phase = phase_count >= 2

    categories: list[str] = []
    if node_count == 1:
        categories.append("A")
    if node_count == 2 and heterogeneous:
        categories.append("B")
    if merge:
        categories.append("C")
    if depth >= 2:
        categories.append("D")
    if skip:
        categories.append("E")
    if multi_phase:
        categories.append("F")

    return StructureProfile(
        candidate_id=record.candidate_id,
        node_count=node_count,
        depth=depth,
        phase_count=phase_count,
        activation_names=activation_names,
        heterogeneous=heterogeneous,
        has_merge_node=merge,
        has_skip_connection=skip,
        multi_phase=multi_phase,
        unreachable_nodes=sorted(set(ir.nodes) - reachable_nodes(ir)),
        categories=categories,
    )


def select_representative_candidates(
    manager: CandidateManager,
    per_category: int = 1,
    allow_overlap: bool = True,
) -> dict[str, list[CandidateRecord]]:
    """Pick actual candidates for categories A-F without handcrafting any.

    With ``allow_overlap=False`` each candidate is used for at most one
    category in the first pass, giving more structural variety.  Remaining
    categories are filled in a second pass only when necessary.
    """
    selected: dict[str, list[CandidateRecord]] = {label: [] for label in CATEGORY_NAMES}

    if allow_overlap:
        for record in manager.unique_records():
            profile = structure_profile(record)
            for label in profile.categories:
                if len(selected[label]) < per_category:
                    selected[label].append(record)
        return selected

    used: set[str] = set()
    for record in manager.unique_records():
        if record.candidate_id in used:
            continue
        profile = structure_profile(record)
        missing = [
            label
            for label in profile.categories
            if len(selected[label]) < per_category
        ]
        if not missing:
            continue
        label = min(missing, key=CATEGORY_NAMES.index)
        selected[label].append(record)
        used.add(record.candidate_id)

    for record in manager.unique_records():
        profile = structure_profile(record)
        for label in profile.categories:
            if len(selected[label]) < per_category:
                selected[label].append(record)

    return selected


__all__ = [
    "CATEGORY_NAMES",
    "StructureProfile",
    "select_representative_candidates",
    "structure_profile",
]
