"""Tests for file state tracking."""

import os
import time
from pathlib import Path

from clawpy.engine.file_state import FileStateTracker


def test_register_and_get(tmp_path: Path):
    tracker = FileStateTracker()
    test_file = tmp_path / "test.py"
    test_file.write_text("hello\n")

    state = tracker.register(str(test_file), "hello\n")
    assert state.path == str(test_file.resolve())
    assert state.line_count == 1

    got = tracker.get(str(test_file))
    assert got is not None
    assert got.content_hash == state.content_hash


def test_check_writable_new_file(tmp_path: Path):
    tracker = FileStateTracker()
    new_file = tmp_path / "new.py"
    # New file (doesn't exist) should be writable without prior read
    assert tracker.check_writable(str(new_file)) is None


def test_check_writable_existing_not_read(tmp_path: Path):
    tracker = FileStateTracker()
    existing = tmp_path / "existing.py"
    existing.write_text("content")
    # Existing file not read → should be rejected
    result = tracker.check_writable(str(existing))
    assert result is not None
    assert "not been read" in result


def test_check_writable_after_read(tmp_path: Path):
    tracker = FileStateTracker()
    f = tmp_path / "test.py"
    f.write_text("content")
    tracker.register(str(f), "content")
    # Should be writable after read
    assert tracker.check_writable(str(f)) is None


def test_check_writable_stale(tmp_path: Path):
    tracker = FileStateTracker()
    f = tmp_path / "test.py"
    f.write_text("original")
    tracker.register(str(f), "original")

    # Modify file externally (change mtime)
    time.sleep(0.05)
    f.write_text("modified")

    result = tracker.check_writable(str(f))
    assert result is not None
    assert "modified since" in result


def test_update_after_write(tmp_path: Path):
    tracker = FileStateTracker()
    f = tmp_path / "test.py"
    f.write_text("v1")
    tracker.register(str(f), "v1")

    # Simulate write
    f.write_text("v2")
    tracker.update_after_write(str(f), "v2")

    # Should be writable (state updated)
    assert tracker.check_writable(str(f)) is None


def test_clear():
    tracker = FileStateTracker()
    tracker.register("/tmp/fake", "content")
    assert tracker.get("/tmp/fake") is not None
    tracker.clear()
    assert tracker.get("/tmp/fake") is None
