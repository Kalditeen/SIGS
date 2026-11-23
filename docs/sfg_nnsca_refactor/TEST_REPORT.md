# Test Report

## New focused suite

```bash
python3 -m pytest tests/test_sfg_nnsca_refactor.py -q
# 13 passed
```

## Existing SFG/Gardner regression suite

```bash
python3 -m pytest \
  tests/test_sfg_bbm_21.py \
  tests/test_sfg_gardner.py \
  tests/test_sfg_gardner_phase2.py \
  tests/test_sfg_gardner_phase3.py \
  tests/test_sfg_gardner_phase4.py -q
# 79 passed
```

## Broad suite excluding known environment failure

```bash
PYTHONPATH=src python3 -m pytest tests -q --ignore=tests/test_hf_data.py
# 105 passed
```

## Full suite

```bash
PYTHONPATH=src python3 -m pytest tests -q
# collection error only in tests/test_hf_data.py:
# pyarrow requires NumPy 2.0 or newer, found 1.26.4
```

This is the pre-existing dependency conflict between `pyproject.toml`
(`numpy<2.0`) and the installed `pyarrow`; it is not caused by the refactor.
