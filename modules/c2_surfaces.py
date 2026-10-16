"""C2 dashboard surfaces fed by the autonomous loop and APT chains.

Single chokepoint (same philosophy as ``chain_registry`` and the
exploit catalogue): every automated write to operator-visible C2
state — banners, CVEs, notes, event rules, session reports — goes
through here. Reads mirror lazyc2's own formats exactly
(``sessions/banners.json``, ``sessions/cves.json``,
``sessions/notes.txt``, ``event_config.json``) so the dashboard needs
zero changes.

Security invariants:
    1. Appends and dedupes only; never deletes operator content.
    2. Every write is atomic (tmp + replace) and capped in size.
    3. Every public function is best-effort and never raises — a full
       disk or a corrupt JSON must not break an engagement loop.
    4. No network, no shell, no credentials handled here.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

log = logging.getLogger("c2_surfaces")

_BASE_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"
_EVENT_CONFIG = _BASE_DIR / "event_config.json"

_MAX_FILE_BYTES = 2_000_000
_MAX_NOTE_CHARS = 200_000

_SEVERITY_TO_RISK = {"critical": "CRITICAL", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}


def _read_json(path: Path, default: Any) -> Any:
    """Read JSON, returning *default* on any failure or oversize file."""
    try:
        if not path.exists() or path.stat().st_size > _MAX_FILE_BYTES:
            return default
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            return json.load(fh)
    except Exception as exc:
        log.debug("surface read failed %s: %s", path, exc)
        return default


def _write_json(path: Path, data: Any) -> bool:
    """Atomic JSON write (tmp + replace). Returns success."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f"{path.name}.tmp.{os.getpid()}")
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
        return True
    except Exception as exc:
        log.debug("surface write failed %s: %s", path, exc)
        return False


def _stamp() -> str:
    """UTC timestamp for notes and descriptions."""
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def publish_banner(
    hostname: str = "",
    port: str | int = "",
    protocol: str = "tcp",
    service: str = "",
    extra: str = "",
    sessions_dir: Path | str = _SESSIONS_DIR,
) -> bool:
    """Append a service banner to sessions/banners.json (deduplicated).

    Matches the ``/banners`` table columns (Hostname, Port, Protocol,
    Extra, Service). Returns True when stored (or already present).
    """
    path = Path(sessions_dir) / "banners.json"
    data = _read_json(path, {"banners": []})
    if not isinstance(data, dict):
        data = {"banners": []}
    banners = data.get("banners", [])
    if not isinstance(banners, list):
        banners = []
    entry = {
        "hostname": str(hostname or ""),
        "port": str(port or ""),
        "protocol": str(protocol or "tcp"),
        "service": str(service or ""),
        "extra": str(extra or "")[:300],
    }
    key = (entry["hostname"].lower(), entry["port"], entry["service"].lower())
    for existing in banners:
        if not isinstance(existing, dict):
            continue
        if (
            str(existing.get("hostname", "")).lower(),
            str(existing.get("port", "")),
            str(existing.get("service", "")).lower(),
        ) == key:
            return True
    banners.append(entry)
    data["banners"] = banners
    return _write_json(path, data)


def publish_cve(
    title: str,
    description: str = "",
    operator: str = "autonomous_loop",
    risk: str = "HIGH",
    sessions_dir: Path | str = _SESSIONS_DIR,
) -> bool:
    """Append a CVE finding to sessions/cves.json (deduplicated by title).

    ``risk`` must be one of CRITICAL/HIGH/MEDIUM/LOW/INFORMATIONAL
    (mirrors the /cves form validation). Returns True when stored or
    already present.
    """
    title = (title or "").strip()[:200]
    if not title:
        return False
    risk = str(risk or "").upper()
    if risk not in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"):
        risk = "MEDIUM"
    path = Path(sessions_dir) / "cves.json"
    cves = _read_json(path, [])
    if not isinstance(cves, list):
        cves = []
    for existing in cves:
        if isinstance(existing, dict) and str(existing.get("title", "")).strip().lower() == title.lower():
            return True
    taken = {c.get("id") for c in cves if isinstance(c, dict) and isinstance(c.get("id"), int)}
    new_id = max(taken) + 1 if taken else 0
    cves.append(
        {
            "id": new_id,
            "title": title,
            "description": str(description or "")[:2000],
            "operator": str(operator or "autonomous_loop"),
            "risk": risk,
        }
    )
    return _write_json(path, cves)


def append_note(line: str, sessions_dir: Path | str = _SESSIONS_DIR) -> bool:
    """Append one timestamped line to sessions/notes.txt (never overwrites).

    The dashboard stores a single ``{"content": ...}`` blob; appending
    preserves operator notes while surfacing loop/loot events.
    """
    line = (line or "").strip()
    if not line:
        return False
    path = Path(sessions_dir) / "notes.txt"
    try:
        current = ""
        if path.exists() and path.stat().st_size <= _MAX_FILE_BYTES:
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                raw = fh.read().strip()
            if raw:
                try:
                    current = str(json.loads(raw).get("content", ""))
                except (json.JSONDecodeError, AttributeError):
                    current = raw
        merged = (current + f"\n[{_stamp()}] {line}").strip()[-_MAX_NOTE_CHARS:]
        with path.open("w", encoding="utf-8") as fh:
            fh.write(json.dumps({"content": merged}, ensure_ascii=False))
        return True
    except Exception as exc:
        log.debug("note append failed: %s", exc)
        return False


def register_loot_event(
    name: str,
    path_glob: str,
    description: str = "",
    event_config: Path | str = _EVENT_CONFIG,
) -> bool:
    """Register an event_config.json rule watching an artefact glob.

    Lets the C2 event engine track loop-produced artefacts (loot,
    emulation reports) like any operator-defined rule. Dedupes by rule
    name. Returns True when stored or already present.
    """
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", (name or "").strip())[:80]
    path_glob = (path_glob or "").strip()
    if not name or not path_glob or ".." in path_glob or "\x00" in path_glob:
        return False
    if os.path.isabs(path_glob) or not path_glob.startswith("sessions/"):
        return False
    cfg_path = Path(event_config)
    config = _read_json(cfg_path, {"events": []})
    if not isinstance(config, dict):
        config = {"events": []}
    events = config.get("events", [])
    if not isinstance(events, list):
        events = []
    for existing in events:
        if isinstance(existing, dict) and existing.get("name") == name:
            return True
    events.append(
        {
            "name": name,
            "src_path": path_glob,
            "size": 500000,
            "description": str(description or f"Auto-registered by autonomous loop [{_stamp()}]")[:300],
            "outputtype": "txt",
            "outputtodelete": "",
            "prompt": "",
            "operator": "autonomous_loop",
            "status": "New",
        }
    )
    config["events"] = events
    return _write_json(cfg_path, config)


def refresh_session_report(timeout: int = 120) -> bool:
    """Regenerate sessions/sessionLazyOwn.json via modules/session_state.py.

    This is what the legacy ``/report`` page renders. Best-effort
    subprocess with a timeout; never raises.
    """
    import subprocess as _sp

    try:
        completed = _sp.run(
            ["python3", "modules/session_state.py"],
            cwd=str(_BASE_DIR),
            capture_output=True,
            text=True,
            timeout=max(10, timeout),
        )
        return completed.returncode == 0
    except Exception as exc:
        log.debug("session report refresh failed: %s", exc)
        return False


def severity_to_risk(severity: str) -> str:
    """Map exploit severity words to /cves risk levels."""
    return _SEVERITY_TO_RISK.get((severity or "").lower(), "MEDIUM")


def _normalize_task_title(title: object) -> str:
    """Collapse a task title to its dedup key (case/space-insensitive)."""
    return re.sub(r"\s+", " ", str(title or "")).strip().lower()


def group_tasks_for_display(tasks: list) -> tuple[list, int]:
    """Group tasks for the /tasks page: unique hits with counts + noise tally.

    Uses the shared ``audit_tasks`` classifier when importable (drops
    timestamp/URL bogus credentials and duplicate titles); falls back to
    plain title grouping otherwise. Never raises — worst case returns
    every task as its own group. Returns (groups, noise_count) where
    each group is {"task": first_task_dict, "count": n}.
    """
    items = [t for t in (tasks or []) if isinstance(t, dict)]
    kept: list = list(items)
    noise = 0
    try:
        sys.path.insert(0, str(_BASE_DIR / "skills"))
        from lazyown_mcp_helpers import audit_tasks as _audit  # type: ignore

        kept = []
        for entry, task in zip(_audit(items), items, strict=False):
            if getattr(entry, "keep", True):
                kept.append(task)
            else:
                noise += 1
    except Exception as exc:
        log.debug("task audit unavailable, plain grouping: %s", exc)
    groups: list = []
    seen: dict = {}
    for task in kept:
        key = _normalize_task_title(task.get("title", ""))
        if key in seen:
            seen[key]["count"] += 1
        else:
            entry = {"task": task, "count": 1}
            seen[key] = entry
            groups.append(entry)
    return groups, noise
