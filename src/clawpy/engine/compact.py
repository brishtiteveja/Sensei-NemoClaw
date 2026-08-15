"""Auto-compact — summarize old messages to free context space.

From claurst spec:
- Trigger at 90% context window utilization
- Keep last KEEP_RECENT messages
- Summarize older messages via LLM call
- Circuit breaker: max 3 consecutive failures
"""

from __future__ import annotations

import logging

from clawpy.provider.base import Provider, Request
from clawpy.types import Message, Role, text_message

logger = logging.getLogger(__name__)

KEEP_RECENT_MESSAGES = 10
MAX_CONSECUTIVE_FAILURES = 3
COMPACT_SYSTEM_PROMPT = (
    "You are a conversation summarizer. Summarize the following conversation "
    "history concisely, preserving key decisions, code changes, file paths, "
    "and important context. Do not use tools. Output only the summary text."
)


async def auto_compact(
    messages: list[Message],
    provider: Provider,
    model: str,
) -> list[Message] | None:
    """Compact conversation by summarizing old messages.

    Returns new message list if compact succeeded, None if skipped/failed.
    """
    if len(messages) <= KEEP_RECENT_MESSAGES + 2:
        return None  # Not enough messages to compact

    old_messages = messages[:-KEEP_RECENT_MESSAGES]
    recent_messages = messages[-KEEP_RECENT_MESSAGES:]

    # Build summary request
    summary_text = _format_for_summary(old_messages)
    summary_request = Request(
        model=model,
        system=COMPACT_SYSTEM_PROMPT,
        messages=[text_message(Role.USER, f"Summarize this conversation:\n\n{summary_text}")],
        tools=[],  # No tools during compact
        max_tokens=4096,
    )

    try:
        response = await provider.send(summary_request)
        summary = ""
        for block in response.content:
            if block.text:
                summary += block.text
    except Exception as e:
        logger.warning("Auto-compact failed: %s", e)
        return None

    if not summary:
        return None

    # Replace history with: summary + recent
    compacted = [
        text_message(Role.USER, f"[Conversation summary]\n{summary}"),
        text_message(Role.ASSISTANT, "Understood. I'll continue with this context."),
        *recent_messages,
    ]

    logger.info(
        "Auto-compact: %d messages → %d (summarized %d old messages)",
        len(messages),
        len(compacted),
        len(old_messages),
    )

    return compacted


def _format_for_summary(messages: list[Message]) -> str:
    """Format messages into text for summarization."""
    parts: list[str] = []
    for msg in messages:
        role = msg.role.value.upper()
        text = msg.text_content()
        if text:
            # Truncate very long messages
            if len(text) > 2000:
                text = text[:2000] + "..."
            parts.append(f"{role}: {text}")
        # Note tool calls/results briefly
        for tc in msg.tool_calls():
            parts.append(f"{role}: [Called tool {tc.name}]")
        for tr in msg.tool_results():
            status = "error" if tr.is_error else "success"
            parts.append(f"{role}: [Tool result: {status}]")
    return "\n".join(parts)
