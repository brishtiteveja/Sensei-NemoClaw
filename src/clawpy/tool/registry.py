"""Tool registry — holds all registered tools, provides lookup and spec generation."""

from __future__ import annotations

from clawpy.provider.base import ToolSpec
from clawpy.tool.base import Tool


class ToolRegistry:
    """Registry of available tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}
        self._order: list[str] = []

    def register(self, tool: Tool) -> None:
        """Register a tool. Later registrations with the same name overwrite."""
        name = tool.name
        if name not in self._tools:
            self._order.append(name)
        self._tools[name] = tool

    def get(self, name: str) -> Tool | None:
        """Look up a tool by name."""
        return self._tools.get(name)

    def all(self) -> list[Tool]:
        """Return all tools in registration order."""
        return [self._tools[n] for n in self._order if n in self._tools]

    def specs(self) -> list[ToolSpec]:
        """Generate ToolSpec list for provider API requests."""
        return [
            ToolSpec(
                name=t.name,
                description=t.description,
                input_schema=t.input_schema(),
            )
            for t in self.all()
        ]

    def __len__(self) -> int:
        return len(self._tools)
