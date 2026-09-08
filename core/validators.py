"""Input validators for runtime configuration values.

These helpers were historically in ``utils.py`` and are imported by ~280 CLI
commands and ~80 C2 routes. They emit a coloured error message to stdout and
return ``False`` when the value is missing, so callers can short-circuit
without raising.
"""

from __future__ import annotations

from typing import Any

from core.console import GREEN, RESET, WHITE, print_error

_HOST_RE = __import__("re").compile(r"^(?=.{1,253}$)([A-Za-z0-9]([A-Za-z0-9._-]{0,251}[A-Za-z0-9])?)$")
_SHELL_META_CHARS = frozenset(";&|`$(){}!><*?~#\\'\"\n\r")


def _rejects_shell_meta(value: str) -> bool:
    """Return True when value contains characters usable for shell injection."""
    return any(ch in _SHELL_META_CHARS for ch in value)


def _is_valid_host(value: object) -> bool:
    """Check value is a plain IP, CIDR, or hostname without shell metacharacters."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text or len(text) > 253 or _rejects_shell_meta(text):
        return False
    import ipaddress

    candidate = text.split("/")[0] if "/" in text else text
    try:
        ipaddress.ip_address(candidate)
        return "/" not in text or _is_valid_cidr(text)
    except ValueError:
        pass
    if "/" in text:
        return _is_valid_cidr(text)
    return _HOST_RE.match(text) is not None


def _is_valid_cidr(value: str) -> bool:
    """Check value is a valid CIDR block."""
    import ipaddress

    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def check_rhost(rhost: Any) -> bool:
    """Return ``True`` if ``rhost`` is set, otherwise print an error and return ``False``."""
    if not rhost:
        print_error(
            f"rhost must be set, {GREEN}Example: assign rhost 10.10.10.10, "
            f"{WHITE}more info see help assign, or help <TOPIC> {RESET}"
        )
        return False
    if not _is_valid_host(rhost):
        print_error(f"rhost has an invalid format or unsafe characters: {rhost!r}")
        return False
    return True


def check_lhost(lhost: Any) -> bool:
    """Return ``True`` if ``lhost`` is set, otherwise print an error and return ``False``."""
    if not lhost:
        print_error(
            f"lhost must be set, {GREEN}Example: assign lhost 10.10.10.10, "
            f"{WHITE}more info see help assign, or help <TOPIC> {RESET}"
        )
        return False
    if not _is_valid_host(lhost):
        print_error(f"lhost has an invalid format or unsafe characters: {lhost!r}")
        return False
    return True


def check_lport(lport: Any) -> bool:
    """Return ``True`` if ``lport`` is set, otherwise print an error and return ``False``."""
    if not lport:
        print_error(
            f"lport must be set, {GREEN}Example: assign lport 5555, {WHITE}more info see help assign, or help <TOPIC> {RESET}"
        )
        return False
    return check_port(lport, name="lport")


def check_port(port: Any, name: str = "port") -> bool:
    """Return ``True`` if ``port`` is a valid TCP/UDP port (1-65535)."""
    try:
        value = int(port)
    except (TypeError, ValueError):
        print_error(f"{name} must be an integer between 1 and 65535")
        return False
    if not (1 <= value <= 65535):
        print_error(f"{name} must be between 1 and 65535, got {value}")
        return False
    return True


__all__ = ["check_rhost", "check_lhost", "check_lport", "check_port"]
