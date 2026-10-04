# Paper IV — Source Recovery Report v0.1

## Outcome

The source audit materially improved. The missing confirmatory preregistrations that had been flagged in the Methods audit were found in the persistent Library and restored into the reproduction package, including the late operator, modal-drift, closure, and regenerative-reentry blocks.

Recovered exact preregistrations include:

- `reactor_full_loop_operator_gain_confirmatory_prereg.json`
- `reactor_loop_half_operator_factorization_confirmatory_prereg.json`
- `reactor_loop_mode_drift_confirmatory_prereg.json`
- `reactor_native_modal_closure_coproduct_confirmatory_prereg.json`
- `reactor_dynamic_half_channel_closure_map_confirmatory_prereg.json`
- `reactor_fixed_instance_closure_multigeneration_confirmatory_prereg.json`
- `reactor_fixed_closure_modal_attractor_confirmatory_prereg.json`
- `reactor_contextual_trace_reactivation_confirmatory_prereg.json`
- `reactor_multi_trace_K_superposition_confirmatory_prereg.json`
- `reactor_K_storage_superposition_nonlinear_readout_confirmatory_prereg.json`
- `reactor_K_readout_nonlinearity_localization_confirmatory_prereg.json`
- `reactor_native_written_field_hysteresis_confirmatory_prereg.json`
- `reactor_mx_memory_relay_confirmatory_prereg.json`

The base source `reactor_v012.py` was also recovered as a Library artifact and included in the archive.

## Late runner code preserved from the conversation transcript

The exact code blocks visible in the current conversation were written to `code/reconstructed_from_chat/` for:

- dynamic half-channel closure map
- fixed instance-specific multigeneration closure
- projective-attractor test
- native modal-closure coproduct test
- native mode-competition test
- input-output modal mismatch/non-normality test

These files preserve the code shown in the conversation, but they are marked as **reconstructed from chat provenance**, not as independently archived originals.

## Remaining critical gaps

The package is not yet fully executable because the following original source files have not been recovered:

1. The rotational-relation scaffold implementing the exact hidden 4D block rotation `R4(phi)` used in Paper IV's history-dependent branch.
2. `reactor_full_loop_operator_gain_diagnostic.py`, the shared relay/operator runner used by several late scripts.
3. `reactor_loop_half_operator_factorization_diagnostic.py`, the half-channel factorization dependency used by the final closure-map script.

The accessible sources verify the operational relation dynamics and all confirmatory decision rules, but the original executable bodies of these dependencies must still be recovered before a claim of complete computational reproducibility.

## Editorial consequence

The manuscript may now use the recovered preregistration files as the authoritative source for hypotheses, seed ranges, thresholds, controls, and scope warnings. Final Methods prose should still wait for recovery of the three critical executable dependencies above, or explicitly state that the released source archive is partial.
