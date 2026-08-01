# COMMANDS.md Documentation  by readmeneitor.py

## _parse_bool_setting
Coerce a cmd2 ``set`` argument into a Python ``bool``.

Accepts native booleans, integers, and the canonical truthy/falsy
strings used elsewhere in the framework (``true``/``false``,
``yes``/``no``, ``on``/``off``, ``1``/``0``). Anything else raises
:class:`ValueError` so cmd2 surfaces the error to the operator
instead of silently coercing to ``False``.

## main
No description available.

## __init__
Bind the proxy to a live ``params`` dictionary.

## __getattr__
No description available.

## __setattr__
No description available.

## __init__
Initializer for the LazyOwnShell class.

This method sets up the initial parameters and scripts for an instance of
the LazyOwnShell class. It initializes a dictionary of parameters with default
values and a list of script names that are part of the LazyOwnShell toolkit.

Attributes:
    params (dict): A dictionary of parameters with their default values.
    scripts (list): A list of script names included in the toolkit.
    output (str): An empty string to store output or results.

## _register_ux_settables
Expose the new UX flags through cmd2's ``set`` command.

cmd2's ``set`` reads/writes from a target object. The
:class:`_PayloadSettableProxy` proxies attribute access to
``self.params`` so ``set <key> <value>`` and ``assign <key> <value>``
update the same backing store and both persist through
:func:`core.config.save_payload`. The four keys registered here
(``tui_theme``, ``enable_operator_presence``, ``enable_toasts``,
``toast_max_per_tick``) match the schema entries in
:mod:`core.payload_schema`.

## _load_extended_params
Load extra parameters from ``params/*.yaml`` into ``self.params``.

Every YAML file in the ``params/`` directory is loaded as a flat
key-value dict and merged into ``self.params`` at startup. This
allows operators to add new configuration keys for lazyaddons,
aliases, and pipelines without modifying ``payload.json`` or
Python source.

Files are loaded in alphabetical order; later files override
earlier ones. ``payload.json`` keys are *not* overwritten.

## log_command
Logs the command execution details to a CSV file.

:param cmd_name: The name of the command.
:param cmd_args: The arguments of the command.
:param start_time: Optional ``"%Y-%m-%d %H:%M:%S"`` string captured
    before execution. Defaults to the current time when omitted.
:param end_time: Optional ``"%Y-%m-%d %H:%M:%S"`` string captured
    after execution. Defaults to ``start_time`` when omitted.
:param duration_ms: Measured wall-clock duration in milliseconds.

## default
Handles undefined commands, including aliases.

This method checks if a given command (or its alias) exists within the class
by attempting to find a corresponding method. If the command or alias is not
found, it prints an error message.

:param line: The command or alias to be handled.
:type line: str
:return: None

## scripts
Auto-discovered list of runnable script names.

Dynamically scans the shell for ``run_<name>`` methods, excluding
internal plumbing helpers (``run_script``, ``run_command``). The
result is cached until the next shell restart.

Returns:
    List of script name strings available via ``run <name>``.

## set
Set a parameter — the unified ``set``/``assign`` surface.

Registered UX settables (``ui_hints``, ``tui_theme``,
``enable_toasts``...) keep native cmd2 semantics. Any other key
delegates to ``assign`` so documentation and muscle memory that
predate the split (``set rhost 10.10.10.10``) work again. With a
single unknown key and no value, prints the current value.

## _ui_hints_level
Return the ambient coaching level: ``on``, ``minimal`` or ``off``.

``off`` suppresses every post-command coaching surface (toasts,
inline hints, protips, autosuggest and engagement flavour);
``minimal`` keeps only the autosuggest accelerator. Any unset or
unknown value means full ``on``.

## _toast_hook
Post-command hook that prints unseen JSONL events as toast lines.

Reads the ``enable_toasts`` flag from ``self.params`` (default
True) so operators can disable transient notifications with
``set enable_toasts false`` without restarting. Any failure is
swallowed — toasts must never block the shell.

Args:
    data: cmd2 PostcommandData containing the executed statement.

Returns:
    ``data`` unchanged.

## _unified_tips_hook
Unified post-command hook: hints + protips + curiosity + autosuggest + ELO + VRI.

Replaces the five fragmented hooks (inline hints, engagement,
autosuggest, toasts, recording) with a single coordination point
via :class:`cli.tips_engine.TipsEngine`.

Args:
    data: cmd2 PostcommandData containing the executed statement.

Returns:
    data unchanged.

## _run_auto_decrypt
Decrypt session data automatically on authenticated startup.

## _run_auto_encrypt
Encrypt session data automatically on application close.

## _read_recent_commands_for_autosuggest
Return the last ``limit`` first-tokens from the session transcript.

Args:
    limit: Maximum number of distinct command names to return.

Returns:
    A list of command first-tokens. Empty when the file is absent.

## _refresh_autosuggest
Recompute the active suggestion from the engine's provider chain.

Args:
    executed_command: Raw string of the command that just ran.

## _recording_hook
Post-command hook: record commands when ``makerc`` is active.

## _did_you_mean
Return up to ``limit`` close-matching command names.

Combines the local ``do_*`` index with the graphify knowledge graph
(when available) so an unknown command is recovered by both lexical
similarity and graph proximity. Empty result means no suggestion is
confident enough to surface.

## logcsv
Forward a command line to :meth:`log_command` for CSV persistence.

Args:
    line: Full command line in ``"<verb> <args>"`` form.
    start_time: Optional pre-execution timestamp string forwarded
        verbatim to :meth:`log_command`.
    end_time: Optional post-execution timestamp string forwarded
        verbatim to :meth:`log_command`.
    duration_ms: Measured wall-clock duration in milliseconds.

## cmd
Internal function to execute commands.

Executes the given shell command, captures stdout via ``tee`` so the
operator both sees the output and a copy lands in ``sessions/logs/``,
and forwards a telemetry record to
:class:`modules.metrics.MetricsRecorder` so the duration and exit
code can be analysed later.

:param command: The command to be executed.
:type command: str
:return: ``None``.
:rtype: NoneType

## onecmd_plus_hooks
Dispatch a command, expanding payload placeholders in custom aliases.

This is the single chokepoint through which every interactive command
flows, so it also enforces the authorization scope guard before the
command runs. Accepts both raw strings and parsed cmd2 ``Statement``
objects.

Args:
    statement: The command to run, as a string or ``Statement``.
    add_to_history: Whether cmd2 should record the command in history.
    raise_keyboard_interrupt: Whether to propagate Ctrl-C.
    orig_rl_history_length: Readline bookkeeping passed through to cmd2.

Returns:
    The ``stop`` flag from cmd2 (``True`` ends the loop). A scope block
    returns ``False`` so the offending command is skipped without
    terminating the session.

## _build_scope_offensive
Compute the set of offensive command names from cmd2 categories.

Reads each command's help category via cmd2 introspection and delegates
the offensive/benign decision to
:func:`cli.scope_guard.build_offensive_commands`, so the classification
policy lives in one tested place.

Returns:
    The frozenset of offensive command names.

## _resolve_offensive
Return whether a command (or custom alias) is offensive.

Args:
    name: The command name or custom alias typed by the operator.

Returns:
    ``True`` when the command, or the command a custom alias expands to,
    belongs to an offensive kill-chain category.

## _scope_check
Authorize a command against the configured engagement scope.

Builds a fresh :class:`cli.scope_guard.ScopeGuard` from the live payload
values so mid-session changes to ``scope`` / ``scope_enforcement`` take
effect immediately, then renders the decision. The guard fails open: any
unexpected error allows the command so a defect here never blocks the
operator.

Args:
    cmd_name: The command name about to run.

Returns:
    ``True`` when the command may proceed, ``False`` when it must be
    skipped (enforce mode, out of scope, confirmation declined).

## _scope_confirm
Ask the operator to confirm an out-of-scope offensive command.

Non-interactive sessions (piped input, ``-c`` execution, scripted runs)
cannot answer a prompt, so they are treated as a refusal: the safer
default for an enforce-mode block.

Args:
    decision: The blocking :class:`cli.scope_guard.ScopeDecision`.

Returns:
    ``True`` only when an interactive operator explicitly confirms.

## one_cmd
Internal function to execute commands.

This method attempts to execute a given command using `onecmd` and captures
the output. It sets the `output` attribute based on whether the command was
executed successfully or an exception occurred.

:param command: The command to be executed.
:type command: str
:return: A message indicating the result of the command execution.
:rtype: str

## emptyline
Handle the case where the user enters an empty line.

This method is called when the user submits an empty line of input in
the command-line interface. By default, it provides feedback indicating
that no command was entered.

It is useful for providing user-friendly messages or handling empty input
cases in a custom manner.

License: This function is part of a program released under the GNU General
Public License v3.0 (GPLv3). You can redistribute it and/or modify it
under the terms of the GPLv3, as published by the Free Software Foundation.

Note: This method is called by the cmd library when an empty line is
entered. You can override it in a subclass to change its behavior.

Example:
    >>> shell = LazyOwnShell()
    >>> shell.emptyline()
    You didn't enter any command.

## load_user_commands
Carga los comandos personalizados desde user_commands.json

## save_user_command
Guarda un nuevo comando en user_commands.json

## list_files_in_directory
Lista todos los archivos en un directorio dado.

## register_tool_commands
Register every active ``tools/*.tool`` as a ``do_<toolname>`` command.

Placeholders in the tool's ``command`` template are resolved at call
time against ``self.params`` (so live config changes are honored).
Optional positional args passed to the command override ``port`` and
are appended as extra flags. When ``sessions/scan_<rhost>.nmap.xml``
exists and the tool's triggers match a discovered service, the host
and port are pre-populated from the scan; otherwise the command falls
back to ``rhost``/``rport`` from ``payload.json``.

Returns:
    None

## _register_lua_command
Registra un comando nuevo desde Lua.

## load_plugins
Load every Lua plugin from the 'plugins/' directory.

## load_yaml_plugins
Loads all YAML plugins from the 'lazyaddons/' directory.

This method scans the 'lazyaddons/' directory, reads each YAML file,
and registers enabled plugins as new commands.

## register_yaml_plugin
Register a YAML addon as a shell command.

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

## register_all_adversary_commands
No description available.

## _register_adversary_command
No description available.

## display_toastr
Display a toastr-like notification in the terminal with adaptive sizing.

## _wrap_text
Helper method to wrap text to fit within specified width.

## completedefault
Fall through to the payload-aware completer for unhandled commands.

## preloop
Print a session-start pro tip and handle first-run setup.

Also attempts auto-login via remember-me token.
If no session exists, warns the operator to use ``login``.

## postparsing_precmd
Gate unauthenticated commands — anonymous operators can only
run ``login``, ``logout``, ``whoami``, ``help``, ``exit``, ``quit``,
and ``set`` until they identify themselves.

Returns:
    The original statement to allow execution, or a statement with
    an empty command string to block execution.

## postloop
Handle operations to perform after exiting the command loop.

This method is called after the command loop terminates, typically used
for performing any final cleanup or displaying messages before the program
exits.

In this implementation, it prints a message indicating that the custom
shell is exiting.

License: This function is part of a program released under the GNU General
Public License v3.0 (GPLv3). You can redistribute it and/or modify it
under the terms of the GPLv3, as published by the Free Software Foundation.

Note: This method is called automatically by the `cmd` library's command
loop after the loop terminates. You can override it in a subclass to
customize its behavior.

Example:
    >>> shell = LazyOwnShell()
    >>> shell.cmdloop()  # Exits the command loop
    GoodBye LazyOwner

## complete_phase
Tab-complete phase names.

## complete_l00t
Tab-complete l00t subcommands.

## complete_loot
Tab-complete loot subcommands (delegates to l00t).

## complete_assign
Tab-complete the parameter name from the live payload keys.

Driven entirely by ``self.params`` so the framework never has to
maintain a parallel list of completion targets — adding a new key to
``payload.json`` makes it tab-completable for free.

## complete_scope
Tab-complete the scope subcommands.

## _scope_entries
Return the current scope as a fresh mutable list of entry strings.

## _scope_save
Persist scope and/or mode changes to ``payload.json``.

Mutates ``self.params`` in place and writes through the same atomic
``save_payload`` path used by ``assign``, keeping a single writer for
the config file.

Args:
    entries: Replacement scope list, or ``None`` to leave it unchanged.
    mode: Replacement enforcement mode, or ``None`` to leave it
        unchanged.

## _scope_render
Print the current scope and enforcement mode.

## complete_palette
Tab-complete the palette command using the live command index.

Position 1 yields phase identifiers and the ``--search`` / ``--info``
verbs; position 2 yields phase-scoped command names (or every name
when the first token is ``--info``). Driven entirely by
:class:`cli.palette_command.PaletteCompleter` so the framework never
has to maintain a parallel completion list — regenerating the index
is enough.

## lazysearch
Runs the internal module `modules/lazysearch.py`.

This method executes the `lazysearch` script from the specified path, using
the `binary_name` parameter from the `self.params` dictionary. If `binary_name`
is not set, it prints an error message.

:return: None

## lazysearch_gui
Run the internal module located at `modules/LazyOwnExplorer.py`.

This method executes the `LazyOwnExplorer.py` script, which is used for graphical user interface (GUI) functionality within the LazyOwn framework.

The function performs the following steps:

1. Calls `self.run_script` with `LazyOwnExplorer.py` to execute the GUI module.

:returns: None

Manual execution:
1. Ensure that the `modules/LazyOwnExplorer.py` script is present in the `modules` directory.
2. Run the script with:
    `python3 modules/LazyOwnExplorer.py`

Example:
    To run `LazyOwnExplorer.py` directly, execute:
    `python3 modules/LazyOwnExplorer.py`

Note:
    - Ensure that the script has the appropriate permissions and dependencies to run.
    - Verify that your environment supports GUI operations if using this script in a non-graphical environment.

## lazyown
Run the internal module located at `modules/lazyown.py`.

This method executes the `lazyown.py` script, which is a core component of the LazyOwn framework.

The function performs the following steps:

1. Calls `self.run_script` with `lazyown.py` to execute the script.

:returns: None

Manual execution:
1. Ensure that the `modules/lazyown.py` script is present in the `modules` directory.
2. Run the script with:
    `python3 modules/lazyown.py`

Example:
    To run `lazyown.py` directly, execute:
    `python3 modules/lazyown.py`

Note:
    - Ensure that the script has the appropriate permissions and dependencies to run.

## update_db
Run the internal module located at `modules/update_db.sh`.

This method executes the `update_db.sh` script to update the database of binary exploitables from `gtofbins`.

The function performs the following steps:

1. Executes the `update_db.sh` script located in the `modules` directory using `os.system`.

:returns: None

Manual execution:
1. Ensure that the `modules/update_db.sh` script is present in the `modules` directory.
2. Run the script with:
    `./modules/update_db.sh`

Example:
    To manually update the database, execute:
    `./modules/update_db.sh`

Note:
    - Ensure that the script has execute permissions.
    - The script should be run with the necessary privileges if required.

## lazynmap
Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.

OS detection (via ping TTL) is performed automatically before scanning
when the target OS is not yet known. This ensures the correct tool chain
is selected for subsequent enumeration: SMB/Kerberos/AD for Windows,
SSH/web for Linux/Unix.

This method executes the `lazynmap` script, using the current working directory
and the `rhost` parameter from the `self.params` dictionary as the target IP.
If `rhost` is not set, it prints an error message.

:return: None

## lazywerkzeugdebug
Run the internal module located at `modules/legacy/lazywerkzeug.py` in debug mode.

This method executes the `lazywerkzeug.py` script with the specified parameters for remote and local hosts and ports. It is used to test Werkzeug in debug mode.

The function performs the following steps:

1. Retrieves the `rhost`, `lhost`, `rport`, and `lport` values from `self.params`.
2. Checks if all required parameters are set. If not, prints an error message and returns.
3. Calls `self.run_script` with `lazywerkzeug.py` and the specified parameters.

:param rhost: The remote host address.
:type rhost: str

:param lhost: The local host address.
:type lhost: str

:param rport: The remote port number.
:type rport: int

:param lport: The local port number.
:type lport: int

:returns: None

Manual execution:
1. Ensure that `rhost`, `lhost`, `rport`, and `lport` are assign in `self.params`.
2. The script `modules/legacy/lazywerkzeug.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazywerkzeug.py <rhost> <rport> <lhost> <lport>`

Example:
    To run `lazywerkzeug.py` with `rhost` assign to `"127.0.0.1"`, `rport` to `5000`, `lhost` to `"localhost"`, and `lport` to `8000`, set:
    `self.params["rhost"] = "127.0.0.1"`
    `self.params["rport"] = 5000`
    `self.params["lhost"] = "localhost"`
    `self.params["lport"] = 8000`
    Then call:
    `run_lazywerkzeugdebug()`

Note:
    - Ensure that `modules/legacy/lazywerkzeug.py` has the appropriate permissions and dependencies to run.
    - Verify that the specified hosts and ports are correct and available.

## lazygath
Run the internal module located at `modules/lazygat.sh`. to gathering the sistem :)

This method executes the `lazygat.sh` script located in the `modules` directory with `sudo` privileges.

The function performs the following steps:

1. Retrieves the current working directory.
2. Executes the `lazygat.sh` script using `sudo` to ensure it runs with elevated permissions.

:returns: None

Manual execution:
1. Ensure that the `modules/lazygat.sh` script is present in the `modules` directory.
2. Run the script with:
    `sudo ./modules/lazygat.sh`

Example:
    To manually run the script with elevated privileges, execute:
    `sudo ./modules/lazygat.sh`

Note:
    - Ensure that the script has execute permissions.
    - The script should be run with `sudo` if it requires elevated privileges.

## lazynmapdiscovery
Runs the internal module `modules/lazynmap.sh` with discovery mode.

This method executes the `lazynmap` script in discovery mode. It uses the current
working directory for locating the script.

:return: None

## lazysniff
Run the sniffer internal module located at `modules/legacy/lazysniff.py` with the specified parameters.

This method executes the script with the following arguments:

- `device`: The network interface to be used for sniffing, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `device` value from `self.params`.
2. Sets up the environment variables `LANG` and `TERM` to ensure proper script execution.
3. Uses `subprocess.run` to execute the `lazysniff.py` script with the `-i` option to specify the network interface.

:param device: The network interface to be used for sniffing.
:type device: str

:returns: None

Manual execution:
1. Ensure that `device` is assign in `self.params`.
2. The script `modules/legacy/lazysniff.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazysniff.py -i <device>`

Example:
    To run `lazysniff` with `device` assign to `"eth0"`, set:
    `self.params["device"] = "eth0"`
    Then call:
    `run_lazysniff()`

Note:
    - Ensure that `modules/legacy/lazysniff.py` has the appropriate permissions and dependencies to run.
    - Ensure that the network interface specified is valid and properly configured.

## lazyftpsniff
Run the sniffer ftp internal module located at `modules/legacy/lazyftpsniff.py` with the specified parameters.

This function executes the script with the following arguments:

- `device`: The network interface to be used for sniffing, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `device` value from `self.params`.
2. Sets up the environment variables `LANG` and `TERM` to ensure proper script execution.
3. Uses `subprocess.run` to execute the `lazyftpsniff.py` script with the `-i` option to specify the network interface.

:param device: The network interface to be used for sniffing.
:type device: str

:returns: None

Manual execution:
1. Ensure that `device` is assign in `self.params`.
2. The script `modules/legacy/lazyftpsniff.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazyftpsniff.py -i <device>`

Example:
    To run `lazyftpsniff` with `device` assign to `"eth0"`, set:
    `self.params["device"] = "eth0"`
    Then call:
    `run_lazyftpsniff()`

Note:
    - Ensure that `modules/legacy/lazyftpsniff.py` has the appropriate permissions and dependencies to run.
    - Ensure that the network interface specified is valid and properly configured.

## lazynetbios
Run the internal module to search netbios vuln victims, located at `modules/legacy/lazynetbios.py` with the specified parameters.

This function executes the script with the following arguments:

- `startip`: The starting IP address for the NetBIOS scan, specified in `self.params`.
- `endip`: The ending IP address for the NetBIOS scan, specified in `self.params`.
- `spoof_ip`: The IP address to be used for spoofing, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `startip`, `endip`, and `spoof_ip` values from `self.params`.
2. Uses `subprocess.run` to execute the `lazynetbios.py` script with the specified parameters.

:param startip: The starting IP address for the NetBIOS scan.
:type startip: str

:param endip: The ending IP address for the NetBIOS scan.
:type endip: str

:param spoof_ip: The IP address to be used for spoofing.
:type spoof_ip: str

:returns: None

Manual execution:
1. Ensure that `startip`, `endip`, and `spoof_ip` are assign in `self.params`.
2. The script `modules/legacy/lazynetbios.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazynetbios.py <startip> <endip> <spoof_ip>`

Example:
    To run `lazynetbios` with `startip` assign to `"192.168.1.1"`, `endip` assign to `"192.168.1.10"`, and `spoof_ip` assign to `"192.168.1.100"`, assign:
    `self.params["startip"] = "192.168.1.1"`
    `self.params["endip"] = "192.168.1.10"`
    `self.params["spoof_ip"] = "192.168.1.100"`
    Then call:
    `run_lazynetbios()`

Note:
    - Ensure that `modules/legacy/lazynetbios.py` has the appropriate permissions and dependencies to run.
    - Ensure that the IP addresses are correctly set and valid for the NetBIOS scan.

## lazyhoneypot
Run the internal module located at `modules/legacy/lazyhoneypot.py` with the specified parameters.

This function executes the script with the following arguments:

- `email_from`: The email address from which messages will be sent, specified in `self.params`.
- `email_to`: The recipient email address, specified in `self.params`.
- `email_username`: The username for email authentication, specified in `self.params`.
- `email_password`: The password for email authentication, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `email_from`, `email_to`, `email_username`, and `email_password` values from `self.params`.
2. Calls the `run_script` method to execute the `lazyhoneypot.py` script with the provided email parameters.

:param email_from: The email address from which messages will be sent.
:type email_from: str

:param email_to: The recipient email address.
:type email_to: str

:param email_username: The username for email authentication.
:type email_username: str

:param email_password: The password for email authentication.
:type email_password: str

:returns: None

Manual execution:
1. Ensure that `email_from`, `email_to`, `email_username`, and `email_password` are assign in `self.params`.
2. The script `modules/legacy/lazyhoneypot.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazyhoneypot.py --email_from <email_from> --email_to <email_to> --email_username <email_username> --email_password <email_password>`

Example:
    To run `lazyhoneypot` with `email_from` assign to `"sender@example.com"`, `email_to` assign to `"recipient@example.com"`, `email_username` assign to `"user"`, and `email_password` assign to `"pass"`, set:
    `self.params["email_from"] = "sender@example.com"`
    `self.params["email_to"] = "recipient@example.com"`
    `self.params["email_username"] = "user"`
    `self.params["email_password"] = "pass"`
    Then call:
    `run_lazyhoneypot()`

Note:
    - Ensure that `modules/legacy/lazyhoneypot.py` has the appropriate permissions and dependencies to run.
    - Ensure that the email credentials are correctly set for successful authentication and operation.

## lazysearch_bot
Run the internal module GROQ AI located at `modules/legacy/lazysearch_bot.py` with the specified parameters.

This function executes the script with the following arguments:

- `prompt`: The prompt to be used by the script, specified in `self.params`.
- `api_key`: The API key to be assign in the environment variable `GROQ_API_KEY`, specified in `self.params`.

The function performs the following steps:

1. Retrieves the `prompt` and `api_key` values from `self.params`.
2. Checks if both `prompt` and `api_key` are assign. If either is missing, it prints an error message and returns.
3. Sets the environment variable `GROQ_API_KEY` with the provided `api_key`.
4. Calls the `run_script` method to execute the `lazysearch_bot.py` script with the `--prompt` argument.

:param prompt: The prompt to be used by the script.
:type prompt: str

:param api_key: The API key for accessing the service.
:type api_key: str

:returns: None

Manual execution:
1. Ensure that `prompt` and `api_key` are assign in `self.params`.
2. The script `modules/legacy/lazysearch_bot.py` should be present in the `modules` directory.
3. Set the environment variable `GROQ_API_KEY` with the API key value.
4. Run the script with:
    `python3 modules/legacy/lazysearch_bot.py --prompt <prompt>`

Example:
    To run `lazysearch_bot` with `prompt` assign to `"Search query"` and `api_key` assign to `"your_api_key"`, assign:
    `self.params["prompt"] = "Search query"`
    `self.params["api_key"] = "your_api_key"`
    Then call:
    `run_lazysearch_bot()`

Note:
    - Ensure that `modules/legacy/lazysearch_bot.py` has the appropriate permissions and dependencies to run.
    - The environment variable `GROQ_API_KEY` must be correctly assign for the script to function.

## lazymetaextract0r
Run the Metadata extractor internal module located at `modules/lazyown_metaextract0r.py` with the specified parameters.

This function executes the script with the following arguments:

- `path`: The file path to be processed by the script, specified in `self.params`.

The function performs the following steps:

1. Retrieves the value for `path` from `self.params`.
2. Checks if the `path` parameter is assign. If not, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazyown_metaextract0r.py` script with the appropriate argument.

:param path: The file path to be processed by the script.
:type path: str

:returns: None

Manual execution:
1. Ensure that `path` is assign in `self.params`.
2. The script `modules/lazyown_metaextract0r.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazyown_metaextract0r.py --path <path>`

Example:
    To run `lazyown_metaextract0r` with `path` assign to `/home/user/file.txt`, set:
    `self.params["path"] = "/home/user/file.txt"`
    Then call:
    `run_lazymetaextract0r()`

Note:
    - Ensure that `modules/lazyown_metaextract0r.py` has the appropriate permissions and dependencies to run.

## lazyownratcli
Run the internal module located at `modules/lazyownclient.py` with the specified parameters.

This function executes the script with the following arguments:

- `lhost`: The IP address of the local host, specified in `self.params`.
- `lport`: The port number of the local host, specified in `self.params`.
- `rat_key`: The RAT key, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `lhost`, `lport`, and `rat_key` from `self.params`.
2. Checks if all required parameters (`lhost`, `lport`, and `rat_key`) are set. If any are missing, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazyownclient.py` script with the appropriate arguments.

:param lhost: The IP address of the local host.
:type lhost: str
:param lport: The port number of the local host.
:type lport: int
:param rat_key: The RAT key.
:type rat_key: str

:returns: None

Manual execution:
1. Ensure that `lhost`, `lport`, and `rat_key` are assign in `self.params`.
2. The script `modules/lazyownclient.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazyownclient.py --host <lhost> --port <lport> --key <rat_key>`

Example:
    To run `lazyownclient` with `lhost` assign to `192.168.1.10`, `lport` assign to `8080`, and `rat_key` assign to `my_secret_key`, set:
    `self.params["lhost"] = "192.168.1.10"`
    `self.params["lport"] = 8080`
    `self.params["rat_key"] = "my_secret_key"`
    Then call:
    `run_lazyownratcli()`

Note:
    - Ensure that `modules/lazyownclient.py` has the appropriate permissions and dependencies to run.

## lazyownrat
Run the internal module located at `modules/lazyownserver.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host, specified in `self.params`.
- `rport`: The port number of the remote host, specified in `self.params`.
- `rat_key`: The RAT key, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rhost`, `rport`, and `rat_key` from `self.params`.
2. Checks if all required parameters (`rhost`, `rport`, and `rat_key`) are set. If any are missing, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazyownserver.py` script with the appropriate arguments.

:param rhost: The IP address of the remote host.
:type rhost: str
:param rport: The port number of the remote host.
:type rport: int
:param rat_key: The RAT key.
:type rat_key: str

:returns: None

Manual execution:
1. Ensure that `rhost`, `rport`, and `rat_key` are assign in `self.params`.
2. The script `modules/lazyownserver.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/lazyownserver.py --host <rhost> --port <rport> --key <rat_key>`

Example:
    To run `lazyownserver` with `rhost` set to `192.168.1.10`, `rport` assign to `8080`, and `rat_key` assign to `my_secret_key`, set:
    `self.params["rhost"] = "192.168.1.10"`
    `self.params["rport"] = 8080`
    `self.params["rat_key"] = "my_secret_key"`
    Then call:
    `run_lazyownrat()`

Note:
    - Ensure that `modules/lazyownserver.py` has the appropriate permissions and dependencies to run.

## lazybotnet
Run the internal module located at `modules/legacy/lazybotnet.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host, hardcoded to "0.0.0.0".
- `rport`: The port number of the remote host, specified in `self.params`.
- `rat_key`: The RAT key, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rport` and `rat_key` from `self.params`. The `rhost` is hardcoded to "0.0.0.0".
2. Checks if all required parameters (`rport` and `rat_key`) are set. If any are missing, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazybotnet.py` script with the appropriate arguments.

:param rport: The port number of the remote host.
:type rport: int
:param rat_key: The RAT key.
:type rat_key: str

:returns: None

Manual execution:
1. Ensure that `rport` and `rat_key` are assign in `self.params`.
2. The script `modules/legacy/lazybotnet.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazybotnet.py --host <rhost> --port <rport> --key <rat_key>`

Example:
    To run `lazybotnet` with `rport` assign to `1234` and `rat_key` assign to `my_key`, assign:
    `self.params["rport"] = 1234`
    `self.params["rat_key"] = "my_key"`
    Then call:
    `run_lazybotnet()`

Note:
    - Ensure that `modules/legacy/lazybotnet.py` has the appropriate permissions and dependencies to run.

## lazylfi2rce
Run the internal module located at `modules/legacy/lazylfi2rce.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host, specified in `self.params`.
- `rport`: The port number of the remote host, specified in `self.params`.
- `lhost`: The IP address of the local host, specified in `self.params`.
- `lport`: The port number of the local host, specified in `self.params`.
- `field`: The field name for the LFI (Local File Inclusion) attack, specified in `self.params`.
- `wordlist`: The path to the wordlist file used for the attack, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rhost`, `rport`, `lhost`, `lport`, `field`, and `wordlist` from `self.params`.
2. Checks if all required parameters are set. If any are missing, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazylfi2rce.py` script with the appropriate arguments.

:param rhost: The IP address of the remote host.
:type rhost: str
:param rport: The port number of the remote host.
:type rport: int
:param lhost: The IP address of the local host.
:type lhost: str
:param lport: The port number of the local host.
:type lport: int
:param field: The field name for the LFI attack.
:type field: str
:param wordlist: The path to the wordlist file.
:type wordlist: str

:returns: None

Manual execution:
1. Ensure that `rhost`, `rport`, `lhost`, `lport`, `field`, and `wordlist` are assign in `self.params`.
2. The script `modules/legacy/lazylfi2rce.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazylfi2rce.py --rhost <rhost> --rport <rport> --lhost <lhost> --lport <lport> --field <field> --wordlist <wordlist>`

Example:
    To run the lazylfi2rce with `rhost` assign to `192.168.1.1`, `rport` assign to `80`, `lhost` assign to `192.168.1.2`, `lport` assign to `8080`, `field` assign to `file`, and `wordlist` assign to `path/to/wordlist.txt`, set:
    `self.params["rhost"] = "192.168.1.1"`
    `self.params["rport"] = 80`
    `self.params["lhost"] = "192.168.1.2"`
    `self.params["lport"] = 8080`
    `self.params["field"] = "file"`
    `self.params["wordlist"] = "path/to/wordlist.txt"`
    Then call:
    `run_lazylfi2rce()`

Note:
    - Ensure that `modules/legacy/lazylfi2rce.py` has the appropriate permissions and dependencies to run.

## lazylogpoisoning
Run the internal module located at `modules/legacy/lazylogpoisoning.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host, specified in `self.params`.
- `lhost`: The IP address of the local host, specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rhost` and `lhost` from `self.params`.
2. Checks if the required parameters `rhost` and `lhost` are assign. If not, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazylogpoisoning.py` script with the appropriate arguments.

:param rhost: The IP address of the remote host. Must be assign in `self.params`.
:type rhost: str
:param lhost: The IP address of the local host. Must be assign in `self.params`.
:type lhost: str

:returns: None

Manual execution:
1. Ensure that `rhost` and `lhost` are assign in `self.params`.
2. The script `modules/legacy/lazylogpoisoning.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazylogpoisoning.py --rhost <rhost> --lhost <lhost>`

Example:
    To run the lazylogpoisoning with `rhost` assign to `192.168.1.1` and `lhost` assign to `192.168.1.2`, set:
    `self.params["rhost"] = "192.168.1.1"`
    `self.params["lhost"] = "192.168.1.2"`
    Then call:
    `run_lazylogpoisoning()`

Note:
    - Ensure that `modules/legacy/lazylogpoisoning.py` has the appropriate permissions and dependencies to run.

## lazybotcli
Run the internal module located at `modules/legacy/lazybotcli.py` with the specified parameters.

This function executes the script with the following arguments:

- `rhost`: The IP address of the remote host (default is `"0.0.0.0"`).
- `rport`: The port number to be used, specified in `self.params`.
- `rat_key`: The key for the Remote Access Tool (RAT), specified in `self.params`.

The function performs the following steps:

1. Retrieves the values for `rport` and `rat_key` from `self.params`.
2. Checks if the required parameters `rport` and `rat_key` are assign. If not, it prints an error message and returns.
3. Calls the `run_script` method to execute the `lazybotcli.py` script with the appropriate arguments.

:param rport: The port number for the connection. Must be assign in `self.params`.
:type rport: int
:param rat_key: The key for the RAT. Must be assign in `self.params`.
:type rat_key: str

:returns: None

Manual execution:
1. Ensure that `rport` and `rat_key` are assign in `self.params`.
2. The script `modules/legacy/lazybotcli.py` should be present in the `modules` directory.
3. Run the script with:
    `python3 modules/legacy/lazybotcli.py --host 0.0.0.0 --port <rport> --key <rat_key>`

Example:
    To run the lazybotcli with port `12345` and key `mysecretkey`, set:
    `self.params["rport"] = 12345`
    `self.params["rat_key"] = "mysecretkey"`
    Then call:
    `run_lazybotcli()`

Note:
    - Ensure that `modules/legacy/lazybotcli.py` has the appropriate permissions and dependencies to run.

## lazyssh77enum
Run the internal module located at `modules/lazybrutesshuserenum.py` with the specified parameters. ONLY valid for 7.x Version !!!

The script will be executed with the following arguments:

- `wordlist`: The path to the wordlist file containing potential usernames for SSH enumeration.
- `rhost`: The target IP address or hostname for SSH enumeration.

The function performs the following steps:

1. Retrieves the values for `wordlist` and `rhost` from `self.params`.
2. Prints a warning message about the potential inaccuracy of the results.
3. Constructs the command to run the `lazybrutesshuserenum.sh` script with the specified arguments.
4. Executes the command using the `os.system` method.

:param wordlist: The path to the wordlist file for username enumeration. Must be assign in `self.params`.
:type wordlist: str
:param rhost: The target IP address or hostname for SSH enumeration. Must be assign in `self.params`.
:type rhost: str

:returns: None

Manual execution:
1. Ensure that `wordlist` and `rhost` are assign in `self.params`.
2. Run the script `modules/lazybrutesshuserenum.sh` with the appropriate arguments.

Dependencies:
- `modules/lazybrutesshuserenum.sh` must be present in the `modules` directory and must be executable.

Example:
    To run the SSH user enumeration with a wordlist located at `/path/to/wordlist.txt` and target IP `192.168.1.1`, set:
    `self.params["usrwordlist"] = "/path/to/wordlist.txt"`
    `self.params["rhost"] = "192.168.1.1"`
    Then call:
    `run_lazyssh77enum()`

Note:
    - The accuracy of the results may vary depending on the version of the script and the wordlist used.

## lazyburpfuzzer
Run the internal module located at `modules/lazyown_burpfuzzer.py` with the specified parameters.

The script will be executed with the following arguments:

- `--url`: The target URL for the fuzzer.
- `--method`: The HTTP method to use (e.g., GET, POST).
- `--proxy_port`: The port for the proxy server.
- `--headers`: Optional HTTP headers to include in the request.
- `--data`: Optional data to include in the request body.
- `--params`: Optional URL parameters to include in the request.
- `--json_data`: Optional JSON data to include in the request body.
- `-w`: Optional wordlist for fuzzing.
- `-hc`: Optional hide code for fuzzing.

The function performs the following steps:

1. Retrieves the values for `url`, `method`, `headers`, `params`, `data`, `json_data`, `proxy_port`, `wordlist`, and `hide_code` from `self.params`.
2. Constructs the command to run the `lazyown_burpfuzzer.py` script with the specified arguments.
3. Adds optional parameters based on whether the corresponding files (`headers_file`, `data_file`, `params_file`, `json_data_file`) are provided.
4. Executes the command using the `run_command` method.

:param url: The target URL for the fuzzer. Must be assign in `self.params`.
:type url: str
:param method: The HTTP method to use. Must be assign in `self.params`.
:type method: str
:param headers: Optional HTTP headers. Must be assign in `self.params` or provided via `headers_file`.
:type headers: str
:param params: Optional URL parameters. Must be assign in `self.params` or provided via `params_file`.
:type params: str
:param data: Optional data for the request body. Must be assign in `self.params` or provided via `data_file`.
:type data: str
:param json_data: Optional JSON data for the request body. Must be assign in `self.params` or provided via `json_data_file`.
:type json_data: str
:param proxy_port: The port for the proxy server. Must be assign in `self.params`.
:type proxy_port: int
:param wordlist: Optional wordlist for fuzzing. Must be assign in `self.params`.
:type wordlist: str
:param hide_code: Optional code to hide. Must be assign in `self.params`.
:type hide_code: int
:param headers_file: Optional file containing headers.
:type headers_file: str, optional
:param data_file: Optional file containing data.
:type data_file: str, optional
:param params_file: Optional file containing parameters.
:type params_file: str, optional
:param json_data_file: Optional file containing JSON data.
:type json_data_file: str, optional

:returns: None

Manual execution:
1. Ensure that `url`, `method`, and `proxy_port` are assign in `self.params`.
2. Provide additional parameters as needed.
3. Run the script `modules/lazyown_burpfuzzer.py` with the appropriate arguments.

Dependencies:
- `modules/lazyown_burpfuzzer.py` must be present in the `modules` directory and must be executable.

Example:
    To run the fuzzer with URL `http://example.com`, HTTP method `POST`, and proxy port `8080`, set:
    `self.params["url"] = "http://example.com"`
    `self.params["method"] = "POST"`
    `self.params["proxy_port"] = 8080`
    Then call:
    `run_lazyburpfuzzer()`

Note:
    - Ensure that all required parameters are assign before calling this function.
    - Parameters can also be provided via corresponding files.

## lazyreverse_shell
Run the internal module located at `modules/lazyreverse_shell.sh` with the specified parameters.

The script will be executed with the following arguments:
- `--ip`: The IP address to use for the reverse shell.
- `--puerto`: The port to use for the reverse shell.

The function performs the following steps:

1. Retrieves the values for `rhost` (IP address) and `reverse_shell_port` (port) from `self.params`.
2. Validates that `rhost` and `reverse_shell_port` parameters are assign.
3. Constructs the command to run the `lazyreverse_shell.sh` script with the specified arguments.
4. Executes the command.

:param ip: The IP address to use for the reverse shell. Must be assign in `self.params`.
:type ip: str
:param port: The port to use for the reverse shell. Must be assign in `self.params`.
:type port: str

:returns: None

Manual execution:
1. Ensure that `rhost` and `reverse_shell_port` are assign in `self.params`.
2. Run the script `modules/lazyreverse_shell.sh` with the appropriate arguments.

Dependencies:
- `modules/lazyreverse_shell.sh` must be present in the `modules` directory and must be executable.

Example:
    To assign up a reverse shell with IP `192.168.1.100` and port `4444`, assign:
    `self.params["rhost"] = "192.168.1.100"`
    `self.params["reverse_shell_port"] = "4444"`
    Then call:
    `run_lazyreverse_shell()`

Note:
    - Ensure that `modules/lazyreverse_shell.sh` has the necessary permissions to execute.
    - Parameters must be assign before calling this function.

## lazyarpspoofing
Run the internal module located at `modules/legacy/lazyarpspoofing.py` with the specified parameters.

The script will be executed with the following arguments:
- `--device`: The network interface to use for ARP spoofing.
- `lhost`: The local host IP address to spoof.
- `rhost`: The remote host IP address to spoof.

The function performs the following steps:

1. Retrieves the values for `lhost`, `rhost`, and `device` from `self.params`.
2. Validates that `lhost`, `rhost`, and `device` parameters are assign.
3. Constructs the command to run the `lazyarpspoofing.py` script with the specified arguments.
4. Executes the command.

:param lhost: The local host IP address to spoof. Must be assign in `self.params`.
:type lhost: str
:param rhost: The remote host IP address to spoof. Must be assign in `self.params`.
:type rhost: str
:param device: The network interface to use for ARP spoofing. Must be assign in `self.params`.
:type device: str

:returns: None

Manual execution:
1. Ensure that `lhost`, `rhost`, and `device` are assign in `self.params`.
2. Run the script `modules/legacy/lazyarpspoofing.py` with the appropriate arguments.

Dependencies:
- `modules/legacy/lazyarpspoofing.py` must be present in the `modules` directory and must be executable.

Example:
    To execute ARP spoofing with local host `192.168.1.2`, remote host `192.168.1.1`, and device `eth0`, set:
    `self.params["lhost"] = "192.168.1.2"`
    `self.params["rhost"] = "192.168.1.1"`
    `self.params["device"] = "eth0"`
    Then call:
    `run_lazyarpspoofing()`

Note:
    - Ensure that `modules/legacy/lazyarpspoofing.py` has the necessary permissions to execute.
    - Parameters must be assign before calling this function.

## lazyattack
Run the internal module located at `modules/lazyatack.sh` with the specified parameters.

The script will be executed with the following arguments:
- `--modo`: The mode of the attack.
- `--ip`: The target IP address.
- `--atacante`: The attacker IP address.

The function performs the following steps:

1. Retrieves the current working directory.
2. Validates that `mode`, `rhost`, and `lhost` parameters are assign.
3. Constructs the command to run the `lazyatack.sh` script with the specified arguments.
4. Executes the command.

:param mode: The mode in which the attack should be run. Must be assign in `self.params`.
:type mode: str
:param target_ip: The IP address of the target. Must be assign in `self.params`.
:type target_ip: str
:param attacker_ip: The IP address of the attacker. Must be assign in `self.params`.
:type attacker_ip: str

:returns: None

Manual execution:
1. Ensure that `mode`, `rhost`, and `lhost` are assign in `self.params`.
2. Run the script `modules/lazyatack.sh` with the appropriate arguments.

Dependencies:
- `modules/lazyatack.sh` must be present in the `modules` directory and must be executable.

Example:
    To execute the attack with mode `scan`, target IP `192.168.1.100`, and attacker IP `192.168.1.1`, assign:
    `self.params["mode"] = "scan"`
    `self.params["rhost"] = "192.168.1.100"`
    `self.params["lhost"] = "192.168.1.1"`
    Then call:
    `run_lazyattack()`

Note:
    - Ensure that `modules/lazyatack.sh` has the necessary permissions to execute.
    - Parameters must be assign before calling this function.

## lazymsfvenom
Executes the `msfvenom` tool to generate a variety of payloads based on user input.

This function prompts the user to select a payload type from a predefined list and runs the corresponding
`msfvenom` command to create the desired payload. It handles tasks such as generating different types of
payloads for Linux, Windows, macOS, and Android systems, including optional encoding with Shikata Ga Nai for C payloads.

The generated payloads are moved to a `sessions` directory, where appropriate permissions are assign. Additionally,
the payloads can be compressed using UPX for space efficiency. If the selected payload is an Android APK,
the function will also sign the APK and perform necessary post-processing steps.

:param line: Command line arguments for the script.
:return: None

## lazyaslrcheck
Creates a path hijacking attack by performing the following steps:

1. Appends the value of `binary_name` to a temporary script located at `modules/tmp.sh`.
2. Copies this temporary script to `/tmp` with the name specified by `binary_name`.
3. Sets executable permissions on the copied script.
4. Prepends `/tmp` to the system's PATH environment variable to ensure the script is executed in preference to other binaries.

The function then prints out each command being executed and a message indicating the binary name used for the path hijacking.

:param binary_name: The name of the binary to be used in the path hijacking attack. It should be assign in `self.params` before calling this method.
:type binary_name: str

:returns: None

Manual execution:
1. Ensure that `binary_name` is assign in `self.params`.
2. Append the binary name to `modules/tmp.sh`.
3. Copy `modules/tmp.sh` to `/tmp/{binary_name}`.
4. assign executable permissions on the copied file.
5. Update the PATH environment variable to prioritize `/tmp`.

Dependencies:
- The `self.params` dictionary must contain a valid `binary_name`.
- Ensure that `modules/tmp.sh` exists and contains appropriate content for the attack.

Example:
    To execute the path hijacking attack with `binary_name` as `malicious`, ensure `self.params["binary_name"]` is assign to `"malicious"`, and then call:
    `run_lazypathhijacking()`

Note:
    - The `binary_name` parameter must be a string representing the name of the binary to hijack.
    - The method modifies the PATH environment variable, which may affect the execution of other binaries.

## lazypathhijacking
Creates a path hijacking attack by performing the following steps:

1. Appends the value of `binary_name` to a temporary script located at `modules/tmp.sh`.
2. Copies this temporary script to `/tmp` with the name specified by `binary_name`.
3. Sets executable permissions on the copied script.
4. Prepends `/tmp` to the system's PATH environment variable to ensure the script is executed in preference to other binaries.

The function then prints out each command being executed and a message indicating the binary name used for the path hijacking.

:param binary_name: The name of the binary to be used in the path hijacking attack.
:returns: None

## script
Run a script with the given arguments

This method constructs and executes a command to run a Python script with the specified arguments. It uses the `run_command` method to execute the script and handle real-time output.

:param script_name: The name of the script to be executed.
:type script_name: str
:param args: The arguments to be passed to the script.
:type args: tuple of str

:returns: None

Manual execution:
1. Build the command list with "python3", the script name, and the arguments.
2. Call `run_command` with the constructed command list.

Dependencies:
- `run_command` method for executing the constructed command and streaming output.

Example:
    To execute a script named `example.py` with arguments `arg1` and `arg2`, call:
    `run_script("example.py", "arg1", "arg2")`

Note:
    - The `script_name` parameter should be a string representing the name of the script.
    - The `args` parameter is a variable-length argument list containing the arguments to be passed to the script.
    - Ensure that the script and arguments are properly specified.

## command
Run a command and print output in real-time

This method executes a given command using `subprocess.Popen` and streams both the standard output and standard error to the console in real-time. The output from both streams is appended to the `self.output` attribute. If interrupted, the process is terminated gracefully.

:param command: The command to be executed.
:type command: str

:returns: None

Manual execution:
1. Execute the command specified by the `command` parameter.
2. Stream and print the command's standard output and error to the console in real-time.
3. Append all output to the `self.output` attribute.
4. Handle `KeyboardInterrupt` by terminating the process and printing an error message.

Dependencies:
- `subprocess` module for running the command and capturing output.
- `print_msg` function for printing output to the console.
- `print_error` function for printing error messages to the console.

Example:
    To execute a command, call `run_command("ls -l")`.

Note:
    - The `command` parameter should be a string representing the command to be executed.
    - `self.output` must be initialized before calling this method.
    - Ensure proper exception handling to manage process interruptions.

## _render_chain_next
Render the chain's ``next`` view for the supplied verb (helper).

Args:
    raw_args: The raw argument string passed to ``do_next``.
        Format: ``<verb> [limit]``.

Returns:
    None.

## get_output
Devuelve la salida acumulada

## upload_file_to_c2
Sube un archivo al C2.

Parameters:
file_path (str): Ruta del archivo a subir.

Returns:
None

## complete_upload_c2
Autocomplete implant names from implant_config_*.json files in sessions/ directory

## download_file_from_c2
Descarga un archivo desde el C2.

Parameters:
file_name (str): Nombre del archivo a descargar.
clientid (str): Identificador del cliente (opcional).

Returns:
None

## issue_command_to_c2
Ejecuta un comando en el cliente usando el C2.

Parameters:
command (str): Comando a ejecutar.
client_id (str): ID del cliente (opcional).

Returns:
None

## complete_issue_command_to_c2
Autocomplete: 1st arg = implant name, 2nd arg = beacon command (with : if needed)

## view_code
Display C and ASM code side by side in a curses-based interface.

This function sets up a curses window to display C code and its corresponding
assembly code side by side. It allows the user to select a .c file from the
'sessions' directory and then displays the code with scrolling capabilities
both vertically and horizontally. A green vertical line separates the C code
from the ASM code.

Parameters:
    stdscr (curses.window): The curses window object to draw on.

Returns:
    None

## get_available_actions
Returns a list of available actions using cmd2 introspection.

## _create_strict_yaml_prompt
Create a prompt that strictly enforces YAML response format without any narrative text

## process_scan_csv
Processes a single scan CSV file.

## process_vuln_csv
Processes a single vulnerability CSV file.

## _load_adversaries
No description available.

## _parse_adversary_args
No description available.

## _patch_template_if_needed
No description available.

## _build_command_stack
No description available.

## _display_adversary_info
No description available.

## _execute_commands
No description available.

## event_log
Show recent EventBus events. Usage: event_log [N] [category]

## state_snapshot
Show unified StateManager snapshot (DB + JSON caches).

## route
Route a natural-language prompt to a LazyOwn tool. Usage: route <prompt>

## _persist
No description available.

## wrapper
No description available.

## wrapper_yaml
No description available.

## cmd_wrapper
No description available.

## show_toastr
No description available.

## make_wrapper
No description available.

## tool_wrapper
No description available.

