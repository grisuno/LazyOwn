#!/usr/bin/env python3
"""
Hermes-native MCP server for LazyOwn.

Provides a compact, namespaced tool surface optimized for Hermes agent
context windows. Auto-detects Hermes sessions and adapts descriptions,
output compaction, and rule generation accordingly.

Usage:
    python3 skills/hermes-lazyown/mcp_server.py

This server does NOT replace skills/lazyown_mcp.py; it complements it
with a Hermes-optimized subset.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

# ── MCP SDK (required) ────────────────────────────────────────────────────────
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# ── Local integration modules ────────────────────────────────────────────────
from constants import Defaults, EnvKeys, Paths, PhaseNames
from config_bridge import ConfigBridge, ConfigBridgeError
from output_compactor import OutputCompactor
from hermes_sync import CheckpointSerializer, ObjectiveTodoSync, DelegationPlanner, HermesSyncError
from claudemd_rules import generate_rules
from executor import LazyOwnExecutor, ExecutionResult

# ── Lazy singletons ─────────────────────────────────────────────────────────────
_config: ConfigBridge | None = None
_compactor: OutputCompactor | None = None
_executor: LazyOwnExecutor | None = None
_checkpoint_serializer: CheckpointSerializer | None = None
_objective_sync: ObjectiveTodoSync | None = None
_delegation_planner: DelegationPlanner | None = None


def _get_config() -> ConfigBridge:
    global _config
    if _config is None:
        _config = ConfigBridge()
    return _config


def _get_compactor() -> OutputCompactor:
    global _compactor
    if _compactor is None:
        max_lines = int(os.environ.get("HERMES_MAX_OUTPUT_LINES", Defaults.MAX_OUTPUT_LINES))
        _compactor = OutputCompactor(max_lines)
    return _compactor


def _get_executor() -> LazyOwnExecutor:
    global _executor
    if _executor is None:
        timeout = int(os.environ.get("HERMES_CMD_TIMEOUT", Defaults.TIMEOUT_SECONDS))
        _executor = LazyOwnExecutor(timeout=timeout)
    return _executor


def _get_checkpoint_serializer() -> CheckpointSerializer:
    global _checkpoint_serializer
    if _checkpoint_serializer is None:
        _checkpoint_serializer = CheckpointSerializer()
    return _checkpoint_serializer


def _get_objective_sync() -> ObjectiveTodoSync:
    global _objective_sync
    if _objective_sync is None:
        _objective_sync = ObjectiveTodoSync()
    return _objective_sync


def _get_delegation_planner() -> DelegationPlanner:
    global _delegation_planner
    if _delegation_planner is None:
        _delegation_planner = DelegationPlanner()
    return _delegation_planner


# ── Helper: compact and wrap result ───────────────────────────────────────────

def _compact(result: ExecutionResult, phase: str = "", tool_name: str = "") -> str:
    """Compact an ExecutionResult based on the current phase."""
    raw = result.combined
    if len(raw.splitlines()) <= Defaults.COMPACT_THRESHOLD_LINES:
        return raw
    compacted = _get_compactor().compact(raw, phase, tool_name)
    return str(compacted)


def _try_import_lazyown_module(module_name: str) -> Any:
    """Try to import a LazyOwn module; return None on failure."""
    try:
        lazyown_dir = str(Paths.lazyown_dir())
        skills_dir = str(Paths.lazyown_dir() / "skills")
        modules_dir = str(Paths.lazyown_dir() / "modules")
        for d in (lazyown_dir, skills_dir, modules_dir):
            if d not in sys.path:
                sys.path.insert(0, d)
        return __import__(module_name, fromlist=[""])
    except Exception:
        return None


# ── Tool definitions ──────────────────────────────────────────────────────────

_is_hermes = bool(os.environ.get(EnvKeys.HERMES_SESSION_ID))


def _desc(base: str) -> str:
    """Return a description string, truncated when running under Hermes."""
    if _is_hermes and len(base) > 120:
        return base[:117] + "..."
    return base


TOOLS: list[types.Tool] = [
    # ── Core ────────────────────────────────────────────────────────────────
    types.Tool(
        name="lazyown_core_session_init",
        description=_desc(
            "Initialize the LazyOwn session. Returns SITREP: config, scans, tasks, objectives, phase. "
            "Call this FIRST at the start of every session."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "format": {"type": "string", "enum": ["pretty", "json"], "default": "json"},
                "include_recommend": {"type": "boolean", "default": True},
            },
        },
    ),
    types.Tool(
        name="lazyown_core_set_config",
        description=_desc("Set a key-value pair in LazyOwn payload.json."),
        inputSchema={
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["key", "value"],
        },
    ),
    types.Tool(
        name="lazyown_core_run_command",
        description=_desc(
            "Execute a LazyOwn CLI command. Abstract commands auto-inject payload.json values. "
            "NEVER write raw tool flags."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "timeout": {"type": "integer", "default": Defaults.TIMEOUT_SECONDS},
                "phase": {"type": "string", "default": ""},
            },
            "required": ["command"],
        },
    ),
    types.Tool(
        name="lazyown_core_command_help",
        description=_desc("Return full documentation for a LazyOwn command."),
        inputSchema={
            "type": "object",
            "properties": {
                "command": {"type": "string"},
            },
            "required": ["command"],
        },
    ),
    # ── Intel ─────────────────────────────────────────────────────────────────
    types.Tool(
        name="lazyown_intel_facts_show",
        description=_desc(
            "Show structured facts from nmap scans and tool output: ports, services, creds, shares."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "target": {"type": "string", "default": ""},
                "refresh": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="lazyown_intel_recommend_next",
        description=_desc(
            "Ask the AI to recommend the best 3-5 LazyOwn commands to run next, ranked by confidence."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    types.Tool(
        name="lazyown_intel_searchsploit",
        description=_desc(
            "Multi-source exploit search: ExploitDB, NVD, PacketStorm, Metasploit, Pompem. "
            "Pass 'query' as 'service version' or a CVE ID."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "service": {"type": "string", "default": ""},
                "version": {"type": "string", "default": ""},
                "include_msf": {"type": "boolean", "default": False},
            },
            "required": ["query"],
        },
    ),
    # ── Autonomous ──────────────────────────────────────────────────────────────
    types.Tool(
        name="lazyown_auto_loop",
        description=_desc(
            "Run the autonomous attack loop: policy -> command -> outcome -> update. "
            "Stops on high-value success or max_steps."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "max_steps": {"type": "integer", "default": 5},
                "step_delay_s": {"type": "integer", "default": 3},
                "bootstrap": {"type": "boolean", "default": True},
                "target": {"type": "string", "default": ""},
            },
        },
    ),
    types.Tool(
        name="lazyown_auto_inject_objective",
        description=_desc(
            "Inject a high-level attack objective into the autonomous queue. "
            "The daemon or auto_loop will pick it up."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"], "default": "high"},
                "notes": {"type": "string", "default": ""},
            },
            "required": ["text"],
        },
    ),
    # ── Hermes Integration ────────────────────────────────────────────────────
    types.Tool(
        name="lazyown_hermes_checkpoint_write",
        description=_desc("Serialize current engagement state for Hermes resume."),
        inputSchema={
            "type": "object",
            "properties": {
                "state": {"type": "object"},
            },
            "required": ["state"],
        },
    ),
    types.Tool(
        name="lazyown_hermes_checkpoint_read",
        description=_desc("Read the latest Hermes checkpoint, if fresh."),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    types.Tool(
        name="lazyown_hermes_rules_generate",
        description=_desc(
            "Generate dynamic Claude.md rules based on current phase, target, and services."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "phase": {"type": "string", "default": ""},
                "rhost": {"type": "string", "default": ""},
                "services": {"type": "array", "items": {"type": "string"}, "default": []},
                "creds_found": {"type": "boolean", "default": False},
            },
        },
    ),
    types.Tool(
        name="lazyown_hermes_delegate_plan",
        description=_desc(
            "Generate a parallel delegation plan for a discovered service or credential. "
            "Returns task descriptors suitable for Hermes delegate_task."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "discovery_type": {"type": "string", "enum": ["service", "credential"]},
                "service": {"type": "string", "default": ""},
                "port": {"type": "integer", "default": 0},
                "rhost": {"type": "string", "default": ""},
                "cred_type": {"type": "string", "default": ""},
                "cred_value": {"type": "string", "default": ""},
            },
            "required": ["discovery_type"],
        },
    ),
    # ── C2 ────────────────────────────────────────────────────────────────────
    types.Tool(
        name="lazyown_c2_status",
        description=_desc("Check if the LazyOwn C2 server is reachable."),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    types.Tool(
        name="lazyown_c2_get_beacons",
        description=_desc("List currently connected C2 beacons/implants."),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
]


# ── Server setup ──────────────────────────────────────────────────────────────

server = Server("hermes-lazyown")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Dispatch incoming tool calls to the appropriate handler."""
    try:
        result = await _handle_tool(name, arguments)
        return [types.TextContent(type="text", text=result)]
    except Exception as exc:
        return [types.TextContent(type="text", text=f"[ERROR] {name}: {exc}")]


# ── Tool handlers ─────────────────────────────────────────────────────────────

async def _handle_tool(name: str, arguments: dict[str, Any]) -> str:
    """Route tool names to their handlers."""

    # ── Core ──────────────────────────────────────────────────────────────────
    if name == "lazyown_core_session_init":
        return _core_session_init(arguments)
    if name == "lazyown_core_set_config":
        return _core_set_config(arguments)
    if name == "lazyown_core_run_command":
        return await _core_run_command(arguments)
    if name == "lazyown_core_command_help":
        return _core_command_help(arguments)

    # ── Intel ─────────────────────────────────────────────────────────────────
    if name == "lazyown_intel_facts_show":
        return _intel_facts_show(arguments)
    if name == "lazyown_intel_recommend_next":
        return _intel_recommend_next()
    if name == "lazyown_intel_searchsploit":
        return _intel_searchsploit(arguments)

    # ── Autonomous ────────────────────────────────────────────────────────────
    if name == "lazyown_auto_loop":
        return _auto_loop(arguments)
    if name == "lazyown_auto_inject_objective":
        return _auto_inject_objective(arguments)

    # ── Hermes Integration ────────────────────────────────────────────────────
    if name == "lazyown_hermes_checkpoint_write":
        return _hermes_checkpoint_write(arguments)
    if name == "lazyown_hermes_checkpoint_read":
        return _hermes_checkpoint_read()
    if name == "lazyown_hermes_rules_generate":
        return _hermes_rules_generate(arguments)
    if name == "lazyown_hermes_delegate_plan":
        return _hermes_delegate_plan(arguments)

    # ── C2 ────────────────────────────────────────────────────────────────────
    if name == "lazyown_c2_status":
        return _c2_status()
    if name == "lazyown_c2_get_beacons":
        return _c2_get_beacons()

    return f"Unknown tool: {name}"


# ── Core handlers ─────────────────────────────────────────────────────────────

def _core_session_init(arguments: dict[str, Any]) -> str:
    """Build a structured SITREP from payload.json and session files."""
    cfg = _get_config()
    cfg.refresh()

    rhost = cfg.get_str("rhost", "<not set>")
    lhost = cfg.get_str("lhost", "<not set>")
    domain = cfg.get_str("domain", "<not set>")
    os_id = cfg.get_str("os_id", "<not set>")

    scan_path = Paths.scan_file(rhost)
    vulns_path = Paths.vulns_file(rhost)

    scan_exists = scan_path.exists()
    vulns_exists = vulns_path.exists()

    sitrep = {
        "active_config": {
            "rhost": rhost,
            "lhost": lhost,
            "domain": domain,
            "os_id": os_id,
        },
        "scan_evidence": {
            "scan_exists": scan_exists,
            "scan_path": str(scan_path) if scan_exists else None,
            "vulns_exists": vulns_exists,
            "vulns_path": str(vulns_path) if vulns_exists else None,
        },
        "hermes_session": cfg.is_hermes_session(),
        "recommendation": "Call lazyown_core_run_command with the next phase-appropriate command.",
    }

    # Try to read world_model phase if available
    wm_path = Paths.world_model_file()
    if wm_path.exists():
        try:
            with wm_path.open("r", encoding="utf-8") as fh:
                wm = json.load(fh)
            sitrep["world_model_phase"] = wm.get("phase", "unknown")
        except Exception:
            sitrep["world_model_phase"] = "unknown"

    return json.dumps(sitrep, indent=2, default=str)


def _core_set_config(arguments: dict[str, Any]) -> str:
    """Update payload.json with a single key-value pair."""
    key = arguments.get("key", "")
    value = arguments.get("value", "")
    if not key:
        return "[set_config] Error: 'key' is required."

    payload_path = Paths.payload_file()
    try:
        if payload_path.exists():
            with payload_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        else:
            data = {}
        data[key] = value
        with payload_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, default=str)
        _get_config().refresh()
        return f"[set_config] {key} = {value}"
    except Exception as exc:
        return f"[set_config] Error: {exc}"


async def _core_run_command(arguments: dict[str, Any]) -> str:
    """Execute a LazyOwn command and return compacted output."""
    command = arguments.get("command", "")
    timeout = arguments.get("timeout", Defaults.TIMEOUT_SECONDS)
    phase = arguments.get("phase", "")

    if not command:
        return "[run_command] Error: 'command' is required."

    result = _get_executor().execute(command, timeout)
    if result.timed_out:
        return f"[run_command] TIMEOUT after {timeout}s\n{result.stdout[:500]}"

    return _compact(result, phase, command)


def _core_command_help(arguments: dict[str, Any]) -> str:
    """Return help for a LazyOwn command via AST extraction (no shell spawn)."""
    command = arguments.get("command", "")
    if not command:
        return "[command_help] Error: 'command' is required."

    lazyown_path = Paths.lazyown_dir() / "lazyown.py"
    if not lazyown_path.exists():
        return f"[command_help] lazyown.py not found at {lazyown_path}"

    try:
        import ast
        source = lazyown_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        func_name = f"do_{command}"
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                docstring = ast.get_docstring(node)
                if docstring:
                    return f"Help for '{command}':\n{docstring}"
                return f"[command_help] '{command}' exists but has no docstring."

        return f"[command_help] Command '{command}' not found."
    except Exception as exc:
        return f"[command_help] Error: {exc}"


# ── Intel handlers ────────────────────────────────────────────────────────────

def _intel_facts_show(arguments: dict[str, Any]) -> str:
    """Show structured facts from session files."""
    target = arguments.get("target", "")
    refresh = arguments.get("refresh", False)

    # Try to use the native LazyOwn FactStore if available
    facts_mod = _try_import_lazyown_module("lazyown_facts")
    if facts_mod is not None:
        try:
            store = facts_mod.FactStore()
            if refresh:
                store.refresh()
            facts = store.show(target=target if target else None)
            return json.dumps(facts, indent=2, default=str)
        except Exception as exc:
            return f"[facts_show] FactStore error: {exc}"

    # Fallback: basic scan file parsing
    rhost = target or _get_config().get_str("rhost")
    if not rhost:
        return "[facts_show] No target configured. Set rhost in payload.json."

    scan_path = Paths.scan_file(rhost)
    if not scan_path.exists():
        return f"[facts_show] No scan file found at {scan_path}. Run lazynmap first."

    try:
        lines = scan_path.read_text(encoding="utf-8").splitlines()
        ports = [ln for ln in lines if "/tcp" in ln or "/udp" in ln]
        return json.dumps({"target": rhost, "open_ports": ports}, indent=2)
    except Exception as exc:
        return f"[facts_show] Error reading scan file: {exc}"


def _intel_recommend_next() -> str:
    """Ask the LazyOwn recommender for next commands."""
    recommender = _try_import_lazyown_module("recommender")
    if recommender is None:
        return (
            "[recommend_next] Recommender module unavailable. "
            "Common next steps: lazynmap -> ww -> gobuster -> ss <service> -> exploit."
        )

    try:
        result = recommender.recommend_and_save()
        return json.dumps(result, indent=2, default=str)
    except Exception as exc:
        return f"[recommend_next] Error: {exc}"


def _intel_searchsploit(arguments: dict[str, Any]) -> str:
    """Search multiple exploit sources."""
    query = arguments.get("query", "")
    service = arguments.get("service", "")
    version = arguments.get("version", "")
    include_msf = arguments.get("include_msf", False)

    if not query:
        return "[searchsploit] Error: 'query' is required."

    # Build the query string
    search_term = query
    if service and version:
        search_term = f"{service} {version}"
    elif service:
        search_term = service

    # Try to delegate to the native ss command via run_command
    cmd = f"ss '{search_term}'"
    if include_msf:
        cmd += " --msf"

    result = _get_executor().execute(cmd, timeout=120)
    return _compact(result, PhaseNames.EXPLOIT, "searchsploit")


# ── Autonomous handlers ───────────────────────────────────────────────────────

def _auto_loop(arguments: dict[str, Any]) -> str:
    """Run the autonomous attack loop."""
    max_steps = arguments.get("max_steps", 5)
    step_delay = arguments.get("step_delay_s", 3)
    bootstrap = arguments.get("bootstrap", True)
    target = arguments.get("target", "")

    cmd_parts = ["auto_loop"]
    if target:
        cmd_parts.append(f"--target {target}")
    if not bootstrap:
        cmd_parts.append("--no-bootstrap")
    cmd_parts.append(f"--max-steps {max_steps}")
    cmd_parts.append(f"--step-delay {step_delay}")

    command = " ".join(cmd_parts)
    result = _get_executor().execute(command, timeout=Defaults.ASYNC_TIMEOUT_SECONDS)
    return _compact(result, PhaseNames.EXPLOIT, "auto_loop")


def _auto_inject_objective(arguments: dict[str, Any]) -> str:
    """Inject an objective into the LazyOwn queue."""
    text = arguments.get("text", "")
    priority = arguments.get("priority", "high")
    notes = arguments.get("notes", "")

    if not text:
        return "[inject_objective] Error: 'text' is required."

    try:
        _get_objective_sync().inject_objective(text, priority, notes)

        # Also sync to Hermes todo if running inside Hermes
        if _get_config().is_hermes_session():
            return (
                f"[inject_objective] Objective injected: '{text[:60]}...'\n"
                "Hermes todo sync: add a todo item with this objective."
            )

        return f"[inject_objective] Objective injected with priority={priority}."
    except HermesSyncError as exc:
        return f"[inject_objective] Sync error: {exc}"


# ── Hermes Integration handlers ───────────────────────────────────────────────

def _hermes_checkpoint_write(arguments: dict[str, Any]) -> str:
    """Write a checkpoint for Hermes resume."""
    state = arguments.get("state", {})
    try:
        _get_checkpoint_serializer().write(state)
        return f"[checkpoint_write] Saved {len(json.dumps(state))} bytes."
    except HermesSyncError as exc:
        return f"[checkpoint_write] Error: {exc}"


def _hermes_checkpoint_read() -> str:
    """Read the latest checkpoint."""
    try:
        state = _get_checkpoint_serializer().read()
        if state is None:
            return "[checkpoint_read] No fresh checkpoint found."
        return json.dumps(state, indent=2, default=str)
    except Exception as exc:
        return f"[checkpoint_read] Error: {exc}"


def _hermes_rules_generate(arguments: dict[str, Any]) -> str:
    """Generate dynamic rules for the current context."""
    phase = arguments.get("phase", "")
    rhost = arguments.get("rhost", "")
    services = arguments.get("services", [])
    creds_found = arguments.get("creds_found", False)
    is_hermes = _get_config().is_hermes_session()

    rules = generate_rules(
        phase=phase,
        rhost=rhost,
        services=services,
        creds_found=creds_found,
        is_hermes=is_hermes,
    )
    return rules


def _hermes_delegate_plan(arguments: dict[str, Any]) -> str:
    """Generate parallel task descriptors for delegate_task."""
    discovery_type = arguments.get("discovery_type", "")

    planner = _get_delegation_planner()

    if discovery_type == "service":
        service = arguments.get("service", "")
        port = arguments.get("port", 0)
        rhost = arguments.get("rhost", "")
        if not service or not rhost:
            return "[delegate_plan] Error: 'service' and 'rhost' required for service discovery."
        plans = planner.plan_for_service(service, port, rhost)
    elif discovery_type == "credential":
        cred_type = arguments.get("cred_type", "")
        cred_value = arguments.get("cred_value", "")
        rhost = arguments.get("rhost", "")
        if not rhost:
            return "[delegate_plan] Error: 'rhost' required for credential discovery."
        plans = planner.plan_for_credential(cred_type, cred_value, rhost)
    else:
        return f"[delegate_plan] Unknown discovery_type: {discovery_type}"

    return json.dumps(plans, indent=2, default=str)


# ── C2 handlers ───────────────────────────────────────────────────────────────

def _c2_status() -> str:
    """Check C2 server reachability."""
    cfg = _get_config()
    c2_host = cfg.get_str("lhost", "127.0.0.1")
    c2_port = cfg.get_int("c2_port", 4444)

    import urllib.request
    import urllib.error

    url = f"http://{c2_host}:{c2_port}/api/status"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode(errors="replace")
        return f"[c2_status] Reachable at {url}\n{data[:500]}"
    except urllib.error.URLError as exc:
        return f"[c2_status] Unreachable: {exc}"
    except Exception as exc:
        return f"[c2_status] Error: {exc}"


def _c2_get_beacons() -> str:
    """List connected beacons via C2 API."""
    cfg = _get_config()
    c2_host = cfg.get_str("lhost", "127.0.0.1")
    c2_port = cfg.get_int("c2_port", 4444)

    import urllib.request
    import urllib.error

    url = f"http://{c2_host}:{c2_port}/api/beacons"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode(errors="replace")
        return f"[c2_get_beacons] {data[:1000]}"
    except urllib.error.URLError as exc:
        return f"[c2_get_beacons] Unreachable: {exc}"
    except Exception as exc:
        return f"[c2_get_beacons] Error: {exc}"


# ── Main entrypoint ───────────────────────────────────────────────────────────

async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
