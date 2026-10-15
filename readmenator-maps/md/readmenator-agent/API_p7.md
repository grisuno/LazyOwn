# API (page 7 of 22)
Previous: [API_p6.md](API_p6.md)

## fast_run_as_r00t.sh
- `log` (function) `fast_run_as_r00t.sh:59` -- ── Pretty-print helpers ──────────────────────────────────────────────────────
- `spin` (function) `fast_run_as_r00t.sh:60`
- `err_box` (function) `fast_run_as_r00t.sh:61`
- `ensure_gum` (function) `fast_run_as_r00t.sh:67` -- ── Ensure gum is installed ───────────────────────────────────────────────────
- `check_deps` (function) `fast_run_as_r00t.sh:78` -- ── Dependency check ──────────────────────────────────────────────────────────
- `check_sudo` (function) `fast_run_as_r00t.sh:87` -- ── Re-exec as root if needed ─────────────────────────────────────────────────
- `parse_args` (function) `fast_run_as_r00t.sh:96` -- ── CLI argument parsing ──────────────────────────────────────────────────────
- `t_send` (function) `fast_run_as_r00t.sh:114` -- Send one or more commands to the active tmux pane
- `t_lazyown` (function) `fast_run_as_r00t.sh:121` -- Open a new pane (split v or h), start LazyOwn shell with optional run flags, then send any follow-up commands once...
- `t_priv_user` (function) `fast_run_as_r00t.sh:134` -- Open a new pane running a command as unprivileged user 1000 (with venv).
- `start_chown_watcher` (function) `fast_run_as_r00t.sh:145` -- ── Background chown watcher ────────────────────────────────────────────────── Re-chowns the project tree to the...

## install.sh
- `usage` (function) `install.sh:49`
- `log` (function) `install.sh:88`
- `spin_run` (function) `install.sh:98`
- `ensure_gum` (function) `install.sh:128`
- `install_system_packages` (function) `install.sh:139`
- `install_external_tools` (function) `install.sh:150`
- `install_python_environment` (function) `install.sh:165`
- `install_ollama` (function) `install.sh:206`
- `install_external_storage` (function) `install.sh:218`
- `install_lazyownbt` (function) `install.sh:231`
- `download_file` (function) `install.sh:251`
- `install_encoder_module` (function) `install.sh:263`
- `generate_certificates` (function) `install.sh:274`
- `seed_payload_config` (function) `install.sh:281`
- `verify_installation` (function) `install.sh:294`
- `main` (function) `install.sh:310`

## key.py
Depends on: `core/console.py`, `core/prompt.py`
- `main` (function) `key.py:10` `def main()`

## lazy_sentinel4.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `sanitize_content` (function) `lazy_sentinel4.py:47` `def sanitize_content(text)` -- Sanitize text to ensure it's safe for rendering.
- `RAGManager.__init__` (method) `lazy_sentinel4.py:61` `def __init__(self, model_name, cache_size)`
- `RAGManager.initialize_cache_table` (method) `lazy_sentinel4.py:73` `def initialize_cache_table(self)`
- `RAGManager.get_cache_key` (method) `lazy_sentinel4.py:85` `def get_cache_key(self, content)`
- `RAGManager.load_existing_vectorstore` (method) `lazy_sentinel4.py:88` `def load_existing_vectorstore(self)`
- `RAGManager.ollama_llm` (method) `lazy_sentinel4.py:101` `def ollama_llm(self, question, context)`
- `RAGManager.process_file_to_rag` (method) `lazy_sentinel4.py:115` `def process_file_to_rag(self, file_path)`
- `RAGManager.query_rag` (method) `lazy_sentinel4.py:155` `def query_rag(self, question)`
- `RAGManager.invalidate_cache` (method) `lazy_sentinel4.py:177` `def invalidate_cache(self, file_path)`
- `RAGManager.get_knowledge_base_stats` (method) `lazy_sentinel4.py:191` `def get_knowledge_base_stats(self)`
- `Database.__init__` (method) `lazy_sentinel4.py:215` `def __init__(self, db_path)`
- `Database.initialize` (method) `lazy_sentinel4.py:219` `def initialize(self)`
- `Database.execute` (method) `lazy_sentinel4.py:243` `def execute(self, query, params)`
- `Database.insert` (method) `lazy_sentinel4.py:255` `def insert(self, query, params)`
- `Alert.__init__` (method) `lazy_sentinel4.py:274` `def __init__(self, alert_type, details, severity)`
- `Alert.to_dict` (method) `lazy_sentinel4.py:280` `def to_dict(self)`
- `Alert.save_to_db` (method) `lazy_sentinel4.py:288` `def save_to_db(self, db)`
- `LazySentinelHandler.__init__` (method) `lazy_sentinel4.py:303` `def __init__(self, lazysentinel)`
- `LazySentinelHandler.is_text_file` (method) `lazy_sentinel4.py:306` `def is_text_file(self, file_path)`
- `LazySentinelHandler.on_created` (method) `lazy_sentinel4.py:316` `def on_created(self, event)`
- `LazySentinelHandler.on_modified` (method) `lazy_sentinel4.py:328` `def on_modified(self, event)`
- `LazySentinel.__init__` (method) `lazy_sentinel4.py:341` `def __init__(self, app, popup_queue, watch_dir, excluded_files, min_file_size)`
- `LazySentinel.chunk_text` (method) `lazy_sentinel4.py:361` `def chunk_text(self, text, chunk_size)`
- `LazySentinel.select_relevant_chunk` (method) `lazy_sentinel4.py:364` `def select_relevant_chunk(self, file_content, chunks)`
- `LazySentinel.parse_deepseek_response` (method) `lazy_sentinel4.py:378` `def parse_deepseek_response(self, response_text)`
- `LazySentinel.show_popup` (method) `lazy_sentinel4.py:404` `def show_popup(self, file_name, relevant_info, commands, details)`
- `LazySentinel.process_file` (method) `lazy_sentinel4.py:422` `def process_file(self, file_path)`
- `LazySentinel.stop` (method) `lazy_sentinel4.py:538` `def stop(self)`
- `App.__init__` (method) `lazy_sentinel4.py:545` `def __init__(self)`
- `App.display_toastr` (method) `lazy_sentinel4.py:559` `def display_toastr(self, file_name, relevant_info, commands, details, severity, duration)` -- Display a toastr-like notification for file processing alerts.
- `App.postcmd` (method) `lazy_sentinel4.py:587` `def postcmd(self, stop, line)` -- Check the popup queue after each command and display toastr notifications.
- `App.do_quit` (method) `lazy_sentinel4.py:611` `def do_quit(self, arg)`
- `App.do_debug` (method) `lazy_sentinel4.py:615` `def do_debug(self, arg)`
- `App.do_rag_query` (method) `lazy_sentinel4.py:624` `def do_rag_query(self, arg)`
- `App.do_rag_add` (method) `lazy_sentinel4.py:632` `def do_rag_add(self, arg)`
- `App.do_rag_status` (method) `lazy_sentinel4.py:647` `def do_rag_status(self, arg)`
- `App.do_rag_toggle` (method) `lazy_sentinel4.py:654` `def do_rag_toggle(self, arg)`
- `App.do_rag_bulk_add` (method) `lazy_sentinel4.py:659` `def do_rag_bulk_add(self, arg)`
- `App.do_rag_search` (method) `lazy_sentinel4.py:678` `def do_rag_search(self, arg)`
- `App.complete_rag_add` (method) `lazy_sentinel4.py:699` `def complete_rag_add(self, text, line, begidx, endidx)`
- `App.complete_rag_bulk_add` (method) `lazy_sentinel4.py:706` `def complete_rag_bulk_add(self, text, line, begidx, endidx)`

## lazyc2.py
Depends on: `cli/auto_crypto.py`, `cli/palette.py`, `cli/palette_command.py`, `core/hardening.py`, `core/logging.py`, `core/parsers.py`, `core/reverse_shell_secret.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/extensions/users.py`, `lazyc2/security/command_allowlist.py`, `lazyc2/security/constants.py`, `lazyc2/security/cors.py`, `lazyc2/security/csrf.py`, `lazyc2/security/html_sanitizer.py`, `lazyc2/security/https_redirect.py`, `lazyc2/security/services.py`, `lazyc2/security/trusted_proxy.py`, `lazyc2/security/validators.py`, `lazyown.py`, `modules/attack_surface3d.py`, `modules/backdoor/server.c`, `modules/beacon_history.py`, `modules/collab_bp.py`, `modules/colors.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/dashboard_bp.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/event_engine.py`, `modules/intel_fusion.py`, `modules/kill_chain_viz.py`, `modules/killchain.py`, `modules/lazy_loop.py`, `modules/lazy_mentions.py`, `modules/lazy_rbac.py`, `modules/listener_manager.py`, `modules/live_surface.py`, `modules/llm_adapter.py`, `modules/logging_config.py`, `modules/metrics.py`, `modules/security_sanitizers.py`, `modules/state_manager.py`, `modules/world_model.py`, `skills/daemon_health.py`, `skills/lazyown_facts.py`, `utils.py`
- `is_insecure_credential` (function) `lazyc2.py:204` `def is_insecure_credential(user, pwd)` -- Check for weak or default credentials
- `_JsonLogFormatter.format` (method) `lazyc2.py:444` `def format(self, record)`
- `ensure_sessions_dir` (function) `lazyc2.py:471` `def ensure_sessions_dir()` -- Ensure the sessions directory exists with safe permissions.
- `load_routes` (function) `lazyc2.py:482` `def load_routes()` -- Load dynamic routes from JSON file.
- `save_routes` (function) `lazyc2.py:492` `def save_routes(routes)` -- Save dynamic routes to JSON file with safe permissions.
- `validate_route_path` (function) `lazyc2.py:506` `def validate_route_path(route_path)` -- Module-level boolean adapter for :func:`lazyc2.security.validators.validate_route_path`.
- `validate_template_name` (function) `lazyc2.py:519` `def validate_template_name(template_name)` -- Module-level boolean adapter for :func:`lazyc2.security.validators.validate_template_name`.
- `is_safe_template_path` (function) `lazyc2.py:529` `def is_safe_template_path(template_path, template_name)` -- Verify ``template_path`` resolves inside ``app.template_folder``.
- `is_binary` (function) `lazyc2.py:569` `def is_binary(safe_filename)` -- Check whether a session file is binary based on its header bytes.
- `clean_expired_tokens` (function) `lazyc2.py:610` `def clean_expired_tokens()`
- `clean_json` (function) `lazyc2.py:618` `def clean_json(text)` -- Extract only the JSON content between ```json and ```, discarding everything else.
- `load_yaml_safely` (function) `lazyc2.py:646` `def load_yaml_safely(file_path)` -- Load a YAML file safely with error handling and default values.
- `Handler.on_any_event` (method) `lazyc2.py:730` `def on_any_event(event)`
- `get_karma_name` (function) `lazyc2.py:755` `def get_karma_name(elo)`
- `fromjson` (function) `lazyc2.py:772` `def fromjson(value)`
- `run_shell` (function) `lazyc2.py:776` `def run_shell()`
- `load_banners` (function) `lazyc2.py:786` `def load_banners()` -- Loads the banners from the JSON file.
- `load_mitre_data` (function) `lazyc2.py:806` `def load_mitre_data()`
- `load_event_config` (function) `lazyc2.py:812` `def load_event_config()`
- `load_notifications` (function) `lazyc2.py:820` `def load_notifications()`
- `implants_check` (function) `lazyc2.py:838` `def implants_check()`
- `extract_attack_vectors` (function) `lazyc2.py:855` `def extract_attack_vectors(nodes, edges)` -- Analyzes BloodHound nodes and edges to extract critical attack vectors for AD compromise.
- `process_bloodhound_zip` (function) `lazyc2.py:942` `def process_bloodhound_zip(zip_filepath)` -- Processes a BloodHound ZIP file to extract nodes and edges for graph visualization.
- `start_watching` (function) `lazyc2.py:1040` `def start_watching()`
- `load_tasks` (function) `lazyc2.py:1056` `def load_tasks()`
- `create_cves` (function) `lazyc2.py:1064` `def create_cves()`
- `load_cves` (function) `lazyc2.py:1070` `def load_cves()`
- `save_cves` (function) `lazyc2.py:1078` `def save_cves(cves)`
- `create_report` (function) `lazyc2.py:1083` `def create_report()`
- `save_tasks` (function) `lazyc2.py:1089` `def save_tasks(tasks)`
- `load_note` (function) `lazyc2.py:1094` `def load_note()`
- `aumentar_elo` (function) `lazyc2.py:1112` `def aumentar_elo(user_id, cantidad)`
- `save_note` (function) `lazyc2.py:1142` `def save_note(content)`
- `escape_js` (function) `lazyc2.py:1148` `def escape_js(s)`
- `markdown_to_html` (function) `lazyc2.py:1185` `def markdown_to_html(text)`
- `to_serializable` (function) `lazyc2.py:1193` `def to_serializable(obj)` -- Convert objects to serializable format.
- `make_serializable` (function) `lazyc2.py:1200` `def make_serializable(data)` -- Recursively convert data to serializable format.
- `datetime_now_iso` (function) `lazyc2.py:1218` `def datetime_now_iso()` -- Return the current UTC timestamp as an ISO-8601 string.
- `escape_js_string` (function) `lazyc2.py:1336` `def escape_js_string(value)` -- Escape special characters in a string for JavaScript.
- `check_auth` (function) `lazyc2.py:1348` `def check_auth(username, password)` -- Verify credentials.
- `authenticate` (function) `lazyc2.py:1363` `def authenticate()` -- Requests authentication.
- `requires_auth_or_session` (function) `lazyc2.py:1372` `def requires_auth_or_session(f)` -- Require Basic auth credentials or a valid Flask-Login session.
- `decorated` (function) `lazyc2.py:1382` `def decorated()`
- `requires_auth` (function) `lazyc2.py:1393` `def requires_auth(f)`
- `decorated` (function) `lazyc2.py:1395` `def decorated()`
- `csrf_protect` (function) `lazyc2.py:1404` `def csrf_protect(view)` -- Decorator that enforces the per-session CSRF token.
- `wrapper` (function) `lazyc2.py:1414` `def wrapper()`
- `aicmd_deepseek` (function) `lazyc2.py:1425` `def aicmd_deepseek(cmd)`
- `aicmd` (function) `lazyc2.py:1539` `def aicmd(cmd)`
- `search_database` (function) `lazyc2.py:1644` `def search_database(term, data_path)` -- Busca un término en un DataFrame, manejando listas, dicts y distintas estructuras.
- `execute_command` (function) `lazyc2.py:1699` `def execute_command(command)`
- `CustomDNSResolver.resolve` (method) `lazyc2.py:1729` `def resolve(self, request, handler)`
- `start_dns_server` (function) `lazyc2.py:1833` `def start_dns_server()` -- Start the C2 DNS server, gracefully degrading when binding is unsafe.
- `tcp_bridge` (function) `lazyc2.py:1873` `def tcp_bridge(local_port, remote_host, remote_port)` -- Establish a TCP bridge between a local port and a remote host.
- `handle_client` (function) `lazyc2.py:1897` `def handle_client(client_socket, remote_host, remote_port)` -- Handle communication between the client and the remote server.
- `decoy` (function) `lazyc2.py:1916` `def decoy()` -- Serve a decoy page to non-operator IPs when decoy mode is enabled.
- `encrypt_data` (function) `lazyc2.py:1954` `def encrypt_data(data)`
- `decrypt_data` (function) `lazyc2.py:1963` `def decrypt_data(encrypted_data, is_file)`
- `set_winsize` (function) `lazyc2.py:1976` `def set_winsize(fd, row, col, xpix, ypix)` -- Configura el tamaño de la terminal
- `read_and_forward_pty_output` (function) `lazyc2.py:1982` `def read_and_forward_pty_output()` -- Lectura continua del PTY y envío por WebSocket
- `get_discovered_hosts` (function) `lazyc2.py:1999` `def get_discovered_hosts()` -- Reads the sessions/hostsdiscovery.txt file and returns a list of discovered hosts.
- `get_local_ip_addresses` (function) `lazyc2.py:2049` `def get_local_ip_addresses()`
- `sanitize_json` (function) `lazyc2.py:2074` `def sanitize_json(data)` -- Elimina datos sensibles del diccionario JSON.
- `add_dynamic_data` (function) `lazyc2.py:2104` `def add_dynamic_data(data)` -- Agrega datos dinámicos al diccionario JSON si es necesario, basándose en el contenido del diccionario 'data'.
- `get_client_ip` (function) `lazyc2.py:2126` `def get_client_ip()` -- Get the client's IP address, handling proxies.
- `get_request_details` (function) `lazyc2.py:2135` `def get_request_details()` -- Collect comprehensive request details.
- `save_to_log` (function) `lazyc2.py:2170` `def save_to_log(data)` -- Append request data to the JSON log file with safe permissions.
- `parse_access_log_for_short_url` (function) `lazyc2.py:2192` `def parse_access_log_for_short_url(short_url)` -- Parse access.log for entries matching the given short URL.
- `parse_execution_log` (function) `lazyc2.py:2214` `def parse_execution_log(implante)` -- Parse execution log for the given implante, returning execution events.
- `load_implant_config` (function) `lazyc2.py:2240` `def load_implant_config(implante)` -- Load implant configuration from JSON file.
- `load_short_urls` (function) `lazyc2.py:2250` `def load_short_urls()` -- Load short URLs from JSON file, creating it if it doesn't exist.
- `save_short_urls` (function) `lazyc2.py:2270` `def save_short_urls(data)` -- Save short URLs to JSON file.
- `is_valid_url` (function) `lazyc2.py:2280` `def is_valid_url(url)` -- Validate if the input is a valid URL or existing local file path.
- `get_safe_file_path` (function) `lazyc2.py:2288` `def get_safe_file_path(user_path)` -- Construye de forma segura el path del archivo y verifica que está en el directorio permitido.
- `analyze_behavioral_data` (function) `lazyc2.py:2358` `def analyze_behavioral_data(behavioral_events)` -- Analyze behavioral events using Groq AI to generate risk scores.
- `analyze_campaign_progress` (function) `lazyc2.py:2386` `def analyze_campaign_progress(campaign_id, events)` -- Analyze campaign progress and suggest adaptations using Grok AI.
- `User.__init__` (method) `lazyc2.py:2965` `def __init__(self, user_data)`
- `load_users` (function) `lazyc2.py:2987` `def load_users()`
- `save_users` (function) `lazyc2.py:2997` `def save_users(users)`
- `load_data` (function) `lazyc2.py:3008` `def load_data()`
- `load_user` (function) `lazyc2.py:3025` `def load_user(user_id)`
- `tojson_filter` (function) `lazyc2.py:3040` `def tojson_filter(value)` -- Custom tojson filter to handle non-serializable objects.
- `index` (function) `lazyc2.py:3047` `def index()`
- `send_command` (function) `lazyc2.py:3197` `def send_command(client_id)`
- `receive_result` (function) `lazyc2.py:3341` `def receive_result(client_id)`
- `issue_command` (function) `lazyc2.py:3882` `def issue_command()`
- `upload` (function) `lazyc2.py:3896` `def upload()`
- `download_file` (function) `lazyc2.py:3933` `def download_file()`
- `serve_file` (function) `lazyc2.py:3960` `def serve_file(file_path)` -- Serve a file from ``sessions/temp_uploads`` through :class:`SafeFileService`.
- `create_route` (function) `lazyc2.py:4062` `def create_route()` -- Register a new operator-supplied dynamic route bound to a template.
- `dynamic_route` (function) `lazyc2.py:4131` `def dynamic_route(route_path, data)` -- Handle dynamic routes based on stored route-to-template mappings.
- `sanitize_input` (function) `lazyc2.py:4138` `def sanitize_input(input_str)` -- Sanitize input to prevent XSS attacks.
- `is_valid_route_path` (function) `lazyc2.py:4148` `def is_valid_route_path(route_path)` -- Validate route path format.
- `is_valid_data` (function) `lazyc2.py:4155` `def is_valid_data(data)` -- Validate data parameter.
- `is_valid_template_name` (function) `lazyc2.py:4165` `def is_valid_template_name(template_name)` -- Validate template name.
- `log` (function) `lazyc2.py:4227` `def log(data)` -- Log request details to JSON file.
- `favicon` (function) `lazyc2.py:4245` `def favicon()` -- Serve the favicon.ico file.
- `palette_view` (function) `lazyc2.py:4258` `def palette_view()` -- Render the operator command palette browser.
- `palette_api` (function) `lazyc2.py:4286` `def palette_api()` -- JSON catalogue feed for the global Cmd+K / Ctrl+K overlay.
- `api_data` (function) `lazyc2.py:4307` `def api_data()`
- `create_short_url` (function) `lazyc2.py:4469` `def create_short_url()` -- Create multiple short URLs for a single original URL.
- `track_interaction` (function) `lazyc2.py:4497` `def track_interaction(short_url)` -- Serve tracking page and log behavioral data.
- `update_short_url` (function) `lazyc2.py:4522` `def update_short_url(short_url)`
- `redirect_to_file` (function) `lazyc2.py:4549` `def redirect_to_file(short_url)`
- `webserver_report` (function) `lazyc2.py:4577` `def webserver_report(filename)` -- Serve nmap HTML report assets from the sessions directory over HTTPS.
- `download_files` (function) `lazyc2.py:4597` `def download_files(filename)` -- Serve implant stage files by name, enforcing strict containment.
- `view_yaml` (function) `lazyc2.py:4649` `def view_yaml()`
- `run_command` (function) `lazyc2.py:4743` `def run_command()` -- Execute one shell command and return a sanitised, JSON-safe result.
- `get_output` (function) `lazyc2.py:4812` `def get_output()`
- `run_shellcode` (function) `lazyc2.py:4839` `def run_shellcode()`
- `get_results` (function) `lazyc2.py:4848` `def get_results()`
- `send_lcommand` (function) `lazyc2.py:4946` `def send_lcommand(ip, port)`
- `chatbot` (function) `lazyc2.py:4979` `def chatbot()`
- `vuln` (function) `lazyc2.py:4995` `def vuln()`
- `taskbot` (function) `lazyc2.py:5034` `def taskbot()`
- `search` (function) `lazyc2.py:5050` `def search()`
- `script` (function) `lazyc2.py:5066` `def script()`
- `redop` (function) `lazyc2.py:5082` `def redop()`
- `adversary` (function) `lazyc2.py:5101` `def adversary()`
- `generalbot` (function) `lazyc2.py:5117` `def generalbot()`
- `csv_to_html` (function) `lazyc2.py:5133` `def csv_to_html()`
- `search_results` (function) `lazyc2.py:5184` `def search_results()`
- `graph` (function) `lazyc2.py:5232` `def graph()`
- `task` (function) `lazyc2.py:5241` `def task(task_id)`
- `get_tasks` (function) `lazyc2.py:5256` `def get_tasks()`
- `tasks` (function) `lazyc2.py:5266` `def tasks()`
- `edit_task` (function) `lazyc2.py:5276` `def edit_task(task_id)`
- `cves` (function) `lazyc2.py:5310` `def cves()`
- `cve` (function) `lazyc2.py:5336` `def cve(cve_id)`
- `edit_cve` (function) `lazyc2.py:5351` `def edit_cve(cve_id)`
- `edit_notes` (function) `lazyc2.py:5385` `def edit_notes()`
- `get_notes` (function) `lazyc2.py:5403` `def get_notes()`
- `view_note` (function) `lazyc2.py:5413` `def view_note()`
- `push_notification` (function) `lazyc2.py:5423` `def push_notification()`
- `edit_event` (function) `lazyc2.py:5450` `def edit_event(event_name)`
- `get_event_config` (function) `lazyc2.py:5485` `def get_event_config()`
- `get_event_config_view` (function) `lazyc2.py:5492` `def get_event_config_view()`
- `aicmd_view` (function) `lazyc2.py:5527` `def aicmd_view()`
- `get_events` (function) `lazyc2.py:5552` `def get_events()`
- `list_tools` (function) `lazyc2.py:5584` `def list_tools()`
- `create_tool` (function) `lazyc2.py:5594` `def create_tool()`
- `view_tool` (function) `lazyc2.py:5621` `def view_tool(toolname)`
- `update_tool` (function) `lazyc2.py:5652` `def update_tool(toolname)`
- `delete_tool` (function) `lazyc2.py:5700` `def delete_tool(toolname)`
- `register` (function) `lazyc2.py:5735` `def register()`
- `login` (function) `lazyc2.py:5794` `def login()`
- `mfa_setup` (function) `lazyc2.py:5841` `def mfa_setup()`
- `mfa_qr` (function) `lazyc2.py:5915` `def mfa_qr(username)` -- Serve a locally-generated QR code SVG for MFA setup.
- `mfa_verify` (function) `lazyc2.py:5937` `def mfa_verify()`
- `admin_users` (function) `lazyc2.py:5985` `def admin_users()`
- `admin_set_role` (function) `lazyc2.py:6000` `def admin_set_role(user_id)`
- `admin_reset_mfa` (function) `lazyc2.py:6022` `def admin_reset_mfa(user_id)`
- `admin_delete_user` (function) `lazyc2.py:6034` `def admin_delete_user(user_id)`
- `admin_tenants` (function) `lazyc2.py:6052` `def admin_tenants()`
- `admin_create_tenant` (function) `lazyc2.py:6073` `def admin_create_tenant()`
- `admin_switch_tenant` (function) `lazyc2.py:6093` `def admin_switch_tenant(tenant_id)`
- `profile` (function) `lazyc2.py:6108` `def profile()`
- `logout` (function) `lazyc2.py:6132` `def logout()`
- `change_password` (function) `lazyc2.py:6147` `def change_password()` -- Force rotation of the initial one-time admin password.
- `aumentar_elo_route` (function) `lazyc2.py:6213` `def aumentar_elo_route(user_id)`
- `banners` (function) `lazyc2.py:6229` `def banners()`
- `mitre` (function) `lazyc2.py:6265` `def mitre()`
- `get_connected_clients` (function) `lazyc2.py:6310` `def get_connected_clients()`
- `lazybot` (function) `lazyc2.py:6321` `def lazybot()`
- `compliance_dashboard` (function) `lazyc2.py:6338` `def compliance_dashboard()`
- `compliance_report` (function) `lazyc2.py:6360` `def compliance_report()`
- `compliance_add_evidence` (function) `lazyc2.py:6390` `def compliance_add_evidence()`
- `compliance_verify_evidence` (function) `lazyc2.py:6426` `def compliance_verify_evidence()`
- `compliance_export` (function) `lazyc2.py:6440` `def compliance_export(format)`
- `lazyreport` (function) `lazyc2.py:6470` `def lazyreport()`
- `teamserver` (function) `lazyc2.py:6489` `def teamserver()`
- `report` (function) `lazyc2.py:6518` `def report()`
- `lazyreport_view` (function) `lazyc2.py:6525` `def lazyreport_view()`
- `killchain_view` (function) `lazyc2.py:6531` `def killchain_view()`
- `api_killchain` (function) `lazyc2.py:6561` `def api_killchain()` -- Return the unified kill-chain snapshot consumed by every surface.
- `api_beacon_results` (function) `lazyc2.py:6592` `def api_beacon_results(client_id)` -- Return the full ordered command/result history for one beacon.
- `connect` (function) `lazyc2.py:6692` `def connect()`
- `listener` (function) `lazyc2.py:6701` `def listener()`
- `listener_connect` (function) `lazyc2.py:6710` `def listener_connect()`
- `listener_disconnect` (function) `lazyc2.py:6721` `def listener_disconnect()`
- `pty_input` (function) `lazyc2.py:6731` `def pty_input(data)`
- `resize` (function) `lazyc2.py:6745` `def resize(data)`
- `pty_connect` (function) `lazyc2.py:6758` `def pty_connect()`
- `handle_input` (function) `lazyc2.py:6789` `def handle_input(data)`
- `listener_command` (function) `lazyc2.py:6813` `def listener_command(msg)`
- `terminal` (function) `lazyc2.py:6827` `def terminal()`
- `terminal_connect` (function) `lazyc2.py:6836` `def terminal_connect()`
- `terminal_disconnect` (function) `lazyc2.py:6846` `def terminal_disconnect()`
- `terminal_input` (function) `lazyc2.py:6856` `def terminal_input(data)`
- `terminal_command` (function) `lazyc2.py:6869` `def terminal_command(data)`
- `terminal_resize` (function) `lazyc2.py:6884` `def terminal_resize(data)`
- `start_reverse_shell` (function) `lazyc2.py:6893` `def start_reverse_shell()`
- `start_bridge` (function) `lazyc2.py:6940` `def start_bridge()` -- Start a TCP bridge to a specified remote host and port.
- `page_not_found` (function) `lazyc2.py:6957` `def page_not_found(e)`
- `internal_server_error` (function) `lazyc2.py:6965` `def internal_server_error(e)`
- `get_config` (function) `lazyc2.py:6974` `def get_config()` -- Lee el archivo payload.json, lo manipula y lo expone como /config.json.
- `capture_image` (function) `lazyc2.py:6993` `def capture_image()`
- `capture_audio` (function) `lazyc2.py:7019` `def capture_audio()`
- `surface` (function) `lazyc2.py:7037` `def surface()`
- `surface_live` (function) `lazyc2.py:7043` `def surface_live()` -- Render the live attack-surface graph page.
- `api_surface_live` (function) `lazyc2.py:7058` `def api_surface_live()` -- Return the live attack-surface graph derived from the world model.
- `intel_view` (function) `lazyc2.py:7083` `def intel_view()` -- Render the fused sessions intel graph page (ReadMenator engine).
- `intel_bundle_view` (function) `lazyc2.py:7102` `def intel_bundle_view()` -- Render the circular/spherical bundle view of the intel graph.
- `attack3d_view` (function) `lazyc2.py:7117` `def attack3d_view()` -- Render the C2-centred attack-surface graph (ReadMenator engine).
- `attack_bundle_view` (function) `lazyc2.py:7136` `def attack_bundle_view()` -- Render the circular/spherical bundle view of the attack surface.
- `api_intel_graph` (function) `lazyc2.py:7151` `def api_intel_graph()` -- Return the fused C2-centred intel graph with precomputed layout.
- `broadcast_view` (function) `lazyc2.py:7207` `def broadcast_view()` -- Render the exploration timeline board for one loop task.
- `api_loop_broadcast_stream` (function) `lazyc2.py:7221` `def api_loop_broadcast_stream()` -- SSE live tail of one loop task's activity stream.
- `api_loop_broadcast` (function) `lazyc2.py:7279` `def api_loop_broadcast()` -- Return the paginated exploration timeline for one loop task.
- `api_guard_audit` (function) `lazyc2.py:7322` `def api_guard_audit()` -- Return guard history with pending approvals kept independent.
- `api_loop_graph` (function) `lazyc2.py:7368` `def api_loop_graph()` -- Return one loop task as ForceGraph-ready nodes/links plus context.
- `api_lazy_mentions` (function) `lazyc2.py:7399` `def api_lazy_mentions()` -- Search @ mention candidates with scroll pagination.
- `api_intel_bundle` (function) `lazyc2.py:7435` `def api_intel_bundle()` -- Return the circular/spherical bundle payload of the intel graph.
- `api_attack_graph` (function) `lazyc2.py:7468` `def api_attack_graph()` -- Return the fused C2-centred attack-surface graph.
- `api_attack_bundle` (function) `lazyc2.py:7520` `def api_attack_bundle()` -- Return the circular/spherical bundle payload of the attack surface.
- `get_data` (function) `lazyc2.py:7550` `def get_data()`
- `upload_zip_file` (function) `lazyc2.py:7559` `def upload_zip_file()` -- Handles the file upload, processes the BloodHound ZIP, and prepares data for visualization.
- `list_campaigns` (function) `lazyc2.py:7617` `def list_campaigns()`
- `create_campaign` (function) `lazyc2.py:7630` `def create_campaign()`
- `lazyphishingai` (function) `lazyc2.py:7708` `def lazyphishingai()`
- `track_pixel` (function) `lazyc2.py:7724` `def track_pixel(campaign_id, email)` -- Píxel de seguimiento para registrar aperturas.
- `campaign_report` (function) `lazyc2.py:7746` `def campaign_report(campaign_id)`
- `orchestrate_campaign` (function) `lazyc2.py:7828` `def orchestrate_campaign(campaign_id)`
- `create_multivector_campaign` (function) `lazyc2.py:7875` `def create_multivector_campaign()`
- `serve_landing_page` (function) `lazyc2.py:8027` `def serve_landing_page(campaign_id, short_url)`
- `health_check` (function) `lazyc2.py:8052` `def health_check()` -- Basic health and readiness endpoint.
- `metrics_exposition` (function) `lazyc2.py:8091` `def metrics_exposition()` -- Prometheus-compatible metrics endpoint.
- `api_dashboard` (function) `lazyc2.py:8098` `def api_dashboard()` -- Aggregated JSON dashboard: beacons, campaign, events, facts summary.
- `api_listeners` (function) `lazyc2.py:8168` `def api_listeners()` -- List all configured C2 listeners and their runtime status.
- `api_listeners_create` (function) `lazyc2.py:8175` `def api_listeners_create()` -- Create a new listener.
- `api_listeners_start` (function) `lazyc2.py:8191` `def api_listeners_start(listener_id)` -- Start an existing listener.
- `api_listeners_stop` (function) `lazyc2.py:8199` `def api_listeners_stop(listener_id)` -- Stop a running listener.
- `api_listeners_delete` (function) `lazyc2.py:8207` `def api_listeners_delete(listener_id)` -- Remove a listener configuration.

## lazyc2/addon_creator.py
Imported by: `lazyc2/blueprints/addons.py`, `tests/test_addon_creator.py`, `tests/test_placeholder_coverage.py`
- `ParamSpec.to_dict` (method) `lazyc2/addon_creator.py:358` `def to_dict(self)` -- Return the param as a schema-ordered mapping.
- `AddonValidationError.__init__` (method) `lazyc2/addon_creator.py:414` `def __init__(self, issues)`
- `AddonValidator.__init__` (method) `lazyc2/addon_creator.py:427` `def __init__(self, draft, config)` -- Store the draft and configuration used by every check.
- `AddonValidator.validate` (method) `lazyc2/addon_creator.py:441` `def validate(self)` -- Run every rule and return the collected issues.
- `AddonValidator.is_valid` (method) `lazyc2/addon_creator.py:455` `def is_valid(self)` -- Return True when the draft passes every rule.
- `AddonYamlRenderer.__init__` (method) `lazyc2/addon_creator.py:726` `def __init__(self, config)` -- Store the configuration used for defaults.
- `AddonYamlRenderer.render` (method) `lazyc2/addon_creator.py:734` `def render(self, draft)` -- Return the YAML document for the draft.
- `AddonYamlRenderer.to_document` (method) `lazyc2/addon_creator.py:752` `def to_document(self, draft)` -- Build the schema-ordered document mapping for the draft.
- `AddonStore.__init__` (method) `lazyc2/addon_creator.py:817` `def __init__(self, config, base_dir)` -- Configure the store.
- `AddonStore.resolve_path` (method) `lazyc2/addon_creator.py:832` `def resolve_path(self, name)` -- Return the safe absolute path for a newly created addon name.
- `AddonStore.resolve_existing_path` (method) `lazyc2/addon_creator.py:847` `def resolve_existing_path(self, name)` -- Return the safe absolute path for an existing addon file.
- `AddonStore.exists` (method) `lazyc2/addon_creator.py:891` `def exists(self, name)` -- Return True when an addon file already exists for the name.
- `AddonStore.save` (method) `lazyc2/addon_creator.py:902` `def save(self, name, yaml_text)` -- Persist the YAML document atomically.
- `AddonStore.load` (method) `lazyc2/addon_creator.py:956` `def load(self, name)` -- Return the parsed addon document for a name.
- `AddonStore.delete` (method) `lazyc2/addon_creator.py:979` `def delete(self, name)` -- Delete the addon file for a name.
- `AddonStore.list_all` (method) `lazyc2/addon_creator.py:995` `def list_all(self)` -- Return summary dicts for every parseable addon.
- `parse_addon_form` (function) `lazyc2/addon_creator.py:1075` `def parse_addon_form(form)` -- Adapt raw form data into an AddonDraft.

## lazyc2/app_factory.py
Depends on: `core/api_authz.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/extensions/__init__.py`, `lazyc2/security/services.py`
- `create_app` (function) `lazyc2/app_factory.py:89` `def create_app()` -- Create and return a fully configured C2 Flask application.

## lazyc2/blueprints/addons.py
Depends on: `core/logging.py`, `lazyc2/addon_creator.py`, `lazyc2/blueprints/session_auth.py`, `lazyc2/extensions/decoy.py`, `lazyc2/security/csrf.py`
Imported by: `lazyc2/blueprints/__init__.py`, `tests/test_addon_creator.py`, `tests/test_security_hardening_v5.py`
- `init_addons_bp` (function) `lazyc2/blueprints/addons.py:69` `def init_addons_bp(base_dir)` -- Configure the blueprint state before registration.
- `csrf_protect` (function) `lazyc2/blueprints/addons.py:96` `def csrf_protect(view)` -- Decorate a view so mutating requests must echo the CSRF token.
- `wrapper` (function) `lazyc2/blueprints/addons.py:110` `def wrapper()`
- `list_addons` (function) `lazyc2/blueprints/addons.py:263` `def list_addons()` -- Render the addon dashboard list page with a fresh CSRF token.
- `create_addon` (function) `lazyc2/blueprints/addons.py:277` `def create_addon()` -- Render the creation form and persist valid addon submissions.
- `view_addon` (function) `lazyc2/blueprints/addons.py:321` `def view_addon(name)` -- Render the persisted YAML document for an addon.
- `delete_addon` (function) `lazyc2/blueprints/addons.py:345` `def delete_addon(name)` -- Delete an addon file.

## lazyc2/blueprints/api.py
Depends on: `core/api_authz.py`, `core/config.py`, `core/defaults.py`, `core/logging.py`
Imported by: `lazyc2/blueprints/__init__.py`, `lazyc2/blueprints/api_v1.py`, `tests/test_core_defaults.py`, `tests/test_security_hardening_v5.py`
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
Depends on: `core/logging.py`, `lazyc2/__init__.py`, `lazyc2/extensions/decoy.py`, `lazyc2/extensions/users.py`, `modules/lazy_rbac.py`
Imported by: `lazyc2/blueprints/__init__.py`, `lazygui/services/teamserver_backend.py`, `static/js/socket.io-4.0.0.min.js`, `static/js/socket.io-4.3.2.min.js`
- `require_role` (function) `lazyc2/blueprints/auth.py:35` `def require_role(role)` -- Return a pass-through decorator when RBAC is unavailable.
- `register` (function) `lazyc2/blueprints/auth.py:96` `def register()`
- `login` (function) `lazyc2/blueprints/auth.py:155` `def login()`
- `mfa_setup` (function) `lazyc2/blueprints/auth.py:200` `def mfa_setup()`
- `mfa_qr` (function) `lazyc2/blueprints/auth.py:273` `def mfa_qr(username)`
- `mfa_verify` (function) `lazyc2/blueprints/auth.py:295` `def mfa_verify()`
- `profile` (function) `lazyc2/blueprints/auth.py:339` `def profile()`
- `logout` (function) `lazyc2/blueprints/auth.py:364` `def logout()`
- `admin_users` (function) `lazyc2/blueprints/auth.py:383` `def admin_users()`
- `admin_set_role` (function) `lazyc2/blueprints/auth.py:400` `def admin_set_role(user_id)`
- `admin_reset_mfa` (function) `lazyc2/blueprints/auth.py:422` `def admin_reset_mfa(user_id)`
- `admin_delete_user` (function) `lazyc2/blueprints/auth.py:434` `def admin_delete_user(user_id)`
- `admin_tenants` (function) `lazyc2/blueprints/auth.py:452` `def admin_tenants()`
- `admin_create_tenant` (function) `lazyc2/blueprints/auth.py:472` `def admin_create_tenant()`
- `admin_switch_tenant` (function) `lazyc2/blueprints/auth.py:491` `def admin_switch_tenant(tenant_id)`

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


Next: [API_p8.md](API_p8.md)
