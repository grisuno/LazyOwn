# Symbols (page 19 of 43)
Previous: [SYMBOLS_p18.md](SYMBOLS_p18.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_local_executor` | function | `modules/playbook_engine.py:722` | `def _local_executor(command, host)` |
| `_obs_parser` | method | `modules/playbook_engine.py:415` | `def _obs_parser(self)` |
| `_world_model` | method | `modules/playbook_engine.py:404` | `def _world_model(self)` |
| `available` | method | `modules/playbook_engine.py:192` | `def available(self)` |
| `available` | method | `modules/playbook_engine.py:264` | `def available(self)` |
| `build` | method | `modules/playbook_engine.py:267` | `def build(self)` |
| `derive` | method | `modules/playbook_engine.py:427` | `def derive(self, target, phase, platform, apt_name)` |
| `execute` | method | `modules/playbook_engine.py:529` | `def execute(self, playbook, executor, dry_run)` |
| `from_dict` | method | `modules/playbook_engine.py:128` | `def from_dict(cls, d)` |
| `from_dict` | method | `modules/playbook_engine.py:152` | `def from_dict(cls, d)` |
| `get_engine` | function | `modules/playbook_engine.py:669` | `def get_engine(api_key)` |
| `load` | method | `modules/playbook_engine.py:611` | `def load(self, path)` |
| `result_summary` | method | `modules/playbook_engine.py:640` | `def result_summary(self, result)` |
| `save` | method | `modules/playbook_engine.py:599` | `def save(self, playbook, path)` |
| `select` | method | `modules/playbook_engine.py:317` | `def select(self, candidates, world_context, target, phase, api_key, top_n)` |
| `store` | method | `modules/playbook_engine.py:195` | `def store(self)` |
| `techniques_for_tactics` | method | `modules/playbook_engine.py:210` | `def techniques_for_tactics(self, tactic_shortnames, platform)` |
| `tests_for_technique` | method | `modules/playbook_engine.py:300` | `def tests_for_technique(self, technique_id, platform)` |
| `to_dict` | method | `modules/playbook_engine.py:113` | `def to_dict(self)` |
| `to_dict` | method | `modules/playbook_engine.py:141` | `def to_dict(self)` |
| `DefaultTTPMapper` | class | `modules/playbook_executor.py:101` | `class DefaultTTPMapper(ITTPMapper)` |
| `ITTPMapper` | class | `modules/playbook_executor.py:93` | `class ITTPMapper(ABC)` |
| `PlaybookEngine` | class | `modules/playbook_executor.py:336` | `class PlaybookEngine` |
| `PlaybookLoader` | class | `modules/playbook_executor.py:203` | `class PlaybookLoader` |
| `PlaybookRunResult` | class | `modules/playbook_executor.py:61` | `class PlaybookRunResult` |
| `PlaybookSpec` | class | `modules/playbook_executor.py:48` | `class PlaybookSpec` |
| `PlaybookTechnique` | class | `modules/playbook_executor.py:36` | `class PlaybookTechnique` |
| `__init__` | method | `modules/playbook_executor.py:208` | `def __init__(self, playbooks_dir)` |
| `__init__` | method | `modules/playbook_executor.py:339` | `def __init__(self, loader, mapper, pipelines_dir)` |
| `_build_pipeline_yaml` | function | `modules/playbook_executor.py:285` | `def _build_pipeline_yaml(playbook, mapper, platform)` |
| `_validate` | method | `modules/playbook_executor.py:235` | `def _validate(self, raw, source_path)` |
| `analyze` | method | `modules/playbook_executor.py:353` | `def analyze(self, name, platform)` |
| `generate_pipeline` | method | `modules/playbook_executor.py:378` | `def generate_pipeline(self, name, platform)` |
| `list` | method | `modules/playbook_executor.py:211` | `def list(self)` |
| `load` | method | `modules/playbook_executor.py:224` | `def load(self, name)` |
| `loader` | method | `modules/playbook_executor.py:350` | `def loader(self)` |
| `playbook_analyze` | function | `modules/playbook_executor.py:422` | `def playbook_analyze(name, platform)` |
| `playbook_generate` | function | `modules/playbook_executor.py:429` | `def playbook_generate(name, platform)` |
| `playbook_list` | function | `modules/playbook_executor.py:416` | `def playbook_list()` |
| `playbook_run` | function | `modules/playbook_executor.py:436` | `def playbook_run(name, platform, target, onecmd)` |
| `register` | method | `modules/playbook_executor.py:180` | `def register(cls, technique_id, platform, command)` |
| `resolve` | method | `modules/playbook_executor.py:97` | `def resolve(self, technique_id, atomic_test, platform)` |
| `resolve` | method | `modules/playbook_executor.py:185` | `def resolve(self, technique_id, atomic_test, platform)` |
| `run` | method | `modules/playbook_executor.py:390` | `def run(self, name, platform, target, onecmd)` |
| `to_dict` | method | `modules/playbook_executor.py:74` | `def to_dict(self)` |
| `MutationConfig` | class | `modules/polymorphic_engine.py:93` | `class MutationConfig` |
| `MutationResult` | class | `modules/polymorphic_engine.py:126` | `class MutationResult` |
| `PolymorphicEngine` | class | `modules/polymorphic_engine.py:146` | `class PolymorphicEngine` |
| `__init__` | method | `modules/polymorphic_engine.py:159` | `def __init__(self, config)` |
| `_base64_wrap` | method | `modules/polymorphic_engine.py:330` | `def _base64_wrap(self, data, arch)` |
| `_compress_data` | method | `modules/polymorphic_engine.py:324` | `def _compress_data(self, data)` |
| `_estimate_entropy` | method | `modules/polymorphic_engine.py:344` | `def _estimate_entropy(data)` |
| `_junk_insertion` | method | `modules/polymorphic_engine.py:282` | `def _junk_insertion(self, data, arch)` |
| `_multi_xor_encrypt` | method | `modules/polymorphic_engine.py:309` | `def _multi_xor_encrypt(self, data)` |
| `_nop_insertion` | method | `modules/polymorphic_engine.py:253` | `def _nop_insertion(self, data, arch)` |
| `_nop_substitution` | method | `modules/polymorphic_engine.py:231` | `def _nop_substitution(self, data, arch)` |
| `_register_reassignment` | method | `modules/polymorphic_engine.py:262` | `def _register_reassignment(self, data, arch)` |
| `_single_pass` | method | `modules/polymorphic_engine.py:184` | `def _single_pass(self, data, arch, pass_num, original_size)` |
| `_xor_encrypt` | method | `modules/polymorphic_engine.py:303` | `def _xor_encrypt(self, data, arch)` |
| `decode_multi_xor` | method | `modules/polymorphic_engine.py:377` | `def decode_multi_xor(data)` |
| `decode_xor` | method | `modules/polymorphic_engine.py:361` | `def decode_xor(data)` |
| `generate_decoder_stub` | method | `modules/polymorphic_engine.py:397` | `def generate_decoder_stub(self, arch)` |
| `get_audit_summary` | method | `modules/polymorphic_engine.py:422` | `def get_audit_summary(self)` |
| `mutate` | method | `modules/polymorphic_engine.py:163` | `def mutate(self, shellcode, arch)` |
| `PrivescVector` | class | `modules/privesc_predictor.py:97` | `class PrivescVector` |
| `SystemProfile` | class | `modules/privesc_predictor.py:114` | `class SystemProfile` |
| `_load_gtfobins_map` | function | `modules/privesc_predictor.py:617` | `def _load_gtfobins_map()` |
| `_parse_kernel_version` | function | `modules/privesc_predictor.py:136` | `def _parse_kernel_version(version_str)` |
| `_parse_version_from_range` | function | `modules/privesc_predictor.py:153` | `def _parse_version_from_range(range_str)` |
| `_try_llm_analysis` | function | `modules/privesc_predictor.py:655` | `def _try_llm_analysis(profile)` |
| `analyze_privesc` | function | `modules/privesc_predictor.py:742` | `def analyze_privesc(filepath, text)` |
| `capability_vectors` | function | `modules/privesc_predictor.py:361` | `def capability_vectors(profile)` |
| `cron_vectors` | function | `modules/privesc_predictor.py:578` | `def cron_vectors(profile)` |
| `format_crystal_ball_output` | function | `modules/privesc_predictor.py:827` | `def format_crystal_ball_output(result)` |
| `group_vectors` | function | `modules/privesc_predictor.py:463` | `def group_vectors(profile)` |
| `main` | function | `modules/privesc_predictor.py:908` | `def main()` |
| `match_known_cves` | function | `modules/privesc_predictor.py:249` | `def match_known_cves(profile)` |
| `parse_linpeas_output` | function | `modules/privesc_predictor.py:165` | `def parse_linpeas_output(text)` |
| `parse_winpeas_output` | function | `modules/privesc_predictor.py:218` | `def parse_winpeas_output(text)` |
| `sudo_vectors` | function | `modules/privesc_predictor.py:501` | `def sudo_vectors(profile)` |
| `suid_vectors` | function | `modules/privesc_predictor.py:287` | `def suid_vectors(profile)` |
| `RedTeamReportGenerator` | class | `modules/professional_report.py:114` | `class RedTeamReportGenerator` |
| `ReportFinding` | class | `modules/professional_report.py:87` | `class ReportFinding` |
| `ReportMetadata` | class | `modules/professional_report.py:102` | `class ReportMetadata` |
| `__init__` | method | `modules/professional_report.py:173` | `def __init__(self, include_credentials)` |
| `_accumulate_loot` | method | `modules/professional_report.py:893` | `def _accumulate_loot(self, summary, path)` |
| `_ai_draft_summary` | method | `modules/professional_report.py:956` | `def _ai_draft_summary(self, data, fallback, backend)` |
| `_classify_credentials` | method | `modules/professional_report.py:682` | `def _classify_credentials(self, credentials, hosts)` |
| `_classify_services` | method | `modules/professional_report.py:585` | `def _classify_services(self, services, hosts)` |
| `_classify_sessions` | method | `modules/professional_report.py:758` | `def _classify_sessions(self, sessions, hosts)` |
| `_classify_vulnerabilities` | method | `modules/professional_report.py:640` | `def _classify_vulnerabilities(self, vulns, hosts)` |
| `_extract_scope` | method | `modules/professional_report.py:822` | `def _extract_scope(self, data)` |
| `_generate_html` | method | `modules/professional_report.py:298` | `def _generate_html(self, out_path, timestamp)` |
| `_generate_json` | method | `modules/professional_report.py:513` | `def _generate_json(self, out_path, timestamp)` |
| `_generate_markdown` | method | `modules/professional_report.py:450` | `def _generate_markdown(self, out_path, timestamp)` |
| `_html_to_pdf` | method | `modules/professional_report.py:552` | `def _html_to_pdf(self, html_path)` |
| `_load_json` | method | `modules/professional_report.py:805` | `def _load_json(self, filename)` |
| `classify_findings` | method | `modules/professional_report.py:217` | `def classify_findings(self, data)` |
| `collect_command_history` | method | `modules/professional_report.py:841` | `def collect_command_history(self, max_entries)` |
| `collect_data` | method | `modules/professional_report.py:179` | `def collect_data(self)` |
| `collect_loot_summary` | method | `modules/professional_report.py:865` | `def collect_loot_summary(self)` |
| `generate` | method | `modules/professional_report.py:244` | `def generate(self, output_dir, output_format, client_name, engagement_type, with_ai, ai_backend)` |
| `generate_executive_summary` | method | `modules/professional_report.py:911` | `def generate_executive_summary(self, data, with_ai, ai_backend)` |
| `download_kernel_sources` | function | `modules/r.sh:10` | `` |
| `ReactionPick` | class | `modules/reaction_bridge.py:66` | `class ReactionPick` |
| `__init__` | method | `modules/reaction_bridge.py:69` | `def __init__(self, command, reason, priority, mitre)` |
| `_buffer_path` | function | `modules/reaction_bridge.py:76` | `def _buffer_path(task_id)` |
| `_load_buffer` | function | `modules/reaction_bridge.py:143` | `def _load_buffer(task_id)` |
| `_placeholder_value` | function | `modules/reaction_bridge.py:154` | `def _placeholder_value(value)` |
| `_write_buffer` | function | `modules/reaction_bridge.py:150` | `def _write_buffer(task_id, payload)` |
| `find_credentials` | function | `modules/reaction_bridge.py:159` | `def find_credentials(output)` |
| `load_reaction_triggers` | function | `modules/reaction_bridge.py:108` | `def load_reaction_triggers(task_id, consumer)` |
| `save_decisions` | function | `modules/reaction_bridge.py:80` | `def save_decisions(task_id, decisions)` |
| `AVBlockedMatcher` | class | `modules/reactive_engine.py:102` | `class AVBlockedMatcher(AbstractSignalMatcher)` |
| `AbstractSignalMatcher` | class | `modules/reactive_engine.py:97` | `class AbstractSignalMatcher(ABC)` |
| `CredentialFoundMatcher` | class | `modules/reactive_engine.py:147` | `class CredentialFoundMatcher(AbstractSignalMatcher)` |
| `DataOfInterestMatcher` | class | `modules/reactive_engine.py:323` | `class DataOfInterestMatcher(AbstractSignalMatcher)` |
| `EvasionAdvisor` | class | `modules/reactive_engine.py:481` | `class EvasionAdvisor` |
| `LateralOpportunityMatcher` | class | `modules/reactive_engine.py:293` | `class LateralOpportunityMatcher(AbstractSignalMatcher)` |
| `NewHostMatcher` | class | `modules/reactive_engine.py:209` | `class NewHostMatcher(AbstractSignalMatcher)` |
| `ParquetAdvisor` | class | `modules/reactive_engine.py:389` | `class ParquetAdvisor` |
| `PrivescAdvisor` | class | `modules/reactive_engine.py:537` | `class PrivescAdvisor` |
| `PrivescHintMatcher` | class | `modules/reactive_engine.py:174` | `class PrivescHintMatcher(AbstractSignalMatcher)` |
| `ReactiveDecision` | class | `modules/reactive_engine.py:80` | `class ReactiveDecision` |
| `ReactiveEngine` | class | `modules/reactive_engine.py:804` | `class ReactiveEngine` |
| `SemanticContextAdvisor` | class | `modules/reactive_engine.py:632` | `class SemanticContextAdvisor` |
| `ServiceVersionMatcher` | class | `modules/reactive_engine.py:232` | `class ServiceVersionMatcher(AbstractSignalMatcher)` |
| `ShellErrorMatcher` | class | `modules/reactive_engine.py:262` | `class ShellErrorMatcher(AbstractSignalMatcher)` |
| `Signal` | class | `modules/reactive_engine.py:69` | `class Signal` |
| `__init__` | method | `modules/reactive_engine.py:395` | `def __init__(self, root)` |
| `__init__` | method | `modules/reactive_engine.py:644` | `def __init__(self, rag, config_loader, min_score, query_limit)` |
| `__init__` | method | `modules/reactive_engine.py:810` | `def __init__(self, matchers, evasion, privesc, parquet, semantic)` |
| `_default_config_loader` | function | `modules/reactive_engine.py:42` | `def _default_config_loader()` |
| `_enabled` | method | `modules/reactive_engine.py:697` | `def _enabled(self)` |
| `_extract_verb` | method | `modules/reactive_engine.py:715` | `def _extract_verb(source)` |
| `_load` | method | `modules/reactive_engine.py:402` | `def _load(self)` |
| `_load_rag` | method | `modules/reactive_engine.py:671` | `def _load_rag(self)` |
| `analyse` | method | `modules/reactive_engine.py:835` | `def analyse(self, output, command, platform, context)` |
| `get_engine` | function | `modules/reactive_engine.py:977` | `def get_engine()` |
| `gtfobins_for` | method | `modules/reactive_engine.py:421` | `def gtfobins_for(self, binary)` |
| `lolbas_for` | method | `modules/reactive_engine.py:434` | `def lolbas_for(self, binary)` |
| `match` | method | `modules/reactive_engine.py:99` | `def match(self, output, context)` |
| `match` | method | `modules/reactive_engine.py:128` | `def match(self, output, context)` |
| `match` | method | `modules/reactive_engine.py:159` | `def match(self, output, context)` |
| `match` | method | `modules/reactive_engine.py:192` | `def match(self, output, context)` |
| `match` | method | `modules/reactive_engine.py:214` | `def match(self, output, context)` |
| `match` | method | `modules/reactive_engine.py:247` | `def match(self, output, context)` |
| `match` | method | `modules/reactive_engine.py:276` | `def match(self, output, context)` |
| `match` | method | `modules/reactive_engine.py:307` | `def match(self, output, context)` |
| `match` | method | `modules/reactive_engine.py:349` | `def match(self, output, context)` |
| `suggest` | method | `modules/reactive_engine.py:504` | `def suggest(self, signals, platform)` |
| `suggest` | method | `modules/reactive_engine.py:565` | `def suggest(self, signals, platform, parquet)` |
| `suggest` | method | `modules/reactive_engine.py:734` | `def suggest(self, output, command, platform, context)` |
| `technique_commands_for` | method | `modules/reactive_engine.py:448` | `def technique_commands_for(self, platform, keyword)` |
| `top_decision` | method | `modules/reactive_engine.py:958` | `def top_decision(self, output, command, platform, context)` |
| `_build_user_prompt` | function | `modules/recommender.py:55` | `def _build_user_prompt(state)` |
| `_call_ai` | function | `modules/recommender.py:97` | `def _call_ai(api_key, user_prompt)` |
| `recommend` | function | `modules/recommender.py:143` | `def recommend(state, api_key)` |
| `recommend_and_save` | function | `modules/recommender.py:163` | `def recommend_and_save(api_key)` |
| `GymAttempt` | class | `modules/redteam_gym.py:318` | `class GymAttempt` |
| `_award_gym_elo` | function | `modules/redteam_gym.py:876` | `def _award_gym_elo(username, elo_bonus)` |
| `_calc_speed_score` | function | `modules/redteam_gym.py:773` | `def _calc_speed_score(elapsed_seconds, max_bonus)` |
| `_calc_stealth_score` | function | `modules/redteam_gym.py:794` | `def _calc_stealth_score(techniques, max_bonus)` |
| `_calc_technique_score` | function | `modules/redteam_gym.py:810` | `def _calc_technique_score(techniques, chal, max_bonus)` |
| `_ensure_gym_dir` | function | `modules/redteam_gym.py:334` | `def _ensure_gym_dir()` |
| `_get_rank` | function | `modules/redteam_gym.py:902` | `def _get_rank(username)` |
| `_get_username` | function | `modules/redteam_gym.py:366` | `def _get_username()` |
| `_load_leaderboard` | function | `modules/redteam_gym.py:339` | `def _load_leaderboard()` |
| `_resolve_active_run` | function | `modules/redteam_gym.py:476` | `def _resolve_active_run(selector, operator)` |
| `_same_engagement` | function | `modules/redteam_gym.py:673` | `def _same_engagement(ip, target)` |
| `_save_leaderboard` | function | `modules/redteam_gym.py:355` | `def _save_leaderboard(board)` |
| `_update_leaderboard` | function | `modules/redteam_gym.py:832` | `def _update_leaderboard(attempt)` |
| `create_gym` | function | `modules/redteam_gym.py:398` | `def create_gym(gym_id)` |
| `definition_rows` | function | `modules/redteam_gym.py:393` | `def definition_rows()` |
| `delete_gym` | function | `modules/redteam_gym.py:445` | `def delete_gym(gym_id)` |
| `engagement_context` | function | `modules/redteam_gym.py:700` | `def engagement_context(target)` |
| `get_active_challenge` | function | `modules/redteam_gym.py:946` | `def get_active_challenge(run_id)` |
| `get_active_challenges` | function | `modules/redteam_gym.py:760` | `def get_active_challenges()` |
| `list_challenges` | function | `modules/redteam_gym.py:453` | `def list_challenges()` |
| `main` | function | `modules/redteam_gym.py:1031` | `def main()` |
| `record_external_attempt` | function | `modules/redteam_gym.py:977` | `def record_external_attempt(challenge_id, success, elo_bonus, techniques)` |
| `reload_challenge_definitions` | function | `modules/redteam_gym.py:299` | `def reload_challenge_definitions(directory)` |
| `save_gym_yaml` | function | `modules/redteam_gym.py:435` | `def save_gym_yaml(gym_id, text)` |
| `show_leaderboard` | function | `modules/redteam_gym.py:919` | `def show_leaderboard(top_n)` |
| `start_challenge` | function | `modules/redteam_gym.py:494` | `def start_challenge(challenge_id, target)` |
| `stop_challenges` | function | `modules/redteam_gym.py:668` | `def stop_challenges(selector)` |
| `submit_challenge` | function | `modules/redteam_gym.py:560` | `def submit_challenge(techniques_used, success, run_id)` |
| `DataDirectory` | class | `modules/reflective_dll.py:70` | `class DataDirectory` |
| `ImportDescriptor` | class | `modules/reflective_dll.py:104` | `class ImportDescriptor` |
| `PEHeader` | class | `modules/reflective_dll.py:37` | `class PEHeader` |
| `PEParser` | class | `modules/reflective_dll.py:142` | `class PEParser` |
| `ReflectiveLoader` | class | `modules/reflective_dll.py:464` | `class ReflectiveLoader` |
| `ReflectiveLoaderConfig` | class | `modules/reflective_dll.py:121` | `class ReflectiveLoaderConfig` |
| `SectionHeader` | class | `modules/reflective_dll.py:83` | `class SectionHeader` |
| `__init__` | method | `modules/reflective_dll.py:151` | `def __init__(self, pe_data)` |
| `__init__` | method | `modules/reflective_dll.py:492` | `def __init__(self, pe_data, config)` |
| `_parse_thunk_names` | method | `modules/reflective_dll.py:426` | `def _parse_thunk_names(self, thunk_rva, sections)` |
| `_read_asciiz_at_rva` | method | `modules/reflective_dll.py:417` | `def _read_asciiz_at_rva(self, rva, sections)` |
| `architecture` | method | `modules/reflective_dll.py:510` | `def architecture(self)` |
| `generate_c_stub` | method | `modules/reflective_dll.py:588` | `def generate_c_stub(self)` |
| `generate_powershell_stub` | method | `modules/reflective_dll.py:666` | `def generate_powershell_stub(self)` |
| `is_64bit` | method | `modules/reflective_dll.py:456` | `def is_64bit(self)` |
| `parse_data_directories` | method | `modules/reflective_dll.py:243` | `def parse_data_directories(self, num_entries)` |
| `parse_exports` | method | `modules/reflective_dll.py:374` | `def parse_exports(self, export_dir, sections)` |
| `parse_file_header` | method | `modules/reflective_dll.py:166` | `def parse_file_header(self)` |
| `parse_imports` | method | `modules/reflective_dll.py:280` | `def parse_imports(self, import_dir, sections)` |
| `parse_relocations` | method | `modules/reflective_dll.py:326` | `def parse_relocations(self, reloc_dir, sections)` |
| `parse_sections` | method | `modules/reflective_dll.py:208` | `def parse_sections(self, num_sections)` |
| `plan_injection` | method | `modules/reflective_dll.py:526` | `def plan_injection(self)` |
| `raw_data` | method | `modules/reflective_dll.py:460` | `def raw_data(self)` |
| `required_imports` | method | `modules/reflective_dll.py:515` | `def required_imports(self)` |
| `rva_to_offset` | method | `modules/reflective_dll.py:265` | `def rva_to_offset(self, rva, sections)` |
| `sha256` | method | `modules/reflective_dll.py:505` | `def sha256(self)` |
| `summarize` | method | `modules/reflective_dll.py:685` | `def summarize(self)` |
| `ResourceScriptEngine` | class | `modules/resource_script.py:268` | `class ResourceScriptEngine` |
| `ScriptContext` | class | `modules/resource_script.py:82` | `class ScriptContext` |
| `ScriptError` | class | `modules/resource_script.py:76` | `class ScriptError(RuntimeError)` |
| `__init__` | method | `modules/resource_script.py:89` | `def __init__(self, shell_params, on_command, on_print)` |
| `__init__` | method | `modules/resource_script.py:276` | `def __init__(self, context)` |
| `_call_macro` | method | `modules/resource_script.py:537` | `def _call_macro(self, name, args)` |
| `_compare` | method | `modules/resource_script.py:220` | `def _compare(left, op, right)` |
| `_execute_line` | method | `modules/resource_script.py:347` | `def _execute_line(self, raw)` |
| `_extract_macros` | method | `modules/resource_script.py:331` | `def _extract_macros(self, lines)` |
| `_jump_past` | method | `modules/resource_script.py:251` | `def _jump_past(self, open_res, close_re)` |
| `_lookup` | method | `modules/resource_script.py:168` | `def _lookup(self, name)` |
| `_repl` | function | `modules/resource_script.py:125` | `def _repl(m)` |
| `_resolve` | method | `modules/resource_script.py:124` | `def _resolve(self, text)` |
| `_resolve_operand` | method | `modules/resource_script.py:183` | `def _resolve_operand(self, operand)` |
| `_skip` | method | `modules/resource_script.py:165` | `def _skip(self)` |
| `eval_condition` | method | `modules/resource_script.py:191` | `def eval_condition(self, raw_condition)` |
| `execute` | method | `modules/resource_script.py:279` | `def execute(self, script_path)` |
| `execute_lines` | method | `modules/resource_script.py:293` | `def execute_lines(self, lines, source)` |
| `execute_string` | method | `modules/resource_script.py:327` | `def execute_string(self, script)` |
| `print` | method | `modules/resource_script.py:138` | `def print(self, msg)` |
| `run_command` | method | `modules/resource_script.py:147` | `def run_command(self, cmd)` |
| `reverse_shell_exit` | function | `modules/reverse-shell.c:16` | `static void __exit reverse_shell_exit(void)` |
| `reverse_shell_init` | function | `modules/reverse-shell.c:12` | `static int __init reverse_shell_init(void)` |
| `DllMain` | function | `modules/revshell.c:10` | `BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)` |
| `xlAutoOpen` | function | `modules/revshell.c:5` | `void __cdecl xlAutoOpen()` |
| `RichDashboard` | class | `modules/rich_tui.py:66` | `class RichDashboard` |
| `__init__` | method | `modules/rich_tui.py:74` | `def __init__(self, dashboard_engine, refresh_interval, live)` |
| `_keyboard_listener` | method | `modules/rich_tui.py:146` | `def _keyboard_listener(self)` |
| `_render` | method | `modules/rich_tui.py:137` | `def _render(self)` |
| `_render_beacons` | method | `modules/rich_tui.py:372` | `def _render_beacons(self, snapshot)` |
| `_render_header` | method | `modules/rich_tui.py:193` | `def _render_header(self, snapshot)` |
| `_render_layout` | method | `modules/rich_tui.py:168` | `def _render_layout(self, snapshot)` |
| `_render_pivots` | method | `modules/rich_tui.py:337` | `def _render_pivots(self, snapshot)` |
| `_render_pivots_beacons` | method | `modules/rich_tui.py:321` | `def _render_pivots_beacons(self, snapshot)` |
| `_render_recommendations` | method | `modules/rich_tui.py:261` | `def _render_recommendations(self, snapshot)` |
| `_render_shortcuts` | method | `modules/rich_tui.py:413` | `def _render_shortcuts(self)` |
| `_render_topology` | method | `modules/rich_tui.py:221` | `def _render_topology(self, snapshot)` |
| `run` | method | `modules/rich_tui.py:96` | `def run(self)` |
| `stop` | method | `modules/rich_tui.py:132` | `def stop(self)` |
| `BucketedStateEncoder` | class | `modules/rl_trainer.py:114` | `class BucketedStateEncoder(IStateEncoder)` |
| `EpsilonTracker` | class | `modules/rl_trainer.py:215` | `class EpsilonTracker` |
| `IStateEncoder` | class | `modules/rl_trainer.py:101` | `class IStateEncoder(ABC)` |
| `QValueStore` | class | `modules/rl_trainer.py:150` | `class QValueStore` |
| `RLConfig` | class | `modules/rl_trainer.py:84` | `class RLConfig` |
| `RLTrainer` | class | `modules/rl_trainer.py:267` | `class RLTrainer` |
| `__init__` | method | `modules/rl_trainer.py:156` | `def __init__(self, path, optimistic_init)` |
| `__init__` | method | `modules/rl_trainer.py:218` | `def __init__(self, start, minimum, decay, path)` |
| `__init__` | method | `modules/rl_trainer.py:284` | `def __init__(self, config, state_encoder, q_store, epsilon_tracker)` |
| `_load` | method | `modules/rl_trainer.py:200` | `def _load(self)` |
| `_load` | method | `modules/rl_trainer.py:250` | `def _load(self)` |
| `_penalize` | method | `modules/rl_trainer.py:407` | `def _penalize(self, reward, detection_prob)` |
| `_persist` | method | `modules/rl_trainer.py:192` | `def _persist(self)` |
| `_save` | method | `modules/rl_trainer.py:241` | `def _save(self)` |
| `argmax` | method | `modules/rl_trainer.py:182` | `def argmax(self, state, candidates)` |
| `best_expert_for_state` | method | `modules/rl_trainer.py:389` | `def best_expert_for_state(self, state, candidates)` |
| `encode` | method | `modules/rl_trainer.py:105` | `def encode(self, task_type, engagement_phase, recent_reward_ema)` |
| `encode` | method | `modules/rl_trainer.py:131` | `def encode(self, task_type, engagement_phase, recent_reward_ema)` |
| `encode_state` | method | `modules/rl_trainer.py:304` | `def encode_state(self, task_type, engagement_phase, recent_reward_ema)` |
| `epsilon` | method | `modules/rl_trainer.py:233` | `def epsilon(self)` |
| `epsilon` | method | `modules/rl_trainer.py:402` | `def epsilon(self)` |
| `get` | method | `modules/rl_trainer.py:168` | `def get(self, state, action)` |
| `get_trainer` | function | `modules/rl_trainer.py:425` | `def get_trainer(config)` |
| `max_q` | method | `modules/rl_trainer.py:176` | `def max_q(self, state, candidates)` |
| `q_values_for_state` | method | `modules/rl_trainer.py:393` | `def q_values_for_state(self, state, candidates)` |
| `save` | method | `modules/rl_trainer.py:188` | `def save(self)` |
| `save` | method | `modules/rl_trainer.py:397` | `def save(self)` |
| `select_action` | method | `modules/rl_trainer.py:313` | `def select_action(self, state, candidates, force_exploit)` |
| `set` | method | `modules/rl_trainer.py:172` | `def set(self, state, action, value)` |
| `step` | method | `modules/rl_trainer.py:236` | `def step(self)` |
| `update` | method | `modules/rl_trainer.py:347` | `def update(self, state, action, reward, next_state, candidates, detection_prob)` |
| `BUFFER_SIZE` | macro | `modules/rootkit/mr.c:32` | `#define BUFFER_SIZE` |
| `Command` | struct | `modules/rootkit/mr.c:43` | `` |
| `DESIRED_LD_PRELOAD` | macro | `modules/rootkit/mr.c:34` | `#define DESIRED_LD_PRELOAD` |
| `HIDE_FILE` | macro | `modules/rootkit/mr.c:36` | `#define HIDE_FILE` |
| `KEY_FILE` | macro | `modules/rootkit/mr.c:37` | `#define KEY_FILE` |
| `MAX_COMMANDS` | macro | `modules/rootkit/mr.c:33` | `#define MAX_COMMANDS` |
| `PASSWORD` | macro | `modules/rootkit/mr.c:39` | `#define PASSWORD` |
| `PATH_MAX` | macro | `modules/rootkit/mr.c:41` | `#define PATH_MAX` |
| `PID_FILE` | macro | `modules/rootkit/mr.c:35` | `#define PID_FILE` |
| `PORT` | macro | `modules/rootkit/mr.c:31` | `#define PORT` |
| `VirtualFile` | struct | `modules/rootkit/mr.c:49` | `` |
| `check_elevate` | function | `modules/rootkit/mr.c:136` | `int check_elevate()` |
| `copy_binary` | function | `modules/rootkit/mr.c:215` | `void copy_binary(const char *source, const char *destination)` |
| `crontab` | function | `modules/rootkit/mr.c:156` | `void crontab(const char *path)` |
| `ensure_hide_file_exists` | function | `modules/rootkit/mr.c:271` | `void ensure_hide_file_exists()` |
| `ensure_key_file_exists` | function | `modules/rootkit/mr.c:253` | `void ensure_key_file_exists()` |
| `ensure_ld_preload` | function | `modules/rootkit/mr.c:100` | `void ensure_ld_preload()` |
| `ensure_pid_file_exists` | function | `modules/rootkit/mr.c:117` | `void ensure_pid_file_exists()` |
| `generate_random_string` | function | `modules/rootkit/mr.c:168` | `char *generate_random_string()` |
| `get_ld_preload` | function | `modules/rootkit/mr.c:84` | `char *get_ld_preload()` |
| `handle_client` | function | `modules/rootkit/mr.c:321` | `void *handle_client(void *client_socket)` |
| `infect_command` | function | `modules/rootkit/mr.c:289` | `void infect_command()` |
| `kde_plasma` | function | `modules/rootkit/mr.c:200` | `void kde_plasma(const char *path)` |
| `load_rootkit` | function | `modules/rootkit/mr.c:303` | `void load_rootkit()` |
| `main` | function | `modules/rootkit/mr.c:639` | `int main()` |
| `mon_shell` | function | `modules/rootkit/mr.c:521` | `void *mon_shell(void *data)` |
| `persist` | function | `modules/rootkit/mr.c:234` | `void persist(const char *path)` |
| `reboot_system` | function | `modules/rootkit/mr.c:615` | `void reboot_system()` |
| `set_ld_preload` | function | `modules/rootkit/mr.c:87` | `void set_ld_preload(const char *ld_preload)` |
| `signal_handler` | function | `modules/rootkit/mr.c:609` | `void signal_handler(int signum)` |
| `unload_rootkit` | function | `modules/rootkit/mr.c:314` | `void unload_rootkit()` |
| `write_file` | function | `modules/rootkit/mr.c:145` | `void write_file(const char *path, const char *content, mode_t mode)` |
| `xdg` | function | `modules/rootkit/mr.c:178` | `void xdg(const char *path, int admin)` |
| `FILE_HIDE_PATH` | macro | `modules/rootkit/mrhyde.c:50` | `#define FILE_HIDE_PATH` |
| `HIDDEN_DIR` | macro | `modules/rootkit/mrhyde.c:33` | `#define HIDDEN_DIR` |
| `HIDDEN_FILE` | macro | `modules/rootkit/mrhyde.c:34` | `#define HIDDEN_FILE` |
| `HIDDEN_FILE1` | macro | `modules/rootkit/mrhyde.c:35` | `#define HIDDEN_FILE1` |
| `HIDDEN_FILE2` | macro | `modules/rootkit/mrhyde.c:36` | `#define HIDDEN_FILE2` |
| `HIDDEN_FILE3` | macro | `modules/rootkit/mrhyde.c:37` | `#define HIDDEN_FILE3` |
| `HIDDEN_FILE4` | macro | `modules/rootkit/mrhyde.c:38` | `#define HIDDEN_FILE4` |
| `HIDDEN_FILE5` | macro | `modules/rootkit/mrhyde.c:39` | `#define HIDDEN_FILE5` |
| `HIDDEN_FILE6` | macro | `modules/rootkit/mrhyde.c:40` | `#define HIDDEN_FILE6` |
| `HIDDEN_FILE7` | macro | `modules/rootkit/mrhyde.c:41` | `#define HIDDEN_FILE7` |
| `HIDDEN_FILE8` | macro | `modules/rootkit/mrhyde.c:42` | `#define HIDDEN_FILE8` |
| `HIDDEN_FILE9` | macro | `modules/rootkit/mrhyde.c:43` | `#define HIDDEN_FILE9` |
| `HIDE_DIR` | macro | `modules/rootkit/mrhyde.c:46` | `#define HIDE_DIR` |
| `HIDE_USER` | macro | `modules/rootkit/mrhyde.c:47` | `#define HIDE_USER` |
| `MAX_HIDE_PIDS` | macro | `modules/rootkit/mrhyde.c:48` | `#define MAX_HIDE_PIDS` |
| `PATHMRHYDE` | macro | `modules/rootkit/mrhyde.c:44` | `#define PATHMRHYDE` |
| `PID_FILE_PATH` | macro | `modules/rootkit/mrhyde.c:49` | `#define PID_FILE_PATH` |
| `fopen` | function | `modules/rootkit/mrhyde.c:283` | `FILE *fopen(const char *pathname, const char *mode)` |
| `fstat` | function | `modules/rootkit/mrhyde.c:503` | `int fstat(int fd, struct stat *statbuf)` |
| `get_username_from_pid` | function | `modules/rootkit/mrhyde.c:178` | `char* get_username_from_pid(pid_t pid)` |
| `getdents` | function | `modules/rootkit/mrhyde.c:557` | `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `getdents64` | function | `modules/rootkit/mrhyde.c:618` | `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `kill` | function | `modules/rootkit/mrhyde.c:125` | `int kill(pid_t pid, int sig)` |
| `linux_dirent64` | struct | `modules/rootkit/mrhyde.c:548` | `` |
| `load_hidden_files` | function | `modules/rootkit/mrhyde.c:93` | `void load_hidden_files()` |
| `load_hidden_pids` | function | `modules/rootkit/mrhyde.c:73` | `void load_hidden_pids()` |
| `lstat` | function | `modules/rootkit/mrhyde.c:459` | `int lstat(const char *pathname, struct stat *statbuf)` |
| `main` | function | `modules/rootkit/mrhyde.c:678` | `int main()` |
| `my_open` | function | `modules/rootkit/mrhyde.c:327` | `int my_open(const char *pathname, int flags, mode_t mode)` |
| `my_openat` | function | `modules/rootkit/mrhyde.c:371` | `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)` |
| `original_dirent` | type_alias | `modules/rootkit/mrhyde.c:51` | `typedef struct dirent original_dirent;` |
| `readdir` | function | `modules/rootkit/mrhyde.c:222` | `struct dirent* readdir(DIR* dirp)` |
| `remove` | function | `modules/rootkit/mrhyde.c:145` | `int remove(const char *pathname)` |
| `should_hide_file` | function | `modules/rootkit/mrhyde.c:212` | `int should_hide_file(const char* filename)` |
| `should_hide_pid` | function | `modules/rootkit/mrhyde.c:197` | `int should_hide_pid(const char* pid)` |
| `stat` | function | `modules/rootkit/mrhyde.c:415` | `int stat(const char *pathname, struct stat *statbuf)` |
| `unlink` | function | `modules/rootkit/mrhyde.c:113` | `int unlink(const char *pathname)` |
| `unlinkat` | function | `modules/rootkit/mrhyde.c:157` | `int unlinkat(int dirfd, const char *pathname, int flags)` |
| `HIDDEN_DIR` | macro | `modules/rootkit/mrhyde2.c:31` | `#define HIDDEN_DIR` |
| `HIDDEN_FILE` | macro | `modules/rootkit/mrhyde2.c:32` | `#define HIDDEN_FILE` |
| `HIDDEN_FILE1` | macro | `modules/rootkit/mrhyde2.c:33` | `#define HIDDEN_FILE1` |
| `HIDDEN_FILE2` | macro | `modules/rootkit/mrhyde2.c:34` | `#define HIDDEN_FILE2` |
| `HIDDEN_FILE3` | macro | `modules/rootkit/mrhyde2.c:35` | `#define HIDDEN_FILE3` |
| `HIDDEN_FILE4` | macro | `modules/rootkit/mrhyde2.c:36` | `#define HIDDEN_FILE4` |
| `HIDDEN_FILE5` | macro | `modules/rootkit/mrhyde2.c:37` | `#define HIDDEN_FILE5` |
| `HIDDEN_FILE6` | macro | `modules/rootkit/mrhyde2.c:38` | `#define HIDDEN_FILE6` |
| `HIDDEN_FILE7` | macro | `modules/rootkit/mrhyde2.c:39` | `#define HIDDEN_FILE7` |
| `HIDDEN_FILE8` | macro | `modules/rootkit/mrhyde2.c:40` | `#define HIDDEN_FILE8` |
| `HIDDEN_FILE9` | macro | `modules/rootkit/mrhyde2.c:41` | `#define HIDDEN_FILE9` |
| `HIDE_DIR` | macro | `modules/rootkit/mrhyde2.c:44` | `#define HIDE_DIR` |
| `HIDE_USER` | macro | `modules/rootkit/mrhyde2.c:45` | `#define HIDE_USER` |
| `MAX_HIDE_PIDS` | macro | `modules/rootkit/mrhyde2.c:46` | `#define MAX_HIDE_PIDS` |
| `PATHMRHYDE` | macro | `modules/rootkit/mrhyde2.c:42` | `#define PATHMRHYDE` |
| `PID_FILE_PATH` | macro | `modules/rootkit/mrhyde2.c:47` | `#define PID_FILE_PATH` |
| `fopen` | function | `modules/rootkit/mrhyde2.c:238` | `FILE *fopen(const char *pathname, const char *mode)` |
| `fstat` | function | `modules/rootkit/mrhyde2.c:423` | `int fstat(int fd, struct stat *statbuf)` |
| `get_username_from_pid` | function | `modules/rootkit/mrhyde2.c:148` | `char* get_username_from_pid(pid_t pid)` |
| `getdents` | function | `modules/rootkit/mrhyde2.c:470` | `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `getdents64` | function | `modules/rootkit/mrhyde2.c:527` | `int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `kill` | function | `modules/rootkit/mrhyde2.c:95` | `int kill(pid_t pid, int sig)` |
| `linux_dirent64` | struct | `modules/rootkit/mrhyde2.c:461` | `` |
| `load_hidden_pids` | function | `modules/rootkit/mrhyde2.c:63` | `void load_hidden_pids()` |
| `lstat` | function | `modules/rootkit/mrhyde2.c:386` | `int lstat(const char *pathname, struct stat *statbuf)` |
| `main` | function | `modules/rootkit/mrhyde2.c:583` | `int main()` |
| `my_open` | function | `modules/rootkit/mrhyde2.c:275` | `int my_open(const char *pathname, int flags, mode_t mode)` |
| `my_openat` | function | `modules/rootkit/mrhyde2.c:312` | `int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)` |
| `original_dirent` | type_alias | `modules/rootkit/mrhyde2.c:48` | `typedef struct dirent original_dirent;` |
| `readdir` | function | `modules/rootkit/mrhyde2.c:182` | `struct dirent* readdir(DIR* dirp)` |
| `remove` | function | `modules/rootkit/mrhyde2.c:115` | `int remove(const char *pathname)` |
| `should_hide_pid` | function | `modules/rootkit/mrhyde2.c:167` | `int should_hide_pid(const char* pid)` |
| `stat` | function | `modules/rootkit/mrhyde2.c:349` | `int stat(const char *pathname, struct stat *statbuf)` |
| `unlink` | function | `modules/rootkit/mrhyde2.c:83` | `int unlink(const char *pathname)` |
| `unlinkat` | function | `modules/rootkit/mrhyde2.c:127` | `int unlinkat(int dirfd, const char *pathname, int flags)` |
| `C2_PORT` | macro | `modules/rootkit/mrhyde3.c:53` | `#define C2_PORT` |
| `C2_SERVER_IP` | macro | `modules/rootkit/mrhyde3.c:52` | `#define C2_SERVER_IP` |
| `CQE_TIMEOUT_MS` | macro | `modules/rootkit/mrhyde3.c:54` | `#define CQE_TIMEOUT_MS` |
| `FILE_HIDE_PATH` | macro | `modules/rootkit/mrhyde3.c:49` | `#define FILE_HIDE_PATH` |
| `HIDDEN_DIR` | macro | `modules/rootkit/mrhyde3.c:33` | `#define HIDDEN_DIR` |
| `HIDDEN_FILE` | macro | `modules/rootkit/mrhyde3.c:34` | `#define HIDDEN_FILE` |
| `HIDDEN_FILE1` | macro | `modules/rootkit/mrhyde3.c:35` | `#define HIDDEN_FILE1` |
| `HIDDEN_FILE2` | macro | `modules/rootkit/mrhyde3.c:36` | `#define HIDDEN_FILE2` |
| `HIDDEN_FILE3` | macro | `modules/rootkit/mrhyde3.c:37` | `#define HIDDEN_FILE3` |
| `HIDDEN_FILE4` | macro | `modules/rootkit/mrhyde3.c:38` | `#define HIDDEN_FILE4` |
| `HIDDEN_FILE5` | macro | `modules/rootkit/mrhyde3.c:39` | `#define HIDDEN_FILE5` |
| `HIDDEN_FILE6` | macro | `modules/rootkit/mrhyde3.c:40` | `#define HIDDEN_FILE6` |
| `HIDDEN_FILE7` | macro | `modules/rootkit/mrhyde3.c:41` | `#define HIDDEN_FILE7` |
| `HIDDEN_FILE8` | macro | `modules/rootkit/mrhyde3.c:42` | `#define HIDDEN_FILE8` |
| `HIDDEN_FILE9` | macro | `modules/rootkit/mrhyde3.c:43` | `#define HIDDEN_FILE9` |
| `HIDE_DIR` | macro | `modules/rootkit/mrhyde3.c:45` | `#define HIDE_DIR` |
| `HIDE_USER` | macro | `modules/rootkit/mrhyde3.c:46` | `#define HIDE_USER` |
| `IO_URING_BUFFER_SIZE` | macro | `modules/rootkit/mrhyde3.c:51` | `#define IO_URING_BUFFER_SIZE` |
| `IO_URING_QUEUE_DEPTH` | macro | `modules/rootkit/mrhyde3.c:50` | `#define IO_URING_QUEUE_DEPTH` |
| `MAX_HIDE_PIDS` | macro | `modules/rootkit/mrhyde3.c:47` | `#define MAX_HIDE_PIDS` |
| `PATHMRHYDE` | macro | `modules/rootkit/mrhyde3.c:44` | `#define PATHMRHYDE` |
| `PID_FILE_PATH` | macro | `modules/rootkit/mrhyde3.c:48` | `#define PID_FILE_PATH` |
| `_GNU_SOURCE` | macro | `modules/rootkit/mrhyde3.c:7` | `#define _GNU_SOURCE` |
| `__io_uring_enter` | function | `modules/rootkit/mrhyde3.c:76` | `static inline int __io_uring_enter(int fd, unsigned int to_submit, unsigned int min_complete,    ...` |
| `__io_uring_register` | function | `modules/rootkit/mrhyde3.c:80` | `static inline int __io_uring_register(int fd, unsigned int opcode, const void *arg, unsigned int ...` |
| `__io_uring_setup` | function | `modules/rootkit/mrhyde3.c:73` | `static inline int __io_uring_setup(unsigned int entries, struct io_uring_params *p)` |
| `fopen` | function | `modules/rootkit/mrhyde3.c:407` | `FILE *fopen(const char *pathname, const char *mode)` |
| `fstat` | function | `modules/rootkit/mrhyde3.c:535` | `int fstat(int fd, struct stat *statbuf)` |
| `get_username_from_pid` | function | `modules/rootkit/mrhyde3.c:297` | `char* get_username_from_pid(pid_t pid)` |
| `getdents` | function | `modules/rootkit/mrhyde3.c:569` | `int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)` |
| `getdents64` | function | `modules/rootkit/mrhyde3.c:605` | `ssize_t getdents64(int fd, void *dirp, size_t count)` |
| `init_root_ring` | function | `modules/rootkit/mrhyde3.c:176` | `static int init_root_ring(void)` |
| `io_uring` | struct | `modules/rootkit/mrhyde3.c:65` | `` |
| `io_uring_cq` | struct | `modules/rootkit/mrhyde3.c:61` | `` |
| `io_uring_sq` | struct | `modules/rootkit/mrhyde3.c:57` | `` |
| `kill` | function | `modules/rootkit/mrhyde3.c:373` | `int kill(pid_t pid, int sig)` |
| `linux_dirent64` | struct | `modules/rootkit/mrhyde3.c:560` | `` |
| `load_hidden_files` | function | `modules/rootkit/mrhyde3.c:282` | `void load_hidden_files(void)` |
| `load_hidden_pids` | function | `modules/rootkit/mrhyde3.c:268` | `void load_hidden_pids(void)` |
| `lstat` | function | `modules/rootkit/mrhyde3.c:511` | `int lstat(const char *pathname, struct stat *statbuf)` |
| `open` | function | `modules/rootkit/mrhyde3.c:430` | `int open(const char *pathname, int flags, ...)` |
| `openat` | function | `modules/rootkit/mrhyde3.c:458` | `int openat(int dirfd, const char *pathname, int flags, ...)` |
| `original_dirent` | type_alias | `modules/rootkit/mrhyde3.c:312` | `typedef struct dirent original_dirent;` |
| `readdir` | function | `modules/rootkit/mrhyde3.c:336` | `struct dirent* readdir(DIR* dirp)` |
| `remove` | function | `modules/rootkit/mrhyde3.c:383` | `int remove(const char *pathname)` |
| `should_hide_file` | function | `modules/rootkit/mrhyde3.c:329` | `int should_hide_file(const char* filename)` |
| `should_hide_pid` | function | `modules/rootkit/mrhyde3.c:320` | `int should_hide_pid(const char* pid)` |
| `stat` | function | `modules/rootkit/mrhyde3.c:487` | `int stat(const char *pathname, struct stat *statbuf)` |
| `traditional_read_file` | function | `modules/rootkit/mrhyde3.c:253` | `static char *traditional_read_file(const char *path)` |
| `unlink` | function | `modules/rootkit/mrhyde3.c:367` | `int unlink(const char *pathname)` |
| `unlinkat` | function | `modules/rootkit/mrhyde3.c:389` | `int unlinkat(int dirfd, const char *pathname, int flags)` |
| `uring_cqe_seen` | function | `modules/rootkit/mrhyde3.c:163` | `static void uring_cqe_seen(struct io_uring *ring, struct io_uring_cqe *cqe)` |
| `uring_get_sqe` | function | `modules/rootkit/mrhyde3.c:130` | `static struct io_uring_sqe *uring_get_sqe(struct io_uring *ring)` |
| `uring_queue_init` | function | `modules/rootkit/mrhyde3.c:85` | `static int uring_queue_init(unsigned int entries, struct io_uring *ring)` |
| `uring_read_whole_file` | function | `modules/rootkit/mrhyde3.c:197` | `static char *uring_read_whole_file(const char *path)` |
| `uring_submit` | function | `modules/rootkit/mrhyde3.c:141` | `static int uring_submit(struct io_uring *ring)` |
| `uring_wait_cqe_timeout` | function | `modules/rootkit/mrhyde3.c:149` | `static int uring_wait_cqe_timeout(struct io_uring *ring, struct io_uring_cqe **cqe_ptr, int timeo...` |
| `_start` | function | `modules/rootkit/rootkit.asm:4` | `` |
| `HIDDEN_FILE_NAME` | macro | `modules/rootkit/rootkit.c:27` | `#define HIDDEN_FILE_NAME` |
| `HIDDEN_PROCESS_NAME` | macro | `modules/rootkit/rootkit.c:26` | `#define HIDDEN_PROCESS_NAME` |
| `LISTENER_IP` | macro | `modules/rootkit/rootkit.c:28` | `#define LISTENER_IP` |
| `LISTENER_PORT` | macro | `modules/rootkit/rootkit.c:29` | `#define LISTENER_PORT` |
| `SPECIAL_STRING` | macro | `modules/rootkit/rootkit.c:31` | `#define SPECIAL_STRING` |
| `SPECIAL_STRING_PORT` | macro | `modules/rootkit/rootkit.c:34` | `#define SPECIAL_STRING_PORT` |
| `disable_module_signature_verification` | function | `modules/rootkit/rootkit.c:181` | `static void disable_module_signature_verification(void)` |
| `hook_syscalls` | function | `modules/rootkit/rootkit.c:195` | `static int __init hook_syscalls(void)` |
| `hooked_getdents` | function | `modules/rootkit/rootkit.c:75` | `static int hooked_getdents(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `hooked_getdents64` | function | `modules/rootkit/rootkit.c:101` | `static int hooked_getdents64(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `hooked_read` | function | `modules/rootkit/rootkit.c:127` | `static int hooked_read(struct kretprobe_instance *ri, struct pt_regs *regs)` |
| `regs_override_return` | function | `modules/rootkit/rootkit.c:43` | `static inline void regs_override_return(struct pt_regs *regs, long new_ret)` |
| `unhook_syscalls` | function | `modules/rootkit/rootkit.c:208` | `static void __exit unhook_syscalls(void)` |
| `SaaSAttackEngine` | class | `modules/saas_attacks.py:152` | `class SaaSAttackEngine` |
| `SaaSConfig` | class | `modules/saas_attacks.py:49` | `class SaaSConfig` |
| `SaaSEnumerationTools` | class | `modules/saas_attacks.py:71` | `class SaaSEnumerationTools` |
| `__init__` | method | `modules/saas_attacks.py:163` | `def __init__(self, config)` |
| `detect_external_sharing` | method | `modules/saas_attacks.py:327` | `def detect_external_sharing(self)` |
| `enumerate_all` | method | `modules/saas_attacks.py:166` | `def enumerate_all(self)` |
| `google_workspace_commands` | method | `modules/saas_attacks.py:100` | `def google_workspace_commands()` |
| `google_workspace_domain_wide_delegation` | method | `modules/saas_attacks.py:228` | `def google_workspace_domain_wide_delegation(self)` |
| `m365_ews_mail_search` | method | `modules/saas_attacks.py:179` | `def m365_ews_mail_search(self, search_term)` |
| `microsoft365_commands` | method | `modules/saas_attacks.py:75` | `def microsoft365_commands()` |
| `salesforce_commands` | method | `modules/saas_attacks.py:118` | `def salesforce_commands()` |
| `salesforce_report_mining` | method | `modules/saas_attacks.py:257` | `def salesforce_report_mining(self)` |
| `servicenow_commands` | method | `modules/saas_attacks.py:135` | `def servicenow_commands()` |
| `slack_data_mining` | method | `modules/saas_attacks.py:286` | `def slack_data_mining(self)` |
| `summary` | method | `modules/saas_attacks.py:352` | `def summary(self)` |
| `BindAddressResolver` | class | `modules/security_sanitizers.py:256` | `class BindAddressResolver` |
| `CommandRedactor` | class | `modules/security_sanitizers.py:318` | `class CommandRedactor` |
| `HeaderValueSanitizer` | class | `modules/security_sanitizers.py:101` | `class HeaderValueSanitizer` |
| `OutputSanitizer` | class | `modules/security_sanitizers.py:406` | `class OutputSanitizer` |
| `SecurityConfig` | class | `modules/security_sanitizers.py:37` | `class SecurityConfig` |
| `SessionPathResolver` | class | `modules/security_sanitizers.py:162` | `class SessionPathResolver` |
| `__init__` | method | `modules/security_sanitizers.py:115` | `def __init__(self, config)` |
| `__init__` | method | `modules/security_sanitizers.py:174` | `def __init__(self, base_dir, config)` |
| `__init__` | method | `modules/security_sanitizers.py:269` | `def __init__(self, config, preferred_addresses)` |
| `__init__` | method | `modules/security_sanitizers.py:333` | `def __init__(self, config)` |
| `__init__` | method | `modules/security_sanitizers.py:418` | `def __init__(self, config)` |
| `_display_password` | method | `modules/security_sanitizers.py:353` | `def _display_password(self, password)` |
| `_display_username` | method | `modules/security_sanitizers.py:345` | `def _display_username(self, username)` |
| `_is_well_formed` | method | `modules/security_sanitizers.py:285` | `def _is_well_formed(self, candidate)` |
| `_sanitize` | method | `modules/security_sanitizers.py:433` | `def _sanitize(self, value, depth)` |
| `base_dir` | method | `modules/security_sanitizers.py:192` | `def base_dir(self)` |
| `build_default_config` | function | `modules/security_sanitizers.py:477` | `def build_default_config(payload)` |

Next: [SYMBOLS_p20.md](SYMBOLS_p20.md)
