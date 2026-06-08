#!/usr/bin/env python3
"""Query phase: run similarity search over the vector store.

Architecture:
  User Question
    -> Vector Store (similarity search)
    -> Retrieval (top-k relevant chunks)

Examples:

    python query_retrieval.py "what are prediction markets?"
    python query_retrieval.py --top-k 5 "what is the wisdom of crowds?"
"""

from __future__ import annotations

import argparse
import sys

from pipeline.config import TOP_K
from pipeline.retrieval import retrieve


def print_results(query: str, top_k: int) -> None:
    results = retrieve(query, top_k=top_k)

    if not results:
        print("No results. Run `python build_index.py` first.")
        return

    print(f"Query: {query}\n")
    for rank, chunk in enumerate(results, start=1):
        preview = chunk.text[:300] + ("..." if len(chunk.text) > 300 else "")
        print(f"--- Result {rank} (distance: {chunk.distance:.4f}) ---")
        print(f"Source: {chunk.source} (chunk {chunk.chunk_index})")
        print(preview)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve relevant chunks for a query.")
    parser.add_argument("query", help="Question to search for")
    parser.add_argument(
        "--top-k",
        type=int,
        default=TOP_K,
        help=f"Number of chunks to retrieve (default: {TOP_K})",
    )
    args = parser.parse_args()

    if not args.query.strip():
        print("Query cannot be empty.", file=sys.stderr)
        sys.exit(1)

    print_results(args.query, args.top_k)


if __name__ == "__main__":
    main()
