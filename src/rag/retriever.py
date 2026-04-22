import chromadb
from chromadb.config import Settings

class SimpleRetriever:
    def __init__(self, collection_name: str = "ml_tutor_notes") -> None:
        from src.rag.embedder import Embedder

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

    def retrieve(self, query: str, top_k: int = 1) -> list[str]:
        query_embedding = self.embedder.encode_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        docs = results.get("documents", [[]])
        return docs[0] if docs else []