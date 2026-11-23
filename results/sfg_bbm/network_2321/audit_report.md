# SFG + NNSCA [2, 3, 2, 1] BBM audit report

## 1. Exact-solution audit

- generated candidates: 3
- unique candidates after structural dedup: 3
- candidates with symbolic analysis success: 3
- candidates with constraint extraction success: 0
- candidates with solver success: 0
- verified exact branches (before equivalence): 0
- verified exact candidates: 0
- distinct exact solutions after equivalence: 0

## 2. Branch verification

## 3. Equivalence

The two JacobiCN**2 branches differ only by a phase sign, and
JacobiCN is even, so they represent the same solution family.
Reflection-equivalent branches are grouped by ``equivalence_key``.

## 4. Source-type split

- seed candidates: 0
- generated candidates: 3

## 5. Candidate quality

- category distribution: {'special': 1, 'hyperbolic': 2}
- depth distribution: {1: 2, 2: 1}
- node count range: 3..8
- complexity range: 2..4
- third-derivative success: 3/3

## 6. Failure stages

{'symbolic_unresolved': 3}

## 7. Conclusion

All currently reported EXACT branches pass the independent raw-residual
check. The main bottleneck is symbolic solving/verification of generated
non-travelling-wave candidates, not the SFG atom library itself.

Next-stage priority should therefore be constraint extraction and
phase/basis handling before expanding the SFG atom library.
