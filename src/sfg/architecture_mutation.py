"""Structural mutation operators for SFG NetworkIR candidates.

Every operator returns an independent child IR and records the nodes/edges it
changed.  No operator mutates the parent in place, so the parent-child chain
remains reconstructable.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import sympy as sp

from sfg.activation_registry import available_activations
from sfg.architecture_utils import clone_ir, hidden_depth, infer_layers, layer_nodes
from sfg.network_ir import Edge, NetworkIR, OutputTerm


@dataclass
class MutationConfig:
    seed: int = 0
    activation_pool: tuple[str, ...] = field(
        default_factory=lambda: tuple(spec.name for spec in available_activations())
    )
    max_total_nodes: int = 8
    max_incoming_edges_per_node: int = 4
    allow_skip_connections: bool = True
    allow_cross_layer_connections: bool = True
    min_nodes_per_layer: int = 1
    max_nodes_per_layer: int = 3


@dataclass
class MutationOutcome:
    network: NetworkIR
    mutation_type: str
    changed_nodes: list[str]
    changed_edges: list[str]
    random_seed: int
    mutation_config: dict
    valid: bool


class ArchitectureMutator:
    """Apply one bounded, deterministic structural mutation at a time."""

    def __init__(self, config: MutationConfig | None = None) -> None:
        self.config = config or MutationConfig()

    def mutate(
        self,
        parent: NetworkIR,
        mutation_type: str,
        seed: int | None = None,
    ) -> MutationOutcome:
        parent.validate()
        effective_seed = self.config.seed if seed is None else seed
        rng = random.Random(self.config.seed if seed is None else seed)
        child_id = f"{parent.ir_id}__{mutation_type}__{rng.randint(0, 9999):04d}"
        child = clone_ir(parent, ir_id=child_id)
        changed_nodes: list[str] = []
        changed_edges: list[str] = []

        try:
            if mutation_type == "mutate_activation":
                changed_nodes = self._mutate_activation(child, rng)
            elif mutation_type == "add_node":
                changed_nodes = self._add_node(child, rng)
            elif mutation_type == "remove_node":
                changed_nodes, changed_edges = self._remove_node(child, rng)
            elif mutation_type == "add_edge":
                changed_edges = self._add_edge(child, rng, skip_only=False)
            elif mutation_type == "add_skip_edge":
                changed_edges = self._add_edge(child, rng, skip_only=True)
            elif mutation_type == "remove_edge":
                changed_edges = self._remove_edge(child, rng)
            elif mutation_type == "rewire_edge":
                changed_edges = self._rewire_edge(child, rng)
            elif mutation_type == "add_layer":
                changed_nodes = self._add_layer(child, rng)
            elif mutation_type == "remove_layer":
                changed_nodes, changed_edges = self._remove_layer(child, rng)
            elif mutation_type == "change_node_layer":
                changed_nodes, changed_edges = self._change_node_layer(child, rng)
            else:
                raise ValueError(f"unknown mutation_type {mutation_type!r}")
        except ValueError:
            return MutationOutcome(
                network=child,
                mutation_type=mutation_type,
                changed_nodes=[],
                changed_edges=[],
                random_seed=effective_seed,
                mutation_config=self._config_dict(),
                valid=False,
            )

        try:
            child.validate()
        except ValueError:
            return MutationOutcome(
                network=child,
                mutation_type=mutation_type,
                changed_nodes=changed_nodes,
                changed_edges=changed_edges,
                random_seed=effective_seed,
                mutation_config=self._config_dict(),
                valid=False,
            )

        child.metadata.setdefault("mutation_history", [])
        child.metadata["mutation_history"].append(
            {
                "parent_ir_id": parent.ir_id,
                "mutation_type": mutation_type,
                "changed_nodes": changed_nodes,
                "changed_edges": changed_edges,
                "random_seed": effective_seed,
            }
        )
        return MutationOutcome(
            network=child,
            mutation_type=mutation_type,
            changed_nodes=changed_nodes,
            changed_edges=changed_edges,
            random_seed=effective_seed,
            mutation_config=self._config_dict(),
            valid=True,
        )

    def _config_dict(self) -> dict:
        return {
            "seed": self.config.seed,
            "activation_pool": list(self.config.activation_pool),
            "max_total_nodes": self.config.max_total_nodes,
            "max_incoming_edges_per_node": self.config.max_incoming_edges_per_node,
            "allow_skip_connections": self.config.allow_skip_connections,
            "allow_cross_layer_connections": self.config.allow_cross_layer_connections,
        }

    def _mutate_activation(self, ir: NetworkIR, rng: random.Random) -> list[str]:
        if not ir.nodes:
            raise ValueError("cannot mutate activation without compute nodes")
        node_id = rng.choice(sorted(ir.nodes))
        current = ir.nodes[node_id].activation.name
        choices = [name for name in self.config.activation_pool if name != current]
        if not choices:
            raise ValueError("activation pool has no alternative activation")
        replacement = rng.choice(choices)
        ir.nodes[node_id].activation = __import__(
            "sfg.activation_registry", fromlist=["activation_by_name"]
        ).activation_by_name(replacement)
        ir.metadata.setdefault("activation_changes", []).append(
            {"node_id": node_id, "from": current, "to": replacement}
        )
        return [node_id]

    def _add_node(self, ir: NetworkIR, rng: random.Random) -> list[str]:
        if len(ir.nodes) >= self.config.max_total_nodes:
            raise ValueError("max_total_nodes reached")
        layers = infer_layers(ir)
        if not layers or not any(layer > 0 for layer in layers.values()):
            raise ValueError("cannot add node to a phase-only network")
        layer_idx = rng.choice([layer for layer in sorted(set(layers.values())) if layer > 0])
        node_id = self._new_node_id(ir, layer_idx)
        sources = self._available_sources_for_layer(ir, layer_idx)
        sources = [source for source in sources if source not in ir.nodes[node_id].sources] if node_id in ir.nodes else sources
        if not sources:
            raise ValueError("no available source for new node")
        max_incoming = min(self.config.max_incoming_edges_per_node, len(sources))
        chosen = sources[: rng.randint(1, max_incoming)]
        ir.add_compute(node_id, rng.choice(self.config.activation_pool), chosen)
        ir.metadata.setdefault("added_nodes", []).append(node_id)
        return [node_id]

    def _remove_node(self, ir: NetworkIR, rng: random.Random) -> tuple[list[str], list[str]]:
        if len(ir.nodes) <= 1:
            raise ValueError("cannot remove the only compute node")
        removable = [node_id for node_id in ir.nodes if not self._is_sole_output(ir, node_id)]
        if not removable:
            removable = list(ir.nodes)
        node_id = rng.choice(removable)

        changed_edges: list[str] = []
        for key in [key for key in ir.edges if key[0] == node_id or key[1] == node_id]:
            changed_edges.append(ir.edges[key].edge_id)
            ir.edges.pop(key, None)

        for other_id, other in ir.nodes.items():
            if other_id == node_id:
                continue
            if node_id in other.sources:
                other.sources = tuple(source for source in other.sources if source != node_id)

        ir.output_terms = [term for term in ir.output_terms if term.source != node_id]
        if not ir.output_terms:
            remaining = sorted(ir.nodes.keys() - {node_id})
            if not remaining:
                raise ValueError("removing node would leave no output")
            ir.output_terms = [OutputTerm(source=remaining[0], weight=sp.Symbol(f"c_{remaining[0]}"))]
        ir.nodes.pop(node_id)
        ir.metadata.setdefault("removed_nodes", []).append(node_id)
        return [node_id], changed_edges

    def _add_edge(self, ir: NetworkIR, rng: random.Random, skip_only: bool) -> list[str]:
        layers = infer_layers(ir)
        targets = [
            node_id
            for node_id, layer in layers.items()
            if node_id in ir.nodes and layer >= (2 if skip_only else 1)
        ]
        if not targets:
            raise ValueError("no node can receive an edge")
        rng.shuffle(targets)
        for target in targets:
            target_layer = layers[target]
            candidates = self._available_sources_for_layer(ir, target_layer)
            if skip_only:
                candidates = [source for source in candidates if layers.get(source, 0) < target_layer - 1]
            existing = set(ir.nodes[target].sources)
            candidates = [source for source in candidates if source not in existing]
            if not candidates or len(ir.nodes[target].sources) >= self.config.max_incoming_edges_per_node:
                continue
            source = rng.choice(candidates)
            break
        else:
            raise ValueError("no missing edge candidate")
        edge_id = f"edge_{source}__{target}"
        ir.edges[(source, target)] = Edge(
            edge_id=edge_id,
            source=source,
            target=target,
            weight=sp.Symbol(f"w_{source}__{target}"),
        )
        ir.nodes[target].sources = tuple(sorted(set(ir.nodes[target].sources) | {source}))
        ir.metadata.setdefault("added_edges", []).append(edge_id)
        return [edge_id]

    def _remove_edge(self, ir: NetworkIR, rng: random.Random) -> list[str]:
        eligible = [
            key for key, edge in ir.edges.items()
            if key[1] in ir.nodes and len(ir.nodes[key[1]].sources) > 1
        ]
        if not eligible:
            raise ValueError("no removable edge with a connected target")
        key = rng.choice(eligible)
        edge_id = ir.edges[key].edge_id
        ir.edges.pop(key)
        target = key[1]
        ir.nodes[target].sources = tuple(source for source in ir.nodes[target].sources if source != key[0])
        ir.metadata.setdefault("removed_edges", []).append(edge_id)
        return [edge_id]

    def _rewire_edge(self, ir: NetworkIR, rng: random.Random) -> list[str]:
        eligible = [key for key in ir.edges if key[1] in ir.nodes]
        if not eligible:
            raise ValueError("no edge to rewire")
        layers = infer_layers(ir)
        rng.shuffle(eligible)
        for key in eligible:
            target = key[1]
            target_layer = layers[target]
            candidates = self._available_sources_for_layer(ir, target_layer)
            existing = set(ir.nodes[target].sources)
            candidates = [source for source in candidates if source != key[0] and source not in existing]
            if candidates:
                new_source = rng.choice(candidates)
                break
        else:
            raise ValueError("no rewire candidate")
        old_edge_id = ir.edges[key].edge_id
        ir.edges.pop(key)
        sources = [source if source != key[0] else new_source for source in ir.nodes[target].sources]
        ir.nodes[target].sources = tuple(sources)
        new_edge_id = f"edge_{new_source}__{target}"
        ir.edges[(new_source, target)] = Edge(
            edge_id=new_edge_id,
            source=new_source,
            target=target,
            weight=sp.Symbol(f"w_{new_source}__{target}"),
        )
        ir.metadata.setdefault("rewired_edges", []).append(
            {"old": old_edge_id, "new": new_edge_id}
        )
        return [old_edge_id, new_edge_id]

    def _add_layer(self, ir: NetworkIR, rng: random.Random) -> list[str]:
        layers = layer_nodes(ir)
        new_layer = max(layers) + 1
        previous = layers[max(layers)]
        width = rng.randint(self.config.min_nodes_per_layer, self.config.max_nodes_per_layer)
        width = min(width, self.config.max_total_nodes - len(ir.nodes))
        if width < 1:
            raise ValueError("max_total_nodes reached")
        added: list[str] = []
        for _ in range(width):
            node_id = self._new_node_id(ir, new_layer)
            sources = self._choose_sources(ir, previous, rng, 1)
            ir.add_compute(node_id, rng.choice(self.config.activation_pool), sources)
            added.append(node_id)
        ir.set_linear_output([node_id for node_id in layer_nodes(ir)[max(layer_nodes(ir))]])
        ir.metadata.setdefault("added_nodes", []).extend(added)
        return added

    def _remove_layer(self, ir: NetworkIR, rng: random.Random) -> tuple[list[str], list[str]]:
        layers = layer_nodes(ir)
        if max(layers) <= 1:
            raise ValueError("cannot remove the only hidden layer")
        removed_layer = max(layers)
        removed_nodes = layers[removed_layer]
        changed_nodes: list[str] = []
        changed_edges: list[str] = []
        for node_id in removed_nodes:
            for key in [key for key in ir.edges if key[0] == node_id or key[1] == node_id]:
                changed_edges.append(ir.edges[key].edge_id)
                ir.edges.pop(key, None)
            ir.nodes.pop(node_id, None)
            changed_nodes.append(node_id)
        for node in ir.nodes.values():
            node.sources = tuple(source for source in node.sources if source not in removed_nodes)
        new_last = layers[removed_layer - 1]
        ir.output_terms = [
            OutputTerm(source=node_id, weight=sp.Symbol(f"c_{node_id}"))
            for node_id in new_last
        ]
        ir.metadata.setdefault("removed_nodes", []).extend(removed_nodes)
        return changed_nodes, changed_edges

    def _change_node_layer(self, ir: NetworkIR, rng: random.Random) -> tuple[list[str], list[str]]:
        layers = infer_layers(ir)
        eligible = [node_id for node_id, layer in layers.items() if layer >= 2]
        if not eligible:
            raise ValueError("no node can change layer")
        node_id = rng.choice(eligible)
        current_layer = layers[node_id]
        target_layer = rng.randint(1, current_layer - 1)
        candidates = self._available_sources_for_layer(ir, target_layer)
        existing = set(ir.nodes[node_id].sources)
        candidates = [source for source in candidates if source not in existing]
        if not candidates:
            raise ValueError("no source available at target layer")
        chosen = candidates[: rng.randint(1, min(self.config.max_incoming_edges_per_node, len(candidates)))]
        old_edges = [ir.edges[(source, node_id)].edge_id for source in ir.nodes[node_id].sources if (source, node_id) in ir.edges]
        for source in list(ir.nodes[node_id].sources):
            ir.edges.pop((source, node_id), None)
        ir.nodes[node_id].sources = tuple(chosen)
        for source in chosen:
            ir.edges[(source, node_id)] = Edge(
                edge_id=f"edge_{source}__{node_id}",
                source=source,
                target=node_id,
                weight=sp.Symbol(f"w_{source}__{node_id}"),
            )
        ir.metadata.setdefault("changed_node_layers", []).append(
            {"node_id": node_id, "from_layer": current_layer, "to_layer": target_layer}
        )
        return [node_id], old_edges + [f"edge_{source}__{node_id}" for source in chosen]

    def _available_sources_for_layer(self, ir: NetworkIR, layer_idx: int) -> list[str]:
        if layer_idx == 1:
            return sorted(ir.phases)
        layers = infer_layers(ir)
        candidates = [
            node_id
            for node_id, layer in layers.items()
            if node_id in ir.nodes and layer < layer_idx
        ]
        include_phases = layer_idx > 1 and (self.config.allow_skip_connections or self.config.allow_cross_layer_connections)
        if include_phases:
            candidates.extend(ir.phases)
        if not self.config.allow_cross_layer_connections:
            candidates = [
                node_id
                for node_id in candidates
                if layers.get(node_id, 0) == layer_idx - 1
            ]
        elif not self.config.allow_skip_connections:
            candidates = [
                node_id
                for node_id in candidates
                if layers.get(node_id, 0) == layer_idx - 1
            ]
        return sorted(set(candidates))

    def _choose_sources(self, ir: NetworkIR, candidates: list[str], rng: random.Random, min_count: int = 1) -> list[str]:
        candidates = sorted(set(candidates))
        if not candidates:
            raise ValueError("no source candidates")
        max_incoming = min(self.config.max_incoming_edges_per_node, len(candidates))
        if max_incoming < min_count:
            raise ValueError("not enough source candidates")
        chosen_count = rng.randint(min_count, max_incoming)
        return candidates[:chosen_count]

    @staticmethod
    def _is_sole_output(ir: NetworkIR, node_id: str) -> bool:
        outputs = {term.source for term in ir.output_terms}
        return outputs == {node_id}

    @staticmethod
    def _new_node_id(ir: NetworkIR, layer_idx: int) -> str:
        idx = 0
        while True:
            node_id = f"h{layer_idx}_{idx}"
            if node_id not in ir.nodes:
                return node_id
            idx += 1


__all__ = ["ArchitectureMutator", "MutationConfig", "MutationOutcome"]
