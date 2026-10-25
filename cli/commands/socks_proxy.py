"""SOCKS proxy CommandSet — beacon tunneling configuration.

Exposes ``modules/socks_proxy`` through the LazyOwn CLI.
"""

from __future__ import annotations

import json

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import GREEN, RED, RESET, YELLOW, print_msg

CATEGORY = "10. Command & Control"


class SocksProxyCommandSet(LazyOwnCommandSet):
    """SOCKS5 proxy configuration commands."""

    phase = "c2"
    category = CATEGORY

    @cmd2.with_category(CATEGORY)
    def do_socks_config(self, line: str):
        """Show or configure the SOCKS5 proxy.

        Usage: socks_config [--bind <ip>] [--port <n>] [--no-localhost] [--json]

        Displays the current SOCKS proxy configuration. Use flags to
        override settings for the next beacon build.
        """
        from modules.socks_proxy import SocksProxyConfig, SocksProxyEngine

        config = SocksProxyConfig()
        if "--bind" in line:
            parts = line.split()
            try:
                idx = parts.index("--bind")
                config = SocksProxyConfig(bind_address=parts[idx + 1])
            except (ValueError, IndexError):
                print_msg(f"{RED}Usage: socks_config --bind <ip>{RESET}")
                return
        if "--port" in line:
            parts = line.split()
            try:
                idx = parts.index("--port")
                config = SocksProxyConfig(bind_port=int(parts[idx + 1]))
            except (ValueError, IndexError):
                print_msg(f"{RED}Usage: socks_config --port <n>{RESET}")
                return
        engine = SocksProxyEngine(config=config)
        errors = engine.validate()
        if errors:
            print_msg(f"{RED}Config errors:{RESET}")
            for e in errors:
                print_msg(f"  - {e}")
            return
        print_msg(f"{GREEN}SOCKS5 Proxy Configuration{RESET}")
        print_msg(f"  Bind address       : {engine.config.bind_address}")
        print_msg(f"  Bind port          : {engine.config.bind_port}")
        print_msg(f"  Auth methods       : {[m.name for m in engine.config.auth_methods]}")
        print_msg(f"  Max connections    : {engine.config.max_connections}")
        print_msg(f"  Session timeout    : {engine.config.session_timeout_seconds}s")
        print_msg(f"  Bandwidth limit    : {engine.config.bandwidth_limit_bps or 'unlimited'} Bps")
        print_msg(f"  Allow localhost    : {engine.config.allow_localhost}")
        print_msg(f"  Allow private      : {engine.config.allow_private_ranges}")
        print_msg(f"  Allowed ports      : {engine.config.allowed_ports or 'all'}")
        print_msg(f"  Denied ports       : {engine.config.denied_ports}")
        print_msg(f"  Connection log     : {engine.config.log_connections}")
        if "--json" in line:
            print(json.dumps(engine.build_spec(), indent=2))

    @cmd2.with_category(CATEGORY)
    def do_socks_sessions(self, line: str):
        """List active SOCKS proxy sessions.

        Usage: socks_sessions
        """
        from modules.socks_proxy import SocksProxyEngine

        engine = SocksProxyEngine()
        sessions = engine.list_sessions()
        if not sessions:
            print_msg(f"{YELLOW}No active SOCKS sessions.{RESET}")
            return
        print_msg(f"{GREEN}{len(sessions)} active session(s):{RESET}")
        for sess in sessions:
            print_msg(f"  {sess['session_id']:20s} {sess['target_host']}:{sess['target_port']}")
            print_msg(f"    bytes: {sess['bytes_sent']} sent / {sess['bytes_received']} recv")
            print_msg(f"    beacon: {sess['beacon_client_id']}")

    @cmd2.with_category(CATEGORY)
    def do_socks_export(self, line: str):
        """Export SOCKS5 proxy specification for beacon delivery.

        Usage: socks_export [--file <path>]

        Outputs the JSON spec that beacons use to configure their
        internal SOCKS5 proxy listener.
        """
        from modules.socks_proxy import SocksProxyEngine

        engine = SocksProxyEngine()
        spec = engine.build_spec()
        if "--file" in line:
            parts = line.split()
            try:
                idx = parts.index("--file")
                filepath = parts[idx + 1]
                with open(filepath, "w") as f:
                    json.dump(spec, f, indent=2)
                print_msg(f"{GREEN}Spec exported to {filepath}{RESET}")
                return
            except (ValueError, IndexError):
                print_msg(f"{RED}Usage: socks_export --file <path>{RESET}")
                return
        print(json.dumps(spec, indent=2))


__all__ = ["SocksProxyCommandSet"]
