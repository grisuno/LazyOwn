"""Configurable pacing: EdrPacer ranges, jitter scaling, sleeper windows.

The orchestrator ``pacing`` block (YAML profile + payload override)
drives the shared EdrPacer used by the loop workers and ChainRunner.
"""

from __future__ import annotations

import time
from modules.loop_guardrails import EdrPacer
from modules.orchestrator_config import SLEEPER_WINDOW_RE, validate_config


def test_sleeper_window_regex_accepts_valid_windows():
    """Given valid HH:MM-HH:MM strings, When matched, Then accepted."""
    assert SLEEPER_WINDOW_RE.match("01:00-05:00")
    assert SLEEPER_WINDOW_RE.match("23:30-03:15")
    assert not SLEEPER_WINDOW_RE.match("25:00-05:00")
    assert not SLEEPER_WINDOW_RE.match("0100-0500")


def test_edr_pacer_configurable_pause_ranges():
    """Given custom ranges, When level rises, Then the drawn delay stays
    inside the configured range."""
    pacer = EdrPacer(pause_ranges={1: (7.0, 9.0)}, rng=lambda low, high: (low + high) / 2)
    pacer.observe("nmap -sS host", 45.0, "done")
    assert pacer.level == 1
    delay = pacer.inter_step_delay()
    assert 7.0 <= delay <= 9.0


def test_edr_pacer_empty_ranges_disables_level_pauses():
    """Given empty pause ranges, When the level rises, Then no delay."""
    pacer = EdrPacer(pause_ranges={})
    pacer.observe("nmap -sS host", 45.0, "done")
    assert pacer.level == 1
    assert pacer.inter_step_delay() == 0.0


def test_edr_pacer_jitter_scales_drawn_delay():
    """Given a +100 pct jitter band, When a pause is drawn, Then the
    midpoint sampler applies a 1.5x factor."""
    pacer = EdrPacer(pause_ranges={1: (5.0, 5.0)}, jitter_pct=(0.0, 100.0), rng=lambda low, high: (low + high) / 2)
    pacer.observe("nmap -sS host", 45.0, "done")
    assert pacer.inter_step_delay() == 7.5


def test_edr_pacer_max_delay_clamps():
    """Given a max delay of 3s, When the range exceeds it, Then clamped."""
    pacer = EdrPacer(pause_ranges={1: (2.0, 50.0)}, max_delay_sec=3.0, rng=lambda low, high: high)
    pacer.observe("nmap -sS host", 45.0, "done")
    assert pacer.inter_step_delay() <= 3.0


def test_edr_pacer_sleeper_window_extends_delay():
    """Given a quiet window covering now, When a calm step ends, Then the
    delay extends to the window end, clamped by max_delay_sec."""
    now = time.mktime((2026, 1, 1, 2, 0, 0, 0, 1, -1))
    window_end = time.mktime((2026, 1, 1, 5, 0, 0, 0, 1, -1))
    pacer = EdrPacer(
        sleeper_windows=["01:00-05:00"],
        max_delay_sec=600.0,
        clock=lambda: now,
        rng=lambda low, high: (low + high) / 2,
    )
    assert pacer.in_sleeper_window(now) is True
    assert pacer.describe()["in_sleeper_window"] is True
    expected = min(window_end - now, 600.0)
    assert abs(pacer.sleeper_delay(now) - expected) < 2.0
    assert abs(pacer.inter_step_delay() - expected) < 2.0


def test_edr_pacer_sleeper_window_outside_is_zero():
    """Given a quiet window away from now, When calm, Then no delay."""
    now = time.mktime((2026, 1, 1, 12, 0, 0, 0, 1, -1))
    pacer = EdrPacer(sleeper_windows=["01:00-05:00"], clock=lambda: now)
    assert pacer.in_sleeper_window(now) is False
    assert pacer.sleeper_delay(now) == 0.0
    assert pacer.inter_step_delay() == 0.0


def test_edr_pacer_sleeper_wraps_midnight():
    """Given a 23:00-03:00 window and 02:00 local time, Then inside."""
    now = time.mktime((2026, 1, 1, 2, 0, 0, 0, 1, -1))
    pacer = EdrPacer(sleeper_windows=["23:00-03:00"], clock=lambda: now)
    assert pacer.in_sleeper_window(now) is True


def test_edr_pacer_parse_windows_skips_invalid():
    """Given malformed windows, When parsed, Then only valid survive."""
    assert EdrPacer.parse_windows(["01:00-05:00", "bad", "99:99-05:00"]) == ((1, 0, 5, 0),)


def test_edr_pacer_from_config_reads_orchestrator(monkeypatch):
    """Given a patched pacing section, When from_config, Then the pacer
    carries the configured knobs."""
    import modules.orchestrator_config as oc

    monkeypatch.setattr(
        oc,
        "pacing",
        lambda: {
            "enabled": True,
            "jitter_pct_min": 10.0,
            "jitter_pct_max": 20.0,
            "edr_pause_ranges": {1: (3.0, 4.0)},
            "max_delay_sec": 60.0,
            "sleeper_windows": ("02:00-04:00",),
        },
    )
    pacer = EdrPacer.from_config()
    described = pacer.describe()
    assert described["jitter_pct"] == (10.0, 20.0)
    assert described["max_delay_sec"] == 60.0
    assert described["sleeper_windows"] == ["02:00-04:00"]


def test_edr_pacer_from_config_disabled_is_inert(monkeypatch):
    """Given pacing disabled, When from_config, Then no delay at all."""
    import modules.orchestrator_config as oc

    monkeypatch.setattr(oc, "pacing", lambda: {"enabled": False})
    pacer = EdrPacer.from_config()
    pacer.observe("nmap -sS host", 45.0, "done")
    assert pacer.inter_step_delay() == 0.0


def test_validate_config_accepts_pacing_block():
    """Given a profile with a valid pacing block, Then no errors."""
    data = {
        "version": 1,
        "profiles": {
            "default": {
                "pacing": {
                    "enabled": True,
                    "jitter_pct_min": -30,
                    "jitter_pct_max": 60,
                    "max_delay_sec": 120,
                    "edr_pause_ranges": {1: [2.0, 5.0]},
                    "sleeper_windows": ["01:00-05:00"],
                    "round_sleep_sec": 15,
                }
            }
        },
    }
    assert validate_config(data) == []


def test_validate_config_rejects_bad_pacing():
    """Given malformed pacing values, Then each is reported."""
    data = {
        "version": 1,
        "profiles": {
            "default": {
                "pacing": {
                    "enabled": "yes",
                    "max_delay_sec": -5,
                    "sleeper_windows": ["noon"],
                    "edr_pause_ranges": {1: [9.0, 2.0]},
                }
            }
        },
    }
    errors = validate_config(data)
    assert any("pacing enabled" in error for error in errors)
    assert any("pacing max_delay_sec" in error for error in errors)
    assert any("pacing sleeper_windows" in error for error in errors)
    assert any("edr_pause_ranges" in error for error in errors)


def test_validate_config_rejects_pacing_not_mapping():
    """Given pacing as a scalar, Then reported as a mapping error."""
    data = {"version": 1, "profiles": {"default": {"pacing": 5}}}
    assert any("pacing must be a mapping" in error for error in validate_config(data))
