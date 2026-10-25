"""Capability installer for the Lazy autonomous loop.

Ports the installer-agent idea with Lazy safety semantics: the loop never
invents install commands. A fixed allowlist maps missing tool binaries to
reviewed one-line install recipes; anything off-list yields no intent.
Install intents only resolve when the payload flag ``installer_enabled``
is set (default off), and every install still crosses the normal Guard
and intercept path, so pairing this with an ask-rule
(``lazy_guard rule-add "apt-get install" ask installs-write-to-host``)
keeps host mutation operator-gated.

Stdlib only.
"""

from __future__ import annotations

INSTALL_INTENT_PREFIX = "install capability "

TOOL_INSTALL: dict[str, str] = {
    "chisel": "go install github.com/jpillora/chisel@latest",
    "socat": "sudo -n apt-get install -y socat",
    "msfconsole": "sudo -n apt-get install -y metasploit-framework",
    "nmap": "sudo -n apt-get install -y nmap",
    "masscan": "sudo -n apt-get install -y masscan",
    "gobuster": "sudo -n apt-get install -y gobuster",
    "ffuf": "sudo -n apt-get install -y ffuf",
    "feroxbuster": "sudo -n apt-get install -y feroxbuster",
    "hydra": "sudo -n apt-get install -y hydra",
    "john": "sudo -n apt-get install -y john",
    "sqlmap": "sudo -n apt-get install -y sqlmap",
    "smbclient": "sudo -n apt-get install -y smbclient",
    "nikto": "sudo -n apt-get install -y nikto",
    "whatweb": "sudo -n apt-get install -y whatweb",
    "enum4linux": "sudo -n apt-get install -y enum4linux",
    "crackmapexec": "sudo -n apt-get install -y crackmapexec",
    "evil-winrm": "gem install evil-winrm",
    "impacket-secretsdump": "pipx install impacket",
}


def installer_enabled() -> bool:
    """Return whether the loop may resolve install intents.

    Reads ``payload.json`` -> ``orchestrator`` -> ``installer``. Defaults
    to off so host mutation stays an explicit operator decision. The flag
    lives under the free-form orchestrator section so enabling it never
    adds a top-level payload key (the schema-coverage contract).
    """
    try:
        from core.config import load_payload

        section = (load_payload() or {}).get("orchestrator") or {}
        return bool(section.get("installer", False))
    except Exception:
        return False


def set_installer_enabled(enabled: bool) -> bool:
    """Persist the installer flag and return the stored value."""
    from core.config import load_payload, save_payload

    payload = dict(load_payload() or {})
    section = dict(payload.get("orchestrator") or {})
    section["installer"] = bool(enabled)
    payload["orchestrator"] = section
    save_payload(payload)
    return bool(enabled)


def install_command_for(tool: str) -> str | None:
    """Return the allowlisted install recipe for one tool, or None."""
    return TOOL_INSTALL.get((tool or "").strip().lower())


def intent_for(tool: str) -> str:
    """Build the canonical install intent summary for one tool."""
    return f"{INSTALL_INTENT_PREFIX}{(tool or '').strip().lower()}".strip()


def tool_from_intent(text: str) -> str:
    """Extract the tool name from an install intent, else empty string."""
    lowered = (text or "").strip().lower()
    if not lowered.startswith(INSTALL_INTENT_PREFIX):
        return ""
    return lowered[len(INSTALL_INTENT_PREFIX):].split()[0] if lowered[len(INSTALL_INTENT_PREFIX):].split() else ""


def steps_for_install(text: str) -> list[str] | None:
    """Resolve an install intent to its recipe, or None.

    Returns None when the installer is disabled, the tool is already
    present, or the tool has no allowlisted recipe.
    """
    tool = tool_from_intent(text)
    if not tool or not installer_enabled():
        return None
    try:
        from modules.auto_registry import binary_available

        if binary_available(tool) or binary_available(tool.split("-")[0]):
            return None
    except Exception:
        pass
    recipe = install_command_for(tool)
    return [recipe] if recipe else None


__all__ = [
    "INSTALL_INTENT_PREFIX",
    "TOOL_INSTALL",
    "installer_enabled",
    "install_command_for",
    "intent_for",
    "set_installer_enabled",
    "steps_for_install",
    "tool_from_intent",
]
