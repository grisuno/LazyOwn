"""Stuck-loop shapes contract: AAAA plus ABABAB oscillation detection.

Every scenario states Given, When, Then. The detector keeps
caller-owned windows; the alternating shape needs six consecutive
records inside the window; varied traffic never triggers.
"""

from __future__ import annotations

from modules.loop_guardrails import RepeatDetector


def test_alternating_pair_never_triggers_below_six():
    """Given a small window, When three alternating commands run, Then not stuck."""
    detector = RepeatDetector(window=3)
    assert detector.record("cmd one") is False
    assert detector.record("cmd two") is False
    assert detector.record("cmd one") is False


def test_full_oscillation_triggers_at_six_records():
    """Given six alternating records in a window of eight, When recorded, Then stuck."""
    detector = RepeatDetector(window=8)
    sequence = ["probe one", "probe two"] * 4
    stuck = any(detector.record(command) for command in sequence)
    assert stuck is True
    first, second = detector.oscillation_pair()
    assert {first, second} == {"probe one", "probe two"}


def test_identical_window_triggers_and_pair_empty():
    """Given one identical command repeated, When the window fills, Then stuck with empty pair."""
    detector = RepeatDetector()
    sequence = ["same"] * 5
    stuck = any(detector.record(command) for command in sequence)
    assert stuck is True
    assert detector.oscillation_pair() == ("", "")


def test_varied_traffic_never_triggers():
    """Given varied progress, When recorded, Then not stuck and no pair lingers."""
    detector = RepeatDetector(window=8)
    signals = [
        detector.record("scan 22"),
        detector.record("scan 80"),
        detector.record("probe ssh"),
        detector.record("scan 445"),
        detector.record("probe http"),
    ]
    assert not any(signals)
    assert detector.oscillation_pair() == ("", "")


def test_reset_clears_pair():
    """Given a latched oscillation, When reset, Then the pair empties."""
    detector = RepeatDetector(window=8)
    for command in ["a1", "b1"] * 3:
        detector.record(command)
    detector.reset()
    assert detector.oscillation_pair() == ("", "")
