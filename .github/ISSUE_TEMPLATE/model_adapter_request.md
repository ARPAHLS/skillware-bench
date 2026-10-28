---
name: Model Adapter Request
about: Propose support for a new frontier, sovereign, or fine-tuned model provider
title: "[ADAPTER]: Support for <Provider / Model Name>"
labels: ["model adapter", "enhancement"]
assignees: ""
---

## Model Provider Details

- **Provider / Host**: `e.g. Cohere, AWS Bedrock, DeepSeek, vLLM, Ollama`
- **Model Identifier(s)**: `e.g. command-r-plus, deepseek-r1`
- **Capability Tier**: `Frontier` / `Enterprise` / `Compact` / `Edge`
- **Inference Protocol**: Native SDK / OpenAI-Compatible REST / JSON-RPC

## Tool Calling & Schema Capabilities

- Does this model support native structured tool calling (function calling)?
- Does it support cached input tokens (prompt cache hits)?
- Does it report exact token accounting in response metadata (`prompt_tokens`, `completion_tokens`, `cached_tokens`)?

## Vanilla Baseline Invariant

- [ ] Confirmed: Vanilla baseline will receive strictly raw agent primitives (`execute_python` and `http_request`) with no prompt-side spoon-feeding or pre-packaged domain parsing tools.

## Proposed Implementation Plan

- [ ] Subclass `BaseModelAdapter` in `skillware_bench/core/adapters/<provider>_adapter.py`
- [ ] Add optional provider dependencies in `pyproject.toml` under `[project.optional-dependencies]` and `all`
- [ ] Register with `AdapterRegistry.register("provider/prefix", AdapterClass)`
- [ ] Implement `execute_with_retry` for exponential backoff on HTTP 429/500/503 errors
- [ ] Add unit tests in `tests/bench/test_adapters.py` verifying token parsing and response structure
- [ ] Document model configuration in `docs/results/models/<model>.md`
