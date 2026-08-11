"""Tests for evidence-backed inline hints.

Covers the three collaborating pieces that turn the bare name-only hint into
advice the operator can trust:

    - ``cli.reactive_hints.confidence_from_score`` — score to display confidence.
    - ``cli.reactive_hints.build_evidence_hints`` / ``render_evidence_hints`` —
      shaping and printing verb + confidence + reason + provenance.
    - ``cli.recommendation_signals.recommend_with_evidence`` — the reuse-friendly
      engine convenience.
    - ``cli.tips_engine.TipsEngine`` wiring — evidence path with graceful
      fallback to the static bare-name hints.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest

from cli.reactive_hints import (
    EvidenceHint,
    build_evidence_hints,
    confidence_from_score,
    render_evidence_hints,
)
from cli.recommendation_signals import recommend_with_evidence
from cli.tips_engine import TipsConfig, TipsEngine


def _rec(
    action: str,
    score: float,
    reasons: tuple[str, ...] = (),
    sources: tuple[str, ...] = (),
    command_preview: str = "",
) -> SimpleNamespace:
    """Build a duck-typed Recommendation for the pure hint builders."""
    return SimpleNamespace(
        action=action,
        score=score,
        reasons=reasons,
        sources=sources,
        command_preview=command_preview,
    )


class _FakeEngine:
    """Stub recommendation engine recording the context it was called with."""

    def __init__(self, recs: list[SimpleNamespace]) -> None:
        self.recs = recs
        self.last_ctx = None

    def recommend(self, ctx) -> list[SimpleNamespace]:
        self.last_ctx = ctx
        return list(self.recs)


class TestConfidenceFromScore:
    def test_zero_score_is_zero_confidence(self):
        assert confidence_from_score(0.0) == 0

    def test_negative_score_floored_to_zero(self):
        assert confidence_from_score(-4.2) == 0

    def test_half_score_constant_yields_fifty(self):
        assert confidence_from_score(1.0) == 50

    def test_monotonic_non_decreasing(self):
        values = [confidence_from_score(s) for s in (0.1, 0.5, 1.0, 2.0, 5.0)]
        assert values == sorted(values)

    def test_never_reaches_or_exceeds_hundred(self):
        assert confidence_from_score(1000.0) < 100
        assert confidence_from_score(1000.0) <= 100

    def test_bounded_in_unit_range_scaled(self):
        for score in (0.0, 0.3, 1.7, 42.0):
            conf = confidence_from_score(score)
            assert 0 <= conf <= 100


class TestBuildEvidenceHints:
    def test_maps_core_fields(self):
        hints = build_evidence_hints(
            [_rec("gobuster", 1.0, ("[gap] web 80 open, no content discovery",), ("gap",))],
            limit=3,
        )
        assert len(hints) == 1
        hint = hints[0]
        assert isinstance(hint, EvidenceHint)
        assert hint.verb == "gobuster"
        assert hint.confidence == 50
        assert hint.reason == "web 80 open, no content discovery"
        assert hint.sources == ("gap",)

    def test_strips_source_tag_from_reason(self):
        hints = build_evidence_hints(
            [_rec("linpeas", 2.0, ("[recon] foothold but no privesc",))], limit=3
        )
        assert hints[0].reason == "foothold but no privesc"

    def test_prefers_command_preview_over_action(self):
        hints = build_evidence_hints(
            [_rec("crackmapexec", 0.9, ("[topology] pivot host",), command_preview="cme smb 10.0.0.5")],
            limit=3,
        )
        assert hints[0].verb == "cme smb 10.0.0.5"

    def test_skips_recommendation_without_verb(self):
        hints = build_evidence_hints([_rec("", 1.0, ("[gap] reason",))], limit=3)
        assert hints == []

    def test_skips_recommendation_without_reason(self):
        hints = build_evidence_hints([_rec("gobuster", 1.0, ())], limit=3)
        assert hints == []

    def test_respects_limit(self):
        recs = [_rec(f"cmd{i}", 1.0, (f"[gap] reason {i}",)) for i in range(5)]
        hints = build_evidence_hints(recs, limit=2)
        assert len(hints) == 2
        assert [h.verb for h in hints] == ["cmd0", "cmd1"]

    def test_truncates_long_reason(self):
        long_reason = "x" * 200
        hints = build_evidence_hints([_rec("gobuster", 1.0, (f"[gap] {long_reason}",))], limit=3)
        assert len(hints[0].reason) <= 54


class TestRenderEvidenceHints:
    def test_prints_verb_confidence_and_reason(self, capsys):
        render_evidence_hints(
            [EvidenceHint(verb="enum4linux", confidence=62, reason="SMB 445 open", sources=("gap",))]
        )
        out = capsys.readouterr().out
        assert "enum4linux" in out
        assert "62%" in out
        assert "SMB 445 open" in out

    def test_empty_list_prints_nothing(self, capsys):
        render_evidence_hints([])
        assert capsys.readouterr().out == ""


class TestRecommendWithEvidence:
    def test_returns_engine_output(self):
        engine = _FakeEngine([_rec("gobuster", 1.0, ("[gap] reason",))])
        result = recommend_with_evidence(payload={"rhost": "10.0.0.1"}, engine=engine)
        assert [r.action for r in result] == ["gobuster"]

    def test_phase_override_reaches_engine_context(self):
        engine = _FakeEngine([])
        recommend_with_evidence(payload={"rhost": "10.0.0.1"}, phase="exploit", engine=engine)
        assert engine.last_ctx.phase == "exploit"

    def test_target_falls_back_to_rhost(self):
        engine = _FakeEngine([])
        recommend_with_evidence(payload={"rhost": "10.0.0.9"}, engine=engine)
        assert engine.last_ctx.target == "10.0.0.9"


@pytest.fixture
def tmp_sessions_with_csv():
    with tempfile.TemporaryDirectory() as d:
        sessions = Path(d)
        (sessions / "engagement_state.json").write_text("{}")
        (sessions / "LazyOwn_session_report.csv").write_text(
            "tool,command\nlazynmap,lazynmap -p 80 10.0.0.1\n"
        )
        yield sessions


def _engine_with_stub(sessions: Path, recs: list[SimpleNamespace], evidence: bool = True) -> TipsEngine:
    cfg = TipsConfig(sessions_dir=str(sessions), payload_path=str(sessions / "payload.json"), evidence_hints=evidence)
    engine = TipsEngine(config=cfg, autosuggest_engine=None)
    engine._rec_engine = _FakeEngine(recs)
    engine._rec_engine_tried = True
    return engine


class TestTipsEngineEvidenceWiring:
    def test_disabled_flag_returns_empty(self, tmp_sessions_with_csv):
        engine = _engine_with_stub(tmp_sessions_with_csv, [_rec("gobuster", 1.0, ("[gap] r",))], evidence=False)
        assert engine._compute_evidence_hints("lazynmap", "enum") == []

    def test_missing_engine_returns_empty(self, tmp_sessions_with_csv):
        cfg = TipsConfig(sessions_dir=str(tmp_sessions_with_csv), evidence_hints=True)
        engine = TipsEngine(config=cfg)
        engine._rec_engine = None
        engine._rec_engine_tried = True
        assert engine._compute_evidence_hints("lazynmap", "enum") == []

    def test_returns_evidence_hints(self, tmp_sessions_with_csv):
        engine = _engine_with_stub(
            tmp_sessions_with_csv, [_rec("gobuster", 1.2, ("[gap] web 80 open",), ("gap",))]
        )
        hints = engine._compute_evidence_hints("lazynmap", "enum")
        assert len(hints) == 1
        assert hints[0].verb == "gobuster"

    def test_filters_already_run_commands(self, tmp_sessions_with_csv):
        engine = _engine_with_stub(
            tmp_sessions_with_csv,
            [
                _rec("lazynmap", 2.0, ("[gap] already scanned",)),
                _rec("gobuster", 1.0, ("[gap] enumerate web",)),
            ],
        )
        verbs = [h.verb for h in engine._compute_evidence_hints("lazynmap", "enum")]
        assert "lazynmap" not in verbs
        assert "gobuster" in verbs

    def test_render_prefers_evidence_over_bare_names(self, tmp_sessions_with_csv, capsys):
        engine = _engine_with_stub(
            tmp_sessions_with_csv, [_rec("gobuster", 1.5, ("[gap] web 80 open",), ("gap",))]
        )
        engine._render_kill_chain_hints("lazynmap", "enum")
        out = capsys.readouterr().out
        assert "gobuster" in out
        assert "%" in out

    def test_render_falls_back_to_bare_names(self, tmp_sessions_with_csv, capsys):
        cfg = TipsConfig(
            sessions_dir=str(tmp_sessions_with_csv),
            evidence_hints=False,
            kill_chain_next={"ping": ["lazynmap", "arpscan"]},
            phase_priority={"recon": ["ping", "arpscan", "hosts_discovery"]},
        )
        engine = TipsEngine(config=cfg)
        engine._render_kill_chain_hints("ping", "recon")
        out = capsys.readouterr().out
        assert "arpscan" in out
        assert "%" not in out
