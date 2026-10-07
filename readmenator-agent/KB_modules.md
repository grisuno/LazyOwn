# Subsystem: modules (page 1 of 10)
Pages: [KB_modules.md](KB_modules.md), [KB_modules_p2.md](KB_modules_p2.md), [KB_modules_p3.md](KB_modules_p3.md), [KB_modules_p4.md](KB_modules_p4.md), [KB_modules_p5.md](KB_modules_p5.md), [KB_modules_p6.md](KB_modules_p6.md), [KB_modules_p7.md](KB_modules_p7.md), [KB_modules_p8.md](KB_modules_p8.md), [KB_modules_p9.md](KB_modules_p9.md), [KB_modules_p10.md](KB_modules_p10.md)

## modules/49803.py
- Doc: Exploit Title: OpenPLC 3 - Remote Code Execution (Authenticated) Date: 25/04/2021 Exploit...
- Layer: utility
- Language: py
- Symbols:
  - `auth` (function, line 42) `def auth()`
  - `injection` (function, line 70) `def injection()`
  - `connection` (function, line 84) `def connection()`

## modules/CVE-2018-15133.php
- Layer: utility
- Language: php

## modules/CVE-2023-28432.py
- Layer: utility
- Language: py
- Symbols:
  - `poc` (function, line 10) `def poc(url)`

## modules/LazyOwnExplorer.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `AutocompleteEntry` (class, line 29) `class AutocompleteEntry(Entry)`
  - `LazyOwnGUI` (class, line 101) `class LazyOwnGUI(Tk)`
  - `__init__` (method, line 30) `def __init__(self, get_suggestions_func)`
  - `changed` (method, line 44) `def changed(self, name, index, mode)`
  - `selection` (method, line 67) `def selection(self, event)`
  - `move_up` (method, line 74) `def move_up(self, event)`
  - `move_down` (method, line 86) `def move_down(self, event)`
  - `comparison` (method, line 98) `def comparison(self, pattern)`
  - `__init__` (method, line 102) `def __init__(self)`
  - `create_widgets` (method, line 116) `def create_widgets(self)`
  - `load_parquet_files` (method, line 176) `def load_parquet_files(self)`
  - `get_unique_values` (method, line 235) `def get_unique_values(self)`
  - `search` (method, line 242) `def search(self)`
  - `search_in_parquet` (method, line 259) `def search_in_parquet(self, term)`
  - `on_row_double_click` (method, line 268) `def on_row_double_click(self, event)`
  - `show_row_details` (method, line 273) `def show_row_details(self, row)`
  - `add_new_attack_vector` (method, line 295) `def add_new_attack_vector(self)`
  - `scan_system_for_binaries` (method, line 343) `def scan_system_for_binaries(self)`
  - `show_scan_results` (method, line 360) `def show_scan_results(self, binaries)`
  - `export_to_csv` (method, line 371) `def export_to_csv(self)`
  - `get_suggestions` (method, line 121) `def get_suggestions(term)`
  - `save_new_vector` (method, line 315) `def save_new_vector()`
  - `is_binary` (method, line 344) `def is_binary(file_path)`

## modules/__init__.py
- Layer: utility
- Language: py
- Imported by: `tests/test_security_sanitizers.py`

## modules/adcs_attacks.py
- Doc: Active Directory Certificate Services (AD CS) attack module.
- Layer: utility
- Language: py
- Symbols:
  - `CertificateTemplate` (class, line 14) `class CertificateTemplate`
  - `ADCSCertipyWrapper` (class, line 69) `class ADCSCertipyWrapper`
  - `esc_vulnerabilities` (method, line 35) `def esc_vulnerabilities(self)`
  - `__init__` (method, line 80) `def __init__(self, certipy_path, timeout)`
  - `_find_certipy` (method, line 85) `def _find_certipy()`
  - `_run` (method, line 95) `def _run(self, args, capture)`
  - `find_certificate_authorities` (method, line 115) `def find_certificate_authorities(self, username, password, domain, dc_ip, hashes)`
  - `_parse_ca_output` (method, line 155) `def _parse_ca_output(output)`
  - `enumerate_templates` (method, line 187) `def enumerate_templates(self, username, password, domain, dc_ip, hashes)`
  - `_parse_template_output` (method, line 226) `def _parse_template_output(self, output)`
  - `request_certificate_esc1` (method, line 271) `def request_certificate_esc1(self, username, password, domain, dc_ip, ca_name, template_name, target_user, output_file)`
  - `request_certificate_esc8` (method, line 320) `def request_certificate_esc8(self, username, password, domain, dc_ip, ca_server, template_name, output_file)`
  - `authenticate_with_certificate` (method, line 361) `def authenticate_with_certificate(self, cert_file, domain, dc_ip, username)`
  - `assess_vulnerability` (method, line 400) `def assess_vulnerability(self, username, password, domain, dc_ip, hashes)`
- Imported by: `cli/commands/exploit_migrated.py`

## modules/agent_runner.py
- Doc: LazyOwn AI Agent - Ultimate Edition Mejoras: Anti-Hang (Timeout), Gestión de Memoria, Validación...
- Layer: utility
- Language: py
- Symbols:
  - `configure_logging` (function, line 58) `def configure_logging(debug)`
  - `AgentTool` (class, line 63) `class AgentTool`
  - `CommandMetadata` (class, line 129) `class CommandMetadata`
  - `ASTToolExtractor` (class, line 135) `class ASTToolExtractor`
  - `AgentRunner` (class, line 177) `class AgentRunner`
  - `LazyOwnShellWrapper` (class, line 357) `class LazyOwnShellWrapper`
  - `VulnBotCLI` (class, line 434) `class VulnBotCLI`
  - `interactive_mode` (method, line 499) `def interactive_mode(bot)`
  - `parse_args` (method, line 522) `def parse_args()`
  - `main` (method, line 531) `def main()`
  - `__init__` (method, line 66) `def __init__(self, name, description, func, parameters, required)`
  - `to_api_format` (method, line 77) `def to_api_format(self)`
  - `execute` (method, line 87) `def execute(self)`
  - `extract_commands_from_file` (method, line 139) `def extract_commands_from_file(file_path, prefix)`
  - `__init__` (method, line 180) `def __init__(self, model, system_prompt, max_iterations)`
  - `_reset_history` (method, line 194) `def _reset_history(self)`
  - `_manage_memory` (method, line 200) `def _manage_memory(self)`
  - `register_tool` (method, line 208) `def register_tool(self, tool)`
  - `register_tool_from_instance` (method, line 211) `def register_tool_from_instance(self, func)`
  - `register_tools_from_metadata` (method, line 229) `def register_tools_from_metadata(self, commands, executor)`
  - `get_tools_for_api` (method, line 254) `def get_tools_for_api(self)`
  - `run` (method, line 259) `def run(self, user_input)`
  - `_call_model` (method, line 283) `def _call_model(self)`
  - `_process_tool_call` (method, line 306) `def _process_tool_call(self, tool_call)`
  - `__init__` (method, line 360) `def __init__(self, script_path)`
  - `_load_shell` (method, line 367) `def _load_shell(self)`
  - `execute_command` (method, line 390) `def execute_command(self, command)`
  - `get_commands_summary` (method, line 427) `def get_commands_summary(self)`
  - `__init__` (method, line 436) `def __init__(self, provider, mode, debug, script_path)`
  - `_load_model` (method, line 448) `def _load_model(self)`
  - `_setup_agent` (method, line 463) `def _setup_agent(self)`
  - `process_request` (method, line 494) `def process_request(self, user_input)`
  - `target` (method, line 397) `def target()`
  - `make_executor` (method, line 232) `def make_executor(cmd_name)`
  - `wrapper` (method, line 233) `def wrapper(command)`
- Depends on: `core/logging.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
- Imported by: `modules/vuln_agent.py`, `modules/vulnbot.py`

## modules/agent_tool.py
- Doc: AgentTool: Representa una herramienta ejecutable por el agente
- Layer: utility
- Language: py
- Symbols:
  - `AgentTool` (class, line 7) `class AgentTool`
  - `__init__` (method, line 10) `def __init__(self, name, description, func, parameters, required)`
  - `to_api_format` (method, line 21) `def to_api_format(self)`
  - `execute` (method, line 32) `def execute(self)`
- Depends on: `core/logging.py`
- Imported by: `modules/tool_extractor.py`, `modules/vuln_agent.py`

## modules/ai_exploit_chain.py
- Doc: AI-Driven Exploit Chaining Engine.
- Layer: utility
- Language: py
- Symbols:
  - `ExploitChainContext` (class, line 154) `class ExploitChainContext`
  - `AIExploitChainer` (class, line 178) `class AIExploitChainer`
  - `__init__` (method, line 190) `def __init__(self)`
  - `reason` (method, line 203) `def reason(self, context)`
  - `evaluate_failure` (method, line 223) `def evaluate_failure(result)`
  - `select_next_strategy` (method, line 235) `def select_next_strategy(self, context)`
  - `estimate_confidence` (method, line 269) `def estimate_confidence(self, strategy, profile)`
  - `build_chain_plan` (method, line 311) `def build_chain_plan(self, context)`
  - `adapt_chain` (method, line 344) `def adapt_chain(self, context, new_info)`
  - `_ensure` (method, line 400) `def _ensure(context, strategy)`
  - `_parse_shell_hints` (method, line 405) `def _parse_shell_hints(self, output, context)`
- Depends on: `modules/autonomous_exploit_engine.py`
- Imported by: `cli/commands/pwn.py`, `skills/lazyown_mcp.py`

## modules/ai_fallback.py
- Doc: LazyOwn AI Fallback Chain
- Layer: utility
- Language: py
- Symbols:
  - `AIResult` (class, line 89) `class AIResult`
  - `_ollama_available` (method, line 99) `def _ollama_available()`
  - `_best_ollama_model` (method, line 107) `def _best_ollama_model()`
  - `_ollama_call` (method, line 134) `def _ollama_call(model, system, user, max_tokens, temperature)`
  - `_is_quota_error` (method, line 178) `def _is_quota_error(exc)`
  - `_groq_call` (method, line 183) `def _groq_call(api_key, system, user, max_tokens, temperature)`
  - `_toposwarm_call` (method, line 210) `def _toposwarm_call(prompt, system)`
  - `call` (method, line 238) `def call(prompt, system, api_key, max_tokens, temperature)`
- Depends on: `modules/llm_factory.py`, `modules/toposwarm_bridge.py`
- Imported by: `modules/recommender.py`, `modules/timeline_narrator.py`

## modules/ai_model.py
- Doc: Concrete language model backends for LazyOwn.
- Layer: business_logic
- Language: py
- Symbols:
  - `AIModel` (class, line 41) `class AIModel(ABC)`
  - `_LazyImporter` (class, line 93) `class _LazyImporter`
  - `GroqModel` (class, line 122) `class GroqModel(AIModel)`
  - `OllamaModel` (class, line 202) `class OllamaModel(AIModel)`
  - `OpenAIModel` (class, line 269) `class OpenAIModel(AIModel)`
  - `AnthropicModel` (class, line 328) `class AnthropicModel(AIModel)`
  - `DeepSeekModel` (class, line 384) `class DeepSeekModel(AIModel)`
  - `generate` (method, line 52) `def generate(self, prompt)`
  - `stream_generate` (method, line 56) `def stream_generate(self, prompt)`
  - `complete` (method, line 59) `def complete(self, system, user, max_tokens, temperature)`
  - `groq` (method, line 101) `def groq(cls)`
  - `openai` (method, line 108) `def openai(cls)`
  - `anthropic` (method, line 115) `def anthropic(cls)`
  - `__init__` (method, line 130) `def __init__(self, api_key, model)`
  - `generate` (method, line 134) `def generate(self, prompt)`
  - `stream_generate` (method, line 152) `def stream_generate(self, prompt)`
  - `complete` (method, line 174) `def complete(self, system, user, max_tokens, temperature)`
  - `__init__` (method, line 210) `def __init__(self, model, host)`
  - `generate` (method, line 218) `def generate(self, prompt)`
  - `stream_generate` (method, line 238) `def stream_generate(self, prompt)`
  - `__init__` (method, line 275) `def __init__(self, api_key, model)`
  - `generate` (method, line 279) `def generate(self, prompt)`
  - `stream_generate` (method, line 290) `def stream_generate(self, prompt)`
  - `complete` (method, line 305) `def complete(self, system, user, max_tokens, temperature)`
  - `__init__` (method, line 334) `def __init__(self, api_key, model)`
  - `generate` (method, line 338) `def generate(self, prompt)`
  - `stream_generate` (method, line 350) `def stream_generate(self, prompt)`
  - `complete` (method, line 364) `def complete(self, system, user, max_tokens, temperature)`
  - `__init__` (method, line 391) `def __init__(self, api_key, model)`
  - `generate` (method, line 398) `def generate(self, prompt)`
  - `stream_generate` (method, line 409) `def stream_generate(self, prompt)`
  - `complete` (method, line 424) `def complete(self, system, user, max_tokens, temperature)`
- Depends on: `core/logging.py`
- Imported by: `contrib/legacy/lazyllmchat.py`, `modules/agent_runner.py`, `modules/llm_factory.py`, `modules/vuln_agent.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`

## modules/amsi.c
- Doc: ¡Gracias a Saad!
- Layer: utility
- Language: c
- Symbols:
  - `LoadNtFunctions` (function, line 38) `void LoadNtFunctions()`
  - `AMS1patch_OpenSession_jne` (function, line 66) `void AMS1patch_OpenSession_jne(HANDLE hproc)`
  - `AMS1patch_OpenSession_ret` (function, line 116) `void AMS1patch_OpenSession_ret(HANDLE hproc)`
  - `AMS1patch_ScanBuffer_ret` (function, line 166) `void AMS1patch_ScanBuffer_ret(HANDLE hproc)`
  - `AMS1patch_RastaMouse` (function, line 215) `void AMS1patch_RastaMouse(HANDLE hproc)`
  - `AMS1patch_E_ACCESSDENIED` (function, line 274) `void AMS1patch_E_ACCESSDENIED(HANDLE hproc)`
  - `AMS1patch_E_HANDLE` (function, line 326) `void AMS1patch_E_HANDLE(HANDLE hproc)`
  - `AMS1patch_E_OUTOFMEMORY` (function, line 378) `void AMS1patch_E_OUTOFMEMORY(HANDLE hproc)`
  - `main` (function, line 428) `int main(int argc, char** argv)`
  - `NT_SUCCESS` (macro, line 11) `#define NT_SUCCESS(Status)`

## modules/amt_auth_bypass.py
- Layer: utility
- Language: py
- Symbols:
  - `start` (function, line 4) `def start()`
  - `BlankAuthResponse` (class, line 8) `class BlankAuthResponse`
  - `request` (method, line 12) `def request(self, flow)`

## modules/apt_playbooks.py
- Doc: APT Playbook Engine — map public APT reports to executable Atomic Red Team chains.
- Layer: utility
- Language: py
- Symbols:
  - `AtomicTestRef` (class, line 41) `class AtomicTestRef`
  - `CalderaAbilityRef` (class, line 48) `class CalderaAbilityRef`
  - `PhaseStep` (class, line 54) `class PhaseStep`
  - `AptPlaybook` (class, line 65) `class AptPlaybook`
  - `AptPlaybookEngine` (class, line 113) `class AptPlaybookEngine`
  - `from_dict` (method, line 74) `def from_dict(cls, data)`
  - `to_summary` (method, line 101) `def to_summary(self)`
  - `__init__` (method, line 116) `def __init__(self, playbook_dir)`
  - `_load_all` (method, line 121) `def _load_all(self)`
  - `list_playbooks` (method, line 133) `def list_playbooks(self)`
  - `get` (method, line 136) `def get(self, name)`
  - `validate` (method, line 140) `def validate(self, pb, atomic_path)`
  - `_build_atomic_index` (method, line 173) `def _build_atomic_index(self, atomic_yaml_path)`
  - `generate_attack_plan` (method, line 187) `def generate_attack_plan(self, pb, output_path)`
  - `report_json` (method, line 202) `def report_json(self, pb, output_path)`
- Depends on: `core/console.py`
- Imported by: `cli/commands/command_and_control_migrated.py`, `cli/recommendation_signals.py`, `modules/operation.py`

## modules/atomic_enricher.py
- Doc: — Enrich techniques.parquet with structured derived columns.
- Layer: utility
- Language: py
- Symbols:
  - `_parse_platforms` (function, line 63) `def _parse_platforms(raw)`
  - `_parse_scope` (function, line 76) `def _parse_scope(name)`
  - `_parse_complexity` (function, line 83) `def _parse_complexity(command)`
  - `_parse_keyword_tags` (function, line 93) `def _parse_keyword_tags(name, description)`
  - `_tactic_prefix` (function, line 105) `def _tactic_prefix(mitre_id)`
  - `enrich` (function, line 113) `def enrich(force)`
  - `_to_pylist` (function, line 148) `def _to_pylist(val)`
  - `load_enriched` (function, line 159) `def load_enriched()`
  - `query_atomic` (function, line 175) `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)`
- Depends on: `core/logging.py`
- Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `tests/test_core_modules.py`

## modules/auto_pivot.py
- Doc: Auto-Pivoting Engine for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `PivotNode` (class, line 23) `class PivotNode`
  - `PivotChain` (class, line 39) `class PivotChain`
  - `AutoPivotEngine` (class, line 47) `class AutoPivotEngine`
  - `__init__` (method, line 73) `def __init__(self, config)`
  - `set_config` (method, line 82) `def set_config(self, config)`
  - `_next_port` (method, line 85) `def _next_port(self)`
  - `add_pivot_node` (method, line 90) `def add_pivot_node(self, ip, access_type, credential_id, hostname)`
  - `remove_pivot_node` (method, line 120) `def remove_pivot_node(self, ip)`
  - `discover_subnets` (method, line 128) `def discover_subnets(self, node_ip, command_output)`
  - `build_chain` (method, line 145) `def build_chain(self, target_ip, via_nodes, subnet)`
  - `generate_proxychains_config` (method, line 175) `def generate_proxychains_config(self, chain_id)`
  - `generate_sshuttle_command` (method, line 203) `def generate_sshuttle_command(self, node_ip, subnet)`
  - `generate_chisel_command` (method, line 206) `def generate_chisel_command(self, target_ip, local_port)`
  - `generate_ssh_socks_command` (method, line 214) `def generate_ssh_socks_command(self, node_ip, local_port)`
  - `health_check` (method, line 218) `def health_check(self, node_ip)`
  - `health_check_all` (method, line 239) `def health_check_all(self)`
  - `get_active_routes` (method, line 245) `def get_active_routes(self)`
  - `get_reachable_hosts` (method, line 259) `def get_reachable_hosts(self, node_ip)`
  - `set_reachable_hosts` (method, line 267) `def set_reachable_hosts(self, node_ip, hosts)`
  - `set_route_priority` (method, line 272) `def set_route_priority(self, node_ip, priority)`
  - `_persist_state` (method, line 277) `def _persist_state(self)`
  - `_load_state` (method, line 314) `def _load_state(self)`
  - `suggest_next_pivot` (method, line 357) `def suggest_next_pivot(self)`
- Imported by: `modules/autonomous_exploit_engine.py`, `skills/lazyown_mcp.py`

## modules/auto_purple.py
- Doc: Purple Team Closed-Loop — honest measurement of offensive detection.
- Layer: utility
- Language: py
- Symbols:
  - `DetectionMethod` (class, line 65) `class DetectionMethod`
  - `PurpleResult` (class, line 124) `class PurpleResult`
  - `PurpleScore` (class, line 156) `class PurpleScore`
  - `IPurpleLoop` (class, line 171) `class IPurpleLoop(ABC)`
  - `IPurpleEvaluator` (class, line 194) `class IPurpleEvaluator(ABC)`
  - `_run_bt_command` (method, line 209) `def _run_bt_command(bt_path, command, timeout)`
  - `_parse_ai_test` (method, line 313) `def _parse_ai_test(output, command, args)`
  - `_parse_keyword_match` (method, line 326) `def _parse_keyword_match(output, command, args)`
  - `_parse_alert_check` (method, line 348) `def _parse_alert_check(output, command, args)`
  - `_parse_fim_check` (method, line 362) `def _parse_fim_check(output, command, args)`
  - `PurpleTeamLoop` (class, line 381) `class PurpleTeamLoop(IPurpleLoop, IPurpleEvaluator)`
  - `get_loop` (method, line 742) `def get_loop(bt_path, detection_delay, methods, auto_feedback)`
  - `load_config_from_payload` (method, line 760) `def load_config_from_payload(params)`
  - `to_csv_row` (method, line 137) `def to_csv_row(self)`
  - `to_dict` (method, line 151) `def to_dict(self)`
  - `execute_and_measure` (method, line 175) `def execute_and_measure(self, command, args, category)`
  - `measure_only` (method, line 180) `def measure_only(self, command, args, category)`
  - `engagement_score` (method, line 185) `def engagement_score(self)`
  - `export_dataset` (method, line 188) `def export_dataset(self)`
  - `export_report` (method, line 191) `def export_report(self)`
  - `last_results` (method, line 198) `def last_results(self, n)`
  - `category_accuracy` (method, line 201) `def category_accuracy(self, category)`
  - `__init__` (method, line 388) `def __init__(self, bt_path, detection_delay, methods, auto_feedback, session_id)`
  - `_init_dataset` (method, line 407) `def _init_dataset(self)`
  - `execute_and_measure` (method, line 417) `def execute_and_measure(self, command, args, category)`
  - `measure_only` (method, line 462) `def measure_only(self, command, args, category)`
  - `engagement_score` (method, line 495) `def engagement_score(self)`
  - `export_dataset` (method, line 533) `def export_dataset(self)`
  - `export_report` (method, line 537) `def export_report(self)`
  - `last_results` (method, line 562) `def last_results(self, n)`
  - `category_accuracy` (method, line 565) `def category_accuracy(self, category)`
  - `_execute_red` (method, line 580) `def _execute_red(self, command, args)`
  - `_query_blue` (method, line 599) `def _query_blue(self, command, args)`
  - `_hash_output` (method, line 647) `def _hash_output(self, output)`
  - `_write_audit` (method, line 652) `def _write_audit(self, result)`
  - `_append_dataset` (method, line 657) `def _append_dataset(self, result)`
  - `_write_feedback` (method, line 663) `def _write_feedback(self, result)`
  - `_load_audit` (method, line 683) `def _load_audit(self)`
  - `_compute_oracle_accuracy` (method, line 700) `def _compute_oracle_accuracy(self)`
  - `_get_detection_methods` (method, line 726) `def _get_detection_methods(self)`
- Depends on: `core/config.py`, `core/logging.py`, `core/process.py`, `modules/detection_oracle.py`
- Imported by: `cli/commands/purple_team.py`

## modules/autonomous_exploit_engine.py
- Doc: Autonomous Exploitation Engine — AI-powered self-adapting exploit chainer.
- Layer: utility
- Language: py
- Symbols:
  - `TargetProfile` (class, line 58) `class TargetProfile`
  - `ExploitCandidate` (class, line 73) `class ExploitCandidate`
  - `ExploitResult` (class, line 88) `class ExploitResult`
  - `AutonomousExploitEngine` (class, line 100) `class AutonomousExploitEngine`
  - `__init__` (method, line 113) `def __init__(self)`
  - `get_instance` (method, line 133) `def get_instance(cls)`
  - `hunt` (method, line 144) `def hunt(self, target, max_exploits)`
  - `retry_with_credentials` (method, line 181) `def retry_with_credentials(self, target, credentials)`
  - `_credential_aware_rank` (method, line 238) `def _credential_aware_rank(self, profile, credentials)`
  - `_filter_placeholder_creds` (method, line 285) `def _filter_placeholder_creds(credentials)`
  - `profile` (method, line 318) `def profile(self, target)`
  - `rank_exploits` (method, line 375) `def rank_exploits(self, profile)`
  - `execute_candidate` (method, line 402) `def execute_candidate(self, candidate, profile)`
  - `_match_exploit_db` (method, line 446) `def _match_exploit_db(self, service, product, version)`
  - `_heuristic_match` (method, line 486) `def _heuristic_match(self, service, product, version)`
  - `_match_by_port` (method, line 958) `def _match_by_port(self, port, os_type)`
  - `_scorer` (method, line 1017) `def _scorer(self, exploit, service, product, version)`
  - `_run_exploit` (method, line 1057) `def _run_exploit(self, candidate, profile)`
  - `_resolve_port` (method, line 1085) `def _resolve_port(self, candidate, profile)`
  - `_build_command_chain` (method, line 1104) `def _build_command_chain(self, candidate, profile)`
  - `_check_success` (method, line 1240) `def _check_success(self, output, candidate)`
  - `_detect_shell` (method, line 1301) `def _detect_shell(self, output)`
  - `_determine_access_level` (method, line 1329) `def _determine_access_level(self, ip, credentials)`
  - `_register_session` (method, line 1361) `def _register_session(self, ip, output)`
  - `_load_payload_config` (method, line 1389) `def _load_payload_config(self)`
  - `_load_world_model` (method, line 1400) `def _load_world_model(self, target)`
  - `_detect_os_from_payload` (method, line 1491) `def _detect_os_from_payload(self)`
  - `_load_from_nmap_xml` (method, line 1509) `def _load_from_nmap_xml(self, target)`
  - `_get_os_type` (method, line 1584) `def _get_os_type(self, profile)`
  - `_apply_stealth_delay` (method, line 1600) `def _apply_stealth_delay(self)`
  - `scan_vulnerabilities` (method, line 1611) `def scan_vulnerabilities(self, profile)`
  - `_parse_nse_output` (method, line 1637) `def _parse_nse_output(self, target_ip)`
  - `_extract_cves_from_text` (method, line 1672) `def _extract_cves_from_text(self, text)`
  - `_match_service_banners` (method, line 1720) `def _match_service_banners(self, profile)`
  - `_check_known_cves` (method, line 1894) `def _check_known_cves(self, profile)`
  - `chain_privesc` (method, line 1918) `def chain_privesc(self, profile, session_id)`
  - `_run_linux_privesc_checks` (method, line 1948) `def _run_linux_privesc_checks(self, profile, session_id)`
  - `_run_windows_privesc_checks` (method, line 2016) `def _run_windows_privesc_checks(self, profile, session_id)`
  - `_match_privesc_techniques` (method, line 2058) `def _match_privesc_techniques(self, findings, os_type)`
  - `_execute_privesc` (method, line 2209) `def _execute_privesc(self, technique, profile, session_id)`
  - `trigger_pivot` (method, line 2306) `def trigger_pivot(self, profile, session_id)`
  - `_discover_internal_interfaces` (method, line 2375) `def _discover_internal_interfaces(self, profile)`
  - `enable_stealth` (method, line 2435) `def enable_stealth(self, stealth_level)`
  - `_get_stealth_scan_flags` (method, line 2480) `def _get_stealth_scan_flags(self)`
  - `full_auto_pwn` (method, line 2499) `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth)`
  - `_is_placeholder` (method, line 290) `def _is_placeholder(value)`
- Depends on: `core/safe_exec.py`, `modules/auto_pivot.py`, `modules/db.py`
- Imported by: `cli/commands/pwn.py`, `cli/commands/session_ops.py`, `modules/ai_exploit_chain.py`, `skills/lazyown_mcp.py`, `tests/test_phase1_data_gaps.py`

## modules/aws_attacks.py
- Doc: AWS privilege escalation — IAM enumeration, Lambda backdoors, STS role chaining.
- Layer: utility
- Language: py
- Symbols:
  - `AWSConfig` (class, line 57) `class AWSConfig`
  - `AWSAttackEngine` (class, line 79) `class AWSAttackEngine`
  - `__init__` (method, line 90) `def __init__(self, config)`
  - `enumerate_iam_permissions` (method, line 94) `def enumerate_iam_permissions(self)`
  - `lambda_backdoor` (method, line 126) `def lambda_backdoor(self, function_name)`
  - `sts_role_chain` (method, line 154) `def sts_role_chain(self, target_role_arn)`
  - `ec2_user_data_exfil` (method, line 180) `def ec2_user_data_exfil(self)`
  - `s3_enumeration` (method, line 205) `def s3_enumeration(self)`
  - `cloudformation_drift` (method, line 234) `def cloudformation_drift(self)`
  - `ec2_ssm_session_abuse` (method, line 263) `def ec2_ssm_session_abuse(self)`
  - `summary` (method, line 282) `def summary(self)`
- Imported by: `cli/commands/cloud_attacks.py`

## modules/beacon_config_builder.py
- Doc: Beacon configuration builder — wires profile engines into beacon compile-time config.
- Layer: infrastructure
- Language: py
- Symbols:
  - `BeaconConfig` (class, line 44) `class BeaconConfig`
  - `BeaconConfigBuilder` (class, line 239) `class BeaconConfigBuilder`
  - `generate_bof_execution_command` (method, line 414) `def generate_bof_execution_command(bof_name, c2_url, client_id, args, bofs_dir)`
  - `to_gen_beacon_args` (method, line 119) `def to_gen_beacon_args(self)`
  - `to_go_implant_vars` (method, line 139) `def to_go_implant_vars(self)`
  - `to_config_json` (method, line 162) `def to_config_json(self)`
  - `to_dict` (method, line 187) `def to_dict(self)`
  - `__init__` (method, line 247) `def __init__(self, payload)`
  - `build` (method, line 250) `def build(self, name)`
  - `_inject_profile_engine` (method, line 319) `def _inject_profile_engine(self, config)`
  - `_inject_sleep_engine` (method, line 365) `def _inject_sleep_engine(self, config)`
  - `_inject_socks_engine` (method, line 384) `def _inject_socks_engine(self, config)`
  - `from_payload` (method, line 402) `def from_payload(cls, payload)`
  - `from_payload_file` (method, line 407) `def from_payload_file(cls, path)`
- Depends on: `core/config.py`, `core/logging.py`, `modules/c2_profile_engine.py`, `modules/sleep_obfuscation.py`, `modules/socks_proxy.py`
- Imported by: `cli/commands/bof_registry.py`, `tests/test_beacon_config_builder.py`

## modules/beacon_history.py
- Doc: Persistent beacon command/result history storage.
- Layer: utility
- Language: py
- Symbols:
  - `BeaconHistoryConfig` (class, line 28) `class BeaconHistoryConfig`
  - `sanitize_client_id` (method, line 70) `def sanitize_client_id(client_id)`
  - `append_record` (method, line 82) `def append_record(record, config)`
  - `read_records` (method, line 116) `def read_records(client_id, config)`
  - `records_path` (method, line 145) `def records_path(client_id, config)`
  - `sessions_dir` (method, line 39) `def sessions_dir(self)`
  - `records_path` (method, line 43) `def records_path(self, client_id)`
- Depends on: `core/logging.py`
- Imported by: `lazyc2.py`, `lazyc2/blueprints/api_v1.py`, `tests/test_api_v1.py`, `tests/test_beacon_history.py`, `tests/test_security_lazyc2.py`

## modules/bin2img.py
- Layer: utility
- Language: py
- Symbols:
  - `binario_a_imagen` (function, line 7) `def binario_a_imagen(binario, imagen_input, imagen_output, block_size)`
  - `main` (function, line 53) `def main()`

## modules/bitm_engine.py
- Doc: Browser-in-the-Middle (BitM) attack engine.
- Layer: utility
- Language: py
- Symbols:
  - `BitMState` (class, line 85) `class BitMState`
  - `_ensure_bitm_dir` (method, line 103) `def _ensure_bitm_dir()`
  - `_save_state` (method, line 108) `def _save_state(state)`
  - `_load_state` (method, line 134) `def _load_state()`
  - `_build_js_payload` (method, line 151) `def _build_js_payload(payload_name, lhost, lport)`
  - `_check_tool` (method, line 168) `def _check_tool(tool)`
  - `_recommend_method` (method, line 180) `def _recommend_method()`
  - `_get_default_interface` (method, line 195) `def _get_default_interface()`
  - `_get_gateway_ip` (method, line 234) `def _get_gateway_ip()`
  - `bitm_start` (method, line 257) `def bitm_start(target_ip, gateway_ip, interface, lhost, lport, method, payloads)`
  - `_start_bettercap` (method, line 354) `def _start_bettercap(target_ip, gateway_ip, interface, lhost, lport, js_payload, harvest_path)`
  - `_start_arpspoof` (method, line 413) `def _start_arpspoof(target_ip, gateway_ip, interface, lhost, lport, js_payload, harvest_path)`
  - `bitm_stop` (method, line 470) `def bitm_stop()`
  - `bitm_status` (method, line 528) `def bitm_status()`
  - `bitm_inject` (method, line 561) `def bitm_inject(payload_name)`
  - `bitm_harvest_stats` (method, line 593) `def bitm_harvest_stats()`
  - `bitm_cleanup` (method, line 628) `def bitm_cleanup()`
  - `main` (method, line 647) `def main()`
- Imported by: `cli/commands/bitm.py`


Next: [KB_modules_p2.md](KB_modules_p2.md)
