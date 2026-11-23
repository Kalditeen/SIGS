# Phase 3-C/D Non-travelling Analysis

The structures below are templates, not known solutions.  Their labels
describe the network shape only; the mathematical travelling-wave test
is run separately and never assumes non-travelling behaviour.

## Template profiles

| template | tag | nodes | phases | parameters | wave classification |
|---|---|---|---|---|---|
| space_time_separated | SPACE_TIME_SEPARATED | 2 | 2 | 12 | NON_TRAVELING_WAVE_CANDIDATE |
| space_time_composite | SPACE_TIME_COMPOSITE | 3 | 2 | 14 | NON_TRAVELING_WAVE_CANDIDATE |
| multi_phase | MULTI_PHASE | 2 | 2 | 13 | NON_TRAVELING_WAVE_CANDIDATE |
| traveling_wave_baseline | TRAVELING_WAVE_ORIENTED | 1 | 1 | 7 | TRAVELING_WAVE_CONFIRMED |

## Stage2 results

| candidate | status | degeneracy | failure reason |
|---|---|---|---|
| candidate_0001 | VERIFICATION_FAILED | UNKNOWN | solver produced branches but none passed independent back-substitution verification |
| candidate_0002 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0003 | CONSTRAINT_FAILED | UNKNOWN | coefficient solve system too large |
| candidate_0004 | VERIFICATION_FAILED | UNKNOWN | solver produced branches but none passed independent back-substitution verification |
