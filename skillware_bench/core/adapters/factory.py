# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Adapter factory and Bring-Your-Own-Model (BYOM) registry."""

from typing import Any, Dict, Optional, Type

from skillware_bench.core.adapters.anthropic_adapter import AnthropicAdapter
from skillware_bench.core.adapters.base import BaseModelAdapter
from skillware_bench.core.adapters.gemini_adapter import GeminiAdapter
from skillware_bench.core.adapters.mistral_adapter import MistralAdapter
from skillware_bench.core.adapters.mock_adapter import MockModelAdapter
from skillware_bench.core.adapters.ollama_adapter import OllamaAdapter
from skillware_bench.core.adapters.openai_adapter import OpenAIAdapter


class AdapterRegistry:
    """Registry allowing users to plug in custom model adapters for BYOM evaluation."""

    _custom_adapters: Dict[str, Type[BaseModelAdapter]] = {}

    @classmethod
    def register(cls, model_prefix: str, adapter_cls: Type[BaseModelAdapter]) -> None:
        """Register a custom adapter class for a model identifier prefix."""
        cls._custom_adapters[model_prefix.lower()] = adapter_cls

    @classmethod
    def get_custom(cls, model_name: str) -> Optional[Type[BaseModelAdapter]]:
        name_lower = model_name.lower()
        for prefix, adapter_cls in cls._custom_adapters.items():
            if name_lower.startswith(prefix):
                return adapter_cls
        return None


def get_adapter(model_name: str, mock: bool = False, **kwargs: Any) -> BaseModelAdapter:
    """Resolve and instantiate the appropriate model adapter."""
    if mock:
        return MockModelAdapter(model_name=model_name, **kwargs)

    name_lower = model_name.lower()

    # Check custom BYOM registry first
    custom_cls = AdapterRegistry.get_custom(name_lower)
    if custom_cls is not None:
        return custom_cls(model_name=model_name, **kwargs)

    # Mock identifiers
    if name_lower in ("mock", "mock-agent", "golden-target", "synthetic"):
        return MockModelAdapter(model_name=model_name, **kwargs)

    # OpenAI family
    if (
        name_lower.startswith("gpt-")
        or name_lower.startswith("o1")
        or name_lower.startswith("o3")
        or name_lower.startswith("chatgpt-")
    ):
        return OpenAIAdapter(model_name=model_name, **kwargs)

    # Anthropic Claude family
    if name_lower.startswith("claude-"):
        return AnthropicAdapter(model_name=model_name, **kwargs)

    # Google Gemini family
    if name_lower.startswith("gemini-"):
        return GeminiAdapter(model_name=model_name, **kwargs)

    # Mistral AI family
    if name_lower.startswith("mistral") or name_lower.startswith("codestral"):
        return MistralAdapter(model_name=model_name, **kwargs)

    # Ollama / Local Sovereign models
    if (
        name_lower.startswith("ollama:")
        or name_lower.startswith("llama")
        or name_lower.startswith("qwen")
    ):
        clean_name = model_name.split(":", 1)[-1]
        return OllamaAdapter(model_name=clean_name, **kwargs)

    # Fallback to Mock if unrecognized, or raise if mock is not desired
    return MockModelAdapter(model_name=model_name, **kwargs)
