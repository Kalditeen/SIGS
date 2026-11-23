# SFG + NNSCA [2,1] BBM audit report

## 1. Exact-solution audit

- generated candidates: 30
- unique candidates after structural dedup: 30
- candidates with symbolic analysis success: 30
- candidates with constraint extraction success: 29
- candidates with solver success: 27
- verified exact branches (before equivalence): 4
- verified exact candidates: 3
- distinct exact solutions after equivalence: 3

## 2. Branch verification

### func_0002
- status: EXACT_VERIFIED
- source: sech(z)**2
- trial: c1*sech(a*x + d - c1*t/(12*a))**2 - c1/3 - 1 + c1/(12*a**2)
- residual: 0
- parameter conditions: ['a != 0', 'c1 != 0']
- domain notes: ['sech**2 is smooth on the real axis; no pole restriction.']

### func_0016
- status: EXACT_VERIFIED
- source: tan(z)**2
- trial: c1*tan(a*x + d + c1*t/(12*a))**2 + 2*c1/3 - 1 - c1/(12*a**2)
- residual: 0
- parameter conditions: ['a != 0', 'c1 != 0']
- domain notes: ['tan**2 has poles where cos(phase)=0, i.e. phase != pi/2 + k*pi;', 'the solution is valid only on intervals avoiding those poles.']

### func_0019
- status: EXACT_VERIFIED
- source: JacobiCN(z, m)**2
- trial: c0 + c1*JacobiCN(d - x*sqrt(3*c0*c1*m + 2*c1**2*m - c1**2 + 3*c1*m)/(6*c0*m + 4*c1*m - 2*c1 + 6*m) + t*sqrt(3*c0*c1*m + 2*c1**2*m - c1**2 + 3*c1*m)/(6*m), m)**2
- residual: 0
- parameter conditions: ['m != 0', 'S = 3*c0*m + 2*c1*m - c1 + 3*m != 0', 'c1*S >= 0 for real a and b']
- domain notes: ['JacobiCN**2 is even, so phase sign reversal gives the same solution.', 'The elliptic parameter is the modulus square m, not the modulus k.']

### func_0019
- status: EXACT_VERIFIED
- source: JacobiCN(z, m)**2
- trial: c0 + c1*JacobiCN(d + x*sqrt(3*c0*c1*m + 2*c1**2*m - c1**2 + 3*c1*m)/(6*c0*m + 4*c1*m - 2*c1 + 6*m) - t*sqrt(3*c0*c1*m + 2*c1**2*m - c1**2 + 3*c1*m)/(6*m), m)**2
- residual: 0
- parameter conditions: ['m != 0', 'S = 3*c0*m + 2*c1*m - c1 + 3*m != 0', 'c1*S >= 0 for real a and b']
- domain notes: ['JacobiCN**2 is even, so phase sign reversal gives the same solution.', 'The elliptic parameter is the modulus square m, not the modulus k.']

## 3. Equivalence

The two JacobiCN**2 branches differ only by a phase sign, and
JacobiCN is even, so they represent the same solution family.
Reflection-equivalent branches are grouped by ``equivalence_key``.

## 4. Source-type split

- seed candidates: 4
- generated candidates: 26

## 5. Candidate quality

- category distribution: {'hyperbolic': 15, 'elementary': 11, 'special': 4}
- depth distribution: {1: 25, 0: 1, 2: 4}
- node count range: 2..8
- complexity range: 1..5
- third-derivative success: 30/30

## 6. Failure stages

{'verification_failed': 24, 'verified': 3, 'symbolic_unresolved': 3}

## 7. Conclusion

All currently reported EXACT branches pass the independent raw-residual
check. The main bottleneck is symbolic solving/verification of generated
non-travelling-wave candidates, not the SFG atom library itself.

Next-stage priority should therefore be constraint extraction and
phase/basis handling before expanding the SFG atom library.
