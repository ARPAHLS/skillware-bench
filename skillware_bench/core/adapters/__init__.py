# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Model adapters for frontier, sovereign, and mock evaluation targets."""

from skillware_bench.core.adapters.anthropic_adapter import AnthropicAdapter
from skillware_bench.core.adapters.base import (
    BaseModelAdapter,
    ModelResponse,
    TokenUsage,
    ToolCallRequest,
    calculate_cost,
    execute_with_retry,
)
from skillware_bench.core.adapters.factory import AdapterRegistry, get_adapter
from skillware_bench.core.adapters.gemini_adapter import GeminiAdapter
from skillware_bench.core.adapters.mistral_adapter import MistralAdapter
from skillware_bench.core.adapters.mock_adapter import (
    MockModelAdapter,
    SimulatedRateLimitError,
    SimulatedServerError,
)
from skillware_bench.core.adapters.ollama_adapter import OllamaAdapter
from skillware_bench.core.adapters.openai_adapter import OpenAIAdapter

__all__ = [
    "BaseModelAdapter",
    "ModelResponse",
    "TokenUsage",
    "ToolCallRequest",
    "calculate_cost",
    "execute_with_retry",
    "AdapterRegistry",
    "get_adapter",
    "OpenAIAdapter",
    "AnthropicAdapter",
    "GeminiAdapter",
    "MistralAdapter",
    "OllamaAdapter",
    "MockModelAdapter",
    "SimulatedRateLimitError",
    "SimulatedServerError",
]
