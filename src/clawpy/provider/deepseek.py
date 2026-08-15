"""DeepSeek provider — OpenAI-compatible with reasoning support.

DeepSeek's API is OpenAI-compatible. DeepSeek-R1 includes reasoning tokens
which can be mapped to thinking blocks.
"""

from __future__ import annotations

import os

from clawpy.config.config import ProviderConfig
from clawpy.provider.openai import OpenAIProvider
from clawpy.provider.registry import register

_DEFAULT_BASE_URL = "https://api.deepseek.com/v1"


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek via OpenAI-compatible endpoint."""

    def __init__(self, cfg: ProviderConfig) -> None:
        cfg_copy = ProviderConfig(
            api_key=cfg.api_key or os.environ.get("DEEPSEEK_API_KEY", ""),
            base_url=cfg.base_url or os.environ.get("DEEPSEEK_BASE_URL", _DEFAULT_BASE_URL),
            model=cfg.model,
        )
        super().__init__(cfg_copy)
        self._provider_name = "deepseek"

    def models(self) -> list[str]:
        return [
            "deepseek-chat",
            "deepseek-coder",
            "deepseek-reasoner",
        ]


def _factory(cfg: ProviderConfig) -> DeepSeekProvider:
    return DeepSeekProvider(cfg)


register("deepseek", _factory)
