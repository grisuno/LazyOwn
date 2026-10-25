"""Operator administration of the shared parameter catalog.

Parameters are the tokens every LazyOwn surface can substitute: addon
templates (``{param}``), aliases, pipelines and the shell ``assign``
command. This set is the non-TUI half of the parameter administrator; the
``lazy_orchestrator`` console (Params tab) is the visual half. Both call
the same registry (:mod:`core.param_registry`), so a parameter declared in
either place is immediately reusable everywhere.

The registry stores the declarations as data in ``params/operator.yaml``,
so creating a parameter needs no source edit: the payload schema and the
addon creator pick the new key up automatically.
"""

from __future__ import annotations

import shlex

import cmd2

from cli.assign import apply_assign as _apply_assign
from cli.commands._base import LazyOwnCommandSet
from core.config import save_payload as _save_payload
from utils import print_error, print_msg, print_warn

__all__ = ["ParamCommandSet"]

_KIND_HELP = "string|integer|boolean|url|path|ip|port|hostname"


class ParamCommandSet(LazyOwnCommandSet):
    """Create, inspect and delete the shared parameters."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_param(self, line):
        """Manage the shared parameter catalog used by addons and aliases.

        A parameter declared here is reusable by every addon: name it
        generically, never after a single tool.

        Usage:
          param list [keyword]              show the catalog (builtin + operator)
          param show <name>                 show one parameter in detail
          param create <name> [options]     declare a new parameter
          param set <name> <value>          set the live value of a parameter
          param delete <name>               remove an operator parameter
          param reload                      re-read params/operator.yaml

        create options:
          --kind <kind>       payload kind (default string)
          --default <value>   default value (default empty)
          --desc <text>       help text
          --category <name>   payload schema category (default general)
        """
        from core.param_registry import (
            apply_to_schema,
            create_param,
            delete_param,
            list_params,
            load_entries,
            sync_shell_params,
        )

        args = shlex.split(line) if line.strip() else []
        action = args[0] if args else "list"

        if action in ("list", ""):
            keyword = args[1] if len(args) > 1 else ""
            params = list_params(include_builtin=True, keyword=keyword)
            operator = sum(1 for p in params if p.source == "operator")
            print_msg(f"Catalog: {len(params)} parameters ({operator} operator, {len(params) - operator} builtin)")
            for param in params:
                marker = "*" if param.source == "operator" else " "
                default = str(param.default)
                default = default[:40] + "..." if len(default) > 43 else default
                print_msg(f" {marker} {param.name:<28} {param.kind:<10} {default:<45} {param.description[:60]}")
            if not params:
                print_msg("[*] no parameters matched")
            return

        if action == "show":
            if len(args) < 2:
                print_error("Usage: param show <name>")
                return
            name = args[1]
            entry = load_entries().get(name)
            if entry is not None:
                print_msg(f"[+] {name} (operator) kind={entry.kind} default={entry.default!r}")
                print_msg(f"    {entry.description}")
                return
            from core.payload_schema import SCHEMA

            spec = SCHEMA.get(name)
            if spec is None:
                print_error(f"[-] unknown parameter: {name}")
                return
            print_msg(f"[+] {name} (builtin) kind={spec.kind.value} default={spec.default!r}")
            print_msg(f"    {spec.description}")
            return

        if action == "create":
            if len(args) < 2:
                print_error("Usage: param create <name> [--kind K] [--default V] [--desc D]")
                return
            name = args[1]
            kind = "string"
            default: object = ""
            description = ""
            category = "general"
            index = 2
            while index < len(args):
                token = args[index]
                if token in ("--kind", "--default", "--desc", "--description", "--category"):
                    if index + 1 >= len(args):
                        print_error(f"[-] {token} needs a value")
                        return
                    value = args[index + 1]
                    if token == "--kind":
                        kind = value
                    elif token == "--default":
                        default = value
                    elif token == "--category":
                        category = value
                    else:
                        description = value
                    index += 2
                    continue
                print_error(f"[-] unknown option: {token}")
                return
            try:
                param = create_param(
                    name,
                    kind=kind,
                    default=default,
                    description=description,
                    category=category,
                )
            except ValueError as exc:
                print_error(f"[-] {exc}")
                return
            sync_shell_params(self._resolve_shell())
            print_msg(f"[+] parameter '{param.name}' created (kind={param.kind}, default={param.default!r})")
            print_msg(f"    usable now as {{{param.name}}} in any addon, alias or pipeline")
            return

        if action == "set":
            if len(args) < 3:
                print_error("Usage: param set <name> <value>")
                return
            name = args[1]
            value = " ".join(args[2:])
            if name not in self.params:
                print_error(f"[-] unknown parameter: {name}")
                return
            issues: list = []
            ok = _apply_assign(
                self.params,
                name,
                value,
                save=_save_payload,
                on_issue=issues.append,
            )
            for issue in issues:
                print_warn(f"[!] {issue.message}")
            if ok:
                print_msg(f"[+] {name} = {self.params.get(name)!r}")
            else:
                print_error(f"[-] could not set {name}")
            return

        if action == "delete":
            if len(args) < 2:
                print_error("Usage: param delete <name>")
                return
            try:
                delete_param(args[1])
            except KeyError as exc:
                print_error(f"[-] {exc} (builtin parameters cannot be deleted)")
                return
            self.params.pop(args[1], None)
            try:
                _save_payload(self.params)
            except Exception as exc:
                print_warn(f"[!] could not persist the payload: {exc}")
            print_msg(f"[+] parameter '{args[1]}' deleted")
            return

        if action == "reload":
            apply_to_schema()
            count = sync_shell_params(self._resolve_shell())
            print_msg(f"[+] reloaded {count} operator parameter(s) into the shell")
            return

        print_warn("Usage: param [list|show|create|set|delete|reload] ...")
