"""OpenAI Chat Completions provider.

Mirrors openaiShim.ts from OpenClaude:
- convertMessages(): neutral → OpenAI format
- convertTools(): ToolSpec → OpenAI function format (normalize required fields)
- Stream state machine: OpenAI SSE chunks → neutral StreamEvents

Also serves as base for Gemini, Ollama, and DeepSeek (all OpenAI-compatible).
"""

from __future__ import annotations

import json
import os
from typing import Any, AsyncIterator

import httpx

from clawpy.config.config import ProviderConfig
from clawpy.provider.base import (
    Delta,
    EventType,
    Request,
    Response,
    StopReason,
    StreamEvent,
    ToolSpec,
    Usage,
)
from clawpy.provider.registry import register
from clawpy.provider.sse import parse_sse
from clawpy.types import ContentBlock, ContentType, Message, Role, ToolCall

_DEFAULT_BASE_URL = "https://api.openai.com/v1"

# Finish reason mapping (OpenAI → neutral)
_STOP_MAP: dict[str | None, StopReason] = {
    "stop": StopReason.END_TURN,
    "tool_calls": StopReason.TOOL_USE,
    "length": StopReason.MAX_TOKENS,
}


class OpenAIProvider:
    """OpenAI Chat Completions API provider.

    Handles the full conversion between neutral types and OpenAI's format.
    Subclassed by Gemini, Ollama, DeepSeek with different base URLs / keys.
    """

    def __init__(self, cfg: ProviderConfig) -> None:
        self._api_key = cfg.api_key or os.environ.get("OPENAI_API_KEY", "")
        self._base_url = (cfg.base_url or _DEFAULT_BASE_URL).rstrip("/")
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0))
        self._provider_name = "openai"

    @property
    def name(self) -> str:
        return self._provider_name

    def models(self) -> list[str]:
        return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1", "o1-mini", "o3-mini"]

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    # ---- Message conversion (neutral → OpenAI) ----

    def _convert_messages(self, request: Request) -> list[dict[str, Any]]:
        """Convert neutral Messages to OpenAI chat format.

        Key mappings (from openaiShim.ts convertMessages()):
        - System prompt → {role: "system", content: text}
        - User text → {role: "user", content: text}
        - Assistant text + tool calls → {role: "assistant", content, tool_calls}
        - ToolResult → {role: "tool", tool_call_id, content}
        - Thinking blocks → stripped (OpenAI doesn't support them)
        """
        result: list[dict[str, Any]] = []

        # System prompt as first message
        if request.system:
            result.append({"role": "system", "content": request.system})

        for msg in request.messages:
            assert isinstance(msg, Message)

            if msg.role == Role.USER:
                # Split tool_result blocks into separate "tool" messages
                text_parts: list[str] = []
                for block in msg.content:
                    if block.type == ContentType.TOOL_RESULT and block.tool_result:
                        tr = block.tool_result
                        content = tr.content
                        if tr.is_error:
                            content = f"Error: {content}"
                        result.append({
                            "role": "tool",
                            "tool_call_id": tr.tool_call_id,
                            "content": content,
                        })
                    elif block.type == ContentType.TEXT:
                        text_parts.append(block.text)
                if text_parts:
                    result.append({"role": "user", "content": "".join(text_parts)})

            elif msg.role == Role.ASSISTANT:
                text_parts = []
                tool_calls: list[dict[str, Any]] = []
                for block in msg.content:
                    if block.type == ContentType.TEXT:
                        text_parts.append(block.text)
                    elif block.type == ContentType.TOOL_CALL and block.tool_call:
                        tc = block.tool_call
                        tool_calls.append({
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": json.dumps(tc.input),
                            },
                        })
                    # Thinking blocks are stripped

                entry: dict[str, Any] = {"role": "assistant"}
                content = "".join(text_parts)
                if content:
                    entry["content"] = content
                if tool_calls:
                    entry["tool_calls"] = tool_calls
                result.append(entry)

            elif msg.role == Role.SYSTEM:
                text = msg.text_content()
                if text:
                    result.append({"role": "system", "content": text})

        return result

    # ---- Tool conversion (ToolSpec → OpenAI function format) ----

    def _convert_tools(self, tools: list[ToolSpec]) -> list[dict[str, Any]] | None:
        """Convert ToolSpecs to OpenAI function tools.

        From openaiShim.ts convertTools(): normalizes all properties into
        required array (OpenAI strict mode needs this).
        """
        if not tools:
            return None
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": _normalize_schema(t.input_schema),
                },
            }
            for t in tools
        ]

    # ---- Streaming ----

    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]:
        """Stream a request, yielding neutral StreamEvents."""
        body: dict[str, Any] = {
            "model": request.model,
            "messages": self._convert_messages(request),
            "max_completion_tokens": request.max_tokens,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        tools = self._convert_tools(request.tools)
        if tools:
            body["tools"] = tools
        if request.temperature is not None:
            body["temperature"] = request.temperature

        # State tracking (mirrors openaiShim.ts state vars)
        content_started = False
        active_tool_calls: dict[int, dict[str, str]] = {}  # index → {id, name}
        tool_json_bufs: dict[int, str] = {}  # index → accumulated JSON
        has_processed_finish = False

        async with self._client.stream(
            "POST",
            f"{self._base_url}/chat/completions",
            json=body,
            headers=self._headers(),
        ) as resp:
            if resp.status_code != 200:
                error_body = await resp.aread()
                yield StreamEvent(
                    type=EventType.ERROR,
                    error=RuntimeError(
                        f"OpenAI API error {resp.status_code}: {error_body.decode()}"
                    ),
                )
                return

            async for data in parse_sse(resp):
                for event in self._map_chunk(
                    data, content_started, active_tool_calls,
                    tool_json_bufs, has_processed_finish,
                ):
                    yield event
                    # Update state flags from yielded events
                    if event.type == EventType.DELTA and event.delta and event.delta.text:
                        content_started = True
                    if event.type == EventType.MESSAGE_STOP:
                        has_processed_finish = True

    def _map_chunk(
        self,
        data: dict[str, Any],
        content_started: bool,
        active_tool_calls: dict[int, dict[str, str]],
        tool_json_bufs: dict[int, str],
        has_processed_finish: bool,
    ) -> list[StreamEvent]:
        """Map an OpenAI SSE chunk to neutral StreamEvents.

        Mirrors openaiStreamToAnthropic() state machine from openaiShim.ts.
        """
        events: list[StreamEvent] = []

        choices = data.get("choices", [])
        usage_data = data.get("usage")

        if not choices and usage_data and not has_processed_finish:
            # Usage-only chunk (no choices)
            events.append(StreamEvent(
                type=EventType.MESSAGE_STOP,
                stop_reason=StopReason.END_TURN,
                usage=Usage(
                    input_tokens=usage_data.get("prompt_tokens", 0),
                    output_tokens=usage_data.get("completion_tokens", 0),
                ),
            ))
            return events

        for choice in choices:
            delta = choice.get("delta", {})
            finish_reason = choice.get("finish_reason")

            # Text delta
            text_content = delta.get("content")
            if text_content:
                events.append(StreamEvent(
                    type=EventType.DELTA,
                    delta=Delta(text=text_content),
                ))

            # Tool calls
            for tc in delta.get("tool_calls", []):
                tc_index = tc.get("index", 0)
                tc_id = tc.get("id")
                tc_func = tc.get("function", {})
                tc_name = tc_func.get("name")
                tc_args = tc_func.get("arguments", "")

                if tc_id and tc_name:
                    # New tool call (has id + name)
                    active_tool_calls[tc_index] = {"id": tc_id, "name": tc_name}
                    tool_json_bufs[tc_index] = tc_args
                    events.append(StreamEvent(
                        type=EventType.TOOL_START,
                        tool_call=ToolCall(id=tc_id, name=tc_name, input={}),
                    ))
                    if tc_args:
                        events.append(StreamEvent(
                            type=EventType.TOOL_DELTA,
                            delta=Delta(text=tc_args),
                        ))
                elif tc_index in active_tool_calls:
                    # Continuation (just arguments)
                    tool_json_bufs[tc_index] = tool_json_bufs.get(tc_index, "") + tc_args
                    if tc_args:
                        events.append(StreamEvent(
                            type=EventType.TOOL_DELTA,
                            delta=Delta(text=tc_args),
                        ))

            # Finish reason
            if finish_reason and not has_processed_finish:
                # Finalize all active tool calls
                for idx in sorted(active_tool_calls.keys()):
                    info = active_tool_calls[idx]
                    raw_json = tool_json_bufs.get(idx, "")
                    parsed: dict[str, Any] = {}
                    if raw_json:
                        try:
                            parsed = json.loads(raw_json)
                        except json.JSONDecodeError:
                            parsed = {"_raw": raw_json}
                    events.append(StreamEvent(
                        type=EventType.TOOL_END,
                        tool_call=ToolCall(id=info["id"], name=info["name"], input=parsed),
                    ))
                active_tool_calls.clear()
                tool_json_bufs.clear()

                stop = _STOP_MAP.get(finish_reason, StopReason.END_TURN)
                usage = Usage()
                if usage_data:
                    usage = Usage(
                        input_tokens=usage_data.get("prompt_tokens", 0),
                        output_tokens=usage_data.get("completion_tokens", 0),
                    )
                events.append(StreamEvent(
                    type=EventType.MESSAGE_STOP,
                    stop_reason=stop,
                    usage=usage,
                ))

        return events

    # ---- Non-streaming ----

    async def send(self, request: Request) -> Response:
        """Non-streaming request."""
        body: dict[str, Any] = {
            "model": request.model,
            "messages": self._convert_messages(request),
            "max_completion_tokens": request.max_tokens,
        }
        tools = self._convert_tools(request.tools)
        if tools:
            body["tools"] = tools

        resp = await self._client.post(
            f"{self._base_url}/chat/completions",
            json=body,
            headers=self._headers(),
        )
        resp.raise_for_status()
        data = resp.json()

        content: list[ContentBlock] = []
        choice = data.get("choices", [{}])[0]
        msg = choice.get("message", {})

        if msg.get("content"):
            content.append(ContentBlock(type=ContentType.TEXT, text=msg["content"]))
        for tc in msg.get("tool_calls", []):
            func = tc.get("function", {})
            input_data: dict[str, Any] = {}
            if func.get("arguments"):
                try:
                    input_data = json.loads(func["arguments"])
                except json.JSONDecodeError:
                    input_data = {"_raw": func["arguments"]}
            content.append(ContentBlock(
                type=ContentType.TOOL_CALL,
                tool_call=ToolCall(
                    id=tc.get("id", ""),
                    name=func.get("name", ""),
                    input=input_data,
                ),
            ))

        usage_data = data.get("usage", {})
        finish = choice.get("finish_reason", "stop")

        return Response(
            id=data.get("id", ""),
            content=content,
            stop_reason=_STOP_MAP.get(finish, StopReason.END_TURN),
            usage=Usage(
                input_tokens=usage_data.get("prompt_tokens", 0),
                output_tokens=usage_data.get("completion_tokens", 0),
            ),
        )


def _normalize_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Normalize JSON Schema for OpenAI strict mode.

    Ensures all properties appear in 'required' array.
    From openaiShim.ts normalizeSchemaForOpenAI().
    """
    result = dict(schema)
    if "properties" in result and isinstance(result["properties"], dict):
        # Add all property keys to required
        existing_required = set(result.get("required", []))
        all_keys = set(result["properties"].keys())
        result["required"] = sorted(existing_required | all_keys)
    return result


def _openai_factory(cfg: ProviderConfig) -> OpenAIProvider:
    return OpenAIProvider(cfg)


register("openai", _openai_factory)
