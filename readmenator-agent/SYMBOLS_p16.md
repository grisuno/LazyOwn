# Symbols (page 16 of 38)
Previous: [SYMBOLS_p15.md](SYMBOLS_p15.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_ensure_team_ca` | method | `modules/operator_profiles.py:93` | `def _ensure_team_ca(self)` |
| `_generate_operator_cert` | method | `modules/operator_profiles.py:130` | `def _generate_operator_cert(self, username)` |
| `_profile_dir` | method | `modules/operator_profiles.py:124` | `def _profile_dir(self, username)` |
| `_profile_path` | method | `modules/operator_profiles.py:127` | `def _profile_path(self, username)` |
| `_save_profile` | method | `modules/operator_profiles.py:255` | `def _save_profile(self, profile)` |
| `create_profile` | method | `modules/operator_profiles.py:192` | `def create_profile(self, username, display_name, role, lhost, lport, listener_port, c2_port, c2_malleable_route...` |
| `delete_profile` | method | `modules/operator_profiles.py:289` | `def delete_profile(self, username)` |
| `effective_config` | method | `modules/operator_profiles.py:360` | `def effective_config(self, username)` |
| `get_attribute` | method | `modules/operator_profiles.py:328` | `def get_attribute(self, username, key, default)` |
| `get_operator_profile_manager` | method | `modules/operator_profiles.py:398` | `def get_operator_profile_manager()` |
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
| `_risk_bucket` | method | `modules/opsec_scorer.py:189` | `def _risk_bucket(noise)` |
| `_risk_label` | method | `modules/opsec_scorer.py:207` | `def _risk_label(noise)` |
| `_risk_level` | method | `modules/opsec_scorer.py:219` | `def _risk_level(noise)` |
| `_risk_to_gate` | method | `modules/opsec_scorer.py:743` | `def _risk_to_gate(self, risk)` |
| `_target_sensitivity_bonus` | method | `modules/opsec_scorer.py:470` | `def _target_sensitivity_bonus(self, rhost)` |
| `assess` | method | `modules/opsec_scorer.py:622` | `def assess(self, command, extra_context)` |
| `evasion_active` | method | `modules/opsec_scorer.py:352` | `def evasion_active(self)` |
| `get_trend` | method | `modules/opsec_scorer.py:709` | `def get_trend(self)` |
| `score` | method | `modules/opsec_scorer.py:365` | `def score(self, command, rhost, phase_override)` |
| `score_batch` | method | `modules/opsec_scorer.py:413` | `def score_batch(self, commands, rhost)` |
| `score_command` | method | `modules/opsec_scorer.py:811` | `def score_command(command, payload, rhost)` |
| `should_allow` | method | `modules/opsec_scorer.py:696` | `def should_allow(self, command)` |
| `suggest_mitigations` | method | `modules/opsec_scorer.py:417` | `def suggest_mitigations(self, command, detectable_by)` |
| `to_dict` | method | `modules/opsec_scorer.py:288` | `def to_dict(self)` |
| `traffic_morphing_active` | method | `modules/opsec_scorer.py:357` | `def traffic_morphing_active(self)` |
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
| `_parse_escaped_hex` | method | `modules/payload_factory.py:442` | `def _parse_escaped_hex(escaped)` |
| `_patch_shellcode_x64` | function | `modules/payload_factory.py:190` | `def _patch_shellcode_x64(raw, lhost, lport)` |
| `_register_builtins` | method | `modules/payload_factory.py:468` | `def _register_builtins(self)` |
| `format_payload_table` | method | `modules/payload_factory.py:672` | `def format_payload_table(payloads)` |
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
| `_derive_auto_populate` | method | `modules/pipeline_engine.py:472` | `def _derive_auto_populate(output)` |
| `_derive_facts_show` | method | `modules/pipeline_engine.py:481` | `def _derive_facts_show(output)` |
| `_derive_lazynmap` | method | `modules/pipeline_engine.py:427` | `def _derive_lazynmap(output)` |
| `_derive_ping` | method | `modules/pipeline_engine.py:412` | `def _derive_ping(output)` |
| `_derive_searchsploit` | method | `modules/pipeline_engine.py:453` | `def _derive_searchsploit(output)` |
| `_heuristic_success` | method | `modules/pipeline_engine.py:587` | `def _heuristic_success(command, output)` |
| `_is_valid_pipeline_name` | method | `modules/pipeline_engine.py:242` | `def _is_valid_pipeline_name(name)` |
| `_load_payload` | method | `modules/pipeline_engine.py:248` | `def _load_payload()` |
| `_make_skipped` | method | `modules/pipeline_engine.py:1206` | `def _make_skipped(step, reason)` |
| `_merge_findings` | method | `modules/pipeline_engine.py:1246` | `def _merge_findings(derived_findings, result)` |
| `_narrate_step` | method | `modules/pipeline_engine.py:1256` | `def _narrate_step(self, result, target)` |
| `_new_run_id` | method | `modules/pipeline_engine.py:238` | `def _new_run_id()` |
| `_now_iso` | method | `modules/pipeline_engine.py:234` | `def _now_iso()` |
| `_read` | method | `modules/pipeline_engine.py:673` | `def _read(self, path)` |
| `_replace` | method | `modules/pipeline_engine.py:282` | `def _replace(match)` |
| `_run_command` | method | `modules/pipeline_engine.py:1077` | `def _run_command(self, step, resolver, target)` |
| `_run_hook` | method | `modules/pipeline_engine.py:1178` | `def _run_hook(self, hook_command, target, timeout_s)` |
| `_run_nested` | method | `modules/pipeline_engine.py:1126` | `def _run_nested(self, step, resolver, target, stack, run)` |
| `_run_via_onecmd` | method | `modules/pipeline_engine.py:566` | `def _run_via_onecmd(self, command, args, target, timeout_s)` |
| `_stringify` | method | `modules/pipeline_engine.py:314` | `def _stringify(value)` |
| `_validate` | method | `modules/pipeline_engine.py:689` | `def _validate(self, raw, name, source)` |
| `_worker` | method | `modules/pipeline_engine.py:1344` | `def _worker()` |
| `cmd_pipeline` | method | `modules/pipeline_engine.py:1436` | `def cmd_pipeline(action, name, target, background)` |
| `derive` | method | `modules/pipeline_engine.py:396` | `def derive(cls, command, output)` |
| `get_default_engine` | method | `modules/pipeline_engine.py:1300` | `def get_default_engine(onecmd)` |
| `is_truthy` | method | `modules/pipeline_engine.py:330` | `def is_truthy(rendered)` |
| `list` | method | `modules/pipeline_engine.py:645` | `def list(self)` |
| `load` | method | `modules/pipeline_engine.py:683` | `def load(self, name)` |
| `loader` | method | `modules/pipeline_engine.py:942` | `def loader(self)` |
| `mcp_pipeline_list` | method | `modules/pipeline_engine.py:1368` | `def mcp_pipeline_list()` |
| `mcp_pipeline_run` | method | `modules/pipeline_engine.py:1314` | `def mcp_pipeline_run(name, target, background, onecmd)` |
| `mcp_pipeline_status` | method | `modules/pipeline_engine.py:1414` | `def mcp_pipeline_status(last_n)` |
| `mcp_pipeline_validate` | method | `modules/pipeline_engine.py:1385` | `def mcp_pipeline_validate(name)` |
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
| `_gather_facts` | method | `modules/planner.py:64` | `def _gather_facts(world_model, obs_parser)` |
| `_llm_tiebreak` | method | `modules/planner.py:387` | `def _llm_tiebreak(self, target, facts, candidates)` |
| `_parser` | method | `modules/planner.py:294` | `def _parser(self)` |
| `_risk_for` | method | `modules/planner.py:160` | `def _risk_for(technique_id)` |
| `_score_step` | method | `modules/planner.py:225` | `def _score_step(step, facts)` |
| `_wm` | method | `modules/planner.py:279` | `def _wm(self)` |
| `blocks` | method | `modules/planner.py:497` | `def blocks(self, tactic)` |
| `get_planner` | method | `modules/planner.py:446` | `def get_planner(api_key)` |
| `next_ready` | method | `modules/planner.py:489` | `def next_ready(self)` |
| `plan` | method | `modules/planner.py:313` | `def plan(self, target, max_candidates)` |
| `pop` | method | `modules/planner.py:551` | `def pop(self)` |
| `refill` | method | `modules/planner.py:532` | `def refill(self, target, max_intents)` |
| `to_dict` | method | `modules/planner.py:413` | `def to_dict(self, result)` |
| `todo_add` | method | `modules/planner.py:472` | `def todo_add(self, name, requires)` |
| `todo_done` | method | `modules/planner.py:478` | `def todo_done(self, name)` |
| `todos` | method | `modules/planner.py:523` | `def todos(self)` |
| `tried` | method | `modules/planner.py:528` | `def tried(self)` |
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
| `_local_executor` | method | `modules/playbook_engine.py:713` | `def _local_executor(command, host)` |
| `_obs_parser` | method | `modules/playbook_engine.py:415` | `def _obs_parser(self)` |
| `_world_model` | method | `modules/playbook_engine.py:404` | `def _world_model(self)` |
| `available` | method | `modules/playbook_engine.py:192` | `def available(self)` |
| `available` | method | `modules/playbook_engine.py:264` | `def available(self)` |
| `build` | method | `modules/playbook_engine.py:267` | `def build(self)` |
| `derive` | method | `modules/playbook_engine.py:427` | `def derive(self, target, phase, platform, apt_name)` |
| `execute` | method | `modules/playbook_engine.py:529` | `def execute(self, playbook, executor, dry_run)` |
| `from_dict` | method | `modules/playbook_engine.py:128` | `def from_dict(cls, d)` |
| `from_dict` | method | `modules/playbook_engine.py:152` | `def from_dict(cls, d)` |
| `get_engine` | method | `modules/playbook_engine.py:660` | `def get_engine(api_key)` |
| `load` | method | `modules/playbook_engine.py:602` | `def load(self, path)` |
| `result_summary` | method | `modules/playbook_engine.py:631` | `def result_summary(self, result)` |
| `save` | method | `modules/playbook_engine.py:590` | `def save(self, playbook, path)` |
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
| `_build_pipeline_yaml` | method | `modules/playbook_executor.py:285` | `def _build_pipeline_yaml(playbook, mapper, platform)` |
| `_validate` | method | `modules/playbook_executor.py:235` | `def _validate(self, raw, source_path)` |
| `analyze` | method | `modules/playbook_executor.py:353` | `def analyze(self, name, platform)` |
| `generate_pipeline` | method | `modules/playbook_executor.py:378` | `def generate_pipeline(self, name, platform)` |
| `list` | method | `modules/playbook_executor.py:211` | `def list(self)` |
| `load` | method | `modules/playbook_executor.py:224` | `def load(self, name)` |
| `loader` | method | `modules/playbook_executor.py:350` | `def loader(self)` |
| `playbook_analyze` | method | `modules/playbook_executor.py:422` | `def playbook_analyze(name, platform)` |
| `playbook_generate` | method | `modules/playbook_executor.py:429` | `def playbook_generate(name, platform)` |
| `playbook_list` | method | `modules/playbook_executor.py:416` | `def playbook_list()` |
| `playbook_run` | method | `modules/playbook_executor.py:436` | `def playbook_run(name, platform, target, onecmd)` |
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
| `_load_gtfobins_map` | method | `modules/privesc_predictor.py:617` | `def _load_gtfobins_map()` |
| `_parse_kernel_version` | method | `modules/privesc_predictor.py:136` | `def _parse_kernel_version(version_str)` |
| `_parse_version_from_range` | method | `modules/privesc_predictor.py:153` | `def _parse_version_from_range(range_str)` |
| `_try_llm_analysis` | method | `modules/privesc_predictor.py:655` | `def _try_llm_analysis(profile)` |
| `analyze_privesc` | method | `modules/privesc_predictor.py:742` | `def analyze_privesc(filepath, text)` |
| `capability_vectors` | method | `modules/privesc_predictor.py:361` | `def capability_vectors(profile)` |
| `cron_vectors` | method | `modules/privesc_predictor.py:578` | `def cron_vectors(profile)` |
| `format_crystal_ball_output` | method | `modules/privesc_predictor.py:827` | `def format_crystal_ball_output(result)` |
| `group_vectors` | method | `modules/privesc_predictor.py:463` | `def group_vectors(profile)` |
| `main` | method | `modules/privesc_predictor.py:908` | `def main()` |
| `match_known_cves` | method | `modules/privesc_predictor.py:249` | `def match_known_cves(profile)` |
| `parse_linpeas_output` | method | `modules/privesc_predictor.py:165` | `def parse_linpeas_output(text)` |
| `parse_winpeas_output` | method | `modules/privesc_predictor.py:218` | `def parse_winpeas_output(text)` |
| `sudo_vectors` | method | `modules/privesc_predictor.py:501` | `def sudo_vectors(profile)` |
| `suid_vectors` | method | `modules/privesc_predictor.py:287` | `def suid_vectors(profile)` |
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
| `get_engine` | method | `modules/reactive_engine.py:977` | `def get_engine()` |
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
| `GymAttempt` | class | `modules/redteam_gym.py:282` | `class GymAttempt` |
| `_award_gym_elo` | method | `modules/redteam_gym.py:636` | `def _award_gym_elo(username, elo_bonus)` |
| `_calc_speed_score` | method | `modules/redteam_gym.py:533` | `def _calc_speed_score(elapsed_seconds, max_bonus)` |
| `_calc_stealth_score` | method | `modules/redteam_gym.py:554` | `def _calc_stealth_score(techniques, max_bonus)` |
| `_calc_technique_score` | method | `modules/redteam_gym.py:570` | `def _calc_technique_score(techniques, chal, max_bonus)` |
| `_ensure_gym_dir` | method | `modules/redteam_gym.py:298` | `def _ensure_gym_dir()` |
| `_get_rank` | method | `modules/redteam_gym.py:662` | `def _get_rank(username)` |
| `_get_username` | method | `modules/redteam_gym.py:330` | `def _get_username()` |
| `_load_leaderboard` | method | `modules/redteam_gym.py:303` | `def _load_leaderboard()` |
| `_save_leaderboard` | method | `modules/redteam_gym.py:319` | `def _save_leaderboard(board)` |
| `_update_leaderboard` | method | `modules/redteam_gym.py:592` | `def _update_leaderboard(attempt)` |
| `get_active_challenge` | method | `modules/redteam_gym.py:706` | `def get_active_challenge()` |
| `list_challenges` | method | `modules/redteam_gym.py:357` | `def list_challenges()` |
| `main` | method | `modules/redteam_gym.py:790` | `def main()` |
| `record_external_attempt` | method | `modules/redteam_gym.py:736` | `def record_external_attempt(challenge_id, success, elo_bonus, techniques)` |
| `show_leaderboard` | method | `modules/redteam_gym.py:679` | `def show_leaderboard(top_n)` |
| `start_challenge` | method | `modules/redteam_gym.py:378` | `def start_challenge(challenge_id)` |
| `submit_challenge` | method | `modules/redteam_gym.py:448` | `def submit_challenge(techniques_used, success)` |
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
| `_repl` | method | `modules/resource_script.py:125` | `def _repl(m)` |
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

Next: [SYMBOLS_p17.md](SYMBOLS_p17.md)
