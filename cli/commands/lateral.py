"""Lateral Movement command set (pending).

Phase 08 — commands for lateral movement: tunneling, pivoting,
remote execution, and protocol-specific lateral movement tools.

Pending status: inherits from :class:`PendingCommandSet`. Promote to
:class:`LazyOwnCommandSet` once originals are deleted from ``lazyown.py``.
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._dormancy import PendingCommandSet
from modules.categories import lateral_movement_category
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


class LateralMovementCommandSet(PendingCommandSet):
    """Lateral Movement phase commands (pending)."""

    phase = "lateral"
    category = "08. Lateral Movement"

    @cmd2.with_category(lateral_movement_category)
    def do_socat(self, line):
        """Run socat for port forwarding."""
        lhost = self.params["lhost"]
        if not check_lhost(lhost):
            return
        if not line:
            print_msg("[+] Usage: socat <local_port>:<remote_host>:<remote_port>")
            print_msg(f"[+] Example: socat TCP-LISTEN:4444,fork TCP:{lhost}:5555")
            return
        self.cmd(f"socat {line}")

    @cmd2.with_category(lateral_movement_category)
    def do_chisel(self, line):
        """Run chisel for quick tunneling."""
        lhost = self.params["lhost"]
        if not check_lhost(lhost):
            return
        mode = input("[?] Server or client mode? (s/c, default c): ") or "c"
        if mode == "s":
            port = input(f"[?] Listen port (default: 1080): ") or "1080"
            print_msg(f"[+] Starting chisel server on port {port}")
            self.cmd(f"chisel server -p {port} --socks5")
        else:
            port = input(f"[?] Server port (default: 1080): ") or "1080"
            print_msg(f"[+] Connecting to chisel server at {lhost}:{port}")
            self.cmd(f"chisel client {lhost}:{port} socks")

    @cmd2.with_category(lateral_movement_category)
    def do_set_proxychains(self, line):
        """Configure proxychains for the current session."""
        lhost = self.params["lhost"]
        if not check_lhost(lhost):
            return
        port = line or "9050"
        config = f"strict_chain\nproxy_dns\ntcp_read_time_out 15000\ntcp_connect_time_out 8000\n[ProxyList]\nsocks4 {lhost} {port}\n"
        with open("/etc/proxychains.conf", "w") as f:
            f.write(config)
        print_msg(f"[+] proxychains configured: {lhost}:{port}")
        print_msg("[+] Usage: proxychains <command>")

    @cmd2.with_category(lateral_movement_category)
    def do_ngrok(self, line):
        """Start ngrok tunnel."""
        port = line or self.params.get("lport", "80")
        print_msg(f"[+] Starting ngrok tunnel on port {port}")
        self.cmd(f"ngrok http {port}")

    @cmd2.with_category(lateral_movement_category)
    def do_ligolo(self, line):
        """Run Ligolo-ng for advanced pivoting."""
        mode = input("[?] Proxy or agent? (p/a, default p): ") or "p"
        if mode == "p":
            self.cmd("ligolo-proxy -selfcert")
        else:
            lhost = self.params["lhost"]
            if not check_lhost(lhost):
                return
            self.cmd(f"ligolo-agent -connect {lhost}:11601 -ignore-cert")

    @cmd2.with_category(lateral_movement_category)
    def do_nc(self, line):
        """Netcat listener or connect."""
        mode = input("[?] Listen (l) or connect (c)? (default l): ") or "l"
        port = line or self.params.get("lport", "4444")
        if mode == "l":
            print_msg(f"[+] Listening on port {port}")
            self.cmd(f"nc -lvnp {port}")
        else:
            rhost = self.params["rhost"]
            if not check_rhost(rhost):
                return
            print_msg(f"[+] Connecting to {rhost}:{port}")
            self.cmd(f"nc -vn {rhost} {port}")

    @cmd2.with_category(lateral_movement_category)
    def do_wmiexec(self, line):
        """Execute commands via WMI."""
        if not line:
            print_error("Usage: wmiexec <target> <command>")
            return
        self.cmd(f"python3 modules/wmiexec.py {line}")

    @cmd2.with_category(lateral_movement_category)
    def do_ssh(self, line):
        """SSH to a remote host (custom port)."""
        rhost = self.params["rhost"]
        if not check_rhost(rhost):
            return
        user = input("[?] Username (default: root): ") or "root"
        port = input("[?] Port (default: 22): ") or "22"
        self.cmd(f"ssh {user}@{rhost} -p {port}")
