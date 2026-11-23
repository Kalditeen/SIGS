#!/usr/bin/env python3
"""Core entry point for the SFG + NNSCA [2,1] BBM workflow.

Usage:

    python scripts/test_sfg_bbm_21.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PDES_DIR = Path(__file__).resolve().parent / "pdes"
if str(PDES_DIR) not in sys.path:
    sys.path.insert(0, str(PDES_DIR))

import sfg_bbm_21  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(sfg_bbm_21.main())
