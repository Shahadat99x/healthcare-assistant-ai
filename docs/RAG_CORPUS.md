# RAG_CORPUS — Trusted Sources & Ingestion Plan

## 1) Purpose
Ensure the assistant is grounded in **trusted, curated** medical content and (optionally) local policy docs. No open-web browsing in MVP.

## 2) Source types (allowed)
- International/official guidance (e.g., public health agencies, clinical guidelines)
- Hospital/municipality policy documents (appointment rules, service navigation)
- Locally curated pages (clearly labeled, with last_verified date)

## 3) Corpus structure
- Raw docs live in: `rag/corpus_raw/`
- Each doc should have metadata:
  - title
  - source type
  - date/last_updated
  - language
  - URL (if applicable)

## 4) Ingestion rules
- Extract text → chunk into 300–800 token chunks
- Store chunk metadata (doc_id, title, last_updated)
- Build embeddings and store in vector DB index at `rag/index/`

## 5) Update policy
- Adding new docs requires re-ingest: `scripts/ingest_rag.py`
- Track `corpus_version` and include `last_updated` in citations.
