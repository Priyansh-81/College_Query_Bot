
import tempfile
import unittest
from pathlib import Path

import pymupdf

from app.rag.loader import load_pdf


class TestPDFLoader(unittest.TestCase):

    def test_load_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "sample.pdf"

            with pymupdf.open() as document:
                page = document.new_page()
                page.insert_text(
                    (72, 72),
                    "The examination fee is 500 rupees."
                )
                document.save(pdf_path)

            text = load_pdf(pdf_path)

            self.assertIn("examination fee", text.lower())
            self.assertIn("500 rupees", text.lower())

    def test_missing_pdf(self):
        with self.assertRaises(FileNotFoundError):
            load_pdf("missing_file.pdf")


if __name__ == "__main__":
    unittest.main()
