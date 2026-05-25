"""Persistent operator status bar for the LazyOwn cmd2 shell.

The status bar collapses the four pieces of context an operator constantly
reaches for into a single line embedded in the shell prompt:

    [ target | phase | found: <last_finding> | next: <suggestion> ]

It replaces the round-trip of opening ``sessions/`` artefacts after every
command. The renderer is wired into ``cmd2`` through a precommand hook so
the bar is recomputed *before* each prompt is drawn, never blocking input.

Design constraints honoured here:

* Single Responsibility: every source class produces exactly one field.
* Open / Closed: new fields are added by registering another
  :class:`IStatusSource`, never by editing the renderer.
* Liskov: every source returns a ``str`` of bounded width.
* Interface Segregation: the source protocol exposes only ``collect``.
* Dependency Inversion: :class:`StatusBarManager` depends on the
  abstractions, never on ``LazyOwnShell`` or ``cmd2`` directly.
* No magic numbers / hardcoded paths: every default lives in
  :class:`StatusBarConfig`; runtime overrides come from ``payload.json``.
* Readline-safe ANSI: colour escapes are wrapped with the GNU readline
  ``\\001 ... \\002`` markers so column accounting stays correct when the
  bar is concatenated into ``self.prompt``.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol, Sequence


@dataclass(frozen=True)
class StatusBarConfig:
    """Immutable configuration container for the status bar subsystem.

    Every tunable lives here. Operator overrides flow in through
    :meth:`from_payload` which reads ``payload.json``; downstream code only
    ever sees an instance of this class.
    """

    enabled_key: str = "enable_status_bar"
    format_key: str = "status_bar_format"
    operators_enabled_key: str = "enable_operator_presence"
    operators_format_key: str = "status_bar_format_with_operators"
    sessions_dir: str = "sessions"
    world_model_filename: str = "world_model.json"
    os_filename: str = "os.json"
    session_report_filename: str = "LazyOwn_session_report.csv"
    operators_filename: str = "operators.json"
    credentials_glob: str = "credentials*.txt"
    hashes_glob: str = "hash*.txt"
    vulns_glob: str = "vulns_*.json"
    notes_filename: str = "notes.jsonl"
    target_payload_keys: tuple[str, ...] = ("active_target", "rhost", "domain")
    phase_payload_key: str = "current_phase"
    phase_world_model_key: str = "phase"
    enabled_default: bool = True
    operators_enabled_default: bool = False
    default_format: str = "[ {target} | {phase} | found: {finding} | next: {suggestion} ]"
    default_format_with_operators: str = (
        "[ {target} | {phase} | found: {finding} | ops: {operators} | next: {suggestion} ]"
    )
    fallback_target: str = "no-target"
    fallback_phase: str = "recon"
    fallback_finding: str = "-"
    fallback_suggestion: str = "ping"
    fallback_operators: str = "0"
    max_target_chars: int = 32
    max_phase_chars: int = 12
    max_finding_chars: int = 36
    max_suggestion_chars: int = 24
    max_operators_chars: int = 24
    max_field_chars: int = 64
    max_file_bytes: int = 524288
    csv_max_rows: int = 2000
    suggestion_limit: int = 1
    operator_stale_seconds: float = 90.0
    color_enabled: bool = True
    color_open: str = "\033[2;36m"
    color_close: str = "\033[0m"
    readline_open_marker: str = "\001"
    readline_close_marker: str = "\002"
    prompt_join: str = "\n"
    truncation_suffix: str = "..."
    allowed_field_pattern: str = r"^[\w./:@\-\[\]+ ]{1,128}$"
    forbidden_substrings: tuple[str, ...] = ("\033", "\r", "\n", "\x07", "\x00")
    truthy_strings: tuple[str, ...] = ("1", "true", "yes", "on")
    falsy_strings: tuple[str, ...] = ("0", "false", "no", "off")

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any] | None) -> StatusBarConfig:
        """Return a config with overrides applied from a ``payload.json`` mapping.

        Args:
            payload: The loaded ``payload.json`` dictionary, or ``None`` to
                accept the defaults verbatim.

        Returns:
            A new :class:`StatusBarConfig` instance. Unknown keys are
            ignored so the framework never crashes on a malformed payload.
        """
        if not payload:
            return cls()
        base = cls()
        fmt_value = payload.get(base.format_key)
        ops_fmt_value = payload.get(base.operators_format_key)
        sessions_value = payload.get("sessions_dir")
        updates: dict[str, Any] = {}
        if isinstance(fmt_value, str) and fmt_value.strip():
            updates["default_format"] = fmt_value
        if isinstance(ops_fmt_value, str) and ops_fmt_value.strip():
            updates["default_format_with_operators"] = ops_fmt_value
        if isinstance(sessions_value, str) and sessions_value.strip():
            updates["sessions_dir"] = sessions_value
        return replace(base, **updates) if updates else base


@dataclass(frozen=True)
class StatusContext:
    """Immutable snapshot of the pieces the bar renders.

    ``operators`` is an opt-in fifth segment populated by
    :class:`CollabPresenceSource`. Empty strings are treated as "field
    disabled" by the renderer so the historical four-segment format remains
    the default.
    """

    target: str
    phase: str
    last_finding: str
    next_suggestion: str
    operators: str = ""


class IStatusSource(Protocol):
    """One-method protocol that every status source must satisfy."""

    def collect(self) -> str:
        """Return the field value for this source as a plain string."""
        ...


class FileSystemReader:
    """Path-validated, size-bounded reader for ``sessions/`` artefacts.

    The reader is the only filesystem entry point in this module. It
    refuses anything that escapes the configured ``sessions_dir`` and
    truncates reads to ``max_file_bytes`` so a runaway log never blows up
    the prompt.
    """

    def __init__(self, config: StatusBarConfig, root: Path | None = None) -> None:
        """Initialise with the active config and optional explicit root.

        Args:
            config: The active :class:`StatusBarConfig`.
            root: Override for the resolved sessions directory. Defaults
                to ``config.sessions_dir`` relative to the current working
                directory.

        Raises:
            ValueError: When ``config.max_file_bytes`` is non-positive.
        """
        if config.max_file_bytes <= 0:
            raise ValueError("max_file_bytes must be positive")
        self._config = config
        base = Path(root) if root is not None else Path(config.sessions_dir)
        self._root = base.resolve()

    @property
    def root(self) -> Path:
        """Return the resolved root directory backing this reader."""
        return self._root

    def read_text(self, relative: str) -> str:
        """Return the contents of ``relative`` truncated to ``max_file_bytes``.

        Args:
            relative: Path fragment under the sessions root. A leading
                separator is rejected; ``..`` escape attempts are rejected.

        Returns:
            The file contents as text, or an empty string when the file
            is missing or unreadable.
        """
        target = self._safe_path(relative)
        if target is None or not target.is_file():
            return ""
        try:
            with target.open("rb") as handle:
                raw = handle.read(self._config.max_file_bytes)
        except OSError:
            return ""
        return raw.decode("utf-8", errors="ignore")

    def read_json(self, relative: str) -> Any:
        """Return parsed JSON from ``relative`` or ``None`` on failure.

        Args:
            relative: Path fragment under the sessions root.

        Returns:
            The decoded JSON object, or ``None`` when the file does not
            exist or contains invalid JSON.
        """
        text = self.read_text(relative)
        if not text:
            return None
        try:
            return json.loads(text)
        except (ValueError, json.JSONDecodeError):
            return None

    def glob_latest(self, pattern: str) -> Path | None:
        """Return the most recently modified path matching ``pattern``.

        Args:
            pattern: Glob expression evaluated relative to the sessions
                root. Patterns are constrained to the root via
                :meth:`_safe_path` once a match is selected.

        Returns:
            The newest matching path, or ``None`` if no match exists.
        """
        if not pattern or self._has_traversal(pattern):
            return None
        try:
            candidates = [p for p in self._root.glob(pattern) if p.is_file()]
        except OSError:
            return None
        if not candidates:
            return None
        candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        chosen = candidates[0]
        if not self._is_within_root(chosen):
            return None
        return chosen

    def _safe_path(self, relative: str) -> Path | None:
        if not relative or self._has_traversal(relative):
            return None
        candidate = (self._root / relative).resolve()
        return candidate if self._is_within_root(candidate) else None

    def _is_within_root(self, candidate: Path) -> bool:
        try:
            candidate.relative_to(self._root)
        except ValueError:
            return False
        return True

    @staticmethod
    def _has_traversal(value: str) -> bool:
        normalised = value.replace("\\", "/")
        if normalised.startswith("/"):
            return True
        return ".." in normalised.split("/")


class PayloadTargetSource:
    """Status source: active target identifier."""

    def __init__(self, config: StatusBarConfig, payload: Mapping[str, Any] | None) -> None:
        """Bind to the live config and a payload mapping.

        Args:
            config: Active configuration.
            payload: ``payload.json`` mapping. ``None`` is treated as an
                empty payload — the source then falls back to
                ``config.fallback_target``.
        """
        self._config = config
        self._payload = payload or {}

    def collect(self) -> str:
        """Return the first non-empty target key from ``payload.json``."""
        for key in self._config.target_payload_keys:
            value = self._payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return self._config.fallback_target


class WorldModelPhaseSource:
    """Status source: current kill-chain phase."""

    def __init__(
        self,
        config: StatusBarConfig,
        reader: FileSystemReader,
        payload: Mapping[str, Any] | None,
    ) -> None:
        """Bind to config, sessions reader and payload mapping."""
        self._config = config
        self._reader = reader
        self._payload = payload or {}

    def collect(self) -> str:
        """Return the active phase from ``world_model.json`` then payload then default."""
        wm = self._reader.read_json(self._config.world_model_filename)
        if isinstance(wm, dict):
            phase = wm.get(self._config.phase_world_model_key)
            if isinstance(phase, str) and phase.strip():
                return phase.strip()
        payload_phase = self._payload.get(self._config.phase_payload_key)
        if isinstance(payload_phase, str) and payload_phase.strip():
            return payload_phase.strip()
        return self._config.fallback_phase


class SessionFindingSource:
    """Status source: most recent meaningful finding."""

    def __init__(self, config: StatusBarConfig, reader: FileSystemReader) -> None:
        """Bind to config and sessions reader."""
        self._config = config
        self._reader = reader

    def collect(self) -> str:
        """Return a short description of the freshest credential / vuln / note."""
        for resolver in (self._latest_credential, self._latest_vuln, self._latest_note):
            value = resolver()
            if value:
                return value
        return self._config.fallback_finding

    def _latest_credential(self) -> str:
        for pattern in (self._config.credentials_glob, self._config.hashes_glob):
            candidate = self._reader.glob_latest(pattern)
            if candidate is None:
                continue
            line = self._last_line(candidate)
            if line:
                return self._summarise_credential(candidate.name, line)
        return ""

    def _latest_vuln(self) -> str:
        candidate = self._reader.glob_latest(self._config.vulns_glob)
        if candidate is None:
            return ""
        try:
            payload = json.loads(candidate.read_bytes()[: self._config.max_file_bytes].decode("utf-8", errors="ignore"))
        except (OSError, ValueError, json.JSONDecodeError):
            return ""
        items = self._extract_vuln_items(payload)
        if not items:
            return ""
        return f"vuln:{items[0]}"

    def _latest_note(self) -> str:
        text = self._reader.read_text(self._config.notes_filename)
        if not text:
            return ""
        for raw_line in reversed(text.splitlines()):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except (ValueError, json.JSONDecodeError):
                return stripped
            if isinstance(record, dict):
                note = record.get("note") or record.get("text") or record.get("message")
                if isinstance(note, str) and note.strip():
                    return f"note:{note.strip()}"
        return ""

    def _last_line(self, path: Path) -> str:
        try:
            with path.open("rb") as handle:
                raw = handle.read(self._config.max_file_bytes)
        except OSError:
            return ""
        text = raw.decode("utf-8", errors="ignore")
        for line in reversed(text.splitlines()):
            stripped = line.strip()
            if stripped:
                return stripped
        return ""

    def _summarise_credential(self, filename: str, line: str) -> str:
        kind = "cred" if "credentials" in filename else "hash"
        user_match = re.match(r"([^:\s]{1,32})", line)
        if user_match:
            return f"{kind}:{user_match.group(1)}"
        return kind

    def _extract_vuln_items(self, payload: Any) -> list[str]:
        if isinstance(payload, dict):
            iterable: Sequence[Any] = payload.get("cves") or payload.get("items") or []
        elif isinstance(payload, list):
            iterable = payload
        else:
            iterable = []
        out: list[str] = []
        for item in iterable:
            if isinstance(item, str) and item.strip():
                out.append(item.strip())
            elif isinstance(item, dict):
                ident = item.get("id") or item.get("cve") or item.get("name")
                if isinstance(ident, str) and ident.strip():
                    out.append(ident.strip())
            if out:
                break
        return out


class CommandHintSuggestionSource:
    """Status source: next command verb derived from kill-chain + phase priority.

    Wraps :func:`cli.reactive_hints.command_hints` so the bar always
    suggests an actionable CLI verb (``lazynmap``, ``gobuster``, ...)
    instead of a graph-node label like a class name. The graph advisor
    remains available as a secondary source for callers that need
    arbitrary node lookups.
    """

    def __init__(
        self,
        config: StatusBarConfig,
        reader: FileSystemReader,
        phase_provider: Callable[[], str],
        hint_provider: Callable[[str, str, str, int], list[str]] | None = None,
    ) -> None:
        """Bind to config, reader and the current-phase callable.

        Args:
            config: Active configuration.
            reader: Sessions filesystem reader (used to discover the
                most recent command verb).
            phase_provider: Zero-arg callable returning the active
                phase identifier. Decoupled so the suggestion source
                does not duplicate the phase-detection logic.
            hint_provider: Optional override for the hint engine. When
                omitted the default :func:`cli.reactive_hints.command_hints`
                is resolved lazily so the import order stays clean.
        """
        self._config = config
        self._reader = reader
        self._phase_provider = phase_provider
        self._hint_provider = hint_provider

    def collect(self) -> str:
        """Return the top kill-chain suggestion or the configured fallback."""
        provider = self._hint_provider or self._default_provider()
        if provider is None:
            return self._config.fallback_suggestion
        last_command = self._latest_command()
        phase = ""
        try:
            phase = self._phase_provider() or ""
        except Exception:
            phase = ""
        try:
            suggestions = provider(
                last_command,
                phase,
                str(self._reader.root),
                self._config.suggestion_limit,
            )
        except Exception:
            return self._config.fallback_suggestion
        for verb in suggestions or []:
            if isinstance(verb, str) and verb.strip():
                return verb.strip()
        return self._config.fallback_suggestion

    def _latest_command(self) -> str:
        text = self._reader.read_text(self._config.session_report_filename)
        if not text:
            return ""
        try:
            reader = csv.DictReader(text.splitlines())
            rows = []
            for index, row in enumerate(reader):
                if index >= self._config.csv_max_rows:
                    break
                rows.append(row)
        except csv.Error:
            return ""
        for row in reversed(rows):
            for column in ("tool", "command", "name"):
                raw = (row.get(column) or "").strip()
                if not raw:
                    continue
                first = raw.split()[0]
                if first:
                    return first
        return ""

    @staticmethod
    def _default_provider() -> Callable[[str, str, str, int], list[str]] | None:
        try:
            from cli.reactive_hints import command_hints
        except ImportError:
            return None
        return command_hints


class GraphSuggestionSource:
    """Status source: top next-step suggestion from the graph advisor."""

    def __init__(
        self,
        config: StatusBarConfig,
        reader: FileSystemReader,
        advisor_factory: Callable[[], Any] | None = None,
    ) -> None:
        """Bind to config, reader, and an optional advisor factory.

        Args:
            config: Active configuration.
            reader: Sessions filesystem reader.
            advisor_factory: Zero-arg callable returning an object that
                exposes ``suggest_next(recent_commands, limit)``. When
                ``None`` the source falls back to ``config.fallback_suggestion``.
        """
        self._config = config
        self._reader = reader
        self._factory = advisor_factory

    def collect(self) -> str:
        """Return a one-token suggestion. Never raises."""
        recent = self._recent_commands()
        if self._factory is None:
            return self._config.fallback_suggestion
        try:
            advisor = self._factory()
            if advisor is None:
                return self._config.fallback_suggestion
            suggestions = advisor.suggest_next(
                recent_commands=recent,
                limit=self._config.suggestion_limit,
            )
        except Exception:
            return self._config.fallback_suggestion
        for entry in suggestions or []:
            label = self._suggestion_label(entry)
            if label:
                return label
        return self._config.fallback_suggestion

    def _recent_commands(self) -> list[str]:
        text = self._reader.read_text(self._config.session_report_filename)
        if not text:
            return []
        try:
            reader = csv.DictReader(text.splitlines())
            rows = []
            for index, row in enumerate(reader):
                if index >= self._config.csv_max_rows:
                    break
                rows.append(row)
        except csv.Error:
            return []
        recent: list[str] = []
        for row in reversed(rows):
            for column in ("tool", "command", "name"):
                raw = (row.get(column) or "").strip()
                if not raw:
                    continue
                first = raw.split()[0]
                if first:
                    recent.append(first)
                    break
            if recent:
                break
        return recent

    @staticmethod
    def _suggestion_label(entry: Any) -> str:
        if isinstance(entry, str):
            return entry.strip()
        if isinstance(entry, dict):
            for key in ("label", "id", "command", "name"):
                value = entry.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
        return ""


class CollabPresenceSource:
    """Status source: number of active collaboration operators.

    Reads ``sessions/operators.json`` (a snapshot written by
    :mod:`modules.collab_bp` or its export hook). The file is expected to
    contain ``{"operators": [{"name": ..., "last_seen": ..., "active": ...}]}``
    where ``last_seen`` is a Unix timestamp. Operators older than
    :attr:`StatusBarConfig.operator_stale_seconds` are filtered out so the
    count reflects live presence and survives a server restart.
    """

    def __init__(
        self,
        config: StatusBarConfig,
        reader: FileSystemReader,
        clock: Callable[[], float] | None = None,
    ) -> None:
        """Bind to the active config, reader, and an injectable clock.

        Args:
            config: Active configuration.
            reader: Sessions reader (the only filesystem entry point).
            clock: Zero-argument callable returning the current Unix
                timestamp. Defaults to :func:`time.time`; tests inject a
                fixed value for determinism.
        """
        import time

        self._config = config
        self._reader = reader
        self._clock = clock or time.time

    def collect(self) -> str:
        """Return the active-operator count formatted as a short string."""
        payload = self._reader.read_json(self._config.operators_filename)
        operators = self._extract_entries(payload)
        if not operators:
            return self._config.fallback_operators
        threshold = self._clock() - self._config.operator_stale_seconds
        active_count = 0
        for entry in operators:
            if self._is_active(entry, threshold):
                active_count += 1
        return str(active_count)

    @staticmethod
    def _extract_entries(payload: Any) -> list[Mapping[str, Any]]:
        if isinstance(payload, dict):
            candidates = payload.get("operators")
            if isinstance(candidates, list):
                return [entry for entry in candidates if isinstance(entry, dict)]
        if isinstance(payload, list):
            return [entry for entry in payload if isinstance(entry, dict)]
        return []

    @staticmethod
    def _is_active(entry: Mapping[str, Any], threshold: float) -> bool:
        active_flag = entry.get("active")
        if active_flag is False:
            return False
        last_seen = entry.get("last_seen")
        if isinstance(last_seen, (int, float)):
            return float(last_seen) >= threshold
        return active_flag is True


class StatusBarRenderer:
    """Compose a sanitised status line from a :class:`StatusContext`."""

    def __init__(self, config: StatusBarConfig) -> None:
        """Bind to the active configuration."""
        self._config = config
        self._pattern = re.compile(config.allowed_field_pattern)

    def render_plain(self, ctx: StatusContext) -> str:
        """Return the line without ANSI colour or readline markers."""
        target = self._sanitise(ctx.target, self._config.max_target_chars)
        phase = self._sanitise(ctx.phase, self._config.max_phase_chars)
        finding = self._sanitise(ctx.last_finding, self._config.max_finding_chars)
        suggestion = self._sanitise(ctx.next_suggestion, self._config.max_suggestion_chars)
        operators_raw = (ctx.operators or "").strip()
        if not operators_raw:
            return self._config.default_format.format(
                target=target,
                phase=phase,
                finding=finding,
                suggestion=suggestion,
            )
        operators = self._sanitise(operators_raw, self._config.max_operators_chars)
        return self._config.default_format_with_operators.format(
            target=target,
            phase=phase,
            finding=finding,
            suggestion=suggestion,
            operators=operators,
        )

    def render_prompt(
        self,
        ctx: StatusContext,
        base_prompt: str,
        color_open: str | None = None,
        color_close: str | None = None,
    ) -> str:
        """Return ``base_prompt`` with the status line prefixed.

        Args:
            ctx: The context snapshot to render.
            base_prompt: Existing prompt string (may already contain ANSI
                wrapped in readline markers).
            color_open: Optional ANSI prefix override. When ``None`` the
                renderer falls back to :attr:`StatusBarConfig.color_open`.
            color_close: Optional ANSI suffix override. When ``None`` the
                renderer falls back to :attr:`StatusBarConfig.color_close`.

        Returns:
            A new prompt string. ANSI sequences inserted here are wrapped
            with readline markers so the input editor counts columns
            correctly.
        """
        body = self.render_plain(ctx)
        if not self._config.color_enabled:
            return f"{body}{self._config.prompt_join}{base_prompt}"
        open_seq = color_open if color_open is not None else self._config.color_open
        close_seq = color_close if color_close is not None else self._config.color_close
        coloured = (
            f"{self._config.readline_open_marker}{open_seq}"
            f"{self._config.readline_close_marker}"
            f"{body}"
            f"{self._config.readline_open_marker}{close_seq}"
            f"{self._config.readline_close_marker}"
        )
        return f"{coloured}{self._config.prompt_join}{base_prompt}"

    def _sanitise(self, value: str, max_chars: int) -> str:
        if value is None:
            value = ""
        text = str(value)
        for token in self._config.forbidden_substrings:
            text = text.replace(token, "")
        text = text.strip()
        bounded = max(1, min(max_chars, self._config.max_field_chars))
        if len(text) > bounded:
            suffix = self._config.truncation_suffix
            keep = max(1, bounded - len(suffix))
            text = text[:keep] + suffix
        if not text:
            text = self._config.fallback_finding
        if not self._pattern.match(text):
            cleaned = re.sub(r"[^\w./:@\-\[\]+ ]", "", text)
            text = cleaned[:bounded] or self._config.fallback_finding
        return text


class StatusBarManager:
    """Lifecycle façade: collect → render → install on the cmd2 shell.

    The manager is the single class ``lazyown.py`` touches. Everything
    else in this module is a private collaborator. Tests instantiate this
    class directly with hand-rolled doubles for sources and shell.
    """

    def __init__(
        self,
        config: StatusBarConfig,
        sources: Mapping[str, IStatusSource],
        renderer: StatusBarRenderer,
        payload: Mapping[str, Any] | None = None,
    ) -> None:
        """Bind config, sources, renderer and a payload mapping.

        Args:
            config: Active configuration.
            sources: Mapping with mandatory keys ``target``, ``phase``,
                ``finding``, ``suggestion``. Each value must be an
                :class:`IStatusSource`.
            renderer: Renderer instance.
            payload: Optional ``payload.json`` mapping used to evaluate
                the enabled flag.

        Raises:
            KeyError: When a mandatory source key is missing.
        """
        required = ("target", "phase", "finding", "suggestion")
        missing = [key for key in required if key not in sources]
        if missing:
            raise KeyError(f"missing status sources: {missing}")
        self._config = config
        self._sources = dict(sources)
        self._renderer = renderer
        self._payload = payload or {}

    @property
    def enabled(self) -> bool:
        """Return ``True`` when the bar should render on this shell."""
        raw = self._payload.get(self._config.enabled_key, self._config.enabled_default)
        if isinstance(raw, bool):
            return raw
        if isinstance(raw, (int, float)):
            return bool(raw)
        if isinstance(raw, str):
            lowered = raw.strip().lower()
            if lowered in self._config.truthy_strings:
                return True
            if lowered in self._config.falsy_strings:
                return False
        return self._config.enabled_default

    def collect_context(self) -> StatusContext:
        """Return a fresh :class:`StatusContext` by polling every source."""
        operators = ""
        if "operators" in self._sources:
            operators = self._safe_collect("operators")
        return StatusContext(
            target=self._safe_collect("target"),
            phase=self._safe_collect("phase"),
            last_finding=self._safe_collect("finding"),
            next_suggestion=self._safe_collect("suggestion"),
            operators=operators,
        )

    def render_prompt(self, base_prompt: str) -> str:
        """Return the prompt with the status line prefixed when enabled.

        The active TUI theme is resolved on every call so a live
        ``set tui_theme bright`` updates the prompt colour on the next
        prompt without restarting the shell.
        """
        if not self.enabled:
            return base_prompt
        color_open, color_close = self._resolve_theme_colors()
        return self._renderer.render_prompt(
            self.collect_context(), base_prompt, color_open, color_close
        )

    def _resolve_theme_colors(self) -> tuple[str | None, str | None]:
        """Return ``(open, close)`` ANSI sequences from the active theme."""
        try:
            from cli.themes import theme_from_payload

            theme = theme_from_payload(self._payload)
            return theme.bar_open, theme.bar_close
        except Exception:
            return None, None

    def render_plain_line(self, ctx: StatusContext | None = None) -> str:
        """Return the rendered status line without ANSI / readline markers.

        Args:
            ctx: Optional pre-collected context. When ``None`` the
                manager collects a fresh one.

        Returns:
            The plain status line. Useful for the ``status_bar show``
            verb when colour escapes would clutter operator scripts.
        """
        snapshot = ctx if ctx is not None else self.collect_context()
        return self._renderer.render_plain(snapshot)

    def set_enabled(self, enabled: bool) -> None:
        """Persist a new enabled state in the payload-backed flag.

        The payload mapping passed to the manager is mutated in place so
        subsequent ``enabled`` reads reflect the change without a config
        reload. Non-mapping payloads are ignored.
        """
        if isinstance(self._payload, dict):
            self._payload[self._config.enabled_key] = bool(enabled)

    def install(
        self,
        shell: Any,
        base_prompt_attribute: str = "custom_prompt",
        prompt_attribute: str = "prompt",
    ) -> bool:
        """Wire the manager into ``shell`` via a precommand hook.

        Args:
            shell: The :class:`cmd2.Cmd` instance.
            base_prompt_attribute: Attribute on the shell that holds the
                static prompt (used as the suffix on every refresh).
            prompt_attribute: Attribute on the shell that cmd2 reads when
                drawing the prompt.

        Returns:
            ``True`` when the hook was registered, ``False`` otherwise.
            Failure is always silent — the shell must boot even when the
            status bar cannot be installed.
        """
        if shell is None or not hasattr(shell, "register_precmd_hook"):
            return False
        base_prompt = getattr(shell, base_prompt_attribute, None) or getattr(shell, prompt_attribute, "")
        if not isinstance(base_prompt, str):
            base_prompt = ""
        try:
            setattr(shell, prompt_attribute, self.render_prompt(base_prompt))
        except Exception:
            pass
        hook = self._build_precmd_hook(shell, base_prompt, base_prompt_attribute, prompt_attribute)
        if hook is None:
            return False
        try:
            shell.register_precmd_hook(hook)
        except Exception:
            return False
        return True

    def _build_precmd_hook(
        self,
        shell: Any,
        base_prompt: str,
        base_prompt_attribute: str,
        prompt_attribute: str,
    ) -> Callable[[Any], Any] | None:
        """Return a cmd2-compatible precmd hook or ``None`` when cmd2 is absent.

        cmd2 enforces strict type annotations on hook callables — the
        single parameter and the return type must both be
        ``cmd2.plugin.PrecommandData``. The closure built here therefore
        binds those exact annotations at install time so the hook passes
        ``Cmd._validate_prepostcmd_hook``.
        """
        try:
            from cmd2.plugin import PrecommandData
        except ImportError:
            return None

        def _hook(data):
            try:
                fresh_base = getattr(shell, base_prompt_attribute, base_prompt)
                if not isinstance(fresh_base, str) or not fresh_base:
                    fresh_base = base_prompt
                setattr(shell, prompt_attribute, self.render_prompt(fresh_base))
            except Exception:
                pass
            return data

        _hook.__annotations__ = {"data": PrecommandData, "return": PrecommandData}
        _hook.__name__ = "status_bar_precmd_hook"
        return _hook

    def _safe_collect(self, key: str) -> str:
        try:
            value = self._sources[key].collect()
        except Exception:
            return self._fallback_for(key)
        if not isinstance(value, str) or not value.strip():
            return self._fallback_for(key)
        return value

    def _fallback_for(self, key: str) -> str:
        return {
            "target": self._config.fallback_target,
            "phase": self._config.fallback_phase,
            "finding": self._config.fallback_finding,
            "suggestion": self._config.fallback_suggestion,
            "operators": self._config.fallback_operators,
        }.get(key, "")


def _operator_presence_enabled(
    payload: Mapping[str, Any] | None,
    config: StatusBarConfig,
) -> bool:
    """Return ``True`` when the operator-presence segment should be wired in."""
    if not payload:
        return config.operators_enabled_default
    raw = payload.get(config.operators_enabled_key, config.operators_enabled_default)
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, (int, float)):
        return bool(raw)
    if isinstance(raw, str):
        lowered = raw.strip().lower()
        if lowered in config.truthy_strings:
            return True
        if lowered in config.falsy_strings:
            return False
    return config.operators_enabled_default


def build_default_manager(
    payload: Mapping[str, Any] | None,
    sessions_dir: str | None = None,
    advisor_factory: Callable[[], Any] | None = None,
    config: StatusBarConfig | None = None,
) -> StatusBarManager:
    """Wire the canonical multi-source manager used by the live shell.

    When ``payload['enable_operator_presence']`` is truthy the manager is
    extended with a fifth :class:`CollabPresenceSource` keyed
    ``operators``. The historical four-segment layout is preserved when
    that flag is absent so existing operators see no change.

    Args:
        payload: Loaded ``payload.json``.
        sessions_dir: Optional override for the sessions root. When given
            it replaces ``config.sessions_dir``.
        advisor_factory: Zero-arg callable returning a
            :class:`cli.graph_advisor.GraphAdvisor`. Optional.
        config: Optional explicit :class:`StatusBarConfig`. When omitted
            the config is derived from ``payload``.

    Returns:
        A fully constructed :class:`StatusBarManager` ready for
        :meth:`StatusBarManager.install`.
    """
    cfg = config or StatusBarConfig.from_payload(payload)
    if sessions_dir is not None and sessions_dir.strip():
        cfg = replace(cfg, sessions_dir=sessions_dir.strip())
    reader = FileSystemReader(cfg)
    phase_source = WorldModelPhaseSource(cfg, reader, payload)
    sources: dict[str, IStatusSource] = {
        "target": PayloadTargetSource(cfg, payload),
        "phase": phase_source,
        "finding": SessionFindingSource(cfg, reader),
        "suggestion": CommandHintSuggestionSource(cfg, reader, phase_source.collect),
    }
    if _operator_presence_enabled(payload, cfg):
        sources["operators"] = CollabPresenceSource(cfg, reader)
    renderer = StatusBarRenderer(cfg)
    return StatusBarManager(cfg, sources, renderer, payload)


__all__ = [
    "StatusBarConfig",
    "StatusContext",
    "IStatusSource",
    "FileSystemReader",
    "PayloadTargetSource",
    "WorldModelPhaseSource",
    "SessionFindingSource",
    "GraphSuggestionSource",
    "CommandHintSuggestionSource",
    "CollabPresenceSource",
    "StatusBarRenderer",
    "StatusBarManager",
    "build_default_manager",
]
