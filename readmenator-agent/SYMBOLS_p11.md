# Symbols (page 11 of 48)
Previous: [SYMBOLS_p10.md](SYMBOLS_p10.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `vulnerabilities` | function | `modules/ad_gym.py:43` | `def vulnerabilities(path)` |
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
| `AddonUpdateResult` | class | `modules/addon_updater.py:33` | `class AddonUpdateResult` |
| `_audit` | function | `modules/addon_updater.py:315` | `def _audit(summary, path)` |
| `_git` | function | `modules/addon_updater.py:135` | `def _git(path)` |
| `_read_addon` | function | `modules/addon_updater.py:61` | `def _read_addon(path)` |
| `_safe_target` | function | `modules/addon_updater.py:107` | `def _safe_target(install_path, root)` |
| `_worktree_root` | function | `modules/addon_updater.py:150` | `def _worktree_root(path, repository_root)` |
| `load_addons` | function | `modules/addon_updater.py:73` | `def load_addons(lazyaddons_dir)` |
| `to_dict` | method | `modules/addon_updater.py:46` | `def to_dict(self)` |
| `update_addon` | function | `modules/addon_updater.py:166` | `def update_addon(name, lazyaddons_dir, root, dry_run)` |
| `update_all` | function | `modules/addon_updater.py:260` | `def update_all(names, lazyaddons_dir, root, dry_run, audit_path)` |
| `ASTToolExtractor` | class | `modules/agent_runner.py:138` | `class ASTToolExtractor` |
| `AgentRunner` | class | `modules/agent_runner.py:194` | `class AgentRunner` |
| `AgentTool` | class | `modules/agent_runner.py:70` | `class AgentTool` |
| `CommandMetadata` | class | `modules/agent_runner.py:131` | `class CommandMetadata` |
| `LazyOwnShellWrapper` | class | `modules/agent_runner.py:486` | `class LazyOwnShellWrapper` |
| `VulnBotCLI` | class | `modules/agent_runner.py:563` | `class VulnBotCLI` |
| `__init__` | method | `modules/agent_runner.py:73` | `def __init__(self, name, description, func, parameters, required)` |
| `__init__` | method | `modules/agent_runner.py:197` | `def __init__(self, model, system_prompt, max_iterations)` |
| `__init__` | method | `modules/agent_runner.py:489` | `def __init__(self, script_path)` |
| `__init__` | method | `modules/agent_runner.py:564` | `def __init__(self, provider, mode, debug, script_path)` |
| `_call_model` | method | `modules/agent_runner.py:299` | `def _call_model(self)` |
| `_emit_delta` | method | `modules/agent_runner.py:419` | `def _emit_delta(self, kind, text)` |
| `_load_model` | method | `modules/agent_runner.py:576` | `def _load_model(self)` |
| `_load_shell` | method | `modules/agent_runner.py:496` | `def _load_shell(self)` |
| `_manage_memory` | method | `modules/agent_runner.py:214` | `def _manage_memory(self)` |
| `_process_tool_call` | method | `modules/agent_runner.py:438` | `def _process_tool_call(self, tool_call)` |
| `_reset_history` | method | `modules/agent_runner.py:211` | `def _reset_history(self)` |
| `_setup_agent` | method | `modules/agent_runner.py:591` | `def _setup_agent(self)` |
| `_stream_call` | method | `modules/agent_runner.py:345` | `def _stream_call(self, model_name, messages, max_tokens)` |
| `_tool_call_snapshot` | function | `modules/agent_runner.py:177` | `def _tool_call_snapshot(tool_call)` |
| `configure_logging` | function | `modules/agent_runner.py:64` | `def configure_logging(debug)` |
| `execute` | method | `modules/agent_runner.py:87` | `def execute(self)` |
| `execute_command` | method | `modules/agent_runner.py:519` | `def execute_command(self, command)` |
| `extract_commands_from_file` | method | `modules/agent_runner.py:142` | `def extract_commands_from_file(file_path, prefix)` |
| `get_commands_summary` | method | `modules/agent_runner.py:556` | `def get_commands_summary(self)` |
| `get_tools_for_api` | method | `modules/agent_runner.py:270` | `def get_tools_for_api(self)` |
| `interactive_mode` | function | `modules/agent_runner.py:624` | `def interactive_mode(bot)` |
| `main` | function | `modules/agent_runner.py:658` | `def main()` |
| `make_executor` | function | `modules/agent_runner.py:247` | `def make_executor(cmd_name)` |
| `parse_args` | function | `modules/agent_runner.py:648` | `def parse_args()` |
| `process_request` | method | `modules/agent_runner.py:619` | `def process_request(self, user_input)` |
| `register_tool` | method | `modules/agent_runner.py:222` | `def register_tool(self, tool)` |
| `register_tool_from_instance` | method | `modules/agent_runner.py:225` | `def register_tool_from_instance(self, func)` |
| `register_tools_from_metadata` | method | `modules/agent_runner.py:243` | `def register_tools_from_metadata(self, commands, executor)` |
| `run` | method | `modules/agent_runner.py:275` | `def run(self, user_input)` |
| `target` | function | `modules/agent_runner.py:526` | `def target()` |
| `to_api_format` | method | `modules/agent_runner.py:81` | `def to_api_format(self)` |
| `wrapper` | function | `modules/agent_runner.py:248` | `def wrapper(command)` |
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
| `AIResult` | class | `modules/ai_fallback.py:108` | `class AIResult` |
| `_best_ollama_model` | function | `modules/ai_fallback.py:126` | `def _best_ollama_model()` |
| `_chain_groq_attempted` | function | `modules/ai_fallback.py:267` | `def _chain_groq_attempted(result)` |
| `_fallback_warning` | function | `modules/ai_fallback.py:349` | `def _fallback_warning(orch)` |
| `_groq_call` | function | `modules/ai_fallback.py:202` | `def _groq_call(api_key, system, user, max_tokens, temperature)` |
| `_is_quota_error` | function | `modules/ai_fallback.py:197` | `def _is_quota_error(exc)` |
| `_ollama_available` | function | `modules/ai_fallback.py:118` | `def _ollama_available()` |
| `_ollama_call` | function | `modules/ai_fallback.py:153` | `def _ollama_call(model, system, user, max_tokens, temperature)` |
| `_summarize_attempts` | function | `modules/ai_fallback.py:354` | `def _summarize_attempts(orch)` |
| `_toposwarm_call` | function | `modules/ai_fallback.py:239` | `def _toposwarm_call(prompt, system)` |
| `_total_failure_result` | function | `modules/ai_fallback.py:359` | `def _total_failure_result(orch, local_error)` |
| `call` | function | `modules/ai_fallback.py:280` | `def call(prompt, system, api_key, max_tokens, temperature)` |
| `AIModel` | class | `modules/ai_model.py:45` | `class AIModel(ABC)` |
| `AnthropicModel` | class | `modules/ai_model.py:493` | `class AnthropicModel(AIModel)` |
| `DeepSeekModel` | class | `modules/ai_model.py:549` | `class DeepSeekModel(AIModel)` |
| `GroqModel` | class | `modules/ai_model.py:129` | `class GroqModel(AIModel)` |
| `LlamaCppModel` | class | `modules/ai_model.py:313` | `class LlamaCppModel(AIModel)` |
| `OllamaModel` | class | `modules/ai_model.py:244` | `class OllamaModel(AIModel)` |
| `OpenAIModel` | class | `modules/ai_model.py:434` | `class OpenAIModel(AIModel)` |
| `_LazyImporter` | class | `modules/ai_model.py:97` | `class _LazyImporter` |
| `__init__` | method | `modules/ai_model.py:137` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:252` | `def __init__(self, model, host)` |
| `__init__` | method | `modules/ai_model.py:324` | `def __init__(self, model, host)` |
| `__init__` | method | `modules/ai_model.py:440` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:499` | `def __init__(self, api_key, model)` |
| `__init__` | method | `modules/ai_model.py:556` | `def __init__(self, api_key, model)` |
| `_chat` | method | `modules/ai_model.py:341` | `def _chat(self, messages, max_tokens, stream)` |
| `_model_chain` | method | `modules/ai_model.py:141` | `def _model_chain(self)` |
| `anthropic` | method | `modules/ai_model.py:121` | `def anthropic(cls)` |
| `complete` | method | `modules/ai_model.py:63` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:216` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:413` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:470` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:529` | `def complete(self, system, user, max_tokens, temperature)` |
| `complete` | method | `modules/ai_model.py:589` | `def complete(self, system, user, max_tokens, temperature)` |
| `generate` | method | `modules/ai_model.py:56` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:155` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:260` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:362` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:444` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:503` | `def generate(self, prompt)` |
| `generate` | method | `modules/ai_model.py:563` | `def generate(self, prompt)` |
| `groq` | method | `modules/ai_model.py:105` | `def groq(cls)` |
| `openai` | method | `modules/ai_model.py:113` | `def openai(cls)` |
| `stream_generate` | method | `modules/ai_model.py:60` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:183` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:281` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:382` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:455` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:515` | `def stream_generate(self, prompt)` |
| `stream_generate` | method | `modules/ai_model.py:574` | `def stream_generate(self, prompt)` |
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
| `_build_atomic_index` | method | `modules/apt_playbooks.py:199` | `def _build_atomic_index(self, atomic_yaml_path)` |
| `_load_all` | method | `modules/apt_playbooks.py:119` | `def _load_all(self)` |
| `from_dict` | method | `modules/apt_playbooks.py:74` | `def from_dict(cls, data)` |
| `generate_attack_plan` | method | `modules/apt_playbooks.py:213` | `def generate_attack_plan(self, pb, output_path)` |
| `get` | method | `modules/apt_playbooks.py:134` | `def get(self, name)` |
| `list_playbooks` | method | `modules/apt_playbooks.py:131` | `def list_playbooks(self)` |
| `report_json` | method | `modules/apt_playbooks.py:230` | `def report_json(self, pb, output_path)` |
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
| `asset_key` | function | `modules/asset_graph.py:28` | `def asset_key(asset_type, value, parent_key)` |
| `assets_for_node` | method | `modules/asset_graph.py:145` | `def assets_for_node(self, exploration_id)` |
| `coverage` | method | `modules/asset_graph.py:157` | `def coverage(self, task_id)` |
| `coverage_for` | function | `modules/asset_graph.py:214` | `def coverage_for(db, workspace_id, scope)` |
| `mirror_to_campaign` | method | `modules/asset_graph.py:170` | `def mirror_to_campaign(self, db, world_model, workspace_id)` |
| `nodes_for_asset` | method | `modules/asset_graph.py:151` | `def nodes_for_asset(self, key)` |
| `upsert_asset` | method | `modules/asset_graph.py:82` | `def upsert_asset(self, asset_type, value, parent_key, company)` |
| `_load_credentials` | function | `modules/atomic_cli.py:147` | `def _load_credentials(params, non_interactive)` |
| `_print` | function | `modules/atomic_cli.py:107` | `def _print(shell, text)` |
| `_prompt_choice` | function | `modules/atomic_cli.py:171` | `def _prompt_choice(count, prompt, non_interactive)` |
| `_resolver` | function | `modules/atomic_cli.py:99` | `def _resolver()` |
| `_safe_copy` | function | `modules/atomic_cli.py:132` | `def _safe_copy(text)` |
| `_sanitized_script_name` | function | `modules/atomic_cli.py:319` | `def _sanitized_script_name(test_id, extension)` |
| `_wants_interactive` | function | `modules/atomic_cli.py:127` | `def _wants_interactive(non_interactive)` |
| `_warn` | function | `modules/atomic_cli.py:118` | `def _warn(text)` |
| `parse_atomic_line` | function | `modules/atomic_cli.py:37` | `def parse_atomic_line(line)` |
| `run_atomic_gen` | function | `modules/atomic_cli.py:325` | `def run_atomic_gen(params, line, shell)` |
| `run_atomic_tests` | function | `modules/atomic_cli.py:185` | `def run_atomic_tests(params, line, shell)` |
| `_parse_complexity` | function | `modules/atomic_enricher.py:142` | `def _parse_complexity(command)` |
| `_parse_keyword_tags` | function | `modules/atomic_enricher.py:152` | `def _parse_keyword_tags(name, description)` |
| `_parse_platforms` | function | `modules/atomic_enricher.py:122` | `def _parse_platforms(raw)` |
| `_parse_scope` | function | `modules/atomic_enricher.py:135` | `def _parse_scope(name)` |
| `_tactic_prefix` | function | `modules/atomic_enricher.py:164` | `def _tactic_prefix(mitre_id)` |
| `_to_pylist` | function | `modules/atomic_enricher.py:204` | `def _to_pylist(val)` |
| `enrich` | function | `modules/atomic_enricher.py:173` | `def enrich(force)` |
| `load_enriched` | function | `modules/atomic_enricher.py:215` | `def load_enriched()` |
| `query_atomic` | function | `modules/atomic_enricher.py:232` | `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` |
| `ExploitCommand` | class | `modules/atomic_exploit_bridge.py:84` | `class ExploitCommand` |
| `ExploitSpec` | class | `modules/atomic_exploit_bridge.py:92` | `class ExploitSpec` |
| `_ShellSession` | class | `modules/atomic_exploit_bridge.py:721` | `class _ShellSession` |
| `__init__` | method | `modules/atomic_exploit_bridge.py:729` | `def __init__(self, target, port, sock, owner)` |
| `_adopt_live_shell` | function | `modules/atomic_exploit_bridge.py:1061` | `def _adopt_live_shell(spec, target, port)` |
| `_claim_port` | function | `modules/atomic_exploit_bridge.py:816` | `def _claim_port(spec_id, target, port)` |
| `_destroy_gym` | function | `modules/atomic_exploit_bridge.py:988` | `def _destroy_gym(container)` |
| `_install_missing_binaries` | function | `modules/atomic_exploit_bridge.py:555` | `def _install_missing_binaries(names)` |
| `_read_until` | method | `modules/atomic_exploit_bridge.py:760` | `def _read_until(self, marker, timeout)` |
| `_release_port` | function | `modules/atomic_exploit_bridge.py:834` | `def _release_port(target, port)` |
| `_string_list` | function | `modules/atomic_exploit_bridge.py:142` | `def _string_list(value)` |
| `_token_mapping` | function | `modules/atomic_exploit_bridge.py:511` | `def _token_mapping(rhost, lhost, lport, port)` |
| `_wait_port_closed` | function | `modules/atomic_exploit_bridge.py:1087` | `def _wait_port_closed(target, port, timeout)` |
| `alive` | method | `modules/atomic_exploit_bridge.py:739` | `def alive(self, timeout)` |
| `auto` | function | `modules/atomic_exploit_bridge.py:351` | `def auto(target, lhost, max_attempts, stop_on_shell, task_id, exploits_dir, scan_dir)` |
| `build_commands` | function | `modules/atomic_exploit_bridge.py:525` | `def build_commands(spec, rhost, lhost, lport, port)` |
| `cleanup_target` | function | `modules/atomic_exploit_bridge.py:929` | `def cleanup_target(target, lhost, hard, gym_container, exploits_dir, staging_dir)` |
| `close` | method | `modules/atomic_exploit_bridge.py:788` | `def close(self)` |
| `close_sessions` | function | `modules/atomic_exploit_bridge.py:887` | `def close_sessions(target)` |
| `detect_shell` | function | `modules/atomic_exploit_bridge.py:543` | `def detect_shell(spec, output)` |
| `emulate` | function | `modules/atomic_exploit_bridge.py:1175` | `def emulate(target, techniques, playbook, platform, lhost, per_technique, exploits_dir, scan_dir, include_manual...` |
| `ensure_session` | function | `modules/atomic_exploit_bridge.py:1006` | `def ensure_session(spec, target, lhost)` |
| `interactive_shell` | function | `modules/atomic_exploit_bridge.py:1120` | `def interactive_shell(target, lhost, interactive, exploits_dir)` |
| `live_sessions` | function | `modules/atomic_exploit_bridge.py:868` | `def live_sessions()` |
| `load_all` | function | `modules/atomic_exploit_bridge.py:226` | `def load_all(exploits_dir)` |
| `main` | function | `modules/atomic_exploit_bridge.py:1297` | `def main()` |
| `match_score` | function | `modules/atomic_exploit_bridge.py:281` | `def match_score(spec, service, product, version, os_hint)` |
| `open_shell` | function | `modules/atomic_exploit_bridge.py:665` | `def open_shell(target, services, lhost, exploits_dir, attempts, privilege)` |
| `parse_scan_xml` | function | `modules/atomic_exploit_bridge.py:314` | `def parse_scan_xml(xml_path)` |
| `rank` | function | `modules/atomic_exploit_bridge.py:456` | `def rank(services, exploits_dir, os_hint)` |
| `record_outcome` | function | `modules/atomic_exploit_bridge.py:1209` | `def record_outcome(spec, target, shell, output, task_id, intent_id, surfaces_dir, port, service, product, version...` |
| `record_shell_outcome` | function | `modules/atomic_exploit_bridge.py:839` | `def record_shell_outcome(target, via)` |
| `remote_exec` | function | `modules/atomic_exploit_bridge.py:1102` | `def remote_exec(spec, target, command, lhost)` |
| `run` | method | `modules/atomic_exploit_bridge.py:746` | `def run(self, command, timeout)` |
| `run_spec` | function | `modules/atomic_exploit_bridge.py:585` | `def run_spec(spec, rhost, lhost, lport, port)` |
| `severity_rank` | method | `modules/atomic_exploit_bridge.py:117` | `def severity_rank(self)` |
| `to_dict` | method | `modules/atomic_exploit_bridge.py:121` | `def to_dict(self)` |
| `validate_spec` | function | `modules/atomic_exploit_bridge.py:150` | `def validate_spec(data, filename)` |
| `AtomicResolver` | class | `modules/atomic_resolver.py:219` | `class AtomicResolver` |
| `AtomicTest` | class | `modules/atomic_resolver.py:131` | `class AtomicTest` |
| `__init__` | method | `modules/atomic_resolver.py:226` | `def __init__(self, atomics_dir)` |
| `_safe_yaml_files` | function | `modules/atomic_resolver.py:171` | `def _safe_yaml_files(atomics_dir)` |
| `_test_from_raw` | function | `modules/atomic_resolver.py:192` | `def _test_from_raw(test, mitre_id)` |
| `available` | method | `modules/atomic_resolver.py:233` | `def available(self)` |
| `build_index` | method | `modules/atomic_resolver.py:265` | `def build_index(self, force)` |
| `build_variables` | function | `modules/atomic_resolver.py:452` | `def build_variables(test, rhost, domain, rport, username, password)` |
| `chain` | method | `modules/atomic_resolver.py:380` | `def chain(self, techniques, platform, first_match_only)` |
| `ensure_repo` | method | `modules/atomic_resolver.py:237` | `def ensure_repo(self)` |
| `get_by_guid` | method | `modules/atomic_resolver.py:311` | `def get_by_guid(self, guid)` |
| `get_resolver` | function | `modules/atomic_resolver.py:424` | `def get_resolver(atomics_dir)` |
| `guids_for_technique` | method | `modules/atomic_resolver.py:305` | `def guids_for_technique(self, mitre_id)` |
| `is_guid` | function | `modules/atomic_resolver.py:109` | `def is_guid(raw)` |
| `is_mitre_id` | function | `modules/atomic_resolver.py:84` | `def is_mitre_id(raw)` |
| `list_for_technique` | method | `modules/atomic_resolver.py:317` | `def list_for_technique(self, mitre_id, platform)` |
| `mitre_url` | method | `modules/atomic_resolver.py:147` | `def mitre_url(self)` |
| `normalize_guid` | function | `modules/atomic_resolver.py:93` | `def normalize_guid(raw)` |
| `normalize_mitre_id` | function | `modules/atomic_resolver.py:66` | `def normalize_mitre_id(raw)` |
| `normalize_platform` | function | `modules/atomic_resolver.py:118` | `def normalize_platform(raw)` |
| `render_command` | function | `modules/atomic_resolver.py:488` | `def render_command(template, variables)` |
| `resolve` | method | `modules/atomic_resolver.py:334` | `def resolve(self, query, platform)` |
| `resolve_chain` | function | `modules/atomic_resolver.py:442` | `def resolve_chain(techniques, platform, atomics_dir)` |
| `resolve_technique` | function | `modules/atomic_resolver.py:432` | `def resolve_technique(mitre_id, platform, atomics_dir)` |
| `stats` | method | `modules/atomic_resolver.py:415` | `def stats(self)` |
| `technique_env_override` | function | `modules/atomic_resolver.py:496` | `def technique_env_override()` |
| `to_dict` | method | `modules/atomic_resolver.py:151` | `def to_dict(self)` |
| `_doc` | function | `modules/attack_surface3d.py:347` | `def _doc(node)` |
| `_enrich` | function | `modules/attack_surface3d.py:385` | `def _enrich(nodes, edges)` |
| `_family_color` | function | `modules/attack_surface3d.py:101` | `def _family_color(name)` |
| `_host_of` | function | `modules/attack_surface3d.py:142` | `def _host_of(node)` |
| `_intel_id_map` | function | `modules/attack_surface3d.py:335` | `def _intel_id_map(intel, key_to_id)` |
| `_pagerank` | function | `modules/attack_surface3d.py:112` | `def _pagerank(ids, pairs, alpha, max_iter, tol)` |
| `_symbols` | function | `modules/attack_surface3d.py:366` | `def _symbols(node)` |
| `add_edge` | function | `modules/attack_surface3d.py:156` | `def add_edge(src, dst, kind, evidence, weight)` |
| `build_attack_graph` | function | `modules/attack_surface3d.py:148` | `def build_attack_graph(sessions_dir, payload_path, est_cap)` |
| `refresh_summary` | function | `modules/attack_surface3d.py:480` | `def refresh_summary(graph, sessions_dir)` |
| `tag` | function | `modules/attack_surface3d.py:167` | `def tag(nid, source)` |
| `DecisionPersistence` | class | `modules/auto_loop_memory.py:212` | `class DecisionPersistence` |
| `FailureMemory` | class | `modules/auto_loop_memory.py:53` | `class FailureMemory` |
| `PendingDecision` | class | `modules/auto_loop_memory.py:45` | `class PendingDecision` |
| `__init__` | method | `modules/auto_loop_memory.py:56` | `def __init__(self, filepath)` |
| `__init__` | method | `modules/auto_loop_memory.py:215` | `def __init__(self, filepath)` |
| `__len__` | method | `modules/auto_loop_memory.py:241` | `def __len__(self)` |
| `_load` | method | `modules/auto_loop_memory.py:186` | `def _load(self)` |
| `_load` | method | `modules/auto_loop_memory.py:262` | `def _load(self)` |
| `_trim` | method | `modules/auto_loop_memory.py:159` | `def _trim(self)` |
| `base_of` | method | `modules/auto_loop_memory.py:75` | `def base_of(command)` |
| `blocked_bases` | method | `modules/auto_loop_memory.py:128` | `def blocked_bases(self, target)` |
| `clear_target` | method | `modules/auto_loop_memory.py:140` | `def clear_target(self, target)` |
| `count_for_base` | method | `modules/auto_loop_memory.py:94` | `def count_for_base(self, target, base_command)` |
| `failure_count` | method | `modules/auto_loop_memory.py:89` | `def failure_count(self, target, category, command)` |
| `failure_count_strict` | method | `modules/auto_loop_memory.py:123` | `def failure_count_strict(self, target, key)` |
| `is_blocked` | method | `modules/auto_loop_memory.py:115` | `def is_blocked(self, target, base_command, bonus_key)` |
| `make_key` | method | `modules/auto_loop_memory.py:68` | `def make_key(target, category, command)` |
| `path` | method | `modules/auto_loop_memory.py:63` | `def path(self)` |
| `peek` | method | `modules/auto_loop_memory.py:237` | `def peek(self)` |
| `pop` | method | `modules/auto_loop_memory.py:229` | `def pop(self)` |
| `push` | method | `modules/auto_loop_memory.py:220` | `def push(self, command, reason)` |
| `record_failure` | method | `modules/auto_loop_memory.py:79` | `def record_failure(self, target, category, command)` |
| `sanctioned_bases` | method | `modules/auto_loop_memory.py:146` | `def sanctioned_bases(self, target)` |
| `save` | method | `modules/auto_loop_memory.py:166` | `def save(self)` |
| `save` | method | `modules/auto_loop_memory.py:244` | `def save(self)` |
| `veto_base` | method | `modules/auto_loop_memory.py:105` | `def veto_base(self, target, base_command)` |
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
| `_parse_ai_test` | function | `modules/auto_purple.py:329` | `def _parse_ai_test(output, command, args)` |
| `_parse_alert_check` | function | `modules/auto_purple.py:374` | `def _parse_alert_check(output, command, args)` |
| `_parse_fim_check` | function | `modules/auto_purple.py:388` | `def _parse_fim_check(output, command, args)` |
| `_parse_keyword_match` | function | `modules/auto_purple.py:342` | `def _parse_keyword_match(output, command, args)` |
| `_query_blue` | method | `modules/auto_purple.py:635` | `def _query_blue(self, command, args)` |
| `_run_bt_command` | function | `modules/auto_purple.py:225` | `def _run_bt_command(bt_path, command, timeout)` |
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
| `get_loop` | function | `modules/auto_purple.py:772` | `def get_loop(bt_path, detection_delay, methods, auto_feedback)` |
| `last_results` | method | `modules/auto_purple.py:214` | `def last_results(self, n)` |
| `last_results` | method | `modules/auto_purple.py:596` | `def last_results(self, n)` |
| `load_config_from_payload` | function | `modules/auto_purple.py:790` | `def load_config_from_payload(params)` |
| `measure_only` | method | `modules/auto_purple.py:193` | `def measure_only(self, command, args, category)` |
| `measure_only` | method | `modules/auto_purple.py:493` | `def measure_only(self, command, args, category)` |
| `to_csv_row` | method | `modules/auto_purple.py:146` | `def to_csv_row(self)` |
| `to_dict` | method | `modules/auto_purple.py:160` | `def to_dict(self)` |
| `AutoVerb` | class | `modules/auto_registry.py:102` | `class AutoVerb` |
| `ShellResult` | class | `modules/auto_registry.py:907` | `class ShellResult` |
| `_TeeCapture` | class | `modules/auto_registry.py:914` | `class _TeeCapture(StringIO)` |
| `__init__` | method | `modules/auto_registry.py:924` | `def __init__(self, observer)` |
| `_apt_chain_steps` | function | `modules/auto_registry.py:756` | `def _apt_chain_steps(embedded, target, strict)` |
| `_atomic_steps` | function | `modules/auto_registry.py:722` | `def _atomic_steps(verb, text)` |
| `_cli_verb_allowed` | function | `modules/auto_registry.py:383` | `def _cli_verb_allowed(name)` |
| `_invoke` | function | `modules/auto_registry.py:965` | `def _invoke()` |
| `_kill` | function | `modules/auto_registry.py:1117` | `def _kill()` |
| `_looks_like_target` | function | `modules/auto_registry.py:37` | `def _looks_like_target(value)` |
| `_os_default_for_verb` | function | `modules/auto_registry.py:246` | `def _os_default_for_verb(verb)` |
| `_parse_trigger_lines` | function | `modules/auto_registry.py:474` | `def _parse_trigger_lines(lines, start)` |
| `_playbook_steps` | function | `modules/auto_registry.py:741` | `def _playbook_steps(text)` |
| `_register_process` | function | `modules/auto_registry.py:1040` | `def _register_process(process)` |
| `_repo_base` | function | `modules/auto_registry.py:411` | `def _repo_base()` |
| `_target` | function | `modules/auto_registry.py:976` | `def _target()` |
| `_unregister_process` | function | `modules/auto_registry.py:1046` | `def _unregister_process(process)` |
| `_verb_row` | function | `modules/auto_registry.py:299` | `def _verb_row(name)` |
| `_verb_rows` | function | `modules/auto_registry.py:254` | `def _verb_rows()` |
| `addon_hits_for` | function | `modules/auto_registry.py:564` | `def addon_hits_for(service_text, limit)` |
| `auto_verb_target` | function | `modules/auto_registry.py:66` | `def auto_verb_target(command)` |
| `binary_available` | function | `modules/auto_registry.py:418` | `def binary_available(name)` |
| `build_command` | function | `modules/auto_registry.py:681` | `def build_command(verb, target)` |
| `cancel_running_commands` | function | `modules/auto_registry.py:1062` | `def cancel_running_commands()` |
| `execute_shell_verb` | function | `modules/auto_registry.py:942` | `def execute_shell_verb(shell, command, timeout_sec, on_output)` |
| `execute_streaming` | function | `modules/auto_registry.py:1085` | `def execute_streaming(command, on_output, timeout_sec)` |
| `is_routable_command` | function | `modules/auto_registry.py:634` | `def is_routable_command(line)` |
| `is_shell_verb` | function | `modules/auto_registry.py:657` | `def is_shell_verb(token)` |
| `iter_addon_triggers` | function | `modules/auto_registry.py:505` | `def iter_addon_triggers()` |
| `iter_tool_triggers` | function | `modules/auto_registry.py:541` | `def iter_tool_triggers()` |
| `missing_binary` | function | `modules/auto_registry.py:434` | `def missing_binary(command)` |
| `propose_addon_intents` | function | `modules/auto_registry.py:590` | `def propose_addon_intents(service_texts, target, limit)` |
| `propose_intents` | function | `modules/auto_registry.py:698` | `def propose_intents(goal, target, finding_texts)` |
| `service_tokens` | function | `modules/auto_registry.py:463` | `def service_tokens(service_text)` |
| `steps_for` | function | `modules/auto_registry.py:784` | `def steps_for(text, target)` |
| `track_process` | function | `modules/auto_registry.py:1052` | `def track_process(process)` |
| `untrack_process` | function | `modules/auto_registry.py:1057` | `def untrack_process(process)` |
| `verb_available` | function | `modules/auto_registry.py:458` | `def verb_available(verb)` |
| `verb_enabled` | function | `modules/auto_registry.py:308` | `def verb_enabled(name)` |
| `verb_gap` | function | `modules/auto_registry.py:446` | `def verb_gap(verb)` |
| `verbs` | function | `modules/auto_registry.py:652` | `def verbs()` |
| `verbs_for` | function | `modules/auto_registry.py:692` | `def verbs_for(text)` |
| `write` | method | `modules/auto_registry.py:929` | `def write(self, data)` |
| `AutonomousExploitEngine` | class | `modules/autonomous_exploit_engine.py:101` | `class AutonomousExploitEngine` |
| `ExploitCandidate` | class | `modules/autonomous_exploit_engine.py:74` | `class ExploitCandidate` |
| `ExploitResult` | class | `modules/autonomous_exploit_engine.py:89` | `class ExploitResult` |
| `TargetProfile` | class | `modules/autonomous_exploit_engine.py:59` | `class TargetProfile` |
| `__init__` | method | `modules/autonomous_exploit_engine.py:114` | `def __init__(self)` |
| `_apply_stealth_delay` | method | `modules/autonomous_exploit_engine.py:1730` | `def _apply_stealth_delay(self)` |
| `_build_command_chain` | method | `modules/autonomous_exploit_engine.py:1176` | `def _build_command_chain(self, candidate, profile)` |
| `_check_known_cves` | method | `modules/autonomous_exploit_engine.py:2030` | `def _check_known_cves(self, profile)` |
| `_check_success` | method | `modules/autonomous_exploit_engine.py:1328` | `def _check_success(self, output, candidate)` |
| `_credential_aware_rank` | method | `modules/autonomous_exploit_engine.py:241` | `def _credential_aware_rank(self, profile, credentials)` |
| `_detect_os_from_payload` | method | `modules/autonomous_exploit_engine.py:1617` | `def _detect_os_from_payload(self)` |
| `_detect_shell` | method | `modules/autonomous_exploit_engine.py:1421` | `def _detect_shell(self, output)` |
| `_determine_access_level` | method | `modules/autonomous_exploit_engine.py:1449` | `def _determine_access_level(self, ip, credentials)` |
| `_discover_internal_interfaces` | method | `modules/autonomous_exploit_engine.py:2551` | `def _discover_internal_interfaces(self, profile)` |
| `_execute_privesc` | method | `modules/autonomous_exploit_engine.py:2386` | `def _execute_privesc(self, technique, profile, session_id)` |
| `_extract_cves_from_text` | method | `modules/autonomous_exploit_engine.py:1802` | `def _extract_cves_from_text(self, text)` |
| `_filter_placeholder_creds` | method | `modules/autonomous_exploit_engine.py:284` | `def _filter_placeholder_creds(credentials)` |
| `_get_os_type` | method | `modules/autonomous_exploit_engine.py:1714` | `def _get_os_type(self, profile)` |
| `_get_stealth_scan_flags` | method | `modules/autonomous_exploit_engine.py:2657` | `def _get_stealth_scan_flags(self)` |
| `_heuristic_match` | method | `modules/autonomous_exploit_engine.py:512` | `def _heuristic_match(self, service, product, version)` |
| `_is_placeholder` | function | `modules/autonomous_exploit_engine.py:299` | `def _is_placeholder(value)` |
| `_load_from_nmap_xml` | method | `modules/autonomous_exploit_engine.py:1635` | `def _load_from_nmap_xml(self, target)` |
| `_load_payload_config` | method | `modules/autonomous_exploit_engine.py:1507` | `def _load_payload_config(self)` |
| `_load_world_model` | method | `modules/autonomous_exploit_engine.py:1518` | `def _load_world_model(self, target)` |
| `_match_by_port` | method | `modules/autonomous_exploit_engine.py:1016` | `def _match_by_port(self, port, os_type)` |
| `_match_exploit_db` | method | `modules/autonomous_exploit_engine.py:474` | `def _match_exploit_db(self, service, product, version)` |
| `_match_privesc_techniques` | method | `modules/autonomous_exploit_engine.py:2196` | `def _match_privesc_techniques(self, findings, os_type)` |
| `_match_service_banners` | method | `modules/autonomous_exploit_engine.py:1850` | `def _match_service_banners(self, profile)` |
| `_parse_nse_output` | method | `modules/autonomous_exploit_engine.py:1767` | `def _parse_nse_output(self, target_ip)` |
| `_register_session` | method | `modules/autonomous_exploit_engine.py:1479` | `def _register_session(self, ip, output)` |
| `_resolve_port` | method | `modules/autonomous_exploit_engine.py:1159` | `def _resolve_port(self, candidate, profile)` |
| `_run_exploit` | method | `modules/autonomous_exploit_engine.py:1113` | `def _run_exploit(self, candidate, profile)` |
| `_run_linux_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2084` | `def _run_linux_privesc_checks(self, profile, session_id)` |
| `_run_windows_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2153` | `def _run_windows_privesc_checks(self, profile, session_id)` |
| `_scorer` | method | `modules/autonomous_exploit_engine.py:1073` | `def _scorer(self, exploit, service, product, version)` |
| `chain_privesc` | method | `modules/autonomous_exploit_engine.py:2056` | `def chain_privesc(self, profile, session_id)` |
| `enable_stealth` | method | `modules/autonomous_exploit_engine.py:2612` | `def enable_stealth(self, stealth_level)` |
| `execute_candidate` | method | `modules/autonomous_exploit_engine.py:412` | `def execute_candidate(self, candidate, profile)` |
| `full_auto_pwn` | method | `modules/autonomous_exploit_engine.py:2676` | `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth)` |
| `get_instance` | method | `modules/autonomous_exploit_engine.py:134` | `def get_instance(cls)` |
| `hunt` | method | `modules/autonomous_exploit_engine.py:145` | `def hunt(self, target, max_exploits, profile)` |
| `profile` | method | `modules/autonomous_exploit_engine.py:328` | `def profile(self, target)` |
| `rank_exploits` | method | `modules/autonomous_exploit_engine.py:389` | `def rank_exploits(self, profile)` |
| `retry_with_credentials` | method | `modules/autonomous_exploit_engine.py:184` | `def retry_with_credentials(self, target, credentials)` |
| `scan_vulnerabilities` | method | `modules/autonomous_exploit_engine.py:1741` | `def scan_vulnerabilities(self, profile)` |
| `trigger_pivot` | method | `modules/autonomous_exploit_engine.py:2486` | `def trigger_pivot(self, profile, session_id)` |
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
| `RUNKEY_NAME` | macro | `modules/backdoor/backdoor.c:17` | `#define RUNKEY_NAME` |
| `Shell` | function | `modules/backdoor/backdoor.c:88` | `void Shell()` |
| `WinMain` | function | `modules/backdoor/backdoor.c:129` | `int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow)` |
| `bootRun` | function | `modules/backdoor/backdoor.c:22` | `int bootRun()` |
| `bzero` | macro | `modules/backdoor/backdoor.c:14` | `#define bzero(p, size)` |
| `str_cut` | function | `modules/backdoor/backdoor.c:53` | `char * str_cut(char str[], int slice_from, int slice_to)` |
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
| `generate_bof_execution_command` | function | `modules/beacon_config_builder.py:416` | `def generate_bof_execution_command(bof_name, c2_url, client_id, args, bofs_dir)` |
| `to_config_json` | method | `modules/beacon_config_builder.py:160` | `def to_config_json(self)` |
| `to_dict` | method | `modules/beacon_config_builder.py:185` | `def to_dict(self)` |
| `to_gen_beacon_args` | method | `modules/beacon_config_builder.py:117` | `def to_gen_beacon_args(self)` |
| `to_go_implant_vars` | method | `modules/beacon_config_builder.py:137` | `def to_go_implant_vars(self)` |
| `BeaconHistoryConfig` | class | `modules/beacon_history.py:28` | `class BeaconHistoryConfig` |
| `append_record` | function | `modules/beacon_history.py:82` | `def append_record(record, config)` |
| `read_records` | function | `modules/beacon_history.py:116` | `def read_records(client_id, config)` |
| `records_path` | method | `modules/beacon_history.py:43` | `def records_path(self, client_id)` |
| `records_path` | function | `modules/beacon_history.py:145` | `def records_path(client_id, config)` |
| `sanitize_client_id` | function | `modules/beacon_history.py:70` | `def sanitize_client_id(client_id)` |
| `sessions_dir` | method | `modules/beacon_history.py:39` | `def sessions_dir(self)` |
| `_append_discovery_ledger` | function | `modules/beacon_recon.py:264` | `def _append_discovery_ledger(primary_ip, discovered, sessions_dir)` |
| `_looks_like_ip` | function | `modules/beacon_recon.py:42` | `def _looks_like_ip(value)` |
| `_ports_from` | function | `modules/beacon_recon.py:111` | `def _ports_from(value)` |
| `ingest_beacon_recon` | function | `modules/beacon_recon.py:169` | `def ingest_beacon_recon(primary_ip, discovered_ips, portscan, hostname, user, client_id, sessions_dir)` |
| `parse_beacon_portscan` | function | `modules/beacon_recon.py:94` | `def parse_beacon_portscan(raw, default_host)` |
| `parse_discovered_ips` | function | `modules/beacon_recon.py:50` | `def parse_discovered_ips(raw)` |
| `binario_a_imagen` | function | `modules/bin2img.py:7` | `def binario_a_imagen(binario, imagen_input, imagen_output, block_size)` |
| `main` | function | `modules/bin2img.py:54` | `def main()` |
| `BitMState` | class | `modules/bitm_engine.py:85` | `class BitMState` |

Next: [SYMBOLS_p12.md](SYMBOLS_p12.md)
