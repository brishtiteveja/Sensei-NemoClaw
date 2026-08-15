"""ListFiles tool — list directory contents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult


class ListFilesTool:
    """List files and directories."""

    @property
    def name(self) -> str:
        return "ListFiles"

    @property
    def description(self) -> str:
        return "List files and directories in a given path."

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to list (default: working directory)",
                },
            },
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.READ_ONLY

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return True

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        dir_path = input.get("path", ctx.work_dir) or ctx.work_dir
        path = Path(dir_path)
        if not path.is_absolute():
            path = Path(ctx.work_dir) / path

        if not path.exists():
            return ToolResult(content=f"Error: Path not found: {path}", is_error=True)
        if not path.is_dir():
            return ToolResult(content=f"Error: {path} is not a directory", is_error=True)

        try:
            entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError as e:
            return ToolResult(content=f"Error listing directory: {e}", is_error=True)

        lines: list[str] = []
        for entry in entries[:500]:
            prefix = "d " if entry.is_dir() else "f "
            lines.append(f"{prefix}{entry.name}")

        if len(entries) > 500:
            lines.append(f"... ({len(entries)} total entries, showing first 500)")

        return ToolResult(content="\n".join(lines) if lines else "(empty directory)")
