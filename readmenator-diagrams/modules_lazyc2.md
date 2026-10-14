# modules: lazyc2

modules: lazyc2 groups 123 files (js, py) around StructuredLogConfig, _JsonLineFormatter, __init__, format, _ConsoleFormatter. Automatic encryption of sensitive session data on app open/close.

```mermaid
graph LR
    cli["cli"]
    contrib["contrib"]
    core["core"]
    lazyc2["lazyc2"]
    modules["modules"]
    root["root"]
    scripts["scripts"]
    skills["skills"]
    static["static"]
    tests["tests"]
    cli -- "calls into" --> core
    cli -- "calls into" --> lazyc2
    cli -- "calls into" --> modules
    cli -- "calls into" --> root
    tests -- "calls into" --> cli
    tests -- "calls into" --> core
    tests -- "calls into" --> lazyc2
    tests -- "calls into" --> modules
    tests -- "calls into" --> root
    tests -- "calls into" --> skills
    contrib -- "depends on" --> core
    contrib -- "calls into" --> modules
    core -- "calls into" --> modules
    core -- "calls into" --> root
    lazyc2 -- "depends on" --> core
    lazyc2 -- "calls into" --> modules
    lazyc2 -- "calls into" --> root
    modules -- "calls into" --> contrib
    modules -- "depends on" --> core
    modules -- "calls into" --> lazyc2
    root -- "depends on" --> cli
    root -- "calls into" --> core
    root -- "calls into" --> lazyc2
    root -- "calls into" --> modules
    root -- "calls into" --> skills
    scripts -- "calls into" --> root
    skills -- "depends on" --> core
    skills -- "calls into" --> modules
    skills -- "calls into" --> root
    static -- "calls into" --> modules
    static -- "calls into" --> root
```

## cli (2.1)

cli groups 5 files (py) around AutoCryptoConfig, AutoCryptoEngine, __init__, enabled, is_encrypted. Automatic encryption of sensitive session data on app open/close.

## contrib (2.2)

contrib groups 12 files (py) around _ret_model, truncate_message, _configure_logging, _load_knowledge_base, _save_knowledge_base. parse_github_url: Extrae (owner, repo) de una URL de GitHub.

## core (2.3)

core groups 7 files (py) around StructuredLogConfig, _JsonLineFormatter, __init__, format, _ConsoleFormatter. Lightweight command execution bridge between C2 bots and the LazyOwn CLI shell.

## lazyc2 (2.4)

lazyc2 groups 11 files (py) around CorsConfigError, CorsPolicy, __init__, env, resolve_origins. Beacon communication blueprint for the LazyOwn C2 server.

## modules (2.5)

modules groups 44 files (py) around is_model_missing_error, groq_model_chain, LLMBackendUnavailableError, LLMBackendNotSupportedError, default_model_for. LazyOwn AI Agent - Ultimate Edition Mejoras: Anti-Hang (Timeout), Gestión de Memoria...

## root (2.6)

root groups 7 files (py) around _ux_debug, _parse_bool_setting, _PayloadSettableProxy, __init__, __getattr__. RAGManager: Manages RAG functionality with CAG caching for document processing and...

## scripts (2.7)

scripts groups 1 files (py) around AuditConfig, argparser_commands, audit, main. Audit every registered shell command for dispatch and parser errors.

## skills (2.8)

skills groups 9 files (py) around Config, default, ServiceFact, CredentialFact, ShareFact. Autonomous Campaign Intelligence (ACI) Planner

## static (2.9)

static groups 1 files (js) around P, S, a, a, a.

## tests (2.10)

tests groups 26 files (py) around _make_goal, _patched_paths, _start_patches, _stop_patches, _make_planner. tests/test_aci_planner.py

**Files**:

- cli/auto_crypto.py
- cli/commands/ai.py
- cli/commands/automation.py
- cli/commands/collaboration.py
- cli/headless.py
- contrib/legacy/lazyaddon_creator.py
- contrib/legacy/lazydeepseekcli.py
- contrib/legacy/lazygptcli.py
- contrib/legacy/lazygptcli_unified.py
- contrib/legacy/lazyhoneypot.py
- contrib/legacy/lazyllmchat.py
- contrib/legacy/lazyopenssh77enum2.py
- contrib/legacy/lazyphishingai.py
- contrib/legacy/lazyproxy.py
- contrib/legacy/lazysearch_bot.py
- contrib/legacy/lazyseo.py
- contrib/legacy/lazyssh.py
- core/command_bridge.py
- core/executor.py
- core/llm_budget.py
- core/logging.py
- core/parsers.py
- core/scheduler.py
- core/security.py
- discord_c2.py
- lazy_sentinel4.py
- lazyc2.py
- lazyc2/blueprints/beacon.py
- lazyc2/blueprints/phishing.py
- lazyc2/extensions/short_urls.py
- lazyc2/security/__init__.py
- lazyc2/security/constants.py
- lazyc2/security/cors.py
- lazyc2/security/html_sanitizer.py
- lazyc2/security/https_redirect.py
- lazyc2/security/services.py
- lazyc2/security/trusted_proxy.py
- lazyc2/security/validators.py
- lazyown.py
- modules/agent_runner.py
- modules/ai_fallback.py
- modules/ai_model.py
- modules/c2_profile.py
- modules/collab_bp.py
- modules/colors.py
- modules/compliance.py
- modules/conditional_hooks.py
- modules/credential_reuse.py
- modules/dashboard_bp.py
- modules/engagement_hooks.py
- modules/event_bus.py
- modules/event_consumers.py
- modules/event_engine.py
- modules/hive_invoke.py
- modules/ia_code_analysis.py
- modules/ia_logs_analysis.py
- modules/ia_network_analysis.py
- modules/lazyownerweb.py
- modules/lesson_ingestor.py
- modules/lilsplunky.py
- modules/listener_manager.py
- modules/llm_adapter.py
- modules/llm_client.py
- modules/llm_factory.py
- modules/llm_prompts.py
- modules/logging_config.py
- modules/mcp_agent_bridge.py
- modules/metrics.py
- modules/operator_profiles.py
- modules/pipeline_engine.py
- modules/playbook_executor.py
- modules/recommender.py
- modules/session_state.py
- modules/sidequestion.py
- modules/state_manager.py
- modules/sudo_tiocsti.py
- modules/timeline_narrator.py
- modules/toposwarm_bridge.py
- modules/ttp_coverage.py
- modules/unified_bridge.py
- modules/vuln_bot_cli.py
- modules/vulnbot.py
- modules/yaml_generator.py
- scripts/devtools/command_audit.py
- skills/aci_planner.py
- skills/daemon_health.py
- skills/heartbeat.py
- skills/lazyown_campaign.py
- skills/lazyown_daemon.py
- skills/lazyown_facts.py
- skills/sessions_watcher.py
- skills/tests/test_facts.py
- skills/toposwarm_autonomous.py
- slack_c2_bot.py
- static/js/xterm.js
- telegram_c2.py
- telegram_hermes.py
- tests/test_aci_planner.py
- tests/test_ai_commands_llm.py
- tests/test_auto_crypto.py
- tests/test_collab_and_onboarding.py
- tests/test_conditional_hooks_extended.py
- tests/test_core_command_bridge.py
- tests/test_core_executor.py
- tests/test_cors_behavior.py
- tests/test_cors_policy.py
- tests/test_cors_socketio_regression.py
- tests/test_dashboard_routes.py
- tests/test_html_sanitizer.py
- tests/test_https_redirect.py
- tests/test_lazy_streaming.py
- tests/test_lesson_ingestor.py
- tests/test_llm_adapter_parity.py
- tests/test_llm_budget.py
- tests/test_llm_prompts.py
- tests/test_logging_config.py
- tests/test_metrics.py
- tests/test_pipeline_engine.py
- tests/test_security_lazyc2.py
- tests/test_short_url_file_containment.py
- tests/test_single_implementation.py
- tests/test_structured_logging.py
- tests/test_trusted_proxy.py
