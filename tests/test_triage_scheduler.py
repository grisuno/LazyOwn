"""Difficulty-triage scheduler BDD contract.

Given queued targets, When the scheduler orders them, Then easy targets drain
first, partials are salvaged near a deadline, and unproductive targets trip the
stop-loss. The scheduler is pure, so every scenario is a direct assertion.
"""

from __future__ import annotations

from modules.loop.triage_scheduler import TriageScheduler, estimate_difficulty


def test_estimate_difficulty_scales_with_surface():
    """Given more ports and services, When estimated, Then difficulty rises."""
    small = estimate_difficulty({"open_ports": 1, "services": ["http"]})
    large = estimate_difficulty({"open_ports": 12, "services": ["http", "smb", "ssh", "ftp"]})
    assert 0.0 <= small < large <= 1.0


def test_estimate_difficulty_accepts_counts_or_collections():
    """Given int or list surface facts, When estimated, Then both are handled."""
    by_count = estimate_difficulty({"open_ports": 6, "services": 0})
    by_list = estimate_difficulty({"open_ports": [1, 2, 3, 4, 5, 6], "services": []})
    assert by_count == by_list


def test_order_is_easy_first():
    """Given mixed difficulty, When ordered, Then the easiest drains first."""
    records = [
        {"task_id": "hard", "difficulty": 0.9},
        {"task_id": "easy", "difficulty": 0.1},
        {"task_id": "mid", "difficulty": 0.5},
    ]
    order = [r["task_id"] for r in TriageScheduler().order(records)]
    assert order == ["easy", "mid", "hard"]


def test_order_breaks_ties_by_progress_then_arrival():
    """Given equal difficulty, When ordered, Then more progress goes first."""
    records = [
        {"task_id": "a", "difficulty": 0.5, "progress": 0.1, "queued_at": 2.0},
        {"task_id": "b", "difficulty": 0.5, "progress": 0.8, "queued_at": 3.0},
        {"task_id": "c", "difficulty": 0.5, "progress": 0.1, "queued_at": 1.0},
    ]
    order = [r["task_id"] for r in TriageScheduler().order(records)]
    assert order == ["b", "c", "a"]


def test_deadline_salvages_partials_first():
    """Given a near deadline, When ordered, Then salvageable partials lead."""
    records = [
        {"task_id": "easy_fresh", "difficulty": 0.1, "progress": 0.0, "partial": False},
        {"task_id": "hard_partial", "difficulty": 0.95, "progress": 0.7, "partial": True},
    ]
    order = [r["task_id"] for r in TriageScheduler().order(records, deadline_near=True)]
    assert order[0] == "hard_partial"


def test_deadline_ignores_partials_below_salvage_threshold():
    """Given a weak partial, When deadline-ordered, Then it is not floated."""
    sched = TriageScheduler(salvage_progress=0.3)
    records = [
        {"task_id": "easy", "difficulty": 0.1, "progress": 0.0, "partial": False},
        {"task_id": "weak_partial", "difficulty": 0.9, "progress": 0.05, "partial": True},
    ]
    order = [r["task_id"] for r in sched.order(records, deadline_near=True)]
    assert order[0] == "easy"


def test_stop_loss_triggers_on_attempts_without_progress():
    """Given exhausted attempts and no progress, When checked, Then stop."""
    sched = TriageScheduler(stop_loss_attempts=3)
    assert sched.should_stop({"task_id": "x", "attempts": 3, "progress": 0.0}) is True
    assert sched.should_stop({"task_id": "x", "attempts": 3, "progress": 0.4}) is False
    assert sched.should_stop({"task_id": "x", "attempts": 2, "progress": 0.0}) is False


def test_route_splits_hard_and_easy():
    """Given difficulty, When routed, Then hard goes to general, easy soldier."""
    sched = TriageScheduler(hard_threshold=0.6)
    assert sched.route({"difficulty": 0.9}) == "general"
    assert sched.route({"difficulty": 0.2}) == "soldier"


def test_pick_next_returns_none_when_empty():
    """Given an empty queue, When picking, Then None is returned."""
    assert TriageScheduler().pick_next([]) is None
