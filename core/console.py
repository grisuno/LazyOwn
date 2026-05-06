"""ANSI color constants and console output helpers.

This module is the single source of truth for terminal styling and the
``print_msg`` / ``print_warn`` / ``print_error`` / ``print_succ`` helpers used
throughout the framework. ``utils.py`` re-exports these names for backwards
compatibility with the historical import path ``from utils import print_msg``.
"""

from __future__ import annotations

RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
INVERT = "\033[7m"
BLINK = "\033[5m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

COLOR_256 = "\033[38;5;{}m"
BG_COLOR_256 = "\033[48;5;{}m"
TRUE_COLOR = "\033[38;2;{};{};{}m"
BG_TRUE_COLOR = "\033[48;2;{};{};{}m"

SURROGATE_CHARS = dict.fromkeys(range(0xD800, 0xE000))
TRANSLATION_TABLE = str.maketrans(SURROGATE_CHARS)

ERROR_PREFIX = "[-]"
INFO_PREFIX = "[+]"
WARN_PREFIX = "[~]"
SUCCESS_PREFIX = "[*]"

ERROR_GLYPH = "[☠]"
INFO_GLYPH = "[\U0001f47d]"
WARN_GLYPH = "[⚠]"
SUCCESS_GLYPH = "[✓]"


def _sanitize(text: object) -> str:
    """Return ``text`` coerced to ``str`` with surrogate code points stripped."""
    return str(text).translate(TRANSLATION_TABLE)


def print_error(error: object) -> None:
    """Print a red error message to stdout."""
    print(f"    {YELLOW}{ERROR_PREFIX}{RED} {_sanitize(error)}{RESET} {ERROR_GLYPH}")


def print_msg(msg: object) -> None:
    """Print a green informational message to stdout."""
    print(f"    {GREEN}{INFO_PREFIX}{WHITE} {_sanitize(msg)}{RESET} {INFO_GLYPH}")


def print_warn(warn: object) -> None:
    """Print a magenta/yellow warning message to stdout."""
    print(f"    {MAGENTA}{WARN_PREFIX}{YELLOW} {_sanitize(warn)}{RESET} {WARN_GLYPH}")


def print_succ(msg: object) -> None:
    """Print a bright green success message to stdout."""
    print(f"    {BRIGHT_GREEN}{SUCCESS_PREFIX}{WHITE} {_sanitize(msg)}{RESET} {SUCCESS_GLYPH}")


__all__ = [
    "RESET",
    "BOLD",
    "UNDERLINE",
    "INVERT",
    "BLINK",
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "WHITE",
    "BG_BLACK",
    "BG_RED",
    "BG_GREEN",
    "BG_YELLOW",
    "BG_BLUE",
    "BG_MAGENTA",
    "BG_CYAN",
    "BG_WHITE",
    "BRIGHT_BLACK",
    "BRIGHT_RED",
    "BRIGHT_GREEN",
    "BRIGHT_YELLOW",
    "BRIGHT_BLUE",
    "BRIGHT_MAGENTA",
    "BRIGHT_CYAN",
    "BRIGHT_WHITE",
    "BG_BRIGHT_BLACK",
    "BG_BRIGHT_RED",
    "BG_BRIGHT_GREEN",
    "BG_BRIGHT_YELLOW",
    "BG_BRIGHT_BLUE",
    "BG_BRIGHT_MAGENTA",
    "BG_BRIGHT_CYAN",
    "BG_BRIGHT_WHITE",
    "COLOR_256",
    "BG_COLOR_256",
    "TRUE_COLOR",
    "BG_TRUE_COLOR",
    "SURROGATE_CHARS",
    "TRANSLATION_TABLE",
    "print_msg",
    "print_warn",
    "print_error",
    "print_succ",
]
