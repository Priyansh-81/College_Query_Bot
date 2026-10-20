
from app.config import chroma_dir, collection_name
import chromadb

client = chromadb.PersistentClient(
    path=str(chroma_dir)
)

client.delete_collection(name=collection_name)

print(f"Deleted collection: {collection_name}")

client.get_or_create_collection(
    name=collection_name,
    metadata={"hnsw:space": "cosine"},
)

print("Created a fresh, empty collection.")
