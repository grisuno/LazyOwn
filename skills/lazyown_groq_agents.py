#!/usr/bin/env python3
"""
skills/lazyown_groq_agents.py
==============================
Translates LazyOwn MCP tools into Groq-native tool-calling format and provides
a multi-agent pool for parallel autonomous operation.

Three layers:
  GroqToolRegistry  -- 18 LazyOwn-aware sync callables with Groq-compatible schemas
  GroqAgentPool     -- thread pool that runs LLMBridge agents concurrently
  Public API        -- spawn_agent / agent_status / agent_result / list_agents

Each agent has access to: run_command, bridge_suggest, bridge_catalog,
parquet_context, facts_show, cve_lookup, memory_search, session_status,
read_session_file, list_sessions, c2_status, c2_command, task_list, task_add,
inject_objective, reactive_suggest, searchsploit, command_help.

Usage from MCP:
  lazyown_groq_agent(goal="Enumerate AD on 10.10.11.78")
  lazyown_groq_agent(goal="Kerberoast and crack hashes", backend="groq", async_mode=True)

Usage standalone:
  python3 skills/lazyown_groq_agents.py spawn "Enumerate SMB on 10.0.0.5" --wait
  python3 skills/lazyown_groq_agents.py tools
  python3 skills/lazyown_groq_agents.py list
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# ── Paths ─────────────────────────────────────────────────────────────────────

SKILLS_DIR   = Path(__file__).parent
LAZYOWN_DIR  = SKILLS_DIR.parent
SESSIONS_DIR = LAZYOWN_DIR / "sessions"
PAYLOAD_FILE = LAZYOWN_DIR / "payload.json"

sys.path.insert(0, str(SKILLS_DIR))
sys.path.insert(0, str(LAZYOWN_DIR / "modules"))

# ── Lazy imports (avoid circular dependency with lazyown_mcp.py) ──────────────

def _load_payload() -> dict:
    try:
        return json.loads(PAYLOAD_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _run_cmd(command: str, timeout: int = 60) -> str:
    """Execute a LazyOwn shell command via the MCP helper (lazy import)."""
    try:
        from lazyown_mcp import _run_lazyown_command  # noqa: PLC0415
        return _run_lazyown_command(command, timeout)
    except ImportError:
        result = subprocess.run(
            [sys.executable, "-W", "ignore", str(LAZYOWN_DIR / "lazyown.py")],
            input=f"{command}\nexit\n",
            capture_output=True, text=True,
            timeout=timeout, cwd=str(LAZYOWN_DIR),
        )
        return (result.stdout + result.stderr).strip()


def _c2_req(path: str, method: str = "GET", body: Optional[dict] = None) -> dict:
    """Forward a request to the LazyOwn C2 REST API (lazy import)."""
    try:
        from lazyown_mcp import _c2_request  # noqa: PLC0415
        return _c2_request(path, method=method, body=body)
    except ImportError:
        return {"error": "C2 request unavailable — lazyown_mcp not importable"}


# ── Tool implementations (sync, Groq-callable) ────────────────────────────────

def _t_run_command(command: str) -> str:
    return _run_cmd(command, timeout=60)


def _t_bridge_suggest(
    phase: str,
    services: str = "",
    tag: str = "",
    os_hint: str = "any",
) -> str:
    try:
        from lazyown_bridge import get_dispatcher  # noqa: PLC0415
        svc_list = [s.strip() for s in services.split(",") if s.strip()]
        result = get_dispatcher().suggest(
            phase=phase, services=svc_list, tag_hint=tag, os_hint=os_hint,
        )
        if result is None:
            return f"No command found for phase={phase} services={svc_list} tag={tag}"
        cmd_str, entry = result
        return (
            f"Suggested: {cmd_str}\n"
            f"MITRE:     {entry.mitre_tactic}\n"
            f"Desc:      {entry.description}"
        )
    except Exception as exc:
        return f"[bridge_suggest error] {exc}"


def _t_bridge_catalog() -> str:
    try:
        from lazyown_bridge import get_dispatcher  # noqa: PLC0415
        d = get_dispatcher()
        lines = [f"Bridge catalog — {d.catalog_count()} commands", ""]
        for phase, cmds in d.catalog_summary().items():
            lines.append(
                f"  {phase:12s}: {', '.join(cmds[:7])}"
                + (" ..." if len(cmds) > 7 else "")
            )
        return "\n".join(lines)
    except Exception as exc:
        return f"[bridge_catalog error] {exc}"


def _t_parquet_context(phase: str, target: str = "") -> str:
    try:
        from lazyown_parquet_db import get_pdb  # noqa: PLC0415
        pdb = get_pdb()
        if pdb is None:
            return "ParquetDB unavailable."
        # context_for_phase returns a rich dict; fall back to query_session if unavailable
        if hasattr(pdb, "context_for_phase"):
            ctx = pdb.context_for_phase(phase, target or None)
            if not ctx:
                return f"No session data for phase={phase}."
            lines = [f"Phase: {phase}"]
            for k, v in ctx.items():
                lines.append(f"  {k}: {str(v)[:120]}")
            return "\n".join(lines)
        rows = pdb.query_session(phase=phase, target=target or None, limit=10)
        if not rows:
            return f"No session data for phase={phase}."
        lines = [f"Phase: {phase} — {len(rows)} record(s)"]
        for r in rows[:5]:
            lines.append(f"  {r.get('command', '?'):30s} -> {r.get('outcome', '?')}")
        return "\n".join(lines)
    except Exception as exc:
        return f"[parquet_context error] {exc}"


def _t_facts_show(target: str = "") -> str:
    try:
        from lazyown_facts import FactStore  # noqa: PLC0415
        return FactStore().summary(target or None) or "No facts found."
    except Exception as exc:
        return f"[facts_show error] {exc}"


def _t_cve_lookup(product: str, version: str = "") -> str:
    try:
        import urllib.request  # noqa: PLC0415
        keyword = f"{product} {version}".strip().replace(" ", "+")
        url = (
            f"https://services.nvd.nist.gov/rest/json/cves/2.0"
            f"?keywordSearch={keyword}&resultsPerPage=5"
        )
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
        items = data.get("vulnerabilities", [])
        if not items:
            return f"No CVEs found for '{product} {version}'."
        lines = []
        for item in items[:5]:
            cve = item.get("cve", {})
            desc = cve.get("descriptions", [{}])[0].get("value", "")[:120]
            lines.append(f"{cve.get('id','?')}: {desc}")
        return "\n".join(lines)
    except Exception as exc:
        return f"[cve_lookup error] {exc}"


def _t_memory_search(query: str) -> str:
    try:
        from lazyown_parquet_db import get_pdb  # noqa: PLC0415
        pdb = get_pdb()
        if pdb is None:
            return "Memory unavailable."
        # query_session has no keyword param — use query_knowledge for text search
        if hasattr(pdb, "query_knowledge"):
            rows = pdb.query_knowledge(keyword=query, limit=5)
        else:
            rows = pdb.query_session(limit=20)
            q_low = query.lower()
            rows = [r for r in rows
                    if q_low in str(r.get("command", "")).lower()
                    or q_low in str(r.get("outcome", "")).lower()][:5]
        if not rows:
            return f"No memory matches for '{query}'."
        return "\n".join(
            f"[{r.get('phase', r.get('category','?'))}] "
            f"{str(r.get('command','?'))[:30]} -> {r.get('outcome','?')}"
            for r in rows
        )
    except Exception as exc:
        return f"[memory_search error] {exc}"


def _t_session_status() -> str:
    try:
        from session_reader import get_aggregator  # noqa: PLC0415
        summary = get_aggregator().aggregate(SESSIONS_DIR)
        lines = [f"Active implants: {len(summary.active_client_ids)}"]
        for cid in summary.active_client_ids[:10]:
            rec = summary.latest_for(cid)
            if rec:
                priv = "PRIVILEGED" if rec.is_privileged else "user"
                lines.append(
                    f"  [{priv}] {cid} | {rec.hostname} | "
                    f"{rec.platform} | user={rec.user}"
                )
        if summary.discovered_hosts:
            lines.append(
                f"Discovered hosts: {', '.join(summary.discovered_hosts[:15])}"
            )
        if summary.tasks:
            pending = [t for t in summary.tasks if t.status not in ("Done", "Blocked")]
            lines.append(f"Pending tasks: {len(pending)}")
        return "\n".join(lines) if lines else "No active sessions."
    except Exception as exc:
        return f"[session_status error] {exc}"


def _t_read_session_file(filename: str) -> str:
    try:
        p = SESSIONS_DIR / filename
        if not p.exists():
            return f"Not found: sessions/{filename}"
        return p.read_text(encoding="utf-8", errors="replace")[:3000]
    except Exception as exc:
        return f"[read_session_file error] {exc}"


def _t_list_sessions() -> str:
    try:
        entries = sorted(SESSIONS_DIR.iterdir())
        return "\n".join(e.name for e in entries[:60]) or "sessions/ is empty."
    except Exception as exc:
        return f"[list_sessions error] {exc}"


def _t_c2_status() -> str:
    data = _c2_req("/api/status")
    return json.dumps(data, indent=2)[:1000]


def _t_c2_command(client_id: str, command: str) -> str:
    data = _c2_req("/api/command", method="POST",
                   body={"client_id": client_id, "command": command})
    return json.dumps(data, indent=2)[:1000]


def _t_task_list(filter_status: str = "") -> str:
    try:
        from session_reader import TaskReader  # noqa: PLC0415
        tasks = TaskReader().read(SESSIONS_DIR)
        if filter_status:
            tasks = [t for t in tasks if t.status.lower() == filter_status.lower()]
        if not tasks:
            return "No tasks found."
        return "\n".join(
            f"#{t.id:3d} [{t.status:8s}] {t.title} (op={t.operator})"
            for t in tasks
        )
    except Exception as exc:
        return f"[task_list error] {exc}"


def _t_task_add(title: str, description: str = "") -> str:
    try:
        from session_reader import TaskWriter  # noqa: PLC0415
        task = TaskWriter(SESSIONS_DIR).append(
            title=title, description=description, operator="groq_agent",
        )
        return f"Task #{task.id} created: [{task.status}] {task.title}"
    except Exception as exc:
        return f"[task_add error] {exc}"


def _t_inject_objective(title: str, description: str = "") -> str:
    try:
        from lazyown_objective import ObjectiveStore  # noqa: PLC0415
        store = ObjectiveStore()
        # inject(text, priority, source, notes) — title maps to text, description to notes
        text = f"{title}: {description}".strip(": ") if description else title
        obj = store.inject(text=text, source="groq_agent", notes=description)
        return f"Objective injected: [{obj.id}] {obj.text[:80]}"
    except Exception as exc:
        return f"[inject_objective error] {exc}"


def _t_reactive_suggest(
    output: str,
    command: str = "",
    platform: str = "unknown",
) -> str:
    try:
        from reactive_engine import get_engine  # noqa: PLC0415
        decisions = get_engine().analyse(
            output=output, command=command, platform=platform,
        )
        if not decisions:
            return "No reactive signals detected."
        lines = []
        for d in decisions[:5]:
            lines.append(
                f"[{d.action:16s}] priority={d.priority}  "
                f"cmd={d.command}  ({d.reason})"
            )
        return "\n".join(lines)
    except Exception as exc:
        return f"[reactive_suggest error] {exc}"


def _t_searchsploit(query: str) -> str:
    try:
        result = subprocess.run(
            ["searchsploit", "--json", query],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return result.stderr.strip() or f"searchsploit returned no output for '{query}'."
        data = json.loads(result.stdout)
        exploits = data.get("RESULTS_EXPLOIT", [])[:5]
        if not exploits:
            return f"No exploits found for '{query}'."
        return "\n".join(
            f"{e.get('EDB-ID','?'):7s}: {e.get('Title','?')}" for e in exploits
        )
    except FileNotFoundError:
        return "searchsploit not installed."
    except Exception as exc:
        return f"[searchsploit error] {exc}"


def _t_command_help(command: str) -> str:
    return _run_cmd(f"help {command}", timeout=15)


def _t_rag_query(query: str, n: int = 5) -> str:
    """Semantic search over indexed sessions/ artefacts."""
    try:
        sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
        from session_rag import get_rag as _get_rag
        _rag = _get_rag()
        _rag.index_new()
        hits = _rag.query(query, int(n))
        if not hits:
            return "No results. The RAG index may be empty — run lazyown_rag_index first."
        lines = []
        for i, h in enumerate(hits, 1):
            score_str = f"  score={h['score']:.3f}" if h["score"] is not None else ""
            lines.append(f"{i}. [{h['source']}]{score_str}")
            lines.append(h["text"].strip()[:300])
        return "\n".join(lines)
    except Exception as exc:
        return f"[rag_query error] {exc}"


def _t_threat_model(action: str = "build") -> str:
    """Build or load the blue team threat model."""
    try:
        sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
        from threat_model import get_builder as _get_tmb
        _tmb = _get_tmb()
        if action == "load":
            model = _tmb.load()
            if model is None:
                return "No threat model found — run with action='build'."
        else:
            model = _tmb.build()
        s = model.get("summary", {})
        return (
            f"Threat Model: {len(model.get('ttps',[]))} TTPs, "
            f"{len(model.get('ioc_registry',[]))} IOCs, "
            f"{len(model.get('detection_rules',[]))} rules, "
            f"{len(model.get('assets',[]))} assets\n"
            f"Highest risk: {s.get('highest_risk_asset','')}  "
            f"Dominant tactic: {s.get('dominant_tactic','')}\n"
            f"Saved: sessions/reports/threat_model.json"
        )
    except Exception as exc:
        return f"[threat_model error] {exc}"


def _t_atomic_search(
    keyword: str = "",
    mitre_id: str = "",
    platform: str = "",
    scope: str = "",
    complexity: str = "",
    has_prereqs: str = "",
    limit: int = 8,
    include_command: bool = False,
) -> str:
    """Structured search over 1690 Atomic Red Team technique tests."""
    try:
        sys.path.insert(0, str(LAZYOWN_DIR / "modules"))
        from atomic_enricher import query_atomic as _qa, enrich as _enrich
        _enrich()
        prereqs: Optional[bool] = None
        if str(has_prereqs).lower() in ("true", "1", "yes"):
            prereqs = True
        elif str(has_prereqs).lower() in ("false", "0", "no"):
            prereqs = False
        rows = _qa(
            keyword=keyword, mitre_id=mitre_id, platform=platform,
            scope=scope, complexity=complexity, has_prereqs=prereqs,
            limit=int(limit), include_command=bool(include_command),
        )
        if not rows:
            return f"No results for filters: keyword={keyword!r} mitre={mitre_id!r} platform={platform!r}"
        lines = [f"{len(rows)} Atomic techniques found:"]
        for r in rows:
            lines.append(
                f"  {r['mitre_id']:12s} [{r['complexity']:6s}] {r['name']}"
            )
            lines.append(f"    platforms: {', '.join(r['platform_list'])}  prereqs: {r['has_prereqs']}")
            if include_command and r.get("command_preview"):
                lines.append(f"    cmd: {r['command_preview'][:100]}")
        return "\n".join(lines)
    except Exception as exc:
        return f"[atomic_search error] {exc}"


# ── Tool registry ─────────────────────────────────────────────────────────────
# Each entry: (description, groq_parameters_schema, callable)

REGISTRY: Dict[str, tuple[str, Dict[str, Any], Callable]] = {
    "run_command": (
        "Execute any LazyOwn shell command and return its output. "
        "Examples: 'lazynmap', 'set rhost 10.0.0.1', 'linpeas', 'adversary_yaml amsi'.",
        {"command": {"type": "string",
                     "description": "LazyOwn command with arguments"}},
        _t_run_command,
    ),
    "bridge_suggest": (
        "Get the best LazyOwn command for a kill-chain phase. "
        "Phases: recon, enum, exploit, postexp, cred, lateral, privesc, persist, exfil, c2, report.",
        {
            "phase":    {"type": "string",
                         "description": "Kill-chain phase"},
            "services": {"type": "string",
                         "description": "Comma-separated detected services (smb,ldap,http)"},
            "tag":      {"type": "string",
                         "description": "Technique tag: kerberos, ad, web, smb, etc."},
            "os_hint":  {"type": "string",
                         "description": "linux, windows, or any"},
        },
        _t_bridge_suggest,
    ),
    "bridge_catalog": (
        "Show the full LazyOwn command catalog summary (347 commands, 11 phases).",
        {},
        _t_bridge_catalog,
    ),
    "parquet_context": (
        "Get phase-aware context from the knowledge base: "
        "past command successes, GTFOBins, LOLBas, ATT&CK techniques.",
        {
            "phase":  {"type": "string",
                       "description": "Attack phase (recon, enum, exploit, privesc, cred, lateral...)"},
            "target": {"type": "string",
                       "description": "Target IP (optional)"},
        },
        _t_parquet_context,
    ),
    "facts_show": (
        "Show structured facts from nmap scans and tool output: "
        "open ports, services, credentials, shares, access level.",
        {"target": {"type": "string",
                    "description": "Target IP (empty string = all targets)"}},
        _t_facts_show,
    ),
    "cve_lookup": (
        "Search NVD for CVEs matching a product name and optional version.",
        {
            "product": {"type": "string",
                        "description": "Product name (e.g. 'Apache', 'OpenSSH')"},
            "version": {"type": "string",
                        "description": "Version string (e.g. '2.4.49')"},
        },
        _t_cve_lookup,
    ),
    "memory_search": (
        "Search episodic memory for past command executions relevant to a keyword.",
        {"query": {"type": "string",
                   "description": "Search keyword or phrase"}},
        _t_memory_search,
    ),
    "session_status": (
        "Show live C2 implant state: OS, user, hostname, IPs, "
        "privileged/unprivileged, discovered hosts, pending tasks.",
        {},
        _t_session_status,
    ),
    "read_session_file": (
        "Read a file from the sessions/ directory.",
        {"filename": {"type": "string",
                      "description": "Filename relative to sessions/ (e.g. 'hostsdiscovery.txt')"}},
        _t_read_session_file,
    ),
    "list_sessions": (
        "List all files and directories in sessions/.",
        {},
        _t_list_sessions,
    ),
    "c2_status": (
        "Check C2 server health and return dashboard data.",
        {},
        _t_c2_status,
    ),
    "c2_command": (
        "Send a command to a specific C2 beacon/implant.",
        {
            "client_id": {"type": "string",
                          "description": "Beacon client ID"},
            "command":   {"type": "string",
                          "description": "Command: whoami, softenum, exfil, etc."},
        },
        _t_c2_command,
    ),
    "task_list": (
        "List campaign tasks from sessions/tasks.json.",
        {"filter_status": {"type": "string",
                           "description": "Status filter: New, Refined, Started, "
                                          "Review, Qa, Done, Blocked (empty = all)"}},
        _t_task_list,
    ),
    "task_add": (
        "Create a new campaign task in sessions/tasks.json.",
        {
            "title":       {"type": "string",
                            "description": "Task title"},
            "description": {"type": "string",
                            "description": "Task description"},
        },
        _t_task_add,
    ),
    "inject_objective": (
        "Inject a high-level attack objective into the objective queue.",
        {
            "title":       {"type": "string",
                            "description": "Objective title"},
            "description": {"type": "string",
                            "description": "Detailed description"},
        },
        _t_inject_objective,
    ),
    "reactive_suggest": (
        "Analyse raw command output and return prioritised reactive decisions: "
        "AV/EDR evasion, privesc hints, credential extraction, new host discovery.",
        {
            "output":   {"type": "string",
                         "description": "Raw command output to analyse"},
            "command":  {"type": "string",
                         "description": "The command that produced the output"},
            "platform": {"type": "string",
                         "description": "Target platform: linux, windows, or unknown"},
        },
        _t_reactive_suggest,
    ),
    "searchsploit": (
        "Search public exploits by CVE ID or service/version string.",
        {"query": {"type": "string",
                   "description": "CVE ID or product/version (e.g. 'Apache 2.4.49')"}},
        _t_searchsploit,
    ),
    "command_help": (
        "Get full documentation for any LazyOwn command.",
        {"command": {"type": "string",
                     "description": "LazyOwn command name"}},
        _t_command_help,
    ),
    "rag_query": (
        "Semantic search over indexed sessions/ artefacts (logs, scans, credentials, etc.). "
        "Falls back to keyword search when ChromaDB is not installed.",
        {
            "query": {"type": "string",
                      "description": "Natural language search query"},
            "n":     {"type": "integer",
                      "description": "Number of results (default 5)"},
        },
        _t_rag_query,
    ),
    "threat_model": (
        "Build or load the blue team threat model: assets with risk scores, "
        "MITRE ATT&CK TTPs, IOC registry, and Sigma-lite detection rules. "
        "action: 'build' (default) or 'load'.",
        {"action": {"type": "string",
                    "description": "build or load"}},
        _t_threat_model,
    ),
    "atomic_search": (
        "Search 1690 Atomic Red Team technique tests by keyword, MITRE ID/prefix, "
        "platform (linux/windows/macos), scope (local/remote), complexity (low/medium/high), "
        "or prerequisite availability. Returns name, mitre_id, platform, complexity, tags.",
        {
            "keyword":         {"type": "string",  "description": "Free-text search"},
            "mitre_id":        {"type": "string",  "description": "MITRE ID or prefix (T1059, T1548.002)"},
            "platform":        {"type": "string",  "description": "linux | windows | macos | freebsd"},
            "scope":           {"type": "string",  "description": "local | remote | elevated | any"},
            "complexity":      {"type": "string",  "description": "low | medium | high"},
            "has_prereqs":     {"type": "string",  "description": "true | false"},
            "limit":           {"type": "integer", "description": "Max results (default 8)"},
            "include_command": {"type": "boolean", "description": "Include command preview"},
        },
        _t_atomic_search,
    ),
}


# ── Agent state ────────────────────────────────────────────────────────────────

@dataclass
class _AgentState:
    agent_id: str
    goal: str
    backend: str
    tools_used: List[str]
    status: str = "queued"       # queued | running | completed | failed
    started_at: str = ""
    completed_at: str = ""
    result: str = ""
    error: str = ""


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _agent_system_prompt(tool_names: List[str]) -> str:
    return (
        "You are an autonomous red-team agent operating the LazyOwn framework.\n"
        "Use the available tools to pursue the goal. Rules:\n"
        "- Always check facts_show and session_status before planning.\n"
        "- Use bridge_suggest to pick the right command for the current phase.\n"
        "- After each run_command output, call reactive_suggest to detect signals.\n"
        "- Use task_add to record significant findings (creds, new hosts, access).\n"
        "- Never invent scan results or credentials.\n"
        "- Be concise. Support every conclusion with real tool output.\n"
        f"Available tools: {', '.join(tool_names)}."
    )


# ── Agent pool ────────────────────────────────────────────────────────────────

class GroqAgentPool:
    """Thread-pool-based manager for concurrent Groq/Ollama agents."""

    def __init__(self) -> None:
        self._agents: Dict[str, _AgentState] = {}
        self._lock   = threading.Lock()

    def spawn(
        self,
        goal: str,
        tools_filter: Optional[List[str]] = None,
        api_key: Optional[str] = None,
        backend: str = "groq",
        max_iterations: int = 8,
        system_prompt: str = "",
        block: bool = False,
    ) -> str:
        """
        Spawn a new agent. Returns agent_id immediately.
        If block=True, waits for completion before returning.
        """
        agent_id  = uuid.uuid4().hex[:8]
        tools     = tools_filter or list(REGISTRY.keys())
        state     = _AgentState(
            agent_id=agent_id, goal=goal, backend=backend, tools_used=tools,
        )
        with self._lock:
            self._agents[agent_id] = state

        t = threading.Thread(
            target=self._run,
            args=(state, tools, api_key, max_iterations, system_prompt),
            daemon=True,
            name=f"groq-agent-{agent_id}",
        )
        t.start()
        if block:
            t.join()
        return agent_id

    def _run(
        self,
        state: _AgentState,
        tools: List[str],
        api_key: Optional[str],
        max_iterations: int,
        system_prompt: str,
    ) -> None:
        state.status     = "running"
        state.started_at = _now_utc()
        try:
            from lazyown_llm import LLMBridge  # noqa: PLC0415
            eff_key = (
                api_key
                or _load_payload().get("api_key", "")
                or os.environ.get("GROQ_API_KEY", "")
            )
            bridge = LLMBridge(backend=state.backend, api_key=eff_key)
            for name in tools:
                if name not in REGISTRY:
                    continue
                desc, params, func = REGISTRY[name]
                bridge.register_tool(name, desc, params, func)

            answer       = bridge.ask(
                goal=state.goal,
                max_iterations=max_iterations,
                system_prompt=system_prompt or _agent_system_prompt(tools),
            )
            state.result = answer
            state.status = "completed"
        except Exception as exc:
            state.error  = str(exc)
            state.status = "failed"
        finally:
            state.completed_at = _now_utc()

    # ── Query methods ─────────────────────────────────────────────────────────

    def status(self, agent_id: str) -> Dict[str, Any]:
        with self._lock:
            s = self._agents.get(agent_id)
        if s is None:
            return {"error": f"Agent '{agent_id}' not found."}
        return {
            "agent_id":        s.agent_id,
            "status":          s.status,
            "goal":            s.goal,
            "backend":         s.backend,
            "tools_available": len(s.tools_used),
            "started_at":      s.started_at,
            "completed_at":    s.completed_at,
            "error":           s.error or None,
        }

    def result(self, agent_id: str) -> str:
        with self._lock:
            s = self._agents.get(agent_id)
        if s is None:
            return f"Agent '{agent_id}' not found."
        if s.status == "running":
            return f"Agent {agent_id} still running — poll again later."
        if s.status == "failed":
            return f"Agent {agent_id} failed: {s.error}"
        if s.status == "queued":
            return f"Agent {agent_id} is queued — not started yet."
        return s.result or "(no result)"

    def list_all(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._lock:
            items = list(self._agents.values())
        items.sort(key=lambda s: s.started_at or "", reverse=True)
        return [
            {
                "agent_id":   s.agent_id,
                "status":     s.status,
                "goal":       s.goal[:80],
                "backend":    s.backend,
                "started_at": s.started_at,
            }
            for s in items[:limit]
        ]


# ── Singleton + public API ────────────────────────────────────────────────────

_pool: Optional[GroqAgentPool] = None
_pool_lock = threading.Lock()


def get_pool() -> GroqAgentPool:
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool = GroqAgentPool()
    return _pool


def spawn_agent(
    goal: str,
    tools_filter: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    backend: str = "groq",
    max_iterations: int = 8,
    block: bool = False,
) -> str:
    """Spawn a new Groq/Ollama agent. Returns agent_id."""
    return get_pool().spawn(
        goal=goal, tools_filter=tools_filter, api_key=api_key,
        backend=backend, max_iterations=max_iterations, block=block,
    )


def agent_status(agent_id: str) -> Dict[str, Any]:
    return get_pool().status(agent_id)


def agent_result(agent_id: str) -> str:
    return get_pool().result(agent_id)


def list_agents(limit: int = 20) -> List[Dict[str, Any]]:
    return get_pool().list_all(limit)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="LazyOwn Groq Agent Pool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_sp = sub.add_parser("spawn", help="Spawn a new agent")
    p_sp.add_argument("goal", help="Goal for the agent")
    p_sp.add_argument("--backend",  default="groq", choices=["groq", "ollama"])
    p_sp.add_argument("--tools",    default="",
                      help="Comma-separated tool names (default: all 18)")
    p_sp.add_argument("--max-iter", type=int, default=8)
    p_sp.add_argument("--wait",     action="store_true",
                      help="Block until agent completes and print result")

    p_st = sub.add_parser("status", help="Check agent status")
    p_st.add_argument("agent_id")

    p_rs = sub.add_parser("result", help="Get agent result")
    p_rs.add_argument("agent_id")

    sub.add_parser("list",  help="List all agents")
    sub.add_parser("tools", help="List available tools and their schemas")

    args = parser.parse_args()

    if args.cmd == "spawn":
        tf = [t.strip() for t in args.tools.split(",") if t.strip()] or None
        aid = spawn_agent(
            goal=args.goal, tools_filter=tf,
            backend=args.backend, max_iterations=args.max_iter,
            block=args.wait,
        )
        print(f"Agent spawned: {aid}")
        if args.wait:
            print("\n" + agent_result(aid))

    elif args.cmd == "status":
        import pprint
        pprint.pprint(agent_status(args.agent_id))

    elif args.cmd == "result":
        print(agent_result(args.agent_id))

    elif args.cmd == "list":
        agents = list_agents()
        if not agents:
            print("No agents.")
        for a in agents:
            print(f"  [{a['status']:9s}] {a['agent_id']}  {a['goal']}")

    elif args.cmd == "tools":
        print(f"Available tools ({len(REGISTRY)}):")
        for name, (desc, params, _) in REGISTRY.items():
            pnames = ", ".join(params.keys()) if params else "(no params)"
            print(f"  {name:22s}  [{pnames}]  {desc[:60]}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
