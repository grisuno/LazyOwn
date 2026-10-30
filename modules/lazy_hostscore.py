"""Host heat score: deterministic 0-100 priority for every known host.

Deterministic pre-classification for plan prioritisation: CVEs that
have named a service at 0.55+ EPSS or have KEV coverage are hot, warm
tiers are CVE HOTWARM; add certainty points for confirmed vulnerabilities and shell ownership; downgrade what the host already had since
the last scan; cap per category and keep the reason list so a score can
be audited. Pure function first (like the frameworks keep their scoring
auditable), persistence second, wrapper last.

Stdlib only. Never raises on untrusted snapshots; missing inputs cost
zero.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

CVE_POINTS = {"hot": 40, "warm": 20, "cold": 5}
CVE_CAP = 50
FINDING_POINTS = {"critical": 25, "high": 25, "medium": 10, "low": 3}
FINDINGS_CAP = 40
SHELL_BONUS = 15
EXPOSURE_POINTS = 10
RECENCY_CAP = 10
SCORE_FILENAME = "host_scores.json"

_ADMIN_PATH_RE = re.compile(r"/(admin|manage|manager|phpmyadmin|wp-admin)", re.IGNORECASE)


def score_host(inputs: dict[str, Any]) -> tuple[int, list[dict[str, Any]]]:
    """Score one host from plain-dict inputs.

    Args:
        inputs: ``{"services": [{"port","name","version"}],
            "findings": [{"severity","state","text"}], "shell": bool,
            "cves": [{"heat"}], "admin_paths": [str], "recency": float}``

    Returns:
        ``(score, detail)`` where detail is the ordered list of
        ``{label, points}`` lines.
    """
    detail: list[dict[str, Any]] = []
    total = 0

    def _add(label: str, points: int) -> None:
        nonlocal total
        total += points
        detail.append({"label": label, "points": points})

    heat_rank: dict[str, int] = {}
    for cve in inputs.get("cves", []) or []:
        row = cve if isinstance(cve, dict) else {}
        heat = "hot" if row.get("kev") else str(row.get("heat", ""))
        if not heat:
            continue
        heat_rank[heat] = max(heat_rank.get(heat, 0), {"hot": 3, "warm": 2, "cold": 1}.get(heat, 1))
    if heat_rank:
        heaviest = max(heat_rank.items(), key=lambda item: item[1])[0]
        _add(f"cve heat {heaviest}", min(CVE_CAP, CVE_POINTS.get(heaviest, 0)))

    counted: dict[str, int] = {}
    findings_subtotal = 0
    for finding in inputs.get("findings", []) or []:
        row = finding if isinstance(finding, dict) else {}
        severity = str(row.get("severity", "")).lower()
        if str(row.get("status", "")).lower() == "discarded":
            continue
        counted[severity] = counted.get(severity, 0) + 1
    if counted.get("critical"):
        findings_subtotal += FINDING_POINTS["critical"]
    if counted.get("high"):
        findings_subtotal += FINDING_POINTS["high"]
    if counted.get("medium"):
        findings_subtotal += FINDING_POINTS["medium"]
    if findings_subtotal:
        findings_capped = min(FINDINGS_CAP, findings_subtotal)
        labels = ", ".join(f"severity {k} x{v}" for k, v in sorted(counted.items()))
        _add(labels, findings_capped)

    if inputs.get("shell"):
        _add("shell foothold", SHELL_BONUS)
    if inputs.get("admin_paths"):
        _add("admin surface open", EXPOSURE_POINTS)
    recency = inputs.get("recency", 0.0) or 0.0
    if 0 < float(recency) <= 7 * 86400.0:
        _add("changed this week", RECENCY_CAP)

    score = min(100, total)
    return score, detail


def rescore(
    sessions_dir: str | Path | None = None,
    allow_network: bool = False,
    now: float | None = None,
) -> dict[str, dict[str, Any]]:
    """Score the whole world model and persist the table result.

    Args:
        sessions_dir: Sessions directory override.
        allow_network: Let CVE correlation use network feeds when a
            cache is cold; default stays offline-only.
        now: Reference epoch; defaults to current time.

    Returns:
        ``{host: {"score", "detail"}}`` for every host the snapshot
        carries, empty on any failure.
    """
    try:
        from modules.world_model import get_world_model

        snapshot = get_world_model().snapshot()
    except Exception:
        return {}
    try:
        from modules.lazy_world_diff import recent_changes as world_recent

        recent = world_recent(sessions_dir or "sessions", days=7)
    except Exception:
        recent = []
    recent_hosts = {str(row.get("ip", "")) for row in recent if row.get("ip")}
    out: dict[str, dict[str, Any]] = {}
    try:
        from modules.lazy_cve_feed import correlate

        feeds = allow_network
        for ip, host in (snapshot.get("hosts", {}) or {}).items():
            if not isinstance(host, dict):
                continue
            services = [
                {
                    "name": str((svc or {}).get("name", "")),
                    "version": str((svc or {}).get("version", "") or (svc or {}).get("name", "")),
                    "port": str(port),
                }
                for port, svc in (host.get("services", {}) or {}).items()
                if isinstance(svc, dict) and svc.get("state", "open") in ("open", "", "unknown")
            ]
            cves = []
            if services or feeds is not None:
                for service in services[:8]:
                    product = service["version"] or service["name"]
                    if not product:
                        continue
                    try:
                        cves.extend(correlate(product, service["version"], allow_network=bool(feeds))[:3])
                    except Exception:
                        continue
            findings = [
                {
                    "severity": str(vuln.get("severity", "")),
                    "status": str(vuln.get("status", "")),
                    "text": str(vuln.get("summary", "")),
                }
                for vuln in (snapshot.get("vulnerabilities", []) or [])
                if str(vuln.get("host", "")) == ip
            ]
            admin_paths = [note for note in (host.get("notes", []) or []) if _ADMIN_PATH_RE.search(str(note))]
            inputs = {
                "services": services,
                "findings": findings,
                "cves": cves[:3],
                "shell": str((host.get("state", "") or "")).lower() == "owned",
                "admin_paths": bool(admin_paths),
                "recency": 1.0 if ip in recent_hosts else 0.0,
            }
            score, detail = score_host(inputs)
            out[str(ip)] = {"score": score, "detail": detail}
    except Exception:
        return {}
    try:
        _persist(out, sessions_dir, now)
    except Exception:
        pass
    return out


def _persist(table: dict[str, dict[str, Any]], sessions_dir: str | Path | None, now: float | None) -> None:
    """Write the bounded host score table under sessions/lazy."""
    path = Path(str(sessions_dir or "sessions")) / "lazy" / SCORE_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ts": float(now if now is not None else time.time()),
        "hosts": table,
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def load_scores(sessions_dir: str | Path | None = None) -> dict[str, float]:
    """Return the persisted per-host scores.

    Args:
        sessions_dir: Sessions directory override.

    Returns:
        ``{host: score}``; empty when the file is absent or stale.
    """
    try:
        path = Path(str(sessions_dir or "sessions")) / "lazy" / SCORE_FILENAME
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return {
                str(host): float(row.get("score", 0.0))
                for host, row in (payload.get("hosts") or {}).items()
                if isinstance(row, dict)
            }
    except Exception:
        return {}
    return {}


__all__ = [
    "CVE_CAP",
    "CVE_POINTS",
    "FINDINGS_CAP",
    "FINDING_POINTS",
    "RECENCY_CAP",
    "SCORE_FILENAME",
    "SHELL_BONUS",
    "score_host",
    "rescore",
    "load_scores",
]
