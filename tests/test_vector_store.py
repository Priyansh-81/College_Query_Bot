
import tempfile
import unittest

from app.rag.vector_store import VectorStore


class TestVectorStore(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.store = VectorStore(
            persist_directory=self.temp_dir.name,
            collection_name="test_college_knowledge",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_search(self):
        chunks = [
            "The college library closes at 8 PM.",
            "Hostel applications open in June.",
            "The examination office handles hall tickets.",
        ]

        # Small illustrative vectors for testing ChromaDB.
        # Real embeddings will come from nomic-embed-text.
        embeddings = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]

        self.store.add_chunks(
            chunks,
            embeddings,
            ids=["library", "hostel", "exams"],
        )

        results = self.store.search(
            query_embedding=[0.99, 0.01, 0.0],
            n_results=2,
        )

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "library")
        self.assertIn("library closes", results[0]["text"])

    def test_empty_search(self):
        results = self.store.search([1.0, 0.0, 0.0])
        self.assertEqual(results, [])

    def test_mismatched_input_lengths(self):
        with self.assertRaises(ValueError):
            self.store.add_chunks(
                ["A college rule"],
                [[1.0, 0.0], [0.0, 1.0]],
            )


if __name__ == "__main__":
    unittest.main()
