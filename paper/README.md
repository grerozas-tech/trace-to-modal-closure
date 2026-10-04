# Paper build

This directory contains the v1.0.0 preprint and Supplement source. The build regenerates publication artifacts from archived result tables; it does not rerun every experiment.

## Files

- `main.tex` / `trace_to_modal_closure.pdf` — main manuscript.
- `supplement.tex` / `trace_to_modal_closure_supplement.pdf` — Supplementary Information.
- `references.bib` — machine-readable bibliography used as the repository reference file; the PDF also embeds a manual bibliography so it builds without BibTeX.
- `figures/make_figures.py` — regenerates all main and supplementary figures from `../results/`.
- `figures/*.pdf` — vector figures included by LaTeX.
- `figures/*.png` — convenient GitHub previews.

## Build

From the repository root:

```bash
bash rebuild_paper.sh
```

Or:

```bash
python paper/figures/make_figures.py
cd paper
pdflatex main.tex
pdflatex main.tex
pdflatex supplement.tex
pdflatex supplement.tex
```

`main.tex` uses REVTeX 4.2 in PRE-style preprint layout. `supplement.tex` uses a portable article layout.
