# Paper IV reproduction package — recovery status

## Current status

The v1.0.0 archival release contains an executable, source-auditable **scientific reproduction pathway** for the principal operator, closure, and finite-horizon regenerative-reentry chain.

The former three-dependency executability gap has been replaced by explicitly labeled, validated `REFERENCE_RECONSTRUCTION` files. This resolves practical execution of the pathway without claiming byte-identical recovery of the transient original files.

## Recovered original artifacts

The release preserves as independently recovered originals:

- the base C4 reactor `reactor_v012.py`;
- recovered prospectively frozen confirmatory design JSONs, including additional originals recovered during the final pre-release audit;
- archived result tables, diagnostics, summaries, and primary tests;
- the Methods audit, Master Matrix, and source-recovery reports.

## Transcript-recovered source

Six late-stage experiment runners are preserved verbatim from visible code blocks in the frozen research transcript. They remain under `code/transcript_recovered/` with their historical transient paths unchanged.

## Validated reference reconstructions

The following unarchived transient dependencies were reconstructed:

1. `reactor_relational_rotation.py`
2. `reactor_full_loop_operator_gain_diagnostic.py`
3. `reactor_loop_half_operator_factorization_diagnostic.py`

The relational rotation passes the frozen causal-signature self-check across the audited relation angles. The two operator scaffolds were validated against archived confirmatory outputs; see `RECONSTRUCTION_VALIDATION.md`.

## Portable execution

`code/portable/` provides a self-contained path-only adaptation of the principal late-stage execution chain. The provenance-preserving source directories remain separate.

## Remaining limitation

The original transient noise-seed mixer was not independently archived. The reference implementation guarantees deterministic matched noise within compared branches, but not forensic identity of every historical random stream. Exact seedwise equality is therefore not expected for every auxiliary quantity.

The release distinguishes:

- **scientific reproduction of frozen primary mechanisms/results**, from
- **forensic byte-level reconstruction of every transient computation**.

## Release classification

The release may be described as:

> an executable, source-auditable preprint and reproducibility package with explicitly labeled validated reference reconstructions for three unarchived transient dependencies.

It should not be described as byte-identical preservation of every original transient source file.

## Historical status reports

Earlier recovery reports are preserved byte-for-byte under `provenance/metadata/historical/`. Their former "not fully executable" statements are historical snapshots and are superseded by this file.
