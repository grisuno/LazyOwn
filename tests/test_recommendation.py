"""Behaviour tests for the unified recommendation engine and its signals.

These tests pin the fusion contract before any consumer is rewired onto the
engine: per-signal normalisation, category-prior boosting, cross-signal merge
with provenance, deterministic ordering, standalone category surfacing, and
graceful degradation when a signal raises.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cli.recommendation import (
    KIND_CATEGORY,
    KIND_COMMAND,
    CategoryResolver,
    EngineWeights,
    Proposal,
    Recommendation,
    RecommendationContext,
    RecommendationEngine,
)
from cli.recommendation_signals import (
    GraphSignal,
    KillChainSignal,
    PolicySignal,
    ReconPlanSignal,
    build_context,
    build_default_engine,
    read_recent_commands,
)


def _ctx(limit: int = 5, recent: list[str] | None = None, phase: str = "recon") -> RecommendationContext:
    return RecommendationContext(
        target="10.10.10.1",
        payload={"rhost": "10.10.10.1"},
        recent_commands=recent or [],
        phase=phase,
        limit=limit,
    )


class _StubSignal:
    def __init__(self, name: str, proposals: list[Proposal]) -> None:
        self.name = name
        self._proposals = proposals

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        return self._proposals


class _BoomSignal:
    name = "boom"

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        raise RuntimeError("backend down")


def _engine(signals, resolver=None, weights=None) -> RecommendationEngine:
    return RecommendationEngine(
        signals=signals,
        resolver=resolver or CategoryResolver(loader=lambda _p: {}),
        weights=weights,
    )


class TestFusionCore:
    def test_single_signal_normalises_to_peak(self) -> None:
        signal = _StubSignal(
            "graph",
            [
                Proposal("a", KIND_COMMAND, 10.0, "r"),
                Proposal("b", KIND_COMMAND, 5.0, "r"),
            ],
        )
        weights = EngineWeights(signal_weights={"graph": 1.0})
        recs = _engine([signal], weights=weights).recommend(_ctx())
        by_action = {r.action: r for r in recs}
        assert by_action["a"].score == pytest.approx(1.0)
        assert by_action["b"].score == pytest.approx(0.5)

    def test_cross_signal_merge_sums_and_records_provenance(self) -> None:
        graph = _StubSignal("graph", [Proposal("gobuster", KIND_COMMAND, 1.0, "near")])
        recon = _StubSignal("recon", [Proposal("gobuster", KIND_COMMAND, 1.0, "http open")])
        weights = EngineWeights(signal_weights={"graph": 0.6, "recon": 1.0})
        recs = _engine([graph, recon], weights=weights).recommend(_ctx())
        assert len(recs) == 1
        merged = recs[0]
        assert merged.action == "gobuster"
        assert merged.score == pytest.approx(1.6)
        assert set(merged.sources) == {"graph", "recon"}
        assert any("near" in r for r in merged.reasons)
        assert any("http open" in r for r in merged.reasons)

    def test_category_prior_boosts_matching_action(self) -> None:
        resolver = CategoryResolver(loader=lambda _p: {"category_to_commands": {"privesc": ["linpeas"]}})
        concrete = _StubSignal("graph", [Proposal("linpeas", KIND_COMMAND, 1.0, "r")])
        hot_policy = _StubSignal("policy", [Proposal("privesc", KIND_CATEGORY, 1.0, "do privesc")])
        weights = EngineWeights(
            signal_weights={"graph": 1.0},
            category_prior_floor=0.6,
            category_prior_span=0.8,
        )
        boosted = _engine([concrete, hot_policy], resolver, weights).recommend(_ctx())
        cold = _engine([concrete], resolver, weights).recommend(_ctx())
        boosted_score = next(r.score for r in boosted if r.action == "linpeas")
        cold_score = next(r.score for r in cold if r.action == "linpeas")
        assert boosted_score == pytest.approx(1.4)
        assert cold_score == pytest.approx(1.0)
        assert boosted_score > cold_score

    def test_uncovered_category_surfaces_as_recommendation(self) -> None:
        policy = _StubSignal("policy", [Proposal("lateral", KIND_CATEGORY, 0.8, "pivot now")])
        recs = _engine([policy]).recommend(_ctx())
        assert len(recs) == 1
        assert recs[0].kind == KIND_CATEGORY
        assert recs[0].action == "lateral"
        assert recs[0].sources == ("policy",)

    def test_covered_category_not_duplicated_as_standalone(self) -> None:
        resolver = CategoryResolver(loader=lambda _p: {"category_to_commands": {"privesc": ["linpeas"]}})
        concrete = _StubSignal("graph", [Proposal("linpeas", KIND_COMMAND, 1.0, "r")])
        policy = _StubSignal("policy", [Proposal("privesc", KIND_CATEGORY, 1.0, "do privesc")])
        recs = _engine([concrete, policy], resolver, EngineWeights(signal_weights={"graph": 1.0})).recommend(_ctx())
        kinds = {r.action: r.kind for r in recs}
        assert kinds == {"linpeas": KIND_COMMAND}

    def test_deterministic_ordering_on_score_tie(self) -> None:
        signal = _StubSignal(
            "graph",
            [Proposal("zeta", KIND_COMMAND, 1.0, "r"), Proposal("alpha", KIND_COMMAND, 1.0, "r")],
        )
        recs = _engine([signal], weights=EngineWeights(signal_weights={"graph": 1.0})).recommend(_ctx())
        assert [r.action for r in recs] == ["alpha", "zeta"]

    def test_limit_is_honoured(self) -> None:
        signal = _StubSignal(
            "graph",
            [Proposal(f"cmd{i}", KIND_COMMAND, float(10 - i), "r") for i in range(8)],
        )
        recs = _engine([signal], weights=EngineWeights(signal_weights={"graph": 1.0})).recommend(_ctx(limit=3))
        assert len(recs) == 3

    def test_failing_signal_is_isolated(self) -> None:
        good = _StubSignal("graph", [Proposal("safe", KIND_COMMAND, 1.0, "r")])
        recs = _engine([_BoomSignal(), good], weights=EngineWeights(signal_weights={"graph": 1.0})).recommend(_ctx())
        assert [r.action for r in recs] == ["safe"]

    def test_zero_weight_signal_contributes_nothing(self) -> None:
        signal = _StubSignal("graph", [Proposal("x", KIND_COMMAND, 1.0, "r")])
        recs = _engine([signal], weights=EngineWeights(signal_weights={})).recommend(_ctx())
        assert recs == []


class TestAdapters:
    def test_graph_signal_extracts_label_and_score(self) -> None:
        class _Advisor:
            def suggest_next(self, recent_commands, limit):
                return [{"label": "ffuf", "score": 3.0}, {"id": "nikto", "score": 1.0}]

        proposals = GraphSignal(_Advisor()).propose(_ctx())
        assert [(p.action, p.weight) for p in proposals] == [("ffuf", 3.0), ("nikto", 1.0)]

    def test_policy_signal_emits_categories(self) -> None:
        class _Policy:
            def get_recommendations(self, target):
                return [{"category": "privesc", "confidence": 0.7, "reason": "go up"}]

        proposals = PolicySignal(_Policy()).propose(_ctx())
        assert proposals[0].kind == KIND_CATEGORY
        assert proposals[0].action == "privesc"
        assert proposals[0].weight == pytest.approx(0.7)

    def test_recon_signal_maps_items_with_descending_weight(self) -> None:
        class _Item:
            def __init__(self, kind, name, reason):
                self.kind = kind
                self.name = name
                self.reason = reason
                self.command_preview = f"run {name}"

        class _Plan:
            items = (_Item("addon", "smbmap", "smb open"), _Item("tool", "nikto", "http open"))

        def _builder(target, engine, payload):
            return _Plan()

        proposals = ReconPlanSignal(engine=object(), builder=_builder).propose(_ctx())
        assert [p.action for p in proposals] == ["smbmap", "nikto"]
        assert proposals[0].weight > proposals[1].weight
        assert proposals[0].command_preview == "run smbmap"

    def test_killchain_signal_uses_adjacency_then_phase(self) -> None:
        signal = KillChainSignal(
            next_table={"lazynmap": ["gobuster", "ffuf"]},
            phase_table={"enum": ["enum4linux", "nikto"]},
        )
        proposals = signal.propose(_ctx(recent=["lazynmap"], phase="enum"))
        actions = [p.action for p in proposals]
        assert actions[:2] == ["gobuster", "ffuf"]
        assert "enum4linux" in actions

    def test_killchain_signal_filters_already_run(self) -> None:
        signal = KillChainSignal(
            next_table={"lazynmap": ["gobuster"]},
            phase_table={"recon": ["lazynmap", "ping"]},
        )
        proposals = signal.propose(_ctx(recent=["lazynmap", "gobuster"]))
        assert "gobuster" not in [p.action for p in proposals]
        assert "lazynmap" not in [p.action for p in proposals]


class TestContextAndFactory:
    def test_read_recent_commands_orders_and_windows(self, tmp_path: Path) -> None:
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        (sessions / "LazyOwn_session_report.csv").write_text(
            "command\nping 10.0.0.1\nlazynmap\ngobuster dir\n", encoding="utf-8"
        )
        verbs = read_recent_commands(str(sessions))
        assert verbs == ["ping", "lazynmap", "gobuster"]

    def test_read_recent_commands_missing_file(self, tmp_path: Path) -> None:
        assert read_recent_commands(str(tmp_path)) == []

    def test_build_context_resolves_target_and_phase(self, tmp_path: Path) -> None:
        ctx = build_context({"rhost": "10.1.1.1", "phase": "ENUM"}, sessions_dir=str(tmp_path))
        assert ctx.target == "10.1.1.1"
        assert ctx.phase == "enum"

    def test_build_default_engine_always_returns_engine(self, tmp_path: Path) -> None:
        engine = build_default_engine(payload={}, command_index_path=str(tmp_path / "missing.json"))
        assert isinstance(engine, RecommendationEngine)
        recs = engine.recommend(_ctx(recent=["lazynmap"]))
        assert all(isinstance(r, Recommendation) for r in recs)
