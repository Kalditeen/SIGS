"""End-to-end tests for generator -> normalizer -> manager -> compiler."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sfg.architecture_generator import ArchitectureGenerator, GeneratorConfig  # noqa: E402
from sfg.candidate_manager import CandidateManager  # noqa: E402
from sfg.paper_templates import PAPER_TEMPLATES  # noqa: E402

X, T = sp.symbols("x t", real=True)


def test_pipeline_compiles_generated_candidates() -> None:
    manager = CandidateManager()
    generator = ArchitectureGenerator(
        GeneratorConfig(seed=4, min_depth=1, max_depth=2, max_nodes_per_layer=2, max_total_nodes=5)
    )
    for ir in generator.generate(6, seed=4):
        manager.register(ir, generation_method="bounded_layered_random")
    manager.compile_all()
    unique = manager.unique_records()
    assert len(unique) == 6
    assert all(record.compile_status == "SUCCESS" for record in unique)
    assert all(record.expression is not None for record in unique)


def test_pipeline_compiles_all_paper_templates() -> None:
    manager = CandidateManager()
    for name, builder in PAPER_TEMPLATES.items():
        manager.register(builder(), generation_method="paper_template")
    manager.compile_all()
    assert all(record.compile_status == "SUCCESS" for record in manager.records)


def test_pipeline_keeps_parameter_roles_and_unknowns() -> None:
    manager = CandidateManager()
    ir = PAPER_TEMPLATES["2231"]()
    manager.register(ir, generation_method="paper_template")
    manager.compile_all()
    record = manager.records[0]
    assert len(record.unknown_parameters) == len(ir.parameter_symbols())
    assert set(record.unknown_parameters) == {str(symbol) for symbol in ir.parameter_symbols()}
    assert record.parameter_roles


def test_pipeline_does_not_use_legacy_codes_widths() -> None:
    manager = CandidateManager()
    ir = PAPER_TEMPLATES["2231"]()
    manager.register(ir, generation_method="paper_template")
    record = manager.records[0]
    assert "codes" not in record.network_ir.to_dict()
    assert "widths" not in record.network_ir.to_dict()
