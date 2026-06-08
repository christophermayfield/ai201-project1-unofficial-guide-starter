"""Shared configuration for the RAG pipeline."""

from __future__ import annotations

import os
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
MAX_DISTANCE = 0.5

# Generation (Groq — https://console.groq.com)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"
INSUFFICIENT_CONTEXT_MARKER = (
    "I could not find enough information in the loaded documents to answer that question."
)

# Paths
CHUNKS_PATH = PROJECT_ROOT / "data" / "chunks.json"
CHROMA_PATH = str(PROJECT_ROOT / "chroma_db")
CHROMA_COLLECTION = "prediction_markets"
