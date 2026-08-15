"""Custom agent definitions — .clawpy/agents/*.md files.

Each markdown file defines a reusable agent persona with YAML frontmatter
for name, description, tools, model, and a system prompt body.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from clawpy.config.paths import global_config_dir


@dataclass(slots=True)
class AgentDefinition:
    """A custom agent loaded from markdown."""

    name: str
    description: str
    system_prompt: str
    source_file: str
    tools: list[str] = field(default_factory=list)
    model: str = ""


def discover_agents(work_dir: str) -> list[AgentDefinition]:
    """Find agent definitions from project and global config."""
    agents: list[AgentDefinition] = []
    seen: set[str] = set()

    for agents_dir in [
        Path(work_dir) / ".clawpy" / "agents",
        global_config_dir() / "agents",
    ]:
        if not agents_dir.is_dir():
            continue
        for md in sorted(agents_dir.glob("*.md")):
            if md.stem in seen:
                continue
            seen.add(md.stem)
            agent = _load_agent_file(md)
            if agent:
                agents.append(agent)

    return agents


def _load_agent_file(path: Path) -> AgentDefinition | None:
    """Load an agent from a markdown file with YAML frontmatter."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None

    meta, body = _parse_frontmatter(text)
    if not body.strip():
        return None

    name = meta.get("name", path.stem)
    tools = meta.get("tools", [])
    if isinstance(tools, str):
        tools = [t.strip() for t in tools.split(",")]

    return AgentDefinition(
        name=name,
        description=meta.get("description", f"Agent: {name}"),
        system_prompt=body.strip(),
        source_file=str(path),
        tools=tools,
        model=meta.get("model", ""),
    )


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML-like frontmatter."""
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
            if val.startswith("[") and val.endswith("]"):
                meta[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",")]
            elif val.lower() in ("true", "false"):
                meta[key] = val.lower() == "true"
            else:
                meta[key] = val.strip("'\"")
    return meta, parts[2].strip()
