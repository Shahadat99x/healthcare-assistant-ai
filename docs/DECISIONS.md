# DECISIONS — Single Source of Truth

## 1) Product scope

- MVP focuses on: safe triage dialogue + citations + evaluation.
- Local Bucharest directory is optional extension (sample data allowed).

## 2) Tech stack (MVP)

- Web: Next.js
- API: FastAPI
- Local model runtime: Ollama
- Vector DB: Chroma (local)
- Directory DB: Postgres (optional in MVP; can be added early)

## 3) Model choice (initial)

- qwen2.5:7b-instruct.
  -Runtime: Ollama
  -base url: http://localhost:11434
- No full training from scratch. Fine-tuning is optional future work.

## 4) Policy decisions

- No diagnosis or dosage.
- Emergency escalation for red flags (112).
- No live web browsing in MVP; curated corpus only.

## 5) Change log

- (Add dated entries here as decisions change.)
