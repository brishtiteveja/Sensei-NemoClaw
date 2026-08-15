"""Cost tracking — estimate session cost from token usage.

Per-model pricing in $/million tokens (input/output).
"""

from __future__ import annotations

# Pricing: (input_per_mtok, output_per_mtok) in USD
_PRICING: dict[str, tuple[float, float]] = {
    # Anthropic
    "claude-opus-4": (15.0, 75.0),
    "claude-sonnet-4": (3.0, 15.0),
    "claude-haiku-4": (0.80, 4.0),
    # OpenAI
    "gpt-4o": (2.50, 10.0),
    "gpt-4o-mini": (0.15, 0.60),
    "o1": (15.0, 60.0),
    "o3-mini": (1.10, 4.40),
    # Gemini
    "gemini-2.5-pro": (1.25, 10.0),
    "gemini-2.5-flash": (0.15, 0.60),
    "gemini-2.0-flash": (0.10, 0.40),
    # DeepSeek
    "deepseek-chat": (0.27, 1.10),
    "deepseek-reasoner": (0.55, 2.19),
    # Ollama (free / local)
    "_ollama": (0.0, 0.0),
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost in USD for given token usage."""
    # Try exact match, then prefix match
    pricing = _PRICING.get(model)
    if not pricing:
        for prefix, p in _PRICING.items():
            if prefix != "_ollama" and model.startswith(prefix):
                pricing = p
                break
    if not pricing:
        if "ollama" in model.lower():
            return 0.0
        pricing = (3.0, 15.0)  # Default to Sonnet pricing

    input_cost = (input_tokens / 1_000_000) * pricing[0]
    output_cost = (output_tokens / 1_000_000) * pricing[1]
    return input_cost + output_cost


def format_cost(cost: float) -> str:
    """Format cost for display."""
    if cost < 0.001:
        return "<$0.001"
    if cost < 0.01:
        return f"${cost:.4f}"
    if cost < 1.0:
        return f"${cost:.3f}"
    return f"${cost:.2f}"
