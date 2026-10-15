# Symbols (page 8 of 40)
Previous: [SYMBOLS_p7.md](SYMBOLS_p7.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `t_send` | function | `fast_run_as_r00t.sh:114` | `` |
| `download_file` | function | `install.sh:251` | `` |
| `ensure_gum` | function | `install.sh:128` | `` |
| `generate_certificates` | function | `install.sh:274` | `` |
| `install_encoder_module` | function | `install.sh:263` | `` |
| `install_external_storage` | function | `install.sh:218` | `` |
| `install_external_tools` | function | `install.sh:150` | `` |
| `install_lazyownbt` | function | `install.sh:231` | `` |
| `install_ollama` | function | `install.sh:206` | `` |
| `install_python_environment` | function | `install.sh:165` | `` |
| `install_system_packages` | function | `install.sh:139` | `` |
| `log` | function | `install.sh:88` | `` |
| `main` | function | `install.sh:310` | `` |
| `seed_payload_config` | function | `install.sh:281` | `` |
| `spin_run` | function | `install.sh:98` | `` |
| `usage` | function | `install.sh:49` | `` |
| `verify_installation` | function | `install.sh:294` | `` |
| `main` | function | `key.py:10` | `def main()` |
| `Alert` | class | `lazy_sentinel4.py:271` | `class Alert` |
| `App` | class | `lazy_sentinel4.py:544` | `class App(Cmd)` |
| `Database` | class | `lazy_sentinel4.py:214` | `class Database` |
| `LazySentinel` | class | `lazy_sentinel4.py:340` | `class LazySentinel` |
| `LazySentinelHandler` | class | `lazy_sentinel4.py:302` | `class LazySentinelHandler(FileSystemEventHandler)` |
| `RAGManager` | class | `lazy_sentinel4.py:58` | `class RAGManager` |
| `__init__` | method | `lazy_sentinel4.py:61` | `def __init__(self, model_name, cache_size)` |
| `__init__` | method | `lazy_sentinel4.py:215` | `def __init__(self, db_path)` |
| `__init__` | method | `lazy_sentinel4.py:274` | `def __init__(self, alert_type, details, severity)` |
| `__init__` | method | `lazy_sentinel4.py:303` | `def __init__(self, lazysentinel)` |
| `__init__` | method | `lazy_sentinel4.py:341` | `def __init__(self, app, popup_queue, watch_dir, excluded_files, min_file_size)` |
| `__init__` | method | `lazy_sentinel4.py:545` | `def __init__(self)` |
| `chunk_text` | method | `lazy_sentinel4.py:361` | `def chunk_text(self, text, chunk_size)` |
| `complete_rag_add` | method | `lazy_sentinel4.py:699` | `def complete_rag_add(self, text, line, begidx, endidx)` |
| `complete_rag_bulk_add` | method | `lazy_sentinel4.py:706` | `def complete_rag_bulk_add(self, text, line, begidx, endidx)` |
| `display_toastr` | method | `lazy_sentinel4.py:559` | `def display_toastr(self, file_name, relevant_info, commands, details, severity, duration)` |
| `do_debug` | method | `lazy_sentinel4.py:615` | `def do_debug(self, arg)` |
| `do_quit` | method | `lazy_sentinel4.py:611` | `def do_quit(self, arg)` |
| `do_rag_add` | method | `lazy_sentinel4.py:632` | `def do_rag_add(self, arg)` |
| `do_rag_bulk_add` | method | `lazy_sentinel4.py:659` | `def do_rag_bulk_add(self, arg)` |
| `do_rag_query` | method | `lazy_sentinel4.py:624` | `def do_rag_query(self, arg)` |
| `do_rag_search` | method | `lazy_sentinel4.py:678` | `def do_rag_search(self, arg)` |
| `do_rag_status` | method | `lazy_sentinel4.py:647` | `def do_rag_status(self, arg)` |
| `do_rag_toggle` | method | `lazy_sentinel4.py:654` | `def do_rag_toggle(self, arg)` |
| `execute` | method | `lazy_sentinel4.py:243` | `def execute(self, query, params)` |
| `get_cache_key` | method | `lazy_sentinel4.py:85` | `def get_cache_key(self, content)` |
| `get_knowledge_base_stats` | method | `lazy_sentinel4.py:191` | `def get_knowledge_base_stats(self)` |
| `initialize` | method | `lazy_sentinel4.py:219` | `def initialize(self)` |
| `initialize_cache_table` | method | `lazy_sentinel4.py:73` | `def initialize_cache_table(self)` |
| `insert` | method | `lazy_sentinel4.py:255` | `def insert(self, query, params)` |
| `invalidate_cache` | method | `lazy_sentinel4.py:177` | `def invalidate_cache(self, file_path)` |
| `is_text_file` | method | `lazy_sentinel4.py:306` | `def is_text_file(self, file_path)` |
| `load_existing_vectorstore` | method | `lazy_sentinel4.py:88` | `def load_existing_vectorstore(self)` |
| `ollama_llm` | method | `lazy_sentinel4.py:101` | `def ollama_llm(self, question, context)` |
| `on_created` | method | `lazy_sentinel4.py:316` | `def on_created(self, event)` |
| `on_modified` | method | `lazy_sentinel4.py:328` | `def on_modified(self, event)` |
| `parse_deepseek_response` | method | `lazy_sentinel4.py:378` | `def parse_deepseek_response(self, response_text)` |
| `postcmd` | method | `lazy_sentinel4.py:587` | `def postcmd(self, stop, line)` |
| `process_file` | method | `lazy_sentinel4.py:422` | `def process_file(self, file_path)` |
| `process_file_to_rag` | method | `lazy_sentinel4.py:115` | `def process_file_to_rag(self, file_path)` |
| `query_rag` | method | `lazy_sentinel4.py:155` | `def query_rag(self, question)` |
| `sanitize_content` | function | `lazy_sentinel4.py:47` | `def sanitize_content(text)` |
| `save_to_db` | method | `lazy_sentinel4.py:288` | `def save_to_db(self, db)` |
| `select_relevant_chunk` | method | `lazy_sentinel4.py:364` | `def select_relevant_chunk(self, file_content, chunks)` |
| `show_popup` | method | `lazy_sentinel4.py:404` | `def show_popup(self, file_name, relevant_info, commands, details)` |
| `stop` | method | `lazy_sentinel4.py:538` | `def stop(self)` |
| `to_dict` | method | `lazy_sentinel4.py:280` | `def to_dict(self)` |
| `CustomDNSResolver` | class | `lazyc2.py:1728` | `class CustomDNSResolver(BaseResolver)` |
| `Handler` | class | `lazyc2.py:728` | `class Handler(FileSystemEventHandler)` |
| `User` | class | `lazyc2.py:2964` | `class User(UserMixin)` |
| `_JsonLogFormatter` | class | `lazyc2.py:441` | `class _JsonLogFormatter(Formatter)` |
| `_LazyShellProxy` | class | `lazyc2.py:2621` | `class _LazyShellProxy` |
| `__getattr__` | function | `lazyc2.py:2601` | `def __getattr__(name)` |
| `__getattr__` | method | `lazyc2.py:2633` | `def __getattr__(self, name)` |
| `__init__` | method | `lazyc2.py:2965` | `def __init__(self, user_data)` |
| `__setattr__` | method | `lazyc2.py:2637` | `def __setattr__(self, name, value)` |
| `_add_security_headers` | function | `lazyc2.py:2473` | `def _add_security_headers(response)` |
| `_api_data_inner` | function | `lazyc2.py:4330` | `def _api_data_inner()` |
| `_append_beacon_record` | function | `lazyc2.py:1260` | `def _append_beacon_record(record)` |
| `_beacon_records_path` | function | `lazyc2.py:1253` | `def _beacon_records_path(client_id)` |
| `_bg_cred_reuse` | function | `lazyc2.py:3713` | `def _bg_cred_reuse(_ip)` |
| `_bootstrap_initial_admin` | function | `lazyc2.py:2688` | `def _bootstrap_initial_admin()` |
| `_build_privesc_command` | function | `lazyc2.py:3310` | `def _build_privesc_command(platform)` |
| `_enforce_https_redirect` | function | `lazyc2.py:2430` | `def _enforce_https_redirect()` |
| `_enforce_password_rotation` | function | `lazyc2.py:2450` | `def _enforce_password_rotation()` |
| `_engage_publish` | function | `lazyc2.py:3497` | `def _engage_publish(_cid, _ip, _host, _user, _platform)` |
| `_env_tag` | function | `lazyc2.py:192` | `def _env_tag()` |
| `_events` | function | `lazyc2.py:7254` | `def _events()` |
| `_extract_first_ip` | function | `lazyc2.py:3553` | `def _extract_first_ip(raw)` |
| `_get_rbac_user_obj` | function | `lazyc2.py:2977` | `def _get_rbac_user_obj(flask_user)` |
| `_handle_404` | function | `lazyc2.py:2540` | `def _handle_404(_error)` |
| `_handle_405` | function | `lazyc2.py:2545` | `def _handle_405(_error)` |
| `_handle_exception` | function | `lazyc2.py:2550` | `def _handle_exception(error)` |
| `_ingest_beacon` | function | `lazyc2.py:3746` | `def _ingest_beacon(_ips, _host, _cmd, _out, _user)` |
| `_init_shell` | function | `lazyc2.py:2574` | `def _init_shell()` |
| `_is_unspecified_bind_literal` | function | `lazyc2.py:279` | `def _is_unspecified_bind_literal(address)` |
| `_is_valid_credential` | function | `lazyc2.py:3566` | `def _is_valid_credential(value)` |
| `_listen_address` | function | `lazyc2.py:252` | `def _listen_address()` |
| `_load_or_create_secret_key` | function | `lazyc2.py:2493` | `def _load_or_create_secret_key()` |
| `_load_reverse_shell_password` | function | `lazyc2.py:4869` | `def _load_reverse_shell_password(secret_path)` |
| `_log_dns_bind_failure` | function | `lazyc2.py:1794` | `def _log_dns_bind_failure(address, error_number)` |
| `_metrics_before_request` | function | `lazyc2.py:2424` | `def _metrics_before_request()` |
| `_normalise_platform` | function | `lazyc2.py:3595` | `def _normalise_platform(raw_platform)` |
| `_persist_bootstrap_password` | function | `lazyc2.py:2668` | `def _persist_bootstrap_password(prefix, password)` |
| `_probe_bind` | function | `lazyc2.py:331` | `def _probe_bind(address, port, sock_type)` |
| `_queue_beacon_cmd` | function | `lazyc2.py:3606` | `def _queue_beacon_cmd(action, ctx)` |
| `_read_beacon_records` | function | `lazyc2.py:1290` | `def _read_beacon_records(client_id)` |
| `_render_enhanced_report` | function | `lazyc2.py:6607` | `def _render_enhanced_report()` |
| `_render_legacy_report` | function | `lazyc2.py:6627` | `def _render_legacy_report()` |
| `_resolve_bind_address` | function | `lazyc2.py:376` | `def _resolve_bind_address(preferred, port, sock_type)` |
| `_resolve_reverse_shell_password` | function | `lazyc2.py:4883` | `def _resolve_reverse_shell_password()` |
| `_resolve_secure_template_path` | function | `lazyc2.py:3995` | `def _resolve_secure_template_path(template_name)` |
| `_resolve_within` | function | `lazyc2.py:629` | `def _resolve_within(allowed_base, name)` |
| `_sanitize_command_output` | function | `lazyc2.py:559` | `def _sanitize_command_output(value)` |
| `_sanitize_csv_field` | function | `lazyc2.py:1210` | `def _sanitize_csv_field(value, maxlen)` |
| `_sanitize_html` | function | `lazyc2.py:1173` | `def _sanitize_html(raw_html)` |
| `_seal_reverse_shell_password` | function | `lazyc2.py:4855` | `def _seal_reverse_shell_password(plaintext)` |
| `_secure_command_queue_path` | function | `lazyc2.py:1223` | `def _secure_command_queue_path(client_id)` |
| `_select_specific_bind_address` | function | `lazyc2.py:298` | `def _select_specific_bind_address(candidate)` |
| `_target` | method | `lazyc2.py:2629` | `def _target(self)` |
| `_try_copy_privesc_tool` | function | `lazyc2.py:3290` | `def _try_copy_privesc_tool(platform)` |
| `add_dynamic_data` | function | `lazyc2.py:2104` | `def add_dynamic_data(data)` |
| `admin_create_tenant` | function | `lazyc2.py:6073` | `def admin_create_tenant()` |
| `admin_delete_user` | function | `lazyc2.py:6034` | `def admin_delete_user(user_id)` |
| `admin_reset_mfa` | function | `lazyc2.py:6022` | `def admin_reset_mfa(user_id)` |
| `admin_set_role` | function | `lazyc2.py:6000` | `def admin_set_role(user_id)` |
| `admin_switch_tenant` | function | `lazyc2.py:6093` | `def admin_switch_tenant(tenant_id)` |
| `admin_tenants` | function | `lazyc2.py:6052` | `def admin_tenants()` |
| `admin_users` | function | `lazyc2.py:5985` | `def admin_users()` |
| `adversary` | function | `lazyc2.py:5101` | `def adversary()` |
| `aicmd` | function | `lazyc2.py:1539` | `def aicmd(cmd)` |
| `aicmd_deepseek` | function | `lazyc2.py:1425` | `def aicmd_deepseek(cmd)` |
| `aicmd_view` | function | `lazyc2.py:5527` | `def aicmd_view()` |
| `analyze_behavioral_data` | function | `lazyc2.py:2358` | `def analyze_behavioral_data(behavioral_events)` |
| `analyze_campaign_progress` | function | `lazyc2.py:2386` | `def analyze_campaign_progress(campaign_id, events)` |
| `api_attack_bundle` | function | `lazyc2.py:7520` | `def api_attack_bundle()` |
| `api_attack_graph` | function | `lazyc2.py:7468` | `def api_attack_graph()` |
| `api_beacon_results` | function | `lazyc2.py:6592` | `def api_beacon_results(client_id)` |
| `api_dashboard` | function | `lazyc2.py:8098` | `def api_dashboard()` |
| `api_data` | function | `lazyc2.py:4307` | `def api_data()` |
| `api_guard_audit` | function | `lazyc2.py:7322` | `def api_guard_audit()` |
| `api_intel_bundle` | function | `lazyc2.py:7435` | `def api_intel_bundle()` |
| `api_intel_graph` | function | `lazyc2.py:7151` | `def api_intel_graph()` |
| `api_killchain` | function | `lazyc2.py:6561` | `def api_killchain()` |
| `api_lazy_mentions` | function | `lazyc2.py:7399` | `def api_lazy_mentions()` |
| `api_listeners` | function | `lazyc2.py:8168` | `def api_listeners()` |
| `api_listeners_create` | function | `lazyc2.py:8175` | `def api_listeners_create()` |
| `api_listeners_delete` | function | `lazyc2.py:8207` | `def api_listeners_delete(listener_id)` |
| `api_listeners_start` | function | `lazyc2.py:8191` | `def api_listeners_start(listener_id)` |
| `api_listeners_stop` | function | `lazyc2.py:8199` | `def api_listeners_stop(listener_id)` |
| `api_loop_broadcast` | function | `lazyc2.py:7279` | `def api_loop_broadcast()` |
| `api_loop_broadcast_stream` | function | `lazyc2.py:7221` | `def api_loop_broadcast_stream()` |
| `api_loop_graph` | function | `lazyc2.py:7368` | `def api_loop_graph()` |
| `api_surface_live` | function | `lazyc2.py:7058` | `def api_surface_live()` |
| `attack3d_view` | function | `lazyc2.py:7117` | `def attack3d_view()` |
| `attack_bundle_view` | function | `lazyc2.py:7136` | `def attack_bundle_view()` |
| `aumentar_elo` | function | `lazyc2.py:1112` | `def aumentar_elo(user_id, cantidad)` |
| `aumentar_elo_route` | function | `lazyc2.py:6213` | `def aumentar_elo_route(user_id)` |
| `authenticate` | function | `lazyc2.py:1363` | `def authenticate()` |
| `banners` | function | `lazyc2.py:6229` | `def banners()` |
| `broadcast_view` | function | `lazyc2.py:7207` | `def broadcast_view()` |
| `campaign_report` | function | `lazyc2.py:7746` | `def campaign_report(campaign_id)` |
| `capture_audio` | function | `lazyc2.py:7019` | `def capture_audio()` |
| `capture_image` | function | `lazyc2.py:6993` | `def capture_image()` |
| `change_password` | function | `lazyc2.py:6147` | `def change_password()` |
| `chatbot` | function | `lazyc2.py:4979` | `def chatbot()` |
| `check_auth` | function | `lazyc2.py:1348` | `def check_auth(username, password)` |
| `clean_expired_tokens` | function | `lazyc2.py:610` | `def clean_expired_tokens()` |
| `clean_json` | function | `lazyc2.py:618` | `def clean_json(text)` |
| `compliance_add_evidence` | function | `lazyc2.py:6390` | `def compliance_add_evidence()` |
| `compliance_dashboard` | function | `lazyc2.py:6338` | `def compliance_dashboard()` |
| `compliance_export` | function | `lazyc2.py:6440` | `def compliance_export(format)` |
| `compliance_report` | function | `lazyc2.py:6360` | `def compliance_report()` |
| `compliance_verify_evidence` | function | `lazyc2.py:6426` | `def compliance_verify_evidence()` |
| `connect` | function | `lazyc2.py:6692` | `def connect()` |
| `create_campaign` | function | `lazyc2.py:7630` | `def create_campaign()` |
| `create_cves` | function | `lazyc2.py:1064` | `def create_cves()` |
| `create_multivector_campaign` | function | `lazyc2.py:7875` | `def create_multivector_campaign()` |
| `create_report` | function | `lazyc2.py:1083` | `def create_report()` |
| `create_route` | function | `lazyc2.py:4062` | `def create_route()` |
| `create_short_url` | function | `lazyc2.py:4469` | `def create_short_url()` |
| `create_tool` | function | `lazyc2.py:5594` | `def create_tool()` |
| `csrf_protect` | function | `lazyc2.py:1404` | `def csrf_protect(view)` |
| `csv_to_html` | function | `lazyc2.py:5133` | `def csv_to_html()` |
| `cve` | function | `lazyc2.py:5336` | `def cve(cve_id)` |
| `cves` | function | `lazyc2.py:5310` | `def cves()` |
| `datetime_now_iso` | function | `lazyc2.py:1218` | `def datetime_now_iso()` |
| `decorated` | function | `lazyc2.py:1382` | `def decorated()` |
| `decorated` | function | `lazyc2.py:1395` | `def decorated()` |
| `decoy` | function | `lazyc2.py:1916` | `def decoy()` |
| `decrypt_data` | function | `lazyc2.py:1963` | `def decrypt_data(encrypted_data, is_file)` |
| `delete_tool` | function | `lazyc2.py:5700` | `def delete_tool(toolname)` |
| `download_file` | function | `lazyc2.py:3933` | `def download_file()` |
| `download_files` | function | `lazyc2.py:4597` | `def download_files(filename)` |
| `dynamic_route` | function | `lazyc2.py:4131` | `def dynamic_route(route_path, data)` |
| `edit_cve` | function | `lazyc2.py:5351` | `def edit_cve(cve_id)` |
| `edit_event` | function | `lazyc2.py:5450` | `def edit_event(event_name)` |
| `edit_notes` | function | `lazyc2.py:5385` | `def edit_notes()` |
| `edit_task` | function | `lazyc2.py:5276` | `def edit_task(task_id)` |
| `encrypt_data` | function | `lazyc2.py:1954` | `def encrypt_data(data)` |
| `ensure_sessions_dir` | function | `lazyc2.py:471` | `def ensure_sessions_dir()` |
| `escape_js` | function | `lazyc2.py:1148` | `def escape_js(s)` |
| `escape_js_string` | function | `lazyc2.py:1336` | `def escape_js_string(value)` |
| `execute_command` | function | `lazyc2.py:1699` | `def execute_command(command)` |
| `extract_attack_vectors` | function | `lazyc2.py:855` | `def extract_attack_vectors(nodes, edges)` |
| `favicon` | function | `lazyc2.py:4245` | `def favicon()` |
| `format` | method | `lazyc2.py:444` | `def format(self, record)` |
| `fromjson` | function | `lazyc2.py:772` | `def fromjson(value)` |
| `generalbot` | function | `lazyc2.py:5117` | `def generalbot()` |
| `get_client_ip` | function | `lazyc2.py:2126` | `def get_client_ip()` |
| `get_config` | function | `lazyc2.py:6974` | `def get_config()` |
| `get_connected_clients` | function | `lazyc2.py:6310` | `def get_connected_clients()` |
| `get_data` | function | `lazyc2.py:7550` | `def get_data()` |
| `get_discovered_hosts` | function | `lazyc2.py:1999` | `def get_discovered_hosts()` |
| `get_event_config` | function | `lazyc2.py:5485` | `def get_event_config()` |
| `get_event_config_view` | function | `lazyc2.py:5492` | `def get_event_config_view()` |
| `get_events` | function | `lazyc2.py:5552` | `def get_events()` |
| `get_karma_name` | function | `lazyc2.py:755` | `def get_karma_name(elo)` |
| `get_local_ip_addresses` | function | `lazyc2.py:2049` | `def get_local_ip_addresses()` |
| `get_notes` | function | `lazyc2.py:5403` | `def get_notes()` |
| `get_output` | function | `lazyc2.py:4812` | `def get_output()` |
| `get_request_details` | function | `lazyc2.py:2135` | `def get_request_details()` |
| `get_results` | function | `lazyc2.py:4848` | `def get_results()` |
| `get_safe_file_path` | function | `lazyc2.py:2288` | `def get_safe_file_path(user_path)` |
| `get_tasks` | function | `lazyc2.py:5256` | `def get_tasks()` |
| `graph` | function | `lazyc2.py:5232` | `def graph()` |
| `handle_client` | function | `lazyc2.py:1897` | `def handle_client(client_socket, remote_host, remote_port)` |
| `handle_input` | function | `lazyc2.py:6789` | `def handle_input(data)` |
| `health_check` | function | `lazyc2.py:8052` | `def health_check()` |
| `implants_check` | function | `lazyc2.py:838` | `def implants_check()` |
| `index` | function | `lazyc2.py:3047` | `def index()` |
| `intel_bundle_view` | function | `lazyc2.py:7102` | `def intel_bundle_view()` |
| `intel_view` | function | `lazyc2.py:7083` | `def intel_view()` |
| `internal_server_error` | function | `lazyc2.py:6965` | `def internal_server_error(e)` |
| `is_binary` | function | `lazyc2.py:569` | `def is_binary(safe_filename)` |
| `is_insecure_credential` | function | `lazyc2.py:204` | `def is_insecure_credential(user, pwd)` |
| `is_safe_template_path` | function | `lazyc2.py:529` | `def is_safe_template_path(template_path, template_name)` |
| `is_valid_data` | function | `lazyc2.py:4155` | `def is_valid_data(data)` |
| `is_valid_route_path` | function | `lazyc2.py:4148` | `def is_valid_route_path(route_path)` |
| `is_valid_template_name` | function | `lazyc2.py:4165` | `def is_valid_template_name(template_name)` |
| `is_valid_url` | function | `lazyc2.py:2280` | `def is_valid_url(url)` |
| `issue_command` | function | `lazyc2.py:3882` | `def issue_command()` |
| `killchain_view` | function | `lazyc2.py:6531` | `def killchain_view()` |
| `lazybot` | function | `lazyc2.py:6321` | `def lazybot()` |
| `lazyphishingai` | function | `lazyc2.py:7708` | `def lazyphishingai()` |
| `lazyreport` | function | `lazyc2.py:6470` | `def lazyreport()` |
| `lazyreport_view` | function | `lazyc2.py:6525` | `def lazyreport_view()` |
| `list_campaigns` | function | `lazyc2.py:7617` | `def list_campaigns()` |
| `list_tools` | function | `lazyc2.py:5584` | `def list_tools()` |
| `listener` | function | `lazyc2.py:6701` | `def listener()` |
| `listener_command` | function | `lazyc2.py:6813` | `def listener_command(msg)` |
| `listener_connect` | function | `lazyc2.py:6710` | `def listener_connect()` |
| `listener_disconnect` | function | `lazyc2.py:6721` | `def listener_disconnect()` |
| `load_banners` | function | `lazyc2.py:786` | `def load_banners()` |
| `load_cves` | function | `lazyc2.py:1070` | `def load_cves()` |
| `load_data` | function | `lazyc2.py:3008` | `def load_data()` |
| `load_event_config` | function | `lazyc2.py:812` | `def load_event_config()` |
| `load_implant_config` | function | `lazyc2.py:2240` | `def load_implant_config(implante)` |
| `load_mitre_data` | function | `lazyc2.py:806` | `def load_mitre_data()` |
| `load_note` | function | `lazyc2.py:1094` | `def load_note()` |
| `load_notifications` | function | `lazyc2.py:820` | `def load_notifications()` |
| `load_routes` | function | `lazyc2.py:482` | `def load_routes()` |
| `load_short_urls` | function | `lazyc2.py:2250` | `def load_short_urls()` |
| `load_tasks` | function | `lazyc2.py:1056` | `def load_tasks()` |
| `load_user` | function | `lazyc2.py:3025` | `def load_user(user_id)` |
| `load_users` | function | `lazyc2.py:2987` | `def load_users()` |
| `load_yaml_safely` | function | `lazyc2.py:646` | `def load_yaml_safely(file_path)` |
| `log` | function | `lazyc2.py:4227` | `def log(data)` |
| `login` | function | `lazyc2.py:5794` | `def login()` |
| `logout` | function | `lazyc2.py:6132` | `def logout()` |
| `make_serializable` | function | `lazyc2.py:1200` | `def make_serializable(data)` |
| `markdown_to_html` | function | `lazyc2.py:1185` | `def markdown_to_html(text)` |
| `metrics_exposition` | function | `lazyc2.py:8091` | `def metrics_exposition()` |
| `mfa_qr` | function | `lazyc2.py:5915` | `def mfa_qr(username)` |
| `mfa_setup` | function | `lazyc2.py:5841` | `def mfa_setup()` |
| `mfa_verify` | function | `lazyc2.py:5937` | `def mfa_verify()` |
| `mitre` | function | `lazyc2.py:6265` | `def mitre()` |
| `on_any_event` | method | `lazyc2.py:730` | `def on_any_event(event)` |
| `orchestrate_campaign` | function | `lazyc2.py:7828` | `def orchestrate_campaign(campaign_id)` |
| `page_not_found` | function | `lazyc2.py:6957` | `def page_not_found(e)` |
| `palette_api` | function | `lazyc2.py:4286` | `def palette_api()` |
| `palette_view` | function | `lazyc2.py:4258` | `def palette_view()` |
| `parse_access_log_for_short_url` | function | `lazyc2.py:2192` | `def parse_access_log_for_short_url(short_url)` |
| `parse_execution_log` | function | `lazyc2.py:2214` | `def parse_execution_log(implante)` |
| `process_bloodhound_zip` | function | `lazyc2.py:942` | `def process_bloodhound_zip(zip_filepath)` |
| `profile` | function | `lazyc2.py:6108` | `def profile()` |
| `pty_connect` | function | `lazyc2.py:6758` | `def pty_connect()` |
| `pty_input` | function | `lazyc2.py:6731` | `def pty_input(data)` |
| `push_notification` | function | `lazyc2.py:5423` | `def push_notification()` |
| `read_and_forward_pty_output` | function | `lazyc2.py:1982` | `def read_and_forward_pty_output()` |
| `receive_result` | function | `lazyc2.py:3341` | `def receive_result(client_id)` |
| `redirect_to_file` | function | `lazyc2.py:4549` | `def redirect_to_file(short_url)` |
| `redop` | function | `lazyc2.py:5082` | `def redop()` |
| `register` | function | `lazyc2.py:5735` | `def register()` |
| `report` | function | `lazyc2.py:6518` | `def report()` |
| `requires_auth` | function | `lazyc2.py:1393` | `def requires_auth(f)` |
| `requires_auth_or_session` | function | `lazyc2.py:1372` | `def requires_auth_or_session(f)` |
| `resize` | function | `lazyc2.py:6745` | `def resize(data)` |
| `resolve` | method | `lazyc2.py:1729` | `def resolve(self, request, handler)` |
| `run_command` | function | `lazyc2.py:4743` | `def run_command()` |
| `run_shell` | function | `lazyc2.py:776` | `def run_shell()` |
| `run_shellcode` | function | `lazyc2.py:4839` | `def run_shellcode()` |
| `sanitize_input` | function | `lazyc2.py:4138` | `def sanitize_input(input_str)` |
| `sanitize_json` | function | `lazyc2.py:2074` | `def sanitize_json(data)` |
| `save_cves` | function | `lazyc2.py:1078` | `def save_cves(cves)` |
| `save_note` | function | `lazyc2.py:1142` | `def save_note(content)` |
| `save_routes` | function | `lazyc2.py:492` | `def save_routes(routes)` |
| `save_short_urls` | function | `lazyc2.py:2270` | `def save_short_urls(data)` |
| `save_tasks` | function | `lazyc2.py:1089` | `def save_tasks(tasks)` |
| `save_to_log` | function | `lazyc2.py:2170` | `def save_to_log(data)` |
| `save_users` | function | `lazyc2.py:2997` | `def save_users(users)` |
| `script` | function | `lazyc2.py:5066` | `def script()` |
| `search` | function | `lazyc2.py:5050` | `def search()` |
| `search_database` | function | `lazyc2.py:1644` | `def search_database(term, data_path)` |
| `search_results` | function | `lazyc2.py:5184` | `def search_results()` |
| `send_command` | function | `lazyc2.py:3197` | `def send_command(client_id)` |
| `send_lcommand` | function | `lazyc2.py:4946` | `def send_lcommand(ip, port)` |
| `serve_file` | function | `lazyc2.py:3960` | `def serve_file(file_path)` |
| `serve_landing_page` | function | `lazyc2.py:8027` | `def serve_landing_page(campaign_id, short_url)` |
| `set_winsize` | function | `lazyc2.py:1976` | `def set_winsize(fd, row, col, xpix, ypix)` |
| `start_bridge` | function | `lazyc2.py:6940` | `def start_bridge()` |
| `start_dns_server` | function | `lazyc2.py:1833` | `def start_dns_server()` |
| `start_reverse_shell` | function | `lazyc2.py:6893` | `def start_reverse_shell()` |
| `start_watching` | function | `lazyc2.py:1040` | `def start_watching()` |
| `surface` | function | `lazyc2.py:7037` | `def surface()` |
| `surface_live` | function | `lazyc2.py:7043` | `def surface_live()` |
| `task` | function | `lazyc2.py:5241` | `def task(task_id)` |
| `taskbot` | function | `lazyc2.py:5034` | `def taskbot()` |
| `tasks` | function | `lazyc2.py:5266` | `def tasks()` |
| `tcp_bridge` | function | `lazyc2.py:1873` | `def tcp_bridge(local_port, remote_host, remote_port)` |
| `teamserver` | function | `lazyc2.py:6489` | `def teamserver()` |
| `terminal` | function | `lazyc2.py:6827` | `def terminal()` |
| `terminal_command` | function | `lazyc2.py:6869` | `def terminal_command(data)` |
| `terminal_connect` | function | `lazyc2.py:6836` | `def terminal_connect()` |
| `terminal_disconnect` | function | `lazyc2.py:6846` | `def terminal_disconnect()` |
| `terminal_input` | function | `lazyc2.py:6856` | `def terminal_input(data)` |
| `terminal_resize` | function | `lazyc2.py:6884` | `def terminal_resize(data)` |
| `to_serializable` | function | `lazyc2.py:1193` | `def to_serializable(obj)` |
| `tojson_filter` | function | `lazyc2.py:3040` | `def tojson_filter(value)` |
| `track_interaction` | function | `lazyc2.py:4497` | `def track_interaction(short_url)` |
| `track_pixel` | function | `lazyc2.py:7724` | `def track_pixel(campaign_id, email)` |
| `update_short_url` | function | `lazyc2.py:4522` | `def update_short_url(short_url)` |
| `update_tool` | function | `lazyc2.py:5652` | `def update_tool(toolname)` |
| `upload` | function | `lazyc2.py:3896` | `def upload()` |
| `upload_zip_file` | function | `lazyc2.py:7559` | `def upload_zip_file()` |
| `validate_route_path` | function | `lazyc2.py:506` | `def validate_route_path(route_path)` |
| `validate_template_name` | function | `lazyc2.py:519` | `def validate_template_name(template_name)` |
| `view_note` | function | `lazyc2.py:5413` | `def view_note()` |
| `view_tool` | function | `lazyc2.py:5621` | `def view_tool(toolname)` |
| `view_yaml` | function | `lazyc2.py:4649` | `def view_yaml()` |
| `vuln` | function | `lazyc2.py:4995` | `def vuln()` |
| `webserver_report` | function | `lazyc2.py:4577` | `def webserver_report(filename)` |
| `wrapper` | function | `lazyc2.py:1414` | `def wrapper()` |
| `AddonCreatorConfig` | class | `lazyc2/addon_creator.py:71` | `class AddonCreatorConfig` |
| `AddonDraft` | class | `lazyc2/addon_creator.py:373` | `class AddonDraft` |
| `AddonStore` | class | `lazyc2/addon_creator.py:808` | `class AddonStore` |
| `AddonValidationError` | class | `lazyc2/addon_creator.py:407` | `class AddonValidationError(ValueError)` |
| `AddonValidator` | class | `lazyc2/addon_creator.py:420` | `class AddonValidator` |
| `AddonYamlRenderer` | class | `lazyc2/addon_creator.py:723` | `class AddonYamlRenderer` |
| `ParamSpec` | class | `lazyc2/addon_creator.py:340` | `class ParamSpec` |
| `ValidationIssue` | class | `lazyc2/addon_creator.py:400` | `class ValidationIssue` |
| `__init__` | method | `lazyc2/addon_creator.py:414` | `def __init__(self, issues)` |
| `__init__` | method | `lazyc2/addon_creator.py:427` | `def __init__(self, draft, config)` |
| `__init__` | method | `lazyc2/addon_creator.py:726` | `def __init__(self, config)` |
| `__init__` | method | `lazyc2/addon_creator.py:817` | `def __init__(self, config, base_dir)` |
| `_atomic_write` | method | `lazyc2/addon_creator.py:926` | `def _atomic_write(self, target, text)` |
| `_check_identity` | method | `lazyc2/addon_creator.py:459` | `def _check_identity(self)` |
| `_check_params` | method | `lazyc2/addon_creator.py:601` | `def _check_params(self)` |
| `_check_placeholders` | method | `lazyc2/addon_creator.py:674` | `def _check_placeholders(self, text, field)` |
| `_check_targeting` | method | `lazyc2/addon_creator.py:503` | `def _check_targeting(self)` |
| `_check_tool` | method | `lazyc2/addon_creator.py:550` | `def _check_tool(self)` |
| `_first_value` | function | `lazyc2/addon_creator.py:1051` | `def _first_value(form, key)` |
| `_is_valid_repo_url` | method | `lazyc2/addon_creator.py:714` | `def _is_valid_repo_url(value)` |
| `_multi_values` | function | `lazyc2/addon_creator.py:1030` | `def _multi_values(form, key)` |
| `_parse_bool` | function | `lazyc2/addon_creator.py:1062` | `def _parse_bool(value)` |
| `_parse_param_rows` | function | `lazyc2/addon_creator.py:1114` | `def _parse_param_rows(form)` |
| `_render_tool` | method | `lazyc2/addon_creator.py:782` | `def _render_tool(self, draft)` |
| `_resolve_target` | method | `lazyc2/addon_creator.py:869` | `def _resolve_target(self, name, pattern)` |
| `delete` | method | `lazyc2/addon_creator.py:979` | `def delete(self, name)` |
| `exists` | method | `lazyc2/addon_creator.py:891` | `def exists(self, name)` |
| `is_valid` | method | `lazyc2/addon_creator.py:455` | `def is_valid(self)` |
| `list_all` | method | `lazyc2/addon_creator.py:995` | `def list_all(self)` |
| `load` | method | `lazyc2/addon_creator.py:956` | `def load(self, name)` |
| `parse_addon_form` | function | `lazyc2/addon_creator.py:1075` | `def parse_addon_form(form)` |
| `render` | method | `lazyc2/addon_creator.py:734` | `def render(self, draft)` |
| `resolve_existing_path` | method | `lazyc2/addon_creator.py:847` | `def resolve_existing_path(self, name)` |
| `resolve_path` | method | `lazyc2/addon_creator.py:832` | `def resolve_path(self, name)` |
| `save` | method | `lazyc2/addon_creator.py:902` | `def save(self, name, yaml_text)` |
| `to_dict` | method | `lazyc2/addon_creator.py:358` | `def to_dict(self)` |
| `to_document` | method | `lazyc2/addon_creator.py:752` | `def to_document(self, draft)` |
| `validate` | method | `lazyc2/addon_creator.py:441` | `def validate(self)` |
| `_add_security_headers` | function | `lazyc2/app_factory.py:167` | `def _add_security_headers(response)` |
| `_build_api_key_store` | function | `lazyc2/app_factory.py:42` | `def _build_api_key_store(payload)` |
| `_handle_404` | function | `lazyc2/app_factory.py:152` | `def _handle_404(_error)` |
| `_handle_405` | function | `lazyc2/app_factory.py:156` | `def _handle_405(_error)` |
| `_handle_exception` | function | `lazyc2/app_factory.py:160` | `def _handle_exception(error)` |
| `_load_or_create_secret_key` | function | `lazyc2/app_factory.py:61` | `def _load_or_create_secret_key(sessions_dir)` |
| `_load_payload_config` | function | `lazyc2/app_factory.py:33` | `def _load_payload_config()` |
| `_make_security_config` | function | `lazyc2/app_factory.py:75` | `def _make_security_config(payload)` |
| `create_app` | function | `lazyc2/app_factory.py:89` | `def create_app()` |
| `_csrf_policy` | function | `lazyc2/blueprints/addons.py:87` | `def _csrf_policy()` |
| `_draft_from_document` | function | `lazyc2/blueprints/addons.py:216` | `def _draft_from_document(document)` |
| `_form_context` | function | `lazyc2/blueprints/addons.py:164` | `def _form_context(draft, issues)` |
| `_issue_csrf` | function | `lazyc2/blueprints/addons.py:120` | `def _issue_csrf(response, policy)` |
| `_issue_map` | function | `lazyc2/blueprints/addons.py:149` | `def _issue_map(issues)` |
| `_render_create` | function | `lazyc2/blueprints/addons.py:193` | `def _render_create(draft, issues)` |
| `_store` | function | `lazyc2/blueprints/addons.py:81` | `def _store()` |
| `create_addon` | function | `lazyc2/blueprints/addons.py:277` | `def create_addon()` |
| `csrf_protect` | function | `lazyc2/blueprints/addons.py:96` | `def csrf_protect(view)` |
| `delete_addon` | function | `lazyc2/blueprints/addons.py:345` | `def delete_addon(name)` |
| `init_addons_bp` | function | `lazyc2/blueprints/addons.py:69` | `def init_addons_bp(base_dir)` |
| `list_addons` | function | `lazyc2/blueprints/addons.py:263` | `def list_addons()` |
| `view_addon` | function | `lazyc2/blueprints/addons.py:321` | `def view_addon(name)` |
| `wrapper` | function | `lazyc2/blueprints/addons.py:110` | `def wrapper()` |
| `HealthConfig` | class | `lazyc2/blueprints/api.py:25` | `class HealthConfig` |
| `_health_status` | function | `lazyc2/blueprints/api.py:36` | `def _health_status(config)` |
| `_listener_alive` | function | `lazyc2/blueprints/api.py:99` | `def _listener_alive(listener)` |
| `get_defaults` | function | `lazyc2/blueprints/api.py:182` | `def get_defaults()` |
| `guarded` | function | `lazyc2/blueprints/api.py:146` | `def guarded()` |
| `health` | function | `lazyc2/blueprints/api.py:108` | `def health()` |
| `health_tenant` | function | `lazyc2/blueprints/api.py:157` | `def health_tenant()` |
| `ping` | function | `lazyc2/blueprints/api.py:120` | `def ping()` |
| `require_api_auth_with_store` | function | `lazyc2/blueprints/api.py:129` | `def require_api_auth_with_store(view)` |
| `set_default` | function | `lazyc2/blueprints/api.py:211` | `def set_default()` |
| `_db` | function | `lazyc2/blueprints/api_v1.py:43` | `def _db()` |
| `_error` | function | `lazyc2/blueprints/api_v1.py:60` | `def _error(message, status)` |
| `_read_webhooks` | function | `lazyc2/blueprints/api_v1.py:170` | `def _read_webhooks()` |
| `_sessions_dir` | function | `lazyc2/blueprints/api_v1.py:38` | `def _sessions_dir()` |
| `_webhooks_path` | function | `lazyc2/blueprints/api_v1.py:166` | `def _webhooks_path()` |
| `campaigns` | function | `lazyc2/blueprints/api_v1.py:141` | `def campaigns()` |
| `health` | function | `lazyc2/blueprints/api_v1.py:65` | `def health()` |
| `results` | function | `lazyc2/blueprints/api_v1.py:108` | `def results()` |
| `targets` | function | `lazyc2/blueprints/api_v1.py:76` | `def targets()` |
| `webhooks_delete` | function | `lazyc2/blueprints/api_v1.py:228` | `def webhooks_delete(index)` |
| `webhooks_list` | function | `lazyc2/blueprints/api_v1.py:180` | `def webhooks_list()` |
| `webhooks_register` | function | `lazyc2/blueprints/api_v1.py:191` | `def webhooks_register()` |
| `_get_rbac_store` | function | `lazyc2/blueprints/auth.py:60` | `def _get_rbac_store()` |
| `_get_rbac_user_obj` | function | `lazyc2/blueprints/auth.py:72` | `def _get_rbac_user_obj(flask_user)` |
| `_get_tenant_manager` | function | `lazyc2/blueprints/auth.py:82` | `def _get_tenant_manager()` |
| `_rbac_available` | function | `lazyc2/blueprints/auth.py:55` | `def _rbac_available()` |
| `admin_create_tenant` | function | `lazyc2/blueprints/auth.py:472` | `def admin_create_tenant()` |
| `admin_delete_user` | function | `lazyc2/blueprints/auth.py:434` | `def admin_delete_user(user_id)` |
| `admin_reset_mfa` | function | `lazyc2/blueprints/auth.py:422` | `def admin_reset_mfa(user_id)` |
| `admin_set_role` | function | `lazyc2/blueprints/auth.py:400` | `def admin_set_role(user_id)` |
| `admin_switch_tenant` | function | `lazyc2/blueprints/auth.py:491` | `def admin_switch_tenant(tenant_id)` |
| `admin_tenants` | function | `lazyc2/blueprints/auth.py:452` | `def admin_tenants()` |
| `admin_users` | function | `lazyc2/blueprints/auth.py:383` | `def admin_users()` |
| `login` | function | `lazyc2/blueprints/auth.py:155` | `def login()` |
| `logout` | function | `lazyc2/blueprints/auth.py:364` | `def logout()` |
| `mfa_qr` | function | `lazyc2/blueprints/auth.py:273` | `def mfa_qr(username)` |
| `mfa_setup` | function | `lazyc2/blueprints/auth.py:200` | `def mfa_setup()` |
| `mfa_verify` | function | `lazyc2/blueprints/auth.py:295` | `def mfa_verify()` |
| `profile` | function | `lazyc2/blueprints/auth.py:339` | `def profile()` |
| `register` | function | `lazyc2/blueprints/auth.py:96` | `def register()` |
| `require_role` | function | `lazyc2/blueprints/auth.py:35` | `def require_role(role)` |
| `_fire_hooks` | function | `lazyc2/blueprints/beacon.py:72` | `def _fire_hooks(event, context)` |
| `_run` | function | `lazyc2/blueprints/beacon.py:97` | `def _run()` |
| `_trigger_cred_reuse` | function | `lazyc2/blueprints/beacon.py:91` | `def _trigger_cred_reuse(context)` |
| `init_beacon_bp` | function | `lazyc2/blueprints/beacon.py:35` | `def init_beacon_bp(commands, results, commands_history, connected_clients, encrypt_fn, decrypt_fn, config...` |
| `issue_command` | function | `lazyc2/blueprints/beacon.py:245` | `def issue_command()` |
| `receive_result` | function | `lazyc2/blueprints/beacon.py:131` | `def receive_result(client_id)` |
| `send_command` | function | `lazyc2/blueprints/beacon.py:111` | `def send_command(client_id)` |
| `cve_detail` | function | `lazyc2/blueprints/operations.py:117` | `def cve_detail(cve_id)` |
| `cves` | function | `lazyc2/blueprints/operations.py:92` | `def cves()` |
| `edit_cve` | function | `lazyc2/blueprints/operations.py:132` | `def edit_cve(cve_id)` |
| `edit_notes` | function | `lazyc2/blueprints/operations.py:158` | `def edit_notes()` |
| `edit_task` | function | `lazyc2/blueprints/operations.py:66` | `def edit_task(task_id)` |
| `event_config` | function | `lazyc2/blueprints/operations.py:192` | `def event_config()` |
| `event_config_view` | function | `lazyc2/blueprints/operations.py:198` | `def event_config_view()` |
| `events` | function | `lazyc2/blueprints/operations.py:218` | `def events()` |
| `get_notes` | function | `lazyc2/blueprints/operations.py:173` | `def get_notes()` |
| `get_tasks` | function | `lazyc2/blueprints/operations.py:48` | `def get_tasks()` |
| `task_detail` | function | `lazyc2/blueprints/operations.py:33` | `def task_detail(task_id)` |
| `tasks` | function | `lazyc2/blueprints/operations.py:57` | `def tasks()` |
| `view_note` | function | `lazyc2/blueprints/operations.py:182` | `def view_note()` |
| `_get_config` | function | `lazyc2/blueprints/phishing.py:43` | `def _get_config(key, default)` |
| `create_short_url` | function | `lazyc2/blueprints/phishing.py:49` | `def create_short_url()` |
| `download_files` | function | `lazyc2/blueprints/phishing.py:192` | `def download_files(filename)` |
| `redirect_to_file` | function | `lazyc2/blueprints/phishing.py:151` | `def redirect_to_file(short_url)` |
| `track_interaction` | function | `lazyc2/blueprints/phishing.py:89` | `def track_interaction(short_url)` |
| `update_short_url` | function | `lazyc2/blueprints/phishing.py:125` | `def update_short_url(short_url)` |
| `webserver_report` | function | `lazyc2/blueprints/phishing.py:174` | `def webserver_report(filename)` |
| `_guard` | function | `lazyc2/blueprints/session_auth.py:36` | `def _guard()` |
| `require_operator_session` | function | `lazyc2/blueprints/session_auth.py:20` | `def require_operator_session(blueprint, login_endpoint)` |
| `decoy_response` | function | `lazyc2/extensions/decoy.py:12` | `def decoy_response()` |
| `_get_safe_file_path` | function | `lazyc2/extensions/short_urls.py:74` | `def _get_safe_file_path(user_path)` |
| `configure` | function | `lazyc2/extensions/short_urls.py:21` | `def configure(sessions_phishing_dir)` |
| `is_valid_url` | function | `lazyc2/extensions/short_urls.py:104` | `def is_valid_url(url)` |
| `load_short_urls` | function | `lazyc2/extensions/short_urls.py:33` | `def load_short_urls()` |
| `save_short_urls` | function | `lazyc2/extensions/short_urls.py:59` | `def save_short_urls(data)` |
| `configure` | function | `lazyc2/extensions/storage.py:18` | `def configure(sessions_dir)` |
| `load_banners` | function | `lazyc2/extensions/storage.py:154` | `def load_banners()` |
| `load_cves` | function | `lazyc2/extensions/storage.py:59` | `def load_cves()` |
| `load_event_config` | function | `lazyc2/extensions/storage.py:121` | `def load_event_config()` |
| `load_note` | function | `lazyc2/extensions/storage.py:87` | `def load_note()` |

Next: [SYMBOLS_p9.md](SYMBOLS_p9.md)
