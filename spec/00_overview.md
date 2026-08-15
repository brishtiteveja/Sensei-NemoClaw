# 00 — Architecture Overview

## What ClawPy Is

ClawPy is a multi-model CLI coding agent written in typed Python. It is a ground-up rewrite
informed by three reference implementations:
- **OpenClaude** (TypeScript) — fork of Claude Code with multi-model shim
- **claw-code** (Rust) — ground-up rewrite with native multi-provider
- **claurst** — spec-driven Rust rewrite with 8 crates

## Design Principles

1. **Neutral internal format** — not coupled to any provider's API shape
2. **Full typing** — `Protocol`, `dataclass(slots=True)`, `mypy --strict`
3. **Async-native** — `asyncio` for streaming, concurrent tool execution
4. **Minimal deps** — 3 runtime packages (httpx, prompt-toolkit, rich)
5. **No SDK deps** — talk to LLM APIs directly via httpx
6. **Provider-agnostic** — switch models via config/env/CLI flag

## Layer Architecture

```
┌─────────────────────────────────────────────┐
│  CLI / REPL  (argparse + prompt_toolkit)    │  ← User interaction
├─────────────────────────────────────────────┤
│  Slash Commands  (/model, /clear, /compact) │  ← Local command dispatch
├─────────────────────────────────────────────┤
│  Engine  (agentic loop)                     │  ← Core turn cycle
│    ├── Token budget / auto-compact          │
│    ├── Stream consumer (state machine)      │
│    └── Tool executor (concurrent batching)  │
├─────────────────────────────────────────────┤
│  Tool System                                │  ← 10+ tools
│    ├── Registry + ToolSpec generation       │
│    ├── Permission Enforcer                  │
│    └── Pre/Post hooks                       │
├─────────────────────────────────────────────┤
│  Provider Layer                             │  ← Multi-model
│    ├── Provider Protocol (stream/send)      │
│    ├── SSE parser (shared)                  │
│    └── Per-provider conversion (convert.py) │
├─────────────────────────────────────────────┤
│  Config / Memory / Session                  │  ← Persistence
│    ├── Layered JSON config                  │
│    ├── CLAWPY.md memory discovery           │
│    └── JSONL session transcripts            │
└─────────────────────────────────────────────┘
```

## Data Flow — Single Turn

1. User types prompt (REPL) or pipes stdin (`clawpy run`)
2. If slash command → dispatch to local handler, skip LLM
3. Engine appends user message to history
4. Engine builds `Request` (system prompt + messages + tool specs)
5. Provider streams response as `AsyncIterator[StreamEvent]`
6. Engine consumes stream → assembles assistant `Message`
   - Text deltas → buffer
   - Tool start/delta/end → accumulate JSON → finalize `ToolCall`
7. Extract `ToolCall` list from assistant message
8. If no tool calls or `stop_reason == end_turn` → done
9. For each tool call:
   a. Permission check (enforcer + hooks)
   b. Execute tool (read-only concurrent via `asyncio.gather`, writes serial)
   c. Collect `ToolResult`
10. Append tool results as user message
11. Check token budget / auto-compact threshold
12. Loop back to step 4

## Key Differences from Reference Implementations

| Aspect | OpenClaude (TS) | claw-code (Rust) | ClawPy (Python) |
|--------|----------------|-------------------|-----------------|
| Internal format | Anthropic SDK types | Neutral structs | Neutral dataclasses |
| Streaming | async generator | tokio channel (256) | AsyncIterator |
| Tool dispatch | Object with function fields | match on name | Protocol + registry |
| Concurrency | Promise.all | tokio::join | asyncio.gather |
| UI framework | React + Ink | ratatui | prompt_toolkit + rich |
| Config | Bun bundler feature flags | cargo features | env vars + JSON |
| Type validation | Zod | serde | dataclass + runtime checks |

## What We Explicitly Skip (MVP)

- React/Ink terminal framework (use prompt_toolkit + rich instead)
- Voice/STT input
- Bridge protocol (remote control from claude.ai)
- Plugin/marketplace system
- IDE integration (MCP bridge)
- GrowthBook feature flags
- Analytics/telemetry pipeline
- Buddy/tamagotchi system
- Vim mode input
- Worktree isolation
- Team/swarm multi-agent orchestration
- Cron scheduling
