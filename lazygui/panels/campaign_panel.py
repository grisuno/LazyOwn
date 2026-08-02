"""Campaign management panel for the operator console.

Displays active campaigns, objectives and playbook execution status from
the teamserver. Supports filtering and detail view.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend
from lazygui.services.models import CampaignSummary


class CampaignPanel(PanelBase):
    """Dock panel displaying active campaign status."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Build the campaign list UI."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier="panel.campaign",
            title="Campaigns",
            parent=parent,
        )
        self._campaigns: tuple[CampaignSummary, ...] = ()
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header = QHBoxLayout()
        title_label = QLabel("Active Campaigns", container)
        title_label.setObjectName("SubtitleLabel")
        header.addWidget(title_label)
        header.addStretch()
        new_btn = QPushButton("New", container)
        new_btn.clicked.connect(self._request_new_campaign)
        header.addWidget(new_btn)
        refresh_btn = QPushButton("Refresh", container)
        refresh_btn.clicked.connect(self._refresh)
        header.addWidget(refresh_btn)
        layout.addLayout(header)

        self._filter_input = QLineEdit(container)
        self._filter_input.setPlaceholderText("Filter campaigns...")
        self._filter_input.textChanged.connect(self._populate_tree)
        layout.addWidget(self._filter_input)

        self._tree = QTreeWidget(container)
        self._tree.setColumnCount(5)
        self._tree.setHeaderLabels(["Name", "Status", "Playbook", "Objectives", "Targets"])
        self._tree.setRootIsDecorated(False)
        self._tree.setAlternatingRowColors(True)
        self._tree.setUniformRowHeights(True)
        self._tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self._tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._tree.header().setStretchLastSection(True)
        layout.addWidget(self._tree)

        actions = QHBoxLayout()
        view_btn = QPushButton("View", container)
        view_btn.clicked.connect(self._request_view_campaign)
        actions.addWidget(view_btn)
        run_btn = QPushButton("Run Playbook", container)
        run_btn.clicked.connect(self._request_run_playbook)
        actions.addWidget(run_btn)
        actions.addStretch()
        layout.addLayout(actions)

        self.setWidget(container)

        backend.campaign_changed.connect(self._on_campaigns_changed)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(constants.timing.panel_refresh_interval_ms)
        self._refresh_timer.timeout.connect(self._refresh)
        self._refresh_timer.start()
        self._refresh()

    def _refresh(self) -> None:
        self._backend.send_command("campaign list", target_session=None)

    def _on_campaigns_changed(self, campaigns: list) -> None:
        self._campaigns = tuple(campaigns) if campaigns else ()
        self._populate_tree()

    def _populate_tree(self) -> None:
        self._tree.clear()
        filter_text = self._filter_input.text().lower().strip()
        for campaign in self._campaigns:
            if filter_text:
                haystack = f"{campaign.name} {campaign.status} {campaign.playbook}".lower()
                if filter_text not in haystack:
                    continue
            objectives = f"{campaign.objectives_completed}/{campaign.objectives_total}"
            QTreeWidgetItem(
                self._tree,
                [campaign.name, campaign.status, campaign.playbook, objectives, str(campaign.target_count)],
            )

    def _request_new_campaign(self) -> None:
        self._backend.send_command("campaign new", target_session=None)

    def _request_view_campaign(self) -> None:
        self._backend.send_command("campaign show", target_session=None)

    def _request_run_playbook(self) -> None:
        items = self._tree.selectedItems()
        if items:
            name = items[0].text(0)
            self._backend.send_command(f"playbook run {name}", target_session=None)

    @property
    def campaign_count(self) -> int:
        """Return the number of active campaigns."""
        return len(self._campaigns)
