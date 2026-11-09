"""Technique-chain selector: compile the phase's techniques into one paced chain.

Single contract. Where :class:`~modules.selection.technique.TechniqueSelector`
emits one ``atomic_tests`` per round and
:class:`~modules.selection.atomic.AtomicSelector` emits a goal-named set, this
strategy compiles the ranked MITRE/Atomic techniques for the current phase (or
a goal that names several) into one ordered chain and runs it through
``apt_chain``. The ChainRunner's shared EdrPacer then applies the configured
jitter and sleeper windows between techniques, so chaining honours the
operator's pacing. Post-foothold phases only, because atomic emulation assumes
an existing execution surface; abstains otherwise.
"""

from __future__ import annotations

from modules.selection.atomic import _SHELL_PHASES, _TECHNIQUE_RE
from modules.selection.base import ActionDecision, SelectionContext

_PRIORITY = 4
_PHASE_TECHNIQUE_LIMIT = 6
_MIN_CHAIN_TECHNIQUES = 2


class TechniqueChainSelector:
    """Propose ``apt_chain <synth> <target>`` for an ordered technique chain."""

    name = "technique_chain"

    def _ordered_techniques(self, ctx: SelectionContext) -> list[str]:
        """Return the ordered technique ids to chain for this context.

        A goal that names two or more technique ids wins verbatim (operator
        intent); otherwise the phase's ranked techniques are used so the
        chain reflects the current kill-chain stage.
        """
        declared = ctx.extra.get("techniques")
        if declared:
            named = [str(t).strip().upper() for t in declared if str(t).strip()]
        else:
            goal = str(ctx.extra.get("goal", "") or "")
            named = [match.upper() for match in _TECHNIQUE_RE.findall(goal)]
        named = list(dict.fromkeys(named))
        if len(named) >= _MIN_CHAIN_TECHNIQUES:
            return named
        try:
            from modules.playbook_engine import phase_techniques
        except Exception:
            return named
        ranked = phase_techniques(ctx.phase, ctx.os_hint, top_n=_PHASE_TECHNIQUE_LIMIT)
        ids = [str(tech.get("technique_id", "") or "").strip() for tech in ranked]
        return [tid for tid in dict.fromkeys(ids) if tid]

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return a technique-chain action, or None when fewer than two fit."""
        if not ctx.target or ctx.phase not in _SHELL_PHASES:
            return None
        techniques = self._ordered_techniques(ctx)
        if len(techniques) < _MIN_CHAIN_TECHNIQUES:
            return None
        try:
            from modules.chain_registry import CHAINS_DIR
            from modules.chain_registry import get as get_chain
            from modules.chain_synth import synth_technique_chain_data, write_generated_chain
        except Exception:
            return None
        data, used = synth_technique_chain_data(ctx.target, techniques, os_hint=ctx.os_hint)
        if not data:
            return None
        name = str(data.get("name", "") or "")
        command = f"apt_chain {name} {ctx.target}"
        if not name or command in ctx.exclude:
            return None
        if get_chain(name) is None:
            _path, errors = write_generated_chain(data, CHAINS_DIR)
            if errors:
                return None
        return ActionDecision(
            command=command,
            source=self.name,
            reason=f"chain {len(used)} phase technique(s): {', '.join(used)}",
            priority=_PRIORITY,
            mitre=used[0],
        )


__all__ = ["TechniqueChainSelector"]
