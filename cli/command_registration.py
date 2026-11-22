"""Dynamic command registration mixin for ``LazyOwnShell``.

This module lifts the command-registration cluster out of
``lazyown.py`` into a single-responsibility mixin. It owns every surface
that turns an on-disk artefact into a live ``do_<name>`` shell command:

- ``tools/*.tool`` pwntomate definitions (:meth:`register_tool_commands`);
- Lua plugins (:meth:`load_plugins`, :meth:`_register_lua_command`);
- ``lazyaddons/*.yaml`` addons (:meth:`load_yaml_plugins`,
  :meth:`register_yaml_plugin`);
- ``lazyadversaries/*.yaml`` adversary emulations
  (:meth:`register_all_adversary_commands`,
  :meth:`_register_adversary_command`).

The mixin depends only on shell attributes it reads through ``self``
(``params``, ``plugins_dir``, ``lazyaddons_dir``, ``lua``, ``cmd``,
``onecmd``, ``display_toastr``, ``do_adversary_yaml``). It never writes to
``payload.json`` and reads live configuration from ``self.params`` so a
single-responsibility class can be unit-tested without the full shell.
"""

from __future__ import annotations

import glob
import json
import os
import re

import cmd2
import yaml

from utils import (
    REQUIRED_KEYS,
    NmapParser,
    is_binary_present,
    print_error,
    print_msg,
    print_warn,
    pwntomate_category,
    replace_command_placeholders,
)

SHELL_BUILTIN_TOKENS = frozenset(
    {
        "export",
        "cd",
        "source",
        ".",
        "set",
        "unset",
        "alias",
        "unalias",
        "eval",
        "exec",
        "read",
        "trap",
        "ulimit",
        "umask",
        "wait",
        "test",
        "[",
        "true",
        "false",
        ":",
        "shopt",
        "local",
        "return",
        "printf",
        "echo",
        "sleep",
    }
)
"""Leading tokens of addon commands that are shell builtins, not binaries.

The addon binary preflight must never warn about ``export`` or ``cd``:
vulnbot-style addons start with ``cd ... && export KEY=... && python3 ...``
and the first token is a builtin, which is always available.
"""

TLS_PORTS = frozenset({"443", "8443"})
YAML_PLUGIN_CATEGORY = "14. Yaml Addon."
ADVERSARY_CATEGORY = "14. Adversary Emulation"
LUA_PLUGIN_CATEGORY = "13. Lua Plugin"


class CommandRegistrationMixin:
    """Register on-disk artefacts as live shell commands.

    Mixed into :class:`LazyOwnShell`; every method is an instance method
    that reads shell state through ``self`` and sets ``do_<name>``
    attributes on the shell instance.
    """

    def register_tool_commands(self) -> None:
        """Register every active ``tools/*.tool`` as a ``do_<toolname>`` command.

        Placeholders in the tool's ``command`` template are resolved at call
        time against ``self.params`` (so live config changes are honored).
        Optional positional args passed to the command override ``port`` and
        are appended as extra flags. When ``sessions/scan_<rhost>.nmap.xml``
        exists and the tool's triggers match a discovered service, the host
        and port are pre-populated from the scan; otherwise the command falls
        back to ``rhost``/``rport`` from ``payload.json``.

        Returns:
            None
        """
        tool_dir = "tools"

        if not os.path.exists(tool_dir):
            print_error(f"[!] Folder '{tool_dir}' not found.")
            return

        params_snapshot = getattr(self, "params", {}) or {}
        current_rhost = params_snapshot.get("rhost") or ""
        preview_domain = params_snapshot.get("domain") or ""
        preview_dnswordlist = params_snapshot.get("dnswordlist") or ""
        preview_start_user = params_snapshot.get("start_user") or ""
        preview_start_pass = params_snapshot.get("start_pass") or ""

        for tool_file in glob.glob(os.path.join(tool_dir, "*.tool")):
            try:
                with open(tool_file, "r") as f:
                    tool_data = json.load(f)

                tool_name = tool_data.get("toolname")
                command_template = tool_data.get("command")
                triggers = tool_data.get("trigger", []) or []
                active = tool_data.get("active", False)
                tool_category = tool_data.get("category", pwntomate_category)
                tool_description = tool_data.get("description", "")

                if not active or not tool_name or not command_template:
                    continue

                safe_tool_name = re.sub(r"[^A-Za-z0-9_]", "_", str(tool_name))

                matched_target = None
                xmmll = f"sessions/scan_{current_rhost}.nmap.xml" if current_rhost else ""
                if xmmll and os.path.exists(xmmll):
                    try:
                        report = NmapParser.parse_fromfile(xmmll)
                        for host in report.hosts:
                            for service in host.services:
                                if service.service in triggers or "all" in triggers:
                                    matched_target = {
                                        "ip": host.address,
                                        "port": str(service.port),
                                        "service": service.service,
                                        "proto": service.protocol,
                                        "tunnel": "s" if service.tunnel == "ssl" else "",
                                    }
                                    break
                            if matched_target:
                                break
                    except Exception as exc:
                        print_warn(f"could not parse {xmmll}: {exc}")

                def make_wrapper(cmd_template, tname, default_target, fallback_rhost):
                    def tool_wrapper(arg):
                        extra = str(arg).strip() if arg is not None else ""
                        port_override = ""
                        extra_flags = ""
                        if extra:
                            parts = extra.split(None, 1)
                            if parts and parts[0].isdigit():
                                port_override = parts[0]
                                extra_flags = parts[1] if len(parts) > 1 else ""
                            else:
                                extra_flags = extra

                        params = self.params
                        target_ip = params.get("rhost") or fallback_rhost or ""
                        target_port = (
                            port_override or (default_target or {}).get("port") or str(params.get("rport") or "")
                        )
                        target_service = (default_target or {}).get("service") or ""
                        target_proto = (default_target or {}).get("proto") or "tcp"
                        target_tunnel = (default_target or {}).get("tunnel")
                        if target_tunnel is None:
                            target_tunnel = "s" if target_port in TLS_PORTS else ""

                        outputdir = os.path.join("sessions", target_ip or "unknown", tname)
                        try:
                            os.makedirs(outputdir, exist_ok=True)
                        except OSError as exc:
                            print_warn(f"could not create {outputdir}: {exc}")

                        cmd_params = {
                            "ip": target_ip,
                            "port": target_port,
                            "domain": params.get("domain", "") or "",
                            "dnswordlist": params.get("dnswordlist", "") or "",
                            "dirworlist": params.get("dirwordlist", "") or "",
                            "usrwordlist": params.get("usrwordlist", "") or "",
                            "nameserver": params.get("nameserver", "") or target_ip,
                            "service": target_service,
                            "proto": target_proto,
                            "username": params.get("start_user", "") or "",
                            "password": params.get("start_pass", "") or "",
                            "outputdir": outputdir,
                            "toolname": tname,
                            "s": target_tunnel,
                            "tunnel": target_tunnel,
                            "ext": params.get("ext", "") or "",
                        }

                        final_command = replace_command_placeholders(cmd_template, cmd_params)
                        if extra_flags:
                            final_command = f"{final_command} {extra_flags}"
                        self.cmd(final_command)

                    return tool_wrapper

                wrapper = make_wrapper(command_template, tool_name, matched_target, current_rhost)

                trigger_label = ", ".join(triggers) if triggers else "(any)"
                preview_params = {
                    "ip": current_rhost or "<rhost>",
                    "port": (matched_target or {}).get("port", "<port>"),
                    "domain": preview_domain or "<domain>",
                    "dnswordlist": preview_dnswordlist or "<dnswordlist>",
                    "dirworlist": "<dirwordlist>",
                    "usrwordlist": "<usrwordlist>",
                    "nameserver": current_rhost or "<nameserver>",
                    "service": (matched_target or {}).get("service", ""),
                    "proto": (matched_target or {}).get("proto", "tcp"),
                    "username": preview_start_user or "<username>",
                    "password": preview_start_pass or "<password>",
                    "outputdir": os.path.join("sessions", current_rhost or "<rhost>", safe_tool_name),
                    "toolname": tool_name,
                    "s": (matched_target or {}).get("tunnel", ""),
                    "tunnel": (matched_target or {}).get("tunnel", ""),
                    "ext": "",
                }
                preview_cmd = replace_command_placeholders(command_template, preview_params)

                docstring = f"{tool_description}\n\n" if tool_description else ""
                docstring += f"Tool:      {tool_name}\n"
                docstring += f"Category:  {tool_category}\n"
                docstring += f"Trigger:   {trigger_label}\n"
                docstring += f"Usage:     {safe_tool_name} [port] [extra-flags]\n"
                docstring += f"Example:   {preview_cmd[:160]}\n"
                if matched_target:
                    docstring += (
                        f"Matched:   {matched_target['service']} "
                        f"({matched_target['proto']}/{matched_target['port']}) on {current_rhost}\n"
                    )
                wrapper.__doc__ = docstring
                cmd2.utils.categorize(wrapper, tool_category)
                setattr(self, f"do_{safe_tool_name}", wrapper)
                print_msg(f"Command '{safe_tool_name}' registered [{tool_category}] from tools")

            except Exception as e:
                print_error(f"[ERROR] Failed to load tool {tool_file}: {e}")

    def _register_lua_command(self, command_name, lua_function) -> None:
        """Register a new command exposed by a Lua plugin.

        Args:
            command_name: Shell command name to register.
            lua_function: Callable Lua function invoked with the raw argline.
        """

        @cmd2.with_category(LUA_PLUGIN_CATEGORY)
        def wrapper(arg):
            try:
                result = lua_function(arg)
                if result is not None:
                    print(result)
            except Exception as e:
                self.display_toastr(f"Error en el comando Lua {command_name}: {e}", type="error")

        yaml_file = os.path.join(self.plugins_dir, f"{command_name}.yaml")
        description = ""

        if os.path.exists(yaml_file):
            try:
                with open(yaml_file, "r") as file:
                    yaml_data = yaml.safe_load(file)
                    description = yaml_data.get("description", "")
            except Exception as e:
                self.display_toastr(f"Error reading YAML  {command_name}: {e}", type="error")

        wrapper.__doc__ = description if description else f"Execute the Lua command '{command_name}'."
        setattr(self, f"do_{command_name}", wrapper)
        print_msg(f"Command '{command_name}' register from Lua.")

    def load_plugins(self) -> None:
        """Load every Lua plugin from the 'plugins/' directory."""
        plugins_dir = self.plugins_dir
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir)
            print_msg("Plugin directory created.")
            return

        for filename in os.listdir(plugins_dir):
            if filename.endswith(".lua"):
                filepath = os.path.join(plugins_dir, filename)
                yaml_ = filename.replace(".lua", ".yaml")
                filepathyaml = os.path.join(plugins_dir, yaml_)
                if filepathyaml == "plugins/init_plugins.yaml":
                    pass
                else:
                    try:
                        with open(filepathyaml, "r") as file:
                            file_yaml = yaml.safe_load(file)
                            enabled = file_yaml.get("enabled")
                            if enabled:
                                try:
                                    with open(filepath, "r") as file:
                                        script = file.read()
                                        self.lua.execute(script)
                                except Exception as e:
                                    print_error(f"Error al cargar el plugin '{filename}': {e}")
                    except Exception as e:
                        print_error(f"Error al cargar el yaml '{filepathyaml}': {e}")

    def load_yaml_plugins(self) -> None:
        """Load all YAML plugins from the 'lazyaddons/' directory.

        Scans the ``lazyaddons/`` directory, reads each YAML file, and
        registers enabled plugins as new commands.
        """
        if not os.path.exists(self.lazyaddons_dir):
            os.makedirs(self.lazyaddons_dir)
            print_warn("Lazyaddons directory created.")
            return

        for filename in os.listdir(self.lazyaddons_dir):
            if filename.endswith(".yaml"):
                filepath = os.path.join(self.lazyaddons_dir, filename)
                try:
                    with open(filepath, "r") as file:
                        plugin_data = yaml.safe_load(file)
                        if plugin_data.get("enabled", False):
                            self.register_yaml_plugin(plugin_data)
                except Exception as e:
                    print_error(f"Error loading YAML plugin '{filename}': {e}")

    def register_yaml_plugin(self, plugin_data) -> None:
        """Register a YAML addon as a shell command.

        Reads the optional ``category`` field from the addon YAML (falls back
        to ``"14. Yaml Addon."`` when absent) and sets the cmd2 category
        attribute on the wrapper so the command appears in the correct palette
        section without any hardcoded string in this method.

        Also reads the optional ``tags`` list for future palette filtering,
        the optional ``os`` field (MITRE platform: ``linux``, ``windows``,
        ``macos``, ``network``, ``containers``, ``saas``, ``iaas`` or
        ``any``) and the optional ``trigger`` list of nmap service names
        consumed by the exploration engine. Both ``os`` and ``trigger``
        default to ``any`` / ``[]`` so legacy addons keep loading.

        A lightweight dependency check runs before first execution.

        Args:
            plugin_data: Parsed addon YAML mapping.
        """
        from cli.exploration import (
            ALLOWED_OS_VALUES,
            ANY_OS,
            normalise_os,
            normalise_trigger,
        )

        tool = plugin_data.get("tool", {})
        name = plugin_data["name"]
        params = plugin_data.get("params", [])
        description = plugin_data.get("description", "")
        tags = plugin_data.get("tags", [])
        execute_command = tool.get("execute_command", "")
        addon_category = plugin_data.get("category", YAML_PLUGIN_CATEGORY)
        addon_os = normalise_os(plugin_data.get("os"), default=ANY_OS)
        addon_trigger = normalise_trigger(plugin_data.get("trigger"))
        raw_os = plugin_data.get("os")
        if isinstance(raw_os, str) and raw_os.strip().lower() not in ALLOWED_OS_VALUES:
            print_warn(
                f"Addon '{name}' declares unknown os='{raw_os}' "
                f"(allowed: {sorted(ALLOWED_OS_VALUES)}); falling back to '{ANY_OS}'."
            )

        def wrapper_yaml(arg):
            try:
                args = arg.split()
                param_values = {}

                for param in params:
                    param_name = param["name"]
                    if param.get("required", False) and param_name not in self.params:
                        self.display_toastr(
                            f"Error: Parameter '{param_name}' is required but not found in self.params.", type="warning"
                        )
                        return
                    if param_name in self.params:
                        param_values[param_name] = self.params[param_name]
                    elif "default" in param:
                        param_values[param_name] = param["default"]
                    else:
                        self.display_toastr(
                            f"Error: Parameter '{param_name}' is missing and no default value is provided.",
                            type="warning",
                        )
                        return
                try:
                    install_path = None
                    if "install_path" in tool:
                        install_path = os.path.join(os.getcwd(), tool["install_path"])
                        if not os.path.exists(install_path):
                            self.display_toastr(f"{tool['name']} is not installed. Installing...", type="warning")
                            self.cmd(f"git clone {tool['repo_url']} {install_path}")
                            if "install_command" in tool:
                                cmdinstall = replace_command_placeholders(tool["install_command"], self.params)
                                self.cmd(f"cd {install_path} && {cmdinstall}")
                                self.cmd("sleep 2")

                    if "execute_command" in tool:
                        binary = execute_command.split()[0] if execute_command else ""
                        if (
                            binary
                            and binary not in SHELL_BUILTIN_TOKENS
                            and not os.path.isabs(binary)
                            and not is_binary_present(binary)
                        ):
                            if tool.get("install_command") and tool.get("repo_url") and tool.get("install_path"):
                                install_hint = tool["install_command"]
                            elif tool.get("repo_url"):
                                install_hint = f"git clone {tool['repo_url']}"
                            else:
                                install_hint = f"see `help {name}` for the install line"
                            print_warn(f"'{binary}' not found in PATH.")
                            print_warn(f"Install: {install_hint[:120]}")
                        command_replaced = replace_command_placeholders(execute_command, self.params).strip()
                        if install_path:
                            if args:
                                final_command = f"cd {install_path} && {command_replaced} {' '.join(args)}"
                            else:
                                final_command = f"cd {install_path} && {command_replaced}"
                        else:
                            if args:
                                final_command = f"{command_replaced} {' '.join(args)}"
                            else:
                                final_command = command_replaced
                        self.cmd(final_command)

                    if "upload_file" in tool:
                        for file_path in [f.strip() for f in tool["upload_file"].split(",")]:
                            if file_path:
                                self.display_toastr(f"Remote Upload executing: upload_c2 {file_path}", type="info")
                                self.onecmd(f"upload_c2 {file_path}")
                                self.cmd("sleep 10")

                    if "remote_command" in tool:
                        remotecmd = replace_command_placeholders(tool["remote_command"], self.params)
                        self.display_toastr(f"Remote command executing: {remotecmd}", type="info")
                        self.onecmd(f"issue_command_to_c2 {remotecmd}")

                    if "download_file" in tool:
                        for file_path in [f.strip() for f in tool["download_file"].split(",")]:
                            if file_path:
                                self.display_toastr(f"Remote Download executing: download_c2 {file_path}", type="info")
                                self.onecmd(f"download_c2 {file_path}")

                    if "lazycommand" in tool:
                        lazycommand = replace_command_placeholders(tool["lazycommand"], self.params)
                        self.display_toastr(f"Lazy Command executing: {lazycommand}", type="info")
                        for lazy_cmd in [c.strip() for c in lazycommand.split(",")]:
                            if lazy_cmd:
                                self.onecmd(lazy_cmd)

                except KeyError as e:
                    self.display_toastr(f"Error: Missing parameter '{e}' in the plugin configuration.", type="error")
                    return

            except Exception as e:
                self.display_toastr(f"Error in plugin '{name}': {e}", type="error")
                return

        trigger_label = ", ".join(addon_trigger) if addon_trigger else "(none)"
        wrapper_yaml.__doc__ = (
            f"{description}\n\nCategory: {addon_category}"
            f"\nOS: {addon_os}"
            f"\nTrigger: {trigger_label}" + (f"\nTags: {', '.join(tags)}" if tags else "")
        )
        cmd2.utils.categorize(wrapper_yaml, addon_category)
        if hasattr(self, f"do_{name}"):
            print_msg(
                f"Command '{name}' already exists as built-in — YAML registered as trigger-only [{addon_category}]."
            )
        else:
            setattr(self, f"do_{name}", wrapper_yaml)
            print_msg(f"Command '{name}' registered [{addon_category}] from YAML.")

    def register_all_adversary_commands(self) -> None:
        """Register every ``lazyadversaries/*.yaml`` entry as a command."""
        for file in glob.glob("lazyadversaries/*.yaml"):
            with open(file, "r") as f:
                try:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict):
                        self._register_adversary_command(data)
                    elif isinstance(data, list):
                        for adversary in data:
                            self._register_adversary_command(adversary)
                except Exception as e:
                    print_error(f"Error parsing {file}: {e}")

    def _register_adversary_command(self, adv) -> None:
        """Register one adversary emulation entry as a ``do_<name>`` command.

        Args:
            adv: Parsed adversary mapping with the required threat fields.
        """
        if not all(k in adv for k in REQUIRED_KEYS):
            print_warn(f"Skipping invalid adversary entry (missing required fields): {adv.get('name', '<unnamed>')}")
            return

        name = adv["name"].replace(".", "_")
        description = adv["description"]

        @cmd2.with_category(ADVERSARY_CATEGORY)
        def cmd_wrapper(_):
            return self.do_adversary_yaml(str(adv["id"]) + " l")

        cmd_wrapper.__doc__ = description
        setattr(self, f"do_{name}", cmd_wrapper)
        print_msg(f"Command '{name}' registered for adversary ID {adv['id']}")
