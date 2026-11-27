"""Operator engagement state primitives shared across layers.

Pure karma ranking plus a file-backed snapshot reader extracted from
``cli.engagement_hooks`` so ``modules`` consumers (gym scoreboard, C2
auth surfaces) never import upward into ``cli``. The CLI module owns
the live in-memory state; this module only ranks and reads.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

SESSIONS_DIR = Path("sessions")

KARMA_THRESHOLDS: tuple[tuple[int, str], ...] = (
    (1000, "Noob"),
    (2000, "Rookie"),
    (3000, "Skidy"),
    (4000, "Hacker"),
    (5000, "Pro"),
    (6000, "Elite"),
)
KARMA_TOP: str = "Godlike"


def get_karma_name(elo: int) -> str:
    """Return karma rank for an ELO score.

    Mirrors the bracket function ``get_karma_name`` in ``lazyc2.py`` so
    the terminal and the C2 web UI display identical ranks for the same
    operator.

    Args:
        elo: Non-negative integer score.

    Returns:
        Human-facing karma label (``Noob`` … ``Godlike``).
    """
    for threshold, label in KARMA_THRESHOLDS:
        if elo < threshold:
            return label
    return KARMA_TOP


def read_state_snapshot(sessions_dir: str | Path | None = None) -> dict[str, Any]:
    """Read the persisted engagement state without CLI module state.

    Fail-soft by contract: any I/O or parse problem yields an empty
    mapping so dashboard/gym surfaces degrade instead of raising.

    Args:
        sessions_dir: Directory holding ``engagement_state.json``.
            Defaults to the repo-relative ``sessions`` directory.

    Returns:
        Plain dict with the persisted engagement fields, or ``{}``.
    """
    base = Path(sessions_dir) if sessions_dir else SESSIONS_DIR
    try:
        raw = json.loads((base / "engagement_state.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(raw, dict):
        return {}
    elo = int(raw.get("elo", 0) or 0)
    snapshot = dict(raw)
    snapshot["karma_name"] = get_karma_name(elo)
    return snapshot


_snapshot_provider: Callable[[], dict[str, Any]] | None = None


def register_snapshot_provider(provider: Callable[[], dict[str, Any]]) -> None:
    """Register the live-state snapshot provider (layer inversion).

    The CLI engagement module owns the in-memory state; it registers
    its snapshot getter at import time so modules consumers see live
    data. Passing ``None`` falls back to the file-backed reader.

    Args:
        provider: Zero-argument callable returning a snapshot dict.
    """
    global _snapshot_provider
    _snapshot_provider = provider


def state_snapshot() -> dict[str, Any]:
    """Return the current engagement snapshot (live when available).

    Returns:
        Snapshot dict; empty when no state exists.
    """
    if _snapshot_provider is not None:
        try:
            return dict(_snapshot_provider() or {})
        except Exception:
            return {}
    return read_state_snapshot()


__all__ = [
    "KARMA_THRESHOLDS",
    "KARMA_TOP",
    "get_karma_name",
    "read_state_snapshot",
    "register_snapshot_provider",
    "state_snapshot",
]
