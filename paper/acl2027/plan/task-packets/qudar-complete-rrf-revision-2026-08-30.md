# Task Packet: Complete-list QuDAR comparison

- Scope: replace the procedural Top-1000 entry-count comparison with a matched
  complete-list RRF comparison whose four-channel target is certified by the
  same bound-based replay principle used for DESA.
- Status: complete.
- Classification: post-held-out supplemental control. It is not a prespecified
  primary or confirmatory comparison.
- Files allowed to edit: QuDAR reporting and replay code, derived QuDAR reports,
  Experiments, Results, Appendix, Limitations, and planning records.
- Evidence inputs: frozen OS, OD, ES, and ED rankings; frozen DESA records; the
  official QuDAR implementation at commit
  `0702721e82799d0489850d3f94ac787da43436ad`.
- Main control: complete-list uniform RRF over OS, OD, ES, and ED with matched
  generated references and RRF constant 60.
- Diagnostic control: confidence-weighted complete-list RRF. Its weights are
  estimated from Top-1000 normalized score margins, so it remains a mechanism
  diagnostic rather than the clean main comparison.
- Required outputs: regenerated quality aggregates and paired tests;
  four-channel replay depths; stratified bootstrap interval and paired
  randomization test for total-depth reduction; revised manuscript text.
- Claim boundary: logical certification depth only, not latency, index work,
  or end-to-end compute. Nonsignificant quality differences are reported as
  statistically unresolved, not equivalent.
- Validation: tests and lint for changed evaluation code; numerical checks
  against query-level records; anonymous and public LaTeX builds; PDF layout
  inspection; `git diff --check`.

## Completion record

- Stable-summation quality regeneration preserved the reported complete-list
  values.
- DESA versus complete uniform QuDAR: nDCG effect `-0.001318` (Holm
  `p=.4393`), Recall effect `-0.001740` (Holm `p=.2140`).
- Total certification depth: 1402.1 for DESA and 5478.4 for uniform QuDAR;
  reduction 74.41%, bootstrap 95% CI 67.27--80.89, Holm `p=.0002`.
- Margin-confidence versus uniform score fusion: nDCG effect `-0.000657`
  (Holm `p=.1182`) and Recall effect `+0.000214` (Holm `p=.5826`); 92.14%
  and 99.04% of pooled query--draw metric outcomes are unchanged.
- Diagnostic complete-list RRF transfer: nDCG effect `-0.001173` (Holm
  `p=.0104`) and Recall effect `-0.000432` (Holm `p=.4312`). The manuscript
  explicitly limits this finding to margin-based weighting in the matched
  setting.
- Verification: Ruff passed; targeted evidence/statistics/replay tests passed;
  anonymous and public PDFs build to 12 pages; no overfull boxes, undefined
  references, or LaTeX errors; the final appendix page was rendered and
  visually inspected; `git diff --check` passed.
