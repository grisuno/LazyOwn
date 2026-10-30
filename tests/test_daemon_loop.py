"""BDD tests for the integrated autonomous loop in the daemon.

Given the existing _run_objective flow with an injected planner,
world model and runner, when the frontier empties, a command repeats,
the goal is proven, or the gate holds, then the loop stops or skips
instead of running blind.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "modules"))
sys.path.insert(0, str(REPO_ROOT / "skills"))

import autonomous_daemon as daemon
from modules.planner import PlanCandidate, PlanResult


class _Phase:
    def __init__(self, value: str = "recon") -> None:
        """Hold a phase value."""
        self.value = value


class _World:
    def __init__(self, state: str = "unknown") -> None:
        """Hold a single host state for the target."""
        self._state = state

    def get_phase(self) -> _Phase:
        """Return the recon phase."""
        return _Phase()

    def snapshot(self) -> dict:
        """Return hosts with the configured state."""
        return {"hosts": {"10.9.0.7": {"state": self._state}}}

    def update_from_findings(self, _findings) -> None:
        """Accept findings without effect."""

    def update_host(self, _target, **_kwargs) -> None:
        """Accept host updates without effect."""


class _Parser:
    def parse(self, _output: str, host: str = "", tool: str = "") -> object:
        """Return an empty observation."""
        from modules.obs_parser import Observation

        return Observation(findings=[], tool=tool, host=host, raw_output=_output)


class _Strategy:
    def __init__(self, commands: list[str]) -> None:
        """Cycle through canned commands."""
        self._commands = list(commands)
        self._at = 0

    def next_command(self, target: str, phase: str, services=None, os_hint: str = "linux", goal: str = ""):
        """Return the next canned command as a planner-free decision."""
        command = self._commands[min(self._at, len(self._commands) - 1)]
        self._at += 1
        return daemon.CommandDecision(command=command, source="test", reason="canned")

    def register_output(self, _output: str, _command: str, platform: str = "linux",
                        success: bool = True) -> None:
        """Accept output without effect."""


class _EmptyPlanner:
    def plan(self, _target: str, max_candidates: int = 10) -> PlanResult:
        """Always report no candidates."""
        return PlanResult(target=_target, candidates=[], chosen=None,
                          rationale="empty", facts_observed=[])


def _patch(monkeypatch, tmp_path) -> None:
    """Point sessions, runner, OS probe and database at fakes."""
    monkeypatch.setattr(daemon, "SESSIONS_DIR", tmp_path / "sessions")
    monkeypatch.setattr(daemon, "EVENTS_FILE", tmp_path / "sessions" / "events.jsonl")
    monkeypatch.setattr(daemon, "STEP_DELAY_S", 0)
    monkeypatch.setattr(daemon, "_DaemonControl", None)
    monkeypatch.setattr(daemon, "_run_lazyown", lambda _cmd, _timeout: "open port 80\nsuccess")

    async def _fake_os(_target, _loop) -> str:
        return "unknown"

    monkeypatch.setattr(daemon, "_detect_target_os", _fake_os)
    import modules.db as db_module

    real_get_db = db_module.get_db

    def _fake_get_db(db_path=None):
        return real_get_db(str(tmp_path / "campaign.db"))

    monkeypatch.setattr(db_module, "get_db", _fake_get_db)


def _events(tmp_path) -> list[dict]:
    """Read the emitted event stream."""
    path = tmp_path / "sessions" / "events.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _run(monkeypatch, tmp_path, objective: str, commands: list[str],
         planner=None, world=None, max_steps: int = 5) -> list:
    """Run one objective with fakes and return step results."""
    _patch(monkeypatch, tmp_path)
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(daemon._run_objective(
            "obj1", objective, "10.9.0.7", max_steps,
            _Strategy(commands), world or _World(), _Parser(), None, loop,
            planner=_EmptyPlanner() if planner is None else planner))
    finally:
        loop.close()


def test_loop_ends_when_no_new_direction(monkeypatch, tmp_path):
    """BDD: empty refills with unchanged facts end the objective."""
    results = _run(monkeypatch, tmp_path, "enumerate services", ["lazynmap 10.9.0.7"])
    assert len(results) == 1
    kinds = [e["type"] for e in _events(tmp_path)]
    assert "NO_NEW_DIRECTION" in kinds


def test_loop_skips_unapproved_gated_command(monkeypatch, tmp_path):
    """BDD: a gated credential-dumping command never executes."""
    seen: list[str] = []
    real_run = daemon._run_lazyown
    _patch(monkeypatch, tmp_path)
    monkeypatch.setattr(daemon, "_run_lazyown",
                        lambda cmd, timeout: (seen.append(cmd), "hash dumped")[1])
    loop = asyncio.new_event_loop()
    try:
        results = loop.run_until_complete(daemon._run_objective(
            "obj1", "dump creds", "10.9.0.7", 3,
            _Strategy(["secretsdump.py LOCAL"]), _World(), _Parser(), None, loop,
            planner=_EmptyPlanner()))
    finally:
        loop.close()
    assert results == []
    assert seen == []
    kinds = [e["type"] for e in _events(tmp_path)]
    assert "STEP_SKIPPED" in kinds


def test_loop_stops_when_objective_proven(monkeypatch, tmp_path):
    """BDD: terminal world state matching the goal ends the loop."""
    results = _run(monkeypatch, tmp_path, "gain access to host",
                   ["lazynmap 10.9.0.7"], world=_World(state="exploited"))
    assert len(results) == 1
    kinds = [e["type"] for e in _events(tmp_path)]
    assert "OBJECTIVE_PROVEN" in kinds


def test_loop_skips_duplicate_success(monkeypatch, tmp_path):
    """BDD: an identical successful command never runs twice."""
    seen: list[str] = []

    class _RepeatPlanner:
        def __init__(self) -> None:
            """Track plan calls."""
            self.calls = 0

        def plan(self, target: str, max_candidates: int = 10) -> PlanResult:
            """Emit the same command with a changing fingerprint."""
            self.calls += 1
            candidate = PlanCandidate(technique_id=f"T{self.calls}", name="n",
                                      tactic="discovery", command="echo hello",
                                      score=100.0)
            return PlanResult(target=target, candidates=[candidate], chosen=candidate,
                              rationale="r", facts_observed=[f"fact-{self.calls}"])

    _patch(monkeypatch, tmp_path)
    monkeypatch.setattr(daemon, "_run_lazyown",
                        lambda cmd, timeout: (seen.append(cmd), "ok success")[1])
    loop = asyncio.new_event_loop()
    try:
        results = loop.run_until_complete(daemon._run_objective(
            "obj1", "enumerate", "10.9.0.7", 4,
            _Strategy(["echo hello"]), _World(), _Parser(), None, loop,
            planner=_RepeatPlanner()))
    finally:
        loop.close()
    assert len(results) == 1
    assert seen == ["assign rhost 10.9.0.7\nassign os_id 4\necho hello"]


def test_decompose_goal_splits_compound(tmp_path):
    """BDD: compound goals split into verifiable objectives."""
    import sys
    from pathlib import Path as _Path

    _root = _Path(__file__).resolve().parent.parent
    for _entry in (str(_root / "skills"), str(_root / "modules")):
        if _entry not in sys.path:
            sys.path.insert(0, _entry)
    from lazyown_objective import decompose_goal

    assert decompose_goal("gain initial access") == ["gain initial access"]
    assert decompose_goal("") == []
    assert decompose_goal("scan the target and then gain initial access",
                          target="10.9.0.7") == [
        "scan the target on 10.9.0.7", "gain initial access on 10.9.0.7"]
    assert decompose_goal("strengthen monitoring") == ["strengthen monitoring"]


def test_marker_helpers_extract_real_output():
    """BDD: marker wrap and strip isolate real command output."""
    import sys
    from pathlib import Path as _Path

    _root = _Path(__file__).resolve().parent.parent
    for _entry in (str(_root / "skills"), str(_root / "modules")):
        if _entry not in sys.path:
            sys.path.insert(0, _entry)
    from autonomous_daemon import _strip_between_markers, _with_markers

    wrapped = _with_markers("ping", "__M__")
    assert "__M___A" in wrapped and "__M___B" in wrapped
    assert _strip_between_markers("__M___A\nreal\n__M___B\nchrome", "__M__") == "real"
    assert _strip_between_markers("no markers here", "__M__") == "no markers here"
    assert _strip_between_markers("__M___B\n__M___A", "__M__") != ""
