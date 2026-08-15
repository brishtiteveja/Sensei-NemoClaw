"""Plugin manager — install, remove, list, enable/disable plugins.

Supports:
- GitHub repos (git clone)
- Local directories (symlink)
- Plugin registry at ~/.clawpy/plugins/
"""

from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from clawpy.config.paths import global_config_dir
from clawpy.plugins.loader import load_plugin
from clawpy.plugins.types import LoadedPlugin, PluginManifest


def _plugins_dir() -> Path:
    return global_config_dir() / "plugins"


def _cache_dir() -> Path:
    return _plugins_dir() / "cache"


def _installed_file() -> Path:
    return _plugins_dir() / "installed.json"


@dataclass(slots=True)
class InstalledEntry:
    name: str
    source: str  # "github:owner/repo", "local:/path"
    install_path: str
    enabled: bool = True
    version: str = ""
    installed_at: str = ""


class PluginManager:
    """Manages plugin installation, loading, and lifecycle."""

    def __init__(self) -> None:
        self._installed: dict[str, InstalledEntry] = {}
        self._loaded: dict[str, LoadedPlugin] = {}
        self._load_installed_registry()

    def _load_installed_registry(self) -> None:
        """Load installed.json registry."""
        path = _installed_file()
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text())
            for name, entry in data.get("plugins", {}).items():
                self._installed[name] = InstalledEntry(
                    name=name,
                    source=entry.get("source", ""),
                    install_path=entry.get("install_path", ""),
                    enabled=entry.get("enabled", True),
                    version=entry.get("version", ""),
                    installed_at=entry.get("installed_at", ""),
                )
        except (json.JSONDecodeError, KeyError):
            pass

    def _save_installed_registry(self) -> None:
        """Save installed.json registry."""
        path = _installed_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": 1,
            "plugins": {
                name: {
                    "source": e.source,
                    "install_path": e.install_path,
                    "enabled": e.enabled,
                    "version": e.version,
                    "installed_at": e.installed_at,
                }
                for name, e in self._installed.items()
            },
        }
        path.write_text(json.dumps(data, indent=2))

    # ---- Install ----

    def install_from_github(self, repo: str, ref: str = "") -> LoadedPlugin:
        """Install a plugin from a GitHub repo (owner/repo format)."""
        if "/" not in repo:
            raise ValueError(f"Invalid repo format: {repo!r}. Use owner/repo.")

        cache = _cache_dir()
        cache.mkdir(parents=True, exist_ok=True)

        # Derive plugin name from repo
        plugin_name = repo.split("/")[-1]
        dest = cache / plugin_name

        # Remove old version
        if dest.exists():
            shutil.rmtree(dest)

        # Git clone
        url = f"https://github.com/{repo}.git"
        cmd = ["git", "clone", "--depth", "1"]
        if ref:
            cmd.extend(["--branch", ref])
        cmd.extend([url, str(dest)])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(f"git clone failed: {result.stderr.strip()}")

        # Remove .git
        git_dir = dest / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)

        # Load and register
        plugin = load_plugin(dest, source=f"github:{repo}")

        import time
        self._installed[plugin.name] = InstalledEntry(
            name=plugin.name,
            source=f"github:{repo}",
            install_path=str(dest),
            enabled=True,
            version=plugin.manifest.version,
            installed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self._save_installed_registry()
        self._loaded[plugin.name] = plugin
        return plugin

    def install_from_local(self, path: str) -> LoadedPlugin:
        """Install a plugin from a local directory (creates symlink)."""
        source_path = Path(path).resolve()
        if not source_path.is_dir():
            raise ValueError(f"Not a directory: {path}")

        plugin = load_plugin(source_path, source=f"local:{source_path}")

        cache = _cache_dir()
        cache.mkdir(parents=True, exist_ok=True)
        link = cache / plugin.name
        if link.exists():
            link.unlink() if link.is_symlink() else shutil.rmtree(link)
        link.symlink_to(source_path)

        import time
        self._installed[plugin.name] = InstalledEntry(
            name=plugin.name,
            source=f"local:{source_path}",
            install_path=str(link),
            enabled=True,
            version=plugin.manifest.version,
            installed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self._save_installed_registry()
        self._loaded[plugin.name] = plugin
        return plugin

    # ---- Remove ----

    def remove(self, name: str) -> bool:
        """Remove an installed plugin."""
        if name not in self._installed:
            return False

        entry = self._installed[name]
        dest = Path(entry.install_path)
        if dest.exists():
            if dest.is_symlink():
                dest.unlink()
            else:
                shutil.rmtree(dest)

        del self._installed[name]
        self._loaded.pop(name, None)
        self._save_installed_registry()
        return True

    # ---- Enable/Disable ----

    def enable(self, name: str) -> bool:
        if name in self._installed:
            self._installed[name].enabled = True
            self._save_installed_registry()
            return True
        return False

    def disable(self, name: str) -> bool:
        if name in self._installed:
            self._installed[name].enabled = False
            self._save_installed_registry()
            return True
        return False

    # ---- List / Get ----

    def list_installed(self) -> list[InstalledEntry]:
        return list(self._installed.values())

    def get_loaded(self, name: str) -> LoadedPlugin | None:
        return self._loaded.get(name)

    def load_all(self) -> list[LoadedPlugin]:
        """Load all enabled plugins from cache."""
        plugins: list[LoadedPlugin] = []
        for name, entry in self._installed.items():
            if not entry.enabled:
                continue
            if name in self._loaded:
                plugins.append(self._loaded[name])
                continue

            path = Path(entry.install_path)
            if path.is_symlink():
                path = path.resolve()
            if not path.exists():
                continue

            plugin = load_plugin(path, source=entry.source)
            self._loaded[name] = plugin
            plugins.append(plugin)
        return plugins

    def get_all_commands(self) -> list[Any]:
        """Get all commands from loaded plugins."""
        from clawpy.plugins.types import PluginCommand
        commands: list[PluginCommand] = []
        for plugin in self.load_all():
            commands.extend(plugin.commands)
        return commands
