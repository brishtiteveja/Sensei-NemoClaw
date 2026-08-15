"""Tool interface and core types.

Every tool implements the Tool Protocol. Permission levels control
what tools can do, from read-only to dangerous operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Awaitable, Callable, Protocol, runtime_checkable


class Permission(IntEnum):
    """Permission levels, from least to most dangerous."""

    READ_ONLY = 0
    WORKSPACE_WRITE = 1
    SHELL_SAFE = 2
    SHELL_UNSAFE = 3
    DANGEROUS = 4


@dataclass(frozen=True, slots=True)
class ToolResult:
    """Result returned by a tool execution."""

    content: str
    is_error: bool = False


@dataclass(frozen=True, slots=True)
class RunContext:
    """Context passed to tool execution."""

    work_dir: str
    ask_user: Callable[[str], Awaitable[str]]
    task_registry: Any = None  # Optional TaskRegistry — avoids circular import
    on_agent_event: Callable[[str, str], None] | None = None  # (task_id, message) notifications


@runtime_checkable
class Tool(Protocol):
    """Interface every tool must implement."""

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    def input_schema(self) -> dict[str, Any]: ...

    def permission_for(self, input: dict[str, Any]) -> Permission: ...

    def is_read_only(self, input: dict[str, Any]) -> bool: ...

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult: ...
