"""Tests for modules/unified_dashboard.py."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.unified_dashboard import UnifiedDashboard, get_unified_dashboard


class TestUnifiedDashboardInit:
    def test_default_init(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        assert dash._sessions_dir == tmp_path

    def test_get_unified_dashboard_singleton(self, tmp_path):
        dash1 = get_unified_dashboard(tmp_path)
        dash2 = get_unified_dashboard(tmp_path)
        assert dash1 is dash2


class TestWorldModelCollection:
    def test_collect_world_model_exists(self, tmp_path):
        wm_data = {"hosts": {"10.0.0.1": {"state": "scanned"}}, "credentials": []}
        (tmp_path / "world_model.json").write_text(json.dumps(wm_data))
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        result = dash._collect_world_model()
        assert "hosts" in result
        assert "10.0.0.1" in result["hosts"]

    def test_collect_world_model_missing(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        result = dash._collect_world_model()
        assert result == {}


class TestDaemonStatus:
    def test_collect_daemon_status_exists(self, tmp_path):
        status = {"current_phase": "exploit", "pending_objectives": [1, 2]}
        (tmp_path / "autonomous_status.json").write_text(json.dumps(status))
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        result = dash._collect_daemon_status()
        assert result["current_phase"] == "exploit"
        assert len(result["pending_objectives"]) == 2

    def test_collect_daemon_status_missing(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        result = dash._collect_daemon_status()
        assert result == {}


class TestUnifiedSnapshot:
    def test_snapshot_keys(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        snap = dash.build_unified_snapshot()
        expected_keys = {
            "world_model", "hive_status", "policy_status",
            "daemon_status", "live_graph", "graph_advice",
            "dashboard", "timestamp",
        }
        assert expected_keys.issubset(set(snap.keys()))

    def test_snapshot_timestamp(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        snap = dash.build_unified_snapshot()
        assert "timestamp" in snap
        assert snap["timestamp"] != ""


class TestRenderUnified:
    def test_render_contains_header(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        output = dash.render_unified()
        assert "LAZYOWN UNIFIED CAMPAIGN DASHBOARD" in output

    def test_render_contains_sections(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        output = dash.render_unified()
        assert "[World Model]" in output
        assert "[Hive Mind]" in output
        assert "[Daemon]" in output
        assert "[Policy]" in output
        assert "[GraphAdvisor]" in output

    def test_render_contains_timestamp(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        output = dash.render_unified()
        assert "Updated:" in output


class TestExportJson:
    def test_export_json(self, tmp_path):
        dash = UnifiedDashboard(sessions_dir=tmp_path)
        result = dash.export_json()
        data = json.loads(result)
        assert "world_model" in data
        assert "timestamp" in data
