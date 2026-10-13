# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Ollama local sovereign model adapter (Llama 3.2, Qwen 2.5)."""

import json
import os
import time
from typing import Any, Dict, List, Optional
import requests

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


class OllamaAdapter(BaseModelAdapter):
    """Adapter for local sovereign models running via Ollama API."""

    def __init__(
        self,
        model_name: str = "llama3.2",
        host: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(model_name=model_name, **kwargs)
        self.host = (host or os.environ.get("OLLAMA_HOST") or "http://localhost:11434").rstrip("/")

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
        url = f"{self.host}/api/chat"

        chat_messages = list(messages)
        if system_prompt and not any(m.get("role") == "system" for m in chat_messages):
            chat_messages.insert(0, {"role": "system", "content": system_prompt})

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": chat_messages,
            "stream": False,
        }

        options: Dict[str, Any] = {}
        if self.temperature is not None:
            options["temperature"] = self.temperature
        if self.max_tokens:
            options["num_predict"] = self.max_tokens
        if options:
            payload["options"] = options

        if tools:
            payload["tools"] = self.format_tools(tools)

        t0 = time.perf_counter()

        def _call_api():
            resp = requests.post(url, json=payload, timeout=self.timeout_seconds)
            resp.raise_for_status()
            return resp.json()

        data = execute_with_retry(
            _call_api,
            retryable_exceptions=(requests.RequestException,),
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0

        message_data = data.get("message", {})
        content = message_data.get("content", "")

        tool_calls: List[ToolCallRequest] = []
        raw_tools = message_data.get("tool_calls", [])
        for tc in raw_tools:
            fn = tc.get("function", {})
            fn_name = fn.get("name", "unknown")
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {"_raw": args}
            tool_calls.append(ToolCallRequest(name=fn_name, arguments=args, id=fn_name))

        prompt_tokens = data.get("prompt_eval_count", 0) or 0
        completion_tokens = data.get("eval_count", 0) or 0
        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        self.record_usage(usage)

        return ModelResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            latency_ms=latency_ms,
            ttft_ms=latency_ms * 0.50,
            model=self.model_name,
            raw=data,
        )
