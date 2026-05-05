"""Result list and action model for the command palette."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QListView, QWidget

from lazygui.config.constants import AppConstants


@dataclass(frozen=True, slots=True)
class CommandPaletteAction:
    """A user-visible entry inside the command palette."""

    identifier: str
    title: str
    subtitle: str
    invoke: Callable[[], None]


_ACTION_USER_ROLE_OFFSET: int = 32


class CommandPaletteList(QListView):
    """List view backed by a fuzzy-filtered :class:`CommandPaletteAction` set."""

    action_invoked = Signal(CommandPaletteAction)

    def __init__(
        self,
        constants: AppConstants,
        actions: Iterable[CommandPaletteAction],
        parent: QWidget | None = None,
    ) -> None:
        """Store the action set and prepare the underlying model."""
        super().__init__(parent)
        self._constants = constants
        self.setObjectName("CommandPaletteResults")
        self.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self.setUniformItemSizes(True)
        self._model = QStandardItemModel(self)
        self.setModel(self._model)
        self._all_actions: tuple[CommandPaletteAction, ...] = tuple(actions)
        self._filtered_actions: tuple[CommandPaletteAction, ...] = self._all_actions
        self._populate(self._all_actions)
        self.activated.connect(self._on_activated)

    def set_actions(self, actions: Iterable[CommandPaletteAction]) -> None:
        """Replace the entire action registry and reset the filter."""
        self._all_actions = tuple(actions)
        self.apply_filter("")

    def apply_filter(self, query: str) -> None:
        """Filter the action set using a substring + token-order heuristic."""
        normalized = query.strip().lower()
        if not normalized:
            self._filtered_actions = self._all_actions
        else:
            scored: list[tuple[int, CommandPaletteAction]] = []
            for action in self._all_actions:
                score = _fuzzy_score(normalized, action.title, action.subtitle)
                if score >= 0:
                    scored.append((score, action))
            scored.sort(key=lambda item: item[0])
            limit = self._constants.palette.max_results
            self._filtered_actions = tuple(action for _score, action in scored[:limit])
        self._populate(self._filtered_actions)
        if self._model.rowCount() > 0:
            self.setCurrentIndex(self._model.index(0, 0))

    def invoke_current(self) -> None:
        """Invoke whichever action is currently highlighted, if any."""
        index = self.currentIndex()
        if not index.isValid():
            return
        action = index.data(role=Qt.ItemDataRole.UserRole + _ACTION_USER_ROLE_OFFSET)
        if isinstance(action, CommandPaletteAction):
            self.action_invoked.emit(action)

    def _on_activated(self, _index) -> None:
        """Forward double-click / Enter to :meth:`invoke_current`."""
        self.invoke_current()

    def _populate(self, actions: Iterable[CommandPaletteAction]) -> None:
        """Rebuild the item model with one row per action."""
        self._model.clear()
        for action in actions:
            item = QStandardItem(f"{action.title}\n{action.subtitle}")
            item.setEditable(False)
            item.setData(action, role=Qt.ItemDataRole.UserRole + _ACTION_USER_ROLE_OFFSET)
            self._model.appendRow(item)


def _fuzzy_score(query: str, title: str, subtitle: str) -> int:
    """Return a sortable score (lower is better) or ``-1`` if no match.

    The algorithm prefers matches in ``title`` over ``subtitle`` and rewards
    shorter strings, which keeps highly relevant short titles at the top.
    """
    haystack_title = title.lower()
    haystack_subtitle = subtitle.lower()
    if query in haystack_title:
        return haystack_title.index(query)
    if query in haystack_subtitle:
        return len(haystack_title) + haystack_subtitle.index(query)
    return _token_order_score(query, haystack_title, base_offset=0)


def _token_order_score(query: str, haystack: str, base_offset: int) -> int:
    """Score by ensuring all query chars appear in order somewhere in haystack."""
    cursor = 0
    score = base_offset
    for char in query:
        found = haystack.find(char, cursor)
        if found < 0:
            return -1
        score += found - cursor
        cursor = found + 1
    return score
