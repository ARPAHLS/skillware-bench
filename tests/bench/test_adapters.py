# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Unit tests for model adapters, token accounting, pricing, and retry engine."""

import pytest
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
)
from skillware_bench.core.adapters.ollama_adapter import OllamaAdapter
from skillware_bench.core.adapters.openai_adapter import OpenAIAdapter


def test_token_usage_and_pricing():
    # GPT-4o: $2.50 prompt, $10.00 completion, $1.25 cached per 1M
    usage = TokenUsage(
        prompt_tokens=1_000_000,
        completion_tokens=500_000,
        cached_tokens=200_000,
    )
    # Uncached prompt: 800k * 2.50 = 2.00
    # Cached prompt: 200k * 1.25 = 0.25
    # Completion: 500k * 10.00 = 5.00
    # Total = 7.25
    cost = calculate_cost("gpt-4o", usage)
    assert pytest.approx(cost, 0.001) == 7.25

    # Llama 3.2 sovereign local: $0.00
    llama_cost = calculate_cost("llama3.2", usage)
    assert llama_cost == 0.0


def test_retry_backoff_recovers():
    call_count = 0

    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise SimulatedRateLimitError("Rate limit hit")
        return "success"

    result = execute_with_retry(
        flaky_func,
        max_retries=4,
        initial_delay=0.01,
        backoff_factor=1.5,
        retryable_exceptions=(SimulatedRateLimitError,),
    )
    assert result == "success"
    assert call_count == 3


def test_retry_backoff_exhaustion():
    def always_fail():
        raise SimulatedRateLimitError("Permanent 429")

    with pytest.raises(SimulatedRateLimitError):
        execute_with_retry(
            always_fail,
            max_retries=2,
            initial_delay=0.01,
            retryable_exceptions=(SimulatedRateLimitError,),
        )


def test_adapter_factory_resolution():
    gpt = get_adapter("gpt-4o", mock=False)
    assert isinstance(gpt, OpenAIAdapter)

    o3 = get_adapter("o3-mini", mock=False)
    assert isinstance(o3, OpenAIAdapter)

    claude = get_adapter("claude-3-7-sonnet", mock=False)
    assert isinstance(claude, AnthropicAdapter)

    gemini = get_adapter("gemini-2.5-flash", mock=False)
    assert isinstance(gemini, GeminiAdapter)

    mistral = get_adapter("mistral-large-latest", mock=False)
    assert isinstance(mistral, MistralAdapter)

    ollama = get_adapter("ollama:llama3.2", mock=False)
    assert isinstance(ollama, OllamaAdapter)
    assert ollama.model_name == "llama3.2"

    mock = get_adapter("golden-target", mock=True)
    assert isinstance(mock, MockModelAdapter)


def test_adapter_registry_custom_byom():
    class CustomEnterpriseAdapter(BaseModelAdapter):
        def chat(self, messages, tools=None, system_prompt=None, **kwargs):
            return ModelResponse(content="custom enterprise response", model=self.model_name)

    AdapterRegistry.register("enterprise-v2", CustomEnterpriseAdapter)
    resolved = get_adapter("enterprise-v2-finetune", mock=False)
    assert isinstance(resolved, CustomEnterpriseAdapter)

    resp = resolved.chat([{"role": "user", "content": "hello"}])
    assert resp.content == "custom enterprise response"


def test_mock_adapter_scripted_responses():
    r1 = ModelResponse(
        content="Turn 1 draft",
        tool_calls=[ToolCallRequest(name="test_tool", arguments={"val": 42})],
        usage=TokenUsage(prompt_tokens=100, completion_tokens=20),
        model="mock",
    )
    r2 = ModelResponse(
        content="Turn 2 confirmed",
        usage=TokenUsage(prompt_tokens=150, completion_tokens=30),
        model="mock",
    )

    adapter = MockModelAdapter(scripted_responses=[r1, r2])
    res1 = adapter.chat([{"role": "user", "content": "turn 1"}])
    assert res1.content == "Turn 1 draft"
    assert len(res1.tool_calls) == 1
    assert res1.tool_calls[0].arguments == {"val": 42}

    res2 = adapter.chat([{"role": "user", "content": "turn 2"}])
    assert res2.content == "Turn 2 confirmed"
    assert adapter.cumulative_usage.total_tokens == 300


def test_tool_formatting_helpers():
    sample_tools = [
        {
            "name": "lookup_company",
            "description": "Look up UK registration details",
            "parameters": {
                "type": "object",
                "properties": {"company_number": {"type": "string"}},
                "required": ["company_number"],
            },
        }
    ]

    openai_adapter = OpenAIAdapter("gpt-4o")
    formatted_openai = openai_adapter.format_tools(sample_tools)
    assert len(formatted_openai) == 1
    assert formatted_openai[0]["type"] == "function"
    assert formatted_openai[0]["function"]["name"] == "lookup_company"

    claude_adapter = AnthropicAdapter("claude-3-7-sonnet")
    formatted_claude = claude_adapter.format_tools(sample_tools)
    assert len(formatted_claude) == 1
    assert formatted_claude[0]["name"] == "lookup_company"
    assert "input_schema" in formatted_claude[0]
