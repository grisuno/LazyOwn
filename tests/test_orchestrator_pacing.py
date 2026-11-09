"""Pacing tab: jitter and sleeper controls round-trip through set_pacing.

Given the operator edits the Pacing tab,
When the fields are saved,
Then valid jitter, sleeper windows and EDR pause ranges persist into the
payload orchestrator.pacing block and reach the loop's EdrPacer, while
malformed windows or ranges are rejected and reported rather than stored.
"""

from __future__ import annotations

import pytest

from cli.orchestrator_assets_tabs import (
    OrchestratorAssetsMixin,
    format_edr_pause_ranges,
    format_sleeper_windows,
    parse_edr_pause_ranges,
    parse_sleeper_windows,
)


@pytest.fixture()
def pacing_store(monkeypatch):
    """Back orchestrator_config pacing reads/writes with an in-memory payload."""
    from modules import orchestrator_config as oc

    store: dict = {}
    monkeypatch.setattr(oc, "_payload", lambda: dict(store))

    def _save(payload: dict) -> None:
        store.clear()
        store.update(payload)
        oc._invalidate()

    monkeypatch.setattr(oc, "_save", _save)
    monkeypatch.setattr(oc, "profile_config", lambda name="": {})
    return store


def _saver():
    """Return a bound save_pacing callable without a full Textual app."""
    return OrchestratorAssetsMixin.save_pacing.__get__(object(), OrchestratorAssetsMixin)


def test_parse_sleeper_windows_splits_valid_and_invalid():
    valid, invalid = parse_sleeper_windows("22:00-06:00, noon, 12:00-13:00, 25:00-01:00")
    assert valid == ["22:00-06:00", "12:00-13:00"]
    assert invalid == ["noon", "25:00-01:00"]


def test_format_sleeper_windows_round_trips():
    assert format_sleeper_windows(("22:00-06:00", "12:00-13:00")) == "22:00-06:00, 12:00-13:00"


def test_parse_edr_pause_ranges_accepts_level_low_high():
    ranges, invalid = parse_edr_pause_ranges("1:2-5,2:5-15")
    assert ranges == {1: [2.0, 5.0], 2: [5.0, 15.0]}
    assert invalid == []


def test_parse_edr_pause_ranges_rejects_inverted_and_garbage():
    ranges, invalid = parse_edr_pause_ranges("1:9-2, x:y")
    assert ranges == {}
    assert sorted(invalid) == ["1:9-2", "x:y"]


def test_format_edr_pause_ranges_round_trips():
    assert format_edr_pause_ranges({1: (2.0, 5.0), 2: (5.0, 15.0)}) == "1:2-5,2:5-15"


def test_save_pacing_persists_valid_sleeper_windows(pacing_store):
    from modules import orchestrator_config as oc

    summary = _saver()(
        {
            "orchestrator.pacing.sleeper_windows": "22:00-06:00, 12:00-13:00",
            "orchestrator.pacing.jitter_pct_min": "10",
        }
    )
    assert summary["errors"] == []
    resolved = oc.pacing()
    assert resolved["sleeper_windows"] == ("22:00-06:00", "12:00-13:00")
    assert resolved["jitter_pct_min"] == 10.0


def test_save_pacing_persists_edr_pause_ranges(pacing_store):
    from modules import orchestrator_config as oc

    summary = _saver()({"orchestrator.pacing.edr_pause_ranges": "1:2-5,2:5-15"})
    assert summary["errors"] == []
    resolved = oc.pacing()
    assert resolved["edr_pause_ranges"] == {1: (2.0, 5.0), 2: (5.0, 15.0)}


def test_save_pacing_rejects_malformed_window(pacing_store):
    from modules import orchestrator_config as oc

    summary = _saver()({"orchestrator.pacing.sleeper_windows": "noon"})
    assert any("sleeper window" in err for err in summary["errors"])
    assert oc.pacing()["sleeper_windows"] == ()


def test_saved_windows_reach_edr_pacer(pacing_store):
    from modules import orchestrator_config as oc
    from modules.loop_guardrails import EdrPacer

    _saver()({"orchestrator.pacing.sleeper_windows": "01:00-05:00"})
    assert oc.pacing()["sleeper_windows"] == ("01:00-05:00",)
    pacer = EdrPacer.from_config()
    assert pacer.describe()["sleeper_windows"] == ["01:00-05:00"]
