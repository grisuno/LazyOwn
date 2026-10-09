# Index (page 1 of 2)
Pages: [INDEX.md](INDEX.md), [INDEX_p2.md](INDEX_p2.md)

| File | Purpose | Subsystem | Symbols | Used by |
|------|---------|-----------|---------|---------|
| `.claude/skills/run-lazyown/driver.sh` | Build and drive LazyOwn inside its Docker sandbox (Debian container). | misc | 0 | 0 |
| `DEPLOY.sh` | update_section_html: Función para actualizar una sección específica | root | 3 | 0 |
| `__init__.py` | - | root | 0 | 0 |
| `banner.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | root | 3 | 0 |
| `bootstrap.sh` | LazyOwn bootstrap installer (one-liner entry point). | root | 16 | 0 |
| `cli/__init__.py` | LazyOwn CLI infrastructure. | cli | 0 | 8 |
| `cli/aliases.py` | Declarative cmd2 alias loader. | cli | 7 | 10 |
| `cli/assign.py` | ``assign`` business logic. | cli | 1 | 12 |
| `cli/auto_crypto.py` | Automatic encryption of sensitive session data on app open/close. | cli | 12 | 3 |
| `cli/autosuggest.py` | Ghost-text autosuggest engine for the LazyOwn cmd2 shell. | cli | 27 | 5 |
| `cli/banner_config.py` | Configurable Neon Box banner for the LazyOwn interactive shell. | cli | 120 | 6 |
| `cli/chain_mode.py` | Interactive kill-chain chaining coordinator. | cli | 23 | 3 |
| `cli/cli_enhancements.py` | CLI enhancement primitives for the LazyOwn interactive shell. | cli | 69 | 3 |
| `cli/command_chain.py` | Command chain registry: explicit prerequisites and dynamic next steps. | cli | 25 | 4 |
| `cli/command_explorer.py` | Interactive command explorer by phase and goal for the LazyOwn shell. | cli | 7 | 1 |
| `cli/command_form.py` | Textual form-mode launcher for LazyOwn commands. | cli | 31 | 1 |
| `cli/commands/__init__.py` | Phase-scoped CommandSet modules. | commands | 0 | 1 |
| `cli/commands/_base.py` | Base class for phase-scoped ``CommandSet`` modules. | commands | 7 | 85 |
| `cli/commands/_dormancy.py` | Dormancy marker for incrementally migrated command sets. | commands | 2 | 9 |
| `cli/commands/active_directory.py` | Active Directory attack commands — Kerberos, tickets, delegation, DACL, GPO, kerberoasting. | commands | 8 | 0 |
| `cli/commands/ai.py` | Artificial Intelligence command set. | commands | 6 | 1 |
| `cli/commands/anti_forensics.py` | Anti-Forensics command set. | commands | 7 | 0 |
| `cli/commands/applocker_bypass.py` | AppLocker and WDAC bypass command set. | commands | 9 | 0 |
| `cli/commands/audit.py` | Audit-mode CommandSet: fuzzy finder, forms, status tail, transcript grep. | commands | 13 | 1 |
| `cli/commands/automation.py` | Automation command set — credential reuse, conditional hooks, operator profiles. | commands | 13 | 0 |
| `cli/commands/bitm.py` | Browser-in-the-Middle CLI command set. | commands | 8 | 0 |
| `cli/commands/bof_registry.py` | BOF marketplace CommandSet — Beacon Object File discovery, install, and execution. | commands | 12 | 0 |
| `cli/commands/c2_profile.py` | C2 profile CommandSet — extended malleable C2 profiles (TLS, DNS, SMB, WS). | commands | 5 | 0 |
| `cli/commands/caldera.py` | Caldera-style command set — operation lifecycle, TTP coverage, and planner. | commands | 21 | 0 |
| `cli/commands/campaign.py` | Campaign export/import commands — portable engagement packages. | commands | 7 | 0 |
| `cli/commands/catalog.py` | Command catalog — browse all registered commands by keyword, phase or category. | commands | 6 | 0 |
| `cli/commands/cicd.py` | CI/CD Enumeration command set. | commands | 7 | 0 |
| `cli/commands/cli_auth.py` | CLI authentication command set — login/logout/whoami. | commands | 5 | 0 |
| `cli/commands/cloud.py` | Cloud attack command set. | commands | 7 | 1 |
| `cli/commands/cloud_attacks.py` | Cloud attack commands — Azure AD/Entra ID, AWS, GCP, Kubernetes, cross-cloud, SaaS. | commands | 7 | 0 |
| `cli/commands/collaboration.py` | Collaboration CLI commands — multi-operator teamwork from the shell. | commands | 8 | 0 |
| `cli/commands/command_and_control.py` | Command & Control command set. | commands | 7 | 0 |
| `cli/commands/command_and_control_migrated.py` | command_and_control commands migrated from lazyown.py. | commands | 26 | 0 |
| `cli/commands/containers.py` | Container and Kubernetes attack command set. | commands | 7 | 9 |
| `cli/commands/cred.py` | Credential Access command set (pending). | commands | 10 | 0 |
| `cli/commands/cred_migrated.py` | cred commands migrated from lazyown.py. | commands | 33 | 1 |
| `cli/commands/crystal_ball.py` | Crystal Ball CLI command set — privilege escalation vector prediction. | commands | 5 | 0 |
| `cli/commands/daemon_ctl.py` | Autonomous daemon control extracted from the miscellaneous cluster. | commands | 7 | 1 |
| `cli/commands/database.py` | Database commands — workspace isolation, host/service/vuln management, nmap import, export, and... | commands | 15 | 0 |
| `cli/commands/demo.py` | End-to-end demo command — MCP registration plus the golden path. | commands | 2 | 0 |
| `cli/commands/diagnostics.py` | Diagnostics CommandSet (Tier 2 pilot). | commands | 3 | 1 |
| `cli/commands/dns_exfil.py` | DNS exfiltration and covert channel command set. | commands | 12 | 0 |
| `cli/commands/dpapi.py` | DPAPI credential harvesting command set. | commands | 5 | 0 |
| `cli/commands/edr_detect.py` | EDR Detection command set. | commands | 5 | 0 |
| `cli/commands/encoding.py` | Encoding commands extracted from misc_migrated.py. | commands | 15 | 1 |
| `cli/commands/enum.py` | Enumeration command set. | commands | 11 | 22 |
| `cli/commands/estorides.py` | Estorides integration commands — bidirectional feedback loop with passive OSINT. | commands | 9 | 0 |
| `cli/commands/evasive_payload.py` | Auto-Adaptive Payload command set. | commands | 13 | 0 |
| `cli/commands/exfiltration.py` | Data Exfiltration command set. | commands | 37 | 0 |
| `cli/commands/exploit.py` | Exploitation command set (pending activation). | commands | 11 | 0 |
| `cli/commands/exploit_migrated.py` | exploit commands migrated from lazyown.py. | commands | 52 | 0 |
| `cli/commands/exploitgym.py` | ExploitGym CLI command set — real-world exploit benchmark harness. | commands | 10 | 1 |
| `cli/commands/help_ui.py` | Help, tutorial and phase guidance extracted from the miscellaneous cluster. | commands | 16 | 1 |
| `cli/commands/infra.py` | Disposable infrastructure commands -- redirectors, C2, cloud IaC. | commands | 18 | 2 |
| `cli/commands/lab.py` | Lab environment commands -- spin up vulnerable practice targets. | commands | 21 | 2 |
| `cli/commands/lateral.py` | Lateral Movement command set (pending). | commands | 9 | 0 |
| `cli/commands/lateral_migrated.py` | lateral commands migrated from lazyown.py. | commands | 23 | 0 |
| `cli/commands/marketplace.py` | Plugin/addon marketplace commands. | commands | 18 | 0 |
| `cli/commands/mcp_bridge.py` | MCP verb bridge — one command language for operators and agents. | commands | 20 | 0 |
| `cli/commands/misc_migrated.py` | misc commands migrated from lazyown.py. | commands | 32 | 6 |
| `cli/commands/mobile_macos.py` | Mobile & macOS exploitation command set. | commands | 10 | 0 |
| `cli/commands/module_manager.py` | Module management commands — search, use, back, and active module context. | commands | 7 | 0 |
| `cli/commands/nethelpers.py` | Network helpers extracted from the miscellaneous cluster. | commands | 11 | 1 |
| `cli/commands/opsec_cleanup.py` | OPSEC and cleanup commands — scoring, log tamper, forensic cleaner, timestomp, memory, network. | commands | 9 | 0 |
| `cli/commands/orchestration.py` | Orchestration CommandSet: operator-facing surface for the new modules. | commands | 13 | 1 |
| `cli/commands/payload_arsenal.py` | Payload arsenal commands — dotnet, reflective DLL, staged delivery, polymorphic, macOS/Linux... | commands | 7 | 0 |
| `cli/commands/payload_generation.py` | Payload generation commands — list payloads and generate. | commands | 3 | 0 |
| `cli/commands/persist.py` | Persistence command set (pending). | commands | 11 | 0 |
| `cli/commands/persist_migrated.py` | persist commands migrated from lazyown.py. | commands | 25 | 0 |
| `cli/commands/phishing_wizard.py` | Phishing Wizard command set. | commands | 17 | 0 |
| `cli/commands/pivoting.py` | Intelligent Pivoting command set. | commands | 14 | 0 |
| `cli/commands/postexp.py` | Post-Exploitation command set (pending). | commands | 9 | 0 |
| `cli/commands/postexp_migrated.py` | postexp commands migrated from lazyown.py. | commands | 39 | 0 |
| `cli/commands/privilege_escalation.py` | Privilege Escalation command set. | commands | 21 | 1 |
| `cli/commands/purple_team.py` | Purple Team CommandSet: closed-loop offensive detection measurement. | commands | 14 | 0 |
| `cli/commands/pwn.py` | Autonomous exploitation and LOLBAS command set. | commands | 8 | 4 |
| `cli/commands/recon.py` | Reconnaissance command set. | commands | 14 | 0 |
| `cli/commands/recon_migrated.py` | recon commands migrated from lazyown.py. | commands | 30 | 0 |
| `cli/commands/redteam_gym.py` | Red Team Gym CLI command set — gamified pentest training. | commands | 8 | 0 |
| `cli/commands/resource_scripting.py` | Resource script commands — run .ls scripts, record macros, spool output. | commands | 8 | 0 |
| `cli/commands/scan.py` | Scanning command set. | commands | 17 | 0 |
| `cli/commands/scan_migrated.py` | scan commands migrated from lazyown.py. | commands | 52 | 0 |
| `cli/commands/security.py` | OPSEC and security commands — risk scoring, credential sealing, rotation. | commands | 8 | 0 |
| `cli/commands/session_ops.py` | Session and campaign operations extracted from the miscellaneous cluster. | commands | 34 | 1 |
| `cli/commands/shellsys.py` | Local shell and system extracted from the miscellaneous cluster. | commands | 12 | 1 |
| `cli/commands/sleep_obfuscation.py` | Sleep obfuscation CommandSet — beacon memory evasion technique management. | commands | 4 | 0 |
| `cli/commands/socks_proxy.py` | SOCKS proxy CommandSet — beacon tunneling configuration. | commands | 4 | 0 |
| `cli/commands/supply_chain.py` | Supply Chain Attack command set. | commands | 13 | 0 |
| `cli/commands/ux.py` | Usability commands: hud, undo, config_diff, cheat, suggest. | commands | 9 | 0 |
| `cli/config_history.py` | In-memory configuration history with undo and diff. | cli | 9 | 2 |
| `cli/config_status.py` | Simplified configuration status display for the LazyOwn shell. | cli | 6 | 1 |
| `cli/confirm.py` | Shared interactive confirmation helpers with safe non-TTY behaviour. | cli | 2 | 4 |
| `cli/contextual_help.py` | Contextual help system for the LazyOwn shell. | cli | 10 | 2 |
| `cli/dashboard_layout.py` | Responsive layout decisions for the Textual operator dashboard. | cli | 3 | 1 |
| `cli/dashboard_tui.py` | LazyOwn operator dashboard — a full-screen Textual TUI. | cli | 64 | 2 |
| `cli/doctor.py` | Environment health check (preflight doctor) for the LazyOwn framework. | cli | 21 | 1 |
| `cli/engagement_hooks.py` | Curiosity-driven engagement engine for LazyOwn. | cli | 32 | 10 |
| `cli/exploit_advisor.py` | Exploit advisor: connects nmap scan results to exploit search and next-step commands. | cli | 11 | 1 |
| `cli/exploration.py` | Exploration engine: trigger and OS aware addon/tool matching. | cli | 48 | 11 |
| `cli/exploration_view.py` | Rich-based renderers for the exploration engine. | cli | 6 | 2 |
| `cli/fuzzy_match.py` | Non-interactive fuzzy matching reusing the picker's scorer. | cli | 3 | 1 |
| `cli/fuzzy_picker.py` | Curses-based fuzzy dropdown picker for the LazyOwn interactive shell. | cli | 41 | 3 |
| `cli/graph_advisor.py` | Graph-aware advisor backed by the graphify knowledge graph. | cli | 52 | 9 |
| `cli/graph_overlay.py` | Textual overlay over :mod:`cli.graph_advisor`. | cli | 26 | 2 |
| `cli/headless.py` | Headless / non-interactive runner for automated pipelines. | cli | 6 | 1 |
| `cli/killchain.py` | Self-populating kill-chain progress derived from the daemon event stream. | cli | 4 | 2 |
| `cli/lazynmap_post.py` | Post-scan side effects executed at the tail of ``do_lazynmap``. | cli | 9 | 3 |
| `cli/marketplace_config.py` | Interactive marketplace manager for LazyOwn lazyaddons, plugins, and tools. | cli | 46 | 2 |
| `cli/noise_verbs.py` | Canonical non-actionable verb registry for post-command surfaces. | cli | 0 | 4 |
| `cli/ops_commands.py` | Power-user operator commands: ctx, tgrep, phase, note, l00t, pivot, tasks, sitrep, scans. | cli | 53 | 8 |
| `cli/output_mode.py` | Structured output modes and dry-run rendering for CLI commands. | cli | 6 | 2 |
| `cli/palette.py` | Read-only loader for ``cli/command_index.json``. | cli | 11 | 11 |
| `cli/palette_command.py` | Pure logic for the operator-facing ``palette`` command. | cli | 51 | 6 |
| `cli/palette_graph.py` | Graph-aware neighbour lookups for the operator command palette. | cli | 13 | 2 |
| `cli/palette_overlay.py` | Textual Cmd-K palette overlay for the LazyOwn shell. | cli | 24 | 2 |
| `cli/palette_telemetry.py` | Behavioural telemetry derived from ``sessions/LazyOwn_session_report.csv``. | cli | 14 | 3 |
| `cli/phase_labels.py` | Canonical human-readable labels for kill-chain command phases. | cli | 1 | 3 |
| `cli/plugin_tiers.py` | Plugin tiers and operator ratings for the marketplace. | cli | 8 | 3 |
| `cli/protips.py` | Pro tips system for the LazyOwn shell. | cli | 13 | 2 |
| `cli/purple_tui.py` | Purple Team Dashboard — Textual TUI for engagement monitoring. | cli | 15 | 1 |
| `cli/reactive_hints.py` | Non-blocking inline hint renderer for the LazyOwn cmd2 shell. | cli | 15 | 11 |
| `cli/reasoning_stream.py` | Operator-facing view over the autonomous daemon decision log. | cli | 9 | 2 |
| `cli/recommendation.py` | Unified next-best-action engine: the single source of truth for "what next". | cli | 22 | 5 |
| `cli/recommendation_signals.py` | Concrete :class:`cli.recommendation.RecommendationSignal` adapters. | cli | 37 | 8 |
| `cli/recon_plan.py` | Reconnaissance plan generator built on top of :mod:`cli.exploration`. | cli | 18 | 4 |
| `cli/registry.py` | ``cmd2.CommandSet`` discovery and registration for ``cli.commands``. | cli | 2 | 11 |
| `cli/scope_guard.py` | Authorization scope guard for offensive command execution. | cli | 12 | 2 |
| `cli/session_hud.py` | Compact session HUD: the numbers no other command shows. | cli | 9 | 1 |
| `cli/session_resumer.py` | Session resumer for the LazyOwn shell. | cli | 6 | 1 |
| `cli/sessions_browser.py` | Textual browser for the LazyOwn ``sessions/`` directory. | cli | 31 | 2 |
| `cli/show.py` | Pretty-print the live payload for the operator. | cli | 1 | 11 |
| `cli/splash.py` | Animated splash overlay for the LazyOwn first-run experience. | cli | 9 | 2 |
| `cli/status_bar.py` | Persistent operator status bar for the LazyOwn cmd2 shell. | cli | 64 | 3 |
| `cli/style.py` | Centralised TUI style tokens for the LazyOwn operator surface. | cli | 4 | 3 |
| `cli/surface_graph.py` | Network surface graph reader for the LazyOwn shell. | cli | 31 | 2 |
| `cli/surface_tui.py` | Terminal renderer for the LazyOwn network surface graph. | cli | 19 | 1 |
| `cli/themes.py` | Theme registry for the LazyOwn TUI surfaces. | cli | 3 | 15 |
| `cli/timeline_browser.py` | Textual scrubber over ``sessions/LazyOwn_session_report.csv``. | cli | 25 | 2 |
| `cli/tips_engine.py` | Unified post-command tips engine: single coordination point for all suggestion surfaces. | cli | 59 | 5 |
| `cli/toast_bus.py` | Non-blocking toast notification subsystem for the LazyOwn shell. | cli | 38 | 5 |
| `cli/tui_theme.py` | Operator-facing ``tui_theme`` command logic. | cli | 4 | 1 |
| `cli/tutorial.py` | Interactive post-install tutorial for the LazyOwn framework. | cli | 7 | 1 |
| `cli/wizard.py` | Guided first-run setup wizard for the LazyOwn framework. | cli | 45 | 5 |
| `cli/wizard_scope.py` | Partial wizard scope: show current state or edit selected fields only. | cli | 4 | 1 |
| `contrib/legacy/__init__.py` | Legacy module shims — deprecated scripts retained for compatibility. | legacy | 0 | 0 |
| `contrib/legacy/lazy_http_bof.py` | - | legacy | 2 | 0 |
| `contrib/legacy/lazy_packet_image_sniffer.py` | - | legacy | 9 | 0 |
| `contrib/legacy/lazyaddon_creator.py` | parse_github_url: Extrae (owner, repo) de una URL de GitHub. | legacy | 14 | 0 |
| `contrib/legacy/lazyarpspoofing.py` | - | legacy | 7 | 0 |
| `contrib/legacy/lazybinenc.py` | - | legacy | 2 | 0 |
| `contrib/legacy/lazybotcli.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | legacy | 3 | 0 |
| `contrib/legacy/lazybotnet.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | legacy | 16 | 0 |
| `contrib/legacy/lazycam.py` | This code is a portion of frigate Event Video Recorder (fEVR)  Copyright (C) 2021-2022  The... | legacy | 10 | 0 |
| `contrib/legacy/lazycreate_webshell.py` | - | legacy | 0 | 0 |
| `contrib/legacy/lazydeepseekcli.py` | Unified Ollama/DeepSeek client for LazyOwn — merges lazydeepseekcli_local +... | legacy | 16 | 1 |
| `contrib/legacy/lazydisassebler.py` | Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Date: 14/04/2025 Licencia: GPL v3... | legacy | 8 | 0 |
| `contrib/legacy/lazyftpsniff.py` | - | legacy | 5 | 0 |
| `contrib/legacy/lazygalazy.py` | - | legacy | 7 | 0 |
| `contrib/legacy/lazygptcli.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | legacy | 14 | 0 |
| `contrib/legacy/lazygptcli_unified.py` | Unified Groq LLM client for LazyOwn — merges lazygptcli2/3/4/5 + lazyagentAi + lazygpttask +... | legacy | 29 | 1 |
| `contrib/legacy/lazyhoneypot.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | legacy | 15 | 0 |
| `contrib/legacy/lazyhttpreverseshell.py` | - | legacy | 10 | 0 |
| `contrib/legacy/lazykeygen.py` | - | legacy | 5 | 0 |
| `contrib/legacy/lazylfi2rce.py` | - | legacy | 4 | 0 |
| `contrib/legacy/lazyllmchat.py` | _load_model: Load the configured LLM backend through the central factory. | legacy | 30 | 0 |
| `contrib/legacy/lazylogpoisoning.py` | - | legacy | 3 | 0 |
| `contrib/legacy/lazymariadb_rce_cve_2016-662.py` | MySQL / MariaDB / Percona -  Remote Root Code Execution / PrivEsc PoC Exploit (CVE-2016-6662)... | legacy | 3 | 0 |
| `contrib/legacy/lazymidm.py` | - | legacy | 8 | 0 |
| `contrib/legacy/lazymitmap.py` | run_cmd_write: Write a file using sudo. | legacy | 21 | 0 |
| `contrib/legacy/lazynetbios.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | legacy | 7 | 0 |
| `contrib/legacy/lazyntlrelayx.py` | - | legacy | 2 | 0 |
| `contrib/legacy/lazyopenssh77enum2.py` | CVE-2018-15473 SSH User Enumeration by Leap Security (@LeapSecurity) https://leapsecurity.io... | legacy | 5 | 0 |
| `contrib/legacy/lazyphishingai.py` | Author: Gris Iscomeback Email: grisiscomeback[at]gmail[dot]com Creation Date: 09/06/2024... | legacy | 12 | 1 |
| `contrib/legacy/lazyproxy.py` | - | legacy | 9 | 0 |
| `contrib/legacy/lazypwn.py` | - | legacy | 15 | 0 |
| `contrib/legacy/lazypwnkit.py` | rmrf: Elimina recursivamente un directorio y su contenido. | legacy | 5 | 0 |
| `contrib/legacy/lazypyautogui.py` | - | legacy | 0 | 0 |
| `contrib/legacy/lazyreversentlmv2.py` | - | legacy | 2 | 0 |
| `contrib/legacy/lazysearch.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | legacy | 3 | 0 |
| `contrib/legacy/lazysearch_bot.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | legacy | 13 | 0 |
| `contrib/legacy/lazyseo.py` | - | legacy | 9 | 0 |
| `contrib/legacy/lazysmbrelay.py` | - | legacy | 7 | 0 |
| `contrib/legacy/lazysniff.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | legacy | 11 | 0 |
| `contrib/legacy/lazysqli.py` | AUTHOR: jahman EDITED BY grisun0 | legacy | 4 | 0 |
| `contrib/legacy/lazyssh.py` | - | legacy | 1 | 0 |
| `contrib/legacy/lazyvsftp.py` | - | legacy | 3 | 0 |
| `contrib/legacy/lazywerkzeug.py` | - | legacy | 0 | 0 |
| `contrib/legacy/sql.py` | - | legacy | 3 | 0 |
| `core/__init__.py` | Core primitives for the LazyOwn framework. | core | 0 | 1 |
| `core/api_authz.py` | Tenant-bound API authorization for the LazyOwn C2 dashboard. | core | 31 | 4 |
| `core/command_bridge.py` | Lightweight command execution bridge between C2 bots and the LazyOwn CLI shell. | core | 9 | 1 |
| `core/config.py` | Configuration loader and Config wrapper. | core | 17 | 31 |
| `core/console.py` | ANSI color constants and console output helpers. | core | 8 | 49 |
| `core/credential_vault.py` | Credential vault — AES-256-GCM encryption for sensitive config values. | core | 8 | 3 |
| `core/credentials.py` | Credential management utilities for the LazyOwn framework. | core | 13 | 1 |
| `core/crypto.py` | Symmetric primitives used by the framework. | core | 7 | 9 |
| `core/dependencies.py` | Graceful optional-import handling for heavy third-party dependencies. | core | 23 | 3 |
| `core/error_advice.py` | Actionable error advice with fix command and documentation link. | core | 5 | 0 |
| `core/errors.py` | Error taxonomy for the LazyOwn framework. | core | 23 | 1 |
| `core/executor.py` | Centralised subprocess wrapper for the LazyOwn framework. | core | 6 | 1 |
| `core/hardening.py` | Centralized security hardening utilities for the LazyOwn framework. | core | 16 | 17 |
| `core/http.py` | HTTP and API utilities for the LazyOwn framework. | core | 10 | 1 |
| `core/llm_budget.py` | LLM budget cap and per call token counter. | core | 45 | 4 |
| `core/logging.py` | Structured JSON-lines logging for the LazyOwn framework. | core | 12 | 123 |
| `core/network.py` | Network primitives for the LazyOwn framework. | core | 8 | 1 |
| `core/parsers.py` | Parsing utilities for the LazyOwn framework. | core | 21 | 8 |
| `core/payload_schema.py` | Declarative schema and validation for ``payload.json``. | core | 27 | 10 |
| `core/process.py` | Process and subprocess utilities for the LazyOwn framework. | core | 12 | 9 |
| `core/profiles.py` | Runtime profiles: ``light`` vs ``full`` installations. | core | 3 | 3 |
| `core/prompt.py` | Prompt builder for LazyOwn CLI and C2 dashboard banner. | core | 8 | 3 |
| `core/protocols.py` | Stable structural interfaces (PEP 544 ``Protocol``) for high-level orchestration. | core | 12 | 1 |
| `core/safe_exec.py` | Centralized safe command execution for the LazyOwn framework. | core | 12 | 15 |
| `core/safe_subprocess.py` | Safe subprocess runner for the LazyOwn framework. | core | 7 | 6 |
| `core/scheduler.py` | Centralized task scheduler for the LazyOwn framework. | core | 17 | 0 |
| `core/security.py` | Security helpers for LazyOwn — anti-debug, certificate generation. | core | 2 | 0 |
| `core/text_utils.py` | Shared text helpers for terminal surfaces. | core | 1 | 8 |
| `core/validators.py` | Input validators for runtime configuration values. | core | 7 | 9 |
| `deploy/range/ad-mini/traffic-gen.py` | Fake network traffic generator for the AD mini range. | misc | 2 | 0 |
| `discord_c2.py` | - | root | 21 | 0 |
| `external/install_external.sh` | Nombre del script: download_resources.sh Autor: Gris Iscomeback Correo electrónico... | misc | 2 | 0 |
| `fast_run_as_r00t.sh` | — LazyOwn full-stack orchestrator  Speed-run launcher: brings up every core service in a tmux... | root | 12 | 0 |
| `gen_cert.sh` | Verifica si se pasó una IP | root | 0 | 0 |
| `install.sh` | LazyOwn installer. | root | 16 | 0 |
| `key.py` | - | root | 1 | 0 |
| `lazy_sentinel4.py` | RAGManager: Manages RAG functionality with CAG caching for document processing and querying. | root | 47 | 0 |
| `lazyc2.py` | is_insecure_credential: Check for weak or default credentials | root | 263 | 0 |
| `lazyc2/__init__.py` | - | lazyc2 | 0 | 2 |
| `lazyc2/addon_creator.py` | LazyAddon creator contract for the LazyOwn C2 web interface. | lazyc2 | 38 | 3 |
| `lazyc2/app_factory.py` | Flask application factory for the LazyOwn C2 server. | lazyc2 | 9 | 0 |
| `lazyc2/blueprints/__init__.py` | Flask Blueprints for lazydown C2. | blueprints | 0 | 2 |
| `lazyc2/blueprints/addons.py` | LazyAddon creator blueprint for the C2 dashboard. | blueprints | 14 | 3 |
| `lazyc2/blueprints/api.py` | API blueprint for the LazyOwn C2 server. | blueprints | 8 | 3 |
| `lazyc2/blueprints/api_v1.py` | Versioned REST API (``/api/v1``) for the LazyOwn C2 server. | blueprints | 12 | 2 |
| `lazyc2/blueprints/auth.py` | Authentication and authorisation blueprint for the LazyOwn C2 server. | blueprints | 19 | 4 |
| `lazyc2/blueprints/beacon.py` | Beacon communication blueprint for the LazyOwn C2 server. | blueprints | 7 | 1 |
| `lazyc2/blueprints/operations.py` | Operations blueprint — tasks, CVEs, notes, and event management. | blueprints | 13 | 1 |
| `lazyc2/blueprints/phishing.py` | Phishing blueprint for the LazyOwn C2 server. | blueprints | 7 | 1 |
| `lazyc2/blueprints/session_auth.py` | Session-based authentication gate for operator dashboard blueprints. | blueprints | 2 | 2 |
| `lazyc2/extensions/__init__.py` | Shared C2 extension modules. | extensions | 0 | 1 |
| `lazyc2/extensions/decoy.py` | Decoy / honeypot page for unauthenticated visitors. | extensions | 1 | 3 |
| `lazyc2/extensions/short_urls.py` | Short URL management utilities for the C2 phishing module. | extensions | 5 | 1 |
| `lazyc2/extensions/storage.py` | JSON-file storage helpers for the C2 web interface. | extensions | 12 | 1 |
| `lazyc2/extensions/users.py` | User management utilities for the C2 auth module. | extensions | 3 | 2 |
| `lazyc2/models.py` | C2 data models extracted from lazyc2.py. | lazyc2 | 2 | 0 |
| `lazyc2/security/__init__.py` | - | security | 0 | 1 |
| `lazyc2/security/command_allowlist.py` | Command allowlist policy for the LazyOwn C2 ``/api/run`` endpoint. | security | 8 | 3 |
| `lazyc2/security/constants.py` | Security constants and validation patterns for the LazyOwn C2 web layer. | security | 0 | 4 |
| `lazyc2/security/cors.py` | CORS origin allowlist policy for the LazyOwn C2 web layer. | security | 15 | 4 |
| `lazyc2/security/csrf.py` | CSRF protection policy for the LazyOwn C2 web layer. | security | 11 | 4 |
| `lazyc2/security/html_sanitizer.py` | HTML sanitizer backed by ``bleach`` for the LazyOwn C2 web layer. | security | 2 | 2 |
| `lazyc2/security/https_redirect.py` | HTTPS redirect policy for the LazyOwn C2 web layer. | security | 5 | 2 |
| `lazyc2/security/services.py` | Security services for the LazyOwn C2 web layer. | security | 16 | 3 |
| `lazyc2/security/trusted_proxy.py` | Trusted proxy resolver for the LazyOwn C2 web layer. | security | 5 | 2 |
| `lazyc2/security/validators.py` | Input validators for the LazyOwn C2 web layer. | security | 9 | 4 |
| `lazyc2/state.py` | Global C2 server state — namespace for shared mutable objects. | lazyc2 | 0 | 1 |
| `lazygui/__init__.py` | LazyOwn Operator Console. | lazygui | 0 | 0 |
| `lazygui/__main__.py` | Entry point for ``python -m lazygui``. | lazygui | 1 | 0 |
| `lazygui/app.py` | Application bootstrap. | lazygui | 14 | 1 |
| `lazygui/config/__init__.py` | Configuration layer. | config | 0 | 0 |
| `lazygui/config/c2_credentials.py` | C2 auto-generated credentials discovery. | config | 4 | 2 |
| `lazygui/config/constants.py` | Immutable application constants. | config | 14 | 33 |
| `lazygui/config/paths.py` | Filesystem layout resolver. | config | 10 | 6 |
| `lazygui/config/settings.py` | Persisted user settings. | config | 18 | 5 |
| `lazygui/panels/__init__.py` | Dockable panels assembled from the reusable widgets. | panels | 0 | 0 |
| `lazygui/panels/base.py` | Common :class:`QDockWidget` base for every panel. | panels | 4 | 13 |
| `lazygui/panels/campaign_panel.py` | Campaign management panel for the operator console. | panels | 9 | 2 |
| `lazygui/panels/credentials_panel.py` | Credentials and loot panel for the operator console. | panels | 5 | 2 |
| `lazygui/panels/cve_panel.py` | CVE tracker panel for the operator console. | panels | 7 | 2 |
| `lazygui/panels/event_log_panel.py` | Panel hosting the application-wide event log. | panels | 3 | 2 |
| `lazygui/panels/graph_panel.py` | Graph panel for Cobalt Strike-style attack topography visualization. | panels | 7 | 2 |
| `lazygui/panels/history_panel.py` | Command history panel showing beacon command logs. | panels | 4 | 2 |
| `lazygui/panels/killchain_panel.py` | Kill-chain visualization panel for the operator console. | panels | 6 | 2 |
| `lazygui/panels/listeners_panel.py` | Panel that lists the listeners advertised by the backend. | panels | 6 | 2 |
| `lazygui/panels/marketplace_panel.py` | Marketplace panel for YARA rules, Nuclei templates, YAML addons and Lua plugins. | panels | 15 | 2 |
| `lazygui/panels/registry.py` | Registry that owns all dock panels. | panels | 5 | 2 |
| `lazygui/panels/sessions_panel.py` | Panel that lists active sessions reported by the backend. | panels | 10 | 2 |
| `lazygui/panels/terminal_panel.py` | Console panel hosting the :class:`TerminalView` with beacon command support. | panels | 7 | 2 |
| `lazygui/services/__init__.py` | Service layer. | services | 0 | 0 |
| `lazygui/services/backend.py` | Backend abstraction. | services | 20 | 22 |
| `lazygui/services/event_log.py` | In-memory ring buffer for :class:`EventRecord`. | services | 7 | 6 |
| `lazygui/services/factory.py` | Factory for backend instances. | services | 4 | 3 |
| `lazygui/services/local_backend.py` | Local backend that runs the LazyOwn cmd2 console on a PTY. | services | 20 | 2 |
| `lazygui/services/models.py` | Immutable domain types consumed by the UI. | services | 15 | 20 |
| `lazygui/services/teamserver_backend.py` | Teamserver backend with Socket.IO real-time and full HTTP API coverage. | services | 46 | 5 |
| `lazygui/theme/__init__.py` | Theme subsystem. | theme | 0 | 0 |
| `lazygui/theme/manager.py` | Theme registry and runtime application of stylesheets. | theme | 10 | 3 |
| `lazygui/theme/palettes/__init__.py` | Built-in palette registry. | palettes | 1 | 1 |
| `lazygui/theme/palettes/catppuccin_mocha.py` | Catppuccin Mocha palette - warm pastel dark theme. | palettes | 0 | 0 |
| `lazygui/theme/palettes/cobalt_clone.py` | Cobalt Clone palette - homage to the classic command-and-control look. | palettes | 0 | 0 |
| `lazygui/theme/palettes/gruvbox_dark.py` | Gruvbox Dark palette - retro warm contrast theme. | palettes | 0 | 0 |
| `lazygui/theme/palettes/solarized_light.py` | Solarized Light palette - low-contrast daylight option. | palettes | 0 | 0 |
| `lazygui/theme/palettes/tactical_green.py` | Tactical Green palette - the LazyOwn signature look. | palettes | 0 | 0 |
| `lazygui/theme/palettes/tokyo_night.py` | Tokyo Night palette - balanced dark blue theme. | palettes | 0 | 0 |
| `lazygui/theme/qss_builder.py` | Builds a Qt stylesheet string from :class:`ThemeTokens`. | theme | 3 | 2 |
| `lazygui/theme/tokens.py` | Design tokens describing a single theme. | theme | 1 | 11 |
| `lazygui/version.py` | Single source of truth for the package version string. | lazygui | 0 | 2 |
| `lazygui/widgets/__init__.py` | Reusable widgets. | widgets | 0 | 0 |
| `lazygui/widgets/beacon_command_modal.py` | Beacon command modal — send commands to beacons and inspect full history. | widgets | 14 | 1 |
| `lazygui/widgets/command_palette_list.py` | Result list and action model for the command palette. | widgets | 10 | 3 |
| `lazygui/widgets/event_log_view.py` | Read-only viewer for :class:`EventLog` records. | widgets | 6 | 2 |
| `lazygui/widgets/filter_bar.py` | Reusable text-filter bar with debounced ``filter_changed`` signal. | widgets | 6 | 3 |
| `lazygui/widgets/graph_view.py` | Interactive attack topography graph widget. | widgets | 41 | 3 |
| `lazygui/widgets/status_badge.py` | Compact label that reflects a :class:`BackendStatus` value. | widgets | 3 | 2 |
| `lazygui/widgets/terminal_view.py` | ANSI-aware terminal viewer. | widgets | 6 | 2 |
| `lazygui/windows/__init__.py` | Top-level windows and dialogs. | windows | 0 | 0 |
| `lazygui/windows/command_palette_window.py` | Frameless palette window invoked by ``Ctrl+K``. | windows | 6 | 2 |
| `lazygui/windows/connect_dialog.py` | Connection dialog for picking a backend. | windows | 9 | 2 |
| `lazygui/windows/main_window.py` | Operator console main window. | windows | 28 | 2 |
| `lazyown-docker/entrypoint.sh` | LazyOwn Entrypoint Script Initializes LazyOwn framework in a Docker container with tmux sessions | lazyown-docker | 0 | 0 |
| `lazyown-docker/hostdiscover.sh` | - | lazyown-docker | 2 | 0 |
| `lazyown-docker/init.sh` | - | lazyown-docker | 0 | 9 |
| `lazyown-docker/mkdocker.sh` | LazyOwn Dockerizer Script Builds, runs, and manages Docker containers for LazyOwn red teaming... | lazyown-docker | 12 | 0 |
| `lazyown.py` | lazyown  Author: Gris Iscomeback Email: grisiscomeback at gmail dot com Creation Date... | root | 127 | 8 |
| `modules/49803.py` | Exploit Title: OpenPLC 3 - Remote Code Execution (Authenticated) Date: 25/04/2021 Exploit... | modules | 3 | 0 |
| `modules/CVE-2018-15133.php` | - | modules | 0 | 0 |
| `modules/CVE-2023-28432.py` | - | modules | 1 | 0 |
| `modules/LazyOwnExplorer.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 23 | 0 |
| `modules/__init__.py` | - | modules | 0 | 1 |
| `modules/adcs_attacks.py` | Active Directory Certificate Services (AD CS) attack module. | modules | 14 | 1 |
| `modules/agent_runner.py` | LazyOwn AI Agent - Ultimate Edition Mejoras: Anti-Hang (Timeout), Gestión de Memoria, Validación... | modules | 35 | 2 |
| `modules/agent_tool.py` | AgentTool: Representa una herramienta ejecutable por el agente | modules | 4 | 2 |
| `modules/ai_exploit_chain.py` | AI-Driven Exploit Chaining Engine. | modules | 11 | 2 |
| `modules/ai_fallback.py` | LazyOwn AI Fallback Chain | modules | 8 | 2 |
| `modules/ai_model.py` | Concrete language model backends for LazyOwn. | modules | 32 | 6 |
| `modules/amsi.c` | ¡Gracias a Saad! | modules | 10 | 0 |
| `modules/amt_auth_bypass.py` | - | modules | 3 | 0 |
| `modules/apt_playbooks.py` | APT Playbook Engine — map public APT reports to executable Atomic Red Team chains. | modules | 15 | 3 |
| `modules/atomic_enricher.py` | — Enrich techniques.parquet with structured derived columns. | modules | 9 | 4 |
| `modules/auto_pivot.py` | Auto-Pivoting Engine for LazyOwn. | modules | 23 | 2 |
| `modules/auto_purple.py` | Purple Team Closed-Loop — honest measurement of offensive detection. | modules | 40 | 1 |
| `modules/autonomous_exploit_engine.py` | Autonomous Exploitation Engine — AI-powered self-adapting exploit chainer. | modules | 46 | 5 |
| `modules/aws_attacks.py` | AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining. | modules | 11 | 1 |
| `modules/backdoor/backdoor.c` | - | backdoor | 5 | 0 |
| `modules/backdoor/keylogger.h` | - | backdoor | 1 | 1 |
| `modules/backdoor/server.c` | - | backdoor | 1 | 10 |
| `modules/beacon_config_builder.py` | Beacon configuration builder — wires profile engines into beacon compile-time config. | modules | 14 | 2 |
| `modules/beacon_history.py` | Persistent beacon command/result history storage. | modules | 7 | 5 |
| `modules/bin2img.py` | - | modules | 2 | 0 |
| `modules/bitm_engine.py` | Browser-in-the-Middle (BitM) attack engine. | modules | 18 | 1 |
| `modules/bof_registry.py` | Beacon Object File (BOF) registry and marketplace for LazyOwn. | modules | 43 | 2 |
| `modules/bot.py` | GitHub repository discovery client. | modules | 5 | 0 |
| `modules/c2_builder.py` | C2 agent builder with profile-driven compilation and safe templating. | modules | 21 | 3 |
| `modules/c2_messaging_base.py` | SecureSessionManager: Unified session manager for C2 messaging bots. | modules | 13 | 0 |
| `modules/c2_profile.py` | modules/c2_profile.py | modules | 32 | 0 |
| `modules/c2_profile_engine.py` | Extended malleable C2 profile engine with TLS, DNS, SMB, and WebSocket transports. | modules | 47 | 3 |
| `modules/cal.sh` | Función para calcular si un año es bisiesto | modules | 3 | 0 |
| `modules/categories.py` | modules/categories.py | modules | 0 | 7 |
| `modules/cgi-bin/lazywebshell.py` | - | cgi-bin | 0 | 0 |
| `modules/cgi-bin/lazywebshell.sh` | - | cgi-bin | 0 | 0 |
| `modules/cicd_enumerator.py` | CI/CD Pipeline Enumeration Module. | modules | 12 | 1 |
| `modules/cli_auth.py` | CLI authentication module — login against users.json with remember-me. | modules | 18 | 9 |
| `modules/cloud_enum.py` | Native cloud enumeration modules for AWS, Azure, and GCP. | modules | 17 | 1 |
| `modules/collab_bp.py` | modules/collab_bp.py | modules | 49 | 7 |
| `modules/colors.py` | retModel: gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k... | modules | 3 | 7 |
| `modules/command_executor.py` | UnifiedCommandExecutor — shared shell command execution service. | modules | 13 | 0 |
| `modules/compliance.py` | modules/compliance.py | modules | 25 | 1 |
| `modules/conditional_hooks.py` | Conditional Hooks System for LazyOwn (Mythic-style triggers). | modules | 23 | 4 |
| `modules/config_store.py` | Thread-safe singleton facade over core.config for payload.json. | modules | 11 | 1 |
| `modules/credential_reuse.py` | Credential Reuse Engine for LazyOwn. | modules | 16 | 4 |
| `modules/cross_cloud.py` | Cross-cloud identity paths — multi-cloud identity federation abuse. | modules | 10 | 1 |
| `modules/cve_matcher.py` | modules/cve_matcher.py | modules | 12 | 2 |
| `modules/dacl_abuse.py` | DACL/SACL abuse module — ACL manipulation for AD privilege escalation. | modules | 15 | 1 |
| `modules/dashboard_bp.py` | modules/dashboard_bp.py | modules | 13 | 3 |
| `modules/dashboard_engine.py` | Live Network Map Dashboard for LazyOwn. | modules | 16 | 4 |
| `modules/db.py` | SQLite database layer for LazyOwn -- hosts, services, vulns, loot, creds, notes. | modules | 35 | 16 |
| `modules/delegation_attacks.py` | Active Directory delegation enumeration and abuse. | modules | 12 | 1 |
| `modules/detailed_search.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 1 | 0 |
| `modules/detection_feed.py` | Dynamic detection feed for the Detection Oracle. | modules | 13 | 2 |
| `modules/detection_oracle.py` | modules/detection_oracle.py | modules | 17 | 7 |
| `modules/dns_beacon.py` | DNS Beacon — covert C2 channel via DNS tunneling. | modules | 19 | 1 |
| `modules/domain_dominance.py` | Domain Dominance Engine — automated Active Directory takeover. | modules | 30 | 1 |
| `modules/dotnet_payload.py` | .NET/C# payload generation — execute-assembly, inline-assembly, Roslyn compilation. | modules | 12 | 1 |
| `modules/dpapi_harvester.py` | DPAPI credential decryption and harvesting engine. | modules | 19 | 1 |
| `modules/duckdns.sh` | Solicita el TOKEN y el DOMAIN al usuario | modules | 0 | 0 |
| `modules/edr_detector.py` | EDR/AV Detection and Evasion Profiling Engine. | modules | 12 | 1 |
| `modules/eegg.sh` | Definición de colores | modules | 4 | 0 |
| `modules/engagement_hooks.py` | modules/engagement_hooks.py — Engagement narration and notification fabric | modules | 42 | 2 |
| `modules/entra_id_attacks.py` | Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing. | modules | 12 | 1 |
| `modules/estorides_importer.py` | estorides_importer | modules | 40 | 2 |
| `modules/evasion_engine.py` | Advanced Evasion Engine for LazyOwn C2 operations. | modules | 24 | 2 |
| `modules/evasive_payloads.py` | Advanced evasive payload generation with multiple obfuscation strategies. | modules | 16 | 1 |
| `modules/event_bus.py` | UnifiedEventBus — central nervous system connecting all LazyOwn components. | modules | 41 | 7 |
| `modules/event_consumers.py` | Event Consumers — reactive layer that makes EventBus events drive real actions. | modules | 18 | 3 |
| `modules/event_engine.py` | LazyOwn Event Engine | modules | 10 | 5 |
| `modules/evilhttprev.sh` | - | modules | 0 | 0 |
| `modules/exp.c` | gcc exp.c -o exp -l mnl -l nftnl -w | modules | 58 | 0 |
| `modules/exploit_chain.py` | Autonomous exploitation chain engine. | modules | 19 | 1 |
| `modules/exploit_recommender.py` | AI-Powered Exploit Recommendation Engine for LazyOwn. | modules | 16 | 4 |
| `modules/exploitgym_gym.py` | ExploitGym integration — real-world vulnerability-to-exploit benchmark. | modules | 20 | 3 |
| `modules/fast_run_service.sh` | LazyOwn service-mode orchestrator. | modules | 39 | 0 |
| `modules/forensic_cleaner.py` | Forensic artifact cleaner — Prefetch, Shimcache, Amcache, MFT/USN cleanup. | modules | 8 | 1 |
| `modules/gcp_attacks.py` | GCP privilege escalation — service account impersonation, Cloud Functions, GCS enumeration. | modules | 11 | 1 |
| `modules/generate_tools.py` | - | modules | 1 | 0 |
| `modules/gpo_abuse.py` | GPO abuse module — Group Policy Object manipulation for AD persistence and privilege escalation. | modules | 16 | 1 |
| `modules/gui_askpass.sh` | — SUDO_ASKPASS helper for LazyOwn MCP  Used by: sudo -A <script>  (set SUDO_ASKPASS to this... | modules | 5 | 0 |
| `modules/hash_cracker.py` | Hash cracking pipeline — John the Ripper and Hashcat integration. | modules | 17 | 2 |
| `modules/hive_invoke.py` | modules/hive_invoke.py | modules | 7 | 0 |
| `modules/hostdiscover.sh` | - | modules | 2 | 0 |
| `modules/ia_code_analysis.py` | CodeAnalyzer: Analyzes source code in a directory and its subdirectories. | modules | 8 | 0 |
| `modules/ia_logs_analysis.py` | Author: Your Name Email: youremail@example.com Creation Date: 10/06/2024 License: GPL v3... | modules | 7 | 0 |
| `modules/ia_network_analysis.py` | Autor: grisun0 Fecha de creación: 30/01/2025 Licencia: GPL v3  Descripción: Bot de monitoreo de... | modules | 4 | 0 |
| `modules/icmp_client.py` | encrypt_data: Encrypt bytes with AES-256-GCM returning ``nonce \|\| ciphertext \|\| tag``. | modules | 7 | 0 |
| `modules/icmp_server.py` | encrypt_data: Encrypt bytes with AES-256-GCM returning ``nonce \|\| ciphertext \|\| tag``. | modules | 9 | 2 |
| `modules/img2bin.py` | - | modules | 2 | 0 |
| `modules/integrations/__init__.py` | LazyOwn integrations — bridges to external platforms and tools. | integrations | 0 | 0 |
| `modules/integrations/misp_export.py` | modules/integrations/misp_export.py | integrations | 38 | 3 |
| `modules/integrations/nuclei_bridge.py` | modules/integrations/nuclei_bridge.py | integrations | 29 | 3 |
| `modules/integrations/nuclei_parser.py` | Nuclei JSON output parser — feeds scan results into DB, WorldModel, and recommender. | integrations | 17 | 2 |
| `modules/integrations/searchsploit.py` | modules/integrations/searchsploit.py | integrations | 27 | 2 |
| `modules/intelligence_engine.py` | IntelligenceEngine — unified collection→analysis→intelligence pipeline. | modules | 27 | 4 |
| `modules/internal_discover.sh` | - | modules | 0 | 0 |
| `modules/iptables_portforward.sh` | - | modules | 1 | 0 |
| `modules/jwtexploit.py` | - | modules | 0 | 0 |
| `modules/k8s_attacks.py` | Kubernetes attack module — RBAC enumeration, pod escape, etcd access, Helm abuse. | modules | 11 | 1 |
| `modules/kerberoasting.py` | Advanced Kerberoasting — targeted SPN enumeration, AES-only attacks, hashcat integration. | modules | 18 | 1 |
| `modules/kerberos_core.py` | Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. | modules | 35 | 2 |
| `modules/kerberos_tickets.py` | Kerberos ticket forgery attacks — silver, golden, diamond, sapphire tickets. | modules | 34 | 1 |
| `modules/kill_chain_viz.py` | SVG / HTML kill-chain visualizer — generates standalone HTML with embedded SVG. | modules | 5 | 1 |
| `modules/killchain.py` | Unified kill-chain — single source of truth consumed by all surfaces. | modules | 21 | 16 |
| `modules/kivi.py` | - | modules | 3 | 0 |
| `modules/lazy_rbac.py` | modules/lazy_rbac.py | modules | 86 | 9 |
| `modules/lazyatack.sh` | Nombre del script: lazyatack.sh Autor: Gris Iscomeback Correo electrónico... | modules | 30 | 0 |
| `modules/lazybrutesshuserenum.sh` | Función para manejar el interruptor de señal Ctrl+C | modules | 0 | 0 |
| `modules/lazyclonewars.sh` | Lista de repositorios (nombre y URL) | modules | 0 | 0 |
| `modules/lazycloud.py` | Cloud-native attack module for AWS, Azure, and GCP. | modules | 26 | 1 |
| `modules/lazycurl.sh` | Nombre del script: lazycurl.sh Autor: Gris Iscomeback Correo electrónico... | modules | 3 | 0 |
| `modules/lazyencoder_decoder.py` | - | modules | 10 | 5 |
| `modules/lazyevilwimrm.sh` | execute_evil_winrm: Función para ejecutar evil-winrm y verificar la salida | modules | 1 | 0 |
| `modules/lazygat.sh` | Nombre del script: lazygath.sh Autor: Gris Iscomeback Correo electrónico... | modules | 0 | 0 |
| `modules/lazyk8s.py` | Container and Kubernetes attack module. | modules | 32 | 1 |
| `modules/lazylynis.sh` | Verificar si se proporcionó un argumento para el host remoto | modules | 1 | 0 |
| `modules/lazymasscan.sh` | Nombre del script: lazymasscan.sh Autor: Gris Iscomeback Correo electrónico... | modules | 4 | 0 |
| `modules/lazymobilerevshell.sh` | Verificar si se pasaron los argumentos de IP y puerto | modules | 0 | 0 |
| `modules/lazynmap.sh` | Nombre del script: lazynmap.sh Autor: Gris Iscomeback Correo electrónico... | modules | 8 | 0 |
| `modules/lazyown_bprfuzzer.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 15 | 0 |
| `modules/lazyown_bridge.py` | modules/lazyown_bridge.py | modules | 43 | 6 |
| `modules/lazyown_metaextract0r.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 9 | 0 |
| `modules/lazyown_parquet_tool.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 4 | 0 |
| `modules/lazyownclient.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 6 | 0 |
| `modules/lazyownerweb.py` | - | modules | 3 | 0 |
| `modules/lazyownserver.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 6 | 0 |
| `modules/lazypsexec.sh` | execute_psexec: Función para ejecutar psexec y verificar la salida | modules | 1 | 0 |
| `modules/lazyreverse_shell.sh` | Nombre del script: lazyreverse_shell.sh Autor: Gris Iscomeback Correo electrónico... | modules | 2 | 0 |
| `modules/lazyrtpflood.sh` | - | modules | 0 | 0 |
| `modules/lazyvpnshield.sh` | Author: Nisrin Ahmed aka Wh1teDrvg0n Modify: grisun0 | modules | 7 | 0 |
| `modules/lazywps.sh` | - | modules | 1 | 0 |
| `modules/legacy/__init__.py` | Backward-compatibility shims for deprecated scripts. | misc | 0 | 0 |
| `modules/lesson_ingestor.py` | Lesson ingestion bridge between EpisodeReflectionEngine and MoERouter. | modules | 11 | 2 |
| `modules/lilsplunky.py` | Author: Your Name Email: youremail@example.com Creation Date: 14/04/2025 License: GPL v3... | modules | 14 | 0 |
| `modules/linux_advanced_payloads.py` | Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants. | modules | 17 | 1 |
| `modules/listener_manager.py` | Multi-listener manager for LazyOwn C2. | modules | 22 | 2 |
| `modules/live_surface.py` | Live attack-surface graph derived from the world model. | modules | 7 | 3 |
| `modules/llm_adapter.py` | LLM adapter facade — single import point for all LLM backends used by lazyc2. | modules | 15 | 6 |
| `modules/llm_client.py` | LazyOwn Unified LLM Client | modules | 11 | 4 |
| `modules/llm_evaluator.py` | — Records LLM decisions and their outcomes, computes quality metrics, and exports fine-tuning... | modules | 28 | 2 |
| `modules/llm_factory.py` | LLM backend factory and selection utilities. | modules | 21 | 18 |
| `modules/llm_prompts.py` | Canonical prompt-template and knowledge-base contract for LLM consumers. | modules | 28 | 4 |
| `modules/log_tamper.py` | Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log. | modules | 9 | 1 |
| `modules/logging_config.py` | Centralized logging configuration for the LazyOwn framework. | modules | 21 | 25 |
| `modules/macos_payloads.py` | macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC. | modules | 16 | 1 |
| `modules/mario.py` | - | modules | 1 | 0 |
| `modules/mcp_agent_bridge.py` | LazyOwn MCP Agent Bridge | modules | 21 | 2 |
| `modules/memory_cleaner.py` | Memory artifact cleanup — process memory wipe, environment variable scrub, clipboard clear. | modules | 7 | 1 |
| `modules/memory_store.py` | — Episodic memory for the LazyOwn auto_loop. | modules | 33 | 2 |
| `modules/metrics.py` | LazyOwn metrics surface. | modules | 24 | 6 |
| `modules/mfa_bypass.py` | MFA Bypass Toolkit — techniques for circumventing multi-factor authentication. | modules | 10 | 1 |
| `modules/mkcloudflaretunnel.sh` | Download cloudflared and create a tunnel to localhost on a specified port. | modules | 0 | 0 |
| `modules/module_registry.py` | Unified module registry for LazyOwn — catalog, search, use/run workflow. | modules | 29 | 6 |
| `modules/moe_router.py` | modules/moe_router.py | modules | 39 | 5 |
| `modules/morse.py` | Morse code conversion service with interactive driver. | modules | 7 | 0 |
| `modules/mysql_hookandroot_lib.c` | reverse_shell: fork & send a bash shell to the attacker before starting mysqld | modules | 6 | 0 |
| `modules/network_opsec.py` | Network OPSEC — proxy chain enforcement, canary detection, traffic randomization. | modules | 12 | 1 |
| `modules/nmap2csv.py` | This file is part of nmaptocsv. | modules | 44 | 0 |
| `modules/obs_parser.py` | modules/obs_parser.py | modules | 41 | 9 |
| `modules/ooficesod0woodo.py` | - | modules | 0 | 0 |
| `modules/operation.py` | Caldera-style operation lifecycle: create, start, pause, resume, stop, status. | modules | 23 | 1 |
| `modules/operator_profiles.py` | Multi-operator profile management for LazyOwn team server. | modules | 20 | 1 |
| `modules/opsec_scorer.py` | OPSEC scoring engine — pre-execution noise assessment and gated scoring. | modules | 36 | 4 |
| `modules/payload_factory.py` | Native payload generation framework — stagers, stages, singles, formats. | modules | 32 | 6 |
| `modules/phishing_orchestrator.py` | Smart Phishing Campaign Orchestrator. | modules | 23 | 3 |
| `modules/pipeline_engine.py` | modules/pipeline_engine.py — Declarative YAML pipelines for LazyOwn | modules | 80 | 5 |
| `modules/planner.py` | Fact-based planner — decides the next ability to run. | modules | 14 | 1 |
| `modules/playbook_engine.py` | modules/playbook_engine.py | modules | 31 | 6 |
| `modules/playbook_executor.py` | Playbook Executor — bridges MITRE ATT&CK playbooks to the pipeline engine. | modules | 25 | 0 |
| `modules/polymorphic_engine.py` | Polymorphic code generation engine — shellcode mutation and obfuscation. | modules | 19 | 1 |
| `modules/privesc_predictor.py` | Crystal Ball — privilege escalation vector prediction engine. | modules | 17 | 1 |
| `modules/professional_report.py` | Professional Red Team Report Generator. | modules | 22 | 2 |
| `modules/r.sh` | Obtener la versión del kernel actual | modules | 1 | 9 |

Next: [INDEX_p2.md](INDEX_p2.md)
