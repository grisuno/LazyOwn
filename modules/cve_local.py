"""Local CVE snapshot — offline SQLite database of NVD + Exploit-DB.

Replaces real-time web scraping with a periodically synced local copy:
``cve_sync`` downloads the Exploit-DB CSV and pages through the NVD API
(incrementally via ``lastModStartDate``), storing everything in one
SQLite database. ``cve_search`` answers instantly from the snapshot,
including the service/product pairs captured by ``ss`` so a re-run
never re-correlates from scratch.

>>> from modules.cve_local import CveLocalDB
>>> db = CveLocalDB()
>>> db.status()["cves"] >= 0
True
"""

from __future__ import annotations

import csv
import io
import json
import re
import sqlite3
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = REPO_ROOT / "sessions" / "cve_local"
DB_PATH = DB_DIR / "snapshot.db"
CONTEXT_DB_PATH = DB_DIR / "service_context.db"

NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
EXPLOITDB_CSV_URL = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_exploits.csv"

NVD_PAGE_SIZE = 2000
NVD_MAX_RESULTS = 2000
DEFAULT_SYNC_TIMEOUT = 30
PAGE_DELAY_SEC = 6.0
DEFAULT_MAX_PAGES = 400
CPE_TOKEN_RE = re.compile(r"cpe:2\.3:[aho]:([^:]+):([^:]+):([^:]+):")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS cves (
    id TEXT PRIMARY KEY,
    cvss REAL NOT NULL DEFAULT 0.0,
    vector TEXT NOT NULL DEFAULT '',
    published TEXT NOT NULL DEFAULT '',
    modified TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    products TEXT NOT NULL DEFAULT '[]'
);
CREATE INDEX IF NOT EXISTS idx_cves_published ON cves(published DESC);
CREATE INDEX IF NOT EXISTS idx_cves_cvss ON cves(cvss DESC);
CREATE TABLE IF NOT EXISTS exploits (
    edb_id TEXT PRIMARY KEY,
    cves TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    type TEXT NOT NULL DEFAULT '',
    platform TEXT NOT NULL DEFAULT '',
    date TEXT NOT NULL DEFAULT '',
    url TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS service_context (
    host TEXT NOT NULL,
    service TEXT NOT NULL,
    product TEXT NOT NULL,
    version TEXT NOT NULL,
    cves TEXT NOT NULL DEFAULT '[]',
    ts REAL NOT NULL,
    PRIMARY KEY (host, service, product, version)
);
"""

SERVICE_CONTEXT_TTL_SEC = 7 * 24 * 3600


@dataclass
class LocalCVE:
    """One snapshot row rendered for consumers."""

    cve_id: str
    cvss: float
    description: str
    published: str
    products: list[str]
    exploitdb: list[str] | None = None

    def __post_init__(self) -> None:
        """Normalize the optional exploit list."""
        if self.exploitdb is None:
            self.exploitdb = []


def _db_connect(path: Path) -> sqlite3.Connection:
    """Open the snapshot database, creating the schema.

    Args:
        path: Database file path.

    Returns:
        Connected sqlite3 handle with the schema applied.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    return conn


class CveLocalDB:
    """Read/write access to the local CVE snapshot."""

    def __init__(self, path: Path | None = None) -> None:
        """Initialize the database handle.

        Args:
            path: Override for the snapshot database path (tests).
        """
        self._path = Path(path) if path else DB_PATH
        self._conn: sqlite3.Connection | None = None

    @property
    def path(self) -> Path:
        """Database file path."""
        return self._path

    def conn(self) -> sqlite3.Connection:
        """Return the open connection, creating the schema once.

        Returns:
            sqlite3 connection.
        """
        if self._conn is None:
            self._conn = _db_connect(self._path)
        return self._conn

    def close(self) -> None:
        """Close the underlying connection when open."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def status(self) -> dict[str, Any]:
        """Report snapshot freshness and row counts.

        Returns:
            Mapping with ``cves``, ``exploits``, ``contexts`` and the
            per-source last sync epoch seconds.
        """
        if not self._path.exists():
            return {"cves": 0, "exploits": 0, "contexts": 0, "last_nvd_sync": 0.0, "last_edb_sync": 0.0}
        conn = self.conn()
        cves = conn.execute("SELECT COUNT(*) FROM cves").fetchone()[0]
        exploits = conn.execute("SELECT COUNT(*) FROM exploits").fetchone()[0]
        contexts = conn.execute("SELECT COUNT(*) FROM service_context").fetchone()[0]
        meta = dict(conn.execute("SELECT key, value FROM meta").fetchall())
        return {
            "cves": cves,
            "exploits": exploits,
            "contexts": contexts,
            "last_nvd_sync": float(meta.get("last_nvd_sync", 0.0) or 0.0),
            "last_edb_sync": float(meta.get("last_edb_sync", 0.0) or 0.0),
        }

    def set_meta(self, key: str, value: str) -> None:
        """Persist one metadata row.

        Args:
            key: Metadata key.
            value: Metadata value.
        """
        self.conn().execute(
            "INSERT INTO meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        self.conn().commit()

    def upsert_cves(self, rows: list[dict[str, Any]]) -> int:
        """Insert or update CVE rows from an NVD page.

        Args:
            rows: Mappings with ``id``, ``cvss``, ``vector``,
                ``published``, ``modified``, ``description``,
                ``products`` (list of ``product`` strings).

        Returns:
            Number of rows written.
        """
        if not rows:
            return 0
        conn = self.conn()
        conn.executemany(
            "INSERT INTO cves (id, cvss, vector, published, modified, description, products) "
            "VALUES (:id, :cvss, :vector, :published, :modified, :description, :products) "
            "ON CONFLICT(id) DO UPDATE SET cvss = excluded.cvss, vector = excluded.vector, "
            "modified = excluded.modified, description = excluded.description, products = excluded.products",
            [
                {
                    "id": row["id"],
                    "cvss": float(row.get("cvss", 0.0) or 0.0),
                    "vector": str(row.get("vector", "") or ""),
                    "published": str(row.get("published", "") or ""),
                    "modified": str(row.get("modified", "") or ""),
                    "description": str(row.get("description", "") or "")[:2000],
                    "products": json.dumps(row.get("products") or []),
                }
                for row in rows
            ],
        )
        conn.commit()
        return len(rows)

    def upsert_exploits(self, rows: list[dict[str, Any]]) -> int:
        """Insert or update Exploit-DB rows.

        Args:
            rows: Mappings with ``edb_id``, ``cves``, ``description``,
                ``type``, ``platform``, ``date``, ``url``.

        Returns:
            Number of rows written.
        """
        if not rows:
            return 0
        conn = self.conn()
        conn.executemany(
            "INSERT INTO exploits (edb_id, cves, description, type, platform, date, url) "
            "VALUES (:edb_id, :cves, :description, :type, :platform, :date, :url) "
            "ON CONFLICT(edb_id) DO UPDATE SET cves = excluded.cves, description = excluded.description, "
            "type = excluded.type, platform = excluded.platform, date = excluded.date",
            [
                {
                    "edb_id": str(row.get("edb_id", "") or ""),
                    "cves": ",".join(row.get("cves") or []),
                    "description": str(row.get("description", "") or "")[:500],
                    "type": str(row.get("type", "") or ""),
                    "platform": str(row.get("platform", "") or ""),
                    "date": str(row.get("date", "") or ""),
                    "url": str(row.get("url", "") or ""),
                }
                for row in rows
            ],
        )
        conn.commit()
        return len(rows)

    def search(self, keyword: str, version: str = "", max_results: int = 20) -> list[dict[str, Any]]:
        """Search the snapshot for a product/CVE keyword.

        Args:
            keyword: Product name, CVE id or description fragment.
            version: Optional version filter matched against products.
            max_results: Row cap.

        Returns:
            CVE rows sorted by CVSS then publication date, each with
            matching Exploit-DB ids attached.
        """
        if not keyword.strip():
            return []
        conn = self.conn()
        token = keyword.strip().lower()
        like = f"%{token}%"
        rows = conn.execute(
            "SELECT id, cvss, published, modified, description, products FROM cves "
            "WHERE lower(id) = :exact OR lower(description) LIKE :like OR lower(products) LIKE :like "
            "ORDER BY cvss DESC, published DESC LIMIT :cap",
            {"exact": token, "like": like, "cap": max_results},
        ).fetchall()
        results: list[dict[str, Any]] = []
        for cve_id, cvss, published, modified, description, products_json in rows:
            products = []
            try:
                products = json.loads(products_json or "[]")
            except ValueError:
                products = []
            if version:
                version_token = token_matches_version(products, version, keyword)
                if not version_token:
                    continue
            edb_ids = self._exploit_ids_for(cve_id)
            results.append(
                {
                    "id": cve_id,
                    "cvss": cvss,
                    "published": published,
                    "modified": modified,
                    "description": description,
                    "products": products,
                    "exploitdb": edb_ids,
                }
            )
        return results

    def _exploit_ids_for(self, cve_id: str) -> list[str]:
        """Resolve Exploit-DB ids that reference a CVE.

        Args:
            cve_id: CVE identifier.

        Returns:
            List of Exploit-DB ids; empty when the exploits table is empty.
        """
        try:
            rows = (
                self.conn()
                .execute(
                    "SELECT edb_id FROM exploits WHERE ',' || cves || ',' LIKE :pattern LIMIT 10",
                    {"pattern": f"%,{cve_id},%"},
                )
                .fetchall()
            )
        except sqlite3.Error:
            return []
        return [str(row[0]) for row in rows]

    def store_context(self, host: str, services: list[dict[str, Any]]) -> int:
        """Persist service/product pairs captured by ``ss`` for a host.

        Args:
            host: Target host or IP.
            services: Rows with ``service``, ``product``, ``version``
                and optionally ``cves``.

        Returns:
            Number of stored rows.
        """
        if not host:
            return 0
        now = time.time()
        conn = self.conn()
        written = 0
        for service in services:
            product = str(service.get("product", "") or "")
            if not product:
                continue
            conn.execute(
                "INSERT INTO service_context (host, service, product, version, cves, ts) "
                "VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(host, service, product, version) DO UPDATE SET "
                "cves = excluded.cves, ts = excluded.ts",
                (
                    str(host),
                    str(service.get("service", "") or ""),
                    product,
                    str(service.get("version", "") or ""),
                    json.dumps(service.get("cves") or []),
                    now,
                ),
            )
            written += 1
        conn.commit()
        return written

    def context_for_host(self, host: str, max_age_sec: float = SERVICE_CONTEXT_TTL_SEC) -> list[dict[str, Any]]:
        """Return the services captured for a host (instant, no network).

        Args:
            host: Target host or IP.
            max_age_sec: Rows older than this are dropped.

        Returns:
            Service rows with products/versions and known CVE ids.
        """
        if not host:
            return []
        cutoff = time.time() - max_age_sec
        rows = (
            self.conn()
            .execute(
                "SELECT service, product, version, cves, ts FROM service_context "
                "WHERE host = ? AND ts >= ? ORDER BY service",
                (str(host), cutoff),
            )
            .fetchall()
        )
        out: list[dict[str, Any]] = []
        for service, product, version, cves_json, ts in rows:
            try:
                cves = json.loads(cves_json or "[]")
            except ValueError:
                cves = []
            out.append({"service": service, "product": product, "version": version, "cves": cves, "ts": ts})
        return out

    def sync_nvd(
        self,
        api_key: str = "",
        max_pages: int = DEFAULT_MAX_PAGES,
        fetcher: Callable[[str, dict[str, str]], bytes] | None = None,
        delay_sec: float = PAGE_DELAY_SEC,
    ) -> dict[str, Any]:
        """Page the NVD API into the snapshot, incrementally.

        Args:
            api_key: Optional NVD API key (raises the rate limit).
            max_pages: Safety cap on pages per run.
            fetcher: Injected fetcher ``(url, headers) -> bytes`` (tests).
            delay_sec: Delay between pages to respect the rate limit.

        Returns:
            Mapping with ``pages``, ``cves`` and ``done`` flags.
        """
        fetch = fetcher or _fetch_url
        headers = {"apiKey": api_key} if api_key else {}
        start_index = 0
        pages = 0
        total = 0
        last_modified = self._meta_value("last_nvd_modified")
        while pages < max_pages:
            params = f"?resultsPerPage={NVD_PAGE_SIZE}&startIndex={start_index}"
            if last_modified:
                params += f"&lastModStartDate={last_modified}"
            url = NVD_API_BASE + params
            try:
                body = fetch(url, headers)
                payload = json.loads(body.decode("utf-8", errors="replace"))
            except Exception:
                break
            items = payload.get("vulnerabilities") or []
            if not items:
                break
            rows = [_nvd_row(item) for item in items]
            self.upsert_cves(rows)
            total += len(rows)
            pages += 1
            start_index += len(items)
            if start_index >= int(payload.get("totalResults", 0) or 0) or len(items) < NVD_PAGE_SIZE:
                break
            if delay_sec > 0:
                time.sleep(delay_sec)
        now = time.time()
        self.set_meta("last_nvd_sync", str(now))
        if pages and not last_modified:
            self.set_meta("last_nvd_modified", _now_iso(-86400))
        return {"pages": pages, "cves": total}

    def sync_exploitdb(
        self,
        fetcher: Callable[[str, dict[str, str]], bytes] | None = None,
    ) -> dict[str, Any]:
        """Refresh the Exploit-DB index from its public CSV.

        Args:
            fetcher: Injected fetcher override (tests).

        Returns:
            Mapping with ``exploits`` row count; ``0`` when offline.
        """
        fetch = fetcher or _fetch_url
        try:
            body = fetch(EXPLOITDB_CSV_URL, {})
        except Exception:
            self.set_meta("last_edb_sync", str(time.time()))
            return {"exploits": 0}
        text = body.decode("utf-8", errors="replace")
        rows = _exploitdb_rows(text)
        self.upsert_exploits(rows)
        self.set_meta("last_edb_sync", str(time.time()))
        return {"exploits": len(rows)}

    def _meta_value(self, key: str) -> str:
        """Read one metadata value.

        Args:
            key: Metadata key.

        Returns:
            Stored value or empty string.
        """
        row = self.conn().execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return str(row[0]) if row else ""


def token_matches_version(products: list[str], version: str, keyword: str) -> bool:
    """Check whether any product token contains both keyword and version.

    Args:
        products: Product strings from the snapshot.
        version: Version string to match.
        keyword: Product keyword.

    Returns:
        True when at least one token mentions both.
    """
    keyword_low = keyword.lower()
    version_low = version.lower()
    return any(keyword_low in str(product).lower() and version_low in str(product).lower() for product in products)


def _now_iso(offset_sec: int = 0) -> str:
    """Format a UTC timestamp offset by ``offset_sec`` as NVD ISO.

    Args:
        offset_sec: Seconds added to now (negative for the past).

    Returns:
        ISO 8601 UTC string with milliseconds.
    """
    from datetime import UTC, datetime, timedelta

    moment = datetime.now(UTC) + timedelta(seconds=offset_sec)
    return moment.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "000"


def _fetch_url(url: str, headers: dict[str, str]) -> bytes:
    """Perform the default HTTP GET.

    Args:
        url: Fully qualified endpoint.
        headers: Request headers (e.g. NVD API key).

    Returns:
        Response body bytes; raises on transport failure.

    Raises:
        OSError: When the request fails or the payload is oversized.
    """
    import urllib.request

    request = urllib.request.Request(url, headers={"User-Agent": "LazyOwn cve_local sync", **headers})
    with urllib.request.urlopen(request, timeout=DEFAULT_SYNC_TIMEOUT) as response:
        return response.read(MAX_DOWNLOAD_BYTES)


MAX_DOWNLOAD_BYTES = 64 * 1024 * 1024


def _nvd_row(item: dict[str, Any]) -> dict[str, Any]:
    """Flatten one NVD ``vulnerabilities`` entry into a row.

    Args:
        item: NVD entry (``cve`` block per API 2.0).

    Returns:
        Row for :meth:`CveLocalDB.upsert_cves`.
    """
    cve = item.get("cve") or {}
    cve_id = str(cve.get("id", "") or "")
    descriptions = cve.get("descriptions") or []
    description = ""
    for desc in descriptions:
        if desc.get("lang") == "en":
            description = str(desc.get("value", "") or "")
            break
    cvss = 0.0
    vector = ""
    metrics = cve.get("metrics") or {}
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        entries = metrics.get(key) or []
        if entries:
            data = entries[0].get("cvssData") or {}
            try:
                cvss = float(data.get("baseScore", 0.0) or 0.0)
            except (TypeError, ValueError):
                cvss = 0.0
            vector = str(data.get("vectorString", "") or "")
            if key != "cvssMetricV2":
                break
    products: list[str] = []
    for config in cve.get("configurations") or []:
        for node in config.get("nodes") or []:
            for match in node.get("cpeMatch") or []:
                criteria = str(match.get("criteria", "") or "")
                for match_obj in CPE_TOKEN_RE.finditer(criteria):
                    products.append(f"{match_obj.group(1)}:{match_obj.group(2)}:{match_obj.group(3)}")
    return {
        "id": cve_id,
        "cvss": cvss,
        "vector": vector,
        "published": str(cve.get("published", "") or ""),
        "modified": str(cve.get("lastModified", "") or ""),
        "description": description,
        "products": products,
    }


def _exploitdb_rows(text: str) -> list[dict[str, Any]]:
    """Parse the Exploit-DB CSV into rows.

    Args:
        text: Raw CSV content.

    Returns:
        Rows for :meth:`CveLocalDB.upsert_exploits`.
    """
    reader = csv.DictReader(io.StringIO(text))
    rows: list[dict[str, Any]] = []
    cve_re = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
    for raw in reader:
        codes = raw.get("codes", "") or ""
        cves = sorted(set(cve_re.findall(codes)))
        edb_id = raw.get("id", "") or ""
        if not edb_id:
            continue
        rows.append(
            {
                "edb_id": edb_id,
                "cves": cves,
                "description": raw.get("description", "") or "",
                "type": raw.get("type", "") or "",
                "platform": raw.get("platform", "") or "",
                "date": raw.get("date_published", "") or raw.get("date_added", "") or "",
                "url": f"https://www.exploit-db.com/exploits/{edb_id}",
            }
        )
    return rows


_DB: CveLocalDB | None = None


def get_db() -> CveLocalDB:
    """Return the shared snapshot handle.

    Returns:
        Process-wide :class:`CveLocalDB`.
    """
    global _DB
    if _DB is None:
        _DB = CveLocalDB()
    return _DB


def reset_db() -> None:
    """Drop the shared handle (tests)."""
    global _DB
    _DB = None


def sync(api_key: str = "", max_pages: int = DEFAULT_MAX_PAGES, delay_sec: float = PAGE_DELAY_SEC) -> dict[str, Any]:
    """Sync both sources through the shared handle.

    Args:
        api_key: Optional NVD API key.
        max_pages: NVD page cap per run.
        delay_sec: NVD page delay.

    Returns:
        Combined sync report.
    """
    db = get_db()
    report = db.sync_exploitdb()
    report.update(db.sync_nvd(api_key=api_key, max_pages=max_pages, delay_sec=delay_sec))
    return report


def search(keyword: str, version: str = "", max_results: int = 20) -> list[dict[str, Any]]:
    """Search the shared snapshot.

    Args:
        keyword: Product or CVE id.
        version: Optional version filter.
        max_results: Row cap.

    Returns:
        Matching CVE rows.
    """
    return get_db().search(keyword, version=version, max_results=max_results)


def store_context(host: str, services: list[dict[str, Any]]) -> int:
    """Persist ``ss`` service context through the shared handle.

    Args:
        host: Target host.
        services: Service rows.

    Returns:
        Stored row count.
    """
    return get_db().store_context(host, services)


def context_for_host(host: str) -> list[dict[str, Any]]:
    """Read stored context through the shared handle.

    Args:
        host: Target host.

    Returns:
        Service rows.
    """
    return get_db().context_for_host(host)


def status() -> dict[str, Any]:
    """Report shared snapshot status.

    Returns:
        Status mapping.
    """
    return get_db().status()
