"""Residual construction and formal/original consistency tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import sympy as sp  # noqa: E402

from src.ch_equation import camassa_holm_residual, trial_function  # noqa: E402
from src.residual_builder import build_residuals  # noqa: E402


def test_trial_has_three_exponentials() -> None:
    trial = trial_function()
    assert trial.has(sp.exp)
    assert len([arg for arg in sp.preorder_traversal(trial) if arg.func is sp.exp]) == 3


def test_residual_is_not_vacuously_zero() -> None:
    residual = camassa_holm_residual(trial_function())
    assert sp.expand(residual) != 0


def test_original_and_formal_residuals_agree() -> None:
    residuals = build_residuals()
    assert residuals.formal_consistency is True
    assert residuals.formal_consistency_error is None
