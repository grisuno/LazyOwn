"""Comprehensive tests for modules.killchain — the unified single source of truth.

Covers:
    - Config invariants (phase count, labels, colors, mappings).
    - Phase derivation from WorldModel host states and raw JSON overrides.
    - Phase advancement (atomic write, completed phases tracking, host advance).
    - Progress computation.
    - Edge cases: empty world model, invalid phases, overwritten files.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

os.environ.setdefault("LAZYOWN_DIR", str(_ROOT))


from modules.killchain import (  # noqa: E402
    _DEFAULT_CONFIG,
    KillChain,
    PhaseStatus,
    get_killchain,
)


class TestKillChainConfig:
    """Invariants on the centralised configuration."""

    def test_phases_is_8_tuple(self):
        assert len(_DEFAULT_CONFIG.phases) == 8
        assert isinstance(_DEFAULT_CONFIG.phases, tuple)
        assert _DEFAULT_CONFIG.phases[0] == "recon"
        assert _DEFAULT_CONFIG.phases[-1] == "report"

    def test_phases_are_in_correct_kill_chain_order(self):
        expected = ("recon", "scan", "enum", "exploit", "privesc", "lateral", "exfil", "report")
        assert _DEFAULT_CONFIG.phases == expected

    def test_compact_phases_are_in_correct_order(self):
        expected = ("recon", "enum", "exploit", "privesc", "lateral")
        assert _DEFAULT_CONFIG.compact_phases == expected

    def test_all_phases_have_labels(self):
        for p in _DEFAULT_CONFIG.phases:
            assert p in _DEFAULT_CONFIG.phase_labels
            assert len(_DEFAULT_CONFIG.phase_labels[p]) > 0

    def test_all_phases_have_colors(self):
        for p in _DEFAULT_CONFIG.phases:
            assert p in _DEFAULT_CONFIG.phase_colors
            assert _DEFAULT_CONFIG.phase_colors[p].startswith("#")

    def test_all_phases_have_rich_colors(self):
        for p in _DEFAULT_CONFIG.phases:
            assert p in _DEFAULT_CONFIG.phase_rich_colors

    def test_engagement_to_cli_covers_all_engagement_phases(self):
        from modules.world_model import EngagementPhase
        for ep in EngagementPhase:
            mapped = _DEFAULT_CONFIG.engagement_to_cli.get(ep.value)
            assert mapped is not None, f"Missing mapping for {ep.value}"
        assert _DEFAULT_CONFIG.engagement_to_cli.get("unknown", "recon") == "recon"

    def test_cli_to_host_state_returns_expected(self):
        assert _DEFAULT_CONFIG.cli_to_host_state.get("recon") == ""
        assert _DEFAULT_CONFIG.cli_to_host_state.get("scan") == "scanned"
        assert _DEFAULT_CONFIG.cli_to_host_state.get("enum") == "enumerated"
        assert _DEFAULT_CONFIG.cli_to_host_state.get("exploit") == "exploited"
        assert _DEFAULT_CONFIG.cli_to_host_state.get("privesc") == "owned"
        assert _DEFAULT_CONFIG.cli_to_host_state.get("lateral") == "owned"
        assert _DEFAULT_CONFIG.cli_to_host_state.get("exfil") == "owned"
        assert _DEFAULT_CONFIG.cli_to_host_state.get("report") == "owned"

    def test_phase_index_valid_and_invalid(self):
        assert _DEFAULT_CONFIG.phase_index("recon") == 0
        assert _DEFAULT_CONFIG.phase_index("exploit") == 3
        assert _DEFAULT_CONFIG.phase_index("report") == 7
        assert _DEFAULT_CONFIG.phase_index("nonexistent") == -1

    def test_is_valid_phase(self):
        assert _DEFAULT_CONFIG.is_valid_phase("recon") is True
        assert _DEFAULT_CONFIG.is_valid_phase("exploit") is True
        assert _DEFAULT_CONFIG.is_valid_phase("nonsense") is False

    def test_compact_phases_and_labels(self):
        assert len(_DEFAULT_CONFIG.compact_phases) == 5
        assert _DEFAULT_CONFIG.compact_labels["recon"] == "R"
        assert _DEFAULT_CONFIG.compact_labels["exploit"] == "X"

    def test_world_model_path(self):
        p = _DEFAULT_CONFIG.world_model_path()
        assert p.name == "world_model.json"
        if p.parent.name:
            assert p.parent.name == "sessions"


class TestKillChainCurrentPhase:
    """Phase derivation from WorldModel and raw JSON fallback."""

    @pytest.fixture(autouse=True)
    def _reset_wm_singleton(self):
        import modules.world_model as wm_mod
        old_default = wm_mod._default_wm
        old_path = getattr(wm_mod, '_DEFAULT_PATH', None)
        wm_mod._default_wm = None
        yield
        wm_mod._default_wm = old_default
        if old_path is not None:
            wm_mod._DEFAULT_PATH = old_path

    def test_returns_recon_when_no_world_model_exists(self):
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            phase = KillChain.current_phase(world_model_path=path)
            assert phase == "recon"

    def test_reads_from_world_model_host_state(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            from modules.world_model import get_world_model
            wm = get_world_model(path=path)
            wm.add_host("10.0.0.1")
            wm.advance_host("10.0.0.1", wm_mod.HostState.EXPLOITED)
            phase = KillChain.current_phase(world_model_path=path)
            assert phase == "exploit"

    def test_raw_json_override_wins_when_higher_rank(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            path.write_text(json.dumps({"current_phase": "privesc", "phase": "exploit"}))
            from modules.world_model import get_world_model
            wm = get_world_model(path=path)
            wm.add_host("10.0.0.1")
            wm.advance_host("10.0.0.1", wm_mod.HostState.EXPLOITED)
            phase = KillChain.current_phase(world_model_path=path)
            assert phase == "privesc"

    def test_raw_json_override_ignored_when_lower_rank(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            path.write_text(json.dumps({"current_phase": "scan"}))
            from modules.world_model import get_world_model
            wm = get_world_model(path=path)
            wm.add_host("10.0.0.1")
            wm.advance_host("10.0.0.1", wm_mod.HostState.EXPLOITED)
            phase = KillChain.current_phase(world_model_path=path)
            assert phase == "exploit"

    def test_falls_back_to_legacy_phase_key(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            path.write_text(json.dumps({"phase": "enum"}))
            phase = KillChain.current_phase(world_model_path=path)
            assert phase == "enum"


class TestKillChainAdvancePhase:
    """Atomic writes that advance the kill chain for all surfaces."""

    @pytest.fixture(autouse=True)
    def _reset_wm_singleton(self):
        import modules.world_model as wm_mod
        old_default = wm_mod._default_wm
        old_path = getattr(wm_mod, '_DEFAULT_PATH', None)
        wm_mod._default_wm = None
        yield
        wm_mod._default_wm = old_default
        if old_path is not None:
            wm_mod._DEFAULT_PATH = old_path

    def test_advance_writes_current_phase_and_phase_keys(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            from modules.world_model import get_world_model
            get_world_model(path=path)
            result = KillChain.advance_phase("exploit", world_model_path=path)
            assert result is True
            raw = json.loads(path.read_text(encoding="utf-8"))
            assert raw["current_phase"] == "exploit"
            assert raw["phase"] == "exploit"

    def test_advance_tracks_completed_phases(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            from modules.world_model import get_world_model
            get_world_model(path=path)
            KillChain.advance_phase("recon", world_model_path=path)
            KillChain.advance_phase("exploit", world_model_path=path)
            raw = json.loads(path.read_text(encoding="utf-8"))
            completed = raw.get("completed_phases", [])
            assert "scan" in completed
            assert "enum" in completed
            assert "recon" in completed

    def test_advance_invalid_phase_returns_false(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            result = KillChain.advance_phase("not_a_phase", world_model_path=path)
            assert result is False

    def test_advance_advances_world_model_hosts(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            from modules.world_model import HostState, get_world_model
            wm = get_world_model(path=path)
            wm.add_host("10.0.0.1")
            result = KillChain.advance_phase("scan", world_model_path=path)
            assert result is True
            host = wm.get_host("10.0.0.1")
            assert host is not None
            assert host.state == HostState.SCANNED

    def test_advance_does_not_downgrade_cached_world_model_state(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            from modules.world_model import get_world_model
            wm = get_world_model(path=path)
            wm.add_host("10.0.0.1")
            wm.advance_host("10.0.0.1", wm_mod.HostState.OWNED)
            result = KillChain.advance_phase("scan", world_model_path=path)
            assert result is True
            host = wm.get_host("10.0.0.1")
            assert host is not None
            assert host.state == wm_mod.HostState.OWNED


class TestKillChainGetProgress:
    """Status list generation for all UI renderers."""

    @pytest.fixture(autouse=True)
    def _reset_wm_singleton(self):
        import modules.world_model as wm_mod
        old_default = wm_mod._default_wm
        old_path = getattr(wm_mod, '_DEFAULT_PATH', None)
        wm_mod._default_wm = None
        yield
        wm_mod._default_wm = old_default
        if old_path is not None:
            wm_mod._DEFAULT_PATH = old_path

    def test_all_pending_when_nothing_done(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            path.write_text(json.dumps({}))
            progress = KillChain.get_progress(world_model_path=path)
            assert len(progress) == 8
            assert progress[0].status == "active"  # recon is the default
            assert all(p.status in ("active", "pending") for p in progress)

    def test_progress_reflects_completed_and_active(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            path.write_text(json.dumps({
                "current_phase": "exploit",
                "completed_phases": ["recon", "scan", "enum"],
            }))
            progress = KillChain.get_progress(world_model_path=path)
            states = {p.key: p.status for p in progress}
            assert states["recon"] == "done"
            assert states["scan"] == "done"
            assert states["enum"] == "done"
            assert states["exploit"] == "active"
            assert states["privesc"] == "pending"
            assert states["report"] == "pending"

    def test_progress_has_colors_and_labels(self):
        import modules.world_model as wm_mod
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            path = sdir / "world_model.json"
            wm_mod._DEFAULT_PATH = path
            path.write_text(json.dumps({"current_phase": "recon"}))
            progress = KillChain.get_progress(world_model_path=path)
            for p in progress:
                assert p.key
                assert p.label
                assert p.color.startswith("#")
                assert p.status in ("done", "active", "pending")


class TestKillChainHelpers:
    """Static helpers and display helpers."""

    def test_phases_for_display_returns_triples(self):
        phases = KillChain.phases_for_display()
        assert len(phases) == 8
        for triple in phases:
            assert len(triple) == 3
            key, label, color = triple
            assert key in _DEFAULT_CONFIG.phases
            assert len(label) > 0
            assert color.startswith("#")

    def test_compact_progress_returns_string(self):
        result = KillChain.compact_progress("recon")
        assert "[" in result
        assert "]" in result
        assert "R" in result

    def test_engagement_phase_to_cli_maps_all(self):
        assert KillChain.engagement_phase_to_cli("recon") == "recon"
        assert KillChain.engagement_phase_to_cli("scanning") == "scan"
        assert KillChain.engagement_phase_to_cli("enumeration") == "enum"
        assert KillChain.engagement_phase_to_cli("exploitation") == "exploit"
        assert KillChain.engagement_phase_to_cli("post_exploitation") == "privesc"
        assert KillChain.engagement_phase_to_cli("complete") == "report"
        assert KillChain.engagement_phase_to_cli("unknown") == "recon"

    def test_cli_phase_to_host_state_maps_all(self):
        assert KillChain.cli_phase_to_host_state("recon") == ""
        assert KillChain.cli_phase_to_host_state("scan") == "scanned"
        assert KillChain.cli_phase_to_host_state("enum") == "enumerated"
        assert KillChain.cli_phase_to_host_state("exploit") == "exploited"
        assert KillChain.cli_phase_to_host_state("privesc") == "owned"
        assert KillChain.cli_phase_to_host_state("cred") == "owned"

    def test_get_killchain_returns_class(self):
        kc = get_killchain()
        assert kc is KillChain

    def test_phase_index_returns_correct(self):
        assert KillChain.phase_index("recon") == 0
        assert KillChain.phase_index("exploit") == 3
        assert KillChain.phase_index("report") == 7
        assert KillChain.phase_index("invalid") == -1


class TestPhaseStatusDataclass:
    """Behaviour-driven: PhaseStatus is used by every UI surface."""

    def test_phase_status_is_immutable(self):
        ps = PhaseStatus(key="recon", label="Recon", color="#fff", status="done")
        with pytest.raises(Exception):
            ps.status = "active"  # type: ignore[misc]

    def test_phase_status_fields_match_config(self):
        ps = PhaseStatus(key="exploit", label="Exploitation", color="#f85149", status="active")
        assert ps.key in _DEFAULT_CONFIG.phases
        assert ps.label == _DEFAULT_CONFIG.phase_labels["exploit"]
        assert ps.color == _DEFAULT_CONFIG.phase_colors["exploit"]
