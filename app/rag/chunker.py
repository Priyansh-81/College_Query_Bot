
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

