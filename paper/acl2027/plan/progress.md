# Writing progress

## Current stage

Stage S5: public-preprint manuscript verified after the post-held-out complete-list QuDAR revision. The public
preprint is the immediate release target; the anonymous ACL review build is
maintained from the same source but is not the current submission priority.

The Chinese Results chapter has been approved by the author and written back.
The English Results chapter has been rebuilt from that approved argument and
is ready for paragraph-level author review. The approved Chinese Conclusion
has been translated, reviewed, and added to the ACL draft. The abstract now
includes the frozen primary findings and observed access boundary.
The title and method name are locked as `Dense Expands, Sparse Anchors:
Coordinated Query Expansion` and DESA (Dense Expansion and Sparse Anchoring).
The manuscript now has a shared-source public arXiv build with the author's
name, affiliation, location, and contact email; the ACL build remains anonymous.

The complete-list QuDAR quality results were regenerated with stable summation;
four-channel certification depths now have paired uncertainty; and Experiments,
Results, Conclusion, Appendix, and Limitations are synchronized to this
supplemental comparison.

Sections 4 and 5 have also received a holistic compression pass. The experiment
protocol now introduces each comparison once, and the Results section answers
the cutoff, primary, mechanism, external-comparison, and robustness questions
without repeating table contents or claim boundaries.

## Status

- [x] Core terminology provisionally locked.
- [x] ACL review-format project initialized.
- [x] Introduction paragraph 1 translated and cited.
- [x] Introduction paragraph 1 approved by the author.
- [x] Introduction paragraphs 2--4 translated, reviewed, and cited.
- [x] Introduction closing paragraph translated and approved by the author.
- [x] Related Work Section 2.1 translated, reviewed, and cited.
- [x] Related Work Section 2.2 translated, reviewed, and cited.
- [x] Related Work Section 2.3 translated, reviewed, and cited.
- [x] Method Section 3.1 translated and reviewed.
- [x] Method Section 3.2 translated and reviewed.
- [x] Method Section 3.3.1 translated and reviewed.
- [x] Method Section 3.3.2 translated and reviewed.
- [x] Method Section 3.4 translated and reviewed.
- [x] Experiments opening and Section 4.1 translated and reviewed.
- [x] Experiments Section 4.2 translated and reviewed.
- [x] Experiments Section 4.3 translated and reviewed.
- [x] Experiments Section 4.4 translated and reviewed.
- [x] Experiments Section 4.5 translated and reviewed.
- [x] Reproducibility material checked against the frozen protocol and
  implementation, translated, and organized into Appendices A--C: generation
  and baselines, operator properties and diagnostics, and retrieval and access
  analysis.
- [x] Abstract problem statement, method summary, primary findings, and access
  boundary reviewed and added.
- [x] Results Section 5.1: fixed Top-$L$ sensitivity drafted from frozen data.
- [x] Results Section 5.2: primary quality and access findings drafted.
- [x] Results Section 5.3: mechanism analysis drafted.
- [x] Results Section 5.4: complete-method comparison drafted.
- [x] Results Section 5.5: robustness and failure boundary drafted.
- [x] Chinese Results chapter created for paragraph-level author review.
- [x] Chinese Results chapter approved by the author.
- [x] English Results chapter rebuilt from the approved Chinese text.
- [x] English Results terminology and internal-consistency self-review completed.
- [x] Chinese Conclusion drafted from the approved findings.
- [x] Chinese Conclusion approved by the author.
- [x] English Conclusion written from the approved Chinese text.
- [x] Seven datasets established as the default scope for controlled, mechanism,
  and cutoff analyses; four-dataset results are labeled as common subsets.
- [x] Anonymous ACL build switched to `review` mode without changing the public
  arXiv build from `preprint` mode.
- [x] Dedicated Limitations section added to both builds.
- [x] Seven-dataset mechanism percentages reconciled with the frozen reporting
  CSVs in the English and Chinese Results sources.
- [x] Dataset, metric, fusion, retriever, encoder, toolkit, and generator
  citations added from primary sources.
- [x] Both public and anonymous PDFs rebuilt and checked for resolved citations,
  identity separation, and layout.
- [x] Dense and Sparse channel operators formalized with concise main-text
  properties and appendix derivations: bounded Dense drift, exact Sparse
  support preservation, rank consistency, and scale invariance.
- [x] Seven-dataset post-hoc mechanism diagnostics completed from frozen
  generations and rankings: realized Dense angles, Sparse turnover and support,
  relevant-document rank movement, within-dataset bins, and descriptive
  correlations.
- [x] Mechanism diagnostics written back into the shared manuscript source.
  The realized-operator distribution is in the main Results section; the
  nonmonotonic quartile analysis and Touch\'e-2020 support-export audit are in
  the appendix. Both anonymous and public-author builds include the figures.

## Capability-use audit

- Skills: research-writing workflow, paper orchestration, evidence-driven
  writing, literature review, LaTeX output, and completion verification.
- Evidence: frozen seven-dataset reporting CSVs; primary proceedings, journal,
  arXiv, and OpenReview records enumerated in `plan/evidence-map.md`.
- Artifacts: separate public and anonymous build entry points, a dedicated
  Limitations section, an expanded `references.bib`, and submission-correctness
  records under `plan/`.
- Scope audit: the manuscript uses seven datasets by default. The two remaining
  four-dataset analyses are explicitly the common prior-method subset and the
  sampled Mistral/Contriever robustness subset.
- Numerical audit: mechanism access reductions now match
  `report/access-macro-bootstrap.csv`: Dense only 8.16\%/7.49\%, Sparse only
  28.77\%/27.74\%, and DESA 36.90\%/36.56\% for Dense/Sparse.
- Method-property verification: the Dense bound was checked against normalized
  production embeddings, and dedicated tests cover the $45^\circ$ angle bound,
  Sparse support preservation, and the no-new-evidence ranking case. All nine
  original method tests pass; the mechanism diagnostics add two further passing
  tests for a known Dense angle and Sparse relevant-rank movement.
- Mechanism audit: all 11,327 query--draw rows satisfy the Dense angle bound.
  Sparse support is exact on six datasets; Touch\'e-2020 contains 25 missing
  tail-document occurrences across 23 query--draw cells, while mean support
  retention remains above 99.9998\%. This implementation boundary is retained
  in the mechanism artifacts rather than hidden.
- Build verification: `make arxiv` produced the signed public preprint and
  `make` produced the anonymous line-numbered review PDF. After the mechanism
  write-back, both builds are thirteen pages including references and appendix;
  the paper body ends before the ACL long-paper limit. The Results and appendix
  figure pages were rendered and inspected.
- Identity verification: the public PDF contains the author's name,
  affiliation, and email; the review title block is anonymous. The review
  bibliography retains ordinary third-person citations, including the related
  preprint.
- Remaining work before public release: decide whether the other planned result
  figures are still needed, perform a final prose/cross-reference pass, and
  package the arXiv source bundle. Further ACL review revisions are deliberately
  deferred until after the preprint release.

### Capability-use audit: mechanism diagnostics write-back

- Required skills: paper orchestration, experiment/results planning, chapter
  writing, core academic writing, English humanization, paper figures, LaTeX,
  PDF inspection, and verification.
- Skills actually used: all required skills above.
- Inputs consumed: frozen per-draw and per-query mechanism CSVs, summary and
  correlation CSVs, figure data files, mechanism manifest, current Experiments,
  Results, Appendix, and approved Chinese Results chapter.
- Inputs not used: no new generations, retrieval runs, citations, or primary
  significance tests were needed because this is a diagnostic write-back.
- Artifacts produced: one main-text PDF figure, one appendix PDF figure,
  revised English and Chinese Results text, revised experiment protocol text,
  an appendix diagnostic table and audit paragraph, and this task packet.
- Verification run: figure regeneration, anonymous and public LaTeX builds,
  visual inspection of Results and Appendix pages, full repository tests,
  linter, artifact-hash verification, identity checks, and `git diff --check`.
- Remaining risk: correlations are descriptive and must not be promoted to
  causal or confirmatory evidence; the Touch\'e-2020 full-ranking export is not
  exactly support preserving in 23 query--draw cells.

### Capability-use audit: ACL-readiness pass, 2026-08-15

- Skills used: research-writing workflow, paper orchestration, peer review,
  evidence-driven writing, LaTeX output, PDF inspection, and verification.
- Evidence used: the frozen seven-dataset reporting CSVs, the current ACL
  manuscript, and the official ACL Anthology record for QuDAR.
- Artifacts produced: direct QuDAR positioning, explicit finite-Sparse-support
  and policy-specific replay semantics, a seven-dataset per-collection table,
  and the complete seven-dataset primary statistical record.
- Scope decision: all seven collections remain one unified primary evaluation;
  no development/held-out split is asserted in the manuscript.
- Verification: anonymous and public PDFs compile to 14 pages with resolved
  citations and cross-references and no overfull boxes. The remaining warnings
  are underfull spacing warnings.
- Remaining evidence risks: no direct QuDAR experimental baseline is yet
  reported, operator-level functional controls remain limited, and the observed
  fixed-cutoff reversals are small in magnitude.

### Capability-use audit: evidence strengthening, 2026-08-16

- Skills used: research-writing workflow, paper orchestration,
  experiment/results planning, LaTeX output, PDF inspection, and completion
  verification.
- Evidence used: frozen seven-dataset complete and fixed-cutoff result records;
  frozen Dense/Sparse ranking stores; the ACL Anthology QuDAR paper; and the
  official QuDAR implementation at commit
  `0702721e82799d0489850d3f94ac787da43436ad`.
- Artifacts produced: query-level fixed-cutoff diagnostics, two matched
  operator-control comparisons, a matched-evidence QuDAR-simple RRF baseline,
  derived JSONL records and hash manifest, concise main-text findings, and
  three appendix tables.
- Scope audit: all new analyses use the same unified seven datasets. No
  development/held-out split was introduced.
- Statistical audit: the operator and QuDAR paired tests average the three
  draws within query, use equal-dataset stratified bootstrap/sign-flip
  inference, and apply Holm correction across nDCG and Recall per comparison.
- Claim audit: fixed-$L$ motivation is now supported by query-level conclusion
  changes; neither operator is claimed independently dominant; paired tests do
  not detect a statistically significant effectiveness difference from
  QuDAR-simple. Accounting for finite sparse lists, the equal-dataset mean
  entry counts imply 64.16% fewer available DESA fusion-side rank entries,
  without claiming lower end-to-end latency.
- Verification: evidence reports were regenerated twice with stable artifact
  hashes; 53 tests passed; Ruff passed for `src`, `scripts`, and `tests`;
  `git diff --check` passed; both anonymous and public LaTeX builds completed
  at 15 pages with no undefined references or overfull boxes. Pages 7--9 and
  13--15 were rendered and visually inspected for legibility and float layout.
- Remaining risk: the direct recent baseline covers QuDAR-simple RRF only.
  QuDAR-confidence needs normalized scores absent from the frozen artifacts,
  and QuDAR-llm would require new relevance judgments.

### Capability-use audit: Related Work revision, 2026-08-16

- Stage: S1 evidence synthesis and S4 chapter revision.
- Required skills: research-writing workflow, paper orchestration,
  evidence-driven writing, literature review, chapter writing, LaTeX output,
  and completion verification.
- Skills actually used: all required skills; subagent delegation was omitted
  because the active workspace instructions prohibit delegation unless the
  user explicitly requests it.
- Inputs consumed: the approved bilingual revision, current Introduction,
  Related Work, Method, project outline, evidence map, evidence-coverage audit,
  QuDAR blueprint, and verified BibTeX records.
- Inputs not used: no new literature search or experimental artifact was needed
  because the revision introduced no new source or empirical claim.
- Artifacts produced: revised `sections/02-related-work.tex`, an expanded
  paragraph blueprint, and the persistent task packet for this revision.
- Verification run: the anonymous ACL build completed at 15 pages; no LaTeX
  errors or unresolved citations/references were reported; Related Work pages
  2--3 were rendered and visually checked; whitespace and scoped Git checks
  passed before commit.
- Remaining risk: the compact section positions the main recent integration
  methods but does not attempt a comprehensive history of classical query
  expansion.

### Capability-use audit: seven-dataset reporting cleanup, 2026-08-16

- Stage: S3 results synchronization and S5 preprint verification.
- Required skills: research-writing workflow, paper orchestration,
  experiment/results planning, LaTeX output, PDF inspection, and verification.
- Skills actually used: research-writing workflow, paper orchestration,
  experiment/results planning, LaTeX output, PDF inspection, and verification.
- Inputs consumed: the immutable pre-evaluation lock, the original frozen
  protocol, seven-dataset controlled and fidelity records, current manuscript,
  and GitHub repository metadata.
- Inputs not used: no new generation, retrieval, relevance judgment, or
  per-query result was created because the change concerns reporting scope and
  provenance rather than experimental evidence.
- Artifacts produced: a versioned post-evaluation seven-dataset reporting
  protocol, seven-dataset fidelity summaries, synchronized English and Chinese
  Results text, a provenance-qualified Figure 1 caption, explicit EAHR replay
  attribution, a repository URL, and an explained mechanism-diagnostic fallback.
- Claim boundary: all seven datasets are reported as one pooled evaluation set;
  the manuscript does not describe that pooled analysis as prespecified,
  preregistered, held-out, or confirmatory. The historical access-control split
  remains intact in the immutable pre-evaluation provenance record.
- Verification run: report regeneration from frozen records, lock verification,
  repository tests and lint, anonymous/public LaTeX builds, PDF text/layout
  checks, scoped numerical recomputation, repository-visibility check, and
  `git diff --check`.
- Remaining risk: the Figure 1 display text remains abridged/paraphrased rather
  than verbatim, but this is now disclosed in its caption. The GitHub URL in the
  manuscript still resolves to a private repository as of the final local
  check, so the author must make it public before completing the arXiv upload.
  AI-use disclosure is intentionally deferred by the author for the arXiv
  preprint and must be reconsidered under the policy of any later conference
  submission.

### Method chapter review, 2026-08-16

- Stage: S2 Method and S4 chapter revision.
- Status: complete bilingual review draft prepared for paragraph-level author
  annotation; no manuscript write-back has been performed.
- Required skills: research-writing workflow, paper orchestration, chapter
  writing, and core academic writing.
- Skills actually used: all required skills; subagent delegation was omitted
  because the active workspace instructions prohibit delegation unless the
  user explicitly requests it.
- Inputs consumed: current Method and operator appendix, frozen implementation
  and method tests, retrieval and fusion code, generator prompt, project
  overview, outline, and chapter architecture.
- Artifact produced: `plan/task-packets/method-chapter-review-2026-08-16.md`
  and the bilingual review draft presented to the author.
- Verification run: input-to-output trace checked against the implementation;
  LaTeX and rendered-page verification remain pending author-approved
  write-back.
- Remaining risk: the access depths are policy-specific certificates rather
  than minimal depth or end-to-end latency, and this boundary must remain in
  the final text.

### Capability-use audit: Method revision write-back, 2026-08-16

- Stage: S2 Method, S4 chapter revision, and S5 verification.
- Required skills: research-writing workflow, paper orchestration, chapter
  writing, core academic writing, LaTeX output, PDF inspection, and completion
  verification.
- Skills actually used: all required skills; no subagent was used because this
  was a single author-approved chapter revision rather than a full-paper
  redraft.
- Inputs consumed: the approved bilingual Method draft, current DESA figure,
  implementation trace, method tests, project overview, outline, and task
  packet.
- Artifact produced: revised `sections/03-method.tex`.
- Verification run: anonymous and public LaTeX builds completed at 15 pages;
  neither log contains unresolved citations, unresolved references, LaTeX
  errors, or overfull boxes. All 11 method tests passed. Pages 2--4 of the
  anonymous build were rendered and checked for equation fit, figure placement,
  column flow, and section transitions. Scoped whitespace and Git checks were
  run before commit.
- Layout follow-up: Figure 2 was restored to the top of the left column on
  page 3. Removing the forced column break keeps the Dense derivation
  continuous and lets the two-column text flow naturally.
- Remaining risk: replay depth remains a policy-specific certificate; its
  interpretation is retained in the experiment protocol and limitations rather
  than repeated defensively in the Method chapter.

### Capability-use audit: Experiments revision write-back, 2026-08-16

- Stage: S3 Experiments, S4 chapter revision, and S5 verification.
- Status: the author-approved Section 4 revision has been written back to the
  manuscript.
- Required skills: research-writing workflow, paper orchestration, experiment
  planning, chapter writing, core academic writing, humanization, LaTeX output,
  and completion verification.
- Skills actually used: all required skills; no subagent was used because the
  workspace instructions prohibit delegation unless the author requests it.
- Inputs consumed: the current Experiments and Results sections, experiment
  protocol, method--experiment traceability record, table schema, fixed-Top-$L$
  diagnostics, baseline configurations, and the author's paragraph-level
  annotations.
- Artifacts produced: revised `sections/04-experiments.tex` with a clearer
  gain/tie/loss cutoff diagnostic, concise baseline descriptions, matched
  operator controls, and a compact statistical protocol.
- Verification run: anonymous and public LaTeX builds completed at 14 pages;
  neither log contains unresolved citations or references, LaTeX errors, or
  overfull boxes. Pages 4--5 were rendered and visually checked for column
  flow, spacing, and the transition into Results. Scoped whitespace checks
  passed.
- Remaining risk: Section 5.1 still uses the older phrase "changes the sign of
  the paired conclusion." It should be aligned with the clearer gain/tie/loss
  terminology when the Results section is revised.

### Results chapter review draft, 2026-08-16

- Stage: S3 Results and S4 chapter revision.
- Status: a complete bilingual review draft has been prepared for author
  annotation; `sections/05-results.tex` has not yet been changed.
- Required skills: research-writing workflow, paper orchestration, experiment
  results planning, chapter writing, core academic writing, humanization,
  LaTeX output, and verification.
- Skills actually used: all required skills; no subagent was used because the
  workspace instructions prohibit delegation unless the author requests it.
- Inputs consumed: the frozen fixed-cutoff diagnostics, main and bootstrap
  results, paired tests, access-change summaries, operator controls, mechanism
  diagnostics, reference-count study, prior-method comparison, QuDAR results,
  robustness matrix, scale results, chapter outline, traceability matrix, and
  the existing Results text.
- Artifact produced: a bilingual Section 5 revision for paragraph-level author
  review. No manuscript write-back has been performed.
- Verification run: all numerical statements in the proposed revision were
  recalculated or checked against the frozen CSV artifacts. In particular,
  gain/tie/loss changes and strict reversals were checked separately, and the
  access-reduction aggregation was distinguished from ratios of raw macro
  depths.
- Remaining risk: Table 2 should state that raw depths are macro means whereas
  the reported 36.90\% and 36.56\% reductions average within-dataset percentage
  changes. The final write-back must preserve the nonsignificant Recall and
  depth comparisons against Shared expansion and the Contriever failure on
  Touch\'e-2020.
- Author-review update: the second bilingual draft removes defensive phrasing,
  centers the joint effect of the two channel operators, and moves binary-mask,
  reference-count, detailed generator, encoder, and corpus-scale results to the
  appendix. The main text retains one concise robustness paragraph and the
  Contriever failure boundary.

### Results figure claim alignment and layout revision, 2026-08-16

- Replaced the cutoff trend plot with a single-column judgment-transition
  matrix at $L=50$. Its diagonal shows preserved gain/tie/loss judgments,
  off-diagonal cells show changed judgments, and the two highlighted corner
  cells show strict gain--loss reversals.
- Rewrote Section 5.1 so the figure answers one explicit question---whether a
  fixed cutoff changes the query-level gain/tie/loss judgment---and moved the
  complete macro curves and Top-20 agreement details to the appendix.
- Removed the quality--access scatter plot from the manuscript because it
  repeated the effectiveness and access-depth comparison already reported in
  Table 1.
- Kept Figure 3 and the main results table in source order within the column;
  the final layout places the figure after its evidence paragraph and Table 1
  after the Section 5.2 result statement.
- Regenerated the PDF/SVG/PNG figure, rebuilt the anonymous paper at 14 pages,
  and visually checked pages 5--7 for column flow, legibility, and float order.

### Capability-use audit: figure/table literature audit, 2026-08-16

- Stage: S3 experiment/result design and S5 evidence review.
- Required skills: research-writing workflow, paper orchestration, experiment
  results planning, PDF inspection, and peer review.
- Skills actually used: all required skills. No subagent was used because the
  workspace instructions prohibit delegation unless the author requests it.
- Inputs consumed: official ACL Anthology PDFs for QuDAR, Weller et al., MuGI,
  and Exp4Fuse; the current 14-page manuscript rendering; figure/table source
  references; evidence and traceability plans; and frozen result CSVs.
- Inputs not used and why: no additional RAG papers were added after the four
  references covered adaptive fusion, expansion failure analysis, integration
  ablations, and fusion-framework presentation without adding a new visual
  design pattern.
- Artifacts produced:
  `plan/task-packets/figure-table-literature-audit-2026-08-16.md` and
  `plan/review/figure-table-literature-audit-2026-08-16.md`.
- Verification run: official PDFs were rendered and inspected; all current
  figure/table references were enumerated; the proposed cross-dataset pattern
  was recomputed from `report/main-results.csv`. DESA exactly preserves the
  Original Sparse support on six datasets and retains 99.9999\% on
  Touch\'e-2020, while Shared expansion ranges from 1.003 to 5.72 times the
  Original support; DESA exceeds Shared nDCG on six of seven datasets.
- Remaining risk: a support-size figure must not be described as a latency
  result or as universal Sparse-depth improvement over Shared expansion.

### Double-column channel-evidence table, 2026-08-16

- Stage: S3 Results and S5 evidence presentation.
- Replaced the rejected quality--access Figure 4 with a full-width evidence
  table that reports the per-dataset pattern behind the channel-asymmetry
  claim rather than repeating the macro comparison in Table 1.
- The table groups three kinds of evidence: relative nDCG changes that isolate
  the contribution of each operator, Dense/Sparse replay-depth reductions
  relative to Original, and Sparse-support ratios for Shared expansion and
  DESA. Pastel group headers and restrained cell colors follow the compact ACL
  table style used in the reference papers; the sole negative operator effect
  is marked in red.
- The summary row states the auditable pattern directly: DESA improves over
  Original on 7/7 datasets; adding Sparse anchoring to Dense expansion helps on
  7/7; adding Dense residual expansion to Sparse anchoring helps on 6/7; and
  both replay depths decrease on 7/7 under the primary BGE setting.
- Updated `figures/data-manifest.md` and `tables/table-schema.md`; moved the
  earlier mechanism boxplot to appendix status and removed the rejected,
  unreferenced Figure 4 assets from the formal figure directories. Prototype
  artifacts remain under `tmp/` for comparison.
- Verification run: both anonymous and arXiv builds complete at 14 pages; the
  final LaTeX logs contain no errors, undefined references, or overfull boxes.
  Pages 6--8 were rendered and visually inspected for table width, text
  overflow, float order, and column balance.
- Layout follow-up: moved the unchanged two-column table declaration to the
  beginning of Section 5.3 and strengthened its top-float preference. It now
  appears at the top of page 7, immediately after its discussion and first
  reference on page 6, rather than being delayed to page 8.
- Remaining risk: replay depth remains a logical access measure, not end-to-end
  latency, and the Contriever/Touch\'e-2020 access failure remains stated
  separately in the robustness discussion.

### Conclusion review candidate, 2026-08-16

- Stage: S4 drafting and S5 consistency review.
- Prepared a read-only Section 6 review and replacement candidate; the
  manuscript conclusion has not been changed pending author confirmation.
- The candidate reduces abstract-level repetition and adds the two Results
  findings needed for closure: the distinct roles of Sparse anchoring and Dense
  residual expansion, and the matched QuDAR-simple quality/access comparison.
- Required skills: research-writing workflow, paper orchestration, chapter
  writing, and core academic writing. All were used; no subagent was used
  because the author did not request delegation.
- Inputs consumed: project overview, outline, abstract, Introduction, Results,
  current Conclusion, and Limitations. No new literature was required because
  the conclusion introduces no new external claim.
- Artifacts produced: `plan/task-packets/conclusion-review-2026-08-16.md` and
  `plan/review/conclusion-review-2026-08-16.md`.
- Verification run: every number and qualifier in the candidate was checked
  against the current Results and Limitations sections.
- Remaining risk: the QuDAR sentence must remain explicitly limited to the
  reconstructable QuDAR-simple RRF comparison, and replay depth must not be
  presented as wall-clock latency.

- Author annotation follow-up: the first candidate was rejected as weakly
  narrated and too defensive. A second candidate now opens with the empirical
  channel-asymmetry finding, treats complete-list replay as supporting method
  rather than the main story, and ends on the Dense-expands/Sparse-anchors
  design principle. Failure and deployment qualifications are left to the
  adjacent Limitations section instead of dominating the conclusion.
- Closing-line follow-up: revised the candidate to end explicitly with the
  paper's title-level formulation, `Dense expands; Sparse anchors.`
- Full-section follow-up: the author found the standalone slogan abrupt and
  requested the complete Section 6 with Chinese translation. The new
  three-paragraph candidate derives the slogan from a final implication
  paragraph and records aligned English and Chinese versions in the review
  artifact; the manuscript remains unchanged pending confirmation.
- Author approval: the three-paragraph Conclusion was written back to
  `sections/06-conclusion.tex`. It now closes on a derived division-of-labor
  statement, `Dense expands, while Sparse anchors`, while detailed failure and
  deployment boundaries remain in the following Limitations section.

### Limitations compression candidate, 2026-08-16

- Stage: S6 author-approved writeback and verification.
- The current 274-word section is over-defensive. The proposed replacement
  retains only three claim boundaries: empirical scope, the distinction
  between replay depth and wall-clock latency, and generated-evidence/qrel
  uncertainty. QuDAR- and MuGI-specific reproduction details remain where they
  are already documented in Results, Experiments, and the appendix.
- Author approval: the two-paragraph candidate was written back to
  `sections/07-limitations.tex` for final LaTeX and layout verification.
- Verification: the section is 100 words (down from 274); both review and
  arXiv builds compile to 14 pages with no LaTeX errors, undefined references,
  or overfull boxes. Page 8 was rendered and visually checked: the unnumbered
  heading, two paragraphs, and adjacent References column fit cleanly.

### Figure candidate pool, 2026-08-16

- Stage: S3 Results presentation and S5 figure review.
- The preceding manuscript revision was committed as `a0af544` before this
  exploratory work began. No candidate figure has been inserted into the
  manuscript.
- Literature design inputs: QuDAR's question--setting--observation figure
  logic; Weller et al.'s cross-dataset relationship and failure-distribution
  plots; Query2doc's scale-response figure; and MuGI's reference-count
  sensitivity framing.
- Required skills: research-writing workflow, paper orchestration,
  experiment-results planning, publication figure design, Python plotting,
  and completion verification. All were used; no subagent was used because the
  author did not request delegation.
- Artifacts produced: seven single-column candidates, one double-column
  mechanism-to-outcome candidate, a contact sheet, editable SVG/PDF/PNG
  exports, seven source-data snapshots, a persistent task packet, an argument
  review, and a separate evidence/layout QA review.
- Main-text shortlist: H for a double-column evidence story, B for one
  standalone single-column result, A for channel-role evidence, and C for the
  query-level distribution. D, G, E, and F are appendix or reserve candidates.
- Evidence audit: FiQA's negative Dense only result is retained; all seven
  controlled datasets remain positive in the joint quality--access plot; the
  query-level both-shallower result reconstructs to 63.31%; and the sole
  robustness access failure remains Contriever on Touch\'e-2020.
- Visual audit: every candidate was inspected at its intended width; stray log
  ticks, label collisions, quadrant shading, and the RRF ideal-region cue were
  corrected. All SVG files retain editable text nodes.
- Verification: consecutive regenerations produced identical PNG and data
  hashes; Ruff and Python compilation passed; all expected exports and data
  snapshots exist; claim assertions and `git diff --check` passed.
- Remaining decision: choose one narrative package before any manuscript
  write-back. H replaces A and B rather than accompanying them.
## 2026-08-16 - Appendix organization and preprint readiness

- **Stage**: S5 Review / submission preparation.
- **Status**: In progress.
- **Scope**: Reorder and tighten the appendix, verify the anonymous and public
  builds, and prepare a source package for author-approved preprint upload.
- **Boundary**: The rejected exploratory candidate figures remain outside the
  manuscript; no external submission is authorized in this task.
- **Task packet**:
  `plan/task-packets/appendix-preprint-readiness-2026-08-16.md`.
- **Status**: Complete for local preprint preparation; external upload remains
  author-controlled.
- Reorganized the appendix into reproducibility details, operator diagnostics,
  and additional experimental results. Removed the low-information binned
  mechanism figure, regrouped cutoff and matched-control tables, and tightened
  the robustness summary without changing any reported result.
- Added a reproducible preprint packaging target and arXiv `00README.json`.
  The archive contains only the source, styles, bibliography/BBL, sections, and
  four figures required by the public build.
- Verification: anonymous and public builds both compile to 14 A4 pages; final
  logs contain no undefined citations/references, overfull boxes, duplicate
  destinations, or LaTeX warnings. The archive compiles in a fresh temporary
  directory, and its extracted PDF text is byte-identical to the project public
  build. Appendix pages 9--14 were rendered and visually inspected.
- Required skills: `using-research-writing`, `paper-orchestration`,
  `writing-chapters`, `latex-output`, `peer-review`, `pdf`, and `verification`;
  all were used. No subagent was used because this was one tightly coupled
  appendix/build task.
- Inputs consumed: manuscript sources, bibliography, build files, current PDFs,
  existing planning records, and official arXiv TeX/README guidance. Rejected
  candidate A--H figures were intentionally excluded; no preprint account or
  external form was accessed because upload was not authorized.
- Artifacts: revised appendix, public PDF, source archive and manifest, task
  packet, and `plan/review/appendix-preprint-readiness-2026-08-16.md`.
- Remaining decisions: arXiv category/cross-list, license, comments and journal
  metadata, followed by visual inspection of arXiv's own compiled preview.

## 2026-08-16 - Appendix layout, terminology, and citation audit

- **Stage**: S1 evidence review / S5 submission review.
- **Status**: Complete locally; external upload remains author-controlled.
- **Scope**: Remove avoidable appendix white space, establish a sourced
  ACL-aligned terminology lock, and review terminology and citations across the
  complete manuscript in multiple passes.
- **Task packet**:
  `plan/task-packets/appendix-layout-terminology-citation-audit-2026-08-16.md`.
- Appendix layout: removed float barriers and the redundant fixed-cutoff macro
  table, consolidated the final result blocks, and reduced both builds from 14
  to 13 pages. Final pages 12--13 have no empty body column, clipping, or text
  overflow.
- Terminology: aligned the manuscript with recent ACL-family usage for HyDE,
  Query2doc, MuGI, Word2Passage, Exp4Fuse, MoR, and QuDAR. DESA consistently
  uses generated/complementary reference passages; retrieval effectiveness,
  access depth, and replay stopping depth remain distinct; RAG is reserved for
  systems that include generation.
- Citation audit: 27 cited keys and 27 bibliography entries, with no missing or
  unused entries. DOI metadata was verified through Crossref when publisher
  pages rejected automated access; citation placement and claim support were
  reviewed separately from key closure.
- Verification: anonymous/public builds and an isolated arXiv-package build all
  pass with 13 pages; no overfull boxes, undefined citations/references,
  duplicate labels, LaTeX/package/pdfTeX warnings, unembedded fonts, or PDF
  placeholder markers. The isolated PDF text is identical to the project public
  build.
- Review artifacts:
  `plan/review/appendix-layout-terminology-citation-spec-2026-08-16.md` and
  `plan/review/appendix-layout-terminology-citation-quality-2026-08-16.md`.

## 2026-08-16 - Two-round independent preprint audit

- **Stage**: S5 final verification.
- **Status**: Complete locally; no external upload performed.
- Three independent read-only reviewers separately audited numerical claims,
  terminology/citations, and LaTeX/layout/package behavior. After the first
  fixes, all three repeated their assigned scope.
- Corrected substantive low-level issues included the MuGI repetition formula,
  HyDE category wording, C-Pack publication metadata, mixed access-percentage
  aggregation, finite QuDAR list lengths, reference-count aggregation, and
  overstrong wording for nonsignificant differences.
- Corrected presentation issues included double-float placement, Matplotlib
  font export, three bibliography case protections, undefined QuDAR
  abbreviations, and baseline-label consistency.
- Final anonymous and public PDFs contain 13 A4 pages. Both final logs are free
  of overfull boxes, undefined citations/references, and LaTeX/package/pdfTeX
  warnings. The rebuilt preprint archive compiles in isolation and its extracted
  text matches the project public PDF.
- Residual nonblocking preflight note: the Draw.io overview embeds one subsetted
  Type 3 ZapfDingbats symbol; all other figure and document fonts are embedded,
  and the Matplotlib outputs are CID TrueType.

## 2026-08-17 - Repository-link placement

- **Stage**: S5 final verification.
- **Status**: Implemented locally.
- Removed the public GitHub URL from the shared manuscript body so that neither
  the arXiv PDF nor the anonymous ACL build contains a repository link.
- Retained the complete prompt and baseline reproduction settings in the
  appendix; repository discovery will be handled through external metadata.

## 2026-08-29 - Abstract revision v3

- Rebuilt the abstract as one causal chain: RAG retrieval grounding, fixed
  top-$L$ conditionality, effectiveness--depth separation, coordinated
  dense--sparse construction, DESA, and controlled evidence.
- Replaced the earlier parallel presentation of evaluation and method with the
  joint-design insight that the fused result and both replay stopping depths
  depend on the two rankings together.
- Added the matched Shared nDCG result because it directly supports
  channel-specific integration after shared generation.
- Retained the Original-relative effectiveness/depth results and the matched
  Shared nDCG and sparse-support comparison. The query-level dual-depth rate
  and the encoder--dataset failure remain in Results and Limitations.
- Derived the title phrase from the method's complementary channel roles rather
  than using it as a detached final slogan.

### Capability-use audit

- Required skills: using-research-writing, writing-chapters, nature-writing,
  writing-core, LaTeX output, verification.
- Skills actually used: all required skills.
- Inputs consumed: revised Introduction, Results, Conclusion, argument outline,
  evidence map, terminology ledger, and current abstract.
- Inputs not used and why: no new literature or raw logs were needed because
  the abstract introduces no new claim or result.
- Artifacts produced: revised abstract, task packet, and two-stage review.
- Verification run: strict word count, `git diff --check`, arXiv build, LaTeX
  warning scan, `pdfinfo`, PDF text check, and rendered-page inspection.
- Remaining risk: the RAG opening is application motivation only; the paper
  evaluates retrieval rather than end-to-end generation.

## 2026-08-29 - Title and Introduction closure

- Renamed the paper to *Dense Expands, Sparse Anchors: Coordinated Query
  Expansion* to foreground cross-channel coordination while retaining the
  query-expansion category.
- Removed the matched-Shared sentence from the abstract for a cleaner
  Original-relative result summary.
- Replaced the repeated `Dense expands; Sparse anchors.` slogan in the
  Introduction with a causal closing sentence that presents shared evidence as
  the mechanism for coordinating the two channels.
- Integrated the Figure 1 reference into that closing sentence instead of
  leaving a standalone backward-reference sentence.
- Verification: `make arxiv` succeeds; the generated PDF remains 13 pages.

## 2026-08-29 - Related Work page closure

- Compressed only the closing paragraph of Section 2.3, removing the repeated
  coupled-system formulation while preserving its prior-work boundary and
  DESA contrast.
- Section 2.3 now ends at the bottom of page 2; Section 3 begins cleanly at the
  top of page 3 without manual page-breaking commands.
- Verification: `make arxiv` succeeds, the PDF remains 13 pages, and rendered
  pages 2--3 confirm the intended boundary with no overflow or undefined
  references.

## 2026-08-29 - Evaluation-protocol attribution

- Rephrased the main-text evaluation protocol as a self-contained description
  of complete-list fusion and bound-based replay, with EAHR retained as a
  parenthetical source rather than the grammatical subject.
- Folded the common-protocol control into that sentence with `Across methods`,
  removing the separate `DESA changes only query construction` statement.
- Kept the explicit protocol attribution in the appendix, where provenance and
  reproduction details belong.
- Verification: `make arxiv` succeeds; the PDF remains 13 pages and the
  Section 2/3 page boundary is unchanged.

## 2026-08-29 - Fixed-prefix list typesetting

- Replaced the unbreakable inline set of seven cutoff values with a prose-led,
  line-breakable enumeration.
- This removes the visibly stretched interword spacing in the narrow ACL
  column without changing the evaluated depths or global template settings.
- Verification: `make arxiv` succeeds, the PDF remains 13 pages, and rendered
  page 4 confirms natural paragraph spacing.

## 2026-08-30 - QuDAR confidence-weighting audit

- Added direct confidence-versus-uniform tests for the official-style
  Top-1000 score fusion and the diagnostic complete-list RRF transfer.
- The appendix now reports no measurable score-fusion benefit from the margin
  weights and a significant nDCG decrease under the RRF diagnostic, without
  generalizing to LLM-based weighting or QuDAR overall.
- Persisted the paired tests and query--draw outcome-stability report so every
  appendix number is regenerated from frozen artifacts.
- Verification: changed scripts pass Ruff; 14 targeted tests pass; anonymous
  and public PDFs compile to 12 pages; the final appendix page is visually
  balanced; `git diff --check` passes.
