#!/usr/bin/env python3
"""
modules/integrations/searchsploit.py
======================================
Bridges searchsploit CLI and ExploitDB with LazyOwn CVE/finding data.

Design (SOLID)
--------------
- Single Responsibility : each class owns one source or one operation
- Open/Closed           : new exploit sources via ExploitSource subclass
- Liskov                : SearchsploitCLI and ExploitDBAPI honour the same contract
- Interface Segregation : consumers import ExploitSource, not concrete types
- Dependency Inversion  : SearchsploitClient depends on ExploitSource abstraction

Usage
-----
    from modules.integrations.searchsploit import get_client, search_cve

    entries = search_cve("CVE-2021-41773")
    for e in entries:
        print(e.id, e.title)

    # CLI:
    python3 modules/integrations/searchsploit.py --cve CVE-2021-41773
    python3 modules/integrations/searchsploit.py --service apache --version 2.4.49
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import subprocess
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional

log = logging.getLogger("searchsploit")

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

_EXPLOITDB_SEARCH_URL = (
    "https://www.exploit-db.com/search"
    "?cve={cve_id}&type=&platform=&format=json"
)
_RATE_LIMIT_SECONDS = 2.0
_last_api_call: float = 0.0


# ---------------------------------------------------------------------------
# Value object
# ---------------------------------------------------------------------------

@dataclass
class ExploitEntry:
    """Represents a single exploit found in ExploitDB or searchsploit."""
    id: str
    title: str
    path: str
    type: str = ""
    platform: str = ""
    cve: str = ""


# ---------------------------------------------------------------------------
# Abstract source
# ---------------------------------------------------------------------------

class ExploitSource(ABC):
    """Interface for any exploit lookup back-end."""

    @abstractmethod
    def search_cve(self, cve_id: str) -> List[ExploitEntry]:
        """Return exploits matching *cve_id* (e.g. 'CVE-2021-41773')."""

    @abstractmethod
    def search_service(self, name: str, version: str = "") -> List[ExploitEntry]:
        """Return exploits matching the service *name* and optional *version*."""


# ---------------------------------------------------------------------------
# searchsploit CLI back-end
# ---------------------------------------------------------------------------

class SearchsploitCLI(ExploitSource):
    """
    Runs ``searchsploit --json <query>`` and parses the result.

    Falls back gracefully to an empty list if searchsploit is not installed.
    Handles both the legacy (RESULTS_EXPLOIT / RESULTS_SHELLCODE) and
    new (data) top-level key formats.
    """

    def __init__(self) -> None:
        self._binary: Optional[str] = shutil.which("searchsploit")
        if not self._binary:
            log.warning(
                "searchsploit not found in PATH; SearchsploitCLI will return empty lists"
            )

    # -- ExploitSource ---------------------------------------------------------

    def search_cve(self, cve_id: str) -> List[ExploitEntry]:
        return self._run(cve_id)

    def search_service(self, name: str, version: str = "") -> List[ExploitEntry]:
        query = f"{name} {version}".strip()
        return self._run(query)

    # -- Internal --------------------------------------------------------------

    def _run(self, query: str) -> List[ExploitEntry]:
        if not self._binary:
            return []
        try:
            result = subprocess.run(
                [self._binary, "--json", query],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return self._parse(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
            log.warning("searchsploit execution failed: %s", exc)
            return []

    def _parse(self, raw: str) -> List[ExploitEntry]:
        if not raw.strip():
            return []
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            log.warning("Failed to parse searchsploit JSON: %s", exc)
            return []

        # Support multiple output formats
        rows: List[dict] = []
        if "RESULTS_EXPLOIT" in data:
            rows = data.get("RESULTS_EXPLOIT", []) + data.get("RESULTS_SHELLCODE", [])
        elif "data" in data:
            rows = data["data"]
        else:
            # Try to iterate whatever top-level list-like value is present
            for val in data.values():
                if isinstance(val, list):
                    rows = val
                    break

        entries: List[ExploitEntry] = []
        for row in rows:
            entry = self._row_to_entry(row)
            if entry:
                entries.append(entry)
        return entries

    def _row_to_entry(self, row: dict) -> Optional[ExploitEntry]:
        # Normalise field names between old and new formats
        eid = str(row.get("EDB-ID") or row.get("id") or row.get("edb_id") or "")
        title = str(row.get("Title") or row.get("title") or row.get("description") or "")
        path = str(row.get("Path") or row.get("file") or row.get("path") or "")
        exploit_type = str(row.get("Type") or row.get("type") or "")
        platform = str(row.get("Platform") or row.get("platform") or "")
        cve = self._extract_cve(title + " " + path)

        if not eid and not title:
            return None
        return ExploitEntry(
            id=eid,
            title=title,
            path=path,
            type=exploit_type,
            platform=platform,
            cve=cve,
        )

    @staticmethod
    def _extract_cve(text: str) -> str:
        match = re.search(r"CVE-\d{4}-\d+", text, re.IGNORECASE)
        return match.group(0).upper() if match else ""


# ---------------------------------------------------------------------------
# ExploitDB HTTP API back-end  (fallback)
# ---------------------------------------------------------------------------

class ExploitDBAPI(ExploitSource):
    """
    Queries the ExploitDB search endpoint directly.

    Disabled gracefully when *requests* is not available.
    Enforces a 2-second rate limit between calls.
    """

    def __init__(self) -> None:
        if not _REQUESTS_AVAILABLE:
            log.warning(
                "requests library not available; ExploitDBAPI will return empty lists"
            )

    # -- ExploitSource ---------------------------------------------------------

    def search_cve(self, cve_id: str) -> List[ExploitEntry]:
        return self._query(cve_id=cve_id)

    def search_service(self, name: str, version: str = "") -> List[ExploitEntry]:
        # ExploitDB search endpoint does not have a direct service parameter;
        # use the CVE field empty and rely on the title search (best-effort).
        query = f"{name} {version}".strip()
        return self._query(cve_id=query)

    # -- Internal --------------------------------------------------------------

    def _query(self, cve_id: str) -> List[ExploitEntry]:
        if not _REQUESTS_AVAILABLE:
            return []
        self._rate_limit()
        url = _EXPLOITDB_SEARCH_URL.format(cve_id=cve_id)
        try:
            resp = _requests.get(url, timeout=10, headers={"Accept": "application/json"})
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            log.warning("ExploitDBAPI request failed: %s", exc)
            return []

        rows = data if isinstance(data, list) else data.get("data", [])
        entries: List[ExploitEntry] = []
        for row in rows:
            eid = str(row.get("id") or "")
            title = str(row.get("description") or row.get("title") or "")
            path = str(row.get("download") or row.get("path") or "")
            exploit_type = str(row.get("type", {}).get("label", "") if isinstance(row.get("type"), dict) else row.get("type", ""))
            platform = str(row.get("platform", {}).get("label", "") if isinstance(row.get("platform"), dict) else row.get("platform", ""))
            entries.append(ExploitEntry(
                id=eid,
                title=title,
                path=path,
                type=exploit_type,
                platform=platform,
                cve=cve_id if re.match(r"CVE-\d{4}-\d+", cve_id, re.I) else "",
            ))
        return entries

    @staticmethod
    def _rate_limit() -> None:
        global _last_api_call
        elapsed = time.time() - _last_api_call
        if elapsed < _RATE_LIMIT_SECONDS:
            time.sleep(_RATE_LIMIT_SECONDS - elapsed)
        _last_api_call = time.time()


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------

class SearchsploitClient:
    """
    Facade that tries SearchsploitCLI first, falls back to ExploitDBAPI.

    Provides high-level helpers consumed by the rest of LazyOwn.
    """

    def __init__(
        self,
        primary: Optional[ExploitSource] = None,
        fallback: Optional[ExploitSource] = None,
    ) -> None:
        self._primary: ExploitSource = primary or SearchsploitCLI()
        self._fallback: ExploitSource = fallback or ExploitDBAPI()

    def search_cve(self, cve_id: str) -> List[ExploitEntry]:
        """Return exploits for *cve_id*, trying CLI then API."""
        results = self._primary.search_cve(cve_id)
        if not results:
            results = self._fallback.search_cve(cve_id)
        return results

    def search_service(self, name: str, version: str = "") -> List[ExploitEntry]:
        """Return exploits for *name*/*version*, trying CLI then API."""
        results = self._primary.search_service(name, version)
        if not results:
            results = self._fallback.search_service(name, version)
        return results

    def enrich_findings(self, findings: list) -> Dict[str, List[ExploitEntry]]:
        """
        Takes an ObsParser Finding list, extracts CVEs and service_versions,
        returns ``{cve_or_service: [ExploitEntry, ...]}``.
        """
        result: Dict[str, List[ExploitEntry]] = {}
        for finding in findings:
            ftype = str(getattr(finding, "type", "")).lower()
            value = str(getattr(finding, "value", ""))

            if "cve" in ftype:
                entries = self.search_cve(value)
                if entries:
                    result[value] = entries

            elif "service_version" in ftype or "service" in ftype:
                parts = value.split(" ", 1)
                name = parts[0]
                version = parts[1] if len(parts) > 1 else ""
                entries = self.search_service(name, version)
                if entries:
                    result[value] = entries

        return result


# ---------------------------------------------------------------------------
# Module-level singleton and convenience functions
# ---------------------------------------------------------------------------

_client: Optional[SearchsploitClient] = None


def get_client() -> SearchsploitClient:
    """Return the module-level SearchsploitClient singleton."""
    global _client
    if _client is None:
        _client = SearchsploitClient()
    return _client


def search_cve(cve_id: str) -> List[ExploitEntry]:
    """Module-level convenience: search by CVE id."""
    return get_client().search_cve(cve_id)


def search_service(name: str, version: str = "") -> List[ExploitEntry]:
    """Module-level convenience: search by service name and version."""
    return get_client().search_service(name, version)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(
        description="Search ExploitDB via searchsploit or the web API"
    )
    parser.add_argument("--cve", metavar="CVE_ID", help="Search by CVE id")
    parser.add_argument("--service", metavar="NAME", help="Service name")
    parser.add_argument("--version", metavar="VER", default="", help="Service version")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    client = get_client()
    entries: List[ExploitEntry] = []

    if args.cve:
        entries = client.search_cve(args.cve)
    elif args.service:
        entries = client.search_service(args.service, args.version)
    else:
        parser.print_help()
        return

    if args.as_json:
        import dataclasses
        print(json.dumps([dataclasses.asdict(e) for e in entries], indent=2))
    else:
        if not entries:
            print("No exploits found.")
            return
        for e in entries:
            print(f"[{e.id}] {e.title}")
            if e.path:
                print(f"    Path    : {e.path}")
            if e.cve:
                print(f"    CVE     : {e.cve}")
            if e.platform:
                print(f"    Platform: {e.platform}")
            print()


if __name__ == "__main__":
    _main()
