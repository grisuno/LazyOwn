"""Lazy mentions multi-type search and scroll pagination."""

from __future__ import annotations


def test_mentions_search_and_cursor(tmp_path, monkeypatch):
    from modules import lazy_mentions as _m

    page = _m.search_mentions_page("", "", "")
    assert len(page.items) <= 20
    if page.next_cursor:
        second = _m.search_mentions_page("", "", page.next_cursor)
        assert isinstance(second.items, list)


def test_mentions_parse_caps_and_trusts_ids():
    from modules import lazy_mentions as _m

    refs = _m.parse_mentions("check @[finding#12 report] and @[ip#7]")
    assert refs == [{"kind": "finding", "id": 12}, {"kind": "ip", "id": 7}]
    assert _m.parse_mentions("no refs") == []
