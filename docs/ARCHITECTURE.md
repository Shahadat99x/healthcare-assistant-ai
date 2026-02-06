# ARCHITECTURE — System Design

## 1) High-level components
- **Web (Next.js):** chat UI, urgency badge, sources panel
- **API (FastAPI):** orchestrator (policy + retrieval + model call)
- **Model runtime (Ollama):** local LLM inference
- **Vector DB (Chroma/FAISS):** RAG index over curated documents
- **Postgres (optional for MVP):** local directory + audit logs (non-PII)

## 2) Request flow (chat)
1. Web sends `{session_id, message}` → API
2. API runs **Safety Policy Engine**
   - detect red flags → urgency + escalation text
   - apply refusal rules
3. API runs **RAG Retrieval**
   - embed query → top-k chunks + metadata
4. API composes prompt (system rules + retrieved context + history)
5. API calls local model (Ollama) → response
6. API returns:
   - `assistant_message`
   - `urgency_level`
   - `citations[]`
   - `recommendations[]` (optional local directory)

## 3) Data stores
- `rag/corpus_raw/*` — curated docs
- `rag/index/*` — vector DB files
- `data/raw/*` — directory raw data (optional)
- `data/processed/*` — normalized directory data (generated)

## 4) Scaling plan (drop data later)
- Add docs → run `scripts/ingest_rag.py` → update vector index
- Add directory rows → run `scripts/ingest_directory.py` → upsert to Postgres
- No API/UX changes needed for new rows; only data updates.

## 5) Security / privacy (MVP)
- Do not store PII by default.
- Log only anonymized metadata for evaluation.
- Always show disclaimers; emergency escalation for red flags.
