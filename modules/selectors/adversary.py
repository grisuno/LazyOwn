"""Adversary selector: run a custom adversary emulation named by the objective.

Single contract: when the task goal names a custom adversary profile from
``lazyadversaries/*.yaml``, propose executing it via the ``adversary_yaml``
verb. Conservative: abstains unless the goal names a known profile.
"""

from __future__ import annotations

import glob
import os
import re

from modules.selectors.base import ActionDecision, SelectionContext

_WORD_RE = re.compile(r"[a-z0-9_]+")


class AdversarySelector:
    """Propose ``adversary_yaml <name>`` when the goal names a profile."""

    name = "adversary"

    def __init__(self, adversaries_dir: str = "lazyadversaries") -> None:
        """Bind the directory holding adversary YAML profiles."""
        self._dir = adversaries_dir

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return an adversary-emulation action when the goal names one."""
        goal = str(ctx.extra.get("goal", "") or "").lower()
        if not goal:
            return None
        try:
            files = glob.glob(os.path.join(self._dir, "*.yaml"))
        except Exception:
            return None
        tokens = set(_WORD_RE.findall(goal))
        for path in sorted(files):
            name = os.path.splitext(os.path.basename(path))[0].strip().lower()
            if not name or name not in tokens:
                continue
            command = f"adversary_yaml {name}"
            if command in ctx.exclude:
                continue
            return ActionDecision(
                command=command,
                source=self.name,
                reason=f"goal names adversary profile {name}",
                priority=4,
            )
        return None


__all__ = ["AdversarySelector"]
