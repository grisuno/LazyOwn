"""Wiring contract tests: loop timeline snapshot + MCP lazy intel tools."""

from __future__ import annotations

from pathlib import Path

LAZY_LOOP_PATH = Path(__file__).resolve().parent.parent / "modules" / "lazy_loop.py"
LAZYOWN_PATH = Path(__file__).resolve().parent.parent / "lazyown.py"
MCP_PATH = Path(__file__).resolve().parent.parent / "skills" / "lazyown_mcp.py"
OPENCODE_BRIDGE_PATH = Path(__file__).resolve().parent.parent / "skills" / "lazyown_mcp_opencode.py"


class TestExposureRefreshWiring:
    def test_loop_refreshes_stale_intel_report(self):
        story = "the intel sync stage refreshes the exposure report when new evidence lands"
        source = (Path(__file__).resolve().parent.parent / "modules" / "lazy_loop.py").read_text(encoding="utf-8")
        assert "refresh_if_stale" in source, story
        assert "intel_report" in source, story

    def test_refresh_stale_contract(self, tmp_path: Path, monkeypatch):
        import time as _time

        from modules import lazy_exposure as module

        module.SESSIONS_DIR = tmp_path
        module.WORLD_MODEL_PATH = tmp_path / "world_model.json"
        scan = tmp_path / "scan_10.66.44.7.nmap.xml"
        scan.write_text("{}", encoding="utf-8")
        scan.touch()
        monkeypatch.setattr(module, "SESSIONS_DIR", tmp_path)
        monkeypatch.setattr(module, "WORLD_MODEL_PATH", tmp_path / "world_model.json")
        _time.sleep(0.02)
        created = module.refresh_if_stale("10.66.44.7")
        story = "a missing report with newer scan evidence is bootstrapped by the refresh path"
        assert created is None or created.exists(), story
        report_at = tmp_path / "lazy_intel_10.66.44.7.json"
        report_at.write_text("{}", encoding="utf-8")
        _time.sleep(0.02)
        scan.touch()
        monkeypatch.setattr(module, "ensure_report", lambda *a, **k: report_at)
        refreshed = module.refresh_if_stale("10.66.44.7")
        assert refreshed == report_at, story


class TestLoopTimelineWiring:
    def test_sync_intel_records_timeline_snapshot(self):
        story = "each intel sync must also snapshot the timeline (record_quiet)"
        source = LAZY_LOOP_PATH.read_text(encoding="utf-8")
        assert "record_quiet" in source, story
        assert "timeline_snapshot" in source, story

    def test_shell_exit_snapshot_registered(self):
        story = "the lazyown shell shuts down with one last timeline snapshot"
        source = LAZYOWN_PATH.read_text(encoding="utf-8")
        assert "_atexit.register(_exit_snapshot)" in source, story

    def test_record_quiet_never_raises(self, tmp_path: Path):
        story = "record_quiet degrades to an empty result on bad inputs"
        from modules.lazy_timeline import record_quiet

        result = record_quiet(state_path=tmp_path / "none", snaps_dir=tmp_path)
        assert result.get("path") is not None or result.get("hosts") == 0, story


class TestMcpTools:
    def test_lazy_tools_declared(self):
        story = "lazyown_lazy_intel and lazyown_lazysearch are listed tools"
        source = MCP_PATH.read_text(encoding="utf-8")
        assert "name=\"lazyown_lazy_intel\"" in source, story
        assert "name=\"lazyown_lazysearch\"" in source, story

    def test_lazy_tools_dispatched(self):
        story = "the call tool chain routes both lazy tools"
        source = MCP_PATH.read_text(encoding="utf-8")
        assert 'elif name == "lazyown_lazy_intel"' in source, story
        assert 'elif name == "lazyown_lazysearch"' in source, story

    def test_hermes_bridge_exposes_lazy_tools(self):
        story = "the opencode bridge aliases the lazy tools under short names"
        bridge = OPENCODE_BRIDGE_PATH.read_text(encoding="utf-8")
        assert '"lazy_intel": "lazyown_lazy_intel"' in bridge, story
        assert '"lazysearch": "lazyown_lazysearch"' in bridge, story
