# Release notes — v1.0.0

This is the archival public-preprint and reproducibility release for **From Trace to Modal Closure: Dynamic Conditions for Regenerative Reentry in a Path-Dependent Adaptive System**.

## Scientific endpoint

The release supports the limited claim that externally supplied instance-specific modal closure plus fixed scalar gain is sufficient for finite-horizon regenerative reentry across four tested nonlinear generations in the studied reactor.

It does not claim endogenous learning of closure/gain, asymptotic stability, autonomy, autopoiesis, biological memory, phenomenology, or consciousness.

## Final pre-release hardening

Before archival freeze, the package underwent external and adversarial review. The final release:

- makes the adaptive timestep and modal metrics mathematically self-contained;
- reserves generation labels G1--G4 and uses `q_cal` / `q_test` for operator carriers;
- expands the literature context around non-normal dynamics, Procrustes/polar geometry, loop gain, recurrent/reservoir dynamics, and local operator identification;
- includes a global evidence/provenance audit and additional recovered original design JSONs;
- corrects the exact timestep indexing of `m`, `K`, and C4 `theta` to the recovered base source;
- documents the local-linear equivalence between memory-stage gain and loop-level scalar gain;
- adds explicitly post-confirmatory robustness audits for post-closure norm restoration, multi-context transfer, and finite-difference epsilon sensitivity;
- adds seed-level distributions/bands to central figures;
- provides execution coverage, a pinned environment, portable late-stage execution, reconstruction validation, and SHA-256 manifests.

None of the post-confirmatory robustness analyses redefine the frozen pass/fail status of the confirmatory experiments.

## Included

- `paper/trace_to_modal_closure.pdf` and LaTeX source;
- `paper/trace_to_modal_closure_supplement.pdf` and source;
- six main and eight supplementary figures with generation script;
- archived main, supplementary, and robustness result tables;
- recovered prospectively frozen design JSONs;
- original base reactor source;
- six verbatim transcript-recovered late-stage runners;
- three validated reference reconstructions;
- repository-relative portable execution copies;
- evidence/provenance and source-recovery metadata;
- executable smoke-test documentation;
- SHA-256 manifest and hashes for excluded private source exports.

## Reproducibility note

Three transient dependencies were not independently archived byte-for-byte. They are released as clearly labeled reference reconstructions and validated against frozen specifications and archived numerical outputs. The original transient noise-seed mixer was not recovered, so exact equality of every auxiliary seedwise quantity is not claimed.

## DOI

The Zenodo version DOI is pending archival of the GitHub v1.0.0 release. After deposit, the DOI should be added to `README.md` and `CITATION.cff` without changing the scientific content of the release.
