"""Parquet selector: propose the command that most often succeeded before.

Single contract: adapt the columnar session knowledge base
(``lazyown_parquet_db.get_pdb``) into the shared
:class:`~modules.selection.base.Selector` protocol. For each lookup category
mapped to the current phase it mines the most-frequent successfully-executed
command head, skipping verbs that are burned, campaign-blacklisted, or already
taken. It is a history fallback: it fires only when the evidence-based and
named selectors ahead of it in the cascade abstain, and sits just before the
bridge catalogue so a proven command wins over a generic catalogue suggestion.
"""

from __future__ import annotations

import sys
from pathlib import Path

from modules.campaign_blacklist import blocked_commands
from modules.selection._phase_categories import categories_for
from modules.selection.base import ActionDecision, SelectionContext

_FALLBACK_PRIORITY = 6
_HISTORY_LIMIT = 30
_BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _get_pdb():
    """Return the parquet knowledge base, or None when unavailable.

    The knowledge base module lives under ``skills/``; this mirrors the house
    pattern in ``modules/ttpscope_bridge.py`` of adding that directory to the
    path and importing it, so a missing optional dependency degrades this one
    selector to an abstention instead of failing the loop.
    """
    try:
        skills_dir = str(_BASE_DIR / "skills")
        if skills_dir not in sys.path:
            sys.path.insert(0, skills_dir)
        from lazyown_parquet_db import get_pdb

        return get_pdb()
    except Exception:
        return None


class ParquetSelector:
    """Propose the most-frequent past-successful command for the phase, or None."""

    name = "parquet"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return a history-backed command head for the context, or None."""
        if not ctx.target:
            return None
        pdb = _get_pdb()
        if pdb is None:
            return None
        taken_verbs = {tokens[0] for command in ctx.exclude for tokens in [str(command).split()] if tokens}
        for category in categories_for(ctx.phase):
            command = self._candidate(pdb, category, ctx, taken_verbs)
            if command:
                return ActionDecision(
                    command=command,
                    source=self.name,
                    reason=f"past success in {category}",
                    priority=_FALLBACK_PRIORITY,
                )
        return None

    def _candidate(self, pdb, category: str, ctx: SelectionContext, taken_verbs: set[str]) -> str | None:
        """Return the most-frequent eligible successful command head, or None."""
        try:
            rows = pdb.query_session(phase=category, target=ctx.target, success_only=True, limit=_HISTORY_LIMIT)
        except Exception:
            return None
        blocked = blocked_commands(category)
        freq: dict[str, int] = {}
        for row in rows or []:
            parts = str(row.get("command", "") or "").strip().split()
            if not parts:
                continue
            head = parts[0]
            if head.startswith("/") or head.startswith("echo"):
                continue
            if head in ctx.burned or head in blocked or head in taken_verbs:
                continue
            freq[head] = freq.get(head, 0) + 1
        return max(freq, key=lambda c: freq[c]) if freq else None


__all__ = ["ParquetSelector"]
