"""Tests for cli/graph_overlay.py.

Exercises the data layer using a hand-rolled fake advisor that mirrors
the contract of :class:`cli.graph_advisor.GraphAdvisor`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.graph_overlay import (  # noqa: E402
    GraphOverlayConfig,
    GraphOverlayState,
    GraphOverlayView,
    build_state,
    launch_overlay,
)


class _FakeAdvisor:
    def __init__(self, available: bool = True) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def god_nodes(self, limit: int | None = None) -> list[dict[str, Any]]:
        rows = [
            {"id": "ping", "label": "ping", "degree": 12},
            {"id": "lazynmap", "label": "lazynmap", "degree": 8},
        ]
        return rows if limit is None else rows[:limit]

    def neighbors(self, query: str, depth: int | None = None, limit: int | None = None) -> dict[str, Any]:
        if query.startswith("missing"):
            return {"available": True, "matched": None, "neighbors": []}
        return {
            "available": True,
            "matched": {"id": query, "label": query, "score": 1.0},
            "neighbors": [
                {
                    "from": query,
                    "node": {"id": "lazynmap", "label": "lazynmap", "score": 0.5},
                    "edges": [{"kind": "calls"}],
                }
            ],
        }


def test_is_available_returns_false_when_advisor_missing() -> None:
    """``None`` from the factory marks the overlay as unavailable."""
    state = GraphOverlayState(config=GraphOverlayConfig(), advisor_factory=lambda: None)
    assert state.is_available() is False


def test_god_nodes_view_returns_hubs() -> None:
    """The default view emits the configured god-nodes."""
    state = GraphOverlayState(
        config=GraphOverlayConfig(),
        advisor_factory=lambda: _FakeAdvisor(),
    )
    header, items = state.snapshot()
    assert header == GraphOverlayConfig().god_nodes_label
    assert [item.node_id for item in items] == ["ping", "lazynmap"]


def test_focus_switches_to_neighbors_view() -> None:
    """Typing a focus query auto-switches the view."""
    state = GraphOverlayState(
        config=GraphOverlayConfig(),
        advisor_factory=lambda: _FakeAdvisor(),
    )
    state.set_focus("ping")
    assert state.view is GraphOverlayView.NEIGHBORS
    header, items = state.snapshot()
    assert "ping" in header
    assert [item.badge for item in items] == ["seed", "calls"]


def test_focus_unknown_returns_no_match_message() -> None:
    """A focus that does not match any node returns the configured message."""
    state = GraphOverlayState(
        config=GraphOverlayConfig(),
        advisor_factory=lambda: _FakeAdvisor(),
    )
    state.set_focus("missing-node")
    header, items = state.snapshot()
    assert header == GraphOverlayConfig().no_match_message
    assert items == []


def test_unavailable_advisor_returns_no_graph_message() -> None:
    """When the advisor reports unavailable the overlay falls back."""
    state = GraphOverlayState(
        config=GraphOverlayConfig(),
        advisor_factory=lambda: _FakeAdvisor(available=False),
    )
    header, items = state.snapshot()
    assert header == GraphOverlayConfig().no_graph_message
    assert items == []


def test_toggle_view_round_trip() -> None:
    """Toggle alternates between god-nodes and neighbors."""
    state = GraphOverlayState(
        config=GraphOverlayConfig(),
        advisor_factory=lambda: _FakeAdvisor(),
    )
    state.set_focus("ping")
    initial = state.view
    state.toggle_view()
    assert state.view is not initial
    state.toggle_view()
    assert state.view is initial


def test_launch_overlay_uses_runner() -> None:
    """The runner override bypasses Textual and returns its value."""
    state = GraphOverlayState(
        config=GraphOverlayConfig(),
        advisor_factory=lambda: _FakeAdvisor(),
    )

    def runner(context):
        return "ping"

    assert launch_overlay(state=state, runner=runner) == "ping"


def test_build_state_uses_default_factory_signature() -> None:
    """The factory accepts no arguments and returns a state instance."""
    state = build_state(advisor_factory=lambda: None)
    assert isinstance(state, GraphOverlayState)
    assert state.is_available() is False
