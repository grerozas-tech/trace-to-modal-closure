# Manual GitHub upload

This package is prepared to be uploaded as the complete initial repository state.

1. Unzip the release bundle locally.
2. Open `grerozas-tech/trace-to-modal-closure` on GitHub.
3. Choose **Add file -> Upload files**.
4. Upload the **contents** of the `trace-to-modal-closure/` directory, preserving folders.
5. Suggested commit message:

   `Publish Paper IV preprint and reproducibility package v1.0.0`

6. Before creating a GitHub Release, verify that `paper/trace_to_modal_closure.pdf`, `paper/trace_to_modal_closure_supplement.pdf`, `code/`, `protocols/`, `results/`, and `MANIFEST_SHA256.txt` are visible.
7. Create tag/release `v1.0.0`.
8. Archive the GitHub release with Zenodo.
9. After Zenodo assigns the version DOI, update the DOI fields/badge in `README.md` and `CITATION.cff` in a small follow-up commit (or before final journal submission).
