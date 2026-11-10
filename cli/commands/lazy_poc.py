"""LazyPoc shell commands: catalogued PoC scripts as reusable verbs."""

from __future__ import annotations

import shlex
from datetime import UTC, datetime
from pathlib import Path

from cli.commands._base import LazyOwnCommandSet
from core.hardening import safe_subprocess_run
from utils import CYAN, GREEN, RESET, print_error, print_msg, print_succ, print_warn

SESSIONS_DIR = Path("sessions")
POC_LOG_DIR = SESSIONS_DIR / "poc"
_MAX_LOG_CHARS = 200_000


class LazyPocCommandSet(LazyOwnCommandSet):
    """Run catalogued proof-of-concept scripts as loop-routable verbs."""

    phase = "exploit"
    category = "12. Miscellaneous"

    def do_lazy_poc(self, line):
        """Operate the PoC verb registry.

        Usage:
            lazy_poc list                     catalogued PoC verbs
            lazy_poc info <name>              one verb's contract
            lazy_poc run <name> [target] [k=v ...]
                                              render placeholders from payload.json
                                              (rhost, rport, lhost, lport, user,
                                              password, domain) and execute the
                                              script through the safe subprocess
        """
        from modules import poc_registry

        args = shlex.split(line.strip()) if line.strip() else []
        action = args[0].lower() if args else "list"
        if action == "list":
            self._list(poc_registry)
            return
        if action == "info":
            if len(args) < 2:
                print_error("usage: lazy_poc info <name>")
                return
            self._info(poc_registry, args[1])
            return
        if action == "run":
            if len(args) < 2:
                print_error("usage: lazy_poc run <name> [target] [key=value ...]")
                return
            name = args[1].lower()
            target = args[2] if len(args) > 2 and "=" not in args[2] else ""
            overrides = {}
            for token in args[2:]:
                if "=" not in token:
                    continue
                key, _, value = token.partition("=")
                if key.strip():
                    overrides[key.strip()] = value
            self._run(poc_registry, name, target, overrides)
            return
        print_error("Unknown action; usage: lazy_poc list|info|run")

    def _list(self, registry) -> None:
        """Print every catalogued PoC verb with phase and risk."""
        verbs = registry.verbs_summary()
        if not verbs:
            print_warn("No PoC verbs catalogued (config/poc_verbs.yaml)")
            return
        print_msg(f"{len(verbs)} PoC verb(s):")
        for verb in verbs:
            state = f"{GREEN}on{RESET}" if verb.get("enabled") else "off"
            print_msg(
                f"  {CYAN}{verb['name']:<20}{RESET} {state} "
                f"{verb['phase']:<8} {verb['risk']:<9} {str(verb['title'])[:60]}"
            )
        print_msg("Run: lazy_poc run <name> [target] [key=value ...]")

    def _info(self, registry, name: str) -> None:
        """Print one PoC verb contract."""
        verb = registry.get_poc(name)
        if verb is None:
            print_error(f"unknown PoC verb '{name}' (lazy_poc list)")
            return
        print_msg(f"{CYAN}{verb.name}{RESET} - {verb.title}")
        print_msg(f"  script      modules/{verb.script} ({verb.interpreter})")
        print_msg(f"  phase       {verb.phase}   risk {verb.risk}   os {verb.os}")
        print_msg(f"  enabled     {verb.enabled}   timeout {verb.timeout_sec:.0f}s")
        if verb.triggers:
            print_msg(f"  triggers    {', '.join(verb.triggers)}")
        if verb.requires:
            print_msg(f"  requires    {', '.join(verb.requires)}")
        if verb.args:
            rendered = " ".join(f"{arg.flag} {arg.value}".strip() for arg in verb.args if arg.flag or arg.value)
            print_msg(f"  args        {rendered}")
        missing = registry.missing_requirements(verb)
        if missing:
            print_warn(f"missing requirements: {', '.join(missing)}")

    def _run(self, registry, name: str, target: str, overrides: dict) -> None:
        """Render and execute one PoC verb with audit logging."""
        verb = registry.get_poc(name)
        if verb is None:
            print_error(f"unknown PoC verb '{name}' (lazy_poc list)")
            return
        if not verb.enabled:
            print_error(f"PoC verb '{name}' is disabled in config/poc_verbs.yaml")
            return
        try:
            from core.config import load_payload

            params = dict(load_payload() or {})
        except Exception:
            params = {}
        for key, value in dict(getattr(self, "params", {}) or {}).items():
            if value not in (None, ""):
                params[key] = value
        rendered = registry.render_argv(verb, params, target=target, overrides=overrides)
        if rendered.missing:
            print_error(
                "unresolved placeholder(s): "
                + ", ".join(rendered.missing)
                + " - set them in payload.json or pass key=value"
            )
            return
        missing = registry.missing_requirements(verb)
        if missing:
            print_error(f"missing requirements: {', '.join(missing)}")
            return
        print_msg(f"[poc] {' '.join(str(part) for part in rendered.argv)}")
        try:
            result = safe_subprocess_run(
                list(rendered.argv),
                timeout=verb.timeout_sec,
                reason=f"lazy_poc run {verb.name}",
            )
        except Exception as exc:
            print_error(f"execution failed: {exc}")
            return
        output = (result.stdout or "") + (result.stderr or "")
        for stream in (result.stdout, result.stderr):
            if stream and stream.strip():
                print(stream.rstrip()[:8000])
        if result.returncode == 0 and output.strip():
            print_succ(f"PoC verb '{verb.name}' finished (rc=0)")
        elif result.returncode != 0:
            print_warn(f"PoC verb '{verb.name}' exited rc={result.returncode}")
        self._log_run(verb, rendered, output, result.returncode)

    def _log_run(self, verb, rendered, output: str, returncode: int) -> None:
        """Persist the PoC transcript under sessions/poc/."""
        try:
            POC_LOG_DIR.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            path = POC_LOG_DIR / f"{verb.name}_{stamp}.log"
            body = [
                f"# {verb.name} ({verb.title})",
                f"# argv: {' '.join(str(part) for part in rendered.argv)}",
                f"# resolved: {rendered.resolved}",
                f"# rc: {returncode}",
                output[:_MAX_LOG_CHARS],
            ]
            path.write_text("\n".join(body), encoding="utf-8")
            print_msg(f"transcript: {path}")
        except OSError as exc:
            print_warn(f"could not persist transcript: {exc}")
