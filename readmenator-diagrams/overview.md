```mermaid
graph LR
    modules_autonomous_daemon["modules: autonomous_daemon"]
    cli_commands_utils["cli/commands: utils"]
    cli["cli"]
    modules_lazy_loop["modules: lazy_loop"]
    modules_lazyc2["modules: lazyc2"]
    lazygui_panels["lazygui/panels"]
    static_js["static/js"]
    modules_lazyown_facts["modules: lazyown_facts"]
    modules_opsec_scorer["modules: opsec_scorer"]
    cli_commands_c2_profile_engine["cli/commands: c2_profile_engine"]
    skills_claude_md_orchestrator["skills/claude_md_orchestrator"]
    core["core"]
    modules_finding_lifecycle["modules: finding_lifecycle"]
    modules_kerberos_core["modules: kerberos_core"]
    modules_saas_attacks["modules: saas_attacks"]
    modules_polymorphic_engine["modules: polymorphic_engine"]
    contrib_legacy["contrib/legacy"]
    tests["tests"]
    scripts_journal["scripts: journal"]
    modules_backdoor["modules/backdoor"]
    poc_tui["poc_tui"]
    scripts_check_contract_manifest["scripts: check_contract_manifest"]
    scripts_migrate_lazyown["scripts: migrate_lazyown"]
    tools["tools"]
    modules_autonomous_daemon -- "depends on" --> cli_commands_c2_profile_engine
    modules_autonomous_daemon -- "calls into" --> skills_claude_md_orchestrator
    modules_autonomous_daemon -- "calls into" --> core
    modules_autonomous_daemon -- "calls into" --> modules_finding_lifecycle
    modules_autonomous_daemon -- "calls into" --> modules_kerberos_core
    modules_autonomous_daemon -- "calls into" --> modules_polymorphic_engine
    modules_autonomous_daemon -- "calls into" --> scripts_journal
    modules_autonomous_daemon -- "calls into" --> cli_commands_utils
    modules_autonomous_daemon -- "calls into" --> poc_tui
    modules_autonomous_daemon -- "calls into" --> cli
    modules_autonomous_daemon -- "calls into" --> modules_lazy_loop
    modules_autonomous_daemon -- "calls into" --> modules_lazyc2
    modules_autonomous_daemon -- "calls into" --> lazygui_panels
    modules_autonomous_daemon -- "calls into" --> static_js
    modules_autonomous_daemon -- "calls into" --> modules_lazyown_facts
    modules_autonomous_daemon -- "calls into" --> modules_opsec_scorer
    cli_commands_c2_profile_engine -- "depends on" --> modules_autonomous_daemon
    cli_commands_c2_profile_engine -- "calls into" --> modules_polymorphic_engine
    cli_commands_c2_profile_engine -- "calls into" --> cli_commands_utils
    cli_commands_c2_profile_engine -- "calls into" --> poc_tui
    cli_commands_c2_profile_engine -- "calls into" --> cli
    cli_commands_c2_profile_engine -- "calls into" --> modules_lazy_loop
    cli_commands_c2_profile_engine -- "calls into" --> modules_lazyc2
    cli_commands_c2_profile_engine -- "calls into" --> lazygui_panels
    cli_commands_c2_profile_engine -- "calls into" --> static_js
    skills_claude_md_orchestrator -- "depends on" --> modules_autonomous_daemon
    skills_claude_md_orchestrator -- "depends on" --> cli_commands_c2_profile_engine
    skills_claude_md_orchestrator -- "calls into" --> core
    skills_claude_md_orchestrator -- "calls into" --> modules_polymorphic_engine
    skills_claude_md_orchestrator -- "calls into" --> scripts_journal
    skills_claude_md_orchestrator -- "depends on" --> cli_commands_utils
    skills_claude_md_orchestrator -- "calls into" --> poc_tui
    skills_claude_md_orchestrator -- "calls into" --> cli
    skills_claude_md_orchestrator -- "calls into" --> modules_lazy_loop
    skills_claude_md_orchestrator -- "calls into" --> modules_lazyc2
    skills_claude_md_orchestrator -- "calls into" --> lazygui_panels
    skills_claude_md_orchestrator -- "calls into" --> static_js
    core -- "depends on" --> modules_autonomous_daemon
    core -- "depends on" --> cli_commands_c2_profile_engine
    core -- "calls into" --> skills_claude_md_orchestrator
    core -- "calls into" --> modules_polymorphic_engine
    core -- "calls into" --> scripts_journal
    core -- "calls into" --> cli_commands_utils
    core -- "calls into" --> poc_tui
    core -- "calls into" --> cli
    core -- "calls into" --> modules_lazy_loop
    core -- "calls into" --> modules_lazyc2
    core -- "depends on" --> static_js
    core -- "calls into" --> modules_opsec_scorer
    modules_finding_lifecycle -- "calls into" --> modules_autonomous_daemon
    modules_finding_lifecycle -- "calls into" --> skills_claude_md_orchestrator
    modules_finding_lifecycle -- "calls into" --> modules_polymorphic_engine
    modules_finding_lifecycle -- "calls into" --> cli_commands_utils
    modules_finding_lifecycle -- "calls into" --> poc_tui
    modules_finding_lifecycle -- "calls into" --> cli
    modules_finding_lifecycle -- "calls into" --> modules_lazy_loop
    modules_finding_lifecycle -- "calls into" --> modules_lazyc2
    modules_finding_lifecycle -- "calls into" --> static_js
    modules_kerberos_core -- "calls into" --> skills_claude_md_orchestrator
    modules_kerberos_core -- "calls into" --> cli_commands_utils
    modules_kerberos_core -- "calls into" --> poc_tui
    modules_kerberos_core -- "calls into" --> lazygui_panels
    modules_saas_attacks -- "calls into" --> scripts_journal
    modules_saas_attacks -- "calls into" --> cli_commands_utils
    modules_saas_attacks -- "calls into" --> poc_tui
    modules_saas_attacks -- "calls into" --> lazygui_panels
    modules_polymorphic_engine -- "calls into" --> cli_commands_utils
    modules_polymorphic_engine -- "calls into" --> poc_tui
    modules_polymorphic_engine -- "calls into" --> modules_lazy_loop
    modules_polymorphic_engine -- "calls into" --> modules_lazyc2
    modules_polymorphic_engine -- "calls into" --> lazygui_panels
    contrib_legacy -- "calls into" --> poc_tui
    contrib_legacy -- "calls into" --> modules_lazy_loop
    tests -- "calls into" --> poc_tui
    tests -- "calls into" --> modules_lazy_loop
    scripts_journal -- "calls into" --> poc_tui
    scripts_journal -- "calls into" --> lazygui_panels
    cli_commands_utils -- "calls into" --> modules_autonomous_daemon
    cli_commands_utils -- "calls into" --> skills_claude_md_orchestrator
    cli_commands_utils -- "calls into" --> core
    cli_commands_utils -- "calls into" --> modules_polymorphic_engine
    cli_commands_utils -- "calls into" --> contrib_legacy
    cli_commands_utils -- "calls into" --> tests
    cli_commands_utils -- "calls into" --> scripts_journal
    cli_commands_utils -- "calls into" --> modules_backdoor
    cli_commands_utils -- "calls into" --> poc_tui
    cli_commands_utils -- "calls into" --> cli
    cli_commands_utils -- "calls into" --> modules_lazy_loop
    cli_commands_utils -- "calls into" --> modules_lazyc2
    cli_commands_utils -- "calls into" --> lazygui_panels
    cli_commands_utils -- "calls into" --> static_js
    cli_commands_utils -- "calls into" --> modules_lazyown_facts
    cli_commands_utils -- "depends on" --> modules_opsec_scorer
    poc_tui -- "calls into" --> skills_claude_md_orchestrator
    poc_tui -- "calls into" --> modules_polymorphic_engine
    poc_tui -- "calls into" --> modules_lazy_loop
    scripts_check_contract_manifest -- "calls into" --> skills_claude_md_orchestrator
    scripts_check_contract_manifest -- "calls into" --> modules_polymorphic_engine
    scripts_check_contract_manifest -- "calls into" --> modules_lazy_loop
    scripts_check_contract_manifest -- "calls into" --> lazygui_panels
    scripts_migrate_lazyown -- "calls into" --> tests
    scripts_migrate_lazyown -- "calls into" --> poc_tui
    scripts_migrate_lazyown -- "calls into" --> modules_lazy_loop
    scripts_migrate_lazyown -- "calls into" --> modules_lazyc2
    cli -- "calls into" --> modules_autonomous_daemon
    cli -- "depends on" --> cli_commands_c2_profile_engine
    cli -- "calls into" --> skills_claude_md_orchestrator
    cli -- "calls into" --> core
    cli -- "calls into" --> modules_polymorphic_engine
    cli -- "calls into" --> tests
    cli -- "calls into" --> scripts_journal
    cli -- "calls into" --> cli_commands_utils
    cli -- "calls into" --> poc_tui
    cli -- "calls into" --> modules_lazy_loop
    cli -- "calls into" --> modules_lazyc2
    cli -- "calls into" --> lazygui_panels
    cli -- "calls into" --> static_js
    cli -- "calls into" --> modules_lazyown_facts
    cli -- "calls into" --> modules_opsec_scorer
    modules_lazy_loop -- "calls into" --> modules_autonomous_daemon
    modules_lazy_loop -- "depends on" --> cli_commands_c2_profile_engine
    modules_lazy_loop -- "calls into" --> skills_claude_md_orchestrator
    modules_lazy_loop -- "calls into" --> core
    modules_lazy_loop -- "calls into" --> modules_finding_lifecycle
    modules_lazy_loop -- "calls into" --> modules_polymorphic_engine
    modules_lazy_loop -- "calls into" --> scripts_journal
    modules_lazy_loop -- "calls into" --> cli_commands_utils
    modules_lazy_loop -- "calls into" --> poc_tui
    modules_lazy_loop -- "calls into" --> cli
    modules_lazy_loop -- "calls into" --> modules_lazyc2
    modules_lazy_loop -- "calls into" --> lazygui_panels
    modules_lazy_loop -- "calls into" --> static_js
    modules_lazy_loop -- "calls into" --> modules_lazyown_facts
    modules_lazy_loop -- "calls into" --> modules_opsec_scorer
    modules_lazyc2 -- "calls into" --> modules_autonomous_daemon
    modules_lazyc2 -- "depends on" --> cli_commands_c2_profile_engine
    modules_lazyc2 -- "calls into" --> skills_claude_md_orchestrator
    modules_lazyc2 -- "calls into" --> core
    modules_lazyc2 -- "depends on" --> modules_finding_lifecycle
    modules_lazyc2 -- "calls into" --> modules_polymorphic_engine
    modules_lazyc2 -- "calls into" --> scripts_journal
    modules_lazyc2 -- "calls into" --> cli_commands_utils
    modules_lazyc2 -- "calls into" --> poc_tui
    modules_lazyc2 -- "calls into" --> cli
    modules_lazyc2 -- "calls into" --> modules_lazy_loop
    modules_lazyc2 -- "calls into" --> lazygui_panels
    modules_lazyc2 -- "calls into" --> static_js
    modules_lazyc2 -- "calls into" --> modules_lazyown_facts
    modules_lazyc2 -- "depends on" --> modules_opsec_scorer
    lazygui_panels -- "calls into" --> modules_autonomous_daemon
    lazygui_panels -- "depends on" --> cli_commands_c2_profile_engine
    lazygui_panels -- "calls into" --> skills_claude_md_orchestrator
    lazygui_panels -- "calls into" --> modules_polymorphic_engine
    lazygui_panels -- "calls into" --> tests
    lazygui_panels -- "calls into" --> scripts_journal
    lazygui_panels -- "calls into" --> poc_tui
    lazygui_panels -- "calls into" --> cli
    lazygui_panels -- "calls into" --> modules_lazy_loop
    lazygui_panels -- "calls into" --> modules_lazyc2
    lazygui_panels -- "calls into" --> static_js
    lazygui_panels -- "calls into" --> modules_opsec_scorer
    static_js -- "calls into" --> modules_autonomous_daemon
    static_js -- "calls into" --> cli_commands_c2_profile_engine
    static_js -- "calls into" --> skills_claude_md_orchestrator
    static_js -- "calls into" --> core
    static_js -- "calls into" --> modules_polymorphic_engine
    static_js -- "calls into" --> cli_commands_utils
    static_js -- "calls into" --> poc_tui
    static_js -- "calls into" --> cli
    static_js -- "calls into" --> modules_lazy_loop
    static_js -- "calls into" --> modules_lazyc2
    static_js -- "calls into" --> lazygui_panels
    modules_lazyown_facts -- "depends on" --> modules_autonomous_daemon
    modules_lazyown_facts -- "calls into" --> cli_commands_c2_profile_engine
    modules_lazyown_facts -- "calls into" --> skills_claude_md_orchestrator
    modules_lazyown_facts -- "calls into" --> core
    modules_lazyown_facts -- "calls into" --> modules_polymorphic_engine
    modules_lazyown_facts -- "calls into" --> tests
    modules_lazyown_facts -- "calls into" --> scripts_journal
    modules_lazyown_facts -- "calls into" --> cli_commands_utils
    modules_lazyown_facts -- "calls into" --> poc_tui
    modules_lazyown_facts -- "calls into" --> cli
    modules_lazyown_facts -- "calls into" --> modules_lazy_loop
    modules_lazyown_facts -- "calls into" --> modules_lazyc2
    modules_lazyown_facts -- "calls into" --> lazygui_panels
    modules_lazyown_facts -- "depends on" --> static_js
    modules_opsec_scorer -- "depends on" --> modules_autonomous_daemon
    modules_opsec_scorer -- "depends on" --> cli_commands_c2_profile_engine
    modules_opsec_scorer -- "calls into" --> modules_polymorphic_engine
    modules_opsec_scorer -- "calls into" --> cli_commands_utils
    modules_opsec_scorer -- "calls into" --> poc_tui
    modules_opsec_scorer -- "depends on" --> cli
    modules_opsec_scorer -- "calls into" --> modules_lazy_loop
    modules_opsec_scorer -- "calls into" --> modules_lazyc2
    modules_opsec_scorer -- "calls into" --> lazygui_panels
    modules_opsec_scorer -- "calls into" --> static_js
    modules_opsec_scorer -- "calls into" --> modules_lazyown_facts
    click modules_autonomous_daemon href "./modules_autonomous_daemon.md" "Details"
    click cli_commands_utils href "./cli_commands_utils.md" "Details"
    click cli href "./cli.md" "Details"
    click modules_lazy_loop href "./modules_lazy_loop.md" "Details"
    click modules_lazyc2 href "./modules_lazyc2.md" "Details"
    click lazygui_panels href "./lazygui_panels.md" "Details"
    click static_js href "./static_js.md" "Details"
    click modules_lazyown_facts href "./modules_lazyown_facts.md" "Details"
    click modules_opsec_scorer href "./modules_opsec_scorer.md" "Details"
    click cli_commands_c2_profile_engine href "./cli_commands_c2_profile_engine.md" "Details"
    click skills_claude_md_orchestrator href "./skills_claude_md_orchestrator.md" "Details"
    click core href "./core.md" "Details"
    click modules_finding_lifecycle href "./modules_finding_lifecycle.md" "Details"
    click modules_kerberos_core href "./modules_kerberos_core.md" "Details"
    click modules_saas_attacks href "./modules_saas_attacks.md" "Details"
    click modules_polymorphic_engine href "./modules_polymorphic_engine.md" "Details"
```

## Details

Static architecture map of 1138 files (asm, c, cpp, cs, h, js, lua, php, py, sh) in 24 components: modules: autonomous_daemon, cli/commands: utils, cli, modules: lazy_loop, modules: lazyc2, lazygui/panels, static/js, modules: lazyown_facts. Structure is extracted statically without LLM calls; component prose may be enriched locally.

### modules: autonomous_daemon (1)

modules: autonomous_daemon groups 163 files (py) around StructuredLogConfig, _JsonLineFormatter, __init__, format, _ConsoleFormatter. Caldera-style command set — operation lifecycle, TTP coverage, and planner.

**Related Classes/Methods**:

- <a href="../core/logging.py#L42-L70">core/logging.py::StructuredLogConfig</a>
- <a href="../core/logging.py#L71-L73">core/logging.py::_JsonLineFormatter</a>
- <a href="../core/logging.py#L74-L77">core/logging.py::__init__</a>
- <a href="../core/logging.py#L78-L120">core/logging.py::format</a>
- <a href="../core/logging.py#L121-L131">core/logging.py::_ConsoleFormatter</a>
- <a href="../core/logging.py#L132-L138">core/logging.py::format</a>
- <a href="../core/logging.py#L139-L147">core/logging.py::StructuredLogger</a>
- <a href="../core/logging.py#L148-L179">core/logging.py::makeRecord</a>

### cli/commands: utils (2)

cli/commands: utils groups 148 files (c, py) around needs_sudo, sudo_available, _retry_sudo_gate, redact_secrets, parse_ip_mac. Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de...

**Related Classes/Methods**:

- <a href="../utils.py#L323-L346">utils.py::needs_sudo</a>
- <a href="../utils.py#L347-L382">utils.py::sudo_available</a>
- <a href="../utils.py#L383-L398">utils.py::_retry_sudo_gate</a>
- <a href="../utils.py#L399-L418">utils.py::redact_secrets</a>
- <a href="../utils.py#L419-L440">utils.py::parse_ip_mac</a>
- <a href="../utils.py#L441-L475">utils.py::create_arp_packet</a>
- <a href="../utils.py#L476-L493">utils.py::send_packet</a>
- <a href="../utils.py#L494-L519">utils.py::load_version</a>

### cli (3)

cli groups 117 files (py) around _sanitize, colors_enabled, _paint, format_line, print_error. LazyOwn CLI infrastructure.

**Related Classes/Methods**:

- <a href="../core/console.py#L93-L97">core/console.py::_sanitize</a>
- <a href="../core/console.py#L98-L113">core/console.py::colors_enabled</a>
- <a href="../core/console.py#L114-L120">core/console.py::_paint</a>
- <a href="../core/console.py#L121-L136">core/console.py::format_line</a>
- <a href="../core/console.py#L137-L142">core/console.py::print_error</a>
- <a href="../core/console.py#L143-L148">core/console.py::print_msg</a>
- <a href="../core/console.py#L149-L154">core/console.py::print_warn</a>
- <a href="../core/console.py#L155-L160">core/console.py::print_succ</a>

### modules: lazy_loop (4)

modules: lazy_loop groups 115 files (py) around _apply_env_overrides, _coerce_env_value, _mask_if_sensitive, _log_config_change, _calling_frame. exploit commands migrated from lazyown.py.

**Related Classes/Methods**:

- <a href="../core/config.py#L70-L102">core/config.py::_apply_env_overrides</a>
- <a href="../core/config.py#L103-L127">core/config.py::_coerce_env_value</a>
- <a href="../core/config.py#L128-L145">core/config.py::_mask_if_sensitive</a>
- <a href="../core/config.py#L146-L167">core/config.py::_log_config_change</a>
- <a href="../core/config.py#L168-L181">core/config.py::_calling_frame</a>
- <a href="../core/config.py#L182-L205">core/config.py::_collect_validation_warnings</a>
- <a href="../core/config.py#L206-L218">core/config.py::Config</a>
- <a href="../core/config.py#L219-L227">core/config.py::__init__</a>

### modules: lazyc2 (5)

modules: lazyc2 groups 72 files (js, py) around Role, valid_roles, Permission, _UsersFileUnreadable, RBACUser. Automation command set — credential reuse, conditional hooks, operator profiles.

**Related Classes/Methods**:

- <a href="../modules/lazy_rbac.py#L55-L61">modules/lazy_rbac.py::Role</a>
- <a href="../modules/lazy_rbac.py#L62-L65">modules/lazy_rbac.py::valid_roles</a>
- <a href="../modules/lazy_rbac.py#L66-L114">modules/lazy_rbac.py::Permission</a>
- <a href="../modules/lazy_rbac.py#L115-L123">modules/lazy_rbac.py::_UsersFileUnreadable</a>
- <a href="../modules/lazy_rbac.py#L124-L135">modules/lazy_rbac.py::RBACUser</a>
- <a href="../modules/lazy_rbac.py#L136-L139">modules/lazy_rbac.py::to_dict</a>
- <a href="../modules/lazy_rbac.py#L140-L163">modules/lazy_rbac.py::from_dict</a>
- <a href="../modules/lazy_rbac.py#L164-L169">modules/lazy_rbac.py::get_role</a>

### lazygui/panels (6)

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

### static/js (7)

static/js groups 43 files (c, js, py, sh) around FieldKind, Severity, FieldSpec, ValidationIssue, _validate_string. ``assign`` business logic.

**Related Classes/Methods**:

- <a href="../core/payload_schema.py#L77-L94">core/payload_schema.py::FieldKind</a>
- <a href="../core/payload_schema.py#L95-L103">core/payload_schema.py::Severity</a>
- <a href="../core/payload_schema.py#L104-L145">core/payload_schema.py::FieldSpec</a>
- <a href="../core/payload_schema.py#L146-L168">core/payload_schema.py::ValidationIssue</a>
- <a href="../core/payload_schema.py#L169-L174">core/payload_schema.py::_validate_string</a>
- <a href="../core/payload_schema.py#L175-L188">core/payload_schema.py::_validate_int</a>
- <a href="../core/payload_schema.py#L189-L198">core/payload_schema.py::_validate_port</a>
- <a href="../core/payload_schema.py#L199-L215">core/payload_schema.py::_validate_bool</a>

### modules: lazyown_facts (8)

modules: lazyown_facts groups 32 files (py) around ChainStep, identifier, Chain, resolve, _render. Parsing, printing and replanning support for the ``apt_chain`` CLI.

**Related Classes/Methods**:

- <a href="../modules/chain_registry.py#L55-L83">modules/chain_registry.py::ChainStep</a>
- <a href="../modules/chain_registry.py#L84-L89">modules/chain_registry.py::identifier</a>
- <a href="../modules/chain_registry.py#L90-L106">modules/chain_registry.py::Chain</a>
- <a href="../modules/chain_registry.py#L107-L163">modules/chain_registry.py::resolve</a>
- <a href="../modules/chain_registry.py#L164-L192">modules/chain_registry.py::_render</a>
- <a href="../modules/chain_registry.py#L193-L219">modules/chain_registry.py::_when_tree</a>
- <a href="../modules/chain_registry.py#L220-L241">modules/chain_registry.py::evaluate_when</a>
- <a href="../modules/chain_registry.py#L242-L284">modules/chain_registry.py::_eval</a>

### modules: opsec_scorer (9)

modules: opsec_scorer groups 27 files (py) around KillChainConfig, world_model_path, phase_index, is_valid_phase, PhaseStatus. OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory...

**Related Classes/Methods**:

- <a href="../modules/killchain.py#L38-L115">modules/killchain.py::KillChainConfig</a>
- <a href="../modules/killchain.py#L116-L119">modules/killchain.py::world_model_path</a>
- <a href="../modules/killchain.py#L120-L126">modules/killchain.py::phase_index</a>
- <a href="../modules/killchain.py#L127-L135">modules/killchain.py::is_valid_phase</a>
- <a href="../modules/killchain.py#L136-L144">modules/killchain.py::PhaseStatus</a>
- <a href="../modules/killchain.py#L145-L153">modules/killchain.py::KillChain</a>
- <a href="../modules/killchain.py#L154-L158">modules/killchain.py::config</a>
- <a href="../modules/killchain.py#L159-L163">modules/killchain.py::phases</a>

### cli/commands: c2_profile_engine (10)

cli/commands: c2_profile_engine groups 26 files (py) around EnumCommandSet, do_smbclient, do_smbclient_impacket, do_smbclient_py, do_smbmap. BOF marketplace CommandSet — Beacon Object File discovery, install, and execution.

**Related Classes/Methods**:

- <a href="../cli/commands/enum.py#L31-L37">cli/commands/enum.py::EnumCommandSet</a>
- <a href="../cli/commands/enum.py#L38-L107">cli/commands/enum.py::do_smbclient</a>
- <a href="../cli/commands/enum.py#L108-L177">cli/commands/enum.py::do_smbclient_impacket</a>
- <a href="../cli/commands/enum.py#L178-L224">cli/commands/enum.py::do_smbclient_py</a>
- <a href="../cli/commands/enum.py#L225-L344">cli/commands/enum.py::do_smbmap</a>
- <a href="../cli/commands/enum.py#L345-L389">cli/commands/enum.py::do_getnpusers</a>
- <a href="../cli/commands/enum.py#L390-L445">cli/commands/enum.py::do_psexec</a>
- <a href="../cli/commands/enum.py#L446-L501">cli/commands/enum.py::do_psexec_py</a>

### skills/claude_md_orchestrator (11)

skills/claude_md_orchestrator groups 23 files (js, py) around _now_iso, Stage, Severity, Contract, to_dict. Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de...

**Related Classes/Methods**:

- <a href="../skills/claude_md_orchestrator/models.py#L19-L27">skills/claude_md_orchestrator/models.py::_now_iso</a>
- <a href="../skills/claude_md_orchestrator/models.py#L28-L49">skills/claude_md_orchestrator/models.py::Stage</a>
- <a href="../skills/claude_md_orchestrator/models.py#L50-L67">skills/claude_md_orchestrator/models.py::Severity</a>
- <a href="../skills/claude_md_orchestrator/models.py#L68-L90">skills/claude_md_orchestrator/models.py::Contract</a>
- <a href="../skills/claude_md_orchestrator/models.py#L91-L95">skills/claude_md_orchestrator/models.py::to_dict</a>
- <a href="../skills/claude_md_orchestrator/models.py#L96-L108">skills/claude_md_orchestrator/models.py::from_dict</a>
- <a href="../skills/claude_md_orchestrator/models.py#L109-L119">skills/claude_md_orchestrator/models.py::SadPath</a>
- <a href="../skills/claude_md_orchestrator/models.py#L120-L124">skills/claude_md_orchestrator/models.py::to_dict</a>

### core (12)

core groups 22 files (py) around strip_ansi, BudgetExceeded, LLMBackendLike, generate, stream_generate. Artificial Intelligence command set.

**Related Classes/Methods**:

- <a href="../core/parsers.py#L15-L34">core/parsers.py::strip_ansi</a>
- <a href="../core/llm_budget.py#L54-L57">core/llm_budget.py::BudgetExceeded</a>
- <a href="../core/llm_budget.py#L58-L60">core/llm_budget.py::LLMBackendLike</a>
- <a href="../core/llm_budget.py#L61-L62">core/llm_budget.py::generate</a>
- <a href="../core/llm_budget.py#L63-L64">core/llm_budget.py::stream_generate</a>
- <a href="../core/llm_budget.py#L65-L68">core/llm_budget.py::complete</a>
- <a href="../core/llm_budget.py#L69-L80">core/llm_budget.py::ModelPrice</a>
- <a href="../core/llm_budget.py#L81-L102">core/llm_budget.py::from_mapping</a>

### modules: finding_lifecycle (13)

modules: finding_lifecycle groups 13 files (py) around _cache_path, _cache_load, _cache_save, _cached, _store. Database commands — workspace isolation, host/service/vuln management, nmap import...

**Related Classes/Methods**:

- <a href="../modules/osint_enrich.py#L47-L51">modules/osint_enrich.py::_cache_path</a>
- <a href="../modules/osint_enrich.py#L52-L60">modules/osint_enrich.py::_cache_load</a>
- <a href="../modules/osint_enrich.py#L61-L68">modules/osint_enrich.py::_cache_save</a>
- <a href="../modules/osint_enrich.py#L69-L76">modules/osint_enrich.py::_cached</a>
- <a href="../modules/osint_enrich.py#L77-L83">modules/osint_enrich.py::_store</a>
- <a href="../modules/osint_enrich.py#L84-L95">modules/osint_enrich.py::_get_json</a>
- <a href="../modules/osint_enrich.py#L96-L109">modules/osint_enrich.py::_post_json</a>
- <a href="../modules/osint_enrich.py#L110-L121">modules/osint_enrich.py::_get_text</a>

### modules: kerberos_core (14)

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

### modules: saas_attacks (15)

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

### modules: polymorphic_engine (16)

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

### contrib/legacy (17)

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

### tests (18)

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

### scripts: journal (19)

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

### modules/backdoor (20)

modules/backdoor groups 2 files (c, h) around logg, bzero, bootRun, str_cut, Shell.

**Related Classes/Methods**:

- <a href="../modules/backdoor/keylogger.h#L1-L106">modules/backdoor/keylogger.h::logg</a>
- <a href="../modules/backdoor/backdoor.c#L14-L17">modules/backdoor/backdoor.c::bzero</a>
- <a href="../modules/backdoor/backdoor.c#L18-L48">modules/backdoor/backdoor.c::bootRun</a>
- <a href="../modules/backdoor/backdoor.c#L49-L83">modules/backdoor/backdoor.c::str_cut</a>
- <a href="../modules/backdoor/backdoor.c#L84-L124">modules/backdoor/backdoor.c::Shell</a>
- <a href="../modules/backdoor/backdoor.c#L125-L160">modules/backdoor/backdoor.c::WinMain</a>

### poc_tui (21)

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

### scripts: check_contract_manifest (22)

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

### scripts: migrate_lazyown (23)

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

### tools (24)

tools groups 2 files (py) around font, render, main, main. Generate LazyOwn demo GIFs without external services.

**Related Classes/Methods**:

- <a href="../tools/gen_demo_gifs.py#L14-L21">tools/gen_demo_gifs.py::font</a>
- <a href="../tools/gen_demo_gifs.py#L22-L69">tools/gen_demo_gifs.py::render</a>
- <a href="../tools/gen_demo_gifs.py#L70-L79">tools/gen_demo_gifs.py::main</a>
- <a href="../tools/gen_demo_gifs_extra.py#L49-L58">tools/gen_demo_gifs_extra.py::main</a>
