"""Core message types for ClawPy.

Neutral internal format — not tied to any provider's API shape.
Every provider converts to/from these types in its own conversion layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ContentType(str, Enum):
    TEXT = "text"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    THINKING = "thinking"
    IMAGE = "image"


@dataclass(frozen=True, slots=True)
class ToolCall:
    """Model requesting a tool invocation."""

    id: str
    name: str
    input: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ToolResult:
    """Output of a tool invocation, sent back to the model."""

    tool_call_id: str
    content: str
    is_error: bool = False


@dataclass(frozen=True, slots=True)
class ImageData:
    media_type: str
    data: bytes


@dataclass(slots=True)
class ContentBlock:
    """A single block within a message. Exactly one payload field is meaningful per type."""

    type: ContentType
    text: str = ""
    tool_call: ToolCall | None = None
    tool_result: ToolResult | None = None
    thinking: str = ""
    image: ImageData | None = None


@dataclass(slots=True)
class Message:
    """A single turn in a conversation."""

    role: Role
    content: list[ContentBlock] = field(default_factory=list)
    id: str = ""

    def text_content(self) -> str:
        """Concatenate all text blocks."""
        return "".join(b.text for b in self.content if b.type == ContentType.TEXT)

    def tool_calls(self) -> list[ToolCall]:
        """Extract all tool call blocks."""
        return [
            b.tool_call
            for b in self.content
            if b.type == ContentType.TOOL_CALL and b.tool_call is not None
        ]

    def tool_results(self) -> list[ToolResult]:
        """Extract all tool result blocks."""
        return [
            b.tool_result
            for b in self.content
            if b.type == ContentType.TOOL_RESULT and b.tool_result is not None
        ]


def text_message(role: Role, text: str) -> Message:
    """Convenience: create a simple text message."""
    return Message(role=role, content=[ContentBlock(type=ContentType.TEXT, text=text)])


def tool_result_message(results: list[ToolResult]) -> Message:
    """Convenience: create a user message carrying tool results."""
    return Message(
        role=Role.USER,
        content=[
            ContentBlock(type=ContentType.TOOL_RESULT, tool_result=r) for r in results
        ],
    )
