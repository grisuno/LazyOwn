"""Audit-mode CommandSet: fuzzy finder, forms, status tail, transcript grep.

This module wires the SOLID primitives in :mod:`cli.cli_enhancements` to the
running ``LazyOwnShell`` instance via cmd2's CommandSet auto-discovery.

Commands exposed
----------------
- ``fz [query]`` — fuzzy command finder backed by ``FuzzyCommandIndex``.
- ``form <command>`` — interactive parameter form for any registered command.
- ``status_tail [target]`` — parse the latest scan partial and print progress.
- ``grep_log <pattern>`` — grep across the recent transcript.
- ``reload_addons`` — trigger one polling sweep over ``lazyaddons/``+``plugins/``.

Design constraints
------------------
- Pull the parent shell instance via ``self._cmd``. Never import lazyown.py.
- Lazily build heavy primitives (transcript store, hot reloader) so cmd2
  startup does not regress.
- Every public command method has a one-line docstring (cmd2 turns it into
  the help text shown by ``help <name>``).
"""

from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Any

from cmd2 import with_category

from cli.cli_enhancements import (
    AddonHotReloader,
    DictPayloadProvider,
    FormField,
    FormSpec,
    FuzzyCommandIndex,
    InteractiveForm,
    LiveStatusTail,
    PayloadAwareCompleter,
    StaticCommandLister,
    TranscriptStore,
    commands_from_cmd2_shell,
)
from cli.commands._base import LazyOwnCommandSet

_FORM_SPECS: dict[str, FormSpec] = {
    "phishing": FormSpec(
        command="phishing",
        summary="Build a phishing campaign payload (calls do_phishing).",
        fields=(
            FormField("template", "Phishing template name (under templates/phishing/)", required=True),
            FormField("target_email", "Recipient email address", required=True),
            FormField("smtp_server", "SMTP host"),
            FormField("smtp_port", "SMTP port", default="587"),
            FormField("smtp_user", "SMTP username"),
            FormField("smtp_pass", "SMTP password"),
            FormField("subject", "Email subject", default="Important security update"),
            FormField("from_name", "From display name", default="IT Support"),
            FormField("track_clicks", "Track link clicks", default="true",
                      options=("true", "false")),
        ),
    ),
    "venom": FormSpec(
        command="venom",
        summary="Generate an msfvenom payload.",
        fields=(
            FormField("payload", "msfvenom payload string", required=True,
                      default="windows/x64/meterpreter/reverse_tcp"),
            FormField("lhost", "Listener host"),
            FormField("lport", "Listener port", default="4444"),
            FormField("output", "Output file path", default="sessions/payload.exe"),
            FormField("encoder", "Encoder name", default=""),
            FormField("iterations", "Encoder iterations", default="1"),
        ),
    ),
    "evil": FormSpec(
        command="evil-winrm",
        summary="Open an evil-winrm session.",
        fields=(
            FormField("rhost", "Target host", required=True),
            FormField("user", "Username", required=True),
            FormField("password", "Password (leave empty to use hash)"),
            FormField("hash", "NT hash for pass-the-hash"),
            FormField("port", "WinRM port", default="5985"),
            FormField("ssl", "Use SSL", default="false", options=("true", "false")),
        ),
    ),
}


class AuditCommandSet(LazyOwnCommandSet):
    """Operator commands that improve audit ergonomics.

    Phase: ``audit`` (cross-cutting; not tied to a kill-chain stage).
    """

    phase = "audit"
    category = "Audit"

    def __init__(self) -> None:
        super().__init__()
        self._fuzzy: FuzzyCommandIndex | None = None
        self._completer: PayloadAwareCompleter | None = None
        self._transcript: TranscriptStore | None = None
        self._hot: AddonHotReloader | None = None

    # ── Lazy singletons ──────────────────────────────────────────────────

    def _ensure_fuzzy(self) -> FuzzyCommandIndex:
        shell = self._cmd
        if self._fuzzy is None and shell is not None:
            commands = commands_from_cmd2_shell(shell)
            self._fuzzy = FuzzyCommandIndex(StaticCommandLister(commands))
        return self._fuzzy

    def _ensure_completer(self) -> PayloadAwareCompleter:
        shell = self._cmd
        if self._completer is None and shell is not None:
            payload = DictPayloadProvider(getattr(shell, "params", {}) or {})
            self._completer = PayloadAwareCompleter(
                payload,
                addon_lister=lambda: list((getattr(shell, "lazyaddons_dir", "") and
                                           [p.stem for p in Path(shell.lazyaddons_dir).glob("*.yaml")]) or []),
                plugin_lister=lambda: list((getattr(shell, "plugins_dir", "") and
                                            [p.stem for p in Path(shell.plugins_dir).glob("*.lua")]) or []),
                credential_lister=lambda: _read_credentials(shell),
            )
        return self._completer

    def _ensure_transcript(self) -> TranscriptStore:
        shell = self._cmd
        if self._transcript is None and shell is not None:
            sessions_dir = Path(getattr(shell, "sessions_dir", "sessions"))
            self._transcript = TranscriptStore(sessions_dir)
        return self._transcript

    def _ensure_hot_reloader(self) -> AddonHotReloader | None:
        shell = self._cmd
        if self._hot is not None or shell is None:
            return self._hot
        addons = Path(getattr(shell, "lazyaddons_dir", "lazyaddons"))
        plugins = Path(getattr(shell, "plugins_dir", "plugins"))
        self._hot = AddonHotReloader(
            directories=[addons, plugins],
            on_change=lambda p: shell.poutput(f"[reload] {p}") if hasattr(shell, "poutput") else None,
        )
        return self._hot

    # ── Commands ─────────────────────────────────────────────────────────

    @with_category("Audit")
    def do_fz(self, statement) -> None:
        """Fuzzy command finder. Usage: fz [query]. Empty lists every command."""
        index = self._ensure_fuzzy()
        if index is None:
            self._cmd.poutput("(fuzzy index unavailable)")
            return
        query = (str(statement) or "").strip()
        matches = index.search(query, limit=25)
        if not matches:
            self._cmd.poutput(f"no match for {query!r}")
            return
        self._cmd.poutput(f"  {'score':>5}  {'cmd':<26} {'aliases':<28} summary")
        self._cmd.poutput(f"  {'-'*5}  {'-'*26} {'-'*28} {'-'*40}")
        for m in matches:
            aliases = ",".join(m.info.aliases[:3])
            self._cmd.poutput(
                f"  {m.score:>5.2f}  {m.info.name:<26} {aliases:<28} "
                f"{m.info.summary[:60]}"
            )

    @with_category("Audit")
    def do_form(self, statement) -> None:
        """Open an interactive form for a known command. Usage: form <command>."""
        argv = shlex.split(str(statement) or "")
        if not argv:
            self._cmd.poutput("usage: form <command>")
            self._cmd.poutput("known forms: " + ", ".join(sorted(_FORM_SPECS.keys())))
            return
        spec = _FORM_SPECS.get(argv[0])
        if spec is None:
            self._cmd.poutput(f"no form for {argv[0]!r}; use one of "
                              f"{sorted(_FORM_SPECS.keys())}")
            return
        defaults = dict(getattr(self._cmd, "params", {}) or {})
        form = InteractiveForm()
        result = form.render(spec, defaults=defaults)
        self._cmd.poutput(json.dumps(result, indent=2, default=str))
        self._cmd.last_result = {"command": spec.command, "args": result}

    @with_category("Audit")
    def do_status_tail(self, statement) -> None:
        """Print live progress from the latest sessions/scan_*.partial file."""
        shell = self._cmd
        sessions_dir = Path(getattr(shell, "sessions_dir", "sessions"))
        argv = shlex.split(str(statement) or "")
        rhost = argv[0] if argv else (getattr(shell, "params", {}) or {}).get("rhost", "")
        candidates: list[Path] = []
        if rhost:
            candidates.extend(sorted(sessions_dir.glob(f"scan_{rhost}*")))
        candidates.extend(sorted(sessions_dir.glob("scan_*.partial")))
        candidates.extend(sorted(sessions_dir.glob("scan_*.nmap")))
        seen: set[Path] = set()
        ordered: list[Path] = []
        for p in candidates:
            if p in seen or not p.is_file():
                continue
            seen.add(p)
            ordered.append(p)
        if not ordered:
            self._cmd.poutput("no scan output found yet")
            return
        latest = max(ordered, key=lambda p: p.stat().st_mtime)
        try:
            content = latest.read_text(errors="replace")
        except OSError as exc:
            self._cmd.poutput(f"cannot read {latest}: {exc}")
            return
        update = LiveStatusTail().parse(content)
        self._cmd.poutput(f"file        : {latest}")
        self._cmd.poutput(f"ports_seen  : {update.ports_seen}")
        if update.open_ports:
            self._cmd.poutput(f"open_ports  : {','.join(str(p) for p in update.open_ports)}")
        if update.completed_pct is not None:
            self._cmd.poutput(f"completed   : {update.completed_pct:.1f}%")
        if update.last_line:
            self._cmd.poutput(f"last_line   : {update.last_line}")

    @with_category("Audit")
    def do_grep_log(self, statement) -> None:
        """Grep recent command outputs. Usage: grep_log <pattern> [--cmd <name>]."""
        text = str(statement) or ""
        argv = shlex.split(text)
        if not argv:
            self._cmd.poutput("usage: grep_log <pattern> [--cmd <name>]")
            return
        pattern = argv[0]
        cmd_filter = None
        if "--cmd" in argv:
            try:
                cmd_filter = argv[argv.index("--cmd") + 1]
            except IndexError:
                pass
        store = self._ensure_transcript()
        if store is None:
            self._cmd.poutput("(transcript store unavailable)")
            return
        results = store.grep(pattern, command_filter=cmd_filter, limit=80)
        if not results:
            self._cmd.poutput(f"no matches for {pattern!r}")
            return
        for r in results:
            if "error" in r:
                self._cmd.poutput(f"[!] {r['error']}")
                continue
            self._cmd.poutput(f"[{r['command']}] L{r['line_no']}: {r['line']}")

    @with_category("Audit")
    def do_reload_addons(self, _statement) -> None:
        """Re-scan lazyaddons/ and plugins/ for changes; reloads what's new."""
        shell = self._cmd
        reloader = self._ensure_hot_reloader()
        if reloader is None:
            self._cmd.poutput("(hot reloader unavailable)")
            return
        changed = reloader.poll_once()
        if not changed:
            self._cmd.poutput("no changes detected")
            return
        if hasattr(shell, "load_plugins"):
            try:
                shell.load_plugins()
            except Exception as exc:
                self._cmd.poutput(f"plugin reload error: {exc}")
        if hasattr(shell, "register_tool_commands"):
            try:
                shell.register_tool_commands()
            except Exception as exc:
                self._cmd.poutput(f"addon reload error: {exc}")
        for p in changed:
            self._cmd.poutput(f"reloaded: {p}")

    @with_category("Audit")
    def do_audit_complete_keys(self, statement) -> None:
        """Print payload-aware completion suggestions for a partial command."""
        argv = shlex.split(str(statement) or "")
        if not argv:
            self._cmd.poutput("usage: audit_complete_keys <command> [partial]")
            return
        command = argv[0]
        partial = argv[1] if len(argv) > 1 else ""
        completer = self._ensure_completer()
        if completer is None:
            self._cmd.poutput("(completer unavailable)")
            return
        for s in completer.complete(command, partial):
            self._cmd.poutput(f"  {s.text:<30} {s.description[:60]}")


def _read_credentials(shell: Any) -> list[str]:
    sessions_dir = Path(getattr(shell, "sessions_dir", "sessions"))
    out: list[str] = []
    for fp in sorted(sessions_dir.glob("credentials*.txt")):
        try:
            for line in fp.read_text(errors="replace").splitlines():
                line = line.strip()
                if line:
                    out.append(line)
        except OSError:
            continue
    seen: set[str] = set()
    deduped: list[str] = []
    for c in out:
        if c not in seen:
            seen.add(c)
            deduped.append(c)
    return deduped[:50]


__all__ = ["AuditCommandSet"]
