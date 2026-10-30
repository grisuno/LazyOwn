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
from modules.selection.playbook import PlaybookSelector


def all_selectors() -> list[Selector]:
    """Return every shared selector in priority order, before admin filtering.

    Order expresses priority. Objective-named capabilities (a specific APT
    actor, adversary profile or MITRE technique the operator asked for) and
    credential reuse win over the generic service-matched chain, because a
    named or evidence-backed intent is a stronger signal than an inferred one.
    The list grows one file at a time as strategies migrate into the package.
    """
    return [
        CredentialSpraySelector(),
        PlaybookSelector(),
        AdversarySelector(),
        AtomicSelector(),
        ChainSelector(),
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
    """Return the first concrete decision from the cascade, or None.

    Args:
        ctx: Live engagement snapshot.
        selectors: Optional explicit cascade; defaults to
            :func:`default_selectors`.

    Returns:
        The first non-None :class:`ActionDecision`, or None when every
        selector abstains.
    """
    for selector in selectors if selectors is not None else default_selectors():
        try:
            decision = selector.propose(ctx)
        except Exception:
            decision = None
        if decision is not None:
            return decision
    return None


__all__ = ["default_selectors", "propose_next"]
