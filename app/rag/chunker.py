
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    if not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and less than chunk size.")

    text = text.strip()
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_pages(pages: list[dict],chunk_size: int = 1000,overlap: int = 150,) -> list[dict]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and less than chunk size.")

    chunks = []

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        page_number = page["page_number"]
        start = 0

        while start < len(text):
            chunk = text[start:start + chunk_size].strip()

            if chunk:
                chunks.append({"page_number": page_number,"text": chunk,})

            start += chunk_size - overlap

    return chunks

