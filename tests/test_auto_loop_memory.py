"""BDD tests for the auto-loop persistent memory and selector cascade."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules.auto_loop_memory import DecisionPersistence, FailureMemory
from modules.selector_manager import Proposal, select


class TestFailureMemory:
    """Failure counters and blocked bases survive restarts."""

    def test_counts_persist_across_reload(self, tmp_path: Path):
        """Given recorded failures, When a new instance loads the file, Then the count is durable."""
        story = "record failures -> reload -> count same"
        given = FailureMemory(tmp_path / "fails.json")
        given.record_failure("10.0.0.1", "enum", "gobuster -u x")
        given.record_failure("10.0.0.1", "enum", "gobuster -u x")
        when = FailureMemory(tmp_path / "fails.json")
        assert when.failure_count("10.0.0.1", "enum", "gobuster -u x") == 2, story

    def test_blocked_after_threshold_by_base(self, tmp_path: Path):
        """Given full-command failures on one verb, Then the base counts as blocked."""
        story = "two gobuster failures must block the gobuster base"
        mem = FailureMemory(tmp_path / "fails.json")
        mem.record_failure("t", "enum", "gobuster tbls")
        assert not mem.is_blocked("t", "gobuster"), story
        mem.record_failure("t", "enum", "gobuster tblx")
        assert mem.is_blocked("t", "gobuster"), story
        assert mem.blocked_bases("t") == {"gobuster"}, story

    def test_veto_blocks_immediately_and_persists(self, tmp_path: Path):
        """Given a stuck-loop veto, Then is_blocked holds after reload."""
        story = "veto must not depend on failure counts"
        one = FailureMemory(tmp_path / "fails.json")
        one.veto_base("t", "curl")
        two = FailureMemory(tmp_path / "fails.json")
        assert two.is_blocked("t", "curl"), story

    def test_trims_to_capacity(self, tmp_path: Path):
        """Given more distinct keys than the cap, Then the oldest are dropped."""
        story = "memory stays bounded"
        mem = FailureMemory(tmp_path / "fails.json")
        for idx in range(230):
            mem.record_failure("t", "c", f"cmd{idx}")
            mem._counts[f"t|c|cmd{idx}"]["last_ts"] = idx
        mem._trim()
        assert len(mem._counts) == 200, story

    def test_clear_target_forgets_records(self, tmp_path: Path):
        """Given failures on two targets, Then clearing one spares the other."""
        story = "manual reset is per-target"
        mem = FailureMemory(tmp_path / "fails.json")
        mem.record_failure("a", "c", "nmap")
        mem.record_failure("b", "c", "nmap")
        mem.clear_target("a")
        assert not mem.is_blocked("a", "nmap"), story
        assert mem.failure_count("b", "c", "nmap") == 1, story

    def test_invalid_key_raises(self, tmp_path: Path):
        """Given an empty command, Then recording raises instead of storing junk."""
        story = "empty identifiers must be rejected loudly"
        mem = FailureMemory(tmp_path / "fails.json")
        with pytest.raises(ValueError):
            mem.record_failure("t", "c", ""), story


class TestFailureMemorySanctioned:
    """Administrative view exposes past-threshold entries."""

    def test_sanctioned_lists_sorted_rows(self, tmp_path: Path):
        """Given two entries above threshold, Then sanctioned reports both with bases."""
        story = "the digest needs a readable blocked view"
        mem = FailureMemory(tmp_path / "fails.json")
        mem.record_failure("t", "enum", "gobuster a")
        mem.record_failure("t", "enum", "gobuster a")
        mem.record_failure("t", "lateral", "hydra b")
        mem.record_failure("t", "lateral", "hydra b")
        rows = mem.sanctioned_bases("t")
        assert [r["base"] for r in rows] == ["gobuster", "hydra"], story


class TestDecisionPersistence:
    """Reactive decisions parked across cycle boundaries."""

    def test_push_pop_round_trip(self, tmp_path: Path):
        """Given a pushed decision, When popped, Then it is consumed once."""
        story = "the backlog behaves like a single-shot queue"
        store = DecisionPersistence(tmp_path / "d.json")
        store.push("lazynuclei --x", reason="privesc hint")
        assert len(store) == 1, story
        decision = store.pop()
        assert decision is not None and decision.command == "lazynuclei --x", story
        assert store.pop() is None, story

    def test_newest_First_and_persisted(self, tmp_path: Path):
        """Given two pushes, Then peek gives newest and reload keeps the backlog."""
        story = "parking survives process restarts"
        store = DecisionPersistence(tmp_path / "d.json")
        store.push("first")
        store.push("second")
        assert store.peek().command == "second", story
        reloaded = DecisionPersistence(tmp_path / "d.json")
        assert len(reloaded) == 2, story
        assert reloaded.pop().command == "second", story

    def test_push_ignores_empty_and_caps(self, tmp_path: Path):
        """Given empty or overflowing pushes, Then no junk and bounded size."""
        story = "backlog of 64 decisions max"
        store = DecisionPersistence(tmp_path / "d.json")
        store.push("   ")
        assert len(store) == 0, story
        for idx in range(70):
            store.push(f"cmd{idx}")
        assert len(store) <= 64, story


class TestSelectorManager:
    """The cascade picks the highest-priority valid proposal."""

    def test_priority_order_wins(self):
        """Given varied priorities, Then the lowest priority number wins."""
        story = "low number means tried first"
        winner = select([Proposal("c", source="cat", priority=90), Proposal("a", source="react", priority=10)])
        assert winner.command == "a" and winner.source == "react", story

    def test_blocked_proposal_skipped_with_trace(self):
        """Given a blocked base and an unblocked fallback, Then the fallback wins with rejection trace."""
        story = "operators see why the reactive idea lost"
        blocked = {"lazynuclei"}
        out = select(
            [
                Proposal("lazynuclei --here", source="react", priority=1),
                Proposal("nmap -sV", source="bridge", priority=2),
            ],
            is_blocked=blocked.__contains__,
        )
        assert out.command == "nmap -sV", story
        assert "react" in out.rejected[0], story

    def test_all_blocked_returns_none(self):
        """Given everything blocked, Then None signals the higher-level fallback."""
        story = "cascade fails soft and honest"
        assert select([Proposal("a"), Proposal("b")], is_blocked=lambda b: True) is None

    def test_duplicates_deduped(self):
        """Given identical commands, Then only the best-priority instance wins."""
        story = "duplicates collapse deterministically on the top-priority proposal"
        out = select([Proposal("nmap sZ", source="parquet", priority=5), Proposal("nmap sZ", source="cat", priority=2)])
        assert out.source == "cat", story

    def test_empty_command_rejected(self):
        """Given an empty command, Then it is filtered with a trace."""
        story = "junk proposals must not win"
        out = select([Proposal("  ", source="llm", priority=1), Proposal("list", source="cat", priority=2)])
        assert out.command == "list", story
        assert "llm" in out.rejected[0], story
