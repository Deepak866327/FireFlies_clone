from typing import Dict, Type

from services.llm.base import LLMProvider, UnsupportedProviderError
from services.llm.gemini_provider import GeminiProvider
from services.llm.openai_provider import OpenAIProvider

_PROVIDERS: Dict[str, Type[LLMProvider]] = {
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
}


def get_provider(name: str) -> LLMProvider:
    provider_cls = _PROVIDERS.get(name)
    if provider_cls is None:
        raise UnsupportedProviderError(f"Unsupported provider: {name}")
    return provider_cls()
