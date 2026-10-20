# Subsystem: modules (page 14 of 15)
Previous: [KB_modules_p13.md](KB_modules_p13.md)

## modules/saas_attacks.py
- Doc: SaaS attacks — Microsoft 365, Google Workspace, Salesforce, ServiceNow exploitation.
- Layer: utility
- Language: py
- Symbols:
  - `SaaSConfig` (class, line 49) `class SaaSConfig`
  - `SaaSEnumerationTools` (class, line 71) `class SaaSEnumerationTools`
  - `SaaSAttackEngine` (class, line 152) `class SaaSAttackEngine`
  - `microsoft365_commands` (method, line 75) `def microsoft365_commands()`
  - `google_workspace_commands` (method, line 100) `def google_workspace_commands()`
  - `salesforce_commands` (method, line 118) `def salesforce_commands()`
  - `servicenow_commands` (method, line 135) `def servicenow_commands()`
  - `__init__` (method, line 163) `def __init__(self, config)`
  - `enumerate_all` (method, line 166) `def enumerate_all(self)`
  - `m365_ews_mail_search` (method, line 179) `def m365_ews_mail_search(self, search_term)`
  - `google_workspace_domain_wide_delegation` (method, line 228) `def google_workspace_domain_wide_delegation(self)`
  - `salesforce_report_mining` (method, line 257) `def salesforce_report_mining(self)`
  - `slack_data_mining` (method, line 286) `def slack_data_mining(self)`
  - `detect_external_sharing` (method, line 327) `def detect_external_sharing(self)`
  - `summary` (method, line 352) `def summary(self)`
- Imported by: `cli/commands/cloud_attacks.py`

## modules/search.py
- Doc: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación...
- Layer: utility
- Language: py
- Imported by: `static/js/showdown-2.1.0.min.js`

## modules/security_sanitizers.py
- Doc: Security sanitizers shared across the LazyOwn framework.
- Layer: utility
- Language: py
- Symbols:
  - `SecurityConfig` (class, line 37) `class SecurityConfig`
  - `HeaderValueSanitizer` (class, line 101) `class HeaderValueSanitizer`
  - `SessionPathResolver` (class, line 162) `class SessionPathResolver`
  - `BindAddressResolver` (class, line 256) `class BindAddressResolver`
  - `CommandRedactor` (class, line 318) `class CommandRedactor`
  - `OutputSanitizer` (class, line 406) `class OutputSanitizer`
  - `build_default_config` (function, line 477) `def build_default_config(payload)`
  - `from_payload` (method, line 68) `def from_payload(cls, payload)`
  - `__init__` (method, line 115) `def __init__(self, config)`
  - `is_valid_name` (method, line 129) `def is_valid_name(self, name)`
  - `sanitize_value` (method, line 139) `def sanitize_value(self, value)`
  - `__init__` (method, line 174) `def __init__(self, base_dir, config)`
  - `base_dir` (method, line 192) `def base_dir(self)`
  - `resolve` (method, line 196) `def resolve(self, untrusted_name)`
  - `file_exists` (method, line 238) `def file_exists(self, untrusted_name)`
  - `__init__` (method, line 269) `def __init__(self, config, preferred_addresses)`
  - `_is_well_formed` (method, line 285) `def _is_well_formed(self, candidate)`
  - `resolve` (method, line 298) `def resolve(self)`
  - `__init__` (method, line 333) `def __init__(self, config)`
  - `_display_username` (method, line 345) `def _display_username(self, username)`
  - `_display_password` (method, line 353) `def _display_password(self, password)`
  - `render` (method, line 359) `def render(self, template, substitutions, username, password)`
  - `__init__` (method, line 418) `def __init__(self, config)`
  - `sanitize` (method, line 429) `def sanitize(self, value)`
  - `_sanitize` (method, line 433) `def _sanitize(self, value, depth)`
- Imported by: `lazyc2.py`, `lazyc2/blueprints/phishing.py`, `modules/lazyown_bprfuzzer.py`, `pwntomate.py`, `tests/test_security_sanitizers.py`

## modules/selector_manager.py
- Doc: Selector manager: deterministic priority cascade with provenance.
- Layer: utility
- Language: py
- Symbols:
  - `Proposal` (class, line 21) `class Proposal`
  - `Selection` (class, line 32) `class Selection`
  - `select` (function, line 42) `def select(proposals, is_blocked)`
- Imported by: `skills/lazyown_mcp.py`, `tests/test_auto_loop_memory.py`

## modules/selfupdate.py
- Doc: Guarded self-update for the LazyOwn working tree.
- Layer: utility
- Language: py
- Symbols:
  - `ReleaseArtifact` (class, line 24) `class ReleaseArtifact`
  - `Updater` (class, line 38) `class Updater`
  - `_run` (function, line 85) `def _run(argv, cwd, timeout)`
  - `_git` (function, line 90) `def _git(args, runner, cwd, timeout)`
  - `current_branch` (function, line 96) `def current_branch(runner)`
  - `dirty` (function, line 102) `def dirty(runner)`
  - `check` (function, line 108) `def check(branch, runner)`
  - `apply` (function, line 140) `def apply(branch, confirm, runner)`
  - `__init__` (method, line 47) `def __init__(self, live_path)`
  - `verify` (method, line 52) `def verify(self, artifact)`
  - `stage` (method, line 57) `def stage(self, artifact, directory)`
  - `rollback` (method, line 77) `def rollback(self)`
- Imported by: `cli/commands/lazyops.py`, `modules/lazy_loop.py`, `tests/test_autonomous_ops.py`, `tests/test_lazy_loop.py`

## modules/session_cleanup.py
- Doc: Ephemeral infrastructure cleanup on shell exit.
- Layer: utility
- Language: py
- Symbols:
  - `find_cloudflared_pids` (function, line 28) `def find_cloudflared_pids(ps_output)`
  - `_run_quiet` (function, line 49) `def _run_quiet(argv, timeout)`
  - `_compose_down` (function, line 66) `def _compose_down(compose_file, label)`
  - `stop_cloudflared_processes` (function, line 94) `def stop_cloudflared_processes()`
  - `cleanup_ephemeral_infra` (function, line 120) `def cleanup_ephemeral_infra()`
- Imported by: `lazyown.py`, `tests/test_infra_disposable.py`

## modules/session_rag.py
- Doc: — ChromaDB-backed RAG over sessions/ artefacts.
- Layer: utility
- Language: py
- Symbols:
  - `_chunk_text` (function, line 88) `def _chunk_text(text, size, overlap)`
  - `_KeywordFallback` (class, line 103) `class _KeywordFallback`
  - `_RagState` (class, line 168) `class _RagState`
  - `SessionRAG` (class, line 188) `class SessionRAG`
  - `get_rag` (function, line 535) `def get_rag()`
  - `__init__` (method, line 111) `def __init__(self)`
  - `load` (method, line 115) `def load(self, path)`
  - `save` (method, line 126) `def save(self, path)`
  - `add` (method, line 136) `def add(self, doc_id, text, meta)`
  - `query` (method, line 146) `def query(self, query_text, n)`
  - `count` (method, line 156) `def count(self)`
  - `reset` (method, line 159) `def reset(self)`
  - `load` (method, line 172) `def load(cls)`
  - `save` (method, line 181) `def save(self)`
  - `__init__` (method, line 191) `def __init__(self)`
  - `_init_backend` (method, line 202) `def _init_backend(self)`
  - `_iter_artefacts` (method, line 248) `def _iter_artefacts(self)`
  - `_index_file` (method, line 265) `def _index_file(self, path, collection_key)`
  - `index_new` (method, line 301) `def index_new(self)`
  - `index_parquet_sources` (method, line 322) `def index_parquet_sources(self, force)`
  - `index_all` (method, line 411) `def index_all(self)`
  - `query` (method, line 439) `def query(self, query_text, n, collection)`
  - `context_for_step` (method, line 489) `def context_for_step(self, phase, target, cmd, n)`
  - `stats` (method, line 509) `def stats(self)`
- Depends on: `core/logging.py`
- Imported by: `cli/commands/mcp_bridge.py`, `modules/reactive_engine.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/integration_autonomous_flow.py`, `tests/test_core_modules.py`

## modules/session_reader.py
- Doc: modules/session_reader.py
- Layer: utility
- Language: py
- Symbols:
  - `ImplantRecord` (class, line 39) `class ImplantRecord`
  - `CampaignTask` (class, line 74) `class CampaignTask`
  - `SessionSummary` (class, line 85) `class SessionSummary`
  - `AbstractReader` (class, line 127) `class AbstractReader(ABC)`
  - `ImplantCSVReader` (class, line 137) `class ImplantCSVReader(AbstractReader)`
  - `CommandOutputReader` (class, line 193) `class CommandOutputReader(AbstractReader)`
  - `DiscoveredHostReader` (class, line 214) `class DiscoveredHostReader(AbstractReader)`
  - `TaskReader` (class, line 232) `class TaskReader(AbstractReader)`
  - `TaskWriter` (class, line 257) `class TaskWriter`
  - `SessionAggregator` (class, line 313) `class SessionAggregator`
  - `get_aggregator` (function, line 347) `def get_aggregator()`
  - `is_privileged` (method, line 55) `def is_privileged(self)`
  - `platform` (method, line 60) `def platform(self)`
  - `ip_list` (method, line 69) `def ip_list(self)`
  - `active_client_ids` (method, line 94) `def active_client_ids(self)`
  - `privileged_sessions` (method, line 101) `def privileged_sessions(self)`
  - `unprivileged_sessions` (method, line 108) `def unprivileged_sessions(self)`
  - `latest_for` (method, line 114) `def latest_for(self, client_id)`
  - `task_by_status` (method, line 118) `def task_by_status(self, status)`
  - `read` (method, line 129) `def read(self, sessions_dir)`
  - `read` (method, line 157) `def read(self, sessions_dir)`
  - `read` (method, line 199) `def read(self, sessions_dir)`
  - `read` (method, line 217) `def read(self, sessions_dir)`
  - `read` (method, line 235) `def read(self, sessions_dir)`
  - `__init__` (method, line 260) `def __init__(self, sessions_dir)`
  - `append` (method, line 263) `def append(self, title, description, operator, status)`
  - `update_status` (method, line 288) `def update_status(self, task_id, status)`
  - `__init__` (method, line 319) `def __init__(self, implant_reader, output_reader, host_reader, task_reader)`
  - `aggregate` (method, line 331) `def aggregate(self, sessions_dir)`
- Imported by: `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`

## modules/session_state.py
- Doc: LazyOwn Session State
- Layer: utility
- Language: py
- Symbols:
  - `_detect_phase` (function, line 50) `def _detect_phase(event_types)`
  - `_read_last_commands` (function, line 75) `def _read_last_commands(n)`
  - `_read_events` (function, line 93) `def _read_events(n)`
  - `_extract_creds_from_events` (function, line 118) `def _extract_creds_from_events(events)`
  - `_extract_hosts` (function, line 133) `def _extract_hosts(rows, payload)`
  - `_summarise_commands` (function, line 175) `def _summarise_commands(rows)`
  - `build_state` (function, line 189) `def build_state()`
  - `refresh` (function, line 240) `def refresh()`
  - `load` (function, line 251) `def load()`
- Imported by: `modules/recommender.py`, `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`

## modules/sidequestion.py
- Doc: Isolated side-question answering against immutable snapshots.
- Layer: utility
- Language: py
- Symbols:
  - `SideConfig` (class, line 19) `class SideConfig`
  - `Snapshot` (class, line 32) `class Snapshot`
  - `SideQuestion` (class, line 42) `class SideQuestion`
  - `SideQuestionService` (class, line 52) `class SideQuestionService`
  - `__init__` (method, line 55) `def __init__(self, answer_fn, config)`
  - `capture` (method, line 66) `def capture(self, task_id, text)`
  - `ask` (method, line 75) `def ask(self, snapshot_id, question)`
  - `cancel` (method, line 104) `def cancel(self, request_id)`
  - `history` (method, line 113) `def history(self, limit, before)`
- Imported by: `cli/commands/ai.py`, `tests/test_autonomous_ops.py`

## modules/sleep_obfuscation.py
- Doc: Sleep obfuscation engine for beacon memory evasion.
- Layer: utility
- Language: py
- Symbols:
  - `OsPlatform` (class, line 57) `class OsPlatform(str, Enum)`
  - `TechniqueRisk` (class, line 64) `class TechniqueRisk(str, Enum)`
  - `SleepTechnique` (class, line 73) `class SleepTechnique`
  - `SleepObfuscationConfig` (class, line 100) `class SleepObfuscationConfig`
  - `SleepTechniqueCatalog` (class, line 163) `class SleepTechniqueCatalog`
  - `_build_default_catalog` (function, line 201) `def _build_default_catalog()`
  - `SleepTechniqueValidator` (class, line 365) `class SleepTechniqueValidator`
  - `SleepObfuscationEngine` (class, line 394) `class SleepObfuscationEngine`
  - `to_dict` (method, line 129) `def to_dict(self)`
  - `from_dict` (method, line 146) `def from_dict(cls, raw)`
  - `__init__` (method, line 170) `def __init__(self)`
  - `register` (method, line 173) `def register(self, technique)`
  - `get` (method, line 177) `def get(self, name)`
  - `list_all` (method, line 184) `def list_all(self)`
  - `list_by_platform` (method, line 192) `def list_by_platform(self, platform)`
  - `list_names` (method, line 196) `def list_names(self)`
  - `validate` (method, line 369) `def validate(config, technique)`
  - `validate_config` (method, line 386) `def validate_config(config)`
  - `__init__` (method, line 407) `def __init__(self, catalog)`
  - `catalog` (method, line 416) `def catalog(self)`
  - `config` (method, line 421) `def config(self)`
  - `detection_resistance` (method, line 426) `def detection_resistance(self)`
  - `select` (method, line 442) `def select(self, technique_name)`
  - `configure` (method, line 449) `def configure(self, technique, overrides)`
  - `validate` (method, line 484) `def validate(self, config)`
  - `recommend` (method, line 500) `def recommend(self, platform)`
  - `to_dict` (method, line 513) `def to_dict(self)`
  - `from_dict` (method, line 522) `def from_dict(cls, raw)`
- Depends on: `cli/commands/enum.py`, `core/logging.py`
- Imported by: `cli/commands/sleep_obfuscation.py`, `modules/beacon_config_builder.py`, `tests/test_sleep_obfuscation.py`

## modules/smbver.sh
- Doc: Author: rewardone Description: Requires root or enough permissions to use tcpdump Will listen...
- Layer: utility
- Language: sh

## modules/socks_proxy.py
- Doc: SOCKS5 proxy engine for tunneling traffic through LazyOwn beacons.
- Layer: utility
- Language: py
- Symbols:
  - `SocksAuthMethod` (class, line 65) `class SocksAuthMethod(IntEnum)`
  - `SocksCommand` (class, line 74) `class SocksCommand(IntEnum)`
  - `SocksAddressType` (class, line 82) `class SocksAddressType(IntEnum)`
  - `SocksReply` (class, line 90) `class SocksReply(IntEnum)`
  - `SocksSession` (class, line 120) `class SocksSession`
  - `SocksProxyConfig` (class, line 166) `class SocksProxyConfig`
  - `SocksValidator` (class, line 244) `class SocksValidator`
  - `SocksProxyEngine` (class, line 368) `class SocksProxyEngine`
  - `message` (method, line 103) `def message(self)`
  - `elapsed_seconds` (method, line 144) `def elapsed_seconds(self)`
  - `to_dict` (method, line 150) `def to_dict(self)`
  - `to_dict` (method, line 199) `def to_dict(self)`
  - `from_dict` (method, line 218) `def from_dict(cls, raw)`
  - `validate_config` (method, line 253) `def validate_config(config)`
  - `validate_request` (method, line 300) `def validate_request(command, address_type, host, port, config)`
  - `_check_access_control` (method, line 340) `def _check_access_control(host, port, config)`
  - `__init__` (method, line 381) `def __init__(self, config)`
  - `config` (method, line 387) `def config(self)`
  - `sessions` (method, line 392) `def sessions(self)`
  - `session_count` (method, line 397) `def session_count(self)`
  - `validate` (method, line 401) `def validate(self, config)`
  - `build_spec` (method, line 413) `def build_spec(self)`
  - `create_session` (method, line 436) `def create_session(self, session_id, target_host, target_port, beacon_client_id)`
  - `remove_session` (method, line 475) `def remove_session(self, session_id)`
  - `get_session` (method, line 482) `def get_session(self, session_id)`
  - `add_bytes` (method, line 486) `def add_bytes(self, session_id, sent, received)`
  - `cleanup_expired` (method, line 497) `def cleanup_expired(self)`
  - `list_sessions` (method, line 511) `def list_sessions(self)`
  - `_find_oldest_session` (method, line 515) `def _find_oldest_session(self)`
  - `from_dict` (method, line 522) `def from_dict(cls, raw)`
  - `from_payload` (method, line 528) `def from_payload(cls, payload)`
- Depends on: `cli/commands/enum.py`, `core/logging.py`
- Imported by: `cli/commands/socks_proxy.py`, `modules/beacon_config_builder.py`, `tests/test_socks_proxy.py`

## modules/staged_delivery.py
- Doc: Staged payload delivery — HTA, Office macros, LNK files, ISO/VHD packaging.
- Layer: utility
- Language: py
- Symbols:
  - `StageDeliveryConfig` (class, line 25) `class StageDeliveryConfig`
  - `StagedDeliveryFactory` (class, line 51) `class StagedDeliveryFactory`
  - `__init__` (method, line 83) `def __init__(self, config, output_dir)`
  - `_obfuscate_powershell` (method, line 88) `def _obfuscate_powershell(self, code)`
  - `_obfuscate_vbscript` (method, line 95) `def _obfuscate_vbscript(self, code)`
  - `_payload_command` (method, line 102) `def _payload_command(self)`
  - `generate_hta` (method, line 134) `def generate_hta(self)`
  - `generate_vba_macro` (method, line 171) `def generate_vba_macro(self)`
  - `generate_xlm_macro` (method, line 219) `def generate_xlm_macro(self)`
  - `generate_lnk` (method, line 237) `def generate_lnk(self)`
  - `generate_iso` (method, line 301) `def generate_iso(self, inner_files)`
  - `_build_primary_volume_descriptor` (method, line 336) `def _build_primary_volume_descriptor(self, files)`
  - `generate_vhd` (method, line 370) `def generate_vhd(self, inner_files)`
  - `generate_all` (method, line 420) `def generate_all(self)`
  - `generate_phishing_page` (method, line 460) `def generate_phishing_page(self, template)`
  - `_office365_phish` (method, line 476) `def _office365_phish(self)`
  - `_gmail_phish` (method, line 504) `def _gmail_phish(self)`
  - `_outlook_phish` (method, line 532) `def _outlook_phish(self)`
- Imported by: `cli/commands/payload_arsenal.py`

## modules/state_manager.py
- Doc: UnifiedStateManager — single source of truth for all LazyOwn campaign state.
- Layer: utility
- Language: py
- Symbols:
  - `_load_json` (function, line 43) `def _load_json(path)`
  - `_save_json` (function, line 53) `def _save_json(path, data)`
  - `HostSummary` (class, line 65) `class HostSummary`
  - `SessionSnapshot` (class, line 76) `class SessionSnapshot`
  - `StateManager` (class, line 92) `class StateManager`
  - `get_state_manager` (function, line 776) `def get_state_manager()`
  - `__init__` (method, line 107) `def __init__(self, db_path, sessions_dir, world_model_path, facts_path)`
  - `instance` (method, line 129) `def instance(cls)`
  - `db` (method, line 137) `def db(self)`
  - `workspace_id` (method, line 146) `def workspace_id(self)`
  - `_ensure_workspace` (method, line 151) `def _ensure_workspace(self)`
  - `set_payload` (method, line 165) `def set_payload(self, payload)`
  - `_publish` (method, line 169) `def _publish(self, category, event_type, payload)`
  - `_find_host` (method, line 184) `def _find_host(self, address)`
  - `_cred_list_for_host` (method, line 192) `def _cred_list_for_host(self, host_id)`
  - `_vuln_list_for_host` (method, line 197) `def _vuln_list_for_host(self, host_id)`
  - `close` (method, line 202) `def close(self)`
  - `add_host` (method, line 213) `def add_host(self, address, mac, hostname, os, state)`
  - `get_host` (method, line 236) `def get_host(self, address)`
  - `list_hosts` (method, line 245) `def list_hosts(self)`
  - `advance_host` (method, line 249) `def advance_host(self, address, new_state)`
  - `delete_host` (method, line 275) `def delete_host(self, address)`
  - `add_service` (method, line 287) `def add_service(self, host_address, port, protocol, name, product, version, state)`
  - `list_services` (method, line 319) `def list_services(self, host_address)`
  - `add_credential` (method, line 328) `def add_credential(self, host_address, username, password, realm, cred_type, origin)`
  - `list_credentials` (method, line 362) `def list_credentials(self, host_address)`
  - `add_vulnerability` (method, line 373) `def add_vulnerability(self, host_address, name, severity, description, refs)`
  - `list_vulnerabilities` (method, line 398) `def list_vulnerabilities(self, host_address, severity)`
  - `add_loot` (method, line 411) `def add_loot(self, name, loot_type, path, notes, host_address)`
  - `list_loot` (method, line 444) `def list_loot(self)`
  - `add_note` (method, line 450) `def add_note(self, data, note_type, host_address)`
  - `list_notes` (method, line 473) `def list_notes(self)`
  - `import_nmap_xml` (method, line 479) `def import_nmap_xml(self, xml_path)`
  - `import_nmap_from_facts` (method, line 495) `def import_nmap_from_facts(self, facts)`
  - `status` (method, line 550) `def status(self)`
  - `_sync_world_model_cache` (method, line 556) `def _sync_world_model_cache(self)`
  - `get_world_model_cache` (method, line 606) `def get_world_model_cache(self)`
  - `load_world_model` (method, line 612) `def load_world_model(self)`
  - `session_snapshot` (method, line 653) `def session_snapshot(self)`
  - `export_csv` (method, line 757) `def export_csv(self, table)`
  - `export_summary` (method, line 761) `def export_summary(self)`
- Depends on: `core/logging.py`, `modules/db.py`, `modules/event_bus.py`, `modules/world_model.py`
- Imported by: `cli/commands/automation.py`, `lazyc2.py`, `lazyc2/blueprints/beacon.py`, `lazyown.py`, `modules/conditional_hooks.py`, `modules/event_consumers.py`, `modules/unified_bridge.py`

## modules/stego_video.py
- Doc: Video steganography addon for LazyOwn.
- Layer: utility
- Language: py
- Symbols:
  - `load_payload_file` (function, line 26) `def load_payload_file()`
  - `is_zip` (function, line 36) `def is_zip(path)`
  - `is_video` (function, line 40) `def is_video(path)`
  - `prompt_path` (function, line 44) `def prompt_path(message)`
  - `resolve_path` (function, line 52) `def resolve_path(arg_path, payload_file, validator, kind)`
  - `generate_carrier` (function, line 61) `def generate_carrier(output)`
  - `encode` (function, line 75) `def encode(zip_path, output_video)`
  - `decode` (function, line 93) `def decode(stego_video, output_zip)`
  - `default_output` (function, line 113) `def default_output(zip_path)`
  - `main` (function, line 118) `def main(argv)`

## modules/sudo_tiocsti.py
- Doc: – Production‑grade TIOCSTI injection with multiple attack modes.
- Layer: utility
- Language: py
- Symbols:
  - `get_controlling_tty` (function, line 52) `def get_controlling_tty()`
  - `inject_byte` (function, line 64) `def inject_byte(fd, byte_char)`
  - `inject_payload` (function, line 79) `def inject_payload(fd, payload, char_delay)`
  - `get_sudo_pids_on_tty` (function, line 102) `def get_sudo_pids_on_tty(tty_path)`
  - `sudo_cache_valid` (function, line 139) `def sudo_cache_valid()`
  - `mode_poll` (function, line 149) `def mode_poll(fd, tty_path)`
  - `mode_prefill` (function, line 175) `def mode_prefill(fd)`
  - `mode_cache` (function, line 185) `def mode_cache(fd)`
  - `main` (function, line 198) `def main()`
- Depends on: `core/logging.py`

## modules/surface_ops.py
- Doc: Pure attack-surface helpers (no cmd2): discovery targets, confirm parsing.
- Layer: utility
- Language: py
- Symbols:
  - `is_ipv4` (function, line 18) `def is_ipv4(value)`
  - `parse_confirm` (function, line 26) `def parse_confirm(answer)`
  - `discovery_targets` (function, line 31) `def discovery_targets(sessions_dir)`
  - `write_world_model_hosts` (function, line 50) `def write_world_model_hosts(document, sessions)`
- Imported by: `cli/commands/surface.py`, `tests/test_estorides_fusion.py`

## modules/tel.py
- Doc: to_numbers: Simula la función toNumbers de JavaScript
- Layer: utility
- Language: py
- Symbols:
  - `get_machine_id` (function, line 10) `def get_machine_id()`
  - `get_version` (function, line 24) `def get_version()`
  - `to_numbers` (function, line 36) `def to_numbers(hex_str)`
  - `to_hex` (function, line 41) `def to_hex(byte_list)`
  - `decrypt_cookie` (function, line 46) `def decrypt_cookie(encrypted, key, iv)`
  - `main` (function, line 53) `def main()`

## modules/test_lazyencoder_decoder.py
- Layer: testing
- Language: py
- Depends on: `modules/lazyencoder_decoder.py`

## modules/threat_model.py
- Doc: — Blue team threat model builder for LazyOwn.
- Layer: business_logic
- Language: py
- Symbols:
  - `_extract_iocs` (function, line 245) `def _extract_iocs(text, first_seen)`
  - `ThreatModelBuilder` (class, line 267) `class ThreatModelBuilder`
  - `get_builder` (function, line 592) `def get_builder()`
  - `build` (method, line 270) `def build(self)`
  - `load` (method, line 293) `def load(self)`
  - `_load_csv` (method, line 305) `def _load_csv(self)`
  - `_build_assets` (method, line 318) `def _build_assets(self, rows)`
  - `_risk_score` (method, line 352) `def _risk_score(self, commands, ports)`
  - `_compromise_indicators` (method, line 388) `def _compromise_indicators(self, commands)`
  - `_build_ttps` (method, line 404) `def _build_ttps(self, rows)`
  - `_build_iocs` (method, line 444) `def _build_iocs(self, rows)`
  - `_build_detection_rules` (method, line 475) `def _build_detection_rules(self, ttps)`
  - `_build_purple_team` (method, line 505) `def _build_purple_team(self, ttps, detection_rules)`
  - `_build_summary` (method, line 560) `def _build_summary(self, rows, assets, ttps)`
  - `_save` (method, line 578) `def _save(self, model)`
  - `_add` (function, line 448) `def _add(ioc)`
- Depends on: `core/logging.py`
- Imported by: `cli/commands/mcp_bridge.py`, `skills/lazyown_groq_agents.py`, `skills/lazyown_mcp.py`, `tests/test_core_modules.py`

## modules/timeline_narrator.py
- Doc: LazyOwn Timeline Narrator
- Layer: utility
- Language: py
- Symbols:
  - `_load_events` (function, line 57) `def _load_events(n)`
  - `_format_events_for_prompt` (function, line 77) `def _format_events_for_prompt(events)`
  - `_call_ai` (function, line 97) `def _call_ai(api_key, events_text, target)`
  - `_write_timeline` (function, line 115) `def _write_timeline(narrative, event_count, target)`
  - `narrate` (function, line 130) `def narrate(api_key, force)`
  - `load_timeline` (function, line 165) `def load_timeline()`
- Depends on: `modules/ai_fallback.py`
- Imported by: `skills/heartbeat.py`, `skills/lazyown_daemon.py`, `skills/lazyown_mcp.py`

## modules/timestomper.py
- Doc: Filesystem timestomping — MACB timestamp manipulation for stealth.
- Layer: utility
- Language: py
- Symbols:
  - `TimestompConfig` (class, line 24) `class TimestompConfig`
  - `FileTimestamps` (class, line 51) `class FileTimestamps`
  - `Timestomper` (class, line 69) `class Timestomper`
  - `__init__` (method, line 106) `def __init__(self, config)`
  - `windows_timestomp_powershell` (method, line 110) `def windows_timestomp_powershell(self)`
  - `windows_timestomp_c` (method, line 152) `def windows_timestomp_c(self)`
  - `linux_timestomp_commands` (method, line 200) `def linux_timestomp_commands(self)`
  - `macos_timestomp_commands` (method, line 241) `def macos_timestomp_commands(self)`
  - `_pick_reference` (method, line 269) `def _pick_reference(self, path, platform)`
  - `generate_random_timestamps` (method, line 280) `def generate_random_timestamps(self, reference_ts, window_days)`
  - `verify_timestamps` (method, line 300) `def verify_timestamps(self, target_paths)`
  - `summary` (method, line 326) `def summary(self)`
- Imported by: `cli/commands/opsec_cleanup.py`

## modules/tmp.sh
- Layer: utility
- Language: sh

## modules/toolset.py
- Doc: Typed tool sets per agent role with shell allowlists.
- Layer: utility
- Language: py
- Symbols:
  - `ToolSeed` (class, line 27) `class ToolSeed`
  - `builtin_seeds` (function, line 35) `def builtin_seeds()`
  - `resolve` (function, line 72) `def resolve(agent, tool_key)`
  - `extract_tool` (function, line 105) `def extract_tool(command)`
  - `validate_shell` (function, line 128) `def validate_shell(role, command)`
- Imported by: `skills/autonomous_daemon.py`


Next: [KB_modules_p15.md](KB_modules_p15.md)
