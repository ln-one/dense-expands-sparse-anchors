from runpy import run_path

import numpy as np

exact_top_k = run_path("scripts/run_anchorqe_dense_comparison.py")["exact_top_k"]


def test_exact_top_k_breaks_score_ties_by_document_id() -> None:
    document_ids = np.asarray(["b", "a", "c"])
    document_embeddings = np.asarray(
        [[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]], dtype=np.float32
    )
    query_vectors = np.asarray([[1.0, 0.0]], dtype=np.float32)
    assert exact_top_k(
        document_ids, document_embeddings, query_vectors, top_k=2, batch_size=1
    ) == [["a", "b"]]
