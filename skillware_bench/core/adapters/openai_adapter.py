# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""OpenAI model adapter (GPT-4o, o3-mini, o1)."""

import json
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


class OpenAIAdapter(BaseModelAdapter):
    """Adapter for OpenAI models supporting chat completions and function calling."""

    def __init__(
        self,
        model_name: str = "gpt-4o",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(model_name=model_name, api_key=api_key, **kwargs)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import openai

                self._client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    timeout=self.timeout_seconds,
                )
            except ImportError:
                raise ImportError(
                    "openai package is required to use OpenAIAdapter. Run: pip install openai"
                )
        return self._client

    def format_tools(self, tool_definitions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        formatted: List[Dict[str, Any]] = []
        for tool in tool_definitions:
            if "function" in tool and tool.get("type") == "function":
                formatted.append(tool)
            elif "manifest" in tool and SkillLoader is not None:
                formatted.append(SkillLoader.to_openai_tool(tool))
            else:
                name = tool.get("name", "unknown_tool")
                desc = tool.get("description", "")
                params = tool.get("parameters", {})
                formatted.append(
                    {
                        "type": "function",
                        "function": {
                            "name": name,
                            "description": desc,
                            "parameters": params,
                        },
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

        chat_messages = list(messages)
        if system_prompt and not any(m.get("role") == "system" for m in chat_messages):
            role = "developer" if ("o1" in self.model_name or "o3" in self.model_name) else "system"
            chat_messages.insert(0, {"role": role, "content": system_prompt})

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": chat_messages,
        }

        # Temperature is not supported on o1/o3-mini in certain API versions
        if not ("o1" in self.model_name or "o3" in self.model_name):
            payload["temperature"] = self.temperature

        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens

        if tools:
            payload["tools"] = self.format_tools(tools)
            payload["tool_choice"] = kwargs.get("tool_choice", "auto")

        t0 = time.perf_counter()

        def _call_api():
            return client.chat.completions.create(**payload)

        try:
            import openai

            retry_types = (
                openai.RateLimitError,
                openai.APIConnectionError,
                openai.InternalServerError,
            )
        except Exception:
            retry_types = (Exception,)

        response = execute_with_retry(_call_api, retryable_exceptions=retry_types)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        choice = response.choices[0]
        content = choice.message.content or ""

        tool_calls: List[ToolCallRequest] = []
        if getattr(choice.message, "tool_calls", None):
            for tc in choice.message.tool_calls:
                fn_name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                except json.JSONDecodeError:
                    args = {"_raw": tc.function.arguments}
                tool_calls.append(ToolCallRequest(name=fn_name, arguments=args, id=tc.id))

        cached_tokens = 0
        if (
            hasattr(response.usage, "prompt_tokens_details")
            and response.usage.prompt_tokens_details
        ):
            cached_tokens = getattr(response.usage.prompt_tokens_details, "cached_tokens", 0) or 0

        usage = TokenUsage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            cached_tokens=cached_tokens,
            total_tokens=response.usage.total_tokens,
        )
        self.record_usage(usage)

        return ModelResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            latency_ms=latency_ms,
            ttft_ms=latency_ms * 0.45,
            model=self.model_name,
            raw=response,
        )
