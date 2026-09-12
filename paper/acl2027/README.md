# DESA manuscript

Edit `markdown/*.md`; `sections/*.tex` is generated. Build with Python 3, Pandoc,
LaTeX, and latexmk:

```sh
make arxiv
python3 scripts/test_markdown.py
```

`make` builds the anonymous version. `make preprint-package` creates the source
archive. The pinned ACL template is downloaded on the first build.

Tables are in `layout/`; figures are in `figures/`. Captions are editable in Markdown.
To refresh editor previews, install `requirements-manuscript.txt` and run:

```sh
python3 scripts/build_markdown.py --previews
```

Preview SVGs do not affect the paper PDF. Preserve labels, citation keys, and
reference anchors; register new sections or assets in `manuscript.json`.

Markdown filenames follow reading order (`01.abstract.md`, `02.introduction.md`,
and so on). Their prefixes do not set the published section numbers.

Publication-only instructions and heading labels live in `manuscript.json`.
Its checked layout boundaries restore the original TeX formatting during compilation.
Ordinary Markdown links open reading targets; the `references` mapping restores
dynamic LaTeX references. Keep this mapping current when moving a target.

Figure colors use Paul Tol’s original palettes (Dense: orange; Sparse: blue).
Edit draw.io or plotting sources, export draw.io SVGs with `--theme auto --transparent`, then refresh
previews (native SVGs are copied unchanged). Publication PDFs use `--theme light`. The fixed-L diagnostic export was recolored without changing its values:
some raw inputs are unavailable locally; `figures/results/recolor_fixed_top_l_export.py`
at the repository root preserves the existing PDF labels and geometry.
