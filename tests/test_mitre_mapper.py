"""MITRE mapper tests: tactic resolution, coverage, artefacts."""

from __future__ import annotations

import json

import pytest

from modules import mitre_mapper
from modules.mitre_mapper import (
    TACTIC_ORDER,
    coverage_report,
    render_html,
    render_markdown,
    tactic_for_technique,
    write_coverage,
)


@pytest.fixture(autouse=True)
def isolated_loops(tmp_path, monkeypatch):
    """Point the loop collectors at an empty directory."""
    from modules import report_engagement as re_engage

    lazy = tmp_path / "lazy"
    lazy.mkdir()
    (lazy / "tasks.json").write_text(json.dumps({"seq": 0, "tasks": {}}))
    monkeypatch.setattr(re_engage, "LAZY_DIR", lazy)
    monkeypatch.setattr(re_engage, "SESSIONS_DIR", tmp_path)
    return tmp_path


@pytest.fixture()
def fake_catalog(monkeypatch):
    entries = [
        type("E", (), {"command": "lazynmap", "phase": "recon", "mitre_tactic": "T1046"}),
        type("E", (), {"command": "batchnmap", "phase": "recon", "mitre_tactic": "T1046"}),
        type("E", (), {"command": "mimikatzpy", "phase": "cred", "mitre_tactic": "T1003"}),
        type("E", (), {"command": "weird", "phase": "x", "mitre_tactic": "not-a-tid"}),
        type("E", (), {"command": "empty", "phase": "x", "mitre_tactic": ""}),
    ]
    monkeypatch.setattr(mitre_mapper, "_catalog_entries", lambda: entries)
    return entries


class TestTacticResolution:
    def test_known_prefixes(self):
        assert tactic_for_technique("T1046") == "discovery"
        assert tactic_for_technique("T1003.001") == "credential-access"
        assert tactic_for_technique("T1595.002") == "reconnaissance"

    def test_unknown_technique(self):
        assert tactic_for_technique("T9999") == "unknown"
        assert tactic_for_technique("") == "unknown"

    def test_tactic_order_complete(self):
        assert "reconnaissance" in TACTIC_ORDER
        assert TACTIC_ORDER[-1] == "unknown"


class TestCoverage:
    def test_catalog_counts(self, fake_catalog):
        report = coverage_report(include_executed=False)
        assert report["totals"]["techniques"] == 2
        assert report["totals"]["commands"] == 3
        t1046 = next(row for row in report["techniques"] if row["technique_id"] == "T1046")
        assert t1046["commands"] == ["lazynmap", "batchnmap"]
        assert t1046["tactic"] == "discovery"

    def test_invalid_ids_skipped(self, fake_catalog):
        report = coverage_report(include_executed=False)
        ids = {row["technique_id"] for row in report["techniques"]}
        assert "not-a-tid" not in ids

    def test_executed_intersection(self, fake_catalog, isolated_loops, monkeypatch):
        from modules import report_engagement as re_engage

        (isolated_loops / "lazy" / "audit_t0001.jsonl").write_text(
            json.dumps({"ts": 1.0, "kind": "command", "command": "lazynmap -sV 10.0.0.5", "ok": True}) + "\n"
        )
        (isolated_loops / "tasks.json").write_text(json.dumps({"seq": 1, "tasks": {"t0001": {"task_id": "t0001"}}}))
        report = coverage_report()
        assert report["totals"]["executed_commands"] >= 1
        t1046 = next(row for row in report["techniques"] if row["technique_id"] == "T1046")
        assert "lazynmap" in t1046["executed"]

    def test_tactics_ordered(self, fake_catalog):
        report = coverage_report(include_executed=False)
        slugs = list(report["tactics"])
        order = [TACTIC_ORDER.index(slug) for slug in slugs]
        assert order == sorted(order)


class TestRender:
    def test_markdown_tables(self, fake_catalog):
        md = render_markdown(coverage_report(include_executed=False))
        assert "| Tactic |" in md
        assert "discovery" in md
        assert "## Techniques" in md

    def test_html_document(self, fake_catalog):
        html = render_html(coverage_report(include_executed=False))
        assert "<table>" in html
        assert "Adversary Coverage" in html

    def test_write_artefacts(self, fake_catalog, tmp_path):
        written = write_coverage(tmp_path)
        assert (tmp_path / "mitre_coverage.md").exists()
        assert (tmp_path / "mitre_coverage.html").exists()
        assert "markdown" in written
