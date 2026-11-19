# Index (page 4 of 4)
Previous: [INDEX_p3.md](INDEX_p3.md)

| File | Purpose | Subsystem | Symbols | Used by |
|------|---------|-----------|---------|---------|
| `tests/test_loop_cli_catalog.py` | BDD tests for planner prompt visibility into routable CLI verbs. | tests | 7 | 0 |
| `tests/test_loop_cold_overview.py` | Cold debounce + planner overview parity (lazy 0.3.8 coldgraph). | tests | 6 | 0 |
| `tests/test_loop_decision_log.py` | Tests for the reproducible loop decision ledger and planner determinism. | tests | 24 | 0 |
| `tests/test_loop_deterministic_mode.py` | Tests for the reproducible loop mode that prefers heuristic steps. | tests | 18 | 0 |
| `tests/test_loop_evidence_wiring.py` | BDD tests for the loop evidence loop-closure wiring. | tests | 19 | 0 |
| `tests/test_loop_exit_gate.py` | Honest loop endings: exit-code mapping, autonomous gate and headless runner. | tests | 16 | 0 |
| `tests/test_loop_fire_pending.py` | Vertical test: fire-pending intelligence drives a real auto_loop round. | tests | 14 | 0 |
| `tests/test_loop_force_graph.py` | Loop ForceGraph context regression tests (lazy 0.3.12 fidelity). | tests | 4 | 0 |
| `tests/test_loop_guard_audit.py` | Guard audit filters + tool_use_id source jump (lazy 0.3.11/0.3.12 parity). | tests | 4 | 0 |
| `tests/test_loop_guardrails.py` | Loop guardrails: repetition detection, EDR pacing, target caps, vector fact memory. | tests | 18 | 0 |
| `tests/test_loop_intent_delete.py` | Intent delete modes regression tests (lazy 0.3.12 parity). | tests | 4 | 0 |
| `tests/test_loop_lazymode_first.py` | Code-mode (lazymode) is the worker's first option. | tests | 9 | 0 |
| `tests/test_loop_llm_resilience.py` | LLM retry layers, wall-clock settle, stall-guard (lazy 0.3.8/0.3.9 parity). | tests | 19 | 0 |
| `tests/test_loop_manager.py` | Tests for modules.loop_manager — safe autonomous loop orchestration. | tests | 51 | 0 |
| `tests/test_loop_manager_outcome.py` | Loop manager outcome propagation: workspace result.json drives status. | tests | 15 | 0 |
| `tests/test_loop_mentions.py` | Lazy mentions multi-type search and scroll pagination. | tests | 2 | 0 |
| `tests/test_loop_multi_target.py` | Multi-target loop entry: scope-file parsing, validation and caps. | tests | 6 | 0 |
| `tests/test_loop_nmap_guard.py` | Loop guardrails: command repair and bounded scanning retests. | tests | 8 | 0 |
| `tests/test_loop_objective_wiring.py` | Loop wiring fidelity: objective queue and Hermes draft consumption. | tests | 12 | 0 |
| `tests/test_loop_preflight.py` | Target preflight for loops and auto_pwn: lab state and TCP reachability. | tests | 10 | 0 |
| `tests/test_loop_progress.py` | Loop milestone panel: inferred stage states stay honest. | tests | 11 | 0 |
| `tests/test_loop_scope_traffic_evidence.py` | Scope ownership, port-aware traffic search, role-based evidences (lazy parity). | tests | 7 | 0 |
| `tests/test_loop_spawn_side.py` | Multi-session chat, persistent side questions, spawn inheritance (lazy 0.3.9). | tests | 4 | 0 |
| `tests/test_loop_store_race.py` | Store file writes stay atomic under parallel workers (race regression). | tests | 2 | 0 |
| `tests/test_loop_supervision.py` | Supervision upgrades: repetition watchdog, stack priors, prompt masking. | tests | 9 | 0 |
| `tests/test_loop_target_authority.py` | Target authority: --target rebinds payload rhost and scope. | tests | 13 | 0 |
| `tests/test_loop_technique_deterministic.py` | Technique intents resolve deterministically, not via the model. | tests | 8 | 0 |
| `tests/test_loop_trigger_hints.py` | BDD for the cve_hot trigger hint fingerprints. | tests | 16 | 0 |
| `tests/test_loop_worker_traces.py` | Worker cross-work trace tools (lazy 0.3.10 parity). | tests | 8 | 0 |
| `tests/test_marketplace_config.py` | Marketplace registry and settings: formats, toggles, CRUD. | tests | 10 | 0 |
| `tests/test_mcp_auto_loop_wrapper.py` | MCP auto_loop wrapper contract: one runner, no dual engines. | tests | 13 | 0 |
| `tests/test_mcp_dispatch.py` | call_tool dispatches through the handler registry. | tests | 11 | 0 |
| `tests/test_mcp_improvements.py` | Tests for the high/medium/low impact MCP improvements. | tests | 34 | 0 |
| `tests/test_mcp_lazy.py` | Contract for the unified MCP lazy-import helper. | tests | 11 | 0 |
| `tests/test_mcp_recommender_embed.py` | Contract tests for the MCP sitrep recommender embedding. | tests | 8 | 0 |
| `tests/test_mcp_tools_registry.py` | Contract for the one-file-per-tool MCP registry (``skills/mcp_tools``). | tests | 11 | 0 |
| `tests/test_mediation.py` | Mediator pattern contract tests for the mediation package. | tests | 52 | 0 |
| `tests/test_memory_semantics.py` | BDD tests for hashing embeddings and hybrid episodic recall. | tests | 14 | 0 |
| `tests/test_metasploitable_gym.py` | Metasploitable 2 gym BDD contract: one exploit, one chain, one index entry. | tests | 6 | 0 |
| `tests/test_metasploitable_migrations.py` | Unit tests for the Metasploitable 2 gym migrations module. | tests | 10 | 0 |
| `tests/test_metrics.py` | Tests for ``modules/metrics.py``. | tests | 14 | 0 |
| `tests/test_metrics_aware_selector.py` | Tests for ``MetricsAwareSelector`` in ``skills/autonomous_daemon.py``. | tests | 24 | 0 |
| `tests/test_module_registry.py` | Tests for modules.module_registry — ModuleInfo, ModuleRegistry, search, summary. | tests | 29 | 0 |
| `tests/test_module_registry_bridge.py` | Module-registry loop bridge: corpus mentions enter planning as intents. | tests | 9 | 0 |
| `tests/test_moe_rl_swan.py` | tests/test_moe_rl_swan.py | tests | 59 | 0 |
| `tests/test_moe_router_check_regression.py` | Regression coverage for ``modules.moe_router.ExpertAvailabilityChecker._check``. | tests | 6 | 0 |
| `tests/test_mutation_verification.py` | Mutation verification contracts. | tests | 5 | 0 |
| `tests/test_nethelpers_command_set.py` | Network helpers command set extraction tests. | tests | 9 | 0 |
| `tests/test_no_shell_execution.py` | Contract tests: no os.system and no manual sys.stdout reassignment. | tests | 8 | 0 |
| `tests/test_nuclei_parser.py` | Tests for modules/integrations/nuclei_parser.py | tests | 21 | 0 |
| `tests/test_objective_bootstrap.py` | Contract tests for modules/loop/objective_bootstrap.py. | tests | 9 | 0 |
| `tests/test_opencode_backend.py` | Contract tests for the OpenCode Zen LLM backend. | tests | 16 | 0 |
| `tests/test_opencode_mcp_harness.py` | Opencode shim harness tool tests. | tests | 5 | 0 |
| `tests/test_ops_loot_phase.py` | Tests for unified loot, cred-graph view, and quantitative phase progress. | tests | 22 | 0 |
| `tests/test_opsec_scorer.py` | Tests for modules/opsec_scorer.py | tests | 13 | 0 |
| `tests/test_opsec_scorer_consolidated.py` | Consolidated OPSEC scorer contract tests (SDD/TDD/BDD). | tests | 22 | 0 |
| `tests/test_orchestrator_api.py` | Integration tests for the orchestrator REST API (``/api/v1/orchestrator``). | tests | 12 | 0 |
| `tests/test_orchestrator_pacing.py` | Pacing tab: jitter and sleeper controls round-trip through set_pacing. | tests | 12 | 0 |
| `tests/test_orchestrator_triggers.py` | BDD tests for the orchestrator Triggers tab. | tests | 6 | 0 |
| `tests/test_orchestrator_yaml.py` | Orchestrator YAML BDD contract: profiles, stages, limits and CLI wiring. | tests | 13 | 0 |
| `tests/test_outcome_attribution.py` | Tests for Observer-style failure attribution and verb demotion. | tests | 16 | 0 |
| `tests/test_outcome_bus.py` | Outcome bus BDD contract: one event, every surface, failure isolation. | tests | 25 | 0 |
| `tests/test_pacing.py` | Configurable pacing: EdrPacer ranges, jitter scaling, sleeper windows. | tests | 14 | 0 |
| `tests/test_packaging.py` | Packaging and project-foundation tests. | tests | 67 | 0 |
| `tests/test_palette_overlay.py` | Tests for cli/palette_overlay.py. | tests | 10 | 0 |
| `tests/test_param_registry.py` | tests/test_param_registry.py  Contract suite for the shared parameter registry. | tests | 54 | 0 |
| `tests/test_payload_factory.py` | Tests for modules.payload_factory — PayloadFactory, PayloadTemplate, format conversion. | tests | 32 | 0 |
| `tests/test_payload_schema.py` | Tests for the ``core.payload_schema`` validation layer. | tests | 53 | 0 |
| `tests/test_payload_write_lock.py` | Concurrency guard for :func:`core.config.save_payload`. | tests | 4 | 0 |
| `tests/test_phase1_data_gaps.py` | Phase 1 data-gap closure: SDD + TDD + BDD tests. | tests | 58 | 0 |
| `tests/test_phase_labels.py` | Tests for cli.phase_labels — canonical phase display labels contract. | tests | 5 | 0 |
| `tests/test_php2shell_addon.py` | tests/test_php2shell_addon.py  Validation suite for the php2shell lazyaddon. | tests | 42 | 0 |
| `tests/test_pi_leg.py` | pi loop-leg contract tests. | tests | 15 | 0 |
| `tests/test_pipeline_engine.py` | tests/test_pipeline_engine.py  Coverage for Pillar 3 (declarative pipelines)... | tests | 65 | 0 |
| `tests/test_placeholder_coverage.py` | Placeholder coverage across every registry that resolves ``{tokens}``. | tests | 8 | 0 |
| `tests/test_planner_initial_access.py` | Deterministic initial-access intent: auto_pwn fires without an LLM. | tests | 16 | 0 |
| `tests/test_playbook_admin.py` | Playbook YAML administration: scan, create, update, delete, validate. | tests | 6 | 0 |
| `tests/test_playbook_chain.py` | Playbook lowering: phases[].steps[] actions and atomic tests become validated chains executed by... | tests | 10 | 0 |
| `tests/test_plugin_loader_safety.py` | Marketplace placeholder substitution must be shell-safe. | tests | 7 | 0 |
| `tests/test_plugin_tiers.py` | Tests for marketplace plugin tiers and operator ratings. | tests | 12 | 0 |
| `tests/test_poc_registry.py` | PoC verb registry contract tests. | tests | 29 | 0 |
| `tests/test_policy_planner_signal.py` | Policy planner signal contract: ranked categories become safe intents. | tests | 10 | 0 |
| `tests/test_profiles.py` | Tests for runtime install profiles (``core.profiles``). | tests | 11 | 0 |
| `tests/test_progress_ledger.py` | Tests for modules.progress_ledger — objective-progress strike rule. | tests | 13 | 0 |
| `tests/test_prompt_readline_markers.py` | Regression tests for readline marker handling in the Neon Box prompt. | tests | 8 | 0 |
| `tests/test_prompt_refresh.py` | Contract tests for live prompt refresh after a payload change. | tests | 9 | 0 |
| `tests/test_pwntomate_tools.py` | Regression guard for pwntomate tool templates (tools/*.tool). | tests | 8 | 0 |
| `tests/test_rea_mcp.py` | Tests for the lazyown_rea MCP tool (REA reverse-engineering skill). | tests | 27 | 0 |
| `tests/test_reaction_bridge.py` | BDD tests for the reaction bridge (planner injections + cred reuse). | tests | 8 | 0 |
| `tests/test_reactive_engine_semantic.py` | Tests for the semantic context advisor in ``modules/reactive_engine.py``. | tests | 13 | 0 |
| `tests/test_reactive_hints.py` | Tests for cli/reactive_hints.py. | tests | 31 | 0 |
| `tests/test_reactive_hints_expanded.py` | Tests for cli.reactive_hints — expanded kill-chain tables. | tests | 27 | 0 |
| `tests/test_reactive_lateral_data.py` | Tests for new reactive engine matchers. | tests | 26 | 0 |
| `tests/test_reasoning_stream.py` | Tests for cli/reasoning_stream.py. | tests | 13 | 0 |
| `tests/test_recommendation.py` | Behaviour tests for the unified recommendation engine and its signals. | tests | 36 | 0 |
| `tests/test_recon_plan.py` | Spec coverage for :mod:`cli.recon_plan`. | tests | 34 | 0 |
| `tests/test_repeat_shapes.py` | Stuck-loop shapes contract: AAAA plus ABABAB oscillation detection. | tests | 10 | 0 |
| `tests/test_report_autogen.py` | Tests for the engagement report auto-generation contract. | tests | 12 | 0 |
| `tests/test_report_banners_endpoints.py` | Tests for /report and /banners endpoints error handling. | tests | 32 | 0 |
| `tests/test_require_guards.py` | Single-call requirement guards for CommandSet methods. | tests | 5 | 0 |
| `tests/test_resource_script.py` | Tests for modules/resource_script.py — ScriptContext and ResourceScriptEngine. | tests | 32 | 0 |
| `tests/test_retry_session.py` | BDD tests for retry sessions, support relaunch and the retry command set. | tests | 25 | 0 |
| `tests/test_rl_trainer_singleton_contract.py` | Watchdog: the RL trainer and MoE router are single shared singletons. | tests | 3 | 0 |
| `tests/test_safe_console.py` | Terminal-safe console: colors and glyphs degrade, never leak. | tests | 4 | 0 |
| `tests/test_safe_subprocess.py` | TDD tests for the safe subprocess runner contract. | tests | 11 | 0 |
| `tests/test_safe_subprocess_behavior.py` | BDD behavior scenarios for the safe subprocess contract. | tests | 3 | 0 |
| `tests/test_safety_gates.py` | BDD scoped tests for safety gates C01-C03. | tests | 8 | 0 |
| `tests/test_scan_brief.py` | Tests for the loop scan-reuse layer and the nmap scan brief module. | tests | 8 | 0 |
| `tests/test_scope_bound_auto_gate.py` | tests/test_scope_bound_auto_gate.py  Coverage for the fully autonomous engage mode ("real auto... | tests | 37 | 0 |
| `tests/test_scope_deny_priority.py` | Tests for scope denylist priority (engine lab scope + CLI guard). | tests | 11 | 0 |
| `tests/test_scope_guard.py` | Test suite for cli/scope_guard.py. | tests | 46 | 0 |
| `tests/test_scope_guard_integration.py` | Integration tests for the scope guard wired into LazyOwnShell. | tests | 30 | 0 |
| `tests/test_sdk_facade.py` | Behaviour tests for the LazyOwn programmatic SDK facade. | tests | 15 | 0 |
| `tests/test_security_alerts_fix.py` | Regression tests for CodeQL alerts #941-#972 (SSRF, TLS, clear-text, ReDoS, paths). | tests | 24 | 0 |
| `tests/test_security_codeql_batch.py` | SDD regression tests for the CodeQL security batch. | tests | 37 | 0 |
| `tests/test_security_hardening.py` | SDD+TDD+BDD tests for security hardening contracts. | tests | 36 | 0 |
| `tests/test_security_hardening_v2.py` | SDD+TDD+BDD tests for security hardening batch v2. | tests | 39 | 0 |
| `tests/test_security_hardening_v3.py` | Security hardening tests — SDD+TDD+BDD for all boy-scout fixes. | tests | 63 | 0 |
| `tests/test_security_hardening_v4.py` | SDD+TDD+BDD tests for security hardening v4 — command execution, URL injection, and path traversal. | tests | 67 | 0 |
| `tests/test_security_hardening_v5.py` | Security hardening v5: operator credential and channel contracts. | tests | 28 | 0 |
| `tests/test_security_lazyc2.py` | Security tests for the LazyOwn C2 web layer. | tests | 58 | 0 |
| `tests/test_security_sanitizers.py` | Unit tests for :mod:`modules.security_sanitizers`. | tests | 51 | 0 |
| `tests/test_selection_bridge.py` | Tests for the shared bridge selector. | tests | 13 | 0 |
| `tests/test_selection_lazyscript.py` | Tests for the LazyscriptSelector. | tests | 10 | 0 |
| `tests/test_selection_module.py` | Tests for the ModuleSelector over the shared module registry bridge. | tests | 10 | 0 |
| `tests/test_selection_parquet.py` | Tests for the shared parquet (session-history) selector. | tests | 14 | 0 |
| `tests/test_selection_technique.py` | Tests for the TechniqueSelector and its playbook_engine helper. | tests | 21 | 0 |
| `tests/test_selection_technique_chain.py` | Tests for TechniqueChainSelector and the focused technique-chain synth. | tests | 16 | 0 |
| `tests/test_selection_wiring.py` | Vertical wiring tests: playbooks, adversaries and apt_chain through the loop. | tests | 13 | 0 |
| `tests/test_selectors_base.py` | Shared selector brain contract: base types, chain selector and cascade. | tests | 11 | 0 |
| `tests/test_selectors_capabilities.py` | Capability selector contracts: playbook, adversary and atomic strategies. | tests | 12 | 0 |
| `tests/test_session_brief.py` | BDD tests for the consolidated session-start brief. | tests | 6 | 0 |
| `tests/test_session_ops_command_set.py` | Session ops command set extraction tests. | tests | 9 | 0 |
| `tests/test_session_reclaim.py` | Contract tests for the audited sessions cleanup planner. | tests | 18 | 0 |
| `tests/test_session_secrets.py` | SessionSecretsSpec: Contract for session-scoped secret rotation. | tests | 8 | 0 |
| `tests/test_sessions_browser.py` | Tests for cli/sessions_browser.py. | tests | 8 | 0 |
| `tests/test_shell_params_seeding.py` | Regression guard: the shell seeds ``self.params`` from the one config source. | tests | 4 | 0 |
| `tests/test_shell_semantics.py` | Contract tests for shell-semantics detection and colored child output. | tests | 10 | 0 |
| `tests/test_shell_session_store.py` | Resumable, hash-identified shell sessions. | tests | 10 | 0 |
| `tests/test_shellsys_command_set.py` | Shell/sys command set extraction tests. | tests | 9 | 0 |
| `tests/test_short_url_file_containment.py` | Containment contract for short-URL file serving. | tests | 16 | 0 |
| `tests/test_sidequest.py` | Tests for read-only side questions over immutable decision checkpoints. | tests | 13 | 0 |
| `tests/test_single_implementation.py` | Single-implementation rule for extracted helpers. | tests | 5 | 0 |
| `tests/test_single_source_of_truth.py` | Single-source-of-truth contract tests. | tests | 26 | 0 |
| `tests/test_sink_chain_feed.py` | Chain-feed sink contract: live step visibility and unhandled-failure steering. | tests | 8 | 0 |
| `tests/test_sink_lazy_intel.py` | BDD tests for the dedicated lazy_intel sink. | tests | 13 | 0 |
| `tests/test_sleep_obfuscation.py` | Tests for modules/sleep_obfuscation.py — SleepTechnique, SleepObfuscationConfig... | tests | 41 | 0 |
| `tests/test_socks_proxy.py` | Tests for modules/socks_proxy.py — SocksProxyConfig, SocksSession, SocksValidator... | tests | 52 | 0 |
| `tests/test_stall_dump.py` | Tests for the stall watchdog dump showing the last executed commands. | tests | 8 | 0 |
| `tests/test_status_bar_operators.py` | Tests for the operator-presence segment of cli/status_bar.py. | tests | 9 | 0 |
| `tests/test_structured_logging.py` | Tests for ``core.logging`` — structured JSON-lines logger. | tests | 19 | 0 |
| `tests/test_surface_graph.py` | Tests for the network surface graph reader. | tests | 13 | 0 |
| `tests/test_sync_doc_stats.py` | Tests for the documentation-stats single source of truth. | tests | 7 | 0 |
| `tests/test_target_os.py` | Contract tests for modules/loop/target_os.py. | tests | 22 | 0 |
| `tests/test_themes.py` | Tests for cli/themes.py. | tests | 6 | 0 |
| `tests/test_timeline_browser.py` | Tests for cli/timeline_browser.py. | tests | 8 | 0 |
| `tests/test_tips_engine.py` | Tests for cli.tips_engine — unified post-command suggestion engine. | tests | 67 | 0 |
| `tests/test_toast_bus.py` | Tests for cli/toast_bus.py. | tests | 24 | 0 |
| `tests/test_toastr_unify.py` | BDD tests for the unified toastr presentation layer. | tests | 12 | 0 |
| `tests/test_toolchain_pins.py` | Contract: one ruff/mypy version across every tooling surface. | tests | 5 | 0 |
| `tests/test_triage_scheduler.py` | Difficulty-triage scheduler BDD contract. | tests | 11 | 0 |
| `tests/test_trigger_policy.py` | BDD contract tests for the declarative trigger policy. | tests | 7 | 0 |
| `tests/test_trusted_proxy.py` | TDD tests for the trusted proxy resolver contract. | tests | 11 | 0 |
| `tests/test_ttpscope_bridge.py` | TTPScope bridge contract: validators, fallbacks, addon schema. | tests | 9 | 0 |
| `tests/test_tui_splash.py` | Tests for cli.splash — the animated first-run overlay. | tests | 17 | 0 |
| `tests/test_tui_style.py` | Tests for the cli/style semantic token layer. | tests | 8 | 0 |
| `tests/test_tui_theme_command.py` | Tests for the cli.tui_theme command logic. | tests | 19 | 0 |
| `tests/test_tui_themes.py` | Tests for the four new themes added on top of the original four. | tests | 15 | 0 |
| `tests/test_unified_bridge_delegate.py` | Contract tests for UnifiedBridge.delegate agent polling. | tests | 9 | 0 |
| `tests/test_unified_dashboard.py` | Tests for modules/unified_dashboard.py. | tests | 18 | 0 |
| `tests/test_utils_import_silent.py` | utils as a library: importing it must never parse the importer's argv. | tests | 2 | 0 |
| `tests/test_verb_catalog.py` | BDD contract tests for the operator verb catalog. | tests | 20 | 0 |
| `tests/test_verb_manifest.py` | BDD tests for the typed verb manifest store. | tests | 13 | 0 |
| `tests/test_viral_adoption.py` | Viral adoption assets: GIFs, smoke script, drift CI, launch kit. | tests | 7 | 0 |
| `tests/test_vuln_mitigations.py` | Regression suite for the GitHub code-scanning mitigations. | tests | 28 | 0 |
| `tests/test_vulnbot_fallback.py` | SDD spec and BDD scenarios for the VulnBot orchestrator-governed CLI. | tests | 25 | 0 |
| `tests/test_winbox_gym.py` | Contract tests for the WinBox gym catalogue, adapter and matrix runner. | tests | 70 | 0 |
| `tests/test_wire_capture.py` | Tests for durable raw wire capture and its TrafficLog wiring. | tests | 11 | 0 |
| `tests/test_wizard_binary_check.py` | tests/test_wizard_binary_check.py  Tests for the wizard binary-readiness check added to... | tests | 26 | 0 |
| `tests/test_wizard_llm.py` | Contract tests for the wizard LLM provider setup step. | tests | 31 | 0 |
| `tests/test_world_diff_retest.py` | World-diff retest loop contract: detected changes steer the planner. | tests | 4 | 0 |
| `tests/test_world_model_extended.py` | Tests for extended WorldModel methods: set_os_hint, get_host, get_hosts_summary. | tests | 22 | 0 |
| `tests/test_writeback_hygiene.py` | Worker writeback hygiene: listing walls never become facts, finding PoCs or bound evidence. | tests | 19 | 0 |
| `tests/test_xss_sanitization.py` | Untrusted data rendered into the DOM must be neutralized. | tests | 8 | 0 |
| `tools/contract_check.py` | Contract conformance checker for single-file LAZY port modules. | tools | 2 | 0 |
| `tools/extract_cluster.py` | Extract a named cluster of do_* methods from a CommandSet module. | tools | 4 | 0 |
| `tools/gen_demo_gifs.py` | Generate LazyOwn demo GIFs without external services. | tools | 3 | 1 |
| `tools/gen_demo_gifs_extra.py` | Additional LazyOwn demo GIFs. | tools | 1 | 0 |
| `tools/generate_metasploitable_gym.py` | Generate the Metasploitable 2 gym catalogue. | tools | 6 | 0 |
| `tools/set_lazyaddon_updates.py` | Set or check the ``update`` flag on every lazyaddon YAML. | tools | 3 | 0 |
| `user_split.sh` | - | root | 0 | 0 |
| `utils.py` | Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024... | root | 127 | 119 |

