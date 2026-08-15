"""Tests for tool registry."""

from typing import Any

from clawpy.tool.base import Permission, RunContext, ToolResult
from clawpy.tool.registry import ToolRegistry


class DummyTool:
    @property
    def name(self) -> str:
        return "Dummy"

    @property
    def description(self) -> str:
        return "A dummy tool"

    def input_schema(self) -> dict[str, Any]:
        return {"type": "object", "properties": {"x": {"type": "string"}}}

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.READ_ONLY

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return True

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        return ToolResult(content="ok")


def test_register_and_get():
    reg = ToolRegistry()
    tool = DummyTool()
    reg.register(tool)
    assert reg.get("Dummy") is tool
    assert reg.get("NonExistent") is None


def test_all_preserves_order():
    reg = ToolRegistry()
    t1 = DummyTool()
    t2 = DummyTool()
    # Override name for t2
    t2.__class__ = type("Tool2", (), {**{k: v for k, v in DummyTool.__dict__.items()}, "name": property(lambda s: "Tool2")})
    reg.register(t1)
    reg.register(t2)
    names = [t.name for t in reg.all()]
    assert names == ["Dummy", "Tool2"]


def test_specs_generation():
    reg = ToolRegistry()
    reg.register(DummyTool())
    specs = reg.specs()
    assert len(specs) == 1
    assert specs[0].name == "Dummy"
    assert specs[0].description == "A dummy tool"
    assert "properties" in specs[0].input_schema


def test_len():
    reg = ToolRegistry()
    assert len(reg) == 0
    reg.register(DummyTool())
    assert len(reg) == 1
