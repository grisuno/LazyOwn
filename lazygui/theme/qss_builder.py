"""Builds a Qt stylesheet string from :class:`ThemeTokens`.

Centralising the QSS template here keeps widgets ignorant of styling. They
declare ``objectName``s and selectors; the builder owns the visual contract.
"""

from __future__ import annotations

from dataclasses import dataclass

from lazygui.config.constants import AppConstants
from lazygui.theme.tokens import ThemeTokens


@dataclass(frozen=True, slots=True)
class QssBuilder:
    """Renders a complete QSS sheet for a given theme."""

    constants: AppConstants

    def build(self, tokens: ThemeTokens) -> str:
        """Return the full QSS sheet for ``tokens``."""
        font_family = self._font_stack(self.constants.font.sans_stack)
        mono_family = self._font_stack(self.constants.font.monospace_stack)
        spacing = tokens.spacing_unit_px
        return _QSS_TEMPLATE.format(
            tokens=tokens,
            base_pt=self.constants.font.base_pt,
            title_pt=self.constants.font.title_pt,
            mono_pt=self.constants.font.monospace_pt,
            font_family=font_family,
            mono_family=mono_family,
            spacing=spacing,
            spacing_double=spacing * 2,
            spacing_half=max(1, spacing // 2),
        )

    @staticmethod
    def _font_stack(stack: tuple[str, ...]) -> str:
        return ", ".join(f'"{name}"' for name in stack)


_QSS_TEMPLATE = """
* {{
    color: {tokens.text_primary};
    font-family: {font_family};
    font-size: {base_pt}pt;
}}

QMainWindow, QDialog, QWidget {{
    background-color: {tokens.background_base};
}}

QToolBar {{
    background-color: {tokens.background_elevated};
    border: none;
    padding: {spacing_half}px {spacing}px;
    spacing: {spacing}px;
}}

QToolBar::separator {{
    background-color: {tokens.border_subtle};
    width: 1px;
    margin: {spacing_half}px {spacing}px;
}}

QStatusBar {{
    background-color: {tokens.background_elevated};
    color: {tokens.text_secondary};
    border-top: 1px solid {tokens.border_subtle};
}}

QStatusBar QLabel {{
    color: {tokens.text_secondary};
    padding: 0px {spacing}px;
}}

QMenuBar {{
    background-color: {tokens.background_elevated};
    border-bottom: 1px solid {tokens.border_subtle};
}}

QMenuBar::item {{
    background: transparent;
    padding: {spacing_half}px {spacing}px;
}}

QMenuBar::item:selected {{
    background-color: {tokens.surface_subtle};
    color: {tokens.text_primary};
}}

QMenu {{
    background-color: {tokens.background_elevated};
    border: 1px solid {tokens.border_subtle};
    padding: {spacing_half}px;
}}

QMenu::item {{
    padding: {spacing_half}px {spacing_double}px;
    border-radius: {tokens.radius_small_px}px;
}}

QMenu::item:selected {{
    background-color: {tokens.accent};
    color: {tokens.text_on_accent};
}}

QDockWidget {{
    color: {tokens.text_secondary};
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}}

QDockWidget::title {{
    background-color: {tokens.background_elevated};
    border-bottom: 1px solid {tokens.border_subtle};
    padding: {spacing_half}px {spacing}px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: {base_pt}pt;
    font-weight: 600;
    color: {tokens.text_secondary};
}}

QSplitter::handle {{
    background-color: {tokens.border_subtle};
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}

QPushButton {{
    background-color: {tokens.surface_subtle};
    color: {tokens.text_primary};
    border: 1px solid {tokens.border_subtle};
    border-radius: {tokens.radius_medium_px}px;
    padding: {spacing_half}px {spacing_double}px;
}}

QPushButton:hover {{
    background-color: {tokens.surface_strong};
    border-color: {tokens.border_strong};
}}

QPushButton:pressed {{
    background-color: {tokens.accent_pressed};
    color: {tokens.text_on_accent};
}}

QPushButton:default {{
    background-color: {tokens.accent};
    color: {tokens.text_on_accent};
    border-color: {tokens.accent};
}}

QPushButton:default:hover {{
    background-color: {tokens.accent_hover};
}}

QLineEdit, QPlainTextEdit, QTextEdit, QComboBox, QSpinBox {{
    background-color: {tokens.background_elevated};
    border: 1px solid {tokens.border_subtle};
    border-radius: {tokens.radius_medium_px}px;
    padding: {spacing_half}px {spacing}px;
    selection-background-color: {tokens.selection_background};
    selection-color: {tokens.selection_foreground};
}}

QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border-color: {tokens.border_focus};
}}

QPlainTextEdit, QTextEdit {{
    font-family: {mono_family};
    font-size: {mono_pt}pt;
}}

QComboBox::drop-down {{
    border: none;
    width: {spacing_double}px;
}}

QComboBox QAbstractItemView {{
    background-color: {tokens.background_elevated};
    border: 1px solid {tokens.border_subtle};
    selection-background-color: {tokens.accent};
    selection-color: {tokens.text_on_accent};
}}

QTabWidget::pane {{
    border: 1px solid {tokens.border_subtle};
    background-color: {tokens.background_base};
}}

QTabBar::tab {{
    background-color: {tokens.background_elevated};
    color: {tokens.text_secondary};
    padding: {spacing_half}px {spacing_double}px;
    border: 1px solid transparent;
    border-bottom: none;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {tokens.background_base};
    color: {tokens.text_primary};
    border-color: {tokens.border_subtle};
    border-bottom: 2px solid {tokens.accent};
}}

QTabBar::tab:hover:!selected {{
    background-color: {tokens.surface_subtle};
}}

QTreeView, QTreeWidget, QListView, QListWidget, QTableView, QTableWidget {{
    background-color: {tokens.background_base};
    alternate-background-color: {tokens.background_elevated};
    border: 1px solid {tokens.border_subtle};
    selection-background-color: {tokens.accent};
    selection-color: {tokens.text_on_accent};
    gridline-color: {tokens.border_subtle};
}}

QHeaderView::section {{
    background-color: {tokens.background_elevated};
    color: {tokens.text_secondary};
    padding: {spacing_half}px {spacing}px;
    border: none;
    border-right: 1px solid {tokens.border_subtle};
    border-bottom: 1px solid {tokens.border_subtle};
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 1px;
}}

QScrollBar:vertical {{
    background-color: {tokens.scrollbar_track};
    width: 10px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {tokens.scrollbar_thumb};
    border-radius: {tokens.radius_small_px}px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {tokens.scrollbar_thumb_hover};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {tokens.scrollbar_track};
    height: 10px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {tokens.scrollbar_thumb};
    border-radius: {tokens.radius_small_px}px;
    min-width: 24px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {tokens.scrollbar_thumb_hover};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QToolTip {{
    background-color: {tokens.background_overlay};
    color: {tokens.text_primary};
    border: 1px solid {tokens.border_strong};
    padding: {spacing_half}px {spacing}px;
}}

QGroupBox {{
    border: 1px solid {tokens.border_subtle};
    border-radius: {tokens.radius_medium_px}px;
    margin-top: {spacing_double}px;
    padding-top: {spacing_double}px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: {spacing}px;
    padding: 0 {spacing_half}px;
    color: {tokens.text_secondary};
    text-transform: uppercase;
    letter-spacing: 1px;
}}

QLabel#TitleLabel {{
    font-size: {title_pt}pt;
    font-weight: 700;
    color: {tokens.text_primary};
}}

QLabel#SubtitleLabel {{
    color: {tokens.text_secondary};
}}

QLabel#AccentLabel {{
    color: {tokens.accent};
    font-weight: 600;
}}

QLabel#DangerLabel {{
    color: {tokens.danger};
}}

QLabel#SuccessLabel {{
    color: {tokens.success};
}}

QLabel#WarningLabel {{
    color: {tokens.warning};
}}

QLabel#InfoLabel {{
    color: {tokens.info};
}}

QFrame#SectionDivider {{
    background-color: {tokens.border_subtle};
    max-height: 1px;
    border: none;
}}

QPlainTextEdit#TerminalView {{
    background-color: {tokens.background_terminal};
    color: {tokens.text_primary};
    font-family: {mono_family};
    font-size: {mono_pt}pt;
    border: 1px solid {tokens.border_subtle};
    selection-background-color: {tokens.selection_background};
    selection-color: {tokens.selection_foreground};
}}

QListView#CommandPaletteResults {{
    background-color: {tokens.background_overlay};
    border: 1px solid {tokens.border_strong};
    border-radius: {tokens.radius_medium_px}px;
}}

QListView#CommandPaletteResults::item {{
    padding: {spacing}px {spacing_double}px;
}}

QListView#CommandPaletteResults::item:selected {{
    background-color: {tokens.accent};
    color: {tokens.text_on_accent};
}}

QLineEdit#CommandPaletteInput {{
    background-color: {tokens.background_overlay};
    border: 1px solid {tokens.border_strong};
    border-radius: {tokens.radius_medium_px}px;
    padding: {spacing}px {spacing_double}px;
    font-size: {title_pt}pt;
}}
"""
