# PHASES — Project Execution Plan (Healthcare Assistant AI)

This file defines the step-by-step phases to build the product-style prototype and produce thesis-ready results.  
**Rule:** Do not move to the next phase until the **Exit Criteria** is met.

---

## Phase 0 — Repo Setup + App Shell
### Goal
Create a clean, runnable skeleton for web + API + docs.

### What we will do
- Create repo structure: `apps/web`, `apps/api`, `docs`, `rag`, `data`, `scripts`, `eval`
- Add `.env.example` templates (web + api)
- Add `GET /health` endpoint in FastAPI
- Create basic Next.js page (“App shell”)

### Deliverables
- FastAPI runs locally
- Next.js runs locally
- `/health` returns OK

### Exit criteria
- `uvicorn apps.api.main:app --reload` runs
- `npm run dev` runs in `apps/web`
- Browser shows the app shell page

---

## Phase 1 — Local Model Setup (Ollama) + Baseline Chat
### Goal
End-to-end chat works via local pretrained model (no RAG, no safety yet).

### What we will do
- Install Ollama and pull model
- Set defaults in `/docs/DECISIONS.md`
- Implement `POST /chat` that calls Ollama
- Build basic chat UI calling the API

### Deliverables
- Working web chat connected to FastAPI → Ollama
- API returns `assistant_message`

### Exit criteria
- `ollama list` shows chosen model (default: `qwen2.5:7b-instruct`)
- Sending a message in web UI returns a model response reliably

---

## Phase 2 — Safety Policy Engine (Guardrails First)
### Goal
Make responses safe and consistent before adding RAG.

### What we will do
- Implement safety module in API:
  - red-flag detection → emergency escalation
  - refusal rules (diagnosis/dosage/prescriptions)
  - consistent disclaimer templates
- Update `/chat` response to include:
  - `urgency`, `safety_flags[]`
- UI:
  - show urgency badge
  - show emergency banner if red flag detected

### Deliverables
- Safety behavior is deterministic and testable
- UI communicates urgency clearly

### Exit criteria
- Red-flag prompts always trigger emergency guidance (112/ER)
- Dosage/prescription requests trigger refusal response
- `docs/SAFETY_POLICY.md` matches implementation

---

## Phase 3 — RAG v1 (Trusted Medical Corpus + Citations)
### Goal
Ground answers in curated documents and show citations (core thesis value).

### What we will do
- Create ingestion pipeline:
  - `rag/corpus_raw/` → chunk → embed → store in vector index (`rag/index/`)
- Implement retrieval in API:
  - top-k relevant chunks for each query
- Update prompts to include retrieved context
- Return citations in API response
- UI sources panel:
  - show title/snippet/last_updated

### Deliverables
- RAG mode that clearly uses retrieved evidence
- Citations visible in UI

### Exit criteria
- Adding a new document + re-ingesting changes retrieved results
- `mode=rag` returns citations for most responses
- Model references retrieved evidence (not only generic text)

---

## Phase 4 — Evaluation Pipeline (Baseline vs RAG vs RAG+Safety)
### Goal
Produce defendable results for thesis: improvements measured, not just demo.

### What we will do
- Create fixed evaluation set `eval/prompts.jsonl` (50–200 prompts)
- Implement `eval/run_eval.py` to run:
  - `baseline`, `rag`, `rag_safety`
- Collect outputs + generate summary tables (CSV/JSON)
- Perform qualitative error analysis (top failure patterns)

### Deliverables
- Results table + comparison charts (optional)
- 5–10 qualitative examples (good vs bad)

### Exit criteria
- One command runs all modes and produces outputs
- Clear evidence of improvement in safety/factuality/citations

---

## Phase 5 — Local Bucharest Directory v1 (Optional Product Differentiator)
### Goal
Prevent “fake clinic info” by using a verified local directory dataset.

### What we will do
- Create Postgres schema for facilities (and optionally doctors)
- Add sample dataset in `data/raw/facilities.jsonl` (20–50 entries)
- Implement `scripts/ingest_directory.py`:
  - validate → normalize → upsert into Postgres
- Add “local recommendations” module:
  - symptoms → specialty suggestion
  - specialty → facility results from Postgres
- API returns `recommendations[]`
- UI renders facility cards (name, address, phone, hours, booking link)

### Deliverables
- Local navigation works and is updateable by “drop data + run script”
- Assistant never invents clinic/doctor data outside dataset

### Exit criteria
- Add a new facility row → rerun ingest → appears in app
- Local suggestions include only DB entries (no hallucinated clinics)

---

## Phase 6 — Deployment + Portfolio Polish
### Goal
Showcase as a real product and highlight DevOps skills.

### What we will do
- Deploy frontend (Vercel)
- Deploy backend (Render/Railway/Fly.io)
- Model strategy for demo:
  - local-only (recommended) OR tunnel for live demo sessions (Cloudflare/ngrok)
- Add CI (GitHub Actions) for lint/test
- Polish README: diagrams, setup steps, demo screenshots, evaluation summary

### Deliverables
- Live web demo link (even if model is local)
- Professional README + docs

### Exit criteria
- Repo looks “company-grade”
- Anyone can run locally using docs
- Demo can be shown reliably to professor/recruiters

---

## Phase 7 — Thesis Writing + Defense Pack
### Goal
Be fully ready to defend.

### What we will do
- Finalize thesis chapters using actual results
- Create slides:
  - problem, architecture, safety, RAG, evaluation results
- Prepare Q&A for common examiner questions (hallucination, privacy, limitations)

### Deliverables
- Final report draft + slides
- Reproducibility appendix (commands, prompt sets, corpus list)

### Exit criteria
- Can present in 8–12 minutes confidently
- Can answer “why not just ChatGPT?” with evidence + evaluation

---

## Notes (rules to avoid derail)
- Core MVP is Phases 0–4. Phase 5 is optional.
- No diagnosis / no dosage. Safety policy is non-negotiable.
- No open-web browsing in MVP; use curated corpus and directory DB only.
