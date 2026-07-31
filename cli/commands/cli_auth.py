"""CLI authentication command set — login/logout/whoami.

Integrates with :mod:`modules.cli_auth` to authenticate CLI operators
against the same ``users.json`` as lazyc2.py.
"""

from __future__ import annotations

import cmd2
import getpass

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


class CliAuthCommandSet(LazyOwnCommandSet):
    """CLI operator authentication — login, logout, whoami."""

    phase = "misc"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_login(self, line):
        """Authenticate against users.json (same users as lazyc2.py).

        Usage:
            login                          — prompt for username and password
            login <username>               — login with specified username
            login --remember <username>     — persist login across shell restarts

        Credentials are verified against the same users.json database
        used by the C2 web dashboard. The password is never echoed.

        With ``--remember``, a secure token is stored in payload.json
        so you are automatically logged in on future shell starts.

        Examples:
            login
            login grisun0
            login --remember grisun0
        """
        import shlex

        args = shlex.split(line)
        remember = False
        username = ""

        for arg in args:
            if arg == "--remember":
                remember = True
            elif not arg.startswith("-") and not username:
                username = arg

        if not username:
            try:
                username = input(f"  {WHITE}Username:{RESET} ").strip()
            except (EOFError, KeyboardInterrupt):
                print_warn("Login cancelled.")
                return

        if not username:
            print_error("Username is required.")
            return

        try:
            password = getpass.getpass(f"  {WHITE}Password:{RESET} ")
        except (EOFError, KeyboardInterrupt):
            print_warn("Login cancelled.")
            return

        if not password:
            print_error("Password is required.")
            return

        try:
            from modules.cli_auth import login
        except ImportError as exc:
            print_error(f"Auth module not available: {exc}")
            return

        print_msg(f"Authenticating {username}...")
        result = login(username, password, remember=remember)

        if result.get("success"):
            print_succ(f"Logged in as {username} ({result.get('role')}, {result.get('elo')} ELO)")
            if result.get("remember"):
                print_succ("Remember-me token saved. Auto-login enabled for future sessions.")
                print_warn("To disable: assign cli_auto_login \"\" && assign cli_remember_token \"\"")
            else:
                print_msg("Tip: use 'login --remember' to skip login next time.")

            shell = self._resolve_shell()
            if shell is not None:
                shell.operator_name = username
                try:
                    from utils import getprompt
                    shell.custom_prompt = getprompt()
                    shell.prompt = shell.custom_prompt
                except Exception:
                    pass
        else:
            print_error(result.get("error", "Authentication failed."))

    @cmd2.with_category(miscellaneous_category)
    def do_logout(self, line):
        """Log out the current CLI operator and clear the remember-me token.

        Usage:
            logout

        Clears the CLI session and removes any stored remember-me token
        from payload.json.
        """
        try:
            from modules.cli_auth import logout
        except ImportError as exc:
            print_error(f"Auth module not available: {exc}")
            return

        result = logout()
        if result.get("success"):
            print_succ(result.get("message", "Logged out."))

            shell = self._resolve_shell()
            if shell is not None:
                shell.operator_name = None
                try:
                    from utils import getprompt
                    shell.custom_prompt = getprompt()
                    shell.prompt = shell.custom_prompt
                except Exception:
                    pass
        else:
            print_error(result.get("error", "Logout failed."))

    @cmd2.with_category(miscellaneous_category)
    def do_whoami(self, line):
        """Show the currently logged-in CLI operator.

        Usage:
            whoami

        Displays username, role, ELO score, and karma rank.
        """
        try:
            from modules.cli_auth import whoami
        except ImportError as exc:
            print_error(f"Auth module not available: {exc}")
            return

        identity = whoami()
        if not identity.get("logged_in"):
            print_warn("Not logged in. Use 'login' to authenticate.")
            print_msg("Login grants access to gamification features (ELO, karma, gym).")
            return

        print_msg("CLI Operator Identity:")
        print(f"    {WHITE}Username:{RESET} {GREEN}{identity['username']}{RESET}")
        print(f"    {WHITE}Role:    {RESET} {identity.get('role', 'operator')}")
        print(f"    {WHITE}ELO:     {RESET} {identity.get('elo', 0)}")
        karma = identity.get("karma", "")
        if karma:
            print(f"    {WHITE}Karma:   {RESET} {YELLOW}{karma}{RESET}")


__all__ = ["CliAuthCommandSet"]
