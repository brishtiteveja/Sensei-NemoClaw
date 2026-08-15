<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/mypy-strict-green?style=flat-square" />
  <img src="https://img.shields.io/badge/deps-3%20only-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/providers-5-purple?style=flat-square" />
  <img src="https://img.shields.io/github/license/AIScienceStudio/clawpy?style=flat-square" />
  <img src="https://img.shields.io/github/stars/AIScienceStudio/clawpy?style=flat-square" />
</p>

<h1 align="center">ClawPy</h1>
<p align="center"><strong>The Python AI coding agent that works with any model.</strong></p>
<p align="center">Claude, GPT-4o, Gemini, Ollama, DeepSeek — one tool, any brain.</p>

---

```
pip install clawpy   # or: git clone + uv pip install -e .
clawpy login         # use your Claude subscription (or set any API key)
clawpy               # start coding with AI
```

<!-- TODO: Replace with actual demo GIF
<p align="center">
  <img src="docs/demo.gif" width="700" />
</p>
-->

## Why ClawPy?

Every AI coding agent locks you into one provider. ClawPy doesn't.

| | ClawPy | Claude Code | Cursor | Aider |
|---|:---:|:---:|:---:|:---:|
| Pure Python | **Yes** | TypeScript | Electron | Python |
| Multi-model (5 providers) | **Yes** | Claude only | OpenAI + Claude | Multi |
| Claude subscription login | **Yes** | Yes | No | No |
| Runs locally with Ollama | **Yes** | No | No | Yes |
| Plugin system | **Yes** | Yes | No | No |
| Background agents | **Yes** | Yes | No | No |
| Memory consolidation (dream) | **Yes** | Yes | No | No |
| MCP support | **Yes** | Yes | No | No |
| Dependencies | **3** | 200+ | Electron | 20+ |
| `mypy --strict` | **Yes** | No | No | No |

## Quickstart

**30 seconds to your first AI-powered code change:**

```bash
# Install
git clone https://github.com/AIScienceStudio/clawpy.git && cd clawpy
uv venv && uv pip install -e .

# Authenticate (pick one)
clawpy login                              # Claude Pro/Max/Team subscription
export OPENAI_API_KEY=sk-...              # or OpenAI
export GEMINI_API_KEY=AIza...             # or Gemini
# Ollama needs no key — just have it running

# Run
clawpy
```

That's it. You're in.

## What it looks like

```
  ClawPy  v0.1.0
  /home/user/myproject
  model: Opus 4.6 via anthropic

> Find the bug in auth.py and fix it

  >> Read src/auth.py  3s
  >> Grep "password"  4s
  >> Edit src/auth.py  6s

  Found the issue: the password hash comparison was using == instead
  of hmac.compare_digest(), making it vulnerable to timing attacks.
  Fixed it.

  --- src/auth.py
  +++ src/auth.py
  @@ -42,1 +42,1 @@
  -    if stored_hash == computed_hash:
  +    if hmac.compare_digest(stored_hash, computed_hash):

  1,808in 65out  $0.031
```

## Switch models in one command

```bash
clawpy -p openai -m gpt-4o          # OpenAI
clawpy -p gemini -m gemini-2.5-pro  # Google (1M context!)
clawpy -p ollama -m llama3.1        # Local, free, private
clawpy -p deepseek -m deepseek-chat # DeepSeek V3
clawpy                               # Claude (default)
```

Or switch mid-conversation:
```
> /model gemini-2.5-pro
  model  Gemini 2.5 Pro  1M context, multimodal
```

## Features

<details>
<summary><strong>9 built-in tools</strong></summary>

| Tool | What it does | Permission |
|------|-------------|------------|
| **Bash** | Execute shell commands | Dynamic (safe commands auto-approved) |
| **Read** | Read files with line numbers | Read-only |
| **Write** | Write/create files | Workspace write |
| **Edit** | Search & replace with diff preview | Workspace write |
| **Grep** | Search contents (ripgrep) | Read-only |
| **Glob** | Find files by pattern | Read-only |
| **ListFiles** | List directory contents | Read-only |
| **WebFetch** | Fetch URL content | Requires approval |
| **Agent** | Spawn sub-agents (background OK) | Requires approval |

</details>

<details>
<summary><strong>22 slash commands</strong></summary>

| Command | Description |
|---------|-------------|
| `/model [name]` | Pick a model or list all available |
| `/tasks [id]` | List running agents or view output |
| `/bg` / `/fg` / `/kill` | Background/foreground/kill agents |
| `/usage` | Claude subscription rate limits |
| `/status` | Session info, auth, cost |
| `/context` | Context window usage with breakdown |
| `/memory` | View, edit, add persistent memory |
| `/dream` | LLM-powered memory consolidation |
| `/plan` | Toggle read-only plan mode |
| `/resume` | Resume a previous session |
| `/plugin` | Install/manage plugins |
| `/agents` | List custom agent definitions |
| `/mcp` | Show MCP server configuration |
| `/login` / `/logout` | Claude subscription auth |
| `/clear` / `/compact` | Reset or compress conversation |
| `/help` / `/quit` | Help and exit |

</details>

<details>
<summary><strong>Memory system with dream consolidation</strong></summary>

Create a `CLAWPY.md` in your project root — the agent reads it automatically:

```markdown
# Project: MyApp
- Django project with PostgreSQL
- Run tests with `pytest -x`
- Never modify vendor/
```

ClawPy discovers memory files from your current directory up to root, plus global `~/.clawpy/CLAWPY.md`.

**Dream** (`/dream`): LLM reviews your conversation and consolidates learnings into organized, persistent memory. Auto-dream triggers after 10+ turns if 24h have passed.

</details>

<details>
<summary><strong>Background agents & parallel tasks</strong></summary>

The LLM can spawn background agents that don't block:

```
> Analyze the codebase and fix the tests

  [bg a0001] started: "Explore structure"
  [bg a0002] started: "Fix tests"

  While those run...

  [bg a0001] >> Glob (5s)
  [bg a0001] >> Read (8s)
  [bg a0001] completed (15s, 4,200 tokens)
  [bg a0002] >> Bash (20s)
  [bg a0002] completed (23s, 6,100 tokens)
```

Manage with `/tasks`, `/kill <id>`, `/fg <id>`.

</details>

<details>
<summary><strong>Plugin system</strong></summary>

Install plugins from GitHub:

```
> /plugin install owner/repo-name
  Cloning...
  Installed my-plugin v1.0.0
  Commands: my-plugin:build, my-plugin:deploy
```

Plugins can add: commands, agents, skills, hooks, MCP servers. Compatible with Claude Code plugin format.

</details>

<details>
<summary><strong>Smart context management</strong></summary>

Three layers prevent context overflow:

1. **Microcompact** (70%) — clears old tool results automatically
2. **Auto-compact** (90%) — LLM summarizes old messages, keeps last 10
3. **Token budget** — stops if diminishing returns detected

Plus per-turn cost tracking: `1,808in 65out  $0.031`

</details>

## Architecture

```
User → CLI → Engine.run_turn()
               ├── Provider.stream() → SSE → StreamEvents
               ├── Consume stream → assistant Message
               ├── ToolCalls → permission → execute (concurrent if read-only)
               ├── Tool results → append → token budget check
               └── Loop until done or compact needed
```

- **50+ source files**, ~6,500 lines of typed Python
- **3 runtime deps**: httpx, prompt-toolkit, rich (no SDK bloat)
- **`mypy --strict`** passes on all files
- **57 tests** covering types, config, tools, permissions, engine, SSE, OpenAI conversion

## Adding a new provider

It's ~30 lines. Gemini, Ollama, and DeepSeek all inherit from the OpenAI provider:

```python
class MyProvider(OpenAIProvider):
    def __init__(self, cfg):
        cfg.base_url = "https://my-api.com/v1"
        super().__init__(cfg)
        self._provider_name = "my-provider"

register("my-provider", lambda cfg: MyProvider(cfg))
```

## Contributing

```bash
uv pip install -e ".[dev]"
uv run pytest tests/ -v      # 57 tests
uv run mypy --strict src/    # 0 errors
uv run ruff check src/       # Lint
```

## License

MIT
