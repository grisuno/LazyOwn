"""Validation plans as data: re-read observed checks through version math.

The retest engine (:mod:`modules.lazy_verify`) already replays read-only
checks; this module adds the interpretation layer: version strings seen
in check evidence are re-read through :func:`lazy_heat.version_in_range`
against the stored OSV range, so a retest verdict states
``reaffirmed``/``version_changed``/``inconclusive`` instead of a grep
lane. A check that fails to reproduce never lowers a hardened finding.

Stdlib only; every entry point degrades to ``inconclusive``.
"""

from __future__ import annotations

import re
from typing import Any

from modules.lazy_heat import parse_version, version_in_range

REAFFIRMED = "reaffirmed"
VERSION_CHANGED = "version_changed"
INCONCLUSIVE = "inconclusive"

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,10}", re.IGNORECASE)
_VERSION_RE = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3}){1,4}(?:[a-zA-Z][a-z0-9]*)?)")
_IP_SHAPE_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")
_MAX_EVIDENCE = 2000


def extract_version(text: str) -> str:
    """Pull the most version-like token from check output.

    The token starts with a digit, tolerates patch tails (``9.9p1``,
    ``1.0.2k``) and rejects four-octet shapes so IPv4 addresses never
    read as versions.

    Args:
        text: Combined check evidence.

    Returns:
        Version string, or '' when absent.
    """
    for match in _VERSION_RE.finditer(str(text or "")):
        candidate = match.group(1)
        if _IP_SHAPE_RE.fullmatch(candidate):
            continue
        return candidate
    return ""


def extract_cve(text: str) -> str:
    """Pull the uppercased CVE id from a finding text, or ''."""
    match = CVE_RE.search(str(text or ""))
    return match.group(0).upper() if match else ""


def interpret_checks(
    checks: list[dict],
    cve: str = "",
    stored_version: str = "",
    ranges: dict | None = None,
) -> dict[str, Any]:
    """Re-read check results through the stored version range.

    Args:
        checks: Results shaped like :func:`lazy_verify.run_check` rows
            (kind/verdict/evidence).
        cve: Finding CVE id; '' pins the generic lane.
        stored_version: Version the finding was recorded with.
        ranges: Stored OSV range dict; ''-safe.

    Returns:
        ``{verdict, observed_version, stored_version, cve, evidence}`
        verdict is REAFFIRMED, VERSION_CHANGED or INCONCLUSIVE.
    """
    evidence_lines: list[str] = []
    hits = 0
    for row in checks or []:
        kind = str(row.get("kind", "")) or "check"
        verdict = str(row.get("verdict", "") or "")
        evidence = str(row.get("evidence", ""))[:400]
        evidence_lines.append(f"[{verdict}] {kind}: {evidence}")
        if verdict == "hit":
            hits += 1
    combined = "\n".join(evidence_lines)[:_MAX_EVIDENCE]
    observed = extract_version(combined)
    verdict = INCONCLUSIVE
    if hits:
        verdict = REAFFIRMED
    if observed and ranges:
        ruling = _range_says(observed, ranges)
        if ruling is True:
            verdict = REAFFIRMED
        elif ruling is False:
            verdict = VERSION_CHANGED
    return {
        "verdict": verdict,
        "observed_version": observed,
        "stored_version": str(stored_version or ""),
        "cve": str(cve or ""),
        "evidence": combined,
    }


def _range_says(version: str, ranges: dict | None) -> bool | None:
    """Evaluate one version against a stored OSV range.

    Args:
        version: Candidate version string.
        ranges: Stored OSV range dict (type/introduced/fixed/lastAffected).

    Returns:
        True inside the range, False outside, None unknown.
    """
    if not version or not ranges:
        return None
    parsed = parse_version(version)
    if parsed is None:
        return None
    return version_in_range(parsed, ranges)


__all__ = [
    "INCONCLUSIVE",
    "REAFFIRMED",
    "VERSION_CHANGED",
    "extract_cve",
    "extract_version",
    "interpret_checks",
]
