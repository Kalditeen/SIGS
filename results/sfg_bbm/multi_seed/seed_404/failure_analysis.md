# BBM [2,1] failure analysis

Candidates with `solve_status=success` do not automatically satisfy the
original PDE. This file records every downstream stage separately.

## func_0001: z**3*sinh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**7*c1**2
    3*a**6*c1**2
    a*b**6*c1**2
    a*c1**2*d**6
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    3*a*b**5*c1**2
    3*a*c1**2*d**5
    6*a**6*c1**2*d
    6*a**6*b*c1**2
    15*a**2*b**4*c1**2
    15*a**2*c1**2*d**4
    15*a**3*b**4*c1**2
    15*a**3*c1**2*d**4
    15*a**5*b**2*c1**2
    15*a**5*c1**2*d**2
    15*a*b**4*c1**2*d
    15*a*b*c1**2*d**4
    20*a**4*b**3*c1**2
    20*a**4*c1**2*d**3
    30*a**3*b**3*c1**2
    30*a**3*c1**2*d**3
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    30*a**5*b*c1**2*d
    6*a**2*b**5*c1**2
    6*a**2*c1**2*d**5
    6*a*b**5*c1**2*d
    6*a*b*c1**2*d**5
    60*a**4*b*c1**2*d
    15*a*b**2*c1**2*d**4
    15*a*b**4*c1**2*d**2
    20*a*b**3*c1**2*d**3
    30*a**2*b**4*c1**2*d
    30*a**2*b*c1**2*d**4
    30*a*b**2*c1**2*d**3
    30*a*b**3*c1**2*d**2
    60*a**2*b**3*c1**2*d
    60*a**2*b*c1**2*d**3
    60*a**3*b**3*c1**2*d
    60*a**3*b*c1**2*d**3
    60*a**4*b**2*c1**2*d
    60*a**4*b*c1**2*d**2
    90*a**3*b**2*c1**2*d
    90*a**3*b*c1**2*d**2
    60*a**2*b**2*c1**2*d**3
    60*a**2*b**3*c1**2*d**2
    90*a**2*b**2*c1**2*d**2
    90*a**3*b**2*c1**2*d**2
    a**3*c1*(-a**2*b + a*c0 + a + b)
    b**3*c1*(-a**2*b + a*c0 + a + b)
    3*a**2*b*c1*(-a**2*b + a*c0 + a + b)
    3*a**2*c1*(-3*a**2*b + a*c0 + a + b)
    3*a**2*c1*d*(-a**2*b + a*c0 + a + b)
    3*b**2*c1*(-3*a**2*b + a*c0 + a + b)
    3*b**2*c1*d*(-a**2*b + a*c0 + a + b)
    3*a*b**2*c1*(-a**2*b + a*c0 + a + b)
    6*a*b*c1*(-3*a**2*b + a*c0 + a + b)
    6*a*b*c1*d*(-a**2*b + a*c0 + a + b)
    6*a*c1*d*(-3*a**2*b + a*c0 + a + b)
    6*b*c1*d*(-3*a**2*b + a*c0 + a + b)
    c1*d*(-a**2*b*d**2 - 18*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    3*a*c1*(-a**2*b*d**2 - 6*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    3*b*c1*(-a**2*b*d**2 - 6*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    3*c1*(-3*a**2*b*d**2 - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0002: z**3*coth(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -a**7*c1**2
    3*a**6*c1**2
    6*a**5*b*c1
    -18*a**4*b*c1
    -a*b**6*c1**2
    -a*c1**2*d**6
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    18*a**3*b**3*c1
    18*a**4*b**2*c1
    18*a**4*b*c1*d
    3*a*b**5*c1**2
    3*a*c1**2*d**5
    6*a**2*b**4*c1
    -18*a**2*b**3*c1
    -36*a**3*b**2*c1
    -36*a**3*b*c1*d
    -6*a**6*c1**2*d
    -6*a**6*b*c1**2
    15*a**2*b**4*c1**2
    15*a**2*c1**2*d**4
    15*a*b**4*c1**2*d
    15*a*b*c1**2*d**4
    18*a**2*b**3*c1*d
    18*a**3*b*c1*d**2
    30*a**3*b**3*c1**2
    30*a**3*c1**2*d**3
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    36*a**3*b**2*c1*d
    6*a**2*b*c1*d**3
    60*a**4*b*c1**2*d
    -15*a**3*b**4*c1**2
    -15*a**3*c1**2*d**4
    -15*a**5*b**2*c1**2
    -15*a**5*c1**2*d**2
    -18*a**2*b*c1*d**2
    -20*a**4*b**3*c1**2
    -20*a**4*c1**2*d**3
    -30*a**5*b*c1**2*d
    -36*a**2*b**2*c1*d
    -6*a**2*b**5*c1**2
    -6*a**2*c1**2*d**5
    -6*a*b**5*c1**2*d
    -6*a*b*c1**2*d**5
    18*a**2*b**2*c1*d**2
    3*a**2*c1*(a*c0 + a + b)
    3*b**2*c1*(a*c0 + a + b)
    30*a*b**2*c1**2*d**3
    30*a*b**3*c1**2*d**2
    6*a*b*c1*(a*c0 + a + b)
    6*a*c1*d*(a*c0 + a + b)
    6*b*c1*d*(a*c0 + a + b)
    60*a**2*b**3*c1**2*d
    60*a**2*b*c1**2*d**3
    90*a**3*b**2*c1**2*d
    90*a**3*b*c1**2*d**2
    -15*a*b**2*c1**2*d**4
    -15*a*b**4*c1**2*d**2
    -20*a*b**3*c1**2*d**3
    -30*a**2*b**4*c1**2*d
    -30*a**2*b*c1**2*d**4
    -60*a**3*b**3*c1**2*d
    -60*a**3*b*c1**2*d**3
    -60*a**4*b**2*c1**2*d
    -60*a**4*b*c1**2*d**2
    90*a**2*b**2*c1**2*d**2
    -60*a**2*b**2*c1**2*d**3
    -60*a**2*b**3*c1**2*d**2
    -90*a**3*b**2*c1**2*d**2
    -a**3*c1*(2*a**2*b + a*c0 + a + b)
    -b**3*c1*(2*a**2*b + a*c0 + a + b)
    -3*a**2*b*c1*(2*a**2*b + a*c0 + a + b)
    -3*a**2*c1*d*(2*a**2*b + a*c0 + a + b)
    -3*b**2*c1*d*(2*a**2*b + a*c0 + a + b)
    -3*a*b**2*c1*(2*a**2*b + a*c0 + a + b)
    -6*a*b*c1*d*(2*a**2*b + a*c0 + a + b)
    3*c1*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    c1*d*(-2*a**2*b*d**2 + 18*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*a*c1*(-2*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*b*c1*(-2*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0003: tanh(cos(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1
    8*a**2*b*c1
    -2*a**2*b*c1
    -6*a**2*b*c1
    c1*(a**2*b + a*c0 + a + b)
    -c1*(a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0005: z**3*csch(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**5*b*c1
    -a**7*c1**2
    2*a**5*b*c1
    3*a**5*b*c1
    3*a**6*c1**2
    a**2*b**4*c1
    -9*a**4*b*c1
    -a*b**6*c1**2
    -a*c1**2*d**6
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    2*a**2*b**4*c1
    3*a**2*b**4*c1
    3*a**3*b**3*c1
    3*a**4*b**2*c1
    3*a**4*b*c1*d
    3*a*b**5*c1**2
    3*a*c1**2*d**5
    6*a**3*b**3*c1
    6*a**4*b**2*c1
    6*a**4*b*c1*d
    9*a**3*b**3*c1
    9*a**4*b**2*c1
    9*a**4*b*c1*d
    a**2*b*c1*d**3
    -18*a**3*b**2*c1
    -18*a**3*b*c1*d
    -6*a**6*c1**2*d
    -6*a**6*b*c1**2
    -9*a**2*b**3*c1
    12*a**3*b**2*c1*d
    15*a**2*b**4*c1**2
    15*a**2*c1**2*d**4
    15*a*b**4*c1**2*d
    15*a*b*c1**2*d**4
    18*a**3*b**2*c1*d
    2*a**2*b*c1*d**3
    3*a**2*b**3*c1*d
    3*a**2*b*c1*d**3
    3*a**3*b*c1*d**2
    30*a**3*b**3*c1**2
    30*a**3*c1**2*d**3
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    6*a**2*b**3*c1*d
    6*a**3*b**2*c1*d
    6*a**3*b*c1*d**2
    60*a**4*b*c1**2*d
    9*a**2*b**3*c1*d
    9*a**3*b*c1*d**2
    -15*a**3*b**4*c1**2
    -15*a**3*c1**2*d**4
    -15*a**5*b**2*c1**2
    -15*a**5*c1**2*d**2
    -18*a**2*b**2*c1*d
    -20*a**4*b**3*c1**2
    -20*a**4*c1**2*d**3
    -30*a**5*b*c1**2*d
    -6*a**2*b**5*c1**2
    -6*a**2*c1**2*d**5
    -6*a*b**5*c1**2*d
    -6*a*b*c1**2*d**5
    -9*a**2*b*c1*d**2
    -a**3*c1*(a*c0 + a + b)
    -b**3*c1*(a*c0 + a + b)
    3*a**2*b**2*c1*d**2
    3*a**2*c1*(a*c0 + a + b)
    3*b**2*c1*(a*c0 + a + b)
    30*a*b**2*c1**2*d**3
    30*a*b**3*c1**2*d**2
    6*a**2*b**2*c1*d**2
    6*a*b*c1*(a*c0 + a + b)
    6*a*c1*d*(a*c0 + a + b)
    6*b*c1*d*(a*c0 + a + b)
    60*a**2*b**3*c1**2*d
    60*a**2*b*c1**2*d**3
    9*a**2*b**2*c1*d**2
    90*a**3*b**2*c1**2*d
    90*a**3*b*c1**2*d**2
    -15*a*b**2*c1**2*d**4
    -15*a*b**4*c1**2*d**2
    -20*a*b**3*c1**2*d**3
    -30*a**2*b**4*c1**2*d
    -30*a**2*b*c1**2*d**4
    -60*a**3*b**3*c1**2*d
    -60*a**3*b*c1**2*d**3
    -60*a**4*b**2*c1**2*d
    -60*a**4*b*c1**2*d**2
    90*a**2*b**2*c1**2*d**2
    -3*a**2*b*c1*(a*c0 + a + b)
    -3*a**2*c1*d*(a*c0 + a + b)
    -3*b**2*c1*d*(a*c0 + a + b)
    -3*a*b**2*c1*(a*c0 + a + b)
    -6*a*b*c1*d*(a*c0 + a + b)
    -60*a**2*b**2*c1**2*d**3
    -60*a**2*b**3*c1**2*d**2
    -90*a**3*b**2*c1**2*d**2
    3*c1*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    c1*d*(18*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*a*c1*(6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*b*c1*(6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0006: exp(z) + tanh(alpha*z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    a*alpha*c1**2
    -a*alpha*c1**2
    6*a**2*alpha**3*b*c1
    c1*(-a**2*b + a*alpha*c1 + a*c0 + a + b)
    alpha*c1*(2*a**2*alpha**2*b + a*c0 + a + b)
    -alpha*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0008: sin(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a*c1**2
    2*c1*(4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0009: csch(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -2*a*c1**2
    12*a**2*b*c1
    4*a**2*b*c1
    8*a**2*b*c1
    -2*c1*(a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0010: cos(z) + JacobiCN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -a*c1**2
    6*a**2*b*c1*m
    -c1*(a**2*b + a*c0 + a + b)
    -c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0011: z**6
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    6*a**12*c1**2
    6*a*b**11*c1**2
    66*a**11*c1**2*d
    66*a**11*b*c1**2
    1980*a**5*b**7*c1**2
    1980*a**8*b**4*c1**2
    1980*a**8*c1**2*d**4
    2772*a**6*b**6*c1**2
    2772*a**7*b**5*c1**2
    2772*a**7*c1**2*d**5
    330*a**10*b**2*c1**2
    330*a**10*c1**2*d**2
    330*a**3*b**9*c1**2
    66*a**2*b**10*c1**2
    66*a*b**10*c1**2*d
    660*a**10*b*c1**2*d
    990*a**4*b**8*c1**2
    990*a**9*b**3*c1**2
    990*a**9*c1**2*d**3
    13860*a**5*b**6*c1**2*d
    13860*a**7*b**4*c1**2*d
    13860*a**7*b*c1**2*d**4
    16632*a**6*b**5*c1**2*d
    16632*a**6*b*c1**2*d**5
    1980*a*b**7*c1**2*d**4
    2772*a*b**6*c1**2*d**5
    2970*a**3*b**8*c1**2*d
    2970*a**9*b**2*c1**2*d
    2970*a**9*b*c1**2*d**2
    330*a*b**9*c1**2*d**2
    660*a**2*b**9*c1**2*d
    7920*a**4*b**7*c1**2*d
    7920*a**8*b**3*c1**2*d
    7920*a**8*b*c1**2*d**3
    990*a*b**8*c1**2*d**3
    11880*a**3*b**7*c1**2*d**2
    11880*a**8*b**2*c1**2*d**2
    13860*a**2*b**6*c1**2*d**4
    16632*a**2*b**5*c1**2*d**5
    27720*a**3*b**6*c1**2*d**3
    27720*a**4*b**6*c1**2*d**2
    27720*a**7*b**2*c1**2*d**3
    27720*a**7*b**3*c1**2*d**2
    2970*a**2*b**8*c1**2*d**2
    41580*a**3*b**4*c1**2*d**5
    41580*a**3*b**5*c1**2*d**4
    41580*a**5*b**2*c1**2*d**5
    41580*a**5*b**5*c1**2*d**2
    41580*a**6*b**2*c1**2*d**4
    41580*a**6*b**4*c1**2*d**2
    55440*a**4*b**3*c1**2*d**5
    55440*a**4*b**5*c1**2*d**3
    55440*a**6*b**3*c1**2*d**3
    69300*a**4*b**4*c1**2*d**4
    69300*a**5*b**3*c1**2*d**4
    69300*a**5*b**4*c1**2*d**3
    7920*a**2*b**7*c1**2*d**3
    6*a**5*c1*(a*c0 + 462*a*c1*d**6 + a + b)
    6*b**5*c1*(a*c0 + 462*a*c1*d**6 + a + b)
    30*a**4*b*c1*(a*c0 + 462*a*c1*d**6 + a + b)
    30*a**4*c1*d*(a*c0 + 66*a*c1*d**6 + a + b)
    30*b**4*c1*d*(a*c0 + 66*a*c1*d**6 + a + b)
    30*a*b**4*c1*(a*c0 + 462*a*c1*d**6 + a + b)
    120*a**3*b*c1*d*(a*c0 + 66*a*c1*d**6 + a + b)
    120*a*b**3*c1*d*(a*c0 + 66*a*c1*d**6 + a + b)
    60*a**2*b**3*c1*(a*c0 + 462*a*c1*d**6 + a + b)
    60*a**3*b**2*c1*(a*c0 + 462*a*c1*d**6 + a + b)
    180*a**2*b**2*c1*d*(a*c0 + 66*a*c1*d**6 + a + b)
    6*c1*d**3*(-20*a**2*b + a*c0*d**2 + a*c1*d**8 + a*d**2 + b*d**2)
    30*a**3*c1*(-4*a**2*b + 2*a*c0*d**2 + 33*a*c1*d**8 + 2*a*d**2 + 2*b*d**2)
    30*b**3*c1*(-4*a**2*b + 2*a*c0*d**2 + 33*a*c1*d**8 + 2*a*d**2 + 2*b*d**2)
    30*a**2*c1*d*(-12*a**2*b + 2*a*c0*d**2 + 11*a*c1*d**8 + 2*a*d**2 + 2*b*d**2)
    30*b**2*c1*d*(-12*a**2*b + 2*a*c0*d**2 + 11*a*c1*d**8 + 2*a*d**2 + 2*b*d**2)
    6*a*c1*d**2*(-60*a**2*b + 5*a*c0*d**2 + 11*a*c1*d**8 + 5*a*d**2 + 5*b*d**2)
    6*b*c1*d**2*(-60*a**2*b + 5*a*c0*d**2 + 11*a*c1*d**8 + 5*a*d**2 + 5*b*d**2)
    60*a*b*c1*d*(-12*a**2*b + 2*a*c0*d**2 + 11*a*c1*d**8 + 2*a*d**2 + 2*b*d**2)
    90*a**2*b*c1*(-4*a**2*b + 2*a*c0*d**2 + 33*a*c1*d**8 + 2*a*d**2 + 2*b*d**2)
    90*a*b**2*c1*(-4*a**2*b + 2*a*c0*d**2 + 33*a*c1*d**8 + 2*a*d**2 + 2*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0013: sin(alpha*z) + cosh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    a*alpha*c1**2
    c1*(-a**2*b + a*c0 + a + b)
    alpha*c1*(a**2*alpha**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0014: tanh(csch(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    a**2*b*c1
    -a**2*b*c1
    2*a**2*b*c1
    3*a**2*b*c1
    6*a**2*b*c1
    8*a**2*b*c1
    c1*(a*c0 + a + b)
    -2*a**2*b*c1
    -3*a**2*b*c1
    -6*a**2*b*c1
    -c1*(a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0017: z**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a**4*c1**2
    2*a*b**3*c1**2
    6*a**3*c1**2*d
    6*a**3*b*c1**2
    12*a**2*b*c1**2*d
    6*a**2*b**2*c1**2
    6*a*b**2*c1**2*d
    2*c1*d*(a*c0 + a*c1*d**2 + a + b)
    2*a*c1*(a*c0 + 3*a*c1*d**2 + a + b)
    2*b*c1*(a*c0 + 3*a*c1*d**2 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0019: tanh(tanh(alpha*z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*alpha*c1**2
    -a*alpha*c1**2
    12*a**2*alpha**3*b*c1
    18*a**2*alpha**3*b*c1
    24*a**2*alpha**3*b*c1
    6*a**2*alpha**3*b*c1
    8*a**2*alpha**3*b*c1
    -12*a**2*alpha**3*b*c1
    -18*a**2*alpha**3*b*c1
    -2*a**2*alpha**3*b*c1
    -24*a**2*alpha**3*b*c1
    -30*a**2*alpha**3*b*c1
    -6*a**2*alpha**3*b*c1
    alpha*c1*(32*a**2*alpha**2*b + a*c0 + a + b)
    alpha*c1*(4*a**2*alpha**2*b + a*c0 + a + b)
    -alpha*c1*(10*a**2*alpha**2*b + a*c0 + a + b)
    -alpha*c1*(14*a**2*alpha**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0020: tanh(JacobiSN(z, m))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1
    12*a**2*b*c1*m
    2*a**2*b*c1*m
    6*a**2*b*c1*m
    -12*a**2*b*c1*m
    -8*a**2*b*c1*m
    6*a**2*b*c1*(m + 1)
    -6*a**2*b*c1*(m + 1)
    2*a**2*b*c1*(7*m + 4)
    -2*a**2*b*c1*(4*m + 1)
    c1*(a**2*b*m + 3*a**2*b + a*c0 + a + b)
    -c1*(a**2*b*m + 9*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0021: exp(-2*z**2)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    64*a**5*b*c1
    -4*a**2*c1**2
    -4*a*c1**2*d
    -4*a*b*c1**2
    192*a**3*b**3*c1
    192*a**4*b**2*c1
    192*a**4*b*c1*d
    64*a**2*b**4*c1
    192*a**2*b**3*c1*d
    384*a**3*b**2*c1*d
    4*a*c1*(48*a**2*b*d**2 - 12*a**2*b - a*c0 - a - b)
    4*b*c1*(48*a**2*b*d**2 - 12*a**2*b - a*c0 - a - b)
    4*c1*d*(16*a**2*b*d**2 - 12*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0022: log(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a**4*c1**2
    6*a**3*b*c1
    2*a*b**3*c1**2
    2*a*c1**2*d**3
    6*a**2*b**2*c1
    6*a**2*b*c1*d
    6*a**3*c1**2*d
    6*a**3*b*c1**2
    12*a**2*b*c1**2*d
    6*a**2*b**2*c1**2
    6*a**2*c1**2*d**2
    6*a*b**2*c1**2*d
    6*a*b*c1**2*d**2
    2*a**3*c1*(a*c0 + a + b)
    2*b**3*c1*(a*c0 + a + b)
    12*a*b*c1*d*(a*c0 + a + b)
    6*a**2*b*c1*(a*c0 + a + b)
    6*a**2*c1*d*(a*c0 + a + b)
    6*b**2*c1*d*(a*c0 + a + b)
    6*a*b**2*c1*(a*c0 + a + b)
    2*c1*d*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    2*a*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    2*b*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0023: exp(-z)*coth(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -a*c1**2
    6*a**2*b*c1
    c1*(a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0025: tanh(tanh(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    12*a**2*b*c1
    18*a**2*b*c1
    24*a**2*b*c1
    6*a**2*b*c1
    8*a**2*b*c1
    -12*a**2*b*c1
    -18*a**2*b*c1
    -2*a**2*b*c1
    -24*a**2*b*c1
    -30*a**2*b*c1
    -6*a**2*b*c1
    c1*(32*a**2*b + a*c0 + a + b)
    c1*(4*a**2*b + a*c0 + a + b)
    -c1*(10*a**2*b + a*c0 + a + b)
    -c1*(14*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0026: cosh(z)/z
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**9*c1**2
    -a**8*c1**2
    a*b**8*c1**2
    a*c1**2*d**8
    -a*b**7*c1**2
    -a*c1**2*d**7
    8*a**8*c1**2*d
    8*a**8*b*c1**2
    -7*a**7*c1**2*d
    -7*a**7*b*c1**2
    28*a**3*b**6*c1**2
    28*a**3*c1**2*d**6
    28*a**7*b**2*c1**2
    28*a**7*c1**2*d**2
    56*a**4*b**5*c1**2
    56*a**4*c1**2*d**5
    56*a**6*b**3*c1**2
    56*a**6*c1**2*d**3
    56*a**7*b*c1**2*d
    70*a**5*b**4*c1**2
    70*a**5*c1**2*d**4
    8*a**2*b**7*c1**2
    8*a**2*c1**2*d**7
    8*a*b**7*c1**2*d
    8*a*b*c1**2*d**7
    -21*a**3*b**5*c1**2
    -21*a**3*c1**2*d**5
    -21*a**6*b**2*c1**2
    -21*a**6*c1**2*d**2
    -35*a**4*b**4*c1**2
    -35*a**4*c1**2*d**4
    -35*a**5*b**3*c1**2
    -35*a**5*c1**2*d**3
    -42*a**6*b*c1**2*d
    -7*a**2*b**6*c1**2
    -7*a**2*c1**2*d**6
    -7*a*b**6*c1**2*d
    -7*a*b*c1**2*d**6
    168*a**3*b**5*c1**2*d
    168*a**3*b*c1**2*d**5
    168*a**6*b**2*c1**2*d
    168*a**6*b*c1**2*d**2
    28*a*b**2*c1**2*d**6
    28*a*b**6*c1**2*d**2
    280*a**4*b**4*c1**2*d
    280*a**4*b*c1**2*d**4
    280*a**5*b**3*c1**2*d
    280*a**5*b*c1**2*d**3
    56*a**2*b**6*c1**2*d
    56*a**2*b*c1**2*d**6
    56*a*b**3*c1**2*d**5
    56*a*b**5*c1**2*d**3
    70*a*b**4*c1**2*d**4
    -105*a**3*b**4*c1**2*d
    -105*a**3*b*c1**2*d**4
    -105*a**5*b**2*c1**2*d
    -105*a**5*b*c1**2*d**2
    -140*a**4*b**3*c1**2*d
    -140*a**4*b*c1**2*d**3
    -21*a*b**2*c1**2*d**5
    -21*a*b**5*c1**2*d**2
    -35*a*b**3*c1**2*d**4
    -35*a*b**4*c1**2*d**3
    -42*a**2*b**5*c1**2*d
    -42*a**2*b*c1**2*d**5
    168*a**2*b**2*c1**2*d**5
    168*a**2*b**5*c1**2*d**2
    280*a**2*b**3*c1**2*d**4
    280*a**2*b**4*c1**2*d**3
    420*a**3*b**2*c1**2*d**4
    420*a**3*b**4*c1**2*d**2
    420*a**5*b**2*c1**2*d**2
    560*a**3*b**3*c1**2*d**3
    560*a**4*b**2*c1**2*d**3
    560*a**4*b**3*c1**2*d**2
    -105*a**2*b**2*c1**2*d**4
    -105*a**2*b**4*c1**2*d**2
    -140*a**2*b**3*c1**2*d**3
    -210*a**3*b**2*c1**2*d**3
    -210*a**3*b**3*c1**2*d**2
    -210*a**4*b**2*c1**2*d**2
    a**9*c1*(-a**2*b + a*c0 + a + b)
    b**9*c1*(-a**2*b + a*c0 + a + b)
    a**8*c1*(3*a**2*b - a*c0 - a - b)
    b**8*c1*(3*a**2*b - a*c0 - a - b)
    9*a**8*b*c1*(-a**2*b + a*c0 + a + b)
    9*a**8*c1*d*(-a**2*b + a*c0 + a + b)
    9*b**8*c1*d*(-a**2*b + a*c0 + a + b)
    9*a*b**8*c1*(-a**2*b + a*c0 + a + b)
    126*a**4*b**5*c1*(-a**2*b + a*c0 + a + b)
    126*a**5*b**4*c1*(-a**2*b + a*c0 + a + b)
    36*a**2*b**7*c1*(-a**2*b + a*c0 + a + b)
    36*a**7*b**2*c1*(-a**2*b + a*c0 + a + b)
    72*a**7*b*c1*d*(-a**2*b + a*c0 + a + b)
    72*a*b**7*c1*d*(-a**2*b + a*c0 + a + b)
    8*a**7*b*c1*(3*a**2*b - a*c0 - a - b)
    8*a**7*c1*d*(3*a**2*b - a*c0 - a - b)
    8*b**7*c1*d*(3*a**2*b - a*c0 - a - b)
    8*a*b**7*c1*(3*a**2*b - a*c0 - a - b)
    84*a**3*b**6*c1*(-a**2*b + a*c0 + a + b)
    84*a**6*b**3*c1*(-a**2*b + a*c0 + a + b)
    252*a**2*b**6*c1*d*(-a**2*b + a*c0 + a + b)
    252*a**6*b**2*c1*d*(-a**2*b + a*c0 + a + b)
    28*a**2*b**6*c1*(3*a**2*b - a*c0 - a - b)
    28*a**6*b**2*c1*(3*a**2*b - a*c0 - a - b)
    504*a**3*b**5*c1*d*(-a**2*b + a*c0 + a + b)
    504*a**5*b**3*c1*d*(-a**2*b + a*c0 + a + b)
    56*a**3*b**5*c1*(3*a**2*b - a*c0 - a - b)
    56*a**5*b**3*c1*(3*a**2*b - a*c0 - a - b)
    56*a**6*b*c1*d*(3*a**2*b - a*c0 - a - b)
    56*a*b**6*c1*d*(3*a**2*b - a*c0 - a - b)
    630*a**4*b**4*c1*d*(-a**2*b + a*c0 + a + b)
    70*a**4*b**4*c1*(3*a**2*b - a*c0 - a - b)
    168*a**2*b**5*c1*d*(3*a**2*b - a*c0 - a - b)
    168*a**5*b**2*c1*d*(3*a**2*b - a*c0 - a - b)
    280*a**3*b**4*c1*d*(3*a**2*b - a*c0 - a - b)
    280*a**4*b**3*c1*d*(3*a**2*b - a*c0 - a - b)
    c1*d**7*(-a**2*b*d**2 - 6*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    c1*d**6*(3*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    126*a**5*c1*d**2*(-a**2*b*d**2 - a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    126*b**5*c1*d**2*(-a**2*b*d**2 - a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    630*a**4*b*c1*d**2*(-a**2*b*d**2 - a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    630*a*b**4*c1*d**2*(-a**2*b*d**2 - a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    1260*a**2*b**3*c1*d**2*(-a**2*b*d**2 - a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    1260*a**3*b**2*c1*d**2*(-a**2*b*d**2 - a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    6*a**7*c1*(-6*a**2*b*d**2 - a**2*b + 6*a*c0*d**2 + 6*a*d**2 + 6*b*d**2)
    6*b**7*c1*(-6*a**2*b*d**2 - a**2*b + 6*a*c0*d**2 + 6*a*d**2 + 6*b*d**2)
    2*a**6*c1*(42*a**2*b*d**2 + 3*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    2*b**6*c1*(42*a**2*b*d**2 + 3*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    42*a**6*b*c1*(-6*a**2*b*d**2 - a**2*b + 6*a*c0*d**2 + 6*a*d**2 + 6*b*d**2)
    42*a**6*c1*d*(-2*a**2*b*d**2 - a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    42*b**6*c1*d*(-2*a**2*b*d**2 - a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    42*a*b**6*c1*(-6*a**2*b*d**2 - a**2*b + 6*a*c0*d**2 + 6*a*d**2 + 6*b*d**2)
    12*a**5*b*c1*(42*a**2*b*d**2 + 3*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    12*a*b**5*c1*(42*a**2*b*d**2 + 3*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    126*a**2*b**5*c1*(-6*a**2*b*d**2 - a**2*b + 6*a*c0*d**2 + 6*a*d**2 + 6*b*d**2)
    126*a**5*b**2*c1*(-6*a**2*b*d**2 - a**2*b + 6*a*c0*d**2 + 6*a*d**2 + 6*b*d**2)
    210*a**3*b**4*c1*(-6*a**2*b*d**2 - a**2*b + 6*a*c0*d**2 + 6*a*d**2 + 6*b*d**2)
    210*a**4*b**3*c1*(-6*a**2*b*d**2 - a**2*b + 6*a*c0*d**2 + 6*a*d**2 + 6*b*d**2)
    252*a**5*b*c1*d*(-2*a**2*b*d**2 - a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    252*a*b**5*c1*d*(-2*a**2*b*d**2 - a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    3*a*c1*d**6*(-3*a**2*b*d**2 - 14*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    3*b*c1*d**6*(-3*a**2*b*d**2 - 14*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    4*a**5*c1*d*(42*a**2*b*d**2 + 9*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    4*b**5*c1*d*(42*a**2*b*d**2 + 9*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    4*a*c1*d**5*(6*a**2*b*d**2 + 9*a**2*b - 2*a*c0*d**2 - 2*a*d**2 - 2*b*d**2)
    4*b*c1*d**5*(6*a**2*b*d**2 + 9*a**2*b - 2*a*c0*d**2 - 2*a*d**2 - 2*b*d**2)
    10*a**4*c1*d**2*(21*a**2*b*d**2 + 9*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
    10*b**4*c1*d**2*(21*a**2*b*d**2 + 9*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
    18*a**2*c1*d**5*(-2*a**2*b*d**2 - 7*a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    18*b**2*c1*d**5*(-2*a**2*b*d**2 - 7*a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    2*a**2*c1*d**4*(42*a**2*b*d**2 + 45*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    2*b**2*c1*d**4*(42*a**2*b*d**2 + 45*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    20*a**4*b*c1*d*(42*a**2*b*d**2 + 9*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    20*a*b**4*c1*d*(42*a**2*b*d**2 + 9*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    30*a**2*b**4*c1*(42*a**2*b*d**2 + 3*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    30*a**4*b**2*c1*(42*a**2*b*d**2 + 3*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    36*a*b*c1*d**5*(-2*a**2*b*d**2 - 7*a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    4*a*b*c1*d**4*(42*a**2*b*d**2 + 45*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    40*a**3*b**3*c1*(42*a**2*b*d**2 + 3*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    42*a**3*c1*d**4*(-2*a**2*b*d**2 - 5*a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    42*a**4*c1*d**3*(-3*a**2*b*d**2 - 5*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    42*b**3*c1*d**4*(-2*a**2*b*d**2 - 5*a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    42*b**4*c1*d**3*(-3*a**2*b*d**2 - 5*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    630*a**2*b**4*c1*d*(-2*a**2*b*d**2 - a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    630*a**4*b**2*c1*d*(-2*a**2*b*d**2 - a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    8*a**3*c1*d**3*(21*a**2*b*d**2 + 15*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
    8*b**3*c1*d**3*(21*a**2*b*d**2 + 15*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
    840*a**3*b**3*c1*d*(-2*a**2*b*d**2 - a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    126*a**2*b*c1*d**4*(-2*a**2*b*d**2 - 5*a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    126*a*b**2*c1*d**4*(-2*a**2*b*d**2 - 5*a**2*b + 2*a*c0*d**2 + 2*a*d**2 + 2*b*d**2)
    168*a**3*b*c1*d**3*(-3*a**2*b*d**2 - 5*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    168*a*b**3*c1*d**3*(-3*a**2*b*d**2 - 5*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    24*a**2*b*c1*d**3*(21*a**2*b*d**2 + 15*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
    24*a*b**2*c1*d**3*(21*a**2*b*d**2 + 15*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
    40*a**2*b**3*c1*d*(42*a**2*b*d**2 + 9*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    40*a**3*b**2*c1*d*(42*a**2*b*d**2 + 9*a**2*b - 14*a*c0*d**2 - 14*a*d**2 - 14*b*d**2)
    40*a**3*b*c1*d**2*(21*a**2*b*d**2 + 9*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
    40*a*b**3*c1*d**2*(21*a**2*b*d**2 + 9*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
    252*a**2*b**2*c1*d**3*(-3*a**2*b*d**2 - 5*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    60*a**2*b**2*c1*d**2*(21*a**2*b*d**2 + 9*a**2*b - 7*a*c0*d**2 - 7*a*d**2 - 7*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0027: tan(z)*coth(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1
    -6*a**2*b*c1
    c1*(-2*a**2*b + a*c0 + a + b)
    c1*(-8*a**2*b + a*c0 + a + b)
    c1*(4*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0030: sin(z)*cosh(z) + sin(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    2*a*c1**2
    c1*(a**2*b + a*c0 + a + b)
    c1*(-2*a**2*b + a*c0 + a + b)
    c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0031: z + tanh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -a*c1**2
    2*a*c1**2
    -a**2*c1**2
    -a*b*c1**2
    2*a**2*c1**2
    2*a*b*c1**2
    6*a**2*b*c1
    2*c1*(a**2*b + a*c0 + a*c1*d + a + b)
    -c1*(8*a**2*b + a*c0 + a*c1*d + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0032: z**3*sech(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    3*a**6*c1**2
    4*a**7*c1**2
    -2*a**7*c1**2
    -6*a**6*c1**2
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    24*a**6*c1**2*d
    24*a**6*b*c1**2
    3*a*b**5*c1**2
    4*a*b**6*c1**2
    -12*a**6*c1**2*d
    -12*a**6*b*c1**2
    -2*a*b**6*c1**2
    -30*a**5*c1**2*d
    -30*a**5*b*c1**2
    -6*a*b**5*c1**2
    120*a**5*b*c1**2*d
    15*a**2*b**4*c1**2
    15*a*b**4*c1**2*d
    24*a**2*b**5*c1**2
    24*a*b**5*c1**2*d
    30*a**3*b**3*c1**2
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    60*a**3*b**4*c1**2
    60*a**4*b*c1**2*d
    60*a**5*b**2*c1**2
    60*a**5*c1**2*d**2
    80*a**4*b**3*c1**2
    -12*a**2*b**5*c1**2
    -12*a*b**5*c1**2*d
    -120*a**4*b*c1**2*d
    -30*a**2*b**4*c1**2
    -30*a**3*b**4*c1**2
    -30*a**5*b**2*c1**2
    -30*a**5*c1**2*d**2
    -30*a*b**4*c1**2*d
    -40*a**4*b**3*c1**2
    -60*a**3*b**3*c1**2
    -60*a**4*b**2*c1**2
    -60*a**4*c1**2*d**2
    -60*a**5*b*c1**2*d
    120*a**2*b**4*c1**2*d
    240*a**3*b**3*c1**2*d
    240*a**4*b**2*c1**2*d
    240*a**4*b*c1**2*d**2
    30*a*b**3*c1**2*d**2
    60*a**2*b**3*c1**2*d
    60*a*b**4*c1**2*d**2
    90*a**3*b**2*c1**2*d
    90*a**3*b*c1**2*d**2
    -120*a**2*b**3*c1**2*d
    -120*a**3*b**3*c1**2*d
    -120*a**4*b**2*c1**2*d
    -120*a**4*b*c1**2*d**2
    -180*a**3*b**2*c1**2*d
    -180*a**3*b*c1**2*d**2
    -30*a*b**4*c1**2*d**2
    -60*a**2*b**4*c1**2*d
    -60*a*b**3*c1**2*d**2
    240*a**2*b**3*c1**2*d**2
    360*a**3*b**2*c1**2*d**2
    90*a**2*b**2*c1**2*d**2
    -120*a**2*b**3*c1**2*d**2
    -180*a**2*b**2*c1**2*d**2
    -180*a**3*b**2*c1**2*d**2
    3*a*c1*d**2*(18*a*b + c1*d**3)
    6*a**3*c1*(9*a*b + 5*c1*d**3)
    -2*a*c1*d**3*(12*a*b + c1*d**3)
    -8*a**4*c1*(3*a*b + 5*c1*d**3)
    12*a**2*b*c1*(9*a*b + 5*c1*d**3)
    3*a**2*c1*d*(36*a*b + 5*c1*d**3)
    3*a*b*c1*d*(36*a*b + 5*c1*d**3)
    6*a*b**2*c1*(9*a*b + 5*c1*d**3)
    -12*a**2*c1*d**2*(6*a*b + c1*d**3)
    -12*a*b*c1*d**2*(6*a*b + c1*d**3)
    -24*a**3*b*c1*(3*a*b + 5*c1*d**3)
    -6*a**3*c1*d*(12*a*b + 5*c1*d**3)
    -8*a*b**3*c1*(3*a*b + 5*c1*d**3)
    -12*a**2*b*c1*d*(12*a*b + 5*c1*d**3)
    -24*a**2*b**2*c1*(3*a*b + 5*c1*d**3)
    -6*a*b**2*c1*d*(12*a*b + 5*c1*d**3)
    2*a**3*c1*(20*a**2*b + a*c0 + 40*a*c1*d**3 + a + b)
    2*b**3*c1*(20*a**2*b + a*c0 + 40*a*c1*d**3 + a + b)
    3*a**2*c1*(6*a**2*b + a*c0 + 10*a*c1*d**3 + a + b)
    3*b**2*c1*(6*a**2*b + a*c0 + 10*a*c1*d**3 + a + b)
    6*a*b*c1*(6*a**2*b + a*c0 + 10*a*c1*d**3 + a + b)
    -2*a**3*c1*(8*a**2*b + a*c0 + 20*a*c1*d**3 + a + b)
    -2*b**3*c1*(8*a**2*b + a*c0 + 20*a*c1*d**3 + a + b)
    -3*a**2*c1*(24*a**2*b + a*c0 + 20*a*c1*d**3 + a + b)
    -3*b**2*c1*(24*a**2*b + a*c0 + 20*a*c1*d**3 + a + b)
    -6*a*b*c1*(24*a**2*b + a*c0 + 20*a*c1*d**3 + a + b)
    -6*a*c1*d*(24*a**2*b + a*c0 + 5*a*c1*d**3 + a + b)
    -6*b*c1*d*(24*a**2*b + a*c0 + 5*a*c1*d**3 + a + b)
    12*a*b*c1*d*(20*a**2*b + a*c0 + 10*a*c1*d**3 + a + b)
    6*a**2*b*c1*(20*a**2*b + a*c0 + 40*a*c1*d**3 + a + b)
    6*a**2*c1*d*(20*a**2*b + a*c0 + 10*a*c1*d**3 + a + b)
    6*b**2*c1*d*(20*a**2*b + a*c0 + 10*a*c1*d**3 + a + b)
    6*a*b**2*c1*(20*a**2*b + a*c0 + 40*a*c1*d**3 + a + b)
    -12*a*b*c1*d*(8*a**2*b + a*c0 + 5*a*c1*d**3 + a + b)
    -6*a**2*b*c1*(8*a**2*b + a*c0 + 20*a*c1*d**3 + a + b)
    -6*a**2*c1*d*(8*a**2*b + a*c0 + 5*a*c1*d**3 + a + b)
    -6*b**2*c1*d*(8*a**2*b + a*c0 + 5*a*c1*d**3 + a + b)
    -6*a*b**2*c1*(8*a**2*b + a*c0 + 20*a*c1*d**3 + a + b)
    3*a*c1*d*(12*a**2*b + 2*a*c0 + 5*a*c1*d**3 + 2*a + 2*b)
    3*b*c1*d*(12*a**2*b + 2*a*c0 + 5*a*c1*d**3 + 2*a + 2*b)
    3*c1*(6*a**2*b*d**2 - 2*a**2*b + a*c0*d**2 + a*c1*d**5 + a*d**2 + b*d**2)
    2*c1*d*(-8*a**2*b*d**2 + 18*a**2*b - a*c0*d**2 - a*c1*d**5 - a*d**2 - b*d**2)
    3*c1*(-24*a**2*b*d**2 + 2*a**2*b - a*c0*d**2 - 2*a*c1*d**5 - a*d**2 - b*d**2)
    2*c1*d*(20*a**2*b*d**2 - 18*a**2*b + a*c0*d**2 + 2*a*c1*d**5 + a*d**2 + b*d**2)
    6*a*c1*(-8*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - 2*a*c1*d**5 - a*d**2 - b*d**2)
    6*a*c1*(20*a**2*b*d**2 - 6*a**2*b + a*c0*d**2 + 4*a*c1*d**5 + a*d**2 + b*d**2)
    6*b*c1*(-8*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - 2*a*c1*d**5 - a*d**2 - b*d**2)
    6*b*c1*(20*a**2*b*d**2 - 6*a**2*b + a*c0*d**2 + 4*a*c1*d**5 + a*d**2 + b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'b': '0', 'd': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'b': '0', 'd': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_s...

## func_0033: log(z)*cosh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**6*c1**2
    a**7*c1**2
    3*a**6*b*c1
    a*b**5*c1**2
    a*b**6*c1**2
    a*c1**2*d**5
    a*c1**2*d**6
    12*a**3*b**4*c1
    12*a**5*b**2*c1
    12*a**5*b*c1*d
    18*a**4*b**3*c1
    3*a**2*b**5*c1
    5*a**5*c1**2*d
    5*a**5*b*c1**2
    6*a**6*c1**2*d
    6*a**6*b*c1**2
    10*a**3*b**3*c1**2
    10*a**3*c1**2*d**3
    10*a**4*b**2*c1**2
    10*a**4*c1**2*d**2
    12*a**2*b**4*c1*d
    12*a**3*b*c1*d**3
    15*a**3*b**4*c1**2
    15*a**3*c1**2*d**4
    15*a**5*b**2*c1**2
    15*a**5*c1**2*d**2
    18*a**4*b*c1*d**2
    20*a**4*b**3*c1**2
    20*a**4*c1**2*d**3
    20*a**4*b*c1**2*d
    3*a**2*b*c1*d**4
    30*a**5*b*c1**2*d
    36*a**3*b**3*c1*d
    36*a**4*b**2*c1*d
    5*a**2*b**4*c1**2
    5*a**2*c1**2*d**4
    5*a*b**4*c1**2*d
    5*a*b*c1**2*d**4
    6*a**2*b**5*c1**2
    6*a**2*c1**2*d**5
    6*a*b**5*c1**2*d
    6*a*b*c1**2*d**5
    10*a*b**2*c1**2*d**3
    10*a*b**3*c1**2*d**2
    12*a**2*b**2*c1*d**3
    15*a*b**2*c1**2*d**4
    15*a*b**4*c1**2*d**2
    18*a**2*b**3*c1*d**2
    20*a**2*b**3*c1**2*d
    20*a**2*b*c1**2*d**3
    20*a*b**3*c1**2*d**3
    30*a**2*b**4*c1**2*d
    30*a**2*b*c1**2*d**4
    30*a**3*b**2*c1**2*d
    30*a**3*b*c1**2*d**2
    36*a**3*b**2*c1*d**2
    60*a**3*b**3*c1**2*d
    60*a**3*b*c1**2*d**3
    60*a**4*b**2*c1**2*d
    60*a**4*b*c1**2*d**2
    30*a**2*b**2*c1**2*d**2
    60*a**2*b**2*c1**2*d**3
    60*a**2*b**3*c1**2*d**2
    90*a**3*b**2*c1**2*d**2
    a**6*c1*(-a**2*b + a*c0 + a + b)
    b**6*c1*(-a**2*b + a*c0 + a + b)
    c1*d**6*(-a**2*b + a*c0 + a + b)
    a**5*c1*(-3*a**2*b + a*c0 + a + b)
    b**5*c1*(-3*a**2*b + a*c0 + a + b)
    6*a**5*b*c1*(-a**2*b + a*c0 + a + b)
    6*a**5*c1*d*(-a**2*b + a*c0 + a + b)
    6*b**5*c1*d*(-a**2*b + a*c0 + a + b)
    6*a*b**5*c1*(-a**2*b + a*c0 + a + b)
    6*a*c1*d**5*(-a**2*b + a*c0 + a + b)
    6*b*c1*d**5*(-a**2*b + a*c0 + a + b)
    15*a**2*b**4*c1*(-a**2*b + a*c0 + a + b)
    15*a**2*c1*d**4*(-a**2*b + a*c0 + a + b)
    15*a**4*b**2*c1*(-a**2*b + a*c0 + a + b)
    15*a**4*c1*d**2*(-a**2*b + a*c0 + a + b)
    15*b**2*c1*d**4*(-a**2*b + a*c0 + a + b)
    15*b**4*c1*d**2*(-a**2*b + a*c0 + a + b)
    20*a**3*b**3*c1*(-a**2*b + a*c0 + a + b)
    20*a**3*c1*d**3*(-a**2*b + a*c0 + a + b)
    20*b**3*c1*d**3*(-a**2*b + a*c0 + a + b)
    30*a**4*b*c1*d*(-a**2*b + a*c0 + a + b)
    30*a*b**4*c1*d*(-a**2*b + a*c0 + a + b)
    30*a*b*c1*d**4*(-a**2*b + a*c0 + a + b)
    5*a**4*b*c1*(-3*a**2*b + a*c0 + a + b)
    5*a**4*c1*d*(-3*a**2*b + a*c0 + a + b)
    5*b**4*c1*d*(-3*a**2*b + a*c0 + a + b)
    5*a*b**4*c1*(-3*a**2*b + a*c0 + a + b)
    10*a**2*b**3*c1*(-3*a**2*b + a*c0 + a + b)
    10*a**3*b**2*c1*(-3*a**2*b + a*c0 + a + b)
    20*a**3*b*c1*d*(-3*a**2*b + a*c0 + a + b)
    20*a*b**3*c1*d*(-3*a**2*b + a*c0 + a + b)
    60*a**2*b**3*c1*d*(-a**2*b + a*c0 + a + b)
    60*a**2*b*c1*d**3*(-a**2*b + a*c0 + a + b)
    60*a**3*b**2*c1*d*(-a**2*b + a*c0 + a + b)
    60*a**3*b*c1*d**2*(-a**2*b + a*c0 + a + b)
    60*a*b**2*c1*d**3*(-a**2*b + a*c0 + a + b)
    60*a*b**3*c1*d**2*(-a**2*b + a*c0 + a + b)
    30*a**2*b**2*c1*d*(-3*a**2*b + a*c0 + a + b)
    90*a**2*b**2*c1*d**2*(-a**2*b + a*c0 + a + b)
    c1*d**3*(-3*a**2*b*d**2 - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    2*a**3*c1*(-15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*b**3*c1*(-15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    6*a**2*b*c1*(-15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    6*a*b**2*c1*(-15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    a*c1*d**2*(-15*a**2*b*d**2 - 6*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    b*c1*d**2*(-15*a**2*b*d**2 - 6*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*a**2*c1*d*(-15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*b**2*c1*d*(-15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    4*a*b*c1*d*(-15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0034: tanh(log(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**4*c1**2
    -a**4*c1**2
    6*a**3*b*c1
    a*b**3*c1**2
    -a*b**3*c1**2
    3*a**3*c1**2*d
    3*a**3*b*c1**2
    6*a**2*b**2*c1
    6*a**2*b*c1*d
    -3*a**3*c1**2*d
    -3*a**3*b*c1**2
    3*a**2*b**2*c1**2
    3*a*b**2*c1**2*d
    6*a**2*b*c1**2*d
    a**3*c1*(a*c0 + a + b)
    b**3*c1*(a*c0 + a + b)
    c1*d**3*(a*c0 + a + b)
    -3*a**2*b**2*c1**2
    -3*a*b**2*c1**2*d
    -6*a**2*b*c1**2*d
    -a**3*c1*(a*c0 + a + b)
    -b**3*c1*(a*c0 + a + b)
    3*a**2*b*c1*(a*c0 + a + b)
    3*a**2*c1*d*(a*c0 + a + b)
    3*b**2*c1*d*(a*c0 + a + b)
    3*a*b**2*c1*(a*c0 + a + b)
    3*a*c1*d**2*(a*c0 + a + b)
    3*b*c1*d**2*(a*c0 + a + b)
    6*a*b*c1*d*(a*c0 + a + b)
    a*c1*d*(-6*a*b + c1*d**2)
    a*c1*d*(6*a*b - c1*d**2)
    -3*a**2*b*c1*(a*c0 + a + b)
    -3*a**2*c1*d*(a*c0 + a + b)
    -3*b**2*c1*d*(a*c0 + a + b)
    -3*a*b**2*c1*(a*c0 + a + b)
    -6*a*b*c1*d*(a*c0 + a + b)
    3*a**2*c1*(-2*a*b + c1*d**2)
    3*a**2*c1*(2*a*b - c1*d**2)
    3*a*b*c1*(-2*a*b + c1*d**2)
    3*a*b*c1*(2*a*b - c1*d**2)
    -c1*d*(6*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    -3*a*c1*(2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    -3*b*c1*(2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0036: exp(z) + cosh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    c1*(-a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0037: log(z) + sech(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**4*c1**2
    a**5*c1**2
    -a**5*c1**2
    6*a**6*b*c1
    a*b**3*c1**2
    a*b**4*c1**2
    a*c1**2*d**3
    a*c1**2*d**4
    -a*b**4*c1**2
    -a*c1**2*d**4
    24*a**3*b**4*c1
    24*a**5*b**2*c1
    24*a**5*b*c1*d
    3*a**3*c1**2*d
    3*a**3*b*c1**2
    36*a**4*b**3*c1
    4*a**4*c1**2*d
    4*a**4*b*c1**2
    6*a**2*b**5*c1
    -4*a**4*c1**2*d
    -4*a**4*b*c1**2
    12*a**3*b*c1**2*d
    24*a**2*b**4*c1*d
    24*a**3*b*c1*d**3
    3*a**2*b**2*c1**2
    3*a**2*c1**2*d**2
    3*a*b**2*c1**2*d
    3*a*b*c1**2*d**2
    36*a**4*b*c1*d**2
    4*a**2*b**3*c1**2
    4*a**2*c1**2*d**3
    4*a*b**3*c1**2*d
    4*a*b*c1**2*d**3
    6*a**2*b*c1**2*d
    6*a**2*b*c1*d**4
    6*a**3*b**2*c1**2
    6*a**3*c1**2*d**2
    72*a**3*b**3*c1*d
    72*a**4*b**2*c1*d
    a**3*c1*(a*c0 + a + b)
    b**3*c1*(a*c0 + a + b)
    -12*a**3*b*c1**2*d
    -4*a**2*b**3*c1**2
    -4*a**2*c1**2*d**3
    -4*a*b**3*c1**2*d
    -4*a*b*c1**2*d**3
    -6*a**3*b**2*c1**2
    -6*a**3*c1**2*d**2
    12*a**2*b**2*c1**2*d
    12*a**2*b*c1**2*d**2
    24*a**2*b**2*c1*d**3
    36*a**2*b**3*c1*d**2
    6*a*b**2*c1**2*d**2
    72*a**3*b**2*c1*d**2
    -12*a**2*b**2*c1**2*d
    -12*a**2*b*c1**2*d**2
    -6*a*b**2*c1**2*d**2
    3*a**2*b*c1*(a*c0 + a + b)
    3*a**2*c1*d*(a*c0 + a + b)
    3*b**2*c1*d*(a*c0 + a + b)
    3*a*b**2*c1*(a*c0 + a + b)
    6*a*b*c1*d*(a*c0 + a + b)
    -a**4*c1*(5*a**2*b + a*c0 + a + b)
    -b**4*c1*(5*a**2*b + a*c0 + a + b)
    -c1*d**4*(5*a**2*b + a*c0 + a + b)
    -4*a**3*b*c1*(5*a**2*b + a*c0 + a + b)
    -4*a**3*c1*d*(5*a**2*b + a*c0 + a + b)
    -4*b**3*c1*d*(5*a**2*b + a*c0 + a + b)
    -4*a*b**3*c1*(5*a**2*b + a*c0 + a + b)
    -4*a*c1*d**3*(5*a**2*b + a*c0 + a + b)
    -4*b*c1*d**3*(5*a**2*b + a*c0 + a + b)
    -12*a**2*b*c1*d*(5*a**2*b + a*c0 + a + b)
    -12*a*b**2*c1*d*(5*a**2*b + a*c0 + a + b)
    -12*a*b*c1*d**2*(5*a**2*b + a*c0 + a + b)
    -6*a**2*b**2*c1*(5*a**2*b + a*c0 + a + b)
    -6*a**2*c1*d**2*(5*a**2*b + a*c0 + a + b)
    -6*b**2*c1*d**2*(5*a**2*b + a*c0 + a + b)
    c1*d*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    a*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    b*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0038: cosh(z)*JacobiCN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1*m
    -6*a**2*b*c1*m
    c1*(2*a**2*b + a*c0 + a + b)
    c1*(-4*a**2*b*m + 2*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0040: tanh(sin(alpha*z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*alpha*c1**2
    -a*alpha*c1**2
    2*a**2*alpha**3*b*c1
    6*a**2*alpha**3*b*c1
    -6*a**2*alpha**3*b*c1
    -8*a**2*alpha**3*b*c1
    alpha*c1*(a**2*alpha**2*b + a*c0 + a + b)
    -alpha*c1*(a**2*alpha**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0042: tanh(coth(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    12*a**2*b*c1
    6*a**2*b*c1
    8*a**2*b*c1
    -12*a**2*b*c1
    -2*a**2*b*c1
    -6*a**2*b*c1
    c1*(2*a**2*b + a*c0 + a + b)
    -c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0044: tanh(sech(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    12*a**2*b*c1
    18*a**2*b*c1
    6*a**2*b*c1
    8*a**2*b*c1
    -12*a**2*b*c1
    -18*a**2*b*c1
    -2*a**2*b*c1
    -6*a**2*b*c1
    c1*(5*a**2*b + a*c0 + a + b)
    -c1*(5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0045: tanh(exp(-z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1
    8*a**2*b*c1
    -2*a**2*b*c1
    -6*a**2*b*c1
    c1*(-a**2*b + a*c0 + a + b)
    c1*(a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0046: cosh(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a*c1**2
    2*c1*(-4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0049: z**4
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    4*a**8*c1**2
    28*a**7*c1**2*d
    28*a**7*b*c1**2
    4*a*b**7*c1**2
    140*a**4*b**4*c1**2
    140*a**5*b**3*c1**2
    140*a**5*c1**2*d**3
    168*a**6*b*c1**2*d
    28*a**2*b**6*c1**2
    28*a*b**6*c1**2*d
    84*a**3*b**5*c1**2
    84*a**6*b**2*c1**2
    84*a**6*c1**2*d**2
    140*a*b**4*c1**2*d**3
    168*a**2*b**5*c1**2*d
    420*a**3*b**4*c1**2*d
    420*a**5*b**2*c1**2*d
    420*a**5*b*c1**2*d**2
    560*a**4*b**3*c1**2*d
    560*a**4*b*c1**2*d**3
    84*a*b**5*c1**2*d**2
    420*a**2*b**4*c1**2*d**2
    560*a**2*b**3*c1**2*d**3
    840*a**3*b**2*c1**2*d**3
    840*a**3*b**3*c1**2*d**2
    840*a**4*b**2*c1**2*d**2
    4*a**3*c1*(a*c0 + 35*a*c1*d**4 + a + b)
    4*b**3*c1*(a*c0 + 35*a*c1*d**4 + a + b)
    12*a**2*b*c1*(a*c0 + 35*a*c1*d**4 + a + b)
    12*a**2*c1*d*(a*c0 + 7*a*c1*d**4 + a + b)
    12*b**2*c1*d*(a*c0 + 7*a*c1*d**4 + a + b)
    12*a*b**2*c1*(a*c0 + 35*a*c1*d**4 + a + b)
    24*a*b*c1*d*(a*c0 + 7*a*c1*d**4 + a + b)
    4*c1*d*(-6*a**2*b + a*c0*d**2 + a*c1*d**6 + a*d**2 + b*d**2)
    4*a*c1*(-6*a**2*b + 3*a*c0*d**2 + 7*a*c1*d**6 + 3*a*d**2 + 3*b*d**2)
    4*b*c1*(-6*a**2*b + 3*a*c0*d**2 + 7*a*c1*d**6 + 3*a*d**2 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0050: coth(z)*JacobiSN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1
    -6*a**2*b*c1
    6*a**2*b*c1*m
    -6*a**2*b*c1*m
    c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    -c1*(3*a**2*b*m + 5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0052: exp(-z)*sin(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    c1*(-2*a**2*b + a*c0 + a + b)
    -c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0055: z**2*cos(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -a**5*c1**2
    2*a**4*c1**2
    -a*b**4*c1**2
    -a*c1**2*d**4
    2*a*b**3*c1**2
    2*a*c1**2*d**3
    6*a**3*c1**2*d
    6*a**3*b*c1**2
    -4*a**4*c1**2*d
    -4*a**4*b*c1**2
    12*a**2*b*c1**2*d
    6*a**2*b**2*c1**2
    6*a**2*c1**2*d**2
    6*a*b**2*c1**2*d
    6*a*b*c1**2*d**2
    -12*a**3*b*c1**2*d
    -4*a**2*b**3*c1**2
    -4*a**2*c1**2*d**3
    -4*a*b**3*c1**2*d
    -4*a*b*c1**2*d**3
    -6*a**3*b**2*c1**2
    -6*a**3*c1**2*d**2
    -12*a**2*b**2*c1**2*d
    -12*a**2*b*c1**2*d**2
    -6*a*b**2*c1**2*d**2
    -a**2*c1*(a**2*b + a*c0 + a + b)
    -b**2*c1*(a**2*b + a*c0 + a + b)
    2*a*c1*(3*a**2*b + a*c0 + a + b)
    2*b*c1*(3*a**2*b + a*c0 + a + b)
    2*c1*d*(3*a**2*b + a*c0 + a + b)
    -2*a*b*c1*(a**2*b + a*c0 + a + b)
    -2*a*c1*d*(a**2*b + a*c0 + a + b)
    -2*b*c1*d*(a**2*b + a*c0 + a + b)
    c1*(-a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0056: tanh(sin(z)*cosh(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    12*a**2*b*c1
    18*a**2*b*c1
    2*a**2*b*c1
    6*a**2*b*c1
    -12*a**2*b*c1
    -24*a**2*b*c1
    -8*a**2*b*c1
    c1*(-2*a**2*b + a*c0 + a + b)
    c1*(2*a**2*b - a*c0 - a - b)
    c1*(2*a**2*b + a*c0 + a + b)
    -c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0057: z*JacobiSN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**2*c1**2
    a**3*c1**2
    a*c1**2*d
    a*b*c1**2
    a*b**2*c1**2
    a*c1**2*d**2
    2*a**2*c1**2*d
    2*a**2*b*c1**2
    2*a*b*c1**2*d
    -6*a**2*b*c1*m
    -6*a**3*b*c1*m
    -6*a**2*b**2*c1*m
    -6*a**2*b*c1*d*m
    a*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    b*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    c1*d*(a**2*b*m + a**2*b + a*c0 + a + b)
    c1*(3*a**2*b*m + 3*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0058: sin(alpha*z)*sech(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    a*alpha*c1**2
    -a*alpha*c1**2
    6*a**2*b*c1
    -6*a**2*alpha*b*c1
    alpha*c1*(a**2*alpha**2*b + 3*a**2*b + a*c0 + a + b)
    -c1*(3*a**2*alpha**2*b + 5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0059: tanh(exp(-z**2))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a**2*c1**2
    2*a*c1**2*d
    2*a*b*c1**2
    48*a**5*b*c1
    64*a**5*b*c1
    8*a**5*b*c1
    -16*a**5*b*c1
    -2*a**2*c1**2
    -2*a*c1**2*d
    -2*a*b*c1**2
    -48*a**5*b*c1
    -8*a**5*b*c1
    144*a**3*b**3*c1
    144*a**4*b**2*c1
    144*a**4*b*c1*d
    192*a**3*b**3*c1
    192*a**4*b**2*c1
    192*a**4*b*c1*d
    24*a**3*b**3*c1
    24*a**4*b**2*c1
    24*a**4*b*c1*d
    48*a**2*b**4*c1
    64*a**2*b**4*c1
    8*a**2*b**4*c1
    -144*a**3*b**3*c1
    -144*a**4*b**2*c1
    -144*a**4*b*c1*d
    -16*a**2*b**4*c1
    -24*a**3*b**3*c1
    -24*a**4*b**2*c1
    -24*a**4*b*c1*d
    -48*a**2*b**4*c1
    -48*a**3*b**3*c1
    -48*a**4*b**2*c1
    -48*a**4*b*c1*d
    -8*a**2*b**4*c1
    144*a**2*b**3*c1*d
    192*a**2*b**3*c1*d
    192*a**3*b*c1*d**2
    24*a**2*b**3*c1*d
    288*a**3*b**2*c1*d
    384*a**3*b**2*c1*d
    48*a**3*b**2*c1*d
    64*a**2*b*c1*d**3
    -144*a**2*b**3*c1*d
    -144*a**3*b*c1*d**2
    -16*a**2*b*c1*d**3
    -24*a**2*b**3*c1*d
    -288*a**3*b**2*c1*d
    -48*a**2*b**3*c1*d
    -48*a**2*b*c1*d**3
    -48*a**3*b**2*c1*d
    -48*a**3*b*c1*d**2
    -96*a**3*b**2*c1*d
    192*a**2*b**2*c1*d**2
    -144*a**2*b**2*c1*d**2
    -48*a**2*b**2*c1*d**2
    24*a**3*b*c1*(1 - 6*d**2)
    24*a**3*b*c1*(6*d**2 - 1)
    24*a**2*b**2*c1*(1 - 6*d**2)
    24*a**2*b**2*c1*(6*d**2 - 1)
    24*a**2*b*c1*d*(1 - 2*d**2)
    24*a**2*b*c1*d*(2*d**2 - 1)
    2*a*c1*(-12*a**2*b*d**2 + 6*a**2*b + a*c0 + a + b)
    2*a*c1*(12*a**2*b*d**2 - 6*a**2*b - a*c0 - a - b)
    2*b*c1*(-12*a**2*b*d**2 + 6*a**2*b + a*c0 + a + b)
    2*b*c1*(12*a**2*b*d**2 - 6*a**2*b - a*c0 - a - b)
    2*c1*d*(-4*a**2*b*d**2 + 6*a**2*b + a*c0 + a + b)
    2*c1*d*(4*a**2*b*d**2 - 6*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0062: tanh(z**3)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    108*a**5*b*c1
    162*a**8*b*c1
    54*a**8*b*c1
    -108*a**5*b*c1
    -216*a**8*b*c1
    108*a**2*b**4*c1
    1080*a**5*b**4*c1
    162*a**2*b**7*c1
    2430*a**4*b**5*c1
    2430*a**6*b**3*c1
    324*a**3*b**3*c1
    324*a**3*b**6*c1
    324*a**4*b**2*c1
    324*a**7*b**2*c1
    324*a**7*b*c1*d
    3240*a**5*b**4*c1
    54*a**2*b**7*c1
    810*a**4*b**5*c1
    810*a**6*b**3*c1
    972*a**3*b**6*c1
    972*a**7*b**2*c1
    972*a**7*b*c1*d
    -108*a**2*b**4*c1
    -1296*a**3*b**6*c1
    -1296*a**7*b**2*c1
    -1296*a**7*b*c1*d
    -216*a**2*b**7*c1
    -324*a**3*b**3*c1
    -324*a**4*b**2*c1
    -3240*a**4*b**5*c1
    -3240*a**6*b**3*c1
    -4320*a**5*b**4*c1
    1080*a**5*b*c1*d**3
    162*a**2*b*c1*d**6
    1620*a**3*b**5*c1*d
    1620*a**6*b**2*c1*d
    2430*a**4*b*c1*d**4
    2430*a**6*b*c1*d**2
    324*a**2*b**6*c1*d
    3240*a**4*b**4*c1*d
    3240*a**5*b**3*c1*d
    3240*a**5*b*c1*d**3
    4860*a**3*b**5*c1*d
    4860*a**6*b**2*c1*d
    810*a**6*b*c1*d**2
    972*a**2*b**6*c1*d
    972*a**3*b*c1*d**5
    9720*a**4*b**4*c1*d
    9720*a**5*b**3*c1*d
    -1296*a**2*b**6*c1*d
    -12960*a**4*b**4*c1*d
    -12960*a**5*b**3*c1*d
    -3240*a**6*b*c1*d**2
    -4320*a**5*b*c1*d**3
    -6480*a**3*b**5*c1*d
    -6480*a**6*b**2*c1*d
    1080*a**2*b**4*c1*d**3
    14580*a**4*b**3*c1*d**2
    2430*a**2*b**3*c1*d**4
    2430*a**2*b**5*c1*d**2
    3240*a**2*b**4*c1*d**3
    3240*a**3*b**3*c1*d**3
    3240*a**3*b**4*c1*d**2
    3240*a**4*b**2*c1*d**3
    3240*a**5*b**2*c1*d**2
    4860*a**3*b**2*c1*d**4
    4860*a**4*b**3*c1*d**2
    810*a**2*b**5*c1*d**2
    972*a**2*b**2*c1*d**5
    9720*a**3*b**3*c1*d**3
    9720*a**3*b**4*c1*d**2
    9720*a**4*b**2*c1*d**3
    9720*a**5*b**2*c1*d**2
    -12960*a**3*b**3*c1*d**3
    -12960*a**3*b**4*c1*d**2
    -12960*a**4*b**2*c1*d**3
    -12960*a**5*b**2*c1*d**2
    -19440*a**4*b**3*c1*d**2
    -3240*a**2*b**5*c1*d**2
    -4320*a**2*b**4*c1*d**3
    3*a**3*c1*(108*a*b*d + c1)
    -3*a**3*c1*(108*a*b*d + c1)
    3*a*b**2*c1*(108*a*b*d + c1)
    3*a*c1*d**2*(36*a*b*d + c1)
    6*a**2*b*c1*(108*a*b*d + c1)
    6*a**2*c1*d*(54*a*b*d + c1)
    6*a*b*c1*d*(54*a*b*d + c1)
    -3*a*b**2*c1*(108*a*b*d + c1)
    -3*a*c1*d**2*(36*a*b*d + c1)
    -6*a**2*b*c1*(108*a*b*d + c1)
    -6*a**2*c1*d*(54*a*b*d + c1)
    -6*a*b*c1*d*(54*a*b*d + c1)
    3*a**2*c1*(270*a**2*b*d**4 + a*c0 + a + b)
    3*b**2*c1*(270*a**2*b*d**4 + a*c0 + a + b)
    6*a*b*c1*(270*a**2*b*d**4 + a*c0 + a + b)
    6*a*c1*d*(54*a**2*b*d**4 + a*c0 + a + b)
    6*b*c1*d*(54*a**2*b*d**4 + a*c0 + a + b)
    -3*a**2*c1*(1080*a**2*b*d**4 + a*c0 + a + b)
    -3*b**2*c1*(1080*a**2*b*d**4 + a*c0 + a + b)
    -6*a*b*c1*(1080*a**2*b*d**4 + a*c0 + a + b)
    -6*a*c1*d*(216*a**2*b*d**4 + a*c0 + a + b)
    -6*b*c1*d*(216*a**2*b*d**4 + a*c0 + a + b)
    3*c1*(-72*a**2*b*d**6 + 2*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*c1*(18*a**2*b*d**6 - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'b': '0'}
    {'b': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'b': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0064: tanh(tan(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    12*a**2*b*c1
    18*a**2*b*c1
    2*a**2*b*c1
    24*a**2*b*c1
    6*a**2*b*c1
    c1*(a*c0 + a + b)
    -12*a**2*b*c1
    -18*a**2*b*c1
    -24*a**2*b*c1
    -8*a**2*b*c1
    c1*(-2*a**2*b + a*c0 + a + b)
    -c1*(16*a**2*b + a*c0 + a + b)
    -c1*(6*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0067: z**2 + cosh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    a**3*c1**2
    2*a**2*c1**2
    2*a**4*c1**2
    2*a*c1**2*d
    2*a*b*c1**2
    a*b**2*c1**2
    2*a**2*c1**2*d
    2*a**2*b*c1**2
    2*a*b**3*c1**2
    2*a*b*c1**2*d
    6*a**3*c1**2*d
    6*a**3*b*c1**2
    12*a**2*b*c1**2*d
    6*a**2*b**2*c1**2
    6*a*b**2*c1**2*d
    2*c1*d*(a*c0 + a*c1*d**2 + a + b)
    2*a*c1*(a*c0 + 3*a*c1*d**2 + a + b)
    2*b*c1*(a*c0 + 3*a*c1*d**2 + a + b)
    c1*(-a**2*b + a*c0 + a*c1*d**2 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0068: sin(alpha*z) + tanh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    a*alpha*c1**2
    6*a**2*b*c1
    c1*(2*a**2*b + a*c0 + a + b)
    -c1*(8*a**2*b + a*c0 + a + b)
    alpha*c1*(a**2*alpha**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0069: tanh(tanh(z)*sech(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    2*a*c1**2
    -2*a*c1**2
    126*a**2*b*c1
    168*a**2*b*c1
    2*a**2*b*c1
    24*a**2*b*c1
    30*a**2*b*c1
    48*a**2*b*c1
    6*a**2*b*c1
    64*a**2*b*c1
    72*a**2*b*c1
    -12*a**2*b*c1
    -126*a**2*b*c1
    -16*a**2*b*c1
    -168*a**2*b*c1
    -24*a**2*b*c1
    -30*a**2*b*c1
    -36*a**2*b*c1
    -48*a**2*b*c1
    -72*a**2*b*c1
    -8*a**2*b*c1
    -96*a**2*b*c1
    c1*(5*a**2*b + a*c0 + a + b)
    -c1*(5*a**2*b + a*c0 + a + b)
    2*c1*(14*a**2*b + a*c0 + a + b)
    -2*c1*(14*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0070: cos(z) + JacobiSN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    -6*a**2*b*c1*m
    -c1*(a**2*b + a*c0 + a + b)
    c1*(a**2*b*m + a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0071: tanh(sech(alpha*z)**2)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    144*a**2*alpha**3*b*c1
    16*a**2*alpha**3*b*c1
    168*a**2*alpha**3*b*c1
    192*a**2*alpha**3*b*c1
    24*a**2*alpha**3*b*c1
    48*a**2*alpha**3*b*c1
    72*a**2*alpha**3*b*c1
    -144*a**2*alpha**3*b*c1
    -168*a**2*alpha**3*b*c1
    -48*a**2*alpha**3*b*c1
    -64*a**2*alpha**3*b*c1
    -72*a**2*alpha**3*b*c1
    2*a*alpha*c1*(-12*a*alpha**2*b + c1)
    2*a*alpha*c1*(-60*a*alpha**2*b + c1)
    2*a*alpha*c1*(12*a*alpha**2*b - c1)
    2*a*alpha*c1*(60*a*alpha**2*b - c1)
    2*alpha*c1*(12*a**2*alpha**2*b - a*c0 - a - b)
    2*alpha*c1*(12*a**2*alpha**2*b + a*c0 + a + b)
    2*alpha*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
    -2*alpha*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'b': '0'}
    {'b': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'b': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0072: tanh(sech(z)**2)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    144*a**2*b*c1
    16*a**2*b*c1
    168*a**2*b*c1
    192*a**2*b*c1
    24*a**2*b*c1
    48*a**2*b*c1
    72*a**2*b*c1
    -144*a**2*b*c1
    -168*a**2*b*c1
    -48*a**2*b*c1
    -64*a**2*b*c1
    -72*a**2*b*c1
    2*a*c1*(-12*a*b + c1)
    2*a*c1*(-60*a*b + c1)
    2*a*c1*(12*a*b - c1)
    2*a*c1*(60*a*b - c1)
    2*c1*(12*a**2*b - a*c0 - a - b)
    2*c1*(12*a**2*b + a*c0 + a + b)
    2*c1*(8*a**2*b + a*c0 + a + b)
    -2*c1*(8*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'b': '0'}
    {'b': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'b': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0073: tanh(exp(z))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    2*a**2*b*c1
    6*a**2*b*c1
    -6*a**2*b*c1
    -8*a**2*b*c1
    c1*(-a**2*b + a*c0 + a + b)
    c1*(a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0074: z
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**2*c1**2
    a*b*c1**2
    c1*(a*c0 + a*c1*d + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0075: sinh(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a*c1**2
    2*c1*(-4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0076: z + JacobiDN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    a**2*c1**2
    a*b*c1**2
    -a*c1**2*m
    -a**2*c1**2*m
    -a*b*c1**2*m
    6*a**2*b*c1*m**2
    c1*(a*c0 + a*c1*d + a + b)
    -c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a*c1*d + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0078: tanh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1
    c1*(2*a**2*b + a*c0 + a + b)
    -c1*(8*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0080: sin(z)*cosh(z) + csch(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    a**2*b*c1
    2*a**2*b*c1
    3*a**2*b*c1
    -c1*(a*c0 + a + b)
    c1*(-2*a**2*b + a*c0 + a + b)
    c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0081: log(z)*sinh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**6*c1**2
    a**7*c1**2
    3*a**6*b*c1
    a*b**5*c1**2
    a*b**6*c1**2
    a*c1**2*d**5
    a*c1**2*d**6
    12*a**3*b**4*c1
    12*a**5*b**2*c1
    12*a**5*b*c1*d
    18*a**4*b**3*c1
    3*a**2*b**5*c1
    5*a**5*c1**2*d
    5*a**5*b*c1**2
    6*a**6*c1**2*d
    6*a**6*b*c1**2
    10*a**3*b**3*c1**2
    10*a**3*c1**2*d**3
    10*a**4*b**2*c1**2
    10*a**4*c1**2*d**2
    12*a**2*b**4*c1*d
    12*a**3*b*c1*d**3
    15*a**3*b**4*c1**2
    15*a**3*c1**2*d**4
    15*a**5*b**2*c1**2
    15*a**5*c1**2*d**2
    18*a**4*b*c1*d**2
    20*a**4*b**3*c1**2
    20*a**4*c1**2*d**3
    20*a**4*b*c1**2*d
    3*a**2*b*c1*d**4
    30*a**5*b*c1**2*d
    36*a**3*b**3*c1*d
    36*a**4*b**2*c1*d
    5*a**2*b**4*c1**2
    5*a**2*c1**2*d**4
    5*a*b**4*c1**2*d
    5*a*b*c1**2*d**4
    6*a**2*b**5*c1**2
    6*a**2*c1**2*d**5
    6*a*b**5*c1**2*d
    6*a*b*c1**2*d**5
    10*a*b**2*c1**2*d**3
    10*a*b**3*c1**2*d**2
    12*a**2*b**2*c1*d**3
    15*a*b**2*c1**2*d**4
    15*a*b**4*c1**2*d**2
    18*a**2*b**3*c1*d**2
    20*a**2*b**3*c1**2*d
    20*a**2*b*c1**2*d**3
    20*a*b**3*c1**2*d**3
    30*a**2*b**4*c1**2*d
    30*a**2*b*c1**2*d**4
    30*a**3*b**2*c1**2*d
    30*a**3*b*c1**2*d**2
    36*a**3*b**2*c1*d**2
    60*a**3*b**3*c1**2*d
    60*a**3*b*c1**2*d**3
    60*a**4*b**2*c1**2*d
    60*a**4*b*c1**2*d**2
    30*a**2*b**2*c1**2*d**2
    60*a**2*b**2*c1**2*d**3
    60*a**2*b**3*c1**2*d**2
    90*a**3*b**2*c1**2*d**2
    a**6*c1*(-a**2*b + a*c0 + a + b)
    b**6*c1*(-a**2*b + a*c0 + a + b)
    c1*d**6*(-a**2*b + a*c0 + a + b)
    a**5*c1*(-3*a**2*b + a*c0 + a + b)
    b**5*c1*(-3*a**2*b + a*c0 + a + b)
    6*a**5*b*c1*(-a**2*b + a*c0 + a + b)
    6*a**5*c1*d*(-a**2*b + a*c0 + a + b)
    6*b**5*c1*d*(-a**2*b + a*c0 + a + b)
    6*a*b**5*c1*(-a**2*b + a*c0 + a + b)
    6*a*c1*d**5*(-a**2*b + a*c0 + a + b)
    6*b*c1*d**5*(-a**2*b + a*c0 + a + b)
    15*a**2*b**4*c1*(-a**2*b + a*c0 + a + b)
    15*a**2*c1*d**4*(-a**2*b + a*c0 + a + b)
    15*a**4*b**2*c1*(-a**2*b + a*c0 + a + b)
    15*a**4*c1*d**2*(-a**2*b + a*c0 + a + b)
    15*b**2*c1*d**4*(-a**2*b + a*c0 + a + b)
    15*b**4*c1*d**2*(-a**2*b + a*c0 + a + b)
    20*a**3*b**3*c1*(-a**2*b + a*c0 + a + b)
    20*a**3*c1*d**3*(-a**2*b + a*c0 + a + b)
    20*b**3*c1*d**3*(-a**2*b + a*c0 + a + b)
    30*a**4*b*c1*d*(-a**2*b + a*c0 + a + b)
    30*a*b**4*c1*d*(-a**2*b + a*c0 + a + b)
    30*a*b*c1*d**4*(-a**2*b + a*c0 + a + b)
    5*a**4*b*c1*(-3*a**2*b + a*c0 + a + b)
    5*a**4*c1*d*(-3*a**2*b + a*c0 + a + b)
    5*b**4*c1*d*(-3*a**2*b + a*c0 + a + b)
    5*a*b**4*c1*(-3*a**2*b + a*c0 + a + b)
    10*a**2*b**3*c1*(-3*a**2*b + a*c0 + a + b)
    10*a**3*b**2*c1*(-3*a**2*b + a*c0 + a + b)
    20*a**3*b*c1*d*(-3*a**2*b + a*c0 + a + b)
    20*a*b**3*c1*d*(-3*a**2*b + a*c0 + a + b)
    60*a**2*b**3*c1*d*(-a**2*b + a*c0 + a + b)
    60*a**2*b*c1*d**3*(-a**2*b + a*c0 + a + b)
    60*a**3*b**2*c1*d*(-a**2*b + a*c0 + a + b)
    60*a**3*b*c1*d**2*(-a**2*b + a*c0 + a + b)
    60*a*b**2*c1*d**3*(-a**2*b + a*c0 + a + b)
    60*a*b**3*c1*d**2*(-a**2*b + a*c0 + a + b)
    30*a**2*b**2*c1*d*(-3*a**2*b + a*c0 + a + b)
    90*a**2*b**2*c1*d**2*(-a**2*b + a*c0 + a + b)
    c1*d**3*(-3*a**2*b*d**2 - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    2*a**3*c1*(-15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*b**3*c1*(-15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    6*a**2*b*c1*(-15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    6*a*b**2*c1*(-15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    a*c1*d**2*(-15*a**2*b*d**2 - 6*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    b*c1*d**2*(-15*a**2*b*d**2 - 6*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*a**2*c1*d*(-15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*b**2*c1*d*(-15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    4*a*b*c1*d*(-15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0082: tanh(JacobiCN(z, m))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1
    -6*a**2*b*c1
    12*a**2*b*c1*m
    2*a**2*b*c1*m
    6*a**2*b*c1*m
    -12*a**2*b*c1*m
    -8*a**2*b*c1*m
    2*a**2*b*c1*(4 - 3*m)
    2*a**2*b*c1*(3*m - 1)
    c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0083: exp(-2*z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -2*a*c1**2
    2*c1*(4*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0084: JacobiSN(z, m) + csch(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    a**2*b*c1
    2*a**2*b*c1
    3*a**2*b*c1
    -c1*(a*c0 + a + b)
    -6*a**2*b*c1*m
    c1*(a**2*b*m + a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0091: sinh(z) + JacobiDN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2*m
    6*a**2*b*c1*m**2
    c1*(-a**2*b + a*c0 + a + b)
    -c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0092: sin(z)*sinh(z)*cosh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    c1*(-a**2*b + a*c0 + a + b)
    c1*(-11*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0094: sech(alpha*z)**4
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -4*a*alpha*c1**2
    8*a*alpha*c1*(15*a*alpha**2*b + 2*c1)
    -4*alpha*c1*(14*a**2*alpha**2*b + a*c0 + a*c1 + a + b)
    8*alpha*c1*(29*a**2*alpha**2*b + a*c0 + 2*a*c1 + a + b)
    -4*alpha*c1*(74*a**2*alpha**2*b + a*c0 + 6*a*c1 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0095: coth(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -2*a*c1**2
    12*a**2*b*c1
    -2*c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0097: cos(z) + sech(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    2*a*c1**2
    -2*a*c1**2
    -2*a*c1*(12*a*b + c1)
    -c1*(a**2*b + a*c0 + a*c1 + a + b)
    -2*c1*(8*a**2*b + a*c0 + a*c1 + a + b)
    2*c1*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0098: z + sin(z)*cosh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    a**2*c1**2
    a*b*c1**2
    c1*(a*c0 + a*c1*d + a + b)
    c1*(-2*a**2*b + a*c0 + a*c1*d + a + b)
    c1*(2*a**2*b + a*c0 + a*c1*d + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0099: sinh(z) + sech(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2
    -a*c1**2
    6*a**2*b*c1
    c1*(-a**2*b + a*c0 + a + b)
    -c1*(5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0100: tanh(alpha*z)*JacobiCN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -a*c1**2
    a*alpha*c1**2
    -a*alpha*c1**2
    6*a**2*b*c1*m
    6*a**2*alpha**2*b*c1
    6*a**2*alpha**3*b*c1
    6*a**2*alpha*b*c1*m
    -6*a**2*alpha*b*c1*m
    alpha*c1*(2*a**2*alpha**2*b + 3*a**2*b + a*c0 + a + b)
    -alpha*c1*(8*a**2*alpha**2*b + 3*a**2*b + a*c0 + a + b)
    -c1*(6*a**2*alpha**2*b + 4*a**2*b*m + a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

