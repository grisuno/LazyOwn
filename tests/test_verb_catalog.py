"""BDD contract tests for the operator verb catalog.

Given a repository whose cmd2 shell exposes hundreds of commands,
When the operator syncs, toggles and queries ``config/verbs.yaml``,
Then every discovered command is catalogued with today's built-ins left
enabled, everything new disabled, operator choices preserved across
syncs, and the autonomous loop refuses disabled CLI verbs.
"""

import json
from pathlib import Path

import pytest

from modules import verb_catalog as catalog


@pytest.fixture()
def sandbox(tmp_path: Path) -> catalog.VerbCatalogConfig:
    """Return a catalog config bound to temporary paths."""
    index_rows = [
        {"name": "do_auto_pwn", "summary": "builtin auto", "phase": "exploit", "duplicate_of": None},
        {"name": "do_lazynmap", "summary": "full scan", "phase": "recon", "duplicate_of": None},
        {"name": "do_webprobe", "summary": "probe web", "phase": "enum", "duplicate_of": None},
        {"name": "do_zzz_stale", "summary": "old command", "phase": "misc", "duplicate_of": None},
    ]
    index_path = tmp_path / "command_index.json"
    index_path.write_text(json.dumps({"commands": index_rows}), encoding="utf-8")
    return catalog.VerbCatalogConfig(catalog_path=tmp_path / "verbs.yaml", index_path=index_path)


def test_sync_generates_catalog_with_builtins_on_and_new_off(sandbox: catalog.VerbCatalogConfig):
    """Given a fresh checkout, sync writes every discovered command with the on/off defaults."""
    stats = catalog.sync(sandbox)
    assert stats["total"] == 4
    assert catalog.entries(sandbox)["auto_pwn"]["enabled"] is True
    assert catalog.entries(sandbox)["lazynmap"]["enabled"] is True
    assert catalog.entries(sandbox)["webprobe"]["enabled"] is False


def test_sync_preserves_operator_choices(sandbox: catalog.VerbCatalogConfig):
    """Given an operator toggle, a later sync keeps the choice and adds new commands off."""
    catalog.sync(sandbox)
    catalog.set_enabled("webprobe", True, sandbox)
    catalog.sync(sandbox)
    entries = catalog.entries(sandbox)
    assert entries["webprobe"]["enabled"] is True
    assert entries["zzz_stale"]["enabled"] is False


def test_sync_prunes_stale_commands(sandbox: catalog.VerbCatalogConfig):
    """Given a command removed from the shell, sync drops its catalog entry."""
    catalog.sync(sandbox)
    catalog.set_enabled("zzz_stale", True, sandbox)
    index_path = sandbox.index_path
    doc = json.loads(index_path.read_text(encoding="utf-8"))
    doc["commands"] = [row for row in doc["commands"] if row["name"] != "do_zzz_stale"]
    index_path.write_text(json.dumps(doc), encoding="utf-8")
    stats = catalog.sync(sandbox)
    assert stats["removed"] == 1
    assert "zzz_stale" not in catalog.entries(sandbox)


def test_load_returns_empty_on_missing_invalid_or_oversize(sandbox: catalog.VerbCatalogConfig, tmp_path: Path):
    """Given a broken catalog file, the loader degrades to an empty mapping."""
    assert catalog.load(sandbox) == {}
    sandbox.catalog_path.write_text("not: [valid", encoding="utf-8")
    assert catalog.load(sandbox) == {}
    sandbox.catalog_path.write_text("x: 'y'\n" * (sandbox.max_yaml_bytes // 10), encoding="utf-8")
    assert catalog.load(sandbox) == {}


def test_set_enabled_unknown_command_raises(sandbox: catalog.VerbCatalogConfig):
    """Given a command the shell does not expose, toggling fails loudly."""
    with pytest.raises(KeyError):
        catalog.set_enabled("no_such_command", True, sandbox)


def test_set_enabled_persists_atomically(sandbox: catalog.VerbCatalogConfig):
    """Given a valid command, toggling writes YAML and reports the new state."""
    catalog.sync(sandbox)
    entry = catalog.set_enabled("webprobe", True, sandbox)
    assert entry["enabled"] is True
    assert catalog.catalog_enabled("webprobe", sandbox) is True
    assert not list(sandbox.catalog_path.parent.glob("*.tmp"))


def test_validate_catalog_rejects_bad_documents(sandbox: catalog.VerbCatalogConfig):
    """Given a malformed document, validation returns human readable errors."""
    assert catalog.validate_catalog({"version": 1, "verbs": {}}) == []
    assert catalog.validate_catalog("nope")
    errors = catalog.validate_catalog({"version": 9, "verbs": {"x": {"enabled": "yes"}}})
    assert any("version" in error for error in errors)
    assert any("x" in error for error in errors)


def test_effective_verbs_include_catalog_entries(sandbox: catalog.VerbCatalogConfig, monkeypatch):
    """Given a synced catalog, the orchestrator merged view exposes CLI verbs."""
    catalog.sync(sandbox)
    monkeypatch.setattr(catalog, "_default_config", lambda: sandbox)
    from modules import orchestrator_config

    monkeypatch.setattr(orchestrator_config, "_payload", lambda: {})
    names = {entry["name"] for entry in orchestrator_config.effective_verbs()}
    assert {"auto_pwn", "lazynmap", "webprobe"} <= names
    entry = orchestrator_config.verb_config("webprobe")
    assert entry is not None and entry["enabled"] is False and entry["source"] == "catalog"
    assert orchestrator_config.verb_enabled("webprobe") is False


def test_loop_refuses_disabled_cli_verb_and_allows_enabled(sandbox: catalog.VerbCatalogConfig, monkeypatch):
    """Given catalog state, the loop router honours it as the permission gate."""
    index_path = sandbox.index_path
    doc = json.loads(index_path.read_text(encoding="utf-8"))
    doc["commands"].append({"name": "do_addalias", "summary": "alias a command", "phase": "misc", "duplicate_of": None})
    index_path.write_text(json.dumps(doc), encoding="utf-8")
    catalog.sync(sandbox)
    monkeypatch.setattr(catalog, "_default_config", lambda: sandbox)
    from modules import lazy_cli_bridge, orchestrator_config

    monkeypatch.setattr(lazy_cli_bridge, "full_cli_enabled", lambda: True)
    monkeypatch.setattr(orchestrator_config, "_payload", lambda: {})
    from modules import auto_registry

    orchestrator_config.reload()
    assert auto_registry.is_shell_verb("addalias") is False
    catalog.set_enabled("addalias", True, sandbox)
    orchestrator_config.reload()
    assert auto_registry.is_shell_verb("addalias") is True
    assert auto_registry.steps_for("auto addalias") == ["addalias"]


def test_stats_reports_on_off_counts(sandbox: catalog.VerbCatalogConfig):
    """Given toggles, stats summarise the catalog for the brief and the API."""
    catalog.sync(sandbox)
    catalog.set_enabled("webprobe", True, sandbox)
    stats = catalog.stats(sandbox)
    assert stats == {"total": 4, "on": 3, "off": 1}


def test_search_filters_catalog(sandbox: catalog.VerbCatalogConfig):
    """Given a query and state filter, search returns matching entries only."""
    catalog.sync(sandbox)
    rows = catalog.search("web", sandbox)
    assert [row["name"] for row in rows] == ["webprobe"]
    rows = catalog.search("", sandbox, enabled=True)
    assert {row["name"] for row in rows} == {"auto_pwn", "lazynmap"}


def _addon_sandbox(tmp_path: Path, enabled: bool = True) -> catalog.VerbCatalogConfig:
    """Return a config whose lazyaddons directory holds one green addon."""
    addons_dir = tmp_path / "lazyaddons"
    addons_dir.mkdir()
    body = (
        f"name: certipy_v2\ndescription: ADCS audit tool.\ncategory: 03. Exploitation\n"
        f"enabled: {str(enabled).lower()}\ntrigger:\n- http\n"
    )
    (addons_dir / "certipy_v2.yaml").write_text(body, encoding="utf-8")
    disabled = addons_dir / "sleepy.yaml"
    if enabled:
        disabled.write_text("name: sleepy\nenabled: false\ntrigger:\n- ssh\n", encoding="utf-8")
    return catalog.VerbCatalogConfig(
        catalog_path=tmp_path / "verbs.yaml",
        index_path=tmp_path / "command_index.json",
        addons_dir=addons_dir,
    )


def test_sync_indexes_enabled_lazyaddons_disabled_by_default(tmp_path: Path):
    """Given a repo lazyaddon, verb sync lists it as an off addon verb."""
    cfg = _addon_sandbox(tmp_path)
    index_path = cfg.index_path
    index_path.write_text(
        json.dumps({"commands": [{"name": "do_lazynmap", "summary": "scan", "phase": "recon", "duplicate_of": None}]}),
        encoding="utf-8",
    )
    stats = catalog.sync(cfg)
    assert stats["total"] == 2
    entry = catalog.entries(cfg)["addon:certipy_v2"]
    assert entry["enabled"] is False
    assert entry["source"] == "addon"
    assert entry["phase"] == "exploit"
    assert entry["description"] == "ADCS audit tool."
    assert "addon:sleepy" not in catalog.entries(cfg)


def test_sync_prunes_renamed_or_disabled_addons(tmp_path: Path):
    """Given an addon flipped off, the next sync drops its catalog row."""
    cfg = _addon_sandbox(tmp_path)
    cfg.index_path.write_text(
        json.dumps({"commands": [{"name": "do_zzz_stale", "summary": "old", "phase": "misc", "duplicate_of": None}]}),
        encoding="utf-8",
    )
    catalog.sync(cfg)
    pkg = cfg.addons_dir / "certipy_v2.yaml"
    pkg.write_text(pkg.read_text(encoding="utf-8").replace("enabled: true", "enabled: false"), encoding="utf-8")
    stats = catalog.sync(cfg)
    assert stats["total"] == 1
    assert "addon:certipy_v2" not in catalog.entries(cfg)


def test_operator_can_turn_addon_verb_on(tmp_path: Path):
    """Given a synced addon, verb on persists the operator choice."""
    cfg = _addon_sandbox(tmp_path)
    index_path = cfg.index_path
    index_path.write_text(json.dumps({"commands": []}), encoding="utf-8")
    catalog.sync(cfg)
    entry = catalog.set_enabled("addon:certipy_v2", True, cfg)
    assert entry["enabled"] is True
    assert entry["source"] == "addon"
    catalog.sync(cfg)
    assert catalog.entries(cfg)["addon:certipy_v2"]["enabled"] is True


def test_steps_for_addon_verb_runs_lazy_addon(tmp_path: Path, monkeypatch):
    """Given an enabled addon verb, the loop router emits a lazy addon line."""
    from types import SimpleNamespace

    from modules import auto_registry

    cfg = _addon_sandbox(tmp_path)
    index_path = cfg.index_path
    index_path.write_text(json.dumps({"commands": []}), encoding="utf-8")
    catalog.sync(cfg)
    catalog.set_enabled("addon:certipy_v2", True, cfg)
    monkeypatch.setattr(
        auto_registry, "_verb_row", lambda name: SimpleNamespace(enabled=True) if name == "addon:certipy_v2" else None
    )
    monkeypatch.setattr(auto_registry, "verb_gap", lambda name: "")
    monkeypatch.setattr(auto_registry, "verb_enabled", lambda name: name == "addon:certipy_v2")
    assert auto_registry.steps_for("auto addon:certipy_v2", "10.0.0.1") == ["lazy addon certipy_v2 10.0.0.1"]
    assert auto_registry.steps_for("auto addon:certipy_v2") == ["lazy addon certipy_v2"]
