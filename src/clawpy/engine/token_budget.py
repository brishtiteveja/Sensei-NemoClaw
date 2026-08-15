"""Token budget management — prevents context overflow and diminishing returns.

From OpenClaude's query/tokenBudget.ts and claurst spec:
- COMPLETION_THRESHOLD = 0.9 (stop at 90% context window)
- DIMINISHING_THRESHOLD = 500 (stop if <500 new tokens after 3+ loops)
"""

from __future__ import annotations

from dataclasses import dataclass

# Context window sizes per provider/model family
CONTEXT_WINDOWS: dict[str, int] = {
    # Anthropic
    "claude-opus-4": 200_000,
    "claude-sonnet-4": 200_000,
    "claude-haiku-4": 200_000,
    # OpenAI
    "gpt-4o": 128_000,
    "gpt-4o-mini": 128_000,
    "gpt-4-turbo": 128_000,
    "o1": 200_000,
    "o3-mini": 200_000,
    # Gemini
    "gemini-2.5-pro": 1_000_000,
    "gemini-2.5-flash": 1_000_000,
    "gemini-2.0-flash": 1_000_000,
    # DeepSeek
    "deepseek-chat": 64_000,
    "deepseek-coder": 64_000,
    "deepseek-reasoner": 64_000,
    # Default
    "_default": 200_000,
}

COMPLETION_THRESHOLD = 0.9
DIMINISHING_THRESHOLD = 500
MIN_CONTINUATIONS_FOR_DIMINISHING = 3


def get_context_window(model: str) -> int:
    """Get context window size for a model."""
    # Try exact match first, then prefix match
    if model in CONTEXT_WINDOWS:
        return CONTEXT_WINDOWS[model]
    for prefix, size in CONTEXT_WINDOWS.items():
        if prefix != "_default" and model.startswith(prefix):
            return size
    return CONTEXT_WINDOWS["_default"]


@dataclass(slots=True)
class TokenBudget:
    """Tracks token usage to decide when to stop the agentic loop."""

    context_window: int
    continuation_count: int = 0
    last_turn_output: int = 0  # Output tokens from most recent turn only
    total_input_tokens: int = 0
    total_output_tokens: int = 0

    def record_turn(self, input_tokens: int, output_tokens: int) -> None:
        """Record token usage from a completed turn."""
        self.last_turn_output = output_tokens
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.continuation_count += 1

    def should_continue(self, has_tool_calls: bool = False) -> bool:
        """Check if we should continue the agentic loop.

        Returns False when:
        1. Total tokens approach context window (90% threshold)
        2. Diminishing returns detected (< 500 output tokens per turn after 3+ continuations)
           — skipped when the turn produced tool calls, since tool call output is intentionally small
        """
        total = self.total_input_tokens + self.total_output_tokens

        # Context window threshold
        if total >= self.context_window * COMPLETION_THRESHOLD:
            return False

        # Diminishing returns — only after enough continuations, skip for tool-calling turns
        if (not has_tool_calls
                and self.continuation_count >= MIN_CONTINUATIONS_FOR_DIMINISHING
                and self.last_turn_output < DIMINISHING_THRESHOLD):
            return False

        return True

    def tokens_remaining(self) -> int:
        """Estimate remaining tokens before threshold."""
        used = self.total_input_tokens + self.total_output_tokens
        limit = int(self.context_window * COMPLETION_THRESHOLD)
        return max(0, limit - used)
