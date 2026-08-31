# Appendix, Terminology, and Citation Quality Review

## Pass 1: Argument and terminology

The paper now maintains one level of abstraction per term. RAG supplies the
motivation, while the contribution is described as query construction for
hybrid retrieval. Generated passages are not called ground-truth evidence.
Access depth is the metric family; replay stopping depth is the measured
quantity under the fixed certification policy. Method labels remain stable
across prose, equations, figures, and tables.

## Pass 2: Citation quality

The Related Work section distinguishes query expansion from heterogeneous
retriever fusion and channel-aware integration. The added MoR citation supports
the specific query-wise retriever-routing claim rather than serving as citation
padding. Method names and generated-object terms agree with their official ACL
records. No citation was added solely to increase bibliography size.

## Pass 3: Layout and information density

The appendix ends with one consolidated evidence table rather than three small
subsections separated from their floats. Page 12 is a balanced two-column page;
page 13 presents the full per-dataset results and two compact diagnostic panels
at readable size. The final page has ordinary bottom whitespace but no empty
column, orphan heading, or isolated miniature table.

## Pass 4: Mechanical correctness

Both anonymous and public builds pass warning, citation, reference, font, text
marker, and isolated-package checks. The source archive includes exactly the
files needed by the public build. No external upload was performed.

## Independent multi-agent review

Three read-only reviewers audited the manuscript independently in two rounds.
One checked numerical claims against the frozen CSV and ranking artifacts; one
checked terminology, formulas, citations, and bibliography metadata against
the cited sources; and one checked LaTeX floats, visual layout, anonymity, and
the preprint package. Round 1 caught and corrected the MuGI repetition formula,
the HyDE category wording, outdated C-Pack metadata, mixed aggregation of
access percentages, nominal rather than available QuDAR entries, undefined
abbreviations, float-placement parameters, and Type 3 Matplotlib exports.
Round 2 then caught the remaining reference-count aggregation mismatch,
overstrong nonsignificance wording, three BibTeX case-protection errors, and
three inconsistent baseline labels. Each correction was rebuilt and rescanned.

## Residual author decisions

Only submission metadata and the preprint platform's own compiled preview
remain author-controlled. One embedded ZapfDingbats symbol in the editable
Draw.io overview remains a subsetted Type 3 font; it is embedded and does not
violate the current ACL embedding requirement, but is recorded as a low-risk
preflight item. These points do not require manuscript-source changes.
