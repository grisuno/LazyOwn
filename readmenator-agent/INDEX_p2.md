# Index (page 2 of 3)
Previous: [INDEX.md](INDEX.md)

| File | Purpose | Subsystem | Symbols | Used by |
|------|---------|-----------|---------|---------|
| `modules/jwtexploit.py` | - | modules | 0 | 0 |
| `modules/k8s_attacks.py` | Kubernetes attack module — RBAC enumeration, pod escape, etcd access, Helm abuse. | modules | 11 | 1 |
| `modules/kerberoasting.py` | Advanced Kerberoasting — targeted SPN enumeration, AES-only attacks, hashcat integration. | modules | 18 | 1 |
| `modules/kerberos_core.py` | Native Kerberos protocol library — AS-REQ, TGS-REQ, ticket parsing, encryption. | modules | 35 | 2 |
| `modules/kerberos_tickets.py` | Kerberos ticket forgery attacks — silver, golden, diamond, sapphire tickets. | modules | 34 | 1 |
| `modules/kill_chain_viz.py` | SVG / HTML kill-chain visualizer — generates standalone HTML with embedded SVG. | modules | 5 | 1 |
| `modules/killchain.py` | Unified kill-chain — single source of truth consumed by all surfaces. | modules | 25 | 24 |
| `modules/kivi.py` | - | modules | 3 | 0 |
| `modules/lab_runtime.py` | Lab runtime: Docker lifecycle for practice targets and cyber ranges. | modules | 19 | 2 |
| `modules/lazy_agent.py` | Agentic tool-calling bridge for the loop and the main agent. | modules | 32 | 3 |
| `modules/lazy_bridge.py` | Bidirectional LAZY <-> LazyOwn bridge. | modules | 21 | 6 |
| `modules/lazy_checks.py` | Validation plans as data: re-read observed checks through version math. | modules | 4 | 1 |
| `modules/lazy_cli_bridge.py` | Full CLI catalog for the Lazy autonomous loop. | modules | 14 | 8 |
| `modules/lazy_creds.py` | Default-credential knowledge base for LazyOwn. | modules | 7 | 0 |
| `modules/lazy_cve_feed.py` | Keyless CVE intelligence feeds and version-aware service correlation. | modules | 26 | 4 |
| `modules/lazy_engine.py` | Lazy autonomous loop engine: single orchestrator for lazy_* commands. | modules | 1 | 38 |
| `modules/lazy_findings.py` | Engagement findings ledger: state machine plus reproducible evidence. | modules | 27 | 2 |
| `modules/lazy_heat.py` | Heat tiers and version math for CVE correlation. | modules | 11 | 7 |
| `modules/lazy_hostscore.py` | Host heat score: deterministic 0-100 priority for every known host. | modules | 5 | 2 |
| `modules/lazy_installer.py` | Capability installer for the Lazy autonomous loop. | modules | 6 | 3 |
| `modules/lazy_intel.py` | Intel feed from the Lazy autonomous loop. | modules | 14 | 6 |
| `modules/lazy_ledger.py` | Freshness ledger: TTL windows per verb and target for the loop worker. | modules | 11 | 3 |
| `modules/lazy_loop.py` | Lazy autonomous loop for LazyOwn. | modules | 486 | 70 |
| `modules/lazy_match_policy.py` | Match policy doctrine: what may claim a match and what stays a lead. | modules | 14 | 1 |
| `modules/lazy_mentions.py` | LAZY chat mentions with multi-type search and scroll pagination. | modules | 15 | 4 |
| `modules/lazy_netattack.py` | Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay. | modules | 12 | 1 |
| `modules/lazy_oob.py` | Local OOB canary for blind SSRF/RCE detection. | modules | 18 | 0 |
| `modules/lazy_orchestrator_feedback.py` | Organic orchestrator training from loop usage. | modules | 11 | 5 |
| `modules/lazy_osinfer.py` | Target OS inference and OS-aware verb gating. | modules | 11 | 0 |
| `modules/lazy_proxy.py` | Recording HTTP/HTTPS proxy for the autonomous loop. | modules | 67 | 5 |
| `modules/lazy_rbac.py` | modules/lazy_rbac.py | modules | 86 | 10 |
| `modules/lazy_reaper.py` | Reaper: expire lazy-loop tasks whose process proves dead. | modules | 3 | 2 |
| `modules/lazy_roles.py` | Lazy specialist roles for the autonomous loop. | modules | 4 | 2 |
| `modules/lazy_runner.py` | Single execution path for ``lazy_loop`` and ``auto_loop``. | modules | 41 | 10 |
| `modules/lazy_sandbox.py` | Per-task Docker sandbox for the Lazy autonomous loop. | modules | 12 | 2 |
| `modules/lazy_scope.py` | Lab-only default scope for autonomous loop targets. | modules | 17 | 1 |
| `modules/lazy_skill_mirror.py` | Mirror LazyOwn skills for Hermes discovery. | modules | 7 | 1 |
| `modules/lazy_skills.py` | Skill context injection for planner/worker prompts. | modules | 7 | 4 |
| `modules/lazy_summarizer.py` | Bounded chain summarizer for the Lazy autonomous loop. | modules | 5 | 0 |
| `modules/lazy_surface_diff.py` | Surface snapshot and diff: what changed about a host since last look. | modules | 9 | 0 |
| `modules/lazy_triage.py` | Triage doctrine: evidence floors, verdict algebra and signature dedup. | modules | 10 | 1 |
| `modules/lazy_verify.py` | Structured read-only verification of loop findings. | modules | 8 | 0 |
| `modules/lazy_world_diff.py` | World-surface diff: host snapshots, change detection, ghost liveness. | modules | 22 | 7 |
| `modules/lazyatack.sh` | Nombre del script: lazyatack.sh Autor: Gris Iscomeback Correo electrónico... | modules | 30 | 0 |
| `modules/lazybrutesshuserenum.sh` | Función para manejar el interruptor de señal Ctrl+C | modules | 0 | 0 |
| `modules/lazyclonewars.sh` | Lista de repositorios (nombre y URL) | modules | 0 | 0 |
| `modules/lazycloud.py` | Cloud-native attack module for AWS, Azure, and GCP. | modules | 26 | 1 |
| `modules/lazycurl.sh` | Nombre del script: lazycurl.sh Autor: Gris Iscomeback Correo electrónico... | modules | 3 | 0 |
| `modules/lazydorks.py` | LazyDorks: target-aware Google and GitHub dork generator for LazyOwn. | modules | 4 | 0 |
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
| `modules/lazyownerweb.py` | - | modules | 3 | 0 |
| `modules/lazypassgen.py` | LazyPassGen: target-aware weak-password generator for LazyOwn. | modules | 5 | 0 |
| `modules/lazypoophish.py` | LazyPoophish: phishing fallback delivery for the LazyOwn autonomous loop. | modules | 3 | 0 |
| `modules/lazypsexec.sh` | execute_psexec: Función para ejecutar psexec y verificar la salida | modules | 1 | 0 |
| `modules/lazyreverse_shell.sh` | Nombre del script: lazyreverse_shell.sh Autor: Gris Iscomeback Correo electrónico... | modules | 2 | 0 |
| `modules/lazyrtpflood.sh` | - | modules | 0 | 0 |
| `modules/lazyshortener.py` | LazyShortener: URL shortener bridge for LazyOwn phishing delivery. | modules | 2 | 1 |
| `modules/lazyvpnshield.sh` | Author: Nisrin Ahmed aka Wh1teDrvg0n Modify: grisun0 | modules | 7 | 0 |
| `modules/lazywps.sh` | - | modules | 1 | 0 |
| `modules/legacy/__init__.py` | Backward-compatibility shims for deprecated scripts. | misc | 0 | 0 |
| `modules/lesson_ingestor.py` | Lesson ingestion bridge between EpisodeReflectionEngine and MoERouter. | modules | 11 | 2 |
| `modules/lilsplunky.py` | Author: Your Name Email: youremail@example.com Creation Date: 14/04/2025 License: AGPL v3... | modules | 14 | 0 |
| `modules/linux_advanced_payloads.py` | Advanced Linux payloads — LD_PRELOAD rootkits, eBPF, PAM backdoors, kernel implants. | modules | 17 | 1 |
| `modules/listener_manager.py` | Multi-listener manager for LazyOwn C2. | modules | 22 | 2 |
| `modules/live_surface.py` | Live attack-surface graph derived from the world model. | modules | 7 | 3 |
| `modules/llm_adapter.py` | LLM adapter facade — single import point for all LLM backends used by lazyc2. | modules | 16 | 7 |
| `modules/llm_client.py` | LazyOwn Unified LLM Client | modules | 12 | 4 |
| `modules/llm_evaluator.py` | — Records LLM decisions and their outcomes, computes quality metrics, and exports fine-tuning... | modules | 28 | 2 |
| `modules/llm_factory.py` | LLM backend factory and selection utilities. | modules | 30 | 30 |
| `modules/llm_orchestrator.py` | Orchestrator-governed LLM failover chain for every AI module. | modules | 21 | 8 |
| `modules/llm_pool.py` | Ordered LLM failover pool with health-aware skipping. | modules | 20 | 9 |
| `modules/llm_prompts.py` | Canonical prompt-template and knowledge-base contract for LLM consumers. | modules | 28 | 5 |
| `modules/log_tamper.py` | Log tampering — Windows Event Log, Linux journald/auditd, macOS unified log. | modules | 9 | 1 |
| `modules/logging_config.py` | Centralized logging configuration for the LazyOwn framework. | modules | 21 | 23 |
| `modules/loop_ai_bridge.py` | Single edge between the autonomous loop and the LazyOwn AI stack. | modules | 28 | 7 |
| `modules/loop_guardrails.py` | Adaptive guardrails for the autonomous loop. | modules | 36 | 5 |
| `modules/loop_manager.py` | Parallel autonomous loop orchestration for the LazyOwn C2 dashboard. | modules | 31 | 2 |
| `modules/loop_progress.py` | Rich Live milestone panel for the autonomous loop. | modules | 15 | 4 |
| `modules/loop_triggers.py` | TriggerStore: persistent loop triggers extracted from the loop core. | modules | 16 | 8 |
| `modules/macos_payloads.py` | macOS payload generation — .app bundles, persistence, TCC bypass, Swift/ObjC. | modules | 16 | 1 |
| `modules/mario.py` | - | modules | 1 | 0 |
| `modules/mcp_agent_bridge.py` | LazyOwn MCP Agent Bridge | modules | 21 | 2 |
| `modules/mediation/__init__.py` | Mediation layer for LazyOwn cross-module coordination. | mediation | 0 | 4 |
| `modules/mediation/chain_mediator.py` | Specialised mediator for the APT chain pipeline. | mediation | 8 | 3 |
| `modules/mediation/contracts.py` | Mediation contracts: the abstractions every participant depends on. | mediation | 12 | 2 |
| `modules/mediation/feedback_mediator.py` | Specialised mediator for step-ordering feedback coordination. | mediation | 3 | 2 |
| `modules/mediation/hub.py` | Thin routing hub for specialised mediators. | mediation | 8 | 3 |
| `modules/mediation/intel_mediator.py` | specialised mediator for recon-intel coordination. | mediation | 9 | 2 |
| `modules/mediation/telemetry_mediator.py` | Specialised mediator for loop telemetry coordination. | mediation | 14 | 2 |
| `modules/memory_cleaner.py` | Memory artifact cleanup — process memory wipe, environment variable scrub, clipboard clear. | modules | 7 | 1 |
| `modules/memory_embeddings.py` | Hashing-trick text embeddings for episodic memory recall. | modules | 7 | 2 |
| `modules/memory_store.py` | — Episodic memory for the LazyOwn auto_loop. | modules | 38 | 3 |
| `modules/metasploitable_gym.py` | Metasploitable 2 gym catalogue loader and matrix validator. | modules | 9 | 3 |
| `modules/metasploitable_migrations.py` | Idempotent migrations for the Metasploitable 2 gym container. | modules | 5 | 2 |
| `modules/metrics.py` | LazyOwn metrics surface. | modules | 24 | 6 |
| `modules/mfa_bypass.py` | MFA Bypass Toolkit — techniques for circumventing multi-factor authentication. | modules | 10 | 1 |
| `modules/mkcloudflaretunnel.sh` | Download cloudflared and create a tunnel to localhost on a specified port. | modules | 0 | 0 |
| `modules/module_registry.py` | Unified module registry for LazyOwn — catalog, search, use/run workflow. | modules | 30 | 8 |
| `modules/moe_router.py` | modules/moe_router.py | modules | 39 | 6 |
| `modules/morse.py` | Morse code conversion service with interactive driver. | modules | 7 | 0 |
| `modules/mysql_hookandroot_lib.c` | reverse_shell: fork & send a bash shell to the attacker before starting mysqld | modules | 6 | 0 |
| `modules/network_opsec.py` | Network OPSEC — proxy chain enforcement, canary detection, traffic randomization. | modules | 12 | 1 |
| `modules/nmap2csv.py` | This file is part of nmaptocsv. | modules | 44 | 0 |
| `modules/notify.py` | Stateless multi-channel notifier for finding events. | modules | 17 | 7 |
| `modules/nuclei_templates_sync.py` | Sync community Nuclei template collections into the LazyOwn marketplace. | modules | 16 | 0 |
| `modules/obs_parser.py` | modules/obs_parser.py | modules | 42 | 10 |
| `modules/ooficesod0woodo.py` | - | modules | 0 | 0 |
| `modules/operation.py` | Caldera-style operation lifecycle: create, start, pause, resume, stop, status. | modules | 23 | 1 |
| `modules/operator_profiles.py` | Multi-operator profile management for LazyOwn team server. | modules | 20 | 1 |
| `modules/opsec_scorer.py` | OPSEC scoring engine — pre-execution noise assessment and gated scoring. | modules | 36 | 5 |
| `modules/orchestrator_config.py` | Operator configuration for the loop core: profiles, stages and auto verbs. | modules | 39 | 20 |
| `modules/osint_enrich.py` | Keyless OSINT enrichment for finding evidence. | modules | 13 | 2 |
| `modules/outcome_bus.py` | Single fan-out contract for engagement outcomes. | modules | 17 | 34 |
| `modules/payload_factory.py` | Native payload generation framework — stagers, stages, singles, formats. | modules | 32 | 7 |
| `modules/phishing_orchestrator.py` | Smart Phishing Campaign Orchestrator. | modules | 23 | 4 |
| `modules/pipeline_engine.py` | modules/pipeline_engine.py — Declarative YAML pipelines for LazyOwn | modules | 80 | 5 |
| `modules/planner.py` | Fact-based planner — decides the next ability to run. | modules | 28 | 7 |
| `modules/playbook_admin.py` | Safe CRUD for the YAML playbooks under ``playbooks/``. | modules | 18 | 2 |
| `modules/playbook_engine.py` | modules/playbook_engine.py | modules | 31 | 6 |
| `modules/playbook_executor.py` | Playbook Executor — bridges MITRE ATT&CK playbooks to the pipeline engine. | modules | 25 | 0 |
| `modules/polymorphic_engine.py` | Polymorphic code generation engine — shellcode mutation and obfuscation. | modules | 19 | 1 |
| `modules/privesc_predictor.py` | Crystal Ball — privilege escalation vector prediction engine. | modules | 17 | 1 |
| `modules/professional_report.py` | Professional Red Team Report Generator. | modules | 24 | 3 |
| `modules/progress_ledger.py` | Objective-progress ledger: qualitative strikes against goal stagnation. | modules | 17 | 2 |
| `modules/r.sh` | Obtener la versión del kernel actual | modules | 1 | 9 |
| `modules/reaction_bridge.py` | Reaction bridge between the reactive engine and the loop planner. | modules | 9 | 2 |
| `modules/reactive_engine.py` | modules/reactive_engine.py | modules | 42 | 9 |
| `modules/recommender.py` | LazyOwn Smart Command Recommender | modules | 4 | 1 |
| `modules/redteam_gym.py` | Red Team Gym — gamified pentest training mode. | modules | 30 | 8 |
| `modules/reflective_dll.py` | Reflective DLL loading — load PE from memory without touching disk. | modules | 27 | 0 |
| `modules/resource_script.py` | Enhanced resource script engine — variables, conditionals, loops, macros. | modules | 21 | 3 |
| `modules/retry_session.py` | Retry sessions - safely relaunch a failed verb or a failed run. | modules | 10 | 3 |
| `modules/reverse-shell.c` | reverse_shell_init: call_usermodehelper function is used to create user mode processes from... | modules | 2 | 0 |
| `modules/revshell.c` | - | modules | 2 | 0 |
| `modules/rich_tui.py` | Rich-based live TUI dashboard for LazyOwn campaign monitoring. | modules | 14 | 1 |
| `modules/rl_trainer.py` | modules/rl_trainer.py | modules | 31 | 5 |
| `modules/rootkit/mr.c` | - | rootkit | 33 | 0 |
| `modules/rootkit/mrhyde.c` | original_dirent: ifndef HIDE_DIR define HIDE_DIR ".rootkit_dir" endif ifndef HIDE_USER define... | rootkit | 38 | 0 |
| `modules/rootkit/mrhyde2.c` | original_dirent: ifndef HIDE_DIR define HIDE_DIR ".rootkit_dir" endif ifndef HIDE_USER define... | rootkit | 35 | 0 |
| `modules/rootkit/mrhyde3.c` | io_uring_sq: #endif #ifndef HIDE_USER #define HIDE_USER "rootkit_user" #endif #define... | rootkit | 57 | 0 |
| `modules/rootkit/rootkit.asm` | - | rootkit | 1 | 0 |
| `modules/rootkit/rootkit.c` | Define the process name and file name to hide Operable values are provided via the Makefile... | rootkit | 13 | 0 |
| `modules/saas_attacks.py` | SaaS attacks — Microsoft 365, Google Workspace, Salesforce, ServiceNow exploitation. | modules | 15 | 1 |
| `modules/scripts/clean_history.sh.sh` | - | misc | 0 | 0 |
| `modules/search.py` | Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación... | modules | 0 | 1 |
| `modules/security_sanitizers.py` | Security sanitizers shared across the LazyOwn framework. | modules | 25 | 5 |
| `modules/selection/__init__.py` | Shared action-selection brain for the unified autonomous loop. | selection | 0 | 0 |
| `modules/selection/adversary.py` | Adversary selector: run a custom adversary emulation named by the objective. | selection | 3 | 3 |
| `modules/selection/atomic.py` | Atomic selector: emulate named MITRE ATT&CK techniques with atomic tests. | selection | 2 | 3 |
| `modules/selection/base.py` | The one shared contract for autonomous action selection. | selection | 4 | 11 |
| `modules/selection/chain.py` | Chain selector: propose a vetted ``apt_chain`` when one fits the state. | selection | 3 | 5 |
| `modules/selection/cred_spray.py` | Credential-spray selector: reuse known credentials against open services. | selection | 2 | 4 |
| `modules/selection/playbook.py` | Playbook selector: run an APT actor emulation named by the objective. | selection | 3 | 3 |
| `modules/selection/registry.py` | Assemble and run the shared selector cascade. | selection | 3 | 5 |
| `modules/selector_manager.py` | Selector manager: deterministic priority cascade with provenance. | modules | 3 | 1 |
| `modules/selfupdate.py` | Guarded self-update for the LazyOwn working tree. | modules | 12 | 4 |
| `modules/session_cleanup.py` | Ephemeral infrastructure cleanup on shell exit. | modules | 5 | 2 |
| `modules/session_rag.py` | — ChromaDB-backed RAG over sessions/ artefacts. | modules | 24 | 6 |
| `modules/session_reader.py` | modules/session_reader.py | modules | 29 | 3 |
| `modules/session_state.py` | LazyOwn Session State | modules | 9 | 4 |
| `modules/sidequestion.py` | Isolated side-question answering against immutable snapshots. | modules | 9 | 2 |
| `modules/sinks/__init__.py` | Outcome sink adapters. | sinks | 0 | 1 |
| `modules/sinks/attack_graph.py` | Attack-graph sink: rebuild the attack surface after meaningful outcomes. | sinks | 1 | 1 |
| `modules/sinks/beacon_dispatch.py` | Beacon dispatch sink: on a foothold, stage the catch-back command. | sinks | 3 | 1 |
| `modules/sinks/c2_surfaces.py` | C2 dashboard sink: banners, CVEs and operator notes. | sinks | 1 | 1 |
| `modules/sinks/campaign_db.py` | Campaign database sink: opt-in host and vulnerability mirror. | sinks | 1 | 0 |
| `modules/sinks/chain_feed.py` | Chain-feed sink: stream chain steps into the autonomous loop. | sinks | 1 | 2 |
| `modules/sinks/event_bus.py` | Unified event-bus sink: publish every outcome once. | sinks | 1 | 0 |
| `modules/sinks/findings.py` | Findings sink: append engagement finding transitions to the ledger. | sinks | 5 | 3 |
| `modules/sinks/intel_graph.py` | Intel-graph sink: rebuild the fused graph after meaningful outcomes. | sinks | 1 | 1 |
| `modules/sinks/killchain.py` | Kill-chain sink: advance the unified phase from proven outcomes. | sinks | 1 | 1 |
| `modules/sinks/objectives.py` | Objectives sink: turn proven outcomes into follow-up work. | sinks | 1 | 1 |
| `modules/sinks/routing.py` | Routing-prior sink: learn from terminal outcomes. | sinks | 1 | 1 |
| `modules/sinks/world_diff.py` | World-diff sink: snapshot hosts and record what changed per outcome. | sinks | 4 | 2 |
| `modules/sinks/world_model.py` | World-model sink: hosts, services, vulnerabilities and credentials. | sinks | 1 | 0 |
| `modules/sleep_obfuscation.py` | Sleep obfuscation engine for beacon memory evasion. | modules | 28 | 3 |
| `modules/smbver.sh` | Author: rewardone Description: Requires root or enough permissions to use tcpdump Will listen... | modules | 0 | 0 |
| `modules/socks_proxy.py` | SOCKS5 proxy engine for tunneling traffic through LazyOwn beacons. | modules | 31 | 3 |
| `modules/staged_delivery.py` | Staged payload delivery — HTA, Office macros, LNK files, ISO/VHD packaging. | modules | 18 | 1 |
| `modules/state_manager.py` | UnifiedStateManager — single source of truth for all LazyOwn campaign state. | modules | 44 | 8 |
| `modules/stego_video.py` | Video steganography addon for LazyOwn. | modules | 10 | 0 |
| `modules/sudo_tiocsti.py` | – Production‑grade TIOCSTI injection with multiple attack modes. | modules | 9 | 0 |
| `modules/surface_ops.py` | Pure attack-surface helpers (no cmd2): discovery targets, confirm parsing. | modules | 4 | 2 |
| `modules/test_lazyencoder_decoder.py` | - | modules | 0 | 0 |
| `modules/threat_model.py` | — Blue team threat model builder for LazyOwn. | modules | 16 | 4 |
| `modules/timeline_narrator.py` | LazyOwn Timeline Narrator | modules | 6 | 3 |
| `modules/timestomper.py` | Filesystem timestomping — MACB timestamp manipulation for stealth. | modules | 12 | 1 |
| `modules/tmp.sh` | - | modules | 0 | 0 |
| `modules/tools/__init__.py` | Reusable development tools for the LazyOwn autonomous loop. | modules_tools | 0 | 1 |
| `modules/tools/loop_smoke.py` | End-to-end smoke of the shared loop runner (no LLM, no network). | modules_tools | 10 | 0 |
| `modules/tools/monitor_smoke.py` | Headless smoke of the Textual worker monitor (``lazy_view``). | modules_tools | 3 | 0 |
| `modules/toolset.py` | Typed tool sets per agent role with shell allowlists. | modules | 5 | 1 |
| `modules/toposwarm_bridge.py` | modules/toposwarm_bridge.py | modules | 22 | 6 |
| `modules/traffic_morpher.py` | C2 traffic obfuscation: domain fronting, protocol mimicking, and traffic shaping. | modules | 11 | 1 |
| `modules/traffic_recorder.py` | HTTP traffic recorder with file-tree storage and SQLite index. | modules | 23 | 11 |
| `modules/trigger_policy.py` | Declarative trigger policy: YAML seeds for the loop TriggerStore. | modules | 8 | 8 |
| `modules/ttp_coverage.py` | TTP coverage matrix — real-time MITRE ATT&CK technique tracking. | modules | 13 | 1 |
| `modules/ttpscope_bridge.py` | Secure bridge for the TTPScope MITRE ATT&CK research client. | modules | 33 | 1 |
| `modules/unified_bridge.py` | UnifiedBridge — single API over all LazyOwn bridges and routing engines. | modules | 29 | 1 |
| `modules/unified_dashboard.py` | Unified campaign dashboard — combines all state sources into one view. | modules | 15 | 2 |
| `modules/update_db.sh` | Nombre del script: update_db.sh Autor: Gris Iscomeback Correo electrónico... | modules | 0 | 0 |
| `modules/venator.py` | - | modules | 34 | 0 |
| `modules/verb_catalog.py` | Operator-owned YAML catalog of every routable shell verb. | modules | 19 | 9 |
| `modules/verb_manifest.py` | Typed verb manifests - semantics for routable shell verbs. | modules | 17 | 3 |
| `modules/vuln_bot_cli.py` | - | modules | 2 | 0 |
| `modules/vulnbot.py` | list_files: Lista archivos en un directorio | modules | 23 | 2 |
| `modules/websocket_beacon.py` | WebSocket beacon transport for modern C2 channels. | modules | 21 | 0 |
| `modules/win_rootkit/backup.c` | - | win_rootkit | 17 | 0 |
| `modules/win_rootkit/mrhyde.c` | RunExperiment: Define the RunExperiment function | win_rootkit | 18 | 0 |
| `modules/win_rootkit/win_rin3_rootkit.cs` | - | win_rootkit | 10 | 0 |
| `modules/win_rootkit/win_ring3_rootkit.c` | initPIDArray: Función para inicializar el arreglo de PIDs | win_rootkit | 27 | 0 |
| `modules/win_rootkit/win_ring3_rootkit.cpp` | - | win_rootkit | 9 | 0 |
| `modules/winbox_gym.py` | WinBox gym catalogue and control-plane bridge. | modules | 38 | 0 |
| `modules/wineconfig.sh` | - | modules | 0 | 0 |
| `modules/workspace.py` | Confined workspace file browser for operators and loop agents. | modules | 7 | 1 |
| `modules/world_model.py` | modules/world_model.py | modules | 70 | 76 |
| `modules/yaml_generator.py` | load_payload: Carga las variables desde payload.json | modules | 8 | 0 |
| `modules/yara_scanner.py` | YARA integration for malware classification and IOC scanning. | modules | 16 | 2 |
| `mutate.sh` | - | root | 0 | 0 |
| `plugins/generate_c_reverse_shell.lua` | - | plugins | 2 | 0 |
| `plugins/generate_cleanup_commands.lua` | - | plugins | 1 | 0 |
| `plugins/generate_html_payload.lua` | - | plugins | 1 | 0 |
| `plugins/generate_lateral_command.lua` | - | plugins | 1 | 0 |
| `plugins/generate_linux_asm_reverse_shell.lua` | - | plugins | 2 | 0 |
| `plugins/generate_linux_raw_shellcode.lua` | - | plugins | 1 | 0 |
| `plugins/generate_lolbird.lua` | - | plugins | 6 | 0 |
| `plugins/generate_msfvenom_loader.lua` | - | plugins | 5 | 0 |
| `plugins/generate_msfvenom_loader_windows.lua` | - | plugins | 1 | 0 |
| `plugins/generate_reverse_shell.lua` | - | plugins | 1 | 0 |
| `plugins/generate_stub.lua` | - | plugins | 5 | 0 |
| `plugins/init_plugins.lua` | - | plugins | 1 | 0 |
| `plugins/kerberos_harvest.lua` | - | plugins | 1 | 0 |
| `plugins/lolbas_bitsadmin_exe.lua` | - | plugins | 0 | 0 |
| `plugins/lolbas_certutil_download_exec.lua` | - | plugins | 3 | 0 |
| `plugins/lolbas_certutil_exe.lua` | - | plugins | 1 | 0 |
| `plugins/lolbas_mshta_js.lua` | - | plugins | 0 | 0 |
| `plugins/lolbas_mshta_reverse_shell.lua` | - | plugins | 0 | 0 |
| `plugins/lolbas_rundll32_dll.lua` | - | plugins | 0 | 0 |
| `plugins/lolbas_wmic_xsl_execution.lua` | - | plugins | 1 | 0 |
| `plugins/parse_nmap_with_xmlstarlet.lua` | - | plugins | 1 | 0 |
| `plugins/run_nuclei_on_nmap_files.lua` | - | plugins | 1 | 0 |
| `plugins/run_python_rev_c2.lua` | - | plugins | 1 | 0 |
| `plugins/rundll32_sct_from_url.lua` | - | plugins | 4 | 0 |
| `plugins/validate_shellcode.lua` | - | plugins | 4 | 0 |
| `plugins/visualize_network.lua` | - | plugins | 1 | 0 |
| `poc_tui/__main__.py` | Entry point: python3 -m poc_tui | poc_tui | 0 | 0 |
| `poc_tui/app.py` | LazyOwn TUI Shell — Proof of Concept.  cmd2 as backend, Textual as frontend. | poc_tui | 47 | 3 |
| `poc_tui/config.py` | Payload.json configuration manager for the TUI shell. | poc_tui | 11 | 1 |
| `poc_tui/plugin_loader.py` | Unified plugin loader — YAML addons, Lua plugins, and .tool files. | poc_tui | 22 | 0 |
| `poc_tui/run.py` | Convenience launcher that symlinks LazyOwn dirs and starts the TUI. | poc_tui | 1 | 0 |
| `poc_tui/test_app.py` | Pytest tests for LazyOwn TUI Shell POC. | poc_tui | 56 | 0 |
| `pwntomate.py` | This software must not be used by military or secret service organisations. | root | 3 | 0 |
| `py2elf.sh` | Nombre del script: py2elf.sh Autor: Gris Iscomeback Correo electrónico... | root | 0 | 0 |
| `readmeneitor.py` | — Automated documentation generator for LazyOwn RedTeam Framework. | root | 11 | 0 |
| `run_telegram_hermes.sh` | Launcher for telegram_hermes.py Uses the dedicated venv with python-telegram-bot dependencies | root | 0 | 0 |
| `run_topoexploit_agent.sh` | Run TopoExploit against an ExploitGym task using the local model. | root | 2 | 0 |
| `scripts/__init__.py` | Repository-side maintenance scripts. | scripts | 0 | 0 |
| `scripts/activate_migrations.py` | Activate dormant CommandSet migrations. | scripts | 7 | 0 |
| `scripts/backfill_addon_os_trigger.py` | One-shot backfill: add ``os`` and ``trigger`` keys to every lazyaddon. | scripts | 5 | 0 |
| `scripts/broadcom_wps_drive.sh` | operator-side driver for the Broadcom 802.11 SDK detection toolkit. | scripts | 25 | 0 |
| `scripts/check_contract_manifest.py` | Verify that documented contracts still exist on disk. | scripts | 13 | 1 |
| `scripts/devtools/command_audit.py` | Audit every registered shell command for dispatch and parser errors. | devtools | 4 | 0 |
| `scripts/devtools/core_smoke.py` | Smoke check for the public surfaces documented in CORE.md. | devtools | 4 | 0 |
| `scripts/dirtyinit_drive.sh` | operator-side driver for the DirtyInit Android root chain. | scripts | 28 | 0 |
| `scripts/fix_migrated_classes.py` | - | scripts | 0 | 0 |
| `scripts/generate_sbom.py` | Generate a minimal CycloneDX SBOM from the pinned requirements files. | scripts | 5 | 0 |
| `scripts/journal.py` | Read-before-you-write journal over GitHub Discussions. | scripts | 14 | 2 |
| `scripts/lazy_hermes_ask.sh` | — detached Hermes task runner for LazyOwn. | scripts | 0 | 0 |
| `scripts/lazy_llamacpp_serve.sh` | — idempotent llama.cpp server manager for LazyOwn. | scripts | 1 | 0 |
| `scripts/lazy_llamacpp_setup.sh` | — one-time local LLM setup for LazyOwn users. | scripts | 1 | 0 |
| `scripts/lazy_msf_lab.sh` | — Metasploitable2 smoke lab manager for LazyOwn. | scripts | 0 | 0 |
| `scripts/lazy_opencode_config.py` | Patch operator agent configs to use the Lazy llama.cpp server. | scripts | 6 | 1 |
| `scripts/mcp_call.py` | Call one LazyOwn MCP tool over stdio and print its text content. | scripts | 9 | 0 |
| `scripts/migrate_commandsets.py` | Merge _migrated.py CommandSet methods into clean phase modules. | scripts | 6 | 0 |
| `scripts/migrate_lazyown.py` | Staged migration script: extract do_* methods from lazyown.py into cli/commands/. | scripts | 6 | 1 |
| `scripts/mutate.sh` | Mutation gate for LazyOwn. | scripts | 3 | 0 |
| `scripts/mutation_gate.py` | Consolidated mutation gate for LazyOwn. | scripts | 3 | 0 |
| `scripts/patch_playbook_atomic_ids.py` | Patch APT playbooks: replace placeholder atomic_ids with real technique_ids. | scripts | 0 | 0 |
| `scripts/pi_qwen_setup.sh` | idempotent bootstrap for the pi_qwen lazyaddon. | scripts | 0 | 0 |
| `scripts/publish_wiki.sh` | Publish LazyOwn documentation to the GitHub wiki. | scripts | 8 | 0 |
| `scripts/read_journal.py` | Print the recent engineering journal before a change is written. | scripts | 2 | 0 |
| `scripts/setup_hermes_mcp.sh` | — register LazyOwn MCP server in Hermes Agent config Usage: bash scripts/setup_hermes_mcp.sh... | scripts | 0 | 0 |
| `scripts/smoke_onboarding.sh` | Smoke test for the 5-minute onboarding path. | scripts | 1 | 0 |
| `scripts/sync_doc_stats.py` | Sync documentation numbers with the live codebase — single source of truth. | scripts | 6 | 0 |
| `scripts/test_bdd.sh` | Behavior-driven (BDD) suite gate for LazyOwn. | scripts | 2 | 0 |
| `scripts/top_tier_check.py` | Top-tier hygiene audit for LazyOwn. | scripts | 10 | 0 |
| `scripts/update_apt_atomic_ids.py` | Update APT playbooks with real Atomic Red Team test IDs. | scripts | 2 | 0 |
| `scripts/validate_agent_contract.sh` | CI validation of the AGENTS.md branching model and coding standards. | scripts | 5 | 0 |
| `setup.py` | Compatibility shim for legacy ``python setup.py`` invocations. | root | 0 | 0 |
| `skills/aci_planner.py` | Autonomous Campaign Intelligence (ACI) Planner | skills | 42 | 2 |
| `skills/autonomous_daemon.py` | skills/autonomous_daemon.py — LazyOwn Autonomous Execution Daemon | skills | 157 | 16 |
| `skills/autonomous_replay.py` | Deterministic replay of past autonomous-daemon runs. | skills | 19 | 2 |
| `skills/claude_md_orchestrator/__init__.py` | Public API for the claude_md_orchestrator skill. | claude_md_orchestrator | 0 | 1 |
| `skills/claude_md_orchestrator/bdd_agent.py` | Behavior-Driven Development agent. | claude_md_orchestrator | 8 | 0 |
| `skills/claude_md_orchestrator/boy_scout.py` | Boy Scout refactor pass. | claude_md_orchestrator | 5 | 0 |
| `skills/claude_md_orchestrator/cicd_agent.py` | CI and CD agent. | claude_md_orchestrator | 7 | 0 |
| `skills/claude_md_orchestrator/config.py` | Centralized configuration for the claude_md_orchestrator skill. | claude_md_orchestrator | 15 | 10 |
| `skills/claude_md_orchestrator/documentation_agent.py` | Documentation agent. | claude_md_orchestrator | 7 | 0 |
| `skills/claude_md_orchestrator/models.py` | Data models for the claude_md_orchestrator skill. | claude_md_orchestrator | 32 | 11 |
| `skills/claude_md_orchestrator/orchestrator.py` | Orchestrator that wires the agents into a deterministic pipeline. | claude_md_orchestrator | 21 | 1 |
| `skills/claude_md_orchestrator/parser.py` | Parser that turns a CLAUDE.md into actionable contracts. | claude_md_orchestrator | 13 | 4 |
| `skills/claude_md_orchestrator/reviewer_agent.py` | Code Reviewer and Quality Assurance agent. | claude_md_orchestrator | 10 | 0 |
| `skills/claude_md_orchestrator/sdd_agent.py` | Spec-Driven Development agent. | claude_md_orchestrator | 6 | 0 |
| `skills/claude_md_orchestrator/tdd_agent.py` | Test-Driven Development agent. | claude_md_orchestrator | 7 | 1 |
| `skills/claude_md_orchestrator/tests/conftest.py` | Pytest bootstrap for the claude_md_orchestrator test suite. | skills_claude_md_orchestrator_tests | 0 | 0 |
| `skills/claude_md_orchestrator/tests/test_orchestrator.py` | Unit tests for the claude_md_orchestrator package. | skills_claude_md_orchestrator_tests | 20 | 0 |
| `skills/claude_md_orchestrator/validators.py` | DoD validators for every artifact the orchestrator produces. | claude_md_orchestrator | 21 | 6 |
| `skills/daemon_control.py` | Operator steering layer for the LazyOwn autonomous daemon. | skills | 27 | 4 |
| `skills/daemon_health.py` | Daemon health monitor — watchdog for the autonomous daemon and C2 listeners. | skills | 16 | 1 |
| `skills/heartbeat.py` | LazyOwn Heartbeat | skills | 5 | 0 |
| `skills/hermes-lazyown/__init__.py` | Hermes-LazyOwn integration package. | hermes-lazyown | 0 | 0 |
| `skills/hermes-lazyown/claudemd_rules.py` | Dynamic Claude.md rule generator for the Hermes-LazyOwn integration. | hermes-lazyown | 14 | 1 |
| `skills/hermes-lazyown/config_bridge.py` | Configuration bridge: unifies LazyOwn payload.json, environment variables, and fallback defaults... | hermes-lazyown | 16 | 1 |
| `skills/hermes-lazyown/constants.py` | Central constants for the Hermes-LazyOwn integration layer. | hermes-lazyown | 15 | 6 |
| `skills/hermes-lazyown/executor.py` | LazyOwn command executor for the Hermes-LazyOwn integration. | hermes-lazyown | 13 | 1 |
| `skills/hermes-lazyown/hermes_sync.py` | Hermes-native synchronization layer. | hermes-lazyown | 14 | 1 |
| `skills/hermes-lazyown/mcp_server.py` | Hermes-native MCP server for LazyOwn. | hermes-lazyown | 28 | 0 |
| `skills/hermes-lazyown/output_compactor.py` | Phase-aware output compaction for the Hermes-LazyOwn integration. | hermes-lazyown | 20 | 1 |
| `skills/hive_mind.py` | skills/hive_mind.py — LazyOwn Borg Hive Mind | skills | 107 | 6 |
| `skills/lazyown_automapper.py` | LazyOwn MCP Auto-Mapper | skills | 23 | 1 |
| `skills/lazyown_campaign.py` | LazyOwn CampaignStore | skills | 26 | 1 |
| `skills/lazyown_claudemd.py` | LazyOwn CLAUDE.md Hierarchical Loader (Claude Code style)  4-level hierarchy (highest → lowest... | skills | 8 | 2 |
| `skills/lazyown_context.py` | LazyOwn Context Compaction Pipeline — 5-layer graduated compression (Claude Code style)  Layers: 1. | skills | 11 | 3 |
| `skills/lazyown_daemon.py` | LazyOwn Unified Daemon | skills | 24 | 0 |
| `skills/lazyown_facts.py` | LazyOwn FactStore | skills | 79 | 10 |
| `skills/lazyown_groq_agents.py` | skills/lazyown_groq_agents.py | skills | 40 | 4 |
| `skills/lazyown_hooks.py` | LazyOwn Hook Pipeline (Claude Code style)  8 lifecycle events with chainable handlers. | skills | 14 | 2 |
| `skills/lazyown_llm.py` | LazyOwn LLM Bridge — MCP Edition | skills | 21 | 4 |
| `skills/lazyown_mcp.py` | LazyOwn MCP Server Exposes LazyOwn framework capabilities as MCP tools for Claude Code and... | skills | 131 | 9 |
| `skills/lazyown_mcp_helpers.py` | LazyOwn MCP helper functions — pure logic, no MCP server imports. | skills | 21 | 4 |
| `skills/lazyown_mcp_opencode.py` | LazyOwn MCP OpenCode bridge. | skills | 6 | 1 |
| `skills/lazyown_objective.py` | LazyOwn Objective Store | skills | 36 | 9 |
| `skills/lazyown_parquet_db.py` | LazyOwn Parquet Knowledge Base | skills | 21 | 8 |
| `skills/lazyown_permissions.py` | LazyOwn Permission System — Deny-First Rule Evaluation (Claude Code style)  Deny rules ALWAYS... | skills | 16 | 2 |
| `skills/lazyown_policy.py` | LazyOwn Policy Engine | skills | 126 | 10 |
| `skills/lazyown_session.py` | LazyOwn Append-Only Session Transcripts (Claude Code style)  All writes are append-only JSONL. | skills | 14 | 2 |
| `skills/mcp_generated_tools.py` | Auto-generated MCP tool handlers from command_index.json. | skills | 645 | 0 |
| `skills/mcp_lazy.py` | Single helper behind every lazy optional import of the MCP server. | skills | 1 | 2 |
| `skills/mcp_restart.sh` | LazyOwn MCP restart helper  Kills ALL lazyown_mcp instances (stdio + SSE) and relaunches the SSE... | skills | 0 | 0 |
| `skills/mcp_tool_generator.py` | Auto-generate MCP tool handlers from cli/command_index.json. | skills | 9 | 0 |
| `skills/sessions_watcher.py` | LazyOwn Sessions Watcher | skills | 18 | 1 |
| `skills/setup.sh` | paths_for_sudo: Collect paths that exist on this system | skills | 5 | 0 |
| `skills/swan_agent.py` | skills/swan_agent.py — LazyOwn SWAN Agent | skills | 44 | 5 |
| `skills/tests/__init__.py` | - | skills_tests | 0 | 0 |
| `skills/tests/test_autonomous_daemon.py` | skills/tests/test_autonomous_daemon.py — Tests for autonomous_daemon.py (SOLID refactoring)  All... | skills_tests | 88 | 0 |
| `skills/tests/test_facts.py` | Tests for lazyown_facts.py — parsers and FactStore. | skills_tests | 37 | 0 |
| `skills/tests/test_harness_e2e.py` | End-to-end test for the Claude Code-style harness layer. | skills_tests | 10 | 0 |
| `skills/tests/test_hive_mind.py` | skills/tests/test_hive_mind.py — Tests for hive_mind.py (SOLID refactoring)  All file I/O uses... | skills_tests | 95 | 0 |
| `skills/tests/test_mcp_smoke.py` | Smoke test for the MCP server: verify all 131 tools are registered. | skills_tests | 5 | 0 |
| `skills/tests/test_objectives.py` | Tests for lazyown_objective.py — ObjectiveStore and SoulUpdater. | skills_tests | 28 | 0 |
| `skills/tests/test_parquet_db.py` | Tests for lazyown_parquet_db.py — ParquetDB. | skills_tests | 33 | 0 |
| `skills/toposwarm_autonomous.py` | skills/toposwarm_autonomous.py | skills | 15 | 0 |
| `skills/unified_orchestrator.py` | Unified orchestrator facade collapsing daemon, hive and SWAN into one surface. | skills | 59 | 2 |
| `skills/update_knowledge.py` | LazyOwn Knowledge Refresh | skills | 1 | 0 |
| `slack_c2_bot.py` | - | root | 16 | 0 |
| `source/conf.py` | Configuration file for the Sphinx documentation builder. | misc | 0 | 0 |
| `static/js/3d-force-graph-1.73.4.min.js` | Version 1.73.4 3d-force-graph - https://github.com/vasturiano/3d-force-graph... | js | 176 | 0 |
| `static/js/bootstrap-4.5.2.min.js` | r: ! | js | 7 | 0 |
| `static/js/bootstrap-5.3.0.bundle.min.js` | W: ! | js | 28 | 0 |
| `static/js/chart.min.js` | xt: ! | js | 88 | 0 |
| `static/js/force-graph-1.43.5.min.js` | Version 1.43.5 force-graph - https://github.com/vasturiano/force-graph... | js | 31 | 0 |
| `static/js/html2pdf.bundle.min.js` | o: 3. | js | 738 | 0 |
| `static/js/jquery-3.5.1.slim.min.js` | ! jQuery v3.5.1 -ajax,-ajax/jsonp,-ajax/load,-ajax/script,-ajax/var/location,-ajax/var/nonce,-aja... | js | 6 | 0 |
| `static/js/particles.js` | - | js | 11 | 0 |
| `static/js/popper-2.5.4.min.js` | - | js | 1 | 0 |
| `static/js/purify-3.0.9.min.js` | ! @license DOMPurify 3.0.9 \| (c) Cure53 and other contributors \| Released under the Apache... | js | 2 | 0 |
| `static/js/quill-2.0.3.js` | ! | js | 124 | 0 |
| `static/js/select2-4.1.0.min.js` | ! | js | 3 | 0 |
| `static/js/showdown-2.1.0.min.js` | ! showdown v 2.1.0 - 21-04-2022 | js | 5 | 0 |
| `static/js/socket.io-4.0.0.min.js` | as: ! | js | 32 | 0 |
| `static/js/socket.io-4.3.2.min.js` | as: ! | js | 15 | 0 |
| `static/js/tippy-6.js` | - | js | 3 | 0 |
| `static/js/vis-network-9.1.2.min.js` | as: @license vis.js is dual licensed under both  1. | js | 135 | 0 |
| `static/js/vis-network.min.js` | as: @license vis.js is dual licensed under both  1. | js | 135 | 0 |
| `static/js/xterm-addon-fit-0.7.0.js` | - | js | 0 | 0 |
| `static/js/xterm-addon-web-links-0.5.0.js` | - | js | 4 | 0 |
| `static/js/xterm.js` | - | js | 62 | 0 |
| `telegram_c2.py` | download_c2: Handle the /download_c2 command to download a file from the C2. | root | 19 | 0 |
| `telegram_hermes.py` | LazyOwn Telegram Bot with Hermes Gateway Integration  This bot bridges Telegram to the full... | root | 31 | 0 |
| `test_bdd.sh` | - | root | 0 | 0 |
| `testmeneitor.py` | - | root | 5 | 0 |
| `tests/__init__.py` | - | tests | 0 | 0 |
| `tests/conftest.py` | Global pytest isolation hooks. | tests | 11 | 0 |
| `tests/contract/__init__.py` | - | contract | 0 | 0 |
| `tests/contract/test_suite_homologation.py` | SDD suite homologation contract for LazyOwn tests. | contract | 20 | 0 |
| `tests/integration_autonomous_flow.py` | test_autonomous_flow_integration: Simulates a simplified autonomous flow to verify module... | tests | 1 | 0 |
| `tests/mutation_common.py` | Shared driver for curated mutation runners. | tests | 5 | 3 |
| `tests/run_mutation_addon_creator.py` | Manual mutation testing runner for the LazyAddon creator contract. | tests | 4 | 0 |
| `tests/run_mutation_addon_updater.py` | Mutation runner for the lazyaddon update contract. | tests | 4 | 0 |
| `tests/run_mutation_api_authz.py` | Mutation testing runner for core.api_authz and core.logging. | tests | 3 | 0 |
| `tests/run_mutation_autonomous_ops.py` | Manual mutation runner for the LAZY port contracts. | tests | 4 | 0 |
| `tests/run_mutation_beacon_dispatch.py` | Mutation runner for the beacon dispatch sink contract. | tests | 5 | 0 |
| `tests/run_mutation_c2_route_auth.py` | Mutation gate for C2 route-level auth boundaries. | tests | 2 | 0 |
| `tests/run_mutation_chain_v2.py` | Mutation runner for the chain v2 contract. | tests | 4 | 0 |
| `tests/run_mutation_contract_manifest.py` | Mutation gate for the contract manifest drift checker. | tests | 2 | 0 |
| `tests/run_mutation_emulation_runner.py` | Mutation runner for the emulation-runner contract. | tests | 4 | 0 |
| `tests/run_mutation_infra_report.py` | Mutation runner for the disposable infra and reporting contracts. | tests | 4 | 0 |
| `tests/run_mutation_intel_svg.py` | Mutation runner for the intel relations-svg contract. | tests | 4 | 0 |
| `tests/run_mutation_killchain.py` | Manual mutation testing runner for the unified kill-chain contract. | tests | 4 | 0 |
| `tests/run_mutation_lazy_scope.py` | Mutation runner for the lab-only default scope contract. | tests | 4 | 0 |
| `tests/run_mutation_llm.py` | Mutation runner for the LLM subsystem contract. | tests | 4 | 0 |
| `tests/run_mutation_llm_orchestrator.py` | Mutation runner for the orchestrator-governed LLM failover contract. | tests | 4 | 0 |
| `tests/run_mutation_loop_cli_catalog.py` | Mutation runner for the planner catalog visibility contract. | tests | 1 | 0 |
| `tests/run_mutation_no_shell.py` | Mutation gate for the no-shell execution contract. | tests | 2 | 0 |
| `tests/run_mutation_opsec.py` | Mutation runner for the consolidated OPSEC scorer contract. | tests | 4 | 0 |
| `tests/run_mutation_orchestrator_yaml.py` | Mutation runner for the orchestrator YAML contract. | tests | 4 | 0 |
| `tests/run_mutation_outcome_bus.py` | Mutation runner for the outcome-bus contract. | tests | 4 | 0 |
| `tests/run_mutation_phase1.py` | Mutation testing runner for Phase 1 data-gap closure. | tests | 4 | 0 |
| `tests/run_mutation_shell_semantics.py` | Mutation gate for shell semantics and colored output. | tests | 2 | 0 |
| `tests/run_mutation_tests.py` | Manual mutation testing runner for LazyOwn connectivity improvements. | tests | 4 | 0 |
| `tests/run_mutation_trigger_hints.py` | Mutation runner for the cve_hot hint fingerprint contract. | tests | 4 | 0 |
| `tests/run_mutation_trigger_policy.py` | Mutation runner for the trigger policy contract. | tests | 1 | 0 |
| `tests/run_mutation_ux_usability.py` | Mutation testing runner for the UX usability contracts. | tests | 4 | 0 |
| `tests/run_mutation_verb_catalog.py` | Mutation runner for the verb catalog contract. | tests | 1 | 0 |
| `tests/run_mutation_world_diff.py` | Mutation runner for the lazy world-diff contract. | tests | 4 | 0 |
| `tests/test_aci_planner.py` | tests/test_aci_planner.py | tests | 95 | 0 |
| `tests/test_ad_lab_gym.py` | Contract tests for the AD lab gym (Docker Samba DC) matrix and capture. | tests | 25 | 0 |
| `tests/test_addon_creator.py` | Tests for the LazyAddon creator contract and C2 blueprint. | tests | 86 | 0 |
| `tests/test_addon_updater.py` | Lazyaddon update BDD contract: opt-in, path-safe, dirty-tree aware. | tests | 13 | 0 |
| `tests/test_aes_key_propagation.py` | TDD tests for the AES key resolution contract. | tests | 12 | 0 |
| `tests/test_ai_commands_llm.py` | Behavioural tests for the resurrected ``ask``/``groq`` commands. | tests | 18 | 0 |
| `tests/test_api_authz.py` | Tests for ``core.api_authz`` — tenant-bound API authorization. | tests | 48 | 0 |
| `tests/test_api_key_resolution.py` | API-key resolution contract tests. | tests | 9 | 0 |
| `tests/test_api_v1.py` | Integration tests for the versioned C2 REST API (``/api/v1``). | tests | 13 | 0 |
| `tests/test_apt_chain_admin.py` | apt_chain admin & run options BDD contract. | tests | 22 | 0 |
| `tests/test_apt_chain_integration.py` | BDD integration: apt_chain runs real cmd2 verbs, raw commands and shell. | tests | 6 | 0 |
| `tests/test_asset_gate.py` | Asset gate + un-nerfed outputs + IntelGraph CSP regression tests. | tests | 16 | 0 |
| `tests/test_atomic_exploit_bridge.py` | Atomic exploit catalogue: one YAML per exploit, engine administered by files. | tests | 38 | 0 |
| `tests/test_atomic_loop.py` | Atomic emulation inside the autonomous loop (registry + playbooks). | tests | 17 | 0 |
| `tests/test_atomic_resolver.py` | MITRE ATT&CK <-> Atomic Red Team translator contract. | tests | 9 | 0 |
| `tests/test_attack_surface3d.py` | Attack-surface 3D module: surface+intel fusion + embedded pages. | tests | 8 | 0 |
| `tests/test_attack_surface_addons.py` | tests/test_attack_surface_addons.py  BDD: Validate cloud, supply-chain, and web attack-surface... | tests | 76 | 0 |
| `tests/test_audit_remediation.py` | Audit-remediation contract tests (P0-P4). | tests | 28 | 0 |
| `tests/test_auto_crypto.py` | Tests for cli.auto_crypto — automatic session data encryption. | tests | 22 | 0 |
| `tests/test_auto_loop_memory.py` | BDD tests for the auto-loop persistent memory and selector cascade. | tests | 19 | 0 |
| `tests/test_auto_registry.py` | Auto-verb registry: loop-ready automation commands. | tests | 20 | 0 |
| `tests/test_autonomous_ops.py` | BDD scoped tests for integrated autonomous operations C04-C10. | tests | 17 | 0 |
| `tests/test_autonomous_replay.py` | Tests for ``skills/autonomous_replay.py``. | tests | 18 | 0 |
| `tests/test_autosuggest.py` | Unit tests for cli.autosuggest. | tests | 41 | 0 |
| `tests/test_awesome_windows_security_skill.py` | tests/test_awesome_windows_security_skill.py  Contract suite for the... | tests | 51 | 0 |
| `tests/test_backdoor_random.py` | Backdoor credentials: random like C2 operators, persisted via assign. | tests | 5 | 0 |
| `tests/test_banner_config.py` | Tests for cli/banner_config.py — registry, settings, renderer, wizard. | tests | 45 | 0 |
| `tests/test_bdd_infra_range_report.py` | BDD scenarios for disposable infra, range, and executive reporting. | tests | 5 | 0 |
| `tests/test_beacon_config_builder.py` | Tests for modules/beacon_config_builder.py — BeaconConfig, BeaconConfigBuilder, and... | tests | 16 | 0 |
| `tests/test_beacon_history.py` | BDD-style tests for persistent beacon command/result history storage. | tests | 10 | 0 |
| `tests/test_beacon_recon_sink.py` | Beacon recon ingest tests. | tests | 18 | 0 |
| `tests/test_blacksandbeacon_addon.py` | tests/test_blacksandbeacon_addon.py  Validation suite for the blacksandbeacon and... | tests | 60 | 0 |
| `tests/test_bof_registry.py` | Tests for modules/bof_registry.py — BofEntry, BofCatalog, BofRegistry, BofMarketplace... | tests | 51 | 0 |
| `tests/test_bootstrap_installer.py` | Integration tests for the installer scripts (no network, no apt). | tests | 14 | 0 |
| `tests/test_boyscout_contracts.py` | Boy-scout contracts for critical shared surfaces. | tests | 15 | 0 |
| `tests/test_bridge_catalog_filtered.py` | tests/test_bridge_catalog_filtered.py  Tests for ``BridgeDispatcher.catalog_summary_filtered``... | tests | 20 | 0 |
| `tests/test_broadcom_wps_addon.py` | tests/test_broadcom_wps_addon.py  Validation suite for the broadcom_wps lazyaddon and its... | tests | 50 | 0 |
| `tests/test_c2_agent.py` | Malleable C2 agent: template safety, key ownership, record reading. | tests | 20 | 0 |
| `tests/test_c2_agent_dual.py` | Dual C2 client profiles (lowpriv/root) contract tests. | tests | 31 | 0 |
| `tests/test_c2_credential_bootstrap.py` | C2 boot credential contract: file, console and RBAC registration. | tests | 21 | 0 |
| `tests/test_c2_profile_engine.py` | Tests for modules/c2_profile_engine.py — TlsProfile, DnsProfile, SmbProfile, WebSocketProfile... | tests | 63 | 0 |
| `tests/test_c2_route_auth.py` | Guard the C2 route-level auth boundaries. | tests | 5 | 0 |
| `tests/test_c2_shell_lazy.py` | The C2 must not build the CLI shell at module load. | tests | 14 | 0 |
| `tests/test_c2_surfaces.py` | C2 dashboard surfaces fed by the autonomous loop and APT chains. | tests | 12 | 0 |
| `tests/test_campaign_import_safety.py` | Campaign import trust boundaries hold against hostile packages. | tests | 14 | 0 |
| `tests/test_categories.py` | Tests for modules/categories.py — category constants and look-up tables. | tests | 47 | 0 |
| `tests/test_chain_approval_c2.py` | Contract tests for the chain approval gate (C2 human-in-the-loop). | tests | 27 | 0 |
| `tests/test_chain_distill.py` | BDD tests for chain_distill trace crystallisation. | tests | 15 | 0 |
| `tests/test_chain_distill_custody.py` | Chain distillation custody contract: replayed steps pin their evidence. | tests | 7 | 0 |
| `tests/test_chain_distill_scope.py` | Chain distillation scope contract: config-driven target exclusion. | tests | 5 | 0 |
| `tests/test_chain_evidence.py` | Chain-of-evidence: depends_on gating, budgets, verdicts and artefact pins. | tests | 27 | 0 |
| `tests/test_chain_freshness_guard.py` | Freshness guards for chain skips: stale artefacts do not skip work. | tests | 9 | 0 |
| `tests/test_chain_list_command.py` | BDD: chain list exposes the YAML chain registry. | tests | 2 | 0 |
| `tests/test_chain_mode.py` | Tests for cli/chain_mode.py. | tests | 28 | 0 |
| `tests/test_chain_parallel_fallback.py` | Chain v2 adaptive execution: parallel groups, fallback, pre-checks. | tests | 26 | 0 |
| `tests/test_chain_registry.py` | Chain registry: orchestration from chains/*.yaml, never hardcoded steps. | tests | 9 | 0 |
| `tests/test_chain_runner.py` | Chain v2 BDD contract: safe conditions, retries, capture and error policy. | tests | 39 | 0 |
| `tests/test_chain_selector.py` | Tests for ``ChainSelector`` in ``skills/autonomous_daemon.py``. | tests | 12 | 0 |
| `tests/test_chain_step_streaming.py` | Chain step streaming contract: chain_step events reach the bus per step. | tests | 23 | 0 |
| `tests/test_chain_synth.py` | BDD tests for runtime chain synthesis. | tests | 10 | 0 |
| `tests/test_chain_token_hardening.py` | Shell-metacharacter containment contract for chain tokens. | tests | 14 | 0 |
| `tests/test_chain_v24_core.py` | Chain v2.4 BDD contract: branching, verify, captures, gates, checkpoints. | tests | 33 | 0 |
| `tests/test_ci_strict.py` | Contract tests for the strict CI workflow. | tests | 10 | 0 |
| `tests/test_claudemd_consistency.py` | Guard against drift between CLAUDE.md numeric claims and reality. | tests | 3 | 0 |
| `tests/test_claudemd_size.py` | Enforce a hard cap on ``CLAUDE.md`` size. | tests | 1 | 0 |
| `tests/test_cli_assign.py` | ``do_assign`` / ``do_show`` behaviour and shell wiring tests. | tests | 44 | 0 |
| `tests/test_cli_auth_remember.py` | Remember-me token comparison must be timing-safe. | tests | 7 | 0 |

Next: [INDEX_p3.md](INDEX_p3.md)
