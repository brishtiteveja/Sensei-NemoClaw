# ClawPy Specification — Quick Reference

> Python rewrite of Claude Code, informed by OpenClaude (TS), claw-code (Rust), and claurst specs.
> Last updated: 2026-04-06

## Spec Files

| File | Scope | Status |
|------|-------|--------|
| [00_overview.md](00_overview.md) | Architecture overview, data flow, design decisions | Done |
| [01_types_messages.md](01_types_messages.md) | Core types, message format, content blocks | Done |
| [02_provider.md](02_provider.md) | Provider abstraction, SSE streaming, multi-model | Done |
| [03_tools.md](03_tools.md) | Tool system, permissions, execution orchestration | Done |
| [04_engine.md](04_engine.md) | Agentic loop, token budget, auto-compact, recovery | Done |
| [05_config_memory.md](05_config_memory.md) | Configuration, CLAUDE.md memory, session persistence | Done |
| [06_cli_repl.md](06_cli_repl.md) | CLI, REPL, slash commands, UI rendering | Done |
| [07_hooks_agents.md](07_hooks_agents.md) | Hooks system, sub-agents, MCP (future) | Done |

## Key Metrics (Target)

| Metric | Value |
|--------|-------|
| Runtime deps | 3 (httpx, prompt-toolkit, rich) |
| Python version | ≥ 3.12 |
| Type checking | mypy --strict |
| MVP tools | 10 |
| MVP providers | 5 (Anthropic, OpenAI, Gemini, Ollama, DeepSeek) |
| Total files (est.) | ~40 |

## Architecture at a Glance

```
User input
  │
  ▼
CLI (argparse) ─── /commands ──► local handlers
  │
  ▼
Engine.run_turn()
  │
  ├─► Build Request (system prompt + messages + tool specs)
  │
  ├─► Provider.stream() ──► SSE ──► StreamEvent channel
  │
  ├─► Consume stream ──► assemble assistant Message
  │
  ├─► Extract ToolCalls
  │     │
  │     ├─► PermissionEnforcer.check()
  │     ├─► PreToolUse hooks
  │     ├─► Tool.run() [concurrent if read-only]
  │     └─► PostToolUse hooks
  │
  ├─► Append ToolResults as user message
  │
  ├─► Token budget check / auto-compact if needed
  │
  └─► Loop until end_turn or max_iterations
```
