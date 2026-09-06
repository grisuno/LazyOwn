# Subsystem: blueprints

## lazyc2/blueprints/__init__.py
- Layer: utility
- Language: py
- Depends on: `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/api.py`, `lazyc2/blueprints/auth.py`, `lazyc2/blueprints/beacon.py`, `lazyc2/blueprints/operations.py`, `lazyc2/blueprints/phishing.py`
- Imported by: `lazyc2.py`, `lazyc2/app_factory.py`

## lazyc2/blueprints/addons.py
- Layer: presentation
- Language: py
- Symbols:
  - `init_addons_bp` (function, line 66) `def init_addons_bp(base_dir)`
  - `_store` (function, line 78) `def _store()`
  - `_csrf_policy` (function, line 84) `def _csrf_policy()`
  - `csrf_protect` (function, line 93) `def csrf_protect(view)`
  - `_issue_csrf` (function, line 117) `def _issue_csrf(response, policy)`
  - `_issue_map` (function, line 146) `def _issue_map(issues)`
  - `_form_context` (function, line 161) `def _form_context(draft, issues)`
  - `_render_create` (function, line 190) `def _render_create(draft, issues)`
  - `_draft_from_document` (function, line 213) `def _draft_from_document(document)`
  - `list_addons` (function, line 260) `def list_addons()`
  - `create_addon` (function, line 274) `def create_addon()`
  - `view_addon` (function, line 317) `def view_addon(name)`
  - `delete_addon` (function, line 341) `def delete_addon(name)`
  - `wrapper` (function, line 107) `def wrapper()`
- Depends on: `lazyc2/addon_creator.py`, `lazyc2/blueprints/session_auth.py`, `lazyc2/extensions/decoy.py`, `lazyc2/security/csrf.py`
- Imported by: `lazyc2/blueprints/__init__.py`, `mutants/tests/test_addon_creator.py`, `tests/test_addon_creator.py`, `tests/test_security_hardening_v5.py`

## lazyc2/blueprints/api.py
- Layer: presentation
- Language: py
- Symbols:
  - `HealthConfig` (class, line 25) `class HealthConfig`
  - `_health_status` (method, line 36) `def _health_status(config)`
  - `_listener_alive` (method, line 99) `def _listener_alive(listener)`
  - `health` (method, line 108) `def health()`
  - `ping` (method, line 120) `def ping()`
  - `require_api_auth_with_store` (method, line 129) `def require_api_auth_with_store(view)`
  - `health_tenant` (method, line 157) `def health_tenant()`
  - `guarded` (method, line 146) `def guarded()`
- Depends on: `core/api_authz.py`, `core/logging.py`
- Imported by: `lazyc2/blueprints/__init__.py`, `tests/test_security_hardening_v5.py`

## lazyc2/blueprints/auth.py
- Layer: presentation
- Language: py
- Symbols:
  - `_rbac_available` (function, line 51) `def _rbac_available()`
  - `_get_rbac_store` (function, line 56) `def _get_rbac_store()`
  - `_get_rbac_user_obj` (function, line 68) `def _get_rbac_user_obj(flask_user)`
  - `_get_tenant_manager` (function, line 78) `def _get_tenant_manager()`
  - `register` (function, line 92) `def register()`
  - `login` (function, line 151) `def login()`
  - `mfa_setup` (function, line 196) `def mfa_setup()`
  - `mfa_qr` (function, line 269) `def mfa_qr(username)`
  - `mfa_verify` (function, line 291) `def mfa_verify()`
  - `profile` (function, line 335) `def profile()`
  - `logout` (function, line 360) `def logout()`
  - `admin_users` (function, line 379) `def admin_users()`
  - `admin_set_role` (function, line 396) `def admin_set_role(user_id)`
  - `admin_reset_mfa` (function, line 418) `def admin_reset_mfa(user_id)`
  - `admin_delete_user` (function, line 430) `def admin_delete_user(user_id)`
  - `admin_tenants` (function, line 448) `def admin_tenants()`
  - `admin_create_tenant` (function, line 468) `def admin_create_tenant()`
  - `admin_switch_tenant` (function, line 486) `def admin_switch_tenant(tenant_id)`
  - `require_role` (function, line 33) `def require_role(role)`
- Depends on: `lazyc2.py`, `lazyc2/extensions/decoy.py`, `lazyc2/extensions/users.py`, `modules/lazy_rbac.py`
- Imported by: `lazyc2/blueprints/__init__.py`, `lazygui/services/teamserver_backend.py`, `static/js/socket.io-4.0.0.min.js`, `static/js/socket.io-4.3.2.min.js`

## lazyc2/blueprints/beacon.py
- Layer: presentation
- Language: py
- Symbols:
  - `init_beacon_bp` (function, line 35) `def init_beacon_bp(commands, results, commands_history, connected_clients, encrypt_fn, decrypt_fn, config, sessions_dir, route_malleable)`
  - `_fire_hooks` (function, line 72) `def _fire_hooks(event, context)`
  - `_trigger_cred_reuse` (function, line 88) `def _trigger_cred_reuse(context)`
  - `send_command` (function, line 108) `def send_command(client_id)`
  - `receive_result` (function, line 128) `def receive_result(client_id)`
  - `issue_command` (function, line 214) `def issue_command()`
  - `_run` (function, line 94) `def _run()`
- Depends on: `core/logging.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/state_manager.py`
- Imported by: `lazyc2/blueprints/__init__.py`

## lazyc2/blueprints/operations.py
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

## lazyc2/blueprints/phishing.py
- Layer: presentation
- Language: py
- Symbols:
  - `_get_config` (function, line 41) `def _get_config(key, default)`
  - `create_short_url` (function, line 47) `def create_short_url()`
  - `track_interaction` (function, line 87) `def track_interaction(short_url)`
  - `update_short_url` (function, line 121) `def update_short_url(short_url)`
  - `redirect_to_file` (function, line 147) `def redirect_to_file(short_url)`
  - `webserver_report` (function, line 170) `def webserver_report(filename)`
  - `download_files` (function, line 188) `def download_files(filename)`
- Depends on: `core/logging.py`, `lazyc2/extensions/short_urls.py`, `modules/security_sanitizers.py`, `utils.py`
- Imported by: `lazyc2/blueprints/__init__.py`

## lazyc2/blueprints/session_auth.py
- Layer: presentation
- Language: py
- Symbols:
  - `require_operator_session` (function, line 20) `def require_operator_session(blueprint, login_endpoint)`
  - `_guard` (function, line 35) `def _guard()`
- Imported by: `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/operations.py`
