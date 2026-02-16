
import os
import glob
import shutil
import pathlib
import time
import chromadb
from sentence_transformers import SentenceTransformer

import json

# Config - Robust Absolute Paths
# scripts/ingest_rag.py -> scripts -> root
FILE_DIR = pathlib.Path(__file__).parent.resolve()
REPO_ROOT = FILE_DIR.parent
# Phase 4: Use trusted guidelines
CORPUS_DIR = REPO_ROOT / "rag" / "corpus_raw" / "trusted_guidelines"
INDEX_DIR = REPO_ROOT / "rag" / "index" / "chroma"
MANIFEST_PATH = CORPUS_DIR / "manifest.json"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# Phase 4: Larger chunks for better context
CHUNK_SIZE = 1000 
CHUNK_OVERLAP = 200

def load_manifest():
    """Loads validation manifest if it exists."""
    if not MANIFEST_PATH.exists():
        print(f"Warning: Manifest not found at {MANIFEST_PATH}")
        return {}
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading manifest: {e}")
        return {}

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    # Simple character-based chunking for now
    while start < len(text):
        end = min(start + size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += (size - overlap)
    return chunks

def remove_readonly(func, path, excinfo):
    """Helper to remove read-only files on Windows."""
    try:
        os.chmod(path, 0o777)
        func(path)
    except Exception as e:
        print(f"Error removing read-only file {path}: {e}")

def safe_recreate_index(index_path):
    """Safely removes and recreates the index directory."""
    path = pathlib.Path(index_path)
    if not path.exists():
        return

    print(f"Removing old index at {path}...")
    try:
        shutil.rmtree(path, onerror=remove_readonly)
    except PermissionError:
        print("\n" + "!" * 50)
        print("ERROR: File Permission Denied.")
        print("Could not delete the existing RAG index.")
        print("Detailed Error: The folder 'rag/index/chroma' is being used by another process.")
        print("ACTION REQUIRED: Stop the running API server (Ctrl+C in your other terminal) and try again.")
        print("!" * 50 + "\n")
        exit(1)
    except Exception as e:
        print(f"Error removing old index: {e}")
        exit(1)

    # Small sleep to let OS release locks
    time.sleep(1)

def main():
    print("--- Starting RAG Ingestion (Phase 4: Trusted Corpus) ---")
    print(f"Repo Root: {REPO_ROOT}")
    print(f"Corpus Dir: {CORPUS_DIR}")
    print(f"Index Dir: {INDEX_DIR}")
    
    # 1. Initialize Clients
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    
    # Clean recreate index
    safe_recreate_index(INDEX_DIR)
    
    print(f"Creating Chroma client at {INDEX_DIR}")
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    collection = client.create_collection(name="medical_docs")

    # 2. Load Manifest
    manifest = load_manifest()
    print(f"Loaded {len(manifest)} entries from manifest.")

    # 3. Process Files
    # Get all .txt and .md files
    docs = list(CORPUS_DIR.glob("*.txt")) + list(CORPUS_DIR.glob("*.md"))
    print(f"Found {len(docs)} documents in {CORPUS_DIR}")

    total_chunks = 0
    ids_batch = []
    embeddings_batch = []
    metadatas_batch = []
    documents_batch = []

    for file_path in docs:
        filename = file_path.name
        # Skip manifest itself if glob picked it up (though glob pattern shouldn't)
        if filename == "manifest.json": continue

        print(f"Processing {filename}...")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Skipping {filename} due to read error: {e}")
            continue
            
        # Get metadata from manifest or default
        if filename in manifest:
            meta = manifest[filename]
            # Flatten tags list to string for Chroma storage compatibility if needed
            # But recent Chroma versions handle lists. Let's keep it safe and join tags.
            if "tags" in meta and isinstance(meta["tags"], list):
                meta["tags"] = ",".join(meta["tags"])
        else:
            print(f"Warning: {filename} not in manifest. Using defaults.")
            meta = {
                "title": filename,
                "org": "Unknown",
                "doc_type": "unknown",
                "tags": ""
            }
        
        # Ensure ID and critical fields are present
        meta["filename"] = filename
        
        chunks = chunk_text(content)
        
        for i, chunk in enumerate(chunks):
            # STABLE ID: filename#chunk_index
            chunk_id = f"{filename}#chunk_{i}"
            
            # Prepare batch
            ids_batch.append(chunk_id)
            documents_batch.append(chunk)
            metadatas_batch.append(meta)
            
            vector = embedder.encode(chunk).tolist()
            embeddings_batch.append(vector)
            
            total_chunks += 1

    # 4. Upsert to Chroma
    if ids_batch:
        print(f"Upserting {len(ids_batch)} chunks to Chroma...")
        collection.add(
            ids=ids_batch,
            embeddings=embeddings_batch,
            metadatas=metadatas_batch,
            documents=documents_batch
        )

    print(f"--- Ingestion Complete. Total Chunks: {total_chunks} ---")

if __name__ == "__main__":
    main()
