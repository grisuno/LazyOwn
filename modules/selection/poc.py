"""PoC selector: propose catalogued PoC verbs when services match.

Single contract: adapt ``modules.poc_registry`` trigger matching into the
shared :class:`~modules.selection.base.Selector` protocol. Every enabled
PoC verb whose trigger token appears in the discovered service names for
the target becomes a ``lazy_poc run <name> <target>`` decision with the
catalog's per-verb proposal overrides embedded (e.g. ``rport=9000`` for
MinIO), so the planner and the daemon queue the exact runnable line.
Guidance-only when the PoC's requirements are missing: the decision is
skipped rather than proposing a command that cannot start.
"""

from __future__ import annotations

import re

from modules.selection.base import ActionDecision, SelectionContext


class PoCSelector:
    """Propose ``lazy_poc run`` for the best-matching catalogued PoC."""

    name = "poc"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return a PoC action for the context, or None when nothing fits.

        Args:
            ctx: Live engagement snapshot with the target's services.

        Returns:
            A ``lazy_poc run <name> <target>`` decision when one enabled
            PoC matches a service token and its requirements are met,
            else None.
        """
        target = str(ctx.target or "").strip()
        if not target:
            return None
        try:
            from modules import poc_registry
        except Exception:
            return None
        tokens = set()
        for service in ctx.services:
            tokens.update(re.findall(r"[a-z0-9]+", str(service or "").lower()))
        excluded = set()
        for command in ctx.exclude:
            parts = command.split() if isinstance(command, str) else list(command or [])
            if len(parts) >= 3 and parts[0] == "lazy_poc" and parts[1] == "run":
                excluded.add(parts[2])
        for verb in poc_registry.poc_verbs().values():
            if not verb.enabled or not verb.triggers:
                continue
            if verb.name in excluded:
                continue
            if not any(trigger in tokens for trigger in verb.triggers):
                continue
            if poc_registry.missing_requirements(verb):
                continue
            command = f"lazy_poc run {verb.name} {target}".strip()
            for key, value in verb.proposal_overrides:
                command = f"{command} {key}={value}"
            return ActionDecision(
                command=command,
                source=self.name,
                reason=f"service match for {verb.name} ({', '.join(verb.triggers[:3])})",
                priority=4,
            )
        return None


__all__ = ["PoCSelector"]
