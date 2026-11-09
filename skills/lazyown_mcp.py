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
        types.Tool(
            name="lazyown_session_init",
            description=(
                "SITREP — Call this FIRST in every new session. "
                "Returns a full situation report: "
                "(1) active config: rhost, domain, lhost, lport, os_id. "
                "(2) OS cross-reference: compares payload.json os_id vs OS detected in nmap scan — "
                "flags conflicts so you know whether to trust the config or update it. "
                "(3) Nmap evidence: checks if sessions/scan_{rhost}.nmap and "
                "sessions/vulns_{rhost}.nmap already exist — lists open ports from them. "
                "(4) Pwntomate evidence: checks sessions/{rhost}/{port}/{tool}/ dirs. "
                "If scans already exist DO NOT re-run them — read the files instead. "
                "(5) Tasks from sessions/tasks.json — pending vs done. "
                "(6) Active objectives from sessions/objectives.jsonl. "
                "(7) World model state for rhost: services, credentials, vulnerabilities. "
                "(8) Engagement phase + top commands for current phase. "
                "(9) Gap analysis: what's missing and recommended next steps. "
                "Pass format='json' to get structured output (preferred for agents). "
                "Pass include_recommend=true to embed top-3 ranked next-step suggestions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Output format: 'pretty' (human banner, default) or 'json' (structured dict).",
                        "enum": ["pretty", "json"],
                        "default": "pretty",
                    },
                    "include_recommend": {
                        "type": "boolean",
                        "description": "Embed top-3 ranked next-step suggestions from the recommender.",
                        "default": False,
                    },
                    "freshness_threshold_seconds": {
                        "type": "integer",
                        "description": "Mark scan/pwntomate evidence as stale beyond this age (default 7d).",
                        "default": DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
                    },
                },
            },
        ),
        types.Tool(
            name="lazyown_run_command_async",
            description=(
                "Submit a long-running LazyOwn command to a background job. Returns a job_id "
                "immediately. Poll with lazyown_job_status. Use this for lazynmap, pwntomate, "
                "auto_loop and anything documented as ≥30min. The synchronous run_command tool "
                "blocks the agent; this one frees it to work on something else."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "LazyOwn shell command(s) to execute, newline-separated.",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Max seconds before the job is killed (default 1800).",
                        "default": 1800,
                    },
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="lazyown_job_status",
            description=(
                "Inspect background jobs created by lazyown_run_command_async. "
                "Without job_id returns a list of recent jobs; with job_id returns full record "
                "including stdout once the job finishes."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "Job identifier from lazyown_run_command_async.",
                        "default": "",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "List size when job_id is omitted (default 20).",
                        "default": 20,
                    },
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
        # ── Unified Dashboard ─────────────────────────────────────────────────────
        # ── Master campaign SITREP ────────────────────────────────────────────
        # ── Session intelligence ──────────────────────────────────────────────
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
        # ── C2 AI endpoints ───────────────────────────────────────────────────
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
        types.Tool(
            name="lazyown_search_tools",
            description=(
                "Search for LazyOwn MCP tools by keyword. "
                "Use this to discover tools when you know what capability you need "
                "but not the exact tool name. "
                "Example: query='smb' returns all SMB-related tools."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keyword to search in tool names and descriptions.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results to return (default 15).",
                        "default": 15,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="lazyown_manage_permissions",
            description=(
                "View or modify the LazyOwn permission system. "
                "Actions: status | set_mode | add_rule | remove_rule | list_rules. "
                "Modes: default | dont_ask | bypass_permissions | plan. "
                "Rule actions: allow | deny | ask. "
                "Example: add allow rule for 'lazyown_run_command' so it never asks."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "status | set_mode | add_rule | remove_rule | list_rules",
                        "enum": ["status", "set_mode", "add_rule", "remove_rule", "list_rules"],
                    },
                    "mode": {
                        "type": "string",
                        "description": "Permission mode (for set_mode action).",
                    },
                    "tool_pattern": {
                        "type": "string",
                        "description": "Glob pattern for tool name (for add_rule/remove_rule).",
                    },
                    "rule_action": {
                        "type": "string",
                        "description": "allow | deny | ask (for add_rule).",
                    },
                    "condition": {
                        "type": "string",
                        "description": "Optional condition: 'contains:<text>' or 'target:<glob>'.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Human note for the rule.",
                        "default": "",
                    },
                },
                "required": ["action"],
            },
        ),
        types.Tool(
            name="lazyown_harness_status",
            description=(
                "Defense-in-depth dashboard. Aggregates status from all 5 harness layers: "
                "permissions (allow/deny/ask counts) + hooks (runs/blocks/errors) + "
                "transcripts (event counts, compact boundaries) + compaction stats + "
                "CLAUDE.md hierarchy. Call this to see if the harness is healthy."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="lazyown_session_resume",
            description=(
                "Reconstruct context from an append-only session transcript. "
                "Returns: event counts, recent tool calls, key findings, "
                "permission decisions, and compact boundaries. Use to pick up "
                "where a previous session left off."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Transcript session_id (12-char). Empty = current active session.",
                        "default": "",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max recent events to summarize (default 50).",
                        "default": 50,
                    },
                },
            },
        ),
        types.Tool(
            name="lazyown_subagent_run",
            description=(
                "Run a goal in an ISOLATED subagent transcript (sidechain). "
                "Forks the parent transcript so the subagent has no permission inheritance, "
                "wraps tool calls to log to the sidechain, and returns ONLY the summary "
                "to the parent context (no inflation). Full subagent transcript "
                "remains on disk for audit."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": "What the subagent should accomplish.",
                    },
                    "backend": {
                        "type": "string",
                        "description": "groq | ollama (default groq).",
                        "default": "groq",
                    },
                    "max_iterations": {
                        "type": "integer",
                        "description": "Max steps (default 5).",
                        "default": 5,
                    },
                },
                "required": ["goal"],
            },
        ),
        types.Tool(
            name="lazyown_claudemd",
            description=(
                "Manage LazyOwn's CLAUDE.md instruction hierarchy (4 levels: "
                "managed → user → project → local). "
                "Actions: status | load | create_user | create_project | create_local | add_rule. "
                "Files are merged in priority order on each session start."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "status | load | create_user | create_project | create_local | add_rule",
                        "enum": ["status", "load", "create_user", "create_project", "create_local", "add_rule"],
                    },
                    "content": {
                        "type": "string",
                        "description": "File content (for create_* / add_rule actions).",
                        "default": "",
                    },
                    "rule_name": {
                        "type": "string",
                        "description": "Rule file name without extension (for add_rule).",
                        "default": "",
                    },
                },
                "required": ["action"],
            },
        ),
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

    # ── run_agent ─────────────────────────────────────────────────────────────
    if name == "lazyown_run_agent":
        if not _ensure_bridge():
            return text("Agent bridge not available — check modules/mcp_agent_bridge.py")

        goal = arguments["goal"]
        backend = arguments.get("backend", "ollama")
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
            # Traceability: log spawn to parent transcript (no isolation, just audit)
            try:
                parent = _get_transcript()
                if parent is not None:
                    parent.append(
                        "agent_spawned",
                        {
                            "agent_id": agent_id,
                            "goal": goal,
                            "backend": backend,
                            "isolated": False,
                        },
                    )
            except Exception:
                pass
            return text(
                f"Agent started.\n"
                f"  id:      {agent_id}\n"
                f"  goal:    {goal}\n"
                f"  backend: {backend} (max {max_iterations} steps)\n\n"
                f"Poll with: lazyown_agent_status('{agent_id}')\n"
                f"Results:   lazyown_agent_result('{agent_id}')\n\n"
                f"For ISOLATED execution (sidechain transcript), use:\n"
                f"  lazyown_subagent_run(goal=..., backend=..., max_iterations=...)"
            )
        except Exception as e:
            return text(f"Failed to start agent: {e}")

    # ── session_init ──────────────────────────────────────────────────────────
    elif name == "lazyown_session_init":
        import glob as _glob
        import json as _json
        from pathlib import Path as _Path

        out_format = (arguments.get("format") or "pretty").lower()
        include_recommend = bool(arguments.get("include_recommend", False))
        freshness_threshold = int(
            arguments.get(
                "freshness_threshold_seconds",
                DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
            )
        )

        # ── 1. Payload config ────────────────────────────────────────────────
        cfg = _load_payload()
        rhost = cfg.get("rhost", "")
        domain = cfg.get("domain", "")
        lhost = cfg.get("lhost", "")
        lport = str(cfg.get("lport", ""))
        os_id_cfg = cfg.get("os_id", "unknown")  # what payload.json says

        # ── 2. World model ───────────────────────────────────────────────────
        wm_path = LAZYOWN_DIR / "sessions" / "world_model.json"
        phase = "recon"
        wm_host_state = "unscanned"
        wm_services: list[str] = []
        wm_creds: list[str] = []
        wm_vulns: list[str] = []
        try:
            if wm_path.exists():
                wm = _json.loads(wm_path.read_text())
                from modules.killchain import KillChain

                phase = KillChain.current_phase(world_model_path=wm_path)
                h = wm.get("hosts", {}).get(rhost, {})
                wm_host_state = h.get("state", "unscanned")
                for svc in h.get("services", {}).values():
                    wm_services.append(
                        f"    {svc.get('port', '?')}/{svc.get('protocol', 'tcp')} "
                        f"{svc.get('name', '?')} {svc.get('version', '')}"
                    )
                for c in wm.get("credentials", [])[:5]:
                    wm_creds.append(f"    {c.get('username', '?')}:{c.get('secret', '?')[:20]} ({c.get('type', '?')})")
                for v in wm.get("vulnerabilities", [])[:5]:
                    wm_vulns.append(
                        f"    {v.get('cve', '?')} {v.get('severity', '?')} — {v.get('description', '')[:60]}"
                    )
        except Exception:
            pass

        # ── 3. Nmap scan evidence ────────────────────────────────────────────
        # lazynmap.sh creates: sessions/scan_{TARGET}.nmap + sessions/vulns_{TARGET}.nmap
        scan_files: list[str] = []
        open_ports: list[str] = []
        os_from_nmap = ""
        nmap_done = False
        vulns_done = False

        if rhost:
            nmap_scan = LAZYOWN_DIR / "sessions" / f"scan_{rhost}.nmap"
            nmap_xml = LAZYOWN_DIR / "sessions" / f"scan_{rhost}.nmap.xml"
            nmap_vulns = LAZYOWN_DIR / "sessions" / f"vulns_{rhost}.nmap"

            nmap_done = nmap_scan.exists() and nmap_scan.stat().st_size > 100
            vulns_done = nmap_vulns.exists() and nmap_vulns.stat().st_size > 100

            if nmap_done:
                scan_files.append(f"  [OK] scan_{rhost}.nmap   ({nmap_scan.stat().st_size:,} bytes)")
                # Parse open ports + OS hint
                try:
                    for line in nmap_scan.read_text(errors="replace").splitlines():
                        stripped = line.strip()
                        if "/tcp" in stripped and "open" in stripped:
                            open_ports.append(f"      {stripped}")
                        if not os_from_nmap:
                            low = stripped.lower()
                            if "os details:" in low or "running:" in low or "aggressive os guesses:" in low:
                                os_from_nmap = stripped
                            # Banner-based fallback
                            elif (
                                "microsoft" in low
                                or "windows" in low
                                and any(x in low for x in ("smb", "iis", "rdp", "winrm"))
                            ):
                                os_from_nmap = f"Windows (service banner: {stripped[:80]})"
                except Exception:
                    pass

            if vulns_done:
                scan_files.append(f"  [OK] vulns_{rhost}.nmap  ({nmap_vulns.stat().st_size:,} bytes)")
            if nmap_xml.exists() and nmap_xml.stat().st_size > 100:
                scan_files.append(f"  [OK] scan_{rhost}.nmap.xml ({nmap_xml.stat().st_size:,} bytes)")

        # ── 4. OS cross-reference ────────────────────────────────────────────
        os_verdict = os_id_cfg
        os_conflict = ""
        os_evidence = ""
        if os_from_nmap:
            low = os_from_nmap.lower()
            nmap_says_win = "windows" in low or "microsoft" in low
            nmap_says_lnx = "linux" in low or "unix" in low
            if nmap_says_win and os_id_cfg in ("linux", "unknown", ""):
                os_conflict = (
                    f"  [CONFLICT] payload.json os_id='{os_id_cfg}' "
                    f"but nmap suggests Windows → update: "
                    f"lazyown_set_config(key='os_id', value='windows')"
                )
                os_verdict = "windows"
            elif nmap_says_lnx and os_id_cfg in ("windows", "unknown", ""):
                os_conflict = (
                    f"  [CONFLICT] payload.json os_id='{os_id_cfg}' "
                    f"but nmap suggests Linux → update: "
                    f"lazyown_set_config(key='os_id', value='linux')"
                )
                os_verdict = "linux"
            os_evidence = f"  os_nmap : {os_from_nmap[:120]}"

        # ── 5. Pwntomate output evidence ─────────────────────────────────────
        # pwntomate writes to {basedir}/{ip}/{port}/{toolname}/
        # LazyOwn uses sessions/{ip}/ and ~/.pwntomate/{ip}/
        pwntomate_lines: list[str] = []
        if rhost:
            for base in [
                LAZYOWN_DIR / "sessions" / rhost,
                _Path.home() / ".pwntomate" / rhost,
            ]:
                if base.exists() and base.is_dir():
                    for port_dir in sorted(base.iterdir()):
                        if port_dir.is_dir():
                            for tool_dir in sorted(port_dir.iterdir()):
                                if tool_dir.is_dir():
                                    fcount = len(list(tool_dir.rglob("*")))
                                    if fcount:
                                        pwntomate_lines.append(
                                            f"  [OK] {rhost}/{port_dir.name}/{tool_dir.name}/ ({fcount} files)"
                                        )

        # ── 6. Tasks ─────────────────────────────────────────────────────────
        tasks_path = LAZYOWN_DIR / "sessions" / "tasks.json"
        tasks_pending: list[str] = []
        tasks_done: list[str] = []
        try:
            if tasks_path.exists():
                for t in _json.loads(tasks_path.read_text()):
                    s = t.get("status", "New")
                    title = t.get("title", "")[:80]
                    tid = t.get("id", "?")
                    if s in ("Done", "Qa"):
                        tasks_done.append(f"  [#{tid} {s}] {title}")
                    else:
                        tasks_pending.append(f"  [#{tid} {s:8s}] {title}")
        except Exception:
            pass

        # ── 7. Active objectives ─────────────────────────────────────────────
        obj_path = LAZYOWN_DIR / "sessions" / "objectives.jsonl"
        objectives: list[str] = []
        try:
            if obj_path.exists():
                for line in obj_path.read_text().splitlines()[-10:]:
                    try:
                        o = _json.loads(line)
                        if o.get("status") == "pending":
                            objectives.append(f"  [{o.get('priority', 'normal'):8s}] {o.get('text', '')[:80]}")
                    except Exception:
                        pass
        except Exception:
            pass

        # ── 8. Phase commands from bridge catalog ────────────────────────────
        phase_commands: list[str] = []
        kill_chain: list[str] = [
            "recon",
            "enum",
            "exploit",
            "postexp",
            "persist",
            "privesc",
            "cred",
            "lateral",
            "exfil",
            "c2",
            "report",
        ]
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from lazyown_bridge import get_dispatcher as _bd_si

            _disp_si = _bd_si()
            kill_chain = _disp_si.phase_kill_chain()
            for e in _disp_si.list_phase(phase)[:10]:
                svc = ",".join(e.services[:3]) if getattr(e, "services", None) else "any"
                desc = getattr(e, "description", "") or ""
                mit = getattr(e, "mitre_tactic", "") or ""
                phase_commands.append(f"  {e.command:<22} [{mit:<7}] {svc:<14} {desc[:50]}")
        except Exception as _ex_bridge:
            phase_commands = [f"  (bridge unavailable: {_ex_bridge})"]

        # ── 9. What's missing / next steps ──────────────────────────────────
        missing: list[str] = []
        next_steps: list[str] = []

        if not rhost:
            missing.append("  [!] rhost not set in payload.json")
            next_steps.append("  A. lazyown_set_config(key='rhost', value='<target_ip>')")
        else:
            if not nmap_done:
                missing.append(f"  [!] sessions/scan_{rhost}.nmap not found — lazynmap not run yet")
                next_steps.append(f"  A. lazyown_run_command('nmap')   → builds sessions/scan_{rhost}.nmap")
            else:
                if not vulns_done:
                    missing.append(f"  [-] sessions/vulns_{rhost}.nmap not found — vuln scan pending")
                if not pwntomate_lines:
                    missing.append(f"  [-] No pwntomate output for {rhost} — run after nmap finishes")
                    next_steps.append("  B. lazyown_run_command('pyautomate')  → pwntomate from latest XML")
                if os_conflict:
                    next_steps.append(f"  C. {os_conflict.strip()}")

            if tasks_pending:
                next_steps.append(f"  D. {len(tasks_pending)} pending task(s) in tasks.json — review and execute")
            if objectives:
                next_steps.append(f"  E. {len(objectives)} pending objective(s) — lazyown_auto_loop() to execute")

        if not missing:
            missing = ["  [OK] Scan evidence present — proceed to analysis and exploitation"]
            if not next_steps:
                next_steps = [
                    f"  A. lazyown_read_session_file('scan_{rhost}.nmap')    — analyse scan",
                    f"  B. lazyown_discover_commands(phase='{phase}')         — phase commands",
                    "  C. lazyown_facts_show()                               — structured findings",
                    f"  D. lazyown_auto_loop(objective='exploit {rhost}')     — autonomous run",
                ]

        # ── 10. Build output ─────────────────────────────────────────────────
        out = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║   LazyOwn — SITREP (Situation Report)  call once/session    ║",
            "╚══════════════════════════════════════════════════════════════╝",
            "",
            "## ACTIVE CONFIG",
            f"  rhost        : {rhost or '(not set)'}",
            f"  domain       : {domain or '(not set)'}",
            f"  lhost/lport  : {lhost or '?'}:{lport or '?'}",
            f"  os_id(cfg)   : {os_id_cfg}",
        ]
        if os_evidence:
            out.append(os_evidence)
        if os_conflict:
            out.append(os_conflict)
        out.append(f"  os_verdict   : {os_verdict}  (use this for tool selection)")

        out += [
            f"  wm_state     : {wm_host_state}",
            "",
            f"## ENGAGEMENT PHASE: {phase.upper()}",
            f"  Kill chain: {' → '.join(kill_chain)}",
            "",
            "## NMAP SCAN EVIDENCE",
        ]
        out += scan_files or [f"  [--] No nmap files found for '{rhost or 'rhost not set'}'"]

        if open_ports:
            out.append(f"\n  Open ports ({len(open_ports)}):")
            out += open_ports[:20]

        if wm_services:
            out.append(f"\n  World-model services ({len(wm_services)}):")
            out += wm_services[:15]

        out.append("\n## PWNTOMATE OUTPUT")
        out += pwntomate_lines or [f"  [--] No pwntomate output for '{rhost or 'rhost not set'}'"]

        out.append("\n## TASKS (sessions/tasks.json)")
        if tasks_pending:
            out.append("  Pending:")
            out += tasks_pending[:8]
        if tasks_done:
            out.append(f"  Done: {len(tasks_done)} task(s) completed already")
        if not tasks_pending and not tasks_done:
            out.append("  (empty)")

        if wm_creds:
            out.append("\n## CREDENTIALS (world model)")
            out += wm_creds
        if wm_vulns:
            out.append("\n## VULNERABILITIES (world model)")
            out += wm_vulns

        out.append("\n## ACTIVE OBJECTIVES (objectives.jsonl)")
        out += objectives or ["  (none pending)"]

        out += ["", "## WHAT'S MISSING / GAPS"]
        out += missing

        # Build inline phase guide for current phase
        _phase_aliases_si = {
            "recon": "nmap=lazynmap | hosts_discover=sweep | arpscan=arp-scan | ping=OS-detect(TTL)",
            "enum": "ww=whatweb | gobuster=dirbust | ffuf=fuzz | ss=exploit-search | dig=DNS | enum4linux=SMB",
            "exploit": "sqlmap=SQLi | ss=searchsploit+NVD+8src | msf=msf-handler | venom=msfvenom",
            "postexp": "creds=cat-creds | hash=cat-hashes | loot=copy-msf-loot | ssh_cmd=SSH-exec",
            "privesc": "linpeas=linux-enum | winpeas=win-enum | getcap=capabilities | lazypwn=LazyPwn",
            "cred": "secretsdump=dump-hashes | hashcat=GPU-crack | john2hash=john | unshadow=shadow-prep",
            "lateral": "evil=evil-winrm | cme=crackmapexec | psexec=impacket-psexec | bloodhound=AD-graph",
            "exfil": "loot=copy-loot | scp=SCP-transfer | ftpd=python-ftp-server",
            "c2": "cc=open-dashboard | msf=handler | venom=payload | download_c2=implant",
            "report": "report=AI-report | lazyreport=C2-report | man=README",
        }
        out += (
            [
                "",
                "## ABSTRACTION MODEL — never write raw tool commands",
                "  Every LazyOwn command is a high-level abstraction.",
                "  payload.json auto-injects ALL parameters (rhost, domain, wordlist, creds, etc.)",
                "  You only need the command name. Examples:",
                "    lazynmap      → nmap -sC -sV -p- -T4 -Pn --script vuln {rhost}",
                "    ww            → whatweb http://{domain} -a 3",
                "    gobuster      → gobuster dir -u http://{rhost} -w {dirwordlist} -t 30",
                "    evil          → evil-winrm -i {rhost} -u {user} -p {pass}",
                "    bloodhound    → bloodhound-python -d {domain} -u {user} -p {pass} -c All",
                "    dig           → dig @{rhost} {domain} axfr",
                "    secretsdump   → impacket-secretsdump {domain}/{user}:{pass}@{rhost}",
                "    ss <term>     → searchsploit+NVD+ExploitAlert+PacketStorm+MSF+Pompem+creds_py",
                "",
                f"## PHASE ALIASES — {phase.upper()}",
                f"  {_phase_aliases_si.get(phase, '(see lazyown_phase_guide)')}",
                "",
                f"## TOP COMMANDS FOR PHASE: {phase.upper()}",
                f"  {'Command':<24} {'MITRE':<10} {'Creds?':<7} {'Services':<18} Description",
                f"  {'-' * 24} {'-' * 10} {'-' * 7} {'-' * 18} {'-' * 40}",
            ]
            + phase_commands
            + [
                f"  → lazyown_phase_guide(phase='{phase}') for FULL guide with payload keys",
                f"  → lazyown_discover_commands(phase='{phase}') for plain command list",
                "",
                "## RECOMMENDED NEXT STEPS",
            ]
            + (next_steps or [f"  lazyown_phase_guide(phase='{phase}')"])
        )

        # ── Optional recommender embedding ───────────────────────────────────
        recommend_top: list[dict[str, Any]] = []
        if include_recommend:
            recommend_top = _sitrep_recommendations()
            if recommend_top and not any("error" in r for r in recommend_top):
                out.append("\n## TOP-3 RECOMMENDED ACTIONS")
                for i, r in enumerate(recommend_top, 1):
                    out.append(f"  {i}. {r['command']:<24} score={r['score']:.2f} — {(r['reasoning'] or '')[:80]}")

        if out_format == "json":
            sitrep_dict: dict[str, Any] = {
                "config": {
                    "rhost": rhost,
                    "domain": domain,
                    "lhost": lhost,
                    "lport": lport,
                    "os_id": os_id_cfg,
                    "os_verdict": os_verdict,
                },
                "engagement": {
                    "phase": phase,
                    "kill_chain": kill_chain,
                    "host_state": wm_host_state,
                },
                "evidence": {
                    "scan": evidence_freshness(
                        LAZYOWN_DIR / "sessions" / f"scan_{rhost}.nmap",
                        threshold_seconds=freshness_threshold,
                    )
                    if rhost
                    else {},
                    "vulns": evidence_freshness(
                        LAZYOWN_DIR / "sessions" / f"vulns_{rhost}.nmap",
                        threshold_seconds=freshness_threshold,
                    )
                    if rhost
                    else {},
                    "xml": evidence_freshness(
                        LAZYOWN_DIR / "sessions" / f"scan_{rhost}.nmap.xml",
                        threshold_seconds=freshness_threshold,
                    )
                    if rhost
                    else {},
                    "open_ports": [s.strip() for s in open_ports[:50]],
                    "pwntomate": [s.strip() for s in pwntomate_lines],
                },
                "tasks": {
                    "pending_count": len(tasks_pending),
                    "done_count": len(tasks_done),
                    "pending_preview": [s.strip() for s in tasks_pending[:8]],
                },
                "objectives": [s.strip() for s in objectives],
                "world_model": {
                    "services": [s.strip() for s in wm_services],
                    "credentials": [s.strip() for s in wm_creds],
                    "vulnerabilities": [s.strip() for s in wm_vulns],
                },
                "missing": [s.strip() for s in missing],
                "next_steps": [s.strip() for s in next_steps],
                "recommend_top": recommend_top,
            }
            try:
                take_snapshot(
                    SESSIONS_DIR,
                    cfg,
                    locals().get("wm") or {},
                    _json.loads((LAZYOWN_DIR / "sessions" / "tasks.json").read_text())
                    if (LAZYOWN_DIR / "sessions" / "tasks.json").exists()
                    else [],
                )
            except Exception:
                pass
            return text(_json.dumps(sitrep_dict, indent=2, default=str))

        return text("\n".join(out))

    # ── run_command_async ─────────────────────────────────────────────────────
    elif name == "lazyown_run_command_async":
        cmd_async = arguments.get("command", "").strip()
        if not cmd_async:
            return text(json.dumps({"error": "command is required"}))
        timeout_async = int(arguments.get("timeout", 1800))
        if needs_confirmation(name, arguments):
            return text(
                json.dumps(
                    {
                        "error": "confirmation_required",
                        "message": "Re-call with confirm=true for destructive commands.",
                    }
                )
            )
        job_id = _job_store.submit(
            cmd_async,
            runner=_run_lazyown_command,
            timeout=timeout_async,
        )
        return text(
            json.dumps(
                {
                    "job_id": job_id,
                    "command": cmd_async,
                    "timeout": timeout_async,
                    "poll_with": f"lazyown_job_status(job_id='{job_id}')",
                },
                indent=2,
            )
        )

    # ── job_status ────────────────────────────────────────────────────────────
    elif name == "lazyown_job_status":
        jid = (arguments.get("job_id") or "").strip()
        if jid:
            status_rec = _job_store.status(jid)
            if status_rec is None:
                return text(json.dumps({"error": f"unknown job_id: {jid}"}))
            return text(json.dumps(status_rec, indent=2, default=str))
        limit_js = int(arguments.get("limit", 20))
        return text(
            json.dumps(
                {
                    "jobs": _job_store.list(limit=limit_js),
                },
                indent=2,
                default=str,
            )
        )

    # ── recommend_next ────────────────────────────────────────────────────────
    elif name == "lazyown_recommend_next":
        cfg = _load_payload()
        target = cfg.get("rhost", "") or cfg.get("lhost", "127.0.0.1")
        lines: list[str] = []

        # Layer 1 — unified engine: fused policy + recon + graph + kill-chain
        def _fused_recommendations() -> list:
            from cli.recommendation import KIND_CATEGORY
            from cli.recommendation_signals import build_context, build_default_engine

            engine = build_default_engine(payload=cfg)
            ctx = build_context(cfg, target=target, limit=8)
            out: list[str] = []
            recs = engine.recommend(ctx)
            if recs:
                out.append(f"[Engine] Fused next-best actions for {target}:")
                for i, rec in enumerate(recs, 1):
                    bar = "█" * int(min(rec.score, 1.0) * 10)
                    tag = "category" if rec.kind == KIND_CATEGORY else rec.kind
                    out.append(f"  {i}. [{bar:<10}] {rec.action}  [{tag} · {', '.join(rec.sources)}]")
                    for reason in rec.reasons:
                        out.append(f"       {reason}")
                    if rec.command_preview:
                        out.append(f"       $ {rec.command_preview}")
                out.append("")
            return out

        lines.extend(await asyncio.get_event_loop().run_in_executor(None, _fused_recommendations))

        # Layer 2 — LLM recommender: specific commands with arguments
        if _RECOMMENDER_AVAILABLE:
            api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
            llm_recs = await asyncio.get_event_loop().run_in_executor(None, lambda: _recommend(api_key))
            if llm_recs and not (len(llm_recs) == 1 and llm_recs[0].get("command") in ("_error", "_unavailable")):
                via = llm_recs[0].get("_via", "")
                header = "[LLM] Specific commands"
                if via:
                    header += f" (via {via})"
                lines.append(header + ":")
                for i, r in enumerate(llm_recs, 1):
                    bar = "█" * int(r["confidence"] * 10)
                    cmd = r["command"]
                    args = f" {r['args']}" if r.get("args") else ""
                    lines.append(f"  {i}. [{bar:<10}] {r['confidence']:.0%}  {cmd}{args}")
                    lines.append(f"       {r['reason']}")
                lines.append("\nSaved to: sessions/recommendations/next_actions.json")

        if not lines:
            return text("No recommendations available — run bootstrap first or install recommender module.")
        return text("\n".join(lines))

    # ── policy_status ─────────────────────────────────────────────────────────
    elif name == "lazyown_policy_status":
        _ensure_policy()
        if not _POLICY_AVAILABLE or _policy is None:
            return text("Policy engine unavailable. Run: python3 skills/lazyown_policy.py bootstrap")
        cfg = _load_payload()
        target = arguments.get("target") or cfg.get("rhost", "") or "127.0.0.1"
        summary = await asyncio.get_event_loop().run_in_executor(None, lambda: _policy._advisor.episode_summary(target))
        recs = await asyncio.get_event_loop().run_in_executor(None, lambda: _policy.get_recommendations(target))
        lines: list[str] = []
        if summary:
            lines.append(
                f"Episode  target={summary['target']}  "
                f"steps={summary['steps']}  "
                f"total_reward={summary['total_reward']:+d}  "
                f"last_state={summary['last_state']}"
            )
        else:
            lines.append(f"No episode data for {target}. Run bootstrap or execute commands first.")
        lines.append("\nRecommendations:")
        for i, r in enumerate(recs, 1):
            bar = "█" * int(r["confidence"] * 10)
            lines.append(f"  {i}. [{bar:<10}] {r['confidence']:.0%}  category={r['category']}  [{r['source']}]")
            lines.append(f"       {r['reason']}")
        return text("\n".join(lines))

    elif name == "lazyown_playbook_run":
        pb_path = arguments.get("path", "").strip()
        pb_target = arguments.get("target", "").strip()
        pb_dry_run = bool(arguments.get("dry_run", False))
        try:
            sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
            from playbook_engine import PlaybookEngine

            engine = PlaybookEngine()

            # Resolve playbook path
            PLAYS_DIRECTORY = LAZYOWN_DIR / "playbooks"
            if pb_path:
                pb_file = Path(pb_path)
                if not pb_file.exists() and PLAYS_DIRECTORY.is_dir():
                    alt = PLAYS_DIRECTORY / pb_file.name
                    if alt.exists():
                        pb_file = alt
            else:
                sessions_pb = sorted(
                    list((LAZYOWN_DIR / "sessions").glob("playbook_*.yaml")) + list(PLAYS_DIRECTORY.glob("apt_*.yaml")),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True,
                )
                if not sessions_pb:
                    return text("[playbook_run] No playbook found. Run lazyown_playbook_generate first.")
                pb_file = sessions_pb[0]

            playbook = await asyncio.get_event_loop().run_in_executor(None, lambda: engine.load(pb_file))

            # Resolve target
            effective_target = pb_target or playbook.target
            if not effective_target:
                cfg = _load_payload()
                effective_target = cfg.get("rhost", "") or cfg.get("target_ip", "")

            # Executor: runs each step command via subprocess
            # Signature: (command, target) matching PlaybookEngine.execute() contract
            def _mcp_executor(command: str, target: str = "") -> str:
                import subprocess

                cmd = substitute_playbook_target(command, target)
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

    # ── create_tool ───────────────────────────────────────────────────────────
    elif name == "lazyown_create_tool":
        toolname = arguments["toolname"]
        command = arguments["command"]
        trigger = arguments["trigger"]
        active = bool(arguments.get("active", True))
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

    # ── search_tools (deferred tool discovery) ───────────────────────────────
    if name == "lazyown_search_tools":
        query = arguments.get("query", "").lower().strip()
        limit = int(arguments.get("limit", 15))
        if not query:
            return text("Provide a 'query' keyword to search tools.")
        # Gather all tool definitions from list_tools
        try:
            all_tools = await list_tools()
        except Exception as e:
            return text(f"[search_tools error] {e}")
        matches = [t for t in all_tools if query in t.name.lower() or query in (t.description or "").lower()]
        if not matches:
            return text(f"No tools found matching '{query}'.")
        lines = [f"Found {len(matches)} tool(s) matching '{query}':"]
        for t in matches[:limit]:
            req = []
            try:
                req = t.inputSchema.get("required", [])
            except Exception:
                pass
            lines.append(f"\n  {t.name}")
            lines.append(f"    {(t.description or '').splitlines()[0][:90]}")
            if req:
                lines.append(f"    required: {', '.join(req)}")
        return text("\n".join(lines))

    # ── manage_permissions ────────────────────────────────────────────────────
    if name == "lazyown_manage_permissions":
        action = arguments.get("action", "status")
        perm_sys = _get_perm_system()
        if perm_sys is None:
            return text("Permission system unavailable (lazyown_permissions.py not found).")

        if action == "status":
            return text(perm_sys.status_text())

        if action == "set_mode":
            mode = arguments.get("mode", "")
            if not mode:
                return text("'mode' parameter required for set_mode action.")
            try:
                return text(perm_sys.set_mode(mode))
            except ValueError as e:
                return text(
                    f"Invalid mode: {e}\nValid: plan | default | accept_edits | auto | dont_ask | bypass_permissions"
                )

        if action == "add_rule":
            tp = arguments.get("tool_pattern", "")
            ra = arguments.get("rule_action", "")
            if not tp or not ra:
                return text("'tool_pattern' and 'rule_action' required for add_rule.")
            result = perm_sys.add_rule(
                tool_pattern=tp,
                action=ra,
                condition=arguments.get("condition"),
                description=arguments.get("description", ""),
            )
            return text(result)

        if action == "remove_rule":
            tp = arguments.get("tool_pattern", "")
            ra = arguments.get("rule_action", "")
            if not tp or not ra:
                return text("'tool_pattern' and 'rule_action' required for remove_rule.")
            return text(perm_sys.remove_rule(tp, ra))

        if action == "list_rules":
            rules = perm_sys.list_rules()
            if not rules:
                return text("No rules configured.")
            return text(json.dumps(rules, indent=2))

        return text(f"Unknown action: {action}")

    # ── harness_status (defense-in-depth dashboard) ──────────────────────────
    if name == "lazyown_harness_status":
        lines = ["═══ LazyOwn Harness Status (Defense-in-Depth Dashboard) ═══", ""]

        # Layer 1: Permissions
        ps = _get_perm_system()
        if ps is not None:
            m = ps.metrics()
            lines += [
                "▼ PERMISSIONS",
                f"  mode:               {m['mode']}",
                f"  rules configured:   {m['rules_count']}",
                f"  total evaluations:  {m['total_evaluations']}",
                f"  decisions:          allow={m['decisions']['allow']}  deny={m['decisions']['deny']}  ask={m['decisions']['ask']}",
            ]
            if m["recent_denials"]:
                lines.append("  recent denials:")
                for d in m["recent_denials"]:
                    lines.append(f"    [{d['ts'][-8:]}] {d['tool']}  →  {d['reason'][:60]}")
            lines.append("")
        else:
            lines += ["▼ PERMISSIONS", "  unavailable (lazyown_permissions not loaded)", ""]

        # Layer 2: Hooks
        hk = _get_hooks()
        if hk is not None:
            m = hk.metrics()
            lines += [
                "▼ HOOKS",
                f"  events registered:  {len(m['events_registered'])}  ({', '.join(m['events_registered'])})",
                f"  totals:             runs={m['totals']['runs']}  blocks={m['totals']['blocks']}  errors={m['totals']['errors']}",
            ]
            for ev, stats in m["per_event"].items():
                if stats["runs"] > 0:
                    lines.append(
                        f"    {ev:20s} runs={stats['runs']:4d}  blocks={stats['blocks']:3d}  errors={stats['errors']:3d}"
                    )
            lines.append("")
        else:
            lines += ["▼ HOOKS", "  unavailable (lazyown_hooks not loaded)", ""]

        # Layer 3: Session transcript
        ts = _get_transcript()
        if ts is not None:
            events = ts.get_recent(500)
            tool_uses = sum(1 for e in events if e.get("type") == "tool_use")
            results = sum(1 for e in events if e.get("type") == "tool_result")
            boundaries = sum(1 for e in events if e.get("type") == "compact_boundary")
            denied = sum(
                1
                for e in events
                if e.get("type") == "permission_decision" and e.get("data", {}).get("decision") == "deny"
            )
            lines += [
                "▼ SESSION TRANSCRIPT",
                f"  session_id:         {ts.session_id}",
                f"  total events:       {ts.count()}",
                f"  tool calls:         {tool_uses}",
                f"  tool results:       {results}",
                f"  compact boundaries: {boundaries}",
                f"  denied calls:       {denied}",
                f"  file:               {ts.path.name}",
                "",
            ]
        else:
            lines += ["▼ SESSION TRANSCRIPT", "  unavailable (lazyown_session not loaded)", ""]

        # Layer 4: CLAUDE.md hierarchy
        cmd_loader = _get_claudemd()
        if cmd_loader is not None:
            files = cmd_loader.list_files()
            lines += ["▼ CLAUDE.md HIERARCHY"]
            if files:
                for f in files:
                    lines.append(f"  [{f['level']:8s}] {f['path']}  ({f['size']:,} bytes)")
            else:
                lines.append("  no CLAUDE.md files found in hierarchy")
            lines.append("")
        else:
            lines += ["▼ CLAUDE.md HIERARCHY", "  unavailable", ""]

        # Layer 5: Compaction (best-effort metrics — last result if any)
        lines += [
            "▼ CONTEXT COMPACTION",
            "  status: active (5-layer pipeline applied to every tool result)",
            "  layers: microcompact → snip → collapse → budget",
            "",
        ]

        return text("\n".join(lines))

    # ── session_resume ────────────────────────────────────────────────────────
    if name == "lazyown_session_resume":
        sid = arguments.get("session_id", "").strip()
        limit = int(arguments.get("limit", 50))

        try:
            from lazyown_session import SessionTranscript
        except ImportError:
            return text("lazyown_session module not available.")

        if sid:
            ts_obj = SessionTranscript(SESSIONS_DIR, sid)
        else:
            ts_obj = _get_transcript()
            if ts_obj is None:
                return text("No active transcript and no session_id provided.")

        events = ts_obj.get_recent(limit)
        if not events:
            return text(f"Session {ts_obj.session_id}: no events found.")

        # Aggregate
        tool_calls: list[str] = []
        tool_results: list[str] = []
        denials: list[str] = []
        boundaries: list[str] = []
        for e in events:
            t = e.get("type", "")
            d = e.get("data", {})
            ts_str = e.get("ts", "")[-8:]
            if t == "tool_use":
                tool = d.get("tool_name", "?")
                args_str = str(d.get("arguments", {}))[:60]
                tool_calls.append(f"  [{ts_str}] {tool}  {args_str}")
            elif t == "tool_result":
                tool = d.get("tool_name", "?")
                preview = (d.get("content", "") or "")[:80].replace("\n", " ")
                tool_results.append(f"  [{ts_str}] {tool}  →  {preview}")
            elif t == "compact_boundary":
                summary = d.get("summary", "")[:80]
                boundaries.append(f"  [{ts_str}] {summary}")
            elif t == "permission_decision":
                if d.get("decision") == "deny":
                    denials.append(f"  [{ts_str}] {d.get('tool_name', '?')} → {d.get('reason', '')[:60]}")

        lines = [
            f"═══ Session Resume: {ts_obj.session_id} ═══",
            f"  total events: {ts_obj.count()}  (showing last {len(events)})",
            f"  transcript:   {ts_obj.path}",
            "",
            f"▼ Tool calls ({len(tool_calls)}):",
            *tool_calls[-10:],
            "",
            f"▼ Tool results ({len(tool_results)}):",
            *tool_results[-10:],
        ]
        if boundaries:
            lines += ["", f"▼ Compact boundaries ({len(boundaries)}):", *boundaries[-3:]]
        if denials:
            lines += ["", f"▼ Permission denials ({len(denials)}):", *denials[-5:]]
        lines += ["", "Use lazyown_run_command or lazyown_subagent_run to continue from this state."]
        return text("\n".join(lines))

    # ── subagent_run (isolated sidechain transcript) ─────────────────────────
    if name == "lazyown_subagent_run":
        goal = arguments.get("goal", "").strip()
        backend = arguments.get("backend", "groq")
        max_iter = int(arguments.get("max_iterations", 5))
        if not goal:
            return text("'goal' parameter is required.")

        if not _ensure_bridge():
            return text("Agent bridge not available — check modules/mcp_agent_bridge.py")

        # 1. Fork transcript → sidechain (no permission inheritance)
        parent = _get_transcript()
        try:
            from lazyown_session import SessionTranscript

            sidechain = SessionTranscript(SESSIONS_DIR)  # fresh session_id
            sidechain.append(
                "subagent_init",
                {
                    "goal": goal,
                    "backend": backend,
                    "parent_session": parent.session_id if parent else None,
                },
            )
        except Exception as exc:
            return text(f"Failed to create sidechain transcript: {exc}")

        # 2. Log spawn event in PARENT transcript
        if parent is not None:
            parent.append(
                "subagent_spawned",
                {
                    "goal": goal,
                    "sidechain_session": sidechain.session_id,
                },
            )

        # 3. Wrap _runner so subagent's tool calls write to SIDECHAIN, not parent
        def _isolated_runner(cmd: str) -> str:
            sidechain.append("tool_use", {"tool_name": "shell", "arguments": {"command": cmd}})
            try:
                output = _run_lazyown_command(cmd, timeout=60)
            except Exception as exc:
                output = f"[runner error] {exc}"
            sidechain.append("tool_result", {"tool_name": "shell", "content": output[:800]})
            return output

        # 4. Inject Groq API key if needed
        if backend == "groq" and not os.environ.get("GROQ_API_KEY"):
            cfg = _load_payload()
            key = cfg.get("api_key", "")
            if key:
                os.environ["GROQ_API_KEY"] = key

        # 5. Spawn the subagent
        try:
            agent_id = await asyncio.get_event_loop().run_in_executor(
                None, lambda: start_agent(goal, backend, _isolated_runner, max_iter)
            )
        except Exception as exc:
            sidechain.append("subagent_error", {"error": str(exc)})
            return text(f"Subagent failed to start: {exc}")

        # 6. Return ONLY summary to parent context (no full history inflation)
        sidechain.append("subagent_started", {"agent_id": agent_id})
        return text(
            f"## Subagent Spawned (Isolated Sidechain)\n"
            f"  agent_id:           {agent_id}\n"
            f"  goal:               {goal}\n"
            f"  backend:            {backend} (max {max_iter} steps)\n"
            f"  sidechain session:  {sidechain.session_id}\n"
            f"  sidechain file:     {sidechain.path}\n"
            f"  parent session:     {parent.session_id if parent else '(none)'}\n\n"
            f"Permissions are NOT inherited from parent (security isolation).\n"
            f"Tool calls log to sidechain only — parent context stays clean.\n\n"
            f"Track progress: lazyown_agent_status('{agent_id}')\n"
            f"Get final result: lazyown_agent_result('{agent_id}')\n"
            f"Resume sidechain: lazyown_session_resume('{sidechain.session_id}')"
        )

    # ── claudemd ──────────────────────────────────────────────────────────────
    if name == "lazyown_claudemd":
        action = arguments.get("action", "status")
        loader = _get_claudemd()
        if loader is None:
            return text("ClaudeMdLoader unavailable (lazyown_claudemd.py not found).")

        if action == "status":
            return text(loader.status_text())

        if action == "load":
            merged = loader.load()
            if not merged:
                return text("No CLAUDE.md files found in hierarchy.")
            return text(merged)

        if action == "create_user":
            content = arguments.get("content", "")
            if not content:
                return text("'content' parameter required.")
            return text(loader.create_user_file(content))

        if action == "create_project":
            content = arguments.get("content", "")
            if not content:
                return text("'content' parameter required.")
            return text(loader.create_project_file(content, local=False))

        if action == "create_local":
            content = arguments.get("content", "")
            if not content:
                return text("'content' parameter required.")
            return text(loader.create_project_file(content, local=True))

        if action == "add_rule":
            rule_name = arguments.get("rule_name", "").strip()
            content = arguments.get("content", "")
            if not rule_name or not content:
                return text("'rule_name' and 'content' required for add_rule.")
            return text(loader.add_rule(rule_name, content))

        return text(f"Unknown action: {action}")

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
