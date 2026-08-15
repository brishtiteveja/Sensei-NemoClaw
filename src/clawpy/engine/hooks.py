"""Hooks system — run shell commands before/after tool execution.

Hooks are configured in settings.json:
  {"hooks": {"pre_tool_use": [...], "post_tool_use": [...]}}

Each hook: {"tool": "Bash", "if": "command:git*", "command": "echo 'detected'"}
"""

from __future__ import annotations

import asyncio
import fnmatch
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class HookConfig:
    """A single hook definition from settings."""

    command: str
    tool: str = ""  # Empty = match all tools
    if_condition: str = ""  # Empty = always match


@dataclass(frozen=True, slots=True)
class HookResult:
    """Result of running hooks."""

    blocked: bool = False
    message: str = ""


@dataclass(slots=True)
class HooksRegistry:
    """Registry of configured hooks."""

    pre_tool_use: list[HookConfig] = field(default_factory=list)
    post_tool_use: list[HookConfig] = field(default_factory=list)

    @classmethod
    def from_config(cls, config_data: dict[str, Any]) -> HooksRegistry:
        """Parse hooks from settings.json 'hooks' key."""
        hooks_data = config_data.get("hooks", {})
        if not isinstance(hooks_data, dict):
            return cls()

        return cls(
            pre_tool_use=_parse_hook_list(hooks_data.get("pre_tool_use", [])),
            post_tool_use=_parse_hook_list(hooks_data.get("post_tool_use", [])),
        )


def _parse_hook_list(data: Any) -> list[HookConfig]:
    if not isinstance(data, list):
        return []
    hooks: list[HookConfig] = []
    for item in data:
        if isinstance(item, dict) and "command" in item:
            hooks.append(HookConfig(
                command=item["command"],
                tool=item.get("tool", ""),
                if_condition=item.get("if", ""),
            ))
    return hooks


def _matches_condition(condition: str, tool_input: dict[str, Any]) -> bool:
    """Check if a hook's 'if' condition matches the tool input.

    Condition format: "key:pattern" where pattern supports glob wildcards.
    Example: "command:git*" matches tool_input={"command": "git status"}
    """
    if not condition:
        return True

    if ":" not in condition:
        return True

    key, pattern = condition.split(":", 1)
    value = str(tool_input.get(key, ""))
    return fnmatch.fnmatch(value, pattern)


async def run_pre_tool_hooks(
    hooks: list[HookConfig],
    tool_name: str,
    tool_input: dict[str, Any],
    work_dir: str,
) -> HookResult:
    """Run pre-tool hooks. Can block tool execution (non-zero exit)."""
    for hook in hooks:
        if hook.tool and hook.tool != tool_name:
            continue
        if not _matches_condition(hook.if_condition, tool_input):
            continue

        env = {
            **os.environ,
            "CLAWPY_TOOL_NAME": tool_name,
            "CLAWPY_TOOL_INPUT": json.dumps(tool_input),
        }

        try:
            proc = await asyncio.create_subprocess_shell(
                hook.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=work_dir,
                env=env,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        except asyncio.TimeoutError:
            logger.warning("Pre-tool hook timed out: %s", hook.command)
            continue
        except OSError as e:
            logger.warning("Pre-tool hook failed: %s: %s", hook.command, e)
            continue

        if proc.returncode != 0:
            msg = stderr.decode("utf-8", errors="replace").strip()
            return HookResult(blocked=True, message=msg or f"Hook exited with code {proc.returncode}")

    return HookResult(blocked=False)


async def run_post_tool_hooks(
    hooks: list[HookConfig],
    tool_name: str,
    tool_input: dict[str, Any],
    tool_output: str,
    work_dir: str,
) -> None:
    """Run post-tool hooks (informational, cannot block)."""
    for hook in hooks:
        if hook.tool and hook.tool != tool_name:
            continue
        if not _matches_condition(hook.if_condition, tool_input):
            continue

        env = {
            **os.environ,
            "CLAWPY_TOOL_NAME": tool_name,
            "CLAWPY_TOOL_INPUT": json.dumps(tool_input),
            "CLAWPY_TOOL_OUTPUT": tool_output[:10_000],  # Truncate for env var
        }

        try:
            proc = await asyncio.create_subprocess_shell(
                hook.command,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
                cwd=work_dir,
                env=env,
            )
            await asyncio.wait_for(proc.communicate(), timeout=30)
        except (asyncio.TimeoutError, OSError) as e:
            logger.warning("Post-tool hook failed: %s: %s", hook.command, e)
