# Appendix, Terminology, and Citation Specification Review

## Outcome

The requested scope is complete. Appendix floats were reorganized to remove
the nearly empty final column/page, terminology was locked against recent
ACL-family retrieval and query-expansion papers, and citations and references
were audited for both evidential fit and LaTeX closure.

## Specification checks

- Appendix: anonymous and public builds are 13 pages. Pages 12--13 were
  rendered after the final float change; no table is clipped, no text overflows,
  and no page contains an empty body column followed by a displaced float.
- Readability: the final table uses footnote size rather than a scaled bitmap or
  illegibly small text. The redundant fixed-cutoff macro table was removed;
  its query-level diagnostic evidence remains in the main figure and appendix
  diagnostic panel.
- Terminology: DESA uses *generated/complementary reference passages*;
  source-specific terms such as *hypothetical document*, *pseudo-document*, and
  *pseudo-reference* remain attached to their original methods. *Retrieval
  effectiveness*, *access depth*, and *replay stopping depth* are used for
  distinct concepts. RAG is not used as a synonym for retrieval.
- Citations: all 27 cited keys exist and all 27 bibliography entries are used.
  Citation-bearing claims were checked against official ACL Anthology records
  for HyDE, Query2doc, MuGI, Word2Passage, Exp4Fuse, MoR, and QuDAR.
- Cross-references: no missing or duplicate labels; no unresolved citation or
  reference markers in either PDF.
- Scope: no rejected candidate figure was inserted and no new experiment was
  introduced. Numerical corrections use the frozen query-level reports and
  ranking stores; they align percentage aggregation and available-entry counts
  with the stated definitions.

## Build checks

- `git diff --check`: passed.
- `make all` and `make arxiv`: passed.
- Final log scan: no overfull boxes, undefined citations/references, duplicate
  destinations, LaTeX warnings, package warnings, or pdfTeX warnings.
- All PDF fonts are embedded and subset.
- The review build retains the anonymous ACL author block; the public build
  contains the public author block. The review PDF contains no author email or
  affiliation. A cited paper by the author remains normally listed in the
  references.
- The arXiv source archive builds in a fresh temporary directory to 13 pages;
  its extracted text is byte-identical to the project public build.

## Independent review closure

- Round 1 used three independent, read-only reviewers for claims/numbers,
  terminology/citations, and LaTeX/layout/package checks.
- Round 2 repeated those same scopes after the fixes. It found one remaining
  percentage-aggregation mismatch, one nonsignificance wording issue, three
  bibliography case-protection errors, and three baseline-label mismatches;
  all were corrected before the final build.
- The only recorded nonblocking preflight item is one embedded, subsetted Type
  3 ZapfDingbats symbol in the Draw.io overview. The two Matplotlib figures now
  use embedded CID TrueType fonts.
