"""Marketplace panel for YARA rules, Nuclei templates, YAML addons and Lua plugins.

Lists installed items from lazyaddons/*.yaml, plugins/*.lua, yara_rules/*.yar,
and nuclei-templates/*.yaml. Supports search, filter, and run actions.
"""

from __future__ import annotations

from collections.abc import Mapping

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
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


class MarketplacePanel(PanelBase):
    """Dock panel listing YARA rules, Nuclei templates, Addons and Plugins."""

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

        self._yara_tree = self._make_tree(("Name", "Category", "Description"))
        self._nuclei_tree = self._make_tree(("Name", "Severity", "CVE", "Description"))
        self._addons_tree = self._make_tree(("Name", "Type", "Phase", "Description"))
        self._plugins_tree = self._make_tree(("Name", "Type", "Description"))

        self._tabs.addTab(self._yara_tree, "YARA Rules")
        self._tabs.addTab(self._nuclei_tree, "Nuclei")
        self._tabs.addTab(self._addons_tree, "Addons")
        self._tabs.addTab(self._plugins_tree, "Plugins")

        filter_bar = QHBoxLayout()
        self._filter_input = QLineEdit(container)
        self._filter_input.setPlaceholderText("Search marketplace...")
        self._filter_input.textChanged.connect(self._apply_filter)
        filter_bar.addWidget(self._filter_input)
        refresh_btn = QPushButton("Refresh", container)
        refresh_btn.clicked.connect(self._refresh)
        filter_bar.addWidget(refresh_btn)
        run_btn = QPushButton("Run", container)
        run_btn.clicked.connect(self._run_selected)
        filter_bar.addWidget(run_btn)
        info_btn = QPushButton("Info", container)
        info_btn.clicked.connect(self._show_selected_info)
        filter_bar.addWidget(info_btn)

        layout.addLayout(filter_bar)
        layout.addWidget(self._tabs)
        self.setWidget(container)

        self._yara_data: list[dict[str, str]] = []
        self._nuclei_data: list[dict[str, str]] = []
        self._addons_data: list[dict[str, str]] = []
        self._plugins_data: list[dict[str, str]] = []

        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(constants.timing.panel_refresh_interval_ms)
        self._refresh_timer.timeout.connect(self._refresh)
        self._refresh_timer.start()
        self._refresh()

    @staticmethod
    def _make_tree(headers: tuple[str, ...]) -> QTreeWidget:
        tree = QTreeWidget()
        tree.setColumnCount(len(headers))
        tree.setHeaderLabels(list(headers))
        tree.setRootIsDecorated(False)
        tree.setAlternatingRowColors(True)
        tree.setUniformRowHeights(True)
        tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        tree.header().setStretchLastSection(True)
        return tree

    def _refresh(self) -> None:
        self._fetch_yara_rules()
        self._fetch_nuclei_templates()
        self._fetch_addons()
        self._fetch_plugins()

    def _fetch_yara_rules(self) -> None:
        rules: list[dict[str, str]] = []
        try:
            from pathlib import Path
            yara_dir = Path("yara_rules")
            if yara_dir.is_dir():
                for yar_file in sorted(yara_dir.glob("*.yar")):
                    category = str(yar_file.stem).replace("_", " ").title()
                    description = f"YARA rule ({yar_file.stat().st_size} bytes)"
                    rules.append({"name": yar_file.name, "category": category, "description": description})
        except Exception:
            pass
        self._yara_data = rules
        self._populate_yara_tree()

    def _fetch_nuclei_templates(self) -> None:
        templates: list[dict[str, str]] = []
        try:
            from pathlib import Path
            for nuclei_dir in (Path("nuclei-templates"), Path.home() / "nuclei-templates"):
                if not nuclei_dir.is_dir():
                    continue
                for yaml_file in sorted(nuclei_dir.rglob("*.yaml"))[:200]:
                    try:
                        lines = yaml_file.read_text(encoding="utf-8", errors="ignore").splitlines()[:20]
                        severity = ""
                        cve_val = ""
                        for line in lines:
                            stripped = line.strip()
                            if stripped.startswith("severity:"):
                                severity = stripped.split(":", 1)[-1].strip()
                            if stripped.lower().startswith("cve:"):
                                cve_val = stripped.split(":", 1)[-1].strip()
                        templates.append({
                            "name": yaml_file.name,
                            "severity": severity or "unknown",
                            "cve": cve_val or "",
                            "description": yaml_file.relative_to(nuclei_dir).as_posix(),
                        })
                    except Exception:
                        pass
                break
        except Exception:
            pass
        self._nuclei_data = templates
        self._populate_nuclei_tree()

    def _fetch_addons(self) -> None:
        addons: list[dict[str, str]] = []
        try:
            from pathlib import Path

            import yaml as _yaml
            addons_dir = Path("lazyaddons")
            if addons_dir.is_dir():
                for yaml_file in sorted(addons_dir.glob("*.yaml")):
                    try:
                        content = _yaml.safe_load(yaml_file.read_text(encoding="utf-8", errors="ignore"))
                        if isinstance(content, Mapping):
                            addons.append({
                                "name": yaml_file.stem,
                                "type": str(content.get("type", content.get("category", "tool"))),
                                "phase": str(content.get("phase", content.get("kill_chain_phase", ""))),
                                "description": str(content.get("description", content.get("summary", "")))[:200],
                                "command": str(content.get("command", content.get("cmd", ""))),
                            })
                        else:
                            addons.append({"name": yaml_file.stem, "type": "yaml", "phase": "", "description": "", "command": ""})
                    except Exception:
                        addons.append({"name": yaml_file.stem, "type": "yaml", "phase": "", "description": "", "command": ""})
        except Exception:
            pass
        self._addons_data = addons
        self._populate_addons_tree()

    def _fetch_plugins(self) -> None:
        plugins: list[dict[str, str]] = []
        try:
            from pathlib import Path
            plugins_dir = Path("plugins")
            if plugins_dir.is_dir():
                for lua_file in sorted(plugins_dir.glob("*.lua")):
                    try:
                        plugins.append({
                            "name": lua_file.stem,
                            "type": "lua",
                            "description": f"Lua plugin ({lua_file.stat().st_size} bytes)",
                        })
                    except Exception:
                        pass
                for yaml_file in plugins_dir.glob("*.yaml"):
                    try:
                        import yaml as _yaml
                        content = _yaml.safe_load(yaml_file.read_text(encoding="utf-8", errors="ignore"))
                        desc = str(content.get("description", ""))[:200] if isinstance(content, Mapping) else ""
                        plugins.append({"name": yaml_file.stem, "type": "yaml", "description": desc})
                    except Exception:
                        plugins.append({"name": yaml_file.stem, "type": "yaml", "description": ""})
        except Exception:
            pass
        self._plugins_data = plugins
        self._populate_plugins_tree()

    def _populate_yara_tree(self) -> None:
        self._yara_tree.clear()
        ft = self._filter_input.text().lower().strip()
        for r in self._yara_data:
            if ft and ft not in f"{r.get('name','')} {r.get('category','')} {r.get('description','')}".lower():
                continue
            QTreeWidgetItem(self._yara_tree, [r["name"], r["category"], r["description"]])

    def _populate_nuclei_tree(self) -> None:
        self._nuclei_tree.clear()
        ft = self._filter_input.text().lower().strip()
        for t in self._nuclei_data:
            if ft and ft not in f"{t.get('name','')} {t.get('severity','')} {t.get('cve','')} {t.get('description','')}".lower():
                continue
            QTreeWidgetItem(self._nuclei_tree, [t["name"], t["severity"], t["cve"], t["description"]])

    def _populate_addons_tree(self) -> None:
        self._addons_tree.clear()
        ft = self._filter_input.text().lower().strip()
        for a in self._addons_data:
            if ft and ft not in f"{a.get('name','')} {a.get('type','')} {a.get('phase','')} {a.get('description','')}".lower():
                continue
            QTreeWidgetItem(self._addons_tree, [a["name"], a["type"], a["phase"], a["description"]])

    def _populate_plugins_tree(self) -> None:
        self._plugins_tree.clear()
        ft = self._filter_input.text().lower().strip()
        for p in self._plugins_data:
            if ft and ft not in f"{p.get('name','')} {p.get('type','')} {p.get('description','')}".lower():
                continue
            QTreeWidgetItem(self._plugins_tree, [p["name"], p["type"], p["description"]])

    def _apply_filter(self) -> None:
        self._populate_yara_tree()
        self._populate_nuclei_tree()
        self._populate_addons_tree()
        self._populate_plugins_tree()

    def _show_selected_info(self) -> None:
        current_tab = self._tabs.currentWidget()
        if current_tab is self._yara_tree:
            self._backend.send_command("yara_marketplace list", target_session=None)
        elif current_tab is self._nuclei_tree:
            self._backend.send_command("nuclei_marketplace list", target_session=None)
        elif current_tab is self._addons_tree:
            self._backend.send_command("marketplace list", target_session=None)
        elif current_tab is self._plugins_tree:
            self._backend.send_command("plugins list", target_session=None)

    def _run_selected(self) -> None:
        current_tab = self._tabs.currentWidget()
        items = current_tab.selectedItems() if current_tab else []
        if not items:
            return
        name = items[0].text(0)
        if current_tab is self._yara_tree:
            self._backend.send_command(f"yara_scan {name}", target_session=None)
        elif current_tab is self._nuclei_tree:
            self._backend.send_command(f"nuclei -t {name}", target_session=None)
        elif current_tab is self._addons_tree:
            self._backend.send_command(f"use {name}\nrun", target_session=None)
        elif current_tab is self._plugins_tree:
            self._backend.send_command(f"plugin load {name}", target_session=None)
