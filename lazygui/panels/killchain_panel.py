"""Kill-chain visualization panel for the operator console.

Displays the current engagement phase and completed phases as a
horizontal progress bar. Reads from ``modules.killchain.KillChain``
as the single source of truth.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend


def _get_phases():
    """Import the unified killchain phase definitions lazily."""
    from modules.killchain import KillChain as _KC
    return _KC.phases_for_display()


_PHASES = _get_phases()
_PHASE_NAMES: dict[str, str] = {ph[0]: ph[1] for ph in _PHASES}
_PHASE_ORDER: tuple[str, ...] = tuple(ph[0] for ph in _PHASES)


class KillChainPanel(PanelBase):
    """Dock widget displaying the engagement kill-chain progress."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            constants=constants,
            backend=backend,
            identifier=constants.panel.killchain_panel_id,
            title="Kill-Chain",
            parent=parent,
        )
        self._phase_widgets: dict[str, QLabel] = {}
        self._completed: set[str] = set()
        self._current: str = "recon"
        self._build_ui()
        backend.sessions_changed.connect(self._refresh)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(constants.timing.panel_refresh_interval_ms)
        self._refresh_timer.timeout.connect(self._refresh)
        self._refresh_timer.start()
        self._refresh()

    def _build_ui(self) -> None:
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        title = QLabel("Engagement Kill-Chain", container)
        title.setObjectName("SubtitleLabel")
        layout.addWidget(title)

        self._bar = QWidget(container)
        bar_layout = QHBoxLayout(self._bar)
        bar_layout.setContentsMargins(4, 4, 4, 4)
        bar_layout.setSpacing(6)

        for ph_id, ph_name, ph_color in _PHASES:
            phase_widget = QLabel(self._bar)
            phase_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            phase_widget.setMinimumWidth(60)
            phase_widget.setFixedHeight(52)
            phase_widget.setStyleSheet(
                "border: 1px solid #30363d; border-radius: 6px; padding: 6px; font-size: 10px;"
            )
            bar_layout.addWidget(phase_widget)
            self._phase_widgets[ph_id] = phase_widget

        bar_layout.addStretch()
        layout.addWidget(self._bar)

        self._detail_label = QLabel("", container)
        self._detail_label.setObjectName("CaptionLabel")
        self._detail_label.setWordWrap(True)
        layout.addWidget(self._detail_label)
        layout.addStretch()
        self.setWidget(container)

    def _refresh(self) -> None:
        """Pull the kill-chain snapshot and drive visuals exclusively from it.

        The single source of truth is the unified ``KillChain.snapshot``
        (served by the backend over HTTP for the teamserver backend); the
        panel never derives phases locally so it cannot diverge.
        """
        try:
            snapshot = self._backend.request_world_model()
        except Exception:
            snapshot = {}
        if not isinstance(snapshot, dict):
            snapshot = {}

        progress = snapshot.get("progress") or []
        current = str(snapshot.get("current_phase", "") or "")
        completed = set()
        for p in (snapshot.get("completed_phases") or []):
            completed.add(str(p).strip().lower())
        for item in progress:
            if isinstance(item, dict):
                status = str(item.get("status", "")).lower()
                key = str(item.get("key", "")).strip().lower()
                if status == "active":
                    current = key
                elif status == "done":
                    completed.add(key)
        if current:
            self._current = current
        self._completed = completed
        self._apply_visuals()

    def _apply_visuals(self) -> None:
        for ph_id, widget in self._phase_widgets.items():
            label = _PHASE_NAMES.get(ph_id, ph_id)
            if ph_id in self._completed:
                color = "#3fb950"
                text = f"{label}\nDONE"
            elif ph_id == self._current:
                color = "#58a6ff"
                text = f"{label}\nACTIVE"
            else:
                color = "#484f58"
                text = f"{label}\n..."
            widget.setText(text)
            widget.setStyleSheet(
                f"border: 1px solid {color}; border-radius: 6px; padding: 6px; font-size: 10px; color: {color};"
            )
        self._detail_label.setText(f"Completed: {', '.join(sorted(self._completed)) or 'none'}")
