# Subsystem: blueprints

## lazyc2/blueprints/__init__.py
- Doc: Flask Blueprints for lazydown C2.
- Layer: utility
- Language: py
- Depends on: `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/api.py`, `lazyc2/blueprints/api_v1.py`, `lazyc2/blueprints/auth.py`, `lazyc2/blueprints/beacon.py`, `lazyc2/blueprints/operations.py`, `lazyc2/blueprints/phishing.py`
- Imported by: `lazyc2.py`, `lazyc2/app_factory.py`, `tests/test_security_codeql_batch.py`

## lazyc2/blueprints/addons.py
- Doc: LazyAddon creator blueprint for the C2 dashboard.
- Layer: presentation
- Language: py
- Symbols:
  - `init_addons_bp` (function, line 69) `def init_addons_bp(base_dir)`
  - `_store` (function, line 81) `def _store()`
  - `_csrf_policy` (function, line 87) `def _csrf_policy()`
  - `csrf_protect` (function, line 96) `def csrf_protect(view)`
  - `_issue_csrf` (function, line 120) `def _issue_csrf(response, policy)`
  - `_issue_map` (function, line 149) `def _issue_map(issues)`
  - `_form_context` (function, line 164) `def _form_context(draft, issues)`
  - `_render_create` (function, line 193) `def _render_create(draft, issues)`
  - `_draft_from_document` (function, line 216) `def _draft_from_document(document)`
  - `list_addons` (function, line 263) `def list_addons()`
  - `create_addon` (function, line 277) `def create_addon()`
  - `view_addon` (function, line 321) `def view_addon(name)`
  - `delete_addon` (function, line 345) `def delete_addon(name)`
  - `wrapper` (function, line 110) `def wrapper()`
- Depends on: `core/logging.py`, `lazyc2/addon_creator.py`, `lazyc2/blueprints/session_auth.py`, `lazyc2/extensions/decoy.py`, `lazyc2/security/csrf.py`
- Imported by: `lazyc2/blueprints/__init__.py`, `tests/test_addon_creator.py`, `tests/test_security_hardening_v5.py`

## lazyc2/blueprints/api.py
- Doc: API blueprint for the LazyOwn C2 server.
- Layer: presentation
- Language: py
- Symbols:
  - `HealthConfig` (class, line 25) `class HealthConfig`
  - `_health_status` (function, line 36) `def _health_status(config)`
  - `_listener_alive` (function, line 99) `def _listener_alive(listener)`
  - `health` (function, line 108) `def health()`
  - `ping` (function, line 120) `def ping()`
  - `require_api_auth_with_store` (function, line 129) `def require_api_auth_with_store(view)`
  - `health_tenant` (function, line 157) `def health_tenant()`
  - `get_defaults` (function, line 182) `def get_defaults()`
  - `set_default` (function, line 211) `def set_default()`
  - `guarded` (function, line 146) `def guarded()`
- Depends on: `core/api_authz.py`, `core/config.py`, `core/defaults.py`, `core/logging.py`
- Imported by: `lazyc2/blueprints/__init__.py`, `lazyc2/blueprints/api_v1.py`, `lazyc2/blueprints/orchestrator.py`, `tests/test_core_defaults.py`, `tests/test_security_hardening_v5.py`

## lazyc2/blueprints/api_v1.py
- Doc: Versioned REST API (``/api/v1``) for the LazyOwn C2 server.
- Layer: presentation
- Language: py
- Symbols:
  - `_sessions_dir` (function, line 38) `def _sessions_dir()`
  - `_db` (function, line 43) `def _db()`
  - `_error` (function, line 60) `def _error(message, status)`
  - `health` (function, line 65) `def health()`
  - `targets` (function, line 76) `def targets()`
  - `results` (function, line 108) `def results()`
  - `campaigns` (function, line 141) `def campaigns()`
  - `_webhooks_path` (function, line 166) `def _webhooks_path()`
  - `_read_webhooks` (function, line 170) `def _read_webhooks()`
  - `webhooks_list` (function, line 180) `def webhooks_list()`
  - `webhooks_register` (function, line 191) `def webhooks_register()`
  - `webhooks_delete` (function, line 228) `def webhooks_delete(index)`
- Depends on: `core/logging.py`, `core/safe_exec.py`, `lazyc2/blueprints/api.py`, `modules/beacon_history.py`, `modules/db.py`
- Imported by: `lazyc2/blueprints/__init__.py`, `tests/test_api_v1.py`

## lazyc2/blueprints/auth.py
- Doc: Authentication and authorisation blueprint for the LazyOwn C2 server.
- Layer: presentation
- Language: py
- Symbols:
  - `_rbac_available` (function, line 87) `def _rbac_available()`
  - `_get_rbac_store` (function, line 92) `def _get_rbac_store()`
  - `_get_rbac_user_obj` (function, line 104) `def _get_rbac_user_obj(flask_user)`
  - `_get_tenant_manager` (function, line 114) `def _get_tenant_manager()`
  - `register` (function, line 128) `def register()`
  - `login` (function, line 187) `def login()`
  - `mfa_setup` (function, line 237) `def mfa_setup()`
  - `mfa_qr` (function, line 310) `def mfa_qr(username)`
  - `mfa_verify` (function, line 332) `def mfa_verify()`
  - `profile` (function, line 383) `def profile()`
  - `logout` (function, line 408) `def logout()`
  - `admin_users` (function, line 428) `def admin_users()`
  - `admin_set_role` (function, line 445) `def admin_set_role(user_id)`
  - `admin_reset_mfa` (function, line 467) `def admin_reset_mfa(user_id)`
  - `admin_delete_user` (function, line 479) `def admin_delete_user(user_id)`
  - `admin_tenants` (function, line 497) `def admin_tenants()`
  - `admin_create_tenant` (function, line 517) `def admin_create_tenant()`
  - `admin_switch_tenant` (function, line 536) `def admin_switch_tenant(tenant_id)`
  - `_complete_login` (function, line 349) `def _complete_login()`
  - `Role` (class, line 38) `class Role(Enum)`
  - `require_role` (function, line 59) `def require_role(role)`
  - `valid_roles` (method, line 51) `def valid_roles(cls)`
  - `decorator` (function, line 69) `def decorator(view)`
  - `wrapper` (function, line 71) `def wrapper()`
- Depends on: `cli/commands/enum.py`, `core/logging.py`, `lazyc2/__init__.py`, `lazyc2/extensions/decoy.py`, `lazyc2/extensions/users.py`, `modules/lazy_rbac.py`
- Imported by: `lazyc2/blueprints/__init__.py`, `lazygui/services/teamserver_backend.py`, `static/js/socket.io-4.0.0.min.js`, `static/js/socket.io-4.3.2.min.js`

## lazyc2/blueprints/beacon.py
- Doc: Beacon communication blueprint for the LazyOwn C2 server.
- Layer: presentation
- Language: py
- Symbols:
  - `init_beacon_bp` (function, line 35) `def init_beacon_bp(commands, results, commands_history, connected_clients, encrypt_fn, decrypt_fn, config...`
  - `_fire_hooks` (function, line 72) `def _fire_hooks(event, context)`
  - `_trigger_cred_reuse` (function, line 91) `def _trigger_cred_reuse(context)`
  - `send_command` (function, line 111) `def send_command(client_id)`
  - `receive_result` (function, line 131) `def receive_result(client_id)`
  - `issue_command` (function, line 245) `def issue_command()`
  - `_run` (function, line 97) `def _run()`
- Depends on: `core/logging.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/state_manager.py`
- Imported by: `lazyc2/blueprints/__init__.py`

## lazyc2/blueprints/operations.py
- Doc: Operations blueprint — tasks, CVEs, notes, and event management.
- Layer: presentation
- Language: py
- Symbols:
  - `task_detail` (function, line 33) `def task_detail(task_id)`
  - `get_tasks` (function, line 48) `def get_tasks()`
  - `tasks` (function, line 57) `def tasks()`
  - `edit_task` (function, line 66) `def edit_task(task_id)`
  - `cves` (function, line 92) `def cves()`
  - `cve_detail` (function, line 117) `def cve_detail(cve_id)`
  - `edit_cve` (function, line 132) `def edit_cve(cve_id)`
  - `edit_notes` (function, line 158) `def edit_notes()`
  - `get_notes` (function, line 173) `def get_notes()`
  - `view_note` (function, line 182) `def view_note()`
  - `event_config` (function, line 192) `def event_config()`
  - `event_config_view` (function, line 198) `def event_config_view()`
  - `events` (function, line 218) `def events()`
- Depends on: `lazyc2/blueprints/session_auth.py`, `lazyc2/extensions/decoy.py`, `lazyc2/extensions/storage.py`
- Imported by: `lazyc2/blueprints/__init__.py`

## lazyc2/blueprints/orchestrator.py
- Doc: Orchestrator REST + web panel for the LazyOwn C2 dashboard.
- Layer: presentation
- Language: py
- Symbols:
  - `_error` (function, line 56) `def _error(message, status)`
  - `_namespaced_path` (function, line 61) `def _namespaced_path(name)`
  - `_world_snapshot` (function, line 66) `def _world_snapshot()`
  - `_status_payload` (function, line 88) `def _status_payload()`
  - `status` (function, line 104) `def status()`
  - `world` (function, line 111) `def world()`
  - `verbs` (function, line 125) `def verbs()`
  - `_read_body_name` (function, line 141) `def _read_body_name()`
  - `verbs_toggle` (function, line 149) `def verbs_toggle()`
  - `stages_toggle` (function, line 166) `def stages_toggle()`
  - `stage_names` (function, line 180) `def stage_names()`
  - `triggers` (function, line 193) `def triggers()`
  - `triggers_add` (function, line 202) `def triggers_add()`
  - `triggers_seed` (function, line 222) `def triggers_seed()`
  - `triggers_delete` (function, line 231) `def triggers_delete(trigger_id)`
  - `panel` (function, line 242) `def panel()`
  - `panel_json` (function, line 262) `def panel_json()`
- Depends on: `core/logging.py`, `lazyc2/blueprints/api.py`, `modules/__init__.py`, `modules/killchain.py`, `modules/loop_triggers.py`, `modules/orchestrator_config.py`, `modules/trigger_policy.py`, `modules/verb_catalog.py`, `modules/world_model.py`
- Imported by: `lazyc2/app_factory.py`, `tests/test_orchestrator_api.py`

## lazyc2/blueprints/phishing.py
- Doc: Phishing blueprint for the LazyOwn C2 server.
- Layer: presentation
- Language: py
- Symbols:
  - `_get_config` (function, line 43) `def _get_config(key, default)`
  - `create_short_url` (function, line 49) `def create_short_url()`
  - `track_interaction` (function, line 89) `def track_interaction(short_url)`
  - `update_short_url` (function, line 125) `def update_short_url(short_url)`
  - `redirect_to_file` (function, line 151) `def redirect_to_file(short_url)`
  - `webserver_report` (function, line 174) `def webserver_report(filename)`
  - `download_files` (function, line 192) `def download_files(filename)`
- Depends on: `core/logging.py`, `lazyc2/extensions/short_urls.py`, `lazyc2/security/validators.py`, `modules/security_sanitizers.py`, `utils.py`
- Imported by: `lazyc2/blueprints/__init__.py`

## lazyc2/blueprints/session_auth.py
- Doc: Session-based authentication gate for operator dashboard blueprints.
- Layer: presentation
- Language: py
- Symbols:
  - `require_operator_session` (function, line 20) `def require_operator_session(blueprint, login_endpoint)`
  - `_guard` (function, line 36) `def _guard()`
- Imported by: `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/operations.py`
