from abc import ABC, abstractmethod
from typing import List, Optional, TypedDict


class ChatTurn(TypedDict):
    role: str
    content: str


def extract_error_message(response) -> Optional[str]:
    """Pulls the provider's own error message out of an OpenAI/Gemini-style error body.

    Both providers use the same {"error": {"message": "..."}} shape, so this is shared
    rather than duplicated per provider.
    """
    try:
        return response.json().get("error", {}).get("message")
    except (ValueError, AttributeError):
        return None


class LLMProvider(ABC):
    """Common interface every LLM provider must implement."""

    name: str

    @abstractmethod
    def ask(self, system_prompt: str, messages: List[ChatTurn]) -> str:
        """Send the system prompt + conversation to the provider and return the reply text."""
        raise NotImplementedError


class LLMError(Exception):
    """Base class for all LLM provider errors."""


class UnsupportedProviderError(LLMError):
    """Raised when the requested provider name has no registered implementation."""


class LLMConfigError(LLMError):
    """Raised when a provider is missing required configuration (e.g. an API key)."""


class LLMRateLimitError(LLMError):
    """Raised when the provider reports a rate limit."""


class LLMTimeoutError(LLMError):
    """Raised when the request to the provider times out."""


class LLMRequestError(LLMError):
    """Raised for network failures or unexpected/malformed provider responses."""
