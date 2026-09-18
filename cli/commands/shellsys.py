"""Local shell and system extracted from the miscellaneous cluster.

Pending status: originals deleted from ``cli/commands/misc_migrated.py``;
this set is registered by ``cli.registry``.
"""

from __future__ import annotations

import base64

import cmd2

from cli.commands._base import LazyOwnCommandSet
from core.safe_exec import safe_run_shell as _safe_run_shell

__all__ = ["ShellSysCommandSet"]


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
        print_msg(
            f'Try echo -e "[\\e[96m`pwd`\\e[0m]\\e[34m" && ls && echo -en "\\e[0m"{RESET}'
        )
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
            line = input ("    [!] enter the filename: ") or 'unamed_lazyownfile'
        users_file_path = os.path.join("sessions", line)
        print_msg(users_file_path)
        if not os.path.exists(users_file_path):
            print_warn(f"{users_file_path} does not exist. Creating the file.")
            os.makedirs(os.path.dirname(users_file_path), exist_ok=True)
            with open(users_file_path, 'w'):
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
            schedule_time = datetime.strptime(time_str, '%H:%M').time()
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
        """
        Deletes files and directories in the `sessions` directory, excluding specified files and directories.

        1. Checks if the `self.params['rhost']` parameter is valid:
        - Uses the `check_rhost` function to verify if `self.params['rhost']` is assign and valid.
        - If `self.params['rhost']` is not valid, exits the function.

        2. Lists files and directories in the `sessions` directory:
        - Uses `os.listdir` to list all files and directories in the `sessions` directory.
        - Compares each item with the list of exclusions.

        3. Deletes files and directories not in the exclusion list:
        - Uses `os.remove` to delete files and `shutil.rmtree` to delete directories.

        4. Prints a message indicating that the cleanup is complete.

        :param line: This parameter is not used in the function.
        :type line: str
        :returns: None

        Manual execution:
        To manually run these tasks, you would need to:
        - Ensure that you have the correct `self.params['rhost']` value set.
        - Manually execute commands to delete files and directories, excluding specified ones.

        Note: This function performs a cleanup by removing various files and directories associated with the current session, excluding specified items.
        """
        rhost = self.params['rhost']
        if not check_rhost(self.params['rhost']):
            return
        if line.startswith("test"):
            self.cmd("sudo rm sessions/test* -rf")
            return
        if line.startswith("log"):
            self.cmd("sudo rm sessions/logs/* -rf")
            return
        if line.startswith("nmap"):
            self.cmd("sudo rm sessions/scan* -rf")
            return
        exclusions = [
            'c',
            'download_resources.sh',
            'implant',
            'ip2asn-v4.tsv.gz',
            'key.aes',
            'LazyOwn_session_report.csv',
            'lin',
            'logs',
            'nmap-bootstrap.xsl',
            'php',
            'phishing',
            'payloads.txt',
            'routes_to_templates.json',
            'sslscan-singleip.sh',
            'tasks.json',
            'temp_uploads',
            'tor.sh',
            'users.txt',
            'uploads',
            'win',
            'www.py'
        ]

        # Path to the sessions directory
        sessions_dir = 'sessions'

        # List all files and directories in the sessions directory
        all_items = os.listdir(sessions_dir)

        for item in all_items:
            item_path = os.path.join(sessions_dir, item)
            if not any(item == exclusion for exclusion in exclusions):
                try:
                    if os.path.isfile(item_path):
                        print_msg(f"Deleting file ... {item_path}")
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        print_msg(f"Deleting dir ... {item_path}")
                        self.cmd(f"rm -rf {item_path}")
                except Exception as e:
                    print_error(f"Failed to delete {item_path}: {e}")

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
            line = input("    [!] Enter command: ") or 'whoami'

        if 'TMUX' not in os.environ:
            self.display_toastr("[!] Error: Not inside a tmux session.", type="error")
            self.display_toastr("    Hint: Run this inside a tmux session (e.g. `v` or `h`).", type="info")
            return

        try:
            subprocess.run(['tmux', 'list-sessions'], check=True, capture_output=True)
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


import utils as _lazy_utils

for _lazy_name in dir(_lazy_utils):
    if not _lazy_name.startswith('_'):
        globals().setdefault(_lazy_name, getattr(_lazy_utils, _lazy_name))
del _lazy_utils, _lazy_name


def __getattr__(name: str):
    """Fall back to ``utils`` for bare-name references used by migrated commands."""
    import utils as _utils
    try:
        return getattr(_utils, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
