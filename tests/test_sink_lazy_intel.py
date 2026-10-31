"""BDD tests for the dedicated lazy_intel sink."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules.db import LazyOwnDB
from modules.outcome_bus import OutcomeEvent
from modules.sinks import lazy_intel as sink
from modules.world_model import WorldModel, read_state_dict


def _event(host: str = "10.66.44.7", cve: str = "CVE-2025-24813") -> OutcomeEvent:
    """Build one lazy_intel event with a single bounded match."""
    return OutcomeEvent(
        kind="lazy_intel",
        target=host,
        title="lazy_intel fire exposure score 42",
        severity="critical",
        success=True,
        source="lazy_intel",
        command="lazyintel",
        metadata={
            "score": 42,
            "temperature": "hot",
            "feed": "rows=3 file=exploit_feed.json sha16=x",
            "cve_ids": [cve],
            "matches": [
                {
                    "cve_id": cve,
                    "host": host,
                    "port": 8080,
                    "product": "apache tomcat",
                    "version": "9.0.45",
                    "tier": "hot",
                    "evidence": "in_range",
                    "references": ["https://example/advisory"],
                }
            ],
        },
    )


@pytest.fixture()
def rigged(monkeypatch, tmp_path: Path):
    """Isolate both stores: temp world model + temp workspace database."""
    world = WorldModel(path=tmp_path / "world_model.json")
    monkeypatch.setattr(sink, "get_world_model", lambda: world)
    db_holder = {}
    db_holder["path"] = tmp_path / "lazyown.db"

    def fake_get_db(_path=None):
        return LazyOwnDB(str(db_holder["path"]))

    monkeypatch.setattr("modules.db.get_db", fake_get_db)
    return {"world": world, "db_path": db_holder["path"], "world_path": tmp_path / "world_model.json"}


class TestSinkRouting:
    def test_other_kinds_ignored(self, rigged):
        story = "the sink self-filters by lazy_intel kind"
        assert sink.apply(OutcomeEvent(kind="finding", target="t")) is False, story

    def test_missing_host_ignored(self, rigged):
        story = "an event without a host is not writable"
        event = _event()
        object.__setattr__(event, "target", "")
        assert sink.apply(event) is False, story


class TestWorldMirror:
    def test_fire_match_becomes_vulnerability(self, rigged):
        story = "the bounded match lands as a cve-tagged vulnerability on the host"
        event = _event()
        assert sink.apply(event) is True, story
        state = read_state_dict(rigged["world_path"])
        vulns = state.get("vulnerabilities") or []
        assert any("CVE-2025-24813" in str(v.get("cve")) for v in vulns), story
        hosts = state.get("hosts") or {}
        assert any("10.66.44.7" in str(ip) for ip in hosts), story

    def test_dedupe_second_event(self, rigged):
        story = "the same cve on the same host is not duplicated"
        event = _event()
        assert sink.apply(event) is True, story
        assert sink.apply(event) is False, story
        state = read_state_dict(rigged["world_path"])
        vulns = [v for v in state.get("vulnerabilities") or [] if "CVE-2025-24813" in str(v.get("cve"))]
        assert len(vulns) == 1, story


class TestDbMirror:
    def test_vuln_row_inserted_with_refs(self, rigged):
        story = "the sqlite workspace gets one vuln row with severity and references"
        assert rigged is not None
        sink.apply(_event())
        db = LazyOwnDB(str(rigged["db_path"]))
        rows = db.vuln_list(db.default_workspace())
        assert any(row.get("name") == "CVE-2025-24813" for row in rows), story
        row = next(r for r in rows if r.get("name") == "CVE-2025-24813")
        assert str(row.get("severity") or "").lower() in ("critical", "medium"), story
        assert "example" in str(row.get("refs") or ""), story

    def test_db_dedupe(self, rigged):
        story = "reapplying the event does not duplicate the sqlite row"
        sink.apply(_event())
        sink.apply(_event())
        db = LazyOwnDB(str(rigged["db_path"]))
        rows = [r for r in db.vuln_list(db.default_workspace()) if r.get("name") == "CVE-2025-24813"]
        assert len(rows) == 1, story

    def test_severity_follows_tier(self, rigged):
        story = "hot matches store as critical and warm as high, per the lazy_heat canon"
        event = _event()
        event.metadata["matches"][0]["tier"] = "warm"
        event.metadata["matches"][0]["cve_id"] = "CVE-2025-9999"
        event.metadata["cve_ids"] = ["CVE-2025-9999"]
        sink.apply(event)
        db = LazyOwnDB(str(rigged["db_path"]))
        rows = {r.get("name"): r for r in db.vuln_list(db.default_workspace())}
        assert str(rows["CVE-2025-9999"].get("severity") or "").lower() == "high", story
