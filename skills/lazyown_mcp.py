#!/usr/bin/env python3
"""
LazyOwn MCP Server
Exposes LazyOwn framework capabilities as MCP tools for Claude Code and Claude web.

Usage:
    python3 skills/lazyown_mcp.py

Configuration via environment variables:
    LAZYOWN_DIR      - Path to LazyOwn directory (default: parent of this file)
    LAZYOWN_C2_HOST  - C2 server host (default: from payload.json)
    LAZYOWN_C2_PORT  - C2 server port (default: from payload.json)
    LAZYOWN_C2_USER  - C2 username (default: from payload.json)
    LAZYOWN_C2_PASS  - C2 password (default: from payload.json)
"""

import asyncio
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from typing import Any

# Event engine (optional — only if modules/ is importable)
sys.path.insert(0, str(Path(__file__).parent.parent / "modules"))
try:
    from event_engine import (
        process_new_rows, read_events, ack_event,
        add_rule, load_rules, is_running as _hb_is_running,
    )
    _ENGINE_AVAILABLE = True
except ImportError:
    _ENGINE_AVAILABLE = False

# Agent bridge (Groq / Ollama delegation)
try:
    from mcp_agent_bridge import (
        start_agent, get_agent_status, get_agent_result, list_agents,
    )
    _BRIDGE_AVAILABLE = True
except ImportError:
    _BRIDGE_AVAILABLE = False

# Session state aggregator
try:
    from session_state import load as _state_load, refresh as _state_refresh
    _STATE_AVAILABLE = True
except ImportError:
    _STATE_AVAILABLE = False

# Smart recommender
try:
    from recommender import recommend_and_save as _recommend
    _RECOMMENDER_AVAILABLE = True
except ImportError:
    _RECOMMENDER_AVAILABLE = False

# Timeline narrator
try:
    from timeline_narrator import narrate as _narrate, load_timeline as _load_timeline
    _NARRATOR_AVAILABLE = True
except ImportError:
    _NARRATOR_AVAILABLE = False

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# ── Paths ─────────────────────────────────────────────────────────────────────
SKILLS_DIR   = Path(__file__).parent
LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(SKILLS_DIR.parent)))
PAYLOAD_FILE = LAZYOWN_DIR / "payload.json"
SESSIONS_DIR = LAZYOWN_DIR / "sessions"

# ── MCP server ────────────────────────────────────────────────────────────────
server = Server("lazyown")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_payload() -> dict:
    """Load payload.json, return empty dict on failure."""
    try:
        with open(PAYLOAD_FILE) as f:
            return json.load(f)
    except Exception as e:
        return {"_error": str(e)}


def _save_payload(data: dict) -> str:
    try:
        with open(PAYLOAD_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return "ok"
    except Exception as e:
        return f"error: {e}"


def _c2_creds():
    """Return (host, port, user, password) from env or payload.json."""
    cfg = _load_payload()
    host = os.environ.get("LAZYOWN_C2_HOST", cfg.get("lhost", "127.0.0.1"))
    port = int(os.environ.get("LAZYOWN_C2_PORT", cfg.get("c2_port", 4444)))
    user = os.environ.get("LAZYOWN_C2_USER", cfg.get("c2_user", "LazyOwn"))
    passwd = os.environ.get("LAZYOWN_C2_PASS", cfg.get("c2_pass", "LazyOwn"))
    return host, port, user, passwd


def _c2_request(path: str, method: str = "GET", body: dict | None = None) -> dict:
    """Make an authenticated HTTP request to the C2 server."""
    host, port, user, passwd = _c2_creds()
    url = f"https://{host}:{port}{path}"

    import base64
    token = base64.b64encode(f"{user}:{passwd}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    # Skip SSL verification for self-signed certs (common in lab environments)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def _run_lazyown_command(command: str, timeout: int = 30) -> str:
    """
    Execute one or more LazyOwn shell commands non-interactively.
    Multiple commands separated by newlines are all sent to stdin.
    """
    cmd_input = command.strip() + "\nexit\n"
    try:
        result = subprocess.run(
            [sys.executable, str(LAZYOWN_DIR / "lazyown.py")],
            input=cmd_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(LAZYOWN_DIR),
        )
        output = result.stdout + result.stderr
        # Strip ANSI escape codes for readability
        import re
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", output).strip()
    except subprocess.TimeoutExpired:
        return f"[timeout] Command exceeded {timeout}s"
    except Exception as e:
        return f"[error] {e}"


# ── Tool definitions ──────────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="lazyown_run_command",
            description=(
                "Execute one or more commands in the LazyOwn interactive shell. "
                "Separate multiple commands with newlines. "
                "Examples: 'list', 'set rhost 10.10.11.78', 'lazynmap'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "LazyOwn shell command(s) to execute (newline-separated).",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Max seconds to wait for output (default 30).",
                        "default": 30,
                    },
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="lazyown_get_config",
            description="Read the current LazyOwn configuration (payload.json). Returns all settings.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_set_config",
            description=(
                "Update one or more values in LazyOwn's payload.json configuration. "
                "Pass a dict of key-value pairs to update. "
                "Example: {\"lhost\": \"10.10.14.5\", \"rhost\": \"10.10.11.78\"}."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "updates": {
                        "type": "object",
                        "description": "Key-value pairs to set in payload.json.",
                    }
                },
                "required": ["updates"],
            },
        ),
        types.Tool(
            name="lazyown_list_modules",
            description="List all available LazyOwn modules and scripts in the modules/ directory.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_get_beacons",
            description="Query the LazyOwn C2 server for currently connected beacons/implants.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_c2_command",
            description=(
                "Issue a tasking command to a specific beacon connected to the LazyOwn C2 server. "
                "Available beacon commands include: whoami, download:<file>, upload:<file>, "
                "rev, exfil, stealth_on, stealth_off, discover, portscan, softenum, "
                "persist, cleanlogs, amsi, escalatelin, terminate, and more."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "client_id": {
                        "type": "string",
                        "description": "The beacon/client ID to task.",
                    },
                    "command": {
                        "type": "string",
                        "description": "Command to send to the beacon.",
                    },
                },
                "required": ["client_id", "command"],
            },
        ),
        types.Tool(
            name="lazyown_run_api",
            description=(
                "Execute a shell command on the C2 server host via the /api/run endpoint. "
                "Requires the C2 server to be running."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Shell command to run on the C2 host.",
                    }
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="lazyown_list_sessions",
            description="List files in the LazyOwn sessions directory (logs, exfil data, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "subdir": {
                        "type": "string",
                        "description": "Optional subdirectory under sessions/ to list.",
                        "default": "",
                    }
                },
            },
        ),
        types.Tool(
            name="lazyown_read_session_file",
            description="Read the contents of a file in the LazyOwn sessions directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Relative path inside sessions/ (e.g. 'logs/beacon1.log').",
                    }
                },
                "required": ["filepath"],
            },
        ),
        types.Tool(
            name="lazyown_c2_status",
            description="Check if the LazyOwn C2 server is reachable and return dashboard data.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_create_addon",
            description=(
                "Create a new YAML addon in lazyaddons/ to integrate ANY GitHub tool into LazyOwn. "
                "The addon becomes an immediately available shell command (do_<name>). "
                "LazyOwn auto-clones the repo on first run and substitutes {param} placeholders "
                "in execute_command with values from payload.json. "
                "Example: create an addon for 'ffuf' that runs fuzzing with {rhost} and {wordlist}."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Command name (no spaces). Becomes do_<name> in the shell.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Human-readable description shown in help.",
                    },
                    "repo_url": {
                        "type": "string",
                        "description": "GitHub repo URL to clone (e.g. https://github.com/user/tool.git).",
                    },
                    "install_path": {
                        "type": "string",
                        "description": "Local path for the clone (e.g. external/.exploit/toolname). Defaults to external/.exploit/<name>.",
                    },
                    "install_command": {
                        "type": "string",
                        "description": "Optional setup command run once after clone (e.g. 'pip install -r requirements.txt').",
                        "default": "",
                    },
                    "execute_command": {
                        "type": "string",
                        "description": "Command to run. Use {param_name} for substitution from payload.json (e.g. '{rhost}', '{lhost}', '{wordlist}').",
                    },
                    "params": {
                        "type": "array",
                        "description": "List of parameter definitions. Each item: {name, required, description}.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "required": {"type": "boolean"},
                                "description": {"type": "string"},
                            },
                        },
                        "default": [],
                    },
                    "author": {
                        "type": "string",
                        "description": "Author name (default: LazyOwn RedTeam).",
                        "default": "LazyOwn RedTeam",
                    },
                    "enabled": {
                        "type": "boolean",
                        "description": "Whether the addon is active immediately (default: true).",
                        "default": True,
                    },
                },
                "required": ["name", "description", "repo_url", "execute_command"],
            },
        ),
        types.Tool(
            name="lazyown_list_addons",
            description="List all YAML addons in lazyaddons/ with their name, enabled status, description, and repo URL.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_list_plugins",
            description="List all Lua plugins in plugins/ with their name, enabled status, and description.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_poll_events",
            description=(
                "Read events emitted by the LazyOwn Event Engine. "
                "Events are generated automatically when LazyOwn commands match detection rules "
                "(e.g. new beacon, port found, credentials captured, vuln scan complete). "
                "Poll this regularly to act proactively without waiting for user input."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Max events to return (default 20).",
                        "default": 20,
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status: 'pending' (default), 'processed', or 'all'.",
                        "enum": ["pending", "processed", "all"],
                        "default": "pending",
                    },
                },
            },
        ),
        types.Tool(
            name="lazyown_ack_event",
            description="Mark a specific event as processed so it won't appear in future pending polls.",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The 8-char event ID returned by lazyown_poll_events.",
                    }
                },
                "required": ["event_id"],
            },
        ),
        types.Tool(
            name="lazyown_add_rule",
            description=(
                "Add or update an event detection rule. Rules define what LazyOwn command patterns "
                "trigger which events. Use this to teach the event engine to detect new conditions. "
                "Trigger fields: 'command' (exact), 'command_contains', 'args_contains', 'output_contains'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "id":          {"type": "string", "description": "Unique rule ID (snake_case)."},
                    "description": {"type": "string", "description": "What this rule detects."},
                    "trigger":     {
                        "type": "object",
                        "description": "Match conditions. Keys: command, command_contains, args_contains, output_contains.",
                    },
                    "event_type":  {"type": "string", "description": "Event type emitted (e.g. CREDS_FOUND)."},
                    "severity":    {
                        "type": "string",
                        "enum": ["info", "high", "critical"],
                        "default": "info",
                    },
                    "suggest":     {"type": "string", "description": "Action suggestion shown in the event."},
                },
                "required": ["id", "description", "trigger", "event_type"],
            },
        ),
        types.Tool(
            name="lazyown_heartbeat_status",
            description="Check whether the LazyOwn Heartbeat process is running. Returns PID and event counts.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_discover_commands",
            description=(
                "Discover ALL commands available in the LazyOwn shell — including built-in commands, "
                "Lua plugins, YAML addons, and adversary modules — by running 'help'. "
                "Use this before operating autonomously so you know every tool available. "
                "Returns commands grouped by category with their one-line description."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_command_help",
            description=(
                "Get the full documentation for any LazyOwn command by running 'help <command>'. "
                "Returns parameters, description, and usage examples. "
                "Use this to understand a command before running it."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The LazyOwn command name to get help for (e.g. 'lazynmap', 'venom', 'c2').",
                    }
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="lazyown_add_target",
            description=(
                "Add or update a target in payload.json's 'targets' list. "
                "Use this to track multiple hosts, their discovered ports, status, and notes. "
                "The active target (rhost/domain) is set separately via lazyown_set_config. "
                "Targets persist across sessions and can be iterated autonomously."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "ip":     {"type": "string", "description": "Target IP address."},
                    "domain": {"type": "string", "description": "Target hostname or domain (optional)."},
                    "ports":  {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Open ports discovered (optional).",
                        "default": [],
                    },
                    "status": {
                        "type": "string",
                        "description": "Current status of this target.",
                        "enum": ["pending", "in_progress", "owned", "blocked", "done"],
                        "default": "pending",
                    },
                    "notes":  {"type": "string", "description": "Free-text notes about this target.", "default": ""},
                    "tags":   {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Labels like ['AD', 'web', 'linux'] for filtering.",
                        "default": [],
                    },
                },
                "required": ["ip"],
            },
        ),
        types.Tool(
            name="lazyown_list_targets",
            description=(
                "List all targets stored in payload.json. "
                "Shows IP, domain, ports, status, tags, and notes for each target. "
                "Use this to decide which target to attack next."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "status_filter": {
                        "type": "string",
                        "description": "Filter by status: pending, in_progress, owned, blocked, done, or 'all' (default).",
                        "default": "all",
                    }
                },
            },
        ),
        types.Tool(
            name="lazyown_run_agent",
            description=(
                "Delegate a goal to an autonomous AI sub-agent (Groq or Ollama) that runs "
                "LazyOwn commands independently until it completes the goal or hits the iteration limit. "
                "Returns an agent_id immediately — use lazyown_agent_status to poll progress "
                "and lazyown_agent_result to read the final answer.\n\n"
                "Use 'groq' for complex reasoning tasks (requires GROQ_API_KEY in payload.json). "
                "Use 'ollama' for local/offline tasks — currently running: qwen3.5:0.8b.\n\n"
                "Example goals: 'Enumerate SMB shares on rhost', "
                "'Find open ports and identify web services', "
                "'Run LDAP enumeration against the domain'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": "Natural language task for the agent to complete autonomously.",
                    },
                    "backend": {
                        "type": "string",
                        "description": "AI backend: 'groq' (cloud, powerful) or 'ollama' (local, private).",
                        "enum": ["groq", "ollama"],
                        "default": "ollama",
                    },
                    "max_iterations": {
                        "type": "integer",
                        "description": "Max tool-call steps before forcing a summary (default 8).",
                        "default": 8,
                    },
                },
                "required": ["goal"],
            },
        ),
        types.Tool(
            name="lazyown_agent_status",
            description=(
                "Check the current status of a running or completed sub-agent. "
                "Returns: status (running/completed/failed), iterations completed, "
                "last tool called, and the final answer if done."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "The 8-char agent ID returned by lazyown_run_agent.",
                    }
                },
                "required": ["agent_id"],
            },
        ),
        types.Tool(
            name="lazyown_agent_result",
            description=(
                "Read the full result of a completed sub-agent: final answer plus "
                "the complete action log (every tool call and its output)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "The 8-char agent ID returned by lazyown_run_agent.",
                    }
                },
                "required": ["agent_id"],
            },
        ),
        types.Tool(
            name="lazyown_list_agents",
            description="List recent sub-agents with their status, goal, backend, and iteration count.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Max agents to return (default 10).",
                        "default": 10,
                    }
                },
            },
        ),
        types.Tool(
            name="lazyown_set_active_target",
            description=(
                "Set a target from the targets list as the active one — updates rhost, domain, "
                "and related fields in payload.json so all subsequent LazyOwn commands use it. "
                "Optionally updates the target's status."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "ip": {
                        "type": "string",
                        "description": "IP of the target to activate (must exist in targets list).",
                    },
                    "status": {
                        "type": "string",
                        "description": "Optionally update target status when activating.",
                        "enum": ["pending", "in_progress", "owned", "blocked", "done"],
                    },
                },
                "required": ["ip"],
            },
        ),
        # ── Session intelligence ──────────────────────────────────────────────
        types.Tool(
            name="lazyown_session_state",
            description=(
                "Return the current aggregated session state: active phase, "
                "discovered hosts, open ports, captured credentials, last commands run, "
                "and pending unactioned events. "
                "Use this to understand the full picture before deciding what to do next."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "refresh": {
                        "type": "boolean",
                        "description": "Force rebuild from raw data even if cached state is fresh (default false).",
                        "default": False,
                    }
                },
            },
        ),
        types.Tool(
            name="lazyown_recommend_next",
            description=(
                "Ask the AI (Groq) to recommend the best 3-5 LazyOwn commands to run next, "
                "ranked by confidence, based on the current session state (phase, findings, creds). "
                "Returns command names, optional args, confidence score, and one-line reasoning. "
                "Requires api_key set in payload.json."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_timeline",
            description=(
                "Generate or return the AI-written red-team timeline narrative. "
                "Groq reads all session events and produces a prose summary "
                "suitable for an executive report. Written to sessions/timeline.md. "
                "Cached for 5 minutes; pass force=true to regenerate immediately."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "force": {
                        "type": "boolean",
                        "description": "Regenerate even if cached (default false).",
                        "default": False,
                    }
                },
            },
        ),
        # ── C2 AI endpoints ───────────────────────────────────────────────────
        types.Tool(
            name="lazyown_c2_vuln_analysis",
            description=(
                "Ask the LazyOwn C2 AI (Groq) to analyse a vulnerability or CVE. "
                "Requires the C2 server to be running. "
                "Example: 'Analyse CVE-2024-1234 and suggest exploitation steps'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Vulnerability description or CVE to analyse.",
                    }
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="lazyown_c2_redop",
            description=(
                "Ask the LazyOwn C2 AI (Groq) to plan a red team operation. "
                "Requires the C2 server to be running. "
                "Returns a structured attack plan based on the scenario."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario": {
                        "type": "string",
                        "description": "Red team scenario or objective to plan.",
                    }
                },
                "required": ["scenario"],
            },
        ),
        types.Tool(
            name="lazyown_c2_search_agent",
            description=(
                "Delegate a research query to the LazyOwn C2 AI search agent (Groq). "
                "Requires the C2 server to be running. "
                "Use for OSINT queries, technique lookups, or tooling research."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Research query or OSINT question.",
                    }
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="lazyown_c2_script",
            description=(
                "Ask the LazyOwn C2 AI (Groq) to generate an exploit or pentest script. "
                "Requires the C2 server to be running. "
                "Returns generated code ready to use."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "request": {
                        "type": "string",
                        "description": "Script request — describe what the script should do.",
                    }
                },
                "required": ["request"],
            },
        ),
        types.Tool(
            name="lazyown_c2_adversary",
            description=(
                "Emulate a MITRE ATT&CK adversary or technique via the LazyOwn C2 AI (Groq). "
                "Requires the C2 server to be running. "
                "Pass a technique ID (e.g. T1059) or adversary group name."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "technique": {
                        "type": "string",
                        "description": "MITRE ATT&CK technique ID or adversary name (e.g. 'T1059', 'APT29').",
                    }
                },
                "required": ["technique"],
            },
        ),
    ]


# ── Tool handlers ─────────────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:

    def text(content: str) -> list[types.TextContent]:
        return [types.TextContent(type="text", text=content)]

    # ── run_command ──────────────────────────────────────────────────────────
    if name == "lazyown_run_command":
        command = arguments["command"]
        timeout = int(arguments.get("timeout", 30))

        # Prefer stateful C2 shell (/api/run) when C2 is reachable
        def _run_with_fallback(cmd: str, to: int) -> str:
            c2_result = _c2_request("/api/run", method="POST", body={"command": cmd})
            # Fall back if: urllib error (_error key), C2 body error (error key), or no useful output
            if "_error" in c2_result or "error" in c2_result:
                return f"[via subprocess]\n{_run_lazyown_command(cmd, to)}"
            output = c2_result.get("output", c2_result.get("result", ""))
            if not output:
                return f"[via subprocess]\n{_run_lazyown_command(cmd, to)}"
            return f"[via C2 /api/run]\n{output}"

        output = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _run_with_fallback(command, timeout)
        )
        return text(output)

    # ── get_config ───────────────────────────────────────────────────────────
    elif name == "lazyown_get_config":
        cfg = _load_payload()
        return text(json.dumps(cfg, indent=2))

    # ── set_config ───────────────────────────────────────────────────────────
    elif name == "lazyown_set_config":
        updates: dict = arguments["updates"]
        cfg = _load_payload()
        if "_error" in cfg:
            return text(f"Cannot load payload.json: {cfg['_error']}")
        cfg.update(updates)
        result = _save_payload(cfg)
        if result == "ok":
            return text(f"Updated {len(updates)} key(s): {', '.join(updates.keys())}")
        return text(result)

    # ── list_modules ─────────────────────────────────────────────────────────
    elif name == "lazyown_list_modules":
        modules_dir = LAZYOWN_DIR / "modules"
        try:
            files = sorted(modules_dir.iterdir())
            lines = []
            for f in files:
                if f.is_file():
                    lines.append(f"  {f.name} ({f.stat().st_size:,} bytes)")
                elif f.is_dir():
                    lines.append(f"  {f.name}/  [dir]")
            return text("\n".join(lines))
        except Exception as e:
            return text(f"error: {e}")

    # ── get_beacons ──────────────────────────────────────────────────────────
    elif name == "lazyown_get_beacons":
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/get_connected_clients")
        )
        return text(json.dumps(result, indent=2))

    # ── c2_command ───────────────────────────────────────────────────────────
    elif name == "lazyown_c2_command":
        client_id = arguments["client_id"]
        command = arguments["command"]
        body = {"client_id": client_id, "command": command}
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/issue_command", method="POST", body=body)
        )
        return text(json.dumps(result, indent=2))

    # ── run_api ──────────────────────────────────────────────────────────────
    elif name == "lazyown_run_api":
        command = arguments["command"]
        body = {"command": command}
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/api/run", method="POST", body=body)
        )
        return text(json.dumps(result, indent=2))

    # ── list_sessions ─────────────────────────────────────────────────────────
    elif name == "lazyown_list_sessions":
        subdir = arguments.get("subdir", "").strip("/")
        target = SESSIONS_DIR / subdir if subdir else SESSIONS_DIR
        try:
            lines = []
            for item in sorted(target.rglob("*")):
                rel = item.relative_to(SESSIONS_DIR)
                if item.is_file():
                    lines.append(f"{rel}  ({item.stat().st_size:,} bytes)")
                else:
                    lines.append(f"{rel}/")
            return text("\n".join(lines) if lines else "(empty)")
        except Exception as e:
            return text(f"error: {e}")

    # ── read_session_file ─────────────────────────────────────────────────────
    elif name == "lazyown_read_session_file":
        filepath = arguments["filepath"].lstrip("/")
        target = SESSIONS_DIR / filepath
        # Safety: ensure path stays inside sessions/
        try:
            target.resolve().relative_to(SESSIONS_DIR.resolve())
        except ValueError:
            return text("error: path traversal not allowed")
        try:
            content = target.read_text(errors="replace")
            if len(content) > 8000:
                content = content[:8000] + "\n... [truncated]"
            return text(content)
        except Exception as e:
            return text(f"error: {e}")

    # ── c2_status ─────────────────────────────────────────────────────────────
    elif name == "lazyown_c2_status":
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/api/data")
        )
        return text(json.dumps(result, indent=2))

    # ── create_addon ──────────────────────────────────────────────────────────
    elif name == "lazyown_create_addon":
        addon_name = arguments["name"].strip().replace(" ", "_")
        description = arguments["description"]
        repo_url = arguments["repo_url"]
        install_path = arguments.get("install_path", f"external/.exploit/{addon_name}")
        install_command = arguments.get("install_command", "")
        execute_command = arguments["execute_command"]
        params = arguments.get("params", [])
        author = arguments.get("author", "LazyOwn RedTeam")
        enabled = arguments.get("enabled", True)

        # Build YAML content manually to preserve readable formatting
        lines = [
            f"name: {addon_name}",
            f"description: >",
            f"  {description}",
            f"author: \"{author}\"",
            f"version: \"1.0\"",
            f"enabled: {'true' if enabled else 'false'}",
        ]

        if params:
            lines.append("params:")
            for p in params:
                lines.append(f"  - name: {p.get('name', '')}")
                lines.append(f"    type: string")
                lines.append(f"    required: {'true' if p.get('required', False) else 'false'}")
                if p.get("description"):
                    lines.append(f"    description: {p['description']}")

        lines.append("tool:")
        lines.append(f"  name: {addon_name}")
        lines.append(f"  repo_url: {repo_url}")
        lines.append(f"  install_path: {install_path}")
        if install_command:
            lines.append(f"  install_command: {install_command}")
        lines.append(f"  execute_command: {execute_command}")

        yaml_content = "\n".join(lines) + "\n"

        addon_file = LAZYOWN_DIR / "lazyaddons" / f"{addon_name}.yaml"
        try:
            addon_file.write_text(yaml_content)
            return text(
                f"Addon '{addon_name}' created at lazyaddons/{addon_name}.yaml\n"
                f"Restart LazyOwn shell or run 'reload' to activate it.\n\n"
                f"--- Preview ---\n{yaml_content}"
            )
        except Exception as e:
            return text(f"error writing addon: {e}")

    # ── list_addons ────────────────────────────────────────────────────────────
    elif name == "lazyown_list_addons":
        addons_dir = LAZYOWN_DIR / "lazyaddons"
        try:
            import yaml as _yaml
        except ImportError:
            _yaml = None

        lines = []
        for f in sorted(addons_dir.glob("*.yaml")):
            if f.name == "README.md":
                continue
            try:
                content = f.read_text()
                if _yaml:
                    data = _yaml.safe_load(content)
                    enabled_flag = "✓" if data.get("enabled", False) else "✗"
                    desc = (data.get("description") or "").strip().replace("\n", " ")[:60]
                    repo = (data.get("tool") or {}).get("repo_url", "")
                    lines.append(f"[{enabled_flag}] {data.get('name', f.stem):<30} {desc}")
                    if repo:
                        lines.append(f"      repo: {repo}")
                else:
                    lines.append(f.name)
            except Exception:
                lines.append(f"{f.name}  (parse error)")

        return text(f"Addons ({len(lines)}):\n" + "\n".join(lines) if lines else "No addons found.")

    # ── list_plugins ───────────────────────────────────────────────────────────
    elif name == "lazyown_list_plugins":
        plugins_dir = LAZYOWN_DIR / "plugins"
        try:
            import yaml as _yaml
        except ImportError:
            _yaml = None

        lines = []
        for f in sorted(plugins_dir.glob("*.lua")):
            meta_file = f.with_suffix(".yaml")
            enabled_flag = "?"
            desc = ""
            if meta_file.exists() and _yaml:
                try:
                    data = _yaml.safe_load(meta_file.read_text())
                    enabled_flag = "✓" if data.get("enabled", False) else "✗"
                    desc = (data.get("description") or "").strip().replace("\n", " ")[:60]
                except Exception:
                    pass
            lines.append(f"[{enabled_flag}] {f.stem:<35} {desc}")

        return text(f"Lua plugins ({len(lines)}):\n" + "\n".join(lines) if lines else "No plugins found.")

    # ── run_agent ─────────────────────────────────────────────────────────────
    elif name == "lazyown_run_agent":
        if not _BRIDGE_AVAILABLE:
            return text("Agent bridge not available — check modules/mcp_agent_bridge.py")

        goal           = arguments["goal"]
        backend        = arguments.get("backend", "ollama")
        max_iterations = int(arguments.get("max_iterations", 8))

        # Inject GROQ_API_KEY from payload.json if not in env
        if backend == "groq" and not os.environ.get("GROQ_API_KEY"):
            cfg = _load_payload()
            key = cfg.get("api_key", "")
            if key:
                os.environ["GROQ_API_KEY"] = key

        def _runner(cmd: str) -> str:
            return _run_lazyown_command(cmd, timeout=60)

        try:
            agent_id = await asyncio.get_event_loop().run_in_executor(
                None, lambda: start_agent(goal, backend, _runner, max_iterations)
            )
            return text(
                f"Agent started.\n"
                f"  id:      {agent_id}\n"
                f"  goal:    {goal}\n"
                f"  backend: {backend} (max {max_iterations} steps)\n\n"
                f"Poll with: lazyown_agent_status('{agent_id}')\n"
                f"Results:   lazyown_agent_result('{agent_id}')"
            )
        except Exception as e:
            return text(f"Failed to start agent: {e}")

    # ── agent_status ──────────────────────────────────────────────────────────
    elif name == "lazyown_agent_status":
        if not _BRIDGE_AVAILABLE:
            return text("Agent bridge not available.")
        agent_id = arguments["agent_id"]
        status   = await asyncio.get_event_loop().run_in_executor(
            None, lambda: get_agent_status(agent_id)
        )
        if "error" in status:
            return text(status["error"])

        icon = {"completed": "✅", "running": "🔄", "failed": "❌"}.get(status["status"], "❓")
        lines = [
            f"{icon} Agent {agent_id}  [{status['status']}]",
            f"  goal:     {status['goal']}",
            f"  backend:  {status['backend']} / {status['model']}",
            f"  steps:    {status['iterations']}",
            f"  started:  {status.get('started_at', '')[:19]}",
        ]
        if status.get("last_action"):
            lines.append(f"  last:     {status['last_action']}")
        if status.get("finished_at"):
            lines.append(f"  finished: {status['finished_at'][:19]}")
        if status.get("answer"):
            lines.append(f"\nAnswer:\n{status['answer'][:800]}")
        return text("\n".join(lines))

    # ── agent_result ──────────────────────────────────────────────────────────
    elif name == "lazyown_agent_result":
        if not _BRIDGE_AVAILABLE:
            return text("Agent bridge not available.")
        agent_id = arguments["agent_id"]
        result   = await asyncio.get_event_loop().run_in_executor(
            None, lambda: get_agent_result(agent_id)
        )
        if "error" in result:
            return text(result["error"])

        lines = [
            f"Agent {agent_id} — {result['status']}",
            f"Goal: {result['goal']}",
            f"Backend: {result['backend']} / {result['model']}",
            f"Steps: {result['iterations']}",
            "",
            "── Action Log ──",
        ]
        for action in result.get("action_log", []):
            lines.append(f"\n[step {action['step']}] {action['tool']}({action['args']})")
            if action.get("output"):
                out = action["output"][:400]
                lines.append(f"  → {out}")
        if result.get("answer"):
            lines.append(f"\n── Final Answer ──\n{result['answer']}")
        return text("\n".join(lines))

    # ── list_agents ───────────────────────────────────────────────────────────
    elif name == "lazyown_list_agents":
        if not _BRIDGE_AVAILABLE:
            return text("Agent bridge not available.")
        limit   = int(arguments.get("limit", 10))
        agents  = await asyncio.get_event_loop().run_in_executor(
            None, lambda: list_agents(limit=limit)
        )
        if not agents:
            return text("No agents found.")
        icon = {"completed": "✅", "running": "🔄", "failed": "❌"}
        lines = [f"Recent agents ({len(agents)}):\n"]
        for a in agents:
            lines.append(
                f"{icon.get(a['status'], '❓')} {a['agent_id']}  "
                f"[{a['backend']}]  {a['status']:<12}  steps={a['iterations']}"
            )
            lines.append(f"   goal: {a['goal'][:70]}")
        return text("\n".join(lines))

    # ── discover_commands ─────────────────────────────────────────────────────
    elif name == "lazyown_discover_commands":
        raw = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _run_lazyown_command("help", timeout=30)
        )
        # cmd2 help format: category header line, then === underline, then
        # commands as space-separated tokens across multiple columns.
        import re as _re
        lines = raw.splitlines()
        groups: dict[str, list[str]] = {}
        current_group = "General"
        # Skip banner/startup noise — only parse after "Documented commands" header
        start_idx = next(
            (i for i, l in enumerate(lines) if "Documented commands" in l), 0
        )
        lines = lines[start_idx:]
        i = 0
        while i < len(lines):
            line = lines[i]
            # Detect category: next line is all '=' and at least 3 chars
            if (i + 1 < len(lines)
                    and _re.match(r"^=+$", lines[i + 1].strip())
                    and len(lines[i + 1].strip()) >= 3):
                current_group = line.strip()
                groups.setdefault(current_group, [])
                i += 2   # skip the === line
                continue
            # Collect command tokens from content lines (non-header, non-empty)
            stripped = line.strip()
            if stripped and not stripped.startswith("Documented") and not _re.match(r"^=+$", stripped):
                tokens = stripped.split()
                for tok in tokens:
                    if _re.match(r"^\w[\w_-]+$", tok):
                        groups.setdefault(current_group, []).append(tok)
            i += 1

        if not any(groups.values()):
            return text(raw[:4000])

        total = sum(len(v) for v in groups.values())
        out = [f"LazyOwn commands ({total} total):\n"]
        for group, cmds in groups.items():
            if cmds:
                out.append(f"── {group} ({len(cmds)}) ──")
                # 3-column display
                for j in range(0, len(cmds), 3):
                    out.append("  " + "  ".join(f"{c:<30}" for c in cmds[j:j+3]))
                out.append("")
        out.append("Tip: use lazyown_command_help(command) for full docs on any command.")
        return text("\n".join(out))

    # ── command_help ──────────────────────────────────────────────────────────
    elif name == "lazyown_command_help":
        cmd  = arguments["command"].strip()
        raw  = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _run_lazyown_command(f"help {cmd}", timeout=20)
        )
        return text(raw[:6000] if raw else f"No help found for '{cmd}'")

    # ── add_target ────────────────────────────────────────────────────────────
    elif name == "lazyown_add_target":
        from datetime import datetime as _dt
        cfg = _load_payload()
        if "_error" in cfg:
            return text(f"Cannot load payload.json: {cfg['_error']}")

        targets = cfg.get("targets", [])
        ip = arguments["ip"].strip()

        # Find existing or create new
        existing = next((t for t in targets if t.get("ip") == ip), None)
        if existing:
            if "domain" in arguments: existing["domain"]  = arguments["domain"]
            if "ports"  in arguments: existing["ports"]   = arguments["ports"]
            if "status" in arguments: existing["status"]  = arguments["status"]
            if "notes"  in arguments: existing["notes"]   = arguments["notes"]
            if "tags"   in arguments: existing["tags"]    = arguments["tags"]
            existing["updated_at"] = _dt.now().isoformat()
            action = "updated"
        else:
            new_target = {
                "ip":         ip,
                "domain":     arguments.get("domain", ""),
                "ports":      arguments.get("ports", []),
                "status":     arguments.get("status", "pending"),
                "notes":      arguments.get("notes", ""),
                "tags":       arguments.get("tags", []),
                "added_at":   _dt.now().isoformat(),
                "updated_at": _dt.now().isoformat(),
            }
            targets.append(new_target)
            action = "added"

        cfg["targets"] = targets
        _save_payload(cfg)
        return text(f"Target {ip} {action}. Total targets: {len(targets)}")

    # ── list_targets ──────────────────────────────────────────────────────────
    elif name == "lazyown_list_targets":
        cfg = _load_payload()
        targets = cfg.get("targets", [])
        status_filter = arguments.get("status_filter", "all")

        if status_filter != "all":
            targets = [t for t in targets if t.get("status") == status_filter]

        if not targets:
            return text(f"No targets{' with status=' + status_filter if status_filter != 'all' else ''}.")

        status_icon = {"pending": "⏳", "in_progress": "🔄", "owned": "✅", "blocked": "🚫", "done": "☑️"}
        lines = [f"Targets ({len(targets)}):\n"]
        for t in targets:
            icon = status_icon.get(t.get("status", ""), "❓")
            ports_str = ",".join(str(p) for p in t.get("ports", [])) or "unknown"
            lines.append(
                f"{icon} {t['ip']:<18} {t.get('domain', ''):<25} ports:[{ports_str}]  "
                f"tags:{t.get('tags', [])}  status:{t.get('status','?')}"
            )
            if t.get("notes"):
                lines.append(f"   notes: {t['notes']}")
        return text("\n".join(lines))

    # ── set_active_target ─────────────────────────────────────────────────────
    elif name == "lazyown_set_active_target":
        from datetime import datetime as _dt
        cfg = _load_payload()
        ip  = arguments["ip"].strip()
        targets = cfg.get("targets", [])
        target = next((t for t in targets if t.get("ip") == ip), None)

        if not target:
            return text(
                f"Target {ip} not found in targets list. "
                f"Add it first with lazyown_add_target."
            )

        # Update active params
        cfg["rhost"] = ip
        if target.get("domain"):
            cfg["domain"] = target["domain"]

        # Optionally update status
        if "status" in arguments:
            target["status"]     = arguments["status"]
            target["updated_at"] = _dt.now().isoformat()
            cfg["targets"] = targets

        _save_payload(cfg)

        summary = (
            f"Active target set to {ip}"
            + (f" ({target['domain']})" if target.get("domain") else "")
            + f"\nrhost and domain updated in payload.json."
            + (f"\nStatus → {arguments['status']}" if "status" in arguments else "")
            + f"\nKnown ports: {target.get('ports', [])}"
            + (f"\nNotes: {target['notes']}" if target.get("notes") else "")
        )
        return text(summary)

    # ── poll_events ───────────────────────────────────────────────────────────
    elif name == "lazyown_poll_events":
        if not _ENGINE_AVAILABLE:
            return text("Event engine not available — check modules/event_engine.py")
        limit  = int(arguments.get("limit", 20))
        status = arguments.get("status", "pending")
        events = await asyncio.get_event_loop().run_in_executor(
            None, lambda: read_events(limit=limit, status=status)
        )
        if not events:
            return text(f"No {status} events.")
        lines = [f"{len(events)} {status} event(s):\n"]
        for ev in events:
            lines.append(
                f"[{ev['id']}] {ev['timestamp'][:19]}  "
                f"{'🔴' if ev['severity']=='critical' else '🟡' if ev['severity']=='high' else '🔵'} "
                f"{ev['type']}  (rule: {ev['rule_id']})\n"
                f"  command: {ev['source']['command']}  target: {ev['source']['target']}\n"
                f"  suggest: {ev['suggest']}\n"
            )
        return text("\n".join(lines))

    # ── ack_event ──────────────────────────────────────────────────────────────
    elif name == "lazyown_ack_event":
        if not _ENGINE_AVAILABLE:
            return text("Event engine not available.")
        event_id = arguments["event_id"]
        found = await asyncio.get_event_loop().run_in_executor(
            None, lambda: ack_event(event_id)
        )
        return text(f"Event {event_id} marked as processed." if found else f"Event {event_id} not found.")

    # ── add_rule ───────────────────────────────────────────────────────────────
    elif name == "lazyown_add_rule":
        if not _ENGINE_AVAILABLE:
            return text("Event engine not available.")
        rule = {
            "id":          arguments["id"],
            "description": arguments["description"],
            "trigger":     arguments["trigger"],
            "event_type":  arguments["event_type"],
            "severity":    arguments.get("severity", "info"),
            "suggest":     arguments.get("suggest", ""),
        }
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: add_rule(rule)
        )
        return text(f"Rule '{rule['id']}' {result}. Total rules: {len(load_rules())}")

    # ── heartbeat_status ──────────────────────────────────────────────────────
    elif name == "lazyown_heartbeat_status":
        if not _ENGINE_AVAILABLE:
            return text("Event engine not available.")
        running, pid = await asyncio.get_event_loop().run_in_executor(
            None, _hb_is_running
        )
        pid_file = SESSIONS_DIR / "heartbeat.pid"
        events_file = SESSIONS_DIR / "events.jsonl"

        pending_count = 0
        total_count = 0
        if events_file.exists():
            for line in events_file.read_text().splitlines():
                if line.strip():
                    try:
                        ev = json.loads(line)
                        total_count += 1
                        if ev.get("status") == "pending":
                            pending_count += 1
                    except Exception:
                        pass

        status_lines = [
            f"Heartbeat: {'RUNNING (pid=' + str(pid) + ')' if running else 'STOPPED'}",
            f"Events total: {total_count}  |  pending: {pending_count}",
            f"Rules loaded: {len(load_rules())}",
            f"To start: python3 skills/heartbeat.py --interval 5 &",
        ]
        return text("\n".join(status_lines))

    # ── session_state ─────────────────────────────────────────────────────────
    elif name == "lazyown_session_state":
        if not _STATE_AVAILABLE:
            return text("session_state module not available — check modules/session_state.py")
        force = arguments.get("refresh", False)
        state = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _state_refresh() if force else _state_load()
        )
        # Pretty-print key sections
        hosts_lines = []
        for ip, info in state.get("hosts", {}).items():
            ports  = info.get("ports", [])
            domain = info.get("domain", "")
            active = " ◄ active" if info.get("is_active") else ""
            hosts_lines.append(
                f"  {ip}" + (f" ({domain})" if domain else "") +
                (f"  ports:{ports}" if ports else "") + active
            )
        pending = state.get("pending_events", [])
        ev_lines = [
            f"  [{e['severity'].upper()}] {e['type']}  — {e['suggest'][:70]}"
            for e in pending
        ]
        output = "\n".join([
            f"Phase:          {state['phase']}",
            f"Active target:  {state['active_target']}  (os: {state['os_target']})",
            f"Domain:         {state['domain'] or 'unknown'}",
            f"Lhost:          {state['lhost']}",
            f"",
            f"Hosts ({len(state['hosts'])}):",
        ] + (hosts_lines or ["  (none)"]) + [
            f"",
            f"Credentials:    {state['credentials'] or ['none']}",
            f"Last commands:  {', '.join(state['last_commands'][-6:]) or 'none'}",
            f"",
            f"Pending events ({state['open_event_count']}):",
        ] + (ev_lines or ["  (none)"]) + [
            f"",
            f"Generated: {state['generated_at'][:19]}",
        ])
        return text(output)

    # ── recommend_next ────────────────────────────────────────────────────────
    elif name == "lazyown_recommend_next":
        if not _RECOMMENDER_AVAILABLE:
            return text("Recommender not available — check modules/recommender.py")
        cfg     = _load_payload()
        api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
        # api_key may be empty — ai_fallback will try Ollama or return help msg
        recs = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _recommend(api_key)
        )
        if not recs:
            return text("No recommendations returned.")
        # Check if the single result is an error/help message
        if len(recs) == 1 and recs[0].get("command") in ("_error", "_unavailable"):
            return text(recs[0]["reason"])
        via = recs[0].get("_via", "")
        header = "Recommended next actions"
        if via:
            header += f" (via local model: {via})"
        header += ":\n"
        lines = [header]
        for i, r in enumerate(recs, 1):
            bar  = "█" * int(r["confidence"] * 10)
            cmd  = r["command"]
            args = f" {r['args']}" if r.get("args") else ""
            lines.append(f"  {i}. [{bar:<10}] {r['confidence']:.0%}  {cmd}{args}")
            lines.append(f"       {r['reason']}")
        lines.append("\nSaved to: sessions/recommendations/next_actions.json")
        return text("\n".join(lines))

    # ── timeline ──────────────────────────────────────────────────────────────
    elif name == "lazyown_timeline":
        if not _NARRATOR_AVAILABLE:
            return text("Timeline narrator not available — check modules/timeline_narrator.py")
        force   = arguments.get("force", False)
        cfg     = _load_payload()
        api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
        # No api_key and not force → try cache first
        if not api_key and not force:
            cached = await asyncio.get_event_loop().run_in_executor(None, _load_timeline)
            if cached:
                return text(cached)
        # ai_fallback handles missing key / quota / Ollama fallback internally
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _narrate(api_key=api_key, force=force)
        )
        return text(result)

    # ── c2_vuln_analysis ──────────────────────────────────────────────────────
    elif name == "lazyown_c2_vuln_analysis":
        query = arguments["query"]
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/vuln", method="POST", body={"query": query})
        )
        if "_error" in result:
            return text(f"C2 unreachable or error: {result['_error']}")
        return text(result.get("result", result.get("response", json.dumps(result))))

    # ── c2_redop ──────────────────────────────────────────────────────────────
    elif name == "lazyown_c2_redop":
        scenario = arguments["scenario"]
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/redop", method="POST", body={"scenario": scenario})
        )
        if "_error" in result:
            return text(f"C2 unreachable or error: {result['_error']}")
        return text(result.get("result", result.get("response", json.dumps(result))))

    # ── c2_search_agent ───────────────────────────────────────────────────────
    elif name == "lazyown_c2_search_agent":
        query = arguments["query"]
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/search", method="POST", body={"query": query})
        )
        if "_error" in result:
            return text(f"C2 unreachable or error: {result['_error']}")
        return text(result.get("result", result.get("response", json.dumps(result))))

    # ── c2_script ─────────────────────────────────────────────────────────────
    elif name == "lazyown_c2_script":
        request = arguments["request"]
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/script", method="POST", body={"request": request})
        )
        if "_error" in result:
            return text(f"C2 unreachable or error: {result['_error']}")
        return text(result.get("result", result.get("response", json.dumps(result))))

    # ── c2_adversary ──────────────────────────────────────────────────────────
    elif name == "lazyown_c2_adversary":
        technique = arguments["technique"]
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _c2_request("/adversary", method="POST", body={"technique": technique})
        )
        if "_error" in result:
            return text(f"C2 unreachable or error: {result['_error']}")
        return text(result.get("result", result.get("response", json.dumps(result))))

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
