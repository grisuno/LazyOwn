```mermaid
graph LR
    skills_mcp_tools["skills/mcp_tools"]
    cli_commands["cli/commands"]
    modules_lazyc2["modules: lazyc2"]
    cli["cli"]
    modules_lazy_loop["modules: lazy_loop"]
    modules_lazyown["modules: lazyown"]
    modules_chain_runner["modules: chain_runner"]
    modules_intel_fusion["modules: intel_fusion"]
    lazygui_panels["lazygui/panels"]
    static_js["static/js"]
    modules_llm_budget["modules: llm_budget"]
    modules_bof_registry["modules: bof_registry"]
    modules_dashboard_engine["modules: dashboard_engine"]
    skills_claude_md_orchestrator["skills/claude_md_orchestrator"]
    modules_defense_eval["modules: defense_eval"]
    modules_kerberos_core["modules: kerberos_core"]
    modules_saas_attacks["modules: saas_attacks"]
    modules_network_opsec["modules: network_opsec"]
    modules_polymorphic_engine["modules: polymorphic_engine"]
    contrib_legacy["contrib/legacy"]
    tests["tests"]
    modules_memory_store["modules: memory_store"]
    scripts_journal["scripts: journal"]
    modules_backdoor["modules/backdoor"]
    modules_lazy_netattack["modules: lazy_netattack"]
    modules_lazy_triage["modules: lazy_triage"]
    poc_tui["poc_tui"]
    scripts_check_contract_manifest["scripts: check_contract_manifest"]
    scripts_migrate_lazyown["scripts: migrate_lazyown"]
    tools["tools"]
    skills_mcp_tools -- "calls into" --> static_js
    skills_mcp_tools -- "calls into" --> modules_llm_budget
    skills_mcp_tools -- "calls into" --> modules_bof_registry
    skills_mcp_tools -- "calls into" --> skills_claude_md_orchestrator
    skills_mcp_tools -- "calls into" --> modules_kerberos_core
    skills_mcp_tools -- "calls into" --> modules_polymorphic_engine
    skills_mcp_tools -- "depends on" --> cli_commands
    skills_mcp_tools -- "calls into" --> modules_memory_store
    skills_mcp_tools -- "calls into" --> scripts_journal
    skills_mcp_tools -- "calls into" --> poc_tui
    skills_mcp_tools -- "calls into" --> modules_lazyc2
    skills_mcp_tools -- "calls into" --> cli
    skills_mcp_tools -- "calls into" --> modules_lazy_loop
    skills_mcp_tools -- "calls into" --> modules_lazyown
    skills_mcp_tools -- "calls into" --> modules_chain_runner
    skills_mcp_tools -- "calls into" --> modules_intel_fusion
    skills_mcp_tools -- "calls into" --> lazygui_panels
    static_js -- "depends on" --> skills_mcp_tools
    static_js -- "calls into" --> modules_llm_budget
    static_js -- "depends on" --> modules_bof_registry
    static_js -- "calls into" --> skills_claude_md_orchestrator
    static_js -- "calls into" --> modules_polymorphic_engine
    static_js -- "calls into" --> cli_commands
    static_js -- "calls into" --> poc_tui
    static_js -- "calls into" --> modules_lazyc2
    static_js -- "calls into" --> cli
    static_js -- "calls into" --> modules_lazy_loop
    static_js -- "calls into" --> modules_lazyown
    static_js -- "calls into" --> modules_chain_runner
    static_js -- "depends on" --> modules_intel_fusion
    static_js -- "calls into" --> lazygui_panels
    modules_llm_budget -- "calls into" --> skills_mcp_tools
    modules_llm_budget -- "calls into" --> static_js
    modules_llm_budget -- "calls into" --> modules_bof_registry
    modules_llm_budget -- "calls into" --> skills_claude_md_orchestrator
    modules_llm_budget -- "calls into" --> modules_polymorphic_engine
    modules_llm_budget -- "calls into" --> cli_commands
    modules_llm_budget -- "calls into" --> scripts_journal
    modules_llm_budget -- "calls into" --> poc_tui
    modules_llm_budget -- "depends on" --> modules_lazyc2
    modules_llm_budget -- "calls into" --> cli
    modules_llm_budget -- "calls into" --> modules_lazy_loop
    modules_llm_budget -- "calls into" --> modules_lazyown
    modules_llm_budget -- "calls into" --> modules_chain_runner
    modules_llm_budget -- "calls into" --> modules_intel_fusion
    modules_llm_budget -- "calls into" --> lazygui_panels
    modules_bof_registry -- "calls into" --> skills_mcp_tools
    modules_bof_registry -- "calls into" --> static_js
    modules_bof_registry -- "calls into" --> modules_polymorphic_engine
    modules_bof_registry -- "calls into" --> cli_commands
    modules_bof_registry -- "calls into" --> poc_tui
    modules_bof_registry -- "calls into" --> modules_lazyc2
    modules_bof_registry -- "calls into" --> cli
    modules_bof_registry -- "depends on" --> modules_lazyown
    modules_bof_registry -- "calls into" --> modules_chain_runner
    modules_bof_registry -- "calls into" --> lazygui_panels
    modules_dashboard_engine -- "depends on" --> skills_mcp_tools
    modules_dashboard_engine -- "calls into" --> modules_llm_budget
    modules_dashboard_engine -- "depends on" --> cli_commands
    modules_dashboard_engine -- "calls into" --> scripts_journal
    modules_dashboard_engine -- "calls into" --> poc_tui
    modules_dashboard_engine -- "calls into" --> modules_lazyc2
    modules_dashboard_engine -- "calls into" --> cli
    modules_dashboard_engine -- "calls into" --> modules_lazy_loop
    modules_dashboard_engine -- "calls into" --> modules_lazyown
    modules_dashboard_engine -- "calls into" --> modules_chain_runner
    modules_dashboard_engine -- "calls into" --> lazygui_panels
    skills_claude_md_orchestrator -- "calls into" --> modules_llm_budget
    skills_claude_md_orchestrator -- "depends on" --> modules_bof_registry
    skills_claude_md_orchestrator -- "calls into" --> modules_polymorphic_engine
    skills_claude_md_orchestrator -- "calls into" --> cli_commands
    skills_claude_md_orchestrator -- "calls into" --> scripts_journal
    skills_claude_md_orchestrator -- "calls into" --> poc_tui
    skills_claude_md_orchestrator -- "calls into" --> modules_lazyc2
    skills_claude_md_orchestrator -- "calls into" --> modules_lazy_loop
    skills_claude_md_orchestrator -- "calls into" --> modules_lazyown
    skills_claude_md_orchestrator -- "calls into" --> modules_chain_runner
    skills_claude_md_orchestrator -- "calls into" --> lazygui_panels
    modules_defense_eval -- "depends on" --> cli_commands
    modules_defense_eval -- "depends on" --> modules_lazyc2
    modules_defense_eval -- "calls into" --> modules_lazy_loop
    modules_defense_eval -- "calls into" --> modules_lazyown
    modules_defense_eval -- "calls into" --> modules_chain_runner
    modules_defense_eval -- "calls into" --> lazygui_panels
    modules_kerberos_core -- "calls into" --> skills_claude_md_orchestrator
    modules_kerberos_core -- "depends on" --> cli_commands
    modules_kerberos_core -- "calls into" --> poc_tui
    modules_kerberos_core -- "calls into" --> modules_lazyown
    modules_kerberos_core -- "calls into" --> lazygui_panels
    modules_saas_attacks -- "depends on" --> cli_commands
    modules_saas_attacks -- "calls into" --> scripts_journal
    modules_saas_attacks -- "calls into" --> poc_tui
    modules_saas_attacks -- "calls into" --> modules_lazyown
    modules_saas_attacks -- "calls into" --> lazygui_panels
    modules_network_opsec -- "calls into" --> static_js
    modules_network_opsec -- "depends on" --> cli_commands
    modules_network_opsec -- "calls into" --> poc_tui
    modules_network_opsec -- "calls into" --> modules_lazyown
    modules_network_opsec -- "calls into" --> lazygui_panels
    modules_polymorphic_engine -- "depends on" --> cli_commands
    modules_polymorphic_engine -- "calls into" --> poc_tui
    modules_polymorphic_engine -- "calls into" --> modules_lazyc2
    modules_polymorphic_engine -- "calls into" --> modules_lazyown
    modules_polymorphic_engine -- "calls into" --> modules_chain_runner
    modules_polymorphic_engine -- "calls into" --> lazygui_panels
    cli_commands -- "calls into" --> skills_mcp_tools
    cli_commands -- "calls into" --> static_js
    cli_commands -- "calls into" --> modules_llm_budget
    cli_commands -- "calls into" --> modules_bof_registry
    cli_commands -- "calls into" --> skills_claude_md_orchestrator
    cli_commands -- "calls into" --> modules_polymorphic_engine
    cli_commands -- "calls into" --> contrib_legacy
    cli_commands -- "calls into" --> tests
    cli_commands -- "calls into" --> scripts_journal
    cli_commands -- "calls into" --> modules_lazy_netattack
    cli_commands -- "calls into" --> poc_tui
    cli_commands -- "calls into" --> modules_lazyc2
    cli_commands -- "calls into" --> cli
    cli_commands -- "calls into" --> modules_lazy_loop
    cli_commands -- "calls into" --> modules_lazyown
    cli_commands -- "calls into" --> modules_chain_runner
    cli_commands -- "calls into" --> modules_intel_fusion
    cli_commands -- "calls into" --> lazygui_panels
    contrib_legacy -- "calls into" --> poc_tui
    contrib_legacy -- "calls into" --> modules_lazy_loop
    tests -- "calls into" --> poc_tui
    tests -- "calls into" --> modules_chain_runner
    modules_memory_store -- "calls into" --> skills_mcp_tools
    modules_memory_store -- "calls into" --> modules_polymorphic_engine
    scripts_journal -- "calls into" --> poc_tui
    scripts_journal -- "calls into" --> lazygui_panels
    modules_lazy_triage -- "calls into" --> poc_tui
    modules_lazy_triage -- "calls into" --> modules_chain_runner
    poc_tui -- "calls into" --> skills_claude_md_orchestrator
    poc_tui -- "calls into" --> modules_polymorphic_engine
    poc_tui -- "calls into" --> modules_chain_runner
    scripts_check_contract_manifest -- "calls into" --> skills_claude_md_orchestrator
    scripts_check_contract_manifest -- "calls into" --> modules_polymorphic_engine
    scripts_check_contract_manifest -- "calls into" --> modules_chain_runner
    scripts_check_contract_manifest -- "calls into" --> lazygui_panels
    scripts_migrate_lazyown -- "calls into" --> tests
    scripts_migrate_lazyown -- "calls into" --> poc_tui
    scripts_migrate_lazyown -- "calls into" --> modules_lazyc2
    scripts_migrate_lazyown -- "calls into" --> modules_chain_runner
    modules_lazyc2 -- "calls into" --> skills_mcp_tools
    modules_lazyc2 -- "calls into" --> static_js
    modules_lazyc2 -- "calls into" --> modules_llm_budget
    modules_lazyc2 -- "depends on" --> modules_bof_registry
    modules_lazyc2 -- "depends on" --> modules_dashboard_engine
    modules_lazyc2 -- "calls into" --> skills_claude_md_orchestrator
    modules_lazyc2 -- "calls into" --> modules_polymorphic_engine
    modules_lazyc2 -- "depends on" --> cli_commands
    modules_lazyc2 -- "calls into" --> scripts_journal
    modules_lazyc2 -- "calls into" --> modules_backdoor
    modules_lazyc2 -- "calls into" --> poc_tui
    modules_lazyc2 -- "calls into" --> cli
    modules_lazyc2 -- "calls into" --> modules_lazy_loop
    modules_lazyc2 -- "calls into" --> modules_lazyown
    modules_lazyc2 -- "calls into" --> modules_chain_runner
    modules_lazyc2 -- "depends on" --> modules_intel_fusion
    modules_lazyc2 -- "calls into" --> lazygui_panels
    cli -- "calls into" --> skills_mcp_tools
    cli -- "calls into" --> static_js
    cli -- "calls into" --> modules_llm_budget
    cli -- "calls into" --> modules_bof_registry
    cli -- "calls into" --> skills_claude_md_orchestrator
    cli -- "calls into" --> modules_polymorphic_engine
    cli -- "calls into" --> cli_commands
    cli -- "calls into" --> tests
    cli -- "calls into" --> scripts_journal
    cli -- "calls into" --> poc_tui
    cli -- "calls into" --> modules_lazyc2
    cli -- "calls into" --> modules_lazy_loop
    cli -- "calls into" --> modules_lazyown
    cli -- "calls into" --> modules_chain_runner
    cli -- "depends on" --> modules_intel_fusion
    cli -- "calls into" --> lazygui_panels
    modules_lazy_loop -- "calls into" --> skills_mcp_tools
    modules_lazy_loop -- "calls into" --> static_js
    modules_lazy_loop -- "calls into" --> modules_llm_budget
    modules_lazy_loop -- "depends on" --> modules_bof_registry
    modules_lazy_loop -- "calls into" --> modules_dashboard_engine
    modules_lazy_loop -- "calls into" --> skills_claude_md_orchestrator
    modules_lazy_loop -- "depends on" --> modules_defense_eval
    modules_lazy_loop -- "calls into" --> modules_polymorphic_engine
    modules_lazy_loop -- "calls into" --> cli_commands
    modules_lazy_loop -- "calls into" --> scripts_journal
    modules_lazy_loop -- "calls into" --> poc_tui
    modules_lazy_loop -- "calls into" --> modules_lazyc2
    modules_lazy_loop -- "calls into" --> cli
    modules_lazy_loop -- "calls into" --> modules_lazyown
    modules_lazy_loop -- "calls into" --> modules_chain_runner
    modules_lazy_loop -- "calls into" --> modules_intel_fusion
    modules_lazy_loop -- "calls into" --> lazygui_panels
    modules_lazyown -- "calls into" --> skills_mcp_tools
    modules_lazyown -- "depends on" --> static_js
    modules_lazyown -- "calls into" --> modules_llm_budget
    modules_lazyown -- "calls into" --> modules_bof_registry
    modules_lazyown -- "calls into" --> skills_claude_md_orchestrator
    modules_lazyown -- "calls into" --> modules_polymorphic_engine
    modules_lazyown -- "calls into" --> cli_commands
    modules_lazyown -- "calls into" --> tests
    modules_lazyown -- "calls into" --> scripts_journal
    modules_lazyown -- "calls into" --> modules_lazy_netattack
    modules_lazyown -- "calls into" --> poc_tui
    modules_lazyown -- "calls into" --> modules_lazyc2
    modules_lazyown -- "calls into" --> cli
    modules_lazyown -- "calls into" --> modules_lazy_loop
    modules_lazyown -- "calls into" --> modules_chain_runner
    modules_lazyown -- "depends on" --> modules_intel_fusion
    modules_lazyown -- "calls into" --> lazygui_panels
    modules_chain_runner -- "calls into" --> skills_mcp_tools
    modules_chain_runner -- "calls into" --> static_js
    modules_chain_runner -- "calls into" --> modules_llm_budget
    modules_chain_runner -- "calls into" --> modules_bof_registry
    modules_chain_runner -- "calls into" --> skills_claude_md_orchestrator
    modules_chain_runner -- "calls into" --> modules_defense_eval
    modules_chain_runner -- "calls into" --> modules_polymorphic_engine
    modules_chain_runner -- "calls into" --> cli_commands
    modules_chain_runner -- "calls into" --> tests
    modules_chain_runner -- "calls into" --> scripts_journal
    modules_chain_runner -- "calls into" --> poc_tui
    modules_chain_runner -- "calls into" --> modules_lazyc2
    modules_chain_runner -- "calls into" --> cli
    modules_chain_runner -- "calls into" --> modules_lazy_loop
    modules_chain_runner -- "calls into" --> modules_lazyown
    modules_chain_runner -- "calls into" --> modules_intel_fusion
    modules_chain_runner -- "calls into" --> lazygui_panels
    modules_intel_fusion -- "depends on" --> skills_mcp_tools
    modules_intel_fusion -- "calls into" --> static_js
    modules_intel_fusion -- "depends on" --> modules_llm_budget
    modules_intel_fusion -- "calls into" --> skills_claude_md_orchestrator
    modules_intel_fusion -- "calls into" --> modules_polymorphic_engine
    modules_intel_fusion -- "depends on" --> cli_commands
    modules_intel_fusion -- "calls into" --> scripts_journal
    modules_intel_fusion -- "calls into" --> poc_tui
    modules_intel_fusion -- "calls into" --> modules_lazyc2
    modules_intel_fusion -- "calls into" --> cli
    modules_intel_fusion -- "calls into" --> modules_lazy_loop
    modules_intel_fusion -- "calls into" --> modules_lazyown
    modules_intel_fusion -- "calls into" --> modules_chain_runner
    modules_intel_fusion -- "calls into" --> lazygui_panels
    lazygui_panels -- "calls into" --> skills_mcp_tools
    lazygui_panels -- "calls into" --> static_js
    lazygui_panels -- "depends on" --> modules_bof_registry
    lazygui_panels -- "calls into" --> skills_claude_md_orchestrator
    lazygui_panels -- "calls into" --> modules_polymorphic_engine
    lazygui_panels -- "calls into" --> cli_commands
    lazygui_panels -- "calls into" --> tests
    lazygui_panels -- "calls into" --> scripts_journal
    lazygui_panels -- "calls into" --> poc_tui
    lazygui_panels -- "calls into" --> modules_lazyc2
    lazygui_panels -- "calls into" --> cli
    lazygui_panels -- "calls into" --> modules_lazy_loop
    lazygui_panels -- "calls into" --> modules_lazyown
    lazygui_panels -- "calls into" --> modules_chain_runner
    lazygui_panels -- "calls into" --> modules_intel_fusion
    click skills_mcp_tools href "./skills_mcp_tools.md" "Details"
    click cli_commands href "./cli_commands.md" "Details"
    click modules_lazyc2 href "./modules_lazyc2.md" "Details"
    click cli href "./cli.md" "Details"
    click modules_lazy_loop href "./modules_lazy_loop.md" "Details"
    click modules_lazyown href "./modules_lazyown.md" "Details"
    click modules_chain_runner href "./modules_chain_runner.md" "Details"
    click modules_intel_fusion href "./modules_intel_fusion.md" "Details"
    click lazygui_panels href "./lazygui_panels.md" "Details"
    click static_js href "./static_js.md" "Details"
    click modules_llm_budget href "./modules_llm_budget.md" "Details"
    click modules_bof_registry href "./modules_bof_registry.md" "Details"
    click modules_dashboard_engine href "./modules_dashboard_engine.md" "Details"
    click skills_claude_md_orchestrator href "./skills_claude_md_orchestrator.md" "Details"
    click modules_defense_eval href "./modules_defense_eval.md" "Details"
    click modules_kerberos_core href "./modules_kerberos_core.md" "Details"
    click modules_saas_attacks href "./modules_saas_attacks.md" "Details"
    click modules_network_opsec href "./modules_network_opsec.md" "Details"
    click modules_polymorphic_engine href "./modules_polymorphic_engine.md" "Details"
```

## Details

Static architecture map of 1545 files (asm, c, cpp, cs, h, js, lua, php, py, sh) in 30 components: skills/mcp_tools, cli/commands, modules: lazyc2, cli, modules: lazy_loop, modules: lazyown, modules: chain_runner, modules: intel_fusion. Structure is extracted statically without LLM calls; component prose may be enriched locally.

### skills/mcp_tools (1)

skills/mcp_tools groups 235 files (py) around MCPContext, _try_import, _update_task_status, _credential_worth_task, _task_title_open. Caldera-style command set — operation lifecycle, TTP coverage, and planner.

**Related Classes/Methods**:

- <a href="../skills/mcp_tools/_context.py#L21-L74">skills/mcp_tools/_context.py::MCPContext</a>
- <a href="../skills/autonomous_daemon.py#L132-L190">skills/autonomous_daemon.py::_try_import</a>
- <a href="../skills/autonomous_daemon.py#L191-L211">skills/autonomous_daemon.py::_update_task_status</a>
- <a href="../skills/autonomous_daemon.py#L212-L233">skills/autonomous_daemon.py::_credential_worth_task</a>
- <a href="../skills/autonomous_daemon.py#L234-L252">skills/autonomous_daemon.py::_task_title_open</a>
- <a href="../skills/autonomous_daemon.py#L253-L295">skills/autonomous_daemon.py::_inject_to_tasks_json</a>
- <a href="../skills/autonomous_daemon.py#L296-L318">skills/autonomous_daemon.py::_emit</a>
- <a href="../skills/autonomous_daemon.py#L319-L333">skills/autonomous_daemon.py::_record_intent</a>

### cli/commands (2)

cli/commands groups 162 files (py) around lazyown_set_config, needs_sudo, sudo_available, _retry_sudo_gate, redact_secrets. Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de...

**Related Classes/Methods**:

- <a href="../utils.py#L324-L357">utils.py::lazyown_set_config</a>
- <a href="../utils.py#L358-L381">utils.py::needs_sudo</a>
- <a href="../utils.py#L382-L417">utils.py::sudo_available</a>
- <a href="../utils.py#L418-L433">utils.py::_retry_sudo_gate</a>
- <a href="../utils.py#L434-L453">utils.py::redact_secrets</a>
- <a href="../utils.py#L454-L475">utils.py::parse_ip_mac</a>
- <a href="../utils.py#L476-L510">utils.py::create_arp_packet</a>
- <a href="../utils.py#L511-L528">utils.py::send_packet</a>

### modules: lazyc2 (3)

modules: lazyc2 groups 138 files (c, js, py) around StructuredLogConfig, _JsonLineFormatter, __init__, format, _ConsoleFormatter. Automation command set — credential reuse, conditional hooks, operator profiles.

**Related Classes/Methods**:

- <a href="../core/logging.py#L42-L70">core/logging.py::StructuredLogConfig</a>
- <a href="../core/logging.py#L71-L73">core/logging.py::_JsonLineFormatter</a>
- <a href="../core/logging.py#L74-L77">core/logging.py::__init__</a>
- <a href="../core/logging.py#L78-L120">core/logging.py::format</a>
- <a href="../core/logging.py#L121-L131">core/logging.py::_ConsoleFormatter</a>
- <a href="../core/logging.py#L132-L138">core/logging.py::format</a>
- <a href="../core/logging.py#L139-L147">core/logging.py::StructuredLogger</a>
- <a href="../core/logging.py#L148-L179">core/logging.py::makeRecord</a>

### cli (4)

cli groups 115 files (py) around _sanitize, colors_enabled, _paint, format_line, print_error. LazyOwn CLI infrastructure.

**Related Classes/Methods**:

- <a href="../core/console.py#L93-L97">core/console.py::_sanitize</a>
- <a href="../core/console.py#L98-L113">core/console.py::colors_enabled</a>
- <a href="../core/console.py#L114-L120">core/console.py::_paint</a>
- <a href="../core/console.py#L121-L136">core/console.py::format_line</a>
- <a href="../core/console.py#L137-L142">core/console.py::print_error</a>
- <a href="../core/console.py#L143-L148">core/console.py::print_msg</a>
- <a href="../core/console.py#L149-L154">core/console.py::print_warn</a>
- <a href="../core/console.py#L155-L160">core/console.py::print_succ</a>

### modules: lazy_loop (5)

modules: lazy_loop groups 110 files (py) around plausible_command, looks_like_prose, _is_host_like_target, _sudo_unavailable, _is_ip_literal. exploit commands migrated from lazyown.py.

**Related Classes/Methods**:

- <a href="../modules/lazy_loop.py#L175-L198">modules/lazy_loop.py::plausible_command</a>
- <a href="../modules/lazy_loop.py#L199-L225">modules/lazy_loop.py::looks_like_prose</a>
- <a href="../modules/lazy_loop.py#L226-L311">modules/lazy_loop.py::_is_host_like_target</a>
- <a href="../modules/lazy_loop.py#L312-L317">modules/lazy_loop.py::_sudo_unavailable</a>
- <a href="../modules/lazy_loop.py#L318-L331">modules/lazy_loop.py::_is_ip_literal</a>
- <a href="../modules/lazy_loop.py#L332-L346">modules/lazy_loop.py::_valid_nmap_port_spec</a>
- <a href="../modules/lazy_loop.py#L347-L424">modules/lazy_loop.py::repair_worker_command</a>
- <a href="../modules/lazy_loop.py#L425-L476">modules/lazy_loop.py::_host_from_token</a>

### modules: lazyown (6)

modules: lazyown groups 106 files (py) around _apply_env_overrides, _coerce_env_value, _mask_if_sensitive, _log_config_change, _calling_frame. Declarative cmd2 alias loader.

**Related Classes/Methods**:

- <a href="../core/config.py#L75-L107">core/config.py::_apply_env_overrides</a>
- <a href="../core/config.py#L108-L132">core/config.py::_coerce_env_value</a>
- <a href="../core/config.py#L133-L150">core/config.py::_mask_if_sensitive</a>
- <a href="../core/config.py#L151-L172">core/config.py::_log_config_change</a>
- <a href="../core/config.py#L173-L186">core/config.py::_calling_frame</a>
- <a href="../core/config.py#L187-L210">core/config.py::_collect_validation_warnings</a>
- <a href="../core/config.py#L211-L223">core/config.py::Config</a>
- <a href="../core/config.py#L224-L232">core/config.py::__init__</a>

### modules: chain_runner (7)

modules: chain_runner groups 98 files (c, js, py) around skip_pending, ChainStep, identifier, Chain, resolve. Parsing, printing and replanning support for the ``apt_chain`` CLI.

**Related Classes/Methods**:

- <a href="../modules/chain_registry.py#L69-L103">modules/chain_registry.py::skip_pending</a>
- <a href="../modules/chain_registry.py#L104-L151">modules/chain_registry.py::ChainStep</a>
- <a href="../modules/chain_registry.py#L152-L157">modules/chain_registry.py::identifier</a>
- <a href="../modules/chain_registry.py#L158-L175">modules/chain_registry.py::Chain</a>
- <a href="../modules/chain_registry.py#L176-L240">modules/chain_registry.py::resolve</a>
- <a href="../modules/chain_registry.py#L241-L269">modules/chain_registry.py::_render</a>
- <a href="../modules/chain_registry.py#L270-L296">modules/chain_registry.py::_when_tree</a>
- <a href="../modules/chain_registry.py#L297-L318">modules/chain_registry.py::evaluate_when</a>

### modules: intel_fusion (8)

modules: intel_fusion groups 66 files (py) around OutcomeEvent, host_value, key, to_dict, OutcomeBus. Attack-surface operations: confirmed discovery scans, estorides fusion.

**Related Classes/Methods**:

- <a href="../modules/outcome_bus.py#L78-L105">modules/outcome_bus.py::OutcomeEvent</a>
- <a href="../modules/outcome_bus.py#L106-L109">modules/outcome_bus.py::host_value</a>
- <a href="../modules/outcome_bus.py#L110-L127">modules/outcome_bus.py::key</a>
- <a href="../modules/outcome_bus.py#L128-L156">modules/outcome_bus.py::to_dict</a>
- <a href="../modules/outcome_bus.py#L157-L159">modules/outcome_bus.py::OutcomeBus</a>
- <a href="../modules/outcome_bus.py#L160-L172">modules/outcome_bus.py::__init__</a>
- <a href="../modules/outcome_bus.py#L173-L178">modules/outcome_bus.py::reset</a>
- <a href="../modules/outcome_bus.py#L179-L193">modules/outcome_bus.py::_sink</a>

### lazygui/panels (9)

lazygui/panels groups 54 files (py) around WindowConstants, TimingConstants, NetworkConstants, PtyConstants, FontConstants. Entry point for ``python -m lazygui``.

**Related Classes/Methods**:

- <a href="../lazygui/config/constants.py#L18-L33">lazygui/config/constants.py::WindowConstants</a>
- <a href="../lazygui/config/constants.py#L34-L47">lazygui/config/constants.py::TimingConstants</a>
- <a href="../lazygui/config/constants.py#L48-L85">lazygui/config/constants.py::NetworkConstants</a>
- <a href="../lazygui/config/constants.py#L86-L98">lazygui/config/constants.py::PtyConstants</a>
- <a href="../lazygui/config/constants.py#L99-L123">lazygui/config/constants.py::FontConstants</a>
- <a href="../lazygui/config/constants.py#L124-L141">lazygui/config/constants.py::KeybindingConstants</a>
- <a href="../lazygui/config/constants.py#L142-L160">lazygui/config/constants.py::IdentifierConstants</a>
- <a href="../lazygui/config/constants.py#L161-L175">lazygui/config/constants.py::ThemeConstants</a>

### static/js (10)

static/js groups 49 files (c, js, php, py, sh) around FieldKind, Severity, FieldSpec, ValidationIssue, _validate_string. ``assign`` business logic.

**Related Classes/Methods**:

- <a href="../core/payload_schema.py#L77-L94">core/payload_schema.py::FieldKind</a>
- <a href="../core/payload_schema.py#L95-L103">core/payload_schema.py::Severity</a>
- <a href="../core/payload_schema.py#L104-L145">core/payload_schema.py::FieldSpec</a>
- <a href="../core/payload_schema.py#L146-L168">core/payload_schema.py::ValidationIssue</a>
- <a href="../core/payload_schema.py#L169-L174">core/payload_schema.py::_validate_string</a>
- <a href="../core/payload_schema.py#L175-L188">core/payload_schema.py::_validate_int</a>
- <a href="../core/payload_schema.py#L189-L198">core/payload_schema.py::_validate_port</a>
- <a href="../core/payload_schema.py#L199-L215">core/payload_schema.py::_validate_bool</a>

### modules: llm_budget (11)

modules: llm_budget groups 41 files (py) around is_model_missing_error, groq_model_chain, LLMBackendUnavailableError, LLMBackendNotSupportedError, default_model_for. Artificial Intelligence command set.

**Related Classes/Methods**:

- <a href="../modules/llm_factory.py#L121-L140">modules/llm_factory.py::is_model_missing_error</a>
- <a href="../modules/llm_factory.py#L141-L189">modules/llm_factory.py::groq_model_chain</a>
- <a href="../modules/llm_factory.py#L190-L193">modules/llm_factory.py::LLMBackendUnavailableError</a>
- <a href="../modules/llm_factory.py#L194-L223">modules/llm_factory.py::LLMBackendNotSupportedError</a>
- <a href="../modules/llm_factory.py#L224-L244">modules/llm_factory.py::default_model_for</a>
- <a href="../modules/llm_factory.py#L245-L265">modules/llm_factory.py::model_config_key</a>
- <a href="../modules/llm_factory.py#L266-L290">modules/llm_factory.py::api_key_config_key</a>
- <a href="../modules/llm_factory.py#L291-L308">modules/llm_factory.py::backend_requires_api_key</a>

### modules: bof_registry (12)

modules: bof_registry groups 32 files (py) around EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap. BOF marketplace CommandSet — Beacon Object File discovery, staging and delivery.

**Related Classes/Methods**:

- <a href="../cli/commands/enum.py#L31-L37">cli/commands/enum.py::EnumCommandSet</a>
- <a href="../cli/commands/enum.py#L38-L107">cli/commands/enum.py::do_smbclient</a>
- <a href="../cli/commands/enum.py#L108-L177">cli/commands/enum.py::do_smbclient_impacket</a>
- <a href="../cli/commands/enum.py#L178-L224">cli/commands/enum.py::do_smbclient_py</a>
- <a href="../cli/commands/enum.py#L225-L344">cli/commands/enum.py::do_smbmap</a>
- <a href="../cli/commands/enum.py#L345-L389">cli/commands/enum.py::do_getnpusers</a>
- <a href="../cli/commands/enum.py#L390-L445">cli/commands/enum.py::do_psexec</a>
- <a href="../cli/commands/enum.py#L446-L501">cli/commands/enum.py::do_psexec_py</a>

### modules: dashboard_engine (13)

modules: dashboard_engine groups 17 files (py) around PwnCommandSet, do_auto_pwn, do_rich_tui, do_exploit_chain, do_lolbas_list. Autonomous exploitation and LOLBAS command set.

**Related Classes/Methods**:

- <a href="../cli/commands/pwn.py#L28-L34">cli/commands/pwn.py::PwnCommandSet</a>
- <a href="../cli/commands/pwn.py#L35-L108">cli/commands/pwn.py::do_auto_pwn</a>
- <a href="../cli/commands/pwn.py#L109-L157">cli/commands/pwn.py::do_rich_tui</a>
- <a href="../cli/commands/pwn.py#L158-L244">cli/commands/pwn.py::do_exploit_chain</a>
- <a href="../cli/commands/pwn.py#L245-L301">cli/commands/pwn.py::do_lolbas_list</a>
- <a href="../cli/commands/pwn.py#L302-L393">cli/commands/pwn.py::do_lolbas_use</a>
- <a href="../cli/commands/pwn.py#L394-L421">cli/commands/pwn.py::do_stealth_on</a>
- <a href="../cli/commands/pwn.py#L422-L435">cli/commands/pwn.py::do_stealth_off</a>

### skills/claude_md_orchestrator (14)

skills/claude_md_orchestrator groups 14 files (py) around _now_iso, Stage, Severity, Contract, to_dict. Public API for the claude_md_orchestrator skill.

**Related Classes/Methods**:

- <a href="../skills/claude_md_orchestrator/models.py#L19-L27">skills/claude_md_orchestrator/models.py::_now_iso</a>
- <a href="../skills/claude_md_orchestrator/models.py#L28-L49">skills/claude_md_orchestrator/models.py::Stage</a>
- <a href="../skills/claude_md_orchestrator/models.py#L50-L67">skills/claude_md_orchestrator/models.py::Severity</a>
- <a href="../skills/claude_md_orchestrator/models.py#L68-L90">skills/claude_md_orchestrator/models.py::Contract</a>
- <a href="../skills/claude_md_orchestrator/models.py#L91-L95">skills/claude_md_orchestrator/models.py::to_dict</a>
- <a href="../skills/claude_md_orchestrator/models.py#L96-L108">skills/claude_md_orchestrator/models.py::from_dict</a>
- <a href="../skills/claude_md_orchestrator/models.py#L109-L119">skills/claude_md_orchestrator/models.py::SadPath</a>
- <a href="../skills/claude_md_orchestrator/models.py#L120-L124">skills/claude_md_orchestrator/models.py::to_dict</a>

### modules: defense_eval (15)

modules: defense_eval groups 8 files (py) around RuleEvaluationError, Condition, Evaluation, to_dict, DatasetSummary. Closed-loop detection rule tuning: baseline vs candidate comparison.

**Related Classes/Methods**:

- <a href="../modules/defense_eval.py#L39-L43">modules/defense_eval.py::RuleEvaluationError</a>
- <a href="../modules/defense_eval.py#L44-L52">modules/defense_eval.py::Condition</a>
- <a href="../modules/defense_eval.py#L53-L61">modules/defense_eval.py::Evaluation</a>
- <a href="../modules/defense_eval.py#L62-L73">modules/defense_eval.py::to_dict</a>
- <a href="../modules/defense_eval.py#L74-L81">modules/defense_eval.py::DatasetSummary</a>
- <a href="../modules/defense_eval.py#L82-L92">modules/defense_eval.py::to_dict</a>
- <a href="../modules/defense_eval.py#L93-L102">modules/defense_eval.py::RuleResult</a>
- <a href="../modules/defense_eval.py#L103-L114">modules/defense_eval.py::to_dict</a>

### modules: kerberos_core (16)

modules: kerberos_core groups 7 files (py) around KerberosPrincipal, to_string, EncryptedData, KerberosTicket, has_flag. Active Directory attack commands — Kerberos, tickets, delegation, DACL, GPO...

**Related Classes/Methods**:

- <a href="../modules/kerberos_core.py#L139-L151">modules/kerberos_core.py::KerberosPrincipal</a>
- <a href="../modules/kerberos_core.py#L152-L156">modules/kerberos_core.py::to_string</a>
- <a href="../modules/kerberos_core.py#L157-L171">modules/kerberos_core.py::EncryptedData</a>
- <a href="../modules/kerberos_core.py#L172-L206">modules/kerberos_core.py::KerberosTicket</a>
- <a href="../modules/kerberos_core.py#L207-L212">modules/kerberos_core.py::has_flag</a>
- <a href="../modules/kerberos_core.py#L213-L227">modules/kerberos_core.py::PACSignature</a>
- <a href="../modules/kerberos_core.py#L228-L248">modules/kerberos_core.py::PACInfo</a>
- <a href="../modules/kerberos_core.py#L249-L270">modules/kerberos_core.py::TGSRequest</a>

### modules: saas_attacks (17)

modules: saas_attacks groups 7 files (py) around AWSConfig, AWSAttackEngine, __init__, enumerate_iam_permissions, lambda_backdoor. Cloud attack commands — Azure AD/Entra ID, AWS, GCP, Kubernetes, cross-cloud, SaaS.

**Related Classes/Methods**:

- <a href="../modules/aws_attacks.py#L58-L79">modules/aws_attacks.py::AWSConfig</a>
- <a href="../modules/aws_attacks.py#L80-L90">modules/aws_attacks.py::AWSAttackEngine</a>
- <a href="../modules/aws_attacks.py#L91-L94">modules/aws_attacks.py::__init__</a>
- <a href="../modules/aws_attacks.py#L95-L126">modules/aws_attacks.py::enumerate_iam_permissions</a>
- <a href="../modules/aws_attacks.py#L127-L154">modules/aws_attacks.py::lambda_backdoor</a>
- <a href="../modules/aws_attacks.py#L155-L180">modules/aws_attacks.py::sts_role_chain</a>
- <a href="../modules/aws_attacks.py#L181-L205">modules/aws_attacks.py::ec2_user_data_exfil</a>
- <a href="../modules/aws_attacks.py#L206-L241">modules/aws_attacks.py::s3_enumeration</a>

### modules: network_opsec (18)

modules: network_opsec groups 6 files (py) around LogTamperConfig, LogTamper, __init__, windows_clear_commands, linux_clear_commands. OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory...

**Related Classes/Methods**:

- <a href="../modules/log_tamper.py#L71-L94">modules/log_tamper.py::LogTamperConfig</a>
- <a href="../modules/log_tamper.py#L95-L104">modules/log_tamper.py::LogTamper</a>
- <a href="../modules/log_tamper.py#L105-L107">modules/log_tamper.py::__init__</a>
- <a href="../modules/log_tamper.py#L108-L175">modules/log_tamper.py::windows_clear_commands</a>
- <a href="../modules/log_tamper.py#L176-L242">modules/log_tamper.py::linux_clear_commands</a>
- <a href="../modules/log_tamper.py#L243-L294">modules/log_tamper.py::macos_clear_commands</a>
- <a href="../modules/log_tamper.py#L295-L306">modules/log_tamper.py::generate_all</a>
- <a href="../modules/log_tamper.py#L307-L340">modules/log_tamper.py::auditd_disable_commands</a>

### modules: polymorphic_engine (19)

modules: polymorphic_engine groups 6 files (py) around DotNetPayloadConfig, DotNetPayloadFactory, __init__, _detect_compiler, list_templates. Payload arsenal commands — dotnet, reflective DLL, staged delivery, polymorphic...

**Related Classes/Methods**:

- <a href="../modules/dotnet_payload.py#L293-L314">modules/dotnet_payload.py::DotNetPayloadConfig</a>
- <a href="../modules/dotnet_payload.py#L315-L326">modules/dotnet_payload.py::DotNetPayloadFactory</a>
- <a href="../modules/dotnet_payload.py#L327-L332">modules/dotnet_payload.py::__init__</a>
- <a href="../modules/dotnet_payload.py#L333-L363">modules/dotnet_payload.py::_detect_compiler</a>
- <a href="../modules/dotnet_payload.py#L364-L367">modules/dotnet_payload.py::list_templates</a>
- <a href="../modules/dotnet_payload.py#L368-L388">modules/dotnet_payload.py::_resolve_template</a>
- <a href="../modules/dotnet_payload.py#L389-L402">modules/dotnet_payload.py::generate_source</a>
- <a href="../modules/dotnet_payload.py#L403-L453">modules/dotnet_payload.py::compile</a>

### contrib/legacy (20)

contrib/legacy groups 5 files (py) around base64_encode, base64_decode, caesar_cipher, caesar_decipher, key_substitution.

**Related Classes/Methods**:

- <a href="../modules/lazyencoder_decoder.py#L4-L7">modules/lazyencoder_decoder.py::base64_encode</a>
- <a href="../modules/lazyencoder_decoder.py#L8-L12">modules/lazyencoder_decoder.py::base64_decode</a>
- <a href="../modules/lazyencoder_decoder.py#L13-L26">modules/lazyencoder_decoder.py::caesar_cipher</a>
- <a href="../modules/lazyencoder_decoder.py#L27-L30">modules/lazyencoder_decoder.py::caesar_decipher</a>
- <a href="../modules/lazyencoder_decoder.py#L31-L46">modules/lazyencoder_decoder.py::key_substitution</a>
- <a href="../modules/lazyencoder_decoder.py#L47-L62">modules/lazyencoder_decoder.py::key_substitution_reverse</a>
- <a href="../modules/lazyencoder_decoder.py#L63-L74">modules/lazyencoder_decoder.py::encode</a>
- <a href="../modules/lazyencoder_decoder.py#L75-L81">modules/lazyencoder_decoder.py::encode_string</a>

### tests (21)

tests groups 4 files (py) around backup_files, restore_files, run_tests, title, run_all. Shared driver for curated mutation runners.

**Related Classes/Methods**:

- <a href="../tests/mutation_common.py#L20-L29">tests/mutation_common.py::backup_files</a>
- <a href="../tests/mutation_common.py#L30-L36">tests/mutation_common.py::restore_files</a>
- <a href="../tests/mutation_common.py#L37-L48">tests/mutation_common.py::run_tests</a>
- <a href="../tests/mutation_common.py#L49-L55">tests/mutation_common.py::title</a>
- <a href="../tests/mutation_common.py#L56-L96">tests/mutation_common.py::run_all</a>
- <a href="../tests/run_mutation_loop_cli_catalog.py#L50-L56">tests/run_mutation_loop_cli_catalog.py::main</a>
- <a href="../tests/run_mutation_trigger_policy.py#L52-L58">tests/run_mutation_trigger_policy.py::main</a>
- <a href="../tests/run_mutation_verb_catalog.py#L52-L58">tests/run_mutation_verb_catalog.py::main</a>

### modules: memory_store (22)

modules: memory_store groups 3 files (py) around EmbeddingError, _fnv1a, _tokens, embed, cosine. Hashing-trick text embeddings for episodic memory recall.

**Related Classes/Methods**:

- <a href="../modules/memory_embeddings.py#L30-L33">modules/memory_embeddings.py::EmbeddingError</a>
- <a href="../modules/memory_embeddings.py#L34-L40">modules/memory_embeddings.py::_fnv1a</a>
- <a href="../modules/memory_embeddings.py#L41-L49">modules/memory_embeddings.py::_tokens</a>
- <a href="../modules/memory_embeddings.py#L50-L74">modules/memory_embeddings.py::embed</a>
- <a href="../modules/memory_embeddings.py#L75-L84">modules/memory_embeddings.py::cosine</a>
- <a href="../modules/memory_embeddings.py#L85-L108">modules/memory_embeddings.py::semantic_top_k</a>
- <a href="../modules/memory_embeddings.py#L109-L113">modules/memory_embeddings.py::as_floats</a>
- <a href="../modules/memory_store.py#L84-L96">modules/memory_store.py::MemoryEntry</a>

### scripts: journal (23)

scripts: journal groups 3 files (py) around JournalError, JournalConfig, from_git_remote, _run_git, _git_remote_slug. Read-before-you-write journal over GitHub Discussions.

**Related Classes/Methods**:

- <a href="../scripts/journal.py#L48-L52">scripts/journal.py::JournalError</a>
- <a href="../scripts/journal.py#L53-L70">scripts/journal.py::JournalConfig</a>
- <a href="../scripts/journal.py#L71-L89">scripts/journal.py::from_git_remote</a>
- <a href="../scripts/journal.py#L90-L113">scripts/journal.py::_run_git</a>
- <a href="../scripts/journal.py#L114-L123">scripts/journal.py::_git_remote_slug</a>
- <a href="../scripts/journal.py#L124-L148">scripts/journal.py::_default_runner</a>
- <a href="../scripts/journal.py#L149-L162">scripts/journal.py::Journal</a>
- <a href="../scripts/journal.py#L163-L183">scripts/journal.py::_graphql</a>

### modules/backdoor (24)

modules/backdoor groups 2 files (c, h) around logg, bzero, RUNKEY_NAME, bootRun, str_cut.

**Related Classes/Methods**:

- <a href="../modules/backdoor/keylogger.h#L1-L106">modules/backdoor/keylogger.h::logg</a>
- <a href="../modules/backdoor/backdoor.c#L14-L16">modules/backdoor/backdoor.c::bzero</a>
- <a href="../modules/backdoor/backdoor.c#L17-L21">modules/backdoor/backdoor.c::RUNKEY_NAME</a>
- <a href="../modules/backdoor/backdoor.c#L22-L52">modules/backdoor/backdoor.c::bootRun</a>
- <a href="../modules/backdoor/backdoor.c#L53-L87">modules/backdoor/backdoor.c::str_cut</a>
- <a href="../modules/backdoor/backdoor.c#L88-L128">modules/backdoor/backdoor.c::Shell</a>
- <a href="../modules/backdoor/backdoor.c#L129-L163">modules/backdoor/backdoor.c::WinMain</a>

### modules: lazy_netattack (25)

modules: lazy_netattack groups 2 files (py) around AttackVectorVerdict, as_dict, SurfaceEvidence, _svc_blob, _windows_hosts. Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.

**Related Classes/Methods**:

- <a href="../modules/lazy_netattack.py#L88-L106">modules/lazy_netattack.py::AttackVectorVerdict</a>
- <a href="../modules/lazy_netattack.py#L107-L119">modules/lazy_netattack.py::as_dict</a>
- <a href="../modules/lazy_netattack.py#L120-L135">modules/lazy_netattack.py::SurfaceEvidence</a>
- <a href="../modules/lazy_netattack.py#L136-L145">modules/lazy_netattack.py::_svc_blob</a>
- <a href="../modules/lazy_netattack.py#L146-L160">modules/lazy_netattack.py::_windows_hosts</a>
- <a href="../modules/lazy_netattack.py#L161-L172">modules/lazy_netattack.py::_ad_hosts</a>
- <a href="../modules/lazy_netattack.py#L173-L178">modules/lazy_netattack.py::_signing_not_required</a>
- <a href="../modules/lazy_netattack.py#L179-L183">modules/lazy_netattack.py::_downgrade_candidates</a>

### modules: lazy_triage (26)

modules: lazy_triage groups 2 files (py) around rank, hard_evidence, apply_rules, signature_for, SignatureStore. Triage doctrine: evidence floors, verdict algebra and signature dedup.

**Related Classes/Methods**:

- <a href="../modules/lazy_triage.py#L42-L46">modules/lazy_triage.py::rank</a>
- <a href="../modules/lazy_triage.py#L47-L79">modules/lazy_triage.py::hard_evidence</a>
- <a href="../modules/lazy_triage.py#L80-L107">modules/lazy_triage.py::apply_rules</a>
- <a href="../modules/lazy_triage.py#L108-L134">modules/lazy_triage.py::signature_for</a>
- <a href="../modules/lazy_triage.py#L135-L137">modules/lazy_triage.py::SignatureStore</a>
- <a href="../modules/lazy_triage.py#L138-L143">modules/lazy_triage.py::__init__</a>
- <a href="../modules/lazy_triage.py#L144-L161">modules/lazy_triage.py::fresh_signature</a>
- <a href="../modules/lazy_triage.py#L162-L165">modules/lazy_triage.py::reset</a>

### poc_tui (27)

poc_tui groups 2 files (py) around PayloadConfig, __post_init__, reload, save, get. Payload.json configuration manager for the TUI shell.

**Related Classes/Methods**:

- <a href="../poc_tui/config.py#L12-L17">poc_tui/config.py::PayloadConfig</a>
- <a href="../poc_tui/config.py#L18-L20">poc_tui/config.py::__post_init__</a>
- <a href="../poc_tui/config.py#L21-L27">poc_tui/config.py::reload</a>
- <a href="../poc_tui/config.py#L28-L34">poc_tui/config.py::save</a>
- <a href="../poc_tui/config.py#L35-L37">poc_tui/config.py::get</a>
- <a href="../poc_tui/config.py#L38-L40">poc_tui/config.py::set</a>
- <a href="../poc_tui/config.py#L41-L43">poc_tui/config.py::keys</a>
- <a href="../poc_tui/config.py#L44-L46">poc_tui/config.py::items</a>

### scripts: check_contract_manifest (28)

scripts: check_contract_manifest groups 2 files (py) around ManifestConfig, __post_init__, _resolve, _top_level_names, _module_path. Verify that documented contracts still exist on disk.

**Related Classes/Methods**:

- <a href="../scripts/check_contract_manifest.py#L34-L52">scripts/check_contract_manifest.py::ManifestConfig</a>
- <a href="../scripts/check_contract_manifest.py#L53-L57">scripts/check_contract_manifest.py::__post_init__</a>
- <a href="../scripts/check_contract_manifest.py#L58-L71">scripts/check_contract_manifest.py::_resolve</a>
- <a href="../scripts/check_contract_manifest.py#L72-L99">scripts/check_contract_manifest.py::_top_level_names</a>
- <a href="../scripts/check_contract_manifest.py#L100-L111">scripts/check_contract_manifest.py::_module_path</a>
- <a href="../scripts/check_contract_manifest.py#L112-L126">scripts/check_contract_manifest.py::_dotted_symbol_exists</a>
- <a href="../scripts/check_contract_manifest.py#L127-L137">scripts/check_contract_manifest.py::_iter_table_cells</a>
- <a href="../scripts/check_contract_manifest.py#L138-L153">scripts/check_contract_manifest.py::_extract_path_tokens</a>

### scripts: migrate_lazyown (29)

scripts: migrate_lazyown groups 2 files (py) around _category_from_decorator, _indent_level, extract_method, rewrite_globals, build_migrated_module. Staged migration script: extract do_* methods from lazyown.py into cli/commands/.

**Related Classes/Methods**:

- <a href="../scripts/migrate_lazyown.py#L70-L83">scripts/migrate_lazyown.py::_category_from_decorator</a>
- <a href="../scripts/migrate_lazyown.py#L84-L87">scripts/migrate_lazyown.py::_indent_level</a>
- <a href="../scripts/migrate_lazyown.py#L88-L95">scripts/migrate_lazyown.py::extract_method</a>
- <a href="../scripts/migrate_lazyown.py#L96-L123">scripts/migrate_lazyown.py::rewrite_globals</a>
- <a href="../scripts/migrate_lazyown.py#L124-L172">scripts/migrate_lazyown.py::build_migrated_module</a>
- <a href="../scripts/migrate_lazyown.py#L173-L239">scripts/migrate_lazyown.py::main</a>
- <a href="../tests/test_migrate_lazyown_generator.py#L27-L56">tests/test_migrate_lazyown_generator.py::_module_all</a>
- <a href="../tests/test_migrate_lazyown_generator.py#L57-L61">tests/test_migrate_lazyown_generator.py::test_generated_module_parses</a>

### tools (30)

tools groups 2 files (py) around font, render, main, main. Generate LazyOwn demo GIFs without external services.

**Related Classes/Methods**:

- <a href="../tools/gen_demo_gifs.py#L14-L21">tools/gen_demo_gifs.py::font</a>
- <a href="../tools/gen_demo_gifs.py#L22-L69">tools/gen_demo_gifs.py::render</a>
- <a href="../tools/gen_demo_gifs.py#L70-L79">tools/gen_demo_gifs.py::main</a>
- <a href="../tools/gen_demo_gifs_extra.py#L49-L58">tools/gen_demo_gifs_extra.py::main</a>
