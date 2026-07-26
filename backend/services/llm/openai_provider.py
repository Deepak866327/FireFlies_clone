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

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


class OpenAIProvider(LLMProvider):
    name = "openai"

    def ask(self, system_prompt: str, messages: List[ChatTurn]) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMConfigError("OpenAI API key is not configured.")

        payload = {
            "model": OPENAI_MODEL,
            "messages": [{"role": "system", "content": system_prompt}, *messages],
            "temperature": 0.2,
        }

        try:
            response = httpx.post(
                OPENAI_API_URL,
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
                timeout=20.0,
            )
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError("The OpenAI request timed out.") from exc
        except httpx.RequestError as exc:
            raise LLMRequestError("Could not reach OpenAI.") from exc

        if response.status_code == 429:
            detail = extract_error_message(response)
            raise LLMRateLimitError(
                detail or "OpenAI rate limit reached. Please try again shortly."
            )
        if response.status_code != 200:
            detail = extract_error_message(response)
            message = f"OpenAI returned an error (status {response.status_code})."
            raise LLMRequestError(f"{message} {detail}" if detail else message)

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError) as exc:
            raise LLMRequestError("Unexpected response from OpenAI.") from exc
