"""Resource script commands — run .ls scripts, record macros, spool output.

Provides:
    resource <file>    — run an enhanced resource script
    makerc <file>      — record commands to a script (alias)
    spool <file|off>   — log output to file
"""

from __future__ import annotations

import os
import shlex
from datetime import datetime

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.resource_script import ResourceScriptEngine, ScriptContext, ScriptError
from utils import (
    BLUE,
    CYAN,
    GREEN,
    RED,
    RESET,
    YELLOW,
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)


class ResourceCommandSet(LazyOwnCommandSet):
    """Enhanced resource script execution and spooling."""

    phase = "resource"
    category = "12. Miscellaneous"

    def _make_context(self) -> ScriptContext:
        shell = self._resolve_shell()
        shell_params = getattr(shell, "params", {}) if shell else {}

        def on_cmd(cmd: str) -> None:
            if shell:
                shell.onecmd(cmd)

        def on_print(msg: str) -> None:
            print_msg(msg)

        return ScriptContext(
            shell_params=shell_params,
            on_command=on_cmd,
            on_print=on_print,
        )

    @cmd2.with_category(miscellaneous_category)
    def do_resource(self, line):
        """Run an enhanced resource script.

        Usage: resource <script.ls>

        Supports variables ($var), conditionals (if/else/endif),
        loops (while/endwhile, for/endfor), macros (macro/endmacro/call),
        spool, sleep, echo, and comments (#).

        Example:
            resource scripts/auto_recon.ls
        """
        path = line.strip()
        if not path:
            print_error("Usage: resource <script.ls>")
            return
        if not os.path.isfile(path):
            print_error(f"Script not found: {path}")
            return

        ctx = self._make_context()
        engine = ResourceScriptEngine(ctx)

        try:
            engine.execute(path)
            print_msg(f"Resource script '{path}' completed.")
        except ScriptError as e:
            print_error(f"Script error: {e}")
        except FileNotFoundError:
            print_error(f"Script not found: {path}")

    @cmd2.with_category(miscellaneous_category)
    def do_makerc(self, line):
        """Record session commands to a resource script.

        Usage: makerc <script.ls>
        Captures all commands executed during the session into the script
        file. Use 'makerc off' to stop recording (not yet implemented).
        """
        path = line.strip()
        if not path:
            print_error("Usage: makerc <script.ls>")
            return

        shell = self._resolve_shell()
        if shell:
            shell._resource_recording = path
            shell._resource_recording_lines = []
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w") as f:
                f.write(f"# LazyOwn recorded script — {datetime.now()}\n")
            print_msg(f"Recording commands to {path}")
        else:
            print_error("No shell context available.")

    @cmd2.with_category(miscellaneous_category)
    def do_spool(self, line):
        """Log session output to a file.

        Usage:
            spool <file>   — start logging to file
            spool off      — stop logging
        """
        target = line.strip()
        if not target:
            print_msg(f"Current spool: {getattr(self._resolve_shell(), '_spool_file', 'none')}")
            return

        shell = self._resolve_shell()
        if not shell:
            print_error("No shell context available.")
            return

        if target.lower() == "off":
            if getattr(shell, "_spool_handle", None):
                shell._spool_handle.close()
            shell._spool_file = None
            shell._spool_handle = None
            print_msg("Spooling stopped.")
        else:
            os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
            shell._spool_file = target
            shell._spool_handle = open(target, "a")
            print_msg(f"Spooling to {target}")

    @cmd2.with_category(miscellaneous_category)
    def do_mkrc(self, line):
        """Alias for makerc — record commands to a script."""
        self.do_makerc(line)


