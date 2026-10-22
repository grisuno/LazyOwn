# API (page 14 of 24)
Previous: [API_p13.md](API_p13.md)

## modules/lazyatack.sh
- `mostrar_ayuda` (function) `modules/lazyatack.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyatack.sh:33` -- Función para validar una dirección IP
- `validar_url` (function) `modules/lazyatack.sh:49` -- Función para validar URL
- `descargar_seclists` (function) `modules/lazyatack.sh:107` -- Función para descargar y extraer SecLists
- `escanear_puertos` (function) `modules/lazyatack.sh:115` -- Función para ejecutar escaneo de puertos con nmap
- `escanear_puertos_especificos` (function) `modules/lazyatack.sh:121` -- Función para escanear puertos específicos
- `enumerar_http` (function) `modules/lazyatack.sh:127` -- Función para enumerar servicios HTTP
- `iniciar_servidor_http` (function) `modules/lazyatack.sh:133` -- Función para iniciar servidor HTTP con Python
- `configurar_netcat` (function) `modules/lazyatack.sh:139` -- Función para configurar netcat
- `enviar_archivo_netcat` (function) `modules/lazyatack.sh:145` -- Función para enviar archivo mediante bash a netcat
- `verificar_conectividad` (function) `modules/lazyatack.sh:151` -- Función para verificar conectividad con ping y tcpdump
- `verificar_curl` (function) `modules/lazyatack.sh:158` -- Función para verificar conectividad con curl
- `configurar_shell_reversa` (function) `modules/lazyatack.sh:165` -- Función para configurar una shell reversa
- `escuchar_shell` (function) `modules/lazyatack.sh:171` -- Función para escuchar shell con netcat
- `monitorear_procesos` (function) `modules/lazyatack.sh:177` -- Función para monitorear procesos
- `ejecutar_wfuzz` (function) `modules/lazyatack.sh:188` -- Función para ejecutar wfuzz
- `comprobar_sudo` (function) `modules/lazyatack.sh:194` -- Función para comprobar permisos sudo
- `explotar_lfi` (function) `modules/lazyatack.sh:200` -- Función para explotar LFI
- `configurar_tty` (function) `modules/lazyatack.sh:206` -- Función para configurar TTY
- `eliminar_archivos` (function) `modules/lazyatack.sh:217` -- Función para eliminar archivos de forma segura
- `obtener_root_shell` (function) `modules/lazyatack.sh:223` -- Función para obtener root shell mediante Docker
- `enumerar_suid` (function) `modules/lazyatack.sh:230` -- Función para enumerar archivos con SUID
- `listar_timers` (function) `modules/lazyatack.sh:236` -- Función para listar timers de systemd
- `comprobar_rutas` (function) `modules/lazyatack.sh:242` -- Función para comprobar rutas de comandos
- `abusar_tar` (function) `modules/lazyatack.sh:248` -- Función para abusar de tar
- `enumerar_puertos` (function) `modules/lazyatack.sh:254` -- Función para enumerar puertos abiertos
- `eliminar_contenedores_docker` (function) `modules/lazyatack.sh:260` -- Función para eliminar contenedores Docker
- `escanear_red` (function) `modules/lazyatack.sh:266` -- Función para escanear red
- `menu_servidor` (function) `modules/lazyatack.sh:272` -- Función para mostrar menú en modo servidor
- `menu_cliente` (function) `modules/lazyatack.sh:307` -- Función para mostrar menú en modo cliente

## modules/lazycloud.py
Imported by: `cli/commands/cloud.py`
- `CloudMetadataHarvester.__init__` (method) `modules/lazycloud.py:111` `def __init__(self, timeout)`
- `CloudMetadataHarvester.session` (method) `modules/lazycloud.py:116` `def session(self)`
- `CloudMetadataHarvester.harvest_aws` (method) `modules/lazycloud.py:139` `def harvest_aws(self)` -- Harvest AWS EC2 instance metadata (IMDSv2 capable).
- `CloudMetadataHarvester.harvest_azure` (method) `modules/lazycloud.py:184` `def harvest_azure(self)` -- Harvest Azure instance metadata.
- `CloudMetadataHarvester.harvest_gcp` (method) `modules/lazycloud.py:208` `def harvest_gcp(self)` -- Harvest GCP instance metadata.
- `CloudMetadataHarvester.harvest_all` (method) `modules/lazycloud.py:231` `def harvest_all(self)` -- Try all three cloud providers sequentially.
- `CloudBucketEnumerator.__init__` (method) `modules/lazycloud.py:251` `def __init__(self, timeout)`
- `CloudBucketEnumerator.session` (method) `modules/lazycloud.py:256` `def session(self)`
- `CloudBucketEnumerator.enumerate_s3` (method) `modules/lazycloud.py:278` `def enumerate_s3(self, prefix, buckets)` -- Enumerate S3 buckets derived from a prefix.
- `CloudBucketEnumerator.enumerate_azure_storage` (method) `modules/lazycloud.py:303` `def enumerate_azure_storage(self, prefix, accounts)` -- Enumerate Azure Blob Storage accounts.
- `CloudBucketEnumerator.enumerate_gcp_storage` (method) `modules/lazycloud.py:321` `def enumerate_gcp_storage(self, prefix, buckets)` -- Enumerate GCP Storage buckets.
- `CloudIAMEnumerator.enumerate_aws_iam` (method) `modules/lazycloud.py:345` `def enumerate_aws_iam(self, access_key, secret_key, session_token)` -- Enumerate AWS IAM (requires valid credentials).
- `CloudScanner.__init__` (method) `modules/lazycloud.py:393` `def __init__(self, target_domain, timeout)`
- `CloudScanner.full_scan` (method) `modules/lazycloud.py:400` `def full_scan(self, target_prefix, sessions_dir)` -- Perform a comprehensive cloud security scan.
- `CloudScanner.quick_metadata` (method) `modules/lazycloud.py:456` `def quick_metadata(self)` -- Fast metadata-only harvest (no bucket enumeration).
- `CloudScanner.quick_buckets` (method) `modules/lazycloud.py:460` `def quick_buckets(self, prefix)` -- Fast S3-only bucket check.

## modules/lazycurl.sh
- `ctrl_c` (function) `modules/lazycurl.sh:23`
- `show_help` (function) `modules/lazycurl.sh:29` -- Función para mostrar la ayuda
- `execute_curl` (function) `modules/lazycurl.sh:52` -- Función para ejecutar el comando CURL

## modules/lazyencoder_decoder.py
Imported by: `contrib/legacy/lazycreate_webshell.py`, `contrib/legacy/lazylogpoisoning.py`, `contrib/legacy/lazyreversentlmv2.py`, `modules/test_lazyencoder_decoder.py`, `utils.py`
- `base64_encode` (function) `modules/lazyencoder_decoder.py:4` `def base64_encode(data)`
- `base64_decode` (function) `modules/lazyencoder_decoder.py:8` `def base64_decode(data)`
- `caesar_cipher` (function) `modules/lazyencoder_decoder.py:13` `def caesar_cipher(text, shift)`
- `caesar_decipher` (function) `modules/lazyencoder_decoder.py:27` `def caesar_decipher(text, shift)`
- `key_substitution` (function) `modules/lazyencoder_decoder.py:31` `def key_substitution(text, key)`
- `key_substitution_reverse` (function) `modules/lazyencoder_decoder.py:47` `def key_substitution_reverse(text, key)`
- `encode` (function) `modules/lazyencoder_decoder.py:63` `def encode(data, shift, key)`
- `encode_string` (function) `modules/lazyencoder_decoder.py:75` `def encode_string(data, shift, key)`
- `decode` (function) `modules/lazyencoder_decoder.py:82` `def decode(data, shift, key)`
- `decode_string` (function) `modules/lazyencoder_decoder.py:94` `def decode_string(data, shift, key)`

## modules/lazyevilwimrm.sh
- `execute_evil_winrm` (function) `modules/lazyevilwimrm.sh:14` -- Función para ejecutar evil-winrm y verificar la salida

## modules/lazyk8s.py
Imported by: `cli/commands/containers.py`
- `DockerEnumerator.__init__` (method) `modules/lazyk8s.py:44` `def __init__(self, socket_path)`
- `DockerEnumerator.is_socket_accessible` (method) `modules/lazyk8s.py:47` `def is_socket_accessible(self)` -- Check if the Docker socket is readable/writable.
- `DockerEnumerator.list_containers` (method) `modules/lazyk8s.py:70` `def list_containers(self)` -- List all containers with extended information.
- `DockerEnumerator.list_images` (method) `modules/lazyk8s.py:94` `def list_images(self)` -- List all Docker images.
- `DockerEnumerator.inspect_container` (method) `modules/lazyk8s.py:118` `def inspect_container(self, container_id)` -- Get detailed configuration of a container (privileged, mounts, capabilities).
- `DockerEnumerator.check_privileged_containers` (method) `modules/lazyk8s.py:137` `def check_privileged_containers(self)` -- Find containers running with --privileged flag.
- `DockerEnumerator.check_sensitive_mounts` (method) `modules/lazyk8s.py:162` `def check_sensitive_mounts(self)` -- Find containers with sensitive host path mounts.
- `DockerEnumerator.check_docker_socket_mount` (method) `modules/lazyk8s.py:196` `def check_docker_socket_mount(self)` -- Find containers with the Docker socket mounted (escape vector).
- `DockerEnumerator.check_capabilities` (method) `modules/lazyk8s.py:217` `def check_capabilities(self)` -- Find containers with dangerous Linux capabilities.
- `DockerEnumerator.full_check` (method) `modules/lazyk8s.py:250` `def full_check(self)` -- Execute all Docker security checks and return aggregated results.
- `K8sEnumerator.__init__` (method) `modules/lazyk8s.py:267` `def __init__(self, kubeconfig, token, api_server)`
- `K8sEnumerator.list_pods` (method) `modules/lazyk8s.py:366` `def list_pods(self, namespace)` -- List pods in all namespaces or a specific namespace.
- `K8sEnumerator.list_namespaces` (method) `modules/lazyk8s.py:390` `def list_namespaces(self)` -- List all namespaces.
- `K8sEnumerator.list_secrets` (method) `modules/lazyk8s.py:410` `def list_secrets(self, namespace)` -- List secrets (without decoding values by default).
- `K8sEnumerator.list_service_accounts` (method) `modules/lazyk8s.py:462` `def list_service_accounts(self, namespace)` -- List service accounts and their attached roles.
- `K8sEnumerator.check_rbac` (method) `modules/lazyk8s.py:498` `def check_rbac(self)` -- Check current user's RBAC permissions.
- `K8sEnumerator.check_pod_escape_vectors` (method) `modules/lazyk8s.py:530` `def check_pod_escape_vectors(self)` -- Check for pod escape vectors in the current pod.
- `K8sEnumerator.full_check` (method) `modules/lazyk8s.py:582` `def full_check(self, sessions_dir)` -- Execute all Kubernetes security checks.
- `ContainerEscapeTechniques.detect_current_environment` (method) `modules/lazyk8s.py:684` `def detect_current_environment()` -- Detect if running inside a container and identify escape opportunities.
- `ContainerRuntimeDetector.detect_runtime` (method) `modules/lazyk8s.py:803` `def detect_runtime()` -- Detect container runtime from multiple indicators.
- `ContainerRuntimeDetector.detect_mounts` (method) `modules/lazyk8s.py:874` `def detect_mounts()` -- Detect dangerous mounts in the current container.
- `ContainerRuntimeDetector.detect_dangerous_capabilities` (method) `modules/lazyk8s.py:921` `def detect_dangerous_capabilities()` -- Detect dangerous Linux capabilities in the current container.
- `ContainerRuntimeDetector.auto_detect_all` (method) `modules/lazyk8s.py:992` `def auto_detect_all()` -- Run comprehensive container escape auto-detection.

## modules/lazylynis.sh
- `check_sudo` (function) `modules/lazylynis.sh:32` -- Función para verificar y relanzar con sudo si es necesario

## modules/lazymasscan.sh
- `ctrl_c` (function) `modules/lazymasscan.sh:20`
- `extract_ports_info` (function) `modules/lazymasscan.sh:74`
- `run_masscan_script` (function) `modules/lazymasscan.sh:94`
- `print_row` (function) `modules/lazymasscan.sh:117`

## modules/lazynmap.sh
- `cleanup` (function) `modules/lazynmap.sh:29`
- `ctrl_c` (function) `modules/lazynmap.sh:38`
- `fix_sessions_owner` (function) `modules/lazynmap.sh:74` -- Best-effort ownership fixup: scans run under sudo leave root-owned files behind, and only root can chown those.
- `nmaptest` (function) `modules/lazynmap.sh:129`
- `discover_network` (function) `modules/lazynmap.sh:149`
- `extract_ports_info` (function) `modules/lazynmap.sh:818`
- `run_nmap_script` (function) `modules/lazynmap.sh:844`
- `print_row` (function) `modules/lazynmap.sh:877`

## modules/lazyown_bprfuzzer.py
Depends on: `modules/backdoor/server.c`, `modules/security_sanitizers.py`
- `load_headers_from_file` (function) `modules/lazyown_bprfuzzer.py:93` `def load_headers_from_file(file_path)`
- `load_data_from_file` (function) `modules/lazyown_bprfuzzer.py:99` `def load_data_from_file(file_path)`
- `signal_handler` (function) `modules/lazyown_bprfuzzer.py:105` `def signal_handler(sig, frame)`
- `ProxyHandler.do_GET` (method) `modules/lazyown_bprfuzzer.py:115` `def do_GET(self)`
- `ProxyHandler.do_POST` (method) `modules/lazyown_bprfuzzer.py:118` `def do_POST(self)`
- `run_proxy` (function) `modules/lazyown_bprfuzzer.py:162` `def run_proxy(port)`
- `edit_file_with_nano` (function) `modules/lazyown_bprfuzzer.py:169` `def edit_file_with_nano(content)`
- `send_request` (function) `modules/lazyown_bprfuzzer.py:179` `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)` -- Envía una solicitud HTTP y devuelve la respuesta.
- `repeater` (function) `modules/lazyown_bprfuzzer.py:203` `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)` -- Funcionalidad de Repeater que permite enviar solicitudes múltiples veces con posibilidad de modificación.
- `lazyfuzz` (function) `modules/lazyown_bprfuzzer.py:233` `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)` -- Funcionalidad de fuzzing que reemplaza LAZYFUZZ con palabras de una wordlist.
- `parse_arguments` (function) `modules/lazyown_bprfuzzer.py:278` `def parse_arguments()` -- Parsear los argumentos de la línea de comandos.
- `main` (function) `modules/lazyown_bprfuzzer.py:302` `def main()`

## modules/lazyown_bridge.py
Depends on: `modules/killchain.py`
Imported by: `modules/unified_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_bridge_catalog_filtered.py`, `tests/test_core_modules.py`, `tests/test_exploitgym_gym.py`
- `CatalogEntry.build_command` (method) `modules/lazyown_bridge.py:63` `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)` -- Return 'command [args]' with known values substituted.
- `CatalogEntry.matches_service` (method) `modules/lazyown_bridge.py:94` `def matches_service(self, services)`
- `CatalogEntry.matches_os` (method) `modules/lazyown_bridge.py:104` `def matches_os(self, os_hint)`
- `CommandCatalog.__init__` (method) `modules/lazyown_bridge.py:118` `def __init__(self)`
- `CommandCatalog.by_phase` (method) `modules/lazyown_bridge.py:3946` `def by_phase(self, phase)`
- `CommandCatalog.by_mitre` (method) `modules/lazyown_bridge.py:3952` `def by_mitre(self, technique_id)`
- `CommandCatalog.by_service` (method) `modules/lazyown_bridge.py:3956` `def by_service(self, service_name)`
- `CommandCatalog.by_tag` (method) `modules/lazyown_bridge.py:3960` `def by_tag(self, tag)`
- `CommandCatalog.by_os` (method) `modules/lazyown_bridge.py:3963` `def by_os(self, os_hint)`
- `CommandCatalog.all_phases` (method) `modules/lazyown_bridge.py:3966` `def all_phases(self)`
- `CommandCatalog.get` (method) `modules/lazyown_bridge.py:3969` `def get(self, command)`
- `CommandCatalog.count` (method) `modules/lazyown_bridge.py:3975` `def count(self)`
- `AbstractSelector.select` (method) `modules/lazyown_bridge.py:3986` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `ServiceAwareSelector.select` (method) `modules/lazyown_bridge.py:4005` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `MitreAlignedSelector.__init__` (method) `modules/lazyown_bridge.py:4045` `def __init__(self, technique_id)`
- `MitreAlignedSelector.select` (method) `modules/lazyown_bridge.py:4049` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `TagSelector.__init__` (method) `modules/lazyown_bridge.py:4074` `def __init__(self, tag)`
- `TagSelector.select` (method) `modules/lazyown_bridge.py:4078` `def select(self, catalog, phase, services, has_creds, excluded, os_hint)`
- `ContextEnricher.enrich` (method) `modules/lazyown_bridge.py:4106` `def enrich(self, entry, target, world_snapshot)`
- `PhaseMapper.canonical_kill_chain_order` (method) `modules/lazyown_bridge.py:4204` `def canonical_kill_chain_order()` -- Return the canonical 8-phase order from KillChain (single source of truth).
- `PhaseMapper.to_bridge_phase` (method) `modules/lazyown_bridge.py:4210` `def to_bridge_phase(self, wm_phase)`
- `PhaseMapper.kill_chain_order` (method) `modules/lazyown_bridge.py:4223` `def kill_chain_order(self)` -- Ordered list of bridge phases following the kill chain.
- `BridgeDispatcher.__init__` (method) `modules/lazyown_bridge.py:4239` `def __init__(self, catalog, selector, enricher, phase_mapper)`
- `BridgeDispatcher.suggest` (method) `modules/lazyown_bridge.py:4251` `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)` -- Return (command_string, entry) or None.
- `BridgeDispatcher.suggest_sequence` (method) `modules/lazyown_bridge.py:4296` `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)` -- Return up to `limit` non-excluded suggestions for the phase.
- `BridgeDispatcher.suggest_for_wm_phase` (method) `modules/lazyown_bridge.py:4325` `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)`
- `BridgeDispatcher.list_phase` (method) `modules/lazyown_bridge.py:4343` `def list_phase(self, phase)`
- `BridgeDispatcher.all_phases` (method) `modules/lazyown_bridge.py:4347` `def all_phases(self)`
- `BridgeDispatcher.catalog_summary` (method) `modules/lazyown_bridge.py:4350` `def catalog_summary(self)`
- `BridgeDispatcher.catalog_summary_filtered` (method) `modules/lazyown_bridge.py:4358` `def catalog_summary_filtered(self, phase, os_hint)` -- Return a kill-chain summary restricted to a phase and target OS.
- `BridgeDispatcher.catalog_count` (method) `modules/lazyown_bridge.py:4395` `def catalog_count(self)`
- `BridgeDispatcher.phase_kill_chain` (method) `modules/lazyown_bridge.py:4398` `def phase_kill_chain(self)`
- `get_dispatcher` (function) `modules/lazyown_bridge.py:4409` `def get_dispatcher()`

## modules/lazyown_metaextract0r.py
- `signal_handler` (function) `modules/lazyown_metaextract0r.py:42` `def signal_handler(sig, frame)`
- `extract_pdf_metadata` (function) `modules/lazyown_metaextract0r.py:51` `def extract_pdf_metadata(file_path)`
- `extract_docx_metadata` (function) `modules/lazyown_metaextract0r.py:62` `def extract_docx_metadata(file_path)`
- `extract_ole_metadata` (function) `modules/lazyown_metaextract0r.py:73` `def extract_ole_metadata(file_path)`
- `extract_image_metadata` (function) `modules/lazyown_metaextract0r.py:85` `def extract_image_metadata(file_path)`
- `extract_metadata` (function) `modules/lazyown_metaextract0r.py:96` `def extract_metadata(file_path)`
- `find_and_extract_metadata` (function) `modules/lazyown_metaextract0r.py:109` `def find_and_extract_metadata(directory, output_file)`
- `parse_arguments` (function) `modules/lazyown_metaextract0r.py:130` `def parse_arguments()` -- Parse command-line arguments.
- `main` (function) `modules/lazyown_metaextract0r.py:140` `def main()`

## modules/lazyown_parquet_tool.py
- `highlight_term` (function) `modules/lazyown_parquet_tool.py:34` `def highlight_term(text, term)` -- Highlight the search term in the given text.
- `search_in_parquet` (function) `modules/lazyown_parquet_tool.py:39` `def search_in_parquet(term, parquet_files)` -- Search for a term in the given Parquet files and return matching rows.
- `buscar_binarios` (function) `modules/lazyown_parquet_tool.py:53` `def buscar_binarios(args)` -- Search for binaries with special permissions and generate a results CSV.
- `ejecutar_opciones` (function) `modules/lazyown_parquet_tool.py:136` `def ejecutar_opciones()` -- Execute options based on the found data.

## modules/lazyownclient.py
- `signal_handler` (function) `modules/lazyownclient.py:34` `def signal_handler(sig, frame)`
- `pad` (function) `modules/lazyownclient.py:51` `def pad(s)`
- `encrypt` (function) `modules/lazyownclient.py:55` `def encrypt(plaintext, key)`
- `decrypt` (function) `modules/lazyownclient.py:62` `def decrypt(ciphertext, key)`
- `handle_command` (function) `modules/lazyownclient.py:69` `def handle_command(cmd, key)`
- `main` (function) `modules/lazyownclient.py:198` `def main()`

## modules/lazyownerweb.py
Depends on: `core/logging.py`, `modules/logging_config.py`
- `send_request` (function) `modules/lazyownerweb.py:36` `def send_request(url, params, method)`
- `test_injection` (function) `modules/lazyownerweb.py:49` `def test_injection(url, payloads, param_name, detection_strings, method)`
- `main` (function) `modules/lazyownerweb.py:59` `def main()`

## modules/lazyownserver.py
- `signal_handler` (function) `modules/lazyownserver.py:34` `def signal_handler(sig, frame)`
- `pad` (function) `modules/lazyownserver.py:42` `def pad(s)`
- `encrypt` (function) `modules/lazyownserver.py:46` `def encrypt(plaintext, key)`
- `decrypt` (function) `modules/lazyownserver.py:53` `def decrypt(ciphertext, key)`
- `handle_client` (function) `modules/lazyownserver.py:60` `def handle_client(conn, addr, key)`
- `main` (function) `modules/lazyownserver.py:97` `def main()`

## modules/lazypsexec.sh
- `execute_psexec` (function) `modules/lazypsexec.sh:15` -- Función para ejecutar psexec y verificar la salida

## modules/lazyreverse_shell.sh
- `mostrar_ayuda` (function) `modules/lazyreverse_shell.sh:21` -- Función para mostrar ayuda
- `validar_ip` (function) `modules/lazyreverse_shell.sh:31` -- Validar dirección IP

## modules/lazyvpnshield.sh
- `ctrl_c` (function) `modules/lazyvpnshield.sh:11`
- `check_sudo` (function) `modules/lazyvpnshield.sh:16`
- `save_current_rules` (function) `modules/lazyvpnshield.sh:29`
- `show_current_rules` (function) `modules/lazyvpnshield.sh:37`
- `apply_vpn_rules` (function) `modules/lazyvpnshield.sh:45`
- `undo_and_restore_rules` (function) `modules/lazyvpnshield.sh:86`
- `main` (function) `modules/lazyvpnshield.sh:113`

## modules/lazywps.sh
- `ctrl_c` (function) `modules/lazywps.sh:9`

## modules/lesson_ingestor.py
Depends on: `core/logging.py`, `modules/moe_router.py`, `modules/rl_trainer.py`
Imported by: `skills/lazyown_campaign.py`, `tests/test_lesson_ingestor.py`
- `LessonLearned.from_dict` (method) `modules/lesson_ingestor.py:66` `def from_dict(cls, d)`
- `LessonIngestor.__init__` (method) `modules/lesson_ingestor.py:86` `def __init__(self, lessons_file, router, trainer, boost_reward)`
- `LessonIngestor.ingest` (method) `modules/lesson_ingestor.py:125` `def ingest(self, lesson)` -- Apply a single lesson to the MoE performance store and RL Q-table.
- `LessonIngestor.ingest_all` (method) `modules/lesson_ingestor.py:185` `def ingest_all(self, lessons)` -- Ingest a batch of lessons.
- `ingest_campaign_lessons` (function) `modules/lesson_ingestor.py:222` `def ingest_campaign_lessons(lessons_file)` -- Module-level convenience function to ingest all campaign lessons.

## modules/lilsplunky.py
Depends on: `core/console.py`, `core/logging.py`, `modules/logging_config.py`
- `simple_parse_log_line` (function) `modules/lilsplunky.py:69` `def simple_parse_log_line(line, file_path)` -- Intenta extraer información básica de una línea de log.
- `store_event` (function) `modules/lilsplunky.py:108` `def store_event(event_data)` -- Almacena el evento procesado (diccionario Python) como una línea JSON en el archivo de salida.
- `analyze_with_deepseek` (function) `modules/lilsplunky.py:123` `def analyze_with_deepseek(log_entry_data)` -- Sends a single log entry to DeepSeek for analysis.
- `LogFileHandler.__init__` (method) `modules/lilsplunky.py:223` `def __init__(self, log_dir, mode)`
- `LogFileHandler.initialize_file_positions` (method) `modules/lilsplunky.py:229` `def initialize_file_positions(self)` -- Set initial position to the end of all currently monitored files.
- `LogFileHandler.is_monitored` (method) `modules/lilsplunky.py:245` `def is_monitored(self, file_path)` -- Check if the file path matches any of the monitored patterns.
- `LogFileHandler.process_file` (method) `modules/lilsplunky.py:257` `def process_file(self, file_path)` -- Reads new lines from a file since the last known position.
- `LogFileHandler.on_modified` (method) `modules/lilsplunky.py:331` `def on_modified(self, event)` -- Triggered when a file or directory is modified.
- `LogFileHandler.on_created` (method) `modules/lilsplunky.py:336` `def on_created(self, event)` -- Triggered when a file or directory is created.
- `display_record` (function) `modules/lilsplunky.py:346` `def display_record(record)` -- Muestra un registro procesado de forma atractiva en la consola.
- `search_logs` (function) `modules/lilsplunky.py:382` `def search_logs(query, file_path)` -- Busca en el archivo de eventos JSONL registros que coincidan (búsqueda simple de substring).
- `start_monitoring` (function) `modules/lilsplunky.py:413` `def start_monitoring(log_dir, mode)` -- Starts monitoring the specified log directory.
- `parse_args` (function) `modules/lilsplunky.py:446` `def parse_args()`

## modules/linux_advanced_payloads.py
Imported by: `cli/commands/payload_arsenal.py`
- `LinuxAdvancedPayloadFactory.__init__` (method) `modules/linux_advanced_payloads.py:105` `def __init__(self, config, output_dir)`
- `LinuxAdvancedPayloadFactory.generate_ld_preload_rootkit` (method) `modules/linux_advanced_payloads.py:110` `def generate_ld_preload_rootkit(self)` -- Generate a C source file for an LD_PRELOAD rootkit.
- `LinuxAdvancedPayloadFactory.generate_ebpf_payload` (method) `modules/linux_advanced_payloads.py:235` `def generate_ebpf_payload(self)` -- Generate an eBPF C program for network manipulation.
- `LinuxAdvancedPayloadFactory.generate_pam_backdoor` (method) `modules/linux_advanced_payloads.py:311` `def generate_pam_backdoor(self)` -- Generate a PAM (Pluggable Authentication Module) backdoor.
- `LinuxAdvancedPayloadFactory.generate_systemd_persistence` (method) `modules/linux_advanced_payloads.py:398` `def generate_systemd_persistence(self)` -- Generate systemd service and timer units for persistent callbacks.
- `LinuxAdvancedPayloadFactory.generate_ssh_persistence` (method) `modules/linux_advanced_payloads.py:458` `def generate_ssh_persistence(self)` -- Generate an SSH persistence script for authorized_keys injection.
- `LinuxAdvancedPayloadFactory.generate_kernel_module` (method) `modules/linux_advanced_payloads.py:519` `def generate_kernel_module(self)` -- Generate a Linux kernel module (LKM) rootkit.
- `LinuxAdvancedPayloadFactory.generate_process_masquerade` (method) `modules/linux_advanced_payloads.py:632` `def generate_process_masquerade(self)` -- Generate a process masquerading script.
- `LinuxAdvancedPayloadFactory.generate_udev_persistence` (method) `modules/linux_advanced_payloads.py:676` `def generate_udev_persistence(self)` -- Generate a udev rule for persistence on USB/device events.
- `LinuxAdvancedPayloadFactory.generate_motd_backdoor` (method) `modules/linux_advanced_payloads.py:689` `def generate_motd_backdoor(self)` -- Generate a Message of the Day (motd) hook for persistence.
- `LinuxAdvancedPayloadFactory.compile_c_source` (method) `modules/linux_advanced_payloads.py:707` `def compile_c_source(self, source, output_name, shared)` -- Compile C source code to a binary or shared library.
- `LinuxAdvancedPayloadFactory.generate_all` (method) `modules/linux_advanced_payloads.py:749` `def generate_all(self)` -- Generate all Linux advanced payload artifacts.
- `LinuxAdvancedPayloadFactory.list_hook_functions` (method) `modules/linux_advanced_payloads.py:793` `def list_hook_functions()`
- `LinuxAdvancedPayloadFactory.list_persistence_methods` (method) `modules/linux_advanced_payloads.py:797` `def list_persistence_methods()`

## modules/listener_manager.py
Depends on: `utils.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `lazyc2.py`
- `Listener.to_dict` (method) `modules/listener_manager.py:152` `def to_dict(self)`
- `Listener.from_dict` (method) `modules/listener_manager.py:162` `def from_dict(cls, data)`
- `ListenerManager.__init__` (method) `modules/listener_manager.py:179` `def __init__(self, app, sessions_dir, payload)`
- `ListenerManager.set_payload` (method) `modules/listener_manager.py:187` `def set_payload(self, payload)` -- Update the payload mapping used to resolve the bind address.
- `ListenerManager.add` (method) `modules/listener_manager.py:229` `def add(self, port, ssl, listener_id)` -- Register a new listener configuration (does not start it).
- `ListenerManager.remove` (method) `modules/listener_manager.py:242` `def remove(self, listener_id)` -- Remove a listener configuration.
- `ListenerManager.start` (method) `modules/listener_manager.py:255` `def start(self, listener_id)` -- Start a single listener.
- `ListenerManager.stop` (method) `modules/listener_manager.py:323` `def stop(self, listener_id)` -- Stop a single listener.
- `ListenerManager.start_all` (method) `modules/listener_manager.py:344` `def start_all(self)` -- Start every listener marked as active.
- `ListenerManager.stop_all` (method) `modules/listener_manager.py:350` `def stop_all(self)` -- Stop every running listener.
- `ListenerManager.status` (method) `modules/listener_manager.py:355` `def status(self)` -- Return status of all listeners.
- `ListenerManager.get_default_port` (method) `modules/listener_manager.py:367` `def get_default_port(self, fallback)` -- Return the port of the first active listener, or fallback.

## modules/live_surface.py
Depends on: `modules/world_model.py`
Imported by: `lazyc2.py`, `modules/unified_dashboard.py`, `tests/test_live_surface.py`
- `build_live_graph` (function) `modules/live_surface.py:72` `def build_live_graph(world)` -- Build a live vis-network payload from a world-model snapshot.

## modules/llm_adapter.py
Depends on: `contrib/legacy/lazydeepseekcli.py`, `contrib/legacy/lazyphishingai.py`, `core/logging.py`, `modules/llm_factory.py`, `modules/llm_prompts.py`
Imported by: `cli/commands/ai.py`, `discord_c2.py`, `lazyc2.py`, `slack_c2_bot.py`, `telegram_c2.py`, `tests/test_llm_adapter_parity.py`
- `safe_groq_client` (function) `modules/llm_adapter.py:48` `def safe_groq_client(api_key)` -- Create a Groq client, returning None when no key is provided.
- `process_prompt` (function) `modules/llm_adapter.py:119` `def process_prompt(client, prompt, debug)` -- Generate a single-line shell command from a user prompt.
- `process_prompt_script` (function) `modules/llm_adapter.py:133` `def process_prompt_script(client, prompt, debug)` -- Generate a full script from a user prompt.
- `process_prompt_adversary` (function) `modules/llm_adapter.py:147` `def process_prompt_adversary(client, prompt, debug)` -- Answer questions about MITRE ATT&CK techniques and Atomic Red Team.
- `process_prompt_general` (function) `modules/llm_adapter.py:161` `def process_prompt_general(client, prompt, debug)` -- Answer as a general red-team assistant with payload.json context.
- `process_prompt_search` (function) `modules/llm_adapter.py:175` `def process_prompt_search(client, prompt, debug)` -- Perform research and threat-intelligence analysis.
- `process_prompt_task` (function) `modules/llm_adapter.py:189` `def process_prompt_task(client, prompt, debug)` -- Analyze a task-assessment JSON file for completion status.
- `process_prompt_vuln` (function) `modules/llm_adapter.py:206` `def process_prompt_vuln(client, prompt, debug, event)` -- Analyze Nmap output for vulnerabilities and propose an action plan.
- `process_prompt_redop` (function) `modules/llm_adapter.py:237` `def process_prompt_redop(client, prompt, debug)` -- Evaluate a red-team operation status from a JSON database file.
- `ask_general` (function) `modules/llm_adapter.py:254` `def ask_general(prompt, debug)` -- Answer through the configured LLM backend, regardless of provider.

## modules/llm_client.py
Depends on: `core/logging.py`, `modules/ai_model.py`
Imported by: `contrib/legacy/lazyaddon_creator.py`, `modules/llm_factory.py`, `modules/planner.py`, `modules/playbook_engine.py`, `skills/lazyown_mcp.py`
- `LLMClient.__init__` (method) `modules/llm_client.py:63` `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)`
- `LLMClient.ask` (method) `modules/llm_client.py:79` `def ask(self, prompt)` -- Send a prompt and return the text response.
- `LLMClient.classify` (method) `modules/llm_client.py:130` `def classify(self, output)` -- Short classification prompt.
- `LLMClient.summarize` (method) `modules/llm_client.py:159` `def summarize(self, text)` -- Summarize a block of text (e.g. nmap output, tool output).
- `get_client` (function) `modules/llm_client.py:268` `def get_client(api_key)` -- Return (or create) the module-level singleton LLMClient.
- `ask` (function) `modules/llm_client.py:276` `def ask(prompt)` -- Module-level convenience wrapper.
- `classify` (function) `modules/llm_client.py:288` `def classify(output)` -- Module-level convenience wrapper.
- `summarize` (function) `modules/llm_client.py:293` `def summarize(text)` -- Module-level convenience wrapper.

## modules/llm_evaluator.py
Imported by: `skills/lazyown_mcp.py`, `tests/test_core_modules.py`
- `OutcomeRecorder.record` (method) `modules/llm_evaluator.py:57` `def record(self, decision)`
- `OutcomeRecorder.update_outcome` (method) `modules/llm_evaluator.py:60` `def update_outcome(self, decision_id, actual, findings_count, success)`
- `OutcomeRecorder.load_all` (method) `modules/llm_evaluator.py:69` `def load_all(self)`
- `OutcomeRecorder.load_by_session` (method) `modules/llm_evaluator.py:72` `def load_by_session(self, session_id)`
- `JSONLRecorder.__init__` (method) `modules/llm_evaluator.py:76` `def __init__(self, path)`
- `JSONLRecorder.record` (method) `modules/llm_evaluator.py:81` `def record(self, decision)`
- `JSONLRecorder.update_outcome` (method) `modules/llm_evaluator.py:86` `def update_outcome(self, decision_id, actual, findings_count, success)`
- `JSONLRecorder.load_all` (method) `modules/llm_evaluator.py:120` `def load_all(self)`
- `JSONLRecorder.load_by_session` (method) `modules/llm_evaluator.py:135` `def load_by_session(self, session_id)`
- `LLMEvaluator.__init__` (method) `modules/llm_evaluator.py:162` `def __init__(self, recorder)`
- `LLMEvaluator.record_decision` (method) `modules/llm_evaluator.py:165` `def record_decision(self, session_id, thought, action, mitre_tactic, expected_outcome, confidence)`
- `LLMEvaluator.record_outcome` (method) `modules/llm_evaluator.py:191` `def record_outcome(self, decision_id, actual_outcome, findings_count, success)`
- `LLMEvaluator.compute_metrics` (method) `modules/llm_evaluator.py:200` `def compute_metrics(self, session_id)`
- `LLMEvaluator.quality_report` (method) `modules/llm_evaluator.py:241` `def quality_report(self, session_id)`
- `LLMEvaluator.export_finetuning_dataset` (method) `modules/llm_evaluator.py:256` `def export_finetuning_dataset(self, path)`
- `get_evaluator` (function) `modules/llm_evaluator.py:293` `def get_evaluator()`
- `record_decision` (function) `modules/llm_evaluator.py:302` `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)`
- `record_outcome` (function) `modules/llm_evaluator.py:313` `def record_outcome(decision_id, actual_outcome, findings_count, success)`

## modules/llm_factory.py
Depends on: `core/llm_budget.py`, `modules/ai_model.py`, `modules/llm_client.py`, `modules/toposwarm_bridge.py`
Imported by: `cli/commands/ai.py`, `cli/wizard.py`, `contrib/legacy/lazyllmchat.py`, `core/payload_schema.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ai_fallback.py`, `modules/ai_model.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/llm_adapter.py`, `modules/mcp_agent_bridge.py`, `modules/privesc_predictor.py`, `modules/professional_report.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`, `skills/claude_md_orchestrator/sdd_agent.py`, `tests/conftest.py`, `tests/test_ai_commands_llm.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_streaming.py`, `tests/test_llm_adapter_parity.py`, `tests/test_loop_ai_bridge.py`, `tests/test_loop_llm_resilience.py`, `tests/test_payload_schema.py`, `tests/test_wizard_llm.py`
- `is_model_missing_error` (function) `modules/llm_factory.py:121` `def is_model_missing_error(message)` -- Return True when an error text means the model id is unavailable.
- `groq_model_chain` (function) `modules/llm_factory.py:141` `def groq_model_chain(config)` -- Return the ordered Groq model ids to try, configured model first.
- `default_model_for` (function) `modules/llm_factory.py:224` `def default_model_for(backend)` -- Return the default model identifier for a backend.
- `model_config_key` (function) `modules/llm_factory.py:245` `def model_config_key(backend)` -- Return the ``payload.json`` key holding a backend's model override.
- `api_key_config_key` (function) `modules/llm_factory.py:266` `def api_key_config_key(backend)` -- Return the ``payload.json`` key holding a backend's API key slot.
- `backend_requires_api_key` (function) `modules/llm_factory.py:291` `def backend_requires_api_key(backend)` -- Report whether a backend needs an API key to operate.
- `load_payload` (function) `modules/llm_factory.py:309` `def load_payload(payload_path)` -- Read ``payload.json`` from disk and return it as a dictionary.
- `get_llm_backend` (function) `modules/llm_factory.py:591` `def get_llm_backend(config, backend)` -- Return a concrete :class:`AIModel` selected by configuration.
- `get_llm_backend_raw` (function) `modules/llm_factory.py:679` `def get_llm_backend_raw(config, backend)` -- Return a raw :class:`AIModel` without the budget wrapper.
- `try_get_llm_backend` (function) `modules/llm_factory.py:701` `def try_get_llm_backend(config, backend)` -- Return a backend or ``None`` if construction fails for any reason.
- `stream_complete` (function) `modules/llm_factory.py:778` `def stream_complete(model, prompt, max_tokens, on_delta)` -- Completion that reports incremental deltas while it arrives.
- `complete` (function) `modules/llm_factory.py:849` `def complete(model, prompt, max_tokens)` -- Complete a prompt through one model spec; raise when unanswered.

## modules/llm_pool.py
Imported by: `cli/commands/ai.py`, `modules/lazy_loop.py`, `skills/autonomous_daemon.py`, `skills/lazyown_mcp.py`, `tests/conftest.py`, `tests/test_autonomous_ops.py`, `tests/test_lazy_parity.py`, `tests/test_lazy_runner.py`
- `shared_registry` (function) `modules/llm_pool.py:50` `def shared_registry(config)` -- Return the process-wide health registry (LAZY Registry parity).
- `HealthRegistry.__init__` (method) `modules/llm_pool.py:83` `def __init__(self, config)` -- Initialize counters from the persisted breaker state.
- `HealthRegistry.report_success` (method) `modules/llm_pool.py:135` `def report_success(self, member_id)` -- Clear failure state for a member.
- `HealthRegistry.report_failure` (method) `modules/llm_pool.py:143` `def report_failure(self, member_id, error)` -- Record a failure; auth/quota errors trip immediately.
- `HealthRegistry.healthy` (method) `modules/llm_pool.py:163` `def healthy(self, member_id)` -- Return True when a member may serve traffic.
- `LLMPool.__init__` (method) `modules/llm_pool.py:179` `def __init__(self, members, health, config)` -- Order members by descending rank (RR within equal rank).
- `LLMPool.members` (method) `modules/llm_pool.py:192` `def members(self)` -- Return chain members in order.
- `LLMPool.session_key` (method) `modules/llm_pool.py:196` `def session_key(self, conversation_id, role, index)` -- Build a sticky session header (LAZY session_header parity).
- `LLMPool.complete` (method) `modules/llm_pool.py:237` `def complete(self, prompt, max_tokens, session_key, overflow_dir)` -- Complete a prompt with pre-token failover across members.

## modules/llm_prompts.py
Depends on: `modules/colors.py`
Imported by: `cli/commands/ai.py`, `modules/llm_adapter.py`, `tests/test_llm_adapter_parity.py`, `tests/test_llm_prompts.py`
- `default_project_root` (function) `modules/llm_prompts.py:67` `def default_project_root()` -- Return the repository root that owns the LLM prompt configuration.
- `resolve_model` (function) `modules/llm_prompts.py:76` `def resolve_model(model)` -- Resolve an explicit model or fall back to the randomized Groq model.
- `truncate_message` (function) `modules/llm_prompts.py:95` `def truncate_message(message, max_chars)` -- Truncate a message with an ellipsis marker when it exceeds the limit.
- `LlmPromptConfig.from_defaults` (method) `modules/llm_prompts.py:130` `def from_defaults(cls, project_root)` -- Build a config rooted at the given project root.
- `LlmPromptConfig.knowledge_base_path` (method) `modules/llm_prompts.py:150` `def knowledge_base_path(self, domain)` -- Return the absolute path for a knowledge-base domain file.
- `LlmPromptConfig.load_payload_context` (method) `modules/llm_prompts.py:161` `def load_payload_context(self)` -- Load the operator context keyed by :data:`PAYLOAD_KEY_ORDER`.
- `LlmPromptConfig.load_event_tool_output` (method) `modules/llm_prompts.py:176` `def load_event_tool_output(self, event_name)` -- Load tool output attached to a named event in event_config.json.
- `LlmPromptConfig.load_plan_history` (method) `modules/llm_prompts.py:203` `def load_plan_history(self)` -- Load the session plan history text if present.
- `LlmPromptConfig.load_report_context` (method) `modules/llm_prompts.py:218` `def load_report_context(self)` -- Load the JSON artefacts consumed by the report template.
- `LlmPromptConfig.knowledge_store` (method) `modules/llm_prompts.py:238` `def knowledge_store(self, domain)` -- Build a knowledge store bound to a domain file.
- `LlmPromptConfig.render` (method) `modules/llm_prompts.py:249` `def render(self, template, base_prompt)` -- Render a named template with shared knowledge and context.
- `render_kb_tail` (function) `modules/llm_prompts.py:271` `def render_kb_tail(lines)` -- Join the most recent knowledge lines for embedding into a prompt.
- `KnowledgeStore.__init__` (method) `modules/llm_prompts.py:289` `def __init__(self, path)` -- Initialize a store bound to a single JSON file.
- `KnowledgeStore.load` (method) `modules/llm_prompts.py:297` `def load(self)` -- Load the knowledge-base records from disk.
- `KnowledgeStore.save` (method) `modules/llm_prompts.py:312` `def save(self, records)` -- Persist a full record list to disk, creating parent directories.
- `KnowledgeStore.add` (method) `modules/llm_prompts.py:324` `def add(self, prompt, response)` -- Append a prompt/response record to the knowledge base.
- `KnowledgeStore.relevant` (method) `modules/llm_prompts.py:335` `def relevant(self, prompt, limit)` -- Return knowledge responses whose text shares keywords with the prompt.

## modules/log_tamper.py
Imported by: `cli/commands/opsec_cleanup.py`
- `LogTamper.__init__` (method) `modules/log_tamper.py:105` `def __init__(self, config)`
- `LogTamper.windows_clear_commands` (method) `modules/log_tamper.py:108` `def windows_clear_commands(self)` -- Generate Windows Event Log clearing commands.
- `LogTamper.linux_clear_commands` (method) `modules/log_tamper.py:176` `def linux_clear_commands(self)` -- Generate Linux log clearing commands.
- `LogTamper.macos_clear_commands` (method) `modules/log_tamper.py:243` `def macos_clear_commands(self)` -- Generate macOS log clearing commands.
- `LogTamper.generate_all` (method) `modules/log_tamper.py:295` `def generate_all(self)` -- Generate log tampering commands for all platforms.
- `LogTamper.auditd_disable_commands` (method) `modules/log_tamper.py:307` `def auditd_disable_commands(self)` -- Commands to temporarily disable or reconfigure auditd on Linux.
- `LogTamper.sysmon_disable_commands` (method) `modules/log_tamper.py:341` `def sysmon_disable_commands(self)` -- Commands to disable or degrade Sysmon on Windows.

## modules/logging_config.py
Depends on: `core/logging.py`
Imported by: `lazy_sentinel4.py`, `lazyc2.py`, `lazyown.py`, `modules/agent_runner.py`, `modules/ia_code_analysis.py`, `modules/ia_logs_analysis.py`, `modules/ia_network_analysis.py`, `modules/icmp_server.py`, `modules/lazyownerweb.py`, `modules/lilsplunky.py`, `modules/vulnbot.py`, `skills/aci_planner.py`, `skills/autonomous_daemon.py`, `skills/hive_mind.py`, `skills/lazyown_campaign.py`, `skills/lazyown_daemon.py`, `skills/lazyown_facts.py`, `skills/lazyown_llm.py`, `skills/lazyown_policy.py`, `skills/sessions_watcher.py`, `skills/swan_agent.py`, `skills/toposwarm_autonomous.py`, `skills/update_knowledge.py`, `tests/test_logging_config.py`
- `ColoredFormatter.format` (method) `modules/logging_config.py:39` `def format(self, record)`
- `JsonFormatter.format` (method) `modules/logging_config.py:72` `def format(self, record)`
- `CorrelationFilter.filter` (method) `modules/logging_config.py:94` `def filter(self, record)`
- `ResilientRotatingFileHandler.emit` (method) `modules/logging_config.py:116` `def emit(self, record)` -- Write one record, no-op after the file has become unwritable.
- `ResilientRotatingFileHandler.handleError` (method) `modules/logging_config.py:122` `def handleError(self, record)` -- Suppress the default per-record traceback; notify once via stderr.
- `set_correlation_id` (function) `modules/logging_config.py:134` `def set_correlation_id(cid)` -- Set the correlation ID for the current async/task context.
- `get_correlation_id` (function) `modules/logging_config.py:139` `def get_correlation_id()` -- Return the current correlation ID, or None.
- `clear_correlation_id` (function) `modules/logging_config.py:144` `def clear_correlation_id()` -- Reset the correlation ID for the current context.
- `configure` (function) `modules/logging_config.py:244` `def configure(level, log_dir, console, file, format_console, format_file, max_bytes, backup_count, module_levels)` -- Configure LazyOwn's centralized logging system.
- `get_logger` (function) `modules/logging_config.py:328` `def get_logger(name, level)` -- Get a logger with the given name.
- `set_level` (function) `modules/logging_config.py:357` `def set_level(name, level)` -- Set the log level for a specific logger.
- `set_quiet` (function) `modules/logging_config.py:367` `def set_quiet()` -- Silence all logging below WARNING level.
- `set_verbose` (function) `modules/logging_config.py:373` `def set_verbose()` -- Enable DEBUG level logging.
- `silence_module` (function) `modules/logging_config.py:379` `def silence_module(name)` -- Completely silence a noisy module.
- `reset` (function) `modules/logging_config.py:388` `def reset()` -- Reset the logging system to defaults.

## modules/loop_ai_bridge.py
Depends on: `modules/detection_oracle.py`, `modules/event_bus.py`, `modules/moe_router.py`, `modules/orchestrator_config.py`, `modules/rl_trainer.py`, `skills/hive_mind.py`, `skills/swan_agent.py`
Imported by: `modules/lazy_agent.py`, `modules/lazy_loop.py`, `tests/conftest.py`, `tests/test_lazy_streaming.py`, `tests/test_loop_ai_bridge.py`
- `publish_loop_event` (function) `modules/loop_ai_bridge.py:74` `def publish_loop_event(task_id, worker, kind, text, severity)` -- Publish one loop activity to the unified bus and Hive memory.
- `annotate_detection` (function) `modules/loop_ai_bridge.py:125` `def annotate_detection(command, action_category)` -- Return oracle details for one command, or None when unavailable.
- `moe_route` (function) `modules/loop_ai_bridge.py:149` `def moe_route(task_type, goal)` -- Return the MoE router's preferred expert for a task type, or None.
- `moe_record_outcome` (function) `modules/loop_ai_bridge.py:166` `def moe_record_outcome(expert_id, task_type, reward, detection_prob)` -- Feed one execution outcome back to the MoE performance store.
- `rl_select` (function) `modules/loop_ai_bridge.py:185` `def rl_select(task_type, phase, candidates, deterministic)` -- Pick an expert with the RL policy; first candidate when unavailable.
- `rl_update` (function) `modules/loop_ai_bridge.py:207` `def rl_update(task_type, phase, action, reward, candidates, detection_prob)` -- Apply one Q-learning update for an executed action.
- `rl_save` (function) `modules/loop_ai_bridge.py:230` `def rl_save()` -- Persist the RL tables after a run.
- `record_step` (function) `modules/loop_ai_bridge.py:249` `def record_step(task_id, worker, command, output, detection_prob)` -- Feed one executed command outcome to MoE and the RL trainer.
- `swan_available` (function) `modules/loop_ai_bridge.py:264` `def swan_available()` -- Return True when the SWAN orchestrator can be constructed.
- `swan_consult` (function) `modules/loop_ai_bridge.py:277` `def swan_consult(prompt, task_type, phase, timeout)` -- Ask SWAN for an ensemble answer; empty string when unavailable.
- `stream_enabled` (function) `modules/loop_ai_bridge.py:304` `def stream_enabled()` -- Return whether token streaming into the activity log is enabled.
- `ai_snapshot` (function) `modules/loop_ai_bridge.py:314` `def ai_snapshot()` -- Compact status of the wired AI stack for the operator log.

## modules/loop_guardrails.py
Imported by: `modules/lazy_loop.py`, `modules/lazy_runner.py`, `tests/test_loop_guardrails.py`
- `RepeatDetector.__init__` (method) `modules/loop_guardrails.py:89` `def __init__(self, window)`
- `RepeatDetector.record` (method) `modules/loop_guardrails.py:93` `def record(self, command)` -- Add one executed command; returns True when the window fills.
- `RepeatDetector.stuck` (method) `modules/loop_guardrails.py:110` `def stuck(self)` -- True when the window is full of one identical command.
- `RepeatDetector.last_commands` (method) `modules/loop_guardrails.py:117` `def last_commands(self)` -- Snapshot of the recent command window (oldest first).
- `RepeatDetector.reset` (method) `modules/loop_guardrails.py:121` `def reset(self)` -- Clear the window (operator intervention acknowledged).
- `EdrPacer.__init__` (method) `modules/loop_guardrails.py:135` `def __init__(self, duration_threshold)`
- `EdrPacer.observe` (method) `modules/loop_guardrails.py:141` `def observe(self, command, duration_sec, output)` -- Feed one executed step and update the telemetry estimate.
- `EdrPacer.decay` (method) `modules/loop_guardrails.py:163` `def decay(self, factor)` -- Cool the estimate down (call once per completed step).
- `EdrPacer.level` (method) `modules/loop_guardrails.py:169` `def level(self)` -- Current pacing level: 0 calm, 1 cautious, 2 stealth.
- `EdrPacer.signal` (method) `modules/loop_guardrails.py:179` `def signal(self)` -- Human-readable reason for the current level (may be empty).
- `EdrPacer.inter_step_delay` (method) `modules/loop_guardrails.py:184` `def inter_step_delay(self)` -- Recommended sleep before the next step at the current level.
- `EdrPacer.quieten` (method) `modules/loop_guardrails.py:192` `def quieten(self, command)` -- Return a quieter variant of the command at the current level.
- `TargetLimiter.__init__` (method) `modules/loop_guardrails.py:216` `def __init__(self, max_concurrent)`
- `TargetLimiter.max_concurrent` (method) `modules/loop_guardrails.py:223` `def max_concurrent(self)` -- Configured upper bound of simultaneous targets.
- `TargetLimiter.active_targets` (method) `modules/loop_guardrails.py:228` `def active_targets(self)` -- How many distinct targets currently hold a slot.
- `TargetLimiter.slot` (method) `modules/loop_guardrails.py:234` `def slot(self, target)` -- Hold one of at most ``max_concurrent`` target slots.
- `FactVectorStore.__init__` (method) `modules/loop_guardrails.py:286` `def __init__(self, path, max_facts)`
- `FactVectorStore.path` (method) `modules/loop_guardrails.py:294` `def path(self)` -- Backing file path.
- `FactVectorStore.add` (method) `modules/loop_guardrails.py:315` `def add(self, text, meta)` -- Embed and store one fact; returns False for duplicates.
- `FactVectorStore.search` (method) `modules/loop_guardrails.py:349` `def search(self, query, k)` -- Return the ``k`` facts most similar to the query.
- `FactVectorStore.search_block` (method) `modules/loop_guardrails.py:379` `def search_block(self, query, k, max_chars)` -- Render retrieved facts as a prompt-ready block (may be empty).
- `FactVectorStore.clear` (method) `modules/loop_guardrails.py:388` `def clear(self)` -- Drop every fact (manual reset path).
- `FactVectorStore.save` (method) `modules/loop_guardrails.py:394` `def save(self)` -- Persist atomically; I/O errors never surface to the loop.

## modules/loop_progress.py
Depends on: `core/safe_console.py`
Imported by: `cli/lazy_monitor.py`, `modules/lazy_runner.py`, `tests/test_lazy_runner.py`, `tests/test_loop_progress.py`
- `snapshot_from_overview` (function) `modules/loop_progress.py:99` `def snapshot_from_overview(overview, record, activity_tail, elapsed_sec)` -- Build a snapshot from a graph overview dict plus task record.
- `snap_to_states` (function) `modules/loop_progress.py:123` `def snap_to_states(snapshot)` -- Infer done/active/pending per chain stage from a snapshot.
- `sanitize_line` (function) `modules/loop_progress.py:151` `def sanitize_line(line, keep_ansi)` -- Strip ANSI codes and carriage returns from a transcript line.
- `LoopProgress.live_mode` (method) `modules/loop_progress.py:195` `def live_mode(self)` -- True only when the sink supports a real live region.
- `LoopProgress.start` (method) `modules/loop_progress.py:202` `def start(self)` -- Open the Live display, or print the header in line mode.
- `LoopProgress.stop` (method) `modules/loop_progress.py:229` `def stop(self)` -- Freeze the final panel on screen (both modes).
- `LoopProgress.refresh` (method) `modules/loop_progress.py:246` `def refresh(self, snapshot)` -- Re-render milestones from a fresh snapshot (thread-safe).
- `LoopProgress.emit` (method) `modules/loop_progress.py:268` `def emit(self, line)` -- Print a transcript line above the live panel, colors preserved.

## modules/loop_triggers.py
Depends on: `modules/auto_registry.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`
Imported by: `cli/orchestrator_assets_tabs.py`, `lazyc2/blueprints/orchestrator.py`, `modules/lazy_loop.py`, `modules/trigger_policy.py`, `tests/test_orchestrator_triggers.py`, `tests/test_trigger_policy.py`
- `TriggerStore.__init__` (method) `modules/loop_triggers.py:26` `def __init__(self, task_id)` -- Bind trigger table (global when task_id empty).
- `TriggerStore.add` (method) `modules/loop_triggers.py:36` `def add(self, kind, arg, every_sec)` -- Register a trigger; interval needs every_sec, events fire on new rows.
- `TriggerStore.upsert_defaults` (method) `modules/loop_triggers.py:58` `def upsert_defaults(self, seeds)` -- Merge declarative seeds without duplicating or re-enabling.
- `TriggerStore.remove` (method) `modules/loop_triggers.py:100` `def remove(self, trigger_id)` -- Delete a trigger.
- `TriggerStore.set_enabled` (method) `modules/loop_triggers.py:111` `def set_enabled(self, trigger_id, enabled)` -- Flip one trigger's enabled flag in place.
- `TriggerStore.list` (method) `modules/loop_triggers.py:125` `def list(self)` -- Return all triggers.
- `TriggerStore.ensure_service_trigger` (method) `modules/loop_triggers.py:129` `def ensure_service_trigger(self)` -- Register the catalog trigger once so services fire the loop.
- `TriggerStore.due` (method) `modules/loop_triggers.py:142` `def due(self, task_id, graph, activity, assets, store)` -- Evaluate triggers like the scheduler tick; fires at most once each.

## modules/macos_payloads.py
Imported by: `cli/commands/payload_arsenal.py`
- `MacOSPayloadFactory.__init__` (method) `modules/macos_payloads.py:111` `def __init__(self, config, output_dir)`
- `MacOSPayloadFactory.generate_app_bundle` (method) `modules/macos_payloads.py:137` `def generate_app_bundle(self)` -- Generate a macOS .app bundle with embedded reverse shell.
- `MacOSPayloadFactory.generate_launchd_persistence` (method) `modules/macos_payloads.py:212` `def generate_launchd_persistence(self)` -- Generate a LaunchDaemon or LaunchAgent plist for persistence.
- `MacOSPayloadFactory.generate_tcc_bypass` (method) `modules/macos_payloads.py:268` `def generate_tcc_bypass(self)` -- Generate a TCC bypass script targeting common permissions.
- `MacOSPayloadFactory.generate_osascript_dropper` (method) `modules/macos_payloads.py:314` `def generate_osascript_dropper(self)` -- Generate an AppleScript-based dropper that downloads and executes a stage.
- `MacOSPayloadFactory.generate_swift_stager` (method) `modules/macos_payloads.py:335` `def generate_swift_stager(self)` -- Generate a Swift reverse shell stager.
- `MacOSPayloadFactory.generate_persistence_scripts` (method) `modules/macos_payloads.py:398` `def generate_persistence_scripts(self)` -- Generate all available macOS persistence scripts.
- `MacOSPayloadFactory.generate_phishing_dialog` (method) `modules/macos_payloads.py:447` `def generate_phishing_dialog(self)` -- Generate an AppleScript credential phishing dialog.
- `MacOSPayloadFactory.generate_all` (method) `modules/macos_payloads.py:470` `def generate_all(self)` -- Generate all macOS payload artifacts.
- `MacOSPayloadFactory.list_tcc_services` (method) `modules/macos_payloads.py:517` `def list_tcc_services()` -- Return the list of known TCC service identifiers.
- `MacOSPayloadFactory.list_persistence_methods` (method) `modules/macos_payloads.py:522` `def list_persistence_methods()` -- Return the list of available persistence methods for macOS.


Next: [API_p15.md](API_p15.md)
