# Session 002 — Phases 2-4 Complete

> Date: 2026-04-06
> Phase: 2 (REPL + tools + memory), 3 (multi-model), 4 (budget + compact)

## What Was Done

### Phase 2 — REPL + remaining tools + memory + system prompt
**New files:**
- `engine/file_state.py` — FileStateTracker for read-before-write enforcement
- `engine/system_prompt.py` — multi-section system prompt + CLAWPY.md memory discovery
- `tool/file_write.py` — write with read-before-write guard + mtime staleness
- `tool/file_edit.py` — search/replace with uniqueness + staleness checks
- `tool/list_files.py` — directory listing sorted dirs-first
- `tool/web_fetch.py` — HTTP fetch with HTML→text, 100K truncation
- `ui/repl.py` — prompt_toolkit async REPL with rich streaming + slash commands

**Modified files:**
- `tool/file_read.py` — now registers files in FileStateTracker
- `engine/engine.py` — added file_state, clears on /clear
- `cli.py` — 8 tools, new system prompt builder, rich REPL

**Key decisions:**
- FileState uses mtime + content hash for staleness detection
- System prompt has 4 static sections + memory + environment (6 total)
- Memory walks CWD→root collecting CLAWPY.md files
- REPL uses prompt_toolkit for input, plain print() for streaming (simpler than rich.Live)

### Phase 3 — Multi-model providers
**New files:**
- `provider/openai.py` — full OpenAI Chat Completions with conversion + SSE state machine
- `provider/gemini.py` — inherits OpenAI, Gemini endpoint
- `provider/ollama.py` — inherits OpenAI, local endpoint
- `provider/deepseek.py` — inherits OpenAI, DeepSeek endpoint

**Key decisions:**
- OpenAI provider is the base class for all OpenAI-compatible providers
- `_convert_messages()` mirrors openaiShim.ts: tool_calls, tool results, thinking stripped
- `_normalize_schema()` adds all properties to required (OpenAI strict mode)
- Stream state machine tracks `active_tool_calls` by index, accumulates JSON, finalizes on finish_reason
- Gemini/Ollama/DeepSeek only override __init__ with different URLs/keys

### Phase 4 — Token budget + auto-compact
**New files:**
- `engine/token_budget.py` — TokenBudget with 90% threshold + diminishing returns
- `engine/compact.py` — auto_compact() summarizes old messages, keeps last 10

**Key decisions:**
- Context windows hardcoded per model family (200K Claude, 128K GPT-4o, 1M Gemini, 64K DeepSeek)
- Diminishing returns: stop if <500 tokens produced after 3+ continuations
- Auto-compact uses a non-streaming LLM call with "no tools" system prompt
- Circuit breaker: max 3 consecutive compact failures before giving up

## Cumulative Stats

| Metric | Value |
|--------|-------|
| Total files | 28 Python files |
| Total lines | ~2,900 |
| Runtime deps | 3 (httpx, prompt-toolkit, rich) |
| Providers | 5 (anthropic, openai, gemini, ollama, deepseek) |
| Tools | 8 (Bash, Read, Write, Edit, Grep, Glob, ListFiles, WebFetch) |
| Commits | 7 total |

## Remaining (Phase 5)
- Session persistence (JSONL)
- Hooks system (PreToolUse/PostToolUse)
- Agent sub-tool
- Unit tests
- mypy --strict

## Discoveries During Implementation
1. OpenAI `stream_options: {include_usage: true}` is needed to get token counts in streaming
2. OpenAI tool_calls use `index` for delta correlation, not `id` (id only on first chunk)
3. finish_reason must finalize ALL accumulated tool calls at once
4. Gemini/Ollama/DeepSeek all work with the same OpenAI conversion code (zero extra logic)
5. Auto-compact needs to use `provider.send()` (non-streaming) since it's a background operation
