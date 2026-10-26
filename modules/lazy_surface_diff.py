"""Surface snapshot and diff: what changed about a host since last look.

Host/service rows in the world model are rewritten in place by every
scan, so "the previous scan's rows" is not a previous snapshot. Each
host therefore carries its own canonical snapshot; a refresh diffs the
current view against the stored one, appends the differences to a
change log, and replaces the snapshot. Downstream consumers read:

- ``sessions/lazy/surface_state.json`` — snapshot + last diff;
- node markers on the intel/attack graph (``changed`` attribute);
- the loop planner (a surface change re-arms discovery intents).

Every evaluator is a pure function so each diff rule is unit-testable
without files. Stdlib only; never raises into the caller.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSIONS_DIR = REPO_ROOT / "sessions"
STATE_FILENAME = "surface_state.json"

MAX_HOSTS_PER_DIFF = 5000
MAX_CHANGES_PER_REFRESH = 2000

KIND_HOST_NEW = "host_new"
KIND_HOST_GONE = "host_gone"
KIND_HOST_RETURNED = "host_returned"
KIND_PORT_OPENED = "port_opened"
KIND_PORT_CLOSED = "port_closed"
KIND_SERVICE_CHANGED = "service_changed"
KIND_VERSION_BUMPED = "version_bumped"
KIND_OS_CHANGED = "os_changed"

CHANGE_KINDS = (
    KIND_HOST_NEW,
    KIND_HOST_GONE,
    KIND_HOST_RETURNED,
    KIND_PORT_OPENED,
    KIND_PORT_CLOSED,
    KIND_SERVICE_CHANGED,
    KIND_VERSION_BUMPED,
    KIND_OS_CHANGED,
)


def snapshot_host(host: dict) -> dict:
    """Canonical snapshot of one host row.

    Args:
        host: World-model host dict with ``services``/``os_hint``.

    Returns:
        ``{"ports": {"443/tcp": {service, product, version}}, "os": str}``.
        Only open ports count.
    """
    ports: dict[str, dict] = {}
    services = host.get("services", {}) or {}
    items = services.items() if isinstance(services, dict) else []
    for port, svc in items:
        svc = svc if isinstance(svc, dict) else {"name": str(svc)}
        if str(svc.get("state", "open") or "open") not in ("", "open"):
            continue
        proto = str(svc.get("protocol", "tcp") or "tcp")
        key = f"{port}/{proto}"
        ports[key] = {
            "service": str(svc.get("name", "") or ""),
            "product": str(svc.get("product", "") or ""),
            "version": str(svc.get("version", "") or ""),
        }
    return {"ports": ports, "os": str(host.get("os_hint", "") or "")[:80]}


def fingerprint(state: dict) -> str:
    """Hash of the canonical snapshot; os text normalised case-insensitively."""
    normalised = {**state, "os": str(state.get("os", "")).lower()}
    return hashlib.sha1(json.dumps(normalised, sort_keys=True).encode()).hexdigest()


def _port_number(key: str) -> int | None:
    """Numeric port from a ``443/tcp`` key."""
    try:
        return int(str(key).split("/", 1)[0])
    except (ValueError, IndexError):
        return None


def diff_hosts(before: dict, after: dict) -> list[tuple]:
    """Pure diff of two host snapshot maps.

    Args:
        before: ``{host: snapshot}`` previous state.
        after: ``{host: snapshot}`` current state.

    Returns:
        List of ``(kind, host, port, detail)`` tuples sorted host/port
        first. A host that vanished and came back reads as
        ``host_returned``; a product appearing where none was recorded
        is enrichment, not a change.
    """
    out: list[tuple] = []
    before, after = before or {}, after or {}
    for host in sorted(set(before) | set(after), key=lambda h: (h)):
        b_state, a_state = before.get(host), after.get(host)
        if b_state is None and a_state is not None:
            out.append((KIND_HOST_NEW, host, None, {"os": a_state.get("os", "")}))
            continue
        if b_state is not None and a_state is None:
            out.append((KIND_HOST_GONE, host, None, {}))
            continue
        if fingerprint(b_state or {}) == fingerprint(a_state or {}):
            continue
        if str(b_state.get("os", "")).lower() != str(a_state.get("os", "")).lower() and a_state.get("os"):
            out.append((KIND_OS_CHANGED, host, None, {"before": b_state.get("os", ""), "after": a_state.get("os", "")}))
        b_ports = (b_state or {}).get("ports", {}) or {}
        a_ports = (a_state or {}).get("ports", {}) or {}
        for key in sorted(set(a_ports) - set(b_ports), key=lambda k: (_port_number(k) or 0, k)):
            out.append((KIND_PORT_OPENED, host, _port_number(key), {"port": key, **a_ports[key]}))
        for key in sorted(set(b_ports) - set(a_ports), key=lambda k: (_port_number(k) or 0, k)):
            out.append((KIND_PORT_CLOSED, host, _port_number(key), {"port": key, **b_ports[key]}))
        for key in sorted(set(a_ports) & set(b_ports)):
            b_svc, a_svc = b_ports.get(key) or {}, a_ports.get(key) or {}
            if (b_svc.get("service") or "") != (a_svc.get("service") or ""):
                out.append(
                    (
                        KIND_SERVICE_CHANGED,
                        host,
                        _port_number(key),
                        {"port": key, "before": b_svc.get("service", ""), "after": a_svc.get("service", "")},
                    )
                )
            elif (b_svc.get("version") or "") != (a_svc.get("version") or "") and a_svc.get("version"):
                out.append(
                    (
                        KIND_VERSION_BUMPED,
                        host,
                        _port_number(key),
                        {"port": key, "before": b_svc.get("version", ""), "after": a_svc.get("version", "")},
                    )
                )
    return out


def _load_previous(path: Path) -> dict:
    """Load the stored snapshot map, tolerating a missing/corrupt file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {k: v for k, v in (data.get("hosts", {}) or {}).items() if isinstance(v, dict)}
    except (OSError, ValueError):
        pass
    return {}


def current_snapshots(world: dict | None = None) -> dict[str, dict]:
    """Snapshot every host of the current world model view.

    Args:
        world: Preloaded world-model dict; read from disk when None.

    Returns:
        ``{host: snapshot}``.
    """
    if world is None:
        try:
            from modules.world_model import read_state_dict

            world = read_state_dict(SESSIONS_DIR / "world_model.json")
        except Exception:
            world = {}
    hosts = world.get("hosts", {}) or {}
    if isinstance(hosts, list):
        hosts = {str(h.get("ip", i)): h for i, h in enumerate(hosts) if isinstance(h, dict)}
    out: dict[str, dict] = {}
    for ip, host in list(hosts.items())[:MAX_HOSTS_PER_DIFF]:
        if isinstance(host, dict):
            out[ip] = snapshot_host(host)
    return out


def refresh(world: dict | None = None, sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Diff the current surface against the stored snapshot and persist.

    Args:
        world: Optional preloaded world-model dict.
        sessions_dir: Sessions directory holding the state file.

    Returns:
        ``{"changes": [...], "added": int, "removed": int, "changed": bool,
        "hosts": int, "ts": float}``; empty diff on any error.
    """
    path = Path(str(sessions_dir)) / STATE_FILENAME
    previous = _load_previous(path)
    current = current_snapshots(world)
    raw = diff_hosts(previous, current)
    changes = [
        {"kind": kind, "host": host, "port": port, "detail": detail}
        for kind, host, port, detail in raw[:MAX_CHANGES_PER_REFRESH]
    ]
    previous_hosts = set(previous)
    current_hosts = set(current)
    payload = {
        "ts": time.time(),
        "hosts": current,
        "last_diff": {
            "changes": changes,
            "detected_at": time.time(),
            "host_new": sorted(current_hosts - previous_hosts)[:200],
            "host_gone": sorted(previous_hosts - current_hosts)[:200],
        },
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        tmp.replace(path)
    except OSError:
        pass
    return {
        "changes": changes,
        "added": len(current_hosts - previous_hosts),
        "removed": len(previous_hosts - current_hosts),
        "changed": bool(changes),
        "hosts": len(current_hosts),
        "ts": payload["ts"],
    }


def last_diff(sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Read the last stored diff without recomputing.

    Args:
        sessions_dir: Sessions directory holding the state file.

    Returns:
        The stored ``last_diff`` payload or ``{"changes": []}``.
    """
    try:
        data = json.loads((Path(str(sessions_dir)) / STATE_FILENAME).read_text(encoding="utf-8"))
        if isinstance(data, dict):
            diff = data.get("last_diff", {})
            return diff if isinstance(diff, dict) else {"changes": []}
    except (OSError, ValueError):
        pass
    return {"changes": []}


def changed_hosts(limit: int = 100, sessions_dir: str | Path = SESSIONS_DIR) -> list[str]:
    """Distinct hosts touched by the last diff, most-recent first.

    Args:
        limit: Row cap.
        sessions_dir: Sessions directory holding the state file.

    Returns:
        List of host addresses.
    """
    out: list[str] = []
    for row in last_diff(sessions_dir).get("changes", []):
        host = str(row.get("host", ""))
        if host and host not in out:
            out.append(host)
        if len(out) >= max(1, limit):
            break
    return out


__all__ = [
    "CHANGE_KINDS",
    "STATE_FILENAME",
    "changed_hosts",
    "current_snapshots",
    "diff_hosts",
    "fingerprint",
    "last_diff",
    "refresh",
    "snapshot_host",
]
