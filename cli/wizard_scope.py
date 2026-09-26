"""Partial wizard scope: show current state or edit selected fields only.

The full wizard walks eight steps linearly. Operators who only need to
change rhost should not pass seven unrelated prompts. This module parses
the scope flags and exposes the editable field registry so do_wizard can
run a subset without duplicating prompt logic.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WizardScopeConfig:
    """Centralized knobs for partial wizard runs."""

    only_flag: str = "--only"
    show_flag: str = "--show"
    separator: str = ","


DEFAULT_SCOPE_CONFIG = WizardScopeConfig()

EDITABLE_FIELDS: tuple[str, ...] = ("rhost", "lhost", "domain", "device", "os_id")


@dataclass(frozen=True)
class WizardScope:
    """Parsed scope for one wizard invocation."""

    show_only: bool = False
    only: tuple[str, ...] = ()


def parse_scope(
    tokens: list[str],
    config: WizardScopeConfig = DEFAULT_SCOPE_CONFIG,
) -> WizardScope:
    """Parse --show and --only=a,b flags from wizard tokens.

    Args:
        tokens: Tokenised wizard arguments.
        config: Flag spellings and separator.

    Returns:
        WizardScope with show_only set and only holding validated field
        names in canonical order. Unknown names are dropped.
    """
    show_only = config.show_flag in tokens
    only: tuple[str, ...] = ()
    for token in tokens:
        if token.startswith(config.only_flag + "="):
            raw = token.split("=", 1)[1]
            wanted = [f.strip().lower() for f in raw.split(config.separator)]
            only = tuple(f for f in EDITABLE_FIELDS if f in wanted)
        elif token == config.only_flag:
            only = ()
    return WizardScope(show_only=show_only, only=only)


def status_rows(params: Mapping[str, Any]) -> list[tuple[str, str, str]]:
    """Build display rows for the current configuration state.

    Args:
        params: Live payload mapping.

    Returns:
        List of (setting, value, status) with status ok or missing.
    """
    rows: list[tuple[str, str, str]] = []
    for field in EDITABLE_FIELDS:
        value = params.get(field)
        if value:
            rows.append((field, str(value)[:48], "ok"))
        else:
            rows.append((field, "not set", "missing"))
    return rows


__all__ = [
    "WizardScope",
    "WizardScopeConfig",
    "DEFAULT_SCOPE_CONFIG",
    "EDITABLE_FIELDS",
    "parse_scope",
    "status_rows",
]
