# 07 — Hooks, Sub-Agents & Future Extensibility

## Hooks System

### File: `src/clawpy/engine/hooks.py` (Phase 4)

Hooks allow user-defined shell commands to run before/after tool execution.
From OpenClaude's spec: PreToolUse, PostToolUse, UserPromptSubmit, Stop.

### Hook Configuration

In `~/.clawpy/settings.json` or `.clawpy/settings.json`:

```json
{
  "hooks": {
    "pre_tool_use": [
      {
        "tool": "Bash",
        "if": "command:git*",
        "command": "echo 'Git operation detected'"
      }
    ],
    "post_tool_use": [
      {
        "tool": "Edit",
        "command": "ruff check --fix $CLAWPY_FILE_PATH"
      }
    ]
  }
}
```

### Hook Events

| Event | When | Env Vars |
|-------|------|----------|
| `pre_tool_use` | Before tool execution | `CLAWPY_TOOL_NAME`, `CLAWPY_TOOL_INPUT` |
| `post_tool_use` | After tool execution | `CLAWPY_TOOL_NAME`, `CLAWPY_TOOL_INPUT`, `CLAWPY_TOOL_OUTPUT` |
| `user_prompt_submit` | Before user prompt is sent | `CLAWPY_USER_PROMPT` |
| `stop` | When assistant turn ends | `CLAWPY_STOP_REASON` |

### Hook Execution

```python
async def run_pre_tool_hooks(
    hooks: list[HookConfig],
    tool_name: str,
    tool_input: dict[str, Any],
) -> HookResult:
    """Run matching pre-tool hooks. Can modify input or deny execution."""
    for hook in hooks:
        if hook.tool and hook.tool != tool_name:
            continue
        if hook.if_condition and not _matches_condition(hook.if_condition, tool_input):
            continue
        result = await _run_hook_command(hook.command, {
            "CLAWPY_TOOL_NAME": tool_name,
            "CLAWPY_TOOL_INPUT": json.dumps(tool_input),
        })
        if result.exit_code != 0:
            return HookResult(blocked=True, message=result.stderr)
    return HookResult(blocked=False)
```

### Hook Result Effects

- Exit code 0 → continue
- Exit code non-0 → block tool execution, return hook stderr as error
- Stdout → can modify tool input (JSON parse attempt)

---

## Sub-Agent System

### File: `src/clawpy/tool/agent.py` (Phase 4)

The Agent tool spawns a sub-engine with its own conversation context.

### Design (from claurst spec)

```python
class AgentTool:
    @property
    def name(self) -> str: return "Agent"

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        prompt = input["prompt"]
        description = input.get("description", "")
        model = input.get("model")

        # Create sub-engine with filtered tools
        sub_tools = ToolRegistry()
        for tool in self._parent_tools.all():
            if tool.name != "Agent":  # Prevent recursion
                sub_tools.register(tool)

        sub_engine = Engine(
            provider=self._provider,
            tools=sub_tools,
            enforcer=self._enforcer,
            config=self._config,
        )

        result = await sub_engine.run_turn(prompt)
        return ToolResult(content=result.messages[-1].text_content())
```

Key constraints:
- Agent tool excluded from sub-engine's tool list (no recursive agents)
- Sub-engine gets its own message history (isolated context)
- Sub-engine shares the same provider and permission enforcer

---

## MCP Integration (Future)

### Not in MVP, but planned architecture:

MCP (Model Context Protocol) allows external tools to be registered dynamically.

```python
class MCPClient:
    """JSON-RPC 2.0 over stdio to an MCP server."""
    transport: str  # "stdio" | "sse"
    tools: list[ToolSpec]  # Discovered via tools/list

    async def connect(self, command: list[str]) -> None: ...
    async def call_tool(self, name: str, input: dict) -> str: ...
    async def list_tools(self) -> list[ToolSpec]: ...
```

MCP tools would be merged into the ToolRegistry alongside built-in tools,
with built-in tools taking priority on name conflicts (matching OpenClaude's
`assembleToolPool()` dedup logic).

---

## Future Extensibility Hooks

Areas identified from the claurst spec that ClawPy should plan for:

1. **Plugin system** — load tools/commands/agents from external packages
2. **Custom agents** — Markdown+YAML agent definitions in `.clawpy/agents/`
3. **Skills** — prompt templates with YAML frontmatter in `.clawpy/skills/`
4. **Output styles** — custom formatting instructions
5. **IDE integration** — MCP bridge for VS Code / JetBrains

These are all post-MVP but the architecture (Protocol-based tools, registry pattern,
layered config) is designed to accommodate them.
