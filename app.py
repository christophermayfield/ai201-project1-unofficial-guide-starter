#!/usr/bin/env python3
"""Gradio interface for the Prediction Markets RAG system.

Architecture (query phase):
  User Question -> Retrieval -> Generation -> Answer + Sources
"""

from __future__ import annotations

import gradio as gr

from pipeline.generation import answer_query
from pipeline.vector_store import get_collection

DOCUMENT_SOURCES = [
    "Prediction Market Accuracy In the Long Run",
    "Practical Experiments in Small Markets",
    "Extended Literature Review",
    "Prediction Markets: An Emerging Form of Gambling",
    "Distilling the Wisdom of Crowds",
    "Reproducibility of Scientific Research",
    "Political Prediction Markets",
    "Prediction Markets as a Public Health Threat",
    "Who Wins and Who Loses on Polymarket",
    "Real-Money vs Play-Money Prediction Markets",
]

EXAMPLE_QUESTIONS = [
    "What are prediction markets?",
    "What are the benefits of prediction markets?",
    "What are prediction polls?",
    "What is the wisdom of crowds?",
    "How are prediction markets a potential threat to democracy?",
]


def check_vector_store() -> None:
    collection = get_collection()
    count = collection.count()
    if count == 0:
        print(
            "\n⚠️  Vector store is empty. Run these commands before using the app:\n"
            "    python ingest_chunk.py\n"
            "    python build_index.py --reset\n"
        )
    else:
        print(f"Vector store ready ({count} chunks indexed).")


def chat(message: str, history) -> str:
    if not message.strip():
        return ""
    return answer_query(message)


with gr.Blocks() as demo:
    gr.HTML(
        """
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#1e3a5f; margin:0;">
                Prediction Markets Guide
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Ask questions about prediction markets — answers grounded in loaded research papers.
            </p>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            gr.ChatInterface(
                fn=chat,
                chatbot=gr.Chatbot(
                    height=440,
                    placeholder=(
                        "Ask a question about prediction markets to get started."
                    ),
                ),
                textbox=gr.Textbox(
                    placeholder='e.g. "What are prediction markets?"',
                    container=False,
                    scale=7,
                ),
                examples=EXAMPLE_QUESTIONS,
                cache_examples=False,
            )

        with gr.Column(scale=1, min_width=200):
            source_items = "".join(
                f"<li>{source}</li>" for source in DOCUMENT_SOURCES
            )
            gr.HTML(
                f"""
                <div style="background:#eff6ff; border:1px solid #bfdbfe;
                            border-radius:10px; padding:1rem; margin-top:0.5rem;">
                    <p style="font-size:0.8rem; font-weight:700; color:#1e3a5f;
                               margin:0 0 0.5rem; letter-spacing:0.05em;">
                        LOADED DOCUMENTS
                    </p>
                    <ul style="font-size:0.8rem; color:#1d4ed8; list-style:none;
                                padding:0; margin:0; line-height:1.7;">
                        {source_items}
                    </ul>
                    <hr style="border:none; border-top:1px solid #bfdbfe; margin:0.75rem 0;">
                    <p style="font-size:0.75rem; color:#2563eb; margin:0; line-height:1.5;">
                        Answers use retrieved document excerpts only.
                        Sources are listed automatically below each answer.
                    </p>
                </div>
                """
            )


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Prediction Markets Guide — starting up")
    print("=" * 50 + "\n")
    check_vector_store()
    demo.launch(theme=gr.themes.Soft(primary_hue="blue"))
