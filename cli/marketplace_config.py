"""Interactive marketplace manager for LazyOwn lazyaddons, plugins, and tools.

A Textual console in the same style as ``lazy_orchestrator``: searchable
tabs, a table per source, a detail/preview pane and keyboard actions to
toggle, edit, create and delete entries.

Sources and their state keys:

===============  =============  ===========  =====================
tab              format         state key    notes
===============  =============  ===========  =====================
``lazyaddons``   YAML           ``enabled``  tool integrations
``plugins``      YAML           ``enabled``  metadata beside Lua code
``tools``        JSON           ``active``   pwntomate auto-jobs
``yara``         text           -            read-only rules
``nuclei``       YAML           -            read-only templates
===============  =============  ===========  =====================

Design (SOLID):

- ``MarketplaceConfig`` centralises labels, columns and file templates.
- ``AddonInfo`` knows how to read and persist one entry in its own format.
- ``AddonRegistry`` scans directories, creates and deletes entries.
- ``MarketplaceSettings`` is the mutable enabled-state view.
- ``MarketplaceConfigApp`` is the only Textual surface.
- ``configure_marketplace_interactive`` is the public entry point.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    Input,
    Static,
    TabbedContent,
    TabPane,
)

from cli.tui_forms import ConfirmModal, FormModal, TextEditorModal

BASE_DIR = Path(__file__).resolve().parent.parent
LAZYADDONS_DIR = BASE_DIR / "lazyaddons"
PLUGINS_DIR = BASE_DIR / "plugins"
TOOLS_DIR = BASE_DIR / "tools"
YARA_DIR = BASE_DIR / "yara_rules"

_NUCLEI_CANDIDATES = [
    BASE_DIR.parent / "nuclei-templates",
    Path.home() / "nuclei-templates",
    Path.home() / ".local" / "nuclei-templates",
    BASE_DIR / "external" / ".exploit" / "nuclei-templates",
]
_SEVERITY_RANK = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 4,
}
_SKIP_STEMS = {"tiers", "_example"}
_SKIP_PREFIXES = ("01 - template",)
MAX_EDITOR_BYTES = 500_000
PREVIEW_LINES = 16


@dataclass(frozen=True)
class MarketplaceConfig:
    """Centralised labels, columns and file templates."""

    wizard_title: str = "LazyOwn Marketplace Manager"
    wizard_subtitle: str = "Addon / Plugin / Tool - search, toggle, edit, create"
    wizard_footer: str = (
        "[/] filter  [space] toggle  [a/n] all/none  [e] edit  [c] create  "
        "[d] delete  [r] rescan  [enter] save  [esc] cancel"
    )
    name_col: int = 34
    detail_lines: int = PREVIEW_LINES

    YAML_ADDON_TEMPLATE: str = (
        "name: {name}\n"
        "description: >\n"
        "  Short description of what {name} does.\n"
        "author: LazyOwn RedTeam\n"
        "version: '1.0'\n"
        "enabled: true\n"
        "params: []\n"
        "os: any\n"
        "trigger: []\n"
        "tool:\n"
        "  name: {name}\n"
        "  repo_url: https://github.com/example/{name}.git\n"
        "  install_path: external/.exploit/{name}\n"
        "  install_command: ''\n"
        "  execute_command: ''\n"
        "category: 12. Miscellaneous\n"
    )
    PLUGIN_TEMPLATE: str = (
        "name: {name}\n"
        "version: '1.0'\n"
        "description: >\n"
        "  Short description of what {name} does.\n"
        "author: LazyOwn RedTeam\n"
        "category: custom\n"
        "phase: post_exploitation\n"
        "enabled: true\n"
        "tags:\n"
        "  - custom\n"
        "params: []\n"
    )
    TOOL_TEMPLATE: dict[str, Any] = field(
        default_factory=lambda: {
            "toolname": "{name}",
            "command": "",
            "trigger": [],
            "active": True,
            "category": "12. Miscellaneous",
            "description": "Pwntomate tool: {name}",
        }
    )


@dataclass
class AddonInfo:
    """One marketplace entry plus the rules to read and persist it."""

    name: str
    path: Path
    kind: str
    enabled: bool = True
    update: bool = False
    description: str = ""
    author: str = ""
    version: str = ""
    category: str = ""
    state_key: str = "enabled"
    data_format: str = "yaml"
    editable: bool = True

    @classmethod
    def from_path(cls, path: Path, kind: str) -> AddonInfo:
        """Build one entry from its file, tolerating malformed content."""
        if kind == "tools":
            return cls._from_json(path, kind)
        if kind in ("yara", "nuclei"):
            return cls._from_read_only(path, kind)
        return cls._from_yaml(path, kind)

    @classmethod
    def _from_yaml(cls, path: Path, kind: str) -> AddonInfo:
        """Parse a YAML addon or plugin metadata file."""
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            data = {}
        if not isinstance(data, dict):
            data = {}
        return cls(
            name=str(data.get("name") or path.stem),
            path=path,
            kind=kind,
            enabled=bool(data.get("enabled", True)),
            update=bool(data.get("update", False)),
            description=" ".join(str(data.get("description") or "").split())[:160],
            author=str(data.get("author") or ""),
            version=str(data.get("version") or ""),
            category=str(data.get("category") or ""),
            state_key="enabled",
            data_format="yaml",
            editable=True,
        )

    @classmethod
    def _from_json(cls, path: Path, kind: str) -> AddonInfo:
        """Parse a ``.tool`` JSON job."""
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            data = {}
        if not isinstance(data, dict):
            data = {}
        return cls(
            name=str(data.get("toolname") or path.stem),
            path=path,
            kind=kind,
            enabled=bool(data.get("active", True)),
            description=" ".join(str(data.get("description") or "").split())[:160],
            author="pwntomate",
            category=str(data.get("category") or ""),
            state_key="active",
            data_format="json",
            editable=True,
        )

    @classmethod
    def _from_read_only(cls, path: Path, kind: str) -> AddonInfo:
        """Build a read-only YARA or Nuclei row."""
        return cls(
            name=path.stem if kind == "yara" else path.name,
            path=path,
            kind=kind,
            enabled=True,
            description="" if kind == "yara" else path.parent.name,
            author="" if kind == "yara" else "nuclei-templates",
            state_key="",
            data_format="text",
            editable=kind == "yara",
        )

    @property
    def toggleable(self) -> bool:
        """Return whether this entry has a persisted enable/disable flag."""
        return bool(self.state_key) and self.editable

    def read_text(self) -> str:
        """Return the raw file text, capped for the in-app editor."""
        return self.path.read_text(encoding="utf-8", errors="replace")[:MAX_EDITOR_BYTES]

    def read_data(self) -> dict[str, Any] | None:
        """Return the parsed mapping for the entry's format."""
        try:
            text = self.path.read_text(encoding="utf-8", errors="replace")
            data = json.loads(text) if self.data_format == "json" else yaml.safe_load(text)
        except Exception:
            return None
        return dict(data) if isinstance(data, dict) else None

    def validate_text(self, text: str) -> None:
        """Raise ``ValueError`` when the edited document is not usable."""
        if not self.editable:
            raise ValueError("this entry is read-only")
        stripped = str(text or "").strip()
        if not stripped:
            raise ValueError("content is empty")
        if self.data_format == "json":
            try:
                data = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON: {exc}") from exc
        elif self.data_format == "yaml":
            try:
                data = yaml.safe_load(stripped)
            except yaml.YAMLError as exc:
                raise ValueError(f"invalid YAML: {exc}") from exc
        else:
            return
        if not isinstance(data, dict):
            raise ValueError("document must be a mapping")

    def save_text(self, text: str) -> bool:
        """Validate and atomically rewrite the raw entry."""
        try:
            self.validate_text(text)
        except ValueError:
            return False
        target = self.path
        tmp = target.with_name(f".{target.name}.tmp")
        try:
            tmp.write_text(text, encoding="utf-8")
            os.replace(tmp, target)
        except OSError:
            return False
        finally:
            if tmp.exists():
                tmp.unlink(missing_ok=True)
        return True

    def set_enabled(self, enabled: bool) -> bool:
        """Persist the enable/disable flag in the entry's native format."""
        if not self.toggleable:
            return False
        data = self.read_data()
        if data is None:
            return False
        data[self.state_key] = bool(enabled)
        try:
            text = (
                json.dumps(data, indent=2, ensure_ascii=False)
                if self.data_format == "json"
                else yaml.safe_dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
            )
        except (TypeError, ValueError):
            return False
        if not self.save_text(text):
            return False
        self.enabled = bool(enabled)
        return True

    def toggle_enabled(self) -> bool:
        """Flip the enabled state on disk."""
        return self.set_enabled(not self.enabled)

    def save_yaml(self, data: dict) -> bool:
        """Rewrite a YAML entry with the given mapping (compatibility helper)."""
        if self.data_format != "yaml":
            return False
        try:
            text = yaml.safe_dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except (TypeError, ValueError):
            return False
        return self.save_text(text)


class AddonRegistry:
    """Scan marketplace directories and create or delete entries."""

    _TAB_SOURCES = {
        "lazyaddons": (LAZYADDONS_DIR, ("*.yaml",)),
        "plugins": (PLUGINS_DIR, ("*.yaml",)),
        "tools": (TOOLS_DIR, ("*.tool",)),
    }
    _TAB_LABELS = {
        "lazyaddons": "YAML Addons",
        "plugins": "Plugins",
        "tools": "Tools",
        "yara": "YARA Rules",
        "nuclei": "Nuclei",
    }
    _READ_ONLY_TABS = frozenset({"yara", "nuclei"})

    def __init__(self) -> None:
        """Start with an empty per-tab cache."""
        self._addons: dict[str, list[AddonInfo]] = {}

    def _nuclei_dir(self) -> Path | None:
        """Return the first populated nuclei-templates directory, if any."""
        for candidate in _NUCLEI_CANDIDATES:
            if candidate.is_dir() and any(candidate.glob("**/*.yaml")):
                return candidate
        return None

    def scan(self, tab: str) -> list[AddonInfo]:
        """Return the cached (or freshly scanned) rows for one tab."""
        if tab in self._addons:
            return self._addons[tab]
        if tab == "yara":
            addons = self._scan_yara()
        elif tab == "nuclei":
            addons = self._scan_nuclei()
        elif tab in self._TAB_SOURCES:
            addons = self._scan_files(tab)
        else:
            addons = []
        self._addons[tab] = addons
        return addons

    def _scan_files(self, tab: str) -> list[AddonInfo]:
        """Scan one YAML/JSON source directory."""
        source, extensions = self._TAB_SOURCES[tab]
        addons: list[AddonInfo] = []
        if not source.is_dir():
            return addons
        for extension in extensions:
            for fpath in sorted(source.glob(extension)):
                if fpath.stem in _SKIP_STEMS or fpath.stem.startswith(_SKIP_PREFIXES):
                    continue
                addons.append(AddonInfo.from_path(fpath, tab))
        return addons

    def _scan_yara(self) -> list[AddonInfo]:
        """Scan YARA rules (read-only toggles)."""
        if not YARA_DIR.exists():
            return []
        addons: list[AddonInfo] = []
        for extension in ("*.yar", "*.yara"):
            for fpath in sorted(YARA_DIR.glob(extension)):
                info = AddonInfo.from_path(fpath, "yara")
                info.description = self._parse_yara_meta(fpath)
                addons.append(info)
        return addons

    def _scan_nuclei(self) -> list[AddonInfo]:
        """Scan Nuclei templates ordered by severity."""
        nuc_dir = self._nuclei_dir()
        if nuc_dir is None:
            return []
        indexed: list[tuple[int, str, Path, str]] = []
        for fpath in nuc_dir.glob("**/*.yaml"):
            severity = self._parse_nuclei_severity(fpath)
            rel = fpath.relative_to(nuc_dir).as_posix()
            indexed.append((_SEVERITY_RANK.get(severity.lower(), 5), rel, fpath, severity))
        indexed.sort(key=lambda item: (item[0], item[1]))
        addons: list[AddonInfo] = []
        for _rank, rel, fpath, severity in indexed:
            info = AddonInfo.from_path(fpath, "nuclei")
            info.name = f"{rel} [{severity}]"
            info.version = severity
            info.description = f"{severity} | {rel}"
            addons.append(info)
        return addons

    @staticmethod
    def _parse_yara_meta(path: Path) -> str:
        """Extract the first description string from a YARA rule."""
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:30]:
                stripped = line.strip()
                if "description" in stripped.lower() and "=" in stripped:
                    return stripped.split("=", 1)[-1].strip().strip('"').strip("'")[:100]
        except OSError:
            pass
        return ""

    @staticmethod
    def _parse_nuclei_severity(path: Path) -> str:
        """Extract the severity field from a Nuclei template."""
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
                stripped = line.strip()
                if stripped.startswith("severity:"):
                    return stripped.split(":", 1)[-1].strip()
        except OSError:
            pass
        return "info"

    def rescan(self, tab: str) -> list[AddonInfo]:
        """Drop one tab cache and scan again."""
        self._addons.pop(tab, None)
        return self.scan(tab)

    def tab_order(self) -> list[str]:
        """Return the tab order used by the console."""
        return ["lazyaddons", "plugins", "tools", "yara", "nuclei"]

    def tab_label(self, tab: str) -> str:
        """Return the human label for one tab."""
        return self._TAB_LABELS.get(tab, tab)

    def tab_count(self, tab: str) -> int:
        """Return how many entries one tab holds."""
        return len(self.scan(tab))

    def tab_is_read_only(self, tab: str) -> bool:
        """Return whether toggles are meaningless for the tab."""
        return tab in self._READ_ONLY_TABS

    def create_addon(self, tab: str, name: str) -> Path | None:
        """Create one entry from the tab template.

        Args:
            tab: Destination tab (``lazyaddons``, ``plugins`` or ``tools``).
            name: File stem; sanitized to ``[a-z0-9_-]``.

        Returns:
            The created path, or None when the tab is read-only or the
            file already exists.
        """
        clean = "".join(char for char in str(name or "").strip() if char.isalnum() or char in "-_")
        if not clean or tab not in self._TAB_SOURCES:
            return None
        source, _extensions = self._TAB_SOURCES[tab]
        if tab == "tools":
            path = source / f"{clean}.tool"
            payload = json.dumps(
                {
                    "toolname": clean,
                    "command": "",
                    "trigger": [],
                    "active": True,
                    "category": "12. Miscellaneous",
                    "description": f"Pwntomate tool: {clean}",
                },
                indent=2,
            )
        elif tab == "plugins":
            path = source / f"{clean}.yaml"
            payload = MarketplaceConfig().PLUGIN_TEMPLATE.format(name=clean)
        else:
            path = source / f"{clean}.yaml"
            payload = MarketplaceConfig().YAML_ADDON_TEMPLATE.format(name=clean)
        if path.exists():
            return None
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload, encoding="utf-8")
        except OSError:
            return None
        self.rescan(tab)
        return path

    def delete_addon(self, addon: AddonInfo) -> bool:
        """Delete one writable entry confined to its source directory."""
        if not addon.editable or addon.kind in self._READ_ONLY_TABS:
            return False
        source = addon.path.parent.resolve()
        target = addon.path.resolve()
        if target.parent != source or target.suffix not in (".yaml", ".yml", ".tool"):
            return False
        try:
            target.unlink()
        except OSError:
            return False
        self.rescan(addon.kind)
        return True


@dataclass
class MarketplaceSettings:
    """Mutable marketplace state: which addons are enabled."""

    enabled: dict[str, set[str]] = field(default_factory=dict)

    def is_enabled(self, kind: str, name: str) -> bool:
        """Return whether one entry is enabled."""
        return name in self.enabled.get(kind, set())

    def toggle(self, addon: AddonInfo) -> bool:
        """Flip one entry, updating the in-memory view only on success."""
        changed = addon.toggle_enabled()
        if not changed:
            return False
        bucket = self.enabled.setdefault(addon.kind, set())
        if addon.enabled:
            bucket.add(addon.name)
        else:
            bucket.discard(addon.name)
        return True

    def enable_all(self, addons: list[AddonInfo]) -> int:
        """Enable every toggleable entry; return how many changed."""
        changed = 0
        for addon in addons:
            if addon.toggleable and not addon.enabled and self.toggle(addon):
                changed += 1
        return changed

    def disable_all(self, addons: list[AddonInfo]) -> int:
        """Disable every toggleable entry; return how many changed."""
        changed = 0
        for addon in addons:
            if addon.toggleable and addon.enabled and self.toggle(addon):
                changed += 1
        return changed


class MarketplaceConfigApp(App[MarketplaceSettings | None]):
    """Textual marketplace console: search, toggle, edit, create, delete."""

    CSS = """
    #market-filter { dock: top; margin: 0 1; }
    #market-tabs { height: 1fr; }
    DataTable { height: 1fr; }
    #market-detail { height: 10; border: round $secondary; padding: 0 1; }
    .modal-box { width: 70; height: auto; padding: 1 2; background: $surface;
                 border: round $accent; }
    .modal-box-wide { width: 100; height: 38; padding: 1 2; background: $surface;
                      border: round $accent; }
    .modal-title { text-style: bold; padding-bottom: 1; }
    .modal-label { padding-top: 1; }
    .modal-hint { color: $text-muted; padding-top: 1; }
    .modal-error { color: $error; padding-top: 1; }
    """

    BINDINGS = [
        Binding("q", "cancel", "Quit"),
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "save", "Save"),
        Binding("r", "rescan", "Rescan"),
        Binding("space", "toggle", "Toggle"),
        Binding("a", "enable_all", "All on"),
        Binding("n", "disable_all", "All off"),
        Binding("e", "edit", "Edit"),
        Binding("c", "create", "Create"),
        Binding("d", "delete", "Delete"),
        Binding("/", "focus_filter", "Filter"),
    ]

    def __init__(
        self,
        config: MarketplaceConfig,
        registry: AddonRegistry,
        initial: MarketplaceSettings,
        start_tab: str = "",
    ) -> None:
        """Bind the console to a config, registry and initial state."""
        super().__init__()
        self._cfg = config
        self._addon_registry = registry
        self._settings = initial
        self._start_tab = start_tab if start_tab in registry.tab_order() else registry.tab_order()[0]
        self._filter = ""

    def compose(self) -> ComposeResult:
        """Header, filter box, one table per tab and the detail pane."""
        yield Header(show_clock=True)
        yield Input(placeholder="filter by name, author or description", id="market-filter")
        with TabbedContent(id="market-tabs", initial=f"market-tab-{self._start_tab}"):
            for tab in self._addon_registry.tab_order():
                with TabPane(self._addon_registry.tab_label(tab), id=f"market-tab-{tab}"):
                    yield DataTable(id=f"market-{tab}")
        yield Static("select an entry to preview it", id="market-detail")
        yield Footer()

    def on_mount(self) -> None:
        """Render every table and focus the filter box."""
        self.title = self._cfg.wizard_title
        self.sub_title = self._cfg.wizard_subtitle
        self._refresh_all()
        try:
            self.query_one("#market-filter", Input).focus()
        except Exception:
            pass

    def _active_tab(self) -> str:
        """Return the active marketplace tab key."""
        try:
            active = str(self.query_one("#market-tabs", TabbedContent).active)
        except Exception:
            return self._addon_registry.tab_order()[0]
        return active.removeprefix("market-tab-")

    def _rows(self, tab: str) -> list[AddonInfo]:
        """Return the filtered rows for one tab."""
        needle = self._filter.strip().lower()
        rows = self._addon_registry.scan(tab)
        if not needle:
            return rows
        return [
            row
            for row in rows
            if needle in row.name.lower()
            or needle in row.author.lower()
            or needle in row.description.lower()
            or needle in row.category.lower()
        ]

    def _refresh_all(self) -> None:
        """Repaint every tab (counts) and the active table."""
        for tab in self._addon_registry.tab_order():
            self._refresh_tab_labels(tab)
        self._refresh_table(self._active_tab())

    def _refresh_tab_labels(self, tab: str) -> None:
        """Rewrite one tab label with the current entry count."""
        try:
            content_tab = self.query_one("#market-tabs", TabbedContent).get_tab(f"market-tab-{tab}")
            content_tab.label = f"{self._addon_registry.tab_label(tab)} ({self._addon_registry.tab_count(tab)})"
        except Exception:
            pass

    def _refresh_table(self, tab: str) -> None:
        """Repaint one tab table from the registry."""
        try:
            table = self.query_one(f"#market-{tab}", DataTable)
        except Exception:
            return
        table.clear(columns=True)
        table.add_columns("name", "state", "author", "version", "update", "description")
        for row in self._rows(tab):
            state = "on" if row.enabled else "off"
            if not row.toggleable and row.kind not in ("yara", "nuclei"):
                state = "?"
            table.add_row(
                row.name[: self._cfg.name_col],
                state,
                row.author[:18],
                row.version[:10],
                "yes" if row.update else "",
                row.description[:70],
                key=str(row.path),
            )
        self._update_detail(self._selected_row(tab), tab)

    def _selected_addon(self, tab: str) -> AddonInfo | None:
        """Return the entry highlighted in one tab table."""
        raw = self._selected_row(tab)
        if not raw:
            return None
        return next((row for row in self._rows(tab) if str(row.path) == raw), None)

    def _selected_row(self, tab: str) -> str:
        """Return the selected row key for one tab."""
        try:
            table = self.query_one(f"#market-{tab}", DataTable)
            key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            return str(key.value or "")
        except Exception:
            return ""

    def _update_detail(self, row_key: str, tab: str = "") -> None:
        """Render the selected entry's metadata and text preview."""
        try:
            panel = self.query_one("#market-detail", Static)
        except Exception:
            return
        if not row_key:
            panel.update("select an entry to preview it")
            return
        tab = tab or self._active_tab()
        addon = next((row for row in self._rows(tab) if str(row.path) == row_key), None)
        if addon is None:
            panel.update("entry unavailable")
            return
        state = "on" if addon.enabled else "off"
        if self._addon_registry.tab_is_read_only(tab):
            state = "read-only"
        header = [
            f"{addon.name}  [{tab}/{state}]",
            f"path: {addon.path}",
            f"author: {addon.author or '-'}  version: {addon.version or '-'}  update: {addon.update}",
        ]
        if addon.category:
            header.append(f"category: {addon.category}")
        if addon.description:
            header.append(f"description: {addon.description}")
        try:
            preview = addon.read_text().splitlines()[: self._cfg.detail_lines]
        except OSError:
            preview = ["unreadable"]
        panel.update("\n".join([*header, "---", *preview]))

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Refresh the detail pane when the cursor moves."""
        try:
            if not str(event.control.id or "").startswith("market-"):
                return
            key = str(event.row_key.value or "")
        except Exception:
            return
        self._update_detail(key, self._active_tab())

    def on_input_changed(self, event: Input.Changed) -> None:
        """Filter the active table as the operator types."""
        if event.input.id == "market-filter":
            self._filter = event.value
            self._refresh_table(self._active_tab())

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        """Repaint the table that just became visible."""
        try:
            tab = str(event.pane.id or "").removeprefix("market-tab-")
        except Exception:
            return
        if tab:
            self._refresh_table(tab)

    def action_focus_filter(self) -> None:
        """Move focus to the filter box."""
        try:
            self.query_one("#market-filter", Input).focus()
        except Exception:
            pass

    def action_rescan(self) -> None:
        """Rescan the active tab and repaint."""
        tab = self._active_tab()
        self._addon_registry.rescan(tab)
        self._refresh_tab_labels(tab)
        self._refresh_table(tab)

    def action_toggle(self) -> None:
        """Toggle the selected entry when the tab supports it."""
        tab = self._active_tab()
        addon = self._selected_addon(tab)
        if addon is None:
            return
        if not self._settings.toggle(addon):
            self.notify(f"{addon.name}: toggling is not supported on this tab", severity="warning")
            return
        self._refresh_table(tab)

    def action_enable_all(self) -> None:
        """Enable every toggleable entry in the active tab."""
        tab = self._active_tab()
        changed = self._settings.enable_all(self._addon_registry.scan(tab))
        self.notify(f"{changed} entry(ies) enabled")
        self._refresh_table(tab)

    def action_disable_all(self) -> None:
        """Disable every toggleable entry in the active tab."""
        tab = self._active_tab()
        changed = self._settings.disable_all(self._addon_registry.scan(tab))
        self.notify(f"{changed} entry(ies) disabled")
        self._refresh_table(tab)

    def action_create(self) -> None:
        """Create one entry in the active tab from its template."""
        tab = self._active_tab()
        if self._addon_registry.tab_is_read_only(tab):
            self.notify("this tab is read-only", severity="warning")
            return

        def _created(values: dict | None) -> None:
            if not (values and values.get("name")):
                return
            path = self._addon_registry.create_addon(tab, values["name"])
            if path is None:
                self.notify("could not create entry (name in use or invalid)", severity="error")
                return
            self._refresh_all()
            self.notify(f"created {path.name}")

        self.push_screen(
            FormModal(
                f"New {self._addon_registry.tab_label(tab)} entry",
                [("name", "Name", "my_addon")],
            ),
            _created,
        )

    def action_edit(self) -> None:
        """Open the raw file editor for the selected entry."""
        tab = self._active_tab()
        addon = self._selected_addon(tab)
        if addon is None or not addon.editable:
            self.notify("this entry is read-only", severity="warning")
            return
        try:
            text = addon.read_text()
        except OSError as exc:
            self.notify(f"unreadable: {exc}", severity="error")
            return
        language = "json" if addon.data_format == "json" else "yaml"

        def _saved(raw: str | None) -> None:
            if raw is None:
                return
            if not addon.save_text(raw):
                self.notify("not saved: invalid content", severity="error")
                return
            self._refresh_all()
            self.notify(f"saved {addon.path.name}")

        self.push_screen(
            TextEditorModal(f"Edit {addon.path.name}", text, validator=addon.validate_text, language=language),
            _saved,
        )

    def action_delete(self) -> None:
        """Delete the selected entry after confirmation."""
        tab = self._active_tab()
        addon = self._selected_addon(tab)
        if addon is None:
            return
        if not addon.editable or self._addon_registry.tab_is_read_only(tab):
            self.notify("this entry is read-only", severity="warning")
            return

        def _confirmed(answer: bool | None) -> None:
            if not answer:
                return
            if self._addon_registry.delete_addon(addon):
                self._refresh_all()
                self.notify(f"deleted {addon.path.name}")
            else:
                self.notify("could not delete entry", severity="error")

        self.push_screen(
            ConfirmModal(f"Delete {addon.name}?", str(addon.path)),
            _confirmed,
        )

    def action_save(self) -> None:
        """Close the console and return the final settings."""
        self.exit(self._settings)

    def action_cancel(self) -> None:
        """Close the console without returning settings."""
        self.exit(None)


def configure_marketplace_interactive(
    config: MarketplaceConfig | None = None,
    start_tab: str = "",
) -> MarketplaceSettings | None:
    """Open the Textual marketplace console.

    Args:
        config: Optional custom configuration.
        start_tab: Optional tab pre-selection (``lazyaddons``, ``plugins``,
            ``tools``, ``yara``, ``nuclei``).

    Returns:
        The final :class:`MarketplaceSettings`, or ``None`` when the
        operator cancels or the environment cannot host a Textual app.
    """
    cfg = config or MarketplaceConfig()
    registry = AddonRegistry()
    initial = _build_initial_settings(registry)
    try:
        return MarketplaceConfigApp(cfg, registry, initial, start_tab=start_tab).run()
    except Exception:
        return None


def _build_initial_settings(registry: AddonRegistry) -> MarketplaceSettings:
    """Build the enabled-state view from the current files."""
    settings = MarketplaceSettings()
    for tab in registry.tab_order():
        settings.enabled[tab] = set()
        for addon in registry.scan(tab):
            if addon.enabled:
                settings.enabled[tab].add(addon.name)
    return settings


def marketplace_summary(registry: AddonRegistry | None = None) -> str:
    """Return a text summary of enabled/disabled addons across all tabs."""
    reg = registry or AddonRegistry()
    parts: list[str] = []
    for tab in reg.tab_order():
        addons = reg.scan(tab)
        on = sum(1 for addon in addons if addon.enabled)
        off = len(addons) - on
        parts.append(f"{reg.tab_label(tab)}: {on}(+{off})")
    return "  ".join(parts)


__all__ = [
    "AddonInfo",
    "AddonRegistry",
    "MarketplaceConfig",
    "MarketplaceConfigApp",
    "MarketplaceSettings",
    "configure_marketplace_interactive",
    "marketplace_summary",
]
