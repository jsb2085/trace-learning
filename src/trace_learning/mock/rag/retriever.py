"""Mock RAG retriever exposed as a LangChain tool."""

from __future__ import annotations

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from trace_learning.mock.rag.store import MockDocumentStore


class RAGQueryInput(BaseModel):
    query: str = Field(description="Natural-language question to retrieve context for")
    top_k: int = Field(default=3, description="Number of documents to return")


_store = MockDocumentStore()


class MockRAGRetriever:
    """Thin wrapper around the document store."""

    def __init__(self, store: MockDocumentStore | None = None) -> None:
        self._store = store or _store

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        return self._store.search(query, top_k=top_k)


def _rag_search(query: str, top_k: int = 3) -> list[dict]:
    retriever = MockRAGRetriever()
    results = retriever.retrieve(query, top_k=top_k)
    return [
        {"doc_id": d["id"], "title": d["title"], "body": d["body"]}
        for d in results
    ]


def get_rag_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=_rag_search,
        name="rag_search",
        description="Search the knowledge base and return relevant document chunks.",
        args_schema=RAGQueryInput,
    )
