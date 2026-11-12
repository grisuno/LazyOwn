"""Bridge selector: propose a phase/service-appropriate catalogued command.

Single contract: adapt the LazyOwn bridge catalogue
(:func:`modules.lazyown_bridge.get_dispatcher`) into the
:class:`~modules.selection.base.Selector` protocol. The dispatcher owns the
MITRE-mapped, OS-filtered 363-command catalogue and all scoring; this file only
tries each phase category as a tag hint, shapes the winning entry into an
:class:`ActionDecision`, and drops commands whose verb is burned or already
taken. It is a fallback tier: it fires only when the evidence-based and named
selectors ahead of it in the cascade abstain.
"""

from __future__ import annotations

from modules.selection._phase_categories import categories_for
from modules.selection.base import ActionDecision, SelectionContext

_FALLBACK_PRIORITY = 7


class BridgeSelector:
    """Propose one bridge-catalogue command for the phase, or None."""

    name = "bridge"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return a catalogue suggestion for the context, or None.

        Each category mapped to the current phase is tried as a tag hint until
        the dispatcher returns a command. Burned verbs and verbs already taken
        this round are passed as the dispatcher's exclusion set and re-checked
        on the returned command, so a dead verb is never proposed.
        """
        if not ctx.target:
            return None
        try:
            from modules.lazyown_bridge import get_dispatcher
        except Exception:
            return None
        try:
            dispatcher = get_dispatcher()
        except Exception:
            return None
        excluded = set(ctx.burned) | {
            tokens[0] for command in ctx.exclude for tokens in [str(command).split()] if tokens
        }
        services = list(ctx.services)
        os_hint = ctx.os_hint or "any"
        for category in categories_for(ctx.phase):
            try:
                result = dispatcher.suggest(
                    phase=ctx.phase,
                    target=ctx.target,
                    services=services,
                    has_creds=ctx.has_creds,
                    excluded=excluded,
                    tag_hint=category,
                    os_hint=os_hint,
                )
            except Exception:
                continue
            if result is None:
                continue
            command, entry = result
            command = str(command or "").strip()
            if not command:
                continue
            verb = command.split()[0]
            if verb in excluded or command in ctx.exclude:
                continue
            return ActionDecision(
                command=command,
                source=self.name,
                reason=f"bridge catalog — {str(getattr(entry, 'description', ''))[:60]}",
                priority=_FALLBACK_PRIORITY,
                mitre=str(getattr(entry, "mitre_tactic", "") or ""),
            )
        return None


__all__ = ["BridgeSelector"]
