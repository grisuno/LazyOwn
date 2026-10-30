"""Module-registry loop bridge: corpus mentions enter planning as intents.

Every scenario states Given, When, Then. Fixtures build a temporary
registry base; the singleton factory is replaced so tests stay isolated,
and planner integration runs on a temporary loop store.
"""

from __future__ import annotations

from pathlib import Path

from modules.module_registry import ModuleInfo, ModuleRegistry


def _registry(tmp_path: Path) -> ModuleRegistry:
    """Build one registry over a temporary base with curated modules."""
    addons = tmp_path / "lazyaddons"
    addons.mkdir(parents=True, exist_ok=True)
    (addons / "lazy_hydra.yaml").write_text(
        "name: lazy_hydra\n"
        "description: Online password brute forcing\n"
        "category: 07. Credential Access\n"
        "enabled: true\n",
        encoding="utf-8",
    )
    (addons / "lazy_winsweep.yaml").write_text(
        "name: lazy_winsweep\n"
        "description: windows enumeration\n"
        "category: 04. Post-Exploitation\n"
        "os: windows\n",
        encoding="utf-8",
    )
    playbooks = tmp_path / "playbooks"
    playbooks.mkdir(parents=True, exist_ok=True)
    (playbooks / "rocke.json").write_text(
        '{"name": "rocke", "description": "ransomware emulation"}', encoding="utf-8"
    )
    registry = ModuleRegistry(tmp_path)
    registry.scan()
    return registry


def _registry_with_extras(tmp_path: Path) -> ModuleRegistry:
    """Extend the fixture registry with non-runnable sources."""
    registry = _registry(tmp_path)
    registry._modules["pytool"] = ModuleInfo(name="pytool", description="python helper", source="python")
    registry._modules["luatool"] = ModuleInfo(name="luatool", description="lua plugin", source="lua")
    return registry


def _empty_osinfer(monkeypatch) -> None:
    """Force host OS inference to report nothing."""
    from modules import lazy_osinfer

    monkeypatch.setattr(lazy_osinfer, "host_os_for_target", lambda target: "", raising=False)


def test_name_mentions_propose_runnable_intents(tmp_path, monkeypatch):
    """Given a corpus mentioning a module name token, When proposing, Then the command is runnable."""
    _empty_osinfer(monkeypatch)
    registry = _registry_with_extras(tmp_path)
    out = registry.proposal_intents(["brute force with lazy_hydra against smb"], target="127.0.0.1")
    assert out == ["lazy addon lazy_hydra 127.0.0.1"]


def test_playbook_mentions_map_to_apt_playbook(tmp_path, monkeypatch):
    """Given a corpus mentioning a playbook name, When proposing, Then apt_playbook runs it."""
    _empty_osinfer(monkeypatch)
    registry = _registry(tmp_path)
    out = registry.proposal_intents(["emulate the rocke playbook"], target="127.0.0.1")
    assert out == ["apt_playbook run rocke"]


def test_incompatible_os_is_gated(tmp_path, monkeypatch):
    """Given an incompatible host OS, When proposing the addon, Then the OS gate blocks it."""
    from modules import lazy_osinfer

    monkeypatch.setattr(lazy_osinfer, "host_os_for_target", lambda target: "linux", raising=False)
    monkeypatch.setattr(lazy_osinfer, "os_compatible", lambda fork, host: False, raising=False)
    registry = _registry_with_extras(tmp_path)
    out = registry.proposal_intents(["winsweep sweep results"], target="10.0.0.2")
    assert out == []


def test_fillers_and_nonrunnable_sources_propose_nothing(tmp_path, monkeypatch):
    """Given filler vocabulary and keywords of excluded sources, When proposing, Then nothing lands."""
    _empty_osinfer(monkeypatch)
    registry = _registry_with_extras(tmp_path)
    out = registry.proposal_intents(["pytool luatool for the with this that check port"])
    assert out == []


def test_limit_caps_results(tmp_path, monkeypatch):
    """Given two matching modules, When the limit is one, Then only the first lands."""
    addons = tmp_path / "lazyaddons"
    addons.mkdir(parents=True, exist_ok=True)
    (addons / "lazy_radcliff.yaml").write_text(
        "name: lazy_radcliff\ndescription: sweep\nenabled: true\n", encoding="utf-8"
    )
    _empty_osinfer(monkeypatch)
    registry = ModuleRegistry(tmp_path)
    registry.scan()
    out = registry.proposal_intents(["radcliff sweep sweep"], limit=1)
    assert out == ["lazy addon lazy_radcliff"]


def test_planner_appends_registry_candidates_last(tmp_path, monkeypatch):
    """Given a finding naming a module, When the planner proposes, Then the registry candidate lands."""
    registry = _registry_with_extras(tmp_path)
    import modules.lazy_loop as loop
    from modules.module_registry import ModuleRegistry as ModReg

    monkeypatch.setattr(ModReg, "get_instance", classmethod(lambda cls, base=None: registry), raising=False)
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name, raising=False)
    engine = type("EngineStub", (), {"assets": None, "store": None})()
    from modules.lazy_engine import LazyEngine

    real_engine = LazyEngine()
    task_id = real_engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    graph.add_node("finding", "hydra confirms weak credentials", state="done")
    planner = loop.Planner(task_id, real_engine.assets, graph, loop.ActivityLog(task_id), real_engine.store)
    rows = planner._candidates()
    summaries = [row[0] for row in rows]
    assert "lazy addon lazy_hydra" in " ".join(summaries)
