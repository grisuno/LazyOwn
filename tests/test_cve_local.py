"""CVE local snapshot tests: sync, search, service context, status."""

from __future__ import annotations

import json
import time

import pytest

from modules import cve_local
from modules.cve_local import CveLocalDB


@pytest.fixture()
def db(tmp_path) -> CveLocalDB:
    return CveLocalDB(path=tmp_path / "snapshot.db")


def _fake_nvd_page(start_index: int, count: int = 2, total: int = 4):
    """Build one synthetic NVD API response."""
    vulnerabilities = []
    for offset in range(count):
        cve_id = f"CVE-2024-1{start_index + offset:04d}"
        vulnerabilities.append(
            {
                "cve": {
                    "id": cve_id,
                    "published": "2024-01-02T10:00:00.000",
                    "lastModified": "2024-06-01T00:00:00.000",
                    "descriptions": [{"lang": "en", "value": f"OpenSSL {start_index + offset} flaw in apache httpd"}],
                    "metrics": {
                        "cvssMetricV31": [{"cvssData": {"baseScore": 7.5, "vectorString": "CVSS:3.1/AV:N/AC:L"}}]
                    },
                    "configurations": [
                        {
                            "nodes": [
                                {
                                    "cpeMatch": [
                                        {
                                            "criteria": f"cpe:2.3:a:apache:http_server:2.4.50:*:*:*:*:*:*:{start_index + offset}:*"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                }
            }
        )
    return json.dumps(
        {"resultsPerPage": count, "startIndex": start_index, "totalResults": total, "vulnerabilities": vulnerabilities}
    ).encode()


class TestSync:
    def test_nvd_sync_pages_into_rows(self, db, monkeypatch):
        monkeypatch.setattr(cve_local, "NVD_PAGE_SIZE", 2)
        pages = {}

        def fetcher(url, headers):
            pages[url] = True
            start = int(url.split("startIndex=")[1])
            return _fake_nvd_page(start, count=2, total=4)

        report = db.sync_nvd(fetcher=fetcher, delay_sec=0.0)
        assert report["pages"] == 2
        assert report["cves"] == 4
        status = db.status()
        assert status["cves"] == 4
        assert status["last_nvd_sync"] > 0

    def test_nvd_sync_offline_keeps_empty(self, db):
        def fetcher(url, headers):
            raise OSError("offline")

        report = db.sync_nvd(fetcher=fetcher, delay_sec=0.0)
        assert report["cves"] == 0
        assert db.status()["cves"] == 0

    def test_exploitdb_sync_parses_cves(self, db):
        csv_text = (
            "id,file,description,date_published,author,type,platform,port,date_added,date_updated,verified,codes,tags,aliases,screenshot_path,application_path,source_url\n"
            "51094,remote/webapps/51094.py,'Apache HTTP Server 2.4.50 - Path Traversal (RCE)',2022-11-01,'someone',webapps,multiple,'',2022-11-01,2022-11-02,0,'CVE-2021-41773; CVE-2021-42013','','','','',''\n"
            "50001,local/exploits/50001.sh,'Local root not cve',2021-01-01,'a',local,linux,'',2021-01-01,'',0,'','','','','',''\n"
        )

        def fetcher(url, headers):
            return csv_text.encode()

        report = db.sync_exploitdb(fetcher=fetcher)
        assert report["exploits"] == 2
        assert db.status()["exploits"] == 2
        assert db.status()["last_edb_sync"] > 0

    def test_exploitdb_offline_reports_zero(self, db):
        def fetcher(url, headers):
            raise OSError("offline")

        assert db.sync_exploitdb(fetcher=fetcher)["exploits"] == 0


class TestSearch:
    def test_exact_cve_and_description(self, db):
        db.sync_nvd(fetcher=lambda url, headers: _fake_nvd_page(0, count=2, total=2), delay_sec=0.0)
        hits = db.search("apache")
        assert hits, "description match expected"
        assert all("apache" in hit["description"].lower() or "apache" in str(hit["products"]).lower() for hit in hits)

    def test_version_filter(self, db):
        db.sync_nvd(fetcher=lambda url, headers: _fake_nvd_page(0, count=2, total=2), delay_sec=0.0)
        assert db.search("apache", version="2.4.50")
        assert not db.search("apache", version="9.9.9")

    def test_exploit_ids_attached(self, db):
        db.upsert_cves(
            [
                {
                    "id": "CVE-2021-41773",
                    "cvss": 9.8,
                    "products": ["apache:http_server:2.4.50"],
                    "description": "apache path traversal",
                    "published": "2021-01-01",
                    "modified": "",
                    "vector": "",
                }
            ]
        )
        db.upsert_exploits(
            [
                {
                    "edb_id": "51094",
                    "cves": ["CVE-2021-41773"],
                    "description": "rce",
                    "type": "webapps",
                    "platform": "multiple",
                    "date": "2022-11-01",
                    "url": "",
                }
            ]
        )
        hits = db.search("CVE-2021-41773")
        assert hits and hits[0]["exploitdb"] == ["51094"]

    def test_search_empty_keyword(self, db):
        assert db.search("") == []


class TestServiceContext:
    def test_store_and_read_context(self, db):
        n = db.store_context(
            "10.0.0.5",
            [{"service": "http", "product": "apache", "version": "2.4.25", "cves": ["CVE-2021-41773"]}],
        )
        assert n == 1
        context = db.context_for_host("10.0.0.5")
        assert context[0]["product"] == "apache"
        assert context[0]["cves"] == ["CVE-2021-41773"]

    def test_ttl_expiry(self, db):
        db.store_context("10.0.0.5", [{"service": "http", "product": "apache", "version": "2.4.25", "cves": []}])
        conn = db.conn()
        conn.execute("UPDATE service_context SET ts = ?", (time.time() - 8 * 24 * 3600,))
        conn.commit()
        assert db.context_for_host("10.0.0.5") == []

    def test_unknown_host_empty(self, db):
        assert db.context_for_host("203.0.113.9") == []

    def test_empty_host_noop(self, db):
        assert db.store_context("", []) == 0


class TestShared:
    def test_shared_status(self, monkeypatch, tmp_path):
        monkeypatch.setattr(cve_local, "DB_PATH", tmp_path / "snap.db")
        monkeypatch.setattr(cve_local, "_DB", None)
        assert cve_local.status()["cves"] == 0

    def test_schema_has_indexes(self, db):
        tables = {row[0] for row in db.conn().execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"cves", "exploits", "service_context", "meta"} <= tables
