#!/usr/bin/env python3
"""
LazyOwn MCP OpenCode bridge.

Curated, short-named MCP server for autonomous OpenCode agents running on local
models (e.g. ollama/qwen3.8:27b). Local models mis-handle large tool catalogs and
re-namespace long names like ``lazyown_lazyown_campaign_sitrep``. This bridge
exposes only the essential LazyOwn tools under short, memorable names and proxies
every call back to the full ``lazyown_mcp`` server, which keeps the single source
of truth for logic, permissions and hooks.

Usage:
    python3 skills/lazyown_mcp_opencode.py

The stdio transport is used (default), matching OpenCode local MCP config.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

_mcp_root = Path(__file__).parent
for _p in [str(_mcp_root), str(_mcp_root.parent / "modules")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from lazyown_mcp import call_tool as _call_tool  # noqa: E402
from lazyown_mcp import list_tools as _list_tools  # noqa: E402

server = Server("lazyown")

CURATED_TOOLS: dict[str, str] = {
    "sitrep": "lazyown_campaign_sitrep",
    "session_init": "lazyown_session_init",
    "set_config": "lazyown_set_config",
    "run": "lazyown_run_command",
    "auto_populate": "lazyown_auto_populate",
    "facts": "lazyown_facts_show",
    "recommend_next": "lazyown_recommend_next",
    "soul": "lazyown_soul",
    "get_config": "lazyown_get_config",
    "list_sessions": "lazyown_list_sessions",
    "read_session_file": "lazyown_read_session_file",
    "get_beacons": "lazyown_get_beacons",
    "next_objective": "lazyown_next_objective",
    "phase_guide": "lazyown_phase_guide",
    "command_next": "lazyown_command_next",
    "auto_loop": "lazyown_auto_loop",
    "apt_chain": "lazyown_apt_chain",
    "ttp_chain": "lazyown_ttp_chain",
    "atomic_shell": "lazyown_atomic_shell",
    "atomic_clean": "lazyown_atomic_clean",
}

HARNESS_TOOLS: dict[str, dict[str, str]] = {
    "harness_status": {
        "description": (
            "Report the deterministic-harness state: env/payload/profile flags, "
            "active profile, default chain and whether cloud LLM backends are "
            "blocked. Read-only."
        ),
        "schema": {"type": "object", "properties": {}},
    },
    "golden_paths_show": {
        "description": (
            "Build the deterministic golden-path attack plan from the live "
            "world model (severity-weighted exploits, confirmed credentials, "
            "graph relations) and show the ranked paths. Read-only: writes "
            "sessions/attack_paths.json only."
        ),
        "schema": {
            "type": "object",
            "properties": {"top_k": {"type": "integer", "default": 5}},
        },
    },
    "golden_paths_push": {
        "description": (
            "Inject every solved golden path into sessions/objectives.jsonl "
            "as an 'auto chain <chain> <target>' directive so the autonomous "
            "loop executes them in cost order."
        ),
        "schema": {"type": "object", "properties": {}},
    },
    "ctf_report": {
        "description": (
            "Summarise the verified CTF path captures under sessions/ctf/ "
            "plus the gym matrix run: totals, status counts, CVE list and "
            "per-vector records."
        ),
        "schema": {"type": "object", "properties": {}},
    },
}


def _sync_harness() -> list[types.Tool]:
    """Render tools wrapping the harness/golden-path/CTF module APIs.

    Returns:
        One :class:`types.Tool` per curated harness helper.
    """
    tools: list[types.Tool] = []
    for short_name, spec in HARNESS_TOOLS.items():
        tools.append(
            types.Tool(
                name=short_name,
                description=str(spec.get("description") or short_name),
                inputSchema=spec.get("schema") or {"type": "object"},
            )
        )
    return tools


def _harness_result(payload: Any) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(payload, indent=2, default=str))]


def _call_harness_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    sys_path_root = str(_mcp_root.parent)
    if sys_path_root not in sys.path:
        sys.path.insert(0, sys_path_root)
    if name == "harness_status":
        from modules.harness import gate, harness_enabled
        from modules.orchestrator_config import active_profile, chain_defaults

        return _harness_result(
            {
                "harness_enabled": harness_enabled(),
                "active_profile": active_profile(),
                "chain": chain_defaults(),
                "plan_llm_allowed": gate("plan_llm"),
                "worker_agentic_allowed": gate("worker_agentic"),
                "worker_llm_steps_allowed": gate("worker_llm_steps"),
            }
        )
    if name == "golden_paths_show":
        from modules import golden_path as _solver

        top_k = int(arguments.get("top_k", 5) or 5)
        result = _solver.build(top_k=max(1, min(top_k, 50)))
        return _harness_result(result)
    if name == "golden_paths_push":
        from modules import golden_path as _solver

        stored = _solver.load_artifact()
        paths = stored.get("paths") or []
        if not paths:
            paths = _solver.build().get("paths") or []
        objectives = _solver.push_objectives(paths)
        return _harness_result(
            {
                "pushed": len(objectives),
                "objectives": [
                    {"id": obj.id, "priority": obj.priority, "text": obj.text[:140]}
                    for obj in objectives
                ],
            }
        )
    if name == "ctf_report":
        from modules import ctf_capture as _ctf
        from modules import gym_matrix_runner as _matrix

        return _harness_result(
            {
                "ctf": _ctf.summary(),
                "matrix": _matrix.load_matrix(),
            }
        )
    raise ValueError(f"Unknown harness tool '{name}'")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Expose the curated subset under short names, keeping original schemas."""
    all_tools = await _list_tools()
    by_name = {tool.name: tool for tool in all_tools}
    curated: list[types.Tool] = []
    for short_name, full_name in CURATED_TOOLS.items():
        original = by_name.get(full_name)
        if original is not None:
            curated.append(
                types.Tool(
                    name=short_name,
                    description=original.description,
                    inputSchema=original.inputSchema,
                )
            )
    curated.extend(_sync_harness())
    return curated


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Proxy the short name to the full LazyOwn MCP handler."""
    if name in HARNESS_TOOLS:
        return _call_harness_tool(name, arguments or {})
    full_name = CURATED_TOOLS.get(name)
    if full_name is None:
        raise ValueError(f"Unknown curated tool '{name}'")
    return await _call_tool(full_name, arguments)


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
