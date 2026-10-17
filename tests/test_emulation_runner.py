"""Emulation runner BDD contract: resolve, execute, normalize, publish.

Every scenario states Given, When, Then. The runner is the only path
from a MITRE technique or APT playbook to an executed Atomic test.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from modules.emulation_runner import EmulationRunner, EmulationStep


@dataclass
class FakeTest:
    """Minimal Atomic test shape consumed by the runner."""

    guid: str = "00000000-0000-0000-0000-000000000001"
    name: str = "Demo test"
    command: str = "echo #{ip_address}"
    platforms: list[str] = field(default_factory=lambda: ["linux"])
    input_arguments: dict = field(default_factory=dict)
    executor_name: str = "sh"


class FakeResolver:
    """Resolver returning one scripted test per technique."""

    def __init__(self, tests: list[FakeTest]) -> None:
        self.tests = tests

    def list_for_technique(self, technique: str, platform: str = ""):
        return list(self.tests)


def test_runner_executes_normalizes_and_publishes(tmp_path: Path):
    """Given a resolved test, When the runner executes, Then the report and bus agree."""
    published: list[dict] = []
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        return "uid=0(root)"

    runner = EmulationRunner(
        resolver=FakeResolver([FakeTest()]),
        sessions_dir=tmp_path,
        shell_detector=lambda spec, output: "uid=" in output,
        outcome_recorder=lambda **kwargs: published.append(kwargs),
    )
    report = runner.run("10.0.0.5", techniques=["T1059"], executor=executor, scan_dir=tmp_path)
    assert report["executed"] == 1 and report["shell"] is True
    assert calls == ["echo 10.0.0.5"]
    assert published and published[0]["kind"] == "emulation"
    assert published[0]["shell"] is True and published[0]["mitre_id"] == "T1059"
    staged = json.loads(Path(report["staged"]).read_text(encoding="utf-8"))
    assert staged["results"][0]["status"] == "executed"


def test_runner_dry_run_never_calls_executor(tmp_path: Path):
    """Given dry_run, When the runner resolves, Then commands are staged without execution."""
    calls: list[str] = []
    runner = EmulationRunner(
        resolver=FakeResolver([FakeTest()]),
        sessions_dir=tmp_path,
        outcome_recorder=lambda **kwargs: None,
    )
    report = runner.run("10.0.0.5", techniques=["T1059"], executor=lambda command: calls.append(command) or "x", dry_run=True)
    assert report["dry_run"] is True
    assert report["executed"] == 1
    assert calls == []
    assert report["results"][0]["status"] == "dry-run"


def test_runner_skips_manual_tests_by_default(tmp_path: Path):
    """Given a manual executor, When include_manual is false, Then it is skipped."""
    manual = FakeTest(executor_name="manual")
    runner = EmulationRunner(
        resolver=FakeResolver([manual]),
        sessions_dir=tmp_path,
        outcome_recorder=lambda **kwargs: None,
    )
    report = runner.run("10.0.0.5", techniques=["T1059"], executor=lambda command: "ran")
    assert report["results"][0]["status"] == "skipped"
    assert report["results"][0]["note"] == "manual"
    report = runner.run("10.0.0.5", techniques=["T1059"], executor=lambda command: "ran", include_manual=True)
    assert report["results"][0]["status"] == "executed"


def test_runner_resolves_playbook_techniques(tmp_path: Path):
    """Given a playbook, When the runner starts, Then its phases supply the techniques."""
    from modules.apt_playbooks import AptPlaybook, PhaseStep

    book = AptPlaybook(
        apt_name="Demo",
        phases=[PhaseStep(name="recon", technique_id="T1018"), PhaseStep(name="exec", technique_id="T1059")],
    )
    runner = EmulationRunner(
        resolver=FakeResolver([FakeTest()]),
        sessions_dir=tmp_path,
        playbook_loader=lambda name: book,
        outcome_recorder=lambda **kwargs: None,
    )
    report = runner.run("10.0.0.5", playbook="demo", executor=lambda command: "ok")
    assert [row["technique"] for row in report["results"]] == ["T1018", "T1059"]


def test_runner_requires_techniques(tmp_path: Path):
    """Given no techniques, When the runner starts, Then it refuses loudly."""
    runner = EmulationRunner(resolver=FakeResolver([]), sessions_dir=tmp_path)
    with pytest.raises(ValueError):
        runner.run("10.0.0.5", executor=lambda command: "ok")


def test_run_steps_handles_dry_run_and_failures():
    """Given resolved steps, When run_steps executes, Then failures are normalized."""
    runner = EmulationRunner(outcome_recorder=lambda **kwargs: None)
    steps = [
        EmulationStep(technique_id="T1059", name="ok", command="echo ok"),
        EmulationStep(technique_id="T1059", name="bad", command="bad"),
        EmulationStep(technique_id="T1059", name="manual", command="manual", manual=True),
    ]

    def executor(command: str) -> str:
        if command == "bad":
            raise RuntimeError("boom")
        return "ok"

    report = runner.run_steps(steps, "10.0.0.5", executor)
    assert [row.status for row in report.results] == ["executed", "error", "skipped"]
    assert "boom" in report.results[1].note


def test_bridge_emulate_delegates_to_runner(monkeypatch, tmp_path: Path):
    """Given the bridge entry point, When emulate runs, Then it delegates once."""
    import modules.atomic_exploit_bridge as bridge

    captured: dict = {}

    class _Runner:
        def __init__(self, **kwargs):
            captured["init"] = kwargs

        def run(self, target, **kwargs):
            captured["target"] = target
            captured["kwargs"] = kwargs
            return {"target": target, "results": [], "executed": 0}

    monkeypatch.setattr("modules.emulation_runner.EmulationRunner", _Runner)
    result = bridge.emulate("10.0.0.5", techniques=["T1059"], scan_dir=tmp_path, include_manual=True)
    assert result["target"] == "10.0.0.5"
    assert captured["kwargs"]["techniques"] == ["T1059"]
    assert captured["kwargs"]["include_manual"] is True


def test_engine_prefers_yaml_command_chain(monkeypatch):
    """Given a YAML exploit id, When the engine builds commands, Then YAML wins over hardcode."""
    import modules.atomic_exploit_bridge as bridge
    from modules.autonomous_exploit_engine import (
        AutonomousExploitEngine,
        ExploitCandidate,
        TargetProfile,
    )

    spec = bridge.ExploitSpec(
        id="demo_strategy",
        mitre_id="T1190",
        cve="CVE-2020-0001",
        title="Demo",
        severity="high",
        confidence=0.9,
        commands=[bridge.ExploitCommand(run="echo yaml {rhost}", timeout=10)],
    )
    monkeypatch.setattr(bridge, "load_all", lambda *args, **kwargs: {"demo_strategy": spec})
    engine = AutonomousExploitEngine()
    candidate = ExploitCandidate(service="ftp", product="demo", version="1", strategy="demo_strategy")
    profile = TargetProfile(ip="10.0.0.5", services=({"name": "ftp", "port": "21"},))
    assert engine._build_command_chain(candidate, profile) == ["echo yaml 10.0.0.5"]


def test_run_steps_dry_run_never_publishes():
    """Given dry_run steps, When run_steps executes, Then the outcome bus stays silent."""
    published: list[dict] = []
    runner = EmulationRunner(outcome_recorder=lambda **kwargs: published.append(kwargs))
    steps = [EmulationStep(technique_id="T1059", name="demo", command="echo ok")]
    report = runner.run_steps(steps, "10.0.0.5", lambda command: "ok", dry_run=True)
    assert report.results[0].status == "dry-run"
    assert published == []


def test_outcome_metadata_uses_scan_dir(tmp_path: Path):
    """Given a scan_dir override, When publishing, Then the sink writes to that session dir."""
    published: list[dict] = []
    other = tmp_path / "other"
    runner = EmulationRunner(
        resolver=FakeResolver([FakeTest()]),
        sessions_dir=tmp_path / "default",
        outcome_recorder=lambda **kwargs: published.append(kwargs),
    )
    runner.run("10.0.0.5", techniques=["T1059"], executor=lambda command: "ok", scan_dir=other)
    assert published[0]["metadata"]["sessions_dir"] == str(other)


def test_resolver_errors_are_reported_not_hidden(tmp_path: Path):
    """Given a broken resolver, When it raises, Then the report carries the reason."""
    class Broken(FakeResolver):
        def list_for_technique(self, technique: str, platform: str = ""):
            raise RuntimeError("index corrupt")

    runner = EmulationRunner(resolver=Broken([]), sessions_dir=tmp_path, outcome_recorder=lambda **kwargs: None)
    report = runner.run("10.0.0.5", techniques=["T1059"], executor=lambda command: "ok")
    assert report["executed"] == 0
    assert "index corrupt" in report["results"][0]["note"]
