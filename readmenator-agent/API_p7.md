# API (page 7 of 28)
Previous: [API_p6.md](API_p6.md)

## core/llm_budget.py
Imported by: `cli/commands/ai.py`, `modules/llm_factory.py`, `skills/mcp_tools/get_llm_budget.py`, `tests/test_llm_budget.py`
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
- `default_model_prices` (function) `core/llm_budget.py:442` `def default_model_prices()` -- Return the default price table the guard ships with.
- `default_sessions_dir` (function) `core/llm_budget.py:461` `def default_sessions_dir()` -- Return the directory the ledger writes to by default.
- `load_budget_config` (function) `core/llm_budget.py:552` `def load_budget_config(payload, sessions_dir)` -- Build a BudgetConfig from a payload mapping.
- `read_budget_status` (function) `core/llm_budget.py:585` `def read_budget_status(payload, sessions_dir)` -- Return a structured snapshot of the current budget.
- `format_budget_status` (function) `core/llm_budget.py:616` `def format_budget_status(config, ledger)` -- Render the budget status as a human readable block.
- `wrap_backend_with_budget` (function) `core/llm_budget.py:657` `def wrap_backend_with_budget(backend, config, estimator, model, ledger)` -- Wrap a concrete backend with a budgeted proxy.

## core/llm_key_pool.py
Imported by: `modules/llm_factory.py`, `tests/test_llm_key_pool.py`
- `KeyPool.__init__` (method) `core/llm_key_pool.py:76` `def __init__(self, cooldown_sec)` -- Initialize an empty pool.
- `KeyPool.set_keys` (method) `core/llm_key_pool.py:88` `def set_keys(self, backend, keys)` -- Replace the key list for one backend.
- `KeyPool.has_pool` (method) `core/llm_key_pool.py:107` `def has_pool(self, backend)` -- Return True when more than one key is configured for the backend.
- `KeyPool.size` (method) `core/llm_key_pool.py:112` `def size(self, backend)` -- Return the number of keys configured for the backend.
- `KeyPool.next_key` (method) `core/llm_key_pool.py:117` `def next_key(self, backend, now)` -- Return the next usable key for a backend, advancing the cursor.
- `KeyPool.mark_exhausted` (method) `core/llm_key_pool.py:149` `def mark_exhausted(self, backend, key, now)` -- Park a key for the cooldown window after an explicit quota error.
- `KeyPool.available` (method) `core/llm_key_pool.py:163` `def available(self, backend, now)` -- Return how many keys are not currently cooling down.
- `KeyPool.reset` (method) `core/llm_key_pool.py:171` `def reset(self)` -- Clear every backend's keys, cursors and cooldowns.
- `build_from_config` (function) `core/llm_key_pool.py:208` `def build_from_config(config, pool)` -- Build or refresh a :class:`KeyPool` from a payload-derived mapping.
- `get_key_pool` (function) `core/llm_key_pool.py:238` `def get_key_pool()` -- Return the process-wide key pool singleton.
- `refresh_from_config` (function) `core/llm_key_pool.py:243` `def refresh_from_config(config)` -- Refresh and return the global pool from a payload-derived mapping.
- `resolve_pooled_key` (function) `core/llm_key_pool.py:249` `def resolve_pooled_key(backend, config, fallback)` -- Return the next pooled key for a backend, or ``fallback`` when no pool.
- `note_quota_error` (function) `core/llm_key_pool.py:274` `def note_quota_error(backend, key)` -- Park a key on the global pool after an explicit provider quota error.

## core/logging.py
Imported by: `cli/auto_crypto.py`, `cli/chain_mode.py`, `cli/reactive_hints.py`, `cli/recommendation_signals.py`, `cli/session_resumer.py`, `cli/tips_engine.py`, `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazygptcli.py`, `contrib/legacy/lazygptcli_unified.py`, `contrib/legacy/lazyhoneypot.py`, `contrib/legacy/lazyopenssh77enum2.py`, `contrib/legacy/lazyphishingai.py`, `contrib/legacy/lazysearch_bot.py`, `contrib/legacy/lazysmbrelay.py`, `contrib/legacy/lazyssh.py`, `core/config.py`, `core/credential_vault.py`, `core/executor.py`, `core/hardening.py`, `core/param_registry.py`, `core/safe_exec.py`, `core/scheduler.py`, `core/security.py`, `core/session_secrets.py`, `lazy_sentinel4.py`, `lazyc2.py`, `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/api.py`, `lazyc2/blueprints/api_v1.py`, `lazyc2/blueprints/auth.py`, `lazyc2/blueprints/beacon.py`, `lazyc2/blueprints/loops.py`, `lazyc2/blueprints/orchestrator.py`, `lazyc2/blueprints/phishing.py`, `lazyc2/extensions/short_urls.py`, `lazyc2/extensions/storage.py`, `lazyc2/security/cli_credentials.py`, `lazyc2/security/health.py`, `lazygui/app.py`, `lazygui/config/c2_credentials.py`, `lazygui/config/settings.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazyown.py`, `modules/addon_updater.py`, `modules/agent_runner.py`, `modules/ai_model.py`, `modules/atomic_cli.py`, `modules/atomic_enricher.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/auto_purple.py`, `modules/beacon_config_builder.py`, `modules/beacon_history.py`, `modules/beacon_recon.py`, `modules/bof_delivery.py`, `modules/bof_registry.py`, `modules/bsb_compat.py`, `modules/c2_agent.py`, `modules/c2_profile.py`, `modules/c2_profile_engine.py`, `modules/c2_surfaces.py`, `modules/chain_distill.py`, `modules/chain_facts.py`, `modules/chain_registry.py`, `modules/chain_runner.py`, `modules/collab_bp.py`, `modules/command_executor.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/config_store.py`, `modules/credential_reuse.py`, `modules/ctf_capture.py`, `modules/ctf_signalman.py`, `modules/cve_matcher.py`, `modules/db.py`, `modules/defense_stages.py`, `modules/detection_feed.py`, `modules/detection_oracle.py`, `modules/emulation_runner.py`, `modules/engagement_hooks.py`, `modules/estorides_importer.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/factsio.py`, `modules/golden_path.py`, `modules/gym_cleanup.py`, `modules/gym_matrix_runner.py`, `modules/gym_registry.py`, `modules/gym_winbox_runner.py`, `modules/harness.py`, `modules/hash_cracker.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/integrations/misp_export.py`, `modules/integrations/nuclei_bridge.py`, `modules/integrations/nuclei_parser.py`, `modules/integrations/searchsploit.py`, `modules/intelligence_engine.py`, `modules/killchain.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `modules/lazy_rbac.py`, `modules/lazyownerweb.py`, `modules/lesson_ingestor.py`, `modules/lilsplunky.py`, `modules/llm_adapter.py`, `modules/llm_client.py`, `modules/logging_config.py`, `modules/mcp_agent_bridge.py`, `modules/metasploitable_gym.py`, `modules/metrics.py`, `modules/module_registry.py`, `modules/moe_router.py`, `modules/obs_parser.py`, `modules/operation.py`, `modules/operator_profiles.py`, `modules/opsec_scorer.py`, `modules/orchestrator_config.py`, `modules/outcome_bus.py`, `modules/pipeline_engine.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/reactive_engine.py`, `modules/rl_trainer.py`, `modules/selection/registry.py`, `modules/session_rag.py`, `modules/sinks/findings.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`, `modules/state_manager.py`, `modules/sudo_tiocsti.py`, `modules/threat_model.py`, `modules/toposwarm_bridge.py`, `modules/trigger_policy.py`, `modules/ttp_coverage.py`, `modules/ttpscope_bridge.py`, `modules/unified_bridge.py`, `modules/unified_dashboard.py`, `modules/verb_catalog.py`, `modules/verb_manifest.py`, `modules/vulnbot.py`, `modules/winbox_gym.py`, `modules/world_model.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/autonomous_replay.py`, `skills/hive_mind.py`, `skills/lazyown_automapper.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_chain_match_determinism.py`, `tests/test_logging_config.py`, `tests/test_security_codeql_batch.py`, `tests/test_structured_logging.py`, `utils.py`
- `_JsonLineFormatter.__init__` (method) `core/logging.py:74` `def __init__(self, redacted_fields)`
- `_JsonLineFormatter.format` (method) `core/logging.py:78` `def format(self, record)`
- `_ConsoleFormatter.format` (method) `core/logging.py:132` `def format(self, record)`
- `StructuredLogger.makeRecord` (method) `core/logging.py:148` `def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)`
- `get_logger` (function) `core/logging.py:231` `def get_logger(name)` -- Return a cached :class:`StructuredLogger` for *name*.
- `install_json_handler` (function) `core/logging.py:251` `def install_json_handler(name, config)` -- Install a JSON-lines file handler on *name*, preserving existing handlers.
- `reconfigure` (function) `core/logging.py:300` `def reconfigure(config)` -- Replace the cached configuration globally.

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

## core/param_registry.py
Depends on: `core/logging.py`, `core/payload_schema.py`
Imported by: `cli/commands/params_ops.py`, `cli/lazy_orchestrator.py`, `core/payload_schema.py`, `lazyc2/addon_creator.py`, `lazyown.py`, `skills/mcp_tools/create_param.py`, `skills/mcp_tools/delete_param.py`, `skills/mcp_tools/list_params.py`, `tests/test_lazy_orchestrator.py`, `tests/test_param_registry.py`, `tests/test_php2shell_addon.py`
- `OperatorParam.as_entry` (method) `core/param_registry.py:135` `def as_entry(self)` -- Return the YAML mapping stored in ``params/operator.yaml``.
- `OperatorParam.to_spec` (method) `core/param_registry.py:144` `def to_spec(self)` -- Return the payload schema spec for this parameter.
- `registry_path` (function) `core/param_registry.py:160` `def registry_path(root)` -- Return the operator registry file path.
- `normalise_kind` (function) `core/param_registry.py:174` `def normalise_kind(kind)` -- Return the canonical kind name for a user-supplied kind.
- `effective_value` (function) `core/param_registry.py:189` `def effective_value(entry)` -- Return the value a parameter contributes to the shell params.
- `load_entries` (function) `core/param_registry.py:228` `def load_entries(root)` -- Return every operator-declared parameter.
- `list_params` (function) `core/param_registry.py:258` `def list_params(root, include_builtin, keyword)` -- Return the parameters visible to the operator.
- `create_param` (function) `core/param_registry.py:293` `def create_param(name, kind, default, description, category, root)` -- Create an operator parameter and persist it in the registry.
- `update_param` (function) `core/param_registry.py:343` `def update_param(name, default, description, kind, category, root)` -- Update an operator parameter in place.
- `delete_param` (function) `core/param_registry.py:389` `def delete_param(name, root)` -- Delete an operator parameter from the registry.
- `param_value` (function) `core/param_registry.py:413` `def param_value(name, root)` -- Return the effective value of an operator parameter.
- `operator_specs` (function) `core/param_registry.py:427` `def operator_specs(root)` -- Return the payload schema specs of the operator parameters.
- `apply_to_schema` (function) `core/param_registry.py:439` `def apply_to_schema(root)` -- Register the operator parameters in the payload schema.
- `sync_shell_params` (function) `core/param_registry.py:461` `def sync_shell_params(shell, root)` -- Push the operator parameters into a live shell parameter dict.

## core/parsers.py
Imported by: `cli/banner_config.py`, `core/__init__.py`, `discord_c2.py`, `lazyc2.py`, `modules/loop_audit.py`, `slack_c2_bot.py`, `telegram_c2.py`, `telegram_hermes.py`, `tests/test_single_implementation.py`, `utils.py`
- `strip_ansi` (function) `core/parsers.py:15` `def strip_ansi(text)` -- Remove ANSI escape sequences and readline markers from a string.

## core/payload_schema.py
Depends on: `cli/commands/enum.py`, `core/param_registry.py`, `modules/llm_factory.py`
Imported by: `cli/assign.py`, `cli/commands/params_ops.py`, `cli/commands/session_ops.py`, `cli/wizard.py`, `core/__init__.py`, `core/config.py`, `core/param_registry.py`, `scripts/devtools/core_smoke.py`, `skills/mcp_tools/set_config.py`, `tests/test_audit_remediation.py`, `tests/test_core_config.py`, `tests/test_core_defaults.py`, `tests/test_infra_disposable.py`, `tests/test_param_registry.py`, `tests/test_payload_schema.py`, `tests/test_php2shell_addon.py`, `tests/test_placeholder_coverage.py`
- `register_specs` (function) `core/payload_schema.py:2214` `def register_specs(specs)` -- Register (or replace) field specs at runtime.
- `unregister_specs` (function) `core/payload_schema.py:2237` `def unregister_specs(keys)` -- Remove runtime-registered specs from the schema.
- `field_for` (function) `core/payload_schema.py:2255` `def field_for(key)` -- Return the :class:`FieldSpec` for ``key`` or ``None`` if it is unknown.
- `coerce_value` (function) `core/payload_schema.py:2260` `def coerce_value(key, raw)` -- Return ``raw`` coerced to the canonical type declared for ``key``.
- `validate_value` (function) `core/payload_schema.py:2283` `def validate_value(key, value)` -- Validate ``value`` against the schema entry for ``key``.
- `validate_payload` (function) `core/payload_schema.py:2357` `def validate_payload(payload)` -- Validate an entire payload dictionary and return all issues found.
- `format_issue` (function) `core/payload_schema.py:2392` `def format_issue(issue)` -- Render a :class:`ValidationIssue` as a single human-readable line.
- `default_payload` (function) `core/payload_schema.py:2410` `def default_payload()` -- Return a freshly built payload dict populated from the schema defaults.
- `categories` (function) `core/payload_schema.py:2418` `def categories()` -- Return schema entries grouped by :attr:`FieldSpec.category`.

## core/process.py
Depends on: `core/console.py`, `core/hardening.py`, `core/safe_exec.py`, `core/safe_subprocess.py`, `core/validators.py`
Imported by: `cli/commands/lazyops.py`, `cli/commands/misc_migrated.py`, `cli/commands/mobile_macos.py`, `core/__init__.py`, `modules/auto_purple.py`, `modules/lazy_verify.py`, `static/js/particles.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `tests/test_lazy_runner.py`, `tests/test_shell_semantics.py`, `utils.py`
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
- `active_profile` (function) `core/profiles.py:40` `def active_profile()` -- Return the selected runtime profile.
- `is_light` (function) `core/profiles.py:59` `def is_light()` -- Return ``True`` when the light profile is selected.
- `specs_for_profile` (function) `core/profiles.py:64` `def specs_for_profile(specs)` -- Filter dependency specs down to the ones the active profile needs.

## core/prompt.py
Depends on: `core/config.py`
Imported by: `key.py`, `static/hexabot/hexabot-spinner.js`, `static/js/quill-2.0.3.js`
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

## core/reverse_shell_secret.py
Depends on: `core/hardening.py`
Imported by: `lazyc2.py`, `tests/test_security_alerts_fix.py`
- `seal_reverse_shell_password` (function) `core/reverse_shell_secret.py:24` `def seal_reverse_shell_password(plaintext)` -- Seal a fallback password for storage.
- `load_reverse_shell_password` (function) `core/reverse_shell_secret.py:41` `def load_reverse_shell_password(secret_path)` -- Load a persisted fallback password, unsealing vault values.
- `generate_reverse_shell_password` (function) `core/reverse_shell_secret.py:65` `def generate_reverse_shell_password()` -- Generate a fresh cryptographically random fallback password.
- `is_configured_password_valid` (function) `core/reverse_shell_secret.py:74` `def is_configured_password_valid(candidate, minimum_length)` -- Return True when an operator-configured password meets the floor.

## core/safe_console.py
Depends on: `core/console.py`
Imported by: `cli/autosuggest.py`, `cli/ops_commands.py`, `cli/tips_engine.py`, `modules/loop_progress.py`, `tests/test_safe_console.py`
- `supports_unicode` (function) `core/safe_console.py:33` `def supports_unicode()` -- Return True when stdout can encode box-drawing glyphs and emoji.
- `get_console` (function) `core/safe_console.py:42` `def get_console()` -- Build a Rich console with safe color/box defaults.
- `panel_box` (function) `core/safe_console.py:52` `def panel_box()` -- Return the ROUNDED box on UTF-8 sinks, ASCII otherwise.
- `milestone_glyph` (function) `core/safe_console.py:57` `def milestone_glyph(state)` -- Glyph for a milestone state: done / active / pending (or other).
- `progress_bar` (function) `core/safe_console.py:67` `def progress_bar(ratio, width)` -- Fixed-width fill bar, unicode blocks or ASCII hashes.

## core/safe_exec.py
Depends on: `core/logging.py`
Imported by: `cli/banner_config.py`, `cli/commands/misc_migrated.py`, `cli/commands/pwn.py`, `cli/commands/shellsys.py`, `core/process.py`, `core/safe_subprocess.py`, `lazyc2/blueprints/api_v1.py`, `modules/atomic_exploit_bridge.py`, `modules/atomic_resolver.py`, `modules/autonomous_exploit_engine.py`, `modules/bof_delivery.py`, `modules/chain_runner.py`, `modules/command_executor.py`, `modules/conditional_hooks.py`, `modules/dns_beacon.py`, `modules/lazyshortener.py`, `modules/metasploitable_migrations.py`, `modules/playbook_engine.py`, `modules/resource_script.py`, `modules/ttpscope_bridge.py`, `modules/winbox_gym.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_executor_kernel.py`, `tests/test_group_kill.py`, `tests/test_security_hardening_v4.py`, `tests/test_shell_semantics.py`
- `needs_shell` (function) `core/safe_exec.py:57` `def needs_shell(command)` -- Return True when a command string needs a shell to be interpreted.
- `safe_system` (function) `core/safe_exec.py:74` `def safe_system(command)` -- Execute a fixed command string through the shell safely.
- `safe_run_argv` (function) `core/safe_exec.py:174` `def safe_run_argv(argv)` -- Execute a command via subprocess without shell interpretation.
- `safe_run_shell` (function) `core/safe_exec.py:228` `def safe_run_shell(command)` -- Execute a command through the shell, gated by policy.
- `safe_clear_screen` (function) `core/safe_exec.py:285` `def safe_clear_screen()` -- Clear the terminal screen without using os.system.
- `validate_url` (function) `core/safe_exec.py:300` `def validate_url(url)` -- Validate a URL string, rejecting shell metacharacters.
- `safe_git_clone` (function) `core/safe_exec.py:327` `def safe_git_clone(repo_url, target_dir)` -- Clone a git repository safely using subprocess list-form.
- `safe_ip_show` (function) `core/safe_exec.py:361` `def safe_ip_show(interface)` -- Parse IP addresses from ``ip show`` output in Python.
- `safe_find_tool` (function) `core/safe_exec.py:398` `def safe_find_tool(name)` -- Find a tool on PATH using shutil.which.
- `safe_file_read` (function) `core/safe_exec.py:414` `def safe_file_read(path)` -- Read a file safely with a size limit.

## core/safe_import.py
Imported by: `cli/commands/campaign.py`, `tests/test_campaign_import_safety.py`
- `is_safe_identifier` (function) `core/safe_import.py:20` `def is_safe_identifier(name)` -- Return True when ``name`` is a bare SQL identifier.
- `filter_columns` (function) `core/safe_import.py:32` `def filter_columns(src_columns, dest_columns)` -- Intersect source columns with destination columns, safely.
- `safe_extract_zip` (function) `core/safe_import.py:51` `def safe_extract_zip(archive, dest)` -- Extract a zip archive with ZipSlip protection.
- `safe_copy_tree` (function) `core/safe_import.py:93` `def safe_copy_tree(src, dest)` -- Copy a directory tree without symlink escape.

## core/safe_subprocess.py
Depends on: `core/hardening.py`, `core/safe_exec.py`
Imported by: `core/process.py`, `tests/test_safe_subprocess.py`, `tests/test_safe_subprocess_behavior.py`, `tests/test_security_hardening.py`, `tests/test_shell_semantics.py`, `utils.py`
- `SafeRunner.__init__` (method) `core/safe_subprocess.py:70` `def __init__(self, audit_log_path)`
- `SafeRunner.run` (method) `core/safe_subprocess.py:73` `def run(self, argv)` -- Execute ``argv`` without invoking a shell.
- `SafeRunner.run_shell` (method) `core/safe_subprocess.py:105` `def run_shell(self, command)` -- Execute ``command`` through the system shell, gated by policy.

## core/scheduler.py
Depends on: `browser_sync_extension/background.js`, `core/logging.py`
- `TaskScheduler.__init__` (method) `core/scheduler.py:61` `def __init__(self)`
- `TaskScheduler.instance` (method) `core/scheduler.py:73` `def instance(cls)` -- Return the singleton ``TaskScheduler`` instance.
- `TaskScheduler.start` (method) `core/scheduler.py:81` `def start(self)` -- Start the scheduler background thread.
- `TaskScheduler.stop` (method) `core/scheduler.py:100` `def stop(self)` -- Stop the scheduler and cancel all pending tasks.
- `TaskScheduler.schedule_task` (method) `core/scheduler.py:123` `def schedule_task(self, name, interval_seconds, func)` -- Register a recurring task to run every ``interval_seconds``.
- `TaskScheduler.schedule_once` (method) `core/scheduler.py:157` `def schedule_once(self, name, delay_seconds, func)` -- Register a one-shot task to run after ``delay_seconds``.
- `TaskScheduler.cancel_task` (method) `core/scheduler.py:192` `def cancel_task(self, name)` -- Cancel a scheduled task by name.
- `TaskScheduler.list_tasks` (method) `core/scheduler.py:205` `def list_tasks(self)` -- Return metadata for all registered tasks.
- `get_scheduler` (function) `core/scheduler.py:285` `def get_scheduler()` -- Return the singleton ``TaskScheduler`` instance.

## core/security.py
Depends on: `core/logging.py`
- `anti_debug` (function) `core/security.py:18` `def anti_debug()` -- Check for debugger attachment and exit if found.
- `generate_certificates` (function) `core/security.py:58` `def generate_certificates(output_dir)` -- Generate a self-signed CA certificate and key pair.

## core/session_secrets.py
Depends on: `core/config.py`, `core/logging.py`
Imported by: `cli/commands/shellsys.py`, `lazyc2.py`, `modules/c2_agent.py`, `modules/c2_builder.py`, `tests/test_session_secrets.py`
- `rotate_session_secrets` (function) `core/session_secrets.py:38` `def rotate_session_secrets(config_obj, sessions_dir)` -- Generate and persist a fresh set of session secrets.
- `ensure_session_secrets` (function) `core/session_secrets.py:72` `def ensure_session_secrets(config_obj, rotate, sessions_dir)` -- Return valid session secrets, rotating them when required.

## core/terminal_guard.py
Imported by: `modules/lazy_runner.py`, `tests/test_lazy_runner.py`
- `emit_restore_sequences` (function) `core/terminal_guard.py:41` `def emit_restore_sequences()` -- Write the mode-reset sequences to the controlling terminal.
- `apply_stty_sane` (function) `core/terminal_guard.py:62` `def apply_stty_sane()` -- Best-effort ``stty sane`` fallback when termios restore fails.
- `TerminalGuard.__init__` (method) `core/terminal_guard.py:85` `def __init__(self)` -- Prepare an empty guard; the snapshot happens on ``__enter__``.
- `TerminalGuard.restore` (method) `core/terminal_guard.py:108` `def restore(self)` -- Restore saved termios, then reset extra terminal modes once.

## core/text_utils.py
Imported by: `cli/autosuggest.py`, `cli/graph_overlay.py`, `cli/palette_command.py`, `cli/palette_overlay.py`, `cli/reactive_hints.py`, `cli/reasoning_stream.py`, `cli/tips_engine.py`, `cli/toast_bus.py`
- `truncate_text` (function) `core/text_utils.py:10` `def truncate_text(value, max_len, marker)` -- Truncate value to max_len using marker.

## core/validators.py
Depends on: `core/console.py`, `core/host_policy.py`
Imported by: `cli/commands/_base.py`, `cli/commands/enum.py`, `cli/commands/mobile_macos.py`, `cli/commands/pwn.py`, `core/__init__.py`, `core/process.py`, `modules/c2_builder.py`, `tests/test_core.py`, `tests/test_host_policy.py`, `tests/test_input_fuzz.py`, `tests/test_require_guards.py`, `utils.py`
- `check_rhost` (function) `core/validators.py:26` `def check_rhost(rhost)` -- Return ``True`` if ``rhost`` is set, otherwise print an error and return ``False``.
- `check_lhost` (function) `core/validators.py:40` `def check_lhost(lhost)` -- Return ``True`` if ``lhost`` is set, otherwise print an error and return ``False``.
- `check_lport` (function) `core/validators.py:54` `def check_lport(lport)` -- Return ``True`` if ``lport`` is set, otherwise print an error and return ``False``.
- `check_port` (function) `core/validators.py:64` `def check_port(port, name)` -- Return ``True`` if ``port`` is a valid TCP/UDP port (1-65535).
- `require_rhost` (function) `core/validators.py:77` `def require_rhost(params)` -- Gate a command on a valid ``rhost`` looked up from ``params``.
- `require_lhost` (function) `core/validators.py:94` `def require_lhost(params)` -- Gate a command on a valid ``lhost`` looked up from ``params``.
- `require_lport` (function) `core/validators.py:107` `def require_lport(params)` -- Gate a command on a valid ``lport`` looked up from ``params``.
- `require_rport` (function) `core/validators.py:120` `def require_rport(params)` -- Gate a command on a valid ``rport`` looked up from ``params``.

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
- `Config.__init__` (method) `discord_c2.py:87` `def __init__(self, config_dict)`
- `load_payload` (function) `discord_c2.py:96` `def load_payload()`
- `on_ready` (function) `discord_c2.py:103` `def on_ready()`
- `start` (function) `discord_c2.py:108` `def start(ctx)`
- `exce_cmd` (function) `discord_c2.py:130` `def exce_cmd(ctx)`
- `add_cli` (function) `discord_c2.py:206` `def add_cli(ctx, new_client_id)`
- `handle_file` (function) `discord_c2.py:216` `def handle_file(ctx)`
- `download_c2` (function) `discord_c2.py:245` `def download_c2(ctx, client_id, file_name)`
- `send_connected_clients` (function) `discord_c2.py:256` `def send_connected_clients(ctx)`
- `clients` (function) `discord_c2.py:273` `def clients(ctx)`
- `addcli` (function) `discord_c2.py:278` `def addcli(ctx, new_client_id)`
- `c2` (function) `discord_c2.py:283` `def c2(ctx)`

## external/install_external.sh
- `ctrl_c` (function) `external/install_external.sh:13`
- `download` (function) `external/install_external.sh:18`

## fast_run_as_r00t.sh
- `log` (function) `fast_run_as_r00t.sh:59` -- ── Pretty-print helpers ──────────────────────────────────────────────────────
- `spin` (function) `fast_run_as_r00t.sh:60`
- `err_box` (function) `fast_run_as_r00t.sh:61`
- `ensure_gum` (function) `fast_run_as_r00t.sh:67` -- ── Ensure gum is installed ───────────────────────────────────────────────────
- `check_deps` (function) `fast_run_as_r00t.sh:78` -- ── Dependency check ──────────────────────────────────────────────────────────
- `check_sudo` (function) `fast_run_as_r00t.sh:87` -- ── Re-exec as root if needed ─────────────────────────────────────────────────
- `parse_args` (function) `fast_run_as_r00t.sh:96` -- ── CLI argument parsing ──────────────────────────────────────────────────────
- `t_send` (function) `fast_run_as_r00t.sh:114` -- Send one or more commands to the active tmux pane
- `t_lazyown` (function) `fast_run_as_r00t.sh:121` -- Open a new pane (split v or h), start LazyOwn shell with optional run flags, then send any follow-up commands once...
- `t_priv_user` (function) `fast_run_as_r00t.sh:134` -- Open a new pane running a command as unprivileged user 1000 (with venv).
- `start_chown_watcher` (function) `fast_run_as_r00t.sh:145` -- ── Background chown watcher ────────────────────────────────────────────────── Re-chowns the project tree to the...
- `kill_stale_c2` (function) `fast_run_as_r00t.sh:166` -- ── Stale C2 cleanup ────────────────────────────────────────────────────────── A lazyc2.py left over from a previous...

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
- `main` (function) `key.py:10` `def main()`

## lazy_sentinel4.py
Depends on: `cli/toast_bus.py`, `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `sanitize_content` (function) `lazy_sentinel4.py:45` `def sanitize_content(text)` -- Sanitize text to ensure it's safe for rendering.
- `RAGManager.__init__` (method) `lazy_sentinel4.py:59` `def __init__(self, model_name, cache_size)`
- `RAGManager.initialize_cache_table` (method) `lazy_sentinel4.py:71` `def initialize_cache_table(self)`
- `RAGManager.get_cache_key` (method) `lazy_sentinel4.py:83` `def get_cache_key(self, content)`
- `RAGManager.load_existing_vectorstore` (method) `lazy_sentinel4.py:86` `def load_existing_vectorstore(self)`
- `RAGManager.ollama_llm` (method) `lazy_sentinel4.py:99` `def ollama_llm(self, question, context)`
- `RAGManager.process_file_to_rag` (method) `lazy_sentinel4.py:113` `def process_file_to_rag(self, file_path)`
- `RAGManager.query_rag` (method) `lazy_sentinel4.py:153` `def query_rag(self, question)`
- `RAGManager.invalidate_cache` (method) `lazy_sentinel4.py:175` `def invalidate_cache(self, file_path)`
- `RAGManager.get_knowledge_base_stats` (method) `lazy_sentinel4.py:189` `def get_knowledge_base_stats(self)`
- `Database.__init__` (method) `lazy_sentinel4.py:213` `def __init__(self, db_path)`
- `Database.initialize` (method) `lazy_sentinel4.py:217` `def initialize(self)`
- `Database.execute` (method) `lazy_sentinel4.py:241` `def execute(self, query, params)`
- `Database.insert` (method) `lazy_sentinel4.py:253` `def insert(self, query, params)`
- `Alert.__init__` (method) `lazy_sentinel4.py:272` `def __init__(self, alert_type, details, severity)`
- `Alert.to_dict` (method) `lazy_sentinel4.py:278` `def to_dict(self)`
- `Alert.save_to_db` (method) `lazy_sentinel4.py:286` `def save_to_db(self, db)`
- `LazySentinelHandler.__init__` (method) `lazy_sentinel4.py:301` `def __init__(self, lazysentinel)`
- `LazySentinelHandler.is_text_file` (method) `lazy_sentinel4.py:304` `def is_text_file(self, file_path)`
- `LazySentinelHandler.on_created` (method) `lazy_sentinel4.py:314` `def on_created(self, event)`
- `LazySentinelHandler.on_modified` (method) `lazy_sentinel4.py:326` `def on_modified(self, event)`
- `LazySentinel.__init__` (method) `lazy_sentinel4.py:339` `def __init__(self, app, popup_queue, watch_dir, excluded_files, min_file_size)`
- `LazySentinel.chunk_text` (method) `lazy_sentinel4.py:359` `def chunk_text(self, text, chunk_size)`
- `LazySentinel.select_relevant_chunk` (method) `lazy_sentinel4.py:362` `def select_relevant_chunk(self, file_content, chunks)`
- `LazySentinel.parse_deepseek_response` (method) `lazy_sentinel4.py:376` `def parse_deepseek_response(self, response_text)`
- `LazySentinel.show_popup` (method) `lazy_sentinel4.py:402` `def show_popup(self, file_name, relevant_info, commands, details)`
- `LazySentinel.process_file` (method) `lazy_sentinel4.py:420` `def process_file(self, file_path)`
- `LazySentinel.stop` (method) `lazy_sentinel4.py:536` `def stop(self)`
- `App.__init__` (method) `lazy_sentinel4.py:543` `def __init__(self)`
- `App.display_toastr` (method) `lazy_sentinel4.py:557` `def display_toastr(self, file_name, relevant_info, commands, details, severity, duration)` -- Display the sentinel popup through the shared toast bus panel.
- `App.postcmd` (method) `lazy_sentinel4.py:567` `def postcmd(self, stop, line)` -- Check the popup queue after each command and display toastr notifications.
- `App.do_quit` (method) `lazy_sentinel4.py:591` `def do_quit(self, arg)`
- `App.do_debug` (method) `lazy_sentinel4.py:595` `def do_debug(self, arg)`
- `App.do_rag_query` (method) `lazy_sentinel4.py:604` `def do_rag_query(self, arg)`
- `App.do_rag_add` (method) `lazy_sentinel4.py:612` `def do_rag_add(self, arg)`
- `App.do_rag_status` (method) `lazy_sentinel4.py:627` `def do_rag_status(self, arg)`
- `App.do_rag_toggle` (method) `lazy_sentinel4.py:634` `def do_rag_toggle(self, arg)`
- `App.do_rag_bulk_add` (method) `lazy_sentinel4.py:639` `def do_rag_bulk_add(self, arg)`
- `App.do_rag_search` (method) `lazy_sentinel4.py:658` `def do_rag_search(self, arg)`
- `App.complete_rag_add` (method) `lazy_sentinel4.py:679` `def complete_rag_add(self, text, line, begidx, endidx)`
- `App.complete_rag_bulk_add` (method) `lazy_sentinel4.py:686` `def complete_rag_bulk_add(self, text, line, begidx, endidx)`


Next: [API_p8.md](API_p8.md)
