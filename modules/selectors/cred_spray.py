"""Credential-spray selector: reuse known credentials against open services.

Single contract: when usable credentials exist and a service that accepts them
is open, propose the service-appropriate LazyOwn verb (which reads the target
and credentials from ``payload.json``). Gated to post-recon phases where
credential reuse is meaningful. Migrated from the daemon's inline selector so
both autonomous runtimes share one implementation.
"""

from __future__ import annotations

from modules.selectors.base import ActionDecision, SelectionContext

_SERVICE_VERBS: dict[str, str] = {
    "ssh": "lazyssh",
    "smb": "crackmapexec",
    "microsoft-ds": "crackmapexec",
    "netbios-ssn": "crackmapexec",
    "winrm": "evil-winrm",
    "ftp": "lazyftp",
    "http": "lazyburp",
    "https": "lazyburp",
    "rdp": "xfreerdp",
    "ms-wbt-server": "xfreerdp",
    "mssql": "mssqlpwner",
    "mysql": "mysqldump",
    "ldap": "ldapdomaindump",
}
_CRED_PHASES = frozenset({"exploit", "lateral", "privesc", "cred"})


class CredentialSpraySelector:
    """Propose a credential-reuse verb for an open service when creds exist."""

    name = "cred_spray"

    def propose(self, ctx: SelectionContext) -> ActionDecision | None:
        """Return a spray verb for the first matching open service, or None."""
        if not ctx.has_creds or ctx.phase not in _CRED_PHASES:
            return None
        for service in ctx.services:
            verb = _SERVICE_VERBS.get(str(service).strip().lower())
            if verb is None or verb in ctx.exclude:
                continue
            return ActionDecision(
                command=verb,
                source=self.name,
                reason=f"credential reuse against {service} on {ctx.target}",
                priority=2,
            )
        return None


__all__ = ["CredentialSpraySelector"]
