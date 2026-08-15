"""System prompt assembly with CLAWPY.md memory discovery.

Mirrors OpenClaude's multi-section system prompt:
- Static sections (identity, task guidance, tool rules, style)
- Dynamic sections (memory, environment info)
"""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path

from clawpy.config.paths import global_config_dir

_MEMORY_FILENAME = "CLAWPY.md"


def build_system_prompt(work_dir: str, model: str) -> str:
    """Assemble the full system prompt from static + dynamic sections."""
    sections: list[str] = [
        _identity_section(),
        _task_guidance_section(),
        _tool_rules_section(),
        _style_section(),
    ]

    # Dynamic: memory files (using memory module)
    from clawpy.engine.memory import build_memory_content
    memory = build_memory_content(work_dir)
    if memory:
        sections.append(memory)

    # Dynamic: environment info
    sections.append(_environment_section(work_dir, model))

    return "\n\n".join(s for s in sections if s)


def _identity_section() -> str:
    return (
        "You are ClawPy, an interactive AI assistant running in the terminal. "
        "You primarily help with software engineering tasks — reading code, fixing bugs, "
        "adding features, refactoring, and explaining code.\n"
        "You also help with general questions, research, and any task the user asks. "
        "Use the tools available to you to accomplish tasks — including WebFetch for "
        "looking things up on the web, and Bash for running commands.\n"
        "Be concise and direct in your responses. Be helpful, not restrictive."
    )


def _task_guidance_section() -> str:
    return (
        "# Doing tasks\n"
        "- Read existing code before suggesting modifications.\n"
        "- Prefer editing existing files over creating new ones.\n"
        "- Do not add features, refactor, or make improvements beyond what was asked.\n"
        "- Do not add comments, docstrings, or type annotations to code you didn't change.\n"
        "- Be careful not to introduce security vulnerabilities.\n"
        "- When referencing code, include file_path:line_number."
    )


def _tool_rules_section() -> str:
    return (
        "# Using tools\n"
        "- Use the Read tool instead of cat/head/tail.\n"
        "- Use the Edit tool instead of sed/awk.\n"
        "- Use the Write tool instead of echo/cat heredoc.\n"
        "- Use the Grep tool instead of grep/rg.\n"
        "- Use the Glob tool instead of find/ls.\n"
        "- Reserve Bash for commands that require shell execution.\n"
        "- Call multiple tools in parallel when they are independent."
    )


def _style_section() -> str:
    return (
        "# Tone and style\n"
        "- Be concise. Lead with the answer, not the reasoning.\n"
        "- Do not restate what the user said.\n"
        "- If you can say it in one sentence, don't use three."
    )


def _load_memory(work_dir: str) -> str:
    """Discover and load CLAWPY.md memory files.

    Walk from work_dir to filesystem root, then check global config.
    """
    files = discover_memory_files(work_dir)
    if not files:
        return ""

    parts: list[str] = ["# Memory"]
    for path in files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace").strip()
            if content:
                # Label the source
                try:
                    rel = path.relative_to(work_dir)
                    label = str(rel)
                except ValueError:
                    label = str(path)
                parts.append(f"## From {label}\n{content}")
        except OSError:
            continue

    return "\n\n".join(parts) if len(parts) > 1 else ""


def discover_memory_files(work_dir: str) -> list[Path]:
    """Walk from work_dir to root, collect CLAWPY.md files."""
    found: list[Path] = []
    seen: set[str] = set()
    current = Path(work_dir).resolve()

    while True:
        for name in [_MEMORY_FILENAME, f".clawpy/{_MEMORY_FILENAME}"]:
            path = current / name
            resolved = str(path.resolve())
            if resolved not in seen and path.is_file():
                found.append(path)
                seen.add(resolved)
        parent = current.parent
        if parent == current:
            break
        current = parent

    # Global memory
    global_mem = global_config_dir() / _MEMORY_FILENAME
    resolved = str(global_mem.resolve())
    if resolved not in seen and global_mem.is_file():
        found.append(global_mem)

    return found


def _environment_section(work_dir: str, model: str) -> str:
    """Environment information for the model."""
    parts: list[str] = ["# Environment"]
    parts.append(f"- Working directory: {work_dir}")
    parts.append(f"- Platform: {platform.system().lower()}")
    parts.append(f"- Model: {model}")

    # Git context
    git = _get_git_context(work_dir)
    if git:
        parts.append(f"- Is a git repository: true")
        if git.get("branch"):
            parts.append(f"- Git branch: {git['branch']}")
        if git.get("status"):
            parts.append(f"- Git status:\n{git['status']}")
        if git.get("recent_commits"):
            parts.append(f"- Recent commits:\n{git['recent_commits']}")

    return "\n".join(parts)


def _get_git_context(work_dir: str) -> dict[str, str]:
    """Get git context: branch, status summary, recent commits."""
    result: dict[str, str] = {}

    def _run(cmd: list[str]) -> str:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir, timeout=5)
            return r.stdout.strip() if r.returncode == 0 else ""
        except (OSError, subprocess.TimeoutExpired):
            return ""

    # Check if git repo
    if not _run(["git", "rev-parse", "--is-inside-work-tree"]):
        return {}

    result["branch"] = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])

    # Status (short format, limited)
    status = _run(["git", "status", "--short"])
    if status:
        lines = status.splitlines()
        if len(lines) > 20:
            status = "\n".join(lines[:20]) + f"\n... ({len(lines)} files total)"
        result["status"] = status

    # Recent commits (last 5, oneline)
    commits = _run(["git", "log", "--oneline", "-5"])
    if commits:
        result["recent_commits"] = commits

    return result
