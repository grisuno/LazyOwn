"""Reusable Textual modals shared by the LazyOwn operator consoles.

``lazy_orchestrator`` and the marketplace manager need the same building
blocks: a key/value form, a searchable picker, a destructive-action
confirmation, and a raw YAML editor. Keeping them in one module avoids
two slightly different modal implementations drifting apart.

The apps only need to expose the shared CSS classes (``modal-box``,
``modal-title``, ``modal-label``, ``modal-hint``, ``modal-error``).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, OptionList, Static, TextArea
from textual.widgets.option_list import Option

MAX_OPTIONS = 300
_SEARCH_LIMIT = 400


def filter_candidates(
    query: str,
    options: Sequence[tuple[str, str]],
    limit: int = MAX_OPTIONS,
) -> list[tuple[str, str]]:
    """Filter ``(value, description)`` pairs by a case-insensitive query.

    Ranking is deterministic and stable: prefix matches first, then
    substring matches in the value, then substring matches only in the
    description. Original order is preserved inside each bucket.

    Args:
        query: Operator input typed in the search box.
        options: Candidate pairs.
        limit: Maximum rows returned.

    Returns:
        The filtered pairs in display order.
    """
    needle = str(query or "").strip().lower()
    if not needle:
        return list(options)[: max(limit, 0)]
    prefix: list[tuple[str, str]] = []
    contains: list[tuple[str, str]] = []
    described: list[tuple[str, str]] = []
    for value, description in options:
        name = str(value).lower()
        if name.startswith(needle):
            prefix.append((value, description))
        elif needle in name:
            contains.append((value, description))
        elif needle in str(description).lower():
            described.append((value, description))
    return (prefix + contains + described)[: max(limit, 0)]


class FormModal(ModalScreen[dict]):
    """Generic key/value modal with optional pre-filled defaults."""

    BINDINGS = [("escape", "dismiss(None)", "cancel")]

    def __init__(
        self,
        title: str,
        fields: Iterable[tuple[str, str, str]],
        defaults: dict[str, str] | None = None,
        save_label: str = "Save",
    ) -> None:
        """Store the title, ``(id, label, placeholder)`` fields and defaults."""
        super().__init__()
        self._title = title
        self._fields = list(fields)
        self._defaults = dict(defaults or {})
        self._save_label = save_label

    def compose(self) -> ComposeResult:
        """One labeled input per field plus the save button."""
        with Vertical(classes="modal-box"):
            yield Static(self._title, classes="modal-title")
            for field_id, label, placeholder in self._fields:
                yield Static(label, classes="modal-label")
                yield Input(
                    value=str(self._defaults.get(field_id, "")),
                    placeholder=placeholder,
                    id=field_id,
                )
            yield Button(self._save_label, id="modal-save", variant="primary")

    def _values(self) -> dict[str, str]:
        """Collect the current input values."""
        return {
            field_id: str(self.query_one(f"#{field_id}", Input).value).strip()
            for field_id, _label, _placeholder in self._fields
        }

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Save closes the modal with every field value."""
        if event.button.id == "modal-save":
            self.dismiss(self._values())

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter commits the form like the save button."""
        self.dismiss(self._values())


class SearchSelectModal(ModalScreen[str | None]):
    """Searchable select with a free-text fallback.

    The operator types to filter an ``OptionList``. Enter selects the
    highlighted row, or returns the typed text when no row matches so a
    new command name can still be registered without leaving the modal.
    """

    BINDINGS = [("escape", "dismiss(None)", "cancel")]

    def __init__(
        self,
        title: str,
        options: Sequence[tuple[str, str]],
        placeholder: str = "type to filter",
        allow_custom: bool = True,
    ) -> None:
        """Store the title, candidate pairs and placeholder."""
        super().__init__()
        self._title = title
        self._options = list(options)
        self._placeholder = placeholder
        self._allow_custom = allow_custom

    def compose(self) -> ComposeResult:
        """Search box, filtered option list and action buttons."""
        with Vertical(classes="modal-box"):
            yield Static(self._title, classes="modal-title")
            yield Input(placeholder=self._placeholder, id="select-search")
            yield OptionList(id="select-options")
            yield Static("", id="select-hint", classes="modal-hint")
            yield Button("Select", id="select-ok", variant="primary")
            yield Button("Cancel", id="select-cancel")
        self._render_options("")

    def on_mount(self) -> None:
        """Render the first page and focus the search box."""
        self._render_options("")
        try:
            self.query_one("#select-search", Input).focus()
        except Exception:
            pass

    def _render_options(self, query: str) -> None:
        """Rebuild the option list for the current query."""
        try:
            option_list = self.query_one("#select-options", OptionList)
        except Exception:
            return
        matches = filter_candidates(query, self._options)
        option_list.clear_options()
        for value, description in matches:
            label = f"{value}  -  {description}" if description else value
            option_list.add_option(Option(label, id=value))
        if not matches:
            option_list.add_option(Option("no match - Enter uses the typed name", id="__custom__"))
            self._hint(f"no match; Enter uses {query.strip()!r}")
        else:
            self._hint(f"{len(matches)} match(es); Enter selects, arrows move")

    def _hint(self, text: str) -> None:
        """Update the hint line when the widget is mounted."""
        try:
            self.query_one("#select-hint", Static).update(text)
        except Exception:
            pass

    def _selected_value(self) -> str:
        """Return the highlighted option id, ignoring the custom placeholder."""
        try:
            option_list = self.query_one("#select-options", OptionList)
            if option_list.highlighted is None and option_list.option_count:
                option_list.highlighted = 0
            option = option_list.get_option_at_index(option_list.highlighted or 0)
            value = str(option.id or "")
        except Exception:
            return ""
        return "" if value == "__custom__" else value

    def _accept(self) -> None:
        """Dismiss with the highlighted value or the typed fallback."""
        value = self._selected_value()
        if not value:
            typed = str(self.query_one("#select-search", Input).value).strip()
            if typed and self._allow_custom:
                value = typed
        if value:
            self.dismiss(value)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Filter as the operator types."""
        if event.input.id == "select-search":
            self._render_options(event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter accepts the highlighted row or the typed custom value."""
        if event.input.id == "select-search":
            self._accept()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Clicking or pressing Enter on a row selects it."""
        value = str(event.option.id or "")
        if value == "__custom__":
            self._accept()
            return
        if value:
            self.dismiss(value)

    def on_key(self, event) -> None:
        """Move focus into the list with the arrow keys."""
        if event.key not in ("down", "up"):
            return
        try:
            search = self.query_one("#select-search", Input)
            option_list = self.query_one("#select-options", OptionList)
        except Exception:
            return
        if not search.has_focus or option_list.option_count == 0:
            return
        option_list.focus()
        if event.key == "down":
            option_list.action_cursor_down()
        else:
            option_list.action_cursor_up()
        event.prevent_default()
        event.stop()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Select and cancel buttons."""
        if event.button.id == "select-ok":
            self._accept()
        elif event.button.id == "select-cancel":
            self.dismiss(None)


class ConfirmModal(ModalScreen[bool]):
    """Small yes/no modal for destructive file actions."""

    BINDINGS = [
        Binding("y", "answer(True)", "Yes"),
        Binding("n", "answer(False)", "No"),
        Binding("escape", "answer(False)", "Cancel"),
    ]

    def __init__(self, title: str, body: str = "") -> None:
        """Store the prompt."""
        super().__init__()
        self._title = title
        self._body = body

    def compose(self) -> ComposeResult:
        """Prompt plus yes/no buttons."""
        with Vertical(classes="modal-box"):
            yield Static(self._title, classes="modal-title")
            if self._body:
                yield Static(self._body, classes="modal-label")
            with Vertical():
                yield Button("Delete", id="confirm-yes", variant="error")
                yield Button("Cancel", id="confirm-no")

    def action_answer(self, answer: bool) -> None:
        """Dismiss with the operator's answer."""
        self.dismiss(bool(answer))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Wire the two buttons to the same answer action."""
        if event.button.id == "confirm-yes":
            self.dismiss(True)
        elif event.button.id == "confirm-no":
            self.dismiss(False)


class TextEditorModal(ModalScreen[str | None]):
    """Raw text editor with a validator hook before saving.

    Args:
        title: Modal title.
        text: Initial document.
        validator: Optional callable raising ``ValueError`` on invalid
            content. The message is shown inside the modal.
        language: Syntax highlighting hint (``yaml``, ``json``, ...).
        save_label: Label for the save button.
    """

    BINDINGS = [("escape", "dismiss(None)", "cancel")]

    def __init__(
        self,
        title: str,
        text: str,
        validator: Callable[[str], None] | None = None,
        language: str = "yaml",
        save_label: str = "Save",
    ) -> None:
        """Store the title, initial document, validator and language."""
        super().__init__()
        self._title = title
        self._text = text
        self._validator = validator
        self._language = language
        self._save_label = save_label

    def compose(self) -> ComposeResult:
        """Editor plus save/cancel buttons and an error line."""
        with Vertical(classes="modal-box-wide"):
            yield Static(self._title, classes="modal-title")
            yield TextArea(text=self._text, language=self._language, id="text-editor")
            yield Static("", id="text-error", classes="modal-error")
            yield Button(self._save_label, id="text-save", variant="primary")
            yield Button("Cancel", id="text-cancel")

    def _current_text(self) -> str:
        """Return the editor contents."""
        return str(self.query_one("#text-editor", TextArea).text)

    def _save(self) -> None:
        """Validate and dismiss with the edited document."""
        text = self._current_text()
        if self._validator is not None:
            try:
                self._validator(text)
            except ValueError as exc:
                self.query_one("#text-error", Static).update(str(exc))
                return
        self.dismiss(text)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Save and cancel buttons."""
        if event.button.id == "text-save":
            self._save()
        elif event.button.id == "text-cancel":
            self.dismiss(None)


YamlEditorModal = TextEditorModal


__all__ = [
    "ConfirmModal",
    "FormModal",
    "SearchSelectModal",
    "TextEditorModal",
    "YamlEditorModal",
    "filter_candidates",
]
