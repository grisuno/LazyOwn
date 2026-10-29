"""Tests for modules.lazydorks — target-aware dork generator.

Covers:
    - Category inventory
    - Per-category rendering with domain scoping
    - GitHub org fallback to domain
    - Empty-input guards
    - Report export round-trip
"""

from __future__ import annotations

import pytest


@pytest.fixture
def dorks():
    from modules import lazydorks

    return lazydorks


class TestLazyDorks:
    def test_categories_populated(self, dorks):
        assert len(dorks.categories()) >= 8
        assert "backend_logins" in dorks.categories()
        assert "github_org" in dorks.categories()

    def test_queries_scoped_to_domain(self, dorks):
        rows = dorks.queries("sql_errors", "example.com")
        assert rows and all("example.com" in row for row in rows)

    def test_queries_cap(self, dorks):
        rows = dorks.queries("exposed_files", "example.com")
        assert 0 < len(rows) <= dorks.MAX_QUERIES_PER_CATEGORY

    def test_unknown_category_empty(self, dorks):
        assert dorks.queries("nope", "example.com") == ()

    def test_github_needs_org_or_domain(self, dorks):
        assert dorks.queries("github_org", "") == ()
        assert dorks.queries("github_org", "example.com")

    def test_github_org_fallback_to_domain(self, dorks):
        rows = dorks.queries("github_org", "example.com")
        assert all("org:example.com" in row for row in rows)

    def test_empty_domain_empty(self, dorks):
        assert dorks.queries("sql_errors", "") == ()
        assert dorks.all_queries("", "org") == {}

    def test_all_queries_only_populated(self, dorks):
        mapping = dorks.all_queries("example.com", "acme")
        assert mapping and all(mapping.values())

    def test_write_report(self, dorks, tmp_path):
        destination = tmp_path / "dorks.md"
        result = dorks.write_report(destination, "example.com", "acme")
        assert result["error"] == ""
        assert result["written"] > 0
        text = destination.read_text(encoding="utf-8")
        assert "Example.Com" not in text.splitlines()[0]
        assert "example.com" in text

    def test_write_report_invalid_target(self, dorks, tmp_path):
        destination = tmp_path / "dorks.md"
        result = dorks.write_report(destination, " ")
        assert result["error"] == "no dorks rendered"
        assert not destination.exists()
