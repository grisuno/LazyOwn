"""Intel selector: feed exploitation intelligence into the autonomous loop.

Shared selector contract: when the exposure pipeline already graded a
target as ``fire`` with bounded evidence and no confirmation chain covers
it yet, the loop acts before any generic proposal and fires the
autofire confirmation chain. When no report exists but a local exploit
feed is staged, the loop refreshes the exposure report first. Both are
read-only steps; operator-owned arming stays inside
``modules.lazy_autofire``.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from modules.selection.base import ActionDecision, SelectionContext

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
REPORT_PREFIX = "lazy_intel_"
FEED_FILENAME = "exploit_feed.json"
CHAIN_PREFIX = "lazy_autofire_"
_CVE_TOKEN = re.compile(r"CVE-\d{4}-\d{4,7}")

_PRIORITY_FIRE = 2
_PRIORITY_REFRESH = 6


def intel_report_path(target: str) -> Path:
    """Return the saved exposure report path for one target.

    Args:
        target: Host address the report was generated for.

    Returns:
        The report file path (may not exist).
    """
    return SESSIONS_DIR / f"{REPORT_PREFIX}{target}.json"


def load_report(target: str) -> dict | None:
    """Read the saved exposure report of one target.

    Args:
        target: Host address.

    Returns:
        The report dict, or None when absent or unreadable.
    """
    try:
        data = json.loads(intel_report_path(target).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def pending_fires(target: str) -> list[dict]:
    """Fire-tier bounded matches of a target not covered by a chain yet.

    Args:
        target: Host address.

    Returns:
        Match rows (tier fire, evidence in_range) with a live chain file
        subtracted by CVE id.
    """
    report = load_report(target)
    if not report:
        return []
    fires = [
        row
        for row in report.get("matches") or []
        if row.get("tier") == "hot" and row.get("evidence") == "in_range"
    ]
    if not fires:
        return []
    covered = _covered_cves(target)
    return [row for row in fires if str(row.get("cve_id")) not in covered]


def _intelligence_sources_ready() -> bool:
    """Whether the exposure pipeline has something to run against.

    True when a local feed is staged or the live keyless feed bundle is
    allowed by the ``LAZYOWN_CVE_FEEDS`` environment flag.
    """
    if (SESSIONS_DIR / "intel" / FEED_FILENAME).exists():
        return True
    try:
        return str(os.environ.get("LAZYOWN_CVE_FEEDS", "1")).strip().lower() not in ("0", "false", "no")
    except Exception:
        return True


def _covered_cves(target: str) -> set[str]:
    """CVE ids already covered by a confirmation chain for this target."""
    slug = str(target or "").lower()
    slug = "".join(ch if ch.isalnum() else "_" for ch in slug)
    while "__" in slug:
        slug = slug.replace("__", "_")
    path = BASE_DIR / "chains" / f"{CHAIN_PREFIX}{slug.strip('_')}.yaml"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    return set(_CVE_TOKEN.findall(text))


class IntelSelector:
    """Propose the next intelligence-driven read-only confirmation step."""

    name = "intel"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return the next intelligence action, or None when none applies.

        Args:
            ctx: Live engagement snapshot from the runtime.

        Returns:
            A pending ``lazyautofire fire <target>`` when fire intel is
            uncovered, a ``lazyintel <target>`` refresh when no report
            exists but a feed is staged, else None.
        """
        target = str(ctx.target or "").strip()
        if not target:
            return None
        if f"lazyautofire fire {target}" in ctx.exclude or f"lazyintel {target}" in ctx.exclude:
            return None
        fires = pending_fires(target)
        if fires:
            return ActionDecision(
                command=f"lazyautofire fire {target}",
                source=self.name,
                reason=(
                    f"{len(fires)} hot-tier bounded match(es) pending confirmation "
                    f"({', '.join(str(row.get('cve_id')) for row in fires[:3])})"
                ),
                priority=_PRIORITY_FIRE,
            )
        if intel_report_path(target).exists():
            return None
        if not _intelligence_sources_ready():
            return None
        return ActionDecision(
            command=f"lazyintel {target}",
            source=self.name,
            reason="no exposure report for this target while intelligence sources are ready",
            priority=_PRIORITY_REFRESH,
        )


__all__ = ["IntelSelector", "intel_report_path", "load_report", "pending_fires"]
