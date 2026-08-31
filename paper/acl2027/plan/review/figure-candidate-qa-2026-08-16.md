# Candidate figure QA, 2026-08-16

## Review 1: evidence and argument

- Candidate A retains the FiQA Dense-only decline (`-0.13%`) rather than
  recoloring or omitting it. DESA's Sparse-support multiplier is at most
  `1.000001` in the exported snapshot, while Shared reaches `5.719x`.
- Candidate B has seven controlled dataset points; every point has positive
  nDCG change and positive mean Dense/Sparse access reduction. The figure is a
  consistency plot, not a correlation claim.
- Candidate C reconstructs the equal-dataset both-shallower proportion as
  `63.31%` from the per-query draw-averaged records. The plotted signed-change
  transform is bounded and handles zero-depth cells; the quadrant assignment
  itself uses the raw stopping depths.
- Candidate D contains exactly one negative access cell, Contriever on
  Touch\'e-2020 (`-9.32%` mean reduction), and retains positive nDCG changes in
  all eight tested condition--dataset cells.
- Candidate E reproduces the monotonic quality increase and depth decrease for
  reference counts 1, 3, and 5. It is a design-sensitivity result, not a scaling
  law.
- Candidate F uses only the four tested RRF constants. The shaded ideal region
  is restricted to high-quality, low-access coordinates and does not label the
  low-quality `k=100` point as preferred.
- Candidate G retains the non-monotonic scale trajectory while keeping all four
  positive quality gains and both positive channel-depth reductions.
- Candidate H reuses the verified A and B snapshots. Its panels must be
  described as a mechanism-to-outcome narrative, not an additive decomposition
  of the full method.

Outcome: all eight candidates pass evidence integrity. No new empirical claim
is introduced beyond the frozen reports.

## Review 2: layout and information density

- A: readable at 3.35 inches; the Sparse panel uses a log axis without stray
  minor tick labels. The long title is acceptable but could be shortened after
  author selection.
- B: dataset labels were manually separated after the first render; the
  equal-dataset star and the `7/7` annotation remain subordinate to the points.
- C: quadrant backgrounds now match the four semantic regions. The axis
  transform requires a caption-level definition, so this is not a
  self-contained drop-in figure.
- D: the annotated heatmap remains legible at one-column width and exposes the
  negative cell without an extra legend or colorbar.
- E: visually clean but comparatively low information density. It should not be
  chosen merely to increase the figure count.
- F: direct labels replaced a redundant colorbar. The resulting single panel
  communicates the policy trade-off with less visual overhead.
- G: the four corpus sizes use categorical spacing to avoid overlapping log-axis
  ticks. The non-monotonic pattern is visible in both panels.
- H: inspected at 7.05 inches. Dataset labels, legends, and panel titles fit;
  the three panels read left to right without depending on a detached legend.
- The contact sheet contains all eight candidates at comparable preview scale.
- All nine SVG exports, including the contact sheet, retain editable text nodes.
  PNG and derived-data hashes are stable across consecutive regenerations.

Rejected figure ideas:

- another method-level quality--access scatter, because Table 1 already carries
  the same macro comparison;
- another fixed-Top-L curve, because the current Figure 3 already carries the
  judgment-change argument;
- promotion of the existing angle/turnover boxplots as a main result, because
  the diagnostics do not yield a monotonic mechanism rule;
- generic grouped bars for Table 1, because they add ink without exposing a new
  relationship.

Outcome: H, B, A, and C pass the main-text relevance screen; D, G, E, and F are
best treated as appendix or reserve figures. No manuscript write-back is
authorized by this review.
