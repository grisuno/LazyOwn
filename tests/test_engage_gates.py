"""BDD tests for gates and transcripts in the live engage path.

Given an EngageOrchestrator with scripted runners, when a command is
denied, duplicated, or already covered by a scan file, then the step
is skipped visibly; every executed step lands in the transcript and
evidence stores under sessions/.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "modules"))
sys.path.insert(0, str(REPO_ROOT / "skills"))


class _ScriptedRunner:
    """ICommandRunner double matching substrings to canned outputs."""

    def __init__(self, scripted: dict[str, str]) -> None:
        """Hold the command to output map."""
        self._scripted = scripted
        self.calls: list[str] = []

    def run(self, command: str, timeout: int) -> str:
        """Record the call and return the first matching output."""
        self.calls.append(command)
        for key, output in self._scripted.items():
            if key in command:
                return output
        return ""

    def name(self) -> str:
        """Identify the double."""
        return "scripted"


class _RecorderNarrator:
    """Narrator double recording event kinds."""

    def __init__(self) -> None:
        """Initialize the event log."""
        self.kinds: list[str] = []

    def narrate(self, kind: str = "", **_kwargs) -> None:
        """Record one event kind."""
        self.kinds.append(kind)


def _approved_gate():
    """Return a gate double that approves everything."""
    return SimpleNamespace(
        request=lambda **_kwargs: SimpleNamespace(is_approved=True, rationale="ok"))


@pytest.fixture
def temp_sessions(tmp_path, monkeypatch):
    """Redirect sessions writes of both engagements and daemon."""
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir(parents=True)
    monkeypatch.setenv("LAZYOWN_DIR", str(tmp_path))
    import autonomous_daemon

    monkeypatch.setattr(autonomous_daemon, "SESSIONS_DIR", sessions_dir)
    return sessions_dir


def _orch(target: str = "10.10.11.5", scripted: dict | None = None,
          plan=None, guard=None):
    """Build an engage orchestrator with doubles."""
    from autonomous_daemon import EngageOrchestrator

    return EngageOrchestrator(
        target=target,
        runner=_ScriptedRunner(scripted or {}),
        narrator=_RecorderNarrator(),
        approval_gate=_approved_gate(),
        safety_guard=guard,
        plan=plan,
    )


def test_denied_command_never_executes(temp_sessions):
    """BDD: a denied step is skipped and its command never runs."""
    from autonomous_daemon import EnginePhaseStep
    from modules.intercept import InterceptRule, Interceptor, Guard

    guard = Guard(interceptor=Interceptor(
        rules=[InterceptRule(pattern="evilwipe", action="deny", priority=50)]))
    orch = _orch(
        scripted={"ping": "1 packets received open"},
        plan=(EnginePhaseStep(phase="recon", primary="ping", label="p"),
              EnginePhaseStep(phase="exploit", primary="evilwipe now", label="e")),
        guard=guard,
    )
    summary = orch.run()
    assert len(summary["steps"]) == 2
    assert summary["steps"][1]["skipped_reason"].startswith("gate:")
    assert not any("evilwipe" in call for call in orch._runner.calls)
    assert "STEP_DENIED" in orch._narrator.kinds


def test_duplicate_success_is_skipped(temp_sessions):
    """BDD: repeating a successful command adds no new direction."""
    from autonomous_daemon import EnginePhaseStep

    orch = _orch(
        scripted={"ping": "1 packets received open"},
        plan=(EnginePhaseStep(phase="recon", primary="ping", label="a"),
              EnginePhaseStep(phase="recon", primary="ping", label="b")),
    )
    summary = orch.run()
    assert summary["steps"][1]["skipped_reason"] == "duplicate_of_successful_step"
    assert sum("ping" in call for call in orch._runner.calls) == 1


def test_scan_step_skipped_when_scan_held(temp_sessions):
    """BDD: lazynmap never re-runs against a held scan file."""
    from autonomous_daemon import EnginePhaseStep

    (temp_sessions / "scan_10.10.11.5.nmap").write_text("<nmap/>")
    orch = _orch(
        scripted={"ping": "1 packets received open"},
        plan=(EnginePhaseStep(phase="recon", primary="ping", label="a"),
              EnginePhaseStep(phase="recon", primary="lazynmap", label="b")),
    )
    summary = orch.run()
    assert summary["steps"][1]["skipped_reason"] == "scan_already_held"
    assert not any("lazynmap" in call for call in orch._runner.calls)


def test_executed_steps_leave_transcript_and_evidence(temp_sessions):
    """BDD: every executed step is recorded with its evidence blob."""
    from autonomous_daemon import EnginePhaseStep
    from modules.traffic_recorder import TrafficRecorder

    orch = _orch(
        scripted={"ping": "1 packets received open success"},
        plan=(EnginePhaseStep(phase="recon", primary="ping", label="a"),),
    )
    orch.run()
    assert TrafficRecorder(temp_sessions / "traffic").count() == 1
    assert list((temp_sessions / "evidence" / "blobs").rglob("*.bin"))
    assert "STEP_DENIED" not in orch._narrator.kinds


def test_notify_journal_written_for_findings(temp_sessions):
    """BDD: high-value notifications render redacted and journal."""
    import autonomous_daemon

    autonomous_daemon._notify_finding("Shell on 10.0.0.1 sk-abcdef123456", "lazymsfvenom",
                                      severity="critical")
    rows = (temp_sessions / "notifications.jsonl").read_text().splitlines()
    assert rows and "[REDACTED]" in rows[0]
    assert json.loads(rows[0])["severity"] == "critical"


def test_no_new_direction_when_world_unchanged(temp_sessions, monkeypatch):
    """BDD: an unchanged world ends the wake with zero extra intents."""
    import autonomous_daemon

    orch = _orch(scripted={"ping": "open"})
    results: list = []
    assert orch._run_planner_intents(results, fp_before="") is False
    assert results == []
    assert "NO_NEW_DIRECTION" in orch._narrator.kinds


def test_planner_intent_executes_mapped_verb(temp_sessions, monkeypatch):
    """BDD: a changed world wakes planner intents mapped to own verbs."""
    import autonomous_daemon

    (temp_sessions / "world_model.json").write_text(
        '{"hosts": {"10.10.11.5": {"state": "scanned"}}}')

    class _Dispatcher:
        def suggest(self, **_kwargs):
            return ("facts_show awakened", object())

    monkeypatch.setattr(autonomous_daemon, "_get_dispatcher",
                        lambda: (lambda: _Dispatcher()))
    orch = _orch(scripted={"facts_show": "found service ssh open"})
    results: list = []
    assert orch._run_planner_intents(results, fp_before="") is False
    assert len(results) >= 1
    assert "PLANNER_INTENT" in orch._narrator.kinds
    assert any("facts_show" in (r.get("command") or "") for r in results)


def test_planner_fallback_pushes_forward(temp_sessions, monkeypatch):
    """BDD: empty refill on a changed world still emits one command."""
    import autonomous_daemon
    from modules.planner import PlanResult

    (temp_sessions / "world_model.json").write_text('{"hosts": {}}')

    class _EmptyPlanner:
        def plan(self, target: str, max_candidates: int = 10) -> PlanResult:
            """Report no candidates."""
            return PlanResult(target=target, candidates=[], chosen=None,
                              rationale="empty", facts_observed=["fact-1"])

    class _Dispatcher:
        def suggest(self, **_kwargs):
            return ("facts_show fallback", object())

    import modules.planner as _planner_mod

    monkeypatch.setattr(autonomous_daemon, "_get_dispatcher",
                        lambda: (lambda: _Dispatcher()))
    orch = _orch(scripted={"facts_show": "found facts open"})
    results: list = []
    assert orch._run_planner_intents(results, fp_before="stale",
                                     planner=_EmptyPlanner()) is False
    assert len(results) == 1
    assert "PLANNER_FALLBACK" in orch._narrator.kinds


def test_latest_hint_renders_newest_event(tmp_path):
    """BDD: spinner hint shows the newest reasoning line."""
    import json as _json

    from cli.reasoning_stream import latest_hint

    assert latest_hint(str(tmp_path / "missing.jsonl")) == ""
    path = tmp_path / "events.jsonl"
    path.write_text(_json.dumps({"id": "1", "ts": "2026-01-01T00:00:00",
                                 "type": "STEP_START", "severity": "info",
                                 "payload": {"command": "lazynmap",
                                             "phase": "recon"}}) + "\n")
    hint = latest_hint(str(path))
    assert "STEP_START" in hint and "lazynmap" in hint


def test_engage_summary_counts_ran_and_skipped(temp_sessions, monkeypatch):
    """BDD: the done message separates ran from skipped steps."""
    import autonomous_daemon
    from autonomous_daemon import EnginePhaseStep

    messages: list[str] = []

    class _Narrator(_RecorderNarrator):
        def narrate(self, kind: str = "", message: str = "", **_kwargs) -> None:
            """Record kinds and messages."""
            self.kinds.append(kind)
            messages.append(message)

    orch = _orch(scripted={"ping": "1 packets received open"})
    orch._narrator = _Narrator()
    orch._plan = (EnginePhaseStep(phase="recon", primary="ping", label="a"),
                  EnginePhaseStep(phase="recon", primary="ping", label="b"))
    orch.run()
    done = next(m for m in messages if "finished" in m)
    assert "1 ran" in done and "1 skipped" in done
