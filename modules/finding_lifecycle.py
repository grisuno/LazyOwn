"""Finding confirmation lifecycle: pending -> confirmed / rejected.

Faithful to the CAIRN discipline (seed-add, seed validation, dead-end
suppression list): a finding only becomes intel once it carries linked
evidence. Anything else stays pending; disproven leads go to the dead-end
list with a labeled reason instead of being silently dropped.

- explicit states persist in ``sessions/finding_lifecycle.json``;
- ``resolve()`` layers explicit state over the automatic rule
  (2+ independent corroborating sources auto-confirm, like CAIRN's
  multi-signal confirmation), explicit reject always wins;
- the campaign funnel counts only confirmed findings at its narrow end.

Stdlib only.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

PENDING = "pending"
CONFIRMED = "confirmed"
REJECTED = "rejected"

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

STORE_FILENAME = "finding_lifecycle.json"
AUTO_CONFIRM_SOURCES = 2


def _store_path(sessions_dir: str | Path) -> Path:
    """Return the lifecycle store path for a sessions directory."""
    return Path(str(sessions_dir)) / STORE_FILENAME


def _load(sessions_dir: str | Path) -> dict:
    """Load the store, tolerating missing or corrupt files."""
    try:
        data = json.loads(_store_path(sessions_dir).read_text())
    except (OSError, ValueError):
        return {"findings": {}, "dead_ends": []}
    if not isinstance(data, dict):
        return {"findings": {}, "dead_ends": []}
    data.setdefault("findings", {})
    data.setdefault("dead_ends", [])
    return data


def _save(sessions_dir: str | Path, data: dict) -> None:
    """Persist the store best-effort."""
    try:
        _store_path(sessions_dir).write_text(json.dumps(data, indent=2))
    except OSError:
        pass


def confirm(finding_id: str, evidence: list[str] | None = None,
            sessions_dir: str | Path = SESSIONS_DIR, by: str = "operator") -> dict:
    """Mark a finding confirmed with linked evidence (CAIRN seed-add).

    Evidence mentioning a CVE id is auto-enriched with keyless OSINT
    (OSV advisory, CISA KEV, EPSS score); enrichment never fails the call.
    """
    store = _load(sessions_dir)
    items = [str(e) for e in (evidence or []) if str(e).strip()]
    try:
        from modules.osint_enrich import enrich_evidence as _enrich
    except Exception:
        _enrich = None
    if _enrich is not None:
        try:
            items = _enrich(items, sessions_dir)
        except Exception:
            pass
    store["findings"][str(finding_id)] = {
        "status": CONFIRMED, "evidence": items[:12], "by": by,
        "at": time.time(),
    }
    _save(sessions_dir, store)
    return store["findings"][str(finding_id)]


def reject(finding_id: str, reason: str = "",
           sessions_dir: str | Path = SESSIONS_DIR, by: str = "operator") -> dict:
    """Mark a finding rejected (disproven lead, CAIRN dead-end discipline)."""
    store = _load(sessions_dir)
    store["findings"][str(finding_id)] = {
        "status": REJECTED, "evidence": [], "by": by,
        "at": time.time(), "reason": str(reason)[:200],
    }
    _save(sessions_dir, store)
    return store["findings"][str(finding_id)]


def add_dead_end(kind: str, value: str, reason: str = "",
                 sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Suppress a value campaign-wide with a labeled reason (dead_end_hashes)."""
    store = _load(sessions_dir)
    entry = {"kind": str(kind), "value": str(value).strip().lower(),
             "reason": str(reason)[:200], "at": time.time()}
    store["dead_ends"] = [e for e in store["dead_ends"]
                          if not (e.get("kind") == entry["kind"]
                                  and e.get("value") == entry["value"])]
    store["dead_ends"].append(entry)
    _save(sessions_dir, store)
    return entry


def is_dead_end(kind: str, value: str, sessions_dir: str | Path = SESSIONS_DIR) -> bool:
    """Return True when a kind/value pair sits on the suppression list."""
    store = _load(sessions_dir)
    needle = str(value).strip().lower()
    return any(e.get("kind") == str(kind) and e.get("value") == needle
               for e in store["dead_ends"])


def suppressed_values(sessions_dir: str | Path = SESSIONS_DIR) -> list[str]:
    """Return every suppressed value for text-level filtering by the loop."""
    store = _load(sessions_dir)
    return sorted({str(e.get("value", "")) for e in store["dead_ends"]
                   if e.get("value")})


def resolve(node: dict, sessions_dir: str | Path = SESSIONS_DIR) -> str:
    """Resolve a finding node's confirmation state.

    Precedence: dead-end list and explicit reject beat everything;
    explicit confirm beats the automatic multi-source rule; otherwise
    2+ independent sources auto-confirm, single-source stays pending.
    Non-finding nodes always resolve to pending.
    """
    if not str(node.get("kind", "")).startswith("finding"):
        return PENDING
    fid = str(node.get("id", ""))
    store = _load(sessions_dir)
    record = store["findings"].get(fid, {})
    if record.get("status") == REJECTED:
        return REJECTED
    if is_dead_end(str(node.get("kind", "")), str(node.get("value", "")),
                   sessions_dir):
        return REJECTED
    if record.get("status") == CONFIRMED:
        return CONFIRMED
    sources = {str(s) for s in (node.get("sources", []) or [])}
    if len(sources) >= AUTO_CONFIRM_SOURCES:
        return CONFIRMED
    return PENDING


def apply_confirmation(nodes: dict[str, dict],
                       sessions_dir: str | Path = SESSIONS_DIR) -> None:
    """Stamp ``confirmation``/``status`` on every finding node in place."""
    for node in nodes.values():
        if not str(node.get("kind", "")).startswith("finding"):
            continue
        state = resolve(node, sessions_dir)
        node["confirmation"] = state
        node["status"] = state


__all__ = [
    "PENDING",
    "CONFIRMED",
    "REJECTED",
    "STORE_FILENAME",
    "AUTO_CONFIRM_SOURCES",
    "add_dead_end",
    "apply_confirmation",
    "confirm",
    "is_dead_end",
    "reject",
    "resolve",
    "suppressed_values",
]
