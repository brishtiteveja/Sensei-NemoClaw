"""Grep tool — search file contents using ripgrep.

Mirrors OpenClaude's GrepTool: supports output modes (content/files_with_matches/count),
head_limit, offset, context lines, case insensitive, glob filter, multiline.
"""

from __future__ import annotations

import asyncio
from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult


class GrepTool:
    """Search file contents using regex patterns via ripgrep."""

    @property
    def name(self) -> str:
        return "Grep"

    @property
    def description(self) -> str:
        return (
            "Search file contents using regex patterns. Uses ripgrep. "
            "Supports output modes: content, files_with_matches, count."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for",
                },
                "path": {
                    "type": "string",
                    "description": "Directory or file to search in",
                },
                "glob": {
                    "type": "string",
                    "description": "Glob pattern to filter files (e.g. '*.py')",
                },
                "output_mode": {
                    "type": "string",
                    "enum": ["content", "files_with_matches", "count"],
                    "description": "Output mode (default: files_with_matches)",
                },
                "-i": {
                    "type": "boolean",
                    "description": "Case insensitive search",
                },
                "-n": {
                    "type": "boolean",
                    "description": "Show line numbers (default true for content mode)",
                },
                "-A": {
                    "type": "number",
                    "description": "Lines to show after each match",
                },
                "-B": {
                    "type": "number",
                    "description": "Lines to show before each match",
                },
                "-C": {
                    "type": "number",
                    "description": "Lines of context around each match",
                },
                "head_limit": {
                    "type": "number",
                    "description": "Limit output to first N entries (default 250)",
                },
                "multiline": {
                    "type": "boolean",
                    "description": "Enable multiline matching",
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

        output_mode = input.get("output_mode", "files_with_matches")

        args: list[str] = ["rg", "--no-heading", "--color=never"]

        # Output mode
        if output_mode == "files_with_matches":
            args.append("--files-with-matches")
        elif output_mode == "count":
            args.append("--count")
        else:
            # content mode — show line numbers by default
            show_lines = input.get("-n", True)
            if show_lines:
                args.append("--line-number")

        # Options
        if input.get("-i"):
            args.append("-i")
        if input.get("multiline"):
            args.extend(["-U", "--multiline-dotall"])
        if input.get("glob"):
            args.extend(["--glob", input["glob"]])

        # Context lines
        if input.get("-C") is not None:
            args.extend(["-C", str(int(input["-C"]))])
        else:
            if input.get("-A") is not None:
                args.extend(["-A", str(int(input["-A"]))])
            if input.get("-B") is not None:
                args.extend(["-B", str(int(input["-B"]))])

        args.append(pattern)

        # Search path
        search_path = input.get("path", ctx.work_dir) or ctx.work_dir
        args.append(search_path)

        try:
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=ctx.work_dir,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        except FileNotFoundError:
            return ToolResult(
                content="Error: ripgrep (rg) not found. Please install it.",
                is_error=True,
            )
        except asyncio.TimeoutError:
            return ToolResult(content="Search timed out after 30s", is_error=True)

        if proc.returncode == 1:
            return ToolResult(content="No matches found.")
        if proc.returncode not in (0, 1):
            err = stderr.decode("utf-8", errors="replace").strip()
            return ToolResult(content=f"rg error: {err}", is_error=True)

        output = stdout.decode("utf-8", errors="replace").strip()
        if not output:
            return ToolResult(content="No matches found.")

        # Apply head_limit
        head_limit = int(input.get("head_limit", 250))
        if head_limit > 0:
            lines = output.split("\n")
            if len(lines) > head_limit:
                total = len(lines)
                lines = lines[:head_limit]
                lines.append(f"... truncated ({total} total lines)")
                output = "\n".join(lines)

        return ToolResult(content=output)
