## Task Packet

- Scope: study figure designs in closely related retrieval papers and generate
  a pool of evidence-backed candidate figures for author selection. Do not add
  any candidate to the manuscript in this task.
- Stage: S3 experiment/results presentation and S5 figure review.
- Files to read: `plan/project-overview.md`, the existing figure audit,
  `figures/data-manifest.md`, the frozen reporting CSVs under `report/`, and the
  current Python figure style helpers.
- Files allowed to edit: this packet, `plan/progress.md`, a dated candidate
  directory under `figures/candidates/`, candidate data snapshots under
  `figures/data/candidates/`, and a dated figure-design review under
  `plan/review/`. Manuscript sections and production figure includes are out of
  scope.
- Required skills: research-writing workflow, paper orchestration,
  experiment-results planning, publication figure design, Python plotting,
  and completion verification.
- Literature inputs: QuDAR for question--setting--observation figure logic;
  Weller et al. for cross-dataset relationship and failure-mechanism plots;
  Query2doc and MuGI for compact sensitivity figures.
- Evidence/data inputs: frozen controlled results, per-query draw-averaged
  records, robustness results, reference-count results, RRF-constant results,
  and scale results under `report/`.
- Required artifacts: at least five visually distinct candidates, each with an
  explicit claim, data source, intended width, reading guide, and rejection
  criterion; PNG/SVG/PDF exports; a contact sheet; and a recommendation that
  separates main-text candidates from appendix-only candidates.
- Figure contracts:
  1. Channel roles: Dense-only effectiveness change plus Sparse support
     preservation across datasets. Core conclusion: the two operators serve
     different retrieval mechanisms.
  2. Joint outcome consistency: per-dataset quality gain against access-depth
     reduction. Core conclusion: DESA usually improves both outcomes rather
     than trading one for the other.
  3. Query-level depth transitions: Dense and Sparse depth ratios for matched
     queries. Core conclusion: the dual-channel access result is a distribution
     over queries, not only a macro mean.
  4. Robustness boundary: compact condition-by-dataset matrix. Core conclusion:
     quality robustness and the observed access failure boundary should be
     visible in the same figure.
  5. Reference-count response: effectiveness and access as the number of
     generated references increases. Core conclusion: most of the benefit is
     obtained by three references, with smaller gains from five.
  6. Fusion-constant frontier: quality against access under RRF constants.
     Core conclusion: the fusion parameter exposes an interpretable
     quality--access frontier.
  7. Corpus-scale response: effectiveness and access changes over nested
     corpus sizes. Core conclusion: benefits persist with scale but are not
     monotonic.
  8. Double-column evidence story: combine channel-specific effects with the
     per-dataset joint outcome. Core conclusion: the mechanism-level division
     of labor leads into the full method's quality--access result.
- Rejection checks: no synthetic values; no duplication of Table 1 at the same
  aggregation level; no causal or threshold claim from descriptive
  correlations; preserve FiQA's Dense-only near-zero negative case and the
  Contriever/Touch\'e-2020 access failure; label logical replay depth as access,
  never latency; keep mixed dataset subsets visibly separated.
- Validation commands: regenerate all candidates from source CSVs; compare
  exported snapshot rows with their sources; inspect rasterized figures at
  intended single- and double-column sizes; run script syntax checks and
  scoped whitespace checks.
