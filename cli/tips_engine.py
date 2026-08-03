"""Unified post-command tips engine: single coordination point for all suggestion surfaces.

Before this module, the shell registered five independent postcmd hooks that
rendered suggestion lines without coordination:
  - ``_inline_hint_hook``: kill-chain adjacency hints (reactive_hints.py)
  - ``_engagement_hook``: curiosity/VRI/ELO rewards (engagement_hooks.py)
  - ``_autosuggest_hook``: ghost-text next-command (autosuggest.py)
  - ``_toast_hook``: event toasts (toasts.py)
  - ``_recording_hook``: makerc recording

Each hook computed its own context, parsed the same transcript, and produced
overlapping or contradictory advice. The operator saw up to five different
"You should run X" lines with no coordination.

This module collapses them into one logical chain of thought:

1.  **Kill-chain adjacency hints** — fast, deterministic follow-ups from
    ``_KILL_CHAIN_NEXT`` and ``_PHASE_PRIORITY`` tables.
2.  **Contextual tips** — triggers that match session state (OS, phase,
    creds found) to surface rarely-discovered commands.
3.  **Curiosity reveal** — one undiscovered command from the same phase,
    varying within the session.
4.  **Auto-suggest refresh** — ghost-text for the next prompt (press '.').
5.  **VRI reward** — variable-interval reinforcement at unpredictable
    command counts.
6.  **ELO / karma scoring** — persistent skill tracking.

All rendering is non-blocking and respects ``ui_hints`` level. A misbehaving
surface is silently skipped; the rest continue.

Design contract (SOLID):
    - Single responsibility: coordinate rendering surfaces.
    - Open/Closed: surfaces are registered as callables; adding a surface
      means appending one entry, never modifying the engine.
    - Dependency Inversion: the engine receives its dependencies (hints
      tables, tip registry, curiosity/engagement state, autosuggest engine)
      via constructor injection, never importing lazyown.py or lazyc2.py.
    - Zero side effects beyond stdout — the engine is pure coordination.
"""

from __future__ import annotations

import csv
import json
import math
import random
import re
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.text import Text

SKIP_COMMANDS: frozenset[str] = frozenset(
    {
        "help",
        "?",
        "exit",
        "quit",
        "history",
        "shell",
        "dashboard",
        "next",
        ".",
        ",",
        "set",
        "assign",
        "show",
        "palette",
        "palette_k",
        "browse",
        "timeline_browser",
        "form",
        "graph_overlay",
        "toast_clear",
        "edit",
        "run_script",
        "shortcuts",
        "_relative_run",
        "sitrep",
        "ctx",
        "phase",
        "note",
        "l00t",
        "pivot",
        "tasks",
        "scans",
        "wizard",
    }
)

_FULL_KILLCHAIN_TRIGGERS: frozenset[str] = frozenset(
    {
        "lazynmap",
        "auto_populate",
        "auto_pwn",
        "hunt",
        "pwntomate",
    }
)

DEFAULT_SESSIONS_DIR: str = "sessions"
DEFAULT_COMMAND_INDEX: str = "cli/command_index.json"
DEFAULT_USERS_PATH: str = "users.json"
DEFAULT_PAYLOAD_PATH: str = "payload.json"

HINT_MAX_LABEL: int = 28
TIP_TEXT_MAX: int = 80
CURIOSITY_MAX_LABEL: int = 28

MEAN_INTERVAL: int = 8
VRI_RETRY_LIMIT: int = 4
NOTIFICATIONS_RING_SIZE: int = 500

ELO_BASE: int = 5
ELO_FIRST_TIME_BONUS: int = 25
ELO_NEW_PHASE_BONUS: int = 50

KARMA_THRESHOLDS: tuple[tuple[int, str], ...] = (
    (1000, "Noob"),
    (2000, "Rookie"),
    (3000, "Skidy"),
    (4000, "Hacker"),
    (5000, "Pro"),
    (6000, "Elite"),
)
KARMA_TOP: str = "Godlike"

COMMAND_NAME_RE: re.Pattern[str] = re.compile(r"^do_[a-z][a-z0-9_]*$")


@dataclass
class TipsConfig:
    """Centralised configuration for the unified tips engine.

    Every magic number, path, and lookup table lives here so the engine
    is testable without touching the filesystem and tunable without
    editing the engine itself.
    """

    sessions_dir: str = DEFAULT_SESSIONS_DIR
    command_index_path: str = DEFAULT_COMMAND_INDEX
    users_path: str = DEFAULT_USERS_PATH
    payload_path: str = DEFAULT_PAYLOAD_PATH

    hints_limit: int = 3
    tip_limit: int = 1

    kill_chain_next: Mapping[str, Sequence[str]] = field(default_factory=dict)
    phase_priority: Mapping[str, Sequence[str]] = field(default_factory=dict)

    high_value_cmds: Mapping[str, int] = field(default_factory=dict)
    phase_bonus: Mapping[str, int] = field(default_factory=dict)

    vri_rewards: Sequence[dict[str, Any]] = field(default_factory=list)
    hidden_features: Sequence[tuple[str, str]] = field(default_factory=list)
    arsenal_tips: Sequence[str] = field(default_factory=list)

    elo_base: int = ELO_BASE
    elo_first_time_bonus: int = ELO_FIRST_TIME_BONUS
    elo_new_phase_bonus: int = ELO_NEW_PHASE_BONUS
    mean_interval: int = MEAN_INTERVAL

    session_tips: Sequence[str] = field(default_factory=list)

    tips_registry: Sequence[dict[str, Any]] = field(default_factory=list)

    enabled: bool = True

    killchain_auto_every: int = 0
    killchain_auto_on_phase_change: bool = True


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
    badges: list[str] = field(default_factory=list)


class TipsEngine:
    """Coordinate all post-command suggestion surfaces into one render pass.

    The engine holds no per-call state beyond the injected config and a
    reference to the autosuggest engine. Engagement state is persisted to
    disk via ``sessions/engagement_state.json``.
    """

    def __init__(
        self,
        config: TipsConfig | None = None,
        autosuggest_engine: Any = None,
    ) -> None:
        """Wire the engine with its configuration and optional autosuggest handle.

        Args:
            config: Centralised configuration. Built from defaults when omitted.
            autosuggest_engine: An :class:`cli.autosuggest.AutoSuggestEngine` instance
                (or any object exposing ``refresh``, ``current``, ``enabled``).
        """
        self.config: TipsConfig = config or TipsConfig()
        self._autosuggest = autosuggest_engine
        self._state: EngagementState | None = None
        self._index: dict[str, Any] | None = None
        self._console: Console = Console(stderr=False, highlight=False, soft_wrap=True)
        self._last_tip_shown: str = ""
        self._session_tip_idx: int = -1
        self._killchain_counter: int = 0
        self._last_auto_phase: str = ""
        self.on_killchain_display = getattr(config, "killchain_display", None) or (lambda: None)

    @property
    def enabled(self) -> bool:
        """Whether the engine renders any output."""
        return self.config.enabled

    def set_enabled(self, value: bool) -> None:
        """Toggle rendering without dropping state."""
        self.config.enabled = bool(value)

    def render(self, cmd: str, phase: str = "") -> None:
        """Run all surfaces for the given command.

        Args:
            cmd: The command name that just executed (e.g. ``lazynmap``).
            phase: Current engagement phase (e.g. ``recon``) from payload.json.
        """
        if not self.config.enabled or not cmd:
            return
        first = (cmd or "").split()[0]
        if not first or first in SKIP_COMMANDS:
            return

        try:
            self._ensure_state_and_index()
            if not self._is_recordable_command(first):
                return
        except Exception:
            return

        resolved_phase = self._resolve_phase(first, phase)
        self._render_kill_chain_hints(first, resolved_phase)
        self._maybe_show_full_killchain(first)
        self._render_contextual_tip(first, resolved_phase)
        self._run_curiosity_reveal(first, resolved_phase)
        self._refresh_autosuggest(cmd, resolved_phase)
        self._update_engagement_state(first, resolved_phase)
        self._maybe_auto_show_killchain(resolved_phase)

    def _maybe_auto_show_killchain(self, phase: str) -> None:
        """Periodically re-surface the current phase without user prompt.

        Shows the unified kill-chain bar after every ``killchain_auto_every``
        commands and immediately whenever the active phase changes. Bounded
        by the injected display callable so the engine stays UI-agnostic.

        Args:
            phase: The resolved phase for the command that just executed.
        """
        if not self.config.enabled:
            return
        phase_changed = phase and phase != self._last_auto_phase
        every = int(self.config.killchain_auto_every or 0)
        self._killchain_counter += 1
        should_show = (every > 0 and self._killchain_counter % every == 0) or (
            phase_changed and self.config.killchain_auto_on_phase_change
        )
        if phase:
            self._last_auto_phase = phase
        if should_show:
            try:
                self.on_killchain_display()
            except Exception:
                pass

    def _resolve_phase(self, cmd: str, fallback: str) -> str:
        """Resolve the current engagement phase with progressive degradation.

        Priority: world_model.json > command_index lookup > past phases > fallback.
        Never returns \"recon\" once the operator has advanced beyond it.
        """
        wm_phase = self._read_world_model_phase()
        if wm_phase and wm_phase != "recon":
            return wm_phase

        index_phase = self._phase_for_cmd(cmd)
        if index_phase:
            return index_phase

        if self._state and self._state.phases_entered:
            recent_phases = self._state.phases_entered[-3:]
            higher = [p for p in recent_phases if p not in ("recon", "")]
            if higher:
                return higher[-1]
            return recent_phases[-1] or fallback or "recon"

        return fallback or "recon"

    def _read_world_model_phase(self) -> str:
        """Read the current phase from the unified killchain module."""
        try:
            from modules.killchain import KillChain as _KC
            wm_path = Path(self.config.sessions_dir) / "world_model.json"
            return _KC.current_phase(world_model_path=wm_path)
        except Exception:
            return ""

    def _read_os_id_from_session(self) -> str:
        """Read the detected OS identifier from sessions/os.json.

        Returns:
            ``"1"`` for Linux, ``"2"`` for Windows, ``""`` if unknown.
        """
        try:
            os_path = Path(self.config.sessions_dir) / "os.json"
            if os_path.exists():
                data = json.loads(os_path.read_text(encoding="utf-8"))
                if isinstance(data, list) and data:
                    os_name = (data[0].get("os") or "").lower()
                    if "linux" in os_name:
                        return "1"
                    elif "windows" in os_name:
                        return "2"
        except Exception:
            pass
        return ""

    def render_session_start(self, phase: str = "", os_id: str = "", **ctx: Any) -> None:
        """Print a single tip at session start (once per boot).

        Args:
            phase: Current engagement phase.
            os_id: Detected OS identifier (``"1"`` = Linux, ``"2"`` = Windows).
            **ctx: Additional context keys forwarded to tip triggers.
        """
        if not self.config.enabled:
            return
        context: dict[str, Any] = {"phase": phase, "os_id": os_id, **ctx}
        matched = [t for t in self.config.tips_registry if self._safe_tip_trigger(t, context)]
        if matched:
            tip = random.choice(matched)
            msg = f"[bold]tip:[/] {tip.get('text', '')}  [dim bold]→ {tip.get('command', '')}[/]"
        else:
            if self.config.session_tips:
                self._session_tip_idx = (self._session_tip_idx + 1) % len(self.config.session_tips)
                msg = f"[bold]tip:[/] {self.config.session_tips[self._session_tip_idx]}"
            else:
                return
        self._console.print(f"    {msg}")
        self._console.print()

    def get_state_snapshot(self) -> dict[str, Any]:
        """Return a read-only snapshot of current engagement state."""
        self._ensure_state_and_index()
        return {
            "elo": self._state.elo,
            "karma_name": self._get_karma_name(self._state.elo),
            "commands_seen": list(self._state.commands_seen),
            "phases_entered": list(self._state.phases_entered),
            "total_commands": self._state.total_commands,
            "session_commands": self._state.session_commands,
            "elo_session_delta": self._state.elo_session_delta,
            "next_reward_at": self._state.next_reward_at,
            "badges": list(self._state.badges),
        }

    def reset_session(self) -> None:
        """Reset session counters without clearing cross-session progress."""
        self._state = None
        self._ensure_state_and_index()

    def heal_commands_seen(self, known: set[str]) -> int:
        """Purge non-command entries from persisted ``commands_seen``."""
        try:
            self._ensure_state_and_index()
            before = len(self._state.commands_seen)
            self._state.commands_seen = self._sanitize_seen(self._state.commands_seen, known)
            removed = before - len(self._state.commands_seen)
            if removed:
                self._save_state()
            return removed
        except Exception:
            return 0

    # ── internal: kill-chain hints ──────────────────────────────────────────

    def _render_kill_chain_hints(self, cmd: str, phase: str) -> None:
        hints = self._compute_command_hints(cmd, phase)
        if not hints:
            return
        hint = Text()
        hint.append("  \u21b3 ", style="bold dim cyan")
        hint.append(" \u00b7 ".join(hints), style="dim white italic")
        self._console.print(hint)
        self._render_killchain_progress(phase)

    def _render_killchain_progress(self, current_phase: str) -> None:
        """Render a compact kill-chain progress bar."""
        from modules.killchain import KillChain as _KC
        _cfg = _KC.config()
        phases = _cfg.compact_phases
        labels = _cfg.compact_labels
        try:
            wm_phase_raw = self._read_world_model_phase()
            derived = wm_phase_raw if wm_phase_raw and wm_phase_raw != "recon" else ""
            active_phase = derived or (self._state.phases_entered[-1] if self._state and self._state.phases_entered else current_phase)
        except Exception:
            active_phase = current_phase
        progress = Text()
        progress.append("  [", style="dim")
        for i, p in enumerate(phases):
            label = labels.get(p, p[0].upper())
            if p == active_phase:
                progress.append(label, style="bold cyan")
            elif self._state and p in self._state.phases_entered:
                progress.append(label, style="green")
            else:
                progress.append(label, style="dim")
            if i < len(phases) - 1:
                progress.append(">", style="dim")
        progress.append("]", style="dim")
        self._console.print(progress)

    def _maybe_show_full_killchain(self, cmd: str) -> None:
        """Show the full killchain progress bar after high-impact commands."""
        if cmd not in _FULL_KILLCHAIN_TRIGGERS:
            return
        try:
            from cli.ops_commands import print_phase as _print_phase
            _print_phase()
        except Exception:
            pass

    def _compute_command_hints(self, cmd: str, phase: str) -> list[str]:
        already_run = self._read_run_commands()
        candidates: list[str] = []
        for c in self.config.kill_chain_next.get(cmd, []):
            if c not in already_run:
                candidates.append(c)
        phase_key = (phase or "recon").lower()
        if len(candidates) < self.config.hints_limit:
            for c in self.config.phase_priority.get(phase_key, []):
                if c not in already_run and c not in candidates and c != cmd:
                    candidates.append(c)
                if len(candidates) >= self.config.hints_limit * 2:
                    break
        return [
            self._truncate(c, HINT_MAX_LABEL)
            for c in candidates[: self.config.hints_limit]
        ]

    # ── internal: contextual tips ───────────────────────────────────────────

    def _render_contextual_tip(self, cmd: str, phase: str) -> None:
        context: dict[str, Any] = {
            "last_cmd": cmd,
            "phase": phase,
            "os_id": "",
            "rhost": "",
            "domain": "",
            "api_key": "",
        }
        try:
            payload = json.loads(Path(self.config.payload_path).read_text(encoding="utf-8"))
            context.update(
                {
                    "rhost": payload.get("rhost", ""),
                    "domain": payload.get("domain", ""),
                    "api_key": payload.get("api_key", ""),
                    "lhost": payload.get("lhost", ""),
                    "os_id": str(payload.get("os_id", "")),
                }
            )
        except Exception:
            pass

        if not context.get("os_id"):
            context["os_id"] = self._read_os_id_from_session()

        matched = [t for t in self.config.tips_registry if self._safe_tip_trigger(t, context)]
        if not matched:
            return
        tip = random.choice(matched)
        tip_key = tip.get("command", "")
        if tip_key == self._last_tip_shown:
            return
        self._last_tip_shown = tip_key

        t = Text()
        t.append("  \u2605 ", style="bold dim yellow")
        t.append(str(tip.get("text", ""))[:TIP_TEXT_MAX], style="dim white italic")
        t.append(f"  \u2192 {tip.get('command', '')}", style="bold dim cyan")
        self._console.print(t)

    @staticmethod
    def _safe_tip_trigger(tip: dict[str, Any], ctx: dict[str, Any]) -> bool:
        trigger = tip.get("trigger")
        if not callable(trigger):
            return False
        try:
            return trigger(ctx)
        except Exception:
            return False

    # ── internal: curiosity reveal ──────────────────────────────────────────

    def _run_curiosity_reveal(self, cmd: str, phase: str) -> None:
        try:
            phase_cmds = self._commands_in_exploration_phase(phase)
            seen_set = set(self._state.commands_seen)
            shown_set = set(self._state.session_curiosity_shown)
            normalized = f"do_{cmd}" if not cmd.startswith("do_") else cmd
            never_run = [
                c for c in phase_cmds
                if c not in seen_set and c not in shown_set and c != normalized and c != cmd
            ]
            if not never_run:
                return
            pick = random.choice(never_run)
            self._state.session_curiosity_shown.append(pick)
            label = pick.replace("do_", "")[:CURIOSITY_MAX_LABEL]
            summary = self._summary_for_exploration_cmd(pick)
            line = f"    \033[2;36m  explore:\033[0m \033[1;36m{label:<{CURIOSITY_MAX_LABEL}}\033[0m"
            if summary:
                line += f"  \033[2m{summary[:70]}\033[0m"
            print(line, flush=True)
        except Exception:
            pass

    def _commands_in_exploration_phase(self, phase: str) -> list[str]:
        if not self._index:
            return []
        ptc = self._index.get("phase_to_commands", {})
        return list(ptc.get(phase, []))

    def _summary_for_exploration_cmd(self, cmd: str) -> str:
        if not self._index:
            return ""
        normalized = cmd if cmd.startswith("do_") else f"do_{cmd}"
        cmds = self._index.get("commands", [])
        if isinstance(cmds, list):
            for entry in cmds:
                if isinstance(entry, dict) and entry.get("name") in (normalized, cmd):
                    return (entry.get("summary") or "")[:80]
        return ""

    # ── internal: autosuggest ───────────────────────────────────────────────

    def _refresh_autosuggest(self, cmd: str, phase: str) -> None:
        engine = self._autosuggest
        if engine is None:
            return
        try:
            if not engine.enabled:
                return
            from cli.autosuggest import SuggestionContext

            context = SuggestionContext(
                last_command=cmd,
                phase=phase,
                recent_commands=self._read_recent_commands_for_autosuggest(),
                target="",
                os_hint="unknown",
            )
            engine.refresh(context)
            suggestion = engine.current()
            if suggestion is None:
                return
            self._render_autosuggest_hint(engine)
        except Exception:
            pass

    def _render_autosuggest_hint(self, engine: Any) -> None:
        try:
            from cli.autosuggest import format_hint_line

            suggestion = engine.current()
            if suggestion is None:
                return
            text = format_hint_line(suggestion)
            self._console.print(f"[dim cyan]  >> [/dim cyan][dim white italic]{text}[/dim white italic]")
        except Exception:
            pass

    # ── internal: engagement state + ELO + VRI ──────────────────────────────

    def _update_engagement_state(self, cmd: str, phase: str) -> None:
        normalized = f"do_{cmd}" if not cmd.startswith("do_") else cmd
        first_time = normalized not in self._state.commands_seen

        self._state.total_commands += 1
        self._state.session_commands += 1
        self._state.last_cmd = cmd

        if first_time:
            self._state.commands_seen.append(normalized)

        current_phase = self._phase_for_cmd(cmd)
        resolved_phase = current_phase or phase
        new_phase = bool(resolved_phase) and resolved_phase not in self._state.phases_entered
        if new_phase:
            self._state.phases_entered.append(resolved_phase)

        elo_delta = self._award_elo(cmd, first_time, new_phase, resolved_phase)
        self._state.elo += elo_delta
        self._state.elo_session_delta += elo_delta
        self._sync_user_elo(elo_delta)
        self._check_badges(cmd, first_time)

        self._check_karma_up()

        if self._state.total_commands >= self._state.next_reward_at:
            total_in_index = sum(len(v) for v in (self._index or {}).get("phase_to_commands", {}).values())
            ctx: dict[str, Any] = {
                "session_commands": self._state.session_commands,
                "total_seen": len(self._state.commands_seen),
                "total_commands_in_index": max(total_in_index, 1),
                "current_phase": resolved_phase,
                "rewards_given": list(self._state.rewards_given[-20:]),
                "elo": self._state.elo,
                "karma_name": self._get_karma_name(self._state.elo),
                "elo_session_delta": self._state.elo_session_delta,
            }
            self._fire_vri_reward(ctx)

        self._save_state()

    def _award_elo(self, cmd: str, first_time: bool, new_phase: bool, phase: str) -> int:
        delta = self.config.elo_base
        key = cmd.replace("do_", "")
        delta += self.config.high_value_cmds.get(key, 0)
        delta += self.config.phase_bonus.get((phase or "").lower(), 0)
        if first_time:
            delta += self.config.elo_first_time_bonus
        if new_phase:
            delta += self.config.elo_new_phase_bonus
        return delta

    def _check_karma_up(self) -> None:
        new_karma = self._get_karma_name(self._state.elo)
        if new_karma == self._state.last_karma_name:
            return
        old = self._state.last_karma_name
        self._state.last_karma_name = new_karma
        self._console.print()
        self._console.print(f"    \033[2m{'─' * 60}\033[0m")
        self._console.print(
            f"    \033[1;33m  KARMA UP  \033[0m\033[2m{old}\033[0m\033[1;33m → "
            f"\033[0m\033[1;32m{new_karma}\033[0m\033[2m  ({self._state.elo} ELO)\033[0m",
        )
        self._console.print(f"    \033[2m{'─' * 60}\033[0m")
        self._console.print()

    def _check_badges(self, cmd: str, first_time: bool) -> None:
        badges = self._state.badges
        if first_time and len(self._state.commands_seen) >= 100 and "arsenal_master" not in badges:
            badges.append("arsenal_master")
            self._print_badge("Arsenal Master", "Discovered 100+ unique commands")
        if (
            cmd.lower() in {"auto_pwn", "chain", "hunt"}
            and "chain_reaction" not in badges
            and any(c.lower().startswith("chain ") or c == "chain" for c in (self._state.commands_seen or []))
        ):
            badges.append("chain_reaction")
            self._print_badge("Chain Reaction", "Executed chain + hunt + auto_pwn in sequence")
        if self._state.session_commands >= 50 and "deep_recon" not in badges:
            badges.append("deep_recon")
            self._print_badge("Deep Recon", "50+ commands in a single session")
        if cmd.lower() in {"linpeas", "winpeas", "crystal_ball"} and "first_owned" not in badges:
            try:
                wm_path = Path(self.config.sessions_dir) / "world_model.json"
                if wm_path.exists():
                    wm = json.loads(wm_path.read_text(encoding="utf-8"))
                    hosts = wm.get("hosts", {})
                    if any(isinstance(h, dict) and h.get("state") == "owned" for h in hosts.values()):
                        badges.append("first_owned")
                        self._print_badge("First Owned", "Achieved root/System on a target host")
            except Exception:
                pass

    def _print_badge(self, name: str, description: str) -> None:
        self._console.print()
        self._console.print(f"    \033[2m{'─' * 40}\033[0m")
        self._console.print(f"    \033[1;35m  BADGE UNLOCKED  \033[0m\033[1;37m{name}\033[0m")
        self._console.print(f"    \033[2m  {description}\033[0m")
        self._console.print(f"    \033[2m{'─' * 40}\033[0m")
        self._console.print()

    def _fire_vri_reward(self, ctx: dict[str, Any]) -> None:
        rewards = list(self.config.vri_rewards) if self.config.vri_rewards else _DEFAULT_VRI_REWARDS
        weights = [r.get("weight", 1) for r in rewards]
        self._console.print()
        self._console.print(f"    \033[2m{'─' * 60}\033[0m")
        rendered = False
        chosen_id = ""
        tried: set[str] = set()
        for _ in range(VRI_RETRY_LIMIT):
            reward = random.choices(rewards, weights=weights, k=1)[0]
            if reward["id"] in tried:
                continue
            tried.add(reward["id"])
            try:
                if reward["render"](ctx, state=self._state, config=self.config):
                    rendered = True
                    chosen_id = reward["id"]
                    break
            except Exception:
                continue
        if not rendered:
            _render_streak(ctx, state=self._state, config=self.config)
            chosen_id = "streak"
        self._console.print(f"    \033[2m{'─' * 60}\033[0m")
        self._console.print()
        if chosen_id:
            self._state.rewards_given.append(chosen_id)
        self._state.next_reward_at = self._next_threshold(self._state.total_commands)

    # ── helpers ─────────────────────────────────────────────────────────────

    def _ensure_state_and_index(self) -> None:
        if self._state is None:
            self._state = self._load_state()
        if self._index is None:
            self._index = self._load_command_index()

    def _load_state(self) -> EngagementState:
        state_path = Path(self.config.sessions_dir) / "engagement_state.json"
        try:
            if state_path.exists():
                raw = json.loads(state_path.read_text(encoding="utf-8"))
                st = EngagementState(**{k: v for k, v in raw.items() if k in EngagementState.__dataclass_fields__})
                st.session_commands = 0
                st.session_curiosity_shown = []
                st.session_start_ts = time.time()
                st.elo_session_delta = 0
                st.commands_seen = self._sanitize_seen(st.commands_seen)
                if not hasattr(st, "badges") or not isinstance(st.badges, list):
                    st.badges = []
                return st
        except Exception:
            pass
        state = EngagementState()
        state.next_reward_at = self._next_threshold(0)
        return state

    def _save_state(self) -> None:
        try:
            state_path = Path(self.config.sessions_dir) / "engagement_state.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = state_path.with_suffix(".tmp")
            data = {
                "total_commands": self._state.total_commands,
                "session_commands": self._state.session_commands,
                "commands_seen": self._state.commands_seen,
                "phases_entered": self._state.phases_entered,
                "rewards_given": self._state.rewards_given,
                "session_curiosity_shown": self._state.session_curiosity_shown,
                "next_reward_at": self._state.next_reward_at,
                "session_start_ts": self._state.session_start_ts,
                "last_cmd": self._state.last_cmd,
                "elo": self._state.elo,
                "last_karma_name": self._state.last_karma_name,
                "elo_session_delta": self._state.elo_session_delta,
                "badges": self._state.badges,
            }
            tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
            tmp.replace(state_path)
        except Exception:
            pass

    def _load_command_index(self) -> dict[str, Any]:
        try:
            return json.loads(Path(self.config.command_index_path).read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _is_recordable_command(self, cmd: str) -> bool:
        normalized = cmd if cmd.startswith("do_") else f"do_{cmd}"
        return bool(COMMAND_NAME_RE.match(normalized))

    def _sanitize_seen(self, names: list[str], known: set[str] | None = None) -> list[str]:
        out: list[str] = []
        seen: set[str] = set()
        for name in names:
            if not isinstance(name, str) or name in seen:
                continue
            if not self._is_recordable_command(name):
                continue
            if known is not None and (name if name.startswith("do_") else f"do_{name}") not in known:
                continue
            seen.add(name)
            out.append(name)
        return out

    def _read_run_commands(self) -> set[str]:
        path = Path(self.config.sessions_dir) / "LazyOwn_session_report.csv"
        seen: set[str] = set()
        if not path.exists():
            return seen
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    for col in ("tool", "command", "name"):
                        val = (row.get(col) or "").strip().split()[0]
                        if val:
                            seen.add(val)
                            break
        except Exception:
            pass
        return seen

    def _read_recent_commands_for_autosuggest(self, limit: int = 5) -> list:
        path = Path(self.config.sessions_dir) / "LazyOwn_session_report.csv"
        if not path.exists():
            return []
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as fh:
                rows = list(csv.DictReader(fh))
            verbs: list[str] = []
            for row in rows[-limit:]:
                for col in ("command", "tool", "name"):
                    val = (row.get(col) or "").strip().split()
                    if val:
                        verbs.append(val[0])
                        break
            return verbs
        except Exception:
            return []

    def _phase_for_cmd(self, cmd: str) -> str:
        if not self._index:
            return ""
        ptc = self._index.get("phase_to_commands", {})
        normalized = f"do_{cmd}" if not cmd.startswith("do_") else cmd
        for p, cmds in ptc.items():
            if normalized in cmds or cmd in cmds:
                return p
        return ""

    @staticmethod
    def _truncate(value: str, max_len: int) -> str:
        if len(value) <= max_len:
            return value
        return value[: max_len - 1] + "\u2026"

    @staticmethod
    def _get_karma_name(elo: int) -> str:
        for threshold, label in KARMA_THRESHOLDS:
            if elo < threshold:
                return label
        return KARMA_TOP

    def _next_threshold(self, current: int) -> int:
        gap = max(2, int(round(-self.config.mean_interval * math.log(max(random.random(), 1e-9)))))
        return current + gap

    def _sync_user_elo(self, delta: int) -> bool:
        if delta <= 0:
            return False
        target: str | None = None
        try:
            from modules.cli_auth import get_current_operator
            target = get_current_operator()
        except ImportError:
            pass
        if not target:
            try:
                payload = json.loads(Path(self.config.payload_path).read_text(encoding="utf-8"))
                target = payload.get("c2_user")
            except Exception:
                pass
        if not target:
            return False
        try:
            from modules.lazy_rbac import get_rbac_store
            store = get_rbac_store()
            user = store.find_by_username(target)
            if user:
                user.elo = int(user.elo or 0) + int(delta)
                store.save(user)
                return True
        except ImportError:
            pass
        users_path = Path(self.config.users_path)
        if not users_path.exists():
            return False
        try:
            users = json.loads(users_path.read_text(encoding="utf-8"))
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
            tmp = users_path.with_suffix(".tmp")
            tmp.write_text(json.dumps(users, indent=4), encoding="utf-8")
            tmp.replace(users_path)
            return True
        except Exception:
            return False


def _render_streak(
    ctx: dict[str, Any],
    state: EngagementState | None = None,
    config: TipsConfig | None = None,
) -> bool:
    n = ctx.get("session_commands", 0) if ctx else 0
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
    elo_val = ctx.get("elo", 0)
    karma_tail = f"  \033[2m· \033[0m\033[1;33m{karma}\033[0m\033[2m {elo_val} ELO\033[0m" if karma else ""
    print(
        f"    \033[2m  {n} commands this session \033[0m\033[1;32m{label}\033[0m{karma_tail}",
        flush=True,
    )
    return True


def _render_exploration(
    ctx: dict[str, Any],
    state: EngagementState | None = None,
    config: TipsConfig | None = None,
) -> bool:
    seen = ctx.get("total_seen", 0)
    total = ctx.get("total_commands_in_index", 1)
    pct = min(100, round(100 * seen / total, 1))
    bar_len = 20
    filled = int(bar_len * pct / 100)
    bar = "\u2588" * filled + "\u2591" * (bar_len - filled)
    print(
        f"    \033[2m  arsenal explored  \033[0m\033[36m{bar}\033[0m\033[1m  {pct}%\033[0m\033[2m  ({seen}/{total} commands)\033[0m",
        flush=True,
    )
    return True


def _render_phase_badge(
    ctx: dict[str, Any],
    state: EngagementState | None = None,
    config: TipsConfig | None = None,
) -> bool:
    _PHASE_LABEL: dict[str, str] = {
        "recon": "Reconnaissance",
        "enum": "Enumeration",
        "exploit": "Exploitation",
        "privesc": "Privilege Escalation",
        "lateral": "Lateral Movement",
        "cred": "Credential Access",
        "postexp": "Post-Exploitation",
        "exfil": "Exfiltration",
        "c2": "Command & Control",
    }
    phase = (ctx.get("current_phase") if ctx else "").lower()
    if not phase:
        return False
    label = _PHASE_LABEL.get(phase, phase.title())
    print(
        f"    \033[2m  phase \033[0m\033[1;37;41m {label} \033[0m\033[2m  — run \033[0m\033[1;36mpalette {phase}\033[0m\033[2m to see all commands in this stage\033[0m",
        flush=True,
    )
    return True


def _render_hidden_feature(
    ctx: dict[str, Any],
    state: EngagementState | None = None,
    config: TipsConfig | None = None,
) -> bool:
    features = list(config.hidden_features) if config and config.hidden_features else _DEFAULT_HIDDEN_FEATURES
    rewards_given = ctx.get("rewards_given", []) if ctx else []
    candidates = [f for f in features if f[0] not in rewards_given]
    if not candidates:
        candidates = features
    if not candidates:
        return False
    cmd_label, description = random.choice(candidates)
    print(
        f"    \033[2m  hidden feature  \033[0m\033[1;35m{cmd_label:<30}\033[0m\033[2m{description}\033[0m",
        flush=True,
    )
    return True


def _render_arsenal_tip(
    ctx: dict[str, Any],
    state: EngagementState | None = None,
    config: TipsConfig | None = None,
) -> bool:
    tips = list(config.arsenal_tips) if config and config.arsenal_tips else _DEFAULT_ARSENAL_TIPS
    if not tips:
        return False
    tip = random.choice(tips)
    print(f"    \033[2m  tip  {tip}\033[0m", flush=True)
    return True


_DEFAULT_HIDDEN_FEATURES: list[tuple[str, str]] = [
    ("auto_pwn <target>", "Full autonomous exploitation from recon to shell"),
    ("chain <target>", "Map nmap services to exploit chain via CVE database"),
    ("hunt <target>", "Profile target and auto-exploit top-ranked candidates"),
    ("nuclei <url>", "Run Nuclei vulnerability scanner with all templates"),
    ("yara_scan <path>", "Scan filesystem for malware with YARA rules"),
    ("yara_marketplace", "Browse and install community YARA rules"),
    ("nuclei_marketplace", "Browse and install community Nuclei templates"),
    ("campaign new <name>", "Start a tracked campaign with milestones"),
    ("collab_join", "Join multi-operator real-time collaboration session"),
    ("dashboard", "Full-screen Textual TUI with live engagement stats"),
    ("marketplace config", "Interactive curses wizard for addons, plugins, tools"),
    ("playbook_generate", "Generate attack playbook from nmap scan"),
    ("palette recon", "Browse every recon command grouped by kill-chain phase"),
    ("encrypt", "Encrypt sensitive session data at rest"),
    ("decrypt", "Decrypt session data to resume operations"),
]

_DEFAULT_ARSENAL_TIPS: list[str] = [
    "Run 'auto_pwn <target>' for fully autonomous exploitation.",
    "'chain <target>' builds an exploit chain from your nmap scan.",
    "Use 'hunt <target>' to exploit the most promising vulnerability first.",
    "'nuclei <url>' runs all Nuclei templates against a web target.",
    "Scan for malware with 'yara_scan <path>'. Browse rules with 'yara_marketplace'.",
    "Browse Nuclei templates: 'nuclei_marketplace search --severity critical'.",
    "Start a tracked campaign: 'campaign new <name> --scope 10.0.0.0/24'.",
    "Collaborate in real-time: 'collab_join' shares your session with the team.",
    "Protect your operation: 'encrypt' locks all sensitive session data.",
    "Dashboard shows live topology: 'dashboard' opens the TUI.",
    "Install community addons: 'marketplace install <name>'.",
    "'form <cmd>' opens an interactive guided form for complex commands.",
    "Press Tab after a partial command for fuzzy completion.",
    "'palette <phase>' filters commands to one kill-chain stage.",
    "'sitrep' prints a unified operational picture in one view.",
]

_DEFAULT_VRI_REWARDS: list[dict[str, Any]] = [
    {"id": "streak", "weight": 3, "render": _render_streak},
    {"id": "exploration_pct", "weight": 2, "render": _render_exploration},
    {"id": "phase_badge", "weight": 2, "render": _render_phase_badge},
    {"id": "hidden_feature", "weight": 2, "render": _render_hidden_feature},
    {"id": "arsenal_tip", "weight": 1, "render": _render_arsenal_tip},
]


def build_default_tips_config() -> TipsConfig:
    """Build a :class:`TipsConfig` populated from the live framework tables.

    Returns:
        A ready-to-use config wired to the static kill-chain tables, ELO
        tables, and tip registries that ship with the framework.
    """
    from cli.reactive_hints import _KILL_CHAIN_NEXT, _PHASE_PRIORITY

    high_value_cmds: dict[str, int] = {
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
        "juicypotato": 20,
        "sudo_privesc": 20,
        "whoami_priv": 10,
        "crystal_ball": 18,
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
        "auto_pwn": 30,
        "chain": 20,
        "hunt": 25,
        "nuclei": 18,
        "yara_scan": 15,
    }

    phase_bonus: dict[str, int] = {
        "recon": 5,
        "enum": 8,
        "exploit": 25,
        "cred": 20,
        "privesc": 30,
        "lateral": 25,
        "postexp": 15,
        "exfil": 20,
        "c2": 12,
    }

    return TipsConfig(
        kill_chain_next=_KILL_CHAIN_NEXT,
        phase_priority=_PHASE_PRIORITY,
        high_value_cmds=high_value_cmds,
        phase_bonus=phase_bonus,
        vri_rewards=list(_DEFAULT_VRI_REWARDS),
        hidden_features=list(_DEFAULT_HIDDEN_FEATURES),
        arsenal_tips=list(_DEFAULT_ARSENAL_TIPS),
        session_tips=[
            "Run [bold]sitrep[/] at the start of every shift for a unified operational picture.",
            "Use [bold]auto_pwn <target>[/] for fully-automated exploitation after recon.",
            "Use [bold]chain <target>[/] to build an exploit chain from your nmap scan.",
            "Use [bold]hunt <target>[/] to auto-exploit the top-ranked vulnerability.",
            "Use [bold]nuclei <url>[/] to run vulnerability templates against a web host.",
            "Use [bold]yara_marketplace[/] to browse and install community malware rules.",
            "Use [bold]encrypt[/] to lock sensitive session data when you step away.",
            "Use [bold]collab_join[/] to work with your team in real time.",
            "Use [bold]dashboard[/] for a live Textual TUI with topology and stats.",
            "Use [bold]marketplace config[/] to browse and enable 76+ YAML addons.",
        ],
    )


__all__ = [
    "TipsEngine",
    "TipsConfig",
    "EngagementState",
    "SKIP_COMMANDS",
    "build_default_tips_config",
]
