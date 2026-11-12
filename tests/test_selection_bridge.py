"""Tests for the shared bridge selector.

The bridge selector adapts the LazyOwn bridge catalogue dispatcher into the
shared ``Selector`` protocol so both autonomous runtimes reach the MITRE-mapped
command catalogue as a cascade fallback. The dispatcher is injected through a
fake so no catalogue YAML is read. Every scenario states Given, When, Then.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

import modules.selection.bridge as bridge_mod  # noqa: E402
from modules.selection.base import SelectionContext  # noqa: E402
from modules.selection.bridge import BridgeSelector  # noqa: E402


@dataclass
class _Entry:
    """Catalogue entry double exposing the fields the selector reads."""

    description: str = "SMB enumeration"
    mitre_tactic: str = "TA0007"


class _Dispatcher:
    """Dispatcher double recording calls and returning a scripted result."""

    def __init__(self, result, raise_on=None):
        self._result = result
        self._raise_on = raise_on or set()
        self.calls = []

    def suggest(self, **kwargs):
        self.calls.append(kwargs)
        if kwargs.get("tag_hint") in self._raise_on:
            raise RuntimeError("boom")
        return self._result


def _bind(monkeypatch, dispatcher) -> None:
    """Point the selector's lazy import at the injected dispatcher."""
    monkeypatch.setattr(bridge_mod, "get_dispatcher", lambda: dispatcher, raising=False)
    import modules.lazyown_bridge as lb

    monkeypatch.setattr(lb, "get_dispatcher", lambda: dispatcher, raising=False)


def _ctx(**kw) -> SelectionContext:
    """Build a SelectionContext with sensible defaults for the bridge path."""
    base = {"target": "10.0.0.9", "phase": "enum", "services": ("microsoft-ds",), "os_hint": "linux"}
    base.update(kw)
    return SelectionContext(**base)


def test_no_target_abstains(monkeypatch):
    """Given no target, When proposing, Then the selector abstains."""
    _bind(monkeypatch, _Dispatcher(("enum4linux-ng 10.0.0.9", _Entry())))
    assert BridgeSelector().propose(_ctx(target="")) is None


def test_catalogue_hit_becomes_decision(monkeypatch):
    """Given a catalogue hit, When proposing, Then an ActionDecision carries it."""
    disp = _Dispatcher(("enum4linux-ng 10.0.0.9", _Entry(description="SMB enum", mitre_tactic="TA0007")))
    _bind(monkeypatch, disp)
    decision = BridgeSelector().propose(_ctx())
    assert decision is not None
    assert decision.command == "enum4linux-ng 10.0.0.9"
    assert decision.source == "bridge"
    assert decision.mitre == "TA0007"
    assert "SMB enum" in decision.reason


def test_target_is_passed_to_dispatcher(monkeypatch):
    """Given a target, When proposing, Then it reaches the dispatcher for substitution."""
    disp = _Dispatcher(("cmd 10.0.0.9", _Entry()))
    _bind(monkeypatch, disp)
    BridgeSelector().propose(_ctx(target="10.0.0.9"))
    assert disp.calls and disp.calls[0]["target"] == "10.0.0.9"


def test_burned_verbs_are_excluded(monkeypatch):
    """Given a burned verb, When proposing, Then it is in the dispatcher exclusion set."""
    disp = _Dispatcher(("cmd 10.0.0.9", _Entry()))
    _bind(monkeypatch, disp)
    BridgeSelector().propose(_ctx(burned=frozenset({"hydra"})))
    assert "hydra" in disp.calls[0]["excluded"]


def test_returned_burned_command_dropped(monkeypatch):
    """Given the dispatcher returns a burned verb, When proposing, Then it is dropped."""
    disp = _Dispatcher(("hydra -L users 10.0.0.9", _Entry()))
    _bind(monkeypatch, disp)
    assert BridgeSelector().propose(_ctx(burned=frozenset({"hydra"}))) is None


def test_no_catalogue_hit_abstains(monkeypatch):
    """Given the dispatcher returns None for every category, When proposing, Then None."""
    _bind(monkeypatch, _Dispatcher(None))
    assert BridgeSelector().propose(_ctx()) is None


def test_dispatcher_error_is_swallowed(monkeypatch):
    """Given the dispatcher raises on a category, When proposing, Then it abstains, not crash."""
    disp = _Dispatcher(None, raise_on={"enum", "recon"})
    _bind(monkeypatch, disp)
    assert BridgeSelector().propose(_ctx()) is None
