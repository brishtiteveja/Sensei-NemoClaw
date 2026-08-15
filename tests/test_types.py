"""Tests for core types."""

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


def test_text_message():
    msg = text_message(Role.USER, "hello")
    assert msg.role == Role.USER
    assert msg.text_content() == "hello"
    assert len(msg.content) == 1
    assert msg.content[0].type == ContentType.TEXT


def test_message_text_content_concatenates():
    msg = Message(role=Role.ASSISTANT, content=[
        ContentBlock(type=ContentType.TEXT, text="Hello "),
        ContentBlock(type=ContentType.TEXT, text="world"),
    ])
    assert msg.text_content() == "Hello world"


def test_message_tool_calls():
    tc = ToolCall(id="tc1", name="Bash", input={"command": "ls"})
    msg = Message(role=Role.ASSISTANT, content=[
        ContentBlock(type=ContentType.TEXT, text="Let me check."),
        ContentBlock(type=ContentType.TOOL_CALL, tool_call=tc),
    ])
    calls = msg.tool_calls()
    assert len(calls) == 1
    assert calls[0].name == "Bash"
    assert calls[0].input == {"command": "ls"}


def test_message_tool_results():
    tr = ToolResult(tool_call_id="tc1", content="file.py", is_error=False)
    msg = tool_result_message([tr])
    assert msg.role == Role.USER
    results = msg.tool_results()
    assert len(results) == 1
    assert results[0].content == "file.py"
    assert not results[0].is_error


def test_tool_call_frozen():
    tc = ToolCall(id="x", name="Read", input={})
    try:
        tc.name = "Write"  # type: ignore
        assert False, "Should be frozen"
    except AttributeError:
        pass


def test_empty_message():
    msg = Message(role=Role.SYSTEM)
    assert msg.text_content() == ""
    assert msg.tool_calls() == []
    assert msg.tool_results() == []
