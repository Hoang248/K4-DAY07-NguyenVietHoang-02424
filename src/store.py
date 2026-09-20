from __future__ import annotations

from typing import Any, Callable

from .chunking import compute_similarity
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Stores records in memory for the lab.

    The embedding_fn parameter allows injection of mock or real embeddings.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._next_index = 0

    def _make_record(self, doc: Document) -> dict[str, Any]:
        metadata = dict(doc.metadata or {})
        # Keep the document id in metadata as well as at the top level so
        # filters and delete_document work for every ingested chunk.
        metadata.setdefault("doc_id", doc.id)
        record_id = f"{doc.id}::{self._next_index}"
        self._next_index += 1
        return {
            "id": doc.id,
            "record_id": record_id,
            "content": doc.content,
            "metadata": metadata,
            "embedding": list(self._embedding_fn(doc.content)),
        }

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        if top_k <= 0 or not records:
            return []
        query_embedding = list(self._embedding_fn(query))
        scored: list[dict[str, Any]] = []
        for record in records:
            result = {key: value for key, value in record.items() if key != "embedding"}
            result["score"] = compute_similarity(query_embedding, record["embedding"])
            scored.append(result)
        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.
        """
        for doc in docs:
            record = self._make_record(doc)
            self._store.append(record)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        For in-memory: compute dot product of query embedding vs all stored embeddings.
        """
        return self._search_records(query, self._store, top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        First filter stored chunks by metadata_filter, then run similarity search.
        """
        if not metadata_filter:
            return self.search(query, top_k=top_k)
        candidates = [
            record
            for record in self._store
            if all(record["metadata"].get(key) == value for key, value in metadata_filter.items())
        ]
        return self._search_records(query, candidates, top_k)

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        removed = [
            record
            for record in self._store
            if record["metadata"].get("doc_id") == doc_id
        ]
        if not removed:
            return False

        self._store = [
            record
            for record in self._store
            if record["metadata"].get("doc_id") != doc_id
        ]
        return True
