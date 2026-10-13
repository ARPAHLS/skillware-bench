# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Google Gemini model adapter (Gemini 2.5 Pro, Gemini 2.5 Flash)."""

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


class GeminiAdapter(BaseModelAdapter):
    """Adapter for Google Gemini models using the modern google-genai SDK."""

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(model_name=model_name, api_key=api_key, **kwargs)
        self.api_key = (
            api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        )
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from google import genai

                self._client = genai.Client(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "google-genai package is required for GeminiAdapter. Run: pip install google-genai"
                )
        return self._client

    def format_tools(self, tool_definitions: List[Dict[str, Any]]) -> List[Any]:
        from google.genai import types

        declarations = []
        for tool in tool_definitions:
            if isinstance(tool, types.Tool):
                return [tool]
            if "manifest" in tool and SkillLoader is not None:
                gemini_tool = SkillLoader.to_gemini_tool(tool)
                if isinstance(gemini_tool, types.Tool):
                    declarations.extend(gemini_tool.function_declarations or [])
                else:
                    declarations.append(gemini_tool)
            else:
                name = tool.get("name", "unknown_tool")
                desc = tool.get("description", "")
                params = tool.get("parameters", {})
                declarations.append(
                    {
                        "name": name,
                        "description": desc,
                        "parameters": params,
                    }
                )

        if declarations:
            return [types.Tool(function_declarations=declarations)]
        return []

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ModelResponse:
        client = self._get_client()
        from google.genai import types

        # Build contents from message list
        contents = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                if not system_prompt:
                    system_prompt = content
                continue
            gemini_role = "model" if role == "assistant" else "user"
            contents.append(
                types.Content(
                    role=gemini_role,
                    parts=[types.Part.from_text(text=str(content))],
                )
            )

        config_params: Dict[str, Any] = {}
        if system_prompt:
            config_params["system_instruction"] = system_prompt
        if self.temperature is not None:
            config_params["temperature"] = self.temperature
        if self.max_tokens:
            config_params["max_output_tokens"] = self.max_tokens
        if tools:
            config_params["tools"] = self.format_tools(tools)

        config = types.GenerateContentConfig(**config_params) if config_params else None

        t0 = time.perf_counter()

        def _call_api():
            return client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config,
            )

        response = execute_with_retry(_call_api)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        content = ""
        tool_calls: List[ToolCallRequest] = []

        if hasattr(response, "text") and response.text:
            content = response.text

        if hasattr(response, "function_calls") and response.function_calls:
            for fc in response.function_calls:
                args = fc.args if isinstance(fc.args, dict) else dict(fc.args or {})
                tool_calls.append(
                    ToolCallRequest(
                        name=fc.name,
                        arguments=args,
                        id=fc.name,
                    )
                )

        # Extract tokens from usage_metadata
        prompt_tokens = 0
        completion_tokens = 0
        cached_tokens = 0
        total_tokens = 0

        if hasattr(response, "usage_metadata") and response.usage_metadata:
            meta = response.usage_metadata
            prompt_tokens = getattr(meta, "prompt_token_count", 0) or 0
            completion_tokens = getattr(meta, "candidates_token_count", 0) or 0
            cached_tokens = getattr(meta, "cached_content_token_count", 0) or 0
            total_tokens = getattr(meta, "total_token_count", 0) or (
                prompt_tokens + completion_tokens
            )

        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cached_tokens=cached_tokens,
            total_tokens=total_tokens,
        )
        self.record_usage(usage)

        return ModelResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            latency_ms=latency_ms,
            ttft_ms=latency_ms * 0.35,
            model=self.model_name,
            raw=response,
        )
