"""Input validators for runtime configuration values.

These helpers were historically in ``utils.py`` and are imported by ~280 CLI
commands and ~80 C2 routes. They emit a coloured error message to stdout and
return ``False`` when the value is missing, so callers can short-circuit
without raising.
"""

from __future__ import annotations

from typing import Any

from core.console import GREEN, RESET, WHITE, print_error


def check_rhost(rhost: Any) -> bool:
    """Return ``True`` if ``rhost`` is set, otherwise print an error and return ``False``."""
    if not rhost:
        print_error(
            f"rhost must be set, {GREEN}Example: set rhost 10.10.10.10, "
            f"{WHITE}more info see help set, or help <TOPIC> {RESET}"
        )
        return False
    return True


def check_lhost(lhost: Any) -> bool:
    """Return ``True`` if ``lhost`` is set, otherwise print an error and return ``False``."""
    if not lhost:
        print_error(
            f"lhost must be set, {GREEN}Example: set lhost 10.10.10.10, "
            f"{WHITE}more info see help set, or help <TOPIC> {RESET}"
        )
        return False
    return True


def check_lport(lport: Any) -> bool:
    """Return ``True`` if ``lport`` is set, otherwise print an error and return ``False``."""
    if not lport:
        print_error(
            f"lport must be set, {GREEN}Example: set lport 5555, {WHITE}more info see help set, or help <TOPIC> {RESET}"
        )
        return False
    return True


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
