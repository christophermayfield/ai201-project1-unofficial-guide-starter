#!/usr/bin/env python3
"""Load documents, clean them, and produce token-based chunks.

Chunk size and overlap match planning.md:
  - 400 tokens per chunk
  - 50 token overlap

Set DOCUMENTS_DIR in .env to the folder containing your source PDFs/text files,
then run:

    python ingest_chunk.py
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from dotenv import load_dotenv

from pipeline.chunking import chunk_text, count_tokens
from pipeline.config import CHUNK_SIZE, OVERLAP
from pipeline.ingest import load_documents

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DOCUMENTS_DIR = Path.home() / "Desktop" / "Prediction Markets"
DOCUMENTS_DIR = Path(
    os.getenv("DOCUMENTS_DIR", DEFAULT_DOCUMENTS_DIR)
).expanduser()
OUTPUT_PATH = PROJECT_ROOT / "data" / "chunks.json"


@dataclass
class ChunkRecord:
    chunk_id: str
    source: str
    chunk_index: int
    text: str
    token_count: int


def build_chunks(documents_dir: Path = DOCUMENTS_DIR) -> list[ChunkRecord]:
    documents = load_documents(documents_dir)
    records: list[ChunkRecord] = []

    for document in documents:
        chunks = chunk_text(document.text, chunk_size=CHUNK_SIZE, overlap=OVERLAP)
        for index, chunk in enumerate(chunks):
            records.append(
                ChunkRecord(
                    chunk_id=f"{document.source}::chunk_{index}",
                    source=document.source,
                    chunk_index=index,
                    text=chunk,
                    token_count=count_tokens(chunk),
                )
            )

    return records


def save_chunks(records: list[ChunkRecord], output_path: Path = OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "chunk_size": CHUNK_SIZE,
        "overlap": OVERLAP,
        "chunk_count": len(records),
        "chunks": [asdict(record) for record in records],
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    print(f"Loading documents from {DOCUMENTS_DIR}")
    records = build_chunks()

    if not records:
        print(
            f"No chunks produced. Add .pdf, .txt, or .md files to {DOCUMENTS_DIR} "
            "and run again."
        )
        return

    save_chunks(records)
    print(f"Wrote {len(records)} chunks to {OUTPUT_PATH}")

    by_source: dict[str, int] = {}
    for record in records:
        by_source[record.source] = by_source.get(record.source, 0) + 1

    print("\nChunks per document:")
    for source, count in sorted(by_source.items()):
        print(f"  {source}: {count}")


if __name__ == "__main__":
    main()
