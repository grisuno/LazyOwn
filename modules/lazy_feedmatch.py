"""Exploit feed matching for LazyOwn.

Turns a local exploit-intelligence feed into per-product evidence decisions
for the services the engagement has already discovered. A product name alone
is never evidence: only a version inside a bounded affected range of the same
product counts, with one deliberate exception for actively exploited
advisories that publish no usable range (kept as low-confidence review
candidates, never counted as heat). Products seen with no version stay as
unversioned leads so a later banner, probe or host report can promote them.

Tier maths live in :mod:`modules.lazy_heat` (the one vocabulary: hot/warm/
cold); this file adds the feed schema, the sighting binding and the live
adapter to :mod:`modules.lazy_cve_feed`. Feed schema (JSON file, default
``sessions/intel/exploit_feed.json``)::

    {"entries": [
        {"cve_id": "CVE-2024-0001", "product": "apache tomcat",
         "cvss": 9.8, "kev": true, "epss": 0.42, "public_exploit": true,
         "ranges": [{"introduced": "10.0.0", "fixed": "10.0.20"}],
         "references": ["https://..."]},
        ...
    ]}

Stdlib only, pure functions on plain input, never raises on bad data.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from modules.lazy_heat import (
    COLD,
    classify_heat,
    match_heat,
    parse_version,
    product_token,
    token_matches,
    version_in_range,
)

BASE_DIR = Path(__file__).resolve().parent.parent
FEED_FILENAME = "exploit_feed.json"
DEFAULT_FEED_PATH = BASE_DIR / "sessions" / "intel" / FEED_FILENAME

EVIDENCE_IN_RANGE = "in_range"
EVIDENCE_UNBOUNDED = "unbounded_kev"
EVIDENCE_NONE = "none"

RANGE_KEYS = frozenset({"introduced", "fixed", "last_affected"})

_GENERIC_WORDS = frozenset({
    "http", "service", "server", "web", "daemon", "open", "project", "edition",
    "community", "enterprise", "generic",
})
_NOT_A_PRODUCT = frozenset({"unknown", "tcpwrapped"})
_OS_SIGHTINGS = re.compile(
    r"^(?:(?:microsoft|canonical|gnu)\s+)?(?:"
    r"windows(?:\s+(?:server|nt|\d[\w.]*|xp|vista|rt|ce|embedded)\b.*)?"
    r"|ubuntu(?:\s+linux)?|debian(?:\s+(?:gnu\s*/\s*)?linux)?|centos(?:\s+linux)?"
    r"|(?:red\s*hat\s+)?(?:enterprise\s+)?linux(?:\s+kernel)?|rhel|fedora"
    r"|alpine(?:\s+linux)?|(?:open)?suse(?:\s+linux)?|rocky(?:\s+linux)?"
    r"|almalinux|oracle\s+linux|amazon\s+linux|freebsd|openbsd|netbsd"
    r"|macos|mac\s+os(?:\s+x)?|os\s+x|unix|android|ios)$",
    re.IGNORECASE,
)


@dataclass
class FeedEntry:
    """One normalized exploit-intelligence entry.

    Attributes:
        cve_id: Advisory identifier.
        product: Normalized product token the advisory names.
        cvss: CVSS score when published.
        kev: Known-exploited catalog membership.
        epss: EPSS probability (0..1) when published, else None.
        public_exploit: A public exploit or working module exists.
        ranges: Affected version ranges as plain dicts.
        raw: The original feed entry row.
    """

    cve_id: str
    product: str
    cvss: float = 0.0
    kev: bool = False
    epss: float | None = None
    public_exploit: bool = False
    ranges: list[dict] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


@dataclass
class Sighting:
    """One observed service on one host.

    Attributes:
        host: Host address.
        port: Service port.
        protocol: Transport protocol.
        product: Product name reported by the scanner or fingerprint.
        version: Version string when known, else empty.
        name: Raw service label when not a product string.
        source: ``scanner`` for a fingerprint endpoint sighting,
            ``host`` when the admission came from a host-reported
            inventory (packages the host says it runs).
    """

    host: str = ""
    port: int = 0
    protocol: str = "tcp"
    product: str = ""
    version: str = ""
    name: str = ""
    source: str = "scanner"


@dataclass
class ExploitSighting:
    """One exploit advisory bound to one sighting with its evidence state.

    Attributes:
        cve_id: Advisory identifier.
        product: Product the advisory named.
        version: Target version string when the sighting had one.
        tier: Match heat tier (HOT/WARM/COLD from :mod:`modules.lazy_heat`).
        cvss: Advisory CVSS score.
        evidence: :data:`EVIDENCE_IN_RANGE`, :data:`EVIDENCE_UNBOUNDED`
            (actively exploited with no bound, review only)
            or :data:`EVIDENCE_NONE`.
        version_in_range: True, False or None when untestable.
        references: Advisory reference links.
        source: Sighting provenance (``scanner``/``host``).
    """

    cve_id: str
    product: str
    version: str = ""
    tier: str = ""
    cvss: float = 0.0
    evidence: str = EVIDENCE_NONE
    version_in_range: bool | None = None
    references: list[str] = field(default_factory=list)
    source: str = "scanner"


def load_feed(path: str | Path | None = None) -> list[dict]:
    """Load raw feed rows from a JSON file.

    Args:
        path: Optional feed path override; falls back to
            :data:`DEFAULT_FEED_PATH`. Supports CISA KEV-style dumps where
            rows may live under ``vulnerabilities``.

    Returns:
        A list of raw entry dicts; empty when the file is missing or bad.
    """
    feed_path = Path(path) if path else DEFAULT_FEED_PATH
    if not feed_path.is_file():
        return []
    try:
        with open(feed_path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("entries")
        if rows is None and isinstance(data.get("vulnerabilities"), list):
            rows = []
            for item in data["vulnerabilities"]:
                mapped = _map_kev_row(item)
                if mapped is not None:
                    rows.append(mapped)
        if rows is None:
            rows = data.get("feeds") or []
    else:
        rows = []
    return [row for row in rows if isinstance(row, dict)]


def _map_kev_row(item: dict) -> dict | None:
    """Project one CISA KEV dump row onto the feed entry schema.

    Args:
        item: Raw KEV catalog JSON object.

    Returns:
        A schema-shaped dict, or None for missing essential fields.
    """
    vendor = item.get("vendorProject", "")
    project = item.get("product", "")
    normalized = " ".join(part for part in (str(vendor), str(project)) if part).strip()
    name = item.get("cveID")
    if not name or not normalized:
        return None
    return {
        "cve_id": name,
        "product": normalized,
        "references": [],
        "kev": True,
    }


def parse_feed(entries: list[dict]) -> list[FeedEntry]:
    """Normalize raw feed rows into :class:`FeedEntry` objects.

    Args:
        entries: Raw dicts from :func:`load_feed`.

    Returns:
        Valid entries with a product name and identifier; malformed rows
        are dropped.
    """
    normalized: list[FeedEntry] = []
    seen: set[tuple[str, str]] = set()
    for row in entries:
        cve_id = str(row.get("cve_id") or row.get("id") or "").strip().upper()
        product = product_token(str(row.get("product") or ""))
        if not cve_id or not product:
            continue
        key = (cve_id, product)
        if key in seen:
            continue
        seen.add(key)
        ranges = row.get("ranges") if isinstance(row.get("ranges"), list) else []
        clean_ranges = [rng for rng in ranges if isinstance(rng, dict) and set(rng) & RANGE_KEYS and any(
            isinstance(rng.get(key), str) and rng.get(key).strip() for key in RANGE_KEYS
        )]
        normalized.append(FeedEntry(
            cve_id=cve_id,
            product=product,
            cvss=_cvss(row.get("cvss")),
            kev=bool(row.get("kev")),
            epss=_float(row.get("epss")) if _float(row.get("epss")) > 0 else None,
            public_exploit=bool(row.get("public_exploit") or row.get("exploit_db")),
            ranges=clean_ranges,
            raw=dict(row),
        ))
    return normalized


def is_os_sighting(name: str) -> bool:
    """Whether a scanner label names an operating system, never an application.

    Args:
        name: Raw scanner product string.

    Returns:
        True for operating-system fingerprints, which do not match
        advisories by name.
    """
    text = re.sub(r"[_\-]+", " ", str(name or "").strip())
    return bool(_OS_SIGHTINGS.match(text))


def entry_matches_product(entry: FeedEntry, product: str) -> bool:
    """Whether an advisory and a sighting name the same product.

    Args:
        entry: Normalized feed entry (lazy_heat token space).
        product: Normalized sighting product token.

    Returns:
        True on whole-token containment either way, so a scanner's
        ``openssh 3.0.2`` still matches an advisory naming ``openssh``.
    """
    if not product:
        return False
    if product == entry.product:
        return True
    return token_matches(entry.product, product) or product in entry.product or entry.product in product


def version_in_ranges(version: tuple | None, ranges: list[dict]) -> bool | None:
    """Test a parsed version against an advisory's affected ranges.

    Delegates each range to :func:`modules.lazy_heat.version_in_range`
    (the one version-range implementation), mapping the feed's
    ``last_affected`` key to the canonical ``lastAffected``.

    Args:
        version: Parsed target version, or None when the sighting has one.
        ranges: Range dicts with ``introduced``, ``fixed`` and
            ``last_affected`` bounds.

    Returns:
        True inside any range, False outside every bounded range, None
        when every range is unbounded and the version cannot be tested.
    """
    if version is None:
        return None
    bounded_ranges = [rng for rng in ranges if _fixed_key(rng)]
    if not bounded_ranges:
        return None
    for rng in bounded_ranges:
        mapped = {
            "type": "SEMVER",
            "introduced": rng.get("introduced") or "",
            "fixed": rng.get("fixed") or "",
            "lastAffected": rng.get("last_affected") or rng.get("lastAffected") or "",
        }
        result = version_in_range(version, mapped)
        if result is True:
            return True
        if result is None:
            return None
    return False


def _fixed_key(rng: dict) -> str | None:
    """Return which bounded key a range carries, else None."""
    if str(rng.get("fixed") or "").strip():
        return "fixed"
    if str(rng.get("last_affected") or "").strip():
        return "last_affected"
    return None


def feed_tier(entry: FeedEntry) -> str:
    """Feed-level heat tier of one advisory via :mod:`modules.lazy_heat`.

    Args:
        entry: Normalized feed entry.

    Returns:
        HOT, WARM or COLD.
    """
    return classify_heat(kev=entry.kev, epss=entry.epss, exploit=entry.public_exploit, cvss=entry.cvss)


def bind_sighting(sighting: Sighting, entries: list[FeedEntry]) -> list[ExploitSighting]:
    """Bind one service sighting to every advisory that names its product.

    Args:
        sighting: One observed service.
        entries: Normalized feed entries from :func:`parse_feed`.

    Returns:
        Evidence-graded :class:`ExploitSighting` bindings, hottest first.
        A version-less sighting yields no bindings, by policy.
    """
    source_text = sighting.product or sighting.name
    token = product_token(source_text)
    if not token or is_os_sighting(source_text) or source_text.strip().lower() in _NOT_A_PRODUCT:
        return []
    if not sighting.version.strip():
        return []
    parsed = parse_version(sighting.version)
    if parsed is None:
        return []
    bindings: list[ExploitSighting] = []
    for entry in entries:
        if not entry_matches_product(entry, token):
            continue
        in_range = version_in_ranges(parsed, entry.ranges)
        evidence = EVIDENCE_NONE
        tier = COLD
        if in_range is True:
            evidence = EVIDENCE_IN_RANGE
            tier = match_heat(feed_tier(entry), cvss=entry.cvss)
        elif in_range is None:
            if not entry.kev:
                continue
            evidence = EVIDENCE_UNBOUNDED
        else:
            continue
        bindings.append(ExploitSighting(
            cve_id=entry.cve_id,
            product=entry.product,
            version=sighting.version.strip(),
            tier=tier,
            cvss=entry.cvss,
            evidence=evidence,
            version_in_range=in_range,
            references=_references(entry.raw),
            source=sighting.source,
        ))
    bindings.sort(key=lambda b: (0 if b.evidence == EVIDENCE_IN_RANGE else 1, -b.cvss))
    return bindings


def unversioned_leads(sightings: list[Sighting]) -> list[Sighting]:
    """Products seen with no version, as leads for later promotion.

    Args:
        sightings: Observed services.

    Returns:
        One lead per distinct unversioned product that no sibling sighting
        already reports with a version.
    """
    versioned = {product_token(s.product or s.name) for s in sightings if s.version.strip()}
    versioned.discard("")
    leads: list[Sighting] = []
    seen: set[str] = set()
    for item in sightings:
        token = product_token(item.product or item.name)
        if not token or token in versioned or token in seen:
            continue
        seen.add(token)
        leads.append(item)
    return leads


def live_bindings(sighting: Sighting, allow_network: bool = True) -> list[ExploitSighting]:
    """Correlate one sighting through the live keyless feed bundle.

    Delegates to :func:`modules.lazy_cve_feed.correlate` (KEV, EPSS,
    Exploit-DB, Metasploit, OSV with disk cache and offline degradation)
    and projects its heat rows onto the evidence-graded sighting shape,
    keeping the lazy_heat vocabulary untouched.

    Args:
        sighting: One observed service with product and version.
        allow_network: Forwarded to the feed bundle; False keeps it
            cache-only.

    Returns:
        Evidence-graded bindings, hottest first.
    """
    try:
        from modules.lazy_cve_feed import correlate

        candidates = correlate(
            sighting.product or sighting.name,
            version=sighting.version or "",
            allow_network=allow_network,
        )
    except Exception:
        return []
    bindings: list[ExploitSighting] = []
    for row in candidates:
        if not isinstance(row, dict):
            continue
        in_range = row.get("in_range")
        tier = str(row.get("heat") or COLD)
        if in_range is True:
            evidence = EVIDENCE_IN_RANGE
        elif in_range is None and bool(row.get("kev")):
            evidence = EVIDENCE_UNBOUNDED
        else:
            continue
        bindings.append(ExploitSighting(
            cve_id=str(row.get("cve") or ""),
            product=product_token(sighting.product or sighting.name),
            version=sighting.version.strip(),
            tier=tier,
            cvss=_cvss(row.get("cvss")),
            evidence=evidence,
            version_in_range=in_range,
            references=[],
            source=sighting.source,
        ))
    bindings.sort(key=lambda b: (0 if b.evidence == EVIDENCE_IN_RANGE else 1, -b.cvss))
    return bindings


def _references(raw: dict) -> list[str]:
    """Collect reference links from a raw feed row."""
    refs = raw.get("references") if isinstance(raw.get("references"), list) else []
    return [str(link) for link in refs if link]


def _cvss(value: object) -> float:
    """Return a CVSS float, 0.0 for unusable input."""
    try:
        return max(0.0, min(10.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _float(value: object) -> float:
    """Return a float, 0.0 for unusable input."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def feed_fingerprint(entries: list[dict]) -> str:
    """Return a size/mtime fingerprint for feed provenance in reports.

    Args:
        entries: Raw loaded rows (unused for path resolution, kept for
            signature stability).

    Returns:
        ``rows=<n> file=<path> sha16=<prefix>`` of the feed file contents.
    """
    feed_env = os.environ.get("LAZY_INTEL_FEED", "")
    feed_path = Path(feed_env or str(DEFAULT_FEED_PATH))
    digest = "none"
    try:
        import hashlib

        payload = feed_path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()[:16]
    except OSError:
        digest = "none"
    return f"rows={len(entries)} file={feed_path.name} sha16={digest}"

__all__ = [
    "DEFAULT_FEED_PATH",
    "EVIDENCE_IN_RANGE",
    "EVIDENCE_UNBOUNDED",
    "EVIDENCE_NONE",
    "FeedEntry",
    "ExploitSighting",
    "RANGE_KEYS",
    "Sighting",
    "bind_sighting",
    "entry_matches_product",
    "feed_fingerprint",
    "feed_tier",
    "is_os_sighting",
    "load_feed",
    "live_bindings",
    "parse_feed",
    "unversioned_leads",
    "version_in_ranges",
]
