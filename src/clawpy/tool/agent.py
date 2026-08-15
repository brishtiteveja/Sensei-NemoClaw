"""Agent tool — spawns sub-engines as tracked tasks.

Supports:
- Foreground agents: stream output to parent, block until done
- Background agents: run as asyncio.Task, return immediately
- Task tracking via TaskRegistry for /tasks, /kill, /fg
"""

from __future__ import annotations

import asyncio
from typing import Any

from clawpy.provider.base import EventType, StreamEvent
from clawpy.tool.base import Permission, RunContext, ToolResult


class AgentTool:
    """Spawn a sub-agent to handle a complex task."""

    def __init__(self) -> None:
        self._provider: Any = None
        self._enforcer: Any = None
        self._config: Any = None
        self._parent_tools: Any = None

    @property
    def name(self) -> str:
        return "Agent"

    @property
    def description(self) -> str:
        return (
            "Launch a sub-agent to handle a complex task autonomously. "
            "The agent gets its own conversation context and tool access. "
            "Set run_in_background=true to run without blocking."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The task for the agent to perform",
                },
                "description": {
                    "type": "string",
                    "description": "Short description of the task (3-5 words)",
                },
                "model": {
                    "type": "string",
                    "description": "Optional model override for the sub-agent",
                },
                "run_in_background": {
                    "type": "boolean",
                    "description": "Run in background without blocking (default false)",
                },
            },
            "required": ["prompt"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.SHELL_UNSAFE

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return False

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        prompt = input.get("prompt", "")
        if not prompt:
            return ToolResult(content="Error: prompt is required", is_error=True)

        if not self._provider or not self._config:
            return ToolResult(content="Error: Agent tool not initialized", is_error=True)

        description = input.get("description", prompt[:50])
        background = input.get("run_in_background", False)

        # Create sub-engine
        sub_engine = self._create_sub_engine(ctx, input.get("model"))
        if sub_engine is None:
            return ToolResult(content="Error: Failed to create sub-engine", is_error=True)

        # Register task
        registry = ctx.task_registry
        notify = ctx.on_agent_event

        if registry:
            from clawpy.engine.tasks import TaskStatus
            task = registry.create(description, background=background)
            task.status = TaskStatus.RUNNING

            if background:
                # Background: spawn asyncio.Task, return immediately
                async_task = asyncio.create_task(
                    self._run_agent_task(sub_engine, prompt, task, registry, notify)
                )
                task._asyncio_task = async_task

                if notify:
                    notify(task.task_id, f"started in background: {description!r}")

                return ToolResult(
                    content=f"Agent [{task.task_id}] launched in background: {description}\n"
                    f"Use /tasks to check progress, /tasks {task.task_id} to view output."
                )
            else:
                # Foreground: run and stream events
                result = await self._run_agent_task(
                    sub_engine, prompt, task, registry, notify
                )
                return result
        else:
            # No registry — simple inline execution (fallback)
            return await self._run_inline(sub_engine, prompt)

    def _create_sub_engine(self, ctx: RunContext, model_override: str | None = None) -> Any:
        """Create an isolated sub-Engine."""
        from clawpy.config.config import Config
        from clawpy.engine.engine import Engine
        from clawpy.engine.system_prompt import build_system_prompt
        from clawpy.tool.permission import PermissionEnforcer
        from clawpy.tool.registry import ToolRegistry

        # Build sub-tool registry excluding Agent (prevent recursion)
        sub_tools = ToolRegistry()
        if self._parent_tools:
            for tool in self._parent_tools.all():
                if tool.name != "Agent":
                    sub_tools.register(tool)

        sub_config = Config(
            provider=self._config.provider,
            model=model_override or self._config.model,
            api_key=self._config.api_key,
            base_url=self._config.base_url,
            max_tokens=self._config.max_tokens,
            permission_mode=self._config.permission_mode,
            work_dir=ctx.work_dir,
        )

        sub_engine = Engine(
            provider=self._provider,
            tools=sub_tools,
            enforcer=self._enforcer,
            config=sub_config,
        )
        sub_engine.set_system_prompt(build_system_prompt(ctx.work_dir, sub_config.model))
        return sub_engine

    async def _run_agent_task(
        self,
        engine: Any,
        prompt: str,
        task: Any,
        registry: Any,
        notify: Any,
    ) -> ToolResult:
        """Run an agent and update task state."""
        from clawpy.engine.tasks import TaskStatus

        # Background heartbeat — shows elapsed time every 15s
        heartbeat_task: asyncio.Task[None] | None = None
        if task.is_background and notify:
            async def _heartbeat() -> None:
                while True:
                    await asyncio.sleep(15)
                    if task.is_done:
                        break
                    notify(
                        task.task_id,
                        f"running ({task.elapsed:.0f}s, {task.tool_calls} tools)...",
                    )

            heartbeat_task = asyncio.create_task(_heartbeat())

        try:
            tool_count = 0
            text_buf = ""

            def on_stream(event: StreamEvent) -> None:
                nonlocal tool_count, text_buf
                if event.type == EventType.TOOL_START and event.tool_call:
                    tool_count += 1
                    task.tool_calls = tool_count
                    log_entry = f">> {event.tool_call.name} ({task.elapsed:.0f}s)"
                    task.log.append(log_entry)
                    if notify and task.is_background:
                        notify(task.task_id, log_entry)
                elif event.type == EventType.DELTA and event.delta and event.delta.text:
                    text_buf += event.delta.text
                elif event.type == EventType.MESSAGE_STOP:
                    if text_buf:
                        # Log a preview of streamed text
                        preview = text_buf[:100].replace("\n", " ")
                        if len(text_buf) > 100:
                            preview += "..."
                        task.log.append(f"   {preview}")
                        text_buf = ""

            result = await engine.run_turn(prompt, on_stream=on_stream)

            # Extract final text
            answer = ""
            for msg in reversed(result.messages):
                if msg.role.value == "assistant":
                    text = msg.text_content()
                    if text:
                        answer = text
                        break

            task.output = answer
            task.input_tokens = result.usage.input_tokens
            task.output_tokens = result.usage.output_tokens
            task.messages = result.messages
            registry.complete(task.task_id, output=answer)

            if notify and task.is_background:
                tokens = result.usage.input_tokens + result.usage.output_tokens
                notify(
                    task.task_id,
                    f"completed ({task.elapsed:.0f}s, {tokens:,} tokens, {tool_count} tools)",
                )

            return ToolResult(content=answer or "Agent completed with no text output.")

        except asyncio.CancelledError:
            registry.kill(task.task_id)
            if notify:
                notify(task.task_id, f"killed ({task.elapsed:.0f}s)")
            return ToolResult(content="Agent was killed.", is_error=True)

        except Exception as e:
            registry.fail(task.task_id, str(e))
            if notify:
                notify(task.task_id, f"failed ({task.elapsed:.0f}s): {e}")
            return ToolResult(content=f"Agent error: {e}", is_error=True)

        finally:
            if heartbeat_task and not heartbeat_task.done():
                heartbeat_task.cancel()

    async def _run_inline(self, engine: Any, prompt: str) -> ToolResult:
        """Fallback: run without task registry."""
        try:
            result = await engine.run_turn(prompt)
            for msg in reversed(result.messages):
                if msg.role.value == "assistant":
                    text = msg.text_content()
                    if text:
                        return ToolResult(content=text)
            return ToolResult(content="Agent completed with no text output.")
        except Exception as e:
            return ToolResult(content=f"Agent error: {e}", is_error=True)
