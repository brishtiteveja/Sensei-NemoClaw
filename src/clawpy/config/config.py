"""Configuration loading with layered merge.

Priority: defaults < global settings < project settings < env vars < CLI flags.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from clawpy.config.paths import global_config_dir, project_config_dir


@dataclass(slots=True)
class ProviderConfig:
    """Configuration for a specific provider instance."""

    api_key: str = ""
    base_url: str = ""
    model: str = ""
    extra: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class Config:
    """Application configuration."""

    # Provider
    provider: str = "anthropic"
    model: str = "claude-opus-4-6"
    api_key: str = ""
    base_url: str = ""

    # Behavior
    max_tokens: int = 8192
    permission_mode: str = "default"
    work_dir: str = "."

    # Rules
    allow_tools: list[str] = field(default_factory=list)
    deny_tools: list[str] = field(default_factory=list)

    # Computed paths (not persisted)
    global_dir: Path = field(default_factory=global_config_dir)
    project_dir: Path = field(default_factory=lambda: Path(".clawpy"))

    @classmethod
    def load(cls, work_dir: str = ".") -> Config:
        """Load configuration with layered merge."""
        cfg = cls()
        cfg.work_dir = os.path.abspath(work_dir)
        cfg.global_dir = global_config_dir()
        cfg.project_dir = project_config_dir(cfg.work_dir)

        # Layer 1: global settings
        global_settings = cfg.global_dir / "settings.json"
        if global_settings.exists():
            _merge_json(cfg, global_settings)

        # Layer 2: project settings
        project_settings = cfg.project_dir / "settings.json"
        if project_settings.exists():
            _merge_json(cfg, project_settings)

        # Layer 3: environment variables
        _merge_env(cfg)

        return cfg

    def provider_config(self) -> ProviderConfig:
        """Build ProviderConfig from resolved settings."""
        api_key = self.api_key
        base_url = self.base_url

        # Provider-specific env var fallbacks
        match self.provider:
            case "anthropic":
                api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
            case "openai":
                api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
                base_url = base_url or os.environ.get("OPENAI_BASE_URL", "")
            case "gemini":
                api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
                base_url = base_url or os.environ.get(
                    "GEMINI_BASE_URL",
                    "https://generativelanguage.googleapis.com/v1beta/openai",
                )
            case "ollama":
                base_url = base_url or os.environ.get(
                    "OLLAMA_BASE_URL", "http://localhost:11434/v1"
                )
            case "deepseek":
                api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
                base_url = base_url or "https://api.deepseek.com/v1"

        return ProviderConfig(
            api_key=api_key,
            base_url=base_url,
            model=self.model,
        )


def detect_provider() -> str:
    """Auto-detect provider from environment variables.

    Priority mirrors OpenClaude's client.ts:
    1. CLAWPY_PROVIDER (explicit)
    2. CLAUDE_CODE_USE_OPENAI=1
    3. CLAUDE_CODE_USE_GEMINI=1
    4. ANTHROPIC_API_KEY set → anthropic
    5. OPENAI_API_KEY set → openai
    6. GEMINI_API_KEY set → gemini
    7. Default: anthropic
    """
    explicit = os.environ.get("CLAWPY_PROVIDER", "").lower()
    if explicit:
        return explicit

    if os.environ.get("CLAUDE_CODE_USE_OPENAI") == "1":
        return "openai"
    if os.environ.get("CLAUDE_CODE_USE_GEMINI") == "1":
        return "gemini"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    return "anthropic"


def _merge_json(cfg: Config, path: Path) -> None:
    """Merge a JSON settings file into the config."""
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return

    if not isinstance(data, dict):
        return

    for key in ("provider", "model", "api_key", "base_url", "permission_mode"):
        if key in data and isinstance(data[key], str):
            setattr(cfg, key, data[key])

    if "max_tokens" in data and isinstance(data["max_tokens"], int):
        cfg.max_tokens = data["max_tokens"]

    for key in ("allow_tools", "deny_tools"):
        if key in data and isinstance(data[key], list):
            setattr(cfg, key, data[key])


def _merge_env(cfg: Config) -> None:
    """Merge environment variables into the config."""
    if v := os.environ.get("CLAWPY_PROVIDER"):
        cfg.provider = v
    if v := os.environ.get("CLAWPY_MODEL"):
        cfg.model = v
    if v := os.environ.get("CLAWPY_MAX_TOKENS"):
        try:
            cfg.max_tokens = int(v)
        except ValueError:
            pass
    if v := os.environ.get("CLAWPY_PERMISSION_MODE"):
        cfg.permission_mode = v

    # Auto-detect provider if not explicitly set
    if not os.environ.get("CLAWPY_PROVIDER") and cfg.provider == "anthropic":
        detected = detect_provider()
        if detected != "anthropic":
            cfg.provider = detected
