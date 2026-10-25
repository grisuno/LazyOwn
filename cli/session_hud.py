"""Compact session HUD: the numbers no other command shows.

``killchain`` already owns the kill-chain view and does it better, with
per-phase percentages. ``sitrep`` owns the full operational picture. This
module covers only the gap: how long the session has run, how many
commands it has executed, and how much material it has captured.

Every figure comes from a source that actually exists on disk. Credential
and note counts use the same globs as the dashboard
(``credentials*.txt``, ``notes*.txt``); the command count and the session
clock come from the engagement state, which is the only component that
knows when the session started.
"""

from __future__ import annotations

import glob as _glob
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class HudConfig:
    """Centralized knobs for HUD data sources."""

    sessions_dir: str = "sessions"
    bar_width: int = 10
    credential_globs: tuple[str, ...] = ("credentials*.txt",)
    notes_globs: tuple[str, ...] = ("notes*.txt",)
    transcript_name: str = "LazyOwn_session_report.csv"
    not_set: str = "not set"
    default_phase: str = "recon"


DEFAULT_HUD_CONFIG = HudConfig()

_KILL_PHASES: tuple[str, ...] = (
    "recon",
    "enum",
    "exploit",
    "privesc",
    "lateral",
    "persist",
)


@dataclass(frozen=True)
class HudSnapshot:
    """Point-in-time values displayed by the HUD."""

    target: str
    phase: str
    session_commands: int
    total_commands: int
    creds: int
    notes: int
    elapsed: str


def count_lines_in_globs(root: str, patterns: tuple[str, ...]) -> int:
    """Count non-empty lines across every file matching the patterns.

    Args:
        root: Directory holding the session artefacts.
        patterns: Glob patterns relative to ``root``.

    Returns:
        Total non-empty line count, zero when nothing matches.
    """
    total = 0
    for pattern in patterns:
        for path in _glob.glob(str(Path(root) / pattern)):
            try:
                with open(path, encoding="utf-8", errors="ignore") as handle:
                    total += sum(1 for line in handle if line.strip())
            except OSError:
                continue
    return total


def count_csv_rows(path: Path) -> int:
    """Count data rows in a CSV file without loading it fully.

    Args:
        path: CSV file path.

    Returns:
        Number of data rows, zero when missing or unreadable.
    """
    try:
        with path.open(encoding="utf-8", errors="ignore") as handle:
            lines = sum(1 for line in handle if line.strip())
        return max(lines - 1, 0)
    except OSError:
        return 0


def format_elapsed(seconds: float) -> str:
    """Format a duration as HH:MM:SS.

    Args:
        seconds: Duration in seconds.

    Returns:
        Zero-padded clock string.
    """
    total = max(0, int(seconds))
    hours, rest = divmod(total, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def phase_bar(phase: str, width: int = DEFAULT_HUD_CONFIG.bar_width) -> str:
    """Render kill-chain progress as filled and empty blocks.

    Args:
        phase: Current phase name.
        width: Bar width in characters.

    Returns:
        String such as [###-------] exploit.
    """
    normalized = str(phase or "").lower().strip()
    try:
        index = _KILL_PHASES.index(normalized)
    except ValueError:
        index = 0
    filled = int(round((index + 1) / len(_KILL_PHASES) * width))
    filled = min(max(filled, 1), width)
    return f"[{'#' * filled}{'-' * (width - filled)}] {normalized or 'recon'}"


def _engagement_facts() -> tuple[int, int, float]:
    """Read session command count, total count and session start time.

    Returns:
        Tuple of (session_commands, total_commands, elapsed_seconds).
        Zeros when the engagement state is unavailable.
    """
    try:
        from cli.engagement_hooks import get_state_snapshot

        snap = get_state_snapshot()
    except Exception:
        return 0, 0, 0.0
    session_commands = int(snap.get("session_commands", 0) or 0)
    total = int(snap.get("total_commands", 0) or 0)
    start = float(snap.get("session_start_ts", 0) or 0)
    elapsed = max(0.0, time.time() - start) if start > 0 else 0.0
    return session_commands, total, elapsed


def build_snapshot(
    params: dict[str, Any],
    config: HudConfig = DEFAULT_HUD_CONFIG,
) -> HudSnapshot:
    """Build a snapshot from live params, engagement state and session files.

    Args:
        params: Live payload mapping with rhost and phase keys.
        config: HUD configuration.

    Returns:
        Populated HudSnapshot with every figure read from a real source.
    """
    session_commands, total_commands, elapsed = _engagement_facts()
    return HudSnapshot(
        target=str(params.get("rhost", "") or config.not_set),
        phase=str(params.get("phase", "") or config.default_phase),
        session_commands=session_commands,
        total_commands=total_commands,
        creds=count_lines_in_globs(config.sessions_dir, config.credential_globs),
        notes=count_lines_in_globs(config.sessions_dir, config.notes_globs),
        elapsed=format_elapsed(elapsed),
    )


def render_snapshot(snapshot: HudSnapshot, config: HudConfig = DEFAULT_HUD_CONFIG) -> list[str]:
    """Render the session counters as two plain lines.

    No kill-chain bar: ``killchain`` renders phases with per-phase
    percentages and duplicating a worse version of it here only confused
    the operator. Level markers are omitted too, because the shell
    printers in ``core.console`` already emit one per line.

    Args:
        snapshot: Values to display.
        config: HUD configuration.

    Returns:
        List of plain lines, one per HUD row.
    """
    return [
        f"session elapsed={snapshot.elapsed} cmds_here={snapshot.session_commands} "
        f"cmds_total={snapshot.total_commands}",
        f"captured creds={snapshot.creds} notes={snapshot.notes}",
    ]


__all__ = [
    "HudConfig",
    "DEFAULT_HUD_CONFIG",
    "HudSnapshot",
    "build_snapshot",
    "render_snapshot",
    "phase_bar",
    "format_elapsed",
    "count_csv_rows",
    "count_lines_in_globs",
]
