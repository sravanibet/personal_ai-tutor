import chromadb
from chromadb.config import Settings

from src.rag.embedder import Embedder


class SimpleRetriever:
    def __init__(self, collection_name: str = "ml_tutor_notes") -> None:
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = Embedder()

    def add_chunks(self, chunks: list[str]) -> None:
        if not chunks:
            return

        existing = self.collection.get()
        if existing and existing.get("ids"):
            self.collection.delete(ids=existing["ids"])

        embeddings = self.embedder.encode_documents(chunks)
        ids = [f"chunk_{i}" for i in range(len(chunks))]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
        )

    def retrieve(self, query: str, top_k: int = 1, max_distance: float = 1.2) -> list[str]:
        query_embedding = self.embedder.encode_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "distances"],
        )

        docs = results.get("documents", [[]])
        distances = results.get("distances", [[]])

        if not docs or not docs[0]:
            return []

        filtered_docs = []
        for doc, distance in zip(docs[0], distances[0]):
            if distance is not None and distance <= max_distance:
                filtered_docs.append(doc)

        return filtered_docs