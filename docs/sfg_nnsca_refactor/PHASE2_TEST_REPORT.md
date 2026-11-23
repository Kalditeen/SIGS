# Phase 2 Test Report

## New Tests

Command:

```bash
PYTHONPATH=src python3 -m pytest \
  tests/test_architecture_generator.py \
  tests/test_architecture_mutation.py \
  tests/test_architecture_normalizer.py \
  tests/test_candidate_manager.py \
  tests/test_architecture_compiler_pipeline.py \
  tests/test_architecture_reproducibility.py -q
```

Result: `36 passed`

Coverage:

- bounded generation and deterministic seeds
- paper-template derivation lineage
- node, connection, and depth mutation validity
- canonicalisation and structural deduplication
- candidate save/load round-trip
- generator-to-compiler pipeline
- reproducibility across generator, mutator, and compiler

## Broad Regression

Command:

```bash
PYTHONPATH=src python3 -m pytest tests -q --ignore=tests/test_hf_data.py
```

Result: `157 passed`

## Full-Suite Known Issue

Running the full suite without the ignore still hits the pre-existing
environment collection error in `tests/test_hf_data.py`:

```text
ImportError: pyarrow requires NumPy 2.0 or newer, found 1.26.4
```

This is unrelated to Phase 2 and existed before this phase.
