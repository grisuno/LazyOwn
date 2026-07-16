"""Reporting command set (pending).

Phase 11 — commands for reporting: AI summaries, screenshot capture,
machine JSON generation, vulnerability tracking, and evidence gathering.

Pending status: inherits from :class:`PendingCommandSet`. Promote to
:class:`LazyOwnCommandSet` once originals are deleted from ``lazyown.py``.
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.categories import reporting_category
from utils import (
    GREEN,
    RESET,
    check_lhost,
    check_rhost,
    print_msg,
    print_warn,
    run_command,
)


class ReportingCommandSet(LazyOwnCommandSet):
    """Reporting phase commands (pending)."""

    phase = "report"
    category = "11. Reporting"

    @cmd2.with_category(reporting_category)
    def do_gpt(self, line):
        """Query GPT/Groq AI for analysis and reporting."""
        if not line:
            print_msg("[+] Usage: gpt <prompt>")
            print_msg("[+] Example: gpt summarize this scan")
            return
        self.onecmd(f"vulnbot_groq {line}")

    @cmd2.with_category(reporting_category)
    def do_eyewitness(self, line):
        """Run EyeWitness for web screenshot capture."""
        if not line:
            rhost = self.params["rhost"]
            if not check_rhost(rhost):
                return
            self.cmd(f"eyewitness --web -single {rhost}")
        else:
            self.cmd(f"eyewitness {line}")

    @cmd2.with_category(reporting_category)
    def do_gowitness(self, line):
        """Run gowitness for web screenshot capture."""
        if not line:
            url = self.params.get("url", "")
            if not url:
                print_msg("[+] Usage: gowitness <url>")
                return
            self.cmd(f"gowitness single --url {url}")
        else:
            self.cmd(f"gowitness single --url {line}")

    @cmd2.with_category(reporting_category)
    def do_createtargets(self, line):
        """Create targets file from nmap scan."""
        self.cmd(f"python3 modules/create_targets.py {line}")

    @cmd2.with_category(reporting_category)
    def do_banners(self, line):
        """Manage custom banners for the framework."""
        if os.path.exists("sessions/banners.json"):
            self.onecmd("edit sessions/banners.json")
        else:
            print_msg("[+] No banners file found. Creating default...")
            with open("sessions/banners.json", "w") as f:
                f.write('{"banners": []}')
            self.onecmd("edit sessions/banners.json")

    @cmd2.with_category(reporting_category)
    def do_vulns(self, line):
        """Display or manage vulnerabilities."""
        self.onecmd("vulns") if not line else self.onecmd(f"vulns {line}")

    @cmd2.with_category(reporting_category)
    def do_create_session_json(self, line):
        """Create the session JSON report file."""
        self.cmd("python3 modules/create_session_json.py")

    @cmd2.with_category(reporting_category)
    def do_malwarebazar(self, line):
        """Search Malware Bazaar for malware samples."""
        if not line:
            print_msg("[+] Usage: malwarebazar <hash>")
            return
        self.cmd(f"python3 modules/malwarebazar.py {line}")
