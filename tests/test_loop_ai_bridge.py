"""Loop AI-stack bridge: event bus, oracle, MoE/RL and SWAN wiring.

The bridge is exercised with stubbed dependencies so no expert, trainer
or oracle file is touched; every stage is enabled explicitly per test.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest


@pytest.fixture()
def store(tmp_path, monkeypatch):
    """Sandbox the lazy store for every test in this module."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return tmp_path


@pytest.fixture()
def bridge(monkeypatch):
    """Bridge with every stage enabled and singletons reset."""
    import modules.loop_ai_bridge as module

    monkeypatch.setattr(module, "_stage", lambda name, default=True: True)
    monkeypatch.setattr(module, "_SINGLETONS", {})
    return module


def test_publish_loop_event_skips_stream_kinds(bridge, monkeypatch):
    """Stream noise never reaches the bus; meaningful kinds are categorized."""
    captured: list = []

    class _Bus:
        def publish(self, event) -> None:
            captured.append(event)

    import modules.event_bus as bus_module

    monkeypatch.setattr(bus_module, "get_event_bus", lambda: _Bus())
    bridge.publish_loop_event("t1", "worker-1", "tool", "[allow] nmap")
    bridge.publish_loop_event("t1", "reporter", "finding", "SQLi found")
    assert len(captured) == 1
    assert captured[0].event_type == "loop:finding"
    assert captured[0].payload["task_id"] == "t1"


def test_activity_log_publishes_to_bridge(store, bridge, monkeypatch):
    """Every activity line reaches the bridge (which gates and maps it)."""
    calls: list = []
    monkeypatch.setattr(bridge, "publish_loop_event", lambda task, worker, kind, text: calls.append((kind, worker)))
    from modules.lazy_loop import ActivityLog

    ActivityLog("t1").emit("worker-1", "finish", "intent #1 -> done")
    assert calls == [("finish", "worker-1")]


def test_annotate_detection_uses_oracle(bridge, monkeypatch):
    class _Oracle:
        def assess(self, tool, command, category):
            return SimpleNamespace(probability=0.42, sigma_names=["sigma-a"], recommendation="safe")

    import modules.detection_oracle as oracle_module

    monkeypatch.setattr(oracle_module, "get_oracle", lambda: _Oracle())
    out = bridge.annotate_detection("nmap -sV 127.0.0.1")
    assert out == {"probability": 0.42, "sigma_names": ["sigma-a"], "recommendation": "safe"}


def test_worker_annotates_detection_and_records_outcome(store, bridge, monkeypatch):
    """Guard steps carry oracle risk and feed MoE/RL with the outcome."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(
        bridge,
        "annotate_detection",
        lambda command, action_category="execution": {"probability": 0.42, "sigma_names": ["s"], "recommendation": ""},
    )
    recorded: list = []
    monkeypatch.setattr(bridge, "record_step", lambda *args, **kwargs: recorded.append(args))
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1")
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
    worker.execute(intent, executor=lambda command: "22/tcp open ssh")
    kinds = [record.get("kind") for record in loop.ActivityLog(task_id).read(300)]
    assert "detection" in kinds
    records = loop.TrafficLog(task_id).read(50)
    assert records and records[-1]["meta"]["detection_prob"] == 0.42
    assert recorded


def test_assess_opsec_wraps_scorer_v2(bridge):
    """Real OpsecScorerV2 output comes back as a plain gate mapping."""
    out = bridge.assess_opsec("nmap -sV 10.0.0.5", rhost="10.0.0.5")
    assert out is not None
    assert out["gate"] in ("allow", "warn", "confirm", "block")
    assert 0 <= out["noise"] <= 10
    assert isinstance(out["mitigations"], list)


def test_assess_opsec_off_when_stage_disabled(monkeypatch):
    import modules.loop_ai_bridge as module

    monkeypatch.setattr(module, "_stage", lambda name, default=True: False)
    assert module.assess_opsec("nmap") is None


def test_assess_opsec_graceful_on_scorer_failure(bridge, monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("scorer down")

    monkeypatch.setattr("modules.opsec_scorer.OpsecScorerV2", boom)
    assert bridge.assess_opsec("nmap") is None


def test_intent_tool_class_mapping(bridge):
    """Summaries map to stable classes the reward and planner both share."""
    assert bridge.intent_tool_class("custom tool blackhound 10.0.0.1") == "custom:blackhound"
    assert bridge.intent_tool_class("auto_pwn 10.0.0.1") == "auto_pwn"
    assert bridge.intent_tool_class("advance serial chain: dump hashes") == "serial_chain"
    assert bridge.intent_tool_class("extend finding: SQLi on login") == "extend_finding"
    assert bridge.intent_tool_class("probe service smb") == "probe:smb"
    assert bridge.intent_tool_class("baseline recon: enumerate 10.0.0.1") == "recon"
    assert bridge.intent_tool_class("re-test 10.0.0.1 after change") == "retest"
    assert bridge.intent_tool_class("") == ""


def test_record_outcome_quality_rewards_findings_over_facts(bridge, monkeypatch):
    moe_calls: list = []
    rl_calls: list = []
    monkeypatch.setattr(bridge, "moe_record_outcome", lambda *args, **kwargs: moe_calls.append(args))
    monkeypatch.setattr(bridge, "rl_update", lambda *args, **kwargs: rl_calls.append(args))

    bridge.record_outcome_quality("worker-1", "extend finding: SQLi", facts=0, findings=1)
    assert moe_calls[-1][2] == 1.0
    assert rl_calls[-1][3] == 1.0
    assert rl_calls[-1][2] == "extend_finding"

    bridge.record_outcome_quality("worker-1", "probe service smb", facts=2, findings=0)
    assert moe_calls[-1][2] == 0.5
    assert rl_calls[-1][2] == "probe:smb"

    bridge.record_outcome_quality("worker-1", "probe service smb", facts=0, findings=0)
    assert moe_calls[-1][2] == 0.0


def test_record_outcome_quality_noop_without_class(bridge, monkeypatch):
    calls: list = []
    monkeypatch.setattr(bridge, "moe_record_outcome", lambda *args, **kwargs: calls.append(args))
    bridge.record_outcome_quality("worker-1", "", facts=1, findings=1)
    assert calls == []


def test_decision_quality_reward_is_closed_loop(bridge):
    """The class the worker rewards is the class the planner reads back.

    A fake trainer stands in for the RL store so producer and consumer are
    exercised through the real bridge: a class that keeps yielding nothing
    decays below the optimistic baseline, one that yields findings climbs
    above it, and both are keyed identically.
    """

    class _FakeTrainer:
        def __init__(self) -> None:
            self.q: dict = {}

        def encode_state(self, task_type, phase, ema=0.0):
            return f"{task_type}:{phase}"

        def update(self, state, action, reward, next_state, candidates, detection_prob=0.0):
            learning_rate, discount = 0.1, 0.9
            current = self.q.get((state, action), 1.0)
            max_next = max(self.q.get((next_state, candidate), 1.0) for candidate in candidates)
            self.q[(state, action)] = current + learning_rate * (reward + discount * max_next - current)

        def q_values_for_state(self, state, candidates):
            return {action: self.q.get((state, action), 1.0) for action in candidates}

    bridge._SINGLETONS["rl_trainer"] = _FakeTrainer()
    for _ in range(5):
        bridge.record_outcome_quality("w", "probe service smb", facts=0, findings=0)
    for _ in range(5):
        bridge.record_outcome_quality("w", "extend finding: RCE", facts=0, findings=1)

    yields = bridge.tool_class_yields(["probe service smb", "extend finding: RCE", "probe service rdp"])
    assert yields["probe service smb"] < 1.0
    assert yields["extend finding: RCE"] > 1.0
    assert yields["probe service rdp"] == 1.0


def test_worker_blocks_on_opsec_gate(store, bridge, monkeypatch):
    """A block verdict from the opsec gate short-circuits before running."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(
        bridge,
        "assess_opsec",
        lambda command, rhost="": {"gate": "block", "noise": 10, "explanation": "too loud"},
    )
    ran: list = []
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1")
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
    worker.execute(intent, executor=lambda command: ran.append(command) or "22/tcp open ssh")
    assert ran == []
    kinds = [record.get("kind") for record in loop.ActivityLog(task_id).read(300)]
    assert "opsec" in kinds
    assert "block" in kinds


def test_worker_confirms_via_intercept_on_opsec_confirm(store, bridge, monkeypatch):
    """A confirm verdict routes the command through the intercept queue.

    Exercised directly at ``_guard_step`` so the probe command is not one
    of the read-only prefixes (`nmap`, `curl`, ...) that bypass operator
    confirmation regardless of the gate decision.
    """
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "INTERCEPT_TIMEOUT_SEC", 0.05)
    monkeypatch.setattr(
        bridge,
        "assess_opsec",
        lambda command, rhost="": {"gate": "confirm", "noise": 7, "explanation": "elevated noise"},
    )
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1")
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
    output, status, detail = worker._guard_step(
        intent,
        "id",
        lambda command: "uid=0",
        loop.Budget(engine.store),
        loop.InterceptQueue(task_id),
        {"model_errors": 0},
    )
    assert status == "blocked"
    assert "needs approval" in detail
    kinds = [record.get("kind") for record in loop.ActivityLog(task_id).read(300)]
    assert "intercept" in kinds


def test_finish_records_decision_quality_outcome(store, bridge, monkeypatch):
    """A finished intent feeds its facts/findings yield back as a reward."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    recorded: list = []
    monkeypatch.setattr(bridge, "record_outcome_quality", lambda *args, **kwargs: recorded.append(args))
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1")
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
    worker.execute(intent, executor=lambda command: "22/tcp open ssh")
    assert recorded
    worker_name, intent_summary, facts, findings = recorded[-1]
    assert worker_name == "worker-1"
    assert intent_summary == "baseline recon: enumerate 127.0.0.1"
    assert isinstance(facts, int) and isinstance(findings, int)


def test_planner_rl_rank_demotes_low_yield_and_boosts_high(store, bridge, monkeypatch):
    """Learned yield shifts candidate priority without reordering the list."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)

    def _yields(summaries, phase="engage"):
        table = {"probe service smb": 0.85, "extend finding: RCE": 1.6, "probe service rdp": 1.0}
        return {s: table[s] for s in summaries if s in table}

    monkeypatch.setattr(
        "modules.mediation.telemetry_mediator.TelemetryMediator.tool_class_yields",
        lambda self, summaries, phase="engage": _yields(summaries),
    )
    base = [
        ("probe service smb", [], [], 6),
        ("extend finding: RCE", [], [], 6),
        ("probe service rdp", [], [], 6),
    ]
    ranked = planner._rl_rank(list(base))
    assert [row[0] for row in ranked] == [row[0] for row in base]
    priority = {row[0]: row[3] for row in ranked}
    assert priority["probe service smb"] == 4
    assert priority["extend finding: RCE"] == 8
    assert priority["probe service rdp"] == 6


def test_planner_rl_rank_noop_without_learned_yield(store, monkeypatch):
    """With no learned signal the candidate priorities are untouched."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    monkeypatch.setattr(
        "modules.mediation.telemetry_mediator.TelemetryMediator.tool_class_yields",
        lambda self, summaries, phase="engage": {},
    )
    base = [("probe service smb", [], [], 6), ("extend finding: RCE", [], [], 7)]
    assert planner._rl_rank(list(base)) == base


def test_llm_pool_prefers_moe_expert_and_records_outcome(store, bridge, monkeypatch):
    """The router's expert runs first and its outcome is fed back."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    monkeypatch.setattr(bridge, "moe_route", lambda task_type, goal="": SimpleNamespace(expert_id="b", model="m-b"))
    monkeypatch.setattr(bridge, "rl_select", lambda *args, **kwargs: "b")
    outcomes: list = []
    monkeypatch.setattr(bridge, "moe_record_outcome", lambda *args, **kwargs: outcomes.append(args))
    monkeypatch.setattr(bridge, "rl_update", lambda *args, **kwargs: None)
    calls: list = []

    def _complete(model, prompt, max_tokens=800):
        calls.append(model)
        return "ok"

    monkeypatch.setattr(factory, "complete", _complete)
    pool = loop.LlmPool()
    pool._health = None
    members = [{"name": "a", "model": "groq:m-a", "priority": 5}, {"name": "b", "model": "groq:m-b", "priority": 5}]
    assert pool.complete("x", members=members) == "ok"
    assert calls and calls[0] == "groq:m-b"
    assert outcomes and outcomes[0][0] == "b"


def test_planner_uses_swan_when_available(store, bridge, monkeypatch):
    """SWAN supplies the planning reply when the stage is on."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(bridge, "swan_available", lambda: True)

    def _swan(prompt, task_type="recon", phase="enumeration", timeout=90.0):
        return "probe ssh banner\ncheck ollama api"

    monkeypatch.setattr(bridge, "swan_consult", _swan)
    monkeypatch.setattr(loop.LlmPool, "members", lambda self: [{"name": "stub"}])
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    proposed = [row[0] for row in planner._llm_candidates(set())]
    assert "probe ssh banner" in proposed
