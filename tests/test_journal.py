"""Tests for the GitHub Discussions engineering journal.

The journal drives ``gh`` through an injected runner, so these tests exercise
the GraphQL wiring and the parsing without touching the network.
"""

from __future__ import annotations

import json

import pytest

from scripts.journal import Journal, JournalConfig, JournalError


class FakeRunner:
    """Return canned GraphQL payloads keyed by a query fragment."""

    def __init__(self, responses: dict[str, dict]) -> None:
        """Store the responses keyed by a fragment of the query string."""
        self._responses = responses
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str]) -> str:
        """Record the call and return the matching payload as JSON."""
        self.calls.append(args)
        joined = " ".join(args)
        for fragment, payload in self._responses.items():
            if fragment in joined:
                return json.dumps(payload)
        raise AssertionError(f"unexpected query: {joined}")


def _success_responses() -> dict[str, dict]:
    return {
        "repository(owner:$owner,name:$name){id}": {"data": {"repository": {"id": "R1"}}},
        "discussionCategories": {
            "data": {"repository": {"discussionCategories": {"nodes": [{"id": "C1", "name": "Show and tell"}]}}}
        },
        "createDiscussion": {
            "data": {"createDiscussion": {"discussion": {"number": 7, "url": "u", "title": "t"}}}
        },
        "discussions(first": {
            "data": {"repository": {"discussions": {"nodes": [{"number": 7, "title": "t", "body": "b", "url": "u", "updatedAt": "now"}]}}}
        },
    }


def test_config_from_remote_slug() -> None:
    """A repository slug resolves without touching git."""
    config = JournalConfig.from_git_remote(remote="grisuno/LazyOwn")
    assert config.owner == "grisuno"
    assert config.name == "LazyOwn"


def test_config_rejects_bare_name() -> None:
    """A slug without a separator is rejected."""
    with pytest.raises(JournalError):
        JournalConfig.from_git_remote(remote="LazyOwn")


def test_post_entry_uses_resolved_ids() -> None:
    """The create mutation receives the repository and category ids."""
    runner = FakeRunner(_success_responses())
    journal = Journal(JournalConfig(owner="grisuno", name="LazyOwn"), runner=runner)
    entry = journal.post("title", "body")
    assert entry["number"] == 7
    assert any("createDiscussion" in " ".join(call) for call in runner.calls)


def test_entries_returns_nodes() -> None:
    """Reading returns the discussion nodes."""
    runner = FakeRunner(_success_responses())
    journal = Journal(JournalConfig(owner="grisuno", name="LazyOwn"), runner=runner)
    entries = journal.entries(3)
    assert entries[0]["number"] == 7


def test_missing_category_raises() -> None:
    """A category that is not present raises instead of silently posting."""
    responses = _success_responses()
    responses["discussionCategories"] = {
        "data": {"repository": {"discussionCategories": {"nodes": [{"id": "C1", "name": "General"}]}}}
    }
    runner = FakeRunner(responses)
    journal = Journal(JournalConfig(owner="grisuno", name="LazyOwn", category="Show and tell"), runner=runner)
    with pytest.raises(JournalError):
        journal.post("title", "body")


def test_graphql_errors_raise() -> None:
    """A GraphQL error payload raises a JournalError."""
    runner = FakeRunner({"repository": {"errors": [{"message": "boom"}]}})
    journal = Journal(JournalConfig(owner="grisuno", name="LazyOwn"), runner=runner)
    with pytest.raises(JournalError):
        _ = journal.repo_id
