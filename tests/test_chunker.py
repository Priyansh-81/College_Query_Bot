
import unittest

from app.rag.chunker import chunk_text


class TestChunker(unittest.TestCase):

    def test_empty_text(self):
        self.assertEqual(chunk_text("   "), [])

    def test_short_text(self):
        text = "College helpdesk information."
        self.assertEqual(chunk_text(text), [text])

    def test_long_text(self):
        text = "A" * 2000
        chunks = chunk_text(text, chunk_size=1000, overlap=150)

        self.assertEqual(len(chunks), 3)
        self.assertEqual(len(chunks[0]), 1000)
        self.assertEqual(len(chunks[1]), 1000)
        self.assertEqual(len(chunks[2]), 300)

    def test_invalid_overlap(self):
        with self.assertRaises(ValueError):
            chunk_text("Some text", chunk_size=100, overlap=100)


if __name__ == "__main__":
    unittest.main()
