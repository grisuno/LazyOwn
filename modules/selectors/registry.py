"""Assemble and run the shared selector cascade.

The cascade is the single ordered list of strategies the unified autonomous
loop consults. :func:`propose_next` tries each selector in order and returns
the first concrete decision, so adding a capability is adding one file and one
registry entry (Open/Closed). Both runtimes build their context and call here
instead of carrying private selection logic.
"""

from __future__ import annotations

from collections.abc import Iterable

from modules.selectors.adversary import AdversarySelector
from modules.selectors.atomic import AtomicSelector
from modules.selectors.base import ActionDecision, SelectionContext, Selector
from modules.selectors.chain import ChainSelector
from modules.selectors.playbook import PlaybookSelector


def default_selectors() -> list[Selector]:
    """Return the default ordered cascade of shared selectors.

    Order expresses priority. Objective-named capabilities (a specific APT
    actor, adversary profile or MITRE technique the operator asked for) win
    over the generic service-matched chain, because a named intent is a
    stronger signal than an inferred one. The list grows one file at a time
    as strategies migrate into the shared package.
    """
    return [
        PlaybookSelector(),
        AdversarySelector(),
        AtomicSelector(),
        ChainSelector(),
    ]


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
