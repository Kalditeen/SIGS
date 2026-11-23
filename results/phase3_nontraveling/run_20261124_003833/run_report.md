# Phase 3-A Automatic Solving Report

Raw Stage2 records are retained in `candidate_results.json`.
Only branches whose raw Gardner residual was symbolically certified
zero are listed as exact.

## Summary

- candidate_total: 4
- status_counts: {'VERIFICATION_FAILED': 2, 'CONSTRAINT_FAILED': 2}
- exact_candidates: 0
- exact_branches: 0
- degeneracy_counts: {'UNKNOWN': 4}
- total_wall_seconds: 0.5024817919984343
- structure_info: {'space_time_separated': {'structure_tag': 'SPACE_TIME_SEPARATED', 'node_count': 2, 'phase_count': 2, 'expression': 'c0 + c_st*tanh(bias_st + w_pt__st*(b_pt*t + d_pt)) + c_sx*sin(bias_sx + w_px__sx*(a_px*x + d_px))', 'parameter_count': 12, 'traveling_wave': {'classification': 'NON_TRAVELING_WAVE_CANDIDATE', 'wave_speed': None, 'reason': 'standard travelling-wave relation was symbolically excluded'}}, 'space_time_composite': {'structure_tag': 'SPACE_TIME_COMPOSITE', 'node_count': 3, 'phase_count': 2, 'expression': 'c0 + c_mix*tanh(bias_mix + w_st__mix*cos(bias_st + w_pt__st*(b_pt*t + d_pt)) + w_sx__mix*sin(bias_sx + w_px__sx*(a_px*x + d_px)))', 'parameter_count': 14, 'traveling_wave': {'classification': 'NON_TRAVELING_WAVE_CANDIDATE', 'wave_speed': None, 'reason': 'standard travelling-wave relation was symbolically excluded'}}, 'multi_phase': {'structure_tag': 'MULTI_PHASE', 'node_count': 2, 'phase_count': 2, 'expression': 'c0 + c_f1*sin(bias_f1 + w_p1__f1*(a_p1*x + b_p1*t + d_p1)) + c_f2*cos(bias_f2 + w_p2__f2*(a_p2*x + b_p2*t + d_p2))', 'parameter_count': 13, 'traveling_wave': {'classification': 'NON_TRAVELING_WAVE_CANDIDATE', 'wave_speed': None, 'reason': 'standard travelling-wave relation was symbolically excluded'}}, 'traveling_wave_baseline': {'structure_tag': 'TRAVELING_WAVE_ORIENTED', 'node_count': 1, 'phase_count': 1, 'expression': 'c0 + c_f1*tanh(bias_f1 + w_p1__f1*(a_p1*x + b_p1*t + d_p1))', 'parameter_count': 7, 'traveling_wave': {'classification': 'TRAVELING_WAVE_CONFIRMED', 'wave_speed': '-b_p1/a_p1', 'reason': 'SymPy solved u_t + c*u_x == 0 with c independent of x,t'}}}

## Candidate Results

| candidate | status | degeneracy | failure |
|---|---|---|---|
| candidate_0001 | VERIFICATION_FAILED | UNKNOWN | solver produced branches but none passed independent back-substitution verification |
| candidate_0002 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0003 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0004 | VERIFICATION_FAILED | UNKNOWN | solver produced branches but none passed independent back-substitution verification |
