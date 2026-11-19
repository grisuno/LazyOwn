"""Tests for the foothold-to-beacon handoff and OS-aware beacon loop.

Covers:
    - :mod:`modules.lazy_handoff` gating, dedupe and worker start.
    - :mod:`modules.beacon_loop` OS-aware platform resolution from
      ``sessions/os.json`` (written by the ``ping`` command) and the
      progressive playbook ladder (awareness -> discovery -> privesc ->
      exfil, persistence goal-gated).
    - ``atomic_cli.default_platform_for_target`` os_id mapping.
"""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from modules import lazy_handoff
from modules.atomic_cli import default_platform_for_target
from modules.beacon_loop import (
    PRIVESC_COMMAND,
    BeaconLoopConfig,
    _platform_from_os_json,
    _wire_command,
    heuristic_plan,
    playbook_ladder,
    run_beacon_loop,
)


class TestHandoffGate:
    def test_disabled_under_pytest(self, monkeypatch):
        monkeypatch.setenv("PYTEST_CURRENT_TEST", "1")
        assert lazy_handoff.handoff_enabled({"loop_beacon_handoff": True}) is False

    def test_env_kill_switch(self, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setenv(lazy_handoff.HANDOFF_ENV, "0")
        assert lazy_handoff.handoff_enabled({"loop_beacon_handoff": True}) is False

    def test_flag_off(self, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        assert lazy_handoff.handoff_enabled({"loop_beacon_handoff": False}) is False

    def test_flag_on(self, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.delenv(lazy_handoff.HANDOFF_ENV, raising=False)
        assert lazy_handoff.handoff_enabled({"loop_beacon_handoff": True}) is True


class TestHandoffStart:
    def _enable(self, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setenv(lazy_handoff.HANDOFF_ENV, "1")
        monkeypatch.setattr(
            "core.config.load_payload", lambda *a, **kw: {"loop_beacon_handoff": True}
        )

    def test_starts_once_per_host(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        spawns = []
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawns.append(a))
        assert lazy_handoff.maybe_beacon_handoff("10.0.0.5", sessions_dir=tmp_path) is True
        assert lazy_handoff.maybe_beacon_handoff("10.0.0.5", sessions_dir=tmp_path) is False
        assert len(spawns) == 1
        assert lazy_handoff.already_handed_off("10.0.0.5", sessions_dir=tmp_path)

    def test_failed_marker_allows_retry(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        spawns = []
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawns.append(a))
        lazy_handoff.maybe_beacon_handoff("10.0.0.7", sessions_dir=tmp_path)
        lazy_handoff._mark_status("10.0.0.7", tmp_path, "failed")
        assert not lazy_handoff.already_handed_off("10.0.0.7", sessions_dir=tmp_path)
        assert lazy_handoff.maybe_beacon_handoff("10.0.0.7", sessions_dir=tmp_path) is True
        assert len(spawns) == 2

    def test_deployed_marker_rearms_when_beacon_is_dead(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        marker = lazy_handoff._marker_path("10.0.0.8", tmp_path)
        marker.write_text(
            json.dumps(
                {
                    "target": "10.0.0.8",
                    "status": "deployed",
                    "updated_at": "2020-01-01T00:00:00+00:00",
                }
            ),
            encoding="utf-8",
        )
        monkeypatch.setattr(lazy_handoff, "_beacon_is_live", lambda host, sessions: False)
        spawns = []
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawns.append(a))
        assert lazy_handoff.maybe_beacon_handoff("10.0.0.8", sessions_dir=tmp_path) is True
        assert len(spawns) == 1

    def test_live_beacon_keeps_deployed_marker(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        marker = lazy_handoff._marker_path("10.0.0.9", tmp_path)
        marker.write_text(
            json.dumps(
                {
                    "target": "10.0.0.9",
                    "status": "deployed",
                    "updated_at": "2020-01-01T00:00:00+00:00",
                }
            ),
            encoding="utf-8",
        )
        monkeypatch.setattr(lazy_handoff, "_beacon_is_live", lambda host, sessions: True)
        spawns = []
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawns.append(a))
        assert lazy_handoff.maybe_beacon_handoff("10.0.0.9", sessions_dir=tmp_path) is False
        assert spawns == []

    def test_task_id_reaches_worker_and_marker(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        spawns = []
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawns.append(a))
        assert lazy_handoff.maybe_beacon_handoff(
            "10.0.0.11", sessions_dir=tmp_path, task_id="t0011"
        ) is True
        argv = spawns[0][0]
        assert "--task-id" in argv
        assert argv[-1] == "t0011"
        state = json.loads(lazy_handoff._marker_path("10.0.0.11", tmp_path).read_text(encoding="utf-8"))
        assert state["task_id"] == "t0011"

    def test_windows_target_skipped(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        monkeypatch.setattr(
            "modules.lazy_osinfer.host_os_for_target", lambda target: "windows"
        )
        spawns = []
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawns.append(a))
        assert lazy_handoff.maybe_beacon_handoff("10.0.0.6", sessions_dir=tmp_path) is False
        assert spawns == []

    def test_noop_without_target(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        assert lazy_handoff.maybe_beacon_handoff("", sessions_dir=tmp_path) is False


class TestOsInference:
    def test_samba_banner_does_not_win_over_linux_markers(self):
        from modules.lazy_osinfer import infer_from_banner

        text = "139/tcp open netbios-ssn Samba smbd 3.X 445/tcp open netbios-ssn Linux"
        assert infer_from_banner(text)["os"] == "linux"

    def test_explicit_windows_still_wins(self):
        from modules.lazy_osinfer import infer_from_banner

        assert infer_from_banner("microsoft-ds Windows Server 2019 netbios-ssn")["os"] == "windows"

    def test_generic_smb_only_falls_back_to_windows(self):
        from modules.lazy_osinfer import infer_from_banner

        assert infer_from_banner("microsoft-ds smb netbios-ssn")["os"] == "windows"


class TestOsJsonPlatform:
    def test_list_schema(self, tmp_path):
        (tmp_path / "os.json").write_text(
            json.dumps([{"id": "1", "os": "Linux", "ttl": 64, "state": "active"}]),
            encoding="utf-8",
        )
        assert _platform_from_os_json(tmp_path) == "linux"

    def test_windows(self, tmp_path):
        (tmp_path / "os.json").write_text(
            json.dumps([{"id": "2", "os": "Windows", "ttl": 128, "state": "active"}]),
            encoding="utf-8",
        )
        assert _platform_from_os_json(tmp_path) == "windows"

    def test_missing(self, tmp_path):
        assert _platform_from_os_json(tmp_path) == ""


class TestPlaybookLadder:
    def test_linux_full_ladder(self):
        ladder = playbook_ladder("privesc and exfil", "linux")
        phases = [phase for phase, _ in ladder]
        assert phases == ["awareness", "discovery", "privesc", "exfil"]
        commands = dict(ladder)
        assert "escalatelin:" in commands["privesc"]
        assert commands["exfil"] == ["exfil:/etc/passwd", "exfil:/etc/shadow"]
        assert "persist:" not in [c for cmds in commands.values() for c in cmds]

    def test_persistence_goal_gated(self):
        ladder = dict(playbook_ladder("persist on reboot and exfil data", "windows"))
        assert "persist:" in ladder["persistence"]
        assert ladder["exfil"] == ["exfil:%USERPROFILE%\\Desktop"]

    def test_no_exfil_without_goal(self):
        ladder = playbook_ladder("just look around", "linux")
        assert [phase for phase, _ in ladder] == ["awareness", "discovery", "privesc"]


class TestHeuristicPlan:
    def test_ladder_progression(self, tmp_path):
        goal = "privilege escalation, situational awareness and exfiltration"
        first = heuristic_plan(goal, "linux", [], sessions_dir=tmp_path)
        assert first == ["id", "netconfig:", PRIVESC_COMMAND, "exfil:/etc/passwd"]
        seen = [{"command": c, "output": "ok"} for c in
                ["id", "uname -a", "hostname", "pwd", "ls -la /etc", "cat /etc/passwd",
                 "netconfig:", "softenum:", "discover:", "portscan:", PRIVESC_COMMAND,
                 "exfil:/etc/passwd"]]
        second = heuristic_plan(goal, "linux", seen, sessions_dir=tmp_path)
        assert second == ["exfil:/etc/shadow"]
        seen.append({"command": "exfil:/etc/shadow", "output": "ok"})
        third = heuristic_plan(goal, "linux", seen, sessions_dir=tmp_path)
        assert third == []

    def test_os_json_fallback(self, tmp_path):
        (tmp_path / "os.json").write_text(
            json.dumps([{"os": "Linux", "state": "active"}]), encoding="utf-8"
        )
        plan = heuristic_plan("exfil", "other", [], sessions_dir=tmp_path)
        assert plan[:1] == ["id"]
        assert "escalatelin:" in plan


class TestRunBeaconLoopSessionsDir:
    def _history(self, sessions: Path, client: str, rows):
        sessions.mkdir(parents=True, exist_ok=True)
        (sessions / f"{client}.records.jsonl").write_text(
            "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8"
        )

    def test_loop_uses_sessions_dir_history(self, tmp_path):
        client = "handoff_beacon"
        self._history(tmp_path / "sessions", client, [{"client": "linux", "command": "id", "output": "uid=0"}])
        queued = []

        def fake_queue(client_id, command, sessions_dir=None):
            queued.append(command)
            return True

        import modules.beacon_loop as bl

        monkey = pytest.MonkeyPatch()
        monkey.setattr(bl, "queue_beacon_command", fake_queue)
        try:
            report = run_beacon_loop(
                BeaconLoopConfig(client_id=client, goal="exfil data", rounds=3, llm_enabled=False),
                log=lambda msg: None,
                sleep=lambda seconds: None,
                sessions_dir=tmp_path / "sessions",
            )
        finally:
            monkey.undo()
        assert report.records_seen == 1
        assert queued and queued[0] == "uname -a"

    def test_exfil_record_advances_killchain(self, tmp_path, monkeypatch):
        client = "exfil_beacon"
        self._history(
            tmp_path / "sessions",
            client,
            [
                {
                    "client": client,
                    "command": "cat /etc/passwd",
                    "output": "root:x:0:0",
                    "ips": "172.17.0.2",
                }
            ],
        )
        calls = []
        from modules.killchain import KillChain

        def fake_advance(new_phase, world_model_path=None, host=None, extras=None):
            calls.append((new_phase, world_model_path, host))
            return True

        monkeypatch.setattr(KillChain, "advance_phase", staticmethod(fake_advance))
        import modules.beacon_loop as bl

        monkeypatch.setattr(
            bl,
            "queue_beacon_command",
            lambda client_id, command, sessions_dir=None: False,
        )
        report = run_beacon_loop(
            BeaconLoopConfig(client_id=client, goal="exfil data", rounds=1, llm_enabled=False),
            log=lambda msg: None,
            sleep=lambda seconds: None,
            sessions_dir=tmp_path / "sessions",
        )
        assert (
            "exfil",
            tmp_path / "sessions" / "world_model.json",
            "172.17.0.2",
        ) in calls
        assert any("killchain advanced to exfil" in note for note in report.notes)

    def test_exfil_capability_uses_beacon_wire_command(self):
        assert _wire_command("exfil:/etc/passwd") == "cat /etc/passwd"
        assert _wire_command("id") == "id"


class TestShellNotification:
    def test_shell_proof_emits_loop_notification(self, monkeypatch):
        from types import SimpleNamespace

        import modules.atomic_exploit_bridge as bridge
        import modules.lazy_loop as loop
        import modules.outcome_bus as bus

        monkeypatch.setattr(bridge, "shell_output_evidence", lambda text: bool(text))
        events = []
        monkeypatch.setattr(bus, "record_event", lambda **kwargs: events.append(kwargs) or "event")
        emitted = []

        class FakeActivity:
            def __init__(self, task_id):
                self.task_id = task_id

            def emit(self, worker, kind, text, intent_id=0, tool_use_id=""):
                emitted.append((worker, kind, text, intent_id))

        monkeypatch.setattr(loop, "ActivityLog", FakeActivity)
        worker = loop.Worker.__new__(loop.Worker)
        worker.name = "worker-1"
        worker.task_id = "t0011"
        intent = SimpleNamespace(node_id=9)
        assert worker._publish_shell_proof(intent, "172.17.0.2", "id", "uid=0(root)") is True
        assert len(events) == 1
        assert emitted and emitted[0][1] == "shell"
        assert "172.17.0.2" in emitted[0][2]


class TestDefaultPlatform:
    def test_os_id_linux(self):
        assert default_platform_for_target({"os_id": "1"}) == "linux"

    def test_os_id_windows(self):
        assert default_platform_for_target({"os_id": "2"}) == "windows"

    def test_unknown(self):
        assert default_platform_for_target({}) == ""


class TestHookPlatformFilter:
    """Windows hooks never queue on Linux beacons and vice versa."""

    def _engine(self):
        from modules.conditional_hooks import HookEngine

        return HookEngine()

    def test_windows_only_blocked_on_linux(self):
        engine = self._engine()
        for command in ("whoami /priv", "net user", "wmic process list", "dir %USERPROFILE%"):
            assert engine._platform_compatible(
                {"type": "run_command", "command": command}, {"platform": "linux"}
            ) is False, command

    def test_linux_only_blocked_on_windows(self):
        engine = self._engine()
        for command in ("id", "uname -a", "chmod 777 /tmp", "ss -tlnp"):
            assert engine._platform_compatible(
                {"type": "run_command", "command": command}, {"platform": "windows"}
            ) is False, command

    def test_dual_fallback_keeps_platform_fragment(self):
        engine = self._engine()
        assert engine._platform_compatible(
            {"type": "run_command", "command": "whoami /priv || id"}, {"platform": "linux"}
        ) is True
        assert engine._platform_compatible(
            {"type": "run_command", "command": "ipconfig /all || ifconfig || ip a"}, {"platform": "windows"}
        ) is True

    def test_zero_cooldown_rule_fires_once_per_beacon(self):
        from modules.conditional_hooks import HookRule

        engine = self._engine()
        rule = HookRule(
            name="test-once",
            trigger={"event": "beacon_connected"},
            actions=[{"type": "run_command", "command": "id"}],
            cooldown_seconds=0,
        )
        engine._rules = [rule]
        fired = []
        engine._execute_action = lambda action, ctx: fired.append(action) or None
        engine.fire("beacon_connected", {"client_id": "b1", "platform": "linux"})
        engine.fire("beacon_connected", {"client_id": "b1", "platform": "linux"})
        engine.fire("beacon_connected", {"client_id": "b2", "platform": "linux"})
        assert len(fired) == 2


class TestHandoffTaskResolution:
    def test_explicit_task_id_wins(self):
        assert lazy_handoff._resolve_task_id("t0042") == "t0042"

    def test_empty_falls_back_to_running_task(self, monkeypatch, tmp_path):
        from modules.lazy_loop import TaskStore

        store = TaskStore()
        monkeypatch.setattr(store, "_path", tmp_path / "tasks.json")
        store._raw = {
            "seq": 2,
            "tasks": {
                "t0001": {"task_id": "t0001", "status": "done", "updated": 1},
                "t0002": {"task_id": "t0002", "status": "running", "updated": 2},
            },
        }
        monkeypatch.setattr("modules.lazy_loop.TaskStore", lambda: store)
        assert lazy_handoff._resolve_task_id("") == "t0002"

    def test_empty_falls_back_to_newest_task(self, monkeypatch, tmp_path):
        from modules.lazy_loop import TaskStore

        store = TaskStore()
        monkeypatch.setattr(store, "_path", tmp_path / "tasks.json")
        store._raw = {
            "seq": 2,
            "tasks": {
                "t0001": {"task_id": "t0001", "status": "done", "updated": 1},
                "t0002": {"task_id": "t0002", "status": "exhausted", "updated": 2},
            },
        }
        monkeypatch.setattr("modules.lazy_loop.TaskStore", lambda: store)
        assert lazy_handoff._resolve_task_id("") == "t0002"

    @staticmethod
    def _enable(monkeypatch) -> None:
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setenv(lazy_handoff.HANDOFF_ENV, "1")
        monkeypatch.setattr(
            "core.config.load_payload", lambda *a, **kw: {"loop_beacon_handoff": True}
        )

    def test_marker_carries_resolved_task(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        monkeypatch.setattr(lazy_handoff, "_resolve_task_id", lambda value: "t0009")
        spawns = []
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawns.append(a))
        lazy_handoff.maybe_beacon_handoff("10.0.0.4", sessions_dir=tmp_path)
        state = json.loads(lazy_handoff._marker_path("10.0.0.4", tmp_path).read_text(encoding="utf-8"))
        assert state["task_id"] == "t0009"
        assert "t0009" in spawns[0][0][-1]

    def test_run_separator_written(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        monkeypatch.setattr(lazy_handoff, "_resolve_task_id", lambda value: "t0009")
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: None)
        lazy_handoff.maybe_beacon_handoff("10.0.0.3", source="test", sessions_dir=tmp_path)
        log_text = (tmp_path / "beacon_handoff_10.0.0.3.log").read_text(encoding="utf-8")
        assert "beacon handoff run" in log_text
        assert "target=10.0.0.3" in log_text
        assert "task=t0009" in log_text


class TestBeaconLiveness:
    def test_live_only_skips_disk_fallback(self, monkeypatch, tmp_path):
        from modules import bof_delivery

        cfg = bof_delivery.BofDeliveryConfig(sessions_dir=tmp_path)
        (tmp_path / "linux_beacon.records.jsonl").write_text(
            json.dumps({"client_id": "linux_beacon", "ips": "172.17.0.2"}),
            encoding="utf-8",
        )

        def raising(*args, **kwargs):
            raise OSError("c2 down")

        monkeypatch.setattr(bof_delivery, "_c2_channel_base", lambda cfg, data: "https://127.0.0.1:1")
        monkeypatch.setattr(bof_delivery.time, "sleep", lambda *_: None)
        monkeypatch.setattr(
            "modules.bof_delivery.urllib.request.urlopen", raising, raising=False
        )
        assert bof_delivery.recent_beacons(config=cfg, payload={}, live_only=True) == []
        assert bof_delivery.recent_beacons(config=cfg, payload={}) != []

    def test_last_seen_empty_when_c2_unreachable(self, monkeypatch, tmp_path):
        from modules import bof_delivery

        def raising(*args, **kwargs):
            raise OSError("c2 down")

        monkeypatch.setattr(bof_delivery, "_c2_channel_base", lambda cfg, data: "https://127.0.0.1:1")
        monkeypatch.setattr(
            "modules.bof_delivery.urllib.request.urlopen", raising, raising=False
        )
        assert bof_delivery.beacon_last_seen("linux_beacon", config=bof_delivery.BofDeliveryConfig(sessions_dir=tmp_path), payload={}) == ""

    def test_stale_last_seen_never_counts_as_live(self, monkeypatch, tmp_path):
        history = tmp_path / "linux_beacon.records.jsonl"
        history.write_text(
            json.dumps({"client_id": "linux_beacon", "ips": "172.17.0.2", "timestamp": "2026-11-19T15:29:12+00:00"}),
            encoding="utf-8",
        )
        monkeypatch.setattr(
            "modules.bof_delivery.beacon_for_target", lambda target, config=None: "linux_beacon"
        )
        monkeypatch.setattr(
            "modules.bof_delivery.beacon_last_seen",
            lambda client_id, config=None, payload=None: "",
        )
        assert lazy_handoff._beacon_is_live("172.17.0.2", tmp_path) is False

    def test_fresh_last_seen_counts_as_live(self, monkeypatch, tmp_path):
        history = tmp_path / "linux_beacon.records.jsonl"
        history.write_text(
            json.dumps({"client_id": "linux_beacon", "ips": "172.17.0.2", "timestamp": "2026-11-19T15:29:12+00:00"}),
            encoding="utf-8",
        )
        monkeypatch.setattr(
            "modules.bof_delivery.beacon_for_target", lambda target, config=None: "linux_beacon"
        )
        fresh = (datetime.now(UTC) - timedelta(seconds=30)).isoformat()
        monkeypatch.setattr(
            "modules.bof_delivery.beacon_last_seen",
            lambda client_id, config=None, payload=None: fresh,
        )
        assert lazy_handoff._beacon_is_live("172.17.0.2", tmp_path) is True

    def test_minutes_old_last_seen_counts_as_dead(self, monkeypatch, tmp_path):
        history = tmp_path / "linux_beacon.records.jsonl"
        history.write_text(
            json.dumps({"client_id": "linux_beacon", "ips": "172.17.0.2", "timestamp": "2026-11-19T15:29:12+00:00"}),
            encoding="utf-8",
        )
        monkeypatch.setattr(
            "modules.bof_delivery.beacon_for_target", lambda target, config=None: "linux_beacon"
        )
        stale = (datetime.now(UTC) - timedelta(minutes=27)).isoformat()
        monkeypatch.setattr(
            "modules.bof_delivery.beacon_last_seen",
            lambda client_id, config=None, payload=None: stale,
        )
        assert lazy_handoff._beacon_is_live("172.17.0.2", tmp_path) is False


class TestSkipReason:
    @staticmethod
    def _enable(monkeypatch) -> None:
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.setenv(lazy_handoff.HANDOFF_ENV, "1")
        monkeypatch.setattr(
            "core.config.load_payload", lambda *a, **kw: {"loop_beacon_handoff": True}
        )

    def test_pending_marker_reason(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        lines = []
        lazy_handoff._marker_path("10.0.0.2", tmp_path).write_text(
            json.dumps({"status": "pending"}), encoding="utf-8"
        )
        lazy_handoff._log_skip_reason("10.0.0.2", tmp_path, lines.append)
        assert any("in flight" in line for line in lines)

    def test_live_beacon_reason(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        lines = []
        lazy_handoff._marker_path("10.0.0.2", tmp_path).write_text(
            json.dumps({"status": "deployed", "client_id": "linux_beacon"}), encoding="utf-8"
        )
        monkeypatch.setattr(lazy_handoff, "_beacon_is_live", lambda host, sessions: True)
        lazy_handoff._log_skip_reason("10.0.0.2", tmp_path, lines.append)
        assert any("still reporting" in line for line in lines)

    def test_rearm_reason(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        lines = []
        lazy_handoff._marker_path("10.0.0.2", tmp_path).write_text(
            json.dumps({"status": "deployed", "client_id": "linux_beacon"}), encoding="utf-8"
        )
        monkeypatch.setattr(lazy_handoff, "_beacon_is_live", lambda host, sessions: False)
        lazy_handoff._log_skip_reason("10.0.0.2", tmp_path, lines.append)
        assert any("re-arm" in line for line in lines)

    def test_skip_is_logged_not_silent(self, monkeypatch, tmp_path):
        self._enable(monkeypatch)
        lines = []
        spawns = []
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawns.append(a))
        lazy_handoff._marker_path("10.0.0.2", tmp_path).write_text(
            json.dumps({"status": "deployed", "client_id": "linux_beacon"}), encoding="utf-8"
        )
        monkeypatch.setattr(lazy_handoff, "_beacon_is_live", lambda host, sessions: True)
        assert lazy_handoff.maybe_beacon_handoff("10.0.0.2", sessions_dir=tmp_path, log=lines.append) is False
        assert spawns == []
        assert any("skipped" in line for line in lines)
