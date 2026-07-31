"""EDR Detection command set.

Phase 02 — commands for detecting endpoint security products on targets,
generating evasion profiles, and recommending bypass techniques.
"""

from __future__ import annotations

import json
import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    GREEN,
    RED,
    RESET,
    YELLOW,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)

EDR_CATEGORY = "02. Scanning & Enumeration"


class EDRDetectCommandSet(LazyOwnCommandSet):
    """EDR/AV detection and evasion profiling commands."""

    phase = "recon"
    category = EDR_CATEGORY

    @cmd2.with_category(EDR_CATEGORY)
    def do_edr_detect(self, line):
        """Detect EDR/AV products on the target.

        Usage:
            edr_detect                    Detect locally (from implant)
            edr_detect --target <ip>      Generate remote detection commands
            edr_detect --target <ip> --user <u> --password <p>  Execute remotely via CrackMapExec

        Fingerprints 17 EDR/AV products and generates tailored bypass recommendations.
        """
        import shlex
        args = shlex.split(line)
        remote_type = self._extract(args, "--type") or "wmi"
        output_file = self._extract(args, "--output") or "sessions/edr_profile.json"

        try:
            from modules.edr_detector import EDRDetector, EDRProfile
        except ImportError as exc:
            print_error(f"EDR detector module not available: {exc}")
            return

        target = self._extract(args, "--target") or self.params.get("rhost", "")

        if not target:
            print_msg("No --target specified. Generating remote detection commands for general use.\n")
            commands = EDRDetector.detect_remote_commands(remote_type)
            for cmd_info in commands:
                print_msg(f"\n{YELLOW}[{cmd_info['name']}]{RESET}")
                print_msg(f"  {cmd_info['command']}")
            print_msg("\nExecute via: cme smb <target> -x '<command>'")
            return

        user = self._extract(args, "--user") or self.params.get("username", "")
        password = self._extract(args, "--password") or self.params.get("password", "")

        if user and password:
            print_msg(f"Running remote EDR detection on {target} via CrackMapExec...")
            commands = EDRDetector.detect_remote_commands(remote_type)
            for cmd_info in commands:
                cmd = cmd_info["command"].replace('"', '\\"')
                self.cmd(f"crackmapexec smb {target} -u {user} -p '{password}' -x '{cmd}' 2>/dev/null")
        else:
            print_msg(f"Remote detection commands for {target}:\n")
            commands = EDRDetector.detect_remote_commands(remote_type)
            for cmd_info in commands:
                print_msg(f"\n{YELLOW}[{cmd_info['name']}]{RESET}")
                print_msg(f"  crackmapexec smb {target} -x '{cmd_info['command']}'")

    @cmd2.with_category(EDR_CATEGORY)
    def do_edr_profile(self, line):
        """Generate an evasion profile based on detected EDR.

        Usage: edr_profile [--product <name>]

        Takes detected EDR product names and recommends specific bypass
        techniques. With no arguments, shows bypasses for common EDRs.
        """
        import shlex
        args = shlex.split(line)
        product = self._extract(args, "--product")

        try:
            from modules.edr_detector import EDRDetector
        except ImportError as exc:
            print_error(f"EDR detector module not available: {exc}")
            return

        from modules.edr_detector import EDRProfile, EDRFinding

        if product:
            profile = EDRProfile()
            profile.detected = [EDRFinding(
                product=product, confidence="user_specified", source="manual", details=""
            )]
        else:
            profile = EDRDetector.detect_local()

        if profile.detected:
            print_msg(f"\n{GREEN}Detected security products:{RESET}")
            for finding in profile.detected:
                conf_color = GREEN if finding.confidence == "high" else YELLOW
                print_msg(f"  {conf_color}{finding.product}{RESET} [{finding.confidence}] — {finding.details}")
        else:
            print_msg("No security products detected from local checks.")

        recommendations = EDRDetector._generate_recommendations(profile)
        if recommendations:
            print_msg(f"\n{GREEN}Recommended bypass techniques:{RESET}")
            for rec in recommendations:
                print_msg(f"  {YELLOW}[*]{RESET} {rec}")

        print_msg(f"\n{YELLOW}Detection severity: {EDRDetector._severity(profile)}{RESET}")

        os.makedirs("sessions", exist_ok=True)
        result = {
            "detected": [
                {"product": f.product, "confidence": f.confidence, "details": f.details}
                for f in profile.detected
            ],
            "severity": EDRDetector._severity(profile),
            "recommendations": recommendations,
        }
        with open("sessions/edr_profile.json", "w") as f:
            json.dump(result, f, indent=2)
        print_msg("Profile saved to sessions/edr_profile.json")

    @cmd2.with_category(EDR_CATEGORY)
    def do_edr_script(self, line):
        """Generate a PowerShell EDR detection script.

        Usage: edr_script [--output <path>]

        Creates a comprehensive PowerShell script that detects 17+ EDR/AV
        products via WMI, services, processes, registry, and drivers.
        Saves to sessions/edr_detect.ps1 by default.
        """
        import shlex
        args = shlex.split(line)

        try:
            from modules.edr_detector import EDRDetector
        except ImportError as exc:
            print_error(f"EDR detector module not available: {exc}")
            return

        output_path = self._extract(args, "--output") or "sessions/edr_detect.ps1"
        remote_type = self._extract(args, "--type") or "local"
        script = EDRDetector.generate_edr_check_script(remote_type)

        os.makedirs(os.path.dirname(output_path) or "sessions", exist_ok=True)
        with open(output_path, "w") as f:
            f.write(script)

        print_succ(f"EDR detection script saved to {output_path}")
        print_msg(f"Run on target: powershell -ExecutionPolicy Bypass -File {output_path}")
        if remote_type in ("smb", "wmi"):
            print_msg(f"Or remotely: crackmapexec {remote_type} <target> -x 'powershell -c \"{script[:200]}...\"'")

    @staticmethod
    def _extract(args: list[str], flag: str) -> str | None:
        try:
            idx = args.index(flag)
            return args[idx + 1]
        except (ValueError, IndexError):
            return None


__all__ = ["EDRDetectCommandSet"]
