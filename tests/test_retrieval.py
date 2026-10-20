from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore

embed=EmbeddingModel()
vs=VectorStore()

question="What are the eligibility requirements for undergraduate admissions at MAHE?"

query_emb=embed.embed_texts([question])[0]

results=vs.search(query_embedding=query_emb,n_results=4)

print(f"Question: {question}\nRetrieved Chunks:{len(results)} chunks\n")
print("Retrieved Chunks:")
for i,result in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(f"ID: {result['id']}")
    print(f"Distance: {result['distance']:.4f}")
    print(result["text"][:700])
    print()