"""Resumable, hash-identified shell session descriptors.

A remote shell is a live socket that dies with the process that opened it, so
it cannot be serialized and reloaded. What survives is the *descriptor*: which
target yielded the shell, through which exploit primitive, on which port, from
which attacker address, and when. This module persists one JSON descriptor per
session under a content-hashed id and re-opens the shell through the recorded
primitive on :func:`resume` -- the same reconnection model serious
post-exploitation frameworks use over non-persistent transports.

The store is deliberately decoupled from the transport: it imports
:mod:`modules.atomic_exploit_bridge` lazily and only inside :func:`resume`, so
registering a descriptor never pulls the socket layer and cannot deadlock the
loop. Every public function is fail-open: persistence or I/O errors degrade to
an empty result instead of raising into a campaign.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

_BASE_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"

ID_LENGTH = 16
STATUS_LIVE = "live"
STATUS_STALE = "stale"
STATUS_CLOSED = "closed"


def _store_dir() -> Path:
    """Return the per-session descriptor directory, created on demand."""
    directory = Path(_SESSIONS_DIR) / "shell_sessions"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 with a trailing Z."""
    import datetime

    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def session_id(target: str, via: str, created_at: str) -> str:
    """Return the stable content hash identifying a session.

    Args:
        target: Host that yielded the shell.
        via: Exploit primitive identifier that produced the shell.
        created_at: Not part of the identity; kept for signature symmetry
            with callers. Identity is ``target`` plus ``via`` so repeated
            shells on the same primitive map to one resumable descriptor.

    Returns:
        A :data:`ID_LENGTH`-character lowercase hex digest.
    """
    seed = f"{str(target).strip()}|{str(via).strip()}".encode("utf-8", "replace")
    return hashlib.sha256(seed).hexdigest()[:ID_LENGTH]


def _path_for(session: str) -> Path:
    """Return the descriptor path for a validated session id."""
    safe = "".join(c for c in str(session) if c in "0123456789abcdef")[:ID_LENGTH]
    return _store_dir() / f"{safe}.json"


def _write(record: dict[str, Any]) -> None:
    """Persist one descriptor atomically."""
    path = _path_for(record["id"])
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def register(target: str, via: str, port: int = 0, lhost: str = "127.0.0.1", evidence: str = "") -> dict[str, Any]:
    """Create or refresh the resumable descriptor for an obtained shell.

    Idempotent per ``(target, via)``: a second shell through the same
    primitive refreshes ``last_seen`` and restores ``live`` status on the one
    descriptor rather than forking a new id.

    Args:
        target: Host that yielded the shell.
        via: Exploit primitive identifier.
        port: Shell port on the target.
        lhost: Attacker address used to trigger the primitive.
        evidence: Optional short provenance note.

    Returns:
        The persisted descriptor, or an empty dict on failure.
    """
    host = str(target or "").strip()
    primitive = str(via or "").strip()
    if not host or not primitive:
        return {}
    try:
        now = _now_iso()
        sid = session_id(host, primitive, now)
        existing = get(sid) or {}
        record = {
            "id": sid,
            "target": host,
            "via": primitive,
            "port": int(port or existing.get("port", 0) or 0),
            "lhost": str(lhost or existing.get("lhost", "127.0.0.1")),
            "status": STATUS_LIVE,
            "created_at": existing.get("created_at", now),
            "last_seen": now,
            "resume_count": int(existing.get("resume_count", 0)),
            "evidence": str(evidence or existing.get("evidence", "")),
        }
        _write(record)
        return record
    except Exception:
        return {}


def get(session: str) -> dict[str, Any] | None:
    """Return one descriptor by id, or None when absent or unreadable."""
    try:
        path = _path_for(session)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def list_sessions(target: str = "") -> list[dict[str, Any]]:
    """Return persisted descriptors, newest first, optionally for one target.

    Each row is enriched with ``live`` reflecting whether the transport layer
    currently holds an in-process session for that ``(target, via)`` pair.
    """
    host = str(target or "").strip()
    rows: list[dict[str, Any]] = []
    try:
        live_keys = _live_keys()
    except Exception:
        live_keys = set()
    try:
        for path in _store_dir().glob("*.json"):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(record, dict) or not record.get("id"):
                continue
            if host and record.get("target") != host:
                continue
            record["live"] = (record.get("target"), record.get("via")) in live_keys
            rows.append(record)
    except Exception:
        return rows
    rows.sort(key=lambda r: str(r.get("last_seen", "")), reverse=True)
    return rows


def _live_keys() -> set[tuple[str, str]]:
    """Return ``(target, via)`` pairs the transport layer currently caches."""
    try:
        from modules.atomic_exploit_bridge import live_sessions

        return {(row.get("target", ""), row.get("owner", "") or row.get("via", "")) for row in live_sessions()}
    except Exception:
        return set()


def mark_closed(target: str, via: str = "") -> int:
    """Mark matching descriptors closed. Returns the count updated."""
    host = str(target or "").strip()
    primitive = str(via or "").strip()
    updated = 0
    for record in list_sessions(host):
        if primitive and record.get("via") != primitive:
            continue
        if record.get("status") == STATUS_CLOSED:
            continue
        record.pop("live", None)
        record["status"] = STATUS_CLOSED
        record["last_seen"] = _now_iso()
        try:
            _write(record)
            updated += 1
        except Exception:
            continue
    return updated


def _reopen_primitive(target: str, via: str, lhost: str) -> bool:
    """Re-open the shell through the recorded primitive. Returns liveness.

    Resolves the exploit spec by id and asks the transport layer to establish
    (or adopt) a live multiplexed session. Never raises.
    """
    try:
        from modules.atomic_exploit_bridge import EXPLOITS_DIR, ensure_session, load_all

        specs = load_all(EXPLOITS_DIR)
        spec = specs.get(via)
        if spec is None:
            return False
        session = ensure_session(spec, target, lhost=lhost or "127.0.0.1")
        return bool(session and session.alive())
    except Exception:
        return False


def resume(session: str) -> dict[str, Any]:
    """Re-establish a persisted shell session through its recorded primitive.

    Args:
        session: The hashed session id.

    Returns:
        ``{"ok": True, "target", "via", "id", "resume_count"}`` on success, or
        ``{"ok": False, "error": ...}``. A primitive that no longer answers
        marks the descriptor ``stale`` so the operator sees it is not live.
    """
    record = get(session)
    if not record:
        return {"ok": False, "error": f"session not found: {session}"}
    target = str(record.get("target", ""))
    via = str(record.get("via", ""))
    lhost = str(record.get("lhost", "127.0.0.1"))
    live = _reopen_primitive(target, via, lhost)
    record.pop("live", None)
    if not live:
        record["status"] = STATUS_STALE
        record["last_seen"] = _now_iso()
        try:
            _write(record)
        except Exception:
            pass
        return {"ok": False, "error": f"primitive {via} did not answer on {target}", "id": record["id"]}
    record["status"] = STATUS_LIVE
    record["last_seen"] = _now_iso()
    record["resume_count"] = int(record.get("resume_count", 0)) + 1
    try:
        _write(record)
    except Exception:
        pass
    return {
        "ok": True,
        "id": record["id"],
        "target": target,
        "via": via,
        "resume_count": record["resume_count"],
    }
