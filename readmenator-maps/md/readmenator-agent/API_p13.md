# API (page 13 of 25)
Previous: [API_p12.md](API_p12.md)

## modules/intercept.py
Depends on: `cli/commands/enum.py`
Imported by: `cli/commands/daemon_ctl.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/test_engage_gates.py`, `tests/test_lazy_parity.py`, `tests/test_safety_gates.py`
- `InterceptRule.matches` (method) `modules/intercept.py:68` `def matches(self, tool, command)` -- Return True when this rule matches the tool call surface.
- `builtin_rules` (function) `modules/intercept.py:101` `def builtin_rules()` -- Return the default destructive and exfiltration guard rules.
- `scope_blocked` (function) `modules/intercept.py:131` `def scope_blocked(target)` -- Return the matching global scope suffix or empty (LAZY parity).
- `observe_post_tool` (function) `modules/intercept.py:144` `def observe_post_tool(output)` -- Classify post-execution output (LAZY Guard.postToolUse parity).
- `Interceptor.__init__` (method) `modules/intercept.py:157` `def __init__(self, rules, ask_timeout_sec, timeout_action)` -- Initialize with rules sorted by descending priority.
- `Interceptor.rules` (method) `modules/intercept.py:172` `def rules(self)` -- Return a copy of the active rule list.
- `Interceptor.add_rule` (method) `modules/intercept.py:177` `def add_rule(self, rule)` -- Add a rule and keep priority ordering.
- `Interceptor.remove_rule` (method) `modules/intercept.py:183` `def remove_rule(self, pattern)` -- Remove the first rule matching pattern text.
- `Interceptor.evaluate` (method) `modules/intercept.py:192` `def evaluate(self, tool, command)` -- Evaluate a tool call and return the verdict.
- `Interceptor.decide` (method) `modules/intercept.py:220` `def decide(self, approval_id, decision)` -- Resolve a pending approval with approve or deny.
- `Interceptor.pending_approvals` (method) `modules/intercept.py:234` `def pending_approvals(self)` -- List unresolved approvals, expiring timed-out ones per policy.
- `Interceptor.approval_status` (method) `modules/intercept.py:249` `def approval_status(self, approval_id)` -- Fetch a single approval record by id.
- `Guard.__init__` (method) `modules/intercept.py:258` `def __init__(self, interceptor)` -- Initialize audit log with an optional interceptor.
- `Guard.interceptor` (method) `modules/intercept.py:266` `def interceptor(self)` -- Expose the underlying interceptor.
- `Guard.check` (method) `modules/intercept.py:270` `def check(self, tool, command)` -- Audit the call then evaluate intercept rules (trace id kept).
- `Guard.observe` (method) `modules/intercept.py:282` `def observe(self, output, source)` -- Classify output and attribute blocked/error counters.
- `Guard.record_failure` (method) `modules/intercept.py:291` `def record_failure(self, source)` -- Attribute a post-execution failure to a source.
- `Guard.audit_log` (method) `modules/intercept.py:296` `def audit_log(self, limit)` -- Return the most recent audit entries.
- `Guard.attribution` (method) `modules/intercept.py:301` `def attribution(self)` -- Return failure attribution counters.

## modules/iptables_portforward.sh
- `display_usage` (function) `modules/iptables_portforward.sh:29`

## modules/jsonl_tail.py
Imported by: `cli/lazy_monitor.py`, `cli/lazy_orchestrator.py`, `modules/lazy_runner.py`
- `JsonlTail.__init__` (method) `modules/jsonl_tail.py:17` `def __init__(self, path)` -- Bind the tail to one file path.
- `JsonlTail.read_new` (method) `modules/jsonl_tail.py:22` `def read_new(self, limit)` -- Return new complete records since the last call.

## modules/k8s_attacks.py
Imported by: `cli/commands/cloud_attacks.py`
- `K8SAttackEngine.__init__` (method) `modules/k8s_attacks.py:87` `def __init__(self, config)`
- `K8SAttackEngine.enumerate_rbac` (method) `modules/k8s_attacks.py:90` `def enumerate_rbac(self)` -- Enumerate RBAC permissions for the current identity.
- `K8SAttackEngine.privileged_pod_escape` (method) `modules/k8s_attacks.py:118` `def privileged_pod_escape(self)` -- Plan a privileged pod escape.
- `K8SAttackEngine.service_account_token_theft` (method) `modules/k8s_attacks.py:173` `def service_account_token_theft(self)` -- Steal service account tokens across namespaces for lateral movement.
- `K8SAttackEngine.kubelet_anonymous_auth_abuse` (method) `modules/k8s_attacks.py:198` `def kubelet_anonymous_auth_abuse(self)` -- Exploit kubelet anonymous authentication.
- `K8SAttackEngine.etcd_access_exploitation` (method) `modules/k8s_attacks.py:222` `def etcd_access_exploitation(self)` -- Exploit etcd database access for complete cluster compromise.
- `K8SAttackEngine.helm_tiller_abuse` (method) `modules/k8s_attacks.py:250` `def helm_tiller_abuse(self)` -- Abuse Helm (v2 Tiller or v3 RBAC) for privilege escalation.
- `K8SAttackEngine.persistence_techniques` (method) `modules/k8s_attacks.py:278` `def persistence_techniques(self)` -- Kubernetes persistence techniques for long-term access.
- `K8SAttackEngine.summary` (method) `modules/k8s_attacks.py:318` `def summary(self)`

## modules/kerberoasting.py
Depends on: `modules/kerberos_core.py`
Imported by: `cli/commands/active_directory.py`
- `KerberoastingEngine.__init__` (method) `modules/kerberoasting.py:95` `def __init__(self, domain, dc_ip, username, password, hash)`
- `KerberoastingEngine.enumerate_spns` (method) `modules/kerberoasting.py:112` `def enumerate_spns(self, ldap_output, bloodhound_data)` -- Enumerate kerberoastable service principals.
- `priority` (function) `modules/kerberoasting.py:172` `def priority(target)`
- `KerberoastingEngine.request_tgs_aes_only` (method) `modules/kerberoasting.py:187` `def request_tgs_aes_only(self, user_spn)` -- Request a TGS ticket using only AES encryption (evades RC4 detection).
- `KerberoastingEngine.request_tgs_rc4` (method) `modules/kerberoasting.py:208` `def request_tgs_rc4(self, user_spn)` -- Request a TGS ticket using RC4-HMAC (mode 13100 for Hashcat).
- `KerberoastingEngine.request_tgs` (method) `modules/kerberoasting.py:219` `def request_tgs(self, user_spn, etype)` -- Request a TGS service ticket for kerberoasting.
- `KerberoastingEngine.targeted_kerberoast` (method) `modules/kerberoasting.py:271` `def targeted_kerberoast(self, high_value_only)` -- Perform targeted Kerberoasting on enumerated SPNs.
- `KerberoastingEngine.asreproast_check` (method) `modules/kerberoasting.py:306` `def asreproast_check(self, usernames)` -- Check which users do NOT require Kerberos pre-authentication (AS-REP roastable).
- `KerberoastingEngine.extract_hashes_from_pcap` (method) `modules/kerberoasting.py:321` `def extract_hashes_from_pcap(self, pcap_path)` -- Extract Kerberoast hashes from a PCAP/PCAPNG network capture.
- `KerberoastingEngine.detect_kerberoasting_activity` (method) `modules/kerberoasting.py:336` `def detect_kerberoasting_activity(self, event_log)` -- Analyze Windows Event Logs for signs of Kerberoasting attacks.
- `KerberoastingEngine.build_hashcat_batch` (method) `modules/kerberoasting.py:379` `def build_hashcat_batch(self, output_path)` -- Build a batch file with all extracted hashes for Hashcat cracking.
- `KerberoastingEngine.summary` (method) `modules/kerberoasting.py:401` `def summary(self)` -- Return a summary of kerberoasting operations.

## modules/kerberos_core.py
Imported by: `modules/kerberoasting.py`, `modules/kerberos_tickets.py`
- `KerberosPrincipal.to_string` (method) `modules/kerberos_core.py:152` `def to_string(self)`
- `KerberosTicket.has_flag` (method) `modules/kerberos_core.py:207` `def has_flag(self, flag_name)`
- `KerberosCrypto.__init__` (method) `modules/kerberos_core.py:277` `def __init__(self)`
- `KerberosCrypto.derive_aes_key` (method) `modules/kerberos_core.py:282` `def derive_aes_key(password, salt, etype)` -- Derive an AES Kerberos key from a password using string-to-key.
- `KerberosCrypto.derive_rc4_key` (method) `modules/kerberos_core.py:318` `def derive_rc4_key(password)` -- Derive RC4-HMAC Kerberos key from password (hash = MD4(UTF16LE(password))).
- `KerberosCrypto.aes_encrypt` (method) `modules/kerberos_core.py:329` `def aes_encrypt(self, key, plaintext, usage)` -- AES encrypt with Kerberos ciphertext stealing (CTS) mode.
- `KerberosCrypto.aes_decrypt` (method) `modules/kerberos_core.py:361` `def aes_decrypt(self, key, ciphertext, usage)` -- AES decrypt with Kerberos CTS mode.
- `KerberosCrypto.compute_checksum` (method) `modules/kerberos_core.py:389` `def compute_checksum(key, data, etype)` -- Compute a Kerberos checksum using HMAC-SHA1-96-AES.
- `KerberosCore.__init__` (method) `modules/kerberos_core.py:421` `def __init__(self, domain, dc_host, dc_ip)`
- `KerberosCore.get_supported_etypes` (method) `modules/kerberos_core.py:427` `def get_supported_etypes(self)` -- Return encryption types supported by this implementation.
- `KerberosCore.build_as_req` (method) `modules/kerberos_core.py:435` `def build_as_req(self, username, domain, password, etype)` -- Build an AS-REQ message for TGT retrieval.
- `KerberosCore.build_tgs_req` (method) `modules/kerberos_core.py:489` `def build_tgs_req(self, params)` -- Build a TGS-REQ message for service ticket retrieval.
- `KerberosCore.parse_as_rep` (method) `modules/kerberos_core.py:534` `def parse_as_rep(self, as_rep_data, key, etype)` -- Parse an AS-REP response and extract the TGT and session key.
- `KerberosCore.parse_tgs_rep` (method) `modules/kerberos_core.py:550` `def parse_tgs_rep(self, tgs_rep_data, session_key, etype)` -- Parse a TGS-REP response and extract the service ticket.
- `KerberosCore.decrypt_ticket` (method) `modules/kerberos_core.py:563` `def decrypt_ticket(self, ticket_data, key, etype)` -- Decrypt the encrypted portion of a Kerberos ticket.
- `KerberosCore.parse_pac` (method) `modules/kerberos_core.py:588` `def parse_pac(self, pac_data)` -- Parse a Privilege Attribute Certificate (PAC) from decrypted auth data.
- `KerberosErrorParser.parse_error` (method) `modules/kerberos_core.py:687` `def parse_error(error_data)` -- Extract error code, message, and client/server realm from a KRB-ERROR.
- `TicketValidator.is_expired` (method) `modules/kerberos_core.py:706` `def is_expired(endtime, grace_period)` -- Check if a ticket has expired.
- `TicketValidator.validate_flags` (method) `modules/kerberos_core.py:719` `def validate_flags(ticket, required_flags)` -- Check that a ticket has all required flags.
- `TicketValidator.validate_pac_checksums` (method) `modules/kerberos_core.py:735` `def validate_pac_checksums(pac)` -- Validate PAC server and KDC checksums.

## modules/kerberos_tickets.py
Depends on: `modules/kerberos_core.py`
Imported by: `cli/commands/active_directory.py`
- `SilverTicketForger.__init__` (method) `modules/kerberos_tickets.py:131` `def __init__(self)`
- `SilverTicketForger.forge` (method) `modules/kerberos_tickets.py:134` `def forge(self, config)` -- Forge a silver ticket for the specified service.
- `GoldenTicketForger.__init__` (method) `modules/kerberos_tickets.py:272` `def __init__(self)`
- `GoldenTicketForger.forge` (method) `modules/kerberos_tickets.py:275` `def forge(self, config)` -- Forge a golden ticket TGT.
- `DiamondTicketForger.__init__` (method) `modules/kerberos_tickets.py:405` `def __init__(self)`
- `DiamondTicketForger.forge` (method) `modules/kerberos_tickets.py:408` `def forge(self, config)` -- Forge a diamond ticket with PAC enhancement.
- `SapphireTicketForger.__init__` (method) `modules/kerberos_tickets.py:469` `def __init__(self, kerberos_core)`
- `SapphireTicketForger.forge_s4u2self` (method) `modules/kerberos_tickets.py:472` `def forge_s4u2self(self, tgt, session_key, target_user, target_service, domain)` -- Generate a TGS-REQ for S4U2self service ticket.
- `SapphireTicketForger.forge_rbcd` (method) `modules/kerberos_tickets.py:530` `def forge_rbcd(self, machine_account_hash, target_service, domain, username)` -- Generate exploit instructions for resource-based constrained delegation.
- `SkeletonKeyInjector.detect_skeleton_key` (method) `modules/kerberos_tickets.py:578` `def detect_skeleton_key(target_host, domain, dc_ip)` -- Check if skeleton key is active on a DC.
- `SkeletonKeyInjector.inject_command` (method) `modules/kerberos_tickets.py:600` `def inject_command(target_host)` -- Generate mimikatz command for skeleton key injection on a DC.
- `SkeletonKeyInjector.cleanup_command` (method) `modules/kerberos_tickets.py:612` `def cleanup_command()` -- Generate LSASS restart command to remove skeleton key patch.

## modules/kill_chain_viz.py
Depends on: `modules/killchain.py`
Imported by: `lazyc2.py`
- `generate_html` (function) `modules/kill_chain_viz.py:69` `def generate_html(target, sessions)`
- `generate_svg` (function) `modules/kill_chain_viz.py:102` `def generate_svg(target, sessions)`

## modules/killchain.py
Depends on: `core/logging.py`, `modules/world_model.py`
Imported by: `cli/commands/ai.py`, `cli/dashboard_tui.py`, `cli/killchain.py`, `cli/lazynmap_post.py`, `cli/ops_commands.py`, `cli/recon_plan.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `lazygui/panels/killchain_panel.py`, `modules/kill_chain_viz.py`, `modules/lazy_cli_bridge.py`, `modules/lazyown_bridge.py`, `modules/opsec_scorer.py`, `modules/sinks/killchain.py`, `scripts/devtools/core_smoke.py`, `skills/autonomous_daemon.py`, `skills/hermes-lazyown/constants.py`, `skills/lazyown_mcp.py`, `tests/test_killchain_snapshot.py`, `tests/test_killchain_unified_v2.py`, `tests/test_single_source_of_truth.py`
- `KillChainConfig.world_model_path` (method) `modules/killchain.py:118` `def world_model_path(self)` -- Return the resolved path to world_model.json.
- `KillChainConfig.phase_index` (method) `modules/killchain.py:122` `def phase_index(self, phase)` -- Return the positional index of a canonical phase in the kill chain.
- `KillChainConfig.is_valid_phase` (method) `modules/killchain.py:129` `def is_valid_phase(self, phase)` -- Return True when ``phase`` is a recognised canonical phase.
- `KillChain.config` (method) `modules/killchain.py:156` `def config()` -- Return the centralised configuration.
- `KillChain.phases` (method) `modules/killchain.py:161` `def phases()` -- Return the canonical 8-phase tuple.
- `KillChain.phase_labels` (method) `modules/killchain.py:166` `def phase_labels()` -- Return the canonical phase label mapping.
- `KillChain.phase_colors` (method) `modules/killchain.py:171` `def phase_colors()` -- Return the canonical phase hex-color mapping.
- `KillChain.phase_rich_colors` (method) `modules/killchain.py:176` `def phase_rich_colors()` -- Return the canonical phase rich-terminal color mapping.
- `KillChain.engagement_phase_to_cli` (method) `modules/killchain.py:181` `def engagement_phase_to_cli(engagement_value)` -- Map a ``WorldModel.EngagementPhase`` value to the CLI phase key.
- `KillChain.cli_phase_to_host_state` (method) `modules/killchain.py:193` `def cli_phase_to_host_state(phase)` -- Map a CLI phase to a ``WorldModel.HostState`` value.
- `KillChain.current_phase` (method) `modules/killchain.py:206` `def current_phase(world_model_path)` -- Derive the current kill-chain phase.
- `KillChain.advance_phase` (method) `modules/killchain.py:253` `def advance_phase(new_phase, world_model_path, host, extras)` -- Advance the kill-chain phase for connected surfaces.
- `KillChain.get_progress` (method) `modules/killchain.py:357` `def get_progress(world_model_path)` -- Return the current kill-chain progress as a list of status objects.
- `KillChain.compact_progress` (method) `modules/killchain.py:406` `def compact_progress(current_phase, phases_entered)` -- Return a compact single-line progress indicator ``[R>E>X>P>L]``.
- `KillChain.phases_for_display` (method) `modules/killchain.py:426` `def phases_for_display()` -- Return an ordered ``(key, label, hex_color)`` triple for every phase.
- `KillChain.phase_index` (method) `modules/killchain.py:437` `def phase_index(phase)` -- Return the zero-based index of a canonical phase.
- `KillChain.snapshot` (method) `modules/killchain.py:442` `def snapshot(world_model_path)` -- Return a single, render-agnostic snapshot of the whole kill-chain.
- `get_killchain` (function) `modules/killchain.py:482` `def get_killchain()` -- Return the ``KillChain`` class as a module-level entry point.

## modules/kivi.py
- `ReverseShellApp.build` (method) `modules/kivi.py:12` `def build(self)`
- `ReverseShellApp.connect_to_server` (method) `modules/kivi.py:27` `def connect_to_server(self, instance)`

## modules/lab_runtime.py
Depends on: `modules/metasploitable_migrations.py`
Imported by: `tests/test_bdd_infra_range_report.py`, `tests/test_infra_disposable.py`
- `docker_available` (function) `modules/lab_runtime.py:93` `def docker_available()` -- Return whether the Docker daemon is reachable.
- `running_containers` (function) `modules/lab_runtime.py:115` `def running_containers()` -- Return the running lab container names.
- `existing_containers` (function) `modules/lab_runtime.py:131` `def existing_containers()` -- Return every lab container name including stopped ones.
- `running_range_containers` (function) `modules/lab_runtime.py:148` `def running_range_containers()` -- Return the running cyber range container names.
- `container_name` (function) `modules/lab_runtime.py:164` `def container_name(scenario)` -- Return the container name for one lab scenario.
- `container_ip` (function) `modules/lab_runtime.py:169` `def container_ip(container_name)` -- Resolve one container's IPv4 on its Docker network.
- `ensure_web` (function) `modules/lab_runtime.py:183` `def ensure_web(scenario, name)` -- Start Apache inside a metasploitable container that booted without it.
- `apply_gym_migrations` (function) `modules/lab_runtime.py:242` `def apply_gym_migrations(name)` -- Apply the metasploitable gym migrations, returning the report.
- `start` (function) `modules/lab_runtime.py:250` `def start(scenario)` -- Spin up one lab scenario container.
- `stop` (function) `modules/lab_runtime.py:304` `def stop(scenario)` -- Stop one lab scenario container.
- `stop_all` (function) `modules/lab_runtime.py:322` `def stop_all()` -- Stop every running lab container.
- `range_compose` (function) `modules/lab_runtime.py:340` `def range_compose(profile)` -- Return the compose file path for one range profile, or None.
- `start_range` (function) `modules/lab_runtime.py:349` `def start_range(profile)` -- Start one cyber range profile via Docker Compose.
- `stop_range` (function) `modules/lab_runtime.py:368` `def stop_range(profile)` -- Stop one cyber range profile (compose down).
- `stop_ranges` (function) `modules/lab_runtime.py:379` `def stop_ranges()` -- Stop every running cyber range.
- `ensure_range_secret` (function) `modules/lab_runtime.py:420` `def ensure_range_secret(profile_dir)` -- Generate the DC admin secret file when missing.

## modules/lazy_agent.py
Depends on: `core/config.py`, `modules/__init__.py`, `modules/agent_runner.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/llm_factory.py`, `modules/loop_ai_bridge.py`
Imported by: `cli/commands/lazyops.py`, `tests/conftest.py`, `tests/test_lazy_agent.py`
- `model_timeout_sec` (function) `modules/lazy_agent.py:41` `def model_timeout_sec()` -- Return the hard per-turn model timeout from configuration.
- `tool_calling_enabled` (function) `modules/lazy_agent.py:57` `def tool_calling_enabled()` -- Return whether agentic tool calling is enabled by configuration.
- `max_iterations` (function) `modules/lazy_agent.py:72` `def max_iterations()` -- Return the bounded agent step budget from configuration.
- `resolve_agentic_model` (function) `modules/lazy_agent.py:83` `def resolve_agentic_model(exclude)` -- Return a raw tool-calling backend for the best pool member, or None.
- `ObservableAgentRunner.__init__` (method) `modules/lazy_agent.py:148` `def __init__(self, model, system_prompt, max_iterations, on_event)` -- Bind the model and the optional event sink (kind, name, text).
- `ObservableAgentRunner.run` (method) `modules/lazy_agent.py:168` `def run(self, user_input)` -- Base loop plus final-turn persistence for true resume.
- `ConversationStore.__init__` (method) `modules/lazy_agent.py:264` `def __init__(self, task_id)` -- Bind the conversation store for one task (``main`` when empty).
- `ConversationStore.intent_messages` (method) `modules/lazy_agent.py:273` `def intent_messages(self, intent_id)` -- Return the stored messages for one intent (resume seed).
- `ConversationStore.save_intent` (method) `modules/lazy_agent.py:278` `def save_intent(self, intent_id, messages)` -- Persist the tail of one intent conversation.
- `ConversationStore.session` (method) `modules/lazy_agent.py:287` `def session(self, session_id)` -- Return one main-agent session payload (empty when unknown).
- `ConversationStore.sessions` (method) `modules/lazy_agent.py:291` `def sessions(self)` -- List main-agent sessions with title, message count and age.
- `ConversationStore.save_session` (method) `modules/lazy_agent.py:305` `def save_session(self, session_id, messages, title)` -- Persist one main-agent session conversation tail.
- `ConversationStore.reset_intents` (method) `modules/lazy_agent.py:315` `def reset_intents(self)` -- Drop every stored intent conversation (fresh agent start).
- `register_tools` (function) `modules/lazy_agent.py:322` `def register_tools(runner, specs)` -- Register tool specs (name, description, func, parameters, required).
- `run_worker_session` (function) `modules/lazy_agent.py:335` `def run_worker_session(model, task_id, intent_id, system_prompt, launch_prompt, tools, on_event)` -- Run one agentic intent attempt with resume seeding.
- `run_main_session` (function) `modules/lazy_agent.py:374` `def run_main_session(model, session_id, system_prompt, prompt, tools, on_event)` -- Run one main-agent turn, resuming the stored session conversation.
- `run_external_opencode` (function) `modules/lazy_agent.py:396` `def run_external_opencode(prompt, session_id, agent, cwd, timeout_sec)` -- Run one headless ``opencode run`` task with MCP tooling.
- `run_external_hermes` (function) `modules/lazy_agent.py:472` `def run_external_hermes(prompt, session_id, cwd, timeout_sec, max_turns, run_budget)` -- Run one detached ``hermes chat --oneshot`` task.

## modules/lazy_bridge.py
Depends on: `modules/finding_lifecycle.py`, `modules/traffic_recorder.py`, `modules/world_model.py`
Imported by: `cli/commands/lazyloop.py`, `modules/lazy_loop.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_cve_pipeline.py`, `tests/test_lazy_loop.py`
- `lazy_tasks` (function) `modules/lazy_bridge.py:92` `def lazy_tasks()` -- Load LAZY task registry.
- `lazy_assets` (function) `modules/lazy_bridge.py:103` `def lazy_assets()` -- Load LAZY asset nodes.
- `lazy_graph` (function) `modules/lazy_bridge.py:114` `def lazy_graph(task_id)` -- Load experiment graph for a task.
- `lazy_activity` (function) `modules/lazy_bridge.py:127` `def lazy_activity(task_id)` -- Load activity transcript for a task.
- `lazy_traffic` (function) `modules/lazy_bridge.py:139` `def lazy_traffic(task_id)` -- Load traffic log for a task.
- `lazy_guard_audit` (function) `modules/lazy_bridge.py:151` `def lazy_guard_audit(task_id)` -- Load guard audit for a task.
- `bridge_status` (function) `modules/lazy_bridge.py:163` `def bridge_status()` -- Summarize LAZY universe and last sync cursor.
- `pull_to_world_model` (function) `modules/lazy_bridge.py:221` `def pull_to_world_model()` -- Sync LAZY graphs and assets into LazyOwn world model.
- `pull_to_objectives` (function) `modules/lazy_bridge.py:298` `def pull_to_objectives()` -- Inject open LAZY tasks as LazyOwn objectives without duplicates.
- `pull_findings_to_lifecycle` (function) `modules/lazy_bridge.py:333` `def pull_findings_to_lifecycle()` -- Confirm LAZY finding nodes in LazyOwn finding lifecycle.
- `pull_traffic_to_recorder` (function) `modules/lazy_bridge.py:408` `def pull_traffic_to_recorder(progress)` -- Mirror new LAZY traffic rows into the LazyOwn recorder index.
- `push_objective_to_lazy` (function) `modules/lazy_bridge.py:476` `def push_objective_to_lazy(goal, scope)` -- Export a LazyOwn objective as an LAZY-compatible task draft.
- `push_tasks_to_c2` (function) `modules/lazy_bridge.py:501` `def push_tasks_to_c2(only)` -- Mirror loop tasks into the lazyc2 Kanban board (sessions/tasks.json).
- `sync_all` (function) `modules/lazy_bridge.py:566` `def sync_all(progress)` -- Run full bidirectional pull plus lifecycle, traffic and board mirror.

## modules/lazy_cli_bridge.py
Depends on: `core/config.py`, `modules/killchain.py`, `modules/verb_catalog.py`
Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/chain_distill.py`, `modules/lazy_intel.py`, `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/verb_catalog.py`, `tests/test_loop_cli_catalog.py`
- `cli_verbs` (function) `modules/lazy_cli_bridge.py:106` `def cli_verbs()` -- Return every discovered shell verb, cached by source mtime.
- `is_cli_verb` (function) `modules/lazy_cli_bridge.py:125` `def is_cli_verb(name)` -- Return True when name is a real shell command.
- `phase_for` (function) `modules/lazy_cli_bridge.py:131` `def phase_for(verb)` -- Map a verb to its kill-chain phase via keyword affinity.
- `risk_for` (function) `modules/lazy_cli_bridge.py:140` `def risk_for(verb)` -- Classify a verb as safe, exploit or high risk.
- `needs_target_for` (function) `modules/lazy_cli_bridge.py:150` `def needs_target_for(verb)` -- Return whether the verb usually carries a target argument.
- `build_cli_command` (function) `modules/lazy_cli_bridge.py:158` `def build_cli_command(verb, target)` -- Build a shell line for any CLI verb bound to target.
- `search_cli_verbs` (function) `modules/lazy_cli_bridge.py:185` `def search_cli_verbs(query, phase, limit)` -- Search the full CLI catalog by keyword and phase.
- `cli_catalog_for_phase` (function) `modules/lazy_cli_bridge.py:211` `def cli_catalog_for_phase(phase, limit)` -- Return a compact verb list for LLM prompt injection.
- `catalog_cli_for_phase` (function) `modules/lazy_cli_bridge.py:219` `def catalog_cli_for_phase(limit)` -- Return enabled catalog commands for the current kill-chain phase.
- `full_cli_enabled` (function) `modules/lazy_cli_bridge.py:253` `def full_cli_enabled()` -- Return whether the loop may route any CLI verb.
- `set_full_cli` (function) `modules/lazy_cli_bridge.py:276` `def set_full_cli(enabled)` -- Persist the full-CLI routing flag and return the new value.

## modules/lazy_creds.py
- `load` (function) `modules/lazy_creds.py:39` `def load()` -- Load the CSV knowledge base once per process.
- `search` (function) `modules/lazy_creds.py:63` `def search(query)` -- Return rows whose vendor or username contains the query.
- `candidates` (function) `modules/lazy_creds.py:79` `def candidates(limit)` -- Return the most repeated (username, password) pairs for spraying.
- `count` (function) `modules/lazy_creds.py:96` `def count()` -- Return the total number of knowledge-base rows.
- `as_lines` (function) `modules/lazy_creds.py:101` `def as_lines(rows)` -- Render rows as aligned ``vendor,username,password`` lines.
- `export_pairs` (function) `modules/lazy_creds.py:106` `def export_pairs(path, limit)` -- Export ``username:password`` pairs for spray tools.

## modules/lazy_cve_feed.py
Depends on: `modules/lazy_heat.py`
Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`
- `load_kev` (function) `modules/lazy_cve_feed.py:158` `def load_kev(force)` -- Return ``{cve_id: {product, vendor}}`` from the CISA KEV catalog.
- `load_epss` (function) `modules/lazy_cve_feed.py:192` `def load_epss(force)` -- Return ``{cve_id: epss}`` from the FIRST daily EPSS scores.
- `load_exploit_cves` (function) `modules/lazy_cve_feed.py:233` `def load_exploit_cves(force)` -- Return CVE ids with public exploit code (Exploit-DB index).
- `load_msf_cves` (function) `modules/lazy_cve_feed.py:257` `def load_msf_cves(force)` -- Return CVE ids weaponized as Metasploit modules.
- `fetch_product_advisories` (function) `modules/lazy_cve_feed.py:291` `def fetch_product_advisories(product, force)` -- Fetch OSV advisories naming one product.
- `cve_intel` (function) `modules/lazy_cve_feed.py:360` `def cve_intel(cve_id, feeds, allow_network)` -- Assemble exploitation signals and the heat tier for one CVE.
- `correlate` (function) `modules/lazy_cve_feed.py:438` `def correlate(product, version, allow_network)` -- Version-aware CVE candidates for one service product.
- `load_kev_matches` (function) `modules/lazy_cve_feed.py:526` `def load_kev_matches(product, feeds)` -- KEV entries whose vendor/product names match one service product.
- `hot_matches` (function) `modules/lazy_cve_feed.py:568` `def hot_matches(services, allow_network)` -- Hot/warm CVE candidates matching discovered services.
- `refresh_feeds_async` (function) `modules/lazy_cve_feed.py:612` `def refresh_feeds_async(products)` -- Refresh bulk feeds in one background daemon thread.

## modules/lazy_heat.py
Imported by: `modules/atomic_exploit_bridge.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/lazy_cve_feed.py`, `modules/loop_triggers.py`
- `classify_heat` (function) `modules/lazy_heat.py:68` `def classify_heat(kev, epss, exploit, cvss)` -- Return the heat tier of one CVE from its exploitation signals.
- `match_heat` (function) `modules/lazy_heat.py:91` `def match_heat(tier, cvss, verdict, distro_status)` -- Return the heat of one CVE *on one host*.
- `parse_version` (function) `modules/lazy_heat.py:118` `def parse_version(value, strict)` -- Parse a dotted version string into a comparable tuple.
- `compare_versions` (function) `modules/lazy_heat.py:154` `def compare_versions(a, b)` -- Compare two version tuples zero-padded so (1, 18) == (1, 18, 0).
- `version_in_range` (function) `modules/lazy_heat.py:162` `def version_in_range(ver, rng)` -- Return True/False/None for ``ver`` inside one affected range.
- `cvss3_base_score` (function) `modules/lazy_heat.py:204` `def cvss3_base_score(vector)` -- Compute the CVSS v3 base score from an inline vector string.
- `product_token` (function) `modules/lazy_heat.py:246` `def product_token(value)` -- Normalise a product name to one comparable token.
- `token_matches` (function) `modules/lazy_heat.py:269` `def token_matches(haystack, needle)` -- Whole-token containment of ``needle`` inside ``haystack``.
- `parse_distro_revision` (function) `modules/lazy_heat.py:303` `def parse_distro_revision(banner)` -- Read the distro family and package release from a service banner.
- `backport_status` (function) `modules/lazy_heat.py:342` `def backport_status(banner, fixed_revision)` -- Classify whether a distro already backported the fix.
- `label_for` (function) `modules/lazy_heat.py:370` `def label_for(status, fixed_revision)` -- Human-readable label for one backport status.

## modules/lazy_installer.py
Depends on: `core/config.py`, `modules/auto_registry.py`
Imported by: `cli/commands/lazyops.py`, `modules/auto_registry.py`, `modules/lazy_loop.py`
- `installer_enabled` (function) `modules/lazy_installer.py:41` `def installer_enabled()` -- Return whether the loop may resolve install intents.
- `set_installer_enabled` (function) `modules/lazy_installer.py:58` `def set_installer_enabled(enabled)` -- Persist the installer flag and return the stored value.
- `install_command_for` (function) `modules/lazy_installer.py:70` `def install_command_for(tool)` -- Return the allowlisted install recipe for one tool, or None.
- `intent_for` (function) `modules/lazy_installer.py:75` `def intent_for(tool)` -- Build the canonical install intent summary for one tool.
- `tool_from_intent` (function) `modules/lazy_installer.py:80` `def tool_from_intent(text)` -- Extract the tool name from an install intent, else empty string.
- `steps_for_install` (function) `modules/lazy_installer.py:88` `def steps_for_install(text)` -- Resolve an install intent to its recipe, or None.

## modules/lazy_intel.py
Depends on: `core/config.py`, `modules/lazy_cli_bridge.py`, `modules/mediation/__init__.py`, `modules/world_model.py`, `utils.py`
Imported by: `modules/lazy_loop.py`, `modules/lazy_orchestrator_feedback.py`, `modules/mediation/intel_mediator.py`, `modules/sinks/routing.py`, `tests/test_loop_supervision.py`, `tests/test_mediation.py`
- `infer_source` (function) `modules/lazy_intel.py:88` `def infer_source(command, intent_text)` -- Classify where a resolved step likely came from.
- `describe_command` (function) `modules/lazy_intel.py:114` `def describe_command(command)` -- Describe a command with phase and risk.
- `record_routing_decision` (function) `modules/lazy_intel.py:129` `def record_routing_decision(task_id, intent_id, command, intent_text, target, stack)` -- Record which verb the loop chose for one intent.
- `record_routing_outcome` (function) `modules/lazy_intel.py:169` `def record_routing_outcome(task_id, intent_id, command, state, facts, findings, stack)` -- Record the terminal outcome of one executed command.
- `read_decisions` (function) `modules/lazy_intel.py:211` `def read_decisions(task_id, limit)` -- Read routing records, optionally filtered by task.
- `mask_configured` (function) `modules/lazy_intel.py:237` `def mask_configured(text)` -- Mask only operator-configured credential values in live text.
- `stack_signature` (function) `modules/lazy_intel.py:272` `def stack_signature(assets)` -- Fingerprint the target stack from service assets.
- `fuse_routing_decisions` (function) `modules/lazy_intel.py:303` `def fuse_routing_decisions(task_id)` -- Fuse routing records into the world model as host notes.
- `export_spans` (function) `modules/lazy_intel.py:342` `def export_spans(task_id, out)` -- Export activity records as trace spans for observability.


Next: [API_p14.md](API_p14.md)
