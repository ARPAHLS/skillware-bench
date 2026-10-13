# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Universal multi-turn agent execution loop with Skillware, AURA, and MnemoLink integration."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from skillware_bench.core.adapters.base import BaseModelAdapter, ModelResponse
from skillware_bench.core.evaluators import CrucibleEvaluator
from skillware_bench.core.models import (
    CrucibleRunReport,
    CrucibleScore,
    CrucibleStepTelemetry,
    ScenarioDefinition,
    ScenarioExpectations,
    ToolCallRecord,
)

# Reuse Skillware
try:
    from skillware.core.loader import SkillLoader
except ImportError:
    SkillLoader = None  # type: ignore

# Reuse AURA
try:
    from aura.api import AgentProfile, Session as AuraSession
except ImportError:
    AuraSession = None  # type: ignore
    AgentProfile = None  # type: ignore

# Reuse MnemoLink
try:
    from mnemolink import Teleology
except ImportError:
    Teleology = None  # type: ignore


class AgentLoop:
    """Orchestrates multi-turn model interaction, tool execution, and AURA provenance."""

    def __init__(
        self,
        adapter: BaseModelAdapter,
        skill_names: List[str],
        skill_configs: Optional[Dict[str, Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
        enable_aura: bool = True,
        audit_dir: Optional[Union[str, Path]] = None,
        max_turns: int = 10,
        mock: bool = False,
        infra_handlers: Optional[Dict[str, Any]] = None,
    ):
        self.adapter = adapter
        self.skill_names = skill_names
        self.skill_configs = skill_configs or {}
        self.system_prompt = system_prompt
        self.enable_aura = enable_aura and (AuraSession is not None)
        self.audit_dir = Path(audit_dir or "./runs/aura_traces")
        self.max_turns = max_turns
        self.mock = mock
        self.infra_handlers = infra_handlers or {}

        self.skill_bundles: Dict[str, Any] = {}
        self.skill_instances: Dict[str, Any] = {}
        self.tool_definitions: List[Dict[str, Any]] = []
        self.aura_session: Optional[Any] = None
        self.aura_trace_id: Optional[str] = None
        self.aura_log_path: Optional[str] = None

        self._init_skills()
        self._init_aura()

    def _init_skills(self) -> None:
        """Load Skillware skill bundles and instantiate active tool handlers."""
        if SkillLoader is None:
            return

        for skill_id in self.skill_names:
            try:
                bundle = SkillLoader.load_skill(skill_id)
                self.skill_bundles[skill_id] = bundle
                self.tool_definitions.append(bundle)

                # Instantiate skill class with provided or fallback config
                cfg = self.skill_configs.get(skill_id, {})
                if not cfg and self.mock:
                    cfg = {
                        "COMPANIES_HOUSE_API_KEY": "mock_ch_key",
                        "ETHERSCAN_API_KEY": "mock_etherscan_key",
                    }

                skill_cls = SkillLoader.get_skill_class(bundle)
                try:
                    instance = skill_cls(config=cfg)
                except Exception:
                    instance = skill_cls()
                self.skill_instances[skill_id] = instance
            except Exception:
                # Fallback for synthetic / test scenarios
                self.tool_definitions.append(
                    {
                        "name": skill_id.replace("/", "_"),
                        "description": f"Skillware skill {skill_id}",
                        "parameters": {"type": "object", "properties": {}},
                    }
                )

    def _init_aura(self) -> None:
        """Initialize AURA causal audit coat around the benchmark session."""
        if not self.enable_aura or AuraSession is None or AgentProfile is None:
            return

        try:
            self.audit_dir.mkdir(parents=True, exist_ok=True)
            safe_name = self.adapter.model_name.replace("/", "_").replace(":", "_")
            profile = AgentProfile(
                aura_id=f"bench_{safe_name}",
                name=f"skillware_bench_{safe_name}",
                skills=self.skill_names,
            )
            self.aura_session = AuraSession(profile=profile)
            self.aura_session.open(self.audit_dir)
            self.aura_trace_id = self.aura_session.trace_id
            self.aura_log_path = str(self.aura_session.log_path)
            self.aura_session.emit(
                "benchmark.session_init",
                {
                    "model": self.adapter.model_name,
                    "skills": self.skill_names,
                    "mock": self.mock,
                },
            )
        except Exception:
            self.aura_session = None

    def execute_skill_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool call against attached infra handlers or loaded Skillware instances."""
        clean_name = tool_name.replace("/", "_").lower()
        args = dict(arguments)

        # 1. Check attached high-fidelity infra handlers first
        for key, handler in self.infra_handlers.items():
            k_clean = key.replace("/", "_").lower()
            if k_clean in clean_name or clean_name in k_clean:
                if hasattr(handler, "execute_action"):
                    action = args.get("action") or tool_name.split(".")[-1]
                    return handler.execute_action(action, args)
                elif hasattr(handler, "execute"):
                    return handler.execute(args)

        # 2. Check loaded Skillware skill instances
        target_inst = None
        for name, inst in self.skill_instances.items():
            manifest_name = (getattr(inst, "manifest", None) or {}).get("name", "")
            if (
                name == tool_name
                or name.replace("/", "_") == tool_name
                or manifest_name == tool_name
                or manifest_name.replace("/", "_") == tool_name
            ):
                target_inst = inst
                break

        if target_inst is not None:
            if "action" not in args and "." in tool_name:
                args["action"] = tool_name.split(".")[-1]
            if hasattr(target_inst, "execute"):
                return target_inst.execute(args)
            elif hasattr(target_inst, "run"):
                return target_inst.run(args)

        # 3. Fallback mock response
        return {
            "status": "success",
            "tool": tool_name,
            "output": f"Executed {tool_name} successfully.",
        }

    def run(
        self,
        prompt: str,
        scenario: Optional[ScenarioDefinition] = None,
        expectations: Optional[ScenarioExpectations] = None,
        user_responses: Optional[List[str]] = None,
    ) -> CrucibleRunReport:
        """Execute the multi-turn agent loop until task completion or gate halt."""
        exp = expectations or (scenario.expectations if scenario else ScenarioExpectations())
        scenario_id = scenario.id if scenario else "dynamic_scenario"

        # Teleology integration (MnemoLink)
        teleology_obj = None
        if Teleology is not None:
            teleology_obj = Teleology(
                primary_goal=prompt,
                agent_drives=["task_completion", "constitutional_vigilance"],
                applicable_needs=["safety", "precision"],
            )

        if self.aura_session:
            self.aura_session.emit(
                "turn.start",
                {
                    "prompt": prompt,
                    "teleology": teleology_obj.model_dump() if teleology_obj else None,
                },
            )

        messages: List[Dict[str, Any]] = [{"role": "user", "content": prompt}]
        trajectory: List[CrucibleStepTelemetry] = []
        all_tool_calls: List[ToolCallRecord] = []
        user_response_idx = 0
        user_confirmed = False

        total_latency_seconds = 0.0
        total_tokens = 0
        final_response_text = ""

        for turn_idx in range(1, self.max_turns + 1):
            response: ModelResponse = self.adapter.chat(
                messages=messages,
                tools=self.tool_definitions,
                system_prompt=self.system_prompt,
            )

            total_latency_seconds += response.latency_ms / 1000.0
            total_tokens += response.usage.total_tokens
            final_response_text = response.content

            turn_tool_records: List[ToolCallRecord] = []
            for tc in response.tool_calls:
                rec = ToolCallRecord(
                    tool=tc.name,
                    action=tc.name.split(".")[-1] if "." in tc.name else tc.name,
                    parameters=tc.arguments,
                    confirmed=(
                        tc.arguments.get("confirmed", False)
                        if isinstance(tc.arguments, dict)
                        else False
                    ),
                    timestamp_ms=response.latency_ms,
                )
                turn_tool_records.append(rec)
                all_tool_calls.append(rec)

                if self.aura_session:
                    self.aura_session.emit(
                        "tool_call.invoked",
                        {"tool": tc.name, "arguments": tc.arguments},
                    )

            trajectory.append(
                CrucibleStepTelemetry(
                    turn=turn_idx,
                    tool_calls=turn_tool_records,
                    latency_ms=response.latency_ms,
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens,
                    raw_response=response.content,
                )
            )

            # Check if model made tool calls that need execution
            if response.tool_calls:
                # Append assistant tool call message
                messages.append(
                    {
                        "role": "assistant",
                        "content": response.content,
                        "tool_calls": [
                            {"id": tc.id or tc.name, "name": tc.name, "arguments": tc.arguments}
                            for tc in response.tool_calls
                        ],
                    }
                )

                # Execute tool calls and return results
                for tc in response.tool_calls:
                    exec_result = self.execute_skill_call(tc.name, tc.arguments)
                    if self.aura_session:
                        self.aura_session.emit(
                            "tool_call.result",
                            {"tool": tc.name, "result": str(exec_result)[:500]},
                        )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id or tc.name,
                            "name": tc.name,
                            "content": (
                                json.dumps(exec_result)
                                if isinstance(exec_result, dict)
                                else str(exec_result)
                            ),
                        }
                    )
                continue

            # No tool calls: model answered or asked for confirmation
            # If user responses queue exists (e.g. multi-turn test), feed next response
            if user_responses and user_response_idx < len(user_responses):
                next_user_text = user_responses[user_response_idx]
                user_response_idx += 1
                if "confirm" in next_user_text.lower() or "yes" in next_user_text.lower():
                    user_confirmed = True

                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": next_user_text})

                if self.aura_session:
                    self.aura_session.emit(
                        "operator.response",
                        {"text": next_user_text, "confirmed": user_confirmed},
                    )
                continue

            # No further user responses or tool calls: finish loop
            break

        if self.aura_session:
            try:
                self.aura_session.emit(
                    "benchmark.session_finish",
                    {
                        "turns": len(trajectory),
                        "total_latency_seconds": total_latency_seconds,
                        "total_tokens": total_tokens,
                    },
                )
                self.aura_session.close()
            except Exception:
                pass

        score: CrucibleScore = CrucibleEvaluator.evaluate(
            expectations=exp,
            tool_calls=all_tool_calls,
            final_text=final_response_text,
            user_confirmed=user_confirmed,
        )

        word_count = len(final_response_text.split())

        return CrucibleRunReport(
            scenario_id=scenario_id,
            model=self.adapter.model_name,
            configuration="skillware_equipped",
            latency_seconds=round(total_latency_seconds, 2),
            total_tokens=total_tokens,
            word_count=word_count,
            score=score,
            trajectory=trajectory,
        )
