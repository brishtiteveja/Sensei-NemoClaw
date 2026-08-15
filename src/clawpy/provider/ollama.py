"""Ollama provider — local OpenAI-compatible endpoint.

Ollama runs locally and exposes an OpenAI-compatible API.
No API key required. Auto-discovery of running instance.
"""

from __future__ import annotations

import os

from clawpy.config.config import ProviderConfig
from clawpy.provider.openai import OpenAIProvider
from clawpy.provider.registry import register

_DEFAULT_BASE_URL = "http://localhost:11434/v1"


class OllamaProvider(OpenAIProvider):
    """Ollama local model server via OpenAI-compatible endpoint."""

    def __init__(self, cfg: ProviderConfig) -> None:
        cfg_copy = ProviderConfig(
            api_key=cfg.api_key or "ollama",  # Ollama accepts any key
            base_url=cfg.base_url or os.environ.get("OLLAMA_BASE_URL", _DEFAULT_BASE_URL),
            model=cfg.model,
        )
        super().__init__(cfg_copy)
        self._provider_name = "ollama"

    def models(self) -> list[str]:
        return [
            "llama3.1",
            "llama3.1:70b",
            "codellama",
            "deepseek-coder-v2",
            "qwen2.5-coder",
        ]


def _factory(cfg: ProviderConfig) -> OllamaProvider:
    return OllamaProvider(cfg)


register("ollama", _factory)
