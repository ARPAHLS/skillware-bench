# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Mock model adapter for deterministic offline CI, unit tests, and fault simulation."""

from typing import Any, Dict, List, Optional

from skillware_bench.core.adapters.base import (
    BaseModelAdapter,
    ModelResponse,
    TokenUsage,
    ToolCallRequest,
)


class SimulatedRateLimitError(Exception):
    """Simulated 429 Too Many Requests error for retry testing."""


class SimulatedServerError(Exception):
    """Simulated 503 Service Unavailable error for retry testing."""


class MockModelAdapter(BaseModelAdapter):
    """Deterministic scriptable adapter for hermetic testing and error simulation."""

    def __init__(
        self,
        model_name: str = "golden-target",
        scripted_responses: Optional[List[ModelResponse]] = None,
        simulated_failures_before_success: int = 0,
        failure_exception_type: type = SimulatedRateLimitError,
        **kwargs: Any,
    ):
        super().__init__(model_name=model_name, **kwargs)
        self.scripted_responses = list(scripted_responses) if scripted_responses else []
        self.simulated_failures_remaining = simulated_failures_before_success
        self.failure_exception_type = failure_exception_type
        self.call_history: List[Dict[str, Any]] = []
        self.step_counter = 0

    def add_response(self, response: ModelResponse) -> None:
        self.scripted_responses.append(response)

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ModelResponse:
        self.call_history.append(
            {
                "messages": messages,
                "tools": tools,
                "system_prompt": system_prompt,
                "kwargs": kwargs,
            }
        )

        if self.simulated_failures_remaining > 0:
            self.simulated_failures_remaining -= 1
            raise self.failure_exception_type("Simulated provider rate limit (429) backoff trigger")

        if self.scripted_responses and self.step_counter < len(self.scripted_responses):
            resp = self.scripted_responses[self.step_counter]
            self.step_counter += 1
            self.record_usage(resp.usage)
            return resp

        # Default fallback response
        self.step_counter += 1
        default_usage = TokenUsage(prompt_tokens=150, completion_tokens=30, total_tokens=180)
        self.record_usage(default_usage)

        tool_calls: List[ToolCallRequest] = []
        if tools and len(tools) > 0:
            first_tool = tools[0]
            name = (
                first_tool.get("function", {}).get("name")
                or first_tool.get("name")
                or first_tool.get("manifest", {}).get("name")
                or "execute_action"
            )
            tool_calls.append(
                ToolCallRequest(
                    name=name,
                    arguments={"status": "mock_arg"},
                    id=f"call_{self.step_counter}",
                )
            )

        return ModelResponse(
            content=f"Mock model response turn {self.step_counter}",
            tool_calls=tool_calls,
            usage=default_usage,
            latency_ms=120.0,
            ttft_ms=50.0,
            model=self.model_name,
        )
