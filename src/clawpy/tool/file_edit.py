"""FileEdit tool — search and replace in files.

Mirrors OpenClaude's FileEditTool:
- old_string must be unique in file (unless replace_all=True)
- Read-before-write enforcement
- Mtime staleness check
- Updates file_state after edit
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from clawpy.engine.file_state import FileStateTracker
from clawpy.tool.base import Permission, RunContext, ToolResult


class FileEditTool:
    """Edit a file by replacing exact string matches."""

    def __init__(self, file_state: FileStateTracker | None = None) -> None:
        self._file_state = file_state

    @property
    def name(self) -> str:
        return "Edit"

    @property
    def description(self) -> str:
        return (
            "Performs exact string replacements in files. "
            "The old_string must be unique in the file unless replace_all is set. "
            "You MUST read the file first before editing."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to modify",
                },
                "old_string": {
                    "type": "string",
                    "description": "The text to replace",
                },
                "new_string": {
                    "type": "string",
                    "description": "The replacement text (must differ from old_string)",
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Replace all occurrences (default false)",
                    "default": False,
                },
            },
            "required": ["file_path", "old_string", "new_string"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.WORKSPACE_WRITE

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return False

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        file_path = input.get("file_path", "")
        old_string = input.get("old_string", "")
        new_string = input.get("new_string", "")
        replace_all = input.get("replace_all", False)

        if not file_path:
            return ToolResult(content="Error: file_path is required", is_error=True)
        if old_string == new_string:
            return ToolResult(content="Error: old_string and new_string must differ", is_error=True)

        path = Path(file_path)
        if not path.is_absolute():
            path = Path(ctx.work_dir) / path

        # Handle file creation (empty old_string + non-existent file)
        if not old_string and not path.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(new_string, encoding="utf-8")
            except OSError as e:
                return ToolResult(content=f"Error creating file: {e}", is_error=True)
            if self._file_state is not None:
                self._file_state.update_after_write(str(path.resolve()), new_string)
            return ToolResult(content=f"Created new file {path}")

        if not path.exists():
            return ToolResult(content=f"Error: File not found: {path}", is_error=True)

        # Read-before-write enforcement
        if self._file_state is not None:
            error = self._file_state.check_writable(str(path))
            if error:
                return ToolResult(content=f"Error: {error}", is_error=True)

        # Read current content
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return ToolResult(content=f"Error reading file: {e}", is_error=True)

        # Check old_string exists
        if not old_string:
            return ToolResult(
                content="Error: old_string is required for existing files",
                is_error=True,
            )

        count = content.count(old_string)
        if count == 0:
            return ToolResult(
                content=f"Error: old_string not found in {path}",
                is_error=True,
            )

        if count > 1 and not replace_all:
            return ToolResult(
                content=(
                    f"Error: old_string found {count} times in {path}. "
                    "Use replace_all=true to replace all occurrences, "
                    "or provide a larger unique string."
                ),
                is_error=True,
            )

        # Perform replacement
        if replace_all:
            new_content = content.replace(old_string, new_string)
        else:
            new_content = content.replace(old_string, new_string, 1)

        # Generate diff for display
        import difflib
        diff_lines = list(difflib.unified_diff(
            content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=str(path),
            tofile=str(path),
            n=3,
        ))
        diff_text = "".join(diff_lines)

        # Write back
        try:
            path.write_text(new_content, encoding="utf-8")
        except OSError as e:
            return ToolResult(content=f"Error writing file: {e}", is_error=True)

        # Update file state
        if self._file_state is not None:
            self._file_state.update_after_write(str(path.resolve()), new_content)

        replacements = count if replace_all else 1
        summary = f"Replaced {replacements} occurrence(s) in {path}"
        if diff_text:
            summary += f"\n\n{diff_text}"
        return ToolResult(content=summary)
