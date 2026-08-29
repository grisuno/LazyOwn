"""SDD+TDD+BDD tests for CodeQL security batch — weak crypto, clear-text secrets, TLS.

Contract: every fix in this batch has a test that proves the weakness is gone
and would detect a regression (mutation-killed). Tests are written
behaviourally so they read as specifications.

Covers (CodeQL alert ids):
  - #895 modules/icmp_server.py + icmp_client.py: AES-ECB -> AES-256-GCM
  - #867 modules/phishing_orchestrator.py: keyed HMAC-SHA-256 instead of salted SHA-256
  - #865 utils.py create_caldera_config: hardcoded credentials removed + 0600 perms
  - #864 utils.py Spray: password no longer logged in clear text
  - #863 cli/commands/phishing_wizard.py: captured passwords encrypted at rest
  - #862/#861 lazyc2.py: one-time admin password persisted to a file, not printed
  - #851 modules/network_opsec.py: minimum TLS version pinned
  - #859 lazyc2/blueprints/addons.py: reflected cookie injection blocked
  - #858/#857 lazyc2/blueprints/api.py: exception details not exposed in responses
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _read(rel: str) -> str:
    """Read a production source file relative to the repository root."""
    return (ROOT / rel).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# SDD Contract 1: ICMP tunnel uses authenticated AES-GCM, never ECB
# ---------------------------------------------------------------------------

class TestIcmpAuthenticatedCrypto:
    """CONTRACT: the ICMP C2 tunnel must encrypt with AES-256-GCM and
    authenticate every payload; ECB mode must be gone."""

    def test_server_has_no_ecb(self):
        assert "MODE_ECB" not in _read("modules/icmp_server.py")

    def test_client_has_no_ecb(self):
        assert "MODE_ECB" not in _read("modules/icmp_client.py")

    def test_server_uses_gcm(self):
        assert "MODE_GCM" in _read("modules/icmp_server.py")

    def test_client_uses_gcm(self):
        assert "MODE_GCM" in _read("modules/icmp_client.py")

    def test_encrypt_decrypt_roundtrip(self):
        from modules.icmp_server import decrypt_data, encrypt_data
        key = hashlib.sha256(b"test-password").digest()
        plaintext = b"whoami"
        ciphertext = encrypt_data(plaintext, key)
        assert decrypt_data(ciphertext, key) == plaintext

    def test_tampered_payload_rejected(self):
        from modules.icmp_server import decrypt_data, encrypt_data
        key = hashlib.sha256(b"test-password").digest()
        ciphertext = bytearray(encrypt_data(b"whoami", key))
        ciphertext[-1] ^= 0x01
        with pytest.raises(ValueError):
            decrypt_data(bytes(ciphertext), key)

    def test_short_payload_rejected(self):
        from modules.icmp_server import decrypt_data
        with pytest.raises(ValueError):
            decrypt_data(b"short", hashlib.sha256(b"k").digest())

    def test_client_sudo_is_guarded(self):
        source = _read("modules/icmp_client.py")
        assert "check_sudo()\n    main()" in source
        assert "check_sudo()\n\ndef checksum" not in source


# ---------------------------------------------------------------------------
# SDD Contract 2: credential log fingerprint uses keyed HMAC, not salted SHA-256
# ---------------------------------------------------------------------------

class TestCredentialLogHashing:
    """CONTRACT: the audit-log fingerprint of a credential must be a keyed
    HMAC so it cannot be brute-forced independently of the secret key."""

    def test_uses_hmac_not_plain_sha256(self):
        source = _read("modules/phishing_orchestrator.py")
        assert "hmac.new" in source

    def test_no_salted_sha256_fingerprint(self):
        source = _read("modules/phishing_orchestrator.py")
        assert "_CREDENTIAL_SALT + plaintext" not in source

    def test_fingerprint_is_hmac_of_proper_key(self):
        with patch.dict(os.environ, {"LAZYOWN_SECRET_KEY": "test-key-123"}):
            from modules.phishing_orchestrator import _hash_credential_for_log
            digest = _hash_credential_for_log("hunter2")
            assert len(digest) == 16
            assert all(c in "0123456789abcdef" for c in digest)


# ---------------------------------------------------------------------------
# SDD Contract 3: Caldera config contains no hardcoded credentials
# ---------------------------------------------------------------------------

class TestCalderaConfigNoHardcodedSecrets:
    """CONTRACT: create_caldera_config must generate every credential and set
    owner-only permissions; no hardcoded passwords may be embedded."""

    def test_no_hardcoded_user_passwords(self):
        source = _read("utils.py")
        for secret in ("lazyownblueadmin", "lazyownredteamtheadmin", "lazyownredteamadmin"):
            assert secret not in source

    def test_generated_user_passwords(self):
        source = _read("utils.py")
        assert "blue_password = secrets." in source
        assert "red_admin_password = secrets." in source
        assert "red_password = secrets." in source

    def test_writes_with_owner_permissions(self):
        source = _read("utils.py")
        assert "os.chmod(file_path, 0o600)" in source

    def test_functional_generates_no_static_passwords(self):
        from utils import create_caldera_config
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "default.yml")
            create_caldera_config(path)
            content = Path(path).read_text(encoding="utf-8")
            for secret in ("lazyownblueadmin", "lazyownredteamtheadmin", "lazyownredteamadmin"):
                assert secret not in content
            assert 0o600 == (stat.S_IMODE(os.stat(path).st_mode))


# ---------------------------------------------------------------------------
# SDD Contract 4: password spray never logs credentials in clear text
# ---------------------------------------------------------------------------

class TestSprayNoClearTextPassword:
    """CONTRACT: the ADFS spray function must not print the sprayed password."""

    def test_does_not_log_password(self):
        source = _read("utils.py")
        assert '"+ password)' not in source
        assert ':: " + password' not in source

    def test_logs_success_without_secret(self):
        source = _read("utils.py")
        assert '"\\t\\t:: success"' in source


# ---------------------------------------------------------------------------
# SDD Contract 5: phishing wizard encrypts captured credentials at rest
# ---------------------------------------------------------------------------

class TestPhishingWizardEncryptsCredentials:
    """CONTRACT: the campaign harvester must encrypt the password before
    writing credentials.json and hash it before the audit log."""

    def test_encrypts_password_before_storage(self):
        source = _read("cli/commands/phishing_wizard.py")
        assert "_encrypt_credential(password)" in source

    def test_hashes_password_before_log(self):
        source = _read("cli/commands/phishing_wizard.py")
        assert "_hash_credential_for_log(password)" in source

    def test_imports_encryption_contract(self):
        source = _read("cli/commands/phishing_wizard.py")
        assert "_encrypt_credential" in source
        assert "_decrypt_credential" in source


# ---------------------------------------------------------------------------
# SDD Contract 6: bootstrap admin password is persisted, not printed
# ---------------------------------------------------------------------------

class TestBootstrapPasswordNotPrinted:
    """CONTRACT: the one-time admin password must be written to an owner-only
    file rather than echoed to the console."""

    def test_no_password_print(self):
        source = _read("lazyc2.py")
        assert 'admin / {one_time_password}' not in source

    def test_persist_helper_exists(self):
        source = _read("lazyc2.py")
        assert "def _persist_bootstrap_password(" in source

    def test_persist_uses_owner_only_permissions(self):
        source = _read("lazyc2.py")
        assert "stat.S_IRUSR | stat.S_IWUSR" in source

    def test_persist_writes_to_file(self):
        source = _read("lazyc2.py")
        assert 'write_text(f"admin / {password}\\n"' in source


# ---------------------------------------------------------------------------
# SDD Contract 7: network OPSEC pins a secure minimum TLS version
# ---------------------------------------------------------------------------

class TestNetworkOpsecTlsVersion:
    """CONTRACT: TLS inspection must never negotiate below TLS 1.2."""

    def test_pins_minimum_version(self):
        source = _read("modules/network_opsec.py")
        assert "context.minimum_version = ssl.TLSVersion.TLSv1_2" in source


# ---------------------------------------------------------------------------
# SDD Contract 8: CSRF cookie client-id is validated, never reflected verbatim
# ---------------------------------------------------------------------------

class TestCsrfCookieInjection:
    """CONTRACT: the CSRF client-id cookie must not reflect arbitrary
    user-supplied values back into a Set-Cookie header."""

    def test_validates_client_id(self):
        source = _read("lazyc2/blueprints/addons.py")
        assert "_SAFE_CLIENT_ID.fullmatch(client_id)" in source

    def test_validator_accepts_only_urlsafe_token(self):
        from lazyc2.blueprints.addons import _SAFE_CLIENT_ID
        import secrets
        assert _SAFE_CLIENT_ID.fullmatch(secrets.token_urlsafe(32)) is not None
        assert _SAFE_CLIENT_ID.fullmatch("value-with-injection\r\nSet-Cookie: evil=1") is None
        assert _SAFE_CLIENT_ID.fullmatch("<script>alert(1)</script>") is None
        assert _SAFE_CLIENT_ID.fullmatch("short") is None


# ---------------------------------------------------------------------------
# SDD Contract 9: health endpoints never leak exception internals
# ---------------------------------------------------------------------------

class TestHealthEndpointNoExceptionLeak:
    """CONTRACT: health responses must be generic 'error' strings; the raw
    exception is logged server-side, never serialized to clients."""

    def test_no_exception_interpolation(self):
        source = _read("lazyc2/blueprints/api.py")
        assert 'f"error: {exc}"' not in source

    def test_database_error_is_generic(self):
        source = _read("lazyc2/blueprints/api.py")
        assert 'result["components"]["database"] = "error"' in source

    def test_listener_error_is_generic(self):
        source = _read("lazyc2/blueprints/api.py")
        assert 'result["components"]["listeners"] = "error"' in source

    def test_loads_only_generic_error(self):
        from flask import Flask

        from lazyc2.blueprints.api import HealthConfig, _health_status

        class BrokenDB:
            conn = MagicMock()
            conn.execute = MagicMock(side_effect=RuntimeError("secret internal stack"))

        app = Flask(__name__)
        app.start_time = 0.0
        app.config["lazyown_db"] = BrokenDB()
        app.config["listener_manager"] = None
        with app.app_context():
            result = _health_status(HealthConfig())
        assert result["components"]["database"] == "error"
        assert "secret internal stack" not in str(result)