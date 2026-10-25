"""Red Team Gym CLI command set - gamified pentest training.

Integrates with the ELO/karma system and Docker lab scenarios to provide
scored challenges with leaderboards, technique tracking and skill
progression. Definitions live in ``gyms/*.yaml``; active runs persist in
the world model and can be started, inspected and stopped by run id.
"""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    BRIGHT_GREEN,
    CYAN,
    GREEN,
    MAGENTA,
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


class RedTeamGymCommandSet(LazyOwnCommandSet):
    """Red Team Gym — scored pentest challenges with leaderboards."""

    phase = "lab"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_gym(self, line):
        """Red Team Gym — gamified pentest training with ELO scoring.

        Usage:
            gym list                              - show available challenges
            gym start <challenge_id> [--target IP] - begin a challenge
            gym status [run_id]                   - list active gyms or inspect one
            gym stop [run_id|gym_id|name]         - stop one gym; no argument stops all
            gym submit [run_id] [--failed] [--techniques t1,t2,...]
            gym leaderboard|top [top_n]           - show top players
            gym hint [run_id]                     - hint for an active gym

        Challenges award ELO that feeds into the existing karma system
        (Noob -> Rookie -> Skidy -> Hacker -> Pro -> Elite -> Godlike).
        Active runs persist in the world model and survive new sessions.

        Examples:
            gym list
            gym start first_blood_web --target 172.17.0.2
            gym status
            gym status gym0001
            gym stop
            gym submit gym0001 --techniques sqli_manual,csrf_bypass
            gym leaderboard 10
        """
        args = shlex.split(line)
        if not args:
            print_msg("Red Team Gym - gamified pentest training.")
            print_msg("Usage: gym <list|start|status|stop|submit|leaderboard|hint> [options]")
            return

        action = args[0].lower()
        rest = args[1:] if len(args) > 1 else []

        if action == "list":
            self._gym_list()
        elif action == "start":
            self._gym_start(rest)
        elif action == "submit":
            self._gym_submit(rest)
        elif action in ("status", "active"):
            self._gym_status(rest)
        elif action == "stop":
            self._gym_stop(rest)
        elif action in ("leaderboard", "top"):
            self._gym_leaderboard(rest)
        elif action == "hint":
            self._gym_hint(rest)
        else:
            print_error(f"Unknown action: {action}")

    @cmd2.with_category(miscellaneous_category)
    def do_gym_ms2(self, line):
        """Metasploitable 2 gym catalogue: list|chains|validate|info <vuln>|chain <vuln>.

        Usage:
            gym_ms2 list
            gym_ms2 chains
            gym_ms2 validate
            gym_ms2 info vsftpd_backdoor
            gym_ms2 chain ms2_distcc_exec
        """
        import json as _json

        from modules.metasploitable_gym import chain_for, get, summary, validate_matrix, vulnerabilities

        args = shlex.split(line) if line.strip() else ["list"]
        action = args[0].lower()
        if action in ("list", "summary"):
            print(_json.dumps(summary(), indent=2))
            return
        if action == "chains":
            for entry in vulnerabilities():
                print_msg(f"{entry['id']:<34} {entry['chain']:<52} exploit={entry['exploit']:<34} {entry['severity']}")
            return
        if action == "validate":
            errors = validate_matrix()
            if errors:
                for error in errors:
                    print_error(error)
                return
            print_succ("Metasploitable 2 matrix is consistent.")
            return
        if action == "info" and len(args) > 1:
            print(_json.dumps(get(args[1]) or {"error": "not found"}, indent=2))
            return
        if action == "chain" and len(args) > 1:
            chain = chain_for(args[1])
            if chain is None:
                print_error(f"Unknown vulnerability: {args[1]}")
                return
            for step in chain.resolve({"target": "TARGET", "lhost": "LHOST", "lport": "4444"}):
                state = "skip" if step["skipped"] else "run"
                print_msg(f"[{state}] {step['run']} {step['reason']}".strip())
            return
        print_error("Usage: gym_ms2 list|chains|validate|info <vuln>|chain <vuln>")

    def _gym_list(self):
        """Display all available gym challenges."""
        try:
            from modules.redteam_gym import list_challenges
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        challenges = list_challenges()
        if not challenges:
            print_msg("No challenges available.")
            return

        difficulty_colors = {
            "easy": GREEN,
            "medium": YELLOW,
            "hard": RED,
        }

        print_msg("Available Gym Challenges:\n")
        for cid, chal in sorted(challenges.items(), key=lambda x: x[1]["difficulty"]):
            dc = difficulty_colors.get(chal["difficulty"], WHITE)
            print(f"  {BRIGHT_GREEN}{chal['name']}{RESET}")
            print(f"    {CYAN}ID:{RESET}         {cid}")
            print(f"    {MAGENTA}Difficulty:{RESET} {dc}{chal['difficulty']}{RESET}")
            print(f"    {MAGENTA}Scenario:{RESET}   {chal['scenario']}")
            print(f"    {MAGENTA}Phases:{RESET}     {', '.join(chal['phases'])}")
            print(f"    {MAGENTA}Max Points:{RESET} {chal['max_points']}  ({chal['elo_bonus']} ELO bonus)")
            print(f"    {WHITE}{chal['description']}{RESET}")
            print("")

        print_msg("Start a challenge: gym start <challenge_id>")
        print_msg("Requires Docker. Spin up the scenario: lab start <scenario>")

    def _gym_start(self, args: list[str]):
        """Begin a gym challenge."""
        if not args:
            print_error("Specify a challenge ID. Use: gym list")
            return

        challenge_id = args[0]
        target = ""
        if "--target" in args:
            index = args.index("--target")
            if index + 1 < len(args):
                target = args[index + 1]
        try:
            from modules.redteam_gym import start_challenge
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        result = start_challenge(challenge_id, target=target)
        if not result.get("success"):
            print_error(result.get("error", "Failed to start challenge."))
            return

        chal = result["challenge"]
        if result.get("already_active"):
            print_warn(f"Challenge already active as {result['run_id']}.")
        else:
            print_succ(f"Challenge started: {chal['name']} (run {result['run_id']})")
        lab = result.get("lab") or {}
        if lab.get("success"):
            state = "already running" if lab.get("already") else "started"
            print_succ(f"Lab '{chal['scenario']}' {state}: {lab.get('container', '')}")
            if lab.get("ip"):
                print_msg(f"  Container IP: {lab['ip']}")
                print_msg(f"  Assign target: assign rhost {lab['ip']}")
            for container_port, host_port in (lab.get("ports") or {}).items():
                print_msg(f"  Mapped port: {host_port} -> {container_port}")
        elif lab and not lab.get("success"):
            print_warn(f"Lab '{chal['scenario']}' failed to start: {lab.get('error', '')[:200]}")
        print("")
        print_msg(f"  Run ID:      {result['run_id']}")
        print_msg(f"  Objective:   {chal['objective']}")
        print_msg(f"  Difficulty:  {chal['difficulty']}")
        print_msg(f"  Max Points:  {chal['max_points']}")
        print_msg(f"  Phases:      {', '.join(chal['phases'])}")
        if target:
            print_msg(f"  Target:      {target}")
        print_msg(f"  Active gyms: {result.get('active_count', 0)}")
        print("")
        print_msg("Next steps:")
        for step in result.get("next_steps", []):
            print_msg(f"  {step}")
        print("")
        hints = chal.get("hints", [])
        if hints:
            print_msg(f"Hint: {hints[0]}")
        print_msg("")
        print_msg(f"When done: gym submit {result['run_id']} --techniques <t1,t2,...>")
        print_msg(f"Stop it:   gym stop {result['run_id']}  (or gym stop for all)")

    def _gym_submit(self, args: list[str]):
        """Submit a completed challenge for scoring."""
        success = True
        techniques: list[str] = []
        run_id = ""

        i = 0
        while i < len(args):
            if args[i] == "--failed":
                success = False
            elif args[i] == "--techniques" and i + 1 < len(args):
                i += 1
                techniques = [t.strip() for t in args[i].split(",") if t.strip()]
            elif not args[i].startswith("-") and not run_id:
                run_id = args[i]
            i += 1

        try:
            from modules.redteam_gym import submit_challenge
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        print_msg("Submitting challenge for scoring...")
        result = submit_challenge(techniques_used=techniques, success=success, run_id=run_id)

        if not result.get("success"):
            print_error(result.get("error", "Submission failed."))
            return

        if result["completed"]:
            scores = result["scores"]
            print_succ(f"Challenge completed: {result['challenge']} (run {result.get('run_id', '')})")
            print("")
            print_msg(f"  Time: {result.get('elapsed_seconds', 0)}s")
            print_msg(f"  Speed score:      {scores['speed']}")
            print_msg(f"  Stealth score:    {scores['stealth']}")
            print_msg(f"  Technique score:  {scores['technique_diversity']}")
            print(f"  {BRIGHT_GREEN}Total score:      {scores['total']} / {scores['max_possible']}{RESET}")
            print_msg(f"  ELO awarded:      +{result.get('elo_awarded', 0)}")
            print_msg(f"  Leaderboard rank: #{result.get('rank', '?')}")
            if result.get("techniques_used"):
                print_msg(f"  Techniques: {', '.join(result['techniques_used'])}")
        else:
            print_warn(f"Challenge '{result['challenge']}' submitted as failed.")
            print_msg("No ELO awarded. Try again!")

    @staticmethod
    def _format_elapsed(seconds: int) -> str:
        """Return a compact ``Xm Ys`` elapsed label."""
        minutes, secs = divmod(max(0, int(seconds)), 60)
        return f"{minutes}m {secs}s"

    def _gym_status(self, args: list[str]):
        """List active gyms or inspect one by run id, gym id or name."""
        try:
            from modules.redteam_gym import engagement_context, get_active_challenge, get_active_challenges
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        if args:
            selector = " ".join(args).strip()
            active = get_active_challenge(selector)
            if not active:
                print_error(f"No active gym matches: {selector}")
                return
            print_msg(f"Active Gym: {active['name']}")
            print_msg(f"  Run ID:     {active['run_id']}")
            print_msg(f"  Gym ID:     {active['challenge_id']}")
            print_msg(f"  Operator:   {active.get('operator', '')}")
            print_msg(f"  Objective:  {active['objective']}")
            print_msg(f"  Elapsed:    {self._format_elapsed(active.get('elapsed_seconds', 0))}")
            if active.get("target"):
                print_msg(f"  Target:     {active['target']}")
            if active.get("hint"):
                print_msg(f"  Hint:       {active['hint']}")
            print_msg("")
            print_msg(f"Submit: gym submit {active['run_id']} --techniques <t1,t2,...>")
            print_msg(f"Stop:   gym stop {active['run_id']}")
            return

        runs = get_active_challenges()
        if not runs:
            context = engagement_context()
            print_msg("No active gyms.")
            live = context.get("live_shells") or []
            hosts = context.get("hosts") or []
            states = context.get("host_states") or {}
            ignored = context.get("ignored_hosts") or []
            target = str(context.get("target", "") or "")
            if live or hosts:
                if live:
                    rendered = ", ".join(f"{row.get('target', '')} via {row.get('via', '')}" for row in live)
                    print_msg(f"Live shell sessions (not gym runs): {rendered}")
                if hosts:
                    rendered = ", ".join(f"{ip} ({states.get(ip, 'compromised')})" for ip in hosts)
                    print_msg(f"Engagement context: compromised hosts={rendered}")
                print_msg("A shell or exploit does not create a gym run.")
                print_msg("Track one with: gym start <challenge_id> [--target <ip>]")
            else:
                if target:
                    print_msg(f"Engagement context: no compromised host matches {target}.")
                print_msg("Start one: gym start <challenge_id>")
            if ignored:
                shown = ", ".join(ignored[:4]) + ("..." if len(ignored) > 4 else "")
                print_msg(f"Ignored unrelated world-model host(s): {shown}")
                print_msg("Prune stale state: python3 -m modules.world_model remove-host <ip>")
            return
        print_msg(f"Active gyms: {len(runs)}")
        for run in runs:
            print_msg(
                f"  {run['run_id']}  {run['challenge_id']}  "
                f"operator={run.get('operator', '')}  "
                f"elapsed={self._format_elapsed(run.get('elapsed_seconds', 0))}  "
                f"target={run.get('target', '') or '-'}"
            )
        print_msg("")
        print_msg("Inspect: gym status <run_id>")
        print_msg("Stop all: gym stop")

    def _gym_stop(self, args: list[str]):
        """Stop one gym by run id, gym id or name; no argument stops all."""
        try:
            from modules.redteam_gym import stop_challenges
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        selector = " ".join(args).strip() if args else ""
        result = stop_challenges(selector)
        if not result.get("count"):
            if selector:
                print_warn(f"No active gym matches: {selector}")
            else:
                print_msg("No active gyms.")
            return
        print_succ(f"Stopped {result['count']} gym(s).")
        for run in result.get("stopped", []):
            print_msg(f"  {run.get('run_id', '')}  {run.get('challenge_id', '')}  operator={run.get('operator', '')}")

    def _gym_leaderboard(self, args: list[str]):
        """Show the gym leaderboard."""
        top_n = 15
        if args:
            try:
                top_n = int(args[0])
            except ValueError:
                pass

        try:
            from modules.redteam_gym import show_leaderboard
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        board = show_leaderboard(top_n)
        if not board:
            print_msg("Leaderboard is empty. Complete a challenge to appear!")
            return

        print(f"\n  {BRIGHT_GREEN}Red Team Gym Leaderboard{RESET}")
        print(f"  {'Rank':<6} {'Operator':<20} {'Score':<10} {'Challenges':<12} {'ELO':<8}")
        print(f"  {'-' * 6} {'-' * 20} {'-' * 10} {'-' * 12} {'-' * 8}")

        for entry in board:
            rank = entry["rank"]
            name = entry["username"][:19]
            score = entry["total_score"]
            completed = entry["challenges_completed"]
            elo = entry["elo_from_gym"]
            print(f"  {rank:<6} {name:<20} {score:<10} {completed:<12} {elo:<8}")

        print("")

    def _gym_hint(self, args: list[str] | None = None):
        """Get the next hint for an active challenge."""
        try:
            from modules.redteam_gym import GYM_CHALLENGE_DEFINITIONS, get_active_challenge
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return
        selector = " ".join(args or []).strip()
        active = get_active_challenge(selector)
        if not active:
            if selector:
                print_error(f"No active gym matches: {selector}")
            else:
                print_msg("No active gyms. Start one: gym start <challenge_id>")
            return
        chal = GYM_CHALLENGE_DEFINITIONS.get(active["challenge_id"])
        if not chal:
            print_error("Challenge definition not found.")
            return
        hints = chal.get("hints", [])
        if not hints:
            print_msg("No hints available for this gym.")
            return
        elapsed = active.get("elapsed_seconds", 0)
        hint_index = min(len(hints) - 1, int(elapsed // 300))
        print_msg(f"Hint ({hint_index + 1}/{len(hints)}): {hints[hint_index]}")


__all__ = ["RedTeamGymCommandSet"]
