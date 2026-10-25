"""Contract tests for the MCP sitrep recommender embedding.

SDD contract: ``_sitrep_recommendations`` adapts
``recommender.recommend_and_save`` output (``command``/``confidence``/
``reason``) into the sitrep shape and never forwards positional
arguments into the recommender.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_mcp_module():
    """Import skills/lazyown_mcp.py reusing the boyscout SDK-stub recipe."""
    helper_path = Path(__file__).resolve().parent / "test_boyscout_contracts.py"
    spec = importlib.util.spec_from_file_location("test_boyscout_contracts", helper_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module._load_mcp_module()


def test_maps_recommender_fields(monkeypatch):
    mcp = _load_mcp_module()
    monkeypatch.setattr(mcp, "_ensure_recommender", lambda: True)
    monkeypatch.setattr(
        mcp,
        "_recommend",
        lambda: [
            {"command": "lazynmap", "args": "-p-", "confidence": 0.9, "reason": "recon first"},
            {"command": "_error", "confidence": 0.0, "reason": "no key"},
            {"command": "   ", "confidence": 1.0, "reason": ""},
            "junk",
        ],
    )

    assert mcp._sitrep_recommendations() == [
        {"command": "lazynmap", "score": 0.9, "reasoning": "recon first"},
    ]


def test_never_forwards_positional_arguments(monkeypatch):
    mcp = _load_mcp_module()
    calls: list = []

    def fake_recommend(*args, **kwargs):
        calls.append((args, kwargs))
        return []

    monkeypatch.setattr(mcp, "_ensure_recommender", lambda: True)
    monkeypatch.setattr(mcp, "_recommend", fake_recommend)

    assert mcp._sitrep_recommendations() == []
    assert calls == [((), {})]


def test_returns_error_entry_on_failure(monkeypatch):
    mcp = _load_mcp_module()

    def explode():
        raise RuntimeError("groq down")

    monkeypatch.setattr(mcp, "_ensure_recommender", lambda: True)
    monkeypatch.setattr(mcp, "_recommend", explode)

    assert mcp._sitrep_recommendations() == [{"error": "groq down"}]


def test_reports_unavailable_recommender(monkeypatch):
    mcp = _load_mcp_module()
    monkeypatch.setattr(mcp, "_ensure_recommender", lambda: False)

    result = mcp._sitrep_recommendations()

    assert len(result) == 1
    assert "error" in result[0]


def test_limits_suggestions(monkeypatch):
    mcp = _load_mcp_module()
    monkeypatch.setattr(mcp, "_ensure_recommender", lambda: True)
    monkeypatch.setattr(
        mcp,
        "_recommend",
        lambda: [{"command": f"cmd{i}", "confidence": 0.5, "reason": ""} for i in range(10)],
    )

    assert len(mcp._sitrep_recommendations(limit=2)) == 2
