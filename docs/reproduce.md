# Reproduction

## Released results

```sh
make setup
make tiny
make tables
```

`make tables` rebuilds and verifies 13 tables from `report/per-query-draw-mean.csv`,
including primary effects, confidence intervals, and paired tests. Outputs are
written to `tmp/reproduced-tables/`. This requires no models or ranking stores.
The CSV contains per-query means over generation draws, not individual generations.

The remaining sections describe full generation and retrieval. Full result JSONs,
model weights, and ranking stores are external artifacts. Some local raw result
files are unavailable; a fresh clone does not include a complete raw-run bundle.
Do not rebuild the reference report from a partial collection of JSON files.

This runbook is the executable boundary for `hqc-formal-v1`. Commands are run from
the repository root. Re-running generation skips completed query/draw records.
Re-running ranking accepts only the immutable run specification beside its SQLite
store.

Queries are sorted by ID and processed in fixed batches of eight. Each batch contains
all three draws for each query and has a seed derived from the protocol, dataset,
prompt hash, and fixed batch index. Records, parsing, fallback, and aggregation remain
draw-specific.

`uv run hqc progress` reports exact completed/expected counts at any time. The lock
command additionally runs `uv run hqc progress --require-complete`; incomplete or
cross-commit generation and ranking artifacts cannot pass the held-out gate.

## 0. Environment and compatibility gate

A fresh full run creates its own lock. The original experiment lock refers to
commit `ec605a35a22693b65ca98f7448ca2954ea6bcfed`; subsequent comparison methods
use later code. See [experiment provenance](../artifacts/lock/README.md).

```bash
make setup
make verify
uv run hqc environment
uv run hqc prepare-model --model primary
uv run hqc prepare-model --model robustness
make compatibility
```

Every formal prompt is gated by two independent 24-record runs. Every run must have
zero final failures and must report its retries, pinned model revision, unquantized
BF16, the pinned MLX-LM and XGrammar backends, and all generation attempts. The two
runs must reproduce query IDs, draw IDs, seeds, raw outputs, parsed references,
statuses, and attempts exactly. The primary prompt is checked with both Qwen and
Mistral; every baseline prompt is checked with Qwen.
A model-load, conversion, BF16, or memory failure stops the formal run. Converted
weight files have their own manifest and are included in the pre-held-out lock.

## 1. Qwen generation before held-out qrels access

```bash
for dataset in scifact nfcorpus trec-covid fiqa arguana webis-touche2020 scidocs; do
  uv run hqc generate --dataset "$dataset" \
    --prompt prompts/primary-reference-v1.txt \
    --output "artifacts/generations/bridge/$dataset.jsonl"
  uv run hqc generate --dataset "$dataset" \
    --prompt prompts/baselines/mugi-v1.txt \
    --output "artifacts/generations/mugi/$dataset.jsonl"
  uv run hqc generate --dataset "$dataset" --reference-count 1 \
    --prompt prompts/baselines/query2doc-v1.txt \
    --output "artifacts/generations/query2doc/$dataset.jsonl"
done

uv run hqc generate --dataset fiqa --reference-count 8 --max-new-tokens 512 \
  --prompt prompts/baselines/hyde-fiqa-v1.txt \
  --output artifacts/generations/hyde/fiqa.jsonl
uv run hqc generate --dataset arguana --reference-count 8 --max-new-tokens 512 \
  --prompt prompts/baselines/hyde-arguana-v1.txt \
  --output artifacts/generations/hyde/arguana.jsonl
uv run hqc generate --dataset scifact --reference-count 8 --max-new-tokens 512 \
  --prompt prompts/baselines/hyde-scifact-v1.txt \
  --output artifacts/generations/hyde/scifact.jsonl
uv run hqc generate --dataset trec-covid --reference-count 8 --max-new-tokens 512 \
  --prompt prompts/baselines/hyde-trec-covid-v1.txt \
  --output artifacts/generations/hyde/trec-covid.jsonl
for dataset in nfcorpus webis-touche2020 scidocs; do
  uv run hqc generate --dataset "$dataset" --reference-count 8 --max-new-tokens 512 \
    --prompt prompts/baselines/hyde-v1.txt \
    --output "artifacts/generations/hyde/$dataset.jsonl"
done
```

## 2. Primary ranking stores

```bash
for dataset in scifact nfcorpus trec-covid fiqa arguana webis-touche2020 scidocs; do
  uv run hqc rank --dataset "$dataset" \
    --bridge-generation "artifacts/generations/bridge/$dataset.jsonl" \
    --mugi-generation "artifacts/generations/mugi/$dataset.jsonl" \
    --hyde-generation "artifacts/generations/hyde/$dataset.jsonl" \
    --query2doc-generation "artifacts/generations/query2doc/$dataset.jsonl"
done
```

Development evaluation is permitted immediately. Held-out evaluation is not.

## 3. Robustness artifacts before held-out qrels access

Mistral uses the hash-selected 100-query subset. Contriever uses the complete Qwen
primary records and a separate ranking store.

```bash
for dataset in fiqa arguana webis-touche2020 scidocs; do
  uv run hqc generate --model robustness --dataset "$dataset" --hash-limit 100 \
    --prompt prompts/primary-reference-v1.txt \
    --output "artifacts/generations/robustness/$dataset.jsonl"
  uv run hqc rank --dataset "$dataset" --run-id mistral \
    --bridge-generation "artifacts/generations/robustness/$dataset.jsonl"
  uv run hqc rank --dataset "$dataset" --run-id contriever \
    --dense-key robustness_dense \
    --bridge-generation "artifacts/generations/bridge/$dataset.jsonl"
done
```

## 4. Nested TREC-COVID scale stores

The same Qwen records are reused because every snapshot has the same queries. Each
snapshot builds its own Lucene index, so BM25 collection statistics are recomputed.

```bash
for dataset in trec-covid-25000 trec-covid-50000 trec-covid-100000 trec-covid-171332; do
  uv run hqc rank --dataset "$dataset" \
    --bridge-generation artifacts/generations/bridge/trec-covid.jsonl
done
```

## 5. Freeze and unseal

All protocol files must be committed and the working tree clean. The lock hashes
held-out corpora, queries, source archives, generation records, indices, embeddings,
and ranking stores.

```bash
make verify
uv run hqc environment
uv run hqc lock
for dataset in fiqa arguana webis-touche2020 scidocs; do
  uv run hqc unseal --dataset "$dataset"
done
```

No protocol file may change after this gate. A necessary correction increments the
protocol version and invalidates all affected held-out results.

## 6. Evaluation matrix

```bash
for dataset in fiqa arguana webis-touche2020 scidocs; do
  uv run hqc evaluate --dataset "$dataset" \
    --store "artifacts/rankings/$dataset/rankings.sqlite3"
  for references in 1 3; do
    uv run hqc evaluate --dataset "$dataset" --reference-count "$references" \
      --skip-fidelity --skip-fixed-top-l \
      --store "artifacts/rankings/$dataset/rankings.sqlite3"
  done
  for constant in 2 20 100; do
    uv run hqc evaluate --dataset "$dataset" --rrf-constant "$constant" \
      --skip-fidelity --skip-fixed-top-l \
      --store "artifacts/rankings/$dataset/rankings.sqlite3"
  done
  uv run hqc evaluate --dataset "$dataset" --result-track robustness \
    --condition-id mistral \
    --skip-fidelity --skip-fixed-top-l --output-id "${dataset}-mistral" \
    --store "artifacts/rankings/$dataset/rankings-mistral.sqlite3"
  uv run hqc evaluate --dataset "$dataset" --result-track robustness \
    --condition-id contriever \
    --skip-fidelity --skip-fixed-top-l --output-id "${dataset}-contriever" \
    --store "artifacts/rankings/$dataset/rankings-contriever.sqlite3"
done

for dataset in trec-covid-25000 trec-covid-50000 trec-covid-100000 trec-covid-171332; do
  uv run hqc evaluate --dataset "$dataset" --result-track scale \
    --skip-fidelity --skip-fixed-top-l \
    --store "artifacts/rankings/$dataset/rankings.sqlite3"
done
```

Development datasets use the same commands but stay separate from held-out tables.

## 7. Clean rebuild and report

```bash
uv run hqc report --input artifacts/results/raw --output report
make verify
make clean-rebuild
```

The clean-room check creates a fresh environment from `uv.lock` and verifies the
13 tables rebuilt from released per-query draw means, using a numerical tolerance
of 1e-10. It does not require original model or ranking artifacts.


## Supplementary analyses

After the ranking stores and generation records are available:

```sh
uv run python scripts/run_mechanism_analysis.py
uv run python scripts/run_evidence_strengthening.py
uv run python scripts/run_qudar_depth.py
uv run python scripts/run_qudar_confidence.py
uv run python scripts/run_anchorqe_dense_comparison.py
uv run python scripts/run_anchorqe_dense_comparison.py --stream-calibrated
```

These commands produce the mechanism, operator-control, QUDAR, and AnchorQE
records in `report/`. They require the full retrieval artifacts; `make tables`
only regenerates the core report from included per-query results.
