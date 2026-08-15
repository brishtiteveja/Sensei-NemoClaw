"""Tests for SSE parser."""

import asyncio
import json
from typing import Any, AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest

from clawpy.provider.sse import parse_sse, parse_sse_with_event


class MockResponse:
    """Mock httpx.Response with async line iteration."""

    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    async def aiter_lines(self) -> AsyncIterator[str]:
        for line in self._lines:
            yield line


@pytest.mark.asyncio
async def test_parse_sse_basic():
    lines = [
        'data: {"type": "text", "value": "hello"}',
        "",
        'data: {"type": "text", "value": "world"}',
        "data: [DONE]",
    ]
    resp = MockResponse(lines)
    results: list[dict[str, Any]] = []
    async for data in parse_sse(resp):  # type: ignore
        results.append(data)
    assert len(results) == 2
    assert results[0]["value"] == "hello"
    assert results[1]["value"] == "world"


@pytest.mark.asyncio
async def test_parse_sse_skips_comments():
    lines = [
        ": this is a comment",
        'data: {"x": 1}',
        "data: [DONE]",
    ]
    resp = MockResponse(lines)
    results = [d async for d in parse_sse(resp)]  # type: ignore
    assert len(results) == 1


@pytest.mark.asyncio
async def test_parse_sse_skips_non_data():
    lines = [
        "event: message",
        'data: {"x": 1}',
        "id: 123",
        'data: {"x": 2}',
        "data: [DONE]",
    ]
    resp = MockResponse(lines)
    results = [d async for d in parse_sse(resp)]  # type: ignore
    assert len(results) == 2


@pytest.mark.asyncio
async def test_parse_sse_with_event_type():
    lines = [
        "event: message_start",
        'data: {"type": "start"}',
        "",
        "event: content_block_delta",
        'data: {"type": "delta", "text": "hi"}',
        "",
        "data: [DONE]",
    ]
    resp = MockResponse(lines)
    results = [(ev, d) async for ev, d in parse_sse_with_event(resp)]  # type: ignore
    assert len(results) == 2
    assert results[0][0] == "message_start"
    assert results[1][0] == "content_block_delta"
    assert results[1][1]["text"] == "hi"


@pytest.mark.asyncio
async def test_parse_sse_handles_malformed_json():
    lines = [
        "data: not json",
        'data: {"valid": true}',
        "data: [DONE]",
    ]
    resp = MockResponse(lines)
    results = [d async for d in parse_sse(resp)]  # type: ignore
    assert len(results) == 1
    assert results[0]["valid"] is True
