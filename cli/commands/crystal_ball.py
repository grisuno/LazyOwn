"""Crystal Ball CLI command set — privilege escalation vector prediction.

Parses linpeas/winpeas output and suggests ranked privesc vectors
with exact commands, CVE references, and MITRE ATT&CK mapping.
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    GREEN,
    RED,
    RESET,
    WHITE,
    YELLOW,
    miscellaneous_category,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)


class CrystalBallCommandSet(LazyOwnCommandSet):
    """Crystal Ball — privesc vector prediction and ranking."""

    phase = "privesc"
    category = "06. Privilege Escalation"

    @cmd2.with_category("06. Privilege Escalation")
    def do_crystal_ball(self, line):
        """Analyze linpeas/winpeas output and rank privesc vectors with exact commands.

        Usage:
            crystal_ball <file>               Analyse enumeration output file
            crystal_ball --text "<output>"     Analyse raw text from clipboard
            crystal_ball --auto                Auto-detect linpeas/winpeas in sessions/

        Matches kernel CVEs, SUID binaries (GTFOBins), capabilities, sudo rules,
        group memberships (docker/lxd), and cron jobs. When an LLM backend is
        configured, additional context-aware vectors are suggested.

        Examples:
            crystal_ball sessions/linpeas_10.0.2.15.txt
            crystal_ball --auto
        """
        import shlex

        args = shlex.split(line)
        filepath = None
        raw_text = None
        use_auto = False

        i = 0
        while i < len(args):
            if args[i] == "--text" and i + 1 < len(args):
                i += 1
                raw_text = args[i]
            elif args[i] == "--auto":
                use_auto = True
            elif not args[i].startswith("--") and not filepath:
                filepath = args[i]
            i += 1

        if use_auto:
            filepath = _auto_detect_enum_file()
            if not filepath:
                print_warn("No linpeas/winpeas output found in sessions/.")
                print_warn("Run linpeas or winpeas first, or specify a file.")
                return

        if filepath:
            import os

            if not os.path.isfile(filepath):
                print_error(f"File not found: {filepath}")
                return
            print_msg(f"Analysing: {filepath}")
        elif not raw_text:
            print_error("Specify a file, --text, or --auto.")
            print_msg("Usage: crystal_ball <file> | crystal_ball --text \"output\" | crystal_ball --auto")
            return

        try:
            from modules.privesc_predictor import analyze_privesc, format_crystal_ball_output
        except ImportError as exc:
            print_error(f"Privesc predictor not available: {exc}")
            return

        print_msg("Analysing enumeration data for privesc vectors...")

        try:
            result = analyze_privesc(filepath=filepath, text=raw_text)
        except Exception as exc:
            print_error(f"Analysis failed: {exc}")
            return

        formatted = format_crystal_ball_output(result)
        print(formatted)

        vectors = result.get("vectors", [])
        if vectors:
            output_path = f"sessions/crystal_ball_{_safe_filename(vectors[0].get('name', 'report'))}.json"
            try:
                import json

                with open(output_path, "w") as f:
                    json.dump(result, f, indent=2)
                print_succ(f"Results saved to {output_path}")
            except Exception:
                pass

    @cmd2.with_category("06. Privilege Escalation")
    def do_privesc_suggest(self, line):
        """Quick alias for crystal_ball --auto.

        Usage:
            privesc_suggest
        """
        self.do_crystal_ball("--auto")


def _auto_detect_enum_file() -> str | None:
    """Find linpeas or winpeas output in sessions/.

    Returns:
        Absolute path to the most recent enumeration file, or None.
    """
    import glob
    import os

    patterns = [
        "sessions/linpeas*.txt",
        "sessions/linpeas_*.txt",
        "sessions/linpeas*.log",
        "sessions/winpeas*.txt",
        "sessions/winpeas*.log",
        "sessions/*peas*.txt",
        "sessions/*peas*.log",
    ]

    candidates: list[tuple[str, float]] = []
    for pattern in patterns:
        for path in glob.glob(pattern):
            mtime = os.path.getmtime(path)
            candidates.append((path, mtime))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def _safe_filename(name: str) -> str:
    """Sanitise a string for use as a filename component."""
    import re

    return re.sub(r"[^\w\-_.]", "_", name)[:50]


__all__ = ["CrystalBallCommandSet"]
