# Symbols (page 20 of 35)
Previous: [SYMBOLS_p19.md](SYMBOLS_p19.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_run_with_fallback` | function | `skills/lazyown_mcp.py:5779` | `def _run_with_fallback(cmd, to)` |
| `_runner` | function | `skills/lazyown_mcp.py:6108` | `def _runner(cmd)` |
| `_save_crons` | function | `skills/lazyown_mcp.py:10567` | `def _save_crons(entries)` |
| `_save_payload` | function | `skills/lazyown_mcp.py:565` | `def _save_payload(data)` |
| `_wait_for_nmap_xml` | function | `skills/lazyown_mcp.py:8158` | `def _wait_for_nmap_xml(tgt, timeout_s)` |
| `call_tool` | function | `skills/lazyown_mcp.py:5682` | `def call_tool(name, arguments)` |
| `coerce_value` | function | `skills/lazyown_mcp.py:870` | `def coerce_value(k, v)` |
| `list_tools` | function | `skills/lazyown_mcp.py:1745` | `def list_tools()` |
| `main` | function | `skills/lazyown_mcp.py:11560` | `def main()` |
| `register_handler` | function | `skills/lazyown_mcp.py:620` | `def register_handler(tool_name)` |
| `substitute_playbook_target` | function | `skills/lazyown_mcp.py:5664` | `def substitute_playbook_target(command, target)` |
| `text` | function | `skills/lazyown_mcp.py:5696` | `def text(content)` |
| `JobRecord` | class | `skills/lazyown_mcp_helpers.py:672` | `class JobRecord` |
| `JobStore` | class | `skills/lazyown_mcp_helpers.py:686` | `class JobStore` |
| `TaskAudit` | class | `skills/lazyown_mcp_helpers.py:153` | `class TaskAudit` |
| `__init__` | method | `skills/lazyown_mcp_helpers.py:689` | `def __init__(self, max_jobs)` |
| `_format_age` | function | `skills/lazyown_mcp_helpers.py:112` | `def _format_age(seconds)` |
| `_worker` | method | `skills/lazyown_mcp_helpers.py:709` | `def _worker()` |
| `audit_tasks` | method | `skills/lazyown_mcp_helpers.py:165` | `def audit_tasks(tasks, min_confidence)` |
| `build_target_context` | method | `skills/lazyown_mcp_helpers.py:414` | `def build_target_context(host, port, sessions_dir, payload, world_model)` |
| `collect_pwntomate_evidence` | method | `skills/lazyown_mcp_helpers.py:376` | `def collect_pwntomate_evidence(rhost, sessions_dir)` |
| `diff_snapshot` | method | `skills/lazyown_mcp_helpers.py:792` | `def diff_snapshot(sessions_dir, payload, world_model, tasks)` |
| `evidence_freshness` | function | `skills/lazyown_mcp_helpers.py:67` | `def evidence_freshness(path, threshold_seconds, now)` |
| `evidence_grep` | method | `skills/lazyown_mcp_helpers.py:297` | `def evidence_grep(pattern, sessions_dir, scope, max_matches, max_file_bytes, case_insensitive)` |
| `find_credential_provenance` | method | `skills/lazyown_mcp_helpers.py:196` | `def find_credential_provenance(value, sessions_dir, csv_name)` |
| `is_likely_credential` | function | `skills/lazyown_mcp_helpers.py:37` | `def is_likely_credential(value)` |
| `list` | method | `skills/lazyown_mcp_helpers.py:732` | `def list(self, limit)` |
| `needs_confirmation` | method | `skills/lazyown_mcp_helpers.py:875` | `def needs_confirmation(tool_name, arguments)` |
| `parse_task_value` | function | `skills/lazyown_mcp_helpers.py:125` | `def parse_task_value(title)` |
| `preflight_command` | method | `skills/lazyown_mcp_helpers.py:575` | `def preflight_command(command, payload, sessions_dir)` |
| `status` | method | `skills/lazyown_mcp_helpers.py:727` | `def status(self, job_id)` |
| `submit` | method | `skills/lazyown_mcp_helpers.py:694` | `def submit(self, command, runner, timeout)` |
| `take_snapshot` | method | `skills/lazyown_mcp_helpers.py:747` | `def take_snapshot(sessions_dir, payload, world_model, tasks)` |
| `call_tool` | function | `skills/lazyown_mcp_opencode.py:76` | `def call_tool(name, arguments)` |
| `list_tools` | function | `skills/lazyown_mcp_opencode.py:57` | `def list_tools()` |
| `main` | function | `skills/lazyown_mcp_opencode.py:84` | `def main()` |
| `Objective` | class | `skills/lazyown_objective.py:105` | `class Objective` |
| `ObjectiveStore` | class | `skills/lazyown_objective.py:123` | `class ObjectiveStore` |
| `SoulUpdater` | class | `skills/lazyown_objective.py:330` | `class SoulUpdater` |
| `__init__` | method | `skills/lazyown_objective.py:131` | `def __init__(self, path)` |
| `__init__` | method | `skills/lazyown_objective.py:350` | `def __init__(self)` |
| `_load_all` | method | `skills/lazyown_objective.py:138` | `def _load_all(self)` |
| `_now` | method | `skills/lazyown_objective.py:135` | `def _now(self)` |
| `_patch_line` | method | `skills/lazyown_objective.py:375` | `def _patch_line(self, key, value)` |
| `_patch_section` | method | `skills/lazyown_objective.py:360` | `def _patch_section(self, header, new_body)` |
| `_read` | method | `skills/lazyown_objective.py:355` | `def _read(self)` |
| `_save_all` | method | `skills/lazyown_objective.py:153` | `def _save_all(self, objs)` |
| `_text_hash` | method | `skills/lazyown_objective.py:159` | `def _text_hash(text)` |
| `_update_status` | method | `skills/lazyown_objective.py:229` | `def _update_status(self, obj_id, status, notes)` |
| `block` | method | `skills/lazyown_objective.py:246` | `def block(self, obj_id, reason)` |
| `cleanup` | method | `skills/lazyown_objective.py:163` | `def cleanup(self)` |
| `complete` | method | `skills/lazyown_objective.py:243` | `def complete(self, obj_id, notes)` |
| `current_plan` | method | `skills/lazyown_objective.py:301` | `def current_plan()` |
| `full_context_for_claude` | method | `skills/lazyown_objective.py:307` | `def full_context_for_claude(target)` |
| `inject` | method | `skills/lazyown_objective.py:193` | `def inject(self, text, priority, source, context, notes)` |
| `list_all` | method | `skills/lazyown_objective.py:265` | `def list_all(self, status, limit)` |
| `list_pending` | method | `skills/lazyown_objective.py:261` | `def list_pending(self, limit)` |
| `main` | method | `skills/lazyown_objective.py:456` | `def main()` |
| `next_pending` | method | `skills/lazyown_objective.py:255` | `def next_pending(self)` |
| `read_soul` | method | `skills/lazyown_objective.py:291` | `def read_soul()` |
| `skip` | method | `skills/lazyown_objective.py:249` | `def skip(self, obj_id, reason)` |
| `sort_key` | method | `skills/lazyown_objective.py:116` | `def sort_key(self)` |
| `start` | method | `skills/lazyown_objective.py:252` | `def start(self, obj_id)` |
| `summary` | method | `skills/lazyown_objective.py:271` | `def summary(self)` |
| `update_access` | method | `skills/lazyown_objective.py:430` | `def update_access(self, level, target, method)` |
| `update_credentials` | method | `skills/lazyown_objective.py:403` | `def update_credentials(self, creds)` |
| `update_os` | method | `skills/lazyown_objective.py:396` | `def update_os(self, os_name, target)` |
| `update_phase` | method | `skills/lazyown_objective.py:388` | `def update_phase(self, phase)` |
| `update_target` | method | `skills/lazyown_objective.py:392` | `def update_target(self, target)` |
| `update_vulnerabilities` | method | `skills/lazyown_objective.py:437` | `def update_vulnerabilities(self, vulns)` |
| `write_soul` | method | `skills/lazyown_objective.py:297` | `def write_soul(content)` |
| `ParquetDB` | class | `skills/lazyown_parquet_db.py:244` | `class ParquetDB` |
| `__init__` | method | `skills/lazyown_parquet_db.py:295` | `def __init__(self, lazyown_dir)` |
| `_build_cmd2_category_map` | function | `skills/lazyown_parquet_db.py:146` | `def _build_cmd2_category_map(lazyown_py)` |
| `_classify_row` | function | `skills/lazyown_parquet_db.py:203` | `def _classify_row(command, args, phase_hint)` |
| `_load_session` | method | `skills/lazyown_parquet_db.py:307` | `def _load_session(self)` |
| `_slim` | method | `skills/lazyown_parquet_db.py:930` | `def _slim(row)` |
| `_stable_id` | function | `skills/lazyown_parquet_db.py:178` | `def _stable_id(start, cmd, args, dest_ip)` |
| `annotate` | method | `skills/lazyown_parquet_db.py:405` | `def annotate(self, row_id, success, category, outcome)` |
| `annotate_rich` | method | `skills/lazyown_parquet_db.py:434` | `def annotate_rich(self, row_id, output, finding_type, target_service, target_port, campaign_id, success, category...` |
| `context_for_phase` | method | `skills/lazyown_parquet_db.py:630` | `def context_for_phase(self, phase, target, limit)` |
| `get_pdb` | method | `skills/lazyown_parquet_db.py:948` | `def get_pdb(lazyown_dir)` |
| `list_parquets` | method | `skills/lazyown_parquet_db.py:743` | `def list_parquets(self)` |
| `main` | method | `skills/lazyown_parquet_db.py:961` | `def main()` |
| `predict_success` | method | `skills/lazyown_parquet_db.py:843` | `def predict_success(self, command, category)` |
| `query_atomic` | method | `skills/lazyown_parquet_db.py:576` | `def query_atomic(self, keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` |
| `query_knowledge` | method | `skills/lazyown_parquet_db.py:526` | `def query_knowledge(self, keyword, parquet_name, columns, limit)` |
| `query_session` | method | `skills/lazyown_parquet_db.py:490` | `def query_session(self, phase, target, success_only, limit)` |
| `stats` | method | `skills/lazyown_parquet_db.py:729` | `def stats(self)` |
| `sync` | method | `skills/lazyown_parquet_db.py:316` | `def sync(self, csv_path)` |
| `train_classifier` | method | `skills/lazyown_parquet_db.py:748` | `def train_classifier(self, min_rows)` |
| `verify_model_integrity` | method | `skills/lazyown_parquet_db.py:892` | `def verify_model_integrity(model_path, encoder_path, hash_path)` |
| `PermissionMode` | class | `skills/lazyown_permissions.py:18` | `class PermissionMode(Enum)` |
| `PermissionRule` | class | `skills/lazyown_permissions.py:29` | `class PermissionRule` |
| `PermissionSystem` | class | `skills/lazyown_permissions.py:91` | `class PermissionSystem` |
| `__init__` | method | `skills/lazyown_permissions.py:103` | `def __init__(self, sessions_dir)` |
| `_audit` | method | `skills/lazyown_permissions.py:132` | `def _audit(self, tool, decision, reason, args)` |
| `_load` | method | `skills/lazyown_permissions.py:113` | `def _load(self)` |
| `_matches` | method | `skills/lazyown_permissions.py:219` | `def _matches(self, rule, tool_name, args)` |
| `_save` | method | `skills/lazyown_permissions.py:124` | `def _save(self)` |
| `add_rule` | method | `skills/lazyown_permissions.py:145` | `def add_rule(self, tool_pattern, action, condition, description)` |
| `evaluate` | method | `skills/lazyown_permissions.py:167` | `def evaluate(self, tool_name, arguments)` |
| `list_rules` | method | `skills/lazyown_permissions.py:162` | `def list_rules(self)` |
| `metrics` | method | `skills/lazyown_permissions.py:237` | `def metrics(self)` |
| `remove_rule` | method | `skills/lazyown_permissions.py:151` | `def remove_rule(self, tool_pattern, action)` |
| `set_mode` | method | `skills/lazyown_permissions.py:157` | `def set_mode(self, mode)` |
| `status_text` | method | `skills/lazyown_permissions.py:279` | `def status_text(self)` |
| `to_dict` | method | `skills/lazyown_permissions.py:36` | `def to_dict(self)` |
| `ActionCategory` | class | `skills/lazyown_policy.py:131` | `class ActionCategory(StrEnum)` |
| `ApprovalDecision` | class | `skills/lazyown_policy.py:1326` | `class ApprovalDecision(StrEnum)` |
| `ApprovalGate` | class | `skills/lazyown_policy.py:1606` | `class ApprovalGate` |
| `ApprovalOutcome` | class | `skills/lazyown_policy.py:1356` | `class ApprovalOutcome` |
| `ApprovalRequest` | class | `skills/lazyown_policy.py:1335` | `class ApprovalRequest` |
| `BroadcastApprovalSink` | class | `skills/lazyown_policy.py:1455` | `class BroadcastApprovalSink(IApprovalSink)` |
| `CSVSessionReader` | class | `skills/lazyown_policy.py:843` | `class CSVSessionReader` |
| `CascadeClassifier` | class | `skills/lazyown_policy.py:657` | `class CascadeClassifier` |
| `ClassificationResult` | class | `skills/lazyown_policy.py:306` | `class ClassificationResult` |
| `CompositeApprovalSink` | class | `skills/lazyown_policy.py:1556` | `class CompositeApprovalSink(IApprovalSink)` |
| `Config` | class | `skills/lazyown_policy.py:54` | `class Config` |
| `DetectionRiskAssessor` | class | `skills/lazyown_policy.py:701` | `class DetectionRiskAssessor` |
| `EpisodeRecord` | class | `skills/lazyown_policy.py:347` | `class EpisodeRecord` |
| `ExitCodeClassifier` | class | `skills/lazyown_policy.py:389` | `class ExitCodeClassifier(IOutputClassifier)` |
| `FileApprovalSink` | class | `skills/lazyown_policy.py:1392` | `class FileApprovalSink(IApprovalSink)` |
| `HeuristicClassifier` | class | `skills/lazyown_policy.py:434` | `class HeuristicClassifier(IOutputClassifier)` |
| `HistoryBootstrapper` | class | `skills/lazyown_policy.py:1922` | `class HistoryBootstrapper` |
| `IApprovalSink` | class | `skills/lazyown_policy.py:1375` | `class IApprovalSink(ABC)` |
| `IEpisodeStore` | class | `skills/lazyown_policy.py:899` | `class IEpisodeStore(ABC)` |
| `IOutputClassifier` | class | `skills/lazyown_policy.py:372` | `class IOutputClassifier(ABC)` |
| `JSONLEpisodeStore` | class | `skills/lazyown_policy.py:915` | `class JSONLEpisodeStore(IEpisodeStore)` |
| `LazyOwnPolicyIntegration` | class | `skills/lazyown_policy.py:1294` | `class LazyOwnPolicyIntegration` |
| `OllamaLargeClassifier` | class | `skills/lazyown_policy.py:598` | `class OllamaLargeClassifier(_OllamaClassifierBase)` |
| `OllamaSmallClassifier` | class | `skills/lazyown_policy.py:588` | `class OllamaSmallClassifier(_OllamaClassifierBase)` |
| `OutcomeType` | class | `skills/lazyown_policy.py:146` | `class OutcomeType(StrEnum)` |
| `OverrideRule` | class | `skills/lazyown_policy.py:1042` | `class OverrideRule` |
| `PolicyAdvisor` | class | `skills/lazyown_policy.py:1262` | `class PolicyAdvisor` |
| `PolicyEngine` | class | `skills/lazyown_policy.py:1097` | `class PolicyEngine` |
| `RewardCalculator` | class | `skills/lazyown_policy.py:754` | `class RewardCalculator` |
| `ScopeBoundAutoGate` | class | `skills/lazyown_policy.py:1820` | `class ScopeBoundAutoGate` |
| `SessionClassificationPipeline` | class | `skills/lazyown_policy.py:1194` | `class SessionClassificationPipeline` |
| `StdinApprovalSink` | class | `skills/lazyown_policy.py:1503` | `class StdinApprovalSink(IApprovalSink)` |
| `StepRecord` | class | `skills/lazyown_policy.py:330` | `class StepRecord` |
| `TransitionTable` | class | `skills/lazyown_policy.py:979` | `class TransitionTable` |
| `UserInteractiveClassifier` | class | `skills/lazyown_policy.py:608` | `class UserInteractiveClassifier(IOutputClassifier)` |
| `_OllamaClassifierBase` | class | `skills/lazyown_policy.py:487` | `class _OllamaClassifierBase(IOutputClassifier)` |
| `__init__` | method | `skills/lazyown_policy.py:496` | `def __init__(self, cfg, model, tier_name)` |
| `__init__` | method | `skills/lazyown_policy.py:591` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:601` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:666` | `def __init__(self, cfg, interactive)` |
| `__init__` | method | `skills/lazyown_policy.py:715` | `def __init__(self)` |
| `__init__` | method | `skills/lazyown_policy.py:773` | `def __init__(self, cfg, risk_assessor)` |
| `__init__` | method | `skills/lazyown_policy.py:850` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:923` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:987` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1107` | `def __init__(self, cfg, transitions)` |
| `__init__` | method | `skills/lazyown_policy.py:1202` | `def __init__(self, cfg, interactive)` |
| `__init__` | method | `skills/lazyown_policy.py:1267` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1302` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1400` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `skills/lazyown_policy.py:1463` | `def __init__(self, narrator, file_sink)` |
| `__init__` | method | `skills/lazyown_policy.py:1513` | `def __init__(self, stream)` |
| `__init__` | method | `skills/lazyown_policy.py:1564` | `def __init__(self, sinks)` |
| `__init__` | method | `skills/lazyown_policy.py:1634` | `def __init__(self, sink, payload_path, poll_interval_s, poll_timeout_s, sleep_fn)` |
| `__init__` | method | `skills/lazyown_policy.py:1850` | `def __init__(self, payload_path, in_scope_fn)` |
| `__init__` | method | `skills/lazyown_policy.py:1928` | `def __init__(self, cfg)` |
| `_apply_overrides` | method | `skills/lazyown_policy.py:1162` | `def _apply_overrides(self, recent_states)` |
| `_auto_approve_enabled` | method | `skills/lazyown_policy.py:1654` | `def _auto_approve_enabled(self)` |
| `_build_prompt` | method | `skills/lazyown_policy.py:503` | `def _build_prompt(self, command, args, output, exit_code)` |
| `_call_ollama` | method | `skills/lazyown_policy.py:525` | `def _call_ollama(self, prompt)` |
| `_cmd_analyze` | method | `skills/lazyown_policy.py:1977` | `def _cmd_analyze(cfg, args)` |
| `_cmd_bootstrap` | method | `skills/lazyown_policy.py:1970` | `def _cmd_bootstrap(cfg, _args)` |
| `_cmd_recommend` | method | `skills/lazyown_policy.py:1991` | `def _cmd_recommend(cfg, args)` |
| `_cmd_report` | method | `skills/lazyown_policy.py:2012` | `def _cmd_report(cfg, _args)` |
| `_default_fallback` | method | `skills/lazyown_policy.py:1171` | `def _default_fallback(self, current_state)` |
| `_default_in_scope` | method | `skills/lazyown_policy.py:1779` | `def _default_in_scope(target, entries)` |
| `_default_sleep` | method | `skills/lazyown_policy.py:1721` | `def _default_sleep(seconds)` |
| `_get_oracle` | method | `skills/lazyown_policy.py:718` | `def _get_oracle(self)` |
| `_is_gated` | method | `skills/lazyown_policy.py:1664` | `def _is_gated(self, phase)` |
| `_is_interactive` | method | `skills/lazyown_policy.py:1517` | `def _is_interactive(self)` |
| `_load` | method | `skills/lazyown_policy.py:1024` | `def _load(self)` |
| `_load_scope_guard` | method | `skills/lazyown_policy.py:1739` | `def _load_scope_guard()` |
| `_normalize_scope` | method | `skills/lazyown_policy.py:1800` | `def _normalize_scope(entries)` |
| `_parse_response` | method | `skills/lazyown_policy.py:540` | `def _parse_response(self, data, fallback)` |
| `_read_payload` | method | `skills/lazyown_policy.py:1859` | `def _read_payload(self)` |
| `_save` | method | `skills/lazyown_policy.py:1032` | `def _save(self)` |
| `_setup_logging` | method | `skills/lazyown_policy.py:1960` | `def _setup_logging(cfg)` |
| `_write_all` | method | `skills/lazyown_policy.py:970` | `def _write_all(self, episodes)` |
| `advise` | method | `skills/lazyown_policy.py:1272` | `def advise(self, target)` |
| `announce` | method | `skills/lazyown_policy.py:1384` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1409` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1471` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1523` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1569` | `def announce(self, request)` |
| `append_step` | method | `skills/lazyown_policy.py:903` | `def append_step(self, step)` |
| `append_step` | method | `skills/lazyown_policy.py:927` | `def append_step(self, step)` |
| `assess_probability` | method | `skills/lazyown_policy.py:733` | `def assess_probability(self, command, args, category)` |
| `calculate` | method | `skills/lazyown_policy.py:783` | `def calculate(self, category, outcome)` |
| `calculate_with_detection` | method | `skills/lazyown_policy.py:798` | `def calculate_with_detection(self, category, outcome, command, args)` |
| `classify` | method | `skills/lazyown_policy.py:376` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:401` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:444` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:570` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:616` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:677` | `def classify(self, command, args, output, exit_code)` |
| `default` | method | `skills/lazyown_policy.py:82` | `def default(cls)` |
| `episode_summary` | method | `skills/lazyown_policy.py:1277` | `def episode_summary(self, target)` |
| `from_dict` | method | `skills/lazyown_policy.py:362` | `def from_dict(cls, d)` |
| `get_episode` | method | `skills/lazyown_policy.py:911` | `def get_episode(self, target)` |
| `get_episode` | method | `skills/lazyown_policy.py:963` | `def get_episode(self, target)` |
| `get_recommendations` | method | `skills/lazyown_policy.py:1318` | `def get_recommendations(self, target)` |
| `infer_category` | method | `skills/lazyown_policy.py:267` | `def infer_category(command, args)` |
| `is_approved` | method | `skills/lazyown_policy.py:1365` | `def is_approved(self)` |
| `is_denied` | method | `skills/lazyown_policy.py:1370` | `def is_denied(self)` |
| `is_high_risk` | method | `skills/lazyown_policy.py:746` | `def is_high_risk(self, command, args, category)` |
| `load_all` | method | `skills/lazyown_policy.py:907` | `def load_all(self)` |
| `load_all` | method | `skills/lazyown_policy.py:947` | `def load_all(self)` |
| `main` | method | `skills/lazyown_policy.py:2036` | `def main()` |
| `ollama_url` | method | `skills/lazyown_policy.py:123` | `def ollama_url(self)` |
| `on_command_complete` | method | `skills/lazyown_policy.py:1307` | `def on_command_complete(self, target, command, args, output, exit_code)` |
| `path` | method | `skills/lazyown_policy.py:1405` | `def path(self)` |
| `process` | method | `skills/lazyown_policy.py:1210` | `def process(self, target, command, args, output, exit_code, timestamp)` |
| `query` | method | `skills/lazyown_policy.py:1003` | `def query(self, from_state)` |
| `read` | method | `skills/lazyown_policy.py:855` | `def read(self)` |
| `recommend` | method | `skills/lazyown_policy.py:1111` | `def recommend(self, recent_steps)` |
| `record` | method | `skills/lazyown_policy.py:993` | `def record(self, from_state, to_category, outcome)` |
| `request` | method | `skills/lazyown_policy.py:1667` | `def request(self, target, phase, command, reason)` |
| `request` | method | `skills/lazyown_policy.py:1866` | `def request(self, target, phase, command, reason)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1388` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1426` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1499` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1552` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1576` | `def resolution_for(self, approval_id)` |
| `run` | method | `skills/lazyown_policy.py:1934` | `def run(self)` |
| `to_dict` | method | `skills/lazyown_policy.py:357` | `def to_dict(self)` |
| `unknown` | method | `skills/lazyown_policy.py:317` | `def unknown(cls, tier)` |
| `SessionTranscript` | class | `skills/lazyown_session.py:71` | `class SessionTranscript` |
| `__init__` | method | `skills/lazyown_session.py:82` | `def __init__(self, sessions_dir, session_id)` |
| `_init_meta` | method | `skills/lazyown_session.py:90` | `def _init_meta(self)` |
| `_redact_sensitive` | function | `skills/lazyown_session.py:47` | `def _redact_sensitive(value)` |
| `add_compact_boundary` | method | `skills/lazyown_session.py:209` | `def add_compact_boundary(self, summary, preserved_uuids)` |
| `append` | method | `skills/lazyown_session.py:106` | `def append(self, event_type, data)` |
| `count` | method | `skills/lazyown_session.py:164` | `def count(self)` |
| `fork` | method | `skills/lazyown_session.py:227` | `def fork(self, new_id)` |
| `get_all` | method | `skills/lazyown_session.py:161` | `def get_all(self)` |
| `get_recent` | method | `skills/lazyown_session.py:143` | `def get_recent(self, n)` |
| `get_transcript` | method | `skills/lazyown_session.py:281` | `def get_transcript(sessions_dir, session_id)` |
| `maybe_auto_compact` | method | `skills/lazyown_session.py:174` | `def maybe_auto_compact(self, threshold)` |
| `reset_transcript` | method | `skills/lazyown_session.py:294` | `def reset_transcript(sessions_dir, session_id)` |
| `status_text` | method | `skills/lazyown_session.py:257` | `def status_text(self)` |
| `_gen_EOF` | function | `skills/mcp_generated_tools.py:696` | `def _gen_EOF(arguments, tool_name, _cmd)` |
| `_gen_GET` | function | `skills/mcp_generated_tools.py:704` | `def _gen_GET(arguments, tool_name, _cmd)` |
| `_gen_OPTIONS` | function | `skills/mcp_generated_tools.py:712` | `def _gen_OPTIONS(arguments, tool_name, _cmd)` |
| `_gen_POST` | function | `skills/mcp_generated_tools.py:720` | `def _gen_POST(arguments, tool_name, _cmd)` |
| `_gen_acknowledgearp` | function | `skills/mcp_generated_tools.py:728` | `def _gen_acknowledgearp(arguments, tool_name, _cmd)` |
| `_gen_acknowledgeicmp` | function | `skills/mcp_generated_tools.py:736` | `def _gen_acknowledgeicmp(arguments, tool_name, _cmd)` |
| `_gen_aclpwn_py` | function | `skills/mcp_generated_tools.py:744` | `def _gen_aclpwn_py(arguments, tool_name, _cmd)` |
| `_gen_ad_ldap_enum` | function | `skills/mcp_generated_tools.py:752` | `def _gen_ad_ldap_enum(arguments, tool_name, _cmd)` |
| `_gen_adcs_check` | function | `skills/mcp_generated_tools.py:760` | `def _gen_adcs_check(arguments, tool_name, _cmd)` |
| `_gen_add2find` | function | `skills/mcp_generated_tools.py:768` | `def _gen_add2find(arguments, tool_name, _cmd)` |
| `_gen_addalias` | function | `skills/mcp_generated_tools.py:776` | `def _gen_addalias(arguments, tool_name, _cmd)` |
| `_gen_addcli` | function | `skills/mcp_generated_tools.py:784` | `def _gen_addcli(arguments, tool_name, _cmd)` |
| `_gen_addhosts` | function | `skills/mcp_generated_tools.py:792` | `def _gen_addhosts(arguments, tool_name, _cmd)` |
| `_gen_addspn_py` | function | `skills/mcp_generated_tools.py:800` | `def _gen_addspn_py(arguments, tool_name, _cmd)` |
| `_gen_addusers` | function | `skills/mcp_generated_tools.py:808` | `def _gen_addusers(arguments, tool_name, _cmd)` |
| `_gen_adgetpass` | function | `skills/mcp_generated_tools.py:816` | `def _gen_adgetpass(arguments, tool_name, _cmd)` |
| `_gen_adsso_spray` | function | `skills/mcp_generated_tools.py:824` | `def _gen_adsso_spray(arguments, tool_name, _cmd)` |
| `_gen_adversary` | function | `skills/mcp_generated_tools.py:832` | `def _gen_adversary(arguments, tool_name, _cmd)` |
| `_gen_adversary_yaml` | function | `skills/mcp_generated_tools.py:840` | `def _gen_adversary_yaml(arguments, tool_name, _cmd)` |
| `_gen_aes_pe` | function | `skills/mcp_generated_tools.py:848` | `def _gen_aes_pe(arguments, tool_name, _cmd)` |
| `_gen_ai_playbook` | function | `skills/mcp_generated_tools.py:856` | `def _gen_ai_playbook(arguments, tool_name, _cmd)` |
| `_gen_ai_toggle` | function | `skills/mcp_generated_tools.py:864` | `def _gen_ai_toggle(arguments, tool_name, _cmd)` |
| `_gen_aliass` | function | `skills/mcp_generated_tools.py:872` | `def _gen_aliass(arguments, tool_name, _cmd)` |
| `_gen_allin` | function | `skills/mcp_generated_tools.py:880` | `def _gen_allin(arguments, tool_name, _cmd)` |
| `_gen_alterx` | function | `skills/mcp_generated_tools.py:888` | `def _gen_alterx(arguments, tool_name, _cmd)` |
| `_gen_amass` | function | `skills/mcp_generated_tools.py:896` | `def _gen_amass(arguments, tool_name, _cmd)` |
| `_gen_android_apk` | function | `skills/mcp_generated_tools.py:904` | `def _gen_android_apk(arguments, tool_name, _cmd)` |
| `_gen_android_enum` | function | `skills/mcp_generated_tools.py:912` | `def _gen_android_enum(arguments, tool_name, _cmd)` |
| `_gen_apache_users` | function | `skills/mcp_generated_tools.py:920` | `def _gen_apache_users(arguments, tool_name, _cmd)` |
| `_gen_applocker_csc` | function | `skills/mcp_generated_tools.py:928` | `def _gen_applocker_csc(arguments, tool_name, _cmd)` |
| `_gen_applocker_installutil` | function | `skills/mcp_generated_tools.py:936` | `def _gen_applocker_installutil(arguments, tool_name, _cmd)` |
| `_gen_applocker_msbuild` | function | `skills/mcp_generated_tools.py:944` | `def _gen_applocker_msbuild(arguments, tool_name, _cmd)` |
| `_gen_applocker_mshta` | function | `skills/mcp_generated_tools.py:952` | `def _gen_applocker_mshta(arguments, tool_name, _cmd)` |
| `_gen_applocker_presentation` | function | `skills/mcp_generated_tools.py:960` | `def _gen_applocker_presentation(arguments, tool_name, _cmd)` |
| `_gen_applocker_regsvcs` | function | `skills/mcp_generated_tools.py:968` | `def _gen_applocker_regsvcs(arguments, tool_name, _cmd)` |
| `_gen_applocker_rundll32` | function | `skills/mcp_generated_tools.py:976` | `def _gen_applocker_rundll32(arguments, tool_name, _cmd)` |
| `_gen_apropos` | function | `skills/mcp_generated_tools.py:984` | `def _gen_apropos(arguments, tool_name, _cmd)` |
| `_gen_apt_playbook` | function | `skills/mcp_generated_tools.py:992` | `def _gen_apt_playbook(arguments, tool_name, _cmd)` |
| `_gen_apt_proxy` | function | `skills/mcp_generated_tools.py:1000` | `def _gen_apt_proxy(arguments, tool_name, _cmd)` |
| `_gen_apt_repo` | function | `skills/mcp_generated_tools.py:1008` | `def _gen_apt_repo(arguments, tool_name, _cmd)` |
| `_gen_arjun` | function | `skills/mcp_generated_tools.py:1016` | `def _gen_arjun(arguments, tool_name, _cmd)` |
| `_gen_arpscan` | function | `skills/mcp_generated_tools.py:1024` | `def _gen_arpscan(arguments, tool_name, _cmd)` |
| `_gen_ask` | function | `skills/mcp_generated_tools.py:1032` | `def _gen_ask(arguments, tool_name, _cmd)` |
| `_gen_asprevbase64` | function | `skills/mcp_generated_tools.py:1040` | `def _gen_asprevbase64(arguments, tool_name, _cmd)` |
| `_gen_assign` | function | `skills/mcp_generated_tools.py:1048` | `def _gen_assign(arguments, tool_name, _cmd)` |
| `_gen_atomic_agent` | function | `skills/mcp_generated_tools.py:1056` | `def _gen_atomic_agent(arguments, tool_name, _cmd)` |
| `_gen_atomic_gen` | function | `skills/mcp_generated_tools.py:1064` | `def _gen_atomic_gen(arguments, tool_name, _cmd)` |
| `_gen_atomic_lazyown` | function | `skills/mcp_generated_tools.py:1072` | `def _gen_atomic_lazyown(arguments, tool_name, _cmd)` |
| `_gen_atomic_tests` | function | `skills/mcp_generated_tools.py:1080` | `def _gen_atomic_tests(arguments, tool_name, _cmd)` |
| `_gen_attack_plan` | function | `skills/mcp_generated_tools.py:1088` | `def _gen_attack_plan(arguments, tool_name, _cmd)` |
| `_gen_attack_surface` | function | `skills/mcp_generated_tools.py:1096` | `def _gen_attack_surface(arguments, tool_name, _cmd)` |
| `_gen_audit_complete_keys` | function | `skills/mcp_generated_tools.py:1104` | `def _gen_audit_complete_keys(arguments, tool_name, _cmd)` |
| `_gen_autoblody` | function | `skills/mcp_generated_tools.py:1112` | `def _gen_autoblody(arguments, tool_name, _cmd)` |
| `_gen_automsf` | function | `skills/mcp_generated_tools.py:1120` | `def _gen_automsf(arguments, tool_name, _cmd)` |
| `_gen_autopivot` | function | `skills/mcp_generated_tools.py:1128` | `def _gen_autopivot(arguments, tool_name, _cmd)` |
| `_gen_back` | function | `skills/mcp_generated_tools.py:1136` | `def _gen_back(arguments, tool_name, _cmd)` |
| `_gen_backdoor_factory` | function | `skills/mcp_generated_tools.py:1144` | `def _gen_backdoor_factory(arguments, tool_name, _cmd)` |
| `_gen_banner` | function | `skills/mcp_generated_tools.py:1152` | `def _gen_banner(arguments, tool_name, _cmd)` |
| `_gen_banners` | function | `skills/mcp_generated_tools.py:1160` | `def _gen_banners(arguments, tool_name, _cmd)` |
| `_gen_base64decode` | function | `skills/mcp_generated_tools.py:1168` | `def _gen_base64decode(arguments, tool_name, _cmd)` |
| `_gen_base64encode` | function | `skills/mcp_generated_tools.py:1176` | `def _gen_base64encode(arguments, tool_name, _cmd)` |
| `_gen_batchnmap` | function | `skills/mcp_generated_tools.py:1184` | `def _gen_batchnmap(arguments, tool_name, _cmd)` |
| `_gen_bbot` | function | `skills/mcp_generated_tools.py:1192` | `def _gen_bbot(arguments, tool_name, _cmd)` |
| `_gen_beaconcfg` | function | `skills/mcp_generated_tools.py:1200` | `def _gen_beaconcfg(arguments, tool_name, _cmd)` |
| `_gen_bin2shellcode` | function | `skills/mcp_generated_tools.py:1208` | `def _gen_bin2shellcode(arguments, tool_name, _cmd)` |
| `_gen_binarycheck` | function | `skills/mcp_generated_tools.py:1216` | `def _gen_binarycheck(arguments, tool_name, _cmd)` |
| `_gen_bitm` | function | `skills/mcp_generated_tools.py:1224` | `def _gen_bitm(arguments, tool_name, _cmd)` |
| `_gen_blazy` | function | `skills/mcp_generated_tools.py:1232` | `def _gen_blazy(arguments, tool_name, _cmd)` |
| `_gen_bloodhound` | function | `skills/mcp_generated_tools.py:1240` | `def _gen_bloodhound(arguments, tool_name, _cmd)` |
| `_gen_bloodyAD` | function | `skills/mcp_generated_tools.py:1248` | `def _gen_bloodyAD(arguments, tool_name, _cmd)` |
| `_gen_breacher` | function | `skills/mcp_generated_tools.py:1256` | `def _gen_breacher(arguments, tool_name, _cmd)` |
| `_gen_browse` | function | `skills/mcp_generated_tools.py:1264` | `def _gen_browse(arguments, tool_name, _cmd)` |
| `_gen_c2` | function | `skills/mcp_generated_tools.py:1272` | `def _gen_c2(arguments, tool_name, _cmd)` |
| `_gen_c2_beacon_cmd` | function | `skills/mcp_generated_tools.py:1280` | `def _gen_c2_beacon_cmd(arguments, tool_name, _cmd)` |
| `_gen_c2_beacons` | function | `skills/mcp_generated_tools.py:1288` | `def _gen_c2_beacons(arguments, tool_name, _cmd)` |
| `_gen_c2_implant` | function | `skills/mcp_generated_tools.py:1296` | `def _gen_c2_implant(arguments, tool_name, _cmd)` |
| `_gen_c2_keygen` | function | `skills/mcp_generated_tools.py:1304` | `def _gen_c2_keygen(arguments, tool_name, _cmd)` |
| `_gen_c2_quickstart` | function | `skills/mcp_generated_tools.py:1312` | `def _gen_c2_quickstart(arguments, tool_name, _cmd)` |
| `_gen_c2asm` | function | `skills/mcp_generated_tools.py:1320` | `def _gen_c2asm(arguments, tool_name, _cmd)` |
| `_gen_cacti_exploit` | function | `skills/mcp_generated_tools.py:1328` | `def _gen_cacti_exploit(arguments, tool_name, _cmd)` |
| `_gen_caldera` | function | `skills/mcp_generated_tools.py:1336` | `def _gen_caldera(arguments, tool_name, _cmd)` |
| `_gen_caldera_export` | function | `skills/mcp_generated_tools.py:1344` | `def _gen_caldera_export(arguments, tool_name, _cmd)` |
| `_gen_caldera_import` | function | `skills/mcp_generated_tools.py:1352` | `def _gen_caldera_import(arguments, tool_name, _cmd)` |
| `_gen_camphish` | function | `skills/mcp_generated_tools.py:1360` | `def _gen_camphish(arguments, tool_name, _cmd)` |
| `_gen_certipy` | function | `skills/mcp_generated_tools.py:1368` | `def _gen_certipy(arguments, tool_name, _cmd)` |
| `_gen_certipy_ad` | function | `skills/mcp_generated_tools.py:1376` | `def _gen_certipy_ad(arguments, tool_name, _cmd)` |
| `_gen_cewl` | function | `skills/mcp_generated_tools.py:1384` | `def _gen_cewl(arguments, tool_name, _cmd)` |
| `_gen_chain` | function | `skills/mcp_generated_tools.py:1392` | `def _gen_chain(arguments, tool_name, _cmd)` |
| `_gen_changeme` | function | `skills/mcp_generated_tools.py:1400` | `def _gen_changeme(arguments, tool_name, _cmd)` |
| `_gen_check_update` | function | `skills/mcp_generated_tools.py:1408` | `def _gen_check_update(arguments, tool_name, _cmd)` |
| `_gen_chisel` | function | `skills/mcp_generated_tools.py:1416` | `def _gen_chisel(arguments, tool_name, _cmd)` |
| `_gen_cicd_scan` | function | `skills/mcp_generated_tools.py:1424` | `def _gen_cicd_scan(arguments, tool_name, _cmd)` |
| `_gen_cicd_secrets` | function | `skills/mcp_generated_tools.py:1432` | `def _gen_cicd_secrets(arguments, tool_name, _cmd)` |
| `_gen_clean` | function | `skills/mcp_generated_tools.py:1440` | `def _gen_clean(arguments, tool_name, _cmd)` |
| `_gen_clean_ad` | function | `skills/mcp_generated_tools.py:1448` | `def _gen_clean_ad(arguments, tool_name, _cmd)` |
| `_gen_clock` | function | `skills/mcp_generated_tools.py:1456` | `def _gen_clock(arguments, tool_name, _cmd)` |
| `_gen_clone_site` | function | `skills/mcp_generated_tools.py:1464` | `def _gen_clone_site(arguments, tool_name, _cmd)` |
| `_gen_cloud_buckets` | function | `skills/mcp_generated_tools.py:1472` | `def _gen_cloud_buckets(arguments, tool_name, _cmd)` |
| `_gen_cloud_enum` | function | `skills/mcp_generated_tools.py:1480` | `def _gen_cloud_enum(arguments, tool_name, _cmd)` |
| `_gen_cloud_iam` | function | `skills/mcp_generated_tools.py:1488` | `def _gen_cloud_iam(arguments, tool_name, _cmd)` |
| `_gen_cloud_metadata` | function | `skills/mcp_generated_tools.py:1496` | `def _gen_cloud_metadata(arguments, tool_name, _cmd)` |
| `_gen_cloud_scan` | function | `skills/mcp_generated_tools.py:1504` | `def _gen_cloud_scan(arguments, tool_name, _cmd)` |
| `_gen_cme` | function | `skills/mcp_generated_tools.py:1512` | `def _gen_cme(arguments, tool_name, _cmd)` |
| `_gen_collab_join` | function | `skills/mcp_generated_tools.py:1520` | `def _gen_collab_join(arguments, tool_name, _cmd)` |
| `_gen_commix` | function | `skills/mcp_generated_tools.py:1528` | `def _gen_commix(arguments, tool_name, _cmd)` |
| `_gen_config_banner` | function | `skills/mcp_generated_tools.py:1536` | `def _gen_config_banner(arguments, tool_name, _cmd)` |
| `_gen_conptyshell` | function | `skills/mcp_generated_tools.py:1544` | `def _gen_conptyshell(arguments, tool_name, _cmd)` |
| `_gen_container_detect` | function | `skills/mcp_generated_tools.py:1552` | `def _gen_container_detect(arguments, tool_name, _cmd)` |
| `_gen_container_escape` | function | `skills/mcp_generated_tools.py:1560` | `def _gen_container_escape(arguments, tool_name, _cmd)` |
| `_gen_convert_remcomsvc_from_file` | function | `skills/mcp_generated_tools.py:1568` | `def _gen_convert_remcomsvc_from_file(arguments, tool_name, _cmd)` |
| `_gen_cover_tracks` | function | `skills/mcp_generated_tools.py:1578` | `def _gen_cover_tracks(arguments, tool_name, _cmd)` |
| `_gen_cp` | function | `skills/mcp_generated_tools.py:1586` | `def _gen_cp(arguments, tool_name, _cmd)` |
| `_gen_cports` | function | `skills/mcp_generated_tools.py:1594` | `def _gen_cports(arguments, tool_name, _cmd)` |
| `_gen_crack_cisco_7_password` | function | `skills/mcp_generated_tools.py:1602` | `def _gen_crack_cisco_7_password(arguments, tool_name, _cmd)` |
| `_gen_crack_hashes` | function | `skills/mcp_generated_tools.py:1610` | `def _gen_crack_hashes(arguments, tool_name, _cmd)` |
| `_gen_create_session_json` | function | `skills/mcp_generated_tools.py:1618` | `def _gen_create_session_json(arguments, tool_name, _cmd)` |
| `_gen_create_synthetic` | function | `skills/mcp_generated_tools.py:1626` | `def _gen_create_synthetic(arguments, tool_name, _cmd)` |
| `_gen_createcookie` | function | `skills/mcp_generated_tools.py:1634` | `def _gen_createcookie(arguments, tool_name, _cmd)` |
| `_gen_createcredentials` | function | `skills/mcp_generated_tools.py:1642` | `def _gen_createcredentials(arguments, tool_name, _cmd)` |
| `_gen_createdll` | function | `skills/mcp_generated_tools.py:1650` | `def _gen_createdll(arguments, tool_name, _cmd)` |
| `_gen_createhash` | function | `skills/mcp_generated_tools.py:1658` | `def _gen_createhash(arguments, tool_name, _cmd)` |
| `_gen_createjsonmachine` | function | `skills/mcp_generated_tools.py:1666` | `def _gen_createjsonmachine(arguments, tool_name, _cmd)` |
| `_gen_createjsonmachine_batch` | function | `skills/mcp_generated_tools.py:1674` | `def _gen_createjsonmachine_batch(arguments, tool_name, _cmd)` |
| `_gen_createmail` | function | `skills/mcp_generated_tools.py:1682` | `def _gen_createmail(arguments, tool_name, _cmd)` |
| `_gen_createpayload` | function | `skills/mcp_generated_tools.py:1690` | `def _gen_createpayload(arguments, tool_name, _cmd)` |
| `_gen_createrevshell` | function | `skills/mcp_generated_tools.py:1698` | `def _gen_createrevshell(arguments, tool_name, _cmd)` |
| `_gen_createtargets` | function | `skills/mcp_generated_tools.py:1706` | `def _gen_createtargets(arguments, tool_name, _cmd)` |
| `_gen_createusers_and_hashs` | function | `skills/mcp_generated_tools.py:1714` | `def _gen_createusers_and_hashs(arguments, tool_name, _cmd)` |
| `_gen_createwebshell` | function | `skills/mcp_generated_tools.py:1722` | `def _gen_createwebshell(arguments, tool_name, _cmd)` |
| `_gen_createwinrevshell` | function | `skills/mcp_generated_tools.py:1730` | `def _gen_createwinrevshell(arguments, tool_name, _cmd)` |
| `_gen_cred` | function | `skills/mcp_generated_tools.py:1738` | `def _gen_cred(arguments, tool_name, _cmd)` |
| `_gen_cred_mark_failed` | function | `skills/mcp_generated_tools.py:1746` | `def _gen_cred_mark_failed(arguments, tool_name, _cmd)` |
| `_gen_cred_reuse` | function | `skills/mcp_generated_tools.py:1754` | `def _gen_cred_reuse(arguments, tool_name, _cmd)` |
| `_gen_creds_py` | function | `skills/mcp_generated_tools.py:1762` | `def _gen_creds_py(arguments, tool_name, _cmd)` |
| `_gen_cron` | function | `skills/mcp_generated_tools.py:1770` | `def _gen_cron(arguments, tool_name, _cmd)` |
| `_gen_crunch` | function | `skills/mcp_generated_tools.py:1778` | `def _gen_crunch(arguments, tool_name, _cmd)` |
| `_gen_crystal_ball` | function | `skills/mcp_generated_tools.py:1786` | `def _gen_crystal_ball(arguments, tool_name, _cmd)` |
| `_gen_ctx` | function | `skills/mcp_generated_tools.py:1794` | `def _gen_ctx(arguments, tool_name, _cmd)` |
| `_gen_cubespraying` | function | `skills/mcp_generated_tools.py:1802` | `def _gen_cubespraying(arguments, tool_name, _cmd)` |
| `_gen_cve` | function | `skills/mcp_generated_tools.py:1810` | `def _gen_cve(arguments, tool_name, _cmd)` |
| `_gen_d3monizedshell` | function | `skills/mcp_generated_tools.py:1818` | `def _gen_d3monizedshell(arguments, tool_name, _cmd)` |
| `_gen_dacledit` | function | `skills/mcp_generated_tools.py:1826` | `def _gen_dacledit(arguments, tool_name, _cmd)` |
| `_gen_darkarmour` | function | `skills/mcp_generated_tools.py:1834` | `def _gen_darkarmour(arguments, tool_name, _cmd)` |
| `_gen_dashboard` | function | `skills/mcp_generated_tools.py:1842` | `def _gen_dashboard(arguments, tool_name, _cmd)` |
| `_gen_davtest` | function | `skills/mcp_generated_tools.py:1850` | `def _gen_davtest(arguments, tool_name, _cmd)` |
| `_gen_db_creds` | function | `skills/mcp_generated_tools.py:1858` | `def _gen_db_creds(arguments, tool_name, _cmd)` |
| `_gen_db_export` | function | `skills/mcp_generated_tools.py:1866` | `def _gen_db_export(arguments, tool_name, _cmd)` |
| `_gen_db_hosts` | function | `skills/mcp_generated_tools.py:1874` | `def _gen_db_hosts(arguments, tool_name, _cmd)` |
| `_gen_db_import` | function | `skills/mcp_generated_tools.py:1882` | `def _gen_db_import(arguments, tool_name, _cmd)` |
| `_gen_db_init` | function | `skills/mcp_generated_tools.py:1890` | `def _gen_db_init(arguments, tool_name, _cmd)` |
| `_gen_db_loot` | function | `skills/mcp_generated_tools.py:1898` | `def _gen_db_loot(arguments, tool_name, _cmd)` |
| `_gen_db_notes` | function | `skills/mcp_generated_tools.py:1906` | `def _gen_db_notes(arguments, tool_name, _cmd)` |
| `_gen_db_services` | function | `skills/mcp_generated_tools.py:1914` | `def _gen_db_services(arguments, tool_name, _cmd)` |
| `_gen_db_status` | function | `skills/mcp_generated_tools.py:1922` | `def _gen_db_status(arguments, tool_name, _cmd)` |
| `_gen_db_vulns` | function | `skills/mcp_generated_tools.py:1930` | `def _gen_db_vulns(arguments, tool_name, _cmd)` |
| `_gen_db_workspace` | function | `skills/mcp_generated_tools.py:1938` | `def _gen_db_workspace(arguments, tool_name, _cmd)` |
| `_gen_dcomexec` | function | `skills/mcp_generated_tools.py:1946` | `def _gen_dcomexec(arguments, tool_name, _cmd)` |
| `_gen_decode` | function | `skills/mcp_generated_tools.py:1954` | `def _gen_decode(arguments, tool_name, _cmd)` |
| `_gen_decrypt` | function | `skills/mcp_generated_tools.py:1962` | `def _gen_decrypt(arguments, tool_name, _cmd)` |
| `_gen_depconfuse` | function | `skills/mcp_generated_tools.py:1970` | `def _gen_depconfuse(arguments, tool_name, _cmd)` |
| `_gen_depscan` | function | `skills/mcp_generated_tools.py:1978` | `def _gen_depscan(arguments, tool_name, _cmd)` |
| `_gen_detect_edr` | function | `skills/mcp_generated_tools.py:1986` | `def _gen_detect_edr(arguments, tool_name, _cmd)` |
| `_gen_dig` | function | `skills/mcp_generated_tools.py:1994` | `def _gen_dig(arguments, tool_name, _cmd)` |
| `_gen_digdug` | function | `skills/mcp_generated_tools.py:2002` | `def _gen_digdug(arguments, tool_name, _cmd)` |
| `_gen_dirsearch` | function | `skills/mcp_generated_tools.py:2010` | `def _gen_dirsearch(arguments, tool_name, _cmd)` |
| `_gen_disableav` | function | `skills/mcp_generated_tools.py:2018` | `def _gen_disableav(arguments, tool_name, _cmd)` |
| `_gen_dmitry` | function | `skills/mcp_generated_tools.py:2026` | `def _gen_dmitry(arguments, tool_name, _cmd)` |
| `_gen_dns_beacon` | function | `skills/mcp_generated_tools.py:2034` | `def _gen_dns_beacon(arguments, tool_name, _cmd)` |
| `_gen_dns_beacon_status` | function | `skills/mcp_generated_tools.py:2042` | `def _gen_dns_beacon_status(arguments, tool_name, _cmd)` |
| `_gen_dns_exfil_listen` | function | `skills/mcp_generated_tools.py:2050` | `def _gen_dns_exfil_listen(arguments, tool_name, _cmd)` |
| `_gen_dnschef` | function | `skills/mcp_generated_tools.py:2058` | `def _gen_dnschef(arguments, tool_name, _cmd)` |
| `_gen_dnsenum` | function | `skills/mcp_generated_tools.py:2066` | `def _gen_dnsenum(arguments, tool_name, _cmd)` |
| `_gen_dnsmap` | function | `skills/mcp_generated_tools.py:2074` | `def _gen_dnsmap(arguments, tool_name, _cmd)` |
| `_gen_dnstool_py` | function | `skills/mcp_generated_tools.py:2082` | `def _gen_dnstool_py(arguments, tool_name, _cmd)` |
| `_gen_docker_enum` | function | `skills/mcp_generated_tools.py:2090` | `def _gen_docker_enum(arguments, tool_name, _cmd)` |
| `_gen_doctor` | function | `skills/mcp_generated_tools.py:2098` | `def _gen_doctor(arguments, tool_name, _cmd)` |
| `_gen_dominion` | function | `skills/mcp_generated_tools.py:2106` | `def _gen_dominion(arguments, tool_name, _cmd)` |
| `_gen_download_c2` | function | `skills/mcp_generated_tools.py:2114` | `def _gen_download_c2(arguments, tool_name, _cmd)` |
| `_gen_download_exploit` | function | `skills/mcp_generated_tools.py:2122` | `def _gen_download_exploit(arguments, tool_name, _cmd)` |
| `_gen_download_malwarebazar` | function | `skills/mcp_generated_tools.py:2130` | `def _gen_download_malwarebazar(arguments, tool_name, _cmd)` |
| `_gen_download_resources` | function | `skills/mcp_generated_tools.py:2138` | `def _gen_download_resources(arguments, tool_name, _cmd)` |
| `_gen_downloader` | function | `skills/mcp_generated_tools.py:2146` | `def _gen_downloader(arguments, tool_name, _cmd)` |
| `_gen_dpapi_blob` | function | `skills/mcp_generated_tools.py:2154` | `def _gen_dpapi_blob(arguments, tool_name, _cmd)` |
| `_gen_dpapi_harvest` | function | `skills/mcp_generated_tools.py:2162` | `def _gen_dpapi_harvest(arguments, tool_name, _cmd)` |
| `_gen_dpapi_masterkeys` | function | `skills/mcp_generated_tools.py:2170` | `def _gen_dpapi_masterkeys(arguments, tool_name, _cmd)` |
| `_gen_dploot` | function | `skills/mcp_generated_tools.py:2178` | `def _gen_dploot(arguments, tool_name, _cmd)` |
| `_gen_dr0p1t` | function | `skills/mcp_generated_tools.py:2186` | `def _gen_dr0p1t(arguments, tool_name, _cmd)` |
| `_gen_duckyspark` | function | `skills/mcp_generated_tools.py:2194` | `def _gen_duckyspark(arguments, tool_name, _cmd)` |
| `_gen_edr_detect` | function | `skills/mcp_generated_tools.py:2202` | `def _gen_edr_detect(arguments, tool_name, _cmd)` |
| `_gen_edr_profile` | function | `skills/mcp_generated_tools.py:2210` | `def _gen_edr_profile(arguments, tool_name, _cmd)` |
| `_gen_edr_script` | function | `skills/mcp_generated_tools.py:2218` | `def _gen_edr_script(arguments, tool_name, _cmd)` |
| `_gen_emp3r0r` | function | `skills/mcp_generated_tools.py:2226` | `def _gen_emp3r0r(arguments, tool_name, _cmd)` |
| `_gen_empire` | function | `skills/mcp_generated_tools.py:2234` | `def _gen_empire(arguments, tool_name, _cmd)` |
| `_gen_encode` | function | `skills/mcp_generated_tools.py:2242` | `def _gen_encode(arguments, tool_name, _cmd)` |
| `_gen_encoderpayload` | function | `skills/mcp_generated_tools.py:2250` | `def _gen_encoderpayload(arguments, tool_name, _cmd)` |
| `_gen_encodewinbase64` | function | `skills/mcp_generated_tools.py:2258` | `def _gen_encodewinbase64(arguments, tool_name, _cmd)` |
| `_gen_encrypt` | function | `skills/mcp_generated_tools.py:2266` | `def _gen_encrypt(arguments, tool_name, _cmd)` |
| `_gen_engage` | function | `skills/mcp_generated_tools.py:2274` | `def _gen_engage(arguments, tool_name, _cmd)` |
| `_gen_enum4linux` | function | `skills/mcp_generated_tools.py:2282` | `def _gen_enum4linux(arguments, tool_name, _cmd)` |
| `_gen_enum4linux_ng` | function | `skills/mcp_generated_tools.py:2290` | `def _gen_enum4linux_ng(arguments, tool_name, _cmd)` |
| `_gen_eternal` | function | `skills/mcp_generated_tools.py:2298` | `def _gen_eternal(arguments, tool_name, _cmd)` |
| `_gen_evasion` | function | `skills/mcp_generated_tools.py:2306` | `def _gen_evasion(arguments, tool_name, _cmd)` |
| `_gen_evasive` | function | `skills/mcp_generated_tools.py:2314` | `def _gen_evasive(arguments, tool_name, _cmd)` |
| `_gen_evasive_payload` | function | `skills/mcp_generated_tools.py:2322` | `def _gen_evasive_payload(arguments, tool_name, _cmd)` |
| `_gen_event_log` | function | `skills/mcp_generated_tools.py:2330` | `def _gen_event_log(arguments, tool_name, _cmd)` |
| `_gen_evidence` | function | `skills/mcp_generated_tools.py:2338` | `def _gen_evidence(arguments, tool_name, _cmd)` |
| `_gen_evil_ssdp` | function | `skills/mcp_generated_tools.py:2346` | `def _gen_evil_ssdp(arguments, tool_name, _cmd)` |
| `_gen_evilwinrm` | function | `skills/mcp_generated_tools.py:2354` | `def _gen_evilwinrm(arguments, tool_name, _cmd)` |
| `_gen_excelntdonut` | function | `skills/mcp_generated_tools.py:2362` | `def _gen_excelntdonut(arguments, tool_name, _cmd)` |
| `_gen_exe2bin` | function | `skills/mcp_generated_tools.py:2370` | `def _gen_exe2bin(arguments, tool_name, _cmd)` |
| `_gen_exe2donutbin` | function | `skills/mcp_generated_tools.py:2378` | `def _gen_exe2donutbin(arguments, tool_name, _cmd)` |
| `_gen_exfil_auto` | function | `skills/mcp_generated_tools.py:2386` | `def _gen_exfil_auto(arguments, tool_name, _cmd)` |
| `_gen_exfil_discord` | function | `skills/mcp_generated_tools.py:2394` | `def _gen_exfil_discord(arguments, tool_name, _cmd)` |
| `_gen_exfil_dns` | function | `skills/mcp_generated_tools.py:2402` | `def _gen_exfil_dns(arguments, tool_name, _cmd)` |
| `_gen_exfil_gcs` | function | `skills/mcp_generated_tools.py:2410` | `def _gen_exfil_gcs(arguments, tool_name, _cmd)` |
| `_gen_exfil_http` | function | `skills/mcp_generated_tools.py:2418` | `def _gen_exfil_http(arguments, tool_name, _cmd)` |
| `_gen_exfil_s3` | function | `skills/mcp_generated_tools.py:2426` | `def _gen_exfil_s3(arguments, tool_name, _cmd)` |
| `_gen_exfil_start_server` | function | `skills/mcp_generated_tools.py:2434` | `def _gen_exfil_start_server(arguments, tool_name, _cmd)` |
| `_gen_exfil_telegram` | function | `skills/mcp_generated_tools.py:2442` | `def _gen_exfil_telegram(arguments, tool_name, _cmd)` |
| `_gen_exit` | function | `skills/mcp_generated_tools.py:2450` | `def _gen_exit(arguments, tool_name, _cmd)` |
| `_gen_explore` | function | `skills/mcp_generated_tools.py:2458` | `def _gen_explore(arguments, tool_name, _cmd)` |
| `_gen_extract_ports` | function | `skills/mcp_generated_tools.py:2466` | `def _gen_extract_ports(arguments, tool_name, _cmd)` |
| `_gen_extract_yaml` | function | `skills/mcp_generated_tools.py:2474` | `def _gen_extract_yaml(arguments, tool_name, _cmd)` |
| `_gen_eyewitness` | function | `skills/mcp_generated_tools.py:2482` | `def _gen_eyewitness(arguments, tool_name, _cmd)` |
| `_gen_eyewitness_py` | function | `skills/mcp_generated_tools.py:2490` | `def _gen_eyewitness_py(arguments, tool_name, _cmd)` |
| `_gen_feroxbuster` | function | `skills/mcp_generated_tools.py:2498` | `def _gen_feroxbuster(arguments, tool_name, _cmd)` |
| `_gen_filtering` | function | `skills/mcp_generated_tools.py:2506` | `def _gen_filtering(arguments, tool_name, _cmd)` |
| `_gen_finalrecon` | function | `skills/mcp_generated_tools.py:2514` | `def _gen_finalrecon(arguments, tool_name, _cmd)` |
| `_gen_find` | function | `skills/mcp_generated_tools.py:2522` | `def _gen_find(arguments, tool_name, _cmd)` |
| `_gen_finger_user_enum` | function | `skills/mcp_generated_tools.py:2530` | `def _gen_finger_user_enum(arguments, tool_name, _cmd)` |
| `_gen_fixel` | function | `skills/mcp_generated_tools.py:2538` | `def _gen_fixel(arguments, tool_name, _cmd)` |
| `_gen_fixperm` | function | `skills/mcp_generated_tools.py:2546` | `def _gen_fixperm(arguments, tool_name, _cmd)` |
| `_gen_follina` | function | `skills/mcp_generated_tools.py:2554` | `def _gen_follina(arguments, tool_name, _cmd)` |
| `_gen_form` | function | `skills/mcp_generated_tools.py:2562` | `def _gen_form(arguments, tool_name, _cmd)` |
| `_gen_ftp` | function | `skills/mcp_generated_tools.py:2570` | `def _gen_ftp(arguments, tool_name, _cmd)` |
| `_gen_fuzz` | function | `skills/mcp_generated_tools.py:2578` | `def _gen_fuzz(arguments, tool_name, _cmd)` |
| `_gen_fz` | function | `skills/mcp_generated_tools.py:2586` | `def _gen_fz(arguments, tool_name, _cmd)` |
| `_gen_gencert` | function | `skills/mcp_generated_tools.py:2594` | `def _gen_gencert(arguments, tool_name, _cmd)` |
| `_gen_generate` | function | `skills/mcp_generated_tools.py:2602` | `def _gen_generate(arguments, tool_name, _cmd)` |
| `_gen_generate_playbook` | function | `skills/mcp_generated_tools.py:2610` | `def _gen_generate_playbook(arguments, tool_name, _cmd)` |
| `_gen_generate_revshell` | function | `skills/mcp_generated_tools.py:2618` | `def _gen_generate_revshell(arguments, tool_name, _cmd)` |
| `_gen_generatedic` | function | `skills/mcp_generated_tools.py:2626` | `def _gen_generatedic(arguments, tool_name, _cmd)` |
| `_gen_getTGT` | function | `skills/mcp_generated_tools.py:2634` | `def _gen_getTGT(arguments, tool_name, _cmd)` |
| `_gen_get_avaible_actions` | function | `skills/mcp_generated_tools.py:2642` | `def _gen_get_avaible_actions(arguments, tool_name, _cmd)` |
| `_gen_getadusers` | function | `skills/mcp_generated_tools.py:2650` | `def _gen_getadusers(arguments, tool_name, _cmd)` |

Next: [SYMBOLS_p21.md](SYMBOLS_p21.md)
