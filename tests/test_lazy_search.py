"""BDD tests for the lazy saved-search grammar over the engagement DB."""

from __future__ import annotations

from modules import lazy_search
from modules.db import LazyOwnDB


def _seed(path):
    """Create a small workspace database with hosts, services, vulns, creds."""
    db = LazyOwnDB(str(path))
    db.default_workspace("default")
    host_id = db.host_add(1, "10.66.44.7", hostname="vpn.lazyown.local", os="linux")
    db.host_add(1, "10.66.44.9", hostname="git.lazyown.local", os="linux")
    db.service_add(host_id, 3389, name="ms-wbt-server", product="Remote Desktop")
    db.service_add(host_id, 8080, name="http", product="Apache Tomcat", version="9.0.45")
    db.vuln_add(1, name="CVE-2024-21762", severity="critical", description="FortiOS edge", refs="https://nvd LoL")
    db.cred_add(1, username="svc_sql", password="CorruptPassw0rd", cred_type="password", origin="captured")
    return db


def _svc_rows(result):
    return [(row.get("host"), row.get("port")) for row in result.get("services", [])]


class TestParse:
    def test_spot_keys_and_exclusions(self):
        story = "aliases and exclusions parse into terms"
        parsed = lazy_search.parse('port:3389 -host:vpn tech:"apache tomcat"')
        terms = [(term.key, term.value, term.negate) for term in parsed.terms]
        assert ("port", "3389", False) in terms, story
        assert ("host", "vpn", True) in terms, story
        assert ("product", "apache tomcat", False) in terms, story
        assert parsed.errors == [], story

    def test_unknown_key_errors(self):
        story = "a typo never silently changes the answer"
        parsed = lazy_search.parse("banana:yes")
        assert parsed.terms == [] and parsed.errors, story

    def test_severity_alias(self):
        story = "sev maps onto the severity vocabulary"
        parsed = lazy_search.parse("sev:crit")
        assert parsed.terms[0].value == "critical", story

    def test_free_words(self):
        story = "bare words stay free text"
        parsed = lazy_search.parse("tomcat lazy")
        assert parsed.free == ["tomcat", "lazy"], story


class TestExecute:
    def test_port_clamp(self, tmp_path):
        story = "port:3389 matches only that service"
        db = _seed(tmp_path / "lazyown.db")
        result = lazy_search.execute(db, "port:3389")
        assert _svc_rows(result) == [(None, 3389)] or [row[1] for row in _svc_rows(result)] == [3389], story

    def test_service_with_host_join(self, tmp_path):
        story = "services carry their host address in the results"
        db = _seed(tmp_path / "lazyown.db")
        result = lazy_search.execute(db, "port:8080")
        rows = result["services"]
        assert rows and rows[0].get("host") == "10.66.44.7", story

    def test_negation_by_host(self, tmp_path):
        story = "-host:vpn excludes every service on the vpn host"
        db = _seed(tmp_path / "lazyown.db")
        result = lazy_search.execute(db, "-host:vpn")
        herlaats = [row for row in result["services"] if row.get("host") == "10.66.44.7"]
        assert herlaats == [], story

    def test_free_word_reach(self, tmp_path):
        story = "bare words reach vuln names and hostnames"
        db = _seed(tmp_path / "lazyown.db")
        result = lazy_search.execute(db, "CVE-2024-21762")
        assert any("CVE-2024-21762" in str(row.get("name")) for row in result["vulns"]), story

    def test_user_clamp(self, tmp_path):
        story = "user: matches the credential table"
        db = _seed(tmp_path / "lazyown.db")
        result = lazy_search.execute(db, "user:svc_sql")
        assert any(row.get("username") == "svc_sql" for row in result["creds"]), story

    def test_multi_term_conjunction(self, tmp_path):
        story = "spot keys AND-combine"
        db = _seed(tmp_path / "lazyown.db")
        result = lazy_search.execute(db, "port:8080 product:tomcat")
        assert [row[1] for row in _svc_rows(result)] == [8080], story

    def test_empty_db_no_error(self, tmp_path):
        story = "an empty workspace returns zero matches, never raises"
        db = LazyOwnDB(str(tmp_path / "empty.db"))
        result = lazy_search.execute(db, "port:3389")
        assert result == {"hosts": [], "services": [], "vulns": [], "creds": [], "errors": []}, story
