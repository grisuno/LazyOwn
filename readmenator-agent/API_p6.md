# API (page 6 of 20)
Previous: [API_p5.md](API_p5.md)

## core/errors.py
Depends on: `cli/commands/enum.py`
Imported by: `core/__init__.py`
- `LazyOwnError.__init__` (method) `core/errors.py:61` `def __init__(self, message, error_code)`
- `LazyOwnError.to_dict` (method) `core/errors.py:66` `def to_dict(self)` -- Return a serialisable dict with code, type, and message.
- `ConfigError.__init__` (method) `core/errors.py:81` `def __init__(self, message, error_code)`
- `TargetError.__init__` (method) `core/errors.py:88` `def __init__(self, message, error_code)`
- `AuthError.__init__` (method) `core/errors.py:95` `def __init__(self, message, error_code)`
- `ToolError.__init__` (method) `core/errors.py:102` `def __init__(self, message, error_code)`
- `PayloadError.__init__` (method) `core/errors.py:109` `def __init__(self, message, error_code)`
- `DatabaseError.__init__` (method) `core/errors.py:116` `def __init__(self, message, error_code)`
- `NetworkError.__init__` (method) `core/errors.py:123` `def __init__(self, message, error_code)`
- `PermissionError.__init__` (method) `core/errors.py:130` `def __init__(self, message, error_code)`
- `ValidationError.__init__` (method) `core/errors.py:137` `def __init__(self, message, error_code)`

## core/executor.py
Depends on: `core/logging.py`
Imported by: `tests/test_core_executor.py`
- `safe_run` (function) `core/executor.py:96` `def safe_run(command)`
- `safe_run` (function) `core/executor.py:98` `def safe_run(command)`
- `safe_run` (function) `core/executor.py:101` `def safe_run(command)` -- Execute a command with logging and timeout.
- `run_shell` (function) `core/executor.py:149` `def run_shell(cmd)` -- Execute a shell command and return its stdout.

## core/hardening.py
Depends on: `core/logging.py`
Imported by: `cli/commands/anti_forensics.py`, `cli/commands/cloud.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/exfiltration.py`, `cli/commands/lateral_migrated.py`, `cli/commands/nethelpers.py`, `cli/commands/persist_migrated.py`, `cli/commands/pivoting.py`, `core/process.py`, `core/safe_subprocess.py`, `lazyc2.py`, `lazyown.py`, `modules/phishing_orchestrator.py`, `modules/websocket_beacon.py`, `scripts/devtools/core_smoke.py`, `tests/test_security_hardening_v3.py`, `tests/test_shell_semantics.py`
- `reject_option_injection` (function) `core/hardening.py:40` `def reject_option_injection(argv)` -- Reject argument-injection payloads in argv.
- `escape_powershell_single_quoted` (function) `core/hardening.py:59` `def escape_powershell_single_quoted(value)` -- Escape a value for embedding in a PowerShell single-quoted string.
- `SecurityViolation.terminal_env` (method) `core/hardening.py:82` `def terminal_env(base)` -- Return a child environment that keeps ANSI colors on a pipe.
- `SecurityViolation.safe_subprocess_run` (method) `core/hardening.py:103` `def safe_subprocess_run(argv)` -- Execute a command via subprocess without shell interpretation.
- `SecurityViolation.safe_clipboard_copy` (method) `core/hardening.py:148` `def safe_clipboard_copy(content)` -- Copy content to system clipboard without shell interpretation.
- `SecurityViolation.build_sshpass_command` (method) `core/hardening.py:187` `def build_sshpass_command(password, ssh_args)` -- Build an sshpass command using SSHPASS env var (sshpass -e).
- `SecurityViolation.set_sshpass_env` (method) `core/hardening.py:216` `def set_sshpass_env(password)` -- Create an environment dict with SSHPASS set for sshpass -e.
- `SecurityViolation.escape_html_content` (method) `core/hardening.py:235` `def escape_html_content(value)` -- Escape HTML special characters to prevent XSS.
- `SecurityViolation.safe_path_join` (method) `core/hardening.py:247` `def safe_path_join(base_dir, user_path)` -- Join base_dir and user_path safely, preventing path traversal.
- `SecurityViolation.validate_network_cidr` (method) `core/hardening.py:273` `def validate_network_cidr(cidr)` -- Validate a network CIDR notation string.
- `SecurityViolation.validate_port_spec` (method) `core/hardening.py:285` `def validate_port_spec(ports)` -- Validate a port specification string.
- `SecurityViolation.validate_host` (method) `core/hardening.py:301` `def validate_host(host)` -- Validate a hostname or IP address.
- `SecurityViolation.require_encryption_key` (method) `core/hardening.py:323` `def require_encryption_key(env_key, secret_file)` -- Require a proper encryption key; never fall back to a static default.
- `SecurityViolation.defused_xml_parse` (method) `core/hardening.py:351` `def defused_xml_parse(source)` -- Parse XML safely using defusedxml.
- `SecurityViolation.sanitize_filename` (method) `core/hardening.py:373` `def sanitize_filename(filename, max_length)` -- Sanitize a filename by removing dangerous characters.

## core/http.py
Depends on: `core/console.py`
Imported by: `core/__init__.py`
- `generate_http_req` (function) `core/http.py:18` `def generate_http_req(host, port, uri, custom_header, cmd)` -- Build and send an HTTP GET request.
- `get_banner` (function) `core/http.py:50` `def get_banner(host, port)` -- Fetch a banner by connecting via HTTP to the given host and port.
- `get_command` (function) `core/http.py:69` `def get_command(url, lhost)` -- Fetch a command payload from a remote URL.
- `send_command` (function) `core/http.py:87` `def send_command(cmd, url, lhost)` -- Send a command via HTTP POST.
- `exploitalert` (function) `core/http.py:106` `def exploitalert(content)` -- Parse ExploitAlert search results HTML.
- `packetstormsecurity` (function) `core/http.py:125` `def packetstormsecurity(content)` -- Parse Packet Storm Security search results HTML.
- `nvddb` (function) `core/http.py:143` `def nvddb(content)` -- Parse NVD JSON vulnerability feed.
- `scrape_news` (function) `core/http.py:174` `def scrape_news()` -- Scrape Hacker News top stories.
- `display_news` (function) `core/http.py:198` `def display_news(titles, links, scores)` -- Display scraped news in the console.
- `inject_payloads` (function) `core/http.py:211` `def inject_payloads(urls, payload_url, request_timeout)` -- Attempt to inject a payload URL into a list of target URLs.

## core/llm_budget.py
Imported by: `cli/commands/ai.py`, `modules/llm_factory.py`, `skills/lazyown_mcp.py`, `tests/test_llm_budget.py`
- `LLMBackendLike.generate` (method) `core/llm_budget.py:61` `def generate(self, prompt)`
- `LLMBackendLike.stream_generate` (method) `core/llm_budget.py:63` `def stream_generate(self, prompt)`
- `LLMBackendLike.complete` (method) `core/llm_budget.py:65` `def complete(self, system, user, max_tokens, temperature)`
- `ModelPrice.from_mapping` (method) `core/llm_budget.py:81` `def from_mapping(cls, data)` -- Build a ModelPrice from a JSON friendly mapping.
- `BudgetLedger.record` (method) `core/llm_budget.py:232` `def record(self, entry)` -- Append a charge to the ledger and persist the new state.
- `BudgetLedger.spent_today` (method) `core/llm_budget.py:251` `def spent_today(self)` -- Return the dollar amount the ledger charged for the current day.
- `BudgetLedger.calls_today` (method) `core/llm_budget.py:256` `def calls_today(self)` -- Return the number of calls the ledger recorded for the current day.
- `BudgetLedger.reset` (method) `core/llm_budget.py:261` `def reset(self)` -- Clear the ledger for the current day and persist the empty state.
- `TokenEstimator.__init__` (method) `core/llm_budget.py:278` `def __init__(self, encoding_name)`
- `TokenEstimator.count` (method) `core/llm_budget.py:292` `def count(self, text)` -- Return the number of tokens the input text contains.
- `BudgetGuard.__init__` (method) `core/llm_budget.py:319` `def __init__(self, config, estimator, ledger)`
- `BudgetGuard.price_for` (method) `core/llm_budget.py:329` `def price_for(self, model)` -- Return the price the guard applies to a model identifier.
- `BudgetGuard.estimate_cost` (method) `core/llm_budget.py:343` `def estimate_cost(self, model, input_tokens, output_tokens)` -- Return the dollar cost the guard would charge for a call.
- `BudgetGuard.estimate_and_check` (method) `core/llm_budget.py:356` `def estimate_and_check(self, prompt, model, output_tokens)` -- Check the budget and record a charge when the call fits.
- `BudgetedBackend.__init__` (method) `core/llm_budget.py:417` `def __init__(self, inner, guard, model)`
- `BudgetedBackend.generate` (method) `core/llm_budget.py:422` `def generate(self, prompt)` -- Forward a non streaming call and record a charge.
- `BudgetedBackend.stream_generate` (method) `core/llm_budget.py:430` `def stream_generate(self, prompt)` -- Forward a streaming call.
- `BudgetedBackend.complete` (method) `core/llm_budget.py:435` `def complete(self, system, user, max_tokens, temperature)` -- Forward a role aware call.
- `BudgetedBackend.default_model_prices` (method) `core/llm_budget.py:442` `def default_model_prices()` -- Return the default price table the guard ships with.
- `BudgetedBackend.default_sessions_dir` (method) `core/llm_budget.py:461` `def default_sessions_dir()` -- Return the directory the ledger writes to by default.
- `BudgetedBackend.load_budget_config` (method) `core/llm_budget.py:552` `def load_budget_config(payload, sessions_dir)` -- Build a BudgetConfig from a payload mapping.
- `BudgetedBackend.read_budget_status` (method) `core/llm_budget.py:585` `def read_budget_status(payload, sessions_dir)` -- Return a structured snapshot of the current budget.
- `BudgetedBackend.format_budget_status` (method) `core/llm_budget.py:616` `def format_budget_status(config, ledger)` -- Render the budget status as a human readable block.
- `BudgetedBackend.wrap_backend_with_budget` (method) `core/llm_budget.py:657` `def wrap_backend_with_budget(backend, config, estimator, model, ledger)` -- Wrap a concrete backend with a budgeted proxy.

## core/logging.py
Imported by: `cli/auto_crypto.py`, `cli/chain_mode.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `cli/session_resumer.py`, `cli/tips_engine.py`, `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazygptcli.py`, `contrib/legacy/lazygptcli_unified.py`, `contrib/legacy/lazyhoneypot.py`, `contrib/legacy/lazyopenssh77enum2.py`, `contrib/legacy/lazyphishingai.py`, `contrib/legacy/lazysearch_bot.py`, `contrib/legacy/lazysmbrelay.py`, `contrib/legacy/lazyssh.py`, `core/config.py`, `core/credential_vault.py`, `core/executor.py`, `core/hardening.py`, `core/safe_exec.py`, `core/scheduler.py`, `core/security.py`, `lazy_sentinel4.py`, `lazyc2.py`, `lazyc2/blueprints/api.py`, `lazyc2/blueprints/api_v1.py`, `lazyc2/blueprints/beacon.py`, `lazyc2/blueprints/phishing.py`, `lazyc2/extensions/short_urls.py`, `lazyc2/extensions/storage.py`, `lazygui/app.py`, `lazygui/config/c2_credentials.py`, `lazygui/config/settings.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/agent_tool.py`, `modules/ai_model.py`, `modules/atomic_enricher.py`, `modules/auto_purple.py`, `modules/beacon_config_builder.py`, `modules/beacon_history.py`, `modules/bof_registry.py`, `modules/c2_profile.py`, `modules/c2_profile_engine.py`, `modules/collab_bp.py`, `modules/command_executor.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/config_store.py`, `modules/credential_reuse.py`, `modules/cve_matcher.py`, `modules/db.py`, `modules/detection_feed.py`, `modules/detection_oracle.py`, `modules/engagement_hooks.py`, `modules/estorides_importer.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/hash_cracker.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/icmp_server.py`, `modules/integrations/misp_export.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/integrations/searchsploit.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_rbac.py`, `modules/lazyownerweb.py`, `modules/lesson_ingestor.py`, `modules/lilsplunky.py`, `modules/llm_adapter.py`, `modules/llm_client.py`, `modules/logging_config.py`, `modules/mcp_agent_bridge.py`, `modules/metrics.py`, `modules/module_registry.py`, `modules/moe_router.py`, `modules/obs_parser.py`, `modules/operation.py`, `modules/operator_profiles.py`, `modules/opsec_scorer.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/reactive_engine.py`, `modules/rl_trainer.py`, `modules/session_rag.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`, `modules/state_manager.py`, `modules/sudo_tiocsti.py`, `modules/threat_model.py`, `modules/toposwarm_bridge.py`, `modules/ttp_coverage.py`, `modules/unified_bridge.py`, `modules/unified_dashboard.py`, `modules/vuln_agent.py`, `modules/vulnbot.py`, `modules/world_model.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/autonomous_replay.py`, `skills/hive_mind.py`, `skills/lazyown_automapper.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`, `tests/test_structured_logging.py`
- `_JsonLineFormatter.__init__` (method) `core/logging.py:74` `def __init__(self, redacted_fields)`
- `_JsonLineFormatter.format` (method) `core/logging.py:78` `def format(self, record)`
- `_ConsoleFormatter.format` (method) `core/logging.py:132` `def format(self, record)`
- `StructuredLogger.makeRecord` (method) `core/logging.py:148` `def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)`
- `StructuredLogger.get_logger` (method) `core/logging.py:231` `def get_logger(name)` -- Return a cached :class:`StructuredLogger` for *name*.
- `StructuredLogger.install_json_handler` (method) `core/logging.py:251` `def install_json_handler(name, config)` -- Install a JSON-lines file handler on *name*, preserving existing handlers.
- `StructuredLogger.reconfigure` (method) `core/logging.py:300` `def reconfigure(config)` -- Replace the cached configuration globally.

## core/network.py
Depends on: `core/console.py`
Imported by: `core/__init__.py`
- `parse_ip_mac` (function) `core/network.py:18` `def parse_ip_mac(input_string)` -- Extract IP and MAC from a formatted string.
- `create_arp_packet` (function) `core/network.py:33` `def create_arp_packet(src_mac, src_ip, dst_ip, dst_mac)` -- Build a raw ARP request/reply packet.
- `send_packet` (function) `core/network.py:66` `def send_packet(packet, iface)` -- Send a raw packet on a given network interface.
- `parse_proc_net_file` (function) `core/network.py:78` `def parse_proc_net_file(file_path)` -- Parse a ``/proc/net/*`` file and extract (ip, port) pairs.
- `get_open_ports` (function) `core/network.py:105` `def get_open_ports()` -- Discover listening TCP ports from ``/proc/net/tcp`` and ``tcp6``.
- `is_port_in_use` (function) `core/network.py:120` `def is_port_in_use(port, host)` -- Check whether a TCP port is already bound.
- `get_banner` (function) `core/network.py:134` `def get_banner(ip, port)` -- Grab a TCP banner from the given host and port.
- `get_network_info` (function) `core/network.py:154` `def get_network_info()` -- Collect local network information.

## core/parsers.py
Depends on: `core/console.py`
Imported by: `cli/banner_config.py`, `core/__init__.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `telegram_hermes.py`, `utils.py`
- `strip_ansi` (function) `core/parsers.py:21` `def strip_ansi(text)` -- Remove ANSI escape sequences and readline markers from a string.
- `clean_output` (function) `core/parsers.py:40` `def clean_output(output)` -- Remove ANSI escape sequences from a string.
- `clean_html` (function) `core/parsers.py:52` `def clean_html(html_string)` -- Strip HTML tags from a string.
- `clean_url` (function) `core/parsers.py:64` `def clean_url(host)` -- Normalize a URL by stripping protocol and trailing slash.
- `htmlify` (function) `core/parsers.py:79` `def htmlify(data)` -- Encode text as HTML entities.
- `de_htmlify` (function) `core/parsers.py:91` `def de_htmlify(data)` -- Decode HTML entities back to plain text.
- `is_exist` (function) `core/parsers.py:105` `def is_exist(file)` -- Check if a file exists.
- `get_xml` (function) `core/parsers.py:120` `def get_xml(directory)` -- Find all XML files in a directory.
- `get_domain_from_xml` (function) `core/parsers.py:136` `def get_domain_from_xml(xml_file)` -- Extract the hostname from an Nmap XML file.
- `extract_banners` (function) `core/parsers.py:160` `def extract_banners(xml_file)` -- Extract service banners from an Nmap XML file.
- `parse_nmap_csv` (function) `core/parsers.py:190` `def parse_nmap_csv(csv_path)` -- Parse an Nmap CSV output file.
- `manual_yaml_extraction` (function) `core/parsers.py:210` `def manual_yaml_extraction(content)` -- Fallback YAML parser for malformed content.
- `fix_common_yaml_issues` (function) `core/parsers.py:231` `def fix_common_yaml_issues(yaml_content)` -- Fix common YAML formatting issues.
- `aggressive_yaml_fix` (function) `core/parsers.py:256` `def aggressive_yaml_fix(yaml_content)` -- Aggressively fix YAML by normalizing indentation.
- `create_synthetic_yaml` (function) `core/parsers.py:282` `def create_synthetic_yaml(nmap_services)` -- Build a YAML string from parsed Nmap service data.
- `parse_yaml_response` (function) `core/parsers.py:305` `def parse_yaml_response(content)` -- Parse a YAML string, trying multiple strategies.
- `load_adversary` (function) `core/parsers.py:324` `def load_adversary()` -- Load adversary profile from ``adversary.json``.
- `load_knowledge_base` (function) `core/parsers.py:337` `def load_knowledge_base(knowledge_file)` -- Load the knowledge base JSON file.
- `load_user_aliases` (function) `core/parsers.py:353` `def load_user_aliases()` -- Load user-defined aliases from ``user_aliases.json``.
- `list_binaries` (function) `core/parsers.py:367` `def list_binaries(directory)` -- List files in the sessions directory.
- `select_binary` (function) `core/parsers.py:382` `def select_binary(binaries)` -- Interactive binary selector (fallback).

## core/payload_schema.py
Depends on: `cli/commands/enum.py`, `modules/llm_factory.py`
Imported by: `cli/assign.py`, `cli/wizard.py`, `core/__init__.py`, `core/config.py`, `scripts/devtools/core_smoke.py`, `skills/lazyown_mcp.py`, `tests/test_core_config.py`, `tests/test_infra_disposable.py`, `tests/test_payload_schema.py`
- `ValidationIssue.field_for` (method) `core/payload_schema.py:1225` `def field_for(key)` -- Return the :class:`FieldSpec` for ``key`` or ``None`` if it is unknown.
- `ValidationIssue.coerce_value` (method) `core/payload_schema.py:1230` `def coerce_value(key, raw)` -- Return ``raw`` coerced to the canonical type declared for ``key``.
- `ValidationIssue.validate_value` (method) `core/payload_schema.py:1253` `def validate_value(key, value)` -- Validate ``value`` against the schema entry for ``key``.
- `ValidationIssue.validate_payload` (method) `core/payload_schema.py:1327` `def validate_payload(payload)` -- Validate an entire payload dictionary and return all issues found.
- `ValidationIssue.format_issue` (method) `core/payload_schema.py:1362` `def format_issue(issue)` -- Render a :class:`ValidationIssue` as a single human-readable line.
- `ValidationIssue.default_payload` (method) `core/payload_schema.py:1380` `def default_payload()` -- Return a freshly built payload dict populated from the schema defaults.
- `ValidationIssue.categories` (method) `core/payload_schema.py:1388` `def categories()` -- Return schema entries grouped by :attr:`FieldSpec.category`.

## core/process.py
Depends on: `core/console.py`, `core/hardening.py`, `core/safe_exec.py`, `core/safe_subprocess.py`, `core/validators.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/mobile_macos.py`, `core/__init__.py`, `modules/auto_purple.py`, `static/js/particles.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `tests/test_shell_semantics.py`, `utils.py`
- `check_go_tool_installed` (function) `core/process.py:34` `def check_go_tool_installed(tool_name)` -- Check if a Go tool binary is installed and runnable.
- `is_binary_present` (function) `core/process.py:54` `def is_binary_present(binary_name)` -- Check whether binary is on ``PATH``.
- `handle_multiple_rhosts` (function) `core/process.py:68` `def handle_multiple_rhosts(func)` -- Decorator that iterates over a list of remote hosts.
- `wrapper` (function) `core/process.py:82` `def wrapper(self)`
- `check_sudo` (function) `core/process.py:97` `def check_sudo()` -- Re-launch the script with ``sudo`` if not already root.
- `run` (function) `core/process.py:108` `def run(command)` -- Execute a shell command via ``SafeRunner``.
- `is_package_installed` (function) `core/process.py:143` `def is_package_installed(package_name)` -- Check whether a Python package is importable.
- `run_command` (function) `core/process.py:183` `def run_command(command, timeout)` -- Run a command, streaming output in real time.
- `ensure_tmux_session` (function) `core/process.py:253` `def ensure_tmux_session(session_name)` -- Create a tmux session if it does not already exist.
- `activate_server` (function) `core/process.py:271` `def activate_server(httpd, url, lhost)` -- Start an HTTP server and print the serving URL.

## core/profiles.py
Imported by: `cli/doctor.py`, `cli/wizard.py`, `tests/test_profiles.py`
- `active_profile` (function) `core/profiles.py:37` `def active_profile()` -- Return the selected runtime profile.
- `is_light` (function) `core/profiles.py:56` `def is_light()` -- Return ``True`` when the light profile is selected.
- `specs_for_profile` (function) `core/profiles.py:61` `def specs_for_profile(specs)` -- Filter dependency specs down to the ones the active profile needs.

## core/prompt.py
Depends on: `core/config.py`
Imported by: `contrib/legacy/lazybinenc.py`, `key.py`, `static/js/quill-2.0.3.js`
- `get_git_info` (function) `core/prompt.py:35` `def get_git_info()` -- Return current git branch and dirty-status for the prompt.
- `get_venv_info` (function) `core/prompt.py:60` `def get_venv_info()` -- Return the active virtualenv name, or empty string if none.
- `get_kernel` (function) `core/prompt.py:68` `def get_kernel()` -- Return the running kernel version (short form).
- `get_terminal_size` (function) `core/prompt.py:78` `def get_terminal_size()` -- Return ``(width, height)`` of the terminal, defaulting to 80x24.
- `get_local_ips` (function) `core/prompt.py:87` `def get_local_ips()` -- Return a comma-separated string of non-loopback IPv4 addresses.
- `copy2clip` (function) `core/prompt.py:109` `def copy2clip(text)` -- Copy ``text`` to the system clipboard via xclip.
- `getprompt` (function) `core/prompt.py:127` `def getprompt()` -- Build the coloured status line for the CLI header and C2 dashboard.

## core/protocols.py
Imported by: `tests/test_core.py`
- `Selector.suggest` (method) `core/protocols.py:27` `def suggest(self, target, phase, context)` -- Return ``{"command": str, "reasoning": str, "mitre": str}`` or ``None``.
- `LLMBackend.complete` (method) `core/protocols.py:40` `def complete(self, system, user, max_tokens, temperature)` -- Return the model completion as a string.
- `MemoryStore.put` (method) `core/protocols.py:54` `def put(self, key, value)`
- `MemoryStore.get` (method) `core/protocols.py:56` `def get(self, key, default)`
- `MemoryStore.search` (method) `core/protocols.py:58` `def search(self, query, k)`
- `BridgeCatalog.filter` (method) `core/protocols.py:65` `def filter(self, phase, os_id)` -- Return command entries matching ``phase`` and ``os_id``.
- `OutcomeEvaluator.evaluate` (method) `core/protocols.py:73` `def evaluate(self, command, output, target, phase)` -- Return a reward in ``[0.0, 1.0]``.

## core/safe_exec.py
Depends on: `core/logging.py`
Imported by: `cli/banner_config.py`, `cli/commands/misc_migrated.py`, `cli/commands/pwn.py`, `cli/commands/shellsys.py`, `core/process.py`, `core/safe_subprocess.py`, `lazyc2/blueprints/api_v1.py`, `lazyown.py`, `modules/autonomous_exploit_engine.py`, `modules/conditional_hooks.py`, `modules/dns_beacon.py`, `modules/playbook_engine.py`, `modules/resource_script.py`, `tests/test_security_hardening_v4.py`, `tests/test_shell_semantics.py`
- `UrlValidationError.needs_shell` (method) `core/safe_exec.py:52` `def needs_shell(command)` -- Return True when a command string needs a shell to be interpreted.
- `UrlValidationError.safe_system` (method) `core/safe_exec.py:69` `def safe_system(command)` -- Execute a fixed command string through the shell safely.
- `UrlValidationError.safe_run_argv` (method) `core/safe_exec.py:106` `def safe_run_argv(argv)` -- Execute a command via subprocess without shell interpretation.
- `UrlValidationError.safe_run_shell` (method) `core/safe_exec.py:146` `def safe_run_shell(command)` -- Execute a command through the shell, gated by policy.
- `UrlValidationError.safe_clear_screen` (method) `core/safe_exec.py:192` `def safe_clear_screen()` -- Clear the terminal screen without using os.system.
- `UrlValidationError.validate_url` (method) `core/safe_exec.py:207` `def validate_url(url)` -- Validate a URL string, rejecting shell metacharacters.
- `UrlValidationError.safe_git_clone` (method) `core/safe_exec.py:234` `def safe_git_clone(repo_url, target_dir)` -- Clone a git repository safely using subprocess list-form.
- `UrlValidationError.safe_ip_show` (method) `core/safe_exec.py:268` `def safe_ip_show(interface)` -- Parse IP addresses from ``ip show`` output in Python.
- `UrlValidationError.safe_find_tool` (method) `core/safe_exec.py:305` `def safe_find_tool(name)` -- Find a tool on PATH using shutil.which.
- `UrlValidationError.safe_file_read` (method) `core/safe_exec.py:321` `def safe_file_read(path)` -- Read a file safely with a size limit.

## core/safe_subprocess.py
Depends on: `core/hardening.py`, `core/safe_exec.py`
Imported by: `core/process.py`, `tests/test_safe_subprocess.py`, `tests/test_safe_subprocess_behavior.py`, `tests/test_security_hardening.py`, `tests/test_shell_semantics.py`, `utils.py`
- `SafeRunner.__init__` (method) `core/safe_subprocess.py:70` `def __init__(self, audit_log_path)`
- `SafeRunner.run` (method) `core/safe_subprocess.py:73` `def run(self, argv)` -- Execute ``argv`` without invoking a shell.
- `SafeRunner.run_shell` (method) `core/safe_subprocess.py:105` `def run_shell(self, command)` -- Execute ``command`` through the system shell, gated by policy.

## core/scheduler.py
Depends on: `core/logging.py`
- `TaskScheduler.__init__` (method) `core/scheduler.py:61` `def __init__(self)`
- `TaskScheduler.instance` (method) `core/scheduler.py:73` `def instance(cls)` -- Return the singleton ``TaskScheduler`` instance.
- `TaskScheduler.start` (method) `core/scheduler.py:81` `def start(self)` -- Start the scheduler background thread.
- `TaskScheduler.stop` (method) `core/scheduler.py:100` `def stop(self)` -- Stop the scheduler and cancel all pending tasks.
- `TaskScheduler.schedule_task` (method) `core/scheduler.py:123` `def schedule_task(self, name, interval_seconds, func)` -- Register a recurring task to run every ``interval_seconds``.
- `TaskScheduler.schedule_once` (method) `core/scheduler.py:157` `def schedule_once(self, name, delay_seconds, func)` -- Register a one-shot task to run after ``delay_seconds``.
- `TaskScheduler.cancel_task` (method) `core/scheduler.py:192` `def cancel_task(self, name)` -- Cancel a scheduled task by name.
- `TaskScheduler.list_tasks` (method) `core/scheduler.py:205` `def list_tasks(self)` -- Return metadata for all registered tasks.
- `TaskScheduler.get_scheduler` (method) `core/scheduler.py:285` `def get_scheduler()` -- Return the singleton ``TaskScheduler`` instance.

## core/security.py
Depends on: `core/logging.py`
- `anti_debug` (function) `core/security.py:18` `def anti_debug()` -- Check for debugger attachment and exit if found.
- `generate_certificates` (function) `core/security.py:58` `def generate_certificates(output_dir)` -- Generate a self-signed CA certificate and key pair.

## core/text_utils.py
Imported by: `cli/autosuggest.py`, `cli/graph_overlay.py`, `cli/palette_command.py`, `cli/palette_overlay.py`, `cli/reactive_hints.py`, `cli/reasoning_stream.py`, `cli/tips_engine.py`, `cli/toast_bus.py`
- `truncate_text` (function) `core/text_utils.py:10` `def truncate_text(value, max_len, marker)` -- Truncate value to max_len using marker.

## core/validators.py
Depends on: `core/console.py`
Imported by: `cli/commands/enum.py`, `cli/commands/mobile_macos.py`, `cli/commands/pwn.py`, `core/__init__.py`, `core/process.py`, `modules/c2_builder.py`, `tests/test_core.py`, `tests/test_input_fuzz.py`, `utils.py`
- `check_rhost` (function) `core/validators.py:55` `def check_rhost(rhost)` -- Return ``True`` if ``rhost`` is set, otherwise print an error and return ``False``.
- `check_lhost` (function) `core/validators.py:69` `def check_lhost(lhost)` -- Return ``True`` if ``lhost`` is set, otherwise print an error and return ``False``.
- `check_lport` (function) `core/validators.py:83` `def check_lport(lport)` -- Return ``True`` if ``lport`` is set, otherwise print an error and return ``False``.
- `check_port` (function) `core/validators.py:93` `def check_port(port, name)` -- Return ``True`` if ``port`` is a valid TCP/UDP port (1-65535).

## deploy/range/ad-mini/traffic-gen.py
- `main` (function) `deploy/range/ad-mini/traffic-gen.py:35` `def main()` -- Loop forever emitting fake background traffic.

## discord_c2.py
Depends on: `core/parsers.py`, `lazyown.py`, `modules/llm_adapter.py`
- `SecureSessionManager.__init__` (method) `discord_c2.py:28` `def __init__(self)`
- `SecureSessionManager.register_failed_attempt` (method) `discord_c2.py:33` `def register_failed_attempt(self, user_id)`
- `SecureSessionManager.check_lockout` (method) `discord_c2.py:40` `def check_lockout(self, user_id)`
- `SecureSessionManager.check_rate_limit` (method) `discord_c2.py:49` `def check_rate_limit(self, user_id)`
- `SecureSessionManager.create_session` (method) `discord_c2.py:62` `def create_session(self, user_id, client_id)`
- `SecureSessionManager.validate_session` (method) `discord_c2.py:70` `def validate_session(self, user_id)`
- `Config.__init__` (method) `discord_c2.py:85` `def __init__(self, config_dict)`
- `Config.load_payload` (method) `discord_c2.py:93` `def load_payload()`
- `Config.on_ready` (method) `discord_c2.py:99` `def on_ready()`
- `Config.start` (method) `discord_c2.py:103` `def start(ctx)`
- `Config.exce_cmd` (method) `discord_c2.py:126` `def exce_cmd(ctx)`
- `Config.add_cli` (method) `discord_c2.py:201` `def add_cli(ctx, new_client_id)`
- `Config.handle_file` (method) `discord_c2.py:210` `def handle_file(ctx)`
- `Config.download_c2` (method) `discord_c2.py:238` `def download_c2(ctx, client_id, file_name)`
- `Config.send_connected_clients` (method) `discord_c2.py:248` `def send_connected_clients(ctx)`
- `Config.clients` (method) `discord_c2.py:264` `def clients(ctx)`
- `Config.addcli` (method) `discord_c2.py:268` `def addcli(ctx, new_client_id)`
- `Config.c2` (method) `discord_c2.py:272` `def c2(ctx)`

## external/install_external.sh
- `ctrl_c` (function) `external/install_external.sh:13`
- `download` (function) `external/install_external.sh:18`

## fast_run_as_r00t.sh
- `log` (function) `fast_run_as_r00t.sh:55` -- ── Pretty-print helpers ──────────────────────────────────────────────────────
- `spin` (function) `fast_run_as_r00t.sh:56`
- `err_box` (function) `fast_run_as_r00t.sh:57`
- `ensure_gum` (function) `fast_run_as_r00t.sh:63` -- ── Ensure gum is installed ───────────────────────────────────────────────────
- `check_deps` (function) `fast_run_as_r00t.sh:74` -- ── Dependency check ──────────────────────────────────────────────────────────
- `check_sudo` (function) `fast_run_as_r00t.sh:83` -- ── Re-exec as root if needed ─────────────────────────────────────────────────
- `parse_args` (function) `fast_run_as_r00t.sh:92` -- ── CLI argument parsing ──────────────────────────────────────────────────────
- `t_send` (function) `fast_run_as_r00t.sh:110` -- Send one or more commands to the active tmux pane
- `t_lazyown` (function) `fast_run_as_r00t.sh:117` -- Open a new pane (split v or h), start LazyOwn shell with optional run flags, then send any follow-up commands once...
- `t_priv_user` (function) `fast_run_as_r00t.sh:130` -- Open a new pane running a command as unprivileged user 1000 (with venv).
- `start_chown_watcher` (function) `fast_run_as_r00t.sh:141` -- ── Background chown watcher ────────────────────────────────────────────────── Re-chowns the project tree to the...

## install.sh
- `usage` (function) `install.sh:49`
- `log` (function) `install.sh:88`
- `spin_run` (function) `install.sh:98`
- `ensure_gum` (function) `install.sh:128`
- `install_system_packages` (function) `install.sh:139`
- `install_external_tools` (function) `install.sh:150`
- `install_python_environment` (function) `install.sh:165`
- `install_ollama` (function) `install.sh:206`
- `install_external_storage` (function) `install.sh:218`
- `install_lazyownbt` (function) `install.sh:231`
- `download_file` (function) `install.sh:251`
- `install_encoder_module` (function) `install.sh:263`
- `generate_certificates` (function) `install.sh:274`
- `seed_payload_config` (function) `install.sh:281`
- `verify_installation` (function) `install.sh:294`
- `main` (function) `install.sh:310`

## key.py
Depends on: `core/console.py`, `core/prompt.py`
- `main` (function) `key.py:9` `def main()`

## lazy_sentinel4.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `sanitize_content` (function) `lazy_sentinel4.py:46` `def sanitize_content(text)` -- Sanitize text to ensure it's safe for rendering.
- `RAGManager.__init__` (method) `lazy_sentinel4.py:59` `def __init__(self, model_name, cache_size)`
- `RAGManager.initialize_cache_table` (method) `lazy_sentinel4.py:71` `def initialize_cache_table(self)`
- `RAGManager.get_cache_key` (method) `lazy_sentinel4.py:83` `def get_cache_key(self, content)`
- `RAGManager.load_existing_vectorstore` (method) `lazy_sentinel4.py:86` `def load_existing_vectorstore(self)`
- `RAGManager.ollama_llm` (method) `lazy_sentinel4.py:99` `def ollama_llm(self, question, context)`
- `RAGManager.process_file_to_rag` (method) `lazy_sentinel4.py:113` `def process_file_to_rag(self, file_path)`
- `RAGManager.query_rag` (method) `lazy_sentinel4.py:160` `def query_rag(self, question)`
- `RAGManager.invalidate_cache` (method) `lazy_sentinel4.py:187` `def invalidate_cache(self, file_path)`
- `RAGManager.get_knowledge_base_stats` (method) `lazy_sentinel4.py:203` `def get_knowledge_base_stats(self)`
- `Database.__init__` (method) `lazy_sentinel4.py:226` `def __init__(self, db_path)`
- `Database.initialize` (method) `lazy_sentinel4.py:230` `def initialize(self)`
- `Database.execute` (method) `lazy_sentinel4.py:254` `def execute(self, query, params)`
- `Database.insert` (method) `lazy_sentinel4.py:266` `def insert(self, query, params)`
- `Alert.__init__` (method) `lazy_sentinel4.py:284` `def __init__(self, alert_type, details, severity)`
- `Alert.to_dict` (method) `lazy_sentinel4.py:290` `def to_dict(self)`
- `Alert.save_to_db` (method) `lazy_sentinel4.py:298` `def save_to_db(self, db)`
- `LazySentinelHandler.__init__` (method) `lazy_sentinel4.py:312` `def __init__(self, lazysentinel)`
- `LazySentinelHandler.is_text_file` (method) `lazy_sentinel4.py:315` `def is_text_file(self, file_path)`
- `LazySentinelHandler.on_created` (method) `lazy_sentinel4.py:325` `def on_created(self, event)`
- `LazySentinelHandler.on_modified` (method) `lazy_sentinel4.py:337` `def on_modified(self, event)`
- `LazySentinel.__init__` (method) `lazy_sentinel4.py:349` `def __init__(self, app, popup_queue, watch_dir, excluded_files, min_file_size)`
- `LazySentinel.chunk_text` (method) `lazy_sentinel4.py:369` `def chunk_text(self, text, chunk_size)`
- `LazySentinel.select_relevant_chunk` (method) `lazy_sentinel4.py:372` `def select_relevant_chunk(self, file_content, chunks)`
- `LazySentinel.parse_deepseek_response` (method) `lazy_sentinel4.py:386` `def parse_deepseek_response(self, response_text)`
- `LazySentinel.show_popup` (method) `lazy_sentinel4.py:410` `def show_popup(self, file_name, relevant_info, commands, details)`
- `LazySentinel.process_file` (method) `lazy_sentinel4.py:428` `def process_file(self, file_path)`
- `LazySentinel.stop` (method) `lazy_sentinel4.py:559` `def stop(self)`
- `App.__init__` (method) `lazy_sentinel4.py:565` `def __init__(self)`
- `App.display_toastr` (method) `lazy_sentinel4.py:579` `def display_toastr(self, file_name, relevant_info, commands, details, severity, duration)` -- Display a toastr-like notification for file processing alerts.
- `App.postcmd` (method) `lazy_sentinel4.py:605` `def postcmd(self, stop, line)` -- Check the popup queue after each command and display toastr notifications.
- `App.do_quit` (method) `lazy_sentinel4.py:629` `def do_quit(self, arg)`
- `App.do_debug` (method) `lazy_sentinel4.py:633` `def do_debug(self, arg)`
- `App.do_rag_query` (method) `lazy_sentinel4.py:640` `def do_rag_query(self, arg)`
- `App.do_rag_add` (method) `lazy_sentinel4.py:648` `def do_rag_add(self, arg)`
- `App.do_rag_status` (method) `lazy_sentinel4.py:663` `def do_rag_status(self, arg)`
- `App.do_rag_toggle` (method) `lazy_sentinel4.py:670` `def do_rag_toggle(self, arg)`
- `App.do_rag_bulk_add` (method) `lazy_sentinel4.py:675` `def do_rag_bulk_add(self, arg)`
- `App.do_rag_search` (method) `lazy_sentinel4.py:694` `def do_rag_search(self, arg)`
- `App.complete_rag_add` (method) `lazy_sentinel4.py:715` `def complete_rag_add(self, text, line, begidx, endidx)`
- `App.complete_rag_bulk_add` (method) `lazy_sentinel4.py:722` `def complete_rag_bulk_add(self, text, line, begidx, endidx)`


Next: [API_p7.md](API_p7.md)
