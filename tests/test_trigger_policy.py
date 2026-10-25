"""BDD contract tests for the declarative trigger policy.

Given ``config/orchestrator.yaml`` declares a ``triggers`` section,
When the loop starts or the operator syncs,
Then seeds land in the persistent TriggerStore without duplicating
existing runtime triggers, invalid seeds fail loudly into validation,
and the exported store state reflects both YAML seeds and runtime
additions.
"""

from pathlib import Path



from modules import trigger_policy


def test_validate_policy_rejects_bad_documents():
    """Given a malformed section, validation returns readable errors."""
    assert trigger_policy.validate_triggers([]) == []
    assert trigger_policy.validate_triggers([{"kind": "interval", "every_sec": 30}]) == []
    errors = trigger_policy.validate_triggers([{"kind": "nope"}, {"kind": "interval"}, {"kind": 5}])
    assert len(errors) == 2


def test_seeds_coerce_and_skip_unknown_kinds():
    """Given mixed seed quality, coercion keeps valid rows and drops the rest."""
    raw = [
        {"kind": "interval", "every_sec": "45", "enabled": "true"},
        {"kind": "unknown_kind"},
        {"kind": "service", "enabled": False},
    ]
    seeds = trigger_policy.seeds(raw)
    assert seeds == [
        {"kind": "interval", "arg": "", "every_sec": 45.0, "enabled": True},
        {"kind": "service", "arg": "", "every_sec": 0.0, "enabled": False},
    ]


def test_yaml_seeds_read_from_orchestrator_document():
    """Given a full YAML document, the reader extracts the triggers section."""
    doc = {"version": 1, "triggers": [{"kind": "toolcall", "every_sec": 10}]}
    seeds = trigger_policy.seeds(doc.get("triggers") or [])
    assert seeds[0]["kind"] == "toolcall"
    assert trigger_policy.seeds(None) == []


def test_seed_store_is_idempotent(tmp_path: Path, monkeypatch):
    """Given repeated seed_store calls, the store gains each seed only once."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    policy = [
        {"kind": "service", "enabled": True},
        {"kind": "interval", "every_sec": 60, "enabled": True},
    ]
    trigger_policy.seed_store(policy=policy)
    trigger_policy.seed_store(policy=policy)
    items = trigger_policy.export_store()
    kinds = sorted(item["kind"] for item in items)
    assert kinds == ["interval", "service"]
    assert all(item["enabled"] for item in items)


def test_seed_store_keeps_runtime_triggers(tmp_path: Path, monkeypatch):
    """Given an operator-added runtime trigger, seeding does not remove it."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    from modules.loop_triggers import TriggerStore

    store = TriggerStore("")
    runtime = store.add("finding")
    trigger_policy.seed_store(policy=[{"kind": "service"}])
    items = store.list()
    assert any(item["id"] == runtime["id"] for item in items)
    assert any(item["kind"] == "service" for item in items)


def test_orchestrator_yaml_declares_trigger_seeds():
    """Given the shipped orchestrator.yaml, the triggers section validates."""
    data = trigger_policy.read_policy()
    assert data, "orchestrator YAML triggers section must exist"
    assert data["raw"] and data["seeds"], "repo config must seed at least one trigger"


def test_seed_store_drops_unknown_kinds(tmp_path: Path, monkeypatch):
    """Given a malformed seed, the store never accepts an unknown kind."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    trigger_policy.seed_store(policy=[{"kind": "not_a_kind", "every_sec": 5}])
    items = trigger_policy.export_store()
    assert [item["kind"] for item in items] == []

