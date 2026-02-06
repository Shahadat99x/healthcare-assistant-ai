import httpx
import logging
from config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT_SECONDS

    async def check_health(self) -> bool:
        """Checks if Ollama is running."""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False

    async def generate_response(self, messages: list) -> str:
        """
        Generates a response from Ollama.
        Returns the content string.
        Raises exceptions if Ollama is down or errors.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.0  # Deterministic for triage
            }
        }
        
        url = f"{self.base_url}/api/chat"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "")
        except httpx.ConnectError:
            raise RuntimeError("Ollama is not running or not accessible.")
        except httpx.TimeoutException:
            raise RuntimeError("Ollama request timed out.")
        except Exception as e:
             raise RuntimeError(f"Ollama error: {str(e)}")

ollama_client = OllamaClient()
