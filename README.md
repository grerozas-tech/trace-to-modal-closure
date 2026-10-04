# From Trace to Modal Closure

**Dynamic Conditions for Regenerative Reentry in a Path-Dependent Adaptive System**

**Author:** Gregorio Rozas Fernández  
**Affiliation:** Independent Researcher  
**Version:** v1.0.0  
**Status:** public preprint release, October 4, 2026  
**Repository:** https://github.com/grerozas-tech/trace-to-modal-closure  
**Version DOI:** 10.5281/zenodo.23144597  
**Concept DOI (all versions):** 10.5281/zenodo.23144596

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23144596.svg)](https://doi.org/10.5281/zenodo.23144596)

## Overview

This repository accompanies the preprint **From Trace to Modal Closure: Dynamic Conditions for Regenerative Reentry in a Path-Dependent Adaptive System**.

The paper asks when historical organization that remains causally available can also survive repeated transmission through the same path-dependent adaptive system.

The central causal arc is:

```text
history
  -> distributed trace
  -> contextual / relational readout
  -> causal reentry
  -> modal selection
  -> input-output modal mismatch
  -> modal closure
  -> finite-horizon regenerative reentry
```

The paper separates distinctions that are easy to conflate:

- trace is not reentry;
- selection is not reproduction;
- reentry is not regeneration;
- gain controls how much survives, while closure controls whether what returns is geometrically reusable.

## Main result

The native `x -> m -> x` relay is causal but strongly dissipative and non-normal. Its best-transmitted input mode is returned along a substantially different output direction. Scalar gain compensation therefore preserves magnitude locally without repairing the geometry needed for the next passage.

An instance-specific closure map reconstructed from the effective causal write and return operators,

```text
A = d m_after_write / d x_before
B = d x_after_return / d m_before
T = B A
```

is frozen in a calibration context and transferred to a distinct test context. Combined with one fixed scalar gain, it preserves near-unit packet amplitude and reusable modal geometry across four tested nonlinear generations. The same fixed gain without geometric closure decays strongly.

This establishes a **sufficiency result for finite-horizon regenerative reentry** in the tested system.

## Scientific claim boundary

This repository does **not** claim:

- autonomous or endogenous learning of the closure map;
- autopoiesis or energetic self-maintenance;
- asymptotic stability of the full simulator;
- a universal closure law across arbitrary systems;
- biological memory;
- phenomenology, consciousness, or subjective experience.

`Regenerative reentry` is used operationally for persistence of transmissible organization over a finite externally corrected protocol.

## Paper

The publication-ready manuscript and Supplement are included under `paper/`:

```text
paper/
├── trace_to_modal_closure.pdf
├── main.tex
├── trace_to_modal_closure_supplement.pdf
├── supplement.tex
├── references.bib
├── figures/
│   ├── make_figures.py
│   ├── fig1_history_trace.{pdf,png}
│   ├── ...
│   └── figS8_static_failures.{pdf,png}
└── README.md
```

The figures are generated from the released result tables wherever those aggregate tables are available; a small number of audited aggregate controls that are not separately released as summary CSVs are encoded in the figure script and identified there. Schematic or scaled display elements are labeled in captions.

## Reproducibility status

The release provides an executable, source-auditable **scientific reproduction pathway**.

Three provenance classes are kept separate:

- **ORIGINAL** — independently recovered archived source or result artifacts;
- **TRANSCRIPT_RECOVERED** — code copied verbatim from visible executable blocks in the frozen research transcript;
- **REFERENCE_RECONSTRUCTION** — executable reconstructions of transient dependencies that were not independently archived, validated against frozen specifications and archived outputs.

The three reference reconstructions are:

- `reactor_relational_rotation.py`;
- `reactor_full_loop_operator_gain_diagnostic.py`;
- `reactor_loop_half_operator_factorization_diagnostic.py`.

They are **not** claimed to be byte-identical copies of the transient original files. The relational rotation satisfies the frozen causal-signature test, and the reconstructed operator scaffolds closely reproduce archived singular-value quantities and preserve the scientific decisions targeted by the reconstruction audit.

The exact transcript-recovered late-stage runners retain their historical `/mnt/data` paths under `code/transcript_recovered/`. For ordinary cloning and execution, `code/portable/` contains path-only portable adaptations together with the required original/reconstructed dependencies.

See:

- `PROVENANCE.md`
- `RECOVERY_STATUS.md`
- `RECONSTRUCTION_VALIDATION.md`
- `provenance/SOURCE_EXPORT_HASHES.txt`

## Post-confirmatory robustness

After adversarial pre-release review, three explicitly post-confirmatory audits were added without altering the frozen primary outcomes: (i) disabling post-closure norm restoration, (ii) repeating dynamic closure transfer over four symmetry-related context pairs on the existing C07 cohort, and (iii) varying the finite-difference step over `1e-3`, `1e-4`, and `1e-5` on a 16-seed subset. These analyses are kept under `code/posthoc_audits/` and `results/robustness/` and are not presented as preregistered or confirmatory tests. See `POSTCONFIRMATORY_ROBUSTNESS.md`.

## Repository structure

```text
.
├── README.md
├── CITATION.cff
├── .zenodo.json
├── LICENSE
├── LICENSE-CODE
├── LICENSE-CONTENT.md
├── CHANGELOG.md
├── RELEASE_NOTES.md
├── PROVENANCE.md
├── RECOVERY_STATUS.md
├── RECONSTRUCTION_VALIDATION.md
├── MANIFEST_SHA256.txt
├── requirements.txt
├── ENVIRONMENT.md
├── EXECUTION_COVERAGE.md
├── SMOKE_TEST.md
├── rebuild_paper.sh
├── paper/
├── code/
│   ├── original/
│   ├── transcript_recovered/
│   ├── reference_reconstruction/
│   ├── portable/
│   └── posthoc_audits/
├── protocols/
│   ├── confirmatory/original/
│   ├── confirmatory/transcript_recovered/
│   └── diagnostic/original/
├── results/
│   ├── main/
│   ├── supplementary/
│   └── robustness/
└── provenance/
    ├── metadata/
    ├── manifests/
    └── SOURCE_EXPORT_HASHES.txt
```

Raw research-conversation exports are intentionally **not** included in the public repository because they contain unrelated material. Their filenames and hashes are preserved instead.

## Build the paper and figures

Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Regenerate figures and PDFs:

```bash
bash rebuild_paper.sh
```

`rebuild_paper.sh` rebuilds the figures and PDFs from the archived result tables. It does not claim to rerun every historical experiment. Experiment-by-experiment execution coverage is documented in `EXECUTION_COVERAGE.md`.

Or manually:

```bash
python paper/figures/make_figures.py
cd paper
pdflatex main.tex
pdflatex main.tex
pdflatex supplement.tex
pdflatex supplement.tex
```

A TeX distribution including REVTeX 4.2 is required for `main.tex`.

## Quick executable checks

```bash
cd code/portable
python reactor_relational_rotation.py
python reactor_full_loop_operator_gain_diagnostic.py
python reactor_loop_half_operator_factorization_diagnostic.py
```

The latter two direct commands run the documented eight-seed reconstruction-validation subsets. Full frozen cohorts can be executed by importing the runners and passing the corresponding seed ranges listed in the paper/Supplement.

## Licensing

- Source code and executable scripts: MIT.
- Original paper text, documentation, figures, and original numerical presentation: CC BY 4.0.

## Citation and DOI

For the archival v1.0.0 release, cite:

**Rozas Fernández, Gregorio (2026). _From Trace to Modal Closure: Dynamic Conditions for Regenerative Reentry in a Path-Dependent Adaptive System_. Version 1.0.0. Zenodo. DOI: 10.5281/zenodo.23144597.**

- Version DOI: `10.5281/zenodo.23144597`
- Concept DOI (all versions): `10.5281/zenodo.23144596`
