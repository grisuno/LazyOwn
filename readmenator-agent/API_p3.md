# API (page 3 of 29)
Previous: [API_p2.md](API_p2.md)

## cli/commands/lazyops.py
Depends on: `cli/commands/_base.py`, `core/process.py`, `modules/__init__.py`, `modules/addon_updater.py`, `modules/auto_registry.py`, `modules/custom_tools.py`, `modules/lazy_agent.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_commander.py`, `modules/lazy_deviations.py`, `modules/lazy_engine.py`, `modules/lazy_installer.py`, `modules/lazy_loop.py`, `modules/lazy_proxy.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/lazy_sandbox.py`, `modules/lazy_skill_mirror.py`, `modules/lazy_skills.py`, `modules/orchestrator_config.py`, `modules/selfupdate.py`, `modules/traffic_recorder.py`, `utils.py`
Imported by: `tests/test_asset_gate.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_runner.py`
- `LazyCommandSet.do_lazy_dispatch` (method) `cli/commands/lazyops.py:95` `def do_lazy_dispatch(self, line)` -- Dispatch one detached task to an external agent: opencode|hermes [--in DIR] [--resume S] [--max-turns N]...
- `LazyCommandSet.do_lazy_task` (method) `cli/commands/lazyops.py:154` `def do_lazy_task(self, line)` -- Create/list/show/pause/resume/delete/spawn/queue/limit/drain tasks.
- `LazyCommandSet.do_lazy_graph` (method) `cli/commands/lazyops.py:276` `def do_lazy_graph(self, line)` -- Show planner-facing graph overview.
- `LazyCommandSet.do_lazy_context` (method) `cli/commands/lazyops.py:305` `def do_lazy_context(self, line)` -- Render the bounded prompt context the planner/worker LLMs receive.
- `LazyCommandSet.do_lazy_skill` (method) `cli/commands/lazyops.py:326` `def do_lazy_skill(self, line)` -- Skills: list|show <name>|preview|inject <name...>|clear|auto on|off|mirror [name]|register-hermes.
- `LazyCommandSet.do_lazy_workspace` (method) `cli/commands/lazyops.py:410` `def do_lazy_workspace(self, line)` -- Confined workspace files: list [path]|read <path>|write <path> <text>|mkdir <path>|rm <path>|path.
- `LazyCommandSet.do_lazy_selfupdate` (method) `cli/commands/lazyops.py:463` `def do_lazy_selfupdate(self, line)` -- Self-update: check [--branch B]|apply [--yes] [--branch B].
- `LazyCommandSet.do_lazy_planner` (method) `cli/commands/lazyops.py:491` `def do_lazy_planner(self, line)` -- Run one planner wakeup (emits 0..N intents).
- `LazyCommandSet.do_lazy_frontier` (method) `cli/commands/lazyops.py:510` `def do_lazy_frontier(self, line)` -- Show pending intent queue.
- `LazyCommandSet.do_lazy_worker` (method) `cli/commands/lazyops.py:522` `def do_lazy_worker(self, line)` -- Claim ONE intent and execute it with real tools.
- `LazyCommandSet.do_lazy_trace` (method) `cli/commands/lazyops.py:562` `def do_lazy_trace(self, line)` -- Worker trace exchange.
- `LazyCommandSet.do_lazy_broadcast` (method) `cli/commands/lazyops.py:615` `def do_lazy_broadcast(self, line)` -- Exploration timeline.
- `LazyCommandSet.do_lazy_commander` (method) `cli/commands/lazyops.py:650` `def do_lazy_commander(self, line)` -- Allocate work slices across the task fleet.
- `LazyCommandSet.do_lazy_deviations` (method) `cli/commands/lazyops.py:698` `def do_lazy_deviations(self, line)` -- List planned-versus-actual deviations.
- `LazyCommandSet.do_lazy_blindspot` (method) `cli/commands/lazyops.py:736` `def do_lazy_blindspot(self, line)` -- Review graph blindspots into hints.
- `LazyCommandSet.do_lazy_hint` (method) `cli/commands/lazyops.py:762` `def do_lazy_hint(self, line)` -- Inject steering hint.
- `LazyCommandSet.do_lazy_intent` (method) `cli/commands/lazyops.py:774` `def do_lazy_intent(self, line)` -- Inject high-priority intent.
- `LazyCommandSet.do_lazy_intent_delete` (method) `cli/commands/lazyops.py:799` `def do_lazy_intent_delete(self, line)` -- Delete an intent.
- `LazyCommandSet.do_lazy_goal` (method) `cli/commands/lazyops.py:842` `def do_lazy_goal(self, line)` -- Goals: list|set <t1;t2>|edit <id> <text>|delete <id>|prove <goal> <evidence> <reason>|met <reason>.
- `LazyCommandSet.do_lazy_constraint` (method) `cli/commands/lazyops.py:881` `def do_lazy_constraint(self, line)` -- Constraints: add <allow|deny> <text> | list.
- `LazyCommandSet.do_lazy_scope` (method) `cli/commands/lazyops.py:899` `def do_lazy_scope(self, line)` -- Scope: add <kind> <value> [reason] | list.
- `LazyCommandSet.do_lazy_todo` (method) `cli/commands/lazyops.py:917` `def do_lazy_todo(self, line)` -- Serial chain todos: add <text> | done <id> | list.
- `LazyCommandSet.do_lazy_asset` (method) `cli/commands/lazyops.py:939` `def do_lazy_asset(self, line)` -- Assets: add <kind> <value> | list [kind] | scoped [--kind K] | coverage | untested.
- `LazyCommandSet.do_lazy_enrich` (method) `cli/commands/lazyops.py:980` `def do_lazy_enrich(self, line)` -- Enrich asset with DNS/HTTP.
- `LazyCommandSet.do_lazy_traffic` (method) `cli/commands/lazyops.py:992` `def do_lazy_traffic(self, line)` -- Traffic: list|search <q>|search-host <host> [--port P]|get <digest>|body <digest>|blob <digest> [--part req|resp]...
- `LazyCommandSet.do_lazy_guard` (method) `cli/commands/lazyops.py:1213` `def do_lazy_guard(self, line)` -- Guard gate: check <cmd> | rule-add <pattern> <allow|ask|deny> [reason] | rule-del <p> | judge on|off [--fail...
- `LazyCommandSet.do_lazy_finding` (method) `cli/commands/lazyops.py:1314` `def do_lazy_finding(self, line)` -- Findings: list [--full] [--limit N]|report <name> :: <summary>|status <id> <st>|update <id> <text>|context <id>.
- `LazyCommandSet.do_lazy_retest` (method) `cli/commands/lazyops.py:1379` `def do_lazy_retest(self, line)` -- Retest finding to reproduced/fixed/inconclusive.
- `LazyCommandSet.do_lazy_steer` (method) `cli/commands/lazyops.py:1398` `def do_lazy_steer(self, line)` -- Mid-run correction.
- `LazyCommandSet.do_lazy_kill` (method) `cli/commands/lazyops.py:1410` `def do_lazy_kill(self, line)` -- Terminate running intent.
- `LazyCommandSet.do_lazy_pause` (method) `cli/commands/lazyops.py:1422` `def do_lazy_pause(self, line)` -- Pause task loops.
- `LazyCommandSet.do_lazy_resume` (method) `cli/commands/lazyops.py:1432` `def do_lazy_resume(self, line)` -- Resume paused task.
- `LazyCommandSet.do_lazy_report` (method) `cli/commands/lazyops.py:1442` `def do_lazy_report(self, line)` -- Export severity-ranked report.
- `LazyCommandSet.do_lazy_runtime` (method) `cli/commands/lazyops.py:1459` `def do_lazy_runtime(self, line)` -- Show/set loop runtime: budgets, deadline, abort cause, heartbeat, settlement text.
- `LazyCommandSet.do_lazy_payload_keys` (method) `cli/commands/lazyops.py:1506` `def do_lazy_payload_keys(self, line)` -- Show worker tool defaults injected into every probe.
- `LazyCommandSet.do_lazy_fact` (method) `cli/commands/lazyops.py:1518` `def do_lazy_fact(self, line)` -- Facts: list [query] [--hot|--cold]|add <text>.
- `LazyCommandSet.do_lazy_node` (method) `cli/commands/lazyops.py:1546` `def do_lazy_node(self, line)` -- Full node detail.
- `LazyCommandSet.do_lazy_evidence` (method) `cli/commands/lazyops.py:1566` `def do_lazy_evidence(self, line)` -- Evidence vault and frozen package.
- `LazyCommandSet.do_lazy_ask` (method) `cli/commands/lazyops.py:1633` `def do_lazy_ask(self, line)` -- Bounded side question over task context.
- `run_command` (function) `cli/commands/lazyops.py:1664` `def run_command(command)` -- Execute one shell command or LazyOwn verb and return its output.
- `list_tasks` (function) `cli/commands/lazyops.py:1686` `def list_tasks()` -- List every task with status, intents, facts and findings.
- `task_graph` (function) `cli/commands/lazyops.py:1690` `def task_graph(task)` -- Graph overview of one task (defaults to the active task).
- `task_findings` (function) `cli/commands/lazyops.py:1694` `def task_findings(task)` -- Findings of one task with severity, status and report size.
- `campaign_sitrep` (function) `cli/commands/lazyops.py:1698` `def campaign_sitrep()` -- Campaign summary: tasks, findings and phase counters.
- `add_hint` (function) `cli/commands/lazyops.py:1711` `def add_hint(text)` -- Inject an operator hint into the active task planner.
- `steer_intent` (function) `cli/commands/lazyops.py:1718` `def steer_intent(intent, message)` -- Send a mid-run course correction to a running intent.
- `LazyCommandSet.do_lazy_agent` (method) `cli/commands/lazyops.py:1787` `def do_lazy_agent(self, line)` -- Main agent with full tool calling (native backend or opencode).
- `LazyCommandSet.do_lazy_company` (method) `cli/commands/lazyops.py:1888` `def do_lazy_company(self, line)` -- Company scope: add <name> [scope]|list|match <value>.
- `LazyCommandSet.do_lazy_tool` (method) `cli/commands/lazyops.py:1910` `def do_lazy_tool(self, line)` -- Tool catalog: list [agent]|bind|unbind <agent> <tool>|custom-add <name> <command|script|http> <target> [--desc D]...
- `LazyCommandSet.do_lazy_verb` (method) `cli/commands/lazyops.py:1982` `def do_lazy_verb(self, line)` -- Loop verb admin: list [--phase P] [--q Q]|enable|disable <verb>|add <verb> --keywords K [--phase P] [--no-target]...
- `LazyCommandSet.do_lazy_stage` (method) `cli/commands/lazyops.py:2080` `def do_lazy_stage(self, line)` -- Loop stage admin: list|enable|disable <stage>|reset.
- `LazyCommandSet.do_lazy_mode` (method) `cli/commands/lazyops.py:2108` `def do_lazy_mode(self, line)` -- Engagement mode + findings/progress admin.
- `LazyCommandSet.do_lazy_addon` (method) `cli/commands/lazyops.py:2134` `def do_lazy_addon(self, line)` -- Addon trigger runner: list [service]|run <name> [--target T]|update [name|--all] [--dry-run].
- `LazyCommandSet.do_lazy_notify` (method) `cli/commands/lazyops.py:2243` `def do_lazy_notify(self, line)` -- Notify channels: list|add <log|webhook|file|slack|email> <target> [--min S] [--to a] [--from f] [--user u] [--pass...
- `LazyCommandSet.do_lazy_trigger` (method) `cli/commands/lazyops.py:2291` `def do_lazy_trigger(self, line)` -- Scheduler triggers: list|add <kind> [every_sec]|remove <id>|on <id>|off <id>|seed|policy|addons|sync.
- `LazyCommandSet.do_lazy_llm` (method) `cli/commands/lazyops.py:2380` `def do_lazy_llm(self, line)` -- LLM chain: list|add <name> [model] [--priority N]|priority <name> <N>|remove <name>|usage|health|context [N]|record...
- `LazyCommandSet.do_lazy_compact` (method) `cli/commands/lazyops.py:2517` `def do_lazy_compact(self, line)` -- Compaction: minor|major [--threshold N]|unfolded [--limit N]|overview|noa|expand <digest>.
- `LazyCommandSet.do_lazy_status` (method) `cli/commands/lazyops.py:2589` `def do_lazy_status(self, line)` -- Full task status.
- `LazyCommandSet.do_lazy_overview` (method) `cli/commands/lazyops.py:2613` `def do_lazy_overview(self, line)` -- Alias of lazy_graph.
- `LazyCommandSet.do_lazy_archive` (method) `cli/commands/lazyops.py:2618` `def do_lazy_archive(self, line)` -- Task snapshots: save [--task T]|list|stats|restore <path>.
- `LazyCommandSet.do_lazy_template` (method) `cli/commands/lazyops.py:2649` `def do_lazy_template(self, line)` -- Goal templates: list|add <name> <goal>|use <name>|remove <name>.
- `LazyCommandSet.do_lazy_category` (method) `cli/commands/lazyops.py:2680` `def do_lazy_category(self, line)` -- Task labels: set <name> [--task T]|list [name].
- `LazyCommandSet.do_lazy_chat` (method) `cli/commands/lazyops.py:2701` `def do_lazy_chat(self, line)` -- Task conversation: say <text>|log|clear|sessions.
- `LazyCommandSet.do_lazy_scheduler` (method) `cli/commands/lazyops.py:2734` `def do_lazy_scheduler(self, line)` -- Scheduler state: show|run.
- `LazyCommandSet.do_lazy_gate` (method) `cli/commands/lazyops.py:2761` `def do_lazy_gate(self, line)` -- Asset gate: list|check <target>|block-add <kind> <pattern> [note]|block-del <id>|allow-add <kind> <pattern>...
- `LazyCommandSet.do_lazy_loop` (method) `cli/commands/lazyops.py:2806` `def do_lazy_loop(self, line)` -- Run the single orchestrator: auto-invokes scope/asset/enrich/planner/frontier/worker/guard/traffic/finding/retest/com...
- `LazyCommandSet.do_lazy_sandbox` (method) `cli/commands/lazyops.py:2813` `def do_lazy_sandbox(self, line)` -- Per-task Docker sandbox: status [--task T]|up --task T [--image I]|down --task T|build|exec --task T <verb...>.
- `LazyCommandSet.do_lazy_install` (method) `cli/commands/lazyops.py:2876` `def do_lazy_install(self, line)` -- Capability installer: <tool> [--dry-run]|on|off|list.
- `LazyCommandSet.do_lazy_pacing` (method) `cli/commands/lazyops.py:2914` `def do_lazy_pacing(self, line)` -- Show or set loop pacing knobs.

## cli/commands/loop_audit.py
Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`
- `LoopAuditCommandSet.do_loop_audit` (method) `cli/commands/loop_audit.py:25` `def do_loop_audit(self, line)` -- Audit what an autonomous loop actually did.

## cli/commands/marketplace.py
Depends on: `cli/commands/_base.py`, `cli/marketplace_config.py`, `cli/plugin_tiers.py`, `modules/addon_updater.py`, `modules/module_registry.py`, `utils.py`
- `MarketplaceCommandSet.do_marketplace` (method) `cli/commands/marketplace.py:104` `def do_marketplace(self, line)` -- Discover and install community plugins, addons, and tools.
- `MarketplaceCommandSet.do_marketplace_config` (method) `cli/commands/marketplace.py:447` `def do_marketplace_config(self, line)` -- Interactive marketplace manager (Textual TUI).

## cli/commands/mcp_bridge.py
Depends on: `cli/aliases.py`, `cli/commands/_base.py`, `core/autonomous.py`, `core/config.py`, `modules/intelligence_engine.py`, `modules/lazy_runner.py`, `modules/playbook_engine.py`, `modules/session_rag.py`, `modules/threat_model.py`, `modules/world_model.py`, `skills/lazyown_facts.py`, `skills/lazyown_parquet_db.py`, `utils.py`
Imported by: `tests/test_cli_assign.py`, `tests/test_loop_auto_orchestrator.py`
- `McpBridgeCommandSet.do_auto_populate` (method) `cli/commands/mcp_bridge.py:151` `def do_auto_populate(self, args)` -- Parse the latest nmap XML scan and auto-populate payload context.
- `McpBridgeCommandSet.do_facts_show` (method) `cli/commands/mcp_bridge.py:261` `def do_facts_show(self, args)` -- Show structured facts extracted from nmap scans and tool output.
- `McpBridgeCommandSet.do_rag_query` (method) `cli/commands/mcp_bridge.py:286` `def do_rag_query(self, args)` -- Semantic search over session artefacts (scans, logs, notes).
- `McpBridgeCommandSet.do_parquet_query` (method) `cli/commands/mcp_bridge.py:316` `def do_parquet_query(self, args)` -- Query the parquet knowledge bases (GTFOBins, LOLBas, ATT&CK, sessions).
- `McpBridgeCommandSet.do_threat_model` (method) `cli/commands/mcp_bridge.py:378` `def do_threat_model(self, args)` -- Build or inspect the threat model derived from session events.
- `McpBridgeCommandSet.do_playbook_run` (method) `cli/commands/mcp_bridge.py:431` `def do_playbook_run(self, args)` -- Execute a generated YAML playbook step by step through the shell.
- `McpBridgeCommandSet.do_auto_loop` (method) `cli/commands/mcp_bridge.py:489` `def do_auto_loop(self, line)` -- Run a goal through the single lazy orchestrator (auto_loop == lazy_loop).
- `McpBridgeCommandSet.do_session_state` (method) `cli/commands/mcp_bridge.py:516` `def do_session_state(self, line)` -- Alias of ``sitrep`` kept for MCP verb parity (lazyown_session_state).
- `McpBridgeCommandSet.do_campaign_sitrep` (method) `cli/commands/mcp_bridge.py:521` `def do_campaign_sitrep(self, line)` -- Alias of ``sitrep`` kept for MCP verb parity (lazyown_campaign_sitrep).
- `McpBridgeCommandSet.do_timeline` (method) `cli/commands/mcp_bridge.py:526` `def do_timeline(self, line)` -- Alias of ``timeline_browser`` kept for MCP verb parity (lazyown_timeline).

## cli/commands/misc_migrated.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/autosuggest.py`, `cli/banner_config.py`, `cli/command_chain.py`, `cli/commands/_base.py`, `cli/dashboard_tui.py`, `cli/exploration.py`, `cli/exploration_view.py`, `cli/graph_advisor.py`, `cli/graph_overlay.py`, `cli/ops_commands.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/palette_overlay.py`, `cli/reactive_hints.py`, `cli/recommendation.py`, `cli/recommendation_signals.py`, `cli/sessions_browser.py`, `cli/show.py`, `cli/timeline_browser.py`, `cli/toast_bus.py`, `cli/wizard.py`, `core/config.py`, `core/console.py`, `core/process.py`, `core/safe_exec.py`, `modules/lazy_loop.py`, `modules/module_registry.py`, `modules/payload_factory.py`, `utils.py`
Imported by: `tests/test_auto_crypto.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_nethelpers_command_set.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`
- `MiscMigratedCommandSet.do_notify` (method) `cli/commands/misc_migrated.py:92` `def do_notify(self, arg)` -- Command to trigger a toastr-like notification.
- `MiscMigratedCommandSet.do_EOF` (method) `cli/commands/misc_migrated.py:111` `def do_EOF(self, line)` -- Handle the end-of-file (EOF) condition.
- `MiscMigratedCommandSet.do_palette` (method) `cli/commands/misc_migrated.py:179` `def do_palette(self, line)` -- Browse the operator command catalogue grouped by kill-chain phase.
- `MiscMigratedCommandSet.do_graph_search` (method) `cli/commands/misc_migrated.py:204` `def do_graph_search(self, line)` -- Fuzzy search the graphify knowledge graph for nodes by label.
- `MiscMigratedCommandSet.do_neighbors` (method) `cli/commands/misc_migrated.py:232` `def do_neighbors(self, line)` -- Show graph neighbors of a node or command from the graphify graph.
- `MiscMigratedCommandSet.do_god_nodes` (method) `cli/commands/misc_migrated.py:259` `def do_god_nodes(self, line)` -- Show the most-connected nodes ("god nodes") from the graph.
- `MiscMigratedCommandSet.do_suggest_next` (method) `cli/commands/misc_migrated.py:278` `def do_suggest_next(self, line)` -- Suggest next commands by walking the graph from recent activity.
- `MiscMigratedCommandSet.do_recommend_next` (method) `cli/commands/misc_migrated.py:404` `def do_recommend_next(self, line)` -- Recommend the next action via the unified recommendation engine.
- `MiscMigratedCommandSet.do_explore` (method) `cli/commands/misc_migrated.py:458` `def do_explore(self, line)` -- Show exploration coverage and addon/tool suggestions per service.
- `MiscMigratedCommandSet.do_prev` (method) `cli/commands/misc_migrated.py:489` `def do_prev(self, line)` -- Show prerequisite commands for a verb (the chain's ``prev`` arrow).
- `MiscMigratedCommandSet.do_dashboard` (method) `cli/commands/misc_migrated.py:526` `def do_dashboard(self, line)` -- Launch the full-screen LazyOwn operator dashboard (Textual TUI).
- `MiscMigratedCommandSet.do_palette_k` (method) `cli/commands/misc_migrated.py:561` `def do_palette_k(self, line)` -- Open the fuzzy Command-K palette overlay.
- `MiscMigratedCommandSet.do_browse` (method) `cli/commands/misc_migrated.py:590` `def do_browse(self, line)` -- Open the sessions/ TUI browser.
- `MiscMigratedCommandSet.do_timeline_browser` (method) `cli/commands/misc_migrated.py:612` `def do_timeline_browser(self, line)` -- Open the timeline scrubber over the session report CSV.
- `MiscMigratedCommandSet.do_graph_overlay` (method) `cli/commands/misc_migrated.py:631` `def do_graph_overlay(self, line)` -- Open the graph overlay over the graphify knowledge graph.
- `MiscMigratedCommandSet.do_toast_clear` (method) `cli/commands/misc_migrated.py:651` `def do_toast_clear(self, line)` -- Mark every pending toast event as seen without printing them.
- `MiscMigratedCommandSet.do_exit` (method) `cli/commands/misc_migrated.py:671` `def do_exit(self, arg)` -- Exit the command line interface.
- `MiscMigratedCommandSet.do_banner` (method) `cli/commands/misc_migrated.py:744` `def do_banner(self, line)` -- Show the banner
- `MiscMigratedCommandSet.do_config_banner` (method) `cli/commands/misc_migrated.py:754` `def do_config_banner(self, line)` -- Open a Powerlevel10k-style wizard to toggle prompt segments.
- `MiscMigratedCommandSet.do_aliass` (method) `cli/commands/misc_migrated.py:798` `def do_aliass(self, line)` -- Prints all configured aliases and their associated commands.
- `MiscMigratedCommandSet.do_graph` (method) `cli/commands/misc_migrated.py:826` `def do_graph(self, line)` -- Generates a graph from JSON payload files containing URL, RHOST, and RPORT.
- `MiscMigratedCommandSet.do_h` (method) `cli/commands/misc_migrated.py:886` `def do_h(self, arg)` -- Open a new window within a tmux session using the LazyOwn RedTeam Framework.
- `MiscMigratedCommandSet.do_v` (method) `cli/commands/misc_migrated.py:932` `def do_v(self, arg)` -- Open a new window within a tmux session using the LazyOwn RedTeam Framework.
- `MiscMigratedCommandSet.do_links` (method) `cli/commands/misc_migrated.py:978` `def do_links(self, line)` -- Displays a list of useful links and allows the user to select and copy a link to the clipboard.
- `MiscMigratedCommandSet.do_news` (method) `cli/commands/misc_migrated.py:1041` `def do_news(self, line)` -- Show the Hacker News in the terminal.
- `MiscMigratedCommandSet.do_check_update` (method) `cli/commands/misc_migrated.py:1054` `def do_check_update(self, line)` -- Checks for updates by comparing the local version with the remote version.
- `MiscMigratedCommandSet.do_addalias` (method) `cli/commands/misc_migrated.py:1099` `def do_addalias(self, arglist)` -- Add a new alias with support for placeholders like {rhost}, {lhost}, {lport}, etc.
- `MiscMigratedCommandSet.do_listaliases` (method) `cli/commands/misc_migrated.py:1151` `def do_listaliases(self, _)` -- List all available aliases.

## cli/commands/mobile_macos.py
Depends on: `cli/commands/_base.py`, `core/process.py`, `core/validators.py`, `utils.py`
- `MobileMacOSCommandSet.do_android_enum` (method) `cli/commands/mobile_macos.py:103` `def do_android_enum(self, line)` -- Enumerate an Android device connected via ADB.
- `MobileMacOSCommandSet.do_android_apk` (method) `cli/commands/mobile_macos.py:171` `def do_android_apk(self, line)` -- Generate a malicious APK with reverse shell payload.
- `MobileMacOSCommandSet.do_macos_persist` (method) `cli/commands/mobile_macos.py:216` `def do_macos_persist(self, line)` -- Generate macOS persistence via LaunchAgent.
- `MobileMacOSCommandSet.do_macos_keychain` (method) `cli/commands/mobile_macos.py:274` `def do_macos_keychain(self, line)` -- Extract secrets from the macOS Keychain.
- `MobileMacOSCommandSet.do_macos_tcc` (method) `cli/commands/mobile_macos.py:323` `def do_macos_tcc(self, line)` -- Generate macOS TCC (Transparency, Consent, Control) bypass.
- `is_binary_present` (function) `cli/commands/mobile_macos.py:374` `def is_binary_present(name)` -- Check if a binary is available on PATH, delegates to core.

## cli/commands/module_manager.py
Depends on: `cli/commands/_base.py`, `modules/module_registry.py`, `utils.py`
- `ModuleManagerCommandSet.do_search` (method) `cli/commands/module_manager.py:71` `def do_search(self, line)` -- Search for modules by name, description, or author.
- `ModuleManagerCommandSet.do_use` (method) `cli/commands/module_manager.py:111` `def do_use(self, line)` -- Select a module to work with.
- `ModuleManagerCommandSet.do_back` (method) `cli/commands/module_manager.py:162` `def do_back(self, line)` -- Leave the current module context.

## cli/commands/netattack.py
Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `modules/loop_triggers.py`, `modules/world_model.py`, `utils.py`
- `NetAttackCommandSet.do_lazy_netattack` (method) `cli/commands/netattack.py:59` `def do_lazy_netattack(self, line)` -- Windows net-attack surface: grade + exact commands; never executes.

## cli/commands/nethelpers.py
Depends on: `cli/commands/_base.py`, `core/hardening.py`, `utils.py`
Imported by: `tests/test_nethelpers_command_set.py`
- `NetworkHelpersCommandSet.do_ip` (method) `cli/commands/nethelpers.py:38` `def do_ip(self, line)` -- Displays IP addresses of network interfaces and copies the IP address from the `tun0` interface to the clipboard.
- `NetworkHelpersCommandSet.do_ipp` (method) `cli/commands/nethelpers.py:120` `def do_ipp(self, line)` -- Displays IP addresses of network interfaces and prints the IP address from the `tun0` interface.
- `NetworkHelpersCommandSet.do_rhost` (method) `cli/commands/nethelpers.py:201` `def do_rhost(self, line)` -- Copies the remote host (self.params['rhost']) to the clipboard and updates the command prompt.
- `NetworkHelpersCommandSet.do_rrhost` (method) `cli/commands/nethelpers.py:254` `def do_rrhost(self, line)` -- Updates the command prompt to include the remote host (self.params['rhost']) and current working directory.
- `NetworkHelpersCommandSet.do_addhosts` (method) `cli/commands/nethelpers.py:295` `def do_addhosts(self, line)` -- Adds an entry to the `/etc/hosts` file, mapping an IP address to a domain name.
- `NetworkHelpersCommandSet.do_ip2asn` (method) `cli/commands/nethelpers.py:319` `def do_ip2asn(self, line)` -- Command to get ASN for a given IP address.
- `NetworkHelpersCommandSet.do_ignorearp` (method) `cli/commands/nethelpers.py:348` `def do_ignorearp(self, line)` -- Configures the system to ignore ARP requests by setting a kernel parameter.
- `NetworkHelpersCommandSet.do_ignoreicmp` (method) `cli/commands/nethelpers.py:383` `def do_ignoreicmp(self, line)` -- Configures the system to ignore ICMP echo requests by setting a kernel parameter.
- `NetworkHelpersCommandSet.do_acknowledgearp` (method) `cli/commands/nethelpers.py:418` `def do_acknowledgearp(self, line)` -- Configures the system to acknowledge ARP requests by setting a kernel parameter.
- `NetworkHelpersCommandSet.do_acknowledgeicmp` (method) `cli/commands/nethelpers.py:453` `def do_acknowledgeicmp(self, line)` -- Configures the system to respond to ICMP echo requests by setting a kernel parameter.

## cli/commands/opsec_cleanup.py
Depends on: `cli/commands/_base.py`, `modules/forensic_cleaner.py`, `modules/log_tamper.py`, `modules/memory_cleaner.py`, `modules/network_opsec.py`, `modules/opsec_scorer.py`, `modules/timestomper.py`
- `OpsecCleanupCommandSet.do_opsec_score` (method) `cli/commands/opsec_cleanup.py:25` `def do_opsec_score(self, line)` -- Real-time OPSEC risk assessment with contextual action gating (v2).
- `OpsecCleanupCommandSet.do_log_tamper` (method) `cli/commands/opsec_cleanup.py:97` `def do_log_tamper(self, line)` -- Cross-platform log clearing commands.
- `OpsecCleanupCommandSet.do_forensic_clean` (method) `cli/commands/opsec_cleanup.py:162` `def do_forensic_clean(self, line)` -- Clean forensic artifacts — Prefetch, Shimcache, Amcache, Jump Lists, etc.
- `OpsecCleanupCommandSet.do_timestomp` (method) `cli/commands/opsec_cleanup.py:219` `def do_timestomp(self, line)` -- Manipulate file MACB timestamps to evade forensic timeline analysis.
- `OpsecCleanupCommandSet.do_memory_clean` (method) `cli/commands/opsec_cleanup.py:288` `def do_memory_clean(self, line)` -- Clean memory artifacts — Kerberos tickets, clipboard, env vars, credentials.
- `OpsecCleanupCommandSet.do_network_opsec` (method) `cli/commands/opsec_cleanup.py:342` `def do_network_opsec(self, line)` -- Network OPSEC — proxy chains, DoH, canary detection, traffic analysis.
- `OpsecCleanupCommandSet.do_auditd_disable` (method) `cli/commands/opsec_cleanup.py:445` `def do_auditd_disable(self, line)` -- Generate commands to disable Linux auditd.
- `OpsecCleanupCommandSet.do_sysmon_disable` (method) `cli/commands/opsec_cleanup.py:468` `def do_sysmon_disable(self, line)` -- Generate commands to disable Windows Sysmon.

## cli/commands/orchestration.py
Depends on: `cli/commands/_base.py`, `cli/reasoning_stream.py`, `core/console.py`
Imported by: `tests/test_improvements_spec.py`
- `run_with_spinner` (function) `cli/commands/orchestration.py:94` `def run_with_spinner(execute)` -- Run a blocking orchestrator call with a live reasoning spinner.
- `OrchestrationCommandSet.do_status_bar` (method) `cli/commands/orchestration.py:190` `def do_status_bar(self, args)` -- Inspect, toggle and refresh the prompt status bar.
- `OrchestrationCommandSet.do_orchestrate` (method) `cli/commands/orchestration.py:216` `def do_orchestrate(self, args)` -- Route a goal through the unified orchestrator and print the result.

## cli/commands/params_ops.py
Depends on: `cli/assign.py`, `cli/commands/_base.py`, `core/config.py`, `core/param_registry.py`, `core/payload_schema.py`, `utils.py`
Imported by: `tests/test_param_registry.py`
- `ParamCommandSet.do_param` (method) `cli/commands/params_ops.py:38` `def do_param(self, line)` -- Manage the shared parameter catalog used by addons and aliases.

## cli/commands/payload_arsenal.py
Depends on: `cli/commands/_base.py`, `modules/dotnet_payload.py`, `modules/linux_advanced_payloads.py`, `modules/macos_payloads.py`, `modules/polymorphic_engine.py`, `modules/staged_delivery.py`
- `PayloadArsenalCommandSet.do_dotnet_payload` (method) `cli/commands/payload_arsenal.py:29` `def do_dotnet_payload(self, line)` -- Generate a .NET/C# payload.
- `PayloadArsenalCommandSet.do_arsenal_show` (method) `cli/commands/payload_arsenal.py:114` `def do_arsenal_show(self, line)` -- Show payload arsenal items.
- `PayloadArsenalCommandSet.do_staged_delivery` (method) `cli/commands/payload_arsenal.py:172` `def do_staged_delivery(self, line)` -- Generate staged delivery artifacts (HTA, VBA, LNK, ISO, VHD).
- `PayloadArsenalCommandSet.do_polymorphic` (method) `cli/commands/payload_arsenal.py:261` `def do_polymorphic(self, line)` -- Apply polymorphic mutation to shellcode.
- `PayloadArsenalCommandSet.do_macos_payload` (method) `cli/commands/payload_arsenal.py:328` `def do_macos_payload(self, line)` -- Generate macOS payloads (.app bundles, persistence, TCC bypass).
- `PayloadArsenalCommandSet.do_linux_advanced_payload` (method) `cli/commands/payload_arsenal.py:401` `def do_linux_advanced_payload(self, line)` -- Generate advanced Linux payloads (LD_PRELOAD, eBPF, PAM, kernel module).

## cli/commands/payload_generation.py
Depends on: `cli/commands/_base.py`, `modules/payload_factory.py`, `utils.py`
- `PayloadCommandSet.do_generate` (method) `cli/commands/payload_generation.py:37` `def do_generate(self, line)` -- Generate a payload.

## cli/commands/persist.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `PersistenceCommandSet.do_createwebshell` (method) `cli/commands/persist.py:31` `def do_createwebshell(self, line)` -- Create web shells (JPG-disguised PHP, p0wny-shell, ASP).
- `PersistenceCommandSet.do_createrevshell` (method) `cli/commands/persist.py:45` `def do_createrevshell(self, line)` -- Create a bash reverse shell script in sessions/.
- `PersistenceCommandSet.do_createwinrevshell` (method) `cli/commands/persist.py:59` `def do_createwinrevshell(self, line)` -- Create a Windows reverse shell (PowerShell).
- `PersistenceCommandSet.do_conptyshell` (method) `cli/commands/persist.py:71` `def do_conptyshell(self, line)` -- Download ConPtyShell and prepare a PowerShell run command.
- `PersistenceCommandSet.do_pwncatcs` (method) `cli/commands/persist.py:87` `def do_pwncatcs(self, line)` -- Start a pwncat-cs reverse shell listener.
- `PersistenceCommandSet.do_revwin` (method) `cli/commands/persist.py:97` `def do_revwin(self, line)` -- Create a Windows reverse shell executable.
- `PersistenceCommandSet.do_wmi_persist` (method) `cli/commands/persist.py:110` `def do_wmi_persist(self, line)` -- Create WMI Event Subscription persistence (fileless, no disk write).
- `PersistenceCommandSet.do_wmi_lateral` (method) `cli/commands/persist.py:168` `def do_wmi_lateral(self, line)` -- Execute a command on a remote host via WMI.
- `PersistenceCommandSet.do_wmi_scheduled_task` (method) `cli/commands/persist.py:207` `def do_wmi_scheduled_task(self, line)` -- Create a scheduled task for persistence via WMI.

## cli/commands/persist_migrated.py
Depends on: `cli/assign.py`, `cli/commands/_base.py`, `core/config.py`, `core/hardening.py`, `modules/traffic_morpher.py`, `utils.py`
Imported by: `tests/test_backdoor_random.py`
- `PersistMigratedCommandSet.generate_backdoor_username` (method) `cli/commands/persist_migrated.py:37` `def generate_backdoor_username()` -- Generate a random backdoor username (same shape as C2 operators).
- `PersistMigratedCommandSet.generate_backdoor_password` (method) `cli/commands/persist_migrated.py:43` `def generate_backdoor_password()` -- Generate a random backdoor password safe for assign, chpasswd and CLIs.
- `PersistMigratedCommandSet.resolve_backdoor_creds` (method) `cli/commands/persist_migrated.py:53` `def resolve_backdoor_creds(params)` -- Return configured creds, or fresh random ones when unset.
- `PersistMigratedCommandSet.do_pwncat` (method) `cli/commands/persist_migrated.py:91` `def do_pwncat(self, line)` -- Runs `pwncat` with the specified port for listening.
- `PersistMigratedCommandSet.do_ftp` (method) `cli/commands/persist_migrated.py:135` `def do_ftp(self, line)` -- Connects to an ftp host using credentials from a file and a specified port.
- `PersistMigratedCommandSet.do_rdp` (method) `cli/commands/persist_migrated.py:194` `def do_rdp(self, line)` -- Reads credentials from a file, encrypts the password, and executes the RDP connection command.
- `PersistMigratedCommandSet.do_grisun0` (method) `cli/commands/persist_migrated.py:268` `def do_grisun0(self, line)` -- Creates and copies a shell command to add a new user, assign a password, add the user to the sudo group, and switch...
- `PersistMigratedCommandSet.do_grisun0w` (method) `cli/commands/persist_migrated.py:312` `def do_grisun0w(self, line)` -- Creates and copies a PowerShell command to add a new user, assign a password, add the user to the Administrators...
- `PersistMigratedCommandSet.do_asprevbase64` (method) `cli/commands/persist_migrated.py:354` `def do_asprevbase64(self, line)` -- Creates a base64 encoded ASP reverse shell payload and copies it to the clipboard.
- `PersistMigratedCommandSet.do_weevelygen` (method) `cli/commands/persist_migrated.py:392` `def do_weevelygen(self, line)` -- Generate a PHP backdoor using Weevely, protected with the given password.
- `PersistMigratedCommandSet.do_weevely` (method) `cli/commands/persist_migrated.py:432` `def do_weevely(self, line)` -- Connect to PHP backdoor using Weevely, protected with the given password.
- `PersistMigratedCommandSet.do_backdoor_factory` (method) `cli/commands/persist_migrated.py:478` `def do_backdoor_factory(self, line)` -- Creates a backdoored executable using `backdoor-factory`.
- `PersistMigratedCommandSet.do_msfpc` (method) `cli/commands/persist_migrated.py:524` `def do_msfpc(self, line)` -- Generates payloads using MSFvenom Payload Creator (MSFPC).
- `PersistMigratedCommandSet.do_ivy` (method) `cli/commands/persist_migrated.py:605` `def do_ivy(self, line)` -- Generates payloads using Ivy with various options.
- `PersistMigratedCommandSet.do_veil` (method) `cli/commands/persist_migrated.py:705` `def do_veil(self, line)` -- Generates payloads using Veil-Evasion with various options.
- `PersistMigratedCommandSet.do_scarecrow` (method) `cli/commands/persist_migrated.py:779` `def do_scarecrow(self, line)` -- Executes ScareCrow with various options for bypassing EDR solutions and executing shellcode. to create the...
- `PersistMigratedCommandSet.do_generate_revshell` (method) `cli/commands/persist_migrated.py:897` `def do_generate_revshell(self, line)` -- Generate a reverse shell in various programming languages.
- `PersistMigratedCommandSet.do_dr0p1t` (method) `cli/commands/persist_migrated.py:963` `def do_dr0p1t(self, line)` -- Execute the Dr0p1t tool to create a stealthy malware dropper.
- `PersistMigratedCommandSet.do_paranoid_meterpreter` (method) `cli/commands/persist_migrated.py:1026` `def do_paranoid_meterpreter(self, line)` -- Creates and deploys a paranoid Meterpreter payload and listener with SSL/TLS pinning and UUID tracking.
- `PersistMigratedCommandSet.do_setoolKits` (method) `cli/commands/persist_migrated.py:1114` `def do_setoolKits(self, line)` -- Executes the SEToolKit workflow to generate a Meterpreter payload and configure the multi-handler using LHOST and...
- `PersistMigratedCommandSet.do_darkarmour` (method) `cli/commands/persist_migrated.py:1147` `def do_darkarmour(self, line)` -- Uses the darkarmour tool to generate an obfuscated version of a PE executable.
- `PersistMigratedCommandSet.do_knokknok` (method) `cli/commands/persist_migrated.py:1215` `def do_knokknok(self, line)` -- Send special string to trigger a reverse shell, with the command 'c2 client_name' create a listener shell script to...
- `PersistMigratedCommandSet.do_listener_go` (method) `cli/commands/persist_migrated.py:1250` `def do_listener_go(self, line)` -- Configures and starts a listener for a specified victim.
- `PersistMigratedCommandSet.do_listener_py` (method) `cli/commands/persist_migrated.py:1317` `def do_listener_py(self, line)` -- Configures and starts a listener for a specified victim.
- `PersistMigratedCommandSet.do_service` (method) `cli/commands/persist_migrated.py:1384` `def do_service(self, line)` -- Creates a systemd service file for a specified binary and generates a script to enable and start the service.
- `PersistMigratedCommandSet.do_toctoc` (method) `cli/commands/persist_migrated.py:1457` `def do_toctoc(self, line)` -- Sends a magic packet to the Chinese malware.
- `PersistMigratedCommandSet.do_beaconcfg` (method) `cli/commands/persist_migrated.py:1480` `def do_beaconcfg(self, line)` -- Generate a C2 beacon profile with traffic morphing and domain fronting.

## cli/commands/phishing_wizard.py
Depends on: `cli/commands/_base.py`, `modules/backdoor/server.c`, `modules/phishing_orchestrator.py`, `utils.py`
- `PhishingWizardCommandSet.do_phish_wizard` (method) `cli/commands/phishing_wizard.py:190` `def do_phish_wizard(self, line)` -- Interactive end-to-end phishing campaign wizard.
- `PhishingWizardCommandSet.do_phish_serve` (method) `cli/commands/phishing_wizard.py:361` `def do_phish_serve(self, line)` -- Start a lightweight HTTP server for phishing landing pages.
- `PhishingHandler.log_message` (method) `cli/commands/phishing_wizard.py:389` `def log_message(self, format)`
- `PhishingHandler.do_GET` (method) `cli/commands/phishing_wizard.py:392` `def do_GET(self)`
- `PhishingHandler.do_POST` (method) `cli/commands/phishing_wizard.py:407` `def do_POST(self)`
- `PhishingHandler.do_OPTIONS` (method) `cli/commands/phishing_wizard.py:427` `def do_OPTIONS(self)`
- `PhishingHandler.do_phish_report` (method) `cli/commands/phishing_wizard.py:443` `def do_phish_report(self, line)` -- Show campaign results and captured credentials.
- `do_phisher` (function) `cli/commands/phishing_wizard.py:637` `def do_phisher(self, line)` -- Launch a phishing campaign against a target domain.

## cli/commands/pivoting.py
Depends on: `cli/commands/_base.py`, `core/hardening.py`, `utils.py`
- `PivotingCommandSet.do_autopivot` (method) `cli/commands/pivoting.py:44` `def do_autopivot(self, line)` -- Auto-detect internal networks and set up pivot tunnels.
- `PivotingCommandSet.do_pivot_status` (method) `cli/commands/pivoting.py:118` `def do_pivot_status(self, line)` -- Show the current pivot chain state.
- `PivotingCommandSet.do_pivot_kill` (method) `cli/commands/pivoting.py:137` `def do_pivot_kill(self, line)` -- Kill all pivot tunnels and clean up.
- `PivotingCommandSet.do_pivot_scan` (method) `cli/commands/pivoting.py:171` `def do_pivot_scan(self, line)` -- Scan internal networks through the current pivot chain.
- `PivotingCommandSet.do_pivot_proxy` (method) `cli/commands/pivoting.py:224` `def do_pivot_proxy(self, line)` -- Start a local SOCKS proxy through the pivot chain.

## cli/commands/postexp.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `PostExploitationCommandSet.do_lazywebshell` (method) `cli/commands/postexp.py:29` `def do_lazywebshell(self, line)` -- Run LazyOwn webshell server on port 8888.
- `PostExploitationCommandSet.do_disableav` (method) `cli/commands/postexp.py:42` `def do_disableav(self, line)` -- Create a VBS script to attempt disabling Windows Defender.
- `PostExploitationCommandSet.do_mimikatzpy` (method) `cli/commands/postexp.py:56` `def do_mimikatzpy(self, line)` -- Run Mimikatz over Python (impacket style).
- `PostExploitationCommandSet.do_scavenger` (method) `cli/commands/postexp.py:61` `def do_scavenger(self, line)` -- Run the Scavenger post-exploitation data collector.
- `PostExploitationCommandSet.do_follina` (method) `cli/commands/postexp.py:66` `def do_follina(self, line)` -- Run the Follina (CVE-2022-30190) exploit setup.
- `PostExploitationCommandSet.do_shellcode` (method) `cli/commands/postexp.py:71` `def do_shellcode(self, line)` -- Generate and manage shellcode.
- `PostExploitationCommandSet.do_ofuscatorps1` (method) `cli/commands/postexp.py:79` `def do_ofuscatorps1(self, line)` -- Obfuscate a PowerShell script.
- `PostExploitationCommandSet.do_atomic_lazyown` (method) `cli/commands/postexp.py:84` `def do_atomic_lazyown(self, line)` -- Execute atomic red-team tests via LazyOwn.

## cli/commands/postexp_migrated.py
Depends on: `cli/commands/_base.py`, `modules/yara_scanner.py`, `utils.py`
- `PostexpMigratedCommandSet.do_find` (method) `cli/commands/postexp_migrated.py:37` `def do_find(self, line)` -- Automates command execution based on a list of aliases and commands.
- `PostexpMigratedCommandSet.do_cports` (method) `cli/commands/postexp_migrated.py:533` `def do_cports(self, line)` -- Generates a command to display TCP and UDP ports and copies it to the clipboard.
- `PostexpMigratedCommandSet.do_rubeus` (method) `cli/commands/postexp_migrated.py:578` `def do_rubeus(self, line)` -- Copies a command to the clipboard for downloading and running Rubeus.
- `PostexpMigratedCommandSet.do_sessionsshstrace` (method) `cli/commands/postexp_migrated.py:618` `def do_sessionsshstrace(self, line)` -- Attach strace to a running process and log output to a file.
- `PostexpMigratedCommandSet.do_powershell_cmd_stager` (method) `cli/commands/postexp_migrated.py:669` `def do_powershell_cmd_stager(self, line)` -- Generate and execute a PowerShell command stager to run a .ps1 script.
- `PostexpMigratedCommandSet.do_shellcode_search` (method) `cli/commands/postexp_migrated.py:706` `def do_shellcode_search(self, line)` -- Search the shell-storm API for shellcodes using the provided keywords.
- `PostexpMigratedCommandSet.do_shellcode2sylk` (method) `cli/commands/postexp_migrated.py:754` `def do_shellcode2sylk(self, line)` -- Converts shellcode to SYLK format and saves the result to a file.
- `PostexpMigratedCommandSet.do_pezorsh` (method) `cli/commands/postexp_migrated.py:799` `def do_pezorsh(self, line)` -- Executes the PEzor tool to pack executables or shellcode with custom configurations.
- `PostexpMigratedCommandSet.do_pip_repo` (method) `cli/commands/postexp_migrated.py:872` `def do_pip_repo(self, line)` -- Sets up a local pip repository to serve Python packages for installation on a compromised machine without internet...
- `PostexpMigratedCommandSet.do_apt_repo` (method) `cli/commands/postexp_migrated.py:984` `def do_apt_repo(self, line)` -- Creates a comprehensive local APT repository with enhanced dependency resolution.
- `resolve_and_download_dependencies` (function) `cli/commands/postexp_migrated.py:1030` `def resolve_and_download_dependencies(package_name)` -- Recursively resolve and download package dependencies with enhanced checks
- `PostexpMigratedCommandSet.do_createpayload` (method) `cli/commands/postexp_migrated.py:1233` `def do_createpayload(self, line)` -- Generates an obfuscated payload to evade AV detection using the payloadGenerator tool. thanks to smokeme
- `PostexpMigratedCommandSet.do_bin2shellcode` (method) `cli/commands/postexp_migrated.py:1285` `def do_bin2shellcode(self, line)` -- Converts a binary file to a shellcode string in C or Nim format.
- `PostexpMigratedCommandSet.do_exe2bin` (method) `cli/commands/postexp_migrated.py:1375` `def do_exe2bin(self, line)` -- Trasnform file .exe into binary file.
- `PostexpMigratedCommandSet.do_exe2donutbin` (method) `cli/commands/postexp_migrated.py:1402` `def do_exe2donutbin(self, line)` -- Trasnform file .exe into donut binary file.
- `PostexpMigratedCommandSet.do_issue_command_to_c2` (method) `cli/commands/postexp_migrated.py:1426` `def do_issue_command_to_c2(self, line)` -- Exec command in the client using the C2. download: command you must put the file in sessions/temp_upload or use...
- `PostexpMigratedCommandSet.do_d3monizedshell` (method) `cli/commands/postexp_migrated.py:1450` `def do_d3monizedshell(self, line)` -- Executes the D3m0n1z3dShell tool for persistence in Linux.
- `PostexpMigratedCommandSet.do_scp` (method) `cli/commands/postexp_migrated.py:1483` `def do_scp(self, line)` -- Copies the local "sessions" directory to a remote host using scp, leveraging sshpass for automated authentication.
- `PostexpMigratedCommandSet.do_apt_proxy` (method) `cli/commands/postexp_migrated.py:1579` `def do_apt_proxy(self, line)` -- Configures the local machine with internet access to act as an APT proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_pip_proxy` (method) `cli/commands/postexp_migrated.py:1635` `def do_pip_proxy(self, line)` -- Configures the local machine with internet access to act as a pip proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_internet_proxy` (method) `cli/commands/postexp_migrated.py:1693` `def do_internet_proxy(self, line)` -- Configures the local machine with internet access to act as a proxy for a machine without internet access.
- `PostexpMigratedCommandSet.do_shellcode2elf` (method) `cli/commands/postexp_migrated.py:1755` `def do_shellcode2elf(self, line)` -- Convert shellcode into an ELF file and infect it.
- `PostexpMigratedCommandSet.do_ssh_cmd` (method) `cli/commands/postexp_migrated.py:1837` `def do_ssh_cmd(self, line)` -- Perform Remote Execution Command through SSH using configured start_user.
- `PostexpMigratedCommandSet.do_service_ssh` (method) `cli/commands/postexp_migrated.py:1866` `def do_service_ssh(self, line)` -- Creates a systemd service file for a specified binary and generates a script to enable and start the service.
- `PostexpMigratedCommandSet.do_ofuscatesh` (method) `cli/commands/postexp_migrated.py:1940` `def do_ofuscatesh(self, line)` -- Obfuscates a shell script by encoding it in Base64 and prepares a command to decode and execute it.
- `PostexpMigratedCommandSet.do_ofuscate_payload` (method) `cli/commands/postexp_migrated.py:1970` `def do_ofuscate_payload(self, line)` -- Obfuscates a shell script by encoding it in Base64 and prepares a command to decode and execute it.
- `PostexpMigratedCommandSet.do_adversary` (method) `cli/commands/postexp_migrated.py:1997` `def do_adversary(self, line)` -- LazyOwn RedTeam Adversary Emulator, you can configure your own adversaries in adversary.json
- `PostexpMigratedCommandSet.do_ofuscate_string` (method) `cli/commands/postexp_migrated.py:2145` `def do_ofuscate_string(self, line)` -- Ofuscate a string into Go code.
- `PostexpMigratedCommandSet.do_path2hex` (method) `cli/commands/postexp_migrated.py:2187` `def do_path2hex(self, line)` -- Convert a binary path to x64 little-endian hex code for shellcode injection.
- `PostexpMigratedCommandSet.do_hex2shellcode` (method) `cli/commands/postexp_migrated.py:2234` `def do_hex2shellcode(self, line)` -- Convert raw hex payload from msfvenom into NASM-compatible shellcode format.
- `PostexpMigratedCommandSet.do_create_synthetic` (method) `cli/commands/postexp_migrated.py:2291` `def do_create_synthetic(self, line)` -- Create a basic synthetic playbook from Nmap CSV when LLM fails.
- `PostexpMigratedCommandSet.do_extract_yaml` (method) `cli/commands/postexp_migrated.py:2343` `def do_extract_yaml(self, line)` -- Extract YAML from an existing debug file and try to create a playbook.
- `PostexpMigratedCommandSet.do_convert_remcomsvc_from_file` (method) `cli/commands/postexp_migrated.py:2405` `def do_convert_remcomsvc_from_file(self, arg)` -- Converts the Python REMCOMSVC byte string from remcomsvc.py to Golang byte slice format, prints a sample, and saves...
- `PostexpMigratedCommandSet.do_adversary_yaml` (method) `cli/commands/postexp_migrated.py:2439` `def do_adversary_yaml(self, line)` -- Execute adversary from YAML in lazyadversaries/*.yaml Syntax: adversary [id] [l|r|n]
- `PostexpMigratedCommandSet.do_add2find` (method) `cli/commands/postexp_migrated.py:2524` `def do_add2find(self, line)` -- Add a new custom command to the 'find' system, saved in user_commands.json.
- `PostexpMigratedCommandSet.do_rmfromfind` (method) `cli/commands/postexp_migrated.py:2552` `def do_rmfromfind(self, line)` -- Remove a custom command by index (as shown in 'find').
- `PostexpMigratedCommandSet.do_aes_pe` (method) `cli/commands/postexp_migrated.py:2581` `def do_aes_pe(self, line)` -- Encrypt with AES and random key to PE EXE file, to usage with loaders.
- `PostexpMigratedCommandSet.do_yara_scan` (method) `cli/commands/postexp_migrated.py:2610` `def do_yara_scan(self, line)` -- Scan files or directories with YARA rules for malware/IOCs.

## cli/commands/privilege_escalation.py
Depends on: `cli/commands/_base.py`, `modules/world_model.py`, `utils.py`
Imported by: `tests/test_shell_semantics.py`
- `PrivilegeEscalationCommandSet.do_smbserver` (method) `cli/commands/privilege_escalation.py:133` `def do_smbserver(self, line)` -- Stand up an Impacket SMB server with three relay variants.
- `PrivilegeEscalationCommandSet.do_responder` (method) `cli/commands/privilege_escalation.py:191` `def do_responder(self, line)` -- Run Responder on the configured ``device`` with elevated privileges.
- `PrivilegeEscalationCommandSet.do_sudo` (method) `cli/commands/privilege_escalation.py:216` `def do_sudo(self, line)` -- Re-launch the framework with root privileges when missing.
- `PrivilegeEscalationCommandSet.do_linpeas` (method) `cli/commands/privilege_escalation.py:229` `def do_linpeas(self, line)` -- Serve ``linpeas.sh`` over HTTP and print the target one-liner.
- `PrivilegeEscalationCommandSet.do_winpeas` (method) `cli/commands/privilege_escalation.py:265` `def do_winpeas(self, line)` -- Serve a winPEAS variant over HTTP and print the target one-liner.
- `PrivilegeEscalationCommandSet.do_les` (method) `cli/commands/privilege_escalation.py:304` `def do_les(self, line)` -- Run Linux Exploit Suggester against a kernel version.
- `PrivilegeEscalationCommandSet.do_suid_check` (method) `cli/commands/privilege_escalation.py:344` `def do_suid_check(self, line)` -- Print SUID/SGID enumeration commands ready to paste on the target.
- `PrivilegeEscalationCommandSet.do_pspy` (method) `cli/commands/privilege_escalation.py:363` `def do_pspy(self, line)` -- Serve the ``pspy`` process monitor over HTTP.
- `PrivilegeEscalationCommandSet.do_gtfo` (method) `cli/commands/privilege_escalation.py:397` `def do_gtfo(self, line)` -- Look up a binary in GTFOBins and LOLBas parquet knowledge bases.
- `PrivilegeEscalationCommandSet.do_whoami_priv` (method) `cli/commands/privilege_escalation.py:444` `def do_whoami_priv(self, line)` -- Print privilege enumeration commands for the target OS.
- `PrivilegeEscalationCommandSet.do_sudo_privesc` (method) `cli/commands/privilege_escalation.py:506` `def do_sudo_privesc(self, line)` -- Analyse sudo -l output and cross-reference with GTFOBins.
- `PrivilegeEscalationCommandSet.do_printspoofer` (method) `cli/commands/privilege_escalation.py:604` `def do_printspoofer(self, line)` -- Serve PrintSpoofer over HTTP for Windows privilege escalation.
- `PrivilegeEscalationCommandSet.do_juicypotato` (method) `cli/commands/privilege_escalation.py:626` `def do_juicypotato(self, line)` -- Serve JuicyPotato over HTTP for Windows privilege escalation.
- `PrivilegeEscalationCommandSet.do_privesc_cmd_by_os` (method) `cli/commands/privilege_escalation.py:749` `def do_privesc_cmd_by_os(self, line)` -- Prepare and send a linpeas/winpeas command to a C2 client.

## cli/commands/purple_team.py
Depends on: `cli/commands/_base.py`, `cli/purple_tui.py`, `core/config.py`, `modules/auto_purple.py`
- `PurpleTeamCommandSet.do_purple_exec` (method) `cli/commands/purple_team.py:144` `def do_purple_exec(self, line)` -- Execute a red action and measure if LazyOwnBT detects it.
- `PurpleTeamCommandSet.do_purple_test` (method) `cli/commands/purple_team.py:203` `def do_purple_test(self, args)` -- Test if LazyOwnBT would detect a command (no execution).
- `PurpleTeamCommandSet.do_purple_score` (method) `cli/commands/purple_team.py:223` `def do_purple_score(self, line)` -- Show current engagement detection score.
- `PurpleTeamCommandSet.do_purple_report` (method) `cli/commands/purple_team.py:271` `def do_purple_report(self, line)` -- Generate full engagement report with datasets.
- `PurpleTeamCommandSet.do_purple_methods` (method) `cli/commands/purple_team.py:285` `def do_purple_methods(self, line)` -- List available LazyOwnBT detection methods.
- `PurpleTeamCommandSet.do_purple_config` (method) `cli/commands/purple_team.py:297` `def do_purple_config(self, args)` -- Show or update purple team configuration (payload.json).
- `PurpleTeamCommandSet.do_purple_dashboard` (method) `cli/commands/purple_team.py:350` `def do_purple_dashboard(self, line)` -- Launch the Purple Team TUI dashboard.
- `PurpleTeamCommandSet.do_purple_history` (method) `cli/commands/purple_team.py:367` `def do_purple_history(self, args)` -- Show recent purple team action results.

## cli/commands/pwn.py
Depends on: `cli/commands/_base.py`, `core/safe_exec.py`, `core/validators.py`, `modules/__init__.py`, `modules/ai_exploit_chain.py`, `modules/autonomous_exploit_engine.py`, `modules/dashboard_engine.py`, `modules/enrich.py`, `modules/exploit_recommender.py`, `modules/rich_tui.py`, `modules/world_model.py`, `utils.py`
Imported by: `contrib/legacy/lazypwn.py`, `contrib/legacy/lazyvsftp.py`, `contrib/legacy/sql.py`
- `PwnCommandSet.do_auto_pwn` (method) `cli/commands/pwn.py:35` `def do_auto_pwn(self, line)` -- Run the full autonomous exploitation chain against the target.
- `PwnCommandSet.do_rich_tui` (method) `cli/commands/pwn.py:138` `def do_rich_tui(self, line)` -- Launch the Rich-based live dashboard TUI.
- `PwnCommandSet.do_exploit_chain` (method) `cli/commands/pwn.py:187` `def do_exploit_chain(self, line)` -- AI-driven multi-step exploit chaining with fallback strategies.
- `PwnCommandSet.do_lolbas_list` (method) `cli/commands/pwn.py:274` `def do_lolbas_list(self, line)` -- List available LOLBAS (Living Off The Land) techniques from plugins.
- `PwnCommandSet.do_lolbas_use` (method) `cli/commands/pwn.py:331` `def do_lolbas_use(self, line)` -- Execute a specific LOLBAS technique.
- `PwnCommandSet.do_stealth_on` (method) `cli/commands/pwn.py:423` `def do_stealth_on(self, line)` -- Enable stealth mode for subsequent operations.
- `PwnCommandSet.do_stealth_off` (method) `cli/commands/pwn.py:451` `def do_stealth_off(self, line)` -- Disable stealth mode.

## cli/commands/recon.py
Depends on: `cli/commands/_base.py`, `cli/exploit_advisor.py`, `cli/lazynmap_post.py`, `core/console.py`, `modules/intelligence_engine.py`, `utils.py`
- `ReconCommandSet.do_batchnmap` (method) `cli/commands/recon.py:47` `def do_batchnmap(self, line)` -- Runs the internal module `modules/lazynmap.sh` for multiple Nmap scans.
- `ReconCommandSet.do_lazynmap` (method) `cli/commands/recon.py:74` `def do_lazynmap(self, line)` -- Runs the internal module `modules/lazynmap.sh` with target mode.
- `ReconCommandSet.do_dig` (method) `cli/commands/recon.py:148` `def do_dig(self, line)` -- Executes the `dig` command to query DNS information.
- `ReconCommandSet.do_dnsenum` (method) `cli/commands/recon.py:180` `def do_dnsenum(self, line)` -- Performs DNS enumeration using `dnsenum` to identify subdomains for a given domain.
- `ReconCommandSet.do_dnsmap` (method) `cli/commands/recon.py:216` `def do_dnsmap(self, line)` -- Performs DNS enumeration using `dnsmap` to discover subdomains for a specified domain.
- `ReconCommandSet.do_whatweb` (method) `cli/commands/recon.py:249` `def do_whatweb(self, line)` -- Performs a web technology fingerprinting scan using `whatweb`.
- `ReconCommandSet.do_nbtscan` (method) `cli/commands/recon.py:286` `def do_nbtscan(self, line)` -- Performs network scanning using `nbtscan` to discover NetBIOS names and addresses in a specified range.
- `ReconCommandSet.do_nikto` (method) `cli/commands/recon.py:314` `def do_nikto(self, line)` -- Runs the `nikto` tool to perform a web server vulnerability scan against the specified target host.
- `ReconCommandSet.do_finalrecon` (method) `cli/commands/recon.py:423` `def do_finalrecon(self, line)` -- Runs the `finalrecon` tool to perform a web server vulnerability scan against the specified target host.
- `ReconCommandSet.do_openssl_sclient` (method) `cli/commands/recon.py:455` `def do_openssl_sclient(self, line)` -- Uses `openssl s_client` to connect to a specified host and port, allowing for testing and debugging of SSL/TLS...
- `ReconCommandSet.do_ss` (method) `cli/commands/recon.py:485` `def do_ss(self, line)` -- Search all exploit sources and map findings to the next LazyOwn command.
- `ReconCommandSet.do_wfuzz` (method) `cli/commands/recon.py:648` `def do_wfuzz(self, line)` -- Uses `wfuzz` to perform fuzzing based on provided parameters.

## cli/commands/recon_migrated.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/commands/_base.py`, `cli/surface_tui.py`, `core/config.py`, `utils.py`
- `ReconMigratedCommandSet.do_surface` (method) `cli/commands/recon_migrated.py:43` `def do_surface(self, line)` -- Render the network surface graph in the terminal.
- `ReconMigratedCommandSet.do_getcap` (method) `cli/commands/recon_migrated.py:97` `def do_getcap(self, line)` -- Retrieve and display file capabilities on the system.
- `ReconMigratedCommandSet.do_launchpad` (method) `cli/commands/recon_migrated.py:131` `def do_launchpad(self, line)` -- Searches for packages on Launchpad based on the provided search term and extracts codenames from the results.
- `ReconMigratedCommandSet.do_ping` (method) `cli/commands/recon_migrated.py:177` `def do_ping(self, line)` -- Perform a ping to check host availability and infer the operating system based on TTL values.
- `ReconMigratedCommandSet.do_gospider` (method) `cli/commands/recon_migrated.py:285` `def do_gospider(self, line)` -- Try gospider for web spidering.
- `ReconMigratedCommandSet.do_proxy` (method) `cli/commands/recon_migrated.py:373` `def do_proxy(self, line)` -- Runs a small proxy server to modify HTTP requests on the fly.
- `ReconMigratedCommandSet.do_ports` (method) `cli/commands/recon_migrated.py:411` `def do_ports(self, line)` -- Lists all open TCP and UDP ports on the local system.
- `ReconMigratedCommandSet.do_tcpdump_icmp` (method) `cli/commands/recon_migrated.py:453` `def do_tcpdump_icmp(self, line)` -- Starts `tcpdump` to capture ICMP traffic on the specified interface.
- `ReconMigratedCommandSet.do_tcpdump_capture` (method) `cli/commands/recon_migrated.py:486` `def do_tcpdump_capture(self, line)` -- Starts packet capture using `tcpdump` on the specified interface.
- `ReconMigratedCommandSet.do_tshark_analyze` (method) `cli/commands/recon_migrated.py:527` `def do_tshark_analyze(self, line)` -- Analyzes a packet capture file using `tshark` based on the provided remote host IP.
- `ReconMigratedCommandSet.do_waybackmachine` (method) `cli/commands/recon_migrated.py:593` `def do_waybackmachine(self, line)` -- Fetch URLs from the Wayback Machine for a given website.
- `ReconMigratedCommandSet.do_sslscan` (method) `cli/commands/recon_migrated.py:633` `def do_sslscan(self, line)` -- Run an SSL scan on the specified remote host.
- `ReconMigratedCommandSet.do_graudit` (method) `cli/commands/recon_migrated.py:674` `def do_graudit(self, line)` -- Executes the graudit command to perform a static code analysis with the specified options.
- `ReconMigratedCommandSet.do_sherlock` (method) `cli/commands/recon_migrated.py:705` `def do_sherlock(self, line)` -- Executes the Sherlock tool to find usernames across social networks.
- `ReconMigratedCommandSet.do_trufflehog` (method) `cli/commands/recon_migrated.py:746` `def do_trufflehog(self, line)` -- Executes trufflehog to search for secrets in a given Git repository URL.
- `ReconMigratedCommandSet.do_apache_users` (method) `cli/commands/recon_migrated.py:784` `def do_apache_users(self, line)` -- Performs enumeration of users from a target system using `apache-users`.
- `ReconMigratedCommandSet.do_trace` (method) `cli/commands/recon_migrated.py:831` `def do_trace(self, line)` -- Traces the DNS information for a given self.params['domain'] using the FreeDNS service.
- `ReconMigratedCommandSet.do_alterx` (method) `cli/commands/recon_migrated.py:874` `def do_alterx(self, line)` -- Executes the 'alterx' command for subdomain enumeration on the provided self.params['domain'].
- `ReconMigratedCommandSet.do_windapsearchscrapeusers` (method) `cli/commands/recon_migrated.py:951` `def do_windapsearchscrapeusers(self, line)` -- Extracts usernames from a JSON output generated by go-windapsearch and appends them to the file sessions/users.txt.
- `ReconMigratedCommandSet.do_cve` (method) `cli/commands/recon_migrated.py:987` `def do_cve(self, line)` -- Search for a CVE using the CIRCL API.
- `ReconMigratedCommandSet.do_serveralive2` (method) `cli/commands/recon_migrated.py:1036` `def do_serveralive2(self, line)` -- Command serveralive2: Uses Impacket to connect to a remote MSRPC interface and retrieves the server bindings.
- `ReconMigratedCommandSet.do_binarycheck` (method) `cli/commands/recon_migrated.py:1070` `def do_binarycheck(self, line)` -- Performs various checks on a selected binary to gather information and protections.
- `ReconMigratedCommandSet.do_dnstool_py` (method) `cli/commands/recon_migrated.py:1115` `def do_dnstool_py(self, line)` -- Executes the dnstool.py tool to modify Active Directory-integrated DNS records.
- `ReconMigratedCommandSet.do_metabigor` (method) `cli/commands/recon_migrated.py:1161` `def do_metabigor(self, line)` -- Executes Metabigor commands for OSINT and scanning tasks with guided input or predefined arguments.
- `ReconMigratedCommandSet.do_httprobe` (method) `cli/commands/recon_migrated.py:1237` `def do_httprobe(self, line)` -- Executes the httprobe tool to probe domains for working HTTP and HTTPS servers.
- `ReconMigratedCommandSet.do_recon` (method) `cli/commands/recon_migrated.py:1280` `def do_recon(self, line)` -- Performs reconnaissance on a specified self.params['domain'] using crt.sh (the target must be visible on internet)...
- `ReconMigratedCommandSet.do_dnschef` (method) `cli/commands/recon_migrated.py:1334` `def do_dnschef(self, line)` -- Executes the DNSChef tool to monitor DNS queries and intercept responses.
- `ReconMigratedCommandSet.do_ipinfo` (method) `cli/commands/recon_migrated.py:1369` `def do_ipinfo(self, line)` -- Retrieves detailed information about an IP address using the ARIN API.

## cli/commands/redteam_gym.py
Depends on: `cli/commands/_base.py`, `modules/chain_registry.py`, `modules/ctf_signalman.py`, `modules/metasploitable_gym.py`, `modules/redteam_gym.py`, `utils.py`
Imported by: `tests/test_gym_cli.py`, `tests/test_gym_ms2_cli.py`
- `RedTeamGymCommandSet.do_gym` (method) `cli/commands/redteam_gym.py:41` `def do_gym(self, line)` -- Red Team Gym — gamified pentest training with ELO scoring.
- `RedTeamGymCommandSet.do_gym_ms2` (method) `cli/commands/redteam_gym.py:138` `def do_gym_ms2(self, line)` -- Metasploitable 2 gym catalogue: list|chains|validate|info <vuln>|chain <vuln>.

## cli/commands/resource_scripting.py
Depends on: `cli/commands/_base.py`, `modules/resource_script.py`, `utils.py`
- `on_cmd` (function) `cli/commands/resource_scripting.py:35` `def on_cmd(cmd)`
- `on_print` (function) `cli/commands/resource_scripting.py:39` `def on_print(msg)`
- `ResourceCommandSet.do_resource` (method) `cli/commands/resource_scripting.py:49` `def do_resource(self, line)` -- Run an enhanced resource script.
- `ResourceCommandSet.do_makerc` (method) `cli/commands/resource_scripting.py:88` `def do_makerc(self, line)` -- Record session commands to a resource script.
- `ResourceCommandSet.do_spool` (method) `cli/commands/resource_scripting.py:122` `def do_spool(self, line)` -- Log session output to a file.
- `ResourceCommandSet.do_mkrc` (method) `cli/commands/resource_scripting.py:152` `def do_mkrc(self, line)` -- Alias for makerc — record commands to a script.

## cli/commands/retry_ops.py
Depends on: `cli/commands/_base.py`, `cli/retry_support.py`, `modules/lazy_runner.py`, `utils.py`
- `RetryOpsCommandSet.do_retry` (method) `cli/commands/retry_ops.py:68` `def do_retry(self, line)` -- Relaunch failed work: retry status | chain | loop.

## cli/commands/scan.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `ScanCommandSet.do_gobuster` (method) `cli/commands/scan.py:56` `def do_gobuster(self, line)` -- Uses `gobuster` for directory and virtual host fuzzing based on provided parameters.
- `ScanCommandSet.do_arpscan` (method) `cli/commands/scan.py:129` `def do_arpscan(self, line)` -- Executes an ARP scan using `arp-scan`.
- `ScanCommandSet.do_dirsearch` (method) `cli/commands/scan.py:170` `def do_dirsearch(self, line)` -- Runs the `dirsearch` tool to perform directory and file enumeration on a specified URL.
- `ScanCommandSet.do_dmitry` (method) `cli/commands/scan.py:213` `def do_dmitry(self, line)` -- This function constructs and executes a command for the 'dmitry' tool.
- `ScanCommandSet.do_feroxbuster` (method) `cli/commands/scan.py:248` `def do_feroxbuster(self, line)` -- Command feroxbuster: Installs and runs Feroxbuster for performing forced browsing and directory brute-forcing.
- `ScanCommandSet.do_nmapscript` (method) `cli/commands/scan.py:316` `def do_nmapscript(self, line)` -- Perform an Nmap scan using a specified script and port.
- `ScanCommandSet.do_nuclei` (method) `cli/commands/scan.py:350` `def do_nuclei(self, line)` -- Executes a Nuclei scan on a specified target URL or host.
- `ScanCommandSet.do_amass` (method) `cli/commands/scan.py:392` `def do_amass(self, line)` -- Executes Amass to perform a passive enumeration on a given domain.
- `ScanCommandSet.do_bbot` (method) `cli/commands/scan.py:422` `def do_bbot(self, line)` -- Executes a BBOT scan to perform various reconnaissance tasks.
- `ScanCommandSet.do_osmedeus` (method) `cli/commands/scan.py:473` `def do_osmedeus(self, line)` -- Executes Osmedeus scans with guided input for various scanning scenarios.
- `ScanCommandSet.do_magicrecon` (method) `cli/commands/scan.py:548` `def do_magicrecon(self, line)` -- Command magicrecon: Automates the setup and usage of MagicRecon to perform various types of reconnaissance and...
- `ScanCommandSet.do_hostdiscover` (method) `cli/commands/scan.py:606` `def do_hostdiscover(self, line)` -- Discover active hosts in a subnet by performing a ping sweep.
- `ScanCommandSet.do_portdiscover` (method) `cli/commands/scan.py:664` `def do_portdiscover(self, line)` -- Scan all ports on a specified host to identify open ports.
- `ScanCommandSet.do_portservicediscover` (method) `cli/commands/scan.py:724` `def do_portservicediscover(self, line)` -- Scan all ports on a specified host to identify open ports and associated services.
- `ScanCommandSet.do_skipfish` (method) `cli/commands/scan.py:789` `def do_skipfish(self, line)` -- This function executes the web security scanning tool Skipfish using the provided configuration and parameters.
- `ScanCommandSet.do_vscan` (method) `cli/commands/scan.py:839` `def do_vscan(self, line)` -- Perform port scanning using vscan with the provided parameters.

## cli/commands/scan_migrated.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `ScanMigratedCommandSet.do_cme` (method) `cli/commands/scan_migrated.py:37` `def do_cme(self, line)` -- Execute CrackMapExec (CME) for SMB enumeration and authentication attempts against a target.
- `ScanMigratedCommandSet.do_ldapdomaindump` (method) `cli/commands/scan_migrated.py:176` `def do_ldapdomaindump(self, line)` -- Dumps LDAP information using `ldapdomaindump` with credentials from a file.
- `ScanMigratedCommandSet.do_bloodhound` (method) `cli/commands/scan_migrated.py:218` `def do_bloodhound(self, line)` -- Perform LDAP enumeration using bloodhound-python with credentials from a file.
- `ScanMigratedCommandSet.do_swaks` (method) `cli/commands/scan_migrated.py:267` `def do_swaks(self, line)` -- Sends an email using `swaks` (Swiss Army Knife for SMTP).
- `ScanMigratedCommandSet.do_samrdump` (method) `cli/commands/scan_migrated.py:306` `def do_samrdump(self, line)` -- Run `impacket-samrdump` to dump SAM data from specified ports.
- `ScanMigratedCommandSet.do_lynis` (method) `cli/commands/scan_migrated.py:361` `def do_lynis(self, line)` -- Performs a Lynis audit on the specified remote system.
- `ScanMigratedCommandSet.do_snmpcheck` (method) `cli/commands/scan_migrated.py:390` `def do_snmpcheck(self, line)` -- Performs an SNMP check on the specified target host.
- `ScanMigratedCommandSet.do_snmpwalk` (method) `cli/commands/scan_migrated.py:417` `def do_snmpwalk(self, line)` -- Performs an SNMP check on the specified target host.
- `ScanMigratedCommandSet.do_smtpuserenum` (method) `cli/commands/scan_migrated.py:444` `def do_smtpuserenum(self, line)` -- Enumerates SMTP users using the `smtp-user-enum` tool with the VRFY method.
- `ScanMigratedCommandSet.do_sessionssh` (method) `cli/commands/scan_migrated.py:483` `def do_sessionssh(self, line)` -- Execute a command to list active SSH connections.
- `ScanMigratedCommandSet.do_smbattack` (method) `cli/commands/scan_migrated.py:507` `def do_smbattack(self, line)` -- Scans for hosts with SMB service open on port 445 in the specified target network.
- `find_tgts` (function) `cli/commands/scan_migrated.py:536` `def find_tgts(subnet)` -- Finds and returns a list of target hosts with port 445 open in the specified subnet.
- `setup_handler` (function) `cli/commands/scan_migrated.py:562` `def setup_handler(config_file, lhost, lport)` -- Sets up a Metasploit multi/handler configuration in the given config file.
- `conficker_exploit` (function) `cli/commands/scan_migrated.py:582` `def conficker_exploit(config_file, host, lhost, lport)` -- Configures and writes a Metasploit exploit for the Conficker vulnerability to the given config file.
- `smb_brute` (function) `cli/commands/scan_migrated.py:602` `def smb_brute(config_file, host, passwd_file, lhost, lport)` -- Configures and writes a Metasploit SMB brute force exploit for the given host to the provided config file.
- `ScanMigratedCommandSet.do_parsero` (method) `cli/commands/scan_migrated.py:667` `def do_parsero(self, line)` -- Executes a parsero scan on a specified target URL or host.
- `ScanMigratedCommandSet.do_changeme` (method) `cli/commands/scan_migrated.py:699` `def do_changeme(self, line)` -- Executes a changeme scan on a specified target URL or host.
- `ScanMigratedCommandSet.do_enum4linux_ng` (method) `cli/commands/scan_migrated.py:730` `def do_enum4linux_ng(self, line)` -- Performs enumeration of information from a target system using `enum4linux-ng`.
- `ScanMigratedCommandSet.do_fuzz` (method) `cli/commands/scan_migrated.py:770` `def do_fuzz(self, line)` -- Executes a web server fuzzing script with user-provided parameters.
- `ScanMigratedCommandSet.do_kerbrute` (method) `cli/commands/scan_migrated.py:815` `def do_kerbrute(self, line)` -- Executes the Kerbrute tool to enumerate user accounts against a specified target self.params['domain'] controller.
- `ScanMigratedCommandSet.do_davtest` (method) `cli/commands/scan_migrated.py:901` `def do_davtest(self, line)` -- Tests WebDAV server configurations using `davtest`.
- `ScanMigratedCommandSet.do_evil_ssdp` (method) `cli/commands/scan_migrated.py:942` `def do_evil_ssdp(self, line)` -- Runs evil-ssdp with various options and user-selected templates.
- `ScanMigratedCommandSet.do_netexec` (method) `cli/commands/scan_migrated.py:988` `def do_netexec(self, line)` -- Executes netexec with various options for network protocol operations.
- `install_netexec` (function) `cli/commands/scan_migrated.py:1015` `def install_netexec()`
- `install_netexec_pipx` (function) `cli/commands/scan_migrated.py:1020` `def install_netexec_pipx()`
- `ScanMigratedCommandSet.do_allin` (method) `cli/commands/scan_migrated.py:1241` `def do_allin(self, line)` -- Execute the AlliN.py tool with various scan modes and parameters.
- `ScanMigratedCommandSet.do_windapsearch` (method) `cli/commands/scan_migrated.py:1312` `def do_windapsearch(self, line)` -- Execute the windapsearch tool to perform Active Directory Domain enumeration through LDAP queries.
- `ScanMigratedCommandSet.do_ldapsearch` (method) `cli/commands/scan_migrated.py:1440` `def do_ldapsearch(self, line)` -- Executes an LDAP search against a target remote host (self.params['rhost']) and saves the results.
- `ScanMigratedCommandSet.do_arjun` (method) `cli/commands/scan_migrated.py:1501` `def do_arjun(self, line)` -- Executes an Arjun scan on the specified URL for parameter discovery.
- `ScanMigratedCommandSet.do_finger_user_enum` (method) `cli/commands/scan_migrated.py:1569` `def do_finger_user_enum(self, line)` -- Executes the `finger-user-enum` tool for enumerating users on the target host.
- `ScanMigratedCommandSet.do_wpscan` (method) `cli/commands/scan_migrated.py:1615` `def do_wpscan(self, line)` -- Command wpscan: Installs and runs WPScan to perform WordPress vulnerability scanning.
- `ScanMigratedCommandSet.do_loxs` (method) `cli/commands/scan_migrated.py:1678` `def do_loxs(self, line)` -- Command loxs: Installs and runs Loxs for multi-vulnerability web application scanning.
- `ScanMigratedCommandSet.do_blazy` (method) `cli/commands/scan_migrated.py:1722` `def do_blazy(self, line)` -- Command blazy: Installs and runs blazy for multi-vulnerability web application scanning.
- `ScanMigratedCommandSet.do_parth` (method) `cli/commands/scan_migrated.py:1771` `def do_parth(self, line)` -- Command parth: Installs and runs Parth for discovering vulnerable URLs and parameters.
- `ScanMigratedCommandSet.do_breacher` (method) `cli/commands/scan_migrated.py:1840` `def do_breacher(self, line)` -- Command breacher: Installs and runs Breacher for finding admin login pages and EAR vulnerabilities.
- `ScanMigratedCommandSet.do_openredirex` (method) `cli/commands/scan_migrated.py:1902` `def do_openredirex(self, line)` -- Command openredirex: Clones, installs, and runs OpenRedirex for testing open redirection vulnerabilities.
- `ScanMigratedCommandSet.do_odat` (method) `cli/commands/scan_migrated.py:1970` `def do_odat(self, line)` -- Command odat: Runs the ODAT sidguesser module to guess Oracle SIDs on a target Oracle database.
- `ScanMigratedCommandSet.do_rpcmap_py` (method) `cli/commands/scan_migrated.py:2088` `def do_rpcmap_py(self, line)` -- Command rpcmap_py: Executes rpcmap.py commands to enumerate MSRPC interfaces.
- `ScanMigratedCommandSet.do_pykerbrute` (method) `cli/commands/scan_migrated.py:2131` `def do_pykerbrute(self, line)` -- Command pykerbrute: Automates the installation and execution of PyKerbrute for bruteforcing Active Directory...
- `ScanMigratedCommandSet.do_netview` (method) `cli/commands/scan_migrated.py:2201` `def do_netview(self, line)` -- Executes the Impacket netview tool to list network shares on a specified target.
- `ScanMigratedCommandSet.do_rdp_check_py` (method) `cli/commands/scan_migrated.py:2265` `def do_rdp_check_py(self, line)` -- Executes the RDP check tool to verify credentials or hash-based authentication on a target system.
- `ScanMigratedCommandSet.do_mqtt_check_py` (method) `cli/commands/scan_migrated.py:2330` `def do_mqtt_check_py(self, line)` -- Executes the MQTT check tool to verify credentials on a target system with optional SSL.
- `ScanMigratedCommandSet.do_lookupsid_py` (method) `cli/commands/scan_migrated.py:2385` `def do_lookupsid_py(self, line)` -- Executes the LookupSID tool to perform SID enumeration on a target system.
- `ScanMigratedCommandSet.do_lookupsid` (method) `cli/commands/scan_migrated.py:2458` `def do_lookupsid(self, line)` -- Executes the Impacket lookupsid tool to enumerate SIDs on a target system.
- `ScanMigratedCommandSet.do_certipy_ad` (method) `cli/commands/scan_migrated.py:2520` `def do_certipy_ad(self, line)` -- Run certipy-ad against Active Directory Certificate Services.
- `ScanMigratedCommandSet.do_certipy` (method) `cli/commands/scan_migrated.py:2584` `def do_certipy(self, line)` -- Executes the Certipy tool to interact with Active Directory Certificate Services.
- `ScanMigratedCommandSet.do_sawks` (method) `cli/commands/scan_migrated.py:2678` `def do_sawks(self, line)` -- Executes the Swaks (Swiss Army Knife for SMTP) tool to send test emails for phishing simulations.
- `ScanMigratedCommandSet.do_ad_ldap_enum` (method) `cli/commands/scan_migrated.py:2715` `def do_ad_ldap_enum(self, line)` -- Executes ad-ldap-enum to enumerate Active Directory objects (users, groups, computers) through LDAP, collecting...
- `ScanMigratedCommandSet.do_net_rpc_addmem` (method) `cli/commands/scan_migrated.py:2769` `def do_net_rpc_addmem(self, line)` -- Executes the net rpc group addmem command to add a user to a specified group in Active Directory.
- `ScanMigratedCommandSet.do_pre2k` (method) `cli/commands/scan_migrated.py:2815` `def do_pre2k(self, line)` -- Executes the pre2k tool to query the self.params['domain'] for pre-Windows 2000 machine accounts or to pass a list...
- `ScanMigratedCommandSet.do_hound` (method) `cli/commands/scan_migrated.py:2908` `def do_hound(self, line)` -- Executes the hound tool for Hound is a simple and light tool for information gathering and capture exact GPS coordinates


Next: [API_p4.md](API_p4.md)
