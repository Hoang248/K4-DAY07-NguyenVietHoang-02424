"""Benchmark retrieval strategies on the L3B ecommerce corpus.

The benchmark intentionally keeps chunking outside EmbeddingStore so that each
chunk carries the source document metadata and can be filtered by audience.
Run, for example:

    python bench.py --strategy recursive --embedding lexical
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv

from src import (
    Document,
    EmbeddingStore,
    FixedSizeChunker,
    GeminiEmbedder,
    MockEmbedder,
    RecursiveChunker,
    SentenceChunker,
)


ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "data" / "etsy-policies"
load_dotenv(dotenv_path=ROOT / ".env", override=False)


BENCHMARKS = [
    {
        "id": "Q1",
        "question_type": "condition",
        "query": "What conditions must be met before a buyer can open a case on Etsy?",
        "gold": "To open a case, the estimated delivery date for the order must have passed and at least 48 hours must have passed since the buyer sent the seller a Help with order request.",
        "gold_doc_ids": ["buyer-estimated-delivery", "buyer-open-case"],
        "must_contain": "48 hours",
        "metadata_filter": {"audience": "buyer"},
    },
    {
        "id": "Q2",
        "question_type": "procedure",
        "query": "How does a seller work with a buyer to resolve an open Etsy case through Shop Manager?",
        "gold": "The seller uses Cases in Shop Manager, selects the applicable case, and communicates through Add Your Comment in the case log.",
        "gold_doc_ids": ["seller-resolve-case"],
        "must_contain": "Shop Manager",
        "metadata_filter": {"audience": "seller"},
    },
    {
        "id": "Q3",
        "question_type": "list",
        "query": "How much refund does Etsy Purchase Protection provide for a qualifying order?",
        "gold": "Etsy’s Purchase Protection program provides a full refund for qualifying orders when an item doesn’t arrive, arrives damaged, arrives 7+ days after the maximum estimated delivery date window provided at checkout, or differs significantly from the item description or photos.",
        "gold_doc_ids": ["buyer-purchase-protection"],
        "must_contain": "full refund",
        "metadata_filter": {"audience": "buyer"},
        "contrast_filter": {"audience": "seller"},
    },
    {
        "id": "Q4",
        "question_type": "formula",
        "query": "Which components are used to calculate an Etsy estimated delivery date?",
        "gold": "Processing time plus carrier transit time equals the estimated delivery date.",
        "gold_doc_ids": ["buyer-estimated-delivery"],
        "must_contain": "carrier transit time",
        "metadata_filter": {"audience": "buyer"},
    },
    {
        "id": "Q5",
        "question_type": "numeric + procedure",
        "query": "How can a seller issue a full or partial refund, and what is the Etsy Payments time limit?",
        "gold": "The seller uses Shop Manager to issue the refund; Etsy Payments refunds can be issued after processing and before 180 days have passed.",
        "gold_doc_ids": ["seller-issue-refund"],
        "must_contain": "180 days",
        "metadata_filter": {"audience": "seller"},
    },
]


def _parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    raw = path.read_text(encoding="utf-8")
    parts = raw.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$", line.strip())
        if not match:
            continue
        value = match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        metadata[match.group(1)] = value
    return metadata, parts[2].strip()


class HeadingChunker:
    """Keep Markdown sections intact and retain the heading on split pieces."""

    _heading = re.compile(r"(?m)^(#{1,6}\s+.+?)\s*$")

    def __init__(self, chunk_size: int = 650) -> None:
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []
        matches = list(self._heading.finditer(text))
        if not matches:
            return RecursiveChunker(chunk_size=self.chunk_size).chunk(text)

        sections: list[str] = []
        if matches[0].start() > 0 and text[: matches[0].start()].strip():
            sections.append(text[: matches[0].start()].strip())
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            sections.append(text[match.start() : end].strip())

        chunks: list[str] = []
        for section in sections:
            # A document title by itself is not an answer-bearing chunk.  Do
            # not let it consume a top-k slot; the actual sections retain
            # their own headings below.
            section_lines = section.splitlines()
            if len(section_lines) == 1 and section_lines[0].lstrip().startswith("#"):
                continue
            if len(section) <= self.chunk_size:
                chunks.append(section)
                continue

            lines = section.splitlines()
            heading = lines[0].strip() if lines and lines[0].lstrip().startswith("#") else ""
            body = "\n".join(lines[1:]).strip() if heading else section
            prefix = f"{heading}\n\n" if heading else ""
            child_size = max(1, self.chunk_size - len(prefix))
            children = RecursiveChunker(chunk_size=child_size).chunk(body)
            chunks.extend(f"{prefix}{child}".strip() for child in children)
        return [chunk for chunk in chunks if chunk]


class TfidfEmbedder:
    """Small deterministic lexical embedder for an offline, meaningful demo."""

    _token = re.compile(r"\w+", re.UNICODE)

    def __init__(self, texts: list[str]) -> None:
        tokenized = [set(self._token.findall(text.lower())) for text in texts]
        document_frequency = Counter(token for tokens in tokenized for token in tokens)
        self.vocabulary = sorted(document_frequency)
        self.index = {token: index for index, token in enumerate(self.vocabulary)}
        document_count = max(1, len(tokenized))
        self.idf = {
            token: math.log((document_count + 1) / (frequency + 1)) + 1.0
            for token, frequency in document_frequency.items()
        }

    def __call__(self, text: str) -> list[float]:
        counts = Counter(self._token.findall(text.lower()))
        vector = [counts[token] * self.idf[token] for token in self.vocabulary]
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


class CachedEmbedder:
    """Persist API embeddings locally so repeated benchmark runs do not re-call the API."""

    def __init__(self, embedder, cache_path: Path) -> None:
        self.embedder = embedder
        self._backend_name = getattr(embedder, "_backend_name", "cached")
        self.cache_path = cache_path
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            loaded = json.loads(self.cache_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            loaded = {}
        self.cache: dict[str, list[float]] = loaded if isinstance(loaded, dict) else {}

    def __call__(self, text: str) -> list[float]:
        model = getattr(self.embedder, "model_name", self._backend_name)
        cache_key = hashlib.sha256(f"{model}\0{text}".encode("utf-8")).hexdigest()
        if cache_key not in self.cache:
            self.cache[cache_key] = self.embedder(text)
            self.cache_path.write_text(
                json.dumps(self.cache, ensure_ascii=False),
                encoding="utf-8",
            )
        return self.cache[cache_key]


def chunker_for(name: str):
    if name == "fixed":
        return FixedSizeChunker(chunk_size=650, overlap=65)
    if name == "recursive":
        return RecursiveChunker(chunk_size=650)
    if name == "sentence":
        return SentenceChunker(max_sentences_per_chunk=4)
    if name == "heading":
        return HeadingChunker(chunk_size=650)
    raise ValueError(f"Unknown strategy: {name}")


def load_chunk_documents(strategy: str) -> tuple[list[Document], dict[str, int]]:
    chunker = chunker_for(strategy)
    documents: list[Document] = []
    counts: dict[str, int] = {}
    for path in sorted(CORPUS_DIR.glob("*.md")):
        metadata, content = _parse_frontmatter(path)
        chunks = chunker.chunk(content)
        counts[path.stem] = len(chunks)
        for index, chunk in enumerate(chunks):
            chunk_metadata = {
                **metadata,
                "doc_id": path.stem,
                "file_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "chunk_index": str(index),
                "strategy": strategy,
            }
            documents.append(Document(id=f"{path.stem}#{index}", content=chunk, metadata=chunk_metadata))
    return documents, counts


def _snippet(text: str, limit: int = 180) -> str:
    return " ".join(text.split())[:limit]


def _run_query(
    store: EmbeddingStore,
    item: dict,
    metadata_filter: dict | None,
) -> list[dict]:
    if metadata_filter:
        return store.search_with_filter(
            item["query"], top_k=3, metadata_filter=metadata_filter
        )
    return store.search(item["query"], top_k=3)


def format_results(results: list[dict], must_contain: str) -> str:
    if not results:
        return "  (không có kết quả)"
    lines = []
    target = must_contain.casefold()
    for rank, result in enumerate(results, start=1):
        marker = "MATCH" if target in result["content"].casefold() else "--"
        lines.append(
            f"  {rank}. {marker} score={result['score']:.4f} "
            f"chunk={result['id']} doc_id={result['metadata'].get('doc_id')} "
            f"audience={result['metadata'].get('audience', 'unknown')} "
            f"| {_snippet(result['content'])}"
        )
    return "\n".join(lines)


def run(strategy: str, embedding: str) -> str:
    documents, counts = load_chunk_documents(strategy)
    if embedding == "lexical":
        embedder = TfidfEmbedder([document.content for document in documents])
    elif embedding == "gemini":
        embedder = CachedEmbedder(
            GeminiEmbedder(),
            ROOT / ".cache" / "gemini_embeddings.json",
        )
    else:
        embedder = MockEmbedder()
    store = EmbeddingStore(collection_name=f"ecommerce_{strategy}", embedding_fn=embedder)
    store.add_documents(documents)

    lines = [
        f"strategy={strategy}",
        f"embedding={embedding}",
        f"chunks={store.get_collection_size()}",
        "chunks_by_document=" + ", ".join(f"{key}:{value}" for key, value in counts.items()),
    ]
    for item in BENCHMARKS:
        results = _run_query(store, item, metadata_filter=item["metadata_filter"])
        marker = item["must_contain"].casefold()
        matching_chunks = [
            result["id"] for result in results if marker in result["content"].casefold()
        ]
        gold_in_top3 = any(result["metadata"].get("doc_id") in item["gold_doc_ids"] for result in results)
        lines.extend(
            [
                "",
                f"[{item['id']}] type={item['question_type']} {item['query']}",
                f"gold={item['gold']}",
                f"gold_source_files={','.join(f'{doc_id}.md' for doc_id in item['gold_doc_ids'])}",
                f"answer_marker={item['must_contain']}",
                f"metadata_filter={item['metadata_filter']}",
                f"gold_doc_in_top3={gold_in_top3} answer_span_in_top3={bool(matching_chunks)}",
                f"matching_chunks={matching_chunks or ['(none)']}",
                "top3:",
                format_results(results, item["must_contain"]),
            ]
        )
        if item["metadata_filter"]:
            unfiltered = _run_query(store, item, metadata_filter=None)
            unfiltered_matching_chunks = [
                result["id"] for result in unfiltered if marker in result["content"].casefold()
            ]
            lines.extend(
                [
                    "A/B without metadata filter:",
                    f"gold_doc_in_top3={any(result['metadata'].get('doc_id') in item['gold_doc_ids'] for result in unfiltered)} "
                    f"answer_span_in_top3={bool(unfiltered_matching_chunks)}",
                    f"matching_chunks={unfiltered_matching_chunks or ['(none)']}",
                    format_results(unfiltered, item["must_contain"]),
                ]
            )
            if item.get("contrast_filter"):
                contrast = _run_query(store, item, metadata_filter=item["contrast_filter"])
                contrast_matching_chunks = [
                    result["id"] for result in contrast if marker in result["content"].casefold()
                ]
                lines.extend(
                    [
                        f"A/B contrast metadata filter={item['contrast_filter']}:",
                        f"gold_doc_in_top3={any(result['metadata'].get('doc_id') in item['gold_doc_ids'] for result in contrast)} "
                        f"answer_span_in_top3={bool(contrast_matching_chunks)}",
                        f"matching_chunks={contrast_matching_chunks or ['(none)']}",
                        format_results(contrast, item["must_contain"]),
                    ]
                )
    return "\n".join(lines) + "\n"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Run the L3B retrieval benchmark")
    parser.add_argument(
        "--strategy",
        choices=["heading", "fixed", "recursive", "sentence"],
        default="recursive",
    )
    parser.add_argument(
        "--embedding",
        choices=["lexical", "mock", "gemini"],
        default="lexical",
    )
    args = parser.parse_args()
    print(run(args.strategy, args.embedding), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
