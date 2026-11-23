# Multi-seed generated-only search

- mode: generated-only
- requested candidates per seed: 100
- seeds: [101, 202, 303, 404, 505]

| seed | generated | unique | constraint | solve | branches | candidates | distinct | failed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 101 | 100 | 79 | 72 | 70 | 6 | 5 | 5 | 74 |
| 202 | 100 | 78 | 74 | 72 | 7 | 4 | 4 | 74 |
| 303 | 100 | 80 | 76 | 72 | 9 | 6 | 6 | 74 |
| 404 | 100 | 81 | 74 | 71 | 5 | 4 | 4 | 77 |
| 505 | 100 | 68 | 64 | 58 | 8 | 6 | 6 | 62 |

## Exact source expressions found across seeds

- `JacobiCN(z, m)**2`
- `JacobiDN(z, m)**2`
- `JacobiSN(z, m)**2`
- `sech(z)**2`
- `tan(z)**2`
- `tanh(alpha*z)**2`
- `tanh(z)**2`
- `z**(-2)`
