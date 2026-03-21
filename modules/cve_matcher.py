#!/usr/bin/env python3
"""
modules/cve_matcher.py
=======================
CVE lookup via NVD API 2.0 (no key required for basic queries).

Rate limits:
  Without key : 5 requests / 30 s
  With key    : 50 requests / 30 s  (set NVD_API_KEY env var)

Results are cached on disk under sessions/cve_cache/ (TTL: 1 hour).

Usage:
    from modules.cve_matcher import CVEMatcher

    m = CVEMatcher()
    for cve in m.search("openssh", "8.4"):
        print(cve.id, cve.cvss, cve.description[:80])

    # CLI:
    python3 modules/cve_matcher.py --product openssh --version 8.4 [--max 10] [--json]
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

log = logging.getLogger("cve_matcher")

NVD_API_BASE  = "https://services.nvd.nist.gov/rest/json/cves/2.0"
_CACHE_TTL    = 3600   # seconds
_RATE_NO_KEY  = 6.1    # seconds between requests without API key
_RATE_WITH_KEY = 0.7   # seconds between requests with API key

_BASE_DIR     = Path(__file__).parent.parent
_CACHE_DIR    = _BASE_DIR / "sessions" / "cve_cache"

_last_request_time: float = 0.0


@dataclass
class CVEResult:
    id: str
    cvss: float
    severity: str
    description: str
    published: str
    references: List[str] = field(default_factory=list)


class CVEMatcher:
    """
    Lookup CVEs for a given product/version using the NVD REST API 2.0.

    Parameters
    ----------
    api_key   : NVD API key (optional, falls back to NVD_API_KEY env var).
    cache_dir : directory for on-disk result cache.
    """

    def __init__(
        self,
        api_key: str = "",
        cache_dir: Optional[str | Path] = None,
    ) -> None:
        self.api_key   = api_key or os.environ.get("NVD_API_KEY", "")
        self.rate_delay = _RATE_WITH_KEY if self.api_key else _RATE_NO_KEY
        self.cache_dir  = Path(cache_dir) if cache_dir else _CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    # ── Public API ────────────────────────────────────────────────────────────

    def search(self, *keywords: str, max_results: int = 10) -> List[CVEResult]:
        """Search CVEs by product / version keywords."""
        query = " ".join(k for k in keywords if k and k.strip())
        if not query.strip():
            return []
        return self._query(keywordSearch=query, resultsPerPage=max_results)

    def search_by_cpe(self, cpe_name: str, max_results: int = 10) -> List[CVEResult]:
        """Search CVEs by CPE 2.3 string."""
        return self._query(cpeName=cpe_name, resultsPerPage=max_results)

    # ── Internal ──────────────────────────────────────────────────────────────

    def _cache_path(self, params: dict) -> Path:
        key = urllib.parse.urlencode(sorted(params.items()))
        digest = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{digest}.json"

    def _load_cache(self, params: dict) -> Optional[List[CVEResult]]:
        p = self._cache_path(params)
        if not p.exists():
            return None
        if time.time() - p.stat().st_mtime > _CACHE_TTL:
            return None
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            return [CVEResult(**item) for item in raw]
        except Exception:
            return None

    def _save_cache(self, params: dict, results: List[CVEResult]) -> None:
        try:
            self._cache_path(params).write_text(
                json.dumps([vars(r) for r in results], indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            log.debug("Cache write failed: %s", exc)

    def _rate_limit(self) -> None:
        global _last_request_time
        elapsed = time.time() - _last_request_time
        if elapsed < self.rate_delay:
            time.sleep(self.rate_delay - elapsed)
        _last_request_time = time.time()

    def _query(self, **params) -> List[CVEResult]:
        cached = self._load_cache(params)
        if cached is not None:
            log.debug("CVE cache hit for %s", params)
            return cached

        self._rate_limit()

        url = NVD_API_BASE + "?" + urllib.parse.urlencode(params)
        headers: dict = {"Accept": "application/json"}
        if self.api_key:
            headers["apiKey"] = self.api_key

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            log.warning("NVD API HTTP %s: %s", exc.code, exc.read()[:200])
            return []
        except Exception as exc:
            log.warning("NVD API error: %s", exc)
            return []

        results: List[CVEResult] = []
        for item in data.get("vulnerabilities", []):
            cve      = item.get("cve", {})
            cve_id   = cve.get("id", "")
            desc     = next(
                (d["value"] for d in cve.get("descriptions", []) if d.get("lang") == "en"),
                "",
            )
            refs      = [r["url"] for r in cve.get("references", [])[:3]]
            published = cve.get("published", "")[:10]

            # CVSS: prefer v3.1 > v3.0 > v2
            metrics  = cve.get("metrics", {})
            cvss     = 0.0
            severity = "UNKNOWN"
            for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
                bucket = metrics.get(key)
                if bucket:
                    m         = bucket[0]
                    cvss_data = m.get("cvssData", {})
                    cvss      = float(cvss_data.get("baseScore", 0.0))
                    severity  = cvss_data.get("baseSeverity", m.get("baseSeverity", "UNKNOWN"))
                    break

            results.append(CVEResult(
                id=cve_id,
                cvss=cvss,
                severity=severity,
                description=desc,
                published=published,
                references=refs,
            ))

        results.sort(key=lambda r: r.cvss, reverse=True)
        self._save_cache(params, results)
        log.info("NVD returned %d CVEs for %s", len(results), params)
        return results


# ── Module-level singleton ────────────────────────────────────────────────────

_default: Optional[CVEMatcher] = None


def get_matcher() -> CVEMatcher:
    """Return (or create) the module-level singleton CVEMatcher."""
    global _default
    if _default is None:
        _default = CVEMatcher()
    return _default


def search(product: str, version: str = "", max_results: int = 10) -> List[CVEResult]:
    """Module-level convenience wrapper."""
    return get_matcher().search(product, version, max_results=max_results)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    p = argparse.ArgumentParser(description="LazyOwn CVE Matcher")
    p.add_argument("--product",  required=True,          help="Product name (e.g. openssh)")
    p.add_argument("--version",  default="",             help="Version string (e.g. 8.4)")
    p.add_argument("--max",      type=int, default=10,   help="Max results (default 10)")
    p.add_argument("--json",     action="store_true",    help="Output raw JSON")
    args = p.parse_args()

    matcher = CVEMatcher()
    results = matcher.search(args.product, args.version, max_results=args.max)

    if not results:
        print("No CVEs found.")
        sys.exit(0)

    if args.json:
        print(json.dumps([vars(r) for r in results], indent=2))
    else:
        for r in results:
            bar = "#" * min(int(r.cvss), 10)
            print(f"[{r.severity:8s}] {r.id}  CVSS {r.cvss:.1f} {bar}  {r.published}")
            print(f"  {r.description[:120]}")
            for ref in r.references:
                print(f"  -> {ref}")
            print()
