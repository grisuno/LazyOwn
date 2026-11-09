"""Module selector: map goal/service mentions onto runnable registry modules.

Single contract: adapt ``ModuleRegistry.proposal_intents`` (conservative
token matching over lazyaddons and APT playbooks) into the
:class:`~modules.selection.base.Selector` protocol.
"""

from __future__ import annotations

from modules.selection.base import ActionDecision, SelectionContext

_PROPOSAL_LIMIT = 3
_PRIORITY = 6


class ModuleSelector:
    """Propose ``lazy addon``/``apt_playbook run`` lines from the registry."""

    name = "module"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return the first unproposed registry intent, or None."""
        if not ctx.target:
            return None
        try:
            from modules.module_registry import ModuleRegistry

            texts = [str(ctx.extra.get("goal", "") or ""), *ctx.services]
            lines = ModuleRegistry.get_instance().proposal_intents(
                texts, target=ctx.target, limit=_PROPOSAL_LIMIT
            )
        except Exception:
            return None
        for line in lines:
            command = str(line or "").strip().replace("lazy addon ", "lazy_addon ", 1)
            if not command or command in ctx.exclude:
                continue
            return ActionDecision(
                command=command,
                source=self.name,
                reason="registry module matches goal or services",
                priority=_PRIORITY,
            )
        return None


__all__ = ["ModuleSelector"]
