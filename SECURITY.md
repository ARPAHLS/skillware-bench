# Security Policy

## Supported Versions

Skillware-Bench follows semantic versioning. We provide security updates and patches for supported releases.

| Version | Supported | Description |
| :--- | :---: | :--- |
| **0.1.x** | Yes | Active development and initial benchmark release |

## Benchmark Safety & Isolation Principles

Evaluating frontier models on actionable, real-world tools requires rigorous safety guardrails:

1. **Zero Secret Leakage in Trajectories**:
   - The benchmark harness automatically strips, masks, and sanitizes API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GMAIL_APP_PASSWORD`, `COMPANIES_HOUSE_API_KEY`, etc.) from model logs, step traces, and generated artifacts.
   - Grounded evaluation artifacts published to the public repository or leaderboard must never contain raw environment variables or credentials.

2. **Dedicated Test Environs & Sandboxing**:
   - Live simulations (e.g. `office/gmail_handler`, EVM, or file operations) must execute against **dedicated test fixtures, disposable agent mailboxes, or local testnets**.
   - Offline benchmark modes (`--mock`) run entirely in-process using recorded mock transports, completely isolated from external network calls.

3. **Permissive Fortress Alignment**:
   - Skills tested by this harness adhere to the Skillware **Permissive Fortress** architecture: credential resolution occurs through explicit host-injected providers, AST safety rules block dangerous execution primitives (`eval`, `exec`), and all tool invocations are audited.

4. **Negative Controls & Ambiguous Gate Testing**:
   - In benchmark crucibles testing safety gates (e.g., `confirm_before_send`), the harness verifies that the model cannot bypass safety rules or synthesize unauthorized confirmation flags.

## Reporting a Vulnerability

If you discover a security vulnerability, credential leak, or sandbox escape in Skillware-Bench:

1. **Do NOT open a public GitHub issue.**
2. Send an email to **[security@arpacorp.net](mailto:security@arpacorp.net)** with full technical details.
3. Include a minimal reproducible proof-of-concept (PoC) if available.

We will acknowledge your report within 48 hours and coordinate a coordinated disclosure and patch timeline.
