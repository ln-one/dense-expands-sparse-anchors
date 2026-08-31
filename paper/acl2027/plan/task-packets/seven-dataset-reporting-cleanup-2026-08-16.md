# Task Packet: Seven-Dataset Reporting Cleanup

## Scope

Represent all seven BEIR collections as one pooled evaluation set in the public
preprint without retroactively describing the pooled analysis as prespecified.
Synchronize the prior-method comparison, provenance language, Figure 1 caption,
repository availability, and minor numerical/reporting corrections.

## Files to read

- `artifacts/lock/pre-heldout-v1.json`
- `plan/experiment-protocol.md`, `plan/formal-runbook.md`
- `src/hybrid_query_construction/reporting.py`
- `report/all-results.csv`, `report/main-results.csv`
- `paper/acl2027/main.tex`
- `paper/acl2027/sections/01-introduction.tex`
- `paper/acl2027/sections/03-method.tex`
- `paper/acl2027/sections/04-experiments.tex`
- `paper/acl2027/sections/05-results.tex`
- `paper/acl2027/sections/a-appendix.tex`

## Files allowed to edit

- reporting code and post-evaluation reporting records
- the manuscript files listed above
- planning and review records under `paper/acl2027/plan/`

The pre-evaluation lock, frozen rankings, generations, and per-query result
records must not be altered.

## Required skills

- paper orchestration
- experiment/results planning
- LaTeX output
- PDF inspection and verification

## Evidence/data inputs

- frozen seven-dataset controlled and fidelity records
- the immutable pre-evaluation lock and its original protocol
- public GitHub repository visibility and URL

## Required artifacts

1. A seven-dataset pooled prior-method comparison regenerated from frozen data.
2. Manuscript language that calls the comparisons primary, not prespecified or
   confirmatory.
3. A versioned post-evaluation reporting protocol that preserves the historical
   pre-evaluation lock.
4. A Figure 1 caption that discloses abridged/paraphrased display text and the
   draw used for ranks.
5. A public repository link and corrected minor reporting details.
6. Rebuilt anonymous and public-author PDFs plus an arXiv source archive.

## Rejection checks

- Do not rewrite or replace the historical lock to make a later reporting
  choice appear preregistered.
- Do not call the seven-dataset pooled analysis held-out or confirmatory.
- Do not claim that prior baselines are unavailable on datasets for which
  frozen results exist.
- Do not change any generation, ranking, metric, or per-query result artifact.
- Do not add an AI-use acknowledgment to this arXiv version unless the author
  requests it.

## Validation commands

- regenerate the report from frozen records;
- run lock verification and scoped tests;
- rebuild anonymous and public PDFs;
- scan logs for unresolved references and overfull boxes;
- inspect affected PDF pages visually;
- verify the repository URL is publicly accessible;
- run `git diff --check`.
