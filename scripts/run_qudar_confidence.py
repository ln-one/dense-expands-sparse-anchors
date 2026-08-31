from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from hybrid_query_construction.datasets import load_qrels, load_queries
from hybrid_query_construction.evidence import (
    paired_quality_tests,
    qudar_confidence_fusion,
    uniform_normalized_score_fusion,
)
from hybrid_query_construction.fusion import rank_scores
from hybrid_query_construction.io import (
    atomic_write_text,
    canonical_json,
    read_jsonl,
    sha256_file,
    write_json,
)
from hybrid_query_construction.java import ensure_java_runtime
from hybrid_query_construction.methods import contextual_mean, primary_sparse_rewrite
from hybrid_query_construction.metrics import ndcg_at_k, recall_at_k
from hybrid_query_construction.retrieval import DenseEncoder, SparseSearcher
from hybrid_query_construction.runner import load_generations
from hybrid_query_construction.storage import RankingStore, ranking_store_digest

DATASETS = (
    "scifact",
    "nfcorpus",
    "trec-covid",
    "fiqa",
    "arguana",
    "webis-touche2020",
    "scidocs",
)
MODEL_ID = "BAAI/bge-small-en-v1.5"
MODEL_REVISION = "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"
INSTRUCTION = "Represent this sentence for searching relevant passages: "
DEPTH = 1000
TAU = 2.0


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    atomic_write_text(path, "".join(canonical_json(row) + "\n" for row in rows))


def _load_raw(directory: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for path in sorted(directory.glob("*.jsonl")):
        if "fixed-top-l" not in path.name:
            rows.extend(read_jsonl(path))
    return pd.DataFrame(rows)


def _dense_scores(
    ranking: tuple[str, ...],
    query_vector: np.ndarray,
    document_embeddings: np.ndarray,
    ordinals: dict[str, int],
) -> dict[str, float]:
    selected = ranking[:DEPTH]
    indices = np.fromiter((ordinals[item] for item in selected), dtype=np.int64)
    values = np.asarray(document_embeddings[indices]) @ query_vector
    scores = {item: float(value) for item, value in zip(selected, values, strict=True)}
    if rank_scores(scores) != list(selected):
        raise RuntimeError("recovered dense scores do not reproduce the frozen ranking")
    return scores


def _recover_sparse_scores(
    scores: dict[str, float], ranking: tuple[str, ...]
) -> dict[str, float]:
    selected = ranking[:DEPTH]
    if any(document_id not in scores for document_id in selected):
        raise RuntimeError("sparse candidate buffer does not cover the frozen ranking")
    recovered_scores = {document_id: scores[document_id] for document_id in selected}
    if rank_scores(recovered_scores) != list(selected):
        raise RuntimeError("recovered sparse scores do not reproduce the frozen ranking")
    return recovered_scores


def _embedding_paths(root: Path, dataset: str) -> tuple[Path, Path]:
    matches = sorted((root / "artifacts" / "rankings" / dataset).glob("dense-dense-*/"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one primary dense cache for {dataset}, found {matches}")
    return matches[0] / "document_ids.json", matches[0] / "document_embeddings.npy"


def _run_dataset(root: Path, dataset: str, encoder: DenseEncoder) -> list[dict[str, object]]:
    print(f"[{dataset}] loading frozen inputs", flush=True)
    dataset_root = root / "data" / "processed" / dataset
    queries = load_queries(dataset_root / "queries.jsonl")
    qrels = load_qrels(dataset_root / "qrels.tsv")
    generations = load_generations(
        root / "artifacts" / "generations" / "bridge" / f"{dataset}.jsonl"
    )
    query_ids = sorted(qrels)
    ids_path, embeddings_path = _embedding_paths(root, dataset)
    document_ids = tuple(json.loads(ids_path.read_text(encoding="utf-8")))
    ordinals = {document_id: index for index, document_id in enumerate(document_ids)}
    document_embeddings = np.load(embeddings_path, mmap_mode="r")
    store_path = root / "artifacts" / "rankings" / dataset / "rankings.sqlite3"
    if RankingStore.load_document_ids(store_path) != document_ids:
        raise RuntimeError(f"document identifiers differ for {dataset}")

    print(f"[{dataset}] encoding dense queries", flush=True)
    original_matrix = encoder.encode_queries(
        [queries[query_id] for query_id in query_ids], INSTRUCTION
    )
    original_vectors = dict(zip(query_ids, original_matrix, strict=True))
    contextual_vectors: dict[tuple[str, int], np.ndarray] = {}
    encoded_keys: list[tuple[str, int]] = []
    contextual_texts: list[str] = []
    for query_id in query_ids:
        draws = sorted(draw for qid, draw in generations if qid == query_id)
        if len(draws) != 3:
            raise RuntimeError(f"expected three draws for {dataset}/{query_id}")
        for draw_id in draws:
            record = generations[(query_id, draw_id)]
            references = record.parsed_references[:5]
            if record.status != "ok" or len(references) != 5:
                contextual_vectors[(query_id, draw_id)] = original_vectors[query_id]
                continue
            encoded_keys.append((query_id, draw_id))
            contextual_texts.extend(
                f"{queries[query_id]} [SEP] {reference}" for reference in references
            )
    encoded_references = encoder.encode_queries(contextual_texts, INSTRUCTION)
    contextual_vectors.update(
        {
            key: contextual_mean(encoded_references[index * 5 : (index + 1) * 5])
            for index, key in enumerate(encoded_keys)
        }
    )

    sparse = SparseSearcher(
        root / "artifacts" / "rankings" / dataset / "lucene-index",
        0.9,
        0.4,
        DEPTH + 100,
    )
    rows: list[dict[str, object]] = []
    with RankingStore(store_path, dataset, document_ids) as store:
        for query_index, query_id in enumerate(query_ids, start=1):
            query = queries[query_id]
            os_artifact = store.get(
                query_id=query_id,
                draw_id=0,
                track="base",
                channel="sparse_original",
                reference_count=0,
            )
            od_artifact = store.get(
                query_id=query_id,
                draw_id=0,
                track="base",
                channel="dense_original",
                reference_count=0,
            )
            os_scores = _recover_sparse_scores(sparse.scores(query), os_artifact.ranking)
            od_scores = _dense_scores(
                od_artifact.ranking,
                original_vectors[query_id],
                document_embeddings,
                ordinals,
            )
            for draw_id in range(3):
                record = generations[(query_id, draw_id)]
                es_artifact = store.get(
                    query_id=query_id,
                    draw_id=draw_id,
                    track="controlled",
                    channel="sparse_rewrite",
                    reference_count=5,
                )
                ed_artifact = store.get(
                    query_id=query_id,
                    draw_id=draw_id,
                    track="controlled",
                    channel="dense_contextual",
                    reference_count=5,
                )
                references = record.parsed_references[:5]
                fallback = record.status != "ok" or len(references) != 5
                raw_es_scores = (
                    os_scores
                    if fallback
                    else sparse.scores(primary_sparse_rewrite(query, references))
                )
                es_scores = (
                    os_scores
                    if fallback
                    else _recover_sparse_scores(raw_es_scores, es_artifact.ranking)
                )
                ed_scores = _dense_scores(
                    ed_artifact.ranking,
                    contextual_vectors[(query_id, draw_id)],
                    document_embeddings,
                    ordinals,
                )
                fused, weights = qudar_confidence_fusion(
                    (os_scores, od_scores, es_scores, ed_scores),
                    retrieval_depth=DEPTH,
                    top_k=20,
                    tau=TAU,
                )
                rows.append(
                    {
                        "dataset": dataset,
                        "query_id": query_id,
                        "draw_id": draw_id,
                        "method": "qudar_confidence_matched",
                        "ndcg_at_10": ndcg_at_k(fused, qrels[query_id], 10),
                        "recall_at_20": recall_at_k(fused, qrels[query_id], 20),
                        "w_os": weights[0],
                        "w_od": weights[1],
                        "w_es": weights[2],
                        "w_ed": weights[3],
                        "available_entries": sum(
                            min(DEPTH, len(artifact.ranking))
                            for artifact in (os_artifact, od_artifact, es_artifact, ed_artifact)
                        ),
                    }
                )
                uniform_fused = uniform_normalized_score_fusion(
                    (os_scores, od_scores, es_scores, ed_scores),
                    retrieval_depth=DEPTH,
                    top_k=20,
                )
                rows.append(
                    {
                        "dataset": dataset,
                        "query_id": query_id,
                        "draw_id": draw_id,
                        "method": "qudar_uniform_score_matched",
                        "ndcg_at_10": ndcg_at_k(uniform_fused, qrels[query_id], 10),
                        "recall_at_20": recall_at_k(uniform_fused, qrels[query_id], 20),
                        "w_os": 0.25,
                        "w_od": 0.25,
                        "w_es": 0.25,
                        "w_ed": 0.25,
                        "available_entries": sum(
                            min(DEPTH, len(artifact.ranking))
                            for artifact in (os_artifact, od_artifact, es_artifact, ed_artifact)
                        ),
                    }
                )
            if query_index % 100 == 0 or query_index == len(query_ids):
                print(f"[{dataset}] {query_index}/{len(query_ids)} queries", flush=True)
    return rows


def _aggregate(root: Path, datasets: tuple[str, ...]) -> None:
    derived = root / "artifacts" / "results" / "derived" / "qudar-confidence"
    rows = [row for dataset in datasets for row in read_jsonl(derived / f"{dataset}.jsonl")]
    qudar = pd.DataFrame(rows)
    metrics = ["ndcg_at_10", "recall_at_20", "available_entries"]
    summary = qudar.groupby(["dataset", "method"], as_index=False)[metrics].mean()
    macro = summary.groupby("method", as_index=False)[metrics].mean()
    macro.insert(0, "dataset", "macro_equal_dataset")
    pd.concat([summary, macro], ignore_index=True).to_csv(
        root / "report" / "qudar-confidence-results.csv", index=False
    )
    qudar.groupby(["dataset", "method"], as_index=False)[
        ["w_os", "w_od", "w_es", "w_ed"]
    ].mean().to_csv(root / "report" / "qudar-confidence-weights.csv", index=False)

    complete = _load_raw(root / "artifacts" / "results" / "raw")
    desa = complete[
        complete["dataset"].isin(datasets)
        & (complete["track"] == "controlled")
        & (complete["condition_id"] == "primary")
        & (complete["reference_count"] == 5)
        & (complete["rrf_constant"] == 60)
        & (complete["method"] == "proposed")
    ][["dataset", "query_id", "draw_id", "ndcg_at_10", "recall_at_20"]].copy()
    desa["method"] = "desa"
    comparison = pd.concat(
        [
            desa,
            qudar[["dataset", "query_id", "draw_id", "method", "ndcg_at_10", "recall_at_20"]],
        ],
        ignore_index=True,
    )
    pd.concat(
        [
            paired_quality_tests(comparison, proposed="desa", comparator=comparator)
            for comparator in (
                "qudar_confidence_matched",
                "qudar_uniform_score_matched",
            )
        ],
        ignore_index=True,
    ).to_csv(root / "report" / "qudar-confidence-paired-tests.csv", index=False)

    paired_quality_tests(
        qudar,
        proposed="qudar_confidence_matched",
        comparator="qudar_uniform_score_matched",
    ).to_csv(
        root / "report" / "qudar-confidence-vs-uniform-tests.csv", index=False
    )

    confidence = qudar[qudar["method"] == "qudar_confidence_matched"]
    uniform = qudar[qudar["method"] == "qudar_uniform_score_matched"]
    paired_outcomes = confidence.merge(
        uniform,
        on=["dataset", "query_id", "draw_id"],
        suffixes=("_confidence", "_uniform"),
        validate="one_to_one",
    )
    stability_rows: list[dict[str, object]] = []
    for metric in ("ndcg_at_10", "recall_at_20"):
        unchanged = (
            paired_outcomes[f"{metric}_confidence"]
            == paired_outcomes[f"{metric}_uniform"]
        )
        stability_rows.append(
            {
                "metric": metric,
                "pooled_query_draw_unchanged": float(unchanged.mean()),
                "macro_equal_dataset_query_draw_unchanged": float(
                    unchanged.groupby(paired_outcomes["dataset"]).mean().mean()
                ),
                "unchanged_query_draws": int(unchanged.sum()),
                "total_query_draws": len(unchanged),
            }
        )
    pd.DataFrame(stability_rows).to_csv(
        root / "report" / "qudar-confidence-outcome-stability.csv", index=False
    )
    write_json(
        root / "report" / "qudar-confidence-manifest.json",
        {
            "schema_version": 1,
            "datasets": list(datasets),
            "variant": "QuDAR-confidence matched",
            "official_code_commit": "0702721e82799d0489850d3f94ac787da43436ad",
            "retrieval_depth_per_signal": DEPTH,
            "confidence_topk": 10,
            "confidence_tau": TAU,
            "signals": ["OS", "OD", "ES", "ED"],
            "dataset_artifacts_sha256": {
                dataset: sha256_file(derived / f"{dataset}.jsonl") for dataset in datasets
            },
            "ranking_store_sha256": {
                dataset: ranking_store_digest(
                    root / "artifacts" / "rankings" / dataset / "rankings.sqlite3"
                )
                for dataset in datasets
            },
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--datasets", nargs="+", choices=DATASETS, default=list(DATASETS))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    datasets = tuple(args.datasets)
    output = root / "artifacts" / "results" / "derived" / "qudar-confidence"
    output.mkdir(parents=True, exist_ok=True)
    pending = [
        dataset
        for dataset in datasets
        if args.force or not (output / f"{dataset}.jsonl").exists()
    ]
    if pending:
        ensure_java_runtime(21)
        encoder = DenseEncoder(MODEL_ID, MODEL_REVISION, device="mps")
        for dataset in pending:
            rows = _run_dataset(root, dataset, encoder)
            _write_jsonl(output / f"{dataset}.jsonl", rows)
            print(f"[{dataset}] saved {len(rows)} query-draw rows", flush=True)
    _aggregate(root, datasets)
    print("QuDAR-confidence reports complete", flush=True)


if __name__ == "__main__":
    main()
