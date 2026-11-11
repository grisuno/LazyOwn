"""Isomorphism-transfer BDD contract: family signatures and chain reuse.

Given structurally-similar targets, When their facts are signed, Then they
share a family; and the registry surfaces the chain that proved a same-family
target over one merely synthesised.
"""

from __future__ import annotations

import modules.lazy_loop as loop
from modules.chain_family import FamilyRegistry, family_signature


def test_signature_ignores_service_order_and_duplicates():
    """Given reordered duplicate services, When signed, Then signatures match."""
    a = family_signature({"services": ["http", "smb", "ssh"], "os_hint": "linux", "has_creds": False})
    b = family_signature({"services": ["ssh", "http", "http", "smb"], "os_hint": "linux", "has_creds": False})
    assert a == b


def test_signature_collapses_known_service_aliases():
    """Given service aliases, When signed, Then they normalise to one family."""
    a = family_signature({"services": ["microsoft-ds", "www"], "os_hint": "", "has_creds": False})
    b = family_signature({"services": ["smb", "http"], "os_hint": "", "has_creds": False})
    assert a == b


def test_signature_distinguishes_os_and_creds():
    """Given different OS or creds, When signed, Then families differ."""
    base = {"services": ["http"], "os_hint": "linux", "has_creds": False}
    assert family_signature(base) != family_signature({**base, "os_hint": "windows"})
    assert family_signature(base) != family_signature({**base, "has_creds": True})


def test_empty_services_is_the_empty_family():
    """Given no services, When signed, Then the empty family is returned."""
    assert family_signature({"services": [], "os_hint": "linux"}) == "empty"


def test_registry_ranks_proven_chain_over_associated(tmp_path):
    """Given a win and an association, When best is read, Then the win leads."""
    registry = FamilyRegistry(tmp_path / "fam.json")
    facts = {"services": ["http", "smb"], "os_hint": "linux", "has_creds": False}
    sig = family_signature(facts)
    registry.record_association(sig, "chain_synth_a")
    registry.record_association(sig, "chain_synth_a")
    registry.record_win(sig, "chain_win_b", target="10.0.0.9")
    best = registry.best(sig)
    assert best["chain"] == "chain_win_b"
    assert best["wins"] == 1
    assert "10.0.0.9" in best["targets"]


def test_registry_empty_family_is_never_recorded(tmp_path):
    """Given the empty family, When recorded, Then nothing persists."""
    registry = FamilyRegistry(tmp_path / "fam.json")
    registry.record_win("empty", "whatever")
    assert registry.best("empty") is None


def test_transfer_note_surfaces_known_chain(tmp_path):
    """Given a prior win, When a same-family target synthesises, Then a note."""
    registry = FamilyRegistry(tmp_path / "fam.json")
    facts = {"services": ["http", "smb"], "os_hint": "linux", "has_creds": False}
    assert registry.transfer_note(facts) == ""
    registry.record_win(family_signature(facts), "chain_win_b", target="10.0.0.9")
    note = registry.transfer_note({"services": ["smb", "http"], "os_hint": "linux", "has_creds": False})
    assert "chain_win_b" in note
    assert "isomorphism transfer" in note


def test_default_registry_uses_store_path(tmp_path, monkeypatch):
    """Given the loop store, When a default registry is built, Then it binds there."""
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    from modules.chain_family import default_registry

    registry = default_registry()
    assert registry.path == tmp_path / "chain_families.json"
