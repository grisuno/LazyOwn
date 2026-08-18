"""BDD-style tests for the unified kill-chain snapshot contract.

Scenario: a single, render-agnostic snapshot drives every surface (CLI,
Flask dashboard, GUI2, API) from one source of truth, and reads state
transparently whether persisted plaintext or auto-encrypted at rest.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path

from modules.killchain import KillChain


def _seed_snapshot(path, phase: str, completed: list[str], current: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "phase": phase,
        "current_phase": current or phase,
        "completed_phases": completed,
        "hosts": {
            "10.10.10.10": {
                "ip": "10.10.10.10",
                "state": "exploited",
                "os_hint": "linux",
                "services": {},
                "notes": [],
                "cloud_metadata": {},
            }
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def _states(snapshot: dict) -> dict:
    return {p["key"]: p["status"] for p in snapshot["progress"]}


def _encrypt_at(path, password: str, salt: bytes) -> None:
    """Encrypt a plain JSON file into an in-place ``.encrypted`` sibling."""
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100_000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    Path(str(path) + ".encrypted").write_bytes(Fernet(key).encrypt(path.read_bytes()))


class TestKillChainSnapshot:
    def test_empty_snapshot_defaults_to_recon(self, tmp_path):
        # Given: no world model state exists
        path = tmp_path / "world_model.json"
        # When: a snapshot is requested
        snap = KillChain.snapshot(world_model_path=path)
        # Then: the phase resolves to recon, recon is active, the rest pending
        assert snap["current_phase"] == "recon"
        states = _states(snap)
        assert states["recon"] == "active"
        assert all(p == "pending" for key, p in states.items() if key != "recon")

    def test_snapshot_reflects_explicit_phase_and_completed(self, tmp_path):
        # Given: operator advanced to exploit and completed recon/scan/enum
        path = tmp_path / "world_model.json"
        _seed_snapshot(path, "exploit", ["recon", "scan", "enum"])
        # When: a snapshot is derived
        snap = KillChain.snapshot(world_model_path=path)
        # Then: recon/scan/enum are done, exploit is active, the rest pending
        states = _states(snap)
        assert states["recon"] == "done"
        assert states["scan"] == "done"
        assert states["enum"] == "done"
        assert states["exploit"] == "active"
        assert states["privesc"] == "pending"
        assert snap["current_phase"] == "exploit"
        assert "recon" in snap["completed_phases"]

    def test_snapshot_is_json_serialisable(self, tmp_path):
        # Given: a seeded world state
        path = tmp_path / "world_model.json"
        _seed_snapshot(path, "enum", ["recon"])
        # When: the snapshot is dumped to JSON
        text = json.dumps(snap := KillChain.snapshot(world_model_path=path))
        # Then: it round-trips without error and carries the compact glyph
        assert json.loads(text)["compact"]
        assert isinstance(snap["progress"], list)

    def test_advance_then_snapshot_is_consistent(self, tmp_path):
        # Given: a recognised phase is advanced on disk
        path = tmp_path / "world_model.json"
        _seed_snapshot(path, "recon", [])
        assert KillChain.advance_phase("exploit", world_model_path=path)
        # When: a snapshot is derived
        snap = KillChain.snapshot(world_model_path=path)
        # Then: it reflects the advanced phase and completion ordering
        assert snap["current_phase"] == "exploit"
        assert snap["completed_phases"] == ["recon", "scan", "enum"]


class TestEncryptedStateTransparency:
    def test_read_state_dict_decrypts_at_rest(self, tmp_path, monkeypatch):
        from modules.world_model import read_state_dict, write_state_dict

        # Given: a world state persisted plaintext
        plain = tmp_path / "world_model.json"
        seed = {"phase": "lateral", "completed_phases": ["recon", "scan", "enum", "exploit", "privesc"]}
        assert write_state_dict(plain, seed)
        assert plain.exists()
        # Given: it is then auto-encrypted in place at rest
        salt = b"0123456789abcdef"
        (tmp_path / ".auto_crypto_salt").write_bytes(salt)
        _encrypt_at(plain, "s3cret", salt)
        plain.unlink()
        # When: read_state_dict is called from a domain that knows the password
        monkeypatch.setenv("LAZYOWN_MASTER_PASSWORD", "s3cret")
        data = read_state_dict(plain)
        # Then: the decrypted payload matches the original seed
        assert data.get("phase") == "lateral"
        assert data.get("completed_phases") == seed["completed_phases"]

    def test_missing_file_reads_empty(self, tmp_path):
        from modules.world_model import read_state_dict

        # When: no plaintext and no encrypted sibling exist
        data = read_state_dict(tmp_path / "nope.json")
        # Then: an empty state dict is returned
        assert data == {}

    def test_encrypted_without_password_reads_empty(self, tmp_path, monkeypatch):
        from modules.world_model import read_state_dict

        # Given: an existing plaintext state is encrypted at rest
        plain = tmp_path / "world_model.json"
        plain.parent.mkdir(parents=True, exist_ok=True)
        plain.write_text(json.dumps({"phase": "enum"}), encoding="utf-8")
        salt = b"0123456789abcdef"
        (tmp_path / ".auto_crypto_salt").write_bytes(salt)
        _encrypt_at(plain, "pw", salt)
        plain.unlink()
        monkeypatch.delenv("LAZYOWN_MASTER_PASSWORD", raising=False)
        # When: read_state_dict is called
        data = read_state_dict(plain)
        # Then: it degrades gracefully to an empty dict
        assert data == {}
