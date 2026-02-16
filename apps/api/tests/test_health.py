"""
Smoke tests for the Healthcare Assistant AI API.
Run: pytest tests/ -v  (from apps/api/)
"""
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_health_returns_200():
    """GET /health should return 200 with expected keys."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "service" in data
    assert data["status"] == "ok"
    assert data["service"] == "api"


def test_health_has_subsystem_keys():
    """Health response should report ollama and rag status."""
    resp = client.get("/health")
    data = resp.json()
    assert "ollama_connected" in data
    assert "rag_index_loaded" in data


def test_docs_returns_200():
    """GET /docs should return the Swagger UI page."""
    resp = client.get("/docs")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_chat_rejects_empty_body():
    """POST /chat with no body should return 422 (validation error)."""
    resp = client.post("/chat")
    assert resp.status_code == 422


def test_ready_returns_json():
    """GET /ready should return valid JSON with expected structure."""
    resp = client.get("/ready")
    assert resp.status_code in (200, 503)
    data = resp.json()
    assert data["status"] in ("ready", "not_ready")
    assert "checks" in data
    for key in ("ollama", "rag_index", "ocr"):
        assert key in data["checks"]
        assert "ok" in data["checks"][key]
        assert "detail" in data["checks"][key]
