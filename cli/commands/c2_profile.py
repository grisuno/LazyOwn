"""C2 profile CommandSet — extended malleable C2 profiles (TLS, DNS, SMB, WS).

Exposes ``modules/c2_profile_engine`` through the LazyOwn CLI.
"""

from __future__ import annotations

import json

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import GREEN, RESET, YELLOW, print_msg

CATEGORY = "10. Command & Control"


class C2ProfileCommandSet(LazyOwnCommandSet):
    """Extended C2 profile commands: TLS, DNS, SMB, WebSocket profiles."""

    phase = "c2"
    category = CATEGORY

    @cmd2.with_category(CATEGORY)
    def do_c2_profiles(self, line: str):
        """List all available C2 transport profiles.

        Usage: c2_profiles [--json]
        """
        from modules.c2_profile_engine import ProfileEngine

        engine = ProfileEngine()
        profiles = engine.get_all_profiles_dict()
        if "--json" in line:
            print(json.dumps(profiles, indent=2))
            return
        print_msg(f"{GREEN}Transport profiles:{RESET}")
        for transport, cfg in profiles.items():
            if transport == "rotation":
                continue
            enabled = cfg.get("enabled", False)
            status = f"{GREEN}ENABLED{RESET}" if enabled else f"{YELLOW}DISABLED{RESET}"
            print_msg(f"  [{status}] {transport}")
        print_msg(f"\nRotation slots: {len(profiles['rotation'])}")
        for slot in profiles["rotation"]:
            active = "->" if slot.get("active") else "  "
            print_msg(f"  {active} {slot['name']} ({slot['transport']})")

    @cmd2.with_category(CATEGORY)
    def do_c2_tls(self, line: str):
        """Display the current TLS C2 profile.

        Usage: c2_tls [--ja3]
        """
        from modules.c2_profile_engine import TlsProfile

        profile = TlsProfile()
        print_msg(f"TLS version  : {profile.min_version} - {profile.max_version}")
        print_msg(f"JA3 library  : {profile.ja3_fingerprint_library}")
        print_msg(f"GREASE       : {profile.grease_extensions}")
        print_msg(f"ALPN         : {profile.alpn_protocols}")
        print_msg("Cipher suites:")
        for cs in profile.get_cipher_suites():
            print_msg(f"  - {cs}")
        if "--ja3" in line:
            print_msg(f"JA3 hash     : {profile.get_ja3_hash()}")

    @cmd2.with_category(CATEGORY)
    def do_c2_dns(self, line: str):
        """Configure or display the DNS beacon profile.

        Usage: c2_dns [--domain <fqdn>] [--encoding base32|base64|hex]
        """
        from modules.c2_profile_engine import DnsProfile, ProfileValidator

        profile = DnsProfile.from_dict({})
        validator = ProfileValidator()
        errors = validator.validate_dns(profile)
        if errors and profile.enabled:
            for e in errors:
                print_msg(f"{YELLOW}[!]{RESET} {e}")
            return
        print_msg(f"DNS domain   : {profile.domain or '(not set)'}")
        print_msg(f"Encoding     : {profile.encoding}")
        print_msg(f"Query types  : {profile.query_types}")
        print_msg(f"Poll interval: {profile.poll_interval_ms} ms")
        print_msg(f"TTL bypass   : {profile.ttl_cache_bypass}")

    @cmd2.with_category(CATEGORY)
    def do_c2_rotate(self, line: str):
        """Rotate to the next C2 transport profile in the rotation queue.

        Usage: c2_rotate
        """
        from modules.c2_profile_engine import (
            DnsProfile,
            ProfileEngine,
            SmbProfile,
            WebSocketProfile,
        )

        engine = ProfileEngine(
            dns_profile=DnsProfile(enabled=True, domain="c2.example.com"),
            websocket_profile=WebSocketProfile(enabled=True),
            smb_profile=SmbProfile(enabled=True, pipe_name=r"\\\.\\pipe\\lazyown"),
        )
        slot = engine.rotate()
        print_msg(f"Rotated to: {slot.name} ({slot.transport.value})")


__all__ = ["C2ProfileCommandSet"]
