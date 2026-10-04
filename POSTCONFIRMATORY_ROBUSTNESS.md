# Post-confirmatory robustness audit

These analyses were added during adversarial pre-release review and are not prospectively frozen confirmatory tests.

## Renormalization

Across the 64-seed portable G01 reference reproduction, the factor required to restore the pre-closure norm after applying `C_dyn` had overall mean 1.000243, median 1.000099, and range 1.000005--1.005344 across 256 seed-generation packets. At generation 4, mean relative norm was 0.982555 with norm restoration and 0.981634 without it in the same reference reproduction. The archived confirmatory G01 result remains the numerical source of record.

## Multiple context pairs

Four symmetry-related calibration-to-test transfers were evaluated on the same 64-seed C07 cohort. Across 256 seed-pair cells, mean transferred alignment was 0.999576; 254/256 exceeded 0.99. The dynamic map exceeded the tested static map in all cells by mean 0.416856. Closure-need MAE was 0.004611; 253/256 cells were below 0.03. Because pair selection occurred after the confirmatory study and reuses the same cohort, this is robustness evidence, not a new confirmatory generalization claim.

## Finite-difference epsilon

On seeds 184000--184015, epsilon values 1e-3, 1e-4, and 1e-5 produced indistinguishable transferred alignment to displayed precision (mean 0.999748) and sign-invariant modal-vector cosines > 0.99999999999998 relative to the 1e-4 baseline.
