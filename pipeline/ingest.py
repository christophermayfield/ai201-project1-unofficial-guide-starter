"""Document loading and text cleaning for the RAG pipeline."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


@dataclass
class Document:
    source: str
    text: str


def clean_text(text: str) -> str:
    """Normalize raw document text before chunking."""
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Rejoin words split across line breaks in PDFs: "predic-\ntion" -> "prediction"
    text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)
    text = re.sub(r"[^\S\n]+", " ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _load_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _load_pdf_file(path: Path) -> str:
    import pdfplumber

    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                pages.append(page_text)
    return "\n\n".join(pages)


def load_document(path: Path) -> Document:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        raw_text = _load_text_file(path)
    elif suffix == ".pdf":
        raw_text = _load_pdf_file(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    return Document(source=path.name, text=clean_text(raw_text))


def load_documents(documents_dir: Path) -> list[Document]:
    """Load and clean all supported documents from a directory."""
    if not documents_dir.is_dir():
        raise FileNotFoundError(f"Documents directory not found: {documents_dir}")

    paths = sorted(
        path
        for path in documents_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    documents: list[Document] = []
    for path in paths:
        document = load_document(path)
        if document.text:
            documents.append(document)
        else:
            print(f"Skipping empty document: {path.name}")

    return documents
