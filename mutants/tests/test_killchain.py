"""Tests for cli/killchain.py.

The suite verifies that kill-chain progress is derived correctly from the
daemon event stream: phases the engagement passed through are marked done, the
current phase is active, later phases stay pending, and per-phase activity and
reward are accumulated. It also pins the world-model fallback used when no
events are available.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.killchain import (  # noqa: E402
    DEFAULT_PHASES,
    STATE_ACTIVE,
    STATE_DONE,
    STATE_PENDING,
    PhaseProgress,
    compute_killchain,
)


def _states(progress: list[PhaseProgress]) -> dict[str, str]:
    return {p.key: p.state for p in progress}


def test_empty_events_all_pending_without_world():
    progress = compute_killchain([], {})
    assert len(progress) == len(DEFAULT_PHASES)
    assert all(p.state == STATE_PENDING for p in progress)


def test_current_phase_from_step_events():
    events = [
        {"type": "STEP_DONE", "payload": {"phase": "recon", "reward": 0.4}},
        {"type": "STEP_START", "payload": {"phase": "enum"}},
    ]
    states = _states(compute_killchain(events, {}))
    assert states["recon"] == STATE_DONE
    assert states["enum"] == STATE_ACTIVE
    assert states["exploit"] == STATE_PENDING


def test_phase_advance_event_sets_current():
    events = [
        {"type": "STEP_DONE", "payload": {"phase": "recon"}},
        {"type": "PHASE_ADVANCE", "payload": {"to": "exploit"}},
    ]
    states = _states(compute_killchain(events, {}))
    assert states["recon"] == STATE_DONE
    assert states["scan"] == STATE_DONE
    assert states["enum"] == STATE_DONE
    assert states["exploit"] == STATE_ACTIVE
    assert states["privesc"] == STATE_PENDING


def test_activity_and_reward_accumulate():
    events = [
        {"type": "STEP_START", "payload": {"phase": "recon"}},
        {"type": "STEP_DONE", "payload": {"phase": "recon", "reward": 0.2}},
        {"type": "STEP_DONE", "payload": {"phase": "recon", "reward": 0.3}},
        {"type": "STEP_START", "payload": {"phase": "enum"}},
    ]
    progress = {p.key: p for p in compute_killchain(events, {})}
    assert progress["recon"].activity == 3
    assert progress["recon"].reward == 0.5
    assert progress["enum"].activity == 1


def test_world_phase_fallback_when_no_events():
    states = _states(compute_killchain([], {"phase": "scan"}))
    assert states["recon"] == STATE_DONE
    assert states["scan"] == STATE_ACTIVE


def test_explicit_completed_phases_respected():
    states = _states(compute_killchain([], {"completed_phases": ["report"]}))
    assert states["report"] == STATE_DONE


def test_unknown_phase_in_event_is_ignored():
    events = [{"type": "STEP_DONE", "payload": {"phase": "nonsense"}}]
    progress = compute_killchain(events, {})
    assert all(p.activity == 0 for p in progress)


def test_non_dict_payload_is_tolerated():
    events = [{"type": "STEP_DONE", "payload": None}]
    progress = compute_killchain(events, {})
    assert all(p.state == STATE_PENDING for p in progress)
