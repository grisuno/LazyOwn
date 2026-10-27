"""Non-blocking toast notification subsystem for the LazyOwn shell.

After each command the postcmd hook calls :func:`render_toasts` which
tails ``sessions/*.jsonl`` event files, deduplicates events the operator
has already seen, and prints at most ``toast_max_per_tick`` formatted
lines to stdout. Toasts surface daemon decisions, beacon callbacks,
collab events, and reactive escalations without forcing the operator
into ``poll_events`` or the SSE feed.

Design (SOLID):

- Single Responsibility: :class:`ToastConfig` owns constants,
  :class:`ToastState` persists the seen offsets, :class:`ToastReader`
  reads the JSONL files, :class:`ToastFormatter` renders a line,
  :class:`ToastBus` orchestrates.
- Open/Closed: a new event source is one extra entry in
  :attr:`ToastConfig.event_files`.
- Dependency Inversion: every collaborator is supplied to
  :class:`ToastBus` through the constructor so tests substitute fakes.
- No magic numbers / hardcoded paths: every value lives in
  :class:`ToastConfig` and overrides flow through ``payload.json``.
"""

from __future__ import annotations

import json
import os
import textwrap
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

from cli.themes import Theme, theme_from_payload


@dataclass(frozen=True)
class ToastConfig:
    """Centralised constants for the toast subsystem."""

    enabled_key: str = "enable_toasts"
    max_per_tick_key: str = "toast_max_per_tick"
    sessions_dir: str = "sessions"
    state_filename: str = ".toast_state.json"
    event_files: tuple[str, ...] = (
        "events.jsonl",
        "autonomous_events.jsonl",
        "activity_*.jsonl",
    )
    enabled_default: bool = True
    max_per_tick_default: int = 5
    max_line_chars: int = 96
    max_panel_width: int = 120
    fallback_width: int = 80
    max_offset_value: int = 1_073_741_824
    truthy_strings: tuple[str, ...] = ("1", "true", "yes", "on")
    falsy_strings: tuple[str, ...] = ("0", "false", "no", "off")
    severity_styles: Mapping[str, str] = field(
        default_factory=lambda: {
            "error": "danger",
            "danger": "danger",
            "critical": "danger",
            "warn": "warning",
            "warning": "warning",
            "info": "accent",
            "success": "success",
        }
    )
    default_role: str = "muted"
    truncation_suffix: str = "..."
    prominent_roles: tuple[str, ...] = ("danger", "warning")
    prominent_kinds: tuple[str, ...] = ("ENGAGE_DONE",)
    prominent_max_chars: int = 800
    prefix_glyph: str = ">>"
    file_offset_separator: str = "::"
    skip_event_types: tuple[str, ...] = ()
    ephemeral_key: str = "toast_ephemeral"
    ephemeral_default: bool = False
    ephemeral_durations: Mapping[str, float] = field(
        default_factory=lambda: {
            "success": 3.0,
            "info": 4.0,
            "warning": 6.0,
            "error": 8.0,
            "danger": 8.0,
            "critical": 8.0,
            "loading": 0.0,
        }
    )
    ephemeral_default_duration: float = 4.0
    ephemeral_icons: Mapping[str, str] = field(
        default_factory=lambda: {
            "success": "\u2714",
            "info": "\u2139",
            "warning": "\u26a0",
            "error": "\u2716",
            "danger": "\u2716",
            "critical": "\u2716",
            "loading": "\u23f3",
        }
    )
    ephemeral_max_chars: int = 200


@dataclass(frozen=True)
class ToastEvent:
    """Immutable record produced by :class:`ToastReader`."""

    source: str
    offset: int
    event_type: str
    severity: str
    summary: str
    timestamp: str


class ToastState:
    """Persist the last byte offset consumed from each event file.

    The state file lives under ``sessions/.toast_state.json``. The schema
    is intentionally trivial: ``{"offsets": {"events.jsonl": 4096, ...}}``.
    Atomic writes (tmp + rename) keep the file safe under SIGINT.
    """

    def __init__(self, config: ToastConfig, root: Path | None = None) -> None:
        """Bind to config and resolve the on-disk state path.

        Args:
            config: Active toast configuration.
            root: Optional override for the sessions root directory.
        """
        self._config = config
        base = Path(root) if root is not None else Path(config.sessions_dir)
        self._root = base
        self._path = base / config.state_filename
        self._offsets: dict[str, int] = {}
        self._loaded = False

    @property
    def path(self) -> Path:
        """Return the resolved state-file path."""
        return self._path

    def get(self, name: str) -> int:
        """Return the persisted offset for ``name`` or 0."""
        self._ensure_loaded()
        return int(self._offsets.get(name, 0))

    def set(self, name: str, offset: int) -> None:
        """Record ``offset`` for ``name`` in memory."""
        self._ensure_loaded()
        bounded = max(0, min(int(offset), self._config.max_offset_value))
        self._offsets[name] = bounded

    def reset(self) -> None:
        """Forget every persisted offset (force replay on next read)."""
        self._offsets = {}
        self._loaded = True

    def flush(self) -> bool:
        """Persist the current offsets atomically.

        Returns:
            ``True`` on success, ``False`` when the filesystem rejects the
            write (read-only mount, missing parent, etc.).
        """
        self._ensure_loaded()
        try:
            self._root.mkdir(parents=True, exist_ok=True)
            tmp = self._path.with_suffix(self._path.suffix + ".tmp")
            payload = json.dumps({"offsets": self._offsets}, sort_keys=True)
            tmp.write_text(payload, encoding="utf-8")
            os.replace(tmp, self._path)
            return True
        except OSError:
            return False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        if not self._path.is_file():
            return
        try:
            raw = self._path.read_text(encoding="utf-8")
            data = json.loads(raw) if raw else {}
        except (OSError, ValueError, json.JSONDecodeError):
            return
        offsets = data.get("offsets") if isinstance(data, dict) else None
        if not isinstance(offsets, dict):
            return
        for key, value in offsets.items():
            if not isinstance(key, str):
                continue
            if isinstance(value, (int, float)):
                self._offsets[key] = max(0, min(int(value), self._config.max_offset_value))


class ToastReader:
    """Read unseen JSONL events from a single file via byte offset."""

    def __init__(self, config: ToastConfig, root: Path | None = None) -> None:
        """Bind to config and resolve the events root directory.

        Args:
            config: Active configuration.
            root: Optional override for the sessions root directory.
        """
        self._config = config
        self._root = Path(root) if root is not None else Path(config.sessions_dir)

    @property
    def root(self) -> Path:
        """Return the resolved events root directory."""
        return self._root

    def read_unseen(self, name: str, start_offset: int) -> tuple[list[ToastEvent], int]:
        """Return events emitted past ``start_offset`` plus the new end offset.

        Args:
            name: Filename relative to the sessions root (call
                :meth:`resolve_sources` first for glob patterns).
            start_offset: Last persisted byte offset for this file.

        Returns:
            ``(events, end_offset)``. ``events`` is empty when the file is
            missing, truncated, or already consumed. ``end_offset`` matches
            the file size at the moment of read.
        """
        path = self._root / name
        if not path.is_file():
            return [], start_offset
        try:
            size = path.stat().st_size
        except OSError:
            return [], start_offset
        if size <= start_offset:
            return [], start_offset
        try:
            with path.open("rb") as handle:
                handle.seek(max(0, start_offset))
                raw = handle.read(max(0, size - start_offset))
        except OSError:
            return [], start_offset
        text = raw.decode("utf-8", errors="ignore")
        events = self._parse(text, name, base_offset=start_offset)
        return events, size

    def resolve_sources(self, names: tuple[str, ...]) -> tuple[tuple[str, ...], bool]:
        """Expand glob source entries against the sessions root.

        Args:
            names: Configured source names, possibly glob patterns.

        Returns:
            ``(resolved_names, changed)`` where ``changed`` is True when
            expansion produced anything different from the input tree.
        """
        resolved: list[str] = []
        changed = False
        for name in names:
            if not any(glob_char in name for glob_char in "*?["):
                resolved.append(name)
                continue
            try:
                matches = sorted(p.name for p in self._root.glob(name) if p.is_file())
            except (OSError, ValueError):
                matches = []
            if sorted(matches) != [name]:
                changed = True
            resolved.extend(matches)
        tuple_resolved = tuple(resolved) if resolved else names
        if list(tuple_resolved) != list(names):
            return tuple_resolved, True
        return tuple_resolved, changed

    def _parse(self, text: str, source: str, base_offset: int) -> list[ToastEvent]:
        out: list[ToastEvent] = []
        cursor = base_offset
        for raw_line in text.splitlines(keepends=True):
            stripped = raw_line.strip()
            cursor_after = cursor + len(raw_line.encode("utf-8"))
            if not stripped:
                cursor = cursor_after
                continue
            event = self._build_event(stripped, source, cursor_after)
            if event is not None:
                out.append(event)
            cursor = cursor_after
        return out

    def _build_event(self, line: str, source: str, offset: int) -> ToastEvent | None:
        try:
            record = json.loads(line)
        except (ValueError, json.JSONDecodeError):
            return None
        if not isinstance(record, dict):
            return None
        worker = self._coerce_str(record.get("worker") or "")
        if record.get("type"):
            event_type = self._coerce_str(record["type"])
        elif worker:
            event_type = worker
        else:
            event_type = self._coerce_str(record.get("kind") or record.get("event") or record.get("event_type") or "")
        severity = self._coerce_str(record.get("severity") or record.get("status") or record.get("level") or "info")
        timestamp = self._coerce_str(record.get("ts") or record.get("timestamp") or "")
        summary = self._summary(record)
        return ToastEvent(
            source=source,
            offset=offset,
            event_type=event_type or "event",
            severity=severity or "info",
            summary=summary,
            timestamp=timestamp,
        )

    @staticmethod
    def _coerce_str(value: Any) -> str:
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, (int, float, bool)):
            return str(value)
        return ""

    @staticmethod
    def _summary(record: Mapping[str, Any]) -> str:
        payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
        sources: list[Mapping[str, Any]] = [record, payload]
        for source in list(sources):
            if isinstance(source, Mapping):
                nested = source.get("metadata")
                if isinstance(nested, Mapping):
                    sources.append(nested)
        first_values: dict[str, str] = {}
        for source in sources:
            for key in ("message", "summary", "detail", "text", "goal"):
                value = source.get(key) if isinstance(source, Mapping) else None
                if isinstance(value, str) and value.strip():
                    return value.strip()
                if isinstance(value, (int, float, bool)):
                    return str(value)
            for key in ("title", "description"):
                if key not in first_values:
                    value = source.get(key) if isinstance(source, Mapping) else None
                    if isinstance(value, str) and value.strip():
                        first_values[key] = value.strip()
        if "description" in first_values:
            return (
                f"{first_values['title']} — {first_values['description']}"
                if "title" in first_values
                else first_values["description"]
            )
        if "title" in first_values:
            return first_values["title"]
        title = ""
        for source in sources:
            if not isinstance(source, Mapping):
                continue
            slug = str(source.get("vuln_id") or "").strip()
            cve = str(source.get("cve") or "").strip()
            raw_artifact = source.get("artifacts")
            if isinstance(raw_artifact, (list, tuple)) and raw_artifact:
                artifact = str(raw_artifact[0]).rsplit("/", 1)[-1]
            else:
                artifact = str(raw_artifact or "").strip()
            if slug or cve:
                title = " · ".join(
                    part
                    for part in (f"capture {slug}" if slug else "", cve, f"artifact {artifact}" if artifact else "")
                    if part
                )
                break
        if title:
            return title
        command = ""
        args = ""
        for source in sources:
            if isinstance(source, Mapping):
                command = command or str(source.get("command") or "").strip()
                args = args or str(source.get("args") or "").strip()
        if args and command and (args == command or command.endswith(f" {args}")):
            args = ""
        if command:
            return f"{command} {args}".strip()
        for source in sources:
            value = source.get("target") if isinstance(source, Mapping) else None
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""


_BORDER_BY_ROLE: dict[str, str] = {
    "danger": "red",
    "warning": "yellow",
    "success": "green",
    "accent": "blue",
}

TOASTR_SEVERITY_STYLES: Mapping[str, Mapping[str, str]] = {
    "success": {"border_style": "green", "text_style": "bold green"},
    "error": {"border_style": "red", "text_style": "bold red"},
    "warning": {"border_style": "yellow", "text_style": "bold yellow"},
    "info": {"border_style": "blue", "text_style": "bold blue"},
    "low": {"border_style": "cyan", "text_style": "bold cyan"},
    "medium": {"border_style": "yellow", "text_style": "bold yellow"},
    "high": {"border_style": "red", "text_style": "bold red"},
    "critical": {"border_style": "magenta", "text_style": "bold magenta"},
}

TOASTR_DEFAULT_SEVERITY = "info"

TOASTR_EMPTY_MESSAGE = "Empty message"

TOASTR_WIDTH_FRACTION = 0.9

TOASTR_MIN_WIDTH = 20

TOASTR_MAX_WIDTH = 100

TOASTR_WIDTH_MARGIN = 8

TOASTR_SENTINEL_WIDTH = 60


@dataclass(frozen=True)
class ToastrConfig:
    """Display knobs for the inline toastr boxes every surface shares."""

    severity_styles: Mapping[str, Mapping[str, str]] = field(default_factory=lambda: TOASTR_SEVERITY_STYLES)
    default_severity: str = TOASTR_DEFAULT_SEVERITY
    empty_message: str = TOASTR_EMPTY_MESSAGE
    width_fraction: float = TOASTR_WIDTH_FRACTION
    min_width: int = TOASTR_MIN_WIDTH
    max_width: int = TOASTR_MAX_WIDTH
    width_margin: int = TOASTR_WIDTH_MARGIN
    sentinel_width: int = TOASTR_SENTINEL_WIDTH


TOASTR = ToastrConfig()


def toastr_severity_style(severity: str) -> dict[str, str]:
    """Resolve one severity into the shared border/text style pair."""
    key = str(severity or "").lower()
    table = TOASTR_SEVERITY_STYLES
    return dict(table.get(key) or table[TOASTR_DEFAULT_SEVERITY])


def rich_toastr_panel(
    message: str,
    severity: str = TOASTR_DEFAULT_SEVERITY,
    terminal_width: int = 0,
    config: ToastrConfig | None = None,
) -> Panel:
    """Build the adaptive toastr panel used by the cmd2 shell.

    Args:
        message: Plain single- or multi-line notification text.
        severity: Key of the shared style table.
        terminal_width: Console width; ``0`` reuses the legacy clamp.
        config: Optional display configuration override.

    Returns:
        A Rich Panel with adaptive width, wrapped plain text and the
        unified severity styling.
    """
    cfg = config or TOASTR
    style = dict(cfg.severity_styles.get(str(severity or "").lower(), {}) or {})
    clean_input = str(message or "").strip() or cfg.empty_message
    lines = clean_input.split("\n")
    max_line_length = max(len(line) for line in lines)
    min_width = max(cfg.min_width, len(str(severity or cfg.default_severity).upper()) + cfg.width_margin)
    max_width = min(cfg.max_width, int(max(terminal_width, cfg.min_width) * cfg.width_fraction))
    content_width = max_line_length + cfg.width_margin
    optimal_width = max(min_width, min(content_width, max_width))
    if max_line_length > optimal_width - cfg.width_margin:
        wrapped: list[str] = []
        for line in lines:
            if len(line) <= optimal_width - cfg.width_margin:
                wrapped.append(line)
            else:
                filler = textwrap.fill(
                    line,
                    width=optimal_width - cfg.width_margin,
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                wrapped.extend(filler.split("\n"))
        final_message = "\n".join(wrapped)
    else:
        final_message = clean_input
    return Panel(
        Text(final_message, style=style.get("text_style", ""), justify="left"),
        border_style=style.get("border_style", "dim"),
        width=optimal_width,
        padding=(0, 2),
        title=f"[bold]{str(severity or cfg.default_severity).upper()}[/bold]",
        title_align="center",
    )


def shell_hint_bypass(console: Any, message: str, severity: str = TOASTR_DEFAULT_SEVERITY) -> bool:
    """Print the flat bypass line used when UI hints are off.

    Args:
        console: Any console-like object exposing ``print``.
        message: Notification text.
        severity: Key of the shared style table.

    Returns:
        Always ``True`` so callers can branch on success.
    """
    cfg = TOASTR
    style = dict(cfg.severity_styles.get(str(severity or "").lower(), {}) or {})
    level = str(severity or cfg.default_severity).upper()
    clean = str(message or "").strip() or cfg.empty_message
    console.print(f"[{level}] {clean}", style=style.get("text_style", ""))
    return True


def sentinel_toast_panel(
    file_name: str,
    relevant_info: str,
    commands: str,
    details: str,
    severity: str = TOASTR_DEFAULT_SEVERITY,
) -> Panel:
    """Build the yara sentinel popup with the shared styling.

    Args:
        file_name: Processed file path.
        relevant_info: Sentinel summary.
        commands: Suggested shell commands.
        details: Alert details block.
        severity: Sentinel alert level.

    Returns:
        A Rich Panel preserving the sentinel field layout.
    """
    style = toastr_severity_style(severity)
    content = (
        f"[bold]File:[/bold] {file_name}\n\n"
        f"[bold]Info:[/bold] {relevant_info}\n\n"
        f"[bold]Commands:[/bold] {commands}\n\n"
        f"[bold]Details:[/bold] {details}"
    )
    return Panel(
        Text.from_markup(content, justify="left"),
        border_style=style.get("border_style", "blue"),
        width=TOASTR.sentinel_width,
        padding=(1, 2),
        height=10,
    )


class ToastFormatter:
    """Render a :class:`ToastEvent` as a :class:`rich.text.Text` line."""

    def __init__(self, config: ToastConfig, theme: Theme) -> None:
        """Bind to config and the active theme."""
        self._config = config
        self._theme = theme

    def format(self, event: ToastEvent) -> Text:
        """Return a single themed line for ``event``."""
        role = self._role_for(event.severity)
        style = getattr(self._theme, role, getattr(self._theme, self._config.default_role))
        icon = self._config.ephemeral_icons.get(str(event.severity or "").lower(), "\u2139")
        text = Text()
        text.append(f"  {self._config.prefix_glyph} ", style=self._theme.hint)
        if event.event_type:
            text.append(f"{icon} {event.event_type} ", style=style)
        summary = self._truncate(event.summary or "(no detail)")
        text.append(summary, style=self._theme.muted)
        return text

    def is_prominent(self, event: ToastEvent) -> bool:
        """Return True when an event deserves a full toastr panel.

        High-severity events and completion summaries are never squeezed
        into a truncated line: they render with their complete text.
        """
        if event.event_type in self._config.prominent_kinds:
            return True
        return self._role_for(event.severity) in self._config.prominent_roles

    def format_prominent(self, event: ToastEvent) -> Panel:
        """Render an event as a toastr panel with the complete summary."""
        role = self._role_for(event.severity)
        border = _BORDER_BY_ROLE.get(role, "dim")
        icon = self._config.ephemeral_icons.get(str(event.severity or "").lower(), "\u2139")
        summary = (event.summary or "(no detail)").strip()
        limit = max(1, self._config.prominent_max_chars)
        if len(summary) > limit:
            summary = summary[:limit] + "\u2026 (truncated, see sessions log)"
        body = Text()
        body.append(f"{icon} ", style=border)
        body.append(summary, style="default")
        if event.timestamp:
            body.append(f"  ·  {event.timestamp}", style="dim")
        title = f"{event.severity.upper()} · {event.event_type}" if event.event_type else event.severity.upper()
        return Panel(
            body,
            title=f"[bold]{title}[/bold]",
            border_style=border,
            padding=(0, 2),
        )

    def format_ephemeral(self, event: ToastEvent) -> Text:
        """Return a single sonner-style line with severity icon for ``event``.

        Reuses the severity-to-role table and the active theme, so the
        ephemeral line never drifts from the persistent panel palette.
        LAZY renders ``toast.success / error / warning / info`` with one
        glyph each; this is the terminal equivalent without the ascii box.

        Args:
            event: Toast event to render.

        Returns:
            One themed Rich Text line.
        """
        role = self._role_for(event.severity)
        style = getattr(self._theme, role, getattr(self._theme, self._config.default_role))
        icon = self._config.ephemeral_icons.get(str(event.severity or "").lower(), "\u2139")
        summary = (event.summary or "(no detail)").strip()
        limit = max(1, self._config.ephemeral_max_chars)
        if len(summary) > limit:
            summary = summary[:limit] + "\u2026"
        text = Text()
        text.append(f" {icon} ", style=style)
        if event.event_type:
            text.append(f"{event.event_type} ", style=style)
        text.append(summary, style=self._theme.muted)
        return text

    def duration_for(self, event: ToastEvent) -> float:
        """Return the auto-dismiss delay in seconds for ``event``.

        Reuses the per-severity duration table from the config, mirroring
        the sonner ``duration`` option per toast level. ``0`` means sticky.

        Args:
            event: Toast event to time.

        Returns:
            Seconds before the line is erased, ``0`` for sticky.
        """
        try:
            return max(
                0.0,
                float(
                    self._config.ephemeral_durations.get(
                        str(event.severity or "").lower(), self._config.ephemeral_default_duration
                    )
                ),
            )
        except (TypeError, ValueError):
            return float(self._config.ephemeral_default_duration)

    @staticmethod
    def digest_line(dropped: list[ToastEvent]) -> str:
        """Summarise over-budget events so none vanish silently."""
        counts: dict[str, int] = {}
        for event in dropped:
            counts[event.event_type or "event"] = counts.get(event.event_type or "event", 0) + 1
        parts = [f"{kind}×{num}" if num > 1 else kind for kind, num in counts.items()]
        return f"… +{len(dropped)} more: {', '.join(parts)}"

    def format_many(self, events: list[ToastEvent], width: int = 0) -> Any:
        """Render several events as one Rich renderable.

        This is the shared presentation contract. The cmd2 shell prints the
        result through a Console; the Textual dashboard embeds the very same
        renderable in a widget. One formatter, two surfaces, no drift.

        Prominent events (high severity, completion summaries) render as
        individual toastr panels with full text. Remaining lines share the
        per-tick budget; over-budget ones collapse into a digest line so
        no unseen notification disappears silently.

        Args:
            events: Events to render, oldest first.
            width: Panel width. ``0`` means auto-clamp to the console width.

        Returns:
            A ``Panel``/``Group`` for several items, a single ``Text``
            line for one plain event, or ``None`` when empty.
        """
        if not events:
            return None
        budget = max(1, self._config.max_per_tick_default)
        filtered = [e for e in events if e.event_type not in self._config.skip_event_types]
        if not filtered:
            return None
        prominent = [e for e in filtered if self.is_prominent(e)]
        normal = [e for e in filtered if not self.is_prominent(e)]
        to_show = normal[-budget:]
        dropped = normal[:-budget]
        renderables: list[Any] = []
        if len(normal) == 1 and not prominent and not dropped:
            return self.format(to_show[0])
        if to_show or dropped:
            lines = [self.format(event) for event in to_show]
            if dropped:
                digest = Text(f"  {self.digest_line(dropped)}", style="dim italic")
                lines.append(digest)
            border_style = getattr(self._theme, "warning", "yellow")
            resolved = width or self._console_width()
            renderables.append(
                Panel(
                    Group(*lines),
                    title="[dim]notifications[/dim]",
                    border_style=border_style,
                    padding=(0, 1),
                    width=min(resolved, self._config.max_panel_width),
                )
            )
        renderables.extend(self.format_prominent(event) for event in prominent)
        if len(renderables) == 1:
            return renderables[0]
        return Group(*renderables)

    def _console_width(self) -> int:
        """Return a sane console width when the caller passes none."""
        try:
            return int(Console().width)
        except Exception:
            return self._config.fallback_width

    def _role_for(self, severity: str) -> str:
        lookup = self._config.severity_styles.get(severity.lower())
        if lookup:
            return lookup
        return self._config.default_role

    def _truncate(self, value: str) -> str:
        from core.text_utils import truncate_text

        return truncate_text(value, self._config.max_line_chars, marker=self._config.truncation_suffix)


class ToastBus:
    """Lifecycle façade: collect → format → print.

    The bus is the single class the cmd2 shell calls. Other code depends
    only on :meth:`render` and :meth:`mark_all_seen`.
    """

    def __init__(
        self,
        config: ToastConfig,
        state: ToastState,
        reader: ToastReader,
        formatter: ToastFormatter,
        console: Console | None = None,
    ) -> None:
        """Bind every collaborator."""
        self._config = config
        self._state = state
        self._reader = reader
        self._formatter = formatter
        self._console = console or Console(stderr=False, highlight=False, soft_wrap=True)

    def collect(self) -> list[ToastEvent]:
        """Return every unseen event across :attr:`ToastConfig.event_files`."""
        out: list[ToastEvent] = []
        resolved, _ = self._reader.resolve_sources(self._config.event_files)
        for name in resolved:
            start = self._state.get(name)
            events, end = self._reader.read_unseen(name, start)
            if events:
                out.extend(events)
            if end > start:
                self._state.set(name, end)
        return out

    def render(self, enabled: bool = True) -> int:
        """Collect, render and persist offsets in a single call.

        When multiple toasts arrive in one tick they are wrapped in a
        Rich Panel with the theme's ``warning`` border so the operator
        can visually separate them from command output. A single toast
        renders as a plain line to avoid unnecessary visual weight.

        Args:
            enabled: When ``False`` the call is a no-op and returns 0.

        Returns:
            The number of toast lines actually printed.
        """
        if not enabled:
            return 0
        events = self.collect()
        if not events:
            self._state.flush()
            return 0
        budget = max(1, self._config.max_per_tick_default)
        renderable = self._formatter.format_many(events, width=self._console.width)
        shown = 0
        if renderable is not None:
            self._console.print(renderable)
            shown = min(len(events), budget)
        self._state.flush()
        return shown

    def mark_all_seen(self) -> None:
        """Advance the offset for every configured file to its current size."""
        resolved, _ = self._reader.resolve_sources(self._config.event_files)
        for name in resolved:
            _, end = self._reader.read_unseen(name, 0)
            self._state.set(name, end)
        self._state.flush()

    def render_ephemeral(self, enabled: bool = True, duration: float | None = None) -> int:
        """Collect unseen events and print each as an auto-expiring line.

        This is the sonner port: one themed icon line per event that is
        erased after its per-severity delay when the output is an
        interactive TTY. On pipes or dumb terminals the lines stay printed
        so logs never lose the event. Offsets persist exactly like
        :meth:`render`, so both paths share the same read cursor.

        Args:
            enabled: When ``False`` the call is a no-op and returns 0.
            duration: Forced seconds per toast, or None for per-level
                defaults from the config. ``0`` means sticky.

        Returns:
            The number of toasts raised.
        """
        if not enabled:
            return 0
        events = self.collect()
        if not events:
            self._state.flush()
            return 0
        budget = max(1, self._config.max_per_tick_default)
        shown = 0
        for event in events[-budget:]:
            delay = max(0.0, float(duration)) if duration is not None else self._formatter.duration_for(event)
            self._console.print(self._formatter.format_ephemeral(event), soft_wrap=True)
            shown += 1
            self._schedule_erase(delay)
        self._state.flush()
        return shown

    def _schedule_erase(self, delay: float) -> None:
        """Erase the last printed line after ``delay`` on interactive TTYs.

        Args:
            delay: Seconds before erasing. ``0`` or less means sticky.
        """
        if delay <= 0:
            return
        stream = getattr(self._console, "file", None)
        if _is_dumb_stream(stream):
            return
        timer = threading.Timer(delay, self._erase_lines, args=(stream, 1))
        timer.daemon = True
        timer.start()

    @staticmethod
    def _erase_lines(stream: Any, rows: int) -> None:
        """Move the cursor up and clear ``rows`` lines.

        Args:
            stream: Output stream behind the console.
            rows: Terminal rows to erase.
        """
        try:
            for _ in range(max(1, rows)):
                stream.write("\x1b[1A\x1b[2K")
            stream.flush()
        except Exception:
            pass


def _is_truthy(value: Any, config: ToastConfig, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in config.truthy_strings:
            return True
        if lowered in config.falsy_strings:
            return False
    return default


def _is_dumb_stream(stream: Any) -> bool:
    """Return True when ANSI erase sequences must not be emitted.

    Args:
        stream: Output stream behind the console.

    Returns:
        True for pipes, dumb terminals, or ``NO_COLOR``.
    """
    if os.environ.get("NO_COLOR"):
        return True
    if os.environ.get("TERM") == "dumb":
        return True
    isatty = getattr(stream, "isatty", None)
    try:
        return not bool(isatty() if callable(isatty) else False)
    except Exception:
        return True


def toasts_enabled(payload: Mapping[str, Any] | None, config: ToastConfig | None = None) -> bool:
    """Return ``True`` when toast rendering is permitted."""
    cfg = config or ToastConfig()
    if payload is None:
        return cfg.enabled_default
    return _is_truthy(payload.get(cfg.enabled_key), cfg, cfg.enabled_default)


def _budget(payload: Mapping[str, Any] | None, config: ToastConfig) -> int:
    if payload is None:
        return config.max_per_tick_default
    raw = payload.get(config.max_per_tick_key)
    if isinstance(raw, bool):
        return config.max_per_tick_default
    if isinstance(raw, (int, float)):
        candidate = int(raw)
    elif isinstance(raw, str) and raw.strip().isdigit():
        candidate = int(raw.strip())
    else:
        return config.max_per_tick_default
    return max(1, min(candidate, 50))


def build_default_bus(
    payload: Mapping[str, Any] | None,
    sessions_dir: str | None = None,
    console: Console | None = None,
) -> ToastBus:
    """Wire the canonical bus used by the shell postcmd hook.

    Args:
        payload: Loaded ``payload.json``.
        sessions_dir: Optional override for the sessions root.
        console: Optional Rich console (tests inject a captured one).

    Returns:
        A ready-to-use :class:`ToastBus` instance.
    """
    config = ToastConfig()
    if sessions_dir is not None and sessions_dir.strip():
        config = replace(config, sessions_dir=sessions_dir.strip(), max_per_tick_default=_budget(payload, config))
    else:
        budget = _budget(payload, config)
        if budget != config.max_per_tick_default:
            config = replace(config, max_per_tick_default=budget)
    theme = theme_from_payload(payload)
    state = ToastState(config)
    reader = ToastReader(config)
    formatter = ToastFormatter(config, theme)
    return ToastBus(config, state, reader, formatter, console=console)


def render_toasts(
    payload: Mapping[str, Any] | None,
    sessions_dir: str | None = None,
    console: Console | None = None,
    bus_factory: Callable[[], ToastBus] | None = None,
) -> int:
    """One-shot helper used by the cmd2 postcmd hook.

    Args:
        payload: Loaded ``payload.json``.
        sessions_dir: Optional override for the sessions root.
        console: Optional pre-built Rich console.
        bus_factory: Optional factory returning a pre-built
            :class:`ToastBus` (used by tests).

    Returns:
        Number of toast lines printed; ``0`` when disabled or quiet.
    """
    if not toasts_enabled(payload):
        return 0
    bus = bus_factory() if bus_factory is not None else build_default_bus(payload, sessions_dir, console)
    return bus.render(enabled=True)


def ephemeral_enabled(payload: Mapping[str, Any] | None, config: ToastConfig | None = None) -> bool:
    """Return True when toasts must auto-dismiss like sonner.

    Args:
        payload: Loaded ``payload.json``.
        config: Optional active configuration.

    Returns:
        Value of the ``toast_ephemeral`` payload flag.
    """
    cfg = config or ToastConfig()
    if payload is None:
        return cfg.ephemeral_default
    return _is_truthy(payload.get(cfg.ephemeral_key), cfg, cfg.ephemeral_default)


def render_ephemeral_toasts(
    payload: Mapping[str, Any] | None,
    sessions_dir: str | None = None,
    console: Console | None = None,
    duration: float | None = None,
    bus_factory: Callable[[], ToastBus] | None = None,
) -> int:
    """Collect unseen events and print each as an auto-expiring line.

    Same read cursor and theme as :func:`render_toasts`; only the
    presentation differs: one sonner-style icon line per event instead of
    the persistent ascii panel.

    Args:
        payload: Loaded ``payload.json``.
        sessions_dir: Optional override for the sessions root.
        console: Optional pre-built Rich console.
        duration: Forced seconds per toast, or None for per-level defaults.
        bus_factory: Optional factory returning a pre-built
            :class:`ToastBus` (used by tests).

    Returns:
        Number of toasts raised; ``0`` when disabled or quiet.
    """
    if not toasts_enabled(payload):
        return 0
    bus = bus_factory() if bus_factory is not None else build_default_bus(payload, sessions_dir, console)
    return bus.render_ephemeral(enabled=True, duration=duration)


def emit_toast(
    message: str,
    severity: str = "info",
    event_type: str = "note",
    sessions_dir: str | None = None,
    config: ToastConfig | None = None,
) -> bool:
    """Append one toast event so the existing render hook displays it.

    The emitter lives beside the reader on purpose: the JSONL schema is
    owned by this module, so writing an event anywhere else would let the
    two sides drift. The cmd2 postcmd hook picks the line up on the next
    command, or immediately via :func:`render_toasts`.

    Args:
        message: Human-readable one-liner.
        severity: One of the keys in ``ToastConfig.severity_styles``.
        event_type: Short label rendered before the message.
        sessions_dir: Override for the sessions root.
        config: Optional active configuration.

    Returns:
        True when the event was appended, False on any write failure.
    """
    cfg = config or ToastConfig()
    root = Path(sessions_dir) if sessions_dir else Path(cfg.sessions_dir)
    text = str(message or "").strip()
    if not text:
        return False
    record = {
        "type": str(event_type or "note"),
        "severity": str(severity or "info").lower(),
        "ts": time.strftime("%H:%M:%S"),
        "message": text,
    }
    target = root / cfg.event_files[0]
    try:
        root.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return True
    except OSError:
        return False


def read_recent_toasts(
    sessions_dir: str | None = None,
    limit: int = 5,
    config: ToastConfig | None = None,
) -> list[ToastEvent]:
    """Return the most recent toast events without touching read offsets.

    The dashboard is a read-only mirror. If it consumed events through
    :meth:`ToastBus.collect` it would advance the shared
    ``sessions/.toast_state.json`` cursor and the cmd2 shell would never
    show those events. Tailing the file keeps both surfaces independent.

    Args:
        sessions_dir: Override for the sessions root.
        limit: Maximum number of events returned, newest last.
        config: Optional active configuration.

    Returns:
        Up to ``limit`` events, oldest first. Empty when the file is
        missing or unreadable.
    """
    cfg = config or ToastConfig()
    root = Path(sessions_dir) if sessions_dir else Path(cfg.sessions_dir)
    reader = ToastReader(cfg, root=root)
    out: list[ToastEvent] = []
    for name in cfg.event_files:
        path = root / name
        if not path.is_file():
            continue
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as handle:
                tail = handle.readlines()[-max(1, limit) :]
        except OSError:
            continue
        for line in tail:
            stripped = line.strip()
            if not stripped:
                continue
            event = reader._build_event(stripped, name, 0)
            if event is not None:
                out.append(event)
    return out[-max(1, limit) :]


def build_toast_renderable(
    events: list[ToastEvent],
    payload: Mapping[str, Any] | None = None,
    width: int = 0,
    config: ToastConfig | None = None,
) -> Any:
    """Render events with the active theme for any surface.

    Args:
        events: Events to render.
        payload: Loaded payload used to resolve the theme.
        width: Panel width. ``0`` means auto.
        config: Optional active configuration.

    Returns:
        A Rich renderable, or ``None`` when there is nothing to show.
    """
    cfg = config or ToastConfig()
    formatter = ToastFormatter(cfg, theme_from_payload(payload))
    return formatter.format_many(events, width=width)


__all__ = [
    "TOASTR_DEFAULT_SEVERITY",
    "TOASTR_SEVERITY_STYLES",
    "ToastBus",
    "ToastConfig",
    "ToastEvent",
    "ToastFormatter",
    "ToastReader",
    "ToastState",
    "ToastrConfig",
    "build_default_bus",
    "build_toast_renderable",
    "emit_toast",
    "ephemeral_enabled",
    "read_recent_toasts",
    "render_ephemeral_toasts",
    "render_toasts",
    "rich_toastr_panel",
    "sentinel_toast_panel",
    "shell_hint_bypass",
    "toasts_enabled",
    "toastr_severity_style",
]
