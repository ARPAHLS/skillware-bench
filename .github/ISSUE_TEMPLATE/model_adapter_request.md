---
name: Model Adapter Request
about: Propose support for a new frontier, sovereign, or fine-tuned model provider
title: "[ADAPTER]: Support for <Provider / Model Name>"
labels: ["model adapter", "enhancement"]
assignees: ""
---

## Model Provider Details

- **Provider**: `e.g. Cohere, AWS Bedrock, DeepSeek, vLLM`
- **Model Identifier(s)**: `e.g. command-r-plus, deepseek-r1`
- **Inference Protocol**: Native SDK / OpenAI-Compatible REST / JSON-RPC

## Tool Calling & Schema Capabilities

- Does this model support native structured tool calling (function calling)?
- Does it support cached input tokens?
- Does it report precise token accounting in response metadata?

## Proposed Implementation Plan

- Subclass `BaseModelAdapter` in `skillware_bench/core/adapters/<provider>_adapter.py`
- Add optional dependencies in `pyproject.toml`
- Register with `AdapterRegistry`
- Add unit tests in `tests/bench/test_adapters.py` with mock responses
