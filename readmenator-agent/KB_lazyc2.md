# Subsystem: lazyc2

## lazyc2/__init__.py
- Layer: utility
- Language: py
- Imported by: `lazyc2/blueprints/auth.py`, `lazyc2/extensions/users.py`

## lazyc2/addon_creator.py
- Doc: LazyAddon creator contract for the LazyOwn C2 web interface.
- Layer: utility
- Language: py
- Symbols:
  - `AddonCreatorConfig` (class, line 71) `class AddonCreatorConfig`
  - `ParamSpec` (class, line 410) `class ParamSpec`
  - `AddonDraft` (class, line 443) `class AddonDraft`
  - `ValidationIssue` (class, line 470) `class ValidationIssue`
  - `AddonValidationError` (class, line 477) `class AddonValidationError(ValueError)`
  - `AddonValidator` (class, line 490) `class AddonValidator`
  - `AddonYamlRenderer` (class, line 793) `class AddonYamlRenderer`
  - `AddonStore` (class, line 878) `class AddonStore`
  - `_multi_values` (function, line 1100) `def _multi_values(form, key)`
  - `_first_value` (function, line 1121) `def _first_value(form, key)`
  - `_parse_bool` (function, line 1132) `def _parse_bool(value)`
  - `parse_addon_form` (function, line 1145) `def parse_addon_form(form)`
  - `_parse_param_rows` (function, line 1184) `def _parse_param_rows(form)`
  - `live_placeholders` (method, line 387) `def live_placeholders(cls)`
  - `to_dict` (method, line 428) `def to_dict(self)`
  - `__init__` (method, line 484) `def __init__(self, issues)`
  - `__init__` (method, line 497) `def __init__(self, draft, config)`
  - `validate` (method, line 511) `def validate(self)`
  - `is_valid` (method, line 525) `def is_valid(self)`
  - `_check_identity` (method, line 529) `def _check_identity(self)`
  - `_check_targeting` (method, line 573) `def _check_targeting(self)`
  - `_check_tool` (method, line 620) `def _check_tool(self)`
  - `_check_params` (method, line 671) `def _check_params(self)`
  - `_check_placeholders` (method, line 744) `def _check_placeholders(self, text, field)`
  - `_is_valid_repo_url` (method, line 784) `def _is_valid_repo_url(value)`
  - `__init__` (method, line 796) `def __init__(self, config)`
  - `render` (method, line 804) `def render(self, draft)`
  - `to_document` (method, line 822) `def to_document(self, draft)`
  - `_render_tool` (method, line 852) `def _render_tool(self, draft)`
  - `__init__` (method, line 887) `def __init__(self, config, base_dir)`
  - `resolve_path` (method, line 902) `def resolve_path(self, name)`
  - `resolve_existing_path` (method, line 917) `def resolve_existing_path(self, name)`
  - `_resolve_target` (method, line 939) `def _resolve_target(self, name, pattern)`
  - `exists` (method, line 961) `def exists(self, name)`
  - `save` (method, line 972) `def save(self, name, yaml_text)`
  - `_atomic_write` (method, line 996) `def _atomic_write(self, target, text)`
  - `load` (method, line 1026) `def load(self, name)`
  - `delete` (method, line 1049) `def delete(self, name)`
  - `list_all` (method, line 1065) `def list_all(self)`
- Depends on: `core/param_registry.py`
- Imported by: `lazyc2/blueprints/addons.py`, `tests/test_addon_creator.py`, `tests/test_param_registry.py`, `tests/test_php2shell_addon.py`, `tests/test_placeholder_coverage.py`

## lazyc2/app_factory.py
- Doc: Flask application factory for the LazyOwn C2 server.
- Layer: presentation
- Language: py
- Symbols:
  - `_load_payload_config` (function, line 36) `def _load_payload_config()`
  - `_build_api_key_store` (function, line 45) `def _build_api_key_store(payload)`
  - `_load_or_create_secret_key` (function, line 64) `def _load_or_create_secret_key(sessions_dir)`
  - `_make_security_config` (function, line 78) `def _make_security_config(payload)`
  - `create_app` (function, line 92) `def create_app()`
  - `_factory_load_user` (function, line 139) `def _factory_load_user(user_id)`
  - `_handle_404` (function, line 178) `def _handle_404(_error)`
  - `_handle_405` (function, line 182) `def _handle_405(_error)`
  - `_handle_exception` (function, line 186) `def _handle_exception(error)`
  - `_add_security_headers` (function, line 193) `def _add_security_headers(response)`
  - `_FactoryUser` (class, line 143) `class _FactoryUser(UserMixin)`
  - `__init__` (method, line 144) `def __init__(self, data)`
- Depends on: `core/api_authz.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/blueprints/gym.py`, `lazyc2/blueprints/loops.py`, `lazyc2/blueprints/orchestrator.py`, `lazyc2/extensions/__init__.py`, `lazyc2/security/services.py`, `modules/lazy_rbac.py`

## lazyc2/models.py
- Doc: C2 data models extracted from lazyc2.py.
- Layer: business_logic
- Language: py
- Symbols:
  - `User` (class, line 16) `class User(UserMixin)`
  - `__init__` (method, line 17) `def __init__(self, user_data)`
- Depends on: `modules/lazy_rbac.py`

## lazyc2/state.py
- Doc: Global C2 server state — namespace for shared mutable objects.
- Layer: utility
- Language: py
- Imported by: `static/js/jquery-3.5.1.slim.min.js`
