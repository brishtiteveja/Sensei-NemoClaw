# ClawPy: Typed Python Rewrite of OpenClaude

> Plan doc — updated as implementation progresses.
> Last updated: 2026-04-06

## Progress

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1** | **DONE** | Core loop — types, provider, tools, engine, CLI |
| Phase 2 | Pending | REPL + remaining tools + read-file-state + memory |
| Phase 3 | Pending | Multi-model (OpenAI, Gemini, Ollama, DeepSeek providers) |
| Phase 4 | Pending | Token budget, auto-compact, recovery paths |
| Phase 5 | Pending | Sessions, hooks, agent tool, tests, mypy strict |

### Gaps Found from claurst Spec Review

These were missing from the original plan and are now incorporated:

1. **Read-before-write enforcement** — FileEdit/FileWrite must check `read_file_state`
   (populated by FileRead). Reject edits if file modified since last read. (Phase 2)
2. **Token budget management** — COMPLETION_THRESHOLD=0.9, DIMINISHING_THRESHOLD=500.
   Stop loop when approaching context limit or diminishing returns. (Phase 4)
3. **Auto-compact** — Trigger at 90% context window. Summarize old messages via LLM,
   keep last 10 messages. Circuit breaker after 3 failures. (Phase 4)
4. **Recovery paths** — Max output tokens retry (3x with escalation), reactive compact
   for prompt-too-long, rate limit backoff. (Phase 4)
5. **CLAWPY.md memory** — Walk CWD→root collecting memory files, inject into system prompt.
   Global memory at ~/.clawpy/CLAWPY.md. (Phase 2)
6. **System prompt assembly** — Multi-section: identity + task guidance + tool rules +
   memory + environment info. Cacheable static vs dynamic sections. (Phase 2)
7. **Hooks system** — PreToolUse/PostToolUse shell hooks with env vars and condition matching. (Phase 5)
8. **Session persistence** — JSONL transcript with session_meta, message, compact entries. (Phase 5)
9. **Slash commands** — /compact, /context, /plan, /resume beyond basic /quit /clear /model. (Phase 2)

### Spec Documentation

Full spec at `/home/projects/claude-exp/docs/clawpy-spec/`:
- `INDEX.md` — quick reference, architecture diagram
- `00_overview.md` — architecture, layers, design decisions
- `01_types_messages.md` — Message, ContentBlock, ToolCall, ToolResult
- `02_provider.md` — Provider Protocol, SSE, multi-model conversion
- `03_tools.md` — Tool Protocol, permissions, execution orchestration
- `04_engine.md` — agentic loop, token budget, auto-compact, recovery
- `05_config_memory.md` — config layers, CLAWPY.md, session persistence
- `06_cli_repl.md` — CLI, REPL, slash commands, UI rendering
- `07_hooks_agents.md` — hooks, sub-agents, MCP (future)

### Phase 1 — Completed Files
- `pyproject.toml`, `.gitignore`
- `src/clawpy/types.py` — Message, ContentBlock, ToolCall, ToolResult
- `src/clawpy/provider/base.py` — Provider Protocol, Request, Response, StreamEvent
- `src/clawpy/provider/registry.py` — provider name → factory registry
- `src/clawpy/provider/sse.py` — shared SSE line parser (async generator)
- `src/clawpy/provider/anthropic.py` — Anthropic Messages API (direct httpx, no SDK)
- `src/clawpy/tool/base.py` — Tool Protocol, Permission enum
- `src/clawpy/tool/registry.py` — ToolRegistry
- `src/clawpy/tool/permission.py` — PermissionEnforcer with 4 modes
- `src/clawpy/tool/bash.py` — shell execution with timeout + read-only detection
- `src/clawpy/tool/file_read.py` — file read with line numbers, offset, limit
- `src/clawpy/tool/grep_tool.py` — ripgrep wrapper with output modes
- `src/clawpy/tool/glob_tool.py` — file glob search
- `src/clawpy/engine/engine.py` — agentic loop (stream → tools → loop)
- `src/clawpy/config/config.py` — layered config (global/project/env/CLI)
- `src/clawpy/config/paths.py` — XDG-aware config paths
- `src/clawpy/cli.py` — argparse CLI with `run` and REPL modes

---

## Context

OpenClaude (TypeScript) is a fork of Claude Code that adds multi-model support. Claw-code (Rust) is a ground-up rewrite. ClawPy is an idiomatic, fully-typed Python rewrite at `/home/projects/claude-exp/clawpy`.

**Key architectural patterns preserved from OpenClaude/claw-code:**
1. Provider abstraction with streaming — normalize all LLM APIs to a common internal format
2. Agentic loop: stream response → extract tool calls → execute → feed results → loop
3. Tool interface with permission enforcement
4. Layered config (global + project + env + CLI flags)

**Key design decisions for Python:**
- **Full typing everywhere** — `Protocol` classes, `dataclass`, `slots=True`, `frozen=True`
- **Neutral internal format** (not Anthropic-mirrored) — avoids the shim coupling OpenClaude has
- **`asyncio` native** — streaming via `AsyncIterator[StreamEvent]`, concurrent tools via `asyncio.gather()`
- **`httpx`** for async HTTP — SSE streaming via `aiter_lines()`
- **`prompt_toolkit`** for REPL, **`rich`** for rendering
- **4 runtime deps only**: httpx, prompt-toolkit, rich (no SDK deps — direct API via httpx)
- **`uv`** for all package management

---

## Architecture

### Project Structure

```
clawpy/
  pyproject.toml
  src/clawpy/
    __init__.py
    __main__.py                     # python -m clawpy
    cli.py                          # argparse CLI (run / repl / version)
    types.py                        # Message, ContentBlock, ToolCall, ToolResult, Role

    config/
      config.py                     # Config model, load(), layered merge
      paths.py                      # ~/.clawpy paths

    provider/
      base.py                       # Provider Protocol, Request, Response, StreamEvent
      registry.py                   # name → factory registry
      sse.py                        # Shared SSE parser
      anthropic.py                  # ✅ Anthropic Messages API
      openai.py                     # OpenAI Chat Completions (Phase 3)
      gemini.py                     # Gemini via OpenAI-compat (Phase 3)
      ollama.py                     # Ollama local (Phase 3)
      deepseek.py                   # DeepSeek (Phase 3)

    tool/
      base.py                       # Tool Protocol, Permission enum
      registry.py                   # ToolRegistry
      permission.py                 # PermissionEnforcer
      bash.py                       # ✅ Shell execution
      file_read.py                  # ✅ File read with line numbers
      file_write.py                 # File write (Phase 2)
      file_edit.py                  # Search/replace (Phase 2)
      glob_tool.py                  # ✅ File glob search
      grep_tool.py                  # ✅ Ripgrep wrapper
      list_files.py                 # Directory listing (Phase 2)
      web_fetch.py                  # HTTP fetch (Phase 2)
      ask_user.py                   # Interactive question (Phase 2)
      agent.py                      # Sub-agent (Phase 4)

    engine/
      engine.py                     # ✅ Agentic loop
      system_prompt.py              # System prompt assembly (Phase 2)

    session/
      session.py                    # JSONL persistence (Phase 4)

    ui/
      repl.py                       # prompt_toolkit REPL (Phase 2)
      render.py                     # rich markdown rendering (Phase 2)
```

### Core Interfaces

**Provider** (`provider/base.py`):
```python
class Provider(Protocol):
    @property
    def name(self) -> str: ...
    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]: ...
    async def send(self, request: Request) -> Response: ...
    def models(self) -> list[str]: ...
```
- `StreamEvent` = discriminated union: DELTA | TOOL_START | TOOL_DELTA | TOOL_END | MESSAGE_STOP | ERROR
- Each provider converts to/from neutral types in its own file

**Tool** (`tool/base.py`):
```python
class Tool(Protocol):
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    def input_schema(self) -> dict[str, Any]: ...
    def permission_for(self, input: dict[str, Any]) -> Permission: ...
    def is_read_only(self, input: dict[str, Any]) -> bool: ...
    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult: ...
```
- Permission levels: READ_ONLY < WORKSPACE_WRITE < SHELL_SAFE < SHELL_UNSAFE < DANGEROUS

**Engine** (`engine/engine.py`):
- `run_turn(user_input, on_stream)` → agentic loop until end_turn or max iterations
- `_consume_stream()` → state machine assembling assistant Message from stream
- `_execute_tools()` → partition into concurrent (read-only) / serial batches

### Agentic Loop Flow
```
User input → append to messages
  ↓
Build Request (system + messages + tool specs)
  ↓
Provider.stream() → consume StreamEvents → assemble assistant Message
  ↓
Extract tool calls from assistant message
  ↓
No tool calls? → return (done)
  ↓
Permission check each tool → execute (read-only concurrent, writes serial)
  ↓
Append tool results as user message → loop back to Build Request
```

---

## Implementation Phases (Detail)

### Phase 2 — REPL + remaining tools + memory + system prompt
- `src/clawpy/ui/repl.py` — prompt_toolkit REPL with async streaming + rich Live rendering
- `src/clawpy/ui/render.py` — markdown/code rendering via rich
- `src/clawpy/tool/file_write.py` — write entire file (with read-before-write enforcement)
- `src/clawpy/tool/file_edit.py` — search/replace (uniqueness + read-before-write + mtime check)
- `src/clawpy/tool/list_files.py` — directory listing
- `src/clawpy/tool/ask_user.py` — prompt user with question
- `src/clawpy/tool/web_fetch.py` — HTTP fetch via httpx (HTML→text, 100K truncation)
- `src/clawpy/engine/system_prompt.py` — multi-section system prompt assembly + CLAWPY.md memory
- `src/clawpy/engine/file_state.py` — read_file_state tracking for edit/write enforcement
- Slash commands: /compact, /context, /plan, /help

### Phase 3 — Multi-model providers
- `src/clawpy/provider/openai.py` — OpenAI Chat Completions
  - `_convert_messages()`: neutral → OpenAI format (mirrors openaiShim.ts convertMessages)
  - `_convert_tools()`: ToolSpec → OpenAI function format (normalize required fields)
  - `_map_chunk()`: OpenAI SSE → neutral StreamEvent (mirrors openaiStreamToAnthropic state machine)
- `src/clawpy/provider/gemini.py` — Gemini via OpenAI-compat endpoint
- `src/clawpy/provider/ollama.py` — Ollama local with auto-discovery
- `src/clawpy/provider/deepseek.py` — DeepSeek with reasoning support

### Phase 4 — Token budget, auto-compact, recovery
- `src/clawpy/engine/token_budget.py` — budget tracking (0.9 threshold, diminishing returns)
- `src/clawpy/engine/compact.py` — auto-compact (summarize old messages, keep last 10)
- `src/clawpy/engine/recovery.py` — max_tokens retry, reactive compact, rate limit backoff
- Integrate into engine loop

### Phase 5 — Sessions, hooks, agent, tests
- `src/clawpy/session/session.py` — JSONL transcript persistence
- `src/clawpy/session/history.py` — session history for /resume
- `src/clawpy/engine/hooks.py` — PreToolUse/PostToolUse shell hooks
- `src/clawpy/tool/agent.py` — sub-agent delegation (filtered tools, isolated context)
- Unit tests for message conversion, tool registry, permission enforcer, config
- `mypy --strict` passing on entire codebase

---

## Verification Checklist

- [ ] Phase 1: `echo "List files" | uv run clawpy run` → Anthropic + tools → answer
- [ ] Phase 2: `uv run clawpy` → interactive REPL with streaming + `/model` + `/quit`
- [ ] Phase 3: `CLAWPY_PROVIDER=openai uv run clawpy run -m gpt-4o "hello"` works
- [ ] Phase 4: `uv run mypy --strict src/` passes, `uv run pytest` passes
- [ ] Permissions: `--permission-mode=plan` blocks all write tools

---

## Reference: Source Project Architecture Mapping

| Subsystem | OpenClaude (TS) | Claw-code (Rust) | ClawPy (Python) |
|-----------|----------------|-------------------|-----------------|
| Provider interface | `src/services/api/client.ts` | `rust/crates/api/src/providers/mod.rs` | `provider/base.py` |
| OpenAI shim | `src/services/api/openaiShim.ts` | `rust/crates/api/src/providers/openai_compat.rs` | `provider/openai.py` |
| Tool type | `src/Tool.ts` | `rust/crates/tools/src/lib.rs` | `tool/base.py` |
| Tool registry | `src/tools.ts` | `GlobalToolRegistry` | `tool/registry.py` |
| Tool orchestration | `src/services/tools/toolOrchestration.ts` | (inline) | `engine/engine.py` |
| Query loop | `src/query.ts` | `runtime/` | `engine/engine.py` |
| Config | `src/utils/config.ts` | `runtime/src/config.rs` | `config/config.py` |
| System prompt | `src/constants/prompts.ts` | (inline) | `engine/system_prompt.py` |
| Permissions | `src/utils/permissions/` | `runtime/src/permissions.rs` | `tool/permission.py` |
