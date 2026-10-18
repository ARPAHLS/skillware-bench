# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""OpenRouter model adapter for frontier and sovereign models via OpenRouter API."""

import copy
import json
import os
import time
from typing import Any, Dict, List, Optional

from skillware_bench.core.adapters.base import (
    BaseModelAdapter,
    ModelResponse,
    TokenUsage,
    ToolCallRequest,
    calculate_cost,
    execute_with_retry,
)

try:
    from skillware.core.loader import SkillLoader
except ImportError:
    SkillLoader = None  # type: ignore


class OpenRouterAdapter(BaseModelAdapter):
    """Adapter for models hosted via OpenRouter (frontier, sovereign, and batch)."""

    OPENROUTER_DEFAULT_URL = "https://openrouter.ai/api/v1"

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        site_url: str = "https://github.com/ARPAHLS/skillware-bench",
        app_name: str = "Skillware-Bench",
        **kwargs: Any,
    ):
        super().__init__(model_name=model_name, api_key=api_key, **kwargs)
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except Exception:
            pass
        self.api_key = (
            api_key or os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API")
        )
        self.base_url = (
            base_url or os.environ.get("OPENROUTER_BASE_URL") or self.OPENROUTER_DEFAULT_URL
        )
        self.site_url = site_url
        self.app_name = app_name
        self._client = None

        if self.max_tokens is None:
            # Default to 1024 tokens to provide adequate room for reasoning models
            self.max_tokens = 1024

    def _get_client(self):
        if self._client is None:
            if not self.api_key:
                raise ValueError(
                    "OpenRouter API key not configured. Set OPENROUTER_API or OPENROUTER_API_KEY environment variable."
                )
            try:
                import openai

                headers = {
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.app_name,
                }
                self._client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    default_headers=headers,
                    timeout=self.timeout_seconds,
                )
            except ImportError:
                raise ImportError(
                    "openai package is required to use OpenRouterAdapter. Run: pip install openai"
                )
        return self._client

    @staticmethod
    def _sanitize_tool_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize JSON schema to ensure compatibility across all OpenRouter providers.

        Deeply nested object schemas inside array items (such as pipelines or attachment lists)
        cause BNF grammar blowouts or schema parsing errors in upstream engines (e.g. vLLM/Llama).
        Simplifying array item schemas to generic objects preserves semantic intent while ensuring
        robust execution across all models.
        """
        if not isinstance(schema, dict):
            return schema
        cleaned = copy.deepcopy(schema)

        def _clean_node(node: Any):
            if isinstance(node, dict):
                if node.get("type") == "array" and isinstance(node.get("items"), dict):
                    items = node["items"]
                    if items.get("type") == "object" and "properties" in items:
                        node["items"] = {"type": "object"}
                for v in node.values():
                    _clean_node(v)
            elif isinstance(node, list):
                for item in node:
                    _clean_node(item)

        _clean_node(cleaned)
        return cleaned

    def format_tools(self, tool_definitions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format tools into standard OpenAI function calling specifications."""
        formatted: List[Dict[str, Any]] = []
        for tool in tool_definitions:
            tool_entry = None
            if (
                isinstance(tool, dict)
                and "type" in tool
                and tool["type"] == "function"
                and "function" in tool
            ):
                tool_entry = copy.deepcopy(tool)
            elif isinstance(tool, dict) and "manifest" in tool and SkillLoader is not None:
                tool_entry = copy.deepcopy(SkillLoader.to_openai_tool(tool))
            elif isinstance(tool, dict):
                name = tool.get("name", "unknown_tool")
                desc = tool.get("description", "")
                params = tool.get("parameters", {"type": "object", "properties": {}})
                tool_entry = {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": desc,
                        "parameters": params,
                    },
                }

            if tool_entry and "function" in tool_entry and "parameters" in tool_entry["function"]:
                tool_entry["function"]["parameters"] = self._sanitize_tool_schema(
                    tool_entry["function"]["parameters"]
                )
            if tool_entry:
                formatted.append(tool_entry)

        return formatted

    def _sanitize_messages(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        has_tools: bool = False,
    ) -> List[Dict[str, Any]]:
        """Normalize message history into strict OpenAI/OpenRouter wire format."""
        sanitized: List[Dict[str, Any]] = []

        # Upstream Jinja chat templates for Llama models inject tool definitions into the system prompt.
        # Having an explicit separate system message causes Jinja template collision / instant EOS.
        # Prepending system instructions into the first user message preserves instructions while enabling tools.
        is_llama = any(k in self.model_name.lower() for k in ["llama", "maverick", "scout"])
        merge_system = has_tools and is_llama

        pending_system_text = ""
        if system_prompt:
            pending_system_text = system_prompt.strip()

        if merge_system:
            system_pieces = [pending_system_text] if pending_system_text else []
            other_messages = []
            for m in messages:
                if m.get("role") == "system":
                    content = (m.get("content") or "").strip()
                    if content:
                        system_pieces.append(content)
                else:
                    other_messages.append(m)

            combined_system = "\n\n".join(system_pieces).strip()
            first_user_found = False

            for m in other_messages:
                role = m.get("role", "user")
                content = m.get("content")

                if role == "user" and not first_user_found:
                    first_user_found = True
                    user_content = str(content or "")
                    if combined_system:
                        user_content = f"{combined_system}\n\n{user_content}"
                    sanitized.append({"role": "user", "content": user_content})
                elif role == "assistant" and "tool_calls" in m and m["tool_calls"]:
                    tc_list = []
                    for tc in m["tool_calls"]:
                        tc_id = tc.get("id") or "call_default"
                        fn_name = (
                            tc.get("name")
                            or (tc.get("function") or {}).get("name")
                            or "unknown_tool"
                        )
                        args = (
                            tc.get("arguments")
                            or (tc.get("function") or {}).get("arguments")
                            or {}
                        )
                        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
                        tc_list.append(
                            {
                                "id": tc_id,
                                "type": "function",
                                "function": {
                                    "name": fn_name,
                                    "arguments": args_str,
                                },
                            }
                        )
                    sanitized.append(
                        {
                            "role": "assistant",
                            "content": content or "",
                            "tool_calls": tc_list,
                        }
                    )
                elif role == "tool":
                    sanitized.append(
                        {
                            "role": "tool",
                            "tool_call_id": m.get("tool_call_id") or m.get("id", "call_default"),
                            "name": m.get("name", ""),
                            "content": str(content or ""),
                        }
                    )
                else:
                    sanitized.append(
                        {
                            "role": role,
                            "content": str(content or ""),
                        }
                    )

            if not first_user_found and combined_system:
                sanitized.insert(0, {"role": "user", "content": combined_system})

            return sanitized

        if system_prompt and not any(m.get("role") == "system" for m in messages):
            sanitized.append({"role": "system", "content": system_prompt})

        for m in messages:
            role = m.get("role", "user")
            content = m.get("content")

            if role == "assistant" and "tool_calls" in m and m["tool_calls"]:
                tc_list = []
                for tc in m["tool_calls"]:
                    tc_id = tc.get("id") or "call_default"
                    fn_name = (
                        tc.get("name") or (tc.get("function") or {}).get("name") or "unknown_tool"
                    )
                    args = tc.get("arguments") or (tc.get("function") or {}).get("arguments") or {}
                    args_str = json.dumps(args) if isinstance(args, dict) else str(args)
                    tc_list.append(
                        {
                            "id": tc_id,
                            "type": "function",
                            "function": {
                                "name": fn_name,
                                "arguments": args_str,
                            },
                        }
                    )
                sanitized.append(
                    {
                        "role": "assistant",
                        "content": content or "",
                        "tool_calls": tc_list,
                    }
                )
            elif role == "tool":
                sanitized.append(
                    {
                        "role": "tool",
                        "tool_call_id": m.get("tool_call_id") or m.get("id", "call_default"),
                        "name": m.get("name", ""),
                        "content": str(content or ""),
                    }
                )
            else:
                sanitized.append(
                    {
                        "role": role,
                        "content": str(content or ""),
                    }
                )

        return sanitized

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ModelResponse:
        """Send chat messages and optional tool definitions to OpenRouter."""
        client = self._get_client()
        sanitized_messages = self._sanitize_messages(
            messages, system_prompt=system_prompt, has_tools=bool(tools)
        )

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": sanitized_messages,
        }

        if self.temperature is not None and not (
            ":free" in self.model_name and "reasoning" in self.model_name
        ):
            payload["temperature"] = self.temperature

        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens

        if tools:
            payload["tools"] = self.format_tools(tools)
            payload["tool_choice"] = kwargs.get("tool_choice", "auto")

        # Exclude upstream backend providers that reject parallel tool calls
        if "extra_body" in kwargs:
            payload["extra_body"] = kwargs["extra_body"]
        elif "provider" in self.extra_config:
            payload["extra_body"] = {"provider": self.extra_config["provider"]}
        else:
            payload["extra_body"] = {"provider": {"ignore": ["CoreWeave", "Groq"]}}

        t0 = time.perf_counter()

        def _call_api():
            res = client.chat.completions.create(**payload)
            if not getattr(res, "choices", None):
                err = (
                    getattr(res, "error", None)
                    or "Empty response choices from OpenRouter upstream provider"
                )
                raise RuntimeError(f"OpenRouter provider error: {err}")
            return res

        try:
            import openai

            retry_types = (
                openai.RateLimitError,
                openai.APIConnectionError,
                openai.InternalServerError,
                openai.APITimeoutError,
                RuntimeError,
            )
        except Exception:
            retry_types = (Exception,)

        response = execute_with_retry(
            _call_api,
            max_retries=5,
            initial_delay=2.0,
            backoff_factor=2.0,
            jitter=True,
            retryable_exceptions=retry_types,
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0

        choice = response.choices[0]
        msg = getattr(choice, "message", None)
        content = (getattr(msg, "content", "") or "") if msg else ""
        refusal = (getattr(msg, "refusal", "") or "") if msg else ""
        if not content and refusal:
            content = refusal

        # Fallback to reasoning text if content is empty and no tool calls exist
        reasoning_text = (getattr(msg, "reasoning", "") or "") if msg else ""
        tool_calls: List[ToolCallRequest] = []

        if msg and getattr(msg, "tool_calls", None):
            for tc in msg.tool_calls:
                fn_name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                except json.JSONDecodeError:
                    args = {"_raw": tc.function.arguments}
                tool_calls.append(ToolCallRequest(name=fn_name, arguments=args, id=tc.id))

        if not content and not tool_calls and reasoning_text:
            content = reasoning_text.strip()

        # Telemetry & exact cost tracking
        prompt_tokens = getattr(response.usage, "prompt_tokens", 0) or 0
        completion_tokens = getattr(response.usage, "completion_tokens", 0) or 0
        total_tokens = getattr(response.usage, "total_tokens", 0) or (
            prompt_tokens + completion_tokens
        )

        cached_tokens = 0
        if (
            hasattr(response.usage, "prompt_tokens_details")
            and response.usage.prompt_tokens_details
        ):
            cached_tokens = getattr(response.usage.prompt_tokens_details, "cached_tokens", 0) or 0

        # Exact upstream cost from OpenRouter if provided
        direct_cost = getattr(response.usage, "cost", None)
        if direct_cost is not None and isinstance(direct_cost, (int, float)):
            cost_usd = float(direct_cost)
        elif ":free" in self.model_name.lower():
            cost_usd = 0.0
        else:
            usage_temp = TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cached_tokens=cached_tokens,
                total_tokens=total_tokens,
            )
            cost_usd = calculate_cost(self.model_name, usage_temp)

        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cached_tokens=cached_tokens,
            total_tokens=total_tokens,
            cost_usd=cost_usd,
        )

        # Accumulate usage on adapter
        self.cumulative_usage.prompt_tokens += usage.prompt_tokens
        self.cumulative_usage.completion_tokens += usage.completion_tokens
        self.cumulative_usage.cached_tokens += usage.cached_tokens
        self.cumulative_usage.total_tokens += usage.total_tokens
        self.cumulative_cost_usd += usage.cost_usd

        return ModelResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            latency_ms=latency_ms,
            ttft_ms=latency_ms * 0.45,
            model=self.model_name,
            raw=response,
        )
