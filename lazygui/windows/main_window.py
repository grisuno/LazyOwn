"""Operator console main window.

Composes panels, menus, toolbar, status bar and shortcuts. Owns no
business logic of its own — every interaction either mutates the active
:class:`Backend` (issuing a command, refreshing) or the persisted
:class:`AppSettings` (theme, layout).
"""

from __future__ import annotations

from typing import Iterable

from PySide6.QtCore import QByteArray, QSize, Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.config.settings import AppSettings
from lazygui.panels.registry import PanelRegistry
from lazygui.services.backend import Backend
from lazygui.services.event_log import EventLog
from lazygui.services.models import EventLevel, EventRecord, Operator
from lazygui.theme.manager import ThemeManager
from lazygui.theme.tokens import ThemeTokens
from lazygui.widgets.command_palette_list import CommandPaletteAction
from lazygui.widgets.status_badge import StatusBadge
from lazygui.windows.command_palette_window import CommandPaletteWindow


class MainWindow(QMainWindow):
    """Top-level operator window."""

    def __init__(
        self,
        constants: AppConstants,
        settings: AppSettings,
        theme_manager: ThemeManager,
        backend: Backend,
        event_log: EventLog,
        parent: QWidget | None = None,
    ) -> None:
        """Wire the dependencies and build the full layout."""
        super().__init__(parent)
        self._constants = constants
        self._settings = settings
        self._theme_manager = theme_manager
        self._backend = backend
        self._event_log = event_log
        self.setWindowTitle(constants.ids.application_name)
        self.resize(constants.window.main_default_width, constants.window.main_default_height)
        self.setMinimumSize(QSize(constants.window.main_min_width, constants.window.main_min_height))
        self.setDockOptions(
            QMainWindow.DockOption.AllowNestedDocks
            | QMainWindow.DockOption.AllowTabbedDocks
            | QMainWindow.DockOption.AnimatedDocks
        )

        self._panels = PanelRegistry.build(
            constants=constants,
            backend=backend,
            event_log=event_log,
            parent=self,
        )
        self._install_panels()
        self._install_menu_bar()
        self._install_toolbar()
        self._install_statusbar()
        self._install_shortcuts()
        self._command_palette = CommandPaletteWindow(
            constants=constants,
            actions=self._build_palette_actions(),
            parent=self,
        )

        backend.status_changed.connect(self._status_badge.set_status)
        backend.operator_changed.connect(self._on_operator_changed)
        backend.event_logged.connect(self._on_event_logged)
        theme_manager.theme_changed.connect(self._on_theme_changed)

        self._restore_geometry_and_state()
        self._status_badge.set_status(backend.status)
        self._on_theme_changed(theme_manager.active_tokens)

    # --- Lifecycle --------------------------------------------------------

    def closeEvent(self, event) -> None:
        """Persist geometry, layout and theme before closing."""
        self._persist_geometry_and_state()
        try:
            self._backend.stop()
        except Exception:
            pass
        super().closeEvent(event)

    # --- Layout setup -----------------------------------------------------

    def _install_panels(self) -> None:
        """Place dock widgets in their default positions."""
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._panels.sessions)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._panels.listeners)
        self.tabifyDockWidget(self._panels.sessions, self._panels.listeners)
        self._panels.sessions.raise_()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._panels.terminal)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._panels.event_log_panel)

    def _install_menu_bar(self) -> None:
        """Build a minimal File / View / Theme menu bar."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        connect_action = QAction("&Connect...", self)
        connect_action.setShortcut(QKeySequence(self._constants.keys.open_connect_dialog))
        connect_action.triggered.connect(self._emit_request_connect)
        file_menu.addAction(connect_action)
        file_menu.addSeparator()
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence(self._constants.keys.quit_application))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        view_menu = menu_bar.addMenu("&View")
        for panel in self._panels:
            toggle = panel.toggleViewAction()
            view_menu.addAction(toggle)
        view_menu.addSeparator()
        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut(QKeySequence(self._constants.keys.refresh_data))
        refresh_action.triggered.connect(self._backend.refresh)
        view_menu.addAction(refresh_action)

        theme_menu = menu_bar.addMenu("&Theme")
        for tokens in self._theme_manager.available():
            action = QAction(tokens.display_name, self)
            action.setData(tokens.identifier)
            action.triggered.connect(self._on_theme_menu_action)
            theme_menu.addAction(action)
        theme_menu.addSeparator()
        cycle_action = QAction("Cycle theme", self)
        cycle_action.setShortcut(QKeySequence(self._constants.keys.cycle_theme))
        cycle_action.triggered.connect(self._theme_manager.cycle)
        theme_menu.addAction(cycle_action)

    def _install_toolbar(self) -> None:
        """Build a single toolbar with the most common actions."""
        toolbar = QToolBar("Main", self)
        toolbar.setObjectName("MainToolbar")
        toolbar.setMovable(False)
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self._backend.refresh)
        toolbar.addAction(refresh_action)
        connect_action = QAction("Connect...", self)
        connect_action.triggered.connect(self._emit_request_connect)
        toolbar.addAction(connect_action)
        toolbar.addSeparator()
        palette_action = QAction("Command palette", self)
        palette_action.triggered.connect(self._show_command_palette)
        toolbar.addAction(palette_action)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def _install_statusbar(self) -> None:
        """Build a status bar with backend badge, operator label and clock."""
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        self._status_badge = StatusBadge(status_bar)
        self._operator_label = QLabel("operator: -", status_bar)
        self._operator_label.setObjectName("SubtitleLabel")
        self._theme_label = QLabel("theme: -", status_bar)
        self._theme_label.setObjectName("AccentLabel")
        self._clock_label = QLabel("--:--:--", status_bar)
        status_bar.addWidget(self._status_badge)
        status_bar.addWidget(self._operator_label, stretch=1)
        status_bar.addPermanentWidget(self._theme_label)
        status_bar.addPermanentWidget(self._clock_label)
        self._clock_timer = QTimer(self)
        self._clock_timer.setInterval(self._constants.timing.statusbar_clock_interval_ms)
        self._clock_timer.timeout.connect(self._tick_clock)
        self._clock_timer.start()
        self._tick_clock()

    def _install_shortcuts(self) -> None:
        """Bind global shortcuts not already attached to menu actions."""
        palette_action = QAction(self)
        palette_action.setShortcut(QKeySequence(self._constants.keys.command_palette))
        palette_action.triggered.connect(self._show_command_palette)
        self.addAction(palette_action)

        terminal_focus_action = QAction(self)
        terminal_focus_action.setShortcut(QKeySequence(self._constants.keys.toggle_terminal_focus))
        terminal_focus_action.triggered.connect(self._panels.terminal.focus_terminal)
        self.addAction(terminal_focus_action)

        for shortcut, panel in (
            (self._constants.keys.toggle_sessions_panel, self._panels.sessions),
            (self._constants.keys.toggle_listeners_panel, self._panels.listeners),
            (self._constants.keys.toggle_event_log_panel, self._panels.event_log_panel),
        ):
            action = QAction(self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(self._make_panel_toggle(panel))
            self.addAction(action)

    # --- Persistence ------------------------------------------------------

    def _persist_geometry_and_state(self) -> None:
        """Encode current geometry/layout into settings."""
        geometry_value = bytes(self.saveGeometry().toBase64()).decode("ascii")
        state_value = bytes(self.saveState().toBase64()).decode("ascii")
        self._settings.set(self._constants.ids.geometry_setting_key, geometry_value)
        self._settings.set(self._constants.ids.state_setting_key, state_value)
        self._settings.save()

    def _restore_geometry_and_state(self) -> None:
        """Restore geometry/layout from settings, ignoring corrupt blobs."""
        geometry = self._settings.get(self._constants.ids.geometry_setting_key)
        state = self._settings.get(self._constants.ids.state_setting_key)
        if isinstance(geometry, str) and geometry:
            self.restoreGeometry(QByteArray.fromBase64(geometry.encode("ascii")))
        if isinstance(state, str) and state:
            self.restoreState(QByteArray.fromBase64(state.encode("ascii")))

    # --- Slot helpers -----------------------------------------------------

    def _build_palette_actions(self) -> Iterable[CommandPaletteAction]:
        """Build the palette catalog from menu and panel toggles."""
        actions: list[CommandPaletteAction] = []
        actions.append(
            CommandPaletteAction(
                identifier="refresh",
                title="Refresh data",
                subtitle="Pull the latest state from the active backend",
                invoke=self._backend.refresh,
            )
        )
        actions.append(
            CommandPaletteAction(
                identifier="cycle_theme",
                title="Cycle theme",
                subtitle="Switch to the next palette",
                invoke=self._theme_manager.cycle,
            )
        )
        for panel in self._panels:
            actions.append(
                CommandPaletteAction(
                    identifier=f"toggle.{panel.identifier}",
                    title=f"Toggle {panel.windowTitle()}",
                    subtitle="Show or hide the dock panel",
                    invoke=self._make_panel_toggle(panel),
                )
            )
        for tokens in self._theme_manager.available():
            actions.append(
                CommandPaletteAction(
                    identifier=f"theme.{tokens.identifier}",
                    title=f"Theme: {tokens.display_name}",
                    subtitle="Apply this colour palette",
                    invoke=self._make_theme_apply(tokens.identifier),
                )
            )
        return tuple(actions)

    def _make_panel_toggle(self, panel) -> callable:
        """Closure that toggles the visibility of ``panel``."""

        def _toggle() -> None:
            panel.setVisible(not panel.isVisible())
            if panel.isVisible():
                panel.raise_()
                panel.setFocus()

        return _toggle

    def _make_theme_apply(self, identifier: str) -> callable:
        """Closure that applies the theme with ``identifier``."""

        def _apply() -> None:
            self._theme_manager.apply(identifier)

        return _apply

    def _on_operator_changed(self, operator: Operator) -> None:
        """Refresh the status-bar operator label."""
        if operator.karma_name:
            self._operator_label.setText(f"operator: {operator.name} ({operator.karma_name})")
        else:
            self._operator_label.setText(f"operator: {operator.name}")

    def _on_event_logged(self, _record: EventRecord) -> None:
        """Surface the most recent event as a transient status bar message."""

    def _on_theme_changed(self, tokens: ThemeTokens) -> None:
        """Update the theme label when a new palette is applied."""
        self._theme_label.setText(f"theme: {tokens.display_name}")

    def _on_theme_menu_action(self) -> None:
        """Apply the theme stored in the triggering action's data field."""
        sender = self.sender()
        if isinstance(sender, QAction):
            identifier = sender.data()
            if isinstance(identifier, str):
                self._theme_manager.apply(identifier)

    def _show_command_palette(self) -> None:
        """Show and centre the command palette."""
        geometry = self.frameGeometry()
        self._command_palette.set_actions(self._build_palette_actions())
        target_x = geometry.center().x() - self._command_palette.width() // 2
        target_y = geometry.top() + geometry.height() // 6
        self._command_palette.move(target_x, target_y)
        self._command_palette.show()
        self._command_palette.raise_()
        self._command_palette.activateWindow()

    def _emit_request_connect(self) -> None:
        """Surface a request to open the connect dialog (handled by Application)."""
        self.window_requests_connect()

    def window_requests_connect(self) -> None:
        """Hook overridden by :class:`Application` to swap backend at runtime."""
        self._event_log.append(
            EventRecord.now(
                level=EventLevel.INFO,
                source="ui",
                message="Connect dialog requested but no handler is wired.",
            )
        )

    def _tick_clock(self) -> None:
        """Update the clock label once per ``statusbar_clock_interval_ms``."""
        from datetime import datetime

        self._clock_label.setText(datetime.now().strftime("%H:%M:%S"))

    @property
    def status_badge(self) -> StatusBadge:
        """Expose the badge so the application can update it on backend swaps."""
        return self._status_badge

    @property
    def panels(self) -> PanelRegistry:
        """Expose the panel registry for backend swaps."""
        return self._panels
