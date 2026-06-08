#!/usr/bin/env python3
"""Indexing phase: embed chunks and store them in ChromaDB.

Architecture:
  Text Chunks (data/chunks.json)
    -> Embedding Model (all-MiniLM-L6-v2)
    -> Vector Store (ChromaDB)

Run after ingest_chunk.py:

    python build_index.py

To rebuild after changing chunks, pass --reset:

    python build_index.py --reset
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pipeline.config import CHUNKS_PATH
from pipeline.vector_store import embed_and_store, get_collection, reset_collection


def load_chunks(chunks_path: Path = CHUNKS_PATH) -> list[dict]:
    if not chunks_path.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {chunks_path}\n"
            "Run `python ingest_chunk.py` first."
        )

    payload = json.loads(chunks_path.read_text(encoding="utf-8"))
    return payload["chunks"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Embed chunks and store in ChromaDB.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear the existing vector store before indexing.",
    )
    args = parser.parse_args()

    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_PATH}")

    collection = get_collection()
    if collection.count() > 0 and not args.reset:
        print(
            f"Vector store already has {collection.count()} chunks. "
            "Use --reset to rebuild."
        )
        return

    if args.reset and collection.count() > 0:
        print("Resetting vector store...")
        reset_collection()

    print("Embedding chunks with all-MiniLM-L6-v2 and storing in ChromaDB...")
    total = embed_and_store(chunks)
    print(f"Indexing complete. {total} chunks stored in chroma_db/")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
