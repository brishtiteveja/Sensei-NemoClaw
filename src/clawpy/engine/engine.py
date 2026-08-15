"""Engine — manages conversation lifecycle and the agentic loop.

Mirrors OpenClaude's QueryEngine + query.ts: handles the stream → tools → loop cycle.
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable

from clawpy.config.config import Config
from clawpy.engine.compact import auto_compact
from clawpy.engine.file_state import FileStateTracker
from clawpy.engine.microcompact import microcompact, should_microcompact
from clawpy.engine.token_budget import TokenBudget, get_context_window
from clawpy.provider.base import (
    Delta,
    EventType,
    Provider,
    Request,
    StopReason,
    StreamEvent,
    Usage,
)
from clawpy.tool.base import Permission, RunContext, ToolResult as ToolExecResult
from clawpy.tool.permission import PermissionEnforcer
from clawpy.tool.registry import ToolRegistry
from clawpy.types import (
    ContentBlock,
    ContentType,
    Message,
    Role,
    ToolCall,
    ToolResult,
    text_message,
    tool_result_message,
)

logger = logging.getLogger(__name__)

MAX_ITERATIONS = 50


@dataclass(slots=True)
class TurnResult:
    """Result of a single agentic turn (may involve multiple LLM calls)."""

    messages: list[Message]
    stop_reason: StopReason
    usage: Usage
    error: str | None = None


class Engine:
    """Conversation engine with agentic tool-use loop."""

    def __init__(
        self,
        provider: Provider,
        tools: ToolRegistry,
        enforcer: PermissionEnforcer,
        config: Config,
    ) -> None:
        self.provider = provider
        self.tools = tools
        self.enforcer = enforcer
        self.config = config
        self.messages: list[Message] = []
        self.system_prompt: str = ""
        self.file_state = FileStateTracker()
        self._compact_failures = 0
        # Task registry for tracking sub-agents
        from clawpy.engine.tasks import TaskRegistry
        self.task_registry = TaskRegistry()
        self.on_agent_event: Callable[[str, str], None] | None = None
        self._ask_user: Callable[[str], Any] | None = None  # Set by REPL for interactive prompts
        # Session persistence
        from clawpy.session.session import SessionStore
        self.session_store: SessionStore | None = None

    def set_system_prompt(self, prompt: str) -> None:
        self.system_prompt = prompt

    def clear(self) -> None:
        """Reset conversation history and file state."""
        self.messages = []
        self.file_state.clear()
        self._compact_failures = 0

    def _persist(self, msg: Message) -> None:
        """Save a message to session store if available."""
        if self.session_store:
            self.session_store.save_message(msg)

    def reload_system_prompt(self) -> None:
        """Rebuild system prompt (e.g., after memory files change)."""
        from clawpy.engine.system_prompt import build_system_prompt
        self.system_prompt = build_system_prompt(self.config.work_dir, self.config.model)

    async def run_turn(
        self,
        user_input: str,
        on_stream: Callable[[StreamEvent], None] | None = None,
    ) -> TurnResult:
        """Execute one full agentic turn.

        The loop (mirrors query.ts):
        1. Append user message
        2. Build Request → stream response from provider
        3. Consume stream → assemble assistant Message
        4. Extract tool calls
        5. If no tool calls or end_turn → return
        6. Permission-check → execute tools (read-only concurrent, writes serial)
        7. Append tool results → goto 2
        """
        user_msg = text_message(Role.USER, user_input)
        self.messages.append(user_msg)
        self._persist(user_msg)
        total_usage = Usage()
        budget = TokenBudget(context_window=get_context_window(self.config.model))

        for iteration in range(MAX_ITERATIONS):
            # Microcompact: clear old tool results at 70% context
            est_tokens = budget.total_input_tokens + budget.total_output_tokens
            if should_microcompact(est_tokens, budget.context_window):
                cleared = microcompact(self.messages)
                if cleared > 0:
                    logger.info("Microcompact: cleared %d old tool results", cleared)

            # Auto-compact if approaching context limit
            if not budget.should_continue() and self._compact_failures < 3:
                compacted = await auto_compact(
                    self.messages, self.provider, self.config.model
                )
                if compacted is not None:
                    self.messages = compacted
                    self._compact_failures = 0
                    logger.info("Auto-compacted conversation")
                else:
                    self._compact_failures += 1

            request = Request(
                model=self.config.model,
                system=self.system_prompt,
                messages=self.messages,
                tools=self.tools.specs(),
                max_tokens=self.config.max_tokens,
            )

            # Stream and assemble assistant message
            assistant_msg, stop_reason, usage = await self._consume_stream(
                request, on_stream
            )
            total_usage = total_usage + usage
            budget.record_turn(usage.input_tokens, usage.output_tokens)
            self.messages.append(assistant_msg)
            self._persist(assistant_msg)

            # Check for tool calls
            tool_calls = assistant_msg.tool_calls()
            if not tool_calls or stop_reason == StopReason.END_TURN:
                return TurnResult(
                    messages=self.messages,
                    stop_reason=stop_reason,
                    usage=total_usage,
                )

            # Token budget check after tool use decision
            if not budget.should_continue(has_tool_calls=bool(tool_calls)):
                logger.info("Token budget exhausted, ending turn")
                return TurnResult(
                    messages=self.messages,
                    stop_reason=StopReason.MAX_TOKENS,
                    usage=total_usage,
                    error="Token budget exhausted",
                )

            # Execute tools with permission checks
            results = await self._execute_tools(tool_calls)

            # Append tool results as user message
            result_msg = tool_result_message(results)
            self.messages.append(result_msg)
            self._persist(result_msg)

            logger.debug(
                "Iteration %d: %d tool calls, %d tokens remaining",
                iteration,
                len(tool_calls),
                budget.tokens_remaining(),
            )

        return TurnResult(
            messages=self.messages,
            stop_reason=StopReason.END_TURN,
            usage=total_usage,
            error=f"Exceeded max iterations ({MAX_ITERATIONS})",
        )

    async def _consume_stream(
        self,
        request: Request,
        on_stream: Callable[[StreamEvent], None] | None,
    ) -> tuple[Message, StopReason, Usage]:
        """Read all stream events and assemble the assistant Message.

        State machine mirrors openaiStreamToAnthropic():
        - Track text buffer, active tool calls, accumulated JSON per tool
        """
        text_buf = ""
        thinking_buf = ""
        completed_tool_calls: list[ToolCall] = []
        active_tools: dict[str, ToolCall] = {}  # id -> partial ToolCall
        tool_json_bufs: dict[str, str] = {}  # id -> accumulated JSON
        stop_reason = StopReason.END_TURN
        total_usage = Usage()
        current_tool_id: str | None = None

        async for event in self.provider.stream(request):
            if on_stream is not None:
                on_stream(event)

            match event.type:
                case EventType.DELTA:
                    if event.delta:
                        text_buf += event.delta.text
                        thinking_buf += event.delta.thinking
                    if event.usage:
                        total_usage = total_usage + event.usage

                case EventType.TOOL_START:
                    if event.tool_call:
                        current_tool_id = event.tool_call.id
                        active_tools[current_tool_id] = event.tool_call
                        tool_json_bufs[current_tool_id] = ""

                case EventType.TOOL_DELTA:
                    if event.delta and current_tool_id:
                        tool_json_bufs[current_tool_id] = (
                            tool_json_bufs.get(current_tool_id, "") + event.delta.text
                        )

                case EventType.TOOL_END:
                    if event.tool_call:
                        # Finalized tool call with parsed input
                        completed_tool_calls.append(event.tool_call)
                        active_tools.pop(event.tool_call.id, None)
                        tool_json_bufs.pop(event.tool_call.id, None)
                        current_tool_id = None
                    elif current_tool_id and current_tool_id in active_tools:
                        # Finalize from accumulated JSON
                        tc = active_tools.pop(current_tool_id)
                        raw = tool_json_bufs.pop(current_tool_id, "")
                        parsed: dict[str, Any] = {}
                        if raw:
                            try:
                                parsed = json.loads(raw)
                            except json.JSONDecodeError:
                                parsed = {"_raw": raw}
                        completed_tool_calls.append(
                            ToolCall(id=tc.id, name=tc.name, input=parsed)
                        )
                        current_tool_id = None

                case EventType.MESSAGE_STOP:
                    if event.stop_reason:
                        stop_reason = event.stop_reason
                    if event.usage:
                        total_usage = total_usage + event.usage

                case EventType.ERROR:
                    logger.error("Stream error: %s", event.error)
                    if event.error:
                        text_buf += f"\n[Stream error: {event.error}]"

        # Build assistant message
        blocks: list[ContentBlock] = []
        if thinking_buf:
            blocks.append(ContentBlock(type=ContentType.THINKING, thinking=thinking_buf))
        if text_buf:
            blocks.append(ContentBlock(type=ContentType.TEXT, text=text_buf))
        for tc in completed_tool_calls:
            blocks.append(ContentBlock(type=ContentType.TOOL_CALL, tool_call=tc))

        assistant_msg = Message(role=Role.ASSISTANT, content=blocks)
        return assistant_msg, stop_reason, total_usage

    async def _execute_tools(self, calls: list[ToolCall]) -> list[ToolResult]:
        """Execute tool calls with permission checks and concurrency batching.

        Mirrors toolOrchestration.ts partitionToolCalls():
        - Partition into batches: consecutive read-only → concurrent, else serial
        - Concurrent batches run via asyncio.gather()
        """
        results: list[ToolResult] = []

        # Partition into batches
        batches = self._partition_tool_calls(calls)

        for batch in batches:
            if len(batch) == 1:
                result = await self._run_single_tool(batch[0])
                results.append(result)
            else:
                # All tools in a concurrent batch are read-only
                coros = [self._run_single_tool(tc) for tc in batch]
                batch_results = await asyncio.gather(*coros)
                results.extend(batch_results)

        return results

    def _partition_tool_calls(
        self, calls: list[ToolCall]
    ) -> list[list[ToolCall]]:
        """Partition tool calls into concurrent (read-only) and serial batches."""
        batches: list[list[ToolCall]] = []
        current_batch: list[ToolCall] = []
        current_is_readonly = True

        for call in calls:
            tool = self.tools.get(call.name)
            is_readonly = tool.is_read_only(call.input) if tool else False

            if not current_batch:
                current_batch = [call]
                current_is_readonly = is_readonly
            elif is_readonly and current_is_readonly:
                # Extend current concurrent batch
                current_batch.append(call)
            else:
                # Flush current batch, start new one
                batches.append(current_batch)
                current_batch = [call]
                current_is_readonly = is_readonly

        if current_batch:
            batches.append(current_batch)

        return batches

    async def _run_single_tool(self, call: ToolCall) -> ToolResult:
        """Run a single tool with permission checking."""
        tool = self.tools.get(call.name)
        if tool is None:
            return ToolResult(
                tool_call_id=call.id,
                content=f"Unknown tool: {call.name}",
                is_error=True,
            )

        # Permission check
        denial = self.enforcer.check(tool, call.input)
        if denial is not None:
            if denial.startswith("ASK:"):
                # Interactive permission prompt
                ask = self._ask_user or _stub_ask_user
                try:
                    # Build a readable description of what's being asked
                    input_preview = str(call.input)
                    if len(input_preview) > 200:
                        input_preview = input_preview[:200] + "..."
                    question = f"Allow {call.name}? {input_preview}\n(y)es / (n)o / (a)lways: "
                    answer = await ask(question)
                    answer = answer.strip().lower()
                    if answer in ("a", "always"):
                        self.enforcer.allow_rules.append(call.name)
                    elif answer not in ("y", "yes", ""):
                        return ToolResult(
                            tool_call_id=call.id,
                            content=f"Permission denied by user for {call.name}",
                            is_error=True,
                        )
                except Exception:
                    pass  # Fallthrough to allow on error
            else:
                return ToolResult(
                    tool_call_id=call.id,
                    content=f"Permission denied: {denial}",
                    is_error=True,
                )

        # Execute
        ctx = RunContext(
            work_dir=self.config.work_dir,
            ask_user=self._ask_user or _stub_ask_user,
            task_registry=self.task_registry,
            on_agent_event=self.on_agent_event,
        )
        try:
            exec_result = await tool.run(call.input, ctx)
        except Exception as e:
            logger.exception("Tool %s failed", call.name)
            return ToolResult(
                tool_call_id=call.id,
                content=f"Tool error: {e}",
                is_error=True,
            )

        return ToolResult(
            tool_call_id=call.id,
            content=exec_result.content,
            is_error=exec_result.is_error,
        )


async def _stub_ask_user(question: str) -> str:
    """Stub ask_user — will be replaced by REPL's interactive prompt."""
    return "y"
