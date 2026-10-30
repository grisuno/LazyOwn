"""Policy planner signal contract: ranked categories become safe intents.

Every scenario states Given, When, Then. The singleton facade fails
soft; mapped categories emit registry-verb intents; unmapped categories
(still covered by the planner baseline) stay out of the proposal list.
"""

from __future__ import annotations

from pathlib import Path

from modules.lazy_loop import _policy_proposals, load_intel_scores


class _StubPolicy:
    """Policy facade stub returning curated rows."""

    def __init__(self, rows: list[dict]) -> None:
        """Bind rows."""
        self.rows = rows

    def get_recommendations(self, target: str) -> list[dict]:
        """Return the configured recommendations."""
        return list(self.rows)


def test_mapped_categories_emit_registry_verbs():
    """Given exploit and privesc rows, When proposing, Then auto intents land."""
    policy = _StubPolicy(
        [
            {"category": "exploit", "reason": "transition says next", "confidence": 0.8},
            {"category": "privesc", "reason": "post exploit", "confidence": 0.6},
        ]
    )
    out = _policy_proposals(policy, "10.0.0.9")
    assert out == ["auto auto_pwn 10.0.0.9", "auto autoblody 10.0.0.9"]


def test_unmapped_categories_are_skipped():
    """Given recon and other rows, When proposing, Then nothing lands."""
    policy = _StubPolicy(
        [
            {"category": "recon", "reason": "start", "confidence": 1.0},
            {"category": "other", "reason": "unknown", "confidence": 0.5},
        ]
    )
    assert _policy_proposals(policy, "10.0.0.9") == []


def test_duplicate_rows_dedupe():
    """Given two identical categories, When proposing, Then one intent."""
    policy = _StubPolicy(
        [
            {"category": "lateral", "reason": "pivot", "confidence": 0.7},
            {"category": "lateral", "reason": "again", "confidence": 0.7},
        ]
    )
    assert _policy_proposals(policy, "10.0.0.9") == ["auto autopivot 10.0.0.9"]


def test_policy_failure_degrades_to_empty():
    """Given a raising policy, When proposing, Then the list is empty."""
    class _Broken(_StubPolicy):
        """Policy raising on every call."""

        def get_recommendations(self, target: str) -> list[dict]:
            """Raise to simulate a broken episode store."""
            raise RuntimeError("store broken")

    assert _policy_proposals(_Broken([]), "10.0.0.9") == []


def test_load_intel_scores_fuses_host_scores(tmp_path: Path, monkeypatch):
    """Given a heat table, When fusing, Then it merges into the planner boost map."""
    import modules.lazy_loop as loop

    table = tmp_path / "lazy" / "host_scores.json"
    table.parent.mkdir(parents=True, exist_ok=True)
    table.write_text('{"ts": 0, "hosts": {"10.0.0.9": {"score": 61, "detail": []}}}', encoding="utf-8")
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path, raising=False)
    scores = loop.load_intel_scores()
    assert scores.get("10.0.0.9") >= 61.0
