import json
from typing import Dict, Iterator, List

import requests


class OllamaClient:
    """Client for interacting with Ollama chat API."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        num_predict: int = 1024,
    ) -> str:
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict,
            },
        }

        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        data = response.json()

        return data["message"]["content"].strip()

    def stream_chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        num_predict: int = 1024,
    ) -> Iterator[str]:
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict,
            },
        }

        response = requests.post(url, json=payload, stream=True, timeout=300)
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            try:
                data = json.loads(line.decode("utf-8"))
            except json.JSONDecodeError:
                continue

            if "message" in data and "content" in data["message"]:
                chunk = data["message"]["content"]
                if chunk:
                    yield chunk

            if data.get("done", False):
                break