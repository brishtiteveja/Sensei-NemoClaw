"""WebFetch tool — fetch URL content via HTTP.

Mirrors OpenClaude's WebFetchTool: HTML→text conversion, 100K char truncation.
"""

from __future__ import annotations

import re
from typing import Any

import httpx

from clawpy.tool.base import Permission, RunContext, ToolResult

_MAX_CHARS = 100_000
_TIMEOUT = 30.0


def _html_to_text(html: str) -> str:
    """Basic HTML tag stripping. Not perfect but good enough for context."""
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class WebFetchTool:
    """Fetch content from a URL."""

    @property
    def name(self) -> str:
        return "WebFetch"

    @property
    def description(self) -> str:
        return "Fetch content from a URL. Returns text content, converting HTML to plain text."

    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch",
                },
            },
            "required": ["url"],
        }

    def permission_for(self, input: dict[str, Any]) -> Permission:
        return Permission.SHELL_UNSAFE

    def is_read_only(self, input: dict[str, Any]) -> bool:
        return True

    async def run(self, input: dict[str, Any], ctx: RunContext) -> ToolResult:
        url = input.get("url", "")
        if not url:
            return ToolResult(content="Error: url is required", is_error=True)

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(_TIMEOUT),
                follow_redirects=True,
            ) as client:
                resp = await client.get(url, headers={"User-Agent": "ClawPy/0.1"})
                resp.raise_for_status()
        except httpx.TimeoutException:
            return ToolResult(content=f"Timeout fetching {url}", is_error=True)
        except httpx.HTTPStatusError as e:
            return ToolResult(content=f"HTTP {e.response.status_code}: {url}", is_error=True)
        except httpx.HTTPError as e:
            return ToolResult(content=f"Fetch error: {e}", is_error=True)

        content_type = resp.headers.get("content-type", "")
        text = resp.text

        if "html" in content_type.lower():
            text = _html_to_text(text)

        if len(text) > _MAX_CHARS:
            text = text[:_MAX_CHARS] + f"\n... (truncated, {len(text)} total chars)"

        return ToolResult(content=text)
