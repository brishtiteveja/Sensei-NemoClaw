"""Plugin loader — discovers and loads plugin components from directories.

Loads commands and agents from markdown files with optional YAML frontmatter.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from clawpy.plugins.types import (
    LoadedPlugin,
    PluginAgent,
    PluginCommand,
    PluginManifest,
)


def load_plugin(plugin_dir: Path, source: str = "") -> LoadedPlugin:
    """Load a plugin from a directory."""
    manifest = _load_manifest(plugin_dir)
    if not manifest.name:
        manifest.name = plugin_dir.name

    plugin = LoadedPlugin(
        name=manifest.name,
        manifest=manifest,
        install_path=plugin_dir,
        source=source or f"local:{plugin_dir}",
    )

    # Load commands
    commands_dir = plugin_dir / "commands"
    if commands_dir.is_dir():
        for md_file in sorted(commands_dir.glob("*.md")):
            try:
                cmd = _load_command(md_file, manifest.name)
                plugin.commands.append(cmd)
            except Exception as e:
                plugin.errors.append(f"Command {md_file.name}: {e}")

    # Also check manifest-declared command files
    for cmd_path in manifest.commands:
        resolved = plugin_dir / cmd_path
        if resolved.is_file() and resolved.suffix == ".md":
            try:
                cmd = _load_command(resolved, manifest.name)
                if not any(c.name == cmd.name for c in plugin.commands):
                    plugin.commands.append(cmd)
            except Exception as e:
                plugin.errors.append(f"Command {cmd_path}: {e}")

    # Load agents
    agents_dir = plugin_dir / "agents"
    if agents_dir.is_dir():
        for md_file in sorted(agents_dir.glob("*.md")):
            try:
                agent = _load_agent(md_file, manifest.name)
                plugin.agents.append(agent)
            except Exception as e:
                plugin.errors.append(f"Agent {md_file.name}: {e}")

    # Load skills (just track paths for now)
    skills_dir = plugin_dir / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                plugin.skills.append(str(skill_dir))

    return plugin


def _load_manifest(plugin_dir: Path) -> PluginManifest:
    """Load manifest from plugin.json or .claude-plugin/plugin.json."""
    for path in [
        plugin_dir / "plugin.json",
        plugin_dir / ".claude-plugin" / "plugin.json",
    ]:
        if path.exists():
            return PluginManifest.from_file(path)
    return PluginManifest(name=plugin_dir.name)


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML-like frontmatter from markdown. Returns (metadata, body)."""
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    meta: dict[str, Any] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # Handle lists (simple inline)
            if val.startswith("[") and val.endswith("]"):
                meta[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",")]
            elif val.lower() in ("true", "false"):
                meta[key] = val.lower() == "true"
            else:
                meta[key] = val.strip("'\"")
    return meta, parts[2].strip()


def _load_command(md_file: Path, plugin_name: str) -> PluginCommand:
    """Load a command from a markdown file."""
    text = md_file.read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(text)

    cmd_name = md_file.stem  # filename without .md
    full_name = f"{plugin_name}:{cmd_name}"

    return PluginCommand(
        name=full_name,
        description=meta.get("description", f"Command from {plugin_name}"),
        content=body,
        plugin_name=plugin_name,
        source_file=str(md_file),
        allowed_tools=meta.get("allowed_tools", meta.get("allowedTools", [])),
        model=meta.get("model", ""),
    )


def _load_agent(md_file: Path, plugin_name: str) -> PluginAgent:
    """Load an agent from a markdown file."""
    text = md_file.read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(text)

    agent_name = meta.get("name", md_file.stem)

    return PluginAgent(
        name=agent_name,
        description=meta.get("description", f"Agent from {plugin_name}"),
        system_prompt=body,
        plugin_name=plugin_name,
        source_file=str(md_file),
        tools=meta.get("tools", []),
        model=meta.get("model", ""),
    )
