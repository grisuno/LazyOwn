# Symbols (page 9 of 40)
Previous: [SYMBOLS_p8.md](SYMBOLS_p8.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `is_allowed` | method | `lazyc2/security/cors.py:136` | `def is_allowed(self, origin)` |
| `origins_for_socketio` | method | `lazyc2/security/cors.py:110` | `def origins_for_socketio(self)` |
| `resolve_origins` | method | `lazyc2/security/cors.py:89` | `def resolve_origins(self)` |
| `CSRFPolicy` | class | `lazyc2/security/csrf.py:48` | `class CSRFPolicy` |
| `__init__` | method | `lazyc2/security/csrf.py:69` | `def __init__(self, header, form_field, cookie_name, exempt_paths, secret)` |
| `check_request` | method | `lazyc2/security/csrf.py:182` | `def check_request(self, session_id, request)` |
| `cookie_name` | method | `lazyc2/security/csrf.py:90` | `def cookie_name(self)` |
| `extract_token` | method | `lazyc2/security/csrf.py:163` | `def extract_token(self, request)` |
| `forget` | method | `lazyc2/security/csrf.py:126` | `def forget(self, session_id)` |
| `header` | method | `lazyc2/security/csrf.py:85` | `def header(self)` |
| `is_exempt` | method | `lazyc2/security/csrf.py:147` | `def is_exempt(self, path)` |
| `issue` | method | `lazyc2/security/csrf.py:94` | `def issue(self, session_id)` |
| `rotate` | method | `lazyc2/security/csrf.py:111` | `def rotate(self, session_id)` |
| `validate` | method | `lazyc2/security/csrf.py:130` | `def validate(self, session_id, candidate)` |
| `_strip_dangerous_blocks` | function | `lazyc2/security/html_sanitizer.py:62` | `def _strip_dangerous_blocks(raw_html)` |
| `sanitize_html` | function | `lazyc2/security/html_sanitizer.py:78` | `def sanitize_html(raw_html, allowed_tags, allowed_attributes)` |
| `HTTPSRedirect` | class | `lazyc2/security/https_redirect.py:41` | `class HTTPSRedirect` |
| `RedirectResponse` | class | `lazyc2/security/https_redirect.py:29` | `class RedirectResponse` |
| `__init__` | method | `lazyc2/security/https_redirect.py:51` | `def __init__(self, env, enabled)` |
| `enabled` | method | `lazyc2/security/https_redirect.py:56` | `def enabled(self)` |
| `evaluate` | method | `lazyc2/security/https_redirect.py:60` | `def evaluate(self, request)` |
| `AESKeyManager` | class | `lazyc2/security/services.py:152` | `class AESKeyManager` |
| `SafeFileService` | class | `lazyc2/security/services.py:56` | `class SafeFileService` |
| `SecretKeyManager` | class | `lazyc2/security/services.py:19` | `class SecretKeyManager` |
| `UploadSizeValidator` | class | `lazyc2/security/services.py:183` | `class UploadSizeValidator` |
| `__init__` | method | `lazyc2/security/services.py:30` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `lazyc2/security/services.py:63` | `def __init__(self, base_dir)` |
| `__init__` | method | `lazyc2/security/services.py:158` | `def __init__(self, key_file)` |
| `__init__` | method | `lazyc2/security/services.py:189` | `def __init__(self, max_size_bytes)` |
| `_resolve_safe` | method | `lazyc2/security/services.py:68` | `def _resolve_safe(self, relative_path)` |
| `exists` | method | `lazyc2/security/services.py:136` | `def exists(self, relative_path)` |
| `get_or_create` | method | `lazyc2/security/services.py:33` | `def get_or_create(self)` |
| `get_or_generate` | method | `lazyc2/security/services.py:161` | `def get_or_generate(self)` |
| `read_bytes` | method | `lazyc2/security/services.py:86` | `def read_bytes(self, relative_path)` |
| `read_text` | method | `lazyc2/security/services.py:102` | `def read_text(self, relative_path, encoding)` |
| `validate` | method | `lazyc2/security/services.py:192` | `def validate(self, content_length)` |
| `write_bytes` | method | `lazyc2/security/services.py:119` | `def write_bytes(self, relative_path, data)` |
| `TrustedProxyResolver` | class | `lazyc2/security/trusted_proxy.py:30` | `class TrustedProxyResolver` |
| `__init__` | method | `lazyc2/security/trusted_proxy.py:42` | `def __init__(self, trusted_count, operator_allowlist)` |
| `client_ip` | method | `lazyc2/security/trusted_proxy.py:57` | `def client_ip(self, remote_addr, x_forwarded_for)` |
| `is_operator` | method | `lazyc2/security/trusted_proxy.py:80` | `def is_operator(self, ip)` |
| `trusted_count` | method | `lazyc2/security/trusted_proxy.py:53` | `def trusted_count(self)` |
| `resolve_contained_file_path` | function | `lazyc2/security/validators.py:174` | `def resolve_contained_file_path(raw_url, base_dir)` |
| `validate_aes_key` | function | `lazyc2/security/validators.py:102` | `def validate_aes_key(key)` |
| `validate_file_path_within_base` | function | `lazyc2/security/validators.py:150` | `def validate_file_path_within_base(file_path, base_dir)` |
| `validate_password_length` | function | `lazyc2/security/validators.py:118` | `def validate_password_length(password)` |
| `validate_request_data` | function | `lazyc2/security/validators.py:86` | `def validate_request_data(data)` |
| `validate_route_path` | function | `lazyc2/security/validators.py:24` | `def validate_route_path(route_path)` |
| `validate_template_name` | function | `lazyc2/security/validators.py:46` | `def validate_template_name(template_name)` |
| `validate_upload_size` | function | `lazyc2/security/validators.py:134` | `def validate_upload_size(content_length)` |
| `validate_yaml_filename` | function | `lazyc2/security/validators.py:68` | `def validate_yaml_filename(filename)` |
| `main` | function | `lazygui/__main__.py:14` | `def main()` |
| `Application` | class | `lazygui/app.py:33` | `class Application` |
| `__init__` | method | `lazygui/app.py:36` | `def __init__(self, argv)` |
| `_build_backend_from_request` | method | `lazygui/app.py:167` | `def _build_backend_from_request(self, request)` |
| `_build_initial_backend` | method | `lazygui/app.py:119` | `def _build_initial_backend(self)` |
| `_configure_logging` | method | `lazygui/app.py:224` | `def _configure_logging(self)` |
| `_configure_qt_application_metadata` | method | `lazygui/app.py:218` | `def _configure_qt_application_metadata(self)` |
| `_configure_qt_attributes` | method | `lazygui/app.py:213` | `def _configure_qt_attributes(self)` |
| `_discover_credentials` | method | `lazygui/app.py:73` | `def _discover_credentials(self)` |
| `_resolve_teamserver_credentials` | method | `lazygui/app.py:150` | `def _resolve_teamserver_credentials(self)` |
| `_start_backend` | method | `lazygui/app.py:194` | `def _start_backend(self, backend)` |
| `_swap_backend` | method | `lazygui/app.py:175` | `def _swap_backend(self, new_backend)` |
| `_sync_credentials_to_settings` | method | `lazygui/app.py:89` | `def _sync_credentials_to_settings(self, credentials)` |
| `run` | method | `lazygui/app.py:65` | `def run(self)` |
| `show_connect_dialog` | method | `lazygui/app.py:100` | `def show_connect_dialog(self)` |
| `C2Credentials` | class | `lazygui/config/c2_credentials.py:24` | `class C2Credentials` |
| `empty` | method | `lazygui/config/c2_credentials.py:33` | `def empty(cls)` |
| `load_c2_credentials` | function | `lazygui/config/c2_credentials.py:71` | `def load_c2_credentials(project_root)` |
| `load_c2_credentials_from_file` | function | `lazygui/config/c2_credentials.py:38` | `def load_c2_credentials_from_file(file_path)` |
| `AppConstants` | class | `lazygui/config/constants.py:223` | `class AppConstants` |
| `BackendConstants` | class | `lazygui/config/constants.py:176` | `class BackendConstants` |
| `CommandPaletteConstants` | class | `lazygui/config/constants.py:214` | `class CommandPaletteConstants` |
| `EventLogConstants` | class | `lazygui/config/constants.py:205` | `class EventLogConstants` |
| `FontConstants` | class | `lazygui/config/constants.py:99` | `class FontConstants` |
| `IdentifierConstants` | class | `lazygui/config/constants.py:142` | `class IdentifierConstants` |
| `KeybindingConstants` | class | `lazygui/config/constants.py:124` | `class KeybindingConstants` |
| `NetworkConstants` | class | `lazygui/config/constants.py:48` | `class NetworkConstants` |
| `PanelConstants` | class | `lazygui/config/constants.py:185` | `class PanelConstants` |
| `PtyConstants` | class | `lazygui/config/constants.py:86` | `class PtyConstants` |
| `ThemeConstants` | class | `lazygui/config/constants.py:161` | `class ThemeConstants` |
| `TimingConstants` | class | `lazygui/config/constants.py:34` | `class TimingConstants` |
| `WindowConstants` | class | `lazygui/config/constants.py:18` | `class WindowConstants` |
| `panel_labels` | method | `lazygui/config/constants.py:239` | `def panel_labels(self)` |
| `AppPaths` | class | `lazygui/config/paths.py:19` | `class AppPaths` |
| `_detect_project_root` | function | `lazygui/config/paths.py:79` | `def _detect_project_root()` |
| `c2_credentials_path` | method | `lazygui/config/paths.py:59` | `def c2_credentials_path(self)` |
| `config_dir` | method | `lazygui/config/paths.py:32` | `def config_dir(self)` |
| `ensure_config_dir` | method | `lazygui/config/paths.py:73` | `def ensure_config_dir(self)` |
| `layout_file` | method | `lazygui/config/paths.py:44` | `def layout_file(self)` |
| `lazyc2_script` | method | `lazygui/config/paths.py:54` | `def lazyc2_script(self)` |
| `project_run_script` | method | `lazygui/config/paths.py:49` | `def project_run_script(self)` |
| `sessions_dir` | method | `lazygui/config/paths.py:69` | `def sessions_dir(self)` |
| `settings_file` | method | `lazygui/config/paths.py:39` | `def settings_file(self)` |
| `AppSettings` | class | `lazygui/config/settings.py:27` | `class AppSettings` |
| `c2_credentials_loaded` | method | `lazygui/config/settings.py:120` | `def c2_credentials_loaded(self)` |
| `c2_credentials_loaded` | method | `lazygui/config/settings.py:125` | `def c2_credentials_loaded(self, value)` |
| `get` | method | `lazygui/config/settings.py:55` | `def get(self, key, default)` |
| `last_backend_id` | method | `lazygui/config/settings.py:73` | `def last_backend_id(self)` |
| `last_backend_id` | method | `lazygui/config/settings.py:78` | `def last_backend_id(self, value)` |
| `last_operator_name` | method | `lazygui/config/settings.py:98` | `def last_operator_name(self)` |
| `last_operator_name` | method | `lazygui/config/settings.py:107` | `def last_operator_name(self, value)` |
| `last_teamserver_password` | method | `lazygui/config/settings.py:111` | `def last_teamserver_password(self)` |
| `last_teamserver_password` | method | `lazygui/config/settings.py:116` | `def last_teamserver_password(self, value)` |
| `last_teamserver_url` | method | `lazygui/config/settings.py:84` | `def last_teamserver_url(self)` |
| `last_teamserver_url` | method | `lazygui/config/settings.py:94` | `def last_teamserver_url(self, value)` |
| `load` | method | `lazygui/config/settings.py:35` | `def load(cls, constants, paths)` |
| `save` | method | `lazygui/config/settings.py:47` | `def save(self)` |
| `set` | method | `lazygui/config/settings.py:59` | `def set(self, key, value)` |
| `snapshot` | method | `lazygui/config/settings.py:128` | `def snapshot(self)` |
| `theme_id` | method | `lazygui/config/settings.py:64` | `def theme_id(self)` |
| `theme_id` | method | `lazygui/config/settings.py:69` | `def theme_id(self, value)` |
| `PanelBase` | class | `lazygui/panels/base.py:17` | `class PanelBase(QDockWidget)` |
| `__init__` | method | `lazygui/panels/base.py:20` | `def __init__(self, constants, backend, identifier, title, parent)` |
| `backend` | method | `lazygui/panels/base.py:48` | `def backend(self)` |
| `identifier` | method | `lazygui/panels/base.py:43` | `def identifier(self)` |
| `CampaignPanel` | class | `lazygui/panels/campaign_panel.py:28` | `class CampaignPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/campaign_panel.py:31` | `def __init__(self, constants, backend, parent)` |
| `_on_campaigns_changed` | method | `lazygui/panels/campaign_panel.py:102` | `def _on_campaigns_changed(self, campaigns)` |
| `_populate_tree` | method | `lazygui/panels/campaign_panel.py:106` | `def _populate_tree(self)` |
| `_refresh` | method | `lazygui/panels/campaign_panel.py:99` | `def _refresh(self)` |
| `_request_new_campaign` | method | `lazygui/panels/campaign_panel.py:120` | `def _request_new_campaign(self)` |
| `_request_run_playbook` | method | `lazygui/panels/campaign_panel.py:126` | `def _request_run_playbook(self)` |
| `_request_view_campaign` | method | `lazygui/panels/campaign_panel.py:123` | `def _request_view_campaign(self)` |
| `campaign_count` | method | `lazygui/panels/campaign_panel.py:133` | `def campaign_count(self)` |
| `CredentialsPanel` | class | `lazygui/panels/credentials_panel.py:27` | `class CredentialsPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/credentials_panel.py:30` | `def __init__(self, constants, backend, parent)` |
| `_build_ui` | method | `lazygui/panels/credentials_panel.py:50` | `def _build_ui(self)` |
| `_copy_selected` | method | `lazygui/panels/credentials_panel.py:130` | `def _copy_selected(self)` |
| `_refresh` | method | `lazygui/panels/credentials_panel.py:95` | `def _refresh(self)` |
| `CVEPanel` | class | `lazygui/panels/cve_panel.py:28` | `class CVEPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/cve_panel.py:31` | `def __init__(self, constants, backend, parent)` |
| `_populate_tree` | method | `lazygui/panels/cve_panel.py:150` | `def _populate_tree(self)` |
| `_refresh` | method | `lazygui/panels/cve_panel.py:102` | `def _refresh(self)` |
| `_request_lookup` | method | `lazygui/panels/cve_panel.py:165` | `def _request_lookup(self)` |
| `_request_search_exploits` | method | `lazygui/panels/cve_panel.py:171` | `def _request_search_exploits(self)` |
| `cve_count` | method | `lazygui/panels/cve_panel.py:178` | `def cve_count(self)` |
| `EventLogPanel` | class | `lazygui/panels/event_log_panel.py:24` | `class EventLogPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/event_log_panel.py:27` | `def __init__(self, constants, backend, event_log, parent)` |
| `_on_level_changed` | method | `lazygui/panels/event_log_panel.py:69` | `def _on_level_changed(self, _index)` |
| `GraphPanel` | class | `lazygui/panels/graph_panel.py:20` | `class GraphPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/graph_panel.py:23` | `def __init__(self, constants, backend, parent)` |
| `_find_node_info` | method | `lazygui/panels/graph_panel.py:109` | `def _find_node_info(self, node_id)` |
| `_on_node_context_menu` | method | `lazygui/panels/graph_panel.py:54` | `def _on_node_context_menu(self, node_id, position)` |
| `_on_node_selected` | method | `lazygui/panels/graph_panel.py:105` | `def _on_node_selected(self, node_id)` |
| `_on_topology_changed` | method | `lazygui/panels/graph_panel.py:50` | `def _on_topology_changed(self, topology)` |
| `graph_view` | method | `lazygui/panels/graph_panel.py:118` | `def graph_view(self)` |
| `HistoryPanel` | class | `lazygui/panels/history_panel.py:30` | `class HistoryPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/history_panel.py:33` | `def __init__(self, constants, backend, parent)` |
| `_populate` | method | `lazygui/panels/history_panel.py:106` | `def _populate(self)` |
| `_refresh` | method | `lazygui/panels/history_panel.py:87` | `def _refresh(self)` |
| `KillChainPanel` | class | `lazygui/panels/killchain_panel.py:35` | `class KillChainPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/killchain_panel.py:38` | `def __init__(self, constants, backend, parent)` |
| `_apply_visuals` | method | `lazygui/panels/killchain_panel.py:128` | `def _apply_visuals(self)` |
| `_build_ui` | method | `lazygui/panels/killchain_panel.py:62` | `def _build_ui(self)` |
| `_get_phases` | function | `lazygui/panels/killchain_panel.py:23` | `def _get_phases()` |
| `_refresh` | method | `lazygui/panels/killchain_panel.py:96` | `def _refresh(self)` |
| `ListenersPanel` | class | `lazygui/panels/listeners_panel.py:21` | `class ListenersPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/listeners_panel.py:24` | `def __init__(self, constants, backend, parent)` |
| `_matches_filter` | method | `lazygui/panels/listeners_panel.py:95` | `def _matches_filter(self, listener)` |
| `_on_filter_changed` | method | `lazygui/panels/listeners_panel.py:70` | `def _on_filter_changed(self, text)` |
| `_on_listeners_changed` | method | `lazygui/panels/listeners_panel.py:65` | `def _on_listeners_changed(self, listeners)` |
| `_populate_visible` | method | `lazygui/panels/listeners_panel.py:75` | `def _populate_visible(self)` |
| `MarketplacePanel` | class | `lazygui/panels/marketplace_panel.py:29` | `class MarketplacePanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/marketplace_panel.py:32` | `def __init__(self, constants, backend, parent)` |
| `_apply_filter` | method | `lazygui/panels/marketplace_panel.py:270` | `def _apply_filter(self)` |
| `_fetch_addons` | method | `lazygui/panels/marketplace_panel.py:163` | `def _fetch_addons(self)` |
| `_fetch_nuclei_templates` | method | `lazygui/panels/marketplace_panel.py:128` | `def _fetch_nuclei_templates(self)` |
| `_fetch_plugins` | method | `lazygui/panels/marketplace_panel.py:198` | `def _fetch_plugins(self)` |
| `_fetch_yara_rules` | method | `lazygui/panels/marketplace_panel.py:112` | `def _fetch_yara_rules(self)` |
| `_make_tree` | method | `lazygui/panels/marketplace_panel.py:94` | `def _make_tree(headers)` |
| `_populate_addons_tree` | method | `lazygui/panels/marketplace_panel.py:250` | `def _populate_addons_tree(self)` |
| `_populate_nuclei_tree` | method | `lazygui/panels/marketplace_panel.py:238` | `def _populate_nuclei_tree(self)` |
| `_populate_plugins_tree` | method | `lazygui/panels/marketplace_panel.py:262` | `def _populate_plugins_tree(self)` |
| `_populate_yara_tree` | method | `lazygui/panels/marketplace_panel.py:230` | `def _populate_yara_tree(self)` |
| `_refresh` | method | `lazygui/panels/marketplace_panel.py:106` | `def _refresh(self)` |
| `_run_selected` | method | `lazygui/panels/marketplace_panel.py:287` | `def _run_selected(self)` |
| `_show_selected_info` | method | `lazygui/panels/marketplace_panel.py:276` | `def _show_selected_info(self)` |
| `PanelRegistry` | class | `lazygui/panels/registry.py:34` | `class PanelRegistry` |
| `__iter__` | method | `lazygui/panels/registry.py:106` | `def __iter__(self)` |
| `all_panels` | method | `lazygui/panels/registry.py:83` | `def all_panels(self)` |
| `build` | method | `lazygui/panels/registry.py:53` | `def build(cls, constants, backend, event_log, parent)` |
| `by_identifier` | method | `lazygui/panels/registry.py:99` | `def by_identifier(self, identifier)` |
| `SessionsPanel` | class | `lazygui/panels/sessions_panel.py:39` | `class SessionsPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/sessions_panel.py:45` | `def __init__(self, constants, backend, parent)` |
| `_matches_filter` | method | `lazygui/panels/sessions_panel.py:202` | `def _matches_filter(self, session)` |
| `_on_context_menu` | method | `lazygui/panels/sessions_panel.py:133` | `def _on_context_menu(self, position)` |
| `_on_filter_changed` | method | `lazygui/panels/sessions_panel.py:98` | `def _on_filter_changed(self, text)` |
| `_on_item_double_clicked` | method | `lazygui/panels/sessions_panel.py:114` | `def _on_item_double_clicked(self, item)` |
| `_on_selection_changed` | method | `lazygui/panels/sessions_panel.py:103` | `def _on_selection_changed(self)` |
| `_on_sessions_changed` | method | `lazygui/panels/sessions_panel.py:93` | `def _on_sessions_changed(self, sessions)` |
| `_populate_visible` | method | `lazygui/panels/sessions_panel.py:182` | `def _populate_visible(self)` |
| `_refresh_initial` | method | `lazygui/panels/sessions_panel.py:87` | `def _refresh_initial(self)` |
| `TerminalPanel` | class | `lazygui/panels/terminal_panel.py:22` | `class TerminalPanel(PanelBase)` |
| `__init__` | method | `lazygui/panels/terminal_panel.py:25` | `def __init__(self, constants, backend, parent)` |
| `_on_beacon_result` | method | `lazygui/panels/terminal_panel.py:119` | `def _on_beacon_result(self, result)` |
| `_send_beacon_command` | method | `lazygui/panels/terminal_panel.py:90` | `def _send_beacon_command(self)` |
| `_update_session_combo` | method | `lazygui/panels/terminal_panel.py:104` | `def _update_session_combo(self, sessions)` |
| `focus_terminal` | method | `lazygui/panels/terminal_panel.py:78` | `def focus_terminal(self)` |
| `set_target_session` | method | `lazygui/panels/terminal_panel.py:82` | `def set_target_session(self, session_id)` |
| `Backend` | class | `lazygui/services/backend.py:52` | `class Backend(QObject)` |
| `BackendDescriptor` | class | `lazygui/services/backend.py:44` | `class BackendDescriptor` |
| `BackendStatus` | class | `lazygui/services/backend.py:33` | `class BackendStatus(StrEnum)` |
| `__init__` | method | `lazygui/services/backend.py:81` | `def __init__(self, descriptor, parent)` |
| `_set_status` | method | `lazygui/services/backend.py:97` | `def _set_status(self, new_status)` |
| `descriptor` | method | `lazygui/services/backend.py:88` | `def descriptor(self)` |
| `feed_terminal_input` | method | `lazygui/services/backend.py:124` | `def feed_terminal_input(self, data)` |
| `known_campaigns` | method | `lazygui/services/backend.py:140` | `def known_campaigns(self)` |
| `known_listeners` | method | `lazygui/services/backend.py:132` | `def known_listeners(self)` |
| `known_sessions` | method | `lazygui/services/backend.py:128` | `def known_sessions(self)` |
| `known_topology` | method | `lazygui/services/backend.py:136` | `def known_topology(self)` |
| `refresh` | method | `lazygui/services/backend.py:116` | `def refresh(self)` |
| `request_beacon_history` | method | `lazygui/services/backend.py:158` | `def request_beacon_history(self, client_id)` |
| `request_session_state` | method | `lazygui/services/backend.py:172` | `def request_session_state(self)` |
| `request_world_model` | method | `lazygui/services/backend.py:144` | `def request_world_model(self)` |
| `resize_terminal` | method | `lazygui/services/backend.py:120` | `def resize_terminal(self, columns, rows)` |
| `send_command` | method | `lazygui/services/backend.py:112` | `def send_command(self, command, target_session)` |
| `start` | method | `lazygui/services/backend.py:104` | `def start(self)` |
| `status` | method | `lazygui/services/backend.py:93` | `def status(self)` |
| `stop` | method | `lazygui/services/backend.py:108` | `def stop(self)` |
| `EventLog` | class | `lazygui/services/event_log.py:20` | `class EventLog(QObject)` |
| `__init__` | method | `lazygui/services/event_log.py:26` | `def __init__(self, constants, parent)` |
| `append` | method | `lazygui/services/event_log.py:37` | `def append(self, record)` |
| `capacity` | method | `lazygui/services/event_log.py:33` | `def capacity(self)` |
| `clear` | method | `lazygui/services/event_log.py:47` | `def clear(self)` |
| `extend` | method | `lazygui/services/event_log.py:42` | `def extend(self, records)` |
| `snapshot` | method | `lazygui/services/event_log.py:52` | `def snapshot(self, minimum_level)` |
| `BackendFactory` | class | `lazygui/services/factory.py:24` | `class BackendFactory` |
| `create` | method | `lazygui/services/factory.py:42` | `def create(self, kind, parent, credentials)` |
| `create_local` | method | `lazygui/services/factory.py:30` | `def create_local(self, parent)` |
| `create_teamserver` | method | `lazygui/services/factory.py:34` | `def create_teamserver(self, credentials, parent)` |
| `LocalPtyBackend` | class | `lazygui/services/local_backend.py:30` | `class LocalPtyBackend(Backend)` |
| `__init__` | method | `lazygui/services/local_backend.py:38` | `def __init__(self, constants, paths, parent)` |
| `_configure_master_fd` | method | `lazygui/services/local_backend.py:156` | `def _configure_master_fd(self)` |
| `_emit_event` | method | `lazygui/services/local_backend.py:235` | `def _emit_event(self, level, message)` |
| `_exec_child_process` | method | `lazygui/services/local_backend.py:147` | `def _exec_child_process(self)` |
| `_handle_pty_eof` | method | `lazygui/services/local_backend.py:215` | `def _handle_pty_eof(self)` |
| `_install_read_notifier` | method | `lazygui/services/local_backend.py:173` | `def _install_read_notifier(self)` |
| `_install_reaper` | method | `lazygui/services/local_backend.py:180` | `def _install_reaper(self)` |
| `_install_window_size` | method | `lazygui/services/local_backend.py:163` | `def _install_window_size(self)` |
| `_on_master_readable` | method | `lazygui/services/local_backend.py:187` | `def _on_master_readable(self)` |
| `_reap_child` | method | `lazygui/services/local_backend.py:220` | `def _reap_child(self)` |
| `announce_local_operator` | method | `lazygui/services/local_backend.py:249` | `def announce_local_operator(self)` |
| `feed_terminal_input` | method | `lazygui/services/local_backend.py:127` | `def feed_terminal_input(self, data)` |
| `known_listeners` | method | `lazygui/services/local_backend.py:141` | `def known_listeners(self)` |
| `known_sessions` | method | `lazygui/services/local_backend.py:137` | `def known_sessions(self)` |
| `refresh` | method | `lazygui/services/local_backend.py:117` | `def refresh(self)` |
| `resize_terminal` | method | `lazygui/services/local_backend.py:121` | `def resize_terminal(self, columns, rows)` |
| `send_command` | method | `lazygui/services/local_backend.py:112` | `def send_command(self, command, target_session)` |
| `start` | method | `lazygui/services/local_backend.py:62` | `def start(self)` |
| `stop` | method | `lazygui/services/local_backend.py:87` | `def stop(self)` |
| `BackendKind` | class | `lazygui/services/models.py:17` | `class BackendKind(StrEnum)` |
| `BeaconResult` | class | `lazygui/services/models.py:164` | `class BeaconResult` |
| `CampaignSummary` | class | `lazygui/services/models.py:151` | `class CampaignSummary` |
| `DashboardPayload` | class | `lazygui/services/models.py:139` | `class DashboardPayload` |
| `EventLevel` | class | `lazygui/services/models.py:24` | `class EventLevel(StrEnum)` |
| `EventRecord` | class | `lazygui/services/models.py:87` | `class EventRecord` |
| `GraphEdge` | class | `lazygui/services/models.py:115` | `class GraphEdge` |
| `GraphNode` | class | `lazygui/services/models.py:102` | `class GraphNode` |
| `Listener` | class | `lazygui/services/models.py:64` | `class Listener` |
| `Operator` | class | `lazygui/services/models.py:76` | `class Operator` |
| `Session` | class | `lazygui/services/models.py:49` | `class Session` |
| `Topology` | class | `lazygui/services/models.py:126` | `class Topology` |
| `empty` | method | `lazygui/services/models.py:133` | `def empty(cls)` |
| `now` | method | `lazygui/services/models.py:96` | `def now(cls, level, source, message)` |
| `numeric` | method | `lazygui/services/models.py:34` | `def numeric(self)` |
| `TeamserverBackend` | class | `lazygui/services/teamserver_backend.py:48` | `class TeamserverBackend(Backend)` |
| `TeamserverCredentials` | class | `lazygui/services/teamserver_backend.py:39` | `class TeamserverCredentials` |
| `__init__` | method | `lazygui/services/teamserver_backend.py:51` | `def __init__(self, constants, credentials, parent)` |
| `_build_http_session` | method | `lazygui/services/teamserver_backend.py:302` | `def _build_http_session(self)` |
| `_build_topology_from_payload` | method | `lazygui/services/teamserver_backend.py:664` | `def _build_topology_from_payload(self, payload)` |
| `_build_url` | method | `lazygui/services/teamserver_backend.py:312` | `def _build_url(self, path)` |
| `_connect_sio` | function | `lazygui/services/teamserver_backend.py:444` | `def _connect_sio()` |
| `_dispatch_terminal_lines` | method | `lazygui/services/teamserver_backend.py:378` | `def _dispatch_terminal_lines(self, data)` |
| `_emit_event` | method | `lazygui/services/teamserver_backend.py:780` | `def _emit_event(self, level, message)` |
| `_establish_flask_session` | method | `lazygui/services/teamserver_backend.py:285` | `def _establish_flask_session(self)` |
| `_http_get_json` | method | `lazygui/services/teamserver_backend.py:318` | `def _http_get_json(self, path)` |
| `_http_post_form` | method | `lazygui/services/teamserver_backend.py:332` | `def _http_post_form(self, path, payload)` |
| `_install_http_polling` | method | `lazygui/services/teamserver_backend.py:424` | `def _install_http_polling(self)` |
| `_on_connect` | function | `lazygui/services/teamserver_backend.py:487` | `def _on_connect()` |
| `_on_disconnect` | function | `lazygui/services/teamserver_backend.py:491` | `def _on_disconnect()` |
| `_on_output` | function | `lazygui/services/teamserver_backend.py:481` | `def _on_output(data)` |
| `_on_pty_connect` | function | `lazygui/services/teamserver_backend.py:461` | `def _on_pty_connect()` |
| `_on_pty_output` | function | `lazygui/services/teamserver_backend.py:465` | `def _on_pty_output(data)` |
| `_on_terminal_connect` | function | `lazygui/services/teamserver_backend.py:471` | `def _on_terminal_connect()` |
| `_on_terminal_response` | function | `lazygui/services/teamserver_backend.py:475` | `def _on_terminal_response(data)` |
| `_parse_graph_edges` | method | `lazygui/services/teamserver_backend.py:645` | `def _parse_graph_edges(self, payload)` |
| `_parse_graph_nodes` | method | `lazygui/services/teamserver_backend.py:621` | `def _parse_graph_nodes(self, payload)` |
| `_poll_beacon_results` | method | `lazygui/services/teamserver_backend.py:242` | `def _poll_beacon_results(self)` |
| `_post_session_command` | method | `lazygui/services/teamserver_backend.py:346` | `def _post_session_command(self, command, client_id)` |
| `_refresh_dashboard` | method | `lazygui/services/teamserver_backend.py:396` | `def _refresh_dashboard(self)` |
| `_refresh_topology` | method | `lazygui/services/teamserver_backend.py:386` | `def _refresh_topology(self)` |
| `_send_command_via_pty` | method | `lazygui/services/teamserver_backend.py:357` | `def _send_command_via_pty(self, command)` |
| `_start_socketio` | method | `lazygui/services/teamserver_backend.py:443` | `def _start_socketio(self)` |
| `_stop_socketio` | method | `lazygui/services/teamserver_backend.py:520` | `def _stop_socketio(self)` |
| `_update_from_payload` | method | `lazygui/services/teamserver_backend.py:530` | `def _update_from_payload(self, payload)` |
| `_update_listeners` | method | `lazygui/services/teamserver_backend.py:577` | `def _update_listeners(self, payload)` |
| `_update_operator` | method | `lazygui/services/teamserver_backend.py:608` | `def _update_operator(self, payload)` |
| `_update_sessions` | method | `lazygui/services/teamserver_backend.py:537` | `def _update_sessions(self, payload)` |
| `feed_terminal_input` | method | `lazygui/services/teamserver_backend.py:151` | `def feed_terminal_input(self, data)` |
| `known_campaigns` | method | `lazygui/services/teamserver_backend.py:181` | `def known_campaigns(self)` |
| `known_listeners` | method | `lazygui/services/teamserver_backend.py:173` | `def known_listeners(self)` |
| `known_sessions` | method | `lazygui/services/teamserver_backend.py:169` | `def known_sessions(self)` |
| `known_topology` | method | `lazygui/services/teamserver_backend.py:177` | `def known_topology(self)` |
| `refresh` | method | `lazygui/services/teamserver_backend.py:124` | `def refresh(self)` |
| `request_beacon_history` | method | `lazygui/services/teamserver_backend.py:224` | `def request_beacon_history(self, client_id)` |
| `request_beacon_results` | method | `lazygui/services/teamserver_backend.py:185` | `def request_beacon_results(self, client_id)` |
| `request_world_model` | method | `lazygui/services/teamserver_backend.py:210` | `def request_world_model(self)` |
| `resize_terminal` | method | `lazygui/services/teamserver_backend.py:139` | `def resize_terminal(self, columns, rows)` |
| `send_command` | method | `lazygui/services/teamserver_backend.py:112` | `def send_command(self, command, target_session)` |
| `start` | method | `lazygui/services/teamserver_backend.py:80` | `def start(self)` |
| `stop` | method | `lazygui/services/teamserver_backend.py:97` | `def stop(self)` |
| `ThemeManager` | class | `lazygui/theme/manager.py:26` | `class ThemeManager(QObject)` |
| `__init__` | method | `lazygui/theme/manager.py:31` | `def __init__(self, constants, settings, application, palettes, parent)` |
| `_apply_to_application` | method | `lazygui/theme/manager.py:103` | `def _apply_to_application(self, tokens)` |
| `_build_qpalette` | method | `lazygui/theme/manager.py:109` | `def _build_qpalette(tokens)` |
| `active_id` | method | `lazygui/theme/manager.py:64` | `def active_id(self)` |
| `active_tokens` | method | `lazygui/theme/manager.py:57` | `def active_tokens(self)` |
| `apply` | method | `lazygui/theme/manager.py:80` | `def apply(self, identifier)` |
| `apply_initial` | method | `lazygui/theme/manager.py:72` | `def apply_initial(self)` |
| `available` | method | `lazygui/theme/manager.py:68` | `def available(self)` |
| `cycle` | method | `lazygui/theme/manager.py:93` | `def cycle(self)` |
| `builtin_palettes` | function | `lazygui/theme/palettes/__init__.py:23` | `def builtin_palettes()` |
| `QssBuilder` | class | `lazygui/theme/qss_builder.py:16` | `class QssBuilder` |
| `_font_stack` | method | `lazygui/theme/qss_builder.py:39` | `def _font_stack(stack)` |
| `build` | method | `lazygui/theme/qss_builder.py:21` | `def build(self, tokens)` |
| `ThemeTokens` | class | `lazygui/theme/tokens.py:14` | `class ThemeTokens` |
| `BeaconCommandModal` | class | `lazygui/widgets/beacon_command_modal.py:44` | `class BeaconCommandModal(QDialog)` |
| `_HistoryEntry` | class | `lazygui/widgets/beacon_command_modal.py:35` | `class _HistoryEntry` |
| `__init__` | method | `lazygui/widgets/beacon_command_modal.py:53` | `def __init__(self, backend, parent)` |
| `_build_ui` | method | `lazygui/widgets/beacon_command_modal.py:75` | `def _build_ui(self)` |
| `_last_entry` | method | `lazygui/widgets/beacon_command_modal.py:201` | `def _last_entry(self, index)` |
| `_on_beacon_result` | method | `lazygui/widgets/beacon_command_modal.py:209` | `def _on_beacon_result(self, result)` |
| `_on_history_clicked` | method | `lazygui/widgets/beacon_command_modal.py:196` | `def _on_history_clicked(self, item)` |
| `_on_sessions_changed` | method | `lazygui/widgets/beacon_command_modal.py:168` | `def _on_sessions_changed(self, sessions)` |
| `_on_target_changed` | method | `lazygui/widgets/beacon_command_modal.py:127` | `def _on_target_changed(self, _text)` |
| `_reload_history` | method | `lazygui/widgets/beacon_command_modal.py:131` | `def _reload_history(self)` |
| `_selected_target` | method | `lazygui/widgets/beacon_command_modal.py:122` | `def _selected_target(self)` |
| `_send_command` | method | `lazygui/widgets/beacon_command_modal.py:182` | `def _send_command(self)` |
| `focus_input` | method | `lazygui/widgets/beacon_command_modal.py:227` | `def focus_input(self)` |
| `open` | method | `lazygui/widgets/beacon_command_modal.py:216` | `def open(self)` |
| `CommandPaletteAction` | class | `lazygui/widgets/command_palette_list.py:16` | `class CommandPaletteAction` |
| `CommandPaletteList` | class | `lazygui/widgets/command_palette_list.py:28` | `class CommandPaletteList(QListView)` |
| `__init__` | method | `lazygui/widgets/command_palette_list.py:33` | `def __init__(self, constants, actions, parent)` |
| `_fuzzy_score` | function | `lazygui/widgets/command_palette_list.py:99` | `def _fuzzy_score(query, title, subtitle)` |
| `_on_activated` | method | `lazygui/widgets/command_palette_list.py:85` | `def _on_activated(self, _index)` |
| `_populate` | method | `lazygui/widgets/command_palette_list.py:89` | `def _populate(self, actions)` |
| `_token_order_score` | function | `lazygui/widgets/command_palette_list.py:114` | `def _token_order_score(query, haystack, base_offset)` |
| `apply_filter` | method | `lazygui/widgets/command_palette_list.py:58` | `def apply_filter(self, query)` |
| `invoke_current` | method | `lazygui/widgets/command_palette_list.py:76` | `def invoke_current(self)` |
| `set_actions` | method | `lazygui/widgets/command_palette_list.py:53` | `def set_actions(self, actions)` |
| `EventLogView` | class | `lazygui/widgets/event_log_view.py:20` | `class EventLogView(QTreeWidget)` |
| `__init__` | method | `lazygui/widgets/event_log_view.py:23` | `def __init__(self, constants, event_log, parent)` |
| `_append_record` | method | `lazygui/widgets/event_log_view.py:71` | `def _append_record(self, record)` |
| `_on_record_appended` | method | `lazygui/widgets/event_log_view.py:65` | `def _on_record_appended(self, record)` |
| `minimum_level` | method | `lazygui/widgets/event_log_view.py:61` | `def minimum_level(self)` |
| `set_minimum_level` | method | `lazygui/widgets/event_log_view.py:51` | `def set_minimum_level(self, level)` |
| `FilterBar` | class | `lazygui/widgets/filter_bar.py:11` | `class FilterBar(QWidget)` |
| `__init__` | method | `lazygui/widgets/filter_bar.py:16` | `def __init__(self, constants, placeholder_text, label_text, parent)` |
| `_emit_filter_changed` | method | `lazygui/widgets/filter_bar.py:54` | `def _emit_filter_changed(self)` |
| `_on_text_changed` | method | `lazygui/widgets/filter_bar.py:50` | `def _on_text_changed(self, _value)` |
| `clear` | method | `lazygui/widgets/filter_bar.py:46` | `def clear(self)` |
| `text` | method | `lazygui/widgets/filter_bar.py:42` | `def text(self)` |
| `GraphEdgeItem` | class | `lazygui/widgets/graph_view.py:285` | `class GraphEdgeItem(QGraphicsLineItem)` |
| `GraphNodeItem` | class | `lazygui/widgets/graph_view.py:140` | `class GraphNodeItem(QGraphicsEllipseItem)` |
| `GraphNodeState` | class | `lazygui/widgets/graph_view.py:132` | `class GraphNodeState` |
| `GraphScene` | class | `lazygui/widgets/graph_view.py:334` | `class GraphScene(QGraphicsScene)` |
| `GraphView` | class | `lazygui/widgets/graph_view.py:499` | `class GraphView(QGraphicsView)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:143` | `def __init__(self, node, radius, color, pixmap, on_selected, on_context_menu, label_visible, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:288` | `def __init__(self, edge, source_item, target_item, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:340` | `def __init__(self, constants, parent)` |
| `__init__` | method | `lazygui/widgets/graph_view.py:509` | `def __init__(self, constants, parent)` |
| `_add_edge` | method | `lazygui/widgets/graph_view.py:393` | `def _add_edge(self, edge)` |
| `_add_node` | method | `lazygui/widgets/graph_view.py:369` | `def _add_node(self, node)` |
| `_apply_force_layout` | method | `lazygui/widgets/graph_view.py:402` | `def _apply_force_layout(self)` |
| `_create_label` | method | `lazygui/widgets/graph_view.py:173` | `def _create_label(self)` |
| `_icon_for_node` | function | `lazygui/widgets/graph_view.py:81` | `def _icon_for_node(node)` |
| `_install_physics_timer` | method | `lazygui/widgets/graph_view.py:540` | `def _install_physics_timer(self)` |
| `_load_icon` | function | `lazygui/widgets/graph_view.py:63` | `def _load_icon(name)` |
| `_on_context_menu` | function | `lazygui/widgets/graph_view.py:377` | `def _on_context_menu(nid, pos)` |
| `_on_selected` | function | `lazygui/widgets/graph_view.py:374` | `def _on_selected(nid)` |
| `_resolve_icon_dir` | function | `lazygui/widgets/graph_view.py:47` | `def _resolve_icon_dir()` |
| `_resolve_node_color` | function | `lazygui/widgets/graph_view.py:575` | `def _resolve_node_color(node)` |
| `_resolve_node_radius` | function | `lazygui/widgets/graph_view.py:584` | `def _resolve_node_radius(node)` |
| `_tick_physics` | method | `lazygui/widgets/graph_view.py:548` | `def _tick_physics(self)` |
| `_update_position` | method | `lazygui/widgets/graph_view.py:313` | `def _update_position(self)` |
| `edge_data` | method | `lazygui/widgets/graph_view.py:329` | `def edge_data(self)` |
| `fit_to_content` | method | `lazygui/widgets/graph_view.py:565` | `def fit_to_content(self)` |
| `hoverEnterEvent` | method | `lazygui/widgets/graph_view.py:266` | `def hoverEnterEvent(self, event)` |
| `hoverLeaveEvent` | method | `lazygui/widgets/graph_view.py:273` | `def hoverLeaveEvent(self, event)` |
| `itemChange` | method | `lazygui/widgets/graph_view.py:279` | `def itemChange(self, change, value)` |
| `mousePressEvent` | method | `lazygui/widgets/graph_view.py:248` | `def mousePressEvent(self, event)` |
| `mouseReleaseEvent` | method | `lazygui/widgets/graph_view.py:259` | `def mouseReleaseEvent(self, event)` |
| `node_data` | method | `lazygui/widgets/graph_view.py:186` | `def node_data(self)` |
| `paint` | method | `lazygui/widgets/graph_view.py:190` | `def paint(self, painter, option, widget)` |
| `scene_handle` | method | `lazygui/widgets/graph_view.py:570` | `def scene_handle(self)` |
| `selected_node_id` | method | `lazygui/widgets/graph_view.py:491` | `def selected_node_id(self)` |
| `selected_node_id` | method | `lazygui/widgets/graph_view.py:561` | `def selected_node_id(self)` |
| `set_theme_colors` | method | `lazygui/widgets/graph_view.py:527` | `def set_theme_colors(self, bg_color, edge_color)` |
| `set_topology` | method | `lazygui/widgets/graph_view.py:349` | `def set_topology(self, topology)` |
| `set_topology` | method | `lazygui/widgets/graph_view.py:535` | `def set_topology(self, topology)` |
| `step_physics` | method | `lazygui/widgets/graph_view.py:419` | `def step_physics(self)` |
| `update_position` | method | `lazygui/widgets/graph_view.py:324` | `def update_position(self)` |
| `wheelEvent` | method | `lazygui/widgets/graph_view.py:551` | `def wheelEvent(self, event)` |
| `StatusBadge` | class | `lazygui/widgets/status_badge.py:18` | `class StatusBadge(QLabel)` |
| `__init__` | method | `lazygui/widgets/status_badge.py:21` | `def __init__(self, parent)` |
| `set_status` | method | `lazygui/widgets/status_badge.py:27` | `def set_status(self, status)` |
| `TerminalView` | class | `lazygui/widgets/terminal_view.py:33` | `class TerminalView(QPlainTextEdit)` |
| `__init__` | method | `lazygui/widgets/terminal_view.py:38` | `def __init__(self, constants, parent)` |
| `_sanitize` | method | `lazygui/widgets/terminal_view.py:66` | `def _sanitize(raw)` |
| `_translate_key_event` | method | `lazygui/widgets/terminal_view.py:85` | `def _translate_key_event(event)` |
| `append_output` | method | `lazygui/widgets/terminal_view.py:54` | `def append_output(self, text)` |
| `keyPressEvent` | method | `lazygui/widgets/terminal_view.py:75` | `def keyPressEvent(self, event)` |
| `CommandPaletteWindow` | class | `lazygui/windows/command_palette_window.py:15` | `class CommandPaletteWindow(QWidget)` |
| `__init__` | method | `lazygui/windows/command_palette_window.py:18` | `def __init__(self, constants, actions, parent)` |
| `_on_action_invoked` | method | `lazygui/windows/command_palette_window.py:77` | `def _on_action_invoked(self, action)` |
| `keyPressEvent` | method | `lazygui/windows/command_palette_window.py:48` | `def keyPressEvent(self, event)` |
| `set_actions` | method | `lazygui/windows/command_palette_window.py:43` | `def set_actions(self, actions)` |
| `showEvent` | method | `lazygui/windows/command_palette_window.py:71` | `def showEvent(self, event)` |
| `ConnectDialog` | class | `lazygui/windows/connect_dialog.py:50` | `class ConnectDialog(QDialog)` |
| `ConnectionRequest` | class | `lazygui/windows/connect_dialog.py:39` | `class ConnectionRequest` |
| `__init__` | method | `lazygui/windows/connect_dialog.py:53` | `def __init__(self, constants, settings, paths, parent)` |
| `_build_local_page` | method | `lazygui/windows/connect_dialog.py:135` | `def _build_local_page(self)` |
| `_build_teamserver_page` | method | `lazygui/windows/connect_dialog.py:150` | `def _build_teamserver_page(self)` |
| `_on_kind_changed` | method | `lazygui/windows/connect_dialog.py:186` | `def _on_kind_changed(self, index)` |
| `_restore_last_choice` | method | `lazygui/windows/connect_dialog.py:168` | `def _restore_last_choice(self)` |
| `persist_choice` | method | `lazygui/windows/connect_dialog.py:120` | `def persist_choice(self)` |
| `request` | method | `lazygui/windows/connect_dialog.py:105` | `def request(self)` |
| `MainWindow` | class | `lazygui/windows/main_window.py:37` | `class MainWindow(QMainWindow)` |
| `__init__` | method | `lazygui/windows/main_window.py:40` | `def __init__(self, constants, settings, theme_manager, backend, event_log, parent)` |
| `_apply` | function | `lazygui/windows/main_window.py:314` | `def _apply()` |
| `_build_palette_actions` | method | `lazygui/windows/main_window.py:261` | `def _build_palette_actions(self)` |
| `_emit_request_connect` | method | `lazygui/windows/main_window.py:372` | `def _emit_request_connect(self)` |
| `_install_layout` | method | `lazygui/windows/main_window.py:108` | `def _install_layout(self)` |
| `_install_menu_bar` | method | `lazygui/windows/main_window.py:131` | `def _install_menu_bar(self)` |
| `_install_shortcuts` | method | `lazygui/windows/main_window.py:220` | `def _install_shortcuts(self)` |
| `_install_statusbar` | method | `lazygui/windows/main_window.py:195` | `def _install_statusbar(self)` |
| `_install_toolbar` | method | `lazygui/windows/main_window.py:171` | `def _install_toolbar(self)` |
| `_make_panel_toggle` | method | `lazygui/windows/main_window.py:300` | `def _make_panel_toggle(self, panel)` |
| `_make_theme_apply` | method | `lazygui/windows/main_window.py:311` | `def _make_theme_apply(self, identifier)` |
| `_on_dashboard_updated` | method | `lazygui/windows/main_window.py:350` | `def _on_dashboard_updated(self, dashboard)` |
| `_on_event_logged` | method | `lazygui/windows/main_window.py:326` | `def _on_event_logged(self, _record)` |
| `_on_operator_changed` | method | `lazygui/windows/main_window.py:319` | `def _on_operator_changed(self, operator)` |
| `_on_sessions_count_changed` | method | `lazygui/windows/main_window.py:345` | `def _on_sessions_count_changed(self, sessions)` |
| `_on_theme_changed` | method | `lazygui/windows/main_window.py:329` | `def _on_theme_changed(self, tokens)` |
| `_on_theme_menu_action` | method | `lazygui/windows/main_window.py:337` | `def _on_theme_menu_action(self)` |
| `_persist_geometry_and_state` | method | `lazygui/windows/main_window.py:244` | `def _persist_geometry_and_state(self)` |
| `_restore_geometry_and_state` | method | `lazygui/windows/main_window.py:252` | `def _restore_geometry_and_state(self)` |
| `_show_beacon_command_modal` | method | `lazygui/windows/main_window.py:354` | `def _show_beacon_command_modal(self)` |
| `_show_command_palette` | method | `lazygui/windows/main_window.py:361` | `def _show_command_palette(self)` |
| `_tick_clock` | method | `lazygui/windows/main_window.py:386` | `def _tick_clock(self)` |
| `_toggle` | function | `lazygui/windows/main_window.py:303` | `def _toggle()` |
| `closeEvent` | method | `lazygui/windows/main_window.py:99` | `def closeEvent(self, event)` |
| `panels` | method | `lazygui/windows/main_window.py:398` | `def panels(self)` |
| `status_badge` | method | `lazygui/windows/main_window.py:393` | `def status_badge(self)` |
| `window_requests_connect` | method | `lazygui/windows/main_window.py:376` | `def window_requests_connect(self)` |
| `extract_ips_from_arp` | function | `lazyown-docker/hostdiscover.sh:21` | `` |
| `extract_listening_ips_from_netstat` | function | `lazyown-docker/hostdiscover.sh:26` | `` |
| `build_image` | function | `lazyown-docker/mkdocker.sh:93` | `` |
| `check_docker` | function | `lazyown-docker/mkdocker.sh:41` | `` |
| `check_file` | function | `lazyown-docker/mkdocker.sh:49` | `` |
| `clean_container_and_image` | function | `lazyown-docker/mkdocker.sh:197` | `` |
| `container_exists` | function | `lazyown-docker/mkdocker.sh:58` | `` |
| `get_ports` | function | `lazyown-docker/mkdocker.sh:68` | `` |
| `image_exists` | function | `lazyown-docker/mkdocker.sh:63` | `` |
| `log` | function | `lazyown-docker/mkdocker.sh:36` | `` |
| `run_container` | function | `lazyown-docker/mkdocker.sh:117` | `` |
| `stop_container` | function | `lazyown-docker/mkdocker.sh:187` | `` |
| `usage` | function | `lazyown-docker/mkdocker.sh:23` | `` |
| `validate_payload` | function | `lazyown-docker/mkdocker.sh:109` | `` |
| `LazyOwnShell` | class | `lazyown.py:298` | `class LazyOwnShell(Cmd)` |
| `_PayloadSettableProxy` | class | `lazyown.py:233` | `class _PayloadSettableProxy` |
| `__getattr__` | method | `lazyown.py:249` | `def __getattr__(self, name)` |
| `__init__` | method | `lazyown.py:245` | `def __init__(self, params)` |
| `__init__` | method | `lazyown.py:373` | `def __init__(self)` |
| `__setattr__` | method | `lazyown.py:255` | `def __setattr__(self, name, value)` |
| `_build_chain_prompt_engine` | method | `lazyown.py:1029` | `def _build_chain_prompt_engine(self)` |
| `_build_command_stack` | method | `lazyown.py:4854` | `def _build_command_stack(self, adversary, r)` |
| `_build_scope_offensive` | method | `lazyown.py:1670` | `def _build_scope_offensive(self)` |
| `_chain_boot_prompt` | method | `lazyown.py:1014` | `def _chain_boot_prompt(self)` |
| `_chain_part_exists` | method | `lazyown.py:1642` | `def _chain_part_exists(self, part)` |
| `_chain_perror` | function | `lazyown.py:1597` | `def _chain_perror()` |
| `_chain_resolver` | method | `lazyown.py:1054` | `def _chain_resolver(self, cmd, phase)` |
| `_create_strict_yaml_prompt` | method | `lazyown.py:4662` | `def _create_strict_yaml_prompt(self, base_prompt, nmap_services, knowledge_base)` |
| `_did_you_mean` | method | `lazyown.py:1239` | `def _did_you_mean(self, query, limit)` |
| `_display_adversary_info` | method | `lazyown.py:4868` | `def _display_adversary_info(self, adversary, commands)` |
| `_execute_commands` | method | `lazyown.py:4875` | `def _execute_commands(self, confirm, remote_cmds)` |
| `_handler` | function | `lazyown.py:1135` | `def _handler(received, frame, _signum)` |
| `_install_crypto_signal_handlers` | method | `lazyown.py:1118` | `def _install_crypto_signal_handlers(self)` |
| `_load_adversaries` | method | `lazyown.py:4821` | `def _load_adversaries(self)` |
| `_load_extended_params` | method | `lazyown.py:744` | `def _load_extended_params(self)` |
| `_maybe_chain_prompt` | method | `lazyown.py:1072` | `def _maybe_chain_prompt(self, cmd, phase)` |
| `_parse_adversary_args` | method | `lazyown.py:4835` | `def _parse_adversary_args(self, line)` |

Next: [SYMBOLS_p10.md](SYMBOLS_p10.md)
