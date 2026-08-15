"""Permission enforcer — gates tool execution based on mode and rules.

Mirrors OpenClaude's permission modes:
- default: ask for non-read-only
- accept_edits: auto-approve workspace writes
- bypass: auto-approve everything
- plan: deny all non-read-only
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from clawpy.tool.base import Permission, Tool


class PermissionMode(str, Enum):
    DEFAULT = "default"
    ACCEPT_EDITS = "accept_edits"
    BYPASS = "bypass"
    PLAN = "plan"


class PermissionEnforcer:
    """Checks whether a tool invocation is permitted."""

    def __init__(
        self,
        mode: PermissionMode,
        work_dir: str,
        allow_rules: list[str] | None = None,
        deny_rules: list[str] | None = None,
    ) -> None:
        self.mode = mode
        self.work_dir = work_dir
        self.allow_rules: list[str] = allow_rules or []
        self.deny_rules: list[str] = deny_rules or []

    def check(self, tool: Tool, input: dict[str, Any]) -> str | None:
        """Check if a tool invocation is allowed.

        Returns None if allowed, or an error message string if denied.
        """
        perm = tool.permission_for(input)

        # Read-only always allowed
        if perm == Permission.READ_ONLY:
            return None

        # Deny rules take precedence
        if tool.name in self.deny_rules:
            return f"Tool {tool.name!r} is denied by configuration"

        # Allow rules override mode
        if tool.name in self.allow_rules:
            return None

        match self.mode:
            case PermissionMode.BYPASS:
                return None
            case PermissionMode.ACCEPT_EDITS:
                if perm <= Permission.WORKSPACE_WRITE:
                    return None
                return (
                    f"Tool {tool.name!r} requires elevated permission "
                    f"(level {perm.name})"
                )
            case PermissionMode.PLAN:
                return f"Tool {tool.name!r} blocked in plan mode"
            case PermissionMode.DEFAULT:
                # In default mode, non-read-only tools need interactive approval.
                # For now, we return an "ask" indicator — the engine handles prompting.
                return f"ASK:Tool {tool.name!r} requires permission ({perm.name})"
