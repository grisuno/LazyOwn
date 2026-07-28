"""Tests for the command-recording gate of cli/engagement_hooks.py.

The engagement telemetry must count only real LazyOwn commands. Before this
gate every first token of an input line was recorded, so menu selections
(``1``), quoted script paths, mistyped emails, host names and free-form
natural language leaked into ``commands_seen`` and inflated the ELO ledger.

Two layers enforce the contract:

  * A module-level syntactic filter (:func:`_is_recordable_command`) that
    rejects anything that is not shaped like a command name. It deliberately
    does not consult the static command index, which can lag the live shell.
  * An authoritative roster purge (:func:`heal_commands_seen` /
    :func:`_sanitize_seen` with a ``known`` set) driven at shell startup by
    the live ``get_all_commands()`` registry, which removes real-looking but
    invalid tokens such as ``do_against``.

Every module-level path is redirected to a tmp directory so the real
``sessions/`` state file is never touched.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
sys.path.insert(0, str(REPO))


def _redirect_paths(tmp_path: Path) -> dict[str, Path]:
    """Point engagement_hooks state at tmp_path but keep the real index."""
    import cli.engagement_hooks as eh

    saved = {
        "STATE_PATH": eh.STATE_PATH,
        "INDEX_PATH": eh.INDEX_PATH,
        "USERS_PATH": eh.USERS_PATH,
        "PAYLOAD_PATH": eh.PAYLOAD_PATH,
        "NOTIFICATIONS_PATH": eh.NOTIFICATIONS_PATH,
    }
    eh.STATE_PATH = tmp_path / "engagement_state.json"
    eh.INDEX_PATH = REPO / "cli" / "command_index.json"
    eh.USERS_PATH = tmp_path / "users.json"
    eh.PAYLOAD_PATH = tmp_path / "payload.json"
    eh.NOTIFICATIONS_PATH = tmp_path / "sessions" / "notifications.json"
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


# ── _is_recordable_command (syntactic layer) ────────────────────────────────────

class TestIsRecordableCommand:
    """The syntactic gate that rejects input-line noise."""

    @pytest.mark.parametrize("cmd", ["lazynmap", "gobuster", "do_ffuf", "enum4linux", "vulns", "sudo"])
    def test_accepts_command_shaped_tokens(self, cmd):
        import cli.engagement_hooks as eh

        assert eh._is_recordable_command(cmd) is True

    @pytest.mark.parametrize(
        "cmd",
        ["1", "5", "./DEPLOY.sh", "grisuno@gmail.com", "CVE-2026", "VariaType.htb",
         "", "127.0.0.1", "no-priv", "Full"],
    )
    def test_rejects_syntactic_garbage(self, cmd):
        import cli.engagement_hooks as eh

        assert eh._is_recordable_command(cmd) is False

    def test_quoted_path_rejected(self):
        import cli.engagement_hooks as eh

        assert eh._is_recordable_command('"/home/grisun0/LazyOwn/lazyscripts/startup.ls"') is False

    def test_do_prefixed_input_is_accepted(self):
        import cli.engagement_hooks as eh

        assert eh._is_recordable_command("do_lazynmap") is True

    def test_normalize_is_idempotent(self):
        import cli.engagement_hooks as eh

        assert eh._normalize_command("lazynmap") == "do_lazynmap"
        assert eh._normalize_command("do_lazynmap") == "do_lazynmap"


# ── render_engagement_hook rejects syntactic noise ──────────────────────────────

class TestHookRejectsNoise:
    """A non-command-shaped token must not touch commands_seen or the ELO."""

    def test_garbage_does_not_enter_commands_seen(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import get_state_snapshot, render_engagement_hook

            for token in ["1", "./DEPLOY.sh", "grisuno@gmail.com", "CVE-2026", "127.0.0.1"]:
                render_engagement_hook(cmd=token, phase="recon", enabled=True)
            snap = get_state_snapshot()
            assert snap["commands_seen"] == []
            assert snap["elo"] == 0
            assert snap["total_commands"] == 0
        finally:
            _restore_paths(saved)

    def test_real_command_recorded_between_garbage(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            from cli.engagement_hooks import get_state_snapshot, render_engagement_hook

            render_engagement_hook(cmd="1", phase="recon", enabled=True)
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=True)
            render_engagement_hook(cmd="grisuno@gmail.com", phase="recon", enabled=True)
            snap = get_state_snapshot()
            assert snap["commands_seen"] == ["do_lazynmap"]
            assert snap["total_commands"] == 1
        finally:
            _restore_paths(saved)


# ── _sanitize_seen and _load_state healing ──────────────────────────────────────

class TestSanitizeSeen:
    """Historical pollution is healed on load and against a roster."""

    def test_syntactic_only_drops_ugly_garbage(self):
        import cli.engagement_hooks as eh

        dirty = ["do_lazynmap", "do_1", "do_./DEPLOY.sh", "do_grisuno@gmail.com",
                 "do_gobuster", "do_lazynmap", "do_CVE-2026"]
        assert eh._sanitize_seen(dirty) == ["do_lazynmap", "do_gobuster"]

    def test_roster_drops_valid_but_unknown_tokens(self):
        import cli.engagement_hooks as eh

        dirty = ["do_lazynmap", "do_against", "do_gobuster", "do_como", "do_git"]
        known = {"do_lazynmap", "do_gobuster", "do_sudo"}
        assert eh._sanitize_seen(dirty, known) == ["do_lazynmap", "do_gobuster"]

    def test_load_state_heals_polluted_file(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            import cli.engagement_hooks as eh

            polluted = {
                "total_commands": 99,
                "commands_seen": ["do_lazynmap", "do_1", 'do_"/x/y.ls"', "do_ffuf", "do_ffuf"],
                "elo": 500,
            }
            eh.STATE_PATH.write_text(json.dumps(polluted), encoding="utf-8")
            eh._state = None
            state = eh._load_state()
            assert state.commands_seen == ["do_lazynmap", "do_ffuf"]
            assert state.elo == 500
        finally:
            _restore_paths(saved)


# ── heal_commands_seen (authoritative purge) ────────────────────────────────────

class TestHealCommandsSeen:
    """The startup purge removes non-command entries against the live roster."""

    def test_purges_and_persists(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            import cli.engagement_hooks as eh

            eh.STATE_PATH.write_text(
                json.dumps({"commands_seen": ["do_lazynmap", "do_against", "do_como", "do_gobuster"]}),
                encoding="utf-8",
            )
            eh._state = None
            removed = eh.heal_commands_seen({"do_lazynmap", "do_gobuster", "do_sudo"})
            assert removed == 2
            on_disk = json.loads(eh.STATE_PATH.read_text(encoding="utf-8"))
            assert on_disk["commands_seen"] == ["do_lazynmap", "do_gobuster"]
        finally:
            _restore_paths(saved)

    def test_idempotent_on_clean_state(self, tmp_path):
        saved = _redirect_paths(tmp_path)
        try:
            import cli.engagement_hooks as eh

            eh.STATE_PATH.write_text(
                json.dumps({"commands_seen": ["do_lazynmap", "do_gobuster"]}),
                encoding="utf-8",
            )
            eh._state = None
            assert eh.heal_commands_seen({"do_lazynmap", "do_gobuster"}) == 0
        finally:
            _restore_paths(saved)
