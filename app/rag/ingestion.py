# from pathlib import Path
# from app.rag.loader import load_pdf
# from app.rag.chunker import chunk_text
# from app.rag.embeddings import EmbeddingModel
# from app.rag.vector_store import VectorStore


# def ingest_pdf(file_path:str|Path, chunk_size:int=1000, overlap:int=150)->int:
#     extracted_text=load_pdf(file_path)
#     if not extracted_text.strip():
#         raise ValueError(f"No text extracted from the PDF: {file_path}")

#     chunks=chunk_text(extracted_text, chunk_size=chunk_size, overlap=overlap)

#     if not chunks:
#         raise ValueError(f"No chunks created from the extracted text of the PDF: {file_path}")

#     embedding_model=EmbeddingModel()
#     embedding=embedding_model.embed_texts(chunks)

#     vs=VectorStore()
#     document_name=Path(file_path).stem
#     ids=[f"{document_name}_{i}" for i in range(len(chunks))]

#     vs.add_chunks(chunks=chunks, embeddings=embedding, ids=ids)

#     return len(chunks)


from pathlib import Path

from app.rag.loader import load_pdf_pages
from app.rag.chunker import chunk_pages
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore


def ingest_pdf(file_path: str | Path,chunk_size: int = 1000,overlap: int = 150,) -> int:
    pages = load_pdf_pages(file_path)
    if not pages:
        raise ValueError(f"No extractable text found in PDF: {file_path}")

    chunks = chunk_pages(pages,chunk_size=chunk_size,overlap=overlap,)

    if not chunks:
        raise ValueError("No text chunks were generated.")

    embedding_model = EmbeddingModel()
    embeddings = embedding_model.embed_texts([chunk["text"] for chunk in chunks])

    vector_store = VectorStore()

    document_name = Path(file_path).stem

    ids = [
        f"{document_name}_p{chunk['page_number']}_c{index}"
        for index, chunk in enumerate(chunks)
    ]

    metadatas = [
        {
            "source": Path(file_path).name,
            "page_number": chunk["page_number"],
        }
        for chunk in chunks
    ]

    vector_store.add_chunks(
        chunks=[chunk["text"] for chunk in chunks],
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas,
    )

    return len(chunks)
