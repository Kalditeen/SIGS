# Gardner failure analysis

`solve_status=success` is not the same as finding a PDE solution. It
means SymPy returned parameter branches for the extracted coefficient
system.  The rows below failed later stages.

| candidate | network | symbolic | constraint | solve | verification | failure |
|---|---|---|---|---|---|---|
| sech(z)**2 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tan(z)**2 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(z) | [2, 2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| sech(z)**2 | [2, 2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(z) | [2, 2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| sech(z)**2|tanh(z) | [2, 2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| JacobiCN(z, m)**2|sech(z)**2 | [2, 2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| JacobiDN(z, m) + sech(z)**2 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(csch(z)) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| z**2 + tanh(alpha*z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| cos(z)*tanh(z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| log(z) + exp(-z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| z**6 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| exp(-2*z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(exp(-z**2)) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| exp(-z)*cosh(z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| cosh(z)**2 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(alpha*z)**2 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(sinh(z)) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| exp(-z)*csch(z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tan(z)*JacobiSN(z, m) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tan(z)**2 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| z + log(z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| z**2 + cosh(z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| z**3 + log(z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| sinh(z)**2 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(sin(z)*cosh(z)) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| exp(2*z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(sech(z)**2) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| JacobiCN(z, m)**2 | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| tanh(tanh(alpha*z)) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |
| exp(z) + tanh(alpha*z) | [2, 1] | success | success | success | FAILED | solver produced branches but none passed independent back-substitution verification |

## Other failures

| candidate | network | solve status | verification | failure |
|---|---|---|---|---|
| JacobiCN(z,m) | [2, 1] | timeout | SYMBOLIC_UNRESOLVED | coefficient solve timeout |
| tanh(z) | [2, 3, 1] | unsupported | SYMBOLIC_UNRESOLVED | coefficient solve system too large |
| tanh(z) | [2, 3, 2, 1] | unsupported | SYMBOLIC_UNRESOLVED | coefficient solve system too large |
| 2*JacobiDN(z, m) | [2, 1] | timeout | SYMBOLIC_UNRESOLVED | coefficient solve timeout |
