"""ChromaDB vector store for chunk embeddings."""

from __future__ import annotations

import chromadb

from pipeline.config import CHROMA_COLLECTION, CHROMA_PATH
from pipeline.embeddings import get_embedding_function

_client: chromadb.PersistentClient | None = None
_collection: chromadb.Collection | None = None


def get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client


def get_collection() -> chromadb.Collection:
    """Return the ChromaDB collection, creating it if needed."""
    global _collection
    if _collection is None:
        _collection = get_client().get_or_create_collection(
            name=CHROMA_COLLECTION,
            embedding_function=get_embedding_function(),
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def reset_collection() -> chromadb.Collection:
    """Delete and recreate the collection (use before re-indexing)."""
    global _collection
    client = get_client()
    try:
        client.delete_collection(CHROMA_COLLECTION)
    except ValueError:
        pass
    _collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )
    return _collection


def embed_and_store(chunks: list[dict]) -> int:
    """Embed chunk text and store vectors + metadata in ChromaDB."""
    collection = get_collection()
    collection.add(
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
                "token_count": chunk["token_count"],
            }
            for chunk in chunks
        ],
        ids=[chunk["chunk_id"] for chunk in chunks],
    )
    return collection.count()
