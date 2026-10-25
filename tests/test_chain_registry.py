"""Chain registry: orchestration from chains/*.yaml, never hardcoded steps."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules.chain_registry import get, load_all, validate_chain  # noqa: E402


def test_shipped_chain_loads() -> None:
    """The bundled apt_chain has ten ordered steps ending in emulation."""
    chain = get("apt_chain")
    assert chain is not None
    assert len(chain.steps) == 12
    assert chain.steps[0].run == "assign target {target}"
    assert chain.steps[1].skip_if_exists == "sessions/scan_{target}.nmap.xml"
    runs = [step.run for step in chain.steps]
    assert "c2_server start" in runs
    assert "c2_deploy {target}" in runs
    assert "c2_loot {target} /etc/shadow" in runs
    assert "create_session_json" in runs
    assert runs[-1] == "atomic_shell --interactive {target}"


def test_validate_rejects_bad_chains() -> None:
    """Schema violations are reported, never silently accepted."""
    assert validate_chain({"name": "Bad Name", "steps": [{"run": "x"}]}, filename="x")
    assert validate_chain({"name": "ok", "steps": []}, filename="ok")
    assert validate_chain({"name": "ok", "steps": [{"run": ""}]}, filename="ok")
    assert validate_chain({"name": "ok", "steps": [{"run": "x", "resolve_newest": {"glob": "a"}}]}, filename="ok")
    assert validate_chain("not a mapping", filename="ok")
    assert validate_chain({"name": "a", "steps": [{"run": "x"}]}, filename="b")


def test_resolve_substitutes_and_skips(tmp_path: Path, monkeypatch) -> None:
    """Tokens bind, existing files skip, newest glob resolves."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "sessions").mkdir()
    (tmp_path / "sessions" / "scan_9.9.9.9.nmap.xml").write_text("<x/>", encoding="utf-8")
    (tmp_path / "playbooks").mkdir()
    (tmp_path / "playbooks" / "attack_plan_old.yaml").write_text("old", encoding="utf-8")
    newest = tmp_path / "playbooks" / "attack_plan_new.yaml"
    newest.write_text("new", encoding="utf-8")
    os.utime(newest, (os.path.getatime(str(newest)) + 10, os.path.getmtime(str(newest)) + 10))
    chain = get("apt_chain")
    assert chain is not None
    resolved = chain.resolve({"playbook": "rocke", "target": "9.9.9.9"})
    by_run = {step["run"]: step for step in resolved}
    assert by_run["assign target 9.9.9.9"]["skipped"] is False
    assert by_run["lazynmap 9.9.9.9"]["skipped"] is True
    assert by_run["apt_playbook validate rocke"]["skipped"] is False
    plan_step = [s for s in resolved if s["run"].startswith("attack_plan ")]
    assert len(plan_step) == 1 and plan_step[0]["run"].endswith("attack_plan_new.yaml")
    assert plan_step[0]["skipped"] is False


def test_resolve_flags_unresolved_tokens() -> None:
    """Steps with unknown tokens never execute silently."""
    chain = get("apt_chain")
    assert chain is not None
    resolved = chain.resolve({"playbook": "rocke"})
    assert any(step["skipped"] and "unresolved token" in step["reason"] for step in resolved)


def test_chain_yaml_matches_skill_contract() -> None:
    """The YAML file itself parses and round-trips through the loader."""
    raw = yaml.safe_load((_ROOT / "chains" / "apt_chain.yaml").read_text(encoding="utf-8"))
    assert validate_chain(raw, filename="apt_chain") == []
    assert load_all()["apt_chain"].defaults.get("playbook") == "rocke"


def test_extends_inherits_steps_and_merges_defaults(tmp_path: Path) -> None:
    """A child chain runs parent steps with its own playbook default."""
    import yaml as _yaml

    from modules.chain_registry import get as _get

    parent = {
        "name": "base_demo",
        "description": "parent",
        "enabled": True,
        "defaults": {"playbook": "base_pb", "target": "t"},
        "steps": [{"run": "echo {playbook} {target}"}, {"run": "echo tail"}],
    }
    child = {
        "name": "child_demo",
        "description": "child",
        "enabled": True,
        "extends": "base_demo",
        "defaults": {"playbook": "child_pb"},
    }
    (tmp_path / "base_demo.yaml").write_text(_yaml.dump(parent), encoding="utf-8")
    (tmp_path / "child_demo.yaml").write_text(_yaml.dump(child), encoding="utf-8")
    loaded = _get("child_demo", tmp_path)
    assert loaded is not None and len(loaded.steps) == 2
    assert loaded.defaults["playbook"] == "child_pb"
    resolved = loaded.resolve({"target": "9.9.9.9"})
    assert resolved[0]["run"] == "echo child_pb 9.9.9.9"
    assert resolved[0]["skipped"] is False


def test_extends_cycle_and_unknown_parent_rejected(tmp_path: Path) -> None:
    """Cycles fail validation; unknown parents fail validation and load."""
    import yaml as _yaml

    from modules.chain_registry import load_all as _load_all
    from modules.chain_registry import validate_chain as _validate

    assert _validate({"name": "a", "extends": "a"}, filename="a")
    assert _validate({"name": "a", "extends": "ghost"}, filename="a", chains_dir=tmp_path)
    lonely = {"name": "lonely", "extends": "ghost", "enabled": True}
    (tmp_path / "lonely.yaml").write_text(_yaml.dump(lonely), encoding="utf-8")
    assert "lonely" not in _load_all(tmp_path)


def test_disabled_chains_skip_but_stay_visible(tmp_path: Path) -> None:
    """Disabled files never execute, but scan_all still lists them."""
    import yaml as _yaml

    from modules.chain_registry import get as _get
    from modules.chain_registry import scan_all as _scan_all
    from modules.chain_registry import set_enabled as _set_enabled

    doc = {"name": "off_demo", "enabled": True, "steps": [{"run": "echo hi"}]}
    (tmp_path / "off_demo.yaml").write_text(_yaml.dump(doc), encoding="utf-8")
    assert _get("off_demo", tmp_path) is not None
    assert _set_enabled("off_demo", False, tmp_path) is True
    assert _get("off_demo", tmp_path) is None
    rows = _scan_all(tmp_path)
    assert any(r["name"] == "off_demo" and r["enabled"] is False for r in rows)
    assert _set_enabled("off_demo", True, tmp_path) is True
    assert _get("off_demo", tmp_path) is not None


def test_generate_for_playbook_roundtrip(tmp_path: Path) -> None:
    """Generated per-APT files pin the engine key and inherit steps."""
    import yaml as _yaml

    from modules.chain_registry import generate_for_playbook as _gen

    path = _gen("rocke", apt_display="Rocke", chains_dir=tmp_path)
    assert path.name == "apt_rocke.yaml"
    raw = _yaml.safe_load(path.read_text(encoding="utf-8"))
    assert raw["extends"] == "apt_chain" and raw["defaults"] == {"playbook": "rocke"}
    try:
        _gen("rocke", chains_dir=tmp_path)
    except FileExistsError:
        pass
    else:
        raise AssertionError("overwrite without flag must fail")
    assert _gen("rocke", chains_dir=tmp_path, overwrite=True).exists()
