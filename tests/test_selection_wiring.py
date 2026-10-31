"""Vertical wiring tests: playbooks, adversaries and apt_chain through the loop.

The shared selector cascade must propose only loop-routable commands, and
the commands the three remaining selectors emit must resolve through the
real routing and the real data libraries (playbooks/{jobberapt,chains},
lazyadversaries, chains/).
"""

from __future__ import annotations

from modules.selection.base import SelectionContext
from modules.selection.registry import propose_next


def _ctx(goal: str, target: str = "10.66.44.7", phase: str = "recon", exclude=()) -> SelectionContext:
    """Build one engagement snapshot for the selectors."""
    return SelectionContext(target=target, phase=phase, exclude=frozenset(exclude), extra={"goal": goal})


class TestPlaybookWiring:
    def test_cascade_names_actor_by_alias(self):
        story = "a goal naming a lazarus alias proposes the lazarus chain"
        decision = propose_next(_ctx("emulate lazarus (hidden cobra) on the target"))
        assert decision is not None and decision.source == "playbook", story
        assert decision.command == "apt_chain apt_lazarusgroup 10.66.44.7", story

    def test_cascade_names_actor_slug(self):
        story = "the apt29 slug names the apt29 chain"
        decision = propose_next(_ctx("run apt29 chain against the target"))
        assert decision is not None and decision.command == "apt_chain apt_apt29 10.66.44.7", story

    def test_generator_stubs_not_the_base_chain(self):
        story = "rocke resolves to apt_rocke, never to the base apt_chain default"
        decision = propose_next(_ctx("emulate rocke group"))
        assert decision is not None and decision.command == "apt_chain apt_rocke 10.66.44.7", story

    def test_unknown_actor_never_runs_a_chain(self):
        story = "a goal without any known actor never proposes a chain run"
        decision = propose_next(_ctx("emulate the fictional red owl crew"))
        assert decision is None or not decision.command.startswith("apt_chain"), story


class TestAdversaryWiring:
    def testProfiles_resolve_to_numeric_ids(self):
        story = "a goal naming a profile proposes the numeric id the verb expects"
        decision = propose_next(_ctx("run malleable beacon implant"))
        assert decision is not None and decision.source == "adversary", story
        assert decision.command == "adversary_yaml 5 l", story

    def test_inject_shellcode_profile(self):
        story = "shellcode goals resolve to the inject_shellcode profile id"
        decision = propose_next(_ctx("inject shellcode into target"))
        assert decision is not None and decision.command == "adversary_yaml 4 l", story

    def test_adverbial_words_do_not_hijack(self):
        story = "implant alone must not steal the proposal from a named profile"
        decision = propose_next(_ctx("nim implant build"))
        assert decision is not None and decision.command == "adversary_yaml 8 l", story


class TestRouting:
    def test_routable_through_loop(self):
        story = "every emitted command survives the real loop routing gate"
        from modules.auto_registry import is_routable_command

        assert is_routable_command("apt_chain apt_lazarusgroup 10.66.44.7"), story
        assert is_routable_command("apt_chain apt_apt29 10.7.7.1"), story
        assert is_routable_command("adversary_yaml 5 l"), story
        assert is_routable_command("lazyintel 10.66.44.7"), story

    def test_lab_env_gate(self, monkeypatch):
        story = "AUTO_CHAIN_SELECTOR_LAB=0 excludes lab chains from the cascade"
        from modules import chain_match

        chain_match._CACHE.update({"rows": [], "ts": 0.0})
        monkeypatch.setenv("AUTO_CHAIN_SELECTOR_LAB", "0")
        rows = chain_match.load_rows(allow_lab=False, ttl=0)
        names = {row["name"] for row in rows}
        assert "apt_ad_lab" not in names and "gym_ad_lab_chain" not in names, story
        assert "apt_lazarusgroup" in names, story
