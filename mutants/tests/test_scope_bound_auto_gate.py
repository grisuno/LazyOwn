"""tests/test_scope_bound_auto_gate.py

Coverage for the fully autonomous engage mode ("real auto mode").

Test scope:
  - skills/lazyown_policy.py :: ScopeBoundAutoGate — the headless approval
    gate that never prompts a human and keeps the authorized scope as the
    single fail-closed safety boundary of unattended autonomy.
  - skills/lazyown_policy.py :: _default_in_scope / _normalize_scope — the
    scope predicate helpers backed by cli/scope_guard.py loaded in isolation.
  - skills/autonomous_daemon.py :: _engage_run_sync(auto=True) wiring and the
    best-effort _maybe_generate_report chaining.
  - End-to-end guarantee: an out-of-scope target under ``enforce`` is DENIED
    at every step and the command runner is never invoked.
"""

from __future__ import annotations

import importlib
import json
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "modules"))
sys.path.insert(0, str(REPO_ROOT / "skills"))


def _write_payload(tmp_path: Path, data: dict) -> Path:
    """Write *data* to a payload.json inside *tmp_path* and return its path."""
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps(data), encoding="utf-8")
    return payload_path


def _gate(tmp_path: Path, data: dict, in_scope_fn=None):
    """Construct a ScopeBoundAutoGate over a temp payload."""
    from lazyown_policy import ScopeBoundAutoGate

    return ScopeBoundAutoGate(
        payload_path=_write_payload(tmp_path, data),
        in_scope_fn=in_scope_fn,
    )


class TestScopeBoundAutoGate:
    """Unit tests for the headless, scope-bound approval gate."""

    def test_dormant_when_scope_empty(self, tmp_path):
        from lazyown_policy import ApprovalDecision

        gate = _gate(tmp_path, {"scope": [], "scope_enforcement": "enforce"})
        outcome = gate.request(target="10.10.11.5", phase="exploit", command="lazymsfvenom")
        assert outcome.is_approved
        assert outcome.decision == ApprovalDecision.APPROVED
        assert "dormant" in outcome.rationale

    def test_dormant_when_enforcement_off(self, tmp_path):
        gate = _gate(
            tmp_path,
            {"scope": ["192.168.0.0/24"], "scope_enforcement": "off"},
            in_scope_fn=lambda target, entries: False,
        )
        assert gate.request(target="10.10.11.5", phase="exploit", command="x").is_approved

    def test_approves_in_scope_under_enforce(self, tmp_path):
        gate = _gate(
            tmp_path,
            {"scope": ["10.10.11.0/24"], "scope_enforcement": "enforce"},
            in_scope_fn=lambda target, entries: True,
        )
        outcome = gate.request(target="10.10.11.5", phase="exploit", command="x")
        assert outcome.is_approved
        assert "in scope" in outcome.rationale

    def test_denies_out_of_scope_under_enforce(self, tmp_path):
        from lazyown_policy import ApprovalDecision

        gate = _gate(
            tmp_path,
            {"scope": ["10.10.11.0/24"], "scope_enforcement": "enforce"},
            in_scope_fn=lambda target, entries: False,
        )
        outcome = gate.request(target="8.8.8.8", phase="exploit", command="x")
        assert outcome.is_denied
        assert outcome.decision == ApprovalDecision.DENIED
        assert "out of scope" in outcome.rationale

    def test_warns_but_approves_out_of_scope(self, tmp_path):
        gate = _gate(
            tmp_path,
            {"scope": ["10.10.11.0/24"], "scope_enforcement": "warn"},
            in_scope_fn=lambda target, entries: False,
        )
        outcome = gate.request(target="8.8.8.8", phase="exploit", command="x")
        assert outcome.is_approved
        assert "out of scope" in outcome.rationale
        assert "warn" in outcome.rationale

    def test_default_enforcement_is_warn(self, tmp_path):
        gate = _gate(
            tmp_path,
            {"scope": ["10.10.11.0/24"]},
            in_scope_fn=lambda target, entries: False,
        )
        assert gate.request(target="8.8.8.8", phase="exploit", command="x").is_approved

    def test_reads_payload_at_request_time(self, tmp_path):
        from lazyown_policy import ScopeBoundAutoGate

        payload = _write_payload(
            tmp_path, {"scope": ["10.0.0.0/8"], "scope_enforcement": "warn"}
        )
        gate = ScopeBoundAutoGate(payload_path=payload, in_scope_fn=lambda t, e: False)
        assert gate.request("8.8.8.8", "exploit", "x").is_approved
        payload.write_text(
            json.dumps({"scope": ["10.0.0.0/8"], "scope_enforcement": "enforce"}),
            encoding="utf-8",
        )
        assert gate.request("8.8.8.8", "exploit", "x").is_denied

    def test_missing_payload_is_dormant(self, tmp_path):
        from lazyown_policy import ScopeBoundAutoGate

        gate = ScopeBoundAutoGate(payload_path=tmp_path / "does_not_exist.json")
        assert gate.request("8.8.8.8", "exploit", "x").is_approved

    def test_never_blocks_returns_synchronously(self, tmp_path):
        gate = _gate(
            tmp_path,
            {"scope": ["10.10.11.0/24"], "scope_enforcement": "enforce"},
            in_scope_fn=lambda target, entries: False,
        )
        start = time.monotonic()
        outcome = gate.request("8.8.8.8", "exploit", "x")
        assert (time.monotonic() - start) < 1.0
        assert outcome.is_denied

    def test_honours_approval_gate_interface(self, tmp_path):
        from lazyown_policy import ApprovalGate, ScopeBoundAutoGate

        auto = ScopeBoundAutoGate(payload_path=_write_payload(tmp_path, {}))
        assert hasattr(auto, "request")
        assert ApprovalGate.request.__code__.co_varnames[:5] == (
            ScopeBoundAutoGate.request.__code__.co_varnames[:5]
        )


class TestDefaultScopePredicate:
    """Integration with the real cli/scope_guard.py predicate."""

    def test_default_predicate_matches_cidr(self, tmp_path):
        from lazyown_policy import ScopeBoundAutoGate

        gate = ScopeBoundAutoGate(
            payload_path=_write_payload(
                tmp_path, {"scope": ["10.10.11.0/24"], "scope_enforcement": "enforce"}
            )
        )
        assert gate.request("10.10.11.5", "exploit", "x").is_approved
        assert gate.request("8.8.8.8", "exploit", "x").is_denied

    def test_normalize_scope_drops_blanks(self):
        from lazyown_policy import _normalize_scope

        result = _normalize_scope(["10.0.0.1", "  ", "", "host.tld"])
        assert "10.0.0.1" in result
        assert "host.tld" in result
        assert "" not in result
        assert "  " not in result

    def test_in_scope_fails_closed_on_predicate_error(self, tmp_path):
        from lazyown_policy import ScopeBoundAutoGate

        def _boom(target, entries):
            raise RuntimeError("scope predicate exploded")

        gate = ScopeBoundAutoGate(
            payload_path=_write_payload(
                tmp_path, {"scope": ["10.10.11.0/24"], "scope_enforcement": "enforce"}
            ),
            in_scope_fn=_boom,
        )
        with pytest.raises(RuntimeError):
            gate.request("10.10.11.5", "exploit", "x")


class TestAutoEngageWiring:
    """_engage_run_sync auto wiring and report chaining."""

    def test_auto_wires_scope_bound_gate_and_chains_report(self, monkeypatch):
        import autonomous_daemon as daemon
        from lazyown_policy import ScopeBoundAutoGate

        captured: dict = {}

        class _SpyOrchestrator:
            def __init__(self, target, max_switches_per_step=3, approval_gate=None, **kwargs):
                captured["gate"] = approval_gate
                self._target = target

            def run(self):
                return {"target": self._target, "shell_obtained": False, "steps": []}

        monkeypatch.setattr(daemon, "EngageOrchestrator", _SpyOrchestrator)
        monkeypatch.setattr(
            daemon, "_maybe_generate_report", lambda: {"generated": True, "path": "sessions/r.md"}
        )
        summary = daemon._engage_run_sync("10.10.11.5", auto=True)
        assert isinstance(captured["gate"], ScopeBoundAutoGate)
        assert summary["report"] == {"generated": True, "path": "sessions/r.md"}

    def test_non_auto_uses_default_gate_and_no_report(self, monkeypatch):
        import autonomous_daemon as daemon

        captured: dict = {}

        class _SpyOrchestrator:
            def __init__(self, target, max_switches_per_step=3, approval_gate=None, **kwargs):
                captured["gate"] = approval_gate
                self._target = target

            def run(self):
                return {"target": self._target, "shell_obtained": False, "steps": []}

        monkeypatch.setattr(daemon, "EngageOrchestrator", _SpyOrchestrator)
        summary = daemon._engage_run_sync("10.10.11.5", auto=False)
        assert captured["gate"] is None
        assert "report" not in summary

    def test_maybe_generate_report_is_best_effort(self, monkeypatch):
        import autonomous_daemon as daemon

        def _explode(*args, **kwargs):
            raise RuntimeError("report generator missing")

        monkeypatch.setattr(daemon, "_emit", lambda *a, **k: None)
        monkeypatch.setitem(sys.modules, "report_generator", None)
        result = daemon._maybe_generate_report()
        assert result["generated"] is False
        assert "error" in result


class _CountingRunner:
    """ICommandRunner double that records every command it is asked to run."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def run(self, command: str, timeout: int) -> str:
        self.calls.append(command)
        return "open success discovered"

    @property
    def name(self) -> str:
        return "counting"


class TestFailClosedAutonomy:
    """End-to-end: unattended run never touches an out-of-scope host."""

    @pytest.fixture
    def temp_engagement(self, tmp_path):
        sessions_dir = tmp_path / "sessions"
        sessions_dir.mkdir(parents=True)
        payload_path = _write_payload(
            tmp_path, {"scope": ["10.10.11.0/24"], "scope_enforcement": "enforce"}
        )

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
        return {"sessions_dir": sessions_dir, "payload_path": payload_path}

    def test_out_of_scope_denies_all_steps_runner_never_called(self, temp_engagement):
        from autonomous_daemon import EngageOrchestrator
        from lazyown_policy import ScopeBoundAutoGate

        runner = _CountingRunner()
        gate = ScopeBoundAutoGate(payload_path=temp_engagement["payload_path"])
        orchestrator = EngageOrchestrator(
            target="8.8.8.8", runner=runner, approval_gate=gate
        )
        summary = orchestrator.run()

        assert runner.calls == []
        assert summary["steps"], "orchestrator should still report the planned steps"
        assert all(not step["success"] for step in summary["steps"])
        assert all("denied" in (step["skipped_reason"] or "") for step in summary["steps"])
        assert not summary["shell_obtained"]

    def test_in_scope_target_executes_steps(self, temp_engagement):
        from autonomous_daemon import EngageOrchestrator
        from lazyown_policy import ScopeBoundAutoGate

        runner = _CountingRunner()
        gate = ScopeBoundAutoGate(payload_path=temp_engagement["payload_path"])
        orchestrator = EngageOrchestrator(
            target="10.10.11.5", runner=runner, approval_gate=gate
        )
        orchestrator.run()

        assert runner.calls, "in-scope target must actually execute the plan"
