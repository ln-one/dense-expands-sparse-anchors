## Task Packet

- Scope: Reorganize the ACL appendix and prepare a verified public-author
  preprint build without changing experimental claims or adding exploratory
  candidate figures.
- Files to read: `main.tex`, `main-arxiv.tex`, `sections/04-experiments.tex`,
  `sections/05-results.tex`, `sections/07-limitations.tex`,
  `sections/a-appendix.tex`, `references.bib`, `Makefile`, and the current
  planning/review records.
- Files allowed to edit: `sections/a-appendix.tex`, `main.tex` when float
  control is required, preprint packaging/build files when required,
  `plan/progress.md`, and review records created for this task.
- Required skills: `using-research-writing`, `paper-orchestration`,
  `writing-chapters`, `latex-output`, `peer-review`, `pdf`, and `verification`.
- Evidence/data inputs: manuscript tables and claims already traceable to the
  frozen formal-run artifacts. No new experimental values are permitted.
- Required artifacts: logically ordered appendix, clean anonymous and public
  LaTeX builds, rendered appendix QA, cross-reference/citation audit, and an
  upload-oriented source manifest or package if the build is clean.
- Rejection checks: no candidate A--H figure enters the manuscript; no claim
  or numeric result changes without a frozen source; no unresolved LaTeX
  references/citations; no clipped or unreadable appendix tables; no anonymous
  author state in the public build; no external upload without explicit author
  confirmation.
- Validation commands: `make all`, `make arxiv`, log scans for undefined
  references/citations and overfull boxes, `pdftotext` checks, Poppler page
  rendering, `git diff --check`, and source-package compilation in an isolated
  temporary directory.
