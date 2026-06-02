"""Tests for the semantic context advisor in ``modules/reactive_engine.py``.

The advisor must:

* return an empty list when no RAG backend is available
* return an empty list when the operator disabled the feature via
  ``payload.json[reactive_semantic_enabled]``
* surface ``suggest_next`` decisions with priority
  :data:`SEMANTIC_PRIORITY` when the RAG yields useful hits
* never overrule the existing regex-based decisions
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest


_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.reactive_engine import (  # noqa: E402
    ReactiveDecision,
    ReactiveEngine,
    SEMANTIC_MIN_SCORE,
    SEMANTIC_MITRE_TACTIC,
    SEMANTIC_PRIORITY,
    SemanticContextAdvisor,
    SEMANTIC_PAYLOAD_KEY,
)


class _FakeRAG:
    """Stand-in for :class:`modules.session_rag.SessionRAG`."""

    def __init__(self, hits: List[Dict[str, Any]], ready: bool = True) -> None:
        self._hits = hits
        self._ready = ready
        self.queries: List[Dict[str, Any]] = []

    def query(self, text: str, n: int = 5) -> List[Dict[str, Any]]:
        self.queries.append({"text": text, "n": n})
        return list(self._hits)


def test_returns_empty_when_rag_unavailable() -> None:
    """No RAG instance means no semantic hints, never a crash."""

    advisor = SemanticContextAdvisor(rag=None)
    decisions = advisor.suggest("nothing", command="ls")
    assert decisions == []


def test_returns_empty_when_disabled_via_payload() -> None:
    """Honour the payload gate exactly once per call."""

    fake = _FakeRAG(hits=[{
        "text": "fake",
        "source": "logs/command_lazynmapoutputexample.txt",
        "score": 0.9,
    }])
    advisor = SemanticContextAdvisor(
        rag=fake,
        config_loader=lambda: {SEMANTIC_PAYLOAD_KEY: False},
    )
    assert advisor.suggest("anything", command="ls") == []
    assert fake.queries == []


def test_emits_priority_five_suggestion() -> None:
    """A high-score hit becomes a ``suggest_next`` decision."""

    fake = _FakeRAG(hits=[{
        "text": "open ports 22, 80, 443 ...",
        "source": "logs/command_lazynmapoutputtarget.htb.txt",
        "score": 0.91,
    }])
    advisor = SemanticContextAdvisor(rag=fake)
    decisions = advisor.suggest("similar nmap output", command="ls")
    assert len(decisions) == 1
    decision = decisions[0]
    assert isinstance(decision, ReactiveDecision)
    assert decision.action == "suggest_next"
    assert decision.command == "lazynmap"
    assert decision.priority == SEMANTIC_PRIORITY
    assert decision.mitre_tactic == SEMANTIC_MITRE_TACTIC
    assert "lazynmap" not in decision.reason or "score=" in decision.reason


def test_skips_low_score_hits() -> None:
    """Hits below :data:`SEMANTIC_MIN_SCORE` are dropped."""

    fake = _FakeRAG(hits=[{
        "text": "noise",
        "source": "logs/command_fakeoutput.txt",
        "score": SEMANTIC_MIN_SCORE - 0.1,
    }])
    advisor = SemanticContextAdvisor(rag=fake)
    assert advisor.suggest("noise output", command="ls") == []


def test_skips_same_command_and_dedupes() -> None:
    """Hits pointing back at the current command and duplicates are dropped."""

    fake = _FakeRAG(hits=[
        {
            "text": "self",
            "source": "logs/command_lsoutputt.txt",
            "score": 0.9,
        },
        {
            "text": "first sibling",
            "source": "logs/command_psoutputt.txt",
            "score": 0.9,
        },
        {
            "text": "duplicate",
            "source": "logs/command_psoutputu.txt",
            "score": 0.85,
        },
    ])
    advisor = SemanticContextAdvisor(rag=fake)
    decisions = advisor.suggest("dummy", command="ls")
    assert [d.command for d in decisions] == ["ps"]


def test_skips_hits_without_command_prefix() -> None:
    """Sources that do not match the ``command_<verb>output`` pattern are dropped."""

    fake = _FakeRAG(hits=[{
        "text": "random",
        "source": "loose_file.txt",
        "score": 0.9,
    }])
    advisor = SemanticContextAdvisor(rag=fake)
    assert advisor.suggest("dummy", command="ls") == []


def test_engine_uses_semantic_advisor_when_supplied() -> None:
    """The engine wires the advisor and includes its decisions."""

    fake = _FakeRAG(hits=[{
        "text": "rich snippet to embed in reason",
        "source": "logs/command_lazynmapoutputt.txt",
        "score": 0.72,
    }])
    advisor = SemanticContextAdvisor(rag=fake)
    engine = ReactiveEngine(semantic=advisor)
    decisions = engine.analyse(
        output="not matched by any regex matcher",
        command="ls",
        platform="linux",
    )
    actions = [d.action for d in decisions]
    assert "suggest_next" in actions
    semantic_first = [d for d in decisions if d.action == "suggest_next"][0]
    assert semantic_first.priority == SEMANTIC_PRIORITY
    higher_priority = [d for d in decisions if d.priority < SEMANTIC_PRIORITY]
    for d in higher_priority:
        assert decisions.index(d) <= decisions.index(semantic_first)


def test_advisor_swallows_rag_query_errors() -> None:
    """A noisy RAG backend never propagates exceptions to the caller."""

    class _ExplodingRAG:
        _ready = True

        def query(self, text: str, n: int = 5) -> List[Dict[str, Any]]:
            raise RuntimeError("boom")

    advisor = SemanticContextAdvisor(rag=_ExplodingRAG())
    assert advisor.suggest("anything", command="ls") == []
