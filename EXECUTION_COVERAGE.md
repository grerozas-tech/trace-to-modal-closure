# Execution coverage

This table separates **paper rebuildability** from **experiment rerunnability**. `rebuild_paper.sh` regenerates figures and PDFs from archived CSVs; it is not represented as an end-to-end rerun of every historical experiment.

The original base reactor is released under `code/original/`. The Paper-IV rotational relation and the two shared operator scaffolds are released as validated `REFERENCE_RECONSTRUCTION` files. Six late-stage runners are preserved verbatim from the frozen research transcript and also provided as path-only portable adaptations.

| ID | Archived design/results | Runner provenance | Independently runnable from public package? | Validation / boundary |
|---|---|---|---|---|
| T01 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| T04 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| T05 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| T06 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| T07 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| F01 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| F02 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| F03 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| F04 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| R01 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| R02 | frozen working record + results (standalone JSON unavailable) | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| R03 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| R04 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| R05 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| R06 | design + results | REFERENCE_RECONSTRUCTION | yes | one-seed portable smoke PASS; independently validated against archived operator outputs; frozen conclusions preserved |
| R07 | design + results | REFERENCE_RECONSTRUCTION | yes | one-seed portable smoke PASS; independently validated against archived half-channel outputs; frozen conclusions preserved |
| M01 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| M02 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| M03 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| M04 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| M05 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| M06 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| M07 | diagnostic result record | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| M08 | design + results | TRANSCRIPT_RECOVERED + portable path adaptation | yes | portable one-seed smoke test PASS; archive remains numerical source of record |
| M09 | design + results | TRANSCRIPT_RECOVERED + portable path adaptation | yes | portable one-seed smoke test PASS; archive remains numerical source of record |
| C01 | design + results | TRANSCRIPT_RECOVERED + portable path adaptation | yes | portable one-seed smoke test PASS; archive remains numerical source of record |
| C02 | diagnostic record + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| C03 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| C04 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| C05 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| C06 | design + results | runner not recovered as public standalone source | no | archived design/results support manuscript; not independently rerunnable from this release |
| C07 | design + results | TRANSCRIPT_RECOVERED + portable path adaptation | yes | portable one-seed smoke test PASS; depends on validated R06/R07 operator reconstruction |
| G01 | design + results | TRANSCRIPT_RECOVERED + portable path adaptation | yes | portable one-seed smoke test PASS; depends on dynamic closure/operator reconstruction |
| G02 | design + results | TRANSCRIPT_RECOVERED + portable path adaptation | yes | portable one-seed smoke test PASS; depends on fixed-closure chain |

## Executable late-stage chain

The public package contains runnable code for the central late-stage operator/closure chain: R06, R07, M08, M09, C01, C07, G01, and G02. This does **not** imply byte-identical replay of the transient originals. R06/R07 and the relation rotation are reference reconstructions; six downstream runners are transcript-recovered. The unrecovered transient noise-seed mixer means exact equality of every auxiliary seedwise quantity is not claimed.

## Post-confirmatory audit coverage

The release also includes three new referee-facing audit scripts under `code/posthoc_audits/`. They are explicitly post-confirmatory and do not alter frozen outcomes. The archived outputs are under `results/robustness/`.

- norm-restoration audit: 64-seed G01 portable reference reproduction;
- multi-context transfer audit: four symmetry-related pairs x 64 C07 seeds;
- epsilon sensitivity: 16 C07 seeds at `1e-3`, `1e-4`, and `1e-5`.

## Rebuild command

```bash
python -m pip install -r requirements.txt
bash rebuild_paper.sh
```

For provenance and reconstruction validation, see `PROVENANCE.md` and `RECONSTRUCTION_VALIDATION.md`. For the complete evidence/design audit, see `provenance/EVIDENCE_AUDIT.csv` and the Supplementary Information.
