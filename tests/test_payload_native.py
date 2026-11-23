"""Contract tests for the native payload builders (donut + garble).

Covers the payload.json schema fields, the garble argv builder and the
fail paths of both pipelines with fakes; the donut happy path runs
against a minimal in-memory PE fixture.
"""

from __future__ import annotations

import struct
import sys
import types

import pytest

from modules.payload_native import (
    DONUT_ARCH_CODES,
    PayloadNativeError,
    build_donut_shellcode,
    build_garble,
    garble_command,
)

_MINIMAL_PE = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40) + b"PE\x00\x00" + b"\x00" * 200


@pytest.fixture()
def tiny_pe(tmp_path):
    path = tmp_path / "tiny.exe"
    path.write_bytes(_MINIMAL_PE)
    return path


class TestSchemaFields:
    def test_donut_specs_registered(self) -> None:
        from core.payload_schema import SCHEMA

        for key in ("donut_arch", "donut_format", "donut_class_name", "donut_bypass", "donut_out"):
            assert key in SCHEMA
        assert SCHEMA["donut_arch"].default == "x64"
        assert SCHEMA["donut_out"].default == "sessions/shellcode.bin"

    def test_garble_specs_registered(self) -> None:
        from core.payload_schema import SCHEMA

        for key in ("garble_level", "garble_seed", "garble_lit", "garble_tiny", "garble_out"):
            assert key in SCHEMA
        assert SCHEMA["garble_level"].allowed == ("minimal", "standard", "max")

    def test_enum_fields_reject_unknown(self) -> None:
        from core.payload_schema import validate_value

        assert validate_value("donut_arch", "sparc") is not None
        assert validate_value("donut_arch", "x64") is None
        assert validate_value("garble_level", "ultra") is not None
        assert validate_value("garble_level", "max") is None

    def test_code_maps_are_total_for_allowed_values(self) -> None:
        assert set(DONUT_ARCH_CODES) == {"x86", "x64", "x86+x64", "any"}
        assert DONUT_ARCH_CODES["x86"] == 1
        assert DONUT_ARCH_CODES["x64"] == 2


class TestGarbleCommand:
    def test_minimal_no_flags(self) -> None:
        argv = garble_command("minimal", "random", False, False, "./cmd/app", "out/app")
        assert argv == ["garble", "build", "-o", "out/app", "./cmd/app"]

    def test_standard_literals(self) -> None:
        argv = garble_command("standard", "random", False, False, "src", "out")
        assert argv[:3] == ["garble", "-literals", "build"]

    def test_max_level_and_tiny(self) -> None:
        argv = garble_command("max", "random", True, True, "src", "out")
        assert argv[:5] == ["garble", "-literals", "-tiny", "build", "-o"]

    def test_seed_appended_when_fixed(self) -> None:
        argv = garble_command("minimal", "aabbcc", False, False, "src", "out")
        assert "-seed" in argv and "aabbcc" in argv

    def test_random_seed_omitted(self) -> None:
        argv = garble_command("minimal", "random", False, False, "src", "out")
        assert "-seed" not in argv


class TestGarbleBuild:
    def test_missing_binary_raises(self, monkeypatch) -> None:
        monkeypatch.setattr("modules.payload_native.shutil.which", lambda name: None)
        with pytest.raises(PayloadNativeError, match="garble binary not found"):
            build_garble("./src", config={"garble_out": "/tmp/opencode/gb"})

    def test_failed_build_reports_rc(self, tmp_path, monkeypatch) -> None:
        fake = tmp_path / "garble-fail"
        fake.write_text("#!/bin/sh\necho boom >&2\nexit 3\n")
        fake.chmod(0o755)
        monkeypatch.setattr("modules.payload_native.shutil.which", lambda name: str(fake))
        with pytest.raises(PayloadNativeError, match="rc=3"):
            build_garble("./src", config={"garble_out": str(tmp_path / "out")})

    def test_successful_build_returns_artefact(self, tmp_path, monkeypatch) -> None:
        out_dir = tmp_path / "out"
        fake = tmp_path / "garble-ok"

        def _build(*args):
            target = None
            argv = list(args)
            if "-o" in argv:
                target = argv[argv.index("-o") + 1]
            out_dir.mkdir(parents=True, exist_ok=True)
            with open(target, "wb") as handle:
                handle.write(b"ELF")
            return 0

        script = f"#!/bin/sh\npython3 -c 'import sys; sys.exit({0}) if False else None'\n"
        fake.write_text(script)
        fake.chmod(0o755)
        monkeypatch.setattr("modules.payload_native.shutil.which", lambda name: str(fake))

        def fake_run(argv, timeout=None, **kwargs):
            rc = _build(*argv)
            return types.SimpleNamespace(returncode=rc, stdout="", stderr="")

        monkeypatch.setattr("modules.payload_native.safe_run_argv", fake_run)
        artefact = build_garble("./src", config={"garble_out": str(out_dir)})
        assert artefact.name == "src"
        assert artefact.read_bytes() == b"ELF"


class TestDonutBuild:
    def test_missing_input_raises(self) -> None:
        with pytest.raises(PayloadNativeError, match="input file not found"):
            build_donut_shellcode("/nonexistent/one.exe", config={"donut_out": "/tmp/opencode/d.bin"})

    def test_missing_package_raises(self, monkeypatch) -> None:
        monkeypatch.setitem(sys.modules, "donut", None)
        with pytest.raises(PayloadNativeError):
            build_donut_shellcode("/tmp/whatever.exe")

    def test_happy_path_writes_artefact(self, tiny_pe, tmp_path) -> None:
        out = tmp_path / "donut.bin"
        artefact = build_donut_shellcode(str(tiny_pe), config={"donut_out": str(out)})
        assert artefact == out
        assert artefact.stat().st_size > 1000

    def test_kwargs_fallback_to_file_only(self, tiny_pe, tmp_path, monkeypatch) -> None:
        out = tmp_path / "donut2.bin"
        calls: list[tuple] = []

        def fake_create(**kwargs):
            calls.append(tuple(kwargs))
            if len(kwargs) > 1:
                raise TypeError("unsupported kwargs")
            return b"\x90" * 16

        fake = types.ModuleType("donut")
        fake.create = fake_create
        monkeypatch.setitem(sys.modules, "donut", fake)
        artefact = build_donut_shellcode(str(tiny_pe), config={"donut_out": str(out)})
        assert artefact.read_bytes() == b"\x90" * 16
        assert len(calls) == 2
        assert calls[0] != calls[1]
