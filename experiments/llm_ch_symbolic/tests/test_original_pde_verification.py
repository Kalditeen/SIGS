"""Raw CH verification test for the Maple-known branch."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.original_pde_verifier import verify_maple_branch  # noqa: E402


def test_maple_branch_residual_is_zero() -> None:
    result = verify_maple_branch()
    assert result["is_zero"] is True


def test_maple_branch_is_fully_recorded() -> None:
    result = verify_maple_branch()
    assert "wx1" in result["branch"]
    assert result["branch"]["wx1"] == "-1"
    assert result["branch"]["wx2"] == "1"
    assert result["branch"]["wx3"] == "-1"
    assert result["branch"]["k"] == "-b4"
