"""Token-based text chunking for the RAG pipeline."""

from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from pipeline.config import CHUNK_SIZE, EMBEDDING_MODEL, OVERLAP


@lru_cache(maxsize=1)
def _get_tokenizer():
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model.tokenizer


def count_tokens(text: str) -> int:
    tokenizer = _get_tokenizer()
    return len(tokenizer.encode(text, add_special_tokens=False))


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks measured in tokens.

    Uses the all-MiniLM-L6-v2 tokenizer so chunk boundaries align with the
    embedding model used later in the pipeline.
    """
    if not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    tokenizer = _get_tokenizer()
    tokens = tokenizer.encode(text, add_special_tokens=False)

    if len(tokens) <= chunk_size:
        return [text.strip()]

    chunks: list[str] = []
    start = 0
    step = chunk_size - overlap

    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(tokenizer.decode(chunk_tokens).strip())

        if end >= len(tokens):
            break
        start += step

    return chunks
