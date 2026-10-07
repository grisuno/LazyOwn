# Symbols (page 20 of 35)
Previous: [SYMBOLS_p19.md](SYMBOLS_p19.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `submit` | method | `skills/lazyown_mcp_helpers.py:656` | `def submit(self, command, runner, timeout)` |
| `take_snapshot` | method | `skills/lazyown_mcp_helpers.py:709` | `def take_snapshot(sessions_dir, payload, world_model, tasks)` |
| `call_tool` | function | `skills/lazyown_mcp_opencode.py:76` | `def call_tool(name, arguments)` |
| `list_tools` | function | `skills/lazyown_mcp_opencode.py:57` | `def list_tools()` |
| `main` | function | `skills/lazyown_mcp_opencode.py:84` | `def main()` |
| `Objective` | class | `skills/lazyown_objective.py:105` | `class Objective` |
| `ObjectiveStore` | class | `skills/lazyown_objective.py:123` | `class ObjectiveStore` |
| `SoulUpdater` | class | `skills/lazyown_objective.py:333` | `class SoulUpdater` |
| `__init__` | method | `skills/lazyown_objective.py:131` | `def __init__(self, path)` |
| `__init__` | method | `skills/lazyown_objective.py:353` | `def __init__(self)` |
| `_load_all` | method | `skills/lazyown_objective.py:138` | `def _load_all(self)` |
| `_now` | method | `skills/lazyown_objective.py:135` | `def _now(self)` |
| `_patch_line` | method | `skills/lazyown_objective.py:378` | `def _patch_line(self, key, value)` |
| `_patch_section` | method | `skills/lazyown_objective.py:363` | `def _patch_section(self, header, new_body)` |
| `_read` | method | `skills/lazyown_objective.py:358` | `def _read(self)` |
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
| `main` | method | `skills/lazyown_objective.py:459` | `def main()` |
| `next_pending` | method | `skills/lazyown_objective.py:255` | `def next_pending(self)` |
| `read_soul` | method | `skills/lazyown_objective.py:291` | `def read_soul()` |
| `skip` | method | `skills/lazyown_objective.py:249` | `def skip(self, obj_id, reason)` |
| `sort_key` | method | `skills/lazyown_objective.py:116` | `def sort_key(self)` |
| `start` | method | `skills/lazyown_objective.py:252` | `def start(self, obj_id)` |
| `summary` | method | `skills/lazyown_objective.py:271` | `def summary(self)` |
| `update_access` | method | `skills/lazyown_objective.py:433` | `def update_access(self, level, target, method)` |
| `update_credentials` | method | `skills/lazyown_objective.py:406` | `def update_credentials(self, creds)` |
| `update_os` | method | `skills/lazyown_objective.py:399` | `def update_os(self, os_name, target)` |
| `update_phase` | method | `skills/lazyown_objective.py:391` | `def update_phase(self, phase)` |
| `update_target` | method | `skills/lazyown_objective.py:395` | `def update_target(self, target)` |
| `update_vulnerabilities` | method | `skills/lazyown_objective.py:440` | `def update_vulnerabilities(self, vulns)` |
| `write_soul` | method | `skills/lazyown_objective.py:297` | `def write_soul(content)` |
| `ParquetDB` | class | `skills/lazyown_parquet_db.py:215` | `class ParquetDB` |
| `__init__` | method | `skills/lazyown_parquet_db.py:251` | `def __init__(self, lazyown_dir)` |
| `_build_cmd2_category_map` | function | `skills/lazyown_parquet_db.py:119` | `def _build_cmd2_category_map(lazyown_py)` |
| `_classify_row` | function | `skills/lazyown_parquet_db.py:175` | `def _classify_row(command, args, phase_hint)` |
| `_load_session` | method | `skills/lazyown_parquet_db.py:266` | `def _load_session(self)` |
| `_slim` | method | `skills/lazyown_parquet_db.py:895` | `def _slim(row)` |
| `_stable_id` | function | `skills/lazyown_parquet_db.py:151` | `def _stable_id(start, cmd, args, dest_ip)` |
| `annotate` | method | `skills/lazyown_parquet_db.py:362` | `def annotate(self, row_id, success, category, outcome)` |
| `annotate_rich` | method | `skills/lazyown_parquet_db.py:391` | `def annotate_rich(self, row_id, output, finding_type, target_service, target_port, campaign_id, success, category...` |
| `context_for_phase` | method | `skills/lazyown_parquet_db.py:590` | `def context_for_phase(self, phase, target, limit)` |
| `get_pdb` | method | `skills/lazyown_parquet_db.py:913` | `def get_pdb(lazyown_dir)` |
| `list_parquets` | method | `skills/lazyown_parquet_db.py:708` | `def list_parquets(self)` |
| `main` | method | `skills/lazyown_parquet_db.py:925` | `def main()` |
| `predict_success` | method | `skills/lazyown_parquet_db.py:806` | `def predict_success(self, command, category)` |
| `query_atomic` | method | `skills/lazyown_parquet_db.py:537` | `def query_atomic(self, keyword, mitre_id, platform, scope, has_prereqs, complexity, limit, include_command)` |
| `query_knowledge` | method | `skills/lazyown_parquet_db.py:485` | `def query_knowledge(self, keyword, parquet_name, columns, limit)` |
| `query_session` | method | `skills/lazyown_parquet_db.py:449` | `def query_session(self, phase, target, success_only, limit)` |
| `stats` | method | `skills/lazyown_parquet_db.py:694` | `def stats(self)` |
| `sync` | method | `skills/lazyown_parquet_db.py:275` | `def sync(self, csv_path)` |
| `train_classifier` | method | `skills/lazyown_parquet_db.py:713` | `def train_classifier(self, min_rows)` |
| `verify_model_integrity` | method | `skills/lazyown_parquet_db.py:855` | `def verify_model_integrity(model_path, encoder_path, hash_path)` |
| `PermissionMode` | class | `skills/lazyown_permissions.py:18` | `class PermissionMode(Enum)` |
| `PermissionRule` | class | `skills/lazyown_permissions.py:29` | `class PermissionRule` |
| `PermissionSystem` | class | `skills/lazyown_permissions.py:89` | `class PermissionSystem` |
| `__init__` | method | `skills/lazyown_permissions.py:101` | `def __init__(self, sessions_dir)` |
| `_audit` | method | `skills/lazyown_permissions.py:130` | `def _audit(self, tool, decision, reason, args)` |
| `_load` | method | `skills/lazyown_permissions.py:111` | `def _load(self)` |
| `_matches` | method | `skills/lazyown_permissions.py:221` | `def _matches(self, rule, tool_name, args)` |
| `_save` | method | `skills/lazyown_permissions.py:122` | `def _save(self)` |
| `add_rule` | method | `skills/lazyown_permissions.py:143` | `def add_rule(self, tool_pattern, action, condition, description)` |
| `evaluate` | method | `skills/lazyown_permissions.py:169` | `def evaluate(self, tool_name, arguments)` |
| `list_rules` | method | `skills/lazyown_permissions.py:164` | `def list_rules(self)` |
| `metrics` | method | `skills/lazyown_permissions.py:239` | `def metrics(self)` |
| `remove_rule` | method | `skills/lazyown_permissions.py:150` | `def remove_rule(self, tool_pattern, action)` |
| `set_mode` | method | `skills/lazyown_permissions.py:159` | `def set_mode(self, mode)` |
| `status_text` | method | `skills/lazyown_permissions.py:278` | `def status_text(self)` |
| `to_dict` | method | `skills/lazyown_permissions.py:36` | `def to_dict(self)` |
| `ActionCategory` | class | `skills/lazyown_policy.py:131` | `class ActionCategory(StrEnum)` |
| `ApprovalDecision` | class | `skills/lazyown_policy.py:1299` | `class ApprovalDecision(StrEnum)` |
| `ApprovalGate` | class | `skills/lazyown_policy.py:1582` | `class ApprovalGate` |
| `ApprovalOutcome` | class | `skills/lazyown_policy.py:1329` | `class ApprovalOutcome` |
| `ApprovalRequest` | class | `skills/lazyown_policy.py:1308` | `class ApprovalRequest` |
| `BroadcastApprovalSink` | class | `skills/lazyown_policy.py:1428` | `class BroadcastApprovalSink(IApprovalSink)` |
| `CSVSessionReader` | class | `skills/lazyown_policy.py:802` | `class CSVSessionReader` |
| `CascadeClassifier` | class | `skills/lazyown_policy.py:614` | `class CascadeClassifier` |
| `ClassificationResult` | class | `skills/lazyown_policy.py:259` | `class ClassificationResult` |
| `CompositeApprovalSink` | class | `skills/lazyown_policy.py:1534` | `class CompositeApprovalSink(IApprovalSink)` |
| `Config` | class | `skills/lazyown_policy.py:54` | `class Config` |
| `DetectionRiskAssessor` | class | `skills/lazyown_policy.py:658` | `class DetectionRiskAssessor` |
| `EpisodeRecord` | class | `skills/lazyown_policy.py:300` | `class EpisodeRecord` |
| `ExitCodeClassifier` | class | `skills/lazyown_policy.py:342` | `class ExitCodeClassifier(IOutputClassifier)` |
| `FileApprovalSink` | class | `skills/lazyown_policy.py:1365` | `class FileApprovalSink(IApprovalSink)` |
| `HeuristicClassifier` | class | `skills/lazyown_policy.py:387` | `class HeuristicClassifier(IOutputClassifier)` |
| `HistoryBootstrapper` | class | `skills/lazyown_policy.py:1897` | `class HistoryBootstrapper` |
| `IApprovalSink` | class | `skills/lazyown_policy.py:1348` | `class IApprovalSink(ABC)` |
| `IEpisodeStore` | class | `skills/lazyown_policy.py:858` | `class IEpisodeStore(ABC)` |
| `IOutputClassifier` | class | `skills/lazyown_policy.py:325` | `class IOutputClassifier(ABC)` |
| `JSONLEpisodeStore` | class | `skills/lazyown_policy.py:874` | `class JSONLEpisodeStore(IEpisodeStore)` |
| `LazyOwnPolicyIntegration` | class | `skills/lazyown_policy.py:1267` | `class LazyOwnPolicyIntegration` |
| `OllamaLargeClassifier` | class | `skills/lazyown_policy.py:555` | `class OllamaLargeClassifier(_OllamaClassifierBase)` |
| `OllamaSmallClassifier` | class | `skills/lazyown_policy.py:545` | `class OllamaSmallClassifier(_OllamaClassifierBase)` |
| `OutcomeType` | class | `skills/lazyown_policy.py:146` | `class OutcomeType(StrEnum)` |
| `OverrideRule` | class | `skills/lazyown_policy.py:1001` | `class OverrideRule` |
| `PolicyAdvisor` | class | `skills/lazyown_policy.py:1231` | `class PolicyAdvisor` |
| `PolicyEngine` | class | `skills/lazyown_policy.py:1056` | `class PolicyEngine` |
| `RewardCalculator` | class | `skills/lazyown_policy.py:709` | `class RewardCalculator` |
| `ScopeBoundAutoGate` | class | `skills/lazyown_policy.py:1793` | `class ScopeBoundAutoGate` |
| `SessionClassificationPipeline` | class | `skills/lazyown_policy.py:1163` | `class SessionClassificationPipeline` |
| `StdinApprovalSink` | class | `skills/lazyown_policy.py:1478` | `class StdinApprovalSink(IApprovalSink)` |
| `StepRecord` | class | `skills/lazyown_policy.py:283` | `class StepRecord` |
| `TransitionTable` | class | `skills/lazyown_policy.py:938` | `class TransitionTable` |
| `UserInteractiveClassifier` | class | `skills/lazyown_policy.py:565` | `class UserInteractiveClassifier(IOutputClassifier)` |
| `_OllamaClassifierBase` | class | `skills/lazyown_policy.py:440` | `class _OllamaClassifierBase(IOutputClassifier)` |
| `__init__` | method | `skills/lazyown_policy.py:449` | `def __init__(self, cfg, model, tier_name)` |
| `__init__` | method | `skills/lazyown_policy.py:548` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:558` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:623` | `def __init__(self, cfg, interactive)` |
| `__init__` | method | `skills/lazyown_policy.py:672` | `def __init__(self)` |
| `__init__` | method | `skills/lazyown_policy.py:730` | `def __init__(self, cfg, risk_assessor)` |
| `__init__` | method | `skills/lazyown_policy.py:809` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:882` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:946` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1066` | `def __init__(self, cfg, transitions)` |
| `__init__` | method | `skills/lazyown_policy.py:1171` | `def __init__(self, cfg, interactive)` |
| `__init__` | method | `skills/lazyown_policy.py:1236` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1275` | `def __init__(self, cfg)` |
| `__init__` | method | `skills/lazyown_policy.py:1373` | `def __init__(self, sessions_dir)` |
| `__init__` | method | `skills/lazyown_policy.py:1436` | `def __init__(self, narrator, file_sink)` |
| `__init__` | method | `skills/lazyown_policy.py:1491` | `def __init__(self, stream)` |
| `__init__` | method | `skills/lazyown_policy.py:1542` | `def __init__(self, sinks)` |
| `__init__` | method | `skills/lazyown_policy.py:1610` | `def __init__(self, sink, payload_path, poll_interval_s, poll_timeout_s, sleep_fn)` |
| `__init__` | method | `skills/lazyown_policy.py:1823` | `def __init__(self, payload_path, in_scope_fn)` |
| `__init__` | method | `skills/lazyown_policy.py:1903` | `def __init__(self, cfg)` |
| `_apply_overrides` | method | `skills/lazyown_policy.py:1126` | `def _apply_overrides(self, recent_states)` |
| `_auto_approve_enabled` | method | `skills/lazyown_policy.py:1628` | `def _auto_approve_enabled(self)` |
| `_build_prompt` | method | `skills/lazyown_policy.py:456` | `def _build_prompt(self, command, args, output, exit_code)` |
| `_call_ollama` | method | `skills/lazyown_policy.py:478` | `def _call_ollama(self, prompt)` |
| `_cmd_analyze` | method | `skills/lazyown_policy.py:1953` | `def _cmd_analyze(cfg, args)` |
| `_cmd_bootstrap` | method | `skills/lazyown_policy.py:1946` | `def _cmd_bootstrap(cfg, _args)` |
| `_cmd_recommend` | method | `skills/lazyown_policy.py:1967` | `def _cmd_recommend(cfg, args)` |
| `_cmd_report` | method | `skills/lazyown_policy.py:1988` | `def _cmd_report(cfg, _args)` |
| `_default_fallback` | method | `skills/lazyown_policy.py:1137` | `def _default_fallback(self, current_state)` |
| `_default_in_scope` | method | `skills/lazyown_policy.py:1752` | `def _default_in_scope(target, entries)` |
| `_default_sleep` | method | `skills/lazyown_policy.py:1695` | `def _default_sleep(seconds)` |
| `_get_oracle` | method | `skills/lazyown_policy.py:675` | `def _get_oracle(self)` |
| `_is_gated` | method | `skills/lazyown_policy.py:1638` | `def _is_gated(self, phase)` |
| `_is_interactive` | method | `skills/lazyown_policy.py:1495` | `def _is_interactive(self)` |
| `_load` | method | `skills/lazyown_policy.py:983` | `def _load(self)` |
| `_load_scope_guard` | method | `skills/lazyown_policy.py:1712` | `def _load_scope_guard()` |
| `_normalize_scope` | method | `skills/lazyown_policy.py:1773` | `def _normalize_scope(entries)` |
| `_parse_response` | method | `skills/lazyown_policy.py:495` | `def _parse_response(self, data, fallback)` |
| `_read_payload` | method | `skills/lazyown_policy.py:1832` | `def _read_payload(self)` |
| `_save` | method | `skills/lazyown_policy.py:991` | `def _save(self)` |
| `_setup_logging` | method | `skills/lazyown_policy.py:1937` | `def _setup_logging(cfg)` |
| `_write_all` | method | `skills/lazyown_policy.py:929` | `def _write_all(self, episodes)` |
| `advise` | method | `skills/lazyown_policy.py:1241` | `def advise(self, target)` |
| `announce` | method | `skills/lazyown_policy.py:1357` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1382` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1444` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1501` | `def announce(self, request)` |
| `announce` | method | `skills/lazyown_policy.py:1547` | `def announce(self, request)` |
| `append_step` | method | `skills/lazyown_policy.py:862` | `def append_step(self, step)` |
| `append_step` | method | `skills/lazyown_policy.py:886` | `def append_step(self, step)` |
| `assess_probability` | method | `skills/lazyown_policy.py:688` | `def assess_probability(self, command, args, category)` |
| `calculate` | method | `skills/lazyown_policy.py:740` | `def calculate(self, category, outcome)` |
| `calculate_with_detection` | method | `skills/lazyown_policy.py:755` | `def calculate_with_detection(self, category, outcome, command, args)` |
| `classify` | method | `skills/lazyown_policy.py:329` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:354` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:397` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:527` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:573` | `def classify(self, command, args, output, exit_code)` |
| `classify` | method | `skills/lazyown_policy.py:634` | `def classify(self, command, args, output, exit_code)` |
| `default` | method | `skills/lazyown_policy.py:82` | `def default(cls)` |
| `episode_summary` | method | `skills/lazyown_policy.py:1246` | `def episode_summary(self, target)` |
| `from_dict` | method | `skills/lazyown_policy.py:315` | `def from_dict(cls, d)` |
| `get_episode` | method | `skills/lazyown_policy.py:870` | `def get_episode(self, target)` |
| `get_episode` | method | `skills/lazyown_policy.py:922` | `def get_episode(self, target)` |
| `get_recommendations` | method | `skills/lazyown_policy.py:1291` | `def get_recommendations(self, target)` |
| `infer_category` | method | `skills/lazyown_policy.py:220` | `def infer_category(command, args)` |
| `is_approved` | method | `skills/lazyown_policy.py:1338` | `def is_approved(self)` |
| `is_denied` | method | `skills/lazyown_policy.py:1343` | `def is_denied(self)` |
| `is_high_risk` | method | `skills/lazyown_policy.py:701` | `def is_high_risk(self, command, args, category)` |
| `load_all` | method | `skills/lazyown_policy.py:866` | `def load_all(self)` |
| `load_all` | method | `skills/lazyown_policy.py:906` | `def load_all(self)` |
| `main` | method | `skills/lazyown_policy.py:2019` | `def main()` |
| `ollama_url` | method | `skills/lazyown_policy.py:123` | `def ollama_url(self)` |
| `on_command_complete` | method | `skills/lazyown_policy.py:1280` | `def on_command_complete(self, target, command, args, output, exit_code)` |
| `path` | method | `skills/lazyown_policy.py:1378` | `def path(self)` |
| `process` | method | `skills/lazyown_policy.py:1179` | `def process(self, target, command, args, output, exit_code, timestamp)` |
| `query` | method | `skills/lazyown_policy.py:962` | `def query(self, from_state)` |
| `read` | method | `skills/lazyown_policy.py:814` | `def read(self)` |
| `recommend` | method | `skills/lazyown_policy.py:1070` | `def recommend(self, recent_steps)` |
| `record` | method | `skills/lazyown_policy.py:952` | `def record(self, from_state, to_category, outcome)` |
| `request` | method | `skills/lazyown_policy.py:1641` | `def request(self, target, phase, command, reason)` |
| `request` | method | `skills/lazyown_policy.py:1839` | `def request(self, target, phase, command, reason)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1361` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1399` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1474` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1530` | `def resolution_for(self, approval_id)` |
| `resolution_for` | method | `skills/lazyown_policy.py:1554` | `def resolution_for(self, approval_id)` |
| `run` | method | `skills/lazyown_policy.py:1909` | `def run(self)` |
| `to_dict` | method | `skills/lazyown_policy.py:310` | `def to_dict(self)` |
| `unknown` | method | `skills/lazyown_policy.py:270` | `def unknown(cls, tier)` |
| `SessionTranscript` | class | `skills/lazyown_session.py:56` | `class SessionTranscript` |
| `__init__` | method | `skills/lazyown_session.py:67` | `def __init__(self, sessions_dir, session_id)` |
| `_init_meta` | method | `skills/lazyown_session.py:75` | `def _init_meta(self)` |
| `_redact_sensitive` | function | `skills/lazyown_session.py:32` | `def _redact_sensitive(value)` |
| `add_compact_boundary` | method | `skills/lazyown_session.py:193` | `def add_compact_boundary(self, summary, preserved_uuids)` |
| `append` | method | `skills/lazyown_session.py:91` | `def append(self, event_type, data)` |
| `count` | method | `skills/lazyown_session.py:149` | `def count(self)` |
| `fork` | method | `skills/lazyown_session.py:209` | `def fork(self, new_id)` |
| `get_all` | method | `skills/lazyown_session.py:146` | `def get_all(self)` |
| `get_recent` | method | `skills/lazyown_session.py:128` | `def get_recent(self, n)` |
| `get_transcript` | method | `skills/lazyown_session.py:259` | `def get_transcript(sessions_dir, session_id)` |
| `maybe_auto_compact` | method | `skills/lazyown_session.py:159` | `def maybe_auto_compact(self, threshold)` |
| `reset_transcript` | method | `skills/lazyown_session.py:273` | `def reset_transcript(sessions_dir, session_id)` |
| `status_text` | method | `skills/lazyown_session.py:236` | `def status_text(self)` |
| `_gen_EOF` | function | `skills/mcp_generated_tools.py:694` | `def _gen_EOF(arguments, tool_name, _cmd)` |
| `_gen_GET` | function | `skills/mcp_generated_tools.py:702` | `def _gen_GET(arguments, tool_name, _cmd)` |
| `_gen_OPTIONS` | function | `skills/mcp_generated_tools.py:710` | `def _gen_OPTIONS(arguments, tool_name, _cmd)` |
| `_gen_POST` | function | `skills/mcp_generated_tools.py:718` | `def _gen_POST(arguments, tool_name, _cmd)` |
| `_gen_acknowledgearp` | function | `skills/mcp_generated_tools.py:726` | `def _gen_acknowledgearp(arguments, tool_name, _cmd)` |
| `_gen_acknowledgeicmp` | function | `skills/mcp_generated_tools.py:734` | `def _gen_acknowledgeicmp(arguments, tool_name, _cmd)` |
| `_gen_aclpwn_py` | function | `skills/mcp_generated_tools.py:742` | `def _gen_aclpwn_py(arguments, tool_name, _cmd)` |
| `_gen_ad_ldap_enum` | function | `skills/mcp_generated_tools.py:750` | `def _gen_ad_ldap_enum(arguments, tool_name, _cmd)` |
| `_gen_adcs_check` | function | `skills/mcp_generated_tools.py:758` | `def _gen_adcs_check(arguments, tool_name, _cmd)` |
| `_gen_add2find` | function | `skills/mcp_generated_tools.py:766` | `def _gen_add2find(arguments, tool_name, _cmd)` |
| `_gen_addalias` | function | `skills/mcp_generated_tools.py:774` | `def _gen_addalias(arguments, tool_name, _cmd)` |
| `_gen_addcli` | function | `skills/mcp_generated_tools.py:782` | `def _gen_addcli(arguments, tool_name, _cmd)` |
| `_gen_addhosts` | function | `skills/mcp_generated_tools.py:790` | `def _gen_addhosts(arguments, tool_name, _cmd)` |
| `_gen_addspn_py` | function | `skills/mcp_generated_tools.py:798` | `def _gen_addspn_py(arguments, tool_name, _cmd)` |
| `_gen_addusers` | function | `skills/mcp_generated_tools.py:806` | `def _gen_addusers(arguments, tool_name, _cmd)` |
| `_gen_adgetpass` | function | `skills/mcp_generated_tools.py:814` | `def _gen_adgetpass(arguments, tool_name, _cmd)` |
| `_gen_adsso_spray` | function | `skills/mcp_generated_tools.py:822` | `def _gen_adsso_spray(arguments, tool_name, _cmd)` |
| `_gen_adversary` | function | `skills/mcp_generated_tools.py:830` | `def _gen_adversary(arguments, tool_name, _cmd)` |
| `_gen_adversary_yaml` | function | `skills/mcp_generated_tools.py:838` | `def _gen_adversary_yaml(arguments, tool_name, _cmd)` |
| `_gen_aes_pe` | function | `skills/mcp_generated_tools.py:846` | `def _gen_aes_pe(arguments, tool_name, _cmd)` |
| `_gen_ai_playbook` | function | `skills/mcp_generated_tools.py:854` | `def _gen_ai_playbook(arguments, tool_name, _cmd)` |
| `_gen_ai_toggle` | function | `skills/mcp_generated_tools.py:862` | `def _gen_ai_toggle(arguments, tool_name, _cmd)` |
| `_gen_aliass` | function | `skills/mcp_generated_tools.py:870` | `def _gen_aliass(arguments, tool_name, _cmd)` |
| `_gen_allin` | function | `skills/mcp_generated_tools.py:878` | `def _gen_allin(arguments, tool_name, _cmd)` |
| `_gen_alterx` | function | `skills/mcp_generated_tools.py:886` | `def _gen_alterx(arguments, tool_name, _cmd)` |
| `_gen_amass` | function | `skills/mcp_generated_tools.py:894` | `def _gen_amass(arguments, tool_name, _cmd)` |
| `_gen_android_apk` | function | `skills/mcp_generated_tools.py:902` | `def _gen_android_apk(arguments, tool_name, _cmd)` |
| `_gen_android_enum` | function | `skills/mcp_generated_tools.py:910` | `def _gen_android_enum(arguments, tool_name, _cmd)` |
| `_gen_apache_users` | function | `skills/mcp_generated_tools.py:918` | `def _gen_apache_users(arguments, tool_name, _cmd)` |
| `_gen_applocker_csc` | function | `skills/mcp_generated_tools.py:926` | `def _gen_applocker_csc(arguments, tool_name, _cmd)` |
| `_gen_applocker_installutil` | function | `skills/mcp_generated_tools.py:934` | `def _gen_applocker_installutil(arguments, tool_name, _cmd)` |
| `_gen_applocker_msbuild` | function | `skills/mcp_generated_tools.py:942` | `def _gen_applocker_msbuild(arguments, tool_name, _cmd)` |
| `_gen_applocker_mshta` | function | `skills/mcp_generated_tools.py:950` | `def _gen_applocker_mshta(arguments, tool_name, _cmd)` |
| `_gen_applocker_presentation` | function | `skills/mcp_generated_tools.py:958` | `def _gen_applocker_presentation(arguments, tool_name, _cmd)` |
| `_gen_applocker_regsvcs` | function | `skills/mcp_generated_tools.py:966` | `def _gen_applocker_regsvcs(arguments, tool_name, _cmd)` |
| `_gen_applocker_rundll32` | function | `skills/mcp_generated_tools.py:974` | `def _gen_applocker_rundll32(arguments, tool_name, _cmd)` |
| `_gen_apropos` | function | `skills/mcp_generated_tools.py:982` | `def _gen_apropos(arguments, tool_name, _cmd)` |
| `_gen_apt_playbook` | function | `skills/mcp_generated_tools.py:990` | `def _gen_apt_playbook(arguments, tool_name, _cmd)` |
| `_gen_apt_proxy` | function | `skills/mcp_generated_tools.py:998` | `def _gen_apt_proxy(arguments, tool_name, _cmd)` |
| `_gen_apt_repo` | function | `skills/mcp_generated_tools.py:1006` | `def _gen_apt_repo(arguments, tool_name, _cmd)` |
| `_gen_arjun` | function | `skills/mcp_generated_tools.py:1014` | `def _gen_arjun(arguments, tool_name, _cmd)` |
| `_gen_arpscan` | function | `skills/mcp_generated_tools.py:1022` | `def _gen_arpscan(arguments, tool_name, _cmd)` |
| `_gen_ask` | function | `skills/mcp_generated_tools.py:1030` | `def _gen_ask(arguments, tool_name, _cmd)` |
| `_gen_asprevbase64` | function | `skills/mcp_generated_tools.py:1038` | `def _gen_asprevbase64(arguments, tool_name, _cmd)` |
| `_gen_assign` | function | `skills/mcp_generated_tools.py:1046` | `def _gen_assign(arguments, tool_name, _cmd)` |
| `_gen_atomic_agent` | function | `skills/mcp_generated_tools.py:1054` | `def _gen_atomic_agent(arguments, tool_name, _cmd)` |
| `_gen_atomic_gen` | function | `skills/mcp_generated_tools.py:1062` | `def _gen_atomic_gen(arguments, tool_name, _cmd)` |
| `_gen_atomic_lazyown` | function | `skills/mcp_generated_tools.py:1070` | `def _gen_atomic_lazyown(arguments, tool_name, _cmd)` |
| `_gen_atomic_tests` | function | `skills/mcp_generated_tools.py:1078` | `def _gen_atomic_tests(arguments, tool_name, _cmd)` |
| `_gen_attack_plan` | function | `skills/mcp_generated_tools.py:1086` | `def _gen_attack_plan(arguments, tool_name, _cmd)` |
| `_gen_attack_surface` | function | `skills/mcp_generated_tools.py:1094` | `def _gen_attack_surface(arguments, tool_name, _cmd)` |
| `_gen_audit_complete_keys` | function | `skills/mcp_generated_tools.py:1102` | `def _gen_audit_complete_keys(arguments, tool_name, _cmd)` |
| `_gen_autoblody` | function | `skills/mcp_generated_tools.py:1110` | `def _gen_autoblody(arguments, tool_name, _cmd)` |
| `_gen_automsf` | function | `skills/mcp_generated_tools.py:1118` | `def _gen_automsf(arguments, tool_name, _cmd)` |
| `_gen_autopivot` | function | `skills/mcp_generated_tools.py:1126` | `def _gen_autopivot(arguments, tool_name, _cmd)` |
| `_gen_back` | function | `skills/mcp_generated_tools.py:1134` | `def _gen_back(arguments, tool_name, _cmd)` |
| `_gen_backdoor_factory` | function | `skills/mcp_generated_tools.py:1142` | `def _gen_backdoor_factory(arguments, tool_name, _cmd)` |
| `_gen_banner` | function | `skills/mcp_generated_tools.py:1150` | `def _gen_banner(arguments, tool_name, _cmd)` |
| `_gen_banners` | function | `skills/mcp_generated_tools.py:1158` | `def _gen_banners(arguments, tool_name, _cmd)` |
| `_gen_base64decode` | function | `skills/mcp_generated_tools.py:1166` | `def _gen_base64decode(arguments, tool_name, _cmd)` |
| `_gen_base64encode` | function | `skills/mcp_generated_tools.py:1174` | `def _gen_base64encode(arguments, tool_name, _cmd)` |
| `_gen_batchnmap` | function | `skills/mcp_generated_tools.py:1182` | `def _gen_batchnmap(arguments, tool_name, _cmd)` |
| `_gen_bbot` | function | `skills/mcp_generated_tools.py:1190` | `def _gen_bbot(arguments, tool_name, _cmd)` |
| `_gen_beaconcfg` | function | `skills/mcp_generated_tools.py:1198` | `def _gen_beaconcfg(arguments, tool_name, _cmd)` |
| `_gen_bin2shellcode` | function | `skills/mcp_generated_tools.py:1206` | `def _gen_bin2shellcode(arguments, tool_name, _cmd)` |
| `_gen_binarycheck` | function | `skills/mcp_generated_tools.py:1214` | `def _gen_binarycheck(arguments, tool_name, _cmd)` |
| `_gen_bitm` | function | `skills/mcp_generated_tools.py:1222` | `def _gen_bitm(arguments, tool_name, _cmd)` |
| `_gen_blazy` | function | `skills/mcp_generated_tools.py:1230` | `def _gen_blazy(arguments, tool_name, _cmd)` |
| `_gen_bloodhound` | function | `skills/mcp_generated_tools.py:1238` | `def _gen_bloodhound(arguments, tool_name, _cmd)` |
| `_gen_bloodyAD` | function | `skills/mcp_generated_tools.py:1246` | `def _gen_bloodyAD(arguments, tool_name, _cmd)` |
| `_gen_breacher` | function | `skills/mcp_generated_tools.py:1254` | `def _gen_breacher(arguments, tool_name, _cmd)` |
| `_gen_browse` | function | `skills/mcp_generated_tools.py:1262` | `def _gen_browse(arguments, tool_name, _cmd)` |
| `_gen_c2` | function | `skills/mcp_generated_tools.py:1270` | `def _gen_c2(arguments, tool_name, _cmd)` |
| `_gen_c2_beacon_cmd` | function | `skills/mcp_generated_tools.py:1278` | `def _gen_c2_beacon_cmd(arguments, tool_name, _cmd)` |
| `_gen_c2_beacons` | function | `skills/mcp_generated_tools.py:1286` | `def _gen_c2_beacons(arguments, tool_name, _cmd)` |
| `_gen_c2_implant` | function | `skills/mcp_generated_tools.py:1294` | `def _gen_c2_implant(arguments, tool_name, _cmd)` |
| `_gen_c2_keygen` | function | `skills/mcp_generated_tools.py:1302` | `def _gen_c2_keygen(arguments, tool_name, _cmd)` |
| `_gen_c2_quickstart` | function | `skills/mcp_generated_tools.py:1310` | `def _gen_c2_quickstart(arguments, tool_name, _cmd)` |
| `_gen_c2asm` | function | `skills/mcp_generated_tools.py:1318` | `def _gen_c2asm(arguments, tool_name, _cmd)` |
| `_gen_cacti_exploit` | function | `skills/mcp_generated_tools.py:1326` | `def _gen_cacti_exploit(arguments, tool_name, _cmd)` |
| `_gen_caldera` | function | `skills/mcp_generated_tools.py:1334` | `def _gen_caldera(arguments, tool_name, _cmd)` |
| `_gen_caldera_export` | function | `skills/mcp_generated_tools.py:1342` | `def _gen_caldera_export(arguments, tool_name, _cmd)` |
| `_gen_caldera_import` | function | `skills/mcp_generated_tools.py:1350` | `def _gen_caldera_import(arguments, tool_name, _cmd)` |
| `_gen_camphish` | function | `skills/mcp_generated_tools.py:1358` | `def _gen_camphish(arguments, tool_name, _cmd)` |
| `_gen_certipy` | function | `skills/mcp_generated_tools.py:1366` | `def _gen_certipy(arguments, tool_name, _cmd)` |
| `_gen_certipy_ad` | function | `skills/mcp_generated_tools.py:1374` | `def _gen_certipy_ad(arguments, tool_name, _cmd)` |
| `_gen_cewl` | function | `skills/mcp_generated_tools.py:1382` | `def _gen_cewl(arguments, tool_name, _cmd)` |
| `_gen_chain` | function | `skills/mcp_generated_tools.py:1390` | `def _gen_chain(arguments, tool_name, _cmd)` |
| `_gen_changeme` | function | `skills/mcp_generated_tools.py:1398` | `def _gen_changeme(arguments, tool_name, _cmd)` |
| `_gen_check_update` | function | `skills/mcp_generated_tools.py:1406` | `def _gen_check_update(arguments, tool_name, _cmd)` |
| `_gen_chisel` | function | `skills/mcp_generated_tools.py:1414` | `def _gen_chisel(arguments, tool_name, _cmd)` |
| `_gen_cicd_scan` | function | `skills/mcp_generated_tools.py:1422` | `def _gen_cicd_scan(arguments, tool_name, _cmd)` |
| `_gen_cicd_secrets` | function | `skills/mcp_generated_tools.py:1430` | `def _gen_cicd_secrets(arguments, tool_name, _cmd)` |
| `_gen_clean` | function | `skills/mcp_generated_tools.py:1438` | `def _gen_clean(arguments, tool_name, _cmd)` |
| `_gen_clean_ad` | function | `skills/mcp_generated_tools.py:1446` | `def _gen_clean_ad(arguments, tool_name, _cmd)` |
| `_gen_clock` | function | `skills/mcp_generated_tools.py:1454` | `def _gen_clock(arguments, tool_name, _cmd)` |
| `_gen_clone_site` | function | `skills/mcp_generated_tools.py:1462` | `def _gen_clone_site(arguments, tool_name, _cmd)` |
| `_gen_cloud_buckets` | function | `skills/mcp_generated_tools.py:1470` | `def _gen_cloud_buckets(arguments, tool_name, _cmd)` |
| `_gen_cloud_enum` | function | `skills/mcp_generated_tools.py:1478` | `def _gen_cloud_enum(arguments, tool_name, _cmd)` |
| `_gen_cloud_iam` | function | `skills/mcp_generated_tools.py:1486` | `def _gen_cloud_iam(arguments, tool_name, _cmd)` |
| `_gen_cloud_metadata` | function | `skills/mcp_generated_tools.py:1494` | `def _gen_cloud_metadata(arguments, tool_name, _cmd)` |
| `_gen_cloud_scan` | function | `skills/mcp_generated_tools.py:1502` | `def _gen_cloud_scan(arguments, tool_name, _cmd)` |
| `_gen_cme` | function | `skills/mcp_generated_tools.py:1510` | `def _gen_cme(arguments, tool_name, _cmd)` |
| `_gen_collab_join` | function | `skills/mcp_generated_tools.py:1518` | `def _gen_collab_join(arguments, tool_name, _cmd)` |
| `_gen_commix` | function | `skills/mcp_generated_tools.py:1526` | `def _gen_commix(arguments, tool_name, _cmd)` |
| `_gen_config_banner` | function | `skills/mcp_generated_tools.py:1534` | `def _gen_config_banner(arguments, tool_name, _cmd)` |
| `_gen_conptyshell` | function | `skills/mcp_generated_tools.py:1542` | `def _gen_conptyshell(arguments, tool_name, _cmd)` |
| `_gen_container_detect` | function | `skills/mcp_generated_tools.py:1550` | `def _gen_container_detect(arguments, tool_name, _cmd)` |
| `_gen_container_escape` | function | `skills/mcp_generated_tools.py:1558` | `def _gen_container_escape(arguments, tool_name, _cmd)` |
| `_gen_convert_remcomsvc_from_file` | function | `skills/mcp_generated_tools.py:1566` | `def _gen_convert_remcomsvc_from_file(arguments, tool_name, _cmd)` |
| `_gen_cover_tracks` | function | `skills/mcp_generated_tools.py:1574` | `def _gen_cover_tracks(arguments, tool_name, _cmd)` |
| `_gen_cp` | function | `skills/mcp_generated_tools.py:1582` | `def _gen_cp(arguments, tool_name, _cmd)` |
| `_gen_cports` | function | `skills/mcp_generated_tools.py:1590` | `def _gen_cports(arguments, tool_name, _cmd)` |
| `_gen_crack_cisco_7_password` | function | `skills/mcp_generated_tools.py:1598` | `def _gen_crack_cisco_7_password(arguments, tool_name, _cmd)` |
| `_gen_crack_hashes` | function | `skills/mcp_generated_tools.py:1606` | `def _gen_crack_hashes(arguments, tool_name, _cmd)` |
| `_gen_create_session_json` | function | `skills/mcp_generated_tools.py:1614` | `def _gen_create_session_json(arguments, tool_name, _cmd)` |
| `_gen_create_synthetic` | function | `skills/mcp_generated_tools.py:1622` | `def _gen_create_synthetic(arguments, tool_name, _cmd)` |
| `_gen_createcookie` | function | `skills/mcp_generated_tools.py:1630` | `def _gen_createcookie(arguments, tool_name, _cmd)` |
| `_gen_createcredentials` | function | `skills/mcp_generated_tools.py:1638` | `def _gen_createcredentials(arguments, tool_name, _cmd)` |
| `_gen_createdll` | function | `skills/mcp_generated_tools.py:1646` | `def _gen_createdll(arguments, tool_name, _cmd)` |
| `_gen_createhash` | function | `skills/mcp_generated_tools.py:1654` | `def _gen_createhash(arguments, tool_name, _cmd)` |
| `_gen_createjsonmachine` | function | `skills/mcp_generated_tools.py:1662` | `def _gen_createjsonmachine(arguments, tool_name, _cmd)` |
| `_gen_createjsonmachine_batch` | function | `skills/mcp_generated_tools.py:1670` | `def _gen_createjsonmachine_batch(arguments, tool_name, _cmd)` |
| `_gen_createmail` | function | `skills/mcp_generated_tools.py:1678` | `def _gen_createmail(arguments, tool_name, _cmd)` |
| `_gen_createpayload` | function | `skills/mcp_generated_tools.py:1686` | `def _gen_createpayload(arguments, tool_name, _cmd)` |
| `_gen_createrevshell` | function | `skills/mcp_generated_tools.py:1694` | `def _gen_createrevshell(arguments, tool_name, _cmd)` |
| `_gen_createtargets` | function | `skills/mcp_generated_tools.py:1702` | `def _gen_createtargets(arguments, tool_name, _cmd)` |
| `_gen_createusers_and_hashs` | function | `skills/mcp_generated_tools.py:1710` | `def _gen_createusers_and_hashs(arguments, tool_name, _cmd)` |
| `_gen_createwebshell` | function | `skills/mcp_generated_tools.py:1718` | `def _gen_createwebshell(arguments, tool_name, _cmd)` |
| `_gen_createwinrevshell` | function | `skills/mcp_generated_tools.py:1726` | `def _gen_createwinrevshell(arguments, tool_name, _cmd)` |
| `_gen_cred` | function | `skills/mcp_generated_tools.py:1734` | `def _gen_cred(arguments, tool_name, _cmd)` |
| `_gen_cred_mark_failed` | function | `skills/mcp_generated_tools.py:1742` | `def _gen_cred_mark_failed(arguments, tool_name, _cmd)` |
| `_gen_cred_reuse` | function | `skills/mcp_generated_tools.py:1750` | `def _gen_cred_reuse(arguments, tool_name, _cmd)` |
| `_gen_creds_py` | function | `skills/mcp_generated_tools.py:1758` | `def _gen_creds_py(arguments, tool_name, _cmd)` |
| `_gen_cron` | function | `skills/mcp_generated_tools.py:1766` | `def _gen_cron(arguments, tool_name, _cmd)` |
| `_gen_crunch` | function | `skills/mcp_generated_tools.py:1774` | `def _gen_crunch(arguments, tool_name, _cmd)` |
| `_gen_crystal_ball` | function | `skills/mcp_generated_tools.py:1782` | `def _gen_crystal_ball(arguments, tool_name, _cmd)` |
| `_gen_ctx` | function | `skills/mcp_generated_tools.py:1790` | `def _gen_ctx(arguments, tool_name, _cmd)` |
| `_gen_cubespraying` | function | `skills/mcp_generated_tools.py:1798` | `def _gen_cubespraying(arguments, tool_name, _cmd)` |
| `_gen_cve` | function | `skills/mcp_generated_tools.py:1806` | `def _gen_cve(arguments, tool_name, _cmd)` |
| `_gen_d3monizedshell` | function | `skills/mcp_generated_tools.py:1814` | `def _gen_d3monizedshell(arguments, tool_name, _cmd)` |
| `_gen_dacledit` | function | `skills/mcp_generated_tools.py:1822` | `def _gen_dacledit(arguments, tool_name, _cmd)` |
| `_gen_darkarmour` | function | `skills/mcp_generated_tools.py:1830` | `def _gen_darkarmour(arguments, tool_name, _cmd)` |
| `_gen_dashboard` | function | `skills/mcp_generated_tools.py:1838` | `def _gen_dashboard(arguments, tool_name, _cmd)` |
| `_gen_davtest` | function | `skills/mcp_generated_tools.py:1846` | `def _gen_davtest(arguments, tool_name, _cmd)` |
| `_gen_db_creds` | function | `skills/mcp_generated_tools.py:1854` | `def _gen_db_creds(arguments, tool_name, _cmd)` |
| `_gen_db_export` | function | `skills/mcp_generated_tools.py:1862` | `def _gen_db_export(arguments, tool_name, _cmd)` |
| `_gen_db_hosts` | function | `skills/mcp_generated_tools.py:1870` | `def _gen_db_hosts(arguments, tool_name, _cmd)` |
| `_gen_db_import` | function | `skills/mcp_generated_tools.py:1878` | `def _gen_db_import(arguments, tool_name, _cmd)` |
| `_gen_db_init` | function | `skills/mcp_generated_tools.py:1886` | `def _gen_db_init(arguments, tool_name, _cmd)` |
| `_gen_db_loot` | function | `skills/mcp_generated_tools.py:1894` | `def _gen_db_loot(arguments, tool_name, _cmd)` |
| `_gen_db_notes` | function | `skills/mcp_generated_tools.py:1902` | `def _gen_db_notes(arguments, tool_name, _cmd)` |
| `_gen_db_services` | function | `skills/mcp_generated_tools.py:1910` | `def _gen_db_services(arguments, tool_name, _cmd)` |
| `_gen_db_status` | function | `skills/mcp_generated_tools.py:1918` | `def _gen_db_status(arguments, tool_name, _cmd)` |
| `_gen_db_vulns` | function | `skills/mcp_generated_tools.py:1926` | `def _gen_db_vulns(arguments, tool_name, _cmd)` |
| `_gen_db_workspace` | function | `skills/mcp_generated_tools.py:1934` | `def _gen_db_workspace(arguments, tool_name, _cmd)` |
| `_gen_dcomexec` | function | `skills/mcp_generated_tools.py:1942` | `def _gen_dcomexec(arguments, tool_name, _cmd)` |
| `_gen_decode` | function | `skills/mcp_generated_tools.py:1950` | `def _gen_decode(arguments, tool_name, _cmd)` |
| `_gen_decrypt` | function | `skills/mcp_generated_tools.py:1958` | `def _gen_decrypt(arguments, tool_name, _cmd)` |
| `_gen_depconfuse` | function | `skills/mcp_generated_tools.py:1966` | `def _gen_depconfuse(arguments, tool_name, _cmd)` |
| `_gen_depscan` | function | `skills/mcp_generated_tools.py:1974` | `def _gen_depscan(arguments, tool_name, _cmd)` |
| `_gen_detect_edr` | function | `skills/mcp_generated_tools.py:1982` | `def _gen_detect_edr(arguments, tool_name, _cmd)` |
| `_gen_dig` | function | `skills/mcp_generated_tools.py:1990` | `def _gen_dig(arguments, tool_name, _cmd)` |
| `_gen_digdug` | function | `skills/mcp_generated_tools.py:1998` | `def _gen_digdug(arguments, tool_name, _cmd)` |
| `_gen_dirsearch` | function | `skills/mcp_generated_tools.py:2006` | `def _gen_dirsearch(arguments, tool_name, _cmd)` |
| `_gen_disableav` | function | `skills/mcp_generated_tools.py:2014` | `def _gen_disableav(arguments, tool_name, _cmd)` |
| `_gen_dmitry` | function | `skills/mcp_generated_tools.py:2022` | `def _gen_dmitry(arguments, tool_name, _cmd)` |
| `_gen_dns_beacon` | function | `skills/mcp_generated_tools.py:2030` | `def _gen_dns_beacon(arguments, tool_name, _cmd)` |
| `_gen_dns_beacon_status` | function | `skills/mcp_generated_tools.py:2038` | `def _gen_dns_beacon_status(arguments, tool_name, _cmd)` |
| `_gen_dns_exfil_listen` | function | `skills/mcp_generated_tools.py:2046` | `def _gen_dns_exfil_listen(arguments, tool_name, _cmd)` |
| `_gen_dnschef` | function | `skills/mcp_generated_tools.py:2054` | `def _gen_dnschef(arguments, tool_name, _cmd)` |
| `_gen_dnsenum` | function | `skills/mcp_generated_tools.py:2062` | `def _gen_dnsenum(arguments, tool_name, _cmd)` |
| `_gen_dnsmap` | function | `skills/mcp_generated_tools.py:2070` | `def _gen_dnsmap(arguments, tool_name, _cmd)` |
| `_gen_dnstool_py` | function | `skills/mcp_generated_tools.py:2078` | `def _gen_dnstool_py(arguments, tool_name, _cmd)` |
| `_gen_docker_enum` | function | `skills/mcp_generated_tools.py:2086` | `def _gen_docker_enum(arguments, tool_name, _cmd)` |
| `_gen_doctor` | function | `skills/mcp_generated_tools.py:2094` | `def _gen_doctor(arguments, tool_name, _cmd)` |
| `_gen_dominion` | function | `skills/mcp_generated_tools.py:2102` | `def _gen_dominion(arguments, tool_name, _cmd)` |
| `_gen_download_c2` | function | `skills/mcp_generated_tools.py:2110` | `def _gen_download_c2(arguments, tool_name, _cmd)` |
| `_gen_download_exploit` | function | `skills/mcp_generated_tools.py:2118` | `def _gen_download_exploit(arguments, tool_name, _cmd)` |
| `_gen_download_malwarebazar` | function | `skills/mcp_generated_tools.py:2126` | `def _gen_download_malwarebazar(arguments, tool_name, _cmd)` |
| `_gen_download_resources` | function | `skills/mcp_generated_tools.py:2134` | `def _gen_download_resources(arguments, tool_name, _cmd)` |
| `_gen_downloader` | function | `skills/mcp_generated_tools.py:2142` | `def _gen_downloader(arguments, tool_name, _cmd)` |
| `_gen_dpapi_blob` | function | `skills/mcp_generated_tools.py:2150` | `def _gen_dpapi_blob(arguments, tool_name, _cmd)` |
| `_gen_dpapi_harvest` | function | `skills/mcp_generated_tools.py:2158` | `def _gen_dpapi_harvest(arguments, tool_name, _cmd)` |
| `_gen_dpapi_masterkeys` | function | `skills/mcp_generated_tools.py:2166` | `def _gen_dpapi_masterkeys(arguments, tool_name, _cmd)` |
| `_gen_dploot` | function | `skills/mcp_generated_tools.py:2174` | `def _gen_dploot(arguments, tool_name, _cmd)` |
| `_gen_dr0p1t` | function | `skills/mcp_generated_tools.py:2182` | `def _gen_dr0p1t(arguments, tool_name, _cmd)` |
| `_gen_duckyspark` | function | `skills/mcp_generated_tools.py:2190` | `def _gen_duckyspark(arguments, tool_name, _cmd)` |
| `_gen_edr_detect` | function | `skills/mcp_generated_tools.py:2198` | `def _gen_edr_detect(arguments, tool_name, _cmd)` |
| `_gen_edr_profile` | function | `skills/mcp_generated_tools.py:2206` | `def _gen_edr_profile(arguments, tool_name, _cmd)` |
| `_gen_edr_script` | function | `skills/mcp_generated_tools.py:2214` | `def _gen_edr_script(arguments, tool_name, _cmd)` |
| `_gen_emp3r0r` | function | `skills/mcp_generated_tools.py:2222` | `def _gen_emp3r0r(arguments, tool_name, _cmd)` |
| `_gen_empire` | function | `skills/mcp_generated_tools.py:2230` | `def _gen_empire(arguments, tool_name, _cmd)` |
| `_gen_encode` | function | `skills/mcp_generated_tools.py:2238` | `def _gen_encode(arguments, tool_name, _cmd)` |
| `_gen_encoderpayload` | function | `skills/mcp_generated_tools.py:2246` | `def _gen_encoderpayload(arguments, tool_name, _cmd)` |
| `_gen_encodewinbase64` | function | `skills/mcp_generated_tools.py:2254` | `def _gen_encodewinbase64(arguments, tool_name, _cmd)` |
| `_gen_encrypt` | function | `skills/mcp_generated_tools.py:2262` | `def _gen_encrypt(arguments, tool_name, _cmd)` |
| `_gen_engage` | function | `skills/mcp_generated_tools.py:2270` | `def _gen_engage(arguments, tool_name, _cmd)` |
| `_gen_enum4linux` | function | `skills/mcp_generated_tools.py:2278` | `def _gen_enum4linux(arguments, tool_name, _cmd)` |
| `_gen_enum4linux_ng` | function | `skills/mcp_generated_tools.py:2286` | `def _gen_enum4linux_ng(arguments, tool_name, _cmd)` |
| `_gen_eternal` | function | `skills/mcp_generated_tools.py:2294` | `def _gen_eternal(arguments, tool_name, _cmd)` |
| `_gen_evasion` | function | `skills/mcp_generated_tools.py:2302` | `def _gen_evasion(arguments, tool_name, _cmd)` |
| `_gen_evasive` | function | `skills/mcp_generated_tools.py:2310` | `def _gen_evasive(arguments, tool_name, _cmd)` |
| `_gen_evasive_payload` | function | `skills/mcp_generated_tools.py:2318` | `def _gen_evasive_payload(arguments, tool_name, _cmd)` |
| `_gen_event_log` | function | `skills/mcp_generated_tools.py:2326` | `def _gen_event_log(arguments, tool_name, _cmd)` |
| `_gen_evidence` | function | `skills/mcp_generated_tools.py:2334` | `def _gen_evidence(arguments, tool_name, _cmd)` |
| `_gen_evil_ssdp` | function | `skills/mcp_generated_tools.py:2342` | `def _gen_evil_ssdp(arguments, tool_name, _cmd)` |
| `_gen_evilwinrm` | function | `skills/mcp_generated_tools.py:2350` | `def _gen_evilwinrm(arguments, tool_name, _cmd)` |
| `_gen_excelntdonut` | function | `skills/mcp_generated_tools.py:2358` | `def _gen_excelntdonut(arguments, tool_name, _cmd)` |
| `_gen_exe2bin` | function | `skills/mcp_generated_tools.py:2366` | `def _gen_exe2bin(arguments, tool_name, _cmd)` |
| `_gen_exe2donutbin` | function | `skills/mcp_generated_tools.py:2374` | `def _gen_exe2donutbin(arguments, tool_name, _cmd)` |
| `_gen_exfil_auto` | function | `skills/mcp_generated_tools.py:2382` | `def _gen_exfil_auto(arguments, tool_name, _cmd)` |
| `_gen_exfil_discord` | function | `skills/mcp_generated_tools.py:2390` | `def _gen_exfil_discord(arguments, tool_name, _cmd)` |
| `_gen_exfil_dns` | function | `skills/mcp_generated_tools.py:2398` | `def _gen_exfil_dns(arguments, tool_name, _cmd)` |
| `_gen_exfil_gcs` | function | `skills/mcp_generated_tools.py:2406` | `def _gen_exfil_gcs(arguments, tool_name, _cmd)` |
| `_gen_exfil_http` | function | `skills/mcp_generated_tools.py:2414` | `def _gen_exfil_http(arguments, tool_name, _cmd)` |
| `_gen_exfil_s3` | function | `skills/mcp_generated_tools.py:2422` | `def _gen_exfil_s3(arguments, tool_name, _cmd)` |
| `_gen_exfil_start_server` | function | `skills/mcp_generated_tools.py:2430` | `def _gen_exfil_start_server(arguments, tool_name, _cmd)` |
| `_gen_exfil_telegram` | function | `skills/mcp_generated_tools.py:2438` | `def _gen_exfil_telegram(arguments, tool_name, _cmd)` |
| `_gen_exit` | function | `skills/mcp_generated_tools.py:2446` | `def _gen_exit(arguments, tool_name, _cmd)` |
| `_gen_explore` | function | `skills/mcp_generated_tools.py:2454` | `def _gen_explore(arguments, tool_name, _cmd)` |
| `_gen_extract_ports` | function | `skills/mcp_generated_tools.py:2462` | `def _gen_extract_ports(arguments, tool_name, _cmd)` |
| `_gen_extract_yaml` | function | `skills/mcp_generated_tools.py:2470` | `def _gen_extract_yaml(arguments, tool_name, _cmd)` |
| `_gen_eyewitness` | function | `skills/mcp_generated_tools.py:2478` | `def _gen_eyewitness(arguments, tool_name, _cmd)` |
| `_gen_eyewitness_py` | function | `skills/mcp_generated_tools.py:2486` | `def _gen_eyewitness_py(arguments, tool_name, _cmd)` |
| `_gen_feroxbuster` | function | `skills/mcp_generated_tools.py:2494` | `def _gen_feroxbuster(arguments, tool_name, _cmd)` |
| `_gen_filtering` | function | `skills/mcp_generated_tools.py:2502` | `def _gen_filtering(arguments, tool_name, _cmd)` |
| `_gen_finalrecon` | function | `skills/mcp_generated_tools.py:2510` | `def _gen_finalrecon(arguments, tool_name, _cmd)` |
| `_gen_find` | function | `skills/mcp_generated_tools.py:2518` | `def _gen_find(arguments, tool_name, _cmd)` |
| `_gen_finger_user_enum` | function | `skills/mcp_generated_tools.py:2526` | `def _gen_finger_user_enum(arguments, tool_name, _cmd)` |
| `_gen_fixel` | function | `skills/mcp_generated_tools.py:2534` | `def _gen_fixel(arguments, tool_name, _cmd)` |
| `_gen_fixperm` | function | `skills/mcp_generated_tools.py:2542` | `def _gen_fixperm(arguments, tool_name, _cmd)` |
| `_gen_follina` | function | `skills/mcp_generated_tools.py:2550` | `def _gen_follina(arguments, tool_name, _cmd)` |
| `_gen_form` | function | `skills/mcp_generated_tools.py:2558` | `def _gen_form(arguments, tool_name, _cmd)` |
| `_gen_ftp` | function | `skills/mcp_generated_tools.py:2566` | `def _gen_ftp(arguments, tool_name, _cmd)` |
| `_gen_fuzz` | function | `skills/mcp_generated_tools.py:2574` | `def _gen_fuzz(arguments, tool_name, _cmd)` |
| `_gen_fz` | function | `skills/mcp_generated_tools.py:2582` | `def _gen_fz(arguments, tool_name, _cmd)` |
| `_gen_gencert` | function | `skills/mcp_generated_tools.py:2590` | `def _gen_gencert(arguments, tool_name, _cmd)` |
| `_gen_generate` | function | `skills/mcp_generated_tools.py:2598` | `def _gen_generate(arguments, tool_name, _cmd)` |
| `_gen_generate_playbook` | function | `skills/mcp_generated_tools.py:2606` | `def _gen_generate_playbook(arguments, tool_name, _cmd)` |
| `_gen_generate_revshell` | function | `skills/mcp_generated_tools.py:2614` | `def _gen_generate_revshell(arguments, tool_name, _cmd)` |
| `_gen_generatedic` | function | `skills/mcp_generated_tools.py:2622` | `def _gen_generatedic(arguments, tool_name, _cmd)` |
| `_gen_getTGT` | function | `skills/mcp_generated_tools.py:2630` | `def _gen_getTGT(arguments, tool_name, _cmd)` |
| `_gen_get_avaible_actions` | function | `skills/mcp_generated_tools.py:2638` | `def _gen_get_avaible_actions(arguments, tool_name, _cmd)` |
| `_gen_getadusers` | function | `skills/mcp_generated_tools.py:2646` | `def _gen_getadusers(arguments, tool_name, _cmd)` |
| `_gen_getcap` | function | `skills/mcp_generated_tools.py:2654` | `def _gen_getcap(arguments, tool_name, _cmd)` |
| `_gen_getnpusers` | function | `skills/mcp_generated_tools.py:2662` | `def _gen_getnpusers(arguments, tool_name, _cmd)` |
| `_gen_getnthash_py` | function | `skills/mcp_generated_tools.py:2670` | `def _gen_getnthash_py(arguments, tool_name, _cmd)` |
| `_gen_gets4uticket_py` | function | `skills/mcp_generated_tools.py:2678` | `def _gen_gets4uticket_py(arguments, tool_name, _cmd)` |
| `_gen_getseclist` | function | `skills/mcp_generated_tools.py:2686` | `def _gen_getseclist(arguments, tool_name, _cmd)` |
| `_gen_gettgtpkinit_py` | function | `skills/mcp_generated_tools.py:2694` | `def _gen_gettgtpkinit_py(arguments, tool_name, _cmd)` |
| `_gen_getuserspns` | function | `skills/mcp_generated_tools.py:2702` | `def _gen_getuserspns(arguments, tool_name, _cmd)` |
| `_gen_gitdumper` | function | `skills/mcp_generated_tools.py:2710` | `def _gen_gitdumper(arguments, tool_name, _cmd)` |
| `_gen_gitlab_enum` | function | `skills/mcp_generated_tools.py:2718` | `def _gen_gitlab_enum(arguments, tool_name, _cmd)` |
| `_gen_gmsadumper` | function | `skills/mcp_generated_tools.py:2726` | `def _gen_gmsadumper(arguments, tool_name, _cmd)` |
| `_gen_gobuster` | function | `skills/mcp_generated_tools.py:2734` | `def _gen_gobuster(arguments, tool_name, _cmd)` |
| `_gen_god_nodes` | function | `skills/mcp_generated_tools.py:2742` | `def _gen_god_nodes(arguments, tool_name, _cmd)` |
| `_gen_gospherus` | function | `skills/mcp_generated_tools.py:2750` | `def _gen_gospherus(arguments, tool_name, _cmd)` |
| `_gen_gospider` | function | `skills/mcp_generated_tools.py:2758` | `def _gen_gospider(arguments, tool_name, _cmd)` |
| `_gen_gowitness` | function | `skills/mcp_generated_tools.py:2766` | `def _gen_gowitness(arguments, tool_name, _cmd)` |
| `_gen_gpt` | function | `skills/mcp_generated_tools.py:2774` | `def _gen_gpt(arguments, tool_name, _cmd)` |
| `_gen_graph` | function | `skills/mcp_generated_tools.py:2782` | `def _gen_graph(arguments, tool_name, _cmd)` |
| `_gen_graph_overlay` | function | `skills/mcp_generated_tools.py:2790` | `def _gen_graph_overlay(arguments, tool_name, _cmd)` |
| `_gen_graudit` | function | `skills/mcp_generated_tools.py:2798` | `def _gen_graudit(arguments, tool_name, _cmd)` |
| `_gen_greatSCT` | function | `skills/mcp_generated_tools.py:2806` | `def _gen_greatSCT(arguments, tool_name, _cmd)` |
| `_gen_grep_log` | function | `skills/mcp_generated_tools.py:2814` | `def _gen_grep_log(arguments, tool_name, _cmd)` |
| `_gen_grisun0` | function | `skills/mcp_generated_tools.py:2822` | `def _gen_grisun0(arguments, tool_name, _cmd)` |
| `_gen_grisun0w` | function | `skills/mcp_generated_tools.py:2830` | `def _gen_grisun0w(arguments, tool_name, _cmd)` |
| `_gen_groq` | function | `skills/mcp_generated_tools.py:2838` | `def _gen_groq(arguments, tool_name, _cmd)` |
| `_gen_gtfo` | function | `skills/mcp_generated_tools.py:2846` | `def _gen_gtfo(arguments, tool_name, _cmd)` |
| `_gen_gym` | function | `skills/mcp_generated_tools.py:2854` | `def _gen_gym(arguments, tool_name, _cmd)` |
| `_gen_h` | function | `skills/mcp_generated_tools.py:2862` | `def _gen_h(arguments, tool_name, _cmd)` |
| `_gen_hashcat` | function | `skills/mcp_generated_tools.py:2870` | `def _gen_hashcat(arguments, tool_name, _cmd)` |
| `_gen_hex2shellcode` | function | `skills/mcp_generated_tools.py:2878` | `def _gen_hex2shellcode(arguments, tool_name, _cmd)` |
| `_gen_hex_to_plaintext` | function | `skills/mcp_generated_tools.py:2886` | `def _gen_hex_to_plaintext(arguments, tool_name, _cmd)` |
| `_gen_hooks` | function | `skills/mcp_generated_tools.py:2894` | `def _gen_hooks(arguments, tool_name, _cmd)` |

Next: [SYMBOLS_p21.md](SYMBOLS_p21.md)
