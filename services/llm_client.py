import json
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "openai/gpt-oss-20b"

    def call_model_json(self, prompt: str) -> Dict[str, Any]:
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
            },
            timeout=30,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)
    def transcribe(self, audio_bytes: bytes) -> str:
        response = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            files={"file": ("recording.wav", audio_bytes, "audio/wav")},
            data={"model": "whisper-large-v3-turbo", "language": "en"},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["text"]