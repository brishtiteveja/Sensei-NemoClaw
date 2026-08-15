"""Dream — LLM-powered memory consolidation.

Reads existing memory files + recent conversation, asks the LLM to
consolidate and organize memories, then writes back to CLAWPY.md.

Two modes:
- Manual: /dream command
- AutoDream: triggers after session end if conditions met (time + turns)
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from clawpy.engine.memory import (
    MEMORY_FILENAME,
    MemoryFile,
    discover_all_memory,
    ensure_memory_file,
    get_project_memory_path,
)
from clawpy.provider.base import Provider, Request, StopReason
from clawpy.types import Message, Role, text_message

logger = logging.getLogger(__name__)

# ---- AutoDream gates ----

AUTO_DREAM_MIN_TURNS = 10  # Min turns in session before auto-dream triggers
AUTO_DREAM_MIN_HOURS = 24  # Min hours since last dream
LOCK_FILENAME = ".dream-lock"

_CONSOLIDATION_PROMPT = """\
# Dream: Memory Consolidation

You are performing a **dream** — a reflective pass over memory files and recent conversation.
Your goal is to synthesize what was learned into well-organized, durable memories.

## Current Memory Files

{existing_memories}

## Recent Conversation Summary

{conversation_summary}

## Instructions

1. **Review** the existing memories and recent conversation.
2. **Identify** new facts, decisions, preferences, and project context worth remembering.
3. **Consolidate** — merge new information into the existing memory structure:
   - Update existing entries if they're outdated
   - Add new entries for genuinely new information
   - Remove entries that are contradicted by recent work
   - Convert relative dates to absolute (today is {today})
4. **Organize** — keep memories concise and well-structured:
   - Use markdown headers and bullet points
   - Group related items
   - Keep the total under 200 lines

## Output

Write the COMPLETE updated memory file content. Output ONLY the markdown content,
no explanations or code fences. This will replace the current CLAWPY.md file.
"""


@dataclass(slots=True)
class DreamResult:
    """Result of a dream consolidation."""

    success: bool
    new_content: str = ""
    tokens_used: int = 0
    error: str = ""


async def run_dream(
    provider: Provider,
    model: str,
    work_dir: str,
    messages: list[Message],
    max_tokens: int = 4096,
) -> DreamResult:
    """Run memory consolidation (dream).

    Reads existing memories + recent conversation, asks LLM to consolidate,
    returns the new memory content.
    """
    # Gather existing memories
    memory_files = discover_all_memory(work_dir)
    existing = _format_existing_memories(memory_files)

    # Summarize recent conversation
    summary = _summarize_conversation(messages)

    today = time.strftime("%Y-%m-%d")

    prompt = _CONSOLIDATION_PROMPT.format(
        existing_memories=existing or "(No existing memories)",
        conversation_summary=summary or "(No recent conversation)",
        today=today,
    )

    request = Request(
        model=model,
        system="You are a memory consolidation agent. Output only markdown content.",
        messages=[text_message(Role.USER, prompt)],
        tools=[],
        max_tokens=max_tokens,
    )

    try:
        response = await provider.send(request)
        new_content = ""
        for block in response.content:
            if block.text:
                new_content += block.text

        if not new_content.strip():
            return DreamResult(success=False, error="Dream produced empty content")

        tokens = response.usage.input_tokens + response.usage.output_tokens
        return DreamResult(success=True, new_content=new_content.strip(), tokens_used=tokens)

    except Exception as e:
        logger.error("Dream failed: %s", e)
        return DreamResult(success=False, error=str(e))


async def dream_and_save(
    provider: Provider,
    model: str,
    work_dir: str,
    messages: list[Message],
) -> DreamResult:
    """Run dream and write results to project memory file."""
    result = await run_dream(provider, model, work_dir, messages)
    if not result.success:
        return result

    path = get_project_memory_path(work_dir)
    ensure_memory_file(path)

    # Write the consolidated content
    path.write_text(result.new_content + "\n", encoding="utf-8")

    # Update lock file (tracks last dream time)
    _update_lock(work_dir)

    logger.info("Dream completed: %d tokens, wrote to %s", result.tokens_used, path)
    return result


def _format_existing_memories(files: list[MemoryFile]) -> str:
    """Format existing memory files for the dream prompt."""
    parts: list[str] = []
    for mf in files:
        if not mf.exists or not mf.content.strip():
            continue
        parts.append(f"### {mf.label}: {mf.path.name}\n```\n{mf.content.strip()}\n```")
    return "\n\n".join(parts)


def _summarize_conversation(messages: list[Message], max_messages: int = 30) -> str:
    """Create a text summary of recent conversation for the dream prompt."""
    if not messages:
        return ""

    # Take last N messages
    recent = messages[-max_messages:]
    parts: list[str] = []

    for msg in recent:
        role = msg.role.value.upper()
        text = msg.text_content()
        if text:
            # Truncate long messages
            if len(text) > 500:
                text = text[:500] + "..."
            parts.append(f"**{role}**: {text}")

        # Note tool usage briefly
        for tc in msg.tool_calls():
            parts.append(f"**{role}**: [Used tool: {tc.name}]")

    return "\n\n".join(parts)


# ---- AutoDream gates ----

def should_auto_dream(work_dir: str, turn_count: int) -> bool:
    """Check if auto-dream should trigger.

    Conditions:
    1. Enough turns in this session (>= AUTO_DREAM_MIN_TURNS)
    2. Enough time since last dream (>= AUTO_DREAM_MIN_HOURS)
    """
    if turn_count < AUTO_DREAM_MIN_TURNS:
        return False

    last_dream = _get_last_dream_time(work_dir)
    if last_dream > 0:
        hours_since = (time.time() - last_dream) / 3600
        if hours_since < AUTO_DREAM_MIN_HOURS:
            return False

    return True


def _get_last_dream_time(work_dir: str) -> float:
    """Get the timestamp of the last dream from the lock file."""
    lock = Path(work_dir) / ".clawpy" / LOCK_FILENAME
    if lock.exists():
        try:
            return lock.stat().st_mtime
        except OSError:
            pass
    return 0.0


def _update_lock(work_dir: str) -> None:
    """Update the dream lock file timestamp."""
    lock_dir = Path(work_dir) / ".clawpy"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock = lock_dir / LOCK_FILENAME
    lock.write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ"), encoding="utf-8")
