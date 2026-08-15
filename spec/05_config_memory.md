# 05 — Configuration, Memory & Session Persistence

## Configuration

### File: `src/clawpy/config/config.py`

### Layered Merge (5 layers, lowest → highest priority)

1. **Defaults** — hardcoded in `Config` dataclass
2. **Global settings** — `~/.clawpy/settings.json`
3. **Project settings** — `<work_dir>/.clawpy/settings.json`
4. **Environment variables** — `CLAWPY_PROVIDER`, `CLAWPY_MODEL`, `ANTHROPIC_API_KEY`, etc.
5. **CLI flags** — `--provider`, `--model`, `--permission-mode`

This mirrors OpenClaude's priority: Managed > Local > Project > Global > Defaults.
We skip Managed (enterprise) for MVP.

### Config Schema

```python
@dataclass(slots=True)
class Config:
    provider: str = "anthropic"
    model: str = "claude-sonnet-4-20250514"
    api_key: str = ""
    base_url: str = ""
    max_tokens: int = 8192
    permission_mode: str = "default"
    work_dir: str = "."
    allow_tools: list[str] = field(default_factory=list)
    deny_tools: list[str] = field(default_factory=list)
```

### Settings File Format

```json
{
  "provider": "anthropic",
  "model": "claude-opus-4-20250514",
  "max_tokens": 16384,
  "permission_mode": "accept_edits",
  "allow_tools": ["Bash"],
  "deny_tools": ["WebFetch"]
}
```

### Provider-Specific Env Vars

| Provider | API Key Env | Base URL Env | Model Env |
|----------|-------------|--------------|-----------|
| anthropic | `ANTHROPIC_API_KEY` | — | `CLAWPY_MODEL` |
| openai | `OPENAI_API_KEY` | `OPENAI_BASE_URL` | `CLAWPY_MODEL` |
| gemini | `GEMINI_API_KEY` | `GEMINI_BASE_URL` | `CLAWPY_MODEL` |
| ollama | — | `OLLAMA_BASE_URL` | `CLAWPY_MODEL` |
| deepseek | `DEEPSEEK_API_KEY` | — | `CLAWPY_MODEL` |

### Paths

```python
def global_config_dir() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", "")) / "clawpy" or Path.home() / ".clawpy"

def project_config_dir(work_dir: str) -> Path:
    return Path(work_dir) / ".clawpy"
```

---

## Memory System (CLAWPY.md)

### File: `src/clawpy/engine/system_prompt.py`

Mirrors OpenClaude's CLAUDE.md memory system.

### Discovery

Walk from CWD to filesystem root, collecting memory files:
1. `<cwd>/CLAWPY.md`
2. `<cwd>/.clawpy/CLAWPY.md`
3. `<parent>/CLAWPY.md` (up to root)
4. `~/.clawpy/CLAWPY.md` (global)

```python
def discover_memory_files(work_dir: str) -> list[Path]:
    """Walk from work_dir to root, collect CLAWPY.md files."""
    found: list[Path] = []
    current = Path(work_dir).resolve()
    while True:
        for name in ["CLAWPY.md", ".clawpy/CLAWPY.md"]:
            path = current / name
            if path.is_file():
                found.append(path)
        parent = current.parent
        if parent == current:
            break
        current = parent
    # Add global
    global_mem = global_config_dir() / "CLAWPY.md"
    if global_mem.is_file():
        found.append(global_mem)
    return found
```

### Injection into System Prompt

Memory content is injected after the static system prompt sections:
```
<system prompt static sections>
<CLAWPY.md content from project>
<CLAWPY.md content from global>
<environment info>
```

---

## Session Persistence

### File: `src/clawpy/session/session.py`

### JSONL Format

Each line is a JSON object with a `type` field:

```jsonl
{"type": "session_meta", "session_id": "abc123", "created_at": 1712345678, "model": "claude-sonnet-4-20250514"}
{"type": "message", "role": "user", "content": [{"type": "text", "text": "Hello"}]}
{"type": "message", "role": "assistant", "content": [{"type": "text", "text": "Hi!"}]}
{"type": "message", "role": "user", "content": [{"type": "tool_result", "tool_call_id": "tc_1", "content": "..."}]}
{"type": "compact", "summary": "User asked about files...", "removed_count": 12}
```

### Storage Location

```
~/.clawpy/sessions/<session_id>.jsonl
```

### Session Operations

```python
class SessionStore:
    def save_message(self, session_id: str, message: Message) -> None: ...
    def save_compact(self, session_id: str, summary: str, removed_count: int) -> None: ...
    def load_session(self, session_id: str) -> list[Message]: ...
    def list_sessions(self) -> list[SessionMeta]: ...
```

### History

Recent sessions listed for `/resume` command:
```
~/.clawpy/history.jsonl   # max 100 entries
```

Each entry: `{"session_id", "title", "started_at", "model", "work_dir"}`
