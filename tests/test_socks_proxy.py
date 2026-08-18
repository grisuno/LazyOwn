"""Tests for modules/socks_proxy.py — SocksProxyConfig, SocksSession,
SocksValidator, SocksProxyEngine, SocksAuthMethod, SocksCommand,
SocksAddressType, SocksReply.

Covers:
    - SocksProxyConfig construction and serialization roundtrip
    - SocksSession byte counting and elapsed time
    - SocksValidator config validation edge cases
    - SocksValidator request validation with access control
    - SocksProxyEngine session lifecycle (create, track, expire)
    - SocksProxyEngine build_spec and validation
    - SocksProxyEngine from_dict and from_payload factories
    - SocksReply enum messages
    - Enum value assertions
"""

from __future__ import annotations

from modules.socks_proxy import (
    SOCKS_DEFAULT_BIND_ADDRESS,
    SOCKS_DEFAULT_BIND_PORT,
    SocksAddressType,
    SocksAuthMethod,
    SocksCommand,
    SocksProxyConfig,
    SocksProxyEngine,
    SocksReply,
    SocksSession,
    SocksValidator,
)


class TestSocksProxyConfig:
    def test_default_construction(self):
        config = SocksProxyConfig()
        assert config.bind_address == SOCKS_DEFAULT_BIND_ADDRESS
        assert config.bind_port == SOCKS_DEFAULT_BIND_PORT
        assert SocksAuthMethod.NO_AUTH in config.auth_methods
        assert config.max_connections == 32
        assert config.denied_ports == [22, 3389]

    def test_serialization_roundtrip(self):
        original = SocksProxyConfig(
            bind_address="0.0.0.0",
            bind_port=9050,
            auth_methods=[SocksAuthMethod.NO_AUTH, SocksAuthMethod.USERNAME_PASSWORD],
            username="proxy_user",
            password="proxy_pass",
            max_connections=64,
            session_timeout_seconds=600,
            bandwidth_limit_bps=1048576,
            allow_localhost=False,
            allow_private_ranges=True,
            allowed_ports=[80, 443, 8080],
            denied_ports=[22],
            log_connections=False,
        )
        restored = SocksProxyConfig.from_dict(original.to_dict())
        assert restored.bind_address == original.bind_address
        assert restored.bind_port == original.bind_port
        assert restored.auth_methods == original.auth_methods
        assert restored.username == original.username
        assert restored.password == original.password
        assert restored.max_connections == original.max_connections
        assert restored.session_timeout_seconds == original.session_timeout_seconds
        assert restored.bandwidth_limit_bps == original.bandwidth_limit_bps
        assert restored.allow_localhost == original.allow_localhost
        assert restored.allow_private_ranges == original.allow_private_ranges
        assert restored.allowed_ports == original.allowed_ports
        assert restored.denied_ports == original.denied_ports
        assert restored.log_connections == original.log_connections

    def test_from_dict_empty(self):
        config = SocksProxyConfig.from_dict({})
        assert config.bind_address == SOCKS_DEFAULT_BIND_ADDRESS
        assert config.bind_port == SOCKS_DEFAULT_BIND_PORT

    def test_from_dict_unknown_auth_method_handled(self):
        config = SocksProxyConfig.from_dict({"auth_methods": ["UNKNOWN_METHOD"]})
        assert len(config.auth_methods) == 1
        assert SocksAuthMethod.NO_AUTH in config.auth_methods


class TestSocksSession:
    def test_construction_and_defaults(self):
        session = SocksSession(
            session_id="sess_001",
            target_host="10.0.0.1",
            target_port=80,
            beacon_client_id="beacon_abc",
        )
        assert session.session_id == "sess_001"
        assert session.bytes_sent == 0
        assert session.bytes_received == 0
        assert session.elapsed_seconds >= 0

    def test_byte_counters(self):
        session = SocksSession("s1", "example.com", 443, "b1")
        session.bytes_sent = 1024
        session.bytes_received = 2048
        assert session.bytes_sent == 1024
        assert session.bytes_received == 2048

    def test_to_dict(self):
        session = SocksSession("s1", "target.io", 8080, "beacon_x")
        d = session.to_dict()
        assert d["session_id"] == "s1"
        assert d["target_host"] == "target.io"
        assert d["target_port"] == 8080
        assert d["beacon_client_id"] == "beacon_x"
        assert "elapsed_seconds" in d

    def test_elapsed_seconds_with_zero_timestamp(self):
        session = SocksSession("s0", "h", 1, "b")
        session.created_at = 0.0
        assert session.elapsed_seconds == 0.0


class TestSocksValidator:
    def test_valid_config_passes(self):
        validator = SocksValidator()
        config = SocksProxyConfig()
        errors = validator.validate_config(config)
        assert errors == []

    def test_invalid_bind_address(self):
        validator = SocksValidator()
        config = SocksProxyConfig(bind_address="not-an-ip")
        errors = validator.validate_config(config)
        assert any("bind_address" in e.lower() for e in errors)

    def test_invalid_bind_port(self):
        validator = SocksValidator()
        config = SocksProxyConfig(bind_port=99999)
        errors = validator.validate_config(config)
        assert any("bind_port" in e.lower() for e in errors)

    def test_max_connections_zero(self):
        validator = SocksValidator()
        config = SocksProxyConfig(max_connections=0)
        errors = validator.validate_config(config)
        assert any("max_connections" in e.lower() for e in errors)

    def test_session_timeout_too_low(self):
        validator = SocksValidator()
        config = SocksProxyConfig(session_timeout_seconds=2)
        errors = validator.validate_config(config)
        assert any("session_timeout" in e.lower() for e in errors)

    def test_session_timeout_too_high(self):
        validator = SocksValidator()
        config = SocksProxyConfig(session_timeout_seconds=999999)
        errors = validator.validate_config(config)
        assert any("session_timeout" in e.lower() for e in errors)

    def test_negative_bandwidth(self):
        validator = SocksValidator()
        config = SocksProxyConfig(bandwidth_limit_bps=-100)
        errors = validator.validate_config(config)
        assert any("bandwidth_limit_bps" in e.lower() for e in errors)

    def test_username_password_without_credentials(self):
        validator = SocksValidator()
        config = SocksProxyConfig(
            auth_methods=[SocksAuthMethod.USERNAME_PASSWORD],
            username="",
            password="",
        )
        errors = validator.validate_config(config)
        assert any("username" in e.lower() for e in errors)

    def test_no_auth_methods(self):
        validator = SocksValidator()
        config = SocksProxyConfig(auth_methods=[])
        errors = validator.validate_config(config)
        assert any("auth_method" in e.lower() for e in errors)

    def test_invalid_allowed_ports(self):
        validator = SocksValidator()
        config = SocksProxyConfig(allowed_ports=[0, 99999])
        errors = validator.validate_config(config)
        assert len(errors) >= 2

    def test_port_in_both_lists(self):
        validator = SocksValidator()
        config = SocksProxyConfig(allowed_ports=[80], denied_ports=[80])
        errors = validator.validate_config(config)
        assert any("both allowed_ports and denied_ports" in e.lower() for e in errors)

    def test_validate_request_valid_connect(self):
        validator = SocksValidator()
        ok, code, msg = validator.validate_request(
            command=SocksCommand.CONNECT,
            address_type=SocksAddressType.IPV4,
            host="10.0.0.1",
            port=80,
        )
        assert ok is True
        assert code == SocksReply.SUCCEEDED

    def test_validate_request_unsupported_command(self):
        validator = SocksValidator()
        ok, code, msg = validator.validate_request(
            command=0xFF,
            address_type=SocksAddressType.IPV4,
            host="10.0.0.1",
            port=80,
        )
        assert ok is False
        assert code == SocksReply.COMMAND_NOT_SUPPORTED

    def test_validate_request_unsupported_address_type(self):
        validator = SocksValidator()
        ok, code, msg = validator.validate_request(
            command=SocksCommand.CONNECT,
            address_type=0xFF,
            host="10.0.0.1",
            port=80,
        )
        assert ok is False
        assert code == SocksReply.ADDRESS_TYPE_NOT_SUPPORTED

    def test_validate_request_invalid_port(self):
        validator = SocksValidator()
        ok, code, msg = validator.validate_request(
            command=SocksCommand.CONNECT,
            address_type=SocksAddressType.IPV4,
            host="10.0.0.1",
            port=0,
        )
        assert ok is False

    def test_validate_request_denied_port_ac(self, tmp_path):
        validator = SocksValidator()
        config = SocksProxyConfig(denied_ports=[22, 23])
        ok, code, msg = validator.validate_request(
            command=SocksCommand.CONNECT,
            address_type=SocksAddressType.IPV4,
            host="10.0.0.1",
            port=22,
            config=config,
        )
        assert ok is False
        assert code == SocksReply.CONNECTION_NOT_ALLOWED


class TestSocksProxyEngine:
    def test_default_engine(self):
        engine = SocksProxyEngine()
        errors = engine.validate()
        assert errors == []

    def test_build_spec(self):
        engine = SocksProxyEngine()
        spec = engine.build_spec()
        assert spec["version"] == 0x05
        assert spec["bind_address"] == SOCKS_DEFAULT_BIND_ADDRESS
        assert spec["bind_port"] == SOCKS_DEFAULT_BIND_PORT

    def test_create_session(self):
        engine = SocksProxyEngine()
        session = engine.create_session("s1", "example.com", 443, "beacon_1")
        assert session is not None
        assert session.target_host == "example.com"
        assert engine.session_count == 1

    def test_remove_session(self):
        engine = SocksProxyEngine()
        engine.create_session("s1", "h", 80, "b")
        assert engine.remove_session("s1") is True
        assert engine.session_count == 0

    def test_remove_nonexistent_session(self):
        engine = SocksProxyEngine()
        assert engine.remove_session("ghost") is False

    def test_get_session(self):
        engine = SocksProxyEngine()
        created = engine.create_session("s1", "h", 80, "b")
        retrieved = engine.get_session("s1")
        assert retrieved is not None
        assert retrieved.session_id == "s1"

    def test_get_nonexistent_session(self):
        engine = SocksProxyEngine()
        assert engine.get_session("ghost") is None

    def test_add_bytes(self):
        engine = SocksProxyEngine()
        engine.create_session("s1", "h", 80, "b")
        engine.add_bytes("s1", sent=100, received=200)
        session = engine.get_session("s1")
        assert session.bytes_sent == 100
        assert session.bytes_received == 200

    def test_add_bytes_to_nonexistent(self):
        engine = SocksProxyEngine()
        engine.add_bytes("ghost", sent=10, received=20)

    def test_max_connections_limit(self):
        config = SocksProxyConfig(max_connections=2)
        engine = SocksProxyEngine(config=config)
        engine.create_session("a", "h1", 80, "b")
        engine.create_session("b", "h2", 80, "b")
        initial_count = engine.session_count
        engine.create_session("c", "h3", 80, "b")
        assert engine.session_count == config.max_connections

    def test_cleanup_expired(self):
        config = SocksProxyConfig(session_timeout_seconds=0)
        engine = SocksProxyEngine(config=config)
        engine.create_session("old", "h", 80, "b")
        count = engine.cleanup_expired()
        assert count == 1
        assert engine.session_count == 0

    def test_list_sessions(self):
        engine = SocksProxyEngine()
        engine.create_session("a", "h1", 80, "b")
        engine.create_session("b", "h2", 443, "b")
        sessions = engine.list_sessions()
        assert len(sessions) == 2
        hosts = {s["target_host"] for s in sessions}
        assert hosts == {"h1", "h2"}

    def test_from_dict(self):
        engine = SocksProxyEngine.from_dict({
            "bind_address": "0.0.0.0",
            "bind_port": 1080,
            "auth_methods": ["NO_AUTH"],
        })
        assert engine.config.bind_address == "0.0.0.0"
        assert engine.config.bind_port == 1080

    def test_from_payload(self):
        engine = SocksProxyEngine.from_payload({
            "socks_proxy": {
                "bind_address": "127.0.0.1",
                "bind_port": 9050,
            }
        })
        assert engine.config.bind_port == 9050

    def test_from_payload_empty(self):
        engine = SocksProxyEngine.from_payload({})
        assert engine.config.bind_port == SOCKS_DEFAULT_BIND_PORT

    def test_validate_custom_config(self):
        config = SocksProxyConfig(max_connections=0)
        engine = SocksProxyEngine(config=config)
        errors = engine.validate()
        assert len(errors) >= 1


class TestSocksReply:
    def test_succeeded_message(self):
        assert SocksReply.SUCCEEDED.message() == "request granted"

    def test_general_failure_message(self):
        assert "general" in SocksReply.GENERAL_FAILURE.message().lower()

    def test_unknown_code_message(self):
        assert SocksReply.SUCCEEDED.message() == "request granted"
        assert SocksReply.COMMAND_NOT_SUPPORTED.message() == "command not supported"
        assert SocksReply.NETWORK_UNREACHABLE.message() == "network unreachable"
        assert "general" in SocksReply.GENERAL_FAILURE.message().lower()


class TestSocksEnums:
    def test_auth_method_values(self):
        assert SocksAuthMethod.NO_AUTH == 0x00
        assert SocksAuthMethod.USERNAME_PASSWORD == 0x02
        assert SocksAuthMethod.NO_ACCEPTABLE == 0xFF

    def test_command_values(self):
        assert SocksCommand.CONNECT == 0x01
        assert SocksCommand.BIND == 0x02
        assert SocksCommand.UDP_ASSOCIATE == 0x03

    def test_address_type_values(self):
        assert SocksAddressType.IPV4 == 0x01
        assert SocksAddressType.DOMAIN == 0x03
        assert SocksAddressType.IPV6 == 0x04
