# Paper IV — Source Recovery Report v0.2

## Outcome

The documentary recovery step is now materially stronger than v0.1.

### Exact original artifacts recovered from the persistent Library

The following confirmatory preregistrations were materialized as original JSON artifacts into `prereg/original/`:

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

These files are no longer reconstructed from memory or narrative summaries; they preserve the original seed ranges, prospective hypotheses, thresholds, controls, and scope warnings.

### Source-export JSONs recovered from the persistent Library

The package now also contains the raw ChatGPT Exporter JSONs used by the draft's editorial traceability annex:

- `ChatGPT-Revisar láminas antes del experimento-20261003-2342.json`
- `ChatGPT-Revisar láminas antes del experimento-20261004-0055.json`
- `ChatGPT-Revisar láminas antes del experimento-20261004-0134.json`
- `ChatGPT-Revisar láminas antes del experimento-20261004-0157.json`

They are preserved in `source_exports/` as documentary sources. They are not treated as substitutes for executable source code.

### Files recovered from exact visible transcript code

The v0.1 package already preserved exact visible runner code for the late closure/relay blocks in `code/reconstructed_from_chat/`. The v0.2 package additionally records transcript-recovered prereg/design files for the static reciprocity/subspace supplement in `prereg/recovered_from_transcript_v02/`.

The provenance distinction remains explicit: `original` means an artifact was recovered from the Library/runtime; `recovered_from_transcript` means the text was copied from an exact visible code/JSON block in the research transcript.

## Remaining critical executable gaps

The archive is **still not fully executable end-to-end** because three original source dependencies remain unresolved:

1. The exact rotational-relation reactor branch implementing the hidden 4D relation `R4(phi)` used by Paper IV's continuous relation histories.
2. `reactor_full_loop_operator_gain_diagnostic.py`, the shared late-stage relay/operator runner.
3. `reactor_loop_half_operator_factorization_diagnostic.py`, the half-channel factorization dependency used by the final dynamic closure script.

No substitute implementation has been silently invented for these files.

## Editorial consequence

The manuscript can now treat the recovered original preregistrations as authoritative sources for confirmatory design, seed cohorts, thresholds and interpretation rules. Final Methods prose should remain conservative about executable reproducibility until the three critical dependencies are recovered or explicitly declared unavailable in the code/data statement.

The Paper IV / Paper V boundary remains locked: endogenous learning of `C_i` or `gamma_i` is not part of Paper IV.
