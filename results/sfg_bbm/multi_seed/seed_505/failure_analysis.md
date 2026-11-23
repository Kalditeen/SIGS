# BBM [2,1] failure analysis

Candidates with `solve_status=success` do not automatically satisfy the
original PDE. This file records every downstream stage separately.

## func_0001: z
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

## func_0002: tanh(log(z))
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

## func_0003: sin(z)**2
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

## func_0005: csch(z)*sech(z)**2
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
    a**2*b*c1
    -2*a*c1**2
    -a**2*b*c1
    2*a**2*b*c1
    3*a**2*b*c1
    6*a**2*b*c1
    -18*a**2*b*c1
    -2*a**2*b*c1
    -24*a**2*b*c1
    -3*a**2*b*c1
    -6*a**2*b*c1
    c1*(24*a**2*b + a*c0 + a + b)
    -c1*(6*a**2*b + a*c0 + a + b)
    2*c1*(20*a**2*b + a*c0 + a + b)
    -2*c1*(8*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0006: tanh(z) + csch(z)
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
    6*a**2*b*c1
    -c1*(a*c0 + a + b)
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

## func_0010: sin(alpha*z)**2
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

## func_0011: sinh(z)**2
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

## func_0013: tanh(csch(z))
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

## func_0015: z + exp(z)
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

## func_0016: sin(z)*cosh(z)**2
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
    -6*a**2*b*c1
    2*c1*(-a**2*b + a*c0 + a + b)
    c1*(-5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0017: coth(z)**2
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

## func_0018: sin(z)*tanh(z)*sech(z)
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
    c1*(16*a**2*b + a*c0 + a + b)
    c1*(8*a**2*b + a*c0 + a + b)
    -2*c1*(17*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0019: cos(z)*sinh(z)
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
    c1*(2*a**2*b - a*c0 - a - b)
    c1*(2*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0020: tanh(z)*coth(z)
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
    -c1*(8*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0021: tanh(sin(z)*cosh(z))
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

## func_0022: tanh(cos(z))
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

## func_0023: sin(z)*cosh(z)*sech(z)
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
    c1*(a**2*b + a*c0 + a + b)
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

## func_0024: tanh(sech(alpha*z)**2)
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

## func_0025: z + JacobiSN(z, m)
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
    -6*a**2*b*c1*m
    c1*(a*c0 + a*c1*d + a + b)
    c1*(a**2*b*m + a**2*b + a*c0 + a*c1*d + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0026: log(z)*cos(z)
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
    -3*a**6*b*c1
    -a*b**6*c1**2
    -a*c1**2*d**6
    5*a**5*c1**2*d
    5*a**5*b*c1**2
    -12*a**3*b**4*c1
    -12*a**5*b**2*c1
    -12*a**5*b*c1*d
    -18*a**4*b**3*c1
    -3*a**2*b**5*c1
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
    -12*a**2*b**4*c1*d
    -12*a**3*b*c1*d**3
    -15*a**3*b**4*c1**2
    -15*a**3*c1**2*d**4
    -15*a**5*b**2*c1**2
    -15*a**5*c1**2*d**2
    -18*a**4*b*c1*d**2
    -20*a**4*b**3*c1**2
    -20*a**4*c1**2*d**3
    -3*a**2*b*c1*d**4
    -30*a**5*b*c1**2*d
    -36*a**3*b**3*c1*d
    -36*a**4*b**2*c1*d
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
    -12*a**2*b**2*c1*d**3
    -15*a*b**2*c1**2*d**4
    -15*a*b**4*c1**2*d**2
    -18*a**2*b**3*c1*d**2
    -20*a*b**3*c1**2*d**3
    -30*a**2*b**4*c1**2*d
    -30*a**2*b*c1**2*d**4
    -36*a**3*b**2*c1*d**2
    -60*a**3*b**3*c1**2*d
    -60*a**3*b*c1**2*d**3
    -60*a**4*b**2*c1**2*d
    -60*a**4*b*c1**2*d**2
    30*a**2*b**2*c1**2*d**2
    -60*a**2*b**2*c1**2*d**3
    -60*a**2*b**3*c1**2*d**2
    -90*a**3*b**2*c1**2*d**2
    -a**6*c1*(a**2*b + a*c0 + a + b)
    -b**6*c1*(a**2*b + a*c0 + a + b)
    -c1*d**6*(a**2*b + a*c0 + a + b)
    a**5*c1*(3*a**2*b + a*c0 + a + b)
    b**5*c1*(3*a**2*b + a*c0 + a + b)
    -6*a**5*b*c1*(a**2*b + a*c0 + a + b)
    -6*a**5*c1*d*(a**2*b + a*c0 + a + b)
    -6*b**5*c1*d*(a**2*b + a*c0 + a + b)
    -6*a*b**5*c1*(a**2*b + a*c0 + a + b)
    -6*a*c1*d**5*(a**2*b + a*c0 + a + b)
    -6*b*c1*d**5*(a**2*b + a*c0 + a + b)
    5*a**4*b*c1*(3*a**2*b + a*c0 + a + b)
    5*a**4*c1*d*(3*a**2*b + a*c0 + a + b)
    5*b**4*c1*d*(3*a**2*b + a*c0 + a + b)
    5*a*b**4*c1*(3*a**2*b + a*c0 + a + b)
    -15*a**2*b**4*c1*(a**2*b + a*c0 + a + b)
    -15*a**2*c1*d**4*(a**2*b + a*c0 + a + b)
    -15*a**4*b**2*c1*(a**2*b + a*c0 + a + b)
    -15*a**4*c1*d**2*(a**2*b + a*c0 + a + b)
    -15*b**2*c1*d**4*(a**2*b + a*c0 + a + b)
    -15*b**4*c1*d**2*(a**2*b + a*c0 + a + b)
    -20*a**3*b**3*c1*(a**2*b + a*c0 + a + b)
    -20*a**3*c1*d**3*(a**2*b + a*c0 + a + b)
    -20*b**3*c1*d**3*(a**2*b + a*c0 + a + b)
    -30*a**4*b*c1*d*(a**2*b + a*c0 + a + b)
    -30*a*b**4*c1*d*(a**2*b + a*c0 + a + b)
    -30*a*b*c1*d**4*(a**2*b + a*c0 + a + b)
    10*a**2*b**3*c1*(3*a**2*b + a*c0 + a + b)
    10*a**3*b**2*c1*(3*a**2*b + a*c0 + a + b)
    20*a**3*b*c1*d*(3*a**2*b + a*c0 + a + b)
    20*a*b**3*c1*d*(3*a**2*b + a*c0 + a + b)
    -60*a**2*b**3*c1*d*(a**2*b + a*c0 + a + b)
    -60*a**2*b*c1*d**3*(a**2*b + a*c0 + a + b)
    -60*a**3*b**2*c1*d*(a**2*b + a*c0 + a + b)
    -60*a**3*b*c1*d**2*(a**2*b + a*c0 + a + b)
    -60*a*b**2*c1*d**3*(a**2*b + a*c0 + a + b)
    -60*a*b**3*c1*d**2*(a**2*b + a*c0 + a + b)
    30*a**2*b**2*c1*d*(3*a**2*b + a*c0 + a + b)
    -90*a**2*b**2*c1*d**2*(a**2*b + a*c0 + a + b)
    c1*d**3*(3*a**2*b*d**2 - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    2*a**3*c1*(15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*b**3*c1*(15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    6*a**2*b*c1*(15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    6*a*b**2*c1*(15*a**2*b*d**2 - a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    a*c1*d**2*(15*a**2*b*d**2 - 6*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    b*c1*d**2*(15*a**2*b*d**2 - 6*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*a**2*c1*d*(15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    2*b**2*c1*d*(15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
    4*a*b*c1*d*(15*a**2*b*d**2 - 3*a**2*b + 5*a*c0*d**2 + 5*a*d**2 + 5*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0028: tanh(z**3)
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

## func_0029: tanh(exp(-z))
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

## func_0030: z**4
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

## func_0034: tanh(z)*JacobiDN(z, m)
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

## func_0035: coth(z) + sech(z)
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
    -c1*(2*a**2*b + a*c0 + a + b)
    -c1*(5*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0038: exp(-z) + 1/z
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -a**11*c1**2
    -a*b**10*c1**2
    -a*c1**2*d**10
    -10*a**10*c1**2*d
    -10*a**10*b*c1**2
    -10*a**2*b**9*c1**2
    -10*a**2*c1**2*d**9
    -10*a*b**9*c1**2*d
    -10*a*b*c1**2*d**9
    -120*a**4*b**7*c1**2
    -120*a**4*c1**2*d**7
    -120*a**8*b**3*c1**2
    -120*a**8*c1**2*d**3
    -210*a**5*b**6*c1**2
    -210*a**5*c1**2*d**6
    -210*a**7*b**4*c1**2
    -210*a**7*c1**2*d**4
    -252*a**6*b**5*c1**2
    -252*a**6*c1**2*d**5
    -45*a**3*b**8*c1**2
    -45*a**3*c1**2*d**8
    -45*a**9*b**2*c1**2
    -45*a**9*c1**2*d**2
    -90*a**9*b*c1**2*d
    -a**8*c1*(a*c0 + a + b)
    -b**8*c1*(a*c0 + a + b)
    -120*a*b**3*c1**2*d**7
    -120*a*b**7*c1**2*d**3
    -1260*a**5*b**5*c1**2*d
    -1260*a**5*b*c1**2*d**5
    -1260*a**6*b**4*c1**2*d
    -1260*a**6*b*c1**2*d**4
    -210*a*b**4*c1**2*d**6
    -210*a*b**6*c1**2*d**4
    -252*a*b**5*c1**2*d**5
    -360*a**3*b**7*c1**2*d
    -360*a**3*b*c1**2*d**7
    -360*a**8*b**2*c1**2*d
    -360*a**8*b*c1**2*d**2
    -45*a*b**2*c1**2*d**8
    -45*a*b**8*c1**2*d**2
    -840*a**4*b**6*c1**2*d
    -840*a**4*b*c1**2*d**6
    -840*a**7*b**3*c1**2*d
    -840*a**7*b*c1**2*d**3
    -90*a**2*b**8*c1**2*d
    -90*a**2*b*c1**2*d**8
    -1260*a**2*b**4*c1**2*d**5
    -1260*a**2*b**5*c1**2*d**4
    -1260*a**3*b**2*c1**2*d**6
    -1260*a**3*b**6*c1**2*d**2
    -1260*a**7*b**2*c1**2*d**2
    -2520*a**3*b**3*c1**2*d**5
    -2520*a**3*b**5*c1**2*d**3
    -2520*a**4*b**2*c1**2*d**5
    -2520*a**4*b**5*c1**2*d**2
    -2520*a**6*b**2*c1**2*d**3
    -2520*a**6*b**3*c1**2*d**2
    -3150*a**3*b**4*c1**2*d**4
    -3150*a**5*b**2*c1**2*d**4
    -3150*a**5*b**4*c1**2*d**2
    -360*a**2*b**2*c1**2*d**7
    -360*a**2*b**7*c1**2*d**2
    -4200*a**4*b**3*c1**2*d**4
    -4200*a**4*b**4*c1**2*d**3
    -4200*a**5*b**3*c1**2*d**3
    -8*a**7*b*c1*(a*c0 + a + b)
    -8*a*b**7*c1*(a*c0 + a + b)
    -840*a**2*b**3*c1**2*d**6
    -840*a**2*b**6*c1**2*d**3
    a**10*c1*(a**2*b - a*c0 - a - b)
    b**10*c1*(a**2*b - a*c0 - a - b)
    -28*a**2*b**6*c1*(a*c0 + a + b)
    -28*a**6*b**2*c1*(a*c0 + a + b)
    -56*a**3*b**5*c1*(a*c0 + a + b)
    -56*a**5*b**3*c1*(a*c0 + a + b)
    -70*a**4*b**4*c1*(a*c0 + a + b)
    10*a**9*b*c1*(a**2*b - a*c0 - a - b)
    10*a*b**9*c1*(a**2*b - a*c0 - a - b)
    120*a**3*b**7*c1*(a**2*b - a*c0 - a - b)
    120*a**7*b**3*c1*(a**2*b - a*c0 - a - b)
    210*a**4*b**6*c1*(a**2*b - a*c0 - a - b)
    210*a**6*b**4*c1*(a**2*b - a*c0 - a - b)
    252*a**5*b**5*c1*(a**2*b - a*c0 - a - b)
    45*a**2*b**8*c1*(a**2*b - a*c0 - a - b)
    45*a**8*b**2*c1*(a**2*b - a*c0 - a - b)
    -a**7*c1*(8*a*c0*d + a*c1 + 8*a*d + 8*b*d)
    -b**7*c1*(8*a*c0*d + a*c1 + 8*a*d + 8*b*d)
    -7*a**6*b*c1*(8*a*c0*d + a*c1 + 8*a*d + 8*b*d)
    -7*a*b**6*c1*(8*a*c0*d + a*c1 + 8*a*d + 8*b*d)
    -21*a**2*b**5*c1*(8*a*c0*d + a*c1 + 8*a*d + 8*b*d)
    -21*a**5*b**2*c1*(8*a*c0*d + a*c1 + 8*a*d + 8*b*d)
    -35*a**3*b**4*c1*(8*a*c0*d + a*c1 + 8*a*d + 8*b*d)
    -35*a**4*b**3*c1*(8*a*c0*d + a*c1 + 8*a*d + 8*b*d)
    a**9*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    b**9*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    c1*d**6*(6*a**2*b - a*c0*d**2 - a*c1*d - a*d**2 - b*d**2)
    9*a**8*b*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    9*a*b**8*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    126*a**4*b**5*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    126*a**5*b**4*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    36*a**2*b**7*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    36*a**7*b**2*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    84*a**3*b**6*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    84*a**6*b**3*c1*(10*a**2*b*d - 10*a*c0*d - a*c1 - 10*a*d - 10*b*d)
    c1*d**8*(a**2*b*d**2 - a*c0*d**2 - a*c1*d - a*c1 - a*d**2 - b*d**2)
    a**6*c1*(6*a**2*b - 28*a*c0*d**2 - 7*a*c1*d - 28*a*d**2 - 28*b*d**2)
    b**6*c1*(6*a**2*b - 28*a*c0*d**2 - 7*a*c1*d - 28*a*d**2 - 28*b*d**2)
    a**5*c1*d*(36*a**2*b - 56*a*c0*d**2 - 21*a*c1*d - 56*a*d**2 - 56*b*d**2)
    b**5*c1*d*(36*a**2*b - 56*a*c0*d**2 - 21*a*c1*d - 56*a*d**2 - 56*b*d**2)
    a*c1*d**5*(36*a**2*b - 8*a*c0*d**2 - 7*a*c1*d - 8*a*d**2 - 8*b*d**2)
    b*c1*d**5*(36*a**2*b - 8*a*c0*d**2 - 7*a*c1*d - 8*a*d**2 - 8*b*d**2)
    6*a**5*b*c1*(6*a**2*b - 28*a*c0*d**2 - 7*a*c1*d - 28*a*d**2 - 28*b*d**2)
    6*a*b**5*c1*(6*a**2*b - 28*a*c0*d**2 - 7*a*c1*d - 28*a*d**2 - 28*b*d**2)
    a**2*c1*d**4*(90*a**2*b - 28*a*c0*d**2 - 21*a*c1*d - 28*a*d**2 - 28*b*d**2)
    a**3*c1*d**3*(120*a**2*b - 56*a*c0*d**2 - 35*a*c1*d - 56*a*d**2 - 56*b*d**2)
    b**2*c1*d**4*(90*a**2*b - 28*a*c0*d**2 - 21*a*c1*d - 28*a*d**2 - 28*b*d**2)
    b**3*c1*d**3*(120*a**2*b - 56*a*c0*d**2 - 35*a*c1*d - 56*a*d**2 - 56*b*d**2)
    15*a**2*b**4*c1*(6*a**2*b - 28*a*c0*d**2 - 7*a*c1*d - 28*a*d**2 - 28*b*d**2)
    15*a**4*b**2*c1*(6*a**2*b - 28*a*c0*d**2 - 7*a*c1*d - 28*a*d**2 - 28*b*d**2)
    2*a*b*c1*d**4*(90*a**2*b - 28*a*c0*d**2 - 21*a*c1*d - 28*a*d**2 - 28*b*d**2)
    20*a**3*b**3*c1*(6*a**2*b - 28*a*c0*d**2 - 7*a*c1*d - 28*a*d**2 - 28*b*d**2)
    5*a**4*b*c1*d*(36*a**2*b - 56*a*c0*d**2 - 21*a*c1*d - 56*a*d**2 - 56*b*d**2)
    5*a**4*c1*d**2*(18*a**2*b - 14*a*c0*d**2 - 7*a*c1*d - 14*a*d**2 - 14*b*d**2)
    5*b**4*c1*d**2*(18*a**2*b - 14*a*c0*d**2 - 7*a*c1*d - 14*a*d**2 - 14*b*d**2)
    5*a*b**4*c1*d*(36*a**2*b - 56*a*c0*d**2 - 21*a*c1*d - 56*a*d**2 - 56*b*d**2)
    10*a**2*b**3*c1*d*(36*a**2*b - 56*a*c0*d**2 - 21*a*c1*d - 56*a*d**2 - 56*b*d**2)
    10*a**3*b**2*c1*d*(36*a**2*b - 56*a*c0*d**2 - 21*a*c1*d - 56*a*d**2 - 56*b*d**2)
    20*a**3*b*c1*d**2*(18*a**2*b - 14*a*c0*d**2 - 7*a*c1*d - 14*a*d**2 - 14*b*d**2)
    20*a*b**3*c1*d**2*(18*a**2*b - 14*a*c0*d**2 - 7*a*c1*d - 14*a*d**2 - 14*b*d**2)
    3*a**2*b*c1*d**3*(120*a**2*b - 56*a*c0*d**2 - 35*a*c1*d - 56*a*d**2 - 56*b*d**2)
    3*a*b**2*c1*d**3*(120*a**2*b - 56*a*c0*d**2 - 35*a*c1*d - 56*a*d**2 - 56*b*d**2)
    a**8*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    b**8*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    30*a**2*b**2*c1*d**2*(18*a**2*b - 14*a*c0*d**2 - 7*a*c1*d - 14*a*d**2 - 14*b*d**2)
    8*a**7*b*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    8*a*b**7*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    a*c1*d**7*(10*a**2*b*d**2 - 10*a*c0*d**2 - 9*a*c1*d - 8*a*c1 - 10*a*d**2 - 10*b*d**2)
    b*c1*d**7*(10*a**2*b*d**2 - 10*a*c0*d**2 - 9*a*c1*d - 8*a*c1 - 10*a*d**2 - 10*b*d**2)
    28*a**2*b**6*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    28*a**6*b**2*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    4*a**7*c1*d*(30*a**2*b*d**2 - 30*a*c0*d**2 - 9*a*c1*d - 2*a*c1 - 30*a*d**2 - 30*b*d**2)
    4*b**7*c1*d*(30*a**2*b*d**2 - 30*a*c0*d**2 - 9*a*c1*d - 2*a*c1 - 30*a*d**2 - 30*b*d**2)
    56*a**3*b**5*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    56*a**5*b**3*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    70*a**4*b**4*c1*(45*a**2*b*d**2 - 45*a*c0*d**2 - 9*a*c1*d - a*c1 - 45*a*d**2 - 45*b*d**2)
    a**2*c1*d**6*(45*a**2*b*d**2 - 45*a*c0*d**2 - 36*a*c1*d - 28*a*c1 - 45*a*d**2 - 45*b*d**2)
    b**2*c1*d**6*(45*a**2*b*d**2 - 45*a*c0*d**2 - 36*a*c1*d - 28*a*c1 - 45*a*d**2 - 45*b*d**2)
    14*a**4*c1*d**4*(15*a**2*b*d**2 - 15*a*c0*d**2 - 9*a*c1*d - 5*a*c1 - 15*a*d**2 - 15*b*d**2)
    14*a**5*c1*d**3*(18*a**2*b*d**2 - 18*a*c0*d**2 - 9*a*c1*d - 4*a*c1 - 18*a*d**2 - 18*b*d**2)
    14*a**6*c1*d**2*(15*a**2*b*d**2 - 15*a*c0*d**2 - 6*a*c1*d - 2*a*c1 - 15*a*d**2 - 15*b*d**2)
    14*b**4*c1*d**4*(15*a**2*b*d**2 - 15*a*c0*d**2 - 9*a*c1*d - 5*a*c1 - 15*a*d**2 - 15*b*d**2)
    14*b**5*c1*d**3*(18*a**2*b*d**2 - 18*a*c0*d**2 - 9*a*c1*d - 4*a*c1 - 18*a*d**2 - 18*b*d**2)
    14*b**6*c1*d**2*(15*a**2*b*d**2 - 15*a*c0*d**2 - 6*a*c1*d - 2*a*c1 - 15*a*d**2 - 15*b*d**2)
    2*a*b*c1*d**6*(45*a**2*b*d**2 - 45*a*c0*d**2 - 36*a*c1*d - 28*a*c1 - 45*a*d**2 - 45*b*d**2)
    28*a**6*b*c1*d*(30*a**2*b*d**2 - 30*a*c0*d**2 - 9*a*c1*d - 2*a*c1 - 30*a*d**2 - 30*b*d**2)
    28*a*b**6*c1*d*(30*a**2*b*d**2 - 30*a*c0*d**2 - 9*a*c1*d - 2*a*c1 - 30*a*d**2 - 30*b*d**2)
    4*a**3*c1*d**5*(30*a**2*b*d**2 - 30*a*c0*d**2 - 21*a*c1*d - 14*a*c1 - 30*a*d**2 - 30*b*d**2)
    4*b**3*c1*d**5*(30*a**2*b*d**2 - 30*a*c0*d**2 - 21*a*c1*d - 14*a*c1 - 30*a*d**2 - 30*b*d**2)
    12*a**2*b*c1*d**5*(30*a**2*b*d**2 - 30*a*c0*d**2 - 21*a*c1*d - 14*a*c1 - 30*a*d**2 - 30*b*d**2)
    12*a*b**2*c1*d**5*(30*a**2*b*d**2 - 30*a*c0*d**2 - 21*a*c1*d - 14*a*c1 - 30*a*d**2 - 30*b*d**2)
    140*a**3*b**4*c1*d*(30*a**2*b*d**2 - 30*a*c0*d**2 - 9*a*c1*d - 2*a*c1 - 30*a*d**2 - 30*b*d**2)
    140*a**4*b**3*c1*d*(30*a**2*b*d**2 - 30*a*c0*d**2 - 9*a*c1*d - 2*a*c1 - 30*a*d**2 - 30*b*d**2)
    56*a**3*b*c1*d**4*(15*a**2*b*d**2 - 15*a*c0*d**2 - 9*a*c1*d - 5*a*c1 - 15*a*d**2 - 15*b*d**2)
    56*a*b**3*c1*d**4*(15*a**2*b*d**2 - 15*a*c0*d**2 - 9*a*c1*d - 5*a*c1 - 15*a*d**2 - 15*b*d**2)
    70*a**4*b*c1*d**3*(18*a**2*b*d**2 - 18*a*c0*d**2 - 9*a*c1*d - 4*a*c1 - 18*a*d**2 - 18*b*d**2)
    70*a*b**4*c1*d**3*(18*a**2*b*d**2 - 18*a*c0*d**2 - 9*a*c1*d - 4*a*c1 - 18*a*d**2 - 18*b*d**2)
    84*a**2*b**5*c1*d*(30*a**2*b*d**2 - 30*a*c0*d**2 - 9*a*c1*d - 2*a*c1 - 30*a*d**2 - 30*b*d**2)
    84*a**5*b**2*c1*d*(30*a**2*b*d**2 - 30*a*c0*d**2 - 9*a*c1*d - 2*a*c1 - 30*a*d**2 - 30*b*d**2)
    84*a**5*b*c1*d**2*(15*a**2*b*d**2 - 15*a*c0*d**2 - 6*a*c1*d - 2*a*c1 - 15*a*d**2 - 15*b*d**2)
    84*a*b**5*c1*d**2*(15*a**2*b*d**2 - 15*a*c0*d**2 - 6*a*c1*d - 2*a*c1 - 15*a*d**2 - 15*b*d**2)
    140*a**2*b**3*c1*d**3*(18*a**2*b*d**2 - 18*a*c0*d**2 - 9*a*c1*d - 4*a*c1 - 18*a*d**2 - 18*b*d**2)
    140*a**3*b**2*c1*d**3*(18*a**2*b*d**2 - 18*a*c0*d**2 - 9*a*c1*d - 4*a*c1 - 18*a*d**2 - 18*b*d**2)
    210*a**2*b**4*c1*d**2*(15*a**2*b*d**2 - 15*a*c0*d**2 - 6*a*c1*d - 2*a*c1 - 15*a*d**2 - 15*b*d**2)
    210*a**4*b**2*c1*d**2*(15*a**2*b*d**2 - 15*a*c0*d**2 - 6*a*c1*d - 2*a*c1 - 15*a*d**2 - 15*b*d**2)
    280*a**3*b**3*c1*d**2*(15*a**2*b*d**2 - 15*a*c0*d**2 - 6*a*c1*d - 2*a*c1 - 15*a*d**2 - 15*b*d**2)
    84*a**2*b**2*c1*d**4*(15*a**2*b*d**2 - 15*a*c0*d**2 - 9*a*c1*d - 5*a*c1 - 15*a*d**2 - 15*b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0040: csch(z)**2
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

## func_0041: z**2 + tanh(alpha*z)
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

## func_0043: z*exp(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a**3*c1**2
    a*b**2*c1**2
    2*a**2*b*c1**2
    a*c1**2*d*(d + 1)
    a**2*c1**2*(2*d + 1)
    a*b*c1**2*(2*d + 1)
    a*c1*(-a**2*b + a*c0 + a + b)
    b*c1*(-a**2*b + a*c0 + a + b)
    c1*(-a**2*b*d - 3*a**2*b + a*c0*d + a*c0 + a*d + a + b*d + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0044: tanh(z)*JacobiCN(z, m)
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
    6*a**2*b*c1*m
    -6*a**2*b*c1*m
    c1*(5*a**2*b + a*c0 + a + b)
    -c1*(11*a**2*b + a*c0 + a + b)
    -c1*(4*a**2*b*m + 7*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0045: tanh(exp(z))
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

## func_0047: sinh(z)*csch(z)
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
    3*a**2*b*c1
    -3*a**2*b*c1
    c1*(-a**2*b + a*c0 + a + b)
    c1*(3*a**2*b - a*c0 - a - b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0050: z + tanh(alpha*z)
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
    a*c1**2*(alpha + 1)
    -a**2*alpha*c1**2
    -a*alpha*b*c1**2
    a**2*c1**2*(alpha + 1)
    a*b*c1**2*(alpha + 1)
    6*a**2*alpha**3*b*c1
    -alpha*c1*(8*a**2*alpha**2*b + a*c0 + a*c1*d + a + b)
    c1*(2*a**2*alpha**3*b + a*alpha*c0 + a*alpha*c1*d + a*alpha + a*c0 + a*c1*d + a + alpha*b + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0052: z**3 + JacobiCN(z, m)
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
    -a*b**3*c1**2
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    3*a*b**2*c1**2
    3*a*b**5*c1**2
    3*a*c1**2*d**2
    6*a**2*c1**2*d
    6*a**2*b*c1**2
    6*a**2*b*c1*m
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
    3*a*c1*d*(2*a*c0 + 5*a*c1*d**3 + 2*a + 2*b)
    3*b*c1*d*(2*a*c0 + 5*a*c1*d**3 + 2*a + 2*b)
    -c1*(4*a**2*b*m + a**2*b + a*c0 + a*c1*d**3 + a + b)
    3*c1*(-2*a**2*b + a*c0*d**2 + a*c1*d**5 + a*d**2 + b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0053: tanh(tanh(alpha*z))
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

## func_0054: cos(z)**2
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
    -2*c1*(4*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0058: z**3*JacobiDN(z, m)
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
    -a**7*c1**2*m
    15*a**5*c1**2*d
    15*a**5*b*c1**2
    3*a*b**5*c1**2
    3*a*c1**2*d**5
    -18*a**4*b*c1*m
    -3*a**6*c1**2*m
    -a*b**6*c1**2*m
    -a*c1**2*d**6*m
    15*a**2*b**4*c1**2
    15*a**2*c1**2*d**4
    15*a*b**4*c1**2*d
    15*a*b*c1**2*d**4
    30*a**3*b**3*c1**2
    30*a**3*c1**2*d**3
    30*a**4*b**2*c1**2
    30*a**4*c1**2*d**2
    6*a**5*b*c1*m**2
    60*a**4*b*c1**2*d
    -15*a**5*c1**2*d*m
    -15*a**5*b*c1**2*m
    -18*a**2*b**3*c1*m
    -3*a*b**5*c1**2*m
    -3*a*c1**2*d**5*m
    -36*a**3*b**2*c1*m
    -36*a**3*b*c1*d*m
    -6*a**6*c1**2*d*m
    -6*a**6*b*c1**2*m
    18*a**3*b**3*c1*m**2
    18*a**4*b**2*c1*m**2
    18*a**4*b*c1*d*m**2
    30*a*b**2*c1**2*d**3
    30*a*b**3*c1**2*d**2
    6*a**2*b**4*c1*m**2
    60*a**2*b**3*c1**2*d
    60*a**2*b*c1**2*d**3
    90*a**3*b**2*c1**2*d
    90*a**3*b*c1**2*d**2
    -15*a**2*b**4*c1**2*m
    -15*a**2*c1**2*d**4*m
    -15*a**3*b**4*c1**2*m
    -15*a**3*c1**2*d**4*m
    -15*a**5*b**2*c1**2*m
    -15*a**5*c1**2*d**2*m
    -15*a*b**4*c1**2*d*m
    -15*a*b*c1**2*d**4*m
    -18*a**2*b*c1*d**2*m
    -20*a**4*b**3*c1**2*m
    -20*a**4*c1**2*d**3*m
    -30*a**3*b**3*c1**2*m
    -30*a**3*c1**2*d**3*m
    -30*a**4*b**2*c1**2*m
    -30*a**4*c1**2*d**2*m
    -30*a**5*b*c1**2*d*m
    -36*a**2*b**2*c1*d*m
    -6*a**2*b**5*c1**2*m
    -6*a**2*c1**2*d**5*m
    -6*a*b**5*c1**2*d*m
    -6*a*b*c1**2*d**5*m
    -60*a**4*b*c1**2*d*m
    18*a**2*b**3*c1*d*m**2
    18*a**3*b*c1*d**2*m**2
    36*a**3*b**2*c1*d*m**2
    6*a**2*b*c1*d**3*m**2
    90*a**2*b**2*c1**2*d**2
    -15*a*b**2*c1**2*d**4*m
    -15*a*b**4*c1**2*d**2*m
    -20*a*b**3*c1**2*d**3*m
    -30*a**2*b**4*c1**2*d*m
    -30*a**2*b*c1**2*d**4*m
    -30*a*b**2*c1**2*d**3*m
    -30*a*b**3*c1**2*d**2*m
    -60*a**2*b**3*c1**2*d*m
    -60*a**2*b*c1**2*d**3*m
    -60*a**3*b**3*c1**2*d*m
    -60*a**3*b*c1**2*d**3*m
    -60*a**4*b**2*c1**2*d*m
    -60*a**4*b*c1**2*d**2*m
    -90*a**3*b**2*c1**2*d*m
    -90*a**3*b*c1**2*d**2*m
    18*a**2*b**2*c1*d**2*m**2
    -60*a**2*b**2*c1**2*d**3*m
    -60*a**2*b**3*c1**2*d**2*m
    -90*a**2*b**2*c1**2*d**2*m
    -90*a**3*b**2*c1**2*d**2*m
    3*a**2*c1*(3*a**2*b*m + a*c0 + a + b)
    3*b**2*c1*(3*a**2*b*m + a*c0 + a + b)
    6*a*b*c1*(3*a**2*b*m + a*c0 + a + b)
    6*a*c1*d*(3*a**2*b*m + a*c0 + a + b)
    6*b*c1*d*(3*a**2*b*m + a*c0 + a + b)
    -a**3*c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
    -b**3*c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
    -3*a**2*b*c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
    -3*a**2*c1*d*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
    -3*b**2*c1*d*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
    -3*a*b**2*c1*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
    -6*a*b*c1*d*m*(a**2*b*m + 4*a**2*b + a*c0 + a + b)
    3*c1*(3*a**2*b*d**2*m - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    c1*d*m*(-a**2*b*d**2*m - 4*a**2*b*d**2 + 18*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*a*c1*m*(-a**2*b*d**2*m - 4*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
    3*b*c1*m*(-a**2*b*d**2*m - 4*a**2*b*d**2 + 6*a**2*b - a*c0*d**2 - a*d**2 - b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0064: exp(-2*z**2)
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

## func_0066: tanh(JacobiDN(z, m))
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

## func_0069: z**3*JacobiSN(z, m)
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
    -18*a**4*b*c1*m
    -6*a**5*b*c1*m
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
    -18*a**2*b**3*c1*m
    -18*a**3*b**3*c1*m
    -18*a**4*b**2*c1*m
    -18*a**4*b*c1*d*m
    -36*a**3*b**2*c1*m
    -36*a**3*b*c1*d*m
    -6*a**2*b**4*c1*m
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
    -18*a**2*b**3*c1*d*m
    -18*a**2*b*c1*d**2*m
    -18*a**3*b*c1*d**2*m
    -36*a**2*b**2*c1*d*m
    -36*a**3*b**2*c1*d*m
    -6*a**2*b*c1*d**3*m
    60*a**2*b**2*c1**2*d**3
    60*a**2*b**3*c1**2*d**2
    90*a**2*b**2*c1**2*d**2
    90*a**3*b**2*c1**2*d**2
    -18*a**2*b**2*c1*d**2*m
    a**3*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    b**3*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    3*a**2*b*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    3*a**2*c1*d*(a**2*b*m + a**2*b + a*c0 + a + b)
    3*b**2*c1*d*(a**2*b*m + a**2*b + a*c0 + a + b)
    3*a*b**2*c1*(a**2*b*m + a**2*b + a*c0 + a + b)
    6*a*b*c1*d*(a**2*b*m + a**2*b + a*c0 + a + b)
    3*a**2*c1*(3*a**2*b*m + 3*a**2*b + a*c0 + a + b)
    3*b**2*c1*(3*a**2*b*m + 3*a**2*b + a*c0 + a + b)
    6*a*b*c1*(3*a**2*b*m + 3*a**2*b + a*c0 + a + b)
    6*a*c1*d*(3*a**2*b*m + 3*a**2*b + a*c0 + a + b)
    6*b*c1*d*(3*a**2*b*m + 3*a**2*b + a*c0 + a + b)
    c1*d*(a**2*b*d**2*m + a**2*b*d**2 - 18*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    3*a*c1*(a**2*b*d**2*m + a**2*b*d**2 - 6*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    3*b*c1*(a**2*b*d**2*m + a**2*b*d**2 - 6*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
    3*c1*(3*a**2*b*d**2*m + 3*a**2*b*d**2 - 2*a**2*b + a*c0*d**2 + a*d**2 + b*d**2)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...

## func_0074: tanh(exp(-z**2))
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

## func_0075: tanh(sin(alpha*z))
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

## func_0076: cos(z) + tanh(z)*sech(z)
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
    -3*a*c1**2
    24*a**2*b*c1
    -c1*(a**2*b + a*c0 + a + b)
    c1*(5*a**2*b + a*c0 + a + b)
    -2*c1*(14*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0077: tanh(tan(z))
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

## func_0080: exp(z) + csch(z)
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

## func_0089: tanh(tanh(z))
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

## func_0092: log(z)**2
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

## func_0094: tanh(alpha*z) + coth(z)
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

## func_0096: tanh(sinh(z))
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

## func_0097: JacobiDN(z, m)*sech(z)
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
    6*a**2*b*c1*m**2
    -c1*(3*a**2*b*m + 5*a**2*b + a*c0 + a + b)
    -c1*m*(a**2*b*m + 7*a**2*b + a*c0 + a + b)
- sympy_solutions:
    {'c1': '0'}
    {'a': '0', 'b': '0'}
    {'a': '0', 'c1': '0'}
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'res...
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 's...
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skip...

## func_0100: tanh(coth(z))
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

