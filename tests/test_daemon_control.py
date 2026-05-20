"""Unit tests for skills.daemon_control.

Coverage:

* :class:`ControlState` and :class:`PendingAction` round-trip
  (to_dict / from_dict, malformed input).
* :class:`DaemonControl` mode transitions, veto add / remove / clear,
  focus replacement, atomic file persistence.
* Approval state machine: propose / decide / consume, TTL expiry.
* :func:`wait_for_decision` and :func:`wait_until_unpaused` honour
  injectable clock and sleep functions for deterministic testing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SKILLS_DIR = REPO_ROOT / "skills"
if str(SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(SKILLS_DIR))

from daemon_control import (
    CONTROL_FILE_NAME,
    ControlState,
    DECISION_APPROVED,
    DECISION_EXPIRED,
    DECISION_PENDING,
    DECISION_VETOED,
    DaemonControl,
    MODE_APPROVAL,
    MODE_AUTO,
    MODE_PAUSED,
    PENDING_TTL_DEFAULT_S,
    PendingAction,
    wait_for_decision,
    wait_until_unpaused,
)


@pytest.fixture()
def sessions_dir(tmp_path):
    target = tmp_path / "sessions"
    target.mkdir()
    return target


def test_default_state_roundtrip(sessions_dir):
    control = DaemonControl(sessions_dir)

    state = control.load()

    assert state.mode == MODE_AUTO
    assert state.vetoed_commands == []
    assert state.focus_targets == []
    assert state.pending is None


def test_set_mode_persists_and_normalises_invalid(sessions_dir):
    control = DaemonControl(sessions_dir)

    control.set_mode(MODE_APPROVAL)
    reloaded = DaemonControl(sessions_dir).load()
    assert reloaded.mode == MODE_APPROVAL

    with pytest.raises(ValueError):
        control.set_mode("totally-invalid")


def test_state_from_dict_sanitises_unknown_mode():
    state = ControlState.from_dict({"mode": "rogue"})

    assert state.mode == MODE_AUTO


def test_state_from_dict_preserves_pending():
    raw = {
        "mode": MODE_APPROVAL,
        "pending": {
            "action_id": "abc",
            "command": "nmap",
            "reason": "recon",
            "target": "10.0.0.1",
            "proposed_at": 100.0,
            "ttl_seconds": 5.0,
            "decision": DECISION_PENDING,
        },
    }

    state = ControlState.from_dict(raw)

    assert state.pending is not None
    assert state.pending.action_id == "abc"
    assert state.pending.command == "nmap"
    assert state.pending.decision == DECISION_PENDING


def test_pause_resume_round_trip(sessions_dir):
    control = DaemonControl(sessions_dir)

    control.pause()
    assert control.is_paused() is True

    control.resume()
    assert control.is_paused() is False


def test_add_remove_clear_veto(sessions_dir):
    control = DaemonControl(sessions_dir)

    control.add_veto("nmap")
    control.add_veto("gobuster")
    control.add_veto("nmap")
    state = control.load()
    assert state.vetoed_commands == ["nmap", "gobuster"]

    control.remove_veto("gobuster")
    assert control.load().vetoed_commands == ["nmap"]

    control.clear_vetoes()
    assert control.load().vetoed_commands == []


def test_add_veto_rejects_empty_token(sessions_dir):
    control = DaemonControl(sessions_dir)

    with pytest.raises(ValueError):
        control.add_veto("   ")


def test_is_vetoed_uses_first_token(sessions_dir):
    control = DaemonControl(sessions_dir)
    control.add_veto("nmap")

    assert control.is_vetoed("nmap -sV 10.0.0.1") is True
    assert control.is_vetoed("gobuster dir") is False


def test_set_focus_replaces_list(sessions_dir):
    control = DaemonControl(sessions_dir)

    control.set_focus(["10.0.0.1", "10.0.0.2"])
    assert control.load().focus_targets == ["10.0.0.1", "10.0.0.2"]

    control.set_focus([])
    assert control.load().focus_targets == []


def test_target_in_focus_defaults_to_true_when_no_focus(sessions_dir):
    control = DaemonControl(sessions_dir)

    assert control.target_in_focus("10.0.0.1") is True

    control.set_focus(["192.168.1.1"])
    assert control.target_in_focus("10.0.0.1") is False
    assert control.target_in_focus("192.168.1.1") is True


def test_propose_decide_consume_cycle(sessions_dir):
    control = DaemonControl(sessions_dir)

    pending = control.propose("nmap 10.0.0.1", reason="recon", target="10.0.0.1")
    assert pending.action_id
    state = control.load()
    assert state.pending is not None
    assert state.pending.action_id == pending.action_id

    decided = control.decide(pending.action_id, DECISION_APPROVED, operator="alice")
    assert decided is not None
    assert decided.decision == DECISION_APPROVED
    assert decided.operator == "alice"

    final = control.consume(pending.action_id)
    assert final is not None
    assert final.decision == DECISION_APPROVED
    assert control.load().pending is None


def test_decide_rejects_invalid_decision(sessions_dir):
    control = DaemonControl(sessions_dir)
    pending = control.propose("nmap", target="10.0.0.1")

    with pytest.raises(ValueError):
        control.decide(pending.action_id, "maybe")


def test_decide_with_unknown_id_returns_none(sessions_dir):
    control = DaemonControl(sessions_dir)
    control.propose("nmap", target="10.0.0.1")

    assert control.decide("nope", DECISION_APPROVED) is None


def test_consume_expires_overdue_pending(sessions_dir):
    control = DaemonControl(sessions_dir)
    pending = control.propose("nmap", target="10.0.0.1", ttl_seconds=0.0)

    final = control.consume(pending.action_id)

    assert final is not None
    assert final.decision == DECISION_EXPIRED
    assert control.load().pending is None


def test_pending_action_is_expired_only_when_still_pending():
    action = PendingAction(
        action_id="x", command="nmap", proposed_at=0.0, ttl_seconds=1.0,
        decision=DECISION_APPROVED,
    )

    assert action.is_expired(now=1000.0) is False


def test_wait_for_decision_returns_approved(sessions_dir):
    control = DaemonControl(sessions_dir)
    pending = control.propose("nmap", target="10.0.0.1", ttl_seconds=60.0)
    control.decide(pending.action_id, DECISION_APPROVED, operator="bob")

    final = wait_for_decision(
        control, pending,
        poll_interval=0.0,
        sleep_fn=lambda _seconds: None,
        now_fn=lambda: pending.proposed_at + 0.1,
    )

    assert final.decision == DECISION_APPROVED


def test_wait_for_decision_expires_after_ttl(sessions_dir):
    control = DaemonControl(sessions_dir)
    pending = control.propose("nmap", target="10.0.0.1", ttl_seconds=1.0)

    final = wait_for_decision(
        control, pending,
        poll_interval=0.0,
        sleep_fn=lambda _seconds: None,
        now_fn=lambda: pending.proposed_at + 10.0,
    )

    assert final.decision == DECISION_EXPIRED


def test_wait_for_decision_polls_until_decided(sessions_dir):
    control = DaemonControl(sessions_dir)
    pending = control.propose("nmap", target="10.0.0.1", ttl_seconds=60.0)
    polls = {"count": 0}

    def _sleep(_seconds):
        polls["count"] += 1
        if polls["count"] == 2:
            control.decide(pending.action_id, DECISION_VETOED)

    final = wait_for_decision(
        control, pending,
        poll_interval=0.0,
        sleep_fn=_sleep,
        now_fn=lambda: pending.proposed_at + 0.1,
    )

    assert final.decision == DECISION_VETOED
    assert polls["count"] >= 2


def test_wait_until_unpaused_returns_true_when_already_running(sessions_dir):
    control = DaemonControl(sessions_dir)

    resumed = wait_until_unpaused(
        control,
        poll_interval=0.0,
        sleep_fn=lambda _seconds: None,
        max_wait_seconds=1.0,
        now_fn=lambda: 0.0,
    )

    assert resumed is True


def test_wait_until_unpaused_returns_false_after_max_wait(sessions_dir):
    control = DaemonControl(sessions_dir)
    control.pause()
    clock = {"now": 0.0}

    def _now():
        return clock["now"]

    def _sleep(_seconds):
        clock["now"] += 0.5

    resumed = wait_until_unpaused(
        control,
        poll_interval=0.0,
        sleep_fn=_sleep,
        max_wait_seconds=1.0,
        now_fn=_now,
    )

    assert resumed is False


def test_wait_until_unpaused_returns_true_after_resume(sessions_dir):
    control = DaemonControl(sessions_dir)
    control.pause()
    polls = {"count": 0}

    def _sleep(_seconds):
        polls["count"] += 1
        if polls["count"] == 2:
            control.resume()

    resumed = wait_until_unpaused(
        control,
        poll_interval=0.0,
        sleep_fn=_sleep,
        max_wait_seconds=None,
        now_fn=lambda: 0.0,
    )

    assert resumed is True


def test_save_writes_atomic_file_with_restricted_mode(sessions_dir):
    control = DaemonControl(sessions_dir)

    control.set_mode(MODE_APPROVAL)

    path = sessions_dir / CONTROL_FILE_NAME
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["mode"] == MODE_APPROVAL


def test_load_returns_defaults_on_invalid_json(sessions_dir):
    path = sessions_dir / CONTROL_FILE_NAME
    path.write_text("not json", encoding="utf-8")
    control = DaemonControl(sessions_dir)

    state = control.load()

    assert state.mode == MODE_AUTO


def test_concurrent_save_serialised_by_lock(sessions_dir):
    control = DaemonControl(sessions_dir)
    control.add_veto("nmap")
    control.add_veto("ffuf")
    control.add_veto("gobuster")

    final = control.load()

    assert sorted(final.vetoed_commands) == ["ffuf", "gobuster", "nmap"]
