import requests
from typing import List, Dict


class OllamaClient:
    """Simple client for interacting with Ollama chat API."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
    ) -> str:
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        data = response.json()

        return data["message"]["content"].strip()