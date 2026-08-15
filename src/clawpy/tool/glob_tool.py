"""Glob tool — find files by name patterns.

Mirrors OpenClaude's GlobTool: supports glob patterns,
returns matching file paths sorted by modification time.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult


class GlobTool:
    """Find files matching glob patterns."""

    @property
    def name(self) -> str:
        return "Glob"

    @property
    def description(self) -> str:
        return (
            "Find files matching glob patterns like '**/*.py' or 'src/**/*.ts'. "
            "Returns matching file paths sorted by modification time."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern to match files against",
                },
                "path": {
                    "type": "string",
                    "description": "Directory to search in (default: working directory)",
                },
            },
            "required": ["pattern"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.READ_ONLY

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return True

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        pattern = input.get("pattern", "")
        if not pattern:
            return ToolResult(content="Error: pattern is required", is_error=True)

        search_dir = input.get("path", ctx.work_dir) or ctx.work_dir
        base = Path(search_dir)

        if not base.exists():
            return ToolResult(
                content=f"Error: Directory not found: {search_dir}",
                is_error=True,
            )

        try:
            matches = list(base.glob(pattern))
        except ValueError as e:
            return ToolResult(content=f"Invalid glob pattern: {e}", is_error=True)

        if not matches:
            return ToolResult(content="No files matched the pattern.")

        # Sort by modification time (newest first)
        try:
            matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        except OSError:
            matches.sort()

        # Format output
        lines: list[str] = []
        for p in matches[:1000]:  # Cap at 1000 results
            try:
                rel = p.relative_to(base)
            except ValueError:
                rel = p
            lines.append(str(rel))

        output = "\n".join(lines)
        if len(matches) > 1000:
            output += f"\n... ({len(matches)} total matches, showing first 1000)"

        return ToolResult(content=output)
