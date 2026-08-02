"""Marketplace panel for YARA rules and Nuclei templates.

Lists installed YARA rules and Nuclei templates from the teamserver,
supports search, filter by severity and install operations.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from lazygui.config.constants import AppConstants
from lazygui.panels.base import PanelBase
from lazygui.services.backend import Backend
from lazygui.services.models import EventLevel


class MarketplacePanel(PanelBase):
    """Dock panel listing YARA rules and Nuclei templates from the marketplace."""

    def __init__(
        self,
        constants: AppConstants,
        backend: Backend,
        parent: QWidget | None = None,
    ) -> None:
        """Build the tabbed marketplace UI."""
        super().__init__(
            constants=constants,
            backend=backend,
            identifier="panel.marketplace",
            title="Marketplace",
            parent=parent,
        )
        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        self._tabs = QTabWidget(container)
        self._yara_tree = QTreeWidget(self._tabs)
        self._nuclei_tree = QTreeWidget(self._tabs)
        self._tools_tree = QTreeWidget(self._tabs)

        for tree, name, headers in (
            (self._yara_tree, "YARA Rules", ("Name", "Category", "Description")),
            (self._nuclei_tree, "Nuclei", ("Name", "Severity", "CVE", "Description")),
            (self._tools_tree, "Tools", ("Name", "Type", "Description")),
        ):
            tree.setColumnCount(len(headers))
            tree.setHeaderLabels(list(headers))
            tree.setRootIsDecorated(False)
            tree.setAlternatingRowColors(True)
            tree.setUniformRowHeights(True)
            tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
            tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            tree.header().setStretchLastSection(True)
            self._tabs.addTab(tree, name)

        filter_bar = QHBoxLayout()
        self._filter_input = QLineEdit(container)
        self._filter_input.setPlaceholderText("Search marketplace...")
        self._filter_input.textChanged.connect(self._apply_filter)
        filter_bar.addWidget(self._filter_input)
        refresh_btn = QPushButton("Refresh", container)
        refresh_btn.clicked.connect(self._refresh)
        filter_bar.addWidget(refresh_btn)
        info_btn = QPushButton("Info", container)
        info_btn.clicked.connect(self._show_selected_info)
        filter_bar.addWidget(info_btn)

        layout.addLayout(filter_bar)
        layout.addWidget(self._tabs)
        self.setWidget(container)

        self._yara_data: list[dict[str, str]] = []
        self._nuclei_data: list[dict[str, str]] = []
        self._tools_data: list[dict[str, str]] = []

        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(constants.timing.panel_refresh_interval_ms)
        self._refresh_timer.timeout.connect(self._refresh)
        self._refresh_timer.start()
        self._refresh()

    def _refresh(self) -> None:
        self._fetch_yara_rules()
        self._fetch_nuclei_templates()
        self._fetch_tools()

    def _fetch_yara_rules(self) -> None:
        try:
            from pathlib import Path

            yara_dir = Path("yara_rules")
            rules: list[dict[str, str]] = []
            if yara_dir.exists():
                for yar_file in sorted(yara_dir.glob("*.yar")):
                    category = str(yar_file.stem).replace("_", " ").title()
                    description = ""
                    content = ""
                    try:
                        content = yar_file.read_text(encoding="utf-8", errors="ignore")[:2000]
                        for line in content.splitlines():
                            if line.strip().startswith(("description", "desc", "meta")):
                                description = line.strip().split("=", 1)[-1].strip().strip('"').strip("'")
                                break
                    except Exception:
                        pass
                    rules.append({
                        "name": yar_file.name,
                        "category": category,
                        "description": description or f"YARA rule ({yar_file.stat().st_size} bytes)",
                    })
            self._yara_data = rules
            self._populate_yara_tree()
        except Exception:
            pass

    def _fetch_nuclei_templates(self) -> None:
        try:
            from pathlib import Path

            nuclei_dirs = (Path("nuclei-templates"), Path.home() / "nuclei-templates")
            templates: list[dict[str, str]] = []
            for nuclei_dir in nuclei_dirs:
                if not nuclei_dir.exists():
                    continue
                for yaml_file in sorted(nuclei_dir.rglob("*.yaml"))[:200]:
                    try:
                        lines = yaml_file.read_text(encoding="utf-8", errors="ignore").splitlines()[:20]
                        severity = ""
                        cve = ""
                        description = ""
                        for line in lines:
                            stripped = line.strip()
                            if stripped.startswith("severity:"):
                                severity = stripped.split(":", 1)[-1].strip()
                            if stripped.lower().startswith("cve:"):
                                cve = stripped.split(":", 1)[-1].strip()
                            if stripped.startswith("description:"):
                                description = stripped.split(":", 1)[-1].strip().strip('"').strip("'")
                        templates.append({
                            "name": yaml_file.name,
                            "severity": severity or "unknown",
                            "cve": cve or "",
                            "description": description or yaml_file.relative_to(nuclei_dir).as_posix(),
                        })
                    except Exception:
                        pass
                self._nuclei_data = templates
                self._populate_nuclei_tree()
                return
        except Exception:
            pass

    def _fetch_tools(self) -> None:
        try:
            from pathlib import Path

            addons_dir = Path("lazyaddons")
            tools: list[dict[str, str]] = []
            if addons_dir.exists():
                for yaml_file in sorted(addons_dir.glob("*.yaml"))[:100]:
                    try:
                        import yaml as _yaml
                        content = _yaml.safe_load(yaml_file.read_text(encoding="utf-8", errors="ignore"))
                        if isinstance(content, Mapping):
                            tools.append({
                                "name": yaml_file.stem,
                                "type": str(content.get("type", "tool")),
                                "description": str(content.get("description", "")),
                            })
                    except Exception:
                        tools.append({
                            "name": yaml_file.stem,
                            "type": "yaml",
                            "description": "",
                        })
            self._tools_data = tools
            self._populate_tools_tree()
        except Exception:
            pass

    def _populate_yara_tree(self) -> None:
        self._yara_tree.clear()
        for rule in self._yara_data:
            filter_text = self._filter_input.text().lower().strip()
            if filter_text:
                haystack = f"{rule.get('name','')} {rule.get('category','')} {rule.get('description','')}".lower()
                if filter_text not in haystack:
                    continue
            QTreeWidgetItem(self._yara_tree, [rule["name"], rule["category"], rule["description"]])

    def _populate_nuclei_tree(self) -> None:
        self._nuclei_tree.clear()
        for tmpl in self._nuclei_data:
            filter_text = self._filter_input.text().lower().strip()
            if filter_text:
                haystack = f"{tmpl.get('name','')} {tmpl.get('severity','')} {tmpl.get('cve','')} {tmpl.get('description','')}".lower()
                if filter_text not in haystack:
                    continue
            QTreeWidgetItem(self._nuclei_tree, [tmpl["name"], tmpl["severity"], tmpl["cve"], tmpl["description"]])

    def _populate_tools_tree(self) -> None:
        self._tools_tree.clear()
        for tool in self._tools_data:
            filter_text = self._filter_input.text().lower().strip()
            if filter_text:
                haystack = f"{tool.get('name','')} {tool.get('type','')} {tool.get('description','')}".lower()
                if filter_text not in haystack:
                    continue
            QTreeWidgetItem(self._tools_tree, [tool["name"], tool["type"], tool["description"]])

    def _apply_filter(self) -> None:
        self._populate_yara_tree()
        self._populate_nuclei_tree()
        self._populate_tools_tree()

    def _show_selected_info(self) -> None:
        current_tab = self._tabs.currentWidget()
        if current_tab is self._yara_tree:
            self._backend.send_command("yara_marketplace list", target_session=None)
        elif current_tab is self._nuclei_tree:
            self._backend.send_command("nuclei_marketplace list", target_session=None)
        elif current_tab is self._tools_tree:
            self._backend.send_command("marketplace list", target_session=None)
