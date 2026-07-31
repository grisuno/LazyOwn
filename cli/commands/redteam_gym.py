"""Red Team Gym CLI command set — gamified pentest training.

Integrates with the ELO/karma system and Docker lab scenarios to
provide scored challenges with leaderboards, technique tracking,
and skill progression.
"""

from __future__ import annotations

import cmd2
import shlex
import time

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
            gym list                    — show available challenges
            gym start <challenge_id>    — begin a challenge
            gym submit [--failed] [--techniques t1,t2,...]  — submit completed challenge
            gym status                  — show active challenge
            gym leaderboard [top_n]     — show top players
            gym hint                    — get a hint for the active challenge

        Challenges award ELO that feeds into the existing karma system
        (Noob -> Rookie -> Skidy -> Hacker -> Pro -> Elite -> Godlike).

        Examples:
            gym list
            gym start first_blood_web
            gym submit --techniques sqli_manual,csrf_bypass
            gym leaderboard 10
        """
        args = shlex.split(line)
        if not args:
            print_msg("Red Team Gym — gamified pentest training.")
            print_msg("Usage: gym <list|start|submit|status|leaderboard|hint> [options]")
            return

        action = args[0].lower()
        rest = args[1:] if len(args) > 1 else []

        if action == "list":
            self._gym_list()
        elif action == "start":
            self._gym_start(rest)
        elif action == "submit":
            self._gym_submit(rest)
        elif action == "status":
            self._gym_status()
        elif action == "leaderboard":
            self._gym_leaderboard(rest)
        elif action == "hint":
            self._gym_hint()
        else:
            print_error(f"Unknown action: {action}")

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
        try:
            from modules.redteam_gym import start_challenge
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        result = start_challenge(challenge_id)
        if not result.get("success"):
            print_error(result.get("error", "Failed to start challenge."))
            return

        chal = result["challenge"]
        print_succ(f"Challenge started: {chal['name']}")
        print("")
        print_msg(f"  Objective:   {chal['objective']}")
        print_msg(f"  Difficulty:  {chal['difficulty']}")
        print_msg(f"  Max Points:  {chal['max_points']}")
        print_msg(f"  Phases:      {', '.join(chal['phases'])}")
        print("")
        print_msg("Next steps:")
        for step in result.get("next_steps", []):
            print_msg(f"  {step}")
        print("")
        hints = chal.get("hints", [])
        if hints:
            print_msg(f"Hint: {hints[0]}")
        print_msg("")
        print_msg("When done, submit: gym submit --techniques <t1,t2,...>")
        print_msg("Give up? gym submit --failed")

    def _gym_submit(self, args: list[str]):
        """Submit a completed challenge for scoring."""
        success = True
        techniques: list[str] = []

        i = 0
        while i < len(args):
            if args[i] == "--failed":
                success = False
            elif args[i] == "--techniques" and i + 1 < len(args):
                i += 1
                techniques = [t.strip() for t in args[i].split(",")]
            i += 1

        try:
            from modules.redteam_gym import submit_challenge
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        print_msg("Submitting challenge for scoring...")
        result = submit_challenge(techniques_used=techniques, success=success)

        if not result.get("success"):
            print_error(result.get("error", "Submission failed."))
            return

        if result["completed"]:
            scores = result["scores"]
            print_succ(f"Challenge completed: {result['challenge']}")
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

    def _gym_status(self):
        """Show the currently active challenge."""
        try:
            from modules.redteam_gym import get_active_challenge
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return

        active = get_active_challenge()
        if not active:
            print_msg("No active challenge.")
            print_msg("Start one: gym start <challenge_id>")
            return

        print_msg(f"Active Challenge: {active['name']}")
        print_msg(f"  Objective: {active['objective']}")
        elapsed = active.get("elapsed_seconds", 0)
        mins, secs = divmod(elapsed, 60)
        print_msg(f"  Elapsed:   {int(mins)}m {int(secs)}s")
        hint = active.get("hint")
        if hint:
            print_msg(f"  Hint:      {hint}")
        print_msg("")
        print_msg("Submit: gym submit --techniques <t1,t2,...>")

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
        print(f"  {'-'*6} {'-'*20} {'-'*10} {'-'*12} {'-'*8}")

        for entry in board:
            rank = entry["rank"]
            name = entry["username"][:19]
            score = entry["total_score"]
            completed = entry["challenges_completed"]
            elo = entry["elo_from_gym"]
            print(f"  {rank:<6} {name:<20} {score:<10} {completed:<12} {elo:<8}")

        print("")

    def _gym_hint(self):
        """Get the next hint for the active challenge."""
        try:
            from modules.redteam_gym import get_active_challenge

            active = get_active_challenge()
            if not active:
                print_msg("No active challenge. Start one: gym start <challenge_id>")
                return

            from modules.redteam_gym import GYM_CHALLENGE_DEFINITIONS

            chal = GYM_CHALLENGE_DEFINITIONS.get(active["challenge_id"])
            if not chal:
                print_error("Challenge definition not found.")
                return

            hints = chal.get("hints", [])
            elapsed = active.get("elapsed_seconds", 0)

            hint_index = min(len(hints) - 1, int(elapsed // 300))
            if hint_index < len(hints):
                print_msg(f"Hint ({hint_index + 1}/{len(hints)}): {hints[hint_index]}")
            else:
                print_msg("No more hints available. You're on your own!")
        except ImportError as exc:
            print_error(f"Gym module not available: {exc}")
            return


__all__ = ["RedTeamGymCommandSet"]
