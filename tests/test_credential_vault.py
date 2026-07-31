"""Tests for core/credential_vault.py"""

from __future__ import annotations

import os
from pathlib import Path

from core.credential_vault import (
    DANGEROUS_DEFAULTS,
    SENSITIVE_KEYS,
    check_dangerous_defaults,
    generate_secure_defaults,
    seal_payload,
    seal_value,
    unseal_payload,
    unseal_value,
)


class TestCheckDefaults:
    def test_default_values_detected(self):
        payload = {"c2_pass": "CHANGE_ME", "api_key": "", "backdoor_password": "CHANGE_ME"}
        warnings = check_dangerous_defaults(payload)
        assert len(warnings) >= 3

    def test_clean_payload_no_warnings(self):
        payload = {
            "c2_pass": "Str0ng!Pass#2024",
            "api_key": "gsk_abc123",
            "backdoor_password": "Str0ng!B@ckd00r",
            "backdoor_username": "svc_backup",
            "email_password": "EmailP@ss123",
            "start_pass": "St@rtP@ss456",
            "start_user": "op_user",
            "start_user_pass": "Us3rP@ss789",
            "rat_key": "abcd1234efgh5678",
        }
        warnings = check_dangerous_defaults(payload)
        assert len(warnings) == 0, f"Expected no warnings but got: {warnings}"

    def test_empty_keys_flagged(self):
        payload = {"c2_pass": "", "api_key": ""}
        warnings = check_dangerous_defaults(payload)
        assert len(warnings) > 0

    def test_changeme_variants(self):
        payload = {
            "c2_pass": "changeme",
            "start_pass": "CHANGE_ME",
            "backdoor_password": "mySecureBackdoor789!",
            "backdoor_username": "svc",
            "api_key": "gsk_test",
        }
        warnings = check_dangerous_defaults(payload)
        assert len(warnings) >= 2, f"Expected at least 2 warnings, got {len(warnings)}: {warnings}"


class TestSealUnseal:
    def test_roundtrip(self):
        key = os.urandom(32)
        encrypted = seal_value("SuperSecret123", key)
        assert encrypted != "SuperSecret123"
        decrypted = unseal_value(encrypted, key)
        assert decrypted == "SuperSecret123"

    def test_empty_string_passthrough(self):
        assert seal_value("") == ""
        assert unseal_value("") == ""

    def test_plaintext_passthrough(self):
        result = unseal_value("not_sealed_plaintext")
        assert result == "not_sealed_plaintext"

    def test_different_key_fails(self):
        key1 = os.urandom(32)
        key2 = os.urandom(32)
        encrypted = seal_value("MyPassword", key1)
        assert encrypted != "MyPassword"
        result = unseal_value(encrypted, key2)
        assert result != "MyPassword"

    def test_payload_roundtrip(self):
        key = os.urandom(32)
        payload = {
            "c2_pass": "secret_c2",
            "api_key": "gsk_mykey",
            "rhost": "10.10.11.5",
            "lhost": "10.10.14.3",
            "aes_key": key.hex(),
        }
        sealed = seal_payload(payload, key)
        assert sealed["rhost"] == "10.10.11.5"
        assert sealed["c2_pass"] != "secret_c2"

        unsealed = unseal_payload(sealed, key)
        assert unsealed["c2_pass"] == "secret_c2"
        assert unsealed["api_key"] == "gsk_mykey"
        assert unsealed["rhost"] == "10.10.11.5"

    def test_sensitive_keys_encrypted(self):
        key = os.urandom(32)
        payload = {k: f"secret_{k}" for k in SENSITIVE_KEYS}
        payload["public_key"] = "visible"
        sealed = seal_payload(payload, key)
        assert sealed["public_key"] == "visible"
        for k in SENSITIVE_KEYS:
            assert sealed[k] != f"secret_{k}"

    def test_non_sensitive_keys_untouched(self):
        key = os.urandom(32)
        payload = {"rhost": "10.10.11.5", "lport": 4444, "domain": "htb.local"}
        sealed = seal_payload(payload, key)
        assert sealed["rhost"] == "10.10.11.5"
        assert sealed["lport"] == 4444
        assert sealed["domain"] == "htb.local"


class TestSecureDefaults:
    def test_generates_random_values(self):
        defaults = generate_secure_defaults()
        for key in ("c2_pass", "backdoor_password", "rat_key"):
            assert defaults[key] != ""
            assert "CHANGE_ME" not in defaults[key]
            assert len(defaults[key]) >= 16

    def test_api_key_is_longer(self):
        defaults = generate_secure_defaults()
        assert len(defaults.get("api_key", "")) > 16
