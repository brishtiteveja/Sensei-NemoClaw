# 03 — Tool System

## File: `src/clawpy/tool/`

## Tool Protocol

```python
@runtime_checkable
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

Compared to OpenClaude's 42+ method Tool type, we keep only the essential 6 methods.
Additional capabilities (deferred loading, UI rendering, auto-classifier) are out of MVP scope.

## Permission Levels

```python
class Permission(IntEnum):
    READ_ONLY = 0         # grep, glob, read, list
    WORKSPACE_WRITE = 1   # edit, write (within project)
    SHELL_SAFE = 2        # ls, git status, etc.
    SHELL_UNSAFE = 3      # arbitrary shell, network
    DANGEROUS = 4         # rm -rf, git push --force
```

Mirrors claw-code's `PermissionMode::ReadOnly | WorkspaceWrite | DangerFullAccess` but
with finer granularity for shell commands.

## Permission Enforcer

```python
class PermissionMode(str, Enum):
    DEFAULT = "default"           # Ask for non-read-only
    ACCEPT_EDITS = "accept_edits" # Auto-approve workspace writes
    BYPASS = "bypass"             # Auto-approve everything (yolo)
    PLAN = "plan"                 # Deny all non-read-only

class PermissionEnforcer:
    def check(self, tool: Tool, input: dict[str, Any]) -> str | None:
        # Returns None if allowed, error string if denied
        # "ASK:" prefix means interactive approval needed
```

Rule evaluation order:
1. Read-only → always allowed
2. Deny rules → always denied
3. Allow rules → always allowed
4. Mode-based decision

## Tool Registry

```python
class ToolRegistry:
    def register(self, tool: Tool) -> None: ...
    def get(self, name: str) -> Tool | None: ...
    def all(self) -> list[Tool]: ...
    def specs(self) -> list[ToolSpec]: ...  # For API requests
```

## Tool Execution Orchestration

From `engine/engine.py`, mirrors `toolOrchestration.ts`:

1. **Partition** tool calls into batches:
   - Consecutive read-only tools → one concurrent batch
   - Non-read-only tool → one serial batch (single tool)
2. **Concurrent batches**: `asyncio.gather(*[tool.run(input, ctx) for ...])`
3. **Serial batches**: `await tool.run(input, ctx)` one at a time

Max concurrency: 10 (matching OpenClaude's `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`).

## MVP Tools (10)

### Bash (`tool/bash.py`) — DONE
- Input: `{command, timeout?, description?}`
- Permission: dynamic — read-only commands → SHELL_SAFE, others → SHELL_UNSAFE
- Read-only detection: safe command allowlist + dangerous pattern blocklist
- Timeout: default 120s, max 600s
- Output truncation: 100K chars

### Read (`tool/file_read.py`) — DONE
- Input: `{file_path, offset?, limit?}`
- Permission: READ_ONLY (always)
- Output: cat -n format (line numbers + tab + content)
- Registers file in `read_file_state` for edit/write enforcement
- Default limit: 2000 lines
- Handles: text, images (future), PDFs (future)

### Write (`tool/file_write.py`) — Phase 2
- Input: `{file_path, content}`
- Permission: WORKSPACE_WRITE
- **Read-before-write**: file must exist in `read_file_state` (or be new)
- **Staleness check**: reject if file mtime changed since last read
- Updates `read_file_state` after write

### Edit (`tool/file_edit.py`) — Phase 2
- Input: `{file_path, old_string, new_string, replace_all?}`
- Permission: WORKSPACE_WRITE
- **Read-before-write**: file must exist in `read_file_state`
- **Uniqueness check**: `old_string` must match exactly once (unless `replace_all`)
- **Staleness check**: reject if mtime changed
- Updates `read_file_state` after edit

### Grep (`tool/grep_tool.py`) — DONE
- Input: `{pattern, path?, glob?, output_mode?, -i?, -A?, -B?, -C?, head_limit?, multiline?}`
- Permission: READ_ONLY
- Output modes: content, files_with_matches (default), count
- Default head_limit: 250
- Backend: ripgrep

### Glob (`tool/glob_tool.py`) — DONE
- Input: `{pattern, path?}`
- Permission: READ_ONLY
- Sorted by mtime (newest first)
- Max 1000 results

### ListFiles (`tool/list_files.py`) — Phase 2
- Input: `{path?}`
- Permission: READ_ONLY
- Output: directory listing with file types

### WebFetch (`tool/web_fetch.py`) — Phase 2
- Input: `{url, headers?}`
- Permission: SHELL_UNSAFE
- Timeout: 30s
- HTML → text conversion, 100K char truncation

### AskUser (`tool/ask_user.py`) — Phase 2
- Input: `{question}`
- Permission: READ_ONLY
- Prompts user interactively, returns their answer

### Agent (`tool/agent.py`) — Phase 4
- Input: `{prompt, description?, model?}`
- Permission: SHELL_UNSAFE
- Spawns sub-engine with filtered tool list (excludes Agent to prevent recursion)
- Runs separate query loop
- Mirrors claurst's Task tool implementation
