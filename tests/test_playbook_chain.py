"""Playbook lowering: phases[].steps[] actions and atomic tests become
validated chains executed by the one runner."""

from __future__ import annotations

from modules.apt_playbooks import AptPlaybook, PlaybookAction
from modules.chain_registry import validate_chain
from modules.playbook_admin import validate_playbook
from modules.playbook_chain import playbook_to_chain, slugify, write_playbook_chain


def _playbook(**overrides) -> AptPlaybook:
    from modules.apt_playbooks import AtomicTestRef, PhaseStep

    base = AptPlaybook(
        apt_name="Rocke",
        description="demo actor",
        platforms=["linux"],
        phases=[
            PhaseStep(
                name="execution",
                technique_id="T1059.004",
                technique_name="Unix Shell",
                atomic_tests=[AtomicTestRef(atomic_id="T1059.004", name="shell", manual=False)],
                steps=[
                    PlaybookAction(kind="lazyscript", run="recon_basics.ls", timeout=600),
                    PlaybookAction(kind="lazyaddon", run="nuclei_templates"),
                    PlaybookAction(kind="command", run="curl -s http://{target}/shell.php?cmd=id", sinks=["world_model"]),
                    PlaybookAction(kind="plugin", run="plugin_registered_verb --flag"),
                ],
            )
        ],
    )
    return overrides.get("playbook", base)


def test_slugify_normalizes_playbook_names():
    """Given a spaced name, When slugified, Then chain-safe."""
    assert slugify("APT Rocke-29") == "apt_rocke_29"
    assert slugify("") == "playbook"


def test_playbook_to_chain_maps_every_kind():
    """Given actions of each kind, When lowered, Then each maps to its
    executor verb and keeps pacing/sinks."""
    chain, errors = playbook_to_chain(_playbook(), target="10.0.0.1")
    assert errors == []
    assert chain is not None
    runs = [step.run for step in chain.steps]
    assert runs[0] == "lazyscript recon_basics.ls"
    assert runs[1] == "lazy_addon run nuclei_templates"
    assert runs[2] == "curl -s http://{target}/shell.php?cmd=id"
    assert runs[3] == "plugin_registered_verb --flag"
    assert any(run.startswith("atomic_emulate --target {target} --techniques T1059.004") for run in runs)
    first = chain.steps[0]
    assert first.timeout == 600 and first.id.startswith("execution_")
    third = chain.steps[2]
    assert third.sinks == ["world_model"]
    assert chain.name == "playbook_rocke"
    assert chain.defaults["target"] == "10.0.0.1"


def test_playbook_to_chain_skips_manual_atomic_tests():
    """Given only manual atomic tests, When lowered, Then no emulate step."""
    from modules.apt_playbooks import AtomicTestRef, PhaseStep

    pb = _playbook(
        playbook=AptPlaybook(
            apt_name="Ghost",
            phases=[
                PhaseStep(
                    name="persistence",
                    technique_id="T1053",
                    atomic_tests=[AtomicTestRef(atomic_id="T1053", name="manual only", manual=True)],
                )
            ],
        )
    )
    chain, errors = playbook_to_chain(pb)
    assert chain is None
    assert any("no executable steps" in error for error in errors)


def test_playbook_to_chain_validates_against_registry():
    """Given the lowered raw mapping, When validated, Then registry-clean."""
    chain, errors = playbook_to_chain(_playbook())
    assert errors == []
    from modules.playbook_chain import _chain_to_raw

    assert validate_chain(_chain_to_raw(chain), filename=chain.name, chains_dir=None) == []


def test_playbook_to_chain_stepwise_eligible_when_verbs_routable(monkeypatch):
    """Given all lowered verbs routable, Then the chain is loop-stepwise."""
    import modules.auto_registry as auto_registry
    from modules.chain_loop import stepwise_eligible

    chain, _ = playbook_to_chain(_playbook())
    monkeypatch.setattr(auto_registry, "is_routable_command", lambda line: True)
    ok, reason = stepwise_eligible(chain)
    assert ok is True and reason == ""


def test_write_playbook_chain_round_trips(tmp_path):
    """Given a lowered chain, When written, Then the YAML reloads clean."""
    chain, errors = playbook_to_chain(_playbook())
    assert errors == []
    path = write_playbook_chain(chain, chains_dir=str(tmp_path))
    import yaml

    data = yaml.safe_load(open(path))
    assert data["name"] == "playbook_rocke"
    assert len(data["steps"]) == len(chain.steps)


def test_validate_playbook_accepts_steps_and_rejects_bad_kinds():
    """Given phase steps, Then kinds/run/numeric fields are enforced."""
    good = {
        "apt_name": "demo",
        "phases": [
            {
                "name": "execution",
                "steps": [
                    {"kind": "lazyscript", "run": "recon.ls", "timeout": 600},
                    {"kind": "atomic", "run": "T1059.004"},
                ],
            }
        ],
    }
    assert validate_playbook(good) == []
    bad = {
        "apt_name": "demo",
        "phases": [
            {
                "name": "execution",
                "steps": [
                    {"kind": "wat", "run": "x"},
                    {"kind": "command"},
                    {"kind": "command", "run": "ls", "timeout": -1},
                    {"kind": "command", "run": "ls", "continue_on_error": "yes"},
                    {"kind": "command", "run": "ls", "sinks": "world_model"},
                ],
            }
        ],
    }
    errors = validate_playbook(bad)
    assert any("kind must be one of" in error for error in errors)
    assert any("run is required" in error for error in errors)
    assert any("timeout must be a non-negative" in error for error in errors)
    assert any("continue_on_error must be a boolean" in error for error in errors)
    assert any("sinks must be a list" in error for error in errors)


def test_synth_playbook_flag_lowers_and_writes(tmp_path, monkeypatch):
    """Given --playbook on synth, When resolving, Then a lowered chain file lands."""
    import os

    monkeypatch.chdir(tmp_path)
    from cli.apt_chain_support import parse_chain_args, resolve_admin
    from modules import apt_playbooks
    from modules.apt_playbooks import AptPlaybookEngine

    engine = AptPlaybookEngine.__new__(AptPlaybookEngine)
    engine.playbook_dir = "playbooks"
    engine._playbooks = {"rocke": _playbook()}
    monkeypatch.setattr(apt_playbooks, "AptPlaybookEngine", lambda *a, **k: engine)

    args = parse_chain_args("synth --playbook rocke --target 10.0.0.2")
    assert args.errors == []
    payload = resolve_admin(args)
    assert payload["ok"], payload
    assert payload["name"] == "playbook_rocke" and payload["steps"] >= 4, payload
    assert str(payload["path"]).endswith("playbook_rocke.yaml"), payload
    assert os.path.exists(tmp_path / "chains" / "playbook_rocke.yaml")


def test_synth_playbook_unknown_name_loud(tmp_path, monkeypatch):
    """Given an unknown playbook, When resolving, Then a loud error comes back."""
    from cli.apt_chain_support import parse_chain_args, resolve_admin
    from modules import apt_playbooks

    monkeypatch.setattr(apt_playbooks, "AptPlaybookEngine", lambda *a, **k: (_ for _ in ()).throw(Exception("no dir")))
    args = parse_chain_args("synth --playbook ghost --target 10.0.0.3")
    payload = resolve_admin(args)
    assert not payload["ok"] and "unavailable" in payload.get("error", ""), payload
