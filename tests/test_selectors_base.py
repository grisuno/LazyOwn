"""Shared selector brain contract: base types, chain selector and cascade.

Both autonomous runtimes consume this one cascade, so these tests pin the
protocol shape and the chain selector's adaptation of the shared matcher.
The chain registry is injected by monkeypatching ``scan_all`` so no YAML is
read.
"""

from __future__ import annotations

from modules.selectors.base import ActionDecision, SelectionContext, Selector
from modules.selectors.chain import ChainSelector
from modules.selectors.registry import default_selectors, propose_next


def _rows() -> list[dict]:
    """Return one linux web chain fixture."""
    return [{"name": "apt_web_http", "enabled": True, "valid": True, "tags": ["web", "http"], "platforms": ["linux"]}]


def _patch_registry(monkeypatch, rows=None) -> None:
    """Inject chain rows and reset the matcher cache."""
    import modules.chain_match as chain_match

    monkeypatch.setattr("modules.chain_registry.scan_all", lambda *a, **k: list(rows if rows is not None else _rows()))
    chain_match.reset_cache()


def test_chain_selector_honours_protocol():
    """Given the chain selector, Then it satisfies the Selector protocol."""
    assert isinstance(ChainSelector(), Selector)
    assert ChainSelector().name == "chain"


def test_chain_selector_proposes_for_matching_service(monkeypatch):
    """Given an http service on linux, When proposing, Then an apt_chain action returns."""
    _patch_registry(monkeypatch)
    ctx = SelectionContext(target="10.0.0.9", phase="exploit", os_hint="linux", services=("http",))
    decision = ChainSelector().propose(ctx)
    assert isinstance(decision, ActionDecision)
    assert decision.command == "apt_chain apt_web_http 10.0.0.9"
    assert decision.source == "chain"
    assert decision.priority == 3


def test_chain_selector_abstains_without_match(monkeypatch):
    """Given no service match, When proposing, Then the selector abstains."""
    _patch_registry(monkeypatch)
    ctx = SelectionContext(target="10.0.0.9", phase="exploit", os_hint="linux", services=("gopher",))
    assert ChainSelector().propose(ctx) is None


def test_chain_selector_respects_exclude(monkeypatch):
    """Given the only match already taken, When proposing, Then nothing returns.

    Exclude is the set of taken command strings; the chain selector derives the
    excluded chain names from any ``apt_chain <name> ...`` already queued.
    """
    _patch_registry(monkeypatch)
    ctx = SelectionContext(
        target="10.0.0.9",
        phase="exploit",
        os_hint="linux",
        services=("http",),
        exclude=frozenset({"apt_chain apt_web_http 10.0.0.9"}),
    )
    assert ChainSelector().propose(ctx) is None


def test_cascade_returns_first_decision(monkeypatch):
    """Given the default cascade, When a chain matches, Then propose_next returns it."""
    _patch_registry(monkeypatch)
    ctx = SelectionContext(target="10.0.0.9", phase="exploit", os_hint="linux", services=("http",))
    decision = propose_next(ctx)
    assert decision is not None
    assert decision.command == "apt_chain apt_web_http 10.0.0.9"


def test_cascade_abstains_when_all_abstain(monkeypatch):
    """Given nothing matches, When propose_next runs, Then it returns None."""
    _patch_registry(monkeypatch)
    ctx = SelectionContext(target="10.0.0.9", phase="recon", os_hint="linux", services=("http",))
    assert propose_next(ctx) is None


def test_default_selectors_contains_chain():
    """Given the default cascade, Then the chain selector is present."""
    names = {selector.name for selector in default_selectors()}
    assert "chain" in names
