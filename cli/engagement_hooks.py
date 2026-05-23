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
import random
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

STATE_PATH = Path("sessions/engagement_state.json")
INDEX_PATH = Path("cli/command_index.json")
USERS_PATH = Path("users.json")
PAYLOAD_PATH = Path("payload.json")
NOTIFICATIONS_PATH = Path("sessions/notifications.json")
TASKS_PATH = Path("sessions/tasks.json")
OBJECTIVES_PATH = Path("sessions/objectives.jsonl")
NOTES_PATH = Path("sessions/notes.jsonl")

MEAN_INTERVAL: int = 8
_MAX_CURIOSITY_LABEL = 28
_NOTIFICATIONS_RING_SIZE: int = 500
_VRI_RETRY_LIMIT: int = 4

KARMA_THRESHOLDS: tuple[tuple[int, str], ...] = (
    (1000, "Noob"),
    (2000, "Rookie"),
    (3000, "Skidy"),
    (4000, "Hacker"),
    (5000, "Pro"),
    (6000, "Elite"),
)
KARMA_TOP: str = "Godlike"

ELO_BASE: int = 5
ELO_FIRST_TIME_BONUS: int = 25
ELO_NEW_PHASE_BONUS: int = 50

ELO_HIGH_VALUE_CMDS: dict[str, int] = {
    "lazynmap": 15,
    "rustscan": 12,
    "nmap": 12,
    "gobuster": 8,
    "ffuf": 8,
    "feroxbuster": 8,
    "nikto": 10,
    "whatweb": 6,
    "enum4linux": 12,
    "kerbrute": 20,
    "crackmapexec": 25,
    "secretsdump": 35,
    "evil-winrm": 30,
    "hashcat": 30,
    "john": 25,
    "responder": 30,
    "mimikatz": 35,
    "linpeas": 25,
    "winpeas": 25,
    "pspy64": 15,
    "printspoofer": 20,
    "searchsploit": 10,
    "sqlmap": 20,
    "burpsuite": 15,
    "psexec": 25,
    "chisel": 15,
    "lazyc2": 20,
    "phase": 10,
    "note": 5,
    "tasks": 5,
    "sitrep": 5,
    "ctx": 3,
}

ELO_PHASE_BONUS: dict[str, int] = {
    "recon": 5,
    "enum": 8,
    "exploit": 25,
    "cred": 20,
    "privesc": 30,
    "lateral": 25,
    "postexp": 15,
    "exfil": 20,
    "report": 10,
    "c2": 12,
}

_PHASE_TO_NEXT_CMD: dict[str, str] = {
    "recon": "lazynmap",
    "enum": "enum4linux",
    "exploit": "searchsploit",
    "cred": "crackmapexec",
    "privesc": "linpeas",
    "lateral": "evil-winrm",
    "postexp": "secretsdump",
    "exfil": "scp",
    "report": "generate_report",
    "c2": "lazyc2",
}

_PHASE_ALIASES: dict[str, str] = {
    "recon": "recon",
    "scan": "recon",
    "enum": "enum",
    "exploit": "exploit",
    "privesc": "privesc",
    "postexp": "postexp",
    "lateral": "lateral",
    "cred": "cred",
    "persist": "persist",
    "exfil": "exfil",
    "report": "report",
    "c2": "c2",
    "ai": "ai",
}

_PHASE_LABEL: dict[str, str] = {
    "recon": "Reconnaissance",
    "scan": "Scanning & Enumeration",
    "enum": "Enumeration",
    "exploit": "Exploitation",
    "privesc": "Privilege Escalation",
    "postexp": "Post-Exploitation",
    "lateral": "Lateral Movement",
    "cred": "Credential Access",
    "persist": "Persistence",
    "exfil": "Exfiltration",
    "report": "Reporting",
    "c2": "Command & Control",
    "ai": "AI Agents",
}

_VRI_REWARDS: list[dict[str, Any]] = [
    {"id": "streak", "weight": 3, "render": lambda ctx: _render_streak(ctx)},
    {"id": "exploration_pct", "weight": 2, "render": lambda ctx: _render_exploration(ctx)},
    {"id": "phase_badge", "weight": 2, "render": lambda ctx: _render_phase_badge(ctx)},
    {"id": "hidden_feature", "weight": 2, "render": lambda ctx: _render_hidden_feature(ctx)},
    {"id": "arsenal_tip", "weight": 1, "render": lambda ctx: _render_arsenal_tip(ctx)},
    {"id": "methodology_task", "weight": 3, "render": lambda ctx: _render_methodology_task(ctx)},
    {"id": "methodology_obj", "weight": 3, "render": lambda ctx: _render_methodology_objective(ctx)},
    {"id": "methodology_note", "weight": 2, "render": lambda ctx: _render_methodology_note(ctx)},
]

_HIDDEN_FEATURES: list[tuple[str, str]] = [
    ("palette recon", "browse every recon command grouped by kill-chain phase"),
    ("suggest_next", "graph-powered next-command from your recent activity"),
    ("recommend_next", "policy + graph recommendation based on session history"),
    ("sitrep", "unified status: scans, creds, tasks, phase, plan"),
    ("wizard --check", "instant readiness check without re-running setup"),
    ("god_nodes", "find the most-connected commands in the knowledge graph"),
    ("apt_playbook list", "list and run public APT emulation playbooks"),
    ("l00t", "review all captured credentials and hashes"),
    ("dashboard", "full-screen TUI: target, kill-chain, recent commands, hints"),
    ("sandbox on", "isolate the next run inside a Docker container"),
    ("pop <cmd>", "open a floating tmux pane to run any command"),
    ("note <text>", "append a timestamped field note to sessions/notes.jsonl"),
    ("pivot <host>", "record a pivot hop and track the network chain"),
    ("ctx", "one-line situational context — good to run between commands"),
    ("scans", "list every nmap artefact in sessions/ with age and size"),
    ("tasks add <text>", "add a task to the backlog; track with 'tasks start/done'"),
    ("phase <name>", "advance the kill-chain phase and log the transition"),
    ("fz <query>", "fuzzy-find any command by partial name or keyword"),
    ("form <cmd>", "interactive guided form for commands with many parameters"),
    ("tgrep <pattern>", "grep across all recent command outputs in one shot"),
    ("graph_search <q>", "semantic search across the knowledge graph nodes"),
    ("neighbors <node>", "walk the knowledge graph outward from any command"),
    ("apt_playbook run", "execute a real APT playbook (apt28, apt29, fin7…)"),
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
    elo: int = 0
    last_karma_name: str = "Noob"
    elo_session_delta: int = 0


def _load_state() -> EngagementState:
    try:
        if STATE_PATH.exists():
            raw = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            st = EngagementState(**{k: v for k, v in raw.items() if k in EngagementState.__dataclass_fields__})
            st.session_commands = 0
            st.session_curiosity_shown = []
            st.session_start_ts = time.time()
            st.elo_session_delta = 0
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
    never_run = [c for c in candidates if c not in seen_set and c not in shown_set and c != f"do_{cmd}" and c != cmd]
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


def _render_streak(ctx: dict[str, Any]) -> bool:
    """Render the streak reward; always succeeds (always renders)."""
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
    for (lo, hi), candidate_label in labels.items():
        if lo <= n <= hi:
            label = candidate_label
            break
    karma = ctx.get("karma_name", "")
    elo = ctx.get("elo", 0)
    karma_tail = f"  \033[2m· \033[0m\033[1;33m{karma}\033[0m\033[2m {elo} ELO\033[0m" if karma else ""
    line = f"    \033[2m  {n} commands this session \033[0m\033[1;32m{label}\033[0m{karma_tail}"
    print(line, flush=True)
    _persist_notification(
        f"<h3>Streak</h3><p>{n} commands this session — <b>{label}</b>"
        + (f" · {karma} ({elo} ELO)" if karma else "")
        + "</p>"
    )
    return True


def _render_exploration(ctx: dict[str, Any]) -> bool:
    """Render arsenal exploration progress bar."""
    seen = ctx.get("total_seen", 0)
    total = ctx.get("total_commands_in_index", 1)
    pct = min(100, round(100 * seen / total, 1))
    bar_len = 20
    filled = int(bar_len * pct / 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    print(
        f"    \033[2m  arsenal explored  \033[0m\033[36m{bar}\033[0m\033[1m  {pct}%\033[0m\033[2m  ({seen}/{total} commands)\033[0m",
        flush=True,
    )
    _persist_notification(
        f"<h3>Arsenal explored</h3><p><b>{pct}%</b> &mdash; {seen} of {total} commands discovered.</p>"
    )
    return True


def _render_phase_badge(ctx: dict[str, Any]) -> bool:
    """Render the current kill-chain phase badge; skips when phase unknown."""
    phase = ctx.get("current_phase", "")
    if not phase:
        return False
    label = _PHASE_LABEL.get(phase, phase.title())
    print(
        f"    \033[2m  phase \033[0m\033[1;37;41m {label} \033[0m\033[2m  — run \033[0m\033[1;36mpalette {phase}\033[0m\033[2m to see all commands in this stage\033[0m",
        flush=True,
    )
    _persist_notification(
        f"<h3>Phase: {label}</h3><p>Run <code>palette {phase}</code> to see every command in this stage.</p>"
    )
    return True


def _render_hidden_feature(ctx: dict[str, Any]) -> bool:
    """Reveal one hidden CLI feature the operator hasn't seen recently."""
    rewards_given = ctx.get("rewards_given", [])
    candidates = [f for f in _HIDDEN_FEATURES if f[0] not in rewards_given]
    if not candidates:
        candidates = _HIDDEN_FEATURES
    cmd_label, description = random.choice(candidates)
    print(
        f"    \033[2m  hidden feature  \033[0m\033[1;35m{cmd_label:<30}\033[0m\033[2m{description}\033[0m", flush=True
    )
    _persist_notification(f"<h3>Hidden feature</h3><p><code>{cmd_label}</code> &mdash; {description}</p>")
    return True


def _render_arsenal_tip(ctx: dict[str, Any]) -> bool:
    """Render a single arsenal usage tip."""
    tip = random.choice(_ARSENAL_TIPS)
    print(f"    \033[2m  tip  {tip}\033[0m", flush=True)
    _persist_notification(f"<h3>Tip</h3><p>{tip}</p>")
    return True


def _render_methodology_task(ctx: dict[str, Any]) -> bool:
    """Surface one open task that aligns with the current phase.

    Reads ``sessions/tasks.json`` written by ``tasks add`` / ACI planner.
    Returns False when no pending task exists so the VRI scheduler can pick
    another reward instead of rendering an empty line.
    """
    try:
        if not TASKS_PATH.exists():
            return False
        tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
        if not isinstance(tasks, list):
            return False
        pending = [
            t for t in tasks if isinstance(t, dict) and str(t.get("status", "")).lower() not in ("done", "completed")
        ]
        if not pending:
            return False
        phase = (ctx.get("current_phase") or "").lower()
        match = [
            t
            for t in pending
            if phase
            and phase in ((t.get("title") or "") + (t.get("description") or "") + (t.get("text") or "")).lower()
        ]
        pick = random.choice(match) if match else random.choice(pending)
        title = (pick.get("title") or pick.get("text") or "")[:80]
        if not title:
            return False
        print(
            f"    \033[2m  open task  \033[0m\033[1;33m▶\033[0m \033[1m{title}\033[0m",
            flush=True,
        )
        _persist_notification(f"<h3>Open task surfaced</h3><p>▶ {title}</p>")
        return True
    except Exception:
        return False


def _render_methodology_objective(ctx: dict[str, Any]) -> bool:
    """Surface one pending objective and a phase-appropriate next command.

    Reads ``sessions/objectives.jsonl`` (auto-injected objectives from the
    world model watcher).  Teaches methodology by pairing the objective text
    with the canonical next command for its phase.
    """
    try:
        if not OBJECTIVES_PATH.exists():
            return False
        objs: list[dict[str, Any]] = []
        for line in OBJECTIVES_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            if not isinstance(o, dict):
                continue
            status = str(o.get("status") or "pending").lower()
            if status in ("pending", "open", "in_progress"):
                objs.append(o)
        if not objs:
            return False
        pick = random.choice(objs[-20:])
        text = (pick.get("text") or pick.get("title") or "")[:80]
        if not text:
            return False
        phase = ""
        ctx_field = pick.get("context")
        if isinstance(ctx_field, dict):
            phase = (ctx_field.get("phase") or "").lower()
        phase = phase or (pick.get("phase") or "").lower()
        cmd_hint = _PHASE_TO_NEXT_CMD.get(phase, "suggest_next")
        print(
            f"    \033[2m  objective  \033[0m\033[1;35m▶\033[0m \033[1m{text}\033[0m  "
            f"\033[2m→ try \033[0m\033[1;36m{cmd_hint}\033[0m",
            flush=True,
        )
        _persist_notification(f"<h3>Objective</h3><p>▶ {text}<br/><i>Suggested next:</i> <code>{cmd_hint}</code></p>")
        return True
    except Exception:
        return False


def _render_methodology_note(ctx: dict[str, Any]) -> bool:
    """Recall the latest operator note and suggest a methodology-aligned command.

    Reads ``sessions/notes.jsonl`` written by the ``note`` command and pairs
    the most-recent note with the canonical next command for its recorded
    phase.  Teaches the operator to translate observations into actions.
    """
    try:
        if not NOTES_PATH.exists():
            return False
        recent = NOTES_PATH.read_text(encoding="utf-8").splitlines()[-10:]
        notes: list[dict[str, Any]] = []
        for line in recent:
            line = line.strip()
            if not line:
                continue
            try:
                n = json.loads(line)
            except Exception:
                continue
            if isinstance(n, dict) and n.get("text"):
                notes.append(n)
        if not notes:
            return False
        pick = notes[-1]
        text = str(pick.get("text", ""))[:70]
        if not text:
            return False
        phase = (pick.get("phase") or "").lower()
        cmd_hint = _PHASE_TO_NEXT_CMD.get(phase, "ctx")
        print(
            f'    \033[2m  recall note  \033[0m\033[3m"{text}"\033[0m  \033[2m→ \033[0m\033[1;36m{cmd_hint}\033[0m',
            flush=True,
        )
        _persist_notification(
            f"<h3>Recall note</h3><blockquote>{text}</blockquote><p><i>Suggested next:</i> <code>{cmd_hint}</code></p>"
        )
        return True
    except Exception:
        return False


def _fire_vri_reward(state: EngagementState, ctx: dict[str, Any]) -> None:
    """Pick one VRI reward and render it; retry on no-op rewards.

    Methodology rewards may return False when their backing artefact is empty
    (no pending tasks, objectives or notes).  The scheduler then samples a
    different reward instead of printing an empty divider.  After at most
    ``_VRI_RETRY_LIMIT`` attempts the streak reward is forced as fallback so
    the operator always sees something when the schedule fires.
    """
    weights = [r.get("weight", 1) for r in _VRI_REWARDS]
    print()
    print("    \033[2m" + "─" * 60 + "\033[0m")
    rendered = False
    chosen_id = ""
    tried: set[str] = set()
    for _ in range(_VRI_RETRY_LIMIT):
        reward = random.choices(_VRI_REWARDS, weights=weights, k=1)[0]
        if reward["id"] in tried:
            continue
        tried.add(reward["id"])
        try:
            if reward["render"](ctx):
                rendered = True
                chosen_id = reward["id"]
                break
        except Exception:
            continue
    if not rendered:
        try:
            _render_streak(ctx)
            chosen_id = "streak"
        except Exception:
            pass
    print("    \033[2m" + "─" * 60 + "\033[0m")
    print()

    if chosen_id:
        state.rewards_given.append(chosen_id)
    state.next_reward_at = _next_threshold(state.total_commands)


# ── ELO + karma + persistence ─────────────────────────────────────────────────


def get_karma_name(elo: int) -> str:
    """Return karma rank for an ELO score.

    Mirrors the bracket function ``get_karma_name`` in ``lazyc2.py`` so the
    terminal and the C2 web UI display identical ranks for the same operator.

    Args:
        elo: Non-negative integer score.

    Returns:
        Human-facing karma label (``Noob`` … ``Godlike``).
    """
    for threshold, label in KARMA_THRESHOLDS:
        if elo < threshold:
            return label
    return KARMA_TOP


def _award_elo(cmd: str, first_time: bool, new_phase: bool, current_phase: str) -> int:
    """Compute the ELO delta for executing ``cmd``.

    The reward is the sum of:
      * ``ELO_BASE`` for any command,
      * a high-value bonus when ``cmd`` is in ``ELO_HIGH_VALUE_CMDS``,
      * a phase bonus when ``current_phase`` is in ``ELO_PHASE_BONUS``,
      * ``ELO_FIRST_TIME_BONUS`` when the operator runs this command for the
        first time across all sessions,
      * ``ELO_NEW_PHASE_BONUS`` when the operator enters a phase for the
        first time across all sessions.

    Returns:
        Positive integer ELO delta to add to the operator's score.
    """
    delta = ELO_BASE
    key = cmd.replace("do_", "")
    delta += ELO_HIGH_VALUE_CMDS.get(key, 0)
    delta += ELO_PHASE_BONUS.get((current_phase or "").lower(), 0)
    if first_time:
        delta += ELO_FIRST_TIME_BONUS
    if new_phase:
        delta += ELO_NEW_PHASE_BONUS
    return delta


def _sync_user_elo(delta: int) -> bool:
    """Patch ``users.json`` so the C2 dashboard reflects terminal activity.

    Reads ``payload.json:c2_user`` to know which row to update.  Performs an
    atomic temp-file rename so a partial write cannot corrupt the user DB the
    Flask login pipeline depends on.  Silent on any failure (missing payload,
    missing users.json, user not registered, IO error) so a terminal session
    on a workstation without the C2 stack never breaks.

    Args:
        delta: ELO points to add (non-negative).

    Returns:
        True when the user row was patched and persisted, False otherwise.
    """
    if delta <= 0:
        return False
    try:
        if not PAYLOAD_PATH.exists() or not USERS_PATH.exists():
            return False
        payload = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
        target = payload.get("c2_user")
        if not target:
            return False
        users = json.loads(USERS_PATH.read_text(encoding="utf-8"))
        if not isinstance(users, list):
            return False
        modified = False
        for user in users:
            if isinstance(user, dict) and user.get("username") == target:
                user["elo"] = int(user.get("elo", 0)) + int(delta)
                modified = True
                break
        if not modified:
            return False
        tmp = USERS_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(users, indent=4), encoding="utf-8")
        tmp.replace(USERS_PATH)
        return True
    except Exception:
        return False


def _persist_notification(html: str) -> bool:
    """Append a notification entry to ``sessions/notifications.json``.

    The C2 dashboard polls this file to render the in-app notification feed,
    so terminal-side rewards become visible in the web UI without any extra
    plumbing.  Writes use a temp-file rename so a concurrent reader never
    sees a half-written JSON document.  The file is capped at
    ``_NOTIFICATIONS_RING_SIZE`` entries to prevent unbounded growth.

    Args:
        html: Sanitized HTML fragment to render inside the dashboard feed.

    Returns:
        True on successful persistence, False on any IO or decoding error.
    """
    try:
        NOTIFICATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
        entries: list[dict[str, Any]] = []
        if NOTIFICATIONS_PATH.exists():
            try:
                raw = json.loads(NOTIFICATIONS_PATH.read_text(encoding="utf-8"))
                if isinstance(raw, list):
                    entries = [e for e in raw if isinstance(e, dict)]
            except Exception:
                entries = []
        entries.append({"html": html})
        if len(entries) > _NOTIFICATIONS_RING_SIZE:
            entries = entries[-_NOTIFICATIONS_RING_SIZE:]
        tmp = NOTIFICATIONS_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(entries, indent=4), encoding="utf-8")
        tmp.replace(NOTIFICATIONS_PATH)
        return True
    except Exception:
        return False


def _check_karma_up(state: EngagementState) -> bool:
    """Fire an out-of-band reward when ELO crosses a karma threshold.

    Karma promotions never consume the VRI schedule so the operator gets a
    clear signal that effort translated into rank, independent of the
    variable reinforcement timer.

    Returns:
        True when a promotion was rendered, False otherwise.
    """
    new_karma = get_karma_name(state.elo)
    if new_karma == state.last_karma_name:
        return False
    old = state.last_karma_name
    state.last_karma_name = new_karma
    print()
    print("    \033[2m" + "─" * 60 + "\033[0m")
    print(
        f"    \033[1;33m  KARMA UP  \033[0m\033[2m{old}\033[0m\033[1;33m → "
        f"\033[0m\033[1;32m{new_karma}\033[0m\033[2m  ({state.elo} ELO)\033[0m",
        flush=True,
    )
    print("    \033[2m" + "─" * 60 + "\033[0m")
    print()
    _persist_notification(f"<h2>Karma Up: {old} → {new_karma}</h2><p>ELO score: {state.elo}</p>")
    return True


# ── Public entry point ────────────────────────────────────────────────────────

_state: EngagementState | None = None
_index: dict[str, Any] | None = None


def render_engagement_hook(
    cmd: str,
    phase: str = "",
    enabled: bool = True,
) -> None:
    """Post-command hook: curiosity reveal + ELO + VRI reward when due.

    Args:
        cmd: The command name that just executed (e.g. "lazynmap").
        phase: Current engagement phase from world_model (e.g. "recon").
        enabled: When False this function is a no-op.  Controlled by
            ``enable_inline_hints`` in payload.json so the operator can
            silence all engagement output with one flag.

    Returns:
        None — side effects are at most 2-3 lines written to stdout and one
        atomic patch each to ``sessions/engagement_state.json``,
        ``sessions/notifications.json`` and ``users.json``.
    """
    if not enabled or not cmd:
        return

    global _state, _index

    try:
        if _state is None:
            _state = _load_state()
        if _index is None:
            _index = _load_index()

        normalized = f"do_{cmd}" if not cmd.startswith("do_") else cmd
        first_time = normalized not in _state.commands_seen

        _state.total_commands += 1
        _state.session_commands += 1
        _state.last_cmd = cmd

        if first_time:
            _state.commands_seen.append(normalized)

        current_phase = _phase_for_cmd(cmd, _index) or phase
        new_phase = bool(current_phase) and current_phase not in _state.phases_entered
        if new_phase:
            _state.phases_entered.append(current_phase)

        elo_delta = _award_elo(cmd, first_time, new_phase, current_phase)
        _state.elo += elo_delta
        _state.elo_session_delta += elo_delta
        _sync_user_elo(elo_delta)

        total_in_index = sum(len(v) for v in _index.get("phase_to_commands", {}).values())

        ctx: dict[str, Any] = {
            "session_commands": _state.session_commands,
            "total_seen": len(_state.commands_seen),
            "total_commands_in_index": max(total_in_index, 1),
            "current_phase": current_phase,
            "rewards_given": list(_state.rewards_given[-20:]),
            "elo": _state.elo,
            "karma_name": get_karma_name(_state.elo),
            "elo_session_delta": _state.elo_session_delta,
        }

        _run_curiosity(cmd, _state, _index)
        _check_karma_up(_state)

        if _state.total_commands >= _state.next_reward_at:
            _fire_vri_reward(_state, ctx)

        _save_state(_state)

    except Exception:
        pass


def get_state_snapshot() -> dict[str, Any]:
    """Return a read-only snapshot of current engagement state for CLI display.

    Used by ``do_karma`` in ``lazyown.py`` to print the operator's current
    score without touching the on-disk state file.  When the state has not
    been loaded yet (e.g. immediately after shell startup) this function
    loads it lazily so the first call from ``karma`` returns real data.

    Returns:
        Plain dict with keys ``elo``, ``karma_name``, ``commands_seen``,
        ``phases_entered``, ``total_commands``, ``session_commands``,
        ``elo_session_delta``, ``next_reward_at``.
    """
    global _state
    if _state is None:
        _state = _load_state()
    return {
        "elo": _state.elo,
        "karma_name": get_karma_name(_state.elo),
        "commands_seen": list(_state.commands_seen),
        "phases_entered": list(_state.phases_entered),
        "total_commands": _state.total_commands,
        "session_commands": _state.session_commands,
        "elo_session_delta": _state.elo_session_delta,
        "next_reward_at": _state.next_reward_at,
    }


def reset_session() -> None:
    """Reset session counters without clearing cross-session progress.

    Call this at shell startup so commands_seen accumulates across sessions
    but session_commands restarts from 0.
    """
    global _state
    _state = _load_state()
