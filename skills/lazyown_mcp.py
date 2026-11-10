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
import shlex
import shutil
import ssl
import struct
import subprocess
import sys
import termios
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# ── MCP server import first — this is the only blocking requirement ───────────
from mcp.server import Server

# ── All optional skill imports are lazy (deferred to first handler call) ──────
# This keeps the MCP startup handshake fast (<3.5s).
# Each _*_AVAILABLE flag starts as None (unchecked) and is set True/False
# on first use by the _ensure_* helpers below.

_mcp_root = Path(__file__).parent
_mcp_lazyown = _mcp_root.parent
for _p in [str(_mcp_lazyown / "modules"), str(_mcp_root)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from mcp_lazy import ensure_optional as _ensure_optional

_CREDENTIAL_FLAGS: dict[str, tuple[str | None, str | None]] = {
    "gobuster": ("-U", "-P"),
    "hydra": ("-l", "-p"),
    "medusa": ("-u", "-p"),
    "ncrack": ("-u", "-P"),
}
_MEM_SNIPPET_LIMIT = 2000
_ENGINE_AVAILABLE = None
_BRIDGE_AVAILABLE = None
_STATE_AVAILABLE = None
_RECOMMENDER_AVAILABLE = None
_NARRATOR_AVAILABLE = None
_POLICY_AVAILABLE = None
_FACTS_AVAILABLE = None
_OBJECTIVES_AVAILABLE = None
_LLM_AVAILABLE = None
_AUTOMAPPER_AVAILABLE = None
_PDB_AVAILABLE = None
_HIVE_AVAILABLE = None
_AUTO_AVAILABLE = None
_ACI_AVAILABLE = None

# Lazy singletons (populated on first use)
_policy = None
_facts = None
_objectives = None
_AutoMapper = None


def _ensure_engine():
    def _load(ns):
        from event_engine import ack_event, add_rule, load_rules, process_new_rows, read_events
        from event_engine import is_running as _hb_is_running

        ns.update(
            process_new_rows=process_new_rows,
            read_events=read_events,
            ack_event=ack_event,
            add_rule=add_rule,
            load_rules=load_rules,
            _hb_is_running=_hb_is_running,
        )
        return True

    return _ensure_optional(globals(), "_ENGINE_AVAILABLE", _load)


def _ensure_bridge():
    def _load(ns):
        from mcp_agent_bridge import get_agent_result, get_agent_status, list_agents, start_agent

        ns.update(
            start_agent=start_agent,
            get_agent_status=get_agent_status,
            get_agent_result=get_agent_result,
            list_agents=list_agents,
        )
        return True

    return _ensure_optional(globals(), "_BRIDGE_AVAILABLE", _load)


def _ensure_state():
    def _load(ns):
        from session_state import load as _state_load
        from session_state import refresh as _state_refresh

        ns.update(_state_load=_state_load, _state_refresh=_state_refresh)
        return True

    return _ensure_optional(globals(), "_STATE_AVAILABLE", _load)


def _ensure_recommender():
    def _load(ns):
        from recommender import recommend_and_save as _recommend

        ns.update(_recommend=_recommend)
        return True

    return _ensure_optional(globals(), "_RECOMMENDER_AVAILABLE", _load)


def _sitrep_recommendations(limit: int = 3) -> list[dict[str, Any]]:
    """Return top-N next-step suggestions for the sitrep payload.

    ``recommend_and_save`` reads target state from ``session_state`` and
    resolves the API key itself, so no positional arguments are forwarded.

    Args:
        limit: Maximum number of suggestions to return.

    Returns:
        ``{"command", "score", "reasoning"}`` dicts, or a single
        ``{"error": ...}`` entry when the recommender is unavailable or
        raises.
    """
    if not _ensure_recommender() or _recommend is None:
        return [{"error": "recommender module unavailable"}]
    try:
        recs = _recommend() or []
    except Exception as exc:
        return [{"error": str(exc)}]
    suggestions: list[dict[str, Any]] = []
    for item in recs:
        if not isinstance(item, dict):
            continue
        command = str(item.get("command", "")).strip()
        if not command or command == "_error":
            continue
        suggestions.append(
            {
                "command": command,
                "score": float(item.get("confidence", item.get("score", 0.0)) or 0.0),
                "reasoning": str(item.get("reason", item.get("reasoning", "")) or ""),
            }
        )
    return suggestions[: max(int(limit), 0)]


def _ensure_narrator():
    def _load(ns):
        from timeline_narrator import load_timeline as _load_timeline
        from timeline_narrator import narrate as _narrate

        ns.update(_narrate=_narrate, _load_timeline=_load_timeline)
        return True

    return _ensure_optional(globals(), "_NARRATOR_AVAILABLE", _load)


def _ensure_policy():
    def _load(ns):
        from lazyown_policy import LazyOwnPolicyIntegration as _PI

        ns.update(_policy=_PI())
        return True

    return _ensure_optional(globals(), "_POLICY_AVAILABLE", _load)


def _ensure_facts():
    def _load(ns):
        try:
            from lazyown_facts import FactStore as _FS
            from lazyown_facts import create_tool_file as _ctf
        except Exception:

            def _create_tool_file(*_a, **_kw):
                raise RuntimeError("lazyown_facts not available")

            ns.update(_create_tool_file=_create_tool_file)
            return False
        ns.update(_facts=_FS(), _create_tool_file=_ctf)
        return True

    return _ensure_optional(globals(), "_FACTS_AVAILABLE", _load)


def _ensure_objectives():
    def _load(ns):
        from lazyown_objective import ObjectiveStore as _OS
        from lazyown_objective import current_plan as _cp
        from lazyown_objective import full_context_for_claude as _fc
        from lazyown_objective import read_soul as _rs
        from lazyown_objective import write_soul as _ws

        ns.update(
            _objectives=_OS(),
            _read_soul=_rs,
            _write_soul=_ws,
            _current_plan=_cp,
            _full_context_for_claude=_fc,
        )
        return True

    return _ensure_optional(globals(), "_OBJECTIVES_AVAILABLE", _load)


def _ensure_llm():
    def _load(ns):
        from lazyown_llm import build_bridge as _build_bridge
        from lazyown_llm import llm_ask as _llm_ask

        ns.update(_llm_ask=_llm_ask, _build_bridge=_build_bridge)
        return True

    return _ensure_optional(globals(), "_LLM_AVAILABLE", _load)


def _ensure_automapper():
    def _load(ns):
        from lazyown_automapper import AutoMapper as _AM

        ns.update(_AutoMapper=_AM)
        return True

    return _ensure_optional(globals(), "_AUTOMAPPER_AVAILABLE", _load)


def _ensure_pdb():
    def _load(ns):
        try:
            from lazyown_parquet_db import get_pdb as _gpdb
        except Exception:

            def _get_pdb(_=None):
                return None

            ns.update(_get_pdb=_get_pdb)
            return False
        ns.update(_get_pdb=_gpdb)
        return True

    return _ensure_optional(globals(), "_PDB_AVAILABLE", _load)


def _ensure_hive():
    def _load(ns):
        from hive_mind import get_hive as _get_hive
        from hive_mind import mcp_hive_collect as _hive_collect
        from hive_mind import mcp_hive_forget as _hive_forget
        from hive_mind import mcp_hive_plan as _hive_plan
        from hive_mind import mcp_hive_recall as _hive_recall
        from hive_mind import mcp_hive_recover as _hive_recover
        from hive_mind import mcp_hive_result as _hive_result
        from hive_mind import mcp_hive_spawn as _hive_spawn
        from hive_mind import mcp_hive_status as _hive_status

        ns.update(
            _get_hive=_get_hive,
            _hive_spawn=_hive_spawn,
            _hive_status=_hive_status,
            _hive_recall=_hive_recall,
            _hive_plan=_hive_plan,
            _hive_result=_hive_result,
            _hive_collect=_hive_collect,
            _hive_forget=_hive_forget,
            _hive_recover=_hive_recover,
        )
        return True

    return _ensure_optional(globals(), "_HIVE_AVAILABLE", _load)


def _ensure_auto():
    def _load(ns):
        from autonomous_daemon import mcp_autonomous_events as _auto_events
        from autonomous_daemon import mcp_autonomous_inject as _auto_inject
        from autonomous_daemon import mcp_autonomous_start as _auto_start
        from autonomous_daemon import mcp_autonomous_status as _auto_status
        from autonomous_daemon import mcp_autonomous_stop as _auto_stop

        ns.update(
            _auto_start=_auto_start,
            _auto_stop=_auto_stop,
            _auto_status=_auto_status,
            _auto_inject=_auto_inject,
            _auto_events=_auto_events,
        )
        return True

    return _ensure_optional(globals(), "_AUTO_AVAILABLE", _load)


def _ensure_aci():
    def _load(ns):
        from aci_planner import mcp_aci_plan as _aci_plan
        from aci_planner import mcp_aci_replan as _aci_replan
        from aci_planner import mcp_aci_status as _aci_status

        ns.update(_aci_plan=_aci_plan, _aci_status=_aci_status, _aci_replan=_aci_replan)
        return True

    return _ensure_optional(globals(), "_ACI_AVAILABLE", _load)


# Stubs for names referenced before lazy init (avoid NameError at parse time)
_state_load = _state_refresh = None
_recommend = None
_narrate = _load_timeline = None
_create_tool_file = None
_read_soul = _write_soul = _current_plan = _full_context_for_claude = None
_llm_ask = _build_bridge = None


def _get_pdb(_=None):
    return None


_get_hive = _hive_spawn = _hive_status = _hive_recall = None
_hive_plan = _hive_result = _hive_collect = _hive_forget = _hive_recover = None
_auto_start = _auto_stop = _auto_status = _auto_inject = _auto_events = None
_aci_plan = _aci_status = _aci_replan = None
process_new_rows = read_events = ack_event = add_rule = load_rules = _hb_is_running = None
start_agent = get_agent_status = get_agent_result = list_agents = None
from mcp import types  # noqa: E402
from mcp.server.stdio import stdio_server  # noqa: E402

# ── Harness layer singletons (lazy — depend on SESSIONS_DIR set below) ────────
_perm_system = None  # PermissionSystem
_hook_registry = None  # HookRegistry
_session_transcript = None  # SessionTranscript
_compact_output_fn = None  # compact_output callable
_claudemd_loader = None  # ClaudeMdLoader


def _get_perm_system():
    """Return PermissionSystem singleton (deny-first rule evaluator)."""
    global _perm_system
    if _perm_system is None:
        try:
            from lazyown_permissions import PermissionSystem

            _perm_system = PermissionSystem(SESSIONS_DIR)
        except Exception:
            pass
    return _perm_system


def _get_hooks():
    """Return HookRegistry singleton."""
    global _hook_registry
    if _hook_registry is None:
        try:
            from lazyown_hooks import get_registry

            _hook_registry = get_registry(SESSIONS_DIR)
        except Exception:
            pass
    return _hook_registry


def _get_transcript():
    """Return active SessionTranscript singleton."""
    global _session_transcript
    if _session_transcript is None:
        try:
            from lazyown_session import get_transcript

            _session_transcript = get_transcript(SESSIONS_DIR)
        except Exception:
            pass
    return _session_transcript


def _compact(content: str, tool_name: str = "_default") -> str:
    """Apply 5-layer context compaction to a tool result string."""
    global _compact_output_fn
    if _compact_output_fn is None:
        try:
            from lazyown_context import compact_output

            _compact_output_fn = compact_output
        except Exception:

            def _compact_output_fn(c, t="_default"):
                return c

    return _compact_output_fn(content, tool_name)


def _get_claudemd():
    """Return ClaudeMdLoader singleton."""
    global _claudemd_loader
    if _claudemd_loader is None:
        try:
            from lazyown_claudemd import ClaudeMdLoader

            _claudemd_loader = ClaudeMdLoader(LAZYOWN_DIR)
        except Exception:
            pass
    return _claudemd_loader


# ── Paths ─────────────────────────────────────────────────────────────────────
SKILLS_DIR = Path(__file__).parent
LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(SKILLS_DIR.parent)))
PAYLOAD_FILE = LAZYOWN_DIR / "payload.json"
SESSIONS_DIR = LAZYOWN_DIR / "sessions"
BASE_DIR = LAZYOWN_DIR
MODULES_DIR = LAZYOWN_DIR / "modules"

# ── Helper module (pure-function logic for new high-impact tools) ─────────────
from lazyown_mcp_helpers import (  # noqa: E402
    DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
    JobStore,
    audit_tasks,
    build_target_context,
    diff_snapshot,
    evidence_freshness,
    evidence_grep,
    is_likely_credential,
    needs_confirmation,
    preflight_command,
    take_snapshot,
)

_job_store = JobStore()

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

            _threading.Thread(target=lambda: _pdb.sync(), daemon=True, name="pdb-sync").start()
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


def _has_data(path: Path) -> bool:
    """Return True when a session file exists and holds content."""
    return path.is_file() and path.stat().st_size > 0


def _save_payload(data: dict) -> str:
    """Persist payload.json atomically with an audit trail (mode 0600)."""
    try:
        from core.config import save_payload as _canonical_save

        _canonical_save(data, PAYLOAD_FILE)
        os.chmod(PAYLOAD_FILE, 0o600)
        return "ok"
    except Exception:
        pass
    try:
        with open(PAYLOAD_FILE, "w") as f:
            json.dump(data, f, indent=2)
        os.chmod(PAYLOAD_FILE, 0o600)
        return "ok"
    except Exception as e:
        return "error: unable to save payload"


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

    def _verified_context() -> "ssl.SSLContext":
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        try:
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        except (AttributeError, ValueError):
            pass
        return context

    def _is_lab_target(name: str) -> bool:
        value = (name or "").strip().strip("[]").lower()
        if value in ("localhost",):
            return True
        try:
            import ipaddress as _ip

            addr = _ip.ip_address(value)
            return bool(addr.is_loopback or addr.is_private or addr.is_link_local)
        except ValueError:
            return False

    try:
        with urllib.request.urlopen(req, context=_verified_context(), timeout=10) as resp:
            return json.loads(resp.read().decode())
    except ssl.SSLCertVerificationError:
        if not _is_lab_target(host) or os.environ.get("LAZYOWN_MCP_INSECURE_TLS", "") == "0":
            return {"error": "TLS verification failed"}
        try:
            import logging as _logging

            _logging.getLogger("lazyown_mcp").warning("unverified TLS fallback for lab C2 %r", host)
        except Exception:
            pass
        fallback = ssl.create_default_context()
        fallback.check_hostname = False
        fallback.verify_mode = ssl.CERT_NONE
        try:
            fallback.minimum_version = ssl.TLSVersion.TLSv1_2
        except (AttributeError, ValueError):
            pass
        try:
            with urllib.request.urlopen(req, context=fallback, timeout=10) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}"}
        except Exception:
            return {"error": "C2 request failed"}
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}"}
    except Exception:
        return {"error": "C2 request failed"}


# ── Tool handler dispatch table ────────────────────────────────────────────────
# The decorator-based registry replaces the giant ``if / elif`` chain with
# O(1) dispatch.  Handlers not yet migrated still work via the fallback path
# inside ``call_tool``.  Add new handlers with ``@register_handler("name")``.

_TOOL_HANDLERS: dict[str, Any] = {}


def register_handler(tool_name: str):
    """Decorator that registers an async handler for *tool_name*.

    The decorated function receives ``(arguments: dict, tool_name: str)``
    and must return ``list[types.TextContent]``.
    """

    def _decorator(func):
        _TOOL_HANDLERS[tool_name] = func
        return func

    return _decorator


def _make_text(tool_name: str, content: str) -> list[types.TextContent]:
    """Return a ``TextContent`` list after compacting *content*."""
    compacted = _compact(content, tool_name)
    try:
        t = _get_transcript()
        if t is not None:
            t.append("tool_result", {"tool_name": tool_name, "content": compacted[:800]})
    except Exception:
        pass
    return [types.TextContent(type="text", text=compacted)]


# ── Registered handlers (migrated from the call_tool elif chain) ───────────────


















# ── New module handlers (ExploitRecommender, EvasionEngine, AutoPivot, Dashboard) ──
























































































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

try:
    from mcp_tools import iter_schemas as _iter_registry_schemas
    from mcp_tools import register_handlers as _register_registry_handlers
    from mcp_tools._context import MCPContext as _MCPContext

    def _policy_integration_or_none():
        """Return the shared policy singleton when available, else None."""
        return _policy if _ensure_policy() else None

    async def _all_tools():
        """Return the full tool catalogue, resolving ``list_tools`` lazily."""
        return await list_tools()

    _MCP_TOOL_CONTEXT = _MCPContext(
        text=_make_text,
        load_payload=_load_payload,
        save_payload=_save_payload,
        lazyown_dir=LAZYOWN_DIR,
        sessions_dir=SESSIONS_DIR,
        modules_dir=MODULES_DIR,
        skills_dir=SKILLS_DIR,
        run_command=_run_lazyown_command,
        c2_request=_c2_request,
        get_policy=_policy_integration_or_none,
        get_transcript=_get_transcript,
        get_perm_system=_get_perm_system,
        get_hooks=_get_hooks,
        get_claudemd=_get_claudemd,
        job_store=_job_store,
        list_tools=_all_tools,
        sitrep_recommendations=_sitrep_recommendations,
    )
    _REGISTERED_TOOL_NAMES = _register_registry_handlers(_TOOL_HANDLERS, _MCP_TOOL_CONTEXT)
except Exception as _registry_exc:  # noqa: BLE001
    _logging.getLogger("lazyown_mcp").warning(
        "mcp_tools registry unavailable: %s", _registry_exc
    )
    _REGISTERED_TOOL_NAMES = []

    def _iter_registry_schemas():
        """Fallback when the one-file-per-tool registry failed to load."""
        return iter(())


def _registry_schemas() -> list[types.Tool]:
    """Return the schemas of every one-file-per-tool module, discovered live.

    Resolved at ``list_tools`` call time so a newly added tool file is
    picked up without editing this module. Any discovery error degrades to
    an empty list rather than breaking the whole tool listing.
    """
    try:
        return list(_iter_registry_schemas())
    except Exception:
        return []


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        # ── Unified Dashboard ─────────────────────────────────────────────────────
        # ── Master campaign SITREP ────────────────────────────────────────────
        # ── Session intelligence ──────────────────────────────────────────────
        # ── C2 AI endpoints ───────────────────────────────────────────────────
        # ── Hive Mind tools ────────────────────────────────────────────────────
        # ── END Hive Mind tools ────────────────────────────────────────────────
        # ── Autonomous Daemon tools ─────────────────────────────────────────
        # ── END Autonomous Daemon tools ─────────────────────────────────────
        # ── Engage Orchestrator tools ───────────────────────────────────────
        # ── END Engage Orchestrator tools ───────────────────────────────────
        # ── Pipeline Engine tools (Pillar 3) ────────────────────────────────
        # ── END Pipeline Engine tools ───────────────────────────────────────
        # ── Campaign management ───────────────────────────────────────────────
        # ── Unified daemon management ─────────────────────────────────────────
        # ── ACI — Autonomous Campaign Intelligence ───────────────────────
        # ── harness / meta tools ─────────────────────────────────────────
    ] + (_automapper.mcp_tools() if _automapper is not None else []) + _registry_schemas()


# ── Tool handlers ─────────────────────────────────────────────────────────────


def substitute_playbook_target(command: str, target: str) -> str:
    """Substitute the {target} token in a playbook step command.

    The value is shell-quoted so metacharacters in the target cannot break
    out of the step command. Step template syntax (pipes, redirects) is
    preserved because only the substituted value is quoted.

    Args:
        command: Step command template containing {target}.
        target: Target value to substitute.

    Returns:
        Command with the quoted target in place of the token.
    """
    return command.replace("{target}", shlex.quote(target)) if target else command


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:

    def text(content: str) -> list[types.TextContent]:
        return _make_text(name, content)

    # ── Permission Gate (deny-first, Claude Code style) ──────────────────────
    perm = _get_perm_system()
    if perm is not None:
        _perm_decision, _perm_reason = perm.evaluate(name, arguments)
        if _perm_decision == "deny":
            try:
                hooks = _get_hooks()
                if hooks is not None:
                    from lazyown_hooks import HookEvent

                    hooks.run(
                        HookEvent.PERMISSION_DENIED,
                        {
                            "tool_name": name,
                            "arguments": arguments,
                            "_event": "permission_denied",
                        },
                    )
            except Exception:
                pass
            return text(
                f"❌ PERMISSION DENIED\n"
                f"Tool:   {name}\n"
                f"Reason: {_perm_reason}\n\n"
                f"To allow this tool, use:\n"
                f"  lazyown_manage_permissions(action='add_rule', "
                f"tool_pattern='{name}', rule_action='allow')\n\n"
                f"Or change mode to 'bypass_permissions' for unrestricted access:\n"
                f"  lazyown_manage_permissions(action='set_mode', mode='bypass_permissions')"
            )
        if _perm_decision == "ask":
            # In non-interactive contexts log the ask and proceed (don't block autonomous agents)
            # Operators can set mode=dont_ask to actually enforce the ask→deny behaviour.
            pass

    # ── Pre-tool-use hooks ────────────────────────────────────────────────────
    try:
        hooks = _get_hooks()
        if hooks is not None:
            from lazyown_hooks import HookEvent

            _hook_ctx = hooks.run(
                HookEvent.PRE_TOOL_USE,
                {
                    "tool_name": name,
                    "arguments": arguments,
                    "_event": "pre_tool_use",
                },
            )
            if _hook_ctx.get("_block"):
                return text(
                    f"🛡️ BLOCKED BY HOOK\n"
                    f"Tool:   {name}\n"
                    f"Reason: {_hook_ctx.get('_block_reason', 'hook denied execution')}"
                )
            # Log tool_use to transcript after hooks pass
            t = _get_transcript()
            if t is not None:
                t.append("tool_use", {"tool_name": name, "arguments": arguments})
    except Exception:
        pass

    # ── Registry-dispatched tools (one file per tool) run after the full ──────
    # perm gate and pre-tool hooks so they share the same policy and auditing.
    dispatched = _TOOL_HANDLERS.get(name)
    if dispatched is not None:
        return (
            await dispatched(arguments, name)
            if asyncio.iscoroutinefunction(dispatched)
            else dispatched(arguments, name)
        )

    # ── dynamic tools (lazyown_addon_*, lazyown_tool_*, lazyown_plugin_*) ────
    if _automapper is not None and (
        name.startswith("lazyown_addon_") or name.startswith("lazyown_tool_") or name.startswith("lazyown_plugin_")
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

import signal  # noqa: E402


def _handle_sighup(signum, frame):
    """Clean exit on SIGHUP — Claude Code will restart the server automatically."""
    sys.exit(0)


signal.signal(signal.SIGHUP, _handle_sighup)


# ── Entry point ───────────────────────────────────────────────────────────────


async def main():
    import sys as _sys

    # --sse [PORT]  → run as HTTP/SSE daemon (default port 9871)
    # default       → stdio (Claude Code subprocess model)
    if "--sse" in _sys.argv:
        try:
            _idx = _sys.argv.index("--sse")
            _port = int(_sys.argv[_idx + 1]) if _idx + 1 < len(_sys.argv) else 9871
        except (ValueError, IndexError):
            _port = 9871
        import uvicorn
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        _sse_transport = SseServerTransport("/messages/")

        async def _handle_sse(request):
            async with _sse_transport.connect_sse(request.scope, request.receive, request._send) as streams:
                await server.run(streams[0], streams[1], server.create_initialization_options())

        async def _handle_messages(scope, receive, send):
            await _sse_transport.handle_post_message(scope, receive, send)

        _app = Starlette(
            routes=[
                Route("/sse", endpoint=_handle_sse),
                Mount("/messages/", app=_handle_messages),
            ]
        )
        print(f"[mcp] SSE server on http://127.0.0.1:{_port}/sse", flush=True)
        await uvicorn.Server(uvicorn.Config(_app, host="127.0.0.1", port=_port, log_level="warning")).serve()
    else:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
