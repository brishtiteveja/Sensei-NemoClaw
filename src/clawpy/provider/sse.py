"""Shared SSE (Server-Sent Events) parser.

Both Anthropic and OpenAI stream as text/event-stream with `data: {...}\n\n` framing.
This replaces the need for any SSE library — just a thin async generator over httpx lines.
"""

from __future__ import annotations

import json
from typing import Any, AsyncIterator

import httpx


async def parse_sse(response: httpx.Response) -> AsyncIterator[dict[str, Any]]:
    """Parse SSE stream, yielding parsed JSON data objects.

    Handles:
    - `data: {...}` lines → yield parsed JSON
    - `data: [DONE]` → stop iteration
    - `event:` lines → ignored (we only need data)
    - Empty lines → ignored (SSE frame separators)
    """
    async for line in response.aiter_lines():
        line = line.strip()
        if not line or line.startswith(":"):
            continue
        if not line.startswith("data: "):
            continue
        data = line[6:]
        if data == "[DONE]":
            return
        try:
            yield json.loads(data)
        except json.JSONDecodeError:
            continue


async def parse_sse_with_event(
    response: httpx.Response,
) -> AsyncIterator[tuple[str, dict[str, Any]]]:
    """Parse SSE stream, yielding (event_type, data) tuples.

    Used by providers that need the `event:` field (e.g., Anthropic).
    """
    event_type = "message"
    async for line in response.aiter_lines():
        line = line.strip()
        if not line:
            event_type = "message"
            continue
        if line.startswith(":"):
            continue
        if line.startswith("event: "):
            event_type = line[7:]
            continue
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                return
            try:
                yield event_type, json.loads(data)
            except json.JSONDecodeError:
                continue
