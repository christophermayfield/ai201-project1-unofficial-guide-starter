"""Shared configuration for the RAG pipeline."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Chunking (see planning.md)
CHUNK_SIZE = 400
OVERLAP = 50

# Embedding + retrieval (see planning.md)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 10

# Paths
CHUNKS_PATH = PROJECT_ROOT / "data" / "chunks.json"
CHROMA_PATH = str(PROJECT_ROOT / "chroma_db")
CHROMA_COLLECTION = "prediction_markets"
