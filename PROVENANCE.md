# Paper IV — provenance model

This repository keeps provenance classes explicit so reconstructed or adapted source is never confused with independently archived original source.

## ORIGINAL

Artifacts independently recovered from the persistent Library, runtime, or archived research files.

Examples include:

- `code/original/reactor_v012.py`;
- prospectively frozen confirmatory design JSONs under `protocols/confirmatory/original/`;
- the final pre-release audit recovered additional original design JSONs from the persistent Library; these are released under the same ORIGINAL class;
- primary result CSVs, diagnostics, summaries, and test tables under `results/`.

## TRANSCRIPT_RECOVERED

Source copied verbatim from visible executable or JSON blocks in the frozen research transcript.

These files preserve the exact text visible in the research record, but no claim is made that they were independently archived as standalone files at experiment time. The six late-stage runners are preserved unchanged under `code/transcript_recovered/`.

## REFERENCE_RECONSTRUCTION

Executable replacements reconstructed from the frozen transcript, recovered original designs, archived result schemas, original base reactor source, and downstream interface requirements.

A reference reconstruction is required to satisfy:

1. **specification consistency** — interfaces, dimensions, timing, interventions, and frozen causal signatures agree with the recovered record;
2. **empirical validation** — primary numerical outputs are compared with archived confirmatory results and the targeted frozen scientific decisions are preserved.

The three reference reconstructions are:

- `reactor_relational_rotation.py`;
- `reactor_full_loop_operator_gain_diagnostic.py`;
- `reactor_loop_half_operator_factorization_diagnostic.py`.

## PORTABLE_ADAPTATION

The exact transcript-recovered late-stage files were written in a transient `/mnt/data` runtime. For normal cloning, `code/portable/` contains a self-contained execution directory. Its copies of the six transcript-recovered runners change only the dependency path from `/mnt/data` to the script directory; required ORIGINAL and REFERENCE_RECONSTRUCTION dependencies are copied alongside them.

The exact transcript versions remain separately preserved and are the documentary source of truth.

## Validation boundary

The reconstruction target is **scientific reproducibility**, not forensic source recovery.

The package does not claim that a `REFERENCE_RECONSTRUCTION` is byte-identical to the missing transient source. In particular, the original transient noise-seed mixer was not independently archived. Deterministic matched-noise semantics are reconstructed, while exact random-stream identity is not claimed.

A reconstruction is considered validated when the recovered protocol is implemented, primary numerical quantities show close correspondence to archived outputs, and the frozen scientific decision targeted by the audit is preserved. Auxiliary historical-packet columns can differ when they depend on unrecovered random-stream details.

## Research-transcript privacy boundary

Raw conversation-export JSON files were used during source recovery but are not released because they contain material unrelated to the scientific package. `provenance/SOURCE_EXPORT_HASHES.txt` records their filenames and SHA-256 hashes. Scientific code/design artifacts extracted from those records are released separately under their explicit provenance class.

## POSTCONFIRMATORY_AUDIT

Code and outputs added during adversarial pre-release review are kept under `code/posthoc_audits/` and `results/robustness/`. They test renormalization, context-pair robustness, and finite-difference sensitivity. They are not represented as prospectively frozen confirmatory analyses.
