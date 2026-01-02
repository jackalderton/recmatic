"""
semantic_embeddings.py

Lightweight local semantic embedding helpers for Recmatic.

Default model: sentence-transformers/all-MiniLM-L6-v2 (fast, CPU-friendly).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable, List, Tuple
import re


def parse_semantic_queries(raw: str) -> List[str]:
    """
    Parse a single text input into a list of queries.
    Accepts comma-separated and/or newline-separated input.
    """
    if not raw:
        return []
    parts = re.split(r"[\n,]+", raw)
    return [p.strip() for p in parts if p and p.strip()]


@lru_cache(maxsize=2)
def _load_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Load a local SentenceTransformer model.

    Raises:
        ImportError: if sentence-transformers is not installed.
    """
    from sentence_transformers import SentenceTransformer  # type: ignore
    return SentenceTransformer(model_name)


def compute_query_similarity_scores(
    content_text: str,
    queries: List[str],
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> List[Tuple[str, float]]:
    """
    Compute cosine similarity between each query embedding and a single content embedding.

    Returns:
        List of (query, score) pairs in the same order as `queries`.
    """
    if not content_text or not queries:
        return []

    model = _load_model(model_name)

    # Encode content + queries in one batch
    vectors = model.encode([content_text] + queries, show_progress_bar=False)

    import numpy as np  # local import to keep module light for non-embedding paths

    vectors = np.asarray(vectors, dtype=np.float32)

    # L2 normalise for cosine similarity via dot product
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    vectors = vectors / norms

    content_vec = vectors[0]
    query_vecs = vectors[1:]
    scores = (query_vecs @ content_vec).tolist()

    return list(zip(queries, [float(s) for s in scores]))


def format_semantic_scores(scored: Iterable[Tuple[str, float]]) -> str:
    """
    Format scores for insertion into the Word template placeholder.

    Example:
        Query embeddings (score):
        query 1 (0.7365), query 2 (0.7867)
    """
    scored_list = list(scored)
    if not scored_list:
        return "Query embeddings (score):\n"
    joined = ", ".join(f"{q} ({score:.4f})" for q, score in scored_list)
    return "Query embeddings (score):\n" + joined
