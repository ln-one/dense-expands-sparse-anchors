ACL_STYLE_REPOSITORY := https://github.com/acl-org/acl-style-files.git
.DEFAULT_GOAL := all
ACL_STYLE_COMMIT := d5adc823ff0f80f98c80405ca0ab66c68e684409
ACL_STYLE_DIR := .cache/acl-style-files

PREPRINT_DIR := output/preprint/arxiv-source
PREPRINT_ARCHIVE := output/preprint/desa-arxiv-source.tar.gz
PREPRINT_PDF := output/pdf/dense-expands-sparse-anchors-preprint.pdf
PREPRINT_FIGURES := \
	figures/fig_desa_intuition.pdf \
	figures/fig_desa_overview.pdf \
	figures/fig_fixed_top_l_diagnostics.pdf \
	figures/fig_mechanism_distributions.pdf

.PHONY: all arxiv preprint-package clean markdown

markdown:
	python3 scripts/build_markdown.py

all: build/main.pdf

arxiv: build/main-arxiv.pdf

preprint-package: build/main-arxiv.pdf
	rm -rf $(PREPRINT_DIR)
	mkdir -p $(PREPRINT_DIR)/sections $(PREPRINT_DIR)/figures $(PREPRINT_DIR)/layout output/pdf
	cp main-arxiv.tex main.tex references.bib build/main-arxiv.bbl $(PREPRINT_DIR)/
	cp $(ACL_STYLE_DIR)/acl.sty $(ACL_STYLE_DIR)/acl_natbib.bst $(PREPRINT_DIR)/
	cp sections/*.tex $(PREPRINT_DIR)/sections/
	cp layout/*.tex $(PREPRINT_DIR)/layout/
	cp $(PREPRINT_FIGURES) $(PREPRINT_DIR)/figures/
	cp preprint/00README.json $(PREPRINT_DIR)/
	cp build/main-arxiv.pdf $(PREPRINT_PDF)
	find $(PREPRINT_DIR) -type f | sort > output/preprint/source-manifest.txt
	tar -czf $(PREPRINT_ARCHIVE) -C $(PREPRINT_DIR) .

$(ACL_STYLE_DIR)/acl.sty:
	mkdir -p .cache
	git clone --quiet $(ACL_STYLE_REPOSITORY) $(ACL_STYLE_DIR)
	git -C $(ACL_STYLE_DIR) checkout --quiet $(ACL_STYLE_COMMIT)

build/main.pdf: markdown main.tex $(wildcard sections/*.tex) $(wildcard figures/*.pdf) references.bib $(ACL_STYLE_DIR)/acl.sty
	mkdir -p build
	TEXINPUTS="$(CURDIR)/$(ACL_STYLE_DIR)//:" \
	BSTINPUTS="$(CURDIR)/$(ACL_STYLE_DIR)//:" \
	BIBINPUTS="$(CURDIR):" \
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex

build/main-arxiv.pdf: markdown main-arxiv.tex main.tex $(wildcard sections/*.tex) $(wildcard figures/*.pdf) references.bib $(ACL_STYLE_DIR)/acl.sty
	mkdir -p build
	TEXINPUTS="$(CURDIR)/$(ACL_STYLE_DIR)//:" \
	BSTINPUTS="$(CURDIR)/$(ACL_STYLE_DIR)//:" \
	BIBINPUTS="$(CURDIR):" \
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main-arxiv.tex

clean:
	rm -rf build
