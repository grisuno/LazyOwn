"""Declarative cmd2 alias loader.

Reads ``cli/aliases.yaml`` and substitutes ``{name}`` placeholders against a
payload dict (typically loaded from ``payload.json``). Missing keys substitute
to an empty string so a partially configured shell still loads every alias.

Usage::

    from core.config import load_payload
    from cli.aliases import load_aliases

    aliases = load_aliases(load_payload())
    self.aliases.update(aliases)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ALIASES_PATH = Path(__file__).resolve().parent / "aliases.yaml"


class _SafeFormatDict(dict):
    """``str.format_map`` source that returns ``""`` for missing/None values."""

    def __missing__(self, key: str) -> str:
        return ""

    def __getitem__(self, key: str) -> str:
        if key not in self:
            return ""
        value = super().__getitem__(key)
        return "" if value is None else str(value)


def _substitute(template: str, payload: dict[str, Any]) -> str:
    """Render ``template`` against ``payload`` placeholders.

    Falls back to the literal template if ``str.format_map`` raises
    (e.g. unbalanced braces from legacy strings) so a malformed entry
    cannot prevent the shell from booting.
    """
    safe = _SafeFormatDict(payload)
    try:
        return template.format_map(safe)
    except (IndexError, ValueError):
        return template


def load_aliases(payload: dict[str, Any] | None = None, path: Path = ALIASES_PATH) -> dict[str, str]:
    """Return the resolved cmd2 alias map.

    Args:
        payload: Configuration dict for placeholder substitution. If ``None``
            the function reads ``payload.json`` lazily so callers don't have
            to import :mod:`core.config` themselves.
        path: Override the YAML location (used by tests).

    Returns:
        Flat ``{name: command}`` dict suitable for ``self.aliases.update(...)``.

    Raises:
        FileNotFoundError: ``path`` does not exist.
        yaml.YAMLError: file is malformed YAML.
        TypeError: top-level YAML is not a mapping.
        ValueError: a key or value has the wrong type.
    """
    if payload is None:
        from core.config import load_payload

        payload = load_payload()

    with path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    if not isinstance(raw, dict):
        raise TypeError(f"{path} must contain a top-level mapping, got {type(raw).__name__}")

    resolved: dict[str, str] = {}
    for name, template in raw.items():
        if not isinstance(name, str):
            raise ValueError(f"alias name must be string, got {type(name).__name__}: {name!r}")
        if not isinstance(template, str):
            raise ValueError(f"alias '{name}' value must be string, got {type(template).__name__}")
        resolved[name] = _substitute(template, payload)
    return resolved


__all__ = ["ALIASES_PATH", "load_aliases"]
