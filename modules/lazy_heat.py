"""Heat tiers and version math for CVE correlation.

Heat is a deterministic pre-classification of a CVE from its
exploitation and severity signals so the pipeline can prioritise what
correlators and the autonomous loop look at first:

  hot   — actively dangerous now: KEV, public/weaponized exploit,
          critical CVSS (>= 9.0), or high EPSS plus high CVSS
  warm  — warning signs: high CVSS (>= 7.0) or EPSS threshold reached
  cold  — low-priority watch: everything else

A match's heat on *your* host differs from the feed heat: a match the
host's distribution already backported a fix for is cold however hot
the CVE is, and a confirmed match on a high score reads as hot.

Version helpers are pure stdlib so every rule is unit-testable without
network access. Thresholds live in one place and are easy to retune.

Stdlib only. Never raises on untrusted input; every entry point
degrades to "unknown" when data is missing.
"""

from __future__ import annotations

import re

HOT = "hot"
WARM = "warm"
COLD = "cold"

HIGH_CVSS = 7.0
CRITICAL_CVSS = 9.0
EPSS_THRESHOLD = 0.1

HEAT_RANK = {HOT: 3, WARM: 2, COLD: 1}

SEVERITY_FROM_HEAT = {HOT: "critical", WARM: "high", COLD: "medium"}

# Severity label -> heat rank for findings that carry no CVE id.
SEVERITY_HEAT = {"critical": HOT, "high": HOT, "medium": WARM, "low": COLD}

# Distro backport status for a version-in-range match.
PATCHED = "patched"
VULNERABLE = "vulnerable"
UNKNOWN = "unknown"
NO_DATA = "no_data"

_VER_RE = re.compile(r"(\d+(?:\.\d+)*)")
_EPOCH_RE = re.compile(r"^\s*\d+:(?=\d)")
_HASH_RE = re.compile(r"^[0-9a-f]{7,40}$", re.IGNORECASE)
_PRE_RE = re.compile(
    r"^[-_.~+ ]?(?:(alpha|beta|rc|cr|pre|dev|snapshot)|(a|b|m))[-_. ]?(\d+)?", re.IGNORECASE
)
_PRE_RANK = {"dev": -6, "snapshot": -6, "alpha": -5, "a": -5, "beta": -4, "b": -4, "m": -3, "pre": -2, "cr": -1, "rc": -1}

_MIN_TOKEN_LEN = 3
# Generic words identify infrastructure, not a vulnerable product.
GENERIC_WORDS = frozenset(
    {
        "cms", "server", "core", "api", "web", "app", "http", "https", "framework", "project", "client",
        "service", "services", "sdk", "cli", "lib", "library", "tool", "tools", "manager", "platform",
        "engine", "plugin", "module", "data", "cloud", "ssl", "tls", "js", "html", "proxy", "gateway",
        "portal", "admin", "system", "daemon", "database", "db",
    }
)


def classify_heat(
    kev: bool = False, epss: float | None = None, exploit: bool = False, cvss: float = 0.0
) -> str:
    """Return the heat tier of one CVE from its exploitation signals.

    Args:
        kev: CVE is on a known-exploited catalog.
        epss: EPSS probability (0..1) or None when unknown.
        exploit: Public or weaponized exploit code exists.
        cvss: CVSS base score.

    Returns:
        One of HOT, WARM, COLD.
    """
    score = float(cvss or 0.0)
    epss_reached = epss is not None and float(epss) >= EPSS_THRESHOLD
    if kev or exploit or score >= CRITICAL_CVSS or (epss_reached and score >= HIGH_CVSS):
        return HOT
    if score >= HIGH_CVSS or epss_reached:
        return WARM
    return COLD


def match_heat(tier: str, cvss: float = 0.0, verdict: str = "", distro_status: str = "") -> str:
    """Return the heat of one CVE *on one host*.

    A backported (patched by distro) match is COLD however dangerous the
    CVE is; a confirmed match on a high score reads as HOT.

    Args:
        tier: Feed tier from :func:`classify_heat`.
        cvss: CVE CVSS base score.
        verdict: Correlation verdict (``affected`` / ``uncertain``).
        distro_status: Distro backport status for the match.

    Returns:
        One of HOT, WARM, COLD.
    """
    if distro_status == PATCHED:
        return COLD
    if distro_status == VULNERABLE:
        return HOT if tier == HOT else max(tier, WARM, key=HEAT_RANK.get)
    if tier == HOT:
        return HOT
    score = float(cvss or 0.0)
    if verdict == "affected" and score >= HIGH_CVSS:
        return HOT
    return tier


def parse_version(value: str, strict: bool = False) -> tuple[int, ...] | None:
    """Parse a dotted version string into a comparable tuple.

    A leading dpkg/rpm epoch ("1:") is dropped, a "v" prefix is ignored,
    pre-release markers become negative components so ``2.0-beta9``
    sorts before ``2.0``, and a git commit hash is not a version. With
    ``strict`` (a bound from a feed, not a banner) the text must start
    with a digit so refs like ``main`` never parse as a version.

    Args:
        value: Raw version text.
        strict: Require the text to start with a digit.

    Returns:
        Tuple of ints, or None when no version can be parsed.
    """
    text = _EPOCH_RE.sub("", str(value or "")).strip()
    if text[:1] in ("v", "V") and text[1:2].isdigit():
        text = text[1:]
    if not text:
        return None
    if _HASH_RE.match(text) and not text.isdigit():
        return None
    match = _VER_RE.match(text) if strict else _VER_RE.search(text)
    if not match:
        return None
    try:
        parts = [int(part) for part in match.group(1).split(".")]
    except ValueError:
        return None
    pre = _PRE_RE.match(text[match.end():])
    if pre and (pre.group(1) or pre.group(3)):
        parts += [_PRE_RANK[(pre.group(1) or pre.group(2)).lower()], int(pre.group(3) or 0)]
    return tuple(parts)


def compare_versions(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    """Compare two version tuples zero-padded so (1, 18) == (1, 18, 0)."""
    size = max(len(a), len(b))
    a = a + (0,) * (size - len(a))
    b = b + (0,) * (size - len(b))
    return (a > b) - (a < b)


def version_in_range(ver: tuple[int, ...] | None, rng: dict) -> bool | None:
    """Return True/False/None for ``ver`` inside one affected range.

    A range with no usable bound is unknown, never "in range": only a
    real bound can put a version inside it. GIT ranges are commit
    hashes and can never be compared with a version.

    Args:
        ver: Parsed version tuple or None.
        rng: Range dict with ``type``, ``introduced``, ``fixed``, ``lastAffected``.

    Returns:
        True when in range, False when out, None when unknown.
    """
    if ver is None:
        return None
    if str(rng.get("type") or "SEMVER").upper() not in ("SEMVER", "ECOSYSTEM"):
        return None
    bounds = [(rng.get(k), parse_version(rng.get(k), strict=True)) for k in ("introduced", "fixed", "lastAffected")]
    if any(raw and parsed is None for raw, parsed in bounds):
        return None
    introduced, fixed, last = (parsed for _raw, parsed in bounds)
    if introduced is None and fixed is None and last is None:
        return None
    if introduced is not None and compare_versions(ver, introduced) < 0:
        return False
    if fixed is not None and compare_versions(ver, fixed) >= 0:
        return False
    if last is not None and compare_versions(ver, last) > 0:
        return False
    return True


_CVSS_V3_METRICS = {
    "AV": {"N": 0.85, "A": 0.65, "L": 0.39, "P": 0.55},
    "AC": {"L": 0.77, "H": 0.44},
    "C": {"H": 0.56, "L": 0.22, "N": 0.0},
    "I": {"H": 0.56, "L": 0.22, "N": 0.0},
    "A": {"H": 0.56, "L": 0.22, "N": 0.0},
}


def cvss3_base_score(vector: str) -> float:
    """Compute the CVSS v3 base score from an inline vector string.

    Args:
        vector: ``CVSS:3.x/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`` form.

    Returns:
        Base score rounded up to one decimal, 0.0 when unparseable.
    """
    parts: dict[str, str] = {}
    scope_changed = "S:C" in str(vector)
    for chunk in str(vector or "").split("/"):
        if ":" in chunk:
            key, value = chunk.split(":", 1)
            parts[key.upper()] = value.upper()
    try:
        av = _CVSS_V3_METRICS["AV"][parts.get("AV", "")]
        ac = _CVSS_V3_METRICS["AC"][parts.get("AC", "")]
        c = _CVSS_V3_METRICS["C"][parts.get("C", "N")]
        i = _CVSS_V3_METRICS["I"][parts.get("I", "N")]
        a = _CVSS_V3_METRICS["A"][parts.get("A", "N")]
    except KeyError:
        return 0.0
    pr_map_changed = {"L": 0.68, "H": 0.5, "U": 0.85}
    pr_map_unchanged = {"L": 0.62, "H": 0.27, "U": 0.85}
    ui = 0.85 if parts.get("UI", "N") == "N" else 0.62
    pr = (pr_map_changed if scope_changed else pr_map_unchanged).get(parts.get("PR", "U"), 0.85)
    iss = 1.0 - (1.0 - c) * (1.0 - i) * (1.0 - a)
    if scope_changed:
        impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15
    else:
        impact = 6.42 * iss
    exploitability = 8.22 * av * ac * pr * ui
    if impact <= 0:
        return 0.0
    if scope_changed:
        score = min(1.08 * (impact + exploitability), 10.0)
    else:
        score = min(impact + exploitability, 10.0)
    return min(10.0, int(score * 10 + 0.999) / 10.0)


def product_token(value: str) -> str:
    """Normalise a product name to one comparable token.

    Generic infrastructure words (``cms``, ``server``, ``api``...) are
    dropped first, so ``cms server`` normalises to nothing while
    ``Apache httpd`` normalises to ``apachehttpd``. Word boundaries
    survive normalisation: callers compare the token with
    :func:`token_matches` so ``cms`` never matches inside ``datocms``.

    Args:
        value: Raw product/banner text.

    Returns:
        Lowercase alphanumeric token, or "" when too generic or short.
    """
    words = re.findall(r"[A-Za-z0-9]+", str(value or "").lower())
    kept = [w for w in words if w not in GENERIC_WORDS and not w.isdigit()]
    token = "".join(kept)
    if len(token) < _MIN_TOKEN_LEN:
        return ""
    return token


def token_matches(haystack: str, needle: str) -> bool:
    """Whole-token containment of ``needle`` inside ``haystack``.

    Args:
        haystack: Normalised product string.
        needle: Normalised product token.

    Returns:
        True when ``needle`` is a whole run of characters of
        ``haystack`` or equal to it.
    """
    if not haystack or not needle:
        return False
    if haystack == needle:
        return True
    for boundary in (f".{needle}.", f"{needle}.", f".{needle}"):
        if boundary in haystack:
            return True
    return False


# -----------------------------------------------------------------------------
# Distro backports
# -----------------------------------------------------------------------------

_UBUNTU_REV = re.compile(r"\d+ubuntu[\d.]+")
_DEBIAN_REV = re.compile(r"[\w.+~]*[+~]deb(\d+)u\d+")
_RHEL_REV = re.compile(r"\.el(\d+)(?:_\d+)?")
_ALPINE_REV = re.compile(r"-r\d+$")
_NMAP_FORM = re.compile(r"^(?P<up>\S+)\s+(?:Ubuntu|Debian)[-\s]+(?P<rev>\S+)", re.IGNORECASE)
_DPKG_FORM = re.compile(r"^(?:\d+:)?\d[\w.+~]*-[\w.+~]+$")
_OS_CPE = re.compile(r"cpe:/o:(?P<vendor>[a-z_]+):(?P<product>[a-z_]+)(?::(?P<ver>[\w.]+))?", re.IGNORECASE)


def parse_distro_revision(banner: str) -> dict:
    """Read the distro family and package release from a service banner.

    Understands nmap's ``8.9p1 Ubuntu 3ubuntu0.6`` form, dpkg/rpm
    release suffixes (``1:8.9p1-3ubuntu0.10``, ``2.4.57-2``,
    ``1.0.9-2.el8``) and OS CPEs.

    Args:
        banner: Product/version/extrainfo text a scanner captured.

    Returns:
        ``{"family": ..., "revision": ...}`` with "" when unknown.
    """
    text = str(banner or "").strip()
    family, revision = "", ""
    nmap = _NMAP_FORM.search(text)
    if nmap and (_UBUNTU_REV.search(nmap.group("rev")) or _DEBIAN_REV.search(nmap.group("rev"))):
        family = "ubuntu" if "ubuntu" in nmap.group("rev").lower() or "ubuntu" in text.lower() else "debian"
        revision = nmap.group("rev")
    if not revision:
        dpkg = _DPKG_FORM.match(text)
        if dpkg:
            rev = _UBUNTU_REV.search(text) or _DEBIAN_REV.search(text)
            if rev:
                family = "ubuntu" if _UBUNTU_REV.search(text) else "debian"
                revision = rev.group(0)
            elif _RHEL_REV.search(text):
                family = "rhel"
                revision = _RHEL_REV.search(text).group(0)
            elif _ALPINE_REV.search(text):
                family = "alpine"
                revision = _ALPINE_REV.search(text).group(0)
    if not family:
        cpe = _OS_CPE.search(text)
        if cpe:
            family = cpe.group("vendor") or ""
    return {"family": family, "revision": revision}


def backport_status(banner: str, fixed_revision: str = "") -> str:
    """Classify whether a distro already backported the fix.

    A revision the distro patched is recognised by comparing the
    package release against the known fixed revision; without fixed
    data the status is NO_DATA and correlation must never drop the
    match because of it.

    Args:
        banner: Product/version/extrainfo text.
        fixed_revision: Distro revision that carries the fix ("" = unknown).

    Returns:
        One of PATCHED, VULNERABLE, UNKNOWN, NO_DATA.
    """
    if not fixed_revision:
        return NO_DATA
    parsed = parse_distro_revision(banner)
    revision = parsed.get("revision", "")
    if not revision:
        return UNKNOWN
    a = parse_version(revision)
    b = parse_version(fixed_revision)
    if a is None or b is None:
        return UNKNOWN
    return PATCHED if compare_versions(a, b) >= 0 else VULNERABLE


def label_for(status: str, fixed_revision: str = "") -> str:
    """Human-readable label for one backport status."""
    if status == PATCHED:
        return "patched by distro" + (f" (fixed in {fixed_revision})" if fixed_revision else "")
    if status == VULNERABLE:
        return "vulnerable per distro revision" + (f" (fix in {fixed_revision})" if fixed_revision else "")
    if status == UNKNOWN:
        return "version-only, distro unknown"
    return "no distro data"


__all__ = [
    "HOT",
    "WARM",
    "COLD",
    "PATCHED",
    "VULNERABLE",
    "UNKNOWN",
    "NO_DATA",
    "HIGH_CVSS",
    "CRITICAL_CVSS",
    "EPSS_THRESHOLD",
    "HEAT_RANK",
    "SEVERITY_FROM_HEAT",
    "SEVERITY_HEAT",
    "classify_heat",
    "match_heat",
    "parse_version",
    "compare_versions",
    "version_in_range",
    "cvss3_base_score",
    "product_token",
    "token_matches",
    "parse_distro_revision",
    "backport_status",
    "label_for",
]
