# API (page 8 of 23)
Previous: [API_p7.md](API_p7.md)

## lazyc2/blueprints/api.py
Depends on: `core/api_authz.py`, `core/config.py`, `core/defaults.py`, `core/logging.py`
Imported by: `lazyc2/blueprints/__init__.py`, `lazyc2/blueprints/api_v1.py`, `lazyc2/blueprints/orchestrator.py`, `tests/test_core_defaults.py`, `tests/test_security_hardening_v5.py`
- `health` (function) `lazyc2/blueprints/api.py:108` `def health()` -- Health-check endpoint returning subsystem status.
- `ping` (function) `lazyc2/blueprints/api.py:120` `def ping()` -- Lightweight liveness probe.
- `require_api_auth_with_store` (function) `lazyc2/blueprints/api.py:129` `def require_api_auth_with_store(view)` -- Protect a view with the app-scoped API key store.
- `guarded` (function) `lazyc2/blueprints/api.py:146` `def guarded()`
- `health_tenant` (function) `lazyc2/blueprints/api.py:157` `def health_tenant()` -- Health-check scoped to the current authenticated tenant.
- `get_defaults` (function) `lazyc2/blueprints/api.py:182` `def get_defaults()` -- Return build-time defaults alongside live payload values.
- `set_default` (function) `lazyc2/blueprints/api.py:211` `def set_default()` -- Persist a per-engagement override for a build default.

## lazyc2/blueprints/api_v1.py
Depends on: `core/logging.py`, `core/safe_exec.py`, `lazyc2/blueprints/api.py`, `modules/beacon_history.py`, `modules/db.py`
Imported by: `lazyc2/blueprints/__init__.py`, `tests/test_api_v1.py`
- `health` (function) `lazyc2/blueprints/api_v1.py:65` `def health()` -- Public service status (same payload as ``/api/health``).
- `targets` (function) `lazyc2/blueprints/api_v1.py:76` `def targets()` -- List in-scope hosts from the campaign database.
- `results` (function) `lazyc2/blueprints/api_v1.py:108` `def results()` -- Return beacon task results.
- `campaigns` (function) `lazyc2/blueprints/api_v1.py:141` `def campaigns()` -- Report autonomous campaign status from operational state files.
- `webhooks_list` (function) `lazyc2/blueprints/api_v1.py:180` `def webhooks_list()` -- List registered result webhooks.
- `webhooks_register` (function) `lazyc2/blueprints/api_v1.py:191` `def webhooks_register()` -- Register a result webhook URL.
- `webhooks_delete` (function) `lazyc2/blueprints/api_v1.py:228` `def webhooks_delete(index)` -- Remove a registered webhook by index.

## lazyc2/blueprints/auth.py
Depends on: `cli/commands/enum.py`, `core/logging.py`, `lazyc2/__init__.py`, `lazyc2/extensions/decoy.py`, `lazyc2/extensions/users.py`, `modules/lazy_rbac.py`
Imported by: `lazyc2/blueprints/__init__.py`, `lazygui/services/teamserver_backend.py`, `static/js/socket.io-4.0.0.min.js`, `static/js/socket.io-4.3.2.min.js`
- `Role.valid_roles` (method) `lazyc2/blueprints/auth.py:51` `def valid_roles(cls)` -- Return valid role values.
- `require_role` (function) `lazyc2/blueprints/auth.py:59` `def require_role(role)` -- Return a deny-by-default decorator when RBAC is unavailable.
- `decorator` (function) `lazyc2/blueprints/auth.py:69` `def decorator(view)`
- `wrapper` (function) `lazyc2/blueprints/auth.py:71` `def wrapper()`
- `register` (function) `lazyc2/blueprints/auth.py:128` `def register()`
- `login` (function) `lazyc2/blueprints/auth.py:187` `def login()`
- `mfa_setup` (function) `lazyc2/blueprints/auth.py:232` `def mfa_setup()`
- `mfa_qr` (function) `lazyc2/blueprints/auth.py:305` `def mfa_qr(username)`
- `mfa_verify` (function) `lazyc2/blueprints/auth.py:327` `def mfa_verify()`
- `profile` (function) `lazyc2/blueprints/auth.py:371` `def profile()`
- `logout` (function) `lazyc2/blueprints/auth.py:396` `def logout()`
- `admin_users` (function) `lazyc2/blueprints/auth.py:415` `def admin_users()`
- `admin_set_role` (function) `lazyc2/blueprints/auth.py:432` `def admin_set_role(user_id)`
- `admin_reset_mfa` (function) `lazyc2/blueprints/auth.py:454` `def admin_reset_mfa(user_id)`
- `admin_delete_user` (function) `lazyc2/blueprints/auth.py:466` `def admin_delete_user(user_id)`
- `admin_tenants` (function) `lazyc2/blueprints/auth.py:484` `def admin_tenants()`
- `admin_create_tenant` (function) `lazyc2/blueprints/auth.py:504` `def admin_create_tenant()`
- `admin_switch_tenant` (function) `lazyc2/blueprints/auth.py:523` `def admin_switch_tenant(tenant_id)`

## lazyc2/blueprints/beacon.py
Depends on: `core/logging.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/state_manager.py`
Imported by: `lazyc2/blueprints/__init__.py`
- `init_beacon_bp` (function) `lazyc2/blueprints/beacon.py:35` `def init_beacon_bp(commands, results, commands_history, connected_clients, encrypt_fn, decrypt_fn, config...` -- Wire the blueprint to the C2 monolith's shared state.
- `send_command` (function) `lazyc2/blueprints/beacon.py:111` `def send_command(client_id)` -- Implant polls for the next encrypted command.
- `receive_result` (function) `lazyc2/blueprints/beacon.py:131` `def receive_result(client_id)` -- Implant reports command output.
- `issue_command` (function) `lazyc2/blueprints/beacon.py:245` `def issue_command()` -- Operator queues a command for a connected implant.

## lazyc2/blueprints/operations.py
Depends on: `lazyc2/blueprints/session_auth.py`, `lazyc2/extensions/decoy.py`, `lazyc2/extensions/storage.py`
Imported by: `lazyc2/blueprints/__init__.py`
- `task_detail` (function) `lazyc2/blueprints/operations.py:33` `def task_detail(task_id)` -- View a single task by ID.
- `get_tasks` (function) `lazyc2/blueprints/operations.py:48` `def get_tasks()` -- Return all tasks as JSON.
- `tasks` (function) `lazyc2/blueprints/operations.py:57` `def tasks()` -- Render the tasks list page.
- `edit_task` (function) `lazyc2/blueprints/operations.py:66` `def edit_task(task_id)` -- Edit an existing task.
- `cves` (function) `lazyc2/blueprints/operations.py:92` `def cves()` -- List all CVEs or create a new one.
- `cve_detail` (function) `lazyc2/blueprints/operations.py:117` `def cve_detail(cve_id)` -- View a single CVE by ID.
- `edit_cve` (function) `lazyc2/blueprints/operations.py:132` `def edit_cve(cve_id)` -- Edit an existing CVE entry.
- `edit_notes` (function) `lazyc2/blueprints/operations.py:158` `def edit_notes()` -- View or edit the operator notes.
- `get_notes` (function) `lazyc2/blueprints/operations.py:173` `def get_notes()` -- Return notes as JSON.
- `view_note` (function) `lazyc2/blueprints/operations.py:182` `def view_note()` -- Render the notes view page.
- `event_config` (function) `lazyc2/blueprints/operations.py:192` `def event_config()` -- Return event configuration as JSON.
- `event_config_view` (function) `lazyc2/blueprints/operations.py:198` `def event_config_view()` -- View or update event configuration.
- `events` (function) `lazyc2/blueprints/operations.py:218` `def events()` -- Render the events page.

## lazyc2/blueprints/orchestrator.py
Depends on: `core/logging.py`, `lazyc2/blueprints/api.py`, `modules/__init__.py`, `modules/killchain.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`, `modules/trigger_policy.py`, `modules/verb_catalog.py`, `modules/world_model.py`
Imported by: `lazyc2/app_factory.py`, `tests/test_orchestrator_api.py`
- `status` (function) `lazyc2/blueprints/orchestrator.py:104` `def status()` -- One-call awareness: world model, verbs, triggers and stages.
- `world` (function) `lazyc2/blueprints/orchestrator.py:111` `def world()` -- Return the raw world-model + kill chain snapshot.
- `verbs` (function) `lazyc2/blueprints/orchestrator.py:125` `def verbs()` -- Verb catalog view with optional search filtering.
- `verbs_toggle` (function) `lazyc2/blueprints/orchestrator.py:149` `def verbs_toggle()` -- Flip one loop verb between enabled and disabled.
- `stages_toggle` (function) `lazyc2/blueprints/orchestrator.py:166` `def stages_toggle()` -- Flip one autonomous-loop stage between enabled and disabled.
- `stage_names` (function) `lazyc2/blueprints/orchestrator.py:180` `def stage_names()` -- Return the known stage names (fallback builtins included).
- `triggers` (function) `lazyc2/blueprints/orchestrator.py:193` `def triggers()` -- List the scheduler triggers pinned in the store.
- `triggers_add` (function) `lazyc2/blueprints/orchestrator.py:202` `def triggers_add()` -- Register one scheduler trigger from the JSON body.
- `triggers_seed` (function) `lazyc2/blueprints/orchestrator.py:222` `def triggers_seed()` -- Re-merge the declarative YAML seeds into the store once.
- `triggers_delete` (function) `lazyc2/blueprints/orchestrator.py:231` `def triggers_delete(trigger_id)` -- Remove one scheduler trigger by id.
- `panel` (function) `lazyc2/blueprints/orchestrator.py:242` `def panel()` -- Dashboard panel mirroring the orchestrator console state.
- `panel_json` (function) `lazyc2/blueprints/orchestrator.py:262` `def panel_json()` -- JSON mirror of the panel payload for automation.

## lazyc2/blueprints/phishing.py
Depends on: `core/logging.py`, `lazyc2/extensions/short_urls.py`, `lazyc2/security/validators.py`, `modules/security_sanitizers.py`, `utils.py`
Imported by: `lazyc2/blueprints/__init__.py`
- `create_short_url` (function) `lazyc2/blueprints/phishing.py:49` `def create_short_url()` -- Create one or more short URLs for a single original URL.
- `track_interaction` (function) `lazyc2/blueprints/phishing.py:89` `def track_interaction(short_url)` -- Serve a tracking page and log behavioural data.
- `update_short_url` (function) `lazyc2/blueprints/phishing.py:125` `def update_short_url(short_url)` -- Update an existing short URL's target or active status.
- `redirect_to_file` (function) `lazyc2/blueprints/phishing.py:151` `def redirect_to_file(short_url)` -- Resolve a short URL and redirect (or serve a local file).
- `webserver_report` (function) `lazyc2/blueprints/phishing.py:174` `def webserver_report(filename)` -- Serve nmap HTML report assets from the sessions directory.
- `download_files` (function) `lazyc2/blueprints/phishing.py:192` `def download_files(filename)` -- Serve a session file by name with path-traversal protection.

## lazyc2/blueprints/session_auth.py
Imported by: `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/operations.py`
- `require_operator_session` (function) `lazyc2/blueprints/session_auth.py:20` `def require_operator_session(blueprint, login_endpoint)` -- Register a ``before_request`` guard on a blueprint.

## lazyc2/extensions/decoy.py
Imported by: `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/auth.py`, `lazyc2/blueprints/operations.py`
- `decoy_response` (function) `lazyc2/extensions/decoy.py:12` `def decoy_response()` -- Return a decoy page when the client IP is not the operator host.

## lazyc2/extensions/short_urls.py
Depends on: `core/logging.py`
Imported by: `lazyc2/blueprints/phishing.py`
- `configure` (function) `lazyc2/extensions/short_urls.py:21` `def configure(sessions_phishing_dir)` -- Set the phishing directory where short_urls.json lives.
- `load_short_urls` (function) `lazyc2/extensions/short_urls.py:33` `def load_short_urls()` -- Load short URLs from JSON file, creating it if it doesn't exist.
- `save_short_urls` (function) `lazyc2/extensions/short_urls.py:59` `def save_short_urls(data)` -- Save short URLs to JSON file.
- `is_valid_url` (function) `lazyc2/extensions/short_urls.py:104` `def is_valid_url(url)` -- Validate if the input is a valid URL or existing local file path.

## lazyc2/extensions/storage.py
Depends on: `core/logging.py`
Imported by: `lazyc2/blueprints/operations.py`
- `configure` (function) `lazyc2/extensions/storage.py:18` `def configure(sessions_dir)` -- Set the session directory path.
- `load_tasks` (function) `lazyc2/extensions/storage.py:31` `def load_tasks()` -- Load tasks from ``sessions/tasks.json``.
- `save_tasks` (function) `lazyc2/extensions/storage.py:45` `def save_tasks(tasks)` -- Persist tasks to ``sessions/tasks.json``.
- `load_cves` (function) `lazyc2/extensions/storage.py:59` `def load_cves()` -- Load CVEs from ``sessions/cves.json``.
- `save_cves` (function) `lazyc2/extensions/storage.py:73` `def save_cves(cves)` -- Persist CVEs to ``sessions/cves.json``.
- `load_note` (function) `lazyc2/extensions/storage.py:87` `def load_note()` -- Load the operator note from ``sessions/notes.txt``.
- `save_note` (function) `lazyc2/extensions/storage.py:107` `def save_note(content)` -- Persist the operator note to ``sessions/notes.txt``.
- `load_event_config` (function) `lazyc2/extensions/storage.py:121` `def load_event_config()` -- Load event configuration from ``event_config.json``.
- `load_notifications` (function) `lazyc2/extensions/storage.py:137` `def load_notifications()` -- Load notifications from ``sessions/notifications.json``.
- `load_banners` (function) `lazyc2/extensions/storage.py:154` `def load_banners()` -- Load banners from ``sessions/banners.json``.
- `load_routes` (function) `lazyc2/extensions/storage.py:179` `def load_routes()` -- Load dynamic routes from ``sessions/routes_to_templates.json``.
- `save_routes` (function) `lazyc2/extensions/storage.py:194` `def save_routes(routes)` -- Persist dynamic routes with atomic write and safe permissions.

## lazyc2/extensions/users.py
Depends on: `lazyc2/__init__.py`, `modules/lazy_rbac.py`
Imported by: `lazyc2.py`, `lazyc2/blueprints/auth.py`
- `configure` (function) `lazyc2/extensions/users.py:16` `def configure(users_path)` -- Set the path for the legacy JSON user file.
- `load_users` (function) `lazyc2/extensions/users.py:26` `def load_users()` -- Load users from the JSON store or RBAC store.
- `save_users` (function) `lazyc2/extensions/users.py:48` `def save_users(users)` -- Persist users to the JSON store or RBAC store.

## lazyc2/models.py
Depends on: `modules/lazy_rbac.py`
- `User.__init__` (method) `lazyc2/models.py:17` `def __init__(self, user_data)`

## lazyc2/security/command_allowlist.py
Depends on: `cli/commands/enum.py`
Imported by: `lazyc2.py`, `tests/test_command_allowlist.py`, `tests/test_command_allowlist_behavior.py`
- `CommandDecision.to_dict` (method) `lazyc2/security/command_allowlist.py:61` `def to_dict(self)` -- Return a JSON-serializable dict for the audit log.
- `CommandAllowlist.__init__` (method) `lazyc2/security/command_allowlist.py:82` `def __init__(self, allowed, audit_log_path)`
- `CommandAllowlist.allowed` (method) `lazyc2/security/command_allowlist.py:94` `def allowed(self)` -- Return the immutable set of allowed first tokens (lowercased).
- `CommandAllowlist.check` (method) `lazyc2/security/command_allowlist.py:98` `def check(self, command)` -- Return the :class:`CommandDecision` for ``command``.

## lazyc2/security/cors.py
Imported by: `lazyc2.py`, `tests/test_cors_behavior.py`, `tests/test_cors_policy.py`, `tests/test_cors_socketio_regression.py`
- `CorsPolicy.__init__` (method) `lazyc2/security/cors.py:70` `def __init__(self, env, lhost, allowed_origins, c2_port, extra_socketio_ports)`
- `CorsPolicy.env` (method) `lazyc2/security/cors.py:85` `def env(self)` -- Return the normalized environment tag (``"PROD"`` or ``"DEV"``).
- `CorsPolicy.resolve_origins` (method) `lazyc2/security/cors.py:89` `def resolve_origins(self)` -- Return the validated allowlist of origins for the current env.
- `CorsPolicy.origins_for_socketio` (method) `lazyc2/security/cors.py:110` `def origins_for_socketio(self)` -- Return the allowlist to feed ``flask_socketio.SocketIO``.
- `CorsPolicy.is_allowed` (method) `lazyc2/security/cors.py:136` `def is_allowed(self, origin)` -- Return ``True`` if ``origin`` matches any allowed entry.

## lazyc2/security/csrf.py
Imported by: `lazyc2.py`, `lazyc2/blueprints/addons.py`, `tests/test_csrf_behavior.py`, `tests/test_csrf_policy.py`
- `CSRFPolicy.__init__` (method) `lazyc2/security/csrf.py:69` `def __init__(self, header, form_field, cookie_name, exempt_paths, secret)`
- `CSRFPolicy.header` (method) `lazyc2/security/csrf.py:85` `def header(self)` -- Return the HTTP header name carrying the token.
- `CSRFPolicy.cookie_name` (method) `lazyc2/security/csrf.py:90` `def cookie_name(self)` -- Return the cookie name that should hold the readable token.
- `CSRFPolicy.issue` (method) `lazyc2/security/csrf.py:94` `def issue(self, session_id)` -- Return the token bound to ``session_id``.
- `CSRFPolicy.rotate` (method) `lazyc2/security/csrf.py:111` `def rotate(self, session_id)` -- Force a fresh token for ``session_id``.
- `CSRFPolicy.forget` (method) `lazyc2/security/csrf.py:126` `def forget(self, session_id)` -- Drop the token bound to ``session_id`` (e.g. on logout).
- `CSRFPolicy.validate` (method) `lazyc2/security/csrf.py:130` `def validate(self, session_id, candidate)` -- Return ``True`` iff ``candidate`` matches the stored token.
- `CSRFPolicy.is_exempt` (method) `lazyc2/security/csrf.py:147` `def is_exempt(self, path)` -- Return ``True`` if ``path`` is in the exempt set.
- `CSRFPolicy.extract_token` (method) `lazyc2/security/csrf.py:163` `def extract_token(self, request)` -- Return the token from a Flask-shaped request.
- `CSRFPolicy.check_request` (method) `lazyc2/security/csrf.py:182` `def check_request(self, session_id, request)` -- Run the full CSRF gate against a request.

## lazyc2/security/html_sanitizer.py
Depends on: `lazyc2/security/constants.py`
Imported by: `lazyc2.py`, `tests/test_html_sanitizer.py`
- `sanitize_html` (function) `lazyc2/security/html_sanitizer.py:78` `def sanitize_html(raw_html, allowed_tags, allowed_attributes)` -- Return a sanitized HTML string safe for ``render_template``.

## lazyc2/security/https_redirect.py
Imported by: `lazyc2.py`, `tests/test_https_redirect.py`
- `HTTPSRedirect.__init__` (method) `lazyc2/security/https_redirect.py:51` `def __init__(self, env, enabled)`
- `HTTPSRedirect.enabled` (method) `lazyc2/security/https_redirect.py:56` `def enabled(self)` -- Return ``True`` when the policy is active.
- `HTTPSRedirect.evaluate` (method) `lazyc2/security/https_redirect.py:60` `def evaluate(self, request)` -- Return a redirect response, or ``None`` if the request can pass.

## lazyc2/security/services.py
Depends on: `lazyc2/security/constants.py`, `lazyc2/security/validators.py`
Imported by: `lazyc2.py`, `lazyc2/app_factory.py`, `modules/c2_agent.py`, `tests/test_security_lazyc2.py`
- `SecretKeyManager.__init__` (method) `lazyc2/security/services.py:30` `def __init__(self, sessions_dir)`
- `SecretKeyManager.get_or_create` (method) `lazyc2/security/services.py:33` `def get_or_create(self)` -- Return an existing secret key or generate and persist a new one.
- `SafeFileService.__init__` (method) `lazyc2/security/services.py:63` `def __init__(self, base_dir)`
- `SafeFileService.read_bytes` (method) `lazyc2/security/services.py:86` `def read_bytes(self, relative_path)` -- Read a file as bytes after path validation.
- `SafeFileService.read_text` (method) `lazyc2/security/services.py:102` `def read_text(self, relative_path, encoding)` -- Read a file as text after path validation.
- `SafeFileService.write_bytes` (method) `lazyc2/security/services.py:119` `def write_bytes(self, relative_path, data)` -- Write bytes to a file after path validation.
- `SafeFileService.exists` (method) `lazyc2/security/services.py:136` `def exists(self, relative_path)` -- Check if a path exists after validation.
- `AESKeyManager.__init__` (method) `lazyc2/security/services.py:158` `def __init__(self, key_file)`
- `AESKeyManager.get_or_generate` (method) `lazyc2/security/services.py:161` `def get_or_generate(self)` -- Return an existing AES key or generate a new one.
- `UploadSizeValidator.__init__` (method) `lazyc2/security/services.py:189` `def __init__(self, max_size_bytes)`
- `UploadSizeValidator.validate` (method) `lazyc2/security/services.py:192` `def validate(self, content_length)` -- Validate upload size.

## lazyc2/security/trusted_proxy.py
Imported by: `lazyc2.py`, `tests/test_trusted_proxy.py`
- `TrustedProxyResolver.__init__` (method) `lazyc2/security/trusted_proxy.py:42` `def __init__(self, trusted_count, operator_allowlist)`
- `TrustedProxyResolver.trusted_count` (method) `lazyc2/security/trusted_proxy.py:53` `def trusted_count(self)` -- Return the configured number of trusted proxy hops.
- `TrustedProxyResolver.client_ip` (method) `lazyc2/security/trusted_proxy.py:57` `def client_ip(self, remote_addr, x_forwarded_for)` -- Return the resolved client IP.
- `TrustedProxyResolver.is_operator` (method) `lazyc2/security/trusted_proxy.py:80` `def is_operator(self, ip)` -- Return ``True`` when ``ip`` is in the operator allowlist.

## lazyc2/security/validators.py
Depends on: `lazyc2/security/constants.py`
Imported by: `lazyc2.py`, `lazyc2/blueprints/phishing.py`, `lazyc2/security/services.py`, `tests/test_security_lazyc2.py`, `tests/test_short_url_file_containment.py`
- `validate_route_path` (function) `lazyc2/security/validators.py:24` `def validate_route_path(route_path)` -- Validate a dynamic route path segment.
- `validate_template_name` (function) `lazyc2/security/validators.py:46` `def validate_template_name(template_name)` -- Validate a Jinja2 template filename.
- `validate_yaml_filename` (function) `lazyc2/security/validators.py:68` `def validate_yaml_filename(filename)` -- Validate a YAML filename for safe loading.
- `validate_request_data` (function) `lazyc2/security/validators.py:86` `def validate_request_data(data)` -- Validate request data length to prevent buffer abuse.
- `validate_aes_key` (function) `lazyc2/security/validators.py:102` `def validate_aes_key(key)` -- Validate AES key length.
- `validate_password_length` (function) `lazyc2/security/validators.py:118` `def validate_password_length(password)` -- Validate password meets minimum length requirement.
- `validate_upload_size` (function) `lazyc2/security/validators.py:134` `def validate_upload_size(content_length)` -- Validate upload size against maximum allowed.
- `validate_file_path_within_base` (function) `lazyc2/security/validators.py:150` `def validate_file_path_within_base(file_path, base_dir)` -- Validate that a resolved file path is within a base directory.
- `resolve_contained_file_path` (function) `lazyc2/security/validators.py:174` `def resolve_contained_file_path(raw_url, base_dir)` -- Resolve a short-URL target to a file path contained in ``base_dir``.

## lazygui/__main__.py
Depends on: `lazygui/app.py`
- `main` (function) `lazygui/__main__.py:14` `def main()` -- Bootstrap the GUI and run the Qt event loop.

## lazygui/app.py
Depends on: `core/logging.py`, `lazygui/config/c2_credentials.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/factory.py`, `lazygui/services/models.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`
Imported by: `lazygui/__main__.py`
- `Application.__init__` (method) `lazygui/app.py:36` `def __init__(self, argv)` -- Build constants/settings/theme/backend/main-window.
- `Application.run` (method) `lazygui/app.py:65` `def run(self)` -- Show the main window, start the backend, and run the event loop.
- `Application.show_connect_dialog` (method) `lazygui/app.py:100` `def show_connect_dialog(self)` -- Open the connection dialog and swap backends if accepted.

## lazygui/config/c2_credentials.py
Depends on: `core/logging.py`
Imported by: `lazygui/app.py`, `lazygui/windows/connect_dialog.py`
- `C2Credentials.empty` (method) `lazygui/config/c2_credentials.py:33` `def empty(cls)` -- Return a sentinel representing no credentials available.
- `load_c2_credentials_from_file` (function) `lazygui/config/c2_credentials.py:38` `def load_c2_credentials_from_file(file_path)` -- Parse ``.c2_credentials.txt`` and return username + password.
- `load_c2_credentials` (function) `lazygui/config/c2_credentials.py:71` `def load_c2_credentials(project_root)` -- Resolve and parse the credentials file relative to ``project_root``.

## lazygui/config/constants.py
Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`, `lazygui/services/event_log.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazygui/theme/qss_builder.py`, `lazygui/widgets/command_palette_list.py`, `lazygui/widgets/event_log_view.py`, `lazygui/widgets/filter_bar.py`, `lazygui/widgets/graph_view.py`, `lazygui/widgets/terminal_view.py`, `lazygui/windows/command_palette_window.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`, `tests/test_lazygui_backend.py`, `tests/test_lazygui_graph_widget.py`
- `AppConstants.panel_labels` (method) `lazygui/config/constants.py:239` `def panel_labels(self)` -- Map panel identifier to human-readable label.

## lazygui/config/paths.py
Depends on: `lazygui/config/constants.py`
Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/config/settings.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/windows/connect_dialog.py`
- `AppPaths.config_dir` (method) `lazygui/config/paths.py:32` `def config_dir(self)` -- User config directory respecting ``XDG_CONFIG_HOME`` when set.
- `AppPaths.settings_file` (method) `lazygui/config/paths.py:39` `def settings_file(self)` -- Absolute path of the persisted settings JSON file.
- `AppPaths.layout_file` (method) `lazygui/config/paths.py:44` `def layout_file(self)` -- Absolute path of the persisted Qt layout binary blob.
- `AppPaths.project_run_script` (method) `lazygui/config/paths.py:49` `def project_run_script(self)` -- Absolute path to the ``run`` shell launcher in the repository.
- `AppPaths.lazyc2_script` (method) `lazygui/config/paths.py:54` `def lazyc2_script(self)` -- Absolute path to the Flask backend ``lazyc2.py``.
- `AppPaths.c2_credentials_path` (method) `lazygui/config/paths.py:59` `def c2_credentials_path(self)` -- Absolute path to the C2 auto-generated credentials file.
- `AppPaths.sessions_dir` (method) `lazygui/config/paths.py:69` `def sessions_dir(self)` -- Absolute path to the sessions directory.
- `AppPaths.ensure_config_dir` (method) `lazygui/config/paths.py:73` `def ensure_config_dir(self)` -- Create the config directory if missing and return it.

## lazygui/config/settings.py
Depends on: `core/logging.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`
Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/theme/manager.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`
- `AppSettings.load` (method) `lazygui/config/settings.py:35` `def load(cls, constants, paths)` -- Load settings from disk, returning empty defaults if absent.
- `AppSettings.save` (method) `lazygui/config/settings.py:47` `def save(self)` -- Persist the current document to disk atomically.
- `AppSettings.get` (method) `lazygui/config/settings.py:55` `def get(self, key, default)` -- Generic accessor for a slash-separated settings key.
- `AppSettings.set` (method) `lazygui/config/settings.py:59` `def set(self, key, value)` -- Assign ``value`` to ``key`` without persisting; call :meth:`save`.
- `AppSettings.theme_id` (method) `lazygui/config/settings.py:64` `def theme_id(self)` -- Currently selected theme identifier.
- `AppSettings.theme_id` (method) `lazygui/config/settings.py:69` `def theme_id(self, value)`
- `AppSettings.last_backend_id` (method) `lazygui/config/settings.py:73` `def last_backend_id(self)` -- Backend identifier last used in the connect dialog.
- `AppSettings.last_backend_id` (method) `lazygui/config/settings.py:78` `def last_backend_id(self, value)`
- `AppSettings.last_teamserver_url` (method) `lazygui/config/settings.py:84` `def last_teamserver_url(self)` -- Last URL typed in the teamserver connection form.
- `AppSettings.last_teamserver_url` (method) `lazygui/config/settings.py:94` `def last_teamserver_url(self, value)`
- `AppSettings.last_operator_name` (method) `lazygui/config/settings.py:98` `def last_operator_name(self)` -- Operator handle the user typed last.
- `AppSettings.last_operator_name` (method) `lazygui/config/settings.py:107` `def last_operator_name(self, value)`
- `AppSettings.last_teamserver_password` (method) `lazygui/config/settings.py:111` `def last_teamserver_password(self)` -- Last teamserver password (stored in settings, derived from credentials file).
- `AppSettings.last_teamserver_password` (method) `lazygui/config/settings.py:116` `def last_teamserver_password(self, value)`
- `AppSettings.c2_credentials_loaded` (method) `lazygui/config/settings.py:120` `def c2_credentials_loaded(self)` -- Whether the last credentials were loaded from the C2 auto-generated file.
- `AppSettings.c2_credentials_loaded` (method) `lazygui/config/settings.py:125` `def c2_credentials_loaded(self, value)`
- `AppSettings.snapshot` (method) `lazygui/config/settings.py:128` `def snapshot(self)` -- Return a defensive read-only copy of the underlying document.

## lazygui/panels/base.py
Depends on: `lazygui/config/constants.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`
- `PanelBase.__init__` (method) `lazygui/panels/base.py:20` `def __init__(self, constants, backend, identifier, title, parent)` -- Initialise the dock widget with stable identifier and title.
- `PanelBase.identifier` (method) `lazygui/panels/base.py:43` `def identifier(self)` -- Stable identifier matching :class:`PanelConstants`.
- `PanelBase.backend` (method) `lazygui/panels/base.py:48` `def backend(self)` -- The currently connected backend instance.

## lazygui/panels/campaign_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `CampaignPanel.__init__` (method) `lazygui/panels/campaign_panel.py:31` `def __init__(self, constants, backend, parent)` -- Build the campaign list UI.
- `CampaignPanel.campaign_count` (method) `lazygui/panels/campaign_panel.py:133` `def campaign_count(self)` -- Return the number of active campaigns.

## lazygui/panels/credentials_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `CredentialsPanel.__init__` (method) `lazygui/panels/credentials_panel.py:30` `def __init__(self, constants, backend, parent)`

## lazygui/panels/cve_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `CVEPanel.__init__` (method) `lazygui/panels/cve_panel.py:31` `def __init__(self, constants, backend, parent)` -- Build the CVE list UI with severity filter.
- `CVEPanel.cve_count` (method) `lazygui/panels/cve_panel.py:178` `def cve_count(self)` -- Return the number of loaded CVEs.

## lazygui/panels/event_log_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/models.py`, `lazygui/widgets/event_log_view.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `EventLogPanel.__init__` (method) `lazygui/panels/event_log_panel.py:27` `def __init__(self, constants, backend, event_log, parent)` -- Compose the toolbar (level filter + clear) and the log view.

## lazygui/panels/graph_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/graph_view.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `GraphPanel.__init__` (method) `lazygui/panels/graph_panel.py:23` `def __init__(self, constants, backend, parent)` -- Build the graph view and connect to backend topology updates.
- `GraphPanel.graph_view` (method) `lazygui/panels/graph_panel.py:118` `def graph_view(self)` -- Return the underlying graph view for layout management.

## lazygui/panels/history_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `HistoryPanel.__init__` (method) `lazygui/panels/history_panel.py:33` `def __init__(self, constants, backend, parent)` -- Build the history viewer UI.

## lazygui/panels/killchain_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `modules/killchain.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `KillChainPanel.__init__` (method) `lazygui/panels/killchain_panel.py:38` `def __init__(self, constants, backend, parent)`

## lazygui/panels/listeners_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/filter_bar.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `ListenersPanel.__init__` (method) `lazygui/panels/listeners_panel.py:24` `def __init__(self, constants, backend, parent)` -- Build the layout and subscribe to backend listener updates.

## lazygui/panels/marketplace_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `MarketplacePanel.__init__` (method) `lazygui/panels/marketplace_panel.py:32` `def __init__(self, constants, backend, parent)` -- Build the tabbed marketplace UI.

## lazygui/panels/registry.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/windows/main_window.py`
- `PanelRegistry.build` (method) `lazygui/panels/registry.py:53` `def build(cls, constants, backend, event_log, parent)` -- Construct every dock panel and return them as a registry.
- `PanelRegistry.all_panels` (method) `lazygui/panels/registry.py:83` `def all_panels(self)` -- Return panels in canonical layout order.
- `PanelRegistry.by_identifier` (method) `lazygui/panels/registry.py:99` `def by_identifier(self, identifier)` -- Look up a panel by its stable identifier.

## lazygui/panels/sessions_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/filter_bar.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `SessionsPanel.__init__` (method) `lazygui/panels/sessions_panel.py:45` `def __init__(self, constants, backend, parent)` -- Build the layout and subscribe to backend session updates.

## lazygui/panels/terminal_panel.py
Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/widgets/terminal_view.py`
Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
- `TerminalPanel.__init__` (method) `lazygui/panels/terminal_panel.py:25` `def __init__(self, constants, backend, parent)` -- Compose the terminal view, session selector and command bar.
- `TerminalPanel.focus_terminal` (method) `lazygui/panels/terminal_panel.py:78` `def focus_terminal(self)` -- Move keyboard focus into the terminal text area.
- `TerminalPanel.set_target_session` (method) `lazygui/panels/terminal_panel.py:82` `def set_target_session(self, session_id)` -- Select a specific beacon in the dropdown.

## lazygui/services/backend.py
Depends on: `cli/commands/enum.py`, `lazygui/services/models.py`
Imported by: `lazygui/app.py`, `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`, `lazygui/services/__init__.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/widgets/beacon_command_modal.py`, `lazygui/widgets/status_badge.py`, `lazygui/windows/main_window.py`, `tests/test_lazygui_backend.py`
- `Backend.__init__` (method) `lazygui/services/backend.py:81` `def __init__(self, descriptor, parent)` -- Store the descriptor that uniquely identifies this backend.
- `Backend.descriptor` (method) `lazygui/services/backend.py:88` `def descriptor(self)` -- Read-only identification for connection dialogs.
- `Backend.status` (method) `lazygui/services/backend.py:93` `def status(self)` -- Current connection lifecycle state.
- `Backend.start` (method) `lazygui/services/backend.py:104` `def start(self)` -- Establish whatever underlying transport this backend uses.
- `Backend.stop` (method) `lazygui/services/backend.py:108` `def stop(self)` -- Tear the underlying transport down cleanly.
- `Backend.send_command` (method) `lazygui/services/backend.py:112` `def send_command(self, command, target_session)` -- Submit ``command``, optionally scoped to ``target_session``.
- `Backend.refresh` (method) `lazygui/services/backend.py:116` `def refresh(self)` -- Force a re-fetch of sessions, listeners and operator info.
- `Backend.resize_terminal` (method) `lazygui/services/backend.py:120` `def resize_terminal(self, columns, rows)` -- Inform the backend the terminal area was resized.
- `Backend.feed_terminal_input` (method) `lazygui/services/backend.py:124` `def feed_terminal_input(self, data)` -- Feed raw keystrokes typed by the operator into the terminal.
- `Backend.known_sessions` (method) `lazygui/services/backend.py:128` `def known_sessions(self)` -- Return the most recent snapshot of sessions, never ``None``.
- `Backend.known_listeners` (method) `lazygui/services/backend.py:132` `def known_listeners(self)` -- Return the most recent snapshot of listeners, never ``None``.
- `Backend.known_topology` (method) `lazygui/services/backend.py:136` `def known_topology(self)` -- Return the most recent graph topology.
- `Backend.known_campaigns` (method) `lazygui/services/backend.py:140` `def known_campaigns(self)` -- Return the most recent snapshot of campaigns.
- `Backend.request_world_model` (method) `lazygui/services/backend.py:144` `def request_world_model(self)` -- Request the current world model state as a dict.
- `Backend.request_beacon_history` (method) `lazygui/services/backend.py:158` `def request_beacon_history(self, client_id)` -- Return the persistent command/result history for a beacon.
- `Backend.request_session_state` (method) `lazygui/services/backend.py:172` `def request_session_state(self)` -- Request the current session state (creds, hashes, loot) as a dict.

## lazygui/services/event_log.py
Depends on: `lazygui/config/constants.py`, `lazygui/services/models.py`
Imported by: `lazygui/app.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/registry.py`, `lazygui/services/__init__.py`, `lazygui/widgets/event_log_view.py`, `lazygui/windows/main_window.py`
- `EventLog.__init__` (method) `lazygui/services/event_log.py:26` `def __init__(self, constants, parent)` -- Initialise the buffer using ``constants.event_log.max_records``.
- `EventLog.capacity` (method) `lazygui/services/event_log.py:33` `def capacity(self)` -- Maximum number of records retained before the oldest is dropped.
- `EventLog.append` (method) `lazygui/services/event_log.py:37` `def append(self, record)` -- Append ``record`` and emit ``record_appended``.
- `EventLog.extend` (method) `lazygui/services/event_log.py:42` `def extend(self, records)` -- Append every entry in ``records`` in iteration order.
- `EventLog.clear` (method) `lazygui/services/event_log.py:47` `def clear(self)` -- Drop all stored records and emit ``cleared``.
- `EventLog.snapshot` (method) `lazygui/services/event_log.py:52` `def snapshot(self, minimum_level)` -- Return a defensive tuple, optionally filtered by ``minimum_level``.

## lazygui/services/factory.py
Depends on: `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/services/backend.py`, `lazygui/services/local_backend.py`, `lazygui/services/models.py`, `lazygui/services/teamserver_backend.py`
Imported by: `lazygui/app.py`, `lazygui/services/__init__.py`, `static/js/html2pdf.bundle.min.js`
- `BackendFactory.create_local` (method) `lazygui/services/factory.py:30` `def create_local(self, parent)` -- Construct a local PTY-based backend.
- `BackendFactory.create_teamserver` (method) `lazygui/services/factory.py:34` `def create_teamserver(self, credentials, parent)` -- Construct a teamserver-based backend with the given credentials.
- `BackendFactory.create` (method) `lazygui/services/factory.py:42` `def create(self, kind, parent, credentials)` -- Convenience dispatch by :class:`BackendKind`.

## lazygui/services/local_backend.py
Depends on: `core/logging.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`
Imported by: `lazygui/services/__init__.py`, `lazygui/services/factory.py`
- `LocalPtyBackend.__init__` (method) `lazygui/services/local_backend.py:38` `def __init__(self, constants, paths, parent)` -- Initialise the backend with the shared constants and paths.
- `LocalPtyBackend.start` (method) `lazygui/services/local_backend.py:62` `def start(self)` -- Fork-exec the cmd2 console behind a PTY.
- `LocalPtyBackend.stop` (method) `lazygui/services/local_backend.py:87` `def stop(self)` -- Send ``SIGTERM`` to the child and tear down notifiers.
- `LocalPtyBackend.send_command` (method) `lazygui/services/local_backend.py:112` `def send_command(self, command, target_session)` -- Write ``command`` followed by a newline to the PTY.
- `LocalPtyBackend.refresh` (method) `lazygui/services/local_backend.py:117` `def refresh(self)` -- No-op for the local backend; the operator drives data from cmd2.
- `LocalPtyBackend.resize_terminal` (method) `lazygui/services/local_backend.py:121` `def resize_terminal(self, columns, rows)` -- Propagate the new size to the PTY using ``TIOCSWINSZ``.
- `LocalPtyBackend.feed_terminal_input` (method) `lazygui/services/local_backend.py:127` `def feed_terminal_input(self, data)` -- Encode ``data`` and write it to the master end of the PTY.
- `LocalPtyBackend.known_sessions` (method) `lazygui/services/local_backend.py:137` `def known_sessions(self)` -- Local backend does not enumerate sessions.
- `LocalPtyBackend.known_listeners` (method) `lazygui/services/local_backend.py:141` `def known_listeners(self)` -- Local backend does not enumerate listeners.
- `LocalPtyBackend.announce_local_operator` (method) `lazygui/services/local_backend.py:249` `def announce_local_operator(self)` -- Emit a synthetic :class:`Operator` describing the local user.

## lazygui/services/models.py
Depends on: `cli/commands/enum.py`
Imported by: `lazygui/app.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/sessions_panel.py`, `lazygui/services/__init__.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/widgets/beacon_command_modal.py`, `lazygui/widgets/event_log_view.py`, `lazygui/widgets/graph_view.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`, `tests/test_lazygui_backend.py`, `tests/test_lazygui_graph_widget.py`, `tests/test_lazygui_models.py`
- `EventLevel.numeric` (method) `lazygui/services/models.py:34` `def numeric(self)` -- Numeric rank used to compare severity.
- `EventRecord.now` (method) `lazygui/services/models.py:96` `def now(cls, level, source, message)` -- Construct a record stamped with the current UTC time.
- `Topology.empty` (method) `lazygui/services/models.py:133` `def empty(cls)` -- Return an empty topology.

## lazygui/services/teamserver_backend.py
Depends on: `core/logging.py`, `lazyc2/blueprints/auth.py`, `lazygui/config/constants.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`
Imported by: `lazygui/app.py`, `lazygui/services/__init__.py`, `lazygui/services/factory.py`, `lazygui/windows/connect_dialog.py`, `tests/test_lazygui_backend.py`
- `TeamserverBackend.__init__` (method) `lazygui/services/teamserver_backend.py:51` `def __init__(self, constants, credentials, parent)` -- Store ``credentials`` and prepare polling timers and Socket.IO client.
- `TeamserverBackend.start` (method) `lazygui/services/teamserver_backend.py:80` `def start(self)` -- Begin polling and establish Socket.IO connection.
- `TeamserverBackend.stop` (method) `lazygui/services/teamserver_backend.py:97` `def stop(self)` -- Tear down all timers and Socket.IO connection.
- `TeamserverBackend.send_command` (method) `lazygui/services/teamserver_backend.py:112` `def send_command(self, command, target_session)` -- Submit ``command`` via Socket.IO PTY (global) or ``/issue_command`` (beacon).
- `TeamserverBackend.refresh` (method) `lazygui/services/teamserver_backend.py:124` `def refresh(self)` -- Pull consolidated state JSON and emit derived signals.
- `TeamserverBackend.resize_terminal` (method) `lazygui/services/teamserver_backend.py:139` `def resize_terminal(self, columns, rows)` -- Forward resize to Socket.IO PTY namespace when connected.
- `TeamserverBackend.feed_terminal_input` (method) `lazygui/services/teamserver_backend.py:151` `def feed_terminal_input(self, data)` -- Feed keystrokes to the PTY via Socket.IO, falling back to HTTP commands.
- `TeamserverBackend.known_sessions` (method) `lazygui/services/teamserver_backend.py:169` `def known_sessions(self)` -- Most recent snapshot delivered by the last poll.
- `TeamserverBackend.known_listeners` (method) `lazygui/services/teamserver_backend.py:173` `def known_listeners(self)` -- Most recent snapshot delivered by the last poll.
- `TeamserverBackend.known_topology` (method) `lazygui/services/teamserver_backend.py:177` `def known_topology(self)` -- Most recent graph topology snapshot.
- `TeamserverBackend.known_campaigns` (method) `lazygui/services/teamserver_backend.py:181` `def known_campaigns(self)` -- Most recent campaign snapshot.
- `TeamserverBackend.request_beacon_results` (method) `lazygui/services/teamserver_backend.py:185` `def request_beacon_results(self, client_id)` -- Fetch stored command results for a specific beacon.
- `TeamserverBackend.request_world_model` (method) `lazygui/services/teamserver_backend.py:210` `def request_world_model(self)` -- Fetch the unified kill-chain snapshot from the teamserver REST API.
- `TeamserverBackend.request_beacon_history` (method) `lazygui/services/teamserver_backend.py:224` `def request_beacon_history(self, client_id)` -- Fetch the persistent ordered command/result history for a beacon.

## lazygui/theme/manager.py
Depends on: `core/logging.py`, `lazygui/config/constants.py`, `lazygui/config/settings.py`, `lazygui/theme/palettes/__init__.py`, `lazygui/theme/qss_builder.py`, `lazygui/theme/tokens.py`
Imported by: `lazygui/app.py`, `lazygui/theme/__init__.py`, `lazygui/windows/main_window.py`
- `ThemeManager.__init__` (method) `lazygui/theme/manager.py:31` `def __init__(self, constants, settings, application, palettes, parent)` -- Initialise the manager.
- `ThemeManager.active_tokens` (method) `lazygui/theme/manager.py:57` `def active_tokens(self)` -- Currently active :class:`ThemeTokens`.
- `ThemeManager.active_id` (method) `lazygui/theme/manager.py:64` `def active_id(self)` -- Identifier of the active palette.
- `ThemeManager.available` (method) `lazygui/theme/manager.py:68` `def available(self)` -- Yield all registered palettes in registration order.
- `ThemeManager.apply_initial` (method) `lazygui/theme/manager.py:72` `def apply_initial(self)` -- Load the saved theme identifier and apply it.
- `ThemeManager.apply` (method) `lazygui/theme/manager.py:80` `def apply(self, identifier)` -- Activate the palette with ``identifier`` and persist the choice.
- `ThemeManager.cycle` (method) `lazygui/theme/manager.py:93` `def cycle(self)` -- Switch to the next palette, wrapping at the end of the registry.

## lazygui/theme/palettes/__init__.py
Depends on: `lazygui/theme/tokens.py`
Imported by: `lazygui/theme/manager.py`
- `builtin_palettes` (function) `lazygui/theme/palettes/__init__.py:23` `def builtin_palettes()` -- Return the built-in palette registry as ``id -> tokens``.

## lazygui/theme/qss_builder.py
Depends on: `lazygui/config/constants.py`, `lazygui/theme/tokens.py`
Imported by: `lazygui/theme/__init__.py`, `lazygui/theme/manager.py`
- `QssBuilder.build` (method) `lazygui/theme/qss_builder.py:21` `def build(self, tokens)` -- Return the full QSS sheet for ``tokens``.

## lazygui/widgets/beacon_command_modal.py
Depends on: `lazygui/services/backend.py`, `lazygui/services/models.py`
Imported by: `lazygui/windows/main_window.py`
- `BeaconCommandModal.__init__` (method) `lazygui/widgets/beacon_command_modal.py:53` `def __init__(self, backend, parent)` -- Initialise the modal with a backend reference.
- `BeaconCommandModal.open` (method) `lazygui/widgets/beacon_command_modal.py:216` `def open(self)` -- Populate sessions before showing.
- `BeaconCommandModal.focus_input` (method) `lazygui/widgets/beacon_command_modal.py:227` `def focus_input(self)` -- Move keyboard focus to the command input.

## lazygui/widgets/command_palette_list.py
Depends on: `lazygui/config/constants.py`
Imported by: `lazygui/widgets/__init__.py`, `lazygui/windows/command_palette_window.py`, `lazygui/windows/main_window.py`
- `CommandPaletteList.__init__` (method) `lazygui/widgets/command_palette_list.py:33` `def __init__(self, constants, actions, parent)` -- Store the action set and prepare the underlying model.
- `CommandPaletteList.set_actions` (method) `lazygui/widgets/command_palette_list.py:53` `def set_actions(self, actions)` -- Replace the entire action registry and reset the filter.
- `CommandPaletteList.apply_filter` (method) `lazygui/widgets/command_palette_list.py:58` `def apply_filter(self, query)` -- Filter the action set using a substring + token-order heuristic.
- `CommandPaletteList.invoke_current` (method) `lazygui/widgets/command_palette_list.py:76` `def invoke_current(self)` -- Invoke whichever action is currently highlighted, if any.

## lazygui/widgets/event_log_view.py
Depends on: `lazygui/config/constants.py`, `lazygui/services/event_log.py`, `lazygui/services/models.py`
Imported by: `lazygui/panels/event_log_panel.py`, `lazygui/widgets/__init__.py`
- `EventLogView.__init__` (method) `lazygui/widgets/event_log_view.py:23` `def __init__(self, constants, event_log, parent)` -- Bind the view to ``event_log`` and configure columns/headers.
- `EventLogView.set_minimum_level` (method) `lazygui/widgets/event_log_view.py:51` `def set_minimum_level(self, level)` -- Filter view to records of severity >= ``level`` and reload.
- `EventLogView.minimum_level` (method) `lazygui/widgets/event_log_view.py:61` `def minimum_level(self)` -- Currently active severity filter.

## lazygui/widgets/filter_bar.py
Depends on: `lazygui/config/constants.py`
Imported by: `lazygui/panels/listeners_panel.py`, `lazygui/panels/sessions_panel.py`, `lazygui/widgets/__init__.py`
- `FilterBar.__init__` (method) `lazygui/widgets/filter_bar.py:16` `def __init__(self, constants, placeholder_text, label_text, parent)` -- Lay out a label + line edit and wire up debounce timing.
- `FilterBar.text` (method) `lazygui/widgets/filter_bar.py:42` `def text(self)` -- Current filter text.
- `FilterBar.clear` (method) `lazygui/widgets/filter_bar.py:46` `def clear(self)` -- Reset the filter to an empty string.

## lazygui/widgets/graph_view.py
Depends on: `lazygui/config/constants.py`, `lazygui/services/models.py`
Imported by: `lazygui/panels/graph_panel.py`, `lazygui/widgets/__init__.py`, `tests/test_lazygui_graph_widget.py`
- `GraphNodeItem.__init__` (method) `lazygui/widgets/graph_view.py:143` `def __init__(self, node, radius, color, pixmap, on_selected, on_context_menu, label_visible, parent)`
- `GraphNodeItem.node_data` (method) `lazygui/widgets/graph_view.py:186` `def node_data(self)` -- Return the immutable node data associated with this item.
- `GraphNodeItem.paint` (method) `lazygui/widgets/graph_view.py:190` `def paint(self, painter, option, widget)`
- `GraphNodeItem.mousePressEvent` (method) `lazygui/widgets/graph_view.py:248` `def mousePressEvent(self, event)`
- `GraphNodeItem.mouseReleaseEvent` (method) `lazygui/widgets/graph_view.py:259` `def mouseReleaseEvent(self, event)`
- `GraphNodeItem.hoverEnterEvent` (method) `lazygui/widgets/graph_view.py:266` `def hoverEnterEvent(self, event)`
- `GraphNodeItem.hoverLeaveEvent` (method) `lazygui/widgets/graph_view.py:273` `def hoverLeaveEvent(self, event)`
- `GraphNodeItem.itemChange` (method) `lazygui/widgets/graph_view.py:279` `def itemChange(self, change, value)`
- `GraphEdgeItem.__init__` (method) `lazygui/widgets/graph_view.py:288` `def __init__(self, edge, source_item, target_item, parent)`
- `GraphEdgeItem.update_position` (method) `lazygui/widgets/graph_view.py:324` `def update_position(self)` -- Recalculate the line endpoints from source and target positions.
- `GraphEdgeItem.edge_data` (method) `lazygui/widgets/graph_view.py:329` `def edge_data(self)` -- Return the immutable edge data.
- `GraphScene.__init__` (method) `lazygui/widgets/graph_view.py:340` `def __init__(self, constants, parent)`
- `GraphScene.set_topology` (method) `lazygui/widgets/graph_view.py:349` `def set_topology(self, topology)` -- Replace the current graph with a new topology using force layout.
- `GraphScene.step_physics` (method) `lazygui/widgets/graph_view.py:419` `def step_physics(self)` -- Run one iteration of force-directed layout.
- `GraphScene.selected_node_id` (method) `lazygui/widgets/graph_view.py:491` `def selected_node_id(self)` -- Return the identifier of the first selected node, or None.
- `GraphView.__init__` (method) `lazygui/widgets/graph_view.py:509` `def __init__(self, constants, parent)`
- `GraphView.set_theme_colors` (method) `lazygui/widgets/graph_view.py:527` `def set_theme_colors(self, bg_color, edge_color)` -- Update graph background and default edge colour from theme tokens.
- `GraphView.set_topology` (method) `lazygui/widgets/graph_view.py:535` `def set_topology(self, topology)` -- Render a new graph topology.
- `GraphView.wheelEvent` (method) `lazygui/widgets/graph_view.py:551` `def wheelEvent(self, event)`
- `GraphView.selected_node_id` (method) `lazygui/widgets/graph_view.py:561` `def selected_node_id(self)` -- Return the identifier of the currently selected node.
- `GraphView.fit_to_content` (method) `lazygui/widgets/graph_view.py:565` `def fit_to_content(self)` -- Zoom to fit all graph content.
- `GraphView.scene_handle` (method) `lazygui/widgets/graph_view.py:570` `def scene_handle(self)` -- Return the underlying graph scene.


Next: [API_p9.md](API_p9.md)
