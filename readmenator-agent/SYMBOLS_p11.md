# Symbols (page 11 of 43)
Previous: [SYMBOLS_p10.md](SYMBOLS_p10.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
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
| `ExploitCommand` | class | `modules/atomic_exploit_bridge.py:70` | `class ExploitCommand` |
| `ExploitSpec` | class | `modules/atomic_exploit_bridge.py:78` | `class ExploitSpec` |
| `_ShellSession` | class | `modules/atomic_exploit_bridge.py:627` | `class _ShellSession` |
| `__init__` | method | `modules/atomic_exploit_bridge.py:635` | `def __init__(self, target, port, sock, owner)` |
| `_adopt_live_shell` | function | `modules/atomic_exploit_bridge.py:962` | `def _adopt_live_shell(spec, target, port)` |
| `_claim_port` | function | `modules/atomic_exploit_bridge.py:722` | `def _claim_port(spec_id, target, port)` |
| `_destroy_gym` | function | `modules/atomic_exploit_bridge.py:889` | `def _destroy_gym(container)` |
| `_install_missing_binaries` | function | `modules/atomic_exploit_bridge.py:482` | `def _install_missing_binaries(names)` |
| `_read_until` | method | `modules/atomic_exploit_bridge.py:666` | `def _read_until(self, marker, timeout)` |
| `_release_port` | function | `modules/atomic_exploit_bridge.py:740` | `def _release_port(target, port)` |
| `_string_list` | function | `modules/atomic_exploit_bridge.py:128` | `def _string_list(value)` |
| `_wait_port_closed` | function | `modules/atomic_exploit_bridge.py:988` | `def _wait_port_closed(target, port, timeout)` |
| `alive` | method | `modules/atomic_exploit_bridge.py:645` | `def alive(self, timeout)` |
| `auto` | function | `modules/atomic_exploit_bridge.py:323` | `def auto(target, lhost, max_attempts, stop_on_shell, task_id, exploits_dir, scan_dir)` |
| `build_commands` | function | `modules/atomic_exploit_bridge.py:452` | `def build_commands(spec, rhost, lhost, lport, port)` |
| `cleanup_target` | function | `modules/atomic_exploit_bridge.py:831` | `def cleanup_target(target, lhost, hard, gym_container, exploits_dir, staging_dir)` |
| `close` | method | `modules/atomic_exploit_bridge.py:694` | `def close(self)` |
| `close_sessions` | function | `modules/atomic_exploit_bridge.py:793` | `def close_sessions(target)` |
| `detect_shell` | function | `modules/atomic_exploit_bridge.py:470` | `def detect_shell(spec, output)` |
| `emulate` | function | `modules/atomic_exploit_bridge.py:1076` | `def emulate(target, techniques, playbook, platform, lhost, per_technique, exploits_dir, scan_dir, include_manual...` |
| `ensure_session` | function | `modules/atomic_exploit_bridge.py:907` | `def ensure_session(spec, target, lhost)` |
| `interactive_shell` | function | `modules/atomic_exploit_bridge.py:1021` | `def interactive_shell(target, lhost, interactive, exploits_dir)` |
| `live_sessions` | function | `modules/atomic_exploit_bridge.py:774` | `def live_sessions()` |
| `load_all` | function | `modules/atomic_exploit_bridge.py:212` | `def load_all(exploits_dir)` |
| `main` | function | `modules/atomic_exploit_bridge.py:1198` | `def main()` |
| `match_score` | function | `modules/atomic_exploit_bridge.py:267` | `def match_score(spec, service, product, version)` |
| `open_shell` | function | `modules/atomic_exploit_bridge.py:592` | `def open_shell(target, services, lhost, exploits_dir, attempts)` |
| `parse_scan_xml` | function | `modules/atomic_exploit_bridge.py:286` | `def parse_scan_xml(xml_path)` |
| `rank` | function | `modules/atomic_exploit_bridge.py:421` | `def rank(services, exploits_dir)` |
| `record_outcome` | function | `modules/atomic_exploit_bridge.py:1110` | `def record_outcome(spec, target, shell, output, task_id, intent_id, surfaces_dir, port, service, product, version...` |
| `record_shell_outcome` | function | `modules/atomic_exploit_bridge.py:745` | `def record_shell_outcome(target, via)` |
| `remote_exec` | function | `modules/atomic_exploit_bridge.py:1003` | `def remote_exec(spec, target, command, lhost)` |
| `run` | method | `modules/atomic_exploit_bridge.py:652` | `def run(self, command, timeout)` |
| `run_spec` | function | `modules/atomic_exploit_bridge.py:512` | `def run_spec(spec, rhost, lhost, lport, port)` |
| `severity_rank` | method | `modules/atomic_exploit_bridge.py:103` | `def severity_rank(self)` |
| `to_dict` | method | `modules/atomic_exploit_bridge.py:107` | `def to_dict(self)` |
| `validate_spec` | function | `modules/atomic_exploit_bridge.py:136` | `def validate_spec(data, filename)` |
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
| `ShellResult` | class | `modules/auto_registry.py:864` | `class ShellResult` |
| `_TeeCapture` | class | `modules/auto_registry.py:871` | `class _TeeCapture(StringIO)` |
| `__init__` | method | `modules/auto_registry.py:881` | `def __init__(self, observer)` |
| `_apt_chain_steps` | function | `modules/auto_registry.py:726` | `def _apt_chain_steps(embedded, target, strict)` |
| `_atomic_steps` | function | `modules/auto_registry.py:692` | `def _atomic_steps(verb, text)` |
| `_cli_verb_allowed` | function | `modules/auto_registry.py:371` | `def _cli_verb_allowed(name)` |
| `_invoke` | function | `modules/auto_registry.py:922` | `def _invoke()` |
| `_kill` | function | `modules/auto_registry.py:1074` | `def _kill()` |
| `_looks_like_target` | function | `modules/auto_registry.py:37` | `def _looks_like_target(value)` |
| `_parse_trigger_lines` | function | `modules/auto_registry.py:462` | `def _parse_trigger_lines(lines, start)` |
| `_playbook_steps` | function | `modules/auto_registry.py:711` | `def _playbook_steps(text)` |
| `_register_process` | function | `modules/auto_registry.py:997` | `def _register_process(process)` |
| `_repo_base` | function | `modules/auto_registry.py:399` | `def _repo_base()` |
| `_target` | function | `modules/auto_registry.py:933` | `def _target()` |
| `_unregister_process` | function | `modules/auto_registry.py:1003` | `def _unregister_process(process)` |
| `_verb_row` | function | `modules/auto_registry.py:287` | `def _verb_row(name)` |
| `_verb_rows` | function | `modules/auto_registry.py:243` | `def _verb_rows()` |
| `addon_hits_for` | function | `modules/auto_registry.py:552` | `def addon_hits_for(service_text, limit)` |
| `auto_verb_target` | function | `modules/auto_registry.py:66` | `def auto_verb_target(command)` |
| `binary_available` | function | `modules/auto_registry.py:406` | `def binary_available(name)` |
| `build_command` | function | `modules/auto_registry.py:651` | `def build_command(verb, target)` |
| `cancel_running_commands` | function | `modules/auto_registry.py:1019` | `def cancel_running_commands()` |
| `execute_shell_verb` | function | `modules/auto_registry.py:899` | `def execute_shell_verb(shell, command, timeout_sec, on_output)` |
| `execute_streaming` | function | `modules/auto_registry.py:1042` | `def execute_streaming(command, on_output, timeout_sec)` |
| `is_routable_command` | function | `modules/auto_registry.py:604` | `def is_routable_command(line)` |
| `is_shell_verb` | function | `modules/auto_registry.py:627` | `def is_shell_verb(token)` |
| `iter_addon_triggers` | function | `modules/auto_registry.py:493` | `def iter_addon_triggers()` |
| `iter_tool_triggers` | function | `modules/auto_registry.py:529` | `def iter_tool_triggers()` |
| `missing_binary` | function | `modules/auto_registry.py:422` | `def missing_binary(command)` |
| `propose_addon_intents` | function | `modules/auto_registry.py:578` | `def propose_addon_intents(service_texts, target, limit)` |
| `propose_intents` | function | `modules/auto_registry.py:668` | `def propose_intents(goal, target, finding_texts)` |
| `service_tokens` | function | `modules/auto_registry.py:451` | `def service_tokens(service_text)` |
| `steps_for` | function | `modules/auto_registry.py:754` | `def steps_for(text, target)` |
| `track_process` | function | `modules/auto_registry.py:1009` | `def track_process(process)` |
| `untrack_process` | function | `modules/auto_registry.py:1014` | `def untrack_process(process)` |
| `verb_available` | function | `modules/auto_registry.py:446` | `def verb_available(verb)` |
| `verb_enabled` | function | `modules/auto_registry.py:296` | `def verb_enabled(name)` |
| `verb_gap` | function | `modules/auto_registry.py:434` | `def verb_gap(verb)` |
| `verbs` | function | `modules/auto_registry.py:622` | `def verbs()` |
| `verbs_for` | function | `modules/auto_registry.py:662` | `def verbs_for(text)` |
| `write` | method | `modules/auto_registry.py:886` | `def write(self, data)` |
| `AutonomousExploitEngine` | class | `modules/autonomous_exploit_engine.py:101` | `class AutonomousExploitEngine` |
| `ExploitCandidate` | class | `modules/autonomous_exploit_engine.py:74` | `class ExploitCandidate` |
| `ExploitResult` | class | `modules/autonomous_exploit_engine.py:89` | `class ExploitResult` |
| `TargetProfile` | class | `modules/autonomous_exploit_engine.py:59` | `class TargetProfile` |
| `__init__` | method | `modules/autonomous_exploit_engine.py:114` | `def __init__(self)` |
| `_apply_stealth_delay` | method | `modules/autonomous_exploit_engine.py:1728` | `def _apply_stealth_delay(self)` |
| `_build_command_chain` | method | `modules/autonomous_exploit_engine.py:1176` | `def _build_command_chain(self, candidate, profile)` |
| `_check_known_cves` | method | `modules/autonomous_exploit_engine.py:2028` | `def _check_known_cves(self, profile)` |
| `_check_success` | method | `modules/autonomous_exploit_engine.py:1328` | `def _check_success(self, output, candidate)` |
| `_credential_aware_rank` | method | `modules/autonomous_exploit_engine.py:241` | `def _credential_aware_rank(self, profile, credentials)` |
| `_detect_os_from_payload` | method | `modules/autonomous_exploit_engine.py:1615` | `def _detect_os_from_payload(self)` |
| `_detect_shell` | method | `modules/autonomous_exploit_engine.py:1421` | `def _detect_shell(self, output)` |
| `_determine_access_level` | method | `modules/autonomous_exploit_engine.py:1449` | `def _determine_access_level(self, ip, credentials)` |
| `_discover_internal_interfaces` | method | `modules/autonomous_exploit_engine.py:2549` | `def _discover_internal_interfaces(self, profile)` |
| `_execute_privesc` | method | `modules/autonomous_exploit_engine.py:2384` | `def _execute_privesc(self, technique, profile, session_id)` |
| `_extract_cves_from_text` | method | `modules/autonomous_exploit_engine.py:1800` | `def _extract_cves_from_text(self, text)` |
| `_filter_placeholder_creds` | method | `modules/autonomous_exploit_engine.py:284` | `def _filter_placeholder_creds(credentials)` |
| `_get_os_type` | method | `modules/autonomous_exploit_engine.py:1712` | `def _get_os_type(self, profile)` |
| `_get_stealth_scan_flags` | method | `modules/autonomous_exploit_engine.py:2655` | `def _get_stealth_scan_flags(self)` |
| `_heuristic_match` | method | `modules/autonomous_exploit_engine.py:512` | `def _heuristic_match(self, service, product, version)` |
| `_is_placeholder` | function | `modules/autonomous_exploit_engine.py:299` | `def _is_placeholder(value)` |
| `_load_from_nmap_xml` | method | `modules/autonomous_exploit_engine.py:1633` | `def _load_from_nmap_xml(self, target)` |
| `_load_payload_config` | method | `modules/autonomous_exploit_engine.py:1507` | `def _load_payload_config(self)` |
| `_load_world_model` | method | `modules/autonomous_exploit_engine.py:1518` | `def _load_world_model(self, target)` |
| `_match_by_port` | method | `modules/autonomous_exploit_engine.py:1016` | `def _match_by_port(self, port, os_type)` |
| `_match_exploit_db` | method | `modules/autonomous_exploit_engine.py:474` | `def _match_exploit_db(self, service, product, version)` |
| `_match_privesc_techniques` | method | `modules/autonomous_exploit_engine.py:2194` | `def _match_privesc_techniques(self, findings, os_type)` |
| `_match_service_banners` | method | `modules/autonomous_exploit_engine.py:1848` | `def _match_service_banners(self, profile)` |
| `_parse_nse_output` | method | `modules/autonomous_exploit_engine.py:1765` | `def _parse_nse_output(self, target_ip)` |
| `_register_session` | method | `modules/autonomous_exploit_engine.py:1479` | `def _register_session(self, ip, output)` |
| `_resolve_port` | method | `modules/autonomous_exploit_engine.py:1159` | `def _resolve_port(self, candidate, profile)` |
| `_run_exploit` | method | `modules/autonomous_exploit_engine.py:1113` | `def _run_exploit(self, candidate, profile)` |
| `_run_linux_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2082` | `def _run_linux_privesc_checks(self, profile, session_id)` |
| `_run_windows_privesc_checks` | method | `modules/autonomous_exploit_engine.py:2151` | `def _run_windows_privesc_checks(self, profile, session_id)` |
| `_scorer` | method | `modules/autonomous_exploit_engine.py:1073` | `def _scorer(self, exploit, service, product, version)` |
| `chain_privesc` | method | `modules/autonomous_exploit_engine.py:2054` | `def chain_privesc(self, profile, session_id)` |
| `enable_stealth` | method | `modules/autonomous_exploit_engine.py:2610` | `def enable_stealth(self, stealth_level)` |
| `execute_candidate` | method | `modules/autonomous_exploit_engine.py:412` | `def execute_candidate(self, candidate, profile)` |
| `full_auto_pwn` | method | `modules/autonomous_exploit_engine.py:2674` | `def full_auto_pwn(cls, target, enable_pivot, enable_privesc, stealth)` |
| `get_instance` | method | `modules/autonomous_exploit_engine.py:134` | `def get_instance(cls)` |
| `hunt` | method | `modules/autonomous_exploit_engine.py:145` | `def hunt(self, target, max_exploits, profile)` |
| `profile` | method | `modules/autonomous_exploit_engine.py:328` | `def profile(self, target)` |
| `rank_exploits` | method | `modules/autonomous_exploit_engine.py:389` | `def rank_exploits(self, profile)` |
| `retry_with_credentials` | method | `modules/autonomous_exploit_engine.py:184` | `def retry_with_credentials(self, target, credentials)` |
| `scan_vulnerabilities` | method | `modules/autonomous_exploit_engine.py:1739` | `def scan_vulnerabilities(self, profile)` |
| `trigger_pivot` | method | `modules/autonomous_exploit_engine.py:2484` | `def trigger_pivot(self, profile, session_id)` |
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
| `binario_a_imagen` | function | `modules/bin2img.py:7` | `def binario_a_imagen(binario, imagen_input, imagen_output, block_size)` |
| `main` | function | `modules/bin2img.py:54` | `def main()` |
| `BitMState` | class | `modules/bitm_engine.py:85` | `class BitMState` |
| `_build_js_payload` | function | `modules/bitm_engine.py:151` | `def _build_js_payload(payload_name, lhost, lport)` |
| `_check_tool` | function | `modules/bitm_engine.py:168` | `def _check_tool(tool)` |
| `_ensure_bitm_dir` | function | `modules/bitm_engine.py:103` | `def _ensure_bitm_dir()` |
| `_get_default_interface` | function | `modules/bitm_engine.py:195` | `def _get_default_interface()` |
| `_get_gateway_ip` | function | `modules/bitm_engine.py:234` | `def _get_gateway_ip()` |
| `_load_state` | function | `modules/bitm_engine.py:134` | `def _load_state()` |
| `_recommend_method` | function | `modules/bitm_engine.py:180` | `def _recommend_method()` |
| `_save_state` | function | `modules/bitm_engine.py:108` | `def _save_state(state)` |
| `_start_arpspoof` | function | `modules/bitm_engine.py:413` | `def _start_arpspoof(target_ip, gateway_ip, interface, lhost, lport, js_payload, harvest_path)` |
| `_start_bettercap` | function | `modules/bitm_engine.py:354` | `def _start_bettercap(target_ip, gateway_ip, interface, lhost, lport, js_payload, harvest_path)` |
| `bitm_cleanup` | function | `modules/bitm_engine.py:642` | `def bitm_cleanup()` |
| `bitm_harvest_stats` | function | `modules/bitm_engine.py:607` | `def bitm_harvest_stats()` |
| `bitm_inject` | function | `modules/bitm_engine.py:572` | `def bitm_inject(payload_name)` |
| `bitm_start` | function | `modules/bitm_engine.py:257` | `def bitm_start(target_ip, gateway_ip, interface, lhost, lport, method, payloads)` |
| `bitm_status` | function | `modules/bitm_engine.py:539` | `def bitm_status()` |
| `bitm_stop` | function | `modules/bitm_engine.py:481` | `def bitm_stop()` |
| `main` | function | `modules/bitm_engine.py:661` | `def main()` |
| `BofCatalog` | class | `modules/bof_registry.py:157` | `class BofCatalog` |
| `BofCategory` | class | `modules/bof_registry.py:68` | `class BofCategory(str, Enum)` |
| `BofEntry` | class | `modules/bof_registry.py:85` | `class BofEntry` |
| `BofMarketplace` | class | `modules/bof_registry.py:639` | `class BofMarketplace` |
| `BofPlatform` | class | `modules/bof_registry.py:61` | `class BofPlatform(str, Enum)` |
| `BofRegistry` | class | `modules/bof_registry.py:552` | `class BofRegistry` |
| `BofValidator` | class | `modules/bof_registry.py:506` | `class BofValidator` |
| `__init__` | method | `modules/bof_registry.py:559` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `modules/bof_registry.py:651` | `def __init__(self, sessions_dir, catalog)` |
| `_build_default_catalog` | function | `modules/bof_registry.py:265` | `def _build_default_catalog()` |
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
| `C2Server` | class | `modules/c2_agent.py:548` | `class C2Server` |
| `__init__` | method | `modules/c2_agent.py:551` | `def __init__(self, port, user, password)` |
| `_api` | function | `modules/c2_agent.py:662` | `def _api(path, data)` |
| `_ensure_key` | function | `modules/c2_agent.py:375` | `def _ensure_key()` |
| `_pid` | method | `modules/c2_agent.py:556` | `def _pid(self)` |
| `_restore_key_from_snapshot` | function | `modules/c2_agent.py:406` | `def _restore_key_from_snapshot()` |
| `_snapshot_key` | function | `modules/c2_agent.py:429` | `def _snapshot_key(aes_hex)` |
| `_sync_credentials_file` | function | `modules/c2_agent.py:50` | `def _sync_credentials_file(user, password)` |
| `_unverified_context` | function | `modules/c2_agent.py:75` | `def _unverified_context()` |
| `build_agent` | function | `modules/c2_agent.py:354` | `def build_agent(c2_url, client_id, aes_hex, route, sleep)` |
| `client_id_for` | function | `modules/c2_agent.py:85` | `def client_id_for(target)` |
| `deploy` | function | `modules/c2_agent.py:446` | `def deploy(target, c2_base, route, lhost, sleep)` |
| `ensure_http_listener` | method | `modules/c2_agent.py:654` | `def ensure_http_listener(self, http_port, auth)` |
| `read_aes_hex` | function | `modules/c2_agent.py:441` | `def read_aes_hex()` |
| `read_records` | function | `modules/c2_agent.py:517` | `def read_records(client_id, limit)` |
| `start` | method | `modules/c2_agent.py:600` | `def start(self)` |
| `status` | method | `modules/c2_agent.py:568` | `def status(self)` |
| `stop` | method | `modules/c2_agent.py:631` | `def stop(self)` |
| `validate_client_id` | function | `modules/c2_agent.py:91` | `def validate_client_id(raw)` |
| `wait_record` | function | `modules/c2_agent.py:534` | `def wait_record(client_id, command, since, timeout)` |
| `C2Builder` | class | `modules/c2_builder.py:392` | `class C2Builder` |
| `C2Profile` | class | `modules/c2_builder.py:76` | `class C2Profile` |
| `__init__` | method | `modules/c2_builder.py:395` | `def __init__(self, params, sessions_dir, cmd_fn, onecmd_fn, toastr_fn, c2_user, c2_pass)` |
| `_build_compile_commands` | function | `modules/c2_builder.py:310` | `def _build_compile_commands(sessions_dir, profile, gocompiler, compile_flags, main_out, main_src, listener_out...` |
| `_build_context` | function | `modules/c2_builder.py:361` | `def _build_context(sessions_dir)` |
| `_command_output` | function | `modules/c2_builder.py:249` | `def _command_output(argv, timeout)` |
| `_ensure_garble_toolchain` | method | `modules/c2_builder.py:413` | `def _ensure_garble_toolchain(self, go_bin, garble_bin, gocompiler, profile)` |
| `_ensure_go` | function | `modules/c2_builder.py:59` | `def _ensure_go(cmd_fn)` |
| `_garble_matches_toolchain` | function | `modules/c2_builder.py:287` | `def _garble_matches_toolchain(go_bin, garble_bin)` |
| `_go_build_version` | function | `modules/c2_builder.py:268` | `def _go_build_version(go_bin, target)` |
| `_go_string_list` | function | `modules/c2_builder.py:220` | `def _go_string_list(urls)` |
| `_parse_go_version` | function | `modules/c2_builder.py:234` | `def _parse_go_version(text)` |
| `_preflight` | function | `modules/c2_builder.py:160` | `def _preflight(profile)` |
| `_read` | function | `modules/c2_builder.py:641` | `def _read(path_)` |
| `_read_required` | function | `modules/c2_builder.py:648` | `def _read_required(path_)` |
| `_render_template` | function | `modules/c2_builder.py:169` | `def _render_template(content, context)` |
| `_replacer` | function | `modules/c2_builder.py:173` | `def _replacer(match)` |
| `_resolve_fallback_urls` | function | `modules/c2_builder.py:180` | `def _resolve_fallback_urls(params)` |
| `_resolve_go_bin` | function | `modules/c2_builder.py:44` | `def _resolve_go_bin()` |
| `_write` | function | `modules/c2_builder.py:652` | `def _write(path_, content)` |
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
| `_make_aggressive_profile` | function | `modules/c2_profile.py:385` | `def _make_aggressive_profile()` |
| `_make_debug_profile` | function | `modules/c2_profile.py:410` | `def _make_debug_profile()` |
| `_make_default_profile` | function | `modules/c2_profile.py:308` | `def _make_default_profile()` |
| `_make_stealth_profile` | function | `modules/c2_profile.py:339` | `def _make_stealth_profile()` |
| `apply_to_response` | method | `modules/c2_profile.py:529` | `def apply_to_response(profile, response)` |
| `apply_to_session` | method | `modules/c2_profile.py:554` | `def apply_to_session(profile, session)` |
| `build_headers` | method | `modules/c2_profile.py:128` | `def build_headers(self, method)` |
| `from_dict` | method | `modules/c2_profile.py:215` | `def from_dict(d)` |
| `from_yaml` | method | `modules/c2_profile.py:200` | `def from_yaml(path)` |
| `get` | method | `modules/c2_profile.py:473` | `def get(self, name)` |
| `get_beacon_config` | method | `modules/c2_profile.py:567` | `def get_beacon_config(profile)` |

Next: [SYMBOLS_p12.md](SYMBOLS_p12.md)
