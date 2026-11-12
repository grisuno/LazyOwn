"""Tests for the shared parquet (session-history) selector.

The parquet selector replays the command that most often succeeded in past
sessions for the current phase's lookup categories, skipping verbs that are
burned, campaign-blacklisted or already taken. The knowledge base and the
blacklist are injected through fakes so no parquet files or lessons files are
read. Every scenario states Given, When, Then.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

import modules.selection.parquet as parquet_mod  # noqa: E402
from modules.selection.base import SelectionContext  # noqa: E402
from modules.selection.parquet import ParquetSelector  # noqa: E402


class _PDB:
    """Knowledge-base double returning scripted rows per category."""

    def __init__(self, rows_by_cat):
        self._rows = rows_by_cat
        self.calls = []

    def query_session(self, phase=None, target=None, success_only=False, limit=20):
        self.calls.append({"phase": phase, "target": target, "success_only": success_only})
        return list(self._rows.get(phase, []))


def _bind(monkeypatch, pdb, blocked=None) -> None:
    """Point the selector's lazy pdb + blacklist lookups at the injected doubles."""
    monkeypatch.setattr(parquet_mod, "_get_pdb", lambda: pdb)
    monkeypatch.setattr(parquet_mod, "blocked_commands", lambda category: set(blocked or ()))


def _rows(*cmds):
    """Build parquet rows from command strings."""
    return [{"command": c} for c in cmds]


def _ctx(**kw) -> SelectionContext:
    """Build a SelectionContext with recon-phase defaults."""
    base = {"target": "10.0.0.9", "phase": "recon"}
    base.update(kw)
    return SelectionContext(**base)


def test_no_target_abstains(monkeypatch):
    """Given no target, When proposing, Then abstain."""
    _bind(monkeypatch, _PDB({"recon": _rows("nmap")}))
    assert ParquetSelector().propose(_ctx(target="")) is None


def test_no_pdb_abstains(monkeypatch):
    """Given no knowledge base, When proposing, Then abstain."""
    _bind(monkeypatch, None)
    assert ParquetSelector().propose(_ctx()) is None


def test_most_frequent_head_wins(monkeypatch):
    """Given repeated successes, When proposing, Then the most-frequent head is chosen."""
    _bind(monkeypatch, _PDB({"recon": _rows("nmap -sV", "nmap -p-", "whatweb x")}))
    decision = ParquetSelector().propose(_ctx())
    assert decision is not None
    assert decision.command == "nmap"
    assert decision.source == "parquet"
    assert decision.reason == "past success in recon"


def test_success_only_query(monkeypatch):
    """Given a query, When proposing, Then only successful history is requested."""
    pdb = _PDB({"recon": _rows("nmap")})
    _bind(monkeypatch, pdb)
    ParquetSelector().propose(_ctx())
    assert pdb.calls and pdb.calls[0]["success_only"] is True and pdb.calls[0]["target"] == "10.0.0.9"


def test_burned_verb_skipped(monkeypatch):
    """Given a burned verb, When proposing, Then it is not chosen."""
    _bind(monkeypatch, _PDB({"recon": _rows("nmap", "nmap", "whatweb")}))
    decision = ParquetSelector().propose(_ctx(burned=frozenset({"nmap"})))
    assert decision is not None and decision.command == "whatweb"


def test_blacklisted_verb_skipped(monkeypatch):
    """Given a campaign-blacklisted verb, When proposing, Then it is not chosen."""
    _bind(monkeypatch, _PDB({"recon": _rows("nmap", "nmap", "whatweb")}), blocked={"nmap"})
    decision = ParquetSelector().propose(_ctx())
    assert decision is not None and decision.command == "whatweb"


def test_taken_and_junk_skipped(monkeypatch):
    """Given taken verbs and junk heads, When proposing, Then they are filtered out."""
    _bind(monkeypatch, _PDB({"recon": _rows("echo hi", "/bin/x", "nmap")}))
    decision = ParquetSelector().propose(_ctx(exclude=frozenset({"nmap 10.0.0.9"})))
    assert decision is None


def test_multi_category_phase_falls_through(monkeypatch):
    """Given an exploit phase, When the first category is empty, Then a later one is mined."""
    pdb = _PDB({"exploit": [], "intrusion": _rows("hydra", "hydra")})
    _bind(monkeypatch, pdb)
    decision = ParquetSelector().propose(_ctx(phase="exploit"))
    assert decision is not None and decision.command == "hydra"
