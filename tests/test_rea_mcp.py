"""Tests for the lazyown_rea MCP tool (REA reverse-engineering skill).

Covers tool registration, argument validation and argv construction for
skills.lazyown_mcp._h_rea without requiring Hopper, Ghidra or network.
"""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT / "skills"))


def _stub_mcp_sdk() -> None:
    """Provide minimal mcp SDK stubs when the pinned SDK cannot load the server.

    The repository pins mcp==2.1.1 whose Server lacks the list_tools/call_tool
    decorators used by skills.lazyown_mcp. The stubs expose just enough API
    for the module to import so handler logic stays testable.
    """
    import types as _pytypes

    mcp = _pytypes.ModuleType("mcp")
    server_mod = _pytypes.ModuleType("mcp.server")
    stdio_mod = _pytypes.ModuleType("mcp.server.stdio")
    types_mod = _pytypes.ModuleType("mcp.types")

    class Tool:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class TextContent:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    types_mod.Tool = Tool
    types_mod.TextContent = TextContent

    class Server:
        def __init__(self, *args, **kwargs):
            pass

        def list_tools(self):
            return lambda func: func

        def call_tool(self):
            return lambda func: func

    server_mod.Server = Server
    stdio_mod.stdio_server = lambda *args, **kwargs: (_ for _ in ()).throw(
        RuntimeError("stub stdio server")
    )
    mcp.types = types_mod
    mcp.server = server_mod
    sys.modules["mcp"] = mcp
    sys.modules["mcp.types"] = types_mod
    sys.modules["mcp.server"] = server_mod
    sys.modules["mcp.server.stdio"] = stdio_mod


try:
    import lazyown_mcp  # noqa: E402
except (ImportError, AttributeError):
    _stub_mcp_sdk()
    import lazyown_mcp  # noqa: E402


def _call(arguments: dict, monkeypatch: pytest.MonkeyPatch) -> dict:
    """Invoke the rea handler and parse its JSON envelope."""
    monkeypatch.setattr(lazyown_mcp.shutil, "which", lambda _: "/usr/bin/rea")
    seen: dict = {}

    def _fake_run(argv, **kwargs):
        seen["argv"] = argv
        return subprocess.CompletedProcess(argv, 0, b'{"ok": true}', b"")

    monkeypatch.setattr(lazyown_mcp.subprocess, "run", _fake_run)
    out = asyncio.run(lazyown_mcp._h_rea(arguments, "lazyown_rea"))
    assert len(out) == 1
    envelope = json.loads(out[0].text)
    envelope["_argv"] = seen.get("argv")
    return envelope


def test_list_tools_has_rea() -> None:
    tools = asyncio.run(lazyown_mcp.list_tools())
    by_name = {t.name: t for t in tools}
    assert "lazyown_rea" in by_name
    schema = by_name["lazyown_rea"].inputSchema
    for prop in ("action", "target", "address", "query", "provider", "timeout"):
        assert prop in schema["properties"], f"missing schema property: {prop}"


def test_unknown_action_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(lazyown_mcp.shutil, "which", lambda _: "/usr/bin/rea")
    out = asyncio.run(lazyown_mcp._h_rea({"action": "pwn"}, "lazyown_rea"))
    assert "Unknown REA action" in json.loads(out[0].text)["error"]


def test_missing_binary(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(lazyown_mcp.shutil, "which", lambda _: None)
    out = asyncio.run(lazyown_mcp._h_rea({"action": "doctor"}, "lazyown_rea"))
    envelope = json.loads(out[0].text)
    assert "not found" in envelope["error"]
    assert "npm install" in envelope["remediation"]


def test_doctor_argv(monkeypatch: pytest.MonkeyPatch) -> None:
    envelope = _call({"action": "doctor"}, monkeypatch)
    assert envelope["_argv"] == ["/usr/bin/rea", "doctor", "--json"]
    assert envelope["returncode"] == 0


def test_inspect_artifact_argv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "libucnet.so"
    target.write_bytes(b"\x7fELF")
    envelope = _call(
        {"action": "inspect-artifact", "target": str(target)}, monkeypatch
    )
    assert envelope["_argv"] == [
        "/usr/bin/rea",
        "inspect-artifact",
        str(target),
        "--json",
    ]
    assert envelope["returncode"] == 0


def test_large_output_survives_compaction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "libucnet.so"
    target.write_bytes(b"\x7fELF")
    monkeypatch.setattr(lazyown_mcp.shutil, "which", lambda _: "/usr/bin/rea")
    big = b'{"evidence": "' + b"x" * 9000 + b'"}'

    def _fake_run(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 0, big, b"")

    monkeypatch.setattr(lazyown_mcp.subprocess, "run", _fake_run)
    out = asyncio.run(
        lazyown_mcp._h_rea(
            {"action": "inspect-artifact", "target": str(target)}, "lazyown_rea"
        )
    )
    envelope = json.loads(out[0].text)
    assert envelope["truncated"] is True
    assert envelope["output"] in big.decode()


def test_analyze_uses_explicit_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "sample.elf"
    target.write_bytes(b"\x7fELF")
    envelope = _call({"action": "analyze", "target": str(target)}, monkeypatch)
    assert envelope["_argv"] == ["/usr/bin/rea", "analyze", str(target), "--json"]


def test_analyze_missing_target(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(lazyown_mcp.shutil, "which", lambda _: "/usr/bin/rea")
    monkeypatch.setattr(
        lazyown_mcp, "_load_payload", lambda: {"target": ""},
    )
    out = asyncio.run(lazyown_mcp._h_rea({"action": "analyze"}, "lazyown_rea"))
    envelope = json.loads(out[0].text)
    assert "target" in envelope["error"].lower()
    assert "lazyown_set_config" in envelope["remediation"]


def test_target_flag_injection_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(lazyown_mcp.shutil, "which", lambda _: "/usr/bin/rea")
    out = asyncio.run(
        lazyown_mcp._h_rea(
            {"action": "analyze", "target": "--provider hopper"}, "lazyown_rea"
        )
    )
    assert "error" in json.loads(out[0].text)


def test_decompile_needs_valid_address(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "sample.elf"
    target.write_bytes(b"\x7fELF")
    bad = _call(
        {"action": "decompile", "target": str(target), "address": "nope"},
        monkeypatch,
    )
    assert "Invalid address" in bad["error"]
    good = _call(
        {"action": "decompile", "target": str(target), "address": "0x1000"},
        monkeypatch,
    )
    assert good["_argv"] == ["/usr/bin/rea", "decompile", str(target), "0x1000"]


def test_search_needs_query(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "app"
    target.mkdir()
    bad = _call({"action": "search", "target": str(target)}, monkeypatch)
    assert "query" in bad["error"].lower()
    good = _call(
        {"action": "search", "target": str(target), "query": "offline"},
        monkeypatch,
    )
    assert good["_argv"] == ["/usr/bin/rea", "search", str(target), "offline"]


def test_provider_flag_appended(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "sample.elf"
    target.write_bytes(b"\x7fELF")
    envelope = _call(
        {"action": "analyze", "target": str(target), "provider": "hopper"},
        monkeypatch,
    )
    assert envelope["_argv"][-2:] == ["--provider", "hopper"]
    rejected = _call(
        {"action": "analyze", "target": str(target), "provider": "ida"},
        monkeypatch,
    )
    assert "Unknown REA provider" in rejected["error"]
