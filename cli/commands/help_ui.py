"""Help, tutorial and phase guidance extracted from the miscellaneous cluster.

Pending status: originals deleted from ``cli/commands/misc_migrated.py``;
this set is registered by ``cli.registry``.
"""

from __future__ import annotations

import shlex

import cmd2
from rich.table import Table as _Table

from cli.aliases import load_aliases as _load_aliases
from cli.assign import apply_assign as _apply_assign
from cli.commands._base import LazyOwnCommandSet
from cli.ops_commands import PHASES as _PHASES
from cli.ops_commands import print_ctx as _print_ctx
from cli.ops_commands import print_phase as _print_phase
from cli.ops_commands import tgrep as _tgrep
from cli.ops_commands import write_phase as _write_phase
from cli.wizard import run as _run_wizard
from core.config import save_payload as _save_payload
from utils import print_error, print_msg, print_warn

__all__ = ["HelpUiCommandSet"]


class HelpUiCommandSet(LazyOwnCommandSet):
    """Help, tutorial and phase guidance."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_wizard(self, line):
        """Guided first-run setup wizard — configure rhost, lhost, domain, wordlists and more.

        Walks the operator through the seven essential configuration values with
        auto-detection (lhost from routing table, wordlist paths from SecLists),
        live ping validation for rhost, and a readiness summary at the end.

        Usage:
            ``wizard``            — start interactive setup
            ``wizard --tutorial`` — extended help text for first-time operators
            ``wizard --check``    — show readiness summary only, no prompts
            ``wizard --quick``    — auto-detect defaults without any prompts
            ``wizard --non-interactive [--rhost X] [--lhost Y] [--domain Z]``
                                  — apply values without prompting (Docker/CI)

        Both novice and experienced operators can use this:
        - Novices: step-by-step prompts with clear descriptions; pass
          ``--tutorial`` for in-depth explanations of every field.
        - Experts: press Enter to accept auto-detected values; Ctrl-C to abort.
        """
        tokens = shlex.split(line or "")
        check_only = "--check" in tokens
        tutorial = "--tutorial" in tokens or "-t" in tokens
        non_interactive = "--non-interactive" in tokens
        quick = "--quick" in tokens

        def _save(key, value):
            _apply_assign(self.params, key, value, save=_save_payload)
            try:
                self.aliases.update(_load_aliases(self.params))
            except Exception:
                pass

        if check_only:
            from cli.wizard import _build_readiness, _print_readiness, _print_validation_summary
            items = _build_readiness(self.params)
            _print_readiness(items)
            _print_validation_summary(self.params)
            return

        if non_interactive:
            from cli.wizard import run_non_interactive as _run_wizard_ni
            values: dict = {}
            flag_names = ("rhost", "lhost", "domain", "device", "os_id", "api_key")
            for index, token in enumerate(tokens):
                flag = token.lstrip("-")
                if token.startswith("--") and flag in flag_names and index + 1 < len(tokens):
                    values[flag] = tokens[index + 1]
            result = _run_wizard_ni(self.params, save=_save, values=values)
            if result and result.saved:
                print_msg("wizard (non-interactive) applied — run 'sitrep' to review.")
            return

        if quick:
            from cli.wizard import run_non_interactive as _run_wizard_ni
            _run_wizard_ni(self.params, save=_save, values={})
            print_msg("wizard (quick) auto-detected defaults — run 'doctor' to verify, then 'sitrep'.")
            return

        result = _run_wizard(self.params, save=_save, tutorial=tutorial)
        if result and result.saved:
            from rich.console import Console as _Console
            _c = _Console(highlight=False, soft_wrap=True)
            _c.print()
            _c.rule("[bold green]Setup complete — suggested next steps[/]")
            _c.print("  [bold cyan]sitrep[/]                    confirm your configuration at a glance")
            _c.print("  [bold cyan]lazynmap[/]                  full port scan of the target")
            _c.print("  [bold cyan]palette recon[/]             browse all recon commands")
            _c.print("  [bold cyan]recommend_next[/]            AI-powered command suggestion")
            _c.rule()
            _c.print()

    @cmd2.with_category("12. Miscellaneous")
    def do_tutorial(self, line):
        """Interactive tutorial that walks you through the golden path.

        Guides a new operator step-by-step through:
            ping -> lazynmap -> auto_populate -> facts_show -> recommend_next

        Usage:
            ``tutorial``         — run the tutorial (skips if already completed)
            ``tutorial --force`` — replay even if already completed
        """
        from cli.tutorial import run as _run_tutorial
        tokens = shlex.split(line or "")
        force = "--force" in tokens
        try:
            _run_tutorial(
                params=self.params,
                command_runner=self.one_cmd,
                force=force,
            )
        except Exception as exc:
            print_error(f"tutorial failed: {exc}")

    @cmd2.with_category("12. Miscellaneous")
    def do_help_phase(self, line):
        """List all commands for a given kill-chain phase.

        Usage:
            ``help_phase recon``       — list recon commands
            ``help_phase exploit``     — list exploit commands
            ``help_phase``             — list all available phases

        Available phases: recon, enum, exploit, postexp, persist, privesc,
        cred, lateral, exfil, c2, report, misc.
        """
        from cli.contextual_help import PHASE_LABELS, ContextualHelp
        ch = ContextualHelp(aliases=self.aliases, params=self.params)
        phase = (line or "").strip().lower()

        if not phase:
            table = _Table(title="Kill-chain phases", show_header=True, header_style="bold")
            table.add_column("Phase", style="green")
            table.add_column("Label")
            for p, label in PHASE_LABELS.items():
                table.add_row(p, label)
            from rich.console import Console as _C
            _C(highlight=False, soft_wrap=True).print(table)
            return

        if phase not in PHASE_LABELS:
            print_error(f"Unknown phase '{phase}'. Valid: {', '.join(PHASE_LABELS)}")
            return
        ch.render_phase_commands(phase)

    @cmd2.with_category("12. Miscellaneous")
    def do_help_status(self, line):
        """Show which session requirements are met (rhost, creds, domain, OS).

        Useful to quickly check what is configured before running a command.

        Usage: ``help_status``
        """
        from cli.contextual_help import ContextualHelp
        ch = ContextualHelp(aliases=self.aliases, params=self.params)
        ch.render_requirements_status()

    @cmd2.with_category("12. Miscellaneous")
    def do_ctx_help(self, line):
        """Show contextual help for a command: description, phase, requirements, tips.

        Unlike plain 'help', this shows whether the command needs rhost,
        credentials, or domain, and gives phase-specific tips.

        Usage:
            ``ctx_help lazynmap``     — contextual help for lazynmap
            ``ctx_help evil``         — contextual help for evil-winrm
        """
        from cli.contextual_help import ContextualHelp
        cmd_name = (line or "").strip()
        if not cmd_name:
            print_warn("Usage: ctx_help <command>")
            return
        ch = ContextualHelp(aliases=self.aliases, params=self.params)
        if not ch.render_command_help(cmd_name):
            print_error(f"Command '{cmd_name}' not found in the index.")

    @cmd2.with_category("12. Miscellaneous")
    def do_ctx(self, line):
        """Print a single-line operator context: rhost, lhost, domain, phase, os, creds.

        No arguments. Reads payload.json and sessions/world_model.json. Fast —
        suitable to run between every command for situational awareness.

        Usage:
            ``ctx``
        """
        _print_ctx(self.params)

    @cmd2.with_category("12. Miscellaneous")
    def do_command_explorer(self, line):
        """Interactive command explorer organized by goals and phases.

        Browse commands by what you want to accomplish, not by category.
        Shows command names, descriptions, and aliases for quick discovery.

        Usage:
            ``command_explorer``            — show all goals
            ``command_explorer web``        — show web-related commands
            ``command_explorer smb_windows`` — show SMB/Windows commands
            ``command_explorer search nmap`` — search commands by keyword
        """
        from cli.command_explorer import GOALS, CommandExplorer
        explorer = CommandExplorer(aliases=self.aliases, params=self.params)
        args = (line or "").strip().split()

        if not args:
            explorer.render_goals_overview()
            return

        query = args[0].lower()
        if query in ("search", "find", "s", "grep"):
            if len(args) < 2:
                print_warn("Usage: explore search <keyword>")
                return
            explorer.render_search(" ".join(args[1:]))
        elif query in GOALS:
            explorer.render_goal_commands(query)
        else:
            explorer.render_search(query)

    @cmd2.with_category("12. Miscellaneous")
    def do_config_status(self, line):
        """Show configuration status grouped by category with set/missing indicators.

        Replaces the raw 'get' (payload.json dump) with a human-friendly
        overview showing which fields are configured, which need attention,
        and how to set them.

        Usage:
            ``config_status``           — full grouped status
            ``config_status --quick``   — show only missing required fields
        """
        from cli.config_status import ConfigStatus
        tokens = shlex.split(line or "")
        status = ConfigStatus(params=self.params)
        if "--quick" in tokens:
            status.render_quick_check()
        else:
            status.render_status()

    @cmd2.with_category("12. Miscellaneous")
    def do_tui_theme(self, line):
        """Switch the TUI colour theme used by the splash and styled output.

        Themes change the accent palette of LazyOwn's rich output (the
        first-run splash overlay and any semantic styled panels). The
        selection persists to ``payload.json`` under ``tui_theme`` so it
        survives shell restarts.

        Usage:
            ``tui_theme``          — list available themes, mark the active one
            ``tui_theme <name>``   — switch to a named theme (case-insensitive)
            ``tui_theme cycle``    — advance to the next theme in order
            ``tui_theme prev``     — step back to the previous theme
            ``tui_theme reset``    — return to the default theme
        """
        from cli.tui_theme import run as _run_tui_theme
        args = (line or "").split()
        try:
            result = _run_tui_theme(args, self.params, _save_payload)
        except Exception as exc:
            print_error(f"tui_theme failed: {exc}")
            return
        print_msg(result)

    @cmd2.with_category("12. Miscellaneous")
    def do_doctor(self, line):
        """Preflight environment health check — verify the install is ready.

        Complements ``wizard``. Where ``wizard --check`` validates your
        configuration (payload.json values), ``doctor`` validates the
        installation itself: Python version, active virtual environment,
        importability of the third-party packages install.sh provisions, the
        C2 TLS certificates, payload.json, SecLists, and external kill-chain
        tooling.

        Usage:
            ``doctor``       — run every check and print a status table
            ``doctor --fix`` — interactively offer to install missing packages
            ``doctor -y``    — auto-fix all issues without prompting

        Blocking failures (missing required packages, payload.json, or an
        unsupported Python) are highlighted in red; warnings cover optional
        features that will simply be skipped at runtime.
        """
        from pathlib import Path as _Path

        from cli.doctor import fix_report, gather_report, render_report

        root = _Path(__file__).resolve().parent
        args = line.strip().split()
        auto_yes = "-y" in args or "--yes" in args
        do_fix = "--fix" in args or auto_yes

        report = gather_report(root)
        render_report(report)

        if do_fix:
            fix_report(report, root=root, auto_yes=auto_yes)

    @cmd2.with_category("12. Miscellaneous")
    def do_karma(self, line):
        """Show ELO score, karma rank and exploration progress for this operator.

        Reads ``sessions/engagement_state.json`` (curiosity + VRI engine) and
        prints the operator's ELO, karma name (Noob → Godlike), commands
        discovered, phases entered, and steps remaining until the next VRI
        reward.  Useful to gauge progress on the curiosity-driven adoption
        loop without re-running another command.

        Usage:
            ``karma``
        """
        try:
            from cli.engagement_hooks import get_state_snapshot
            snap = get_state_snapshot()
        except Exception as exc:
            print_error(f"engagement state unavailable: {exc}")
            return
        elo = snap.get("elo", 0)
        karma = snap.get("karma_name", "Noob")
        seen = len(snap.get("commands_seen", []))
        phases = snap.get("phases_entered", [])
        total = snap.get("total_commands", 0)
        session = snap.get("session_commands", 0)
        delta = snap.get("elo_session_delta", 0)
        next_at = snap.get("next_reward_at", 0)
        gap = max(0, next_at - total)
        print(f"  \033[1;33mKarma\033[0m   {karma}  \033[2m({elo} ELO, +{delta} this session)\033[0m")
        print(f"  \033[1;36mUsage\033[0m   {total} total · {session} this session")
        print(f"  \033[1;35mArsenal\033[0m {seen} commands discovered")
        print(f"  \033[1;32mPhases\033[0m  {', '.join(phases) if phases else '—'}")
        print(f"  \033[2mNext reward in ~{gap} command(s)\033[0m")

    @cmd2.with_category("12. Miscellaneous")
    def do_tgrep(self, line):
        """Search across all previous command outputs and session logs.

        Searches in: sessions/_cli_transcript.jsonl (full outputs),
        sessions/LazyOwn_session_report.csv (command list), and
        sessions/logs/*.txt (tool output files). Useful for recalling
        credentials, open ports, or any string from earlier in the session.

        Usage:
            ``tgrep <pattern>``
            ``tgrep password``
            ``tgrep '10\\.10\\.11'``
            ``tgrep Administrator``
        """
        _tgrep((line or "").strip())

    @cmd2.with_category("12. Miscellaneous")
    def do_phase(self, line):
        """Get or set the current kill-chain phase.

        When called without arguments, shows the current phase and the
        full kill-chain progress bar. When called with a phase name,
        updates sessions/world_model.json — the dashboard reflects the
        change on its next refresh (within 5 s).

        Valid phases: recon scan enum exploit privesc lateral exfil report

        Usage:
            ``phase``               — show current phase and progress bar
            ``phase exploit``       — move to exploit phase
            ``phase privesc``       — advance to privilege escalation

        The phase drives the inline hints and the kill-chain panel in the
        operator dashboard. Advancing a phase also marks the previous one
        as completed in the dashboard progress bar.
        """
        arg = (line or "").strip().lower()
        if not arg:
            _print_phase()
            return
        if arg not in _PHASES:
            valid = ", ".join(_PHASES)
            print_error(f"Unknown phase: {arg!r}  valid phases: {valid}")
            return
        ok = _write_phase(arg)
        if ok:
            print_msg(f"Phase set to {arg.upper()}  — dashboard will update within 5 s")
        else:
            print_error("Failed to write phase to sessions/world_model.json")

    @cmd2.with_category("12. Miscellaneous")
    def do_killchain(self, line):
        """Show the unified kill-chain progress and control auto-refresh.

        Displays every kill-chain phase with its status derived from the
        WorldModel (the single source of truth), plus the operator-set
        override when it differs.

        A compact progress bar can also be surfaced automatically after
        commands. Use ``killchain auto on|off|N`` to enable it every N
        commands, or set the phase-change trigger that fires whenever the
        active phase advances.

        Usage:
            ``killchain``            — show unified kill-chain progress bar
            ``killchain auto on``    — show bar periodically after commands
            ``killchain auto off``   — disable auto-refresh
            ``killchain auto 5``     — show bar every 5 commands
        """
        arg = (line or "").strip()
        if arg.lower().startswith("auto"):
            self._handle_killchain_auto(arg[len("auto"):])
            return
        _print_phase()
        try:
            from modules.world_model import get_world_model
            wm = get_world_model()
            ctx = wm.to_context_string()
            print(ctx, flush=True)
        except Exception:
            pass

