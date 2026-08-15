"""Fetch Claude subscription usage/rate limits.

Calls the /api/oauth/usage endpoint with OAuth Bearer token.
Returns utilization percentages and reset times for each limit window.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx

from clawpy.auth.oauth import load_tokens, refresh_tokens

_USAGE_URL = "https://api.anthropic.com/api/oauth/usage"


@dataclass(slots=True)
class LimitWindow:
    """A single rate limit window (e.g., 5-hour session, 7-day weekly)."""

    label: str
    utilization: float  # 0-100 percentage
    resets_at: str  # ISO 8601 timestamp
    available: bool = True

    @property
    def resets_in(self) -> str:
        """Human-readable time until reset."""
        try:
            reset_dt = datetime.fromisoformat(self.resets_at.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            delta = reset_dt - now
            total_sec = max(0, int(delta.total_seconds()))
            if total_sec < 60:
                return f"{total_sec}s"
            if total_sec < 3600:
                return f"{total_sec // 60}m"
            hours = total_sec // 3600
            mins = (total_sec % 3600) // 60
            return f"{hours}h {mins}m"
        except Exception:
            return self.resets_at


@dataclass(slots=True)
class ExtraUsage:
    """Extra usage (overage) info for Pro/Max subscribers."""

    enabled: bool = False
    monthly_limit: float | None = None  # In dollars
    used_credits: float | None = None
    utilization: float | None = None  # 0-100


@dataclass(slots=True)
class UsageInfo:
    """Complete usage information."""

    windows: list[LimitWindow]
    extra: ExtraUsage | None = None
    error: str = ""


async def fetch_usage() -> UsageInfo:
    """Fetch usage from the Claude API."""
    tokens = load_tokens()
    if not tokens:
        return UsageInfo(windows=[], error="Not logged in. Use /login first.")

    if tokens.is_expired and tokens.refresh_token:
        try:
            tokens = await refresh_tokens(tokens)
        except Exception as e:
            return UsageInfo(windows=[], error=f"Token refresh failed: {e}")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                _USAGE_URL,
                headers={
                    "Authorization": f"Bearer {tokens.access_token}",
                    "anthropic-beta": "oauth-2025-04-20",
                },
            )
            if resp.status_code != 200:
                return UsageInfo(
                    windows=[],
                    error=f"API returned {resp.status_code}: {resp.text[:200]}",
                )
            data = resp.json()
    except httpx.HTTPError as e:
        return UsageInfo(windows=[], error=f"Request failed: {e}")

    return _parse_usage(data)


def _parse_usage(data: dict[str, Any]) -> UsageInfo:
    """Parse the /api/oauth/usage response."""
    windows: list[LimitWindow] = []

    # 5-hour session limit
    if five := data.get("five_hour"):
        windows.append(LimitWindow(
            label="Session (5h)",
            utilization=five.get("utilization", 0),
            resets_at=five.get("resets_at", ""),
        ))

    # 7-day all models
    if seven := data.get("seven_day"):
        windows.append(LimitWindow(
            label="Weekly (all models)",
            utilization=seven.get("utilization", 0),
            resets_at=seven.get("resets_at", ""),
        ))

    # 7-day opus specific
    if opus := data.get("seven_day_opus"):
        windows.append(LimitWindow(
            label="Weekly (Opus)",
            utilization=opus.get("utilization", 0),
            resets_at=opus.get("resets_at", ""),
        ))

    # 7-day sonnet specific
    if sonnet := data.get("seven_day_sonnet"):
        windows.append(LimitWindow(
            label="Weekly (Sonnet)",
            utilization=sonnet.get("utilization", 0),
            resets_at=sonnet.get("resets_at", ""),
        ))

    # 7-day oauth apps
    if oauth := data.get("seven_day_oauth_apps"):
        windows.append(LimitWindow(
            label="Weekly (OAuth apps)",
            utilization=oauth.get("utilization", 0),
            resets_at=oauth.get("resets_at", ""),
        ))

    # Extra usage
    extra = None
    if ex := data.get("extra_usage"):
        extra = ExtraUsage(
            enabled=ex.get("is_enabled", False),
            monthly_limit=ex.get("monthly_limit"),
            used_credits=ex.get("used_credits"),
            utilization=ex.get("utilization"),
        )

    return UsageInfo(windows=windows, extra=extra)
