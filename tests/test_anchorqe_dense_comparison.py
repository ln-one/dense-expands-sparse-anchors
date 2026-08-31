from runpy import run_path

import numpy as np

exact_top_k = run_path("scripts/run_anchorqe_dense_comparison.py")["exact_top_k"]
stream_calibrated_alpha = run_path("scripts/run_anchorqe_dense_comparison.py")[
    "stream_calibrated_alpha"
]


def test_exact_top_k_breaks_score_ties_by_document_id() -> None:
    document_ids = np.asarray(["b", "a", "c"])
    document_embeddings = np.asarray(
        [[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]], dtype=np.float32
    )
    query_vectors = np.asarray([[1.0, 0.0]], dtype=np.float32)
    assert exact_top_k(
        document_ids, document_embeddings, query_vectors, top_k=2, batch_size=1
    ) == [["a", "b"]]


def test_stream_calibration_matches_conjunctive_ratio() -> None:
    documents = np.asarray([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    queries = np.asarray([[1.0, 0.0]], dtype=np.float32)
    expansions = np.asarray([[0.6, 0.8]], dtype=np.float32)
    np.testing.assert_allclose(
        stream_calibrated_alpha(documents, queries, expansions, support_k=1),
        1.0 / 6.0,
    )
