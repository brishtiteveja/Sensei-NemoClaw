"""Microcompact — clear old tool results to save context tokens.

Triggers at 70% context utilization (before auto-compact at 90%).
Replaces tool result content with "[result cleared]" for messages
older than the last N messages.
"""

from __future__ import annotations

from clawpy.types import ContentBlock, ContentType, Message, ToolResult

MICROCOMPACT_TRIGGER = 0.70  # Trigger at 70% context window
KEEP_RECENT = 6  # Keep last N messages' tool results intact


def should_microcompact(total_tokens: int, context_window: int) -> bool:
    """Check if microcompact should trigger."""
    return total_tokens >= context_window * MICROCOMPACT_TRIGGER


def microcompact(messages: list[Message], keep_recent: int = KEEP_RECENT) -> int:
    """Clear old tool results in-place. Returns count of results cleared."""
    if len(messages) <= keep_recent:
        return 0

    cleared = 0
    old_messages = messages[:-keep_recent]

    for msg in old_messages:
        new_content: list[ContentBlock] = []
        for block in msg.content:
            if (
                block.type == ContentType.TOOL_RESULT
                and block.tool_result
                and len(block.tool_result.content) > 100
            ):
                # Replace with stub
                new_content.append(ContentBlock(
                    type=ContentType.TOOL_RESULT,
                    tool_result=ToolResult(
                        tool_call_id=block.tool_result.tool_call_id,
                        content="[result cleared to save context]",
                        is_error=block.tool_result.is_error,
                    ),
                ))
                cleared += 1
            else:
                new_content.append(block)
        msg.content = new_content

    return cleared
