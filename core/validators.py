"""Input validators for runtime configuration values.

These helpers were historically in ``utils.py`` and are imported by ~280 CLI
commands and ~80 C2 routes. They emit a coloured error message to stdout and
return ``False`` when the value is missing, so callers can short-circuit
without raising.
"""

from __future__ import annotations

from typing import Any

from core.console import GREEN, RESET, WHITE, print_error
from core.host_policy import _SHELL_META_CHARS
from core.host_policy import is_valid_host as _is_valid_host

__all__ = [
    "_SHELL_META_CHARS",
    "check_rhost",
    "check_lhost",
    "check_lport",
    "check_port",
]


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


def require_rhost(params: Any) -> bool:
    """Gate a command on a valid ``rhost`` looked up from ``params``.

    Replaces the ``params['rhost']`` + ``check_rhost`` two-liner with a
    single fail-closed call that never raises ``KeyError`` on a
    missing key.

    Args:
        params: Live params mapping (``self.params`` in CommandSets).

    Returns:
        Result of :func:`check_rhost` on the looked-up value.
    """
    value = params.get("rhost") if hasattr(params, "get") else None
    return check_rhost(value)


def require_lhost(params: Any) -> bool:
    """Gate a command on a valid ``lhost`` looked up from ``params``.

    Args:
        params: Live params mapping (``self.params`` in CommandSets).

    Returns:
        Result of :func:`check_lhost` on the looked-up value.
    """
    value = params.get("lhost") if hasattr(params, "get") else None
    return check_lhost(value)


def require_lport(params: Any) -> bool:
    """Gate a command on a valid ``lport`` looked up from ``params``.

    Args:
        params: Live params mapping (``self.params`` in CommandSets).

    Returns:
        Result of :func:`check_lport` on the looked-up value.
    """
    value = params.get("lport") if hasattr(params, "get") else None
    return check_lport(value)


def require_rport(params: Any) -> bool:
    """Gate a command on a valid ``rport`` looked up from ``params``.

    Args:
        params: Live params mapping (``self.params`` in CommandSets).

    Returns:
        Result of :func:`check_port` on the looked-up value.
    """
    value = params.get("rport") if hasattr(params, "get") else None
    return check_port(value, name="rport")


__all__ = [
    "check_rhost",
    "check_lhost",
    "check_lport",
    "check_port",
    "require_rhost",
    "require_lhost",
    "require_lport",
    "require_rport",
]
