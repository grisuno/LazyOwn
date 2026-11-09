"""Technique selector: propose MITRE technique emulation for the phase.

Single contract: adapt :func:`modules.playbook_engine.phase_techniques`
(STIX-first with local atomic-index fallback) into the
:class:`~modules.selection.base.Selector` protocol. Post-foothold phases
only — technique emulation assumes an existing execution surface.
"""

from __future__ import annotations

from modules.selection.atomic import _SHELL_PHASES
from modules.selection.base import ActionDecision, SelectionContext

_TECHNIQUE_LIMIT = 6
_PRIORITY = 5


class TechniqueSelector:
    """Propose ``atomic_tests <TID> --non-interactive`` for the phase."""

    name = "technique"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return a technique emulation action, or None when not applicable."""
        if not ctx.target or ctx.phase not in _SHELL_PHASES:
            return None
        try:
            from modules.playbook_engine import phase_techniques
        except Exception:
            return None
        techniques = phase_techniques(ctx.phase, ctx.os_hint, top_n=_TECHNIQUE_LIMIT)
        for tech in techniques:
            tid = str(tech.get("technique_id", "") or "").strip()
            if not tid:
                continue
            command = f"atomic_tests {tid} --non-interactive"
            if command in ctx.exclude:
                continue
            name = str(tech.get("name", "") or "").strip()
            detail = f" ({name})" if name else ""
            return ActionDecision(
                command=command,
                source=self.name,
                reason=f"phase technique for {ctx.phase}: {tid}{detail}",
                priority=_PRIORITY,
            )
        return None


__all__ = ["TechniqueSelector"]
