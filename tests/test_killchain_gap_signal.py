"""Tests for :class:`cli.recommendation_signals.KillchainGapSignal`.

Covers gap detection rules:
    - EXPLOITED host without privesc
    - OWNED host without credentials
    - Scan exists without enumeration
    - Credentials exist without lateral movement
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from cli.recommendation import KIND_COMMAND, RecommendationContext
from cli.recommendation_signals import KillchainGapSignal, SOURCE_GAP


@pytest.fixture
def sessions_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


def _write_world_model(sessions_dir: Path, data: dict) -> None:
    (sessions_dir / "world_model.json").write_text(json.dumps(data))


class TestKillchainGapSignalConstruction:

    def test_name_is_gap_source(self):
        signal = KillchainGapSignal(sessions_dir="/tmp/x")
        assert signal.name == SOURCE_GAP


class TestGapExploitedNoPrivesc:

    def test_exploited_linux_recommends_linpeas(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.1": {"state": "exploited", "os_hint": "linux"}},
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="exploit")
        proposals = signal.propose(ctx)
        assert any(p.action == "linpeas" and p.category == "privesc" for p in proposals)

    def test_exploited_windows_recommends_winpeas(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.2": {"state": "exploited", "os_hint": "windows"}},
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="exploit")
        proposals = signal.propose(ctx)
        assert any(p.action == "winpeas" and p.category == "privesc" for p in proposals)

    def test_unscanned_host_no_proposals(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.1": {"state": "unscanned"}},
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="recon")
        proposals = signal.propose(ctx)
        assert len(proposals) == 0

    def test_no_world_model_returns_empty(self, sessions_dir):
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="recon")
        proposals = signal.propose(ctx)
        assert proposals == []


class TestGapOwnedNoCreds:

    def test_owned_no_credentials_recommends_lazydump(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.1": {"state": "owned", "os_hint": "linux"}},
            "credentials": [],
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="postexp")
        proposals = signal.propose(ctx)
        assert any(p.action == "lazydump" and p.category == "cred" for p in proposals)

    def test_owned_with_credentials_no_proposals(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.1": {"state": "owned", "os_hint": "linux"}},
            "credentials": [{"value": "root:hash", "host": "10.0.0.1"}],
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="postexp")
        proposals = signal.propose(ctx)
        assert not any(p.action == "lazydump" for p in proposals)


class TestGapScanNoEnum:

    def test_scanned_no_enum_recommends_gobuster(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.1": {"state": "scanned", "os_hint": ""}},
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="scan")
        proposals = signal.propose(ctx)
        assert any(p.action == "gobuster" and p.category == "enum" for p in proposals)

    def test_scanned_with_enum_recent_no_proposals(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.1": {"state": "scanned", "os_hint": ""}},
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(
            target=None, payload={},
            recent_commands=["lazynmap", "gobuster"], phase="enum",
        )
        proposals = signal.propose(ctx)
        assert not any(p.action == "gobuster" for p in proposals)


class TestGapCredsNoLateral:

    def test_credentials_no_lateral_recommends_crackmapexec(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.1": {"state": "owned", "os_hint": "linux"}},
            "credentials": [{"value": "admin:pass", "host": "10.0.0.1"}],
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="postexp")
        proposals = signal.propose(ctx)
        assert any(p.action == "crackmapexec" and p.category == "lateral" for p in proposals)

    def test_no_credentials_no_lateral_proposals(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {"10.0.0.1": {"state": "exploited", "os_hint": "linux"}},
            "credentials": [],
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="exploit")
        proposals = signal.propose(ctx)
        assert not any(p.category == "lateral" for p in proposals)


class TestKillchainGapSignalIntegration:

    def test_multiple_gaps_detected_simultaneously(self, sessions_dir):
        _write_world_model(sessions_dir, {
            "hosts": {
                "10.0.0.1": {"state": "scanned", "os_hint": "linux"},
                "10.0.0.2": {"state": "exploited", "os_hint": "windows"},
                "10.0.0.3": {"state": "owned", "os_hint": "linux"},
            },
            "credentials": [{"value": "admin:pass", "host": "10.0.0.3"}],
        })
        signal = KillchainGapSignal(sessions_dir=str(sessions_dir))
        ctx = RecommendationContext(target=None, payload={}, recent_commands=[], phase="postexp")
        proposals = signal.propose(ctx)
        actions = {p.action for p in proposals}
        assert "gobuster" in actions
        assert "winpeas" in actions
        assert "lazydump" not in actions
        assert "crackmapexec" in actions
