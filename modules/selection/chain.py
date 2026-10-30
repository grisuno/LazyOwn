"""Chain selector: propose a vetted ``apt_chain`` when one fits the state.

Single contract: adapt the shared chain matcher (``modules.chain_match``) into
the :class:`~modules.selection.base.Selector` protocol. The scoring rules live
in ``chain_match``; this file only shapes the decision and dedupes per target.
"""

from __future__ import annotations

from modules.selection.base import ActionDecision, SelectionContext


class ChainSelector:
    """Propose ``apt_chain <name> <target>`` for the best-matching chain."""

    name = "chain"

    def __init__(self, allow_lab: bool = True) -> None:
        """Bind the lab-inclusion policy for the matcher.

        Args:
            allow_lab: Include lab/gym chains (default True; real engagements
                pass False).
        """
        self._allow_lab = bool(allow_lab)

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return a chain action for the context, or None when nothing fits."""
        if not ctx.target:
            return None
        try:
            from modules.chain_match import best_chain
        except Exception:
            return None
        excluded_names = {
            tokens[1]
            for command in ctx.exclude
            for tokens in [str(command).split()]
            if len(tokens) >= 2 and tokens[0] == "apt_chain"
        }
        match = best_chain(
            phase=ctx.phase,
            os_hint=ctx.os_hint,
            services=list(ctx.services),
            exclude=excluded_names,
            allow_lab=self._allow_lab,
        )
        if match is None:
            return None
        name, reason = match
        return ActionDecision(
            command=f"apt_chain {name} {ctx.target}",
            source=self.name,
            reason=reason,
            priority=3,
        )


__all__ = ["ChainSelector"]
