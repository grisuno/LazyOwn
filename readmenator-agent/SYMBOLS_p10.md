# Symbols (page 10 of 38)
Previous: [SYMBOLS_p9.md](SYMBOLS_p9.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `scan_system_for_binaries` | method | `modules/LazyOwnExplorer.py:357` | `def scan_system_for_binaries(self)` |
| `search` | method | `modules/LazyOwnExplorer.py:248` | `def search(self)` |
| `search_in_parquet` | method | `modules/LazyOwnExplorer.py:267` | `def search_in_parquet(self, term)` |
| `selection` | method | `modules/LazyOwnExplorer.py:68` | `def selection(self, event)` |
| `show_row_details` | method | `modules/LazyOwnExplorer.py:283` | `def show_row_details(self, row)` |
| `show_scan_results` | method | `modules/LazyOwnExplorer.py:374` | `def show_scan_results(self, binaries)` |
| `ADCSCertipyWrapper` | class | `modules/adcs_attacks.py:69` | `class ADCSCertipyWrapper` |
| `CertificateTemplate` | class | `modules/adcs_attacks.py:14` | `class CertificateTemplate` |
| `__init__` | method | `modules/adcs_attacks.py:80` | `def __init__(self, certipy_path, timeout)` |
| `_find_certipy` | method | `modules/adcs_attacks.py:85` | `def _find_certipy()` |
| `_parse_ca_output` | method | `modules/adcs_attacks.py:157` | `def _parse_ca_output(output)` |
| `_parse_template_output` | method | `modules/adcs_attacks.py:232` | `def _parse_template_output(self, output)` |
| `_run` | method | `modules/adcs_attacks.py:93` | `def _run(self, args, capture)` |
| `assess_vulnerability` | method | `modules/adcs_attacks.py:411` | `def assess_vulnerability(self, username, password, domain, dc_ip, hashes)` |
| `authenticate_with_certificate` | method | `modules/adcs_attacks.py:367` | `def authenticate_with_certificate(self, cert_file, domain, dc_ip, username)` |
| `enumerate_templates` | method | `modules/adcs_attacks.py:189` | `def enumerate_templates(self, username, password, domain, dc_ip, hashes)` |
| `esc_vulnerabilities` | method | `modules/adcs_attacks.py:35` | `def esc_vulnerabilities(self)` |
| `find_certificate_authorities` | method | `modules/adcs_attacks.py:113` | `def find_certificate_authorities(self, username, password, domain, dc_ip, hashes)` |
| `request_certificate_esc1` | method | `modules/adcs_attacks.py:268` | `def request_certificate_esc1(self, username, password, domain, dc_ip, ca_name, template_name, target_user, output_file)` |
| `request_certificate_esc8` | method | `modules/adcs_attacks.py:322` | `def request_certificate_esc8(self, username, password, domain, dc_ip, ca_server, template_name, output_file)` |
| `ASTToolExtractor` | class | `modules/agent_runner.py:133` | `class ASTToolExtractor` |
| `AgentRunner` | class | `modules/agent_runner.py:172` | `class AgentRunner` |
| `AgentTool` | class | `modules/agent_runner.py:65` | `class AgentTool` |
| `CommandMetadata` | class | `modules/agent_runner.py:126` | `class CommandMetadata` |
| `LazyOwnShellWrapper` | class | `modules/agent_runner.py:347` | `class LazyOwnShellWrapper` |
| `VulnBotCLI` | class | `modules/agent_runner.py:424` | `class VulnBotCLI` |
| `__init__` | method | `modules/agent_runner.py:68` | `def __init__(self, name, description, func, parameters, required)` |
| `__init__` | method | `modules/agent_runner.py:175` | `def __init__(self, model, system_prompt, max_iterations)` |
| `__init__` | method | `modules/agent_runner.py:350` | `def __init__(self, script_path)` |
| `__init__` | method | `modules/agent_runner.py:425` | `def __init__(self, provider, mode, debug, script_path)` |
| `_call_model` | method | `modules/agent_runner.py:277` | `def _call_model(self)` |
| `_load_model` | method | `modules/agent_runner.py:437` | `def _load_model(self)` |
| `_load_shell` | method | `modules/agent_runner.py:357` | `def _load_shell(self)` |
| `_manage_memory` | method | `modules/agent_runner.py:192` | `def _manage_memory(self)` |
| `_process_tool_call` | method | `modules/agent_runner.py:302` | `def _process_tool_call(self, tool_call)` |
| `_reset_history` | method | `modules/agent_runner.py:189` | `def _reset_history(self)` |
| `_setup_agent` | method | `modules/agent_runner.py:452` | `def _setup_agent(self)` |
| `configure_logging` | function | `modules/agent_runner.py:59` | `def configure_logging(debug)` |
| `execute` | method | `modules/agent_runner.py:82` | `def execute(self)` |
| `execute_command` | method | `modules/agent_runner.py:380` | `def execute_command(self, command)` |
| `extract_commands_from_file` | method | `modules/agent_runner.py:137` | `def extract_commands_from_file(file_path, prefix)` |
| `get_commands_summary` | method | `modules/agent_runner.py:417` | `def get_commands_summary(self)` |
| `get_tools_for_api` | method | `modules/agent_runner.py:248` | `def get_tools_for_api(self)` |
| `interactive_mode` | method | `modules/agent_runner.py:485` | `def interactive_mode(bot)` |
| `main` | method | `modules/agent_runner.py:519` | `def main()` |
| `make_executor` | method | `modules/agent_runner.py:225` | `def make_executor(cmd_name)` |
| `parse_args` | method | `modules/agent_runner.py:509` | `def parse_args()` |
| `process_request` | method | `modules/agent_runner.py:480` | `def process_request(self, user_input)` |
| `register_tool` | method | `modules/agent_runner.py:200` | `def register_tool(self, tool)` |
| `register_tool_from_instance` | method | `modules/agent_runner.py:203` | `def register_tool_from_instance(self, func)` |
| `register_tools_from_metadata` | method | `modules/agent_runner.py:221` | `def register_tools_from_metadata(self, commands, executor)` |
| `run` | method | `modules/agent_runner.py:253` | `def run(self, user_input)` |
| `target` | method | `modules/agent_runner.py:387` | `def target()` |
| `to_api_format` | method | `modules/agent_runner.py:76` | `def to_api_format(self)` |
| `wrapper` | method | `modules/agent_runner.py:226` | `def wrapper(command)` |
| `AgentTool` | class | `modules/agent_tool.py:7` | `class AgentTool` |
| `__init__` | method | `modules/agent_tool.py:10` | `def __init__(self, name, description, func, parameters, required)` |
| `execute` | method | `modules/agent_tool.py:25` | `def execute(self)` |
| `to_api_format` | method | `modules/agent_tool.py:18` | `def to_api_format(self)` |
| `AIExploitChainer` | class | `modules/ai_exploit_chain.py:247` | `class AIExploitChainer` |
| `ExploitChainContext` | class | `modules/ai_exploit_chain.py:223` | `class ExploitChainContext` |
| `__init__` | method | `modules/ai_exploit_chain.py:259` | `def __init__(self)` |
| `_ensure` | method | `modules/ai_exploit_chain.py:487` | `def _ensure(context, strategy)` |
| `_parse_shell_hints` | method | `modules/ai_exploit_chain.py:492` | `def _parse_shell_hints(self, output, context)` |
| `adapt_chain` | method | `modules/ai_exploit_chain.py:428` | `def adapt_chain(self, context, new_info)` |
| `build_chain_plan` | method | `modules/ai_exploit_chain.py:391` | `def build_chain_plan(self, context)` |
| `estimate_confidence` | method | `modules/ai_exploit_chain.py:349` | `def estimate_confidence(self, strategy, profile)` |
| `evaluate_failure` | method | `modules/ai_exploit_chain.py:306` | `def evaluate_failure(result)` |
| `reason` | method | `modules/ai_exploit_chain.py:285` | `def reason(self, context)` |
| `select_next_strategy` | method | `modules/ai_exploit_chain.py:318` | `def select_next_strategy(self, context)` |
| `AIResult` | class | `modules/ai_fallback.py:89` | `class AIResult` |
| `_best_ollama_model` | method | `modules/ai_fallback.py:107` | `def _best_ollama_model()` |
| `_groq_call` | method | `modules/ai_fallback.py:183` | `def _groq_call(api_key, system, user, max_tokens, temperature)` |
| `_is_quota_error` | method | `modules/ai_fallback.py:178` | `def _is_quota_error(exc)` |
| `_ollama_available` | method | `modules/ai_fallback.py:99` | `def _ollama_available()` |
| `_ollama_call` | method | `modules/ai_fallback.py:134` | `def _ollama_call(model, system, user, max_tokens, temperature)` |
| `_toposwarm_call` | method | `modules/ai_fallback.py:210` | `def _toposwarm_call(prompt, system)` |
| `call` | method | `modules/ai_fallback.py:238` | `def call(prompt, system, api_key, max_tokens, temperature)` |
| `AIModel` | class | `modules/ai_model.py:41` | `class AIModel(ABC)` |
| `AnthropicModel` | class | `modules/ai_model.py:331` | `class AnthropicModel(AIModel)` |
| `DeepSeekModel` | class | `modules/ai_model.py:387` | `class DeepSeekModel(AIModel)` |
| `GroqModel` | class | `modules/ai_model.py:125` | `class GroqModel(AIModel)` |
| `OllamaModel` | class | `modules/ai_model.py:205` | `class OllamaModel(AIModel)` |
| `OpenAIModel` | class | `modules/ai_model.py:272` | `class OpenAIModel(AIModel)` |
| `_LazyImporter` | class | `modules/ai_model.py:93` | `class _LazyImporter` |
| `__init__` | method | `modules/ai_model.py:133` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:213` | `def __init__(self, model, host)` |
| `__init__` | method | `modules/ai_model.py:278` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:337` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:394` | `def __init__(self, api_key, model)` |
| `anthropic` | method | `modules/ai_model.py:117` | `def anthropic(cls)` |
| `complete` | method | `modules/ai_model.py:59` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:177` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:308` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:367` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:427` | `def complete(self, system, user, max_tokens, temperature)` |
| `generate` | method | `modules/ai_model.py:52` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:137` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:221` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:282` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:341` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:401` | `def generate(self, prompt)` |
| `groq` | method | `modules/ai_model.py:101` | `def groq(cls)` |
| `openai` | method | `modules/ai_model.py:109` | `def openai(cls)` |
| `stream_generate` | method | `modules/ai_model.py:56` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:155` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:241` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:293` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:353` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:412` | `def stream_generate(self, prompt)` |
| `AMS1patch_E_ACCESSDENIED` | function | `modules/amsi.c:274` | `void AMS1patch_E_ACCESSDENIED(HANDLE hproc)` |
| `AMS1patch_E_HANDLE` | function | `modules/amsi.c:326` | `void AMS1patch_E_HANDLE(HANDLE hproc)` |
| `AMS1patch_E_OUTOFMEMORY` | function | `modules/amsi.c:378` | `void AMS1patch_E_OUTOFMEMORY(HANDLE hproc)` |
| `AMS1patch_OpenSession_jne` | function | `modules/amsi.c:66` | `void AMS1patch_OpenSession_jne(HANDLE hproc)` |
| `AMS1patch_OpenSession_ret` | function | `modules/amsi.c:116` | `void AMS1patch_OpenSession_ret(HANDLE hproc)` |
| `AMS1patch_RastaMouse` | function | `modules/amsi.c:215` | `void AMS1patch_RastaMouse(HANDLE hproc)` |
| `AMS1patch_ScanBuffer_ret` | function | `modules/amsi.c:166` | `void AMS1patch_ScanBuffer_ret(HANDLE hproc)` |
| `LoadNtFunctions` | function | `modules/amsi.c:38` | `void LoadNtFunctions()` |
| `NT_SUCCESS` | macro | `modules/amsi.c:11` | `#define NT_SUCCESS(Status)` |
| `main` | function | `modules/amsi.c:428` | `int main(int argc, char** argv)` |
| `BlankAuthResponse` | class | `modules/amt_auth_bypass.py:8` | `class BlankAuthResponse` |
| `request` | method | `modules/amt_auth_bypass.py:11` | `def request(self, flow)` |
| `start` | function | `modules/amt_auth_bypass.py:4` | `def start()` |
| `AptPlaybook` | class | `modules/apt_playbooks.py:65` | `class AptPlaybook` |
| `AptPlaybookEngine` | class | `modules/apt_playbooks.py:111` | `class AptPlaybookEngine` |
| `AtomicTestRef` | class | `modules/apt_playbooks.py:41` | `class AtomicTestRef` |
| `CalderaAbilityRef` | class | `modules/apt_playbooks.py:48` | `class CalderaAbilityRef` |
| `PhaseStep` | class | `modules/apt_playbooks.py:54` | `class PhaseStep` |
| `__init__` | method | `modules/apt_playbooks.py:114` | `def __init__(self, playbook_dir)` |
| `_build_atomic_index` | method | `modules/apt_playbooks.py:175` | `def _build_atomic_index(self, atomic_yaml_path)` |
| `_load_all` | method | `modules/apt_playbooks.py:119` | `def _load_all(self)` |
| `from_dict` | method | `modules/apt_playbooks.py:74` | `def from_dict(cls, data)` |
| `generate_attack_plan` | method | `modules/apt_playbooks.py:189` | `def generate_attack_plan(self, pb, output_path)` |
| `get` | method | `modules/apt_playbooks.py:134` | `def get(self, name)` |
| `list_playbooks` | method | `modules/apt_playbooks.py:131` | `def list_playbooks(self)` |
| `report_json` | method | `modules/apt_playbooks.py:204` | `def report_json(self, pb, output_path)` |
| `to_summary` | method | `modules/apt_playbooks.py:99` | `def to_summary(self)` |
| `validate` | method | `modules/apt_playbooks.py:138` | `def validate(self, pb, atomic_path)` |
| `Anchor` | class | `modules/asset_graph.py:63` | `class Anchor` |
| `AssetGraph` | class | `modules/asset_graph.py:70` | `class AssetGraph` |
| `AssetNode` | class | `modules/asset_graph.py:36` | `class AssetNode` |
| `ExplorationNode` | class | `modules/asset_graph.py:50` | `class ExplorationNode` |
| `GraphConfig` | class | `modules/asset_graph.py:17` | `class GraphConfig` |
| `__init__` | method | `modules/asset_graph.py:73` | `def __init__(self, config)` |
| `add_fact` | method | `modules/asset_graph.py:123` | `def add_fact(self, task_id, text, parent_id, payload)` |
| `add_finding` | method | `modules/asset_graph.py:128` | `def add_finding(self, task_id, text, parent_id, payload)` |
| `add_node` | method | `modules/asset_graph.py:108` | `def add_node(self, task_id, kind, text, parent_id, payload)` |
| `anchor` | method | `modules/asset_graph.py:133` | `def anchor(self, exploration_id, key)` |
| `asset_key` | method | `modules/asset_graph.py:28` | `def asset_key(asset_type, value, parent_key)` |
| `assets_for_node` | method | `modules/asset_graph.py:145` | `def assets_for_node(self, exploration_id)` |
| `coverage` | method | `modules/asset_graph.py:157` | `def coverage(self, task_id)` |
| `coverage_for` | method | `modules/asset_graph.py:214` | `def coverage_for(db, workspace_id, scope)` |
| `mirror_to_campaign` | method | `modules/asset_graph.py:170` | `def mirror_to_campaign(self, db, world_model, workspace_id)` |
| `nodes_for_asset` | method | `modules/asset_graph.py:151` | `def nodes_for_asset(self, key)` |
| `upsert_asset` | method | `modules/asset_graph.py:82` | `def upsert_asset(self, asset_type, value, parent_key, company)` |
| `_parse_complexity` | function | `modules/atomic_enricher.py:142` | `def _parse_complexity(command)` |
| `_parse_keyword_tags` | function | `modules/atomic_enricher.py:152` | `def _parse_keyword_tags(name, description)` |
| `_parse_platforms` | function | `modules/atomic_enricher.py:122` | `def _parse_platforms(raw)` |
| `_parse_scope` | function | `modules/atomic_enricher.py:135` | `def _parse_scope(name)` |
| `_tactic_prefix` | function | `modules/atomic_enricher.py:164` | `def _tactic_prefix(mitre_id)` |
| `_to_pylist` | function | `modules/atomic_enricher.py:204` | `def _to_pylist(val)` |
| `enrich` | function | `modules/atomic_enricher.py:173` | `def enrich(force)` |
| `load_enriched` | function | `modules/atomic_enricher.py:215` | `def load_enriched()` |
| `query_atomic` | function | `modules/atomic_enricher.py:232` | `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` |
| `_doc` | function | `modules/attack_surface3d.py:327` | `def _doc(node)` |
| `_enrich` | function | `modules/attack_surface3d.py:365` | `def _enrich(nodes, edges)` |
| `_family_color` | function | `modules/attack_surface3d.py:100` | `def _family_color(name)` |
| `_host_of` | function | `modules/attack_surface3d.py:141` | `def _host_of(node)` |
| `_intel_id_map` | function | `modules/attack_surface3d.py:315` | `def _intel_id_map(intel, key_to_id)` |
| `_pagerank` | function | `modules/attack_surface3d.py:111` | `def _pagerank(ids, pairs, alpha, max_iter, tol)` |
| `_symbols` | function | `modules/attack_surface3d.py:346` | `def _symbols(node)` |
| `add_edge` | function | `modules/attack_surface3d.py:155` | `def add_edge(src, dst, kind, evidence, weight)` |
| `build_attack_graph` | function | `modules/attack_surface3d.py:147` | `def build_attack_graph(sessions_dir, payload_path, est_cap)` |
| `refresh_summary` | function | `modules/attack_surface3d.py:460` | `def refresh_summary(graph, sessions_dir)` |
| `tag` | function | `modules/attack_surface3d.py:166` | `def tag(nid, source)` |
| `AutoPivotEngine` | class | `modules/auto_pivot.py:47` | `class AutoPivotEngine` |
| `PivotChain` | class | `modules/auto_pivot.py:39` | `class PivotChain` |
| `PivotNode` | class | `modules/auto_pivot.py:23` | `class PivotNode` |
| `__init__` | method | `modules/auto_pivot.py:73` | `def __init__(self, config)` |
| `_load_state` | method | `modules/auto_pivot.py:314` | `def _load_state(self)` |
| `_next_port` | method | `modules/auto_pivot.py:85` | `def _next_port(self)` |
| `_persist_state` | method | `modules/auto_pivot.py:277` | `def _persist_state(self)` |
| `add_pivot_node` | method | `modules/auto_pivot.py:90` | `def add_pivot_node(self, ip, access_type, credential_id, hostname)` |
| `build_chain` | method | `modules/auto_pivot.py:146` | `def build_chain(self, target_ip, via_nodes, subnet)` |
| `discover_subnets` | method | `modules/auto_pivot.py:128` | `def discover_subnets(self, node_ip, command_output)` |
| `generate_chisel_command` | method | `modules/auto_pivot.py:206` | `def generate_chisel_command(self, target_ip, local_port)` |
| `generate_proxychains_config` | method | `modules/auto_pivot.py:177` | `def generate_proxychains_config(self, chain_id)` |
| `generate_ssh_socks_command` | method | `modules/auto_pivot.py:212` | `def generate_ssh_socks_command(self, node_ip, local_port)` |
| `generate_sshuttle_command` | method | `modules/auto_pivot.py:203` | `def generate_sshuttle_command(self, node_ip, subnet)` |
| `get_active_routes` | method | `modules/auto_pivot.py:243` | `def get_active_routes(self)` |
| `get_reachable_hosts` | method | `modules/auto_pivot.py:259` | `def get_reachable_hosts(self, node_ip)` |
| `health_check` | method | `modules/auto_pivot.py:216` | `def health_check(self, node_ip)` |
| `health_check_all` | method | `modules/auto_pivot.py:237` | `def health_check_all(self)` |
| `remove_pivot_node` | method | `modules/auto_pivot.py:120` | `def remove_pivot_node(self, ip)` |
| `set_config` | method | `modules/auto_pivot.py:82` | `def set_config(self, config)` |
| `set_reachable_hosts` | method | `modules/auto_pivot.py:267` | `def set_reachable_hosts(self, node_ip, hosts)` |
| `set_route_priority` | method | `modules/auto_pivot.py:272` | `def set_route_priority(self, node_ip, priority)` |
| `suggest_next_pivot` | method | `modules/auto_pivot.py:352` | `def suggest_next_pivot(self)` |
| `DetectionMethod` | class | `modules/auto_purple.py:72` | `class DetectionMethod` |
| `IPurpleEvaluator` | class | `modules/auto_purple.py:210` | `class IPurpleEvaluator(ABC)` |
| `IPurpleLoop` | class | `modules/auto_purple.py:181` | `class IPurpleLoop(ABC)` |
| `PurpleResult` | class | `modules/auto_purple.py:132` | `class PurpleResult` |
| `PurpleScore` | class | `modules/auto_purple.py:165` | `class PurpleScore` |
| `PurpleTeamLoop` | class | `modules/auto_purple.py:407` | `class PurpleTeamLoop(IPurpleLoop, IPurpleEvaluator)` |
| `__init__` | method | `modules/auto_purple.py:414` | `def __init__(self, bt_path, detection_delay, methods, auto_feedback, session_id)` |
| `_append_dataset` | method | `modules/auto_purple.py:698` | `def _append_dataset(self, result)` |
| `_compute_oracle_accuracy` | method | `modules/auto_purple.py:739` | `def _compute_oracle_accuracy(self)` |
| `_execute_red` | method | `modules/auto_purple.py:614` | `def _execute_red(self, command, args)` |
| `_get_detection_methods` | method | `modules/auto_purple.py:759` | `def _get_detection_methods(self)` |
| `_hash_output` | method | `modules/auto_purple.py:687` | `def _hash_output(self, output)` |
| `_init_dataset` | method | `modules/auto_purple.py:433` | `def _init_dataset(self)` |
| `_load_audit` | method | `modules/auto_purple.py:724` | `def _load_audit(self)` |
| `_parse_ai_test` | method | `modules/auto_purple.py:329` | `def _parse_ai_test(output, command, args)` |
| `_parse_alert_check` | method | `modules/auto_purple.py:374` | `def _parse_alert_check(output, command, args)` |
| `_parse_fim_check` | method | `modules/auto_purple.py:388` | `def _parse_fim_check(output, command, args)` |
| `_parse_keyword_match` | method | `modules/auto_purple.py:342` | `def _parse_keyword_match(output, command, args)` |
| `_query_blue` | method | `modules/auto_purple.py:635` | `def _query_blue(self, command, args)` |
| `_run_bt_command` | method | `modules/auto_purple.py:225` | `def _run_bt_command(bt_path, command, timeout)` |
| `_write_audit` | method | `modules/auto_purple.py:693` | `def _write_audit(self, result)` |
| `_write_feedback` | method | `modules/auto_purple.py:704` | `def _write_feedback(self, result)` |
| `category_accuracy` | method | `modules/auto_purple.py:217` | `def category_accuracy(self, category)` |
| `category_accuracy` | method | `modules/auto_purple.py:599` | `def category_accuracy(self, category)` |
| `engagement_score` | method | `modules/auto_purple.py:201` | `def engagement_score(self)` |
| `engagement_score` | method | `modules/auto_purple.py:529` | `def engagement_score(self)` |
| `execute_and_measure` | method | `modules/auto_purple.py:185` | `def execute_and_measure(self, command, args, category)` |
| `execute_and_measure` | method | `modules/auto_purple.py:443` | `def execute_and_measure(self, command, args, category)` |
| `export_dataset` | method | `modules/auto_purple.py:204` | `def export_dataset(self)` |
| `export_dataset` | method | `modules/auto_purple.py:567` | `def export_dataset(self)` |
| `export_report` | method | `modules/auto_purple.py:207` | `def export_report(self)` |
| `export_report` | method | `modules/auto_purple.py:571` | `def export_report(self)` |
| `get_loop` | method | `modules/auto_purple.py:772` | `def get_loop(bt_path, detection_delay, methods, auto_feedback)` |
| `last_results` | method | `modules/auto_purple.py:214` | `def last_results(self, n)` |
| `last_results` | method | `modules/auto_purple.py:596` | `def last_results(self, n)` |
| `load_config_from_payload` | method | `modules/auto_purple.py:790` | `def load_config_from_payload(params)` |
| `measure_only` | method | `modules/auto_purple.py:193` | `def measure_only(self, command, args, category)` |
| `measure_only` | method | `modules/auto_purple.py:493` | `def measure_only(self, command, args, category)` |
| `to_csv_row` | method | `modules/auto_purple.py:146` | `def to_csv_row(self)` |
| `to_dict` | method | `modules/auto_purple.py:160` | `def to_dict(self)` |
| `AutoVerb` | class | `modules/auto_registry.py:29` | `class AutoVerb` |
| `ShellResult` | class | `modules/auto_registry.py:162` | `class ShellResult` |
| `_target` | method | `modules/auto_registry.py:184` | `def _target()` |
| `build_command` | method | `modules/auto_registry.py:109` | `def build_command(verb, target)` |
| `execute_shell_verb` | method | `modules/auto_registry.py:169` | `def execute_shell_verb(shell, command, timeout_sec)` |
| `is_shell_verb` | method | `modules/auto_registry.py:103` | `def is_shell_verb(token)` |
| `propose_intents` | method | `modules/auto_registry.py:127` | `def propose_intents(goal, target, finding_texts)` |
| `steps_for` | method | `modules/auto_registry.py:139` | `def steps_for(text, target)` |
| `verbs` | method | `modules/auto_registry.py:98` | `def verbs()` |
| `verbs_for` | method | `modules/auto_registry.py:120` | `def verbs_for(text)` |
| `AutonomousExploitEngine` | class | `modules/autonomous_exploit_engine.py:100` | `class AutonomousExploitEngine` |
| `ExploitCandidate` | class | `modules/autonomous_exploit_engine.py:73` | `class ExploitCandidate` |
| `ExploitResult` | class | `modules/autonomous_exploit_engine.py:88` | `class ExploitResult` |
| `TargetProfile` | class | `modules/autonomous_exploit_engine.py:58` | `class TargetProfile` |
| `__init__` | method | `modules/autonomous_exploit_engine.py:113` | `def __init__(self)` |
| `_apply_stealth_delay` | method | `modules/autonomous_exploit_engine.py:1636` | `def _apply_stealth_delay(self)` |
| `_build_command_chain` | method | `modules/autonomous_exploit_engine.py:1104` | `def _build_command_chain(self, candidate, profile)` |
| `_check_known_cves` | method | `modules/autonomous_exploit_engine.py:1936` | `def _check_known_cves(self, profile)` |
| `_check_success` | method | `modules/autonomous_exploit_engine.py:1236` | `def _check_success(self, output, candidate)` |
| `_credential_aware_rank` | method | `modules/autonomous_exploit_engine.py:240` | `def _credential_aware_rank(self, profile, credentials)` |
| `_detect_os_from_payload` | method | `modules/autonomous_exploit_engine.py:1523` | `def _detect_os_from_payload(self)` |
| `_detect_shell` | method | `modules/autonomous_exploit_engine.py:1329` | `def _detect_shell(self, output)` |
| `_determine_access_level` | method | `modules/autonomous_exploit_engine.py:1357` | `def _determine_access_level(self, ip, credentials)` |
| `_discover_internal_interfaces` | method | `modules/autonomous_exploit_engine.py:2457` | `def _discover_internal_interfaces(self, profile)` |
| `_execute_privesc` | method | `modules/autonomous_exploit_engine.py:2292` | `def _execute_privesc(self, technique, profile, session_id)` |
| `_extract_cves_from_text` | method | `modules/autonomous_exploit_engine.py:1708` | `def _extract_cves_from_text(self, text)` |
| `_filter_placeholder_creds` | method | `modules/autonomous_exploit_engine.py:283` | `def _filter_placeholder_creds(credentials)` |
| `_get_os_type` | method | `modules/autonomous_exploit_engine.py:1620` | `def _get_os_type(self, profile)` |
| `_get_stealth_scan_flags` | method | `modules/autonomous_exploit_engine.py:2563` | `def _get_stealth_scan_flags(self)` |
| `_heuristic_match` | method | `modules/autonomous_exploit_engine.py:491` | `def _heuristic_match(self, service, product, version)` |
| `_is_placeholder` | method | `modules/autonomous_exploit_engine.py:298` | `def _is_placeholder(value)` |
| `_load_from_nmap_xml` | method | `modules/autonomous_exploit_engine.py:1541` | `def _load_from_nmap_xml(self, target)` |
| `_load_payload_config` | method | `modules/autonomous_exploit_engine.py:1415` | `def _load_payload_config(self)` |
| `_load_world_model` | method | `modules/autonomous_exploit_engine.py:1426` | `def _load_world_model(self, target)` |
| `_match_by_port` | method | `modules/autonomous_exploit_engine.py:961` | `def _match_by_port(self, port, os_type)` |
| `_match_exploit_db` | method | `modules/autonomous_exploit_engine.py:453` | `def _match_exploit_db(self, service, product, version)` |
| `_match_privesc_techniques` | method | `modules/autonomous_exploit_engine.py:2102` | `def _match_privesc_techniques(self, findings, os_type)` |
| `_match_service_banners` | method | `modules/autonomous_exploit_engine.py:1756` | `def _match_service_banners(self, profile)` |
| `_parse_nse_output` | method | `modules/autonomous_exploit_engine.py:1673` | `def _parse_nse_output(self, target_ip)` |
| `_register_session` | method | `modules/autonomous_exploit_engine.py:1387` | `def _register_session(self, ip, output)` |
| `_resolve_port` | method | `modules/autonomous_exploit_engine.py:1087` | `def _resolve_port(self, candidate, profile)` |
| `_run_exploit` | method | `modules/autonomous_exploit_engine.py:1058` | `def _run_exploit(self, candidate, profile)` |
| `_run_linux_privesc_checks` | method | `modules/autonomous_exploit_engine.py:1990` | `def _run_linux_privesc_checks(self, profile, session_id)` |
| `_run_windows_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2059` | `def _run_windows_privesc_checks(self, profile, session_id)` |
| `_scorer` | method | `modules/autonomous_exploit_engine.py:1018` | `def _scorer(self, exploit, service, product, version)` |
| `chain_privesc` | method | `modules/autonomous_exploit_engine.py:1962` | `def chain_privesc(self, profile, session_id)` |
| `enable_stealth` | method | `modules/autonomous_exploit_engine.py:2518` | `def enable_stealth(self, stealth_level)` |
| `execute_candidate` | method | `modules/autonomous_exploit_engine.py:411` | `def execute_candidate(self, candidate, profile)` |
| `full_auto_pwn` | method | `modules/autonomous_exploit_engine.py:2582` | `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth)` |
| `get_instance` | method | `modules/autonomous_exploit_engine.py:133` | `def get_instance(cls)` |
| `hunt` | method | `modules/autonomous_exploit_engine.py:144` | `def hunt(self, target, max_exploits, profile)` |
| `profile` | method | `modules/autonomous_exploit_engine.py:327` | `def profile(self, target)` |
| `rank_exploits` | method | `modules/autonomous_exploit_engine.py:388` | `def rank_exploits(self, profile)` |
| `retry_with_credentials` | method | `modules/autonomous_exploit_engine.py:183` | `def retry_with_credentials(self, target, credentials)` |
| `scan_vulnerabilities` | method | `modules/autonomous_exploit_engine.py:1647` | `def scan_vulnerabilities(self, profile)` |
| `trigger_pivot` | method | `modules/autonomous_exploit_engine.py:2392` | `def trigger_pivot(self, profile, session_id)` |
| `AWSAttackEngine` | class | `modules/aws_attacks.py:80` | `class AWSAttackEngine` |
| `AWSConfig` | class | `modules/aws_attacks.py:58` | `class AWSConfig` |
| `__init__` | method | `modules/aws_attacks.py:91` | `def __init__(self, config)` |
| `cloudformation_drift` | method | `modules/aws_attacks.py:242` | `def cloudformation_drift(self)` |
| `ec2_ssm_session_abuse` | method | `modules/aws_attacks.py:274` | `def ec2_ssm_session_abuse(self)` |
| `ec2_user_data_exfil` | method | `modules/aws_attacks.py:181` | `def ec2_user_data_exfil(self)` |
| `enumerate_iam_permissions` | method | `modules/aws_attacks.py:95` | `def enumerate_iam_permissions(self)` |
| `lambda_backdoor` | method | `modules/aws_attacks.py:127` | `def lambda_backdoor(self, function_name)` |
| `s3_enumeration` | method | `modules/aws_attacks.py:206` | `def s3_enumeration(self)` |
| `sts_role_chain` | method | `modules/aws_attacks.py:155` | `def sts_role_chain(self, target_role_arn)` |
| `summary` | method | `modules/aws_attacks.py:293` | `def summary(self)` |
| `Shell` | function | `modules/backdoor/backdoor.c:84` | `void Shell()` |
| `WinMain` | function | `modules/backdoor/backdoor.c:125` | `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)` |
| `bootRun` | function | `modules/backdoor/backdoor.c:18` | `int bootRun()` |
| `bzero` | macro | `modules/backdoor/backdoor.c:14` | `#define bzero(p, size)` |
| `str_cut` | function | `modules/backdoor/backdoor.c:49` | `char * str_cut(char str[], int slice_from, int slice_to)` |
| `logg` | function | `modules/backdoor/keylogger.h:1` | `DWORD WINAPI logg(LPVOID lpParam)` |
| `main` | function | `modules/backdoor/server.c:10` | `int main()` |
| `BeaconConfig` | class | `modules/beacon_config_builder.py:44` | `class BeaconConfig` |
| `BeaconConfigBuilder` | class | `modules/beacon_config_builder.py:237` | `class BeaconConfigBuilder` |
| `__init__` | method | `modules/beacon_config_builder.py:245` | `def __init__(self, payload)` |
| `_inject_profile_engine` | method | `modules/beacon_config_builder.py:318` | `def _inject_profile_engine(self, config)` |
| `_inject_sleep_engine` | method | `modules/beacon_config_builder.py:366` | `def _inject_sleep_engine(self, config)` |
| `_inject_socks_engine` | method | `modules/beacon_config_builder.py:385` | `def _inject_socks_engine(self, config)` |
| `build` | method | `modules/beacon_config_builder.py:248` | `def build(self, name)` |
| `from_payload` | method | `modules/beacon_config_builder.py:403` | `def from_payload(cls, payload)` |
| `from_payload_file` | method | `modules/beacon_config_builder.py:408` | `def from_payload_file(cls, path)` |
| `generate_bof_execution_command` | method | `modules/beacon_config_builder.py:416` | `def generate_bof_execution_command(bof_name, c2_url, client_id, args, bofs_dir)` |
| `to_config_json` | method | `modules/beacon_config_builder.py:160` | `def to_config_json(self)` |
| `to_dict` | method | `modules/beacon_config_builder.py:185` | `def to_dict(self)` |
| `to_gen_beacon_args` | method | `modules/beacon_config_builder.py:117` | `def to_gen_beacon_args(self)` |
| `to_go_implant_vars` | method | `modules/beacon_config_builder.py:137` | `def to_go_implant_vars(self)` |
| `BeaconHistoryConfig` | class | `modules/beacon_history.py:28` | `class BeaconHistoryConfig` |
| `append_record` | method | `modules/beacon_history.py:82` | `def append_record(record, config)` |
| `read_records` | method | `modules/beacon_history.py:116` | `def read_records(client_id, config)` |
| `records_path` | method | `modules/beacon_history.py:43` | `def records_path(self, client_id)` |
| `records_path` | method | `modules/beacon_history.py:145` | `def records_path(client_id, config)` |
| `sanitize_client_id` | method | `modules/beacon_history.py:70` | `def sanitize_client_id(client_id)` |
| `sessions_dir` | method | `modules/beacon_history.py:39` | `def sessions_dir(self)` |
| `binario_a_imagen` | function | `modules/bin2img.py:7` | `def binario_a_imagen(binario, imagen_input, imagen_output, block_size)` |
| `main` | function | `modules/bin2img.py:54` | `def main()` |
| `BitMState` | class | `modules/bitm_engine.py:85` | `class BitMState` |
| `_build_js_payload` | method | `modules/bitm_engine.py:151` | `def _build_js_payload(payload_name, lhost, lport)` |
| `_check_tool` | method | `modules/bitm_engine.py:168` | `def _check_tool(tool)` |
| `_ensure_bitm_dir` | method | `modules/bitm_engine.py:103` | `def _ensure_bitm_dir()` |
| `_get_default_interface` | method | `modules/bitm_engine.py:195` | `def _get_default_interface()` |
| `_get_gateway_ip` | method | `modules/bitm_engine.py:234` | `def _get_gateway_ip()` |
| `_load_state` | method | `modules/bitm_engine.py:134` | `def _load_state()` |
| `_recommend_method` | method | `modules/bitm_engine.py:180` | `def _recommend_method()` |
| `_save_state` | method | `modules/bitm_engine.py:108` | `def _save_state(state)` |
| `_start_arpspoof` | method | `modules/bitm_engine.py:413` | `def _start_arpspoof(target_ip, gateway_ip, interface, lhost, lport, js_payload, harvest_path)` |
| `_start_bettercap` | method | `modules/bitm_engine.py:354` | `def _start_bettercap(target_ip, gateway_ip, interface, lhost, lport, js_payload, harvest_path)` |
| `bitm_cleanup` | method | `modules/bitm_engine.py:642` | `def bitm_cleanup()` |
| `bitm_harvest_stats` | method | `modules/bitm_engine.py:607` | `def bitm_harvest_stats()` |
| `bitm_inject` | method | `modules/bitm_engine.py:572` | `def bitm_inject(payload_name)` |
| `bitm_start` | method | `modules/bitm_engine.py:257` | `def bitm_start(target_ip, gateway_ip, interface, lhost, lport, method, payloads)` |
| `bitm_status` | method | `modules/bitm_engine.py:539` | `def bitm_status()` |
| `bitm_stop` | method | `modules/bitm_engine.py:481` | `def bitm_stop()` |
| `main` | method | `modules/bitm_engine.py:661` | `def main()` |
| `BofCatalog` | class | `modules/bof_registry.py:157` | `class BofCatalog` |
| `BofCategory` | class | `modules/bof_registry.py:68` | `class BofCategory(str, Enum)` |
| `BofEntry` | class | `modules/bof_registry.py:85` | `class BofEntry` |
| `BofMarketplace` | class | `modules/bof_registry.py:639` | `class BofMarketplace` |
| `BofPlatform` | class | `modules/bof_registry.py:61` | `class BofPlatform(str, Enum)` |
| `BofRegistry` | class | `modules/bof_registry.py:552` | `class BofRegistry` |
| `BofValidator` | class | `modules/bof_registry.py:506` | `class BofValidator` |
| `__init__` | method | `modules/bof_registry.py:559` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/bof_registry.py:651` | `def __init__(self, sessions_dir, catalog)` |
| `_build_default_catalog` | method | `modules/bof_registry.py:265` | `def _build_default_catalog()` |
| `_load_manifest` | method | `modules/bof_registry.py:569` | `def _load_manifest(self)` |
| `_save_manifest` | method | `modules/bof_registry.py:580` | `def _save_manifest(self, manifest)` |
| `bulk_install` | method | `modules/bof_registry.py:769` | `def bulk_install(self, names)` |
| `catalog` | method | `modules/bof_registry.py:662` | `def catalog(self)` |
| `compute_sha256` | method | `modules/bof_registry.py:515` | `def compute_sha256(filepath)` |
| `from_dict` | method | `modules/bof_registry.py:137` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/bof_registry.py:241` | `def from_dict(cls, raw)` |
| `get` | method | `modules/bof_registry.py:177` | `def get(self, name)` |
| `get_install_info` | method | `modules/bof_registry.py:633` | `def get_install_info(self, name)` |
| `info` | method | `modules/bof_registry.py:690` | `def info(self, name)` |
| `install` | method | `modules/bof_registry.py:590` | `def install(self, entry)` |
| `install` | method | `modules/bof_registry.py:707` | `def install(self, name)` |
| `install_dir` | method | `modules/bof_registry.py:565` | `def install_dir(self)` |
| `is_installed` | method | `modules/bof_registry.py:585` | `def is_installed(self, name)` |
| `list_all` | method | `modules/bof_registry.py:229` | `def list_all(self)` |
| `list_by_category` | method | `modules/bof_registry.py:221` | `def list_by_category(self, category)` |
| `list_by_platform` | method | `modules/bof_registry.py:225` | `def list_by_platform(self, platform)` |
| `list_installed` | method | `modules/bof_registry.py:628` | `def list_installed(self)` |
| `list_installed` | method | `modules/bof_registry.py:749` | `def list_installed(self)` |
| `list_missing_dependencies` | method | `modules/bof_registry.py:761` | `def list_missing_dependencies(self, name)` |
| `load` | method | `modules/bof_registry.py:249` | `def load(cls, path)` |
| `register` | method | `modules/bof_registry.py:167` | `def register(self, entry)` |
| `register_many` | method | `modules/bof_registry.py:172` | `def register_many(self, entries)` |
| `registry` | method | `modules/bof_registry.py:667` | `def registry(self)` |
| `save` | method | `modules/bof_registry.py:257` | `def save(self, path)` |
| `search` | method | `modules/bof_registry.py:188` | `def search(self, query)` |
| `search` | method | `modules/bof_registry.py:671` | `def search(self, query)` |
| `to_dict` | method | `modules/bof_registry.py:118` | `def to_dict(self)` |
| `to_dict` | method | `modules/bof_registry.py:233` | `def to_dict(self)` |
| `uninstall` | method | `modules/bof_registry.py:611` | `def uninstall(self, name, remove_files)` |
| `uninstall` | method | `modules/bof_registry.py:736` | `def uninstall(self, name)` |
| `validate_args` | method | `modules/bof_registry.py:540` | `def validate_args(entry, args)` |
| `verify_entry` | method | `modules/bof_registry.py:524` | `def verify_entry(entry, filepath)` |
| `BotConfig` | class | `modules/bot.py:20` | `class BotConfig` |
| `find_new_repos` | method | `modules/bot.py:48` | `def find_new_repos(language, days, count, order, config)` |
| `format_output` | method | `modules/bot.py:128` | `def format_output(content, config)` |
| `main` | method | `modules/bot.py:148` | `def main(config)` |
| `render_repos` | method | `modules/bot.py:102` | `def render_repos(repos, config)` |
| `C2Builder` | class | `modules/c2_builder.py:392` | `class C2Builder` |
| `C2Profile` | class | `modules/c2_builder.py:76` | `class C2Profile` |
| `__init__` | method | `modules/c2_builder.py:395` | `def __init__(self, params, sessions_dir, cmd_fn, onecmd_fn, toastr_fn, c2_user, c2_pass)` |
| `_build_compile_commands` | method | `modules/c2_builder.py:310` | `def _build_compile_commands(sessions_dir, profile, gocompiler, compile_flags, main_out, main_src, listener_out...` |
| `_build_context` | method | `modules/c2_builder.py:361` | `def _build_context(sessions_dir)` |
| `_command_output` | method | `modules/c2_builder.py:249` | `def _command_output(argv, timeout)` |
| `_ensure_garble_toolchain` | method | `modules/c2_builder.py:413` | `def _ensure_garble_toolchain(self, go_bin, garble_bin, gocompiler, profile)` |
| `_ensure_go` | function | `modules/c2_builder.py:59` | `def _ensure_go(cmd_fn)` |
| `_garble_matches_toolchain` | method | `modules/c2_builder.py:287` | `def _garble_matches_toolchain(go_bin, garble_bin)` |
| `_go_build_version` | method | `modules/c2_builder.py:268` | `def _go_build_version(go_bin, target)` |
| `_go_string_list` | method | `modules/c2_builder.py:220` | `def _go_string_list(urls)` |
| `_parse_go_version` | method | `modules/c2_builder.py:234` | `def _parse_go_version(text)` |
| `_preflight` | method | `modules/c2_builder.py:160` | `def _preflight(profile)` |
| `_read` | method | `modules/c2_builder.py:641` | `def _read(path_)` |
| `_read_required` | method | `modules/c2_builder.py:648` | `def _read_required(path_)` |
| `_render_template` | method | `modules/c2_builder.py:169` | `def _render_template(content, context)` |
| `_replacer` | method | `modules/c2_builder.py:173` | `def _replacer(match)` |
| `_resolve_fallback_urls` | method | `modules/c2_builder.py:180` | `def _resolve_fallback_urls(params)` |
| `_resolve_go_bin` | function | `modules/c2_builder.py:44` | `def _resolve_go_bin()` |
| `_write` | method | `modules/c2_builder.py:652` | `def _write(path_, content)` |
| `run` | method | `modules/c2_builder.py:453` | `def run(self, line, choice, use_tunnel)` |
| `PayloadConfigAdapter` | class | `modules/c2_messaging_base.py:117` | `class PayloadConfigAdapter` |
| `SecureSessionManager` | class | `modules/c2_messaging_base.py:9` | `class SecureSessionManager` |
| `__getitem__` | method | `modules/c2_messaging_base.py:129` | `def __getitem__(self, key)` |
| `__init__` | method | `modules/c2_messaging_base.py:22` | `def __init__(self, max_failed_attempts, lockout_duration, rate_limit, session_timeout)` |
| `__init__` | method | `modules/c2_messaging_base.py:124` | `def __init__(self, config_dict)` |
| `check_lockout` | method | `modules/c2_messaging_base.py:46` | `def check_lockout(self, user_id)` |
| `check_rate_limit` | method | `modules/c2_messaging_base.py:61` | `def check_rate_limit(self, user_id)` |
| `create_session` | method | `modules/c2_messaging_base.py:79` | `def create_session(self, user_id, client_id)` |
| `get` | method | `modules/c2_messaging_base.py:132` | `def get(self, key, default)` |
| `get_client` | method | `modules/c2_messaging_base.py:111` | `def get_client(self, user_id)` |
| `register_failed_attempt` | method | `modules/c2_messaging_base.py:37` | `def register_failed_attempt(self, user_id)` |
| `set_client` | method | `modules/c2_messaging_base.py:106` | `def set_client(self, user_id, client_id)` |
| `validate_session` | method | `modules/c2_messaging_base.py:89` | `def validate_session(self, user_id)` |
| `C2Profile` | class | `modules/c2_profile.py:81` | `class C2Profile` |
| `HttpConfig` | class | `modules/c2_profile.py:62` | `class HttpConfig` |
| `ProfileApplier` | class | `modules/c2_profile.py:520` | `class ProfileApplier` |
| `ProfileLoader` | class | `modules/c2_profile.py:187` | `class ProfileLoader` |
| `ProfileRegistry` | class | `modules/c2_profile.py:449` | `class ProfileRegistry` |
| `ProfileValidator` | class | `modules/c2_profile.py:155` | `class ProfileValidator` |
| `SleepConfig` | class | `modules/c2_profile.py:54` | `class SleepConfig` |
| `StagerConfig` | class | `modules/c2_profile.py:72` | `class StagerConfig` |
| `__init__` | method | `modules/c2_profile.py:457` | `def __init__(self)` |
| `_config_for` | method | `modules/c2_profile.py:144` | `def _config_for(self, method)` |
| `_make_aggressive_profile` | method | `modules/c2_profile.py:385` | `def _make_aggressive_profile()` |
| `_make_debug_profile` | method | `modules/c2_profile.py:410` | `def _make_debug_profile()` |
| `_make_default_profile` | method | `modules/c2_profile.py:308` | `def _make_default_profile()` |
| `_make_stealth_profile` | method | `modules/c2_profile.py:339` | `def _make_stealth_profile()` |
| `apply_to_response` | method | `modules/c2_profile.py:529` | `def apply_to_response(profile, response)` |
| `apply_to_session` | method | `modules/c2_profile.py:554` | `def apply_to_session(profile, session)` |
| `build_headers` | method | `modules/c2_profile.py:128` | `def build_headers(self, method)` |
| `from_dict` | method | `modules/c2_profile.py:215` | `def from_dict(d)` |
| `from_yaml` | method | `modules/c2_profile.py:200` | `def from_yaml(path)` |
| `get` | method | `modules/c2_profile.py:473` | `def get(self, name)` |
| `get_beacon_config` | method | `modules/c2_profile.py:567` | `def get_beacon_config(profile)` |
| `get_profile` | method | `modules/c2_profile.py:620` | `def get_profile(name)` |
| `get_registry` | method | `modules/c2_profile.py:595` | `def get_registry()` |
| `get_uri` | method | `modules/c2_profile.py:117` | `def get_uri(self, method)` |
| `jitter_delay` | method | `modules/c2_profile.py:101` | `def jitter_delay(self)` |
| `list_names` | method | `modules/c2_profile.py:485` | `def list_names(self)` |
| `list_profiles` | method | `modules/c2_profile.py:625` | `def list_profiles()` |
| `load_from_directory` | method | `modules/c2_profile.py:493` | `def load_from_directory(self, path)` |
| `register` | method | `modules/c2_profile.py:464` | `def register(self, name, profile)` |
| `save` | method | `modules/c2_profile.py:282` | `def save(profile, path)` |
| `to_dict` | method | `modules/c2_profile.py:254` | `def to_dict(profile)` |
| `validate` | method | `modules/c2_profile.py:162` | `def validate(self, profile)` |
| `DnsProfile` | class | `modules/c2_profile_engine.py:205` | `class DnsProfile` |
| `ProfileEngine` | class | `modules/c2_profile_engine.py:611` | `class ProfileEngine` |
| `ProfileRotator` | class | `modules/c2_profile_engine.py:441` | `class ProfileRotator` |
| `ProfileValidator` | class | `modules/c2_profile_engine.py:503` | `class ProfileValidator` |
| `RotationSlot` | class | `modules/c2_profile_engine.py:414` | `class RotationSlot` |
| `SmbProfile` | class | `modules/c2_profile_engine.py:289` | `class SmbProfile` |
| `TlsProfile` | class | `modules/c2_profile_engine.py:117` | `class TlsProfile` |
| `TransportType` | class | `modules/c2_profile_engine.py:404` | `class TransportType(Enum)` |
| `WebSocketProfile` | class | `modules/c2_profile_engine.py:349` | `class WebSocketProfile` |
| `__init__` | method | `modules/c2_profile_engine.py:453` | `def __init__(self, slots)` |
| `__init__` | method | `modules/c2_profile_engine.py:627` | `def __init__(self, tls_profile, dns_profile, smb_profile, websocket_profile, rotation_slots)` |
| `_default_slots` | method | `modules/c2_profile_engine.py:709` | `def _default_slots(self)` |
| `active_transport` | method | `modules/c2_profile_engine.py:668` | `def active_transport(self)` |
| `build_query_subdomain` | method | `modules/c2_profile_engine.py:231` | `def build_query_subdomain(self, data, packet_id)` |
| `current_slot` | method | `modules/c2_profile_engine.py:460` | `def current_slot(self)` |
| `dns_profile` | method | `modules/c2_profile_engine.py:648` | `def dns_profile(self)` |
| `from_config` | method | `modules/c2_profile_engine.py:771` | `def from_config(cls, config)` |
| `from_dict` | method | `modules/c2_profile_engine.py:173` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:261` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:319` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:375` | `def from_dict(raw)` |
| `from_dict` | method | `modules/c2_profile_engine.py:747` | `def from_dict(cls, raw)` |
| `from_payload` | method | `modules/c2_profile_engine.py:766` | `def from_payload(cls, payload)` |
| `get_active_profile_dict` | method | `modules/c2_profile_engine.py:685` | `def get_active_profile_dict(self)` |
| `get_all_profiles_dict` | method | `modules/c2_profile_engine.py:699` | `def get_all_profiles_dict(self)` |
| `get_cipher_suites` | method | `modules/c2_profile_engine.py:144` | `def get_cipher_suites(self)` |

Next: [SYMBOLS_p11.md](SYMBOLS_p11.md)
