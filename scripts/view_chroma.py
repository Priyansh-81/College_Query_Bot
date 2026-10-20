
import chromadb

from app.config import chroma_dir, collection_name

client = chromadb.PersistentClient(path=str(chroma_dir))

collection = client.get_or_create_collection(
    name=collection_name
)

print("Collection:", collection.name)
print("Total entries:", collection.count())

results = collection.get(
    include=["documents", "metadatas", "embeddings"]
)

for i, entry_id in enumerate(results["ids"]):
    print(f"\nEntry {i + 1}")
    print("ID:", entry_id)
    print("Document:", results["documents"][i])
    print("Metadata:", results["metadatas"][i])

    embedding = results["embeddings"][i]
    if embedding is not None:
        print("Embedding dimensions:", len(embedding))
        print("First five values:", embedding[:5])
