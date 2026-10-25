# lazyc2/security

*Community 6 | 52 files | cohesion 0.47*

## Definition

This community groups 52 file(s) rooted at `tests` with dominant language py (cohesion 0.47). Central symbols: `AESKeyManager`, `AutoRecommender`, `AutomationCommandSet`, `CSRFPolicy`, `CollabBusSink`, `CommandAllowlist`, `CommandDecision`, `CommandRejectionReason`. Core file: `lazyc2.py` (292 symbols). Documented purpose: Automation command set — credential reuse, conditional hooks, operator profiles.  Provides CLI commands for managing the credential reuse engine, conditional ho.

## Files

### `tests` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_command_allowlist.py` | py | testing | 14 | yes |
| `tests/test_command_allowlist_behavior.py` | py | testing | 3 | yes |

### `lazyc2/security` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |
| `lazyc2/security/constants.py` | py | utility | 0 | yes |

### `modules` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/conditional_hooks.py` | py | utility | 23 | yes |
| `modules/credential_reuse.py` | py | utility | 16 | yes |

### `lazyc2/blueprints` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `lazyc2/extensions` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `lazyc2` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |
| `lazyc2/app_factory.py` | py | presentation | 12 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |
| `static/js/socket.io-4.3.2.min.js` | js | utility | 15 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 292 | no |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |

### `modules/sinks` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/event_bus.py` | py | infrastructure | 1 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

*... and 32 more files in this community.*


## Key Symbols

- `AutomationCommandSet` (class, `cli/commands/automation.py:17`) `class AutomationCommandSet(LazyOwnCommandSet)` - Automation & operator workflow commands.
- `do_cred_reuse` (method, `cli/commands/automation.py:24`) `def do_cred_reuse(self, line)` - Analyze captured credentials and suggest spray targets.
- `do_cred_mark_failed` (method, `cli/commands/automation.py:57`) `def do_cred_mark_failed(self, line)` - Mark a credential as failed against a host.
- `do_hooks_list` (method, `cli/commands/automation.py:78`) `def do_hooks_list(self, line)` - List all conditional hook rules.
- `do_hooks_enable` (method, `cli/commands/automation.py:101`) `def do_hooks_enable(self, line)` - Enable or disable a hook rule.
- `do_hooks_add` (method, `cli/commands/automation.py:129`) `def do_hooks_add(self, line)` - Add a new conditional hook rule (JSON string).
- `do_hooks_remove` (method, `cli/commands/automation.py:150`) `def do_hooks_remove(self, line)` - Remove a hook rule by name.
- `do_hooks_fire` (method, `cli/commands/automation.py:172`) `def do_hooks_fire(self, line)` - Manually fire a hook event for testing.
- `do_operators` (method, `cli/commands/automation.py:202`) `def do_operators(self, line)` - List all operator profiles.
- `do_operator_create` (method, `cli/commands/automation.py:229`) `def do_operator_create(self, line)` - Create a new operator profile.
- `do_operator_load` (method, `cli/commands/automation.py:264`) `def do_operator_load(self, line)` - Load effective config for an operator (team baseline + overrides).
- `do_operator_delete` (method, `cli/commands/automation.py:292`) `def do_operator_delete(self, line)` - Delete an operator profile.
- `do_hooks` (method, `cli/commands/automation.py:314`) `def do_hooks(self, line)` - Conditional hooks management — list, enable, disable, add, remove rules.
- `_env_tag` (function, `lazyc2.py:192`) `def _env_tag()` - Return the runtime environment tag from ``payload.json``.
- `is_insecure_credential` (function, `lazyc2.py:204`) `def is_insecure_credential(user, pwd)` - Check for weak or default credentials
- `_listen_address` (function, `lazyc2.py:252`) `def _listen_address()` - Return the bind address chosen by :class:`BindAddressResolver`.
- `_is_unspecified_bind_literal` (function, `lazyc2.py:279`) `def _is_unspecified_bind_literal(address)` - Return True when ``address`` is a wildcard bind literal.
- `_select_specific_bind_address` (function, `lazyc2.py:298`) `def _select_specific_bind_address(candidate)` - Return a specific IP literal safe to pass to ``socket.bind``.
- `_probe_bind` (function, `lazyc2.py:331`) `def _probe_bind(address, port, sock_type)` - Probe whether ``(address, port)`` can be bound for ``sock_type``.
- `_resolve_bind_address` (function, `lazyc2.py:376`) `def _resolve_bind_address(preferred, port, sock_type)` - Return an address that can actually be bound to on this host.
- `_JsonLogFormatter` (class, `lazyc2.py:441`) `class _JsonLogFormatter(Formatter)` - Optional structured JSON formatter for C2 access logs.
- `format` (method, `lazyc2.py:444`) `def format(self, record)`
- `ensure_sessions_dir` (function, `lazyc2.py:471`) `def ensure_sessions_dir()` - Ensure the sessions directory exists with safe permissions.
- `load_routes` (function, `lazyc2.py:482`) `def load_routes()` - Load dynamic routes from JSON file.
- `save_routes` (function, `lazyc2.py:492`) `def save_routes(routes)` - Save dynamic routes to JSON file with safe permissions.
- `validate_route_path` (function, `lazyc2.py:506`) `def validate_route_path(route_path)` - Module-level boolean adapter for :func:`lazyc2.security.validators.validate_route_path`.
- `validate_template_name` (function, `lazyc2.py:519`) `def validate_template_name(template_name)` - Module-level boolean adapter for :func:`lazyc2.security.validators.validate_template_name`.
- `is_safe_template_path` (function, `lazyc2.py:529`) `def is_safe_template_path(template_path, template_name)` - Verify ``template_path`` resolves inside ``app.template_folder``.
- `_sanitize_command_output` (function, `lazyc2.py:559`) `def _sanitize_command_output(value)` - Return a JSON-safe projection of ``value`` without exception details.
- `is_binary` (function, `lazyc2.py:569`) `def is_binary(safe_filename)` - Check whether a session file is binary based on its header bytes.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 114
- Cross-boundary resolved imports (EXTRACTED): 138

## Connections

- [EXTRACTED] depends_on community 6 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_core_modules.py` (testing) -> `modules/dashboard_bp.py` (presentation)
- [layer strict] `tests/test_dashboard_routes.py` (testing) -> `modules/dashboard_bp.py` (presentation)
- [layer strict] `tests/test_dashboard_routes.py` (testing) -> `modules/dashboard_bp.py` (presentation)
- [layer strict] `tests/test_dashboard_routes.py` (testing) -> `modules/dashboard_bp.py` (presentation)
- [layer strict] `tests/test_dashboard_routes.py` (testing) -> `modules/dashboard_bp.py` (presentation)
- [layer strict] `tests/test_https_redirect.py` (testing) -> `lazyc2/security/https_redirect.py` (presentation)
- [layer strict] `tests/test_security_hardening_v5.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `lazyc2.py:361` `_probe_bind` `probe`: Result of allocator stored in `probe` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `lazyc2.py:1981` `tcp_bridge` `server_socket`: Result of allocator stored in `server_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `lazyc2.py:7068` `start_reverse_shell` `server_socket`: Result of allocator stored in `server_socket` is never checked against NULL.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `lazyc2.py`)? What purpose do they serve?
- What would break if the most connected file in lazyc2/security changed?
- Should lazyc2/security be split, given cohesion 0.47?

## Sources

- `cli/commands/automation.py`
- `lazyc2.py`
- `lazyc2/__init__.py`
- `lazyc2/app_factory.py`
- `lazyc2/blueprints/__init__.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/auth.py`
- `lazyc2/blueprints/beacon.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/session_auth.py`
- `lazyc2/extensions/__init__.py`
- `lazyc2/extensions/decoy.py`
- `lazyc2/extensions/storage.py`
- `lazyc2/extensions/users.py`
- `lazyc2/models.py`
- `lazyc2/security/__init__.py`
- `lazyc2/security/command_allowlist.py`
- `lazyc2/security/constants.py`
- `lazyc2/security/cors.py`
- `lazyc2/security/csrf.py`
- *... and 32 more*
