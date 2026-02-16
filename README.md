# Healthcare Assistant AI

[![CI](https://github.com/Shahadat99x/healthcare-assistant-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Shahadat99x/healthcare-assistant-ai/actions/workflows/ci.yml)

Local-first triage assistant (Next.js + FastAPI + RAG + Safety + Evaluation).

## Overview

A robust healthcare chatbot demonstrating:

1.  **Baseline**: Standard Ollama LLM integration.
2.  **RAG**: Retrieval-Augmented Generation using a local ChromaDB corpus.
3.  **Safety & Triage**:
    - Emergency Lock for critical symptoms (e.g., stroke).
    - Urgent Clarifiers for vague symptoms.
    - Refusal of medication dosing/diagnosis.
4.  **Evaluation**: Reproducible framework to compare these modes.

## Tech Stack

- **Frontend**: Next.js 15, TailwindCSS (App Router)
- **Backend**: FastAPI, Uvicorn
- **AI/ML**: Ollama (LLM), SentenceTransformers (Embeddings), ChromaDB (Vector Store)

## Quick Start

### 1. Requirements

- Node.js 18+
- Python 3.10+
- Ollama running locally (serve `llama3` or similar)

### 2. Run Application (Dev Mode)

Use the helper script to launch both API and Web:

```powershell
./dev.ps1
```

- Web: http://localhost:3000
- API: http://127.0.0.1:8000

---

## 3. RAG System (Phase 3)

The system uses a local medical corpus (Markdown files in `rag/corpus_raw`).

**Ingest Data:**

```bash
python scripts/ingest_rag.py
```

This chunks, embeds, and indexes the documents into `rag/index/chroma`.

---

## 4. Evaluation (Phase 4)

We provide a comprehensive evaluation suite to compare `Baseline` (Ollama only), `RAG` (Retrieval only), and `RAG + Safety` (Full System).

**Run the Full Evaluation:**

```powershell
./scripts/run_all_eval.ps1
```

This will:

1. Run 80+ prompts against all 3 modes.
2. Generate JSONL logs in `eval/results/<timestamp>/`.
3. Produce a `summary.md` and `summary.csv` with Safety and Grounding metrics.

**Manual Steps:**

```bash
# 1. Run inference
python scripts/run_eval.py

# 2. Summarize results
python scripts/summarize_eval.py --run eval/results/<timestamp>
```

**Metrics Calculated:**

- Emergency Recall Rate
- Refusal Compliance Rate
- Citation Coverage
- Latency Stats

---

## 5. Docker (Phase 1 — One-Command Run)

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running (whale icon green in system tray)
- Ollama installed on the host **OR** use the compose profile (see below)

### Option A — Host Ollama (default)

Run Ollama natively on your machine, then:

```bash
docker compose up --build
```

The API container reaches your host Ollama via `host.docker.internal:11434`.

### Option B — Ollama inside Docker

```bash
docker compose --profile ollama up --build
```

Then pull a model into the container:

```bash
docker compose exec ollama ollama pull qwen2.5:7b-instruct
```

> If using this mode, change `OLLAMA_BASE_URL` in `docker-compose.yml` to `http://ollama:11434`.

### Services

| Service  | URL                        | Description           |
| -------- | -------------------------- | --------------------- |
| Web      | http://localhost:3000      | Next.js frontend      |
| API      | http://localhost:8000      | FastAPI backend       |
| API Docs | http://localhost:8000/docs | Swagger UI            |
| Ollama   | http://localhost:11434     | LLM (host or profile) |

### Verification Checklist

```bash
# API health
curl http://localhost:8000/health

# API docs (expect 200)
curl -I http://localhost:8000/docs

# Chat page
curl -I http://localhost:3000/chat

# Intake page
curl -I http://localhost:3000/intake
```

---

## Common Issues (Windows)

| Issue                                         | Fix                                                                                                                  |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `//./pipe/dockerDesktopLinuxEngine` not found | Start **Docker Desktop** and wait for the green whale icon                                                           |
| Port 3000 / 8000 / 11434 already in use       | Stop local dev servers (`Ctrl+C`) or change ports in `docker-compose.yml`                                            |
| Web hot-reload not detecting changes          | `WATCHPACK_POLLING=true` and `CHOKIDAR_USEPOLLING=true` are set in compose. Restart the container if still stuck     |
| API can't reach host Ollama                   | Ensure Ollama is running on the host. `host.docker.internal` is set via `extra_hosts` in compose                     |
| Ollama model not found                        | Run `ollama pull qwen2.5:7b-instruct` on the host (or `docker compose exec ollama ollama pull ...` for profile mode) |
| First build very slow                         | `sentence-transformers` + `chromadb` are large pip installs. Subsequent builds use Docker layer cache                |
| RAG index not found                           | Ensure `rag/index/chroma/` exists locally. Run `python scripts/ingest_rag.py` first                                  |
