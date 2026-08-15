"""Tests for OpenAI provider message/tool conversion."""

import json

from clawpy.config.config import ProviderConfig
from clawpy.provider.base import Request, ToolSpec
from clawpy.provider.openai import OpenAIProvider, _normalize_schema
from clawpy.types import (
    ContentBlock,
    ContentType,
    Message,
    Role,
    ToolCall,
    ToolResult,
)


def _provider() -> OpenAIProvider:
    return OpenAIProvider(ProviderConfig(api_key="test"))


def test_convert_simple_user_message():
    p = _provider()
    req = Request(
        model="gpt-4o",
        system="You help.",
        messages=[Message(role=Role.USER, content=[
            ContentBlock(type=ContentType.TEXT, text="hello"),
        ])],
    )
    converted = p._convert_messages(req)
    assert len(converted) == 2
    assert converted[0] == {"role": "system", "content": "You help."}
    assert converted[1] == {"role": "user", "content": "hello"}


def test_convert_assistant_with_tool_call():
    p = _provider()
    req = Request(
        model="gpt-4o",
        system="",
        messages=[Message(role=Role.ASSISTANT, content=[
            ContentBlock(type=ContentType.TEXT, text="Let me check."),
            ContentBlock(
                type=ContentType.TOOL_CALL,
                tool_call=ToolCall(id="tc1", name="Bash", input={"command": "ls"}),
            ),
        ])],
    )
    converted = p._convert_messages(req)
    # No system prompt (empty), just the assistant message
    assert len(converted) == 1
    msg = converted[0]
    assert msg["role"] == "assistant"
    assert msg["content"] == "Let me check."
    assert len(msg["tool_calls"]) == 1
    tc = msg["tool_calls"][0]
    assert tc["id"] == "tc1"
    assert tc["function"]["name"] == "Bash"
    assert json.loads(tc["function"]["arguments"]) == {"command": "ls"}


def test_convert_tool_result():
    p = _provider()
    req = Request(
        model="gpt-4o",
        system="",
        messages=[Message(role=Role.USER, content=[
            ContentBlock(
                type=ContentType.TOOL_RESULT,
                tool_result=ToolResult(tool_call_id="tc1", content="file.py"),
            ),
        ])],
    )
    converted = p._convert_messages(req)
    assert len(converted) == 1
    assert converted[0]["role"] == "tool"
    assert converted[0]["tool_call_id"] == "tc1"
    assert converted[0]["content"] == "file.py"


def test_convert_tool_result_error():
    p = _provider()
    req = Request(
        model="gpt-4o",
        system="",
        messages=[Message(role=Role.USER, content=[
            ContentBlock(
                type=ContentType.TOOL_RESULT,
                tool_result=ToolResult(tool_call_id="tc1", content="not found", is_error=True),
            ),
        ])],
    )
    converted = p._convert_messages(req)
    assert converted[0]["content"] == "Error: not found"


def test_thinking_blocks_stripped():
    p = _provider()
    req = Request(
        model="gpt-4o",
        system="",
        messages=[Message(role=Role.ASSISTANT, content=[
            ContentBlock(type=ContentType.THINKING, thinking="Let me think..."),
            ContentBlock(type=ContentType.TEXT, text="Here's my answer."),
        ])],
    )
    converted = p._convert_messages(req)
    assert len(converted) == 1
    # Should only have the text, thinking is stripped
    assert converted[0]["content"] == "Here's my answer."
    assert "thinking" not in str(converted[0])


def test_convert_tools():
    p = _provider()
    tools = [ToolSpec(
        name="Bash",
        description="Run a command",
        input_schema={"type": "object", "properties": {"command": {"type": "string"}}},
    )]
    converted = p._convert_tools(tools)
    assert converted is not None
    assert len(converted) == 1
    assert converted[0]["type"] == "function"
    assert converted[0]["function"]["name"] == "Bash"
    # Should have normalized required
    assert "command" in converted[0]["function"]["parameters"]["required"]


def test_normalize_schema():
    schema = {
        "type": "object",
        "properties": {"a": {"type": "string"}, "b": {"type": "integer"}},
        "required": ["a"],
    }
    normalized = _normalize_schema(schema)
    assert set(normalized["required"]) == {"a", "b"}


def test_convert_no_tools():
    p = _provider()
    assert p._convert_tools([]) is None
