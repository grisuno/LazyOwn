"""Match policy doctrine: what may claim a match and what stays a lead.

Adapted from the evidence-driven matching doctrine: a match needs the
same product and a version inside a bounded affected range; everything
else is a lead, evidence attaches to matches but never creates them,
and anything a human, template or retest touched never auto-closes.

Core state machine:

- ``match`` — version known, inside a bounded range.
- ``lead`` — product seen without any version; dedupe keeps the best
  sighting, OS sightings never name a version.
- ``version_unknown`` — non-bounded evidence (EOL branch, no bound),
  capped score, human closure only.
- Closures persist their reason and reopen only on new evidence.
- ``has_standing`` protects remediated/dialed rows: auto-merge skips.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

MATCH = "match"
LEAD = "lead"
VERSION_UNKNOWN = "version_unknown"
LEAD_SCORE_CAP = 2
MATCH_SCORE_CAP = 100
UNKNOWN_SCORE_CAP = 2
STORE_FILENAME = "match_policy.json"
_STANDING_KINDS = ("remediation", "assignee", "comment", "manual-validation", "template", "retest", "operator")
_MAX_STORE_ROWS = 4000


def strand_from_sighting(sighting: dict[str, Any]) -> str:
    """Classify one product sighting per the doctrine.

    Args:
        sighting: ``{"product", "version", "os": bool, "ranges": dict,
            "kev_nobound": bool}``.

    Returns:
        One of MATCH, LEAD, VERSION_UNKNOWN.
    """
    product = str((sighting or {}).get("product", "") or "").strip()
    if not product:
        return LEAD
    version = str((sighting or {}).get("version", "") or "").strip()
    if not version:
        return LEAD
    ranges = (sighting or {}).get("ranges") or {}
    if not ranges:
        if bool((sighting or {}).get("kev_nobound")):
            return VERSION_UNKNOWN
        return LEAD
    ruling = _version_in_range(version, ranges)
    if ruling is True:
        return MATCH
    if ruling is False:
        return LEAD
    return VERSION_UNKNOWN


def _version_in_range(version: str, ranges: dict) -> bool | None:
    """Judge one version inside a stored range dict."""
    try:
        from modules.lazy_heat import parse_version, version_in_range

        parsed = parse_version(version)
        if parsed is None:
            return None
        return version_in_range(parsed, ranges)
    except Exception:
        return None


def is_os_sighting(product: str, cpe: str = "") -> bool:
    """Return True when the sighting names an operating system.

    OS names never headline version matches: nmap OS CPE plus a
    product name is still an OS sighting.

    Args:
        product: Product text.
        cpe: Optional CPE string.

    Returns:
        True for obvious OS identities.
    """
    lowered = str(product or "").lower()
    cpe_l = str(cpe or "").lower()
    if cpe_l.startswith("cpe:/o:"):
        return True
    names = ("linux", "windows", "macos", "darwin", "freebsd", "debian", "ubuntu", "centos", "red hat")
    if any(name in lowered for name in names) and len(lowered) < 40:
        return True
    return False


def strand_rank(strand: str) -> int:
    """Return the merge precedence of a strand."""
    return {"": 0, LEAD: 1, VERSION_UNKNOWN: 2, MATCH: 3}.get(str(strand or "").strip().lower(), 0)


def has_standing(match: dict[str, Any]) -> bool:
    """Return True when humans or durable evidence touched a match.

    Args:
        match: Match row carrying an ``evidence``/``timeline`` list.

    Returns:
        True when any standing kind appears in the row.
    """
    for key in ("evidence", "timeline", "sources"):
        for entry in (match or {}).get(key, []) or []:
            kind = str((entry or {}).get("kind", "")).lower()
            if kind and any(name in kind for name in _STANDING_KINDS):
                return True
    return bool((match or {}).get("standing"))


class MatchStore:
    """Bounded JSON registry of matches and leads with closure audit."""

    def __init__(self, sessions_dir: str | Path | None = None) -> None:
        """Bind the store file under sessions/lazy."""
        base = Path(str(sessions_dir or "sessions")) / "lazy"
        self._path = base / STORE_FILENAME

    def upsert(self, identity: dict[str, Any], sighting: dict[str, Any], now: float | None = None) -> dict[str, Any]:
        """Record one sighting under the dedupe identity.

        Known-version sightings win over bare leads; a better row
        replaces a worse one. The operator's standing blocks overwrite.

        Args:
            identity: Match identity fields.
            sighting: One product sighting shaped for
                :func:`strand_from_sighting`.
            now: Reference epoch for timeline stamps.

        Returns:
            The row after the update.
        """
        store = self._load()
        rows = store.setdefault("rows", {})
        key = self._key(identity)
        row = rows.get(key, {"identity": dict(identity), "strand": "", "sightings": [], "timeline": []})
        strand = strand_from_sighting(sighting)
        stamp = {"ts": float(now if now is not None else time.time()), "strand": strand,
                 "version": str((sighting or {}).get("version", "") or "")}
        existing_versions = {entry.get("version", "") for entry in row.get("sightings", [])}
        if stamp["version"] or strand != LEAD or not existing_versions:
            row.setdefault("sightings", []).append(stamp)
        current = str(row.get("strand", "") or "")
        if strand_rank(strand) > strand_rank(current):
            row["strand"] = strand
        snapshot = float(now if now is not None else time.time())
        row.setdefault("timeline", []).append(
            {"ts": snapshot, "kind": "match-sighting" if strand == MATCH else "sighting"}
        )
        row["timeline"] = row["timeline"][-200:]
        rows[key] = row
        self._save_frame(store)
        return self._load()["rows"][key]

    @staticmethod
    def _key(identity: dict[str, Any]) -> str:
        """Build the dedupe identity key."""
        return "|".join(
            f"{part}={str((identity or {}).get(part, '') or '').strip().lower()}"
            for part in ("cve", "product", "host")
        )

    def rows(self) -> dict[str, dict[str, Any]]:
        """Return every stored row."""
        return dict(self._load().get("rows", {}))

    def close(self, identity: dict[str, Any], reason: str, now: float | None = None) -> dict:
        """Close one row, keeping its reason and reopening block."""
        store = self._load()
        rows = store.setdefault("rows", {})
        key = self._key(identity)
        row = rows.get(key)
        if not row:
            return {}
        row["closed"] = {
            "ts": float(now if now is not None else time.time()),
            "reason": str(reason or "").strip()[:300] or "no reason recorded",
        }
        self._save_frame(store)
        return row["closed"]

    def closed_reason(self, identity: dict[str, Any]) -> str:
        """Return the persisted closure reason, or '' when open or unknown."""
        row = self._load().get("rows", {}).get(self._key(identity))
        if not row:
            return ""
        return str((row.get("closed") or {}).get("reason", "") or "")

    def _load(self) -> dict:
        """Read the store or start empty."""
        try:
            if self._path.is_file():
                data = json.loads(self._path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        return {}

    def _save_frame(self, store: dict) -> None:
        """Persist with row pruning."""
        try:
            rows = store.setdefault("rows", {})
            if len(rows) > _MAX_STORE_ROWS:
                pruned = dict(sorted(rows.items(), key=lambda item: -(item[1].get("timeline") or [{}])[-1].get("ts", 0.0))[:_MAX_STORE_ROWS])
                store["rows"] = pruned
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(store), encoding="utf-8")
        except Exception:
            pass


__all__ = [
    "LEAD",
    "LEAD_SCORE_CAP",
    "MATCH",
    "MATCH_SCORE_CAP",
    "STORE_FILENAME",
    "UNKNOWN_SCORE_CAP",
    "VERSION_UNKNOWN",
    "MatchStore",
    "has_standing",
    "is_os_sighting",
    "strand_from_sighting",
]
