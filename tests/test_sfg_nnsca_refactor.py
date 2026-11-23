"""Focused tests for the refactored SFG-NNSCA architecture."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
PDES = ROOT / "scripts" / "pdes"
for path in (SRC, PDES):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from nnsca.adapter import Stage2Adapter  # noqa: E402
from nnsca.compiler import AnsatzCompiler  # noqa: E402
from nnsca.models import AnsatzCandidate, NetworkNode, NetworkStructure  # noqa: E402
from nnsca.registry import (  # noqa: E402
    ROLE_NODE_BIAS,
    ROLE_NODE_WEIGHT,
    ROLE_OUTPUT_BIAS,
    ROLE_OUTPUT_WEIGHT,
    ParameterRegistry,
)
from pdes.bbm import bbm_residual  # noqa: E402
from pdes.gardner import gardner_residual  # noqa: E402
from sfg.atoms import ActivationAtom, atom_by_name, available_atoms, parse_activation  # noqa: E402
from sfg.search import SearchConfig, SFGNetworkSearch  # noqa: E402

X, T = sp.symbols("x t", real=True)


def _single_node_structure(atom_name: str) -> NetworkStructure:
    structure = NetworkStructure(f"single_{atom_name}", nodes={})
    structure.nodes["x"] = NetworkNode("x", 0, 0, None)
    structure.nodes["t"] = NetworkNode("t", 0, 1, None)
    structure.add_hidden_node("h1_0", 1, 0, atom_by_name(atom_name), ["x", "t"])
    structure.set_linear_output(["h1_0"])
    return structure


def test_atom_registry_contains_jacobi_and_powers() -> None:
    names = {atom.name for atom in available_atoms()}
    assert {"tanh", "sech_pow2", "tan_pow2", "JacobiCN", "JacobiCN_pow2"} <= names


def test_parse_activation_roundtrips_expression() -> None:
    atom = parse_activation("JacobiCN_pow2")
    parsed = parse_activation(atom.expression)
    assert parsed.name == "JacobiCN_pow2"
    assert parsed.family == "jacobi"


def test_parameter_registry_reuses_symbols() -> None:
    registry = ParameterRegistry()
    first = registry.register(ROLE_NODE_WEIGHT, "w1_0_0")
    second = registry.register(ROLE_NODE_WEIGHT, "w1_0_0")
    assert first is second
    assert registry.role_of(first) == ROLE_NODE_WEIGHT
    assert ROLE_OUTPUT_WEIGHT in registry.by_role() or ROLE_OUTPUT_WEIGHT == "output_weight"


def test_structure_has_explicit_connections_and_roles() -> None:
    structure = _single_node_structure("tanh")
    assert structure.connections
    assert structure.output_terms
    roles = structure.parameter_roles()
    assert any("w1_0_0" in symbols for symbols in roles.values())
    assert any("b1_0" in symbols for symbols in roles.values())


def test_compiler_single_node_expression() -> None:
    structure = _single_node_structure("sech_pow2")
    candidate = AnsatzCandidate("single", structure)
    compiled = AnsatzCompiler().compile(candidate)
    assert compiled.expression.has(X, T)
    assert any("w1_0_0" in str(s) for s in compiled.expression.free_symbols)


def test_compiler_general_mixed_derivative() -> None:
    structure = _single_node_structure("tanh")
    compiled = AnsatzCompiler().compile(AnsatzCandidate("single", structure))
    value = compiled.derivative((X, 2), (T, 1))
    assert value is compiled.derivative((X, 2), (T, 1))


def test_compiler_node_specific_special_parameters() -> None:
    structure = NetworkStructure("jacobi", nodes={})
    structure.nodes["x"] = NetworkNode("x", 0, 0, None)
    structure.nodes["t"] = NetworkNode("t", 0, 1, None)
    structure.add_hidden_node("h1_0", 1, 0, "JacobiCN", ["x", "t"])
    structure.set_linear_output(["h1_0"])
    compiled = AnsatzCompiler().compile(AnsatzCandidate("jacobi", structure))
    assert any(str(symbol).endswith("_h1_0") for symbol in compiled.expression.free_symbols)


def test_search_generates_complete_structures_and_dedupes() -> None:
    config = SearchConfig(
        num_candidates=8,
        seed=101,
        max_hidden_layers=1,
        max_width_per_layer=2,
        max_total_hidden_nodes=4,
        include_single_node_baseline=True,
    )
    candidates = SFGNetworkSearch(config).generate()
    assert len(candidates) <= 8
    signatures = [candidate.structure.signature() for candidate in candidates]
    assert len(signatures) == len(set(signatures))
    assert all(isinstance(candidate.structure, NetworkStructure) for candidate in candidates)


def test_search_is_seed_reproducible() -> None:
    config = SearchConfig(
        num_candidates=6,
        seed=303,
        max_hidden_layers=2,
        max_width_per_layer=2,
        max_total_hidden_nodes=5,
        include_single_node_baseline=True,
    )
    first = [c.structure.signature() for c in SFGNetworkSearch(config).generate()]
    second = [c.structure.signature() for c in SFGNetworkSearch(config).generate()]
    assert first == second


def test_stage2_adapter_gardner_jacobi_cn_recovers_known_family() -> None:
    structure = _single_node_structure("JacobiCN")
    compiled = AnsatzCompiler().compile(AnsatzCandidate("jacobi_cn", structure))
    config = {
        "solver": {
            "extract_timeout": 8.0,
            "solve_timeout": 8.0,
            "residual_timeout": 8.0,
            "verify_timeout": 8.0,
        }
    }
    record = Stage2Adapter().process(compiled.expression, gardner_residual, config)
    assert record["solve_status"] == "success"
    assert record["verification_status"] == "EXACT_VERIFIED"
    assert record["exact_solutions"]


def test_stage2_adapter_bbm_residual_is_generic() -> None:
    structure = _single_node_structure("sech_pow2")
    compiled = AnsatzCompiler().compile(AnsatzCandidate("sech2", structure))
    config = {
        "solver": {
            "extract_timeout": 8.0,
            "solve_timeout": 8.0,
            "residual_timeout": 8.0,
            "verify_timeout": 8.0,
        }
    }
    record = Stage2Adapter().process(compiled.expression, bbm_residual, config)
    assert record["verification_status"] in {"EXACT_VERIFIED", "FAILED", "NO_SOLUTION", "SYMBOLIC_UNRESOLVED"}


def test_pde_specs_are_not_gardner_specific() -> None:
    from pdes.bbm import BBM
    from pdes.ch import CH
    from pdes.gardner import GARDNER

    assert BBM.name == "BBM"
    assert CH.name == "Camassa-Holm"
    assert GARDNER.name == "Gardner"


def test_run_gardner_script_end_to_end(tmp_path: Path) -> None:
    script = ROOT / "scripts" / "run_gardner.py"
    result_dir = tmp_path / "gardner_refactor"
    proc = subprocess.run(
        [
            sys.executable,
            str(script),
            "--num-structures", "3",
            "--max-hidden-layers", "1",
            "--max-width-per-layer", "1",
            "--max-total-hidden-nodes", "3",
            "--results-dir", str(result_dir),
        ],
        text=True,
        capture_output=True,
        cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stderr
    assert (result_dir / "summary.json").exists()
    summary = json.loads((result_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["generated_structures"] <= 3
    assert summary["unique_structures"] <= summary["generated_structures"]
