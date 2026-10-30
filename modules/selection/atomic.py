"""Atomic selector: emulate named MITRE ATT&CK techniques with atomic tests.

Single contract covering both MITRE ATT&CK techniques and the Atomic Red Team
library, which share one execution path: ``atomic_emulate --techniques``. When
the objective names ATT&CK technique ids (``T1059``, ``T1059.001``), propose
emulating them against the target. Gated to post-foothold phases because
atomic emulation runs through a working shell; abstains otherwise.
"""

from __future__ import annotations

import re

from modules.selection.base import ActionDecision, SelectionContext

_TECHNIQUE_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
_SHELL_PHASES = frozenset({"postexp", "privesc", "lateral", "exfil", "cred", "exploit"})


class AtomicSelector:
    """Propose ``atomic_emulate --target <t> --techniques <ids>`` for named TTPs."""

    name = "atomic"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return an atomic-emulation action when technique ids are named."""
        if not ctx.target or ctx.phase not in _SHELL_PHASES:
            return None
        declared = ctx.extra.get("techniques")
        if declared:
            found = [str(t).strip().upper() for t in declared if str(t).strip()]
        else:
            goal = str(ctx.extra.get("goal", "") or "")
            found = [match.upper() for match in _TECHNIQUE_RE.findall(goal)]
        ids = list(dict.fromkeys(found))
        if not ids:
            return None
        command = f"atomic_emulate --target {ctx.target} --techniques {','.join(ids)}"
        if command in ctx.exclude:
            return None
        return ActionDecision(
            command=command,
            source=self.name,
            reason=f"emulate MITRE/atomic technique(s) {','.join(ids)}",
            priority=4,
        )


__all__ = ["AtomicSelector"]
