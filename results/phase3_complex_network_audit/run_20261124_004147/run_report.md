# Phase 3-A Automatic Solving Report

Raw Stage2 records are retained in `candidate_results.json`.
Only branches whose raw Gardner residual was symbolically certified
zero are listed as exact.

## Summary

- candidate_total: 6
- status_counts: {'CONSTRAINT_FAILED': 5, 'VERIFICATION_FAILED': 1}
- exact_candidates: 0
- exact_branches: 0
- degeneracy_counts: {'UNKNOWN': 6}
- total_wall_seconds: 179.58479583200096
- category_selection: {'A': {'candidate_id': 'candidate_0057', 'node_count': 1, 'depth': 1, 'activation_names': ['tan'], 'categories': ['A', 'C', 'F']}, 'B': {'candidate_id': 'candidate_0046', 'node_count': 2, 'depth': 1, 'activation_names': ['sech', 'tanh'], 'categories': ['B', 'C', 'F']}, 'C': {'candidate_id': 'candidate_0002', 'node_count': 5, 'depth': 2, 'activation_names': ['JacobiCN', 'exp', 'sech', 'square', 'tanh'], 'categories': ['C', 'D', 'F']}, 'D': {'candidate_id': 'candidate_0003', 'node_count': 5, 'depth': 2, 'activation_names': ['JacobiCN', 'cosh', 'exp', 'identity', 'square'], 'categories': ['C', 'D', 'F']}, 'E': {'candidate_id': 'candidate_0041', 'node_count': 6, 'depth': 3, 'activation_names': ['JacobiCN', 'cosh', 'exp', 'identity', 'square', 'tanh'], 'categories': ['C', 'D', 'E', 'F']}, 'F': {'candidate_id': 'candidate_0001', 'node_count': 3, 'depth': 1, 'activation_names': ['cosh', 'identity', 'square'], 'categories': ['F']}}
- missing_categories: []

## Candidate Results

| candidate | status | degeneracy | failure |
|---|---|---|---|
| candidate_0001 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0002 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0003 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0041 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0046 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0057 | VERIFICATION_FAILED | UNKNOWN | solver produced branches but none passed independent back-substitution verification |
