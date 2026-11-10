# API (page 15 of 27)
Previous: [API_p14.md](API_p14.md)

## modules/lazy_match_policy.py
Depends on: `modules/lazy_heat.py`
Imported by: `tests/test_lazy_match_policy.py`
- `strand_from_sighting` (function) `modules/lazy_match_policy.py:37` `def strand_from_sighting(sighting)` -- Classify one product sighting per the doctrine.
- `is_os_sighting` (function) `modules/lazy_match_policy.py:79` `def is_os_sighting(product, cpe)` -- Return True when the sighting names an operating system.
- `strand_rank` (function) `modules/lazy_match_policy.py:102` `def strand_rank(strand)` -- Return the merge precedence of a strand.
- `has_standing` (function) `modules/lazy_match_policy.py:107` `def has_standing(match)` -- Return True when humans or durable evidence touched a match.
- `MatchStore.__init__` (method) `modules/lazy_match_policy.py:127` `def __init__(self, sessions_dir)` -- Bind the store file under sessions/lazy.
- `MatchStore.upsert` (method) `modules/lazy_match_policy.py:132` `def upsert(self, identity, sighting, now)` -- Record one sighting under the dedupe identity.
- `MatchStore.rows` (method) `modules/lazy_match_policy.py:177` `def rows(self)` -- Return every stored row.
- `MatchStore.close` (method) `modules/lazy_match_policy.py:181` `def close(self, identity, reason, now)` -- Close one row, keeping its reason and reopening block.
- `MatchStore.closed_reason` (method) `modules/lazy_match_policy.py:196` `def closed_reason(self, identity)` -- Return the persisted closure reason, or '' when open or unknown.

## modules/lazy_mentions.py
Depends on: `modules/lazy_loop.py`, `skills/mcp_tools/lazy_finding.py`
Imported by: `cli/commands/lazyloop.py`, `lazyc2.py`, `skills/mcp_tools/lazy_mention.py`, `tests/test_security_codeql_batch.py`
- `search_mentions_page` (function) `modules/lazy_mentions.py:193` `def search_mentions_page(kind, query, cursor)` -- Search one scroll page of mention candidates.
- `parse_mentions` (function) `modules/lazy_mentions.py:237` `def parse_mentions(message)` -- Parse @[kind#id] tokens trusting type plus numeric id only.
- `compose_message` (function) `modules/lazy_mentions.py:268` `def compose_message(message)` -- Append server-read snapshots for referenced records as data.

## modules/lazy_netattack.py
Imported by: `tests/test_lazy_netattack.py`
- `AttackVectorVerdict.as_dict` (method) `modules/lazy_netattack.py:107` `def as_dict(self)` -- Return one JSON-safe view.
- `surface_decision` (function) `modules/lazy_netattack.py:184` `def surface_decision(evidence)` -- Grade the Windows network-attack families from evidence bags.
- `hint_text` (function) `modules/lazy_netattack.py:311` `def hint_text(verdict)` -- Shape one loop hint line for a verdict.

## modules/lazy_objective_queue.py
Depends on: `modules/lazy_loop.py`
- `pending_objectives` (function) `modules/lazy_objective_queue.py:105` `def pending_objectives(limit, target)` -- Return pending objectives shaped as planner candidates.
- `mark_started` (function) `modules/lazy_objective_queue.py:177` `def mark_started(objective_id, task_id)` -- Mark an objective ``in_progress`` when a task claims it.
- `settle` (function) `modules/lazy_objective_queue.py:196` `def settle(objective_id, task_id, success)` -- Complete a done objective or requeue an unfinished one.
- `objective_ids_from_text` (function) `modules/lazy_objective_queue.py:235` `def objective_ids_from_text(text)` -- Extract the objective id embedded in an intent summary prefix.

## modules/lazy_oob.py
Depends on: `modules/backdoor/server.c`
- `OobHit.as_dict` (method) `modules/lazy_oob.py:51` `def as_dict(self)` -- Return the JSON-serialisable row.
- `_CanaryHandler.do_GET` (method) `modules/lazy_oob.py:92` `def do_GET(self)` -- Record a GET callback.
- `_CanaryHandler.do_POST` (method) `modules/lazy_oob.py:97` `def do_POST(self)` -- Record a POST callback (body discarded).
- `_CanaryHandler.do_HEAD` (method) `modules/lazy_oob.py:102` `def do_HEAD(self)` -- Record a HEAD callback.
- `_CanaryHandler.log_message` (method) `modules/lazy_oob.py:107` `def log_message(self, fmt)` -- Silence the default stderr access log.
- `record_hit` (function) `modules/lazy_oob.py:112` `def record_hit(hit)` -- Store one hit in memory and append it to the JSONL mirror.
- `start` (function) `modules/lazy_oob.py:128` `def start(host, port)` -- Start (or reuse) the canary listener.
- `new_token` (function) `modules/lazy_oob.py:167` `def new_token()` -- Return one URL-safe callback token.
- `url` (function) `modules/lazy_oob.py:184` `def url(token)` -- Return the callback URL for a token (latest when omitted).
- `hits` (function) `modules/lazy_oob.py:204` `def hits(token)` -- Return recorded hits, optionally filtered by token.
- `stop` (function) `modules/lazy_oob.py:220` `def stop()` -- Shut the canary down and report how many hits it saw.
- `reset` (function) `modules/lazy_oob.py:241` `def reset()` -- Clear recorded hits and stop the listener (operator/test utility).
- `is_running` (function) `modules/lazy_oob.py:249` `def is_running()` -- Return whether the canary listener is alive.

## modules/lazy_orchestrator_feedback.py
Depends on: `modules/lazy_cli_bridge.py`, `modules/lazy_intel.py`
Imported by: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/mediation/feedback_mediator.py`, `tests/test_loop_supervision.py`, `tests/test_mediation.py`
- `adjust_from_usage` (function) `modules/lazy_orchestrator_feedback.py:61` `def adjust_from_usage(limit)` -- Fold routing outcomes into per-(phase, stack, verb) success priors.
- `verb_prior` (function) `modules/lazy_orchestrator_feedback.py:162` `def verb_prior(phase, verb, stack)` -- Return the success prior for one (phase, stack, verb) triple.
- `rank_verbs` (function) `modules/lazy_orchestrator_feedback.py:189` `def rank_verbs(phase, verbs, stack)` -- Order verbs by learned success rate, stable for cold verbs.
- `order_steps` (function) `modules/lazy_orchestrator_feedback.py:213` `def order_steps(steps, stack)` -- Reorder resolved step lines by stack-aware verb priors.
- `export_dataset` (function) `modules/lazy_orchestrator_feedback.py:238` `def export_dataset(out, limit)` -- Export instruction-tuning rows joined from decisions + outcomes.

## modules/lazy_osinfer.py
Depends on: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/world_model.py`
- `infer_from_ttl` (function) `modules/lazy_osinfer.py:47` `def infer_from_ttl(ttl)` -- Infer the remote OS family from a reply's TTL value.
- `infer_from_ping_output` (function) `modules/lazy_osinfer.py:72` `def infer_from_ping_output(output)` -- Read ``ttl=``/``TTL=`` from ping output and classify the OS.
- `infer_from_banner` (function) `modules/lazy_osinfer.py:97` `def infer_from_banner(text)` -- Infer the OS family from service names or banner text.
- `merge_os` (function) `modules/lazy_osinfer.py:118` `def merge_os(current, new)` -- Merge two inferred OS hints; a confident value wins.
- `addon_target_os` (function) `modules/lazy_osinfer.py:130` `def addon_target_os(name)` -- Return the ``os:`` field of one lazyaddon manifest.
- `verb_target_os` (function) `modules/lazy_osinfer.py:157` `def verb_target_os(command)` -- Return the OS family one command line targets.
- `os_compatible` (function) `modules/lazy_osinfer.py:194` `def os_compatible(verb_os, host_os)` -- Whether a verb's target OS may run against a host's inferred OS.
- `verb_compatible_with_host` (function) `modules/lazy_osinfer.py:216` `def verb_compatible_with_host(command, host_os)` -- Gate one command line against a host's inferred OS.
- `host_os_for_target` (function) `modules/lazy_osinfer.py:239` `def host_os_for_target(target)` -- Return the remembered OS for one target host.
- `remember_host_os` (function) `modules/lazy_osinfer.py:287` `def remember_host_os(target, os_name, reason)` -- Persist an inferred OS on the asset graph and world model.
- `learn_from_transcripts` (function) `modules/lazy_osinfer.py:330` `def learn_from_transcripts(target, transcripts)` -- Infer and remember the host OS from executed step outputs.

## modules/lazy_probes.py
Imported by: `modules/lazy_autofire.py`, `modules/lazy_exposure.py`, `tests/test_lazy_probes.py`
- `range_text` (function) `modules/lazy_probes.py:70` `def range_text(ranges)` -- Render affected ranges as a human phrase.
- `check_errors` (function) `modules/lazy_probes.py:108` `def check_errors(kind, params)` -- Validate one check request against the kind's allowlist.
- `render_check` (function) `modules/lazy_probes.py:156` `def render_check(kind, params)` -- Render one read-only validation command.
- `render_checks` (function) `modules/lazy_probes.py:177` `def render_checks(checks)` -- Render a batch of checks in order.

## modules/lazy_proxy.py
Depends on: `core/hardening.py`, `core/logging.py`, `modules/backdoor/server.c`, `modules/traffic_recorder.py`
Imported by: `cli/commands/lazyops.py`, `tests/test_lazy_proxy.py`, `tests/test_lazy_runner.py`, `tests/test_security_alerts_fix.py`, `tests/test_security_codeql_batch.py`
- `tls_lab_unverified_allowed` (function) `modules/lazy_proxy.py:253` `def tls_lab_unverified_allowed(host)` -- Return True only when a lab host has explicit self-signed opt-in.
- `resolve_validated_target` (function) `modules/lazy_proxy.py:282` `def resolve_validated_target(host, port, scheme)` -- Validate a target and return its pinned IP literals.
- `connect_pinned` (function) `modules/lazy_proxy.py:355` `def connect_pinned(host, ips, port, scheme)` -- Open a socket to a pinned validated IP, wrapping TLS for https.
- `_PinnedHTTPConnection.__init__` (method) `modules/lazy_proxy.py:384` `def __init__(self, host, port)` -- Store pinned IPs; hostname is kept for headers only.
- `_PinnedHTTPConnection.connect` (method) `modules/lazy_proxy.py:389` `def connect(self)` -- Dial the pinned IP so DNS cannot re-resolve to another host.
- `_PinnedHTTPSConnection.__init__` (method) `modules/lazy_proxy.py:397` `def __init__(self, host, port)` -- Store pinned IPs and the verifying TLS context.
- `_PinnedHTTPSConnection.connect` (method) `modules/lazy_proxy.py:410` `def connect(self)` -- Dial the pinned IP and verify the cert against the hostname.
- `detect_trust_target` (function) `modules/lazy_proxy.py:490` `def detect_trust_target()` -- Return the first existing system trust anchor directory and refresh command.
- `ca_trusted` (function) `modules/lazy_proxy.py:498` `def ca_trusted(ca_path)` -- Return True when the system anchor already holds this CA.
- `detect_nss_profiles` (function) `modules/lazy_proxy.py:517` `def detect_nss_profiles()` -- Return user NSS database directories (Firefox profiles + Chrome).
- `install_ca_nss` (function) `modules/lazy_proxy.py:532` `def install_ca_nss(ca_path, runner, profiles)` -- Install the recorder CA into user NSS databases via certutil.
- `install_ca_trust` (function) `modules/lazy_proxy.py:572` `def install_ca_trust(ca_path, runner)` -- Install the recorder CA into the system trust store.
- `CertificateAuthority.__init__` (method) `modules/lazy_proxy.py:626` `def __init__(self, pki_dir)` -- Load or create the CA under ``pki_dir``.
- `CertificateAuthority.context_for` (method) `modules/lazy_proxy.py:736` `def context_for(self, host)` -- Return the server TLS context for one host, generating on miss.
- `RecorderServer.__init__` (method) `modules/lazy_proxy.py:779` `def __init__(self, address, handler)`
- `RecorderServer.handle_error` (method) `modules/lazy_proxy.py:786` `def handle_error(self, request, client_address)` -- Silence client-side connection noise instead of tracebacks.
- `ProxyController.__init__` (method) `modules/lazy_proxy.py:806` `def __init__(self)` -- Prepare state; nothing binds until :meth:`start`.
- `ProxyController.start` (method) `modules/lazy_proxy.py:819` `def start(self, host, port, task_id, traffic_dir, upstream)` -- Bind the recorder proxy; idempotent while already running.
- `ProxyController.stop` (method) `modules/lazy_proxy.py:864` `def stop(self)` -- Shut the proxy down; safe when it was never started.
- `ProxyController.status` (method) `modules/lazy_proxy.py:880` `def status(self)` -- Report running state, address, CA path and exchange count.
- `ProxyController.recorder` (method) `modules/lazy_proxy.py:902` `def recorder(self)` -- Return the live recorder for ingestion, or None when stopped.
- `ProxyController.ca_path` (method) `modules/lazy_proxy.py:906` `def ca_path(self)` -- Return the CA certificate path for trust-store wiring.
- `ProxyHandler.log_message` (method) `modules/lazy_proxy.py:921` `def log_message(self, fmt)` -- Silence per-request logging; the recorder is the audit trail.
- `ProxyHandler.do_CONNECT` (method) `modules/lazy_proxy.py:925` `def do_CONNECT(self)` -- Terminate TLS for a CONNECT tunnel and record inner requests.
- `ProxyHandler.do_GET` (method) `modules/lazy_proxy.py:978` `def do_GET(self)` -- Forward every plain HTTP method through one path.
- `get_proxy` (function) `modules/lazy_proxy.py:1336` `def get_proxy()` -- Return the process-wide recorder proxy controller.
- `env_for_ca` (function) `modules/lazy_proxy.py:1345` `def env_for_ca(ca_path, host, port)` -- Build the environment overrides that route tools through the proxy.
- `apply_env` (function) `modules/lazy_proxy.py:1361` `def apply_env(ca_path, host, port)` -- Apply proxy env vars, returning the previous values for restore.
- `restore_env` (function) `modules/lazy_proxy.py:1368` `def restore_env(previous)` -- Restore environment values captured by :func:`apply_env`.

## modules/lazy_rbac.py
Depends on: `cli/commands/enum.py`, `core/logging.py`
Imported by: `cli/commands/session_ops.py`, `cli/engagement_hooks.py`, `cli/tips_engine.py`, `lazyc2.py`, `lazyc2/app_factory.py`, `lazyc2/blueprints/auth.py`, `lazyc2/extensions/users.py`, `lazyc2/models.py`, `modules/cli_auth.py`, `modules/collab_bp.py`
- `Role.valid_roles` (method) `modules/lazy_rbac.py:62` `def valid_roles(cls)`
- `RBACUser.to_dict` (method) `modules/lazy_rbac.py:136` `def to_dict(self)`
- `RBACUser.from_dict` (method) `modules/lazy_rbac.py:140` `def from_dict(cls, data)`
- `RBACUser.get_role` (method) `modules/lazy_rbac.py:164` `def get_role(self)`
- `RBACUser.has_permission` (method) `modules/lazy_rbac.py:170` `def has_permission(self, permission)`
- `RBACUser.can_manage_role` (method) `modules/lazy_rbac.py:174` `def can_manage_role(self, target_role)` -- Check if this user can assign/manage the given role.
- `RBACUser.get_mfa_provisioning_uri` (method) `modules/lazy_rbac.py:182` `def get_mfa_provisioning_uri(self)`
- `RBACUser.verify_totp` (method) `modules/lazy_rbac.py:187` `def verify_totp(self, token)`
- `RBACUser.verify_recovery_code` (method) `modules/lazy_rbac.py:192` `def verify_recovery_code(self, code)`
- `RBACUser.consume_recovery_code` (method) `modules/lazy_rbac.py:200` `def consume_recovery_code(self, code)`
- `RBACStore.__init__` (method) `modules/lazy_rbac.py:213` `def __init__(self, users_path)`
- `RBACStore.load_all` (method) `modules/lazy_rbac.py:245` `def load_all(self)`
- `RBACStore.find_by_id` (method) `modules/lazy_rbac.py:249` `def find_by_id(self, user_id)`
- `RBACStore.find_by_username` (method) `modules/lazy_rbac.py:255` `def find_by_username(self, username)`
- `RBACStore.save` (method) `modules/lazy_rbac.py:261` `def save(self, user)`
- `RBACStore.create_user` (method) `modules/lazy_rbac.py:274` `def create_user(self, username, password_hash, role, tenant_id)`
- `RBACStore.delete_user` (method) `modules/lazy_rbac.py:295` `def delete_user(self, user_id)`
- `RBACStore.update_role` (method) `modules/lazy_rbac.py:304` `def update_role(self, user_id, new_role)`
- `RBACStore.enable_mfa` (method) `modules/lazy_rbac.py:314` `def enable_mfa(self, user_id)`
- `RBACStore.disable_mfa` (method) `modules/lazy_rbac.py:324` `def disable_mfa(self, user_id)`
- `RBACStore.consume_recovery_code` (method) `modules/lazy_rbac.py:334` `def consume_recovery_code(self, user_id, code)`
- `RBACStore.ensure_admin` (method) `modules/lazy_rbac.py:343` `def ensure_admin(self, username, password_hash)` -- Ensure at least one admin exists, creating one if needed.
- `TenantConfig.from_payload` (method) `modules/lazy_rbac.py:377` `def from_payload(cls, tenant_id, name, payload_path)`
- `TenantConfig.to_dict` (method) `modules/lazy_rbac.py:386` `def to_dict(self)`
- `TenantConfig.from_dict` (method) `modules/lazy_rbac.py:390` `def from_dict(cls, data)`
- `TenantManager.__init__` (method) `modules/lazy_rbac.py:397` `def __init__(self, payloads_dir, config_path, default_payload)`
- `TenantManager.list_tenants` (method) `modules/lazy_rbac.py:431` `def list_tenants(self)`
- `TenantManager.get_active` (method) `modules/lazy_rbac.py:434` `def get_active(self)`
- `TenantManager.get_active_payload_path` (method) `modules/lazy_rbac.py:439` `def get_active_payload_path(self)`
- `TenantManager.get_active_sessions_dir` (method) `modules/lazy_rbac.py:445` `def get_active_sessions_dir(self)`
- `TenantManager.get_payload_for_tenant` (method) `modules/lazy_rbac.py:451` `def get_payload_for_tenant(self, tenant_id)`
- `TenantManager.create_tenant` (method) `modules/lazy_rbac.py:457` `def create_tenant(self, name, base_payload)`
- `TenantManager.switch_tenant` (method) `modules/lazy_rbac.py:486` `def switch_tenant(self, tenant_id)`
- `TenantManager.delete_tenant` (method) `modules/lazy_rbac.py:495` `def delete_tenant(self, tenant_id)`
- `TenantManager.ensure_default_tenant` (method) `modules/lazy_rbac.py:504` `def ensure_default_tenant(self)`
- `init_rbac_store` (function) `modules/lazy_rbac.py:523` `def init_rbac_store(users_path)`
- `init_tenant_manager` (function) `modules/lazy_rbac.py:527` `def init_tenant_manager(payloads_dir, config_path, default_payload)`
- `require_role` (function) `modules/lazy_rbac.py:539` `def require_role()` -- Flask decorator: require one of the given roles.
- `decorator` (function) `modules/lazy_rbac.py:542` `def decorator(f)`
- `decorated` (function) `modules/lazy_rbac.py:544` `def decorated()`
- `require_permission` (function) `modules/lazy_rbac.py:565` `def require_permission()` -- Flask decorator: require specific permissions.
- `decorator` (function) `modules/lazy_rbac.py:568` `def decorator(f)`
- `decorated` (function) `modules/lazy_rbac.py:570` `def decorated()`
- `require_mfa` (function) `modules/lazy_rbac.py:596` `def require_mfa(f)` -- Decorator that enforces MFA before accessing protected routes.
- `decorated` (function) `modules/lazy_rbac.py:600` `def decorated()`
- `get_rbac_store` (function) `modules/lazy_rbac.py:639` `def get_rbac_store()`
- `set_rbac_store` (function) `modules/lazy_rbac.py:643` `def set_rbac_store(store)`
- `get_tenant_manager` (function) `modules/lazy_rbac.py:648` `def get_tenant_manager()`
- `set_tenant_manager` (function) `modules/lazy_rbac.py:655` `def set_tenant_manager(tm)`
- `check_cli_permission` (function) `modules/lazy_rbac.py:660` `def check_cli_permission(username, permission)` -- Check if a CLI user has the given permission.
- `get_user_role` (function) `modules/lazy_rbac.py:672` `def get_user_role(username)`
- `generate_mfa_qr_url` (function) `modules/lazy_rbac.py:680` `def generate_mfa_qr_url(secret, username)` -- Generate a QR code data URI for MFA setup (local, no external API).
- `generate_qr_svg` (function) `modules/lazy_rbac.py:689` `def generate_qr_svg(data)` -- Generate an SVG QR code image from text data.
- `gf_mul` (function) `modules/lazy_rbac.py:927` `def gf_mul(a, b)`

## modules/lazy_reaper.py
Depends on: `modules/lazy_loop.py`
Imported by: `modules/lazy_loop.py`, `tests/test_lazy_reaper.py`
- `reap` (function) `modules/lazy_reaper.py:30` `def reap(store, log_path, now, stale_seconds)` -- Expire tasks whose heartbeat is provably stale.

## modules/lazy_roles.py
Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`
- `list_roles` (function) `modules/lazy_roles.py:100` `def list_roles()` -- Return every Lazy role descriptor.
- `role_prompt` (function) `modules/lazy_roles.py:109` `def role_prompt(role, goal, context)` -- Build the system prompt for one role.
- `roles_for_phase` (function) `modules/lazy_roles.py:134` `def roles_for_phase(phase)` -- Return role names serving one kill-chain phase.
- `conformance` (function) `modules/lazy_roles.py:154` `def conformance(role)` -- Probe every pool member with role prompts, like provider conformance.

## modules/lazy_runner.py
Depends on: `cli/lazy_monitor.py`, `core/autonomous.py`, `core/config.py`, `core/hardening.py`, `core/terminal_guard.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/custom_tools.py`, `modules/jsonl_tail.py`, `modules/lazy_engine.py`, `modules/lazy_exposure.py`, `modules/lazy_loop.py`, `modules/lazy_sandbox.py`, `modules/loop_guardrails.py`, `modules/loop_progress.py`, `utils.py`
Imported by: `cli/commands/lazyops.py`, `cli/commands/mcp_bridge.py`, `cli/commands/retry_ops.py`, `cli/lazy_monitor.py`, `modules/tools/loop_smoke.py`, `skills/mcp_tools/auto_loop.py`, `tests/test_lazy_runner.py`, `tests/test_loop_budget.py`, `tests/test_loop_multi_target.py`, `tests/test_loop_nmap_guard.py`, `tests/test_loop_target_authority.py`, `tests/test_orchestrator_yaml.py`
- `ThreadStdoutRouter.__init__` (method) `modules/lazy_runner.py:55` `def __init__(self, main_stream, spool)` -- Bind the real stream and the worker spool queue.
- `ThreadStdoutRouter.write` (method) `modules/lazy_runner.py:61` `def write(self, data)` -- Route main-thread writes to the terminal, worker writes to spool.
- `ThreadStdoutRouter.flush` (method) `modules/lazy_runner.py:72` `def flush(self)` -- Flush the real stream; the spool needs no flushing.
- `ThreadStdoutRouter.encoding` (method) `modules/lazy_runner.py:80` `def encoding(self)` -- Report the real stream encoding.
- `ThreadStdoutRouter.isatty` (method) `modules/lazy_runner.py:84` `def isatty(self)` -- Report whether the real stream is a terminal.
- `LoopRunConfig.clamped` (method) `modules/lazy_runner.py:120` `def clamped(self)` -- Clamp numeric knobs to the supported operating range.
- `parse_loop_line` (function) `modules/lazy_runner.py:172` `def parse_loop_line(line)` -- Parse one loop command line into a :class:`LoopRunConfig`.
- `resolve_loop_defaults` (function) `modules/lazy_runner.py:302` `def resolve_loop_defaults(config)` -- Fill unset rounds and workers from the selected orchestrator profile.
- `build_executor` (function) `modules/lazy_runner.py:338` `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` -- Build the worker executor: shell verbs, custom tools, safe bash.
- `report_result` (function) `modules/lazy_runner.py:521` `def report_result(result)` -- Print the final outcome of one loop run.
- `stream` (function) `modules/lazy_runner.py:657` `def stream(text)`
- `bind_target_authority` (function) `modules/lazy_runner.py:954` `def bind_target_authority(shell, targets)` -- Make the run's target(s) authoritative over payload rhost and scope.
- `load_targets_file` (function) `modules/lazy_runner.py:1014` `def load_targets_file(path)` -- Read and validate one target per line from a scope file.
- `run_loop` (function) `modules/lazy_runner.py:1069` `def run_loop(shell, params, config)` -- Execute one complete loop run and return its summary.

## modules/lazy_sandbox.py
Depends on: `core/config.py`
Imported by: `cli/commands/lazyops.py`, `modules/lazy_runner.py`
- `image_name` (function) `modules/lazy_sandbox.py:52` `def image_name(configured)` -- Resolve the sandbox image name.
- `container_name` (function) `modules/lazy_sandbox.py:67` `def container_name(task_id)` -- Return the deterministic container name for one task.
- `docker_available` (function) `modules/lazy_sandbox.py:73` `def docker_available()` -- Return True when the docker CLI is on PATH.
- `image_available` (function) `modules/lazy_sandbox.py:78` `def image_available(image)` -- Return True when the sandbox image exists locally.
- `container_running` (function) `modules/lazy_sandbox.py:94` `def container_running(task_id)` -- Return the container name when it is up, else empty string.
- `ensure_container` (function) `modules/lazy_sandbox.py:112` `def ensure_container(task_id, image)` -- Start the per-task container when needed, return its name or error.
- `exec_command` (function) `modules/lazy_sandbox.py:180` `def exec_command(task_id, command, timeout_sec, image)` -- Run one Lazy shell verb inside the task container.
- `remove_container` (function) `modules/lazy_sandbox.py:214` `def remove_container(task_id)` -- Stop and remove the task container.
- `status` (function) `modules/lazy_sandbox.py:223` `def status(task_id)` -- Describe sandbox readiness and containers.
- `executor_for` (function) `modules/lazy_sandbox.py:251` `def executor_for(task_id, image)` -- Build a worker executor routing shell verbs into the sandbox.

## modules/lazy_scope.py
Imported by: `modules/chain_distill.py`
- `_ResolveCache.get` (method) `modules/lazy_scope.py:70` `def get(self, name, now)` -- Return cached addresses when fresh.
- `_ResolveCache.put` (method) `modules/lazy_scope.py:89` `def put(self, name, values, now)` -- Store resolution results.
- `is_lab_address` (function) `modules/lazy_scope.py:105` `def is_lab_address(address)` -- Classify one address as lab-local.
- `extract_hosts` (function) `modules/lazy_scope.py:130` `def extract_hosts(text)` -- Pull IP literals and plausible hostnames out of free text.
- `resolve_addresses` (function) `modules/lazy_scope.py:164` `def resolve_addresses(name, now)` -- Resolve a hostname to all of its addresses.
- `read_scope_file` (function) `modules/lazy_scope.py:209` `def read_scope_file(name, sessions_dir)` -- Load operator entries from a scope list file.
- `read_allowlist` (function) `modules/lazy_scope.py:231` `def read_allowlist(sessions_dir)` -- Load operator-approved extra lab hosts.
- `read_denylist` (function) `modules/lazy_scope.py:243` `def read_denylist(sessions_dir)` -- Load explicitly denied hosts and networks.
- `scope_verdict` (function) `modules/lazy_scope.py:255` `def scope_verdict(target, resolver, allowlist, denylist)` -- Decide whether one target is inside the default lab scope.
- `command_scope_verdict` (function) `modules/lazy_scope.py:351` `def command_scope_verdict(command, resolver, allowlist, denylist)` -- Check every host mentioned in a command line.

## modules/lazy_search.py
Depends on: `modules/db.py`
Imported by: `skills/mcp_tools/lazysearch.py`
- `parse` (function) `modules/lazy_search.py:94` `def parse(query)` -- Parse the grammar tokens.
- `execute` (function) `modules/lazy_search.py:132` `def execute(db, query, workspace_name, db_path)` -- Run a parsed query against the engagement database.

## modules/lazy_sentinel.py
Depends on: `modules/lazy_feedmatch.py`
- `ingest_spool` (function) `modules/lazy_sentinel.py:45` `def ingest_spool(path)` -- Parse a sentinel spool artefact back into queryable sightings.
- `validate_ranges` (function) `modules/lazy_sentinel.py:123` `def validate_ranges(ranges)` -- Reject unbounded or non-private targets for the sentinel blob.
- `provision_blob` (function) `modules/lazy_sentinel.py:152` `def provision_blob(ranges, spool_path, spool_dir)` -- Build the copy-paste sentinel sweep blob.
- `dispatch_line` (function) `modules/lazy_sentinel.py:203` `def dispatch_line(client_id, blob)` -- Render the ``c2_exec`` line that runs the blob through one beacon.
- `save_sightings` (function) `modules/lazy_sentinel.py:252` `def save_sightings(sightings, path)` -- Persist parsed sightings for the report/check surfaces.
- `load_sightings` (function) `modules/lazy_sentinel.py:282` `def load_sightings(path)` -- Reload a previous ``save_sightings`` artefact.

## modules/lazy_skill_mirror.py
Imported by: `cli/commands/lazyops.py`
- `available_skills` (function) `modules/lazy_skill_mirror.py:67` `def available_skills()` -- Return repo skill names that ship a SKILL.md.
- `mirror_skill` (function) `modules/lazy_skill_mirror.py:78` `def mirror_skill(name)` -- Write the Hermes mirror of one skill.
- `mirror_all` (function) `modules/lazy_skill_mirror.py:106` `def mirror_all()` -- Mirror every repo skill; return per-skill summaries.
- `register_external_dirs` (function) `modules/lazy_skill_mirror.py:117` `def register_external_dirs()` -- Register the repo skills tree in the hermes config.

## modules/lazy_skills.py
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`, `modules/loop/worker_agentic.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_runner.py`
- `list_skills` (function) `modules/lazy_skills.py:85` `def list_skills()` -- Return every parsed skill sorted by name.
- `get_skill` (function) `modules/lazy_skills.py:91` `def get_skill(name)` -- Find one skill by exact or case-insensitive name.
- `match_skills` (function) `modules/lazy_skills.py:102` `def match_skills(text, limit)` -- Rank skills whose keywords appear in the text, best first.
- `skills_context` (function) `modules/lazy_skills.py:118` `def skills_context(text, explicit, auto, budget)` -- Render pinned plus auto-matched skills as one prompt section.

## modules/lazy_summarizer.py
- `should_compact` (function) `modules/lazy_summarizer.py:35` `def should_compact(used_chars, budget_chars)` -- Return True when context exceeds the usable budget.
- `summarize_chain` (function) `modules/lazy_summarizer.py:50` `def summarize_chain(records, budget_chars, complete)` -- Bound a record chain to budget, digesting the oldest pairs.

## modules/lazy_surface_diff.py
Depends on: `modules/world_model.py`
- `snapshot_host` (function) `modules/lazy_surface_diff.py:52` `def snapshot_host(host)` -- Canonical snapshot of one host row.
- `fingerprint` (function) `modules/lazy_surface_diff.py:79` `def fingerprint(state)` -- Hash of the canonical snapshot; os text normalised case-insensitively.
- `diff_hosts` (function) `modules/lazy_surface_diff.py:93` `def diff_hosts(before, after)` -- Pure diff of two host snapshot maps.
- `current_snapshots` (function) `modules/lazy_surface_diff.py:160` `def current_snapshots(world)` -- Snapshot every host of the current world model view.
- `refresh` (function) `modules/lazy_surface_diff.py:186` `def refresh(world, sessions_dir)` -- Diff the current surface against the stored snapshot and persist.
- `last_diff` (function) `modules/lazy_surface_diff.py:234` `def last_diff(sessions_dir)` -- Read the last stored diff without recomputing.
- `changed_hosts` (function) `modules/lazy_surface_diff.py:253` `def changed_hosts(limit, sessions_dir)` -- Distinct hosts touched by the last diff, most-recent first.

## modules/lazy_timeline.py
Depends on: `modules/world_model.py`
Imported by: `lazyown.py`, `modules/lazy_loop.py`, `tests/test_lazy_intel_wiring.py`
- `resolve_hostnames` (function) `modules/lazy_timeline.py:36` `def resolve_hostnames(names, resolver)` -- Resolve candidate hostnames for the snapshot DNS record.
- `record` (function) `modules/lazy_timeline.py:66` `def record(state_path, snaps_dir, keep, dns)` -- Snapshot the current world model (internally, never raises).
- `record_quiet` (function) `modules/lazy_timeline.py:111` `def record_quiet(state_path, snaps_dir, keep, dns)` -- Snapshot for the autonomous loop: same as record(), never raises.
- `find_snapshots` (function) `modules/lazy_timeline.py:135` `def find_snapshots(snaps_dir)` -- List snapshot files oldest first.
- `diff` (function) `modules/lazy_timeline.py:151` `def diff(_old, _new)` -- Diff two world-model snapshots.
- `show` (function) `modules/lazy_timeline.py:180` `def show(snaps_dir, last)` -- Summarize the newest snapshots.

## modules/lazy_triage.py
Imported by: `tests/test_lazy_triage.py`
- `rank` (function) `modules/lazy_triage.py:42` `def rank(verdict)` -- Return the comparison rank of a triage verdict.
- `hard_evidence` (function) `modules/lazy_triage.py:47` `def hard_evidence(kind, facts)` -- Classify one finding from its deterministic evidence floor.
- `apply_rules` (function) `modules/lazy_triage.py:80` `def apply_rules(verdict, kind, facts)` -- Constrain a (model or operator) verdict by the evidence floor.
- `signature_for` (function) `modules/lazy_triage.py:108` `def signature_for(kind, fields)` -- Return the evidence signature of one classification request.
- `SignatureStore.__init__` (method) `modules/lazy_triage.py:138` `def __init__(self, sessions_dir, ttl)` -- Bind the store file under sessions/lazy.
- `SignatureStore.fresh_signature` (method) `modules/lazy_triage.py:144` `def fresh_signature(self, signature, now)` -- Return the previous signature row when it is inside the TTL window.
- `SignatureStore.reset` (method) `modules/lazy_triage.py:162` `def reset(self)` -- Drop every signature row.

## modules/lazy_verify.py
Depends on: `core/process.py`
- `plan_checks` (function) `modules/lazy_verify.py:84` `def plan_checks(finding_text, poc)` -- Build the read-only check list for one finding.
- `run_check` (function) `modules/lazy_verify.py:143` `def run_check(check, executor)` -- Run one read-only check and classify its result.
- `verdict_from_checks` (function) `modules/lazy_verify.py:214` `def verdict_from_checks(checks_results)` -- Deterministic verdict from a list of check results.
- `verify_finding` (function) `modules/lazy_verify.py:232` `def verify_finding(finding_text, poc, executor)` -- Plan, run and judge the read-only checks for one finding.

## modules/lazy_world_diff.py
Depends on: `modules/world_model.py`
Imported by: `modules/intel_fusion.py`, `modules/lazy_hostscore.py`, `modules/lazy_loop.py`, `modules/sinks/world_diff.py`, `tests/test_lazy_world_diff.py`, `tests/test_mediation.py`, `tests/test_world_diff_retest.py`
- `host_snapshot` (function) `modules/lazy_world_diff.py:78` `def host_snapshot(world, ip)` -- Read one host out of a world-model dict as a canonical snapshot.
- `snapshot_fingerprint` (function) `modules/lazy_world_diff.py:119` `def snapshot_fingerprint(state)` -- Hash one snapshot canonically; key order never matters.
- `diff_snapshots` (function) `modules/lazy_world_diff.py:131` `def diff_snapshots(before, after)` -- Deterministic change list between two host snapshots.
- `record_changes` (function) `modules/lazy_world_diff.py:200` `def record_changes(changes, sessions_dir, now)` -- Append changes to the campaign change log, deduped and bounded.
- `recent_changes` (function) `modules/lazy_world_diff.py:260` `def recent_changes(sessions_dir, days, host)` -- Change rows newest-first within the window, optionally per host.
- `prune_changes` (function) `modules/lazy_world_diff.py:270` `def prune_changes(sessions_dir, keep_days)` -- Drop change rows older than ``keep_days``; returns how many.
- `load_host_snapshots` (function) `modules/lazy_world_diff.py:290` `def load_host_snapshots(sessions_dir)` -- Stored per-host snapshots keyed by ip.
- `save_host_snapshots` (function) `modules/lazy_world_diff.py:301` `def save_host_snapshots(snapshots, sessions_dir)` -- Persist per-host snapshots atomically-enough (best effort).
- `campaign_snapshots` (function) `modules/lazy_world_diff.py:312` `def campaign_snapshots(sessions_dir)` -- Snapshot every world-model host, then diff against stored ones.
- `ghost_endpoints` (function) `modules/lazy_world_diff.py:366` `def ghost_endpoints(snapshot, limit)` -- Web endpoints (ip, port, scheme) a snapshot last had open.
- `name_resolves` (function) `modules/lazy_world_diff.py:395` `def name_resolves(host, resolver)` -- Whether a hostname still resolves (injectable for tests).
- `load_ghosts` (function) `modules/lazy_world_diff.py:435` `def load_ghosts(sessions_dir)` -- The ghost store ``{"hosts": {...}}`` tolerant of corruption.
- `ghost_state_apply` (function) `modules/lazy_world_diff.py:447` `def ghost_state_apply(host, answers, sessions_dir, now)` -- Record one ghost observation and return the host's ghost record.
- `find_ghost_hosts` (function) `modules/lazy_world_diff.py:489` `def find_ghost_hosts(candidates, snapshots, checker, resolver, cap)` -- Which candidate hostnames are ghosts: unresolvable yet answering.
- `snapshot_engagement` (function) `modules/lazy_world_diff.py:528` `def snapshot_engagement(sessions_dir, now, world)` -- Append one daily campaign snapshot when the cooldown allows.

## modules/lazyatack.sh
- `mostrar_ayuda` (function) `modules/lazyatack.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyatack.sh:33` -- Función para validar una dirección IP
- `validar_url` (function) `modules/lazyatack.sh:49` -- Función para validar URL
- `descargar_seclists` (function) `modules/lazyatack.sh:107` -- Función para descargar y extraer SecLists
- `escanear_puertos` (function) `modules/lazyatack.sh:115` -- Función para ejecutar escaneo de puertos con nmap
- `escanear_puertos_especificos` (function) `modules/lazyatack.sh:121` -- Función para escanear puertos específicos
- `enumerar_http` (function) `modules/lazyatack.sh:127` -- Función para enumerar servicios HTTP
- `iniciar_servidor_http` (function) `modules/lazyatack.sh:133` -- Función para iniciar servidor HTTP con Python
- `configurar_netcat` (function) `modules/lazyatack.sh:139` -- Función para configurar netcat
- `enviar_archivo_netcat` (function) `modules/lazyatack.sh:145` -- Función para enviar archivo mediante bash a netcat
- `verificar_conectividad` (function) `modules/lazyatack.sh:151` -- Función para verificar conectividad con ping y tcpdump
- `verificar_curl` (function) `modules/lazyatack.sh:158` -- Función para verificar conectividad con curl
- `configurar_shell_reversa` (function) `modules/lazyatack.sh:165` -- Función para configurar una shell reversa
- `escuchar_shell` (function) `modules/lazyatack.sh:171` -- Función para escuchar shell con netcat
- `monitorear_procesos` (function) `modules/lazyatack.sh:177` -- Función para monitorear procesos
- `ejecutar_wfuzz` (function) `modules/lazyatack.sh:188` -- Función para ejecutar wfuzz
- `comprobar_sudo` (function) `modules/lazyatack.sh:194` -- Función para comprobar permisos sudo
- `explotar_lfi` (function) `modules/lazyatack.sh:200` -- Función para explotar LFI
- `configurar_tty` (function) `modules/lazyatack.sh:206` -- Función para configurar TTY
- `eliminar_archivos` (function) `modules/lazyatack.sh:217` -- Función para eliminar archivos de forma segura
- `obtener_root_shell` (function) `modules/lazyatack.sh:223` -- Función para obtener root shell mediante Docker
- `enumerar_suid` (function) `modules/lazyatack.sh:230` -- Función para enumerar archivos con SUID
- `listar_timers` (function) `modules/lazyatack.sh:236` -- Función para listar timers de systemd
- `comprobar_rutas` (function) `modules/lazyatack.sh:242` -- Función para comprobar rutas de comandos
- `abusar_tar` (function) `modules/lazyatack.sh:248` -- Función para abusar de tar
- `enumerar_puertos` (function) `modules/lazyatack.sh:254` -- Función para enumerar puertos abiertos
- `eliminar_contenedores_docker` (function) `modules/lazyatack.sh:260` -- Función para eliminar contenedores Docker
- `escanear_red` (function) `modules/lazyatack.sh:266` -- Función para escanear red
- `menu_servidor` (function) `modules/lazyatack.sh:272` -- Función para mostrar menú en modo servidor
- `menu_cliente` (function) `modules/lazyatack.sh:307` -- Función para mostrar menú en modo cliente

## modules/lazycloud.py
Imported by: `cli/commands/cloud.py`
- `CloudMetadataHarvester.__init__` (method) `modules/lazycloud.py:111` `def __init__(self, timeout)`
- `CloudMetadataHarvester.session` (method) `modules/lazycloud.py:116` `def session(self)`
- `CloudMetadataHarvester.harvest_aws` (method) `modules/lazycloud.py:139` `def harvest_aws(self)` -- Harvest AWS EC2 instance metadata (IMDSv2 capable).
- `CloudMetadataHarvester.harvest_azure` (method) `modules/lazycloud.py:184` `def harvest_azure(self)` -- Harvest Azure instance metadata.
- `CloudMetadataHarvester.harvest_gcp` (method) `modules/lazycloud.py:208` `def harvest_gcp(self)` -- Harvest GCP instance metadata.
- `CloudMetadataHarvester.harvest_all` (method) `modules/lazycloud.py:231` `def harvest_all(self)` -- Try all three cloud providers sequentially.
- `CloudBucketEnumerator.__init__` (method) `modules/lazycloud.py:251` `def __init__(self, timeout)`
- `CloudBucketEnumerator.session` (method) `modules/lazycloud.py:256` `def session(self)`
- `CloudBucketEnumerator.enumerate_s3` (method) `modules/lazycloud.py:278` `def enumerate_s3(self, prefix, buckets)` -- Enumerate S3 buckets derived from a prefix.
- `CloudBucketEnumerator.enumerate_azure_storage` (method) `modules/lazycloud.py:303` `def enumerate_azure_storage(self, prefix, accounts)` -- Enumerate Azure Blob Storage accounts.
- `CloudBucketEnumerator.enumerate_gcp_storage` (method) `modules/lazycloud.py:321` `def enumerate_gcp_storage(self, prefix, buckets)` -- Enumerate GCP Storage buckets.
- `CloudIAMEnumerator.enumerate_aws_iam` (method) `modules/lazycloud.py:345` `def enumerate_aws_iam(self, access_key, secret_key, session_token)` -- Enumerate AWS IAM (requires valid credentials).
- `CloudScanner.__init__` (method) `modules/lazycloud.py:393` `def __init__(self, target_domain, timeout)`
- `CloudScanner.full_scan` (method) `modules/lazycloud.py:400` `def full_scan(self, target_prefix, sessions_dir)` -- Perform a comprehensive cloud security scan.
- `CloudScanner.quick_metadata` (method) `modules/lazycloud.py:456` `def quick_metadata(self)` -- Fast metadata-only harvest (no bucket enumeration).
- `CloudScanner.quick_buckets` (method) `modules/lazycloud.py:460` `def quick_buckets(self, prefix)` -- Fast S3-only bucket check.

## modules/lazycurl.sh
- `ctrl_c` (function) `modules/lazycurl.sh:23`
- `show_help` (function) `modules/lazycurl.sh:29` -- Función para mostrar la ayuda
- `execute_curl` (function) `modules/lazycurl.sh:52` -- Función para ejecutar el comando CURL

## modules/lazydorks.py
- `categories` (function) `modules/lazydorks.py:96` `def categories()` -- Return every supported dork category.
- `queries` (function) `modules/lazydorks.py:101` `def queries(category, domain, org)` -- Render the dork queries for one category against one target.
- `all_queries` (function) `modules/lazydorks.py:123` `def all_queries(domain, org)` -- Render the full grammar for one target.
- `write_report` (function) `modules/lazydorks.py:137` `def write_report(path, domain, org)` -- Persist the rendered dorks as a markdown playbook.

## modules/lazyencoder_decoder.py
Imported by: `contrib/legacy/lazycreate_webshell.py`, `contrib/legacy/lazylogpoisoning.py`, `contrib/legacy/lazyreversentlmv2.py`, `modules/test_lazyencoder_decoder.py`, `utils.py`
- `base64_encode` (function) `modules/lazyencoder_decoder.py:4` `def base64_encode(data)`
- `base64_decode` (function) `modules/lazyencoder_decoder.py:8` `def base64_decode(data)`
- `caesar_cipher` (function) `modules/lazyencoder_decoder.py:13` `def caesar_cipher(text, shift)`
- `caesar_decipher` (function) `modules/lazyencoder_decoder.py:27` `def caesar_decipher(text, shift)`
- `key_substitution` (function) `modules/lazyencoder_decoder.py:31` `def key_substitution(text, key)`
- `key_substitution_reverse` (function) `modules/lazyencoder_decoder.py:47` `def key_substitution_reverse(text, key)`
- `encode` (function) `modules/lazyencoder_decoder.py:63` `def encode(data, shift, key)`
- `encode_string` (function) `modules/lazyencoder_decoder.py:75` `def encode_string(data, shift, key)`
- `decode` (function) `modules/lazyencoder_decoder.py:82` `def decode(data, shift, key)`
- `decode_string` (function) `modules/lazyencoder_decoder.py:94` `def decode_string(data, shift, key)`

## modules/lazyevilwimrm.sh
- `execute_evil_winrm` (function) `modules/lazyevilwimrm.sh:14` -- Función para ejecutar evil-winrm y verificar la salida

## modules/lazyk8s.py
Imported by: `cli/commands/containers.py`
- `DockerEnumerator.__init__` (method) `modules/lazyk8s.py:44` `def __init__(self, socket_path)`
- `DockerEnumerator.is_socket_accessible` (method) `modules/lazyk8s.py:47` `def is_socket_accessible(self)` -- Check if the Docker socket is readable/writable.
- `DockerEnumerator.list_containers` (method) `modules/lazyk8s.py:70` `def list_containers(self)` -- List all containers with extended information.
- `DockerEnumerator.list_images` (method) `modules/lazyk8s.py:94` `def list_images(self)` -- List all Docker images.
- `DockerEnumerator.inspect_container` (method) `modules/lazyk8s.py:118` `def inspect_container(self, container_id)` -- Get detailed configuration of a container (privileged, mounts, capabilities).
- `DockerEnumerator.check_privileged_containers` (method) `modules/lazyk8s.py:137` `def check_privileged_containers(self)` -- Find containers running with --privileged flag.
- `DockerEnumerator.check_sensitive_mounts` (method) `modules/lazyk8s.py:162` `def check_sensitive_mounts(self)` -- Find containers with sensitive host path mounts.
- `DockerEnumerator.check_docker_socket_mount` (method) `modules/lazyk8s.py:196` `def check_docker_socket_mount(self)` -- Find containers with the Docker socket mounted (escape vector).
- `DockerEnumerator.check_capabilities` (method) `modules/lazyk8s.py:217` `def check_capabilities(self)` -- Find containers with dangerous Linux capabilities.
- `DockerEnumerator.full_check` (method) `modules/lazyk8s.py:250` `def full_check(self)` -- Execute all Docker security checks and return aggregated results.
- `K8sEnumerator.__init__` (method) `modules/lazyk8s.py:267` `def __init__(self, kubeconfig, token, api_server)`
- `K8sEnumerator.list_pods` (method) `modules/lazyk8s.py:366` `def list_pods(self, namespace)` -- List pods in all namespaces or a specific namespace.
- `K8sEnumerator.list_namespaces` (method) `modules/lazyk8s.py:390` `def list_namespaces(self)` -- List all namespaces.
- `K8sEnumerator.list_secrets` (method) `modules/lazyk8s.py:410` `def list_secrets(self, namespace)` -- List secrets (without decoding values by default).
- `K8sEnumerator.list_service_accounts` (method) `modules/lazyk8s.py:462` `def list_service_accounts(self, namespace)` -- List service accounts and their attached roles.
- `K8sEnumerator.check_rbac` (method) `modules/lazyk8s.py:498` `def check_rbac(self)` -- Check current user's RBAC permissions.
- `K8sEnumerator.check_pod_escape_vectors` (method) `modules/lazyk8s.py:530` `def check_pod_escape_vectors(self)` -- Check for pod escape vectors in the current pod.
- `K8sEnumerator.full_check` (method) `modules/lazyk8s.py:582` `def full_check(self, sessions_dir)` -- Execute all Kubernetes security checks.
- `ContainerEscapeTechniques.detect_current_environment` (method) `modules/lazyk8s.py:684` `def detect_current_environment()` -- Detect if running inside a container and identify escape opportunities.
- `ContainerRuntimeDetector.detect_runtime` (method) `modules/lazyk8s.py:803` `def detect_runtime()` -- Detect container runtime from multiple indicators.
- `ContainerRuntimeDetector.detect_mounts` (method) `modules/lazyk8s.py:874` `def detect_mounts()` -- Detect dangerous mounts in the current container.
- `ContainerRuntimeDetector.detect_dangerous_capabilities` (method) `modules/lazyk8s.py:921` `def detect_dangerous_capabilities()` -- Detect dangerous Linux capabilities in the current container.
- `ContainerRuntimeDetector.auto_detect_all` (method) `modules/lazyk8s.py:992` `def auto_detect_all()` -- Run comprehensive container escape auto-detection.

## modules/lazylynis.sh
- `check_sudo` (function) `modules/lazylynis.sh:32` -- Función para verificar y relanzar con sudo si es necesario

## modules/lazymasscan.sh
- `ctrl_c` (function) `modules/lazymasscan.sh:20`
- `extract_ports_info` (function) `modules/lazymasscan.sh:74`
- `run_masscan_script` (function) `modules/lazymasscan.sh:94`
- `print_row` (function) `modules/lazymasscan.sh:117`

## modules/lazynmap.sh
- `cleanup` (function) `modules/lazynmap.sh:29`
- `ctrl_c` (function) `modules/lazynmap.sh:38`
- `fix_sessions_owner` (function) `modules/lazynmap.sh:74` -- Best-effort ownership fixup: scans run under sudo leave root-owned files behind, and only root can chown those.
- `nmaptest` (function) `modules/lazynmap.sh:129`
- `discover_network` (function) `modules/lazynmap.sh:149`
- `extract_ports_info` (function) `modules/lazynmap.sh:818`
- `run_nmap_script` (function) `modules/lazynmap.sh:844`
- `print_row` (function) `modules/lazynmap.sh:877`

## modules/lazyown_bprfuzzer.py
Depends on: `modules/backdoor/server.c`, `modules/security_sanitizers.py`
- `load_headers_from_file` (function) `modules/lazyown_bprfuzzer.py:93` `def load_headers_from_file(file_path)`
- `load_data_from_file` (function) `modules/lazyown_bprfuzzer.py:99` `def load_data_from_file(file_path)`
- `signal_handler` (function) `modules/lazyown_bprfuzzer.py:105` `def signal_handler(sig, frame)`
- `ProxyHandler.do_GET` (method) `modules/lazyown_bprfuzzer.py:115` `def do_GET(self)`
- `ProxyHandler.do_POST` (method) `modules/lazyown_bprfuzzer.py:118` `def do_POST(self)`
- `run_proxy` (function) `modules/lazyown_bprfuzzer.py:162` `def run_proxy(port)`
- `edit_file_with_nano` (function) `modules/lazyown_bprfuzzer.py:169` `def edit_file_with_nano(content)`
- `send_request` (function) `modules/lazyown_bprfuzzer.py:179` `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)` -- Envía una solicitud HTTP y devuelve la respuesta.
- `repeater` (function) `modules/lazyown_bprfuzzer.py:203` `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)` -- Funcionalidad de Repeater que permite enviar solicitudes múltiples veces con posibilidad de modificación.
- `lazyfuzz` (function) `modules/lazyown_bprfuzzer.py:233` `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)` -- Funcionalidad de fuzzing que reemplaza LAZYFUZZ con palabras de una wordlist.
- `parse_arguments` (function) `modules/lazyown_bprfuzzer.py:278` `def parse_arguments()` -- Parsear los argumentos de la línea de comandos.
- `main` (function) `modules/lazyown_bprfuzzer.py:302` `def main()`

## modules/lazyown_bridge.py
Depends on: `modules/killchain.py`
Imported by: `modules/unified_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/mcp_tools/bridge_suggest.py`, `skills/mcp_tools/discover_commands.py`, `skills/mcp_tools/phase_guide.py`, `skills/mcp_tools/session_init.py`, `tests/test_bridge_catalog_filtered.py`, `tests/test_core_modules.py`, `tests/test_exploitgym_gym.py`
- `CatalogEntry.build_command` (method) `modules/lazyown_bridge.py:63` `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)` -- Return 'command [args]' with known values substituted.
- `CatalogEntry.matches_service` (method) `modules/lazyown_bridge.py:94` `def matches_service(self, services)`
- `CatalogEntry.matches_os` (method) `modules/lazyown_bridge.py:104` `def matches_os(self, os_hint)`
- `CommandCatalog.__init__` (method) `modules/lazyown_bridge.py:118` `def __init__(self)`
- `CommandCatalog.by_phase` (method) `modules/lazyown_bridge.py:3946` `def by_phase(self, phase)`
- `CommandCatalog.by_mitre` (method) `modules/lazyown_bridge.py:3952` `def by_mitre(self, technique_id)`
- `CommandCatalog.by_service` (method) `modules/lazyown_bridge.py:3956` `def by_service(self, service_name)`
- `CommandCatalog.by_tag` (method) `modules/lazyown_bridge.py:3960` `def by_tag(self, tag)`
- `CommandCatalog.by_os` (method) `modules/lazyown_bridge.py:3963` `def by_os(self, os_hint)`
- `CommandCatalog.all_phases` (method) `modules/lazyown_bridge.py:3966` `def all_phases(self)`
- `CommandCatalog.get` (method) `modules/lazyown_bridge.py:3969` `def get(self, command)`
- `CommandCatalog.count` (method) `modules/lazyown_bridge.py:3975` `def count(self)`
- `AbstractSelector.select` (method) `modules/lazyown_bridge.py:3986` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `ServiceAwareSelector.select` (method) `modules/lazyown_bridge.py:4005` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `MitreAlignedSelector.__init__` (method) `modules/lazyown_bridge.py:4045` `def __init__(self, technique_id)`
- `MitreAlignedSelector.select` (method) `modules/lazyown_bridge.py:4049` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `TagSelector.__init__` (method) `modules/lazyown_bridge.py:4074` `def __init__(self, tag)`
- `TagSelector.select` (method) `modules/lazyown_bridge.py:4078` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `ContextEnricher.enrich` (method) `modules/lazyown_bridge.py:4106` `def enrich(self, entry, target, world_snapshot)`
- `PhaseMapper.canonical_kill_chain_order` (method) `modules/lazyown_bridge.py:4204` `def canonical_kill_chain_order()` -- Return the canonical 8-phase order from KillChain (single source of truth).
- `PhaseMapper.to_bridge_phase` (method) `modules/lazyown_bridge.py:4210` `def to_bridge_phase(self, wm_phase)`
- `PhaseMapper.kill_chain_order` (method) `modules/lazyown_bridge.py:4223` `def kill_chain_order(self)` -- Ordered list of bridge phases following the kill chain.
- `BridgeDispatcher.__init__` (method) `modules/lazyown_bridge.py:4239` `def __init__(self, catalog, selector, enricher, phase_mapper)`
- `BridgeDispatcher.suggest` (method) `modules/lazyown_bridge.py:4251` `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)` -- Return (command_string, entry) or None.
- `BridgeDispatcher.suggest_sequence` (method) `modules/lazyown_bridge.py:4296` `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)` -- Return up to `limit` non-excluded suggestions for the phase.
- `BridgeDispatcher.suggest_for_wm_phase` (method) `modules/lazyown_bridge.py:4325` `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)`
- `BridgeDispatcher.list_phase` (method) `modules/lazyown_bridge.py:4343` `def list_phase(self, phase)`
- `BridgeDispatcher.all_phases` (method) `modules/lazyown_bridge.py:4347` `def all_phases(self)`
- `BridgeDispatcher.catalog_summary` (method) `modules/lazyown_bridge.py:4350` `def catalog_summary(self)`
- `BridgeDispatcher.catalog_summary_filtered` (method) `modules/lazyown_bridge.py:4358` `def catalog_summary_filtered(self, phase, os_hint)` -- Return a kill-chain summary restricted to a phase and target OS.
- `BridgeDispatcher.catalog_count` (method) `modules/lazyown_bridge.py:4395` `def catalog_count(self)`
- `BridgeDispatcher.phase_kill_chain` (method) `modules/lazyown_bridge.py:4398` `def phase_kill_chain(self)`
- `get_dispatcher` (function) `modules/lazyown_bridge.py:4409` `def get_dispatcher()`


Next: [API_p16.md](API_p16.md)
