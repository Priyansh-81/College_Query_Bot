from pathlib import Path
from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore


def ingest_pdf(file_path:str|Path, chunk_size:int=1000, overlap:int=150)->int:
    extracted_text=load_pdf(file_path)
    if not extracted_text.strip():
        raise ValueError(f"No text extracted from the PDF: {file_path}")

    chunks=chunk_text(extracted_text, chunk_size=chunk_size, overlap=overlap)

    if not chunks:
        raise ValueError(f"No chunks created from the extracted text of the PDF: {file_path}")

    embedding_model=EmbeddingModel()
    embedding=embedding_model.embed_texts(chunks)

    vs=VectorStore()
    document_name=Path(file_path).stem
    ids=[f"{document_name}_{i}" for i in range(len(chunks))]

    vs.add_chunks(chunks=chunks, embeddings=embedding, ids=ids)

    return len(chunks)
