"""Shared action-selection brain for the unified autonomous loop.

One file per selector contract; the runtimes depend only on
:mod:`modules.selectors.base` and :func:`modules.selectors.registry.propose_next`.
"""

from __future__ import annotations

from modules.selectors.adversary import AdversarySelector
from modules.selectors.atomic import AtomicSelector
from modules.selectors.base import ActionDecision, SelectionContext, Selector
from modules.selectors.chain import ChainSelector
from modules.selectors.cred_spray import CredentialSpraySelector
from modules.selectors.playbook import PlaybookSelector
from modules.selectors.registry import all_selectors, default_selectors, propose_next

__all__ = [
    "ActionDecision",
    "AdversarySelector",
    "AtomicSelector",
    "ChainSelector",
    "CredentialSpraySelector",
    "PlaybookSelector",
    "SelectionContext",
    "Selector",
    "all_selectors",
    "default_selectors",
    "propose_next",
]
