"""Typed tool sets per agent role with shell allowlists.

Ports the LAZY ``agent/toolcatalog.go`` + ``agent/tools.go`` contract:
each agent role (planner / worker / main / goals) owns a fixed tool set.
Handlers always live in code; this catalog only decides visibility and
safe defaults. Shell commands from the LLM go through
:func:`extract_tool` (shlex, not naive split) and :func:`validate_shell`.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field


PLANNER = "planner"
WORKER = "worker"
MAIN = "main"
GOALS = "goals"

VALID_ROLES = frozenset({PLANNER, WORKER, MAIN, GOALS})

_SHELL_META_CHARS = (";", "&&", "||", "$(", "`", "|", ">", "<", "\n")


@dataclass(frozen=True, slots=True)
class ToolSeed:
    """Catalog entry mirroring LAZY ToolSeed (key + desc + agents)."""

    key: str
    desc: str
    agents: tuple = ()


def builtin_seeds() -> list[ToolSeed]:
    """Return the default graph-tool catalog (handlers stay in code)."""
    return [
        ToolSeed(key="set_goals", desc="Decompose an objective into goals.",
                 agents=(GOALS, MAIN)),
        ToolSeed(key="set_constraints", desc="Record task allow/deny constraints.",
                 agents=(GOALS, MAIN)),
        ToolSeed(key="graph_overview", desc="Read exploration frontier and coverage.",
                 agents=(PLANNER, MAIN)),
        ToolSeed(key="add_intent", desc="Queue one exploration intent.",
                 agents=(PLANNER,)),
        ToolSeed(key="prove_goal", desc="Link evidence to a goal and mark it met.",
                 agents=(PLANNER, WORKER)),
        ToolSeed(key="goal_met", desc="End the whole task immediately.", agents=()),
        ToolSeed(key="record_fact", desc="Write an exploration fact.",
                 agents=(WORKER,)),
        ToolSeed(key="report_finding", desc="Record a confirmed finding with evidence.",
                 agents=(WORKER,)),
        ToolSeed(key="bind_finding_traffic",
                 desc="Attach traffic refs to a finding.",
                 agents=(WORKER, PLANNER)),
        ToolSeed(key="insert_assets", desc="Upsert assets into the graph.",
                 agents=(WORKER, PLANNER)),
        ToolSeed(key="list_assets", desc="Query assets by DSL.",
                 agents=(PLANNER, WORKER, MAIN)),
        ToolSeed(key="traffic_search", desc="Search recorded exchanges.",
                 agents=(PLANNER, WORKER)),
        ToolSeed(key="traffic_get", desc="Fetch one exchange body.",
                 agents=(PLANNER, WORKER)),
        ToolSeed(key="node_detail", desc="Fetch one exploration node.",
                 agents=(PLANNER, WORKER)),
    ]


_SEEDS_BY_KEY = {s.key: s for s in builtin_seeds()}


def resolve(agent: str, tool_key: str) -> ToolSeed | None:
    """Return the seed when bound to agent, else None (LAZY ToolResolve)."""
    seed = _SEEDS_BY_KEY.get(str(tool_key or ""))
    if seed is None:
        return None
    if str(agent or "") not in seed.agents:
        return None
    return seed


PLANNER_SHELL = frozenset({
    "lazynmap", "nmap", "rustscan", "masscan", "whatweb", "nikto",
    "gobuster", "ffuf", "fuzz", "dig", "nslookup", "whois",
    "smbclient", "rpcclient", "enum4linux", "ldapsearch",
    "facts_show", "auto_populate", "threat_model", "recommend_next",
})

WORKER_SHELL = PLANNER_SHELL | frozenset({
    "hydra", "medusa", "crackmapexec", "cme", "nxc", "evil-winrm",
    "impacket", "secretsdump", "psexec", "wmiexec", "smbexec",
    "metasploit", "msfconsole", "msfvenom", "searchsploit",
    "sqlmap", "burp", "curl", "wget", "ssh", "scp",
    "powershell", "cmd", "mimikatz", "bloodhound",
    "linpeas", "winpeas", "privesc", "hunt", "auto_pwn",
    "exploit", "chain", "playbook", "payload",
})

MAIN_SHELL = WORKER_SHELL | frozenset({
    "orchestrate", "engage", "campaign", "report", "sitrep",
    "dashboard", "collab", "ask", "chat",
})


def extract_tool(command: str) -> tuple[str, bool]:
    """Split tool name with shlex; flag shell metacharacters.

    Returns (tool, has_shell_meta). Empty command yields ("", False).
    """
    raw = str(command or "").strip()
    if not raw:
        return "", False
    has_meta = any(m in raw for m in _SHELL_META_CHARS)
    first_line = raw.splitlines()[0] if "\n" in raw else raw
    for sep in (";", "|", "&", "`", "$("):
        if sep in first_line:
            first_line = first_line.split(sep)[0]
    try:
        parts = shlex.split(first_line, posix=True)
    except ValueError:
        parts = first_line.strip().split()
    if not parts:
        return "", has_meta
    tool = parts[0].rsplit("/", 1)[-1].lower()
    return tool, has_meta


def validate_shell(role: str, command: str) -> tuple[bool, str]:
    """Check a shell command against the role allowlist.

    Returns (allowed, reason). Planner is recon-only; exploit verbs are
    denied for planner and must run as worker intents (LAZY parity).
    Shell metacharacters always require ask (returned as not-allowed
    with reason shell_meta so the caller routes to approval).
    """
    normalized_role = str(role or "").lower()
    if normalized_role not in VALID_ROLES:
        return False, f"unknown role: {role}"
    tool, has_meta = extract_tool(command)
    if not tool:
        return False, "empty command"
    if has_meta:
        return False, "shell_meta: compound command needs approval"
    if normalized_role == PLANNER and tool not in PLANNER_SHELL:
        if tool in WORKER_SHELL:
            return False, f"planner cannot run exploit tool '{tool}': use worker intent"
        return False, f"planner unknown tool '{tool}'"
    if normalized_role == WORKER:
        # LazyOwn exposes 700+ shell verbs; the catalog cannot enumerate
        # them all. Unknown worker tools are allowed through (the Guard
        # intercept still blocks destructive patterns) but shell
        # metacharacters always need approval.
        return True, "ok"
    if normalized_role == MAIN and tool not in MAIN_SHELL:
        return True, "ok-unknown-main"
    return True, "ok"


__all__ = [
    "PLANNER", "WORKER", "MAIN", "GOALS", "VALID_ROLES",
    "ToolSeed", "builtin_seeds", "resolve",
    "PLANNER_SHELL", "WORKER_SHELL", "MAIN_SHELL",
    "extract_tool", "validate_shell",
]
