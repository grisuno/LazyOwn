"""Tests for modules.progress_ledger — objective-progress strike rule.

Covers:
    - StrikePolicy clamping
    - Engagement id confinement
    - Brief diff signals (facts/findings/goals/verdicts)
    - Strikes increasing on hypothesis-only and idle rounds
    - Progress resets the counter
    - Handoff decision at the configured cap
    - Persistence across reload
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def ledger_module():
    import modules.progress_ledger as pl

    return pl


@pytest.fixture
def tmp_base():
    with tempfile.TemporaryDirectory() as directory:
        yield Path(directory)


class TestPolicy:
    def test_clamp(self, ledger_module):
        pl = ledger_module
        assert pl.StrikePolicy(max_strikes=99).clamped().max_strikes == 20
        assert pl.StrikePolicy(max_strikes=0).clamped().max_strikes == 1

    def test_engagement_confined(self, ledger_module, tmp_base):
        pl = ledger_module
        with pytest.raises(pl.InvalidEngagement):
            pl.ProgressLedger("../evil", tmp_base)


class TestObserve:
    def test_hypothesis_only_strikes(self, ledger_module, tmp_base):
        pl = ledger_module
        led = pl.ProgressLedger("t1", tmp_base, pl.StrikePolicy(3, True)).load()
        for expected in (1, 2, 3):
            signals = led.signals_from_brief({"facts": 0, "findings": 0, "new_intents": 4})
            result = led.observe(signals)
            assert result["strikes"] == expected
        assert result["decision"] == "handoff"

    def test_idle_round_strikes(self, ledger_module, tmp_base):
        pl = ledger_module
        led = pl.ProgressLedger("t1", tmp_base, pl.StrikePolicy(2, True)).load()
        signals = led.signals_from_brief({"facts": 0, "findings": 0})
        result = led.observe(signals)
        assert result["decision"] == "strike"
        assert "no intents" in result["reason"]

    def test_progress_resets(self, ledger_module, tmp_base):
        pl = ledger_module
        led = pl.ProgressLedger("t1", tmp_base, pl.StrikePolicy(3, True)).load()
        led.observe(led.signals_from_brief({"facts": 0, "findings": 0, "new_intents": 2}))
        led.observe(led.signals_from_brief({"facts": 0, "findings": 0, "new_intents": 2}))
        signals = led.signals_from_brief({"facts": 3, "findings": 1, "new_intents": 2})
        result = led.observe(signals)
        assert result["progress"] is True
        assert result["strikes"] == 0
        assert result["decision"] == "progress"

    def test_reproduced_verdict_counts(self, ledger_module, tmp_base):
        pl = ledger_module
        led = pl.ProgressLedger("t1", tmp_base, pl.StrikePolicy(3, True)).load()
        led.signals_from_brief({"facts": 0, "findings": 0})
        led.observe(led.signals_from_brief({"facts": 0, "findings": 0, "new_intents": 0}))
        signals = led.signals_from_brief({"facts": 0, "findings": 0, "new_intents": 0})
        signals = pl.RoundSignals(facts=0, findings=0, reproduced=1)
        result = led.observe(signals)
        assert result["progress"] is True

    def test_cap_disabled_keeps_strike(self, ledger_module, tmp_base):
        pl = ledger_module
        led = pl.ProgressLedger("t1", tmp_base, pl.StrikePolicy(1, False)).load()
        result = led.observe(led.signals_from_brief({"facts": 0, "findings": 0, "new_intents": 8}))
        assert result["decision"] == "strike"


class TestPersistence:
    def test_reload_keeps_strikes(self, ledger_module, tmp_base):
        pl = ledger_module
        first = pl.ProgressLedger("t1", tmp_base, pl.StrikePolicy(3, True)).load()
        first.observe(first.signals_from_brief({"facts": 0, "findings": 0, "new_intents": 9}))
        second = pl.ProgressLedger("t1", tmp_base, pl.StrikePolicy(3, True)).load()
        assert second.strikes == 1
