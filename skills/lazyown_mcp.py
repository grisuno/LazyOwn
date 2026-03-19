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
import fcntl
import json
import os
import pty
import select
import struct
import subprocess
import sys
import termios
import time
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

# Policy engine — reward-based transition learning and classification
try:
    _skills_path = str(Path(__file__).parent)
    if _skills_path not in sys.path:
        sys.path.insert(0, _skills_path)
    from lazyown_policy import LazyOwnPolicyIntegration as _PolicyIntegration
    _policy = _PolicyIntegration()
    _POLICY_AVAILABLE = True
except Exception:
    _POLICY_AVAILABLE = False
    _policy = None

# Fact store — structured extraction from nmap XML and tool output
try:
    from lazyown_facts import FactStore as _FactStore, create_tool_file as _create_tool_file
    _facts = _FactStore()
    _FACTS_AVAILABLE = True
except Exception:
    _FACTS_AVAILABLE = False
    _facts = None  # type: ignore[assignment]
    def _create_tool_file(*_a, **_kw):  # type: ignore[misc]
        raise RuntimeError("lazyown_facts not available")

# Objective store — priority queue for high-level attack goals
# Claude Code (frontier model) is the primary writer/reasoner; sub-systems inject
# automatically from sessions_watcher when new scan/tool output appears.
try:
    from lazyown_objective import (
        ObjectiveStore as _ObjectiveStore,
        read_soul as _read_soul,
        write_soul as _write_soul,
        current_plan as _current_plan,
        full_context_for_claude as _full_context_for_claude,
    )
    _objectives = _ObjectiveStore()
    _OBJECTIVES_AVAILABLE = True
except Exception:
    _OBJECTIVES_AVAILABLE = False
    _objectives = None  # type: ignore[assignment]

# LLM Bridge — satellite model (Groq native tool calling + Ollama ReAct)
try:
    from lazyown_llm import llm_ask as _llm_ask, build_bridge as _build_bridge
    _LLM_AVAILABLE = True
except Exception:
    _LLM_AVAILABLE = False

# Auto-mapper — discovers lazyaddons/, tools/*.tool, plugins/ at startup and
# exposes each as a dynamic MCP tool (lazyown_addon_*, lazyown_tool_*, lazyown_plugin_*)
try:
    from lazyown_automapper import AutoMapper as _AutoMapper
    _AUTOMAPPER_AVAILABLE = True
except Exception:
    _AUTOMAPPER_AVAILABLE = False
    _AutoMapper = None  # type: ignore[assignment,misc]

# Parquet knowledge base — session history enriched with id/category/success
# + generic knowledge queries over all parquets/ (GTFOBins, LOLBAS, techniques)
try:
    from lazyown_parquet_db import ParquetDB as _ParquetDB, get_pdb as _get_pdb
    _PDB_AVAILABLE = True
except Exception:
    _PDB_AVAILABLE = False
    _get_pdb = lambda _=None: None  # type: ignore[misc]

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# ── Paths ─────────────────────────────────────────────────────────────────────
SKILLS_DIR   = Path(__file__).parent
LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(SKILLS_DIR.parent)))
PAYLOAD_FILE = LAZYOWN_DIR / "payload.json"
SESSIONS_DIR = LAZYOWN_DIR / "sessions"

# ── Category → default LazyOwn command (auto-loop fallback when LLM unavailable) ──
# Keys match ActionCategory values from lazyown_policy.py.
# Override by placing a policy_command_map.json in sessions/.
_CATEGORY_COMMAND_MAP: dict = {
    "recon":       "lazynmap",
    "enum":        "enum_smb",
    "brute_force": "crackmapexec",
    "exploit":     "searchsploit",
    "intrusion":   "evil-winrm",
    "privesc":     "linpeas",
    "credential":  "secretsdump",
    "lateral":     "crackmapexec",
    "payload":     "generate_reverse_shell",
    "other":       "list",
}

def _load_category_command_map() -> dict:
    """Return the category→command map, merging any user overrides from sessions/."""
    override_path = SESSIONS_DIR / "policy_command_map.json"
    if override_path.exists():
        try:
            with override_path.open() as fh:
                overrides = json.load(fh)
            return {**_CATEGORY_COMMAND_MAP, **overrides}
        except (json.JSONDecodeError, OSError):
            pass
    return _CATEGORY_COMMAND_MAP


# ── MCP server ────────────────────────────────────────────────────────────────
server = Server("lazyown")

# ── ParquetDB — initialise after LAZYOWN_DIR is set ───────────────────────────
_pdb = None
if _PDB_AVAILABLE:
    try:
        _pdb = _get_pdb(LAZYOWN_DIR)
        # Auto-sync CSV on startup (fast — only new rows are ingested)
        if _pdb is not None:
            import threading as _threading
            _threading.Thread(
                target=lambda: _pdb.sync(), daemon=True, name="pdb-sync"
            ).start()
    except Exception as _pdb_err:
        import logging as _logging
        _logging.getLogger("lazyown_mcp").warning(f"ParquetDB init failed: {_pdb_err}")

# ── Auto-mapper — initialise after LAZYOWN_DIR is set ─────────────────────────
_automapper = None
if _AUTOMAPPER_AVAILABLE and _AutoMapper is not None:
    try:
        _automapper = _AutoMapper(LAZYOWN_DIR)
        # Regenerate skills/lazyown.md with discovered tools table
        _automapper.update_skills_md(SKILLS_DIR / "lazyown.md")
    except Exception as _ae:
        import logging as _logging
        _logging.getLogger("lazyown_mcp").warning(f"automapper init failed: {_ae}")


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

    Uses a PTY (pseudo-terminal) for stdout/stderr so that LazyOwn's
    os.get_terminal_size(stdout.fileno()) succeeds without the ioctl error.
    stdin is kept as a pipe so we can send commands programmatically.
    start_new_session=True keeps the child in its own session — sudo can't
    reach /dev/tty for password prompts (use sudoers NOPASSWD via setup.sh).
    """
    import re
    cmd_input = (command.strip() + "\nexit\n").encode()

    run_script = LAZYOWN_DIR / "run"
    if run_script.is_file():
        argv = ["bash", str(run_script)]
    else:
        argv = [sys.executable, "-W", "ignore", str(LAZYOWN_DIR / "lazyown.py")]

    env = os.environ.copy()
    env["TERM"] = "xterm-256color"

    # Allocate a PTY so os.get_terminal_size(stdout.fileno()) doesn't fail
    master_fd, slave_fd = pty.openpty()
    # Tell the PTY its size (rows=50, cols=220)
    winsize = struct.pack("HHHH", 50, 220, 0, 0)
    fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsize)

    try:
        proc = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=slave_fd,
            stderr=slave_fd,
            env=env,
            cwd=str(LAZYOWN_DIR),
            start_new_session=True,
        )
        os.close(slave_fd)  # parent doesn't need the slave end

        # Send all commands then close stdin
        try:
            proc.stdin.write(cmd_input)
            proc.stdin.close()
        except BrokenPipeError:
            pass

        # Drain master_fd with timeout
        output_chunks: list[str] = []
        deadline = time.monotonic() + timeout

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                proc.kill()
                os.close(master_fd)
                return f"[timeout] Command exceeded {timeout}s"

            r, _, _ = select.select([master_fd], [], [], min(remaining, 0.5))
            if r:
                try:
                    data = os.read(master_fd, 4096)
                    if data:
                        output_chunks.append(data.decode("utf-8", errors="replace"))
                except OSError:
                    break  # EIO — child closed its PTY end (normal exit)
            else:
                if proc.poll() is not None:
                    # Drain remaining bytes
                    try:
                        while True:
                            r2, _, _ = select.select([master_fd], [], [], 0.1)
                            if not r2:
                                break
                            data = os.read(master_fd, 4096)
                            if not data:
                                break
                            output_chunks.append(data.decode("utf-8", errors="replace"))
                    except OSError:
                        pass
                    break

        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    finally:
        try:
            os.close(master_fd)
        except OSError:
            pass

    output = "".join(output_chunks)
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", output).strip()


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
                "Set a single key-value pair in LazyOwn's payload.json. "
                "Call multiple times to update several keys. "
                "Common keys: lhost, rhost, lport, rport, domain, wordlist, api_key."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The payload.json key to update (e.g. 'rhost', 'lhost', 'lport').",
                    },
                    "value": {
                        "type": "string",
                        "description": "The value to set (always pass as string; numbers are auto-converted).",
                    },
                },
                "required": ["key", "value"],
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
        types.Tool(
            name="lazyown_policy_status",
            description=(
                "Show the policy engine episode summary and next-action recommendations for a target. "
                "Displays total accumulated reward, number of steps, last observed state, and "
                "ranked recommended categories derived from learned transition frequencies and "
                "hand-coded override rules. Use after bootstrap or after executing commands."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target IP or hostname. Defaults to rhost from payload.json.",
                    }
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_auto_loop",
            description=(
                "Autonomous attack loop guided by the policy engine. "
                "Repeats: get policy recommendation → resolve to a LazyOwn command → execute → "
                "record outcome → update policy. Stops when max_steps is reached or a "
                "high-value success (intrusion, privesc, credential) is observed. "
                "Enables maximum unattended operation: the loop self-directs using accumulated "
                "session history and learned transition patterns."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target IP or hostname. Defaults to rhost from payload.json.",
                    },
                    "max_steps": {
                        "type": "integer",
                        "description": "Maximum number of execution steps (default 5, max 20).",
                    },
                    "stop_on_high_value_success": {
                        "type": "boolean",
                        "description": (
                            "Halt the loop when intrusion, privesc, or credential success is "
                            "achieved (default true)."
                        ),
                    },
                    "step_timeout_s": {
                        "type": "integer",
                        "description": "Per-step execution timeout in seconds (default 60).",
                    },
                    "step_delay_s": {
                        "type": "integer",
                        "description": "Seconds to pause between steps (default 3).",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_create_tool",
            description=(
                "Create a new pwntomate .tool file so that future runs of pwntomate "
                "automatically apply it to matching services discovered by nmap. "
                "Each .tool file defines a command template with placeholders "
                "{ip} {port} {domain} {username} {password} {outputdir} {s} (ssl). "
                "The file is written to tools/ and takes effect on the next pwntomate run. "
                "Use this when you discover a service that has no existing tool coverage."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "toolname": {
                        "type": "string",
                        "description": "Unique name for the tool (e.g. 'redis_enum').",
                    },
                    "command": {
                        "type": "string",
                        "description": (
                            "Shell command template. Use {ip}, {port}, {domain}, "
                            "{username}, {password}, {outputdir}, {s} as placeholders."
                        ),
                    },
                    "trigger": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "List of nmap service names that activate this tool "
                            "(e.g. ['http', 'https']). Use ['all'] to run on every port."
                        ),
                    },
                    "active": {
                        "type": "boolean",
                        "description": "Whether the tool is active (default true).",
                        "default": True,
                    },
                },
                "required": ["toolname", "command", "trigger"],
            },
        ),
        types.Tool(
            name="lazyown_llm_ask",
            description=(
                "Ask a satellite language model (Groq or local deepseek-r1:1.5b) "
                "to reason about a goal using LazyOwn tools.\n\n"
                "Groq backend — llama-3.3-70b with native tool calling: "
                "run_command, read_nmap, read_plan, read_facts, read_objectives.\n"
                "Ollama backend — deepseek-r1:1.5b via ReAct loop (Thought/Action/Observation). "
                "No API key needed; runs fully offline.\n\n"
                "Use this when you need a satellite model to:\n"
                "  • Analyse an nmap scan and suggest next steps\n"
                "  • Interpret tool output and extract credentials/findings\n"
                "  • Generate a specific exploit or command sequence\n"
                "  • Reason about facts/objectives before injecting a new goal"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": "Goal or question for the satellite model.",
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional extra context (paste tool output, facts, etc.).",
                        "default": "",
                    },
                    "backend": {
                        "type": "string",
                        "description": "'groq' (cloud, tool calling) or 'ollama' (local deepseek-r1, ReAct).",
                        "enum": ["groq", "ollama"],
                        "default": "groq",
                    },
                    "model": {
                        "type": "string",
                        "description": "Override model name (e.g. 'llama-3.1-8b-instant' for groq, 'deepseek-r1:1.5b' for ollama).",
                        "default": "",
                    },
                    "max_iterations": {
                        "type": "integer",
                        "description": "Max tool-call cycles (default 6).",
                        "default": 6,
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional system prompt override.",
                        "default": "",
                    },
                },
                "required": ["goal"],
            },
        ),
        types.Tool(
            name="lazyown_inject_objective",
            description=(
                "Inject a new high-level attack objective into the objective queue. "
                "USE THIS as the frontier-model reasoning entry point: after reading "
                "plan.txt, facts, or events, formulate specific next-step objectives "
                "and inject them here so the autonomous loop can execute them. "
                "Example objectives: "
                "'Enumerate SMB shares on 10.10.11.78 port 445 — use crackmapexec', "
                "'Kerberoast service accounts found in LDAP enum', "
                "'Run linPEAS on beacon abc123 — privesc phase'. "
                "Injected objectives are picked up by auto_loop and next_objective."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Objective text — be specific: include target, tool, port.",
                    },
                    "priority": {
                        "type": "string",
                        "description": "Priority: critical / high / medium / low (default: high).",
                        "enum": ["critical", "high", "medium", "low"],
                        "default": "high",
                    },
                    "notes": {
                        "type": "string",
                        "description": "Optional reasoning notes — why this objective, what evidence.",
                        "default": "",
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="lazyown_next_objective",
            description=(
                "Return the full frontier-model context needed to reason about the next action: "
                "• soul.md — agent persona, priorities, hard stops\n"
                "• sessions/plan.txt — current VulnBot-generated attack plan\n"
                "• Next pending objective from the queue\n"
                "• Count of remaining pending objectives\n"
                "• Top 5 pending objectives preview\n\n"
                "USE THIS at the start of each reasoning cycle before deciding what to do. "
                "After reading this, inject new objectives or run auto_loop."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_soul",
            description=(
                "Read or update the agent soul (sessions/soul.md). "
                "The soul defines: campaign objective, priority order, hard stops, "
                "guardrails, and current focus. "
                "Reading the soul before reasoning gives the frontier model its "
                "operating mandate. Writing it lets the operator change the campaign "
                "objective or add constraints mid-operation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "'read' to get current soul, 'write' to replace it.",
                        "enum": ["read", "write"],
                        "default": "read",
                    },
                    "content": {
                        "type": "string",
                        "description": "New soul content (only required when action='write').",
                        "default": "",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_facts_show",
            description=(
                "Show all structured facts extracted from nmap scans and tool output. "
                "Facts include: open ports, detected services, discovered credentials, "
                "accessible shares, and achieved access level per target. "
                "Optionally re-parse all sessions/ files before displaying. "
                "These facts drive context-aware command selection in auto_loop."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Filter to a specific target IP (default: all targets).",
                    },
                    "refresh": {
                        "type": "boolean",
                        "description": "Re-parse sessions/ before displaying (default false).",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_parquet_query",
            description=(
                "Query the LazyOwn Parquet knowledge base. "
                "Two modes:\n"
                "  1. Session knowledge: filter by phase (recon/scanning/exploit/privesc/"
                "credential/lateral/persistence/exfil/c2/reporting/other) and target IP "
                "to see what commands succeeded or failed in the past.\n"
                "  2. Keyword search: find relevant entries across ALL parquets "
                "(GTFOBins, LOLBAS, MITRE ATT&CK techniques, session history).\n"
                "Use 'context' mode to get a full phase-aware briefing that combines "
                "session history + GTFOBins + MITRE techniques for planning."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["session", "keyword", "context", "stats", "list"],
                        "description": (
                            "Query mode: "
                            "'session' = filter session_knowledge by phase/target; "
                            "'keyword' = search all parquets for a keyword; "
                            "'context' = full phase briefing (session+GTFOBins+MITRE); "
                            "'stats' = show session_knowledge statistics; "
                            "'list' = list available parquets."
                        ),
                        "default": "context",
                    },
                    "phase": {
                        "type": "string",
                        "description": (
                            "Attack phase filter. One of: recon, scanning, exploit, "
                            "post_exploit, privesc, credential, lateral, persistence, "
                            "exfil, c2, reporting, other. Required for 'session' and 'context' modes."
                        ),
                    },
                    "target": {
                        "type": "string",
                        "description": "Target IP to filter by (default: rhost from config).",
                    },
                    "keyword": {
                        "type": "string",
                        "description": "Search keyword for 'keyword' mode (e.g. 'smb', 'kerberos', 'sudo').",
                    },
                    "parquet": {
                        "type": "string",
                        "description": (
                            "Restrict keyword search to one parquet. "
                            "Options: binarios, detalles, lolbas_index, lolbas_details, "
                            "techniques, session_knowledge. Default: all."
                        ),
                    },
                    "success_only": {
                        "type": "boolean",
                        "description": "In session mode: only return rows where success=True.",
                        "default": False,
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max rows per result set.",
                        "default": 15,
                    },
                    "sync": {
                        "type": "boolean",
                        "description": "Re-ingest CSV before querying (default false).",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_parquet_annotate",
            description=(
                "Annotate a session row in session_knowledge.parquet with the actual "
                "outcome of a command after it has executed. "
                "Use the row 'id' from lazyown_parquet_query results. "
                "This is how the knowledge base learns: MCP runs a command, observes "
                "the output, then calls annotate to record whether it succeeded. "
                "Over time this builds a high-quality training dataset."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "row_id": {
                        "type": "string",
                        "description": "The 16-char hex id from session_knowledge.parquet.",
                    },
                    "success": {
                        "type": "boolean",
                        "description": "Whether the command succeeded.",
                    },
                    "category": {
                        "type": "string",
                        "description": (
                            "Override the attack category. One of: recon, scanning, exploit, "
                            "post_exploit, privesc, credential, lateral, persistence, exfil, "
                            "c2, reporting, other."
                        ),
                    },
                    "outcome": {
                        "type": "string",
                        "description": "Detailed outcome string (e.g. 'success', 'failure', 'partial').",
                    },
                },
                "required": ["row_id"],
            },
        ),
        # ── Campaign management ───────────────────────────────────────────────
        types.Tool(
            name="lazyown_campaign",
            description=(
                "Manage a pentest campaign: group multiple targets under a named engagement "
                "with CIDR scope, per-host phase tracking, and milestones. "
                "Actions: new, status, phase, milestone, complete, add_scope."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["new", "status", "phase", "milestone", "complete", "add_scope"],
                        "description": "Campaign action to perform.",
                    },
                    "name": {"type": "string", "description": "Campaign name (for 'new')."},
                    "scope": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of IPs or CIDRs in scope (for 'new').",
                    },
                    "host": {"type": "string", "description": "Target host IP (for 'phase')."},
                    "phase": {"type": "string", "description": "Phase name (for 'phase')."},
                    "title": {"type": "string", "description": "Milestone title (for 'milestone')."},
                    "notes": {"type": "string", "description": "Notes (for 'milestone'/'complete'/'new')."},
                    "ip_or_cidr": {"type": "string", "description": "IP or CIDR to add to scope (for 'add_scope')."},
                },
                "required": ["action"],
            },
        ),
        # ── Unified daemon management ─────────────────────────────────────────
        types.Tool(
            name="lazyown_daemon",
            description=(
                "Manage the LazyOwn unified background daemon that combines the file watcher, "
                "event engine, and heartbeat into a single asyncio process. "
                "Actions: start, stop, status."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["start", "stop", "status"],
                        "description": "Daemon action.",
                    },
                },
                "required": ["action"],
            },
        ),
    ] + (_automapper.mcp_tools() if _automapper is not None else [])


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

        # Feed every executed command into the policy engine asynchronously
        if _POLICY_AVAILABLE and _policy is not None:
            _cfg = _load_payload()
            _target = _cfg.get("rhost", "") or _cfg.get("lhost", "127.0.0.1")
            _parts = command.strip().split(None, 1)
            _cmd_name = _parts[0] if _parts else command
            _cmd_args = _parts[1] if len(_parts) > 1 else ""
            try:
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: _policy.on_command_complete(
                        _target, _cmd_name, _cmd_args, output, None
                    ),
                )
            except Exception:
                pass  # policy errors must never affect command execution

        return text(output)

    # ── get_config ───────────────────────────────────────────────────────────
    elif name == "lazyown_get_config":
        cfg = _load_payload()
        return text(json.dumps(cfg, indent=2))

    # ── set_config ───────────────────────────────────────────────────────────
    elif name == "lazyown_set_config":
        key = arguments["key"].strip()
        raw_value = arguments["value"]
        # Auto-convert numeric strings and booleans
        value: Any = raw_value
        if isinstance(raw_value, str):
            if raw_value.lower() == "true":
                value = True
            elif raw_value.lower() == "false":
                value = False
            else:
                try:
                    value = int(raw_value)
                except ValueError:
                    try:
                        value = float(raw_value)
                    except ValueError:
                        value = raw_value
        cfg = _load_payload()
        if "_error" in cfg:
            return text(f"Cannot load payload.json: {cfg['_error']}")
        cfg[key] = value
        result = _save_payload(cfg)
        if result == "ok":
            return text(f"Set {key} = {value!r}")
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
        cfg    = _load_payload()
        target = cfg.get("rhost", "") or cfg.get("lhost", "127.0.0.1")
        lines: list[str] = []

        # Layer 1 — policy engine: strategic category recommendations from learned transitions
        if _POLICY_AVAILABLE and _policy is not None:
            policy_recs = await asyncio.get_event_loop().run_in_executor(
                None, lambda: _policy.get_recommendations(target)
            )
            if policy_recs:
                lines.append(f"[Policy] Strategic recommendations for {target}:")
                for i, r in enumerate(policy_recs, 1):
                    bar = "█" * int(r["confidence"] * 10)
                    lines.append(
                        f"  {i}. [{bar:<10}] {r['confidence']:.0%}  "
                        f"category={r['category']}  [{r['source']}]"
                    )
                    lines.append(f"       {r['reason']}")
                lines.append("")

        # Layer 2 — LLM recommender: specific commands with arguments
        if _RECOMMENDER_AVAILABLE:
            api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
            llm_recs = await asyncio.get_event_loop().run_in_executor(
                None, lambda: _recommend(api_key)
            )
            if llm_recs and not (
                len(llm_recs) == 1 and llm_recs[0].get("command") in ("_error", "_unavailable")
            ):
                via = llm_recs[0].get("_via", "")
                header = "[LLM] Specific commands"
                if via:
                    header += f" (via {via})"
                lines.append(header + ":")
                for i, r in enumerate(llm_recs, 1):
                    bar  = "█" * int(r["confidence"] * 10)
                    cmd  = r["command"]
                    args = f" {r['args']}" if r.get("args") else ""
                    lines.append(f"  {i}. [{bar:<10}] {r['confidence']:.0%}  {cmd}{args}")
                    lines.append(f"       {r['reason']}")
                lines.append("\nSaved to: sessions/recommendations/next_actions.json")

        if not lines:
            return text("No recommendations available — run bootstrap first or install recommender module.")
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

    # ── policy_status ─────────────────────────────────────────────────────────
    elif name == "lazyown_policy_status":
        if not _POLICY_AVAILABLE or _policy is None:
            return text(
                "Policy engine unavailable. "
                "Run: python3 skills/lazyown_policy.py bootstrap"
            )
        cfg    = _load_payload()
        target = arguments.get("target") or cfg.get("rhost", "") or "127.0.0.1"
        summary = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _policy._advisor.episode_summary(target)
        )
        recs = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _policy.get_recommendations(target)
        )
        lines: list[str] = []
        if summary:
            lines.append(
                f"Episode  target={summary['target']}  "
                f"steps={summary['steps']}  "
                f"total_reward={summary['total_reward']:+d}  "
                f"last_state={summary['last_state']}"
            )
        else:
            lines.append(
                f"No episode data for {target}. "
                "Run bootstrap or execute commands first."
            )
        lines.append("\nRecommendations:")
        for i, r in enumerate(recs, 1):
            bar = "█" * int(r["confidence"] * 10)
            lines.append(
                f"  {i}. [{bar:<10}] {r['confidence']:.0%}  "
                f"category={r['category']}  [{r['source']}]"
            )
            lines.append(f"       {r['reason']}")
        return text("\n".join(lines))

    # ── auto_loop ─────────────────────────────────────────────────────────────
    elif name == "lazyown_auto_loop":
        if not _POLICY_AVAILABLE or _policy is None:
            return text(
                "Policy engine unavailable. "
                "Run: python3 skills/lazyown_policy.py bootstrap"
            )
        cfg              = _load_payload()
        target           = arguments.get("target") or cfg.get("rhost", "") or "127.0.0.1"
        max_steps        = min(int(arguments.get("max_steps", 5)), 20)
        stop_on_high     = bool(arguments.get("stop_on_high_value_success", True))
        step_timeout     = int(arguments.get("step_timeout_s", 60))
        step_delay       = int(arguments.get("step_delay_s", 3))
        cat_map          = _load_category_command_map()
        high_value_cats  = {"intrusion", "privesc", "credential"}

        execution_log: list[dict] = []
        # Track commands that failed this session per (target, category)
        _fail_counts: dict[str, int] = {}

        def _parquet_candidates(category: str, tgt: str) -> list[str]:
            """
            Query session_knowledge for commands that succeeded in `category`
            against `tgt` in the past.  Returns a list ordered by frequency.
            """
            if _pdb is None:
                return []
            try:
                rows = _pdb.query_session(
                    phase=category, target=tgt, success_only=True, limit=50
                )
                freq: dict[str, int] = {}
                for r in rows:
                    cmd = (r.get("command") or "").strip()
                    if cmd and not cmd.startswith("/") and not cmd.startswith("echo"):
                        freq[cmd] = freq.get(cmd, 0) + 1
                return sorted(freq, key=lambda c: -freq[c])
            except Exception:
                return []

        def _run_pwntomate_if_xml_ready(tgt: str) -> str:
            """
            After lazynmap runs, try to find the generated XML file and pass it
            to pwntomate for parallel, service-aware tool execution.
            Returns a short status string for logging.
            """
            xml_pattern = SESSIONS_DIR / f"scan_{tgt}.nmap.xml"
            if not xml_pattern.exists():
                import glob as _glob
                matches = _glob.glob(str(SESSIONS_DIR / f"scan_*{tgt}*.nmap.xml"))
                if not matches:
                    return "no xml found for pwntomate"
                xml_pattern = Path(matches[0])
            try:
                import subprocess as _sp
                result = _sp.run(
                    [
                        sys.executable, "-W", "ignore",
                        str(LAZYOWN_DIR / "pwntomate.py"),
                        str(xml_pattern),
                        "-x",
                        "-b", str(SESSIONS_DIR),
                        "-t", str(LAZYOWN_DIR / "tools"),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=step_timeout,
                    cwd=str(LAZYOWN_DIR),
                )
                return f"pwntomate ran on {xml_pattern.name} (exit {result.returncode})"
            except Exception as exc:
                return f"pwntomate error: {exc}"

        def _refresh_facts(tgt: str) -> None:
            """Re-ingest sessions/ into the fact store after pwntomate runs."""
            if _FACTS_AVAILABLE and _facts is not None:
                try:
                    _facts.parse_all(target=tgt)
                except Exception:
                    pass

        def _build_command_from_facts(
            category: str,
            resolved_cmd: str,
            resolved_args: str,
            tgt: str,
        ) -> tuple[str, str]:
            """
            Use FactStore context to substitute concrete values into the command.
            Returns (cmd, args) possibly augmented with known port/creds.
            """
            if not (_FACTS_AVAILABLE and _facts is not None):
                return resolved_cmd, resolved_args
            ctx = _facts.context_for_command(tgt, category)
            if not ctx:
                return resolved_cmd, resolved_args

            # Build enriched args only when the generic fallback command is used
            # (LLM-generated commands already contain explicit args).
            if resolved_args:
                return resolved_cmd, resolved_args

            parts: list[str] = []
            port = ctx.get("port")
            username = ctx.get("username", "")
            password = ctx.get("password", "")
            if port:
                parts.append(f"-p {port}")
            if username:
                parts.append(f"-u {username}")
            if password:
                parts.append(f"-p '{password}'")
            return resolved_cmd, " ".join(parts)

        def _execute_step() -> dict:
            recs = _policy.get_recommendations(target)
            if not recs:
                return {"stop": True, "reason": "No policy recommendations available."}
            top_rec = recs[0]
            category = top_rec["category"]

            # ── Adaptive command selection ────────────────────────────────────
            # Priority: parquet historical successes > LLM recommender > cat_map
            resolved_cmd = ""
            resolved_args = ""

            # 1. Parquet: commands proven to work for this category+target
            hist_candidates = _parquet_candidates(category, target)
            for cand in hist_candidates:
                fail_key = f"{target}:{category}:{cand}"
                if _fail_counts.get(fail_key, 0) >= 2:
                    continue  # blocked: failed twice this session
                resolved_cmd = cand
                break

            # 2. LLM recommender as fallback
            if not resolved_cmd and _RECOMMENDER_AVAILABLE:
                api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
                try:
                    llm_recs = _recommend(api_key)
                    for lr in (llm_recs or []):
                        cmd_cand = lr.get("command", "")
                        fail_key = f"{target}:{category}:{cmd_cand}"
                        if cmd_cand not in ("_error", "_unavailable") and \
                                _fail_counts.get(fail_key, 0) < 2:
                            resolved_cmd  = cmd_cand
                            resolved_args = lr.get("args", "")
                            break
                except Exception:
                    pass

            # 3. Static category map as last resort
            if not resolved_cmd:
                fallback = cat_map.get(category, "list")
                fail_key = f"{target}:{category}:{fallback}"
                resolved_cmd = (
                    fallback if _fail_counts.get(fail_key, 0) < 2 else "list"
                )

            # Enrich args with FactStore context when no explicit args were given
            resolved_cmd, resolved_args = _build_command_from_facts(
                category, resolved_cmd, resolved_args, target
            )

            full_command = f"{resolved_cmd} {resolved_args}".strip()

            # Log classifier success prediction (informational — does not gate execution)
            _pred_prob: float | None = None
            if _pdb is not None:
                try:
                    _pred_prob = _pdb.predict_success(resolved_cmd, category)
                except Exception:
                    pass

            # Execute
            c2_result = _c2_request("/api/run", method="POST", body={"command": full_command})
            if "_error" in c2_result or "error" in c2_result:
                output = _run_lazyown_command(full_command, step_timeout)
                via = "subprocess"
            else:
                output = c2_result.get("output", c2_result.get("result", ""))
                if not output:
                    output = _run_lazyown_command(full_command, step_timeout)
                    via = "subprocess"
                else:
                    via = "c2"

            # Record outcome in policy engine
            step = _policy.on_command_complete(
                target, resolved_cmd, resolved_args, output, None
            )

            # Annotate parquet knowledge base with the real outcome (rich version)
            if _pdb is not None:
                try:
                    import hashlib as _hl
                    from datetime import datetime as _dt
                    _ts = _dt.now().strftime("%Y-%m-%d %H:%M:%S")
                    _rid = _hl.sha256(
                        f"{_ts}|{resolved_cmd}|{resolved_args}|{target}".encode()
                    ).hexdigest()[:16]
                    # Get campaign_id if available
                    _camp_id = ""
                    try:
                        from lazyown_campaign import CampaignStore as _CS
                        _camp = _CS().load()
                        if _camp:
                            _camp_id = _camp.campaign_id
                    except Exception:
                        pass
                    _pdb.annotate_rich(
                        _rid,
                        output=output,
                        success=(step.outcome == "success"),
                        category=step.category,
                        outcome=step.outcome,
                        campaign_id=_camp_id,
                    )
                except Exception:
                    pass  # parquet annotation must never affect the loop

            # Track failures for adaptive selection
            fail_key = f"{target}:{step.category}:{resolved_cmd}"
            if step.outcome != "success":
                _fail_counts[fail_key] = _fail_counts.get(fail_key, 0) + 1

            # Update soul.md phase on high-value success
            if step.outcome == "success" and step.category in high_value_cats:
                if _OBJECTIVES_AVAILABLE:
                    try:
                        from lazyown_objective import SoulUpdater as _SoulUpdater
                        _SoulUpdater().update_phase(step.category)
                    except Exception:
                        pass

            # If recon just succeeded, trigger pwntomate and refresh facts
            pwntomate_note = ""
            if resolved_cmd in ("lazynmap", "nmap") and step.outcome == "success":
                pwntomate_note = _run_pwntomate_if_xml_ready(target)
                _refresh_facts(target)

            should_stop = (
                stop_on_high
                and step.outcome == "success"
                and step.category in high_value_cats
            )
            step_dict = {
                "command":    full_command,
                "category":   step.category,
                "outcome":    step.outcome,
                "reward":     step.reward,
                "confidence": step.confidence,
                "via":        via,
                "policy_rec": top_rec["reason"],
                "source":     top_rec["source"],
            }
            if _pred_prob is not None:
                step_dict["predicted_success_prob"] = round(_pred_prob, 3)
            if pwntomate_note:
                step_dict["pwntomate"] = pwntomate_note
            return {"stop": should_stop, "step": step_dict}

        for i in range(max_steps):
            result = await asyncio.get_event_loop().run_in_executor(None, _execute_step)
            if "step" in result:
                execution_log.append(result["step"])
            if result.get("stop"):
                break
            if i < max_steps - 1:
                await asyncio.sleep(step_delay)

        # Format report
        total_reward = sum(s["reward"] for s in execution_log)
        lines = [
            f"Auto-loop complete — {len(execution_log)} step(s) for target {target}",
            "",
        ]
        for i, s in enumerate(execution_log, 1):
            r_str = f"{s['reward']:+d}"
            lines.append(
                f"  Step {i}: [{s['via']}] {s['command']}"
                f"  ->  {s['category']}:{s['outcome']}"
                f"  (reward={r_str}, conf={s['confidence']:.0%})"
            )
            lines.append(f"           {s['policy_rec']}")
            if s.get("pwntomate"):
                lines.append(f"           [pwntomate] {s['pwntomate']}")
        lines.append(f"\nTotal reward: {total_reward:+d}")
        if execution_log:
            last = execution_log[-1]
            if last["outcome"] == "success" and last["category"] in high_value_cats:
                lines.append(
                    f"STOPPED: high-value success ({last['category']}) achieved."
                )
        return text("\n".join(lines))

    # ── llm_ask ───────────────────────────────────────────────────────────────
    elif name == "lazyown_llm_ask":
        if not _LLM_AVAILABLE:
            return text("LLM bridge unavailable. Check skills/lazyown_llm.py.")
        goal           = arguments["goal"]
        context        = arguments.get("context", "")
        backend        = arguments.get("backend", "groq")
        model_override = arguments.get("model", "") or None
        max_iter       = int(arguments.get("max_iterations", 6))
        sys_prompt     = arguments.get("system_prompt", "")

        cfg     = _load_payload()
        api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")

        if backend == "groq" and not api_key:
            return text(
                "Groq backend requires api_key in payload.json or GROQ_API_KEY env var. "
                "Use backend='ollama' for local deepseek-r1:1.5b (no key needed)."
            )

        result = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: _llm_ask(
                goal=goal,
                context=context,
                backend=backend,
                model=model_override,
                api_key=api_key if backend == "groq" else None,
                max_iterations=max_iter,
                system_prompt=sys_prompt,
            ),
        )
        return text(result)

    # ── inject_objective ──────────────────────────────────────────────────────
    elif name == "lazyown_inject_objective":
        if not _OBJECTIVES_AVAILABLE or _objectives is None:
            return text("Objective store unavailable. Check skills/lazyown_objective.py.")
        obj_text = arguments["text"]
        priority = arguments.get("priority", "high")
        notes    = arguments.get("notes", "")
        obj = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: _objectives.inject(obj_text, priority=priority, source="claude", notes=notes),
        )
        return text(
            f"Objective injected [{obj.id}] priority={obj.priority}\n"
            f"  {obj.text}\n\n"
            f"Queue now has {len(_objectives.list_pending(limit=100))} pending objective(s).\n"
            f"Use lazyown_auto_loop or lazyown_run_command to act on it."
        )

    # ── next_objective ────────────────────────────────────────────────────────
    elif name == "lazyown_next_objective":
        if not _OBJECTIVES_AVAILABLE:
            return text("Objective store unavailable.")
        ctx = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _full_context_for_claude()
        )
        parts = []
        parts.append("=== SOUL ===")
        parts.append(ctx.get("soul", "(none)"))
        parts.append("\n=== CURRENT ATTACK PLAN ===")
        parts.append(ctx.get("plan", "(none)"))
        parts.append(f"\n=== OBJECTIVES ({ctx.get('pending_count', 0)} pending) ===")
        next_obj = ctx.get("next_objective")
        if next_obj:
            parts.append(
                f"NEXT [{next_obj['priority']}] [{next_obj['id']}]\n  {next_obj['text']}"
            )
            if next_obj.get("notes"):
                parts.append(f"  Notes: {next_obj['notes']}")
            if next_obj.get("context"):
                parts.append(f"  Context: {json.dumps(next_obj['context'])}")
        else:
            parts.append("No pending objectives. Inject one with lazyown_inject_objective.")
        if ctx.get("pending_preview"):
            parts.append("\nFull queue:")
            for o in ctx["pending_preview"]:
                parts.append(f"  [{o['priority']:8s}] [{o['id']}] {o['text'][:80]}")
        return text("\n".join(parts))

    # ── soul ──────────────────────────────────────────────────────────────────
    elif name == "lazyown_soul":
        action  = arguments.get("action", "read")
        if action == "write":
            content = arguments.get("content", "")
            if not content.strip():
                return text("content must not be empty when action='write'.")
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: _write_soul(content)
            )
            return text("soul.md updated.")
        else:
            soul = await asyncio.get_event_loop().run_in_executor(None, _read_soul)
            return text(soul)

    # ── create_tool ───────────────────────────────────────────────────────────
    elif name == "lazyown_create_tool":
        toolname  = arguments["toolname"]
        command   = arguments["command"]
        trigger   = arguments["trigger"]
        active    = bool(arguments.get("active", True))
        try:
            tools_dir = LAZYOWN_DIR / "tools"
            written = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: _create_tool_file(toolname, command, trigger, active, tools_dir),
            )
            return text(
                f"Tool file created: {written}\n"
                f"  toolname: {toolname}\n"
                f"  trigger:  {trigger}\n"
                f"  active:   {active}\n"
                f"  command:  {command}\n\n"
                "Run 'pwntomate <nmap.xml> -x' or the pwntomate LazyOwn command "
                "to apply it to the current scan."
            )
        except Exception as exc:
            return text(f"Failed to create tool file: {exc}")

    # ── facts_show ────────────────────────────────────────────────────────────
    elif name == "lazyown_facts_show":
        if not _FACTS_AVAILABLE or _facts is None:
            return text(
                "FactStore unavailable. "
                "Run: python3 skills/lazyown_facts.py parse"
            )
        cfg    = _load_payload()
        target = arguments.get("target") or cfg.get("rhost") or None
        refresh = bool(arguments.get("refresh", False))

        def _do_facts() -> str:
            if refresh:
                _facts.parse_all(target=target)
            return _facts.summary(target)

        summary = await asyncio.get_event_loop().run_in_executor(None, _do_facts)
        return text(summary or "No facts found. Run with refresh=true to ingest sessions/ files.")

    # ── parquet_query ─────────────────────────────────────────────────────────
    elif name == "lazyown_parquet_query":
        if not _PDB_AVAILABLE or _pdb is None:
            return text("ParquetDB unavailable. Run: pip install pandas pyarrow")

        mode        = arguments.get("mode", "context")
        cfg         = _load_payload()
        target      = arguments.get("target") or cfg.get("rhost") or None
        phase       = arguments.get("phase", "recon")
        keyword     = arguments.get("keyword", "")
        parquet_name = arguments.get("parquet")
        success_only = bool(arguments.get("success_only", False))
        limit       = int(arguments.get("limit", 15))
        do_sync     = bool(arguments.get("sync", False))

        def _run_parquet_query() -> str:
            if do_sync:
                _pdb.sync()

            if mode == "stats":
                return _pdb.stats()

            if mode == "list":
                return "Available parquets:\n" + "\n".join(f"  • {p}" for p in _pdb.list_parquets())

            if mode == "keyword":
                if not keyword:
                    return "keyword mode requires 'keyword' argument."
                results = _pdb.query_knowledge(keyword, parquet_name, limit=limit)
                if not results:
                    return f"No results for keyword '{keyword}'."
                out_parts: list = []
                for stem, rows in results.items():
                    out_parts.append(f"\n── {stem} ({len(rows)} matches) ──")
                    for r in rows[:5]:
                        out_parts.append(
                            json.dumps({k: str(v)[:100] for k, v in r.items()}, ensure_ascii=False)
                        )
                return "\n".join(out_parts)

            if mode == "session":
                rows = _pdb.query_session(
                    phase=phase, target=target,
                    success_only=success_only, limit=limit,
                )
                if not rows:
                    return f"No session rows for phase='{phase}' target='{target}'."
                return json.dumps(rows, indent=2, default=str)

            # mode == "context" (default)
            ctx = _pdb.context_for_phase(phase, target, limit=limit)
            return json.dumps(ctx, indent=2, default=str)

        result = await asyncio.get_event_loop().run_in_executor(None, _run_parquet_query)
        return text(result)

    # ── parquet_annotate ──────────────────────────────────────────────────────
    elif name == "lazyown_parquet_annotate":
        if not _PDB_AVAILABLE or _pdb is None:
            return text("ParquetDB unavailable. Run: pip install pandas pyarrow")

        row_id   = arguments.get("row_id", "")
        success  = arguments.get("success")   # may be None
        category = arguments.get("category")
        outcome  = arguments.get("outcome")

        if not row_id:
            return text("row_id is required.")

        ok = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: _pdb.annotate(row_id, success=success, category=category, outcome=outcome),
        )
        if ok:
            return text(f"Annotated row {row_id}: success={success} category={category} outcome={outcome}")
        return text(f"Row id not found: {row_id}. Run lazyown_parquet_query(mode='session') to list ids.")

    # ── campaign ──────────────────────────────────────────────────────────────
    elif name == "lazyown_campaign":
        action = arguments.get("action", "status")

        def _run_campaign() -> str:
            try:
                from lazyown_campaign import CampaignStore
                cs = CampaignStore()
            except ImportError:
                return "lazyown_campaign.py not found in SKILLS_DIR."

            if action == "new":
                camp_name  = arguments.get("name", "default")
                scope      = arguments.get("scope", [])
                notes      = arguments.get("notes", "")
                camp = cs.create(camp_name, scope, notes=notes)
                return f"Campaign '{camp.name}' created. ID: {camp.campaign_id}"

            elif action == "status":
                return cs.summary()

            elif action == "phase":
                host  = arguments.get("host", "")
                phase = arguments.get("phase", "")
                if not host or not phase:
                    return "host and phase are required for action='phase'."
                cs.update_phase(host, phase)
                return f"Phase for {host} set to '{phase}'."

            elif action == "milestone":
                title = arguments.get("title", "")
                notes = arguments.get("notes", "")
                if not title:
                    return "title is required for action='milestone'."
                cs.add_milestone(title=title, notes=notes)
                return f"Milestone '{title}' added."

            elif action == "complete":
                notes = arguments.get("notes", "")
                cs.complete(notes=notes)
                return "Campaign marked complete."

            elif action == "add_scope":
                ip_or_cidr = arguments.get("ip_or_cidr", "")
                if not ip_or_cidr:
                    return "ip_or_cidr is required for action='add_scope'."
                cs.add_to_scope(ip_or_cidr)
                return f"Added '{ip_or_cidr}' to campaign scope."

            return f"Unknown campaign action: {action}"

        result = await asyncio.get_event_loop().run_in_executor(None, _run_campaign)
        return text(result)

    # ── daemon ────────────────────────────────────────────────────────────────
    elif name == "lazyown_daemon":
        action = arguments.get("action", "status")

        def _run_daemon() -> str:
            import subprocess, sys
            daemon_script = str(SKILLS_DIR / "lazyown_daemon.py")

            if action == "start":
                try:
                    proc = subprocess.Popen(
                        [sys.executable, daemon_script, "start"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    )
                    out, err = proc.communicate(timeout=10)
                    return (out + err).decode(errors="replace").strip() or "Daemon start requested."
                except Exception as exc:
                    return f"Failed to start daemon: {exc}"

            elif action == "stop":
                try:
                    proc = subprocess.run(
                        [sys.executable, daemon_script, "stop"],
                        capture_output=True, timeout=10,
                    )
                    return proc.stdout.decode(errors="replace").strip() or "Daemon stop requested."
                except Exception as exc:
                    return f"Failed to stop daemon: {exc}"

            elif action == "status":
                try:
                    proc = subprocess.run(
                        [sys.executable, daemon_script, "status"],
                        capture_output=True, timeout=10,
                    )
                    return proc.stdout.decode(errors="replace").strip() or "No daemon status available."
                except Exception as exc:
                    return f"Daemon status error: {exc}"

            return f"Unknown daemon action: {action}"

        result = await asyncio.get_event_loop().run_in_executor(None, _run_daemon)
        return text(result)

    # ── dynamic tools (lazyown_addon_*, lazyown_tool_*, lazyown_plugin_*) ────
    if _automapper is not None and (
        name.startswith("lazyown_addon_")
        or name.startswith("lazyown_tool_")
        or name.startswith("lazyown_plugin_")
    ):
        cfg = _load_payload()
        dyn_result = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: _automapper.dispatch(name, arguments, cfg, _run_lazyown_command),
        )
        if dyn_result is not None:
            return text(dyn_result)

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


# ── Hot-reload via SIGHUP ─────────────────────────────────────────────────────
# Sending SIGHUP re-execs the process in-place keeping the same PID visible
# to Claude Code — no reconnect needed.

import signal

def _handle_sighup(signum, frame):
    """Clean exit on SIGHUP — Claude Code will restart the server automatically."""
    sys.exit(0)

signal.signal(signal.SIGHUP, _handle_sighup)


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
