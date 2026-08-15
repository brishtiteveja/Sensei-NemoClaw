"""Tests for configuration loading."""

import json
import os
from pathlib import Path

from clawpy.config.config import Config, detect_provider


def test_config_defaults():
    cfg = Config()
    assert cfg.provider == "anthropic"
    assert cfg.model == "claude-opus-4-6"
    assert cfg.max_tokens == 8192
    assert cfg.permission_mode == "default"


def test_config_load(tmp_path: Path):
    cfg = Config.load(str(tmp_path))
    assert cfg.work_dir == str(tmp_path)
    assert cfg.provider == "anthropic"


def test_config_merge_global(tmp_path: Path, monkeypatch):
    # Create global settings
    global_dir = tmp_path / "global"
    global_dir.mkdir()
    (global_dir / "settings.json").write_text(json.dumps({"model": "custom-model"}))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    # Trick: create a clawpy subdir
    clawpy_dir = tmp_path / "clawpy"
    clawpy_dir.mkdir()
    (clawpy_dir / "settings.json").write_text(json.dumps({"model": "custom-model"}))

    cfg = Config.load(str(tmp_path))
    assert cfg.model == "custom-model"


def test_config_env_override(monkeypatch):
    monkeypatch.setenv("CLAWPY_PROVIDER", "openai")
    monkeypatch.setenv("CLAWPY_MODEL", "gpt-4o")
    cfg = Config.load(".")
    assert cfg.provider == "openai"
    assert cfg.model == "gpt-4o"


def test_detect_provider_explicit(monkeypatch):
    monkeypatch.setenv("CLAWPY_PROVIDER", "gemini")
    assert detect_provider() == "gemini"


def test_detect_provider_from_api_key(monkeypatch):
    monkeypatch.delenv("CLAWPY_PROVIDER", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_USE_OPENAI", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_USE_GEMINI", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    assert detect_provider() == "openai"


def test_detect_provider_default(monkeypatch):
    for key in ["CLAWPY_PROVIDER", "CLAUDE_CODE_USE_OPENAI", "CLAUDE_CODE_USE_GEMINI",
                 "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"]:
        monkeypatch.delenv(key, raising=False)
    assert detect_provider() == "anthropic"


def test_provider_config():
    cfg = Config(provider="openai", api_key="sk-test", base_url="http://local")
    pc = cfg.provider_config()
    assert pc.api_key == "sk-test"
    assert pc.base_url == "http://local"
