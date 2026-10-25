"""Supervision upgrades: repetition watchdog, stack priors, prompt masking."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    """Return an engine whose stores live entirely under tmp_path."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def _isolate_intel(tmp_path, monkeypatch):
    """Redirect intel routing log and priors under tmp_path."""
    import modules.lazy_intel as intel
    import modules.lazy_orchestrator_feedback as feedback

    monkeypatch.setattr(intel, "STORE_DIR", tmp_path)
    monkeypatch.setattr(feedback, "STORE_DIR", tmp_path)


class _DeadPool:
    """LLM pool double with no members (deterministic, no network)."""

    def members(self):
        """Return no members so heuristic paths run."""
        return []

    def complete(self, *args, **kwargs):
        """Return empty reply."""
        return ""


def _kill_llm(monkeypatch):
    """Neutralize every pool the worker path may consult."""
    import modules.lazy_engine as engine
    import modules.lazy_loop as loop

    monkeypatch.setattr(engine, "LlmPool", lambda *a, **k: _DeadPool())
    monkeypatch.setattr(loop, "LlmPool", lambda *a, **k: _DeadPool())


def test_repetition_watchdog_settles(tmp_path, monkeypatch):
    """BDD: three identical consecutive steps settle instead of looping."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    _isolate_intel(tmp_path, monkeypatch)
    _kill_llm(monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "ping the target repeatedly")
    worker = loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )
    monkeypatch.setattr(worker, "_steps_for", lambda _intent: ["ping 127.0.0.1"] * 5)
    calls: list[str] = []
    outcome = worker.execute(intent, executor=lambda cmd: calls.append(cmd) or "pong")
    assert outcome["state"] == "exhausted"
    assert len(calls) == 2
    kinds = [r.get("kind", "") for r in loop.ActivityLog(task_id).read(50)]
    assert "loop-guard" in kinds


def test_stack_priors_prefer_same_stack(tmp_path, monkeypatch):
    """BDD: repeat stacks learn faster, unseen stacks keep default order."""
    import modules.lazy_intel as intel
    import modules.lazy_orchestrator_feedback as feedback

    _isolate_intel(tmp_path, monkeypatch)
    stack = "tcp/22 ssh,tcp/80 http"
    other = "tcp/445 smb"
    for _ in range(3):
        intel.record_routing_decision("t1", 1, "gobuster 10.0.0.5", "probe web", "10.0.0.5", stack)
        intel.record_routing_outcome("t1", 1, "gobuster 10.0.0.5", "done", 1, 0, stack)
    for _ in range(3):
        intel.record_routing_decision("t2", 2, "enum_smb 10.0.0.6", "probe smb", "10.0.0.6", other)
        intel.record_routing_outcome("t2", 2, "enum_smb 10.0.0.6", "done", 1, 0, other)
    summary = feedback.adjust_from_usage()
    assert summary["outcomes"] == 6
    assert feedback.verb_prior("recon", "gobuster", stack) is not None
    assert feedback.verb_prior("recon", "gobuster", "tcp/25 smtp") is None
    ordered = feedback.order_steps(["enum_smb 10.0.0.6", "gobuster 10.0.0.5"], stack)
    assert [c.split()[0] for c in ordered] == ["gobuster", "enum_smb"]
    cold = feedback.order_steps(["enum_smb 10.0.0.6", "gobuster 10.0.0.5"], "tcp/25 smtp")
    assert [c.split()[0] for c in cold] == ["enum_smb", "gobuster"]


def test_prompt_context_masks_configured_only(tmp_path, monkeypatch):
    """BDD: payload secrets never reach cloud backends, loot still does."""
    import modules.lazy_loop as loop
    from core.config import load_payload

    engine = _patched_engine(tmp_path, monkeypatch)
    secret = str((load_payload() or {}).get("start_pass", "") or "")
    assert len(secret) >= 6
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    graph.add_node("fact", f"operator uses {secret} everywhere", state="done")
    graph.add_node("fact", "hash abc123def456 found on share", state="done")
    context = loop.build_prompt_context(task_id, graph, engine.assets, engine.store)
    assert secret not in context
    assert "abc123def456" in context
