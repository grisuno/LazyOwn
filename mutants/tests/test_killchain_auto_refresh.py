"""BDD-style tests for the periodic kill-chain auto-refresh in the tips engine.

Scenario: the unified kill-chain progress is re-surfaced after commands,
both on a periodic cadence and whenever the active phase advances.
"""

from __future__ import annotations

from cli.tips_engine import TipsConfig, TipsEngine


def _engine(**overrides) -> tuple[TipsEngine, list[str]]:
    calls: list[str] = []
    config = TipsConfig(enabled=bool(overrides.get("enabled", True)))
    config.killchain_auto_every = int(overrides.get("every", 0))
    config.killchain_auto_on_phase_change = bool(overrides.get("on_phase_change", True))
    engine = TipsEngine(config=config)
    engine.on_killchain_display = lambda: calls.append("show")
    return engine, calls


class TestPeriodicAutoRefresh:
    def test_shows_immediately_on_phase_change(self):
        # Given: auto cadence every 2, phase-change trigger on
        engine, calls = _engine(every=2, on_phase_change=True)
        # When: an exploit command is processed (phase changed from none)
        engine._maybe_auto_show_killchain("exploit")
        # Then: the kill-chain is surfaced because the phase moved
        assert calls == ["show"]

    def test_shows_on_cadence_without_phase_change(self):
        # Given: cadence every 2 commands, phase already established
        engine, calls = _engine(every=2, on_phase_change=False)
        engine._last_auto_phase = "exploit"
        # When: two same-phase commands execute
        engine._maybe_auto_show_killchain("exploit")
        engine._maybe_auto_show_killchain("exploit")
        # Then: it shows only on the cadence boundary (2nd call)
        assert calls == ["show"]

    def test_cadence_below_every_surpresses(self):
        # Given: cadence 5, phase unchanged
        engine, calls = _engine(every=5, on_phase_change=False)
        engine._last_auto_phase = "exploit"
        # When: only one command runs
        engine._maybe_auto_show_killchain("exploit")
        # Then: nothing is shown yet
        assert calls == []

    def test_phase_change_beats_periodic_cadence(self):
        # Given: cadence 10 (periodic would not fire yet)
        engine, calls = _engine(every=10, on_phase_change=True)
        engine._last_auto_phase = "exploit"
        # When: phase advances to privesc after one command
        engine._maybe_auto_show_killchain("privesc")
        # Then: the kill-chain is surfaced because of the transition
        assert calls == ["show"]

    def test_disabled_engine_never_shows(self):
        # Given: the engine is disabled
        engine, calls = _engine(enabled=False, every=1, on_phase_change=True)
        # When: a phase-changing command runs
        engine._maybe_auto_show_killchain("exploit")
        # Then: nothing is surfaced
        assert calls == []

    def test_zero_every_and_no_phase_change_never_shows(self):
        # Given: auto-refresh disabled (every=0, no phase trigger)
        engine, calls = _engine(every=0, on_phase_change=False)
        engine._last_auto_phase = "exploit"
        # When: several commands run
        for _ in range(3):
            engine._maybe_auto_show_killchain("exploit")
        # Then: never shown
        assert calls == []
