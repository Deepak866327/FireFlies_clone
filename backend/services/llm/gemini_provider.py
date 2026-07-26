import os
from typing import List

import httpx

from services.llm.base import (
    ChatTurn,
    LLMConfigError,
    LLMProvider,
    LLMRateLimitError,
    LLMRequestError,
    LLMTimeoutError,
    extract_error_message,
)

GEMINI_MODEL = "gemini-flash-latest"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


class GeminiProvider(LLMProvider):
    name = "gemini"

    def ask(self, system_prompt: str, messages: List[ChatTurn]) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise LLMConfigError("Gemini API key is not configured.")

        contents = [
            {
                "role": "model" if message["role"] == "assistant" else "user",
                "parts": [{"text": message["content"]}],
            }
            for message in messages
        ]

        payload = {
            "contents": contents,
            "systemInstruction": {"parts": [{"text": system_prompt}]},
        }

        try:
            response = httpx.post(
                GEMINI_API_URL,
                params={"key": api_key},
                json=payload,
                timeout=20.0,
            )
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError("The Gemini request timed out.") from exc
        except httpx.RequestError as exc:
            raise LLMRequestError("Could not reach Gemini.") from exc

        if response.status_code == 429:
            detail = extract_error_message(response)
            raise LLMRateLimitError(
                detail or "Gemini rate limit reached. Please try again shortly."
            )
        if response.status_code != 200:
            detail = extract_error_message(response)
            message = f"Gemini returned an error (status {response.status_code})."
            raise LLMRequestError(f"{message} {detail}" if detail else message)

        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError) as exc:
            raise LLMRequestError("Unexpected response from Gemini.") from exc
