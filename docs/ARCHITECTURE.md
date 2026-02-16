# System Architecture

## Overview

A local-first, safety-critical AI healthcare assistant designed for safe triage and grounded advice.

## Pipeline (Request Flow)

1. **User Input** (Web UI)
   ↓
2. **Intent Router** (API) -> `chitchat`, `meta`, `logistics`, `medical_symptoms`
   ↓
3. **Safety Policy Engine**
   - Checks for Red Flags (Emergency).
   - Checks for Lock State.
   - **Action**: Allow, Escalate (Lock), or Refuse.
     ↓
4. **Triage Service** (If Safe)
   - Parses Symptoms (Rules-based).
   - Assigns Urgency (`emergency`, `urgent`, `routine`, `self_care`, `unknown`).
   - If `unknown` -> Ask clarifying questions (Skip RAG).
     ↓
5. **RAG Retrieval** (If Known Urgency)
   - Expands Query (User msg + Symptom Tags).
   - Retrieves Chunks (ChromaDB).
   - **Re-ranking**: Boosts Trusted Orgs (NHS, WHO, CDC).
   - **Grounding Check**: If no relevant docs -> Set `citations_used=False`.
     ↓
6. **LLM Generation** (Ollama)
   - System Prompt enforces "No Advice without Sources".
   - Generates Response with Markdown.
     ↓
7. **Response Formatting**
   - Attaches Structured Citations.
   - Attaches Triage Metadata.
   - Attaches Local Resources (if Emergency).

## Modules

- **Apps**:
  - `apps/api`: FastAPI backend.
  - `apps/web`: Next.js frontend (Markdown support).
- **Services**:
  - `safety_service.py`: Risk assessment.
  - `triage_service.py`: Symptom parsing.
  - `rag_service.py`: Retrieval & Re-ranking.
  - `logistics_service.py`: Database of local resources.
- **Data**:
  - `rag/corpus_raw/trusted_guidelines`: Validated source documents.
  - `rag/index`: ChromaDB vector store.
  - `data/processed`: Cleaned logistics data.
