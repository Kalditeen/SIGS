SIGS + Stage-I audit report
Repository: /Users/kang/SIGS
Output: /Users/kang/SIGS/results/sigs_stage1_audit_20261123_084737

PART A: SIGS expression capability
  See report.json and part_A_all_expressions.csv.
  part_A_univariate_function_candidates.csv contains extracted one-variable
  function-bearing subexpressions that may be considered as activation candidates.

PART B: Stage-I reference independence
  See report.json and part_B_candidates_*.csv.
  B1 changes only PDESpec.true_solution while keeping the PDE/search config fixed.
  B2 additionally removes explicit sech/sech2 target-family seeds and x-2*t atoms.

Interpretation warning:
  The current Stage I is a structural prefilter. It does not currently rank
  candidates by PDE residual. Passing B1 only proves that true_solution is not
  directly read by stage_one(); it does not prove that Stage I is free from
  manually designed function/phase priors or that it discovers exact solutions.

No source files were modified.