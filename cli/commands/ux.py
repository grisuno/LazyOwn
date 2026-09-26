"""Usability commands: hud, undo, config_diff, cheat, suggest.

These commands close the highest-impact UX gaps without touching the
legacy shell: a one-glance session HUD, configuration undo and diff,
an in-shell cheatsheet renderer, and fuzzy typo correction. All data
helpers live in their own contracts; this set only wires them to cmd2.
"""

from __future__ import annotations

import shlex
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import print_error, print_msg, print_warn

_CHEAT_PATH = Path(__file__).resolve().parent.parent.parent / "CHEATSHEET.md"

_CHEAT_SECTIONS: tuple[str, ...] = (
    "configuration",
    "recon",
    "web",
    "dns",
    "smb",
    "exploit",
    "privesc",
    "lateral",
    "marketplace",
    "autonomous",
    "c2",
    "report",
    "ai",
    "security",
)


class UxCommandSet(LazyOwnCommandSet):
    """Session HUD, config undo, cheatsheet and fuzzy suggestion."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_hud(self, line):
        """Session counters: elapsed time, commands run, material captured.

        Complements rather than repeats the other commands. ``killchain``
        owns the kill-chain phases, the status bar already shows target and
        phase, and ``sitrep`` owns the full picture. This shows only what
        nothing else reports: how long this session has run, how many
        commands it executed, and how many credentials and notes exist.

        Usage:
            ``hud``          — two counter lines
            ``hud --json``   — machine-readable JSON without ANSI
            ``hud --plain``  — plain text without colours
        """
        from cli.output_mode import format_output, parse_output_flags
        from cli.session_hud import build_snapshot, render_snapshot

        mode = parse_output_flags(shlex.split(line or ""))
        snapshot = build_snapshot(dict(self.params))
        if mode.as_json or mode.plain:
            print(
                format_output(
                    {
                        "target": snapshot.target,
                        "phase": snapshot.phase,
                        "elapsed": snapshot.elapsed,
                        "session_commands": snapshot.session_commands,
                        "total_commands": snapshot.total_commands,
                        "creds": snapshot.creds,
                        "notes": snapshot.notes,
                    },
                    mode,
                )
            )
            return
        for text_line in render_snapshot(snapshot):
            print_msg(text_line)

    @cmd2.with_category("12. Miscellaneous")
    def do_undo(self, line):
        """Revert the last assign/set configuration change.

        Usage:
            ``undo``
        """
        del line
        from cli.config_history import get_shell_history
        from core.config import save_payload as _save

        shell = self._resolve_shell() or self
        history = get_shell_history(shell)
        previous = history.undo()
        if previous is None:
            print_warn("Nothing to undo.")
            return
        self.params.clear()
        self.params.update(previous)
        try:
            _save(self.params)
        except Exception as exc:
            print_warn(f"Restored in memory but payload save failed: {exc}")
            return
        try:
            self.refresh_prompt()
        except Exception:
            pass
        print_msg("Undone — previous configuration restored.")

    @cmd2.with_category("12. Miscellaneous")
    def do_config_diff(self, line):
        """Show what changed since the session started.

        Usage:
            ``config_diff``          — human-readable list
            ``config_diff --json``   — machine-readable JSON
        """
        from cli.config_history import get_shell_history
        from cli.output_mode import format_output, parse_output_flags

        mode = parse_output_flags(shlex.split(line or ""))
        shell = self._resolve_shell() or self
        history = get_shell_history(shell)
        changes = history.diff(dict(self.params))
        if not changes:
            print_msg("No configuration changes since session start.")
            return
        if mode.as_json:
            print(format_output({k: {"old": o, "new": n} for k, (o, n) in changes.items()}, mode))
            return
        for key in sorted(changes):
            old, new = changes[key]
            print_msg(f"{key}: {old!r} -> {new!r}")

    @cmd2.with_category("12. Miscellaneous")
    def do_cheat(self, line):
        """Render a cheatsheet section inside the shell.

        Usage:
            ``cheat``          — list available topics
            ``cheat recon``    — recon commands with examples
            ``cheat privesc``  — privilege escalation checklist
        """
        from rich.console import Console as _Console
        from rich.table import Table as _Table

        query = (line or "").strip().lower()
        if not query:
            print_msg(f"Topics: {', '.join(_CHEAT_SECTIONS)}")
            return
        section = self._find_cheat_section(query)
        if section is None:
            print_error(f"No cheatsheet topic for {query!r}. Topics: {', '.join(_CHEAT_SECTIONS)}")
            return
        table = _Table(title=f"cheat: {section[0]}", show_header=True, header_style="bold")
        table.add_column("Goal")
        table.add_column("Command", style="cyan")
        for goal, command in section[1]:
            table.add_row(goal, command)
        _Console(highlight=False, soft_wrap=True).print(table)

    @cmd2.with_category("12. Miscellaneous")
    def do_toast(self, line):
        """Raise a toast notification inside the cmd2 shell.

        The shell already renders toasts after every command; this command
        lets you raise one yourself. Use it to flag state changes for
        yourself or for a teammate tailing the same session.

        Usage:
            ``toast <message>``                      — info level
            ``toast <message> --level success``      — success / warn / error
            ``toast <message> --type beacon``        — custom label
            ``toast <message> --now``                — print immediately
            ``toast <message> --dry-run``            — show what would be written
        """
        from cli.output_mode import dry_run_line
        from cli.toast_bus import emit_toast, render_toasts

        args = shlex.split(line or "")
        level = "info"
        event_type = "note"
        show_now = False
        dry_run = False
        words: list[str] = []
        index = 0
        while index < len(args):
            token = args[index]
            if token in ("--level", "-l") and index + 1 < len(args):
                level = args[index + 1]
                index += 2
                continue
            if token.startswith("--level="):
                level = token.split("=", 1)[1]
                index += 1
                continue
            if token in ("--type", "-t") and index + 1 < len(args):
                event_type = args[index + 1]
                index += 2
                continue
            if token.startswith("--type="):
                event_type = token.split("=", 1)[1]
                index += 1
                continue
            if token == "--now":
                show_now = True
            elif token == "--dry-run":
                dry_run = True
            elif not token.startswith("-"):
                words.append(token)
            index += 1

        message = " ".join(words).strip()
        if not message:
            print_warn("Usage: toast <message> [--level info|success|warn|error] [--now]")
            return
        if dry_run:
            print_msg(dry_run_line(f"toast level={level} type={event_type} message={message!r}"))
            return
        sessions_dir = getattr(self._resolve_shell() or self, "sessions_dir", "sessions")
        written = emit_toast(message, severity=level, event_type=event_type, sessions_dir=sessions_dir)
        if not written:
            print_error("Could not write the toast event (sessions dir not writable).")
            return
        if show_now:
            render_toasts(payload=self.params, sessions_dir=sessions_dir)
        else:
            print_msg(f"toast queued [{level}] — it renders after your next command")

    @cmd2.with_category("12. Miscellaneous")
    def do_suggest(self, line):
        """Fuzzy command suggestion for typos and fragments.

        Usage:
            ``suggest nmp``      — suggests lazynmap, nmap variants
            ``suggest gobustr``  — suggests gobuster
        """
        from cli.fuzzy_match import suggest as _suggest

        query = (line or "").strip()
        if not query:
            print_warn("Usage: suggest <fragment>")
            return
        candidates = self._candidate_commands()
        ranked = _suggest(query, candidates, limit=5)
        if not ranked:
            print_warn(f"No command matches {query!r}.")
            return
        print_msg(f"Did you mean: {', '.join(ranked)}?")

    def _candidate_commands(self) -> list[str]:
        """Return searchable command names from the shell or aliases."""
        shell = self._resolve_shell()
        if shell is not None:
            for attr in ("get_all_commands", "get_all_command_names"):
                try:
                    names = getattr(shell, attr)()
                    if names:
                        return [str(n) for n in names]
                except Exception:
                    continue
        try:
            return sorted(str(k) for k in self.aliases.keys())
        except Exception:
            return []

    @staticmethod
    def _find_cheat_section(query: str) -> tuple[str, list[tuple[str, str]]] | None:
        """Locate a cheatsheet section matching query.

        Args:
            query: Lowercase topic fragment.

        Returns:
            Tuple of section title and (goal, command) rows, or None.
        """
        try:
            text = _CHEAT_PATH.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None
        sections: list[tuple[str, list[tuple[str, str]]]] = []
        current: tuple[str, list[tuple[str, str]]] | None = None
        for raw in text.splitlines():
            stripped = raw.strip()
            if stripped.startswith("## "):
                if current is not None:
                    sections.append(current)
                current = (stripped[3:].strip(), [])
            elif current is not None and stripped.startswith("|") and not stripped.startswith("| Goal"):
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                if len(cells) >= 2 and cells[0] and not cells[0].startswith("-"):
                    current[1].append((cells[0].replace("`", ""), cells[1].replace("`", "")))
        if current is not None:
            sections.append(current)
        for title, rows in sections:
            lowered = title.lower()
            if query in lowered or any(query in topic for topic in _CHEAT_SECTIONS if topic in lowered):
                return title, rows
        for title, rows in sections:
            if any(word in title.lower() for word in query.split()):
                return title, rows
        return None


__all__ = ["UxCommandSet"]
