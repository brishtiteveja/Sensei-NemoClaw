"""Provider registry — maps provider names to factory functions."""

from __future__ import annotations

from typing import Any, Callable

from clawpy.config.config import ProviderConfig
from clawpy.provider.base import Provider

ProviderFactory = Callable[[ProviderConfig], Any]  # Returns Provider-compatible

_registry: dict[str, ProviderFactory] = {}


def register(name: str, factory: ProviderFactory) -> None:
    """Register a provider factory by name."""
    _registry[name] = factory


def create(name: str, cfg: ProviderConfig) -> Provider:
    """Create a provider instance by name."""
    if name not in _registry:
        available = ", ".join(sorted(_registry)) or "(none)"
        raise ValueError(f"Unknown provider: {name!r}. Available: {available}")
    provider: Provider = _registry[name](cfg)
    return provider


def available() -> list[str]:
    """Return sorted list of registered provider names."""
    return sorted(_registry)
