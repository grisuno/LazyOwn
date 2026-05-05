"""Theme registry and runtime application of stylesheets.

The :class:`ThemeManager` holds the available palettes, applies the active
one onto the running :class:`QApplication`, and emits ``theme_changed`` so
widgets that draw with custom painters can refresh their cached colours.
"""

from __future__ import annotations

import logging
from typing import Iterable, Mapping

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from lazygui.config.constants import AppConstants
from lazygui.config.settings import AppSettings
from lazygui.theme.palettes import builtin_palettes
from lazygui.theme.qss_builder import QssBuilder
from lazygui.theme.tokens import ThemeTokens

_logger = logging.getLogger(__name__)


class ThemeManager(QObject):
    """Owns palettes and applies them to the application instance."""

    theme_changed = Signal(ThemeTokens)

    def __init__(
        self,
        constants: AppConstants,
        settings: AppSettings,
        application: QApplication,
        palettes: Mapping[str, ThemeTokens] | None = None,
        parent: QObject | None = None,
    ) -> None:
        """Initialise the manager.

        :param constants: shared :class:`AppConstants` instance.
        :param settings: persisted :class:`AppSettings` for read/write of the
            active theme identifier.
        :param application: the running ``QApplication`` instance.
        :param palettes: optional override registry; defaults to the built-in
            palettes returned by :func:`builtin_palettes`.
        """
        super().__init__(parent)
        self._constants = constants
        self._settings = settings
        self._application = application
        self._palettes: dict[str, ThemeTokens] = dict(palettes or builtin_palettes())
        self._builder = QssBuilder(constants=constants)
        self._active_id: str | None = None

    @property
    def active_tokens(self) -> ThemeTokens:
        """Currently active :class:`ThemeTokens`. Defaults if none set yet."""
        if self._active_id is None:
            return self._palettes[self._constants.theme.default_palette_id]
        return self._palettes[self._active_id]

    @property
    def active_id(self) -> str:
        """Identifier of the active palette."""
        return self._active_id or self._constants.theme.default_palette_id

    def available(self) -> Iterable[ThemeTokens]:
        """Yield all registered palettes in registration order."""
        return tuple(self._palettes.values())

    def apply_initial(self) -> None:
        """Load the saved theme identifier and apply it."""
        candidate = self._settings.theme_id
        if candidate not in self._palettes:
            _logger.warning("Saved theme %r not found; falling back to default.", candidate)
            candidate = self._constants.theme.default_palette_id
        self.apply(candidate)

    def apply(self, identifier: str) -> None:
        """Activate the palette with ``identifier`` and persist the choice."""
        if identifier not in self._palettes:
            raise KeyError(f"Unknown theme identifier: {identifier!r}")
        if identifier == self._active_id:
            return
        tokens = self._palettes[identifier]
        self._active_id = identifier
        self._apply_to_application(tokens)
        self._settings.theme_id = identifier
        self._settings.save()
        self.theme_changed.emit(tokens)

    def cycle(self) -> None:
        """Switch to the next palette, wrapping at the end of the registry."""
        order = self._constants.theme.palette_ids
        try:
            current_index = order.index(self.active_id)
        except ValueError:
            current_index = -1
        next_index = (current_index + 1) % len(order)
        self.apply(order[next_index])

    def _apply_to_application(self, tokens: ThemeTokens) -> None:
        stylesheet = self._builder.build(tokens)
        self._application.setStyleSheet(stylesheet)
        self._application.setPalette(self._build_qpalette(tokens))

    @staticmethod
    def _build_qpalette(tokens: ThemeTokens) -> QPalette:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(tokens.background_base))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(tokens.text_primary))
        palette.setColor(QPalette.ColorRole.Base, QColor(tokens.background_elevated))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(tokens.surface_subtle))
        palette.setColor(QPalette.ColorRole.Text, QColor(tokens.text_primary))
        palette.setColor(QPalette.ColorRole.Button, QColor(tokens.surface_subtle))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(tokens.text_primary))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(tokens.accent))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(tokens.text_on_accent))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(tokens.background_overlay))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(tokens.text_primary))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(tokens.text_muted))
        return palette
