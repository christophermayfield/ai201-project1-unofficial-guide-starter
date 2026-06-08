"""Similarity search over embedded chunks."""

from __future__ import annotations

from dataclasses import dataclass

from pipeline.config import TOP_K
from pipeline.vector_store import get_collection


@dataclass
class RetrievedChunk:
    chunk_id: str
    source: str
    chunk_index: int
    text: str
    distance: float


def retrieve(query: str, top_k: int = TOP_K) -> list[RetrievedChunk]:
    """Find the most relevant chunks for a user question."""
    collection = get_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    return [
        RetrievedChunk(
            chunk_id=chunk_id,
            source=metadata["source"],
            chunk_index=metadata["chunk_index"],
            text=text,
            distance=distance,
        )
        for chunk_id, text, metadata, distance in zip(
            ids, documents, metadatas, distances
        )
    ]
