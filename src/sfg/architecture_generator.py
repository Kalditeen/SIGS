"""Bounded SFG network-architecture generator.

The generator builds :class:`~sfg.network_ir.NetworkIR` objects with explicit
phases, node-scoped activations, and sparse/skip edges.  All search-space
bounds live in :class:`GeneratorConfig` so experiment scripts never bury
magic numbers in their own loops.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from sfg.activation_registry import available_activations
from sfg.network_ir import NetworkIR


@dataclass
class GeneratorConfig:
    seed: int = 0
    min_depth: int = 1
    max_depth: int = 3
    min_nodes_per_layer: int = 1
    max_nodes_per_layer: int = 3
    min_phases: int = 2
    max_phases: int = 2
    max_total_nodes: int = 8
    max_total_edges: int = 24
    max_incoming_edges_per_node: int = 4
    allow_skip_connections: bool = True
    allow_cross_layer_connections: bool = True
    output_structure: str = "last_layer_linear"
    activation_pool: tuple[str, ...] = field(
        default_factory=lambda: tuple(spec.name for spec in available_activations())
    )
    include_identity_nodes: bool = True

    def __post_init__(self) -> None:
        if self.min_depth < 1:
            raise ValueError("min_depth must be at least 1")
        if self.max_depth < self.min_depth:
            raise ValueError("max_depth must be >= min_depth")
        if self.min_nodes_per_layer < 1:
            raise ValueError("min_nodes_per_layer must be at least 1")
        if self.max_nodes_per_layer < self.min_nodes_per_layer:
            raise ValueError("max_nodes_per_layer must be >= min_nodes_per_layer")
        if not self.activation_pool:
            raise ValueError("activation_pool must not be empty")
        for name in self.activation_pool:
            available_activations()
            if name not in {spec.name for spec in available_activations()}:
                raise ValueError(f"unknown activation {name!r}")


class ArchitectureGenerator:
    """Generate valid, deterministic NetworkIR candidates within a config."""

    def __init__(self, config: GeneratorConfig | None = None) -> None:
        self.config = config or GeneratorConfig()

    def generate(self, count: int | None = None, seed: int | None = None) -> list[NetworkIR]:
        """Generate ``count`` layered architectures from scratch."""
        count = self.config.max_total_nodes if count is None else count
        rng = random.Random(self.config.seed if seed is None else seed)
        results: list[NetworkIR] = []
        seen: set[str] = set()
        attempts = 0
        max_attempts = max(count * 20, 100)
        while len(results) < count and attempts < max_attempts:
            attempts += 1
            ir = self._random_layered_ir(f"generated_{len(results) + 1:04d}", rng)
            signature = ir.signature()
            if signature in seen:
                continue
            seen.add(signature)
            ir.metadata.update(
                {
                    "source_type": "generated",
                    "generation_rule": "bounded_layered_random",
                    "category": self._category(ir),
                    "seed": self.config.seed if seed is None else seed,
                }
            )
            results.append(ir)
        return results

    def generate_from_template(
        self,
        template_ir: NetworkIR,
        count: int = 1,
        seed: int | None = None,
    ) -> list[NetworkIR]:
        """Derive candidates from a paper template without mutating it."""
        from sfg.architecture_mutation import ArchitectureMutator, MutationConfig

        mutator = ArchitectureMutator(
            MutationConfig(
                seed=self.config.seed if seed is None else seed,
                activation_pool=self.config.activation_pool,
                max_total_nodes=self.config.max_total_nodes,
                max_incoming_edges_per_node=self.config.max_incoming_edges_per_node,
                allow_skip_connections=self.config.allow_skip_connections,
                allow_cross_layer_connections=self.config.allow_cross_layer_connections,
            )
        )
        results: list[NetworkIR] = []
        mutation_types = ("mutate_activation", "add_node", "add_layer")
        attempts = 0
        while len(results) < count and attempts < count * 8:
            attempts += 1
            mutation_type = mutation_types[len(results) % len(mutation_types)]
            outcome = mutator.mutate(template_ir, mutation_type=mutation_type, seed=(self.config.seed if seed is None else seed) + attempts)
            if not outcome.valid:
                continue
            child = outcome.network
            child.metadata["parent_template_id"] = template_ir.ir_id
            child.metadata["derived_from"] = template_ir.ir_id
            results.append(child)
        return results

    def _random_layered_ir(self, ir_id: str, rng: random.Random) -> NetworkIR:
        depth = rng.randint(self.config.min_depth, self.config.max_depth)
        phase_count = rng.randint(self.config.min_phases, self.config.max_phases)

        widths: list[int] = []
        total = 0
        for _ in range(depth):
            remaining = self.config.max_total_nodes - total
            if remaining < self.config.min_nodes_per_layer:
                break
            upper = min(self.config.max_nodes_per_layer, remaining)
            if upper < self.config.min_nodes_per_layer:
                upper = self.config.min_nodes_per_layer
            width = rng.randint(self.config.min_nodes_per_layer, upper)
            widths.append(width)
            total += width
        if not widths:
            widths = [self.config.min_nodes_per_layer]

        ir = NetworkIR(ir_id=ir_id)
        for phase_idx in range(phase_count):
            ir.add_phase(f"p{phase_idx + 1}")

        previous = [f"p{idx + 1}" for idx in range(phase_count)]
        node_counter = 0
        for layer_idx, width in enumerate(widths, start=1):
            current: list[str] = []
            for _ in range(width):
                node_id = f"h{layer_idx}_{node_counter}"
                node_counter += 1
                activation = rng.choice(self.config.activation_pool)
                sources = self._choose_sources(layer_idx, previous, node_id, ir, rng)
                ir.add_compute(node_id, activation, sources)
                current.append(node_id)
            previous = current

        if self.config.output_structure == "last_layer_linear":
            output_sources = previous
        elif self.config.output_structure == "all_hidden_linear":
            output_sources = [node_id for node_id in ir.nodes]
        else:
            raise ValueError(f"unknown output_structure {self.config.output_structure!r}")
        ir.set_linear_output(output_sources)
        ir.metadata["depth"] = len(widths)
        ir.metadata["layer_of_node"] = {
            node_id: layer
            for layer, node_id in enumerate(ir.topological_order(), start=1)
        }
        return ir

    def _choose_sources(
        self,
        layer_idx: int,
        previous: list[str],
        node_id: str,
        ir: NetworkIR,
        rng: random.Random,
    ) -> list[str]:
        candidates: list[str] = list(previous)
        if layer_idx > 1:
            phases = list(ir.phases)
            if self.config.allow_skip_connections:
                candidates = candidates + phases
            if self.config.allow_cross_layer_connections:
                earlier = [
                    other
                    for other in ir.nodes
                    if other != node_id
                ]
                candidates = candidates + earlier
        candidates = sorted(set(candidates), key=str)
        rng.shuffle(candidates)
        max_incoming = min(self.config.max_incoming_edges_per_node, max(1, len(candidates)))
        if len(candidates) <= 1:
            chosen = candidates[:1]
        else:
            chosen = candidates[: rng.randint(1, max_incoming)]
        return sorted(chosen)

    @staticmethod
    def _category(ir: NetworkIR) -> str:
        families = {node.activation.family for node in ir.nodes.values()}
        return "mixed" if len(families) > 1 else next(iter(families), "unknown")


__all__ = ["ArchitectureGenerator", "GeneratorConfig"]
