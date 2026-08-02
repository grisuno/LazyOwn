"""CVE tracker panel for the operator console.

Displays known CVEs from the knowledge base with severity filtering and
search. Supports lookup and exploitation suggestions.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QComboBox,
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


class CVEPanel(PanelBase):
    """Dock panel listing CVEs from the knowledge base."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Build the CVE list UI with severity filter."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier="panel.cve",
            title="CVEs",
            parent=parent,
        )
        self._cve_data: list[dict[str, str]] = []
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header = QHBoxLayout()
        title_label = QLabel("CVE Tracker", container)
        title_label.setObjectName("SubtitleLabel")
        header.addWidget(title_label)
        header.addStretch()
        refresh_btn = QPushButton("Refresh", container)
        refresh_btn.clicked.connect(self._refresh)
        header.addWidget(refresh_btn)
        layout.addLayout(header)

        filter_row = QHBoxLayout()
        self._filter_input = QLineEdit(container)
        self._filter_input.setPlaceholderText("Search CVE ID or description...")
        self._filter_input.textChanged.connect(self._populate_tree)
        filter_row.addWidget(self._filter_input)

        self._severity_combo = QComboBox(container)
        self._severity_combo.addItems(["All", "Critical", "High", "Medium", "Low"])
        self._severity_combo.currentTextChanged.connect(self._populate_tree)
        filter_row.addWidget(self._severity_combo)
        layout.addLayout(filter_row)

        self._tree = QTreeWidget(container)
        self._tree.setColumnCount(4)
        self._tree.setHeaderLabels(["CVE ID", "Severity", "Score", "Description"])
        self._tree.setRootIsDecorated(False)
        self._tree.setAlternatingRowColors(True)
        self._tree.setUniformRowHeights(True)
        self._tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self._tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._tree.header().setStretchLastSection(True)
        layout.addWidget(self._tree)

        actions = QHBoxLayout()
        lookup_btn = QPushButton("Lookup", container)
        lookup_btn.clicked.connect(self._request_lookup)
        actions.addWidget(lookup_btn)
        search_btn = QPushButton("Search Exploits", container)
        search_btn.clicked.connect(self._request_search_exploits)
        actions.addWidget(search_btn)
        actions.addStretch()
        layout.addLayout(actions)

        self.setWidget(container)

        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(constants.timing.panel_refresh_interval_ms)
        self._refresh_timer.timeout.connect(self._refresh)
        self._refresh_timer.start()
        self._refresh()

    def _refresh(self) -> None:
        try:
            from pathlib import Path
            import json

            cve_files = (
                Path("knowledge_base_vuln.json"),
                Path("parquets") / "cve_kb.parquet",
            )
            cves: list[dict[str, str]] = []
            for cve_file in cve_files:
                if not cve_file.exists():
                    continue
                if cve_file.suffix == ".json":
                    data = json.loads(cve_file.read_text(encoding="utf-8", errors="ignore"))
                    if isinstance(data, list):
                        for item in data[:200]:
                            if isinstance(item, dict):
                                cves.append({
                                    "cve": str(item.get("cve", item.get("id", ""))),
                                    "severity": str(item.get("severity", item.get("cvss_severity", "Unknown"))),
                                    "score": str(item.get("cvss", item.get("score", ""))),
                                    "description": str(item.get("description", "")),
                                })
                elif cve_file.suffix == ".parquet":
                    try:
                        import pandas as pd
                        df = pd.read_parquet(cve_file)
                        for _, row in df.head(200).iterrows():
                            cves.append({
                                "cve": str(row.get("cve", row.get("CVE", ""))),
                                "severity": str(row.get("severity", "Unknown")),
                                "score": str(row.get("cvss", row.get("score", ""))),
                                "description": str(row.get("description", "")),
                            })
                    except Exception:
                        pass
                self._cve_data = cves
                self._populate_tree()
                return
        except Exception:
            pass

    def _populate_tree(self) -> None:
        self._tree.clear()
        filter_text = self._filter_input.text().lower().strip()
        severity_filter = self._severity_combo.currentText().lower()
        for cve in self._cve_data:
            if filter_text:
                haystack = f"{cve.get('cve','')} {cve.get('description','')}".lower()
                if filter_text not in haystack:
                    continue
            if severity_filter != "all":
                cve_sev = cve.get("severity", "").lower()
                if severity_filter not in cve_sev and cve_sev != severity_filter:
                    continue
            QTreeWidgetItem(self._tree, [cve["cve"], cve["severity"], cve["score"], cve["description"]])

    def _request_lookup(self) -> None:
        items = self._tree.selectedItems()
        if items:
            cve_id = items[0].text(0)
            self._backend.send_command(f"cve lookup {cve_id}", target_session=None)

    def _request_search_exploits(self) -> None:
        items = self._tree.selectedItems()
        if items:
            cve_id = items[0].text(0)
            self._backend.send_command(f"searchsploit {cve_id}", target_session=None)

    @property
    def cve_count(self) -> int:
        """Return the number of loaded CVEs."""
        return len(self._cve_data)
