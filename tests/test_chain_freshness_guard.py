"""Freshness guards for chain skips: stale artefacts do not skip work.

Every scenario states Given, When, Then. ``skip_if_exists`` stays the
forever-guard by default; a step declaring ``skip_max_age`` re-runs
when the artefact is older than its window.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from modules.chain_registry import Chain, ChainStep, skip_pending, validate_chain
from modules.chain_runner import ChainRunner


def _file(path: Path, payload: bytes, mtime: float) -> Path:
    """Write an artefact with a fixed mtime."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    os.utime(path, (mtime, mtime))
    return path


def test_skip_pending_fresh_and_forever(tmp_path: Path):
    """Given an existing artefact, When the guard reads, Then max-age 0 always skips."""
    path = _file(tmp_path / "nmap.xml", b"<a/>", time.time() - 5)
    assert skip_pending(str(path), 0) == f"exists: {path}"
    assert skip_pending(str(path), 60, now=time.time()) == f"exists: {path}"


def test_skip_pending_stale_artifact_runs(tmp_path: Path):
    """Given a very old artefact, When the window is short, Then the step must run."""
    path = _file(tmp_path / "nmap.xml", b"<a/>", time.time() - 4000)
    assert skip_pending(str(path), 60) is None
    assert skip_pending(str(path), 3600) is None


def test_missing_artifact_runs(tmp_path: Path):
    """Given no artefact, When the guard reads, Then the step runs."""
    assert skip_pending(str(tmp_path / "nmap.xml"), 0) is None


def test_schema_validates_skip_max_age():
    """Given a negative or oversized max age, When validating, Then the file is rejected."""
    for bad in (-1, 365 * 86400 + 1, True):
        errors = validate_chain(
            {
                "name": "demo",
                "steps": [{"run": "scan {target}", "skip_if_exists": "sessions/scan_{target}.nmap.xml",
                           "skip_max_age": bad}],
            },
            filename="demo",
        )
        assert any("skip_max_age" in row for row in errors)
    ok = validate_chain(
        {
            "name": "demo",
            "steps": [{"run": "scan {target}", "skip_if_exists": "sessions/scan_{target}.nmap.xml",
                       "skip_max_age": 86400}],
        },
        filename="demo",
    )
    assert ok == []


def test_runner_reexecutes_stale_step(tmp_path: Path):
    """Given a stale artefact, When the chain runs, Then the step executes again."""
    _file(tmp_path / "scan.nmap.xml", b"old", time.time() - 5000)
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        return "scanned"

    chain = Chain(
        name="demo",
        defaults={"target": "10.0.0.9", "artifact": str(tmp_path / "scan.nmap.xml")},
        steps=[ChainStep(id="scan", run="scan {target} --out {artifact}", skip_if_exists="{artifact}",
                          skip_max_age=60)],
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True
    assert len(calls) == 1
    assert calls[0] == "scan 10.0.0.9 --out " + str(tmp_path / "scan.nmap.xml")


def test_runner_skips_fresh_step(tmp_path: Path):
    """Given a fresh artefact, When the chain runs, Then the step is skipped."""
    _file(tmp_path / "scan.nmap.xml", b"new", time.time())
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        return "scanned"

    chain = Chain(
        name="demo",
        defaults={"target": "10.0.0.9", "artifact": str(tmp_path / "scan.nmap.xml")},
        steps=[ChainStep(id="scan", run="scan {target} --out {artifact}", skip_if_exists="{artifact}",
                          skip_max_age=3600)],
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True
    assert calls == []
    assert result.steps[0].status == "skipped"
