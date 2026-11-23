# SFG + NNSCA [2,1] BBM audit report

## 1. Exact-solution audit

- generated candidates: 100
- unique candidates after structural dedup: 78
- candidates with symbolic analysis success: 78
- candidates with constraint extraction success: 74
- candidates with solver success: 72
- verified exact branches (before equivalence): 7
- verified exact candidates: 4
- distinct exact solutions after equivalence: 4

## 2. Branch verification

### func_0007
- status: EXACT_VERIFIED
- source: JacobiDN(z, m)**2
- trial: c0 + c1*JacobiDN(d + t*sqrt(3*c0*c1 - c1**2*m + 2*c1**2 + 3*c1)/6 - x*sqrt(3*c0*c1 - c1**2*m + 2*c1**2 + 3*c1)/(6*c0 - 2*c1*m + 4*c1 + 6), m)**2
- residual: 0
- parameter conditions: []
- domain notes: []

### func_0007
- status: EXACT_VERIFIED
- source: JacobiDN(z, m)**2
- trial: c0 + c1*JacobiDN(d - t*sqrt(3*c0*c1 - c1**2*m + 2*c1**2 + 3*c1)/6 + x*sqrt(3*c0*c1 - c1**2*m + 2*c1**2 + 3*c1)/(6*c0 - 2*c1*m + 4*c1 + 6), m)**2
- residual: 0
- parameter conditions: []
- domain notes: []

### func_0055
- status: EXACT_VERIFIED
- source: JacobiSN(z, m)**2
- trial: c0 + c1*JacobiSN(d - x*sqrt(-3*c0*c1*m - c1**2*m - c1**2 - 3*c1*m)/(6*c0*m + 2*c1*m + 2*c1 + 6*m) + t*sqrt(-3*c0*c1*m - c1**2*m - c1**2 - 3*c1*m)/(6*m), m)**2
- residual: 0
- parameter conditions: []
- domain notes: []

### func_0055
- status: EXACT_VERIFIED
- source: JacobiSN(z, m)**2
- trial: c0 + c1*JacobiSN(d + x*sqrt(-3*c0*c1*m - c1**2*m - c1**2 - 3*c1*m)/(6*c0*m + 2*c1*m + 2*c1 + 6*m) - t*sqrt(-3*c0*c1*m - c1**2*m - c1**2 - 3*c1*m)/(6*m), m)**2
- residual: 0
- parameter conditions: []
- domain notes: []

### func_0061
- status: EXACT_VERIFIED
- source: JacobiCN(z, m)**2
- trial: c0 + c1*JacobiCN(d - x*sqrt(3*c0*c1*m + 2*c1**2*m - c1**2 + 3*c1*m)/(6*c0*m + 4*c1*m - 2*c1 + 6*m) + t*sqrt(3*c0*c1*m + 2*c1**2*m - c1**2 + 3*c1*m)/(6*m), m)**2
- residual: 0
- parameter conditions: ['m != 0', 'S = 3*c0*m + 2*c1*m - c1 + 3*m != 0', 'c1*S >= 0 for real a and b']
- domain notes: ['JacobiCN**2 is even, so phase sign reversal gives the same solution.', 'The elliptic parameter is the modulus square m, not the modulus k.']

### func_0061
- status: EXACT_VERIFIED
- source: JacobiCN(z, m)**2
- trial: c0 + c1*JacobiCN(d + x*sqrt(3*c0*c1*m + 2*c1**2*m - c1**2 + 3*c1*m)/(6*c0*m + 4*c1*m - 2*c1 + 6*m) - t*sqrt(3*c0*c1*m + 2*c1**2*m - c1**2 + 3*c1*m)/(6*m), m)**2
- residual: 0
- parameter conditions: ['m != 0', 'S = 3*c0*m + 2*c1*m - c1 + 3*m != 0', 'c1*S >= 0 for real a and b']
- domain notes: ['JacobiCN**2 is even, so phase sign reversal gives the same solution.', 'The elliptic parameter is the modulus square m, not the modulus k.']

### func_0082
- status: EXACT_VERIFIED
- source: tan(z)**2
- trial: c1*tan(a*x + d + c1*t/(12*a))**2 + 2*c1/3 - 1 - c1/(12*a**2)
- residual: 0
- parameter conditions: ['a != 0', 'c1 != 0']
- domain notes: ['tan**2 has poles where cos(phase)=0, i.e. phase != pi/2 + k*pi;', 'the solution is valid only on intervals avoiding those poles.']

## 3. Equivalence

The two JacobiCN**2 branches differ only by a phase sign, and
JacobiCN is even, so they represent the same solution family.
Reflection-equivalent branches are grouped by ``equivalence_key``.

## 4. Source-type split

- seed candidates: 0
- generated candidates: 100

## 5. Candidate quality

- category distribution: {'hyperbolic': 44, 'special': 14, 'elementary': 20}
- depth distribution: {2: 17, 1: 57, 0: 4}
- node count range: 2..8
- complexity range: 1..5
- third-derivative success: 78/78

## 6. Failure stages

{'verification_failed': 68, 'verified': 4, 'symbolic_unresolved': 6}

## 7. Conclusion

All currently reported EXACT branches pass the independent raw-residual
check. The main bottleneck is symbolic solving/verification of generated
non-travelling-wave candidates, not the SFG atom library itself.

Next-stage priority should therefore be constraint extraction and
phase/basis handling before expanding the SFG atom library.
