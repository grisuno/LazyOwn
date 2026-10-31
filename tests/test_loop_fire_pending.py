"""Vertical test: fire-pending intelligence drives a real auto_loop round.

Exercises the true loop path on the real modules: the shared selector
cascade (modules.selection), the planner turning the pending action into a
``run action:`` intent, ``Worker._steps_for`` expanding it verbatim, and the
registry routing ``lazyautofire`` through the shell verb path. A recorded
stub shell keeps the run read-only.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPORT_TARGET = "10.66.44.7"
REPORT_MATCH = {
    "cve_id": "CVE-2025-24813",
    "host": REPORT_TARGET,
    "port": 8080,
    "protocol": "tcp",
    "product": "apache tomcat",
    "version": "9.0.45",
    "tier": "hot",
    "cvss": 9.8,
    "evidence": "in_range",
    "references": [],
    "source": "scanner",
}


class _RecordingShell:
    """Shell stub the workers execute routable verbs on."""

    def __init__(self) -> None:
        self.executed: list[str] = []

    def onecmd_plus_hooks(self, line: str) -> None:
        self.executed.append(line)
        print("action ran")


@pytest.fixture()
def fire_report(tmp_path: Path, monkeypatch) -> Path:
    """Sandbox the intelligence paths and stage a hot fire report."""
    import modules.lazy_autofire as autofire_module
    import modules.selection.intel as intel_module

    (tmp_path / f"lazy_intel_{REPORT_TARGET}.json").write_text(json.dumps({
        "target": REPORT_TARGET,
        "temperature": "hot",
        "score": 50,
        "matches": [dict(REPORT_MATCH)],
    }), encoding="utf-8")
    monkeypatch.setattr(intel_module, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(intel_module, "BASE_DIR", tmp_path)
    monkeypatch.setattr(autofire_module, "CHAINS_DIR", tmp_path / "chains")
    monkeypatch.setattr(autofire_module, "SESSIONS_DIR", tmp_path)
    return tmp_path


class TestCascadeFirePending:
    def test_cascade_answers_fire_first(self, fire_report):
        story = "with fire intel pending the shared cascade proposes the confirmation action"
        from modules.selection import registry
        from modules.selection.base import SelectionContext

        decision = registry.propose_next(SelectionContext(target=REPORT_TARGET, phase="recon"))
        assert decision is not None, story
        assert decision.source == "intel", story
        assert decision.command == f"lazyautofire fire {REPORT_TARGET}", story


class TestPlannerFireIntent:
    def test_planner_queues_fire_action(self, fire_report, monkeypatch):
        story = "the planner's selector cascade queues a run action intent for the pending fire"
        import modules.lazy_loop as loop
        from modules.lazy_engine import LazyEngine

        monkeypatch.setattr(loop, "resolve_target", lambda *a, **k: REPORT_TARGET)
        engine = LazyEngine()
        task_id = engine.create_task(f"probe {REPORT_TARGET}")["task_id"]
        planner = loop.Planner(task_id, engine.assets, loop.ExplorationGraph(task_id), loop.ActivityLog(task_id), engine.store)
        intents = planner._selector_candidates()
        texts = [item[0] for item in intents]
        assert f"run action: lazyautofire fire {REPORT_TARGET}" in texts, story
        priorities = [item[3] for item in intents if item[0].startswith("run action: lazyautofire")]
        assert priorities and priorities[0] <= 2, story

    def test_planner_dedupes_after_first_proposal(self, fire_report, monkeypatch):
        story = "already queued fire actions never repeat (exclude set)"
        import modules.lazy_loop as loop
        from modules.lazy_engine import LazyEngine

        monkeypatch.setattr(loop, "resolve_target", lambda *a, **k: REPORT_TARGET)
        engine = LazyEngine()
        task_id = engine.create_task(f"probe {REPORT_TARGET}")["task_id"]
        graph = loop.ExplorationGraph(task_id)
        graph.add_node("intent", f"run action: lazyautofire fire {REPORT_TARGET}", priority=2)
        planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
        assert planner._selector_candidates() == [], story


class TestWorkerExecutesFireAction:
    def test_steps_expand_verbatim(self):
        story = "run action intents expand to the exact command line"
        import modules.lazy_loop as loop
        from modules.lazy_engine import LazyEngine

        engine = LazyEngine()
        task_id = engine.create_task(f"probe {REPORT_TARGET}")["task_id"]
        graph = loop.ExplorationGraph(task_id)
        intent = graph.add_node("intent", f"run action: lazyautofire fire {REPORT_TARGET}", priority=2)
        worker = loop.Worker(
            "worker-fire",
            task_id,
            engine.assets,
            graph,
            loop.ActivityLog(task_id),
            loop.TrafficLog(task_id),
            loop.Guard(task_id),
            engine.store,
            shell=None,
        )
        assert worker._steps_for(intent) == [f"lazyautofire fire {REPORT_TARGET}"], story

    def test_registry_routes_and_shell_receives(self):
        story = "the lazyautofire verb is loop-routable and lands on the shell onecmd"
        import modules.lazy_loop as loop
        from modules.auto_registry import is_routable_command

        assert is_routable_command(f"lazyautofire fire {REPORT_TARGET}") is True, story
        engine = LazyEngineX = None
        _ = engine
        shell = _RecordingShell()
        from modules.lazy_engine import LazyEngine
        from modules.lazy_loop import Worker

        engine = LazyEngine()
        task_id = engine.create_task(f"probe {REPORT_TARGET}")["task_id"]
        worker = Worker(
            "worker-fire-run",
            task_id,
            engine.assets,
            loop.ExplorationGraph(task_id),
            loop.ActivityLog(task_id),
            loop.TrafficLog(task_id),
            loop.Guard(task_id),
            engine.store,
            shell=shell,
        )
        worker._run(f"lazyautofire fire {REPORT_TARGET}", None)
        assert f"lazyautofire fire {REPORT_TARGET}" in shell.executed, story


class TestRegistry:
    def test_lazy_intel_verbs_routable(self):
        story = "the loop registers lazy intel verbs as built-in routables"
        from modules.auto_registry import ROUTABLE_VERBS

        assert {"lazyintel", "lazyautofire", "lazytimeline", "lazysearch"} <= set(ROUTABLE_VERBS), story
