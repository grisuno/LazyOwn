"""Tests for extended WorldModel methods: set_os_hint, get_host, get_hosts_summary."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from modules.world_model import HostState, WorldModel


@pytest.fixture
def world_model():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "test_world_model.json"
        wm = WorldModel(path=str(path))
        yield wm
        wm.reset()


class TestSetOsHint:

    def test_set_os_hint_on_new_host(self, world_model):
        world_model.set_os_hint("10.0.0.1", "linux")
        host = world_model.get_host("10.0.0.1")
        assert host is not None
        assert host.os_hint == "linux"

    def test_set_os_hint_on_existing_host(self, world_model):
        world_model.add_host("10.0.0.1")
        world_model.set_os_hint("10.0.0.1", "windows")
        host = world_model.get_host("10.0.0.1")
        assert host is not None
        assert host.os_hint == "windows"

    def test_set_os_hint_empty_string_is_stored(self, world_model):
        world_model.set_os_hint("10.0.0.1", "")
        host = world_model.get_host("10.0.0.1")
        assert host is not None
        assert host.os_hint == ""


class TestGetHost:

    def test_get_host_returns_none_for_unknown(self, world_model):
        assert world_model.get_host("10.0.0.99") is None

    def test_get_host_returns_entry_for_known(self, world_model):
        world_model.add_host("10.0.0.1")
        host = world_model.get_host("10.0.0.1")
        assert host is not None
        assert host.ip == "10.0.0.1"

    def test_get_host_is_thread_safe(self, world_model):
        world_model.add_host("10.0.0.1")
        world_model.advance_host("10.0.0.1", HostState.SCANNED)
        host = world_model.get_host("10.0.0.1")
        assert host is not None
        assert host.state == HostState.SCANNED


class TestGetHostsSummary:

    def test_empty_summary(self, world_model):
        assert world_model.get_hosts_summary() == {}

    def test_populated_summary(self, world_model):
        world_model.add_host("10.0.0.1")
        world_model.advance_host("10.0.0.1", HostState.EXPLOITED)
        world_model.add_host("10.0.0.2")
        summary = world_model.get_hosts_summary()
        assert summary == {"10.0.0.1": "exploited", "10.0.0.2": "unscanned"}


class TestAdvanceHostEdgeCases:

    def test_advance_host_skips_on_same_state(self, world_model):
        world_model.advance_host("10.0.0.1", HostState.SCANNED)
        result = world_model.advance_host("10.0.0.1", HostState.SCANNED)
        assert result is False

    def test_advance_host_skips_on_lower_state(self, world_model):
        world_model.advance_host("10.0.0.1", HostState.EXPLOITED)
        result = world_model.advance_host("10.0.0.1", HostState.SCANNED)
        assert result is False

    def test_advance_host_to_owned_is_allowed_from_exploited(self, world_model):
        world_model.advance_host("10.0.0.1", HostState.EXPLOITED)
        result = world_model.advance_host("10.0.0.1", HostState.OWNED)
        assert result is True


class TestGetPhaseAfterStateChanges:

    def test_phase_derived_from_host_state(self, world_model):
        world_model.advance_host("10.0.0.1", HostState.EXPLOITED)
        assert world_model.get_phase().value == "exploitation"

    def test_phase_post_exploitation_on_owned(self, world_model):
        world_model.advance_host("10.0.0.1", HostState.OWNED)
        world_model.add_host("10.0.0.2")
        assert world_model.get_phase().value == "post_exploitation"

    def test_phase_complete_when_all_owned(self, world_model):
        world_model.advance_host("10.0.0.1", HostState.OWNED)
        world_model.advance_host("10.0.0.2", HostState.OWNED)
        assert world_model.get_phase().value == "complete"

    def test_phase_recon_when_no_hosts(self, world_model):
        assert world_model.get_phase().value == "recon"
