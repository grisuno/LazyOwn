"""Purple Team CommandSet: closed-loop offensive detection measurement.

Exposes commands that orchestrate the red->blue->purple cycle:

* ``purple_exec`` — execute a red action and measure detection via LazyOwnBT
* ``purple_test`` — measure without executing (dry-run, ai_test only)
* ``purple_score`` — show current engagement detection score
* ``purple_report`` — generate full engagement report with datasets
* ``purple_methods`` — list available detection methods
* ``purple_config`` — show/update purple team configuration
* ``purple_history`` — show recent purple team results

Each command generates CSV datasets for ML training and feedback for
the DetectionOracle calibration loop.
"""

from __future__ import annotations

import argparse
from typing import Any

from cmd2 import Cmd2ArgumentParser, with_argparser, with_category

from cli.commands._base import LazyOwnCommandSet

_CATEGORY = "Purple Team"


def _build_exec_parser() -> Cmd2ArgumentParser:
    parser = Cmd2ArgumentParser(prog="purple_exec")
    parser.add_argument("command", nargs="+", help="Command and arguments (e.g. nmap -sV 127.0.0.1)")
    parser.add_argument(
        "--category",
        "-c",
        default=None,
        choices=[
            "recon",
            "enum",
            "exploit",
            "credential",
            "lateral",
            "privesc",
            "payload",
            "brute_force",
            "intrusion",
            "other",
        ],
        help="Kill-chain category",
    )
    parser.add_argument(
        "--delay",
        "-d",
        type=int,
        default=None,
        help="Override detection delay (seconds)",
    )
    parser.add_argument(
        "--methods",
        "-m",
        nargs="+",
        default=None,
        help="Override detection methods to use",
    )
    return parser


def _build_test_parser() -> Cmd2ArgumentParser:
    parser = Cmd2ArgumentParser(prog="purple_test")
    parser.add_argument("command", help="Command to test against BT detection")
    parser.add_argument("args", nargs="?", default="", help="Command arguments")
    parser.add_argument(
        "--category",
        "-c",
        default="other",
        choices=[
            "recon",
            "enum",
            "exploit",
            "credential",
            "lateral",
            "privesc",
            "payload",
            "brute_force",
            "intrusion",
            "other",
        ],
        help="Kill-chain category",
    )
    return parser


def _build_config_parser() -> Cmd2ArgumentParser:
    parser = Cmd2ArgumentParser(prog="purple_config")
    parser.add_argument(
        "action",
        nargs="?",
        default="show",
        choices=["show", "set", "methods"],
        help="show=current config, set=update a key, methods=list detection methods",
    )
    parser.add_argument("key", nargs="?", default="", help="Config key to set")
    parser.add_argument("value", nargs="?", default="", help="New value")
    return parser


def _build_history_parser() -> Cmd2ArgumentParser:
    parser = Cmd2ArgumentParser(prog="purple_history")
    parser.add_argument(
        "--last",
        "-n",
        type=int,
        default=10,
        help="Number of recent results to show",
    )
    parser.add_argument(
        "--category",
        "-c",
        default=None,
        help="Filter by category",
    )
    return parser


class PurpleTeamCommandSet(LazyOwnCommandSet):
    """Purple team orchestration commands for the LazyOwn shell."""

    phase = "purple"
    category = _CATEGORY

    def _get_loop(self, **overrides: Any) -> Any:
        """Build a PurpleTeamLoop from payload.json config."""
        from modules.auto_purple import PurpleTeamLoop, load_config_from_payload

        cfg = load_config_from_payload(self.params)
        merged = {**cfg, **{k: v for k, v in overrides.items() if v is not None}}
        return PurpleTeamLoop(
            bt_path=merged.get("bt_path"),
            detection_delay=merged.get("detection_delay", 5),
            methods=merged.get("methods"),
            auto_feedback=merged.get("auto_feedback", True),
        )

    @with_category(_CATEGORY)
    def do_purple_exec(self, line: str) -> None:
        """Execute a red action and measure if LazyOwnBT detects it.

        Usage: purple_exec <command> [args...] [category]
        The last word is category if it matches a known category.
        Example: purple_exec nmap -sV 127.0.0.1 recon
        Example: purple_exec lazynmap recon
        """
        if not line.strip():
            self.poutput("Usage: purple_exec <command> [args...] [category]")
            return

        known_categories = {
            "recon",
            "enum",
            "exploit",
            "credential",
            "lateral",
            "privesc",
            "payload",
            "brute_force",
            "intrusion",
            "other",
        }

        parts = line.strip().split()
        category = "other"
        if parts[-1] in known_categories:
            category = parts.pop()

        if not parts:
            self.poutput("Usage: purple_exec <command> [args...] [category]")
            return

        command = parts[0]
        args_str = " ".join(parts[1:]) if len(parts) > 1 else ""

        loop = self._get_loop()
        result = loop.execute_and_measure(command, args_str, category)

        self.poutput(f"\n  Command    : {result.command} {result.args}")
        self.poutput(f"  Category   : {result.category}")
        self.poutput(f"  Oracle pred: {result.oracle_prediction:.1%}")
        self.poutput(f"  Detected   : {'YES' if result.actually_detected else 'NO'}")
        self.poutput("  Methods    :")
        for method, detected in result.detection_methods.items():
            status = "DETECTED" if detected else "missed"
            self.poutput(f"    {method:20s} : {status}")

        if result.actually_detected:
            self.poutput("\n  [!] Action was detected by blue team")
        else:
            self.poutput("\n  [+] Action evaded all detection methods")

        self.poutput("  Dataset    : sessions/purple_dataset.csv")
        self.poutput("  Audit      : sessions/purple_audit.jsonl\n")

    @with_argparser(_build_test_parser())
    @with_category(_CATEGORY)
    def do_purple_test(self, args: argparse.Namespace) -> None:
        """Test if LazyOwnBT would detect a command (no execution).

        Dry-run mode: queries BT detection methods without actually
        executing the red action. Useful for pre-engagement assessment.
        """
        loop = self._get_loop()
        result = loop.measure_only(args.command, args.args, args.category)

        self.poutput(f"\n  Command    : {result.command} {result.args}")
        self.poutput(f"  Category   : {result.category}")
        self.poutput(f"  Oracle pred: {result.oracle_prediction:.1%}")
        self.poutput(f"  Detected   : {'YES' if result.actually_detected else 'NO'}")
        self.poutput("  Methods    :")
        for method, detected in result.detection_methods.items():
            status = "DETECTED" if detected else "missed"
            self.poutput(f"    {method:20s} : {status}")
        self.poutput("")

    @with_category(_CATEGORY)
    def do_purple_score(self, line: str) -> None:
        """Show current engagement detection score.

        Displays total actions, detection rate, per-category and per-method
        breakdowns. Written to sessions/purple_score.json.
        """
        loop = self._get_loop()
        score = loop.engagement_score()

        if score.total == 0:
            self.poutput("\n  No purple team actions recorded yet.")
            self.poutput("  Use 'purple_exec <command>' to start measuring.\n")
            return

        self.poutput(f"\n  {'=' * 50}")
        self.poutput("  PURPLE TEAM ENGAGEMENT SCORE")
        self.poutput(f"  {'=' * 50}")
        self.poutput(f"  Total actions : {score.total}")
        self.poutput(f"  Detected      : {score.detected}")
        self.poutput(f"  Missed        : {score.missed}")
        self.poutput(f"  Detection rate: {score.score:.1%}")

        if score.score <= 0.3:
            self.poutput("  Rating        : STEALTH (excellent evasion)")
        elif score.score <= 0.6:
            self.poutput("  Rating        : MODERATE (some detection)")
        elif score.score <= 0.8:
            self.poutput("  Rating        : NOISY (high detection)")
        else:
            self.poutput("  Rating        : VISIBLE (almost all detected)")

        if score.by_category:
            self.poutput("\n  By Category:")
            for cat, stats in score.by_category.items():
                rate = stats["detected"] / stats["total"] if stats["total"] > 0 else 0
                bar = "#" * int(rate * 20) + "." * (20 - int(rate * 20))
                self.poutput(f"    {cat:15s} [{bar}] {stats['detected']}/{stats['total']} ({rate:.0%})")

        if score.by_method:
            self.poutput("\n  By Detection Method:")
            for method, stats in score.by_method.items():
                rate = stats["detected"] / stats["total"] if stats["total"] > 0 else 0
                bar = "#" * int(rate * 20) + "." * (20 - int(rate * 20))
                self.poutput(f"    {method:20s} [{bar}] {stats['detected']}/{stats['total']} ({rate:.0%})")

        self.poutput(f"  {'=' * 50}\n")

    @with_category(_CATEGORY)
    def do_purple_report(self, line: str) -> None:
        """Generate full engagement report with datasets.

        Produces sessions/purple_report.json with score, oracle accuracy,
        per-action results, and dataset paths for ML training.
        """
        loop = self._get_loop()
        path = loop.export_report()
        self.poutput(f"\n  Report exported to: {path}")
        self.poutput("  CSV dataset       : sessions/purple_dataset.csv")
        self.poutput("  Oracle feedback   : sessions/detection_feedback.jsonl")
        self.poutput("  Audit log         : sessions/purple_audit.jsonl\n")

    @with_category(_CATEGORY)
    def do_purple_methods(self, line: str) -> None:
        """List available LazyOwnBT detection methods."""
        from modules.auto_purple import _DETECTION_METHODS

        self.poutput(f"\n  {'Method':20s}  {'Parser':18s}  Description")
        self.poutput(f"  {'-' * 70}")
        for m in _DETECTION_METHODS:
            self.poutput(f"  {m.name:20s}  {m.output_parser:18s}  {m.description}")
        self.poutput("")

    @with_argparser(_build_config_parser())
    @with_category(_CATEGORY)
    def do_purple_config(self, args: argparse.Namespace) -> None:
        """Show or update purple team configuration (payload.json)."""
        from modules.auto_purple import load_config_from_payload

        if args.action == "show":
            cfg = load_config_from_payload(self.params)
            self.poutput("\n  Purple Team Configuration:")
            self.poutput(f"  {'=' * 40}")
            for k, v in cfg.items():
                self.poutput(f"  {k:20s} : {v}")
            self.poutput("")
            return

        if args.action == "methods":
            from modules.auto_purple import _DETECTION_METHODS

            self.poutput(f"\n  Available methods: {', '.join(m.name for m in _DETECTION_METHODS)}")
            self.poutput(f"  Current: {', '.join(load_config_from_payload(self.params).get('methods', []))}")
            self.poutput("")
            return

        if args.action == "set":
            if not args.key or not args.value:
                self.poutput("  Usage: purple_config set <key> <value>")
                self.poutput(
                    "  Keys: enabled, lazyownbt_path, detection_delay, methods, auto_feedback, score_threshold"
                )
                return

            from core.config import load_payload, save_payload

            payload = load_payload()
            pt = payload.get("purple_team", {})

            key = args.key
            value = args.value

            if key in ("enabled", "auto_feedback"):
                pt[key] = value.lower() in ("true", "1", "yes")
            elif key == "detection_delay":
                pt[key] = int(value)
            elif key == "score_threshold":
                pt[key] = float(value)
            elif key == "methods":
                pt[key] = [m.strip() for m in value.split(",")]
            else:
                pt[key] = value

            payload["purple_team"] = pt
            save_payload(payload)
            self.poutput(f"  Set {key} = {pt[key]}")

    @with_category(_CATEGORY)
    def do_purple_dashboard(self, line: str) -> None:
        """Launch the Purple Team TUI dashboard.

        Full-screen Textual interface showing engagement score,
        detection rates, recent actions, and ML dataset stats.
        Press Q to return to the shell.
        """
        try:
            from cli.purple_tui import launch

            launch()
        except ImportError as e:
            self.perror(f"Textual not available: {e}")
            self.poutput("  Install with: pip install textual")

    @with_argparser(_build_history_parser())
    @with_category(_CATEGORY)
    def do_purple_history(self, args: argparse.Namespace) -> None:
        """Show recent purple team action results."""
        loop = self._get_loop()
        results = loop.last_results(args.last)

        if not results:
            self.poutput("\n  No results yet. Use 'purple_exec' to start measuring.\n")
            return

        filtered = results
        if args.category:
            filtered = [r for r in results if r.category == args.category]

        self.poutput(f"\n  {'Time':20s}  {'Command':30s}  {'Cat':12s}  {'Oracle':8s}  {'Detected':8s}")
        self.poutput(f"  {'-' * 82}")
        for r in filtered:
            ts = r.timestamp[11:19] if len(r.timestamp) > 19 else r.timestamp
            cmd = f"{r.command} {r.args}"[:30]
            det = "YES" if r.actually_detected else "NO"
            self.poutput(f"  {ts:20s}  {cmd:30s}  {r.category:12s}  {r.oracle_prediction:.0%}     {det:8s}")
        self.poutput("")
