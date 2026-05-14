"""Curiosity-driven engagement engine for LazyOwn.

Two psychological mechanisms drive operator adoption:

1. Biological Curiosity (Loewenstein Information Gap Theory, 1994)
   Curiosity arises when we perceive a gap between what we know and what we
   want to know.  The engine surfaces ONE undiscovered command after each
   execution, chosen from the same kill-chain phase as the command just run.
   The gap is made explicit: "You haven't tried X — it does Y."  The operator
   knows something useful exists, doesn't know how it works, and is pulled to
   explore it.  Same suggestion never repeats in a session.

2. Variable Interval Reinforcement (Skinner, 1957)
   The most durable reinforcement schedule known to behavioural science.
   Rewards appear at unpredictable command counts (drawn from a geometric
   distribution with mean MEAN_INTERVAL).  Because the operator cannot predict
   WHEN the next reward arrives, the behaviour of "run another command" is
   maintained even in the absence of an immediate payoff.  Rewards are
   genuinely useful: streak acknowledgements, exploration milestones,
   hidden-feature reveals, phase-progression badges.

Architecture
------------
- Zero imports from lazyown.py, lazyc2.py, or Flask.
- All I/O is wrapped in try/except; failure is always silent.
- Output via rich.Console so ANSI is correct on every terminal.
- State persisted to ``sessions/engagement_state.json`` (cross-session).
- The caller (shell postcmd hook) passes a minimal context dict; this module
  never reads payload.json directly.
"""

from __future__ import annotations

import json
import math
import os
import random
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

STATE_PATH = Path("sessions/engagement_state.json")
INDEX_PATH = Path("cli/command_index.json")

MEAN_INTERVAL: int = 8
_MAX_CURIOSITY_LABEL = 28

_PHASE_ALIASES: dict[str, str] = {
    "recon": "recon", "scan": "recon", "enum": "enum",
    "exploit": "exploit", "privesc": "privesc", "postexp": "postexp",
    "lateral": "lateral", "cred": "cred", "persist": "persist",
    "exfil": "exfil", "report": "report", "c2": "c2", "ai": "ai",
}

_PHASE_LABEL: dict[str, str] = {
    "recon":   "Reconnaissance",
    "scan":    "Scanning & Enumeration",
    "enum":    "Enumeration",
    "exploit": "Exploitation",
    "privesc": "Privilege Escalation",
    "postexp": "Post-Exploitation",
    "lateral": "Lateral Movement",
    "cred":    "Credential Access",
    "persist": "Persistence",
    "exfil":   "Exfiltration",
    "report":  "Reporting",
    "c2":      "Command & Control",
    "ai":      "AI Agents",
}

_VRI_REWARDS: list[dict[str, Any]] = [
    {
        "id": "streak",
        "render": lambda ctx: _render_streak(ctx),
    },
    {
        "id": "exploration_pct",
        "render": lambda ctx: _render_exploration(ctx),
    },
    {
        "id": "phase_badge",
        "render": lambda ctx: _render_phase_badge(ctx),
    },
    {
        "id": "hidden_feature",
        "render": lambda ctx: _render_hidden_feature(ctx),
    },
    {
        "id": "arsenal_tip",
        "render": lambda ctx: _render_arsenal_tip(ctx),
    },
]

_HIDDEN_FEATURES: list[tuple[str, str]] = [
    ("palette recon",     "browse every recon command grouped by kill-chain phase"),
    ("suggest_next",      "graph-powered next-command from your recent activity"),
    ("recommend_next",    "policy + graph recommendation based on session history"),
    ("sitrep",            "unified status: scans, creds, tasks, phase, plan"),
    ("wizard --check",    "instant readiness check without re-running setup"),
    ("god_nodes",         "find the most-connected commands in the knowledge graph"),
    ("apt_playbook list", "list and run public APT emulation playbooks"),
    ("l00t",              "review all captured credentials and hashes"),
    ("dashboard",         "full-screen TUI: target, kill-chain, recent commands, hints"),
    ("sandbox on",        "isolate the next run inside a Docker container"),
    ("pop <cmd>",         "open a floating tmux pane to run any command"),
    ("note <text>",       "append a timestamped field note to sessions/notes.jsonl"),
    ("pivot <host>",      "record a pivot hop and track the network chain"),
    ("ctx",               "one-line situational context — good to run between commands"),
    ("scans",             "list every nmap artefact in sessions/ with age and size"),
    ("tasks add <text>",  "add a task to the backlog; track with 'tasks start/done'"),
    ("phase <name>",      "advance the kill-chain phase and log the transition"),
    ("fz <query>",        "fuzzy-find any command by partial name or keyword"),
    ("form <cmd>",        "interactive guided form for commands with many parameters"),
    ("tgrep <pattern>",   "grep across all recent command outputs in one shot"),
    ("graph_search <q>",  "semantic search across the knowledge graph nodes"),
    ("neighbors <node>",  "walk the knowledge graph outward from any command"),
    ("apt_playbook run",  "execute a real APT playbook (apt28, apt29, fin7…)"),
]

_ARSENAL_TIPS: list[str] = [
    "Run 'assign' to set any payload.json key — tab-complete shows all available keys.",
    "'palette <phase>' filters the command catalogue to just one kill-chain stage.",
    "The 'sandbox' command lets you toggle Docker isolation without restarting.",
    "'listener add <port> [ssl]' registers a new C2 port without restarting lazyc2.",
    "Press Tab after a partial command — fuzzy completion finds it even with typos.",
    "'suggest_next' reads your command history and recommends the graph-adjacent next step.",
    "The 'pop <cmd>' command opens a floating tmux pane — great for long-running tools.",
    "All sessions/ artefacts are permanent — 'scans' lists every nmap output with age.",
    "'wizard --check' shows your readiness summary in seconds without changing anything.",
    "'ctx' prints a one-line situational summary — fast enough to run before every command.",
    "Every 'do_*' command is exposed to Claude Code automatically via the MCP server.",
    "'tgrep <pattern>' searches across ALL previous command outputs, not just the last one.",
    "'apt_playbook run <name>' generates an attack_plan.yaml from a real APT report.",
    "The reactive hints line below each command comes from a knowledge graph — run '/graphify .' to rebuild it.",
    "'form <cmd>' opens an interactive guided form for any complex command.",
    "Use 'note' to capture field observations; they appear in 'sitrep' under your target.",
]


@dataclass
class EngagementState:
    """Persisted cross-session engagement metrics."""

    total_commands: int = 0
    session_commands: int = 0
    commands_seen: list[str] = field(default_factory=list)
    phases_entered: list[str] = field(default_factory=list)
    rewards_given: list[str] = field(default_factory=list)
    session_curiosity_shown: list[str] = field(default_factory=list)
    next_reward_at: int = 0
    session_start_ts: float = field(default_factory=time.time)
    last_cmd: str = ""


def _load_state() -> EngagementState:
    try:
        if STATE_PATH.exists():
            raw = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            st = EngagementState(**{k: v for k, v in raw.items() if k in EngagementState.__dataclass_fields__})
            st.session_commands = 0
            st.session_curiosity_shown = []
            st.session_start_ts = time.time()
            return st
    except Exception:
        pass
    state = EngagementState()
    state.next_reward_at = _next_threshold(0)
    return state


def _save_state(state: EngagementState) -> None:
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = STATE_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")
        tmp.replace(STATE_PATH)
    except Exception:
        pass


def _load_index() -> dict[str, Any]:
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _next_threshold(current: int) -> int:
    """Draw the next reward trigger from a geometric distribution."""
    gap = max(2, int(round(-MEAN_INTERVAL * math.log(max(random.random(), 1e-9)))))
    return current + gap


def _phase_for_cmd(cmd: str, index: dict[str, Any]) -> str:
    ptc = index.get("phase_to_commands", {})
    normalized = f"do_{cmd}" if not cmd.startswith("do_") else cmd
    for phase, cmds in ptc.items():
        if normalized in cmds or cmd in cmds:
            return phase
    return ""


def _commands_in_phase(phase: str, index: dict[str, Any]) -> list[str]:
    ptc = index.get("phase_to_commands", {})
    return list(ptc.get(phase, []))


def _summary_for_cmd(cmd: str, index: dict[str, Any]) -> str:
    normalized = f"do_{cmd}" if not cmd.startswith("do_") else cmd
    cmds = index.get("commands", [])
    if isinstance(cmds, list):
        for entry in cmds:
            if isinstance(entry, dict) and entry.get("name") in (normalized, cmd):
                return (entry.get("summary") or "")[:80]
        return ""
    if isinstance(cmds, dict):
        entry = cmds.get(normalized) or cmds.get(cmd) or {}
        return (entry.get("summary") or "")[:80]
    return ""


# ── Curiosity engine ──────────────────────────────────────────────────────────

def _run_curiosity(cmd: str, state: EngagementState, index: dict[str, Any]) -> None:
    """Surface one undiscovered command from the same phase as ``cmd``."""
    phase = _phase_for_cmd(cmd, index)
    if not phase:
        return

    candidates = _commands_in_phase(phase, index)
    seen_set = set(state.commands_seen)
    shown_set = set(state.session_curiosity_shown)
    never_run = [
        c for c in candidates
        if c not in seen_set
        and c not in shown_set
        and c != f"do_{cmd}"
        and c != cmd
    ]
    if not never_run:
        return

    pick = random.choice(never_run)
    state.session_curiosity_shown.append(pick)

    label = pick.replace("do_", "")[:_MAX_CURIOSITY_LABEL]
    summary = _summary_for_cmd(pick, index)

    line = f"    \033[2;36m  explore:\033[0m \033[1;36m{label:<{_MAX_CURIOSITY_LABEL}}\033[0m"
    if summary:
        line += f"  \033[2m{summary[:70]}\033[0m"
    print(line, flush=True)


# ── VRI rewards ───────────────────────────────────────────────────────────────

def _render_streak(ctx: dict[str, Any]) -> None:
    n = ctx.get("session_commands", 0)
    labels = {
        (1, 3): "warming up",
        (4, 9): "finding your rhythm",
        (10, 19): "in the zone",
        (20, 49): "on a roll",
        (50, 99): "deep recon mode",
        (100, 10000): "elite operator",
    }
    label = "going strong"
    for (lo, hi), l in labels.items():
        if lo <= n <= hi:
            label = l
            break
    print(f"    \033[2m  {n} commands this session \033[0m\033[1;32m{label}\033[0m", flush=True)


def _render_exploration(ctx: dict[str, Any]) -> None:
    seen = ctx.get("total_seen", 0)
    total = ctx.get("total_commands_in_index", 1)
    pct = min(100, round(100 * seen / total, 1))
    bar_len = 20
    filled = int(bar_len * pct / 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"    \033[2m  arsenal explored  \033[0m\033[36m{bar}\033[0m\033[1m  {pct}%\033[0m\033[2m  ({seen}/{total} commands)\033[0m", flush=True)


def _render_phase_badge(ctx: dict[str, Any]) -> None:
    phase = ctx.get("current_phase", "")
    if not phase:
        return
    label = _PHASE_LABEL.get(phase, phase.title())
    print(f"    \033[2m  phase \033[0m\033[1;37;41m {label} \033[0m\033[2m  — run \033[0m\033[1;36mpalette {phase}\033[0m\033[2m to see all commands in this stage\033[0m", flush=True)


def _render_hidden_feature(ctx: dict[str, Any]) -> None:
    rewards_given = ctx.get("rewards_given", [])
    candidates = [f for f in _HIDDEN_FEATURES if f[0] not in rewards_given]
    if not candidates:
        candidates = _HIDDEN_FEATURES
    cmd_label, description = random.choice(candidates)
    print(f"    \033[2m  hidden feature  \033[0m\033[1;35m{cmd_label:<30}\033[0m\033[2m{description}\033[0m", flush=True)


def _render_arsenal_tip(ctx: dict[str, Any]) -> None:
    tip = random.choice(_ARSENAL_TIPS)
    print(f"    \033[2m  tip  {tip}\033[0m", flush=True)


def _fire_vri_reward(state: EngagementState, ctx: dict[str, Any]) -> None:
    """Pick and render one VRI reward, then schedule the next threshold."""
    weights = [3, 2, 2, 2, 1]
    reward = random.choices(_VRI_REWARDS, weights=weights, k=1)[0]

    print()
    print("    \033[2m" + "─" * 60 + "\033[0m")
    try:
        reward["render"](ctx)
    except Exception:
        pass
    print("    \033[2m" + "─" * 60 + "\033[0m")
    print()

    state.rewards_given.append(reward["id"])
    state.next_reward_at = _next_threshold(state.total_commands)


# ── Public entry point ────────────────────────────────────────────────────────

_state: EngagementState | None = None
_index: dict[str, Any] | None = None


def render_engagement_hook(
    cmd: str,
    phase: str = "",
    enabled: bool = True,
) -> None:
    """Post-command hook: curiosity reveal + VRI reward when due.

    Args:
        cmd: The command name that just executed (e.g. "lazynmap").
        phase: Current engagement phase from world_model (e.g. "recon").
        enabled: When False this function is a no-op.  Controlled by
            ``enable_inline_hints`` in payload.json so the operator can
            silence all engagement output with one flag.

    Returns:
        None — side effects are at most 2-3 lines written to stdout.
    """
    if not enabled or not cmd:
        return

    global _state, _index

    try:
        if _state is None:
            _state = _load_state()
        if _index is None:
            _index = _load_index()

        _state.total_commands += 1
        _state.session_commands += 1
        _state.last_cmd = cmd

        normalized = f"do_{cmd}" if not cmd.startswith("do_") else cmd
        if normalized not in _state.commands_seen:
            _state.commands_seen.append(normalized)

        current_phase = _phase_for_cmd(cmd, _index) or phase
        if current_phase and current_phase not in _state.phases_entered:
            _state.phases_entered.append(current_phase)

        total_in_index = sum(
            len(v) for v in _index.get("phase_to_commands", {}).values()
        )

        ctx: dict[str, Any] = {
            "session_commands": _state.session_commands,
            "total_seen": len(_state.commands_seen),
            "total_commands_in_index": max(total_in_index, 1),
            "current_phase": current_phase,
            "rewards_given": list(_state.rewards_given[-20:]),
        }

        _run_curiosity(cmd, _state, _index)

        if _state.total_commands >= _state.next_reward_at:
            _fire_vri_reward(_state, ctx)

        _save_state(_state)

    except Exception:
        pass


def reset_session() -> None:
    """Reset session counters without clearing cross-session progress.

    Call this at shell startup so commands_seen accumulates across sessions
    but session_commands restarts from 0.
    """
    global _state
    _state = _load_state()
