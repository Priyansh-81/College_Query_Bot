from pathlib import Path


base_dir=Path(__file__).resolve().parent.parent
data_dir=base_dir/"data"

#print(data_dir)
model_name="gemma4:e4b"

emb_model="nomic-embed-text"
chroma_dir=data_dir/"chroma"
collection_name="college_knowloedge"

database_path = data_dir / "helpdesk.db"#sqlite db path

top_k = 4

app_name="College Helpdesk Bot"
debug=True

if __name__ == "__main__":
    print(f"Base directory: {base_dir}")
    print(f"Data directory: {data_dir}")
    print(f"Chroma directory: {chroma_dir}")
    print(f"Database path: {database_path}")
    print(f"Collection name: {collection_name}")
    print(f"Top K: {top_k}")
    print(f"App name: {app_name}")
    print(f"Debug: {debug}")