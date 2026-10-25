# Symbols (page 21 of 45)
Previous: [SYMBOLS_p20.md](SYMBOLS_p20.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `refresh` | function | `modules/session_state.py:240` | `def refresh()` |
| `SideConfig` | class | `modules/sidequestion.py:19` | `class SideConfig` |
| `SideQuestion` | class | `modules/sidequestion.py:42` | `class SideQuestion` |
| `SideQuestionService` | class | `modules/sidequestion.py:52` | `class SideQuestionService` |
| `Snapshot` | class | `modules/sidequestion.py:32` | `class Snapshot` |
| `__init__` | method | `modules/sidequestion.py:55` | `def __init__(self, answer_fn, config)` |
| `ask` | method | `modules/sidequestion.py:75` | `def ask(self, snapshot_id, question)` |
| `cancel` | method | `modules/sidequestion.py:104` | `def cancel(self, request_id)` |
| `capture` | method | `modules/sidequestion.py:66` | `def capture(self, task_id, text)` |
| `history` | method | `modules/sidequestion.py:113` | `def history(self, limit, before)` |
| `apply` | function | `modules/sinks/attack_graph.py:13` | `def apply(event)` |
| `apply` | function | `modules/sinks/c2_surfaces.py:11` | `def apply(event)` |
| `apply` | function | `modules/sinks/campaign_db.py:9` | `def apply(event)` |
| `apply` | function | `modules/sinks/event_bus.py:9` | `def apply(event)` |
| `apply` | function | `modules/sinks/intel_graph.py:13` | `def apply(event)` |
| `apply` | function | `modules/sinks/killchain.py:11` | `def apply(event)` |
| `apply` | function | `modules/sinks/objectives.py:16` | `def apply(event)` |
| `apply` | function | `modules/sinks/routing.py:9` | `def apply(event)` |
| `apply` | function | `modules/sinks/world_model.py:12` | `def apply(event)` |
| `OsPlatform` | class | `modules/sleep_obfuscation.py:57` | `class OsPlatform(str, Enum)` |
| `SleepObfuscationConfig` | class | `modules/sleep_obfuscation.py:100` | `class SleepObfuscationConfig` |
| `SleepObfuscationEngine` | class | `modules/sleep_obfuscation.py:394` | `class SleepObfuscationEngine` |
| `SleepTechnique` | class | `modules/sleep_obfuscation.py:73` | `class SleepTechnique` |
| `SleepTechniqueCatalog` | class | `modules/sleep_obfuscation.py:163` | `class SleepTechniqueCatalog` |
| `SleepTechniqueValidator` | class | `modules/sleep_obfuscation.py:365` | `class SleepTechniqueValidator` |
| `TechniqueRisk` | class | `modules/sleep_obfuscation.py:64` | `class TechniqueRisk(str, Enum)` |
| `__init__` | method | `modules/sleep_obfuscation.py:170` | `def __init__(self)` |
| `__init__` | method | `modules/sleep_obfuscation.py:407` | `def __init__(self, catalog)` |
| `_build_default_catalog` | function | `modules/sleep_obfuscation.py:201` | `def _build_default_catalog()` |
| `catalog` | method | `modules/sleep_obfuscation.py:416` | `def catalog(self)` |
| `config` | method | `modules/sleep_obfuscation.py:421` | `def config(self)` |
| `configure` | method | `modules/sleep_obfuscation.py:449` | `def configure(self, technique, overrides)` |
| `detection_resistance` | method | `modules/sleep_obfuscation.py:426` | `def detection_resistance(self)` |
| `from_dict` | method | `modules/sleep_obfuscation.py:146` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/sleep_obfuscation.py:522` | `def from_dict(cls, raw)` |
| `get` | method | `modules/sleep_obfuscation.py:177` | `def get(self, name)` |
| `list_all` | method | `modules/sleep_obfuscation.py:184` | `def list_all(self)` |
| `list_by_platform` | method | `modules/sleep_obfuscation.py:192` | `def list_by_platform(self, platform)` |
| `list_names` | method | `modules/sleep_obfuscation.py:196` | `def list_names(self)` |
| `recommend` | method | `modules/sleep_obfuscation.py:500` | `def recommend(self, platform)` |
| `register` | method | `modules/sleep_obfuscation.py:173` | `def register(self, technique)` |
| `select` | method | `modules/sleep_obfuscation.py:442` | `def select(self, technique_name)` |
| `to_dict` | method | `modules/sleep_obfuscation.py:129` | `def to_dict(self)` |
| `to_dict` | method | `modules/sleep_obfuscation.py:513` | `def to_dict(self)` |
| `validate` | method | `modules/sleep_obfuscation.py:369` | `def validate(config, technique)` |
| `validate` | method | `modules/sleep_obfuscation.py:484` | `def validate(self, config)` |
| `validate_config` | method | `modules/sleep_obfuscation.py:386` | `def validate_config(config)` |
| `SocksAddressType` | class | `modules/socks_proxy.py:82` | `class SocksAddressType(IntEnum)` |
| `SocksAuthMethod` | class | `modules/socks_proxy.py:65` | `class SocksAuthMethod(IntEnum)` |
| `SocksCommand` | class | `modules/socks_proxy.py:74` | `class SocksCommand(IntEnum)` |
| `SocksProxyConfig` | class | `modules/socks_proxy.py:166` | `class SocksProxyConfig` |
| `SocksProxyEngine` | class | `modules/socks_proxy.py:368` | `class SocksProxyEngine` |
| `SocksReply` | class | `modules/socks_proxy.py:90` | `class SocksReply(IntEnum)` |
| `SocksSession` | class | `modules/socks_proxy.py:120` | `class SocksSession` |
| `SocksValidator` | class | `modules/socks_proxy.py:244` | `class SocksValidator` |
| `__init__` | method | `modules/socks_proxy.py:381` | `def __init__(self, config)` |
| `_check_access_control` | method | `modules/socks_proxy.py:340` | `def _check_access_control(host, port, config)` |
| `_find_oldest_session` | method | `modules/socks_proxy.py:515` | `def _find_oldest_session(self)` |
| `add_bytes` | method | `modules/socks_proxy.py:486` | `def add_bytes(self, session_id, sent, received)` |
| `build_spec` | method | `modules/socks_proxy.py:413` | `def build_spec(self)` |
| `cleanup_expired` | method | `modules/socks_proxy.py:497` | `def cleanup_expired(self)` |
| `config` | method | `modules/socks_proxy.py:387` | `def config(self)` |
| `create_session` | method | `modules/socks_proxy.py:436` | `def create_session(self, session_id, target_host, target_port, beacon_client_id)` |
| `elapsed_seconds` | method | `modules/socks_proxy.py:144` | `def elapsed_seconds(self)` |
| `from_dict` | method | `modules/socks_proxy.py:218` | `def from_dict(cls, raw)` |
| `from_dict` | method | `modules/socks_proxy.py:522` | `def from_dict(cls, raw)` |
| `from_payload` | method | `modules/socks_proxy.py:528` | `def from_payload(cls, payload)` |
| `get_session` | method | `modules/socks_proxy.py:482` | `def get_session(self, session_id)` |
| `list_sessions` | method | `modules/socks_proxy.py:511` | `def list_sessions(self)` |
| `message` | method | `modules/socks_proxy.py:103` | `def message(self)` |
| `remove_session` | method | `modules/socks_proxy.py:475` | `def remove_session(self, session_id)` |
| `session_count` | method | `modules/socks_proxy.py:397` | `def session_count(self)` |
| `sessions` | method | `modules/socks_proxy.py:392` | `def sessions(self)` |
| `to_dict` | method | `modules/socks_proxy.py:150` | `def to_dict(self)` |
| `to_dict` | method | `modules/socks_proxy.py:199` | `def to_dict(self)` |
| `validate` | method | `modules/socks_proxy.py:401` | `def validate(self, config)` |
| `validate_config` | method | `modules/socks_proxy.py:253` | `def validate_config(config)` |
| `validate_request` | method | `modules/socks_proxy.py:300` | `def validate_request(command, address_type, host, port, config)` |
| `StageDeliveryConfig` | class | `modules/staged_delivery.py:25` | `class StageDeliveryConfig` |
| `StagedDeliveryFactory` | class | `modules/staged_delivery.py:51` | `class StagedDeliveryFactory` |
| `__init__` | method | `modules/staged_delivery.py:83` | `def __init__(self, config, output_dir)` |
| `_build_primary_volume_descriptor` | method | `modules/staged_delivery.py:336` | `def _build_primary_volume_descriptor(self, files)` |
| `_gmail_phish` | method | `modules/staged_delivery.py:504` | `def _gmail_phish(self)` |
| `_obfuscate_powershell` | method | `modules/staged_delivery.py:88` | `def _obfuscate_powershell(self, code)` |
| `_obfuscate_vbscript` | method | `modules/staged_delivery.py:95` | `def _obfuscate_vbscript(self, code)` |
| `_office365_phish` | method | `modules/staged_delivery.py:476` | `def _office365_phish(self)` |
| `_outlook_phish` | method | `modules/staged_delivery.py:532` | `def _outlook_phish(self)` |
| `_payload_command` | method | `modules/staged_delivery.py:102` | `def _payload_command(self)` |
| `generate_all` | method | `modules/staged_delivery.py:420` | `def generate_all(self)` |
| `generate_hta` | method | `modules/staged_delivery.py:134` | `def generate_hta(self)` |
| `generate_iso` | method | `modules/staged_delivery.py:301` | `def generate_iso(self, inner_files)` |
| `generate_lnk` | method | `modules/staged_delivery.py:237` | `def generate_lnk(self)` |
| `generate_phishing_page` | method | `modules/staged_delivery.py:460` | `def generate_phishing_page(self, template)` |
| `generate_vba_macro` | method | `modules/staged_delivery.py:171` | `def generate_vba_macro(self)` |
| `generate_vhd` | method | `modules/staged_delivery.py:370` | `def generate_vhd(self, inner_files)` |
| `generate_xlm_macro` | method | `modules/staged_delivery.py:219` | `def generate_xlm_macro(self)` |
| `HostSummary` | class | `modules/state_manager.py:65` | `class HostSummary` |
| `SessionSnapshot` | class | `modules/state_manager.py:76` | `class SessionSnapshot` |
| `StateManager` | class | `modules/state_manager.py:92` | `class StateManager` |
| `__init__` | method | `modules/state_manager.py:107` | `def __init__(self, db_path, sessions_dir, world_model_path, facts_path)` |
| `_cred_list_for_host` | method | `modules/state_manager.py:192` | `def _cred_list_for_host(self, host_id)` |
| `_ensure_workspace` | method | `modules/state_manager.py:151` | `def _ensure_workspace(self)` |
| `_find_host` | method | `modules/state_manager.py:184` | `def _find_host(self, address)` |
| `_load_existing_world_model` | method | `modules/state_manager.py:586` | `def _load_existing_world_model(self)` |
| `_load_json` | function | `modules/state_manager.py:43` | `def _load_json(path)` |
| `_merge_world_model` | method | `modules/state_manager.py:599` | `def _merge_world_model(existing, hosts_data, all_creds, all_vulns)` |
| `_publish` | method | `modules/state_manager.py:169` | `def _publish(self, category, event_type, payload)` |
| `_save_json` | function | `modules/state_manager.py:53` | `def _save_json(path, data)` |
| `_sync_world_model_cache` | method | `modules/state_manager.py:556` | `def _sync_world_model_cache(self)` |
| `_vuln_list_for_host` | method | `modules/state_manager.py:197` | `def _vuln_list_for_host(self, host_id)` |
| `_write_world_model` | method | `modules/state_manager.py:657` | `def _write_world_model(self, data)` |
| `add_credential` | method | `modules/state_manager.py:328` | `def add_credential(self, host_address, username, password, realm, cred_type, origin)` |
| `add_host` | method | `modules/state_manager.py:213` | `def add_host(self, address, mac, hostname, os, state)` |
| `add_loot` | method | `modules/state_manager.py:411` | `def add_loot(self, name, loot_type, path, notes, host_address)` |
| `add_note` | method | `modules/state_manager.py:450` | `def add_note(self, data, note_type, host_address)` |
| `add_service` | method | `modules/state_manager.py:287` | `def add_service(self, host_address, port, protocol, name, product, version, state)` |
| `add_vulnerability` | method | `modules/state_manager.py:373` | `def add_vulnerability(self, host_address, name, severity, description, refs)` |
| `advance_host` | method | `modules/state_manager.py:249` | `def advance_host(self, address, new_state)` |
| `close` | method | `modules/state_manager.py:202` | `def close(self)` |
| `db` | method | `modules/state_manager.py:137` | `def db(self)` |
| `delete_host` | method | `modules/state_manager.py:275` | `def delete_host(self, address)` |
| `export_csv` | method | `modules/state_manager.py:817` | `def export_csv(self, table)` |
| `export_summary` | method | `modules/state_manager.py:821` | `def export_summary(self)` |
| `get_host` | method | `modules/state_manager.py:236` | `def get_host(self, address)` |
| `get_state_manager` | function | `modules/state_manager.py:836` | `def get_state_manager()` |
| `get_world_model_cache` | method | `modules/state_manager.py:666` | `def get_world_model_cache(self)` |
| `import_nmap_from_facts` | method | `modules/state_manager.py:495` | `def import_nmap_from_facts(self, facts)` |
| `import_nmap_xml` | method | `modules/state_manager.py:479` | `def import_nmap_xml(self, xml_path)` |
| `instance` | method | `modules/state_manager.py:129` | `def instance(cls)` |
| `list_credentials` | method | `modules/state_manager.py:362` | `def list_credentials(self, host_address)` |
| `list_hosts` | method | `modules/state_manager.py:245` | `def list_hosts(self)` |
| `list_loot` | method | `modules/state_manager.py:444` | `def list_loot(self)` |
| `list_notes` | method | `modules/state_manager.py:473` | `def list_notes(self)` |
| `list_services` | method | `modules/state_manager.py:319` | `def list_services(self, host_address)` |
| `list_vulnerabilities` | method | `modules/state_manager.py:398` | `def list_vulnerabilities(self, host_address, severity)` |
| `load_world_model` | method | `modules/state_manager.py:672` | `def load_world_model(self)` |
| `session_snapshot` | method | `modules/state_manager.py:713` | `def session_snapshot(self)` |
| `set_payload` | method | `modules/state_manager.py:165` | `def set_payload(self, payload)` |
| `status` | method | `modules/state_manager.py:550` | `def status(self)` |
| `workspace_id` | method | `modules/state_manager.py:146` | `def workspace_id(self)` |
| `decode` | function | `modules/stego_video.py:93` | `def decode(stego_video, output_zip)` |
| `default_output` | function | `modules/stego_video.py:113` | `def default_output(zip_path)` |
| `encode` | function | `modules/stego_video.py:75` | `def encode(zip_path, output_video)` |
| `generate_carrier` | function | `modules/stego_video.py:61` | `def generate_carrier(output)` |
| `is_video` | function | `modules/stego_video.py:40` | `def is_video(path)` |
| `is_zip` | function | `modules/stego_video.py:36` | `def is_zip(path)` |
| `load_payload_file` | function | `modules/stego_video.py:26` | `def load_payload_file()` |
| `main` | function | `modules/stego_video.py:118` | `def main(argv)` |
| `prompt_path` | function | `modules/stego_video.py:44` | `def prompt_path(message)` |
| `resolve_path` | function | `modules/stego_video.py:52` | `def resolve_path(arg_path, payload_file, validator, kind)` |
| `get_controlling_tty` | function | `modules/sudo_tiocsti.py:52` | `def get_controlling_tty()` |
| `get_sudo_pids_on_tty` | function | `modules/sudo_tiocsti.py:102` | `def get_sudo_pids_on_tty(tty_path)` |
| `inject_byte` | function | `modules/sudo_tiocsti.py:64` | `def inject_byte(fd, byte_char)` |
| `inject_payload` | function | `modules/sudo_tiocsti.py:79` | `def inject_payload(fd, payload, char_delay)` |
| `main` | function | `modules/sudo_tiocsti.py:198` | `def main()` |
| `mode_cache` | function | `modules/sudo_tiocsti.py:185` | `def mode_cache(fd)` |
| `mode_poll` | function | `modules/sudo_tiocsti.py:149` | `def mode_poll(fd, tty_path)` |
| `mode_prefill` | function | `modules/sudo_tiocsti.py:175` | `def mode_prefill(fd)` |
| `sudo_cache_valid` | function | `modules/sudo_tiocsti.py:139` | `def sudo_cache_valid()` |
| `discovery_targets` | function | `modules/surface_ops.py:31` | `def discovery_targets(sessions_dir)` |
| `is_ipv4` | function | `modules/surface_ops.py:18` | `def is_ipv4(value)` |
| `parse_confirm` | function | `modules/surface_ops.py:26` | `def parse_confirm(answer)` |
| `write_world_model_hosts` | function | `modules/surface_ops.py:50` | `def write_world_model_hosts(document, sessions)` |
| `decrypt_cookie` | function | `modules/tel.py:46` | `def decrypt_cookie(encrypted, key, iv)` |
| `get_machine_id` | function | `modules/tel.py:10` | `def get_machine_id()` |
| `get_version` | function | `modules/tel.py:24` | `def get_version()` |
| `main` | function | `modules/tel.py:53` | `def main()` |
| `to_hex` | function | `modules/tel.py:41` | `def to_hex(byte_list)` |
| `to_numbers` | function | `modules/tel.py:36` | `def to_numbers(hex_str)` |
| `ThreatModelBuilder` | class | `modules/threat_model.py:267` | `class ThreatModelBuilder` |
| `_add` | function | `modules/threat_model.py:448` | `def _add(ioc)` |
| `_build_assets` | method | `modules/threat_model.py:318` | `def _build_assets(self, rows)` |
| `_build_detection_rules` | method | `modules/threat_model.py:475` | `def _build_detection_rules(self, ttps)` |
| `_build_iocs` | method | `modules/threat_model.py:444` | `def _build_iocs(self, rows)` |
| `_build_purple_team` | method | `modules/threat_model.py:505` | `def _build_purple_team(self, ttps, detection_rules)` |
| `_build_summary` | method | `modules/threat_model.py:560` | `def _build_summary(self, rows, assets, ttps)` |
| `_build_ttps` | method | `modules/threat_model.py:404` | `def _build_ttps(self, rows)` |
| `_compromise_indicators` | method | `modules/threat_model.py:388` | `def _compromise_indicators(self, commands)` |
| `_extract_iocs` | function | `modules/threat_model.py:245` | `def _extract_iocs(text, first_seen)` |
| `_load_csv` | method | `modules/threat_model.py:305` | `def _load_csv(self)` |
| `_risk_score` | method | `modules/threat_model.py:352` | `def _risk_score(self, commands, ports)` |
| `_save` | method | `modules/threat_model.py:578` | `def _save(self, model)` |
| `build` | method | `modules/threat_model.py:270` | `def build(self)` |
| `get_builder` | function | `modules/threat_model.py:592` | `def get_builder()` |
| `load` | method | `modules/threat_model.py:293` | `def load(self)` |
| `_call_ai` | function | `modules/timeline_narrator.py:97` | `def _call_ai(api_key, events_text, target)` |
| `_format_events_for_prompt` | function | `modules/timeline_narrator.py:77` | `def _format_events_for_prompt(events)` |
| `_load_events` | function | `modules/timeline_narrator.py:57` | `def _load_events(n)` |
| `_write_timeline` | function | `modules/timeline_narrator.py:115` | `def _write_timeline(narrative, event_count, target)` |
| `load_timeline` | function | `modules/timeline_narrator.py:165` | `def load_timeline()` |
| `narrate` | function | `modules/timeline_narrator.py:130` | `def narrate(api_key, force)` |
| `FileTimestamps` | class | `modules/timestomper.py:51` | `class FileTimestamps` |
| `TimestompConfig` | class | `modules/timestomper.py:24` | `class TimestompConfig` |
| `Timestomper` | class | `modules/timestomper.py:69` | `class Timestomper` |
| `__init__` | method | `modules/timestomper.py:106` | `def __init__(self, config)` |
| `_pick_reference` | method | `modules/timestomper.py:269` | `def _pick_reference(self, path, platform)` |
| `generate_random_timestamps` | method | `modules/timestomper.py:280` | `def generate_random_timestamps(self, reference_ts, window_days)` |
| `linux_timestomp_commands` | method | `modules/timestomper.py:200` | `def linux_timestomp_commands(self)` |
| `macos_timestomp_commands` | method | `modules/timestomper.py:241` | `def macos_timestomp_commands(self)` |
| `summary` | method | `modules/timestomper.py:326` | `def summary(self)` |
| `verify_timestamps` | method | `modules/timestomper.py:300` | `def verify_timestamps(self, target_paths)` |
| `windows_timestomp_c` | method | `modules/timestomper.py:152` | `def windows_timestomp_c(self)` |
| `windows_timestomp_powershell` | method | `modules/timestomper.py:110` | `def windows_timestomp_powershell(self)` |
| `FakeEngine` | class | `modules/tools/loop_smoke.py:31` | `class FakeEngine` |
| `FakeShell` | class | `modules/tools/loop_smoke.py:22` | `class FakeShell` |
| `__init__` | method | `modules/tools/loop_smoke.py:36` | `def __init__(self)` |
| `bind_shell` | method | `modules/tools/loop_smoke.py:44` | `def bind_shell(self, shell)` |
| `create_task` | method | `modules/tools/loop_smoke.py:52` | `def create_task(self, goal, description)` |
| `main` | function | `modules/tools/loop_smoke.py:114` | `def main()` |
| `onecmd_plus_hooks` | method | `modules/tools/loop_smoke.py:25` | `def onecmd_plus_hooks(self, command)` |
| `orchestrate` | method | `modules/tools/loop_smoke.py:56` | `def orchestrate(self)` |
| `run` | function | `modules/tools/loop_smoke.py:77` | `def run()` |
| `set_concurrency` | method | `modules/tools/loop_smoke.py:48` | `def set_concurrency(self, value)` |
| `_drive` | function | `modules/tools/monitor_smoke.py:40` | `def _drive()` |
| `main` | function | `modules/tools/monitor_smoke.py:59` | `def main()` |
| `run` | function | `modules/tools/monitor_smoke.py:20` | `def run()` |
| `ToolSeed` | class | `modules/toolset.py:27` | `class ToolSeed` |
| `builtin_seeds` | function | `modules/toolset.py:35` | `def builtin_seeds()` |
| `extract_tool` | function | `modules/toolset.py:105` | `def extract_tool(command)` |
| `resolve` | function | `modules/toolset.py:72` | `def resolve(agent, tool_key)` |
| `validate_shell` | function | `modules/toolset.py:128` | `def validate_shell(role, command)` |
| `OnlineFeedbackLoop` | class | `modules/toposwarm_bridge.py:273` | `class OnlineFeedbackLoop` |
| `RoutedCall` | class | `modules/toposwarm_bridge.py:71` | `class RoutedCall` |
| `TopoSwarmBridge` | class | `modules/toposwarm_bridge.py:424` | `class TopoSwarmBridge` |
| `__init__` | method | `modules/toposwarm_bridge.py:296` | `def __init__(self, maxsize)` |
| `__init__` | method | `modules/toposwarm_bridge.py:432` | `def __init__(self)` |
| `_hook` | function | `modules/toposwarm_bridge.py:508` | `def _hook(m, i, o)` |
| `_keyword_route` | function | `modules/toposwarm_bridge.py:202` | `def _keyword_route(prompt)` |
| `_load_toposwarm_modules` | function | `modules/toposwarm_bridge.py:241` | `def _load_toposwarm_modules()` |
| `_neural_route` | method | `modules/toposwarm_bridge.py:493` | `def _neural_route(self, prompt)` |
| `_try_load` | method | `modules/toposwarm_bridge.py:452` | `def _try_load(self)` |
| `available` | method | `modules/toposwarm_bridge.py:444` | `def available(self)` |
| `execute_via_orchestrator` | method | `modules/toposwarm_bridge.py:613` | `def execute_via_orchestrator(self, prompt, no_model)` |
| `feedback` | method | `modules/toposwarm_bridge.py:318` | `def feedback(self, result_id, good, comment, routing_head)` |
| `feedback` | method | `modules/toposwarm_bridge.py:562` | `def feedback(self, result_id, good, comment)` |
| `get_bridge` | function | `modules/toposwarm_bridge.py:645` | `def get_bridge()` |
| `lazyown_command` | method | `modules/toposwarm_bridge.py:81` | `def lazyown_command(self)` |
| `load_feedback_for_training` | method | `modules/toposwarm_bridge.py:389` | `def load_feedback_for_training(self)` |
| `model_loaded` | method | `modules/toposwarm_bridge.py:449` | `def model_loaded(self)` |
| `pending_count` | method | `modules/toposwarm_bridge.py:379` | `def pending_count(self)` |
| `register` | method | `modules/toposwarm_bridge.py:303` | `def register(self, result, hidden)` |
| `route` | method | `modules/toposwarm_bridge.py:586` | `def route(self, prompt)` |
| `stats` | method | `modules/toposwarm_bridge.py:382` | `def stats(self)` |
| `TrafficMorpher` | class | `modules/traffic_morpher.py:18` | `class TrafficMorpher` |
| `__init__` | method | `modules/traffic_morpher.py:77` | `def __init__(self)` |
| `generate_beacon_profile` | method | `modules/traffic_morpher.py:270` | `def generate_beacon_profile(self, name, protocol, jitter_pct, user_agent)` |
| `generate_cloudflare_worker_proxy_config` | method | `modules/traffic_morpher.py:205` | `def generate_cloudflare_worker_proxy_config(self, c2_host, c2_port, auth_token)` |
| `generate_dns_tunnel_payload` | method | `modules/traffic_morpher.py:138` | `def generate_dns_tunnel_payload(self, data, domain)` |
| `generate_icmp_exfil_payload` | method | `modules/traffic_morpher.py:164` | `def generate_icmp_exfil_payload(self, data, chunk_size)` |
| `generate_jitter` | method | `modules/traffic_morpher.py:125` | `def generate_jitter(self, base_delay, jitter_pct)` |
| `generate_traffic_padding` | method | `modules/traffic_morpher.py:108` | `def generate_traffic_padding(self, min_bytes, max_bytes)` |
| `generate_websocket_masking` | method | `modules/traffic_morpher.py:190` | `def generate_websocket_masking(self, data)` |
| `get_cdn_fronting_hosts` | method | `modules/traffic_morpher.py:91` | `def get_cdn_fronting_hosts(self, provider, count)` |
| `get_random_http_headers` | method | `modules/traffic_morpher.py:81` | `def get_random_http_headers(self)` |
| `Exchange` | class | `modules/traffic_recorder.py:80` | `class Exchange` |
| `RecorderConfig` | class | `modules/traffic_recorder.py:24` | `class RecorderConfig` |
| `TrafficRecorder` | class | `modules/traffic_recorder.py:91` | `class TrafficRecorder` |
| `__init__` | method | `modules/traffic_recorder.py:94` | `def __init__(self, base_dir)` |
| `_connect` | method | `modules/traffic_recorder.py:132` | `def _connect(self)` |
| `_fts_query` | method | `modules/traffic_recorder.py:375` | `def _fts_query(query)` |
| `_index_fts` | method | `modules/traffic_recorder.py:323` | `def _index_fts(self, exchange_id, req, resp)` |
| `_migrate_fts` | method | `modules/traffic_recorder.py:115` | `def _migrate_fts(self, conn)` |
| `_scan_bodies` | method | `modules/traffic_recorder.py:422` | `def _scan_bodies(self, needle, limit)` |
| `backfill_fts` | method | `modules/traffic_recorder.py:343` | `def backfill_fts(self, batch)` |
| `count` | method | `modules/traffic_recorder.py:317` | `def count(self)` |
| `export_archive` | method | `modules/traffic_recorder.py:451` | `def export_archive(self, path, limit, task)` |
| `gc` | method | `modules/traffic_recorder.py:587` | `def gc(self, older_than_sec)` |
| `get_body` | method | `modules/traffic_recorder.py:275` | `def get_body(self, exchange_id)` |
| `import_archive` | method | `modules/traffic_recorder.py:493` | `def import_archive(self, path)` |
| `import_inbox` | method | `modules/traffic_recorder.py:554` | `def import_inbox(self, inbox_dir)` |
| `latest_rowid` | method | `modules/traffic_recorder.py:247` | `def latest_rowid(self)` |
| `query` | method | `modules/traffic_recorder.py:253` | `def query(self, host, status, limit, offset, task)` |
| `read_body` | method | `modules/traffic_recorder.py:284` | `def read_body(self, exchange_id, part, offset, length)` |
| `record` | method | `modules/traffic_recorder.py:138` | `def record(self, method, url, status, req_body, resp_body, content_type, req_headers, resp_headers, host, port...` |
| `search_body` | method | `modules/traffic_recorder.py:382` | `def search_body(self, query, limit)` |
| `since` | method | `modules/traffic_recorder.py:230` | `def since(self, rowid, limit)` |
| `url_template` | function | `modules/traffic_recorder.py:69` | `def url_template(url)` |
| `TriggerPolicyConfig` | class | `modules/trigger_policy.py:31` | `class TriggerPolicyConfig` |
| `_coerce_every_sec` | function | `modules/trigger_policy.py:79` | `def _coerce_every_sec(value)` |
| `export_store` | function | `modules/trigger_policy.py:171` | `def export_store(task_id)` |
| `read_policy` | function | `modules/trigger_policy.py:120` | `def read_policy(path)` |
| `remove_seed` | function | `modules/trigger_policy.py:185` | `def remove_seed(kind, arg, task_id)` |
| `seed_store` | function | `modules/trigger_policy.py:146` | `def seed_store(policy, store, task_id)` |
| `seeds` | function | `modules/trigger_policy.py:87` | `def seeds(raw)` |
| `validate_triggers` | function | `modules/trigger_policy.py:40` | `def validate_triggers(raw)` |
| `TTPCoverage` | class | `modules/ttp_coverage.py:65` | `class TTPCoverage` |
| `TTPRow` | class | `modules/ttp_coverage.py:55` | `class TTPRow` |
| `__init__` | method | `modules/ttp_coverage.py:68` | `def __init__(self)` |
| `_blocking_facts` | method | `modules/ttp_coverage.py:168` | `def _blocking_facts(self, tactic)` |
| `_load_state` | method | `modules/ttp_coverage.py:248` | `def _load_state(self)` |
| `_save_state` | method | `modules/ttp_coverage.py:241` | `def _save_state(self)` |
| `add` | method | `modules/ttp_coverage.py:125` | `def add(self, technique_id, name, tactic, status, operation_id)` |
| `compute_ready` | method | `modules/ttp_coverage.py:149` | `def compute_ready(self, available_facts)` |
| `get_coverage` | function | `modules/ttp_coverage.py:260` | `def get_coverage()` |
| `matrix` | method | `modules/ttp_coverage.py:190` | `def matrix(self)` |
| `rebuild_from_operations` | method | `modules/ttp_coverage.py:76` | `def rebuild_from_operations(self)` |
| `status_by_id` | method | `modules/ttp_coverage.py:231` | `def status_by_id(self, technique_id)` |
| `to_dict` | method | `modules/ttp_coverage.py:234` | `def to_dict(self)` |
| `_as_list` | function | `modules/ttpscope_bridge.py:460` | `def _as_list(value)` |
| `_cache_dataset_path` | function | `modules/ttpscope_bridge.py:146` | `def _cache_dataset_path()` |
| `_fallback_matrix_bundle` | function | `modules/ttpscope_bridge.py:384` | `def _fallback_matrix_bundle(platform)` |
| `_fallback_matrix_parquet` | function | `modules/ttpscope_bridge.py:453` | `def _fallback_matrix_parquet(platform)` |
| `_fallback_note` | function | `modules/ttpscope_bridge.py:422` | `def _fallback_note(object_id, text)` |
| `_fallback_notes` | function | `modules/ttpscope_bridge.py:442` | `def _fallback_notes(object_id)` |
| `_fallback_search_bundle` | function | `modules/ttpscope_bridge.py:235` | `def _fallback_search_bundle(query, limit)` |
| `_fallback_search_parquet` | function | `modules/ttpscope_bridge.py:282` | `def _fallback_search_parquet(query, limit)` |
| `_fallback_show_bundle` | function | `modules/ttpscope_bridge.py:303` | `def _fallback_show_bundle(object_id)` |
| `_fallback_show_parquet` | function | `modules/ttpscope_bridge.py:350` | `def _fallback_show_parquet(object_id)` |
| `_fallback_sync` | function | `modules/ttpscope_bridge.py:153` | `def _fallback_sync()` |
| `_load_atomic_parquet` | function | `modules/ttpscope_bridge.py:273` | `def _load_atomic_parquet()` |
| `_load_parquet` | function | `modules/ttpscope_bridge.py:259` | `def _load_parquet(name)` |
| `_load_stix_bundle` | function | `modules/ttpscope_bridge.py:193` | `def _load_stix_bundle()` |
| `_notes_dir` | function | `modules/ttpscope_bridge.py:415` | `def _notes_dir()` |
| `_run_ttpscope` | function | `modules/ttpscope_bridge.py:129` | `def _run_ttpscope(args)` |
| `_slug` | function | `modules/ttpscope_bridge.py:123` | `def _slug(text)` |
| `_stage` | function | `modules/ttpscope_bridge.py:485` | `def _stage(action, slug, stdout, extra)` |
| `_stix_external_id` | function | `modules/ttpscope_bridge.py:211` | `def _stix_external_id(obj)` |
| `_stix_index` | function | `modules/ttpscope_bridge.py:219` | `def _stix_index(bundle)` |
| `do_chain` | function | `modules/ttpscope_bridge.py:582` | `def do_chain(object_id, platform, limit)` |
| `do_matrix` | function | `modules/ttpscope_bridge.py:535` | `def do_matrix(platform)` |
| `do_note` | function | `modules/ttpscope_bridge.py:551` | `def do_note(object_id, text)` |
| `do_notes` | function | `modules/ttpscope_bridge.py:570` | `def do_notes(object_id)` |
| `do_search` | function | `modules/ttpscope_bridge.py:508` | `def do_search(query)` |
| `do_show` | function | `modules/ttpscope_bridge.py:520` | `def do_show(object_id)` |
| `do_sync` | function | `modules/ttpscope_bridge.py:497` | `def do_sync()` |
| `locate_binary` | function | `modules/ttpscope_bridge.py:82` | `def locate_binary()` |
| `main` | function | `modules/ttpscope_bridge.py:679` | `def main()` |
| `run_action` | function | `modules/ttpscope_bridge.py:652` | `def run_action(action)` |
| `validate_object_id` | function | `modules/ttpscope_bridge.py:92` | `def validate_object_id(raw)` |
| `validate_platform` | function | `modules/ttpscope_bridge.py:112` | `def validate_platform(raw)` |
| `validate_query` | function | `modules/ttpscope_bridge.py:100` | `def validate_query(raw)` |
| `DelegateResult` | class | `modules/unified_bridge.py:59` | `class DelegateResult` |
| `KeywordBackend` | class | `modules/unified_bridge.py:75` | `class KeywordBackend(RouteBackend)` |
| `LazyownBridgeBackend` | class | `modules/unified_bridge.py:123` | `class LazyownBridgeBackend(RouteBackend)` |
| `RouteBackend` | class | `modules/unified_bridge.py:67` | `class RouteBackend(ABC)` |
| `RouteResult` | class | `modules/unified_bridge.py:46` | `class RouteResult` |
| `TopoSwarmBackend` | class | `modules/unified_bridge.py:161` | `class TopoSwarmBackend(RouteBackend)` |
| `UnifiedBridge` | class | `modules/unified_bridge.py:195` | `class UnifiedBridge` |
| `__init__` | method | `modules/unified_bridge.py:214` | `def __init__(self)` |
| `_await_agent` | method | `modules/unified_bridge.py:355` | `def _await_agent(self, get_status, agent_id, timeout)` |
| `_detect_phase` | method | `modules/unified_bridge.py:464` | `def _detect_phase(self)` |
| `_get_active_target` | method | `modules/unified_bridge.py:473` | `def _get_active_target(self)` |
| `_init_backends` | method | `modules/unified_bridge.py:219` | `def _init_backends(self)` |
| `_publish` | method | `modules/unified_bridge.py:233` | `def _publish(self, category, event_type, payload)` |
| `_run_agent_command` | method | `modules/unified_bridge.py:384` | `def _run_agent_command(self, command)` |
| `available` | method | `modules/unified_bridge.py:69` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:102` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:126` | `def available(self)` |
| `available` | method | `modules/unified_bridge.py:164` | `def available(self)` |
| `delegate` | method | `modules/unified_bridge.py:300` | `def delegate(self, goal, backend, timeout, max_iterations)` |
| `delegate_task` | function | `modules/unified_bridge.py:488` | `def delegate_task(goal, backend)` |
| `get` | method | `modules/unified_bridge.py:225` | `def get(cls)` |
| `list_backends` | method | `modules/unified_bridge.py:461` | `def list_backends(self)` |
| `route` | method | `modules/unified_bridge.py:72` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:105` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:134` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:173` | `def route(self, prompt, context)` |
| `route` | method | `modules/unified_bridge.py:253` | `def route(self, prompt, context)` |
| `route_prompt` | function | `modules/unified_bridge.py:483` | `def route_prompt(prompt, context)` |
| `set_publish_callback` | method | `modules/unified_bridge.py:230` | `def set_publish_callback(self, cb)` |
| `UnifiedDashboard` | class | `modules/unified_dashboard.py:37` | `class UnifiedDashboard` |
| `__init__` | method | `modules/unified_dashboard.py:44` | `def __init__(self, sessions_dir)` |
| `_collect_daemon_status` | method | `modules/unified_dashboard.py:121` | `def _collect_daemon_status(self)` |
| `_collect_dashboard` | method | `modules/unified_dashboard.py:160` | `def _collect_dashboard(self)` |
| `_collect_graph_advice` | method | `modules/unified_dashboard.py:142` | `def _collect_graph_advice(self)` |
| `_collect_hive_status` | method | `modules/unified_dashboard.py:101` | `def _collect_hive_status(self)` |
| `_collect_live_graph` | method | `modules/unified_dashboard.py:130` | `def _collect_live_graph(self)` |
| `_collect_policy_status` | method | `modules/unified_dashboard.py:111` | `def _collect_policy_status(self)` |
| `_collect_world_model` | method | `modules/unified_dashboard.py:95` | `def _collect_world_model(self)` |
| `_get_dashboard` | method | `modules/unified_dashboard.py:49` | `def _get_dashboard(self)` |
| `_get_graph` | method | `modules/unified_dashboard.py:65` | `def _get_graph(self)` |
| `build_unified_snapshot` | method | `modules/unified_dashboard.py:76` | `def build_unified_snapshot(self)` |
| `export_json` | method | `modules/unified_dashboard.py:251` | `def export_json(self)` |
| `get_unified_dashboard` | function | `modules/unified_dashboard.py:256` | `def get_unified_dashboard(sessions_dir)` |
| `render_unified` | method | `modules/unified_dashboard.py:170` | `def render_unified(self)` |
| `GatekeeperStatus` | function | `modules/venator.py:651` | `def GatekeeperStatus(output_file)` |
| `SIPStatus` | function | `modules/venator.py:637` | `def SIPStatus(output_file)` |
| `amzn_canonical_req` | function | `modules/venator.py:856` | `def amzn_canonical_req(filename_path, headers_list)` |
| `amzn_sig` | function | `modules/venator.py:846` | `def amzn_sig(secret_access_key, data, aws_region, aws_service)` |
| `checkSignature` | function | `modules/venator.py:132` | `def checkSignature(file, bundle)` |
| `datetime_handler` | function | `modules/venator.py:210` | `def datetime_handler(x)` |
| `getApps` | function | `modules/venator.py:741` | `def getApps(path, output_file, ignoreVFlag)` |
| `getBashHistory` | function | `modules/venator.py:786` | `def getBashHistory(output_file, users)` |
| `getChromeDownloads` | function | `modules/venator.py:388` | `def getChromeDownloads(chromeHistoryDbPath, output_file)` |
| `getChromeExtensions` | function | `modules/venator.py:357` | `def getChromeExtensions(path, output_file)` |
| `getConnections` | function | `modules/venator.py:609` | `def getConnections(output_file)` |
| `getCronJobs` | function | `modules/venator.py:494` | `def getCronJobs(users, output_file)` |
| `getEmond` | function | `modules/venator.py:513` | `def getEmond(output_file)` |
| `getEnv` | function | `modules/venator.py:577` | `def getEnv(output_file)` |
| `getEventTaps` | function | `modules/venator.py:763` | `def getEventTaps(output_file)` |
| `getFirefoxExtensions` | function | `modules/venator.py:442` | `def getFirefoxExtensions(path, output_file)` |
| `getHash` | function | `modules/venator.py:112` | `def getHash(file, ignoreVFlag)` |
| `getInstallHistory` | function | `modules/venator.py:477` | `def getInstallHistory(output_file)` |
| `getKext` | function | `modules/venator.py:530` | `def getKext(sipStatus, kextPath, output_file, ignoreVFlag)` |
| `getLaunchAgents` | function | `modules/venator.py:287` | `def getLaunchAgents(path, output_file, ignoreVFlag)` |
| `getLaunchDaemons` | function | `modules/venator.py:302` | `def getLaunchDaemons(path, output_file, ignoreVFlag)` |
| `getLoginItems` | function | `modules/venator.py:706` | `def getLoginItems(path, output_file, ignoreVFlag)` |
| `getPeriodicScripts` | function | `modules/venator.py:592` | `def getPeriodicScripts(output_file)` |
| `getSafariExtensions` | function | `modules/venator.py:338` | `def getSafariExtensions(path, output_file)` |
| `getShellStartupScripts` | function | `modules/venator.py:804` | `def getShellStartupScripts(users, output_file)` |
| `getSystemInfo` | function | `modules/venator.py:66` | `def getSystemInfo(output_file)` |
| `getUUID` | function | `modules/venator.py:38` | `def getUUID()` |
| `getUsers` | function | `modules/venator.py:317` | `def getUsers(output_file)` |
| `getVTResult` | function | `modules/venator.py:83` | `def getVTResult(fileHash)` |
| `hmac_sha256` | function | `modules/venator.py:842` | `def hmac_sha256(key, data)` |
| `io_key` | function | `modules/venator.py:49` | `def io_key(keyname)` |
| `parseAgentsDaemons` | function | `modules/venator.py:215` | `def parseAgentsDaemons(item, path)` |
| `parseApp` | function | `modules/venator.py:663` | `def parseApp(app, ignoreVFlag)` |
| `s3_upload` | function | `modules/venator.py:866` | `def s3_upload(data, content_type, filename_path, access_key_id, secret_access_key, s3_bucket, aws_region)` |
| `VerbCatalogConfig` | class | `modules/verb_catalog.py:76` | `class VerbCatalogConfig` |
| `_addon_discoveries` | function | `modules/verb_catalog.py:137` | `def _addon_discoveries(config)` |
| `_all_discoveries` | function | `modules/verb_catalog.py:181` | `def _all_discoveries(config)` |
| `_builtin_names` | function | `modules/verb_catalog.py:105` | `def _builtin_names()` |
| `_default_config` | function | `modules/verb_catalog.py:99` | `def _default_config()` |
| `_drop_cache` | function | `modules/verb_catalog.py:494` | `def _drop_cache(path_key)` |
| `_phase_fallback` | function | `modules/verb_catalog.py:117` | `def _phase_fallback(verb)` |
| `_risk_fallback` | function | `modules/verb_catalog.py:127` | `def _risk_fallback(verb)` |
| `_write` | function | `modules/verb_catalog.py:470` | `def _write(cfg, verbs)` |
| `catalog_enabled` | function | `modules/verb_catalog.py:349` | `def catalog_enabled(name, config)` |
| `catalog_source` | function | `modules/verb_catalog.py:364` | `def catalog_source(name, config)` |
| `entries` | function | `modules/verb_catalog.py:296` | `def entries(config)` |
| `index_commands` | function | `modules/verb_catalog.py:190` | `def index_commands(config)` |
| `load` | function | `modules/verb_catalog.py:263` | `def load(config)` |
| `search` | function | `modules/verb_catalog.py:516` | `def search(query, config, phase, enabled, limit)` |
| `set_enabled` | function | `modules/verb_catalog.py:378` | `def set_enabled(name, enabled, config)` |
| `stats` | function | `modules/verb_catalog.py:502` | `def stats(config)` |
| `sync` | function | `modules/verb_catalog.py:415` | `def sync(config)` |
| `validate_catalog` | function | `modules/verb_catalog.py:230` | `def validate_catalog(data)` |
| `FactPredicate` | class | `modules/verb_manifest.py:123` | `class FactPredicate` |
| `ManifestCost` | class | `modules/verb_manifest.py:93` | `class ManifestCost` |
| `ManifestNoise` | class | `modules/verb_manifest.py:108` | `class ManifestNoise` |
| `VerbManifest` | class | `modules/verb_manifest.py:188` | `class VerbManifest` |
| `_load_document` | function | `modules/verb_manifest.py:338` | `def _load_document(path)` |
| `_parse_cost` | function | `modules/verb_manifest.py:254` | `def _parse_cost(data)` |
| `_parse_noise` | function | `modules/verb_manifest.py:276` | `def _parse_noise(data)` |
| `args` | method | `modules/verb_manifest.py:152` | `def args(self)` |
| `coverage` | function | `modules/verb_manifest.py:522` | `def coverage(total_verbs, path)` |
| `facts_for_target` | function | `modules/verb_manifest.py:411` | `def facts_for_target(host)` |
| `is_wild` | method | `modules/verb_manifest.py:156` | `def is_wild(self, key)` |
| `manifest_for` | function | `modules/verb_manifest.py:396` | `def manifest_for(verb, path)` |
| `manifests` | function | `modules/verb_manifest.py:371` | `def manifests(path)` |
| `matches` | method | `modules/verb_manifest.py:161` | `def matches(self, other)` |
| `parse_manifest` | function | `modules/verb_manifest.py:296` | `def parse_manifest(verb, data)` |
| `parse_predicate` | function | `modules/verb_manifest.py:222` | `def parse_predicate(data)` |
| `plan_check` | function | `modules/verb_manifest.py:467` | `def plan_check(steps, tokens, path, facts)` |
| `main` | function | `modules/vuln_bot_cli.py:22` | `def main()` |
| `parse_args` | function | `modules/vuln_bot_cli.py:10` | `def parse_args()` |
| `VulnBotCLI` | class | `modules/vulnbot.py:29` | `class VulnBotCLI` |
| `__init__` | method | `modules/vulnbot.py:30` | `def __init__(self, provider, mode, debug, script_path)` |
| `_load_external_tools` | method | `modules/vulnbot.py:109` | `def _load_external_tools(self, script_path)` |
| `_load_model` | method | `modules/vulnbot.py:46` | `def _load_model(self)` |
| `_register_file_tools` | method | `modules/vulnbot.py:83` | `def _register_file_tools(self)` |
| `_setup_agent` | method | `modules/vulnbot.py:61` | `def _setup_agent(self, script_path)` |
| `_stream_agent_response` | method | `modules/vulnbot.py:136` | `def _stream_agent_response(self, prompt)` |
| `add_to_knowledge_base` | method | `modules/vulnbot.py:212` | `def add_to_knowledge_base(self, prompt, response)` |
| `create_complex_prompt` | method | `modules/vulnbot.py:160` | `def create_complex_prompt(self, base_prompt, history, knowledge)` |
| `edit_file` | function | `modules/vulnbot.py:95` | `def edit_file(path, content, old_text)` |
| `generate` | function | `modules/vulnbot.py:139` | `def generate()` |
| `generate` | function | `modules/vulnbot.py:207` | `def generate()` |
| `get_relevant_knowledge` | method | `modules/vulnbot.py:155` | `def get_relevant_knowledge(self, prompt)` |
| `list_files` | function | `modules/vulnbot.py:86` | `def list_files(directory)` |
| `load_event_config` | method | `modules/vulnbot.py:182` | `def load_event_config(self)` |
| `load_knowledge_base` | method | `modules/vulnbot.py:145` | `def load_knowledge_base(self)` |
| `process_with_context` | method | `modules/vulnbot.py:190` | `def process_with_context(self, file_path, event)` |
| `read_file` | function | `modules/vulnbot.py:90` | `def read_file(path)` |
| `read_file_content` | method | `modules/vulnbot.py:176` | `def read_file_content(self, file_path)` |
| `save_knowledge_base` | method | `modules/vulnbot.py:151` | `def save_knowledge_base(self, kb)` |
| `stream_response` | method | `modules/vulnbot.py:206` | `def stream_response(self, prompt)` |
| `WebSocketBeacon` | class | `modules/websocket_beacon.py:46` | `class WebSocketBeacon` |
| `WebSocketC2Handler` | class | `modules/websocket_beacon.py:274` | `class WebSocketC2Handler` |
| `__init__` | method | `modules/websocket_beacon.py:62` | `def __init__(self, server_url, beacon_id, encryption_key, sleep_seconds, jitter_percent, ssl_verify, proxy)` |
| `__init__` | method | `modules/websocket_beacon.py:288` | `def __init__(self, host, port, ssl_context, beacon_callback, task_callback, result_callback)` |
| `_build_message` | method | `modules/websocket_beacon.py:103` | `def _build_message(self, msg_type, payload)` |
| `_decrypt` | method | `modules/websocket_beacon.py:97` | `def _decrypt(self, data)` |
| `_encrypt` | method | `modules/websocket_beacon.py:91` | `def _encrypt(self, data)` |
| `_handle_connection` | method | `modules/websocket_beacon.py:310` | `def _handle_connection(self, websocket, path)` |
| `_jittered_sleep` | method | `modules/websocket_beacon.py:114` | `def _jittered_sleep(self)` |
| `_run_loop` | method | `modules/websocket_beacon.py:410` | `def _run_loop(self, loop)` |
| `check_in` | method | `modules/websocket_beacon.py:157` | `def check_in(self)` |
| `connect` | method | `modules/websocket_beacon.py:122` | `def connect(self)` |
| `list_beacons` | method | `modules/websocket_beacon.py:447` | `def list_beacons(self)` |
| `remove_stale_beacons` | method | `modules/websocket_beacon.py:464` | `def remove_stale_beacons(self, timeout)` |
| `run` | method | `modules/websocket_beacon.py:214` | `def run(self, command_handler)` |
| `send_result` | method | `modules/websocket_beacon.py:191` | `def send_result(self, task_id, output, exit_code)` |
| `send_task` | method | `modules/websocket_beacon.py:416` | `def send_task(self, beacon_id, command)` |
| `shutdown` | method | `modules/websocket_beacon.py:263` | `def shutdown(self)` |
| `start` | method | `modules/websocket_beacon.py:382` | `def start(self)` |
| `start_in_thread` | method | `modules/websocket_beacon.py:399` | `def start_in_thread(self)` |
| `stop` | method | `modules/websocket_beacon.py:392` | `def stop(self)` |
| `BUFFER_SIZE` | macro | `modules/win_rootkit/backup.c:18` | `#define BUFFER_SIZE` |
| `Command` | struct | `modules/win_rootkit/backup.c:27` | `` |
| `HIDE_FILE` | macro | `modules/win_rootkit/backup.c:21` | `#define HIDE_FILE` |
| `KEY_FILE` | macro | `modules/win_rootkit/backup.c:22` | `#define KEY_FILE` |

Next: [SYMBOLS_p22.md](SYMBOLS_p22.md)
