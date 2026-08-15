"""Plugin types — manifest, loaded plugin, component definitions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class PluginManifest:
    """Plugin manifest from plugin.json."""

    name: str
    version: str = "0.0.0"
    description: str = ""
    author: str = ""
    homepage: str = ""
    keywords: list[str] = field(default_factory=list)

    # Component directories (relative to plugin root)
    commands: list[str] = field(default_factory=list)  # markdown command files
    agents: list[str] = field(default_factory=list)  # markdown agent files
    skills: list[str] = field(default_factory=list)  # skill directories
    hooks: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PluginManifest:
        commands = data.get("commands", [])
        if isinstance(commands, str):
            commands = [commands]
        agents = data.get("agents", [])
        if isinstance(agents, str):
            agents = [agents]
        skills = data.get("skills", [])
        if isinstance(skills, str):
            skills = [skills]

        return cls(
            name=data.get("name", ""),
            version=data.get("version", "0.0.0"),
            description=data.get("description", ""),
            author=data.get("author", {}).get("name", "") if isinstance(data.get("author"), dict) else str(data.get("author", "")),
            homepage=data.get("homepage", ""),
            keywords=data.get("keywords", []),
            commands=commands,
            agents=agents,
            skills=skills,
            hooks=data.get("hooks", {}),
        )

    @classmethod
    def from_file(cls, path: Path) -> PluginManifest:
        data = json.loads(path.read_text())
        return cls.from_dict(data)


@dataclass(slots=True)
class PluginCommand:
    """A slash command loaded from a plugin markdown file."""

    name: str  # e.g. "myplugin:build"
    description: str
    content: str  # The prompt template
    plugin_name: str
    source_file: str
    allowed_tools: list[str] = field(default_factory=list)
    model: str = ""


@dataclass(slots=True)
class PluginAgent:
    """An agent definition loaded from a plugin markdown file."""

    name: str
    description: str
    system_prompt: str
    plugin_name: str
    source_file: str
    tools: list[str] = field(default_factory=list)
    model: str = ""


@dataclass(slots=True)
class LoadedPlugin:
    """A fully loaded plugin with all components resolved."""

    name: str
    manifest: PluginManifest
    install_path: Path
    source: str  # "github:owner/repo", "local:/path", "marketplace:name"
    enabled: bool = True
    commands: list[PluginCommand] = field(default_factory=list)
    agents: list[PluginAgent] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)  # Skill directory paths
    errors: list[str] = field(default_factory=list)
