# Session 001 — Phase 1 Complete

> Date: 2026-04-06
> Duration: ~1 session
> Phase: 1 (Core loop — types, provider, tools, engine, CLI)

## What Was Done

### Files Created (18 files, ~900 lines)
- `pyproject.toml` — PEP 621, 3 runtime deps (httpx, prompt-toolkit, rich)
- `.gitignore`
- `src/clawpy/__init__.py`, `__main__.py`
- `src/clawpy/types.py` — Message, ContentBlock, ToolCall, ToolResult, Role (neutral format)
- `src/clawpy/provider/base.py` — Provider Protocol, Request, Response, StreamEvent, Usage
- `src/clawpy/provider/registry.py` — name→factory registry
- `src/clawpy/provider/sse.py` — shared SSE parser (async generator over httpx lines)
- `src/clawpy/provider/anthropic.py` — Anthropic Messages API (direct httpx, no SDK)
- `src/clawpy/tool/base.py` — Tool Protocol, Permission IntEnum, RunContext
- `src/clawpy/tool/registry.py` — ToolRegistry with ordered insertion
- `src/clawpy/tool/permission.py` — PermissionEnforcer (4 modes: default/accept_edits/bypass/plan)
- `src/clawpy/tool/bash.py` — shell exec with timeout, read-only detection
- `src/clawpy/tool/file_read.py` — file read with cat -n format, offset/limit
- `src/clawpy/tool/grep_tool.py` — ripgrep wrapper, 3 output modes, head_limit
- `src/clawpy/tool/glob_tool.py` — file glob, sorted by mtime
- `src/clawpy/engine/engine.py` — Engine class with agentic loop, stream consumer, tool executor
- `src/clawpy/config/config.py` — layered config (defaults < global < project < env)
- `src/clawpy/config/paths.py` — XDG-aware paths
- `src/clawpy/cli.py` — argparse CLI with `run` and REPL modes

### Key Design Decisions Made
1. **Neutral internal format** — not Anthropic-mirrored. Each provider owns conversion.
2. **dataclass(slots=True, frozen=True)** for immutable types, plain slots for mutable.
3. **AsyncIterator[StreamEvent]** for streaming — natural Python async for.
4. **No SDK dependencies** — direct httpx to APIs. Reduces dependency surface.
5. **Permission as IntEnum** — enables `<=` comparisons for level checking.
6. **Usage.__add__** — accumulate token counts naturally.

### What Worked Well
- Provider Protocol + registry pattern is clean and extensible
- SSE parser is ~30 lines, handles both Anthropic and OpenAI formats
- Engine's stream consumer state machine maps 1:1 from openaiShim.ts
- Tool partitioning (concurrent read-only batches) is simple with asyncio.gather

### What Needs Improvement (Found Later from Spec Review)
- No read_file_state tracking → FileEdit/Write can't enforce read-before-write
- No token budget → loop runs until max_iterations (50) blindly
- No auto-compact → context window will overflow on long conversations
- No recovery paths → errors are fatal
- System prompt is a hardcoded string → needs multi-section assembly + memory
- REPL is basic input() → needs prompt_toolkit with async streaming

### Verification
```bash
uv run python -c "from clawpy.cli import main; print('Import OK')"  # ✅
uv run python -c "from clawpy.types import text_message, Role; m = text_message(Role.USER, 'hello'); assert m.text_content() == 'hello'"  # ✅
uv run python -c "from clawpy.cli import _build_tools; t = _build_tools(); print(len(t), [x.name for x in t.all()])"  # ✅ 4 tools
```

### Commits
- `8fb9347` — Phase 1: Core architecture — types, provider, tools, engine, CLI
- `08fcf17` — Add .gitignore, remove cached bytecode from tracking
- `4c21adc` — Add spec and plan docs from architecture review

### Research Done (for future optimization)
- Read OpenClaude's openaiShim.ts (1200+ lines) — full SSE state machine
- Read OpenClaude's Tool.ts (493 lines) — 42+ method interface, we kept 6
- Read OpenClaude's query.ts (69KB) — core async generator loop
- Read OpenClaude's toolOrchestration.ts — partition + concurrent execution
- Read claw-code's Provider trait, OpenAiCompatClient, ToolSpec, PermissionEnforcer
- Read all 14 claurst spec files (~990KB total)
- Key insight: OpenClaude's shim pattern (force everything into Anthropic types) creates coupling. Our neutral format is cleaner.
