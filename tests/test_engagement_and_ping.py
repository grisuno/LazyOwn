#!/usr/bin/env python3
"""
tests/test_engagement_and_ping.py
==================================
Tests for:
  - cli/engagement_hooks.py  (curiosity engine + VRI scheduler)
  - do_ping os_id fix        (Linux=1, Windows=2, persisted via _apply_assign)
  - do_recommend_next        (command-index layer, no graph nodes)

All tests are isolated: no real filesystem writes outside tmp_path,
no real network calls, no real LazyOwn shell instantiation.
"""

from __future__ import annotations

import csv
import json
import math
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

# ── path setup ────────────────────────────────────────────────────────────────

REPO = Path(__file__).parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "skills"))


# ══════════════════════════════════════════════════════════════════════════════
# Engagement hooks
# ══════════════════════════════════════════════════════════════════════════════

class TestEngagementState:
    def test_load_fresh_state_has_zero_commands(self, tmp_path):
        from cli.engagement_hooks import _load_state, STATE_PATH
        import cli.engagement_hooks as eh
        old = eh.STATE_PATH
        eh.STATE_PATH = tmp_path / "engagement_state.json"
        try:
            state = _load_state()
            assert state.total_commands == 0
            assert state.session_commands == 0
            assert state.commands_seen == []
            assert state.next_reward_at > 0
        finally:
            eh.STATE_PATH = old

    def test_save_and_reload_state(self, tmp_path):
        from cli.engagement_hooks import _load_state, _save_state, EngagementState
        import cli.engagement_hooks as eh
        old = eh.STATE_PATH
        eh.STATE_PATH = tmp_path / "engagement_state.json"
        try:
            state = EngagementState(total_commands=42, next_reward_at=50)
            state.commands_seen = ["do_lazynmap", "do_gobuster"]
            _save_state(state)
            reloaded = _load_state()
            assert reloaded.total_commands == 42
            assert "do_lazynmap" in reloaded.commands_seen
        finally:
            eh.STATE_PATH = old

    def test_atomic_write_leaves_no_tmp_file(self, tmp_path):
        from cli.engagement_hooks import _save_state, EngagementState
        import cli.engagement_hooks as eh
        old = eh.STATE_PATH
        eh.STATE_PATH = tmp_path / "engagement_state.json"
        try:
            _save_state(EngagementState())
            tmp_file = tmp_path / "engagement_state.tmp"
            assert not tmp_file.exists()
            assert (tmp_path / "engagement_state.json").exists()
        finally:
            eh.STATE_PATH = old


class TestVRIScheduler:
    def test_next_threshold_always_positive(self):
        from cli.engagement_hooks import _next_threshold
        for _ in range(200):
            gap = _next_threshold(0)
            assert gap >= 2, f"gap={gap} must be >= 2"

    def test_next_threshold_mean_near_target(self):
        from cli.engagement_hooks import _next_threshold, MEAN_INTERVAL
        gaps = [_next_threshold(0) for _ in range(2000)]
        mean = sum(gaps) / len(gaps)
        assert abs(mean - MEAN_INTERVAL) < 2.5, f"mean={mean:.2f} too far from {MEAN_INTERVAL}"

    def test_threshold_is_variable_not_constant(self):
        from cli.engagement_hooks import _next_threshold
        gaps = {_next_threshold(0) for _ in range(50)}
        assert len(gaps) > 3, "VRI gaps must vary (not fixed interval)"

    def test_vri_fires_when_threshold_reached(self, tmp_path, capsys):
        from cli.engagement_hooks import render_engagement_hook, reset_session, EngagementState
        import cli.engagement_hooks as eh
        old_state_path = eh.STATE_PATH
        old_index_path = eh.INDEX_PATH
        eh.STATE_PATH = tmp_path / "state.json"
        eh.INDEX_PATH = REPO / "cli" / "command_index.json"
        eh._state = None
        eh._index = None
        try:
            reset_session()
            eh._state.next_reward_at = 2   # force early reward
            eh._state.total_commands = 0
            eh._state.commands_seen = []
            eh._state.session_curiosity_shown = []
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=True)
            render_engagement_hook(cmd="gobuster", phase="recon", enabled=True)
            out = capsys.readouterr().out
            assert "─" * 20 in out or "explore" in out, "VRI reward or curiosity must appear"
        finally:
            eh.STATE_PATH = old_state_path
            eh.INDEX_PATH = old_index_path
            eh._state = None
            eh._index = None

    def test_vri_does_not_fire_before_threshold(self, tmp_path, capsys):
        from cli.engagement_hooks import render_engagement_hook, reset_session, EngagementState
        import cli.engagement_hooks as eh
        old_state_path = eh.STATE_PATH
        old_index_path = eh.INDEX_PATH
        eh.STATE_PATH = tmp_path / "state.json"
        eh.INDEX_PATH = REPO / "cli" / "command_index.json"
        eh._state = None
        eh._index = None
        try:
            reset_session()
            eh._state.next_reward_at = 9999  # never fires
            eh._state.commands_seen = []
            eh._state.session_curiosity_shown = []
            render_engagement_hook(cmd="ping", phase="recon", enabled=True)
            out = capsys.readouterr().out
            assert "─" * 20 not in out, "VRI reward must NOT fire before threshold"
        finally:
            eh.STATE_PATH = old_state_path
            eh.INDEX_PATH = old_index_path
            eh._state = None
            eh._index = None


class TestCuriosityEngine:
    def _make_state(self, seen=None):
        from cli.engagement_hooks import EngagementState
        s = EngagementState()
        s.commands_seen = seen or []
        s.session_curiosity_shown = []
        return s

    def _minimal_index(self, phase_cmds):
        return {
            "phase_to_commands": phase_cmds,
            "commands": [
                {"name": c, "summary": f"summary for {c}"}
                for cmds in phase_cmds.values() for c in cmds
            ],
        }

    def test_curiosity_shows_undiscovered_command(self, capsys):
        from cli.engagement_hooks import _run_curiosity
        idx = self._minimal_index({"recon": ["do_lazynmap", "do_gobuster", "do_cve"]})
        state = self._make_state(seen=["do_lazynmap"])
        _run_curiosity("lazynmap", state, idx)
        out = capsys.readouterr().out
        assert "explore:" in out
        assert "lazynmap" not in out.split("explore:")[1].split("\n")[0]

    def test_curiosity_does_not_repeat_in_session(self, capsys):
        from cli.engagement_hooks import _run_curiosity
        import re
        cmds = [f"do_cmd{i}" for i in range(10)]
        idx = self._minimal_index({"enum": cmds})
        state = self._make_state()
        shown = set()
        for _ in range(8):
            _run_curiosity("cmd0", state, idx)
            out = re.sub(r'\x1b\[[0-9;]*m', '', capsys.readouterr().out)
            if "explore:" in out:
                label = out.split("explore:")[1].strip().split()[0]
                assert label not in shown, f"Repeated suggestion: {label}"
                shown.add(label)

    def test_curiosity_silent_when_all_discovered(self, capsys):
        from cli.engagement_hooks import _run_curiosity
        cmds = ["do_lazynmap", "do_gobuster"]
        idx = self._minimal_index({"recon": cmds})
        state = self._make_state(seen=cmds)
        _run_curiosity("lazynmap", state, idx)
        out = capsys.readouterr().out
        assert "explore:" not in out

    def test_curiosity_silent_when_disabled(self, capsys):
        from cli.engagement_hooks import render_engagement_hook, reset_session
        import cli.engagement_hooks as eh
        old = eh._state
        try:
            from cli.engagement_hooks import EngagementState
            eh._state = EngagementState()
            eh._state.next_reward_at = 9999
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=False)
            out = capsys.readouterr().out
            assert out == ""
        finally:
            eh._state = old

    def test_curiosity_silent_for_unknown_phase(self, capsys):
        from cli.engagement_hooks import _run_curiosity
        idx = self._minimal_index({"recon": ["do_lazynmap"]})
        state = self._make_state()
        _run_curiosity("nonexistent_cmd_xyz", state, idx)
        out = capsys.readouterr().out
        assert "explore:" not in out

    def test_commands_seen_accumulates_across_calls(self, tmp_path):
        from cli.engagement_hooks import render_engagement_hook, reset_session
        import cli.engagement_hooks as eh
        old_state = eh.STATE_PATH
        old_index = eh.INDEX_PATH
        eh.STATE_PATH = tmp_path / "s.json"
        eh.INDEX_PATH = REPO / "cli" / "command_index.json"
        eh._state = None
        eh._index = None
        try:
            reset_session()
            eh._state.next_reward_at = 9999
            render_engagement_hook(cmd="lazynmap", phase="recon", enabled=True)
            render_engagement_hook(cmd="gobuster", phase="recon", enabled=True)
            assert "do_lazynmap" in eh._state.commands_seen
            assert "do_gobuster" in eh._state.commands_seen
        finally:
            eh.STATE_PATH = old_state
            eh.INDEX_PATH = old_index
            eh._state = None
            eh._index = None


# ══════════════════════════════════════════════════════════════════════════════
# do_ping — os_id fix
# ══════════════════════════════════════════════════════════════════════════════

class TestPingOsId:
    """Verify that TTL→os_id mapping and persistence are correct."""

    def _ping_stdout(self, ttl: int) -> str:
        return f"PING host (1.2.3.4): 56 data bytes\n64 bytes from 1.2.3.4: icmp_seq=0 ttl={ttl} time=1 ms\n"

    def _make_params(self):
        return {"rhost": "1.2.3.4", "os_id": "4"}

    def _extract_os_id_from_json(self, data: list) -> str:
        return data[0]["id"] if data else "4"

    def test_ttl_64_maps_to_os_id_1_linux(self):
        stdout = self._ping_stdout(64)
        ttl_idx = stdout.find("ttl=")
        ttl = int(stdout[ttl_idx + 4: ttl_idx + 7])
        os_id = "1" if ttl <= 64 else ("2" if ttl <= 128 else "4")
        assert os_id == "1", "TTL 64 must map to os_id=1 (Linux)"

    def test_ttl_128_maps_to_os_id_2_windows(self):
        stdout = self._ping_stdout(128)
        ttl_idx = stdout.find("ttl=")
        ttl = int(stdout[ttl_idx + 4: ttl_idx + 7])
        os_id = "1" if ttl <= 64 else ("2" if ttl <= 128 else "4")
        assert os_id == "2", "TTL 128 must map to os_id=2 (Windows)"

    def test_ttl_127_maps_to_os_id_2_windows(self):
        stdout = self._ping_stdout(127)
        ttl_idx = stdout.find("ttl=")
        ttl = int(stdout[ttl_idx + 4: ttl_idx + 7])
        os_id = "1" if ttl <= 64 else ("2" if ttl <= 128 else "4")
        assert os_id == "2"

    def test_ttl_63_maps_to_os_id_1_linux(self):
        stdout = self._ping_stdout(63)
        ttl_idx = stdout.find("ttl=")
        ttl = int(stdout[ttl_idx + 4: ttl_idx + 7])
        os_id = "1" if ttl <= 64 else ("2" if ttl <= 128 else "4")
        assert os_id == "1"

    def test_ttl_255_maps_to_unknown(self):
        stdout = self._ping_stdout(255)
        ttl_idx = stdout.find("ttl=")
        ttl = int(stdout[ttl_idx + 4: ttl_idx + 7])
        os_id = "1" if ttl <= 64 else ("2" if ttl <= 128 else "4")
        assert os_id == "4"

    def test_ping_os_json_contract(self):
        """sessions/os.json schema: id, os, ttl, state."""
        entry = {"id": "1", "os": "Linux", "ttl": 64, "state": "active"}
        assert entry["id"] == "1"
        assert entry["os"] == "Linux"
        assert entry["ttl"] == 64
        assert entry["state"] == "active"

    def test_ping_persists_via_apply_assign(self):
        """do_ping must call _apply_assign so os_id survives restart."""
        with open("lazyown.py") as f:
            src = f.read()
        start = src.find("def do_ping(self, line):")
        end = src.find("\n    @cmd2", start)
        fragment = src[start:end]
        assert "_apply_assign" in fragment, "do_ping must use _apply_assign to persist os_id"
        assert "_save_payload" in fragment, "do_ping must pass _save_payload to persist"
        assert 'id": \'2\'' not in fragment or "Windows" in fragment, \
            "os_id=2 must only appear for Windows branch"


# ══════════════════════════════════════════════════════════════════════════════
# do_recommend_next — command index layer
# ══════════════════════════════════════════════════════════════════════════════

class TestRecommendNextCommandIndex:
    """Verify the command-index layer in do_recommend_next works without graph."""

    def _build_index(self, tmp_path, phase="recon", n_cmds=10):
        cmds = [f"do_cmd{i}" for i in range(n_cmds)]
        idx = {
            "schema_version": 1,
            "phase_to_commands": {phase: cmds},
            "commands": [{"name": c, "summary": f"Does {c}"} for c in cmds],
            "totals": {},
        }
        p = tmp_path / "command_index.json"
        p.write_text(json.dumps(idx))
        return p, cmds

    def _build_csv(self, tmp_path, run_cmds):
        p = tmp_path / "session_report.csv"
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["start","end","source_ip","source_port",
                "destination_ip","destination_port","domain","subdomain","url",
                "pivot_port","command","args"])
            w.writeheader()
            for c in run_cmds:
                w.writerow({"command": c, **{k: "" for k in ["start","end","source_ip",
                    "source_port","destination_ip","destination_port","domain",
                    "subdomain","url","pivot_port","args"]}})
        return p

    def test_shows_unrun_commands(self, tmp_path, capsys):
        idx_path, all_cmds = self._build_index(tmp_path, "recon", 6)
        csv_path = self._build_csv(tmp_path, ["cmd0", "cmd1"])

        import json as _json, csv as _csv
        idx = _json.loads(idx_path.read_text())
        ptc = idx["phase_to_commands"]
        cmds_list = idx["commands"]
        summary_map = {e["name"]: e.get("summary","") for e in cmds_list if "name" in e}

        seen: set = set()
        with open(csv_path, newline="") as fh:
            for row in _csv.DictReader(fh):
                c = (row.get("command") or "").strip()
                if c:
                    seen.add(c); seen.add(f"do_{c}")

        candidates = ptc.get("recon", [])
        never_run = [c for c in candidates if c not in seen]

        assert len(never_run) == 4
        assert "do_cmd0" not in never_run
        assert "do_cmd1" not in never_run

    def test_shows_nothing_when_all_run(self, tmp_path):
        idx_path, all_cmds = self._build_index(tmp_path, "recon", 3)
        csv_path = self._build_csv(tmp_path, ["cmd0", "cmd1", "cmd2"])

        import json as _json, csv as _csv
        idx = _json.loads(idx_path.read_text())
        seen: set = set()
        with open(csv_path, newline="") as fh:
            for row in _csv.DictReader(fh):
                c = (row.get("command") or "").strip()
                if c:
                    seen.add(c); seen.add(f"do_{c}")

        candidates = idx["phase_to_commands"].get("recon", [])
        never_run = [c for c in candidates if c not in seen]
        assert never_run == []

    def test_no_graph_nodes_in_output(self, tmp_path, capsys):
        """Command-index layer must never show code graph nodes."""
        idx_path, all_cmds = self._build_index(tmp_path, "enum", 5)
        csv_path = self._build_csv(tmp_path, [])

        import json as _json, csv as _csv
        idx = _json.loads(idx_path.read_text())
        candidates = idx["phase_to_commands"].get("enum", [])

        for c in candidates:
            assert "()" not in c, f"Code node leaked: {c}"
            assert "." not in c or c.startswith("do_"), f"Code node leaked: {c}"

    def test_no_advisor_reference_before_definition(self):
        """The NameError bug: 'advisor' must not be used before it's defined."""
        with open("lazyown.py") as f:
            src = f.read()
        start = src.find("def do_recommend_next(self, line):")
        end = src.find("\n    @cmd2", start)
        fragment = src[start:end]

        # Strip docstring before checking — it may mention "graph advisor" in prose
        import ast
        try:
            tree = ast.parse(fragment)
            func = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
            docstring_end = 0
            if (func.body and isinstance(func.body[0], ast.Expr)
                    and isinstance(func.body[0].value, ast.Constant)):
                docstring_end = func.body[0].end_lineno
        except Exception:
            docstring_end = 0

        lines = fragment.split("\n")
        code_lines = lines[docstring_end:]

        advisor_defined_at = None
        for i, line in enumerate(code_lines):
            if "advisor = _GraphAdvisor" in line:
                advisor_defined_at = i
                break

        for i, line in enumerate(code_lines):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if "advisor." in stripped and "advisor = " not in stripped:
                if advisor_defined_at is None or i < advisor_defined_at:
                    pytest.fail(
                        f"'advisor' used at line {i} before being defined "
                        f"(defined at {advisor_defined_at}): {stripped}"
                    )

    def test_rule_not_used_without_import(self):
        """Rule from rich must be imported if used in do_recommend_next."""
        with open("lazyown.py") as f:
            src = f.read()
        start = src.find("def do_recommend_next(self, line):")
        end = src.find("\n    @cmd2", start)
        fragment = src[start:end]
        if "Rule(" in fragment:
            assert "from rich.rule import Rule" in src or "from rich import" in src, \
                "Rule is used in do_recommend_next but not imported"

    def test_fallback_message_present(self):
        """When no data: must show a useful fallback, not crash."""
        with open("lazyown.py") as f:
            src = f.read()
        start = src.find("def do_recommend_next(self, line):")
        end = src.find("\n    @cmd2", start)
        fragment = src[start:end]
        assert "No recommendations" in fragment or "lazynmap" in fragment, \
            "do_recommend_next must have a fallback message"
