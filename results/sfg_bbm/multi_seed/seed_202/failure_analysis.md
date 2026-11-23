# BBM [2,1] failure analysis

Candidates with `solve_status=success` do not automatically satisfy the
original PDE. This file records every downstream stage separately.

## func_0001: tanh(sin(alpha*z))
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

## func_0002: cosh(z) + JacobiDN(z, m)
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

## func_0003: tanh(exp(-z))
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

## func_0004: tanh(z**2)
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

## func_0005: tanh(z)*JacobiDN(z, m)
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
    a*c1**2*m
    -a*c1**2*m
    6*a**2*b*c1
    6*a**2*b*c1*m
    -6*a**2*b*c1*m
    6*a**2*b*c1*m**2
    c1*(3*a**2*b*m + 2*a**2*b + a*c0 + a + b)
    -c1*(3*a**2*b*m + 8*a**2*b + a*c0 + a + b)
    -c1*m*(a**2*b*m + 10*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0006: cos(z) + coth(z)
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

## func_0008: tanh(sech(z))
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

## func_0009: coth(z)**2
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

## func_0010: tanh(tanh(z))
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

## func_0011: z**2 + log(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a**6*c1**2
    2*a**8*c1**2
    10*a**5*c1**2*d
    10*a**5*b*c1**2
    14*a**7*c1**2*d
    14*a**7*b*c1**2
    2*a*b**5*c1**2
    2*a*b**7*c1**2
    10*a**2*b**4*c1**2
    10*a*b**4*c1**2*d
    14*a**2*b**6*c1**2
    14*a*b**6*c1**2*d
    20*a**3*b**3*c1**2
    20*a**4*b**2*c1**2
    40*a**4*b*c1**2*d
    42*a**3*b**5*c1**2
    42*a**6*b**2*c1**2
    70*a**4*b**4*c1**2
    70*a**5*b**3*c1**2
    84*a**6*b*c1**2*d
    210*a**3*b**4*c1**2*d
    210*a**5*b**2*c1**2*d
    280*a**4*b**3*c1**2*d
    40*a**2*b**3*c1**2*d
    60*a**3*b**2*c1**2*d
    84*a**2*b**5*c1**2*d
    a**4*c1**2*(20*d**2 + 1)
    a**3*c1**2*d*(20*d**2 + 3)
    a*b**3*c1**2*(20*d**2 + 1)
    a*c1**2*d**3*(2*d**2 + 1)
    3*a**3*b*c1**2*(20*d**2 + 1)
    a**2*c1**2*d**2*(10*d**2 + 3)
    a*b**2*c1**2*d*(20*d**2 + 3)
    a*b*c1**2*d**2*(10*d**2 + 3)
    2*a**2*b*c1**2*d*(20*d**2 + 3)
    3*a**2*b**2*c1**2*(20*d**2 + 1)
    a**5*c1*(2*a*c0 + 42*a*c1*d**2 + a*c1 + 2*a + 2*b)
    b**5*c1*(2*a*c0 + 42*a*c1*d**2 + a*c1 + 2*a + 2*b)
    5*a**4*b*c1*(2*a*c0 + 42*a*c1*d**2 + a*c1 + 2*a + 2*b)
    5*a**4*c1*d*(2*a*c0 + 14*a*c1*d**2 + a*c1 + 2*a + 2*b)
    5*b**4*c1*d*(2*a*c0 + 14*a*c1*d**2 + a*c1 + 2*a + 2*b)
    5*a*b**4*c1*(2*a*c0 + 42*a*c1*d**2 + a*c1 + 2*a + 2*b)
    10*a**2*b**3*c1*(2*a*c0 + 42*a*c1*d**2 + a*c1 + 2*a + 2*b)
    10*a**3*b**2*c1*(2*a*c0 + 42*a*c1*d**2 + a*c1 + 2*a + 2*b)
    20*a**3*b*c1*d*(2*a*c0 + 14*a*c1*d**2 + a*c1 + 2*a + 2*b)
    20*a*b**3*c1*d*(2*a*c0 + 14*a*c1*d**2 + a*c1 + 2*a + 2*b)
    30*a**2*b**2*c1*d*(2*a*c0 + 14*a*c1*d**2 + a*c1 + 2*a + 2*b)
    a**3*c1*(20*a*c0*d**2 + a*c0 + 70*a*c1*d**4 + 10*a*c1*d**2 + 20*a*d**2 + a + 20*b*d**2 + b)
    b**3*c1*(20*a*c0*d**2 + a*c0 + 70*a*c1*d**4 + 10*a*c1*d**2 + 20*a*d**2 + a + 20*b*d**2 + b)
    3*a**2*b*c1*(20*a*c0*d**2 + a*c0 + 70*a*c1*d**4 + 10*a*c1*d**2 + 20*a*d**2 + a + 20*b*d**2 + b)
    3*a*b**2*c1*(20*a*c0*d**2 + a*c0 + 70*a*c1*d**4 + 10*a*c1*d**2 + 20*a*d**2 + a + 20*b*d**2 + b)
    a**2*c1*d*(20*a*c0*d**2 + 3*a*c0 + 42*a*c1*d**4 + 10*a*c1*d**2 + 20*a*d**2 + 3*a + 20*b*d**2 + 3*b)
    b**2*c1*d*(20*a*c0*d**2 + 3*a*c0 + 42*a*c1*d**4 + 10*a*c1*d**2 + 20*a*d**2 + 3*a + 20*b*d**2 + 3*b)
    2*a*b*c1*d*(20*a*c0*d**2 + 3*a*c0 + 42*a*c1*d**4 + 10*a*c1*d**2 + 20*a*d**2 + 3*a + 20*b*d**2 + 3*b)
    c1*d*(-2*a**2*b + 2*a*c0*d**4 + a*c0*d**2 + 2*a*c1*d**6 + a*c1*d**4 + 2*a*d**4 + a*d**2 + 2*b*d**4 + b*d**2)
    a*c1*(-2*a**2*b + 10*a*c0*d**4 + 3*a*c0*d**2 + 14*a*c1*d**6 + 5*a*c1*d**4 + 10*a*d**4 + 3*a*d**2 + 10*b*d**4 + 3*b*d**2)
    b*c1*(-2*a**2*b + 10*a*c0*d**4 + 3*a*c0*d**2 + 14*a*c1*d**6 + 5*a*c1*d**4 + 10*a*d**4 + 3*a*d**2 + 10*b*d**4 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0012: sin(z)*cosh(z)*JacobiDN(z, m)
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
    6*a**2*b*c1*m
    -6*a**2*b*c1*m
    6*a**2*b*c1*m**2
    c1*(3*a**2*b*m - 2*a**2*b + a*c0 + a + b)
    c1*(3*a**2*b*m + 2*a**2*b + a*c0 + a + b)
    -c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0013: z**4
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

## func_0014: z + exp(z)
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
    c1*(-a**2*b + a*c0 + a*c1*d + a*c1 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0015: exp(-2*z)
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

## func_0016: cosh(z)**2
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

## func_0017: sin(z)*cosh(z) + tan(z)
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
    c1*(-2*a**2*b + a*c0 + a + b)
    c1*(-8*a**2*b + a*c0 + a + b)
    c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0018: sin(z)**2
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

## func_0019: tanh(z) + JacobiDN(z, m)
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
    -a*c1**2*m
    6*a**2*b*c1
    6*a**2*b*c1*m**2
    c1*(2*a**2*b + a*c0 + a + b)
    -c1*(8*a**2*b + a*c0 + a + b)
    -c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0020: sin(alpha*z)*tan(z)
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
    -6*a**2*b*c1
    -6*a**2*alpha*b*c1
    alpha*c1*(a**2*alpha**2*b - 6*a**2*b + a*c0 + a + b)
    c1*(3*a**2*alpha**2*b - 2*a**2*b + a*c0 + a + b)
    c1*(3*a**2*alpha**2*b - 8*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0021: tanh(tanh(z)*sech(z))
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

## func_0023: tan(z) + cosh(z)
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
    c1*(-2*a**2*b + a*c0 + a + b)
    c1*(-8*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0024: exp(-2*z**2)
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

## func_0026: cos(z)*sech(z)**2
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
    4*a*c1**2
    -2*a*c1**2
    -18*a**2*b*c1
    -24*a**2*b*c1
    c1*(25*a**2*b + a*c0 + a + b)
    -c1*(7*a**2*b + a*c0 + a + b)
    2*c1*(23*a**2*b + a*c0 + a + b)
    -2*c1*(11*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0027: tanh(z**3)
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

## func_0029: tanh(log(z))
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

## func_0030: tanh(csch(z))
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

## func_0032: z**2
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

## func_0033: z*sech(z)
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
    -a**2*c1**2
    -a**3*c1**2
    -a*c1**2*d
    -a*b*c1**2
    6*a**3*b*c1
    a*b**2*c1**2
    a*c1**2*d**2
    -6*a**2*b*c1
    -a*b**2*c1**2
    -a*c1**2*d**2
    2*a**2*c1**2*d
    2*a**2*b*c1**2
    2*a*b*c1**2*d
    6*a**2*b**2*c1
    6*a**2*b*c1*d
    -2*a**2*c1**2*d
    -2*a**2*b*c1**2
    -2*a*b*c1**2*d
    c1*(3*a**2*b + a*c0 + a + b)
    -a*c1*(5*a**2*b + a*c0 + a + b)
    -b*c1*(5*a**2*b + a*c0 + a + b)
    -c1*d*(5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0034: z*sin(z)*cosh(z)
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
    c1*(a*c0 + a + b)
    -6*a**2*b*c1
    2*a**2*c1**2*d
    2*a**2*b*c1**2
    2*a*b*c1**2*d
    a*c1*(-2*a**2*b + a*c0 + a + b)
    a*c1*(2*a**2*b + a*c0 + a + b)
    b*c1*(-2*a**2*b + a*c0 + a + b)
    b*c1*(2*a**2*b + a*c0 + a + b)
    c1*d*(-2*a**2*b + a*c0 + a + b)
    c1*d*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0035: sin(z)*cosh(z)*JacobiSN(z, m)
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

## func_0036: sinh(z)*sech(z)
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

## func_0037: exp(-z)*tan(z)
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
    c1*(-11*a**2*b + a*c0 + a + b)
    c1*(-5*a**2*b + a*c0 + a + b)
    c1*(7*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0041: tanh(JacobiDN(z, m))
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

## func_0042: exp(z)*tanh(z)*sech(z)
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
    -3*a*c1**2
    24*a**2*b*c1
    -18*a**2*b*c1
    c1*(14*a**2*b + a*c0 + a + b)
    c1*(2*a**2*b + a*c0 + a + b)
    -2*c1*(11*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0043: tanh(exp(-z**2))
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

## func_0044: z**3 + csch(z)
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
    -a**4*c1**2
    2*a**2*b*c1
    3*a**2*b*c1
    3*a**3*c1**2
    3*a**6*c1**2
    -a*b**3*c1**2
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    3*a*b**2*c1**2
    3*a*b**5*c1**2
    3*a*c1**2*d**2
    6*a**2*c1**2*d
    6*a**2*b*c1**2
    6*a*b*c1**2*d
    -3*a**3*c1**2*d
    -3*a**3*b*c1**2
    15*a**2*b**4*c1**2
    15*a*b**4*c1**2*d
    30*a**3*b**3*c1**2
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    60*a**4*b*c1**2*d
    -3*a**2*b**2*c1**2
    -3*a**2*c1**2*d**2
    -3*a*b**2*c1**2*d
    -3*a*b*c1**2*d**2
    -6*a**2*b*c1**2*d
    30*a*b**3*c1**2*d**2
    60*a**2*b**3*c1**2*d
    90*a**3*b**2*c1**2*d
    90*a**3*b*c1**2*d**2
    90*a**2*b**2*c1**2*d**2
    -c1*(a*c0 + a*c1*d**3 + a + b)
    3*a**2*c1*(a*c0 + 10*a*c1*d**3 + a + b)
    3*b**2*c1*(a*c0 + 10*a*c1*d**3 + a + b)
    6*a*b*c1*(a*c0 + 10*a*c1*d**3 + a + b)
    3*a*c1*d*(2*a*c0 + 5*a*c1*d**3 + 2*a + 2*b)
    3*b*c1*d*(2*a*c0 + 5*a*c1*d**3 + 2*a + 2*b)
    3*c1*(-2*a**2*b + a*c0*d**2 + a*c1*d**5 + a*d**2 + b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0045: tanh(z)
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

## func_0047: tanh(coth(z))
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

## func_0049: sin(z) + tan(z)
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
    c1*(a**2*b + a*c0 + a + b)
    c1*(-2*a**2*b + a*c0 + a + b)
    c1*(-8*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0052: log(z) + JacobiCN(z, m)
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
    6*a**6*b*c1*m
    -4*a**4*c1**2*d
    -4*a**4*b*c1**2
    24*a**3*b**4*c1*m
    24*a**5*b**2*c1*m
    24*a**5*b*c1*d*m
    3*a**2*b**2*c1**2
    3*a**2*c1**2*d**2
    3*a*b**2*c1**2*d
    3*a*b*c1**2*d**2
    36*a**4*b**3*c1*m
    6*a**2*b**5*c1*m
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
    24*a**2*b**4*c1*d*m
    24*a**3*b*c1*d**3*m
    36*a**4*b*c1*d**2*m
    6*a**2*b*c1*d**4*m
    72*a**3*b**3*c1*d*m
    72*a**4*b**2*c1*d*m
    -12*a**2*b**2*c1**2*d
    -12*a**2*b*c1**2*d**2
    -6*a*b**2*c1**2*d**2
    24*a**2*b**2*c1*d**3*m
    3*a**2*b*c1*(a*c0 + a + b)
    3*a**2*c1*d*(a*c0 + a + b)
    3*b**2*c1*d*(a*c0 + a + b)
    3*a*b**2*c1*(a*c0 + a + b)
    36*a**2*b**3*c1*d**2*m
    6*a*b*c1*d*(a*c0 + a + b)
    72*a**3*b**2*c1*d**2*m
    -a**4*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -b**4*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -c1*d**4*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    c1*d*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    -4*a**3*b*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -4*a**3*c1*d*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -4*b**3*c1*d*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -4*a*b**3*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -4*a*c1*d**3*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -4*b*c1*d**3*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -12*a**2*b*c1*d*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -12*a*b**2*c1*d*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -12*a*b*c1*d**2*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -6*a**2*b**2*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -6*a**2*c1*d**2*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -6*b**2*c1*d**2*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    a*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    b*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0053: tanh(sin(z)*cosh(z))
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

## func_0054: JacobiCN(z, m)*csch(z)
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
    6*a**2*b*c1*m
    -c1*(3*a**2*b + a*c0 + a + b)
    -c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0060: log(z) + tanh(alpha*z)
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

## func_0063: z*sech(alpha*z)**2
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
    -2*a**2*c1**2
    -2*a*b*c1**2
    4*a**3*alpha*c1**2
    -2*a**3*alpha*c1**2
    4*a*alpha*b**2*c1**2
    8*a**2*alpha*b*c1**2
    -2*a*alpha*b**2*c1**2
    -4*a**2*alpha*b*c1**2
    a*c1*(18*a*alpha**2*b + c1*d)
    -2*a*alpha*c1*d*(12*a*alpha**2*b + c1*d)
    -4*a**2*alpha*c1*(6*a*alpha**2*b + c1*d)
    -4*a*alpha*b*c1*(6*a*alpha**2*b + c1*d)
    c1*(6*a**2*alpha**2*b + a*c0 + a*c1*d + a + b)
    -c1*(24*a**2*alpha**2*b + a*c0 + 2*a*c1*d + a + b)
    -2*alpha*c1*d*(8*a**2*alpha**2*b + a*c0 + a*c1*d + a + b)
    2*a*alpha*c1*(20*a**2*alpha**2*b + a*c0 + 4*a*c1*d + a + b)
    2*alpha*b*c1*(20*a**2*alpha**2*b + a*c0 + 4*a*c1*d + a + b)
    2*alpha*c1*d*(20*a**2*alpha**2*b + a*c0 + 2*a*c1*d + a + b)
    -2*a*alpha*c1*(8*a**2*alpha**2*b + a*c0 + 2*a*c1*d + a + b)
    -2*alpha*b*c1*(8*a**2*alpha**2*b + a*c0 + 2*a*c1*d + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0064: sech(alpha*z)**4
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

## func_0065: cos(z) + exp(-z)
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
    c1*(a**2*b - a*c0 - a - b)
    -c1*(a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0068: tanh(sin(z))
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

## func_0070: tanh(sinh(z))
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

## func_0071: tan(z) + tanh(alpha*z)
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
    -a*alpha*c1**2
    a*c1**2*(alpha + 1)
    -6*a**2*b*c1
    6*a**2*alpha**3*b*c1
    c1*(-8*a**2*b + a*c0 + a + b)
    -alpha*c1*(8*a**2*alpha**2*b + a*c0 + a + b)
    c1*(2*a**2*alpha**3*b - 2*a**2*b + a*alpha*c0 + a*alpha + a*c0 + a + alpha*b + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0073: exp(z) + cos(z)
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
    c1*(-a**2*b + a*c0 + a + b)
    -c1*(a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0074: log(z) + JacobiSN(z, m)
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
    -6*a**6*b*c1*m
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
    -24*a**3*b**4*c1*m
    -24*a**5*b**2*c1*m
    -24*a**5*b*c1*d*m
    -36*a**4*b**3*c1*m
    -6*a**2*b**5*c1*m
    12*a**2*b**2*c1**2*d
    12*a**2*b*c1**2*d**2
    6*a*b**2*c1**2*d**2
    -24*a**2*b**4*c1*d*m
    -24*a**3*b*c1*d**3*m
    -36*a**4*b*c1*d**2*m
    -6*a**2*b*c1*d**4*m
    -72*a**3*b**3*c1*d*m
    -72*a**4*b**2*c1*d*m
    3*a**2*b*c1*(a*c0 + a + b)
    3*a**2*c1*d*(a*c0 + a + b)
    3*b**2*c1*d*(a*c0 + a + b)
    3*a*b**2*c1*(a*c0 + a + b)
    6*a*b*c1*d*(a*c0 + a + b)
    -24*a**2*b**2*c1*d**3*m
    -36*a**2*b**3*c1*d**2*m
    -72*a**3*b**2*c1*d**2*m
    a**4*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    b**4*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    c1*d**4*(a**2*b*m + a**2*b + a*c0 + a + b)
    4*a**3*b*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    4*a**3*c1*d*(a**2*b*m + a**2*b + a*c0 + a + b)
    4*b**3*c1*d*(a**2*b*m + a**2*b + a*c0 + a + b)
    4*a*b**3*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    4*a*c1*d**3*(a**2*b*m + a**2*b + a*c0 + a + b)
    4*b*c1*d**3*(a**2*b*m + a**2*b + a*c0 + a + b)
    c1*d*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    12*a**2*b*c1*d*(a**2*b*m + a**2*b + a*c0 + a + b)
    12*a*b**2*c1*d*(a**2*b*m + a**2*b + a*c0 + a + b)
    12*a*b*c1*d**2*(a**2*b*m + a**2*b + a*c0 + a + b)
    6*a**2*b**2*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    6*a**2*c1*d**2*(a**2*b*m + a**2*b + a*c0 + a + b)
    6*b**2*c1*d**2*(a**2*b*m + a**2*b + a*c0 + a + b)
    a*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    b*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0076: sin(z)*cosh(z) + tanh(z)
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
    c1*(-2*a**2*b + a*c0 + a + b)
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

## func_0077: exp(-z)*sin(z)
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

## func_0079: csch(z)**2
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

## func_0080: z**3 + coth(z)
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
    -a**4*c1**2
    3*a**3*c1**2
    3*a**6*c1**2
    6*a**2*b*c1
    -a*b**3*c1**2
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    3*a*b**2*c1**2
    3*a*b**5*c1**2
    3*a*c1**2*d**2
    6*a**2*c1**2*d
    6*a**2*b*c1**2
    6*a*b*c1**2*d
    -3*a**3*c1**2*d
    -3*a**3*b*c1**2
    15*a**2*b**4*c1**2
    15*a*b**4*c1**2*d
    30*a**3*b**3*c1**2
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    60*a**4*b*c1**2*d
    -3*a**2*b**2*c1**2
    -3*a**2*c1**2*d**2
    -3*a*b**2*c1**2*d
    -3*a*b*c1**2*d**2
    -6*a**2*b*c1**2*d
    30*a*b**3*c1**2*d**2
    60*a**2*b**3*c1**2*d
    90*a**3*b**2*c1**2*d
    90*a**3*b*c1**2*d**2
    90*a**2*b**2*c1**2*d**2
    3*a**2*c1*(a*c0 + 10*a*c1*d**3 + a + b)
    3*b**2*c1*(a*c0 + 10*a*c1*d**3 + a + b)
    6*a*b*c1*(a*c0 + 10*a*c1*d**3 + a + b)
    -c1*(2*a**2*b + a*c0 + a*c1*d**3 + a + b)
    3*a*c1*d*(2*a*c0 + 5*a*c1*d**3 + 2*a + 2*b)
    3*b*c1*d*(2*a*c0 + 5*a*c1*d**3 + 2*a + 2*b)
    3*c1*(-2*a**2*b + a*c0*d**2 + a*c1*d**5 + a*d**2 + b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0081: sin(z) + cos(z)
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

## func_0083: tanh(exp(z))
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

## func_0084: tanh(sech(z)**2)
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

## func_0085: tanh(tan(z))
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

## func_0086: log(z) + sech(z)**2
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
    2*a**5*c1**2
    a*b**3*c1**2
    a*c1**2*d**3
    -2*a**5*c1**2
    -a*b**3*c1**2
    -a*c1**2*d**3
    2*a*b**4*c1**2
    2*a*c1**2*d**4
    3*a**3*c1**2*d
    3*a**3*b*c1**2
    8*a**4*c1**2*d
    8*a**4*b*c1**2
    -2*a*b**4*c1**2
    -2*a*c1**2*d**4
    -3*a**3*c1**2*d
    -3*a**3*b*c1**2
    -8*a**4*c1**2*d
    -8*a**4*b*c1**2
    12*a**3*b**2*c1**2
    12*a**3*c1**2*d**2
    24*a**3*b*c1**2*d
    3*a**2*b**2*c1**2
    3*a**2*c1**2*d**2
    3*a*b**2*c1**2*d
    3*a*b*c1**2*d**2
    6*a**2*b*c1**2*d
    8*a**2*b**3*c1**2
    8*a**2*c1**2*d**3
    8*a*b**3*c1**2*d
    8*a*b*c1**2*d**3
    -12*a**3*b**2*c1**2
    -12*a**3*c1**2*d**2
    -24*a**3*b*c1**2*d
    -3*a**2*b**2*c1**2
    -3*a**2*c1**2*d**2
    -3*a*b**2*c1**2*d
    -3*a*b*c1**2*d**2
    -6*a**2*b*c1**2*d
    -8*a**2*b**3*c1**2
    -8*a**2*c1**2*d**3
    -8*a*b**3*c1**2*d
    -8*a*b*c1**2*d**3
    12*a*b**2*c1**2*d**2
    24*a**2*b**2*c1**2*d
    24*a**2*b*c1**2*d**2
    -12*a*b**2*c1**2*d**2
    -2*a**5*c1*(12*a*b + c1)
    -24*a**2*b**2*c1**2*d
    -24*a**2*b*c1**2*d**2
    a**3*c1*(a*c0 + a*c1 + a + b)
    b**3*c1*(a*c0 + a*c1 + a + b)
    -2*a*b**4*c1*(12*a*b + c1)
    -2*a*c1*d**4*(12*a*b + c1)
    -8*a**4*b*c1*(12*a*b + c1)
    -8*a**4*c1*d*(12*a*b + c1)
    -12*a**3*b**2*c1*(12*a*b + c1)
    -12*a**3*c1*d**2*(12*a*b + c1)
    -24*a**3*b*c1*d*(12*a*b + c1)
    -8*a**2*b**3*c1*(12*a*b + c1)
    -8*a**2*c1*d**3*(12*a*b + c1)
    -8*a*b**3*c1*d*(12*a*b + c1)
    -8*a*b*c1*d**3*(12*a*b + c1)
    3*a**2*b*c1*(a*c0 + a*c1 + a + b)
    3*a**2*c1*d*(a*c0 + a*c1 + a + b)
    3*b**2*c1*d*(a*c0 + a*c1 + a + b)
    3*a*b**2*c1*(a*c0 + a*c1 + a + b)
    6*a*b*c1*d*(a*c0 + a*c1 + a + b)
    -12*a*b**2*c1*d**2*(12*a*b + c1)
    -24*a**2*b**2*c1*d*(12*a*b + c1)
    -24*a**2*b*c1*d**2*(12*a*b + c1)
    -2*a**4*c1*(8*a**2*b + a*c0 + a*c1 + a + b)
    -2*b**4*c1*(8*a**2*b + a*c0 + a*c1 + a + b)
    -2*c1*d**4*(8*a**2*b + a*c0 + a*c1 + a + b)
    2*a**4*c1*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    2*b**4*c1*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    2*c1*d**4*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    -8*a**3*b*c1*(8*a**2*b + a*c0 + a*c1 + a + b)
    -8*a**3*c1*d*(8*a**2*b + a*c0 + a*c1 + a + b)
    -8*b**3*c1*d*(8*a**2*b + a*c0 + a*c1 + a + b)
    -8*a*b**3*c1*(8*a**2*b + a*c0 + a*c1 + a + b)
    -8*a*c1*d**3*(8*a**2*b + a*c0 + a*c1 + a + b)
    -8*b*c1*d**3*(8*a**2*b + a*c0 + a*c1 + a + b)
    8*a**3*b*c1*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    8*a**3*c1*d*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    8*b**3*c1*d*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    8*a*b**3*c1*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    8*a*c1*d**3*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    8*b*c1*d**3*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    -12*a**2*b**2*c1*(8*a**2*b + a*c0 + a*c1 + a + b)
    -12*a**2*c1*d**2*(8*a**2*b + a*c0 + a*c1 + a + b)
    -12*b**2*c1*d**2*(8*a**2*b + a*c0 + a*c1 + a + b)
    -24*a**2*b*c1*d*(8*a**2*b + a*c0 + a*c1 + a + b)
    -24*a*b**2*c1*d*(8*a**2*b + a*c0 + a*c1 + a + b)
    -24*a*b*c1*d**2*(8*a**2*b + a*c0 + a*c1 + a + b)
    12*a**2*b**2*c1*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    12*a**2*c1*d**2*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    12*b**2*c1*d**2*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    24*a**2*b*c1*d*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    24*a*b**2*c1*d*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    24*a*b*c1*d**2*(20*a**2*b + a*c0 + 2*a*c1 + a + b)
    c1*d*(-2*a**2*b + a*c0*d**2 + a*c1*d**2 + a*d**2 + b*d**2)
    a*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*c1*d**2 + 3*a*d**2 + 3*b*d**2)
    b*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*c1*d**2 + 3*a*d**2 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0087: tanh(alpha*z) + JacobiDN(z, m)
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

## func_0089: z**3*JacobiCN(z, m)
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
    -3*a**6*c1**2
    -a*b**6*c1**2
    -a*c1**2*d**6
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    3*a*b**5*c1**2
    3*a*c1**2*d**5
    6*a**5*b*c1*m
    -15*a**5*c1**2*d
    -15*a**5*b*c1**2
    -18*a**4*b*c1*m
    -3*a*b**5*c1**2
    -3*a*c1**2*d**5
    -6*a**6*c1**2*d
    -6*a**6*b*c1**2
    15*a**2*b**4*c1**2
    15*a**2*c1**2*d**4
    15*a*b**4*c1**2*d
    15*a*b*c1**2*d**4
    18*a**3*b**3*c1*m
    18*a**4*b**2*c1*m
    18*a**4*b*c1*d*m
    30*a**3*b**3*c1**2
    30*a**3*c1**2*d**3
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    6*a**2*b**4*c1*m
    60*a**4*b*c1**2*d
    -15*a**2*b**4*c1**2
    -15*a**2*c1**2*d**4
    -15*a**3*b**4*c1**2
    -15*a**3*c1**2*d**4
    -15*a**5*b**2*c1**2
    -15*a**5*c1**2*d**2
    -15*a*b**4*c1**2*d
    -15*a*b*c1**2*d**4
    -18*a**2*b**3*c1*m
    -20*a**4*b**3*c1**2
    -20*a**4*c1**2*d**3
    -30*a**3*b**3*c1**2
    -30*a**3*c1**2*d**3
    -30*a**4*b**2*c1**2
    -30*a**4*c1**2*d**2
    -30*a**5*b*c1**2*d
    -36*a**3*b**2*c1*m
    -36*a**3*b*c1*d*m
    -6*a**2*b**5*c1**2
    -6*a**2*c1**2*d**5
    -6*a*b**5*c1**2*d
    -6*a*b*c1**2*d**5
    -60*a**4*b*c1**2*d
    18*a**2*b**3*c1*d*m
    18*a**3*b*c1*d**2*m
    30*a*b**2*c1**2*d**3
    30*a*b**3*c1**2*d**2
    36*a**3*b**2*c1*d*m
    6*a**2*b*c1*d**3*m
    60*a**2*b**3*c1**2*d
    60*a**2*b*c1**2*d**3
    90*a**3*b**2*c1**2*d
    90*a**3*b*c1**2*d**2
    -15*a*b**2*c1**2*d**4
    -15*a*b**4*c1**2*d**2
    -18*a**2*b*c1*d**2*m
    -20*a*b**3*c1**2*d**3
    -30*a**2*b**4*c1**2*d
    -30*a**2*b*c1**2*d**4
    -30*a*b**2*c1**2*d**3
    -30*a*b**3*c1**2*d**2
    -36*a**2*b**2*c1*d*m
    -60*a**2*b**3*c1**2*d
    -60*a**2*b*c1**2*d**3
    -60*a**3*b**3*c1**2*d
    -60*a**3*b*c1**2*d**3
    -60*a**4*b**2*c1**2*d
    -60*a**4*b*c1**2*d**2
    -90*a**3*b**2*c1**2*d
    -90*a**3*b*c1**2*d**2
    18*a**2*b**2*c1*d**2*m
    90*a**2*b**2*c1**2*d**2
    -60*a**2*b**2*c1**2*d**3
    -60*a**2*b**3*c1**2*d**2
    -90*a**2*b**2*c1**2*d**2
    -90*a**3*b**2*c1**2*d**2
    3*a**2*c1*(3*a**2*b + a*c0 + a + b)
    3*b**2*c1*(3*a**2*b + a*c0 + a + b)
    6*a*b*c1*(3*a**2*b + a*c0 + a + b)
    6*a*c1*d*(3*a**2*b + a*c0 + a + b)
    6*b*c1*d*(3*a**2*b + a*c0 + a + b)
    -a**3*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -b**3*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -3*a**2*b*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -3*a**2*c1*d*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -3*b**2*c1*d*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -3*a*b**2*c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -6*a*b*c1*d*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    3*c1*(3*a**2*b*d**2 - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    c1*d*(-4*a**2*b*d**2*m - a**2*b*d**2 + 18*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*a*c1*(-4*a**2*b*d**2*m - a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*b*c1*(-4*a**2*b*d**2*m - a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0090: z**3*sech(z)
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
    -a**7*c1**2
    3*a**6*c1**2
    6*a**5*b*c1
    a*b**6*c1**2
    a*c1**2*d**6
    -18*a**4*b*c1
    -3*a**6*c1**2
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
    6*a**6*c1**2*d
    6*a**6*b*c1**2
    -15*a**5*c1**2*d
    -15*a**5*b*c1**2
    -18*a**2*b**3*c1
    -3*a*b**5*c1**2
    -3*a*c1**2*d**5
    -36*a**3*b**2*c1
    -36*a**3*b*c1*d
    -6*a**6*c1**2*d
    -6*a**6*b*c1**2
    15*a**2*b**4*c1**2
    15*a**2*c1**2*d**4
    15*a**3*b**4*c1**2
    15*a**3*c1**2*d**4
    15*a**5*b**2*c1**2
    15*a**5*c1**2*d**2
    15*a*b**4*c1**2*d
    15*a*b*c1**2*d**4
    18*a**2*b**3*c1*d
    18*a**3*b*c1*d**2
    20*a**4*b**3*c1**2
    20*a**4*c1**2*d**3
    30*a**3*b**3*c1**2
    30*a**3*c1**2*d**3
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    30*a**5*b*c1**2*d
    36*a**3*b**2*c1*d
    6*a**2*b**5*c1**2
    6*a**2*c1**2*d**5
    6*a**2*b*c1*d**3
    6*a*b**5*c1**2*d
    6*a*b*c1**2*d**5
    60*a**4*b*c1**2*d
    -15*a**2*b**4*c1**2
    -15*a**2*c1**2*d**4
    -15*a**3*b**4*c1**2
    -15*a**3*c1**2*d**4
    -15*a**5*b**2*c1**2
    -15*a**5*c1**2*d**2
    -15*a*b**4*c1**2*d
    -15*a*b*c1**2*d**4
    -18*a**2*b*c1*d**2
    -20*a**4*b**3*c1**2
    -20*a**4*c1**2*d**3
    -30*a**3*b**3*c1**2
    -30*a**3*c1**2*d**3
    -30*a**4*b**2*c1**2
    -30*a**4*c1**2*d**2
    -30*a**5*b*c1**2*d
    -36*a**2*b**2*c1*d
    -6*a**2*b**5*c1**2
    -6*a**2*c1**2*d**5
    -6*a*b**5*c1**2*d
    -6*a*b*c1**2*d**5
    -60*a**4*b*c1**2*d
    15*a*b**2*c1**2*d**4
    15*a*b**4*c1**2*d**2
    18*a**2*b**2*c1*d**2
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
    -15*a*b**2*c1**2*d**4
    -15*a*b**4*c1**2*d**2
    -20*a*b**3*c1**2*d**3
    -30*a**2*b**4*c1**2*d
    -30*a**2*b*c1**2*d**4
    -30*a*b**2*c1**2*d**3
    -30*a*b**3*c1**2*d**2
    -60*a**2*b**3*c1**2*d
    -60*a**2*b*c1**2*d**3
    -60*a**3*b**3*c1**2*d
    -60*a**3*b*c1**2*d**3
    -60*a**4*b**2*c1**2*d
    -60*a**4*b*c1**2*d**2
    -90*a**3*b**2*c1**2*d
    -90*a**3*b*c1**2*d**2
    60*a**2*b**2*c1**2*d**3
    60*a**2*b**3*c1**2*d**2
    90*a**2*b**2*c1**2*d**2
    90*a**3*b**2*c1**2*d**2
    -60*a**2*b**2*c1**2*d**3
    -60*a**2*b**3*c1**2*d**2
    -90*a**2*b**2*c1**2*d**2
    -90*a**3*b**2*c1**2*d**2
    -a**3*c1*(5*a**2*b + a*c0 + a + b)
    -b**3*c1*(5*a**2*b + a*c0 + a + b)
    3*a**2*c1*(3*a**2*b + a*c0 + a + b)
    3*b**2*c1*(3*a**2*b + a*c0 + a + b)
    6*a*b*c1*(3*a**2*b + a*c0 + a + b)
    6*a*c1*d*(3*a**2*b + a*c0 + a + b)
    6*b*c1*d*(3*a**2*b + a*c0 + a + b)
    -3*a**2*b*c1*(5*a**2*b + a*c0 + a + b)
    -3*a**2*c1*d*(5*a**2*b + a*c0 + a + b)
    -3*b**2*c1*d*(5*a**2*b + a*c0 + a + b)
    -3*a*b**2*c1*(5*a**2*b + a*c0 + a + b)
    -6*a*b*c1*d*(5*a**2*b + a*c0 + a + b)
    3*c1*(3*a**2*b*d**2 - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    c1*d*(-5*a**2*b*d**2 + 18*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*a*c1*(-5*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*b*c1*(-5*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0093: exp(-z)*log(z)
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

## func_0095: cosh(z) + csch(z)
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
    c1*(-a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0098: z + coth(z)
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
    6*a**2*b*c1
    c1*(a*c0 + a*c1*d + a + b)
    -c1*(2*a**2*b + a*c0 + a*c1*d + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0100: tanh(cosh(z))
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

