# Experiments and Results holistic revision

## Scope

Revise Sections 4 and 5 as one argument. Preserve the experimental protocol,
all reported values, statistical boundaries, citations, tables, figures, and
appendix pointers. Do not introduce new claims or rerun experiments.

## Reader path

1. Section 4 states the questions and defines one matched protocol for each.
2. Section 5 answers those questions in the same order.
3. The primary result is separated from mechanism evidence, external controls,
   and robustness boundaries.

## Revision rules

- Remove repeated setup and repeated interpretations.
- Keep one controlling claim per paragraph.
- Prefer explicit subjects and short transitions over abstract summaries.
- Keep complete-list effectiveness and certification depth distinct but linked.
- Describe QuDAR as a matched four-ranking control; do not imply equivalence,
  runtime gains, or physical-work savings.
- Preserve the negative Contriever/Touch\'e-2020 access result.
- Keep terminology fixed: complete-list fusion, certification depth, replay
  stopping depth, shared expansion, channel-specific integration, and DESA.

## Verification

- [x] Every numerical claim remains unchanged and traceable to the existing tables.
- [x] Section 4 and Section 5 subsection order remains aligned.
- [x] No new citation or empirical claim is introduced.
- [x] Anonymous and public PDFs compile without unresolved references.
- [x] Results pages are rendered and visually inspected.
- [x] Scoped diff and whitespace checks pass.

## Status

Complete.
