"""Terminal renderer for the LazyOwn network surface graph.

This is the TUI counterpart of the ``vis.js`` graph rendered by
``templates/index.html``. It walks the :class:`~cli.surface_graph.SurfaceGraph`
that :class:`~cli.surface_graph.SurfaceGraphBuilder` assembled from
``sessions/`` and ``payload.json`` and offers three rendering modes so it
plugs into any operator workflow:

* :func:`render_static` — print a Rich tree once and return; ideal for the
  ``do_surface`` cmd2 command in non-interactive shells.
* :func:`launch_tui`    — open a full-screen Textual app with a navigable
  tree + detail pane (Q to quit, R to refresh).
* :func:`render_json`   — emit the graph as JSON for piping into other
  tools or feeding the MCP layer.

The module degrades cleanly when ``textual`` is missing: only the TUI
launcher requires it, and it raises a typed :class:`TextualNotInstalled`
that the caller can translate into an operator-friendly message.
"""

from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from cli.surface_graph import (
    NODE_C2,
    NODE_KIND_C2,
    NODE_KIND_CLIENT,
    NODE_KIND_HOST,
    NODE_KIND_PORT,
    NODE_KIND_SERVICE,
    SurfaceGraph,
    SurfaceNode,
    build_surface_graph,
)

KIND_STYLE: dict[str, str] = {
    NODE_KIND_C2: "bold magenta",
    NODE_KIND_CLIENT: "bold red",
    NODE_KIND_HOST: "bold cyan",
    NODE_KIND_PORT: "bold yellow",
    NODE_KIND_SERVICE: "green",
}

KIND_GLYPH: dict[str, str] = {
    NODE_KIND_C2: "[C2]",
    NODE_KIND_CLIENT: "[implant]",
    NODE_KIND_HOST: "[host]",
    NODE_KIND_PORT: "[port]",
    NODE_KIND_SERVICE: "[svc]",
}


class TextualNotInstalled(RuntimeError):
    """Raised when the optional ``textual`` dependency is unavailable."""


def render_static(
    graph: SurfaceGraph | None = None,
    sessions_dir: str = "sessions",
    payload_path: str = "payload.json",
    console: Console | None = None,
) -> SurfaceGraph:
    """Render the surface graph as a Rich tree and return it.

    Args:
        graph: Optional prebuilt graph. When ``None``, the function reads
            ``sessions_dir`` and ``payload_path`` to build one.
        sessions_dir: Path to the LazyOwn sessions directory.
        payload_path: Path to ``payload.json``.
        console: Optional Rich console; a new stdout console is created
            when ``None``.

    Returns:
        The :class:`SurfaceGraph` that was rendered (useful for tests).
    """
    resolved_graph = graph if graph is not None else build_surface_graph(sessions_dir, payload_path)
    console = console or Console(highlight=False, soft_wrap=True)
    tree = _build_rich_tree(resolved_graph)
    console.print(Panel.fit(tree, title="LazyOwn Network Surface", border_style="cyan"))
    console.print(_stats_table(resolved_graph))
    return resolved_graph


def render_json(
    graph: SurfaceGraph | None = None,
    sessions_dir: str = "sessions",
    payload_path: str = "payload.json",
) -> str:
    """Return the surface graph as a JSON string.

    Args:
        graph: Optional prebuilt graph; built on demand when ``None``.
        sessions_dir: Path to the LazyOwn sessions directory.
        payload_path: Path to ``payload.json``.

    Returns:
        A pretty-printed JSON document mirroring the dict returned by
        :meth:`SurfaceGraph.to_dict`.
    """
    resolved_graph = graph if graph is not None else build_surface_graph(sessions_dir, payload_path)
    return json.dumps(resolved_graph.to_dict(), indent=2, sort_keys=False)


def launch_tui(sessions_dir: str = "sessions", payload_path: str = "payload.json") -> None:
    """Open the full-screen Textual surface explorer.

    Args:
        sessions_dir: Path to the LazyOwn sessions directory.
        payload_path: Path to ``payload.json``.

    Raises:
        TextualNotInstalled: When the ``textual`` package is missing.
    """
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Horizontal
        from textual.widgets import Footer, Header, Static
        from textual.widgets import Tree as TextualTree
    except ImportError as exc:
        raise TextualNotInstalled("textual is not installed. Run: pip install textual") from exc

    class SurfaceExplorer(App):
        """Two-pane Textual app: surface tree + selected-node metadata."""

        TITLE = "LazyOwn Surface Graph"
        SUB_TITLE = "press Q to return to the shell"
        BINDINGS = [
            ("q", "quit", "Quit"),
            ("r", "refresh", "Refresh"),
            ("e", "expand_all", "Expand all"),
            ("c", "collapse_all", "Collapse all"),
        ]
        DEFAULT_CSS = """
        Screen { layout: vertical; }
        #body { layout: horizontal; height: 1fr; }
        #tree-pane { width: 60%; border: round $primary; padding: 0 1; }
        #detail-pane { width: 40%; border: round $accent; padding: 1 2; }
        """

        def __init__(self, sessions_dir: str, payload_path: str) -> None:
            super().__init__()
            self._sessions_dir = sessions_dir
            self._payload_path = payload_path
            self._graph: SurfaceGraph | None = None

        def compose(self) -> ComposeResult:
            yield Header()
            with Horizontal(id="body"):
                yield TextualTree("LazyOwn", id="tree-pane")
                yield Static("Select a node to see its details.", id="detail-pane")
            yield Footer()

        def on_mount(self) -> None:
            self._reload_graph()

        def action_refresh(self) -> None:
            self._reload_graph()
            self.notify("Refreshed.", timeout=1.5)

        def action_expand_all(self) -> None:
            tree_widget = self.query_one("#tree-pane", TextualTree)
            tree_widget.root.expand_all()

        def action_collapse_all(self) -> None:
            tree_widget = self.query_one("#tree-pane", TextualTree)
            tree_widget.root.collapse_all()

        def on_tree_node_selected(self, event: TextualTree.NodeSelected) -> None:  # type: ignore[name-defined]
            node = event.node
            data = getattr(node, "data", None)
            detail = self.query_one("#detail-pane", Static)
            if not isinstance(data, dict):
                detail.update("Select a host/port/implant node to see its details.")
                return
            detail.update(_render_node_detail(data))

        def _reload_graph(self) -> None:
            self._graph = build_surface_graph(self._sessions_dir, self._payload_path)
            tree_widget = self.query_one("#tree-pane", TextualTree)
            tree_widget.clear()
            root_node = self._graph.get(NODE_C2)
            if root_node is None:
                tree_widget.root.label = "(empty graph — no sessions/ artefacts)"
                return
            root_label = _styled_label(root_node)
            tree_widget.root.set_label(root_label)
            tree_widget.root.data = root_node.to_dict()
            tree_widget.root.expand()
            self._add_children(tree_widget.root, self._graph, root_node.id)
            stats = self._graph.stats()
            self.sub_title = (
                f"clients={stats.get(NODE_KIND_CLIENT, 0)} "
                f"hosts={stats.get(NODE_KIND_HOST, 0)} "
                f"ports={stats.get(NODE_KIND_PORT, 0)} (Q quits)"
            )

        def _add_children(self, parent_node: Any, graph: SurfaceGraph, parent_id: str) -> None:
            for child in graph.children_of(parent_id):
                node_view = parent_node.add(_styled_label(child), data=child.to_dict())
                node_view.expand()
                self._add_children(node_view, graph, child.id)

    SurfaceExplorer(sessions_dir=sessions_dir, payload_path=payload_path).run()


def _build_rich_tree(graph: SurfaceGraph) -> Tree:
    root = graph.get(NODE_C2)
    if root is None:
        return Tree("(empty graph — no sessions/ artefacts)")
    tree = Tree(_styled_label(root))
    _attach_children(tree, graph, root.id, set())
    return tree


def _attach_children(parent: Tree, graph: SurfaceGraph, parent_id: str, seen: set[str]) -> None:
    for child in graph.children_of(parent_id):
        if child.id in seen:
            continue
        seen.add(child.id)
        branch = parent.add(_styled_label(child))
        _attach_children(branch, graph, child.id, seen)


def _styled_label(node: SurfaceNode) -> Text:
    glyph = KIND_GLYPH.get(node.kind, "[?]")
    style = KIND_STYLE.get(node.kind, "white")
    text = Text()
    text.append(f"{glyph} ", style="dim cyan")
    text.append(node.label, style=style)
    return text


def _stats_table(graph: SurfaceGraph) -> Table:
    table = Table(title="Surface stats", expand=False)
    table.add_column("kind", style="bold cyan")
    table.add_column("count", justify="right")
    stats = graph.stats()
    ordering = (
        NODE_KIND_C2,
        NODE_KIND_CLIENT,
        NODE_KIND_HOST,
        NODE_KIND_PORT,
        NODE_KIND_SERVICE,
        "edges",
    )
    for key in ordering:
        if key in stats:
            table.add_row(key, str(stats[key]))
    return table


def _render_node_detail(data: dict[str, Any]) -> Text:
    text = Text()
    text.append(f"{data.get('label', '')}\n", style="bold cyan")
    text.append(f"id={data.get('id')}  kind={data.get('kind')}\n\n", style="dim white")
    metadata = data.get("metadata") or {}
    if not metadata:
        text.append("(no metadata)", style="dim italic")
        return text
    for key, value in metadata.items():
        text.append(f"  {key}: ", style="dim white")
        text.append(f"{value}\n", style="bold white")
    return text


__all__ = [
    "TextualNotInstalled",
    "launch_tui",
    "render_json",
    "render_static",
]
