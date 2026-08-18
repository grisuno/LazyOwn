"""Sleep obfuscation CommandSet — beacon memory evasion technique management.

Exposes ``modules/sleep_obfuscation`` through the LazyOwn CLI.
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import GREEN, RED, RESET, YELLOW, print_msg

CATEGORY = "04. Evasion & Bypass"


class SleepObfuscationCommandSet(LazyOwnCommandSet):
    """Sleep obfuscation technique manager."""

    phase = "evasion"
    category = CATEGORY

    @cmd2.with_category(CATEGORY)
    def do_sleep_list(self, line: str):
        """List available sleep obfuscation techniques.

        Usage: sleep_list [--windows | --linux]
        """
        from modules.sleep_obfuscation import OsPlatform, SleepObfuscationEngine

        engine = SleepObfuscationEngine()
        platform = OsPlatform.WINDOWS
        if "--linux" in line:
            platform = OsPlatform.LINUX
        techniques = engine.recommend(platform)
        print_msg(f"{GREEN}{len(techniques)} technique(s) for {platform.value}:{RESET}")
        for tech in techniques:
            risk_color = {
                "low": GREEN,
                "medium": YELLOW,
                "high": RED,
            }.get(tech.risk.value, RESET)
            print_msg(
                f"  {YELLOW}{tech.name}{RESET} [{risk_color}{tech.risk.value}{RESET}] score={tech.detection_resistance}"
            )
            print_msg(f"    {tech.description[:120]}")
            if tech.stability_note:
                print_msg(f"    {RED}Note:{RESET} {tech.stability_note[:100]}")

    @cmd2.with_category(CATEGORY)
    def do_sleep_info(self, line: str):
        """Show detailed information about a sleep obfuscation technique.

        Usage: sleep_info <technique_name>
        """
        from modules.sleep_obfuscation import SleepObfuscationEngine

        name = line.strip()
        if not name:
            print_msg("Usage: sleep_info <technique_name>")
            return
        engine = SleepObfuscationEngine()
        try:
            tech = engine.select(name)
        except KeyError:
            print_msg(f"{RED}Unknown technique: {name}{RESET}")
            return
        print_msg(f"{YELLOW}{tech.name}{RESET}")
        print_msg(f"  Description        : {tech.description}")
        print_msg(f"  Platforms          : {[p.value for p in tech.platforms]}")
        print_msg(f"  Detection resist   : {tech.detection_resistance}/100")
        print_msg(f"  Risk               : {tech.risk.value}")
        print_msg(f"  Min beacon version : {tech.min_beacon_version}")
        print_msg(f"  Requires ROP       : {tech.requires_rop_gadgets}")
        if tech.stability_note:
            print_msg(f"  {RED}Stability note    :{RESET} {tech.stability_note}")
        if tech.params:
            print_msg("  Parameters:")
            for pname, pdef in tech.params.items():
                print_msg(f"    --{pname} ({pdef['type']}, default={pdef['default']})")

    @cmd2.with_category(CATEGORY)
    def do_sleep_configure(self, line: str):
        """Configure the active sleep obfuscation technique.

        Usage: sleep_configure <technique_name> [--encrypt_heap --indirect_syscalls]

        Available techniques:
          sleep_mask, ekko, stack_spoof, module_stomp, fiber_sleep,
          thread_pool, hwbp_sleep, linux_gatekeeper, linux_futex_hide
        """
        from modules.sleep_obfuscation import SleepObfuscationEngine

        parts = line.strip().split()
        if not parts:
            print_msg("Usage: sleep_configure <technique_name>")
            return
        name = parts[0]
        engine = SleepObfuscationEngine()
        try:
            tech = engine.select(name)
        except KeyError:
            print_msg(f"{RED}Unknown technique: {name}{RESET}")
            return
        overrides = {}
        if "--encrypt_heap" in line:
            overrides["encrypt_heap"] = True
        if "--no-encrypt-heap" in line:
            overrides["encrypt_heap"] = False
        if "--indirect_syscalls" in line:
            overrides["indirect_syscalls"] = True
        if "--no-indirect" in line:
            overrides["indirect_syscalls"] = False
        config = engine.configure(tech, overrides)
        errors = engine.validate(config)
        if errors:
            print_msg(f"{RED}Validation errors:{RESET}")
            for e in errors:
                print_msg(f"  - {e}")
            return
        print_msg(f"{GREEN}Active technique: {config.technique_name}{RESET}")
        print_msg(f"  Encrypt heap     : {config.encrypt_heap}")
        print_msg(f"  Encrypt stack    : {config.encrypt_stack}")
        print_msg(f"  RWX->RW cycle    : {config.rwx_to_rw_cycle}")
        print_msg(f"  Indirect syscalls: {config.indirect_syscalls}")
        print_msg(f"  ROP gadgets      : {config.rop_gadget_count}")


__all__ = ["SleepObfuscationCommandSet"]
