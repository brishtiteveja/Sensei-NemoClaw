"""Provider abstraction — the interface every LLM provider implements.

Streaming uses AsyncIterator[StreamEvent] which maps naturally to
Python's `async for` and is composable with asyncio.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from collections.abc import AsyncIterator
from typing import Any, Protocol, runtime_checkable

from clawpy.types import ContentBlock, ToolCall


class StopReason(str, Enum):
    END_TURN = "end_turn"
    TOOL_USE = "tool_use"
    MAX_TOKENS = "max_tokens"
    STOP_SEQUENCE = "stop_sequence"


class EventType(Enum):
    DELTA = auto()
    TOOL_START = auto()
    TOOL_DELTA = auto()
    TOOL_END = auto()
    MESSAGE_STOP = auto()
    ERROR = auto()


@dataclass(frozen=True, slots=True)
class Delta:
    text: str = ""
    thinking: str = ""


@dataclass(frozen=True, slots=True)
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0

    def __add__(self, other: Usage) -> Usage:
        return Usage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
        )


@dataclass(slots=True)
class StreamEvent:
    type: EventType
    delta: Delta | None = None
    tool_call: ToolCall | None = None
    stop_reason: StopReason | None = None
    usage: Usage | None = None
    error: Exception | None = None


@dataclass(frozen=True, slots=True)
class ToolSpec:
    """Tool description sent to the provider API."""

    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass(slots=True)
class Request:
    """Provider-neutral request."""

    model: str
    system: str
    messages: list[Any]  # list[Message] — Any to avoid circular import
    tools: list[ToolSpec] = field(default_factory=list)
    max_tokens: int = 8192
    temperature: float | None = None
    stop_sequences: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Response:
    """Complete non-streaming response."""

    id: str
    content: list[ContentBlock]
    stop_reason: StopReason
    usage: Usage


@runtime_checkable
class Provider(Protocol):
    """Interface every LLM provider must implement."""

    @property
    def name(self) -> str: ...

    def stream(self, request: Request) -> AsyncIterator[StreamEvent]: ...

    async def send(self, request: Request) -> Response: ...

    def models(self) -> list[str]: ...
