#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
# Rebuilds figures and publication PDFs from archived result tables; it does not rerun every experiment.
python "$ROOT/paper/figures/make_figures.py"
cd "$ROOT/paper"
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
mv -f main.pdf trace_to_modal_closure.pdf
mv -f supplement.pdf trace_to_modal_closure_supplement.pdf
rm -f main.aux main.log main.out mainNotes.bib supplement.aux supplement.log supplement.out supplementNotes.bib
printf 'Built paper/trace_to_modal_closure.pdf and paper/trace_to_modal_closure_supplement.pdf\n'
