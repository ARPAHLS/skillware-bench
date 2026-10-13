# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Anthropic model adapter (Claude 3.7 Sonnet, Claude 3.5 Haiku)."""

import os
import time
from typing import Any, Dict, List, Optional

from skillware_bench.core.adapters.base import (
    BaseModelAdapter,
    ModelResponse,
    TokenUsage,
    ToolCallRequest,
    execute_with_retry,
)

try:
    from skillware.core.loader import SkillLoader
except ImportError:
    SkillLoader = None  # type: ignore


class AnthropicAdapter(BaseModelAdapter):
    """Adapter for Anthropic Claude models supporting structured tool use."""

    def __init__(
        self,
        model_name: str = "claude-3-7-sonnet-20250219",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(model_name=model_name, api_key=api_key, **kwargs)
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = base_url or os.environ.get("ANTHROPIC_BASE_URL")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic

                self._client = anthropic.Anthropic(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    timeout=self.timeout_seconds,
                )
            except ImportError:
                raise ImportError(
                    "anthropic package is required to use AnthropicAdapter. Run: pip install anthropic"
                )
        return self._client

    def format_tools(self, tool_definitions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        formatted: List[Dict[str, Any]] = []
        for tool in tool_definitions:
            if "name" in tool and "input_schema" in tool:
                formatted.append(tool)
            elif "manifest" in tool and SkillLoader is not None:
                formatted.append(SkillLoader.to_claude_tool(tool))
            else:
                name = tool.get("name", "unknown_tool")
                desc = tool.get("description", "")
                params = tool.get("parameters") or tool.get("input_schema") or {}
                formatted.append(
                    {
                        "name": name,
                        "description": desc,
                        "input_schema": params,
                    }
                )
        return formatted

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ModelResponse:
        client = self._get_client()

        anthropic_messages: List[Dict[str, Any]] = []
        for m in messages:
            role = m.get("role", "user")
            if role == "system":
                if not system_prompt:
                    system_prompt = m.get("content", "")
                continue
            anthropic_messages.append({"role": role, "content": m.get("content", "")})

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": anthropic_messages,
            "max_tokens": self.max_tokens or 2048,
        }

        if self.temperature is not None:
            payload["temperature"] = self.temperature

        if system_prompt:
            payload["system"] = system_prompt

        if tools:
            payload["tools"] = self.format_tools(tools)

        t0 = time.perf_counter()

        def _call_api():
            return client.messages.create(**payload)

        try:
            import anthropic

            retry_types = (
                anthropic.RateLimitError,
                anthropic.APIConnectionError,
                anthropic.InternalServerError,
            )
        except Exception:
            retry_types = (Exception,)

        response = execute_with_retry(_call_api, retryable_exceptions=retry_types)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        content_parts = []
        tool_calls: List[ToolCallRequest] = []

        for block in response.content:
            if getattr(block, "type", "") == "text":
                content_parts.append(block.text)
            elif getattr(block, "type", "") == "tool_use":
                tool_calls.append(
                    ToolCallRequest(
                        name=block.name,
                        arguments=block.input if isinstance(block.input, dict) else {},
                        id=block.id,
                    )
                )

        content = "\n".join(content_parts)

        cached_tokens = 0
        if hasattr(response.usage, "cache_read_input_tokens"):
            cached_tokens += getattr(response.usage, "cache_read_input_tokens", 0) or 0
        if hasattr(response.usage, "cache_creation_input_tokens"):
            cached_tokens += getattr(response.usage, "cache_creation_input_tokens", 0) or 0

        usage = TokenUsage(
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            cached_tokens=cached_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens,
        )
        self.record_usage(usage)

        return ModelResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            latency_ms=latency_ms,
            ttft_ms=latency_ms * 0.40,
            model=self.model_name,
            raw=response,
        )
