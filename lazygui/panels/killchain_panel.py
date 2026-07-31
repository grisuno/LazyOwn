"""Kill-chain visualization panel for the operator console.

Displays the current engagement phase and completed phases as a
horizontal progress bar rendered via QLabels with colour coding,
making it easy for the operator to see at a glance where they are
in the kill chain.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend

_PHASES = [
    ("recon", "Recon", "#a371f7"),
    ("scan", "Scan", "#58a6ff"),
    ("enum", "Enum", "#56d364"),
    ("exploit", "Exploit", "#f85149"),
    ("privesc", "PrivEsc", "#d2991d"),
    ("lateral", "Lateral", "#db61a2"),
    ("exfil", "Exfil", "#7c3aed"),
    ("report", "Report", "#3fb950"),
]

_PHASE_NAMES: dict[str, str] = {ph[0]: ph[1] for ph in _PHASES}


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
        self._build_ui()
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

        scroll = QScrollArea(container)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFixedHeight(80)

        bar = QWidget(scroll)
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(4, 4, 4, 4)
        bar_layout.setSpacing(6)

        for ph_id, ph_name, ph_color in _PHASES:
            phase_widget = QLabel(bar)
            phase_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            phase_widget.setMinimumWidth(60)
            phase_widget.setFixedHeight(52)
            phase_widget.setStyleSheet(
                f"border: 1px solid #30363d; border-radius: 6px; padding: 6px; font-size: 10px;"
            )
            bar_layout.addWidget(phase_widget)
            self._phase_widgets[ph_id] = phase_widget

        bar_layout.addStretch()
        scroll.setWidget(bar)
        layout.addWidget(scroll)

        self._detail_label = QLabel("", container)
        self._detail_label.setObjectName("CaptionLabel")
        self._detail_label.setWordWrap(True)
        layout.addWidget(self._detail_label)
        layout.addStretch()
        self.setWidget(container)

    def _refresh(self) -> None:
        try:
            world = self._backend.request_world_model()
        except Exception:
            world = {}
        current = world.get("current_phase", world.get("phase", "recon"))
        completed = set(world.get("completed_phases", []))
        for ph_id, widget in self._phase_widgets.items():
            label = _PHASE_NAMES.get(ph_id, ph_id)
            if ph_id in completed:
                color = "#3fb950"
                text = f"{label}\nDONE"
            elif ph_id == current:
                color = "#58a6ff"
                text = f"{label}\nACTIVE"
            else:
                color = "#484f58"
                text = f"{label}\n..."
            widget.setText(text)
            widget.setStyleSheet(
                f"border: 1px solid {color}; border-radius: 6px; padding: 6px; font-size: 10px; color: {color};"
            )
        self._detail_label.setText(f"Current phase: {current.upper()}")


__all__ = ["KillChainPanel"]
