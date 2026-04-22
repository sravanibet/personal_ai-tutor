from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer


class Embedder:
    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self._is_fitted = False

    def encode_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            self._is_fitted = False
            return []

        matrix = self.vectorizer.fit_transform(texts)
        self._is_fitted = True
        return matrix.toarray().tolist()

    def encode_query(self, query: str) -> list[float]:
        if not self._is_fitted:
            return []

        matrix = self.vectorizer.transform([query])
        return matrix.toarray()[0].tolist()