"""Target exposure report for LazyOwn.

Binds the discovered world-model services to a local exploit feed with
hard-evidence policy, ranks the result by exploitation heat, scores the
host 0-100 and renders read-only validation commands for the top matches.

Report artefact lives at ``sessions/lazy_intel_<target>.json``; every
generation also publishes one ``lazy_intel`` event through
:mod:`modules.outcome_bus` so the world model, C2 surfaces, intel graph
and reports stay consistent with the fan-out contract; the deduped
store sink ``modules.sinks.lazy_intel`` mirrors bounded matches into
the world model and the SQLite workspace.

Feed rows come from :mod:`modules.lazy_feedmatch`; heat tiers from
:mod:`modules.lazy_heat` (the single vocabulary); probe rendering from
:mod:`modules.lazy_probes`.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from modules import lazy_feedmatch
from modules.lazy_feedmatch import (
    EVIDENCE_IN_RANGE,
    EVIDENCE_UNBOUNDED,
    Sighting,
    bind_sighting,
    feed_fingerprint,
    unversioned_leads,
)
from modules.lazy_heat import (
    COLD,
    HOT,
    SEVERITY_FROM_HEAT,
    WARM,
    heat_rank,
    host_heat,
)
from modules.lazy_probes import CHECK_VERSION_BANNER, render_check

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
REPORT_PREFIX = "lazy_intel_"
WORLD_MODEL_PATH = SESSIONS_DIR / "world_model.json"

SCORE_CVE_CAP = 50
SCORE_UNBOUNDED_CAP = 2
SCORE_SURFACE_CAP = 10
MAX_CHECKS = 3


def ensure_report(target: str, entries: list[dict] | dict | None = None, refresh: bool = False) -> Path | None:
    """Create the target exposure report if absent (loop bootstrap path).

    Generates one report through :func:`generate_report` with the saved
    file reused when present (pass ``refresh`` to re-run anyway), then
    persists and publishes it, so the fire-pending selector and the
    loop share one artefact path: ``sessions/lazy_intel_<target>.json``.

    Args:
        target: Host address.
        entries: Optional live feed rows override; empty falls back to
            the local feed then the keyless live bundle.
        refresh: Regenerate even when a report already exists.

    Returns:
        The report path, or None when the target is empty or nothing
        could be written.
    """
    clean = str(target or "").strip()
    if not clean:
        return None
    if not refresh:
        existing = SESSIONS_DIR / f"{REPORT_PREFIX}{clean}.json"
        if existing.exists():
            return existing
    try:

        sightings = read_sightings(clean, state_path=WORLD_MODEL_PATH)
        report = generate_report(clean, entries if entries else [], sightings=sightings)
        meaningful = bool(report.get("matches") or report.get("version_unknown"))
        if not meaningful and not refresh:
            return None
        path = save_report(report)
        if path is None:
            return None
        publish_report(report)
        return path
    except Exception:
        return None


def read_sightings(target: str | None = None, state_path: str | Path | None = None) -> list[Sighting]:
    """Extract observed service sightings from the encrypted world model.

    Args:
        target: Optional host key prefix filter; all hosts when empty.
        state_path: Optional world-model state path override.

    Returns:
        :class:`Sighting` rows for services with a product-ish name or a
        known version; unusable rows are skipped. Never raises.
    """
    from modules.world_model import read_state_dict

    path = state_path or WORLD_MODEL_PATH
    try:
        state = read_state_dict(path)
    except Exception:
        return []
    hosts = state.get("hosts") if isinstance(state, dict) else None
    if not isinstance(hosts, dict):
        return []
    usable = []
    for ip, host in hosts.items():
        if target and target not in str(ip):
            continue
        if isinstance(host, dict):
            row = dict(host)
            row.setdefault("ip", ip)
            usable.append(row)
    return _shape_sightings(usable)


def generate_report(target: str, entries: list[dict] | dict | None, sightings: list | None = None) -> dict:
    """Build the exposure report for one target.

    Args:
        target: Target host address, echoed into the report.
        entries: Road exploit feed rows (or a feed-shaped dict); when
            empty the report falls back to the live keyless feed bundle
            (`modules.lazy_cve_feed`, bounded by LAZYOWN_CVE_FEEDS env).
        sightings: Explicit sightings override; when omitted the world
            model is consulted.

    Returns:
        The report dict with score, matches, leads and rendered checks.
    """
    rows = sightings if sightings is not None else read_sightings(target)
    if rows and isinstance(rows[0], dict):
        rows = _shape_sightings(rows)
    if entries is None:
        entries = []
    if isinstance(entries, dict):
        entries = entries.get("entries") or []
    feed = lazy_feedmatch.parse_feed(entries)
    live_mode = not feed
    matches: list[dict] = []
    review: list[dict] = []
    highest_cvss = {}
    for sighting in rows:
        bindings = (
            lazy_feedmatch.live_bindings(sighting)
            if live_mode
            else bind_sighting(sighting, feed)
        )
        for binding in bindings:
            row = {
                "cve_id": binding.cve_id,
                "host": sighting.host,
                "port": sighting.port,
                "protocol": sighting.protocol,
                "product": binding.product,
                "version": binding.version,
                "tier": binding.tier,
                "cvss": round(binding.cvss, 3),
                "evidence": binding.evidence,
                "references": binding.references,
                "source": binding.source,
            }
            if binding.evidence == EVIDENCE_UNBOUNDED:
                review.append(row)
                continue
            if binding.evidence != EVIDENCE_IN_RANGE:
                continue
            matches.append(row)
            best = highest_cvss.get(binding.tier)
            if best is None or binding.cvss > best:
                highest_cvss[binding.tier] = binding.cvss
    matches.sort(key=_match_hot_key)
    review.sort(key=_match_hot_key)
    lead_rows = [{"host": s.host, "port": s.port, "product": s.product or s.name}
                 for s in unversioned_leads(rows)]
    score, detail = score_report(entries=matches, bounded_unknown=review, services=len(rows))
    temperatures = {row["tier"] for row in matches}
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "target": target,
        "feed": _live_fingerprint() if live_mode else feed_fingerprint(entries),
        "live_feeds": live_mode,
        "temperature": host_heat(temperatures),
        "score": score,
        "score_detail": detail,
        "matches": matches,
        "version_unknown": review,
        "leads": lead_rows,
        "checks": probe_checks(matches, feed),
        "notes": [
            "Product name alone is never evidence; only a version inside a bounded affected range counts.",
            "Unbounded actively-exploited entries wait for review at the lowest heat, whatever their score.",
        ],
    }
    return report


def _live_fingerprint() -> str:
    """Fingerprint for live-feed mode provenance."""
    try:
        feeds_on = str(os.environ.get("LAZYOWN_CVE_FEEDS", "1")).strip().lower() not in ("0", "false", "no")
    except Exception:
        feeds_on = True
    return f"live=lazy_cve_feed(kev,epss,exploitdb,msf,osv) allow_network={str(feeds_on).lower()}"


def score_report(entries: list[dict], bounded_unknown: list[dict], services: int) -> tuple[int, list[dict]]:
    """Score a host 0-100 with an audited point breakdown.

    Args:
        entries: Live in-range matches.
        bounded_unknown: Actively-exploited-but-unbounded review rows.
        services: Number of discovered network services.

    Returns:
        ``(score, detail)`` where detail is the ordered
        ``{"label", "points"}`` breakdown, capped at 100 points.
    """
    detail: list[dict] = []
    left = 100
    worst = None
    for row in entries:
        points = {HOT: 40, WARM: 20, COLD: 5}.get(row["tier"], 5)
        if worst is None or points > worst["points"]:
            worst = {"label": f"{row['tier'].capitalize()} match {row['cve_id']} ({row['product']})",
                     "points": points}
    if worst is not None:
        detail.append(worst)
        left -= min(worst["points"], left)
    if len(bounded_unknown):
        points = min(len(bounded_unknown), SCORE_UNBOUNDED_CAP)
        ids = ", ".join(sorted(row["cve_id"] for row in bounded_unknown)[:3])
        detail.append({"label": f"Actively exploited matches with unbounded versions to review ({ids})",
                       "points": min(points, left)})
        left = max(0, left - points)
    if services:
        points = min(services, SCORE_SURFACE_CAP)
        label = f"Discovered service surface ({services} service{'s' if services != 1 else ''})"
        detail.append({"label": label, "points": min(points, left)})
        left -= points
    total = sum(item["points"] for item in detail)
    return max(0, min(total, 100)), detail


def probe_checks(matches: list[dict], feed: list[lazy_feedmatch.FeedEntry]) -> list[dict]:
    """Render read-only validation checks for the hottest matches.

    Args:
        matches: In-range match rows from :func:`generate_report`.
        feed: Parsed feed entries carrying the affected ranges.

    Returns:
        Up to :data:`MAX_CHECKS` rendered check dicts ready to paste into
        a chain step or a beacon session.
    """
    ranges_by_cve = {entry.cve_id: entry.ranges for entry in feed}
    rendered: list[dict] = []
    for row in matches:
        if len(rendered) >= MAX_CHECKS:
            break
        check = render_check(CHECK_VERSION_BANNER, {
            "port": row["port"],
            "product": row["product"],
            "ranges": ranges_by_cve.get(row["cve_id"], []),
        })
        if check.errors:
            continue
        rendered.append({
            "kind": check.kind,
            "tool": check.tool,
            "command": check.command,
            "expect": check.expect,
            "explain": check.explain,
            "cve_id": row["cve_id"],
        })
    return rendered


def save_report(report: dict, path: str | Path | None = None) -> Path | None:
    """Atomically persist the report for downstream surfaces.

    Args:
        report: Report dict from :func:`generate_report`.
        path: Optional path override.

    Returns:
        The written path, or None on failure. Never raises.
    """
    target = str(report.get("target") or "target")
    out_path = Path(path) if path else SESSIONS_DIR / f"{REPORT_PREFIX}{_slug(target)}.json"
    payload = json.dumps(report, indent=2, default=str)
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = out_path.with_suffix(out_path.suffix + ".tmp")
        tmp.write_text(payload, encoding="utf-8")
        os.replace(tmp, out_path)
        return out_path
    except OSError:
        return None


def publish_report(report: dict) -> dict:
    """Publish one outcome event for the whole report.

    Args:
        report: Report dict from :func:`generate_report`.

    Returns:
        The ``{sink: ok}`` fan-out map from :mod:`modules.outcome_bus`.
    """
    from modules.outcome_bus import record_event

    severity = SEVERITY_FROM_HEAT.get(str(report.get("temperature") or ""), "medium")
    matches = report.get("matches") or []
    return record_event(
        kind="lazy_intel",
        target=str(report.get("target") or ""),
        title=f"lazy_intel {report.get('temperature', 'clean')} exposure score {report.get('score', 0)}",
        description=(
            f"{len(matches)} in-range exploit match(es), "
            f"{len(report.get('version_unknown') or [])} unbounded review item(s)"
        ),
        severity=severity,
        success=True,
        source="lazy_intel",
        command="lazyintel",
        artifacts=[str(REPORT_PREFIX)],
        metadata={
            "score": report.get("score", 0),
            "temperature": report.get("temperature", ""),
            "feed": report.get("feed", ""),
            "cve_ids": [row["cve_id"] for row in matches],
            "matches": [
                {
                    "cve_id": row["cve_id"],
                    "host": row["host"],
                    "port": row["port"],
                    "product": row["product"],
                    "version": row["version"],
                    "tier": row["tier"],
                    "evidence": row["evidence"],
                    "references": _short_refs(row),
                }
                for row in matches[:MAX_SINK_ROWS]
            ],
        },
    )


MAX_SINK_ROWS = 8


def _short_refs(row: dict) -> list[str]:
    """Keep at most short reference links for sink metadata."""
    return [str(link)[:120] for link in (row.get("references") or [])[:2]]


def _shape_sightings(rows: list[dict]) -> list[Sighting]:
    """Project world-model-shaped dicts into :class:`Sighting` rows."""
    shaped: list[Sighting] = []
    for row in rows:
        host = str(row.get("ip") or row.get("host") or "")
        services = row.get("services") if isinstance(row.get("services"), dict) else None
        if services is not None:
            for port, svc in services.items():
                if not isinstance(svc, dict):
                    continue
                shaped.append(Sighting(
                    host=host,
                    port=_int(svc.get("port"), port),
                    protocol=str(svc.get("protocol") or "tcp"),
                    product=str(svc.get("name") or svc.get("product") or "").strip(),
                    version=str(svc.get("version") or "").strip(),
                    name=str(svc.get("service_name") or "").strip(),
                ))
            continue
        shaped.append(Sighting(
            host=host,
            port=_int(row.get("port"), 0),
            protocol=str(row.get("protocol") or "tcp"),
            product=str(row.get("product") or row.get("name") or "").strip(),
            version=str(row.get("version") or "").strip(),
            source=str(row.get("source") or "scanner"),
        ))
    return shaped


def _match_hot_key(row: dict) -> tuple[int, float]:
    """Sort key, hottest first then strongest CVSS."""
    return (-heat_rank(row.get("tier", "")), -float(row.get("cvss") or 0.0))


def _slug(text: str) -> str:
    """Compact a target into a filename fragment."""
    return "".join(ch if ch.isalnum() or ch == "." else "_" for ch in text).strip("._") or "target"


def _int(value: object, fallback: int) -> int:
    """Return an int port, keeping the dict key as a fallback."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def refresh_if_stale(target: str, entries: list[dict] | dict | None = None) -> Path | None:
    """Regenerate the report only when newer evidence exists.

    The report is stale when the nmap XML ingest is newer than the saved
    exposition artefact (a fresh scan happened after the last intel
    pass); the engine calls this from the intel sync stage so the
    fire-pending selector never reads outdated intelligence.

    Args:
        target: Host address.
        entries: Optional feed rows forwarded to :func:`ensure_report`.

    Returns:
        The refreshed report path, or None when nothing was stale.
    """
    clean = str(target or "").strip()
    if not clean:
        return None
    report_path = SESSIONS_DIR / f"{REPORT_PREFIX}{clean}.json"
    scan_path = SESSIONS_DIR / f"scan_{clean}.nmap.xml"
    if not scan_path.exists():
        return None
    if report_path.exists():
        try:
            if scan_path.stat().st_mtime <= report_path.stat().st_mtime:
                return None
        except OSError:
            return None
    return ensure_report(clean, entries=entries, refresh=True)


__all__ = [
    "ensure_report",
    "MAX_CHECKS",
    "SCORE_SURFACE_CAP",
    "SCORE_UNBOUNDED_CAP",
    "SESSIONS_DIR",
    "generate_report",
    "probe_checks",
    "publish_report",
    "read_sightings",
    "refresh_if_stale",
    "save_report",
    "score_report",
]
