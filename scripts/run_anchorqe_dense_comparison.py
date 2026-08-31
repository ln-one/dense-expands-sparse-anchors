from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml
import zstandard as zstd

from hybrid_query_construction.datasets import load_qrels
from hybrid_query_construction.io import read_jsonl, sha256_bytes, sha256_file, write_json
from hybrid_query_construction.methods import (
    fixed_anchor_qe,
    l2_normalize,
)
from hybrid_query_construction.metrics import ndcg_at_k, recall_at_k
from hybrid_query_construction.retrieval import DenseEncoder
from hybrid_query_construction.statistics import (
    holm_adjust,
    stratified_macro_bootstrap,
    stratified_sign_flip_pvalue,
)

DATASETS = (
    "scifact",
    "nfcorpus",
    "trec-covid",
    "fiqa",
    "arguana",
    "webis-touche2020",
    "scidocs",
)
METHODS = (
    "original",
    "expansion_only",
    "query_expansion_reencode",
    "anchorqe_fixed_015",
    "desa_de",
)
ALPHA = 0.15
REFERENCE_COUNT = 5


class StoredTopK:
    def __init__(self, path: Path) -> None:
        self.connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        row = self.connection.execute(
            "SELECT value FROM metadata WHERE key='documents_json'"
        ).fetchone()
        if row is None:
            raise RuntimeError(f"missing document metadata: {path}")
        self.document_ids = tuple(json.loads(row[0]))
        dataset_row = self.connection.execute(
            "SELECT value FROM metadata WHERE key='dataset'"
        ).fetchone()
        if dataset_row is None:
            raise RuntimeError(f"missing dataset metadata: {path}")
        self.dataset = str(dataset_row[0])

    def close(self) -> None:
        self.connection.close()

    def get(
        self,
        query_id: str,
        draw_id: int,
        track: str,
        channel: str,
        reference_count: int,
        top_k: int = 20,
    ) -> list[str]:
        row = self.connection.execute(
            """SELECT ranking, ranking_sha256 FROM rankings
            WHERE dataset=? AND query_id=? AND draw_id=? AND track=? AND channel=?
            AND reference_count=?""",
            (self.dataset, query_id, draw_id, track, channel, reference_count),
        ).fetchone()
        if row is None:
            raise KeyError((query_id, draw_id, track, channel, reference_count))
        raw = zstd.ZstdDecompressor().decompress(row[0])
        if sha256_bytes(raw) != row[1]:
            raise RuntimeError("ranking artifact hash mismatch")
        ordinals = np.frombuffer(raw, dtype="<u4", count=top_k)
        return [self.document_ids[int(index)] for index in ordinals]


def exact_top_k(
    document_ids: np.ndarray[Any, np.dtype[np.str_]],
    document_embeddings: np.ndarray[Any, np.dtype[np.float32]],
    query_vectors: np.ndarray[Any, np.dtype[np.float32]],
    *,
    top_k: int = 20,
    batch_size: int = 24,
) -> list[list[str]]:
    rankings: list[list[str]] = []
    for start in range(0, len(query_vectors), batch_size):
        scores = np.asarray(
            document_embeddings @ query_vectors[start : start + batch_size].T,
            dtype=np.float32,
        )
        for column in range(scores.shape[1]):
            values = scores[:, column]
            boundary = np.partition(values, len(values) - top_k)[-top_k]
            candidates = np.flatnonzero(values >= boundary)
            order = np.lexsort((document_ids[candidates], -values[candidates]))[:top_k]
            rankings.append(document_ids[candidates[order]].tolist())
    return rankings


def metric_row(
    dataset: str,
    query_id: str,
    draw_id: int,
    method: str,
    ranking: list[str],
    qrels: dict[str, int],
) -> dict[str, object]:
    return {
        "dataset": dataset,
        "query_id": query_id,
        "draw_id": draw_id,
        "method": method,
        "ndcg_at_10": ndcg_at_k(ranking, qrels, 10),
        "recall_at_20": recall_at_k(ranking, qrels, 20),
    }


def run_dataset(
    root: Path,
    dataset: str,
    encoder: DenseEncoder,
    instruction: str,
    dense_cache_id: str,
    *,
    encode_batch_size: int,
    score_batch_size: int,
) -> list[dict[str, object]]:
    records = [
        row
        for row in read_jsonl(
            root / "artifacts" / "generations" / "bridge" / f"{dataset}.jsonl"
        )
        if row["status"] == "ok" and len(row["parsed_references"]) >= REFERENCE_COUNT
    ]
    records.sort(key=lambda row: (str(row["query_id"]), int(row["draw_id"])))
    query_texts = {str(row["query_id"]): str(row["query_text"]) for row in records}
    query_ids = sorted(query_texts)
    original_matrix = encoder.encode_queries(
        [query_texts[query_id] for query_id in query_ids],
        instruction,
        batch_size=encode_batch_size,
    )
    original_by_query = dict(zip(query_ids, original_matrix, strict=True))

    expansion_texts: list[str] = []
    combined_texts: list[str] = []
    for row in records:
        query = str(row["query_text"])
        references = [str(item) for item in row["parsed_references"][:REFERENCE_COUNT]]
        expansion_texts.extend(references)
        combined_texts.append(" [SEP] ".join([query, *references]))
    expansion_stream_vectors = encoder.encode_queries(
        expansion_texts, instruction, batch_size=encode_batch_size
    ).reshape(len(records), REFERENCE_COUNT, -1)
    combined_vectors = encoder.encode_queries(
        combined_texts, instruction, batch_size=encode_batch_size
    )

    anchor_vectors = np.stack(
        [
            fixed_anchor_qe(original_by_query[str(row["query_id"])], vectors, ALPHA)
            for row, vectors in zip(records, expansion_stream_vectors, strict=True)
        ]
    )
    expansion_vectors = np.stack(
        [
            l2_normalize(np.mean(vectors, axis=0, dtype=np.float32))
            for vectors in expansion_stream_vectors
        ]
    )
    candidate_vectors = np.concatenate(
        [expansion_vectors, combined_vectors, anchor_vectors], axis=0
    )

    dense_cache = (
        root
        / "artifacts"
        / "rankings"
        / dataset
        / f"dense-dense-{dense_cache_id}"
    )
    document_ids = np.asarray(
        json.loads((dense_cache / "document_ids.json").read_text(encoding="utf-8")),
        dtype=str,
    )
    document_embeddings = np.load(
        dense_cache / "document_embeddings.npy", mmap_mode="r"
    )
    new_rankings = exact_top_k(
        document_ids,
        document_embeddings,
        candidate_vectors,
        batch_size=score_batch_size,
    )
    count = len(records)
    expansion_rankings = new_rankings[:count]
    combined_rankings = new_rankings[count : 2 * count]
    anchor_rankings = new_rankings[2 * count :]

    qrels = load_qrels(root / "data" / "processed" / dataset / "qrels.tsv")
    store = StoredTopK(
        root / "artifacts" / "rankings" / dataset / "rankings.sqlite3"
    )
    rows: list[dict[str, object]] = []
    original_cache: dict[str, list[str]] = {}
    try:
        for index, row in enumerate(records):
            query_id = str(row["query_id"])
            draw_id = int(row["draw_id"])
            if query_id not in original_cache:
                original_cache[query_id] = store.get(
                    query_id, 0, "base", "dense_original", 0
                )
            rankings = {
                "original": original_cache[query_id],
                "expansion_only": expansion_rankings[index],
                "query_expansion_reencode": combined_rankings[index],
                "anchorqe_fixed_015": anchor_rankings[index],
                "desa_de": store.get(
                    query_id,
                    draw_id,
                    "controlled",
                    "dense_residual",
                    REFERENCE_COUNT,
                ),
            }
            rows.extend(
                metric_row(
                    dataset,
                    query_id,
                    draw_id,
                    method,
                    rankings[method],
                    qrels[query_id],
                )
                for method in METHODS
            )
    finally:
        store.close()
    return rows


def summarize(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    query_means = (
        frame.groupby(["dataset", "query_id", "method"], as_index=False)[
            ["ndcg_at_10", "recall_at_20"]
        ]
        .mean()
        .sort_values(["dataset", "query_id", "method"])
    )
    dataset_means = (
        query_means.groupby(["dataset", "method"], as_index=False)[
            ["ndcg_at_10", "recall_at_20"]
        ]
        .mean()
        .sort_values(["dataset", "method"])
    )
    macro = (
        dataset_means.groupby("method", as_index=False)[
            ["ndcg_at_10", "recall_at_20"]
        ]
        .mean()
        .assign(dataset="Macro")
    )
    summary = pd.concat([dataset_means, macro], ignore_index=True)
    return query_means, summary


def paired_tests(query_means: pd.DataFrame) -> pd.DataFrame:
    tests: list[dict[str, object]] = []
    raw_pvalues: dict[str, float] = {}
    for metric in ("ndcg_at_10", "recall_at_20"):
        wide = query_means.pivot(
            index=["dataset", "query_id"], columns="method", values=metric
        )
        differences = {
            str(dataset): group["desa_de"].sub(group["anchorqe_fixed_015"]).tolist()
            for dataset, group in wide.groupby(level="dataset")
        }
        estimate, lower, upper = stratified_macro_bootstrap(differences)
        pvalue = stratified_sign_flip_pvalue(differences)
        raw_pvalues[metric] = pvalue
        tests.append(
            {
                "comparison": "desa_de-anchorqe_fixed_015",
                "metric": metric,
                "macro_difference": estimate,
                "ci95_lower": lower,
                "ci95_upper": upper,
                "p_raw": pvalue,
            }
        )
    adjusted = holm_adjust(raw_pvalues)
    for row in tests:
        row["p_holm"] = adjusted[str(row["metric"])]
    return pd.DataFrame(tests)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--encode-batch-size", type=int, default=128)
    parser.add_argument("--score-batch-size", type=int, default=24)
    args = parser.parse_args()
    root = args.root.resolve()
    retrievers = yaml.safe_load(
        (root / "configs" / "retrievers" / "formal-v1.yaml").read_text(encoding="utf-8")
    )
    dense = retrievers["dense"]
    dense_cache_id = sha256_bytes(
        json.dumps(dense, sort_keys=True, separators=(",", ":")).encode()
    )[:12]
    encoder = DenseEncoder(dense["model_id"], dense["revision"])

    rows: list[dict[str, object]] = []
    for dataset in DATASETS:
        print(f"Running {dataset}...", flush=True)
        rows.extend(
            run_dataset(
                root,
                dataset,
                encoder,
                dense.get("query_instruction", ""),
                dense_cache_id,
                encode_batch_size=args.encode_batch_size,
                score_batch_size=args.score_batch_size,
            )
        )

    report = root / "report"
    frame = pd.DataFrame(rows)
    query_means, summary = summarize(frame)
    tests = paired_tests(query_means)
    raw_path = report / "anchorqe-dense-results.csv"
    summary_path = report / "anchorqe-dense-summary.csv"
    tests_path = report / "anchorqe-dense-paired-tests.csv"
    frame.to_csv(raw_path, index=False)
    summary.to_csv(summary_path, index=False)
    tests.to_csv(tests_path, index=False)
    write_json(
        report / "anchorqe-dense-manifest.json",
        {
            "schema_version": 1,
            "datasets": list(DATASETS),
            "methods": list(METHODS),
            "reference_count": REFERENCE_COUNT,
            "anchorqe_alpha": ALPHA,
            "anchorqe_expansion_mixture": (
                "uniform mean of five normalized E_query(reference_i) vectors"
            ),
            "desa_contextual_mixture": (
                "mean of five normalized E_query(query [SEP] reference_i) vectors"
            ),
            "query_expansion_reencode": (
                "E_query(query [SEP] reference_1 ... [SEP] reference_5)"
            ),
            "draw_aggregation": "mean within query",
            "dataset_aggregation": "equal-weight macro",
            "paired_test": "stratified query-level sign flip; Holm over two metrics",
            "bootstrap": "10000 stratified query resamples; seed 20260813",
            "raw_results_sha256": sha256_file(raw_path),
            "summary_sha256": sha256_file(summary_path),
            "paired_tests_sha256": sha256_file(tests_path),
            "generation_sha256": {
                dataset: sha256_file(
                    root
                    / "artifacts"
                    / "generations"
                    / "bridge"
                    / f"{dataset}.jsonl"
                )
                for dataset in DATASETS
            },
        },
    )
    print(summary[summary["dataset"] == "Macro"].to_string(index=False), flush=True)
    print(tests.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
