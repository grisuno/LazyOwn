"""Tests for the LazyscriptSelector.

The selector turns a curated lazyscript recipe into a routable
``lazyscript <name>.ls`` proposal when its name tokens match the goal or
the discovered services, and abstains otherwise.
"""

from __future__ import annotations

import pytest

from modules.selection.base import SelectionContext
from modules.selection.lazyscript import LazyscriptSelector


@pytest.fixture()
def scripts_dir(tmp_path):
    """Create a small lazyscripts catalogue for the selector."""
    for name in ("smb.ls", "certipy_ad.ls", "cloud_enum.ls", "startup.ls", "lazyquit.ls"):
        (tmp_path / name).write_text("ping\n", encoding="utf-8")
    return tmp_path


def _ctx(goal="", services=(), target="10.0.0.5", exclude=()):
    return SelectionContext(
        target=target,
        phase="enum",
        services=tuple(services),
        exclude=frozenset(exclude),
        extra={"goal": goal},
    )


def test_matches_service_token(scripts_dir):
    selector = LazyscriptSelector(scripts_dir=scripts_dir)
    decision = selector.propose(_ctx(services=["smb"]))
    assert decision is not None
    assert decision.command == "lazyscript smb.ls"
    assert decision.source == "lazyscript"


def test_matches_goal_token(scripts_dir):
    selector = LazyscriptSelector(scripts_dir=scripts_dir)
    decision = selector.propose(_ctx(goal="enumerate certipy_ad on the domain"))
    assert decision is not None
    assert decision.command == "lazyscript certipy_ad.ls"


def test_abstains_without_match(scripts_dir):
    selector = LazyscriptSelector(scripts_dir=scripts_dir)
    assert selector.propose(_ctx(goal="exfiltrate database")) is None


def test_skips_lifecycle_scripts(scripts_dir):
    selector = LazyscriptSelector(scripts_dir=scripts_dir)
    assert selector.propose(_ctx(goal="startup")) is None
    assert selector.propose(_ctx(goal="lazyquit now")) is None


def test_requires_target(scripts_dir):
    selector = LazyscriptSelector(scripts_dir=scripts_dir)
    ctx = SelectionContext(target="", phase="enum", services=("smb",), extra={})
    assert selector.propose(ctx) is None


def test_excluded_command_abstains(scripts_dir):
    selector = LazyscriptSelector(scripts_dir=scripts_dir)
    decision = selector.propose(_ctx(services=["smb"], exclude={"lazyscript smb.ls"}))
    assert decision is None


def test_missing_dir_is_safe(tmp_path):
    selector = LazyscriptSelector(scripts_dir=tmp_path / "nope")
    assert selector.propose(_ctx(services=["smb"])) is None


def test_emitted_command_is_routable(scripts_dir):
    from modules.auto_registry import is_routable_command

    selector = LazyscriptSelector(scripts_dir=scripts_dir)
    decision = selector.propose(_ctx(services=["smb"]))
    assert decision is not None
    assert is_routable_command(decision.command)
