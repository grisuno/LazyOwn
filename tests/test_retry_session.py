"""BDD tests for retry sessions, support relaunch and the retry command set."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from modules.chain_registry import Chain, ChainStep
from modules.chain_runner import ChainRunner
from modules.chain_state import write_checkpoint
from modules.retry_session import (
    SUDO_WARNING,
    apply_sudo_askpass,
    clear_sudo_secret,
    is_active,
    set_sudo_secret,
    sudo_gate_open,
)


@pytest.fixture(autouse=True)
def clean_session(monkeypatch, tmp_path):
    """No elevation leaks between tests; secret dir is test-local."""
    for env_key in ("SUDO_ASKPASS", "LAZYOWN_RETRY_SUDO"):
        monkeypatch.delenv(env_key, raising=False)
    monkeypatch.setattr("modules.retry_session.SESSION_DIR", tmp_path / "sessions" / "retry")
    clear_sudo_secret()
    yield
    clear_sudo_secret()


@pytest.fixture
def checkpoint(tmp_path, monkeypatch) -> dict:
    """One aborted checkpoint for a known chain name with one failed step."""
    monkeypatch.setattr("modules.chain_state.checkpoint_dir", lambda base=None: tmp_path / "chains")
    state = {
        "run_id": "apt_chain_20261020_150000_909",
        "chain": "apt_chain",
        "target": "10.0.0.9",
        "state": "aborted",
        "ok": False,
        "aborted": True,
        "reason": "exp_sweep: failed",
        "variables": {"target": "10.0.0.9", "playbook": "rocke"},
        "steps": [
            {"id": "scope", "status": "ok", "reason": ""},
            {"id": "scan", "status": "skipped", "reason": "exists"},
        ],
        "next_index": 2,
    }
    write_checkpoint(tmp_path / "chains", state)
    return state


class TestElevatedSession:
    """The sudo secret is session-scoped and never in argv."""

    def test_arm_and_gate(self):
        """Given a password, Then the gate opens and askpass gets it."""
        set_sudo_secret("hop-s3cret")
        assert is_active(), "session marker set"
        assert sudo_gate_open(), "gate open for arming"
        helper = Path(os.environ["SUDO_ASKPASS"])
        assert helper.is_file(), "askpass helper exists"
        assert helper.stat().st_mode & 0o777 == 0o700, "helper 0700"
        secret_file = helper.parent / "sudo.secret"
        assert secret_file.stat().st_mode & 0o777 == 0o600, "secret 0600"
        assert "hop-s3cret" not in helper.read_text(), "secret never lands in the helper"

    def test_clear_revokes(self):
        """Given an armed session, clearing, Then gate closes and files die."""
        set_sudo_secret("hop-s3cret")
        clear_sudo_secret()
        assert not is_active()
        assert not sudo_gate_open()
        assert not Path(os.environ.get("SUDO_ASKPASS", "/")).is_file()

    def test_empty_secret_refused(self):
        """Given an empty password, Then ValueError fails closed."""
        with pytest.raises(ValueError):
            set_sudo_secret("   ")

    def test_apply_sudo_askpass_rewrite(self):
        """Given armed session, Then segment-leading sudo gets -A."""
        set_sudo_secret("hop-s3cret")
        assert (
            apply_sudo_askpass("sudo nmap -sS 10.0.0.1; sudo -n true") == "sudo -A nmap -sS 10.0.0.1; sudo -A -n true"
        )
        assert apply_sudo_askpass("echo sudo stays intact") == "echo sudo stays intact"
        assert apply_sudo_askpass("FOO=1 sudo scan") == "FOO=1 sudo -A scan"
        assert apply_sudo_askpass("lazynmap 10.0.0.1") == "lazynmap 10.0.0.1"


class TestConsent:
    """Elevation is opt-in, warned and fail-closed."""

    def test_no_flag_no_consent(self):
        """Given no --sudo, Then no arming, no nag."""
        from cli.retry_support import consent_to_elevate

        armed, note = consent_to_elevate([], lambda _w: "YES")
        assert not armed and note == "", "silent when not requested"

    def test_no_tty_refuses(self):
        """Given --sudo without prompt, Then refused with a note."""
        from cli.retry_support import consent_to_elevate

        armed, note = consent_to_elevate(["--sudo"], None)
        assert not armed and "refused" in note

    def test_wrong_answer_refuses(self):
        """Given --sudo and a non-YES answer, Then refused."""
        from cli.retry_support import consent_to_elevate

        armed, note = consent_to_elevate(["--sudo"], lambda _w: "y")
        assert not armed and "aborted" in note

    def test_warning_mentions_destructive_steps(self):
        """The consent text must say why elevation is dangerous."""
        text = SUDO_WARNING.lower()
        assert "destructive" in text and "root" in text, "consequence spelled out"


class TestCheckpointSelectionRun:
    """Chain relaunch picks the stored checkpoint and keeps the run id."""

    def test_chain_filter_selection(self, tmp_path):
        """Given two failed checkpoints, Then the chain filter wins."""
        from modules.retry_session import newest_failed_checkpoint

        directory = tmp_path / "chains"
        write_checkpoint(
            directory,
            {
                "run_id": "alpha_20261020_100000_1",
                "chain": "alpha",
                "state": "aborted",
                "ok": False,
                "next_index": 1,
            },
        )
        write_checkpoint(
            directory,
            {
                "run_id": "bravo_20261020_090000_2",
                "chain": "bravo",
                "state": "aborted",
                "ok": False,
                "next_index": 3,
            },
        )
        monkey = pytest.MonkeyPatch()
        monkey.setattr("modules.chain_state.checkpoint_dir", lambda base=None: directory)
        try:
            state = newest_failed_checkpoint(chain="bravo")
            assert state["run_id"] == "bravo_20261020_090000_2", "chain filter honored"
            state = newest_failed_checkpoint(run_id="alpha_20261020_100000_1")
            assert state["chain"] == "alpha", "explicit run id wins"
        finally:
            monkey.undo()

    def test_retry_chain_resume_respects_completed_steps(self, checkpoint, monkeypatch):
        """Given a varied config, Then the relaunch skips done steps."""
        from cli.retry_support import retry_chain

        monkeypatch.setattr(
            "cli.retry_support.get_chain",
            lambda name, chains_dir=None: Chain(
                name=name,
                steps=[
                    ChainStep(id="scope", run="assign target {target}"),
                    ChainStep(id="scan", run="lazynmap {target}"),
                    ChainStep(id="attack", run="atomic_exploit --target {target} --port {port}"),
                ],
            ),
        )
        report = retry_chain("apt_chain", shell=None, extra_vars={"target": "172.17.0.5", "port": "9999"}, dry_run=True)
        assert report.error == "", f"resume must validate: {report.error}"
        assert report.run_id == checkpoint["run_id"], "same run id keeps the audit trail"
        assert report.variables["target"] == "172.17.0.5", "user-varied config wins"
        assert report.variables["port"] == "9999"
        resumed = [s for s in report.skipped if "already completed" in s]
        assert len(resumed) >= 2, "completed work stays skipped, never re-executed"

    def test_retry_chain_disabled_chain_hint(self, checkpoint, monkeypatch):
        """Given a recorded chain that is disabled, Then the hint enables it."""
        from cli.retry_support import retry_chain

        monkeypatch.setattr("cli.retry_support.get_chain", lambda name, chains_dir=None: None)

        def fake_scan(chains_dir=None):
            return [{"name": "apt_chain", "enabled": False, "valid": True}]

        monkeypatch.setattr("modules.chain_registry.scan_all", fake_scan)
        report = retry_chain("apt_chain", dry_run=True)
        assert "disabled" in report.error and "apt_chain enable apt_chain" in report.error


class TestRunnerCommandFilter:
    """Command filters hook into both verb and raw execution paths."""

    def test_filter_applies(self):
        """Given a filter, Then every executed command is transformed."""
        seen: list[str] = []

        def capture(command: str) -> str:
            seen.append(command)
            return command

        chain = Chain(
            name="filterdemo", steps=[ChainStep(id="s1", run="assign target x"), ChainStep(id="s2", run="echo 1")]
        )
        result = ChainRunner(chain, executor=lambda cmd: "ok", command_filter=capture).run()
        assert result.steps[-1].status == "ok"
        assert seen == ["assign target x", "echo 1"], "filter sees both lines"


class TestUtilsGate:
    """``utils.sudo_available`` honors the armed retry session."""

    def test_retry_gate_overrides_cached_probe(self, monkeypatch):
        """Given an armed retry session, Then the sudo gate opens."""
        import utils

        monkeypatch.setattr(utils, "_SUDO_STATE", {"checked": False, "ok": False})
        for env_key in ("SUDO_ASKPASS", "LAZYOWN_RETRY_SUDO"):
            monkeypatch.delenv(env_key, raising=False)
        assert utils._retry_sudo_gate() is False, "nothing armed"
        set_sudo_secret("hop")
        assert utils.sudo_available() is True, "askpass gate answers True"
        helper = os.environ["SUDO_ASKPASS"]
        os.unlink(helper)
        assert utils.sudo_available() is False, "stale env without disk backing closes"


class TestRetryStatus:
    """The status view aggregates checkpoint and task failures."""

    def test_snapshot_digs_past_finished_rows(self, checkpoint, tmp_path):
        """Given a pile of finished runs, Then the newest failure surfaces."""
        from cli.retry_support import status_snapshot

        for index in range(40):
            write_checkpoint(
                tmp_path / "chains",
                {
                    "run_id": f"done_chain_20261020_16000{index:02d}_1",
                    "chain": "done_chain",
                    "state": "finished",
                    "ok": True,
                    "next_index": 1,
                },
            )
        snapshot = status_snapshot(limit=2)
        assert snapshot["checkpoint_rows"], "buried failure is not missed"
        assert snapshot["checkpoint_rows"][0]["chain"] == "apt_chain"

    def test_snapshot_shape(self, checkpoint):
        """Given a stored failure, Then the snapshot exposes it."""
        from cli.retry_support import last_loop_task, status_snapshot

        snapshot = status_snapshot(limit=3)
        assert snapshot["checkpoint_rows"], "failed checkpoint listed"
        assert snapshot["checkpoint_rows"][0]["chain"] == "apt_chain"
        assert not snapshot["sudo_armed"]
        task = last_loop_task()
        assert hasattr(task, "known")
