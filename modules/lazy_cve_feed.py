"""Keyless CVE intelligence feeds and version-aware service correlation.

Correlates discovered services against public exploit intelligence with
no account and no API key, then grades every candidate with a
deterministic heat tier (see :mod:`modules.lazy_heat`):

  cisa_kev    CISA Known Exploited Vulnerabilities catalog (JSON)
  epss        FIRST EPSS probability scores (daily CSV, gzipped)
  exploit_db  Exploit-DB public exploit index (CSV)
  metasploit  Metasploit module metadata (JSON)
  osv         OSV.dev advisories for version ranges (per-product, cached)

A source only ever adds evidence: being absent from one source never
clears what another reported. Every download is bounded, cached on disk
under ``sessions/cve_feed/`` with its own TTL, and every entry point
degrades to empty results when the network or the feed is unavailable,
so the autonomous loop never stalls on intelligence.

Stdlib only.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import os
import re
import time
import urllib.request
from pathlib import Path

from modules.lazy_heat import (
    COLD,
    HOT,
    HEAT_RANK,
    SEVERITY_FROM_HEAT,
    WARM,
    classify_heat,
    cvss3_base_score,
    match_heat,
    parse_version,
    product_token,
    token_matches,
    version_in_range,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSIONS_DIR = REPO_ROOT / "sessions"
CACHE_DIR = SESSIONS_DIR / "cve_feed"

USER_AGENT = "LazyOwn intel feed (self-hosted red-team framework)"
HTTP_TIMEOUT_SEC = 20
MAX_DOWNLOAD_BYTES = 64 * 1024 * 1024

KEV_TTL_SEC = 24 * 3600
EPSS_TTL_SEC = 12 * 3600
EXPLOIT_TTL_SEC = 24 * 3600
MSF_TTL_SEC = 24 * 3600
OSV_TTL_SEC = 7 * 24 * 3600

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_URL = "https://epss.empiricalsecurity.com/epss_scores-current.csv.gz"
EXPLOITDB_URL = "https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv"
MSF_URL = "https://raw.githubusercontent.com/rapid7/metasploit-framework/master/db/modules_metadata_base.json"
OSV_QUERY_URL = "https://api.osv.dev/v1/query"

OSV_PAGE_MAX = 3
OSV_PAGE_SIZE = 100
CORRELATE_CAP = 40

_CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)

# KEV product labels that name a known service product, lowercase keyed.
_KEV_PRODUCT_ALIASES = {
    "apache http server": "apache",
    "apache tomcat": "tomcat",
    "exim": "exim",
    "microsoft exchange": "exchange",
    "microsoft iis": "iis",
    "microsoft sharepoint": "sharepoint",
    "samba": "samba",
    "vmware esxi": "esxi",
    "vmware vcenter": "vcenter",
    "zoho manageengine": "manageengine",
}


def _env_flag(name: str, default: str = "1") -> bool:
    """Return True when an env toggle is not explicitly disabled."""
    return os.environ.get(name, default).strip().lower() not in ("0", "false", "no")


def _cache_path(name: str) -> Path:
    """Return the cache file path for one feed, ensuring the directory."""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    return CACHE_DIR / name


def _cache_fresh(path: Path, ttl_sec: int) -> bool:
    """Return True when a cache file exists and is younger than the TTL."""
    try:
        return path.exists() and (time.time() - path.stat().st_mtime) < ttl_sec
    except OSError:
        return False


def _fetch(url: str) -> bytes | None:
    """Download a feed with a byte cap; None on any failure."""
    if not _env_flag("LAZYOWN_CVE_FEEDS"):
        return None
    try:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        chunks: list[bytes] = []
        total = 0
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SEC) as resp:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    return None
                chunks.append(chunk)
        return b"".join(chunks)
    except Exception:
        return None


def _store_bytes(name: str, payload: bytes) -> None:
    """Persist one feed payload best-effort."""
    try:
        _cache_path(name).write_bytes(payload)
    except OSError:
        pass


def _store_json(name: str, data) -> None:
    """Persist one JSON document best-effort."""
    try:
        _cache_path(name).write_text(json.dumps(data), encoding="utf-8")
    except (OSError, TypeError, ValueError):
        pass


def _load_json(name: str):
    """Load one cached JSON document or None."""
    try:
        return json.loads(_cache_path(name).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def load_kev(force: bool = False) -> dict[str, dict]:
    """Return ``{cve_id: {product, vendor}}`` from the CISA KEV catalog.

    Args:
        force: Re-download even when the cache is fresh.

    Returns:
        Mapping keyed by upper CVE id; empty when offline.
    """
    cache = _cache_path("kev.json")
    if not force and _cache_fresh(cache, KEV_TTL_SEC):
        data = _load_json("kev.json")
        if isinstance(data, dict):
            return {k: v for k, v in data.items()}
    raw = _fetch(KEV_URL)
    if raw:
        try:
            doc = json.loads(raw.decode("utf-8", "replace"))
            out = {}
            for row in doc.get("vulnerabilities", []) or []:
                cve = str(row.get("cveID", "")).upper()
                if cve:
                    out[cve] = {
                        "product": str(row.get("product", "")).strip(),
                        "vendor": str(row.get("vendorProject", "")).strip(),
                    }
            _store_json("kev.json", out)
            return out
        except (ValueError, AttributeError):
            pass
    data = _load_json("kev.json")
    return {k: v for k, v in (data or {}).items()} if isinstance(data, dict) else {}


def load_epss(force: bool = False) -> dict[str, float]:
    """Return ``{cve_id: epss}`` from the FIRST daily EPSS scores.

    Args:
        force: Re-download even when the cache is fresh.

    Returns:
        Mapping keyed by upper CVE id; empty when offline.
    """
    cache = _cache_path("epss.csv.gz")
    if not force and _cache_fresh(cache, EPSS_TTL_SEC):
        data = _load_json("epss.json")
        if isinstance(data, dict):
            return {k: float(v) for k, v in data.items()}
    raw = _fetch(EPSS_URL)
    if raw:
        try:
            text = gzip.decompress(raw).decode("utf-8", "replace")
        except (OSError, ValueError):
            text = ""
        out: dict[str, float] = {}
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            cve = str(row.get("cve", "")).upper()
            try:
                out[cve] = float(row.get("epss", "") or 0.0)
            except ValueError:
                continue
        if out:
            _store_bytes(cache, raw)
            _store_json("epss.json", out)
            return out
    data = _load_json("epss.json")
    return {k: float(v) for k, v in (data or {}).items()} if isinstance(data, dict) else {}


def _exploit_cves_from_text(text: str) -> set[str]:
    """Extract upper CVE ids from feed text."""
    return {m.upper() for m in _CVE_RE.findall(text or "")}


def load_exploit_cves(force: bool = False) -> set[str]:
    """Return CVE ids with public exploit code (Exploit-DB index).

    Args:
        force: Re-download even when the cache is fresh.

    Returns:
        Set of upper CVE ids; empty when offline.
    """
    cache = _cache_path("exploitdb.csv")
    if not force and _cache_fresh(cache, EXPLOIT_TTL_SEC):
        data = _load_json("exploitdb.json")
        if isinstance(data, dict):
            return {str(k) for k in data.get("ids", [])}
    raw = _fetch(EXPLOITDB_URL)
    if raw:
        ids = _exploit_cves_from_text(raw.decode("utf-8", "replace"))
        _store_bytes(cache, raw)
        _store_json("exploitdb.json", {"ids": sorted(ids)})
        return ids
    data = _load_json("exploitdb.json")
    return {str(k) for k in (data or {}).get("ids", [])} if isinstance(data, dict) else set()


def load_msf_cves(force: bool = False) -> set[str]:
    """Return CVE ids weaponized as Metasploit modules.

    Args:
        force: Re-download even when the cache is fresh.

    Returns:
        Set of upper CVE ids; empty when offline.
    """
    cache = _cache_path("msf.json")
    if not force and _cache_fresh(cache, MSF_TTL_SEC):
        data = _load_json("msf.json")
        if isinstance(data, dict):
            return {str(k) for k in data.get("ids", [])}
    raw = _fetch(MSF_URL)
    if raw:
        ids = _exploit_cves_from_text(raw.decode("utf-8", "replace"))
        _store_bytes(cache, raw)
        _store_json("msf.json", {"ids": sorted(ids)})
        return ids
    data = _load_json("msf.json")
    return {str(k) for k in (data or {}).get("ids", [])} if isinstance(data, dict) else set()


def _osv_cache_path(product: str) -> Path:
    """Return the per-product OSV cache path."""
    token = re.sub(r"[^a-z0-9_-]+", "_", str(product or "").lower()).strip("_") or "unknown"
    return _cache_path(f"osv_{token}.json")


# Distro ecosystems OSV answers for; queried in order, merged.
OSV_ECOSYSTEMS = ("Debian", "Ubuntu:20.04:LTS", "Alpine:v3.14")


def fetch_product_advisories(product: str, force: bool = False) -> list[dict]:
    """Fetch OSV advisories naming one product.

    The query endpoint requires an ecosystem, so candidate package
    names (each banner word plus the joined token) are tried against
    each candidate distro ecosystem and the answers merged; the merged
    set is cached per product with the OSV TTL.

    Args:
        product: Product text as found on a banner (``Samba smbd 3.0.20``).
        force: Re-query even when the cache is fresh.

    Returns:
        List of advisory dicts with ``affected`` ranges; [] offline.
    """
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z0-9_.-]*", str(product or "").lower())]
    names: list[str] = []
    for word in words:
        token = product_token(word)
        if token and len(token) >= 4 and token not in names:
            names.append(token)
    whole = product_token(product)
    if whole and len(whole) >= 4 and whole not in names:
        names.append(whole)
    if not names:
        return []
    cache = _osv_cache_path(names[0] if len(names) == 1 else whole)
    if not force and _cache_fresh(cache, OSV_TTL_SEC):
        try:
            data = json.loads(cache.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        if isinstance(data, dict):
            return list(data.get("vulns", []) or [])
    if not _env_flag("LAZYOWN_CVE_FEEDS"):
        return []
    seen: set[str] = set()
    vulns: list[dict] = []
    for name in names[:3]:
        for ecosystem in OSV_ECOSYSTEMS:
            try:
                pkg: dict = {"name": name}
                if ecosystem:
                    pkg["ecosystem"] = ecosystem
                payload = json.dumps({"package": pkg}).encode("utf-8")
                request = urllib.request.Request(
                    OSV_QUERY_URL,
                    data=payload,
                    headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
                )
                with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SEC) as resp:
                    doc = json.loads(resp.read().decode("utf-8", "replace"))
            except Exception:
                continue
            for advisory in doc.get("vulns") or []:
                if not isinstance(advisory, dict):
                    continue
                key = str(advisory.get("id", "")) or str(advisory.get("aliases", ["?"])[0])
                if key in seen:
                    continue
                seen.add(key)
                vulns.append(advisory)
    try:
        cache.write_text(json.dumps({"vulns": vulns[:200]}), encoding="utf-8")
    except OSError:
        pass
    return vulns


def cve_intel(cve_id: str, feeds: dict | None = None, allow_network: bool = True) -> dict:
    """Assemble exploitation signals and the heat tier for one CVE.

    Args:
        cve_id: CVE id (``CVE-2021-41773``).
        feeds: Preloaded feeds (``kev``/``epss``/``exploit``/``msf``); loaded lazily when None.
        allow_network: Allow feed downloads on a cold cache.

    Returns:
        ``{"cve", "kev", "epss", "exploit", "msf", "cvss", "heat"}``.
    """
    cve = str(cve_id or "").upper().strip()
    feeds = feeds or {}
    kev_rows = feeds.get("kev") if feeds.get("kev") is not None else (
        load_kev() if allow_network else (load_kev() if _cache_fresh(_cache_path("kev.json"), KEV_TTL_SEC) else {})
    )
    epss_rows = feeds.get("epss") if feeds.get("epss") is not None else (
        load_epss()
        if allow_network or _cache_fresh(_cache_path("epss.json"), EPSS_TTL_SEC) or _cache_fresh(_cache_path("epss.csv.gz"), EPSS_TTL_SEC)
        else {}
    )
    exploit_ids = feeds.get("exploit") if feeds.get("exploit") is not None else (
        load_exploit_cves()
        if allow_network or _cache_fresh(_cache_path("exploitdb.json"), EXPLOIT_TTL_SEC)
        else set()
    )
    msf_ids = feeds.get("msf") if feeds.get("msf") is not None else (
        load_msf_cves() if allow_network or _cache_fresh(_cache_path("msf.json"), MSF_TTL_SEC) else set()
    )
    kev = cve in kev_rows
    epss = epss_rows.get(cve)
    exploit = cve in exploit_ids
    msf = cve in msf_ids
    cvss = 0.0
    heat = classify_heat(kev=kev, epss=epss, exploit=exploit or msf, cvss=cvss)
    return {"cve": cve, "kev": kev, "epss": epss, "exploit": exploit, "msf": msf, "cvss": cvss, "heat": heat}


def _advisory_cve_id(advisory: dict) -> str:
    """Best CVE id from one OSV advisory (aliases first, then its own id)."""
    for source in list(advisory.get("aliases", []) or []) + [str(advisory.get("id", ""))]:
        match = re.search(r"CVE-\d{4}-\d{4,7}", str(source or ""), re.IGNORECASE)
        if match:
            return match.group(0).upper()
    return ""


def _advisory_cvss(advisory: dict) -> float:
    """Best CVSS v3 base score from one OSV advisory."""
    best = 0.0
    for sev in advisory.get("severity", []) or []:
        if not isinstance(sev, dict):
            continue
        vector = str(sev.get("vector", "") or "")
        if "CVSS:3" in vector:
            score = cvss3_base_score(vector)
            if score > best:
                best = score
    return best


def _advisory_matches_product(advisory: dict, banner_words: list[str]) -> bool:
    """Whole-token product match over an advisory's affected packages."""
    for affected in advisory.get("affected", []) or []:
        if not isinstance(affected, dict):
            continue
        pkg = affected.get("package", {}) or {}
        names = " ".join([str(pkg.get("name", "")), str(affected.get("database_specific", {}))])
        for word in re.findall(r"[a-z][a-z0-9_-]{2,}", names.lower()):
            token = product_token(word)
            if not token:
                continue
            for candidate in banner_words:
                if token_matches(token, candidate) or token_matches(candidate, token):
                    return True
    return False


def correlate(product: str, version: str = "", allow_network: bool = True) -> list[dict]:
    """Version-aware CVE candidates for one service product.

    Candidates come from OSV advisories (which carry affected version
    ranges) filtered by :func:`version_in_range`, plus KEV product
    matches KEV lists under the same vendor product. Every candidate is
    heat-graded; a match inside the affected range reads as affected.

    Args:
        product: Product name from a banner (``vsftpd``, ``OpenSSH``).
        version: Product version when known.
        allow_network: Allow OSV queries on a cold cache.

    Returns:
        List of ``{"cve", "heat", "cvss", "kev", "epss", "exploit",
        "in_range", "confidence", "severity"}`` sorted hottest first,
        capped at :data:`CORRELATE_CAP`.
    """
    token = product_token(product)
    if not token:
        return []
    banner_words = [product_token(w) for w in re.findall(r"[A-Za-z][A-Za-z0-9_.-]*", str(product or ""))]
    banner_words = [w for w in banner_words if w] or [token]
    feeds = {
        "kev": load_kev() if allow_network else ({k: v for k, v in (_load_json("kev.json") or {}).items()} if _cache_fresh(_cache_path("kev.json"), KEV_TTL_SEC) else {}),
        "epss": load_epss() if allow_network else ({k: float(v) for k, v in (_load_json("epss.json") or {}).items()} if _cache_fresh(_cache_path("epss.json"), EPSS_TTL_SEC) else {}),
        "exploit": load_exploit_cves() if allow_network else ({str(k) for k in (_load_json("exploitdb.json") or {}).get("ids", [])} if _cache_fresh(_cache_path("exploitdb.json"), EXPLOIT_TTL_SEC) else set()),
        "msf": load_msf_cves() if allow_network else ({str(k) for k in (_load_json("msf.json") or {}).get("ids", [])} if _cache_fresh(_cache_path("msf.json"), MSF_TTL_SEC) else set()),
    }
    ver = parse_version(version) if version else None
    out: dict[str, dict] = {}
    for advisory in fetch_product_advisories(product, force=False) if allow_network else []:
        if not _advisory_matches_product(advisory, banner_words):
            continue
        cve = _advisory_cve_id(advisory)
        if not cve:
            continue
        in_range: bool | None = None
        if ver is not None:
            for affected in advisory.get("affected", []) or []:
                if not isinstance(affected, dict):
                    continue
                for converted in convert_osv_ranges(affected):
                    result = version_in_range(ver, converted)
                    if result is True:
                        in_range = True
                        break
                if in_range is True:
                    break
        intel = cve_intel(cve, feeds=feeds, allow_network=False)
        cvss = _advisory_cvss(advisory) or intel["cvss"]
        if cvss:
            intel["heat"] = classify_heat(kev=intel["kev"], epss=intel["epss"], exploit=intel["exploit"] or intel["msf"], cvss=cvss)
        confidence = {True: 0.9, False: 0.0, None: 0.5}[in_range] if ver is not None else 0.5
        if intel["heat"] == COLD and in_range is False:
            continue
        out[cve] = {
            "cve": cve,
            "heat": intel["heat"],
            "cvss": cvss,
            "kev": intel["kev"],
            "epss": intel["epss"],
            "exploit": intel["exploit"] or intel["msf"],
            "in_range": in_range,
            "confidence": confidence,
            "severity": SEVERITY_FROM_HEAT.get(intel["heat"], "info"),
        }
    for cve, meta in load_kev_matches(token, feeds):
        if cve not in out:
            out[cve] = {**meta, "in_range": None, "confidence": 0.6, "cvss": meta.get("cvss", 0.0)}
    ranked = sorted(out.values(), key=lambda row: (-HEAT_RANK.get(row.get("heat", COLD), 0), -float(row.get("cvss", 0.0))))
    return ranked[:CORRELATE_CAP]


_KEV_MATCH_CACHE: dict[str, list[tuple[str, dict]]] = {}


def convert_osv_ranges(affected: dict) -> list[dict]:
    """Convert one OSV ``affected`` entry into version-range dicts.

    Args:
        affected: One OSV affected entry (``package`` plus ``ranges``).

    Returns:
        List of range dicts shaped for :func:`version_in_range`
        (``type/introduced/fixed/lastAffected``), possibly empty.
    """
    converted: list[dict] = []
    for rng in (affected or {}).get("ranges", []) or []:
        if not isinstance(rng, dict):
            continue
        built = {
            "type": rng.get("type", ""),
            "introduced": (rng.get("events") or [""])[0].get("introduced", ""),
            "fixed": "",
            "lastAffected": "",
        }
        for event in rng.get("events", []) or []:
            if isinstance(event, dict) and event.get("fixed"):
                built["fixed"] = str(event.get("fixed"))
            if isinstance(event, dict) and event.get("last_affected"):
                built["lastAffected"] = str(event.get("last_affected"))
        converted.append(built)
    return converted


def _cached_advisories() -> list[dict]:
    """Return advisories from the offline OSV cache files.

    Returns:
        Merged advisory list (possibly empty) without touching network.
    """
    merged: list[dict] = []
    try:
        cache_dir = _cache_path("osv_unknown.json").parent
        for cache in sorted(cache_dir.glob("osv_*.json")):
            try:
                data = json.loads(cache.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(data, dict):
                merged.extend(advisory for advisory in (data.get("vulns") or []) if isinstance(advisory, dict))
    except Exception:
        return []
    return merged


def range_for_cve(cve_id: str, allow_network: bool = False) -> dict:
    """Return the OSV affected ranges bound to one CVE, offline-first.

    Args:
        cve_id: CVE identifier (``CVE-2024-...``).
        allow_network: When offline caches carry nothing, this flag is
            reserved for future network lookups and currently forbidden
            to keep the contract fail-soft (always offline data here).

    Returns:
        Range dict shaped for :func:`version_in_range` (first matching
        affected entry), or ``{}`` when unknown.
    """
    wanted = str(cve_id or "").strip().upper()
    if not wanted or allow_network:
        return {}
    for advisory in _cached_advisories():
        identifiers = [str(advisory.get("id", ""))] + [str(a) for a in (advisory.get("aliases") or [])]
        if not any(ident.upper() == wanted for ident in identifiers if ident):
            continue
        for affected in advisory.get("affected", []) or []:
            if not isinstance(affected, dict):
                continue
            ranges = convert_osv_ranges(affected)
            if ranges:
                return ranges[0]
    return {}


def load_kev_matches(product: str, feeds: dict | None = None) -> list[tuple[str, dict]]:
    """KEV entries whose vendor/product names match one service product.

    Matching is word-level: a banner like ``Samba smbd 3.0.20`` matches
    the KEV product ``Samba`` without demanding the whole banner token.

    Args:
        product: Banner product/version text (not a normalised token).
        feeds: Preloaded KEV mapping; loaded when None.

    Returns:
        List of ``(cve, intel)`` pairs, hottest first.
    """
    banner_words = [product_token(w) for w in re.findall(r"[A-Za-z][A-Za-z0-9_.-]*", str(product or ""))]
    banner_words = [w for w in banner_words if w]
    whole = product_token(product)
    if whole and whole not in banner_words:
        banner_words.append(whole)
    if not banner_words:
        return []
    cache_key = " ".join(sorted(banner_words))
    cached = _KEV_MATCH_CACHE.get(cache_key)
    if cached is not None:
        return cached
    kev_rows = feeds.get("kev") if feeds and feeds.get("kev") is not None else load_kev()
    out: list[tuple[str, dict]] = []
    for cve, meta in kev_rows.items():
        name = _KEV_PRODUCT_ALIASES.get(meta.get("product", "").lower(), meta.get("product", "").lower())
        kev_token = product_token(name) or product_token(meta.get("vendor", ""))
        if not kev_token:
            continue
        if any(token_matches(kev_token, candidate) or token_matches(candidate, kev_token) for candidate in banner_words):
            intel = cve_intel(cve, feeds={"kev": kev_rows, "epss": None, "exploit": None, "msf": None}, allow_network=False)
            intel["kev"] = True
            intel["heat"] = HOT
            intel["severity"] = SEVERITY_FROM_HEAT[HOT]
            out.append((cve, intel))
    out.sort(key=lambda pair: -float(pair[1].get("cvss", 0.0)))
    _KEV_MATCH_CACHE[cache_key] = out
    return out


def hot_matches(services: list[dict], allow_network: bool = False) -> list[dict]:
    """Hot/warm CVE candidates matching discovered services.

    Built for the loop's ``cve_hot`` trigger: each service row carries
    ``name``/``product``/``version`` and every returned row carries the
    service context so the planner can target verification intents.

    Args:
        services: ``[{"name", "product", "version", "host", "port"}]``.
        allow_network: Allow OSV queries on a cold cache.

    Returns:
        Match rows ``{"cve", "heat", "product", "version", "host",
        "port", "confidence"}`` hottest first.
    """
    out: list[dict] = []
    for svc in services or []:
        if not isinstance(svc, dict):
            continue
        product = str(svc.get("product", "") or svc.get("name", "") or "")
        matches = correlate(product, str(svc.get("version", "") or ""), allow_network=allow_network)
        for row in matches:
            if row.get("heat") not in (HOT, WARM):
                continue
            out.append(
                {
                    "cve": row["cve"],
                    "heat": row["heat"],
                    "cvss": row.get("cvss", 0.0),
                    "product": product,
                    "version": str(svc.get("version", "") or ""),
                    "host": str(svc.get("host", "") or ""),
                    "port": str(svc.get("port", "") or ""),
                    "confidence": row.get("confidence", 0.5),
                    "severity": row.get("severity", "unknown"),
                }
            )
    out.sort(key=lambda row: (-HEAT_RANK.get(row["heat"], 0), -float(row.get("cvss", 0.0))))
    return out


_FEED_REFRESH_STARTED = False


def refresh_feeds_async(products: list[str] | None = None) -> None:
    """Refresh bulk feeds in one background daemon thread.

    Call once per process (idempotent): KEV, EPSS, Exploit-DB and
    Metasploit re-download only when their TTL expired, and each
    product gets one OSV prefetch so later cache-only correlations
    find candidates without blocking the pipeline on network.

    Args:
        products: Banner strings to prefetch OSV advisories for.
    """
    global _FEED_REFRESH_STARTED
    if _FEED_REFRESH_STARTED:
        return
    _FEED_REFRESH_STARTED = True

    def _worker() -> None:
        try:
            load_kev()
        except Exception:
            pass
        try:
            load_epss()
        except Exception:
            pass
        try:
            load_exploit_cves()
        except Exception:
            pass
        try:
            load_msf_cves()
        except Exception:
            pass
        for product in (products or [])[:20]:
            try:
                fetch_product_advisories(product)
            except Exception:
                continue

    import threading

    try:
        threading.Thread(target=_worker, daemon=True, name="lazy-cve-feed-refresh").start()
    except Exception:
        pass


__all__ = [
    "CACHE_DIR",
    "correlate",
    "cve_intel",
    "cvss3_base_score",
    "fetch_product_advisories",
    "hot_matches",
    "load_epss",
    "load_exploit_cves",
    "load_kev",
    "load_kev_matches",
    "load_msf_cves",
    "refresh_feeds_async",
]
