"""Freshness ledger contract: recurring windows are ledger windows.

Every scenario states Given, When, Then. One identity key per
verb/target pair unites proposals and executions; a terminal outcome
record inside its TTL silences the planner proposal; never-run rows
sort before waiting rows and failures degrade to "not fresh".
"""

from __future__ import annotations

from pathlib import Path

from modules import lazy_ledger


def _dir(tmp_path: Path) -> Path:
    """Return an isolated ledger sessions directory."""
    store = tmp_path / "lazy"
    store.mkdir(parents=True, exist_ok=True)
    return tmp_path


def test_key_from_command_normalises_addon_surfaces():
    """Given three addon spellings, When deriving keys, Then they collide on one window."""
    proposal = lazy_ledger.key_from_command("lazy addon hydra 127.0.0.1", "")
    replay = lazy_ledger.key_from_command("lazy_addon run hydra --target 127.0.0.1", "")
    bare = lazy_ledger.key_from_command("lazy_addon hydra --target 127.0.0.1", "")
    assert proposal == replay == bare
    assert proposal == "lazy_hydra|127.0.0.1"


def test_plain_verbs_key_by_first_token():
    """Given a non-addon command, When deriving, Then the verb and target pair keys."""
    assert lazy_ledger.key_from_command("lazynmap 10.0.0.9", "10.0.0.9") == "lazynmap|10.0.0.9"
    assert lazy_ledger.key_from_command("", "10.0.0.9") == ""


def test_record_and_fresh_within_window(tmp_path):
    """Given a recorded run, When the window covers now, Then it reads fresh."""
    assert lazy_ledger.fresh("lazy_hydra", "127.0.0.1", sessions_dir=_dir(tmp_path)) is False
    lazy_ledger.record("lazy_hydra", "127.0.0.1", ok=True, sessions_dir=_dir(tmp_path))
    assert lazy_ledger.fresh("lazy_hydra", "127.0.0.1", sessions_dir=_dir(tmp_path)) is True


def test_ttl_windows_are_verb_specific(tmp_path):
    """Given two verbs recorded together, When a short window governs one, Then only that one expires."""
    d = _dir(tmp_path)
    lazy_ledger.record("lazy_hydra", "t", ok=True, now=1000.0, sessions_dir=d)
    lazy_ledger.record("lazynmap", "t", ok=True, now=1000.0, sessions_dir=d)
    assert lazy_ledger.fresh("lazy_hydra", "t", now=1000.0 + 5 * 86400.0, sessions_dir=d) is False
    assert lazy_ledger.fresh("lazynmap", "t", now=1000.0 + 5 * 86400.0, sessions_dir=d) is True
    assert lazy_ledger.fresh("lazy_hydra", "t", now=1000.0 + 24 * 3600, sessions_dir=d) is True


def test_stale_first_orders_unknown_then_oldest(tmp_path):
    """Given mixed history, When ordering, Then unknown first then longest-waiting."""
    d = _dir(tmp_path)
    lazy_ledger.record("a1", "t", ok=True, now=500.0, sessions_dir=d)
    lazy_ledger.record("a2", "t", ok=True, now=100.0, sessions_dir=d)
    ordered = lazy_ledger.stale_first([("a1", "t"), ("a2", "t"), ("a3", "t")], sessions_dir=d)
    assert [pair[0] for pair in ordered] == ["a3", "a2", "a1"]


def test_corrupt_store_fails_open(tmp_path):
    """Given a malformed ledger file, When reading, Then no row is fresh."""
    d = _dir(tmp_path)
    (d / "lazy" / lazy_ledger.LEDGER_FILENAME).write_text("{not json", encoding="utf-8")
    assert lazy_ledger.fresh("lazy_hydra", "127.0.0.1", sessions_dir=d) is False
    assert lazy_ledger.stale_first([("lazy_hydra", "127.0.0.1")], sessions_dir=d) == [
        ("lazy_hydra", "127.0.0.1")
    ]


def test_routing_sink_records_terminal_outcomes(tmp_path, monkeypatch):
    """Given a terminal shell event, When routing records, Then the ledger holds the pair."""
    from modules.outcome_bus import OutcomeEvent
    from modules.sinks import routing

    d = _dir(tmp_path)
    monkeypatch.setattr(Path, "is_file", Path.is_file)
    payload = OutcomeEvent(
        kind="shell",
        task_id="t0001",
        target="127.0.0.1",
        title="demo shell",
        success=True,
        source="demo",
        command="lazy_addon run hydra --target 127.0.0.1",
    )
    monkeypatch.setattr(routing, "record_routing_outcome", lambda *a, **k: None, raising=False)
    import modules.lazy_ledger as ledger

    original = ledger._path
    monkeypatch.setattr(ledger, "_path", lambda sessions_dir=None: d / "lazy" / ledger.LEDGER_FILENAME, raising=False)
    try:
        assert routing.apply(payload) is True
        assert lazy_ledger.fresh("lazy_hydra", "127.0.0.0", sessions_dir=d) is False
        assert lazy_ledger.fresh("lazy_hydra", "127.0.0.1", sessions_dir=d) is True
    finally:
        monkeypatch.setattr(ledger, "_path", original, raising=False)


def test_planner_skips_fresh_addon_proposals(tmp_path, monkeypatch):
    """Given a fresh terminal record, When the planner proposes, Then its addon copy is dropped."""
    d = _dir(tmp_path)
    from modules.lazy_ledger import key_from_command

    verb_key, target_key = key_from_command("lazy addon demoaddon 127.0.0.1", "").split("|", 1)
    lazy_ledger.record(verb_key, target_key, ok=True, sessions_dir=d)

    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "_store_path", lambda name: d / "lazy" / name if "verb_ledger" in str(name) else d / name, raising=False)
    engine_store_patch = loop.TASK_STORES = {}
    del engine_store_patch

    class _PlannerStub(loop.Planner):
        """Expose the freshness helper with a redirected ledger path."""

        def __init__(self) -> None:  # noqa: D401
            """Skip Planner constructor; only the helper method is exercised."""
            self.task_id = "t0001"
            self.assets = None
            self.graph = None
            self.activity = None
            self.store = None
            self.todos = None

    planner = _PlannerStub()
    assert planner._ledger_fresh_summary("lazy addon demoaddon 127.0.0.1") is True
    assert planner._ledger_fresh_summary("lazy addon other 127.0.0.1") is False
