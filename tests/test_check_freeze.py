"""Freeze gate contract: the surface baseline only shrinks during a freeze."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_freeze_gate_passes_on_current_tree():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "check_freeze.py")],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_freeze_gate_fails_when_surface_grows(tmp_path, monkeypatch):
    import json

    import scripts.check_freeze as gate

    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps({"commands": 1, "addons": 1, "tools": 1}))
    monkeypatch.setattr(gate, "BASELINE_PATH", baseline_path)
    monkeypatch.setattr(gate, "_live_counts", lambda: {"commands": 2, "addons": 1, "tools": 1})
    monkeypatch.setattr(sys, "argv", ["check_freeze.py"])

    assert gate.main() == 1


def test_freeze_gate_update_rewrites_baseline(tmp_path, monkeypatch):
    import json

    import scripts.check_freeze as gate

    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps({"commands": 1, "addons": 1, "tools": 1}))
    monkeypatch.setattr(gate, "BASELINE_PATH", baseline_path)
    monkeypatch.setattr(gate, "_live_counts", lambda: {"commands": 2, "addons": 1, "tools": 1})
    monkeypatch.setattr(sys, "argv", ["check_freeze.py", "--update"])

    assert gate.main() == 0
    saved = json.loads(baseline_path.read_text())
    assert saved == {"commands": 2, "addons": 1, "tools": 1}
