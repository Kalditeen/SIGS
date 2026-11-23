# Scripts Cleanup Report

This report covers Phase 0 of the SFG-NNSCA refactor. The `results/` directory was not touched and will be recreated by the user or by later experiments.

## Audit Method

1. Listed every Python, shell, and auxiliary file under `scripts/`.
2. Searched `tests/`, `src/`, and remaining `scripts/` modules for imports and direct references.
3. Classified each file as core/reusable, new architecture entry point, or obsolete experiment/temporary diagnostic.
4. Deleted only files with no test or retained-module dependency.

## Deleted Files

### Obsolete NNSCA/SIGS experiments

- `scripts/pdes/bbm_pipeline.py`
- `scripts/pdes/ch_nnsca.py`
- `scripts/pdes/kdv_nnsca.py`
- `scripts/pdes/vcgardner_nnsca.py`
- `scripts/ch/ch_nnsca_2221.py`
- `scripts/ch/ch_nnsca_2231.py`
- `scripts/ch/ch_nnsca_231.py`
- `scripts/ch/ch_nnsca_2321.py`
- `scripts/ch/ch_nnsca_23211.py`
- `scripts/ch/run_ch_ablation.sh`
- `scripts/kdv/kdv_common.py`
- `scripts/kdv/kdv_nnsca.py`
- `scripts/kdv/kdv_nnsca2.py`
- `scripts/kdv/kdv_nnsca2321.py`
- `scripts/kdv/kdv_repro.py`
- `scripts/kdv/kdv_unbiased_test.py`
- `scripts/vkdv/vkdv_common.py`
- `scripts/vkdv/vkdv_nnsca.py`

Reason: these are fixed-template `codes + widths` NNSCA/SIGS experiment files. They are replaced by the new SFG network-structure search path and are not imported by tests or retained modules.

### Temporary or superseded diagnostics

- `scripts/pdes/diagnose_sfg_solver.py`
- `scripts/pdes/test_sigs_stage1_audit.py`
- `scripts/pdes/run_sfg_phase3_multi_seed.py`
- `scripts/pdes/run_sfg_phase4.py`
- `scripts/pdes/run_sfg_phase5.py`
- `scripts/pdes/run_sfg_gardner.py`
- `scripts/test_sfg_bbm_21.py`
- `scripts/smoke_test.py`

Reason: superseded by `run_sfg_gardner_phase2.py`, `run_sfg_gardner_phase3.py`, `run_sfg_gardner_phase4.py`, or the real pytest suites under `tests/`.

### Unrelated SIGS/Euler discovery scripts

- `scripts/discover.py`
- `scripts/euler_search.py`
- `scripts/optimize.py`
- `scripts/plot_euler.py`
- `scripts/run_euler_four_fields.py`
- `scripts/run_euler_same_series.py`

Reason: unrelated to the current one-dimensional shallow-water SFG-NNSCA exact-solver architecture.

## Restored During Audit

- `scripts/ch/ch_common.py`

This file was initially marked for deletion, but dependency analysis showed `scripts/pdes/pde_common.py` and `scripts/pdes/maple_export.py` import it as `_ch`. It is retained as a Stage2 support module.

## Retained Files

- `scripts/pdes/bbm_nnsca.py`: new SFG + NNSCA BBM entry.
- `scripts/pdes/equations.py`: PDE specifications used by the generic engine.
- `scripts/pdes/maple_export.py`: Maple export/import helpers, no automatic Maple call.
- `scripts/pdes/pde_common.py`: existing Stage1/Stage2 symbolic engine to be protected.
- `scripts/pdes/run_sfg_gardner_phase2.py`
- `scripts/pdes/run_sfg_gardner_phase3.py`
- `scripts/pdes/run_sfg_gardner_phase4.py`
- `scripts/pdes/sfg_bbm_21.py`
- `scripts/pdes/sfg_dag.py`
- `scripts/pdes/sfg_families.py`
- `scripts/pdes/sfg_gardner.py`
- `scripts/pdes/sfg_graph.py`
- `scripts/pdes/sfg_reduction.py`
- `scripts/ch/ch_common.py`

## Dependency Check Result

No retained test or retained module imports a deleted file. The only cross-dependency correction was restoring `ch_common.py`.

## New `scripts` Structure

```text
scripts/
├── ch/
│   └── ch_common.py
└── pdes/
    ├── bbm_nnsca.py
    ├── equations.py
    ├── maple_export.py
    ├── pde_common.py
    ├── run_sfg_gardner_phase2.py
    ├── run_sfg_gardner_phase3.py
    ├── run_sfg_gardner_phase4.py
    ├── sfg_bbm_21.py
    ├── sfg_dag.py
    ├── sfg_families.py
    ├── sfg_gardner.py
    ├── sfg_graph.py
    └── sfg_reduction.py
```
