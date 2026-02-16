# ──────────────────────────────────────────────
# Healthcare Assistant AI — API (FastAPI)
# Optimized: CPU-only torch, minimal COPY
# ──────────────────────────────────────────────
FROM python:3.11-slim

# System deps: Tesseract OCR + OpenCV headless requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Dependency install (layer-cached) ──────────
# 1. Install CPU-only PyTorch FIRST (saves ~1.5 GB vs default CUDA bundle)
RUN pip install --no-cache-dir \
    torch --extra-index-url https://download.pytorch.org/whl/cpu

# 2. Install remaining requirements
COPY apps/api/requirements.txt /app/apps/api/requirements.txt
RUN pip install --no-cache-dir -r /app/apps/api/requirements.txt

# ── Copy only what's needed at runtime ─────────
# Application code
COPY apps/api/ /app/apps/api/

# RAG index (also volume-mounted in compose, but baked in for standalone)
COPY rag/index/ /app/rag/index/

# Facilities data for logistics service
COPY data/ /app/data/

# Runtime directory for exports
RUN mkdir -p /app/eval/evidence

# Uvicorn runs from apps/api/ (relative imports expect this cwd)
WORKDIR /app/apps/api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
