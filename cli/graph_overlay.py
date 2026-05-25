"""Textual overlay over :mod:`cli.graph_advisor`.

The overlay visualises the same data ``god_nodes`` and ``neighbors``
already expose as text. The operator types a focus node, sees the
matching seed plus its neighbours grouped by hop, and switches between
"god nodes" (highest-degree) and "neighbors of <node>" modes from a
single screen.

Design (SOLID):

- Single Responsibility: :class:`GraphOverlayConfig` owns constants,
  :class:`GraphOverlayState` calls into :class:`GraphAdvisor` and
  normalises the results, :class:`GraphOverlayApp` renders.
- Open/Closed: a new view mode is one ``View`` enum entry plus one
  branch in :meth:`GraphOverlayState.snapshot`.
- Dependency Inversion: the state takes a callable that returns a
  :class:`GraphAdvisor`-shaped object so tests pass a fake.
- No magic numbers / hardcoded paths: every value lives in the config.
- Textual is imported lazily — :func:`launch_overlay` returns ``None``
  when Textual is missing or the graph is unavailable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Mapping, Sequence

from cli.themes import Theme, theme_from_payload


class GraphOverlayView(str, Enum):
    """Two view modes the overlay toggles between."""

    GOD_NODES = "god_nodes"
    NEIGHBORS = "neighbors"


@dataclass(frozen=True)
class GraphOverlayConfig:
    """Centralised constants for the overlay."""

    title: str = "Graph overlay"
    subtitle: str = "Tab to switch mode, type to focus, Esc to close"
    focus_placeholder: str = "Type a node id, label, or command verb"
    god_nodes_label: str = "Top central nodes"
    neighbors_label: str = "Neighbors"
    no_graph_message: str = "Graph not available — run /graphify . to enable."
    no_match_message: str = "No node matches the current focus."
    max_god_nodes: int = 20
    max_neighbors: int = 40
    neighbor_depth: int = 2
    summary_max_chars: int = 88
    truncation_suffix: str = "..."


@dataclass(frozen=True)
class GraphOverlayItem:
    """One render-ready row."""

    label: str
    node_id: str
    badge: str
    score: float


@dataclass
class GraphOverlayState:
    """Pure data layer for the overlay."""

    config: GraphOverlayConfig
    advisor_factory: Callable[[], Any]
    focus: str = ""
    view: GraphOverlayView = GraphOverlayView.GOD_NODES

    def is_available(self) -> bool:
        """Return ``True`` when the underlying graph advisor has data."""
        advisor = self._advisor()
        if advisor is None:
            return False
        try:
            return bool(advisor.is_available())
        except Exception:
            return False

    def set_focus(self, value: str) -> None:
        """Replace the focus query."""
        self.focus = (value or "").strip()
        if self.focus:
            self.view = GraphOverlayView.NEIGHBORS
        else:
            self.view = GraphOverlayView.GOD_NODES

    def toggle_view(self) -> None:
        """Switch between god-nodes and neighbors-of-focus."""
        if self.view is GraphOverlayView.GOD_NODES:
            self.view = GraphOverlayView.NEIGHBORS
        else:
            self.view = GraphOverlayView.GOD_NODES

    def snapshot(self) -> tuple[str, list[GraphOverlayItem]]:
        """Return ``(header, items)`` for the current view."""
        advisor = self._advisor()
        if advisor is None or not self.is_available():
            return self.config.no_graph_message, []
        if self.view is GraphOverlayView.GOD_NODES or not self.focus:
            return self._god_nodes(advisor)
        return self._neighbors(advisor)

    def _god_nodes(self, advisor: Any) -> tuple[str, list[GraphOverlayItem]]:
        try:
            ranked = advisor.god_nodes(limit=self.config.max_god_nodes) or []
        except Exception:
            return self.config.no_graph_message, []
        items = [self._row(row, badge="hub") for row in ranked]
        return self.config.god_nodes_label, items

    def _neighbors(self, advisor: Any) -> tuple[str, list[GraphOverlayItem]]:
        try:
            payload = advisor.neighbors(
                self.focus,
                depth=self.config.neighbor_depth,
                limit=self.config.max_neighbors,
            )
        except Exception:
            return self.config.no_graph_message, []
        if not isinstance(payload, Mapping):
            return self.config.no_graph_message, []
        if not payload.get("available", False):
            return self.config.no_graph_message, []
        matched = payload.get("matched")
        if matched is None:
            return self.config.no_match_message, []
        items: list[GraphOverlayItem] = [self._row(matched, badge="seed")]
        for entry in payload.get("neighbors", []) or []:
            if not isinstance(entry, Mapping):
                continue
            node = entry.get("node")
            if not isinstance(node, Mapping):
                continue
            badge = self._edge_badge(entry.get("edges"))
            items.append(self._row(node, badge=badge))
        header = f"{self.config.neighbors_label} of {matched.get('id') or matched.get('label') or self.focus}"
        return header, items

    def _row(self, payload: Mapping[str, Any], badge: str) -> GraphOverlayItem:
        node_id = str(payload.get("id") or payload.get("label") or "")
        label = self._truncate(str(payload.get("label") or node_id))
        score_raw = payload.get("score")
        if isinstance(score_raw, (int, float)):
            score = float(score_raw)
        elif isinstance(payload.get("degree"), (int, float)):
            score = float(payload["degree"])
        else:
            score = 0.0
        return GraphOverlayItem(label=label, node_id=node_id, badge=badge, score=score)

    def _edge_badge(self, edges: Any) -> str:
        if not isinstance(edges, list) or not edges:
            return "link"
        first = edges[0]
        if isinstance(first, Mapping):
            kind = first.get("kind") or first.get("type") or first.get("relation")
            if isinstance(kind, str) and kind.strip():
                return kind.strip()[:8]
        return "link"

    def _truncate(self, value: str) -> str:
        if len(value) <= self.config.summary_max_chars:
            return value
        keep = max(1, self.config.summary_max_chars - len(self.config.truncation_suffix))
        return value[:keep] + self.config.truncation_suffix

    def _advisor(self) -> Any | None:
        try:
            return self.advisor_factory()
        except Exception:
            return None


def _default_advisor_factory() -> Any | None:
    try:
        from cli.graph_advisor import GraphAdvisor
    except Exception:
        return None
    try:
        return GraphAdvisor.from_path()
    except Exception:
        return None


def build_state(
    config: GraphOverlayConfig | None = None,
    advisor_factory: Callable[[], Any] | None = None,
) -> GraphOverlayState:
    """Wire the canonical state used by :func:`launch_overlay`."""
    return GraphOverlayState(
        config=config or GraphOverlayConfig(),
        advisor_factory=advisor_factory or _default_advisor_factory,
    )


def launch_overlay(
    payload: Mapping[str, Any] | None = None,
    state: GraphOverlayState | None = None,
    runner: Any | None = None,
) -> str | None:
    """Open the overlay and return the last-focused node id on exit.

    Args:
        payload: Loaded ``payload.json``.
        state: Optional pre-built state.
        runner: Optional callable used by tests.

    Returns:
        The last focused node id, or ``None`` when cancelled / Textual
        unavailable.
    """
    chosen = state if state is not None else build_state()
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


def _build_app(state: GraphOverlayState, theme: Theme) -> Any | None:
    try:
        from textual.app import App, ComposeResult
        from textual.binding import Binding
        from textual.containers import Vertical
        from textual.widgets import Footer, Header, Input, ListItem, ListView, Static
    except Exception:
        return None

    cfg = state.config

    class _GraphOverlayApp(App):
        TITLE = cfg.title
        SUB_TITLE = cfg.subtitle
        BINDINGS = [
            Binding("escape", "close", "Close"),
            Binding("tab", "toggle_view", "Toggle view"),
        ]
        CSS = (
            "Screen { layout: vertical; }\n"
            "#focus-input { dock: top; height: 3; }\n"
            "#graph-header { padding: 0 1; color: $text-muted; }\n"
            "#graph-list { height: 1fr; }\n"
        )

        def __init__(self) -> None:
            super().__init__()
            self._state = state
            self._theme = theme

        def compose(self) -> ComposeResult:
            yield Header()
            yield Input(placeholder=cfg.focus_placeholder, id="focus-input")
            with Vertical(id="graph-body"):
                yield Static(cfg.god_nodes_label, id="graph-header")
                yield ListView(id="graph-list")
            yield Footer()

        def on_mount(self) -> None:
            self._refresh()

        def on_input_changed(self, event: Input.Changed) -> None:
            self._state.set_focus(event.value or "")
            self._refresh()

        def action_toggle_view(self) -> None:
            self._state.toggle_view()
            self._refresh()

        def action_close(self) -> None:
            self.exit(result=self._state.focus or None)

        def _refresh(self) -> None:
            header, items = self._state.snapshot()
            self.query_one("#graph-header", Static).update(header)
            list_view = self.query_one("#graph-list", ListView)
            list_view.clear()
            for item in items:
                marker = f"[{item.badge}]".ljust(8)
                row = f"{marker} {item.label}  ({item.score:.2f})"
                element = ListItem(Static(row))
                element.node_id = item.node_id
                list_view.append(element)

    return _GraphOverlayApp()


__all__ = [
    "GraphOverlayConfig",
    "GraphOverlayItem",
    "GraphOverlayState",
    "GraphOverlayView",
    "build_state",
    "launch_overlay",
]
