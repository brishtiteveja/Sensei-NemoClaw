"""Memory file management — discover, read, edit, append CLAWPY.md files.

Memory files provide persistent context injected into the system prompt.
Discovery walks from CWD to root, plus global ~/.clawpy/CLAWPY.md.
"""

from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from clawpy.config.paths import global_config_dir

MEMORY_FILENAME = "CLAWPY.md"


class MemoryType(str, Enum):
    GLOBAL = "global"
    PROJECT = "project"
    PROJECT_LOCAL = "project_local"
    PARENT = "parent"


@dataclass(slots=True)
class MemoryFile:
    """A discovered memory file."""

    path: Path
    memory_type: MemoryType
    exists: bool
    content: str = ""
    line_count: int = 0

    @property
    def label(self) -> str:
        match self.memory_type:
            case MemoryType.GLOBAL:
                return "Global"
            case MemoryType.PROJECT:
                return "Project"
            case MemoryType.PROJECT_LOCAL:
                return "Project (local)"
            case MemoryType.PARENT:
                return "Parent"

    @property
    def preview(self) -> str:
        """First 3 lines as preview."""
        if not self.content:
            return ""
        lines = self.content.strip().splitlines()[:3]
        return "\n".join(lines)


def discover_all_memory(work_dir: str, include_missing: bool = True) -> list[MemoryFile]:
    """Discover all memory files from CWD to root + global.

    Returns files in display order (project first, then parents, then global).
    Parent files only included if they exist (to avoid noise), unless include_missing
    forces showing project + project_local + global even when missing.
    """
    found: list[MemoryFile] = []
    seen: set[str] = set()
    current = Path(work_dir).resolve()
    is_first = True

    while True:
        for name, mem_type in [
            (MEMORY_FILENAME, MemoryType.PROJECT if is_first else MemoryType.PARENT),
            (f".clawpy/{MEMORY_FILENAME}", MemoryType.PROJECT_LOCAL if is_first else MemoryType.PARENT),
        ]:
            path = current / name
            resolved = str(path.resolve())
            if resolved in seen:
                continue
            seen.add(resolved)

            exists = path.is_file()
            content = ""
            if exists:
                try:
                    content = path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    pass

            # Only show parent files if they exist (avoid listing 10+ empty dirs)
            if not is_first and not exists:
                continue

            # Always show project + project_local (even if missing) for discoverability
            found.append(MemoryFile(
                path=path,
                memory_type=mem_type,
                exists=exists,
                content=content,
                line_count=content.count("\n") + 1 if content else 0,
            ))

        parent = current.parent
        if parent == current:
            break
        current = parent
        is_first = False

    # Global memory
    global_path = global_config_dir() / MEMORY_FILENAME
    resolved = str(global_path.resolve())
    if resolved not in seen:
        exists = global_path.is_file()
        content = ""
        if exists:
            try:
                content = global_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
        found.append(MemoryFile(
            path=global_path,
            memory_type=MemoryType.GLOBAL,
            exists=exists,
            content=content,
            line_count=content.count("\n") + 1 if content else 0,
        ))

    return found


def get_project_memory_path(work_dir: str) -> Path:
    """Get the default project memory file path."""
    return Path(work_dir).resolve() / MEMORY_FILENAME


def ensure_memory_file(path: Path, template: str = "") -> None:
    """Create a memory file if it doesn't exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        default = template or f"# {MEMORY_FILENAME}\n\n"
        path.write_text(default, encoding="utf-8")


def append_to_memory(path: Path, text: str) -> None:
    """Append a note to a memory file, creating it if needed."""
    ensure_memory_file(path)
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n- {text}  <!-- added {timestamp} -->\n")


def edit_in_editor(path: Path) -> bool:
    """Open a memory file in the user's editor.

    Uses $VISUAL → $EDITOR → nano fallback.
    Returns True if editor was launched successfully.
    """
    ensure_memory_file(path)
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR") or "nano"

    try:
        result = subprocess.run([editor, str(path)])
        return result.returncode == 0
    except FileNotFoundError:
        # Try vi as last resort
        try:
            result = subprocess.run(["vi", str(path)])
            return result.returncode == 0
        except FileNotFoundError:
            return False


def build_memory_content(work_dir: str) -> str:
    """Build the memory section for the system prompt from all discovered files."""
    files = discover_all_memory(work_dir)
    active = [f for f in files if f.exists and f.content.strip()]

    if not active:
        return ""

    parts: list[str] = ["# Memory"]
    for mf in active:
        try:
            rel = mf.path.relative_to(work_dir)
            label = str(rel)
        except ValueError:
            label = str(mf.path)
        parts.append(f"## From {label} ({mf.label})\n{mf.content.strip()}")

    return "\n\n".join(parts)
