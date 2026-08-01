"""Interactive marketplace manager for LazyOwn lazyaddons, plugins, and tools.

Provides a curses-based TUI mirroring the Powerlevel10k-style configurator from
``banner_config.py``. The operator can browse, enable/disable, edit, and create
lazyaddons, Lua plugins, and pwntomate tools from a single interface.

Design (SOLID):

- ``MarketplaceConfig`` centralises constants (keys, key codes, palette IDs).
- ``MarketplaceSettings`` is the mutable state (enabled/disabled per addon).
- ``AddonInfo`` describes a single addon from YAML/Lua/.tool on disk.
- ``AddonRegistry`` scans ``lazyaddons/``, ``plugins/``, ``tools/`` and builds the
  canonical list.
- ``MarketplaceConfigurator`` is the only piece bound to curses; tests can
  drive any registry behaviour without a TTY.
- ``configure_marketplace_interactive`` is the public entry point.
"""

from __future__ import annotations

import curses
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

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
EDITOR = os.environ.get("EDITOR", os.environ.get("VISUAL", "vim"))


@dataclass(frozen=True)
class MarketplaceConfig:
    """Centralised constants for the marketplace configurator."""

    wizard_title: str = "LazyOwn Marketplace Manager"
    wizard_subtitle: str = "Addon / Plugin / Tool — enable, disable, edit, create"
    wizard_preview_label: str = "Details:"
    wizard_footer: str = (
        "[up/down] move  [space] toggle  [a/n] all/none  [e] edit  [c] create  [tab] tab  [enter] save  [esc] cancel"
    )

    wizard_padding_x: int = 2
    wizard_min_width: int = 88
    wizard_max_width: int = 132
    wizard_name_col: int = 28
    wizard_type_col: int = 10
    wizard_author_col: int = 14

    color_pair_border: int = 1
    color_pair_title: int = 2
    color_pair_help: int = 3
    color_pair_row: int = 4
    color_pair_selected: int = 5
    color_pair_enabled: int = 6
    color_pair_disabled: int = 7
    color_pair_preview: int = 8
    color_pair_tab_active: int = 9
    color_pair_tab_inactive: int = 10

    color_border_fg: int = curses.COLOR_CYAN
    color_title_fg: int = curses.COLOR_GREEN
    color_help_fg: int = curses.COLOR_YELLOW
    color_row_fg: int = curses.COLOR_WHITE
    color_selected_bg: int = curses.COLOR_BLUE
    color_selected_fg: int = curses.COLOR_WHITE
    color_enabled_fg: int = curses.COLOR_GREEN
    color_disabled_fg: int = curses.COLOR_MAGENTA
    color_preview_fg: int = curses.COLOR_CYAN
    color_tab_active_fg: int = curses.COLOR_BLACK
    color_tab_active_bg: int = curses.COLOR_GREEN
    color_tab_inactive_fg: int = curses.COLOR_WHITE

    key_tab: int = 9
    key_btab: int = 353
    key_enter: int = 10
    key_carriage_return: int = 13
    key_escape: int = 27
    key_ctrl_c: int = 3
    key_space: int = ord(" ")
    key_d_lower: int = ord("d")
    key_a_lower: int = ord("a")
    key_n_lower: int = ord("n")
    key_e_lower: int = ord("e")
    key_c_lower: int = ord("c")

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


@dataclass
class AddonInfo:
    """Metadata for one addon on disk."""

    name: str
    path: Path
    kind: str
    enabled: bool = True
    description: str = ""
    author: str = ""
    version: str = ""
    category: str = ""

    @classmethod
    def from_yaml(cls, path: Path) -> AddonInfo:
        try:
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                data = yaml.safe_load(fh) if yaml else {}
        except (OSError, Exception):
            data = {}
        if not isinstance(data, dict):
            data = {}
        kind = "tool" if path.suffix == ".tool" else "plugin"
        return cls(
            name=data.get("name", path.stem),
            path=path,
            kind=kind,
            enabled=data.get("enabled", True),
            description=(data.get("description") or "").replace("\n", " ")[:120],
            author=data.get("author", ""),
            version=str(data.get("version", "")),
            category=data.get("category", ""),
        )

    def toggle_enabled(self) -> None:
        """Flip the enabled state on disk."""
        self.set_enabled(not self.enabled)

    def set_enabled(self, enabled: bool) -> None:
        """Set the enabled state and persist to disk."""
        if not self.path.exists():
            return
        try:
            if yaml is None:
                return
            with self.path.open("r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
            data = yaml.safe_load(content) or {}
            data["enabled"] = enabled
            self.enabled = enabled
            with self.path.open("w", encoding="utf-8") as fh:
                yaml.safe_dump(data, fh, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except (OSError, Exception):
            pass

    def save_yaml(self, data: dict) -> None:
        """Rewrite the YAML file with the given data dictionary."""
        try:
            if yaml is None:
                return
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8") as fh:
                yaml.safe_dump(data, fh, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except (OSError, Exception):
            pass


class AddonRegistry:
    """Scans lazyaddons/, plugins/, tools/, yara_rules/, nuclei-templates/ and builds the addon list."""

    _TAB_SOURCES = {
        "lazyaddons": LAZYADDONS_DIR,
        "plugins": PLUGINS_DIR,
        "tools": TOOLS_DIR,
    }
    _TAB_EXTENSIONS = {
        "lazyaddons": ("*.yaml",),
        "plugins": ("*.yaml", "*.lua"),
        "tools": ("*.tool",),
        "yara": ("*.yar", "*.yara"),
        "nuclei": ("*.yaml",),
    }
    _TAB_LABELS = {
        "lazyaddons": "YAML Addons",
        "plugins": "Plugins",
        "tools": "Tools",
        "yara": "YARA Rules",
        "nuclei": "Nuclei",
    }

    def __init__(self) -> None:
        self._addons: dict[str, list[AddonInfo]] = {}

    def _nuclei_dir(self) -> Path | None:
        for candidate in _NUCLEI_CANDIDATES:
            if candidate.exists() and candidate.is_dir():
                yaml_files = list(candidate.glob("*.yaml"))
                if not yaml_files:
                    for sub in candidate.iterdir():
                        if sub.is_dir() and list(sub.glob("*.yaml")):
                            return candidate
                else:
                    return candidate
        return None

    def scan(self, tab: str) -> list[AddonInfo]:
        if tab in self._addons:
            return self._addons[tab]

        if tab == "yara":
            return self._scan_yara()
        if tab == "nuclei":
            return self._scan_nuclei()
        if tab not in self._TAB_SOURCES:
            return []

        source = self._TAB_SOURCES[tab]
        extensions = self._TAB_EXTENSIONS[tab]
        addons: list[AddonInfo] = []

        for ext in extensions:
            for fpath in sorted(source.glob(ext)):
                info = AddonInfo.from_yaml(fpath)
                info.kind = tab
                addons.append(info)

        self._addons[tab] = addons
        return addons

    def _scan_yara(self) -> list[AddonInfo]:
        addons: list[AddonInfo] = []
        if not YARA_DIR.exists():
            YARA_DIR.mkdir(parents=True, exist_ok=True)
        for ext in self._TAB_EXTENSIONS.get("yara", ("*.yar",)):
            for fpath in sorted(YARA_DIR.glob(ext)):
                info = AddonInfo(
                    name=fpath.stem,
                    path=fpath,
                    kind="yara",
                    enabled=True,
                    description=self._parse_yara_meta(fpath),
                    author="",
                    version="",
                )
                addons.append(info)
        self._addons["yara"] = addons
        return addons

    def _scan_nuclei(self) -> list[AddonInfo]:
        addons: list[AddonInfo] = []
        nuc_dir = self._nuclei_dir()
        if nuc_dir is None:
            self._addons["nuclei"] = addons
            return addons
        templates = sorted(nuc_dir.glob("**/*.yaml"))[:500]
        for fpath in templates:
            severity, cve_id = self._parse_nuclei_info(fpath)
            label = f"{fpath.stem} [{severity}]"
            info = AddonInfo(
                name=label[:80],
                path=fpath,
                kind="nuclei",
                enabled=True,
                description=f"CVE: {cve_id}" if cve_id else f"{severity} severity",
                author="nuclei-templates",
                version=severity,
            )
            addons.append(info)
        self._addons["nuclei"] = addons
        return addons

    @staticmethod
    def _parse_yara_meta(path: Path) -> str:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            for line in content.splitlines()[:30]:
                stripped = line.strip()
                if "description" in stripped.lower() and "=" in stripped:
                    return stripped.split("=", 1)[-1].strip().strip('"').strip("'")[:100]
        except Exception:
            pass
        return ""

    @staticmethod
    def _parse_nuclei_info(path: Path) -> tuple[str, str]:
        severity = "info"
        cve_id = ""
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            for line in content.splitlines()[:40]:
                stripped = line.strip()
                if stripped.startswith("severity:"):
                    severity = stripped.split(":", 1)[-1].strip()
                if stripped.lower().startswith("cve:") or stripped.lower().startswith("cve-id:"):
                    cve_id = stripped.split(":", 1)[-1].strip()
        except Exception:
            pass
        return severity, cve_id

    def rescan(self, tab: str) -> list[AddonInfo]:
        self._addons.pop(tab, None)
        return self.scan(tab)

    def tab_order(self) -> list[str]:
        return ["lazyaddons", "plugins", "tools", "yara", "nuclei"]

    def tab_label(self, tab: str) -> str:
        return self._TAB_LABELS.get(tab, tab)

    def tab_count(self, tab: str) -> int:
        return len(self.scan(tab))


@dataclass
class MarketplaceSettings:
    """Mutable marketplace state: which addons are enabled."""

    enabled: dict[str, set[str]] = field(default_factory=dict)

    def is_enabled(self, kind: str, name: str) -> bool:
        return name in self.enabled.get(kind, set())

    def toggle(self, addon: AddonInfo) -> None:
        addon.toggle_enabled()
        key = addon.kind
        if key not in self.enabled:
            self.enabled[key] = set()
        if addon.enabled:
            self.enabled[key].add(addon.name)
        else:
            self.enabled[key].discard(addon.name)

    def enable_all(self, addons: list[AddonInfo]) -> None:
        for a in addons:
            if not a.enabled:
                self.toggle(a)

    def disable_all(self, addons: list[AddonInfo]) -> None:
        for a in addons:
            if a.enabled:
                self.toggle(a)


class MarketplaceConfigurator:
    """Curses-driven p10k-style wizard for marketplace management."""

    def __init__(
        self,
        config: MarketplaceConfig,
        registry: AddonRegistry,
        initial: MarketplaceSettings,
    ) -> None:
        self._cfg = config
        self._registry = registry
        self._settings = initial
        self._current_tab = self._registry.tab_order()[0]
        self._cursor: dict[str, int] = {tab: 0 for tab in self._registry.tab_order()}
        self._scroll_offset: dict[str, int] = {tab: 0 for tab in self._registry.tab_order()}
        self._saved = False

    def run(self, start_tab: str = "") -> MarketplaceSettings | None:
        if not self._tty_available():
            return None
        try:
            if start_tab and start_tab in self._registry.tab_order():
                self._active_tab = self._registry.tab_order().index(start_tab)
            return curses.wrapper(self._loop)
        except curses.error:
            return None
        except KeyboardInterrupt:
            return None

    @staticmethod
    def _tty_available() -> bool:
        return sys.stdin.isatty() and sys.stdout.isatty() and os.environ.get("TERM", "") not in {"", "dumb"}

    def _rows_for_tab(self, tab: str) -> list[AddonInfo]:
        return self._registry.scan(tab)

    def _loop(self, stdscr: curses._CursesWindow) -> MarketplaceSettings | None:
        curses.curs_set(0)
        stdscr.keypad(True)
        self._init_colors()
        while True:
            rows = self._rows_for_tab(self._current_tab)
            cursor = self._cursor[self._current_tab]
            offset = self._scroll_offset[self._current_tab]
            if rows:
                cursor = max(0, min(cursor, len(rows) - 1))
                self._cursor[self._current_tab] = cursor
            self._render(stdscr, rows, cursor, offset)
            key = stdscr.getch()
            if key in (self._cfg.key_escape, self._cfg.key_ctrl_c):
                return self._settings if self._saved else None
            if key in (self._cfg.key_enter, self._cfg.key_carriage_return, curses.KEY_ENTER):
                self._saved = True
                return self._settings
            if key == self._cfg.key_tab:
                self._cycle_tab(1)
                continue
            if key in (self._cfg.key_btab, curses.KEY_BTAB):
                self._cycle_tab(-1)
                continue
            if not rows:
                continue
            if key == curses.KEY_UP:
                cursor = (cursor - 1) % len(rows)
                self._cursor[self._current_tab] = cursor
            elif key == curses.KEY_DOWN:
                cursor = (cursor + 1) % len(rows)
                self._cursor[self._current_tab] = cursor
            elif key == curses.KEY_HOME:
                self._cursor[self._current_tab] = 0
            elif key == curses.KEY_END:
                self._cursor[self._current_tab] = len(rows) - 1
            elif key == curses.KEY_NPAGE:
                self._cursor[self._current_tab] = min(cursor + 10, len(rows) - 1)
            elif key == curses.KEY_PPAGE:
                self._cursor[self._current_tab] = max(cursor - 10, 0)
            elif key == self._cfg.key_space:
                self._settings.toggle(rows[cursor])
            elif key == self._cfg.key_a_lower:
                self._settings.enable_all(rows)
            elif key == self._cfg.key_n_lower:
                self._settings.disable_all(rows)
            elif key == self._cfg.key_e_lower:
                self._edit_addon(rows[cursor])
            elif key == self._cfg.key_c_lower:
                self._create_addon(stdscr)

    def _cycle_tab(self, direction: int) -> None:
        tab_order = self._registry.tab_order()
        idx = tab_order.index(self._current_tab)
        self._current_tab = tab_order[(idx + direction) % len(tab_order)]

    def _edit_addon(self, addon: AddonInfo) -> None:
        curses.endwin()
        sys.stdout.flush()
        try:
            subprocess.call([EDITOR, str(addon.path)])
        except FileNotFoundError:
            curses.beep()
        sys.stdout.flush()
        self._registry.rescan(addon.kind)

    def _create_addon(self, stdscr: curses._CursesWindow) -> None:
        curses.echo()
        curses.curs_set(1)
        height, width = stdscr.getmaxyx()
        prompt_y = height - 2
        try:
            stdscr.addnstr(prompt_y, 2, "New addon name: ", width - 12, curses.A_BOLD)
            stdscr.refresh()
            name_bytes = bytearray()
            while True:
                ch = stdscr.getch()
                if ch in (self._cfg.key_enter, self._cfg.key_carriage_return):
                    break
                if ch in (self._cfg.key_escape, self._cfg.key_ctrl_c):
                    name_bytes = bytearray()
                    break
                if ch in (curses.KEY_BACKSPACE, 127, 8):
                    if name_bytes:
                        name_bytes.pop()
                        stdscr.addnstr(prompt_y, 2, " " * (width - 12), width - 12, 0)
                        stdscr.addnstr(prompt_y, 2, f"New addon name: {name_bytes.decode('utf-8', 'replace')}", width - 12, curses.A_BOLD)
                elif 32 <= ch <= 126:
                    name_bytes.append(ch)
                stdscr.addnstr(prompt_y, 2, " " * (width - 12), width - 12, 0)
                stdscr.addnstr(prompt_y, 2, f"New addon name: {name_bytes.decode('utf-8', 'replace')}", width - 12, curses.A_BOLD)
                stdscr.refresh()
        except curses.error:
            pass
        curses.noecho()
        curses.curs_set(0)

        name = name_bytes.decode("utf-8", "replace").strip()
        if not name:
            return

        dest = LAZYADDONS_DIR / f"{name}.yaml"
        if dest.exists():
            return

        content = self._cfg.YAML_ADDON_TEMPLATE.format(name=name)
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
        except OSError:
            return

        self._registry.rescan(self._current_tab)
        self._current_tab = self._registry.tab_order()[0]

    def _init_colors(self) -> None:
        if not curses.has_colors():
            return
        try:
            curses.start_color()
            curses.use_default_colors()
        except curses.error:
            return
        default_bg = -1
        pairs = (
            (self._cfg.color_pair_border, self._cfg.color_border_fg, default_bg),
            (self._cfg.color_pair_title, self._cfg.color_title_fg, default_bg),
            (self._cfg.color_pair_help, self._cfg.color_help_fg, default_bg),
            (self._cfg.color_pair_row, self._cfg.color_row_fg, default_bg),
            (self._cfg.color_pair_selected, self._cfg.color_selected_fg, self._cfg.color_selected_bg),
            (self._cfg.color_pair_enabled, self._cfg.color_enabled_fg, default_bg),
            (self._cfg.color_pair_disabled, self._cfg.color_disabled_fg, default_bg),
            (self._cfg.color_pair_preview, self._cfg.color_preview_fg, default_bg),
            (self._cfg.color_pair_tab_active, self._cfg.color_tab_active_fg, self._cfg.color_tab_active_bg),
            (self._cfg.color_pair_tab_inactive, self._cfg.color_tab_inactive_fg, default_bg),
        )
        for pair_id, fg, bg in pairs:
            try:
                curses.init_pair(pair_id, fg, bg)
            except curses.error:
                continue

    def _render(self, stdscr: curses._CursesWindow, rows: list[AddonInfo], cursor: int, offset: int) -> None:
        cfg = self._cfg
        max_y, max_x = stdscr.getmaxyx()
        width = max(cfg.wizard_min_width, min(cfg.wizard_max_width, max_x))
        body_rows = max(len(rows), 1)
        height = min(max_y, body_rows + 10)
        top = 0
        left = max(0, (max_x - width) // 2)

        stdscr.erase()
        self._draw_frame(stdscr, top, left, height, width)
        self._draw_header(stdscr, top, left, width)
        self._draw_tabs(stdscr, top + 3, left, width)
        self._draw_column_headers(stdscr, top + 4, left, width, rows)

        body_top = top + 5
        view_height = height - 10
        if view_height < 2:
            view_height = 2

        if cursor < offset:
            offset = cursor
        elif cursor >= offset + view_height:
            offset = cursor - view_height + 1
        scroll_offset = max(0, min(offset, max(0, len(rows) - view_height)))
        self._scroll_offset[self._current_tab] = scroll_offset

        visible = rows[scroll_offset : scroll_offset + view_height]
        for v_idx, addon in enumerate(visible):
            real_idx = scroll_offset + v_idx
            self._draw_row(stdscr, body_top + v_idx, left, width, addon, real_idx == cursor)

        preview_top = body_top + view_height + 1
        if rows and 0 <= cursor < len(rows):
            self._draw_preview(stdscr, preview_top, left, width, rows[cursor])

        self._draw_summary(stdscr, preview_top + 5, left, width, rows)
        self._draw_footer(stdscr, top + height - 2, left, width)
        stdscr.refresh()

    def _draw_frame(self, stdscr, top: int, left: int, height: int, width: int) -> None:
        cfg = self._cfg
        attr = self._color(cfg.color_pair_border)
        horizontal = "═" * (width - 2)
        try:
            stdscr.addnstr(top, left, "╔" + horizontal + "╗", width, attr)
            for y in range(top + 1, top + height - 1):
                stdscr.addnstr(y, left, "║", 1, attr)
                stdscr.addnstr(y, left + width - 1, "║", 1, attr)
            stdscr.addnstr(top + 2, left, "╠" + horizontal + "╣", width, attr)
            stdscr.addnstr(top + height - 1, left, "╚" + horizontal + "╝", width, attr)
        except curses.error:
            pass

    def _draw_header(self, stdscr, top: int, left: int, width: int) -> None:
        cfg = self._cfg
        title_attr = self._color(cfg.color_pair_title) | curses.A_BOLD
        sub_attr = self._color(cfg.color_pair_help)
        try:
            stdscr.addnstr(
                top + 1, left + cfg.wizard_padding_x, cfg.wizard_title,
                width - cfg.wizard_padding_x * 2, title_attr,
            )
            subtitle_x = left + width - len(cfg.wizard_subtitle) - cfg.wizard_padding_x
            stdscr.addnstr(
                top + 1,
                max(subtitle_x, left + cfg.wizard_padding_x + len(cfg.wizard_title) + 2),
                cfg.wizard_subtitle,
                width - cfg.wizard_padding_x * 2,
                sub_attr,
            )
        except curses.error:
            pass

    def _draw_tabs(self, stdscr, row_y: int, left: int, width: int) -> None:
        cfg = self._cfg
        x = left + cfg.wizard_padding_x
        for tab in self._registry.tab_order():
            label_tab = self._registry.tab_label(tab)
            count = self._registry.tab_count(tab)
            label = f"  {label_tab} ({count})  "
            attr = (
                self._color(cfg.color_pair_tab_active) | curses.A_BOLD
                if tab == self._current_tab
                else self._color(cfg.color_pair_tab_inactive)
            )
            try:
                stdscr.addnstr(row_y, x, label, len(label), attr)
            except curses.error:
                return
            x += len(label) + 1

    def _draw_column_headers(self, stdscr, row_y: int, left: int, width: int, rows: list[AddonInfo]) -> None:
        cfg = self._cfg
        attr = self._color(cfg.color_pair_border) | curses.A_BOLD
        pad = cfg.wizard_padding_x
        header = f"{' ' * pad} {'#':>3}  {'Name':<{cfg.wizard_name_col}}  {'Status':<8}"
        try:
            stdscr.addnstr(row_y, left + pad, header, width - pad * 2, attr)
        except curses.error:
            pass

    def _draw_row(self, stdscr, row_y: int, left: int, width: int, addon: AddonInfo, selected: bool) -> None:
        cfg = self._cfg
        if selected:
            attr = self._color(cfg.color_pair_selected) | curses.A_BOLD
        elif addon.enabled:
            attr = self._color(cfg.color_pair_enabled)
        else:
            attr = self._color(cfg.color_pair_disabled)

        pointer = "▶" if selected else " "
        status = "[x] ON " if addon.enabled else "[ ] OFF"
        label = addon.name[: cfg.wizard_name_col].ljust(cfg.wizard_name_col)
        desc = (addon.description or "").replace("\n", " ")[:60]

        pad = cfg.wizard_padding_x
        text = f" {pointer}  {status}  {label}  {desc}"
        usable = width - pad * 2
        try:
            stdscr.addnstr(row_y, left + pad, " " * usable, usable, attr)
            stdscr.addnstr(row_y, left + pad, text, usable, attr)
        except curses.error:
            pass

    def _draw_preview(self, stdscr, top: int, left: int, width: int, addon: AddonInfo) -> None:
        cfg = self._cfg
        label_attr = self._color(cfg.color_pair_title) | curses.A_BOLD
        preview_attr = self._color(cfg.color_pair_preview)
        pad = cfg.wizard_padding_x
        usable = width - pad * 2

        try:
            stdscr.addnstr(top, left + pad, cfg.wizard_preview_label, usable, label_attr)
        except curses.error:
            pass

        detail_lines = [
            f"  Name:        {addon.name}",
            f"  Path:        {addon.path}",
            f"  Author:      {addon.author}",
            f"  Version:     {addon.version}",
            f"  Description: {addon.description}",
        ]
        if addon.category:
            detail_lines.insert(3, f"  Category:    {addon.category}")

        try:
            for offset, line in enumerate(detail_lines, 1):
                stdscr.addnstr(top + offset, left + pad, line, usable, preview_attr)
        except curses.error:
            pass

    def _draw_summary(self, stdscr, row_y: int, left: int, width: int, rows: list[AddonInfo]) -> None:
        cfg = self._cfg
        attr = self._color(cfg.color_pair_help)
        enabled_count = sum(1 for a in rows if a.enabled)
        disabled_count = len(rows) - enabled_count
        pad = cfg.wizard_padding_x
        text = f"  Total: {len(rows)}  |  Enabled: {enabled_count}  |  Disabled: {disabled_count}"
        try:
            stdscr.addnstr(row_y, left + pad, text, width - pad * 2, attr)
        except curses.error:
            pass

    def _draw_footer(self, stdscr, row_y: int, left: int, width: int) -> None:
        cfg = self._cfg
        attr = self._color(cfg.color_pair_help)
        try:
            stdscr.addnstr(row_y, left + cfg.wizard_padding_x, cfg.wizard_footer, width - cfg.wizard_padding_x * 2, attr)
        except curses.error:
            pass

    def _color(self, pair: int) -> int:
        if not curses.has_colors():
            return curses.A_NORMAL
        try:
            return curses.color_pair(pair)
        except curses.error:
            return curses.A_NORMAL


def configure_marketplace_interactive(
    config: MarketplaceConfig | None = None,
    start_tab: str = "",
) -> MarketplaceSettings | None:
    """Open the multi-tab curses wizard for marketplace management.

    Args:
        config: Optional custom configuration.
        start_tab: Optional tab pre-selection (\"lazyaddons\", \"plugins\",
            \"tools\", \"yara\", \"nuclei\").

    Returns ``None`` when the operator cancels or the environment cannot
    host a curses session.

    Returns:
        :class:`MarketplaceSettings` with the final state, or ``None``.
    """
    cfg = config or MarketplaceConfig()
    registry = AddonRegistry()
    initial = _build_initial_settings(registry)
    return MarketplaceConfigurator(cfg, registry, initial).run()


def _build_initial_settings(registry: AddonRegistry) -> MarketplaceSettings:
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
        on = sum(1 for a in addons if a.enabled)
        off = len(addons) - on
        parts.append(f"{reg.tab_label(tab)}: {on}(+{off})")
    return "  ".join(parts)
