# Figure candidate pool, 2026-08-16

## Scope

These figures are exploratory candidates only. None is included in the
manuscript. Every value is derived from the frozen reporting CSVs, and every
candidate has PNG, editable-text SVG, and PDF exports under
`figures/candidates/2026-08-16/`.

## What the related papers do well

- [QuDAR](https://aclanthology.org/2026.acl-long.1791/) assigns a narrow
  empirical question to each compact figure and then states the setting,
  observation, and insight in the surrounding text. Its figures justify a
  decision; they do not merely restate a result table.
- [Weller et al.](https://aclanthology.org/2024.findings-eacl.134/) turn a large
  result table into a cross-dataset relationship plot and use a rank-change
  distribution to expose the failure mechanism. This is the strongest model
  for our per-dataset and per-query candidates.
- [Query2doc](https://aclanthology.org/2023.emnlp-main.585/) uses a simple
  performance-versus-data-scale curve only to establish consistency across
  scales. This motivates the corpus-scale candidate, not another generic
  method-comparison chart.
- [MuGI](https://aclanthology.org/2024.findings-emnlp.103/) treats the number of
  generated references as an empirical design question. This motivates a
  compact reference-count response figure, primarily for the appendix.

The common principle is that a table supplies exact values, whereas a figure
should expose a relationship, a distribution, a mechanism, or a boundary.

## Candidate A: channel roles

- File: `candidate_a_channel_roles.*`
- Intended width: single column.
- Claim: generated evidence has different channel-level consequences. Dense
  residual expansion improves nDCG on six of seven datasets, while DESA keeps
  Sparse support at approximately `1x` Original and Shared expansion enlarges
  it by as much as `5.72x`.
- Reading guide: panel a preserves the small negative FiQA Dense-only result;
  panel b contrasts the support-preserving DESA diamonds with Shared squares.
- Value: directly supports the title-level channel asymmetry rather than
  repeating Table 1.
- Limitation: panel a measures effectiveness, not semantic novelty itself. The
  caption must not say that the plot directly measures new semantic content.
- Recommendation: strong single-column main-text candidate.

## Candidate B: joint quality--access outcomes

- File: `candidate_b_joint_outcomes.*`
- Intended width: single column.
- Claim: on every controlled dataset, DESA improves nDCG and reduces mean
  Dense/Sparse access relative to Original.
- Reading guide: each point is one dataset; the upper-right region means higher
  quality and shallower access. The star is the equal-dataset mean.
- Value: follows Weller et al.'s strongest design move by turning per-dataset
  numbers into an immediately visible cross-dataset pattern. Unlike the
  deleted method-level scatter, this plot is not another rendering of Table 1's
  macro rows.
- Limitation: seven positive points establish consistency in the controlled
  setup, not a causal correlation between quality and access.
- Recommendation: strongest standalone main-results candidate.

## Candidate C: query-level depth transitions

- File: `candidate_c_query_depth_transitions.*`
- Intended width: single column.
- Claim: the access result is query-level rather than only an aggregate mean;
  with equal dataset weighting, `63.3%` of queries become shallower in both
  channels.
- Reading guide: each axis is the bounded signed change
  `(DESA - Original) / (DESA + Original)` for one channel. Negative values mean
  shallower access. Hexagon color is the log query count; quadrant percentages
  are equal-dataset means.
- Value: shows the full distribution behind the headline percentage and makes
  the strong coupling of Dense and Sparse stopping depths visible.
- Limitation: the near-diagonal structure partly reflects the fixed replay
  policy. It supports a query-level access statement, not a claim that the two
  retrieval channels are intrinsically correlated.
- Recommendation: good main-text alternative if the paper should emphasize
  query heterogeneity; otherwise an informative appendix figure.

## Candidate D: robustness and failure boundary

- File: `candidate_d_robustness_boundary.*`
- Intended width: single column.
- Claim: quality gains persist across the tested generator and Dense encoder,
  while the access benefit has one visible failure case: Contriever on
  Touch\'e-2020 (`-9.3%` mean access reduction).
- Reading guide: green is favorable and red unfavorable; all values are printed
  in the cells, so the color is a reading aid rather than a replacement for
  numbers.
- Value: high information density and an honest boundary in one compact figure,
  similar to QuDAR's use of small heatmaps for interactions.
- Limitation: the two rows do not use identical query counts for every
  condition. The caption must retain the sampled-subset wording.
- Recommendation: strongest appendix candidate; possible main-text figure if
  robustness becomes a central review concern.

## Candidate E: number of generated references

- File: `candidate_e_reference_count.*`
- Intended width: single column.
- Claim: increasing the reference count improves quality and reduces stopping
  depth, with most of the movement occurring from one to three references and
  smaller gains from three to five.
- Reading guide: the left panel shows equal-dataset macro effectiveness; the
  right panel shows raw Dense and Sparse stopping depths.
- Value: directly justifies the chosen reference count and follows the
  sensitivity style used by MuGI.
- Limitation: only three x values are available, so the figure is too sparse to
  carry a main-paper claim by itself.
- Recommendation: appendix-only unless reviewers explicitly question the
  reference count.

## Candidate F: RRF quality--access frontier

- File: `candidate_f_rrf_frontier.*`
- Intended width: single column.
- Claim: the RRF constant changes the balance between retrieval quality and
  replay access; the default `k=60` lies between the quality-oriented `k=20`
  and access-oriented `k=100` settings.
- Reading guide: upper left is preferable, but no tested setting dominates all
  others. Dashed segments connect the tested constants.
- Value: makes a real policy trade-off visible and is distinct from comparing
  methods at a single fixed policy.
- Limitation: this is a sensitivity analysis of the fusion policy, not evidence
  for the DESA mechanism.
- Recommendation: appendix-only.

## Candidate G: nested corpus scale

- File: `candidate_g_scale_response.*`
- Intended width: single column.
- Claim: DESA retains positive effectiveness gains and substantial access
  reductions across all four nested TREC-COVID corpus sizes, but the trend is
  non-monotonic.
- Reading guide: both panels use the same four snapshots; the left reports
  relative quality gains and the right reports per-channel depth reductions.
- Value: a compact answer to the corpus-scale question, following Query2doc's
  scale-response design.
- Limitation: this is one dataset with nested corpora, not evidence of a general
  scaling law.
- Recommendation: appendix-only.

## Candidate H: double-column evidence story

- File: `candidate_h_double_column_story.*`
- Intended width: double column.
- Claim: Dense residual expansion contributes effectiveness, Sparse anchoring
  controls lexical support, and their combination improves both quality and
  access on all seven controlled datasets.
- Reading guide: panels a and b establish the two channel roles; panel c shows
  the resulting full-method outcome.
- Value: the highest information density and the clearest progression back to
  the paper's central message. It replaces, rather than accompanies, candidates
  A and B.
- Limitation: panels a and b are mechanism-level diagnostics whereas panel c is
  the full method. The caption must describe this as a narrative progression,
  not an additive numerical decomposition.
- Recommendation: strongest double-column main-text candidate if the page
  budget permits.

## Recommended shortlists

### Conservative single-column revision

1. Add B to the main Results section.
2. Add D to the appendix.
3. Keep A, C, E, F, and G as reserve material.

This adds one nonredundant main figure and one compact robustness figure.

### Mechanism-forward revision

1. Add A and C as separate single-column figures near their corresponding
   paragraphs.
2. Add D to the appendix.

This resembles QuDAR's embedded figure rhythm, but costs more vertical space.

### One double-column results figure

1. Add H to the main Results section.
2. Add D and optionally G to the appendix.
3. Do not also add A or B.

This is the strongest visual story, but it should be used only if the
double-column float can sit immediately before the channel-operator results.

## Current ranking

1. H, if a double-column result figure is acceptable.
2. B, if only one single-column main figure is added.
3. A, if the title-level channel asymmetry needs more direct visual support.
4. C, if query-level heterogeneity is central to the narrative.
5. D, strongest appendix figure.
6. G, useful scale robustness.
7. E, useful parameter justification.
8. F, informative but least central to the method claim.

The contact sheet is `candidate_contact_sheet.*`. No candidate should be
inserted until the author chooses a narrative role and a float width.
