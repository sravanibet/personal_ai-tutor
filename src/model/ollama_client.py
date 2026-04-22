import json
from typing import Dict, Iterator, List

import requests


class OllamaClient:
    """Simple client for interacting with Ollama chat API."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        num_predict: int | None = None,
        keep_alive: str = "30m",
    ) -> str:
        url = f"{self.base_url}/api/chat"

        options = {"temperature": temperature}
        if num_predict is not None:
            options["num_predict"] = num_predict

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "keep_alive": keep_alive,
            "options": options,
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
        num_predict: int | None = None,
        keep_alive: str = "30m",
    ) -> Iterator[str]:
        url = f"{self.base_url}/api/chat"

        options = {"temperature": temperature}
        if num_predict is not None:
            options["num_predict"] = num_predict

        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "keep_alive": keep_alive,
            "options": options,
        }

        with requests.post(url, json=payload, timeout=300, stream=True) as response:
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue

                data = json.loads(line)
                content = data.get("message", {}).get("content", "")
                if content:
                    yield content