"""apt_chain admin & run options BDD contract.

Given a registered command set, When operators parse, list, validate,
dry-run, branch, gate or resume chains, Then every flag is honored
loudly and unknown flags fail instead of being swallowed.
"""

from __future__ import annotations

import builtins
import json
from pathlib import Path

import cmd2
import yaml

from cli.apt_chain_support import parse_chain_args, select_step_ids
from modules import chain_registry
from modules.chain_registry import Chain, ChainStep
from modules.chain_state import checkpoint_dir, load_checkpoint


def _make_shell():
    """Return a minimal registered shell."""
    from cli.commands.command_and_control_migrated import CommandAndControlMigratedCommandSet

    class _Set(CommandAndControlMigratedCommandSet):
        """Command set under test."""

    class _Shell(cmd2.Cmd):
        """Minimal registered shell with the params a chain needs."""

        def __init__(self) -> None:
            super().__init__(allow_cli_args=False)
            self.params = {"rhost": "10.0.0.5", "lhost": "127.0.0.1", "lport": "4444"}
            self.register_command_set(_Set())

    return _Shell()


def _write_chain(tmp_path, name: str, steps: list[dict], enabled: bool | None = None) -> None:
    """Write one chain file into the command registry."""
    document = {"name": name, "version": 2, "steps": steps}
    if enabled is not None:
        document["enabled"] = enabled
    (tmp_path / f"{name}.yaml").write_text(yaml.safe_dump(document), encoding="utf-8")


def _patch_chain_loading(monkeypatch, tmp_path: Path, enabled_name: str = "demo", chain=None):
    """Patch the registry to resolve one in-memory chain by name."""
    monkeypatch.setattr(chain_registry, "CHAINS_DIR", tmp_path)
    monkeypatch.setattr(
        chain_registry,
        "get",
        lambda name, chains_dir=None: chain if name == enabled_name else None,
    )


def test_parse_flags_and_unknown_flag_fails_loudly():
    """Given an apt_chain line, When parsing, Then options bind and junk errors."""
    args = parse_chain_args("apt_rocke 172.17.0.2 --var user=admin --json --timeout 90 --dry-run")
    assert args.errors == []
    assert args.positional == ["apt_rocke", "172.17.0.2"]
    assert args.vars == {"user": "admin"}
    assert args.json_out is True and args.timeout == 90.0 and args.dry_run is True
    broken = parse_chain_args("rocke --resume")
    assert any("missing value" in error for error in broken.errors)
    junk = parse_chain_args("rocke --foo bar")
    assert any("--foo" in error for error in junk.errors)
    bad_var = parse_chain_args("rocke --var 9bad=1")
    assert any("--var" in error for error in bad_var.errors)


def test_select_step_ids_supports_step_from_and_to():
    """Given chain steps, When selecting, Then slices bind and unknown ids fail."""
    rich_chain = Chain(
        name="demo",
        steps=[
            ChainStep(id="one", run="a"),
            ChainStep(id="two", run="b"),
            ChainStep(id="three", run="c"),
        ],
    )
    args = parse_chain_args("--step two")
    ids, errors = select_step_ids(rich_chain, args)
    assert ids == {"two"} and errors == []

    args = parse_chain_args("--from-step two")
    ids, errors = select_step_ids(rich_chain, args)
    assert ids == {"two", "three"} and errors == []

    args = parse_chain_args("--from-step one --to-step two")
    ids, errors = select_step_ids(rich_chain, args)
    assert ids == {"one", "two"} and errors == []

    args = parse_chain_args("--from-step nope")
    ids, errors = select_step_ids(rich_chain, args)
    assert errors and "nope" in errors[0]


def test_admin_list_validate_and_enable_disable(tmp_path, monkeypatch, capsys):
    """Given admin actions, When invoked, Then rows print and flags flip."""
    _write_chain(tmp_path, "demo", [{"id": "one", "run": "echo one"}], enabled=True)
    shell = _make_shell()
    monkeypatch.setattr(chain_registry, "CHAINS_DIR", tmp_path)
    shell.do_apt_chain("list --json")
    payload, _ = json.JSONDecoder().raw_decode(capsys.readouterr().out.strip())
    rows = payload["rows"]
    assert [row["name"] for row in rows] == ["demo"]

    capsys.readouterr()
    shell.do_apt_chain("validate demo")
    assert "demo" in capsys.readouterr().out

    capsys.readouterr()
    shell.do_apt_chain("disable demo")
    document = yaml.safe_load((tmp_path / "demo.yaml").read_text(encoding="utf-8"))
    assert document["enabled"] is False

    capsys.readouterr()
    shell.do_apt_chain("enable demo")
    document = yaml.safe_load((tmp_path / "demo.yaml").read_text(encoding="utf-8"))
    assert document["enabled"] is True
    assert capsys.readouterr().out.strip()


def test_admin_missing_chain_and_bad_input_fail(tmp_path, monkeypatch, capsys):
    """Given broken admin input, When invoked, Then the failure names the problem."""
    shell = _make_shell()
    monkeypatch.setattr(chain_registry, "CHAINS_DIR", tmp_path)
    capsys.readouterr()
    shell.do_apt_chain("show nope_chain")
    assert "not found" in capsys.readouterr().out
    shell.do_apt_chain("resume")
    assert "resume <run_id>" in capsys.readouterr().out


def test_run_dry_run_json_output(tmp_path, monkeypatch, capsys):
    """Given a chain, When dry-run --json, Then steps print statuses and no exec."""
    _write_chain(
        tmp_path,
        "demo",
        [{"id": "one", "run": "echo one"}, {"id": "two", "run": "echo {target}"}],
    )
    chain = chain_registry.load_all(tmp_path)["demo"]
    shell = _make_shell()
    _patch_chain_loading(monkeypatch, tmp_path, "demo", chain)
    monkeypatch.setattr("modules.outcome_bus.record_event", lambda **kwargs: {})
    monkeypatch.chdir(tmp_path)
    capsys.readouterr()
    shell.do_apt_chain("demo 10.9.9.9 --dry-run --json --no-checkpoint")
    payload, _ = json.JSONDecoder().raw_decode(capsys.readouterr().out.strip())
    assert payload["name"] == "demo"
    assert [step["status"] for step in payload["steps"]] == ["dry-run", "dry-run"]


def test_run_checkpoints_and_resume(tmp_path, monkeypatch, capsys):
    """Given an interrupted run, When resuming, Then done steps resume skipped."""
    _write_chain(
        tmp_path,
        "demo",
        [
            {"id": "first", "run": "echo first", "capture": "word"},
            {"id": "second", "run": "python3 -c \"import sys; sys.exit(1)\""},
            {"id": "third", "run": "echo third {word}"},
        ],
    )
    chain = chain_registry.load_all(tmp_path)["demo"]
    shell = _make_shell()
    _patch_chain_loading(monkeypatch, tmp_path, "demo", chain)
    monkeypatch.setattr("modules.outcome_bus.record_event", lambda **kwargs: {})
    monkeypatch.chdir(tmp_path)
    capsys.readouterr()
    shell.do_apt_chain("demo 10.9.9.9")
    directory = checkpoint_dir()
    run_ids = [path.stem for path in directory.glob("*.json")] if directory.is_dir() else []
    assert run_ids

    from modules.chain_state import write_checkpoint

    write_checkpoint(
        directory,
        {
            "run_id": "resume_me",
            "chain": "demo",
            "target": "10.9.9.9",
            "state": "aborted",
            "variables": {"word": "first"},
            "captured_keys": ["word"],
            "steps": [{"id": "first", "status": "ok"}, {"id": "second", "status": "failed"}],
            "next_index": 1,
        },
    )
    shell.do_apt_chain("resume resume_me --no-checkpoint")
    out = capsys.readouterr().out
    assert "resumed (already completed)" in out
    assert load_checkpoint(directory, "resume_me") is not None


def test_confirm_gate_auto_approves_in_autonomous_mode(tmp_path, monkeypatch, capsys):
    """Given a confirm step, When autonomous, Then it auto-approves and runs."""
    _write_chain(tmp_path, "demo", [{"id": "guarded", "run": "echo guarded", "confirm": True}])
    chain = chain_registry.load_all(tmp_path)["demo"]
    shell = _make_shell()
    _patch_chain_loading(monkeypatch, tmp_path, "demo", chain)
    monkeypatch.setattr("modules.outcome_bus.record_event", lambda **kwargs: {})
    monkeypatch.setenv("LAZYOWN_AUTONOMOUS", "1")
    monkeypatch.chdir(tmp_path)
    capsys.readouterr()
    shell.do_apt_chain("demo 10.9.9.9 --no-checkpoint")
    out = capsys.readouterr().out
    assert "auto-approved confirm step guarded" in out
    assert "ok: echo guarded" in out
    monkeypatch.delenv("LAZYOWN_AUTONOMOUS")


def test_confirm_gate_denies_when_operator_refuses(tmp_path, monkeypatch, capsys):
    """Given a confirm step, When operator says no, Then the chain denies and aborts."""
    _write_chain(tmp_path, "demo", [{"id": "guarded", "run": "echo guarded", "confirm": True}])
    chain = chain_registry.load_all(tmp_path)["demo"]
    shell = _make_shell()
    _patch_chain_loading(monkeypatch, tmp_path, "demo", chain)
    monkeypatch.setattr("modules.outcome_bus.record_event", lambda **kwargs: {})
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "n")
    monkeypatch.chdir(tmp_path)
    capsys.readouterr()
    shell.do_apt_chain("demo 10.9.9.9 --no-checkpoint")
    out = capsys.readouterr().out
    assert "approval denied" in out
    assert "aborted" in out


def test_engagement_tokens_resolved_from_fact_store(monkeypatch, tmp_path):
    """Given fact-store findings, When building tokens, Then the values bind."""
    from skills import lazyown_facts as facts_engine

    hf = facts_engine.HostFacts(host="10.9.9.9")
    hf.services.extend(
        [
            facts_engine.ServiceFact(
                host="10.9.9.9", port=22, protocol="tcp", service="ssh", product="openssh", version="", state="open"
            ),
            facts_engine.ServiceFact(
                host="10.9.9.9", port=80, protocol="tcp", service="http", product="nginx", version="", state="open"
            ),
        ]
    )
    hf.credentials.append(
        facts_engine.CredentialFact(host="10.9.9.9", username="svc", password="hunter2", source_file="")
    )
    hf.os_hint = "Ubuntu 22.04"

    class FakeStore:
        """Fake fact store returning one host."""

        def __init__(self, *args, **kwargs) -> None:
            return None

        @staticmethod
        def parse_all(*args, **kwargs) -> dict:
            """Do nothing."""
            return {}

        @staticmethod
        def get_host(host):
            """Return the fake host."""
            return hf if host == "10.9.9.9" else None

    monkeypatch.setattr(facts_engine, "FactStore", FakeStore)
    monkeypatch.chdir(tmp_path)
    from modules.chain_tokens import build_tokens

    tokens = build_tokens("10.9.9.9")
    assert tokens["ports"] == "22,80"
    assert tokens["svc_port"] == "22"
    assert "ssh" in tokens["services"] and "http" in tokens["services"]
    assert tokens["username"] == "svc" and tokens["password"] == "hunter2"
    assert tokens["os"] == "Ubuntu 22.04"
    assert build_tokens("") == {}


def test_playbook_overrides_base_chain(tmp_path, monkeypatch, capsys):
    """Given --playbook, When running, Then the chain pins the playbook token."""
    _write_chain(tmp_path, "demo", [{"id": "pb", "run": "echo playbook={playbook} dry=1"}])
    chain = chain_registry.load_all(tmp_path)["demo"]
    shell = _make_shell()
    _patch_chain_loading(monkeypatch, tmp_path, "demo", chain)
    monkeypatch.setattr("modules.outcome_bus.record_event", lambda **kwargs: {})
    monkeypatch.chdir(tmp_path)
    capsys.readouterr()
    shell.do_apt_chain("demo 10.9.9.9 --playbook rocke --no-checkpoint")
    assert "playbook=rocke" in capsys.readouterr().out


def test_step_filtering_drops_out_of_scope_steps(tmp_path, monkeypatch, capsys):
    """Given --step, When running, Then only selected steps execute."""
    _write_chain(
        tmp_path,
        "demo",
        [
            {"id": "one", "run": "echo one"},
            {"id": "two", "run": "echo two"},
            {"id": "three", "run": "echo three && exit 9"},
        ],
    )
    chain = chain_registry.load_all(tmp_path)["demo"]
    shell = _make_shell()
    _patch_chain_loading(monkeypatch, tmp_path, "demo", chain)
    monkeypatch.setattr("modules.outcome_bus.record_event", lambda **kwargs: {})
    monkeypatch.chdir(tmp_path)
    capsys.readouterr()
    shell.do_apt_chain("demo 10.9.9.9 --step one,two --no-checkpoint --json")
    payload, _ = json.JSONDecoder().raw_decode(capsys.readouterr().out.strip())
    assert [step["id"] for step in payload["steps"]] == ["one", "two"]
    assert payload["filtered"] == 1


def test_unknown_run_flags_fail_loudly(tmp_path, monkeypatch, capsys):
    """Given an unknown run flag, When parsing, Then nothing executes."""
    shell = _make_shell()
    _patch_chain_loading(monkeypatch, tmp_path, "demo", None)
    capsys.readouterr()
    shell.do_apt_chain("demo 10.0.0.9 --totally-unknown-flag")
    assert "unknown option" in capsys.readouterr().out
