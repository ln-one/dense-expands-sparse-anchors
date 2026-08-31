# Experiments and Results revision: specification review

## Verdict

Pass.

## Checks

- The complete-list target, replay rule, fixed-cutoff diagnostic, datasets,
  generators, retrievers, baselines, controls, robustness axes, and statistical
  procedure remain present.
- All primary values and corrected significance statements are unchanged.
- The Shared comparison still claims an nDCG advantage but no Recall or depth
  advantage.
- The QuDAR comparison remains supplemental. Its effectiveness difference is
  unresolved, and its depth result is explicitly limited to logical access.
- The negative Contriever/Touch\'e-2020 depth result remains visible.
- No citation, experiment, or causal claim was added.

## Boundary retained

Certification depth is not runtime, latency, or physical index work. Matched
operator controls do not establish either operator implementation as uniquely
optimal.
