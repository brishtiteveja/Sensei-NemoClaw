"""FileRead tool — read files with optional offset and limit.

Mirrors OpenClaude's FileReadTool: supports line offset/limit,
outputs with line numbers (cat -n format).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from clawpy.engine.file_state import FileStateTracker
from clawpy.tool.base import Permission, RunContext, ToolResult


class FileReadTool:
    """Read a file from the local filesystem."""

    def __init__(self, file_state: FileStateTracker | None = None) -> None:
        self._file_state = file_state

    @property
    def name(self) -> str:
        return "Read"

    @property
    def description(self) -> str:
        return (
            "Reads a file from the local filesystem. "
            "The file_path must be an absolute path. "
            "You can optionally specify a line offset and limit."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to read",
                },
                "offset": {
                    "type": "integer",
                    "description": "Line number to start reading from (0-based)",
                    "minimum": 0,
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of lines to read",
                    "exclusiveMinimum": 0,
                },
            },
            "required": ["file_path"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.READ_ONLY

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return True

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        file_path = input.get("file_path", "")
        if not file_path:
            return ToolResult(content="Error: file_path is required", is_error=True)

        # Resolve relative paths against work_dir
        path = Path(file_path)
        if not path.is_absolute():
            path = Path(ctx.work_dir) / path

        if not path.exists():
            return ToolResult(
                content=f"Error: File not found: {path}", is_error=True
            )

        if path.is_dir():
            return ToolResult(
                content=f"Error: {path} is a directory, not a file. Use Bash with ls to list directory contents.",
                is_error=True,
            )

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return ToolResult(content=f"Error reading file: {e}", is_error=True)

        # Register in file state tracker for edit/write enforcement
        if self._file_state is not None:
            self._file_state.register(str(path.resolve()), text)

        lines = text.splitlines(keepends=True)

        offset = input.get("offset", 0)
        limit = input.get("limit")

        if offset > 0:
            lines = lines[offset:]
        if limit is not None and limit > 0:
            lines = lines[:limit]

        if not lines:
            return ToolResult(content="(empty file or no lines in range)")

        # Format with line numbers (cat -n style)
        start_line = offset + 1
        numbered: list[str] = []
        for i, line in enumerate(lines):
            line_no = start_line + i
            # Strip trailing newline for cleaner output
            clean = line.rstrip("\n").rstrip("\r")
            numbered.append(f"{line_no}\t{clean}")

        output = "\n".join(numbered)

        # Truncate very large files
        max_chars = 200_000
        if len(output) > max_chars:
            output = output[:max_chars] + "\n... (truncated)"

        return ToolResult(content=output)
