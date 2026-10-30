"""Chain distillation custody contract: replayed steps pin their evidence.

A distilled step that referenced ``sessions/`` artefacts carries the
artefact paths as ``evidence`` with sha256 digests in
``evidence_sha256``; the chain runner verifies those digests at replay,
so regenerated or tampered artefacts fail loudly instead of passing
silently.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from modules.chain_distill import _artifact_pins, build_chain_data
from modules.chain_registry import Chain, ChainStep
from modules.chain_runner import ChainRunner


def _write_artifact(sessions_dir: Path, name: str, payload: bytes) -> Path:
    """Create one session artefact for a pin scenario."""
    sessions_dir.mkdir(parents=True, exist_ok=True)
    path = sessions_dir / name
    path.write_bytes(payload)
    return path


def _pinned_step(digest: str) -> ChainStep:
    """Build the pinned evidence step for the tamper scenario."""
    return ChainStep(
        id="scan",
        run="printf pinned",
        evidence=["sessions/scan_10.0.0.9.nmap.xml"],
        evidence_sha256={"sessions/scan_10.0.0.9.nmap.xml": digest},
    )


def test_pins_hash_referenced_session_artifacts(tmp_path, monkeypatch):
    """Given a command referencing a session artefact, When distilling, Then the digest pins it."""
    import modules.chain_distill as distill

    _write_artifact(tmp_path / "sessions", "scan_10.0.0.9.nmap.xml", b"<nmaprun/>")
    monkeypatch.setattr(distill, "REPO_ROOT", tmp_path, raising=False)
    digest = hashlib.sha256(b"<nmaprun/>").hexdigest()
    assert _artifact_pins("lazynmap -oX sessions/scan_10.0.0.9.nmap.xml", "", "10.0.0.9") == {
        "sessions/scan_10.0.0.9.nmap.xml": digest
    }


def test_pins_tokenized_paths_resolve_target(tmp_path, monkeypatch):
    """Given a tokenized path and a target, When hashing, Then the real file is read."""
    import modules.chain_distill as distill

    _write_artifact(tmp_path / "sessions", "scan_10.0.0.9.nmap.xml", b"<nmaprun/>")
    monkeypatch.setattr(distill, "REPO_ROOT", tmp_path, raising=False)
    digest = hashlib.sha256(b"<nmaprun/>").hexdigest()
    assert _artifact_pins("lazynmap -oX sessions/scan_{target}.nmap.xml {target}", "", "10.0.0.9") == {
        "sessions/scan_{target}.nmap.xml": digest
    }


def test_missing_and_oversized_artifacts_are_skipped(tmp_path, monkeypatch):
    """Given absent or oversized artefacts, When hashing, Then they produce no pins."""
    import modules.chain_distill as distill

    _write_artifact(tmp_path / "sessions", "big.bin", b"a" * (distill._MAX_ARTIFACT_BYTES + 1))
    monkeypatch.setattr(distill, "REPO_ROOT", tmp_path, raising=False)
    assert _artifact_pins("view sessions/absent.bin sessions/big.bin", "", "10.0.0.9") == {}


def test_build_chain_data_attaches_evidence_pins(tmp_path, monkeypatch):
    """Given a kept nmap row, When building the chain, Then the step carries evidence pins."""
    import modules.chain_distill as distill

    _write_artifact(tmp_path / "sessions", "scan_10.0.0.9.nmap.xml", b"<nmaprun/>")
    monkeypatch.setattr(distill, "REPO_ROOT", tmp_path, raising=False)
    row = {
        "kind": "bash",
        "command": "lazynmap 10.0.0.9 -oX sessions/scan_10.0.0.9.nmap.xml",
        "output": "scan written",
        "digest": "deadbeef",
        "meta": {"intent": 1},
        "truncated": False,
    }
    graph = {"goal": "attack 10.0.0.9", "intents": {"1": "scan the host"}}
    data, _decisions = distill.build_chain_data("t0001", [row], graph)
    steps = data["steps"]
    assert steps[0]["evidence"] == ["sessions/scan_10.0.0.9.nmap.xml"]
    assert steps[0]["evidence_sha256"] == {
        "sessions/scan_10.0.0.9.nmap.xml": hashlib.sha256(b"<nmaprun/>").hexdigest()
    }
    assert distill.validate_chain(data, filename=data["name"]) == []


def test_verify_rejects_tampered_evidence_at_replay(tmp_path, monkeypatch):
    """Given a pinned step, When the artefact changes, Then verification fails loudly."""
    artifact = _write_artifact(tmp_path / "sessions", "scan_10.0.0.9.nmap.xml", b"<nmaprun/>")
    digest = hashlib.sha256(b"<nmaprun/>").hexdigest()
    monkeypatch.chdir(tmp_path)
    chain = Chain(name="demo", defaults={"target": "10.0.0.9"}, steps=[_pinned_step(digest)])
    result = ChainRunner(
        chain,
        tokens={"target": "10.0.0.9"},
        executor=lambda _command: "pinned",
        checkpoint_dir=tmp_path / "checkpoints",
    ).run()
    assert result.ok is True

    artifact.write_bytes(b"<nmaprun tampered/>")
    replay = ChainRunner(
        Chain(name="demo", defaults={"target": "10.0.0.9"}, steps=[_pinned_step(digest)]),
        tokens={"target": "10.0.0.9"},
        executor=lambda _command: "pinned",
        checkpoint_dir=tmp_path / "checkpoints",
    ).run()
    step_outcome = replay.steps[0]
    assert step_outcome.status == "failed"
    assert "hash mismatch" in step_outcome.reason
