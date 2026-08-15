"""Tests for permission enforcer."""

from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult
from clawpy.tool.permission import PermissionEnforcer, PermissionMode


class MockTool:
    def __init__(self, name: str = "Test", perm: Permission = Permission.SHELL_UNSAFE):
        self._name = name
        self._perm = perm

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return ""

    def input_schema(self) -> dict[str, Any]:
        return {}

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return self._perm

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return self._perm == Permission.READ_ONLY

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        return ToolResult(content="")


def test_read_only_always_allowed():
    enforcer = PermissionEnforcer(mode=PermissionMode.PLAN, work_dir=".")
    tool = MockTool(perm=Permission.READ_ONLY)
    assert enforcer.check(tool, {}) is None


def test_plan_mode_blocks_writes():
    enforcer = PermissionEnforcer(mode=PermissionMode.PLAN, work_dir=".")
    tool = MockTool(perm=Permission.WORKSPACE_WRITE)
    result = enforcer.check(tool, {})
    assert result is not None
    assert "plan mode" in result


def test_bypass_mode_allows_all():
    enforcer = PermissionEnforcer(mode=PermissionMode.BYPASS, work_dir=".")
    tool = MockTool(perm=Permission.DANGEROUS)
    assert enforcer.check(tool, {}) is None


def test_accept_edits_allows_workspace_write():
    enforcer = PermissionEnforcer(mode=PermissionMode.ACCEPT_EDITS, work_dir=".")
    tool = MockTool(perm=Permission.WORKSPACE_WRITE)
    assert enforcer.check(tool, {}) is None


def test_accept_edits_blocks_shell_unsafe():
    enforcer = PermissionEnforcer(mode=PermissionMode.ACCEPT_EDITS, work_dir=".")
    tool = MockTool(perm=Permission.SHELL_UNSAFE)
    result = enforcer.check(tool, {})
    assert result is not None
    assert "elevated" in result


def test_deny_rules():
    enforcer = PermissionEnforcer(
        mode=PermissionMode.BYPASS, work_dir=".", deny_rules=["Bash"]
    )
    tool = MockTool(name="Bash", perm=Permission.SHELL_UNSAFE)
    result = enforcer.check(tool, {})
    assert result is not None
    assert "denied" in result


def test_allow_rules():
    enforcer = PermissionEnforcer(
        mode=PermissionMode.DEFAULT, work_dir=".", allow_rules=["Bash"]
    )
    tool = MockTool(name="Bash", perm=Permission.SHELL_UNSAFE)
    assert enforcer.check(tool, {}) is None
