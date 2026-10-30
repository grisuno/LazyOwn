"""Shared selector for the best vetted chain given phase, platform and services.

Both the autonomous daemon's ChainSelector and the LazyLoopEngine planner need
to answer the same question -- "which chain under ``chains/`` fits what we have
discovered right now?" -- so the scoring rules live here once and both callers
delegate to :func:`best_chain`. Selection is evidence-based: a chain scores zero
unless at least one of its tags matches a discovered service, so a chain is never
proposed blindly. Phase affinity only re-ranks already service-matched chains.
Lab and gym chains are excluded unless ``allow_lab`` is set, keeping autonomous
runs focused on real adversary emulation rather than range-specific recipes.
"""

from __future__ import annotations

import threading
import time
from typing import Any

STRATEGIC_PHASES = frozenset({"exploit", "lateral", "privesc", "cred", "c2", "postexp"})
LAB_TAGS = frozenset({"gym", "lab", "ad-lab", "metasploitable2", "ms2"})
SERVICE_TAG_ALIASES: dict[str, str] = {
    "microsoft-ds": "smb",
    "netbios-ssn": "smb",
    "netbios-dgm": "smb",
    "samba": "smb",
    "ms-wbt-server": "rdp",
    "domain": "dns",
    "ldap": "ad",
    "kerberos-sec": "ad",
    "https": "http",
}
PHASE_AFFINITY: dict[str, frozenset[str]] = {
    "cred": frozenset({"credentials", "creds", "ad"}),
    "lateral": frozenset({"ad", "lateral", "smb", "winbox"}),
    "privesc": frozenset({"privesc", "kernel", "ad"}),
    "exploit": frozenset({"web", "http", "exploit"}),
    "c2": frozenset({"c2", "beacon", "apt"}),
    "postexp": frozenset({"persistence", "exfil", "apt"}),
}

_DEFAULT_TTL = 60.0
_CACHE_LOCK = threading.Lock()
_CACHE: dict[str, Any] = {"rows": [], "ts": 0.0, "allow_lab": None}


def normalize_tags(tags: Any) -> list[str]:
    """Return a chain's tags lowercased and aliased to the shared vocabulary.

    Chain tags and discovered service names pass through the same alias map
    (``samba`` -> ``smb``, ``https`` -> ``http``, ...) so a tag and a service
    name that mean the same thing compare equal. Lab markers (``gym``,
    ``ad-lab``) are not aliased and survive for the lab exclusion filter.
    """
    out: list[str] = []
    for tag in tags or []:
        name = str(tag).strip().lower()
        if name:
            out.append(SERVICE_TAG_ALIASES.get(name, name))
    return out


def service_tokens(services: Any) -> set[str]:
    """Normalise discovered service names into the chain tag vocabulary."""
    tokens: set[str] = set()
    for svc in services or []:
        name = str(svc).strip().lower()
        if name:
            tokens.add(SERVICE_TAG_ALIASES.get(name, name))
    return tokens


def platform_ok(platforms: Any, os_hint: str) -> bool:
    """Return True when a chain's platforms admit the target OS hint."""
    declared = {str(p).strip().lower() for p in (platforms or []) if str(p).strip()}
    if not declared:
        return True
    hint = str(os_hint or "").strip().lower()
    if hint in ("", "unknown", "any"):
        return True
    return hint in declared


def score(tags: set[str], phase: str, svc_tokens: set[str]) -> int:
    """Score one chain's tags for the phase and discovered services.

    A chain scores zero without a service-tag match, so nothing is proposed
    blindly; phase affinity only boosts a chain that already matched a service.
    """
    service_hits = len(tags & svc_tokens)
    if service_hits == 0:
        return 0
    return 2 * service_hits + len(tags & PHASE_AFFINITY.get(phase, frozenset()))


def reset_cache() -> None:
    """Clear the process-wide registry scan cache (tests, long-lived loops)."""
    with _CACHE_LOCK:
        _CACHE["rows"] = []
        _CACHE["ts"] = 0.0
        _CACHE["allow_lab"] = None


def load_rows(allow_lab: bool = False, ttl: float = _DEFAULT_TTL) -> list[dict]:
    """Return enabled, valid, non-lab chain rows, cached for the TTL.

    Args:
        allow_lab: Keep lab/gym chains when True.
        ttl: Seconds the cached scan stays valid.

    Returns:
        List of ``chain_registry.scan_all`` rows after filtering.
    """
    now = time.time()
    with _CACHE_LOCK:
        fresh = (now - float(_CACHE["ts"])) < max(0.0, float(ttl))
        if _CACHE["rows"] and fresh and _CACHE["allow_lab"] == bool(allow_lab):
            return list(_CACHE["rows"])
    try:
        from modules.chain_registry import scan_all

        rows = [row for row in scan_all() if row.get("valid") and row.get("enabled")]
    except Exception:
        rows = []
    if not allow_lab:
        rows = [row for row in rows if not (set(normalize_tags(row.get("tags"))) & LAB_TAGS)]
    with _CACHE_LOCK:
        _CACHE["rows"] = list(rows)
        _CACHE["ts"] = now
        _CACHE["allow_lab"] = bool(allow_lab)
    return rows


def best_chain(
    phase: str,
    os_hint: str,
    services: Any,
    exclude: Any = (),
    allow_lab: bool = False,
    rows: list[dict] | None = None,
    ttl: float = _DEFAULT_TTL,
) -> tuple[str, str] | None:
    """Return the ``(name, reason)`` of the best matching chain, or None.

    Args:
        phase: Current kill-chain phase; only strategic phases match.
        os_hint: Target OS hint (``linux``/``windows``/...); blank means any.
        services: Discovered service names for the target.
        exclude: Chain names already proposed, skipped to avoid repeats.
        allow_lab: Include lab/gym chains when True.
        rows: Pre-loaded registry rows (tests); None loads via cached scan.
        ttl: Cache TTL seconds when ``rows`` is None.

    Returns:
        The highest-scoring eligible chain as ``(name, reason)``, or None when
        the phase is non-strategic or nothing scores on a service match.
    """
    if phase not in STRATEGIC_PHASES:
        return None
    excluded = {str(name) for name in (exclude or [])}
    svc_tokens = service_tokens(services)
    if not svc_tokens:
        return None
    candidates = rows if rows is not None else load_rows(allow_lab=allow_lab, ttl=ttl)
    best: dict | None = None
    best_score = 0
    for row in candidates:
        name = str(row.get("name", "") or "")
        if not name or name in excluded:
            continue
        if not platform_ok(row.get("platforms"), os_hint):
            continue
        row_score = score(set(normalize_tags(row.get("tags"))), phase, svc_tokens)
        if row_score > best_score:
            best, best_score = row, row_score
    if best is None or best_score < 1:
        return None
    name = str(best["name"])
    matched = sorted(set(normalize_tags(best.get("tags"))) & svc_tokens)
    return name, f"vetted chain {name} matches {phase} on service(s) {','.join(matched)}"


__all__ = [
    "LAB_TAGS",
    "PHASE_AFFINITY",
    "SERVICE_TAG_ALIASES",
    "STRATEGIC_PHASES",
    "best_chain",
    "load_rows",
    "normalize_tags",
    "platform_ok",
    "reset_cache",
    "score",
    "service_tokens",
]
