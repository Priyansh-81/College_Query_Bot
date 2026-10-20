
import unittest

from app.rag.embeddings import EmbeddingModel


class TestEmbeddingModel(unittest.TestCase):
    def test_empty_input(self):
        model = EmbeddingModel()
        self.assertEqual(model.embed_texts([]), [])

    def test_embed_texts(self):
        model = EmbeddingModel()

        texts = [
            "The college library closes at 8 PM.",
            "Students can apply for hostel accommodation.",
        ]

        embeddings = model.embed_texts(texts)

        self.assertEqual(len(embeddings), len(texts))
        self.assertTrue(all(len(vector) > 0 for vector in embeddings))
        self.assertEqual(
            len(embeddings[0]),
            len(embeddings[1]),
        )

        print("Number of embeddings:", len(embeddings))
        print("Vector dimensions:", len(embeddings[0]))
        print("First five values:", embeddings[0][:5])


if __name__ == "__main__":
    unittest.main()
