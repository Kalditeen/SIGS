# Solver limitations

## What this run can and cannot conclude

- Solver failure or an inconsistent augmented system does not prove
  that no non-degenerate BBM solution exists.
- Groebner is attempted only when the augmented equations are polynomial
  in the network parameters and the auxiliary variable q.
- Saturation ideals are not exposed directly by the current SymPy path;
  the auxiliary-equation method is the recorded substitute.
- No numerical near-zero check is accepted as an exact-solution proof.

| expression | active status | polynomial | groebner |
|---|---|---|---|
| sech(z)**2 | no_solution | True | computed |
| tan(z)**2 | no_solution | True | computed |
| JacobiCN(z,m)**2 | no_solution | True | computed |
| sech(z)**2|tan(z)**2 | no_solution | True | computed |
| JacobiCN(z,m)**2|sech(z)**2 | no_solution | True | computed |
| JacobiCN(z,m)**2|tan(z)**2 | no_solution | True | computed |
| JacobiDN(z, m) + sech(z)**2 | no_solution | True | computed |
| tanh(csch(z)) | no_solution | True | computed |
| z**2 + tanh(alpha*z) | no_solution | True | computed |
| cos(z)*tanh(z) | no_solution | True | computed |
| JacobiDN(z, m) + sech(z)**2|tanh(csch(z)) | no_solution | True | computed |
| JacobiDN(z, m) + sech(z)**2|z**2 + tanh(alpha*z) | no_solution | True | computed |
