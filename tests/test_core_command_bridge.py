"""Tests for core.command_bridge — CommandBridge lazy shell facade."""

from __future__ import annotations

import sys
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(autouse=True)
def _reset_bridge_singleton():
    """Reset the module-level singleton before each test."""
    import core.command_bridge as mod

    mod._bridge = None
    yield
    mod._bridge = None


class TestCommandBridgeInitialization:
    """Tests for :class:`CommandBridge` construction and initial state."""

    def test_ready_is_false_initially(self):
        """CommandBridge is not ready until _ensure_shell succeeds."""
        from core.command_bridge import CommandBridge

        bridge = CommandBridge()
        assert bridge.ready is False

    def test_error_is_none_initially(self):
        """CommandBridge.error is None before any initialization attempt."""
        from core.command_bridge import CommandBridge

        bridge = CommandBridge()
        assert bridge.error is None

    def test_get_bridge_returns_same_singleton(self, _reset_bridge_singleton):
        """get_bridge always returns the same CommandBridge instance."""
        from core.command_bridge import get_bridge

        b1 = get_bridge()
        b2 = get_bridge()
        assert b1 is b2


class TestCommandBridgeOnecmd:
    """Tests for :meth:`CommandBridge.onecmd`."""

    def test_empty_command_returns_empty_string(self):
        """onecmd returns an empty string when given an empty or blank command."""
        from core.command_bridge import CommandBridge

        bridge = CommandBridge()
        assert bridge.onecmd("") == ""
        assert bridge.onecmd("   ") == ""

    def test_nonexistent_command_returns_error_string(self):
        """onecmd does not crash and handles init failures gracefully."""
        from core.command_bridge import CommandBridge

        bridge = CommandBridge()
        try:
            result = bridge.onecmd("nonexistent_cmd_12345_xyz")
            assert isinstance(result, str)
            assert len(result) > 0
        except SystemExit:
            pass

    def test_thread_safety_multiple_threads(self):
        """Concurrent onecmd calls from multiple threads do not crash."""
        from core.command_bridge import CommandBridge

        bridge = CommandBridge()
        errors = []

        def call_onecmd():
            try:
                result = bridge.onecmd("")
                assert result == ""
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=call_onecmd) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(errors) == 0


class TestCommandBridgeOneCmdAlias:
    """Tests for :meth:`CommandBridge.one_cmd` and :meth:`CommandBridge.execute`."""

    def test_empty_command_returns_empty(self):
        """one_cmd returns an empty string when given an empty command."""
        from core.command_bridge import CommandBridge

        bridge = CommandBridge()
        assert bridge.one_cmd("") == ""
        assert bridge.one_cmd("   ") == ""

    def test_execute_alias_returns_string(self):
        """execute delegates to one_cmd and returns a string for empty input."""
        from core.command_bridge import CommandBridge

        bridge = CommandBridge()
        result = bridge.execute("")
        assert isinstance(result, str)
        assert result == ""

    def test_nonexistent_lazy_loaded_cmd_returns_error(self):
        """one_cmd returns an error string when shell initialization fails."""
        from core.command_bridge import CommandBridge

        bridge = CommandBridge()
        result = bridge.one_cmd("nonexistent_cmd_12345_xyz")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "error" in result.lower()
