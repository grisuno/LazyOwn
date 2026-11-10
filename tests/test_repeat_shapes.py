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


def test_periodic_cycle_of_five_triggers_after_two_rounds():
    """Given a five-command recon cycle repeating round after round,
    When the second full round completes, Then stuck fires with the cycle."""
    detector = RepeatDetector(window=8)
    cycle = ["ping t", "searchsploit t", "lazynmap t", "auto_populate t", "facts_show t"]
    fired = [detector.record(command) for command in cycle * 2]
    assert not any(fired[: len(cycle)]), "one full round is still progress"
    assert fired[-1] is True
    assert tuple(c.split()[0] for c in detector.cycle()) == ("ping", "searchsploit", "lazynmap", "auto_populate", "facts_show")


def test_periodic_cycle_never_fires_on_varied_progress():
    """Given ten distinct real-work commands, When recorded, Then not stuck."""
    detector = RepeatDetector(window=8)
    sequence = ["scan 21", "scan 80", "probe ssh", "scan 445", "probe http", "dig t", "nmap t", "curl t", "hydra t", "enum t"]
    assert not any(detector.record(command) for command in sequence)
    assert detector.cycle() == ()


def test_periodic_cycle_never_fires_below_two_rounds():
    """Given exactly one full round of a three-command cycle, When recorded, Then not stuck."""
    detector = RepeatDetector(window=8)
    sequence = ["a t", "b t", "c t"]
    assert not any(detector.record(command) for command in sequence)
    assert detector.cycle() == ()


def test_describe_reports_cycle_shape():
    """Given a stuck cycle, When described, Then the sentence names a cycle."""
    detector = RepeatDetector(window=8)
    sequence = ["ping t", "searchsploit t", "lazynmap t", "auto_populate t", "facts_show t"] * 2
    for command in sequence:
        detector.record(command)
    assert "cycle of 5 commands x2" in detector.describe()


def test_nine_step_round_family_is_caught_after_two_rounds():
    """Given the 9-step recon family the loop re-runs every round (the
    t0193 runaway), When the family completes twice, Then the worker
    window marks it stuck: no third round ever runs."""
    detector = RepeatDetector(window=16)
    family = [
        "ping 127.0.0.1",
        "lazynmap 127.0.0.1",
        "rustscan 127.0.0.1",
        "batchnmap 127.0.0.1",
        "dnsenum 127.0.0.1",
        "lazymsfvenom 127.0.0.1",
        "auto_populate 127.0.0.1",
        "facts_show 127.0.0.1",
        "searchsploit 127.0.0.1",
    ]
    fired_flags = [detector.record(command) for command in family * 2]
    assert not any(fired_flags[: len(family)]), "one full round is real work"
    assert any(fired_flags[len(family) :]), "two full rounds with no new intel is a stall"
    assert "cycle of 9 commands x2" in detector.describe()
