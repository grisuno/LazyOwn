"""Segmented dispatch sweep: no command may crash the shell on dispatch.

Companion to ``tests/test_shell_boot_smoke.py``. The unit suite never
drives ``LazyOwnShell.cmd`` and the boot smoke covers a curated list;
this test drives a SAMPLE of every indexed command through the real
shell with the executor stubbed, so dispatch-time crashes
(``AttributeError``/``NameError``/``TypeError``) surface in CI.

The sweep runs in segments (one subprocess per segment) because hung
interactive commands accumulate threads in-process. Crashes are compared
against ``tests/dispatch_sweep_baseline.json`` — a fixed name must
either be fixed or explicitly rebased with a reason.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SWEEP = REPO_ROOT / "scripts" / "dispatch_sweep.py"
BASELINE_PATH = REPO_ROOT / "tests" / "dispatch_sweep_baseline.json"

SEGMENT_SIZE = 150
STRIDE = 5


def _count_indexed_commands() -> int:
    result = subprocess.run(
        [sys.executable, str(SWEEP), "--list-names"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr[-300:]
    return len(json.loads(result.stdout))


_TOTAL_COMMANDS = _count_indexed_commands()
_SEGMENTS = [i for i in range(0, _TOTAL_COMMANDS, SEGMENT_SIZE)]


def _run_segment(start: int) -> dict:
    report_path = REPO_ROOT / "sessions" / f"dispatch_sweep_seg{start}.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SWEEP),
            "--start",
            str(start),
            "--limit",
            str(SEGMENT_SIZE),
            "--stride",
            str(STRIDE),
            "--isolated",
            "--report",
            str(report_path),
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=900,
    )
    assert report_path.exists(), f"segment {start} produced no report: {result.stdout[-300:]} {result.stderr[-300:]}"
    return json.loads(report_path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("start", _SEGMENTS, ids=lambda s: f"seg{s}")
def test_segment_no_new_crashes(start: int) -> None:
    """Commands crashing at dispatch must stay within the known baseline."""
    report = _run_segment(start)
    baseline: dict[str, str] = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    new_crashes = {c["name"]: c["error"][:160] for c in report["crashed"] if c["name"] not in baseline}
    assert not new_crashes, "new dispatch crashes:\n" + "\n".join(f"  {n}: {e}" for n, e in sorted(new_crashes.items()))


def test_baseline_covers_known_crashes() -> None:
    """Every baseline entry must still be a real crash (no stale entries)."""
    latest = {}
    for start in _SEGMENTS:
        report_path = REPO_ROOT / "sessions" / f"dispatch_sweep_seg{start}.json"
        if report_path.exists():
            report = json.loads(report_path.read_text(encoding="utf-8"))
            for c in report["crashed"]:
                latest[c["name"]] = c["error"][:160]
    baseline: dict[str, str] = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    stale = sorted(set(baseline) - set(latest))
    assert not stale, f"fixed commands must be removed from the baseline: {stale}"
