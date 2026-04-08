from __future__ import annotations

from typing import Iterable

import faiss
import numpy as np


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Split text into overlapping character chunks for a simple teaching example."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap cannot be negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        chunks.append(cleaned[start:end].strip())
        if end == len(cleaned):
            break
        start = end - overlap

    return chunks


def package_chunks(chunks: Iterable[str], source_file: str) -> list[dict]:
    """Attach simple metadata to each chunk for retrieval demos."""
    return [
        {"chunk_id": idx, "source_file": source_file, "text": chunk}
        for idx, chunk in enumerate(chunks)
    ]


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Build a simple exact FAISS index over float32 embeddings."""
    matrix = np.asarray(embeddings, dtype="float32")
    if matrix.ndim != 2:
        raise ValueError("embeddings must be a 2D array")

    index = faiss.IndexFlatL2(matrix.shape[1])
    index.add(matrix)
    return index


def search_index(
    index: faiss.IndexFlatL2, query_embedding: np.ndarray, top_k: int = 3
) -> tuple[np.ndarray, np.ndarray]:
    """Return distances and indices for the nearest chunks."""
    vector = np.asarray(query_embedding, dtype="float32")
    if vector.ndim == 1:
        vector = vector.reshape(1, -1)
    return index.search(vector, top_k)


def build_grounded_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    """Create a simple grounded prompt using retrieved chunk text."""
    sources = []
    for chunk in retrieved_chunks:
        sources.append(
            f"[{chunk['source_file']} | chunk {chunk['chunk_id']}] {chunk['text']}"
        )

    joined_sources = "\n\n".join(sources)
    return (
        "Answer the question using only the retrieved context below. "
        "If the answer is not in the context, say you do not have enough information.\n\n"
        f"Question: {question}\n\n"
        f"Retrieved context:\n{joined_sources}\n"
    )
