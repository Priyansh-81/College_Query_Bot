
import tempfile
import unittest
from pathlib import Path

import pymupdf

from app.rag.ingestion import ingest_pdf


class TestIngestion(unittest.TestCase):

    def test_ingest_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "college_rules.pdf"

            with pymupdf.open() as document:
                page = document.new_page()
                page.insert_text(
                    (72, 72),
                    "Students must register for examinations "
                    "before the published deadline."
                )
                document.save(pdf_path)

            chunks = ingest_pdf(pdf_path, chunk_size=50, overlap=10)

            self.assertGreater(len(chunks), 0)
            self.assertTrue(
                any("examinations" in chunk for chunk in chunks)
            )

    def test_empty_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "empty.pdf"

            with pymupdf.open() as document:
                document.new_page()
                document.save(pdf_path)

            with self.assertRaises(ValueError):
                ingest_pdf(pdf_path)


if __name__ == "__main__":
    unittest.main()
