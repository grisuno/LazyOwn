"""Tests for the ModuleSelector over the shared module registry bridge.

Uses a synthetic registry (same fixture shape as
``tests/test_module_registry_bridge.py``) so the unit scope stays fast
and deterministic against the real matching logic.
"""

from __future__ import annotations

import pytest

import modules.module_registry as mr
from modules.selection.base import SelectionContext
from modules.selection.module import ModuleSelector


@pytest.fixture
def registry(tmp_path, monkeypatch):
    """A synthetic ModuleRegistry with one addon and one playbook entry."""
    addons = tmp_path / "lazyaddons"
    addons.mkdir(parents=True, exist_ok=True)
    (addons / "lazy_hydra.yaml").write_text(
        "name: lazy_hydra\ndescription: brute force\nenabled: true\n",
        encoding="utf-8",
    )
    playbooks = tmp_path / "playbooks"
    playbooks.mkdir(parents=True, exist_ok=True)
    (playbooks / "rocke.json").write_text(
        '{"name": "rocke", "description": "ransomware emulation"}', encoding="utf-8"
    )
    reg = mr.ModuleRegistry(tmp_path)
    reg.scan()

    from modules import lazy_osinfer

    monkeypatch.setattr(lazy_osinfer, "host_os_for_target", lambda target: "", raising=False)
    monkeypatch.setattr(mr.ModuleRegistry, "get_instance", classmethod(lambda cls, base_dir=None: reg))
    return reg


def _ctx(goal: str = "", target: str = "10.66.44.7", services=(), exclude=()):
    return SelectionContext(
        target=target,
        phase="enum",
        services=tuple(services),
        exclude=frozenset(exclude),
        extra={"goal": goal},
    )


class TestModuleSelector:
    def test_goal_token_raises_addon(self, registry):
        story = "a goal naming a lazyaddon module proposes its run line"
        decision = ModuleSelector().propose(_ctx(goal="brute force with lazy_hydra against smb"))
        assert decision is not None and decision.source == "module", story
        assert "lazy_hydra" in decision.command, story

    def test_playbook_entry_routes_apt_playbook(self, registry):
        story = "a playbook-named goal proposes apt_playbook run"
        decision = ModuleSelector().propose(_ctx(goal="emulate the rocke playbook"))
        assert decision is not None, story
        assert decision.command == "apt_playbook run rocke", story

    def test_lazy_addon_normalised_to_routable_verb(self, registry):
        story = "registry 'lazy addon' lines are normalised to the routable verb"
        decision = ModuleSelector().propose(_ctx(goal="brute force with lazy_hydra"))
        assert decision is not None, story
        assert decision.command.startswith("lazy_addon "), story

    def test_routable_through_loop(self, registry):
        story = "the emitted command survives the real loop routing gate"
        from modules.auto_registry import is_routable_command

        decision = ModuleSelector().propose(_ctx(goal="brute force with lazy_hydra"))
        assert decision is not None, story
        assert is_routable_command(decision.command), story

    def test_no_match_abstains(self, registry):
        story = "a goal with no registry mention yields no proposal"
        assert ModuleSelector().propose(_ctx(goal="watch the clouds drift by")) is None, story

    def test_requires_target(self, registry):
        story = "no target means no proposal"
        ctx = SelectionContext(target="", phase="enum", extra={"goal": "lazy_hydra"})
        assert ModuleSelector().propose(ctx) is None, story

    def test_exclude_skips_taken_intent(self, registry):
        story = "an already-queued intent falls through to the next candidate"
        decision = ModuleSelector().propose(
            _ctx(goal="brute force with lazy_hydra against smb", exclude={"lazy_addon lazy_hydra 10.66.44.7"})
        )
        assert decision is None or decision.command != "lazy_addon lazy_hydra 10.66.44.7", story
