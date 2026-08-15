# Session 004 — All Features Complete

> Date: 2026-04-07

## Final Stats

| Metric | Value |
|--------|-------|
| Source files | 50+ |
| Test files | 9 |
| Tests | 57 passing |
| Lines of code | ~6,500+ |
| Runtime deps | 3 (httpx, prompt-toolkit, rich) |
| Providers | 5 (Anthropic, OpenAI, Gemini, Ollama, DeepSeek) |
| Tools | 9 (Bash, Read, Write, Edit, Grep, Glob, ListFiles, WebFetch, Agent) |
| Slash commands | 22 |
| Commits | 25+ |

## Complete Feature List

### Core
- Neutral message types (not coupled to any provider)
- Provider Protocol with AsyncIterator streaming
- Agentic loop: stream → tool calls → execute → loop
- Token budget (90% threshold + diminishing returns)
- Auto-compact (LLM summarization, keep last 10 messages)
- Microcompact (clear old tool results at 70%)
- Read-before-write enforcement with mtime staleness
- Full typing: mypy --strict passes

### Providers
- Anthropic (direct API, OAuth subscription support)
- OpenAI (full message/tool conversion, SSE state machine)
- Gemini (OpenAI-compat endpoint)
- Ollama (local, no API key)
- DeepSeek (OpenAI-compat)

### Authentication
- OAuth PKCE flow (same client ID as Claude Code)
- Token storage at ~/.clawpy/credentials.json
- Auto-refresh with 5-minute buffer
- Required beta headers (oauth-2025-04-20, claude-code-20250219)
- Billing attribution in system prompt

### Tools
- Bash (timeout, read-only detection, sandbox-aware)
- Read (line numbers, offset/limit, file state tracking)
- Write (read-before-write, mtime check)
- Edit (diff preview, uniqueness check, staleness guard)
- Grep (ripgrep, 3 output modes, head_limit)
- Glob (mtime sorted, 1000 cap)
- ListFiles (dirs-first sorting)
- WebFetch (HTML→text, 100K truncation)
- Agent (background/foreground, task tracking, heartbeat)

### Task System
- TaskRegistry: track running/completed/killed agents
- Background agents with asyncio.Task
- 15-second heartbeat for long-running background tasks
- /tasks, /bg, /fg, /kill commands

### Memory System
- CLAWPY.md discovery (CWD→root + global)
- /memory list, add, edit, show, reload
- Dream: LLM-powered memory consolidation
- Auto-dream: triggers after 10+ turns, 24h since last
- Memory reload without conversation reset

### Plugins
- Install from GitHub repos or local directories
- plugin.json manifest with commands/agents/skills
- /plugin install, list, remove, enable, disable, info

### MCP
- JSON-RPC 2.0 client over stdio
- Tool discovery and execution
- Config from .clawpy/mcp.json

### Custom Agents
- .clawpy/agents/*.md with YAML frontmatter
- /agents to list discovered definitions

### UX
- ClawPy amber/orange branding
- prompt_toolkit async REPL with history
- Tab completion for /commands and @files
- Interactive permission prompts (Y/n/always)
- File edit diff preview (unified diff)
- Streaming with cost display per turn
- Session persistence + /resume
- Cost tracking with per-model pricing
- Git-aware system prompt (branch, status, commits)
- Microcompact at 70% context
- Terminal bell on background agent completion
- Ctrl+C graceful interrupt
- 22 slash commands

### Slash Commands
/model, /tasks, /bg, /fg, /kill, /usage, /status, /context,
/memory, /dream, /plan, /clear, /compact, /plugin, /resume,
/agents, /mcp, /login, /logout, /help, /quit
