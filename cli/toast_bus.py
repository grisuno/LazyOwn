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
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from rich.console import Console
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
    )
    enabled_default: bool = True
    max_per_tick_default: int = 5
    max_line_chars: int = 96
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
    prefix_glyph: str = ">>"
    file_offset_separator: str = "::"
    skip_event_types: tuple[str, ...] = ()


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
            name: Filename relative to the sessions root.
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
        event_type = self._coerce_str(
            record.get("type") or record.get("kind") or record.get("event") or ""
        )
        severity = self._coerce_str(
            record.get("severity") or record.get("status") or record.get("level") or "info"
        )
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
        for source in (record, payload):
            for key in ("message", "summary", "detail", "goal", "command", "target"):
                value = source.get(key) if isinstance(source, Mapping) else None
                if isinstance(value, str) and value.strip():
                    return value.strip()
                if isinstance(value, (int, float, bool)):
                    return str(value)
        return ""


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
        text = Text()
        text.append(f"  {self._config.prefix_glyph} ", style=self._theme.hint)
        if event.event_type:
            text.append(f"{event.event_type} ", style=style)
        summary = self._truncate(event.summary or "(no detail)")
        text.append(summary, style=self._theme.muted)
        return text

    def _role_for(self, severity: str) -> str:
        lookup = self._config.severity_styles.get(severity.lower())
        if lookup:
            return lookup
        return self._config.default_role

    def _truncate(self, value: str) -> str:
        limit = self._config.max_line_chars
        if len(value) <= limit:
            return value
        keep = max(1, limit - len(self._config.truncation_suffix))
        return value[:keep] + self._config.truncation_suffix


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
        for name in self._config.event_files:
            start = self._state.get(name)
            events, end = self._reader.read_unseen(name, start)
            if events:
                out.extend(events)
            if end > start:
                self._state.set(name, end)
        return out

    def render(self, enabled: bool = True) -> int:
        """Collect, render and persist offsets in a single call.

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
        filtered = [event for event in events if event.event_type not in self._config.skip_event_types]
        to_show = filtered[-budget:]
        for event in to_show:
            self._console.print(self._formatter.format(event))
        self._state.flush()
        return len(to_show)

    def mark_all_seen(self) -> None:
        """Advance the offset for every configured file to its current size."""
        for name in self._config.event_files:
            _, end = self._reader.read_unseen(name, 0)
            self._state.set(name, end)
        self._state.flush()


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
        config = ToastConfig(
            enabled_key=config.enabled_key,
            max_per_tick_key=config.max_per_tick_key,
            sessions_dir=sessions_dir.strip(),
            state_filename=config.state_filename,
            event_files=config.event_files,
            enabled_default=config.enabled_default,
            max_per_tick_default=_budget(payload, config),
            max_line_chars=config.max_line_chars,
            max_offset_value=config.max_offset_value,
            truthy_strings=config.truthy_strings,
            falsy_strings=config.falsy_strings,
            severity_styles=config.severity_styles,
            default_role=config.default_role,
            truncation_suffix=config.truncation_suffix,
            prefix_glyph=config.prefix_glyph,
            file_offset_separator=config.file_offset_separator,
            skip_event_types=config.skip_event_types,
        )
    else:
        budget = _budget(payload, config)
        if budget != config.max_per_tick_default:
            config = ToastConfig(
                enabled_key=config.enabled_key,
                max_per_tick_key=config.max_per_tick_key,
                sessions_dir=config.sessions_dir,
                state_filename=config.state_filename,
                event_files=config.event_files,
                enabled_default=config.enabled_default,
                max_per_tick_default=budget,
                max_line_chars=config.max_line_chars,
                max_offset_value=config.max_offset_value,
                truthy_strings=config.truthy_strings,
                falsy_strings=config.falsy_strings,
                severity_styles=config.severity_styles,
                default_role=config.default_role,
                truncation_suffix=config.truncation_suffix,
                prefix_glyph=config.prefix_glyph,
                file_offset_separator=config.file_offset_separator,
                skip_event_types=config.skip_event_types,
            )
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


__all__ = [
    "ToastBus",
    "ToastConfig",
    "ToastEvent",
    "ToastFormatter",
    "ToastReader",
    "ToastState",
    "build_default_bus",
    "render_toasts",
    "toasts_enabled",
]
