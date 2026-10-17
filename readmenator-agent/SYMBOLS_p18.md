# Symbols (page 18 of 42)
Previous: [SYMBOLS_p17.md](SYMBOLS_p17.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `has` | method | `modules/obs_parser.py:86` | `def has(self, ftype)` |
| `is_success` | method | `modules/obs_parser.py:407` | `def is_success(self, text)` |
| `parse` | method | `modules/obs_parser.py:454` | `def parse(self, output, host, tool)` |
| `parse` | function | `modules/obs_parser.py:508` | `def parse(output, host, tool)` |
| `register` | method | `modules/obs_parser.py:109` | `def register(self, extractor)` |
| `register` | method | `modules/obs_parser.py:450` | `def register(self, extractor)` |
| `run_all` | method | `modules/obs_parser.py:112` | `def run_all(self, text, host)` |
| `OpEvent` | class | `modules/operation.py:52` | `class OpEvent` |
| `Operation` | class | `modules/operation.py:79` | `class Operation` |
| `OperationManager` | class | `modules/operation.py:180` | `class OperationManager` |
| `OperationStatus` | class | `modules/operation.py:42` | `class OperationStatus(StrEnum)` |
| `OperationStep` | class | `modules/operation.py:63` | `class OperationStep` |
| `__init__` | method | `modules/operation.py:183` | `def __init__(self)` |
| `create` | method | `modules/operation.py:206` | `def create(self, name, target, apt_name, description)` |
| `from_dict` | method | `modules/operation.py:116` | `def from_dict(cls, d)` |
| `get` | method | `modules/operation.py:199` | `def get(self, op_id)` |
| `get_manager` | function | `modules/operation.py:471` | `def get_manager()` |
| `list` | method | `modules/operation.py:187` | `def list(self)` |
| `log_event` | method | `modules/operation.py:143` | `def log_event(self, step_index, step_name, status, summary, findings_count, error)` |
| `pause` | method | `modules/operation.py:369` | `def pause(self, op_id)` |
| `plan_from_apt` | method | `modules/operation.py:225` | `def plan_from_apt(self, op, playbook_yaml_path)` |
| `record_facts` | method | `modules/operation.py:164` | `def record_facts(self, findings)` |
| `report` | method | `modules/operation.py:431` | `def report(self, op_id)` |
| `resume` | method | `modules/operation.py:378` | `def resume(self, op_id, executor)` |
| `save` | method | `modules/operation.py:134` | `def save(self)` |
| `start` | method | `modules/operation.py:287` | `def start(self, op_id, executor)` |
| `status` | method | `modules/operation.py:396` | `def status(self, op_id)` |
| `stop` | method | `modules/operation.py:386` | `def stop(self, op_id)` |
| `timeline` | method | `modules/operation.py:425` | `def timeline(self, op_id)` |
| `to_dict` | method | `modules/operation.py:98` | `def to_dict(self)` |
| `OperatorProfile` | class | `modules/operator_profiles.py:38` | `class OperatorProfile` |
| `OperatorProfileManager` | class | `modules/operator_profiles.py:77` | `class OperatorProfileManager` |
| `__init__` | method | `modules/operator_profiles.py:88` | `def __init__(self)` |
| `_ensure_team_ca` | method | `modules/operator_profiles.py:93` | `def _ensure_team_ca(self)` |
| `_generate_operator_cert` | method | `modules/operator_profiles.py:130` | `def _generate_operator_cert(self, username)` |
| `_profile_dir` | method | `modules/operator_profiles.py:124` | `def _profile_dir(self, username)` |
| `_profile_path` | method | `modules/operator_profiles.py:127` | `def _profile_path(self, username)` |
| `_save_profile` | method | `modules/operator_profiles.py:255` | `def _save_profile(self, profile)` |
| `create_profile` | method | `modules/operator_profiles.py:192` | `def create_profile(self, username, display_name, role, lhost, lport, listener_port, c2_port, c2_malleable_route...` |
| `delete_profile` | method | `modules/operator_profiles.py:289` | `def delete_profile(self, username)` |
| `effective_config` | method | `modules/operator_profiles.py:360` | `def effective_config(self, username)` |
| `get_attribute` | method | `modules/operator_profiles.py:328` | `def get_attribute(self, username, key, default)` |
| `get_operator_profile_manager` | function | `modules/operator_profiles.py:398` | `def get_operator_profile_manager()` |
| `list_profiles` | method | `modules/operator_profiles.py:300` | `def list_profiles(self)` |
| `load_profile` | method | `modules/operator_profiles.py:260` | `def load_profile(self, username)` |
| `log_action` | method | `modules/operator_profiles.py:335` | `def log_action(self, username, action, details)` |
| `set_attribute` | method | `modules/operator_profiles.py:319` | `def set_attribute(self, username, key, value)` |
| `to_dict` | method | `modules/operator_profiles.py:57` | `def to_dict(self)` |
| `touch_activity` | method | `modules/operator_profiles.py:312` | `def touch_activity(self, username)` |
| `update_profile` | method | `modules/operator_profiles.py:276` | `def update_profile(self, username)` |
| `GateAction` | class | `modules/opsec_scorer.py:180` | `class GateAction(IntEnum)` |
| `GatedOpsecScore` | class | `modules/opsec_scorer.py:303` | `class GatedOpsecScore` |
| `OpsecContext` | class | `modules/opsec_scorer.py:232` | `class OpsecContext` |
| `OpsecScore` | class | `modules/opsec_scorer.py:265` | `class OpsecScore` |
| `OpsecScorer` | class | `modules/opsec_scorer.py:331` | `class OpsecScorer` |
| `OpsecScorerV2` | class | `modules/opsec_scorer.py:559` | `class OpsecScorerV2` |
| `RiskLevel` | class | `modules/opsec_scorer.py:170` | `class RiskLevel(IntEnum)` |
| `__init__` | method | `modules/opsec_scorer.py:343` | `def __init__(self, payload, world_model)` |
| `__init__` | method | `modules/opsec_scorer.py:617` | `def __init__(self, context)` |
| `_build_explanation` | method | `modules/opsec_scorer.py:796` | `def _build_explanation(cmd, noise, detects, gate)` |
| `_build_recommendation` | method | `modules/opsec_scorer.py:544` | `def _build_recommendation(risk_level, mitigations)` |
| `_detection_risk_label` | method | `modules/opsec_scorer.py:532` | `def _detection_risk_label(detectable, noise)` |
| `_estimate_noise` | method | `modules/opsec_scorer.py:426` | `def _estimate_noise(self, command)` |
| `_evasion_reduction` | method | `modules/opsec_scorer.py:498` | `def _evasion_reduction(self, detectable)` |
| `_find_alternatives` | method | `modules/opsec_scorer.py:777` | `def _find_alternatives(cmd)` |
| `_gather_mitigations` | method | `modules/opsec_scorer.py:510` | `def _gather_mitigations(self, detectable, noise)` |
| `_generate_mitigations` | method | `modules/opsec_scorer.py:753` | `def _generate_mitigations(noise, detects)` |
| `_get_host_purpose` | method | `modules/opsec_scorer.py:479` | `def _get_host_purpose(self, rhost)` |
| `_noise_to_risk` | method | `modules/opsec_scorer.py:527` | `def _noise_to_risk(noise)` |
| `_noise_to_risk` | method | `modules/opsec_scorer.py:739` | `def _noise_to_risk(noise)` |
| `_phase_mismatch_penalty` | method | `modules/opsec_scorer.py:448` | `def _phase_mismatch_penalty(self, tool_phase, override)` |
| `_risk_bucket` | function | `modules/opsec_scorer.py:189` | `def _risk_bucket(noise)` |
| `_risk_label` | function | `modules/opsec_scorer.py:207` | `def _risk_label(noise)` |
| `_risk_level` | function | `modules/opsec_scorer.py:219` | `def _risk_level(noise)` |
| `_risk_to_gate` | method | `modules/opsec_scorer.py:743` | `def _risk_to_gate(self, risk)` |
| `_target_sensitivity_bonus` | method | `modules/opsec_scorer.py:470` | `def _target_sensitivity_bonus(self, rhost)` |
| `assess` | method | `modules/opsec_scorer.py:622` | `def assess(self, command, extra_context)` |
| `evasion_active` | method | `modules/opsec_scorer.py:352` | `def evasion_active(self)` |
| `get_trend` | method | `modules/opsec_scorer.py:709` | `def get_trend(self)` |
| `score` | method | `modules/opsec_scorer.py:365` | `def score(self, command, rhost, phase_override)` |
| `score_batch` | method | `modules/opsec_scorer.py:413` | `def score_batch(self, commands, rhost)` |
| `score_command` | function | `modules/opsec_scorer.py:811` | `def score_command(command, payload, rhost)` |
| `should_allow` | method | `modules/opsec_scorer.py:696` | `def should_allow(self, command)` |
| `suggest_mitigations` | method | `modules/opsec_scorer.py:417` | `def suggest_mitigations(self, command, detectable_by)` |
| `to_dict` | method | `modules/opsec_scorer.py:288` | `def to_dict(self)` |
| `traffic_morphing_active` | method | `modules/opsec_scorer.py:357` | `def traffic_morphing_active(self)` |
| `_default_profile_name` | function | `modules/orchestrator_config.py:241` | `def _default_profile_name(data)` |
| `_fallback_profile` | function | `modules/orchestrator_config.py:161` | `def _fallback_profile()` |
| `_invalidate` | function | `modules/orchestrator_config.py:101` | `def _invalidate()` |
| `_merge_profile` | function | `modules/orchestrator_config.py:191` | `def _merge_profile(parent, child)` |
| `_merge_stage` | function | `modules/orchestrator_config.py:175` | `def _merge_stage(base, override)` |
| `_payload` | function | `modules/orchestrator_config.py:114` | `def _payload()` |
| `_read_yaml` | function | `modules/orchestrator_config.py:137` | `def _read_yaml(path)` |
| `_resolve_profile` | function | `modules/orchestrator_config.py:211` | `def _resolve_profile(name, raw_profiles, stack)` |
| `_save` | function | `modules/orchestrator_config.py:129` | `def _save(payload)` |
| `_section` | function | `modules/orchestrator_config.py:124` | `def _section(payload)` |
| `active_profile` | function | `modules/orchestrator_config.py:251` | `def active_profile()` |
| `budget` | function | `modules/orchestrator_config.py:301` | `def budget()` |
| `chain_defaults` | function | `modules/orchestrator_config.py:308` | `def chain_defaults()` |
| `effective_verbs` | function | `modules/orchestrator_config.py:394` | `def effective_verbs()` |
| `limits` | function | `modules/orchestrator_config.py:294` | `def limits()` |
| `profile_config` | function | `modules/orchestrator_config.py:263` | `def profile_config(name)` |
| `profiles` | function | `modules/orchestrator_config.py:226` | `def profiles()` |
| `reload` | function | `modules/orchestrator_config.py:109` | `def reload()` |
| `remove_verb` | function | `modules/orchestrator_config.py:518` | `def remove_verb(name)` |
| `reset` | function | `modules/orchestrator_config.py:539` | `def reset()` |
| `set_profile` | function | `modules/orchestrator_config.py:270` | `def set_profile(name)` |
| `set_stage` | function | `modules/orchestrator_config.py:369` | `def set_stage(name, enabled)` |
| `sinks` | function | `modules/orchestrator_config.py:317` | `def sinks()` |
| `stage_enabled` | function | `modules/orchestrator_config.py:358` | `def stage_enabled(name)` |
| `stage_params` | function | `modules/orchestrator_config.py:364` | `def stage_params(name)` |
| `stages` | function | `modules/orchestrator_config.py:328` | `def stages()` |
| `upsert_verb` | function | `modules/orchestrator_config.py:461` | `def upsert_verb(name)` |
| `validate_config` | function | `modules/orchestrator_config.py:546` | `def validate_config(data)` |
| `verb_config` | function | `modules/orchestrator_config.py:446` | `def verb_config(name)` |
| `verb_enabled` | function | `modules/orchestrator_config.py:455` | `def verb_enabled(name)` |
| `_cache_load` | function | `modules/osint_enrich.py:52` | `def _cache_load(sessions_dir)` |
| `_cache_path` | function | `modules/osint_enrich.py:47` | `def _cache_path(sessions_dir)` |
| `_cache_save` | function | `modules/osint_enrich.py:61` | `def _cache_save(sessions_dir, data)` |
| `_cached` | function | `modules/osint_enrich.py:69` | `def _cached(sessions_dir, key, ttl)` |
| `_get_json` | function | `modules/osint_enrich.py:84` | `def _get_json(url, params)` |
| `_get_text` | function | `modules/osint_enrich.py:110` | `def _get_text(url, params)` |
| `_post_json` | function | `modules/osint_enrich.py:96` | `def _post_json(url, payload)` |
| `_store` | function | `modules/osint_enrich.py:77` | `def _store(sessions_dir, key, data)` |
| `cve_lookup` | function | `modules/osint_enrich.py:122` | `def cve_lookup(cve_id, sessions_dir)` |
| `domain_exposure` | function | `modules/osint_enrich.py:198` | `def domain_exposure(domain, sessions_dir)` |
| `enrich_evidence` | function | `modules/osint_enrich.py:213` | `def enrich_evidence(items, sessions_dir)` |
| `host_geo` | function | `modules/osint_enrich.py:183` | `def host_geo(ip, sessions_dir)` |
| `reverse_dns` | function | `modules/osint_enrich.py:161` | `def reverse_dns(ip, sessions_dir)` |
| `OutcomeBus` | class | `modules/outcome_bus.py:149` | `class OutcomeBus` |
| `OutcomeEvent` | class | `modules/outcome_bus.py:71` | `class OutcomeEvent` |
| `__init__` | method | `modules/outcome_bus.py:152` | `def __init__(self, ledger_path, sink_map)` |
| `_append_ledger` | method | `modules/outcome_bus.py:244` | `def _append_ledger(self, event, statuses)` |
| `_enabled_sinks` | method | `modules/outcome_bus.py:186` | `def _enabled_sinks(self, requested)` |
| `_sink` | method | `modules/outcome_bus.py:171` | `def _sink(self, name)` |
| `category_for_event` | function | `modules/outcome_bus.py:294` | `def category_for_event(kind)` |
| `get_bus` | function | `modules/outcome_bus.py:265` | `def get_bus()` |
| `host_value` | method | `modules/outcome_bus.py:99` | `def host_value(self)` |
| `key` | method | `modules/outcome_bus.py:103` | `def key(self)` |
| `record` | method | `modules/outcome_bus.py:197` | `def record(self, event, sinks)` |
| `record` | function | `modules/outcome_bus.py:279` | `def record(event, sinks)` |
| `record_event` | function | `modules/outcome_bus.py:284` | `def record_event()` |
| `reset` | method | `modules/outcome_bus.py:165` | `def reset(self)` |
| `reset_bus` | function | `modules/outcome_bus.py:274` | `def reset_bus()` |
| `severity_for_event` | function | `modules/outcome_bus.py:289` | `def severity_for_event(severity)` |
| `to_dict` | method | `modules/outcome_bus.py:121` | `def to_dict(self)` |
| `DynamicShellcodePayload` | class | `modules/payload_factory.py:409` | `class DynamicShellcodePayload(PayloadTemplate)` |
| `MsfvenomPayload` | class | `modules/payload_factory.py:322` | `class MsfvenomPayload(PayloadTemplate)` |
| `PayloadFactory` | class | `modules/payload_factory.py:457` | `class PayloadFactory` |
| `PayloadTemplate` | class | `modules/payload_factory.py:216` | `class PayloadTemplate(ABC)` |
| `ReverseShellPayload` | class | `modules/payload_factory.py:251` | `class ReverseShellPayload(PayloadTemplate)` |
| `ShellcodePayload` | class | `modules/payload_factory.py:363` | `class ShellcodePayload(PayloadTemplate)` |
| `WindowsReverseShellPayload` | class | `modules/payload_factory.py:290` | `class WindowsReverseShellPayload(PayloadTemplate)` |
| `__init__` | method | `modules/payload_factory.py:222` | `def __init__(self, name, platform, arch, description, options)` |
| `__init__` | method | `modules/payload_factory.py:254` | `def __init__(self)` |
| `__init__` | method | `modules/payload_factory.py:293` | `def __init__(self)` |
| `__init__` | method | `modules/payload_factory.py:325` | `def __init__(self, name, platform, arch)` |
| `__init__` | method | `modules/payload_factory.py:374` | `def __init__(self, name, platform, arch, description, escaped_hex, patcher)` |
| `__init__` | method | `modules/payload_factory.py:416` | `def __init__(self, name, platform, arch, description, builder)` |
| `__init__` | method | `modules/payload_factory.py:464` | `def __init__(self)` |
| `_apply_format` | method | `modules/payload_factory.py:575` | `def _apply_format(data, fmt)` |
| `_build_linux_x64_reverse_tcp` | function | `modules/payload_factory.py:118` | `def _build_linux_x64_reverse_tcp(lhost, lport)` |
| `_parse_escaped_hex` | function | `modules/payload_factory.py:442` | `def _parse_escaped_hex(escaped)` |
| `_patch_shellcode_x64` | function | `modules/payload_factory.py:190` | `def _patch_shellcode_x64(raw, lhost, lport)` |
| `_register_builtins` | method | `modules/payload_factory.py:468` | `def _register_builtins(self)` |
| `format_payload_table` | function | `modules/payload_factory.py:672` | `def format_payload_table(payloads)` |
| `generate` | method | `modules/payload_factory.py:237` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:272` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:305` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:337` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:397` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:436` | `def generate(self)` |
| `generate` | method | `modules/payload_factory.py:529` | `def generate(self, name, format, output)` |
| `get` | method | `modules/payload_factory.py:525` | `def get(self, name)` |
| `list` | method | `modules/payload_factory.py:516` | `def list(self, platform)` |
| `list_formats` | method | `modules/payload_factory.py:664` | `def list_formats()` |
| `register` | method | `modules/payload_factory.py:512` | `def register(self, template)` |
| `to_dict` | method | `modules/payload_factory.py:241` | `def to_dict(self)` |
| `CampaignResult` | class | `modules/phishing_orchestrator.py:167` | `class CampaignResult` |
| `CampaignTarget` | class | `modules/phishing_orchestrator.py:139` | `class CampaignTarget` |
| `PhishingOrchestrator` | class | `modules/phishing_orchestrator.py:180` | `class PhishingOrchestrator` |
| `PhishingTemplate` | class | `modules/phishing_orchestrator.py:154` | `class PhishingTemplate` |
| `__init__` | method | `modules/phishing_orchestrator.py:316` | `def __init__(self)` |
| `_decrypt_credential` | function | `modules/phishing_orchestrator.py:100` | `def _decrypt_credential(encrypted_b64)` |
| `_derive_credential_key` | function | `modules/phishing_orchestrator.py:57` | `def _derive_credential_key()` |
| `_encrypt_credential` | function | `modules/phishing_orchestrator.py:84` | `def _encrypt_credential(plaintext)` |
| `_generate_landing_page` | method | `modules/phishing_orchestrator.py:683` | `def _generate_landing_page(self, template, target_domain, campaign_id)` |
| `_hash_credential_for_log` | function | `modules/phishing_orchestrator.py:116` | `def _hash_credential_for_log(plaintext)` |
| `_inject_harvester` | method | `modules/phishing_orchestrator.py:769` | `def _inject_harvester(self, html, page_id)` |
| `_load_config` | method | `modules/phishing_orchestrator.py:808` | `def _load_config(self)` |
| `_load_targets_from_file` | method | `modules/phishing_orchestrator.py:644` | `def _load_targets_from_file(self, filepath)` |
| `_send_email` | method | `modules/phishing_orchestrator.py:735` | `def _send_email(self, to_email, subject, html_body, smtp_config)` |
| `_setup_harvesting_endpoint` | method | `modules/phishing_orchestrator.py:723` | `def _setup_harvesting_endpoint(self, campaign_id)` |
| `clone_landing_page` | method | `modules/phishing_orchestrator.py:533` | `def clone_landing_page(self, url)` |
| `generate_template` | method | `modules/phishing_orchestrator.py:486` | `def generate_template(self, name, target_domain, context)` |
| `get_instance` | method | `modules/phishing_orchestrator.py:321` | `def get_instance(cls)` |
| `get_results` | method | `modules/phishing_orchestrator.py:560` | `def get_results(self, campaign_id)` |
| `launch` | method | `modules/phishing_orchestrator.py:332` | `def launch(self, target_domain, template, mode, targets_file, sender_email, sender_password, smtp_host, smtp_port)` |
| `profile_targets` | method | `modules/phishing_orchestrator.py:441` | `def profile_targets(self, domain)` |
| `record_click` | method | `modules/phishing_orchestrator.py:584` | `def record_click(self, campaign_id, email)` |
| `record_credentials` | method | `modules/phishing_orchestrator.py:605` | `def record_credentials(self, campaign_id, email, password)` |
| `ConditionEvaluator` | class | `modules/pipeline_engine.py:326` | `class ConditionEvaluator` |
| `EngagementNarratorAdapter` | class | `modules/pipeline_engine.py:868` | `class EngagementNarratorAdapter(INarratorAdapter)` |
| `INarratorAdapter` | class | `modules/pipeline_engine.py:848` | `class INarratorAdapter(ABC)` |
| `IStepRunner` | class | `modules/pipeline_engine.py:509` | `class IStepRunner(ABC)` |
| `LazyOwnStepRunner` | class | `modules/pipeline_engine.py:523` | `class LazyOwnStepRunner(IStepRunner)` |
| `PipelineCycleError` | class | `modules/pipeline_engine.py:101` | `class PipelineCycleError(PipelineError)` |
| `PipelineEngine` | class | `modules/pipeline_engine.py:908` | `class PipelineEngine` |
| `PipelineError` | class | `modules/pipeline_engine.py:89` | `class PipelineError(Exception)` |
| `PipelineLoader` | class | `modules/pipeline_engine.py:626` | `class PipelineLoader` |
| `PipelineNotFoundError` | class | `modules/pipeline_engine.py:97` | `class PipelineNotFoundError(PipelineError)` |
| `PipelineRun` | class | `modules/pipeline_engine.py:199` | `class PipelineRun` |
| `PipelineSchemaError` | class | `modules/pipeline_engine.py:93` | `class PipelineSchemaError(PipelineError)` |
| `PipelineSpec` | class | `modules/pipeline_engine.py:152` | `class PipelineSpec` |
| `PipelineStep` | class | `modules/pipeline_engine.py:111` | `class PipelineStep` |
| `RunArtifactStore` | class | `modules/pipeline_engine.py:769` | `class RunArtifactStore` |
| `StepDerivers` | class | `modules/pipeline_engine.py:375` | `class StepDerivers` |
| `StepResult` | class | `modules/pipeline_engine.py:163` | `class StepResult` |
| `StepValidator` | class | `modules/pipeline_engine.py:341` | `class StepValidator` |
| `TemplateResolver` | class | `modules/pipeline_engine.py:260` | `class TemplateResolver` |
| `_SilentNarrator` | class | `modules/pipeline_engine.py:863` | `class _SilentNarrator(INarratorAdapter)` |
| `__init__` | method | `modules/pipeline_engine.py:275` | `def __init__(self, context)` |
| `__init__` | method | `modules/pipeline_engine.py:537` | `def __init__(self, runner, onecmd)` |
| `__init__` | method | `modules/pipeline_engine.py:638` | `def __init__(self, pipelines_dir)` |
| `__init__` | method | `modules/pipeline_engine.py:778` | `def __init__(self, runs_dir)` |
| `__init__` | method | `modules/pipeline_engine.py:871` | `def __init__(self, narrator)` |
| `__init__` | method | `modules/pipeline_engine.py:927` | `def __init__(self, runner, loader, artifact_store, narrator, max_nesting)` |
| `_build_context` | method | `modules/pipeline_engine.py:1221` | `def _build_context(self, spec, target, step_results, derived_findings, current_step)` |
| `_derive_auto_populate` | function | `modules/pipeline_engine.py:472` | `def _derive_auto_populate(output)` |
| `_derive_facts_show` | function | `modules/pipeline_engine.py:481` | `def _derive_facts_show(output)` |
| `_derive_lazynmap` | function | `modules/pipeline_engine.py:427` | `def _derive_lazynmap(output)` |
| `_derive_ping` | function | `modules/pipeline_engine.py:412` | `def _derive_ping(output)` |
| `_derive_searchsploit` | function | `modules/pipeline_engine.py:453` | `def _derive_searchsploit(output)` |
| `_heuristic_success` | function | `modules/pipeline_engine.py:587` | `def _heuristic_success(command, output)` |
| `_is_valid_pipeline_name` | function | `modules/pipeline_engine.py:242` | `def _is_valid_pipeline_name(name)` |
| `_load_payload` | function | `modules/pipeline_engine.py:248` | `def _load_payload()` |
| `_make_skipped` | method | `modules/pipeline_engine.py:1206` | `def _make_skipped(step, reason)` |
| `_merge_findings` | method | `modules/pipeline_engine.py:1246` | `def _merge_findings(derived_findings, result)` |
| `_narrate_step` | method | `modules/pipeline_engine.py:1256` | `def _narrate_step(self, result, target)` |
| `_new_run_id` | function | `modules/pipeline_engine.py:238` | `def _new_run_id()` |
| `_now_iso` | function | `modules/pipeline_engine.py:234` | `def _now_iso()` |
| `_read` | method | `modules/pipeline_engine.py:673` | `def _read(self, path)` |
| `_replace` | function | `modules/pipeline_engine.py:282` | `def _replace(match)` |
| `_run_command` | method | `modules/pipeline_engine.py:1077` | `def _run_command(self, step, resolver, target)` |
| `_run_hook` | method | `modules/pipeline_engine.py:1178` | `def _run_hook(self, hook_command, target, timeout_s)` |
| `_run_nested` | method | `modules/pipeline_engine.py:1126` | `def _run_nested(self, step, resolver, target, stack, run)` |
| `_run_via_onecmd` | method | `modules/pipeline_engine.py:566` | `def _run_via_onecmd(self, command, args, target, timeout_s)` |
| `_stringify` | method | `modules/pipeline_engine.py:314` | `def _stringify(value)` |
| `_validate` | method | `modules/pipeline_engine.py:689` | `def _validate(self, raw, name, source)` |
| `_worker` | function | `modules/pipeline_engine.py:1344` | `def _worker()` |
| `cmd_pipeline` | function | `modules/pipeline_engine.py:1436` | `def cmd_pipeline(action, name, target, background)` |
| `derive` | method | `modules/pipeline_engine.py:396` | `def derive(cls, command, output)` |
| `get_default_engine` | function | `modules/pipeline_engine.py:1300` | `def get_default_engine(onecmd)` |
| `is_truthy` | method | `modules/pipeline_engine.py:330` | `def is_truthy(rendered)` |
| `list` | method | `modules/pipeline_engine.py:645` | `def list(self)` |
| `load` | method | `modules/pipeline_engine.py:683` | `def load(self, name)` |
| `loader` | method | `modules/pipeline_engine.py:942` | `def loader(self)` |
| `mcp_pipeline_list` | function | `modules/pipeline_engine.py:1368` | `def mcp_pipeline_list()` |
| `mcp_pipeline_run` | function | `modules/pipeline_engine.py:1314` | `def mcp_pipeline_run(name, target, background, onecmd)` |
| `mcp_pipeline_status` | function | `modules/pipeline_engine.py:1414` | `def mcp_pipeline_status(last_n)` |
| `mcp_pipeline_validate` | function | `modules/pipeline_engine.py:1385` | `def mcp_pipeline_validate(name)` |
| `narrate` | method | `modules/pipeline_engine.py:852` | `def narrate(self, kind, target, message, payload, severity)` |
| `narrate` | method | `modules/pipeline_engine.py:864` | `def narrate(self)` |
| `narrate` | method | `modules/pipeline_engine.py:881` | `def narrate(self, kind, target, message, payload, severity)` |
| `open_run` | method | `modules/pipeline_engine.py:785` | `def open_run(self, pipeline_name, run_id)` |
| `pipelines_dir` | method | `modules/pipeline_engine.py:642` | `def pipelines_dir(self)` |
| `register` | method | `modules/pipeline_engine.py:389` | `def register(cls, command, deriver)` |
| `render` | method | `modules/pipeline_engine.py:278` | `def render(self, template)` |
| `resolve` | method | `modules/pipeline_engine.py:289` | `def resolve(self, dotted_path)` |
| `resolve_path` | method | `modules/pipeline_engine.py:658` | `def resolve_path(self, name)` |
| `run` | method | `modules/pipeline_engine.py:513` | `def run(self, command, args, target, timeout_s)` |
| `run` | method | `modules/pipeline_engine.py:548` | `def run(self, command, args, target, timeout_s)` |
| `run` | method | `modules/pipeline_engine.py:949` | `def run(self, name, target, nesting_stack)` |
| `runs_dir` | method | `modules/pipeline_engine.py:782` | `def runs_dir(self)` |
| `to_context` | method | `modules/pipeline_engine.py:180` | `def to_context(self)` |
| `to_dict` | method | `modules/pipeline_engine.py:213` | `def to_dict(self)` |
| `validate` | method | `modules/pipeline_engine.py:352` | `def validate(predicate, output)` |
| `validate` | method | `modules/pipeline_engine.py:945` | `def validate(self, name)` |
| `write_plan` | method | `modules/pipeline_engine.py:797` | `def write_plan(self, run_dir, spec)` |
| `write_step` | method | `modules/pipeline_engine.py:814` | `def write_step(self, run_dir, result)` |
| `write_summary` | method | `modules/pipeline_engine.py:828` | `def write_summary(self, run_dir, run)` |
| `Frontier` | class | `modules/planner.py:505` | `class Frontier` |
| `PlanCandidate` | class | `modules/planner.py:41` | `class PlanCandidate` |
| `PlanResult` | class | `modules/planner.py:54` | `class PlanResult` |
| `Planner` | class | `modules/planner.py:260` | `class Planner` |
| `TodoItem` | class | `modules/planner.py:452` | `class TodoItem` |
| `TodoList` | class | `modules/planner.py:460` | `class TodoList` |
| `__init__` | method | `modules/planner.py:269` | `def __init__(self, world_model, obs_parser, api_key)` |
| `__init__` | method | `modules/planner.py:468` | `def __init__(self)` |
| `__init__` | method | `modules/planner.py:514` | `def __init__(self, planner, todos)` |
| `__len__` | method | `modules/planner.py:560` | `def __len__(self)` |
| `_build_rationale` | method | `modules/planner.py:374` | `def _build_rationale(chosen, facts, target)` |
| `_gather_facts` | function | `modules/planner.py:64` | `def _gather_facts(world_model, obs_parser)` |
| `_llm_tiebreak` | method | `modules/planner.py:387` | `def _llm_tiebreak(self, target, facts, candidates)` |
| `_parser` | method | `modules/planner.py:294` | `def _parser(self)` |
| `_risk_for` | function | `modules/planner.py:160` | `def _risk_for(technique_id)` |
| `_score_step` | function | `modules/planner.py:225` | `def _score_step(step, facts)` |
| `_wm` | method | `modules/planner.py:279` | `def _wm(self)` |
| `blocks` | method | `modules/planner.py:497` | `def blocks(self, tactic)` |
| `get_planner` | function | `modules/planner.py:446` | `def get_planner(api_key)` |
| `next_ready` | method | `modules/planner.py:489` | `def next_ready(self)` |
| `plan` | method | `modules/planner.py:313` | `def plan(self, target, max_candidates)` |
| `pop` | method | `modules/planner.py:551` | `def pop(self)` |
| `refill` | method | `modules/planner.py:532` | `def refill(self, target, max_intents)` |
| `to_dict` | method | `modules/planner.py:413` | `def to_dict(self, result)` |
| `todo_add` | method | `modules/planner.py:472` | `def todo_add(self, name, requires)` |
| `todo_done` | method | `modules/planner.py:478` | `def todo_done(self, name)` |
| `todos` | method | `modules/planner.py:523` | `def todos(self)` |
| `tried` | method | `modules/planner.py:528` | `def tried(self)` |
| `PlaybookEntry` | class | `modules/playbook_admin.py:40` | `class PlaybookEntry` |
| `_count_steps` | function | `modules/playbook_admin.py:183` | `def _count_steps(data)` |
| `_target_for_write` | function | `modules/playbook_admin.py:337` | `def _target_for_write(path, directory)` |
| `_write_atomic` | function | `modules/playbook_admin.py:282` | `def _write_atomic(target, data)` |
| `_yaml_module` | function | `modules/playbook_admin.py:55` | `def _yaml_module()` |
| `create_playbook` | function | `modules/playbook_admin.py:297` | `def create_playbook(filename)` |
| `delete_playbook` | function | `modules/playbook_admin.py:406` | `def delete_playbook(path, directory)` |
| `load_playbook` | function | `modules/playbook_admin.py:102` | `def load_playbook(path)` |
| `playbook_kind` | function | `modules/playbook_admin.py:123` | `def playbook_kind(data)` |
| `playbook_path` | function | `modules/playbook_admin.py:75` | `def playbook_path(filename, directory)` |
| `playbook_template` | function | `modules/playbook_admin.py:265` | `def playbook_template(name, description, platforms)` |
| `preview_playbook` | function | `modules/playbook_admin.py:251` | `def preview_playbook(path, limit)` |
| `save_playbook_yaml` | function | `modules/playbook_admin.py:377` | `def save_playbook_yaml(path, text, directory)` |
| `scan_playbooks` | function | `modules/playbook_admin.py:231` | `def scan_playbooks(directory)` |
| `slugify` | function | `modules/playbook_admin.py:62` | `def slugify(value)` |
| `summarize` | function | `modules/playbook_admin.py:197` | `def summarize(path)` |
| `update_playbook` | function | `modules/playbook_admin.py:350` | `def update_playbook(path, data, directory)` |
| `validate_playbook` | function | `modules/playbook_admin.py:136` | `def validate_playbook(data)` |
| `Playbook` | class | `modules/playbook_engine.py:133` | `class Playbook` |
| `PlaybookEngine` | class | `modules/playbook_engine.py:375` | `class PlaybookEngine` |
| `PlaybookResult` | class | `modules/playbook_engine.py:173` | `class PlaybookResult` |
| `PlaybookStep` | class | `modules/playbook_engine.py:101` | `class PlaybookStep` |
| `StepResult` | class | `modules/playbook_engine.py:165` | `class StepResult` |
| `_AtomicIndex` | class | `modules/playbook_engine.py:254` | `class _AtomicIndex` |
| `_StixLoader` | class | `modules/playbook_engine.py:185` | `class _StixLoader` |
| `_TechniqueSelector` | class | `modules/playbook_engine.py:311` | `class _TechniqueSelector` |
| `__init__` | method | `modules/playbook_engine.py:188` | `def __init__(self, json_path)` |
| `__init__` | method | `modules/playbook_engine.py:260` | `def __init__(self, atomics_path)` |
| `__init__` | method | `modules/playbook_engine.py:387` | `def __init__(self, world_model, obs_parser, api_key, top_n)` |
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

Next: [SYMBOLS_p19.md](SYMBOLS_p19.md)
