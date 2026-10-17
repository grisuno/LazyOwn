"""Objectives sink: turn proven outcomes into follow-up work."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from modules.outcome_bus import SESSIONS_DIR, OutcomeEvent

_KINDS = frozenset({"finding", "exploit", "emulation", "chain"})
_PRIORITY = {"critical": "high", "high": "high", "medium": "medium", "low": "low", "info": "low"}


def apply(event: OutcomeEvent) -> bool:
    """Append one actionable objective when the outcome warrants it.

    Args:
        event: Outcome to convert.

    Returns:
        True when the objective was written.
    """
    text = (event.title or event.description or "").strip()
    if not text or event.kind not in _KINDS:
        return False
    if bool(event.metadata.get("dry_run")):
        return False
    if event.kind in ("exploit", "emulation", "chain") and not (event.success or event.shell):
        return False
    sessions = Path(str(event.metadata.get("sessions_dir") or SESSIONS_DIR))
    path = sessions / "objectives.jsonl"
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    digest = hashlib.sha1(f"{event.key()}:{text}".encode()).hexdigest()[:10]
    record = {
        "id": f"outcome_{digest}",
        "text": f"Review {event.cve or event.mitre_id or event.source}: {text[:200]}",
        "priority": _PRIORITY.get(str(event.severity or "").lower(), "medium"),
        "status": "pending",
        "source": "outcome_bus",
        "context": {
            "target": event.host_value,
            "task_id": event.task_id,
            "cve": event.cve,
            "mitre_id": event.mitre_id,
            "shell": event.shell,
        },
        "created_at": stamp,
        "updated_at": stamp,
        "notes": event.description[:500],
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        return False
    return True
