# Subsystem: lazyc2

## lazyc2/__init__.py
- Layer: utility
- Language: py

## lazyc2/addon_creator.py
- Layer: utility
- Language: py
- Symbols:
  - `AddonCreatorConfig` (class, line 71) `class AddonCreatorConfig`
  - `ParamSpec` (class, line 295) `class ParamSpec`
  - `AddonDraft` (class, line 328) `class AddonDraft`
  - `ValidationIssue` (class, line 355) `class ValidationIssue`
  - `AddonValidationError` (class, line 362) `class AddonValidationError(ValueError)`
  - `AddonValidator` (class, line 375) `class AddonValidator`
  - `AddonYamlRenderer` (class, line 678) `class AddonYamlRenderer`
  - `AddonStore` (class, line 763) `class AddonStore`
  - `_multi_values` (method, line 985) `def _multi_values(form, key)`
  - `_first_value` (method, line 1006) `def _first_value(form, key)`
  - `_parse_bool` (method, line 1017) `def _parse_bool(value)`
  - `parse_addon_form` (method, line 1030) `def parse_addon_form(form)`
  - `_parse_param_rows` (method, line 1069) `def _parse_param_rows(form)`
  - `to_dict` (method, line 313) `def to_dict(self)`
  - `__init__` (method, line 369) `def __init__(self, issues)`
  - `__init__` (method, line 382) `def __init__(self, draft, config)`
  - `validate` (method, line 396) `def validate(self)`
  - `is_valid` (method, line 410) `def is_valid(self)`
  - `_check_identity` (method, line 414) `def _check_identity(self)`
  - `_check_targeting` (method, line 458) `def _check_targeting(self)`
  - `_check_tool` (method, line 505) `def _check_tool(self)`
  - `_check_params` (method, line 556) `def _check_params(self)`
  - `_check_placeholders` (method, line 629) `def _check_placeholders(self, text, field)`
  - `_is_valid_repo_url` (method, line 669) `def _is_valid_repo_url(value)`
  - `__init__` (method, line 681) `def __init__(self, config)`
  - `render` (method, line 689) `def render(self, draft)`
  - `to_document` (method, line 707) `def to_document(self, draft)`
  - `_render_tool` (method, line 737) `def _render_tool(self, draft)`
  - `__init__` (method, line 772) `def __init__(self, config, base_dir)`
  - `resolve_path` (method, line 787) `def resolve_path(self, name)`
  - `resolve_existing_path` (method, line 802) `def resolve_existing_path(self, name)`
  - `_resolve_target` (method, line 824) `def _resolve_target(self, name, pattern)`
  - `exists` (method, line 846) `def exists(self, name)`
  - `save` (method, line 857) `def save(self, name, yaml_text)`
  - `_atomic_write` (method, line 881) `def _atomic_write(self, target, text)`
  - `load` (method, line 911) `def load(self, name)`
  - `delete` (method, line 934) `def delete(self, name)`
  - `list_all` (method, line 950) `def list_all(self)`
- Imported by: `lazyc2/blueprints/addons.py`, `mutants/tests/test_addon_creator.py`, `tests/test_addon_creator.py`

## lazyc2/app_factory.py
- Layer: presentation
- Language: py
- Symbols:
  - `_load_payload_config` (function, line 33) `def _load_payload_config()`
  - `_build_api_key_store` (function, line 42) `def _build_api_key_store(payload)`
  - `_load_or_create_secret_key` (function, line 61) `def _load_or_create_secret_key(sessions_dir)`
  - `_make_security_config` (function, line 74) `def _make_security_config(payload)`
  - `create_app` (function, line 88) `def create_app()`
  - `_handle_404` (function, line 150) `def _handle_404(_error)`
  - `_handle_405` (function, line 154) `def _handle_405(_error)`
  - `_handle_exception` (function, line 158) `def _handle_exception(error)`
  - `_add_security_headers` (function, line 165) `def _add_security_headers(response)`
- Depends on: `core/api_authz.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/extensions/__init__.py`, `lazyc2/security/services.py`

## lazyc2/models.py
- Layer: presentation
- Language: py
- Symbols:
  - `User` (class, line 16) `class User(UserMixin)`
  - `__init__` (method, line 17) `def __init__(self, user_data)`
- Depends on: `modules/lazy_rbac.py`

## lazyc2/state.py
- Layer: utility
- Language: py
- Imported by: `static/js/jquery-3.5.1.slim.min.js`
