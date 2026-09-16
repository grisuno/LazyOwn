# Subsystem: extensions

## lazyc2/extensions/__init__.py
- Layer: infrastructure
- Language: py
- Imported by: `lazyc2/app_factory.py`

## lazyc2/extensions/decoy.py
- Layer: presentation
- Language: py
- Symbols:
  - `decoy_response` (function, line 12) `def decoy_response()`
- Imported by: `lazyc2/blueprints/addons.py`, `lazyc2/blueprints/auth.py`, `lazyc2/blueprints/operations.py`

## lazyc2/extensions/short_urls.py
- Layer: infrastructure
- Language: py
- Symbols:
  - `configure` (function, line 21) `def configure(sessions_phishing_dir)`
  - `load_short_urls` (function, line 33) `def load_short_urls()`
  - `save_short_urls` (function, line 59) `def save_short_urls(data)`
  - `_get_safe_file_path` (function, line 74) `def _get_safe_file_path(user_path)`
  - `is_valid_url` (function, line 104) `def is_valid_url(url)`
- Depends on: `core/logging.py`
- Imported by: `lazyc2/blueprints/phishing.py`

## lazyc2/extensions/storage.py
- Layer: data_access
- Language: py
- Symbols:
  - `configure` (function, line 18) `def configure(sessions_dir)`
  - `load_tasks` (function, line 31) `def load_tasks()`
  - `save_tasks` (function, line 45) `def save_tasks(tasks)`
  - `load_cves` (function, line 59) `def load_cves()`
  - `save_cves` (function, line 73) `def save_cves(cves)`
  - `load_note` (function, line 87) `def load_note()`
  - `save_note` (function, line 107) `def save_note(content)`
  - `load_event_config` (function, line 121) `def load_event_config()`
  - `load_notifications` (function, line 137) `def load_notifications()`
  - `load_banners` (function, line 154) `def load_banners()`
  - `load_routes` (function, line 179) `def load_routes()`
  - `save_routes` (function, line 194) `def save_routes(routes)`
- Depends on: `core/logging.py`
- Imported by: `lazyc2/blueprints/operations.py`

## lazyc2/extensions/users.py
- Layer: infrastructure
- Language: py
- Symbols:
  - `configure` (function, line 16) `def configure(users_path)`
  - `load_users` (function, line 26) `def load_users()`
  - `save_users` (function, line 46) `def save_users(users)`
- Depends on: `lazyc2.py`, `modules/lazy_rbac.py`
- Imported by: `lazyc2.py`, `lazyc2/blueprints/auth.py`, `lazyc2/blueprints/auth.py`
