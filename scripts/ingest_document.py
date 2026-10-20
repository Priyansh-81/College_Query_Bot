from app.rag.ingestion import ingest_pdf
from pathlib import Path

path_to_pdf = Path("data/documents/colleage_rules.pdf")

if not path_to_pdf.exists():
    raise FileNotFoundError(f"The specified PDF file does not exist: {path_to_pdf}")

number_of_chunks = ingest_pdf(path_to_pdf, chunk_size=1000, overlap=150)
print(f"Successfully ingested {number_of_chunks} chunks from the PDF: {path_to_pdf.name}")