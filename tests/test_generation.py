
from app.rag.query import Rag


rag_pipeline = Rag()

question ="How to reach MAHE?"


result = rag_pipeline.generate_response(question)

print("\nQuestion:")
print(result["question"])

print("\nAnswer:")
print(result["answer"])

print("\nRetrieved sources:")
for index, source in enumerate(result["sources"], start=1):
    print(f"\n--- Source {index} ---")
    print(f"ID: {source['id']}")
    print(f"Distance: {source['distance']:.4f}")
    print(source["text"][:500])
