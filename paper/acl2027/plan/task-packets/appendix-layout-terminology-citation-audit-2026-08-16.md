## Task Packet

- Status: Complete locally; no external upload performed.

- Scope: Remove avoidable white space from the appendix and conduct a
  paper-wide terminology and citation audit against recent ACL-family work on
  RAG, hybrid retrieval, and LLM-based query expansion.
- Stage: S1 evidence review plus S5 submission review.
- Files to read: `main.tex`, all `sections/*.tex`, `references.bib`,
  `plan/terminology.md`, `plan/evidence-map.md`, the current anonymous/public
  PDFs, and official ACL Anthology pages or PDFs used for terminology evidence.
- Files allowed to edit: manuscript `.tex` sources, `references.bib` only when
  verified metadata or a genuinely missing citation requires it,
  `plan/terminology.md`, `plan/evidence-map.md`, terminology/evidence review
  artifacts, this task packet, and `plan/progress.md`.
- Required skills: `using-research-writing`, `paper-orchestration`,
  `evidence-driven-writing`, `literature-review`, `latex-output`, `pdf`,
  `peer-review`, and `verification`.
- Evidence inputs: official ACL Anthology records and paper text for recent
  LLM-based query-expansion, hybrid-retrieval, and RAG papers; current frozen
  experimental artifacts remain the only source for numeric claims.
- Required artifacts: rendered before/after appendix layout audit; a sourced
  terminology map; evidence coverage and BibTeX consistency checks; revised
  manuscript sources; clean anonymous and public builds; independent
  spec-compliance and quality review records.
- Rejection checks: do not add citations merely to increase count; do not use
  RAG as a synonym for retrieval when no generation stage is evaluated; do not
  silently rename method-specific terms from cited papers; do not change
  experimental claims; do not solve white space by shrinking text or making
  tables unreadable; do not introduce undefined citations/references,
  anonymous-author leakage, or candidate figures.
- Validation commands: ACL-source metadata verification; citation-key and
  unused-reference audit; terminology scans; `make all`; `make arxiv`; final-log
  warning scans; `git diff --check`; Poppler rendering and visual inspection of
  every appendix page; isolated public-source package compilation.
