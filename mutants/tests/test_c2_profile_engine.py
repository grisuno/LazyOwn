"""Tests for modules/c2_profile_engine.py — TlsProfile, DnsProfile, SmbProfile,
WebSocketProfile, ProfileRotator, ProfileValidator, ProfileEngine.

Covers:
    - Dataclass construction and serialization round-trips
    - TLS JA3 hash computation and cipher suite resolution
    - DNS query subdomain building with various encodings
    - SMB profile validation edge cases
    - WebSocket protocol and path validation
    - ProfileRotator cooldown and skip logic
    - ProfileValidator transport-level checks
    - ProfileEngine composition and rotation
    - ProfileEngine.from_dict and from_payload factory methods
"""

from __future__ import annotations

import pytest

from modules.c2_profile_engine import (
    LIBRARY_CIPHER_SUITES,
    DnsProfile,
    ProfileEngine,
    ProfileRotator,
    ProfileValidator,
    RotationSlot,
    SmbProfile,
    TlsProfile,
    TransportType,
    WebSocketProfile,
)


class TestTlsProfile:
    def test_default_construction(self):
        profile = TlsProfile()
        assert profile.enabled is True
        assert profile.min_version == "1.2"
        assert profile.max_version == "1.3"
        assert profile.ja3_fingerprint_library == "chrome_120"
        assert profile.grease_extensions is True
        assert "h2" in profile.alpn_protocols

    def test_get_cipher_suites_returns_library_defaults(self):
        profile = TlsProfile(ja3_fingerprint_library="firefox_120")
        suites = profile.get_cipher_suites()
        assert len(suites) == 3
        assert "TLS_AES_128_GCM_SHA256" in suites

    def test_get_cipher_suites_returns_custom_when_set(self):
        custom = ["TLS_CUSTOM_SUITE"]
        profile = TlsProfile(cipher_suites=custom)
        assert profile.get_cipher_suites() == custom

    def test_get_cipher_suites_unknown_library_falls_back_to_generic(self):
        profile = TlsProfile(ja3_fingerprint_library="nonexistent_library")
        suites = profile.get_cipher_suites()
        generic = LIBRARY_CIPHER_SUITES["generic_tls"]
        assert suites == generic

    def test_get_ja3_hash_produces_stable_output(self):
        profile = TlsProfile(
            min_version="1.2",
            ja3_fingerprint_library="chrome_120",
            grease_extensions=False,
        )
        hash1 = profile.get_ja3_hash()
        hash2 = profile.get_ja3_hash()
        assert hash1 == hash2
        assert len(hash1) == 32

    def test_get_ja3_hash_with_grease_produces_variable_output(self):
        profile = TlsProfile(grease_extensions=True)
        hashes = {profile.get_ja3_hash() for _ in range(10)}
        assert len(hashes) >= 2

    def test_serialization_roundtrip(self):
        original = TlsProfile(
            enabled=False,
            min_version="1.3",
            cipher_suites=["TLS_AES_256_GCM_SHA384"],
            sni_hostname="cdn.example.com",
        )
        restored = TlsProfile.from_dict(original.to_dict())
        assert restored.enabled == original.enabled
        assert restored.min_version == original.min_version
        assert restored.cipher_suites == original.cipher_suites
        assert restored.sni_hostname == original.sni_hostname

    def test_from_dict_empty(self):
        profile = TlsProfile.from_dict({})
        assert profile.enabled is True

    def test_disabled_profile(self):
        profile = TlsProfile(enabled=False)
        assert profile.enabled is False


class TestDnsProfile:
    def test_default_construction(self):
        profile = DnsProfile()
        assert profile.enabled is False
        assert profile.domain == ""
        assert profile.encoding == "base64"
        assert profile.max_query_length == 63

    def test_build_query_subdomain_base64(self):
        profile = DnsProfile(domain="c2.example.com", encoding="base64")
        sub = profile.build_query_subdomain(b"hello", packet_id=1)
        assert "p1" in sub
        assert "c2.example.com" in sub

    def test_build_query_subdomain_base32(self):
        profile = DnsProfile(domain="dns.c2.org", encoding="base32")
        sub = profile.build_query_subdomain(b"test")
        assert sub.endswith("dns.c2.org")
        assert sub.islower()

    def test_build_query_subdomain_hex(self):
        profile = DnsProfile(domain="exfil.local", encoding="hex")
        sub = profile.build_query_subdomain(b"\xDE\xAD\xBE\xEF")
        assert "deadbeef" in sub

    def test_build_query_subdomain_truncates_to_max_length(self):
        profile = DnsProfile(domain="x.io", encoding="hex", max_query_length=10)
        data = b"A" * 100
        sub = profile.build_query_subdomain(data)
        assert len(sub.replace("x.io", "")) <= 30

    def test_build_query_subdomain_ttl_cache_bypass_disabled(self):
        profile = DnsProfile(domain="dns.c2", ttl_cache_bypass=False)
        sub = profile.build_query_subdomain(b"data")
        assert sub.startswith("c")

    def test_serialization_roundtrip(self):
        original = DnsProfile(
            enabled=True,
            domain="tunnel.example.com",
            encoding="hex",
            query_types=["A", "TXT", "MX"],
        )
        restored = DnsProfile.from_dict(original.to_dict())
        assert restored.enabled == original.enabled
        assert restored.domain == original.domain
        assert restored.encoding == original.encoding
        assert restored.query_types == original.query_types

    def test_from_dict_empty(self):
        profile = DnsProfile.from_dict({})
        assert profile.enabled is False
        assert profile.encoding == "base64"


class TestSmbProfile:
    def test_default_construction(self):
        profile = SmbProfile()
        assert profile.enabled is False
        assert profile.pipe_name == ""
        assert profile.encrypt_traffic is True

    def test_serialization_roundtrip(self):
        original = SmbProfile(
            enabled=True,
            pipe_name=r"\\\.\\pipe\\lazyown",
            domain="CORP",
            username="svc_beacon",
            ntlm_hash="A" * 32,
            retry_count=5,
        )
        restored = SmbProfile.from_dict(original.to_dict())
        assert restored.enabled == original.enabled
        assert restored.pipe_name == original.pipe_name
        assert restored.domain == original.domain
        assert restored.username == original.username
        assert restored.ntlm_hash == original.ntlm_hash
        assert restored.retry_count == 5

    def test_from_dict_empty(self):
        profile = SmbProfile.from_dict({})
        assert profile.enabled is False


class TestWebSocketProfile:
    def test_default_construction(self):
        profile = WebSocketProfile()
        assert profile.enabled is False
        assert profile.protocol == "wss"
        assert profile.path == "/ws/connect"
        assert profile.use_compression is True

    def test_serialization_roundtrip(self):
        original = WebSocketProfile(
            enabled=True,
            protocol="ws",
            path="/api/stream",
            origin="https://legit-site.com",
            subprotocols=["v1", "v2"],
            heartbeat_interval_ms=15000,
        )
        restored = WebSocketProfile.from_dict(original.to_dict())
        assert restored.enabled == original.enabled
        assert restored.protocol == original.protocol
        assert restored.path == original.path
        assert restored.origin == original.origin
        assert restored.subprotocols == original.subprotocols
        assert restored.heartbeat_interval_ms == 15000

    def test_from_dict_empty(self):
        profile = WebSocketProfile.from_dict({})
        assert profile.enabled is False
        assert profile.protocol == "wss"


class TestProfileRotator:
    def test_requires_at_least_one_slot(self):
        with pytest.raises(ValueError, match="at least one"):
            ProfileRotator([])

    def test_single_slot_always_active(self):
        slot = RotationSlot(name="http", transport=TransportType.HTTP)
        rotator = ProfileRotator([slot])
        assert rotator.transport == TransportType.HTTP
        rotated = rotator.rotate()
        assert rotated.name == "http"

    def test_rotation_cycles_through_slots(self):
        slots = [
            RotationSlot(name="a", transport=TransportType.HTTP, cooldown_s=0),
            RotationSlot(name="b", transport=TransportType.DNS, cooldown_s=0),
            RotationSlot(name="c", transport=TransportType.WEBSOCKET, cooldown_s=0),
        ]
        rotator = ProfileRotator(slots)
        assert rotator.transport == TransportType.HTTP
        assert rotator.rotate().transport == TransportType.DNS
        assert rotator.rotate().transport == TransportType.WEBSOCKET
        assert rotator.rotate().transport == TransportType.HTTP

    def test_rotation_skips_cooldown_slots(self):
        cooldown = 10
        slots = [
            RotationSlot(name="a", transport=TransportType.HTTP, cooldown_s=0),
            RotationSlot(name="b", transport=TransportType.DNS, cooldown_s=cooldown),
        ]
        rotator = ProfileRotator(slots)
        rotator.rotate()
        current = rotator.current_slot
        assert current.name == "b"
        rotator.rotate()
        second = rotator.current_slot
        assert second.name == "a"

    def test_rotation_resets_all_cooldowns_when_all_busy(self):
        slots = [
            RotationSlot(name="x", transport=TransportType.HTTP, cooldown_s=999999),
            RotationSlot(name="y", transport=TransportType.DNS, cooldown_s=999999),
        ]
        rotator = ProfileRotator(slots)
        rotator.rotate()
        rotator.rotate()
        after = rotator.current_slot
        assert after.name == "x"

    def test_list_slots(self):
        slots = [
            RotationSlot(name="http", transport=TransportType.HTTP),
            RotationSlot(name="dns", transport=TransportType.DNS),
        ]
        rotator = ProfileRotator(slots)
        info = rotator.list_slots()
        assert len(info) == 2
        assert info[0]["active"] is True
        assert info[1]["active"] is False

    def test_is_available_fresh_slot(self):
        slot = RotationSlot(name="fresh", transport=TransportType.HTTP)
        assert slot.is_available() is True

    def test_is_available_after_touch(self):
        slot = RotationSlot(name="touched", transport=TransportType.HTTP, cooldown_s=10)
        slot.touch()
        assert slot.is_available() is False

    def test_current_slot_identity(self):
        slots = [
            RotationSlot(name="first", transport=TransportType.HTTP),
        ]
        rotator = ProfileRotator(slots)
        assert rotator.current_slot is rotator.current_slot


class TestProfileValidator:
    def test_validate_tls_valid(self):
        validator = ProfileValidator()
        profile = TlsProfile(enabled=True, min_version="1.2", max_version="1.3")
        assert validator.validate_tls(profile) == []

    def test_validate_tls_disabled_skips(self):
        validator = ProfileValidator()
        profile = TlsProfile(enabled=False, min_version="1.0", max_version="9.9")
        assert validator.validate_tls(profile) == []

    def test_validate_tls_invalid_version(self):
        validator = ProfileValidator()
        profile = TlsProfile(enabled=True, min_version="1.0")
        errors = validator.validate_tls(profile)
        assert len(errors) >= 1

    def test_validate_tls_missing_key_with_cert(self):
        validator = ProfileValidator()
        profile = TlsProfile(
            enabled=True,
            certificate_path="/tmp/fake_cert.pem",
            key_path="",
        )
        errors = validator.validate_tls(profile)
        assert any("key_path" in e.lower() for e in errors)

    def test_validate_tls_unknown_library(self):
        validator = ProfileValidator()
        profile = TlsProfile(
            enabled=True,
            ja3_fingerprint_library="made_up_browser",
        )
        errors = validator.validate_tls(profile)
        assert any("ja3_fingerprint_library" in e for e in errors)

    def test_validate_dns_enabled_missing_domain(self):
        validator = ProfileValidator()
        profile = DnsProfile(enabled=True, domain="")
        errors = validator.validate_dns(profile)
        assert any("domain" in e.lower() for e in errors)

    def test_validate_dns_invalid_encoding(self):
        validator = ProfileValidator()
        profile = DnsProfile(enabled=True, domain="c2.test.com", encoding="rot13")
        errors = validator.validate_dns(profile)
        assert any("encoding" in e.lower() for e in errors)

    def test_validate_dns_disabled_skips(self):
        validator = ProfileValidator()
        profile = DnsProfile(enabled=False)
        assert validator.validate_dns(profile) == []

    def test_validate_dns_invalid_domain_format(self):
        validator = ProfileValidator()
        profile = DnsProfile(enabled=True, domain="not-a-valid-domain")
        errors = validator.validate_dns(profile)
        assert any("domain" in e.lower() for e in errors)

    def test_validate_smb_missing_pipe_name(self):
        validator = ProfileValidator()
        profile = SmbProfile(enabled=True, pipe_name="")
        errors = validator.validate_smb(profile)
        assert any("pipe_name" in e.lower() for e in errors)

    def test_validate_smb_disabled_skips(self):
        validator = ProfileValidator()
        profile = SmbProfile(enabled=False, pipe_name="", retry_count=0)
        assert validator.validate_smb(profile) == []

    def test_validate_smb_username_without_domain(self):
        validator = ProfileValidator()
        profile = SmbProfile(
            enabled=True,
            pipe_name=r"\\\.\\pipe\\test",
            username="admin",
            domain="",
        )
        errors = validator.validate_smb(profile)
        assert any("domain" in e.lower() for e in errors)

    def test_validate_websocket_invalid_protocol(self):
        validator = ProfileValidator()
        profile = WebSocketProfile(enabled=True, protocol="ftp")
        errors = validator.validate_websocket(profile)
        assert any("protocol" in e.lower() for e in errors)

    def test_validate_websocket_disabled_skips(self):
        validator = ProfileValidator()
        profile = WebSocketProfile(enabled=False, protocol="ftp", path="bad")
        assert validator.validate_websocket(profile) == []

    def test_validate_all_returns_dict(self):
        validator = ProfileValidator()
        result = validator.validate_all(
            tls=TlsProfile(),
            dns=DnsProfile(),
            smb=SmbProfile(),
            websocket=WebSocketProfile(),
        )
        assert set(result.keys()) == {"tls", "dns", "smb", "websocket"}
        for errors in result.values():
            assert isinstance(errors, list)
            assert len(errors) == 0


class TestProfileEngine:
    def test_default_engine_has_http_slot(self):
        engine = ProfileEngine()
        assert engine.active_transport == TransportType.HTTP

    def test_engine_with_all_transports(self):
        engine = ProfileEngine(
            tls_profile=TlsProfile(enabled=True),
            dns_profile=DnsProfile(enabled=True, domain="c2.test.com"),
            smb_profile=SmbProfile(enabled=True, pipe_name=r"\\\.\\pipe\\beacon"),
            websocket_profile=WebSocketProfile(enabled=True),
        )
        assert engine.tls_profile.enabled is True
        assert engine.dns_profile.enabled is True

    def test_engine_validate_returns_errors_for_invalid_dns(self):
        engine = ProfileEngine(
            dns_profile=DnsProfile(enabled=True, domain=""),
        )
        errors = engine.validate()
        assert "dns" in errors
        assert len(errors["dns"]) > 0

    def test_engine_rotate_through_transports(self):
        engine = ProfileEngine(
            dns_profile=DnsProfile(enabled=True, domain="c2.test.com"),
        )
        engine.rotate()
        assert engine.active_transport == TransportType.DNS

    def test_engine_get_active_profile_dict(self):
        engine = ProfileEngine()
        profile = engine.get_active_profile_dict()
        assert "transport" in profile
        assert "tls" in profile

    def test_engine_get_all_profiles_dict(self):
        engine = ProfileEngine()
        all_profiles = engine.get_all_profiles_dict()
        assert "tls" in all_profiles
        assert "dns" in all_profiles
        assert "smb" in all_profiles
        assert "websocket" in all_profiles
        assert "rotation" in all_profiles

    def test_engine_from_dict(self):
        raw = {
            "c2_tls": {"enabled": True, "min_version": "1.3"},
            "c2_dns": {"enabled": True, "domain": "dns.c2.io"},
            "c2_smb": {},
            "c2_websocket": {},
        }
        engine = ProfileEngine.from_dict(raw)
        assert engine.tls_profile.enabled is True
        assert engine.tls_profile.min_version == "1.3"
        assert engine.dns_profile.enabled is True
        assert engine.dns_profile.domain == "dns.c2.io"

    def test_engine_from_payload(self):
        payload = {
            "c2_tls": {"enabled": False},
            "c2_dns": {"enabled": False},
            "c2_smb": {},
            "c2_websocket": {},
        }
        engine = ProfileEngine.from_payload(payload)
        assert engine.tls_profile.enabled is False

    def test_engine_empty_payload_falls_back_to_defaults(self):
        engine = ProfileEngine.from_payload({})
        assert engine.tls_profile.enabled is True
        assert engine.active_transport == TransportType.HTTP
