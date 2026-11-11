# Index (page 4 of 4)
Previous: [INDEX_p3.md](INDEX_p3.md)

| File | Purpose | Subsystem | Symbols | Used by |
|------|---------|-----------|---------|---------|
| `tests/test_reactive_hints_expanded.py` | Tests for cli.reactive_hints — expanded kill-chain tables. | tests | 27 | 0 |
| `tests/test_reactive_lateral_data.py` | Tests for new reactive engine matchers. | tests | 26 | 0 |
| `tests/test_reasoning_stream.py` | Tests for cli/reasoning_stream.py. | tests | 13 | 0 |
| `tests/test_recommendation.py` | Behaviour tests for the unified recommendation engine and its signals. | tests | 36 | 0 |
| `tests/test_recon_plan.py` | Spec coverage for :mod:`cli.recon_plan`. | tests | 34 | 0 |
| `tests/test_repeat_shapes.py` | Stuck-loop shapes contract: AAAA plus ABABAB oscillation detection. | tests | 10 | 0 |
| `tests/test_report_banners_endpoints.py` | Tests for /report and /banners endpoints error handling. | tests | 32 | 0 |
| `tests/test_require_guards.py` | Single-call requirement guards for CommandSet methods. | tests | 5 | 0 |
| `tests/test_resource_script.py` | Tests for modules/resource_script.py — ScriptContext and ResourceScriptEngine. | tests | 32 | 0 |
| `tests/test_retry_session.py` | BDD tests for retry sessions, support relaunch and the retry command set. | tests | 25 | 0 |
| `tests/test_safe_console.py` | Terminal-safe console: colors and glyphs degrade, never leak. | tests | 4 | 0 |
| `tests/test_safe_subprocess.py` | TDD tests for the safe subprocess runner contract. | tests | 11 | 0 |
| `tests/test_safe_subprocess_behavior.py` | BDD behavior scenarios for the safe subprocess contract. | tests | 3 | 0 |
| `tests/test_safety_gates.py` | BDD scoped tests for safety gates C01-C03. | tests | 8 | 0 |
| `tests/test_scope_bound_auto_gate.py` | tests/test_scope_bound_auto_gate.py  Coverage for the fully autonomous engage mode ("real auto... | tests | 37 | 0 |
| `tests/test_scope_deny_priority.py` | Tests for scope denylist priority (engine lab scope + CLI guard). | tests | 11 | 0 |
| `tests/test_scope_guard.py` | Test suite for cli/scope_guard.py. | tests | 46 | 0 |
| `tests/test_scope_guard_integration.py` | Integration tests for the scope guard wired into LazyOwnShell. | tests | 30 | 0 |
| `tests/test_security_alerts_fix.py` | Regression tests for CodeQL alerts #941-#972 (SSRF, TLS, clear-text, ReDoS, paths). | tests | 24 | 0 |
| `tests/test_security_codeql_batch.py` | SDD regression tests for the CodeQL security batch. | tests | 37 | 0 |
| `tests/test_security_hardening.py` | SDD+TDD+BDD tests for security hardening contracts. | tests | 36 | 0 |
| `tests/test_security_hardening_v2.py` | SDD+TDD+BDD tests for security hardening batch v2. | tests | 39 | 0 |
| `tests/test_security_hardening_v3.py` | Security hardening tests — SDD+TDD+BDD for all boy-scout fixes. | tests | 63 | 0 |
| `tests/test_security_hardening_v4.py` | SDD+TDD+BDD tests for security hardening v4 — command execution, URL injection, and path traversal. | tests | 67 | 0 |
| `tests/test_security_hardening_v5.py` | SDD+TDD+BDD tests for CodeQL security batch — weak crypto, clear-text secrets, TLS. | tests | 40 | 0 |
| `tests/test_security_lazyc2.py` | Security tests for the LazyOwn C2 web layer. | tests | 58 | 0 |
| `tests/test_security_sanitizers.py` | Unit tests for :mod:`modules.security_sanitizers`. | tests | 45 | 0 |
| `tests/test_selection_lazyscript.py` | Tests for the LazyscriptSelector. | tests | 10 | 0 |
| `tests/test_selection_module.py` | Tests for the ModuleSelector over the shared module registry bridge. | tests | 10 | 0 |
| `tests/test_selection_technique.py` | Tests for the TechniqueSelector and its playbook_engine helper. | tests | 21 | 0 |
| `tests/test_selection_technique_chain.py` | Tests for TechniqueChainSelector and the focused technique-chain synth. | tests | 16 | 0 |
| `tests/test_selection_wiring.py` | Vertical wiring tests: playbooks, adversaries and apt_chain through the loop. | tests | 13 | 0 |
| `tests/test_selectors_base.py` | Shared selector brain contract: base types, chain selector and cascade. | tests | 9 | 0 |
| `tests/test_selectors_capabilities.py` | Capability selector contracts: playbook, adversary and atomic strategies. | tests | 12 | 0 |
| `tests/test_session_brief.py` | BDD tests for the consolidated session-start brief. | tests | 6 | 0 |
| `tests/test_session_ops_command_set.py` | Session ops command set extraction tests. | tests | 9 | 0 |
| `tests/test_session_secrets.py` | SessionSecretsSpec: Contract for session-scoped secret rotation. | tests | 8 | 0 |
| `tests/test_sessions_browser.py` | Tests for cli/sessions_browser.py. | tests | 8 | 0 |
| `tests/test_shell_semantics.py` | Contract tests for shell-semantics detection and colored child output. | tests | 10 | 0 |
| `tests/test_shellsys_command_set.py` | Shell/sys command set extraction tests. | tests | 9 | 0 |
| `tests/test_short_url_file_containment.py` | Containment contract for short-URL file serving. | tests | 16 | 0 |
| `tests/test_single_implementation.py` | Single-implementation rule for extracted helpers. | tests | 5 | 0 |
| `tests/test_single_source_of_truth.py` | Single-source-of-truth contract tests. | tests | 26 | 0 |
| `tests/test_sink_chain_feed.py` | Chain-feed sink contract: live step visibility and unhandled-failure steering. | tests | 8 | 0 |
| `tests/test_sink_lazy_intel.py` | BDD tests for the dedicated lazy_intel sink. | tests | 13 | 0 |
| `tests/test_sleep_obfuscation.py` | Tests for modules/sleep_obfuscation.py — SleepTechnique, SleepObfuscationConfig... | tests | 41 | 0 |
| `tests/test_socks_proxy.py` | Tests for modules/socks_proxy.py — SocksProxyConfig, SocksSession, SocksValidator... | tests | 52 | 0 |
| `tests/test_status_bar_operators.py` | Tests for the operator-presence segment of cli/status_bar.py. | tests | 9 | 0 |
| `tests/test_structured_logging.py` | Tests for ``core.logging`` — structured JSON-lines logger. | tests | 19 | 0 |
| `tests/test_surface_graph.py` | Tests for the network surface graph reader. | tests | 13 | 0 |
| `tests/test_sync_doc_stats.py` | Tests for the documentation-stats single source of truth. | tests | 7 | 0 |
| `tests/test_themes.py` | Tests for cli/themes.py. | tests | 6 | 0 |
| `tests/test_timeline_browser.py` | Tests for cli/timeline_browser.py. | tests | 8 | 0 |
| `tests/test_tips_engine.py` | Tests for cli.tips_engine — unified post-command suggestion engine. | tests | 67 | 0 |
| `tests/test_toast_bus.py` | Tests for cli/toast_bus.py. | tests | 24 | 0 |
| `tests/test_toastr_unify.py` | BDD tests for the unified toastr presentation layer. | tests | 12 | 0 |
| `tests/test_triage_scheduler.py` | Difficulty-triage scheduler BDD contract. | tests | 9 | 0 |
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
| `utils.py` | Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation date: 09/06/2024... | root | 126 | 113 |

