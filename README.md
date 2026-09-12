# DESA: Dense Expansion and Sparse Anchoring

Code and experiment results for **Dense Expands, Sparse Anchors**.
DESA constructs separate dense and sparse queries for hybrid retrieval.

## Quick start

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
make setup
make tiny
make test
```

The synthetic example requires no external datasets or models.

## Reproduce

```sh
make tables
```

This rebuilds and verifies 13 result tables from the included per-query draw means.
Outputs go to `tmp/reproduced-tables/`.
See [the reproduction guide](docs/reproduce.md) for generation, retrieval,
evaluation, and supplementary analyses. Full runs require model and dataset downloads.

- [Results](report/REPORT.md) and [per-query records](report/per-query-draw-mean.csv).
- [Protocol](docs/protocol.md) and [baseline settings](docs/baselines/).
- [Paper source](paper/acl2027/README.md).

See [LICENSE](LICENSE) and [CITATION.cff](CITATION.cff).
