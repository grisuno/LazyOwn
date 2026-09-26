"""Actionable error advice with fix command and documentation link.

Every framework error renders four lines: what failed, why it failed,
the exact command that fixes it, and the documentation anchor. This
replaces bare red messages that forced operators to guess the remedy.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.console import DOCS_BASE_URL


@dataclass(frozen=True)
class ErrorAdviceConfig:
    """Centralized knobs for error advice rendering."""

    docs_base_url: str = DOCS_BASE_URL
    max_detail_len: int = 220


DEFAULT_CONFIG = ErrorAdviceConfig()


@dataclass(frozen=True)
class ErrorAdvice:
    """Structured remedy for one failure mode."""

    what: str
    why: str
    fix: str
    docs_anchor: str

    def docs_url(self, config: ErrorAdviceConfig = DEFAULT_CONFIG) -> str:
        """Return absolute documentation URL for this advice."""
        return f"{config.docs_base_url}{self.docs_anchor}"


_ADVICE: dict[str, ErrorAdvice] = {
    "tool_not_found:nmap": ErrorAdvice(
        what="nmap executable not found on PATH",
        why="Recon commands shell out to nmap and it is not installed",
        fix="sudo apt install nmap",
        docs_anchor="#nmap",
    ),
    "tool_not_found:gobuster": ErrorAdvice(
        what="gobuster executable not found on PATH",
        why="Web enumeration commands shell out to gobuster",
        fix="sudo apt install gobuster",
        docs_anchor="#gobuster",
    ),
    "config_missing:rhost": ErrorAdvice(
        what="Target address rhost is not set",
        why="Most commands read the target from payload.json",
        fix="assign rhost <target-IP>",
        docs_anchor="#configuration",
    ),
    "config_missing:lhost": ErrorAdvice(
        what="Attacker address lhost is not set",
        why="Payloads and listeners need a callback address",
        fix="assign lhost <your-IP>",
        docs_anchor="#configuration",
    ),
    "auth_failed": ErrorAdvice(
        what="Operator authentication failed",
        why="Credentials do not match any entry in users.json",
        fix="register <username> or login <username>",
        docs_anchor="#authentication",
    ),
}


def get_advice(key: str) -> ErrorAdvice | None:
    """Return advice for key or None when unknown.

    Args:
        key: Lookup key such as tool_not_found:nmap.

    Returns:
        Matching ErrorAdvice or None.
    """
    return _ADVICE.get(str(key).strip().lower())


def render_advice(key: str, config: ErrorAdviceConfig = DEFAULT_CONFIG) -> str:
    """Render advice as four plain lines with explicit level tags.

    Args:
        key: Lookup key.
        config: Rendering configuration.

    Returns:
        Multiline string, empty when the key is unknown.
    """
    advice = get_advice(key)
    if advice is None:
        return ""
    detail = str(advice.why)[: config.max_detail_len]
    return (
        f"[ERROR] {advice.what}\n"
        f"[INFO] Why: {detail}\n"
        f"[OK] Fix: {advice.fix}\n"
        f"[INFO] Docs: {advice.docs_url(config)}"
    )


__all__ = ["ErrorAdvice", "ErrorAdviceConfig", "DEFAULT_CONFIG", "get_advice", "render_advice"]
