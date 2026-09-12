# DESA manuscript

The LaTeX source is `main.tex` and `sections/`. Build with LaTeX and latexmk:

```sh
make arxiv
```

`make` builds the anonymous version. `make preprint-package` creates the source
archive. The pinned ACL template is downloaded on the first build.

Figures are in `figures/`; references are in `references.bib`.
