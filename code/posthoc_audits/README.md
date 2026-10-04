# Post-confirmatory audit code

These scripts were added during adversarial pre-release review. They are **not** part of the prospectively frozen confirmatory criteria and do not redefine any confirmatory outcome. They use the portable/reference-reconstruction execution pathway to probe three referee-facing robustness questions:

- `audit_fixed_dynamic_no_renorm.py`: contribution of post-closure norm restoration;
- `audit_multicontext_transfer.py`: transfer over four symmetry-related context pairs on the existing C07 cohort;
- `audit_operator_epsilon_sensitivity.py`: central-difference sensitivity for epsilon = 1e-3, 1e-4, 1e-5 on 16 seeds.

Archived outputs are under `results/robustness/`.
