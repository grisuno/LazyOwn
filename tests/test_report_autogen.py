"""Tests for the engagement report auto-generation contract.

Covers the funnel-shape normalizer that keeps the ``/report`` page from
crashing on the producer's list-form funnel, plus the gating, format
resolution and best-effort behaviour of ``modules.report_autogen``.
"""

from __future__ import annotations

import importlib

import pytest


def test_normalize_funnel_list_to_dict():
    """Given the producer list funnel, When normalized, Then stage keys map to counts."""
    from modules.report_autogen import normalize_funnel as _normalize_funnel

    funnel = [
        {"stage": "discovered", "hosts": 50},
        {"stage": "with findings", "hosts": 3},
        {"stage": "owned", "hosts": 2},
    ]
    result = _normalize_funnel(funnel)
    assert result == {"discovered": 50, "with findings": 3, "owned": 2}
    assert result.get("discovered", 0) == 50


def test_normalize_funnel_handles_dict_and_junk():
    """Given a dict, None, or malformed rows, When normalized, Then it never raises."""
    from modules.report_autogen import normalize_funnel as _normalize_funnel

    assert _normalize_funnel({"discovered": "7"}) == {"discovered": 7}
    assert _normalize_funnel(None) == {}
    assert _normalize_funnel("bad") == {}
    assert _normalize_funnel([{"stage": "", "hosts": 1}, {"nope": 1}, 5]) == {}
    assert _normalize_funnel([{"stage": "owned", "hosts": "x"}]) == {"owned": 0}


def test_resolve_formats_filters_and_defaults():
    """Given configured formats, When resolved, Then only valid de-duped formats remain."""
    autogen = importlib.import_module("modules.report_autogen")
    assert autogen._resolve_formats({}) == ["html", "md", "json"]
    assert autogen._resolve_formats({"auto_report_formats": "pdf, html, html, bogus"}) == ["pdf", "html"]
    assert autogen._resolve_formats({"auto_report_formats": "   "}) == ["html", "md", "json"]


@pytest.mark.parametrize(
    "value,expected",
    [(True, True), (False, False), ("true", True), ("0", False), ("on", True), ("no", False)],
)
def test_is_enabled(value, expected):
    """Given the toggle in various forms, When read, Then it resolves to a bool."""
    autogen = importlib.import_module("modules.report_autogen")
    assert autogen._is_enabled({"auto_report_on_finish": value}) is expected


def test_generate_refreshes_session_even_when_disabled(monkeypatch):
    """Given auto-report disabled, When generating, Then the session still refreshes but no artifacts."""
    autogen = importlib.import_module("modules.report_autogen")
    monkeypatch.setattr(autogen, "_load_params", lambda: {"auto_report_on_finish": False})
    monkeypatch.setattr(autogen, "_last_run_at", 0.0, raising=False)
    monkeypatch.setattr("modules.c2_surfaces.refresh_session_report", lambda timeout=120: True)

    result = autogen.generate_campaign_report(reason="unit", force=True)
    assert result["session_refreshed"] is True
    assert result["enabled"] is False
    assert result["reports"] == []


def test_generate_emits_artifacts_when_enabled(monkeypatch, tmp_path):
    """Given auto-report enabled, When generating, Then the configured formats are emitted."""
    autogen = importlib.import_module("modules.report_autogen")
    monkeypatch.setattr(
        autogen,
        "_load_params",
        lambda: {
            "auto_report_on_finish": True,
            "auto_report_formats": "html,json",
            "report_output_path": str(tmp_path),
        },
    )
    monkeypatch.setattr(autogen, "_last_run_at", 0.0, raising=False)
    monkeypatch.setattr("modules.c2_surfaces.refresh_session_report", lambda timeout=120: True)

    produced: list[str] = []

    class _Gen:
        def generate(self, output_dir, output_format, client_name):
            path = f"{output_dir}/report.{output_format}"
            produced.append(output_format)
            return path

    monkeypatch.setattr("modules.professional_report.RedTeamReportGenerator", _Gen)

    result = autogen.generate_campaign_report(reason="unit", force=True)
    assert result["enabled"] is True
    assert produced == ["html", "json"]
    assert len(result["reports"]) == 2


def test_generate_never_raises_on_generator_failure(monkeypatch):
    """Given a generator that explodes, When generating, Then the error is captured, not raised."""
    autogen = importlib.import_module("modules.report_autogen")
    monkeypatch.setattr(autogen, "_load_params", lambda: {"auto_report_on_finish": True})
    monkeypatch.setattr(autogen, "_last_run_at", 0.0, raising=False)
    monkeypatch.setattr("modules.c2_surfaces.refresh_session_report", lambda timeout=120: True)

    class _Boom:
        def generate(self, **kwargs):
            raise RuntimeError("boom")

    monkeypatch.setattr("modules.professional_report.RedTeamReportGenerator", _Boom)
    result = autogen.generate_campaign_report(reason="unit", force=True)
    assert result["reports"] == []
    assert any("boom" in err for err in result["errors"])


def test_throttle_collapses_rapid_calls(monkeypatch):
    """Given two rapid calls, When the second runs, Then it is throttled."""
    autogen = importlib.import_module("modules.report_autogen")
    monkeypatch.setattr(autogen, "_load_params", lambda: {"auto_report_on_finish": False})
    monkeypatch.setattr(autogen, "_last_run_at", 0.0, raising=False)
    monkeypatch.setattr("modules.c2_surfaces.refresh_session_report", lambda timeout=120: True)

    first = autogen.generate_campaign_report(reason="a", force=True)
    second = autogen.generate_campaign_report(reason="b")
    assert first["session_refreshed"] is True
    assert "throttled" in second["errors"]
