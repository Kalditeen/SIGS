# Directory Plan

This is the target layout for the SFG-NNSCA refactor. Existing valid modules are kept in place until their new-home counterparts are stable; no large mechanical migration is performed in Phase 0.

```text
SIGS/
├── docs/
│   └── sfg_nnsca_refactor/
│       ├── SCRIPTS_CLEANUP_REPORT.md
│       ├── ARCHITECTURE_AUDIT.md
│       └── DIRECTORY_PLAN.md
│
├── src/
│   ├── sfg/
│   │   ├── atoms/
│   │   ├── graph/
│   │   ├── search/
│   │   └── normalize/
│   │
│   ├── nnsca/
│   │   ├── compiler/
│   │   ├── symbolic/
│   │   ├── constraints/
│   │   ├── solver/
│   │   └── verification/
│   │
│   └── pdes/
│       ├── gardner.py
│       ├── bbm.py
│       └── ch.py
│
├── scripts/
│   ├── run_gardner.py
│   └── audit_candidates.py
│
├── tests/
│   ├── test_sfg/
│   ├── test_compiler/
│   ├── test_stage2/
│   └── test_gardner/
│
├── results/
│
└── ...
```

## Transition Rules

1. Keep `scripts/pdes/pde_common.py`, `equations.py`, and `maple_export.py` as the existing Stage2 implementation until the `src/nnsca/*` modules are independently tested.
2. New SFG and AnsatzCompiler code starts under `src/sfg/` and `src/nnsca/compiler/`, with thin scripts in `scripts/`.
3. New results go into a fresh `results/` directory; old results are not migrated.
4. Do not move `src/sigs/` wholesale. Reuse only its `jacobi.py` and any still-needed utilities.
5. Do not hardcode Gardner solutions in SFG, network search, compiler, or Stage2.
