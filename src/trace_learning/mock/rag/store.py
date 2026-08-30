"""In-memory document store backing the mock RAG retriever."""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_DOCUMENTS_PATH = Path(__file__).resolve().parents[4] / "data" / "rag" / "documents.json"


class MockDocumentStore:
    """Simple keyword-indexed document store (no embeddings yet)."""

    def __init__(self, documents_path: Path | None = None) -> None:
        path = documents_path or DEFAULT_DOCUMENTS_PATH
        with path.open() as f:
            raw = json.load(f)
        self._documents: list[dict] = raw["documents"] if isinstance(raw, dict) else raw

    @property
    def documents(self) -> list[dict]:
        return self._documents

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Return documents whose title or body contain query tokens."""
        tokens = query.lower().split()
        scored: list[tuple[int, dict]] = []
        for doc in self._documents:
            haystack = f"{doc['title']} {doc['body']}".lower()
            score = sum(1 for t in tokens if t in haystack)
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]
