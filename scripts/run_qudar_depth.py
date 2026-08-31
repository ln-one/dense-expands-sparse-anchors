from __future__ import annotations

import argparse
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from hybrid_query_construction.io import atomic_write_text, canonical_json, read_jsonl
from hybrid_query_construction.replay import replay_complete_wrrf_multi
from hybrid_query_construction.statistics import holm_adjust, stratified_sign_flip_pvalue
from hybrid_query_construction.storage import RankingStore

DATASETS = (
    "scifact",
    "nfcorpus",
    "trec-covid",
    "fiqa",
    "arguana",
    "webis-touche2020",
    "scidocs",
)


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    atomic_write_text(path, "".join(canonical_json(row) + "\n" for row in rows))


def _artifact(
    store: RankingStore,
    channel: str,
    query_id: str,
    draw_id: int,
):
    base = channel in {"sparse_original", "dense_original"}
    return store.get(
        query_id=query_id,
        draw_id=0 if base else draw_id,
        track="base" if base else "controlled",
        channel=channel,
        reference_count=0 if base else 5,
    )


def _run_dataset_shard(
    root_string: str,
    dataset: str,
    shard_index: int,
    shard_count: int,
) -> str:
    root = Path(root_string)
    output = root / "artifacts" / "results" / "derived" / "qudar-depth"
    output.mkdir(parents=True, exist_ok=True)
    confidence_rows = read_jsonl(
        root
        / "artifacts"
        / "results"
        / "derived"
        / "qudar-confidence"
        / f"{dataset}.jsonl"
    )
    weights = {
        (str(row["query_id"]), int(row["draw_id"])): (
            float(row["w_os"]),
            float(row["w_od"]),
            float(row["w_es"]),
            float(row["w_ed"]),
        )
        for row in confidence_rows
        if row["method"] == "qudar_confidence_matched"
    }
    store_path = root / "artifacts" / "rankings" / dataset / "rankings.sqlite3"
    document_ids = RankingStore.load_document_ids(store_path)
    rows: list[dict[str, object]] = []
    with RankingStore(store_path, dataset, document_ids) as store:
        draws = sorted(
            {
                (query_id, draw_id)
                for query_id, draw_id, track, channel, count in store.keys()
                if track == "controlled"
                and channel == "dense_residual"
                and count == 5
            }
        )
        selected_draws = draws[shard_index::shard_count]
        for index, (query_id, draw_id) in enumerate(selected_draws, start=1):
            artifacts = tuple(
                _artifact(store, channel, query_id, draw_id)
                for channel in (
                    "sparse_original",
                    "dense_original",
                    "sparse_rewrite",
                    "dense_contextual",
                )
            )
            rankings = tuple(artifact.ranking for artifact in artifacts)
            for method, method_weights in (
                ("qudar_complete_uniform_rrf", None),
                ("qudar_complete_confidence_rrf", weights[(query_id, draw_id)]),
            ):
                try:
                    replay = replay_complete_wrrf_multi(
                        rankings,
                        top_k=20,
                        constant=60,
                        weights=method_weights,
                    )
                except AssertionError as error:
                    raise AssertionError(
                        f"{dataset}/{query_id}/{draw_id}/{method}"
                    ) from error
                rows.append(
                    {
                        "dataset": dataset,
                        "query_id": query_id,
                        "draw_id": draw_id,
                        "method": method,
                        "os_depth": replay.depths[0],
                        "od_depth": replay.depths[1],
                        "es_depth": replay.depths[2],
                        "ed_depth": replay.depths[3],
                        "total_depth": sum(replay.depths),
                        "checks": replay.checks,
                    }
                )
            if index % 100 == 0 or index == len(selected_draws):
                print(
                    f"[{dataset} shard {shard_index + 1}/{shard_count}] "
                    f"{index}/{len(selected_draws)} query-draws",
                    flush=True,
                )
    path = output / f"{dataset}.part-{shard_index:02d}-of-{shard_count:02d}.jsonl"
    _write_jsonl(path, rows)
    return str(path)


def _merge_shards(root: Path, dataset: str, paths: list[str]) -> None:
    rows = [row for path in paths for row in read_jsonl(Path(path))]
    rows.sort(key=lambda row: (str(row["query_id"]), int(row["draw_id"]), str(row["method"])))
    output = root / "artifacts" / "results" / "derived" / "qudar-depth"
    _write_jsonl(output / f"{dataset}.jsonl", rows)


def _load_desa(root: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    raw = root / "artifacts" / "results" / "raw"
    for path in sorted(raw.glob("*.jsonl")):
        if "fixed-top-l" not in path.name:
            rows.extend(read_jsonl(path))
    frame = pd.DataFrame(rows)
    selected = frame[
        frame["dataset"].isin(DATASETS)
        & (frame["track"] == "controlled")
        & (frame["condition_id"] == "primary")
        & (frame["reference_count"] == 5)
        & (frame["rrf_constant"] == 60)
        & (frame["method"] == "proposed")
    ][["dataset", "query_id", "draw_id", "dense_depth", "sparse_depth"]].copy()
    selected["method"] = "desa"
    selected["os_depth"] = float("nan")
    selected["od_depth"] = float("nan")
    selected["es_depth"] = float("nan")
    selected["ed_depth"] = float("nan")
    selected["total_depth"] = selected["dense_depth"] + selected["sparse_depth"]
    return selected


def _macro_ratio_bootstrap(
    paired: dict[str, np.ndarray],
    *,
    resamples: int = 10_000,
    seed: int = 20260813,
) -> tuple[float, float, float]:
    """Bootstrap 1 - macro(DESA depth) / macro(comparator depth)."""
    arrays = [np.asarray(values, dtype=np.float64) for values in paired.values()]
    if not arrays or any(len(values) == 0 for values in arrays):
        raise ValueError("each dataset needs at least one paired row")

    def reduction(sampled: list[np.ndarray]) -> float:
        desa_macro = float(np.mean([values[:, 0].mean() for values in sampled]))
        comparator_macro = float(
            np.mean([values[:, 1].mean() for values in sampled])
        )
        return 1.0 - desa_macro / comparator_macro

    observed = reduction(arrays)
    random = np.random.default_rng(seed)
    samples = np.empty(resamples, dtype=np.float64)
    for sample_index in range(resamples):
        sampled = [
            values[random.integers(0, len(values), size=len(values))]
            for values in arrays
        ]
        samples[sample_index] = reduction(sampled)
    lower, upper = np.quantile(samples, [0.025, 0.975])
    return observed, float(lower), float(upper)


def _write_paired_tests(root: Path, frame: pd.DataFrame) -> None:
    query_means = frame.groupby(
        ["dataset", "query_id", "method"], as_index=False
    )["total_depth"].mean()
    desa = query_means[query_means["method"] == "desa"]
    rows: list[dict[str, object]] = []
    pvalues: dict[str, float] = {}
    for comparator in (
        "qudar_complete_uniform_rrf",
        "qudar_complete_confidence_rrf",
    ):
        other = query_means[query_means["method"] == comparator]
        merged = desa.merge(
            other,
            on=["dataset", "query_id"],
            suffixes=("_desa", "_comparator"),
            validate="one_to_one",
        )
        paired = {
            str(dataset): group[
                ["total_depth_desa", "total_depth_comparator"]
            ].to_numpy(dtype=float)
            for dataset, group in merged.groupby("dataset")
        }
        estimate, lower, upper = _macro_ratio_bootstrap(paired)
        differences = {
            dataset: (values[:, 1] - values[:, 0]).tolist()
            for dataset, values in paired.items()
        }
        pvalue = stratified_sign_flip_pvalue(differences)
        pvalues[comparator] = pvalue
        rows.append(
            {
                "comparison": f"desa_vs_{comparator}",
                "total_depth_reduction": estimate,
                "ci95_lower": lower,
                "ci95_upper": upper,
                "p_raw": pvalue,
            }
        )
    adjusted = holm_adjust(pvalues)
    for row in rows:
        comparator = str(row["comparison"]).removeprefix("desa_vs_")
        row["p_holm"] = adjusted[comparator]
    pd.DataFrame(rows).to_csv(
        root / "report" / "qudar-depth-paired-tests.csv", index=False
    )


def _aggregate(root: Path) -> None:
    directory = root / "artifacts" / "results" / "derived" / "qudar-depth"
    qudar = pd.DataFrame(
        [row for dataset in DATASETS for row in read_jsonl(directory / f"{dataset}.jsonl")]
    )
    desa = _load_desa(root)
    columns = ["os_depth", "od_depth", "es_depth", "ed_depth", "total_depth"]
    frame = pd.concat([desa, qudar], ignore_index=True)
    dataset = frame.groupby(["dataset", "method"], as_index=False)[columns].mean()
    macro = dataset.groupby("method", as_index=False)[columns].mean()
    macro.insert(0, "dataset", "macro_equal_dataset")
    pd.concat([dataset, macro], ignore_index=True).to_csv(
        root / "report" / "qudar-depth-results.csv", index=False
    )
    _write_paired_tests(root, frame)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--datasets", nargs="+", choices=DATASETS, default=list(DATASETS))
    parser.add_argument("--shards", type=int, default=1)
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.aggregate_only:
        _aggregate(root)
        print("QuDAR depth reports aggregated", flush=True)
        return
    datasets = tuple(args.datasets)
    if args.shards <= 0:
        raise ValueError("shards must be positive")
    workers = min(len(datasets) * args.shards, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            (dataset, shard): executor.submit(
                _run_dataset_shard,
                str(root),
                dataset,
                shard,
                args.shards,
            )
            for dataset in datasets
            for shard in range(args.shards)
        }
        for dataset in datasets:
            paths = [futures[(dataset, shard)].result() for shard in range(args.shards)]
            _merge_shards(root, dataset, paths)
    directory = root / "artifacts" / "results" / "derived" / "qudar-depth"
    if all((directory / f"{dataset}.jsonl").exists() for dataset in DATASETS):
        _aggregate(root)
        print("QuDAR depth reports complete", flush=True)
    else:
        print("Selected QuDAR depth datasets complete", flush=True)


if __name__ == "__main__":
    main()
