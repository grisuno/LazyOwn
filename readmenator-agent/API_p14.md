# API (page 14 of 24)
Previous: [API_p13.md](API_p13.md)

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

## modules/lazy_roles.py
Depends on: `modules/lazy_engine.py`, `modules/lazy_loop.py`
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`
- `list_roles` (function) `modules/lazy_roles.py:100` `def list_roles()` -- Return every Lazy role descriptor.
- `role_prompt` (function) `modules/lazy_roles.py:109` `def role_prompt(role, goal, context)` -- Build the system prompt for one role.
- `roles_for_phase` (function) `modules/lazy_roles.py:134` `def roles_for_phase(phase)` -- Return role names serving one kill-chain phase.
- `conformance` (function) `modules/lazy_roles.py:154` `def conformance(role)` -- Probe every pool member with role prompts, like provider conformance.

## modules/lazy_runner.py
Depends on: `cli/lazy_monitor.py`, `core/autonomous.py`, `core/hardening.py`, `core/terminal_guard.py`, `modules/__init__.py`, `modules/auto_registry.py`, `modules/custom_tools.py`, `modules/jsonl_tail.py`, `modules/lazy_engine.py`, `modules/lazy_loop.py`, `modules/lazy_sandbox.py`, `modules/loop_guardrails.py`, `modules/loop_progress.py`, `utils.py`
Imported by: `cli/commands/lazyops.py`, `cli/commands/mcp_bridge.py`, `cli/commands/retry_ops.py`, `cli/lazy_monitor.py`, `modules/tools/loop_smoke.py`, `tests/test_lazy_runner.py`, `tests/test_loop_budget.py`, `tests/test_loop_multi_target.py`, `tests/test_loop_nmap_guard.py`, `tests/test_orchestrator_yaml.py`
- `ThreadStdoutRouter.__init__` (method) `modules/lazy_runner.py:55` `def __init__(self, main_stream, spool)` -- Bind the real stream and the worker spool queue.
- `ThreadStdoutRouter.write` (method) `modules/lazy_runner.py:61` `def write(self, data)` -- Route main-thread writes to the terminal, worker writes to spool.
- `ThreadStdoutRouter.flush` (method) `modules/lazy_runner.py:72` `def flush(self)` -- Flush the real stream; the spool needs no flushing.
- `ThreadStdoutRouter.encoding` (method) `modules/lazy_runner.py:80` `def encoding(self)` -- Report the real stream encoding.
- `ThreadStdoutRouter.isatty` (method) `modules/lazy_runner.py:84` `def isatty(self)` -- Report whether the real stream is a terminal.
- `LoopRunConfig.clamped` (method) `modules/lazy_runner.py:118` `def clamped(self)` -- Clamp numeric knobs to the supported operating range.
- `parse_loop_line` (function) `modules/lazy_runner.py:163` `def parse_loop_line(line)` -- Parse one loop command line into a :class:`LoopRunConfig`.
- `resolve_loop_defaults` (function) `modules/lazy_runner.py:282` `def resolve_loop_defaults(config)` -- Fill unset rounds and workers from the selected orchestrator profile.
- `build_executor` (function) `modules/lazy_runner.py:318` `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` -- Build the worker executor: shell verbs, custom tools, safe bash.
- `report_result` (function) `modules/lazy_runner.py:449` `def report_result(result)` -- Print the final outcome of one loop run.
- `stream` (function) `modules/lazy_runner.py:550` `def stream(text)`
- `load_targets_file` (function) `modules/lazy_runner.py:847` `def load_targets_file(path)` -- Read and validate one target per line from a scope file.
- `run_loop` (function) `modules/lazy_runner.py:902` `def run_loop(shell, params, config)` -- Execute one complete loop run and return its summary.

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

## modules/lazy_skill_mirror.py
Imported by: `cli/commands/lazyops.py`
- `available_skills` (function) `modules/lazy_skill_mirror.py:67` `def available_skills()` -- Return repo skill names that ship a SKILL.md.
- `mirror_skill` (function) `modules/lazy_skill_mirror.py:78` `def mirror_skill(name)` -- Write the Hermes mirror of one skill.
- `mirror_all` (function) `modules/lazy_skill_mirror.py:106` `def mirror_all()` -- Mirror every repo skill; return per-skill summaries.
- `register_external_dirs` (function) `modules/lazy_skill_mirror.py:117` `def register_external_dirs()` -- Register the repo skills tree in the hermes config.

## modules/lazy_skills.py
Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`, `tests/test_lazy_loop.py`, `tests/test_lazy_runner.py`
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

## modules/lazy_verify.py
Depends on: `core/process.py`
- `plan_checks` (function) `modules/lazy_verify.py:84` `def plan_checks(finding_text, poc)` -- Build the read-only check list for one finding.
- `run_check` (function) `modules/lazy_verify.py:143` `def run_check(check, executor)` -- Run one read-only check and classify its result.
- `verdict_from_checks` (function) `modules/lazy_verify.py:214` `def verdict_from_checks(checks_results)` -- Deterministic verdict from a list of check results.
- `verify_finding` (function) `modules/lazy_verify.py:232` `def verify_finding(finding_text, poc, executor)` -- Plan, run and judge the read-only checks for one finding.

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
Imported by: `modules/unified_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_bridge_catalog_filtered.py`, `tests/test_core_modules.py`, `tests/test_exploitgym_gym.py`
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

## modules/lazyown_metaextract0r.py
- `signal_handler` (function) `modules/lazyown_metaextract0r.py:42` `def signal_handler(sig, frame)`
- `extract_pdf_metadata` (function) `modules/lazyown_metaextract0r.py:51` `def extract_pdf_metadata(file_path)`
- `extract_docx_metadata` (function) `modules/lazyown_metaextract0r.py:62` `def extract_docx_metadata(file_path)`
- `extract_ole_metadata` (function) `modules/lazyown_metaextract0r.py:73` `def extract_ole_metadata(file_path)`
- `extract_image_metadata` (function) `modules/lazyown_metaextract0r.py:85` `def extract_image_metadata(file_path)`
- `extract_metadata` (function) `modules/lazyown_metaextract0r.py:96` `def extract_metadata(file_path)`
- `find_and_extract_metadata` (function) `modules/lazyown_metaextract0r.py:109` `def find_and_extract_metadata(directory, output_file)`
- `parse_arguments` (function) `modules/lazyown_metaextract0r.py:130` `def parse_arguments()` -- Parse command-line arguments.
- `main` (function) `modules/lazyown_metaextract0r.py:140` `def main()`

## modules/lazyown_parquet_tool.py
- `highlight_term` (function) `modules/lazyown_parquet_tool.py:34` `def highlight_term(text, term)` -- Highlight the search term in the given text.
- `search_in_parquet` (function) `modules/lazyown_parquet_tool.py:39` `def search_in_parquet(term, parquet_files)` -- Search for a term in the given Parquet files and return matching rows.
- `buscar_binarios` (function) `modules/lazyown_parquet_tool.py:53` `def buscar_binarios(args)` -- Search for binaries with special permissions and generate a results CSV.
- `ejecutar_opciones` (function) `modules/lazyown_parquet_tool.py:136` `def ejecutar_opciones()` -- Execute options based on the found data.

## modules/lazyownerweb.py
Depends on: `core/logging.py`, `modules/logging_config.py`
- `send_request` (function) `modules/lazyownerweb.py:36` `def send_request(url, params, method)`
- `test_injection` (function) `modules/lazyownerweb.py:49` `def test_injection(url, payloads, param_name, detection_strings, method)`
- `main` (function) `modules/lazyownerweb.py:59` `def main()`

## modules/lazypsexec.sh
- `execute_psexec` (function) `modules/lazypsexec.sh:15` -- Función para ejecutar psexec y verificar la salida

## modules/lazyreverse_shell.sh
- `mostrar_ayuda` (function) `modules/lazyreverse_shell.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyreverse_shell.sh:31` -- Validar dirección IP

## modules/lazyvpnshield.sh
- `ctrl_c` (function) `modules/lazyvpnshield.sh:11`
- `check_sudo` (function) `modules/lazyvpnshield.sh:16`
- `save_current_rules` (function) `modules/lazyvpnshield.sh:29`
- `show_current_rules` (function) `modules/lazyvpnshield.sh:37`
- `apply_vpn_rules` (function) `modules/lazyvpnshield.sh:45`
- `undo_and_restore_rules` (function) `modules/lazyvpnshield.sh:86`
- `main` (function) `modules/lazyvpnshield.sh:113`

## modules/lazywps.sh
- `ctrl_c` (function) `modules/lazywps.sh:9`

## modules/lesson_ingestor.py
Depends on: `core/logging.py`, `modules/moe_router.py`, `modules/rl_trainer.py`
Imported by: `skills/lazyown_campaign.py`, `tests/test_lesson_ingestor.py`
- `LessonLearned.from_dict` (method) `modules/lesson_ingestor.py:66` `def from_dict(cls, d)`
- `LessonIngestor.__init__` (method) `modules/lesson_ingestor.py:86` `def __init__(self, lessons_file, router, trainer, boost_reward)`
- `LessonIngestor.ingest` (method) `modules/lesson_ingestor.py:125` `def ingest(self, lesson)` -- Apply a single lesson to the MoE performance store and RL Q-table.
- `LessonIngestor.ingest_all` (method) `modules/lesson_ingestor.py:185` `def ingest_all(self, lessons)` -- Ingest a batch of lessons.
- `ingest_campaign_lessons` (function) `modules/lesson_ingestor.py:222` `def ingest_campaign_lessons(lessons_file)` -- Module-level convenience function to ingest all campaign lessons.

## modules/lilsplunky.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `simple_parse_log_line` (function) `modules/lilsplunky.py:69` `def simple_parse_log_line(line, file_path)` -- Intenta extraer información básica de una línea de log.
- `store_event` (function) `modules/lilsplunky.py:108` `def store_event(event_data)` -- Almacena el evento procesado (diccionario Python) como una línea JSON en el archivo de salida.
- `analyze_with_deepseek` (function) `modules/lilsplunky.py:123` `def analyze_with_deepseek(log_entry_data)` -- Sends a single log entry to DeepSeek for analysis.
- `LogFileHandler.__init__` (method) `modules/lilsplunky.py:223` `def __init__(self, log_dir, mode)`
- `LogFileHandler.initialize_file_positions` (method) `modules/lilsplunky.py:229` `def initialize_file_positions(self)` -- Set initial position to the end of all currently monitored files.
- `LogFileHandler.is_monitored` (method) `modules/lilsplunky.py:245` `def is_monitored(self, file_path)` -- Check if the file path matches any of the monitored patterns.
- `LogFileHandler.process_file` (method) `modules/lilsplunky.py:257` `def process_file(self, file_path)` -- Reads new lines from a file since the last known position.
- `LogFileHandler.on_modified` (method) `modules/lilsplunky.py:331` `def on_modified(self, event)` -- Triggered when a file or directory is modified.
- `LogFileHandler.on_created` (method) `modules/lilsplunky.py:336` `def on_created(self, event)` -- Triggered when a file or directory is created.
- `display_record` (function) `modules/lilsplunky.py:346` `def display_record(record)` -- Muestra un registro procesado de forma atractiva en la consola.
- `search_logs` (function) `modules/lilsplunky.py:382` `def search_logs(query, file_path)` -- Busca en el archivo de eventos JSONL registros que coincidan (búsqueda simple de substring).
- `start_monitoring` (function) `modules/lilsplunky.py:413` `def start_monitoring(log_dir, mode)` -- Starts monitoring the specified log directory.
- `parse_args` (function) `modules/lilsplunky.py:446` `def parse_args()`

## modules/linux_advanced_payloads.py
Imported by: `cli/commands/payload_arsenal.py`
- `LinuxAdvancedPayloadFactory.__init__` (method) `modules/linux_advanced_payloads.py:105` `def __init__(self, config, output_dir)`
- `LinuxAdvancedPayloadFactory.generate_ld_preload_rootkit` (method) `modules/linux_advanced_payloads.py:110` `def generate_ld_preload_rootkit(self)` -- Generate a C source file for an LD_PRELOAD rootkit.
- `LinuxAdvancedPayloadFactory.generate_ebpf_payload` (method) `modules/linux_advanced_payloads.py:235` `def generate_ebpf_payload(self)` -- Generate an eBPF C program for network manipulation.
- `LinuxAdvancedPayloadFactory.generate_pam_backdoor` (method) `modules/linux_advanced_payloads.py:311` `def generate_pam_backdoor(self)` -- Generate a PAM (Pluggable Authentication Module) backdoor.
- `LinuxAdvancedPayloadFactory.generate_systemd_persistence` (method) `modules/linux_advanced_payloads.py:398` `def generate_systemd_persistence(self)` -- Generate systemd service and timer units for persistent callbacks.
- `LinuxAdvancedPayloadFactory.generate_ssh_persistence` (method) `modules/linux_advanced_payloads.py:458` `def generate_ssh_persistence(self)` -- Generate an SSH persistence script for authorized_keys injection.
- `LinuxAdvancedPayloadFactory.generate_kernel_module` (method) `modules/linux_advanced_payloads.py:519` `def generate_kernel_module(self)` -- Generate a Linux kernel module (LKM) rootkit.
- `LinuxAdvancedPayloadFactory.generate_process_masquerade` (method) `modules/linux_advanced_payloads.py:632` `def generate_process_masquerade(self)` -- Generate a process masquerading script.
- `LinuxAdvancedPayloadFactory.generate_udev_persistence` (method) `modules/linux_advanced_payloads.py:676` `def generate_udev_persistence(self)` -- Generate a udev rule for persistence on USB/device events.
- `LinuxAdvancedPayloadFactory.generate_motd_backdoor` (method) `modules/linux_advanced_payloads.py:689` `def generate_motd_backdoor(self)` -- Generate a Message of the Day (motd) hook for persistence.
- `LinuxAdvancedPayloadFactory.compile_c_source` (method) `modules/linux_advanced_payloads.py:707` `def compile_c_source(self, source, output_name, shared)` -- Compile C source code to a binary or shared library.
- `LinuxAdvancedPayloadFactory.generate_all` (method) `modules/linux_advanced_payloads.py:749` `def generate_all(self)` -- Generate all Linux advanced payload artifacts.
- `LinuxAdvancedPayloadFactory.list_hook_functions` (method) `modules/linux_advanced_payloads.py:793` `def list_hook_functions()`
- `LinuxAdvancedPayloadFactory.list_persistence_methods` (method) `modules/linux_advanced_payloads.py:797` `def list_persistence_methods()`

## modules/listener_manager.py
Depends on: `utils.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `lazyc2.py`
- `Listener.to_dict` (method) `modules/listener_manager.py:152` `def to_dict(self)`
- `Listener.from_dict` (method) `modules/listener_manager.py:162` `def from_dict(cls, data)`
- `ListenerManager.__init__` (method) `modules/listener_manager.py:179` `def __init__(self, app, sessions_dir, payload)`
- `ListenerManager.set_payload` (method) `modules/listener_manager.py:187` `def set_payload(self, payload)` -- Update the payload mapping used to resolve the bind address.
- `ListenerManager.add` (method) `modules/listener_manager.py:229` `def add(self, port, ssl, listener_id)` -- Register a new listener configuration (does not start it).
- `ListenerManager.remove` (method) `modules/listener_manager.py:242` `def remove(self, listener_id)` -- Remove a listener configuration.
- `ListenerManager.start` (method) `modules/listener_manager.py:255` `def start(self, listener_id)` -- Start a single listener.
- `ListenerManager.stop` (method) `modules/listener_manager.py:335` `def stop(self, listener_id)` -- Stop a single listener.
- `ListenerManager.start_all` (method) `modules/listener_manager.py:356` `def start_all(self)` -- Start every listener marked as active.
- `ListenerManager.stop_all` (method) `modules/listener_manager.py:362` `def stop_all(self)` -- Stop every running listener.
- `ListenerManager.status` (method) `modules/listener_manager.py:367` `def status(self)` -- Return status of all listeners.
- `ListenerManager.get_default_port` (method) `modules/listener_manager.py:379` `def get_default_port(self, fallback)` -- Return the port of the first active listener, or fallback.

## modules/live_surface.py
Depends on: `modules/world_model.py`
Imported by: `lazyc2.py`, `modules/unified_dashboard.py`, `tests/test_live_surface.py`
- `build_live_graph` (function) `modules/live_surface.py:72` `def build_live_graph(world)` -- Build a live vis-network payload from a world-model snapshot.

## modules/llm_adapter.py
Depends on: `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazyphishingai.py`, `core/logging.py`, `modules/llm_factory.py`, `modules/llm_prompts.py`
Imported by: `cli/commands/ai.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_llm_adapter_parity.py`
- `safe_groq_client` (function) `modules/llm_adapter.py:48` `def safe_groq_client(api_key)` -- Create a Groq client, returning None when no key is provided.
- `process_prompt` (function) `modules/llm_adapter.py:119` `def process_prompt(client, prompt, debug)` -- Generate a single-line shell command from a user prompt.
- `process_prompt_script` (function) `modules/llm_adapter.py:133` `def process_prompt_script(client, prompt, debug)` -- Generate a full script from a user prompt.
- `process_prompt_adversary` (function) `modules/llm_adapter.py:147` `def process_prompt_adversary(client, prompt, debug)` -- Answer questions about MITRE ATT&CK techniques and Atomic Red Team.
- `process_prompt_general` (function) `modules/llm_adapter.py:161` `def process_prompt_general(client, prompt, debug)` -- Answer as a general red-team assistant with payload.json context.
- `process_prompt_search` (function) `modules/llm_adapter.py:175` `def process_prompt_search(client, prompt, debug)` -- Perform research and threat-intelligence analysis.
- `process_prompt_task` (function) `modules/llm_adapter.py:189` `def process_prompt_task(client, prompt, debug)` -- Analyze a task-assessment JSON file for completion status.
- `process_prompt_vuln` (function) `modules/llm_adapter.py:206` `def process_prompt_vuln(client, prompt, debug, event)` -- Analyze Nmap output for vulnerabilities and propose an action plan.
- `process_prompt_redop` (function) `modules/llm_adapter.py:237` `def process_prompt_redop(client, prompt, debug)` -- Evaluate a red-team operation status from a JSON database file.
- `ask_general` (function) `modules/llm_adapter.py:254` `def ask_general(prompt, debug)` -- Answer through the configured LLM backend, regardless of provider.

## modules/llm_client.py
Depends on: `core/logging.py`, `modules/ai_model.py`
Imported by: `contrib/legacy/lazyaddon_creator.py`, `modules/llm_factory.py`, `modules/planner.py`, `modules/playbook_engine.py`, `skills/lazyown_mcp.py`
- `LLMClient.__init__` (method) `modules/llm_client.py:63` `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)`
- `LLMClient.ask` (method) `modules/llm_client.py:79` `def ask(self, prompt)` -- Send a prompt and return the text response.
- `LLMClient.classify` (method) `modules/llm_client.py:130` `def classify(self, output)` -- Short classification prompt.
- `LLMClient.summarize` (method) `modules/llm_client.py:159` `def summarize(self, text)` -- Summarize a block of text (e.g. nmap output, tool output).
- `get_client` (function) `modules/llm_client.py:268` `def get_client(api_key)` -- Return (or create) the module-level singleton LLMClient.
- `ask` (function) `modules/llm_client.py:276` `def ask(prompt)` -- Module-level convenience wrapper.
- `classify` (function) `modules/llm_client.py:288` `def classify(output)` -- Module-level convenience wrapper.
- `summarize` (function) `modules/llm_client.py:293` `def summarize(text)` -- Module-level convenience wrapper.


Next: [API_p15.md](API_p15.md)
