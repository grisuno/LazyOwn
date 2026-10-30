"""Freshness ledger: TTL windows per verb and target for the loop worker.

CVEngine doctrine, adapted: recurring windows are ledger windows, not
schedules. A tool that already answered for one target within its
freshness TTL skips the repeat; rows that never ran or waited the
longest come first (``stale_first``). Claims are bounding, never
blocking — a missing store file, a malformed row or any failure around
the ledger degrades to "not fresh" so the loop keeps working.

State: ``sessions/lazy/verb_ledger.json`` — ``{key: {"ts", "ok"}}``.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

LEDGER_FILENAME = "verb_ledger.json"

DEFAULT_TTL_SEC = {
    "lazynmap": 7 * 86400.0,
    "lazyaddon": 72 * 3600.0,
    "lazy_addon": 72 * 3600.0,
    "apt_chain": 72 * 3600.0,
}
_DEFAULT_TTL = 24 * 3600.0
_ADDON_PREFIX = "lazy_"
_MAX_ROWS = 8000


def window_for(verb: str) -> float:
    """Return the freshness window for one verb identity.

    Exact table entries win; derived addon identities
    (``lazy_<name>``) share the addon window; everything else takes
    the default day.

    Args:
        verb: Recorded verb identity.

    Returns:
        Window length in seconds.
    """
    lowered = str(verb or "").strip().lower()
    if lowered in DEFAULT_TTL_SEC:
        return DEFAULT_TTL_SEC[lowered]
    if lowered.startswith(_ADDON_PREFIX):
        return DEFAULT_TTL_SEC["lazy_addon"]
    return _DEFAULT_TTL


def ledger_key(verb: str, target: str) -> str:
    """Return the identity key of one verb/target pair."""
    return f"{str(verb or '').strip().lower()}|{str(target or '').strip().lower()}"


def key_from_command(command: str, target: str) -> str:
    """Derive the ledger key from one executed command line.

    Addon surfaces normalise: ``lazy addon <name> <target>``,
    ``lazy_addon run <name>`` and ``lazy_addon <name> --target <t>``
    key as ``lazy_<name>`` so proposals and executions collide on one
    freshness window. Any other shape keys by the first token.

    Args:
        command: Executed command line.
        target: Engagement target fallback for the key.

    Returns:
        Ledger identity key, or '' for a commandless event.
    """
    tokens = [token.lower() for token in str(command or "").split()]
    if not tokens:
        return ""
    lead, rest = tokens[0], tokens[1:]
    if lead == "lazy" and rest and rest[0] == "addon":
        name = rest[1] if len(rest) > 1 else ""
        addon_target = rest[2] if len(rest) > 2 else ""
        if name:
            return ledger_key(f"lazy_{name}", addon_target or target)
    if lead == "lazy_addon":
        pair = _addon_run_pair(rest)
        if pair:
            return ledger_key(f"lazy_{pair[0]}", pair[1] or target)
    return ledger_key(lead, target)


def _addon_run_pair(rest: list[str]) -> tuple[str, str] | None:
    """Extract ``<name>, <target>`` from a lazy_addon tail.

    Args:
        rest: Tokens after the ``lazy_addon`` verb.

    Returns:
        Pair or None when the tail names no module.
    """
    if not rest:
        return None
    if rest[0] == "run":
        if len(rest) < 2:
            return None
        name, tail = rest[1], rest[2:]
    else:
        name, tail = rest[0], rest[1:]
    if "--target" in tail:
        index = tail.index("--target")
        target = tail[index + 1] if index + 1 < len(tail) else ""
    else:
        target = tail[0] if tail else ""
    return name, target


def _path(sessions_dir: str | Path | None = None) -> Path:
    """Return the ledger file path under sessions/lazy."""
    from modules.lazy_loop import _store_path

    return Path(str(_store_path(LEDGER_FILENAME))) if sessions_dir is None else Path(str(sessions_dir)) / "lazy" / LEDGER_FILENAME


def _load(sessions_dir: str | Path | None = None) -> dict[str, dict[str, Any]]:
    """Load the ledger rows; malformed stores degrade to empty."""
    path = _path(sessions_dir)
    try:
        data = json_load(path)
        if isinstance(data, dict):
            return {str(key): dict(value) for key, value in data.items() if isinstance(value, dict)}
    except Exception:
        pass
    return {}


def json_load(path: Path) -> Any:
    """Read one JSON document or raise on malformed content."""
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def fresh(verb: str, target: str, now: float | None = None, sessions_dir: str | Path | None = None) -> bool:
    """Return True when one verb/target pair already ran inside its TTL.

    Args:
        verb: Command verb (``lazynmap``, ``lazyaddon``, ...).
        target: Target value.
        now: Reference epoch; defaults to current time.
        sessions_dir: Optional sessions directory override.

    Returns:
        True fresh, when the last recorded row is inside the window.
    """
    rows = _load(sessions_dir)
    row = rows.get(ledger_key(verb, target))
    if not row:
        return False
    try:
        ran_at = float(row.get("ts", 0.0))
    except (TypeError, ValueError):
        return False
    window = window_for(str(verb or "").strip().lower())
    return (now if now is not None else time.time()) - ran_at < window


def record(verb: str, target: str, ok: bool = True, now: float | None = None, sessions_dir: str | Path | None = None) -> None:
    """Upsert one completed run so the pair stops being stale.

    Args:
        verb: Command verb.
        target: Target value.
        ok: Whether the run completed usefully at all.
        now: Reference epoch; defaults to current time.
        sessions_dir: Optional sessions directory override.
    """
    path = _path(sessions_dir)
    rows = _load(sessions_dir)
    rows[ledger_key(verb, target)] = {
        "ts": float(now if now is not None else time.time()),
        "ok": bool(ok),
    }
    if len(rows) > _MAX_ROWS:
        rows = dict(sorted(rows.items(), key=lambda item: -float(item[1].get("ts", 0.0)))[:_MAX_ROWS])
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        import json

        path.write_text(json.dumps(rows), encoding="utf-8")
    except Exception:
        pass


def stale_first(
    catalog: list[tuple[str, str]],
    now: float | None = None,
    sessions_dir: str | Path | None = None,
) -> list[tuple[str, str]]:
    """Order verb/target pairs: never-run first, then longest-waiting.

    Args:
        catalog: ``[(verb, target), ...]`` candidate pairs.
        now: Reference epoch; defaults to current time.
        sessions_dir: Optional sessions directory override.

    Returns:
        Reordered candidate list.
    """
    rows = _load(sessions_dir)
    reference = now if now is not None else time.time()

    def _sort_key(pair: tuple[str, str]) -> tuple[int, float]:
        row = rows.get(ledger_key(*pair), {})
        try:
            ran_at = float(row.get("ts", 0.0))
        except (TypeError, ValueError):
            ran_at = 0.0
        return (1, ran_at) if ran_at else (0, 0.0)

    return sorted(catalog, key=_sort_key)


__all__ = [
    "DEFAULT_TTL_SEC",
    "LEDGER_FILENAME",
    "fresh",
    "ledger_key",
    "window_for",
    "record",
    "stale_first",
]
