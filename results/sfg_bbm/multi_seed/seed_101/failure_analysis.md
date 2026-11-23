# BBM [2,1] failure analysis

Candidates with `solve_status=success` do not automatically satisfy the
original PDE. This file records every downstream stage separately.

## func_0001: JacobiDN(z, m) + sech(z)**2
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
    a*c1**2*m
    -2*a*c1**2
    -a*c1**2*m
    6*a**2*b*c1*m**2
    -2*a*c1*(12*a*b + c1)
    -2*c1*(8*a**2*b + a*c0 + a*c1 + a + b)
    2*c1*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    -c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a*c1 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0002: tanh(csch(z))
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

## func_0003: z**2 + tanh(alpha*z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -a*alpha*c1**2
    2*a**2*c1**2
    2*a**4*c1**2
    2*a*b*c1**2
    -a**3*alpha*c1**2
    2*a*b**3*c1**2
    6*a**3*b*c1**2
    a*c1**2*(alpha + 2*d)
    -a*alpha*b**2*c1**2
    6*a**2*alpha**3*b*c1
    6*a**2*b**2*c1**2
    a**3*c1**2*(alpha + 6*d)
    -2*a**2*alpha*c1**2*d
    -2*a**2*alpha*b*c1**2
    -2*a*alpha*b*c1**2*d
    a*b**2*c1**2*(alpha + 6*d)
    2*a**2*b*c1**2*(alpha + 6*d)
    2*a*c1*(a*alpha*c1*d + a*c0 + 3*a*c1*d**2 + a + b)
    2*b*c1*(a*alpha*c1*d + a*c0 + 3*a*c1*d**2 + a + b)
    -alpha*c1*(8*a**2*alpha**2*b + a*c0 + a*c1*d**2 + a + b)
    c1*(2*a**2*alpha**3*b + a*alpha*c0 + a*alpha*c1*d**2 + a*alpha + 2*a*c0*d + 2*a*c1*d**3 + 2*a*d + alpha*b + 2*b*d)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0004: cos(z)*tanh(z)
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
    c1*(5*a**2*b + a*c0 + a + b)
    -c1*(11*a**2*b + a*c0 + a + b)
    -c1*(7*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0005: log(z) + exp(-z)
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
    -a**5*c1**2
    a*b**3*c1**2
    a*c1**2*d**3
    -a*b**4*c1**2
    -a*c1**2*d**4
    3*a**3*c1**2*d
    3*a**3*b*c1**2
    -4*a**4*c1**2*d
    -4*a**4*b*c1**2
    3*a**2*b**2*c1**2
    3*a**2*c1**2*d**2
    3*a*b**2*c1**2*d
    3*a*b*c1**2*d**2
    6*a**2*b*c1**2*d
    a**3*c1*(a*c0 + a + b)
    b**3*c1*(a*c0 + a + b)
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
    3*a**2*b*c1*(a*c0 + a + b)
    3*a**2*c1*d*(a*c0 + a + b)
    3*b**2*c1*d*(a*c0 + a + b)
    3*a*b**2*c1*(a*c0 + a + b)
    6*a*b*c1*d*(a*c0 + a + b)
    a**4*c1*(a**2*b - a*c0 - a - b)
    b**4*c1*(a**2*b - a*c0 - a - b)
    4*a**3*b*c1*(a**2*b - a*c0 - a - b)
    4*a*b**3*c1*(a**2*b - a*c0 - a - b)
    6*a**2*b**2*c1*(a**2*b - a*c0 - a - b)
    c1*d**3*(a**2*b*d - a*c0*d + a*c1 - a*d - b*d)
    c1*d*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    a*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    b*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    a**3*c1*(4*a**2*b*d - 4*a*c0*d + a*c1 - 4*a*d - 4*b*d)
    b**3*c1*(4*a**2*b*d - 4*a*c0*d + a*c1 - 4*a*d - 4*b*d)
    3*a**2*b*c1*(4*a**2*b*d - 4*a*c0*d + a*c1 - 4*a*d - 4*b*d)
    3*a**2*c1*d*(2*a**2*b*d - 2*a*c0*d + a*c1 - 2*a*d - 2*b*d)
    3*b**2*c1*d*(2*a**2*b*d - 2*a*c0*d + a*c1 - 2*a*d - 2*b*d)
    3*a*b**2*c1*(4*a**2*b*d - 4*a*c0*d + a*c1 - 4*a*d - 4*b*d)
    6*a*b*c1*d*(2*a**2*b*d - 2*a*c0*d + a*c1 - 2*a*d - 2*b*d)
    a*c1*d**2*(4*a**2*b*d - 4*a*c0*d + 3*a*c1 - 4*a*d - 4*b*d)
    b*c1*d**2*(4*a**2*b*d - 4*a*c0*d + 3*a*c1 - 4*a*d - 4*b*d)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0006: z**6
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

## func_0007: exp(-2*z)
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

## func_0008: tanh(exp(-z**2))
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

## func_0009: exp(-z)*cosh(z)
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
    c1*(-4*a**2*b + a*c0 + a + b)
    c1*(4*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0010: cosh(z)**2
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

## func_0013: tanh(sinh(z))
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

## func_0015: tanh(z)
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

## func_0016: exp(-z)*csch(z)
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
    a**2*b*c1
    2*a**2*b*c1
    3*a**2*b*c1
    c1*(a**2*b - a*c0 - a - b)
    c1*(3*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0017: tan(z)*JacobiSN(z, m)
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
    -6*a**2*b*c1
    -6*a**2*b*c1*m
    c1*(3*a**2*b*m + a**2*b + a*c0 + a + b)
    c1*(a**2*b*m - 5*a**2*b + a*c0 + a + b)
    c1*(3*a**2*b*m - 5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0019: z + log(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**5*c1**2
    a**6*c1**2
    a*b**4*c1**2
    a*b**5*c1**2
    4*a**4*b*c1**2
    5*a**5*b*c1**2
    10*a**3*b**3*c1**2
    10*a**4*b**2*c1**2
    4*a**2*b**3*c1**2
    5*a**2*b**4*c1**2
    6*a**3*b**2*c1**2
    a**4*c1**2*(4*d + 1)
    a*c1**2*d**3*(d + 1)
    a*b**3*c1**2*(4*d + 1)
    3*a**3*c1**2*d*(2*d + 1)
    3*a**3*b*c1**2*(4*d + 1)
    a**2*c1**2*d**2*(4*d + 3)
    a*b*c1**2*d**2*(4*d + 3)
    3*a**2*b**2*c1**2*(4*d + 1)
    3*a*b**2*c1**2*d*(2*d + 1)
    6*a**2*b*c1**2*d*(2*d + 1)
    a**4*c1*(a*c0 + 5*a*c1*d + a*c1 + a + b)
    b**4*c1*(a*c0 + 5*a*c1*d + a*c1 + a + b)
    4*a**3*b*c1*(a*c0 + 5*a*c1*d + a*c1 + a + b)
    4*a*b**3*c1*(a*c0 + 5*a*c1*d + a*c1 + a + b)
    6*a**2*b**2*c1*(a*c0 + 5*a*c1*d + a*c1 + a + b)
    a**3*c1*(4*a*c0*d + a*c0 + 10*a*c1*d**2 + 4*a*c1*d + 4*a*d + a + 4*b*d + b)
    b**3*c1*(4*a*c0*d + a*c0 + 10*a*c1*d**2 + 4*a*c1*d + 4*a*d + a + 4*b*d + b)
    3*a**2*b*c1*(4*a*c0*d + a*c0 + 10*a*c1*d**2 + 4*a*c1*d + 4*a*d + a + 4*b*d + b)
    3*a*b**2*c1*(4*a*c0*d + a*c0 + 10*a*c1*d**2 + 4*a*c1*d + 4*a*d + a + 4*b*d + b)
    a**2*c1*d*(6*a*c0*d + 3*a*c0 + 10*a*c1*d**2 + 6*a*c1*d + 6*a*d + 3*a + 6*b*d + 3*b)
    b**2*c1*d*(6*a*c0*d + 3*a*c0 + 10*a*c1*d**2 + 6*a*c1*d + 6*a*d + 3*a + 6*b*d + 3*b)
    2*a*b*c1*d*(6*a*c0*d + 3*a*c0 + 10*a*c1*d**2 + 6*a*c1*d + 6*a*d + 3*a + 6*b*d + 3*b)
    c1*d*(-2*a**2*b + a*c0*d**3 + a*c0*d**2 + a*c1*d**4 + a*c1*d**3 + a*d**3 + a*d**2 + b*d**3 + b*d**2)
    a*c1*(-2*a**2*b + 4*a*c0*d**3 + 3*a*c0*d**2 + 5*a*c1*d**4 + 4*a*c1*d**3 + 4*a*d**3 + 3*a*d**2 + 4*b*d**3 + 3*b*d**2)
    b*c1*(-2*a**2*b + 4*a*c0*d**3 + 3*a*c0*d**2 + 5*a*c1*d**4 + 4*a*c1*d**3 + 4*a*d**3 + 3*a*d**2 + 4*b*d**3 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0020: z**2 + cosh(z)
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

## func_0021: z**3 + log(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    3*a**10*c1**2
    3*a**7*c1**2
    18*a**6*c1**2*d
    18*a**6*b*c1**2
    27*a**9*c1**2*d
    27*a**9*b*c1**2
    3*a*b**6*c1**2
    3*a*b**9*c1**2
    108*a**3*b**7*c1**2
    108*a**8*b**2*c1**2
    108*a**8*c1**2*d**2
    18*a**2*b**5*c1**2
    18*a*b**5*c1**2*d
    216*a**8*b*c1**2*d
    252*a**4*b**6*c1**2
    252*a**7*b**3*c1**2
    27*a**2*b**8*c1**2
    27*a*b**8*c1**2*d
    378*a**5*b**5*c1**2
    378*a**6*b**4*c1**2
    45*a**3*b**4*c1**2
    45*a**5*b**2*c1**2
    45*a**5*c1**2*d**2
    60*a**4*b**3*c1**2
    90*a**5*b*c1**2*d
    108*a*b**7*c1**2*d**2
    1512*a**4*b**5*c1**2*d
    1512*a**6*b**3*c1**2*d
    180*a**3*b**3*c1**2*d
    180*a**4*b**2*c1**2*d
    180*a**4*b*c1**2*d**2
    1890*a**5*b**4*c1**2*d
    216*a**2*b**7*c1**2*d
    45*a*b**4*c1**2*d**2
    756*a**3*b**6*c1**2*d
    756*a**7*b**2*c1**2*d
    756*a**7*b*c1**2*d**2
    90*a**2*b**4*c1**2*d
    a**4*c1**2*(60*d**3 + 1)
    180*a**2*b**3*c1**2*d**2
    2268*a**3*b**5*c1**2*d**2
    2268*a**6*b**2*c1**2*d**2
    270*a**3*b**2*c1**2*d**2
    3780*a**4*b**4*c1**2*d**2
    3780*a**5*b**3*c1**2*d**2
    756*a**2*b**6*c1**2*d**2
    a*b**3*c1**2*(60*d**3 + 1)
    a*c1**2*d**3*(3*d**3 + 1)
    3*a**3*c1**2*d*(15*d**3 + 1)
    3*a**3*b*c1**2*(60*d**3 + 1)
    3*a**2*b**2*c1**2*(60*d**3 + 1)
    3*a**2*c1**2*d**2*(6*d**3 + 1)
    3*a*b**2*c1**2*d*(15*d**3 + 1)
    3*a*b*c1**2*d**2*(6*d**3 + 1)
    6*a**2*b*c1**2*d*(15*d**3 + 1)
    a**6*c1*(3*a*c0 + 252*a*c1*d**3 + a*c1 + 3*a + 3*b)
    b**6*c1*(3*a*c0 + 252*a*c1*d**3 + a*c1 + 3*a + 3*b)
    6*a**5*b*c1*(3*a*c0 + 252*a*c1*d**3 + a*c1 + 3*a + 3*b)
    6*a**5*c1*d*(3*a*c0 + 63*a*c1*d**3 + a*c1 + 3*a + 3*b)
    6*b**5*c1*d*(3*a*c0 + 63*a*c1*d**3 + a*c1 + 3*a + 3*b)
    6*a*b**5*c1*(3*a*c0 + 252*a*c1*d**3 + a*c1 + 3*a + 3*b)
    15*a**2*b**4*c1*(3*a*c0 + 252*a*c1*d**3 + a*c1 + 3*a + 3*b)
    15*a**4*b**2*c1*(3*a*c0 + 252*a*c1*d**3 + a*c1 + 3*a + 3*b)
    20*a**3*b**3*c1*(3*a*c0 + 252*a*c1*d**3 + a*c1 + 3*a + 3*b)
    30*a**4*b*c1*d*(3*a*c0 + 63*a*c1*d**3 + a*c1 + 3*a + 3*b)
    30*a*b**4*c1*d*(3*a*c0 + 63*a*c1*d**3 + a*c1 + 3*a + 3*b)
    60*a**2*b**3*c1*d*(3*a*c0 + 63*a*c1*d**3 + a*c1 + 3*a + 3*b)
    60*a**3*b**2*c1*d*(3*a*c0 + 63*a*c1*d**3 + a*c1 + 3*a + 3*b)
    3*a**4*c1*(-2*a**2*b + 15*a*c0*d**2 + 126*a*c1*d**5 + 5*a*c1*d**2 + 15*a*d**2 + 15*b*d**2)
    3*b**4*c1*(-2*a**2*b + 15*a*c0*d**2 + 126*a*c1*d**5 + 5*a*c1*d**2 + 15*a*d**2 + 15*b*d**2)
    12*a**3*b*c1*(-2*a**2*b + 15*a*c0*d**2 + 126*a*c1*d**5 + 5*a*c1*d**2 + 15*a*d**2 + 15*b*d**2)
    12*a*b**3*c1*(-2*a**2*b + 15*a*c0*d**2 + 126*a*c1*d**5 + 5*a*c1*d**2 + 15*a*d**2 + 15*b*d**2)
    18*a**2*b**2*c1*(-2*a**2*b + 15*a*c0*d**2 + 126*a*c1*d**5 + 5*a*c1*d**2 + 15*a*d**2 + 15*b*d**2)
    a**3*c1*(-24*a**2*b*d + 60*a*c0*d**3 + a*c0 + 252*a*c1*d**6 + 20*a*c1*d**3 + 60*a*d**3 + a + 60*b*d**3 + b)
    b**3*c1*(-24*a**2*b*d + 60*a*c0*d**3 + a*c0 + 252*a*c1*d**6 + 20*a*c1*d**3 + 60*a*d**3 + a + 60*b*d**3 + b)
    3*a**2*b*c1*(-24*a**2*b*d + 60*a*c0*d**3 + a*c0 + 252*a*c1*d**6 + 20*a*c1*d**3 + 60*a*d**3 + a + 60*b*d**3 + b)
    3*a**2*c1*d*(-12*a**2*b*d + 15*a*c0*d**3 + a*c0 + 36*a*c1*d**6 + 5*a*c1*d**3 + 15*a*d**3 + a + 15*b*d**3 + b)
    3*b**2*c1*d*(-12*a**2*b*d + 15*a*c0*d**3 + a*c0 + 36*a*c1*d**6 + 5*a*c1*d**3 + 15*a*d**3 + a + 15*b*d**3 + b)
    3*a*b**2*c1*(-24*a**2*b*d + 60*a*c0*d**3 + a*c0 + 252*a*c1*d**6 + 20*a*c1*d**3 + 60*a*d**3 + a + 60*b*d**3 + b)
    6*a*b*c1*d*(-12*a**2*b*d + 15*a*c0*d**3 + a*c0 + 36*a*c1*d**6 + 5*a*c1*d**3 + 15*a*d**3 + a + 15*b*d**3 + b)
    c1*d*(-6*a**2*b*d**3 - 2*a**2*b + 3*a*c0*d**5 + a*c0*d**2 + 3*a*c1*d**8 + a*c1*d**5 + 3*a*d**5 + a*d**2 + 3*b*d**5 + b*d**2)
    a*c1*(-24*a**2*b*d**3 - 2*a**2*b + 18*a*c0*d**5 + 3*a*c0*d**2 + 27*a*c1*d**8 + 6*a*c1*d**5 + 18*a*d**5 + 3*a*d**2 + 18*b*d**5 + 3*b*d**2)
    b*c1*(-24*a**2*b*d**3 - 2*a**2*b + 18*a*c0*d**5 + 3*a*c0*d**2 + 27*a*c1*d**8 + 6*a*c1*d**5 + 18*a*d**5 + 3*a*d**2 + 18*b*d**5 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0022: sinh(z)**2
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

## func_0023: tanh(sin(z)*cosh(z))
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

## func_0024: exp(2*z)
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

## func_0025: 2*JacobiDN(z, m)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -4*a*c1**2*m
    12*a**2*b*c1*m**2
    -2*c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'m': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
    {'a': '0', 'm': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'m': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'substituted trial is constant', 'identity_verification_status': ...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...
    {'solution': {'a': '0', 'm': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'substituted trial is constant', 'identity_verification...

## func_0027: tanh(sech(z)**2)
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

## func_0029: tanh(tanh(alpha*z))
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

## func_0030: exp(z) + tanh(alpha*z)
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

## func_0032: tanh(sin(z))
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

## func_0034: z**2 + tanh(z)
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
    -a**3*c1**2
    2*a**2*c1**2
    2*a**4*c1**2
    2*a*b*c1**2
    6*a**2*b*c1
    -a*b**2*c1**2
    2*a*b**3*c1**2
    6*a**3*b*c1**2
    a*c1**2*(2*d + 1)
    -2*a**2*c1**2*d
    -2*a**2*b*c1**2
    -2*a*b*c1**2*d
    6*a**2*b**2*c1**2
    a**3*c1**2*(6*d + 1)
    a*b**2*c1**2*(6*d + 1)
    2*a**2*b*c1**2*(6*d + 1)
    -c1*(8*a**2*b + a*c0 + a*c1*d**2 + a + b)
    2*a*c1*(a*c0 + 3*a*c1*d**2 + a*c1*d + a + b)
    2*b*c1*(a*c0 + 3*a*c1*d**2 + a*c1*d + a + b)
    c1*(2*a**2*b + 2*a*c0*d + a*c0 + 2*a*c1*d**3 + a*c1*d**2 + 2*a*d + a + 2*b*d + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0035: log(z)**2
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

## func_0037: log(z) + tanh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**5*c1**2
    -a**5*c1**2
    6*a**6*b*c1
    a*b**4*c1**2
    -a*b**4*c1**2
    -a*c1**2*d**4
    24*a**3*b**4*c1
    24*a**5*b**2*c1
    24*a**5*b*c1*d
    36*a**4*b**3*c1
    4*a**4*b*c1**2
    6*a**2*b**5*c1
    -4*a**4*c1**2*d
    -4*a**4*b*c1**2
    24*a**2*b**4*c1*d
    24*a**3*b*c1*d**3
    36*a**4*b*c1*d**2
    4*a**2*b**3*c1**2
    6*a**2*b*c1*d**4
    6*a**3*b**2*c1**2
    72*a**3*b**3*c1*d
    72*a**4*b**2*c1*d
    a**4*c1**2*(4*d + 1)
    a*c1**2*d**3*(d + 1)
    -12*a**3*b*c1**2*d
    -4*a**2*b**3*c1**2
    -4*a**2*c1**2*d**3
    -4*a*b**3*c1**2*d
    -4*a*b*c1**2*d**3
    -6*a**3*b**2*c1**2
    -6*a**3*c1**2*d**2
    24*a**2*b**2*c1*d**3
    36*a**2*b**3*c1*d**2
    72*a**3*b**2*c1*d**2
    a*b**3*c1**2*(4*d + 1)
    -12*a**2*b**2*c1**2*d
    -12*a**2*b*c1**2*d**2
    -6*a*b**2*c1**2*d**2
    3*a**3*c1**2*d*(2*d + 1)
    3*a**3*b*c1**2*(4*d + 1)
    a**2*c1**2*d**2*(4*d + 3)
    a*b*c1**2*d**2*(4*d + 3)
    3*a**2*b**2*c1**2*(4*d + 1)
    3*a*b**2*c1**2*d*(2*d + 1)
    6*a**2*b*c1**2*d*(2*d + 1)
    a**4*c1*(2*a**2*b + a*c0 + a + b)
    b**4*c1*(2*a**2*b + a*c0 + a + b)
    -a**4*c1*(8*a**2*b + a*c0 + a + b)
    -b**4*c1*(8*a**2*b + a*c0 + a + b)
    -c1*d**4*(8*a**2*b + a*c0 + a + b)
    4*a**3*b*c1*(2*a**2*b + a*c0 + a + b)
    4*a*b**3*c1*(2*a**2*b + a*c0 + a + b)
    -4*a**3*b*c1*(8*a**2*b + a*c0 + a + b)
    -4*a**3*c1*d*(8*a**2*b + a*c0 + a + b)
    -4*b**3*c1*d*(8*a**2*b + a*c0 + a + b)
    -4*a*b**3*c1*(8*a**2*b + a*c0 + a + b)
    -4*a*c1*d**3*(8*a**2*b + a*c0 + a + b)
    -4*b*c1*d**3*(8*a**2*b + a*c0 + a + b)
    6*a**2*b**2*c1*(2*a**2*b + a*c0 + a + b)
    -12*a**2*b*c1*d*(8*a**2*b + a*c0 + a + b)
    -12*a*b**2*c1*d*(8*a**2*b + a*c0 + a + b)
    -12*a*b*c1*d**2*(8*a**2*b + a*c0 + a + b)
    -6*a**2*b**2*c1*(8*a**2*b + a*c0 + a + b)
    -6*a**2*c1*d**2*(8*a**2*b + a*c0 + a + b)
    -6*b**2*c1*d**2*(8*a**2*b + a*c0 + a + b)
    a**3*c1*(8*a**2*b*d + 4*a*c0*d + a*c0 + 4*a*d + a + 4*b*d + b)
    b**3*c1*(8*a**2*b*d + 4*a*c0*d + a*c0 + 4*a*d + a + 4*b*d + b)
    3*a**2*b*c1*(8*a**2*b*d + 4*a*c0*d + a*c0 + 4*a*d + a + 4*b*d + b)
    3*a**2*c1*d*(4*a**2*b*d + 2*a*c0*d + a*c0 + 2*a*d + a + 2*b*d + b)
    3*b**2*c1*d*(4*a**2*b*d + 2*a*c0*d + a*c0 + 2*a*d + a + 2*b*d + b)
    3*a*b**2*c1*(8*a**2*b*d + 4*a*c0*d + a*c0 + 4*a*d + a + 4*b*d + b)
    6*a*b*c1*d*(4*a**2*b*d + 2*a*c0*d + a*c0 + 2*a*d + a + 2*b*d + b)
    c1*d*(2*a**2*b*d**3 - 2*a**2*b + a*c0*d**3 + a*c0*d**2 + a*d**3 + a*d**2 + b*d**3 + b*d**2)
    a*c1*(8*a**2*b*d**3 - 2*a**2*b + 4*a*c0*d**3 + 3*a*c0*d**2 + 4*a*d**3 + 3*a*d**2 + 4*b*d**3 + 3*b*d**2)
    b*c1*(8*a**2*b*d**3 - 2*a**2*b + 4*a*c0*d**3 + 3*a*c0*d**2 + 4*a*d**3 + 3*a*d**2 + 4*b*d**3 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0039: exp(-2*z**2)
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

## func_0040: exp(z)*sin(z)*cosh(z)
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
    -6*a**2*b*c1
    c1*(-a**2*b + a*c0 + a + b)
    c1*(-5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0042: tanh(JacobiDN(z, m))
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2*m
    -a*c1**2*m
    12*a**2*b*c1*m**2
    2*a**2*b*c1*m**3
    6*a**2*b*c1*m**2
    6*a**2*b*c1*m**3
    -12*a**2*b*c1*m**2
    -6*a**2*b*c1*m**2
    -6*a**2*b*c1*m**3
    -8*a**2*b*c1*m**3
    2*a**2*b*c1*m**2*(3 - m)
    2*a**2*b*c1*m**2*(4*m - 3)
    c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
    -c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'m': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
    {'a': '0', 'm': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'m': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'substituted trial is constant', 'identity_verification_status': ...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...
    {'solution': {'a': '0', 'm': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'substituted trial is constant', 'identity_verification...

## func_0043: cos(z) + JacobiSN(z, m)
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

## func_0044: tanh(JacobiSN(z, m))
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

## func_0046: z + cos(z)
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
    a**2*c1**2
    a*b*c1**2
    -a**2*c1**2
    -a*b*c1**2
    c1*(a*c0 + a*c1*d + a + b)
    -c1*(a**2*b + a*c0 + a*c1*d + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0047: sin(z)**2
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

## func_0051: tanh(tan(z))
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

## func_0052: tanh(alpha*z) + JacobiDN(z, m)
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
    -a*c1**2*m
    -a*alpha*c1**2
    6*a**2*alpha**3*b*c1
    6*a**2*b*c1*m**2
    alpha*c1*(2*a**2*alpha**2*b + a*c0 + a + b)
    -alpha*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
    -c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0054: tanh(alpha*z) + coth(z)
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
    6*a**2*b*c1
    6*a**2*alpha**3*b*c1
    -c1*(2*a**2*b + a*c0 + a + b)
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

## func_0055: z
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

## func_0057: tanh(cosh(z))
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

## func_0058: sin(z)*sin(alpha*z)
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
    c1*(3*a**2*alpha**2*b + a**2*b + a*c0 + a + b)
    alpha*c1*(a**2*alpha**2*b + 3*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0061: tanh(z**2)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    16*a**5*b*c1
    48*a**5*b*c1
    -64*a**5*b*c1
    144*a**3*b**3*c1
    144*a**4*b**2*c1
    144*a**4*b*c1*d
    16*a**2*b**4*c1
    48*a**2*b**4*c1
    48*a**3*b**3*c1
    48*a**4*b**2*c1
    48*a**4*b*c1*d
    -192*a**3*b**3*c1
    -192*a**4*b**2*c1
    -192*a**4*b*c1*d
    -64*a**2*b**4*c1
    144*a**2*b**3*c1*d
    144*a**3*b*c1*d**2
    288*a**3*b**2*c1*d
    48*a**2*b**3*c1*d
    48*a**2*b*c1*d**3
    96*a**3*b**2*c1*d
    -192*a**2*b**3*c1*d
    -384*a**3*b**2*c1*d
    144*a**2*b**2*c1*d**2
    2*a**2*c1*(12*a*b + c1)
    2*a*b*c1*(12*a*b + c1)
    2*a*c1*d*(12*a*b + c1)
    -2*a**2*c1*(12*a*b + c1)
    -2*a*b*c1*(12*a*b + c1)
    -2*a*c1*d*(12*a*b + c1)
    2*a*c1*(24*a**2*b*d**2 + a*c0 + a + b)
    2*b*c1*(24*a**2*b*d**2 + a*c0 + a + b)
    2*c1*d*(8*a**2*b*d**2 + a*c0 + a + b)
    -2*a*c1*(96*a**2*b*d**2 + a*c0 + a + b)
    -2*b*c1*(96*a**2*b*d**2 + a*c0 + a + b)
    -2*c1*d*(32*a**2*b*d**2 + a*c0 + a + b)
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

## func_0062: tanh(z)*JacobiCN(z, m)*sech(z)
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
    3*a*c1**2
    -2*a*c1**2
    -3*a*c1**2
    18*a**2*b*c1
    24*a**2*b*c1
    12*a**2*b*c1*m
    6*a**2*b*c1*m
    -6*a**2*b*c1*m
    c1*(8*a**2*b + a*c0 + a + b)
    -2*c1*(17*a**2*b + a*c0 + a + b)
    -c1*(4*a**2*b*m + 16*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0064: log(z) + tanh(alpha*z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**5*alpha*c1**2
    -a**5*alpha*c1**2
    a*alpha*b**4*c1**2
    -a*alpha*b**4*c1**2
    -a*alpha*c1**2*d**4
    4*a**4*alpha*b*c1**2
    6*a**6*alpha**3*b*c1
    -4*a**4*alpha*c1**2*d
    -4*a**4*alpha*b*c1**2
    24*a**3*alpha**3*b**4*c1
    24*a**5*alpha**3*b**2*c1
    24*a**5*alpha**3*b*c1*d
    36*a**4*alpha**3*b**3*c1
    4*a**2*alpha*b**3*c1**2
    6*a**2*alpha**3*b**5*c1
    6*a**3*alpha*b**2*c1**2
    a**4*c1**2*(4*alpha*d + 1)
    a*c1**2*d**3*(alpha*d + 1)
    -12*a**3*alpha*b*c1**2*d
    -4*a**2*alpha*b**3*c1**2
    -4*a**2*alpha*c1**2*d**3
    -4*a*alpha*b**3*c1**2*d
    -4*a*alpha*b*c1**2*d**3
    -6*a**3*alpha*b**2*c1**2
    -6*a**3*alpha*c1**2*d**2
    24*a**2*alpha**3*b**4*c1*d
    24*a**3*alpha**3*b*c1*d**3
    36*a**4*alpha**3*b*c1*d**2
    6*a**2*alpha**3*b*c1*d**4
    72*a**3*alpha**3*b**3*c1*d
    72*a**4*alpha**3*b**2*c1*d
    a*b**3*c1**2*(4*alpha*d + 1)
    -12*a**2*alpha*b**2*c1**2*d
    -12*a**2*alpha*b*c1**2*d**2
    -6*a*alpha*b**2*c1**2*d**2
    24*a**2*alpha**3*b**2*c1*d**3
    3*a**3*c1**2*d*(2*alpha*d + 1)
    3*a**3*b*c1**2*(4*alpha*d + 1)
    36*a**2*alpha**3*b**3*c1*d**2
    72*a**3*alpha**3*b**2*c1*d**2
    a**2*c1**2*d**2*(4*alpha*d + 3)
    a*b*c1**2*d**2*(4*alpha*d + 3)
    3*a**2*b**2*c1**2*(4*alpha*d + 1)
    3*a*b**2*c1**2*d*(2*alpha*d + 1)
    6*a**2*b*c1**2*d*(2*alpha*d + 1)
    a**4*alpha*c1*(2*a**2*alpha**2*b + a*c0 + a + b)
    alpha*b**4*c1*(2*a**2*alpha**2*b + a*c0 + a + b)
    -a**4*alpha*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
    -alpha*b**4*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
    -alpha*c1*d**4*(8*a**2*alpha**2*b + a*c0 + a + b)
    4*a**3*alpha*b*c1*(2*a**2*alpha**2*b + a*c0 + a + b)
    4*a*alpha*b**3*c1*(2*a**2*alpha**2*b + a*c0 + a + b)
    -4*a**3*alpha*b*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
    -4*a**3*alpha*c1*d*(8*a**2*alpha**2*b + a*c0 + a + b)
    -4*a*alpha*b**3*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
    -4*a*alpha*c1*d**3*(8*a**2*alpha**2*b + a*c0 + a + b)
    -4*alpha*b**3*c1*d*(8*a**2*alpha**2*b + a*c0 + a + b)
    -4*alpha*b*c1*d**3*(8*a**2*alpha**2*b + a*c0 + a + b)
    6*a**2*alpha*b**2*c1*(2*a**2*alpha**2*b + a*c0 + a + b)
    -12*a**2*alpha*b*c1*d*(8*a**2*alpha**2*b + a*c0 + a + b)
    -12*a*alpha*b**2*c1*d*(8*a**2*alpha**2*b + a*c0 + a + b)
    -12*a*alpha*b*c1*d**2*(8*a**2*alpha**2*b + a*c0 + a + b)
    -6*a**2*alpha*b**2*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
    -6*a**2*alpha*c1*d**2*(8*a**2*alpha**2*b + a*c0 + a + b)
    -6*alpha*b**2*c1*d**2*(8*a**2*alpha**2*b + a*c0 + a + b)
    a**3*c1*(8*a**2*alpha**3*b*d + 4*a*alpha*c0*d + 4*a*alpha*d + a*c0 + a + 4*alpha*b*d + b)
    b**3*c1*(8*a**2*alpha**3*b*d + 4*a*alpha*c0*d + 4*a*alpha*d + a*c0 + a + 4*alpha*b*d + b)
    3*a**2*b*c1*(8*a**2*alpha**3*b*d + 4*a*alpha*c0*d + 4*a*alpha*d + a*c0 + a + 4*alpha*b*d + b)
    3*a**2*c1*d*(4*a**2*alpha**3*b*d + 2*a*alpha*c0*d + 2*a*alpha*d + a*c0 + a + 2*alpha*b*d + b)
    3*b**2*c1*d*(4*a**2*alpha**3*b*d + 2*a*alpha*c0*d + 2*a*alpha*d + a*c0 + a + 2*alpha*b*d + b)
    3*a*b**2*c1*(8*a**2*alpha**3*b*d + 4*a*alpha*c0*d + 4*a*alpha*d + a*c0 + a + 4*alpha*b*d + b)
    6*a*b*c1*d*(4*a**2*alpha**3*b*d + 2*a*alpha*c0*d + 2*a*alpha*d + a*c0 + a + 2*alpha*b*d + b)
    c1*d*(2*a**2*alpha**3*b*d**3 - 2*a**2*b + a*alpha*c0*d**3 + a*alpha*d**3 + a*c0*d**2 + a*d**2 + alpha*b*d**3 + b*d**2)
    a*c1*(8*a**2*alpha**3*b*d**3 - 2*a**2*b + 4*a*alpha*c0*d**3 + 4*a*alpha*d**3 + 3*a*c0*d**2 + 3*a*d**2 + 4*alpha*b*d**3 + 3*b*d**2)
    b*c1*(8*a**2*alpha**3*b*d**3 - 2*a**2*b + 4*a*alpha*c0*d**3 + 4*a*alpha*d**3 + 3*a*c0*d**2 + 3*a*d**2 + 4*alpha*b*d**3 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0065: z**4
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

## func_0066: tanh(sech(alpha*z)**2)
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

## func_0067: cos(z)*coth(z)
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
    -c1*(a**2*b + a*c0 + a + b)
    -c1*(5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0069: log(z)/z
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
    -a*b**6*c1**2
    -a*c1**2*d**6
    -6*a**6*c1**2*d
    -6*a**6*b*c1**2
    a**7*c1*(a*c0 + a + b)
    b**7*c1*(a*c0 + a + b)
    -15*a**3*b**4*c1**2
    -15*a**3*c1**2*d**4
    -15*a**5*b**2*c1**2
    -15*a**5*c1**2*d**2
    -20*a**4*b**3*c1**2
    -20*a**4*c1**2*d**3
    -30*a**5*b*c1**2*d
    -6*a**2*b**5*c1**2
    -6*a**2*c1**2*d**5
    -6*a*b**5*c1**2*d
    -6*a*b*c1**2*d**5
    -a**7*c1*(a*c0 + a + b)
    -b**7*c1*(a*c0 + a + b)
    -15*a*b**2*c1**2*d**4
    -15*a*b**4*c1**2*d**2
    -20*a*b**3*c1**2*d**3
    -30*a**2*b**4*c1**2*d
    -30*a**2*b*c1**2*d**4
    -60*a**3*b**3*c1**2*d
    -60*a**3*b*c1**2*d**3
    -60*a**4*b**2*c1**2*d
    -60*a**4*b*c1**2*d**2
    7*a**6*b*c1*(a*c0 + a + b)
    7*a**6*c1*d*(a*c0 + a + b)
    7*b**6*c1*d*(a*c0 + a + b)
    7*a*b**6*c1*(a*c0 + a + b)
    -60*a**2*b**2*c1**2*d**3
    -60*a**2*b**3*c1**2*d**2
    -7*a**6*b*c1*(a*c0 + a + b)
    -7*a*b**6*c1*(a*c0 + a + b)
    -90*a**3*b**2*c1**2*d**2
    21*a**2*b**5*c1*(a*c0 + a + b)
    21*a**5*b**2*c1*(a*c0 + a + b)
    35*a**3*b**4*c1*(a*c0 + a + b)
    35*a**4*b**3*c1*(a*c0 + a + b)
    42*a**5*b*c1*d*(a*c0 + a + b)
    42*a*b**5*c1*d*(a*c0 + a + b)
    -21*a**2*b**5*c1*(a*c0 + a + b)
    -21*a**5*b**2*c1*(a*c0 + a + b)
    -35*a**3*b**4*c1*(a*c0 + a + b)
    -35*a**4*b**3*c1*(a*c0 + a + b)
    105*a**2*b**4*c1*d*(a*c0 + a + b)
    105*a**4*b**2*c1*d*(a*c0 + a + b)
    140*a**3*b**3*c1*d*(a*c0 + a + b)
    a**6*c1*(-7*a*c0*d + a*c1 - 7*a*d - 7*b*d)
    b**6*c1*(-7*a*c0*d + a*c1 - 7*a*d - 7*b*d)
    6*a**5*b*c1*(-7*a*c0*d + a*c1 - 7*a*d - 7*b*d)
    6*a*b**5*c1*(-7*a*c0*d + a*c1 - 7*a*d - 7*b*d)
    c1*d**5*(-11*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    15*a**2*b**4*c1*(-7*a*c0*d + a*c1 - 7*a*d - 7*b*d)
    15*a**4*b**2*c1*(-7*a*c0*d + a*c1 - 7*a*d - 7*b*d)
    20*a**3*b**3*c1*(-7*a*c0*d + a*c1 - 7*a*d - 7*b*d)
    a**5*c1*(-11*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    b**5*c1*(-11*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    c1*d**5*(6*a**2*b - a*c0*d**2 + a*c1*d - a*d**2 - b*d**2)
    a*c1*d**4*(-55*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    b*c1*d**4*(-55*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    5*a**4*b*c1*(-11*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    5*a**4*c1*d*(-11*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    5*b**4*c1*d*(-11*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    5*a*b**4*c1*(-11*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    a**2*c1*d**3*(-110*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    b**2*c1*d**3*(-110*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    10*a**2*b**3*c1*(-11*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    10*a**3*b**2*c1*(-11*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    2*a*b*c1*d**3*(-110*a**2*b + 21*a*c0*d**2 + 21*a*d**2 + 21*b*d**2)
    20*a**3*b*c1*d*(-11*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    20*a*b**3*c1*d*(-11*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    5*a**3*c1*d**2*(-22*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    5*b**3*c1*d**2*(-22*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    15*a**2*b*c1*d**2*(-22*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    15*a*b**2*c1*d**2*(-22*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    30*a**2*b**2*c1*d*(-11*a**2*b + 7*a*c0*d**2 + 7*a*d**2 + 7*b*d**2)
    3*a**5*c1*(2*a**2*b - 7*a*c0*d**2 + 2*a*c1*d - 7*a*d**2 - 7*b*d**2)
    3*b**5*c1*(2*a**2*b - 7*a*c0*d**2 + 2*a*c1*d - 7*a*d**2 - 7*b*d**2)
    a*c1*d**4*(30*a**2*b - 7*a*c0*d**2 + 6*a*c1*d - 7*a*d**2 - 7*b*d**2)
    b*c1*d**4*(30*a**2*b - 7*a*c0*d**2 + 6*a*c1*d - 7*a*d**2 - 7*b*d**2)
    15*a**4*b*c1*(2*a**2*b - 7*a*c0*d**2 + 2*a*c1*d - 7*a*d**2 - 7*b*d**2)
    15*a*b**4*c1*(2*a**2*b - 7*a*c0*d**2 + 2*a*c1*d - 7*a*d**2 - 7*b*d**2)
    5*a**4*c1*d*(6*a**2*b - 7*a*c0*d**2 + 3*a*c1*d - 7*a*d**2 - 7*b*d**2)
    5*b**4*c1*d*(6*a**2*b - 7*a*c0*d**2 + 3*a*c1*d - 7*a*d**2 - 7*b*d**2)
    20*a**3*b*c1*d*(6*a**2*b - 7*a*c0*d**2 + 3*a*c1*d - 7*a*d**2 - 7*b*d**2)
    20*a*b**3*c1*d*(6*a**2*b - 7*a*c0*d**2 + 3*a*c1*d - 7*a*d**2 - 7*b*d**2)
    3*a**2*c1*d**3*(20*a**2*b - 7*a*c0*d**2 + 5*a*c1*d - 7*a*d**2 - 7*b*d**2)
    3*b**2*c1*d**3*(20*a**2*b - 7*a*c0*d**2 + 5*a*c1*d - 7*a*d**2 - 7*b*d**2)
    30*a**2*b**3*c1*(2*a**2*b - 7*a*c0*d**2 + 2*a*c1*d - 7*a*d**2 - 7*b*d**2)
    30*a**3*b**2*c1*(2*a**2*b - 7*a*c0*d**2 + 2*a*c1*d - 7*a*d**2 - 7*b*d**2)
    5*a**3*c1*d**2*(12*a**2*b - 7*a*c0*d**2 + 4*a*c1*d - 7*a*d**2 - 7*b*d**2)
    5*b**3*c1*d**2*(12*a**2*b - 7*a*c0*d**2 + 4*a*c1*d - 7*a*d**2 - 7*b*d**2)
    6*a*b*c1*d**3*(20*a**2*b - 7*a*c0*d**2 + 5*a*c1*d - 7*a*d**2 - 7*b*d**2)
    15*a**2*b*c1*d**2*(12*a**2*b - 7*a*c0*d**2 + 4*a*c1*d - 7*a*d**2 - 7*b*d**2)
    15*a*b**2*c1*d**2*(12*a**2*b - 7*a*c0*d**2 + 4*a*c1*d - 7*a*d**2 - 7*b*d**2)
    30*a**2*b**2*c1*d*(6*a**2*b - 7*a*c0*d**2 + 3*a*c1*d - 7*a*d**2 - 7*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0070: sin(z)*cosh(z)*JacobiSN(z, m)
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
    -6*a**2*b*c1
    -6*a**2*b*c1*m
    c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    c1*(3*a**2*b*m + a**2*b + a*c0 + a + b)
    c1*(3*a**2*b*m + 5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0071: exp(z) + sin(z)*cosh(z)
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

## func_0073: coth(z) + exp(-z)
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
    -c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0075: cos(z) + coth(z)
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
    -c1*(a**2*b + a*c0 + a + b)
    -c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0078: z**2*tanh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**5*c1**2
    -a**5*c1**2
    2*a**4*c1**2
    6*a**4*b*c1
    a*b**4*c1**2
    -a*b**4*c1**2
    12*a**3*b**2*c1
    12*a**3*b*c1*d
    2*a*b**3*c1**2
    4*a**4*c1**2*d
    4*a**4*b*c1**2
    6*a**2*b**3*c1
    6*a**3*b*c1**2
    -4*a**4*c1**2*d
    -4*a**4*b*c1**2
    12*a**2*b**2*c1*d
    12*a**3*b*c1**2*d
    4*a**2*b**3*c1**2
    4*a*b**3*c1**2*d
    6*a**2*b**2*c1**2
    6*a**2*b*c1*d**2
    6*a**3*b**2*c1**2
    6*a**3*c1**2*d**2
    -12*a**3*b*c1**2*d
    -4*a**2*b**3*c1**2
    -4*a*b**3*c1**2*d
    -6*a**3*b**2*c1**2
    -6*a**3*c1**2*d**2
    12*a**2*b**2*c1**2*d
    12*a**2*b*c1**2*d**2
    6*a*b**2*c1**2*d**2
    -12*a**2*b**2*c1**2*d
    -12*a**2*b*c1**2*d**2
    -6*a*b**2*c1**2*d**2
    -a*c1*d*(12*a*b + c1*d**3)
    -4*a**2*c1*(3*a*b + c1*d**3)
    -4*a*b*c1*(3*a*b + c1*d**3)
    a**2*c1*(2*a**2*b + a*c0 + a + b)
    b**2*c1*(2*a**2*b + a*c0 + a + b)
    2*a*b*c1*(2*a**2*b + a*c0 + a + b)
    2*a*c1*d*(2*a**2*b + a*c0 + a + b)
    2*b*c1*d*(2*a**2*b + a*c0 + a + b)
    a**2*c1*(-8*a**2*b - a*c0 + 6*a*c1*d - a - b)
    b**2*c1*(-8*a**2*b - a*c0 + 6*a*c1*d - a - b)
    2*a*b*c1*(-8*a**2*b - a*c0 + 6*a*c1*d - a - b)
    2*a*c1*(6*a**2*b + a*c0 + 2*a*c1*d**3 + a + b)
    2*a*c1*d*(-8*a**2*b - a*c0 + 3*a*c1*d - a - b)
    2*b*c1*(6*a**2*b + a*c0 + 2*a*c1*d**3 + a + b)
    2*b*c1*d*(-8*a**2*b - a*c0 + 3*a*c1*d - a - b)
    c1*d*(12*a**2*b + 2*a*c0 + a*c1*d**3 + 2*a + 2*b)
    c1*(2*a**2*b*d**2 - 6*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    c1*(-8*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 + 2*a*c1*d**3 - a*d**2 - b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0079: log(z) + sinh(z)
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
    a*b**3*c1**2
    a*b**4*c1**2
    a*c1**2*d**3
    a*c1**2*d**4
    3*a**3*c1**2*d
    3*a**3*b*c1**2
    4*a**4*c1**2*d
    4*a**4*b*c1**2
    12*a**3*b*c1**2*d
    3*a**2*b**2*c1**2
    3*a**2*c1**2*d**2
    3*a*b**2*c1**2*d
    3*a*b*c1**2*d**2
    4*a**2*b**3*c1**2
    4*a**2*c1**2*d**3
    4*a*b**3*c1**2*d
    4*a*b*c1**2*d**3
    6*a**2*b*c1**2*d
    6*a**3*b**2*c1**2
    6*a**3*c1**2*d**2
    a**3*c1*(a*c0 + a + b)
    b**3*c1*(a*c0 + a + b)
    12*a**2*b**2*c1**2*d
    12*a**2*b*c1**2*d**2
    6*a*b**2*c1**2*d**2
    3*a**2*b*c1*(a*c0 + a + b)
    3*a**2*c1*d*(a*c0 + a + b)
    3*b**2*c1*d*(a*c0 + a + b)
    3*a*b**2*c1*(a*c0 + a + b)
    6*a*b*c1*d*(a*c0 + a + b)
    a**4*c1*(-a**2*b + a*c0 + a + b)
    b**4*c1*(-a**2*b + a*c0 + a + b)
    c1*d**4*(-a**2*b + a*c0 + a + b)
    4*a**3*b*c1*(-a**2*b + a*c0 + a + b)
    4*a**3*c1*d*(-a**2*b + a*c0 + a + b)
    4*b**3*c1*d*(-a**2*b + a*c0 + a + b)
    4*a*b**3*c1*(-a**2*b + a*c0 + a + b)
    4*a*c1*d**3*(-a**2*b + a*c0 + a + b)
    4*b*c1*d**3*(-a**2*b + a*c0 + a + b)
    12*a**2*b*c1*d*(-a**2*b + a*c0 + a + b)
    12*a*b**2*c1*d*(-a**2*b + a*c0 + a + b)
    12*a*b*c1*d**2*(-a**2*b + a*c0 + a + b)
    6*a**2*b**2*c1*(-a**2*b + a*c0 + a + b)
    6*a**2*c1*d**2*(-a**2*b + a*c0 + a + b)
    6*b**2*c1*d**2*(-a**2*b + a*c0 + a + b)
    c1*d*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    a*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    b*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0080: sin(z)*tanh(alpha*z)
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
    -6*a**2*alpha**2*b*c1
    c1*(6*a**2*alpha**2*b + a**2*b + a*c0 + a + b)
    alpha*c1*(2*a**2*alpha**2*b + 3*a**2*b + a*c0 + a + b)
    -alpha*c1*(8*a**2*alpha**2*b + 3*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0085: sin(z) + sinh(z)
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
    c1*(a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0087: tanh(sech(z))
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

## func_0088: exp(-z)*log(z)
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
    -a**7*c1**2
    a*b**5*c1**2
    a*c1**2*d**5
    -a*b**6*c1**2
    -a*c1**2*d**6
    5*a**5*c1**2*d
    5*a**5*b*c1**2
    -6*a**6*c1**2*d
    -6*a**6*b*c1**2
    10*a**3*b**3*c1**2
    10*a**3*c1**2*d**3
    10*a**4*b**2*c1**2
    10*a**4*c1**2*d**2
    20*a**4*b*c1**2*d
    5*a**2*b**4*c1**2
    5*a**2*c1**2*d**4
    5*a*b**4*c1**2*d
    5*a*b*c1**2*d**4
    -15*a**3*b**4*c1**2
    -15*a**3*c1**2*d**4
    -15*a**5*b**2*c1**2
    -15*a**5*c1**2*d**2
    -20*a**4*b**3*c1**2
    -20*a**4*c1**2*d**3
    -30*a**5*b*c1**2*d
    -6*a**2*b**5*c1**2
    -6*a**2*c1**2*d**5
    -6*a*b**5*c1**2*d
    -6*a*b*c1**2*d**5
    10*a*b**2*c1**2*d**3
    10*a*b**3*c1**2*d**2
    20*a**2*b**3*c1**2*d
    20*a**2*b*c1**2*d**3
    30*a**3*b**2*c1**2*d
    30*a**3*b*c1**2*d**2
    -15*a*b**2*c1**2*d**4
    -15*a*b**4*c1**2*d**2
    -20*a*b**3*c1**2*d**3
    -30*a**2*b**4*c1**2*d
    -30*a**2*b*c1**2*d**4
    -60*a**3*b**3*c1**2*d
    -60*a**3*b*c1**2*d**3
    -60*a**4*b**2*c1**2*d
    -60*a**4*b*c1**2*d**2
    30*a**2*b**2*c1**2*d**2
    -60*a**2*b**2*c1**2*d**3
    -60*a**2*b**3*c1**2*d**2
    -90*a**3*b**2*c1**2*d**2
    a**6*c1*(a**2*b - a*c0 - a - b)
    b**6*c1*(a**2*b - a*c0 - a - b)
    c1*d**6*(a**2*b - a*c0 - a - b)
    a**5*c1*(-3*a**2*b + a*c0 + a + b)
    b**5*c1*(-3*a**2*b + a*c0 + a + b)
    6*a**5*b*c1*(a**2*b - a*c0 - a - b)
    6*a**5*c1*d*(a**2*b - a*c0 - a - b)
    6*b**5*c1*d*(a**2*b - a*c0 - a - b)
    6*a*b**5*c1*(a**2*b - a*c0 - a - b)
    6*a*c1*d**5*(a**2*b - a*c0 - a - b)
    6*b*c1*d**5*(a**2*b - a*c0 - a - b)
    15*a**2*b**4*c1*(a**2*b - a*c0 - a - b)
    15*a**2*c1*d**4*(a**2*b - a*c0 - a - b)
    15*a**4*b**2*c1*(a**2*b - a*c0 - a - b)
    15*a**4*c1*d**2*(a**2*b - a*c0 - a - b)
    15*b**2*c1*d**4*(a**2*b - a*c0 - a - b)
    15*b**4*c1*d**2*(a**2*b - a*c0 - a - b)
    20*a**3*b**3*c1*(a**2*b - a*c0 - a - b)
    20*a**3*c1*d**3*(a**2*b - a*c0 - a - b)
    20*b**3*c1*d**3*(a**2*b - a*c0 - a - b)
    30*a**4*b*c1*d*(a**2*b - a*c0 - a - b)
    30*a*b**4*c1*d*(a**2*b - a*c0 - a - b)
    30*a*b*c1*d**4*(a**2*b - a*c0 - a - b)
    5*a**4*b*c1*(-3*a**2*b + a*c0 + a + b)
    5*a*b**4*c1*(-3*a**2*b + a*c0 + a + b)
    10*a**2*b**3*c1*(-3*a**2*b + a*c0 + a + b)
    10*a**3*b**2*c1*(-3*a**2*b + a*c0 + a + b)
    60*a**2*b**3*c1*d*(a**2*b - a*c0 - a - b)
    60*a**2*b*c1*d**3*(a**2*b - a*c0 - a - b)
    60*a**3*b**2*c1*d*(a**2*b - a*c0 - a - b)
    60*a**3*b*c1*d**2*(a**2*b - a*c0 - a - b)
    60*a*b**2*c1*d**3*(a**2*b - a*c0 - a - b)
    60*a*b**3*c1*d**2*(a**2*b - a*c0 - a - b)
    90*a**2*b**2*c1*d**2*(a**2*b - a*c0 - a - b)
    a**4*c1*(-15*a**2*b*d - 3*a**2*b + 5*a*c0*d + 5*a*d + 5*b*d)
    b**4*c1*(-15*a**2*b*d - 3*a**2*b + 5*a*c0*d + 5*a*d + 5*b*d)
    4*a**3*b*c1*(-15*a**2*b*d - 3*a**2*b + 5*a*c0*d + 5*a*d + 5*b*d)
    4*a*b**3*c1*(-15*a**2*b*d - 3*a**2*b + 5*a*c0*d + 5*a*d + 5*b*d)
    6*a**2*b**2*c1*(-15*a**2*b*d - 3*a**2*b + 5*a*c0*d + 5*a*d + 5*b*d)
    c1*d**3*(-3*a**2*b*d**2 - 3*a**2*b*d - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    2*a**3*c1*(-15*a**2*b*d**2 - 6*a**2*b*d - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*b**3*c1*(-15*a**2*b*d**2 - 6*a**2*b*d - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    6*a**2*b*c1*(-15*a**2*b*d**2 - 6*a**2*b*d - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    6*a*b**2*c1*(-15*a**2*b*d**2 - 6*a**2*b*d - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    a*c1*d**2*(-15*a**2*b*d**2 - 12*a**2*b*d - 6*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    b*c1*d**2*(-15*a**2*b*d**2 - 12*a**2*b*d - 6*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*a**2*c1*d*(-15*a**2*b*d**2 - 9*a**2*b*d - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*b**2*c1*d*(-15*a**2*b*d**2 - 9*a**2*b*d - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    4*a*b*c1*d*(-15*a**2*b*d**2 - 9*a**2*b*d - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0089: sin(alpha*z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a*alpha*c1**2
    2*alpha*c1*(4*a**2*alpha**2*b + a*c0 + a + b)
- sympy_solutions:
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0090: z**2 + sin(alpha*z)
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
    2*a**2*c1**2
    2*a**4*c1**2
    2*a*c1**2*d
    2*a*b*c1**2
    a**3*alpha*c1**2
    2*a*b**3*c1**2
    6*a**3*c1**2*d
    6*a**3*b*c1**2
    a*alpha*b**2*c1**2
    12*a**2*b*c1**2*d
    2*a**2*alpha*c1**2*d
    2*a**2*alpha*b*c1**2
    2*a*alpha*b*c1**2*d
    6*a**2*b**2*c1**2
    6*a*b**2*c1**2*d
    2*c1*d*(a*c0 + a*c1*d**2 + a + b)
    2*a*c1*(a*c0 + 3*a*c1*d**2 + a + b)
    2*b*c1*(a*c0 + 3*a*c1*d**2 + a + b)
    alpha*c1*(a**2*alpha**2*b + a*c0 + a*c1*d**2 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0094: tanh(sin(alpha*z))
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

## func_0097: z**3*exp(z)
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
    a*b**6*c1**2
    6*a**6*b*c1**2
    15*a**3*b**4*c1**2
    15*a**5*b**2*c1**2
    20*a**4*b**3*c1**2
    6*a**2*b**5*c1**2
    a*c1**2*d**5*(d + 3)
    15*a**5*c1**2*d*(d + 1)
    3*a**6*c1**2*(2*d + 1)
    15*a**3*c1**2*d**3*(d + 2)
    15*a**5*b*c1**2*(2*d + 1)
    15*a*b**4*c1**2*d*(d + 1)
    3*a*b**5*c1**2*(2*d + 1)
    60*a**4*b*c1**2*d*(d + 1)
    10*a**4*c1**2*d**2*(2*d + 3)
    15*a**2*b**4*c1**2*(2*d + 1)
    15*a*b**2*c1**2*d**3*(d + 2)
    3*a**2*c1**2*d**4*(2*d + 5)
    3*a*b*c1**2*d**4*(2*d + 5)
    30*a**2*b*c1**2*d**3*(d + 2)
    30*a**3*b**3*c1**2*(2*d + 1)
    30*a**4*b**2*c1**2*(2*d + 1)
    60*a**2*b**3*c1**2*d*(d + 1)
    90*a**3*b**2*c1**2*d*(d + 1)
    a**3*c1*(-a**2*b + a*c0 + a + b)
    b**3*c1*(-a**2*b + a*c0 + a + b)
    10*a*b**3*c1**2*d**2*(2*d + 3)
    30*a**3*b*c1**2*d**2*(2*d + 3)
    3*a**2*b*c1*(-a**2*b + a*c0 + a + b)
    3*a*b**2*c1*(-a**2*b + a*c0 + a + b)
    30*a**2*b**2*c1**2*d**2*(2*d + 3)
    3*a**2*c1*(-a**2*b*d - 3*a**2*b + a*c0*d + a*c0 + a*d + a + b*d + b)
    3*b**2*c1*(-a**2*b*d - 3*a**2*b + a*c0*d + a*c0 + a*d + a + b*d + b)
    6*a*b*c1*(-a**2*b*d - 3*a**2*b + a*c0*d + a*c0 + a*d + a + b*d + b)
    3*a*c1*(-a**2*b*d**2 - 6*a**2*b*d - 6*a**2*b + a*c0*d**2 + 2*a*c0*d + a*d**2 + 2*a*d + b*d**2 + 2*b*d)
    3*b*c1*(-a**2*b*d**2 - 6*a**2*b*d - 6*a**2*b + a*c0*d**2 + 2*a*c0*d + a*d**2 + 2*a*d + b*d**2 + 2*b*d)
    c1*(-a**2*b*d**3 - 9*a**2*b*d**2 - 18*a**2*b*d - 6*a**2*b + a*c0*d**3 + 3*a*c0*d**2 + a*d**3 + 3*a*d**2 + b*d**3 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0098: tan(z)*sech(z)
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
    c1*(a**2*b - a*c0 - a - b)
    c1*(a**2*b + a*c0 + a + b)
    c1*(-5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0099: sinh(z)*JacobiDN(z, m)
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
    -6*a**2*b*c1*m
    6*a**2*b*c1*m**2
    c1*(3*a**2*b*m - a**2*b + a*c0 + a + b)
    -c1*m*(a**2*b*m + a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0100: z**2 + tan(z)
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
    2*a*b*c1**2
    a*b**2*c1**2
    -6*a**2*b*c1
    2*a**2*c1**2*d
    2*a**2*b*c1**2
    2*a*b**3*c1**2
    2*a*b*c1**2*d
    6*a**3*b*c1**2
    a*c1**2*(2*d + 1)
    6*a**2*b**2*c1**2
    a**3*c1**2*(6*d + 1)
    a*b**2*c1**2*(6*d + 1)
    2*a**2*b*c1**2*(6*d + 1)
    c1*(-8*a**2*b + a*c0 + a*c1*d**2 + a + b)
    2*a*c1*(a*c0 + 3*a*c1*d**2 + a*c1*d + a + b)
    2*b*c1*(a*c0 + 3*a*c1*d**2 + a*c1*d + a + b)
    c1*(-2*a**2*b + 2*a*c0*d + a*c0 + 2*a*c1*d**3 + a*c1*d**2 + 2*a*d + a + 2*b*d + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

