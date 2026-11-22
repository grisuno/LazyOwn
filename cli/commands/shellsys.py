"""Local shell and system extracted from the miscellaneous cluster.

Pending status: originals deleted from ``cli/commands/misc.py``;
this set is registered by ``cli.registry``.
"""

from __future__ import annotations

import os
import subprocess
from datetime import date, datetime, timedelta
from threading import Timer

import cmd2

from cli.commands._base import LazyOwnCommandSet
from core.safe_exec import safe_run_shell as _safe_run_shell
from core.session_secrets import rotate_session_secrets
from modules import session_reclaim
from utils import RESET, print_error, print_msg, print_warn

__all__ = ["ShellSysCommandSet"]

_CLEAN_SUBSETS = tuple(session_reclaim.SUBSET_PATTERNS)
_CLEAN_MAX_LISTED = 12


def _print_cleanup_plan(plan: session_reclaim.CleanupPlan, include_sensitive: bool) -> None:
    """Render an audited cleanup plan to the operator without deleting anything.

    Args:
        plan: The partitioned plan produced by ``session_reclaim.build_plan``.
        include_sensitive: Whether the sensitive tier is in the removal scope.
    """
    scope = f"subset '{plan.subset}'" if plan.subset else "full sessions/"
    print_msg(f"Cleanup audit for {scope} ({plan.sessions_dir})")

    protected = plan.by_tier(session_reclaim.TIER_PROTECTED)
    if protected:
        kept = session_reclaim.human_size(plan.tier_bytes(session_reclaim.TIER_PROTECTED))
        print_msg(f"  PROTECTED (never removed): {len(protected)} items, {kept}")

    sensitive_groups = plan.grouped(session_reclaim.TIER_SENSITIVE)
    if sensitive_groups:
        tag = "will be removed (--all)" if include_sensitive else "kept; add --all to remove"
        total = session_reclaim.human_size(plan.tier_bytes(session_reclaim.TIER_SENSITIVE))
        print_warn(f"  SENSITIVE ({tag}): {_count(sensitive_groups)} items, {total}")
        _print_groups(sensitive_groups, list_entries=True)

    reclaim_groups = plan.grouped(session_reclaim.TIER_RECLAIM)
    reclaim_total = session_reclaim.human_size(plan.tier_bytes(session_reclaim.TIER_RECLAIM))
    print_msg(f"  RECLAIM (removed by --force): {_count(reclaim_groups)} items, {reclaim_total}")
    _print_groups(reclaim_groups, list_entries=False)

    now = plan.tier_bytes(session_reclaim.TIER_RECLAIM)
    with_all = now + plan.tier_bytes(session_reclaim.TIER_SENSITIVE)
    reclaimable = session_reclaim.human_size(now)
    reclaimable_all = session_reclaim.human_size(with_all)
    print_msg(f"  Reclaimable now: {reclaimable}  |  with --all: {reclaimable_all}")


def _print_groups(groups: dict, list_entries: bool) -> None:
    """Print one summary line per label group, optionally listing entries."""
    for label, entries in groups.items():
        size = session_reclaim.human_size(sum(item.size_bytes for item in entries))
        print_msg(f"    - {label}: {len(entries)} items, {size}")
        if not list_entries:
            continue
        for entry in entries[:_CLEAN_MAX_LISTED]:
            print_msg(f"        {entry.display_name} ({session_reclaim.human_size(entry.size_bytes)})")
        if len(entries) > _CLEAN_MAX_LISTED:
            print_msg(f"        ... and {len(entries) - _CLEAN_MAX_LISTED} more")


def _count(groups: dict) -> int:
    """Return the total number of entries across all label groups."""
    return sum(len(entries) for entries in groups.values())


class ShellSysCommandSet(LazyOwnCommandSet):
    """Local shell and system."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_sh(self, line):
        """
        Executes a shell command directly from the LazyOwn interface.

        This function allows the user to execute arbitrary shell commands without exiting the LazyOwn shell.
        It checks if a command is provided, prints a message indicating the command being executed, and then
        runs the command using `os.system`.

        Usage:
            sh <command>

        :param line: The shell command to be executed.
        :type line: str
        :raises ValueError: If no command is provided, an error message is printed indicating that a command is required.
        :returns: None

        Example:
            sh ls -la
            # This will execute 'ls -la' in the shell without exiting LazyOwn.

        Note:
            Ensure that the command provided is safe to execute and does not include potentially harmful operations.

        """
        if not line:
            print_error("You must pass the command linke argument")
            return

        self.cmd(f"{line}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_sys(self, line):
        """
        Executes a shell command directly from the LazyOwn interface.

        This function allows the user to execute arbitrary shell commands without exiting the LazyOwn shell.
        It checks if a command is provided, prints a message indicating the command being executed, and then
        runs the command through the audited safe_run_shell gate with output capture.

        Usage:
            sh <command>

        :param line: The shell command to be executed.
        :type line: str
        :raises ValueError: If no command is provided, an error message is printed indicating that a command is required.
        :returns: None

        Example:
            sh ls -la
            # This will execute 'ls -la' in the shell without exiting LazyOwn.

        Note:
            Ensure that the command provided is safe to execute and does not include potentially harmful operations.

        """
        if not line:
            print_error("You must pass the command linke argument")
            return

        try:
            result = _safe_run_shell(
                line,
                allow=True,
                reason="operator issued the sh shell command",
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            print_error("Command timed out after 60 seconds")
            return
        except (ValueError, PermissionError) as exc:
            print_error(f"Command rejected: {exc}")
            return
        if result.stdout:
            print_msg(result.stdout)
        if result.stderr:
            print_error(result.stderr)
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_pwd(self, line):
        """
        Displays the current working directory and lists files, and copies the current directory path to the clipboard.

        This function performs the following tasks:
        1. Displays the current working directory with `pwd` and lists files in the directory using `ls`.
        2. Copies the current directory path to the clipboard using `xclip`.

        Usage:
            pwd

        :param line: This parameter is not used in the function but is included for consistency with other command methods.
        :type line: str
        :returns: None

        Manual execution:
            1. The command `echo -e "[\\e[96m\\`pwd\\`\\e[0m]\\e[34m" && ls && echo -en "\\e[0m"` is executed to display the current working directory and list files in it.
            2. The current directory path is copied to the clipboard using the command `pwd | xclip -sel clip`.

        Dependencies:
            - The function relies on `echo`, `pwd`, `ls`, and `xclip` to display the directory and copy the path to the clipboard.

        Example:
            pwd
            # This will display the current working directory, list files, and copy the current directory path to the clipboard.

        Note:
            Ensure that `xclip` is installed on your system for copying to the clipboard to work.
        """
        print_msg(f'Try echo -e "[\\e[96m`pwd`\\e[0m]\\e[34m" && ls && echo -en "\\e[0m"{RESET}')
        self.cmd('echo -e "[\\e[96m`pwd`\\e[0m]\\e[34m" && ls && echo -en "\\e[0m"')
        self.cmd("pwd | xclip -sel clip")
        print_msg(f" pwd directory copied to clipboard{RESET}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_nano(self, line):
        """
        Opens or creates the file using line in the sessions directory for editing using nano.

        :param line: name of the file to use in nano in session directory.

        :returns: None
        """
        if not line:
            line = input("    [!] enter the filename: ") or "unamed_lazyownfile"
        users_file_path = os.path.join("sessions", line)
        print_msg(users_file_path)
        if not os.path.exists(users_file_path):
            print_warn(f"{users_file_path} does not exist. Creating the file.")
            os.makedirs(os.path.dirname(users_file_path), exist_ok=True)
            with open(users_file_path, "w"):
                pass

        print_msg(f"Opening {users_file_path} with nano for editing.")
        self.cmd(f"nano {users_file_path} -l")

        return

    @cmd2.with_category("12. Miscellaneous")
    def do_cron(self, line):
        """
        Schedules a command to run at a specified time.

        This function allows users to schedule a command to execute at a specific hour and minute.
        If the specified time has already passed for the current day, the command will be scheduled
        to run the following day.

        Usage:
            cron HH:MM command [args]

        Parameters:
        line (str): The input string containing the scheduled time in 'HH:MM' format followed by the command and arguments.

        Returns:
        None
        """
        if not line:
            print_error("Enter the hour and the command")
            return

        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            print_error("Format: cron HH:MM command [args]")
            return

        time_str, command = parts
        try:
            schedule_time = datetime.strptime(time_str, "%H:%M").time()
            now = datetime.now().time()

            delta = datetime.combine(date.today(), schedule_time) - datetime.combine(date.today(), now)
            if delta.total_seconds() < 0:
                delta += timedelta(days=1)

            def lazyrun_command():
                self.onecmd(command)

            Timer(delta.total_seconds(), lazyrun_command).start()
            print_msg(f"Command scheduled for: {time_str}")

        except ValueError:
            print_error("Invalid format. Use cron HH:MM command [optional args]")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_clean(self, line):
        """Audit and reclaim the ``sessions`` directory, dry-run by default.

        The command partitions ``sessions`` into three tiers before touching
        the disk:

        - ``protected``: scaffolding, long-lived secrets, operator identity and
          the canonical ``soul.md`` persona. Never removed.
        - ``sensitive``: captured credentials, evidence, findings, intel,
          operator notes and the campaign memory. Removed only with ``--all``.
        - ``reclaim``: generated reports, plans and digests, scans, transcripts,
          atomic runs, loop state, implant builds, logs, caches and the C2
          traffic archive.

        Usage:
            clean [nmap|log|test] [--dry-run] [--force] [--all]

        With no ``--force`` the command only prints the audit and deletes
        nothing. ``--force`` removes the reclaim tier; ``--force --all`` also
        removes the sensitive tier. A subset keyword restricts the plan to a
        matching family of artefacts.

        :param line: Optional subset keyword and flags.
        :type line: str
        :returns: None
        """
        tokens = line.split()
        force = False
        dry_run = False
        include_sensitive = False
        subset = None
        for token in tokens:
            if token in ("--force", "-f"):
                force = True
            elif token in ("--dry-run", "-n"):
                dry_run = True
            elif token in ("--all", "--include-sensitive"):
                include_sensitive = True
            elif token in _CLEAN_SUBSETS:
                subset = token
            else:
                print_error(f"Unknown clean argument: {token}")
                print_msg(f"Usage: clean [{'|'.join(_CLEAN_SUBSETS)}] [--dry-run] [--force] [--all]")
                return

        plan = session_reclaim.build_plan(session_reclaim.SESSIONS_DIRNAME, subset=subset)
        if not plan.entries:
            print_warn("Nothing to clean in sessions/ for the requested scope.")
            return

        if not force or dry_run:
            _print_cleanup_plan(plan, include_sensitive)
            print_msg(
                "Dry-run only; nothing was deleted. "
                "Run `clean --force` to remove the reclaim tier, "
                "or `clean --force --all` to also remove the sensitive tier."
            )
            return

        targets = plan.removable(include_sensitive)
        reclaim_estimate = session_reclaim.human_size(sum(item.size_bytes for item in targets))
        print_warn(f"Removing {len(targets)} items (~{reclaim_estimate}) from sessions/ ...")
        result = session_reclaim.remove_entries(targets)
        for entry, message in result.errors:
            print_error(f"Failed to delete {entry.path}: {message}")

        reclaimed = session_reclaim.human_size(result.reclaimed_bytes)
        print_msg(f"Removed {len(result.removed)} items, reclaimed {reclaimed}.")

        if subset is None:
            rotate_session_secrets(self.params)
            print_msg("Rotated session secrets (key.aes, rat_key, session_magic).")
        print_msg(f"Cleaned sessions directory. {RESET}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_fixperm(self, line):
        """Fix permissions for LazyOwn shell scripts.

        This function adjusts the file permissions for shell scripts and CGI scripts in the `modules` directory, making them executable.

        Usage:
            fixperm

        :param line: This parameter is not used in this function.
        :type line: str

        :returns: None

        Manual execution:
        1. Change the permissions of all shell scripts in the `modules` directory to be executable.
        2. Change the permissions of all files in the `modules/cgi-bin` directory to be executable.

        Dependencies:
        - `chmod` command must be available on the system.

        Example:
            To execute the function, simply call `fixperm`.

        Note:
            - Ensure you have the necessary permissions to modify file permissions.
        """

        print_msg("[F]ix script perm")
        self.cmd("chmod +x modules/*.sh")
        self.cmd("chmod +x modules/cgi-bin/*")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_fixel(self, line):
        """
        Fixes file permissions and line endings in the project directories.

        This function converts line endings from DOS/Windows format to Unix format for all files in the project directories. This helps to ensure consistent line endings and can prevent issues related to file format mismatches.

        Usage:
            fixel

        :param line: Command parameters (not used in this function).
        :type line: str

        :returns: None

        Manual execution:
        1. Run the method to fix line endings in the specified directories.

        Dependencies:
        - The `dos2unix` command must be installed and accessible from the command line.

        Examples:
            1. Run `do_fixel` to convert line endings for all files in the project directories.

        Note:
            - This method only fixes line endings and does not modify file permissions.
            - Ensure that the `dos2unix` command is installed and functioning correctly.
        """

        self.cmd("dos2unix *")
        self.cmd("dos2unix modules/*")
        self.cmd("dos2unix modules/cgi-bin/*")

    @cmd2.with_category("12. Miscellaneous")
    def do_pop(self, line):
        """
        Open a centered popup in the current tmux session to execute a shell command.

        If no command is provided via argument, prompts the user interactively.
        The popup remains open after command execution and waits for user acknowledgment
        via pressing ENTER, avoiding premature closure without requiring fixed sleep delays.

        Requirements:
        - Must be run inside an active tmux session (TMUX environment variable set).
        - Tmux server must be running.

        The command is executed in a bash shell within the popup. If tmux is not available
        or the environment is invalid, an error message is displayed and execution aborts.

        Args:
            line (str): The command to execute in the popup. If empty, prompts user input.
        """
        if not line:
            line = input("    [!] Enter command: ") or "whoami"

        if "TMUX" not in os.environ:
            self.display_toastr("[!] Error: Not inside a tmux session.", type="error")
            self.display_toastr("    Hint: Run this inside a tmux session (e.g. `v` or `h`).", type="info")
            return

        try:
            subprocess.run(["tmux", "list-sessions"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.display_toastr("    [!] Error: Tmux server not running or tmux not installed.", type="error")
            return

        cmd = f"""tmux popup -w 80% -h 60% -x C -y C -E 'bash -c \"{line} ; sleep 3\"'"""
        self.cmd(cmd)
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_tab(self, line):
        """
        Executes the `lazypyautogui.py` script with optional arguments.
        This open new terminal tab and then run and instance of LazyOwn strokes the keyboard with pyautogui

        If a `line` argument is provided, it appends the argument to the command.
        Otherwise, it runs the script without additional parameters. The constructed
        command is displayed and executed in the system shell.

        Parameters:
            line (str): Optional argument to pass as input to the `lazypyautogui.py` script.

        Returns:
            None
        """
        if line:
            command = f"python3 modules/lazypyautogui.py {line}"
        else:
            command = "python3 modules/lazypyautogui.py"
        print_msg(command)
        self.cmd(command)
        return
