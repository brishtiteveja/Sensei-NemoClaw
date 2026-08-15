"""Bash tool — execute shell commands.

Mirrors OpenClaude's BashTool: supports timeout, background execution,
and dynamic permission based on command content.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult

# Commands that are always safe (read-only)
_SAFE_COMMANDS = frozenset({
    "cat", "head", "tail", "less", "more", "wc", "sort", "uniq", "diff",
    "grep", "rg", "find", "fd", "ls", "tree", "file", "stat", "du", "df",
    "pwd", "echo", "printf", "date", "whoami", "hostname", "uname",
    "env", "printenv", "which", "whereis", "type",
    "git status", "git log", "git diff", "git show", "git branch",
    "git remote", "git tag", "git rev-parse", "git describe",
    "python --version", "python3 --version", "node --version",
    "npm --version", "go version", "rustc --version", "cargo --version",
})


def _is_read_only_command(cmd: str) -> bool:
    """Heuristic: is this command read-only?"""
    stripped = cmd.strip()
    # Check exact matches and prefix matches
    for safe in _SAFE_COMMANDS:
        if stripped == safe or stripped.startswith(safe + " "):
            return True
    # Reject if contains redirect, pipe to write, or known dangerous patterns
    dangerous_patterns = [">", ">>", "rm ", "rm\t", "mv ", "cp ", "chmod ", "chown ",
                          "kill ", "pkill ", "sudo ", "apt ", "pip install",
                          "npm install", "git push", "git reset", "git checkout"]
    for pat in dangerous_patterns:
        if pat in stripped:
            return False
    return False


class BashTool:
    """Execute shell commands."""

    @property
    def name(self) -> str:
        return "Bash"

    @property
    def description(self) -> str:
        return (
            "Executes a given bash command and returns its output. "
            "The working directory persists between commands."
        )

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute",
                },
                "timeout": {
                    "type": "number",
                    "description": "Optional timeout in milliseconds (max 600000)",
                },
                "description": {
                    "type": "string",
                    "description": "Clear description of what this command does",
                },
            },
            "required": ["command"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        cmd = input.get("command", "")
        if _is_read_only_command(cmd):
            return Permission.SHELL_SAFE
        return Permission.SHELL_UNSAFE

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return _is_read_only_command(input.get("command", ""))

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        command = input.get("command", "")
        if not command:
            return ToolResult(content="Error: command is required", is_error=True)

        timeout_ms = input.get("timeout", 120_000)
        timeout_sec = min(timeout_ms / 1000, 600)

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=ctx.work_dir,
                env={**os.environ},
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout_sec
            )
        except asyncio.TimeoutError:
            return ToolResult(
                content=f"Command timed out after {timeout_sec}s",
                is_error=True,
            )
        except OSError as e:
            return ToolResult(content=f"Command failed: {e}", is_error=True)

        output_parts: list[str] = []
        if stdout:
            output_parts.append(stdout.decode("utf-8", errors="replace"))
        if stderr:
            output_parts.append(f"stderr:\n{stderr.decode('utf-8', errors='replace')}")

        output = "\n".join(output_parts) if output_parts else "(no output)"

        # Truncate very large outputs
        max_chars = 100_000
        if len(output) > max_chars:
            output = output[:max_chars] + f"\n... (truncated, {len(output)} total chars)"

        if proc.returncode != 0:
            output = f"Exit code: {proc.returncode}\n{output}"

        return ToolResult(content=output, is_error=proc.returncode != 0)
