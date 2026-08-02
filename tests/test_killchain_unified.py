"""Tests for unified killchain phase: read_phase, write_phase, phase mapping helpers."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from cli.ops_commands import (
    _cli_phase_to_host_state,
    _engagement_phase_to_cli,
    _phase_rank,
    read_phase,
    write_phase,
)


class TestPhaseMapping:

    def test_engagement_phase_to_cli_maps_all(self):
        assert _engagement_phase_to_cli("recon") == "recon"
        assert _engagement_phase_to_cli("scanning") == "scan"
        assert _engagement_phase_to_cli("enumeration") == "enum"
        assert _engagement_phase_to_cli("exploitation") == "exploit"
        assert _engagement_phase_to_cli("post_exploitation") == "privesc"
        assert _engagement_phase_to_cli("complete") == "report"
        assert _engagement_phase_to_cli("unknown") == "recon"

    def test_cli_phase_to_host_state_maps_correctly(self):
        assert _cli_phase_to_host_state("recon") == ""
        assert _cli_phase_to_host_state("scan") == "scanned"
        assert _cli_phase_to_host_state("enum") == "enumerated"
        assert _cli_phase_to_host_state("exploit") == "exploited"
        assert _cli_phase_to_host_state("privesc") == "owned"
        assert _cli_phase_to_host_state("lateral") == "owned"
        assert _cli_phase_to_host_state("exfil") == "owned"
        assert _cli_phase_to_host_state("report") == "owned"
        assert _cli_phase_to_host_state("cred") == "owned"

    def test_phase_rank_returns_correct_index(self):
        assert _phase_rank("recon") == 0
        assert _phase_rank("exploit") == 3
        assert _phase_rank("report") == 7
        assert _phase_rank("unknown") == -1


class TestWritePhaseWithWorldModel:
    """Integration test: write_phase advances WorldModel hosts."""

    @pytest.fixture
    def sessions_dir(self):
        with tempfile.TemporaryDirectory() as d:
            sdir = Path(d)
            (sdir / "world_model.json").write_text(json.dumps({}))
            original = Path("sessions/world_model.json")
            backup = None
            if original.exists():
                backup = original.read_text()
            try:
                import cli.ops_commands as mod
                old_wm = mod._WORLD_MODEL
                mod._WORLD_MODEL = str(sdir / "world_model.json")
                from modules.world_model import WorldModel, get_world_model
                import modules.world_model as wm_mod
                old_default = wm_mod._default_wm
                wm_mod._default_wm = None
                wm_mod._DEFAULT_PATH = sdir / "world_model.json"
                yield sdir
                wm_mod._default_wm = old_default
                wm_mod._DEFAULT_PATH = old_default
                mod._WORLD_MODEL = old_wm
                if backup is not None:
                    original.write_text(backup)
            finally:
                if backup is not None and original.exists():
                    pass

    def test_write_phase_advances_hosts(self, sessions_dir):
        from modules.world_model import WorldModel, get_world_model
        import modules.world_model as wm_mod
        wm_mod._default_wm = None
        wm_mod._DEFAULT_PATH = sessions_dir / "world_model.json"
        wm = get_world_model()
        wm.add_host("10.0.0.1")

        result = write_phase("enum")
        assert result is True

        host = wm.get_host("10.0.0.1")
        assert host is not None
        assert host.state.value == "enumerated"

    def test_write_phase_invalid_returns_false(self, sessions_dir):
        result = write_phase("not_a_phase")
        assert result is False

    def test_write_phase_completed_phases_tracks_progress(self, sessions_dir):
        import modules.world_model as wm_mod
        wm_mod._default_wm = None
        wm_mod._DEFAULT_PATH = sessions_dir / "world_model.json"
        result = write_phase("recon")
        assert result is True

        world = json.loads((sessions_dir / "world_model.json").read_text())
        assert world.get("current_phase") == "recon"

        result = write_phase("exploit")
        assert result is True

        world = json.loads((sessions_dir / "world_model.json").read_text())
        completed = world.get("completed_phases", [])
        assert "scan" in completed
        assert "enum" in completed
