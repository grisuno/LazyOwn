# Subsystem: modules (page 1 of 17)
Pages: [KB_modules.md](KB_modules.md), [KB_modules_p2.md](KB_modules_p2.md), [KB_modules_p3.md](KB_modules_p3.md), [KB_modules_p4.md](KB_modules_p4.md), [KB_modules_p5.md](KB_modules_p5.md), [KB_modules_p6.md](KB_modules_p6.md), [KB_modules_p7.md](KB_modules_p7.md), [KB_modules_p8.md](KB_modules_p8.md), [KB_modules_p9.md](KB_modules_p9.md), [KB_modules_p10.md](KB_modules_p10.md), [KB_modules_p11.md](KB_modules_p11.md), [KB_modules_p12.md](KB_modules_p12.md), [KB_modules_p13.md](KB_modules_p13.md), [KB_modules_p14.md](KB_modules_p14.md), [KB_modules_p15.md](KB_modules_p15.md), [KB_modules_p16.md](KB_modules_p16.md), [KB_modules_p17.md](KB_modules_p17.md)

## modules/49803.py
- Doc: Exploit Title: OpenPLC 3 - Remote Code Execution (Authenticated) Date: 25/04/2021 Exploit...
- Layer: utility
- Language: py
- Symbols:
  - `auth` (function, line 43) `def auth()`
  - `injection` (function, line 69) `def injection()`
  - `connection` (function, line 106) `def connection()`

## modules/CVE-2018-15133.php
- Layer: utility
- Language: php

## modules/CVE-2023-28432.py
- Layer: utility
- Language: py
- Symbols:
  - `poc` (function, line 12) `def poc(url)`

## modules/LazyOwnExplorer.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Symbols:
  - `AutocompleteEntry` (class, line 30) `class AutocompleteEntry(Entry)`
  - `LazyOwnGUI` (class, line 104) `class LazyOwnGUI(Tk)`
  - `__init__` (method, line 31) `def __init__(self, get_suggestions_func)`
  - `changed` (method, line 45) `def changed(self, name, index, mode)`
  - `selection` (method, line 68) `def selection(self, event)`
  - `move_up` (method, line 75) `def move_up(self, event)`
  - `move_down` (method, line 87) `def move_down(self, event)`
  - `comparison` (method, line 99) `def comparison(self, pattern)`
  - `__init__` (method, line 105) `def __init__(self)`
  - `create_widgets` (method, line 119) `def create_widgets(self)`
  - `load_parquet_files` (method, line 181) `def load_parquet_files(self)`
  - `get_unique_values` (method, line 241) `def get_unique_values(self)`
  - `search` (method, line 248) `def search(self)`
  - `search_in_parquet` (method, line 267) `def search_in_parquet(self, term)`
  - `on_row_double_click` (method, line 278) `def on_row_double_click(self, event)`
  - `show_row_details` (method, line 283) `def show_row_details(self, row)`
  - `add_new_attack_vector` (method, line 305) `def add_new_attack_vector(self)`
  - `scan_system_for_binaries` (method, line 357) `def scan_system_for_binaries(self)`
  - `show_scan_results` (method, line 374) `def show_scan_results(self, binaries)`
  - `export_to_csv` (method, line 385) `def export_to_csv(self)`
  - `get_suggestions` (function, line 124) `def get_suggestions(term)`
  - `save_new_vector` (function, line 325) `def save_new_vector()`
  - `is_binary` (function, line 358) `def is_binary(file_path)`

## modules/__init__.py
- Layer: utility
- Language: py
- Imported by: `cli/apt_chain_support.py`, `cli/commands/golden_paths.py`, `cli/commands/gym_matrix.py`, `cli/commands/lab.py`, `cli/commands/lazy_creds.py`, `cli/commands/lazy_dorks.py`, `cli/commands/lazy_oob.py`, `cli/commands/lazy_passgen.py`, `cli/commands/lazyops.py`, `cli/commands/netattack.py`, `cli/commands/winbox_gym.py`, `cli/orchestrator_assets_tabs.py`, `cli/session_brief.py`, `lazyc2.py`, `lazyc2/blueprints/orchestrator.py`, `modules/ad_gym.py`, `modules/atomic_exploit_bridge.py`, `modules/attack_surface3d.py`, `modules/auto_registry.py`, `modules/gym_cleanup.py`, `modules/gym_matrix_runner.py`, `modules/gym_winbox_runner.py`, `modules/intel_fusion.py`, `modules/intelligence_engine.py`, `modules/lazy_agent.py`, `modules/lazy_loop.py`, `modules/lazy_runner.py`, `modules/lazypassgen.py`, `modules/loop_triggers.py`, `modules/module_registry.py`, `modules/outcome_bus.py`, `modules/redteam_gym.py`, `modules/sinks/findings.py`, `skills/lazyown_mcp.py`, `skills/lazyown_mcp_opencode.py`, `tests/test_ad_lab_gym.py`, `tests/test_apt_chain_admin.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_autonomous_ops.py`, `tests/test_c2_agent.py`, `tests/test_c2_agent_dual.py`, `tests/test_chain_distill_scope.py`, `tests/test_defense_stages.py`, `tests/test_golden_path.py`, `tests/test_gym_cli.py`, `tests/test_gym_lifecycle.py`, `tests/test_gym_matrix_ctf.py`, `tests/test_gym_registry.py`, `tests/test_harness_mode.py`, `tests/test_intel_fusion.py`, `tests/test_lazy_agent.py`, `tests/test_lazy_bridge_traffic.py`, `tests/test_lazy_creds.py`, `tests/test_lazy_ledger.py`, `tests/test_lazy_oob.py`, `tests/test_lazy_orchestrator.py`, `tests/test_lazy_runner.py`, `tests/test_lazy_runner_fallback.py`, `tests/test_lazy_scope.py`, `tests/test_lazy_worker_safety.py`, `tests/test_lazydorks.py`, `tests/test_lazypassgen.py`, `tests/test_lazypoophish.py`, `tests/test_lazyshortener.py`, `tests/test_llm_orchestrator.py`, `tests/test_loop_auto_orchestrator.py`, `tests/test_loop_budget.py`, `tests/test_loop_cli_catalog.py`, `tests/test_loop_mentions.py`, `tests/test_module_registry_bridge.py`, `tests/test_opencode_mcp_harness.py`, `tests/test_orchestrator_api.py`, `tests/test_orchestrator_yaml.py`, `tests/test_pi_leg.py`, `tests/test_safety_gates.py`, `tests/test_scope_deny_priority.py`, `tests/test_security_sanitizers.py`, `tests/test_session_brief.py`, `tests/test_trigger_policy.py`, `tests/test_ttpscope_bridge.py`, `tests/test_unified_bridge_delegate.py`, `tests/test_verb_catalog.py`, `tests/test_winbox_gym.py`

## modules/ad_gym.py
- Doc: AD lab gym catalogue (Docker Samba DC): index, exploits, chains.
- Layer: utility
- Language: py
- Symbols:
  - `_load_yaml` (function, line 27) `def _load_yaml(path)`
  - `load_index` (function, line 38) `def load_index(path)`
  - `vulnerabilities` (function, line 43) `def vulnerabilities(path)`
  - `get` (function, line 49) `def get(vuln_id, path)`
  - `chain_for` (function, line 58) `def chain_for(vuln_id, path)`
  - `exploit_for` (function, line 68) `def exploit_for(vuln_id, path)`
  - `validate_matrix` (function, line 78) `def validate_matrix(path)`
  - `summary` (function, line 127) `def summary(path)`
  - `readiness` (function, line 146) `def readiness()`
  - `main` (function, line 166) `def main()`
- Depends on: `modules/__init__.py`, `modules/atomic_exploit_bridge.py`, `modules/chain_registry.py`

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
  - `_run` (method, line 93) `def _run(self, args, capture)`
  - `find_certificate_authorities` (method, line 113) `def find_certificate_authorities(self, username, password, domain, dc_ip, hashes)`
  - `_parse_ca_output` (method, line 157) `def _parse_ca_output(output)`
  - `enumerate_templates` (method, line 189) `def enumerate_templates(self, username, password, domain, dc_ip, hashes)`
  - `_parse_template_output` (method, line 232) `def _parse_template_output(self, output)`
  - `request_certificate_esc1` (method, line 268) `def request_certificate_esc1(self, username, password, domain, dc_ip, ca_name, template_name, target_user, output_file)`
  - `request_certificate_esc8` (method, line 322) `def request_certificate_esc8(self, username, password, domain, dc_ip, ca_server, template_name, output_file)`
  - `authenticate_with_certificate` (method, line 367) `def authenticate_with_certificate(self, cert_file, domain, dc_ip, username)`
  - `assess_vulnerability` (method, line 411) `def assess_vulnerability(self, username, password, domain, dc_ip, hashes)`
- Imported by: `cli/commands/exploit_migrated.py`

## modules/addon_updater.py
- Doc: Git update contract for lazyaddons.
- Layer: utility
- Language: py
- Symbols:
  - `AddonUpdateResult` (class, line 33) `class AddonUpdateResult`
  - `_read_addon` (function, line 61) `def _read_addon(path)`
  - `load_addons` (function, line 73) `def load_addons(lazyaddons_dir)`
  - `_safe_target` (function, line 107) `def _safe_target(install_path, root)`
  - `_git` (function, line 135) `def _git(path)`
  - `_worktree_root` (function, line 150) `def _worktree_root(path, repository_root)`
  - `update_addon` (function, line 166) `def update_addon(name, lazyaddons_dir, root, dry_run)`
  - `update_all` (function, line 260) `def update_all(names, lazyaddons_dir, root, dry_run, audit_path)`
  - `_audit` (function, line 315) `def _audit(summary, path)`
  - `to_dict` (method, line 46) `def to_dict(self)`
- Depends on: `core/logging.py`
- Imported by: `cli/commands/lazyops.py`, `cli/commands/marketplace.py`, `tests/test_addon_updater.py`

## modules/agent_runner.py
- Doc: LazyOwn AI Agent - Ultimate Edition Improvements: anti-hang timeout, memory management, argument...
- Layer: utility
- Language: py
- Symbols:
  - `configure_logging` (function, line 64) `def configure_logging(debug)`
  - `AgentTool` (class, line 70) `class AgentTool`
  - `CommandMetadata` (class, line 131) `class CommandMetadata`
  - `ASTToolExtractor` (class, line 138) `class ASTToolExtractor`
  - `_tool_call_snapshot` (function, line 177) `def _tool_call_snapshot(tool_call)`
  - `AgentRunner` (class, line 194) `class AgentRunner`
  - `LazyOwnShellWrapper` (class, line 486) `class LazyOwnShellWrapper`
  - `VulnBotCLI` (class, line 563) `class VulnBotCLI`
  - `interactive_mode` (function, line 624) `def interactive_mode(bot)`
  - `parse_args` (function, line 648) `def parse_args()`
  - `main` (function, line 658) `def main()`
  - `__init__` (method, line 73) `def __init__(self, name, description, func, parameters, required)`
  - `to_api_format` (method, line 81) `def to_api_format(self)`
  - `execute` (method, line 87) `def execute(self)`
  - `extract_commands_from_file` (method, line 142) `def extract_commands_from_file(file_path, prefix)`
  - `__init__` (method, line 197) `def __init__(self, model, system_prompt, max_iterations)`
  - `_reset_history` (method, line 211) `def _reset_history(self)`
  - `_manage_memory` (method, line 214) `def _manage_memory(self)`
  - `register_tool` (method, line 222) `def register_tool(self, tool)`
  - `register_tool_from_instance` (method, line 225) `def register_tool_from_instance(self, func)`
  - `register_tools_from_metadata` (method, line 243) `def register_tools_from_metadata(self, commands, executor)`
  - `get_tools_for_api` (method, line 270) `def get_tools_for_api(self)`
  - `run` (method, line 275) `def run(self, user_input)`
  - `_call_model` (method, line 299) `def _call_model(self)`
  - `_stream_call` (method, line 345) `def _stream_call(self, model_name, messages, max_tokens)`
  - `_emit_delta` (method, line 419) `def _emit_delta(self, kind, text)`
  - `_process_tool_call` (method, line 438) `def _process_tool_call(self, tool_call)`
  - `__init__` (method, line 489) `def __init__(self, script_path)`
  - `_load_shell` (method, line 496) `def _load_shell(self)`
  - `execute_command` (method, line 519) `def execute_command(self, command)`
  - `get_commands_summary` (method, line 556) `def get_commands_summary(self)`
  - `__init__` (method, line 564) `def __init__(self, provider, mode, debug, script_path)`
  - `_load_model` (method, line 576) `def _load_model(self)`
  - `_setup_agent` (method, line 591) `def _setup_agent(self)`
  - `process_request` (method, line 619) `def process_request(self, user_input)`
  - `target` (function, line 526) `def target()`
  - `make_executor` (function, line 247) `def make_executor(cmd_name)`
  - `wrapper` (function, line 248) `def wrapper(command)`
- Depends on: `core/logging.py`, `modules/ai_model.py`, `modules/llm_factory.py`, `modules/logging_config.py`
- Imported by: `modules/lazy_agent.py`, `modules/vulnbot.py`, `tests/test_lazy_streaming.py`

## modules/ai_exploit_chain.py
- Doc: AI-Driven Exploit Chaining Engine.
- Layer: utility
- Language: py
- Symbols:
  - `ExploitChainContext` (class, line 223) `class ExploitChainContext`
  - `AIExploitChainer` (class, line 247) `class AIExploitChainer`
  - `__init__` (method, line 259) `def __init__(self)`
  - `reason` (method, line 285) `def reason(self, context)`
  - `evaluate_failure` (method, line 306) `def evaluate_failure(result)`
  - `select_next_strategy` (method, line 318) `def select_next_strategy(self, context)`
  - `estimate_confidence` (method, line 349) `def estimate_confidence(self, strategy, profile)`
  - `build_chain_plan` (method, line 391) `def build_chain_plan(self, context)`
  - `adapt_chain` (method, line 428) `def adapt_chain(self, context, new_info)`
  - `_ensure` (method, line 487) `def _ensure(context, strategy)`
  - `_parse_shell_hints` (method, line 492) `def _parse_shell_hints(self, output, context)`
- Depends on: `modules/autonomous_exploit_engine.py`
- Imported by: `cli/commands/pwn.py`, `skills/lazyown_mcp.py`

## modules/ai_fallback.py
- Doc: LazyOwn AI Fallback Chain
- Layer: utility
- Language: py
- Symbols:
  - `AIResult` (class, line 108) `class AIResult`
  - `_ollama_available` (function, line 118) `def _ollama_available()`
  - `_best_ollama_model` (function, line 126) `def _best_ollama_model()`
  - `_ollama_call` (function, line 153) `def _ollama_call(model, system, user, max_tokens, temperature)`
  - `_is_quota_error` (function, line 197) `def _is_quota_error(exc)`
  - `_groq_call` (function, line 202) `def _groq_call(api_key, system, user, max_tokens, temperature)`
  - `_toposwarm_call` (function, line 239) `def _toposwarm_call(prompt, system)`
  - `_chain_groq_attempted` (function, line 267) `def _chain_groq_attempted(result)`
  - `call` (function, line 280) `def call(prompt, system, api_key, max_tokens, temperature)`
  - `_fallback_warning` (function, line 349) `def _fallback_warning(orch)`
  - `_summarize_attempts` (function, line 354) `def _summarize_attempts(orch)`
  - `_total_failure_result` (function, line 359) `def _total_failure_result(orch, local_error)`
- Depends on: `modules/llm_factory.py`, `modules/llm_orchestrator.py`, `modules/toposwarm_bridge.py`
- Imported by: `modules/recommender.py`, `modules/timeline_narrator.py`, `tests/test_llm_orchestrator.py`

## modules/ai_model.py
- Doc: Concrete language model backends for LazyOwn.
- Layer: business_logic
- Language: py
- Symbols:
  - `AIModel` (class, line 45) `class AIModel(ABC)`
  - `_LazyImporter` (class, line 97) `class _LazyImporter`
  - `GroqModel` (class, line 129) `class GroqModel(AIModel)`
  - `OllamaModel` (class, line 244) `class OllamaModel(AIModel)`
  - `LlamaCppModel` (class, line 313) `class LlamaCppModel(AIModel)`
  - `OpenAIModel` (class, line 434) `class OpenAIModel(AIModel)`
  - `AnthropicModel` (class, line 493) `class AnthropicModel(AIModel)`
  - `DeepSeekModel` (class, line 549) `class DeepSeekModel(AIModel)`
  - `generate` (method, line 56) `def generate(self, prompt)`
  - `stream_generate` (method, line 60) `def stream_generate(self, prompt)`
  - `complete` (method, line 63) `def complete(self, system, user, max_tokens, temperature)`
  - `groq` (method, line 105) `def groq(cls)`
  - `openai` (method, line 113) `def openai(cls)`
  - `anthropic` (method, line 121) `def anthropic(cls)`
  - `__init__` (method, line 137) `def __init__(self, api_key, model)`
  - `_model_chain` (method, line 141) `def _model_chain(self)`
  - `generate` (method, line 155) `def generate(self, prompt)`
  - `stream_generate` (method, line 183) `def stream_generate(self, prompt)`
  - `complete` (method, line 216) `def complete(self, system, user, max_tokens, temperature)`
  - `__init__` (method, line 252) `def __init__(self, model, host)`
  - `generate` (method, line 260) `def generate(self, prompt)`
  - `stream_generate` (method, line 281) `def stream_generate(self, prompt)`
  - `__init__` (method, line 324) `def __init__(self, model, host)`
  - `_chat` (method, line 341) `def _chat(self, messages, max_tokens, stream)`
  - `generate` (method, line 362) `def generate(self, prompt)`
  - `stream_generate` (method, line 382) `def stream_generate(self, prompt)`
  - `complete` (method, line 413) `def complete(self, system, user, max_tokens, temperature)`
  - `__init__` (method, line 440) `def __init__(self, api_key, model)`
  - `generate` (method, line 444) `def generate(self, prompt)`
  - `stream_generate` (method, line 455) `def stream_generate(self, prompt)`
  - `complete` (method, line 470) `def complete(self, system, user, max_tokens, temperature)`
  - `__init__` (method, line 499) `def __init__(self, api_key, model)`
  - `generate` (method, line 503) `def generate(self, prompt)`
  - `stream_generate` (method, line 515) `def stream_generate(self, prompt)`
  - `complete` (method, line 529) `def complete(self, system, user, max_tokens, temperature)`
  - `__init__` (method, line 556) `def __init__(self, api_key, model)`
  - `generate` (method, line 563) `def generate(self, prompt)`
  - `stream_generate` (method, line 574) `def stream_generate(self, prompt)`
  - `complete` (method, line 589) `def complete(self, system, user, max_tokens, temperature)`
- Depends on: `core/logging.py`, `modules/llm_factory.py`
- Imported by: `contrib/legacy/lazyllmchat.py`, `modules/agent_runner.py`, `modules/llm_client.py`, `modules/llm_factory.py`, `modules/vulnbot.py`, `modules/yaml_generator.py`

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
  - `request` (method, line 11) `def request(self, flow)`

## modules/apt_playbooks.py
- Doc: APT Playbook Engine — map public APT reports to executable Atomic Red Team chains.
- Layer: utility
- Language: py
- Symbols:
  - `AtomicTestRef` (class, line 41) `class AtomicTestRef`
  - `CalderaAbilityRef` (class, line 48) `class CalderaAbilityRef`
  - `PhaseStep` (class, line 54) `class PhaseStep`
  - `AptPlaybook` (class, line 65) `class AptPlaybook`
  - `AptPlaybookEngine` (class, line 111) `class AptPlaybookEngine`
  - `from_dict` (method, line 74) `def from_dict(cls, data)`
  - `to_summary` (method, line 99) `def to_summary(self)`
  - `__init__` (method, line 114) `def __init__(self, playbook_dir)`
  - `_load_all` (method, line 119) `def _load_all(self)`
  - `list_playbooks` (method, line 131) `def list_playbooks(self)`
  - `get` (method, line 134) `def get(self, name)`
  - `validate` (method, line 138) `def validate(self, pb, atomic_path)`
  - `_build_atomic_index` (method, line 199) `def _build_atomic_index(self, atomic_yaml_path)`
  - `generate_attack_plan` (method, line 213) `def generate_attack_plan(self, pb, output_path)`
  - `report_json` (method, line 230) `def report_json(self, pb, output_path)`
- Depends on: `core/console.py`, `modules/atomic_resolver.py`
- Imported by: `cli/commands/command_and_control_migrated.py`, `cli/orchestrator_assets_tabs.py`, `cli/recommendation_signals.py`, `modules/emulation_runner.py`, `modules/operation.py`, `tests/test_atomic_loop.py`, `tests/test_emulation_runner.py`

## modules/asset_graph.py
- Doc: Global asset truth store joined to per-task exploration chains.
- Layer: utility
- Language: py
- Symbols:
  - `GraphConfig` (class, line 17) `class GraphConfig`
  - `asset_key` (function, line 28) `def asset_key(asset_type, value, parent_key)`
  - `AssetNode` (class, line 36) `class AssetNode`
  - `ExplorationNode` (class, line 50) `class ExplorationNode`
  - `Anchor` (class, line 63) `class Anchor`
  - `AssetGraph` (class, line 70) `class AssetGraph`
  - `coverage_for` (function, line 214) `def coverage_for(db, workspace_id, scope)`
  - `__init__` (method, line 73) `def __init__(self, config)`
  - `upsert_asset` (method, line 82) `def upsert_asset(self, asset_type, value, parent_key, company)`
  - `add_node` (method, line 108) `def add_node(self, task_id, kind, text, parent_id, payload)`
  - `add_fact` (method, line 123) `def add_fact(self, task_id, text, parent_id, payload)`
  - `add_finding` (method, line 128) `def add_finding(self, task_id, text, parent_id, payload)`
  - `anchor` (method, line 133) `def anchor(self, exploration_id, key)`
  - `assets_for_node` (method, line 145) `def assets_for_node(self, exploration_id)`
  - `nodes_for_asset` (method, line 151) `def nodes_for_asset(self, key)`
  - `coverage` (method, line 157) `def coverage(self, task_id)`
  - `mirror_to_campaign` (method, line 170) `def mirror_to_campaign(self, db, world_model, workspace_id)`
- Imported by: `skills/autonomous_daemon.py`, `tests/test_autonomous_ops.py`

## modules/atomic_cli.py
- Doc: Non-interactive, agent-safe implementation for atomic_tests / atomic_gen.
- Layer: utility
- Language: py
- Symbols:
  - `parse_atomic_line` (function, line 37) `def parse_atomic_line(line)`
  - `_resolver` (function, line 99) `def _resolver()`
  - `_print` (function, line 107) `def _print(shell, text)`
  - `_warn` (function, line 118) `def _warn(text)`
  - `_wants_interactive` (function, line 127) `def _wants_interactive(non_interactive)`
  - `_safe_copy` (function, line 132) `def _safe_copy(text)`
  - `_load_credentials` (function, line 147) `def _load_credentials(params, non_interactive)`
  - `_prompt_choice` (function, line 171) `def _prompt_choice(count, prompt, non_interactive)`
  - `run_atomic_tests` (function, line 185) `def run_atomic_tests(params, line, shell)`
  - `_sanitized_script_name` (function, line 319) `def _sanitized_script_name(test_id, extension)`
  - `run_atomic_gen` (function, line 325) `def run_atomic_gen(params, line, shell)`
- Depends on: `core/console.py`, `core/hardening.py`, `core/logging.py`, `modules/atomic_resolver.py`, `utils.py`
- Imported by: `cli/commands/command_and_control_migrated.py`

## modules/atomic_enricher.py
- Doc: — Enrich techniques.parquet with structured derived columns.
- Layer: utility
- Language: py
- Symbols:
  - `_parse_platforms` (function, line 122) `def _parse_platforms(raw)`
  - `_parse_scope` (function, line 135) `def _parse_scope(name)`
  - `_parse_complexity` (function, line 142) `def _parse_complexity(command)`
  - `_parse_keyword_tags` (function, line 152) `def _parse_keyword_tags(name, description)`
  - `_tactic_prefix` (function, line 164) `def _tactic_prefix(mitre_id)`
  - `enrich` (function, line 173) `def enrich(force)`
  - `_to_pylist` (function, line 204) `def _to_pylist(val)`
  - `load_enriched` (function, line 215) `def load_enriched()`
  - `query_atomic` (function, line 232) `def query_atomic(keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)`
- Depends on: `core/logging.py`
- Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `skills/lazyown_parquet_db.py`, `tests/test_core_modules.py`

## modules/atomic_exploit_bridge.py
- Doc: Atomic exploit catalogue bridge — one YAML per exploit under ``exploits/``.
- Layer: utility
- Language: py
- Symbols:
  - `ExploitCommand` (class, line 84) `class ExploitCommand`
  - `ExploitSpec` (class, line 92) `class ExploitSpec`
  - `_string_list` (function, line 142) `def _string_list(value)`
  - `validate_spec` (function, line 150) `def validate_spec(data, filename)`
  - `load_all` (function, line 226) `def load_all(exploits_dir)`
  - `match_score` (function, line 281) `def match_score(spec, service, product, version, os_hint)`
  - `parse_scan_xml` (function, line 314) `def parse_scan_xml(xml_path)`
  - `auto` (function, line 351) `def auto(target, lhost, max_attempts, stop_on_shell, task_id, exploits_dir, scan_dir)`
  - `rank` (function, line 456) `def rank(services, exploits_dir, os_hint)`
  - `_token_mapping` (function, line 511) `def _token_mapping(rhost, lhost, lport, port)`
  - `build_commands` (function, line 525) `def build_commands(spec, rhost, lhost, lport, port)`
  - `detect_shell` (function, line 543) `def detect_shell(spec, output)`
  - `_install_missing_binaries` (function, line 555) `def _install_missing_binaries(names)`
  - `run_spec` (function, line 585) `def run_spec(spec, rhost, lhost, lport, port)`
  - `open_shell` (function, line 665) `def open_shell(target, services, lhost, exploits_dir, attempts, privilege)`
  - `_ShellSession` (class, line 721) `class _ShellSession`
  - `_claim_port` (function, line 816) `def _claim_port(spec_id, target, port)`
  - `_release_port` (function, line 834) `def _release_port(target, port)`
  - `record_shell_outcome` (function, line 839) `def record_shell_outcome(target, via)`
  - `live_sessions` (function, line 868) `def live_sessions()`
  - `close_sessions` (function, line 887) `def close_sessions(target)`
  - `cleanup_target` (function, line 929) `def cleanup_target(target, lhost, hard, gym_container, exploits_dir, staging_dir)`
  - `_destroy_gym` (function, line 988) `def _destroy_gym(container)`
  - `ensure_session` (function, line 1006) `def ensure_session(spec, target, lhost)`
  - `_adopt_live_shell` (function, line 1061) `def _adopt_live_shell(spec, target, port)`
  - `_wait_port_closed` (function, line 1087) `def _wait_port_closed(target, port, timeout)`
  - `remote_exec` (function, line 1102) `def remote_exec(spec, target, command, lhost)`
  - `interactive_shell` (function, line 1120) `def interactive_shell(target, lhost, interactive, exploits_dir)`
  - `emulate` (function, line 1175) `def emulate(target, techniques, playbook, platform, lhost, per_technique, exploits_dir, scan_dir, include_manual...`
  - `record_outcome` (function, line 1209) `def record_outcome(spec, target, shell, output, task_id, intent_id, surfaces_dir, port, service, product, version...`
  - `main` (function, line 1297) `def main()`
  - `severity_rank` (method, line 117) `def severity_rank(self)`
  - `to_dict` (method, line 121) `def to_dict(self)`
  - `__init__` (method, line 729) `def __init__(self, target, port, sock, owner)`
  - `alive` (method, line 739) `def alive(self, timeout)`
  - `run` (method, line 746) `def run(self, command, timeout)`
  - `_read_until` (method, line 760) `def _read_until(self, marker, timeout)`
  - `close` (method, line 788) `def close(self)`
- Depends on: `core/config.py`, `core/logging.py`, `core/safe_exec.py`, `modules/__init__.py`, `modules/c2_surfaces.py`, `modules/emulation_runner.py`, `modules/lazy_cve_feed.py`, `modules/lazy_heat.py`, `modules/outcome_bus.py`, `modules/world_model.py`
- Imported by: `cli/commands/command_and_control_migrated.py`, `modules/ad_gym.py`, `modules/autonomous_exploit_engine.py`, `modules/c2_agent.py`, `modules/emulation_runner.py`, `modules/metasploitable_gym.py`, `modules/redteam_gym.py`, `modules/winbox_gym.py`, `skills/lazyown_mcp.py`, `tests/test_atomic_exploit_bridge.py`, `tests/test_c2_surfaces.py`, `tests/test_emulation_runner.py`, `tests/test_gym_cli.py`, `tests/test_metasploitable_gym.py`, `tests/test_outcome_bus.py`

## modules/atomic_resolver.py
- Doc: Central MITRE ATT&CK <-> Atomic Red Team translator.
- Layer: utility
- Language: py
- Symbols:
  - `normalize_mitre_id` (function, line 66) `def normalize_mitre_id(raw)`
  - `is_mitre_id` (function, line 84) `def is_mitre_id(raw)`
  - `normalize_guid` (function, line 93) `def normalize_guid(raw)`
  - `is_guid` (function, line 109) `def is_guid(raw)`
  - `normalize_platform` (function, line 118) `def normalize_platform(raw)`
  - `AtomicTest` (class, line 131) `class AtomicTest`
  - `_safe_yaml_files` (function, line 171) `def _safe_yaml_files(atomics_dir)`
  - `_test_from_raw` (function, line 192) `def _test_from_raw(test, mitre_id)`
  - `AtomicResolver` (class, line 219) `class AtomicResolver`
  - `get_resolver` (function, line 424) `def get_resolver(atomics_dir)`
  - `resolve_technique` (function, line 432) `def resolve_technique(mitre_id, platform, atomics_dir)`
  - `resolve_chain` (function, line 442) `def resolve_chain(techniques, platform, atomics_dir)`
  - `build_variables` (function, line 452) `def build_variables(test, rhost, domain, rport, username, password)`
  - `render_command` (function, line 488) `def render_command(template, variables)`
  - `technique_env_override` (function, line 496) `def technique_env_override()`
  - `mitre_url` (method, line 147) `def mitre_url(self)`
  - `to_dict` (method, line 151) `def to_dict(self)`
  - `__init__` (method, line 226) `def __init__(self, atomics_dir)`
  - `available` (method, line 233) `def available(self)`
  - `ensure_repo` (method, line 237) `def ensure_repo(self)`
  - `build_index` (method, line 265) `def build_index(self, force)`
  - `guids_for_technique` (method, line 305) `def guids_for_technique(self, mitre_id)`
  - `get_by_guid` (method, line 311) `def get_by_guid(self, guid)`
  - `list_for_technique` (method, line 317) `def list_for_technique(self, mitre_id, platform)`
  - `resolve` (method, line 334) `def resolve(self, query, platform)`
  - `chain` (method, line 380) `def chain(self, techniques, platform, first_match_only)`
  - `stats` (method, line 415) `def stats(self)`
- Depends on: `core/logging.py`, `core/safe_exec.py`
- Imported by: `cli/commands/command_and_control_migrated.py`, `modules/apt_playbooks.py`, `modules/atomic_cli.py`, `modules/emulation_runner.py`, `modules/ttpscope_bridge.py`, `skills/lazyown_mcp.py`, `tests/test_atomic_loop.py`, `tests/test_atomic_resolver.py`

## modules/attack_surface3d.py
- Doc: Attack-surface 3D intel module: C2-centred campaign graph.
- Layer: utility
- Language: py
- Symbols:
  - `_family_color` (function, line 101) `def _family_color(name)`
  - `_pagerank` (function, line 112) `def _pagerank(ids, pairs, alpha, max_iter, tol)`
  - `_host_of` (function, line 142) `def _host_of(node)`
  - `build_attack_graph` (function, line 148) `def build_attack_graph(sessions_dir, payload_path, est_cap)`
  - `_intel_id_map` (function, line 335) `def _intel_id_map(intel, key_to_id)`
  - `_doc` (function, line 347) `def _doc(node)`
  - `_symbols` (function, line 366) `def _symbols(node)`
  - `_enrich` (function, line 385) `def _enrich(nodes, edges)`
  - `refresh_summary` (function, line 480) `def refresh_summary(graph, sessions_dir)`
  - `add_edge` (function, line 156) `def add_edge(src, dst, kind, evidence, weight)`
  - `tag` (function, line 167) `def tag(nid, source)`
- Depends on: `cli/surface_graph.py`, `modules/__init__.py`, `modules/estorides_fusion.py`, `modules/finding_lifecycle.py`, `modules/intel_fusion.py`
- Imported by: `cli/commands/surface.py`, `lazyc2.py`, `modules/sinks/attack_graph.py`, `tests/test_attack_surface3d.py`

## modules/auto_loop_memory.py
- Doc: Persistent memory for the auto loop.
- Layer: utility
- Language: py
- Symbols:
  - `PendingDecision` (class, line 45) `class PendingDecision`
  - `FailureMemory` (class, line 53) `class FailureMemory`
  - `DecisionPersistence` (class, line 212) `class DecisionPersistence`
  - `__init__` (method, line 56) `def __init__(self, filepath)`
  - `path` (method, line 63) `def path(self)`
  - `make_key` (method, line 68) `def make_key(target, category, command)`
  - `base_of` (method, line 75) `def base_of(command)`
  - `record_failure` (method, line 79) `def record_failure(self, target, category, command)`
  - `failure_count` (method, line 89) `def failure_count(self, target, category, command)`
  - `count_for_base` (method, line 94) `def count_for_base(self, target, base_command)`
  - `veto_base` (method, line 105) `def veto_base(self, target, base_command)`
  - `is_blocked` (method, line 115) `def is_blocked(self, target, base_command, bonus_key)`
  - `failure_count_strict` (method, line 123) `def failure_count_strict(self, target, key)`
  - `blocked_bases` (method, line 128) `def blocked_bases(self, target)`
  - `clear_target` (method, line 140) `def clear_target(self, target)`
  - `sanctioned_bases` (method, line 146) `def sanctioned_bases(self, target)`
  - `_trim` (method, line 159) `def _trim(self)`
  - `save` (method, line 166) `def save(self)`
  - `_load` (method, line 186) `def _load(self)`
  - `__init__` (method, line 215) `def __init__(self, filepath)`
  - `push` (method, line 220) `def push(self, command, reason)`
  - `pop` (method, line 229) `def pop(self)`
  - `peek` (method, line 237) `def peek(self)`
  - `__len__` (method, line 241) `def __len__(self)`
  - `save` (method, line 244) `def save(self)`
  - `_load` (method, line 262) `def _load(self)`
- Imported by: `modules/lazy_loop.py`, `tests/test_auto_loop_memory.py`, `tests/test_failure_memory_veto.py`


Next: [KB_modules_p2.md](KB_modules_p2.md)
