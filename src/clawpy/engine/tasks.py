"""Task registry — tracks running, completed, and background agents.

Each sub-agent runs as an asyncio Task with isolated Engine state.
Tasks can be foregrounded, backgrounded, viewed, and killed.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from clawpy.types import Message


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"


@dataclass(slots=True)
class TaskState:
    """State of a running or completed task."""

    task_id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    is_background: bool = False
    started_at: float = 0.0
    finished_at: float = 0.0
    messages: list[Message] = field(default_factory=list)
    output: str = ""
    error: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: int = 0
    log: list[str] = field(default_factory=list)  # Live activity log
    _asyncio_task: asyncio.Task[Any] | None = field(default=None, repr=False)

    @property
    def elapsed(self) -> float:
        end = self.finished_at or time.time()
        return end - self.started_at if self.started_at else 0.0

    @property
    def is_done(self) -> bool:
        return self.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.KILLED)


_counter = 0


def _next_id(prefix: str = "a") -> str:
    global _counter
    _counter += 1
    return f"{prefix}{_counter:04d}"


class TaskRegistry:
    """Registry of all running and completed tasks."""

    def __init__(self) -> None:
        self._tasks: dict[str, TaskState] = {}
        self._foreground_id: str | None = None
        self._on_update: Callable[[], None] | None = None

    def set_on_update(self, callback: Callable[[], None]) -> None:
        """Set callback for task state changes (for UI refresh)."""
        self._on_update = callback

    def _notify(self) -> None:
        if self._on_update:
            self._on_update()

    def create(self, description: str, background: bool = False) -> TaskState:
        """Create a new task entry."""
        task = TaskState(
            task_id=_next_id(),
            description=description,
            status=TaskStatus.PENDING,
            is_background=background,
            started_at=time.time(),
        )
        self._tasks[task.task_id] = task
        if not background and self._foreground_id is None:
            self._foreground_id = task.task_id
        self._notify()
        return task

    def get(self, task_id: str) -> TaskState | None:
        return self._tasks.get(task_id)

    def list_all(self) -> list[TaskState]:
        return list(self._tasks.values())

    def list_running(self) -> list[TaskState]:
        return [t for t in self._tasks.values() if t.status == TaskStatus.RUNNING]

    def list_background(self) -> list[TaskState]:
        return [t for t in self._tasks.values() if t.is_background and not t.is_done]

    @property
    def foreground_id(self) -> str | None:
        return self._foreground_id

    def background(self, task_id: str) -> None:
        """Send a task to background."""
        task = self._tasks.get(task_id)
        if task:
            task.is_background = True
            if self._foreground_id == task_id:
                self._foreground_id = None
            self._notify()

    def foreground(self, task_id: str) -> None:
        """Bring a task to foreground."""
        task = self._tasks.get(task_id)
        if task and not task.is_done:
            task.is_background = False
            self._foreground_id = task_id
            self._notify()

    def complete(self, task_id: str, output: str = "") -> None:
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.finished_at = time.time()
            task.output = output
            if self._foreground_id == task_id:
                self._foreground_id = None
            self._notify()

    def fail(self, task_id: str, error: str) -> None:
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.finished_at = time.time()
            task.error = error
            if self._foreground_id == task_id:
                self._foreground_id = None
            self._notify()

    def kill(self, task_id: str) -> bool:
        """Kill a running task."""
        task = self._tasks.get(task_id)
        if not task or task.is_done:
            return False
        task.status = TaskStatus.KILLED
        task.finished_at = time.time()
        if task._asyncio_task and not task._asyncio_task.done():
            task._asyncio_task.cancel()
        if self._foreground_id == task_id:
            self._foreground_id = None
        self._notify()
        return True

    def clear_completed(self) -> int:
        """Remove completed/failed/killed tasks. Returns count removed."""
        to_remove = [tid for tid, t in self._tasks.items() if t.is_done]
        for tid in to_remove:
            del self._tasks[tid]
        return len(to_remove)
