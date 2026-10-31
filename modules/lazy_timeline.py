"""Lazy engagement timeline for LazyOwn.

Snapshots the world model between rounds and diffs them: new hosts, gone
hosts, opened ports, closed ports, version changes and state changes.
When a DNS name stops resolving while the host still answers, the diff
flags a zombie host (retired infrastructure that kept serving), which in
an engagement is signal worth reading first.

Snapshots live under ``sessions/timeline/`` with bounded retention.
Stdlib only; every entry point degrades to an empty result on errors.
"""

from __future__ import annotations

import json
import socket
import time
from pathlib import Path

from modules.world_model import read_state_dict

BASE_DIR = Path(__file__).resolve().parent.parent
SNAPSHOT_DIR = BASE_DIR / "sessions" / "timeline"
KEEP_SNAPSHOTS = 20

KIND_HOST_NEW = "host_new"
KIND_HOST_GONE = "host_gone"
KIND_PORT_OPENED = "port_opened"
KIND_PORT_CLOSED = "port_closed"
KIND_VERSION_CHANGED = "version_changed"
KIND_STATE_CHANGED = "state_changed"

RECENT_CHANGE_KINDS = (KIND_PORT_OPENED, KIND_VERSION_CHANGED, KIND_STATE_CHANGED)


def resolve_hostnames(names: list[str], resolver=None) -> dict[str, str]:
    """Resolve candidate hostnames for the snapshot DNS record.

    Args:
        names: Hostnames or FQDNs to track.
        resolver: Optional ``name -> ip or ''`` override for tests.

    Returns:
        ``{name: ip}`` for the names that resolved, empty string entry
        for the rest.
    """
    wrapped = resolver or _getaddrinfo_resolver
    tracked: dict[str, str] = {}
    for name in names:
        cleaned = str(name or "").strip()
        if not cleaned:
            continue
        try:
            tracked[cleaned] = wrapped(cleaned)
        except OSError:
            tracked[cleaned] = ""
    return tracked


def _getaddrinfo_resolver(name: str) -> str:
    """Stdlib resolver returning the first IPv4 answer as a string."""
    answers = socket.getaddrinfo(name, None, family=socket.AF_INET, type=socket.SOCK_STREAM)
    return answers[0][4][0] if answers else ""


def record(
    state_path: str | Path | None = None,
    snaps_dir: str | Path | None = None,
    keep: int = KEEP_SNAPSHOTS,
    dns: dict[str, str] | None = None,
) -> dict:
    """Snapshot the current world model (internally, never raises).

    Args:
        state_path: Optional world model state path override.
        snaps_dir: Optional snapshot directory override.
        keep: Maximum snapshots retained (oldest pruned).
        dns: Optional ``{name: ip}`` map from :func:`resolve_hostnames`.

    Returns:
        ``{"path": path written or None, "hosts": n, "dns": recorded map}``;
        a dict with a None path records nothing.
    """
    try:
        state = read_state_dict(Path(state_path) if state_path else _default_state_path())
    except (OSError, ValueError, KeyError):
        state = {}
    hosts = _extract_hosts(state)
    snapshot = {
        "ts": time.time(),
        "hosts": hosts,
        "dns": dns or {},
    }
    directory = Path(snaps_dir or SNAPSHOT_DIR)
    path = None
    try:
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"snap_{int(snapshot['ts'] * 1000)}.json"
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(snapshot, indent=2, default=str), encoding="utf-8")
        tmp.replace(path)
    except OSError:
        return {"path": None, "hosts": 0, "dns": {}}
    try:
        _prune(find_snapshots(directory), keep)
    except OSError:
        pass
    return {"path": str(path), "hosts": len(hosts), "dns": snapshot["dns"]}


def record_quiet(
    state_path: str | Path | None = None,
    snaps_dir: str | Path | None = None,
    keep: int = KEEP_SNAPSHOTS,
    dns: dict[str, str] | None = None,
) -> dict:
    """Snapshot for the autonomous loop: same as record(), never raises.

    Args:
        state_path: Optional world model state path override.
        snaps_dir: Optional snapshot directory override.
        keep: Maximum snapshots retained (oldest pruned).
        dns: Optional ``{name: ip}`` map from :func:`resolve_hostnames`.

    Returns:
        The :func:`record` result dict, or ``{"path": None, "hosts": 0,
        "dns": {}}`` when anything failed.
    """
    try:
        return record(state_path=state_path, snaps_dir=snaps_dir, keep=keep, dns=dns)
    except Exception:
        return {"path": None, "hosts": 0, "dns": {}}


def find_snapshots(snaps_dir: str | Path | None = None) -> list[Path]:
    """List snapshot files oldest first.

    Args:
        snaps_dir: Optional directory override.

    Returns:
        Sorted snapshot paths (empty when none).
    """
    directory = Path(snaps_dir or SNAPSHOT_DIR)
    try:
        return sorted(directory.glob("snap_*.json"))
    except OSError:
        return []


def diff(_old: dict | Path | str, _new: dict | Path | str) -> dict:
    """Diff two world-model snapshots.

    Args:
        _old: Earlier snapshot dict or file path.
        _new: Later snapshot dict or file path.

    Returns:
        ``{"changes": [{"kind", "host", "port", "detail"}...] (oldest
        steady order), "zombies": [ip], "a_ts", "b_ts"}``. Unreadable
        inputs degrade to empty results.
    """
    a = _load(_old)
    b = _load(_new)
    if not a or not b:
        return {"changes": [], "zombies": [], "a_ts": None, "b_ts": None}
    a_hosts = a.get("hosts") or {}
    b_hosts = b.get("hosts") or {}
    changes: list[dict] = []
    for ip in sorted(set(a_hosts) - set(b_hosts)):
        changes.append({"kind": KIND_HOST_GONE, "host": ip, "port": 0, "detail": "host disappeared from the world model"})
    for ip in sorted(set(b_hosts) - set(a_hosts)):
        changes.append({"kind": KIND_HOST_NEW, "host": ip, "port": 0, "detail": "new host in the world model"})
    for ip in sorted(set(a_hosts) & set(b_hosts)):
        changes.extend(_host_diff(ip, a_hosts[ip], b_hosts[ip]))
    zombies = _zombies(a, b)
    return {"changes": changes, "zombies": zombies, "a_ts": a.get("ts"), "b_ts": b.get("ts")}


def show(snaps_dir: str | Path | None = None, last: int = 3) -> list[dict]:
    """Summarize the newest snapshots.

    Args:
        snaps_dir: Optional directory override.
        last: How many recent snapshots to summarize.

    Returns:
        One summary dict per snapshot: ``{"path", "ts", "hosts", "services"}``.
    """
    out: list[dict] = []
    for path in find_snapshots(snaps_dir)[-last:]:
        snap = _load(path)
        if not snap:
            continue
        services = sum(len(host.get("services") or {}) for host in (snap.get("hosts") or {}).values())
        out.append({"path": str(path), "ts": snap.get("ts"), "hosts": len(snap.get("hosts") or {}), "services": services})
    return out


def _default_state_path() -> Path:
    """Return the default encrypted world model path."""
    from modules.world_model import WORLD_MODEL_PATH as STATE_PATH

    return Path(STATE_PATH)


def _extract_hosts(state: dict) -> dict[str, dict]:
    """Project the world-model state onto snapshot shape."""
    hosts = state.get("hosts") if isinstance(state, dict) else None
    if not isinstance(hosts, dict):
        return {}
    shaped: dict[str, dict] = {}
    for ip, host in hosts.items():
        if not isinstance(host, dict):
            continue
        services: dict[str, dict] = {}
        for port, svc in (host.get("services") or {}).items():
            if not isinstance(svc, dict):
                continue
            services[str(port)] = {
                "name": str(svc.get("name") or svc.get("service_name") or "").strip(),
                "version": str(svc.get("version") or "").strip(),
                "state": str(svc.get("state") or "open"),
            }
        shaped[str(ip)] = {"state": str(host.get("state") or ""), "services": services}
    return shaped


def _host_diff(ip: str, before: dict, after: dict) -> list[dict]:
    """Diff one host entry between two snapshots."""
    changes: list[dict] = []
    before_services = before.get("services") or {}
    after_services = after.get("services") or {}
    for port in sorted(set(before_services) - set(after_services)):
        changes.append({"kind": KIND_PORT_CLOSED, "host": ip, "port": int(port) if port.isdigit() else 0, "detail": "service no longer open"})
    for port in sorted(set(after_services) - set(before_services)):
        changes.append({"kind": KIND_PORT_OPENED, "host": ip, "port": int(port) if port.isdigit() else 0, "detail": "service appeared"})
    for port in sorted(set(after_services) & set(before_services)):
        old = before_services[port] or {}
        new = after_services[port] or {}
        if str(old.get("version")) != str(new.get("version")) and str(new.get("version")):
            changes.append({
                "kind": KIND_VERSION_CHANGED,
                "host": ip,
                "port": int(port) if port.isdigit() else 0,
                "detail": f"{str(old.get('version') or '?')} -> {str(new.get('version') or '?')}",
            })
    if str(before.get("state") or "") != str(after.get("state") or ""):
        changes.append({
            "kind": KIND_STATE_CHANGED,
            "host": ip,
            "port": 0,
            "detail": f"{str(before.get('state') or '?')} -> {str(after.get('state') or '?')}",
        })
    return changes


def _zombies(_old_snapshot: dict, snapshot: dict) -> list[str]:
    """Hosts whose DNS name stopped resolving while services still answer.

    The DNS map of the later snapshot is the truth: a name that resolved
    before and is unresolved now marks the previously answered address as
    a zombie when the world model still shows services on it.

    Args:
        _old_snapshot: Earlier snapshot providing the previous mapping.
        snapshot: Current snapshot with the fresh DNS record and hosts.

    Returns:
        Zombie host IPs sorted.
    """
    if dns_map := (snapshot.get("dns") or {}):
        dead = [name for name, address in dns_map.items() if not str(address or "").strip()]
    else:
        dead = []
    if not dead:
        return []
    old_dns = _old_snapshot.get("dns") or {}
    previous = {name: value for name, value in old_dns.items() if str(value or "").strip()}
    zombies: set[str] = set()
    hosts = snapshot.get("hosts") or {}
    for name in dead:
        address = str(previous.get(name) or "").strip()
        if not address:
            continue
        host = hosts.get(address)
        if isinstance(host, dict) and host.get("services"):
            zombies.add(address)
    return sorted(zombies)


def _prune(paths: list[Path], keep: int) -> None:
    """Remove oldest snapshots beyond the retention bound."""
    for path in paths[: max(0, len(paths) - keep)]:
        try:
            path.unlink()
        except OSError:
            continue


def _load(source: dict | Path | str) -> dict:
    """Load a snapshot from a dict input or a file path."""
    if isinstance(source, dict):
        return source
    try:
        data = json.loads(Path(source).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


__all__ = [
    "KIND_HOST_GONE",
    "KIND_HOST_NEW",
    "KIND_PORT_CLOSED",
    "KIND_PORT_OPENED",
    "KIND_STATE_CHANGED",
    "KIND_VERSION_CHANGED",
    "KEEP_SNAPSHOTS",
    "RECENT_CHANGE_KINDS",
    "SNAPSHOT_DIR",
    "diff",
    "find_snapshots",
    "record",
    "record_quiet",
    "resolve_hostnames",
    "show",
]
