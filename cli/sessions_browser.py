"""Textual browser for the LazyOwn ``sessions/`` directory.

The browser turns ``sessions/`` into a navigable surface so the operator
no longer needs to leave the shell to inspect credentials, hashes,
vulns, notes, or raw nmap output. Files are categorised, listed in a
left pane, and previewed in a right pane with bounded reads to keep the
TUI responsive on multi-megabyte transcripts.

Design (SOLID):

- Single Responsibility: :class:`SessionsBrowserConfig` owns constants,
  :class:`SessionEntry` is the immutable record, :class:`SessionsIndex`
  classifies files, :class:`SessionPreview` returns bounded text, and
  :class:`SessionsBrowserApp` renders.
- Open/Closed: a new category is one entry in
  :attr:`SessionsBrowserConfig.categories`.
- Dependency Inversion: the app is always constructed from a state
  object so tests exercise the data layer without Textual.
- No magic numbers / hardcoded paths: every value lives in the config.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cli.themes import Theme, theme_from_payload


@dataclass(frozen=True)
class CategorySpec:
    """One row in :attr:`SessionsBrowserConfig.categories`.

    Attributes:
        identifier: Stable lowercase identifier (``creds``, ``hashes``...).
        label: Human-readable header rendered in the tree.
        patterns: Glob expressions evaluated relative to the sessions
            root. The first matching pattern wins.
    """

    identifier: str
    label: str
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class SessionsBrowserConfig:
    """Centralised constants for the browser."""

    title: str = "Sessions browser"
    subtitle: str = "Tab to switch panes, / to filter, Esc to close"
    sessions_dir: str = "sessions"
    max_preview_bytes: int = 524_288
    max_entries_per_category: int = 250
    max_path_chars: int = 64
    truncation_suffix: str = "..."
    categories: tuple[CategorySpec, ...] = (
        CategorySpec("creds", "Credentials", ("credentials*.txt",)),
        CategorySpec("hashes", "Hashes", ("hash*.txt",)),
        CategorySpec("vulns", "Vulnerabilities", ("vulns_*.json", "vulns_*.nmap")),
        CategorySpec("scan", "Scans", ("scan_*.nmap", "scan_*.xml")),
        CategorySpec("notes", "Notes", ("notes.jsonl", "notes.txt", "sessionLazyOwn.json")),
        CategorySpec("events", "Events", ("events.jsonl", "autonomous_events.jsonl", "engagement_audit.jsonl")),
        CategorySpec("world", "World model", ("world_model.json", "tasks.json", "os.json")),
    )
    other_category_identifier: str = "other"
    other_category_label: str = "Other"
    other_excluded_filenames: tuple[str, ...] = (".toast_state.json",)
    binary_indicator: str = "(binary)"
    binary_byte_threshold: int = 32


@dataclass(frozen=True)
class SessionEntry:
    """Immutable description of a single file under ``sessions/``."""

    category: str
    label: str
    relative_path: str
    size_bytes: int


class SessionsIndex:
    """Classify files under the sessions root into operator-relevant buckets."""

    def __init__(self, config: SessionsBrowserConfig, root: Path | None = None) -> None:
        """Bind to config and resolve the sessions root.

        Args:
            config: Active configuration.
            root: Optional explicit root override; defaults to
                ``Path(config.sessions_dir)``.
        """
        self._config = config
        self._root = Path(root) if root is not None else Path(config.sessions_dir)

    @property
    def root(self) -> Path:
        """Return the resolved sessions root."""
        return self._root

    def categories(self) -> dict[str, list[SessionEntry]]:
        """Return a mapping ``category_identifier -> [SessionEntry, ...]``."""
        if not self._root.is_dir():
            return {}
        grouped: dict[str, list[SessionEntry]] = {}
        seen_paths: set[str] = set()
        for spec in self._config.categories:
            entries = self._entries_for(spec.patterns, spec)
            seen_paths.update(entry.relative_path for entry in entries)
            grouped[spec.identifier] = entries
        other = self._collect_other(seen_paths)
        if other:
            grouped[self._config.other_category_identifier] = other
        return grouped

    def _entries_for(
        self, patterns: Iterable[str], spec: CategorySpec
    ) -> list[SessionEntry]:
        seen: set[str] = set()
        collected: list[SessionEntry] = []
        for pattern in patterns:
            if not pattern or pattern.startswith("/") or ".." in pattern.split("/"):
                continue
            try:
                matches = list(self._root.glob(pattern))
            except OSError:
                continue
            for path in matches:
                if not path.is_file():
                    continue
                rel = self._relative(path)
                if rel in seen:
                    continue
                seen.add(rel)
                collected.append(self._build_entry(path, rel, spec.identifier))
                if len(collected) >= self._config.max_entries_per_category:
                    return collected
        collected.sort(key=lambda entry: entry.relative_path)
        return collected

    def _collect_other(self, claimed: set[str]) -> list[SessionEntry]:
        out: list[SessionEntry] = []
        try:
            for path in sorted(self._root.iterdir()):
                if not path.is_file():
                    continue
                if path.name in self._config.other_excluded_filenames:
                    continue
                rel = path.name
                if rel in claimed:
                    continue
                out.append(self._build_entry(path, rel, self._config.other_category_identifier))
                if len(out) >= self._config.max_entries_per_category:
                    break
        except OSError:
            return out
        return out

    def _build_entry(self, path: Path, relative: str, category: str) -> SessionEntry:
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        return SessionEntry(
            category=category,
            label=self._label(relative),
            relative_path=relative,
            size_bytes=size,
        )

    def _label(self, relative: str) -> str:
        if len(relative) <= self._config.max_path_chars:
            return relative
        keep = max(1, self._config.max_path_chars - len(self._config.truncation_suffix))
        return relative[:keep] + self._config.truncation_suffix

    def _relative(self, path: Path) -> str:
        try:
            return str(path.relative_to(self._root))
        except ValueError:
            return path.name


class SessionPreview:
    """Bounded text reader for the preview pane."""

    def __init__(self, config: SessionsBrowserConfig, root: Path | None = None) -> None:
        """Bind to config and the sessions root."""
        self._config = config
        self._root = Path(root) if root is not None else Path(config.sessions_dir)

    def read(self, relative: str) -> str:
        """Return ``relative`` as text, capped at ``max_preview_bytes``.

        Args:
            relative: Path fragment under the sessions root. ``..`` and
                absolute paths are rejected.

        Returns:
            UTF-8 decoded text. Files that appear binary (more than
            ``binary_byte_threshold`` NUL bytes in the head) return the
            configured binary indicator instead of garbled output.
        """
        if not relative or relative.startswith("/") or ".." in relative.replace("\\", "/").split("/"):
            return ""
        target = (self._root / relative).resolve()
        try:
            target.relative_to(self._root.resolve())
        except (OSError, ValueError):
            return ""
        if not target.is_file():
            return ""
        try:
            with target.open("rb") as handle:
                raw = handle.read(self._config.max_preview_bytes)
        except OSError:
            return ""
        if raw.count(b"\x00") > self._config.binary_byte_threshold:
            return self._config.binary_indicator
        return raw.decode("utf-8", errors="ignore")


@dataclass
class SessionsBrowserState:
    """Top-level state passed to the Textual app and to tests."""

    config: SessionsBrowserConfig
    index: SessionsIndex
    preview: SessionPreview
    filter_query: str = ""

    def grouped_entries(self) -> dict[str, list[SessionEntry]]:
        """Return classified entries, optionally filtered by :attr:`filter_query`."""
        groups = self.index.categories()
        if not self.filter_query:
            return groups
        needle = self.filter_query.lower()
        filtered: dict[str, list[SessionEntry]] = {}
        for identifier, entries in groups.items():
            matching = [
                entry
                for entry in entries
                if needle in entry.relative_path.lower() or needle in entry.label.lower()
            ]
            if matching:
                filtered[identifier] = matching
        return filtered

    def category_label(self, identifier: str) -> str:
        """Return the human-readable label for ``identifier``."""
        for spec in self.config.categories:
            if spec.identifier == identifier:
                return spec.label
        if identifier == self.config.other_category_identifier:
            return self.config.other_category_label
        return identifier


def build_state(
    payload: Mapping[str, Any] | None = None,
    sessions_dir: str | None = None,
    config: SessionsBrowserConfig | None = None,
) -> SessionsBrowserState:
    """Wire the canonical state used by :func:`launch_browser`.

    Args:
        payload: Loaded ``payload.json``. Currently unused beyond
            theme propagation but accepted for forward compatibility.
        sessions_dir: Optional override for the sessions root.
        config: Optional explicit :class:`SessionsBrowserConfig`.

    Returns:
        A fresh :class:`SessionsBrowserState`.
    """
    cfg = config or SessionsBrowserConfig()
    root = Path(sessions_dir) if sessions_dir and sessions_dir.strip() else Path(cfg.sessions_dir)
    index = SessionsIndex(cfg, root=root)
    preview = SessionPreview(cfg, root=root)
    return SessionsBrowserState(config=cfg, index=index, preview=preview)


def launch_browser(
    payload: Mapping[str, Any] | None = None,
    state: SessionsBrowserState | None = None,
    runner: Any | None = None,
) -> str | None:
    """Open the Textual browser and return the last-viewed relative path.

    Args:
        payload: Loaded ``payload.json``.
        state: Optional pre-built state (tests inject one).
        runner: Optional callable used by tests instead of running the
            real Textual app.

    Returns:
        The relative path of the last file the operator inspected, or
        ``None`` when the browser was cancelled or Textual is missing.
    """
    chosen = state if state is not None else build_state(payload)
    theme = theme_from_payload(payload)
    if runner is not None:
        return runner({"state": chosen, "theme": theme})
    app = _build_app(chosen, theme)
    if app is None:
        return None
    try:
        result = app.run()
    except Exception:
        return None
    if isinstance(result, str) and result:
        return result
    return None


def _build_app(state: SessionsBrowserState, theme: Theme) -> Any | None:
    try:
        from textual.app import App, ComposeResult
        from textual.binding import Binding
        from textual.containers import Horizontal, Vertical
        from textual.widgets import Footer, Header, Input, Static, Tree
    except Exception:
        return None

    cfg = state.config

    class _SessionsBrowserApp(App):
        TITLE = cfg.title
        SUB_TITLE = cfg.subtitle
        BINDINGS = [
            Binding("escape", "close", "Close"),
            Binding("ctrl+r", "refresh", "Refresh"),
        ]
        CSS = (
            "Screen { layout: vertical; }\n"
            "#filter-input { dock: top; height: 3; }\n"
            "#browser-body { layout: horizontal; height: 1fr; }\n"
            "#tree-pane { width: 40%; min-width: 28; border: round $primary; }\n"
            "#preview-pane { width: 1fr; border: round $accent; padding: 0 1; }\n"
        )

        def __init__(self) -> None:
            super().__init__()
            self._state = state
            self._theme = theme
            self._selected: str | None = None

        def compose(self) -> ComposeResult:
            yield Header()
            yield Input(placeholder="Filter (substring on path)", id="filter-input")
            with Horizontal(id="browser-body"):
                with Vertical(id="tree-pane"):
                    yield Tree(cfg.sessions_dir, id="sessions-tree")
                with Vertical(id="preview-pane"):
                    yield Static("(select a file)", id="preview")
            yield Footer()

        def on_mount(self) -> None:
            self._rebuild_tree()

        def on_input_changed(self, event: Input.Changed) -> None:
            self._state.filter_query = (event.value or "").strip()
            self._rebuild_tree()

        def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
            data = event.node.data
            if isinstance(data, dict):
                relative = data.get("relative_path")
                if isinstance(relative, str) and relative:
                    self._show_preview(relative)

        def action_refresh(self) -> None:
            self._rebuild_tree()

        def action_close(self) -> None:
            self.exit(result=self._selected)

        def _rebuild_tree(self) -> None:
            tree = self.query_one("#sessions-tree", Tree)
            tree.clear()
            grouped = self._state.grouped_entries()
            for spec in cfg.categories:
                entries = grouped.get(spec.identifier, [])
                if not entries:
                    continue
                branch = tree.root.add(f"{spec.label} ({len(entries)})", expand=True)
                for entry in entries:
                    branch.add_leaf(
                        f"{entry.label}  [{entry.size_bytes}b]",
                        data={"relative_path": entry.relative_path},
                    )
            other = grouped.get(cfg.other_category_identifier, [])
            if other:
                branch = tree.root.add(f"{cfg.other_category_label} ({len(other)})", expand=False)
                for entry in other:
                    branch.add_leaf(
                        f"{entry.label}  [{entry.size_bytes}b]",
                        data={"relative_path": entry.relative_path},
                    )

        def _show_preview(self, relative: str) -> None:
            self._selected = relative
            content = self._state.preview.read(relative) or "(empty)"
            preview = self.query_one("#preview", Static)
            preview.update(content)

    return _SessionsBrowserApp()


__all__ = [
    "CategorySpec",
    "SessionEntry",
    "SessionPreview",
    "SessionsBrowserConfig",
    "SessionsBrowserState",
    "SessionsIndex",
    "build_state",
    "launch_browser",
]
