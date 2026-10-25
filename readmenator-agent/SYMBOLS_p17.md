# Symbols (page 17 of 45)
Previous: [SYMBOLS_p16.md](SYMBOLS_p16.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `update_role` | method | `modules/lazy_rbac.py:304` | `def update_role(self, user_id, new_role)` |
| `valid_roles` | method | `modules/lazy_rbac.py:62` | `def valid_roles(cls)` |
| `verify_recovery_code` | method | `modules/lazy_rbac.py:192` | `def verify_recovery_code(self, code)` |
| `verify_totp` | method | `modules/lazy_rbac.py:187` | `def verify_totp(self, token)` |
| `conformance` | function | `modules/lazy_roles.py:154` | `def conformance(role)` |
| `list_roles` | function | `modules/lazy_roles.py:100` | `def list_roles()` |
| `role_prompt` | function | `modules/lazy_roles.py:109` | `def role_prompt(role, goal, context)` |
| `roles_for_phase` | function | `modules/lazy_roles.py:134` | `def roles_for_phase(phase)` |
| `LoopRunConfig` | class | `modules/lazy_runner.py:94` | `class LoopRunConfig` |
| `ThreadStdoutRouter` | class | `modules/lazy_runner.py:45` | `class ThreadStdoutRouter(TextIOBase)` |
| `__init__` | method | `modules/lazy_runner.py:55` | `def __init__(self, main_stream, spool)` |
| `_abort_run` | function | `modules/lazy_runner.py:391` | `def _abort_run(engine, task_id, reason)` |
| `_apply_budget` | function | `modules/lazy_runner.py:506` | `def _apply_budget(engine, task_id, budget)` |
| `_bootstrap` | function | `modules/lazy_runner.py:492` | `def _bootstrap(scan_target, executor)` |
| `_budget_declined` | function | `modules/lazy_runner.py:519` | `def _budget_declined(config)` |
| `_dump_thread_stacks` | function | `modules/lazy_runner.py:665` | `def _dump_thread_stacks()` |
| `_executor` | function | `modules/lazy_runner.py:343` | `def _executor(command)` |
| `_format_activity` | function | `modules/lazy_runner.py:651` | `def _format_activity(record)` |
| `_limited` | function | `modules/lazy_runner.py:1042` | `def _limited()` |
| `_overview` | function | `modules/lazy_runner.py:641` | `def _overview(task_id)` |
| `_poll_progress` | function | `modules/lazy_runner.py:694` | `def _poll_progress(engine, config, progress, transcript, worker)` |
| `_prepare_engine` | function | `modules/lazy_runner.py:410` | `def _prepare_engine(engine, shell, config, params)` |
| `_resolve_alias` | function | `modules/lazy_runner.py:335` | `def _resolve_alias(command)` |
| `_run` | function | `modules/lazy_runner.py:587` | `def _run()` |
| `_run_plain` | function | `modules/lazy_runner.py:812` | `def _run_plain(engine, config)` |
| `_run_targets_file` | function | `modules/lazy_runner.py:1016` | `def _run_targets_file(shell, params, config)` |
| `_run_with_progress` | function | `modules/lazy_runner.py:535` | `def _run_with_progress(engine, config)` |
| `_stall_thresholds` | function | `modules/lazy_runner.py:680` | `def _stall_thresholds(verb_timeout)` |
| `_start_proxy` | function | `modules/lazy_runner.py:424` | `def _start_proxy(engine, params)` |
| `_terminal_stream` | function | `modules/lazy_runner.py:790` | `def _terminal_stream()` |
| `_to_float` | function | `modules/lazy_runner.py:155` | `def _to_float(raw, default)` |
| `_to_int` | function | `modules/lazy_runner.py:147` | `def _to_int(raw, default)` |
| `_tty_available` | function | `modules/lazy_runner.py:1003` | `def _tty_available()` |
| `_work_one` | function | `modules/lazy_runner.py:1039` | `def _work_one(target)` |
| `_write` | function | `modules/lazy_runner.py:802` | `def _write(text)` |
| `build_executor` | function | `modules/lazy_runner.py:318` | `def build_executor(shell, config, stream, cancelled, sandbox_task_id, sandbox_image)` |
| `clamped` | method | `modules/lazy_runner.py:118` | `def clamped(self)` |
| `encoding` | method | `modules/lazy_runner.py:80` | `def encoding(self)` |
| `flush` | method | `modules/lazy_runner.py:72` | `def flush(self)` |
| `isatty` | method | `modules/lazy_runner.py:84` | `def isatty(self)` |
| `load_targets_file` | function | `modules/lazy_runner.py:847` | `def load_targets_file(path)` |
| `parse_loop_line` | function | `modules/lazy_runner.py:163` | `def parse_loop_line(line)` |
| `report_result` | function | `modules/lazy_runner.py:449` | `def report_result(result)` |
| `resolve_loop_defaults` | function | `modules/lazy_runner.py:282` | `def resolve_loop_defaults(config)` |
| `run_loop` | function | `modules/lazy_runner.py:902` | `def run_loop(shell, params, config)` |
| `stream` | function | `modules/lazy_runner.py:550` | `def stream(text)` |
| `write` | method | `modules/lazy_runner.py:61` | `def write(self, data)` |
| `_payload_value` | function | `modules/lazy_sandbox.py:41` | `def _payload_value(key, default)` |
| `_sandbox_executor` | function | `modules/lazy_sandbox.py:265` | `def _sandbox_executor(command)` |
| `container_name` | function | `modules/lazy_sandbox.py:67` | `def container_name(task_id)` |
| `container_running` | function | `modules/lazy_sandbox.py:94` | `def container_running(task_id)` |
| `docker_available` | function | `modules/lazy_sandbox.py:73` | `def docker_available()` |
| `ensure_container` | function | `modules/lazy_sandbox.py:112` | `def ensure_container(task_id, image)` |
| `exec_command` | function | `modules/lazy_sandbox.py:180` | `def exec_command(task_id, command, timeout_sec, image)` |
| `executor_for` | function | `modules/lazy_sandbox.py:251` | `def executor_for(task_id, image)` |
| `image_available` | function | `modules/lazy_sandbox.py:78` | `def image_available(image)` |
| `image_name` | function | `modules/lazy_sandbox.py:52` | `def image_name(configured)` |
| `remove_container` | function | `modules/lazy_sandbox.py:214` | `def remove_container(task_id)` |
| `status` | function | `modules/lazy_sandbox.py:223` | `def status(task_id)` |
| `_hermes_config_path` | function | `modules/lazy_skill_mirror.py:112` | `def _hermes_config_path()` |
| `_hermes_frontmatter` | function | `modules/lazy_skill_mirror.py:45` | `def _hermes_frontmatter(name, fields)` |
| `_split_frontmatter` | function | `modules/lazy_skill_mirror.py:30` | `def _split_frontmatter(text)` |
| `available_skills` | function | `modules/lazy_skill_mirror.py:67` | `def available_skills()` |
| `mirror_all` | function | `modules/lazy_skill_mirror.py:106` | `def mirror_all()` |
| `mirror_skill` | function | `modules/lazy_skill_mirror.py:78` | `def mirror_skill(name)` |
| `register_external_dirs` | function | `modules/lazy_skill_mirror.py:117` | `def register_external_dirs()` |
| `_frontmatter` | function | `modules/lazy_skills.py:28` | `def _frontmatter(text)` |
| `_load` | function | `modules/lazy_skills.py:53` | `def _load(path)` |
| `_skill_files` | function | `modules/lazy_skills.py:42` | `def _skill_files()` |
| `get_skill` | function | `modules/lazy_skills.py:91` | `def get_skill(name)` |
| `list_skills` | function | `modules/lazy_skills.py:85` | `def list_skills()` |
| `match_skills` | function | `modules/lazy_skills.py:102` | `def match_skills(text, limit)` |
| `skills_context` | function | `modules/lazy_skills.py:118` | `def skills_context(text, explicit, auto, budget)` |
| `_digest` | function | `modules/lazy_summarizer.py:100` | `def _digest(older, complete)` |
| `_text_of` | function | `modules/lazy_summarizer.py:26` | `def _text_of(record)` |
| `_truncate_records` | function | `modules/lazy_summarizer.py:126` | `def _truncate_records(records, budget)` |
| `should_compact` | function | `modules/lazy_summarizer.py:35` | `def should_compact(used_chars, budget_chars)` |
| `summarize_chain` | function | `modules/lazy_summarizer.py:50` | `def summarize_chain(records, budget_chars, complete)` |
| `abusar_tar` | function | `modules/lazyatack.sh:248` | `` |
| `comprobar_rutas` | function | `modules/lazyatack.sh:242` | `` |
| `comprobar_sudo` | function | `modules/lazyatack.sh:194` | `` |
| `configurar_netcat` | function | `modules/lazyatack.sh:139` | `` |
| `configurar_shell_reversa` | function | `modules/lazyatack.sh:165` | `` |
| `configurar_tty` | function | `modules/lazyatack.sh:206` | `` |
| `descargar_seclists` | function | `modules/lazyatack.sh:107` | `` |
| `ejecutar_wfuzz` | function | `modules/lazyatack.sh:188` | `` |
| `eliminar_archivos` | function | `modules/lazyatack.sh:217` | `` |
| `eliminar_contenedores_docker` | function | `modules/lazyatack.sh:260` | `` |
| `enumerar_http` | function | `modules/lazyatack.sh:127` | `` |
| `enumerar_puertos` | function | `modules/lazyatack.sh:254` | `` |
| `enumerar_suid` | function | `modules/lazyatack.sh:230` | `` |
| `enviar_archivo_netcat` | function | `modules/lazyatack.sh:145` | `` |
| `escanear_puertos` | function | `modules/lazyatack.sh:115` | `` |
| `escanear_puertos_especificos` | function | `modules/lazyatack.sh:121` | `` |
| `escanear_red` | function | `modules/lazyatack.sh:266` | `` |
| `escuchar_shell` | function | `modules/lazyatack.sh:171` | `` |
| `explotar_lfi` | function | `modules/lazyatack.sh:200` | `` |
| `iniciar_servidor_http` | function | `modules/lazyatack.sh:133` | `` |
| `listar_timers` | function | `modules/lazyatack.sh:236` | `` |
| `menu_cliente` | function | `modules/lazyatack.sh:307` | `` |
| `menu_servidor` | function | `modules/lazyatack.sh:272` | `` |
| `monitorear_procesos` | function | `modules/lazyatack.sh:177` | `` |
| `mostrar_ayuda` | function | `modules/lazyatack.sh:21` | `` |
| `obtener_root_shell` | function | `modules/lazyatack.sh:223` | `` |
| `validar_ip` | function | `modules/lazyatack.sh:33` | `` |
| `validar_url` | function | `modules/lazyatack.sh:49` | `` |
| `verificar_conectividad` | function | `modules/lazyatack.sh:151` | `` |
| `verificar_curl` | function | `modules/lazyatack.sh:158` | `` |
| `CloudBucketEnumerator` | class | `modules/lazycloud.py:248` | `class CloudBucketEnumerator` |
| `CloudFinding` | class | `modules/lazycloud.py:98` | `class CloudFinding` |
| `CloudIAMEnumerator` | class | `modules/lazycloud.py:342` | `class CloudIAMEnumerator` |
| `CloudMetadataHarvester` | class | `modules/lazycloud.py:108` | `class CloudMetadataHarvester` |
| `CloudResource` | class | `modules/lazycloud.py:87` | `class CloudResource` |
| `CloudScanner` | class | `modules/lazycloud.py:390` | `class CloudScanner` |
| `__init__` | method | `modules/lazycloud.py:111` | `def __init__(self, timeout)` |
| `__init__` | method | `modules/lazycloud.py:251` | `def __init__(self, timeout)` |
| `__init__` | method | `modules/lazycloud.py:393` | `def __init__(self, target_domain, timeout)` |
| `_aws_sig` | function | `modules/lazycloud.py:361` | `def _aws_sig(key, msg)` |
| `_check_url` | method | `modules/lazycloud.py:262` | `def _check_url(self, url)` |
| `_get` | method | `modules/lazycloud.py:122` | `def _get(self, url, headers)` |
| `_sign` | function | `modules/lazycloud.py:364` | `def _sign(key, msg)` |
| `enumerate_aws_iam` | method | `modules/lazycloud.py:345` | `def enumerate_aws_iam(self, access_key, secret_key, session_token)` |
| `enumerate_azure_storage` | method | `modules/lazycloud.py:303` | `def enumerate_azure_storage(self, prefix, accounts)` |
| `enumerate_gcp_storage` | method | `modules/lazycloud.py:321` | `def enumerate_gcp_storage(self, prefix, buckets)` |
| `enumerate_s3` | method | `modules/lazycloud.py:278` | `def enumerate_s3(self, prefix, buckets)` |
| `full_scan` | method | `modules/lazycloud.py:400` | `def full_scan(self, target_prefix, sessions_dir)` |
| `harvest_all` | method | `modules/lazycloud.py:231` | `def harvest_all(self)` |
| `harvest_aws` | method | `modules/lazycloud.py:139` | `def harvest_aws(self)` |
| `harvest_azure` | method | `modules/lazycloud.py:184` | `def harvest_azure(self)` |
| `harvest_gcp` | method | `modules/lazycloud.py:208` | `def harvest_gcp(self)` |
| `quick_buckets` | method | `modules/lazycloud.py:460` | `def quick_buckets(self, prefix)` |
| `quick_metadata` | method | `modules/lazycloud.py:456` | `def quick_metadata(self)` |
| `session` | method | `modules/lazycloud.py:116` | `def session(self)` |
| `session` | method | `modules/lazycloud.py:256` | `def session(self)` |
| `ctrl_c` | function | `modules/lazycurl.sh:23` | `` |
| `execute_curl` | function | `modules/lazycurl.sh:52` | `` |
| `show_help` | function | `modules/lazycurl.sh:29` | `` |
| `base64_decode` | function | `modules/lazyencoder_decoder.py:8` | `def base64_decode(data)` |
| `base64_encode` | function | `modules/lazyencoder_decoder.py:4` | `def base64_encode(data)` |
| `caesar_cipher` | function | `modules/lazyencoder_decoder.py:13` | `def caesar_cipher(text, shift)` |
| `caesar_decipher` | function | `modules/lazyencoder_decoder.py:27` | `def caesar_decipher(text, shift)` |
| `decode` | function | `modules/lazyencoder_decoder.py:82` | `def decode(data, shift, key)` |
| `decode_string` | function | `modules/lazyencoder_decoder.py:94` | `def decode_string(data, shift, key)` |
| `encode` | function | `modules/lazyencoder_decoder.py:63` | `def encode(data, shift, key)` |
| `encode_string` | function | `modules/lazyencoder_decoder.py:75` | `def encode_string(data, shift, key)` |
| `key_substitution` | function | `modules/lazyencoder_decoder.py:31` | `def key_substitution(text, key)` |
| `key_substitution_reverse` | function | `modules/lazyencoder_decoder.py:47` | `def key_substitution_reverse(text, key)` |
| `execute_evil_winrm` | function | `modules/lazyevilwimrm.sh:14` | `` |
| `ContainerEscapeTechniques` | class | `modules/lazyk8s.py:624` | `class ContainerEscapeTechniques` |
| `ContainerFinding` | class | `modules/lazyk8s.py:30` | `class ContainerFinding` |
| `ContainerResource` | class | `modules/lazyk8s.py:20` | `class ContainerResource` |
| `ContainerRuntimeDetector` | class | `modules/lazyk8s.py:759` | `class ContainerRuntimeDetector` |
| `DockerEnumerator` | class | `modules/lazyk8s.py:41` | `class DockerEnumerator` |
| `K8sEnumerator` | class | `modules/lazyk8s.py:264` | `class K8sEnumerator` |
| `__init__` | method | `modules/lazyk8s.py:44` | `def __init__(self, socket_path)` |
| `__init__` | method | `modules/lazyk8s.py:267` | `def __init__(self, kubeconfig, token, api_server)` |
| `_docker_api` | method | `modules/lazyk8s.py:51` | `def _docker_api(self, endpoint)` |
| `_get_k8s_api` | method | `modules/lazyk8s.py:285` | `def _get_k8s_api(self, path)` |
| `_load_kubeconfig` | method | `modules/lazyk8s.py:274` | `def _load_kubeconfig(self)` |
| `auto_detect_all` | method | `modules/lazyk8s.py:992` | `def auto_detect_all()` |
| `check_capabilities` | method | `modules/lazyk8s.py:217` | `def check_capabilities(self)` |
| `check_docker_socket_mount` | method | `modules/lazyk8s.py:196` | `def check_docker_socket_mount(self)` |
| `check_pod_escape_vectors` | method | `modules/lazyk8s.py:530` | `def check_pod_escape_vectors(self)` |
| `check_privileged_containers` | method | `modules/lazyk8s.py:137` | `def check_privileged_containers(self)` |
| `check_rbac` | method | `modules/lazyk8s.py:498` | `def check_rbac(self)` |
| `check_sensitive_mounts` | method | `modules/lazyk8s.py:162` | `def check_sensitive_mounts(self)` |
| `detect_current_environment` | method | `modules/lazyk8s.py:684` | `def detect_current_environment()` |
| `detect_dangerous_capabilities` | method | `modules/lazyk8s.py:921` | `def detect_dangerous_capabilities()` |
| `detect_mounts` | method | `modules/lazyk8s.py:874` | `def detect_mounts()` |
| `detect_runtime` | method | `modules/lazyk8s.py:803` | `def detect_runtime()` |
| `full_check` | method | `modules/lazyk8s.py:250` | `def full_check(self)` |
| `full_check` | method | `modules/lazyk8s.py:582` | `def full_check(self, sessions_dir)` |
| `inspect_container` | method | `modules/lazyk8s.py:118` | `def inspect_container(self, container_id)` |
| `is_socket_accessible` | method | `modules/lazyk8s.py:47` | `def is_socket_accessible(self)` |
| `list_containers` | method | `modules/lazyk8s.py:70` | `def list_containers(self)` |
| `list_images` | method | `modules/lazyk8s.py:94` | `def list_images(self)` |
| `list_namespaces` | method | `modules/lazyk8s.py:390` | `def list_namespaces(self)` |
| `list_pods` | method | `modules/lazyk8s.py:366` | `def list_pods(self, namespace)` |
| `list_secrets` | method | `modules/lazyk8s.py:410` | `def list_secrets(self, namespace)` |
| `list_service_accounts` | method | `modules/lazyk8s.py:462` | `def list_service_accounts(self, namespace)` |
| `check_sudo` | function | `modules/lazylynis.sh:32` | `` |
| `ctrl_c` | function | `modules/lazymasscan.sh:20` | `` |
| `extract_ports_info` | function | `modules/lazymasscan.sh:74` | `` |
| `print_row` | function | `modules/lazymasscan.sh:117` | `` |
| `run_masscan_script` | function | `modules/lazymasscan.sh:94` | `` |
| `cleanup` | function | `modules/lazynmap.sh:29` | `` |
| `ctrl_c` | function | `modules/lazynmap.sh:38` | `` |
| `discover_network` | function | `modules/lazynmap.sh:149` | `` |
| `extract_ports_info` | function | `modules/lazynmap.sh:818` | `` |
| `fix_sessions_owner` | function | `modules/lazynmap.sh:74` | `` |
| `nmaptest` | function | `modules/lazynmap.sh:129` | `` |
| `print_row` | function | `modules/lazynmap.sh:877` | `` |
| `run_nmap_script` | function | `modules/lazynmap.sh:844` | `` |
| `ProxyHandler` | class | `modules/lazyown_bprfuzzer.py:114` | `class ProxyHandler(BaseHTTPRequestHandler)` |
| `_handle_request` | method | `modules/lazyown_bprfuzzer.py:121` | `def _handle_request(self, method)` |
| `_load_security_config` | function | `modules/lazyown_bprfuzzer.py:45` | `def _load_security_config()` |
| `do_GET` | method | `modules/lazyown_bprfuzzer.py:115` | `def do_GET(self)` |
| `do_POST` | method | `modules/lazyown_bprfuzzer.py:118` | `def do_POST(self)` |
| `edit_file_with_nano` | function | `modules/lazyown_bprfuzzer.py:169` | `def edit_file_with_nano(content)` |
| `lazyfuzz` | function | `modules/lazyown_bprfuzzer.py:233` | `def lazyfuzz(url, method, headers, params, data, json_data, proxies, wordlist_path, hide_code)` |
| `load_data_from_file` | function | `modules/lazyown_bprfuzzer.py:99` | `def load_data_from_file(file_path)` |
| `load_headers_from_file` | function | `modules/lazyown_bprfuzzer.py:93` | `def load_headers_from_file(file_path)` |
| `main` | function | `modules/lazyown_bprfuzzer.py:302` | `def main()` |
| `parse_arguments` | function | `modules/lazyown_bprfuzzer.py:278` | `def parse_arguments()` |
| `repeater` | function | `modules/lazyown_bprfuzzer.py:203` | `def repeater(url, method, headers, params, data, json_data, proxies, hide_code)` |
| `run_proxy` | function | `modules/lazyown_bprfuzzer.py:162` | `def run_proxy(port)` |
| `send_request` | function | `modules/lazyown_bprfuzzer.py:179` | `def send_request(url, method, headers, params, data, json_data, proxies, hide_code)` |
| `signal_handler` | function | `modules/lazyown_bprfuzzer.py:105` | `def signal_handler(sig, frame)` |
| `AbstractSelector` | class | `modules/lazyown_bridge.py:3984` | `class AbstractSelector(ABC)` |
| `BridgeDispatcher` | class | `modules/lazyown_bridge.py:4233` | `class BridgeDispatcher` |
| `CatalogEntry` | class | `modules/lazyown_bridge.py:48` | `class CatalogEntry` |
| `CommandCatalog` | class | `modules/lazyown_bridge.py:115` | `class CommandCatalog` |
| `ContextEnricher` | class | `modules/lazyown_bridge.py:4103` | `class ContextEnricher` |
| `MitreAlignedSelector` | class | `modules/lazyown_bridge.py:4042` | `class MitreAlignedSelector(AbstractSelector)` |
| `PhaseMapper` | class | `modules/lazyown_bridge.py:4153` | `class PhaseMapper` |
| `ServiceAwareSelector` | class | `modules/lazyown_bridge.py:4002` | `class ServiceAwareSelector(AbstractSelector)` |
| `TagSelector` | class | `modules/lazyown_bridge.py:4071` | `class TagSelector(AbstractSelector)` |
| `__init__` | method | `modules/lazyown_bridge.py:118` | `def __init__(self)` |
| `__init__` | method | `modules/lazyown_bridge.py:4045` | `def __init__(self, technique_id)` |
| `__init__` | method | `modules/lazyown_bridge.py:4074` | `def __init__(self, tag)` |
| `__init__` | method | `modules/lazyown_bridge.py:4239` | `def __init__(self, catalog, selector, enricher, phase_mapper)` |
| `_populate` | method | `modules/lazyown_bridge.py:122` | `def _populate(self)` |
| `all_phases` | method | `modules/lazyown_bridge.py:3966` | `def all_phases(self)` |
| `all_phases` | method | `modules/lazyown_bridge.py:4347` | `def all_phases(self)` |
| `build_command` | method | `modules/lazyown_bridge.py:63` | `def build_command(self, target, port, user, password, domain, url, wordlist, lhost, lport)` |
| `by_mitre` | method | `modules/lazyown_bridge.py:3952` | `def by_mitre(self, technique_id)` |
| `by_os` | method | `modules/lazyown_bridge.py:3963` | `def by_os(self, os_hint)` |
| `by_phase` | method | `modules/lazyown_bridge.py:3946` | `def by_phase(self, phase)` |
| `by_service` | method | `modules/lazyown_bridge.py:3956` | `def by_service(self, service_name)` |
| `by_tag` | method | `modules/lazyown_bridge.py:3960` | `def by_tag(self, tag)` |
| `canonical_kill_chain_order` | method | `modules/lazyown_bridge.py:4204` | `def canonical_kill_chain_order()` |
| `catalog_count` | method | `modules/lazyown_bridge.py:4395` | `def catalog_count(self)` |
| `catalog_summary` | method | `modules/lazyown_bridge.py:4350` | `def catalog_summary(self)` |
| `catalog_summary_filtered` | method | `modules/lazyown_bridge.py:4358` | `def catalog_summary_filtered(self, phase, os_hint)` |
| `count` | method | `modules/lazyown_bridge.py:3975` | `def count(self)` |
| `enrich` | method | `modules/lazyown_bridge.py:4106` | `def enrich(self, entry, target, world_snapshot)` |
| `get` | method | `modules/lazyown_bridge.py:3969` | `def get(self, command)` |
| `get_dispatcher` | function | `modules/lazyown_bridge.py:4409` | `def get_dispatcher()` |
| `kill_chain_order` | method | `modules/lazyown_bridge.py:4223` | `def kill_chain_order(self)` |
| `list_phase` | method | `modules/lazyown_bridge.py:4343` | `def list_phase(self, phase)` |
| `matches_os` | method | `modules/lazyown_bridge.py:104` | `def matches_os(self, os_hint)` |
| `matches_service` | method | `modules/lazyown_bridge.py:94` | `def matches_service(self, services)` |
| `phase_kill_chain` | method | `modules/lazyown_bridge.py:4398` | `def phase_kill_chain(self)` |
| `select` | method | `modules/lazyown_bridge.py:3986` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:4005` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:4049` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `select` | method | `modules/lazyown_bridge.py:4078` | `def select(self, catalog, phase, services, has_creds, excluded, os_hint)` |
| `suggest` | method | `modules/lazyown_bridge.py:4251` | `def suggest(self, phase, target, services, has_creds, excluded, world_snapshot, mitre_hint, tag_hint, os_hint)` |
| `suggest_for_wm_phase` | method | `modules/lazyown_bridge.py:4325` | `def suggest_for_wm_phase(self, wm_phase_value, target, services, has_creds, excluded, world_snapshot)` |
| `suggest_sequence` | method | `modules/lazyown_bridge.py:4296` | `def suggest_sequence(self, phase, target, services, has_creds, excluded, world_snapshot, limit)` |
| `to_bridge_phase` | method | `modules/lazyown_bridge.py:4210` | `def to_bridge_phase(self, wm_phase)` |
| `extract_docx_metadata` | function | `modules/lazyown_metaextract0r.py:62` | `def extract_docx_metadata(file_path)` |
| `extract_image_metadata` | function | `modules/lazyown_metaextract0r.py:85` | `def extract_image_metadata(file_path)` |
| `extract_metadata` | function | `modules/lazyown_metaextract0r.py:96` | `def extract_metadata(file_path)` |
| `extract_ole_metadata` | function | `modules/lazyown_metaextract0r.py:73` | `def extract_ole_metadata(file_path)` |
| `extract_pdf_metadata` | function | `modules/lazyown_metaextract0r.py:51` | `def extract_pdf_metadata(file_path)` |
| `find_and_extract_metadata` | function | `modules/lazyown_metaextract0r.py:109` | `def find_and_extract_metadata(directory, output_file)` |
| `main` | function | `modules/lazyown_metaextract0r.py:140` | `def main()` |
| `parse_arguments` | function | `modules/lazyown_metaextract0r.py:130` | `def parse_arguments()` |
| `signal_handler` | function | `modules/lazyown_metaextract0r.py:42` | `def signal_handler(sig, frame)` |
| `buscar_binarios` | function | `modules/lazyown_parquet_tool.py:53` | `def buscar_binarios(args)` |
| `ejecutar_opciones` | function | `modules/lazyown_parquet_tool.py:136` | `def ejecutar_opciones()` |
| `highlight_term` | function | `modules/lazyown_parquet_tool.py:34` | `def highlight_term(text, term)` |
| `search_in_parquet` | function | `modules/lazyown_parquet_tool.py:39` | `def search_in_parquet(term, parquet_files)` |
| `main` | function | `modules/lazyownerweb.py:59` | `def main()` |
| `send_request` | function | `modules/lazyownerweb.py:36` | `def send_request(url, params, method)` |
| `test_injection` | function | `modules/lazyownerweb.py:49` | `def test_injection(url, payloads, param_name, detection_strings, method)` |
| `execute_psexec` | function | `modules/lazypsexec.sh:15` | `` |
| `mostrar_ayuda` | function | `modules/lazyreverse_shell.sh:21` | `` |
| `validar_ip` | function | `modules/lazyreverse_shell.sh:31` | `` |
| `apply_vpn_rules` | function | `modules/lazyvpnshield.sh:45` | `` |
| `check_sudo` | function | `modules/lazyvpnshield.sh:16` | `` |
| `ctrl_c` | function | `modules/lazyvpnshield.sh:11` | `` |
| `main` | function | `modules/lazyvpnshield.sh:113` | `` |
| `save_current_rules` | function | `modules/lazyvpnshield.sh:29` | `` |
| `show_current_rules` | function | `modules/lazyvpnshield.sh:37` | `` |
| `undo_and_restore_rules` | function | `modules/lazyvpnshield.sh:86` | `` |
| `ctrl_c` | function | `modules/lazywps.sh:9` | `` |
| `LessonIngestor` | class | `modules/lesson_ingestor.py:77` | `class LessonIngestor` |
| `LessonLearned` | class | `modules/lesson_ingestor.py:55` | `class LessonLearned` |
| `__init__` | method | `modules/lesson_ingestor.py:86` | `def __init__(self, lessons_file, router, trainer, boost_reward)` |
| `_expert_for_topic` | method | `modules/lesson_ingestor.py:122` | `def _expert_for_topic(self, topic)` |
| `_get_router` | method | `modules/lesson_ingestor.py:98` | `def _get_router(self)` |
| `_get_trainer` | method | `modules/lesson_ingestor.py:110` | `def _get_trainer(self)` |
| `_load_from_file` | method | `modules/lesson_ingestor.py:202` | `def _load_from_file(self)` |
| `from_dict` | method | `modules/lesson_ingestor.py:66` | `def from_dict(cls, d)` |
| `ingest` | method | `modules/lesson_ingestor.py:125` | `def ingest(self, lesson)` |
| `ingest_all` | method | `modules/lesson_ingestor.py:185` | `def ingest_all(self, lessons)` |
| `ingest_campaign_lessons` | function | `modules/lesson_ingestor.py:222` | `def ingest_campaign_lessons(lessons_file)` |
| `LogFileHandler` | class | `modules/lilsplunky.py:217` | `class LogFileHandler(FileSystemEventHandler)` |
| `__init__` | method | `modules/lilsplunky.py:223` | `def __init__(self, log_dir, mode)` |
| `analyze_with_deepseek` | function | `modules/lilsplunky.py:123` | `def analyze_with_deepseek(log_entry_data)` |
| `display_record` | function | `modules/lilsplunky.py:346` | `def display_record(record)` |
| `initialize_file_positions` | method | `modules/lilsplunky.py:229` | `def initialize_file_positions(self)` |
| `is_monitored` | method | `modules/lilsplunky.py:245` | `def is_monitored(self, file_path)` |
| `on_created` | method | `modules/lilsplunky.py:336` | `def on_created(self, event)` |
| `on_modified` | method | `modules/lilsplunky.py:331` | `def on_modified(self, event)` |
| `parse_args` | function | `modules/lilsplunky.py:446` | `def parse_args()` |
| `process_file` | method | `modules/lilsplunky.py:257` | `def process_file(self, file_path)` |
| `search_logs` | function | `modules/lilsplunky.py:382` | `def search_logs(query, file_path)` |
| `simple_parse_log_line` | function | `modules/lilsplunky.py:69` | `def simple_parse_log_line(line, file_path)` |
| `start_monitoring` | function | `modules/lilsplunky.py:413` | `def start_monitoring(log_dir, mode)` |
| `store_event` | function | `modules/lilsplunky.py:108` | `def store_event(event_data)` |
| `LinuxAdvancedConfig` | class | `modules/linux_advanced_payloads.py:64` | `class LinuxAdvancedConfig` |
| `LinuxAdvancedPayloadFactory` | class | `modules/linux_advanced_payloads.py:92` | `class LinuxAdvancedPayloadFactory` |
| `__init__` | method | `modules/linux_advanced_payloads.py:105` | `def __init__(self, config, output_dir)` |
| `_ip_to_hex` | method | `modules/linux_advanced_payloads.py:305` | `def _ip_to_hex(ip_str)` |
| `compile_c_source` | method | `modules/linux_advanced_payloads.py:707` | `def compile_c_source(self, source, output_name, shared)` |
| `generate_all` | method | `modules/linux_advanced_payloads.py:749` | `def generate_all(self)` |
| `generate_ebpf_payload` | method | `modules/linux_advanced_payloads.py:235` | `def generate_ebpf_payload(self)` |
| `generate_kernel_module` | method | `modules/linux_advanced_payloads.py:519` | `def generate_kernel_module(self)` |
| `generate_ld_preload_rootkit` | method | `modules/linux_advanced_payloads.py:110` | `def generate_ld_preload_rootkit(self)` |
| `generate_motd_backdoor` | method | `modules/linux_advanced_payloads.py:689` | `def generate_motd_backdoor(self)` |
| `generate_pam_backdoor` | method | `modules/linux_advanced_payloads.py:311` | `def generate_pam_backdoor(self)` |
| `generate_process_masquerade` | method | `modules/linux_advanced_payloads.py:632` | `def generate_process_masquerade(self)` |
| `generate_ssh_persistence` | method | `modules/linux_advanced_payloads.py:458` | `def generate_ssh_persistence(self)` |
| `generate_systemd_persistence` | method | `modules/linux_advanced_payloads.py:398` | `def generate_systemd_persistence(self)` |
| `generate_udev_persistence` | method | `modules/linux_advanced_payloads.py:676` | `def generate_udev_persistence(self)` |
| `list_hook_functions` | method | `modules/linux_advanced_payloads.py:793` | `def list_hook_functions()` |
| `list_persistence_methods` | method | `modules/linux_advanced_payloads.py:797` | `def list_persistence_methods()` |
| `Listener` | class | `modules/listener_manager.py:141` | `class Listener` |
| `ListenerManager` | class | `modules/listener_manager.py:172` | `class ListenerManager` |
| `__init__` | method | `modules/listener_manager.py:179` | `def __init__(self, app, sessions_dir, payload)` |
| `_bind_address` | method | `modules/listener_manager.py:191` | `def _bind_address(self, port)` |
| `_collect_listener_bind_candidates` | function | `modules/listener_manager.py:35` | `def _collect_listener_bind_candidates(payload)` |
| `_listeners_path` | method | `modules/listener_manager.py:201` | `def _listeners_path(self)` |
| `_load` | method | `modules/listener_manager.py:204` | `def _load(self)` |
| `_probe_listener_bind` | function | `modules/listener_manager.py:72` | `def _probe_listener_bind(address, port)` |
| `_resolve_listener_bind_address` | function | `modules/listener_manager.py:110` | `def _resolve_listener_bind_address(payload, port)` |
| `_save` | method | `modules/listener_manager.py:217` | `def _save(self)` |
| `_stop` | method | `modules/listener_manager.py:331` | `def _stop(self, listener)` |
| `add` | method | `modules/listener_manager.py:229` | `def add(self, port, ssl, listener_id)` |
| `from_dict` | method | `modules/listener_manager.py:162` | `def from_dict(cls, data)` |
| `get_default_port` | method | `modules/listener_manager.py:367` | `def get_default_port(self, fallback)` |
| `remove` | method | `modules/listener_manager.py:242` | `def remove(self, listener_id)` |
| `set_payload` | method | `modules/listener_manager.py:187` | `def set_payload(self, payload)` |
| `start` | method | `modules/listener_manager.py:255` | `def start(self, listener_id)` |
| `start_all` | method | `modules/listener_manager.py:344` | `def start_all(self)` |
| `status` | method | `modules/listener_manager.py:355` | `def status(self)` |
| `stop` | method | `modules/listener_manager.py:323` | `def stop(self, listener_id)` |
| `stop_all` | method | `modules/listener_manager.py:350` | `def stop_all(self)` |
| `to_dict` | method | `modules/listener_manager.py:152` | `def to_dict(self)` |
| `_emit_edge` | function | `modules/live_surface.py:126` | `def _emit_edge(source, target, relation, weight)` |
| `_emit_node` | function | `modules/live_surface.py:106` | `def _emit_node(node_id, state, title)` |
| `_group_for` | function | `modules/live_surface.py:55` | `def _group_for(node_id)` |
| `_is_compromised` | function | `modules/live_surface.py:45` | `def _is_compromised(state)` |
| `_label_for` | function | `modules/live_surface.py:64` | `def _label_for(node_id)` |
| `_node_value` | function | `modules/live_surface.py:50` | `def _node_value(centrality)` |
| `build_live_graph` | function | `modules/live_surface.py:72` | `def build_live_graph(world)` |
| `_complete` | function | `modules/llm_adapter.py:82` | `def _complete(client, full_prompt, model)` |
| `_configure_logging` | function | `modules/llm_adapter.py:65` | `def _configure_logging(debug)` |
| `_process` | function | `modules/llm_adapter.py:96` | `def _process(client, prompt, debug, template, config)` |
| `_read_error` | function | `modules/llm_adapter.py:78` | `def _read_error(prompt)` |
| `_read_prompt_file` | function | `modules/llm_adapter.py:70` | `def _read_prompt_file(prompt)` |
| `ask_general` | function | `modules/llm_adapter.py:254` | `def ask_general(prompt, debug)` |
| `process_prompt` | function | `modules/llm_adapter.py:119` | `def process_prompt(client, prompt, debug)` |
| `process_prompt_adversary` | function | `modules/llm_adapter.py:147` | `def process_prompt_adversary(client, prompt, debug)` |
| `process_prompt_general` | function | `modules/llm_adapter.py:161` | `def process_prompt_general(client, prompt, debug)` |
| `process_prompt_redop` | function | `modules/llm_adapter.py:237` | `def process_prompt_redop(client, prompt, debug)` |
| `process_prompt_script` | function | `modules/llm_adapter.py:133` | `def process_prompt_script(client, prompt, debug)` |
| `process_prompt_search` | function | `modules/llm_adapter.py:175` | `def process_prompt_search(client, prompt, debug)` |
| `process_prompt_task` | function | `modules/llm_adapter.py:189` | `def process_prompt_task(client, prompt, debug)` |
| `process_prompt_vuln` | function | `modules/llm_adapter.py:206` | `def process_prompt_vuln(client, prompt, debug, event)` |
| `safe_groq_client` | function | `modules/llm_adapter.py:48` | `def safe_groq_client(api_key)` |
| `LLMClient` | class | `modules/llm_client.py:45` | `class LLMClient` |
| `__init__` | method | `modules/llm_client.py:63` | `def __init__(self, api_key, groq_model, ollama_model, timeout, max_tokens)` |
| `_ask_groq` | method | `modules/llm_client.py:179` | `def _ask_groq(self, prompt, model, system, temperature)` |
| `_ask_llamacpp` | method | `modules/llm_client.py:242` | `def _ask_llamacpp(self, prompt, model, system)` |
| `_ask_ollama` | method | `modules/llm_client.py:220` | `def _ask_ollama(self, prompt, model)` |
| `ask` | method | `modules/llm_client.py:79` | `def ask(self, prompt)` |
| `ask` | function | `modules/llm_client.py:276` | `def ask(prompt)` |
| `classify` | method | `modules/llm_client.py:130` | `def classify(self, output)` |
| `classify` | function | `modules/llm_client.py:288` | `def classify(output)` |
| `get_client` | function | `modules/llm_client.py:268` | `def get_client(api_key)` |
| `summarize` | method | `modules/llm_client.py:159` | `def summarize(self, text)` |
| `summarize` | function | `modules/llm_client.py:293` | `def summarize(text)` |
| `DecisionRecord` | class | `modules/llm_evaluator.py:21` | `class DecisionRecord` |
| `JSONLRecorder` | class | `modules/llm_evaluator.py:75` | `class JSONLRecorder(OutcomeRecorder)` |
| `LLMEvaluator` | class | `modules/llm_evaluator.py:161` | `class LLMEvaluator` |
| `OutcomeRecorder` | class | `modules/llm_evaluator.py:55` | `class OutcomeRecorder(ABC)` |
| `QualityMetrics` | class | `modules/llm_evaluator.py:140` | `class QualityMetrics` |
| `__init__` | method | `modules/llm_evaluator.py:76` | `def __init__(self, path)` |
| `__init__` | method | `modules/llm_evaluator.py:162` | `def __init__(self, recorder)` |
| `_cli` | function | `modules/llm_evaluator.py:322` | `def _cli()` |
| `_new_id` | function | `modules/llm_evaluator.py:35` | `def _new_id()` |
| `_record_from_dict` | function | `modules/llm_evaluator.py:39` | `def _record_from_dict(d)` |
| `_safe_mean` | function | `modules/llm_evaluator.py:150` | `def _safe_mean(values)` |
| `_tactic_success_rates` | function | `modules/llm_evaluator.py:154` | `def _tactic_success_rates(records)` |
| `compute_metrics` | method | `modules/llm_evaluator.py:200` | `def compute_metrics(self, session_id)` |
| `export_finetuning_dataset` | method | `modules/llm_evaluator.py:256` | `def export_finetuning_dataset(self, path)` |
| `get_evaluator` | function | `modules/llm_evaluator.py:293` | `def get_evaluator()` |
| `load_all` | method | `modules/llm_evaluator.py:69` | `def load_all(self)` |
| `load_all` | method | `modules/llm_evaluator.py:120` | `def load_all(self)` |
| `load_by_session` | method | `modules/llm_evaluator.py:72` | `def load_by_session(self, session_id)` |
| `load_by_session` | method | `modules/llm_evaluator.py:135` | `def load_by_session(self, session_id)` |
| `quality_report` | method | `modules/llm_evaluator.py:241` | `def quality_report(self, session_id)` |
| `record` | method | `modules/llm_evaluator.py:57` | `def record(self, decision)` |
| `record` | method | `modules/llm_evaluator.py:81` | `def record(self, decision)` |
| `record_decision` | method | `modules/llm_evaluator.py:165` | `def record_decision(self, session_id, thought, action, mitre_tactic, expected_outcome, confidence)` |
| `record_decision` | function | `modules/llm_evaluator.py:302` | `def record_decision(session_id, thought, action, mitre_tactic, expected_outcome, confidence)` |
| `record_outcome` | method | `modules/llm_evaluator.py:191` | `def record_outcome(self, decision_id, actual_outcome, findings_count, success)` |
| `record_outcome` | function | `modules/llm_evaluator.py:313` | `def record_outcome(decision_id, actual_outcome, findings_count, success)` |
| `update_outcome` | method | `modules/llm_evaluator.py:60` | `def update_outcome(self, decision_id, actual, findings_count, success)` |
| `update_outcome` | method | `modules/llm_evaluator.py:86` | `def update_outcome(self, decision_id, actual, findings_count, success)` |
| `LLMBackendNotSupportedError` | class | `modules/llm_factory.py:194` | `class LLMBackendNotSupportedError(ValueError)` |
| `LLMBackendUnavailableError` | class | `modules/llm_factory.py:190` | `class LLMBackendUnavailableError(RuntimeError)` |
| `_build_anthropic` | function | `modules/llm_factory.py:524` | `def _build_anthropic(config)` |
| `_build_backend` | function | `modules/llm_factory.py:685` | `def _build_backend(normalized, resolved_config)` |
| `_build_deepseek` | function | `modules/llm_factory.py:546` | `def _build_deepseek(config)` |
| `_build_groq` | function | `modules/llm_factory.py:452` | `def _build_groq(config)` |
| `_build_llamacpp` | function | `modules/llm_factory.py:488` | `def _build_llamacpp(config)` |
| `_build_ollama` | function | `modules/llm_factory.py:474` | `def _build_ollama(config)` |
| `_build_openai` | function | `modules/llm_factory.py:502` | `def _build_openai(config)` |
| `_normalize_backend` | function | `modules/llm_factory.py:387` | `def _normalize_backend(backend)` |
| `_pi_complete` | function | `modules/llm_factory.py:787` | `def _pi_complete(model, prompt, max_tokens)` |
| `_pi_timeout` | function | `modules/llm_factory.py:775` | `def _pi_timeout()` |
| `_require_cloud_allowed` | function | `modules/llm_factory.py:420` | `def _require_cloud_allowed(normalized)` |
| `_resolve_api_key` | function | `modules/llm_factory.py:333` | `def _resolve_api_key(config)` |
| `_resolve_api_key_for_backend` | function | `modules/llm_factory.py:356` | `def _resolve_api_key_for_backend(backend, config)` |
| `_resolve_model_identifier` | function | `modules/llm_factory.py:568` | `def _resolve_model_identifier(backend_identifier, config)` |
| `_wrap_with_budget` | function | `modules/llm_factory.py:595` | `def _wrap_with_budget(backend, config, backend_identifier)` |
| `api_key_config_key` | function | `modules/llm_factory.py:266` | `def api_key_config_key(backend)` |
| `backend_requires_api_key` | function | `modules/llm_factory.py:291` | `def backend_requires_api_key(backend)` |
| `complete` | function | `modules/llm_factory.py:899` | `def complete(model, prompt, max_tokens)` |
| `default_model_for` | function | `modules/llm_factory.py:224` | `def default_model_for(backend)` |
| `get_llm_backend` | function | `modules/llm_factory.py:633` | `def get_llm_backend(config, backend)` |
| `get_llm_backend_raw` | function | `modules/llm_factory.py:729` | `def get_llm_backend_raw(config, backend)` |
| `groq_model_chain` | function | `modules/llm_factory.py:141` | `def groq_model_chain(config)` |
| `is_model_missing_error` | function | `modules/llm_factory.py:121` | `def is_model_missing_error(message)` |
| `load_payload` | function | `modules/llm_factory.py:309` | `def load_payload(payload_path)` |
| `model_config_key` | function | `modules/llm_factory.py:245` | `def model_config_key(backend)` |
| `stream_complete` | function | `modules/llm_factory.py:828` | `def stream_complete(model, prompt, max_tokens, on_delta)` |
| `try_get_llm_backend` | function | `modules/llm_factory.py:751` | `def try_get_llm_backend(config, backend)` |
| `HealthRegistry` | class | `modules/llm_pool.py:75` | `class HealthRegistry` |
| `LLMPool` | class | `modules/llm_pool.py:176` | `class LLMPool` |
| `PoolConfig` | class | `modules/llm_pool.py:29` | `class PoolConfig` |
| `PoolExhausted` | class | `modules/llm_pool.py:42` | `class PoolExhausted(RuntimeError)` |
| `PoolMember` | class | `modules/llm_pool.py:64` | `class PoolMember` |
| `__init__` | method | `modules/llm_pool.py:83` | `def __init__(self, config)` |
| `__init__` | method | `modules/llm_pool.py:179` | `def __init__(self, members, health, config)` |
| `_backoff_for` | method | `modules/llm_pool.py:155` | `def _backoff_for(self, failures)` |
| `_health_path` | function | `modules/llm_pool.py:20` | `def _health_path()` |
| `_load` | method | `modules/llm_pool.py:92` | `def _load(self)` |
| `_ordered` | method | `modules/llm_pool.py:201` | `def _ordered(self)` |
| `_persist_locked` | method | `modules/llm_pool.py:116` | `def _persist_locked(self)` |
| `_truncate` | method | `modules/llm_pool.py:217` | `def _truncate(self, text, overflow_dir)` |
| `complete` | method | `modules/llm_pool.py:237` | `def complete(self, prompt, max_tokens, session_key, overflow_dir)` |
| `healthy` | method | `modules/llm_pool.py:163` | `def healthy(self, member_id)` |
| `members` | method | `modules/llm_pool.py:192` | `def members(self)` |
| `report_failure` | method | `modules/llm_pool.py:143` | `def report_failure(self, member_id, error)` |
| `report_success` | method | `modules/llm_pool.py:135` | `def report_success(self, member_id)` |
| `session_key` | method | `modules/llm_pool.py:196` | `def session_key(self, conversation_id, role, index)` |
| `shared_registry` | function | `modules/llm_pool.py:50` | `def shared_registry(config)` |
| `KnowledgeStore` | class | `modules/llm_prompts.py:286` | `class KnowledgeStore` |
| `LlmPromptConfig` | class | `modules/llm_prompts.py:111` | `class LlmPromptConfig` |
| `__init__` | method | `modules/llm_prompts.py:289` | `def __init__(self, path)` |
| `_payload_block` | function | `modules/llm_prompts.py:354` | `def _payload_block(config)` |
| `_prompt_adversary` | function | `modules/llm_prompts.py:393` | `def _prompt_adversary(base_prompt, kb_text, config)` |
| `_prompt_general` | function | `modules/llm_prompts.py:409` | `def _prompt_general(base_prompt, kb_text, config)` |
| `_prompt_oneliner` | function | `modules/llm_prompts.py:362` | `def _prompt_oneliner(base_prompt, kb_text, config)` |
| `_prompt_redop` | function | `modules/llm_prompts.py:462` | `def _prompt_redop(base_prompt, kb_text, config)` |
| `_prompt_script` | function | `modules/llm_prompts.py:378` | `def _prompt_script(base_prompt, kb_text, config)` |
| `_prompt_search` | function | `modules/llm_prompts.py:422` | `def _prompt_search(base_prompt, kb_text, config)` |
| `_prompt_task` | function | `modules/llm_prompts.py:450` | `def _prompt_task(base_prompt, kb_text, config)` |
| `_prompt_vuln` | function | `modules/llm_prompts.py:436` | `def _prompt_vuln(base_prompt, kb_text, config)` |
| `add` | method | `modules/llm_prompts.py:324` | `def add(self, prompt, response)` |
| `default_project_root` | function | `modules/llm_prompts.py:67` | `def default_project_root()` |
| `from_defaults` | method | `modules/llm_prompts.py:130` | `def from_defaults(cls, project_root)` |
| `knowledge_base_path` | method | `modules/llm_prompts.py:150` | `def knowledge_base_path(self, domain)` |
| `knowledge_store` | method | `modules/llm_prompts.py:238` | `def knowledge_store(self, domain)` |
| `load` | method | `modules/llm_prompts.py:297` | `def load(self)` |
| `load_event_tool_output` | method | `modules/llm_prompts.py:176` | `def load_event_tool_output(self, event_name)` |
| `load_payload_context` | method | `modules/llm_prompts.py:161` | `def load_payload_context(self)` |
| `load_plan_history` | method | `modules/llm_prompts.py:203` | `def load_plan_history(self)` |
| `load_report_context` | method | `modules/llm_prompts.py:218` | `def load_report_context(self)` |
| `relevant` | method | `modules/llm_prompts.py:335` | `def relevant(self, prompt, limit)` |
| `render` | method | `modules/llm_prompts.py:249` | `def render(self, template, base_prompt)` |
| `render_kb_tail` | function | `modules/llm_prompts.py:271` | `def render_kb_tail(lines)` |
| `resolve_model` | function | `modules/llm_prompts.py:76` | `def resolve_model(model)` |
| `save` | method | `modules/llm_prompts.py:312` | `def save(self, records)` |
| `truncate_message` | function | `modules/llm_prompts.py:95` | `def truncate_message(message, max_chars)` |
| `LogTamper` | class | `modules/log_tamper.py:95` | `class LogTamper` |
| `LogTamperConfig` | class | `modules/log_tamper.py:71` | `class LogTamperConfig` |
| `__init__` | method | `modules/log_tamper.py:105` | `def __init__(self, config)` |
| `auditd_disable_commands` | method | `modules/log_tamper.py:307` | `def auditd_disable_commands(self)` |
| `generate_all` | method | `modules/log_tamper.py:295` | `def generate_all(self)` |
| `linux_clear_commands` | method | `modules/log_tamper.py:176` | `def linux_clear_commands(self)` |
| `macos_clear_commands` | method | `modules/log_tamper.py:243` | `def macos_clear_commands(self)` |
| `sysmon_disable_commands` | method | `modules/log_tamper.py:341` | `def sysmon_disable_commands(self)` |
| `windows_clear_commands` | method | `modules/log_tamper.py:108` | `def windows_clear_commands(self)` |
| `ColoredFormatter` | class | `modules/logging_config.py:36` | `class ColoredFormatter(Formatter)` |
| `CorrelationFilter` | class | `modules/logging_config.py:91` | `class CorrelationFilter(Filter)` |
| `JsonFormatter` | class | `modules/logging_config.py:53` | `class JsonFormatter(Formatter)` |

Next: [SYMBOLS_p18.md](SYMBOLS_p18.md)
