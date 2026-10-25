"""Async target enrichment with scan dedup (LAZY enrich parity).

LAZY ``enrich/enrich.go`` runs DNS + HTTP jobs off the hot path with a
4-worker pool, 1024 queue and 5-minute cooldown. This port provides the
same shape in stdlib Python: a small thread-pool engine plus
:func:`should_rescan`, which stops the loop re-running nmap when
``sessions/scan_<target>.nmap*`` already holds fresh results.
"""

from __future__ import annotations

import socket
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path


WORKERS = 4
QUEUE_SIZE = 1024
COOLDOWN_SEC = 300.0
DNS_TIMEOUT_SEC = 4.0
HTTP_TIMEOUT_SEC = 12.0
SCAN_FRESH_SEC = 3600.0


@dataclass
class EnrichResult:
    """One enrichment outcome for a target."""

    target: str
    ips: list[str] = field(default_factory=list)
    ports: list[int] = field(default_factory=list)
    http_attrs: dict = field(default_factory=dict)
    dns_attrs: dict = field(default_factory=dict)


def scan_files_for(sessions_dir: str | Path, target: str) -> list[Path]:
    """Return existing scan artefacts for a target."""
    base = Path(str(sessions_dir))
    safe = "".join(c for c in str(target) if c.isalnum() or c in ".-_")
    out: list[Path] = []
    for suffix in (".nmap", ".nmap.xml", ".xml", ".gnmap"):
        candidate = base / f"scan_{safe}{suffix}"
        if candidate.exists():
            out.append(candidate)
    out.extend(sorted(base.glob(f"scan_{safe}*.nmap*")))
    seen: list[Path] = []
    for path in out:
        if path not in seen:
            seen.append(path)
    return seen


def should_rescan(sessions_dir: str | Path, target: str,
                  fresh_sec: float = SCAN_FRESH_SEC) -> bool:
    """Return True when no fresh scan artefact exists for target."""
    files = scan_files_for(sessions_dir, target)
    if not files:
        return True
    now = time.time()
    for path in files:
        try:
            if now - path.stat().st_mtime < fresh_sec:
                return False
        except OSError:
            continue
    return True


def resolve_dns(target: str, timeout: float = DNS_TIMEOUT_SEC) -> dict:
    """Resolve A/AAAA for a target with a bounded timeout."""
    old = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        _, _, addrs = socket.gethostbyname_ex(str(target))
        return {"a": list(addrs)}
    except (socket.gaierror, socket.timeout, OSError):
        return {"a": []}
    finally:
        socket.setdefaulttimeout(old)


def fetch_http(target: str, timeout: float = HTTP_TIMEOUT_SEC) -> dict:
    """Fetch HTTP headers for a target without following credentials."""
    for scheme in ("http://", "https://"):
        try:
            req = urllib.request.Request(scheme + str(target), method="HEAD")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return {"scheme": scheme.rstrip("://"),
                        "status": int(resp.status),
                        "server": resp.headers.get("Server", "")[:128]}
        except Exception:
            continue
    return {}


class EnrichEngine:
    """Bounded async enrichment pool (LAZY Engine parity)."""

    def __init__(self, max_workers: int = WORKERS) -> None:
        """Create the pool and cooldown index."""
        self._pool = ThreadPoolExecutor(max_workers=max(1, int(max_workers)))
        self._lock = threading.Lock()
        self._last: dict[str, float] = {}
    def submit(self, target: str) -> bool:
        """Queue DNS+HTTP enrichment unless inside cooldown."""
        key = str(target or "").strip().lower()
        if not key:
            return False
        now = time.time()
        with self._lock:
            if now - self._last.get(key, 0.0) < COOLDOWN_SEC:
                return False
            self._last[key] = now
        self._pool.submit(self._run, key)
        return True

    def _run(self, target: str) -> EnrichResult:
        """Execute DNS then HTTP enrichment for one target."""
        dns = resolve_dns(target)
        http = fetch_http(target)
        return EnrichResult(target=target, ips=list(dns.get("a", [])),
                            dns_attrs=dns, http_attrs=http)

    def shutdown(self, wait: bool = False) -> None:
        """Shut the pool down without blocking the loop by default."""
        self._pool.shutdown(wait=wait)


_SHARED_ENGINE: EnrichEngine | None = None
_SHARED_ENGINE_LOCK = threading.Lock()


def shared_engine() -> EnrichEngine:
    """Return the process-wide enrichment engine (LAZY parity).

    One pool serves both flows; per-target cooldown dedups submissions
    so enrichment never blocks the hot path.
    """
    global _SHARED_ENGINE
    with _SHARED_ENGINE_LOCK:
        if _SHARED_ENGINE is None:
            _SHARED_ENGINE = EnrichEngine()
        return _SHARED_ENGINE


__all__ = [
    "WORKERS", "QUEUE_SIZE", "COOLDOWN_SEC", "SCAN_FRESH_SEC",
    "EnrichResult", "scan_files_for", "should_rescan",
    "resolve_dns", "fetch_http", "EnrichEngine", "shared_engine",
]
