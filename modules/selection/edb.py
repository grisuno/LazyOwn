from __future__ import annotations

from modules.selection.base import ActionDecision, SelectionContext


class EDBSelector:
    """Propose ExploitDB (atomic_exploit) when services/cves fit."""

    name = "edb"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        if not ctx.target:
            return None
        svcs = [str(s).lower() for s in (ctx.services or ())]
        if ctx.phase not in ("exploit", "initial", "access", "post"):
            return None
        try:
            from modules import atomic_exploit_bridge as aeb

            services = [{"name": s, "port": "", "product": "", "version": ""} for s in svcs]
            rows = aeb.rank(services or [{"name": "generic"}], os_hint=ctx.os_hint or "linux") if svcs else aeb.rank([], os_hint=ctx.os_hint or "linux")
            if not rows:
                return None
            top = rows[0]
            eid = top["id"]
            cmd = f"atomic_exploit run --id {eid} --rhost {ctx.target}"
            if cmd in ctx.exclude:
                return None
            return ActionDecision(
                command=cmd,
                source=self.name,
                reason=f"EDB {eid} matches {top.get('service') or svcs or 'target'} conf={top.get('confidence',0):.0%}",
                priority=4,
                mitre=top.get("mitre_id") or "",
            )
        except Exception:
            return None


__all__ = ["EDBSelector"]
