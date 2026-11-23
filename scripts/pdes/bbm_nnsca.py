#!/usr/bin/env python3
"""BBM validation with the SFG + NNSCA [2,1] workflow.

The hierarchical `[2,2,1]` engine remains available in ``bbm_pipeline.py``;
this entry point runs the minimal single-activation system required by the
SFG/NNSCA development task.
"""

import sfg_bbm_21
if __name__ == "__main__":
    raise SystemExit(sfg_bbm_21.main())
