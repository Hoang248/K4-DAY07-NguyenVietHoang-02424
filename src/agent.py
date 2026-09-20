from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
<<<<<<< HEAD
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.store.search(question, top_k=top_k)
        if results:
            context = "\n\n".join(
                (
                    f"[Context {index}] doc_id={result['metadata'].get('doc_id', result['id'])} "
                    f"source={result['metadata'].get('source_url', result['metadata'].get('file_path', 'unknown'))}\n"
                    f"{result['content']}"
                )
                for index, result in enumerate(results, start=1)
            )
        else:
            context = "(No relevant context was retrieved.)"

        prompt = (
            "Answer the question using only the provided context. "
            "If the context does not contain the answer, say that the information "
            "is not available in the knowledge base.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )
        return self.llm_fn(prompt)
=======
        # TODO: store references to store and llm_fn
        pass

    def answer(self, question: str, top_k: int = 3) -> str:
        # TODO: retrieve chunks, build prompt, call llm_fn
        raise NotImplementedError("Implement KnowledgeBaseAgent.answer")
>>>>>>> e05a3a610f763dc292c285e48aff812c6b564639
