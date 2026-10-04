# v1.0.0 executable smoke test

Test date: 2026-10-04.

All 24 Python files in the package compile under Python 3.13.5. The relational rotation self-test passes. The following portable late-stage experiments were executed on one confirmatory seed each to verify dependency resolution and runnable public paths:

| Experiment | Seed | Result |
|---|---:|---|
| R06 full-loop operator | 151000 | PASS |
| R07 half-channel factorization | 153000 | PASS |
| M08 native mode competition | 170000 | PASS |
| M09 input-output mismatch | 172000 | PASS |
| C01 native co-product closure | 174000 | PASS |
| C07 dynamic causal closure | 184000 | PASS |
| G01 fixed closure + gain | 186000 | PASS |
| G02 projective basin | 188000 | PASS |

This is an executability smoke test, not a claim that one seed reproduces the confirmatory statistics. R06/R07 have separate multi-seed reconstruction validation against archived outputs in `RECONSTRUCTION_VALIDATION.md`; the confirmatory result tables remain the numerical source of record.

Post-confirmatory audit outputs were also regenerated during adversarial pre-release review: 64-seed norm-restoration audit, four-pair x 64-seed context-transfer audit, and 16-seed epsilon sensitivity audit. These remain non-confirmatory robustness analyses.
