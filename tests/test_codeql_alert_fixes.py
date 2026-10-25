"""Regression tests for CodeQL alerts 984, 983 and 982."""

from __future__ import annotations

import json

import modules.retry_session as retry_session
from modules.chain_distill import _infer_target, _is_doc_example
from modules.world_model import read_state_dict, write_state_dict


class TestWorldModelEncryptedAtRest:
    """Alert 984: sensitive state must never persist in clear text."""

    def test_write_is_fernet_not_json(self, tmp_path, monkeypatch):
        monkeypatch.delenv("LAZYOWN_MASTER_PASSWORD", raising=False)
        path = tmp_path / "world_model.json"
        assert write_state_dict(path, {"credentials": [{"password": "P@ssw0rd!"}], "hosts": {}}) is True
        raw = path.read_text()
        assert raw.startswith("gAAAAA")
        assert "P@ssw0rd" not in raw

    def test_roundtrip_decrypt(self, tmp_path, monkeypatch):
        monkeypatch.delenv("LAZYOWN_MASTER_PASSWORD", raising=False)
        path = tmp_path / "world_model.json"
        document = {"hosts": {"10.0.0.1": {"state": "owned"}}, "current_phase": "exploit"}
        assert write_state_dict(path, document) is True
        assert read_state_dict(path) == document

    def test_legacy_plain_json_still_readable(self, tmp_path, monkeypatch):
        monkeypatch.delenv("LAZYOWN_MASTER_PASSWORD", raising=False)
        path = tmp_path / "world_model.json"
        path.write_text(json.dumps({"hosts": {}, "phase": "enum"}), encoding="utf-8")
        assert read_state_dict(path).get("phase") == "enum"

    def test_legacy_autocrypto_sibling_readable(self, tmp_path, monkeypatch):
        monkeypatch.setenv("LAZYOWN_MASTER_PASSWORD", "op-secret")
        path = tmp_path / "world_model.json"
        salt_path = tmp_path / ".auto_crypto_salt"
        salt_path.write_bytes(bytes(range(16)))
        from cryptography.fernet import Fernet

        import modules.world_model as wm

        key = wm._derive_crypto_key("op-secret", bytes(range(16)))
        document = {"hosts": {"10.0.0.2": {"state": "scanned"}}}
        (tmp_path / "world_model.json.encrypted").write_text(
            Fernet(key).encrypt(json.dumps(document).encode()).decode("ascii")
        )
        assert read_state_dict(path) == document

    def test_restricted_mode_after_write(self, tmp_path, monkeypatch):
        monkeypatch.delenv("LAZYOWN_MASTER_PASSWORD", raising=False)
        path = tmp_path / "world_model.json"
        write_state_dict(path, {"hosts": {}})
        assert (path.stat().st_mode & 0o777) == 0o600

    def test_refuses_persist_without_key_material(self, tmp_path, monkeypatch):
        import modules.world_model as wm

        monkeypatch.delenv("LAZYOWN_MASTER_PASSWORD", raising=False)
        monkeypatch.setattr(wm, "_master_password", lambda: None)
        path = tmp_path / "world_model.json"
        assert write_state_dict(path, {"credentials": [{"password": "x"}]}) is False
        assert not path.exists()

    def test_device_secret_created_used_then_readable(self, tmp_path, monkeypatch):
        import modules.cli_auth as cli_auth
        import modules.world_model as wm

        monkeypatch.delenv("LAZYOWN_MASTER_PASSWORD", raising=False)
        monkeypatch.setattr(cli_auth, "get_current_operator", lambda: None)
        monkeypatch.setattr(wm, "_SESSIONS_DIR", tmp_path)
        monkeypatch.setattr(wm, "_SALT_RELATIVE", ".auto_crypto_salt")
        salt = tmp_path / ".auto_crypto_salt"
        salt.write_bytes(bytes(range(16)))
        path = tmp_path / "world_model.json"
        document = {"hosts": {"1.2.3.4": {"state": "owned"}}}
        assert write_state_dict(path, document) is True
        assert read_state_dict(path) == document
        secret = tmp_path / ".state_secret"
        assert secret.is_file()
        assert (secret.stat().st_mode & 0o777) == 0o600


class TestSudoSegmentRegexLinear:
    """Alert 983: segment sudo rewrite keeps semantics, kills backtracking."""

    def test_rewrites_leading_sudo(self):
        assert retry_session._rewrite_segment("sudo nmap -sS 10.0.0.1") == "sudo -A nmap -sS 10.0.0.1"

    def test_env_prefix_sudo_rewrites(self):
        for segment in ["FOO=1 sudo scan", "A=x sudo true", "  sudo ls", "sudo"]:
            assert "sudo -A" in retry_session._rewrite_segment(segment)

    def test_bare_mid_sentence_untouched(self):
        assert retry_session._rewrite_segment("echo sudo stays intact") == "echo sudo stays intact"

    def test_scored_marker_never_matched(self):
        assert retry_session._rewrite_segment("sudoa") == "sudoa"
        assert retry_session._rewrite_segment("no sudo here") == "no sudo here"


class TestDocExampleDomainSanitize:
    """Alert 982: example.com placeholder exclusion is label-precise."""

    def test_exact_and_subdomains_excluded(self):
        assert _is_doc_example("example.com") is True
        assert _is_doc_example("api.example.com") is True
        assert _is_doc_example("www.example.com.") is True

    def test_lookalikes_not_matched(self):
        assert _is_doc_example("evilexample.com") is False
        assert _is_doc_example("notexample.com") is False
        assert _is_doc_example("10.0.0.9") is False

    def test_goal_prefers_real_host_over_examples(self):
        rows: list[dict] = []
        placeholder_goal = {"goal": "attack api.example.com now, host 10.0.0.9"}
        assert _infer_target(rows, placeholder_goal) == "10.0.0.9"
        lookalike_goal = {"goal": "attack evilexample.com then host 10.0.0.9"}
        assert _infer_target(rows, lookalike_goal) == "evilexample.com"
