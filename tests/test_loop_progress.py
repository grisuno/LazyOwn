"""Loop milestone panel: inferred stage states stay honest."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.loop_progress import (  # noqa: E402
    CHAIN_STAGES,
    LoopProgress,
    LoopSnapshot,
    snap_to_states,
    snapshot_from_overview,
)


def _overview(**over) -> dict:
    """Minimal overview dict as ExplorationGraph.overview returns it."""
    base = {"goals": [], "intents": [], "pending": [], "facts": 0,
            "findings": 0, "hints": [], "nodes": 0, "edges": 0, "anchors": 0}
    base.update(over)
    return base


def test_chain_has_fourteen_stages() -> None:
    """Milestones mirror the orchestrator chain one to one."""
    assert len(CHAIN_STAGES) == 14
    assert CHAIN_STAGES[0] == "lazy_task" and CHAIN_STAGES[-1] == "lazy_report"


def test_fresh_task_shows_first_stage_current() -> None:
    """Empty overview: task done (exists), scope current, rest pending."""
    snap = snapshot_from_overview(_overview(), {"status": "running", "scope": []})
    states = snap_to_states(snap)
    assert states["lazy_task"] == "done"
    assert all(v == "pending" for k, v in states.items() if k != "lazy_task")
    current = next(s for s in CHAIN_STAGES if states[s] != "done")
    assert current == "lazy_scope"


def test_progress_advances_with_evidence() -> None:
    """Facts flip enrich/worker/guard/traffic; findings flip the finding leg."""
    snap = snapshot_from_overview(
        _overview(facts=2, findings=1, anchors=1,
                  intents=[{"id": 1, "state": "done", "text": "x", "priority": 5}]),
        {"status": "running", "scope": [{"kind": "ip", "value": "10.0.0.1"}]})
    states = snap_to_states(snap)
    for stage in ("lazy_scope", "lazy_asset", "lazy_enrich", "lazy_planner",
                  "lazy_worker", "lazy_guard", "lazy_traffic", "lazy_finding",
                  "lazy_trace"):
        assert states[stage] == "done", stage
    assert states["lazy_report"] == "pending"


def test_finished_task_all_green() -> None:
    """Done status closes compact and report too."""
    snap = snapshot_from_overview(
        _overview(facts=1, findings=1, anchors=1,
                  intents=[{"id": 1, "state": "done", "text": "x", "priority": 5}],
                  goals=[{"id": 1, "state": "done", "text": "g"}]),
        {"status": "done", "scope": [{"kind": "ip", "value": "10.0.0.1"}]})
    states = snap_to_states(snap)
    assert all(v == "done" for v in states.values())


def test_snapshot_counts_intent_states() -> None:
    """Intent buckets split pending/open/done for the footer."""
    snap = snapshot_from_overview(_overview(intents=[
        {"id": 1, "state": "pending", "text": "a", "priority": 5},
        {"id": 2, "state": "open", "text": "b", "priority": 5},
        {"id": 3, "state": "running", "text": "c", "priority": 5},
        {"id": 4, "state": "done", "text": "d", "priority": 5}]), {})
    assert (snap.intents_pending, snap.intents_open, snap.intents_done) == (1, 2, 1)


def test_panel_renders_without_live() -> None:
    """Panel builds for empty and full snapshots (no terminal needed)."""
    progress = LoopProgress(goal="gain access", target="10.0.0.1")
    panel = progress._render(LoopSnapshot())
    assert panel is not None
    full = snapshot_from_overview(_overview(facts=3, findings=1), {"status": "done"})
    assert progress._render(full) is not None


def test_render_contains_no_markup_strings() -> None:
    """Cells are Text objects: literal [green] tags can never leak."""
    import io

    from rich.console import Console

    progress = LoopProgress(goal="gain access [brackets] test", target="10.0.0.1")
    stream = io.StringIO()
    console = Console(file=stream, width=100, highlight=False, soft_wrap=True)
    progress._console = console
    console.print(progress._render(LoopSnapshot()))
    out = stream.getvalue()
    assert "[green]" not in out and "[/]" not in out
    assert "task" in out and "report" in out


def test_line_mode_prints_only_on_stage_change(capsys) -> None:
    """Non-terminal sinks get one line per milestone, never full redraws."""
    import io

    from rich.console import Console

    stream = io.StringIO()
    progress = LoopProgress(goal="g", target="t")
    progress._console = Console(file=stream, width=100, highlight=False)
    assert progress.live_mode is False
    progress.start()
    snap = snapshot_from_overview(_overview(), {"status": "running", "scope": []})
    progress.refresh(snap)
    progress.refresh(snap)
    progress.refresh(snap)
    first = stream.getvalue()
    assert first.count("now:") == 1
    progress.stop()
    assert "task" in stream.getvalue()
    capsys.readouterr()


def test_sanitize_line_strips_ansi_and_cr() -> None:
    """Transcript lines lose escape codes and carriage returns."""
    from modules.loop_progress import sanitize_line

    assert sanitize_line("\x1b[32mhi\x1b[0m\r\n") == "hi"
    assert sanitize_line("[timeout] curl http://x/") == "[timeout] curl http://x/"
