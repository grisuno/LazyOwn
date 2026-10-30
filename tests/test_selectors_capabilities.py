"""Capability selector contracts: playbook, adversary and atomic strategies.

Each fires only when the objective names its capability, so the cascade stays
conservative. External listings (playbooks, chains, adversary files) are
injected so no filesystem or registry state is required.
"""

from __future__ import annotations

from modules.selectors.adversary import AdversarySelector
from modules.selectors.atomic import AtomicSelector
from modules.selectors.base import SelectionContext
from modules.selectors.playbook import PlaybookSelector


def _ctx(goal: str = "", phase: str = "exploit", **extra) -> SelectionContext:
    """Build a context with a goal and optional extra inputs."""
    payload = {"goal": goal}
    payload.update(extra)
    return SelectionContext(target="10.0.0.9", phase=phase, os_hint="linux", extra=payload)


def test_playbook_fires_when_goal_names_actor(monkeypatch):
    """Given a goal naming apt28 and a matching chain, Then the actor chain is proposed."""
    import modules.apt_playbooks as pb
    import modules.chain_registry as cr

    monkeypatch.setattr(
        pb.AptPlaybookEngine, "list_playbooks",
        lambda self: [{"apt_name": "apt28", "aliases": ["fancybear"]}], raising=False,
    )
    monkeypatch.setattr(cr, "get", lambda name, *a, **k: object() if name == "apt_apt28" else None)
    decision = PlaybookSelector().propose(_ctx("emulate apt28 against the host"))
    assert decision is not None
    assert decision.command == "apt_chain apt_apt28 10.0.0.9"
    assert decision.source == "playbook"


def test_playbook_abstains_without_actor(monkeypatch):
    """Given a goal naming no actor, Then the selector abstains."""
    import modules.apt_playbooks as pb

    monkeypatch.setattr(
        pb.AptPlaybookEngine, "list_playbooks",
        lambda self: [{"apt_name": "apt28", "aliases": []}], raising=False,
    )
    assert PlaybookSelector().propose(_ctx("gain initial access")) is None


def test_adversary_fires_when_goal_names_profile(monkeypatch):
    """Given a goal naming an adversary profile, Then adversary_yaml is proposed."""
    import modules.selectors.adversary as adv

    monkeypatch.setattr(adv.glob, "glob", lambda pattern: ["lazyadversaries/amsi.yaml", "lazyadversaries/infect.yaml"])
    decision = AdversarySelector().propose(_ctx("run the infect adversary profile"))
    assert decision is not None
    assert decision.command == "adversary_yaml infect"
    assert decision.source == "adversary"


def test_adversary_abstains_without_profile(monkeypatch):
    """Given a goal naming no profile, Then the selector abstains."""
    import modules.selectors.adversary as adv

    monkeypatch.setattr(adv.glob, "glob", lambda pattern: ["lazyadversaries/amsi.yaml"])
    assert AdversarySelector().propose(_ctx("escalate privileges")) is None


def test_atomic_fires_on_technique_ids_in_postexp():
    """Given technique ids in a post-foothold phase, Then atomic_emulate is proposed."""
    decision = AtomicSelector().propose(_ctx("emulate T1059.001 and T1082", phase="postexp"))
    assert decision is not None
    assert decision.command == "atomic_emulate --target 10.0.0.9 --techniques T1059.001,T1082"
    assert decision.source == "atomic"


def test_atomic_honours_explicit_techniques_extra():
    """Given techniques passed via extra, Then they drive the emulation."""
    decision = AtomicSelector().propose(_ctx("", phase="lateral", techniques=["T1021", "T1021"]))
    assert decision is not None
    assert decision.command == "atomic_emulate --target 10.0.0.9 --techniques T1021"


def test_atomic_abstains_in_recon_phase():
    """Given technique ids but a pre-foothold phase, Then the selector abstains."""
    assert AtomicSelector().propose(_ctx("emulate T1059", phase="recon")) is None


def test_atomic_abstains_without_techniques():
    """Given no technique ids, Then the selector abstains."""
    assert AtomicSelector().propose(_ctx("do privilege escalation", phase="privesc")) is None
