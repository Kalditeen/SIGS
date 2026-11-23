"""Tests for candidate recording, deduplication, persistence, and stats."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sfg.candidate_manager import CandidateManager  # noqa: E402
from sfg.paper_templates import paper_templates  # noqa: E402


def test_register_and_compile_candidates() -> None:
    manager = CandidateManager()
    templates = paper_templates()
    for name, ir in templates.items():
        manager.register(ir, generation_method="paper_template")
    manager.compile_all()
    assert len(manager.records) == 5
    assert all(record.compile_status == "SUCCESS" for record in manager.records)
    assert all(record.expression for record in manager.records)
    assert all(record.unknown_parameters for record in manager.records)


def test_duplicate_candidates_are_marked_not_dropped() -> None:
    manager = CandidateManager()
    ir = paper_templates()["231"]
    first = manager.register(ir, generation_method="paper_template")
    second = manager.register(ir, generation_method="paper_template")
    assert first.status == "GENERATED"
    assert second.status == "DUPLICATE"
    assert manager.stats()["generated_candidates"] == 2
    assert manager.stats()["unique_candidates"] == 1


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    manager = CandidateManager()
    for name, ir in paper_templates().items():
        manager.register(ir, generation_method="paper_template")
    manager.compile_all()
    path = manager.save(tmp_path / "candidates.json")

    restored = CandidateManager.load(path)
    assert len(restored.records) == len(manager.records)
    assert restored.records[0].candidate_id == manager.records[0].candidate_id
    assert restored.records[0].structure_signature == manager.records[0].structure_signature
    assert restored.records[0].compile_status == "SUCCESS"


def test_parent_child_lineage_is_recorded() -> None:
    manager = CandidateManager()
    parent = manager.register(paper_templates()["231"], generation_method="paper_template")
    child = manager.register(
        paper_templates()["231"],
        generation_method="derived",
        parent_candidate_id=parent.candidate_id,
    )
    assert child.parent_candidate_id == parent.candidate_id


def test_invalid_candidate_is_not_registered() -> None:
    manager = CandidateManager()
    from sfg.network_ir import NetworkIR

    invalid = NetworkIR("bad")
    invalid.phases["p1"] = invalid.add_phase("p1").phases["p1"]
    invalid.nodes["h1"] = None  # force invalid state
    with pytest.raises((ValueError, AttributeError)):
        manager.register(invalid)
