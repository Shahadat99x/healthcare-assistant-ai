# README_AI — Start Here (AI Handoff)

## 1) Project summary
**Project name:** healthcare-assistant-ai  
**One-liner:** A product-style symptom triage assistant that generates safer medical conversations using a local LLM + RAG (trusted sources) + safety guardrails + evaluation, with optional Bucharest local navigation data.

## 2) Core goals (must-have)
- Build a **web app** (Next.js) + **API** (FastAPI) + **local LLM runtime** (Ollama).
- Implement **RAG** over a curated medical corpus to reduce hallucinations and provide **citations**.
- Implement a **Safety Policy Engine**: red-flag escalation + refusal rules + consistent disclaimers.
- Provide **evaluation** comparing: Baseline vs RAG vs RAG+Safety.

## 3) Non-goals (do NOT build)
- No diagnosis, no prescriptions, no dosage recommendations.
- No live web browsing for medical facts in MVP (use curated sources only).
- No storage of personally identifying patient data by default.

## 4) Current status
- Docs scaffold created in `/docs`.
- Next milestone: implement minimal backend + local LLM call + chat UI.

## 5) Repo structure (planned)
- `apps/web` — Next.js UI (chat + sources + urgency badge)
- `apps/api` — FastAPI orchestrator (chat, retrieval, safety)
- `rag/corpus_raw` — trusted medical docs (md/txt/pdf)
- `rag/index` — vector DB index (Chroma/FAISS)
- `data/raw` — local directory raw data (optional) (jsonl/csv)
- `data/processed` — normalized data (generated)
- `scripts` — ingestion + eval scripts
- `eval` — prompts + results + notebooks

## 6) How to start (target commands; update once implemented)
- Local model: `ollama serve` and `ollama run <model>`
- API: `uvicorn apps.api.main:app --reload`
- Web: `npm run dev` inside `apps/web`

## 7) Working rules for any AI assistant
- Follow `/docs/DECISIONS.md` as source of truth.
- Do not invent features outside `/docs/PRD.md`.
- Any change must update: `/docs/DECISIONS.md` + `/docs/STATUS.md`.
- Prioritize correctness/safety over “helpful” medical advice.
