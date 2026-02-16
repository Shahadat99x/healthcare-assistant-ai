import sys
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Setup paths
REPO_ROOT = os.getcwd()
INDEX_PATH = os.path.join(REPO_ROOT, "rag", "index", "chroma")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def check_distances():
    print(f"Index Path: {INDEX_PATH}")
    client = chromadb.PersistentClient(path=INDEX_PATH)
    collection = client.get_collection(name="medical_docs")
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    
    queries = [
        "I have a fever of 40 degrees", # Should be relevant
        "I have a mild headache",       # Should be relevant (Goal: < 1.25)
        "Rash for 2 weeks",             # Should be irrelevant (Goal: > 1.25)
        "My leg is broken",             # Should be irrelevant
        "Just checking in"              # Should be irrelevant
    ]
    
    for q in queries:
        print(f"\nQuery: {q}")
        embed = embedder.encode(q).tolist()
        results = collection.query(
            query_embeddings=[embed],
            n_results=3,
            include=["documents", "distances", "metadatas"]
        )
        
        for i in range(len(results["ids"][0])):
            doc = results["documents"][0][i][:50]
            dist = results["distances"][0][i]
            meta = results["metadatas"][0][i]
            print(f"  Result {i+1}: Dist={dist:.4f} | {doc}... | {meta.get('title')}")

if __name__ == "__main__":
    check_distances()
