"""Session persistence — JSONL transcript storage.

Each session is a JSONL file at ~/.clawpy/sessions/<session_id>.jsonl.
History (for /resume) is at ~/.clawpy/history.jsonl (max 100 entries).
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from clawpy.config.paths import global_config_dir, session_dir
from clawpy.types import ContentBlock, ContentType, Message, Role, ToolCall, ToolResult


def generate_session_id() -> str:
    return uuid.uuid4().hex[:12]


@dataclass(frozen=True, slots=True)
class SessionMeta:
    session_id: str
    created_at: float
    model: str
    work_dir: str
    title: str = ""


class SessionStore:
    """Persists conversation messages as JSONL."""

    def __init__(self, session_id: str | None = None) -> None:
        self.session_id = session_id or generate_session_id()
        self._dir = session_dir()
        self._dir.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self._dir / f"{self.session_id}.jsonl"

    def save_meta(self, model: str, work_dir: str) -> None:
        """Write session metadata as the first line."""
        self._append({
            "type": "session_meta",
            "session_id": self.session_id,
            "created_at": time.time(),
            "model": model,
            "work_dir": work_dir,
        })

    def save_message(self, message: Message) -> None:
        """Append a message to the session transcript."""
        content: list[dict[str, Any]] = []
        for block in message.content:
            entry: dict[str, Any] = {"type": block.type.value}
            if block.type == ContentType.TEXT:
                entry["text"] = block.text
            elif block.type == ContentType.TOOL_CALL and block.tool_call:
                entry["id"] = block.tool_call.id
                entry["name"] = block.tool_call.name
                entry["input"] = block.tool_call.input
            elif block.type == ContentType.TOOL_RESULT and block.tool_result:
                entry["tool_call_id"] = block.tool_result.tool_call_id
                entry["content"] = block.tool_result.content
                entry["is_error"] = block.tool_result.is_error
            elif block.type == ContentType.THINKING:
                entry["thinking"] = block.thinking
            content.append(entry)

        self._append({
            "type": "message",
            "role": message.role.value,
            "content": content,
        })

    def save_compact(self, summary: str, removed_count: int) -> None:
        """Record a compaction event."""
        self._append({
            "type": "compact",
            "summary": summary,
            "removed_count": removed_count,
            "timestamp": time.time(),
        })

    def load_session(self) -> list[Message]:
        """Load all messages from a session file."""
        if not self.path.exists():
            return []

        messages: list[Message] = []
        for line in self.path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if data.get("type") != "message":
                continue
            msg = _deserialize_message(data)
            if msg:
                messages.append(msg)
        return messages

    def _append(self, data: dict[str, Any]) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, separators=(",", ":")) + "\n")

    # ---- History management ----

    @staticmethod
    def list_sessions() -> list[SessionMeta]:
        """List recent sessions from history file."""
        history_path = global_config_dir() / "history.jsonl"
        if not history_path.exists():
            return []

        sessions: list[SessionMeta] = []
        for line in history_path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                sessions.append(SessionMeta(
                    session_id=data["session_id"],
                    created_at=data.get("created_at", 0),
                    model=data.get("model", ""),
                    work_dir=data.get("work_dir", ""),
                    title=data.get("title", ""),
                ))
            except (json.JSONDecodeError, KeyError):
                continue

        return sessions[-100:]  # Last 100

    @staticmethod
    def save_to_history(meta: SessionMeta) -> None:
        """Append session to history file."""
        history_path = global_config_dir() / "history.jsonl"
        history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(history_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "session_id": meta.session_id,
                "created_at": meta.created_at,
                "model": meta.model,
                "work_dir": meta.work_dir,
                "title": meta.title,
            }, separators=(",", ":")) + "\n")


def _deserialize_message(data: dict[str, Any]) -> Message | None:
    """Deserialize a message from JSONL."""
    try:
        role = Role(data["role"])
    except (ValueError, KeyError):
        return None

    blocks: list[ContentBlock] = []
    for block_data in data.get("content", []):
        block_type = block_data.get("type", "")
        if block_type == "text":
            blocks.append(ContentBlock(type=ContentType.TEXT, text=block_data.get("text", "")))
        elif block_type == "tool_call":
            blocks.append(ContentBlock(
                type=ContentType.TOOL_CALL,
                tool_call=ToolCall(
                    id=block_data.get("id", ""),
                    name=block_data.get("name", ""),
                    input=block_data.get("input", {}),
                ),
            ))
        elif block_type == "tool_result":
            blocks.append(ContentBlock(
                type=ContentType.TOOL_RESULT,
                tool_result=ToolResult(
                    tool_call_id=block_data.get("tool_call_id", ""),
                    content=block_data.get("content", ""),
                    is_error=block_data.get("is_error", False),
                ),
            ))
        elif block_type == "thinking":
            blocks.append(ContentBlock(
                type=ContentType.THINKING,
                thinking=block_data.get("thinking", ""),
            ))

    return Message(role=role, content=blocks)
