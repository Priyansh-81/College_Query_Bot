
import ollama
from app.config import emb_model


class EmbeddingModel:
    def __init__(self):
        self.model = emb_model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        cleaned_texts = [text.strip() for text in texts]

        if any(not text for text in cleaned_texts):
            raise ValueError("Texts must not contain empty strings.")

        all_embeddings = []
        batch_size = 8

        try:
            for start in range(0, len(cleaned_texts), batch_size):
                batch = cleaned_texts[start:start + batch_size]

                print(
                    f"Embedding batch: "
                    f"{start + 1}-{start + len(batch)} "
                    f"of {len(cleaned_texts)} chunks"
                )

                response = ollama.embed(
                    model=self.model,
                    input=batch,
                )

                all_embeddings.extend(response.embeddings)

        except ollama.ResponseError as e:
            raise RuntimeError(
                f"Error generating embeddings: {e}"
            ) from e

        if len(all_embeddings) != len(cleaned_texts):
            raise RuntimeError(
                "Mismatch between number of embeddings and input texts."
            )

        if any(not embedding for embedding in all_embeddings):
            raise RuntimeError("An empty embedding was returned.")

        dimensions = len(all_embeddings[0])

        if any(
            len(embedding) != dimensions
            for embedding in all_embeddings
        ):
            raise RuntimeError(
                "Embedding vectors have inconsistent dimensions."
            )

        return all_embeddings
