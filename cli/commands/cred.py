"""Credential Access command set (pending).

Phase 07 — commands for credential access: password cracking,
hash manipulation, dictionary generation, and credential harvesting.

Pending status: inherits from :class:`PendingCommandSet`. Promote to
:class:`LazyOwnCommandSet` once originals are deleted from ``lazyown.py``.
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.categories import credential_access_category
from utils import (
    GREEN,
    RESET,
    check_lhost,
    check_rhost,
    copy2clip,
    print_error,
    print_msg,
    run_command,
)


class CredentialAccessCommandSet(LazyOwnCommandSet):
    """Credential Access phase commands (pending)."""

    phase = "cred"
    category = "07. Credential Access"

    @cmd2.with_category(credential_access_category)
    def do_hashcat(self, line):
        """Run hashcat password cracking."""
        if not line:
            print_msg("[+] Usage: hashcat <hash_file> <wordlist>")
            print_msg("[+] Example: hashcat hashes.txt /usr/share/wordlists/rockyou.txt")
            return
        self.cmd(f"hashcat --force {line}")

    @cmd2.with_category(credential_access_category)
    def do_john2hash(self, line):
        """Convert a hash to John the Ripper format."""
        if not line:
            print_error("Usage: john2hash <file>")
            return
        self.cmd(f"python3 modules/john2hash.py {line}")

    @cmd2.with_category(credential_access_category)
    def do_hydra(self, line):
        """Run Hydra for online password attacks."""
        rhost = self.params["rhost"]
        if not check_rhost(rhost):
            return
        if not line:
            print_msg("[+] Usage: hydra <service://target> <options>")
            print_msg(f"[+] Example: hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{rhost}")
            return
        self.cmd(f"hydra {line}")

    @cmd2.with_category(credential_access_category)
    def do_medusa(self, line):
        """Run Medusa for online password attacks."""
        if not line:
            print_error("Usage: medusa <options>")
            return
        self.cmd(f"medusa {line}")

    @cmd2.with_category(credential_access_category)
    def do_crunch(self, line):
        """Generate wordlists with crunch."""
        if not line:
            print_error("Usage: crunch <min> <max> <charset> -o <output>")
            return
        self.cmd(f"crunch {line}")

    @cmd2.with_category(credential_access_category)
    def do_cewl(self, line):
        """Generate a wordlist from a website with cewl."""
        if not line:
            url = self.params.get("url", "")
            if not url:
                print_error("Usage: cewl <url> or assign url")
                return
            self.cmd(f"cewl {url}")
        else:
            self.cmd(f"cewl {line}")

    @cmd2.with_category(credential_access_category)
    def do_sshkey(self, line):
        """Generate an SSH key pair."""
        self.cmd("ssh-keygen -t rsa -b 4096 -f sessions/id_rsa -N ''")
        print_msg("[+] SSH key pair created in sessions/")

    @cmd2.with_category(credential_access_category)
    def do_creds_py(self, line):
        """Extract credentials from a file or command output."""
        self.cmd(f"python3 modules/creds.py {line}")

    @cmd2.with_category(credential_access_category)
    def do_spraykatz(self, line):
        """Run SprayKatz for credential spraying."""
        self.cmd(f"python3 modules/spraykatz.py {line}")
