"""Untrusted data rendered into the DOM must be neutralized.

SDD contract: beacon output, scan hostnames, AI text and collab
events reach ``innerHTML`` sinks. Every such sink must pass through
``DOMPurify.sanitize`` (vendored lib, the index.html precedent) or
the ``esc()`` entity-encoder for pure-text slots. Raw
interpolations of response/label/operator data are regressions.
"""

from __future__ import annotations

import re
from pathlib import Path

T = Path(__file__).resolve().parent.parent / "templates"


def _src(name: str) -> str:
    return (T / name).read_text(encoding="utf-8")


class TestXssSinks:
    def test_collab_events_escaped(self) -> None:
        src = _src("collab.html")
        assert "function esc(" in src or "DOMPurify.sanitize" in src
        assert "${ev.operator}" not in src or "esc(ev.operator)" in src or "sanitize" in src

    def test_yaml_view_loads_purify(self) -> None:
        src = _src("yaml_view.html")
        assert "purify-3.0.9.min.js" in src

    def test_yaml_view_chatbot_sanitized(self) -> None:
        src = _src("yaml_view.html")
        assert "${data.error}" not in src
        assert "DOMPurify.sanitize" in src

    def test_new_campaign_chunks_sanitized(self) -> None:
        src = _src("new_campaign.html")
        assert "innerHTML +=  data.response" not in src
        assert "innerHTML += data.response" not in src

    def test_surface_labels_escaped(self) -> None:
        src = _src("surface.html")
        assert "function esc(" in src or "purify-3.0.9.min.js" in src
        assert "${suggestion.label}" not in src or "esc(" in src

    def test_index_lazyos_response_sanitized(self) -> None:
        src = _src("index.html")
        assert "' + data.response + '" not in src
