"""Campaign command blacklist loaded from ``sessions/campaign_lessons.jsonl``.

A lesson with ``outcome == "failed"`` blacklists its command head under the
lesson's ``context`` (or ``any``), so a history- or catalogue-driven selector
never re-proposes a command a past campaign already learned to be a dead end.
The loader lived privately in the daemon; it is shared here so both autonomous
runtimes consult one blacklist. The result is cached and reloaded when the
lessons file changes.
"""

from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

_CACHE: dict[str, object] = {"data": {}, "mtime": -1.0}


def _lessons_path() -> Path:
    """Return the lessons file path, resolved at call time for test isolation."""
    return SESSIONS_DIR / "campaign_lessons.jsonl"


def _load() -> dict[str, list[str]]:
    """Parse the lessons file into a context -> blacklisted command-head map."""
    blacklist: dict[str, list[str]] = {}
    path = _lessons_path()
    if not path.exists():
        return blacklist
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            lesson = json.loads(line)
            if lesson.get("outcome") != "failed":
                continue
            parts = str(lesson.get("command", "") or "").strip().split()
            if not parts:
                continue
            command = parts[0]
            ctx = str(lesson.get("context", "any") or "any")
            blacklist.setdefault(ctx, [])
            if command not in blacklist[ctx]:
                blacklist[ctx].append(command)
    except Exception:
        return blacklist
    return blacklist


def campaign_blacklist() -> dict[str, list[str]]:
    """Return the cached blacklist, reloading when the lessons file changes."""
    path = _lessons_path()
    mtime = path.stat().st_mtime if path.exists() else -1.0
    if mtime != _CACHE["mtime"]:
        _CACHE["data"] = _load()
        _CACHE["mtime"] = mtime
    return dict(_CACHE["data"])  # type: ignore[arg-type]


def blocked_commands(category: str) -> set[str]:
    """Return command heads blacklisted for a category plus the global ``any``."""
    data = campaign_blacklist()
    return set(data.get(category, [])) | set(data.get("any", []))


__all__ = ["BASE_DIR", "SESSIONS_DIR", "blocked_commands", "campaign_blacklist"]
