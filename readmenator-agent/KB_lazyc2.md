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
  - `ParamSpec` (class, line 348) `class ParamSpec`
  - `AddonDraft` (class, line 381) `class AddonDraft`
  - `ValidationIssue` (class, line 408) `class ValidationIssue`
  - `AddonValidationError` (class, line 415) `class AddonValidationError(ValueError)`
  - `AddonValidator` (class, line 428) `class AddonValidator`
  - `AddonYamlRenderer` (class, line 731) `class AddonYamlRenderer`
  - `AddonStore` (class, line 816) `class AddonStore`
  - `_multi_values` (function, line 1038) `def _multi_values(form, key)`
  - `_first_value` (function, line 1059) `def _first_value(form, key)`
  - `_parse_bool` (function, line 1070) `def _parse_bool(value)`
  - `parse_addon_form` (function, line 1083) `def parse_addon_form(form)`
  - `_parse_param_rows` (function, line 1122) `def _parse_param_rows(form)`
  - `to_dict` (method, line 366) `def to_dict(self)`
  - `__init__` (method, line 422) `def __init__(self, issues)`
  - `__init__` (method, line 435) `def __init__(self, draft, config)`
  - `validate` (method, line 449) `def validate(self)`
  - `is_valid` (method, line 463) `def is_valid(self)`
  - `_check_identity` (method, line 467) `def _check_identity(self)`
  - `_check_targeting` (method, line 511) `def _check_targeting(self)`
  - `_check_tool` (method, line 558) `def _check_tool(self)`
  - `_check_params` (method, line 609) `def _check_params(self)`
  - `_check_placeholders` (method, line 682) `def _check_placeholders(self, text, field)`
  - `_is_valid_repo_url` (method, line 722) `def _is_valid_repo_url(value)`
  - `__init__` (method, line 734) `def __init__(self, config)`
  - `render` (method, line 742) `def render(self, draft)`
  - `to_document` (method, line 760) `def to_document(self, draft)`
  - `_render_tool` (method, line 790) `def _render_tool(self, draft)`
  - `__init__` (method, line 825) `def __init__(self, config, base_dir)`
  - `resolve_path` (method, line 840) `def resolve_path(self, name)`
  - `resolve_existing_path` (method, line 855) `def resolve_existing_path(self, name)`
  - `_resolve_target` (method, line 877) `def _resolve_target(self, name, pattern)`
  - `exists` (method, line 899) `def exists(self, name)`
  - `save` (method, line 910) `def save(self, name, yaml_text)`
  - `_atomic_write` (method, line 934) `def _atomic_write(self, target, text)`
  - `load` (method, line 964) `def load(self, name)`
  - `delete` (method, line 987) `def delete(self, name)`
  - `list_all` (method, line 1003) `def list_all(self)`
- Imported by: `lazyc2/blueprints/addons.py`, `tests/test_addon_creator.py`, `tests/test_placeholder_coverage.py`

## lazyc2/app_factory.py
- Doc: Flask application factory for the LazyOwn C2 server.
- Layer: presentation
- Language: py
- Symbols:
  - `_load_payload_config` (function, line 34) `def _load_payload_config()`
  - `_build_api_key_store` (function, line 43) `def _build_api_key_store(payload)`
  - `_load_or_create_secret_key` (function, line 62) `def _load_or_create_secret_key(sessions_dir)`
  - `_make_security_config` (function, line 76) `def _make_security_config(payload)`
  - `create_app` (function, line 90) `def create_app()`
  - `_factory_load_user` (function, line 137) `def _factory_load_user(user_id)`
  - `_handle_404` (function, line 173) `def _handle_404(_error)`
  - `_handle_405` (function, line 177) `def _handle_405(_error)`
  - `_handle_exception` (function, line 181) `def _handle_exception(error)`
  - `_add_security_headers` (function, line 188) `def _add_security_headers(response)`
  - `_FactoryUser` (class, line 141) `class _FactoryUser(UserMixin)`
  - `__init__` (method, line 142) `def __init__(self, data)`
- Depends on: `core/api_authz.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/blueprints/orchestrator.py`, `lazyc2/extensions/__init__.py`, `lazyc2/security/services.py`, `modules/lazy_rbac.py`

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
