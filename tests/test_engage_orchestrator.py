"""tests/test_engage_orchestrator.py

Coverage for the engage feature added in modules/engagement_hooks.py,
skills/lazyown_policy.py (ApprovalGate), skills/autonomous_daemon.py
(EngageOrchestrator + narrator + shell detector), and the lazyc2.py /
lazyown.py wiring around them.

Test scope:
  - EngagementNarrator persists to engagement.log and engagement_audit.jsonl
  - NotificationBroadcaster fans out to every sink
  - publish_shell_obtained is idempotent per client_id
  - ApprovalGate honours auto_approve, gates only gated phases, polls the
    injected sink, and respects the timeout
  - FileApprovalSink stores pending then resolved records
  - StdinApprovalSink returns None when stdin is not a TTY
  - EngageOrchestrator: validates target, runs the plan, switches tools on
    failure, narrates SWITCH_TOOL events, stops on shell-obtained indicator
  - StaticFallbackResolver returns alternatives in order, then exhausts
  - mcp_engage_target rejects bogus targets and returns an engagement_id
  - mcp_engage_status returns log lines + pending approvals
  - lazyown.py exposes do_engage; lazyc2.py installs the SHELL_OBTAINED hook
"""

from __future__ import annotations

import ast
import io
import json
import sys
import time
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "modules"))
sys.path.insert(0, str(REPO_ROOT / "skills"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def temp_sessions(tmp_path, monkeypatch):
    """Redirect engagement_hooks to a writable temp sessions dir."""
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir(parents=True)
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps({"auto_approve": True}))

    monkeypatch.setenv("LAZYOWN_DIR", str(tmp_path))

    import importlib

    import engagement_hooks
    importlib.reload(engagement_hooks)
    engagement_hooks.ENGAGEMENT_LOG = sessions_dir / "engagement.log"
    engagement_hooks.ENGAGEMENT_AUDIT = sessions_dir / "engagement_audit.jsonl"
    engagement_hooks.APPROVALS_FILE = sessions_dir / "engagement_approvals.jsonl"
    engagement_hooks.SHELL_SEEN_FILE = sessions_dir / "engagement_seen_beacons.json"
    engagement_hooks.StreamEventSink.EVENTS_FILE = sessions_dir / "autonomous_events.jsonl"
    engagement_hooks._SESSIONS_DIR = sessions_dir
    engagement_hooks._PAYLOAD_FILE = payload_path
    engagement_hooks._default_narrator_singleton = None

    yield {
        "sessions_dir": sessions_dir,
        "payload_path": payload_path,
        "log_file":     engagement_hooks.ENGAGEMENT_LOG,
        "audit_file":   engagement_hooks.ENGAGEMENT_AUDIT,
        "approvals":    engagement_hooks.APPROVALS_FILE,
        "seen_file":    engagement_hooks.SHELL_SEEN_FILE,
        "events_file":  engagement_hooks.StreamEventSink.EVENTS_FILE,
    }


# ---------------------------------------------------------------------------
# EngagementNarrator + sinks
# ---------------------------------------------------------------------------


class TestEngagementNarrator:
    def test_narrate_writes_log_and_audit(self, temp_sessions):
        from engagement_hooks import EngagementNarrator, NotificationBroadcaster, StreamEventSink

        bcast = NotificationBroadcaster([StreamEventSink()])
        narrator = EngagementNarrator(broadcaster=bcast)
        event = narrator.narrate(
            kind="STEP_START",
            target="10.0.0.5",
            message="nmap full scan",
            payload={"phase": "recon"},
        )

        assert event.kind == "STEP_START"
        assert event.target == "10.0.0.5"
        assert temp_sessions["log_file"].exists()
        content = temp_sessions["log_file"].read_text()
        assert "STEP_START" in content
        assert "nmap full scan" in content

        audit_lines = temp_sessions["audit_file"].read_text().splitlines()
        assert len(audit_lines) == 1
        record = json.loads(audit_lines[0])
        assert record["kind"] == "STEP_START"
        assert record["payload"]["phase"] == "recon"

    def test_stream_sink_appends_to_autonomous_events(self, temp_sessions):
        from engagement_hooks import EngagementNarrator, NotificationBroadcaster, StreamEventSink

        narrator = EngagementNarrator(
            broadcaster=NotificationBroadcaster([StreamEventSink()])
        )
        narrator.narrate(kind="PHASE", target="t", message="m")
        assert temp_sessions["events_file"].exists()
        line = temp_sessions["events_file"].read_text().splitlines()[0]
        record = json.loads(line)
        assert record["type"] == "PHASE"
        assert record["payload"]["target"] == "t"

    def test_render_line_format_is_stable(self):
        from engagement_hooks import EngagementEvent

        evt = EngagementEvent(
            event_id="abc12345",
            ts="2026-05-16T18:42:01+00:00",
            kind="STEP_DONE",
            target="10.10.11.5",
            message="nmap succeeded",
        )
        line = evt.render_line()
        assert line.startswith("[2026-05-16T18:42:01Z] [INFO    ] [STEP_DONE")
        assert "10.10.11.5" in line
        assert "nmap succeeded" in line


class TestNotificationBroadcaster:
    def test_fans_out_to_every_sink(self, temp_sessions):
        from engagement_hooks import EngagementEvent, INotificationSink, NotificationBroadcaster

        deliveries: list[str] = []

        class _CountingSink(INotificationSink):
            def __init__(self, name: str) -> None:
                self._name = name

            @property
            def name(self) -> str:
                return self._name

            def deliver(self, event: EngagementEvent) -> bool:
                deliveries.append(self._name)
                return True

        bcast = NotificationBroadcaster([_CountingSink("a"), _CountingSink("b")])
        accepted = bcast.deliver(EngagementEvent.now("X", "t", "m"))
        assert deliveries == ["a", "b"]
        assert accepted == ["a", "b"]

    def test_failing_sink_does_not_break_broadcaster(self, temp_sessions):
        from engagement_hooks import EngagementEvent, INotificationSink, NotificationBroadcaster

        class _BoomSink(INotificationSink):
            @property
            def name(self) -> str:
                return "boom"

            def deliver(self, event: EngagementEvent) -> bool:
                raise RuntimeError("simulated network outage")

        class _GoodSink(INotificationSink):
            @property
            def name(self) -> str:
                return "good"

            def deliver(self, event: EngagementEvent) -> bool:
                return True

        bcast = NotificationBroadcaster([_BoomSink(), _GoodSink()])
        accepted = bcast.deliver(EngagementEvent.now("Y", "t", "m"))
        assert accepted == ["good"]


# ---------------------------------------------------------------------------
# publish_shell_obtained
# ---------------------------------------------------------------------------


class TestShellObtainedPublisher:
    def test_first_call_emits_event(self, temp_sessions):
        from engagement_hooks import publish_shell_obtained

        evt = publish_shell_obtained(
            client_id="abc123",
            primary_ip="10.10.11.5",
            hostname="dc01.varia.htb",
            user="SYSTEM",
            platform="windows",
        )
        assert evt is not None
        assert evt.kind == "SHELL_OBTAINED"
        assert evt.target == "10.10.11.5"
        assert temp_sessions["seen_file"].exists()
        seen = json.loads(temp_sessions["seen_file"].read_text())
        assert "abc123" in seen

    def test_repeat_call_is_idempotent(self, temp_sessions):
        from engagement_hooks import publish_shell_obtained

        first = publish_shell_obtained(client_id="b1", primary_ip="1.2.3.4")
        second = publish_shell_obtained(client_id="b1", primary_ip="1.2.3.4")
        assert first is not None
        assert second is None

    def test_invalid_client_id_returns_none(self, temp_sessions):
        from engagement_hooks import publish_shell_obtained

        assert publish_shell_obtained(client_id="", primary_ip="1.2.3.4") is None
        assert publish_shell_obtained(client_id=None, primary_ip="1.2.3.4") is None  # type: ignore[arg-type]

    def test_client_id_is_sanitised(self, temp_sessions):
        from engagement_hooks import publish_shell_obtained

        evt = publish_shell_obtained(
            client_id="../etc/passwd-injection",
            primary_ip="10.10.10.10",
        )
        assert evt is not None
        seen = json.loads(temp_sessions["seen_file"].read_text())
        keys = list(seen.keys())
        assert all(".." not in k and "/" not in k for k in keys)


# ---------------------------------------------------------------------------
# is_valid_target
# ---------------------------------------------------------------------------


class TestIsValidTarget:
    def test_accepts_ipv4(self):
        from engagement_hooks import is_valid_target

        assert is_valid_target("10.10.11.5")
        assert is_valid_target("127.0.0.1")

    def test_accepts_hostname(self):
        from engagement_hooks import is_valid_target

        assert is_valid_target("dc01.varia.htb")
        assert is_valid_target("target-server")

    def test_rejects_garbage(self):
        from engagement_hooks import is_valid_target

        assert not is_valid_target("")
        assert not is_valid_target("999.999.999.999")
        assert not is_valid_target("rm -rf /")
        assert not is_valid_target("'; DROP TABLE users; --")
        assert not is_valid_target(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# ApprovalGate
# ---------------------------------------------------------------------------


@pytest.fixture
def policy_module(temp_sessions, monkeypatch):
    """Reload lazyown_policy so its module-level paths see the temp dir."""
    import importlib

    import lazyown_policy
    importlib.reload(lazyown_policy)
    return lazyown_policy


class _RecordingSink:
    """Test double satisfying IApprovalSink."""

    def __init__(self) -> None:
        self.announced: list[Any] = []
        self.resolutions: dict[str, Any] = {}

    def announce(self, request) -> None:
        self.announced.append(request)

    def resolution_for(self, approval_id: str):
        return self.resolutions.get(approval_id)


class TestApprovalGate:
    def test_auto_approve_true_returns_approved_for_gated_phase(
        self, policy_module, temp_sessions
    ):
        # payload.json already has auto_approve: true from the fixture.
        gate = policy_module.ApprovalGate(
            sink=_RecordingSink(),
            payload_path=temp_sessions["payload_path"],
        )
        outcome = gate.request(
            target="10.10.11.5",
            phase="exploit",
            command="msfconsole",
            reason="test",
        )
        assert outcome.is_approved
        assert outcome.rationale == "auto_approve=true"

    def test_non_gated_phase_bypasses_sink(self, policy_module, temp_sessions):
        sink = _RecordingSink()
        gate = policy_module.ApprovalGate(
            sink=sink,
            payload_path=temp_sessions["payload_path"],
        )
        outcome = gate.request(
            target="10.10.11.5",
            phase="recon",
            command="lazynmap",
            reason="test",
        )
        assert outcome.is_approved
        assert outcome.rationale == "phase not gated"
        assert sink.announced == []

    def test_gated_phase_with_auto_approve_false_polls_sink(
        self, policy_module, temp_sessions
    ):
        temp_sessions["payload_path"].write_text(json.dumps({"auto_approve": False}))
        sink = _RecordingSink()

        def _injected_sleep(_seconds: float) -> None:
            # Inject the resolution as soon as the gate sleeps once.
            request = sink.announced[0]
            sink.resolutions[request.approval_id] = policy_module.ApprovalOutcome(
                decision=policy_module.ApprovalDecision.APPROVED,
                approval_id=request.approval_id,
                rationale="injected by test",
                operator="tester",
            )

        gate = policy_module.ApprovalGate(
            sink=sink,
            payload_path=temp_sessions["payload_path"],
            poll_interval_s=0.1,
            poll_timeout_s=2.0,
            sleep_fn=_injected_sleep,
        )
        outcome = gate.request(
            target="10.10.11.5",
            phase="exploit",
            command="msfconsole",
            reason="initial-access stage",
        )
        assert outcome.is_approved
        assert len(sink.announced) == 1

    def test_gated_phase_times_out_to_denied(
        self, policy_module, temp_sessions
    ):
        temp_sessions["payload_path"].write_text(json.dumps({"auto_approve": False}))
        sink = _RecordingSink()
        gate = policy_module.ApprovalGate(
            sink=sink,
            payload_path=temp_sessions["payload_path"],
            poll_interval_s=0.05,
            poll_timeout_s=0.15,
            sleep_fn=lambda _s: None,
        )
        outcome = gate.request(
            target="10.10.11.5",
            phase="privesc",
            command="linpeas",
            reason="late-stage",
        )
        assert outcome.is_denied
        assert "timeout" in outcome.rationale

    def test_invalid_payload_defaults_to_auto_approve_true(
        self, policy_module, temp_sessions
    ):
        temp_sessions["payload_path"].write_text("not-json")
        gate = policy_module.ApprovalGate(
            sink=_RecordingSink(),
            payload_path=temp_sessions["payload_path"],
        )
        outcome = gate.request(
            target="t", phase="exploit", command="x", reason="r"
        )
        assert outcome.is_approved


class TestFileApprovalSink:
    def test_announce_writes_pending_record(self, policy_module, temp_sessions):
        sink = policy_module.FileApprovalSink(sessions_dir=temp_sessions["sessions_dir"])
        request = policy_module.ApprovalRequest(
            approval_id="abc12345",
            target="10.0.0.1",
            phase="exploit",
            command="msfconsole",
            reason="test",
            created_ts="2026-05-16T00:00:00+00:00",
        )
        sink.announce(request)
        assert sink.path.exists()
        record = json.loads(sink.path.read_text().splitlines()[0])
        assert record["approval_id"] == "abc12345"
        assert record["status"] == "pending"

    def test_resolution_returns_latest_non_pending(self, policy_module, temp_sessions):
        sink = policy_module.FileApprovalSink(sessions_dir=temp_sessions["sessions_dir"])
        request = policy_module.ApprovalRequest(
            approval_id="r1",
            target="t",
            phase="exploit",
            command="x",
            reason="r",
            created_ts="now",
        )
        sink.announce(request)
        with sink.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "approval_id": "r1",
                "status":      "approved",
                "operator":    "alice",
                "rationale":   "ok",
            }) + "\n")
        outcome = sink.resolution_for("r1")
        assert outcome is not None
        assert outcome.is_approved
        assert outcome.operator == "alice"


class TestStdinApprovalSink:
    def test_no_tty_returns_none(self, policy_module):
        sink = policy_module.StdinApprovalSink(stream=io.StringIO())
        request = policy_module.ApprovalRequest(
            approval_id="x1", target="t", phase="exploit",
            command="c", reason="r", created_ts="now",
        )
        sink.announce(request)  # stdin is not a TTY in pytest
        assert sink.resolution_for("x1") is None


# ---------------------------------------------------------------------------
# Fallback resolver
# ---------------------------------------------------------------------------


class TestStaticFallbackResolver:
    def test_returns_alternatives_in_order(self):
        from autonomous_daemon import _TOOL_FALLBACK_MAP, StaticFallbackResolver

        r = StaticFallbackResolver()
        assert _TOOL_FALLBACK_MAP["lazynmap"] == ("rustscan", "masscan", "nmap")
        assert r.next_tool("lazynmap", "recon", 0) == "rustscan"
        assert r.next_tool("lazynmap", "recon", 1) == "masscan"
        assert r.next_tool("lazynmap", "recon", 2) == "nmap"
        assert r.next_tool("lazynmap", "recon", 3) is None

    def test_unknown_primary_returns_none(self):
        from autonomous_daemon import StaticFallbackResolver

        assert StaticFallbackResolver().next_tool("doesnotexist", "recon", 0) is None


# ---------------------------------------------------------------------------
# EngageOrchestrator
# ---------------------------------------------------------------------------


class _ScriptedRunner:
    """ICommandRunner double driven by an in-memory map of cmd -> output.

    Outputs default to '' which counts as a failure under the heuristic,
    forcing the fallback path. Keys can be substrings matched against the
    composed command (so 'lazynmap' matches 'assign rhost ...\nlazynmap').
    """

    def __init__(self, scripted: dict[str, str]) -> None:
        self._scripted = scripted
        self.calls: list[str] = []

    def run(self, command: str, timeout: int) -> str:
        self.calls.append(command)
        for key, output in self._scripted.items():
            if key in command:
                return output
        return ""

    @property
    def name(self) -> str:
        return "scripted"


class _NoOpGate:
    def request(self, target, phase, command, reason):
        from lazyown_policy import ApprovalDecision, ApprovalOutcome
        return ApprovalOutcome(
            decision=ApprovalDecision.APPROVED,
            approval_id="",
            rationale="no-op gate",
        )


class _RejectingGate:
    def __init__(self, rejected_phase: str) -> None:
        self._rejected = rejected_phase

    def request(self, target, phase, command, reason):
        from lazyown_policy import ApprovalDecision, ApprovalOutcome
        if phase == self._rejected:
            return ApprovalOutcome(
                decision=ApprovalDecision.DENIED,
                approval_id="rej",
                rationale="rejected by test",
            )
        return ApprovalOutcome(
            decision=ApprovalDecision.APPROVED,
            approval_id="",
            rationale="ok",
        )


class TestEngageOrchestrator:
    def test_rejects_invalid_target(self, temp_sessions, policy_module):
        from autonomous_daemon import EngageOrchestrator

        with pytest.raises(ValueError):
            EngageOrchestrator(target="not a target")

    def test_runs_full_plan_on_success(self, temp_sessions, policy_module):
        from autonomous_daemon import EngageOrchestrator

        runner = _ScriptedRunner({
            "ping":          "1 packets received open",
            "lazynmap":      "22/tcp open ssh",
            "auto_populate": "discovered domain target.htb",
            "facts_show":    "found service ssh",
            "searchsploit":  "CVE-2024-1234 found",
            "lazymsfvenom":  "payload generated success",
        })
        orch = EngageOrchestrator(
            target="10.10.11.5",
            runner=runner,
            approval_gate=_NoOpGate(),
        )
        summary = orch.run()
        assert summary["target"] == "10.10.11.5"
        assert len(summary["steps"]) == 6
        assert all(s["success"] for s in summary["steps"])
        assert not summary["shell_obtained"]

    def test_switches_tool_on_failure(self, temp_sessions, policy_module):
        from autonomous_daemon import EngageOrchestrator, StaticFallbackResolver

        runner = _ScriptedRunner({
            "ping":          "1 packets received open",
            # lazynmap fails (empty output), rustscan succeeds
            "rustscan":      "22 open",
            "auto_populate": "discovered open",
            "facts_show":    "found facts open",
            "searchsploit":  "CVE found",
            "lazymsfvenom":  "payload success",
        })
        orch = EngageOrchestrator(
            target="10.10.11.5",
            runner=runner,
            approval_gate=_NoOpGate(),
            fallback_resolver=StaticFallbackResolver(),
        )
        summary = orch.run()
        nmap_step = [s for s in summary["steps"] if s["phase"] == "recon" and "lazynmap" in s.get("switched_from", "")]
        assert nmap_step, "expected lazynmap to be switched to a fallback"
        assert nmap_step[0]["command"] == "rustscan"
        assert nmap_step[0]["success"]

    def test_denied_step_is_skipped(self, temp_sessions, policy_module):
        from autonomous_daemon import EngageOrchestrator

        runner = _ScriptedRunner({
            "ping":          "1 packets received open",
            "lazynmap":      "open",
            "auto_populate": "open",
            "facts_show":    "found",
            "searchsploit":  "CVE found",
            "lazymsfvenom":  "payload success",
        })
        orch = EngageOrchestrator(
            target="10.10.11.5",
            runner=runner,
            approval_gate=_RejectingGate(rejected_phase="exploit"),
        )
        summary = orch.run()
        exploit = [s for s in summary["steps"] if s["phase"] == "exploit"]
        assert exploit, "exploit step must be present in result list"
        assert exploit[0]["success"] is False
        assert "denied" in exploit[0]["skipped_reason"]

    def test_shell_indicator_stops_loop(self, temp_sessions, policy_module):
        from autonomous_daemon import EngageOrchestrator

        runner = _ScriptedRunner({
            "ping":          "uid=0(root) shell open got shell",
        })
        orch = EngageOrchestrator(
            target="10.10.11.5",
            runner=runner,
            approval_gate=_NoOpGate(),
        )
        summary = orch.run()
        assert summary["shell_obtained"] is True
        assert len(summary["steps"]) == 1


# ---------------------------------------------------------------------------
# MCP entry points
# ---------------------------------------------------------------------------


class TestMcpEntryPoints:
    def test_engage_target_rejects_invalid(self, temp_sessions, policy_module):
        from autonomous_daemon import mcp_engage_target

        result = json.loads(mcp_engage_target("invalid target"))
        assert result["status"] == "error"

    def test_engage_target_returns_engagement_id(self, temp_sessions, policy_module):
        from autonomous_daemon import mcp_engage_target

        result = json.loads(mcp_engage_target("10.0.0.1", detach=True))
        assert result["status"] == "started"
        assert "engagement_id" in result
        # Background thread is running; give it a moment to no-op exit.
        time.sleep(0.2)

    def test_engage_status_returns_pending_approvals_structure(
        self, temp_sessions, policy_module
    ):
        from autonomous_daemon import mcp_engage_status

        result = json.loads(mcp_engage_status(last_n=5))
        assert result["status"] == "ok"
        assert "lines" in result
        assert "pending_approvals" in result

    def test_engage_approve_rejects_bad_decision(self, temp_sessions, policy_module):
        from autonomous_daemon import mcp_engage_approve

        result = json.loads(mcp_engage_approve("abc", "maybe"))
        assert result["status"] == "error"

    def test_engage_approve_accepts_valid_decision(
        self, temp_sessions, policy_module
    ):
        from autonomous_daemon import mcp_engage_approve

        result = json.loads(mcp_engage_approve("abc12345", "approved", "alice"))
        assert result["status"] == "ok"
        assert result["decision"] == "approved"
        assert result["operator"] == "alice"


# ---------------------------------------------------------------------------
# Wiring smoke tests (no runtime invocation)
# ---------------------------------------------------------------------------


class TestWiring:
    def test_do_engage_method_exists_in_lazyown(self):
        src = (REPO_ROOT / "lazyown.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        methods = [
            n.name for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "do_engage"
        ]
        assert len(methods) == 1, "do_engage must be defined exactly once"

    def test_lazyc2_has_engagement_hook_call(self):
        src = (REPO_ROOT / "lazyc2.py").read_text(encoding="utf-8")
        assert "publish_shell_obtained" in src, (
            "lazyc2.py must call publish_shell_obtained on beacon registration"
        )

    def test_mcp_exposes_four_engage_tools(self):
        src = (REPO_ROOT / "skills" / "lazyown_mcp.py").read_text(encoding="utf-8")
        for name in (
            "lazyown_engage_target",
            "lazyown_engage_status",
            "lazyown_engage_approve",
            "lazyown_engage_list_pending",
        ):
            assert src.count(f'"{name}"') >= 1, f"{name} missing from MCP tool list"

    def test_daemon_has_engage_subcommand(self):
        from autonomous_daemon import _COMMANDS

        assert "engage" in _COMMANDS

    def test_payload_json_auto_approve_key_is_bool_when_present(self):
        cfg = json.loads((REPO_ROOT / "payload.json").read_text(encoding="utf-8"))
        if "auto_approve" in cfg:
            assert isinstance(cfg["auto_approve"], bool), (
                "auto_approve must be a JSON boolean when present"
            )

    def test_approval_gate_defaults_to_true_when_key_missing(self, tmp_path):
        import lazyown_policy

        payload = tmp_path / "payload.json"
        payload.write_text(json.dumps({"rhost": "10.0.0.1"}))
        gate = lazyown_policy.ApprovalGate(
            sink=_RecordingSink(),
            payload_path=payload,
        )
        outcome = gate.request(
            target="10.0.0.1", phase="exploit",
            command="msfconsole", reason="test",
        )
        assert outcome.is_approved
        assert outcome.rationale == "auto_approve=true"

    def test_engagement_hooks_module_exposes_public_surface(self):
        import engagement_hooks
        for name in (
            "EngagementEvent",
            "EngagementNarrator",
            "NotificationBroadcaster",
            "publish_shell_obtained",
            "is_valid_target",
            "list_pending_approvals",
            "resolve_approval",
        ):
            assert hasattr(engagement_hooks, name), f"missing public symbol: {name}"

    def test_policy_module_exposes_approval_surface(self):
        import lazyown_policy
        for name in (
            "ApprovalGate",
            "ApprovalDecision",
            "ApprovalOutcome",
            "IApprovalSink",
            "FileApprovalSink",
            "BroadcastApprovalSink",
            "StdinApprovalSink",
            "CompositeApprovalSink",
        ):
            assert hasattr(lazyown_policy, name), f"missing public symbol: {name}"
