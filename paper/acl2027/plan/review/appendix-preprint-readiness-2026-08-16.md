# Appendix and Preprint Readiness Review

## Outcome

The appendix is organized into three functional blocks: reproducibility
details, operator properties and diagnostics, and additional experimental
results. The low-information binned-mechanism figure and redundant fixed-cutoff
macro table were removed. Related results are grouped without float barriers,
and the final three result blocks share one readable double-column table. The
public and anonymous papers both compile to 13 pages.

## Specification compliance

- No experimental claim or numeric result was added or changed.
- None of the rejected candidate A--H figures is referenced by the manuscript
  or included in the preprint source archive.
- The public build contains the author name, affiliation, and email; the
  anonymous build retains the ACL anonymous author block and contains no author
  email or affiliation.
- The source archive contains the two entry files, bibliography sources and
  generated BBL, ACL style files, section sources, and exactly the four figures
  referenced by the paper.
- `00README.json` declares `main-arxiv.tex` as the top-level file and PDFLaTeX
  as the compiler.
- No external upload was performed.

## Verification

- `make all` and `make arxiv`: passed; both outputs are 13-page A4 PDFs.
- Final LaTeX-log scan: no undefined citations or references, overfull boxes,
  duplicate destinations, or LaTeX warnings.
- `git diff --check`: passed.
- The source archive was extracted into a fresh temporary directory and built
  with `latexmk -pdf -interaction=nonstopmode -halt-on-error main-arxiv.tex`.
- The isolated build is 13 pages and its `pdftotext` output is byte-identical
  to the project public build.
- The four `\\includegraphics` references exactly match the four packaged
  figure files.
- Appendix pages 9--13 were rendered and visually inspected for clipping,
  overflow, table legibility, and float placement.

## Capability-use audit

- Required skills: `using-research-writing`, `paper-orchestration`,
  `writing-chapters`, `latex-output`, `peer-review`, `pdf`, and `verification`.
- Skills used: all required skills above. No subagent was used because the task
  was a single, tightly coupled appendix and packaging pass.
- Inputs consumed: manuscript entry files, Experiments, Results, Limitations,
  the complete appendix, bibliography, build rules, existing review records,
  the public and anonymous PDFs, and official arXiv TeX/README guidance.
- Inputs intentionally excluded: candidate A--H figures and their data, because
  the author rejected them; no external preprint form or account state was
  accessed because upload was not authorized.
- Artifacts produced: revised appendix, public PDF, isolated-buildable source
  archive, source manifest, task packet, and this review record.

## Remaining author decisions

The manuscript package is technically ready for an arXiv submission preview.
The author still needs to choose the primary category and any cross-list,
license, comments and journal-reference metadata, then inspect arXiv's compiled
preview before confirming submission.
