"""
Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.

Produces instruction snippets that Hermes injects into the system prompt
based on the current engagement phase, discovered services, and credentials.

Follows the Builder pattern: start from base rules, then layer phase-specific
and target-specific constraints.
"""

from pathlib import Path
from typing import Any

from constants import PhaseNames


class RuleSetBuilder:
    """
    Builds a dynamic rule set string suitable for Hermes system prompt injection.

    Usage:
        builder = RuleSetBuilder()
        rules = builder.with_phase("recon").with_target("10.10.11.5").build()
        # rules is a markdown string that can be appended to the system prompt
    """

    def __init__(self) -> None:
        self._phase: str = ""
        self._rhost: str = ""
        self._services: list[str] = []
        self._creds_found: bool = False
        self._is_hermes: bool = False

    def with_phase(self, phase: str) -> "RuleSetBuilder":
        """Set the current engagement phase."""
        self._phase = phase
        return self

    def with_target(self, rhost: str) -> "RuleSetBuilder":
        """Set the active target IP."""
        self._rhost = rhost
        return self

    def with_services(self, services: list[str]) -> "RuleSetBuilder":
        """Set discovered services (e.g., ['http:80', 'smb:445'])."""
        self._services = services
        return self

    def with_creds(self, found: bool) -> "RuleSetBuilder":
        """Set whether credentials have been discovered."""
        self._creds_found = found
        return self

    def with_hermes(self, is_hermes: bool) -> "RuleSetBuilder":
        """Set whether running inside a Hermes session."""
        self._is_hermes = is_hermes
        return self

    def build(self) -> str:
        """Build and return the complete rule set markdown."""
        lines: list[str] = ["## LazyOwn Dynamic Rules"]

        lines.extend(self._base_rules())
        lines.extend(self._phase_rules())
        lines.extend(self._service_rules())
        lines.extend(self._credential_rules())
        lines.extend(self._hermes_rules())

        return "\n".join(lines)

    # ── Internal rule generators ────────────────────────────────────────────────

    def _base_rules(self) -> list[str]:
        return [
            "",
            "### Base Rules",
            "",
            "1. ALWAYS call lazyown_session_init at the start of every session.",
            "2. NEVER write raw tool commands with hardcoded flags. Use LazyOwn abstract commands instead.",
            "3. NEVER assume target details. Read payload.json and scan files before reasoning.",
            "4. Document every command and finding for the next operator shift.",
            "5. When uncertain, ask the machine (recommend_next) rather than guessing.",
        ]

    def _phase_rules(self) -> list[str]:
        rules: list[str] = ["", f"### Phase Rules ({self._phase or 'unknown'})", ""]

        if self._phase == PhaseNames.RECON:
            rules.extend([
                "- Do NOT run exploitation tools during recon.",
                "- Preserve scan files; do not re-run if sessions/scan_<rhost>.nmap exists.",
                "- Report open ports, services, and OS guesses only.",
            ])
        elif self._phase == PhaseNames.ENUM:
            rules.extend([
                "- Focus on service-specific enumeration.",
                "- Compare findings against the world model; highlight deltas.",
                "- Stop when you have service versions and potential vectors.",
            ])
        elif self._phase == PhaseNames.EXPLOIT:
            rules.extend([
                "- Only attempt exploits matching the target service versions.",
                "- Verify each exploit with searchsploit/cve_search before execution.",
                "- Report success or failure with the exact error message.",
            ])
        elif self._phase == PhaseNames.PRIVESC:
            rules.extend([
                "- Run automated privesc scanners (linpeas/winpeas) before manual attempts.",
                "- Prioritize low-complexity vectors (SUID, sudo, writable paths).",
                "- Do NOT delete evidence or logs during privesc attempts.",
            ])
        elif self._phase == PhaseNames.CRED:
            rules.extend([
                "- Store every found credential in sessions/credentials.txt immediately.",
                "- Hashcat/john only if GPU/wordlist resources are confirmed available.",
                "- Test credentials against multiple services before reporting.",
            ])
        elif self._phase == PhaseNames.LATERAL:
            rules.extend([
                "- Use the least-privileged credential that achieves the move.",
                "- Map the network before pivoting; do not spray blindly.",
                "- Document each hop and the credential used.",
            ])
        else:
            rules.append("- Follow the kill-chain order: recon -> enum -> exploit -> postexp.")

        return rules

    def _service_rules(self) -> list[str]:
        if not self._services:
            return []

        rules: list[str] = ["", "### Service-Specific Rules", ""]
        for svc in self._services:
            if "smb" in svc.lower():
                rules.append("- SMB: enumerate shares, test null session, run crackmapexec.")
            if "http" in svc.lower() or "https" in svc.lower():
                rules.append("- HTTP/S: run whatweb, gobuster, nikto. Check for default creds.")
            if "ssh" in svc.lower():
                rules.append("- SSH: check banner, test key auth, avoid brute force without wordlist.")
            if "ldap" in svc.lower():
                rules.append("- LDAP: dump naming contexts, check anonymous bind.")
            if "kerberos" in svc.lower():
                rules.append("- Kerberos: run GetNPUsers, check AS-REP roasting.")

        return rules

    def _credential_rules(self) -> list[str]:
        if not self._creds_found:
            return []

        return [
            "",
            "### Credential Rules",
            "",
            "- Credentials exist. Test them across all discovered services before new attacks.",
            "- Update payload.json start_user/start_pass when valid creds are confirmed.",
            "- Use evil-winrm, psexec, or smbclient for lateral validation.",
        ]

    def _hermes_rules(self) -> list[str]:
        if not self._is_hermes:
            return []

        return [
            "",
            "### Hermes Integration Rules",
            "",
            "- Use the todo tool to track objectives derived from inject_objective.",
            "- Use delegate_task for parallel research (CVE, exploit search, OSINT).",
            "- Call checkpoint_write before long-running commands.",
            "- Respect max_turns: batch commands when possible to reduce turn count.",
        ]


def generate_rules(
    phase: str = "",
    rhost: str = "",
    services: list[str] | None = None,
    creds_found: bool = False,
    is_hermes: bool = False,
) -> str:
    """
    Convenience function: build a rule set from parameters.

    Args:
        phase: Current kill-chain phase.
        rhost: Active target IP.
        services: Discovered services strings.
        creds_found: Whether credentials are known.
        is_hermes: Whether running inside Hermes.

    Returns:
        A markdown string ready for system prompt injection.
    """
    return (
        RuleSetBuilder()
        .with_phase(phase)
        .with_target(rhost)
        .with_services(services or [])
        .with_creds(creds_found)
        .with_hermes(is_hermes)
        .build()
    )
