# Subsystem: commands (page 3 of 5)
Previous: [KB_commands_p2.md](KB_commands_p2.md)

## cli/commands/lab.py
- Doc: Lab environment commands -- spin up vulnerable practice targets.
- Layer: utility
- Language: py
- Symbols:
  - `LabCommandSet` (class, line 27) `class LabCommandSet(LazyOwnCommandSet)`
  - `_docker_available` (method, line 33) `def _docker_available(self)`
  - `_running_containers` (method, line 37) `def _running_containers(self)`
  - `_running_range_containers` (method, line 41) `def _running_range_containers(self)`
  - `_container_name` (method, line 45) `def _container_name(self, scenario)`
  - `_container_ip` (method, line 49) `def _container_ip(self, container_name)`
  - `_lab_ensure_web` (method, line 53) `def _lab_ensure_web(self, scenario, container_name)`
  - `_print_lab_target` (method, line 57) `def _print_lab_target(self, scenario, container_name, ports)`
  - `_lab_migrate` (method, line 78) `def _lab_migrate(self, scenario, container_name)`
  - `do_lab` (method, line 93) `def do_lab(self, line)`
  - `_lab_list` (method, line 145) `def _lab_list(self)`
  - `_lab_start` (method, line 159) `def _lab_start(self, scenario)`
  - `_lab_stop` (method, line 205) `def _lab_stop(self, scenario)`
  - `_range_dispatch` (method, line 218) `def _range_dispatch(self, args)`
  - `_range_list` (method, line 250) `def _range_list(self)`
  - `_range_start` (method, line 259) `def _range_start(self, profile)`
  - `_range_container_state` (method, line 296) `def _range_container_state(self, container)`
  - `_range_wait_healthy` (method, line 321) `def _range_wait_healthy(self, compose, timeout)`
  - `_range_verify` (method, line 353) `def _range_verify(self, profile)`
  - `_tcp_reachable` (method, line 390) `def _tcp_reachable(host, port, timeout)`
  - `_range_container_ip` (method, line 407) `def _range_container_ip(self, container)`
  - `_range_stop` (method, line 418) `def _range_stop(self, profile)`
  - `_range_status` (method, line 431) `def _range_status(self)`
  - `_lab_container_state` (method, line 442) `def _lab_container_state(self, container_name)`
  - `_lab_status` (method, line 456) `def _lab_status(self)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`
- Imported by: `tests/test_infra_disposable.py`, `tests/test_lab_target_visibility.py`

## cli/commands/lateral.py
- Doc: Lateral Movement command set (pending).
- Layer: utility
- Language: py
- Symbols:
  - `LateralMovementCommandSet` (class, line 24) `class LateralMovementCommandSet(LazyOwnCommandSet)`
  - `do_socat` (method, line 31) `def do_socat(self, line)`
  - `do_chisel` (method, line 43) `def do_chisel(self, line)`
  - `do_set_proxychains` (method, line 59) `def do_set_proxychains(self, line)`
  - `do_ngrok` (method, line 72) `def do_ngrok(self, line)`
  - `do_ligolo` (method, line 79) `def do_ligolo(self, line)`
  - `do_nc` (method, line 91) `def do_nc(self, line)`
  - `do_wmiexec` (method, line 106) `def do_wmiexec(self, line)`
  - `do_ssh` (method, line 114) `def do_ssh(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`

## cli/commands/lateral_migrated.py
- Doc: lateral commands migrated from lazyown.py.
- Layer: utility
- Language: py
- Symbols:
  - `LateralMigratedCommandSet` (class, line 24) `class LateralMigratedCommandSet(LazyOwnCommandSet)`
  - `do_vpn` (method, line 29) `def do_vpn(self, line)`
  - `do_id_rsa` (method, line 101) `def do_id_rsa(self, line)`
  - `do_sshd` (method, line 172) `def do_sshd(self, line)`
  - `do_wifipass` (method, line 199) `def do_wifipass(self, line)`
  - `do_bloodyAD` (method, line 229) `def do_bloodyAD(self, line)`
  - `do_getTGT` (method, line 321) `def do_getTGT(self, line)`
  - `do_tord` (method, line 369) `def do_tord(self, line)`
  - `do_shadowsocks` (method, line 404) `def do_shadowsocks(self, line)`
  - `do_rnc` (method, line 477) `def do_rnc(self, line)`
  - `do_gospherus` (method, line 543) `def do_gospherus(self, line)`
  - `do_mssqlcli` (method, line 613) `def do_mssqlcli(self, line)`
  - `do_penelope` (method, line 666) `def do_penelope(self, line)`
  - `do_stormbreaker` (method, line 777) `def do_stormbreaker(self, line)`
  - `do_regeorg` (method, line 823) `def do_regeorg(self, line)`
  - `do_targetedKerberoas` (method, line 871) `def do_targetedKerberoas(self, line)`
  - `do_dcomexec` (method, line 931) `def do_dcomexec(self, line)`
  - `do_upload_c2` (method, line 1002) `def do_upload_c2(self, line)`
  - `do_wmiexecpro` (method, line 1031) `def do_wmiexecpro(self, line)`
  - `do_lateral_mov_lin` (method, line 1247) `def do_lateral_mov_lin(self, line)`
  - `do_addcli` (method, line 1302) `def do_addcli(self, line)`
  - `do_dominion` (method, line 1317) `def do_dominion(self, line)`
  - `install_wmiexecpro` (function, line 1070) `def install_wmiexecpro()`
- Depends on: `cli/commands/_base.py`, `core/hardening.py`, `modules/domain_dominance.py`, `utils.py`

## cli/commands/lazy_creds.py
- Doc: LazyCreds shell commands: default-credential knowledge base lookups.
- Layer: utility
- Language: py
- Symbols:
  - `LazyCredsCommandSet` (class, line 21) `class LazyCredsCommandSet(LazyOwnCommandSet)`
  - `do_lazycreds` (method, line 28) `def do_lazycreds(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`

## cli/commands/lazy_dorks.py
- Doc: LazyDorks shell command: render target dork playbooks into session artefacts.
- Layer: utility
- Language: py
- Symbols:
  - `_slug` (function, line 18) `def _slug(domain)`
  - `LazyDorksCommandSet` (class, line 30) `class LazyDorksCommandSet(LazyOwnCommandSet)`
  - `do_lazydork` (method, line 37) `def do_lazydork(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`

## cli/commands/lazy_oob.py
- Doc: LazyOob shell commands: local OOB canary for blind SSRF/RCE callbacks.
- Layer: utility
- Language: py
- Symbols:
  - `LazyOobCommandSet` (class, line 22) `class LazyOobCommandSet(LazyOwnCommandSet)`
  - `do_lazyoob` (method, line 29) `def do_lazyoob(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`

## cli/commands/lazy_passgen.py
- Doc: LazyPassGen shell command: target-aware weak password generation.
- Layer: utility
- Language: py
- Symbols:
  - `LazyPassGenCommandSet` (class, line 14) `class LazyPassGenCommandSet(LazyOwnCommandSet)`
  - `do_lazypassgen` (method, line 21) `def do_lazypassgen(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `utils.py`

## cli/commands/lazy_poc.py
- Doc: LazyPoc shell commands: catalogued PoC scripts as reusable verbs.
- Layer: utility
- Language: py
- Symbols:
  - `LazyPocCommandSet` (class, line 20) `class LazyPocCommandSet(LazyOwnCommandSet)`
  - `do_lazy_poc` (method, line 25) `def do_lazy_poc(self, line)`
  - `_list` (method, line 67) `def _list(self, registry)`
  - `_info` (method, line 82) `def _info(self, registry, name)`
  - `_run` (method, line 105) `def _run(self, registry, name, target, overrides)`
  - `_log_run` (method, line 155) `def _log_run(self, verb, rendered, output, returncode)`
- Depends on: `cli/commands/_base.py`, `core/config.py`, `core/hardening.py`, `modules/__init__.py`, `utils.py`

## cli/commands/lazyloop.py
- Doc: Lazy queue and misc command set.
- Layer: utility
- Language: py
- Symbols:
  - `_engine` (function, line 22) `def _engine()`
  - `LazyQueueCommandSet` (class, line 29) `class LazyQueueCommandSet(LazyOwnCommandSet)`
  - `do_lazy_sync` (method, line 36) `def do_lazy_sync(self, line)`
  - `do_lazy_intents` (method, line 51) `def do_lazy_intents(self, line)`
  - `do_lazy_delete` (method, line 71) `def do_lazy_delete(self, line)`
  - `do_lazy_findings` (method, line 110) `def do_lazy_findings(self, line)`
  - `do_lazy_handoff` (method, line 180) `def do_lazy_handoff(self, line)`
  - `do_lazy_verdict` (method, line 190) `def do_lazy_verdict(self, line)`
  - `do_lazy_mention` (method, line 213) `def do_lazy_mention(self, line)`
  - `do_lazy_approve` (method, line 248) `def do_lazy_approve(self, line)`
  - `do_lazy_fleet` (method, line 270) `def do_lazy_fleet(self, line)`
  - `do_lazy_orchestrator` (method, line 335) `def do_lazy_orchestrator(self, line)`
  - `do_lazy_view` (method, line 364) `def do_lazy_view(self, line)`
- Depends on: `cli/commands/_base.py`, `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `modules/lazy_bridge.py`, `modules/lazy_engine.py`, `modules/lazy_mentions.py`, `modules/sinks/findings.py`, `utils.py`
- Imported by: `tests/test_guardrails.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_runner.py`

## cli/commands/lazyops.py
- Doc: Lazy autonomous loop commands (single orchestrator, lazy_* surface).
- Layer: utility
- Language: py
- Symbols:
  - `_engine` (function, line 28) `def _engine()`
  - `LazyCommandSet` (class, line 35) `class LazyCommandSet(LazyOwnCommandSet)`
  - `_task_id` (method, line 41) `def _task_id(self, args)`
  - `_require_task` (method, line 54) `def _require_task(self, args)`
  - `_free_text` (method, line 62) `def _free_text(args)`
  - `do_lazy_dispatch` (method, line 88) `def do_lazy_dispatch(self, line)`
  - `do_lazy_task` (method, line 147) `def do_lazy_task(self, line)`
  - `do_lazy_graph` (method, line 269) `def do_lazy_graph(self, line)`
  - `do_lazy_context` (method, line 298) `def do_lazy_context(self, line)`
  - `do_lazy_skill` (method, line 319) `def do_lazy_skill(self, line)`
  - `do_lazy_workspace` (method, line 403) `def do_lazy_workspace(self, line)`
  - `do_lazy_selfupdate` (method, line 456) `def do_lazy_selfupdate(self, line)`
  - `do_lazy_planner` (method, line 484) `def do_lazy_planner(self, line)`
  - `do_lazy_frontier` (method, line 503) `def do_lazy_frontier(self, line)`
  - `do_lazy_worker` (method, line 515) `def do_lazy_worker(self, line)`
  - `do_lazy_trace` (method, line 555) `def do_lazy_trace(self, line)`
  - `do_lazy_broadcast` (method, line 608) `def do_lazy_broadcast(self, line)`
  - `do_lazy_hint` (method, line 643) `def do_lazy_hint(self, line)`
  - `do_lazy_intent` (method, line 655) `def do_lazy_intent(self, line)`
  - `do_lazy_intent_delete` (method, line 680) `def do_lazy_intent_delete(self, line)`
  - `do_lazy_goal` (method, line 723) `def do_lazy_goal(self, line)`
  - `do_lazy_constraint` (method, line 762) `def do_lazy_constraint(self, line)`
  - `do_lazy_scope` (method, line 780) `def do_lazy_scope(self, line)`
  - `do_lazy_todo` (method, line 798) `def do_lazy_todo(self, line)`
  - `do_lazy_asset` (method, line 820) `def do_lazy_asset(self, line)`
  - `do_lazy_enrich` (method, line 861) `def do_lazy_enrich(self, line)`
  - `do_lazy_traffic` (method, line 873) `def do_lazy_traffic(self, line)`
  - `do_lazy_guard` (method, line 1094) `def do_lazy_guard(self, line)`
  - `do_lazy_finding` (method, line 1195) `def do_lazy_finding(self, line)`
  - `do_lazy_retest` (method, line 1260) `def do_lazy_retest(self, line)`
  - `do_lazy_steer` (method, line 1279) `def do_lazy_steer(self, line)`
  - `do_lazy_kill` (method, line 1291) `def do_lazy_kill(self, line)`
  - `do_lazy_pause` (method, line 1303) `def do_lazy_pause(self, line)`
  - `do_lazy_resume` (method, line 1313) `def do_lazy_resume(self, line)`
  - `do_lazy_report` (method, line 1323) `def do_lazy_report(self, line)`
  - `do_lazy_runtime` (method, line 1340) `def do_lazy_runtime(self, line)`
  - `do_lazy_payload_keys` (method, line 1387) `def do_lazy_payload_keys(self, line)`
  - `do_lazy_fact` (method, line 1399) `def do_lazy_fact(self, line)`
  - `do_lazy_node` (method, line 1427) `def do_lazy_node(self, line)`
  - `do_lazy_evidence` (method, line 1447) `def do_lazy_evidence(self, line)`
  - `do_lazy_ask` (method, line 1514) `def do_lazy_ask(self, line)`
  - `_agent_main_tools` (method, line 1540) `def _agent_main_tools(self, task_id)`
  - `_agent_main_prompt` (method, line 1657) `def _agent_main_prompt(self, task_id)`
  - `do_lazy_agent` (method, line 1668) `def do_lazy_agent(self, line)`
  - `do_lazy_company` (method, line 1769) `def do_lazy_company(self, line)`
  - `do_lazy_tool` (method, line 1791) `def do_lazy_tool(self, line)`
  - `do_lazy_verb` (method, line 1863) `def do_lazy_verb(self, line)`
  - `do_lazy_stage` (method, line 1961) `def do_lazy_stage(self, line)`
  - `do_lazy_mode` (method, line 1989) `def do_lazy_mode(self, line)`
  - `do_lazy_addon` (method, line 2015) `def do_lazy_addon(self, line)`
  - `do_lazy_notify` (method, line 2122) `def do_lazy_notify(self, line)`
  - `do_lazy_trigger` (method, line 2170) `def do_lazy_trigger(self, line)`
  - `do_lazy_llm` (method, line 2259) `def do_lazy_llm(self, line)`
  - `do_lazy_compact` (method, line 2396) `def do_lazy_compact(self, line)`
  - `do_lazy_status` (method, line 2468) `def do_lazy_status(self, line)`
  - `do_lazy_overview` (method, line 2492) `def do_lazy_overview(self, line)`
  - `do_lazy_archive` (method, line 2497) `def do_lazy_archive(self, line)`
  - `do_lazy_template` (method, line 2528) `def do_lazy_template(self, line)`
  - `do_lazy_category` (method, line 2559) `def do_lazy_category(self, line)`
  - `do_lazy_chat` (method, line 2580) `def do_lazy_chat(self, line)`
  - `do_lazy_scheduler` (method, line 2613) `def do_lazy_scheduler(self, line)`
  - `do_lazy_gate` (method, line 2640) `def do_lazy_gate(self, line)`
  - `do_lazy_loop` (method, line 2685) `def do_lazy_loop(self, line)`
  - `do_lazy_sandbox` (method, line 2711) `def do_lazy_sandbox(self, line)`
  - `do_lazy_install` (method, line 2774) `def do_lazy_install(self, line)`
  - `do_lazy_pacing` (method, line 2812) `def do_lazy_pacing(self, line)`
  - `run_command` (function, line 1545) `def run_command(command)`
  - `list_tasks` (function, line 1567) `def list_tasks()`
  - `task_graph` (function, line 1571) `def task_graph(task)`
  - `task_findings` (function, line 1575) `def task_findings(task)`
  - `campaign_sitrep` (function, line 1579) `def campaign_sitrep()`
  - `add_hint` (function, line 1592) `def add_hint(text)`
  - `steer_intent` (function, line 1599) `def steer_intent(intent, message)`
- Depends on: `cli/commands/_base.py`, `core/process.py`, `modules/__init__.py`, `modules/addon_updater.py`, `modules/auto_registry.py`, `modules/custom_tools.py`, `modules/lazy_agent.py`, `modules/lazy_cli_bridge.py`, `modules/lazy_engine.py`, `modules/lazy_installer.py`, `modules/lazy_proxy.py`, `modules/lazy_roles.py`, `modules/lazy_runner.py`, `modules/lazy_sandbox.py`, `modules/lazy_skill_mirror.py`, `modules/lazy_skills.py`, `modules/orchestrator_config.py`, `modules/selfupdate.py`, `modules/traffic_recorder.py`, `utils.py`
- Imported by: `tests/test_asset_gate.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_engine.py`, `tests/test_lazy_runner.py`

## cli/commands/marketplace.py
- Doc: Plugin/addon marketplace commands.
- Layer: utility
- Language: py
- Symbols:
  - `_safe_git_clone` (function, line 47) `def _safe_git_clone(repo_url, dest, depth)`
  - `MarketplaceCommandSet` (class, line 62) `class MarketplaceCommandSet(LazyOwnCommandSet)`
  - `_registry` (method, line 68) `def _registry(self)`
  - `_tiers` (method, line 74) `def _tiers(self)`
  - `_ratings_path` (method, line 78) `def _ratings_path(self)`
  - `_tier_label` (method, line 82) `def _tier_label(self, name, tiers)`
  - `_installed_plugins` (method, line 86) `def _installed_plugins(self)`
  - `do_marketplace` (method, line 104) `def do_marketplace(self, line)`
  - `_mp_list` (method, line 178) `def _mp_list(self, tier_filter)`
  - `_mp_search` (method, line 206) `def _mp_search(self, query)`
  - `_mp_install` (method, line 244) `def _mp_install(self, name)`
  - `_mp_update` (method, line 303) `def _mp_update(self)`
  - `_mp_update_addons` (method, line 336) `def _mp_update_addons(self, args)`
  - `_mp_info` (method, line 354) `def _mp_info(self, name)`
  - `_mp_rate` (method, line 401) `def _mp_rate(self, name, raw_stars)`
  - `_mp_ratings` (method, line 415) `def _mp_ratings(self, name)`
  - `_mp_interactive_config` (method, line 435) `def _mp_interactive_config(self)`
  - `do_marketplace_config` (method, line 447) `def do_marketplace_config(self, line)`
  - `_mp_toggle_addon` (method, line 490) `def _mp_toggle_addon(self, name, enable_state)`
- Depends on: `cli/commands/_base.py`, `cli/marketplace_config.py`, `cli/plugin_tiers.py`, `modules/addon_updater.py`, `modules/module_registry.py`, `utils.py`

## cli/commands/mcp_bridge.py
- Doc: MCP verb bridge — one command language for operators and agents.
- Layer: utility
- Language: py
- Symbols:
  - `_build_auto_populate_parser` (function, line 55) `def _build_auto_populate_parser()`
  - `_build_facts_show_parser` (function, line 72) `def _build_facts_show_parser()`
  - `_build_rag_query_parser` (function, line 89) `def _build_rag_query_parser()`
  - `_build_parquet_query_parser` (function, line 97) `def _build_parquet_query_parser()`
  - `_build_threat_model_parser` (function, line 116) `def _build_threat_model_parser()`
  - `_build_playbook_run_parser` (function, line 129) `def _build_playbook_run_parser()`
  - `McpBridgeCommandSet` (class, line 143) `class McpBridgeCommandSet(LazyOwnCommandSet)`
  - `do_auto_populate` (method, line 151) `def do_auto_populate(self, args)`
  - `do_facts_show` (method, line 261) `def do_facts_show(self, args)`
  - `do_rag_query` (method, line 286) `def do_rag_query(self, args)`
  - `do_parquet_query` (method, line 316) `def do_parquet_query(self, args)`
  - `do_threat_model` (method, line 378) `def do_threat_model(self, args)`
  - `do_playbook_run` (method, line 431) `def do_playbook_run(self, args)`
  - `do_auto_loop` (method, line 489) `def do_auto_loop(self, line)`
  - `do_session_state` (method, line 534) `def do_session_state(self, line)`
  - `do_campaign_sitrep` (method, line 539) `def do_campaign_sitrep(self, line)`
  - `do_timeline` (method, line 544) `def do_timeline(self, line)`
  - `_delegate` (method, line 548) `def _delegate(self, command, line)`
  - `_refresh_aliases` (method, line 556) `def _refresh_aliases(self)`
  - `_executor` (function, line 475) `def _executor(command, host)`
- Depends on: `cli/aliases.py`, `cli/commands/_base.py`, `core/autonomous.py`, `core/config.py`, `modules/intelligence_engine.py`, `modules/lazy_runner.py`, `modules/playbook_engine.py`, `modules/session_rag.py`, `modules/threat_model.py`, `modules/world_model.py`, `skills/lazyown_facts.py`, `skills/lazyown_parquet_db.py`, `utils.py`
- Imported by: `tests/test_cli_assign.py`, `tests/test_loop_auto_orchestrator.py`

## cli/commands/misc_migrated.py
- Doc: misc commands migrated from lazyown.py.
- Layer: utility
- Language: py
- Symbols:
  - `MiscMigratedCommandSet` (class, line 87) `class MiscMigratedCommandSet(LazyOwnCommandSet)`
  - `__getattr__` (function, line 1172) `def __getattr__(name)`
  - `do_notify` (method, line 92) `def do_notify(self, arg)`
  - `do_EOF` (method, line 111) `def do_EOF(self, line)`
  - `_handle_killchain_auto` (method, line 150) `def _handle_killchain_auto(self, spec)`
  - `do_palette` (method, line 179) `def do_palette(self, line)`
  - `do_graph_search` (method, line 204) `def do_graph_search(self, line)`
  - `do_neighbors` (method, line 232) `def do_neighbors(self, line)`
  - `do_god_nodes` (method, line 259) `def do_god_nodes(self, line)`
  - `do_suggest_next` (method, line 278) `def do_suggest_next(self, line)`
  - `do_recommend_next` (method, line 404) `def do_recommend_next(self, line)`
  - `do_explore` (method, line 458) `def do_explore(self, line)`
  - `do_prev` (method, line 489) `def do_prev(self, line)`
  - `do_dashboard` (method, line 526) `def do_dashboard(self, line)`
  - `do_palette_k` (method, line 561) `def do_palette_k(self, line)`
  - `do_browse` (method, line 590) `def do_browse(self, line)`
  - `do_timeline_browser` (method, line 612) `def do_timeline_browser(self, line)`
  - `do_graph_overlay` (method, line 631) `def do_graph_overlay(self, line)`
  - `do_toast_clear` (method, line 651) `def do_toast_clear(self, line)`
  - `do_exit` (method, line 671) `def do_exit(self, arg)`
  - `_persist_chainmode` (method, line 726) `def _persist_chainmode(self, enabled)`
  - `do_banner` (method, line 744) `def do_banner(self, line)`
  - `do_config_banner` (method, line 754) `def do_config_banner(self, line)`
  - `do_aliass` (method, line 798) `def do_aliass(self, line)`
  - `do_graph` (method, line 826) `def do_graph(self, line)`
  - `do_h` (method, line 886) `def do_h(self, arg)`
  - `do_v` (method, line 932) `def do_v(self, arg)`
  - `do_links` (method, line 978) `def do_links(self, line)`
  - `do_news` (method, line 1041) `def do_news(self, line)`
  - `do_check_update` (method, line 1054) `def do_check_update(self, line)`
  - `do_addalias` (method, line 1099) `def do_addalias(self, arglist)`
  - `do_listaliases` (method, line 1151) `def do_listaliases(self, _)`
- Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/autosuggest.py`, `cli/banner_config.py`, `cli/command_chain.py`, `cli/commands/_base.py`, `cli/dashboard_tui.py`, `cli/exploration.py`, `cli/exploration_view.py`, `cli/graph_advisor.py`, `cli/graph_overlay.py`, `cli/ops_commands.py`, `cli/palette.py`, `cli/palette_command.py`, `cli/palette_overlay.py`, `cli/reactive_hints.py`, `cli/recommendation.py`, `cli/recommendation_signals.py`, `cli/sessions_browser.py`, `cli/show.py`, `cli/timeline_browser.py`, `cli/toast_bus.py`, `cli/wizard.py`, `core/config.py`, `core/console.py`, `core/process.py`, `core/safe_exec.py`, `modules/lazy_loop.py`, `modules/module_registry.py`, `modules/payload_factory.py`, `utils.py`
- Imported by: `tests/test_auto_crypto.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_nethelpers_command_set.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`

## cli/commands/mobile_macos.py
- Doc: Mobile & macOS exploitation command set.
- Layer: utility
- Language: py
- Symbols:
  - `MobileMacOSCommandSet` (class, line 96) `class MobileMacOSCommandSet(LazyOwnCommandSet)`
  - `_extract_flag` (function, line 351) `def _extract_flag(args, flag)`
  - `_adb_argv` (function, line 361) `def _adb_argv(serial)`
  - `_is_safe_output_path` (function, line 368) `def _is_safe_output_path(path)`
  - `is_binary_present` (function, line 374) `def is_binary_present(name)`
  - `do_android_enum` (method, line 103) `def do_android_enum(self, line)`
  - `do_android_apk` (method, line 171) `def do_android_apk(self, line)`
  - `do_macos_persist` (method, line 216) `def do_macos_persist(self, line)`
  - `do_macos_keychain` (method, line 274) `def do_macos_keychain(self, line)`
  - `do_macos_tcc` (method, line 323) `def do_macos_tcc(self, line)`
- Depends on: `cli/commands/_base.py`, `core/process.py`, `core/validators.py`, `utils.py`

## cli/commands/module_manager.py
- Doc: Module management commands — search, use, back, and active module context.
- Layer: utility
- Language: py
- Symbols:
  - `ModuleManagerCommandSet` (class, line 36) `class ModuleManagerCommandSet(LazyOwnCommandSet)`
  - `_get_registry` (method, line 42) `def _get_registry(self)`
  - `_get_active_module` (method, line 50) `def _get_active_module(self)`
  - `_get_active_options` (method, line 56) `def _get_active_options(self)`
  - `do_search` (method, line 71) `def do_search(self, line)`
  - `do_use` (method, line 111) `def do_use(self, line)`
  - `do_back` (method, line 162) `def do_back(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/module_registry.py`, `utils.py`

## cli/commands/netattack.py
- Doc: Windows network-attack surface command set: plan, attest, show.
- Layer: utility
- Language: py
- Symbols:
  - `_signing_evidence_path` (function, line 24) `def _signing_evidence_path()`
  - `_world_evidence` (function, line 29) `def _world_evidence()`
  - `NetAttackCommandSet` (class, line 52) `class NetAttackCommandSet(LazyOwnCommandSet)`
  - `do_lazy_netattack` (method, line 59) `def do_lazy_netattack(self, line)`
  - `_attest` (method, line 83) `def _attest(self, args)`
  - `_show_attestations` (method, line 103) `def _show_attestations(self)`
  - `_plan` (method, line 114) `def _plan(self, target)`
- Depends on: `cli/commands/_base.py`, `modules/__init__.py`, `modules/loop_triggers.py`, `modules/world_model.py`, `utils.py`

## cli/commands/nethelpers.py
- Doc: Network helpers extracted from the miscellaneous cluster.
- Layer: utility
- Language: py
- Symbols:
  - `NetworkHelpersCommandSet` (class, line 31) `class NetworkHelpersCommandSet(LazyOwnCommandSet)`
  - `do_ip` (method, line 38) `def do_ip(self, line)`
  - `do_ipp` (method, line 120) `def do_ipp(self, line)`
  - `do_rhost` (method, line 201) `def do_rhost(self, line)`
  - `do_rrhost` (method, line 254) `def do_rrhost(self, line)`
  - `do_addhosts` (method, line 295) `def do_addhosts(self, line)`
  - `do_ip2asn` (method, line 319) `def do_ip2asn(self, line)`
  - `do_ignorearp` (method, line 348) `def do_ignorearp(self, line)`
  - `do_ignoreicmp` (method, line 383) `def do_ignoreicmp(self, line)`
  - `do_acknowledgearp` (method, line 418) `def do_acknowledgearp(self, line)`
  - `do_acknowledgeicmp` (method, line 453) `def do_acknowledgeicmp(self, line)`
- Depends on: `cli/commands/_base.py`, `core/hardening.py`, `utils.py`
- Imported by: `tests/test_nethelpers_command_set.py`

## cli/commands/opsec_cleanup.py
- Doc: OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory, network.
- Layer: utility
- Language: py
- Symbols:
  - `OpsecCleanupCommandSet` (class, line 19) `class OpsecCleanupCommandSet(LazyOwnCommandSet)`
  - `do_opsec_score` (method, line 25) `def do_opsec_score(self, line)`
  - `do_log_tamper` (method, line 97) `def do_log_tamper(self, line)`
  - `do_forensic_clean` (method, line 162) `def do_forensic_clean(self, line)`
  - `do_timestomp` (method, line 219) `def do_timestomp(self, line)`
  - `do_memory_clean` (method, line 288) `def do_memory_clean(self, line)`
  - `do_network_opsec` (method, line 342) `def do_network_opsec(self, line)`
  - `do_auditd_disable` (method, line 445) `def do_auditd_disable(self, line)`
  - `do_sysmon_disable` (method, line 468) `def do_sysmon_disable(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/forensic_cleaner.py`, `modules/log_tamper.py`, `modules/memory_cleaner.py`, `modules/network_opsec.py`, `modules/opsec_scorer.py`, `modules/timestomper.py`

## cli/commands/orchestration.py
- Doc: Orchestration CommandSet: operator-facing surface for the new modules.
- Layer: utility
- Language: py
- Symbols:
  - `OrchestrationConfig` (class, line 37) `class OrchestrationConfig`
  - `_spinner_hints` (function, line 60) `def _spinner_hints(stop, events_path)`
  - `run_with_spinner` (function, line 94) `def run_with_spinner(execute)`
  - `_build_status_bar_parser` (function, line 115) `def _build_status_bar_parser()`
  - `_build_orchestrate_parser` (function, line 128) `def _build_orchestrate_parser()`
  - `OrchestrationCommandSet` (class, line 182) `class OrchestrationCommandSet(LazyOwnCommandSet)`
  - `do_status_bar` (method, line 190) `def do_status_bar(self, args)`
  - `do_orchestrate` (method, line 216) `def do_orchestrate(self, args)`
  - `_resolve_shell` (method, line 263) `def _resolve_shell(self)`
  - `_status_manager` (method, line 278) `def _status_manager(self)`
  - `_orchestrator` (method, line 284) `def _orchestrator(self)`
  - `_status_bar_show` (method, line 290) `def _status_bar_show(self, manager)`
  - `_status_bar_refresh` (method, line 295) `def _status_bar_refresh(self, manager)`
  - `_status_bar_toggle` (method, line 305) `def _status_bar_toggle(self, manager, enabled)`
  - `_format_text` (method, line 314) `def _format_text(result)`
- Depends on: `cli/commands/_base.py`, `cli/reasoning_stream.py`, `core/console.py`
- Imported by: `tests/test_improvements_spec.py`

## cli/commands/params_ops.py
- Doc: Operator administration of the shared parameter catalog.
- Layer: utility
- Language: py
- Symbols:
  - `ParamCommandSet` (class, line 31) `class ParamCommandSet(LazyOwnCommandSet)`
  - `do_param` (method, line 38) `def do_param(self, line)`
- Depends on: `cli/assign.py`, `cli/commands/_base.py`, `core/config.py`, `core/param_registry.py`, `core/payload_schema.py`, `utils.py`
- Imported by: `tests/test_param_registry.py`

## cli/commands/payload_arsenal.py
- Doc: Payload arsenal commands — dotnet, reflective DLL, staged delivery, polymorphic, macOS/Linux...
- Layer: utility
- Language: py
- Symbols:
  - `PayloadArsenalCommandSet` (class, line 23) `class PayloadArsenalCommandSet(LazyOwnCommandSet)`
  - `do_dotnet_payload` (method, line 29) `def do_dotnet_payload(self, line)`
  - `do_arsenal_show` (method, line 114) `def do_arsenal_show(self, line)`
  - `do_staged_delivery` (method, line 172) `def do_staged_delivery(self, line)`
  - `do_polymorphic` (method, line 261) `def do_polymorphic(self, line)`
  - `do_macos_payload` (method, line 328) `def do_macos_payload(self, line)`
  - `do_linux_advanced_payload` (method, line 401) `def do_linux_advanced_payload(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/dotnet_payload.py`, `modules/linux_advanced_payloads.py`, `modules/macos_payloads.py`, `modules/polymorphic_engine.py`, `modules/staged_delivery.py`

## cli/commands/payload_generation.py
- Doc: Payload generation commands — list payloads and generate.
- Layer: utility
- Language: py
- Symbols:
  - `PayloadCommandSet` (class, line 24) `class PayloadCommandSet(LazyOwnCommandSet)`
  - `_get_factory` (method, line 30) `def _get_factory(self)`
  - `do_generate` (method, line 37) `def do_generate(self, line)`
- Depends on: `cli/commands/_base.py`, `modules/payload_factory.py`, `utils.py`

## cli/commands/persist.py
- Doc: Persistence command set (pending).
- Layer: utility
- Language: py
- Symbols:
  - `PersistenceCommandSet` (class, line 26) `class PersistenceCommandSet(LazyOwnCommandSet)`
  - `do_createwebshell` (method, line 33) `def do_createwebshell(self, line)`
  - `do_createrevshell` (method, line 47) `def do_createrevshell(self, line)`
  - `do_createwinrevshell` (method, line 61) `def do_createwinrevshell(self, line)`
  - `do_conptyshell` (method, line 73) `def do_conptyshell(self, line)`
  - `do_pwncatcs` (method, line 89) `def do_pwncatcs(self, line)`
  - `do_revwin` (method, line 99) `def do_revwin(self, line)`
  - `do_wmi_persist` (method, line 112) `def do_wmi_persist(self, line)`
  - `do_wmi_lateral` (method, line 170) `def do_wmi_lateral(self, line)`
  - `do_wmi_scheduled_task` (method, line 209) `def do_wmi_scheduled_task(self, line)`
  - `_extract` (method, line 275) `def _extract(args, flag)`
- Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`


Next: [KB_commands_p4.md](KB_commands_p4.md)
