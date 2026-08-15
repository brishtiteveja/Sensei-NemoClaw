"""Tests for engine with mock provider."""

import asyncio
from typing import Any, AsyncIterator

import pytest

from clawpy.config.config import Config
from clawpy.engine.engine import Engine
from clawpy.provider.base import (
    Delta,
    EventType,
    Request,
    Response,
    StopReason,
    StreamEvent,
    ToolSpec,
    Usage,
)
from clawpy.tool.base import Permission, RunContext, ToolResult
from clawpy.tool.permission import PermissionEnforcer, PermissionMode
from clawpy.tool.registry import ToolRegistry
from clawpy.types import ContentBlock, ContentType, ToolCall


class MockProvider:
    """Provider that returns canned responses."""

    def __init__(self, responses: list[list[StreamEvent]]) -> None:
        self._responses = responses
        self._call_count = 0

    @property
    def name(self) -> str:
        return "mock"

    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]:
        events = self._responses[self._call_count % len(self._responses)]
        self._call_count += 1
        for event in events:
            yield event

    async def send(self, request: Request) -> Response:
        raise NotImplementedError

    def models(self) -> list[str]:
        return ["mock"]


class EchoTool:
    """Tool that echoes its input."""

    @property
    def name(self) -> str:
        return "Echo"

    @property
    def description(self) -> str:
        return "Echo input"

    def input_schema(self) -> dict[str, Any]:
        return {"type": "object", "properties": {"text": {"type": "string"}}}

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.READ_ONLY

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return True

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        return ToolResult(content=f"Echo: {input.get('text', '')}")


def _make_engine(responses: list[list[StreamEvent]]) -> Engine:
    provider = MockProvider(responses)
    tools = ToolRegistry()
    tools.register(EchoTool())
    enforcer = PermissionEnforcer(mode=PermissionMode.BYPASS, work_dir=".")
    config = Config(model="mock", work_dir=".")
    return Engine(provider=provider, tools=tools, enforcer=enforcer, config=config)


@pytest.mark.asyncio
async def test_simple_text_response():
    """Test a turn with just text, no tool calls."""
    events = [
        StreamEvent(type=EventType.DELTA, delta=Delta(text="Hello ")),
        StreamEvent(type=EventType.DELTA, delta=Delta(text="world!")),
        StreamEvent(type=EventType.MESSAGE_STOP, stop_reason=StopReason.END_TURN, usage=Usage(10, 5)),
    ]
    engine = _make_engine([events])
    result = await engine.run_turn("hi")

    assert result.stop_reason == StopReason.END_TURN
    assert result.usage.input_tokens == 10
    assert result.usage.output_tokens == 5
    # Last message should be assistant with "Hello world!"
    last_assistant = [m for m in result.messages if m.role.value == "assistant"][-1]
    assert last_assistant.text_content() == "Hello world!"


@pytest.mark.asyncio
async def test_tool_use_loop():
    """Test a turn that calls a tool then returns text."""
    # First response: tool call
    tool_call_response = [
        StreamEvent(type=EventType.DELTA, delta=Delta(text="Let me echo.")),
        StreamEvent(
            type=EventType.TOOL_START,
            tool_call=ToolCall(id="tc1", name="Echo", input={}),
        ),
        StreamEvent(type=EventType.TOOL_DELTA, delta=Delta(text='{"text": "test"}')),
        StreamEvent(
            type=EventType.TOOL_END,
            tool_call=ToolCall(id="tc1", name="Echo", input={"text": "test"}),
        ),
        StreamEvent(type=EventType.MESSAGE_STOP, stop_reason=StopReason.TOOL_USE, usage=Usage(10, 20)),
    ]
    # Second response: final text
    text_response = [
        StreamEvent(type=EventType.DELTA, delta=Delta(text="The echo said: test")),
        StreamEvent(type=EventType.MESSAGE_STOP, stop_reason=StopReason.END_TURN, usage=Usage(30, 10)),
    ]

    engine = _make_engine([tool_call_response, text_response])
    result = await engine.run_turn("echo test")

    assert result.stop_reason == StopReason.END_TURN
    # Should have: user, assistant(tool call), user(tool result), assistant(text)
    assert len(result.messages) == 4
    # Total usage should be combined
    assert result.usage.input_tokens == 40
    assert result.usage.output_tokens == 30


@pytest.mark.asyncio
async def test_unknown_tool():
    """Test that unknown tool calls return an error result."""
    events = [
        StreamEvent(
            type=EventType.TOOL_START,
            tool_call=ToolCall(id="tc1", name="NonExistent", input={}),
        ),
        StreamEvent(
            type=EventType.TOOL_END,
            tool_call=ToolCall(id="tc1", name="NonExistent", input={}),
        ),
        StreamEvent(type=EventType.MESSAGE_STOP, stop_reason=StopReason.TOOL_USE, usage=Usage(5, 5)),
    ]
    text_response = [
        StreamEvent(type=EventType.DELTA, delta=Delta(text="Sorry.")),
        StreamEvent(type=EventType.MESSAGE_STOP, stop_reason=StopReason.END_TURN, usage=Usage(5, 5)),
    ]

    engine = _make_engine([events, text_response])
    result = await engine.run_turn("use nonexistent")

    # Should have tool result with error
    tool_results = [
        m for m in result.messages
        if m.role.value == "user" and m.tool_results()
    ]
    assert len(tool_results) == 1
    tr = tool_results[0].tool_results()[0]
    assert tr.is_error
    assert "Unknown tool" in tr.content


@pytest.mark.asyncio
async def test_clear_resets():
    engine = _make_engine([[]])
    engine.messages.append(ContentBlock(type=ContentType.TEXT, text="test"))  # type: ignore
    engine.clear()
    assert len(engine.messages) == 0
