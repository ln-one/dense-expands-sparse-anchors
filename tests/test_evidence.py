import pandas as pd
import pytest

from hybrid_query_construction.evidence import (
    fixed_cutoff_diagnostics,
    paired_quality_tests,
    qudar_confidence_fusion,
    qudar_simple_rrf,
    uniform_normalized_score_fusion,
)


def test_qudar_simple_rrf_uses_four_truncated_rankings() -> None:
    rankings = (["a", "b"], ["b", "a"], ["a", "c"], ["c", "a"])
    assert qudar_simple_rrf(rankings, retrieval_depth=1, top_k=3, constant=0) == [
        "a",
        "b",
        "c",
    ]
    with pytest.raises(ValueError):
        qudar_simple_rrf(rankings[:3])


def test_qudar_confidence_fusion_weights_score_margins() -> None:
    signals = (
        {"a": 3.0, "b": 1.0},
        {"b": 2.0, "a": 1.0},
        {"c": 1.0, "a": 0.9},
        {"a": 1.0, "c": 1.0},
    )
    ranking, weights = qudar_confidence_fusion(signals, top_k=3, tau=2.0)
    assert ranking == ["a", "b", "c"]
    assert sum(weights) == pytest.approx(1.0)
    assert weights[0] == pytest.approx(weights[1])
    assert weights[0] > weights[2] > weights[3]
    with pytest.raises(ValueError):
        qudar_confidence_fusion(signals[:3])


def test_uniform_normalized_score_fusion() -> None:
    signals = ({"a": 2.0, "b": 0.0}, {"b": 4.0, "a": 3.0})
    assert uniform_normalized_score_fusion(signals, top_k=2) == ["a", "b"]


def test_fixed_cutoff_diagnostics_counts_conclusion_changes() -> None:
    complete = pd.DataFrame(
        [
            {
                "dataset": "d",
                "query_id": "q",
                "draw_id": 0,
                "method": "original",
                "reference_count": 5,
                "rrf_constant": 60,
                "ndcg_at_10": 0.4,
                "recall_at_20": 0.4,
            },
            {
                "dataset": "d",
                "query_id": "q",
                "draw_id": 0,
                "method": "proposed",
                "reference_count": 5,
                "rrf_constant": 60,
                "ndcg_at_10": 0.5,
                "recall_at_20": 0.3,
            },
        ]
    )
    fixed = pd.DataFrame(
        [
            {
                **complete.iloc[0].to_dict(),
                "top_l": 10,
                "complete_top20_exact": False,
                "ndcg_at_10": 0.45,
                "recall_at_20": 0.4,
            },
            {
                **complete.iloc[1].to_dict(),
                "top_l": 10,
                "complete_top20_exact": False,
                "ndcg_at_10": 0.35,
                "recall_at_20": 0.5,
            },
        ]
    )
    diagnostics, conclusions = fixed_cutoff_diagnostics(
        complete, fixed, methods=("original", "proposed")
    )
    proposed = diagnostics[diagnostics["method"] == "proposed"].iloc[0]
    assert proposed["ndcg_at_10_abs_error"] == pytest.approx(0.15)
    outcome = conclusions.iloc[0]
    assert outcome["ndcg_direction_reversal"] == 1.0
    assert outcome["recall_direction_reversal"] == 1.0


def test_paired_quality_tests_average_draws_and_adjust_outcomes() -> None:
    rows = []
    for method, values in (("a", (0.2, 0.6)), ("b", (0.1, 0.3))):
        for draw_id, value in enumerate(values):
            rows.append(
                {
                    "dataset": "d",
                    "query_id": "q",
                    "draw_id": draw_id,
                    "method": method,
                    "ndcg_at_10": value,
                    "recall_at_20": value,
                }
            )
    result = paired_quality_tests(pd.DataFrame(rows), proposed="a", comparator="b")
    assert set(result["metric"]) == {"ndcg_at_10", "recall_at_20"}
    assert result["favorable_difference"].tolist() == pytest.approx([0.2, 0.2])
    assert result["p_holm"].between(0.0, 1.0).all()
