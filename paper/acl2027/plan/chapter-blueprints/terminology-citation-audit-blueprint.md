# Terminology and Citation Audit Blueprint

## Abstract and Introduction

- Role: define the paper as a retrieval study motivated by RAG, not as an
  end-to-end RAG system.
- Main terminology: LLM-based query expansion; hybrid retrieval; dense and
  sparse retrievers; generated reference passages; retrieval effectiveness;
  replay stopping depth.
- Evidence IDs: T1--T8.
- Required distinction: RAG includes a generation stage; DESA is evaluated at
  the retrieval and fusion stages.
- Forbidden content: calling generated passages `evidence` without a qualifier,
  using `exact-access depth`, or capitalizing dense/sparse as ordinary nouns.

## Related Work

- Role: synthesize LLM-based query expansion, heterogeneous retriever fusion,
  and channel-aware integration.
- Main claim: recent ACL-family work uses source-specific terms such as
  hypothetical document, pseudo-document, and pseudo-reference; retain those
  names only when describing the corresponding source and use generated
  reference passage for DESA.
- Evidence IDs: T1--T8.
- Citation action: retain method-specific citations and add a recent mixture-of-
  retrievers citation only where it directly supports query-wise heterogeneous
  retriever combination.
- Forbidden content: citation stacking without a concrete claim or treating
  query rewriting as a synonym for query expansion.

## Method, Experiments, Results, and Appendix

- Role: use operational terms consistently across definitions, labels,
  captions, and result interpretation.
- Main terminology: dense/sparse retrieval channel after first definition;
  original query; shared expansion; replay stopping depth $(L_D,L_S)$; access
  depth as the reported metric family; complete-list fusion; fixed top-$L$;
  ordered top-$K$.
- Evidence IDs: T7--T8 plus frozen experimental artifacts E29--E31.
- Required label rule: method labels may capitalize `Original`, `Shared`,
  `Dense only`, and `Sparse only`; ordinary prose remains lowercase.
- Forbidden content: `No expansion` as a second name for `Original`, mixing
  access depth with wall-clock latency, or changing numeric results.

## Review passes

1. Source-alignment pass: terminology and citation claims against official ACL
   records/full text.
2. Manuscript-consistency pass: every occurrence, caption, table label, and
   heading against `plan/terminology.md`.
3. Citation-integrity pass: cited keys exist, bibliography entries are used,
   metadata and supported claims match, and LaTeX resolves every citation.
4. Layout and anonymity pass: render every page, inspect floats/white space,
   and verify public/anonymous identities.
