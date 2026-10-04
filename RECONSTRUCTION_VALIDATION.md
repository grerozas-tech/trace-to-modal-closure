# Paper IV missing-source reconstruction validation

The three files below are executable reference replacements reconstructed from the frozen research conversation, recovered original designs, archived result schemas, and `reactor_v012.py`. They are not claimed to be byte-identical copies of the transient originals.

## `R4(phi)`

The sign convention is fixed by the recovered causal-signature estimator. The deterministic noiseless self-check passes for:

`-135, -90, -45, 0, 45, 90, 135, 180` degrees.

## Full-loop operator — eight archived confirmatory seeds, 151000–151007

| Metric | Archived mean | Reconstructed mean | MAE | Seedwise r |
|---|---:|---:|---:|---:|
| G0 sigma1 | 0.109109 | 0.108412 | 0.001595 | 0.9980 |
| G1 sigma1 | 0.108898 | 0.109649 | 0.001372 | 0.9989 |
| G0 sigma2 | 0.065195 | 0.064653 | 0.001814 | 0.9914 |
| G1 sigma2 | 0.065013 | 0.064929 | 0.001250 | 0.9965 |

## Half-channel factorization — eight archived confirmatory seeds, 153000–153007

| Metric | Archived mean | Reconstructed mean | MAE | Seedwise r |
|---|---:|---:|---:|---:|
| G0 sigmaA | 0.145947 | 0.144942 | 0.003359 | 0.9892 |
| G0 sigmaB | 1.270538 | 1.268840 | 0.016012 | 0.9955 |
| G0 sigmaT | 0.112234 | 0.110623 | 0.002794 | 0.9934 |
| G1 sigmaA | 0.146744 | 0.147245 | 0.001765 | 0.9981 |
| G1 sigmaB | 1.298164 | 1.273523 | 0.028581 | 0.9807 |
| G1 sigmaT | 0.114413 | 0.113208 | 0.001734 | 0.9982 |

The close seedwise correspondence of the primary singular-value quantities is the validation target for the missing operator scaffolds. Exact historical-packet auxiliary columns can differ because the original transient noise-seed mixer and history runner were not independently archived.

## Portable smoke checks

The v1.0.0 package was additionally checked after repository assembly:

- all Python files in `code/portable/` compile;
- `python reactor_relational_rotation.py` returns `R4 self-check: PASS`;
- the portable full-loop audit executes seed 151000 and returns finite G0/G1 singular gains;
- the portable half-channel audit executes seed 153000 and returns finite `sigmaA`, `sigmaB`, and `sigmaT`;
- the portable dynamic-closure runner executes a C07 seed and produces near-unit own-map alignment.

These smoke checks verify path portability and executable dependency resolution; the archived CSVs remain the authoritative evidence for the published cohort-level numerical results.
