"""Gemini provider via OpenAI-compatible endpoint.

Google Gemini supports an OpenAI-compatible Chat Completions endpoint.
Same conversion logic, different base URL and API key.
"""

from __future__ import annotations

import os

from clawpy.config.config import ProviderConfig
from clawpy.provider.openai import OpenAIProvider
from clawpy.provider.registry import register

_DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"


class GeminiProvider(OpenAIProvider):
    """Google Gemini via OpenAI-compatible endpoint."""

    def __init__(self, cfg: ProviderConfig) -> None:
        cfg_copy = ProviderConfig(
            api_key=cfg.api_key or os.environ.get("GEMINI_API_KEY", ""),
            base_url=cfg.base_url or os.environ.get("GEMINI_BASE_URL", _DEFAULT_BASE_URL),
            model=cfg.model,
        )
        super().__init__(cfg_copy)
        self._provider_name = "gemini"

    def models(self) -> list[str]:
        return [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ]


def _factory(cfg: ProviderConfig) -> GeminiProvider:
    return GeminiProvider(cfg)


register("gemini", _factory)
