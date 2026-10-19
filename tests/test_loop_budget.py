"""BDD tests for first-class budget flags on the loop runner."""

from __future__ import annotations

import pytest

from modules.lazy_runner import LoopRunConfig, parse_loop_line


class TestBudgetParsing:
    """--budget parses, clamps and rejects loudly."""

    def test_budget_pairs_parsed(self):
        """Given pairs, Then the config carries the caps."""
        story = "one flag, several caps"
        cfg = parse_loop_line("--budget rounds=4,toolcalls=900,findings=6 'gain access'")
        assert cfg.budget == {"rounds": 4.0, "toolcalls": 900.0, "findings": 6.0}, story

    def test_minimums_clamped(self):
        """Given a zero finding cap, Then clamps to the bottom limit."""
        story = "nonsense bottoms are rejected by clamping"
        cfg = parse_loop_line("--budget rounds=0,timeout_sec=2")
        assert cfg.budget == {"rounds": 1.0, "timeout_sec": 60.0}, story

    def test_unknown_key_rejected(self):
        """Given an unknown key, Then the parser raises."""
        story = "typos must fail loudly, not silently pass"
        with pytest.raises(ValueError):
            parse_loop_line("--budget cashback=5")

    def test_budget_confirm_toggle(self):
        """Given the toggle, Then confirm is set."""
        story = "HITL gate opt-in"
        cfg = parse_loop_line("--budget-confirm --budget rounds=2 t")
        assert cfg.budget_confirm is True and cfg.budget == math_close({"rounds": 2}), story


def math_close(budget: dict) -> dict:
    return {k: float(v) for k, v in budget.items()}


class TestBudgetGate:
    """The confirm gate blocks unless approved or autonomous."""

    def test_gate_blocks_when_declined(self, monkeypatch):
        """Given the user answering n, Then run aborts before the engine boots."""
        from modules import lazy_runner

        monkeypatch.setattr("builtins.input", lambda *a, **k: "n")
        result = lazy_runner._budget_declined(
            LoopRunConfig(goal="x", budget={"rounds": 2.0}, budget_confirm=True)
        )
        assert result is True

    def test_gate_pass_when_approved(self, monkeypatch):
        """Given yes, Then the run proceeds."""
        from modules import lazy_runner

        monkeypatch.setattr("builtins.input", lambda *a, **k: "y")
        result = lazy_runner._budget_declined(
            LoopRunConfig(goal="x", budget={"rounds": 2.0}, budget_confirm=True)
        )
        assert result is False

    def test_gate_skipped_autonomous(self, monkeypatch):
        """Given LAZYOWN_AUTONOMOUS=1, Then no prompt appears."""
        from modules import lazy_runner

        monkeypatch.setenv("LAZYOWN_AUTONOMOUS", "1")
        monkeypatch.setattr("builtins.input", lambda *a, **k: pytest.fail("no prompt expected"))
        assert lazy_runner._budget_declined(
            LoopRunConfig(goal="x", budget={"rounds": 2.0}, budget_confirm=True)
        ) is False
