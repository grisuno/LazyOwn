"""Tests for modules.loop.evidence."""

from __future__ import annotations

import time

from modules.loop.evidence import (
    CitationService,
    extract_quote,
    normalize_ws,
    verbatim_contains,
)


class FakeTraffic:
    def __init__(self, rows):
        self._rows = rows

    def read(self, limit=200):
        return self._rows[: max(1, limit)]

    def record(self, kind, command, output="", meta=None):
        return {}


def test_normalize_ws():
    assert normalize_ws("a\n  b\t c") == "a b c"
    assert normalize_ws(None) == ""


def test_verbatim_contains():
    assert verbatim_contains("uid=0(root) gid=0(root)", "line1\nuid=0(root)  gid=0(root)\nline2")
    assert not verbatim_contains("uid=0(root)", "uid=1000(user)")
    assert not verbatim_contains("", "anything")
    assert not verbatim_contains("short", "short")


def test_extract_quote_double():
    assert extract_quote('found: "uid=0(root) gid=0(root)" on target') == "uid=0(root) gid=0(root)"


def test_extract_quote_backtick():
    assert extract_quote("proof `root:admin1234` here") == "root:admin1234"


def test_extract_quote_label():
    assert extract_quote("quote: password is secret12") == "password is secret12"


def test_extract_quote_no_quote():
    assert extract_quote("plain text without quotes") == ""


def test_verify_hits_fresh_record():
    traffic = FakeTraffic(
        [{"command": "id", "output": "uid=0(root) gid=0(root) groups=0(root)", "ts": time.time(), "digest": "abc"}]
    )
    service = CitationService()
    result = service.verify("uid=0(root) gid=0(root)", traffic)
    assert result["verified"] is True
    assert result["digest"] == "abc"


def test_verify_rejects_stale_record():
    traffic = FakeTraffic(
        [{"command": "id", "output": "uid=0(root) gid=0(root)", "ts": time.time() - 100000, "digest": "abc"}]
    )
    service = CitationService(max_age_sec=3600)
    assert service.verify("uid=0(root) gid=0(root)", traffic)["verified"] is False


def test_verify_no_traffic():
    assert CitationService().verify("uid=0(root) gid=0(root)", None)["verified"] is False


def test_replay_executes_and_records():
    traffic = FakeTraffic([])
    service = CitationService()
    result = service.replay("id", lambda command: "uid=0(root)", traffic)
    assert result["executed"] is True
    assert "uid=0" in result["output"]


def test_replay_failure_is_reported():
    service = CitationService()

    def boom(command):
        raise RuntimeError("down")

    result = service.replay("id", boom, None)
    assert result["executed"] is False
    assert "replay failed" in result["output"]


def test_replay_empty_command():
    assert CitationService().replay("", lambda command: "x", None)["executed"] is False


def test_annotate_writes_meta():
    finding = {"meta": {}}
    meta = CitationService().annotate(finding, {"verified": True, "digest": "d1", "age": 2.0})
    assert meta["citation"]["verified"] is True
    assert meta["citation"]["digest"] == "d1"
