"""Module management commands — search, use, back, and active module context.

Provides the Metasploit-like workflow:
    search <query>
    use <module>
    show options
    set <option> <value>  (via cmd2 builtin — sets shell params)
    run
    back

The active module context is stored on the parent shell
(``_active_module`` and ``_active_module_options``) so the extended
``do_show`` and ``do_run`` in ``lazyown.py`` can read it.
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.module_registry import (
    ModuleRegistry,
    format_module_detail,
    format_module_table,
)
from utils import (
    GREEN,
    RESET,
    YELLOW,
    miscellaneous_category,
    print_error,
    print_msg,
)


class ModuleManagerCommandSet(LazyOwnCommandSet):
    """Search, browse, and select framework modules."""

    phase = "module_manager"
    category = "12. Miscellaneous"

    def _get_registry(self) -> ModuleRegistry:
        shell = self._resolve_shell()
        if shell is None:
            return ModuleRegistry()
        if getattr(shell, "_module_registry", None) is None:
            shell._module_registry = ModuleRegistry()
        return shell._module_registry

    def _get_active_module(self) -> dict | None:
        shell = self._resolve_shell()
        if shell is None:
            return None
        return getattr(shell, "_active_module", None)

    def _get_active_options(self) -> dict:
        shell = self._resolve_shell()
        if shell is None:
            return {}
        opts = getattr(shell, "_active_module_options", None)
        if opts is None:
            opts = {}
            shell._active_module_options = opts
        return opts

    # ------------------------------------------------------------------
    # search
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_search(self, line):
        """Search for modules by name, description, or author.

        Usage:
            search <query>
            search type:exploit <query>
            search platform:windows

        Examples:
            search smb
            search type:exploit
            search cve-2023
        """
        reg = self._get_registry()
        query = line.strip()
        module_type = None
        text_query = query

        if query.startswith("type:"):
            parts = query.split(None, 1)
            module_type = parts[0].split(":", 1)[1]
            text_query = parts[1] if len(parts) > 1 else ""
        elif " type:" in query:
            parts = query.rsplit(" type:", 1)
            text_query = parts[0].strip()
            module_type = parts[1].strip().split()[0] if parts[1].strip() else None

        results = reg.search(query=text_query, module_type=module_type)
        if not results:
            print_msg(f"No modules found for '{query}'.")
            return

        print_msg(f"Found {len(results)} modules:")
        print(format_module_table(results, cols=("name", "type", "description")))

    # ------------------------------------------------------------------
    # use
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_use(self, line):
        """Select a module to work with.

        Usage: use <module_name>
        Shows module metadata and enters module context.
        Use 'show options' to view configurable parameters.
        Use 'run' to execute the module.
        Use 'back' to leave module context.
        """
        name = line.strip()
        if not name:
            print_error("Usage: use <module_name>")
            return

        reg = self._get_registry()
        reg.scan()
        module = reg.get(name)
        if module is None:
            print_error(f"Module '{name}' not found. Use 'search <query>' to find modules.")
            return

        shell = self._resolve_shell()
        if shell is not None:
            shell._active_module = module
            shell._active_module_options = {}
            shell._module_param_snapshot = {}
            base = getattr(shell, "custom_prompt", None) or shell.prompt
            shell._pre_module_prompt = shell.prompt
            shell.prompt = f"{base}{YELLOW}[module:{module.name}]{RESET}"

        print_msg(f"Using module: {module.name}")
        print(format_module_detail(module))
        print_msg(f"\nRun '{GREEN}run{RESET}' to execute or '{GREEN}show options{RESET}' to view params.")

        # Load default params into shell params for convenience, recording
        # the previous values so `back` can restore them untouched.
        if shell is not None:
            for p in module.params:
                pname = p.get("name", "")
                default = p.get("default", "")
                if pname and default is not None:
                    if pname not in shell._module_param_snapshot:
                        shell._module_param_snapshot[pname] = shell.params.get(pname)
                    if pname not in shell.params:
                        shell.params[pname] = str(default)

    # ------------------------------------------------------------------
    # back
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_back(self, line):
        """Leave the current module context.

        Usage: back
        """
        shell = self._resolve_shell()
        if shell is not None and getattr(shell, "_active_module", None):
            name = shell._active_module.name
            snapshot = getattr(shell, "_module_param_snapshot", {})
            for pname, old_value in snapshot.items():
                if old_value is None:
                    shell.params.pop(pname, None)
                else:
                    shell.params[pname] = old_value
            shell._active_module = None
            shell._active_module_options = {}
            shell._module_param_snapshot = {}
            pre = getattr(shell, "_pre_module_prompt", None)
            if pre is not None:
                shell.prompt = pre
                shell._pre_module_prompt = None
            print_msg(f"Left module '{name}'. Module params restored.")
        else:
            print_msg("No active module.")
