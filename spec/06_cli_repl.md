# 06 — CLI, REPL & Slash Commands

## CLI Entry Point

### File: `src/clawpy/cli.py`

```
clawpy                           # Interactive REPL (default)
clawpy run "prompt"              # Non-interactive, single prompt
clawpy run < file.txt            # Pipe stdin
clawpy -p openai -m gpt-4o run "hello"
clawpy --permission-mode=bypass run "refactor this"
clawpy --version
```

### Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--provider` | `-p` | LLM provider name |
| `--model` | `-m` | Model ID |
| `--dir` | | Working directory |
| `--permission-mode` | | default / accept_edits / bypass / plan |
| `--version` | | Print version |

## REPL

### File: `src/clawpy/ui/repl.py`

Uses `prompt_toolkit` for input and `rich` for output rendering.

### REPL Loop

```python
class REPL:
    async def run(self) -> None:
        while True:
            user_input = await self.session.prompt_async("❯ ")
            if user_input.startswith("/"):
                self._handle_slash(user_input)
                continue
            await self.engine.run_turn(user_input, on_stream=self._render_stream)
```

### Streaming Output

Uses `rich.live.Live` for real-time streaming display:

```python
def _render_stream(self, event: StreamEvent, live: Live) -> None:
    match event.type:
        case EventType.DELTA:
            # Append text to buffer, update Live display
            self._text_buf += event.delta.text
            live.update(Markdown(self._text_buf))
        case EventType.TOOL_START:
            # Show tool name indicator
            console.print(f"⚡ {event.tool_call.name}")
        case EventType.TOOL_END:
            # Show tool completion
            pass
        case EventType.ERROR:
            console.print(f"[red]Error: {event.error}[/red]")
```

### Permission Prompts

In DEFAULT mode, non-read-only tools trigger interactive approval:

```python
async def _ask_permission(self, tool_name: str, input: dict) -> bool:
    """Prompt user for tool execution approval."""
    self.console.print(f"[yellow]Allow {tool_name}?[/yellow] (y/n/a)")
    response = await self.session.prompt_async("")
    match response.strip().lower():
        case "y" | "yes": return True
        case "a" | "always":
            self.enforcer.allow_rules.append(tool_name)
            return True
        case _: return False
```

## Slash Commands

### Command Types (from OpenClaude spec)

- **Local**: handled entirely in-process, no LLM call
- **Prompt**: expands to text sent to model

### MVP Commands

| Command | Type | Description |
|---------|------|-------------|
| `/quit` | local | Exit REPL |
| `/clear` | local | Reset conversation history |
| `/model` | local | Show current model |
| `/model <name>` | local | Switch model |
| `/compact` | local | Manually trigger conversation compaction |
| `/context` | local | Show token usage breakdown |
| `/help` | local | List available commands |
| `/plan` | local | Enter plan mode (read-only) |
| `/resume` | local | Resume previous session (Phase 4) |

### Command Implementation

```python
SLASH_COMMANDS: dict[str, Callable] = {
    "/quit": cmd_quit,
    "/clear": cmd_clear,
    "/model": cmd_model,
    "/compact": cmd_compact,
    "/context": cmd_context,
    "/help": cmd_help,
    "/plan": cmd_plan,
}

def _handle_slash(self, raw: str) -> None:
    parts = raw.split(maxsplit=1)
    cmd_name = parts[0]
    args = parts[1] if len(parts) > 1 else ""
    handler = SLASH_COMMANDS.get(cmd_name)
    if handler:
        handler(self, args)
    else:
        self.console.print(f"Unknown command: {cmd_name}")
```

## Output Rendering

### File: `src/clawpy/ui/render.py`

Uses `rich` for:
- **Markdown rendering** — `rich.markdown.Markdown`
- **Code syntax highlighting** — `rich.syntax.Syntax`
- **Diff rendering** — colored +/- lines
- **Tool output** — panels with headers
- **Spinners** — `rich.spinner.Spinner` during tool execution

```python
def render_tool_use(console: Console, name: str, input: dict) -> None:
    """Render a tool invocation indicator."""
    console.print(Panel(
        Pretty(input),
        title=f"⚡ {name}",
        border_style="blue",
    ))

def render_tool_result(console: Console, name: str, result: ToolResult) -> None:
    """Render tool output."""
    style = "red" if result.is_error else "green"
    console.print(Panel(
        result.content[:2000],  # Truncate for display
        title=f"← {name}",
        border_style=style,
    ))
```
