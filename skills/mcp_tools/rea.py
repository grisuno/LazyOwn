"""MCP tool ``lazyown_rea``: reverse-engineer a local artifact via the REA CLI."""

from __future__ import annotations

import asyncio
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_REA_BINARY = "rea"
_REA_TIMEOUT_DEFAULT = 120
_REA_TIMEOUT_MAX = 600
_REA_OUTPUT_LIMIT = 8000
_REA_SUPPORTED_ACTIONS = frozenset(
    {
        "analyze",
        "inspect",
        "inspect-artifact",
        "search",
        "function",
        "xrefs",
        "trace",
        "decompile",
        "providers",
        "capabilities",
        "doctor",
    }
)
_REA_ADDRESS_ACTIONS = frozenset({"function", "xrefs", "decompile"})
_REA_QUERY_ACTIONS = frozenset({"search", "trace"})
_REA_PROVIDERS = frozenset({"auto", "hopper", "ghidra"})
_ADDRESS_PATTERN = re.compile(r"(0x[0-9a-fA-F]+|\d+)")

TOOL = types.Tool(
    name="lazyown_rea",
    description=(
        "Reverse-engineer a local binary, app bundle, .asar or JS/Electron tree "
        "with REA (Reverse Engineer Anything). Actions: analyze (default, needs "
        "target), inspect, inspect-artifact (works without Hopper/Ghidra), "
        "search/trace (need query), function/xrefs/decompile (need address), "
        "providers, capabilities, doctor. Target defaults to "
        "payload.json 'target' (set with lazyown_set_config). Deep native "
        "analysis needs Hopper or Ghidra; JS/artifact analysis works without "
        "them. Runs the local 'rea' CLI, nothing is uploaded."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": (
                    "REA action: analyze, inspect, inspect-artifact, search, "
                    "function, xrefs, trace, decompile, providers, "
                    "capabilities, doctor."
                ),
                "default": "analyze",
            },
            "target": {
                "type": "string",
                "description": ("Path to the binary, .app, .asar or directory. Defaults to payload.json 'target'."),
                "default": "",
            },
            "address": {
                "type": "string",
                "description": "Function address for function/xrefs/decompile (e.g. 0x1000).",
                "default": "",
            },
            "query": {
                "type": "string",
                "description": "String or symbol to look for (search/trace actions).",
                "default": "",
            },
            "provider": {
                "type": "string",
                "description": "Deep-analysis provider: auto, hopper, ghidra.",
                "default": "auto",
            },
            "timeout": {
                "type": "integer",
                "description": "Max seconds to wait (default 120, max 600).",
                "default": _REA_TIMEOUT_DEFAULT,
            },
        },
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Run one REA CLI action against a local artifact and return a JSON envelope.

    Args:
        arguments: action, target, address, query, provider, timeout.
        tool_name: Registered tool name used for the response envelope.
        ctx: Injected runtime helpers.

    Returns:
        Single TextContent holding a JSON envelope with the REA result.
    """

    def _fail(message: str, remediation: str = "") -> list:
        envelope: dict[str, Any] = {"error": message}
        if remediation:
            envelope["remediation"] = remediation
        return ctx.text(tool_name, json.dumps(envelope, indent=2))

    action = str(arguments.get("action", "analyze")).strip().lower()
    if action not in _REA_SUPPORTED_ACTIONS:
        return _fail(
            f"Unknown REA action: {action!r}.",
            f"Supported actions: {sorted(_REA_SUPPORTED_ACTIONS)}.",
        )

    rea_bin = shutil.which(_REA_BINARY)
    if rea_bin is None:
        return _fail(
            "REA CLI not found in PATH.",
            "Install with: npm install --global rea-agents@4.0.1 (see lazyaddons/rea.yaml), then run: rea setup.",
        )

    provider = str(arguments.get("provider", "auto")).strip().lower() or "auto"
    if provider not in _REA_PROVIDERS:
        return _fail(
            f"Unknown REA provider: {provider!r}.",
            f"Supported providers: {sorted(_REA_PROVIDERS)}.",
        )
    try:
        timeout = int(arguments.get("timeout", _REA_TIMEOUT_DEFAULT))
    except (TypeError, ValueError):
        timeout = _REA_TIMEOUT_DEFAULT
    timeout = max(1, min(timeout, _REA_TIMEOUT_MAX))

    argv: list[str] = [rea_bin]
    target = ""
    if action == "doctor":
        argv += ["doctor", "--json"]
    elif action == "providers":
        argv += ["providers", "--json"]
    elif action == "capabilities":
        argv += ["capabilities"]
    else:
        target = str(arguments.get("target") or ctx.load_payload().get("target") or "").strip()
        if not target or target.startswith("-"):
            return _fail(
                "A target artifact path is required for this action.",
                "Set it with lazyown_set_config(key='target', value='/path/to/binary') "
                "or pass target='/path/to/binary' directly.",
            )
        if not Path(target).exists():
            return _fail(
                f"Target not found: {target}.",
                "Pass an existing binary, .app bundle, .asar or directory.",
            )
        if action in _REA_ADDRESS_ACTIONS:
            address = str(arguments.get("address", "")).strip()
            if not _ADDRESS_PATTERN.fullmatch(address):
                return _fail(
                    f"Invalid address: {address!r}.",
                    "Use a hex address (0x1000) or decimal offset.",
                )
            argv += [action, target, address]
        elif action in _REA_QUERY_ACTIONS:
            query = str(arguments.get("query", "")).strip()
            if not query:
                return _fail(
                    "A query string is required for search/trace actions.",
                    "Pass query='offline search' (string or symbol to look for).",
                )
            argv += [action, target, query]
        else:
            argv += [action, target, "--json"]
        if provider != "auto":
            argv += ["--provider", provider]

    def _run_rea() -> dict[str, Any]:
        try:
            proc = subprocess.run(argv, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"action": action, "argv": argv, "error": f"REA timed out after {timeout}s."}
        raw = proc.stdout or proc.stderr or b""
        text = raw.decode(errors="replace")
        return {
            "action": action,
            "target": target or None,
            "provider": provider,
            "returncode": proc.returncode,
            "truncated": len(text) > _REA_OUTPUT_LIMIT,
            "output": text[:_REA_OUTPUT_LIMIT],
        }

    result = await asyncio.get_event_loop().run_in_executor(None, _run_rea)
    return ctx.text(tool_name, json.dumps(result, indent=2, ensure_ascii=False))
