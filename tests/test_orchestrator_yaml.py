"""Orchestrator YAML BDD contract: profiles, stages, limits and CLI wiring.

Every scenario states Given, When, Then. YAML is the default source;
payload overrides win. The engine and the admin console read the same
resolved view.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def payload_store(monkeypatch):
    """In-memory payload so profile writes stay sandboxed."""
    store = {"payload": {"rhost": "127.0.0.1"}}

    def _load(target=None):
        return dict(store["payload"])

    def _save(data, target=None):
        store["payload"] = dict(data)

    import core.config

    monkeypatch.setattr(core.config, "load_payload", _load)
    monkeypatch.setattr(core.config, "save_payload", _save)
    import modules.orchestrator_config as config

    config.reload()
    yield store
    config.reload()


def test_shipped_yaml_declares_required_profiles(payload_store):
    """Given the shipped YAML, When profiles load, Then the four profiles exist."""
    from modules import orchestrator_config as config

    profiles = config.profiles()
    assert {"default", "stealth", "lab", "gym"} <= set(profiles)
    assert profiles["default"]["limits"]["rounds"] > 0
    assert profiles["gym"]["sinks"]["intel_graph"] is True


def test_payload_profile_overrides_yaml(payload_store):
    """Given the payload names a profile, When limits resolve, Then that profile wins."""
    from modules import orchestrator_config as config

    assert config.active_profile() == "default"
    config.set_profile("gym")
    assert config.active_profile() == "gym"
    assert config.limits()["rounds"] == 15
    assert payload_store["payload"]["orchestrator"]["profile"] == "gym"


def test_stage_params_resolve_and_payload_still_overrides(payload_store):
    """Given a profile, When a stage is read, Then its params resolve; payload can disable it."""
    from modules import orchestrator_config as config

    config.set_profile("stealth")
    assert config.stage_params("retest")["limit"] == 1
    assert config.limits()["intel_sync_sec"] == 30
    config.set_stage("retest", False)
    assert config.stage_enabled("retest") is False
    assert config.stages()["retest"]["params"]["limit"] == 1


def test_profile_inheritance_merges_stages_and_limits(payload_store, tmp_path, monkeypatch):
    """Given a child profile extends a parent, When resolved, Then parent defaults survive."""
    from modules import orchestrator_config as config

    document = {
        "version": 1,
        "default_profile": "base",
        "stages": {
            "planner": {"enabled": True, "label": "Planner", "fires_when": "round", "params": {"max_intents": 4}},
            "retest": {"enabled": True, "label": "Retest", "fires_when": "round", "params": {"limit": 3}},
        },
        "profiles": {
            "base": {
                "description": "base",
                "limits": {"rounds": 4, "workers": 2},
                "budget": {"max_rounds": 4},
                "chain": "apt_chain",
                "playbook": "rocke",
                "sinks": {"world_model": True},
            },
            "child": {
                "description": "child",
                "extends": "base",
                "stages": {"retest": {"params": {"limit": 1}}},
                "limits": {"rounds": 8},
            },
        },
    }
    import yaml

    target = tmp_path / "orchestrator.yaml"
    target.write_text(yaml.safe_dump(document), encoding="utf-8")
    monkeypatch.setattr(config, "ORCHESTRATOR_YAML_PATH", target)
    config.reload()
    config.set_profile("child")
    assert config.limits()["rounds"] == 8
    assert config.limits()["workers"] == 2
    assert config.stage_params("retest")["limit"] == 1
    assert config.chain_defaults()["chain"] == "apt_chain"


def test_unknown_profile_is_rejected_and_payload_falls_back(payload_store):
    """Given an unknown profile, When set, Then it raises; a stale payload falls back."""
    from modules import orchestrator_config as config

    with pytest.raises(KeyError):
        config.set_profile("ghost")
    payload_store["payload"]["orchestrator"] = {"profile": "ghost"}
    config.reload()
    assert config.active_profile() == "default"


def test_validate_config_rejects_unknown_version_and_bad_stage():
    """Given malformed YAML, When validated, Then errors name the problem."""
    from modules import orchestrator_config as config

    errors = config.validate_config({"version": 9, "default_profile": "x", "profiles": {}})
    assert any("version" in error for error in errors)
    errors = config.validate_config(
        {
            "version": 1,
            "default_profile": "x",
            "profiles": {"x": {"limits": {"rounds": "many"}, "stages": {"ghost": {"enabled": True}}}},
        }
    )
    assert any("rounds" in error for error in errors)
    assert any("ghost" in error for error in errors)


def test_engine_uses_profile_limits(payload_store, monkeypatch, tmp_path):
    """Given the gym profile, When the engine starts, Then its limits follow the YAML."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    engine = loop.LazyLoopEngine()
    engine.apply_profile("gym")
    assert engine.profile_name == "gym"
    assert engine.retest_limit == 4
    assert engine.enrich_limit == 3
    assert engine.worker_cap == 4
    assert engine.heartbeat_sec == 300.0
    assert engine.debounce_sec == 0.2


def test_runner_parses_profile_and_resolves_defaults(payload_store):
    """Given --profile without rounds, When defaults resolve, Then profile limits fill the gap."""
    from modules import orchestrator_config as config
    from modules.lazy_runner import parse_loop_line, resolve_loop_defaults

    config.set_profile("gym")
    parsed = parse_loop_line("--profile gym --target 127.0.0.1 'gain access'")
    assert parsed.profile == "gym"
    assert parsed.rounds_set is False
    resolved = resolve_loop_defaults(parsed)
    assert resolved.rounds == 15
    assert resolved.workers == 4

    explicit = parse_loop_line("--profile gym --rounds 2 --workers 1 'gain access'")
    resolved = resolve_loop_defaults(explicit)
    assert resolved.rounds == 2
    assert resolved.workers == 1


def test_admin_console_switches_profile(payload_store):
    """Given the console, When a profile is activated, Then the payload and rows agree."""
    from cli.lazy_orchestrator import LazyOrchestratorApp
    from modules import orchestrator_config as config

    app = LazyOrchestratorApp()
    assert app.activate_profile("lab") is True
    assert config.active_profile() == "lab"
    assert any(row["name"] == "lab" and row["active"] for row in app.profile_rows())
    assert app.activate_profile("ghost") is False


def test_payload_sink_toggles_override_profile(payload_store):
    """Given payload sink toggles, When resolved, Then they beat YAML and legacy aliases map."""
    from modules import orchestrator_config as config

    assert config.sinks()["killchain"] is True
    payload_store["payload"].setdefault("orchestrator", {})["sinks"] = {
        "killchain": False,
        "asset_graph": False,
    }
    config.reload()
    resolved = config.sinks()
    assert resolved["killchain"] is False
    assert resolved["attack_graph"] is False
    assert resolved["world_model"] is True
