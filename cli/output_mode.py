"""Structured output modes and dry-run rendering for CLI commands.

Piped automation needs JSON without ANSI. Operators skimming logs need
plain text. Sensitive engagements need to preview the exact shell line
before it runs. This module centralizes all three so every command
parses the same flags and formats the same way.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

_ANSI_RE: re.Pattern[str] = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


@dataclass(frozen=True)
class OutputModeConfig:
    """Centralized knobs for output formatting."""

    json_flag: str = "--json"
    plain_flag: str = "--plain"
    dry_run_flag: str = "--dry-run"
    force_flag: str = "--force"


DEFAULT_OUTPUT_CONFIG = OutputModeConfig()


@dataclass(frozen=True)
class OutputMode:
    """Parsed output flags for one command invocation."""

    as_json: bool = False
    plain: bool = False
    dry_run: bool = False
    force: bool = False
    rest: tuple[str, ...] = ()


def parse_output_flags(
    args: list[str],
    config: OutputModeConfig = DEFAULT_OUTPUT_CONFIG,
) -> OutputMode:
    """Split output control flags from positional command arguments.

    Args:
        args: Tokenised argument list.
        config: Flag spellings.

    Returns:
        OutputMode with flags set and remaining tokens in rest.
    """
    as_json = config.json_flag in args
    plain = config.plain_flag in args
    dry_run = config.dry_run_flag in args
    force = config.force_flag in args
    flags = {config.json_flag, config.plain_flag, config.dry_run_flag, config.force_flag}
    rest = tuple(a for a in args if a not in flags)
    return OutputMode(as_json=as_json, plain=plain, dry_run=dry_run, force=force, rest=rest)


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from text.

    Args:
        text: Possibly coloured string.

    Returns:
        Plain string with escapes removed.
    """
    return _ANSI_RE.sub("", str(text))


def format_output(data: Any, mode: OutputMode) -> str:
    """Render data according to the parsed output mode.

    Args:
        data: Mapping, sequence or preformatted string.
        mode: Parsed flags from parse_output_flags.

    Returns:
        JSON document when as_json, ANSI-stripped text when plain,
        otherwise the string form unchanged.
    """
    if mode.as_json:
        if isinstance(data, str):
            return json.dumps({"output": strip_ansi(data)}, indent=2)
        return json.dumps(data, indent=2, default=str)
    text = data if isinstance(data, str) else json.dumps(data, indent=2, default=str)
    if mode.plain:
        return strip_ansi(text)
    return text


def dry_run_line(command: str) -> str:
    """Render the exact shell line that would run without running it.

    Args:
        command: Shell line preview.

    Returns:
        Single tagged line.
    """
    return f"[INFO] dry-run: {command}"


__all__ = [
    "OutputMode",
    "OutputModeConfig",
    "DEFAULT_OUTPUT_CONFIG",
    "parse_output_flags",
    "strip_ansi",
    "format_output",
    "dry_run_line",
]
