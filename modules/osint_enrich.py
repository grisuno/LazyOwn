"""Keyless OSINT enrichment for finding evidence.

VirusTotal has no keyless API, so this module assembles the same answers
from sources that need no API key at all:

- CVE advisories: OSV (https://api.osv.dev, no key, POST).
- Exploited in the wild: CISA KEV catalog (public JSON feed, no key).
- Exploit probability: EPSS scores from FIRST (https://api.first.org, no key).
- Host intel: HackerTarget free endpoints + DNS-over-HTTPS + ip-api
  community rate limit (all keyless), urlscan.io public search (no key).

Every lookup is cached under ``sessions/osint_cache.json`` (7-day TTL,
KEV catalog 24h) and fails silent: enrichment must never break the loop.
Stdlib only (urllib).
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE_FILENAME = "osint_cache.json"
CACHE_TTL_SEC = 7 * 24 * 3600
KEV_TTL_SEC = 24 * 3600
HTTP_TIMEOUT_SEC = 6.0
USER_AGENT = "LazyOwn-intel/1.0 (keyless-osint)"

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

CVE_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)

OSV_URL = "https://api.osv.dev/v1/query"
KEV_URL = ("https://www.cisa.gov/sites/default/files/feeds/"
           "known_exploited_vulnerabilities.json")
EPSS_URL = "https://api.first.org/data/v1/epss"
HACKERTARGET_URL = "https://api.hackertarget.com/{tool}/"
DNS_GOOGLE_URL = "https://dns.google/resolve"
IP_API_URL = "http://ip-api.com/json/{ip}"
URLSCAN_URL = "https://urlscan.io/api/v1/search/"


def _cache_path(sessions_dir: str | Path) -> Path:
    """Return the OSINT disk-cache path for a sessions directory."""
    return Path(str(sessions_dir)) / CACHE_FILENAME


def _cache_load(sessions_dir: str | Path) -> dict:
    """Load the cache, tolerating missing or corrupt files."""
    try:
        data = json.loads(_cache_path(sessions_dir).read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _cache_save(sessions_dir: str | Path, data: dict) -> None:
    """Persist the cache best-effort."""
    try:
        _cache_path(sessions_dir).write_text(json.dumps(data))
    except OSError:
        pass


def _cached(sessions_dir: str | Path, key: str, ttl: float) -> dict | None:
    """Return a fresh cached entry, else None."""
    entry = _cache_load(sessions_dir).get(key)
    if isinstance(entry, dict) and time.time() - float(entry.get("at", 0)) < ttl:
        return entry.get("data")
    return None


def _store(sessions_dir: str | Path, key: str, data: dict) -> None:
    """Store one cache entry."""
    cache = _cache_load(sessions_dir)
    cache[key] = {"at": time.time(), "data": data}
    _cache_save(sessions_dir, cache)


def _get_json(url: str, params: dict | None = None) -> dict | list | None:
    """GET a JSON document, returning None on any failure."""
    try:
        query = ("?" + urllib.parse.urlencode(params)) if params else ""
        request = urllib.request.Request(
            url + query, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SEC) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except Exception:
        return None


def _post_json(url: str, payload: dict) -> dict | None:
    """POST a JSON document, returning the decoded response or None."""
    try:
        body = json.dumps(payload).encode()
        request = urllib.request.Request(
            url, data=body, headers={"User-Agent": USER_AGENT,
                                     "Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SEC) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
            return data if isinstance(data, dict) else None
    except Exception:
        return None


def _get_text(url: str, params: dict | None = None) -> str | None:
    """GET a plain-text document, returning None on any failure."""
    try:
        query = ("?" + urllib.parse.urlencode(params)) if params else ""
        request = urllib.request.Request(
            url + query, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SEC) as resp:
            return resp.read().decode("utf-8", "replace").strip()
    except Exception:
        return None


def cve_lookup(cve_id: str, sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Assemble OSV advisory + KEV flag + EPSS score for one CVE id."""
    cve = str(cve_id).upper().strip()
    cached = _cached(sessions_dir, f"cve:{cve}", CACHE_TTL_SEC)
    if cached is not None:
        return cached
    result: dict = {"cve": cve, "summary": "", "severity": "",
                    "kev": False, "epss": None}
    osv = _post_json(OSV_URL, {"package": {}, "version": "0", "findings": [],
                               "commit": "", "cve": cve}) or {}
    vulns = osv.get("vulns") or []
    if vulns:
        first = vulns[0] if isinstance(vulns[0], dict) else {}
        result["summary"] = str(first.get("summary", "") or "")[:300]
        for sev in first.get("severity", []) or []:
            if isinstance(sev, dict) and sev.get("score"):
                result["severity"] = f"{sev.get('type', '')} {sev.get('score')}"
                break
    kev = _cached(sessions_dir, "kev:catalog", KEV_TTL_SEC)
    if kev is None:
        feed = _get_json(KEV_URL) or {}
        vulns_feed = feed.get("vulnerabilities") or []
        kev = {str(v.get("cveID", "")).upper() for v in vulns_feed
               if isinstance(v, dict)}
        _store(sessions_dir, "kev:catalog", {"ids": sorted(kev)})
    else:
        kev = set(kev.get("ids") or [])
    result["kev"] = cve in kev
    epss = _get_json(EPSS_URL, {"cve": cve})
    try:
        items = (epss or {}).get("data") or []
        if items and isinstance(items[0], dict):
            result["epss"] = float(items[0].get("epss", 0.0))
    except (TypeError, ValueError):
        pass
    _store(sessions_dir, f"cve:{cve}", result)
    return result


def reverse_dns(ip: str, sessions_dir: str | Path = SESSIONS_DIR) -> str:
    """Best-effort PTR hostname for an IP (HackerTarget, then DoH)."""
    key = f"ptr:{ip}"
    cached = _cached(sessions_dir, key, CACHE_TTL_SEC)
    if cached is not None:
        return str(cached.get("ptr", ""))
    name = _get_text(HACKERTARGET_URL.format(tool="reversedns"), {"q": ip}) or ""
    name = name.splitlines()[0].strip() if name else ""
    if not name or "error" in name.lower() or "/" in name:
        try:
            octets = str(ip).split(".")
            arpa = ".".join(reversed(octets)) + ".in-addr.arpa"
            answer = _get_json(DNS_GOOGLE_URL, {"name": arpa, "type": "PTR"}) or {}
            answers = answer.get("Answer") or []
            if answers and isinstance(answers[0], dict):
                name = str(answers[0].get("data", "")).rstrip(".")
        except Exception:
            name = ""
    _store(sessions_dir, key, {"ptr": name})
    return name


def host_geo(ip: str, sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Country/org/ISP for an IP via the keyless ip-api endpoint."""
    key = f"geo:{ip}"
    cached = _cached(sessions_dir, key, CACHE_TTL_SEC)
    if cached is not None:
        return cached
    data = _get_json(IP_API_URL.format(ip=urllib.parse.quote(str(ip))),
                     {"fields": "status,country,org,isp,query"}) or {}
    result = {"country": str(data.get("country", "")),
              "org": str(data.get("org", "")),
              "isp": str(data.get("isp", ""))} if data.get("status") == "success" else {}
    _store(sessions_dir, key, result)
    return result


def domain_exposure(domain: str, sessions_dir: str | Path = SESSIONS_DIR) -> int:
    """Count public urlscan.io results for a domain (no key needed)."""
    key = f"urlscan:{domain}"
    cached = _cached(sessions_dir, key, CACHE_TTL_SEC)
    if cached is not None:
        return int(cached.get("total", 0))
    data = _get_json(URLSCAN_URL, {"q": f"domain:{domain}"}) or {}
    try:
        total = int(data.get("total", 0))
    except (TypeError, ValueError):
        total = 0
    _store(sessions_dir, key, {"total": total})
    return total


def enrich_evidence(items: list[str], sessions_dir: str | Path = SESSIONS_DIR) -> list[str]:
    """Append keyless OSINT verdicts to CVE mentions inside evidence items."""
    out = list(items)
    seen: set[str] = set()
    for item in items:
        for match in CVE_RE.findall(str(item)):
            cve = match.upper()
            if cve in seen:
                continue
            seen.add(cve)
            try:
                verdict = cve_lookup(cve, sessions_dir)
            except Exception:
                continue
            bits = [cve]
            if verdict.get("severity"):
                bits.append(str(verdict["severity"]))
            if verdict.get("kev"):
                bits.append("CISA-KEV exploited-in-the-wild")
            if verdict.get("epss") is not None:
                try:
                    bits.append(f"EPSS {float(verdict['epss']):.3f}")
                except (TypeError, ValueError):
                    pass
            if verdict.get("summary"):
                bits.append(str(verdict["summary"])[:160])
            out.append("osint: " + " | ".join(bits))
    return out


__all__ = [
    "CACHE_FILENAME",
    "cve_lookup",
    "domain_exposure",
    "enrich_evidence",
    "host_geo",
    "reverse_dns",
]
