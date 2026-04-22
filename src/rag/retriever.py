import math

from src.rag.embedder import Embedder


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SimpleRetriever:
    def __init__(self, collection_name: str = "ml_tutor_notes") -> None:
        self.embedder = Embedder()
        self._chunks: list[str] = []
        self._embeddings: list[list[float]] = []

    def add_chunks(self, chunks: list[str]) -> None:
        if not chunks:
            return
        self._chunks = chunks
        self._embeddings = self.embedder.encode_documents(chunks)

    def retrieve(self, query: str, top_k: int = 3, max_distance: float = 2.0) -> list[str]:
        if not self._chunks:
            return []

        query_embedding = self.embedder.encode_query(query)
        scores = [
            _cosine_similarity(query_embedding, emb)
            for emb in self._embeddings
        ]

        ranked = sorted(
            zip(scores, self._chunks),
            key=lambda x: x[0],
            reverse=True,
        )

        return [chunk for score, chunk in ranked[:top_k] if score > 0.1]
