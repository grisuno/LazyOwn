"""Determinism tests for chain selection tie-breaking and selector resilience.

A score tie between two vetted chains must resolve the same way no matter how
the registry happens to order its rows, otherwise two operators on identical
state pick different chains. A selector that raises must still be treated as a
clean abstention (fail-open) while leaving an observable log trace rather than
vanishing silently.
"""

from __future__ import annotations

import logging

from modules.chain_match import best_chain
from modules.selection.base import ActionDecision, SelectionContext
from modules.selection.registry import propose_next


def _rows(names: list[str]) -> list[dict]:
    """Build equally-scoring exploit-phase chain rows for the given names."""
    return [{"name": name, "tags": ["http", "exploit"], "platforms": []} for name in names]


def test_tie_break_is_name_ascending_regardless_of_order():
    forward = best_chain("exploit", "", ["http"], rows=_rows(["bravo", "alpha", "charlie"]))
    reverse = best_chain("exploit", "", ["http"], rows=_rows(["charlie", "bravo", "alpha"]))
    assert forward is not None and reverse is not None
    assert forward[0] == "alpha"
    assert forward[0] == reverse[0]


def test_higher_score_still_wins_over_name_order():
    rows = [
        {"name": "alpha", "tags": ["http"], "platforms": []},
        {"name": "zulu", "tags": ["http", "exploit"], "platforms": []},
    ]
    match = best_chain("exploit", "", ["http"], rows=rows)
    assert match is not None and match[0] == "zulu"


def test_excluded_chain_is_skipped_deterministically():
    match = best_chain("exploit", "", ["http"], exclude={"alpha"}, rows=_rows(["alpha", "bravo"]))
    assert match is not None and match[0] == "bravo"


def test_no_service_match_returns_none():
    assert best_chain("exploit", "", ["ftp"], rows=_rows(["alpha"])) is None


class _Boom:
    """Selector that always raises, to prove the cascade stays fail-open."""

    name = "boom"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        raise RuntimeError("selector exploded")


class _Quiet:
    """Selector that always abstains."""

    name = "quiet"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        return None


class _Pick:
    """Selector that always proposes one ordinary action."""

    name = "pick"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        return ActionDecision(command="id", source=self.name, reason="probe", priority=5)


def test_crashing_selector_is_abstention_but_logged(caplog):
    ctx = SelectionContext(target="10.0.0.1")
    with caplog.at_level(logging.WARNING, logger="modules.selection.registry"):
        decision = propose_next(ctx, selectors=[_Boom(), _Pick()])
    assert decision is not None and decision.command == "id"
    assert any("boom" in rec.message and "crashed" in rec.message for rec in caplog.records)


def test_clean_abstention_emits_no_warning(caplog):
    ctx = SelectionContext(target="10.0.0.1")
    with caplog.at_level(logging.WARNING, logger="modules.selection.registry"):
        decision = propose_next(ctx, selectors=[_Quiet(), _Pick()])
    assert decision is not None and decision.command == "id"
    assert not caplog.records
