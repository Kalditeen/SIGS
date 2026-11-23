# Phase-4 failure analysis

| expression | symbolic | constraint | solve | verification | failure |
|---|---|---|---|---|---|
| sech(z)**2 | success | success | success | EXACT_VERIFIED |  |
| tan(z)**2 | success | success | success | EXACT_VERIFIED |  |
| JacobiCN(z,m)**2 | success | success | success | EXACT_VERIFIED |  |
| sech(z)**2|tan(z)**2 | success | success | success | EXACT_VERIFIED |  |
| JacobiCN(z,m)**2|sech(z)**2 | success | success | success | EXACT_VERIFIED |  |
| JacobiCN(z,m)**2|tan(z)**2 | success | success | success | EXACT_VERIFIED |  |
| func_0001 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0002 | success | success | success | EXACT_VERIFIED |  |
| func_0003 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0004 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0005 | success | success | unsupported | SYMBOLIC_UNRESOLVED | coefficient solve system too large |
| func_0006 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0007 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0008 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0009 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0010 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0011 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0012 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0013 | success | unsupported | skipped | SYMBOLIC_UNRESOLVED | coefficient extraction non-polynomial phase: sqrt(a*x + b*t + d) contains an element of the set of generators. |
| func_0014 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0015 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0016 | success | success | success | EXACT_VERIFIED |  |
| func_0017 | success | success | unsupported | SYMBOLIC_UNRESOLVED | coefficient solve system too large |
| func_0018 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0019 | success | success | success | EXACT_VERIFIED |  |
| func_0020 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0021 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0022 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0023 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0024 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0025 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0026 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0027 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0028 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0029 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| func_0030 | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
