"""Tests for token budget management."""

from clawpy.engine.token_budget import TokenBudget, get_context_window


def test_context_window_known_models():
    assert get_context_window("gpt-4o") == 128_000
    assert get_context_window("claude-sonnet-4-20250514") == 200_000
    assert get_context_window("gemini-2.5-pro") == 1_000_000
    assert get_context_window("deepseek-chat") == 64_000


def test_context_window_prefix_match():
    assert get_context_window("claude-opus-4-something") == 200_000


def test_context_window_unknown():
    assert get_context_window("unknown-model") == 200_000


def test_budget_fresh():
    b = TokenBudget(context_window=200_000)
    assert b.should_continue()
    assert b.tokens_remaining() == 180_000  # 200K * 0.9


def test_budget_context_threshold():
    b = TokenBudget(context_window=100_000)
    b.record_turn(85_000, 6_000)  # 91K total > 90K threshold
    assert not b.should_continue()


def test_budget_diminishing_returns():
    b = TokenBudget(context_window=200_000)
    # 5 turns with tiny output each time
    for _ in range(5):
        b.record_turn(100, 50)
    # After 3+ continuations with <500 tokens, should stop
    assert not b.should_continue()


def test_budget_no_diminishing_early():
    b = TokenBudget(context_window=200_000)
    # Only 2 turns — not enough for diminishing check
    b.record_turn(100, 50)
    b.record_turn(100, 50)
    assert b.should_continue()


def test_budget_tokens_remaining():
    b = TokenBudget(context_window=100_000)
    b.record_turn(40_000, 10_000)
    # Used 50K, limit is 90K (90%), so 40K remaining
    assert b.tokens_remaining() == 40_000
