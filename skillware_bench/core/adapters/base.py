# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Base model adapter interface, precision token accounting, pricing, and retry engine."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type


@dataclass
class ToolCallRequest:
    """Represents a structured tool/function call emitted by an LLM."""

    name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    id: str = ""


@dataclass
class TokenUsage:
    """Precision token telemetry including prompt, completion, and prefix caching."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    cached_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0

    def __post_init__(self):
        if self.total_tokens == 0:
            self.total_tokens = self.prompt_tokens + self.completion_tokens


@dataclass
class ModelResponse:
    """Standardized response across all LLM provider adapters."""

    content: str
    tool_calls: List[ToolCallRequest] = field(default_factory=list)
    usage: TokenUsage = field(default_factory=TokenUsage)
    latency_ms: float = 0.0
    ttft_ms: float = 0.0
    model: str = ""
    raw: Any = None


# Pricing matrix (USD per million tokens): (prompt, completion, cached_prompt)
MODEL_PRICING_TABLE: Dict[str, Tuple[float, float, float]] = {
    # OpenAI
    "gpt-4o": (2.50, 10.00, 1.25),
    "gpt-4o-mini": (0.15, 0.60, 0.075),
    "o3-mini": (1.10, 4.40, 0.55),
    "o1": (15.00, 60.00, 7.50),
    # Anthropic
    "claude-3-7-sonnet": (3.00, 15.00, 0.30),
    "claude-3-5-sonnet": (3.00, 15.00, 0.30),
    "claude-3-5-haiku": (0.80, 4.00, 0.08),
    # Google Gemini
    "gemini-2.5-pro": (1.25, 5.00, 0.3125),
    "gemini-2.5-flash": (0.075, 0.30, 0.01875),
    "gemini-1.5-pro": (1.25, 5.00, 0.3125),
    "gemini-1.5-flash": (0.075, 0.30, 0.01875),
    # Mistral
    "mistral-large": (2.00, 6.00, 0.0),
    "codestral": (0.30, 0.90, 0.0),
    # Local Sovereign (Zero API Cost)
    "llama3.2": (0.0, 0.0, 0.0),
    "llama3": (0.0, 0.0, 0.0),
    "qwen2.5": (0.0, 0.0, 0.0),
}


def calculate_cost(model_name: str, usage: TokenUsage) -> float:
    """Compute exact USD cost based on token telemetry and model pricing tier."""
    name_lower = model_name.lower()
    rates: Optional[Tuple[float, float, float]] = None

    for key, val in MODEL_PRICING_TABLE.items():
        if key in name_lower:
            rates = val
            break

    if rates is None:
        rates = (1.00, 3.00, 0.0)

    prompt_rate, completion_rate, cached_rate = rates
    uncached_prompt = max(0, usage.prompt_tokens - usage.cached_tokens)

    cost = (
        (uncached_prompt * prompt_rate / 1_000_000.0)
        + (usage.cached_tokens * cached_rate / 1_000_000.0)
        + (usage.completion_tokens * completion_rate / 1_000_000.0)
    )
    return round(cost, 6)


def execute_with_retry(
    fn: Callable[[], Any],
    max_retries: int = 4,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Any:
    """Execute callable with exponential backoff and jitter for resilient API calling."""
    delay = initial_delay
    last_err: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        try:
            return fn()
        except retryable_exceptions as e:
            last_err = e
            if attempt == max_retries:
                raise e
            sleep_time = delay * (1.0 + (random.uniform(0, 0.25) if jitter else 0.0))
            time.sleep(sleep_time)
            delay *= backoff_factor

    if last_err is not None:
        raise last_err


class BaseModelAdapter(ABC):
    """Abstract base adapter for frontier and sovereign LLM providers."""

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        timeout_seconds: float = 60.0,
        **kwargs: Any,
    ):
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        self.extra_config = kwargs

        self.cumulative_usage = TokenUsage()
        self.cumulative_cost_usd: float = 0.0

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ModelResponse:
        """Send chat messages and optional tool definitions to the LLM."""
        pass

    def format_tools(self, tool_definitions: List[Dict[str, Any]]) -> List[Any]:
        """Convert generic tool definitions into provider-native format."""
        return tool_definitions

    def record_usage(self, usage: TokenUsage) -> None:
        """Accumulate token accounting and compute incremental cost."""
        usage.cost_usd = calculate_cost(self.model_name, usage)
        self.cumulative_usage.prompt_tokens += usage.prompt_tokens
        self.cumulative_usage.completion_tokens += usage.completion_tokens
        self.cumulative_usage.cached_tokens += usage.cached_tokens
        self.cumulative_usage.total_tokens += usage.total_tokens
        self.cumulative_cost_usd += usage.cost_usd
