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
SC_METHODS = (
    "original",
    "anchorqe_fixed_015",
    "anchorqe_sc_matched",
    "desa_de",
)
ALPHA = 0.15
CALIBRATION_QUERIES = 8
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


def stream_calibrated_alpha(
    document_embeddings: np.ndarray[Any, np.dtype[np.float32]],
    original_vectors: np.ndarray[Any, np.dtype[np.float32]],
    expansion_mixtures: np.ndarray[Any, np.dtype[np.float32]],
    *,
    support_k: int = 10,
) -> float:
    """Apply AnchorQE's label-free stream calibration to matched mixtures."""
    query_scores = np.asarray(document_embeddings @ original_vectors.T, dtype=np.float32)
    expansion_scores = np.asarray(
        document_embeddings @ expansion_mixtures.T, dtype=np.float32
    )
    query_top = np.max(query_scores, axis=0)
    expansion_top = np.max(expansion_scores, axis=0)
    query_support: list[float] = []
    expansion_support: list[float] = []
    for column in range(query_scores.shape[1]):
        indices = np.argpartition(query_scores[:, column], -support_k)[-support_k:]
        query_support.append(float(np.mean(query_scores[indices, column])))
        expansion_support.append(float(np.mean(expansion_scores[indices, column])))

    def positive_mean(values: object) -> float:
        return float(np.mean(np.maximum(np.asarray(values, dtype=np.float32), 0.0)))

    query_top_mean = positive_mean(query_top)
    expansion_top_mean = positive_mean(expansion_top)
    query_support_mean = positive_mean(query_support)
    expansion_support_mean = positive_mean(expansion_support)
    top_denominator = query_top_mean + expansion_top_mean
    support_denominator = query_support_mean + expansion_support_mean
    if top_denominator == 0.0 or support_denominator == 0.0:
        return 0.0
    return (expansion_top_mean / top_denominator) * (
        expansion_support_mean / support_denominator
    )


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
    stream_calibrated: bool,
) -> tuple[list[dict[str, object]], dict[int, float]]:
    records = [
        row
        for row in read_jsonl(
            root / "artifacts" / "generations" / "bridge" / f"{dataset}.jsonl"
        )
        if row["status"] == "ok" and len(row["parsed_references"]) >= REFERENCE_COUNT
    ]
    natural_query_ids = list(dict.fromkeys(str(row["query_id"]) for row in records))
    calibration_query_ids = set(natural_query_ids[:CALIBRATION_QUERIES])
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
        if not stream_calibrated:
            combined_texts.append(" [SEP] ".join([query, *references]))
    expansion_stream_vectors = encoder.encode_queries(
        expansion_texts, instruction, batch_size=encode_batch_size
    ).reshape(len(records), REFERENCE_COUNT, -1)
    combined_vectors = (
        encoder.encode_queries(combined_texts, instruction, batch_size=encode_batch_size)
        if combined_texts
        else np.empty((0, original_matrix.shape[1]), dtype=np.float32)
    )

    anchor_vectors = np.stack(
        [
            fixed_anchor_qe(original_by_query[str(row["query_id"])], vectors, ALPHA)
            for row, vectors in zip(records, expansion_stream_vectors, strict=True)
        ]
    )
    expansion_mixtures = np.mean(expansion_stream_vectors, axis=1, dtype=np.float32)
    expansion_vectors = np.stack(
        [
            l2_normalize(mixture)
            for mixture in expansion_mixtures
        ]
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

    calibration: dict[int, float] = {}
    sc_vectors: list[np.ndarray[Any, np.dtype[np.float32]]] = []
    if stream_calibrated:
        for draw_id in sorted({int(row["draw_id"]) for row in records}):
            indices = [
                index
                for index, row in enumerate(records)
                if int(row["draw_id"]) == draw_id
                and str(row["query_id"]) in calibration_query_ids
            ]
            if len(indices) != CALIBRATION_QUERIES:
                raise RuntimeError(
                    f"{dataset} draw {draw_id}: expected {CALIBRATION_QUERIES} "
                    f"calibration queries, found {len(indices)}"
                )
            calibration[draw_id] = stream_calibrated_alpha(
                document_embeddings,
                np.stack(
                    [original_by_query[str(records[index]["query_id"])] for index in indices]
                ),
                expansion_mixtures[indices],
            )
        sc_vectors = [
            fixed_anchor_qe(
                original_by_query[str(row["query_id"])],
                vectors,
                calibration[int(row["draw_id"])],
            )
            for row, vectors in zip(records, expansion_stream_vectors, strict=True)
        ]

    candidate_parts = [anchor_vectors]
    if stream_calibrated:
        candidate_parts.append(np.stack(sc_vectors))
    else:
        candidate_parts[0:0] = [expansion_vectors, combined_vectors]
    candidate_vectors = np.concatenate(candidate_parts, axis=0)
    new_rankings = exact_top_k(
        document_ids,
        document_embeddings,
        candidate_vectors,
        batch_size=score_batch_size,
    )
    count = len(records)
    if stream_calibrated:
        anchor_rankings = new_rankings[:count]
        sc_rankings = new_rankings[count:]
        expansion_rankings: list[list[str]] = []
        combined_rankings: list[list[str]] = []
    else:
        expansion_rankings = new_rankings[:count]
        combined_rankings = new_rankings[count : 2 * count]
        anchor_rankings = new_rankings[2 * count :]
        sc_rankings = []

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
            if stream_calibrated and query_id in calibration_query_ids:
                continue
            if query_id not in original_cache:
                original_cache[query_id] = store.get(
                    query_id, 0, "base", "dense_original", 0
                )
            rankings: dict[str, list[str]] = {
                "original": original_cache[query_id],
                "anchorqe_fixed_015": anchor_rankings[index],
                "desa_de": store.get(
                    query_id,
                    draw_id,
                    "controlled",
                    "dense_residual",
                    REFERENCE_COUNT,
                ),
            }
            if stream_calibrated:
                rankings["anchorqe_sc_matched"] = sc_rankings[index]
                methods = SC_METHODS
            else:
                rankings["expansion_only"] = expansion_rankings[index]
                rankings["query_expansion_reencode"] = combined_rankings[index]
                methods = METHODS
            rows.extend(
                metric_row(
                    dataset,
                    query_id,
                    draw_id,
                    method,
                    rankings[method],
                    qrels[query_id],
                )
                for method in methods
            )
    finally:
        store.close()
    return rows, calibration


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


def paired_tests(
    query_means: pd.DataFrame, left: str = "desa_de", right: str = "anchorqe_fixed_015"
) -> pd.DataFrame:
    tests: list[dict[str, object]] = []
    raw_pvalues: dict[str, float] = {}
    for metric in ("ndcg_at_10", "recall_at_20"):
        wide = query_means.pivot(
            index=["dataset", "query_id"], columns="method", values=metric
        )
        differences = {
            str(dataset): group[left].sub(group[right]).tolist()
            for dataset, group in wide.groupby(level="dataset")
        }
        estimate, lower, upper = stratified_macro_bootstrap(differences)
        pvalue = stratified_sign_flip_pvalue(differences)
        raw_pvalues[metric] = pvalue
        tests.append(
            {
                "comparison": f"{left}-{right}",
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
    parser.add_argument("--stream-calibrated", action="store_true")
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
    calibration: dict[str, dict[int, float]] = {}
    for dataset in DATASETS:
        print(f"Running {dataset}...", flush=True)
        dataset_rows, dataset_calibration = run_dataset(
                root,
                dataset,
                encoder,
                dense.get("query_instruction", ""),
                dense_cache_id,
                encode_batch_size=args.encode_batch_size,
                score_batch_size=args.score_batch_size,
                stream_calibrated=args.stream_calibrated,
            )
        rows.extend(dataset_rows)
        calibration[dataset] = dataset_calibration

    report = root / "report"
    frame = pd.DataFrame(rows)
    query_means, summary = summarize(frame)
    if args.stream_calibrated:
        tests = pd.concat(
            [
                paired_tests(query_means, "desa_de", "anchorqe_sc_matched"),
                paired_tests(query_means, "anchorqe_sc_matched", "anchorqe_fixed_015"),
            ],
            ignore_index=True,
        )
        prefix = "anchorqe-sc-dense"
        methods = SC_METHODS
    else:
        tests = paired_tests(query_means)
        prefix = "anchorqe-dense"
        methods = METHODS
    raw_path = report / f"{prefix}-results.csv"
    summary_path = report / f"{prefix}-summary.csv"
    tests_path = report / f"{prefix}-paired-tests.csv"
    frame.to_csv(raw_path, index=False)
    summary.to_csv(summary_path, index=False)
    tests.to_csv(tests_path, index=False)
    write_json(
        report / f"{prefix}-manifest.json",
        {
            "schema_version": 1,
            "datasets": list(DATASETS),
            "methods": list(methods),
            "reference_count": REFERENCE_COUNT,
            "anchorqe_alpha": ALPHA,
            "stream_calibration": (
                {
                    "calibration_queries": CALIBRATION_QUERIES,
                    "split": "first unique queries in stored generation order",
                    "scope": "independent per dataset and draw",
                    "alphas": calibration,
                    "note": (
                        "matched five-reference mixture adaptation of SC-AnchorQE; "
                        "the source paper calibrates one expansion per query"
                    ),
                }
                if args.stream_calibrated
                else None
            ),
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
