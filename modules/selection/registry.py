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

_URGENT_PRIORITY = 2


def all_selectors() -> list[Selector]:
    """Return every shared selector in priority order, before admin filtering.

    Order expresses priority. Objective-named capabilities (a specific APT
    actor, adversary profile or MITRE technique the operator asked for) and
    credential reuse win over the generic service-matched chain, because a
    named or evidence-backed intent is a stronger signal than an inferred one.
    The list grows one file at a time as strategies migrate into the package.
    """
    import os

    allow_lab = os.environ.get("AUTO_CHAIN_SELECTOR_LAB", "1").strip().lower() not in ("0", "false", "no")
    return [
        CredentialSpraySelector(),
        PlaybookSelector(),
        AdversarySelector(),
        IntelSelector(),
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
    """Return the first concrete decision from the cascade, or None.

    Resolution is two-pass: any decision graded urgent (``priority`` <= 2)
    wins over the ordinary order, so pending intelligence or credential
    spraying (new, evidence-backed signals) outrank generic chain runs;
    otherwise the ordered list decides, with objective-named capabilities
    (actor, adversary profile, technique) ahead of the generic chain.

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
        if ordinary is None:
            ordinary = decision
    return ordinary


__all__ = ["default_selectors", "propose_next"]
