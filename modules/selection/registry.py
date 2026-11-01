"""Assemble and run the shared selector cascade.

The cascade is the single ordered list of strategies the unified autonomous
loop consults. :func:`propose_next` tries each selector in order and returns
the first concrete decision, so adding a capability is adding one file and one
registry entry (Open/Closed). Both runtimes build their context and call here
instead of carrying private selection logic.
"""

from __future__ import annotations

from collections.abc import Iterable

from modules.selection.adversary import AdversarySelector
from modules.selection.atomic import AtomicSelector
from modules.selection.base import ActionDecision, SelectionContext, Selector
from modules.selection.chain import ChainSelector
from modules.selection.cred_spray import CredentialSpraySelector
from modules.selection.intel import IntelSelector
from modules.selection.playbook import PlaybookSelector
from modules.selection.poc import PoCSelector
from modules.selection.edb import EDBSelector

_URGENT_PRIORITY = 2


def all_selectors() -> list[Selector]:
    """Return every shared selector in priority order, before admin filtering.

    Order expresses priority. Objective-named capabilities (a specific APT
    actor, adversary profile or MITRE technique the operator asked for) and
    credential reuse win over the generic service-matched chain, because a
    named or evidence-backed intent is a stronger signal than an inferred one.
    A service-matched catalogued PoC sits between the intel-driven selectors
    and the generic chain: it is narrower than a full chain and broader than
    a named actor. The list grows one file at a time as strategies migrate
    into the package.
    """
    import os

    allow_lab = os.environ.get("AUTO_CHAIN_SELECTOR_LAB", "1").strip().lower() not in ("0", "false", "no")
    return [
        CredentialSpraySelector(),
        PlaybookSelector(),
        AdversarySelector(),
        IntelSelector(),
        PoCSelector(),
        AtomicSelector(),
        ChainSelector(allow_lab=allow_lab),
    ]

def default_selectors() -> list[Selector]:
    """Return the cascade after applying the orchestrator's enable toggles.

    The orchestrator is the single admin surface: a selector disabled via
    ``orchestrator.selectors.<name> = false`` is dropped here, so both
    runtimes honour one administration point without their own switches.
    """
    try:
        from modules import orchestrator_config

        return [sel for sel in all_selectors() if orchestrator_config.selector_enabled(sel.name)]
    except Exception:
        return all_selectors()


def propose_next(
    ctx: SelectionContext,
    selectors: Iterable[Selector] | None = None,
) -> ActionDecision | None:
    """Return the best concrete decision from the cascade, or None.

    Resolution is two-pass: any decision graded urgent (``priority`` <= 2)
    wins immediately, so pending intelligence or credential spraying (new,
    evidence-backed signals) outrank everything. Otherwise every ordinary
    decision competes on priority: the lowest ``priority`` number wins
    (lower is more urgent), cascade order breaking ties, so a service-matched
    chain (priority 3) outranks a generic refresh (priority 6) even when the
    refresh sits earlier in the cascade.

    Args:
        ctx: Live engagement snapshot.
        selectors: Optional explicit cascade; defaults to
            :func:`default_selectors`.

    Returns:
        The winning :class:`ActionDecision`, or None when every
        selector abstains.
    """
    cascade = list(selectors) if selectors is not None else default_selectors()
    ordinary: ActionDecision | None = None
    for selector in cascade:
        try:
            decision = selector.propose(ctx)
        except Exception:
            decision = None
        if decision is None or not str(decision.command or "").strip():
            continue
        if int(decision.priority) <= _URGENT_PRIORITY:
            return decision
        if ordinary is None or int(decision.priority) < int(ordinary.priority):
            ordinary = decision
    return ordinary


__all__ = ["default_selectors", "propose_next"]
