"""Contract tests for modules/loop/objective_bootstrap.py.

Pins the once-per-objective setup contract extracted from the daemon
``_run_objective`` coroutine: goal decomposition, the scope-deny early abort,
asynchronous enrichment, and frontier/guard construction.
"""

from modules.loop.objective_bootstrap import bootstrap_objective


def _collect_emit():
    events: list[tuple[str, dict]] = []

    def _emit(name, payload):
        events.append((name, payload))

    return events, _emit


def test_scope_denied_aborts_before_enrich_and_frontier(monkeypatch):
    events, emit = _collect_emit()
    enrich_calls: list = []

    monkeypatch.setattr(
        "modules.intercept.scope_blocked", lambda _t: "target.gov is out of scope"
    )
    monkeypatch.setattr(
        "modules.enrich.shared_engine",
        lambda: (_ for _ in ()).throw(AssertionError("enrich must not run")),
    )

    result = bootstrap_objective(
        "obj1",
        "enumerate the host",
        "www.target.gov",
        world_model=None,
        obs_parser=None,
        planner=object(),
        emit=emit,
        load_payload=lambda: {},
    )

    assert result.scope_denied == "target.gov is out of scope"
    assert result.frontier is None
    assert result.guard is None
    assert enrich_calls == []
    names = [e[0] for e in events]
    assert "STEP_BLOCKED" in names
    blocked = next(e[1] for e in events if e[0] == "STEP_BLOCKED")
    assert blocked["reason"] == "scope:target.gov is out of scope"


def test_in_scope_builds_frontier_guard_and_enriches(monkeypatch):
    events, emit = _collect_emit()
    enrich_submits: list[str] = []

    class _FakeEngine:
        def submit(self, target):
            enrich_submits.append(target)

    monkeypatch.setattr("modules.intercept.scope_blocked", lambda _t: "")
    monkeypatch.setattr("modules.enrich.shared_engine", lambda: _FakeEngine())

    result = bootstrap_objective(
        "obj1",
        "get a shell and dump credentials",
        "10.0.0.5",
        world_model=None,
        obs_parser=None,
        planner=None,
        emit=emit,
        load_payload=lambda: {},
    )

    assert result.scope_denied == ""
    assert result.frontier is not None
    assert result.guard is not None
    assert enrich_submits == ["10.0.0.5"]
    assert "STEP_BLOCKED" not in [e[0] for e in events]


def test_goals_decomposed_emitted(monkeypatch):
    events, emit = _collect_emit()
    monkeypatch.setattr("modules.intercept.scope_blocked", lambda _t: "")
    monkeypatch.setattr(
        "modules.enrich.shared_engine",
        lambda: type("E", (), {"submit": lambda self, t: None})(),
    )

    result = bootstrap_objective(
        "obj1",
        "get a shell and dump credentials",
        "10.0.0.5",
        world_model=None,
        obs_parser=None,
        planner=object(),
        emit=emit,
        load_payload=lambda: {},
    )

    assert result.goal_tracker is not None
    decomposed = next((e for e in events if e[0] == "GOALS_DECOMPOSED"), None)
    assert decomposed is not None
    assert decomposed[1]["goals"]


def test_goal_failure_degrades_without_raising(monkeypatch):
    events, emit = _collect_emit()
    monkeypatch.setattr("modules.intercept.scope_blocked", lambda _t: "")
    monkeypatch.setattr(
        "modules.enrich.shared_engine",
        lambda: type("E", (), {"submit": lambda self, t: None})(),
    )

    def _boom():
        raise RuntimeError("constraints unavailable")

    result = bootstrap_objective(
        "obj1",
        "get a shell",
        "10.0.0.5",
        world_model=None,
        obs_parser=None,
        planner=object(),
        emit=emit,
        load_payload=_boom,
    )

    assert result.scope_denied == ""
    assert result.task_constraints is None
