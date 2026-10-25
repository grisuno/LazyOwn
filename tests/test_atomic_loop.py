"""Atomic emulation inside the autonomous loop (registry + playbooks)."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.apt_playbooks import AptPlaybook, AptPlaybookEngine, PhaseStep  # noqa: E402
from modules.atomic_resolver import AtomicResolver  # noqa: E402
from modules.auto_registry import propose_intents, steps_for, verbs_for  # noqa: E402

_GUID = "f3132740-55bc-48c4-bcc0-758a459cd027"


def _fixture_atomics(root: Path) -> Path:
    """Minimal synthetic atomics tree with one technique."""
    atomics = root / "atomics"
    (atomics / "T1059.001").mkdir(parents=True)
    (atomics / "T1059.001" / "T1059.001.yaml").write_text(
        yaml.dump(
            {
                "attack_technique": "T1059.001",
                "atomic_tests": [
                    {
                        "auto_generated_guid": _GUID,
                        "name": "Mimikatz",
                        "description": "Dump creds",
                        "supported_platforms": ["windows"],
                        "executor": {"name": "powershell", "command": "mimikatz"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return atomics


def test_steps_for_explicit_atomic_intent() -> None:
    """Loop agents staging via explicit auto form get a runnable line."""
    assert steps_for("auto atomic_tests T1059.001 on windows", "10.0.0.5") == [
        "atomic_tests T1059.001 --platform windows --non-interactive"
    ]
    assert steps_for("auto atomic_gen T1059.001", "10.0.0.5") == [
        "atomic_gen T1059.001 --non-interactive"
    ]


def test_steps_for_keyword_atomic_intent() -> None:
    """Emulation goals resolve to staging lines; technique-less ones abstain."""
    assert steps_for("emulate T1003 adversary emulation on linux", "10.0.0.5") == [
        "atomic_tests T1003 --platform linux --non-interactive"
    ]
    assert steps_for("emulate adversary emulation techniques", "10.0.0.5") is None


def test_atomic_lines_are_always_non_interactive() -> None:
    """Loop-produced atomic lines never block on input()."""
    for intent in (
        "auto atomic_tests T1003",
        "run adversary emulation TTP chain T1059.001",
        "atomic_gen T1547.001 windows",
    ):
        lines = steps_for(intent, "10.0.0.5")
        assert lines is not None and all("--non-interactive" in line for line in lines)


def test_planner_discovers_atomic_verbs() -> None:
    """Emulation goals surface atomic verbs to the planner."""
    assert "atomic_tests" in [v.verb for v in verbs_for("adversary emulation ttp chain")]
    assert "auto atomic_tests" in propose_intents("emulate techniques with atomic tests", "10.0.0.5")


def test_steps_for_explicit_playbook_intent() -> None:
    """Loop agents can generate a named APT plan with one line."""
    assert steps_for("auto apt_playbook run rocke", "172.17.0.2") == ["apt_playbook run rocke"]
    assert steps_for("auto apt_playbook", "172.17.0.2") is None


def test_steps_for_keyword_playbook_intent() -> None:
    """Any '<name> playbook' intent resolves; bare mentions abstain."""
    assert steps_for("emulate the rocke playbook against linux", "172.17.0.2") == [
        "apt_playbook run rocke"
    ]
    assert steps_for("run the apt29 playbook", "172.17.0.2") == ["apt_playbook run apt29"]
    assert steps_for("emulate apt playbook techniques", "172.17.0.2") is None


def test_rocke_playbook_resolves_linux_chain() -> None:
    """Rocke playbook loads, validates, and every staged technique exists."""
    engine = AptPlaybookEngine(playbook_dir="playbooks")
    pb = engine.get("rocke")
    assert pb is not None and "linux" in pb.platforms
    tids = [ph.technique_id for ph in pb.phases]
    assert "T1210" in tids and "T1053.003" in tids
    result = engine.validate(pb, atomic_path="external/.exploit/atomic-red-team/atomics")
    assert result["atomic_tests_found"] >= 10
    assert {m["atomic_id"] for m in result["missing"]} <= {"T1190", "T1210"}


def test_planner_discovers_playbook_verb() -> None:
    """Playbook goals surface the apt_playbook verb to the planner."""
    assert "apt_playbook" in [v.verb for v in verbs_for("run the apt playbook for rocke")]
    assert "auto apt_playbook" in propose_intents("emulate apt playbook rocke", "172.17.0.2")


def test_loop_reaches_apt_chain_end_to_end() -> None:
    """The autonomous loop's full path: goal -> intent -> shell line.

    This is the contract the loop depends on: the planner proposes an
    ``auto apt_chain`` intent from an emulation goal, steps_for binds
    playbook + target, and the line routes through the shell executor.
    If any link breaks, the loop silently drops APT emulation.
    """
    from modules.auto_registry import is_routable_command, verb_enabled, verb_gap

    goal = "run the full apt chain end-to-end emulation on 172.17.0.2"
    intents = propose_intents(goal, "172.17.0.2")
    chain_intents = [i for i in intents if "apt_chain" in i]
    assert chain_intents, f"planner never proposes apt_chain for: {goal}"
    assert verb_enabled("apt_chain") and not verb_gap("apt_chain")
    for intent in chain_intents:
        lines = steps_for(intent, "172.17.0.2")
        assert lines, f"no steps for intent: {intent}"
        for line in lines:
            assert is_routable_command(line), f"loop cannot execute: {line}"
    assert any("apt_chain" in (steps_for(i, "172.17.0.2") or [""])[0] for i in chain_intents)


def test_apt_chain_binds_playbook_and_target() -> None:
    """Explicit chain intents bind both slots; explicit IP wins."""
    assert steps_for("auto apt_chain rocke 172.17.0.2", "10.0.0.5") == [
        "apt_chain rocke 172.17.0.2"
    ]
    assert steps_for("auto apt_chain apt29 10.0.0.9", "") == ["apt_chain apt29 10.0.0.9"]
    assert steps_for("auto apt_chain 172.17.0.2", "") == ["apt_chain rocke 172.17.0.2"]
    assert steps_for("auto apt_chain", "172.17.0.2") == ["apt_chain rocke 172.17.0.2"]


def test_apt_chain_keyword_never_invents_playbook() -> None:
    """Free-text binds IPs and <name> playbook forms only, never filler."""
    assert steps_for("run the full apt chain", "172.17.0.2") == ["apt_chain rocke 172.17.0.2"]
    assert steps_for("run the full apt chain on 10.0.0.9", "172.17.0.2") == [
        "apt_chain rocke 10.0.0.9"
    ]
    assert steps_for("prove the chain with the apt29 playbook", "172.17.0.2") == [
        "apt_chain apt29 172.17.0.2"
    ]


def test_apt_chain_line_routes_via_shell() -> None:
    """Every produced chain line must execute through the shell."""
    from modules.auto_registry import is_routable_command

    for text, target in [
        ("auto apt_chain rocke 172.17.0.2", ""),
        ("run the full apt chain", "172.17.0.2"),
    ]:
        lines = steps_for(text, target)
        assert lines and all(is_routable_command(line) for line in lines)


def test_planner_discovers_apt_chain_verb() -> None:
    """Chain goals surface apt_chain to the planner."""
    assert "apt_chain" in [v.verb for v in verbs_for("run the full apt chain end-to-end")]
    assert "auto apt_chain 172.17.0.2" in propose_intents("full apt chain", "172.17.0.2")


def test_validate_resolves_technique_ids(
    tmp_path: Path, monkeypatch) -> None:
    """Playbook T-IDs validate through the resolver, not just GUIDs."""
    atomics = _fixture_atomics(tmp_path)
    monkeypatch.setattr(
        "modules.atomic_resolver._resolver",
        AtomicResolver(atomics),
        raising=False,
    )
    engine = AptPlaybookEngine.__new__(AptPlaybookEngine)
    pb = AptPlaybook(
        apt_name="TestAPT",
        phases=[
            PhaseStep(name="execution", technique_id="T1059.001", atomic_tests=[]),
        ],
    )
    pb.phases[0].atomic_tests = [
        type("Ref", (), {"atomic_id": "T1059.001", "name": "Mimikatz"})(),
        type("Ref", (), {"atomic_id": _GUID, "name": "Mimikatz"})(),
        type("Ref", (), {"atomic_id": "NOPE", "name": "Bogus"})(),
    ]
    result = engine.validate(pb, atomic_path=str(atomics))
    assert result["atomic_tests_found"] == 2
    assert result["atomic_tests_missing"] == 1
    assert result["found"][0]["resolved_guid"] == _GUID
    assert result["missing"][0]["atomic_id"] == "NOPE"


def test_atomic_shell_never_interactive_from_loop() -> None:
    """Loop-produced shell lines verify only; REPL needs an explicit flag."""
    from modules.auto_registry import is_routable_command

    lines = steps_for("auto atomic_shell 172.17.0.2", "172.17.0.2")
    assert lines == ["atomic_shell 172.17.0.2"]
    assert all(is_routable_command(line) for line in lines)
    assert "atomic_shell" in [v.verb for v in verbs_for("drop into an interactive shell now")]


def test_atomic_clean_routes_and_never_autofires() -> None:
    """Cleanup resolves explicitly; hard mode needs the literal flag."""
    lines = steps_for("auto atomic_clean 172.17.0.2", "172.17.0.2")
    assert lines == ["atomic_clean 172.17.0.2"] and "--hard" not in lines[0]
    assert "atomic_clean" in [v.verb for v in verbs_for("cleanup artefacts from the lab")]
