"""LLM retry layers, wall-clock settle, stall-guard (lazy 0.3.8/0.3.9 parity)."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def test_empty_reply_replays_before_failover(tmp_path, monkeypatch):
    """BDD: a connected-but-empty model is replayed, not abandoned."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    _patched_engine(tmp_path, monkeypatch)
    calls = []

    def scripted(model, prompt, max_tokens=800):
        calls.append(model)
        return "" if len(calls) < 3 else "probe the login form"

    monkeypatch.setattr(factory, "complete", scripted)
    pool = loop.LlmPool()
    pool._health = None
    assert pool.complete("suggest one probe") == "probe the login form"
    assert len(calls) == 3


def test_empty_budget_exhausted_moves_to_next_member(tmp_path, monkeypatch):
    """BDD: empty budget spent on one member, the chain still answers."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    _patched_engine(tmp_path, monkeypatch)
    models = []

    def first_empty_then_ok(model, prompt, max_tokens=800):
        models.append(model)
        return "answer" if "ollama" in model else ""

    monkeypatch.setattr(factory, "complete", first_empty_then_ok)
    pool = loop.LlmPool()
    pool._health = None
    assert pool.complete("suggest one probe", empty_retries=0) == "answer"
    assert any("groq" in m for m in models)
    assert any("ollama" in m for m in models)


def test_error_reply_fails_over_instead_of_becoming_content(tmp_path, monkeypatch):
    """BDD: backend error banners are failures, never planner intents."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    _patched_engine(tmp_path, monkeypatch)

    def error_then_ok(model, prompt, max_tokens=800):
        return ("[LLM error] GROQ_API_KEY not set."
                if "groq" in model else "probe the login form")

    monkeypatch.setattr(factory, "complete", error_then_ok)
    pool = loop.LlmPool()
    pool._health = None
    assert pool.complete("suggest one probe") == "probe the login form"


def test_worker_llm_steps_filtered_by_scope_and_tooling(tmp_path, monkeypatch):
    """BDD: pool commands pass scope, binary and deny filters before running."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]

    def scripted(model, prompt, max_tokens=800):
        return ("nmap -sV 127.0.0.1\n"
                "definitelynotinstalled -x 127.0.0.1\n"
                "curl http://10.9.9.9/inside\n"
                "curl -sS http://127.0.0.1/\n")

    monkeypatch.setattr(factory, "complete", scripted)
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "probe http surface")
    worker = loop.Worker("worker-1", task_id, engine.assets, graph,
                         loop.ActivityLog(task_id), loop.TrafficLog(task_id),
                         loop.Guard(task_id), engine.store)
    steps = worker._llm_steps(intent)
    assert steps == ["nmap -sV 127.0.0.1", "curl -sS http://127.0.0.1/"]


def test_wall_clock_settles_partial_not_hard_kill(tmp_path, monkeypatch):
    """BDD: expired deadline stops the work and keeps partial steps."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    intent = engine.add_intent(task_id, "probe ssh")
    engine.store.set_deadline(task_id, -1.0)
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker("worker-1", task_id, engine.assets, graph,
                         loop.ActivityLog(task_id), loop.TrafficLog(task_id),
                         loop.Guard(task_id), engine.store)
    outcome = worker.execute(graph.get(intent.node_id), executor=lambda cmd: "ok")
    assert outcome["state"] == "stopped"
    trail = loop.ActivityLog(task_id).read(50)
    assert any(r.get("kind") == "timeout" and "settling" in r.get("text", "")
               for r in trail)


def test_stall_guard_forces_intent_when_nothing_open(tmp_path, monkeypatch):
    """BDD: goals unmet plus zero open work always yields a next intent."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph,
                           loop.ActivityLog(task_id), engine.store)
    first = planner.plan()
    assert len(first) >= 1
    for node in loop.ExplorationGraph(task_id).list("intent"):
        loop.ExplorationGraph(task_id).set_state(node.node_id, "done")
    fresh = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, fresh,
                           loop.ActivityLog(task_id), engine.store)
    second = planner.plan()
    assert len(second) >= 1
    assert {n.node_id for n in second} != {n.node_id for n in first}


def test_task_llm_chain_quota_failover(tmp_path, monkeypatch):
    """BDD: explicit quota exhaustion rotates the task chain permanently."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    engine.store.set_llm_chain(task_id, [
        {"name": "primary", "model": "groq:llama", "priority": 10},
        {"name": "backup", "model": "ollama:local", "priority": 5},
    ])

    def scripted(model, prompt, max_tokens=800):
        if "groq" in model:
            return "Error: quota exceeded, insufficient credits"
        return "probe the login form"

    monkeypatch.setattr(factory, "complete", scripted)
    pool = loop.LlmPool()
    pool._health = None
    assert pool.complete("suggest", task_id=task_id) == "probe the login form"
    state = engine.store.llm_state(task_id)
    assert int(state["active"]) == 1
    seen: list[str] = []

    def scripted_next(model, prompt, max_tokens=800):
        seen.append(model)
        return "ok"

    monkeypatch.setattr(factory, "complete", scripted_next)
    assert pool.complete("suggest", task_id=task_id) == "ok"
    assert seen and "groq" not in seen[0]


def test_raw_llm_recording_toggle(tmp_path, monkeypatch):
    """BDD: raw prompts/replies are recorded only while enabled."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    _patched_engine(tmp_path, monkeypatch)
    pool = loop.LlmPool()
    pool._health = None
    monkeypatch.setattr(factory, "complete",
                        lambda model, prompt, max_tokens=800: "answer")
    assert pool.record_raw() is False
    assert pool.set_record_raw(True) is True
    assert pool.complete("question one") == "answer"
    entries = pool.raw_entries(10)
    assert entries and entries[-1]["reply"] == "answer"
    assert "question one" in entries[-1]["prompt"]
    pool.set_record_raw(False)
    pool.complete("question two")
    assert len(pool.raw_entries(10)) == len(entries)


def test_llm_context_budget_roundtrip(tmp_path, monkeypatch):
    """BDD: prompt context budget is persisted and clamped."""
    import modules.lazy_loop as loop

    _patched_engine(tmp_path, monkeypatch)
    pool = loop.LlmPool()
    assert pool.set_context_budget(900) == 900
    assert pool.context_budget() == 900
    assert pool.set_context_budget(1) == 200
    assert pool.set_context_budget(10 ** 9) == 20000


def test_planner_uses_bound_task_chain(tmp_path, monkeypatch):
    """BDD: a bound task chain drives planner LLM calls, not the global pool."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    engine.store.set_llm_chain(task_id, [{"name": "only", "model": "ollama:local",
                                          "priority": 0}])
    models: list[str] = []

    def scripted(model, prompt, max_tokens=800):
        models.append(model)
        return "probe the smb service"

    monkeypatch.setattr(factory, "complete", scripted)
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph,
                           loop.ActivityLog(task_id), engine.store)
    candidates = planner._llm_candidates(set())
    assert models and all("ollama" in model for model in models)
    assert any("smb" in summary for summary, _a, _p, _pr in candidates)
