# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Mistral AI model adapter (Mistral Large, Codestral)."""

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


class MistralAdapter(BaseModelAdapter):
    """Adapter for Mistral AI frontier models using the official mistralai SDK."""

    def __init__(
        self,
        model_name: str = "mistral-large-latest",
        api_key: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(model_name=model_name, api_key=api_key, **kwargs)
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from mistralai import Mistral

                self._client = Mistral(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "mistralai package is required for MistralAdapter. Run: pip install mistralai"
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
            chat_messages.insert(0, {"role": "system", "content": system_prompt})

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": chat_messages,
        }

        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens
        if tools:
            payload["tools"] = self.format_tools(tools)

        t0 = time.perf_counter()

        def _call_api():
            return client.chat.complete(**payload)

        response = execute_with_retry(_call_api)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        choice = response.choices[0]
        content = choice.message.content or ""

        tool_calls: List[ToolCallRequest] = []
        if getattr(choice.message, "tool_calls", None):
            for tc in choice.message.tool_calls:
                fn_name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                except (json.JSONDecodeError, TypeError):
                    args = tc.function.arguments if isinstance(tc.function.arguments, dict) else {}
                tool_calls.append(
                    ToolCallRequest(name=fn_name, arguments=args, id=tc.id or fn_name)
                )

        usage = TokenUsage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
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
