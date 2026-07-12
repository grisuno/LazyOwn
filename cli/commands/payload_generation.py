"""Payload generation commands — list payloads and generate.

Provides:
    show payloads           — list all registered payloads
    generate <name> [options] [--format f] [--output path]
"""

from __future__ import annotations

import os
import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.payload_factory import PayloadFactory, format_payload_table
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


class PayloadCommandSet(LazyOwnCommandSet):
    """Payload generation and listing."""

    phase = "payload"
    category = "12. Miscellaneous"

    def _get_factory(self) -> PayloadFactory:
        shell = self._resolve_shell()
        if shell is None:
            return PayloadFactory()
        return getattr(shell, "_payload_factory", PayloadFactory())

    @cmd2.with_category(miscellaneous_category)
    def do_generate(self, line):
        """Generate a payload.

        Usage: generate <payload_name> LHOST=<ip> LPORT=<port> [--format f] [--output path]

        Examples:
            generate cmd/unix/reverse_shell LHOST=10.0.0.1 LPORT=4444
            generate cmd/unix/reverse_shell LHOST=10.0.0.1 LPORT=4444 shell_type=python
            generate cmd/windows/reverse_powershell LHOST=10.0.0.1 LPORT=4444 --format ps1 --output /tmp/shell.ps1

        Use 'show payloads' to list available payloads.
        """
        if not line.strip():
            print_error("Usage: generate <payload_name> LHOST=<ip> LPORT=<port> [options]")
            return

        factory = self._get_factory()
        args = shlex.split(line.strip())
        if not args:
            return
        name = args[0]
        template = factory.get(name)
        if template is None:
            print_error(f"Unknown payload: {name}")
            print_msg(f"Use 'show payloads' to list available payloads.")
            return

        kwargs: dict = {}
        fmt = "raw"
        output = None
        remaining = args[1:]

        i = 0
        while i < len(remaining):
            arg = remaining[i]
            if arg == "--format" and i + 1 < len(remaining):
                fmt = remaining[i + 1]
                i += 2
            elif arg == "--output" and i + 1 < len(remaining):
                output = remaining[i + 1]
                i += 2
            elif "=" in arg:
                key, val = arg.split("=", 1)
                kwargs[key.lower()] = val
                i += 1
            else:
                print_warn(f"Ignoring unknown argument: {arg}")
                i += 1

        shell = self._resolve_shell()
        if shell is not None:
            for key in ("lhost", "lport", "rhost", "rport", "domain"):
                if key not in kwargs and key in shell.params:
                    kwargs[key] = shell.params[key]

        try:
            raw = factory.generate(name, format=fmt, output=output, **kwargs)
            out_size = len(raw)
            out_loc = output or "<stdout>"
            print_msg(f"Generated payload: {name}")
            print_msg(f"  Format : {fmt}")
            print_msg(f"  Size   : {out_size} bytes")
            if output:
                print_msg(f"  Output : {output}")
            else:
                if fmt in ("raw", "bin"):
                    hex_preview = raw[:32].hex()
                    print_msg(f"  Raw    : {hex_preview}...")
                else:
                    print(raw.decode("utf-8", errors="replace"))
        except Exception as e:
            print_error(f"Generation failed: {e}")
