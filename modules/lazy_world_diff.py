"""World-surface diff: host snapshots, change detection, ghost liveness.

The world model stores the *current* campaign truth; this module stores
what a host looked like last time we looked and reports the difference:

- ``host_snapshot`` reads one host out of a world-model dict as a plain,
  canonical snapshot (open services only).
- ``snapshot_fingerprint`` hashes a snapshot so an unchanged host never
  re-triggers.
- ``diff_snapshots`` returns the deterministic change list between two
  snapshots. A product appearing where there was none is nmap
  enrichment, not a change; a flip of an existing identity is.
- Changes append to ``sessions/lazy_changes.jsonl`` (bounded per host,
  prunable) so the report and the loop can read *what moved*.
- Ghost liveness: a host whose name no longer resolves but whose last
  known address still answers is recorded in ``sessions/lazy_ghosts.json``
  so the operator sees the asset is not gone, only unnamed. The probe is
  injectable and every check is read-only.
- ``snapshot_engagement`` appends a daily point-in-time campaign snapshot
  to ``sessions/lazy_stats_history.jsonl``.

Stdlib only. Every entry point degrades silently on missing data and
never raises on untrusted input.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

CHANGES_FILENAME = "lazy_changes.jsonl"
SNAPSHOTS_FILENAME = "lazy_host_snapshots.json"
GHOSTS_FILENAME = "lazy_ghosts.json"
STATS_FILENAME = "lazy_stats_history.jsonl"

HOST_NEW = "host_new"
HOST_RETURNED = "host_returned"
HOST_RETIRED = "host_retired"
PORT_OPENED = "port_opened"
PORT_CLOSED = "port_closed"
SERVICE_CHANGED = "service_changed"
OS_CHANGED = "os_changed"

HOST_CHANGES_PER_HOST = 40
CHANGES_KEEP_DAYS = 90
RECENT_WINDOW_DAYS = 7
GHOST_WEB_PORTS = frozenset({80, 443, 8000, 8008, 8080, 8081, 8443, 8888, 9443, 3000})
GHOST_ENDPOINT_LIMIT = 3
GHOST_CONNECT_TIMEOUT = 3.0
GHOST_MAX_HOSTS = 100
SNAPSHOT_MIN_INTERVAL = 20 * 3600
MAX_HOSTS_PER_DIFF = 2000

_GHOST = "ghost"
_CLEARED = "cleared"


@dataclass(frozen=True)
class SurfaceChange:
    """One deterministic difference between two host snapshots."""

    kind: str
    ip: str
    port: int
    before: dict | None
    after: dict | None


# ----------------------------------------------------------------- snapshots


def host_snapshot(world: dict, ip: str) -> dict:
    """Read one host out of a world-model dict as a canonical snapshot.

    Only open services enter the snapshot so a port that closed is a
    diffable event instead of vanishing silently.

    Args:
        world: World-model dict with a ``hosts`` mapping (dict or list form).
        ip: Host address to snapshot.

    Returns:
        ``{"ip", "state", "os", "ports": {"p/proto": {...}}}``; empty
        dict when the host is absent.
    """
    hosts = world.get("hosts", {}) or {}
    if isinstance(hosts, list):
        hosts = {str(h.get("ip", i)): h for i, h in enumerate(hosts) if isinstance(h, dict)}
    host = hosts.get(ip)
    if not isinstance(host, dict):
        return {}
    ports: dict[str, dict] = {}
    services = host.get("services", {}) or {}
    items = services.items() if isinstance(services, dict) else []
    for port, svc in items:
        svc = svc if isinstance(svc, dict) else {"name": str(svc)}
        if str(svc.get("state", "open")) not in ("", "open"):
            continue
        key = f"{port}/{svc.get('protocol', 'tcp')}"
        ports[key] = {
            "service": str(svc.get("name", "") or ""),
            "product": str(svc.get("product", "") or ""),
            "version": str(svc.get("version", "") or ""),
        }
    return {
        "ip": ip,
        "state": str(host.get("state", "") or ""),
        "os": str(host.get("os_hint", "") or host.get("os", "") or ""),
        "ports": ports,
    }


def snapshot_fingerprint(state: dict) -> str:
    """Hash one snapshot canonically; key order never matters."""
    return hashlib.sha1(json.dumps(state or {}, sort_keys=True).encode()).hexdigest()


def _port_number(key: str) -> int:
    try:
        return int(str(key).split("/")[0])
    except ValueError:
        return 0


def diff_snapshots(before: dict, after: dict) -> list[SurfaceChange]:
    """Deterministic change list between two host snapshots.

    Args:
        before: Prior snapshot (possibly empty).
        after: Current snapshot.

    Returns:
        List of :class:`SurfaceChange` sorted by port number.
    """
    before, after = before or {}, after or {}
    b_ports = before.get("ports", {}) or {}
    a_ports = after.get("ports", {}) or {}
    out: list[SurfaceChange] = []
    keys = sorted(set(b_ports) | set(a_ports), key=lambda k: (_port_number(k), k))
    for key in keys:
        was, now = b_ports.get(key), a_ports.get(key)
        if was is None and now is not None:
            out.append(SurfaceChange(PORT_OPENED, str(after.get("ip", "")), _port_number(key), None, dict(now)))
        elif was is not None and now is None:
            out.append(SurfaceChange(PORT_CLOSED, str(before.get("ip", "")), _port_number(key), dict(was), None))
        elif was is not None and now is not None:
            identity_was = (was.get("service", ""), was.get("product", ""), was.get("version", ""))
            identity_now = (now.get("service", ""), now.get("product", ""), now.get("version", ""))
            if identity_was == identity_now:
                continue
            if not (was.get("product") or was.get("version")):
                continue
            out.append(
                SurfaceChange(SERVICE_CHANGED, str(after.get("ip", "")), _port_number(key), dict(was), dict(now))
            )
    os_was = str(before.get("os", "") or "")
    os_now = str(after.get("os", "") or "")
    if os_was and os_now and os_was != os_now:
        out.append(SurfaceChange(OS_CHANGED, str(after.get("ip", "")), 0, {"os": os_was}, {"os": os_now}))
    return out


# ----------------------------------------------------------------- changes log


def _changes_path(sessions_dir: str | Path) -> Path:
    return Path(str(sessions_dir)) / CHANGES_FILENAME


def _load_changes(sessions_dir: str | Path) -> list[dict]:
    try:
        lines = _changes_path(sessions_dir).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def _as_change(change: SurfaceChange | tuple) -> SurfaceChange:
    """Accept either a SurfaceChange or its (kind, ip, port, before, after) tuple."""
    if isinstance(change, SurfaceChange):
        return change
    kind, ip, port, before, after = (list(change) + [None, None, None, None, None])[:5]
    return SurfaceChange(str(kind), str(ip or ""), int(port or 0), before, after)


def record_changes(changes: list[SurfaceChange], sessions_dir: str | Path, now: float | None = None) -> int:
    """Append changes to the campaign change log, deduped and bounded.

    An entry identical to the host's most recent one is skipped, and a
    host cannot hold more than ``HOST_CHANGES_PER_HOST`` rows.

    Args:
        changes: Diffs from :func:`diff_snapshots` (or equivalent tuples).
        sessions_dir: Sessions directory holding the log.
        now: Override timestamp (epoch seconds).

    Returns:
        How many rows were actually written.
    """
    if not changes:
        return 0
    stamp = float(now if now is not None else time.time())
    existing = _load_changes(sessions_dir)
    latest_by_host: dict[str, dict] = {}
    for row in existing:
        latest_by_host[str(row.get("ip", ""))] = row
    per_host_count: dict[str, int] = {}
    for row in existing:
        per_host_count[str(row.get("ip", ""))] = per_host_count.get(str(row.get("ip", "")), 0) + 1
    fresh: list[dict] = []
    for raw in changes:
        change = _as_change(raw)
        ip = str(change.ip)
        latest = latest_by_host.get(ip, {})
        same = (
            latest.get("kind") == change.kind
            and int(latest.get("port", 0) or 0) == change.port
            and latest.get("after") == change.after
        )
        if same or per_host_count.get(ip, 0) + len(fresh) >= HOST_CHANGES_PER_HOST:
            continue
        fresh.append(
            {
                "kind": change.kind,
                "ip": ip,
                "port": change.port,
                "before": change.before,
                "after": change.after,
                "detected": stamp,
            }
        )
        per_host_count[ip] = per_host_count.get(ip, 0) + 1
    if not fresh:
        return 0
    path = _changes_path(sessions_dir)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            for row in fresh:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        return 0
    return len(fresh)


def recent_changes(sessions_dir: str | Path, days: int = RECENT_WINDOW_DAYS, host: str = "") -> list[dict]:
    """Change rows newest-first within the window, optionally per host."""
    horizon = time.time() - max(0, days) * 24 * 3600
    rows = [row for row in _load_changes(sessions_dir) if float(row.get("detected", 0) or 0) >= horizon]
    if host:
        rows = [row for row in rows if str(row.get("ip", "")) == str(host)]
    rows.sort(key=lambda row: -float(row.get("detected", 0) or 0))
    return rows


def prune_changes(sessions_dir: str | Path, keep_days: int = CHANGES_KEEP_DAYS) -> int:
    """Drop change rows older than ``keep_days``; returns how many."""
    horizon = time.time() - max(0, keep_days) * 24 * 3600
    rows = _load_changes(sessions_dir)
    kept = [row for row in rows if float(row.get("detected", 0) or 0) >= horizon]
    removed = len(rows) - len(kept)
    if removed <= 0:
        return 0
    try:
        _changes_path(sessions_dir).write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in kept), encoding="utf-8"
        )
    except OSError:
        return 0
    return removed


# ----------------------------------------------------------------- snapshots store


def load_host_snapshots(sessions_dir: str | Path) -> dict[str, dict]:
    """Stored per-host snapshots keyed by ip."""
    path = Path(str(sessions_dir)) / SNAPSHOTS_FILENAME
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    hosts = payload.get("hosts", {}) if isinstance(payload, dict) else {}
    return {str(k): v for k, v in hosts.items() if isinstance(v, dict)}


def save_host_snapshots(snapshots: dict[str, dict], sessions_dir: str | Path) -> bool:
    """Persist per-host snapshots atomically-enough (best effort)."""
    path = Path(str(sessions_dir)) / SNAPSHOTS_FILENAME
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"hosts": snapshots, "saved_at": time.time()}, ensure_ascii=False), encoding="utf-8")
    except OSError:
        return False
    return True


def campaign_snapshots(sessions_dir: str | Path) -> dict[str, dict]:
    """Snapshot every world-model host, then diff against stored ones.

    One pass computes current snapshots, diffs them against the stored
    prior snapshots, records the changes and replaces the store.

    Args:
        sessions_dir: Sessions directory (world model + stores).

    Returns:
        ``{"changed": int, "changes": [SurfaceChange-like dicts],
        "snapshots": current snapshots}``.
    """
    root = Path(str(sessions_dir))
    try:
        from modules.world_model import read_state_dict

        world = read_state_dict(root / "world_model.json")
    except Exception:
        world = {}
    hosts = world.get("hosts", {}) or {}
    if isinstance(hosts, list):
        hosts = {str(h.get("ip", i)): h for i, h in enumerate(hosts) if isinstance(h, dict)}
    stored = load_host_snapshots(root)
    current: dict[str, dict] = {}
    changes: list[SurfaceChange] = []
    seen = set()
    for ip in hosts:
        if not str(ip).strip() or len(current) >= MAX_HOSTS_PER_DIFF:
            continue
        snap = host_snapshot(world, str(ip))
        current[str(ip)] = snap
        seen.add(str(ip))
        prior = stored.get(str(ip))
        if prior is None:
            changes.append(SurfaceChange(HOST_NEW, str(ip), 0, None, {"state": snap.get("state", "")}))
            continue
        if snapshot_fingerprint(prior) != snapshot_fingerprint(snap):
            changes.extend(diff_snapshots(prior, snap))
    for ip in stored:
        if ip not in seen:
            changes.append(SurfaceChange(HOST_RETIRED, ip, 0, {"state": stored[ip].get("state", "")}, None))
    recorded = record_changes(changes, root)
    save_host_snapshots(current, root)
    return {
        "changed": recorded,
        "changes": [vars(_as_change(change)) for change in changes],
        "snapshots": current,
    }


# ----------------------------------------------------------------- ghosts


def ghost_endpoints(snapshot: dict, limit: int = GHOST_ENDPOINT_LIMIT) -> list[tuple[str, int, str]]:
    """Web endpoints (ip, port, scheme) a snapshot last had open.

    443 first, then 80, then the rest ascending; non-web ports are not
    probed (the check is an HTTP GET).

    Args:
        snapshot: Snapshot from :func:`host_snapshot`.
        limit: Maximum endpoints returned.

    Returns:
        List of ``(ip, port, scheme)`` triples.
    """
    ip = str((snapshot or {}).get("ip", ""))
    if not ip:
        return []
    found: list[tuple[int, str]] = []
    for key, port in ((snapshot or {}).get("ports", {}) or {}).items():
        number = _port_number(str(key))
        if number <= 0:
            continue
        service = str((port or {}).get("service", "")).lower()
        scheme = "https" if number in (443, 8443, 9443) or "https" in service or "ssl" in service else "http"
        if number in GHOST_WEB_PORTS or "http" in service:
            found.append((number, scheme))
    found.sort(key=lambda item: (0 if item[0] == 443 else 1 if item[0] == 80 else 2, item[0]))
    return [(ip, number, scheme) for number, scheme in found[: max(0, limit)]]


def name_resolves(host: str, resolver: callable | None = None) -> bool:
    """Whether a hostname still resolves (injectable for tests)."""
    if not host:
        return True
    lookup = resolver or _default_resolve
    try:
        return bool(lookup(host))
    except Exception:
        return False


def _default_resolve(host: str) -> bool:
    import socket

    try:
        return bool(socket.gethostbyname(host))
    except OSError:
        return False


def _default_probe(ip: str, port: int, scheme: str, host: str) -> bool:
    import socket
    import urllib.request

    if scheme != "https" and scheme != "http":
        return False
    bracket = f"[{ip}]" if ":" in ip else ip
    try:
        with socket.create_connection((bracket, port), timeout=GHOST_CONNECT_TIMEOUT):
            pass
    except OSError:
        return False
    try:
        request = urllib.request.Request(f"{scheme}://{bracket}:{port}/", headers={"Host": host})
        urllib.request.urlopen(request, timeout=GHOST_CONNECT_TIMEOUT, data=None).read(4096)
        return True
    except Exception:
        return True


def load_ghosts(sessions_dir: str | Path) -> dict:
    """The ghost store ``{"hosts": {...}}`` tolerant of corruption."""
    path = Path(str(sessions_dir)) / GHOSTS_FILENAME
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"hosts": {}}
    if not isinstance(payload, dict) or not isinstance(payload.get("hosts", {}), dict):
        return {"hosts": {}}
    return payload


def ghost_state_apply(host: str, answers: list[str], sessions_dir: str | Path, now: float | None = None) -> dict:
    """Record one ghost observation and return the host's ghost record.

    Answers keep it ghost (``since`` preserved), no answers clear it
    (``cleared_at`` set). Never raises; empty hosts are ignored.

    Args:
        host: Hostname that stopped resolving.
        answers: ``ip:port`` strings that still answered.
        sessions_dir: Sessions directory holding the store.
        now: Override timestamp.

    Returns:
        The updated record for ``host``.
    """
    host = str(host or "").strip()
    if not host:
        return {}
    stamp = float(now if now is not None else time.time())
    payload = load_ghosts(sessions_dir)
    hosts = payload.setdefault("hosts", {})
    record = hosts.get(host) or {}
    if answers:
        if record.get("state") != _GHOST:
            record = {"state": _GHOST, "since": stamp, "answers": [], "cleared_at": None}
        record["answers"] = list(answers)[:8]
        record["last_seen"] = stamp
    else:
        if record.get("state") == _GHOST:
            record["state"] = _CLEARED
            record["cleared_at"] = stamp
            record["answers"] = []
    hosts[host] = record
    path = Path(str(sessions_dir)) / GHOSTS_FILENAME
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return record


def find_ghost_hosts(
    candidates: list[str],
    snapshots: dict[str, dict],
    checker: callable | None = None,
    resolver: callable | None = None,
    cap: int = GHOST_MAX_HOSTS,
) -> dict[str, list[str]]:
    """Which candidate hostnames are ghosts: unresolvable yet answering.

    Args:
        candidates: Hostnames to inspect (from the world model).
        snapshots: Current snapshots by ip.
        checker: ``(ip, port, scheme, host) -> bool`` probe override.
        resolver: ``(host) -> bool`` DNS override.
        cap: Maximum hosts probed per pass.

    Returns:
        ``{host: ["ip:port", ...]}`` for the hosts still answering.
    """
    probe = checker or _default_probe
    out: dict[str, list[str]] = {}
    for host in [str(c) for c in candidates if str(c).strip()][: max(0, cap)]:
        if name_resolves(host, resolver):
            continue
        for ip in snapshots:
            snapshot = snapshots.get(ip) or {}
            answers = []
            for eip, port, scheme in ghost_endpoints(snapshot):
                if probe(eip, port, scheme, host):
                    answers.append(f"{eip}:{port}")
            if answers:
                out[host] = answers
                break
    return out


# ----------------------------------------------------------------- stats history


def snapshot_engagement(sessions_dir: str | Path, now: float | None = None, world: dict | None = None) -> dict | None:
    """Append one daily campaign snapshot when the cooldown allows.

    Args:
        sessions_dir: Sessions directory holding the history file.
        now: Override timestamp.
        world: Pre-loaded world-model dict override.

    Returns:
        The snapshot written, or None when one was taken recently.
    """
    root = Path(str(sessions_dir))
    stamp = float(now if now is not None else time.time())
    path = root / STATS_FILENAME
    rows: list[dict] = []
    try:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, ValueError):
        rows = []
    rows = [row for row in rows if isinstance(row, dict)]
    if rows and stamp - float(rows[-1].get("ts", 0) or 0) < SNAPSHOT_MIN_INTERVAL:
        return None
    if world is None:
        try:
            from modules.world_model import read_state_dict

            world = read_state_dict(root / "world_model.json")
        except Exception:
            world = {}
    hosts = world.get("hosts", {}) or {}
    if isinstance(hosts, list):
        hosts = {str(h.get("ip", i)): h for i, h in enumerate(hosts) if isinstance(h, dict)}
    owned = 0
    with_services = 0
    for entry in hosts.values():
        if not isinstance(entry, dict):
            continue
        state = str(entry.get("state", ""))
        if state in ("owned", "root", "system", "shell"):
            owned += 1
        services = entry.get("services", {}) or {}
        if isinstance(services, dict) and services:
            with_services += 1
    vulns: list[dict] = []
    raw_vulns = world.get("vulnerabilities", []) or []
    for row in raw_vulns:
        if isinstance(row, dict):
            vulns.append(row)
    by_severity: dict[str, int] = {}
    for row in vulns:
        severity = str(row.get("severity", "unknown")).lower() or "unknown"
        by_severity[severity] = by_severity.get(severity, 0) + 1
    heat_counts = {"hot": 0, "warm": 0, "cold": 0}
    try:
        summary = json.loads((root / "intel_summary.json").read_text(encoding="utf-8"))
        heat_counts.update(summary.get("heat_counts", {}) or {})
    except (OSError, ValueError):
        pass
    change_rows = _load_changes(root)
    snapshot = {
        "date": time.strftime("%Y-%m-%d", time.gmtime(stamp)),
        "ts": stamp,
        "hosts": len(hosts),
        "owned": owned,
        "with_services": with_services,
        "findings": by_severity,
        "cve_heat": heat_counts,
        "changes_logged": len(change_rows),
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(snapshot, ensure_ascii=False) + "\n")
    except OSError:
        return None
    return snapshot


__all__ = [
    "BASE_DIR",
    "CHANGES_FILENAME",
    "GHOSTS_FILENAME",
    "GHOST_ENDPOINT_LIMIT",
    "HOST_NEW",
    "HOST_RETIRED",
    "HOST_RETURNED",
    "OS_CHANGED",
    "PORT_CLOSED",
    "PORT_OPENED",
    "SERVICE_CHANGED",
    "SNAPSHOTS_FILENAME",
    "STATS_FILENAME",
    "SurfaceChange",
    "campaign_snapshots",
    "diff_snapshots",
    "find_ghost_hosts",
    "ghost_endpoints",
    "ghost_state_apply",
    "host_snapshot",
    "load_ghosts",
    "load_host_snapshots",
    "name_resolves",
    "prune_changes",
    "recent_changes",
    "record_changes",
    "save_host_snapshots",
    "snapshot_engagement",
    "snapshot_fingerprint",
]
