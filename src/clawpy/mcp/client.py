"""MCP (Model Context Protocol) client — JSON-RPC 2.0 over stdio.

Connects to MCP servers that expose tools, resources, and prompts.
Tools are merged into the ToolRegistry alongside built-in tools.
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from clawpy.provider.base import ToolSpec

logger = logging.getLogger(__name__)

_JSONRPC_VERSION = "2.0"
_MCP_PROTOCOL_VERSION = "2024-11-05"


@dataclass(slots=True)
class MCPTool:
    """A tool discovered from an MCP server."""

    name: str
    description: str
    input_schema: dict[str, Any]
    server_name: str


@dataclass(slots=True)
class MCPServerConfig:
    """Configuration for an MCP server."""

    name: str
    command: list[str]  # e.g. ["npx", "-y", "@modelcontextprotocol/server-filesystem"]
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)


class MCPClient:
    """Client for a single MCP server over stdio."""

    def __init__(self, config: MCPServerConfig) -> None:
        self.config = config
        self._process: asyncio.subprocess.Process | None = None
        self._request_id = 0
        self._tools: list[MCPTool] = []
        self._pending: dict[int, asyncio.Future[Any]] = {}
        self._reader_task: asyncio.Task[None] | None = None

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def tools(self) -> list[MCPTool]:
        return self._tools

    async def connect(self) -> None:
        """Start the MCP server process and initialize."""
        cmd = self.config.command + self.config.args
        self._process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**dict(__import__("os").environ), **self.config.env},
        )
        self._reader_task = asyncio.create_task(self._read_loop())

        # Initialize
        result = await self._request("initialize", {
            "protocolVersion": _MCP_PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "clawpy", "version": "0.1.0"},
        })
        logger.info("MCP %s initialized: %s", self.name, result)

        # Send initialized notification
        await self._notify("notifications/initialized", {})

        # List tools
        tools_result = await self._request("tools/list", {})
        for t in tools_result.get("tools", []):
            self._tools.append(MCPTool(
                name=f"{self.name}_{t['name']}",
                description=t.get("description", ""),
                input_schema=t.get("inputSchema", {"type": "object"}),
                server_name=self.name,
            ))
        logger.info("MCP %s: %d tools", self.name, len(self._tools))

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """Call a tool on the MCP server."""
        # Strip server prefix from tool name
        bare_name = tool_name
        prefix = f"{self.name}_"
        if bare_name.startswith(prefix):
            bare_name = bare_name[len(prefix):]

        result = await self._request("tools/call", {
            "name": bare_name,
            "arguments": arguments,
        })
        # Extract text content from result
        content_parts: list[str] = []
        for item in result.get("content", []):
            if item.get("type") == "text":
                content_parts.append(item.get("text", ""))
        return "\n".join(content_parts) or json.dumps(result)

    async def disconnect(self) -> None:
        """Shut down the MCP server."""
        if self._process and self._process.returncode is None:
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=5)
            except asyncio.TimeoutError:
                self._process.kill()
        if self._reader_task:
            self._reader_task.cancel()

    def tool_specs(self) -> list[ToolSpec]:
        """Convert MCP tools to provider ToolSpecs."""
        return [
            ToolSpec(name=t.name, description=t.description, input_schema=t.input_schema)
            for t in self._tools
        ]

    async def _request(self, method: str, params: dict[str, Any]) -> Any:
        """Send a JSON-RPC request and wait for response."""
        self._request_id += 1
        req_id = self._request_id

        msg = {
            "jsonrpc": _JSONRPC_VERSION,
            "id": req_id,
            "method": method,
            "params": params,
        }
        future: asyncio.Future[Any] = asyncio.get_event_loop().create_future()
        self._pending[req_id] = future

        await self._send(msg)
        return await asyncio.wait_for(future, timeout=30)

    async def _notify(self, method: str, params: dict[str, Any]) -> None:
        """Send a JSON-RPC notification (no response expected)."""
        msg = {
            "jsonrpc": _JSONRPC_VERSION,
            "method": method,
            "params": params,
        }
        await self._send(msg)

    async def _send(self, msg: dict[str, Any]) -> None:
        """Write a JSON-RPC message to the server's stdin."""
        if not self._process or not self._process.stdin:
            raise RuntimeError("MCP server not connected")
        data = json.dumps(msg)
        self._process.stdin.write(f"{data}\n".encode())
        await self._process.stdin.drain()

    async def _read_loop(self) -> None:
        """Read JSON-RPC responses from the server's stdout."""
        if not self._process or not self._process.stdout:
            return
        try:
            while True:
                line = await self._process.stdout.readline()
                if not line:
                    break
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                req_id = msg.get("id")
                if req_id and req_id in self._pending:
                    future = self._pending.pop(req_id)
                    if "error" in msg:
                        future.set_exception(RuntimeError(str(msg["error"])))
                    else:
                        future.set_result(msg.get("result", {}))
        except asyncio.CancelledError:
            pass


class MCPToolWrapper:
    """Wraps an MCP server tool as a ClawPy Tool for the ToolRegistry."""

    def __init__(self, client: MCPClient, spec: ToolSpec) -> None:
        self._client = client
        self._spec = spec

    @property
    def name(self) -> str:
        return self._spec.name

    @property
    def description(self) -> str:
        return self._spec.description

    def input_schema(self) -> dict[str, Any]:
        return self._spec.input_schema

    def permission_for(self, input: dict[str, Any]) -> Any:
        from clawpy.tool.base import Permission
        return Permission.SHELL_SAFE

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return False

    async def run(self, input: dict[str, Any], ctx: Any) -> Any:
        from clawpy.tool.base import ToolResult
        try:
            result = await self._client.call_tool(self._spec.name, input)
            return ToolResult(content=result)
        except Exception as e:
            return ToolResult(content=f"MCP tool error: {e}", is_error=True)


def load_mcp_configs(work_dir: str) -> list[MCPServerConfig]:
    """Load MCP server configs from .clawpy/mcp.json or .mcp.json."""
    configs: list[MCPServerConfig] = []
    for name in [".clawpy/mcp.json", ".mcp.json"]:
        path = Path(work_dir) / name
        if path.exists():
            try:
                data = json.loads(path.read_text())
                servers = data.get("mcpServers", data.get("servers", {}))
                for srv_name, srv_cfg in servers.items():
                    cmd = srv_cfg.get("command", "")
                    args = srv_cfg.get("args", [])
                    if isinstance(cmd, str):
                        cmd = [cmd]
                    configs.append(MCPServerConfig(
                        name=srv_name,
                        command=cmd,
                        args=args,
                        env=srv_cfg.get("env", {}),
                    ))
            except (json.JSONDecodeError, OSError):
                pass
    return configs
