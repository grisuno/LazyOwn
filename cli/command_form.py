"""Textual form-mode launcher for LazyOwn commands.

The form turns any ``do_*`` command into a guided launcher: the operator
picks a command name, sees the inferred summary, reviews the relevant
``payload.json`` values that the command would read, types optional
extra arguments, and confirms with Enter. The launcher returns the final
command string so the cmd2 shell can dispatch it as if the operator had
typed it.

The form does not parse argparser specifications today — it surfaces the
fields most commonly tuned per invocation (target, ports, wordlists,
custom args) so the operator no longer has to remember flag names from
the docs. New per-command fields are added by extending
:attr:`CommandFormConfig.field_sets`.

Design (SOLID):

- Single Responsibility: :class:`CommandFormConfig` owns constants,
  :class:`CommandFormState` builds the field list and assembles the final
  command, :class:`CommandFormApp` renders.
- Open/Closed: a new per-command field set is one tuple entry in the
  config; the state and the app do not change.
- Dependency Inversion: the state takes a pre-loaded command index +
  payload mapping; tests inject in-memory dicts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, MutableMapping

from cli.themes import Theme, theme_from_payload


@dataclass(frozen=True)
class FormField:
    """Single editable input in the form."""

    identifier: str
    label: str
    payload_key: str
    default: str = ""
    placeholder: str = ""


@dataclass(frozen=True)
class CommandFieldSet:
    """Fields the form surfaces for a given command name."""

    command: str
    fields: tuple[FormField, ...]


@dataclass(frozen=True)
class CommandFormConfig:
    """Centralised constants for the form-mode launcher."""

    title: str = "Command form"
    subtitle: str = "Tab to switch fields, Enter to run, Esc to cancel"
    extra_args_label: str = "Extra arguments"
    extra_args_placeholder: str = "Optional positional or flag-style args"
    missing_command_message: str = "Command not found in index."
    default_field_set: tuple[FormField, ...] = (
        FormField("target", "Target (rhost)", "rhost", placeholder="10.0.0.1"),
        FormField("attacker", "Attacker (lhost)", "lhost", placeholder="10.10.14.20"),
        FormField("port", "Target port (rport)", "rport"),
    )
    field_sets: tuple[CommandFieldSet, ...] = (
        CommandFieldSet(
            "do_lazynmap",
            (
                FormField("target", "Target (rhost)", "rhost", placeholder="10.0.0.1"),
                FormField("port", "Target port (rport)", "rport"),
                FormField("device", "Interface (device)", "device"),
            ),
        ),
        CommandFieldSet(
            "do_gobuster",
            (
                FormField("target", "Target (rhost)", "rhost"),
                FormField("port", "Target port (rport)", "rport"),
                FormField("wordlist", "Directory wordlist", "dirwordlist"),
            ),
        ),
        CommandFieldSet(
            "do_ffuf",
            (
                FormField("url", "Target URL", "url"),
                FormField("wordlist", "Directory wordlist", "dirwordlist"),
            ),
        ),
        CommandFieldSet(
            "do_enum4linux",
            (
                FormField("target", "Target (rhost)", "rhost"),
                FormField("domain", "Domain", "domain"),
            ),
        ),
        CommandFieldSet(
            "do_kerbrute",
            (
                FormField("target", "Target (rhost)", "rhost"),
                FormField("domain", "Domain", "domain"),
                FormField("wordlist", "Username wordlist", "usrwordlist"),
            ),
        ),
        CommandFieldSet(
            "do_searchsploit",
            (FormField("target", "Target (rhost)", "rhost"),),
        ),
    )


@dataclass
class CommandFormState:
    """Pure data layer for the form."""

    config: CommandFormConfig
    command_name: str
    index: Mapping[str, Any]
    payload: Mapping[str, Any]
    values: MutableMapping[str, str] = field(default_factory=dict)
    extra_args: str = ""

    def __post_init__(self) -> None:
        for field_spec in self.fields():
            if field_spec.identifier not in self.values:
                self.values[field_spec.identifier] = self._default_for(field_spec)

    def fields(self) -> tuple[FormField, ...]:
        """Return the fields associated with :attr:`command_name`."""
        normalised = self._normalise_command(self.command_name)
        for field_set in self.config.field_sets:
            if field_set.command == normalised:
                return field_set.fields
        return self.config.default_field_set

    def summary(self) -> str:
        """Return the command summary from the index, or an empty string."""
        normalised = self._normalise_command(self.command_name)
        for row in self._iter_rows():
            if row.get("name") == normalised:
                value = row.get("summary")
                if isinstance(value, str):
                    return value.strip()
                break
        return ""

    def set_value(self, identifier: str, value: str) -> None:
        """Update the value of one field."""
        self.values[identifier] = (value or "").strip()

    def set_extra_args(self, value: str) -> None:
        """Replace the extra-args buffer."""
        self.extra_args = (value or "").strip()

    def build_command(self) -> str:
        """Return the cmd-line preview string the operator sees.

        The preview is a single readable line — overrides are rendered
        as inline ``key=value`` annotations. The actual dispatch in
        :class:`LazyOwnShell.do_form` applies overrides one at a time
        through ``assign`` (see :meth:`overrides` + :meth:`verb_line`)
        so the form never depends on cmd2's settable subsystem.
        """
        verb_line = self.verb_line()
        annotations = " ".join(f"{key}={value}" for key, value in self.overrides())
        if annotations:
            return f"{annotations} | {verb_line}"
        return verb_line

    def overrides(self) -> list[tuple[str, str]]:
        """Return ``[(payload_key, value), ...]`` for fields the operator changed.

        Each pair is applied through ``assign`` by the dispatcher so the
        mutation is validated and persisted just like a manual
        ``assign rhost 10.0.0.5`` would be.
        """
        out: list[tuple[str, str]] = []
        for field_spec in self.fields():
            current = self.values.get(field_spec.identifier, "")
            payload_value = self._payload_str(field_spec.payload_key)
            if current and current != payload_value:
                out.append((field_spec.payload_key, current))
        return out

    def verb_line(self) -> str:
        """Return ``"<verb> <extra_args>"`` ready for the shell."""
        verb = self._verb(self.command_name)
        if self.extra_args:
            return f"{verb} {self.extra_args}".strip()
        return verb

    def is_valid(self) -> bool:
        """Return ``True`` when the command name is known in the index."""
        normalised = self._normalise_command(self.command_name)
        return any(row.get("name") == normalised for row in self._iter_rows())

    def _default_for(self, field_spec: FormField) -> str:
        if field_spec.default:
            return field_spec.default
        return self._payload_str(field_spec.payload_key)

    def _payload_str(self, key: str) -> str:
        value = self.payload.get(key) if isinstance(self.payload, Mapping) else None
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, (int, float, bool)):
            return str(value)
        return ""

    def _iter_rows(self) -> Iterable[Mapping[str, Any]]:
        rows = self.index.get("commands") if isinstance(self.index, Mapping) else None
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, Mapping)]
        return []

    @staticmethod
    def _normalise_command(name: str) -> str:
        candidate = (name or "").strip()
        if not candidate:
            return ""
        if not candidate.startswith("do_"):
            return f"do_{candidate}"
        return candidate

    @staticmethod
    def _verb(name: str) -> str:
        candidate = (name or "").strip()
        if candidate.startswith("do_"):
            return candidate[3:]
        return candidate


def _load_index() -> Mapping[str, Any]:
    try:
        from cli.palette import load_index
    except Exception:
        return {}
    try:
        return load_index()
    except Exception:
        return {}


def build_state(
    command_name: str,
    payload: Mapping[str, Any] | None = None,
    index: Mapping[str, Any] | None = None,
    config: CommandFormConfig | None = None,
) -> CommandFormState:
    """Wire the canonical state used by :func:`launch_form`."""
    return CommandFormState(
        config=config or CommandFormConfig(),
        command_name=command_name,
        index=index if index is not None else _load_index(),
        payload=payload or {},
    )


def launch_form(
    command_name: str,
    payload: Mapping[str, Any] | None = None,
    state: CommandFormState | None = None,
    runner: Any | None = None,
) -> CommandFormState | None:
    """Open the form and return the populated state on submit.

    Args:
        command_name: ``do_*`` (or plain verb) to pre-fill.
        payload: Loaded ``payload.json``.
        state: Optional pre-built state (tests inject one).
        runner: Optional callable used by tests instead of Textual.

    Returns:
        The :class:`CommandFormState` the operator confirmed, or
        ``None`` when cancelled / Textual is unavailable. The caller
        applies :meth:`CommandFormState.overrides` through ``assign``
        and dispatches :meth:`CommandFormState.verb_line`.
    """
    chosen = state if state is not None else build_state(command_name, payload=payload)
    theme = theme_from_payload(payload)
    if runner is not None:
        return runner({"state": chosen, "theme": theme})
    app = _build_app(chosen, theme)
    if app is None:
        return None
    try:
        result = app.run()
    except Exception:
        return None
    if isinstance(result, CommandFormState):
        return result
    return None


def _build_app(state: CommandFormState, theme: Theme) -> Any | None:
    try:
        from textual.app import App, ComposeResult
        from textual.binding import Binding
        from textual.containers import Vertical
        from textual.widgets import Footer, Header, Input, Static
    except Exception:
        return None

    cfg = state.config

    class _CommandFormApp(App):
        TITLE = cfg.title
        SUB_TITLE = cfg.subtitle
        BINDINGS = [
            Binding("escape", "cancel", "Cancel"),
            Binding("ctrl+enter", "submit", "Run", show=False),
        ]
        CSS = (
            "Screen { align: center middle; }\n"
            "#form-root { width: 70%; height: auto; border: round $primary; padding: 1 2; }\n"
            "#form-summary { color: $text-muted; }\n"
            "#form-preview { color: $accent; margin-top: 1; }\n"
            ".form-row { layout: horizontal; height: 3; }\n"
            ".form-row Static { width: 28; }\n"
        )

        def __init__(self) -> None:
            super().__init__()
            self._state = state
            self._theme = theme

        def compose(self) -> ComposeResult:
            yield Header()
            with Vertical(id="form-root"):
                yield Static(f"command: {self._state.command_name}", id="form-command")
                yield Static(self._state.summary() or "(no summary)", id="form-summary")
                for field_spec in self._state.fields():
                    initial = self._state.values.get(field_spec.identifier, "")
                    yield Static(field_spec.label)
                    yield Input(
                        value=initial,
                        placeholder=field_spec.placeholder,
                        id=f"field-{field_spec.identifier}",
                    )
                yield Static(cfg.extra_args_label)
                yield Input(placeholder=cfg.extra_args_placeholder, id="field-extra")
                yield Static("", id="form-preview")
            yield Footer()

        def on_mount(self) -> None:
            self._refresh_preview()

        def on_input_changed(self, event: Input.Changed) -> None:
            identifier_with_prefix = event.input.id or ""
            if identifier_with_prefix == "field-extra":
                self._state.set_extra_args(event.value or "")
            elif identifier_with_prefix.startswith("field-"):
                identifier = identifier_with_prefix[len("field-") :]
                self._state.set_value(identifier, event.value or "")
            self._refresh_preview()

        def on_input_submitted(self, event: Input.Submitted) -> None:
            self.action_submit()

        def action_submit(self) -> None:
            self.exit(result=self._state)

        def action_cancel(self) -> None:
            self.exit()

        def _refresh_preview(self) -> None:
            preview = self.query_one("#form-preview", Static)
            preview.update(self._state.build_command())

    return _CommandFormApp()


__all__ = [
    "CommandFieldSet",
    "CommandFormConfig",
    "CommandFormState",
    "FormField",
    "build_state",
    "launch_form",
]
