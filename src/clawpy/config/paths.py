"""Path utilities for ClawPy configuration and data directories."""

from __future__ import annotations

import os
from pathlib import Path


def global_config_dir() -> Path:
    """Return the global config directory (~/.clawpy or XDG_CONFIG_HOME/clawpy)."""
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "clawpy"
    return Path.home() / ".clawpy"


def project_config_dir(work_dir: str = ".") -> Path:
    """Return the project-local config directory."""
    return Path(work_dir) / ".clawpy"


def session_dir() -> Path:
    """Return the directory for session storage."""
    return global_config_dir() / "sessions"
