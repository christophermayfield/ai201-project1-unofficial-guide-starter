"""Grounded answer generation via Groq LLM."""

from __future__ import annotations

from dataclasses import dataclass

from groq import Groq

from pipeline.config import (
    GROQ_API_KEY,
    INSUFFICIENT_CONTEXT_MARKER,
    LLM_MODEL,
    MAX_DISTANCE,
)
from pipeline.retrieval import RetrievedChunk, retrieve

_client: Groq | None = None


@dataclass
class GenerationResult:
    answer: str
    sources: list[str]
    formatted_response: str
    chunks_used: int


def _get_client() -> Groq:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. Add it to your .env file."
            )
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def _filter_chunks(chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    return [chunk for chunk in chunks if chunk.distance <= MAX_DISTANCE]


def _build_context(chunks: list[RetrievedChunk]) -> str:
    parts: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        parts.append(
            f"[Excerpt {index} | {chunk.source} | chunk {chunk.chunk_index}]\n"
            f"{chunk.text}"
        )
    return "\n\n".join(parts)


def _build_sources(chunks: list[RetrievedChunk]) -> list[str]:
    """Build a deduplicated source list from retrieved chunk metadata."""
    seen: set[tuple[str, int]] = set()
    sources: list[str] = []

    for chunk in chunks:
        key = (chunk.source, chunk.chunk_index)
        if key in seen:
            continue
        seen.add(key)
        sources.append(f"{chunk.source} (chunk {chunk.chunk_index})")

    return sources


def _format_response(answer: str, sources: list[str]) -> str:
    if not sources:
        return answer

    source_lines = "\n".join(f"- {source}" for source in sources)
    return f"{answer}\n\n---\n**Sources:**\n{source_lines}"


def _build_system_prompt() -> str:
    return (
        "You are a prediction markets research assistant. "
        "You MUST answer using ONLY the document excerpts provided in the user message.\n\n"
        "Rules:\n"
        "1. Use only facts explicitly stated in the provided excerpts.\n"
        "2. Do NOT use outside knowledge, training data, or assumptions.\n"
        "3. Do NOT infer facts that are not supported by the excerpts.\n"
        f"4. If the excerpts do not contain enough information to answer the question, "
        f"respond with EXACTLY this sentence and nothing else:\n"
        f'"{INSUFFICIENT_CONTEXT_MARKER}"\n'
        "5. Do NOT include sources, citations, references, or a bibliography. "
        "Source attribution is handled separately by the application.\n"
        "6. Write a concise, direct answer in plain prose."
    )


def _build_user_prompt(query: str, context: str) -> str:
    return (
        "Answer the question using ONLY the excerpts below.\n\n"
        f"{context}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )


def generate_response(
    query: str,
    retrieved_chunks: list[RetrievedChunk] | None = None,
) -> GenerationResult:
    """Generate a grounded answer and attach sources programmatically."""
    chunks = _filter_chunks(retrieved_chunks or retrieve(query))

    if not chunks:
        return GenerationResult(
            answer=INSUFFICIENT_CONTEXT_MARKER,
            sources=[],
            formatted_response=INSUFFICIENT_CONTEXT_MARKER,
            chunks_used=0,
        )

    context = _build_context(chunks)
    sources = _build_sources(chunks)

    response = _get_client().chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": _build_system_prompt()},
            {"role": "user", "content": _build_user_prompt(query, context)},
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content.strip()
    return GenerationResult(
        answer=answer,
        sources=sources,
        formatted_response=_format_response(answer, sources),
        chunks_used=len(chunks),
    )


def answer_query(query: str) -> str:
    """End-to-end RAG: retrieve, generate, return formatted answer + sources."""
    return generate_response(query).formatted_response
