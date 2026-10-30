"""Playbook selector: run an APT actor emulation named by the objective.

Single contract: when the task goal names a known APT actor (from the
``playbooks/`` library) and a matching ``apt_<actor>`` chain exists, propose
running it end to end via ``apt_chain``. Conservative: abstains unless the goal
clearly names an actor, so it never emulates an actor the operator did not ask
for.
"""

from __future__ import annotations

import re

from modules.selectors.base import ActionDecision, SelectionContext

_WORD_RE = re.compile(r"[a-z0-9]+")


class PlaybookSelector:
    """Propose ``apt_chain apt_<actor> <target>`` when the goal names an actor."""

    name = "playbook"

    def __init__(self, playbook_dir: str = "playbooks") -> None:
        """Bind the playbook directory to scan for known actors."""
        self._dir = playbook_dir

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return an actor-emulation action when the goal names one, else None."""
        goal = str(ctx.extra.get("goal", "") or "").lower()
        if not ctx.target or not goal:
            return None
        try:
            from modules.apt_playbooks import AptPlaybookEngine
            from modules.chain_registry import get as get_chain
        except Exception:
            return None
        try:
            actors = AptPlaybookEngine(playbook_dir=self._dir).list_playbooks()
        except Exception:
            return None
        tokens = set(_WORD_RE.findall(goal))
        for summary in actors:
            actor = str(summary.get("apt_name", "") or "").strip().lower()
            if not actor:
                continue
            aliases = {str(a).strip().lower() for a in (summary.get("aliases") or [])}
            if not ({actor} | aliases) & tokens:
                continue
            chain = actor if actor.startswith("apt_") else f"apt_{actor}"
            command = f"apt_chain {chain} {ctx.target}"
            if command in ctx.exclude:
                continue
            try:
                if get_chain(chain) is None:
                    continue
            except Exception:
                continue
            return ActionDecision(
                command=command,
                source=self.name,
                reason=f"goal names APT actor {actor}",
                priority=4,
            )
        return None


__all__ = ["PlaybookSelector"]
