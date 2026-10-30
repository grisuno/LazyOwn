"""Shared action-selection brain for the unified autonomous loop.

One file per selector contract; the runtimes depend only on
:mod:`modules.selection.base` and :func:`modules.selection.registry.propose_next`.
"""

from __future__ import annotations

from modules.selection.adversary import AdversarySelector
from modules.selection.atomic import AtomicSelector
from modules.selection.base import ActionDecision, SelectionContext, Selector
from modules.selection.chain import ChainSelector
from modules.selection.cred_spray import CredentialSpraySelector
from modules.selection.playbook import PlaybookSelector
from modules.selection.registry import all_selectors, default_selectors, propose_next

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
