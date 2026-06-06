"""Tests for the ELO + karma + methodology extensions of cli/engagement_hooks.py.

Covers:
  * get_karma_name thresholds (mirror of lazyc2.py).
  * _award_elo additive structure (base, high-value, phase, first-time, new phase).
  * _sync_user_elo dual-write to users.json (atomic, schema-preserving).
  * _persist_notification atomic append + ring cap.
  * Methodology rewards: _render_methodology_{task,objective,note} (data-driven,
    return False when artefact missing, return True when artefact has entries).
  * _check_karma_up fires on threshold cross and is idempotent.
  * render_engagement_hook integration: ELO accumulates, dashboard notification
    persisted on VRI reward, karma_name reflected in state snapshot.

All tests redirect every module-level Path to a per-test tmp directory so the
real ``sessions/``, ``payload.json`` and ``users.json`` are never touched.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
sys.path.insert(0, str(REPO))


# ── helpers ───────────────────────────────────────────────────────────────────

def _redirect_paths(tmp_path: Path) -> dict[str, Path]:
    """Point every engagement_hooks path at tmp_path; return mapping for restore."""
    import cli.engagement_hooks as eh
    saved = {
        "STATE_PATH": eh.STATE_PATH,
        "INDEX_PATH": eh.INDEX_PATH,
        "USERS_PATH": eh.USERS_PATH,
        "PAYLOAD_PATH": eh.PAYLOAD_PATH,
        "NOTIFICATIONS_PATH": eh.NOTIFICATIONS_PATH,
        "TASKS_PATH": eh.TASKS_PATH,
        "OBJECTIVES_PATH": eh.OBJECTIVES_PATH,
        "NOTES_PATH": eh.NOTES_PATH,
    }
    eh.STATE_PATH = tmp_path / "engagement_state.json"
    eh.INDEX_PATH = REPO / "cli" / "command_index.json"
    eh.USERS_PATH = tmp_path / "users.json"
    eh.PAYLOAD_PATH = tmp_path / "payload.json"
    eh.NOTIFICATIONS_PATH = tmp_path / "sessions" / "notifications.json"
    eh.TASKS_PATH = tmp_path / "sessions" / "tasks.json"
    eh.OBJECTIVES_PATH = tmp_path / "sessions" / "objectives.jsonl"
    eh.NOTES_PATH = tmp_path / "sessions" / "notes.jsonl"
    (tmp_path / "sessions").mkdir(exist_ok=True)
    eh._state = None
    eh._index = None
    return saved


def _restore_paths(saved: dict[str, Path]) -> None:
    import cli.engagement_hooks as eh
    for k, v in saved.items():
        setattr(eh, k, v)
    eh._state = None
    eh._index = None


# ── karma thresholds ──────────────────────────────────────────────────────────

class TestGetKarmaName:
    """Verify karma bracket boundaries mirror lazyc2.get_karma_name."""

    @pytest.mark.parametrize(
        "elo,expected",
        [
            (0, "Noob"),
            (999, "Noob"),
            (1000, "Rookie"),
            (1999, "Rookie"),
            (2000, "Skidy"),
            (2999, "Skidy"),
            (3000, "Hacker"),
            (3999, "Hacker"),
            (4000, "Pro"),
            (4999, "Pro"),
            (5000, "Elite"),
            (5999, "Elite"),
            (6000, "Godlike"),
            (12345, "Godlike"),
        ],
    )
    def test_thresholds(self, elo, expected):
        from cli.engagement_hooks import get_karma_name
        assert get_karma_name(elo) == expected


# ── ELO award math ────────────────────────────────────────────────────────────

class TestAwardElo:
    def test_base_only_for_unknown_command_and_phase(self):
        from cli.engagement_hooks import ELO_BASE, _award_elo
        assert _award_elo("totally_unknown_cmd", False, False, "") == ELO_BASE

    def test_high_value_bonus_applied(self):
        from cli.engagement_hooks import ELO_BASE, ELO_HIGH_VALUE_CMDS, _award_elo
        delta = _award_elo("secretsdump", False, False, "")
        assert delta == ELO_BASE + ELO_HIGH_VALUE_CMDS["secretsdump"]

    def test_phase_bonus_applied(self):
        from cli.engagement_hooks import ELO_BASE, ELO_PHASE_BONUS, _award_elo
        delta = _award_elo("unknown_cmd", False, False, "exploit")
        assert delta == ELO_BASE + ELO_PHASE_BONUS["exploit"]

    def test_first_time_bonus(self):
        from cli.engagement_hooks import ELO_BASE, ELO_FIRST_TIME_BONUS, _award_elo
        delta = _award_elo("unknown_cmd", True, False, "")
        assert delta == ELO_BASE + ELO_FIRST_TIME_BONUS

    def test_new_phase_bonus(self):
        from cli.engagement_hooks import ELO_BASE, ELO_NEW_PHASE_BONUS, _award_elo
        delta = _award_elo("unknown_cmd", False, True, "")
        assert delta == ELO_BASE + ELO_NEW_PHASE_BONUS

    def test_all_bonuses_stack(self):
        from cli.engagement_hooks import (
            ELO_BASE,
            ELO_FIRST_TIME_BONUS,
            ELO_HIGH_VALUE_CMDS,
            ELO_NEW_PHASE_BONUS,
            ELO_PHASE_BONUS,
            _award_elo,
        )
        delta = _award_elo("crackmapexec", True, True, "cred")
        expected = (
            ELO_BASE
            + ELO_HIGH_VALUE_CMDS["crackmapexec"]
            + ELO_PHASE_BONUS["cred"]
            + ELO_FIRST_TIME_BONUS
            + ELO_NEW_PHASE_BONUS
        )
        assert delta == expected

    def test_do_prefix_is_stripped(self):
        from cli.engagement_hooks import ELO_BASE, ELO_HIGH_VALUE_CMDS, _award_elo
        delta = _award_elo("do_lazynmap", False, False, "")
        assert delta == ELO_BASE + ELO_HIGH_VALUE_CMDS["lazynmap"]


# ── users.json sync ───────────────────────────────────────────────────────────

class TestSyncUserElo:
    def test_patches_matching_username(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "payload.json").write_text(json.dumps({"c2_user": "alice"}))
            users = [
                {"id": 1, "username": "alice", "password_hash": "h", "elo": 100},
                {"id": 2, "username": "bob",   "password_hash": "h", "elo": 200},
            ]
            (tmp_path / "users.json").write_text(json.dumps(users))
            from cli.engagement_hooks import _sync_user_elo
            assert _sync_user_elo(50) is True
            patched = json.loads((tmp_path / "users.json").read_text())
            assert patched[0]["elo"] == 150
            assert patched[1]["elo"] == 200, "non-target user must not be modified"
            assert patched[0]["password_hash"] == "h"
        finally:
            _restore_paths(saved)

    def test_silent_when_payload_missing(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "users.json").write_text(json.dumps([
                {"id": 1, "username": "alice", "password_hash": "h", "elo": 0}
            ]))
            from cli.engagement_hooks import _sync_user_elo
            assert _sync_user_elo(10) is False
        finally:
            _restore_paths(saved)

    def test_silent_when_username_not_found(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "payload.json").write_text(json.dumps({"c2_user": "ghost"}))
            (tmp_path / "users.json").write_text(json.dumps([
                {"id": 1, "username": "alice", "password_hash": "h", "elo": 0}
            ]))
            from cli.engagement_hooks import _sync_user_elo
            assert _sync_user_elo(10) is False
        finally:
            _restore_paths(saved)

    def test_ignores_non_positive_delta(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import _sync_user_elo
            assert _sync_user_elo(0) is False
            assert _sync_user_elo(-5) is False
        finally:
            _restore_paths(saved)

    def test_atomic_rename_leaves_no_tmp(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "payload.json").write_text(json.dumps({"c2_user": "alice"}))
            (tmp_path / "users.json").write_text(json.dumps([
                {"id": 1, "username": "alice", "password_hash": "h", "elo": 0}
            ]))
            from cli.engagement_hooks import _sync_user_elo
            _sync_user_elo(10)
            assert not (tmp_path / "users.tmp").exists()
        finally:
            _restore_paths(saved)


# ── notifications.json persistence ────────────────────────────────────────────

class TestPersistNotification:
    def test_creates_file_on_first_call(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import _persist_notification
            assert _persist_notification("<p>hi</p>") is True
            data = json.loads((tmp_path / "sessions" / "notifications.json").read_text())
            assert data == [{"html": "<p>hi</p>"}]
        finally:
            _restore_paths(saved)

    def test_appends_to_existing_file(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "sessions" / "notifications.json").write_text(
                json.dumps([{"html": "<p>old</p>"}])
            )
            from cli.engagement_hooks import _persist_notification
            _persist_notification("<p>new</p>")
            data = json.loads((tmp_path / "sessions" / "notifications.json").read_text())
            assert len(data) == 2
            assert data[1]["html"] == "<p>new</p>"
        finally:
            _restore_paths(saved)

    def test_ring_cap_drops_oldest(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            import cli.engagement_hooks as eh
            eh._NOTIFICATIONS_RING_SIZE = 3
            from cli.engagement_hooks import _persist_notification
            for i in range(5):
                _persist_notification(f"<p>{i}</p>")
            data = json.loads((tmp_path / "sessions" / "notifications.json").read_text())
            assert len(data) == 3
            assert data[0]["html"] == "<p>2</p>"
            assert data[-1]["html"] == "<p>4</p>"
        finally:
            import cli.engagement_hooks as eh
            eh._NOTIFICATIONS_RING_SIZE = 500
            _restore_paths(saved)

    def test_recovers_from_corrupt_file(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "sessions" / "notifications.json").write_text("{ not json")
            from cli.engagement_hooks import _persist_notification
            assert _persist_notification("<p>x</p>") is True
            data = json.loads((tmp_path / "sessions" / "notifications.json").read_text())
            assert data == [{"html": "<p>x</p>"}]
        finally:
            _restore_paths(saved)


# ── methodology rewards ───────────────────────────────────────────────────────

class TestMethodologyRewards:
    def test_task_reward_silent_when_no_file(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import _render_methodology_task
            assert _render_methodology_task({"current_phase": "recon"}) is False
            assert capsys.readouterr().out == ""
        finally:
            _restore_paths(saved)

    def test_task_reward_renders_pending_match(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "sessions" / "tasks.json").write_text(json.dumps([
                {"id": 0, "title": "Done one", "status": "Done"},
                {"id": 1, "title": "Recon 10.0.0.1 — map ports", "status": "Pending"},
            ]))
            from cli.engagement_hooks import _render_methodology_task
            assert _render_methodology_task({"current_phase": "recon"}) is True
            out = capsys.readouterr().out
            assert "open task" in out
            assert "Recon 10.0.0.1" in out
        finally:
            _restore_paths(saved)

    def test_task_reward_silent_when_all_done(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "sessions" / "tasks.json").write_text(json.dumps([
                {"id": 0, "title": "X", "status": "Done"},
                {"id": 1, "title": "Y", "status": "completed"},
            ]))
            from cli.engagement_hooks import _render_methodology_task
            assert _render_methodology_task({"current_phase": "enum"}) is False
        finally:
            _restore_paths(saved)

    def test_objective_reward_uses_phase_to_next_cmd(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            lines = [
                json.dumps({"id": "a", "text": "Run kerbrute", "status": "pending",
                            "context": {"phase": "cred"}}),
                json.dumps({"id": "b", "text": "Done one", "status": "done"}),
            ]
            (tmp_path / "sessions" / "objectives.jsonl").write_text("\n".join(lines))
            from cli.engagement_hooks import _render_methodology_objective
            assert _render_methodology_objective({}) is True
            out = capsys.readouterr().out
            assert "objective" in out
            assert "crackmapexec" in out

        finally:
            _restore_paths(saved)

    def test_objective_reward_silent_when_no_pending(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "sessions" / "objectives.jsonl").write_text(
                json.dumps({"id": "a", "text": "x", "status": "done"})
            )
            from cli.engagement_hooks import _render_methodology_objective
            assert _render_methodology_objective({}) is False
        finally:
            _restore_paths(saved)

    def test_note_reward_renders_latest(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "sessions" / "notes.jsonl").write_text("\n".join([
                json.dumps({"ts": 1, "text": "older", "phase": "recon"}),
                json.dumps({"ts": 2, "text": "smb open on 445", "phase": "enum"}),
            ]))
            from cli.engagement_hooks import _render_methodology_note
            assert _render_methodology_note({}) is True
            out = capsys.readouterr().out
            assert "recall note" in out
            assert "smb open on 445" in out
            assert "enum4linux" in out
        finally:
            _restore_paths(saved)

    def test_note_reward_silent_when_empty(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import _render_methodology_note
            assert _render_methodology_note({}) is False
        finally:
            _restore_paths(saved)


# ── karma_up promotion ────────────────────────────────────────────────────────

class TestKarmaUp:
    def test_fires_on_threshold_crossing(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import EngagementState, _check_karma_up
            state = EngagementState(elo=1500, last_karma_name="Noob")
            assert _check_karma_up(state) is True
            assert state.last_karma_name == "Rookie"
            out = capsys.readouterr().out
            assert "KARMA UP" in out
            assert "Noob" in out and "Rookie" in out
        finally:
            _restore_paths(saved)

    def test_idempotent_when_no_threshold_cross(self, capsys):
        from cli.engagement_hooks import EngagementState, _check_karma_up
        state = EngagementState(elo=500, last_karma_name="Noob")
        assert _check_karma_up(state) is False
        assert capsys.readouterr().out == ""

    def test_persists_notification(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import EngagementState, _check_karma_up
            state = EngagementState(elo=3000, last_karma_name="Rookie")
            _check_karma_up(state)
            data = json.loads((tmp_path / "sessions" / "notifications.json").read_text())
            assert any("KARMA UP" in str(e).upper() or "Karma Up" in e.get("html", "")
                       for e in data)
        finally:
            _restore_paths(saved)


# ── render_engagement_hook integration ────────────────────────────────────────

class TestRenderEngagementHookIntegration:
    def test_elo_accumulates_across_commands(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import get_state_snapshot, render_engagement_hook
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=True)
            render_engagement_hook(cmd="enum4linux", phase="enum", enabled=True)
            snap = get_state_snapshot()
            assert snap["elo"] > 0
            assert snap["total_commands"] == 2
            assert "do_lazynmap" in snap["commands_seen"]
            assert "do_enum4linux" in snap["commands_seen"]
        finally:
            _restore_paths(saved)

    def test_first_time_bonus_only_once_per_command(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import get_state_snapshot, render_engagement_hook
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=True)
            first_elo = get_state_snapshot()["elo"]
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=True)
            second_elo = get_state_snapshot()["elo"]
            second_delta = second_elo - first_elo
            assert second_delta < first_elo, (
                "running the same command twice must NOT grant first-time bonus again"
            )
        finally:
            _restore_paths(saved)

    def test_users_json_syncd_when_payload_present(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            (tmp_path / "payload.json").write_text(json.dumps({"c2_user": "alice"}))
            (tmp_path / "users.json").write_text(json.dumps([
                {"id": 1, "username": "alice", "password_hash": "h", "elo": 0}
            ]))
            from cli.engagement_hooks import render_engagement_hook
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=True)
            patched = json.loads((tmp_path / "users.json").read_text())
            assert patched[0]["elo"] > 0
        finally:
            _restore_paths(saved)

    def test_disabled_flag_is_noop(self, tmp_path, capsys):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import get_state_snapshot, render_engagement_hook
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=False)
            snap = get_state_snapshot()
            assert snap["total_commands"] == 0
            assert capsys.readouterr().out == ""
        finally:
            _restore_paths(saved)


# ── get_state_snapshot ────────────────────────────────────────────────────────

class TestStateSnapshot:
    def test_returns_required_keys(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import get_state_snapshot
            snap = get_state_snapshot()
            for key in (
                "elo", "karma_name", "commands_seen", "phases_entered",
                "total_commands", "session_commands", "elo_session_delta",
                "next_reward_at",
            ):
                assert key in snap, f"missing key {key} in snapshot"
            assert snap["karma_name"] == "Noob"
            assert snap["elo"] == 0
        finally:
            _restore_paths(saved)
