"""Embedding model for converting text chunks to vectors."""

from __future__ import annotations

from functools import lru_cache

from chromadb.utils import embedding_functions

from pipeline.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_function() -> embedding_functions.SentenceTransformerEmbeddingFunction:
    """Return the sentence-transformers embedding function used by ChromaDB."""
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )
