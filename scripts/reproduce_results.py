"""Rebuild result tables from released per-query draw means, without models."""
import argparse
from pathlib import Path

import pandas as pd

from hybrid_query_construction.reporting import (
    EVALUATION_DATASETS,
    _access_changes,
    _classify_primary_outcomes,
    _method_macro_intervals,
    _paired_tests,
    _summary,
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    reference = root / "report"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "tmp/reproduced-tables")
    output = parser.parse_args().output
    output.mkdir(parents=True, exist_ok=True)
    queries = pd.read_csv(reference / "per-query-draw-mean.csv")
    summary = _summary(queries)
    evaluation = queries[queries.dataset.isin(EVALUATION_DATASETS)]
    access, intervals = _access_changes(evaluation)
    paired = _paired_tests(evaluation)
    tables = {
        "all-results": summary,
        "main-results": summary[
            summary.dataset.isin(EVALUATION_DATASETS)
            & summary.track.eq("controlled") & summary.condition_id.eq("primary")
            & summary.reference_count.eq(5) & summary.rrf_constant.eq(60)
        ],
        "fidelity-results": summary[
            summary.dataset.isin(EVALUATION_DATASETS) & summary.track.eq("fidelity")
        ],
        "ablation-results": summary[summary.track.eq("ablation")],
        "reference-count-results": summary[
            summary.track.isin(("controlled", "ablation")) & summary.rrf_constant.eq(60)
        ],
        "rrf-constant-results": summary[
            summary.track.isin(("controlled", "ablation")) & summary.reference_count.eq(5)
        ],
        "robustness-results": summary[summary.track.eq("robustness")],
        "scale-results": summary[summary.track.eq("scale")],
        "access-changes-vs-original": access,
        "access-macro-bootstrap": intervals,
        "primary-paired-tests": paired,
        "main-macro-bootstrap": _method_macro_intervals(evaluation),
        "outcome-classification": _classify_primary_outcomes(paired),
    }
    for name, frame in tables.items():
        frame.to_csv(output / f"{name}.csv", index=False)
        expected = pd.read_csv(reference / f"{name}.csv")
        pd.testing.assert_frame_equal(
            frame.reset_index(drop=True), expected, check_dtype=False,
            check_exact=False, rtol=1e-10, atol=1e-10,
        )
    print(f"Verified {len(tables)} tables against released per-query records: {output}")


if __name__ == "__main__":
    main()
