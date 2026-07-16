"""Tests for modules.payload_factory — PayloadFactory, PayloadTemplate, format conversion.

Covers built-in payloads, format conversion, fallback to msfvenom, and
the payload table formatter.
"""

from __future__ import annotations

import pytest

from modules.payload_factory import (
    OUTPUT_FORMATS,
    PayloadFactory,
    PayloadTemplate,
    ReverseShellPayload,
    WindowsReverseShellPayload,
    format_payload_table,
)


class TestPayloadTemplate:
    def test_abstract_cannot_instantiate(self):
        """PayloadTemplate ABC cannot be instantiated directly."""
        with pytest.raises(TypeError):
            PayloadTemplate("test", "unix", "x86", "desc")

    def test_concrete_subclass(self):
        """A minimal concrete subclass works."""

        class MinimalPayload(PayloadTemplate):
            def generate(self, **kwargs):
                return b"hello"

        p = MinimalPayload("test/minimal", "unix", "cmd", "A minimal test payload")
        assert p.to_dict()["name"] == "test/minimal"
        assert p.generate() == b"hello"


class TestReverseShellPayload:
    def test_bash_default(self):
        p = ReverseShellPayload()
        raw = p.generate(lhost="10.0.0.1", lport=4444)
        assert b"10.0.0.1" in raw
        assert b"4444" in raw
        assert raw.startswith(b"bash -i")

    def test_nc_shell(self):
        p = ReverseShellPayload()
        raw = p.generate(lhost="10.0.0.1", lport=9999, shell_type="nc")
        assert b"nc 10.0.0.1 9999" in raw

    def test_python_shell(self):
        p = ReverseShellPayload()
        raw = p.generate(lhost="10.0.0.1", lport=8080, shell_type="python")
        assert b"10.0.0.1" in raw
        assert b"socket" in raw

    def test_unknown_shell_type_falls_back_to_bash(self):
        p = ReverseShellPayload()
        raw = p.generate(lhost="10.0.0.1", lport=4444, shell_type="nonexistent")
        assert raw.startswith(b"bash -i")


class TestWindowsReverseShellPayload:
    def test_generates_powershell(self):
        p = WindowsReverseShellPayload()
        raw = p.generate(lhost="10.0.0.1", lport=5555)
        assert b"10.0.0.1" in raw
        assert b"5555" in raw
        assert b"New-Object" in raw
        assert b"TCPClient" in raw


class TestPayloadFactory:
    def test_list_all(self):
        factory = PayloadFactory()
        all_payloads = factory.list()
        names = [p["name"] for p in all_payloads]
        assert "cmd/unix/reverse_shell" in names
        assert "cmd/windows/reverse_powershell" in names

    def test_list_filter_by_platform(self):
        factory = PayloadFactory()
        unix = factory.list(platform="unix")
        assert all(p["platform"] == "unix" for p in unix)
        windows = factory.list(platform="windows")
        assert all(p["platform"] == "windows" for p in windows)

    def test_get_existing_payload(self):
        factory = PayloadFactory()
        template = factory.get("cmd/unix/reverse_shell")
        assert template is not None
        assert template.name == "cmd/unix/reverse_shell"

    def test_get_nonexistent_returns_none(self):
        factory = PayloadFactory()
        assert factory.get("nonexistent/payload") is None

    def test_generate_native_payload(self):
        factory = PayloadFactory()
        result = factory.generate("cmd/unix/reverse_shell", lhost="10.0.0.1", lport=7777)
        assert isinstance(result, bytes)
        assert b"10.0.0.1" in result
        assert b"7777" in result

    def test_register_custom(self):
        factory = PayloadFactory()

        class CustomPayload(PayloadTemplate):
            def generate(self, **kwargs):
                return b"custom"

        factory.register(CustomPayload("custom/test", "test", "x86", "Custom"))
        assert factory.get("custom/test") is not None
        result = factory.generate("custom/test")
        assert result == b"custom"

    def test_format_raw(self):
        factory = PayloadFactory()
        result = factory.generate("cmd/unix/reverse_shell", format="raw", lhost="1.2.3.4", lport=1234)
        assert b"1.2.3.4" in result
        assert b"1234" in result

    def test_format_hex(self):
        factory = PayloadFactory()
        result = factory.generate("cmd/unix/reverse_shell", format="hex", lhost="1.2.3.4", lport=1234)
        assert isinstance(result, bytes)
        assert all(c in b"0123456789abcdef" for c in result)

    def test_format_base64(self):
        factory = PayloadFactory()
        result = factory.generate("cmd/unix/reverse_shell", format="base64", lhost="1.2.3.4", lport=1234)
        import base64

        decoded = base64.b64decode(result)
        assert b"1.2.3.4" in decoded

    def test_format_c(self):
        factory = PayloadFactory()
        result = factory.generate("cmd/unix/reverse_shell", format="c", lhost="1.2.3.4", lport=1234)
        assert result.startswith(b"unsigned char buf[]")
        assert b"\\x" in result

    def test_format_python(self):
        factory = PayloadFactory()
        result = factory.generate("cmd/unix/reverse_shell", format="py", lhost="1.2.3.4", lport=1234)
        assert result.startswith(b"buf = b")
        assert b"\\x" in result

    def test_list_formats(self):
        formats = PayloadFactory.list_formats()
        assert isinstance(formats, list)
        fmt_names = {f["format"] for f in formats}
        assert "raw" in fmt_names
        assert "hex" in fmt_names
        assert "base64" in fmt_names
        assert "c" in fmt_names
        assert "python" in fmt_names
        assert len(formats) == len(OUTPUT_FORMATS)

    def test_fallback_to_msfvenom_when_not_found(self):
        """Fallback to msfvenom returns empty bytes when msfvenom is not installed."""
        factory = PayloadFactory()
        result = factory.generate("windows/meterpreter/reverse_tcp", lhost="1.2.3.4", lport=4444)
        assert isinstance(result, bytes)


class TestFormatPayloadTable:
    def test_empty_list(self):
        result = format_payload_table([])
        assert "No payloads" in result

    def test_formats_list(self):
        payloads = [
            {"name": "test/payload", "platform": "unix", "arch": "cmd", "description": "A test"},
        ]
        result = format_payload_table(payloads)
        assert "test/payload" in result
        assert "unix" in result
        assert "cmd" in result

    def test_multiple_payloads_aligned(self):
        payloads = [
            {"name": "a", "platform": "unix", "arch": "x64", "description": "short"},
            {"name": "longer_name", "platform": "windows", "arch": "x86", "description": "longer description here"},
        ]
        result = format_payload_table(payloads)
        lines = result.splitlines()
        assert "a" in lines[2]
        assert "longer_name" in lines[3]
