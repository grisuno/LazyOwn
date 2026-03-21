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
            name="lazyown_read_prompt",
            description=(
                "Read the LazyOwn developer reference (prompt.md). "
                "Contains the full architecture reference: MCP tools, command categories, "
                "payload.json schema, session file layout, C2 routes, addon/tool/plugin schemas, "
                "auto-loop algorithm, policy engine, FactStore, ObjectiveStore, ParquetDB API, "
                "and development rules (DO / DO NOT). "
                "Call this whenever you need to understand how a LazyOwn component works, "
                "what parameters it accepts, or how to add new capabilities without breaking "
                "existing integrations."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "description": (
                            "Optional section filter. Pass a heading keyword to get only that "
                            "section (e.g. 'MCP tool', 'payload.json', 'auto-loop', 'FactStore', "
                            "'reglas', 'campaign'). Leave empty to get the full document."
                        ),
                        "default": "",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_generate_report",
            description=(
                "Auto-generate a structured Markdown penetration test report "
                "from session artefacts (facts, events, credentials, objectives, plan). "
                "The report is written to sessions/report_<timestamp>.md and the path is returned."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "output": {
                        "type": "string",
                        "description": "Optional output file path. Defaults to sessions/report_<ts>.md.",
                        "default": "",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_cve_search",
            description=(
                "Search the NVD database for CVEs matching a product and optional version. "
                "Results are cached on disk. Returns id, CVSS score, severity, description, published date. "
                "Use this after discovering a service version to find known vulnerabilities."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Product name (e.g. 'openssh', 'apache httpd', 'vsftpd').",
                    },
                    "version": {
                        "type": "string",
                        "description": "Version string (e.g. '8.4', '2.4.49'). Optional.",
                        "default": "",
                    },
                    "max_results": {
                        "type": "string",
                        "description": "Maximum number of CVEs to return (default 10).",
                        "default": "10",
                    },
                },
                "required": ["product"],
            },
        ),
        types.Tool(
            name="lazyown_playbook_generate",
            description=(
                "Generate a MITRE ATT&CK-grounded playbook for a target using STIX2 "
                "technique data and Atomic Red Team tests. The playbook is derived "
                "from the current engagement phase in the WorldModel and saved as YAML. "
                "Returns the saved path and a step summary."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target IP or hostname to derive the playbook for.",
                    },
                    "phase": {
                        "type": "string",
                        "description": (
                            "Engagement phase override. One of: recon, scanning, "
                            "enumeration, exploitation, post_exploitation. "
                            "If omitted, derived from WorldModel."
                        ),
                        "default": "",
                    },
                    "platform": {
                        "type": "string",
                        "description": "Target platform: linux, windows, macos. Default: linux.",
                        "default": "linux",
                    },
                    "top_n": {
                        "type": "string",
                        "description": "Maximum number of steps to include (default 5).",
                        "default": "5",
                    },
                },
                "required": ["target"],
            },
        ),
        types.Tool(
            name="lazyown_playbook_run",
            description=(
                "Execute a previously generated playbook YAML against the target. "
                "Each step is dispatched as a LazyOwn MCP command. "
                "Tool output is parsed by ObsParser and ingested into WorldModel. "
                "Returns a result summary with per-step success/failure and findings."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the playbook YAML file.",
                        "default": "",
                    },
                    "target": {
                        "type": "string",
                        "description": (
                            "Target IP used for command substitution. "
                            "If omitted, uses the active target from payload.json."
                        ),
                        "default": "",
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "If true, log steps without executing them.",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_memory_recall",
            description=(
                "Query the episodic memory store for past command executions. "
                "Returns the most relevant past sessions matching the query — including "
                "what command was run, against which host, what findings were produced, "
                "and whether it succeeded. Use this before choosing a tool to avoid "
                "repeating failed approaches and to reuse proven techniques."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Free-text query: service name, CVE, technique, host IP.",
                    },
                    "host": {
                        "type": "string",
                        "description": "Filter results to a specific host IP.",
                        "default": "",
                    },
                    "top_k": {
                        "type": "string",
                        "description": "Number of results to return (default 5).",
                        "default": "5",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="lazyown_memory_store",
            description=(
                "Explicitly save a command execution to episodic memory. "
                "The auto_loop saves automatically, but use this tool to manually "
                "record important findings that should be recalled in future sessions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "host":    {"type": "string", "description": "Target host IP."},
                    "tool":    {"type": "string", "description": "Tool or technique name."},
                    "command": {"type": "string", "description": "Command that was executed."},
                    "output":  {"type": "string", "description": "Command output (will be trimmed to 2000 chars)."},
                    "success": {"type": "boolean", "description": "Whether it succeeded.", "default": True},
                },
                "required": ["host", "tool", "command", "output"],
            },
        ),
        types.Tool(
            name="lazyown_searchsploit",
            description=(
                "Search for public exploits matching a CVE ID or service name/version. "
                "Uses searchsploit CLI if available, falls back to ExploitDB. "
                "Returns exploit title, type, platform, and path."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "cve": {
                        "type": "string",
                        "description": "CVE identifier (e.g. CVE-2021-41773).",
                        "default": "",
                    },
                    "service": {
                        "type": "string",
                        "description": "Service name (e.g. 'apache', 'vsftpd').",
                        "default": "",
                    },
                    "version": {
                        "type": "string",
                        "description": "Service version (e.g. '2.4.49').",
                        "default": "",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_misp_export",
            description=(
                "Export current session findings as a MISP-compatible event JSON. "
                "Converts WorldModel hosts, services, credentials, and CVEs into "
                "typed MISP attributes. Saves to sessions/misp_event.json."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Filter to a specific target (default: all).",
                        "default": "",
                    },
                    "output": {
                        "type": "string",
                        "description": "Output file path (default: sessions/misp_event.json).",
                        "default": "",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_eval_quality",
            description=(
                "Show LLM decision quality report: success rate, top/worst MITRE tactics, "
                "confidence calibration. Helps identify where the auto_loop makes poor choices. "
                "Optionally export a fine-tuning dataset from successful decisions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Filter to a specific session (default: all sessions).",
                        "default": "",
                    },
                    "export_dataset": {
                        "type": "boolean",
                        "description": "Export fine-tuning JSONL to sessions/finetuning_dataset.jsonl.",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_collab_publish",
            description=(
                "Broadcast a structured event to all connected operators via SSE. "
                "Use this to share findings, alerts, or status updates in real time. "
                "Operators connected to /collab/stream will receive the event immediately."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "description": "Event type: 'finding', 'command', 'phase_change', 'alert', 'chat'.",
                    },
                    "payload": {
                        "type": "string",
                        "description": "JSON string with event payload data.",
                    },
                    "operator": {
                        "type": "string",
                        "description": "Operator name (default: 'agent').",
                        "default": "agent",
                    },
                },
                "required": ["type", "payload"],
            },
        ),
        types.Tool(
            name="lazyown_c2_profile",
            description=(
                "Show, set or list malleable C2 profiles. "
                "Profiles control beacon sleep interval, jitter, HTTP headers, "
                "URI paths, and user-agent — affecting how detectable C2 traffic is. "
                "Built-in profiles: default, stealth, aggressive, debug."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "'list' to show available profiles, 'show' to display one, 'set' to activate.",
                        "enum": ["list", "show", "set"],
                        "default": "list",
                    },
                    "name": {
                        "type": "string",
                        "description": "Profile name (required for show/set).",
                        "default": "",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_bridge_suggest",
            description=(
                "Query the full LazyOwn command catalog (347 commands, 11 phases) "
                "for the best command to run given engagement phase, services, "
                "credential state, and OS target. "
                "Args are auto-filled from the WorldModel (target IP, open port, creds). "
                "Catalog phases: recon (35), enum (71), exploit (61), postexp (40), "
                "cred (32), lateral (28), privesc (2), persist (30), exfil (19), "
                "c2 (14), report (15). "
                "Also accepts WorldModel phases: scanning, enumeration, exploitation, "
                "post_exploitation, lateral_movement, exfiltration. "
                "Use list_all=true to see every command for a phase. "
                "Use sequence=true to get the next 5 commands in priority order. "
                "Use tag_hint for technique-specific filtering: 'kerberos', 'smb', "
                "'web', 'ad', 'impacket', 'ldap', 'bruteforce', 'tunnel', 'av_bypass'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "phase": {
                        "type": "string",
                        "description": (
                            "Engagement phase: recon, scanning, enum, enumeration, "
                            "exploit, exploitation, postexp, post_exploitation, "
                            "cred, credential_access, lateral, lateral_movement, "
                            "privesc, privilege_escalation, persist, persistence, "
                            "exfil, exfiltration, c2, command_and_control, report, reporting."
                        ),
                        "default": "recon",
                    },
                    "target": {
                        "type": "string",
                        "description": "Target IP or hostname (used for arg substitution).",
                        "default": "",
                    },
                    "services": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Discovered services (e.g. ['http:80','ssh:22','smb:445',"
                            "'ldap:389','kerberos:88','winrm:5985']). "
                            "Filters catalog to commands relevant to those services."
                        ),
                        "default": [],
                    },
                    "excluded": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Command names to skip.",
                        "default": [],
                    },
                    "mitre_hint": {
                        "type": "string",
                        "description": "Prefer commands matching this MITRE technique (e.g. 'T1046', 'T1110').",
                        "default": "",
                    },
                    "tag_hint": {
                        "type": "string",
                        "description": (
                            "Filter by technique tag: 'kerberos', 'ad', 'smb', 'web', "
                            "'ldap', 'impacket', 'bruteforce', 'spray', 'tunnel', "
                            "'webshell', 'av_bypass', 'osint', 'dns', 'snmp', 'ssh'."
                        ),
                        "default": "",
                    },
                    "os_hint": {
                        "type": "string",
                        "description": "Target OS: 'linux', 'windows', or 'any' (default).",
                        "enum": ["any", "linux", "windows"],
                        "default": "any",
                    },
                    "list_all": {
                        "type": "boolean",
                        "description": "List ALL commands for the phase (sorted by priority).",
                        "default": False,
                    },
                    "sequence": {
                        "type": "boolean",
                        "description": "Return next 5 commands in kill-chain order.",
                        "default": False,
                    },
                    "catalog_summary": {
                        "type": "boolean",
                        "description": "Show full catalog summary (all phases + command counts).",
                        "default": False,
                    },
                },
                "required": [],
            },
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
            name="lazyown_groq_agent",
            description=(
                "Spawn an autonomous Groq or Ollama agent pre-loaded with 21 LazyOwn tools: "
                "run_command, bridge_suggest, bridge_catalog, parquet_context, facts_show, "
                "cve_lookup, memory_search, session_status, read_session_file, list_sessions, "
                "c2_status, c2_command, task_list, task_add, inject_objective, "
                "reactive_suggest, searchsploit, command_help, rag_query, threat_model, "
                "atomic_search. "
                "Groq uses native tool calling; Ollama uses ReAct prompt engineering. "
                "async_mode=False (default) blocks and returns the final answer. "
                "async_mode=True fires-and-forgets and returns an agent_id to poll with "
                "lazyown_agent_status / lazyown_agent_result."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": "Autonomous goal for the agent to pursue.",
                    },
                    "tools_filter": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Restrict the agent to a subset of the 18 tools. "
                            "Default: all tools. Example: ['run_command','bridge_suggest','facts_show']"
                        ),
                        "default": [],
                    },
                    "backend": {
                        "type": "string",
                        "enum": ["groq", "ollama"],
                        "description": "'groq' for native tool calling, 'ollama' for local ReAct.",
                        "default": "groq",
                    },
                    "max_iterations": {
                        "type": "integer",
                        "description": "Max tool-call iterations before the agent returns a Final Answer.",
                        "default": 8,
                    },
                    "async_mode": {
                        "type": "boolean",
                        "description": "True = fire-and-forget (returns agent_id); False = block until done.",
                        "default": False,
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Override the default agent system prompt (optional).",
                        "default": "",
                    },
                },
                "required": ["goal"],
            },
        ),
        types.Tool(
            name="lazyown_rag_index",
            description=(
                "Incrementally index all sessions/ artefacts (*.log, *.txt, *.csv, *.xml, "
                "*.json, *.nmap, *.md) into the ChromaDB semantic store. "
                "Only new or changed files are processed — safe to call from cron. "
                "mode='incremental' (default) indexes only new/changed files. "
                "mode='full' rebuilds the entire index from scratch. "
                "Returns: {files: N, chunks: N} counts."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["incremental", "full"],
                        "description": "Indexing mode.",
                        "default": "incremental",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_rag_query",
            description=(
                "Semantic search over indexed sessions/ artefacts. "
                "Returns the top-n most relevant chunks from logs, scan results, "
                "credential files, and other session data. "
                "Falls back to keyword search when ChromaDB is not available. "
                "Install ChromaDB for full semantic search: pip install chromadb"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query.",
                    },
                    "n": {
                        "type": "integer",
                        "description": "Number of results to return.",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="lazyown_threat_model",
            description=(
                "Build or load the blue team threat model from LazyOwn session data. "
                "Reads LazyOwn_session_report.csv, maps commands to MITRE ATT&CK techniques, "
                "and produces assets with risk scores, TTP catalogue, IOC registry, "
                "and Sigma-lite detection rules. "
                "Output saved to sessions/reports/threat_model.json. "
                "action='build' (re)generates the model. "
                "action='load' returns the last saved model. "
                "action='ttps' returns only the TTP list. "
                "action='rules' returns only detection rules. "
                "action='iocs' returns only the IOC registry. "
                "action='purple' returns the full purple team mapping (red TTP + blue detection side-by-side). "
                "action='gaps' returns TTPs with no detection rule (coverage gaps)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["build", "load", "ttps", "rules", "iocs", "purple", "gaps"],
                        "description": "What to return.",
                        "default": "build",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_atomic_search",
            description=(
                "Structured search over the 1690 Atomic Red Team technique tests "
                "(parquets/techniques_enriched.parquet). "
                "Supports simultaneous filtering by keyword, MITRE ID/prefix, platform, "
                "scope, prerequisites, and complexity. "
                "Returns id, name, mitre_id, platform_list, scope, complexity, "
                "has_prereqs, keyword_tags, description_preview — and optionally command_preview. "
                "Examples: keyword='bypass amsi' platform='windows'; "
                "mitre_id='T1548' platform='linux' complexity='low'; "
                "keyword='kerberos' no_prereqs=true."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Free-text search over name, description, tags.",
                        "default": "",
                    },
                    "mitre_id": {
                        "type": "string",
                        "description": "MITRE technique ID or prefix (T1059, T1059.001, T1548.002).",
                        "default": "",
                    },
                    "platform": {
                        "type": "string",
                        "description": "Target platform: linux | windows | macos | freebsd | cloud.",
                        "default": "",
                    },
                    "scope": {
                        "type": "string",
                        "enum": ["", "local", "remote", "elevated", "any"],
                        "description": "Execution scope.",
                        "default": "",
                    },
                    "complexity": {
                        "type": "string",
                        "enum": ["", "low", "medium", "high"],
                        "description": "Command complexity based on line count.",
                        "default": "",
                    },
                    "has_prereqs": {
                        "type": "boolean",
                        "description": "true = only tests with prerequisites; false = no prereqs needed.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results to return (default 10).",
                        "default": 10,
                    },
                    "include_command": {
                        "type": "boolean",
                        "description": "Include command_preview (first 300 chars) in results.",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_session_status",
            description=(
                "Show live C2 session state: active implants, their OS/user/hostname/IPs, "
                "privileged vs unprivileged status, discovered hosts, and open campaign tasks. "
                "Reads sessions/{client_id}.log CSV files, sessions/hostsdiscovery.txt, "
                "and sessions/tasks.json without touching lazyc2.py."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "client_id": {
                        "type": "string",
                        "description": "Filter to a specific client_id (default: all).",
                        "default": "",
                    },
                    "show_tasks": {
                        "type": "boolean",
                        "description": "Include campaign task board (default true).",
                        "default": True,
                    },
                    "show_outputs": {
                        "type": "boolean",
                        "description": "Include latest command outputs per implant (default false).",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_reactive_suggest",
            description=(
                "Parse raw command output and return prioritised reactive decisions. "
                "Detects: AV/EDR blocks (evasion via amsi.yaml/darkarmour), "
                "privesc hints (SUID/sudo/polkit → adversary_yaml/lazypwn), "
                "credentials found, new hosts discovered, service versions, "
                "and shell errors (switch-tool recommendations). "
                "Priority 1-2 decisions are auto-injected into the next auto_loop step."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "output": {
                        "type": "string",
                        "description": "Raw command output to analyse.",
                    },
                    "command": {
                        "type": "string",
                        "description": "The command that produced the output.",
                        "default": "",
                    },
                    "platform": {
                        "type": "string",
                        "description": "Target platform: 'linux', 'windows', or 'unknown'.",
                        "enum": ["linux", "windows", "unknown"],
                        "default": "unknown",
                    },
                    "max_decisions": {
                        "type": "integer",
                        "description": "Maximum decisions to return (default 5).",
                        "default": 5,
                    },
                },
                "required": ["output"],
            },
        ),
        types.Tool(
            name="lazyown_campaign_tasks",
            description=(
                "Manage campaign tasks in sessions/tasks.json. "
                "Statuses: New -> Refined -> Started -> Review -> Qa -> Done | Blocked. "
                "Use for campaign reporting beyond vulnbot's markdown — full task board "
                "with operator assignments and status tracking."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["list", "add", "update"],
                        "description": (
                            "'list' = show all tasks; "
                            "'add' = create a new task; "
                            "'update' = change a task's status."
                        ),
                        "default": "list",
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (required for action='add').",
                        "default": "",
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (used for action='add').",
                        "default": "",
                    },
                    "operator": {
                        "type": "string",
                        "description": "Operator assigned to the task (default: 'agent').",
                        "default": "agent",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID (required for action='update').",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["New", "Refined", "Started", "Review", "Qa", "Done", "Blocked"],
                        "description": "New status (required for action='update').",
                        "default": "New",
                    },
                    "filter_status": {
                        "type": "string",
                        "description": "Filter listed tasks by status (default: all).",
                        "default": "",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="lazyown_cron_schedule",
            description=(
                "Schedule a LazyOwn command to run at a specific time using the built-in "
                "cron system. LazyOwn's cron acts as a time-motor for autonomous activities: "
                "schedule recon at intervals, privesc attempts, lateral movement, or any "
                "command from the bridge catalog. Format: HH:MM. "
                "List scheduled crons or remove one by ID."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["add", "list", "remove"],
                        "description": "'add' schedules a command; 'list' shows all; 'remove' deletes by ID.",
                        "default": "list",
                    },
                    "time": {
                        "type": "string",
                        "description": "Execution time as HH:MM (required for action='add').",
                        "default": "",
                    },
                    "command": {
                        "type": "string",
                        "description": "LazyOwn command to schedule (required for action='add').",
                        "default": "",
                    },
                    "args": {
                        "type": "string",
                        "description": "Optional arguments for the command.",
                        "default": "",
                    },
                    "cron_id": {
                        "type": "string",
                        "description": "Cron entry ID to remove (required for action='remove').",
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
                        "type": "string",
                        "description": (
                            "Comma-separated IPs and/or CIDRs in scope (for 'new'). "
                            "Examples: '127.0.0.1', '10.10.11.0/24,10.10.12.0/24', '192.168.1.5,192.168.1.10'."
                        ),
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
        types.Tool(
            name="lazyown_fast_run",
            description=(
                "Launch the LazyOwn full-stack HackTheBox orchestrator "
                "(fast_run_as_r00t.sh). Opens a tmux session with: nmap recon, "
                "ping sweep, C2 implant, auto-loop, Flask C2 server, HTTP file "
                "server, and VPN pane. Optional panes controlled by payload.json "
                "flags: DeepSeek/Ollama, Discord C2, Telegram C2, Cloudflare "
                "tunnel, NC reverse shell. "
                "IMPORTANT: requires root — will prompt for sudo password via a "
                "GUI dialog (ssh-askpass/zenity/yad). "
                "Call with confirm=false first to see the plan without launching."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {
                        "type": "boolean",
                        "description": (
                            "Set to true to actually launch the stack. "
                            "Defaults to false (dry-run: shows the plan without executing)."
                        ),
                        "default": False,
                    },
                    "vpn": {
                        "type": "integer",
                        "description": "VPN interface index passed to --vpn (default 1).",
                        "default": 1,
                    },
                },
                "required": [],
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

        # --- OpenClaw-style world model + observation parser ---
        _wm = None
        _obs_parser = None
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from world_model import WorldModel, EngagementPhase
            from obs_parser import ObsParser
            _wm = WorldModel()
            _obs_parser = ObsParser()
        except Exception:
            pass

        execution_log: list[dict] = []
        # Track commands that failed this session per (target, category)
        _fail_counts: dict[str, int] = {}
        # Reactive engine — carries the highest-priority decision across steps
        _reactive_state: dict[str, str] = {}   # keys: "cmd", "args", "reason", "mitre"

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
            # Priority: reactive > parquet > bridge catalog > LLM recommender > cat_map
            resolved_cmd = ""
            resolved_args = ""

            # 0. Reactive engine: consume the top decision injected by the previous step
            if _reactive_state.get("cmd"):
                _r_parts = _reactive_state["cmd"].split(None, 1)
                resolved_cmd  = _r_parts[0]
                resolved_args = _r_parts[1] if len(_r_parts) > 1 else _reactive_state.get("args", "")
                _reactive_state.clear()

            # 1. Parquet: commands proven to work for this category+target
            hist_candidates = _parquet_candidates(category, target)
            for cand in hist_candidates:
                fail_key = f"{target}:{category}:{cand}"
                if _fail_counts.get(fail_key, 0) >= 2:
                    continue  # blocked: failed twice this session
                resolved_cmd = cand
                break

            # 1.5. Bridge catalog: phase-aware, service-matched recommendation
            if not resolved_cmd:
                try:
                    from lazyown_bridge import get_dispatcher as _get_bridge
                    _bridge = _get_bridge()
                    _phase_val = _wm.get_phase().value if _wm is not None else category
                    _services: list[str] = []
                    _has_creds_wm = False
                    _wm_snap = None
                    if _wm is not None:
                        _wm_snap = _wm.snapshot()
                        _host_info = _wm_snap.get("hosts", {}).get(target, {})
                        _svcs = _host_info.get("services", {})
                        _services = [
                            f"{v.get('name','')}" for v in _svcs.values()
                            if isinstance(v, dict)
                        ]
                        _has_creds_wm = bool(_wm_snap.get("credentials"))
                    _excl_set = {
                        k.split(":")[-1] for k, v in _fail_counts.items()
                        if k.startswith(f"{target}:") and v >= 2
                    }
                    _bridge_result = _bridge.suggest(
                        phase=_phase_val,
                        target=target,
                        services=_services,
                        has_creds=_has_creds_wm,
                        excluded=_excl_set,
                        world_snapshot=_wm_snap,
                    )
                    if _bridge_result is not None:
                        _bridge_cmd, _bridge_entry = _bridge_result
                        _bridge_parts = _bridge_cmd.split(None, 1)
                        resolved_cmd  = _bridge_parts[0]
                        resolved_args = _bridge_parts[1] if len(_bridge_parts) > 1 else ""
                except Exception:
                    pass

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

            # --- RAG context injection (OpenClaw style) ---
            _rag_context = ""
            try:
                sys.path.insert(0, str(MODULES_DIR))
                from session_rag import get_rag as _get_rag_auto
                _rag_auto = _get_rag_auto()
                _rag_auto.index_new()   # incremental — fast, no-op if nothing changed
                _rag_context = _rag_auto.context_for_step(
                    phase=_wm.get_phase().value if _wm is not None else category,
                    target=target,
                    cmd=resolved_cmd,
                    n=3,
                )
            except Exception:
                pass

            # --- Structured thought (OpenClaw-style reason-before-act) ---
            _thought = ""
            _mitre_tactic = ""
            _api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
            if _api_key:
                try:
                    _wm_context = _wm.to_context_string() if _wm is not None else "No world model available."
                    _thought_prompt = (
                        f"You are an autonomous penetration tester.\n"
                        f"Target: {target}\n"
                        f"Current phase: {_wm.get_phase().value if _wm else 'unknown'}\n"
                        f"World model:\n{_wm_context}\n\n"
                        + (f"{_rag_context}\n\n" if _rag_context else "")
                        + f"About to execute: {resolved_cmd} {resolved_args}\n"
                        f"Category: {category}\n\n"
                        f"Respond with a single JSON object (no markdown):\n"
                        f'{{"thought": "one sentence reasoning", '
                        f'"expected": "what success looks like", '
                        f'"mitre_tactic": "T-number or empty string", '
                        f'"confidence": 0.0}}'
                    )
                    from modules.llm_client import LLMClient as _LLMC
                    _llm = _LLMC(api_key=_api_key)
                    _raw_thought = _llm.ask(
                        _thought_prompt,
                        provider="groq",
                        system="You are a penetration testing reasoning engine. Reply only with valid JSON.",
                        temperature=0.1,
                    )
                    import re as _re
                    _jm = _re.search(r'\{.*\}', _raw_thought, _re.DOTALL)
                    if _jm:
                        _tj = json.loads(_jm.group())
                        _thought = _tj.get("thought", "")
                        _mitre_tactic = _tj.get("mitre_tactic", "")
                except Exception:
                    pass

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

            # --- Persist output for future RAG iterations ---
            if output and output.strip():
                try:
                    import re as _re_rag
                    _safe_cmd = _re_rag.sub(r"[^a-zA-Z0-9_-]", "_", resolved_cmd)[:40]
                    _out_dir  = SESSIONS_DIR / "auto_loop_outputs"
                    _out_dir.mkdir(parents=True, exist_ok=True)
                    _out_ts   = int(time.time())
                    (_out_dir / f"{_out_ts}_{_safe_cmd}.txt").write_text(
                        output[:8000], errors="replace"
                    )
                except Exception:
                    pass

            # --- Observation parsing + world model update ---
            if _obs_parser is not None and _wm is not None:
                try:
                    obs = _obs_parser.parse(output, host=target, tool=resolved_cmd)
                    _wm.update_from_findings(obs.findings)
                    # Auto-complete objectives satisfied by findings
                    if _OBJECTIVES_AVAILABLE and obs.findings:
                        try:
                            from lazyown_objective import ObjectiveStore as _OS
                            _ostore = _OS()
                            _pending = _ostore.peek()
                            if _pending:
                                _obj_text = _pending.get("title", _pending.get("description", ""))
                                _satisfied = any(
                                    f.value and len(f.value) > 3 and f.value.lower() in _obj_text.lower()
                                    for f in obs.findings
                                )
                                if _satisfied:
                                    _ostore.complete_current()
                        except Exception:
                            pass
                except Exception:
                    pass

            # --- Reactive engine: analyse output, inject top decision next step ---
            _reactive_decision_note = ""
            try:
                from reactive_engine import get_engine as _get_reactive
                _re_engine  = _get_reactive()
                _re_platform = "unknown"
                if _wm is not None:
                    try:
                        _re_platform = _wm.snapshot().get("hosts", {}).get(
                            target, {}
                        ).get("platform", "unknown")
                    except Exception:
                        pass
                _re_decisions = _re_engine.analyse(
                    output=output,
                    command=resolved_cmd,
                    platform=_re_platform,
                )
                if _re_decisions:
                    top_d = _re_decisions[0]
                    if top_d.priority <= 2 and not _reactive_state.get("cmd"):
                        _reactive_state["cmd"]   = top_d.command
                        _reactive_state["args"]  = ""
                        _reactive_state["reason"] = top_d.reason
                        _reactive_state["mitre"] = top_d.mitre_tactic
                        _reactive_decision_note = (
                            f"reactive:{top_d.action}:{top_d.command}"
                        )
            except Exception:
                pass

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
            if _thought:
                step_dict["thought"] = _thought
            if _mitre_tactic:
                step_dict["mitre_tactic"] = _mitre_tactic
            if _wm is not None:
                step_dict["phase"] = _wm.get_phase().value
            if _pred_prob is not None:
                step_dict["predicted_success_prob"] = round(_pred_prob, 3)
            if pwntomate_note:
                step_dict["pwntomate"] = pwntomate_note
            if _reactive_decision_note:
                step_dict["reactive"] = _reactive_decision_note
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
    elif name == "lazyown_read_prompt":
        section = arguments.get("section", "").strip().lower()
        prompt_path = LAZYOWN_DIR / "prompt.md"

        def _read_prompt() -> str:
            if not prompt_path.exists():
                return (
                    "prompt.md no encontrado en la raíz del proyecto. "
                    "El archivo documenta la arquitectura de LazyOwn. "
                    "Puede haberse excluido del repositorio (está en .gitignore)."
                )
            content = prompt_path.read_text(errors="replace")
            if not section:
                return content
            # Filter to the requested section only
            lines = content.splitlines()
            result_lines: list = []
            in_section = False
            for line in lines:
                if line.startswith("## ") or line.startswith("# "):
                    in_section = section in line.lower()
                if in_section:
                    result_lines.append(line)
                # Stop at next same-level heading after section found
                elif result_lines and (line.startswith("## ") or line.startswith("# ")):
                    break
            if result_lines:
                return "\n".join(result_lines)
            return f"Sección '{section}' no encontrada. Llama sin 'section' para ver el índice completo."

        result = await asyncio.get_event_loop().run_in_executor(None, _read_prompt)
        return text(result)

    elif name == "lazyown_generate_report":
        output_path = arguments.get("output", "").strip() or None
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from report_generator import ReportGenerator
            rg   = ReportGenerator(sessions_dir=LAZYOWN_DIR / "sessions")
            path = rg.generate(output_path=output_path)
            return text(f"Report generated: {path}")
        except Exception as exc:
            return text(f"[report error] {exc}")

    elif name == "lazyown_cve_search":
        product     = arguments.get("product", "").strip()
        version     = arguments.get("version", "").strip()
        max_results = int(arguments.get("max_results", "10") or "10")
        if not product:
            return text("[cve_search error] 'product' is required.")
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from cve_matcher import CVEMatcher
            matcher = CVEMatcher()
            results = await asyncio.get_event_loop().run_in_executor(
                None, lambda: matcher.search(product, version, max_results=max_results)
            )
            if not results:
                return text(f"No CVEs found for '{product} {version}'.".strip())
            lines = [f"CVEs for {product} {version}:".strip(), ""]
            for r in results:
                lines.append(f"[{r.severity:8s}] {r.id}  CVSS {r.cvss:.1f}  {r.published}")
                lines.append(f"  {r.description[:120]}")
                for ref in r.references:
                    lines.append(f"  -> {ref}")
                lines.append("")
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[cve_search error] {exc}")

    elif name == "lazyown_playbook_generate":
        pb_target   = arguments.get("target", "").strip()
        pb_phase    = arguments.get("phase", "").strip() or None
        pb_platform = arguments.get("platform", "linux").strip() or "linux"
        pb_top_n    = int(arguments.get("top_n", "5") or "5")
        if not pb_target:
            return text("[playbook_generate] 'target' is required.")
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from playbook_engine import PlaybookEngine
            engine   = PlaybookEngine(top_n=pb_top_n)
            playbook = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: engine.derive(pb_target, phase=pb_phase, platform=pb_platform),
            )
            saved_path = await asyncio.get_event_loop().run_in_executor(
                None, lambda: engine.save(playbook)
            )
            lines = [
                f"Playbook generated: {saved_path}",
                f"Target: {playbook.target}  Phase: {playbook.phase}  "
                f"Platform: {pb_platform}  Steps: {len(playbook.steps)}",
                "",
            ]
            for i, step in enumerate(playbook.steps, 1):
                atomic_id = step.atomic_id or "no atomic"
                lines.append(
                    f"  Step {i}: [{step.technique_id}] {step.name[:60]} "
                    f"({atomic_id})"
                )
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[playbook_generate error] {exc}")

    elif name == "lazyown_playbook_run":
        pb_path    = arguments.get("path", "").strip()
        pb_target  = arguments.get("target", "").strip()
        pb_dry_run = bool(arguments.get("dry_run", False))
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from playbook_engine import PlaybookEngine
            engine = PlaybookEngine()

            # Resolve playbook path
            if pb_path:
                pb_file = Path(pb_path)
            else:
                # Fall back to most recently modified playbook in sessions/
                sessions_pb = sorted(
                    (LAZYOWN_DIR / "sessions").glob("playbook_*.yaml"),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True,
                )
                if not sessions_pb:
                    return text("[playbook_run] No playbook found. Run lazyown_playbook_generate first.")
                pb_file = sessions_pb[0]

            playbook = await asyncio.get_event_loop().run_in_executor(
                None, lambda: engine.load(pb_file)
            )

            # Resolve target
            effective_target = pb_target or playbook.target
            if not effective_target:
                cfg = _load_payload()
                effective_target = cfg.get("rhost", "") or cfg.get("target_ip", "")

            # Executor: runs each step command via subprocess
            # Signature: (command, target) matching PlaybookEngine.execute() contract
            def _mcp_executor(command: str, target: str = "") -> str:
                import subprocess
                cmd = command.replace("{target}", target) if target else command
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    cwd=str(LAZYOWN_DIR),
                )
                return (result.stdout + result.stderr).strip()

            pb_result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: engine.execute(
                    playbook,
                    executor=_mcp_executor,
                    dry_run=pb_dry_run,
                ),
            )
            summary = engine.result_summary(pb_result)
            return text(summary)
        except Exception as exc:
            return text(f"[playbook_run error] {exc}")

    # ── memory_recall ──────────────────────────────────────────────────────────
    elif name == "lazyown_memory_recall":
        query  = arguments.get("query", "").strip()
        host   = arguments.get("host", "").strip()
        top_k  = int(arguments.get("top_k", "5") or "5")
        if not query and not host:
            return text("[memory_recall] 'query' or 'host' is required.")
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from memory_store import get_memory_store
            ms = get_memory_store()
            entries = ms.recall_by_host(host, top_k=top_k) if (host and not query) \
                      else ms.recall(query, top_k=top_k)
            if not entries:
                return text("No matching memories found.")
            lines = [f"Memory recall: {len(entries)} results for '{query or host}'", ""]
            for e in entries:
                status = "OK" if e.success else "FAIL"
                lines.append(f"[{status}] host={e.host} tool={e.tool}")
                lines.append(f"  cmd: {e.command[:100]}")
                lines.append(f"  out: {e.output_snippet[:120]}")
                if e.findings_json and e.findings_json != "[]":
                    lines.append(f"  findings: {e.findings_json[:120]}")
                lines.append("")
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[memory_recall error] {exc}")

    elif name == "lazyown_memory_store":
        m_host    = arguments.get("host", "").strip()
        m_tool    = arguments.get("tool", "").strip()
        m_command = arguments.get("command", "").strip()
        m_output  = arguments.get("output", "").strip()
        m_success = bool(arguments.get("success", True))
        if not all([m_host, m_tool, m_command]):
            return text("[memory_store] host, tool, command are required.")
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from memory_store import get_memory_store
            import uuid as _uuid
            ms = get_memory_store()
            ms.remember(
                session_id=_uuid.uuid4().hex[:8],
                host=m_host, tool=m_tool,
                command=m_command, output=m_output,
                findings=[], success=m_success,
            )
            stats = ms.stats()
            return text(f"Stored. Memory total: {stats.get('total', '?')} entries.")
        except Exception as exc:
            return text(f"[memory_store error] {exc}")

    # ── searchsploit ───────────────────────────────────────────────────────────
    elif name == "lazyown_searchsploit":
        sp_cve     = arguments.get("cve", "").strip()
        sp_service = arguments.get("service", "").strip()
        sp_version = arguments.get("version", "").strip()
        if not sp_cve and not sp_service:
            return text("[searchsploit] 'cve' or 'service' is required.")
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules" / "integrations"))
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from integrations.searchsploit import get_client as _sp_get
            client = _sp_get()
            results = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.search_cve(sp_cve) if sp_cve else client.search_service(sp_service, sp_version)
            )
            if not results:
                return text(f"No exploits found for '{sp_cve or sp_service}'.")
            lines = [f"Exploits for {sp_cve or (sp_service + ' ' + sp_version).strip()}:", ""]
            for r in results:
                lines.append(f"  [{r.type:10s}] [{r.platform:8s}] {r.title[:70]}")
                if r.cve:
                    lines.append(f"    CVE: {r.cve}")
                lines.append(f"    Path: {r.path}")
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[searchsploit error] {exc}")

    # ── misp_export ────────────────────────────────────────────────────────────
    elif name == "lazyown_misp_export":
        misp_target = arguments.get("target", "").strip() or None
        misp_output = arguments.get("output", "").strip() or None
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from integrations.misp_export import get_exporter as _misp_get
            exporter = _misp_get()
            event = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: exporter.export_session(LAZYOWN_DIR / "sessions", target=misp_target)
            )
            out_path = misp_output or str(LAZYOWN_DIR / "sessions" / "misp_event.json")
            saved = await asyncio.get_event_loop().run_in_executor(
                None, lambda: exporter.save(event, out_path)
            )
            return text(
                f"MISP event saved: {saved}\n"
                f"Attributes: {len(event.attributes)}  "
                f"Threat level: {event.threat_level_id}  "
                f"Tags: {', '.join(event.tags) or 'none'}"
            )
        except Exception as exc:
            return text(f"[misp_export error] {exc}")

    # ── eval_quality ───────────────────────────────────────────────────────────
    elif name == "lazyown_eval_quality":
        eq_session  = arguments.get("session_id", "").strip() or None
        eq_export   = bool(arguments.get("export_dataset", False))
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from llm_evaluator import get_evaluator
            ev      = get_evaluator()
            report  = ev.quality_report(session_id=eq_session)
            if eq_export:
                out_path = LAZYOWN_DIR / "sessions" / "finetuning_dataset.jsonl"
                exported = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: ev.export_finetuning_dataset(out_path)
                )
                report += f"\n\nFine-tuning dataset exported: {exported}"
            return text(report)
        except Exception as exc:
            return text(f"[eval_quality error] {exc}")

    # ── collab_publish ─────────────────────────────────────────────────────────
    elif name == "lazyown_collab_publish":
        cp_type     = arguments.get("type", "generic").strip()
        cp_payload  = arguments.get("payload", "{}").strip()
        cp_operator = arguments.get("operator", "agent").strip()
        try:
            payload_dict = json.loads(cp_payload) if cp_payload else {}
        except Exception:
            payload_dict = {"raw": cp_payload}
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from collab_bp import publish_event
            publish_event(type=cp_type, payload=payload_dict, operator=cp_operator)
            return text(f"Event '{cp_type}' published to {cp_operator} channel.")
        except Exception as exc:
            return text(f"[collab_publish error] {exc}")

    # ── c2_profile ─────────────────────────────────────────────────────────────
    elif name == "lazyown_c2_profile":
        cp_action = arguments.get("action", "list").strip()
        cp_name   = arguments.get("name", "").strip()
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from c2_profile import get_registry
            registry = get_registry()
            if cp_action == "list":
                names = registry.list_names()
                lines = ["Available C2 profiles:", ""]
                for n in names:
                    p = registry.get(n)
                    lines.append(f"  {n:12s}  sleep={p.sleep.interval_ms}ms  "
                                 f"jitter={p.sleep.jitter_pct}%  "
                                 f"ua={p.http_get.user_agent[:40]}")
                return text("\n".join(lines))
            elif cp_action in ("show", "set"):
                if not cp_name:
                    return text(f"[c2_profile] 'name' is required for action='{cp_action}'.")
                profile = registry.get(cp_name)
                if profile is None:
                    return text(f"[c2_profile] Unknown profile '{cp_name}'. "
                                f"Available: {registry.list_names()}")
                if cp_action == "set":
                    cfg = _load_payload()
                    cfg["c2_profile"] = cp_name
                    try:
                        payload_path = LAZYOWN_DIR / "payload.json"
                        import json as _json
                        payload_path.write_text(_json.dumps(cfg, indent=2))
                    except Exception:
                        pass
                lines = [
                    f"Profile: {profile.name}",
                    f"  {profile.description}",
                    f"  Sleep:   {profile.sleep.interval_ms}ms  Jitter: {profile.sleep.jitter_pct}%",
                    f"  GET UA:  {profile.http_get.user_agent}",
                    f"  GET URI: {profile.http_get.uri_paths}",
                    f"  POST URI:{profile.http_post.uri_paths}",
                    f"  Headers: {dict(list(profile.http_get.headers.items())[:3])}",
                ]
                if cp_action == "set":
                    lines.append(f"  Active profile set to '{cp_name}' in payload.json.")
                return text("\n".join(lines))
            else:
                return text(f"[c2_profile] Unknown action '{cp_action}'. Use: list, show, set.")
        except Exception as exc:
            return text(f"[c2_profile error] {exc}")

    # ── bridge_suggest ──────────────────────────────────────────────────────────
    elif name == "lazyown_bridge_suggest":
        bs_phase       = arguments.get("phase", "recon").strip() or "recon"
        bs_target      = arguments.get("target", "").strip()
        bs_services    = arguments.get("services", [])
        bs_excluded    = set(arguments.get("excluded", []))
        bs_mitre       = arguments.get("mitre_hint", "").strip()
        bs_tag         = arguments.get("tag_hint", "").strip()
        bs_os          = arguments.get("os_hint", "any").strip() or "any"
        bs_list_all    = bool(arguments.get("list_all", False))
        bs_sequence    = bool(arguments.get("sequence", False))
        bs_cat_summary = bool(arguments.get("catalog_summary", False))
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from lazyown_bridge import get_dispatcher as _bridge_dispatcher

            dispatcher = _bridge_dispatcher()

            # ── catalog_summary mode ──────────────────────────────────────
            if bs_cat_summary:
                summary = dispatcher.catalog_summary()
                lines = [
                    f"LazyOwn Bridge Catalog — {dispatcher.catalog_count()} commands",
                    f"Kill chain order: {' -> '.join(dispatcher.phase_kill_chain())}",
                    "",
                ]
                for phase, cmds in summary.items():
                    lines.append(f"  {phase:12s} ({len(cmds):3d}): {', '.join(cmds[:8])}"
                                 + (" ..." if len(cmds) > 8 else ""))
                return text("\n".join(lines))

            # ── list_all mode ─────────────────────────────────────────────
            if bs_list_all:
                entries = dispatcher.list_phase(bs_phase)
                if not entries:
                    return text(f"[bridge_suggest] No commands catalogued for phase '{bs_phase}'.")
                lines = [
                    f"Commands for phase '{bs_phase}' ({len(entries)} total):",
                    f"  Catalog total: {dispatcher.catalog_count()} commands",
                    "",
                ]
                for e in entries:
                    cred_tag = " [creds]" if e.requires_creds else ""
                    svc_tag  = f" [{','.join(e.services[:3])}]" if e.services else ""
                    os_tag   = f" [{e.os_target}]" if e.os_target != "any" else ""
                    tag_str  = f" #{','.join(e.tags[:2])}" if e.tags else ""
                    lines.append(
                        f"  {e.priority}. {e.command:30s}{cred_tag}{svc_tag}{os_tag}{tag_str}"
                        f"  {e.mitre_tactic}"
                    )
                    lines.append(f"       {e.description}")
                return text("\n".join(lines))

            # ── Load WorldModel snapshot for arg enrichment ───────────────
            _wm_snapshot = None
            try:
                from world_model import WorldModel
                _wm_snapshot = WorldModel().snapshot()
                if not bs_target and _wm_snapshot:
                    _hosts = list(_wm_snapshot.get("hosts", {}).keys())
                    if _hosts:
                        bs_target = _wm_snapshot.get("primary_target") or _hosts[0]
            except Exception:
                pass

            _has_creds = bool(_wm_snapshot.get("credentials")) if _wm_snapshot else False
            _eff_target = bs_target or _load_payload().get("rhost", "")

            # ── sequence mode ─────────────────────────────────────────────
            if bs_sequence:
                seq = dispatcher.suggest_sequence(
                    phase=bs_phase,
                    target=_eff_target,
                    services=bs_services,
                    has_creds=_has_creds,
                    excluded=bs_excluded,
                    world_snapshot=_wm_snapshot,
                    limit=5,
                )
                if not seq:
                    return text(f"[bridge_suggest] No sequence found for phase='{bs_phase}'.")
                lines = [f"Next {len(seq)} commands for phase '{bs_phase}':", ""]
                for i, (cmd_s, ent) in enumerate(seq, 1):
                    lines.append(f"  {i}. {cmd_s}")
                    lines.append(f"       [{ent.mitre_tactic}] {ent.description}")
                return text("\n".join(lines))

            # ── single suggest mode ───────────────────────────────────────
            result = dispatcher.suggest(
                phase=bs_phase,
                target=_eff_target,
                services=bs_services,
                has_creds=_has_creds,
                excluded=bs_excluded,
                world_snapshot=_wm_snapshot,
                mitre_hint=bs_mitre,
                tag_hint=bs_tag,
                os_hint=bs_os,
            )
            if result is None:
                return text(
                    f"[bridge_suggest] No suitable command for phase='{bs_phase}' "
                    f"services={bs_services} tag='{bs_tag}' os='{bs_os}'. "
                    f"Try list_all=true or catalog_summary=true."
                )
            cmd_str, entry = result
            tag_str = f" #{', #'.join(entry.tags)}" if entry.tags else ""
            os_str  = f" [{entry.os_target}]" if entry.os_target != "any" else ""
            lines = [
                f"Suggested: {cmd_str}",
                f"  Phase:       {entry.phase}",
                f"  MITRE:       {entry.mitre_tactic}",
                f"  Description: {entry.description}",
                f"  Priority:    {entry.priority}{os_str}{tag_str}",
            ]
            if entry.services:
                lines.append(f"  Services:    {', '.join(entry.services)}")
            if entry.requires_creds:
                lines.append("  Note: requires credentials in WorldModel")
            lines.append("")
            lines.append(f"Run: lazyown_run_command  command='{cmd_str}'")
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[bridge_suggest error] {exc}")

    # ── atomic_search ────────────────────────────────────────────────────────
    elif name == "lazyown_atomic_search":
        as_keyword      = arguments.get("keyword", "").strip()
        as_mitre        = arguments.get("mitre_id", "").strip()
        as_platform     = arguments.get("platform", "").strip()
        as_scope        = arguments.get("scope", "").strip()
        as_complexity   = arguments.get("complexity", "").strip()
        as_has_prereqs  = arguments.get("has_prereqs")   # None | True | False
        as_limit        = int(arguments.get("limit", 10))
        as_incl_cmd     = bool(arguments.get("include_command", False))
        if as_has_prereqs is not None:
            as_has_prereqs = bool(as_has_prereqs)
        if not any([as_keyword, as_mitre, as_platform, as_scope, as_complexity,
                    as_has_prereqs is not None]):
            return text(
                "[atomic_search] Provide at least one filter: keyword, mitre_id, "
                "platform, scope, complexity, or has_prereqs."
            )
        try:
            sys.path.insert(0, str(MODULES_DIR))
            from atomic_enricher import query_atomic as _qa, enrich as _enrich_atomic
            # Build enriched parquet on first use
            _enrich_atomic()
            rows = _qa(
                keyword=as_keyword,
                mitre_id=as_mitre,
                platform=as_platform,
                scope=as_scope,
                has_prereqs=as_has_prereqs,
                complexity=as_complexity,
                limit=as_limit,
                include_command=as_incl_cmd,
            )
            if not rows:
                return text(
                    f"[atomic_search] No results for: keyword='{as_keyword}' "
                    f"mitre='{as_mitre}' platform='{as_platform}' scope='{as_scope}' "
                    f"complexity='{as_complexity}'. Try broader filters."
                )
            lines = [f"Atomic Red Team search: {len(rows)} results\n"]
            for r in rows:
                plat_str  = ", ".join(r["platform_list"]) or "any"
                lines.append(
                    f"{r['mitre_id']:12s}  [{r['complexity']:6s}] [{r['scope']:8s}]  "
                    f"{r['name']}"
                )
                lines.append(
                    f"  platforms: {plat_str}   prereqs: {r['has_prereqs']}"
                )
                lines.append(f"  tags: {', '.join(r['keyword_tags'][:6])}")
                if as_incl_cmd and r.get("command_preview"):
                    lines.append(f"  command: {r['command_preview'][:120]}")
                lines.append("")
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[atomic_search error] {exc}")

    # ── rag_index ─────────────────────────────────────────────────────────────
    elif name == "lazyown_rag_index":
        rag_mode = arguments.get("mode", "incremental")
        try:
            sys.path.insert(0, str(MODULES_DIR))
            from session_rag import get_rag as _get_rag
            _rag = _get_rag()
            if rag_mode == "full":
                result_counts = await asyncio.get_event_loop().run_in_executor(
                    None, _rag.index_all
                )
            else:
                result_counts = await asyncio.get_event_loop().run_in_executor(
                    None, _rag.index_new
                )
            # Also index knowledge-base parquets (techniques, binarios, lolbas)
            pq_counts = await asyncio.get_event_loop().run_in_executor(
                None, lambda: _rag.index_parquet_sources(force=(rag_mode == "full"))
            )
            stats = _rag.stats()
            lines = [
                f"RAG index ({rag_mode}): {result_counts['files']} session files, "
                f"{result_counts['chunks']} new chunks",
                f"  + parquets:     {pq_counts['files']} KB files, "
                f"{pq_counts['chunks']} new chunks",
                f"Backend:        {stats['backend']}",
                f"Indexed files:  {stats['indexed_files']}",
                f"Total chunks:   {stats['total_chunks']}",
            ]
            if not stats["chroma_ok"]:
                lines.append("Note: chromadb not installed — using keyword fallback. "
                             "For semantic search: pip install chromadb")
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[rag_index error] {exc}")

    # ── rag_query ─────────────────────────────────────────────────────────────
    elif name == "lazyown_rag_query":
        rq_query = arguments.get("query", "").strip()
        rq_n     = int(arguments.get("n", 5))
        if not rq_query:
            return text("[rag_query] 'query' is required.")
        try:
            sys.path.insert(0, str(MODULES_DIR))
            from session_rag import get_rag as _get_rag
            _rag = _get_rag()
            # Trigger incremental index first so newly created files are visible
            await asyncio.get_event_loop().run_in_executor(None, _rag.index_new)
            hits = await asyncio.get_event_loop().run_in_executor(
                None, lambda: _rag.query(rq_query, rq_n)
            )
            if not hits:
                return text("No results found. Run lazyown_rag_index first.")
            lines = [f"RAG query: '{rq_query}'  ({len(hits)} hits)\n"]
            for i, h in enumerate(hits, 1):
                score_str = f"  score={h['score']:.3f}" if h["score"] is not None else ""
                lines.append(f"{i}. [{h['source']}]{score_str}")
                lines.append(h["text"].strip()[:300])
                lines.append("")
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[rag_query error] {exc}")

    # ── threat_model ──────────────────────────────────────────────────────────
    elif name == "lazyown_threat_model":
        tm_action = arguments.get("action", "build")
        try:
            sys.path.insert(0, str(MODULES_DIR))
            from threat_model import get_builder as _get_tm_builder
            _tmb = _get_tm_builder()
            if tm_action == "load":
                model = _tmb.load()
                if model is None:
                    return text("No threat model found — run with action='build' first.")
            else:
                model = await asyncio.get_event_loop().run_in_executor(None, _tmb.build)

            if tm_action in ("build", "load"):
                s = model.get("summary", {})
                lines = [
                    f"Threat Model  generated_at={model.get('generated_at','')}",
                    f"  Assets:          {len(model.get('assets', []))}  (highest risk: {s.get('highest_risk_asset','')})",
                    f"  TTPs:            {len(model.get('ttps', []))}  (dominant tactic: {s.get('dominant_tactic','')})",
                    f"  IOCs:            {len(model.get('ioc_registry', []))}",
                    f"  Detection rules: {len(model.get('detection_rules', []))}",
                    f"  Total events:    {s.get('total_events',0)}",
                    "",
                    "Top 5 TTPs:",
                ]
                for t in model.get("ttps", [])[:5]:
                    lines.append(
                        f"  {t['technique_id']:12s} [{t['severity']:8s}] {t['tactic']:28s} "
                        f"{t['technique_name']}  (x{t['occurrences']})"
                    )
                lines.append("")
                lines.append(f"Full model: sessions/reports/threat_model.json")
                return text("\n".join(lines))
            elif tm_action == "ttps":
                ttps = model.get("ttps", [])
                lines = [f"TTPs ({len(ttps)}):"]
                for t in ttps:
                    lines.append(
                        f"  {t['technique_id']:12s} [{t['severity']:8s}]  "
                        f"{t['technique_name']}  (x{t['occurrences']})"
                    )
                return text("\n".join(lines))
            elif tm_action == "rules":
                rules = model.get("detection_rules", [])
                lines = [f"Detection Rules ({len(rules)}):"]
                for r in rules:
                    lines.append(
                        f"  {r['rule_id']}  [{r['severity']:8s}]  {r['name']}"
                    )
                    lines.append(f"    log_source: {r['log_source']}  |  condition: {r['condition']}")
                    lines.append(f"    response: {r['response']}")
                return text("\n".join(lines))
            elif tm_action == "iocs":
                iocs = model.get("ioc_registry", [])
                lines = [f"IOC Registry ({len(iocs)}):"]
                for ioc in iocs[:50]:
                    lines.append(f"  {ioc['type']:12s}  {ioc['value']}")
                if len(iocs) > 50:
                    lines.append(f"  ... and {len(iocs) - 50} more")
                return text("\n".join(lines))
            elif tm_action == "purple":
                purple = model.get("purple_team", [])
                lines = [f"Purple Team Mapping ({len(purple)} TTPs)\n"]
                for p in purple:
                    gap_str = "  [COVERAGE GAP]" if p["gap"] else ""
                    lines.append(
                        f"{p['technique_id']:12s} [{p['severity']:8s}]  "
                        f"{p['technique_name']}{gap_str}"
                    )
                    r = p["red"]
                    lines.append(
                        f"  RED : {', '.join(r['commands'])}  "
                        f"(x{r['occurrences']}  {r['first_seen'][:10]} – {r['last_seen'][:10]})"
                    )
                    b = p["blue"]
                    if b:
                        lines.append(f"  BLUE: {b['rule_id']} {b['name']}")
                        lines.append(f"        {b['response']}")
                    else:
                        lines.append("  BLUE: no detection rule")
                    lines.append("")
                return text("\n".join(lines))
            elif tm_action == "gaps":
                purple = model.get("purple_team", [])
                gaps   = [p for p in purple if p["gap"]]
                covered = len(purple) - len(gaps)
                pct     = round(covered / len(purple) * 100) if purple else 0
                lines = [
                    f"Detection Coverage: {covered}/{len(purple)} TTPs covered ({pct}%)",
                    f"Coverage gaps: {len(gaps)}\n",
                ]
                for p in gaps:
                    lines.append(
                        f"  {p['technique_id']:12s} [{p['severity']:8s}]  {p['technique_name']}"
                    )
                    lines.append(
                        f"    Commands: {', '.join(p['red']['commands'])}"
                    )
                if not gaps:
                    lines.append("  All detected TTPs have a detection rule.")
                return text("\n".join(lines))
            return text(json.dumps(model, indent=2, default=str))
        except Exception as exc:
            return text(f"[threat_model error] {exc}")

    # ── groq_agent ───────────────────────────────────────────────────────────
    elif name == "lazyown_groq_agent":
        ga_goal       = arguments.get("goal", "").strip()
        if not ga_goal:
            return text("[groq_agent] 'goal' is required.")
        ga_tools      = arguments.get("tools_filter") or None
        ga_backend    = arguments.get("backend", "groq")
        ga_max_iter   = int(arguments.get("max_iterations", 8))
        ga_async      = bool(arguments.get("async_mode", False))
        ga_sys_prompt = arguments.get("system_prompt", "")
        try:
            sys.path.insert(0, str(SKILLS_DIR))
            from lazyown_groq_agents import get_pool as _groq_pool
            cfg     = _load_payload()
            api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
            pool    = _groq_pool()

            if ga_async:
                agent_id = pool.spawn(
                    goal=ga_goal, tools_filter=ga_tools,
                    api_key=api_key, backend=ga_backend,
                    max_iterations=ga_max_iter,
                    system_prompt=ga_sys_prompt,
                    block=False,
                )
                return text(
                    f"Agent spawned: {agent_id}\n"
                    f"Backend  : {ga_backend}\n"
                    f"Tools    : {len(ga_tools) if ga_tools else 18}\n"
                    f"Max iter : {ga_max_iter}\n\n"
                    f"Poll: lazyown_agent_status(agent_id='{agent_id}')\n"
                    f"Read: lazyown_agent_result(agent_id='{agent_id}')"
                )

            # Synchronous mode — run in thread executor so we don't block the
            # MCP async event loop while the agent iterates.
            def _blocking_run() -> str:
                aid = pool.spawn(
                    goal=ga_goal, tools_filter=ga_tools,
                    api_key=api_key, backend=ga_backend,
                    max_iterations=ga_max_iter,
                    system_prompt=ga_sys_prompt,
                    block=True,
                )
                return pool.result(aid)

            answer = await asyncio.get_event_loop().run_in_executor(
                None, _blocking_run
            )
            return text(answer)

        except Exception as exc:
            return text(f"[groq_agent error] {exc}")

    # ── session_status ────────────────────────────────────────────────────────
    elif name == "lazyown_session_status":
        filter_id    = arguments.get("client_id", "").strip()
        show_tasks   = bool(arguments.get("show_tasks", True))
        show_outputs = bool(arguments.get("show_outputs", False))
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from session_reader import get_aggregator as _get_session_agg
            summary = _get_session_agg().aggregate(SESSIONS_DIR)

            lines: list[str] = []

            # -- Active implants --
            client_ids = summary.active_client_ids
            if filter_id:
                client_ids = [c for c in client_ids if filter_id in c]
            lines.append(f"Active implants: {len(client_ids)}")
            for cid in client_ids:
                rec = summary.latest_for(cid)
                if rec is None:
                    continue
                priv = "PRIVILEGED" if rec.is_privileged else "user"
                lines.append(
                    f"  [{priv}] {cid} | {rec.hostname} | {rec.platform} | "
                    f"user={rec.user} | ips={rec.ips}"
                )
                if rec.result_portscan:
                    lines.append(f"    portscan: {rec.result_portscan[:120]}")
                if show_outputs and rec.output:
                    lines.append(f"    last output: {rec.output[:200]}")

            # -- Privileged vs unprivileged summary --
            priv_count   = len(summary.privileged_sessions)
            unpriv_count = len(summary.unprivileged_sessions)
            lines.append("")
            lines.append(f"Privileged sessions: {priv_count} | Unprivileged: {unpriv_count}")

            # -- Discovered hosts --
            if summary.discovered_hosts:
                lines.append("")
                lines.append(f"Discovered hosts ({len(summary.discovered_hosts)}):")
                for h in summary.discovered_hosts[:30]:
                    lines.append(f"  {h}")

            # -- Command outputs --
            if show_outputs and summary.command_outputs:
                lines.append("")
                lines.append(f"Recent command outputs ({len(summary.command_outputs)} files):")
                for stem, content in list(summary.command_outputs.items())[-5:]:
                    lines.append(f"  [{stem}] {content[:150]}")

            # -- Campaign tasks --
            if show_tasks and summary.tasks:
                lines.append("")
                lines.append(f"Campaign tasks ({len(summary.tasks)}):")
                for t in summary.tasks:
                    lines.append(f"  [{t.status:8s}] #{t.id} {t.title} (op={t.operator})")

            if not lines or (len(client_ids) == 0 and not summary.discovered_hosts):
                lines.append("No active sessions found. Start lazyc2.py and wait for implants.")

            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[session_status error] {exc}")

    # ── reactive_suggest ──────────────────────────────────────────────────────
    elif name == "lazyown_reactive_suggest":
        raw_output    = arguments.get("output", "")
        command       = arguments.get("command", "")
        platform      = arguments.get("platform", "unknown")
        max_decisions = int(arguments.get("max_decisions", 5))
        if not raw_output.strip():
            return text("[reactive_suggest] 'output' field is required.")
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from reactive_engine import get_engine as _get_react_engine
            engine    = _get_react_engine()
            decisions = engine.analyse(
                output=raw_output,
                command=command,
                platform=platform,
            )
            if not decisions:
                return text("No reactive signals detected in the provided output.")
            lines = [
                f"Reactive analysis — {len(decisions)} decision(s) found:",
                "",
            ]
            for i, d in enumerate(decisions[:max_decisions], 1):
                sigs = ", ".join(f"{s.kind}({s.value[:30]})" for s in d.signals[:3])
                lines.append(f"  {i}. [{d.action:12s}] priority={d.priority}")
                lines.append(f"       Command : {d.command}")
                lines.append(f"       Reason  : {d.reason}")
                lines.append(f"       MITRE   : {d.mitre_tactic}")
                lines.append(f"       Signals : {sigs}")
                lines.append("")
            if decisions and decisions[0].priority <= 2:
                lines.append(
                    f"AUTO-INJECT: top decision (priority {decisions[0].priority}) "
                    f"will be used as next auto_loop step."
                )
            return text("\n".join(lines))
        except Exception as exc:
            return text(f"[reactive_suggest error] {exc}")

    # ── campaign_tasks ────────────────────────────────────────────────────────
    elif name == "lazyown_campaign_tasks":
        action        = arguments.get("action", "list")
        filter_status = arguments.get("filter_status", "").strip()
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from session_reader import TaskReader as _TaskReader, TaskWriter as _TaskWriter

            if action == "list":
                tasks = _TaskReader().read(SESSIONS_DIR)
                if filter_status:
                    tasks = [t for t in tasks if t.status.lower() == filter_status.lower()]
                if not tasks:
                    return text(
                        f"No tasks found{' with status=' + filter_status if filter_status else ''}."
                        " Use action='add' to create one."
                    )
                lines = [f"Campaign tasks ({len(tasks)}):"]
                for t in tasks:
                    lines.append(
                        f"  #{t.id:3d} [{t.status:8s}] {t.title} (op={t.operator})"
                    )
                    if t.description:
                        lines.append(f"         {t.description[:100]}")
                return text("\n".join(lines))

            elif action == "add":
                title = arguments.get("title", "").strip()
                if not title:
                    return text("[campaign_tasks] 'title' is required for action='add'.")
                desc     = arguments.get("description", "")
                operator = arguments.get("operator", "agent")
                status   = arguments.get("status", "New")
                writer   = _TaskWriter(SESSIONS_DIR)
                task     = writer.append(
                    title=title, description=desc,
                    operator=operator, status=status,
                )
                return text(
                    f"Task #{task.id} created: [{task.status}] {task.title} (op={task.operator})"
                )

            elif action == "update":
                task_id = arguments.get("task_id")
                if task_id is None:
                    return text("[campaign_tasks] 'task_id' is required for action='update'.")
                status  = arguments.get("status", "")
                if not status:
                    return text("[campaign_tasks] 'status' is required for action='update'.")
                writer  = _TaskWriter(SESSIONS_DIR)
                ok      = writer.update_status(int(task_id), status)
                if ok:
                    return text(f"Task #{task_id} updated to status '{status}'.")
                return text(f"Task #{task_id} not found.")
            else:
                return text(f"[campaign_tasks] Unknown action '{action}'. Use: list, add, update.")
        except Exception as exc:
            return text(f"[campaign_tasks error] {exc}")

    # ── cron_schedule ─────────────────────────────────────────────────────────
    elif name == "lazyown_cron_schedule":
        action   = arguments.get("action", "list")
        cron_dir = SESSIONS_DIR / "crons"

        def _load_crons() -> list[dict]:
            path = cron_dir / "scheduled.json"
            if not path.exists():
                return []
            try:
                import json as _json
                return _json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return []

        def _save_crons(entries: list[dict]) -> None:
            cron_dir.mkdir(parents=True, exist_ok=True)
            path = cron_dir / "scheduled.json"
            import json as _json
            tmp = str(path) + ".tmp"
            Path(tmp).write_text(_json.dumps(entries, indent=2), encoding="utf-8")
            import os as _os
            _os.replace(tmp, str(path))

        if action == "list":
            entries = _load_crons()
            if not entries:
                return text(
                    "No cron entries scheduled. Use action='add' time='HH:MM' command='...' "
                    "to schedule a command. LazyOwn cron: cron HH:MM <command> [args]"
                )
            lines = [f"Scheduled crons ({len(entries)}):"]
            for e in entries:
                lines.append(
                    f"  [{e.get('id','?')}] {e.get('time','?')} -> "
                    f"{e.get('command','')} {e.get('args','')}"
                )
            return text("\n".join(lines))

        elif action == "add":
            cron_time = arguments.get("time", "").strip()
            command   = arguments.get("command", "").strip()
            if not cron_time or not command:
                return text("[cron_schedule] 'time' (HH:MM) and 'command' are required.")
            import re as _re
            if not _re.match(r"^\d{2}:\d{2}$", cron_time):
                return text(f"[cron_schedule] Invalid time format '{cron_time}'. Use HH:MM.")
            cron_args = arguments.get("args", "").strip()
            entries   = _load_crons()
            import uuid as _uuid
            new_id    = str(_uuid.uuid4())[:8]
            entries.append({
                "id": new_id, "time": cron_time,
                "command": command, "args": cron_args,
            })
            _save_crons(entries)
            # Also run via LazyOwn cron system
            full_cron_cmd = f"cron {cron_time} {command}"
            if cron_args:
                full_cron_cmd += f" {cron_args}"
            _run_lazyown_command(full_cron_cmd, timeout=10)
            return text(
                f"Cron #{new_id} added: {cron_time} -> {command} {cron_args}\n"
                f"LazyOwn cron registered: {full_cron_cmd}"
            )

        elif action == "remove":
            cron_id = arguments.get("cron_id", "").strip()
            if not cron_id:
                return text("[cron_schedule] 'cron_id' is required for action='remove'.")
            entries = _load_crons()
            before  = len(entries)
            entries = [e for e in entries if e.get("id") != cron_id]
            if len(entries) == before:
                return text(f"Cron ID '{cron_id}' not found.")
            _save_crons(entries)
            return text(f"Cron #{cron_id} removed.")
        else:
            return text(f"[cron_schedule] Unknown action '{action}'. Use: add, list, remove.")

    # ── soul ────────────────────────────────────────────────────────────────────
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
                camp_name = arguments.get("name", "default")
                raw_scope = arguments.get("scope", "")
                # Accept string (comma-sep), JSON array string, or already-a-list
                if isinstance(raw_scope, list):
                    scope = [s.strip() for s in raw_scope if s.strip()]
                elif isinstance(raw_scope, str):
                    raw_scope = raw_scope.strip()
                    if raw_scope.startswith("["):
                        try:
                            scope = json.loads(raw_scope)
                        except Exception:
                            scope = [raw_scope]
                    else:
                        scope = [s.strip() for s in raw_scope.split(",") if s.strip()]
                else:
                    scope = []
                notes = arguments.get("notes", "")
                camp = cs.create(camp_name, scope, notes=notes)
                scope_str = ", ".join(scope) if scope else "(none)"
                return f"Campaign '{camp.name}' created. ID: {camp.campaign_id}\nScope: {scope_str}"

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

    # ── fast_run ──────────────────────────────────────────────────────────────
    elif name == "lazyown_fast_run":
        confirm = bool(arguments.get("confirm", False))
        vpn     = int(arguments.get("vpn", 1))

        cfg     = _load_payload()
        rhost   = cfg.get("rhost", "<not set>")
        domain  = cfg.get("domain", "<not set>")

        plan_lines = [
            "LazyOwn fast_run_as_r00t.sh — launch plan",
            "==========================================",
            f"  Primary target  : rhost={rhost}",
            f"  Domain          : {domain}",
            f"  VPN interface   : {vpn}",
            "",
            "Panes that will open in tmux session 'lazyown_sessions':",
            "  [0] Recon        — lazynmap full scan",
            "  [1] Network      — addhosts + ping sweep",
            "  [2] C2 implant   — createcredentials + c2 launch",
            "  [3] Auto-loop    — autonomous loop",
            "  [4] lazyc2       — Flask C2 server (unprivileged)",
            "  [5] www          — HTTP file server + certs",
            "  [6] VPN          — tun interface",
            "",
            "Optional panes (driven by payload.json flags):",
            "  DeepSeek/Ollama, Discord C2, Telegram C2, Cloudflare tunnel, NC revshell",
            "",
            "sudo password will be requested via GUI dialog (ssh-askpass/zenity/yad).",
            "A display (DISPLAY/WAYLAND_DISPLAY) must be available.",
        ]

        if not confirm:
            plan_lines += [
                "",
                "DRY RUN — nothing launched.",
                "Call with confirm=true to start the stack.",
            ]
            return text("\n".join(plan_lines))

        def _launch() -> str:
            import subprocess, os, shutil, time

            askpass_script = str(LAZYOWN_DIR / "modules" / "gui_askpass.sh")
            fast_run       = str(LAZYOWN_DIR / "fast_run_as_r00t.sh")

            if not os.path.isfile(askpass_script):
                return f"[fast_run] SUDO_ASKPASS helper not found: {askpass_script}"
            if not os.path.isfile(fast_run):
                return f"[fast_run] Script not found: {fast_run}"

            # Ensure gui_askpass.sh is executable
            os.chmod(askpass_script, 0o755)

            env = os.environ.copy()
            env["SUDO_ASKPASS"] = askpass_script

            try:
                proc = subprocess.Popen(
                    ["sudo", "-A", "./fast_run_as_r00t.sh",
                     "--no-attach", "--vpn", str(vpn)],
                    cwd=str(LAZYOWN_DIR),
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True,
                )
            except Exception as exc:
                return f"[fast_run] Failed to launch: {exc}"

            # Wait for tmux session to initialise (up to 15 s)
            session_up = False
            for _ in range(15):
                time.sleep(1)
                try:
                    r = subprocess.run(
                        ["tmux", "has-session", "-t", "lazyown_sessions"],
                        capture_output=True,
                    )
                    if r.returncode == 0:
                        session_up = True
                        break
                except Exception:
                    pass

            # Collect any early output / errors (non-blocking)
            try:
                out, err = proc.communicate(timeout=0.1)
            except subprocess.TimeoutExpired:
                out, err = b"", b""

            lines = ["\n".join(plan_lines), ""]
            if session_up:
                lines.append("tmux session 'lazyown_sessions' is UP.")
                lines.append("Attach manually:  tmux attach -t lazyown_sessions")
            else:
                lines.append(
                    "WARNING: tmux session 'lazyown_sessions' not detected after 15 s. "
                    "The script may still be initialising."
                )
                lines.append(
                    "Check manually:  tmux ls  |  tmux attach -t lazyown_sessions"
                )
            if err:
                lines.append("")
                lines.append("stderr (first 500 chars):")
                lines.append(err.decode(errors="replace")[:500])
            return "\n".join(lines)

        result = await asyncio.get_event_loop().run_in_executor(None, _launch)
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
