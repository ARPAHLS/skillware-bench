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


def get_adapter(
    model_name: str,
    mock: bool = False,
    adapter_path: Optional[str] = None,
    **kwargs: Any,
) -> BaseModelAdapter:
    """Resolve and instantiate the appropriate model adapter."""
    if adapter_path:
        return load_adapter_from_file(adapter_path, model_name=model_name, **kwargs)

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
        or name_lower.startswith("gpt")
        or name_lower.startswith("o1")
        or name_lower.startswith("o3")
        or name_lower.startswith("o4")
        or name_lower.startswith("chatgpt-")
    ):
        return OpenAIAdapter(model_name=model_name, **kwargs)

    # Anthropic Claude family
    if (
        name_lower.startswith("claude-")
        or name_lower.startswith("claude")
        or name_lower.startswith("sonnet")
        or name_lower.startswith("haiku")
        or name_lower.startswith("opus")
    ):
        return AnthropicAdapter(model_name=model_name, **kwargs)

    # Google Gemini family
    if name_lower.startswith("gemini-") or name_lower.startswith("gemini"):
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


def load_adapter_from_file(file_path: str, **kwargs: Any) -> BaseModelAdapter:
    """Dynamically load and instantiate a BaseModelAdapter subclass from a Python file."""
    import importlib.util
    import inspect
    from pathlib import Path

    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Adapter file not found: {file_path}")

    spec = importlib.util.spec_from_file_location("custom_adapter_module", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from: {file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (
            inspect.isclass(attr)
            and issubclass(attr, BaseModelAdapter)
            and attr is not BaseModelAdapter
        ):
            model_name = kwargs.pop("model_name", "custom-byom-model")
            return attr(model_name=model_name, **kwargs)

    raise ValueError(f"No BaseModelAdapter subclass found in {file_path}")
