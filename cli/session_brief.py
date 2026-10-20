"""Consolidated session-start brief for the LazyOwn shell.

The shell used to print scattered startup noise (auth warnings, one
session tip, chain prompts, toasts). This contract owns one short
campaign overview instead: target, derived world-model phase,
autonomous tasks, loop-throttled verb count and declarative trigger
count in a single panel. Every collaborator failure collapses into its
muted placeholder line so the brief can never block or crash the shell.

Single responsibility: rendering one startup panel. Persistence stays
in ``modules.world_model`` (world model), ``modules.lazy_loop``
(tasks), ``modules.verb_catalog`` (verbs) and
``modules.trigger_policy`` (triggers); the shell only injects
``payload.json`` and the ``ui_hints`` gate.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from rich.panel import Panel
from rich.text import Text

BRIEF_PHASE_PLACEHOLDER = "recon"
BRIEF_TASK_PLACEHOLDER = "no loop tasks"
BRIEF_WORLD_PLACEHOLDER = "no world-model data yet"
LEGACY_ENV_SESSIONS = "LAZY_SESSIONS_DIR"

RUNNING_STATUS_PREFIXES = ("running", "paused")


@dataclass(frozen=True)
class SessionBriefConfig:
    """Display knobs for the startup brief."""

    title: str = "session brief"
    goal_cap: int = 60
    hint_key: str = "ui_hints"
    hint_off_values: tuple[str, ...] = ("off", "false", "0", "no")


SESSION_BRIEF = SessionBriefConfig()


def brief_enabled(payload: Mapping[str, Any] | None) -> bool:
    """Return False when the UI hints continuity suppresses the brief."""
    if not payload:
        return True
    raw = str(payload.get(SESSION_BRIEF.hint_key, "on") or "on").strip().lower()
    return raw not in SESSION_BRIEF.hint_off_values


def _redirect_world_model_env(payload: Mapping[str, Any]) -> None:
    """Point the world-model singleton at the operator's sandbox root."""
    import os as _os
    from pathlib import Path as _Path

    override = (_os.environ.get(LEGACY_ENV_SESSIONS) or "").strip()
    if not override:
        return
    from modules import world_model as world_model_module

    world_model_module._DEFAULT_PATH = str(_Path(override) / "world_model.json")


def _world_line(payload: Mapping[str, Any]) -> str:
    """Return the world-model phase line, falling back to a placeholder."""
    try:
        _redirect_world_model_env(payload)
        from modules.world_model import get_world_model

        model = get_world_model()
        hosts = dict(model.get_hosts_summary())
        if not hosts:
            return BRIEF_WORLD_PLACEHOLDER
        phase = str(getattr(model.get_phase(), "value", model.get_phase())).strip().lower()
        return f"world phase={phase} hosts={len(hosts)}"
    except Exception:
        return BRIEF_WORLD_PLACEHOLDER


def fetch_task_rows() -> list[dict]:
    """Read the full task rows from the loop store, never raising."""
    try:
        from modules.lazy_engine import TaskStore

        return list(TaskStore().list())
    except Exception:
        return []


def _task_line(rows: list[dict]) -> str:
    """Return the newest running loop task line, or the placeholder."""
    running = [
        row
        for row in rows
        if str(row.get("status", "")).lower().startswith(RUNNING_STATUS_PREFIXES)
    ]
    if not running:
        return BRIEF_TASK_PLACEHOLDER
    newest = max(running, key=lambda row: float(row.get("updated", 0.0) or 0.0))
    goal = str(newest.get("goal", ""))[: SESSION_BRIEF.goal_cap].strip() or "-"
    return (
        f"loop task={newest.get('task_id', '')} status={newest.get('status', '')} goal={goal}"
    )


def _verb_line() -> str:
    """Return the loop verb catalog summary line, or a placeholder."""
    try:
        from modules.verb_catalog import stats

        overview = stats()
    except Exception:
        return "verbs unavailable"
    return (
        f"verbs on={overview['on']} off={overview['off']} total={overview['total']}"
    )


def _trigger_line() -> str:
    """Return the declarative trigger summary line, or a placeholder."""
    try:
        from modules.trigger_policy import export_store

        rows = export_store()
    except Exception:
        return "triggers unavailable"
    on = sum(1 for row in rows if row.get("enabled"))
    return f"triggers={len(rows)} ({on} on)"


def build_session_brief(
    payload: Mapping[str, Any],
    tasks: list[dict] | None = None,
) -> Panel:
    """Build the one-startup campaign brief panel.

    Args:
        payload: Active ``payload.json`` mapping.
        tasks: Optional pre-fetched task rows (tests sandbox the store).

    Returns:
        A Rich panel with ``label=value`` pairs so the operator can grep
        the block instead of reading prose.
    """
    cfg = SESSION_BRIEF
    target = str(payload.get("rhost") or "unset")
    os_id = str(payload.get("os_id") or "unknown")
    domain = str(payload.get("domain") or "-")
    lhost = str(payload.get("lhost") or "unset")
    text = Text()
    text.append(f"target rhost={target} lhost={lhost} os={os_id} domain={domain}\n")
    text.append(f"{_world_line(payload)}\n")
    text.append(f"{_task_line(fetch_task_rows() if tasks is None else tasks)}\n")
    text.append(f"{_verb_line()}\n")
    text.append(_trigger_line())
    from cli.themes import theme_from_payload

    theme = theme_from_payload(payload)
    return Panel(
        text,
        title=f"[bold]{cfg.title}[/bold]",
        border_style=theme.border,
        padding=(0, 1),
    )


def print_session_brief(console: Any, payload: Mapping[str, Any]) -> bool:
    """Render the brief through ``console`` when UI hints allow.

    Args:
        console: The shell's Rich console.
        payload: Active ``payload.json`` mapping.

    Returns:
        ``True`` when the brief printed.
    """
    if not brief_enabled(payload):
        return False
    console.print(build_session_brief(payload))
    return True


__all__ = [
    "SESSION_BRIEF",
    "SessionBriefConfig",
    "brief_enabled",
    "build_session_brief",
    "fetch_task_rows",
    "print_session_brief",
]
