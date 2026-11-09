"""Lazyscript selector: propose an operator-authored .ls recipe when it fits.

Single contract. Lazyscripts (``lazyscripts/*.ls``) are ordered lists of
LazyOwn verbs an operator curated for a task (SMB sweep, AD enumeration, an
atomic-agent run). They are a safe, explicit chaining surface no selector
reached before. This strategy token-matches the goal and discovered services
against each script name and proposes ``lazyscript <name>.ls`` for the best
fit, so the autonomous loop can run a curated recipe instead of rebuilding it
one verb at a time. Matching mirrors the conservative whole-token rule the
module registry uses, so a plain substring never fires a script.
"""

from __future__ import annotations

import re
from pathlib import Path

from modules.selection.base import ActionDecision, SelectionContext

_PRIORITY = 6
_MIN_TOKEN_LEN = 3
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "lazyscripts"
_SKIP_STEMS = frozenset({"startup", "lazyquit", "lazyscript"})
_STOPWORDS = frozenset({"the", "and", "for", "run", "get", "all", "lazy", "scan"})


def _tokens(text: str) -> set[str]:
    """Return the matchable lowercase tokens in one text blob."""
    return {
        token
        for token in re.findall(r"[a-z0-9]+", str(text or "").lower())
        if len(token) >= _MIN_TOKEN_LEN and token not in _STOPWORDS
    }


class LazyscriptSelector:
    """Propose ``lazyscript <name>.ls`` when a curated recipe matches the state."""

    name = "lazyscript"

    def __init__(self, scripts_dir: Path | None = None) -> None:
        """Bind the lazyscripts directory (overridable for tests)."""
        self._dir = Path(scripts_dir) if scripts_dir is not None else _SCRIPTS_DIR

    def _catalogue(self) -> list[str]:
        """Return the actionable lazyscript stems in a stable order."""
        if not self._dir.is_dir():
            return []
        stems: list[str] = []
        for path in sorted(self._dir.glob("*.ls")):
            stem = path.stem
            if stem and stem not in _SKIP_STEMS:
                stems.append(stem)
        return stems

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return a lazyscript action for the context, or None when none fit."""
        if not ctx.target:
            return None
        corpus = _tokens(str(ctx.extra.get("goal", "") or ""))
        corpus |= _tokens(" ".join(ctx.services))
        if not corpus:
            return None
        for stem in self._catalogue():
            if not _tokens(stem) & corpus:
                continue
            command = f"lazyscript {stem}.ls"
            if command in ctx.exclude:
                continue
            return ActionDecision(
                command=command,
                source=self.name,
                reason=f"curated recipe matches goal or services: {stem}",
                priority=_PRIORITY,
            )
        return None


__all__ = ["LazyscriptSelector"]
