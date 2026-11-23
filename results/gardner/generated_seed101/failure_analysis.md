# Gardner failure analysis

A `solve_status=success` record means SymPy returned parameter
branches for the extracted algebraic coefficient system. It does not
mean the original Gardner residual is identically zero. Every branch
is independently back-substituted below.

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
    2*a*c1**3
    -4*a*c1**3
    -a*c1**3*m
    2*a*c1**3*m
    -2*a*c1**3*m
    2*a*c1**2*(2*c0 + 4*c1 + 1)
    a*c1**2*m*(2*c0 + 2*c1 + 1)
    a*c1*m**2*(-6*a**2 + c1**2)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    a**3*c1
    a*c1**3
    -a**3*c1
    2*a**3*c1
    3*a**3*c1
    6*a**3*c1
    -2*a**3*c1
    -3*a**3*c1
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    2*a**6*c1**3
    4*a**4*c1**3
    -a**5*alpha*c1**3
    10*a**5*b*c1**3
    12*a**3*b*c1**3
    2*a*b**5*c1**3
    4*a*b**3*c1**3
    -2*a**3*alpha*c1**3
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    a*c1**3
    -a*c1**3
    -6*a**3*c1
    a*c1**2*(2*c0 + 1)
    -a*c1**2*(2*c0 + 1)
    c1*(-5*a**3 + a*c0**2 + a*c0 + b)
    c1*(11*a**3 - a*c0**2 - a*c0 - b)
    c1*(7*a**3 - a*c0**2 - a*c0 - b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    a**4*c1**3
    -a**5*c1**3
    a*b**3*c1**3
    a*c1**3*d**3
    -2*a**5*c1**3
    -a*b**4*c1**3
    -a*c1**3*d**4
    3*a**3*c1**3*d
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    6*a**18*c1**3
    102*a**17*c1**3*d
    102*a**17*b*c1**3
    6*a*b**17*c1**3
    102*a**2*b**16*c1**3
    102*a*b**16*c1**3*d
    116688*a**11*b**7*c1**3
    116688*a**8*b**10*c1**3
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    -2*a*c1**3
    -2*a*c1**2*(2*c0 + 1)
    -2*c1*(4*a**3 + a*c0**2 + a*c0 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    16*a**6*c1
    48*a**6*c1
    8*a**6*c1
    -48*a**6*c1
    -64*a**6*c1
    -8*a**6*c1
    144*a**5*b*c1
    144*a**5*c1*d
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    a*c1**3
    -a*c1**3
    a*c1**2*(2*c0 + 1)
    -a*c1**2*(2*c0 + 1)
    c1*(4*a**3 + a*c0**2 + a*c0 + b)
    -c1*(4*a**3 + a*c0**2 + a*c0 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    2*a*c1**3
    2*a*c1**2*(2*c0 + 1)
    2*c1*(4*a**3 + a*c0**2 + a*c0 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

## func_0012: tanh(alpha*z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -2*a*alpha*c1**3
    2*alpha*c1*(-8*a**3*alpha**2 + a*c0**2 + a*c0 + b)
    2*a*alpha*c1*(-12*a**2*alpha**2 - 2*c0*c1 + c1**2 - c1)
    2*alpha*c1*(20*a**3*alpha**2 - a*c0**2 + 2*a*c0*c1 - a*c0 + a*c1 - b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    -a*c1**3
    6*a**3*c1
    8*a**3*c1
    -2*a**3*c1
    -6*a**3*c1
    a*c1**2*(2*c0 + 1)
    -a*c1**2*(2*c0 + 1)
    c1*(a**3 + a*c0**2 + a*c0 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

## func_0015: tanh(z)
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONTRIVIAL
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    a*c1**2*(2*c0 + 1)
    -a*c1**2*(2*c0 + 1)
    -a*c1*(6*a**2 + c1**2)
    c1*(-2*a**3 + a*c0**2 + a*c0 + b)
    c1*(8*a**3 - a*c0**2 - a*c0 + a*c1**2 - b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c0': '-1/2', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    -a**3*c1
    -a*c1**3
    -2*a**3*c1
    -3*a**3*c1
    -a*c1**2*(2*c0 + 1)
    -c1*(a**3 + a*c0**2 + a*c0 + b)
    -c1*(3*a**3 + a*c0**2 + a*c0 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    a*c1**3
    6*a**3*c1
    6*a**3*c1*m
    a*c1**2*(2*c0 + 1)
    a*c1*(6*a**2*m + c1**2)
    c1*(-3*a**3*m - a**3 + a*c0**2 + a*c0 + b)
    c1*(-a**3*m + 5*a**3 + a*c0**2 + a*c0 + b)
    c1*(-3*a**3*m + 5*a**3 + a*c0**2 + a*c0 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

## func_0018: tan(z)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    2*a*c1**3
    2*c1*(8*a**3 + a*c0**2 + a*c0 + b)
    2*a*c1*(12*a**2 + 2*c0*c1 + c1**2 + c1)
    2*c1*(20*a**3 + a*c0**2 + 2*a*c0*c1 + a*c0 + a*c1 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    a**5*c1**3
    a**7*c1**3
    2*a**6*c1**3
    a*b**4*c1**3
    a*b**6*c1**3
    10*a**5*b*c1**3
    2*a*b**5*c1**3
    4*a**4*b*c1**3
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    a*c1**3
    a**5*c1**3
    2*a**2*c1**3
    2*a**3*c1**3
    2*a**6*c1**3
    2*a*c1**3*d
    2*a*b*c1**3
    4*a**4*c1**3
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    3*a**13*c1**3
    3*a**7*c1**3
    6*a**10*c1**3
    18*a**6*c1**3*d
    18*a**6*b*c1**3
    3*a*b**12*c1**3
    3*a*b**6*c1**3
    36*a**12*c1**3*d
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    2*a*c1**3
    2*a*c1**2*(2*c0 + 1)
    2*c1*(4*a**3 + a*c0**2 + a*c0 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    -a*c1**3
    12*a**3*c1
    24*a**3*c1
    8*a**3*c1
    -12*a**3*c1
    -18*a**3*c1
    -2*a**3*c1
    -6*a**3*c1
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    2*a*c1**3
    2*a*c1**2*(2*c0 + 1)
    2*c1*(4*a**3 + a*c0**2 + a*c0 + b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    144*a**3*c1
    168*a**3*c1
    2*a*c1**3
    48*a**3*c1
    64*a**3*c1
    72*a**3*c1
    -144*a**3*c1
    -16*a**3*c1
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

## func_0028: JacobiCN(z, m)**2
- symbolic_status: success
- constraint_status: success
- solve_status: success
- nontrivial_status: NONE
- substitution_status: success
- identity_verification_status: skipped
- verification_status: FAILED
- failure_reason: solver produced branches but none passed independent back-substitution verification
- coefficient_equations:
    -2*a*c1**3
    2*a*c1*(-12*a**2*m + 2*c0*c1 + 2*c1**2 + c1)
    2*c1*(4*a**3*m + 4*a**3 - a*c0**2 - 2*a*c0*c1 - a*c0 - a*c1**2 - a*c1 - b)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    12*a**3*alpha**3*c1
    2*a**3*alpha**3*c1
    24*a**3*alpha**3*c1
    30*a**3*alpha**3*c1
    6*a**3*alpha**3*c1
    -12*a**3*alpha**3*c1
    -18*a**3*alpha**3*c1
    -24*a**3*alpha**3*c1
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

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
    a*c1**3
    2*a*c1**3
    -a*alpha*c1**3
    -2*a*alpha*c1**3
    a*alpha*c1**2*(2*c0 + 1)
    -a*alpha*c1**2*(2*c0 + 1)
    a*c1**2*(-2*alpha*c0 - alpha + c1)
    a*c1**2*(alpha*c1 + 2*c0 + 1)
- branch_attempts:
    {'solution': {'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'b': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'DEGENERATE', 'nontrivial_reason': 'a == 0 and b == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}
    {'solution': {'a': '0', 'c1': '0'}, 'substitution_status': 'success', 'nontrivial_status': 'CONSTANT_TRIVIAL', 'nontrivial_reason': 'c1 == 0', 'identity_verification_status': 'skipped', 'residual': None, 'two_node_branch_classification': None}

