"""Bounded SFG network-structure search.

The search space is deliberately finite and configuration is centralised here.
Each generated candidate is a complete :class:`~nnsca.models.AnsatzCandidate`
wrapping an explicit :class:`~nnsca.models.NetworkStructure`, not an old-style
activation code.  Candidates carry generation rules and source type so results
remain traceable without treating a fixed template as the core architecture.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from nnsca.models import AnsatzCandidate, NetworkNode, NetworkStructure
from sfg.atoms import ActivationAtom, available_atoms




@dataclass
class SearchConfig:
    num_candidates: int = 10
    seed: int = 42
    max_hidden_layers: int = 2
    max_width_per_layer: int = 2
    max_total_hidden_nodes: int = 5
    allow_skip_connections: bool = False
    allow_shared_inputs: bool = True
    output_mode: str = "last_layer_linear"
    activation_pool: tuple[str, ...] = field(
        default_factory=lambda: tuple(atom.name for atom in available_atoms())
    )
    include_single_node_baseline: bool = True

    def with_seed(self, seed: int) -> "SearchConfig":
        return SearchConfig(
            num_candidates=self.num_candidates,
            seed=seed,
            max_hidden_layers=self.max_hidden_layers,
            max_width_per_layer=self.max_width_per_layer,
            max_total_hidden_nodes=self.max_total_hidden_nodes,
            allow_skip_connections=self.allow_skip_connections,
            allow_shared_inputs=self.allow_shared_inputs,
            output_mode=self.output_mode,
            activation_pool=self.activation_pool,
            include_single_node_baseline=self.include_single_node_baseline,
        )


def _atoms_from_config(config: SearchConfig) -> list[ActivationAtom]:
    from sfg.atoms import atom_by_name

    return [atom_by_name(name) for name in config.activation_pool]


class SFGNetworkSearch:
    """Generate complete, deduplicated network structures inside a bounded space."""

    def __init__(self, config: SearchConfig | None = None) -> None:
        self.config = config or SearchConfig()

    def generate(self) -> list[AnsatzCandidate]:
        atoms = _atoms_from_config(self.config)
        candidates: list[AnsatzCandidate] = []
        seen_signatures: set[str] = set()

        def _keep(candidate: AnsatzCandidate) -> None:
            if len(candidates) >= self.config.num_candidates:
                return
            signature = candidate.structure.signature()
            if signature in seen_signatures:
                return
            seen_signatures.add(signature)
            candidates.append(candidate)

        rng = random.Random(self.config.seed)
        if self.config.include_single_node_baseline:
            for atom in atoms[: self.config.num_candidates]:
                candidate = self._single_node_candidate(
                    atom, len(candidates), "single_node_baseline"
                )
                _keep(candidate)
                if len(candidates) >= self.config.num_candidates:
                    break

        attempts = 0
        while len(candidates) < self.config.num_candidates and attempts < self.config.num_candidates * 40:
            attempts += 1
            structure_id = f"struct_{len(candidates) + 1:04d}"
            structure = self._random_structure(structure_id, atoms, rng)
            if structure is None:
                continue
            candidate = AnsatzCandidate(
                candidate_id=f"candidate_{len(candidates) + 1:04d}",
                structure=structure,
                metadata={
                    "source_type": "generated",
                    "generation_rule": structure.metadata.get("generation_rule", "random_network"),
                    "category": self._category(structure),
                },
            )
            _keep(candidate)

        # If the random sampler could not fill the budget, enumerate compact
        # layered structures deterministically as a fallback.
        if len(candidates) < self.config.num_candidates:
            for widths, activations in self._fallback_structures(atoms):
                structure = self._layered_structure(widths, activations)
                candidate = AnsatzCandidate(
                    candidate_id=f"candidate_{len(candidates) + 1:04d}",
                    structure=structure,
                    metadata={
                        "source_type": "generated",
                        "generation_rule": "layered_enumeration",
                        "category": self._category(structure),
                    },
                )
                _keep(candidate)
                if len(candidates) >= self.config.num_candidates:
                    break
        return candidates

    def _single_node_candidate(
        self, atom: ActivationAtom, index: int, rule: str
    ) -> AnsatzCandidate:
        structure = NetworkStructure(f"single_{atom.name}_{index}", nodes={})
        structure.nodes["x"] = NetworkNode("x", 0, 0, None)
        structure.nodes["t"] = NetworkNode("t", 0, 1, None)
        structure.add_hidden_node("h1_0", 1, 0, atom, ["x", "t"])
        structure.set_linear_output(["h1_0"])
        structure.metadata = {
            "source_type": "generated",
            "generation_rule": rule,
        }
        return AnsatzCandidate(
            candidate_id=f"candidate_{index + 1:04d}",
            structure=structure,
            metadata={
                "source_type": "generated",
                "generation_rule": rule,
                "category": atom.family,
            },
        )

    def _random_structure(
        self, structure_id: str, atoms: list[ActivationAtom], rng: random.Random
    ) -> NetworkStructure | None:
        hidden_layers = rng.randint(1, self.config.max_hidden_layers)
        total_hidden = 0
        widths: list[int] = []
        for _ in range(hidden_layers):
            width = rng.randint(1, self.config.max_width_per_layer)
            if total_hidden + width > self.config.max_total_hidden_nodes:
                width = max(1, self.config.max_total_hidden_nodes - total_hidden)
            widths.append(width)
            total_hidden += width
        if total_hidden == 0:
            return None

        structure = NetworkStructure(structure_id, nodes={})
        structure.nodes["x"] = NetworkNode("x", 0, 0, None)
        structure.nodes["t"] = NetworkNode("t", 0, 1, None)
        previous = ["x", "t"]
        node_counter = 0
        for layer_idx, width in enumerate(widths, start=1):
            current: list[str] = []
            for node_idx in range(width):
                activation = rng.choice(atoms)
                sources = previous[:]
                if self.config.allow_shared_inputs and layer_idx > 1 and self.config.allow_skip_connections:
                    if rng.random() < 0.3 and "x" not in sources:
                        sources.append("x")
                    if rng.random() < 0.3 and "t" not in sources:
                        sources.append("t")
                elif layer_idx == 1:
                    # Sparse first layers are optional; keep both inputs by default.
                    sources = ["x", "t"]
                node_id = f"h{layer_idx}_{node_idx}"
                structure.add_hidden_node(node_id, layer_idx, node_counter, activation, sources)
                current.append(node_id)
                node_counter += 1
            previous = current

        structure.set_linear_output(previous)
        structure.metadata = {
            "source_type": "generated",
            "generation_rule": "random_depth_width_connections",
        }
        return structure

    def _layered_structure(
        self,
        widths: list[int],
        activations: list[ActivationAtom],
    ) -> NetworkStructure:
        structure = NetworkStructure(f"layered_{'_'.join(str(w) for w in widths)}", nodes={})
        structure.nodes["x"] = NetworkNode("x", 0, 0, None)
        structure.nodes["t"] = NetworkNode("t", 0, 1, None)
        previous = ["x", "t"]
        cursor = 0
        for layer_idx, width in enumerate(widths, start=1):
            current = []
            for node_idx in range(width):
                atom = activations[cursor]
                cursor += 1
                node_id = f"h{layer_idx}_{node_idx}"
                structure.add_hidden_node(node_id, layer_idx, node_idx, atom, previous)
                current.append(node_id)
            previous = current
        structure.set_linear_output(previous)
        return structure

    def _fallback_structures(self, atoms: list[ActivationAtom]):
        patterns = [
            ([1], [atoms[0]]),
            ([1], [atoms[1]]),
            ([2], [atoms[0], atoms[1]]),
            ([1, 1], [atoms[0], atoms[1]]),
        ]
        for widths, activations in patterns:
            yield widths, activations

    @staticmethod
    def _category(structure: NetworkStructure) -> str:
        families = {
            node.activation.family
            for node in structure.hidden_nodes()
            if node.activation is not None
        }
        if len(families) > 1:
            return "mixed"
        return next(iter(families), "unknown")


__all__ = ["SearchConfig", "SFGNetworkSearch"]
