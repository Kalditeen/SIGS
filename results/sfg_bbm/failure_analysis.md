# BBM [2,1] failure analysis

Candidates with `solve_status=success` do not automatically satisfy the
original PDE. This file records every downstream stage separately.

## func_0001: tanh(z)
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

## func_0003: exp(-z**2)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    8*a**5*b*c1
    -2*a**2*c1**2
    -2*a*c1**2*d
    -2*a*b*c1**2
    24*a**3*b**3*c1
    24*a**4*b**2*c1
    24*a**4*b*c1*d
    8*a**2*b**4*c1
    24*a**2*b**3*c1*d
    48*a**3*b**2*c1*d
    2*a*c1*(12*a**2*b*d**2 - 6*a**2*b - a*c0 - a - b)
    2*b*c1*(12*a**2*b*d**2 - 6*a**2*b - a*c0 - a - b)
    2*c1*d*(4*a**2*b*d**2 - 6*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0004: sin(z)
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
    c1*(a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0006: cosh(z)*sech(z)**2
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
    4*a*c1**2
    -2*a*c1**2
    18*a**2*b*c1
    -24*a**2*b*c1
    c1*(5*a**2*b + a*c0 + a + b)
    -c1*(23*a**2*b + a*c0 + a + b)
    2*c1*(17*a**2*b + a*c0 + a + b)
    -2*c1*(5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0007: z**3 + z
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
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    3*a*b**5*c1**2
    15*a**2*b**4*c1**2
    15*a*b**4*c1**2*d
    30*a**3*b**3*c1**2
    30*a**4*b**2*c1**2
    60*a**4*b*c1**2*d
    60*a**2*b**3*c1**2*d
    90*a**3*b**2*c1**2*d
    2*a**4*c1**2*(15*d**2 + 2)
    2*a*b**3*c1**2*(15*d**2 + 2)
    6*a**3*b*c1**2*(15*d**2 + 2)
    6*a**2*b**2*c1**2*(15*d**2 + 2)
    3*a**2*c1*(a*c0 + 10*a*c1*d**3 + 4*a*c1*d + a + b)
    3*b**2*c1*(a*c0 + 10*a*c1*d**3 + 4*a*c1*d + a + b)
    6*a*b*c1*(a*c0 + 10*a*c1*d**3 + 4*a*c1*d + a + b)
    a*c1*(6*a*c0*d + 15*a*c1*d**4 + 12*a*c1*d**2 + a*c1 + 6*a*d + 6*b*d)
    b*c1*(6*a*c0*d + 15*a*c1*d**4 + 12*a*c1*d**2 + a*c1 + 6*a*d + 6*b*d)
    c1*(-6*a**2*b + 3*a*c0*d**2 + a*c0 + 3*a*c1*d**5 + 4*a*c1*d**3 + a*c1*d + 3*a*d**2 + a + 3*b*d**2 + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0008: tanh(csch(z))
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

## func_0009: exp(-2*z**2)
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

## func_0010: JacobiDN(z, m)*JacobiSN(z, m)
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
    -2*a*c1**2*m
    24*a**2*b*c1*m**2
    c1*(4*a**2*b*m + a**2*b + a*c0 + a + b)
    -2*c1*m*(4*a**2*b*m + 10*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0011: sin(alpha*z) + JacobiSN(z, m)
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
    -6*a**2*b*c1*m
    alpha*c1*(a**2*alpha**2*b + a*c0 + a + b)
    c1*(a**2*b*m + a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0012: sech(alpha*z)**4
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

## func_0014: sin(alpha*z)*cos(z)
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
    -c1*(3*a**2*alpha**2*b + a**2*b + a*c0 + a + b)
    alpha*c1*(a**2*alpha**2*b + 3*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0015: z**3*sinh(z)
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

## func_0018: sinh(z)**2
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

## func_0020: z**2 + tanh(alpha*z)
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

## func_0021: sin(z)*sin(alpha*z)
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

## func_0022: tanh(sinh(z))
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

## func_0023: exp(2*z)
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

## func_0024: exp(-2*z)
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

## func_0025: tanh(exp(z))
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

## func_0026: log(z) + sin(z)*cosh(z)
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
    a**4*c1*(-2*a**2*b + a*c0 + a + b)
    a**4*c1*(2*a**2*b + a*c0 + a + b)
    b**4*c1*(-2*a**2*b + a*c0 + a + b)
    b**4*c1*(2*a**2*b + a*c0 + a + b)
    c1*d**4*(-2*a**2*b + a*c0 + a + b)
    c1*d**4*(2*a**2*b + a*c0 + a + b)
    4*a**3*b*c1*(-2*a**2*b + a*c0 + a + b)
    4*a**3*b*c1*(2*a**2*b + a*c0 + a + b)
    4*a**3*c1*d*(-2*a**2*b + a*c0 + a + b)
    4*a**3*c1*d*(2*a**2*b + a*c0 + a + b)
    4*b**3*c1*d*(-2*a**2*b + a*c0 + a + b)
    4*b**3*c1*d*(2*a**2*b + a*c0 + a + b)
    4*a*b**3*c1*(-2*a**2*b + a*c0 + a + b)
    4*a*b**3*c1*(2*a**2*b + a*c0 + a + b)
    4*a*c1*d**3*(-2*a**2*b + a*c0 + a + b)
    4*a*c1*d**3*(2*a**2*b + a*c0 + a + b)
    4*b*c1*d**3*(-2*a**2*b + a*c0 + a + b)
    4*b*c1*d**3*(2*a**2*b + a*c0 + a + b)
    12*a**2*b*c1*d*(-2*a**2*b + a*c0 + a + b)
    12*a**2*b*c1*d*(2*a**2*b + a*c0 + a + b)
    12*a*b**2*c1*d*(-2*a**2*b + a*c0 + a + b)
    12*a*b**2*c1*d*(2*a**2*b + a*c0 + a + b)
    12*a*b*c1*d**2*(-2*a**2*b + a*c0 + a + b)
    12*a*b*c1*d**2*(2*a**2*b + a*c0 + a + b)
    6*a**2*b**2*c1*(-2*a**2*b + a*c0 + a + b)
    6*a**2*b**2*c1*(2*a**2*b + a*c0 + a + b)
    6*a**2*c1*d**2*(-2*a**2*b + a*c0 + a + b)
    6*a**2*c1*d**2*(2*a**2*b + a*c0 + a + b)
    6*b**2*c1*d**2*(-2*a**2*b + a*c0 + a + b)
    6*b**2*c1*d**2*(2*a**2*b + a*c0 + a + b)
    c1*d*(-2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    a*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
    b*c1*(-2*a**2*b + 3*a*c0*d**2 + 3*a*d**2 + 3*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0027: cos(z)*tanh(alpha*z)
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
    6*a**2*alpha**2*b*c1
    6*a**2*alpha**3*b*c1
    -c1*(6*a**2*alpha**2*b + a**2*b + a*c0 + a + b)
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

## func_0028: tanh(JacobiSN(z, m))
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

## func_0029: z**3 + log(z)
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

## func_0030: sech(z)**4
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -4*a*c1**2
    8*a*c1*(15*a*b + 2*c1)
    -4*c1*(14*a**2*b + a*c0 + a*c1 + a + b)
    8*c1*(29*a**2*b + a*c0 + 2*a*c1 + a + b)
    -4*c1*(74*a**2*b + a*c0 + 6*a*c1 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

