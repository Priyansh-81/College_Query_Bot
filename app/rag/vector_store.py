
import chromadb

from app.config import (
    chroma_dir,
    collection_name as default_collection_name,
    top_k,
)


class VectorStore:
    def __init__(self,persist_directory: str = str(chroma_dir),collection_name: str = default_collection_name,):
        self.client = chromadb.PersistentClient(
            path=str(persist_directory),
            settings=chromadb.config.Settings(
                anonymized_telemetry=False,
            ),
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        ids: list[str] | None = None,
    ) -> None:
        if not chunks:
            return

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match the number of embeddings."
            )

        if any(not chunk.strip() for chunk in chunks):
            raise ValueError("Chunks must not contain empty strings.")

        if any(not embedding for embedding in embeddings):
            raise ValueError("Embeddings must not be empty.")

        dimensions = len(embeddings[0])

        if any(len(vector) != dimensions for vector in embeddings):
            raise ValueError(
                "Embedding vectors have inconsistent dimensions."
            )

        if ids is None:
            start = self.collection.count()
            ids = [
                f"chunk_{start + index}"
                for index in range(len(chunks))
            ]

        if len(ids) != len(chunks):
            raise ValueError(
                "Number of IDs must match the number of chunks."
            )

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
        )

    def search(self,query_embedding: list[float],n_results: int = top_k,) -> list[dict]:
        if not query_embedding:
            raise ValueError("Query embedding must not be empty.")

        if n_results <= 0:
            raise ValueError("n_results must be positive.")

        count = self.collection.count()

        if count == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, count),
            include=["documents", "distances"],
        )

        matches = []

        for index, document in enumerate(results["documents"][0]):
            matches.append(
                {
                    "id": results["ids"][0][index],
                    "text": document,
                    "distance": results["distances"][0][index],
                }
            )

        return matches
