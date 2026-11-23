# SFG solver diagnosis

- processed candidates: 30

## Stage counts

| stage | counts |
|---|---|
| symbolic | {'success': 30} |
| constraint | {'success': 29, 'unsupported': 1} |
| extraction | {'success': 29, 'unsupported': 1} |
| solve | {'success': 27, 'unsupported': 2, 'skipped': 1} |
| nontrivial | {'NONE': 24, 'NONTRIVIAL': 3, 'skipped': 3} |
| substitution | {'success': 27, 'skipped': 3} |
| identity | {'skipped': 27, 'verified': 3} |
| verification | {'FAILED': 24, 'EXACT_VERIFIED': 3, 'SYMBOLIC_UNRESOLVED': 3} |

- solve success: 27
- solve success that are EXACT_VERIFIED: 3

## Branch nontrivial statuses

- CONSTANT_TRIVIAL: 40
- DEGENERATE: 27
- NONTRIVIAL: 4

## Failure patterns

- solver_branches_not_exact: 24
- solve_timeout_or_error: 2
- extraction_timeout_or_error: 1
