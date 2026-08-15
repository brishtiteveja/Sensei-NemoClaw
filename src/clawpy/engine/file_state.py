"""Read-file state tracking for edit/write enforcement.

Mirrors OpenClaude's readFileState cache:
- FileRead registers files in state with mtime + content hash
- FileEdit/FileWrite check state before allowing modifications
- Staleness detection: reject if file modified since last read
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileState:
    """Snapshot of a file at the time it was read."""

    path: str
    mtime: float
    content_hash: str
    line_count: int


class FileStateTracker:
    """Tracks which files have been read, for edit/write enforcement."""

    def __init__(self) -> None:
        self._state: dict[str, FileState] = {}

    def register(self, path: str, content: str) -> FileState:
        """Register a file as read. Called by FileReadTool after reading."""
        resolved = str(Path(path).resolve())
        try:
            mtime = os.path.getmtime(resolved)
        except OSError:
            mtime = 0.0
        state = FileState(
            path=resolved,
            mtime=mtime,
            content_hash=hashlib.sha256(content.encode()).hexdigest(),
            line_count=content.count("\n") + (1 if content and not content.endswith("\n") else 0),
        )
        self._state[resolved] = state
        return state

    def get(self, path: str) -> FileState | None:
        """Get the state of a previously read file."""
        resolved = str(Path(path).resolve())
        return self._state.get(resolved)

    def check_writable(self, path: str) -> str | None:
        """Check if a file can be written/edited.

        Returns None if OK, or an error message if not.
        """
        resolved = str(Path(path).resolve())
        state = self._state.get(resolved)

        # New file (doesn't exist yet) — allow write without prior read
        if not Path(resolved).exists():
            return None

        # Existing file must have been read first
        if state is None:
            return (
                f"File {path} has not been read yet. "
                "Use the Read tool first before editing."
            )

        # Check mtime staleness
        try:
            current_mtime = os.path.getmtime(resolved)
        except OSError:
            return f"Cannot stat file: {path}"

        if current_mtime != state.mtime:
            return (
                f"File {path} has been modified since last read "
                f"(mtime changed from {state.mtime} to {current_mtime}). "
                "Read the file again before editing."
            )

        return None

    def update_after_write(self, path: str, new_content: str) -> None:
        """Update state after a successful write/edit."""
        self.register(path, new_content)

    def clear(self) -> None:
        """Clear all tracked state (e.g., on /clear)."""
        self._state.clear()
