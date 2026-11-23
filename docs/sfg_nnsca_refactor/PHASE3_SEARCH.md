# Phase 3: SFG Network Search

## Scope

Added `src/sfg/search.py` with `SearchConfig` and `SFGNetworkSearch`.

## Behaviour

- Generates complete `AnsatzCandidate` records.
- Produces single-node baselines and bounded random layered structures.
- Keeps node activations independent.
- Uses deterministic seeds and explicit generation rules.
- Performs structural deduplication by `NetworkStructure.signature()`.
- Keeps all search-space limits in one `SearchConfig` object.

## Compatibility

The old `scripts/pdes/sfg_bbm_21.generate_candidates` entry remains intact for
regression.  It is no longer the architecture's primary structural generator.

## Status

Implemented and covered by focused tests.
