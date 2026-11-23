"""Candidate-network registry, deduplication, persistence, and statistics."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import sympy as sp

from nnsca.compiler.ansatz_compiler import AnsatzCompiler
from sfg.architecture_normalizer import ArchitectureNormalizer, NormalizedNetwork
from sfg.network_ir import NetworkIR


@dataclass
class CandidateRecord:
    candidate_id: str
    parent_candidate_id: str | None
    network_ir: NetworkIR
    structure_signature: str
    generation_method: str
    mutation_history: list[dict]
    random_seed: int
    status: str
    normalized_ir: NormalizedNetwork | None = None
    source_type: str = "generated"
    category: str = "unknown"
    compile_status: str = "PENDING"
    compile_error: str | None = None
    expression: str | None = None
    unknown_parameters: list[str] = field(default_factory=list)
    parameter_roles: dict[str, list[str]] = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "parent_candidate_id": self.parent_candidate_id,
            "network_ir": self.network_ir.to_dict(),
            "normalized_ir": self.normalized_ir.to_dict() if self.normalized_ir else None,
            "structure_signature": self.structure_signature,
            "generation_method": self.generation_method,
            "mutation_history": self.mutation_history,
            "random_seed": self.random_seed,
            "status": self.status,
            "source_type": self.source_type,
            "category": self.category,
            "compile_status": self.compile_status,
            "compile_error": self.compile_error,
            "expression": self.expression,
            "unknown_parameters": self.unknown_parameters,
            "parameter_roles": self.parameter_roles,
            "metadata": _jsonable(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CandidateRecord":
        normalized = None
        if data.get("normalized_ir"):
            normalized = NormalizedNetwork(
                network=NetworkIR.from_dict(data["normalized_ir"]["network_ir"]),
                signature=data["normalized_ir"]["signature"],
                duplicate_edges_removed=data["normalized_ir"].get("duplicate_edges_removed", []),
                unreachable_nodes=data["normalized_ir"].get("unreachable_nodes", []),
                notes=data["normalized_ir"].get("notes", []),
            )
        return cls(
            candidate_id=data["candidate_id"],
            parent_candidate_id=data["parent_candidate_id"],
            network_ir=NetworkIR.from_dict(data["network_ir"]),
            normalized_ir=normalized,
            structure_signature=data["structure_signature"],
            generation_method=data["generation_method"],
            mutation_history=data["mutation_history"],
            random_seed=data["random_seed"],
            status=data["status"],
            source_type=data["source_type"],
            category=data["category"],
            compile_status=data["compile_status"],
            compile_error=data["compile_error"],
            expression=data.get("expression"),
            unknown_parameters=data.get("unknown_parameters", []),
            parameter_roles=data.get("parameter_roles", {}),
            metadata=data.get("metadata", {}),
        )


def _jsonable(value):
    if isinstance(value, dict):
        return {str(key): _jsonable(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    return value


class CandidateManager:
    """Own candidate IDs, deduplicate structures, compile, persist, and count."""

    def __init__(
        self,
        normalizer: ArchitectureNormalizer | None = None,
        compiler: AnsatzCompiler | None = None,
    ) -> None:
        self.normalizer = normalizer or ArchitectureNormalizer()
        self.compiler = compiler or AnsatzCompiler()
        self.records: list[CandidateRecord] = []
        self._unique_signatures: dict[str, str] = {}

    def register(
        self,
        ir: NetworkIR,
        *,
        parent_candidate_id: str | None = None,
        generation_method: str = "generated",
        mutation_history: list[dict] | None = None,
        random_seed: int = 0,
        source_type: str | None = None,
        category: str | None = None,
        status: str = "GENERATED",
        deduplicate: bool = True,
    ) -> CandidateRecord:
        ir.validate()
        normalized = self.normalizer.normalize(ir)
        signature = normalized.signature
        candidate_id = self._next_id()

        duplicate_of = None
        if deduplicate and signature in self._unique_signatures:
            duplicate_of = self._unique_signatures[signature]
            status = "DUPLICATE"
        else:
            if deduplicate:
                self._unique_signatures[signature] = candidate_id

        record = CandidateRecord(
            candidate_id=candidate_id,
            parent_candidate_id=parent_candidate_id,
            network_ir=ir,
            normalized_ir=normalized,
            structure_signature=signature,
            generation_method=generation_method,
            mutation_history=list(mutation_history or []),
            random_seed=random_seed,
            status=status,
            source_type=source_type or "generated",
            category=category or self._category(ir),
            metadata={"duplicate_of": duplicate_of} if duplicate_of else {},
        )
        self.records.append(record)
        return record

    def compile_record(self, record: CandidateRecord) -> CandidateRecord:
        if record.status == "DUPLICATE":
            record.compile_status = "SKIPPED_DUPLICATE"
            return record
        try:
            compiled = self.compiler.compile_ir(record.network_ir)
            record.expression = sp.sstr(compiled.expression)
            record.unknown_parameters = [str(s) for s in compiled.candidate.unknown_parameters]
            record.parameter_roles = compiled.candidate.parameter_roles
            record.compile_status = "SUCCESS"
            record.compile_error = None
        except Exception as exc:
            record.compile_status = "FAILED"
            record.compile_error = f"{type(exc).__name__}: {exc}"
        return record

    def compile_all(self) -> list[CandidateRecord]:
        for record in self.records:
            self.compile_record(record)
        return self.records

    def unique_records(self) -> list[CandidateRecord]:
        return [record for record in self.records if record.status != "DUPLICATE"]

    def to_dicts(self) -> list[dict]:
        return [record.to_dict() for record in self.records]

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dicts(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    @classmethod
    def load(cls, path: str | Path) -> "CandidateManager":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        manager = cls()
        for item in data:
            manager.records.append(CandidateRecord.from_dict(item))
        manager._unique_signatures = {
            record.structure_signature: record.candidate_id
            for record in manager.records
            if record.status != "DUPLICATE"
        }
        return manager

    def stats(self) -> dict:
        unique = self.unique_records()
        depths = sorted({self._depth(record.network_ir) for record in unique})
        node_counts = sorted({len(record.network_ir.nodes) for record in unique})
        activation_combinations = sorted(
            {
                tuple(sorted(node.activation.name for node in record.network_ir.nodes.values()))
                for record in unique
            }
        )
        compiled = [r for r in unique if r.compile_status == "SUCCESS"]
        failed = [r for r in unique if r.compile_status == "FAILED"]
        return {
            "generated_candidates": len(self.records),
            "unique_candidates": len(unique),
            "duplicate_candidates": len(self.records) - len(unique),
            "legal_candidates": len(unique),
            "invalid_candidates": sum(1 for r in self.records if r.status == "INVALID"),
            "depths": depths,
            "distinct_depth_count": len(depths),
            "node_counts": node_counts,
            "distinct_node_count": len(node_counts),
            "activation_combinations": [list(combo) for combo in activation_combinations],
            "distinct_activation_combination_count": len(activation_combinations),
            "compiler_success_count": len(compiled),
            "compiler_failure_count": len(failed),
        }

    @staticmethod
    def _category(ir: NetworkIR) -> str:
        families = {node.activation.family for node in ir.nodes.values()}
        return "mixed" if len(families) > 1 else next(iter(families), "unknown")

    @staticmethod
    def _depth(ir: NetworkIR) -> int:
        layers = {node_id: 0 for node_id in ir.phases}
        for node_id in ir.topological_order():
            node = ir.nodes[node_id]
            layers[node_id] = 1 + max((layers[source] for source in node.sources), default=0)
        return max(layers.values(), default=0)

    def _next_id(self) -> str:
        return f"candidate_{len(self.records) + 1:04d}"


__all__ = ["CandidateManager", "CandidateRecord"]
