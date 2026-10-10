# API (page 7 of 20)
Previous: [API_p6.md](API_p6.md)

## lazyc2.py
Depends on: `cli/auto_crypto.py`, `cli/palette.py`, `cli/palette_command.py`, `core/hardening.py`, `core/logging.py`, `core/parsers.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/extensions/users.py`, `lazyc2/security/command_allowlist.py`, `lazyc2/security/constants.py`, `lazyc2/security/cors.py`, `lazyc2/security/csrf.py`, `lazyc2/security/html_sanitizer.py`, `lazyc2/security/https_redirect.py`, `lazyc2/security/services.py`, `lazyc2/security/trusted_proxy.py`, `lazyc2/security/validators.py`, `lazyown.py`, `modules/backdoor/server.c`, `modules/beacon_history.py`, `modules/collab_bp.py`, `modules/colors.py`, `modules/compliance.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/dashboard_bp.py`, `modules/event_bus.py`, `modules/event_consumers.py`, `modules/event_engine.py`, `modules/kill_chain_viz.py`, `modules/killchain.py`, `modules/lazy_rbac.py`, `modules/listener_manager.py`, `modules/live_surface.py`, `modules/llm_adapter.py`, `modules/logging_config.py`, `modules/metrics.py`, `modules/security_sanitizers.py`, `modules/state_manager.py`, `modules/world_model.py`, `skills/daemon_health.py`, `skills/lazyown_facts.py`, `utils.py`
- `is_insecure_credential` (function) `lazyc2.py:187` `def is_insecure_credential(user, pwd)` -- Check for weak or default credentials
- `_JsonLogFormatter.format` (method) `lazyc2.py:427` `def format(self, record)`
- `_JsonLogFormatter.ensure_sessions_dir` (method) `lazyc2.py:454` `def ensure_sessions_dir()` -- Ensure the sessions directory exists with safe permissions.
- `_JsonLogFormatter.load_routes` (method) `lazyc2.py:465` `def load_routes()` -- Load dynamic routes from JSON file.
- `_JsonLogFormatter.save_routes` (method) `lazyc2.py:475` `def save_routes(routes)` -- Save dynamic routes to JSON file with safe permissions.
- `_JsonLogFormatter.validate_route_path` (method) `lazyc2.py:489` `def validate_route_path(route_path)` -- Module-level boolean adapter for :func:`lazyc2.security.validators.validate_route_path`.
- `_JsonLogFormatter.validate_template_name` (method) `lazyc2.py:502` `def validate_template_name(template_name)` -- Module-level boolean adapter for :func:`lazyc2.security.validators.validate_template_name`.
- `_JsonLogFormatter.is_safe_template_path` (method) `lazyc2.py:512` `def is_safe_template_path(template_path, template_name)` -- Verify ``template_path`` resolves inside ``app.template_folder``.
- `_JsonLogFormatter.is_binary` (method) `lazyc2.py:552` `def is_binary(safe_filename)` -- Check whether a session file is binary based on its header bytes.
- `_JsonLogFormatter.clean_expired_tokens` (method) `lazyc2.py:593` `def clean_expired_tokens()`
- `_JsonLogFormatter.clean_json` (method) `lazyc2.py:601` `def clean_json(text)` -- Extract only the JSON content between ```json and ```, discarding everything else.
- `_JsonLogFormatter.load_yaml_safely` (method) `lazyc2.py:629` `def load_yaml_safely(file_path)` -- Load a YAML file safely with error handling and default values.
- `Handler.on_any_event` (method) `lazyc2.py:713` `def on_any_event(event)`
- `Handler.get_karma_name` (method) `lazyc2.py:738` `def get_karma_name(elo)`
- `Handler.fromjson` (method) `lazyc2.py:755` `def fromjson(value)`
- `Handler.run_shell` (method) `lazyc2.py:759` `def run_shell()`
- `Handler.load_banners` (method) `lazyc2.py:769` `def load_banners()` -- Loads the banners from the JSON file.
- `Handler.load_mitre_data` (method) `lazyc2.py:789` `def load_mitre_data()`
- `Handler.load_event_config` (method) `lazyc2.py:795` `def load_event_config()`
- `Handler.load_notifications` (method) `lazyc2.py:803` `def load_notifications()`
- `Handler.implants_check` (method) `lazyc2.py:821` `def implants_check()`
- `Handler.extract_attack_vectors` (method) `lazyc2.py:838` `def extract_attack_vectors(nodes, edges)` -- Analyzes BloodHound nodes and edges to extract critical attack vectors for AD compromise.
- `Handler.process_bloodhound_zip` (method) `lazyc2.py:925` `def process_bloodhound_zip(zip_filepath)` -- Processes a BloodHound ZIP file to extract nodes and edges for graph visualization.
- `Handler.start_watching` (method) `lazyc2.py:1023` `def start_watching()`
- `Handler.load_tasks` (method) `lazyc2.py:1039` `def load_tasks()`
- `Handler.create_cves` (method) `lazyc2.py:1047` `def create_cves()`
- `Handler.load_cves` (method) `lazyc2.py:1053` `def load_cves()`
- `Handler.save_cves` (method) `lazyc2.py:1061` `def save_cves(cves)`
- `Handler.create_report` (method) `lazyc2.py:1066` `def create_report()`
- `Handler.save_tasks` (method) `lazyc2.py:1072` `def save_tasks(tasks)`
- `Handler.load_note` (method) `lazyc2.py:1077` `def load_note()`
- `Handler.aumentar_elo` (method) `lazyc2.py:1095` `def aumentar_elo(user_id, cantidad)`
- `Handler.save_note` (method) `lazyc2.py:1125` `def save_note(content)`
- `Handler.escape_js` (method) `lazyc2.py:1131` `def escape_js(s)`
- `Handler.markdown_to_html` (method) `lazyc2.py:1168` `def markdown_to_html(text)`
- `Handler.to_serializable` (method) `lazyc2.py:1176` `def to_serializable(obj)` -- Convert objects to serializable format.
- `Handler.make_serializable` (method) `lazyc2.py:1183` `def make_serializable(data)` -- Recursively convert data to serializable format.
- `Handler.datetime_now_iso` (method) `lazyc2.py:1201` `def datetime_now_iso()` -- Return the current UTC timestamp as an ISO-8601 string.
- `Handler.escape_js_string` (method) `lazyc2.py:1319` `def escape_js_string(value)` -- Escape special characters in a string for JavaScript.
- `Handler.check_auth` (method) `lazyc2.py:1331` `def check_auth(username, password)` -- Verify credentials.
- `Handler.authenticate` (method) `lazyc2.py:1346` `def authenticate()` -- Requests authentication.
- `Handler.requires_auth_or_session` (method) `lazyc2.py:1355` `def requires_auth_or_session(f)` -- Require Basic auth credentials or a valid Flask-Login session.
- `Handler.decorated` (method) `lazyc2.py:1365` `def decorated()`
- `Handler.requires_auth` (method) `lazyc2.py:1376` `def requires_auth(f)`
- `Handler.decorated` (method) `lazyc2.py:1378` `def decorated()`
- `Handler.csrf_protect` (method) `lazyc2.py:1387` `def csrf_protect(view)` -- Decorator that enforces the per-session CSRF token.
- `Handler.wrapper` (method) `lazyc2.py:1397` `def wrapper()`
- `Handler.aicmd_deepseek` (method) `lazyc2.py:1408` `def aicmd_deepseek(cmd)`
- `Handler.aicmd` (method) `lazyc2.py:1522` `def aicmd(cmd)`
- `Handler.search_database` (method) `lazyc2.py:1627` `def search_database(term, data_path)` -- Busca un término en un DataFrame, manejando listas, dicts y distintas estructuras.
- `Handler.execute_command` (method) `lazyc2.py:1682` `def execute_command(command)`
- `CustomDNSResolver.resolve` (method) `lazyc2.py:1712` `def resolve(self, request, handler)`
- `CustomDNSResolver.start_dns_server` (method) `lazyc2.py:1816` `def start_dns_server()` -- Start the C2 DNS server, gracefully degrading when binding is unsafe.
- `CustomDNSResolver.tcp_bridge` (method) `lazyc2.py:1856` `def tcp_bridge(local_port, remote_host, remote_port)` -- Establish a TCP bridge between a local port and a remote host.
- `CustomDNSResolver.handle_client` (method) `lazyc2.py:1880` `def handle_client(client_socket, remote_host, remote_port)` -- Handle communication between the client and the remote server.
- `CustomDNSResolver.decoy` (method) `lazyc2.py:1899` `def decoy()` -- Serve a decoy page to non-operator IPs when decoy mode is enabled.
- `CustomDNSResolver.encrypt_data` (method) `lazyc2.py:1937` `def encrypt_data(data)`
- `CustomDNSResolver.decrypt_data` (method) `lazyc2.py:1946` `def decrypt_data(encrypted_data, is_file)`
- `CustomDNSResolver.set_winsize` (method) `lazyc2.py:1959` `def set_winsize(fd, row, col, xpix, ypix)` -- Configura el tamaño de la terminal
- `CustomDNSResolver.read_and_forward_pty_output` (method) `lazyc2.py:1965` `def read_and_forward_pty_output()` -- Lectura continua del PTY y envío por WebSocket
- `CustomDNSResolver.get_discovered_hosts` (method) `lazyc2.py:1982` `def get_discovered_hosts()` -- Reads the sessions/hostsdiscovery.txt file and returns a list of discovered hosts.
- `CustomDNSResolver.get_local_ip_addresses` (method) `lazyc2.py:2032` `def get_local_ip_addresses()`
- `CustomDNSResolver.sanitize_json` (method) `lazyc2.py:2057` `def sanitize_json(data)` -- Elimina datos sensibles del diccionario JSON.
- `CustomDNSResolver.add_dynamic_data` (method) `lazyc2.py:2087` `def add_dynamic_data(data)` -- Agrega datos dinámicos al diccionario JSON si es necesario, basándose en el contenido del diccionario 'data'.
- `CustomDNSResolver.get_client_ip` (method) `lazyc2.py:2109` `def get_client_ip()` -- Get the client's IP address, handling proxies.
- `CustomDNSResolver.get_request_details` (method) `lazyc2.py:2118` `def get_request_details()` -- Collect comprehensive request details.
- `CustomDNSResolver.save_to_log` (method) `lazyc2.py:2153` `def save_to_log(data)` -- Append request data to the JSON log file with safe permissions.
- `CustomDNSResolver.parse_access_log_for_short_url` (method) `lazyc2.py:2175` `def parse_access_log_for_short_url(short_url)` -- Parse access.log for entries matching the given short URL.
- `CustomDNSResolver.parse_execution_log` (method) `lazyc2.py:2197` `def parse_execution_log(implante)` -- Parse execution log for the given implante, returning execution events.
- `CustomDNSResolver.load_implant_config` (method) `lazyc2.py:2223` `def load_implant_config(implante)` -- Load implant configuration from JSON file.
- `CustomDNSResolver.load_short_urls` (method) `lazyc2.py:2233` `def load_short_urls()` -- Load short URLs from JSON file, creating it if it doesn't exist.
- `CustomDNSResolver.save_short_urls` (method) `lazyc2.py:2253` `def save_short_urls(data)` -- Save short URLs to JSON file.
- `CustomDNSResolver.is_valid_url` (method) `lazyc2.py:2263` `def is_valid_url(url)` -- Validate if the input is a valid URL or existing local file path.
- `CustomDNSResolver.get_safe_file_path` (method) `lazyc2.py:2271` `def get_safe_file_path(user_path)` -- Construye de forma segura el path del archivo y verifica que está en el directorio permitido.
- `CustomDNSResolver.analyze_behavioral_data` (method) `lazyc2.py:2341` `def analyze_behavioral_data(behavioral_events)` -- Analyze behavioral events using Groq AI to generate risk scores.
- `CustomDNSResolver.analyze_campaign_progress` (method) `lazyc2.py:2369` `def analyze_campaign_progress(campaign_id, events)` -- Analyze campaign progress and suggest adaptations using Grok AI.
- `User.__init__` (method) `lazyc2.py:2875` `def __init__(self, user_data)`
- `User.load_users` (method) `lazyc2.py:2897` `def load_users()`
- `User.save_users` (method) `lazyc2.py:2907` `def save_users(users)`
- `User.load_data` (method) `lazyc2.py:2918` `def load_data()`
- `User.load_user` (method) `lazyc2.py:2935` `def load_user(user_id)`
- `User.tojson_filter` (method) `lazyc2.py:2950` `def tojson_filter(value)` -- Custom tojson filter to handle non-serializable objects.
- `User.index` (method) `lazyc2.py:2957` `def index()`
- `User.send_command` (method) `lazyc2.py:3107` `def send_command(client_id)`
- `User.receive_result` (method) `lazyc2.py:3251` `def receive_result(client_id)`
- `User.issue_command` (method) `lazyc2.py:3792` `def issue_command()`
- `User.upload` (method) `lazyc2.py:3806` `def upload()`
- `User.download_file` (method) `lazyc2.py:3843` `def download_file()`
- `User.serve_file` (method) `lazyc2.py:3870` `def serve_file(file_path)` -- Serve a file from ``sessions/temp_uploads`` through :class:`SafeFileService`.
- `User.create_route` (method) `lazyc2.py:3972` `def create_route()` -- Register a new operator-supplied dynamic route bound to a template.
- `User.dynamic_route` (method) `lazyc2.py:4041` `def dynamic_route(route_path, data)` -- Handle dynamic routes based on stored route-to-template mappings.
- `User.sanitize_input` (method) `lazyc2.py:4048` `def sanitize_input(input_str)` -- Sanitize input to prevent XSS attacks.
- `User.is_valid_route_path` (method) `lazyc2.py:4058` `def is_valid_route_path(route_path)` -- Validate route path format.
- `User.is_valid_data` (method) `lazyc2.py:4065` `def is_valid_data(data)` -- Validate data parameter.
- `User.is_valid_template_name` (method) `lazyc2.py:4075` `def is_valid_template_name(template_name)` -- Validate template name.
- `User.log` (method) `lazyc2.py:4137` `def log(data)` -- Log request details to JSON file.
- `User.favicon` (method) `lazyc2.py:4155` `def favicon()` -- Serve the favicon.ico file.
- `User.palette_view` (method) `lazyc2.py:4168` `def palette_view()` -- Render the operator command palette browser.
- `User.palette_api` (method) `lazyc2.py:4195` `def palette_api()` -- JSON catalogue feed for the global Cmd+K / Ctrl+K overlay.
- `User.api_data` (method) `lazyc2.py:4216` `def api_data()`
- `User.create_short_url` (method) `lazyc2.py:4378` `def create_short_url()` -- Create multiple short URLs for a single original URL.
- `User.track_interaction` (method) `lazyc2.py:4406` `def track_interaction(short_url)` -- Serve tracking page and log behavioral data.
- `User.update_short_url` (method) `lazyc2.py:4431` `def update_short_url(short_url)`
- `User.redirect_to_file` (method) `lazyc2.py:4458` `def redirect_to_file(short_url)`
- `User.webserver_report` (method) `lazyc2.py:4486` `def webserver_report(filename)` -- Serve nmap HTML report assets from the sessions directory over HTTPS.
- `User.download_files` (method) `lazyc2.py:4506` `def download_files(filename)` -- Serve implant stage files by name, enforcing strict containment.
- `User.view_yaml` (method) `lazyc2.py:4558` `def view_yaml()`
- `User.run_command` (method) `lazyc2.py:4600` `def run_command()` -- Execute one shell command and return a sanitised, JSON-safe result.
- `User.get_output` (method) `lazyc2.py:4669` `def get_output()`
- `User.run_shellcode` (method) `lazyc2.py:4696` `def run_shellcode()`
- `User.get_results` (method) `lazyc2.py:4705` `def get_results()`
- `User.send_lcommand` (method) `lazyc2.py:4745` `def send_lcommand(ip, port)`
- `User.chatbot` (method) `lazyc2.py:4778` `def chatbot()`
- `User.vuln` (method) `lazyc2.py:4794` `def vuln()`
- `User.taskbot` (method) `lazyc2.py:4833` `def taskbot()`
- `User.search` (method) `lazyc2.py:4849` `def search()`
- `User.script` (method) `lazyc2.py:4865` `def script()`
- `User.redop` (method) `lazyc2.py:4881` `def redop()`
- `User.adversary` (method) `lazyc2.py:4900` `def adversary()`
- `User.generalbot` (method) `lazyc2.py:4916` `def generalbot()`
- `User.csv_to_html` (method) `lazyc2.py:4932` `def csv_to_html()`
- `User.search_results` (method) `lazyc2.py:4983` `def search_results()`
- `User.graph` (method) `lazyc2.py:5031` `def graph()`
- `User.task` (method) `lazyc2.py:5040` `def task(task_id)`
- `User.get_tasks` (method) `lazyc2.py:5055` `def get_tasks()`
- `User.tasks` (method) `lazyc2.py:5065` `def tasks()`
- `User.edit_task` (method) `lazyc2.py:5075` `def edit_task(task_id)`
- `User.cves` (method) `lazyc2.py:5109` `def cves()`
- `User.cve` (method) `lazyc2.py:5135` `def cve(cve_id)`
- `User.edit_cve` (method) `lazyc2.py:5150` `def edit_cve(cve_id)`
- `User.edit_notes` (method) `lazyc2.py:5184` `def edit_notes()`
- `User.get_notes` (method) `lazyc2.py:5202` `def get_notes()`
- `User.view_note` (method) `lazyc2.py:5212` `def view_note()`
- `User.push_notification` (method) `lazyc2.py:5222` `def push_notification()`
- `User.edit_event` (method) `lazyc2.py:5249` `def edit_event(event_name)`
- `User.get_event_config` (method) `lazyc2.py:5284` `def get_event_config()`
- `User.get_event_config_view` (method) `lazyc2.py:5291` `def get_event_config_view()`
- `User.aicmd_view` (method) `lazyc2.py:5326` `def aicmd_view()`
- `User.get_events` (method) `lazyc2.py:5351` `def get_events()`
- `User.list_tools` (method) `lazyc2.py:5383` `def list_tools()`
- `User.create_tool` (method) `lazyc2.py:5393` `def create_tool()`
- `User.view_tool` (method) `lazyc2.py:5420` `def view_tool(toolname)`
- `User.update_tool` (method) `lazyc2.py:5451` `def update_tool(toolname)`
- `User.delete_tool` (method) `lazyc2.py:5499` `def delete_tool(toolname)`
- `User.register` (method) `lazyc2.py:5534` `def register()`
- `User.login` (method) `lazyc2.py:5593` `def login()`
- `User.mfa_setup` (method) `lazyc2.py:5640` `def mfa_setup()`
- `User.mfa_qr` (method) `lazyc2.py:5714` `def mfa_qr(username)` -- Serve a locally-generated QR code SVG for MFA setup.
- `User.mfa_verify` (method) `lazyc2.py:5736` `def mfa_verify()`
- `User.admin_users` (method) `lazyc2.py:5784` `def admin_users()`
- `User.admin_set_role` (method) `lazyc2.py:5799` `def admin_set_role(user_id)`
- `User.admin_reset_mfa` (method) `lazyc2.py:5821` `def admin_reset_mfa(user_id)`
- `User.admin_delete_user` (method) `lazyc2.py:5833` `def admin_delete_user(user_id)`
- `User.admin_tenants` (method) `lazyc2.py:5851` `def admin_tenants()`
- `User.admin_create_tenant` (method) `lazyc2.py:5872` `def admin_create_tenant()`
- `User.admin_switch_tenant` (method) `lazyc2.py:5891` `def admin_switch_tenant(tenant_id)`
- `User.profile` (method) `lazyc2.py:5905` `def profile()`
- `User.logout` (method) `lazyc2.py:5929` `def logout()`
- `User.change_password` (method) `lazyc2.py:5944` `def change_password()` -- Force rotation of the initial one-time admin password.
- `User.aumentar_elo_route` (method) `lazyc2.py:6010` `def aumentar_elo_route(user_id)`
- `User.banners` (method) `lazyc2.py:6026` `def banners()`
- `User.mitre` (method) `lazyc2.py:6062` `def mitre()`
- `User.get_connected_clients` (method) `lazyc2.py:6107` `def get_connected_clients()`
- `User.lazybot` (method) `lazyc2.py:6118` `def lazybot()`
- `User.compliance_dashboard` (method) `lazyc2.py:6135` `def compliance_dashboard()`
- `User.compliance_report` (method) `lazyc2.py:6157` `def compliance_report()`
- `User.compliance_add_evidence` (method) `lazyc2.py:6186` `def compliance_add_evidence()`
- `User.compliance_verify_evidence` (method) `lazyc2.py:6222` `def compliance_verify_evidence()`
- `User.compliance_export` (method) `lazyc2.py:6236` `def compliance_export(format)`
- `User.lazyreport` (method) `lazyc2.py:6266` `def lazyreport()`
- `User.teamserver` (method) `lazyc2.py:6285` `def teamserver()`
- `User.report` (method) `lazyc2.py:6314` `def report()`
- `User.lazyreport_view` (method) `lazyc2.py:6321` `def lazyreport_view()`
- `User.killchain_view` (method) `lazyc2.py:6327` `def killchain_view()`
- `User.api_killchain` (method) `lazyc2.py:6357` `def api_killchain()` -- Return the unified kill-chain snapshot consumed by every surface.
- `User.api_beacon_results` (method) `lazyc2.py:6388` `def api_beacon_results(client_id)` -- Return the full ordered command/result history for one beacon.
- `User.connect` (method) `lazyc2.py:6488` `def connect()`
- `User.listener` (method) `lazyc2.py:6497` `def listener()`
- `User.listener_connect` (method) `lazyc2.py:6506` `def listener_connect()`
- `User.listener_disconnect` (method) `lazyc2.py:6517` `def listener_disconnect()`
- `User.pty_input` (method) `lazyc2.py:6527` `def pty_input(data)`
- `User.resize` (method) `lazyc2.py:6541` `def resize(data)`
- `User.pty_connect` (method) `lazyc2.py:6554` `def pty_connect()`
- `User.handle_input` (method) `lazyc2.py:6585` `def handle_input(data)`
- `User.listener_command` (method) `lazyc2.py:6609` `def listener_command(msg)`
- `User.terminal` (method) `lazyc2.py:6623` `def terminal()`
- `User.terminal_connect` (method) `lazyc2.py:6632` `def terminal_connect()`
- `User.terminal_disconnect` (method) `lazyc2.py:6642` `def terminal_disconnect()`
- `User.terminal_input` (method) `lazyc2.py:6652` `def terminal_input(data)`
- `User.terminal_command` (method) `lazyc2.py:6665` `def terminal_command(data)`
- `User.terminal_resize` (method) `lazyc2.py:6680` `def terminal_resize(data)`
- `User.start_reverse_shell` (method) `lazyc2.py:6689` `def start_reverse_shell()`
- `User.start_bridge` (method) `lazyc2.py:6736` `def start_bridge()` -- Start a TCP bridge to a specified remote host and port.
- `User.page_not_found` (method) `lazyc2.py:6753` `def page_not_found(e)`
- `User.internal_server_error` (method) `lazyc2.py:6761` `def internal_server_error(e)`
- `User.get_config` (method) `lazyc2.py:6770` `def get_config()` -- Lee el archivo payload.json, lo manipula y lo expone como /config.json.
- `User.capture_image` (method) `lazyc2.py:6789` `def capture_image()`
- `User.capture_audio` (method) `lazyc2.py:6815` `def capture_audio()`
- `User.surface` (method) `lazyc2.py:6833` `def surface()`
- `User.surface_live` (method) `lazyc2.py:6839` `def surface_live()` -- Render the live attack-surface graph page.
- `User.api_surface_live` (method) `lazyc2.py:6854` `def api_surface_live()` -- Return the live attack-surface graph derived from the world model.
- `User.get_data` (method) `lazyc2.py:6879` `def get_data()`
- `User.upload_zip_file` (method) `lazyc2.py:6888` `def upload_zip_file()` -- Handles the file upload, processes the BloodHound ZIP, and prepares data for visualization.
- `User.list_campaigns` (method) `lazyc2.py:6946` `def list_campaigns()`
- `User.create_campaign` (method) `lazyc2.py:6959` `def create_campaign()`
- `User.lazyphishingai` (method) `lazyc2.py:7037` `def lazyphishingai()`
- `User.track_pixel` (method) `lazyc2.py:7053` `def track_pixel(campaign_id, email)` -- Píxel de seguimiento para registrar aperturas.
- `User.campaign_report` (method) `lazyc2.py:7075` `def campaign_report(campaign_id)`
- `User.orchestrate_campaign` (method) `lazyc2.py:7157` `def orchestrate_campaign(campaign_id)`
- `User.create_multivector_campaign` (method) `lazyc2.py:7204` `def create_multivector_campaign()`
- `User.serve_landing_page` (method) `lazyc2.py:7356` `def serve_landing_page(campaign_id, short_url)`
- `User.health_check` (method) `lazyc2.py:7381` `def health_check()` -- Basic health and readiness endpoint.
- `User.metrics_exposition` (method) `lazyc2.py:7420` `def metrics_exposition()` -- Prometheus-compatible metrics endpoint.
- `User.api_dashboard` (method) `lazyc2.py:7427` `def api_dashboard()` -- Aggregated JSON dashboard: beacons, campaign, events, facts summary.
- `User.api_listeners` (method) `lazyc2.py:7497` `def api_listeners()` -- List all configured C2 listeners and their runtime status.
- `User.api_listeners_create` (method) `lazyc2.py:7504` `def api_listeners_create()` -- Create a new listener.
- `User.api_listeners_start` (method) `lazyc2.py:7520` `def api_listeners_start(listener_id)` -- Start an existing listener.
- `User.api_listeners_stop` (method) `lazyc2.py:7528` `def api_listeners_stop(listener_id)` -- Stop a running listener.
- `User.api_listeners_delete` (method) `lazyc2.py:7536` `def api_listeners_delete(listener_id)` -- Remove a listener configuration.

## lazyc2/addon_creator.py
Imported by: `lazyc2/blueprints/addons.py`, `tests/test_addon_creator.py`, `tests/test_placeholder_coverage.py`
- `ParamSpec.to_dict` (method) `lazyc2/addon_creator.py:353` `def to_dict(self)` -- Return the param as a schema-ordered mapping.
- `AddonValidationError.__init__` (method) `lazyc2/addon_creator.py:409` `def __init__(self, issues)`
- `AddonValidator.__init__` (method) `lazyc2/addon_creator.py:422` `def __init__(self, draft, config)` -- Store the draft and configuration used by every check.
- `AddonValidator.validate` (method) `lazyc2/addon_creator.py:436` `def validate(self)` -- Run every rule and return the collected issues.
- `AddonValidator.is_valid` (method) `lazyc2/addon_creator.py:450` `def is_valid(self)` -- Return True when the draft passes every rule.
- `AddonYamlRenderer.__init__` (method) `lazyc2/addon_creator.py:721` `def __init__(self, config)` -- Store the configuration used for defaults.
- `AddonYamlRenderer.render` (method) `lazyc2/addon_creator.py:729` `def render(self, draft)` -- Return the YAML document for the draft.
- `AddonYamlRenderer.to_document` (method) `lazyc2/addon_creator.py:747` `def to_document(self, draft)` -- Build the schema-ordered document mapping for the draft.
- `AddonStore.__init__` (method) `lazyc2/addon_creator.py:812` `def __init__(self, config, base_dir)` -- Configure the store.
- `AddonStore.resolve_path` (method) `lazyc2/addon_creator.py:827` `def resolve_path(self, name)` -- Return the safe absolute path for a newly created addon name.
- `AddonStore.resolve_existing_path` (method) `lazyc2/addon_creator.py:842` `def resolve_existing_path(self, name)` -- Return the safe absolute path for an existing addon file.
- `AddonStore.exists` (method) `lazyc2/addon_creator.py:886` `def exists(self, name)` -- Return True when an addon file already exists for the name.
- `AddonStore.save` (method) `lazyc2/addon_creator.py:897` `def save(self, name, yaml_text)` -- Persist the YAML document atomically.
- `AddonStore.load` (method) `lazyc2/addon_creator.py:951` `def load(self, name)` -- Return the parsed addon document for a name.
- `AddonStore.delete` (method) `lazyc2/addon_creator.py:974` `def delete(self, name)` -- Delete the addon file for a name.
- `AddonStore.list_all` (method) `lazyc2/addon_creator.py:990` `def list_all(self)` -- Return summary dicts for every parseable addon.
- `AddonStore.parse_addon_form` (method) `lazyc2/addon_creator.py:1070` `def parse_addon_form(form)` -- Adapt raw form data into an AddonDraft.

## lazyc2/app_factory.py
Depends on: `core/api_authz.py`, `lazyc2/blueprints/__init__.py`, `lazyc2/extensions/__init__.py`, `lazyc2/security/services.py`
- `create_app` (function) `lazyc2/app_factory.py:89` `def create_app()` -- Create and return a fully configured C2 Flask application.

## lazyc2/blueprints/addons.py
Depends on: `lazyc2/addon_creator.py`, `lazyc2/blueprints/session_auth.py`, `lazyc2/extensions/decoy.py`, `lazyc2/security/csrf.py`
Imported by: `lazyc2/blueprints/__init__.py`, `tests/test_addon_creator.py`, `tests/test_security_hardening_v5.py`
- `init_addons_bp` (function) `lazyc2/blueprints/addons.py:66` `def init_addons_bp(base_dir)` -- Configure the blueprint state before registration.
- `csrf_protect` (function) `lazyc2/blueprints/addons.py:93` `def csrf_protect(view)` -- Decorate a view so mutating requests must echo the CSRF token.
- `wrapper` (function) `lazyc2/blueprints/addons.py:107` `def wrapper()`
- `list_addons` (function) `lazyc2/blueprints/addons.py:260` `def list_addons()` -- Render the addon dashboard list page with a fresh CSRF token.
- `create_addon` (function) `lazyc2/blueprints/addons.py:274` `def create_addon()` -- Render the creation form and persist valid addon submissions.
- `view_addon` (function) `lazyc2/blueprints/addons.py:317` `def view_addon(name)` -- Render the persisted YAML document for an addon.
- `delete_addon` (function) `lazyc2/blueprints/addons.py:341` `def delete_addon(name)` -- Delete an addon file.

## lazyc2/blueprints/api.py
Depends on: `core/api_authz.py`, `core/logging.py`
Imported by: `lazyc2/blueprints/__init__.py`, `lazyc2/blueprints/api_v1.py`, `tests/test_security_hardening_v5.py`
- `HealthConfig.health` (method) `lazyc2/blueprints/api.py:108` `def health()` -- Health-check endpoint returning subsystem status.
- `HealthConfig.ping` (method) `lazyc2/blueprints/api.py:120` `def ping()` -- Lightweight liveness probe.
- `HealthConfig.require_api_auth_with_store` (method) `lazyc2/blueprints/api.py:129` `def require_api_auth_with_store(view)` -- Protect a view with the app-scoped API key store.
- `HealthConfig.guarded` (method) `lazyc2/blueprints/api.py:146` `def guarded()`
- `HealthConfig.health_tenant` (method) `lazyc2/blueprints/api.py:157` `def health_tenant()` -- Health-check scoped to the current authenticated tenant.

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
Depends on: `lazyc2/__init__.py`, `lazyc2/extensions/decoy.py`, `lazyc2/extensions/users.py`, `modules/lazy_rbac.py`
Imported by: `lazyc2/blueprints/__init__.py`, `lazygui/services/teamserver_backend.py`, `static/js/socket.io-4.0.0.min.js`, `static/js/socket.io-4.3.2.min.js`
- `require_role` (function) `lazyc2/blueprints/auth.py:33` `def require_role(role)` -- Return a pass-through decorator when RBAC is unavailable.
- `register` (function) `lazyc2/blueprints/auth.py:92` `def register()`
- `login` (function) `lazyc2/blueprints/auth.py:151` `def login()`
- `mfa_setup` (function) `lazyc2/blueprints/auth.py:196` `def mfa_setup()`
- `mfa_qr` (function) `lazyc2/blueprints/auth.py:269` `def mfa_qr(username)`
- `mfa_verify` (function) `lazyc2/blueprints/auth.py:291` `def mfa_verify()`
- `profile` (function) `lazyc2/blueprints/auth.py:335` `def profile()`
- `logout` (function) `lazyc2/blueprints/auth.py:360` `def logout()`
- `admin_users` (function) `lazyc2/blueprints/auth.py:379` `def admin_users()`
- `admin_set_role` (function) `lazyc2/blueprints/auth.py:396` `def admin_set_role(user_id)`
- `admin_reset_mfa` (function) `lazyc2/blueprints/auth.py:418` `def admin_reset_mfa(user_id)`
- `admin_delete_user` (function) `lazyc2/blueprints/auth.py:430` `def admin_delete_user(user_id)`
- `admin_tenants` (function) `lazyc2/blueprints/auth.py:448` `def admin_tenants()`
- `admin_create_tenant` (function) `lazyc2/blueprints/auth.py:468` `def admin_create_tenant()`
- `admin_switch_tenant` (function) `lazyc2/blueprints/auth.py:486` `def admin_switch_tenant(tenant_id)`

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
Depends on: `core/logging.py`, `lazyc2/extensions/short_urls.py`, `modules/security_sanitizers.py`, `utils.py`
Imported by: `lazyc2/blueprints/__init__.py`
- `create_short_url` (function) `lazyc2/blueprints/phishing.py:47` `def create_short_url()` -- Create one or more short URLs for a single original URL.
- `track_interaction` (function) `lazyc2/blueprints/phishing.py:87` `def track_interaction(short_url)` -- Serve a tracking page and log behavioural data.
- `update_short_url` (function) `lazyc2/blueprints/phishing.py:123` `def update_short_url(short_url)` -- Update an existing short URL's target or active status.
- `redirect_to_file` (function) `lazyc2/blueprints/phishing.py:149` `def redirect_to_file(short_url)` -- Resolve a short URL and redirect (or serve a local file).
- `webserver_report` (function) `lazyc2/blueprints/phishing.py:172` `def webserver_report(filename)` -- Serve nmap HTML report assets from the sessions directory.
- `download_files` (function) `lazyc2/blueprints/phishing.py:190` `def download_files(filename)` -- Serve a session file by name with path-traversal protection.

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

## lazyc2/security/csrf.py
Imported by: `lazyc2.py`, `lazyc2/blueprints/addons.py`, `tests/test_csrf_behavior.py`, `tests/test_csrf_policy.py`
- `CSRFPolicy.__init__` (method) `lazyc2/security/csrf.py:69` `def __init__(self, header, form_field, cookie_name, exempt_paths, secret)`
- `CSRFPolicy.header` (method) `lazyc2/security/csrf.py:85` `def header(self)` -- Return the HTTP header name carrying the token.
- `CSRFPolicy.cookie_name` (method) `lazyc2/security/csrf.py:90` `def cookie_name(self)` -- Return the cookie name that should hold the readable token.
- `CSRFPolicy.issue` (method) `lazyc2/security/csrf.py:94` `def issue(self, session_id)` -- Return the token bound to ``session_id``.
- `CSRFPolicy.rotate` (method) `lazyc2/security/csrf.py:111` `def rotate(self, session_id)` -- Force a fresh token for ``session_id``.
- `CSRFPolicy.forget` (method) `lazyc2/security/csrf.py:126` `def forget(self, session_id)` -- Drop the token bound to ``session_id`` (e.g. on logout).
- `CSRFPolicy.validate` (method) `lazyc2/security/csrf.py:130` `def validate(self, session_id, candidate)` -- Return ``True`` iff ``candidate`` matches the stored token.
- `CSRFPolicy.is_exempt` (method) `lazyc2/security/csrf.py:147` `def is_exempt(self, path)` -- Return ``True`` if ``path`` is in the exempt set.
- `CSRFPolicy.extract_token` (method) `lazyc2/security/csrf.py:163` `def extract_token(self, request)` -- Return the token from a Flask-shaped request.
- `CSRFPolicy.check_request` (method) `lazyc2/security/csrf.py:182` `def check_request(self, session_id, request)` -- Run the full CSRF gate against a request.

## lazyc2/security/html_sanitizer.py
Depends on: `lazyc2/security/constants.py`
Imported by: `lazyc2.py`, `tests/test_html_sanitizer.py`
- `sanitize_html` (function) `lazyc2/security/html_sanitizer.py:78` `def sanitize_html(raw_html, allowed_tags, allowed_attributes)` -- Return a sanitized HTML string safe for ``render_template``.

## lazyc2/security/https_redirect.py
Imported by: `lazyc2.py`, `tests/test_https_redirect.py`
- `HTTPSRedirect.__init__` (method) `lazyc2/security/https_redirect.py:51` `def __init__(self, env, enabled)`
- `HTTPSRedirect.enabled` (method) `lazyc2/security/https_redirect.py:56` `def enabled(self)` -- Return ``True`` when the policy is active.
- `HTTPSRedirect.evaluate` (method) `lazyc2/security/https_redirect.py:60` `def evaluate(self, request)` -- Return a redirect response, or ``None`` if the request can pass.

## lazyc2/security/services.py
Depends on: `lazyc2/security/constants.py`, `lazyc2/security/validators.py`
Imported by: `lazyc2.py`, `lazyc2/app_factory.py`, `tests/test_security_lazyc2.py`
- `SecretKeyManager.__init__` (method) `lazyc2/security/services.py:30` `def __init__(self, sessions_dir)`
- `SecretKeyManager.get_or_create` (method) `lazyc2/security/services.py:33` `def get_or_create(self)` -- Return an existing secret key or generate and persist a new one.
- `SafeFileService.__init__` (method) `lazyc2/security/services.py:63` `def __init__(self, base_dir)`
- `SafeFileService.read_bytes` (method) `lazyc2/security/services.py:86` `def read_bytes(self, relative_path)` -- Read a file as bytes after path validation.
- `SafeFileService.read_text` (method) `lazyc2/security/services.py:102` `def read_text(self, relative_path, encoding)` -- Read a file as text after path validation.
- `SafeFileService.write_bytes` (method) `lazyc2/security/services.py:119` `def write_bytes(self, relative_path, data)` -- Write bytes to a file after path validation.
- `SafeFileService.exists` (method) `lazyc2/security/services.py:136` `def exists(self, relative_path)` -- Check if a path exists after validation.
- `AESKeyManager.__init__` (method) `lazyc2/security/services.py:158` `def __init__(self, key_file)`
- `AESKeyManager.get_or_generate` (method) `lazyc2/security/services.py:161` `def get_or_generate(self)` -- Return an existing AES key or generate a new one.
- `UploadSizeValidator.__init__` (method) `lazyc2/security/services.py:189` `def __init__(self, max_size_bytes)`
- `UploadSizeValidator.validate` (method) `lazyc2/security/services.py:192` `def validate(self, content_length)` -- Validate upload size.

## lazyc2/security/trusted_proxy.py
Imported by: `lazyc2.py`, `tests/test_trusted_proxy.py`
- `TrustedProxyResolver.__init__` (method) `lazyc2/security/trusted_proxy.py:42` `def __init__(self, trusted_count, operator_allowlist)`
- `TrustedProxyResolver.trusted_count` (method) `lazyc2/security/trusted_proxy.py:53` `def trusted_count(self)` -- Return the configured number of trusted proxy hops.
- `TrustedProxyResolver.client_ip` (method) `lazyc2/security/trusted_proxy.py:57` `def client_ip(self, remote_addr, x_forwarded_for)` -- Return the resolved client IP.
- `TrustedProxyResolver.is_operator` (method) `lazyc2/security/trusted_proxy.py:80` `def is_operator(self, ip)` -- Return ``True`` when ``ip`` is in the operator allowlist.

## lazyc2/security/validators.py
Depends on: `lazyc2/security/constants.py`
Imported by: `lazyc2.py`, `lazyc2/security/services.py`, `tests/test_security_lazyc2.py`, `tests/test_short_url_file_containment.py`
- `validate_route_path` (function) `lazyc2/security/validators.py:24` `def validate_route_path(route_path)` -- Validate a dynamic route path segment.
- `validate_template_name` (function) `lazyc2/security/validators.py:46` `def validate_template_name(template_name)` -- Validate a Jinja2 template filename.
- `validate_yaml_filename` (function) `lazyc2/security/validators.py:68` `def validate_yaml_filename(filename)` -- Validate a YAML filename for safe loading.
- `validate_request_data` (function) `lazyc2/security/validators.py:86` `def validate_request_data(data)` -- Validate request data length to prevent buffer abuse.
- `validate_aes_key` (function) `lazyc2/security/validators.py:102` `def validate_aes_key(key)` -- Validate AES key length.
- `validate_password_length` (function) `lazyc2/security/validators.py:118` `def validate_password_length(password)` -- Validate password meets minimum length requirement.
- `validate_upload_size` (function) `lazyc2/security/validators.py:134` `def validate_upload_size(content_length)` -- Validate upload size against maximum allowed.
- `validate_file_path_within_base` (function) `lazyc2/security/validators.py:150` `def validate_file_path_within_base(file_path, base_dir)` -- Validate that a resolved file path is within a base directory.
- `resolve_contained_file_path` (function) `lazyc2/security/validators.py:174` `def resolve_contained_file_path(raw_url, base_dir)` -- Resolve a short-URL target to a file path contained in ``base_dir``.

## lazygui/__main__.py
Depends on: `lazygui/app.py`
- `main` (function) `lazygui/__main__.py:14` `def main()` -- Bootstrap the GUI and run the Qt event loop.

## lazygui/app.py
Depends on: `core/logging.py`, `lazygui/config/c2_credentials.py`, `lazygui/config/constants.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/factory.py`, `lazygui/services/models.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`
Imported by: `lazygui/__main__.py`
- `Application.__init__` (method) `lazygui/app.py:36` `def __init__(self, argv)` -- Build constants/settings/theme/backend/main-window.
- `Application.run` (method) `lazygui/app.py:65` `def run(self)` -- Show the main window, start the backend, and run the event loop.
- `Application.show_connect_dialog` (method) `lazygui/app.py:100` `def show_connect_dialog(self)` -- Open the connection dialog and swap backends if accepted.

## lazygui/config/c2_credentials.py
Depends on: `core/logging.py`
Imported by: `lazygui/app.py`, `lazygui/windows/connect_dialog.py`
- `C2Credentials.empty` (method) `lazygui/config/c2_credentials.py:33` `def empty(cls)` -- Return a sentinel representing no credentials available.
- `C2Credentials.load_c2_credentials_from_file` (method) `lazygui/config/c2_credentials.py:38` `def load_c2_credentials_from_file(file_path)` -- Parse ``.c2_credentials.txt`` and return username + password.
- `C2Credentials.load_c2_credentials` (method) `lazygui/config/c2_credentials.py:71` `def load_c2_credentials(project_root)` -- Resolve and parse the credentials file relative to ``project_root``.

## lazygui/config/constants.py
Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/config/paths.py`, `lazygui/config/settings.py`, `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`, `lazygui/services/event_log.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/services/teamserver_backend.py`, `lazygui/theme/manager.py`, `lazygui/theme/qss_builder.py`, `lazygui/widgets/command_palette_list.py`, `lazygui/widgets/event_log_view.py`, `lazygui/widgets/filter_bar.py`, `lazygui/widgets/graph_view.py`, `lazygui/widgets/terminal_view.py`, `lazygui/windows/command_palette_window.py`, `lazygui/windows/connect_dialog.py`, `lazygui/windows/main_window.py`, `tests/test_lazygui_backend.py`, `tests/test_lazygui_graph_widget.py`
- `AppConstants.panel_labels` (method) `lazygui/config/constants.py:239` `def panel_labels(self)` -- Map panel identifier to human-readable label.

## lazygui/config/paths.py
Depends on: `lazygui/config/constants.py`
Imported by: `lazygui/app.py`, `lazygui/config/__init__.py`, `lazygui/config/settings.py`, `lazygui/services/factory.py`, `lazygui/services/local_backend.py`, `lazygui/windows/connect_dialog.py`
- `AppPaths.config_dir` (method) `lazygui/config/paths.py:32` `def config_dir(self)` -- User config directory respecting ``XDG_CONFIG_HOME`` when set.
- `AppPaths.settings_file` (method) `lazygui/config/paths.py:39` `def settings_file(self)` -- Absolute path of the persisted settings JSON file.
- `AppPaths.layout_file` (method) `lazygui/config/paths.py:44` `def layout_file(self)` -- Absolute path of the persisted Qt layout binary blob.
- `AppPaths.project_run_script` (method) `lazygui/config/paths.py:49` `def project_run_script(self)` -- Absolute path to the ``run`` shell launcher in the repository.
- `AppPaths.lazyc2_script` (method) `lazygui/config/paths.py:54` `def lazyc2_script(self)` -- Absolute path to the Flask backend ``lazyc2.py``.
- `AppPaths.c2_credentials_path` (method) `lazygui/config/paths.py:59` `def c2_credentials_path(self)` -- Absolute path to the C2 auto-generated credentials file.
- `AppPaths.sessions_dir` (method) `lazygui/config/paths.py:69` `def sessions_dir(self)` -- Absolute path to the sessions directory.
- `AppPaths.ensure_config_dir` (method) `lazygui/config/paths.py:73` `def ensure_config_dir(self)` -- Create the config directory if missing and return it.


Next: [API_p8.md](API_p8.md)
