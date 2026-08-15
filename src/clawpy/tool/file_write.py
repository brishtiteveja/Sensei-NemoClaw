"""FileWrite tool — write entire file content.

Mirrors OpenClaude's FileWriteTool:
- Read-before-write enforcement (existing files must be read first)
- Mtime staleness check
- Updates file_state after write
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from clawpy.engine.file_state import FileStateTracker
from clawpy.tool.base import Permission, RunContext, ToolResult


class FileWriteTool:
    """Write content to a file, creating it if it doesn't exist."""

    def __init__(self, file_state: FileStateTracker | None = None) -> None:
        self._file_state = file_state

    @property
    def name(self) -> str:
        return "Write"

    @property
    def description(self) -> str:
        return (
            "Writes content to a file. If the file exists, you MUST read it first. "
            "This tool will overwrite the existing file."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to write",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.WORKSPACE_WRITE

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return False

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        file_path = input.get("file_path", "")
        content = input.get("content", "")

        if not file_path:
            return ToolResult(content="Error: file_path is required", is_error=True)

        path = Path(file_path)
        if not path.is_absolute():
            path = Path(ctx.work_dir) / path

        # Read-before-write enforcement
        if self._file_state is not None:
            error = self._file_state.check_writable(str(path))
            if error:
                return ToolResult(content=f"Error: {error}", is_error=True)

        # Ensure parent directory exists
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return ToolResult(content=f"Error creating directory: {e}", is_error=True)

        # Write the file
        try:
            path.write_text(content, encoding="utf-8")
        except OSError as e:
            return ToolResult(content=f"Error writing file: {e}", is_error=True)

        # Update file state
        if self._file_state is not None:
            self._file_state.update_after_write(str(path.resolve()), content)

        line_count = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
        return ToolResult(content=f"Successfully wrote {line_count} lines to {path}")
